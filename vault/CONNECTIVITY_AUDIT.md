---
type: audit
title: "Connectivity audit — v2.0_scored"
---

# Connectivity audit

Read-only pass over `v2.0_scored/`. Counts every edge of every type for every entity. Goal: surface where the graph is sparse so we can fill it in before factorial combinations.

## Edge-table summary

| Edge table | Rows | Notes |
|------------|------|-------|
| hypothesis_mechanism_edges | 117 | possible: 2310 |
| intervention_hypothesis_edges | 100 | possible: 7070 |
| intervention_mechanism_edges | 170 | possible: 3333 |
| intervention_gene_edges | 9 | possible: 157964 |
| intervention_phenotype_edges | 148 | **0 rows — completely empty** |
| mechanism_phenotype_edges | 37 | possible: 231 |
| gene_hypothesis_edges | 796 | only 796 for 1564 genes |
| gene_mechanism_edges | 38 | only 38 for 1564 genes |
| gene_phenotype_edges | 13 | only 13 for 1564 genes |
| hypothesis_hypothesis_edges | 33 | possible: 4830 |
| combination_members | 24 | for 5 combinations |
| evidence_links | 1649 | from 1421 fragments |

## Hypotheses (70)

- Min edges: **1**, median: **6**, max: **784**
- Orphans (zero edges of any type): **0**

### Bottom-10 by total edges

| ID | Name | Total | Breakdown |
|----|------|-------|-----------|
| HYP-0014 | [[HYP-0014 Pesticide exposure (organophosphates, glyphosate)]] | 1 | mechanism=0, intervention=1, gene=0, hypothesis_upstream=0, hypothesis_downstream=0, source_citations=0 |
| HYP-0016 | [[HYP-0016 Mold mycotoxin exposure]] | 1 | mechanism=0, intervention=1, gene=0, hypothesis_upstream=0, hypothesis_downstream=0, source_citations=0 |
| HYP-0018 | [[HYP-0018 Maternal diabetes (GDM, T2)]] | 1 | mechanism=1, intervention=0, gene=0, hypothesis_upstream=0, hypothesis_downstream=0, source_citations=0 |
| HYP-0019 | [[HYP-0019 Maternal obesity]] | 1 | mechanism=1, intervention=0, gene=0, hypothesis_upstream=0, hypothesis_downstream=0, source_citations=0 |
| HYP-0020 | [[HYP-0020 Maternal vitamin D deficiency]] | 1 | mechanism=0, intervention=1, gene=0, hypothesis_upstream=0, hypothesis_downstream=0, source_citations=0 |
| HYP-0024 | [[HYP-0024 Maternal SSRI in pregnancy]] | 1 | mechanism=0, intervention=0, gene=0, hypothesis_upstream=0, hypothesis_downstream=0, source_citations=1 |
| HYP-0026 | [[HYP-0026 PANDAS PANS triggers (strep, mycoplasma)]] | 1 | mechanism=0, intervention=1, gene=0, hypothesis_upstream=0, hypothesis_downstream=0, source_citations=0 |
| HYP-0055 | [[HYP-0055 Endocannabinoid system dysregulation]] | 1 | mechanism=0, intervention=0, gene=0, hypothesis_upstream=0, hypothesis_downstream=0, source_citations=1 |
| HYP-0009 | [[HYP-0009 Advanced parental age (especially paternal)]] | 2 | mechanism=0, intervention=0, gene=0, hypothesis_upstream=0, hypothesis_downstream=0, source_citations=2 |
| HYP-0017 | [[HYP-0017 EMF exposure (controversial)]] | 2 | mechanism=1, intervention=1, gene=0, hypothesis_upstream=0, hypothesis_downstream=0, source_citations=0 |

## Mechanisms (33)

- Min edges: **2**, median: **10**, max: **33**
- Orphans (zero edges of any type): **0**

### Bottom-10 by total edges

| ID | Name | Total | Breakdown |
|----|------|-------|-----------|
| MEC-0025 | [[MEC-0025 Bile acid metabolism FXR signaling]] | 2 | hypothesis=1, intervention=0, gene=0, phenotype=1, source_citations=0 |
| MEC-0013 | [[MEC-0013 FOXO transcription factors]] | 4 | hypothesis=0, intervention=4, gene=0, phenotype=0, source_citations=0 |
| MEC-0018 | [[MEC-0018 Endocannabinoid system]] | 4 | hypothesis=1, intervention=1, gene=0, phenotype=0, source_citations=2 |
| MEC-0033 | [[MEC-0033 Photobiomodulation cytochrome c oxidase activation]] | 4 | hypothesis=1, intervention=1, gene=0, phenotype=1, source_citations=1 |
| MEC-0023 | [[MEC-0023 Tryptophan-kynurenine metabolism]] | 5 | hypothesis=3, intervention=0, gene=0, phenotype=1, source_citations=1 |
| MEC-0004 | [[MEC-0004 BBB dysfunction]] | 6 | hypothesis=2, intervention=2, gene=1, phenotype=1, source_citations=0 |
| MEC-0005 | [[MEC-0005 Microglial activation]] | 6 | hypothesis=3, intervention=2, gene=0, phenotype=1, source_citations=0 |
| MEC-0012 | [[MEC-0012 IGF-1 insulin signaling]] | 6 | hypothesis=1, intervention=0, gene=1, phenotype=2, source_citations=2 |
| MEC-0032 | [[MEC-0032 Aluminum adjuvant accumulation TLR-mediated neuroinflammation]] | 6 | hypothesis=4, intervention=0, gene=0, phenotype=0, source_citations=2 |
| MEC-0014 | [[MEC-0014 SIRTUIN NAD+ metabolism]] | 7 | hypothesis=2, intervention=4, gene=0, phenotype=1, source_citations=0 |

## Interventions (99)

- Min edges: **1**, median: **6**, max: **89**
- Orphans (zero edges of any type): **0**

### Bottom-10 by total edges

| ID | Name | Total | Breakdown |
|----|------|-------|-----------|
| INT-0051 | [[INT-0051 HEPA air filtration]] | 1 | hypothesis=1, mechanism=0, gene=0, phenotype=0, combination=0, source_citations=0 |
| INT-0054 | [[INT-0054 Mold remediation]] | 1 | hypothesis=1, mechanism=0, gene=0, phenotype=0, combination=0, source_citations=0 |
| INT-0018 | [[INT-0018 Trimethylglycine (TMG betaine)]] | 2 | hypothesis=0, mechanism=1, gene=0, phenotype=1, combination=0, source_citations=0 |
| INT-0019 | [[INT-0019 S-adenosylmethionine (SAMe)]] | 2 | hypothesis=0, mechanism=1, gene=0, phenotype=1, combination=0, source_citations=0 |
| INT-0021 | [[INT-0021 Lithium orotate (low-dose)]] | 2 | hypothesis=0, mechanism=2, gene=0, phenotype=0, combination=0, source_citations=0 |
| INT-0032 | [[INT-0032 Ashwagandha]] | 2 | hypothesis=0, mechanism=1, gene=0, phenotype=1, combination=0, source_citations=0 |
| INT-0039 | [[INT-0039 Riluzole]] | 2 | hypothesis=0, mechanism=1, gene=0, phenotype=1, combination=0, source_citations=0 |
| INT-0040 | [[INT-0040 D-cycloserine]] | 2 | hypothesis=0, mechanism=1, gene=0, phenotype=1, combination=0, source_citations=0 |
| INT-0043 | [[INT-0043 Low-glutamate diet]] | 2 | hypothesis=0, mechanism=1, gene=0, phenotype=1, combination=0, source_citations=0 |
| INT-0044 | [[INT-0044 Cruciferous vegetable-rich diet]] | 2 | hypothesis=0, mechanism=1, gene=0, phenotype=1, combination=0, source_citations=0 |

## Phenotypes (7)

- Min edges: **18**, median: **29**, max: **41**
- Orphans (zero edges of any type): **0**

### Bottom-10 by total edges

| ID | Name | Total | Breakdown |
|----|------|-------|-----------|
| PHE-0006 | [[PHE-0006 Fragile X (FMR1)]] | 18 | mechanism=4, intervention=13, gene=1, source_citations=0 |
| PHE-0001 | [[PHE-0001 Cerebral folate deficiency phenotype]] | 21 | mechanism=3, intervention=16, gene=2, source_citations=0 |
| PHE-0007 | [[PHE-0007 GABA Cl- imbalance phenotype]] | 28 | mechanism=4, intervention=21, gene=3, source_citations=0 |
| PHE-0005 | [[PHE-0005 mTOR pathway syndromic (TSC, PTEN)]] | 29 | mechanism=6, intervention=19, gene=4, source_citations=0 |
| PHE-0003 | [[PHE-0003 Regressive immune-inflammatory phenotype]] | 32 | mechanism=6, intervention=25, gene=0, source_citations=1 |
| PHE-0004 | [[PHE-0004 Autism + GI microbiome phenotype]] | 33 | mechanism=8, intervention=23, gene=0, source_citations=2 |
| PHE-0002 | [[PHE-0002 Mitochondrial dysfunction phenotype]] | 41 | mechanism=6, intervention=31, gene=3, source_citations=1 |

## Combinations (5)

- Min edges: **3**, median: **3**, max: **12**
- Orphans (zero edges of any type): **0**

### Bottom-10 by total edges

| ID | Name | Total | Breakdown |
|----|------|-------|-----------|
| COM-0001 | [[COM-0001 Leucovorin + Methyl-B12 + Sulforaphane]] | 3 | intervention_member=3 |
| COM-0002 | [[COM-0002 Methylated folate + Choline + Omega-3 (preconception prenatal)]] | 3 | intervention_member=3 |
| COM-0003 | [[COM-0003 GFCF diet + L-glutamine + Probiotics (gut-axis combo)]] | 3 | intervention_member=3 |
| COM-0004 | [[COM-0004 Reverse-osmosis water + Organic produce + Glass storage (environmental remediati]] | 3 | intervention_member=3 |
| COM-0005 | [[COM-0005 Preconception mitochondrial optimization combo (parental)]] | 12 | intervention_member=12 |

## Genes (1564)

- Total genes: **1564**
- Genes with zero edges (orphans): **769**
- Genes with ≤1 edge: **1536**
- Genes with ≥2 edges: **28**
- Median edges per gene: **1.0**
- Max edges any single gene: **8**

### Top 20 most-connected genes

| ID | Symbol | Total edges | hypothesis | mechanism | phenotype | intervention |
|----|--------|-------------|------------|-----------|-----------|--------------|
| GEN-0003 | `SHANK3` | 8 | 3 | 2 | 1 | 1 |
| GEN-0008 | `PTEN` | 6 | 2 | 2 | 1 | 1 |
| GEN-0001 | `FOLR1` | 5 | 1 | 2 | 1 | 1 |
| GEN-0002 | `MTHFR` | 5 | 1 | 1 | 2 | 1 |
| GEN-0004 | `MECP2` | 5 | 1 | 3 | 0 | 1 |
| GEN-0006 | `TSC1` | 5 | 1 | 2 | 1 | 1 |
| GEN-0007 | `TSC2` | 5 | 1 | 2 | 1 | 1 |
| GEN-0005 | `FMR1` | 4 | 1 | 2 | 1 | 0 |
| GEN-0009 | `CHD8` | 4 | 2 | 1 | 0 | 0 |
| GEN-0418 | `GABRB3` | 3 | 1 | 1 | 1 | 0 |
| GEN-0463 | `GRIN2B` | 3 | 1 | 2 | 0 | 0 |
| GEN-0728 | `NLGN3` | 3 | 2 | 1 | 0 | 0 |
| GEN-0729 | `NLGN4X` | 3 | 2 | 1 | 0 | 0 |
| GEN-0743 | `NRXN1` | 3 | 2 | 1 | 0 | 0 |
| GEN-0974 | `SCN2A` | 3 | 2 | 1 | 0 | 0 |
| GEN-0010 | `NRF2 (NFE2L2)` | 2 | 0 | 0 | 1 | 1 |
| GEN-0415 | `GABRA3` | 2 | 0 | 1 | 1 | 0 |
| GEN-0417 | `GABRB2` | 2 | 1 | 1 | 0 | 0 |
| GEN-0461 | `GRIN1` | 2 | 1 | 1 | 0 | 0 |
| GEN-0462 | `GRIN2A` | 2 | 1 | 1 | 0 | 0 |

## Prioritized fix-list (deterministic ranking)

### 1. P0 — completely empty edge table

**`intervention_phenotype_edges` has 0 rows.** No intervention is directly tied to any of the 7 phenotypes. This is the single biggest structural gap. Easiest fix: walk transitively `intervention → hypothesis|mechanism → phenotype` and emit derived edges with `relation_type = derived_via_walk` so the spec's deterministic-only rule isn't violated.

### 2. P1 — gene linkage near-empty

Only 796 gene→hypothesis, 38 gene→mechanism, 13 gene→phenotype edges exist for **1564 genes**. Genes are loaded but largely floating. SFARI/OpenTargets scores are in `genes.csv` but no semantic connection to the rest of the graph. Most genes are effectively decoration right now. Fix: cross-walk SFARI gene → known phenotype categories (Fragile X → PHE-0006, Rett → its phenotype, etc.), plus opentargets_score to seed gene→hypothesis weight.

### 3. P2 — hypothesis→hypothesis sparse

Only 33 cause→cause edges among 70 hypotheses. Many hypotheses sit in isolation when they're known to be upstream/downstream of others (e.g., maternal infection → cytokine storm → neuroinflammation; PFAS exposure → oxidative stress; glyphosate → gut dysbiosis). Fix: pass over hypotheses sharing mechanism IDs and propose upstream/downstream candidates for review.

### 4. P3 — phenotype connection asymmetry

Only 7 phenotypes total. With `intervention_phenotype_edges` empty and `gene_phenotype_edges` at 9 rows, the phenotype layer is essentially a stub. Either expand the phenotype list (the spec implies more granular phenotypes are valuable) or accept it as a small high-level taxonomy and at minimum fully connect every intervention/mechanism that touches each phenotype.

### 5. P4 — combinations under-developed

Only 5 hand-curated combinations. v2.1 explicitly exists to score the 4,851 intervention pairs. Don't run it until P0–P3 are addressed because pair-scoring inherits from edge data — and garbage-in is worse at the combinatorial layer.

## Calibration sanity

INT-0001 Leucovorin: **83.35** (PASS ✅). Spec requires ≥ 80.

