# Phase 2 Engine v0.1 — Sub-Agent Audit Punch List

**Audit date:** 2026-04-30
**Scope:** `/Users/Greg/Autism/personalized_risk.py` (605 lines)
**Findings:** 6 CRITICAL + 7 HIGH + 10 MEDIUM + 9 LOW

## CRITICAL

- **C-1** Determinism gap — output not byte-identical between runs because of `computed_at` timestamp (intended) but no canonical-payload digest field for diff-testable equality. Add `canonical_digest: sha256(...)`.
- **C-2** `load_csv` doesn't pin `encoding='utf-8'` or `newline=''` — cross-platform breakage risk.
- **C-3** `stable_sort_rows` silently masks missing-ID rows by collapsing to `""` — should raise.
- **C-4** **Iatrogenic substring match dangerously loose**. `med_name in specific or any(part in med_name for part in specific.split("_"))` would false-positive on tokens like `"sodium"`, `"t3"`, single-character meds. Fix: exact normalized-token match only.
- **C-5** **Postnatal exposures entirely ignored.** Engine only reads `maternal.pregnancy_history.medications` + `gestational_birth_data.vaccinations_administered`. Hannah Poling case is *postnatal* multi-vaccine; engine silently misses this. Calibration anchor passes by accident (mtDNA heteroplasmy alone). Fix: also read `child_data.exposure_history` + `child_data.vaccinations_administered_postnatal` + planned exposures.
- **C-6** Iatrogenic loop indexes wrong sort key (`r.get("id","")` instead of `iatrogenic_id` per CSV).

## HIGH

- **H-1** §6 conflict resolution not implemented — pure additive sum double-counts when both population-average and subgroup-conditional rows match. Spec §6.3 requires XOR.
- **H-2** Hardcoded log-odds shifts (FRAA +0.55, MTHFR T/T +0.30, etc.) inside engine instead of in prior CSVs. Need explicit STUB warnings.
- **H-3** **Verification-protocol enforcement missing.** Engine should refuse to run on unverified prior tables. Per CLAUDE.md "Verification protocol" + spec §24, this is the structural defense against the 2026-04-30 fabrication incident.
- **H-4** Walsh ranking issue (PHE-0001 wins over PHE-0008 in case_020) — baseline prevalence asymmetry pulls Walsh cases toward PHE-0001. Fix: per-phenotype baseline rows for all 11 + full Walsh marker panel.
- **H-5** Walley IDM credal bands not weighted by `evidence_quality` — every phenotype gets identical band width.
- **H-6** Cancelled-shifts driver suppression — when protective and risk shifts cancel to ~0, both drivers disappear from output.
- **H-7** `subject_sex` and `operating_mode` validated but not used in scoring (§5.3 sex-stratified base rates, X-linked variants, life-stage filters).

## MEDIUM

- **M-1** Dead variable `child_data` at line 272.
- **M-2** Lookup uses `top_intervention_ids_legacy` field instead of canonical `intervention_phenotype_edges.csv`.
- **M-3** Empty/None input handling — type-check before validate_input.
- **M-4** Numeric field tolerance — `float()` raises on whitespace, "N/A".
- **M-5** Timestamp precision; non-canonical comment.
- **M-6** Confidence-label threshold (`abs(total_shift) > 0.7`) has no spec citation.
- **M-7** Hardcoded ATLAS_VERSION should load from manifest.
- **M-8** Output schema deviation from §9.1 — missing `primary_drivers`, `modality_breakdown`, `rationale`, `pathway_burdens`, `cdr_state`, `functional_trajectory`, `responder_predictions`, `avoidance_bundle`, `next_biomarkers_ranked`, `feasible_bundle`, `open_questions`, `rare_syndrome_rule_out_checklist`, `reasoning_trace`, `clinician_handoff_summary`, `model_card_ref`. Forward-compat fix: emit the keys even if empty.
- **M-9** `intervention_bundle` returned as list, spec returns dict keyed by life-stage.
- **M-10** Type hints incomplete; Python ≥3.10 requirement not pinned.

## LOW

- **L-1** Walsh detection no-op `pass` should be a comment.
- **L-2** Calibration anchor INT-0001 ≥80 informational only — should assert at startup.
- **L-3** Atlas Layer 2 isolation confirmed clean.
- **L-4** No network/external API at runtime — confirmed.
- **L-5** Privacy: no PHI logged — confirmed.
- **L-6** Sparse internal-function docstrings.
- **L-7** PEP 8 / formatting nits.
- **L-8** Argparse formatting OK.
- **L-9** Missing CSV silently returns `[]` — should emit `missing_tables` warning.

## Top fixes to apply

1. **C-5** postnatal exposure handling (anchor case integrity)
2. **C-4** iatrogenic substring match tightening (false-positive risk)
3. **H-1** §6 dedup (double-counting fix)
4. **H-3** verification-protocol enforcement (BioMysteryBench defense)
5. **C-2** UTF-8 + newline pinning
6. **C-1** canonical_digest field
