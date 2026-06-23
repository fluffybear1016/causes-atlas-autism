---
id: TOPIC-SFARI
type: research_initiative
founder: Jim Simons / Simons Foundation
url: https://www.sfari.org
integration_status: tier_1_backbone
last_updated: 2026-06-23
audience: parent, clinician, researcher
---

# SFARI — Simons Foundation Autism Research Initiative

**SFARI is Jim Simons' decades-long investment in autism research.** The
Causes Atlas integrates SFARI as a tier-1 gene-layer backbone — the
1,277-gene curated database is auto-refreshed quarterly and forms the
canonical genetic-evidence substrate for atlas reports.

## The Simons thesis (and why it matters here)

Jim Simons founded Renaissance Technologies, widely considered the
most successful quantitative hedge fund in history. He then turned the
same systematic-evidence-aggregation discipline toward autism research
through the Simons Foundation, founded 2003. SFARI launched 2005,
funded at ~$78M/year, with $525M+ committed to date.

The atlas builds *on top of* his infrastructure, not in competition with
it. SFARI handles the gene-curation problem at scale; the atlas adds the
individual-level functional-medicine layer SFARI institutionally doesn't
cover.

## What the atlas integrates from SFARI

### Quarterly: SFARI Gene database
1,277 genes graded for autism-association evidence:
- **Tier 1:** High-confidence autism genes — clinical-grade evidence
- **Tier 2:** Strong evidence — multiple replicating studies
- **Tier 3:** Suggestive — emerging evidence
- **Syndromic (S):** Genes whose disruption causes a syndromic disorder
  that includes autism (e.g. [[SHANK3]] → Phelan-McDermid, [[MECP2]] →
  Rett, [[TSC1]]/[[TSC2]] → tuberous sclerosis)

New columns refreshed each quarter:
- Ensembl ID (canonical)
- Chromosome
- Genetic category (multi-valued: rare single-gene; CNV; etc.)
- Syndromic flag (separated from numeric tier)
- **EAGLE score** (new Schaaf 2020 ClinGen-derived metric;
  Limited <7 / Moderate 7–11 / Strong ≥12 / Definitive ≥12+replicated)
- Number of reports (publication-count signal)

Refresh script: `scripts/sfari/integrate_genes.py` — runs quarterly via
the autonomous loop, surfaces deltas, gates on `--apply` for human review.

### Weekly: SFARI-funded publications
~2,288 SFARI-funded papers in the canonical publications database.
Each new paper goes through §24 PubMed verification before landing in
`sources.csv`. Script: `scripts/sfari/integrate_publications.py`.

### Daily: The Transmitter + SFARI News RSS
[[The Transmitter]] (rebranded from Spectrum News, 2024) covers autism
research journalism. Daily ingestion extracts PMIDs from article bodies,
§24-verifies, queues for atlas ingestion. Script: `scripts/sfari/integrate_rss.py`.

### Quarterly: Simons Searchlight community map
68 gene-specific and CNV-specific patient communities (~55 mapped to atlas
genes). For each: NHS active status, approximate community size, partner
foundation (when external). Boosts atlas `confidence_score` for genes
with active community infrastructure. Script: `scripts/sfari/integrate_cohorts.py`.

## Scale at a glance (verified 2026-06-23)

| Resource | Size |
|---|---|
| SFARI Gene database | 1,277 graded genes (Q2 2026) |
| SPARK enrollment | 157,771 autistic + 222,906 family members |
| SPARK WES samples | 106,000+ |
| SPARK WGS samples | 12,000+ |
| Simons Searchlight | 10,166 registered across 184 genes + 24 CNVs |
| SFARI-funded publications | 2,288 |
| SFARI annual research budget | ~$78M |
| SFARI total committed since 2006 | $525M+ |
| Current SFARI investigators | 250+ |

## Where SFARI focuses (and where it doesn't)

SFARI funds aggressively in: rare-variant genetics, polygenic
architecture, structural variation, sex differences, quantitative
behavioral phenotyping, basic circuit mechanism. The 2025 Director Award
is literally called "AutismAtlas" — they are building genetic-atlas
infrastructure adjacent to ours.

SFARI's funding gradient does **not** cover (and the atlas's CLAUDE.md §1
explicitly handles this asymmetry): cerebral folate deficiency,
mitochondrial biomarkers, methylation cycle interventions, microbiome
treatments, contested-hypothesis territories (vaccines, aluminum
adjuvants, hep B birth-dose), functional medicine clinicians like Frye,
Naviaux, Walsh, Adams, Rossignol.

**Critical epistemic principle:** SFARI silence on a topic is NOT a
downweight signal. SFARI's non-coverage of leucovorin / mito cocktails /
MTHFR functional impact reflects institutional priorities and funding
asymmetries — not the underlying biology. The atlas integrates SFARI as
a tier-1 gene-evidence backbone while preserving the [[Hannah Poling framework]]
primacy for individual-level decisions.

## What this means for a family

A child with a SFARI Tier 1 gene variant (e.g. SYNGAP1, SCN2A, STXBP1,
CHD8, ADNP) likely has access to:
1. A specific [[Simons Searchlight]] community
2. An active gene-specific natural-history study
3. A potential Phase 1/2 gene-targeted trial in the pipeline
4. Higher-confidence atlas intervention recommendations

A child with a SFARI Tier 2 gene gets the same atlas weighting boost but
may not yet have an active community. A child with no SFARI-graded
variants still gets the atlas's phenotype-stratified intervention
recommendations — the genetics layer is one input, not the only input.

## Related vault pages

- [[autism_testing_priority_ladder]] — recommended test sequence
- [[SPARK]] — the free WES enrollment program
- [[Simons Searchlight]] — gene-community / natural history overview
- [[The Transmitter]] — SFARI's journalism arm (research news)
- [[Hannah Poling framework]] — atlas's central organizing principle
- [[CLAUDE]] — the 11 epistemic principles
