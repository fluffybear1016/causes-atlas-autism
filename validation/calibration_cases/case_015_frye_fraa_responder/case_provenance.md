# Case 015 — Frye 2018 FRAA-positive leucovorin responder profile

## Source profile

**Published case profile** (synthesized from cohort-level findings; not a single named patient).

**Atlas source:** Frye RE et al., *Mol Psychiatry* 2018 — "Folinic acid improves verbal communication in children with autism and language impairment: a randomized double-blind placebo-controlled trial."
- **PMID 27752075** ([PubMed verified](https://pubmed.ncbi.nlm.nih.gov/27752075/))
- 12-week placebo-controlled RCT, n=48, FRAA-positive subset showed substantial improvement in verbal communication

**Calibration anchor for Layer 2 INT-0001 ≥ 80** — this case represents the responder profile Layer 2 CSRS scoring is calibrated for.

## Pre-treatment clinical profile (synthesized)

- 5-year-old male
- Diagnosed with autism + language impairment
- FRAA blocking + binding both positive on serum testing
- MTHFR C677T heterozygous (C/T)
- No documented mitochondrial dysfunction (normal lactate, no muscle biopsy)
- No regression history (congenital/developmental autism phenotype)
- Family history: maternal autoimmune (Hashimoto's)
- No syndromic features; no rare-syndrome gate trigger

## Triggering / etiologic factors

- Per Frye-Slattery framework: cerebral folate transport blocked by autoantibodies against folate receptor 1 (FOLR1)
- Mechanism: FRAA blocks folate transport at choroid plexus; brain folate deficient despite normal blood folate
- Treatable with **folinic acid (leucovorin)** which uses an alternative transporter (RFC) to reach brain

## Why this case is the Layer 2 calibration anchor

INT-0001 (leucovorin) calibration anchor at CSRS ≥ 80 is supported by this responder profile. Frye 2018 RCT showed:
- Substantial improvement in verbal communication in FRAA+ subset
- Effect size ~0.5-1.0 (Cohen's d) across language outcome measures
- Subset-stratified design = exemplar of Hannah-Poling-style P(Φ|P,E) > P(Φ|E) where the susceptibility profile FRAA+ is the P

## Expected calculator behavior on this input

- **Top phenotype**: PHE-0001 (cerebral folate deficiency phenotype) should dominate posterior with point estimate ≥ 0.55, credal interval excludes < 0.30
- **Top interventions** (≥2 of these in top-3 of bundle):
  - INT-0001 Leucovorin (the calibration anchor)
  - INT-0008 Methylated folate (5-MTHF) — alternative folate form
  - INT-0003 Methyl-B12 — methylation cycle support
  - INT-0017 Pyridoxal-5-phosphate (B6) — methylation cycle support
- **Recommendation type for INT-0001**: START with HIGH confidence
- **Avoidance bundle**: synthetic folic acid (high-dose) — flagged because of unmetabolized folic acid concern in folate-pathway-impaired children
- **CDR state**: not_applicable_to_static_phenotype or sub_acute (per §7.6)
- **Syndromic flag**: false
- **Open questions**: should NOT flag FRAA panel (already in input); may flag homocysteine + methylation panel as next biomarkers

## Calibration validation criterion

- Top phenotype = PHE-0001 (exact match)
- PHE-0001 posterior point ≥ 0.55, ceiling ≤ 0.95
- ≥2 of {INT-0001, INT-0008, INT-0003, INT-0017} in top-3 of intervention bundle
- INT-0001 recommendation_type = START (exact match)
- syndromic_flag = false
