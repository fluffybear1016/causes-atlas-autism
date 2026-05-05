# Validation Suite — Causes Atlas (Autism)

This directory holds the calibration suite for the Hannah Poling Personalized
Risk Calculator (Session 4, see [SESSION_4_HANNAH_POLING_SPEC.md](../SESSION_4_HANNAH_POLING_SPEC.md)).

## Structure

```
validation/
├── README.md                          (this file)
├── calibration_cases/                 (≥60 cases per spec §13.1, BioMysteryBench-aligned)
│   ├── case_011_hannah_poling/
│   │   ├── input.json                 family multi-omics input
│   │   ├── expected_output.yaml       ground truth + p_floor/ceiling
│   │   ├── validation_notebook.py     executable assertions
│   │   └── case_provenance.md         published source profile + PMID grounding
│   ├── case_001_preconception_double_mthfr/
│   ├── case_009_pans_classic/
│   └── ...
├── negative_controls/                 (≥5 cases with no autism etiology)
└── external_benchmarks/               (Tier 1 published case profiles per §13.6)
```

## BioMysteryBench-aligned standard

Per spec §24.5, every calibration case must ship three artifacts:

1. **input.json** — input per §2 schema
2. **expected_output.yaml** — ground truth with `expected_top_phenotype`,
   `expected_phenotype_p_floor`, `expected_phenotype_p_ceiling`,
   `expected_top_3_intervention_ids`, `expected_recommendation_types`,
   `expected_syndromic_flag`, `expected_cdr_state`, `expected_open_questions_includes`
3. **validation_notebook.py** (or .ipynb) — executable, runs the engine,
   asserts equality with expected_output. Must pass in CI.

A calibration case without all three artifacts is not a calibration case.

## Calibration-pass criterion

Per spec §13.1:

- Top phenotype matches `expected_top_phenotype` exactly
- Posterior point estimate is within [`p_floor`, `p_ceiling`]
- ≥2 of 3 expected interventions appear in top-3 of intervention bundle
- Recommendation types match for tested interventions
- No unexpected `syndromic_flag`

## Adding a new case

1. Create `calibration_cases/case_NN_short_name/` directory
2. Write `case_provenance.md` — what published case profile, PMID-grounded
3. Write `input.json` — multi-omics input (use `null` for unknowns)
4. Write `expected_output.yaml` — expected output, with PMID-grounded rationale
5. Write `validation_notebook.py` — executable assertions
6. Run via: `python validation_notebook.py` — must exit 0
7. Add to CI suite: `python -m validation.run_all`
