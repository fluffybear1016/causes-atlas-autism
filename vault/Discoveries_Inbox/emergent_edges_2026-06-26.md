# Emergent edges report — 2026-06-26

**Scan window:** last 365 days
**Sources scanned:** 1467
**Fragments scanned:** 1462
**Co-occurrence threshold:** ≥3 distinct sources

Pattern miner #1 of the autonomous discovery pipeline. These are co-mention candidates only — they require human curator review and PMID-verified primary evidence before promotion to atlas. **No edges are auto-promoted.**

---

## Candidate gene → mechanism edges

- _No novel candidate gene-mechanism edges above threshold this scan._

## Candidate gene → phenotype edges

- _No novel candidate gene-phenotype edges above threshold this scan._

---

## Curator workflow

1. Pick a candidate edge from above.
2. Read the sample source(s) and the full evidence fragment.
3. If the co-mention represents a real, mechanism-grounded relationship (not coincidence), add an edge row to the appropriate edge table:
   - Gene × mechanism → `v2.0_scored/gene_mechanism_edges.csv`
   - Gene × phenotype → `v2.0_scored/gene_phenotype_edges.csv`
4. Re-run scoring: `python3 run_scoring_v20.py`
5. Verify INT-0001 calibration anchor still holds.
6. Commit with the source PMID(s) in the commit message.

## Provenance

- Pipeline: `scripts/find_emergent_edges.py`
- Run timestamp: 2026-06-26T10:17:18.329958Z
- Determinism guarantee: byte-identical output for byte-identical inputs.
