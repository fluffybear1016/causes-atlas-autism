---
id: TOPIC-SFARI
type: research_initiative
url: https://www.sfari.org
integration_status: tier_1_backbone
last_updated: 2026-06-23
audience: parent, clinician, researcher
---

# SFARI — Simons Foundation Autism Research Initiative

SFARI is a research initiative founded 2005 under the Simons Foundation,
funded at approximately $78M/year, with $525M+ committed since inception.
The atlas integrates SFARI as a tier-1 gene-evidence backbone. This page
documents the integration, scope, and the epistemic constraints that
apply.

## SFARI Gene database

A curated database of 1,277 genes graded for autism-association
evidence (verified Q2 2026):

| Tier | Meaning |
|---|---|
| 1 | High-confidence — multiple independent lines of evidence |
| 2 | Strong — well-replicated |
| 3 | Suggestive — emerging evidence |
| S (Syndromic) | Disruption causes a syndromic disorder that includes autism (e.g. [[SHANK3]] → Phelan-McDermid, [[MECP2]] → Rett, [[TSC1]]/[[TSC2]] → tuberous sclerosis) |

The Q2 2026 release introduced the EAGLE scoring system — a Schaaf 2020
ClinGen-derived metric with thresholds Limited <7, Moderate 7–11, Strong
≥12, Definitive ≥12+replicated. Captured in the atlas as an orthogonal
evidence axis.

Refresh cadence: quarterly. Script: `scripts/sfari/integrate_genes.py`.

## SFARI-funded publications

A canonical database of approximately 2,288 papers funded by SFARI
grants. The atlas's autonomous loop scrapes the index weekly, extracts
PMIDs, verifies each via PubMed esummary (per §24), and queues for
ingestion into `sources.csv`. Script:
`scripts/sfari/integrate_publications.py`.

## The Transmitter

[[The Transmitter]] (rebranded from Spectrum News, 2024) is SFARI's
science journalism arm. The atlas pulls the sitewide RSS feed daily,
filters for the `/spectrum/` autism vertical, and extracts PMIDs from
article bodies for verification + ingestion. Script:
`scripts/sfari/integrate_rss.py`.

## SFARI participant cohorts

| Cohort | Scope |
|---|---|
| [[SPARK]] | 157,771 autistic individuals + family; broadest enrollment |
| Simons Simplex Collection (SSC) | Smaller, deeply phenotyped families; dbGaP companion phs000298 |
| [[Simons Searchlight]] | 10,166 registered across 184 specific genes + 24 CNV loci; gene-specific natural-history program |

Participant-level data sits behind credentialed-researcher access at
SFARI Base. Public summary statistics and the publication corpus are
fully ingestable.

## Epistemic constraint: SFARI silence is not a downweight signal

SFARI funds genetics, circuits, and basic mechanism aggressively. Per
the funded-investigator audit (`outputs/sfari_publications_map.md`),
functional-medicine researchers central to the atlas — Frye, Naviaux,
Adams, Rossignol, Walsh — are absent from SFARI's investigator list.
SFARI does not fund work on cerebral folate deficiency, mitochondrial
biomarkers, methylation cycle interventions, microbiome treatments, or
contested hypotheses (vaccines, aluminum adjuvants, hep B birth-dose).

Per CLAUDE.md §1 (mainstream consensus is one input, not authoritative)
and §2 (primary documents > secondary literature): SFARI-funded papers
are weighted tier-1 for their stated topics (rare-variant genetics,
polygenic architecture, structural variation, sex differences,
quantitative behavioral phenotyping). SFARI silence on a topic — vaccine
safety in mitochondrially-vulnerable subsets, leucovorin response in
FOLR1-AA-positive children, mast cell activation, glutathione status —
does NOT downweight that topic. Funding asymmetries are not evidence.

The atlas integrates SFARI as a tier-1 gene layer while preserving the
[[Hannah Poling framework]] as the central organizing principle for
individual-level decisions.

## SFARI's stated research priorities (Δ² trajectory signals)

Per the funded-RFA audit (Q2 2026):
1. Quantitative behavioral and circuit phenotyping that survives
   heterogeneity
2. Polygenic and structural genetic architecture with AI-integrated
   multi-modal analysis (the 2025 SFARI Director Award is titled
   "AutismAtlas")
3. Sex-differences biology and rare-NDD gene-first deep phenotyping

These are forward indicators for where SFARI-funded evidence will
accelerate. The atlas's Δ² engine treats RFA-aligned topics as
trajectory-positive even before the publications land.

## Integration scripts

| Script | Cadence | What it does |
|---|---|---|
| `scripts/sfari/integrate_genes.py` | quarterly | Refreshes SFARI Gene database; delta detection; Discoveries_Inbox stubs for new genes |
| `scripts/sfari/integrate_publications.py` | weekly | Scrapes funded-publications index; verifies PMIDs; queues for ingestion |
| `scripts/sfari/integrate_rss.py` | daily | Pulls Transmitter + SFARI feeds; extracts PMIDs; verifies; queues |
| `scripts/sfari/integrate_cohorts.py` | quarterly | Cross-walks [[Simons Searchlight]] community list to gene confidence weighting |
| `scripts/sfari/run_all.py` | daily entry point | Cadence-aware orchestrator invoked by `autonomous_loop.py` |

## License and attribution

SFARI declares underlying data public-domain with attribution requested
for the curation layer. Compatible with the atlas's PolyForm-NC + CC-BY-NC
licensing. Attribution string: `"SFARI Gene © Simons Foundation Autism
Research Initiative. Source data public-domain; curation attributed."`

## Related vault pages

- [[autism_testing_priority_ladder]]
- [[SPARK]]
- [[Simons Searchlight]]
- [[The Transmitter]]
- [[Hannah Poling framework]]
- [[CLAUDE]]
