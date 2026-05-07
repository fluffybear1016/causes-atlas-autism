#!/usr/bin/env python3
"""patch_cohort_responder_rates_batch4.py

Populate full-text-extracted responder data for the final cohort entry:
  rrc_005 Chez 2002 carnosine (PMID 12585724)

Each value cited to specific table/page in the source PDF.

Run from /Users/Greg/Autism:
    python3 scripts/patch_cohort_responder_rates_batch4.py
"""
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
COHORT_PATH = ROOT / "validation" / "responder_rate_calibration" / "cohort.yaml"

PATCHES: dict[str, dict] = {
    "rrc_005_chez_2002_carnosine": {
        "n_total_in_stratum": 14,  # active arm completers
        "n_responder_in_stratum": None,
        "published_responder_rate": None,
        "placebo_responder_rate": None,
        "responder_definition": (
            "Paper does NOT publish a dichotomized responder rate. Primary "
            "outcomes are continuous: Clinical Global Impression (CGI), "
            "Childhood Autism Rating Scale, Gilliam Autism Rating Scale "
            "(GARS) total + Behavior/Socialization/Communication subscales, "
            "Receptive and Expressive One-Word Picture Vocabulary tests. "
            "Significant 8-week active-arm changes (Table 3 page 836): "
            "CGI 2-vs-6wk p=0.04, Receptive Vocabulary raw p=0.01, GARS "
            "total p=0.04 (Behavior p=0.04, Socialization p=0.01, "
            "Communication p=0.03). Placebo arm (Table 2): all measures NS."
        ),
        "representative_input_profile_path": "representative_inputs/rrc_005.json",
        "expected_engine_behavior": {
            "intervention_in_top_5": True,
            "primary_target_dimension": "PHE-0007",
            "_representative_input_authored_for_qualitative_check_only": True,
        },
        "status": "full_text_extracted_excluded_from_mae_2026_05_07",
        "response_minus_placebo": None,
        "effect_size_cohen_d": None,
        "p_value": 0.04,
        "p_value_test": (
            "paired t-test with Tukey correction, GARS total score, active arm "
            "baseline-vs-8wk"
        ),
        "extraction_notes": (
            "Source: Chez 2002 J Child Neurol (PMID 12585724). N=31 enrolled "
            "(17 placebo + 14 active L-carnosine 800 mg/day), 8 weeks "
            "double-blind RCT, ages 3-12, broad ASD inclusion (NOT biomarker "
            "stratified). 13 subjects had abnormal EEG; 13 were on valproic "
            "acid. Mechanism: GABA modulation via homocarnosine, possible "
            "anticonvulsant effects, frontal/temporal cortex protection. "
            "Maps to PHE-0007 (GABA/Cl⁻ imbalance). EXCLUDED from cohort "
            "responder-rate MAE for two reasons: (1) paper publishes only "
            "continuous outcomes (no dichotomized responder rate, like Adams "
            "2011 and Wright 2011), and (2) PHE-0007 has no biomarker "
            "drivers in v0.3 engine — same architectural gap as Lemonnier "
            "rrc_002. Both gaps would be addressed by the engine v0.4 "
            "refactor. Representative profile (rrc_005.json) encodes the "
            "GABA-imbalance phenotype proxy (epileptiform EEG + valproic acid "
            "concomitant) for engine STRUCTURAL-TEST purposes only."
        ),
        "pmid_verified_at_fulltext": "2026-05-07",
    },
}


def main() -> None:
    raw = COHORT_PATH.read_text()
    cohort = yaml.safe_load(raw)

    patched = 0
    for entry in cohort["entries"]:
        eid = entry["entry_id"]
        if eid in PATCHES:
            patch = PATCHES[eid]
            for key, value in patch.items():
                entry[key] = value
            patched += 1
            print(f"  patched {eid}")

    if patched != len(PATCHES):
        raise SystemExit(
            f"Expected to patch {len(PATCHES)} entries, only patched {patched}"
        )

    cohort["cohort_version"] = "v0.5_full_text_extracted_12_of_13_complete"
    COHORT_PATH.write_text(yaml.safe_dump(cohort, sort_keys=False, width=88))
    print(f"\nWrote {COHORT_PATH}")
    print(f"Cohort version: v0.5_full_text_extracted_12_of_13_complete")
    print()
    print("Note: 12 of 13 entries fully extracted from full-text PDFs;")
    print("rrc_002 Lemonnier remains at scaffold pending engine v0.4")
    print("(which adds PHE-0007 biomarker drivers and unlocks that entry).")


if __name__ == "__main__":
    main()
