---
type: index
title: "Causes Atlas (Autism) — Vault Index"
---

# Causes Atlas (Autism)

Generated from `v2.0_scored/`. One markdown note per entity (except genes, which live in a single index). All cross-references are `[[wiki-links]]` so the graph view renders the causal DAG natively.

## Counts

- Hypotheses: **75**
- Mechanisms: **34**
- Interventions: **137**
- Combinations: **5**
- Phenotypes: **11**
- Genes: **1564** (see [[INDEX|genes/INDEX]])
- Sources: **1462**
- Evidence fragments: **1462**
- Evidence links: **1747**
- Hypothesis→hypothesis edges: **33**

## Top 10 interventions (by CSRS)

| Rank | ID | Name | CSRS | Prevention | Treatment | Modality |
|------|----|------|------|-----------|-----------|----------|
| 1 | INT-0001 | [[INT-0001 Leucovorin (folinic acid)]] | 83.35 | 81.36 | 82.34 | drug |
| 2 | INT-0008 | [[INT-0008 Methylated folate (5-MTHF) — preconception prenatal]] | 75.90 | 79.66 | 74.64 | supplement |
| 3 | INT-0002 | [[INT-0002 Sulforaphane (broccoli sprout extract)]] | 74.51 | 77.58 | 74.57 | supplement |
| 4 | INT-0025 | [[INT-0025 Probiotics (multi-strain)]] | 72.04 | 76.00 | 71.66 | supplement |
| 5 | INT-0076 | [[INT-0076 Fecal microbiota transplantation (FMT)]] | 69.67 | 64.65 | 71.79 | drug |
| 6 | INT-0013 | [[INT-0013 Vitamin D3]] | 67.74 | 75.10 | 66.60 | supplement |
| 7 | INT-0047 | [[INT-0047 Aerobic exercise (structured)]] | 67.27 | 75.50 | 67.53 | lifestyle |
| 8 | INT-0036 | [[INT-0036 Rapamycin (sirolimus)]] | 67.02 | 65.29 | 68.85 | drug |
| 9 | INT-0015 | [[INT-0015 Magnesium glycinate]] | 64.73 | 72.99 | 63.96 | supplement |
| 10 | INT-0030 | [[INT-0030 Choline (CDP-choline Alpha-GPC)]] | 63.90 | 73.03 | 63.20 | supplement |

## Top 5 combinations (by CSRS)

| Rank | ID | Name | CSRS |
|------|----|------|------|
| 1 | COM-0003 | [[COM-0003 GFCF diet + L-glutamine + Probiotics (gut-axis combo)]] | 55.57 |
| 2 | COM-0002 | [[COM-0002 Methylated folate + Choline + Omega-3 (preconception prenatal)]] | 55.03 |
| 3 | COM-0001 | [[COM-0001 Leucovorin + Methyl-B12 + Sulforaphane]] | 53.96 |
| 4 | COM-0005 | [[COM-0005 Preconception mitochondrial optimization combo (parental)]] | 51.00 |
| 5 | COM-0004 | [[COM-0004 Reverse-osmosis water + Organic produce + Glass storage (environmental remediati]] | 33.37 |

## Contested hypotheses (6)

- [[HYP-0044 Childhood vaccine exposure (contested)]] — confidence 0.7116
- [[HYP-0054 Acetaminophen postnatal use (contested)]] — confidence 0.3201
- [[HYP-0066 Hepatitis B vaccine (neonatal birth-dose)]] — confidence 0.6226
- [[HYP-0067 Aluminum adjuvant cumulative exposure (vaccines)]] — confidence 0.5878
- [[HYP-0068 MMR vaccine specifically (contested)]] — confidence 0.6265
- [[HYP-0069 Thimerosal exposure (contested, largely removed)]] — confidence 0.6542

## Recently scored (top 10 interventions by csrs_last_updated)

| ID | Name | CSRS | Last updated |
|----|------|------|--------------|
| INT-0128 | [[INT-0128 Trehalose (autophagy promoter)]] |  |  |
| INT-0120 | [[INT-0120 MitoQ (mito-targeted CoQ10)]] |  |  |
| INT-0119 | [[INT-0119 PQQ (pyrroloquinoline quinone)]] |  |  |
| INT-0129 | [[INT-0129 Lovastatin (low-dose)]] |  |  |
| INT-0121 | [[INT-0121 NAD+ precursors (NMN NR)]] |  |  |
| INT-0137 | [[INT-0137 Vitamin D high-dose (deficiency-correction)]] |  |  |
| INT-0136 | [[INT-0136 Pregnenolone (low-dose)]] |  |  |
| INT-0135 | [[INT-0135 MOTS-c (mito-derived peptide)]] |  |  |
| INT-0134 | [[INT-0134 Humanin (mito-derived peptide)]] |  |  |
| INT-0133 | [[INT-0133 Antimicrobial peptides (cathelicidin LL-37)]] |  |  |

## Calibration status

Anchor: **INT-0001 Leucovorin** must score ≥ 80.
- Current score: **83.35** (PASS ✅)
- Link: [[INT-0001 Leucovorin (folinic acid)]]

### `calibration.txt`

```
======================================================================
CALIBRATION TEST — INT-0001 (Leucovorin)
Threshold: csrs_score >= 80.0
======================================================================
  csrs_score              = 81.95  [PASS]
  components:
    hypothesis_alignment      = 0.8011
    mechanism_strength        = 0.7086
    phenotype_effect          = 0.0000
    genetic_coherence         = 1.0000
    safety_score              = 0.8755
    replication_score         = 1.0000
    trend_score               = 0.7500
    synergy_bonus             = 0.0000
  HYP-0001 confidence       = 0.8011
  MEC-0003 (methylation)    = 0.8037
  MEC-0004 (BBB)            = 0.8336
======================================================================
```

### `run_summary.json`

```json
{
  "engine_version": "scoring-engine/1.0",
  "config_hash": "035eecd0d49b4d23",
  "run_timestamp": "2026-04-27T22:29:21+00:00",
  "tables_written": [
    "evidence_fragments",
    "hypotheses",
    "mechanisms",
    "interventions",
    "combinations",
    "hypothesis_mechanism_edges",
    "mechanism_phenotype_edges",
    "gene_mechanism_edges",
    "gene_hypothesis_edges",
    "gene_phenotype_edges",
    "intervention_mechanism_edges",
    "intervention_hypothesis_edges",
    "intervention_phenotype_edges",
    "intervention_gene_edges",
    "phenotypes",
    "genes",
    "sources",
    "evidence_links",
    "combination_members",
    "node_aliases",
    "score_history",
    "hypothesis_hypothesis_edges"
  ],
  "calibration_passed": true,
  "calibration_score": 81.94721498982983,
  "n_hypotheses_scored": 70,
  "n_mechanisms_scored": 33,
  "n_interventions_scored": 99,
  "n_combinations_scored": 5
}
```

## Dataview queries

Top interventions by CSRS:

```dataview
TABLE csrs_score, csrs_prevention_score, csrs_treatment_score, modality
FROM "interventions"
WHERE type = "intervention"
SORT csrs_score DESC
LIMIT 25
```

Contested hypotheses:

```dataview
TABLE confidence_score, evidence_count
FROM "hypotheses"
WHERE contested = true
SORT confidence_score DESC
```

Top combinations:

```dataview
TABLE csrs_score, member_intervention_ids
FROM "combinations"
WHERE type = "combination"
SORT csrs_score DESC
```

