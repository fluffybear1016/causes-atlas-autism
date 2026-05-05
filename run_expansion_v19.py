#!/usr/bin/env python3
"""
run_expansion_v19.py — Causes Atlas (Autism) v1.9 X-extracted claims

Reads:  expanded_output_v18/*.csv
Writes: expanded_output_v19/*.csv

User pasted Grok extraction of X content from thehealthb0t, HighWireTalk,
Outdoctrination, anomalie_blue, DrJesseMorse. After de-duping against
v1.0-v1.8 (most claims already in the atlas), v1.9 adds the genuinely
new content with proper provenance:

  NEW INTERVENTIONS:
    - Red light / photobiomodulation therapy (635 nm) — Leisman 2018
      double-blind RCT, n=21-22, 5 min 2x/week 4 weeks, ~50%
      reduction in irritability/lethargy/stereotypy
    - Vitamin A megadose protocol — Guo 2018 pilot, 200,000 IU single
      dose in vitamin-A-deficient ASD children
    - Chelation (DMSA / EDTA) — added with NEGATIVE evidence (James
      2015 Cochrane) per spec §1.1; no benefit + significant risks
      including death

  NEW MECHANISMS:
    - Photobiomodulation / cytochrome c oxidase activation —
      distinct from heat shock response and from mitochondrial
      dysfunction itself; specifically the red/NIR light pathway

  NEW HYPOTHESIS:
    - Lactate / pyruvate ratio elevation (bioenergetic biomarker) —
      Oh 2020 Korean study, specific cutoffs lactate ≥22 mg/dL,
      pyruvate ≥1.4 mg/dL, ratio >25 abnormal. anomalie_blue's Ray
      Peat-influenced bioenergetic framing.

  NEW SOURCES (12):
    - Leisman 2018 photobiomodulation RCT
    - Guo 2018 vitamin A megadose
    - James 2015 Cochrane chelation review (negative)
    - Adams 2009 DMSA chelation pilot
    - Arora 2017 baby teeth twin study (Nature)
    - Shaw 2017 urinary organic acid metabolites
    - Oh 2020 Korean lactate/pyruvate study
    - Gvozdjakova 2014 ubiquinol RCT
    - Frye 2020 mitochondrial-targeted treatments review
    - Boukhris 2016 SSRI / autism cohort
    - Bjorklund 2013 zinc / autism review
    - LoParo 2015 oxytocin meta-analysis

Determinism: same inputs → bitwise identical outputs.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

INPUT_DIR = Path("expanded_output_v18")
OUTPUT_DIR = Path("expanded_output_v19")


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")


def pad_id(prefix: str, n: int, width: int) -> str:
    return f"{prefix}-{str(n).zfill(width)}"


# ---------------------------------------------------------------------------
# v1.9 content
# ---------------------------------------------------------------------------

NEW_MECHANISMS = [
    ("Photobiomodulation / cytochrome c oxidase activation",
     "neural", "hsa00190", "R-HSA-611105", "",
     "Red and near-infrared light (600-1100 nm) absorbed by "
     "cytochrome c oxidase (complex IV); displaces nitric oxide, "
     "increases ATP synthesis, modulates ROS signaling. Distinct "
     "mechanism from heat shock response. Direct mitochondrial "
     "stimulation pathway. Underlies Leisman 2018 red-laser "
     "intervention in autism."),
]


NEW_HYPOTHESES = [
    ("Lactate / pyruvate ratio elevation (bioenergetic biomarker)",
     "metabolic",
     "Elevated blood/CSF lactate (≥22 mg/dL) and lactate:pyruvate "
     "ratio (>25) indicate anaerobic shift in cellular metabolism, "
     "reported across autism, schizophrenia, bipolar. Distinct from "
     "general 'mitochondrial dysfunction' hypothesis (HYP-0006) — "
     "this is the specific quantifiable bioenergetic biomarker. "
     "Magnesium (lactate clearance), B-complex (PDH/ETC cofactors), "
     "and CO2 (Bohr effect) are mechanistically targetable. "
     "anomalie_blue's Ray-Peat-influenced framing on X.",
     "Subset with elevated biomarkers; ~30-50% of mitochondrial "
     "subset",
     "Oh 2020 Korean cohort; bioenergetic framing emphasizes "
     "metabolism-first interpretation."),
]


NEW_INTERVENTIONS = [
    ("Red light / photobiomodulation therapy (635 nm)",
     "lifestyle", "treatment",
     "Transcranial red laser (635 nm, 5 min, 2x/week, 4 weeks) "
     "applied at skull base/temples. Leisman 2018 double-blind "
     "RCT (n=21-22) showed ~50% reductions in irritability, "
     "lethargy/social withdrawal, stereotypic behavior, hyperactivity, "
     "and total ABC-C score vs. placebo LED, with gains persisting. "
     "Mechanism: photobiomodulation activates cytochrome c oxidase, "
     "boosts ATP, reduces neuroinflammation.",
     "635 nm laser, 5 min @ skull base + temples, 2x/week, "
     "4 weeks", 200, "otc", "yes",
     "Small but rigorous RCT; replication needed. Outdoctrination "
     "X clip referenced this study."),

    ("Vitamin A megadose (single 200,000 IU)",
     "supplement", "treatment",
     "Guo 2018 pilot showed single 200,000 IU vitamin A in "
     "vitamin-A-deficient ASD children reduced symptoms and lowered "
     "serum serotonin (peripheral hyperserotonemia is documented "
     "in autism). Mechanism: RAR/RXR signaling, gut-serotonin "
     "modulation. Liver/cod-liver-oil dietary equivalent safer "
     "long-term. NOT routine — only with documented deficiency "
     "and clinician supervision (vit A is hepatotoxic at high "
     "chronic doses).",
     "Single 200,000 IU under clinician supervision, only if "
     "documented deficiency", 30, "rx", "uncertain",
     "Pilot evidence; caution required — vitamin A toxicity is "
     "real."),

    ("Chelation therapy (DMSA / EDTA)",
     "drug", "treatment",
     "Pharmacological chelation of heavy metals (mercury, lead, "
     "aluminum) with DMSA, DMPS, or EDTA. Adams 2009 small DMSA "
     "pilot showed urinary metal output but mixed clinical effect. "
     "James 2015 Cochrane review concluded INSUFFICIENT EVIDENCE "
     "of benefit on core ASD symptoms and documented significant "
     "risks including renal injury and death (one fatal "
     "hypocalcemia case from disodium-EDTA confusion in 2005). "
     "AAP and FDA warn against chelation for ASD outside proven "
     "heavy-metal poisoning. Per spec §1.1 added with negative-"
     "tilting evidence; NOT recommended.",
     "DMSA 10 mg/kg/dose protocols studied; NOT recommended",
     400, "rx", "no",
     "James 2015 Cochrane: insufficient evidence + harm. Pediatric_"
     "safe=no due to documented fatalities. Status active for "
     "tracking; effective use is contraindicated outside true "
     "heavy-metal poisoning."),
]


NEW_LANDMARKS = [
    # Photobiomodulation
    ("30258461",
     "Effects of low-level laser therapy in autism spectrum "
     "disorder", 2018, "rct", 22, "study", "Leisman",
     [("intervention",
       "Red light / photobiomodulation therapy (635 nm)", "positive"),
      ("mechanism",
       "Photobiomodulation / cytochrome c oxidase activation",
       "positive"),
      ("hypothesis",
       "Mitochondrial dysfunction (acquired or inherited)",
       "positive")]),

    # Vitamin A
    ("29936517",
     "Vitamin A supplementation modifies the antioxidant system "
     "in autism spectrum disorder children (Guo)", 2018, "rct", 64,
     "study", "Guo",
     [("intervention", "Vitamin A megadose (single 200,000 IU)",
       "positive"),
      ("mechanism", "Oxidative stress", "positive"),
      ("mechanism",
       "Vitamin-D-regulated serotonin synthesis (TPH2)",
       "neutral")]),

    # Chelation — negative direction (Cochrane null)
    ("26106752",
     "Chelation for autism spectrum disorder (Cochrane Database "
     "Systematic Review — insufficient evidence + significant "
     "risks)", 2015, "review", 0, "review", "James-Cochrane",
     [("intervention", "Chelation therapy (DMSA / EDTA)",
       "negative"),
      ("hypothesis",
       "Heavy metal exposure (Pb, Hg, Al)", "neutral")]),

    # Adams 2009 DMSA pilot
    ("19799531",
     "Safety and efficacy of oral DMSA therapy for children with "
     "autism spectrum disorders: part A (Adams pilot)",
     2009, "case_series", 65, "study", "Adams-DMSA",
     [("intervention", "Chelation therapy (DMSA / EDTA)",
       "neutral"),
      ("hypothesis",
       "Heavy metal exposure (Pb, Hg, Al)", "positive")]),

    # Arora 2017 baby teeth twin study
    ("28593989",
     "Fetal and postnatal metal dysregulation in autism (Arora "
     "Nature Communications, baby teeth temporal biomarker "
     "twin study)", 2017, "case_control", 32, "study", "Arora",
     [("hypothesis",
       "Heavy metal exposure (Pb, Hg, Al)", "positive"),
      ("hypothesis", "Zinc deficiency / copper:zinc imbalance",
       "positive")]),

    # Shaw 2017 organic acid markers
    ("28218275",
     "Elevated urinary glyphosate and clostridia metabolites with "
     "altered amino acid metabolism in children with autism "
     "(Shaw OAT)", 2017, "case_control", 35, "study", "Shaw-OAT",
     [("hypothesis",
       "Clostridia overgrowth / dysbiotic fermentation",
       "positive"),
      ("hypothesis", "Glyphosate exposure (food + water)",
       "positive"),
      ("mechanism",
       "p-cresol / 4-EPS aromatic metabolite production",
       "positive")]),

    # Oh 2020 Korean lactate study
    ("32574078",
     "Lactate and pyruvate levels in children with autism spectrum "
     "disorder (Oh)", 2020, "case_control", 200, "study",
     "Oh-Korean",
     [("hypothesis",
       "Lactate / pyruvate ratio elevation (bioenergetic "
       "biomarker)", "positive"),
      ("hypothesis",
       "Mitochondrial dysfunction (acquired or inherited)",
       "positive"),
      ("mechanism", "Mitochondrial dysfunction", "positive")]),

    # Gvozdjakova 2014 ubiquinol RCT
    ("24803935",
     "Ubiquinol improves symptoms in children with autism "
     "(Gvozdjakova 2014 trial)", 2014, "rct", 24, "study",
     "Gvozdjakova",
     [("intervention", "Coenzyme Q10 (ubiquinol)", "positive"),
      ("hypothesis",
       "Mitochondrial dysfunction (acquired or inherited)",
       "positive"),
      ("mechanism", "Mitochondrial dysfunction", "positive")]),

    # Frye 2020 mitochondrial review
    ("32296057",
     "Mitochondrial dysfunction in autism spectrum disorders: "
     "unique abnormalities and targeted treatments (Frye review)",
     2020, "review", 0, "review", "Frye-2020",
     [("hypothesis",
       "Mitochondrial dysfunction (acquired or inherited)",
       "positive"),
      ("mechanism", "Mitochondrial dysfunction", "positive"),
      ("intervention",
       "Mitochondrial cocktail (CoQ10+L-carnitine+B-complex)",
       "positive"),
      ("intervention", "Coenzyme Q10 (ubiquinol)", "positive"),
      ("intervention", "L-carnitine", "positive")]),

    # Boukhris 2016 SSRI
    ("26710107",
     "Antidepressant use during pregnancy and the risk of autism "
     "spectrum disorder in children (Boukhris JAMA Pediatrics)",
     2016, "cohort", 145456, "study", "Boukhris",
     [("hypothesis", "Maternal SSRI in pregnancy", "positive")]),

    # Bjorklund 2013 zinc
    ("23708981",
     "The role of zinc and copper in autism spectrum disorders "
     "(Bjorklund review)", 2013, "review", 0, "review",
     "Bjorklund",
     [("hypothesis", "Zinc deficiency / copper:zinc imbalance",
       "positive"),
      ("intervention", "Zinc (zinc picolinate)", "positive")]),

    # LoParo 2015 oxytocin meta
    ("25895429",
     "Oxytocin receptor gene (OXTR) variants and social cognition "
     "in autism: a meta-analysis (LoParo)", 2015, "meta_analysis",
     0, "review", "LoParo",
     [("hypothesis", "Oxytocin system dysregulation", "positive"),
      ("intervention", "Intranasal oxytocin", "positive")]),
]


NEW_HYP_MECH_LINKS = [
    ("Lactate / pyruvate ratio elevation (bioenergetic biomarker)",
     "Mitochondrial dysfunction"),
    ("Lactate / pyruvate ratio elevation (bioenergetic biomarker)",
     "AMPK signaling"),
    ("Lactate / pyruvate ratio elevation (bioenergetic biomarker)",
     "Photobiomodulation / cytochrome c oxidase activation"),
]

NEW_MECH_PHEN_LINKS = [
    ("Photobiomodulation / cytochrome c oxidase activation",
     "PHE-0002"),  # Mitochondrial subtype
]

NEW_INT_HYP_LINKS = [
    ("Red light / photobiomodulation therapy (635 nm)",
     "Mitochondrial dysfunction (acquired or inherited)"),
    ("Red light / photobiomodulation therapy (635 nm)",
     "Lactate / pyruvate ratio elevation (bioenergetic biomarker)"),
    ("Vitamin A megadose (single 200,000 IU)",
     "Brain serotonin synthesis dysregulation (TPH2/vitamin D)"),
    ("Chelation therapy (DMSA / EDTA)",
     "Heavy metal exposure (Pb, Hg, Al)"),
    ("Chelation therapy (DMSA / EDTA)",
     "Thimerosal exposure (contested, largely removed)"),
]

NEW_INT_MECH_LINKS = [
    ("Red light / photobiomodulation therapy (635 nm)",
     "Photobiomodulation / cytochrome c oxidase activation"),
    ("Red light / photobiomodulation therapy (635 nm)",
     "Mitochondrial dysfunction"),
    ("Red light / photobiomodulation therapy (635 nm)",
     "Neuroinflammation"),
    ("Vitamin A megadose (single 200,000 IU)", "Oxidative stress"),
    ("Chelation therapy (DMSA / EDTA)", "Oxidative stress"),
]


# ---------------------------------------------------------------------------
# Expansion logic
# ---------------------------------------------------------------------------

def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    ts = now_iso()

    print(f"[v1.9] running at {ts}")
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
        print(f"[v1.9] mechanisms: +{len(new_mec)}")

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
        print(f"[v1.9] hypotheses: +{len(new_hyp)}")

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
        print(f"[v1.9] interventions: +{len(new_int)}")

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
            "model_system": "human",
            "raw_metadata": json.dumps({
                "year": year, "first_author": author,
                "added_in": "v1.9_x_extracted_claims",
            }, sort_keys=True),
            "notes": "",
        })
        eid = pad_id("EVD", next_evd, 6); next_evd += 1
        dir_counts = {}
        for _, _, d in targets:
            dir_counts[d] = dir_counts.get(d, 0) + 1
        default_dir = max(dir_counts, key=dir_counts.get) if dir_counts \
                       else "neutral"
        new_evd.append({
            "id": eid, "source_id": sid,
            "fragment_type": "result",
            "text_excerpt": title[:480],
            "structured_payload": json.dumps({
                "first_author": author, "design": design,
                "sample_size": n, "year": year,
                "added_in": "v1.9_x_extracted_claims",
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
    print(f"[v1.9] sources: +{len(new_src)}, evidence_fragments: "
          f"+{len(new_evd)}, evidence_links: +{len(new_evl)}")
    if skipped:
        for pmid, ttype, name in skipped[:8]:
            print(f"  [warn] skipped: PMID {pmid}: {ttype}={name}")

    # Edges
    def add_edges(table_name, prefix, src_col, dst_col, lookups,
                  pairs, relation_type):
        n = next_n(table_name, prefix)
        rows = []
        for src_name, dst_name in pairs:
            sid_ = lookups[0].get(src_name)
            did_ = lookups[1].get(dst_name)
            if not sid_ or not did_: continue
            eid = pad_id(prefix, n, 5); n += 1
            rows.append({
                "id": eid, src_col: sid_, dst_col: did_,
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
    print(f"[v1.9] hypothesis_mechanism_edges: +{n_hme}")

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
    print(f"[v1.9] mechanism_phenotype_edges: +{len(rows)}")

    n_ihe = add_edges(
        "intervention_hypothesis_edges", "IHE",
        "intervention_id", "hypothesis_id",
        (int_name_to_id, hyp_name_to_id),
        NEW_INT_HYP_LINKS, "cause_mitigation")
    print(f"[v1.9] intervention_hypothesis_edges: +{n_ihe}")

    n_ime = add_edges(
        "intervention_mechanism_edges", "IME",
        "intervention_id", "mechanism_id",
        (int_name_to_id, mech_name_to_id),
        NEW_INT_MECH_LINKS, "modulates")
    print(f"[v1.9] intervention_mechanism_edges: +{n_ime}")

    for name, df in tables.items():
        target = OUTPUT_DIR / f"{name}.csv"
        df.to_csv(target, index=False, encoding="utf-8")

    summary = {
        "expansion_version": "v1.9_x_extracted_claims",
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
            "intervention_hypothesis_edges": n_ihe,
            "intervention_mechanism_edges": n_ime,
        },
        "skipped_targets": len(skipped),
        "claim_disposition_from_grok_extraction": {
            "already_in_atlas_v1_to_v1.8": [
                "CDC Simpsonwood / hep B (HYP-0066, IOM 2004/2011)",
                "Glyphosate / Clostridia (HYP-0005, HYP-0057)",
                "CoQ10 ubiquinol (INT-0012)",
                "Mitochondrial dysfunction (HYP-0006, MEC-0010)",
                "HBOT (INT-0092)",
                "Heavy metals / lead (HYP-0015)",
                "SSRI in pregnancy (HYP-0024) — Boukhris 2016 added "
                "in v1.9 as supporting source",
                "Zinc / Cu:Zn (HYP-0046) — Bjorklund 2013 added",
                "Oxytocin (HYP-0034, INT-0061) — LoParo 2015 added",
                "Multifactorial causation (entire Layer 1 model)",
                "Mitochondrial cocktail (INT-0055)",
                "Glycine (INT-0024)",
            ],
            "newly_added_in_v1.9": [
                "Red light / photobiomodulation (Leisman 2018) — "
                "completely new mechanism + intervention",
                "Vitamin A megadose (Guo 2018) — new intervention",
                "Chelation DMSA/EDTA (James 2015 Cochrane) — new "
                "intervention with NEGATIVE evidence",
                "Lactate/pyruvate ratio bioenergetic biomarker "
                "(Oh 2020) — new hypothesis with specific cutoffs",
                "Photobiomodulation/cytochrome c oxidase — new "
                "mechanism distinct from heat shock and "
                "mitochondrial",
                "Arora 2017 baby teeth twin study — new source for "
                "heavy metal hypothesis",
                "Shaw 2017 OAT urinary metabolites — new source "
                "for Clostridia hypothesis",
                "Frye 2020 mitochondrial review",
                "Gvozdjakova 2014 ubiquinol RCT",
            ],
            "deliberately_balanced_by_atlas_design": (
                "Per spec §1.1 (no pre-judging), §9.1 (contested "
                "permanent), §7.2 (social signals lowest weight): "
                "claims like 'CDC secret meetings' and 'chelation "
                "cures autism' enter as either (a) peer-reviewed "
                "sources with proper effect_direction, or (b) "
                "social-signal evidence at the lowest tier. The "
                "scoring engine resolves them honestly. Chelation "
                "specifically lands as an intervention with NEGATIVE "
                "evidence (James 2015 Cochrane null + harm) — the "
                "system thus correctly tells you 'this exists, and "
                "the evidence weight is against it.'"),
        },
    }
    Path("expansion_v19_summary.json").write_text(
        json.dumps(summary, indent=2))
    print()
    print("=" * 60)
    print("v1.9 X-EXTRACTED CLAIMS EXPANSION COMPLETE")
    print(json.dumps(summary["added"], indent=2))


if __name__ == "__main__":
    main()
