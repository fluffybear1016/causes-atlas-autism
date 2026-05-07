#!/usr/bin/env python3
"""patch_cohort_responder_rates_batch2.py

Populate full-text-extracted responder data for cohort entries:
  rrc_009 Kang 2017 MTT      (PMID 28122648)
  rrc_010 Rossignol 2012 HBOT (PMID 22703610)
  rrc_012 Tsilioni 2015 luteolin (PMID 26418275)

Each value cited to specific table/page in the source PDF.

Run from /Users/Greg/Autism:
    python3 scripts/patch_cohort_responder_rates_batch2.py
"""
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
COHORT_PATH = ROOT / "validation" / "responder_rate_calibration" / "cohort.yaml"

PATCHES: dict[str, dict] = {
    "rrc_009_kang_2017_microbiota_transfer": {
        "n_total_in_stratum": 18,
        "n_responder_in_stratum": 16,
        "published_responder_rate": 0.889,
        "placebo_responder_rate": None,
        "responder_definition": (
            "≥50% reduction in average GSRS (Gastrointestinal Symptom Rating Scale) "
            "from baseline; ASD-related behavior improvement also reported "
            "(CARS −22%, VABS-II +1.4y dev age) but the dichotomized responder "
            "criterion is the GSRS-reduction cutoff."
        ),
        "representative_input_profile_path": "representative_inputs/rrc_009.json",
        "expected_engine_behavior": {
            "intervention_in_top_5": True,
            "primary_target_dimension": "PHE-0004",
            "profile_dominant_dimensions_must_include": ["PHE-0004"],
        },
        "status": "full_text_extracted_2026_05_07",
        "response_minus_placebo": None,
        "effect_size_cohen_d": None,
        "p_value": 0.001,
        "p_value_test": (
            "two-tailed Wilcoxon signed-rank test on GSRS pre-vs-post "
            "(p<0.001 at end of treatment; p=0.002 after 8-week observation)"
        ),
        "extraction_notes": (
            "Source: Kang 2017 Microbiome (open access). Results section "
            "page 7-8 + Figure 2a. Quote: 'Only two out of 18 children with "
            "ASD (11%) achieved less than 50% reduction in the average GSRS, "
            "the cutoff for improvement, and were designated as non-responders.' "
            "→ responder rate = 16/18 = 0.889. Open-label, no placebo arm — "
            "a major caveat for the responder rate magnitude. Trial design is "
            "GI-symptom-stratified (inclusion criterion: moderate-to-severe "
            "GI problems), so this is a clean stratified-subgroup entry for "
            "PHE-0004 (GI/microbiome) calibration."
        ),
        "pmid_verified_at_fulltext": "2026-05-07",
    },
    "rrc_010_rossignol_2012_hbot": {
        "n_total_in_stratum": None,
        "n_responder_in_stratum": None,
        "published_responder_rate": None,
        "placebo_responder_rate": None,
        "responder_definition": (
            "Per-paper composite behavioral outcomes; review aggregates 2 "
            "controlled trials (Rossignol 2009 multicenter RCT [125] and "
            "Granpeesheh 2010 [120]) with conflicting results. No single "
            "dichotomized responder rate published at the review level."
        ),
        "representative_input_profile_path": "representative_inputs/rrc_010.json",
        "expected_engine_behavior": {
            "intervention_in_top_5": True,
            "primary_target_dimension": "PHE-0002",
            "_representative_input_authored_for_qualitative_check_only": True,
        },
        "status": "review_extracted_excluded_from_mae_2026_05_07",
        "response_minus_placebo": None,
        "effect_size_cohen_d": None,
        "p_value": None,
        "p_value_test": None,
        "extraction_notes": (
            "Source: Rossignol 2012 Med Gas Res review (PMID 22703610), "
            "open access. CRITICAL FRAMING: this entry is a REVIEW of HBOT-"
            "in-ASD evidence, NOT a single RCT. The review aggregates two "
            "controlled trials with conflicting results: Rossignol 2009 "
            "multicenter RCT [ref 125, PMID 19284641] showed effect sizes "
            "0.55-1.00 favoring HBOT; Granpeesheh 2010 [ref 120] showed "
            "no significant changes. Rossignol 2012 explicitly hypothesizes "
            "that 'the variability in results between studies could also "
            "have been due to certain subgroups of children with ASD "
            "responding differently to HBOT' (p9), specifically children "
            "with abnormal cytokines, higher inflammatory markers, cerebral "
            "hypoperfusion, or mitochondrial dysfunction. This is the "
            "responder-stratification claim. Because the review does not "
            "publish a dichotomized stratum responder rate, this entry is "
            "EXCLUDED from cohort responder-rate MAE computation. The "
            "representative input profile (rrc_010.json) encodes the "
            "mito-vulnerable + neuroinflammatory subset claim qualitatively "
            "for engine structural-test purposes only. Future work: add "
            "Rossignol 2009 (PMID 19284641) as a separate cohort entry "
            "with its actual published responder rate."
        ),
        "pmid_verified_at_fulltext": "2026-05-07",
    },
    "rrc_012_tsilioni_2015_luteolin": {
        "n_total_in_stratum": 10,
        "n_responder_in_stratum": 10,
        "published_responder_rate": 0.263,
        "placebo_responder_rate": None,
        "responder_definition": (
            "Subgroup-membership-as-responder framing: of n=38 ASD children, "
            "n=10 had elevated baseline serum IL-6 AND TNF (post-hoc bimodal "
            "stratification, page 2). This high-cytokine subgroup showed "
            "significant VABS improvement at 26 weeks (effect sizes 0.35-0.45 "
            "across communication/daily-living/social/composite, p=0.0003 to "
            "p=0.008 per Table 1 page 3). Low-cytokine subgroup did not. "
            "Cohort-level responder fraction = 10/38 = 0.263."
        ),
        "representative_input_profile_path": "representative_inputs/rrc_012.json",
        "expected_engine_behavior": {
            "intervention_in_top_5": True,
            "primary_target_dimension": "PHE-0003",
            "profile_dominant_dimensions_must_include": ["PHE-0003"],
        },
        "status": "full_text_extracted_2026_05_07",
        "response_minus_placebo": None,
        "effect_size_cohen_d": 0.42,  # composite VABS effect size, Table 1
        "p_value": 0.001,  # composite VABS, Table 1
        "p_value_test": (
            "general linear model for repeated measures, VABS composite score, "
            "high-IL-6/TNF subgroup pre-vs-post"
        ),
        "extraction_notes": (
            "Source: Tsilioni 2015 Transl Psychiatry (PMID 26418275), open "
            "access. CRITICAL CAVEAT: this is an OPEN-LABEL trial, not an "
            "RCT — no placebo arm, n=38 ASD children all received the "
            "luteolin-containing dietary formulation (NeuroProtek: luteolin "
            "100mg + quercetin 70mg + rutin 30mg) for 26 weeks. Stratification "
            "is post-hoc on baseline serum IL-6 + TNF (bimodal distribution, "
            "page 2): n=10 in high-cytokine cluster, n=28 in low-cytokine "
            "cluster. The high-cytokine subgroup showed significant VABS "
            "improvement (Table 1 page 3): communication AE 38.91→48.64 "
            "(d=0.38, p=0.008), daily living 38.45→45.09 (d=0.35, p=0.0003), "
            "social 36.55→44.64 (d=0.45, p=0.001), composite 37.97→46.12 "
            "(d=0.42, p=0.001). Cytokines significantly decreased in the "
            "high-cytokine subgroup post-treatment (IL-6 p=0.036, TNF "
            "p=0.015). The paper does NOT dichotomize responders at the "
            "individual level; the 'responder rate' encoded here uses the "
            "subgroup-membership-as-responder convention (10/38=0.263), "
            "which is the most defensible numeric value extractable. This "
            "tests whether the engine's MCAS-like / inflammatory-stratifier "
            "logic correctly predicts the proportion of cohort that "
            "responds — Theoharides framework."
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

    cohort["cohort_version"] = "v0.3_full_text_extracted_8_of_13"
    COHORT_PATH.write_text(yaml.safe_dump(cohort, sort_keys=False, width=88))
    print(f"\nWrote {COHORT_PATH}")
    print(f"Cohort version: v0.3_full_text_extracted_8_of_13")


if __name__ == "__main__":
    main()
