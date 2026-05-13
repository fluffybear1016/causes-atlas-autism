# The Substrate Thesis

> One-page positioning document. The single sentence that should appear on slide 1, in the abstract, and in any institutional pitch.

---

## The thesis (verbatim)

**We built an open, deterministic substrate for condition-specific causal inference atlases. Autism is the first fully instantiated atlas. The substrate is condition-agnostic and forkable.**

**Shared infrastructure, condition-specific evidence graphs.**

---

## What this changes

| Old framing | New framing |
|---|---|
| "We built a better autism framework" | "We built an atlas substrate that any condition community can fork, audit, extend, and validate" |
| Autism is the deliverable | Autism is the proof-of-concept; the platform is the infrastructure |
| Funding rationale: extend the autism atlas | Funding rationale: fund the substrate; the same pattern unlocks Long COVID, ME/CFS, Lyme, EDS, PANS/PANDAS, PCOS, ADHD, mood disorders |
| Vendor: us | Vendor: anyone (MIT license; no vendor capture) |
| Audience: autism families | Audience: any chronic-disease community where mainstream meta-analytic methods systematically dilute biologically distinct subgroup signals |

---

## Why federal agencies should care

Three properties make this substrate uniquely suited to federal infrastructure investment:

1. **Reproducibility is structural, not procedural.** The scoring engine produces byte-identical output for byte-identical input. Determinism tests gate every automated pipeline run. Same machine, different machine, different month — same answer. Federal agencies cannot operate on tools that drift.

2. **Provenance is structural, not procedural.** Every atlas claim traces to a PMID-verified primary source. Memory-based citation generation is forbidden by code, not policy. Federal agencies cannot operate on tools that may have hallucinated their evidence.

3. **The substrate is condition-agnostic.** The same engine instantiates against any chronic condition where effect heterogeneity dominates published evidence. Federal investment in the substrate generates returns across the full chronic-disease portfolio, not just one condition.

---

## What's already built (autism instantiation)

```
1,462 PMID-verified primary sources
   95 hypotheses
   34 mechanisms
   11 phenotype dimensions
  137 interventions
   52 formulations
1,564 genes (SFARI Tier 1+2 + atlas additions)
  178 biomarkers

Cohort responder-rate validation:
  n=8 RCTs
  MAE = 0.067 (6.7 percentage points)
  4 sub-3% errors across 3 mechanism axes (oxidative stress, methylation, GABA/Cl⁻);
  5 sub-7% errors across 4 axes when inflammation is included
  — structural replication

Calibration anchor: INT-0001 leucovorin = 83.35 (must remain ≥80)
Engine version: session4_v0.4.0_profile_vector
```

---

## What this enables (substrate-wide)

```
1 substrate
× N condition atlases
= the federal reference architecture for individualized
  causal inference in chronic disease

Already seeded:
   Long COVID atlas (v0.1)

Architecture supports:
   ME/CFS, Lyme disease + co-infections,
   Ehlers-Danlos / hypermobility spectrum,
   PANS/PANDAS, PCOS, ADHD, mood disorders,
   any chronic condition where effect heterogeneity dominates
```

---

## Deck slide 13 (revised)

**Title:** An open substrate for condition-specific causal atlases

**Left:** Architecture diagram

```
VAULT.md
   ↓
deterministic ingestion
   ↓
evidence graph
   ↓
phenotype topology
   ↓
validation pipeline
   ↓
condition-specific atlas
```

**Center:** Atlas examples

```
Autism Atlas       fully instantiated · n=8 RCT validated
Long COVID Atlas   v0.1 seeded
Future forks       community-extensible
```

**Right:** Core sentence

> *The atlas architecture is open-source, deterministic, and condition-agnostic. Any research or patient community can fork the substrate to model heterogeneous chronic conditions using the same evidence topology and validation pipeline.*

**Footer phrase (anywhere on the slide):**

> *Shared infrastructure, condition-specific evidence graphs.*

---

## Internal positioning hierarchy

These three phrases must appear consistently across all artifacts:

1. **Top of stack** (any context):
   *"Open, deterministic substrate for condition-specific causal inference atlases."*

2. **Mid-stack** (HHS-grade institutional language):
   *"Deterministic evidence-ingestion substrate with curator-gated promotion workflows."*

3. **Bottom of stack** (operational language for AI agents):
   *"Read VAULT.md. Run the pipelines. Wake the curator only on the three triggers."*

These are not synonyms. They are three different audiences seeing the same architecture in three different registers.

---

## What we are NOT (clarity for HHS positioning)

- We are not building a clinical decision support tool. The substrate is decision *support*; clinical decisions are for licensed clinicians.
- We are not building a chatbot. The scoring math contains no language-model calls.
- We are not selling a service. MIT license; no vendor lock-in; no vendor capture.
- We are not advocating policy positions. Contested status is preserved; both directions of evidence visible; user decides.
- We are not extending mainstream consensus. We are operationalizing the structural fix to mainstream meta-analytic averaging.

---

## What this requires from federal partners (the asks)

1. **HHS evaluation as federal reference substrate** for condition-specific causal-inference atlases
2. **NIH-supported cohort expansion** of the autism instantiation from n=8 to n=20+ RCTs
3. **HIPAA-compliant clinical-deployment partnership** for individual-patient deployment beyond the published-literature substrate

---

*Author: Greg [LAST]. License: MIT. Citation DOI: pending Zenodo deposit.*

*This document is the master positioning artifact. Update annually or when the framing shifts. Last updated: 2026-05-08.*
