# Contributing to the Causes Atlas

Thank you for your interest. The atlas is open under MIT license and welcomes contributions that strengthen the evidence base, expand condition coverage, or improve the inference engine.

## Hard rules (non-negotiable per spec)

These rules protect the atlas's integrity. PRs that violate them will be rejected.

1. **No LLMs in scoring math.** Determinism is the foundation. Never add `openai.ChatCompletion`, `anthropic.messages.create`, or any equivalent inside `run_scoring_v20.py`, `personalized_risk.py`, `compute_delta_squared.py`, or `compute_formulation_scores.py`.

2. **Verify-before-write protocol.** Every PMID added to the atlas must be verified against PubMed esummary. Use `scripts/seed_with_verification.py` template. Memory-based PMID generation by an LLM agent is forbidden — see `CLAUDE.md` §Verification protocol.

3. **Preserve contested status.** Don't drop "contested" status from any entity based on a single paper either way. Contested = permanent valid state per spec §1.1, §9.1.

4. **Don't edit `v2.0_scored/` CSVs by hand.** Re-run the scoring pipeline. Hand-edits desync the audit trail.

5. **Don't recommend population-level vaccination policy as if it were individual-level optimization.** Different objective function. The atlas is for individual / family decisions per the Hannah Poling framework. See `CLAUDE.md` Mission framing section.

6. **Calibration anchor must hold.** INT-0001 leucovorin atlas signal must score ≥80 across all changes. Any PR that drops it below 80 will be rejected.

## What we welcome

### New evidence (PMID-verified)

Adding a new RCT, mechanistic paper, or primary source:

1. Run `python3 scripts/seed_with_verification.py --pmid <PMID> --claimed-author "<NAME>" --claimed-year <YEAR> --key-term "<TERM>"`.
2. The script verifies against PubMed esummary; refuses to write if mismatch.
3. Edit the appropriate CSV (`sources.csv`, `evidence_links.csv`, etc.).
4. Re-run scoring: `python3 run_scoring_v20.py`.
5. Verify INT-0001 calibration: `grep "^INT-0001," v2.0_scored/interventions.csv` should show csrs_score ≥ 80.
6. Submit PR.

### New formulations (FRM-XXXX rows)

Adding a formulation-level entry to `intervention_formulations.csv`:

1. Identify the parent intervention ID (must exist in `interventions.csv`).
2. Determine `delivery_route` (oral, IV, sublingual, topical, transdermal, intranasal, subcutaneous, intramuscular, inhaled, rectal, etc.).
3. Determine `formulation_evidence_status` (`established_RCT`, `established_mechanistic`, `anecdotal_plus_mechanistic`, `mechanistic_only`, `anecdotal_only`, `untested`, `contested`).
4. Provide PMID-verified citations for any "established" status claims.
5. Set `contested_at_formulation_level: true` ONLY if there's negative evidence specifically for this formulation. Set `contested_at_molecule_level_only: true` if molecule has negative RCTs but formulation has its own evidence story.
6. Re-run `python3 scripts/compute_formulation_scores.py`.
7. Submit PR.

### New atlas instantiations (a different condition)

See `ATLAS_OS_README.md` for the multi-atlas substrate. To add a new condition:

1. Open a tracking issue with proposed condition + rough scope (50+ PMIDs target).
2. Author the condition-specific CSVs per the schema spec.
3. Bootstrap with at least 50 PMID-verified primary sources.
4. Run scoring; identify a calibration anchor (one well-established intervention scoring ≥80).
5. Submit PR or fork with cross-link to the canonical autism atlas.

### Engine improvements

The engine code (`personalized_risk.py`) is the most sensitive part of the atlas. Changes here require:

- All 4 v0.2 calibration cases (case_011, 015, 020, 026) must continue to PASS via `python3 scripts/validate_v02_calibration.py`.
- Cohort responder-rate MAE must not regress (`python3 scripts/compute_responder_mae.py`).
- Determinism test: 3 consecutive runs of the cohort MAE must be byte-identical.
- Sub-agent independent audit confirming no fabricated calibration.
- Engine version bumped per semver.

### Documentation / SEO / GEO improvements

Improvements to `llms.txt`, `JSON_LD_SPEC.md`, `SEO_GEO_PLAN.md`, `ATLAS_OS_README.md`, `CONTRIBUTING.md`, the manuscript outline, etc. are welcome via standard PR.

## What we won't accept

- **Memory-based PMID generation** without verification (see Hard Rule 2).
- **LLM calls in scoring math** (see Hard Rule 1).
- **Mainstream-consensus-only framing** that drops contested status (see Hard Rule 3).
- **Hand-edits to `v2.0_scored/`** (see Hard Rule 4).
- **Population-policy recommendations** as if they were individual-level (see Hard Rule 5).
- **Calibration-breaking changes** without a fix (see Hard Rule 6).
- **Industry-funded marketing material** as primary evidence. The atlas down-weights these per epistemic principle §3.
- **Fact-check journalism / advocacy content** as primary evidence. Down-weighted per epistemic principle §3.

## Code style

- Python: PEP 8 + type hints where reasonable.
- CSVs: stable column order; UTF-8; CRLF or LF line endings.
- Comments: prefer "why" over "what."
- Docstrings: explain the spec section being implemented.

## Workflow

1. Fork → branch → commit → PR.
2. Use `git pull --rebase origin main` before pushing if there's drift.
3. Sub-agent verification runs are encouraged for non-trivial PRs.
4. Reviewers will check: hard rules, calibration anchor, determinism, citation integrity.

## Questions

GitHub Issues: https://github.com/[USER]/Autism/issues

For sensitive matters (e.g., correcting a fabricated PMID), email directly: `473abel@gmail.com`.

## License

By contributing, you agree your contributions are licensed under MIT.
