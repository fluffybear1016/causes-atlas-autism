---
id: TOPIC-SIMONS-SEARCHLIGHT
type: research_program
sponsor: simons_foundation
url: https://www.simonssearchlight.org
last_updated: 2026-06-23
audience: parent, clinician, researcher
---

# Simons Searchlight — gene-specific natural history communities

Simons Searchlight is the gene-and-CNV-specific research-community arm of
[[SFARI]]. Whereas [[SPARK]] is enrollment-broad (any autism family),
Searchlight is enrollment-narrow but depth-rich: ~10,166 families across
184 specific genes and 24 CNV loci, with 83,408 standardized surveys
completed and ongoing natural-history studies in flight for the largest
communities.

## What Searchlight does for a family

If your child has a confirmed variant in one of the 184 Searchlight
genes or 24 CNV loci, the program offers:

- **Gene-specific community connection** — other families with the same
  variant; pediatric specialists experienced with the gene
- **Standardized natural history survey participation** — semi-annual
  questionnaires that feed clinical-trial-ready evidence
- **Disease-modifying trial pipeline access** — when a gene-targeted
  therapy enters trials (antisense oligo, AAV gene replacement, selective
  small molecule), Searchlight participation is often the recruitment path
- **Free deep phenotyping data sharing** — research-grade developmental,
  behavioral, and medical phenotype data flows back to participating
  clinicians

## The communities (verified 2026-06-23)

### Largest Tier 1 communities (200+ registered)

- [[SYNGAP1]] — synaptic Ras-GTPase; ID + epilepsy + ASD
- [[SCN2A]] — voltage-gated sodium channel; epilepsy + ASD spectrum
- [[STXBP1]] — synaptic vesicle release; epileptic encephalopathy
- [[GRIN2B]] — NMDA receptor subunit; ID + ASD
- [[ADNP]] — chromatin remodeling; Helsmoortel-Van Der Aa syndrome
- [[ARID1B]] — chromatin remodeling; Coffin-Siris syndrome
- [[DYRK1A]] — kinase; ID + microcephaly + ASD
- [[ANKRD11]] — KBG syndrome
- [[SCN8A]] — voltage-gated sodium channel; EIEE13

### Medium Tier 1 communities (50–100)

- [[CHD8]] — chromatin helicase; ASD + macrocephaly
- [[CHD2]] — myoclonic-atonic epilepsy
- [[POGZ]] — White-Sutton syndrome
- [[FOXP1]] — speech + ID + ASD
- [[SETD5]] — chromatin; ID + ASD
- [[MED13L]] — Mediator complex; ID + ASD
- [[ASXL3]] — Bainbridge-Ropers syndrome
- [[RAI1]] — Smith-Magenis syndrome
- [[MEF2C]] — neuronal differentiation
- [[GNAO1]] — G-protein subunit; movement disorder + ID
- [[SLC6A1]] — GABA transporter; epilepsy + ID + ASD

### CNV loci communities

- **16p11.2 deletion/duplication** — the original Simons VIP cohort,
  largest CNV community (500+)
- **22q11.2 deletion** — also handled by 22q Society
- **15q13.3 microdeletion** — epilepsy + ID
- **1q21.1 dup/del** — microcephaly/macrocephaly
- **3q29 deletion** — ID + psychosis risk
- **17q12 deletion** — renal cysts + diabetes + ASD
- **8p23.1 dup/del**
- **2p16.3 deletion** — [[NRXN1]] region
- **7q11.23 duplication** — Williams region inverse
- **17q11.2** — [[NF1]] region

### Externally-led communities (Searchlight cross-references)

For some genes Searchlight defers to disease-specific patient
organizations that pre-date Searchlight:

| Gene | Foundation |
|---|---|
| [[FMR1]] | FRAXA + National Fragile X Foundation |
| [[MECP2]] | Rett Syndrome Research Trust + IRSF |
| [[TSC1]] / [[TSC2]] | TS Alliance |
| [[PTEN]] | PTEN Hamartoma Tumor Syndrome Foundation |
| [[NF1]] | Children's Tumor Foundation |
| [[SHANK3]] | Phelan-McDermid Syndrome Foundation |
| [[UBE3A]] | FAST (Foundation for Angelman Syndrome Therapeutics) |
| [[TCF4]] | Pitt Hopkins Research Foundation |
| [[KMT2D]] | Kabuki Syndrome Foundation |
| [[PURA]] | PURA Syndrome Foundation |
| [[FOXP2]] | CASPA (speech/language) |

## How the atlas uses Searchlight data

The cohorts integration script
(`scripts/sfari/integrate_cohorts.py`) applies a `confidence_score` boost
to atlas gene entries with active Searchlight communities:

- **+0.05** for a gene with active natural history study (NHS)
- **+0.03** for community without NHS yet
- **+0.04** for genes with external partner-foundation communities

The boost is capped (additive, idempotent, ceilinged at 0.95). The
reasoning: community infrastructure is a real-world signal that the
gene's clinical phenotype is sufficiently characterized for individual-
family decision support. It is corroborating evidence, not foundational.

## Eligibility and enrollment

- Any family with a child with a confirmed disease-causing variant in
  one of the 184 covered genes or 24 CNV loci
- Genetic confirmation required — typically returned from [[SPARK]],
  [[TEST-0009]] WES, or [[TEST-0105]] SFARI gene panel
- Enrollment is online at `simonssearchlight.org`
- Currently US-focused with growing international participation

## Data access for researchers

Like [[SPARK]], Searchlight individual-level data is behind a
credentialed-researcher gate at SFARI Base (institutional affiliation +
IRB required). Public aggregate statistics are available at
`simonssearchlight.org/research/data-statistics/` — the cohorts
integration script uses these to maintain the community mapping.

## What this means in practice for your child

If your child's [[SPARK]] WES or [[TEST-0105]] Invitae panel returns a
variant in a Searchlight gene, the atlas's report will include:
1. A direct link to that gene's Searchlight community
2. Whether the community has an active NHS
3. The atlas confidence-score boost for that gene
4. Cross-references to relevant atlas hypothesis pages and intervention
   recommendations

For genes externally handled (Phelan-McDermid, Rett, Fragile X, etc.),
the atlas links to the partner foundation directly.

## Related vault pages

- [[autism_testing_priority_ladder]] — recommended test sequence
- [[SFARI]] — overview of the broader Simons Foundation initiative
- [[SPARK]] — the free WES enrollment program
- [[TEST-0009]] — clinical-grade WES
- [[TEST-0105]] — SFARI gene panel via Invitae
- [[Hannah Poling framework]] — atlas's central organizing principle
