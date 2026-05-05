# UI — Causes Atlas (autism) · research prototype v0.3

Streamlit front-end over the deterministic engine in `personalized_risk.py`.
Research prototype — not for clinical use.

## What it does

- Loads any of the four bundled literature-derived calibration cases
  (mtDNA-heteroplasmy + multi-vaccine challenge [federally adjudicated 2008],
  Frye FRAA-responder, Walsh undermethylator, 22q11.2 deletion) *or* an
  uploaded `input.json` conforming to the §3 schema.
- Runs the engine locally — no network, no telemetry.
- Displays output tier-aware (Researcher / Clinician / Family).
- Surfaces the calibration anchor, the SHA-256 canonical digest, the
  freshness page, and per-row evidence balance (supporting + opposing PMIDs)
  + mainstream consensus position for contested entities.

## Run

```bash
pip install -r ui/requirements.txt
streamlit run ui/app.py
```

The UI imports `personalized_risk.py` from the repo root — no engine
duplication.

## Disclaimers

See the **About / Disclaimer** tab in the app, and the project-wide
`CLAUDE.md`. Bottom line:

- Not FDA-cleared. Not a medical device. Not a substitute for clinical care.
- Many priors are stub log-odds pending priors-CSV calibration in v0.2.
- Walley IDM credal aggregation, within-phenotype responder model, CDR state,
  functional trajectory predictor, and pathway burden are deferred to v0.2.

## Determinism + verification

- No LLMs in scoring math.
- Same input → same output → same `canonical_digest`.
- Every PMID PubMed-verified per the verify-before-write protocol
  (CLAUDE.md §Verification protocol).
- Every contested entity carries both supporting and opposing evidence,
  plus a mainstream consensus position, displayed at equal prominence.
