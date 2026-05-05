# Phase 0 Sub-Agent Audit Punch List

**Audit date:** 2026-04-30
**Scope:** All 6 Phase 0 CSVs + seed_with_verification.py + Hannah Poling validation case + spec v2.3 §24
**Total findings:** 5 CRITICAL, 11 HIGH, 10 MEDIUM, 10 LOW

## CRITICAL (block Phase 1 implementation)

- **C-1** `iatrogenic_exposure_priors.csv` rows IEP-00003, 00004, 00006, 00007, 00008, 00017 all assign `mechanism_id = MEC-0028` but MEC-0028 is "BDNF / neurotrophin signaling" — not teratogen mechanism. Must remap.
- **C-2** Several iatrogenic rows have empty `mechanism_id` (IEP-00002, 00009, 00010, 00021, 00023). Schema needs explicit nullable allow + `mechanism_status: not_applicable` flag.
- **C-3** PSN table mixes methodology framework rows (zero numerical values) with numerical reference rows. Engine will hit NaN. Add `row_type` enum.
- **C-4** PSN delivers 6 rows vs spec §3.13b ~150 promised. POC label sufficient if engine documents biomarkers-without-coverage warning behavior.
- **C-5** Walsh phenotypes (PHE-0008–0011) propagate as engine output dimensions without evidence-tier tag — `confidence_label: LOW` not visually distinct from credal width. Add `phenotype_evidence_tier` output field.

## HIGH

- **H-1** Hannah Poling input.json embeds T2387C heteroplasmy claim without source PMID — soften.
- **H-2** Calibration-anchor INT-0001 ≥80 score (global) vs DONT_START (per-case) needs spec disambiguation.
- **H-3** Aluminum-adjuvant row missing entirely from iatrogenic table.
- **H-4** 16 "pending" atlas_gene_id refs in genetic_id_aliases — break PGx joins. Add CYP2D6/2C19/COMT/MTRR/BHMT/CBS/APOE/FUT2 to genes.csv or define non-atlas vocabulary.
- **H-5** Rare-syndrome `target_phenotype_routing` mixes PHE-NNNN (TSC/PTEN/FXS/mito) with free-text (`rett_specific`, etc.). Split into 2 cols or unify.
- **H-6** PHE-0001 prevalence has 3 rows with different point estimates (0.75, 0.20, 0.55) — engine ambiguity; add `prevalence_definition` enum.
- **H-7** validation_notebook.py vs spec §24.5 `.ipynb` — cosmetic, sync spec language.
- **H-8** SNRIs missing from iatrogenic table despite spec §3.13c bullet.
- **H-9** Stimulants × CYP2D6, atomoxetine × CYP2D6, risperidone × CYP2D6 missing from PGx despite spec §3.8.
- **H-10** Fluoroquinolone PMID 26955658 (Kaur 2016 J Community Support Oncol) is thin grounding for black-box mito-tox — add Lawrence 1996 or FDA refs.
- **H-11** Sandin 2017 heritability range 0.5-0.95 too wide; narrow to actual CI 0.74-0.87 or add range_basis field.

## MEDIUM

- **M-1** IEP-00015 (GA mito-vulnerable) empty primary_pmids despite non-zero log_odds_shift.
- **M-2** IEP-00023 (Hep B birth dose) empty PMIDs despite non-zero subgroup log_odds_shift — flag as placeholder.
- **M-3** PSN cortisol cutoffs claim Stalder 2016 source but Stalder is methodology-only paper.
- **M-4** RSG-0005 PTEN macrocephaly threshold ambiguous (Z>+2 vs Z>+3).
- **M-5** Several rare-syndrome rows have free-text autism prevalence ("substantial subset") vs numerical.
- **M-6** Reichenberg 2006 paternal age RR 5.75 is high-end single-study; meta-analyses report ~1.3-1.5 per decade.
- **M-7** PGX-0030 framework reference row mixed with numerical rows (same as C-3).
- **M-8** **CRITICAL CLINICAL ISSUE**: Many iatrogenic rows route teratogens (VPA, isotretinoin, thalidomide, misoprostol, lithium) to PHE-0003 (regressive immune-inflammatory) — but these cause CONGENITAL not REGRESSIVE phenotypes. Define new routing or use multi-valued.
- **M-9** Caramaschi 2018 sibling-control paper ARGUES AGAINST smoking-autism but cited as supporting log_odds_shift 0.10. Reduce to ~0.0 or 0.05.
- **M-10** PHE-0008..0011 missing top_intervention_ids_legacy in phenotypes.csv.

## LOW

- **L-1** Date format inconsistency across files (with/without timezone).
- **L-2** Vocabulary normalization between variant_id and common_name in genetic_id_aliases.
- **L-3** IEP-00024 vaginal_seeding has off-enum `iatrogenic_class`.
- **L-4** expected_phenotype_p_floor/ceiling 0.50/0.90 wide latitude.
- **L-5** Several PMID date verifications corner case.
- **L-6** Header field `primary_pmid` (singular) vs `primary_pmids` (plural) inconsistent across tables.
- **L-7** Date format minor issues.
- **L-8** PHE-0004 prevalence 20-85% needs point_estimate_basis field.
- **L-9** SLOS prevalence on high end of reported range.
- **L-10** Verbose facial-feature descriptions in syndrome rows.

## Top fixes to apply now (most critical for engine safety)

1. C-1 MEC-0028 misassignment (engine pollution)
2. M-8 teratogen → PHE-0003 over-routing (clinical mistake)
3. C-3 methodology row contamination (NaN landmines)
4. H-1 Hannah Poling T2387C softening (anchor case integrity)
5. M-9 Caramaschi smoking row direction inversion
