#!/usr/bin/env python3
"""
run_expansion_v15.py — Causes Atlas (Autism) v1.5 Patrick/FoundMyFitness layer

Reads:  expanded_output_v14/*.csv
Writes: expanded_output_v15/*.csv

v1.5 mission: incorporate Dr. Rhonda Patrick's well-evidenced mechanistic
framework where it adds discriminating power not already in the atlas.
Patrick's themes that need explicit representation:

  (1) Vitamin D → TPH2 → serotonin synthesis (Patrick & Ames 2014 FASEB):
      brain serotonin synthesis is regulated by vitamin D via tryptophan
      hydroxylase 2 expression. This is a discrete mechanism, not just
      "vitamin D deficiency" in general.

  (2) Heat shock protein response (HSF1/HSP70/HSP90): induced by heat,
      cold, exercise, sulforaphane. Distinct from oxidative stress.
      Connects sauna, hyperthermia, "fever effect" of autism (Curran
      2007 — ~80% of autistic children show transient improvement
      during fever) to a single underlying mechanism.

  (3) BDNF / neurotrophic signaling: lactate-driven during exercise,
      central to neuroplasticity. We have aerobic exercise as an
      intervention but BDNF was implicit. Make it explicit.

  (4) Membrane phospholipid composition (DHA): Patrick distinguishes
      phospholipid DHA (krill, salmon roe) from triglyceride DHA (most
      fish oils). 10x preferential brain accumulation in phospholipid
      form. Distinct from neuroinflammation pathway.

  (5) Autophagy / proteostasis: AMPK and mTOR are already mechanisms,
      but autophagy itself is the downstream effector and was missing.
      Activated by fasting, exercise, caloric restriction, rapamycin.

Adds:
  4 new mechanisms (HSP response, BDNF signaling, vitamin-D-regulated
                    serotonin synthesis, autophagy/proteostasis)
  4 new hypotheses (serotonin synthesis dysregulation, brain glutathione
                    depletion, DHA membrane phospholipid insufficiency,
                    "fever effect" / HSP-responsive subtype)
  5 new interventions (phospholipid DHA, tryptophan, creatine,
                       time-restricted eating, HIIT)
  6 new landmark sources (Patrick & Ames 2014 + 2015, Curran 2007 fever,
                          hyperthermia mouse model, BDNF in ASD, Werner
                          phospholipid DHA bioavailability)
  Cross-pollination edges connecting Patrick's framework to existing
  nodes.

Determinism: same inputs → bitwise identical outputs.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

INPUT_DIR = Path("expanded_output_v14")
OUTPUT_DIR = Path("expanded_output_v15")


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")


def pad_id(prefix: str, n: int, width: int) -> str:
    return f"{prefix}-{str(n).zfill(width)}"


# ---------------------------------------------------------------------------
# v1.5 content
# ---------------------------------------------------------------------------

NEW_MECHANISMS = [
    ("Heat shock protein (HSF1/HSP70/HSP90) response",
     "other", "hsa04141", "R-HSA-3371556", "",
     "Cellular stress-response chaperone system. Refolds misfolded "
     "proteins, prevents aggregation, modulates inflammation. Induced "
     "by heat (sauna), cold, exercise, sulforaphane. Hypothesized "
     "mechanism for the 'fever effect' in autism (Curran 2007)."),
    ("BDNF / neurotrophin signaling",
     "neural", "hsa04722", "R-HSA-209560", "",
     "Brain-derived neurotrophic factor; central to synaptic "
     "plasticity, neurogenesis, dendritic growth. Reduced serum BDNF "
     "in autism subsets. Lactate-driven by exercise; modulated by "
     "ketones, sulforaphane, omega-3."),
    ("Vitamin-D-regulated serotonin synthesis (TPH2)",
     "neural", "hsa00380", "R-HSA-380615", "",
     "Calcitriol activates TPH2 transcription via VDRE in brain "
     "(serotonin↑) and represses TPH1 in periphery. Patrick & Ames "
     "2014: explains low brain / high peripheral serotonin paradox in "
     "autism. Distinct from kynurenine pathway (MEC-0023)."),
    ("Autophagy / proteostasis",
     "metabolic", "hsa04140", "R-HSA-1632852", "",
     "Cellular quality-control: degradation of damaged proteins and "
     "organelles. Activated by fasting, exercise, caloric restriction, "
     "rapamycin (mTOR inhibition), AMPK signaling. Disrupted in "
     "syndromic autism (TSC, PTEN — mTOR hyperactivation). Distinct "
     "from mTOR pathway itself (MEC-0009) — autophagy is downstream "
     "effector."),
    ("DHA membrane phospholipid composition",
     "neural", "hsa00592", "R-HSA-1483115", "",
     "DHA (22:6n-3) incorporated into neuronal phospholipids "
     "(phosphatidylserine, phosphatidylethanolamine). Determines "
     "membrane fluidity, receptor function, signaling. Phospholipid "
     "DHA accumulates ~10x more in brain than triglyceride DHA "
     "(Werner 2011). Distinct from neuroinflammation effects."),
]


NEW_HYPOTHESES = [
    ("Brain serotonin synthesis dysregulation (TPH2/vitamin D)",
     "metabolic",
     "Low brain serotonin paired with elevated peripheral serotonin "
     "(hyperserotonemia) is a long-documented autism finding. Patrick "
     "& Ames 2014 propose this is mediated by vitamin D regulation of "
     "TPH2 (brain) vs TPH1 (gut) — vitamin D deficiency could "
     "preferentially impair brain serotonin synthesis while leaving "
     "peripheral synthesis intact.",
     "Population-wide signal; vitamin-D-deficient subset",
     "Patrick & Ames 2014 FASEB J hypothesis paper."),

    ("Brain glutathione depletion",
     "metabolic",
     "Reduced GSH/GSSG ratio reported in autism brain and plasma; "
     "compromises antioxidant capacity, methylation, mercury "
     "detoxification. Sulforaphane raises plasma + brain glutathione "
     "(Liu 2020). Distinct from general 'oxidative stress' — the "
     "specific antioxidant pool that's depleted.",
     "Subset; biomarker-defined",
     "James 2004; Liu 2020 brain GSH."),

    ("DHA membrane phospholipid insufficiency",
     "metabolic",
     "Inadequate phospholipid DHA in neuronal membranes during "
     "developmental windows compromises receptor function, synaptic "
     "plasticity, microglial regulation. Distinct from omega-3 "
     "deficiency in general — phospholipid form (krill, salmon roe) "
     "vs triglyceride form (most fish oil) determines brain uptake.",
     "Western diet populations; preconception/prenatal critical",
     "Werner 2011; Patrick FoundMyFitness 2017."),

    ("Heat shock response insufficiency / 'fever effect' subtype",
     "immune",
     "Curran 2007 documented that ~80% of autistic children showed "
     "behavioral improvement during fever. Subsequent animal work "
     "showed whole-body hyperthermia improves behavior in C58/J and "
     "Shank3B- mice. Hypothesis: a subset of autism reflects "
     "insufficient baseline heat shock response that is transiently "
     "rescued by HSF1 activation (fever, sauna, exercise, "
     "sulforaphane).",
     "Subset; ~80% by parental report (Curran 2007)",
     "Curran 2007 Pediatrics; hyperthermia mouse models."),
]


NEW_INTERVENTIONS = [
    ("Phospholipid DHA (krill oil / salmon roe)",
     "supplement", "treatment",
     "Phospholipid form of DHA; ~10x preferential brain accumulation "
     "vs triglyceride DHA. Patrick emphasizes for pregnancy/lactation "
     "and developmental windows. Werner 2011 demonstrated fold-higher "
     "brain DHA from phospholipid form.",
     "500-2000 mg combined EPA+DHA in PL form/day", 50, "otc", "yes",
     "Distinct from INT-0014 standard fish oil."),

    ("Tryptophan supplementation (with vitamin D)",
     "supplement", "treatment",
     "Patrick & Ames recommendation: tryptophan + vitamin D "
     "co-supplementation to support brain serotonin synthesis. "
     "Tryptophan crosses BBB via large neutral amino acid transporter; "
     "vitamin D upregulates TPH2 to use it.",
     "500-2000 mg tryptophan + 2000 IU vit D /day", 25, "otc", "uncertain",
     "Speculative as autism intervention; mechanistic prior strong."),

    ("Creatine monohydrate",
     "supplement", "treatment",
     "Methyl donor (via creatine synthesis cost), brain energy buffer "
     "via phosphocreatine, supports cognitive function. Methylation "
     "protocol component (with choline + glycine).",
     "3-5 g/day", 15, "otc", "yes",
     "Robust safety; emerging cognitive evidence."),

    ("Time-restricted eating / 16:8 fasting",
     "lifestyle", "treatment",
     "Daily eating window restriction (typically 8 hours). Activates "
     "AMPK, autophagy, metabolic flexibility. Less direct autism "
     "evidence; mechanistic prior via mTOR/AMPK axis.",
     "16h fast / 8h eating window", 0, "lifestyle", "uncertain",
     "Pediatric application requires clinical caution."),

    ("HIIT (high-intensity interval training)",
     "lifestyle", "treatment",
     "High-intensity intervals produce more lactate (cf. Brooks "
     "lactate shuttle), driving more BDNF crossing BBB. Patrick + "
     "Gibala emphasize for cognitive/neuroplasticity benefit. "
     "Distinct from steady-state aerobic (INT-0047).",
     "Tabata 4 min, or 4x4 min @ 90% HR_max, 2-3x/week", 0,
     "lifestyle", "yes",
     "Pediatric adaptation needed; very modifiable."),

    ("Whole-body hyperthermia (clinical)",
     "drug", "treatment",
     "Medically supervised raising of core body temperature to "
     "~38.5°C. Activates HSF1/HSP70, modulates immune response. "
     "Investigational for autism per fever-effect rationale.",
     "Single 90-min session, core temp 38.5°C", 500, "rx", "uncertain",
     "Distinct from home sauna (INT-0048); investigational."),
]


NEW_LANDMARKS = [
    # (pmid, title, year, design, sample_size, type, author, targets)
    ("24558199",
     "Vitamin D hormone regulates serotonin synthesis. Part 1: "
     "relevance for autism", 2014, "review", 0, "review", "Patrick",
     [("hypothesis",
       "Brain serotonin synthesis dysregulation (TPH2/vitamin D)",
       "positive"),
      ("mechanism",
       "Vitamin-D-regulated serotonin synthesis (TPH2)", "positive"),
      ("intervention", "Vitamin D3", "positive"),
      ("intervention", "Tryptophan supplementation (with vitamin D)",
       "positive")]),

    ("25653435",
     "Vitamin D and the omega-3 fatty acids control serotonin "
     "synthesis and action, part 2: relevance for ADHD, bipolar "
     "disorder, schizophrenia, and impulsive behavior", 2015,
     "review", 0, "review", "Patrick",
     [("mechanism",
       "Vitamin-D-regulated serotonin synthesis (TPH2)", "positive"),
      ("intervention", "Omega-3 (EPA + DHA)", "positive"),
      ("intervention", "Phospholipid DHA (krill oil / salmon roe)",
       "positive")]),

    ("18055655",
     "Behaviors associated with fever in children with pervasive "
     "developmental disorders", 2007, "case_control", 30, "study",
     "Curran",
     [("hypothesis",
       "Heat shock response insufficiency / 'fever effect' subtype",
       "positive"),
      ("mechanism", "Heat shock protein (HSF1/HSP70/HSP90) response",
       "positive")]),

    ("33408389",
     "Sulforaphane treatment of autism spectrum disorder: a "
     "randomized double-blind placebo-controlled trial replication",
     2020, "rct", 50, "study", "Liu",
     [("intervention", "Sulforaphane (broccoli sprout extract)",
       "positive"),
      ("hypothesis", "Brain glutathione depletion", "positive"),
      ("mechanism", "Heat shock protein (HSF1/HSP70/HSP90) response",
       "positive")]),

    ("21664337",
     "DHA from phospholipid is more bioavailable than DHA from "
     "triglyceride", 2011, "rct", 0, "study", "Werner",
     [("intervention", "Phospholipid DHA (krill oil / salmon roe)",
       "positive"),
      ("hypothesis", "DHA membrane phospholipid insufficiency",
       "positive"),
      ("mechanism", "DHA membrane phospholipid composition",
       "positive")]),

    ("25033474",
     "Sulforaphane treatment of autism spectrum disorder (ASD)",
     2014, "rct", 44, "study", "Singh",
     [("intervention", "Sulforaphane (broccoli sprout extract)",
       "positive"),
      ("mechanism", "Heat shock protein (HSF1/HSP70/HSP90) response",
       "positive"),
      ("hypothesis", "Brain glutathione depletion", "positive")]),

    ("23211717",
     "Brain-derived neurotrophic factor (BDNF) levels in children "
     "with autism spectrum disorder", 2014, "case_control", 47,
     "study", "Halepoto",
     [("mechanism", "BDNF / neurotrophin signaling", "positive"),
      ("intervention", "Aerobic exercise (structured)", "positive")]),

    ("32533039",
     "Whole-body hyperthermia improves behavioural signs in animal "
     "models of autism spectrum disorder", 2023, "mechanistic", 0,
     "study", "Roesner",
     [("hypothesis",
       "Heat shock response insufficiency / 'fever effect' subtype",
       "positive"),
      ("intervention", "Whole-body hyperthermia (clinical)",
       "positive"),
      ("intervention", "Sauna / heat therapy", "positive")]),

    ("15585776",
     "Metabolic biomarkers of increased oxidative stress and "
     "impaired methylation capacity in children with autism",
     2004, "case_control", 119, "study", "James",
     [("hypothesis", "Brain glutathione depletion", "positive"),
      ("mechanism", "Impaired methylation", "positive"),
      ("mechanism", "Oxidative stress", "positive")]),
]


# ---------------------------------------------------------------------------
# Edges
# ---------------------------------------------------------------------------

NEW_HYP_MECH_LINKS = [
    # New hypotheses → new mechanisms
    ("Brain serotonin synthesis dysregulation (TPH2/vitamin D)",
     "Vitamin-D-regulated serotonin synthesis (TPH2)"),
    ("Brain glutathione depletion", "Oxidative stress"),
    ("Brain glutathione depletion", "Impaired methylation"),
    ("DHA membrane phospholipid insufficiency",
     "DHA membrane phospholipid composition"),
    ("DHA membrane phospholipid insufficiency",
     "BDNF / neurotrophin signaling"),
    ("Heat shock response insufficiency / 'fever effect' subtype",
     "Heat shock protein (HSF1/HSP70/HSP90) response"),
    ("Heat shock response insufficiency / 'fever effect' subtype",
     "Neuroinflammation"),
    # Existing hypotheses connecting to new mechanisms
    ("Vitamin D deficiency (maternal + child)",
     "Vitamin-D-regulated serotonin synthesis (TPH2)"),
    ("Maternal omega-3 deficiency",
     "DHA membrane phospholipid composition"),
    ("Maternal immune activation (prenatal infection or autoimmune)",
     "Heat shock protein (HSF1/HSP70/HSP90) response"),
    ("Mitochondrial dysfunction (acquired or inherited)",
     "Autophagy / proteostasis"),
    ("Tuberous sclerosis (TSC1/TSC2)", "Autophagy / proteostasis"),
    ("PTEN hamartoma syndrome", "Autophagy / proteostasis"),
    ("AMPK pathway dysregulation", "Autophagy / proteostasis"),
]

NEW_MECH_PHEN_LINKS = [
    # HSP response → multiple phenotypes (especially the regression /
    # immune-inflammatory phenotype where fever-effect is most reported)
    ("Heat shock protein (HSF1/HSP70/HSP90) response", "PHE-0003"),
    ("BDNF / neurotrophin signaling", "PHE-0006"),  # Fragile X
    ("BDNF / neurotrophin signaling", "PHE-0005"),  # mTOR syndromic
    ("Vitamin-D-regulated serotonin synthesis (TPH2)", "PHE-0001"),
    ("Vitamin-D-regulated serotonin synthesis (TPH2)", "PHE-0007"),
    ("Autophagy / proteostasis", "PHE-0002"),  # mitochondrial
    ("Autophagy / proteostasis", "PHE-0005"),  # mTOR syndromic
    ("DHA membrane phospholipid composition", "PHE-0006"),  # Fragile X
]

NEW_INT_HYP_LINKS = [
    ("Phospholipid DHA (krill oil / salmon roe)",
     "DHA membrane phospholipid insufficiency"),
    ("Phospholipid DHA (krill oil / salmon roe)",
     "Maternal omega-3 deficiency"),
    ("Tryptophan supplementation (with vitamin D)",
     "Brain serotonin synthesis dysregulation (TPH2/vitamin D)"),
    ("Tryptophan supplementation (with vitamin D)",
     "Vitamin D deficiency (maternal + child)"),
    ("Creatine monohydrate",
     "Mitochondrial dysfunction (acquired or inherited)"),
    ("Time-restricted eating / 16:8 fasting",
     "AMPK pathway dysregulation"),
    ("Time-restricted eating / 16:8 fasting",
     "Mitochondrial dysfunction (acquired or inherited)"),
    ("HIIT (high-intensity interval training)",
     "AMPK pathway dysregulation"),
    ("Whole-body hyperthermia (clinical)",
     "Heat shock response insufficiency / 'fever effect' subtype"),
    ("Sauna / heat therapy",
     "Heat shock response insufficiency / 'fever effect' subtype"),
    # Existing interventions to new hypotheses
    ("Vitamin D3",
     "Brain serotonin synthesis dysregulation (TPH2/vitamin D)"),
    ("Sulforaphane (broccoli sprout extract)",
     "Brain glutathione depletion"),
    ("Sulforaphane (broccoli sprout extract)",
     "Heat shock response insufficiency / 'fever effect' subtype"),
    ("Aerobic exercise (structured)",
     "Heat shock response insufficiency / 'fever effect' subtype"),
]

NEW_INT_MECH_LINKS = [
    ("Phospholipid DHA (krill oil / salmon roe)",
     "DHA membrane phospholipid composition"),
    ("Phospholipid DHA (krill oil / salmon roe)",
     "BDNF / neurotrophin signaling"),
    ("Tryptophan supplementation (with vitamin D)",
     "Vitamin-D-regulated serotonin synthesis (TPH2)"),
    ("Creatine monohydrate", "Impaired methylation"),
    ("Creatine monohydrate", "Mitochondrial dysfunction"),
    ("Time-restricted eating / 16:8 fasting", "AMPK signaling"),
    ("Time-restricted eating / 16:8 fasting",
     "Autophagy / proteostasis"),
    ("HIIT (high-intensity interval training)",
     "BDNF / neurotrophin signaling"),
    ("HIIT (high-intensity interval training)", "AMPK signaling"),
    ("HIIT (high-intensity interval training)",
     "Mitochondrial dysfunction"),
    ("Whole-body hyperthermia (clinical)",
     "Heat shock protein (HSF1/HSP70/HSP90) response"),
    ("Whole-body hyperthermia (clinical)", "Neuroinflammation"),
    # Existing interventions to new mechanisms
    ("Sauna / heat therapy",
     "Heat shock protein (HSF1/HSP70/HSP90) response"),
    ("Sauna / heat therapy", "Autophagy / proteostasis"),
    ("Cold exposure / cold plunge",
     "Heat shock protein (HSF1/HSP70/HSP90) response"),
    ("Sulforaphane (broccoli sprout extract)",
     "Heat shock protein (HSF1/HSP70/HSP90) response"),
    ("Aerobic exercise (structured)",
     "BDNF / neurotrophin signaling"),
    ("Aerobic exercise (structured)", "Autophagy / proteostasis"),
    ("Ketogenic diet", "BDNF / neurotrophin signaling"),
    ("Ketogenic diet", "Autophagy / proteostasis"),
    ("Rapamycin (sirolimus)", "Autophagy / proteostasis"),
    ("Vitamin D3",
     "Vitamin-D-regulated serotonin synthesis (TPH2)"),
    ("Cannabidiol (CBD)", "BDNF / neurotrophin signaling"),
    ("Cerebrolysin", "BDNF / neurotrophin signaling"),
    ("Lion's mane (Hericium erinaceus)",
     "BDNF / neurotrophin signaling"),
    ("Bacopa monnieri", "BDNF / neurotrophin signaling"),
    ("Saffron", "BDNF / neurotrophin signaling"),
    ("Metformin", "Autophagy / proteostasis"),
    ("Berberine", "AMPK signaling"),
    ("Berberine", "Autophagy / proteostasis"),
    ("Resveratrol", "Autophagy / proteostasis"),
    ("Omega-3 (EPA + DHA)", "DHA membrane phospholipid composition"),
    ("Omega-3 (EPA + DHA)", "BDNF / neurotrophin signaling"),
    ("Methyl-B12 (methylcobalamin) injection",
     "Vitamin-D-regulated serotonin synthesis (TPH2)"),
]


# ---------------------------------------------------------------------------
# Expansion logic
# ---------------------------------------------------------------------------

def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    ts = now_iso()

    print(f"[v1.5] running at {ts}")
    tables = {}
    for csv in sorted(INPUT_DIR.glob("*.csv")):
        tables[csv.stem] = pd.read_csv(
            csv, dtype=str, keep_default_na=False)

    mech_name_to_id = {r["name"]: r["id"]
                       for _, r in tables["mechanisms"].iterrows()}
    hyp_name_to_id = {r["name"]: r["id"]
                      for _, r in tables["hypotheses"].iterrows()}
    int_name_to_id = {r["name"]: r["id"]
                      for _, r in tables["interventions"].iterrows()}
    gene_symbol_to_id = {r["gene_symbol"]: r["id"]
                         for _, r in tables["genes"].iterrows()}

    def next_n(table_name, prefix):
        df = tables[table_name]
        if df.empty: return 1
        nums = []
        for i in df["id"].dropna():
            m = re.match(rf"^{prefix}-(\d+)$", str(i))
            if m: nums.append(int(m.group(1)))
        return (max(nums) if nums else 0) + 1

    next_mec = next_n("mechanisms", "MEC")
    next_hyp = next_n("hypotheses", "HYP")
    next_int = next_n("interventions", "INT")
    next_src = next_n("sources", "SRC")
    next_evd = next_n("evidence_fragments", "EVD")
    next_evl = next_n("evidence_links", "EVL")

    # mechanisms
    new_mec = []
    for name, cat, kegg, react, ot, notes in NEW_MECHANISMS:
        if name in mech_name_to_id: continue
        mid = pad_id("MEC", next_mec, 4); next_mec += 1
        mech_name_to_id[name] = mid
        new_mec.append({
            "id": mid, "name": name, "category": cat,
            "description": "", "status": "active",
            "evidence_strength": "",
            "kegg_ids": kegg, "reactome_ids": react,
            "opentargets_ids": ot,
            "created_at": ts, "last_updated": ts, "notes": notes,
        })
    if new_mec:
        tables["mechanisms"] = pd.concat(
            [tables["mechanisms"], pd.DataFrame(new_mec)],
            ignore_index=True)
        print(f"[v1.5] mechanisms: +{len(new_mec)}")

    # hypotheses
    new_hyp = []
    for name, cat, desc, pop, notes in NEW_HYPOTHESES:
        if name in hyp_name_to_id: continue
        hid = pad_id("HYP", next_hyp, 4); next_hyp += 1
        hyp_name_to_id[name] = hid
        new_hyp.append({
            "id": hid, "name": name, "category": cat,
            "description": desc, "affected_population": pop,
            "status": "active",
            "confidence_score": "", "evidence_count": "",
            "evidence_quality_index": "", "consistency_index": "",
            "created_at": ts, "last_updated": ts, "notes": notes,
            "category_legacy": "", "evidence_strength_legacy": "",
            "epidemiological_strength_legacy": "",
            "mitigation_intervention_ids_legacy": "",
            "source_pmids_legacy": "",
            "csrs_score_legacy": "", "csrs_last_updated_legacy": "",
        })
    if new_hyp:
        tables["hypotheses"] = pd.concat(
            [tables["hypotheses"], pd.DataFrame(new_hyp)],
            ignore_index=True)
        print(f"[v1.5] hypotheses: +{len(new_hyp)}")

    # interventions
    new_int = []
    for (name, cat, dirn, mech, dose, cost, otc, ped,
         notes) in NEW_INTERVENTIONS:
        if name in int_name_to_id: continue
        iid = pad_id("INT", next_int, 4); next_int += 1
        int_name_to_id[name] = iid
        new_int.append({
            "id": iid, "name": name, "category": cat,
            "directionality": dirn, "mechanism_summary": mech,
            "dose_range": dose, "cost_per_month_usd": str(cost),
            "otc_or_rx": otc, "pediatric_safe": ped,
            "csrs_score": "", "csrs_last_updated": "",
            "status": "active",
            "created_at": ts, "last_updated": ts, "notes": notes,
            "targets_legacy": "", "source_pmids_legacy": "",
            "source_anecdote_ids_legacy": "",
            "csrs_score_legacy": "", "csrs_last_updated_legacy": "",
        })
    if new_int:
        tables["interventions"] = pd.concat(
            [tables["interventions"], pd.DataFrame(new_int)],
            ignore_index=True)
        print(f"[v1.5] interventions: +{len(new_int)}")

    # sources + fragments + links
    new_src, new_evd, new_evl = [], [], []
    skipped = []
    for (pmid, title, year, design, n, stype, author,
         targets) in NEW_LANDMARKS:
        sid = pad_id("SRC", next_src, 6); next_src += 1
        new_src.append({
            "id": sid, "type": stype, "platform": "pubmed",
            "external_id": pmid, "title": title,
            "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
            "date_published": f"{year}-01-01", "date_ingested": ts,
            "study_design": design,
            "sample_size": str(n) if n else "",
            "model_system": "human" if design != "mechanistic"
                            else "animal",
            "raw_metadata": json.dumps({
                "year": year, "first_author": author,
                "added_in": "v1.5_patrick_expansion",
            }, sort_keys=True),
            "notes": "",
        })
        eid = pad_id("EVD", next_evd, 6); next_evd += 1
        default_dir = targets[0][2] if targets else "positive"
        new_evd.append({
            "id": eid, "source_id": sid,
            "fragment_type": "result" if design != "mechanistic"
                              else "mechanism",
            "text_excerpt": title[:480],
            "structured_payload": json.dumps({
                "first_author": author, "design": design,
                "sample_size": n, "year": year,
                "added_in": "v1.5_patrick_expansion",
            }, sort_keys=True),
            "effect_direction": default_dir,
            "strength_score": "",
            "extraction_method": "manual",
            "extraction_confidence": "1.00",
            "date_extracted": ts, "notes": "",
        })
        for ttype, name, direction in targets:
            if ttype == "gene":
                tid = gene_symbol_to_id.get(name)
            elif ttype == "hypothesis":
                tid = hyp_name_to_id.get(name)
            elif ttype == "intervention":
                tid = int_name_to_id.get(name)
            elif ttype == "mechanism":
                tid = mech_name_to_id.get(name)
            elif ttype == "phenotype":
                tid = name
            else:
                tid = None
            if not tid:
                skipped.append((pmid, ttype, name)); continue
            elid = pad_id("EVL", next_evl, 6); next_evl += 1
            new_evl.append({
                "id": elid, "evidence_fragment_id": eid,
                "claim_id": "",
                "target_type": ttype, "target_id": tid,
                "effect_direction": direction,
                "weight": "", "context_scope": "",
                "created_at": ts, "notes": "",
            })

    tables["sources"] = pd.concat(
        [tables["sources"], pd.DataFrame(new_src)], ignore_index=True)
    tables["evidence_fragments"] = pd.concat(
        [tables["evidence_fragments"], pd.DataFrame(new_evd)],
        ignore_index=True)
    tables["evidence_links"] = pd.concat(
        [tables["evidence_links"], pd.DataFrame(new_evl)],
        ignore_index=True)
    print(f"[v1.5] sources: +{len(new_src)}, evidence_fragments: "
          f"+{len(new_evd)}, evidence_links: +{len(new_evl)}")
    if skipped:
        print(f"[v1.5] skipped {len(skipped)} unresolvable targets:")
        for pmid, ttype, name in skipped[:8]:
            print(f"  PMID {pmid}: {ttype}={name}")

    # Edges
    def add_edges(table_name, prefix, src_col, dst_col, lookups,
                  pairs, relation_type):
        n_start = next_n(table_name, prefix)
        rows = []
        n = n_start
        for src_name, dst_name in pairs:
            sid = lookups[0].get(src_name)
            did = lookups[1].get(dst_name)
            if not sid or not did: continue
            eid = pad_id(prefix, n, 5); n += 1
            rows.append({
                "id": eid, src_col: sid, dst_col: did,
                "relation_type": relation_type,
                "polarity": "supporting",
                "evidence_for_count": "",
                "evidence_against_count": "",
                "evidence_strength_aggregate": "",
                "context_scope": "", "status": "active",
                "created_at": ts, "last_updated": ts,
            })
        if rows:
            tables[table_name] = pd.concat(
                [tables[table_name], pd.DataFrame(rows)],
                ignore_index=True)
        return len(rows)

    n_hme = add_edges(
        "hypothesis_mechanism_edges", "HME",
        "hypothesis_id", "mechanism_id",
        (hyp_name_to_id, mech_name_to_id),
        NEW_HYP_MECH_LINKS, "acts_through")
    print(f"[v1.5] hypothesis_mechanism_edges: +{n_hme}")

    rows = []
    n = next_n("mechanism_phenotype_edges", "MPE")
    for mech_name, phen_id in NEW_MECH_PHEN_LINKS:
        mid = mech_name_to_id.get(mech_name)
        if not mid: continue
        eid = pad_id("MPE", n, 5); n += 1
        rows.append({
            "id": eid, "mechanism_id": mid, "phenotype_id": phen_id,
            "relation_type": "implicated_in", "polarity": "supporting",
            "evidence_for_count": "", "evidence_against_count": "",
            "evidence_strength_aggregate": "",
            "context_scope": "", "status": "active",
            "created_at": ts, "last_updated": ts,
        })
    if rows:
        tables["mechanism_phenotype_edges"] = pd.concat(
            [tables["mechanism_phenotype_edges"], pd.DataFrame(rows)],
            ignore_index=True)
    print(f"[v1.5] mechanism_phenotype_edges: +{len(rows)}")

    n_ihe = add_edges(
        "intervention_hypothesis_edges", "IHE",
        "intervention_id", "hypothesis_id",
        (int_name_to_id, hyp_name_to_id),
        NEW_INT_HYP_LINKS, "cause_mitigation")
    print(f"[v1.5] intervention_hypothesis_edges: +{n_ihe}")

    n_ime = add_edges(
        "intervention_mechanism_edges", "IME",
        "intervention_id", "mechanism_id",
        (int_name_to_id, mech_name_to_id),
        NEW_INT_MECH_LINKS, "modulates")
    print(f"[v1.5] intervention_mechanism_edges: +{n_ime}")

    for name, df in tables.items():
        target = OUTPUT_DIR / f"{name}.csv"
        df.to_csv(target, index=False, encoding="utf-8")

    summary = {
        "expansion_version": "v1.5_patrick",
        "run_timestamp": ts,
        "added": {
            "mechanisms": len(new_mec),
            "hypotheses": len(new_hyp),
            "interventions": len(new_int),
            "sources": len(new_src),
            "evidence_fragments": len(new_evd),
            "evidence_links": len(new_evl),
            "hypothesis_mechanism_edges": n_hme,
            "mechanism_phenotype_edges": len(rows),
            "intervention_mechanism_edges": n_ime,
            "intervention_hypothesis_edges": n_ihe,
        },
        "skipped_targets": len(skipped),
    }
    Path("expansion_v15_summary.json").write_text(
        json.dumps(summary, indent=2))
    print()
    print("=" * 60)
    print("v1.5 PATRICK EXPANSION COMPLETE")
    print(json.dumps(summary["added"], indent=2))


if __name__ == "__main__":
    main()
