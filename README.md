# Causes Atlas

**A reproducible, evidence-weighted knowledge graph of every known and
speculated cause, mechanism, phenotype, gene, intervention, test, and
combination relevant to a medical condition — built for the individual,
not the population average.**

Autism is the proof-of-concept condition. The substrate generalizes.

---

## What this is

Mainstream medicine optimizes for population-average risk and benefit.
The Causes Atlas optimizes for a different question: *what is right for
**this** specific child, given **this** specific susceptibility
profile?*

The organizing principle is the Hannah Poling framework:

> causation = susceptibility (P) × trigger (E) → mechanism (M) → phenotype (Φ)

For any specific person, the conditional risk `P(Φ | P, E)` matters more
than the population-average risk `P(Φ | E)`. A million-person cohort can
have enormous statistical power for the average effect and still be
blind to a real, large effect inside a small susceptible subgroup. The
atlas is built to make that subgroup visible.

It is **not medical advice.** It is an evidence-mapping research
substrate. The patterns it surfaces are real; any action plan belongs
in a conversation with a qualified clinician who knows the full clinical
history.

## What's in this repository

- **`vault/`** — the knowledge graph as an Obsidian vault: ~700 pages
  covering hypotheses, mechanisms, phenotypes, genes, biomarkers,
  interventions, combinations, tests, researchers, and deep-dive topics.
  Open the folder in [Obsidian](https://obsidian.md) and the graph view
  is navigable directly.
- **`v2.0_scored/`** — the canonical scored dataset, 22 normalized CSVs.
- **`scripts/`** — the engines: the scoring pipeline, the paper-ingestion
  pipeline, the Δ² research-trajectory overlay, the vault builder, the
  living-graph builder, and the verification tooling.
- **`living_graph.html`** — a self-contained, browser-rendered view of
  the whole graph. Upload genetics or lab reports and it reads your data
  against the atlas, entirely in your browser.
- **`validation/`** — calibration cases and the responder-rate cohort
  that anchor the methodology.
- **specifications** — `CAUSES_ATLAS_AUTISM_SPEC*.md`,
  `SCORING_ENGINE_SPEC.md`, `MASTER_README.md` (the engineering entry
  point).

## Why it can be trusted

The atlas is a research substrate, so its trustworthiness is structural,
not rhetorical:

- **Reproducible scoring.** No language-model calls in the scoring math,
  no random seeds, stable sort by ID. Identical input produces identical
  output, across major revisions.
- **Verify-before-write.** No citation is written without PubMed
  verification of every PMID. A pre-commit hook blocks unverified
  citations. Memory-based citation generation is forbidden.
- **Contested status is permanent.** Vaccines, aluminum adjuvants,
  glyphosate, and similar entities stay `contested` regardless of which
  way the published epidemiology tilts — because population-average
  studies have known methodological limits that do not resolve the
  individual-level question.
- **Field-outcomes firewall.** Parent-submitted outcome data is
  curator-write, scoring-engine-read-never — it cannot silently drift the
  published calibration.

Three ground-truth numbers, stated exactly:

- Within-driver coverage MAE (n=7): **0.049**
- Sub-3% errors spanning 3 mechanism axes (oxidative stress /
  methylation / GABA-Cl⁻): **4**
- INT-0001 Leucovorin calibration anchor (CSRS): **83.35** — non-drifted
  across every major revision.

## License — free, credited, paid if you monetize

This is a **source-available** project. Free to use, study, modify, and
share for any noncommercial purpose. You must credit the project.
Commercial use requires a separate paid license.

- **Code** — PolyForm Noncommercial License 1.0.0 — see `LICENSE`
- **Science and data** (the vault, CSVs, specs, knowledge graph) —
  Creative Commons Attribution-NonCommercial 4.0 — see `LICENSE-DATA`
- **Commercial use** — see `COMMERCIAL.md`

Free for families, clinicians, researchers, charities, schools, and
public institutions. If you build a business on it, a commercial license
funds further research. That is the deal.

## Disclaimer

The Causes Atlas is for individual and family research and
decision-support inquiry. It is **not medical advice**, not a diagnostic
device, and not a substitute for a licensed clinician. Nothing here
should be acted on without professional medical guidance. The licensors
make no warranty and accept no liability, to the extent the law allows.
