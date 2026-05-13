---
title: Peptide evidence tiers — methodology
tags: #peptides #methodology
---

# Peptide evidence tiers

Tiers used across this database. Strictly descriptive; no comparative ranking implied between tiers. A `mechanistic_only` peptide with strong preclinical work + biological plausibility is not "worse" than an `established_RCT_mixed` peptide where the RCTs were negative — they are answering different questions.

| Tier | Meaning | Example |
| --- | --- | --- |
| `established_RCT_mixed` | ≥1 multi-arm RCT in autism population; aggregate effect mixed; subset signals present | Oxytocin (intranasal) |
| `established_RCT_subset` | RCT evidence positive in a defined biological subset | IGF-1 in Phelan-McDermid (SHANK3) |
| `preliminary_RCT_pediatric` | Small pediatric RCT(s); not yet replicated | Cerebrolysin (Akhondzadeh 2018) |
| `preliminary_RCT_subset` | Small RCT in defined subset; signal but underpowered | Vasopressin (Parker 2019, n=30) |
| `preliminary_investigational_ADNP_subset` | Investigational compound in syndromic subset | Davunetide / NAP in ADNP-related autism |
| `mechanistic_only` | Mechanism + preclinical data only; no clinical | P21, MOTS-c exogenous |
| `mechanistic_strong_clinical_anecdotal` | Strong mechanism + adult anecdotal use | Dihexa |
| `preclinical_strong_clinical_extra_autism` | Strong preclinical or extra-autism clinical | TB-500 in dry eye (EU approved); no autism data |
| `preclinical_strong_clinical_absent` | Strong preclinical; no human clinical data | BPC-157 |
| `preclinical_only_gut_targeted` | Preclinical work; gut-local action | KPV |
| `russian_clinical_use_western_no_RCT` | Decades of Russian/EE clinical use; no Western RCT | Cortexin |
| `anecdotal_russian_clinical_western_unverified` | Russian claims; Western skepticism | Epitalon |
| `anecdotal_plus_mechanistic_russian_clinical` | Russian clinical use + mechanism + Western mechanism support | Semax, Selank |
| `established_extra_autism_anecdotal_in_autism` | Approved/established in non-autism indication; anecdotal autism use | Thymosin α-1 |
| `established_endogenous_indirect_modulation` | Endogenous peptide modulated indirectly | LL-37 via vitamin D |
| `established_HIV_lipodystrophy_no_autism_data` | Approved in unrelated indication; no autism data | Tesamorelin |
| `established_GH_deficiency_no_autism_data` | Approved in GH-deficiency; no autism data | Sermorelin |
| `no_pediatric_no_autism_data` | No pediatric data of any kind | Ipamorelin, CJC-1295 |
| `endogenous_signaling_research_only_clinical` | Endogenous; exogenous use is research-only | PACAP |

## Rule of thumb for promotion to canonical atlas

A vault peptide page is a candidate for promotion to canonical `interventions.csv` when:
- ≥1 PMID-verifiable autism-specific clinical study exists (any size, any design), OR
- Strong mechanism + ≥1 PMID-verifiable RCT in a closely-related neurodevelopmental syndrome
- AND the curator has reviewed safety profile for pediatric eligibility

`mechanistic_only` and `no_pediatric_no_autism_data` tiers stay vault-only until they accumulate evidence.
