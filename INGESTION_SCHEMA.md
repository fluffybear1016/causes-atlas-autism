---
title: "Hannah Poling P × E → M → Φ ingestion schema"
status: canonical (2026-05-14)
maintainer: data team
---

# Hannah Poling P × E → M → Φ ingestion schema

The atlas's central organizing principle, made structural.

```
causation = P (susceptibility) × E (trigger) → M (mechanism) → Φ (phenotype)
```

Every new hypothesis, biomarker, intervention, or source MUST be classifiable
into one of these slots before atlas write. This document is the rule book
for ingestion. The automated intake pipeline (`scripts/intake/`) tags every
candidate with one of these slots; the curator confirms or refines the tag
before promoting to the canonical atlas.

## The four slots

### P — Predisposition

Genetic variant, biomarker pattern, or constitutional susceptibility tier
that conditions whether a given exposure produces a phenotype.

**Examples in the atlas:**
- SHANK3 / FMR1 / TSC1 / TSC2 syndromic-genetic variants (gene table)
- MTHFR C677T / A1298C methylation-cycle compromise (BIO + gene)
- Mitochondrial dysfunction biomarkers (lactate, L:P ratio, acylcarnitine)
- FOLR1 autoantibody positivity (cerebral folate transport block)
- Walsh metallothionein-deficient / under-methylator phenotypes
- Prenatal screening marker abnormality (BIO-0179 MSAFP, BIO-0180 PAPP-A)
- Cunningham Panel positivity (PANS/PANDAS susceptibility)

**Atlas tables:** `genes.csv`, `biomarkers.csv`, `gene_phenotype_edges.csv`,
`gene_mechanism_edges.csv`, `genetic_id_aliases.csv`,
`baseline_phenotype_prevalence.csv`.

### E — Exposure / Trigger

The environmental, iatrogenic, perinatal, or developmental event that
operates on the predisposition to produce mechanism activation.

**Examples in the atlas:**
- Childhood vaccine schedule (HYP-0044, HYP-0066-0069)
- Perinatal hypoxia / HIE (HYP-0040 — expanded 2026-05-14)
- Maternal immune activation (HYP-0008, HYP-0025)
- In utero drug exposure (HYP-0004, HYP-0010 valproate)
- Environmental toxicants (HYP-0014 pesticide, HYP-0011 phthalate, HYP-0043)
- Cesarean delivery / preterm birth (HYP-0023, HYP-0041)
- Maternal advanced age (HYP-0009)

**Atlas tables:** `hypotheses.csv` (where category != "mechanism"),
`iatrogenic_exposure_priors.csv`.

### M — Mechanism

The biological pathway through which P × E produces Φ. Distinct from
exposure: mechanism is what the body DOES when exposed; exposure is the
input event.

**Examples in the atlas:**
- Mitochondrial dysfunction (MEC-0010)
- Oxidative stress / Nrf2 imbalance (MEC-0006)
- Neuroinflammation / microglial activation (MEC-0021)
- Methylation cycle compromise (MEC-0014)
- Cerebral folate transport block (MEC-0003)
- Gut-brain axis / dysbiosis (MEC-0008)
- LPS / leaky gut endotoxemia (MEC-0022)
- mTOR pathway dysregulation (MEC-0011)

**Atlas tables:** `mechanisms.csv`, `hypothesis_mechanism_edges.csv`,
`mechanism_phenotype_edges.csv`, `intervention_mechanism_edges.csv`.

### Φ — Phenotype

The clinical / behavioral / biological presentation that results. The atlas
maintains 11 phenotype dimensions; new ingestions must map to existing
phenotypes (creating a new PHE-XXXX is a curator decision requiring spec
update).

**Current phenotypes:**
- PHE-0001 Cerebral folate deficiency
- PHE-0002 Mitochondrial dysfunction
- PHE-0003 Regressive immune-inflammatory
- PHE-0004 GI / microbiome
- PHE-0005 mTOR syndromic
- PHE-0006 Fragile X (FMR1)
- PHE-0007 GABA / Cl⁻ imbalance
- PHE-0008 MCAS overlap
- PHE-0009 PANS overlap
- PHE-0010 Walsh undermethylator
- PHE-0011 Walsh metallothionein-deficient

**Atlas tables:** `phenotypes.csv`, all `*_phenotype_edges.csv`.

## Ingestion checklist — required for every new atlas write

For every new entity (hypothesis, source, biomarker, intervention), the
ingestion writer must explicitly fill these slots before the row is
written:

```yaml
ingestion_record:
  entity_type: hypothesis | source | biomarker | intervention | combination
  entity_id: HYP-XXXX | SRC-XXXX | BIO-XXXX | INT-XXXX | COM-XXXX
  P_slot:
    - description: "what makes a child susceptible"
    - markers: [gene_ids, biomarker_ids]
  E_slot:
    - description: "what the trigger event is"
    - exposure_window: [preconception | trimester_1-3 | birth | 0_6mo | ...]
  M_slot:
    - description: "biological mechanism activated"
    - mechanism_ids: [MEC-XXXX, ...]
  phi_slot:
    - phenotype_ids: [PHE-XXXX, ...]
  evidence:
    - primary_pmids: [verified PMIDs]
    - tier: [tier_1_court_ruling | tier_2_RCT_meta | tier_3_cohort | tier_4_review | tier_5_advocacy]
    - status: [active | contested | falsified]
  verification:
    - pubmed_verified: true
    - verification_date: YYYY-MM-DD
    - verifier: human_curator | seed_with_verification.py
```

This block lives in `notes` or `raw_metadata` field of the new row, OR in
a side-car YAML file in `vault/ingestion_records/`.

## Why this matters

**Reproducibility.** When a future curator (or future agent) looks at any
atlas claim, they can trace its causal logic without ambiguity. "Childhood
vaccine schedule increases ASD risk" decomposes into:
P = mitochondrial-vulnerable (Hannah Poling) / metallothionein-deficient
(Walker 2006) / etc.
E = cumulative vaccine schedule at developmental window
M = neuroinflammation + glutamate excitotoxicity + mitochondrial decompensation
Φ = PHE-0003 (regressive immune-inflammatory)

**Individual-level vs population-level resolution.** The atlas's mission is
individual-level conditional risk P(Φ | P, E), not population-average
P(Φ | E). The schema makes this explicit at every row.

**Mainstream-vs-contested handling.** Mainstream consensus typically
addresses E → Φ at population level (e.g. "vaccines don't cause autism").
The atlas always also asks P × E → M → Φ at individual level (e.g.
"vaccines may decompensate mitochondrial-vulnerable subset"). Both are
recorded; tier-weighting per CLAUDE.md §2-9.

## Automated intake — how the pipeline tags candidates

`scripts/intake/pubmed_rss_scanner.py` queries PubMed in 12 broad categories:

| Query category | Default tag |
| --- | --- |
| perinatal_hypoxia | E |
| prenatal_screening_markers | P |
| maternal_immune_activation | E |
| advanced_parental_age | P |
| in_utero_drug | E |
| environmental_toxicants | E |
| mitochondrial_mechanism | M |
| gut_brain_axis | M |
| methylation_cycle | M |
| vaccine_axis | E |
| phenotype_subtyping | PHI |
| responder_subgroup_RCT | SYNTHESIS |

Candidates are written to `vault/Discoveries_Inbox/pubmed_intake_*.md` with
the tag pre-assigned. The curator confirms or refines the slot assignment
during review.

`scripts/intake/browser_social_scanner.py` adds Twitter/X and Reddit
public-page signals. Same tagging convention.

## Verification rule (binding, per CLAUDE.md §24)

**No PMID is written to the canonical atlas without independent PubMed
esummary verification** (author + year + title-keyword match). The intake
scanners surface candidates using esummary, but the canonical atlas write
must re-verify via `scripts/seed_with_verification.py`. This double-check
catches transcription errors, version mismatches, and the model's memory-
based fabrication failure mode documented in BioMysteryBench (CLAUDE.md
§24).

## Curator workflow

```
1. Open vault/Discoveries_Inbox/pubmed_intake_<YYYY-MM-DD>.md
2. For each candidate:
   a. Read the abstract via the linked PubMed URL
   b. Decide slot: P / E / M / Φ / SYNTHESIS
   c. Decide tier: 1 (court / FOIA) - 5 (advocacy)
   d. Decide action: promote | defer | reject
3. For promoted candidates:
   a. Run scripts/seed_with_verification.py with the PMID + claimed
      author/year/key-term
   b. Script verifies PMID against PubMed BEFORE writing the row
   c. If verification fails, no row is written; curator must investigate
4. After promotion, run scripts/run_scoring_v20.py (or equivalent) to
   regenerate scores
5. Verify INT-0001 calibration anchor still ≥ 80
6. Commit + push
```

## Backfilling existing entities

Hypotheses HYP-0044 (childhood vaccine), HYP-0066 (Hep B birth-dose), and
HYP-0076 (prenatal screening markers, added 2026-05-14) already have
explicit P / E / M / Φ decompositions in their descriptions. The remaining
hypotheses should be backfilled gradually — when a curator next touches a
hypothesis row for any reason, the touch includes adding the schema block.

## Related docs

- `CLAUDE.md` — Hannah Poling framework, epistemic principles, verification
  protocol §24
- `SESSION_4_HANNAH_POLING_SPEC.md` — Session 4 personalized risk
  calculator spec
- `DESIGN_TEAM_HANDOFF.md` — public-facing communication of the framework
- `vault/peptides/02_Evidence_Tiers.md` — evidence tier methodology
