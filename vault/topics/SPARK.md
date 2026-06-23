---
id: TOPIC-SPARK
type: research_cohort
sponsor: simons_foundation
url: https://sparkforautism.org
last_updated: 2026-06-23
audience: parent, clinician, researcher
---

# SPARK

SPARK is the participant cohort of [[SFARI]]. As of mid-2026 it
contains genotype and phenotype data from 157,771 autistic individuals
plus 222,906 family members. Whole exome sequencing has been performed
on 106,000+ samples; whole genome sequencing on 12,000+.

## Structure

SPARK collects:
- Saliva sample for genotyping
- Standardized phenotype questionnaires (developmental history, medical
  history, behavior measures)
- Longitudinal follow-up surveys at family-defined intervals

Participants receive variant interpretation from a board-certified
genetic counselor when a clinically actionable finding is identified
(~10–15% diagnostic yield in autism cohorts of comparable design).

## Eligibility

Any family with a child who has a professional autism diagnosis. The
participant cost is zero; SFARI funds the sequencing, analysis, and
counselor consult from the research budget.

Turnaround from sample submission to results is approximately 6–12 months
— consistent with research-cohort sequencing timelines.

## How the atlas uses SPARK-returned results

When a SPARK report is uploaded to the atlas intake, the variants are
cross-walked against the [[SFARI]] Gene database (refreshed quarterly
via `scripts/sfari/integrate_genes.py`). Variants in SFARI Tier 1 or
Tier 2 genes contribute to phenotype matching across the 11 atlas
phenotype subtypes. Variants in genes with active [[Simons Searchlight]]
communities surface the community URL in the report.

The atlas does not run the sequencing pipeline; SPARK does. The atlas
reads the result.

## How the atlas uses SPARK as a research source

SPARK-driven publications (~173 to date) are cross-walked into
`sources.csv` via `scripts/sfari/integrate_publications.py`. PMIDs are
verified per the §24 PubMed esummary protocol before any source row is
written. SPARK summary statistics are public; participant-level data is
behind credentialed-researcher access at SFARI Base.

## Position in the atlas's test catalog

SPARK is recorded as [[TEST-0134]] in the test catalog with cost field
zeroed and turnaround of 180 days. It is one of multiple paths to whole
exome sequencing data; clinical-grade WES via the [[TEST-0009]] path
returns faster but at consumer or insurance cost. The atlas does not
rank these against each other — both are categorized as comprehensive
gene-level sequencing.

## Related vault pages

- [[autism_testing_priority_ladder]] — tests grouped by what they reveal
- [[SFARI]] — the parent research initiative
- [[Simons Searchlight]] — gene-community natural history program
- [[TEST-0009]] — clinical-grade whole exome sequencing
- [[TEST-0014]] — FRAA test (the calibration-critical biomarker)
- [[INT-0001]] — Leucovorin (calibration anchor intervention)
- [[Hannah Poling framework]] — central organizing principle
