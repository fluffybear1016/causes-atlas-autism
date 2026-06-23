---
id: TOPIC-SIMONS-SEARCHLIGHT
type: research_program
url: https://www.simonssearchlight.org
last_updated: 2026-06-23
audience: parent, clinician, researcher
---

# Simons Searchlight

Simons Searchlight is the gene-and-CNV-specific research-community arm
of [[SFARI]]. As of mid-2026: 10,166 registered families across 184
specific genes and 24 CNV loci, with 83,408 standardized surveys
completed.

Where [[SPARK]] is enrollment-broad (any autism family), Searchlight is
enrollment-narrow but depth-rich. Each gene or CNV community feeds a
separate natural-history study; the largest also feed Phase 1/2
gene-targeted therapeutic trials (antisense oligos, AAV gene replacement,
selective small molecules).

## Coverage

68 communities total — distributed across SFARI gene tiers and CNV loci.

### Tier 1 single-gene communities

Largest (200+ registered): [[SYNGAP1]], [[SCN2A]], [[STXBP1]],
[[GRIN2B]], [[ADNP]], [[ARID1B]], [[DYRK1A]], [[ANKRD11]], [[SCN8A]].

Medium (50–100): [[CHD8]], [[CHD2]], [[POGZ]], [[FOXP1]], [[SETD5]],
[[MED13L]], [[ASXL3]], [[RAI1]], [[MEF2C]], [[GNAO1]], [[SLC6A1]].

Smaller (<50): [[TBR1]], [[PPP2R5D]], [[KMT2C]], [[KMT5B]], [[WAC]],
[[PHF8]], [[GABRB3]], [[CACNA1C]], [[AUTS2]], plus additional Tier 2
genes ([[NRXN1]], [[NRXN2]], [[NLGN3]], [[NLGN4X]], [[CNTNAP2]],
[[TCF20]], [[TRIO]], [[KDM6B]], [[ZNF292]], [[ANK2]], [[DEAF1]],
[[GRIN2A]], [[HNRNPU]]).

### CNV communities

Original Simons VIP cohort (500+): **16p11.2** deletion/duplication.

Active mid-scale CNV communities: **15q13.3**, **1q21.1**, **3q29**,
**17q12**, **8p23.1**, **2p16.3** ([[NRXN1]] region).

External cross-references: **22q11.2** (22q Society), **7q11.23**
(Williams Syndrome Association), **17q11.2** ([[NF1]] region, Children's
Tumor Foundation), **22q13** (Phelan-McDermid).

### Externally-led gene communities

For some genes the community infrastructure pre-dates Searchlight and is
maintained by a disease-specific foundation. Searchlight cross-references
rather than duplicates:

| Gene | Partner foundation |
|---|---|
| [[FMR1]] | FRAXA + National Fragile X Foundation |
| [[MECP2]] | Rett Syndrome Research Trust + IRSF |
| [[TSC1]] / [[TSC2]] | TS Alliance |
| [[PTEN]] | PTEN Hamartoma Tumor Syndrome Foundation |
| [[NF1]] | Children's Tumor Foundation |
| [[SHANK3]] | Phelan-McDermid Syndrome Foundation |
| [[UBE3A]] | FAST (Foundation for Angelman Syndrome Therapeutics) |
| [[TCF4]] | Pitt Hopkins Research Foundation |
| [[KMT2D]] | Kabuki Syndrome Foundation |
| [[PURA]] | PURA Syndrome Foundation |
| [[FOXP2]] | CASPA (speech/language) |

## How the atlas uses Searchlight data

The cohorts cross-walk (`scripts/sfari/integrate_cohorts.py`) applies a
small confidence-score adjustment to atlas gene entries with active
Searchlight communities. Adjustments:

- **+0.05** for genes with active natural-history study
- **+0.04** for externally-led communities (partner foundation infra
  exists)
- **+0.03** for community without NHS yet

The adjustment is additive, idempotent, and ceilinged at 0.95. Community
infrastructure is corroborating evidence that the clinical phenotype is
sufficiently characterized for individual-level decision support — it
is not foundational evidence.

## Eligibility

Genetic confirmation of a variant in one of the covered genes or CNV
loci. Typical confirmation paths: SPARK results, [[TEST-0009]] whole
exome sequencing, [[TEST-0105]] SFARI gene panel via Invitae.
Participant cost is zero.

## Data access

Individual-level Searchlight data: behind credentialed-researcher access
at SFARI Base (institutional affiliation + IRB required).

Public aggregate statistics: maintained at
`simonssearchlight.org/research/data-statistics/`. The atlas's cohorts
integration script uses these to keep the community mapping current.

## What surfaces in atlas reports

When an uploaded profile (from any genetic-test path) returns a variant
in a Searchlight-covered gene, the atlas report displays:

- Direct link to the community
- Whether an active natural history study is enrolling
- Confidence-score adjustment applied
- Cross-references to atlas hypothesis pages and intervention
  recommendations relevant to the gene's mechanism

For externally-handled genes, the report links to the partner foundation
rather than the Searchlight page.

## Related vault pages

- [[autism_testing_priority_ladder]]
- [[SFARI]]
- [[SPARK]]
- [[TEST-0009]] — clinical-grade WES
- [[TEST-0105]] — Invitae SFARI gene panel
- [[Hannah Poling framework]]
