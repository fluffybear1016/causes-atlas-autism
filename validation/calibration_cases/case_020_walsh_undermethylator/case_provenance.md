# Case 020 — Walsh undermethylator biotype profile

## Source profile

**Walsh framework biotype** (synthesized; based on Walsh Research Institute clinical pattern).

**Atlas reference:** Walsh-framework biotype phenotype PHE-0008 with confidence_label LOW per audit H-10. The Walsh framework lacks primary peer-reviewed RCT evidence; the atlas treats Walsh-derived priors with explicit lower evidence_quality (0.30-0.35) and wider credal intervals.

**This case tests two engine behaviors:**
1. Walsh-biotype routing (PHE-0008) functions correctly
2. Engine emits appropriate `phenotype_evidence_tier` flag per audit C-5 (Walsh phenotypes routed with framework-derived caveat, not as high-confidence priors)

## Pre-treatment clinical profile (synthesized Walsh undermethylator pattern)

- 9-year-old female (Walsh framework reports undermethylator more common in females per his series; not peer-reviewed)
- Diagnosed with autism + comorbid OCD features
- Personality cluster (per Walsh framework): high inner tension, perfectionism, OCD/ritualistic behaviors, seasonal allergies
- Whole-blood histamine: low (Walsh undermethylator marker)
- Plasma SAM/SAH ratio: low (impaired methylation capacity)
- MTHFR C677T heterozygous (C/T)
- COMT V158M heterozygous (V/M)
- No FRAA evidence
- No mitochondrial markers elevated
- No regression history; congenital pattern
- No syndromic features

## Etiology proposal (Walsh framework)

- Per Walsh: low whole-blood histamine + low SAM/SAH = "undermethylator" phenotype
- Treatment per Walsh: methyl donors (methionine, SAMe, methyl-B12; sometimes 5-MTHF cautiously)
- Atlas position: Walsh framework recorded as evidence at LOW evidence_quality per audit H-10; not dismissed but not given high-confidence weight

## Expected calculator behavior

- **Top phenotype**: PHE-0008 (Walsh undermethylator) should appear in top-3 with confidence label MODERATE-LOW
- May share top-rank with PHE-0001 (CFD-spectrum) or other methylation-pathway phenotypes
- **Phenotype evidence tier flag**: must show `phenotype_evidence_tier: framework_derived_LOW` per audit C-5 fix
- **Top interventions** (≥1 of these in top-3):
  - INT-0019 SAMe (methyl donor)
  - INT-0003 Methyl-B12
  - INT-0017 Pyridoxal-5-phosphate (B6)
  - INT-0018 TMG/betaine
- **Avoidance**: synthetic folic acid high-dose (folate-cautious in some Walsh frameworks)
- **Recommendation type for top interventions**: CONSIDER (not START) due to LOW evidence_quality
- **Syndromic flag**: false
- **Open questions**: should flag urinary kryptopyrroles (PHE-0010 differential) and Cu/Zn ratio (PHE-0011 differential)

## Calibration validation criterion

- PHE-0008 in top-3 phenotype ranking
- Confidence label for PHE-0008 ≤ MODERATE
- ≥1 of {INT-0019, INT-0003, INT-0017, INT-0018} in top-3 of intervention bundle
- Recommendation type for top Walsh-derived intervention = CONSIDER (not START)
- syndromic_flag = false
