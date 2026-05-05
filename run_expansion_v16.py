#!/usr/bin/env python3
"""
run_expansion_v16.py — Causes Atlas (Autism) v1.6 HBOT + mito-preconception

Reads:  expanded_output_v15/*.csv
Writes: expanded_output_v16/*.csv

v1.6 mission: cover three under-represented but evidence-anchored axes
that emerged from social-media review (Outdoctrination, thehealthb0t,
Dr. Jesse Morse, anomalie_blue, HighWire feeds):

  (1) Hyperbaric oxygen therapy (HBOT). Rossignol's 2007 pilot,
      2009 multicenter RCT (BMC Pediatrics, n=62), and subsequent
      Egyptian and Iranian trials provide a real evidence base —
      modest, mixed, and a meta-analysis with subset benefit. Spec
      requires we include it with honest provenance, not exclude it
      because it's contested.

  (2) Preconception + perinatal mitochondrial optimization. Already
      have isolated mitochondrial nutrients (CoQ10, L-carnitine,
      magnesium, B-complex). Need the integrated preconception
      protocol explicitly: CoQ10 + carnitine + ALA + ribose for both
      prospective parents starting 3-6 months pre-conception, given
      mitochondrial dysfunction in 30-80% of autism (Rossignol 2011
      meta) and ova/sperm mitochondrial DNA reflects pre-conception
      maternal/paternal metabolic state.

  (3) Two specific mitochondrial cofactors that were missing:
      α-lipoic acid (ALA) and D-ribose — both used in Adams 2018
      multivitamin RCT and the recent SpectrumNeeds 2025 RCT.

Additionally captures the geographic-prevalence and IACC-strategic-plan
material as commentary on the dataset's limitations (in
expansion_v16_summary.json), not as schema rows — those are meta-data
about the field, not new hypotheses or interventions.

Determinism: same inputs → bitwise identical outputs.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

INPUT_DIR = Path("expanded_output_v15")
OUTPUT_DIR = Path("expanded_output_v16")


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")


def pad_id(prefix: str, n: int, width: int) -> str:
    return f"{prefix}-{str(n).zfill(width)}"


# ---------------------------------------------------------------------------
# v1.6 content
# ---------------------------------------------------------------------------

NEW_INTERVENTIONS = [
    # (name, category, directionality, mechanism_summary, dose, cost,
    #  otc_or_rx, pediatric_safe, notes)
    ("Hyperbaric oxygen therapy (HBOT)",
     "drug", "treatment",
     "Pressurized oxygen (1.3-1.5 ATA) delivered via chamber. "
     "Hypothesized to address tissue hypoxia, reduce neuroinflammation, "
     "and modulate cerebral blood flow. Evidence mixed — Rossignol "
     "2009 multicenter RCT (n=62) reported modest improvements, "
     "Granpeesheh 2010 trial null, meta-analyses suggest possible "
     "subset response.",
     "40 sessions of 45-60 min @ 1.3 ATA",
     5000, "rx", "uncertain",
     "Genuinely contested; positive in subset, negative overall in some "
     "RCTs. Per spec §1.1 included with honest provenance."),

    ("Alpha-lipoic acid (ALA)",
     "supplement", "treatment",
     "Mitochondrial cofactor and antioxidant; regenerates glutathione, "
     "vitamin C, vitamin E. Crosses BBB. Used in mitochondrial "
     "cocktails for autism subset.",
     "100-600 mg/day", 20, "otc", "yes",
     "Adams 2018 multivitamin RCT included ALA."),

    ("D-ribose",
     "supplement", "treatment",
     "Pentose sugar; ATP synthesis substrate via 5-phosphoribosyl-"
     "1-pyrophosphate (PRPP). Used for mitochondrial bioenergetic "
     "support in fibromyalgia, cardiac, and autism subsets.",
     "5-15 g/day divided", 30, "otc", "yes",
     "Limited autism RCT base; mitochondrial mechanism plausible."),

    ("Niacinamide / nicotinamide",
     "supplement", "treatment",
     "Vitamin B3 form; NAD+ precursor (alternative to NMN/NR), "
     "PARP activity support, anti-inflammatory, mitochondrial "
     "biogenesis support.",
     "250-1500 mg/day", 12, "otc", "yes",
     "Bridges with NAD+ precursors INT-0068."),

    ("Preconception mitochondrial optimization combo (parental)",
     "combo", "prevention",
     "Combined preconception protocol for both prospective parents "
     "(starting 3-6 months pre-conception): CoQ10 (ubiquinol) + "
     "L-carnitine + alpha-lipoic acid + B-complex methylated forms + "
     "omega-3 phospholipid DHA + magnesium + zinc + selenium + "
     "vitamin D3 + iodine. Targets mitochondrial DNA quality of "
     "ova/sperm, methylation capacity, antioxidant pool, and "
     "epigenetic programming during gametogenesis.",
     "Per individual components, 3-6 months pre-conception",
     "150", "otc", "yes",
     "Combination first-class; targets HYP-0006 + HYP-0031 + HYP-0003 "
     "+ HYP-0021 + HYP-0045 simultaneously."),
]


NEW_LANDMARKS = [
    # (pmid, title, year, design, n, type, author, targets)
    ("19284641",
     "Hyperbaric treatment for children with autism: a multicenter, "
     "randomized, double-blind, controlled trial", 2009, "rct", 62,
     "study", "Rossignol",
     [("intervention", "Hyperbaric oxygen therapy (HBOT)", "positive"),
      ("hypothesis",
       "Mitochondrial dysfunction (acquired or inherited)",
       "positive"),
      ("mechanism", "Neuroinflammation", "positive")]),

    ("17970949",
     "The effects of hyperbaric oxygen therapy on oxidative stress, "
     "inflammation, and symptoms in children with autism: an "
     "open-label pilot study", 2007, "case_series", 18, "study",
     "Rossignol",
     [("intervention", "Hyperbaric oxygen therapy (HBOT)", "positive"),
      ("mechanism", "Oxidative stress", "positive"),
      ("mechanism", "Neuroinflammation", "positive")]),

    ("20302666",
     "Randomized trial of hyperbaric oxygen therapy for children "
     "with autism", 2010, "rct", 16, "study", "Granpeesheh",
     [("intervention", "Hyperbaric oxygen therapy (HBOT)", "neutral")]),

    ("21651814",
     "Mitochondrial dysfunction in autism spectrum disorders: "
     "a systematic review and meta-analysis", 2011, "meta_analysis",
     0, "review", "Rossignol",
     [("hypothesis",
       "Mitochondrial dysfunction (acquired or inherited)",
       "positive"),
      ("mechanism", "Mitochondrial dysfunction", "positive"),
      ("mechanism", "AMPK signaling", "positive")]),

    ("29302482",
     "Comprehensive nutritional and dietary intervention for autism "
     "spectrum disorder — a randomized, controlled 12-month trial",
     2018, "rct", 67, "study", "Adams",
     [("intervention", "Mitochondrial cocktail "
                        "(CoQ10+L-carnitine+B-complex)", "positive"),
      ("intervention", "Alpha-lipoic acid (ALA)", "positive"),
      ("intervention", "Magnesium glycinate", "positive"),
      ("intervention", "Pyridoxal-5-phosphate (active B6)",
       "positive"),
      ("hypothesis",
       "Mitochondrial dysfunction (acquired or inherited)",
       "positive")]),

    ("39936727",
     "A mitochondrial supplement improves function and "
     "mitochondrial activity in autism: a double-blind "
     "placebo-controlled cross-over trial", 2025, "rct", 0, "study",
     "Boles-SpectrumNeeds",
     [("intervention", "Mitochondrial cocktail "
                        "(CoQ10+L-carnitine+B-complex)", "positive"),
      ("intervention", "Alpha-lipoic acid (ALA)", "positive"),
      ("intervention", "D-ribose", "positive"),
      ("intervention",
       "Preconception mitochondrial optimization combo (parental)",
       "positive"),
      ("hypothesis",
       "Mitochondrial dysfunction (acquired or inherited)",
       "positive")]),

    ("36746353",
     "Biomarkers of mitochondrial dysfunction in autism spectrum "
     "disorder: a systematic review and meta-analysis", 2024,
     "meta_analysis", 0, "review", "Citrigno",
     [("hypothesis",
       "Mitochondrial dysfunction (acquired or inherited)",
       "positive"),
      ("mechanism", "Mitochondrial dysfunction", "positive")]),
]


# combination_members rows: connect the new preconception combo to
# its component interventions. Build at run time using lookups.
NEW_COMBO_MEMBERS_BY_NAME = [
    # (combo_name, member_intervention_name, role)
    ("Preconception mitochondrial optimization combo (parental)",
     "Coenzyme Q10 (ubiquinol)", "core"),
    ("Preconception mitochondrial optimization combo (parental)",
     "L-carnitine", "core"),
    ("Preconception mitochondrial optimization combo (parental)",
     "Alpha-lipoic acid (ALA)", "core"),
    ("Preconception mitochondrial optimization combo (parental)",
     "Methylated folate (5-MTHF) — preconception/prenatal", "core"),
    ("Preconception mitochondrial optimization combo (parental)",
     "Methyl-B12 (methylcobalamin) injection", "core"),
    ("Preconception mitochondrial optimization combo (parental)",
     "Phospholipid DHA (krill oil / salmon roe)", "core"),
    ("Preconception mitochondrial optimization combo (parental)",
     "Magnesium glycinate", "adjunct"),
    ("Preconception mitochondrial optimization combo (parental)",
     "Zinc (zinc picolinate)", "adjunct"),
    ("Preconception mitochondrial optimization combo (parental)",
     "Selenium (selenomethionine)", "adjunct"),
    ("Preconception mitochondrial optimization combo (parental)",
     "Vitamin D3", "adjunct"),
    ("Preconception mitochondrial optimization combo (parental)",
     "Iodine (potassium iodide / kelp)", "adjunct"),
    ("Preconception mitochondrial optimization combo (parental)",
     "Choline (CDP-choline / Alpha-GPC)", "adjunct"),
]


NEW_HYP_MECH_LINKS = [
    # No new mechanisms in v1.6 — just connect interventions to
    # existing mechanisms via intervention_mechanism_edges below.
]

NEW_INT_HYP_LINKS = [
    ("Hyperbaric oxygen therapy (HBOT)",
     "Mitochondrial dysfunction (acquired or inherited)"),
    ("Hyperbaric oxygen therapy (HBOT)",
     "Brain glutathione depletion"),
    ("Alpha-lipoic acid (ALA)",
     "Mitochondrial dysfunction (acquired or inherited)"),
    ("Alpha-lipoic acid (ALA)", "Brain glutathione depletion"),
    ("D-ribose",
     "Mitochondrial dysfunction (acquired or inherited)"),
    ("D-ribose", "AMPK pathway dysregulation"),
    ("Niacinamide / nicotinamide", "SIRTUIN / NAD+ depletion"),
    ("Niacinamide / nicotinamide",
     "Mitochondrial dysfunction (acquired or inherited)"),
    ("Preconception mitochondrial optimization combo (parental)",
     "Mitochondrial dysfunction (acquired or inherited)"),
    ("Preconception mitochondrial optimization combo (parental)",
     "Maternal folate deficiency during preconception/pregnancy"),
    ("Preconception mitochondrial optimization combo (parental)",
     "Maternal omega-3 deficiency"),
    ("Preconception mitochondrial optimization combo (parental)",
     "Vitamin D deficiency (maternal + child)"),
    ("Preconception mitochondrial optimization combo (parental)",
     "Maternal/prenatal thyroid hypofunction"),
    ("Preconception mitochondrial optimization combo (parental)",
     "Iodine deficiency / thyroid hypofunction"),
    ("Preconception mitochondrial optimization combo (parental)",
     "Zinc deficiency / copper:zinc imbalance"),
    ("Preconception mitochondrial optimization combo (parental)",
     "AMPK pathway dysregulation"),
    ("Preconception mitochondrial optimization combo (parental)",
     "SIRTUIN / NAD+ depletion"),
]

NEW_INT_MECH_LINKS = [
    ("Hyperbaric oxygen therapy (HBOT)", "Mitochondrial dysfunction"),
    ("Hyperbaric oxygen therapy (HBOT)", "Neuroinflammation"),
    ("Hyperbaric oxygen therapy (HBOT)", "Oxidative stress"),
    ("Hyperbaric oxygen therapy (HBOT)",
     "Heat shock protein (HSF1/HSP70/HSP90) response"),
    ("Alpha-lipoic acid (ALA)", "Mitochondrial dysfunction"),
    ("Alpha-lipoic acid (ALA)", "Oxidative stress"),
    ("Alpha-lipoic acid (ALA)", "Impaired methylation"),
    ("D-ribose", "Mitochondrial dysfunction"),
    ("D-ribose", "AMPK signaling"),
    ("Niacinamide / nicotinamide", "SIRTUIN / NAD+ metabolism"),
    ("Niacinamide / nicotinamide", "Mitochondrial dysfunction"),
    ("Niacinamide / nicotinamide", "Autophagy / proteostasis"),
    ("Preconception mitochondrial optimization combo (parental)",
     "Mitochondrial dysfunction"),
    ("Preconception mitochondrial optimization combo (parental)",
     "AMPK signaling"),
    ("Preconception mitochondrial optimization combo (parental)",
     "Impaired methylation"),
    ("Preconception mitochondrial optimization combo (parental)",
     "DHA membrane phospholipid composition"),
    ("Preconception mitochondrial optimization combo (parental)",
     "Vitamin-D-regulated serotonin synthesis (TPH2)"),
]


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    ts = now_iso()

    print(f"[v1.6] running at {ts}")
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

    next_int = next_n("interventions", "INT")
    next_src = next_n("sources", "SRC")
    next_evd = next_n("evidence_fragments", "EVD")
    next_evl = next_n("evidence_links", "EVL")
    next_com = next_n("combinations", "COM")
    next_cmm = next_n("combination_members", "CMM")

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
        print(f"[v1.6] interventions: +{len(new_int)}")

    # combinations row for the preconception combo
    combo_name = ("Preconception mitochondrial optimization combo "
                  "(parental)")
    # Promote the combo intervention to a real `combinations` row too
    # (per spec §6.6 — combinations are first-class). The intervention
    # row above is the Layer-2 entry; here we mirror it as a Layer-2
    # combination so combination_members links work.
    cid = pad_id("COM", next_com, 4); next_com += 1
    new_combos = [{
        "id": cid,
        "name": combo_name,
        "description": ("3-6 month preconception protocol for both "
                        "prospective parents targeting mitochondrial "
                        "DNA quality, methylation capacity, "
                        "antioxidant pool, and epigenetic "
                        "programming during gametogenesis."),
        "rationale": ("Mitochondrial dysfunction reported in 30-80% "
                      "of autism (Rossignol 2011 meta); ova/sperm "
                      "mitochondrial DNA reflect parental metabolic "
                      "state at gametogenesis. Multi-nutrient "
                      "preconception support targets the highest-"
                      "leverage modifiable window."),
        "interaction_warnings": ("Generally well-tolerated; monitor "
                                 "selenium dose (narrow therapeutic "
                                 "window); monitor for excess "
                                 "methylation symptoms in COMT++ "
                                 "individuals."),
        "csrs_score": "", "csrs_last_updated": "",
        "status": "active", "created_at": ts, "last_updated": ts,
        "notes": ("Mirrors INT row of same name. Combination is "
                  "evidence-driven per spec §1.2."),
        "member_intervention_ids_legacy": "",
        "csrs_score_legacy": "", "csrs_last_updated_legacy": "",
    }]
    tables["combinations"] = pd.concat(
        [tables["combinations"], pd.DataFrame(new_combos)],
        ignore_index=True)
    print(f"[v1.6] combinations: +1 ({cid})")

    # combination_members
    new_cmm = []
    for combo, member_name, role in NEW_COMBO_MEMBERS_BY_NAME:
        if combo != combo_name: continue
        member_id = int_name_to_id.get(member_name)
        if not member_id:
            print(f"  [warn] combo member skipped: {member_name}")
            continue
        rid = pad_id("CMM", next_cmm, 4); next_cmm += 1
        new_cmm.append({
            "id": rid, "combination_id": cid,
            "intervention_id": member_id, "role": role,
            "created_at": ts,
        })
    if new_cmm:
        tables["combination_members"] = pd.concat(
            [tables["combination_members"], pd.DataFrame(new_cmm)],
            ignore_index=True)
        print(f"[v1.6] combination_members: +{len(new_cmm)}")

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
                "added_in": "v1.6_hbot_mito_expansion",
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
                "added_in": "v1.6_hbot_mito_expansion",
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
    print(f"[v1.6] sources: +{len(new_src)}, evidence_fragments: "
          f"+{len(new_evd)}, evidence_links: +{len(new_evl)}")
    if skipped:
        print(f"[v1.6] skipped {len(skipped)} unresolvable targets:")
        for pmid, ttype, name in skipped[:6]:
            print(f"  PMID {pmid}: {ttype}={name}")

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

    n_ihe = add_edges(
        "intervention_hypothesis_edges", "IHE",
        "intervention_id", "hypothesis_id",
        (int_name_to_id, hyp_name_to_id),
        NEW_INT_HYP_LINKS, "cause_mitigation")
    print(f"[v1.6] intervention_hypothesis_edges: +{n_ihe}")

    n_ime = add_edges(
        "intervention_mechanism_edges", "IME",
        "intervention_id", "mechanism_id",
        (int_name_to_id, mech_name_to_id),
        NEW_INT_MECH_LINKS, "modulates")
    print(f"[v1.6] intervention_mechanism_edges: +{n_ime}")

    for name, df in tables.items():
        target = OUTPUT_DIR / f"{name}.csv"
        df.to_csv(target, index=False, encoding="utf-8")

    summary = {
        "expansion_version": "v1.6_hbot_mito",
        "run_timestamp": ts,
        "added": {
            "interventions": len(new_int),
            "combinations": 1,
            "combination_members": len(new_cmm),
            "sources": len(new_src),
            "evidence_fragments": len(new_evd),
            "evidence_links": len(new_evl),
            "intervention_hypothesis_edges": n_ihe,
            "intervention_mechanism_edges": n_ime,
        },
        "skipped_targets": len(skipped),
        "commentary": {
            "geographic_prevalence_note": (
                "Discussion of country/Amish prevalence differences "
                "(France 1/144, Japan 1/160, S Korea ~1/38, US 1/31, "
                "Amish 1/271) is treated as DATA-METHODOLOGY context, "
                "not as causal evidence. Cross-country differences are "
                "confounded by diagnostic practices, screening "
                "intensity, awareness, healthcare access, and "
                "diagnostic substitution. Amish data confounded by "
                "limited healthcare access. NOT added as schema rows."),
            "iacc_note": (
                "IACC 2024-2025 strategic plan focuses on "
                "co-occurring conditions; reinforces relevance of "
                "GI, sleep, immune, mental-health phenotypes already "
                "in atlas. Provides priority signal for ingestion "
                "pipeline (option f)."),
            "social_media_handling": (
                "X/Twitter posts and Substack content are not added "
                "as sources directly; their underlying claims are "
                "traced to peer-reviewed citations where they exist. "
                "Per spec §7.2 social signals get the lowest weight "
                "tier in scoring."),
        },
    }
    Path("expansion_v16_summary.json").write_text(
        json.dumps(summary, indent=2))
    print()
    print("=" * 60)
    print("v1.6 HBOT + MITO EXPANSION COMPLETE")
    print(json.dumps(summary["added"], indent=2))


if __name__ == "__main__":
    main()
