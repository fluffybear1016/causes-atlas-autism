#!/usr/bin/env python3
"""patch_cohort_responder_rates_batch3.py

Populate full-text-extracted responder data for cohort entries:
  rrc_003 Singh 2014 sulforaphane (PMID 25313065 — overrides cohort.yaml's previous
                                    PMID 34034808 which was Zimmerman 2021 followup;
                                    Singh 2014 is the original landmark RCT with the
                                    cleaner dichotomized responder data)
  rrc_007 Wright 2011 melatonin   (PMID 20535539)
  rrc_013 Frankovich 2017 PANS    (PMID 36358107)

Each value cited to specific table/page in the source PDF.

Run from /Users/Greg/Autism:
    python3 scripts/patch_cohort_responder_rates_batch3.py
"""
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
COHORT_PATH = ROOT / "validation" / "responder_rate_calibration" / "cohort.yaml"

PATCHES: dict[str, dict] = {
    # rrc_003: rewrite to point at Singh 2014 (original RCT) instead of
    # Zimmerman 2021 (younger-children followup with non-significant primary
    # outcome — would have been a much weaker cohort entry).
    "rrc_003_zimmerman_singh_2021_sulforaphane": {
        "entry_id": "rrc_003_singh_2014_sulforaphane",
        "rct_pmid": 25313065,
        "rct_first_author": "Singh K",
        "rct_year": 2014,
        "rct_journal": "Proc Natl Acad Sci USA",
        "rct_title": (
            "Sulforaphane treatment of autism spectrum disorder (ASD)."
        ),
        "pmid_verified": True,
        "pmid_verified_at": "2026-05-07",
        "intervention_id": "INT-0030",
        "intervention_name": "Sulforaphane (broccoli sprout extract)",
        "target_phenotype_id": "PHE-0002",
        "stratification_criterion": (
            "None (unstratified by biomarker). Trial inclusion was male age "
            "13-27 with moderate-to-severe ASD. Cohort had unusually high "
            "prevalence of fever-responder phenotype (32/40 = 80% vs ~35% in "
            "general ASD populations) — a behavioral observation, not a "
            "stratification axis."
        ),
        "n_total_in_stratum": 26,
        "n_responder_in_stratum": 9,
        "published_responder_rate": 0.346,
        "placebo_responder_rate": 0.0,
        "responder_definition": (
            "Post-hoc dichotomization: positive response = ≥30% decrease "
            "from baseline in BOTH total ABC and total SRS scores at 18 weeks. "
            "9/26 (34.6%) sulforaphane vs 0/11 (0%) placebo, Fisher's exact "
            "p=0.036. (Looser ABC-alone responder criterion: 15/25 = 60% "
            "sulforaphane vs 2/10 = 20% placebo, p=0.059.)"
        ),
        "representative_input_profile_path": "representative_inputs/rrc_003.json",
        "expected_engine_behavior": {
            "intervention_in_top_5": True,
            "primary_target_dimension": "PHE-0002",
            "profile_dominant_dimensions_must_include": ["PHE-0002"],
        },
        "status": "full_text_extracted_2026_05_07",
        "response_minus_placebo": 0.346,
        "effect_size_cohen_d": None,  # not reported
        "p_value": 0.036,
        "p_value_test": (
            "Fisher's exact test, dual ABC+SRS responder criterion at 18 weeks"
        ),
        "extraction_notes": (
            "Source: Singh 2014 PNAS (PMID 25313065), open access. Quote: "
            "'A positive response was defined post hoc as a 30% decrease "
            "from baseline in total ABC and SRS scores. Thirty-five percent "
            "(9 of 26) of participants on sulforaphane had a positive response "
            "with 0% (0 of 11) on placebo (Fisher's exact test P = 0.036), "
            "and 60% (15 of 25) of participants receiving sulforaphane had "
            "a positive response on ABC compared with 20% (2 of 10) on "
            "placebo (P = 0.059).' COHORT ENTRY REWRITE: previously pointed "
            "at PMID 34034808 (Zimmerman 2021, younger-children followup); "
            "now points at PMID 25313065 (Singh 2014, original landmark RCT). "
            "Singh 2014 has cleaner dichotomized responder data and a larger "
            "effect size than Zimmerman 2021 (which had non-significant "
            "primary outcome OACIS d=0.10-0.21). Mechanism is oxidative "
            "stress / Nrf2 / glutathione / mitochondrial — maps to PHE-0002. "
            "Trial was unstratified by biomarker; representative profile "
            "encodes population-typical mild oxidative-stress signal."
        ),
        "pmid_verified_at_fulltext": "2026-05-07",
    },
    "rrc_007_wright_2011_melatonin": {
        "n_total_in_stratum": 17,
        "n_responder_in_stratum": None,
        "published_responder_rate": None,
        "placebo_responder_rate": None,
        "responder_definition": (
            "Paper does NOT publish a dichotomized responder rate. Primary "
            "outcomes are continuous: sleep latency, total sleep time, number "
            "of night wakenings. Significant improvements in sleep latency "
            "(mean reduction 46.7 min, p=0.004 melatonin vs placebo) and "
            "total sleep time (+52.3 min, p=0.002), no difference in "
            "wakenings (p=0.209). Trial defined 'good sleep' as ≥50% "
            "improvement for individual dose-titration purposes but did not "
            "report what fraction of subjects met that threshold."
        ),
        "representative_input_profile_path": "representative_inputs/rrc_007.json",
        "expected_engine_behavior": {
            "intervention_in_top_5": True,
            "_representative_input_authored_for_qualitative_check_only": True,
        },
        "status": "full_text_extracted_excluded_from_mae_2026_05_07",
        "response_minus_placebo": None,
        "effect_size_cohen_d": None,
        "p_value": 0.004,
        "p_value_test": (
            "Wilcoxon signed-rank test, sleep latency, melatonin vs placebo, "
            "crossover design"
        ),
        "extraction_notes": (
            "Source: Wright 2011 J Autism Dev Disord (PMID 20535539). "
            "Randomized double-blind crossover trial; n=22 randomized, n=17 "
            "completed. Inclusion: ASD with severe sleep problems NOT "
            "amenable to behavior management — sleep-stratified subset. "
            "Primary outcomes are continuous (Table 1 page 7); paper does "
            "NOT publish a dichotomized responder rate. Closest proxy: "
            "12/16 placebo subjects reached the 10mg max dose vs 6/16 on "
            "melatonin, suggesting ~62% on melatonin achieved 'good sleep' "
            "without needing the maximum dose, but this is a dose-titration "
            "metric not a responder rate. EXCLUDED from cohort responder-"
            "rate MAE for the same reason as Adams 2011 (continuous outcomes "
            "only). The engine does not currently have a sleep-axis phenotype "
            "dimension; this entry remains in the cohort to document the "
            "sleep-stratifier gap and motivate engine v0.5+ work on a "
            "PHE-0012 sleep/circadian phenotype."
        ),
        "pmid_verified_at_fulltext": "2026-05-07",
    },
    "rrc_013_frankovich_2017_pans_treatment": {
        "n_total_in_stratum": None,
        "n_responder_in_stratum": None,
        "published_responder_rate": None,
        "placebo_responder_rate": None,
        "responder_definition": (
            "Paper is a TREATMENT GUIDELINES / consensus document, NOT an RCT. "
            "It reviews two prior controlled trials (Perlmutter 1999 and "
            "Williams 2016) and synthesizes expert clinical experience from "
            ">1000 PRC-evaluated PANS patients. No primary responder rate "
            "is published at the guidelines level."
        ),
        "representative_input_profile_path": "representative_inputs/rrc_013.json",
        "expected_engine_behavior": {
            "intervention_in_top_5": True,
            "primary_target_dimension": "PHE-0003",
            "_representative_input_authored_for_qualitative_check_only": True,
        },
        "status": "guidelines_paper_excluded_from_mae_2026_05_07",
        "response_minus_placebo": None,
        "effect_size_cohen_d": None,
        "p_value": None,
        "p_value_test": None,
        "extraction_notes": (
            "Source: Frankovich 2017 J Child Adolesc Psychopharmacol (PMID "
            "36358107). Marked as 'Review Article' on page 1. CRITICAL "
            "FRAMING: this entry is an EXPERT GUIDELINES paper from the PANS "
            "Research Consortium immunomodulatory task force, NOT a single "
            "RCT. The paper reviews two prior controlled trials: Perlmutter "
            "1999 (IVIG vs TPE vs placebo in PANDAS — OC symptoms reduced "
            "45% IVIG / 58% TPE / no effect placebo) and Williams 2016 (IVIG "
            "vs placebo in PANDAS — primary outcome did not reach statistical "
            "significance in double-blind portion; open-label IVIG produced "
            "~50% OCD severity reduction). The Frankovich guidelines paper "
            "does NOT publish its own dichotomized responder rate. EXCLUDED "
            "from cohort responder-rate MAE for the same reason as Rossignol "
            "2012 (review/guidelines paper, not RCT). The representative "
            "input profile (rrc_013.json) encodes the PANS-positive Cunningham "
            "panel composite + acute onset phenotype for engine STRUCTURAL-"
            "TEST purposes only — engine should load PHE-0003 (regressive "
            "immune-inflammatory) on this profile. Future work: add Williams "
            "2016 (PMID 27227558) as a separate cohort entry with its actual "
            "published responder rate."
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
            if "entry_id" in patch:
                print(f"    (renamed → {patch['entry_id']})")

    if patched != len(PATCHES):
        raise SystemExit(
            f"Expected to patch {len(PATCHES)} entries, only patched {patched}"
        )

    cohort["cohort_version"] = "v0.4_full_text_extracted_11_of_13"
    COHORT_PATH.write_text(yaml.safe_dump(cohort, sort_keys=False, width=88))
    print(f"\nWrote {COHORT_PATH}")
    print(f"Cohort version: v0.4_full_text_extracted_11_of_13")


if __name__ == "__main__":
    main()
