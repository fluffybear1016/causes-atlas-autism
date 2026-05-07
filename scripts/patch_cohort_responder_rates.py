#!/usr/bin/env python3
"""
patch_cohort_responder_rates.py

Populates the responder-rate fields in
validation/responder_rate_calibration/cohort.yaml for the 6 entries
extracted from full-text papers in this session.

Each extraction was performed by reading the published PDF, identifying
the responder analysis (typically Table 2 or Results section), and
recording the published count + denominator + responder definition.
Where the paper does NOT publish a dichotomized responder rate (e.g.,
Adams 2011 reports continuous PGI-R), that's documented explicitly
rather than fabricated.

Per CLAUDE.md verify-before-write protocol: every numeric value below
is traceable to a specific table/page in the corresponding PDF at
validation/responder_rate_calibration/papers/.
"""
from __future__ import annotations
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required.", file=sys.stderr)
    sys.exit(2)

REPO = Path(__file__).resolve().parent.parent
COHORT_YAML = REPO / "validation" / "responder_rate_calibration" / "cohort.yaml"

# ─────────────────────────────────────────────────────────────────────────────
# Extracted data — every value cited to its source location in the paper
# ─────────────────────────────────────────────────────────────────────────────

EXTRACTIONS = {
    "rrc_001_frye_2018_leucovorin_fraa": {
        # Frye 2018 Mol Psychiatry, Table 2B (page 5) — FRAA-positive subgroup
        # ITT denominator from Table 2B footnote^d (folinic n=14) and
        # footnote^e (placebo n=18); responder count derived from %.
        "n_total_in_stratum": 32,  # 14 folinic + 18 placebo (FRAA-positive)
        "n_responder_in_stratum": 10,  # folinic-acid arm responders (10/13 ≈ 77%)
        "published_responder_rate": 0.77,  # 77% (95% CI 54-99%)
        "placebo_responder_rate": 0.22,  # 22% (95% CI 3-41%); 4/18 placebo responders
        "response_minus_placebo": 0.55,  # +55% absolute difference
        "responder_definition": (
            "≥5 standardized point increase on primary verbal communication "
            "outcome (Preschool Language Scale-5 / Clinical Evaluation of "
            "Language Fundamentals); FRAA-positive subgroup analysis."
        ),
        "effect_size_cohen_d": 0.91,  # FRAA+ subgroup, "large" effect
        "p_value": 0.005,  # adjusted; Table 2B
        "p_value_test": "adjusted odds ratio in mixed-model regression",
        "adjusted_odds_ratio": 67.4,
        "adjusted_odds_ratio_ci": [5.6, 999.9],
        "number_needed_to_treat": 1.8,
        "extraction_notes": (
            "Source: Frye 2018 Mol Psychiatry, Table 2B page 5. Responder "
            "definition is paper-defined (5 std-point ≥ minimal clinically "
            "important difference). FRAA-positive subgroup is the cohort's "
            "strongest stratification signal; OR=67.4 reflects very wide CI "
            "due to small subgroup denominator."
        ),
    },
    "rrc_002_lemonnier_2017_bumetanide": {
        # Lemonnier 2017 Transl Psychiatry, Table 3 (page 6) — pooled
        # bumetanide vs placebo; ≥6 CARS point reduction.
        "n_total_in_stratum": 88,  # 65 bumetanide pooled + 23 placebo (FAS)
        "n_responder_in_stratum": 23,  # all 3 bumetanide doses pooled, ≥6 CARS reduction
        "published_responder_rate": 0.354,  # 23/65 = 35.4%
        "placebo_responder_rate": 0.043,  # 1/23 = 4.3%
        "response_minus_placebo": 0.311,
        "responder_definition": (
            "≥6 point reduction on Childhood Autism Rating Scale (CARS) from "
            "screening to day 90. Per-dose responder rates: 0.5 mg b.i.d. "
            "10/20 (50%); 1.0 mg b.i.d. 5/23 (22%); 2.0 mg b.i.d. 8/22 (36%)."
        ),
        "effect_size_cohen_d": None,  # not directly reported as Cohen's d in this format
        "p_value": 0.0029,  # Fisher's exact, ≥6 CARS responder analysis
        "p_value_test": "Fisher's exact test, ≥6 CARS reduction responder analysis",
        "extraction_notes": (
            "Source: Lemonnier 2017 Transl Psychiatry, Table 3 page 6. "
            "IMPORTANT: this RCT was NOT stratified by CSF Cl⁻ or KCC2 "
            "biomarker — it's an unstratified pediatric ASD population "
            "(CARS ≥34, age 2-18). The cohort.yaml's earlier "
            "stratifier_biomarker = csf_or_neuronal_intracellular_chloride_"
            "proxy was aspirational; the trial doesn't actually use it."
        ),
    },
    "rrc_004_hardan_2012_nac": {
        # Hardan 2012 Biol Psychiatry — Table 2 + page 958 prose for CGI-I
        # responder counts (CGI-I = 2, "much improved").
        "n_total_in_stratum": 29,  # 14 NAC + 15 placebo with follow-up
        "n_responder_in_stratum": 5,  # NAC arm CGI-I = "much improved"
        "published_responder_rate": 0.357,  # 5/14 = 35.7% (CGI-I ≤ 2)
        "placebo_responder_rate": 0.133,  # 2/15 = 13.3%
        "response_minus_placebo": 0.224,
        "responder_definition": (
            "CGI-I = 1 ('very much improved') or 2 ('much improved') at "
            "12 weeks. Per-subject CGI-I distribution from page 958 prose. "
            "Note: paper's primary statistic was continuous ABC-Irritability "
            "change (Cohen's d = 0.96), not the binary responder count."
        ),
        "effect_size_cohen_d": 0.96,  # ABC-Irritability primary continuous outcome
        "p_value": 0.001,  # continuous primary outcome F = 6.80
        "p_value_test": "mixed-effects regression, ABC-Irritability change",
        "extraction_notes": (
            "Source: Hardan 2012 Biol Psychiatry, Table 2 page 959 + prose "
            "page 958. The binary responder count was NOT the primary "
            "statistic — paper analyzed continuous ABC-Irritability change "
            "via mixed-effects regression (F=6.80, p<.001, d=.96). Binary "
            "count derived from per-subject CGI-I narrative description."
        ),
    },
    "rrc_006_hendren_2016_methyl_b12": {
        # Hendren 2016 J Child Adolesc Psychopharmacol — Results page 6
        # (B12: 14/27 responders; Placebo: 6/23 responders).
        "n_total_in_stratum": 50,  # 27 B12 + 23 placebo with valid CGI-I
        "n_responder_in_stratum": 14,  # B12 arm
        "published_responder_rate": 0.519,  # 14/27 = 51.9%
        "placebo_responder_rate": 0.261,  # 6/23 = 26.1%
        "response_minus_placebo": 0.258,
        "responder_definition": (
            "CGI-I = 1 ('very much improved') or 2 ('much improved') at "
            "8 weeks. Subset analysis (Table 5) showed responders had "
            "significantly lower baseline plasma methionine (17.3 vs 21.6 μM, "
            "p=0.006), suggesting methylation-deficient subgroup enrichment."
        ),
        "effect_size_cohen_d": 0.84,  # continuous CGI-I difference 0.7 points
        "p_value": 0.086,  # binary responder analysis
        "p_value_test": "Fisher's exact, binary responder",
        "p_value_continuous": 0.005,  # continuous mean CGI-I (B12 2.4 vs placebo 3.1)
        "extraction_notes": (
            "Source: Hendren 2016, Results page 6. The continuous mean CGI-I "
            "primary outcome was significant (p=0.005, d=0.84); the binary "
            "responder analysis trended toward significance (p=0.086) but "
            "did not reach the 0.05 threshold. Paper notes this is likely "
            "due to information loss in dichotomization. Cohort entry uses "
            "binary responder rate per ChatGPT validation framing."
        ),
    },
    "rrc_008_owen_2009_aripiprazole": {
        # Owen 2009 Pediatrics — page 1537 explicit responder analysis.
        "n_total_in_stratum": 95,  # 46 aripiprazole + 49 placebo (efficacy sample)
        "n_responder_in_stratum": 24,  # 52.2% × 46 ≈ 24
        "published_responder_rate": 0.522,  # 52.2% at week 8
        "placebo_responder_rate": 0.143,  # 14.3%
        "response_minus_placebo": 0.379,
        "responder_definition": (
            "≥25% reduction in ABC-Irritability subscale score AND CGI-I = 1 "
            "or 2 at week 8 (composite responder criterion)."
        ),
        "effect_size_cohen_d": 0.87,  # continuous ABC-Irritability TD = -7.9
        "p_value": 0.001,  # responder analysis significant from week 1
        "p_value_test": "χ² test, composite responder criterion",
        "extraction_notes": (
            "Source: Owen 2009 Pediatrics, Results page 1537 + Figure 3. "
            "Industry-funded BMS/Otsuka submission trial; responder analysis "
            "is rigorous and pre-specified. NOT biomarker-stratified — "
            "inclusion was CGI-S ≥4 + ABC-I ≥18 (irritability severity)."
        ),
    },
    "rrc_011_adams_2011_vitamin_mineral": {
        # Adams 2011 BMC Pediatr — does NOT publish a dichotomized responder
        # rate. Primary outcome is continuous PGI-R Average Change.
        "n_total_in_stratum": 104,  # 53 supplement + 51 placebo (completed forms)
        "n_responder_in_stratum": None,  # not published as dichotomized count
        "published_responder_rate": None,  # not a dichotomized analysis
        "placebo_responder_rate": None,
        "response_minus_placebo": None,
        "responder_definition": (
            "Paper does NOT publish a dichotomized responder rate. Primary "
            "outcome is continuous Parental Global Impressions-Revised "
            "Average Change score. Significance reported as p-values: "
            "PGI-R Average Change p=0.008; Hyperactivity p=0.003; "
            "Tantrumming p=0.009; Overall p=0.02; Receptive Language p=0.03."
        ),
        "effect_size_cohen_d": None,  # not reported
        "p_value": 0.008,  # PGI-R Average Change primary outcome
        "p_value_test": "unpaired t-test, PGI-R Average Change",
        "extraction_notes": (
            "Source: Adams 2011 BMC Pediatr (open access), Abstract + "
            "Results. NO dichotomized responder rate published — outcomes "
            "are continuous. This entry is retained in the cohort for "
            "documentation of the continuous-effect signal but cannot "
            "contribute to responder-rate MAE computation. Bonus: paper "
            "reports R²=0.61 regression with biotin and vitamin K as "
            "strongest baseline predictors of clinical response, suggesting "
            "responder-stratification opportunity in re-analysis."
        ),
    },
}


def main():
    if not COHORT_YAML.exists():
        print(f"ERROR: cohort.yaml not found: {COHORT_YAML}", file=sys.stderr)
        sys.exit(2)
    cohort = yaml.safe_load(COHORT_YAML.read_text(encoding="utf-8")) or {}
    entries = cohort.get("entries", []) or []

    patched = 0
    for entry in entries:
        eid = entry.get("entry_id")
        if eid not in EXTRACTIONS:
            continue
        ext = EXTRACTIONS[eid]
        # Replace the previous <extract from paper> placeholder fields and add
        # the new effect-size + extraction_notes fields.
        for k, v in ext.items():
            entry[k] = v
        # Mark status as full-text-extracted
        entry["status"] = "full_text_extracted_2026_05_07"
        # Update pmid_verified_at to mark we re-verified at full-text level
        entry["pmid_verified_at_fulltext"] = "2026-05-07"
        patched += 1
        print(f"  ✓ {eid}")

    cohort["cohort_version"] = "v0.2_full_text_extracted_6_of_13"
    cohort["last_updated"] = "2026-05-07"

    with open(COHORT_YAML, "w", encoding="utf-8") as f:
        yaml.safe_dump(cohort, f, default_flow_style=False, sort_keys=False,
                       allow_unicode=True, width=120)

    print(f"\n{patched} entries patched.")
    print(f"Cohort version → v0.2_full_text_extracted_6_of_13")


if __name__ == "__main__":
    main()
