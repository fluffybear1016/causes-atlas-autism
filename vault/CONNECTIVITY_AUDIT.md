---
type: audit
title: "Connectivity audit — v2.0_scored"
refreshed: 2026-05-09 (post-rebuild)
---

# Connectivity audit

Read-only pass over `v2.0_scored/`. Counts every edge of every type for every entity. Goal: surface where the graph is sparse so we can fill it before factorial combinations.

**Refreshed 2026-05-09** after engine v0.4 + formulations layer + combinations expansion + peptide vault build.

## Entity counts (current truth)

| Entity table | Rows | vs prior audit |
| --- | --- | --- |
| interventions | **140** | +3 net (added INT-0140 L-carnosine, INT-0141 Aripiprazole, INT-0142 Adams multinutrient, INT-0143 IVIG, INT-0145 L-theanine; removed duplicate INT-0105 Quercetin → canonical INT-0029, INT-0118 NAC → canonical INT-0004, INT-0144 Cromolyn → canonical INT-0103) |
| hypotheses | 75 | refreshed |
| mechanisms | 34 | unchanged |
| phenotypes | 11 | unchanged |
| genes | 1,564 | unchanged (SFARI Tier 1+2 + atlas additions) |
| biomarkers | 178 | unchanged |
| sources | 1,462 | unchanged |
| combinations | **25** | unchanged from prior audit (5 → 25 expansion); member-list integrity now repaired across 11 combinations |
| intervention_formulations | 52 | 4 parent-link fixes applied (FRM-0044, FRM-0045 cromolyn → INT-0103; FRM-0050, FRM-0051 Mg threonate/oxide → INT-0015) |
| combination_members | **81** | was 70; integrity sweep added 15 component links, removed 4 mis-wired refs |

## Edge-table summary (current truth)

| Edge table | Rows | Density assessment | Notes |
| --- | --- | --- | --- |
| hypothesis_mechanism_edges | 123 | moderate | possible: 95×34 = 3,230. ~3.8% density. |
| intervention_hypothesis_edges | 100 | moderate | possible: 137×95 = 13,015. ~0.77%. Could be denser. |
| intervention_mechanism_edges | 171 | moderate | possible: 137×34 = 4,658. ~3.7%. |
| intervention_gene_edges | **9** | **thin** | Critically thin. Most genetic-stratification logic depends on this. **Next-fill priority #1.** |
| intervention_phenotype_edges | 148 | moderate | Was "completely empty" in prior audit — fixed by post-scoring MPE derivation. Now correctly populated. |
| mechanism_phenotype_edges | 37 | thin | possible: 34×11 = 374 (9.9%). Weights populated 0.31-0.79. **Next-fill priority #2.** |
| gene_hypothesis_edges | 1,569 | dense | 100%+ of genes mapped. SFARI Tier 1+2 + curated. |
| gene_mechanism_edges | 38 | **thin** | only 38 for 1,564 genes. **Next-fill priority #3.** |
| gene_phenotype_edges | 13 | **thin** | only 13 for 1,564 genes. Most genetic-phenotype claims live in gene_hypothesis_edges; explicit phenotype mapping is thin. |
| hypothesis_hypothesis_edges | 33 | thin | possible: 95² = 9,025. ~0.37%. Cross-hypothesis claims sparse. |
| combination_members | **70** | improved | was 24. Now reflects 25 combinations with avg 2.8 members each. |
| evidence_links | 1,747 | dense | from 1,462 fragments — most are PMID-grounded. |

## Holes ranked by leverage

**Critical (next-fill priority #1-3):**

1. **intervention_gene_edges (9 rows)** — connects interventions to genetic markers. Currently the engine cannot say "this child has SHANK3 → consider IGF-1" via the canonical edge graph. Examples needing wiring:
   - IGF-1 (INT-0132) → SHANK3, MECP2, ADNP
   - Leucovorin (INT-0001) → MTHFR, FOLR1
   - Methyl-B12 (INT-0003) → MTRR, MTR
   - Rapamycin (INT-0036) → TSC1, TSC2, PTEN, NF1
   - Bumetanide (INT-0023) → SLC12A2 (NKCC1)

2. **mechanism_phenotype_edges (37 rows)** — routing layer between mechanism modules and phenotype dimensions. Higher density improves intervention → mechanism → phenotype chain walks. Weights derived but row count expansion is the next step.

3. **gene_mechanism_edges (38 rows)** — connects genes to biological mechanisms. Critical for syndromic-autism stratification (FMR1 → mTOR, SHANK3 → IGF-1 signaling, TSC1/2 → mTOR, etc.). 1,564 genes / 38 edges = essentially unused layer.

**Moderate (improvement-worthy but not blocking):**

4. **gene_phenotype_edges (13 rows)** — top-50 SFARI Tier 1 genes × their primary phenotype dimension would close this.
5. **hypothesis_hypothesis_edges (33 rows)** — cross-hypothesis contradiction + convergence claims. Densifying surfaces the contested-evidence dual-color edges in the atlas explorer.

**Healthy:**

- intervention_hypothesis, intervention_mechanism, hypothesis_mechanism, evidence_links: all at reasonable density given the atlas stage.

## Fix priority for next session

Recommended order, with target end-state row counts:

1. **intervention_gene_edges**: 9 → 50+ rows. Wire genetic-responder-population interventions.
2. **gene_mechanism_edges**: 38 → 200+ rows. Top-50 SFARI Tier 1 × primary mechanism.
3. **gene_phenotype_edges**: 13 → 100+ rows. Top-50 SFARI Tier 1 × primary phenotype dimension.

Combined: pushes syndromic-genetic-stratification capability from "thin to barely-functional" → "first-class layer." Matters for HHS-deck claim that the substrate handles individual-level conditional risk.

## Other observations

- **Discoveries_Inbox** active. Daily-pipeline cron writes here. Latest run: 2026-05-07. Surfaces 139 candidate findings across 4 finder scripts.
- **Peptides section** new (2026-05-09). 25 peptide pages + MOC + lifecycle matrix + safety synthesis + evidence-tier methodology. Vault-only scaffold; promotion to canonical atlas via verify-before-write.
- **Formulations layer** (`v2.0_scored/intervention_formulations.csv`) live with 52 FRM-XXXX rows. Orthogonal-formulation negative evidence does not cascade down.
- **20 new combinations** (COM-0006 through COM-0025) appended via `scripts/expand_combinations.py`. Calibration anchor INT-0001 = 83.35 preserved.

## Methodology note

This audit surfaces structural holes that gate downstream functionality (engine inference, calibration, manuscript claims). It is not a complete graph density analysis. A more rigorous analysis would include per-entity edge degree distribution, connected-component analysis, and edge-evidence-tier distribution. Reserved for future audits.

---

*Refreshed via direct file count + manual review. Pre-MPE-derivation versions of this page asserted "intervention_phenotype_edges: 148 rows, 0 rows completely empty" — that contradiction was a stale-text artifact + correct row count; fixed in this version.*
