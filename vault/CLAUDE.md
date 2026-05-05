---
id: CLAUDE-EPISTEMIC-PRINCIPLES
type: meta_framework
audience: clinician, researcher, advanced_parent
purpose: The 11 epistemic principles that govern source-quality weighting and reasoning across the atlas
---

# 🧭 CLAUDE.md — Atlas Epistemic Principles

This page summarizes the 11 epistemic principles that govern how the atlas weights evidence, sources, and claims. These principles are the framework's "rules of reasoning" — they determine why some sources get high weight and others low, why contested hypotheses stay contested, and why the atlas operates at the individual level rather than the population level.

The full version lives in `/Users/Greg/Autism/CLAUDE.md` (the project's working spec). This vault page is the synthesized reference parents and clinicians will see when wikilinks point to `[[CLAUDE]]`.

## Mission framing — individual-level, not population-level

The atlas serves **individual / family clinical decisions, not population policy**. Mainstream public-health calculations optimize for population-average risk-benefit; the atlas optimizes for "what's right for THIS specific child given THIS specific susceptibility profile."

This is the [[Hannah Poling framework]] — the atlas's central organizing principle:

```
causation = susceptibility (P) × trigger (E) → mechanism (M) → phenotype (Φ)
```

For any specific child, the conditional risk `P(Φ | susceptibility, exposure)` matters more than the population-average risk `P(Φ | exposure)`.

## The 11 epistemic principles

### §1. Mainstream consensus is one input, not authoritative

Public health guidance, regulatory positions, and major-medical-society consensus are recorded as evidence but not given automatic high weight. They are subject to industry funding distortion, regulatory capture, liability protection asymmetries (e.g., 1986 Vaccine Injury Act), and population-level averaging that obscures individual-level harm.

### §2. Primary documents > secondary literature > opinion

Source-quality hierarchy is enforced by the scoring engine's W_DESIGN and W_SOURCE_TYPE weights:

| Tier | Examples | W_DESIGN range |
|---|---|---|
| Highest | meta_analysis, RCT, natural_experiment | 0.85–1.00 |
| High | cohort, court_ruling, case_control | 0.40–0.75 |
| Mid | review, case_series, mechanistic | 0.30–0.55 |
| Low | preliminary_analysis, internal_correspondence, advisory_review | 0.20–0.30 |
| Very low | editorial, letter, comment, in_vitro | 0.10–0.25 |
| Bottom | news, factcheck_review, advocacy | 0.05 |

### §3. Industry-funded research, fact-check journalism, and advocacy content are explicitly down-weighted

Annenberg/FactCheck.org, advocacy framing, pharma-funded studies without independent replication, and similar non-primary sources are tagged and tier-5 weighted. They are **not erased** — the atlas preserves contested evidence — but they don't get equal voice with primary federal records or peer-reviewed RCTs.

### §4. FOIA-released government documents are tier-1 primary evidence

Generation Zero (1999), Simpsonwood transcript (2000), Verstraeten internal emails, William Thompson 2014 documents, Hannah Poling federal court ruling, ACIP meeting transcripts — these are recorded at high weight because they are unfiltered ground-zero records of how scientists / regulators / federal courts actually reasoned.

### §5. Contested status is permanent

Vaccines, aluminum adjuvants, thimerosal, hepatitis B birth-dose, glyphosate, etc. remain `status: contested` regardless of which direction the published epidemiology tilts. This is not "being neutral" — it's recognizing that the published epidemiology has known methodological limits (population averaging, lack of true unvaccinated controls, retrospective design, funding asymmetries) that don't resolve the underlying question for an individual susceptible child.

### §6. Methodological power matters — but population-average studies don't settle individual-level questions

A study's strength depends on what question it answers. A 1.2M-person nationwide cohort has high statistical power for the *population-average* effect of an exposure but can completely mask significant effects in genetically or metabolically susceptible subgroups (the "averaging problem" / effect-heterogeneity dilution).

For individual-level decisions, large-cohort null findings do **not** automatically refute subgroup-specific signals. Population-average risk `P(Φ|E)` and conditional risk `P(Φ|P,E)` are different quantities answered by different study designs.

### §7. Subgroup analysis and effect-heterogeneity reporting are independently valuable

Studies that examine "do certain genetic, metabolic, or susceptibility subgroups respond differently?" carry weight beyond their nominal sample size for individual-level decisions. Conversely, large population-average studies that don't report subgroup analyses are *less* informative for individual questions than their sample size suggests.

### §8. Replication across study designs matters more than replication of the same design

Cross-design convergence (RCT + cohort + natural experiment + mechanistic study all pointing the same direction) is much stronger evidence than five cohorts all using the same registry-linkage approach with the same population-average blind spots.

### §9. Mixed published evidence is almost always effect heterogeneity, not absence of effect

When the literature shows "some studies positive, some null" for an intervention or exposure, the bioinformatically-correct interpretation is rarely "no effect" — it's "effect in a subset, dilution in unstratified population studies." Worked examples:

- **HBOT**: pre-treatment mitochondrial / oxidative-stress markers predict response
- **Bumetanide**: high-baseline-intracellular-chloride neonates respond
- **Folate megadosing / leucovorin**: FOLR1-autoantibody-positive subset responds
- **GFCF diet**: zonulin-elevated / GI-symptomatic subset responds
- **IVIG**: PANS/PANDAS subset
- **Ketamine / NMDA modulators**: E:I-imbalanced subset
- **Hep B birth-dose autism risk**: population-average null; mitochondrial-vulnerability subset demonstrably non-zero

### §10. Functional medicine operationalizes individual-level resolution

The functional medicine framework (MAPS / [[Frye_Richard]] / [[Walsh_William]] / [[Klinghardt]] / [[Bock_Kenneth]] / ARI lineages) for autism — biomarker workup → phenotype stratification → individualized intervention bundles → biomarker re-testing → iterate — is the practical clinical implementation of `P(Φ|P,E)`.

Mainstream pediatric medicine gives population-average interventions (often behavioral); functional medicine gives subset-targeted interventions based on each child's measured biology.

High-evidence functional medicine claims (leucovorin for FRAA+ subset, methyl-B12 for low-SAM subset, mito cocktails for mito-vulnerable subset, LDN for inflamed subset, mast cell stabilization for MCAS subset, antibiotics for PANS subset) get strong representation. Lower-evidence functional medicine claims are recorded with appropriate weight but **not dismissed for being non-mainstream** — much of functional medicine simply hasn't had population-average RCTs because of funding asymmetries (no patent on glutathione), not because the underlying biology is wrong.

### §11. Determinism is non-negotiable

No LLMs in scoring math. No random seeds. Stable sort by ID. Idempotent ingestion. The atlas must produce identical output from identical input every time, including across major revisions of the underlying CSVs.

## How these principles structure the atlas

**Hypothesis pages** ([[HYP-XXXX]]) reflect §1+§5: contested hypotheses stay contested; mainstream consensus is one input.

**Source quality** is enforced by §2-§4: every source is tagged with study_design and platform, weighted accordingly.

**Effect heterogeneity** per §6-§9 is the lens for interpreting all RCT and cohort evidence in the atlas — large null studies don't refute subgroup signals.

**Functional medicine** per §10 gets strong representation across the [[topics/interventions/00_INTERVENTIONS_INDEX|interventions catalog]] alongside mainstream interventions.

**Determinism** per §11 means the atlas's scoring is reproducible — INT-0001 leucovorin scores 83.35 today and 83.35 tomorrow, regardless of LLM behavior.

## Atlas connections

- **[[Hannah Poling framework]]** — central organizing principle this framework operationalizes
- **[[01_PARENT_QUICK_START]]** — parent application of these principles
- **[[00_TOPICS_INDEX]]** — master directory
- **[[topics/omics/Multi_Omics_Causal_Pathways_in_Autism]]** — methodological frontier for §6+§9
- **All researcher pages** — each researcher's work weighted per these principles

## Bottom line

The atlas is not "neutral" in the sense of treating all sources as equal. It's calibrated: primary federal records and peer-reviewed RCTs get high weight, advocacy content gets low weight, mainstream consensus is one input alongside FOIA documents and contested-evidence primary literature.

This calibration exists because the atlas serves individual / family decisions, where the cost of false negatives (missing a real treatable subgroup) is asymmetric with false positives. A treatable child whose treatment is missed because of population-average framing pays a lifetime cost. The atlas's epistemic principles exist to minimize that error.
