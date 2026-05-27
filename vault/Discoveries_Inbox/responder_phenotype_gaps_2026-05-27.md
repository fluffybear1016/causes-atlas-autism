# Responder phenotype gaps — 2026-05-27

Pattern miner #4: surfaces interventions with mixed published evidence that have **not yet** been tagged with a responder-phenotype profile. Per `CLAUDE.md` §9: mixed evidence is almost always effect heterogeneity, not absence of effect.

**Total interventions:** 140
**Mixed-evidence interventions:** 1
**Interventions with formulation-level responder notes:** 19
**Gap candidates:** 1

---

## Top 1 responder-phenotype gap candidates

| # | ID | Name | CSRS | Status | Priority |
| --- | --- | --- | --- | --- | --- |
| 1 | `INT-0129` | Lovastatin (low-dose) | 0.0 | contested | **low** |

---

## Curator workflow

For each candidate above:

1. **Investigate study heterogeneity.** Read 2-3 of the strongest negative trials + 2-3 of the strongest positive trials. Look for:
   - Different patient populations (age, sex, baseline biomarkers, phenotype)
   - Different formulations / doses / durations
   - Different outcome measures
   - Different inclusion/exclusion criteria

2. **Extract responder profile.** Write the responder phenotype as concretely as possible:
   - 'High pre-treatment FRAA + AND age >5 with severe verbal communication delay'
   - 'Walsh undermethylator (low histamine + low SAM/SAH) AND no MTHFR T/T'
   - 'GI-symptom-positive + microbiome dysbiosis + age >2'

3. **Update atlas.** Either:
   - Add a formulation row (`intervention_formulations.csv`) with `responder_population_notes`, OR
   - Add an `intervention_phenotype_edge` linking to the responder phenotype dimension, OR
   - Update `intervention.notes` with the responder profile.

4. **Submit PMID-verified citations** for the responder-stratification claim.

## Provenance

- Pipeline: `scripts/find_responder_phenotype_gaps.py`
- Run timestamp: 2026-05-27T10:51:55.408632Z
