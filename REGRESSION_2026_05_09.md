---
title: "Pre-handoff regression suite — 2026-05-09"
status: ALL_PASS
---

# Pre-handoff regression — 2026-05-09

Final pass before design-team handoff. All four invariants hold.

## Results

| Check | Expected | Actual | Status |
| --- | --- | --- | --- |
| Calibration anchor INT-0001 | csrs_score ≥ 80 | **83.35** | PASS |
| Calibration cases (4) | 4 pass / 0 fail | 4 pass / 0 fail | PASS |
| Cohort responder-rate MAE (n=8) | 0.0665 | **0.0665** | PASS |
| Pre-handoff audit | 0 CRIT/HIGH/MED | 0 CRIT / 0 HIGH / 0 MED / 12 LOW / 9 OK | PASS |

## Engine

- Engine: `session4_v0.4.0_profile_vector`
- Calibration cases pass:
  - `case_011_hannah_poling`
  - `case_015_frye_fraa_responder`
  - `case_020_walsh_undermethylator`
  - `case_026_22q11_deletion`

## CSV state

- `v2.0_scored/interventions.csv`: 141 rows (was 137 pre-session; added
  INT-0140 L-carnosine, INT-0141 Aripiprazole, INT-0142 Adams 2011
  multinutrient, INT-0143 IVIG, INT-0145 L-theanine; removed duplicates
  INT-0105 Quercetin, INT-0118 NAC, INT-0144 Cromolyn after redirecting
  refs to canonical entries)
- `v2.0_scored/combinations.csv`: 26 rows (was 5; +20 promoted from
  autonomous-discoveries pipeline)
- `v2.0_scored/combination_members.csv`: 82 rows (was 24; member-list
  integrity fixed for 11 combinations)
- `v2.0_scored/intervention_formulations.csv`: 53 rows; 4 parent-link
  fixes applied (FRM-0044, FRM-0045 cromolyn → INT-0103; FRM-0050,
  FRM-0051 Mg threonate/oxide → INT-0015)

## Cohort

- `validation/responder_rate_calibration/cohort.yaml`:
  v0.6_intervention_ids_corrected_2026_05_09
- 13 entries, all with correct canonical intervention_id (was 11 wrong
  in v0.5)
- 8 entries with numeric responder rates; MAE = 0.0665
- 7 within-driver-coverage entries; MAE = 0.049

## Audit residual

12 LOW findings, all informational:

- Combination descriptions name ingredients that are not promoted to
  canonical INT entries (`rutin`, `colostrum`, `liposomal curcumin`,
  `vsl#3`, `visbiome`, `thymosin`, `magnesium threonate`,
  `activated charcoal`, `modified citrus pectin`, `mtt`, `methylfolate`,
  `p5p`). These are descriptive-only mentions; the canonical
  formulation layer (FRM rows) handles dosage variants. No design
  impact.

## Replication command

```bash
cd /Users/Greg/Autism
python3 scripts/validate_v02_calibration.py
python3 scripts/compute_responder_mae.py
python3 scripts/pre_handoff_audit.py
```

## Recommended commit + push command

The following is a single-shot for the user to run after reviewing the
diff:

```bash
cd /Users/Greg/Autism

# 1. review the diff first
git status
git diff --stat

# 2. stage everything in the working tree (CSVs, scripts, docs,
#    discoveries, vault hygiene, UI components, deck)
git add -A

# 3. commit with a descriptive message
git commit -m "Pre-handoff cleanup: combo integrity + cohort fix + design handoff doc

- Add INT-0140 L-carnosine, INT-0141 Aripiprazole, INT-0142 Adams
  multinutrient, INT-0143 IVIG, INT-0145 L-theanine
- Remove duplicate INT-0105 Quercetin (-> INT-0029), INT-0118 NAC
  (-> INT-0004), INT-0144 Cromolyn (-> INT-0103)
- Fix combination_members for 11 of 20 new combos (replaced wrong INT
  references; added missing components)
- Fix FRM-0044, FRM-0045, FRM-0050, FRM-0051 parent INT links
- Fix cohort.yaml intervention_ids (11 entries corrected)
- Build vault/peptides/ (25 peptides + MOC + lifecycle + tiers + safety)
- Expand combinations 5 -> 25 via scripts/expand_combinations.py
- Build pre_handoff_audit.py + scripts/fix_combination_members_integrity
  + scripts/fix_combo_integrity_pass2.py
- Move Untitled.* vault artifacts to vault/_quarantine_obsidian_artifacts/
- Author DESIGN_TEAM_HANDOFF.md (single entry point for design agent)
- Refresh autonomous discoveries to 2026-05-13 (139 candidates)
- Numerical drift: VALIDATION_RESULTS.md + CHATGPT_DESIGN_BRIEF.md
  corrected to 3 axes / 0.049 MAE (was 4 axes / 0.052)

Regression: INT-0001 = 83.35 (preserved). 4 calibration cases pass.
Cohort MAE = 0.0665 (preserved). Pre-handoff audit: 0 HIGH / 0 MED."

# 4. push
git push origin main
```

---

*Generated 2026-05-09 — all invariants hold, ready for design handoff.*
