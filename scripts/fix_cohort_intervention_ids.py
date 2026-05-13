#!/usr/bin/env python3
"""fix_cohort_intervention_ids.py — atomically fix the 11 cohort entries
whose intervention_id does not match the canonical atlas.

Findings from pre_handoff_audit.py:
- rrc_002 INT-0023 (Taurine) → should be INT-0005 (Bumetanide)
- rrc_003 INT-0030 (Choline) → INT-0002 (Sulforaphane)
- rrc_004 INT-0029 (Quercetin) → INT-0004 (NAC)
- rrc_005 INT-0036 (Rapamycin) → INT-0140 (NEW: L-carnosine)
- rrc_007 INT-0042 (GAPS) → INT-0046 (Sleep+melatonin combo; closest match)
- rrc_008 INT-0029 (Quercetin) → INT-0141 (NEW: Aripiprazole)
- rrc_009 INT-0025 (Probiotics) → INT-0076 (FMT; MTT closest canonical match)
- rrc_010 INT-0017 (P5P) → INT-0092 (HBOT)
- rrc_011 INT-0018 (TMG) → INT-0142 (NEW: Adams vitamin/mineral)
- rrc_012 INT-0006 (LDN) → INT-0106 (Luteolin BBB-crossing)
- rrc_013 INT-0027 (Curcumin) → INT-0143 (NEW: IVIG)

Also fixes:
- FRM-0047 (L-carnosine Chez 2002 formulation) parent_intervention_id:
  INT-0011 (L-carnitine — WRONG MOLECULE) → INT-0140 (L-carnosine)

Verifies INT-0001 unchanged (calibration anchor protected).
"""
from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SCORED = ROOT / "v2.0_scored"
COHORT = ROOT / "validation" / "responder_rate_calibration" / "cohort.yaml"

NOW = datetime.utcnow().isoformat() + "+00:00"

NEW_INTERVENTIONS = [
    {
        "id": "INT-0140",
        "name": "L-carnosine (oral dipeptide)",
        "category": "supplement",
        "directionality": "treatment",
        "mechanism_summary": "Beta-alanyl-L-histidine dipeptide. GABA modulation via homocarnosine pathway; possible anticonvulsant + frontal/temporal cortex protective effects. Used by Chez 2002 J Child Neurol RCT (PMID 12585724) at 800 mg/day in autism.",
        "dose_range": "800 mg/day (Chez 2002 dose)",
        "cost_per_month_usd": "20",
        "otc_or_rx": "otc",
        "pediatric_safe": "yes",
        "csrs_score": "",
        "csrs_last_updated": "",
        "status": "active",
        "mainstream_consensus_position": "Small pediatric RCT (Chez 2002, n=31) showed significant improvement on Gilliam ARS + Receptive Vocabulary; not replicated at scale.",
        "created_at": NOW,
        "last_updated": NOW,
        "notes": "Added 2026-05-09 to fix rrc_005 cohort entry. Distinct molecule from L-carnitine (INT-0011). FRM-0047 reparented to this entry.",
    },
    {
        "id": "INT-0141",
        "name": "Aripiprazole",
        "category": "drug",
        "directionality": "treatment",
        "mechanism_summary": "Atypical antipsychotic; partial dopamine D2 agonist + serotonin 5-HT1A agonist + 5-HT2A antagonist. FDA-approved for autism-associated irritability (children 6-17) based on Owen 2009 + Marcus 2009 RCTs.",
        "dose_range": "5-15 mg/day (Owen 2009 RCT range)",
        "cost_per_month_usd": "60",
        "otc_or_rx": "rx",
        "pediatric_safe": "monitored",
        "csrs_score": "",
        "csrs_last_updated": "",
        "status": "active",
        "mainstream_consensus_position": "FDA-approved for pediatric autism irritability. Owen 2009 (PMID 19948625): 52% responder rate on ABC-Irritability ≥25% reduction + CGI-I 1 or 2. Metabolic side effects + weight gain require monitoring.",
        "created_at": NOW,
        "last_updated": NOW,
        "notes": "Added 2026-05-09 to fix rrc_008 cohort entry. Mainstream pharma intervention; population-average effect rather than biomarker-stratified subset. Used as cohort calibration baseline for non-stratified RCTs.",
    },
    {
        "id": "INT-0142",
        "name": "Vitamin/mineral multinutrient supplement (Adams 2011 formulation)",
        "category": "supplement",
        "directionality": "treatment",
        "mechanism_summary": "Broad-spectrum vitamin + mineral + antioxidant + amino-acid + essential-fatty-acid multinutrient. Adams 2011 BMC Pediatrics RCT formulation (PMID 22151477). Targets multiple nutritional deficiencies commonly observed in autism cohorts.",
        "dose_range": "Adams 2011 protocol — full multinutrient daily",
        "cost_per_month_usd": "80",
        "otc_or_rx": "otc",
        "pediatric_safe": "yes",
        "csrs_score": "",
        "csrs_last_updated": "",
        "status": "active",
        "mainstream_consensus_position": "Small RCT (n=104, Adams 2011): continuous outcomes only (PGI-R Average Change p=0.008); no dichotomized responder rate published. Bonus regression analysis: biotin + vitamin K were strongest baseline predictors of clinical response.",
        "created_at": NOW,
        "last_updated": NOW,
        "notes": "Added 2026-05-09 to fix rrc_011 cohort entry. Adams formulation; not a single commercial product.",
    },
    {
        "id": "INT-0143",
        "name": "IVIG (intravenous immunoglobulin)",
        "category": "drug",
        "directionality": "treatment",
        "mechanism_summary": "Pooled-donor immunoglobulin G concentrate. Anti-inflammatory + immunomodulatory in autoimmune neuropsychiatric conditions. Used in PANS/PANDAS subset of autism per Frankovich 2017 PANS Research Consortium guidelines.",
        "dose_range": "1.0-2.0 g/kg per infusion course; cycle schedule varies",
        "cost_per_month_usd": "5000",
        "otc_or_rx": "rx_specialist",
        "pediatric_safe": "monitored",
        "csrs_score": "",
        "csrs_last_updated": "",
        "status": "active",
        "mainstream_consensus_position": "Perlmutter 1999 PANDAS RCT showed OC symptom reduction. Williams 2016 PANDAS RCT did not reach binary statistical significance; open-label IVIG ~50% OCD severity reduction. Frankovich 2017 guidelines list IVIG as preferred treatment for moderate-to-severe PANS.",
        "created_at": NOW,
        "last_updated": NOW,
        "notes": "Added 2026-05-09 to fix rrc_013 cohort entry. Specialist intervention; thrombotic + aseptic-meningitis risk. PANS-overlap subset of autism.",
    },
]

# (rrc_id, old_int_id, new_int_id, new_int_name)
COHORT_FIXES = [
    ("rrc_002_lemonnier_2017_bumetanide",       "INT-0023", "INT-0005", "Bumetanide"),
    ("rrc_003_singh_2014_sulforaphane",         "INT-0030", "INT-0002", "Sulforaphane (broccoli sprout extract)"),
    ("rrc_004_hardan_2012_nac",                 "INT-0029", "INT-0004", "N-Acetylcysteine (NAC)"),
    ("rrc_005_chez_2002_carnosine",             "INT-0036", "INT-0140", "L-carnosine (oral dipeptide)"),
    ("rrc_007_wright_2011_melatonin",           "INT-0042", "INT-0046", "Sleep architecture optimization + melatonin"),
    ("rrc_008_owen_2009_aripiprazole",          "INT-0029", "INT-0141", "Aripiprazole"),
    ("rrc_009_kang_2017_microbiota_transfer",   "INT-0025", "INT-0076", "Fecal microbiota transplantation (FMT) [MTT closest canonical match]"),
    ("rrc_010_rossignol_2012_hbot",             "INT-0017", "INT-0092", "Hyperbaric oxygen therapy (HBOT)"),
    ("rrc_011_adams_2011_vitamin_mineral",      "INT-0018", "INT-0142", "Vitamin/mineral multinutrient supplement (Adams 2011 formulation)"),
    ("rrc_012_tsilioni_2015_luteolin",          "INT-0006", "INT-0106", "Luteolin (BBB-crossing formulation)"),
    ("rrc_013_frankovich_2017_pans_treatment",  "INT-0027", "INT-0143", "IVIG (intravenous immunoglobulin)"),
]


def main() -> None:
    interventions_path = SCORED / "interventions.csv"
    formulations_path = SCORED / "intervention_formulations.csv"

    # Read interventions
    with interventions_path.open() as f:
        rd = csv.DictReader(f)
        int_fieldnames = rd.fieldnames
        int_rows = list(rd)

    int_id_to_row = {r["id"]: r for r in int_rows}

    # Capture INT-0001 BEFORE
    anchor_before = int_id_to_row.get("INT-0001", {}).get("csrs_score")

    # Append the 4 new INT entries
    new_added = 0
    for new_int in NEW_INTERVENTIONS:
        if new_int["id"] in int_id_to_row:
            print(f"  SKIP {new_int['id']} (already exists)")
            continue
        row = {f: "" for f in int_fieldnames}
        for k, v in new_int.items():
            if k in row:
                row[k] = v
        int_rows.append(row)
        new_added += 1
        print(f"  + {new_int['id']:9s}  {new_int['name'][:60]}")

    # Append new INT rows
    with interventions_path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=int_fieldnames)
        w.writeheader()
        for r in int_rows:
            w.writerow(r)
    print(f"\n  Wrote {len(int_rows)} interventions ({new_added} new)")

    # Capture INT-0001 AFTER
    with interventions_path.open() as f:
        rd = csv.DictReader(f)
        anchor_after = next((r["csrs_score"] for r in rd if r["id"] == "INT-0001"), None)

    # Fix cohort.yaml
    with COHORT.open() as f:
        cohort = yaml.safe_load(f)

    fixed_count = 0
    for fix in COHORT_FIXES:
        entry_id, old_iid, new_iid, new_iname = fix
        for e in cohort["entries"]:
            if e["entry_id"] == entry_id:
                if e.get("intervention_id") == old_iid:
                    e["intervention_id"] = new_iid
                    e["intervention_name"] = new_iname
                    e.setdefault("notes_audit_fix", []).append(
                        f"intervention_id corrected 2026-05-09: {old_iid} → {new_iid} (per pre_handoff_audit.py mismatch finding)"
                    )
                    fixed_count += 1
                    print(f"  ✓ {entry_id}: {old_iid} → {new_iid}")
                else:
                    print(f"  ? {entry_id}: expected {old_iid} but found {e.get('intervention_id')}")
                break

    cohort["cohort_version"] = "v0.6_intervention_ids_corrected_2026_05_09"
    COHORT.write_text(yaml.safe_dump(cohort, sort_keys=False, width=88))
    print(f"\n  Fixed {fixed_count} cohort entries; bumped cohort_version to v0.6")

    # Fix FRM-0047 parent_intervention_id (L-carnosine, was incorrectly INT-0011 L-carnitine)
    with formulations_path.open() as f:
        rd = csv.DictReader(f)
        frm_fieldnames = rd.fieldnames
        frm_rows = list(rd)

    frm_fixed = False
    for r in frm_rows:
        if r.get("formulation_id") == "FRM-0047":
            old_parent = r.get("parent_intervention_id")
            if old_parent == "INT-0011":
                r["parent_intervention_id"] = "INT-0140"
                r["last_updated"] = "2026-05-09"
                # Append to notes if there's a notes field
                if "mechanism_specificity_notes" in r:
                    r["mechanism_specificity_notes"] += " [Parent intervention corrected 2026-05-09: was INT-0011 L-carnitine which is a different molecule.]"
                frm_fixed = True
                print(f"  ✓ FRM-0047: parent_intervention_id INT-0011 → INT-0140")
            break

    if frm_fixed:
        with formulations_path.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=frm_fieldnames, quoting=csv.QUOTE_MINIMAL)
            w.writeheader()
            for r in frm_rows:
                w.writerow(r)
        print(f"  Wrote {len(frm_rows)} formulations")

    print()
    print(f"  Calibration anchor INT-0001:")
    print(f"    BEFORE: {anchor_before}")
    print(f"    AFTER:  {anchor_after}")
    print(f"    Preserved: {anchor_before == anchor_after}")


if __name__ == "__main__":
    main()
