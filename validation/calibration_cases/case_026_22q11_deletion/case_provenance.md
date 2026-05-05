# Case 026 — 22q11.2 deletion syndrome (DiGeorge / velocardiofacial) — syndromic gate test

## Source profile

**Synthesized published case profile** representing the typical 22q11.2 deletion syndrome presentation per Motahari 2019 J Neurodev Disord (PMID 31174463) review.

**Atlas reference:** RSG-0010 (rare-syndrome screening gate row 10) routes 22q11.2 deletion to `22q11_specific` syndromic-specific output (NOT generic phenotype assignment). This case is the calibration test for syndromic-gate routing per spec §4.

## Pre-presentation profile

- 4-year-old male
- Presented at birth with conotruncal cardiac defect (tetralogy of Fallot, surgically corrected)
- Hypocalcemia infancy (resolved with supplementation)
- Mild thymic hypoplasia on imaging
- Cleft palate (surgically repaired)
- Developmental delay diagnosed at 18 months
- Autism features per ADOS/ADI-R at age 4
- 22q11.2 typical 3 Mb deletion confirmed by FISH at age 2
- No known mitochondrial dysfunction
- Family history negative for autism; positive for psychiatric disorders (paternal aunt schizophrenia)

## Why this case is a syndromic gate test

Per spec §4: rare-syndrome screening gate runs FIRST in calculation engine. If a syndromic match is detected, generic phenotype assignment is bypassed and syndrome-specific output is produced. This case validates that:
1. Engine detects 22q11.2 deletion in genetic input
2. Sets `syndromic_flag: true`
3. Routes output via 22q11_specific path (NOT to generic PHE-0001..0011)
4. Includes specialty referral recommendation (22q11.2 Society network + cardiology + immunology + endocrinology + psychiatry surveillance)
5. Includes psychiatric surveillance for emerging psychosis from adolescence (~25% lifetime risk per Motahari 2019)

## Expected calculator behavior

- **syndromic_flag: true** (CRITICAL — this is the primary test)
- **syndromic_match: 22q11.2_deletion_DiGeorge**
- **target_routing: 22q11_specific** (not a PHE-NNNN ID)
- **Generic phenotype assignment**: should be DEPRIORITIZED relative to syndrome-specific output. Engine may still emit phenotype posteriors but with explicit syndromic-context flag
- **Specialty referrals**: should include cardiology, immunology, endocrinology, psychiatry surveillance, 22q11.2 Society network
- **Avoidance**: live-virus vaccine caution if T-cell deficiency, calcium monitoring
- **Open questions**: should flag T-cell subset analysis if not in input; PTH/calcium if not in input

## Calibration validation criterion

- syndromic_flag = true (exact match)
- syndromic_match = 22q11.2_deletion_DiGeorge or equivalent (exact match)
- Output includes psychiatric_surveillance_recommendation
- Output includes specialty_referral_22q11_network or equivalent
- Generic phenotype top != PHE-0001..0011 OR explicit syndromic_context flag attached
