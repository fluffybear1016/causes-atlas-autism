# Causes Atlas — an Open Source Operating System for Condition Causation

The Causes Atlas (Autism) is the first instantiation of a generalizable operating system for evidence-driven, individual-level causation mapping. The same engine + scoring substrate + verification protocol applies to any complex chronic condition where:

- Effect heterogeneity dominates the literature
- Mainstream consensus underweights subgroup-specific signals
- Functional medicine claims responder phenotypes that mainstream RCTs dilute
- Individual / family clinical decisions need a different objective function from population public health

## What you can fork

The atlas is a **substrate**, not a single condition. Already supported:

| Atlas | Status | Manifest |
|---|---|---|
| Autism (canonical) | v0.4 production | `atlas_manifest.yaml` |
| Long COVID | v0.1 seed | (PIVOT branch) |

Engine accepts `--atlas-path` flag. To bootstrap a new atlas:

```bash
mkdir -p /path/to/your-condition-atlas/v1.0_scored/
# Author CSV files matching the canonical 22-CSV schema
# (see CAUSES_ATLAS_AUTISM_SPEC_v1.2.md §2 for schema)
python3 personalized_risk.py --atlas-path /path/to/your-condition-atlas --input profile.json
```

## What's generalizable across conditions

Every Causes Atlas substrate shares:

1. **Two-layer model**: Layer 1 causal graph (hypotheses, mechanisms, phenotypes, genes) + Layer 2 decision/CSRS (interventions, combinations).
2. **Hannah Poling framework**: causation = susceptibility × trigger → mechanism → phenotype. Conditional risk `P(Φ|P,E)` matters more than population-average for individual decisions.
3. **Source-quality hierarchy**: primary documents > secondary > opinion. FOIA / federal-court records get tier-1 weight regardless of mainstream consensus.
4. **Contested-status preservation**: contested = permanent valid state. Both directions of evidence preserved.
5. **Determinism**: stable sort by ID, no random seeds, no LLMs in scoring math, idempotent ingestion via `node_aliases`.
6. **Verify-before-write protocol**: every PMID verified against PubMed esummary before ingestion.
7. **Δ² research-attention overlay**: tracks trajectory of evidence acceleration alongside truth-strength.
8. **Anti-reflexivity defense**: code-enforced check that ingestion isn't preferentially feeding already-Δ²-positive entities.
9. **Formulation-aware evidence elevation**: negative orthogonal-formulation studies don't cascade across formulations of the same molecule.
10. **Responder-rate calibration cohort**: empirical validation that engine output matches published RCT responder rates.

## What's condition-specific

Each atlas instantiation needs:

- `atlas_manifest.yaml` — versioning + condition metadata
- `phenotypes.csv` — condition-specific phenotype dimensions (autism has 11; another condition may have 5-15)
- `mechanisms.csv` — biological pathways relevant to the condition
- `genes.csv` — relevant genetic risk factors (autism uses SFARI; other conditions use comparable curated lists)
- `interventions.csv` — therapeutic options for the condition
- `intervention_formulations.csv` — formulation-level resolution for key interventions (v0.4 schema)
- `biomarkers.csv` — measurable indicators relevant to the condition
- Edge tables connecting all of the above (`hypothesis_mechanism_edges.csv`, etc.)
- `sources.csv` — PMID-verified primary literature
- `evidence_links.csv` — links between sources and entities
- `baseline_phenotype_prevalence.csv` — population-level prior probabilities

## Suggested next forks (priority order)

1. **Long COVID** — v0.1 seed exists; needs phenotype taxonomy completion + biomarker schema seeding + 100+ PMID ingestion.
2. **ME/CFS** — high overlap with Long COVID; mitochondrial + immunological + dysautonomia phenotypes; existing biomarker literature (Naviaux, Ron Davis lab).
3. **Lyme disease + co-infections** — chronic-disease subset, contested mainstream consensus, strong functional medicine community.
4. **EDS / hypermobility spectrum** — connective-tissue + dysautonomia + MCAS overlap; growing literature.
5. **PANS/PANDAS** — already partial overlap with autism atlas (HYP-0026 placeholder); could spin off as standalone atlas.
6. **PCOS / endometriosis / women's hormonal conditions** — large patient population, mainstream-consensus underserves.
7. **Mood disorders (depression, bipolar) — methylation + nutrient-deficient subsets** — Walsh framework directly transfers.
8. **ADHD** — overlaps autism but distinct phenotype; many functional medicine claims undertested.

## Governance model

The Causes Atlas is open-source under MIT license. Contributors who want to fork for a new condition:

1. Fork the GitHub repo.
2. Create a new branch for your condition (e.g., `long-covid-v0.1`).
3. Author the condition-specific CSVs per the schema spec.
4. Bootstrap with at least 50 PMID-verified primary sources.
5. Run scoring engine; verify a calibration anchor (one well-established intervention should score ≥80).
6. Submit PR or maintain as separate fork with cross-links.

The autism atlas remains the canonical reference for the substrate. New conditions extend the substrate; they don't modify the autism atlas's data.

## Why this matters

The current state of the art for chronic-condition evidence synthesis is:

- Mainstream meta-analyses that average across heterogeneous populations and dilute subgroup signals
- Functional-medicine clinical experience that lacks systematic evidence aggregation
- Individual researchers' literature reviews that don't replicate across labs
- LLM responses trained on the above, propagating both the strengths and the dilution

The Causes Atlas substrate gives any condition community a **deterministic, reproducible, evidence-weighted, individual-level inference layer** that:

- Doesn't dilute subgroup signals
- Preserves contested evidence
- Distinguishes molecule-level from formulation-level evidence
- Is quantitatively validated against published RCT responder rates
- Cites primary sources transparently
- Operates without LLMs in the scoring math (so its outputs don't drift across model updates)

That's the OS thesis.

## Roadmap

- **v0.4 (current)** — autism atlas production; formulation-aware evidence; responder-rate cohort with n=8 entries
- **v0.5** — engine refactor to data-driven driver dispatcher; sleep-axis phenotype; behavioral-severity dimension
- **v1.0** — Zenodo DOI minted; manuscript published; Long COVID atlas at v0.5+
- **v1.5** — autonomous Obsidian pattern-mining engine; daily Δ² recomputation; emergent-edge detection
- **v2.0** — multi-atlas community; 5+ condition atlases active; shared substrate maintenance

## Quick start (for atlas authors)

```bash
git clone https://github.com/[USER]/Autism.git
cd Autism
pip install -r requirements.txt
python3 -m venv venv && source venv/bin/activate

# Run engine on existing autism atlas
python3 personalized_risk.py --input validation/calibration_cases/case_015_frye_fraa_responder/input.json

# Run cohort validation
python3 scripts/compute_responder_mae.py

# Start API server
uvicorn api.main:app --port 8000

# Scaffolding for a new condition atlas
mkdir -p ../my-condition-atlas/v1.0_scored
cp atlas_manifest.yaml ../my-condition-atlas/  # then edit
# author CSVs per CAUSES_ATLAS_AUTISM_SPEC_v1.2.md §2
```

## Citation

> Greg [LAST]. (2026). *Causes Atlas (Autism): Deterministic Evidence-Weighted Inference Engine, v0.4.0*. Zenodo. https://doi.org/10.5281/zenodo.[PENDING]

## License

MIT. See `LICENSE`.

## Contact

GitHub Issues: https://github.com/[USER]/Autism/issues
