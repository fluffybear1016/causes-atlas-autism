# Responder-rate calibration cohort

**Move 2 of the post-mortem fix plan.** Replaces atlas-internal calibration
(INT-0001 leucovorin CSRS = 83.35, which only validates that the atlas's own
weights produce a leucovorin score in the 80s — circular) with
**literature-predictive** calibration: the engine, fed published baseline
profiles from N stratified RCTs, predicts published responder rates within X%
mean absolute error (MAE).

## What this directory contains

- `cohort.yaml` — the cohort manifest. One YAML entry per RCT, each with:
  - PMID (PubMed-verified)
  - Stratification criterion (e.g., "FRAA-positive at serum titer ≥ 1:5")
  - Target atlas dimension (e.g., PHE-0001)
  - n_responder / n_total in the stratum
  - published_responder_rate
  - responder_definition (CGI-I, ABC-I, etc.)
  - representative input profile (synthetic typical patient in the stratum)
  - Expected engine behavior (intervention rank, primary target dimension)
- `representative_inputs/<entry_id>.json` — synthetic input profiles used
  to test that the engine surfaces the right intervention for each
  stratification.
- `compute_responder_mae.py` — runs every entry through the v0.2 engine
  and reports per-RCT abs error + cohort MAE.

## Cohort scope (target ~30 entries by month 3)

Each entry must:
1. Cite a published RCT or stratified observational study with reported
   responder rates.
2. Map the stratification criterion onto an atlas phenotype dimension.
3. Provide a representative-input JSON that, fed through the engine,
   makes the relevant phenotype dimension dominate.
4. Specify the engine's expected behavior (which intervention should
   rank #1).

## Why this matters

This is the credentialing event. Atlas-internal calibration cannot survive
peer review because it doesn't predict anything outside the atlas. Cohort-
level responder-rate calibration is the standard validation methodology for
biomarker-stratified treatment selection (see e.g., the OncoKB and CPIC
literature).

The deliverable is a preprint at *Patterns* / *npj Digital Medicine* / *Cell
Reports Medicine* establishing:

> **The Causes Atlas v0.2 engine, given baseline biomarker profiles
> representative of N=30 published RCT responder strata, predicts published
> responder rates with MAE = X% (95% CI: ...). This validates the
> profile-vector approach against literature ground truth and provides a
> per-stratum reproducibility benchmark.**

## v0 scaffold status

This directory ships with **2 worked entries** (Frye 2018 leucovorin /
FRAA-positive; Lemonnier 2017 bumetanide / unstratified responder rate)
to demonstrate the schema and the validation script. Expansion to ~30
entries is a documented work item for month 3 of the post-mortem-fix plan.

All cohort PMIDs must pass the verify-before-write protocol
(scripts/seed_with_verification.py) before being committed.
