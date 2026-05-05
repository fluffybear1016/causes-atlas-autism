# Case 011 — Hannah Poling (federal Vaccine Court ruling, 2008)

## Source profile

**Published / federally-adjudicated case profile** (anonymized for atlas use).
This case is the namesake calibration anchor for the personalized risk
calculator (per [SESSION_4_HANNAH_POLING_SPEC.md](../../../SESSION_4_HANNAH_POLING_SPEC.md)
§13.5).

**Federal record:** Office of Special Masters, U.S. Court of Federal Claims,
*Poling v. Secretary of Health and Human Services*, No. 02-1466V, conceded
2008. The Department of Health and Human Services conceded that vaccinations
"significantly aggravated an underlying mitochondrial disorder, which
predisposed [Hannah Poling] to deficits in cellular energy metabolism, and
manifested as a regressive encephalopathy with features of autism spectrum
disorder."

**Atlas source rows:**
- SRC-001418 — Hannah Poling federal Vaccine Court ruling (atlas tier 1
  primary FOIA / federal-record evidence per CLAUDE.md §1.2)

**Published clinical record:** Poling JS et al., *J Child Neurol* 2006
(published before federal ruling, by Hannah's father describing similar
mitochondrial-vulnerability cases). PMID-verified separately if cited in
spec body.

## Pre-vaccination clinical profile (per court record)

- 19-month-old female
- Healthy and developmentally on track until July 2000
- Family history: maternal SLE-spectrum autoimmune disease (relevant per
  HYP-0008 maternal immune activation framework)
- No known prior neurodevelopmental concerns

## Triggering event

July 2000: simultaneous administration of 9 vaccine doses across 5 vaccines
(DTaP, Hib, MMR, varicella, IPV) in one office visit.

Within 48 hours: high fever, persistent crying, refusal to walk.
Within 2 weeks: lethargy, irritability, loss of language, regression
across multiple developmental domains.

## Post-event clinical evolution

- Encephalopathy diagnosis
- Mitochondrial enzyme deficiency identified on muscle biopsy:
  Complex I, III, V deficits
- mtDNA mutation: T2387C heteroplasmy (12S rRNA region)
- Subsequent diagnosis of autism spectrum disorder per DSM criteria

## Why this case is the calibration anchor

Per CLAUDE.md mission framing and SESSION_4_HANNAH_POLING_SPEC.md §0:
this is the canonical **legal-medical recognition** of the susceptibility
× trigger → mechanism → phenotype framework. A mitochondrial-vulnerability
profile (P) plus a vaccine-immune challenge (E) produced a regressive
encephalopathy with autism features (Φ) via energy-metabolism cascade
(M). The federal court awarded compensation specifically on the basis
that the conditional risk P(Φ | P, E) was non-zero and substantial,
even where the population-average P(Φ | E) is null.

## Expected calculator behavior on this input

- **Top phenotype**: PHE-0002 (mitochondrial dysfunction phenotype) should
  dominate the posterior, with PHE-0003 (regressive immune-inflammatory)
  as secondary.
- **Posterior point estimate** for PHE-0002: ≥ 0.50, with credal interval
  excluding < 0.20 (per §13.5 anchor stability rule).
- **Top interventions**: mitochondrial cocktail (CoQ10, L-carnitine,
  B-vitamins) — INT-0011, INT-0012, INT-0017, INT-0019, INT-0020 — with
  immune-modulatory secondary (LDN INT-0006, antihistamine support).
- **Avoidance bundle** must flag: simultaneous multi-vaccine administration
  in mito-vulnerable subset (per §3.13c iatrogenic priors); consider
  spaced schedule with prior pediatric mitochondrial workup; chelation
  must NOT be a top recommendation (see anchor stability discussion).
- **CDR state**: sub-acute or chronic (not acute, given case occurred
  ~26 years before this run).
- **Syndromic flag**: false (POLG / mtDNA-related but not classified as a
  rare-syndromic-autism gate hit per §4 rule-out checklist).
- **Open questions**: should flag muscle-biopsy + cytokine + Cunningham
  Panel as high-EIG biomarkers if not already in input.

## Calibration-anchor stability rule

Per §13.5: the PHE-0002 posterior point estimate from this case must remain
within ±0.10 of the locked v1.0 baseline across version revisions. If it
drifts outside this band, the version is flagged for review.
