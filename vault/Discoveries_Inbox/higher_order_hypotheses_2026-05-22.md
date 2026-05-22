# Higher-order hypothesis chains — 2026-05-22

Pattern miner #3: walks the atlas graph for 2nd-order chains (intervention→mechanism→phenotype) and flags pairs where the direct edge does NOT yet exist. These are implied causal claims the atlas already supports indirectly.

**Edges walked:** {'hypothesis_mechanism_edges': 123, 'mechanism_phenotype_edges': 37, 'intervention_mechanism_edges': 171, 'intervention_phenotype_edges': 148}

---

## Top 13 implied intervention → phenotype edges (via mechanism)

| # | Intervention | Phenotype | Mechanism path |
| --- | --- | --- | --- |
| 1 | `INT-0021` Lithium orotate (low-dose) | `PHE-0005` mTOR pathway syndromic (TSC, P | MEC-0009 + MEC-0028 |
| 2 | `INT-0021` Lithium orotate (low-dose) | `PHE-0006` Fragile X (FMR1) | MEC-0028 |
| 3 | `INT-0022` Inositol (myo-inositol) | `PHE-0005` mTOR pathway syndromic (TSC, P | MEC-0015 |
| 4 | `INT-0024` Glycine | `PHE-0002` Mitochondrial dysfunction phen | MEC-0001 |
| 5 | `INT-0024` Glycine | `PHE-0007` GABA/Cl- imbalance phenotype | MEC-0020 |
| 6 | `INT-0041` GFCF diet | `PHE-0003` Regressive immune-inflammatory | MEC-0022 |
| 7 | `INT-0049` Sunlight exposure | `PHE-0001` Cerebral folate deficiency phe | MEC-0029 |
| 8 | `INT-0049` Sunlight exposure | `PHE-0003` Regressive immune-inflammatory | MEC-0016 |
| 9 | `INT-0049` Sunlight exposure | `PHE-0007` GABA/Cl- imbalance phenotype | MEC-0029 |
| 10 | `INT-0100` Cod liver oil (fermented preferred) | `PHE-0006` Fragile X (FMR1) | MEC-0031 |
| 11 | `INT-0100` Cod liver oil (fermented preferred) | `PHE-0007` GABA/Cl- imbalance phenotype | MEC-0029 |
| 12 | `INT-0101` L-glutamine (free amino acid) | `PHE-0002` Mitochondrial dysfunction phen | MEC-0001 |
| 13 | `INT-0101` L-glutamine (free amino acid) | `PHE-0003` Regressive immune-inflammatory | MEC-0022 |

## Top 50 implied hypothesis → phenotype edges

Hypotheses with intervention targeting + mechanism path to phenotype.

| # | Hypothesis | Phenotype | Via mech. | Interventions targeting hyp |
| --- | --- | --- | --- | --- |
| 1 | `HYP-0001` | `PHE-0001` Cerebral folate deficienc | 2 | INT-0001 |
| 2 | `HYP-0003` | `PHE-0001` Cerebral folate deficienc | 1 | INT-0008, INT-0096 |
| 3 | `HYP-0005` | `PHE-0004` Autism + GI / microbiome  | 2 | INT-0009 |
| 4 | `HYP-0006` | `PHE-0002` Mitochondrial dysfunction | 5 | INT-0088, INT-0089, INT-0092 |
| 5 | `HYP-0006` | `PHE-0005` mTOR pathway syndromic (T | 1 | INT-0088, INT-0089, INT-0092 |
| 6 | `HYP-0007` | `PHE-0001` Cerebral folate deficienc | 1 | INT-0076, INT-0078, INT-0101 |
| 7 | `HYP-0007` | `PHE-0004` Autism + GI / microbiome  | 6 | INT-0076, INT-0078, INT-0101 |
| 8 | `HYP-0007` | `PHE-0007` GABA/Cl- imbalance phenot | 1 | INT-0076, INT-0078, INT-0101 |
| 9 | `HYP-0011` | `PHE-0003` Regressive immune-inflamm | 1 | INT-0052 |
| 10 | `HYP-0012` | `PHE-0003` Regressive immune-inflamm | 1 | INT-0052 |
| 11 | `HYP-0017` | `PHE-0002` Mitochondrial dysfunction | 1 | INT-0050 |
| 12 | `HYP-0021` | `PHE-0006` Fragile X (FMR1) | 1 | INT-0014, INT-0086, INT-0096 |
| 13 | `HYP-0022` | `PHE-0004` Autism + GI / microbiome  | 3 | INT-0025 |
| 14 | `HYP-0022` | `PHE-0007` GABA/Cl- imbalance phenot | 1 | INT-0025 |
| 15 | `HYP-0023` | `PHE-0004` Autism + GI / microbiome  | 2 | INT-0059 |
| 16 | `HYP-0023` | `PHE-0007` GABA/Cl- imbalance phenot | 1 | INT-0059 |
| 17 | `HYP-0029` | `PHE-0002` Mitochondrial dysfunction | 1 | INT-0036 |
| 18 | `HYP-0029` | `PHE-0005` mTOR pathway syndromic (T | 3 | INT-0036 |
| 19 | `HYP-0030` | `PHE-0002` Mitochondrial dysfunction | 1 | INT-0036 |
| 20 | `HYP-0030` | `PHE-0005` mTOR pathway syndromic (T | 3 | INT-0036 |
| 21 | `HYP-0031` | `PHE-0002` Mitochondrial dysfunction | 3 | INT-0007, INT-0037, INT-0047 |
| 22 | `HYP-0031` | `PHE-0005` mTOR pathway syndromic (T | 1 | INT-0007, INT-0037, INT-0047 |
| 23 | `HYP-0032` | `PHE-0005` mTOR pathway syndromic (T | 2 | INT-0065 |
| 24 | `HYP-0032` | `PHE-0006` Fragile X (FMR1) | 2 | INT-0065 |
| 25 | `HYP-0033` | `PHE-0002` Mitochondrial dysfunction | 2 | INT-0068, INT-0095, INT-0096 |
| 26 | `HYP-0034` | `PHE-0003` Regressive immune-inflamm | 1 | INT-0061, INT-0069 |
| 27 | `HYP-0035` | `PHE-0003` Regressive immune-inflamm | 1 | INT-0066, INT-0070, INT-0096 |
| 28 | `HYP-0036` | `PHE-0003` Regressive immune-inflamm | 2 | INT-0075 |
| 29 | `HYP-0037` | `PHE-0003` Regressive immune-inflamm | 1 | INT-0071, INT-0073, INT-0074 |
| 30 | `HYP-0037` | `PHE-0004` Autism + GI / microbiome  | 1 | INT-0071, INT-0073, INT-0074 |
| 31 | `HYP-0038` | `PHE-0005` mTOR pathway syndromic (T | 1 | INT-0072 |
| 32 | `HYP-0038` | `PHE-0006` Fragile X (FMR1) | 1 | INT-0072 |
| 33 | `HYP-0039` | `PHE-0002` Mitochondrial dysfunction | 1 | INT-0046 |
| 34 | `HYP-0039` | `PHE-0003` Regressive immune-inflamm | 1 | INT-0046 |
| 35 | `HYP-0045` | `PHE-0001` Cerebral folate deficienc | 1 | INT-0013, INT-0087, INT-0096 |
| 36 | `HYP-0045` | `PHE-0003` Regressive immune-inflamm | 1 | INT-0013, INT-0087, INT-0096 |
| 37 | `HYP-0045` | `PHE-0007` GABA/Cl- imbalance phenot | 2 | INT-0013, INT-0087, INT-0096 |
| 38 | `HYP-0046` | `PHE-0001` Cerebral folate deficienc | 1 | INT-0016, INT-0096 |
| 39 | `HYP-0046` | `PHE-0002` Mitochondrial dysfunction | 1 | INT-0016, INT-0096 |
| 40 | `HYP-0047` | `PHE-0007` GABA/Cl- imbalance phenot | 2 | INT-0015 |
| 41 | `HYP-0048` | `PHE-0003` Regressive immune-inflamm | 1 | INT-0066, INT-0070, INT-0096 |
| 42 | `HYP-0049` | `PHE-0002` Mitochondrial dysfunction | 1 | INT-0067 |
| 43 | `HYP-0050` | `PHE-0001` Cerebral folate deficienc | 1 | INT-0030 |
| 44 | `HYP-0056` | `PHE-0004` Autism + GI / microbiome  | 2 | INT-0025, INT-0076, INT-0077 |
| 45 | `HYP-0056` | `PHE-0007` GABA/Cl- imbalance phenot | 1 | INT-0025, INT-0076, INT-0077 |
| 46 | `HYP-0057` | `PHE-0004` Autism + GI / microbiome  | 2 | INT-0076, INT-0084 |
| 47 | `HYP-0058` | `PHE-0003` Regressive immune-inflamm | 1 | INT-0025, INT-0076, INT-0080 |
| 48 | `HYP-0058` | `PHE-0004` Autism + GI / microbiome  | 2 | INT-0025, INT-0076, INT-0080 |
| 49 | `HYP-0059` | `PHE-0003` Regressive immune-inflamm | 2 | INT-0076, INT-0078, INT-0080 |
| 50 | `HYP-0059` | `PHE-0004` Autism + GI / microbiome  | 1 | INT-0076, INT-0078, INT-0080 |

---

## Curator workflow

1. Pick a candidate chain.
2. Read the mechanism path; confirm the chain is biologically valid (not just graph artifact).
3. Add direct intervention_phenotype_edge or hypothesis_phenotype_edge if the chain is real.
4. Re-run scoring; verify INT-0001 calibration anchor.

## Provenance

- Pipeline: `scripts/find_higher_order_hypotheses.py`
- Run timestamp: 2026-05-22T10:20:07.920304Z
