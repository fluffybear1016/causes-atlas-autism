# Session 4 v2.2 Spec — Sub-Agent Audit Punch List

**Audit date:** 2026-04-30
**Auditor:** independent sub-agent
**Spec audited:** `/Users/Greg/Autism/SESSION_4_HANNAH_POLING_SPEC.md` v2.2

## CRITICAL (must fix before Phase 1 implementation)

- **C-1** Determinism vs Walley IDM contradiction (§7.1, §7.3). Sensitivity sweep over s ∈ {1,2,5,10} contradicts byte-identical-output promise. Fix: lock canonical s=2, sweeps are diagnostic-only with separate fixed seeds.
- **C-2** Version-string mismatch — header says v2.2 but `input_version: "2.1"` and `engine_version: "session4_v2.1"` everywhere. Fix: bump all to 2.2.
- **C-3** Phenotype count needs cross-check against live atlas — verify PHE-0001..0011 IDs match `phenotypes.csv`.
- **C-4** Floating-point determinism not specified. Need numpy version pin, stable summation order, no parallel reductions, regression test for byte-identical output.
- **C-5** Conflict resolution math contradictory — subgroup-supersedes rule + additive sum can double-count when multiple subgroup rows match. Fix: deduplication rule, profile disjointness, overlap math.
- **C-6** CSRS scoring engine integration hand-waved. Need explicit utility function combining responder_p, efficacy_credal, CSRS, cost, PGx_risk.
- **C-7** PGx hard-fail vs soft-modifier ambiguity — `dose_reduce_50pct`, `alternative_form_preferred` require dosing/alt-form lookup tables not specified. Fix: drop to STOP_WITH_CLINICIAN flags or add `pgx_action_table.csv`.

## HIGH (substantive scientific or engineering issues)

- **H-1** Sensory-processing phenotype absent (DSM-5 B.4 criterion). Add PHE-0012 sensory-processing phenotype.
- **H-2** Sleep medicine almost completely missing — no melatonin pathway priors, no sleep-disorder intervention rows, no actigraphy input, no circadian-disruption phenotype prior.
- **H-3** Autonomic / vagal dimension under-specified. Expand vagal_tone block, map autonomic biotype to phenotype.
- **H-4** Acetaminophen-in-pregnancy claim overstated. Ahlqvist 2024 (JAMA) sibling-control attenuated association substantially. Fix: contested-status, add countervailing PMID.
- **H-5** SSRI mechanism leap (PHE-0007 GABA/Cl⁻ specific claim). Fix: mark mechanism as "proposed", lower evidence_quality, add Brown 2017 sibling-control + Sujan 2017 to countervailing.
- **H-6** mtDNA tRNA variants need per-variant rows + tissue-specific heteroplasmy thresholds + age-adjusted penetrance.
- **H-7** CDR state classifier not actually specified — list of inputs ≠ decision tree. Fix: specify branches concretely OR downgrade to "experimental" and remove from public output.
- **H-8** Functional trajectory predictor un-specified — credal IQ predictions before Phase 6 data is liability. Restrict to qualitative bands in v1.
- **H-9** Pathway burden 0–10 normalization underspecified — relative to what? Lock reference cohort or absolute log-odds-sum cutoff.
- **H-10** Walsh biotypes evidence base weak — false precision in `+0.85` log-odds. Fix: add evidence_quality field, default lower, widen credal intervals.
- **H-11** Cunningham Panel single-lab proprietary — flag in §17, widen credal intervals.
- **H-12** Microbiome priors structurally unsound — genus-level abundances depend on 16S region + extraction + pipeline. Add lab-method normalization, require sample-method tag.
- **H-13** Adult Mode E menstrual-cycle phase coverage insufficient — Phase 0G seed estimate (~150 rows) too low; female-specific subset alone needs ~50 cycle-phase × biomarker rows.
- **H-14** ACEs scoring conflates exposure types — single ace_score lumps neglect with abuse. Use category flags as primary.
- **H-15** Supplement-PGx missing from Phase 1 seed — methyl-folate × COMT V158M × MTHFR × MTRR × BHMT supplement-PGx rows are exactly what families need.
- **H-16** 30 calibration cases borderline insufficient. Target 60+ for Phase 1, specify minimum coverage per (mode × phenotype) cell.
- **H-17** Calibration-pass criterion ambiguous. Require explicit `expected_top_phenotype`, `expected_top_3_intervention_ids`, `expected_phenotype_p_floor/ceiling` per validation YAML.
- **H-18** External validation benchmarks under-specified. ABCD/SPARK require data-access plans. Specify tier-1 (must-achieve) vs tier-2 (post-release).

## MEDIUM (real issues, batch fix)

- **M-1** Rare-syndrome screening gate gaps — add Kleefstra (EHMT1), KBG (ANKRD11), Coffin-Siris (ARID1B), CDKL5, FOXG1, SETBP1, MEF2C, GRIN2B-related, syndromic ADNP, Cohen syndrome (VPS13B), Mowat-Wilson (ZEB2). Expand to ~40.
- **M-2** Anti-NMDAR encephalitis missing as autism mimic differential. Add to syndromic gate.
- **M-3** Concordance bonus calculation undefined. Specify formula: `bonus = min(0.10, 0.02 × (n_concordant_modalities − 1))`.
- **M-4** Renal/hepatic dosing fallback contradicts "calculator does not prescribe" framing. Output recommendation type only.
- **M-5** VAR-NNNN namespace not in atlas. Decide on separate namespace, document.
- **M-6** Within-phenotype responder predictors hard-coded by example. Need dedicated `responder_predictor_priors.csv` with PMID per shift.
- **M-7** Sibling sex-concordance numerics not populated. Phase 1 seed must populate from Sandin 2014.
- **M-8** Geographic/environmental factors absent — air pollution, water quality, season of conception. Add `environmental_exposure_priors.csv`.
- **M-9** Parental occupational exposures un-prioritized. Controlled vocabulary + prior table.
- **M-10** Drug-supplement interactions absent. Add `supplement_drug_interaction_table.csv`.
- **M-11** Intervention-intervention pairwise antagonism absent. Add pairwise filter step.
- **M-12** Privacy retention path needs k-anonymity ≥5 or drop entirely.
- **M-13** Re-identification risk via case_id + quasi-identifiers + rare variants. Recommend against storing input JSON.
- **M-14** Disability-rights consultation under-specified. Panel of ≥3 autistic self-advocates including non-speaking, intellectually disabled, late-diagnosed.
- **M-15** "Patient" terminology in Mode E — many adult autistic individuals reject. Use "user" or "individual."
- **M-16** No explicit non-binary/intersex pathway beyond input field. Document fallback.
- **M-17** Vaccine-policy framing risk — "AVOID Hep B birth dose" output is clinician-pushback risk. Use STOP_WITH_CLINICIAN always for vaccine outputs.
- **M-18** Calibration-anchor stability rule can't apply at v1.0 release without baseline. Lock at v1.0.
- **M-19** JSON snippets mix Python type hints with JSON Schema. Mark illustrative-only or replace.
- **M-20** Lactation/nursing-infant block missing from `child_data`. Maternal medications transfer through milk.
- **M-21** Geography/climate not in input schema (latitude, climate zone, UV index, time zone). Add residential geography block (anonymized to 100km grid).

## LOW (nits)

- **L-1** §1 architecture diagram order ≠ §7.2 step order
- **L-2** §3.13b "~150 rows" estimate unrealistic; cortisol alone is ~50 cells. Realistic estimate 400+.
- **L-3** §0.7 Walsh "clinician-only" — Walsh Research now has DTC kit
- **L-4** §13.7 sub-agent audit not in §15 phases
- **L-5** "9 negative-control cases" mismatches §13.3 text ("5 + 3")
- **L-6** §20 says sex-stratified base rates resolved (✓) but §17.8 admits unresolved
- **L-7** Snake_case consistency check needed in actual schema
- **L-8** No CSV row count caps; engine perf not analyzed
- **L-9** model_card_ref should be structured object not string
- **L-10** Signed prior tables (Phase 5+) — no hash/signature mechanism specified

## Top-5 critical fixes (block Phase 1)

C-1, C-2, C-4, C-5, C-6.

## Top-5 scientific-accuracy concerns

H-4 (acetaminophen overstatement), H-5 (SSRI mechanism leap), H-6 (mtDNA oversimplification), H-7 (CDR not specified), H-10 (Walsh false precision).
