# Long COVID / ME-CFS atlas v0.1 — seed

Second condition on the Causes Atlas multi-atlas substrate.
Per `PLATFORM_PIVOT_v0.1.md`.

## Why Long COVID first (after autism)

Highest condition-prioritization score in the framework: maximum FM-clinician
relevance, maximum mainstream whitespace (no accepted protocol), maximum
mechanistic overlap with the autism atlas (mito, immune, MCAS, microbiome
dimensions all reuse), exploding literature, motivated patient population,
moderate political radioactivity (lower than chronic Lyme).

## What's in v0.1 seed

- `atlas_manifest.yaml` — condition metadata, 9-dimension phenotype taxonomy,
  calibration-anchor candidate (low-dose naltrexone), upstream-atlas links
  to autism for shared mechanisms, freshness query patterns for the daily
  PubMed crawler.
- `phenotypes.csv` — 9 phenotype rows (LC-PHE-0001..0009) following the
  same schema as the autism atlas's `phenotypes.csv`.
- `sources.csv` — 11 PMID-verified primary sources covering mito (1),
  POTS (2), LC-MCAS (2), microclots (3), LDN intervention (3). All PMIDs
  pass PubMed esummary verification per the verify-before-write protocol
  (CLAUDE.md §Verification protocol).

## What's NOT yet in v0.1

- `interventions.csv` — pending ingestion of the LDN, supplements, MCAS
  treatments, mito support, anticoagulation (microclot subset), apheresis,
  and exercise-rehabilitation literature. Target: month 2.
- Edge tables (intervention_phenotype_edges, biomarker_phenotype_edges,
  iatrogenic_exposure_priors, rare_syndrome_screening_gate, baseline_
  phenotype_prevalence). Target: month 2-3.
- Calibration cases. Target: month 3.
- Responder-rate calibration cohort. Target: month 3-4.

## Running the engine against this atlas

```bash
python personalized_risk.py \
  --input <profile.json> \
  --atlas-path atlases/long_covid/v0.1/
```

Note: the engine's hardcoded biomarker shifts are autism-specific
(FRAA→PHE-0001, mtDNA→PHE-0002, Walsh→PHE-0008). For the Long COVID
atlas to drive its own loadings from typed input, the engine needs the
v0.3 refactor that moves biomarker shifts from hardcoded to atlas-driven
via `biomarker_phenotype_edges.csv`. Until then, this atlas is structurally
ready (loaders work, manifest parses) but does not produce condition-
specific loadings on Long COVID profiles. Documented engine limitation,
not an atlas defect.

## Verify-before-write log

All 11 seed PMIDs verified against PubMed esummary on 2026-05-05.
Verification claims (PMID → expected author/year/key term match) are
in the cohort.yaml's `pmid_verified_at` field per row.
