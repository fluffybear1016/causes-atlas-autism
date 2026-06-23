---
id: TOPIC-SPARK
type: research_cohort
sponsor: simons_foundation
url: https://sparkforautism.org
cost: free
last_updated: 2026-06-23
audience: parent, clinician
---

# SPARK — Simons Foundation Powering Autism Research

**SPARK is the largest autism cohort study in the world.** It is free for
any family with an autistic child to enroll, and the value proposition for
the family is concrete: free Whole Exome Sequencing with clinical-grade
variant interpretation returned by a board-certified genetic counselor.

## Why this is the lead test the atlas recommends

- **Free.** WES costs $200–$1,000+ commercially. SPARK eats the cost
  because they want the data for the cohort.
- **Comprehensive.** ~20,000 protein-coding genes sequenced — including
  every [[SFARI]] Tier 1 and Tier 2 autism-associated gene. Catches rare
  and de novo variants where the bulk of monogenic autism signal lives.
- **Clinical-grade.** CLIA-certified lab, ACMG variant classification,
  genetic counselor consult included for any clinically actionable finding.
- **Cohort-scale re-analysis.** When new gene associations are published
  (which happens regularly via [[SFARI]] funded research and
  [[The Transmitter]] coverage), your child's already-sequenced data is
  re-analyzed against the new finding without additional cost or sample.
- **Pipeline to [[Simons Searchlight]].** If your child's variant is in
  one of the 184 Searchlight gene communities or 24 CNV loci, SPARK
  connects you to the natural-history study and clinical-trial pipeline
  for gene-targeted therapies (antisense oligos, AAV gene replacement,
  selective small molecules).
- **Trial matching.** Phase 1/2 gene-targeted trials are increasingly
  using SPARK enrollment as a prerequisite. Enrolling now opens optionality
  later.

## Scale (verified 2026-06-23)

- 157,771 autistic individuals enrolled
- 222,906 family members participating
- 424,819 individuals phenotyped
- 106,000+ Whole Exome Sequencing samples
- 12,000+ Whole Genome Sequencing samples (subset)
- ~173 SPARK-driven publications to date

## What the atlas does with SPARK results

When you upload SPARK WES results to the atlas's intake (UPDATE MY DATA
modal):

1. Every gene with a variant is cross-referenced against the atlas's
   1,564-gene SFARI-backed knowledge graph.
2. Variants in [[SFARI]] Tier 1 or Tier 2 genes trigger weighted phenotype
   matching against the 11 atlas phenotype subtypes.
3. Active [[Simons Searchlight]] community matches are surfaced with direct
   community URLs in the report.
4. Atlas interventions ([[INT-0001]] Leucovorin through INT-0145) are
   ranked by CSRS × phenotype match × gene-cluster overlap.
5. The report flags safety contraindications (e.g. F5 carriers + estrogen
   contraindication, MTHFR + folic acid caution).
6. Generates an Obsidian-compatible markdown profile of your child.

## The honest tradeoff

SPARK is **slow** — 6 to 12 months from sample submission to results.
For a family wanting the atlas's report immediately, the recommendation
is to:

1. **Enroll in SPARK today.** Sample collection happens at home; ship the
   kit. Set it up and move on.
2. **In parallel, order a fast test.** Either:
   - Invitae Autism Spectrum Disorder panel ($250–400, insurance often
     covers) — clinical-grade WES on the ~100 highest-confidence SFARI
     genes, results in 2–4 weeks.
   - Or 23andMe Health ($199, results in 4–6 weeks) for the
     functional-medicine methylation panel (MTHFR, COMT, MAOA, GST)
     while waiting for SPARK.
3. **Order the FRAA test** ([[TEST-0014]]) — $200–400 from Religious
   Sisters of Mercy / Iliad Neurosciences. Independent of any DNA test,
   this is THE biomarker for predicting [[INT-0001]] Leucovorin response.

When SPARK results return, re-upload to the atlas. The report updates.

## Enrollment process

1. Visit `sparkforautism.org`
2. Confirm eligibility (autistic child with professional diagnosis)
3. Complete online registration + electronic consent
4. Receive saliva collection kit by mail
5. Ship sample back
6. Receive results 6–12 months later

## Researcher-side note (for clinicians and FM doctors)

SPARK data is also accessible to credentialed researchers via SFARI Base
(institutional affiliation + IRB required; no solo-researcher path). For
a functional medicine clinician, this means:

- You cannot pull individual SPARK records.
- But you CAN reference SPARK's published summary statistics for your
  patient's gene cluster — most SPARK papers are cited in this atlas's
  `sources.csv` via the [[SFARI integration]].
- The atlas's autonomous SFARI integration pipeline pulls new SPARK
  publications weekly and cross-walks PMIDs.

## Related vault pages

- [[autism_testing_priority_ladder]] — full test ladder
- [[SFARI]] — overview of the Simons Foundation Autism Research Initiative
- [[Simons Searchlight]] — gene-specific communities + natural history
- [[TEST-0009]] — Whole Exome Sequencing (clinical-grade paid path)
- [[TEST-0014]] — FRAA test (the calibration-critical biomarker)
- [[INT-0001]] — Leucovorin (the calibration anchor intervention)
- [[Hannah Poling framework]] — central organizing principle
