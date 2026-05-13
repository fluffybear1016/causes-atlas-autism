---
type: MOC
title: Peptide database — map of content
created: 2026-05-12
tags: #moc #peptides
---

# Peptide database — map of content

**25 peptides** mapped · **10 promoted to canonical atlas** · **15 vault-only research scaffolds** · evidence tiers explicit per page

> This section is the comprehensive peptide knowledge surface for the Causes Atlas. Scope: every peptide that may plausibly affect the lifecycle window from **6 months pre-conception through end of brain development** (adolescence). Goal: become the dominant open knowledge source on peptides for neurodevelopmental medicine. The atlas's verify-before-write protocol gates promotion of vault entries to canonical scoring.
>
> **Caution.** Most peptides in this database have minimal pediatric RCT data. Many are research peptides, compounding-pharmacy products, or Russian/Eastern-European clinical agents not approved in US/EU. Evidence tier is explicit on every page. Pediatric safety unknowns are flagged.

## By mechanism class

### Gh Secretagogue

| Peptide | Evidence tier | Atlas link |
| --- | --- | --- |
| [[ipamorelin\|Ipamorelin]] | `no_pediatric_no_autism_data` | _atlas-pending_ |

### Ghrh Analog

| Peptide | Evidence tier | Atlas link |
| --- | --- | --- |
| [[sermorelin\|Sermorelin (GHRH 1-29)]] | `established_GH_deficiency_no_autism_data` | _atlas-pending_ |
| [[tesamorelin\|Tesamorelin]] | `established_HIV_lipodystrophy_no_autism_data` | _atlas-pending_ |
| [[cjc-1295\|CJC-1295 (with or without DAC)]] | `no_pediatric_no_autism_data` | _atlas-pending_ |

### Anti Inflammatory Peptide

| Peptide | Evidence tier | Atlas link |
| --- | --- | --- |
| [[kpv\|KPV (Lys-Pro-Val)]] | `preclinical_only_gut_targeted` | _atlas-pending_ |

### Antimicrobial Peptide

| Peptide | Evidence tier | Atlas link |
| --- | --- | --- |
| [[ll-37-cathelicidin\|LL-37 (cathelicidin)]] | `established_endogenous_indirect_modulation` | [[INT-0133]] |

### Anxiolytic Peptide

| Peptide | Evidence tier | Atlas link |
| --- | --- | --- |
| [[selank\|Selank (TKPRPGP)]] | `anecdotal_plus_mechanistic_russian_clinical` | [[INT-0063]] |

### Developmental Neuropeptide

| Peptide | Evidence tier | Atlas link |
| --- | --- | --- |
| [[pacap\|PACAP (Pituitary Adenylate Cyclase-Activating Polypeptide)]] | `endogenous_signaling_research_only_clinical` | _atlas-pending_ |
| [[vip\|VIP (Vasoactive Intestinal Peptide)]] | `preliminary_investigational_ADNP_subset` | _atlas-pending_ |

### Growth Factor

| Peptide | Evidence tier | Atlas link |
| --- | --- | --- |
| [[igf-1-mecasermin\|IGF-1 (Mecasermin, Increlex)]] | `established_RCT_syndromic_subset` | [[INT-0132]] |

### Immune Modulator

| Peptide | Evidence tier | Atlas link |
| --- | --- | --- |
| [[thymosin-alpha-1\|Thymosin α-1 (Tα1, Zadaxin)]] | `established_extra_autism_anecdotal_in_autism` | _atlas-pending_ |

### Mitochondrial Derived

| Peptide | Evidence tier | Atlas link |
| --- | --- | --- |
| [[humanin\|Humanin (mitochondrial-derived peptide)]] | `mechanistic_only` | [[INT-0134]] |
| [[mots-c\|MOTS-c (mitochondrial-derived peptide)]] | `mechanistic_only` | [[INT-0135]] |

### Mitochondrial Targeted

| Peptide | Evidence tier | Atlas link |
| --- | --- | --- |
| [[ss-31-elamipretide\|SS-31 (Elamipretide / MTP-131)]] | `established_mechanistic_extra_autism` | _atlas-pending_ |

### Neurotrophic Mixture

| Peptide | Evidence tier | Atlas link |
| --- | --- | --- |
| [[cerebrolysin\|Cerebrolysin]] | `preliminary_RCT_pediatric` | [[INT-0065]] |
| [[cortexin\|Cortexin (bovine cortical peptide complex)]] | `russian_clinical_use_western_no_RCT` | _atlas-pending_ |

### Neurotrophic Peptide

| Peptide | Evidence tier | Atlas link |
| --- | --- | --- |
| [[p21-cntf-analog\|P21 (CNTF peptide analog)]] | `mechanistic_only` | _atlas-pending_ |
| [[dihexa\|Dihexa (PNB-0408)]] | `mechanistic_strong_clinical_anecdotal` | _atlas-pending_ |

### Nootropic Peptide

| Peptide | Evidence tier | Atlas link |
| --- | --- | --- |
| [[semax\|Semax (ACTH 4-10 analog)]] | `anecdotal_plus_mechanistic_russian_clinical` | [[INT-0064]] |

### Pineal Peptide

| Peptide | Evidence tier | Atlas link |
| --- | --- | --- |
| [[epitalon\|Epitalon (Ala-Glu-Asp-Gly)]] | `anecdotal_russian_clinical_western_unverified` | _atlas-pending_ |

### Regenerative Peptide

| Peptide | Evidence tier | Atlas link |
| --- | --- | --- |
| [[bpc-157\|BPC-157 (Body Protection Compound)]] | `preclinical_strong_clinical_absent` | [[INT-0062]] |
| [[tb-500-thymosin-beta-4\|TB-500 / Thymosin β-4]] | `preclinical_strong_clinical_extra_autism` | _atlas-pending_ |

### Social Neuropeptide

| Peptide | Evidence tier | Atlas link |
| --- | --- | --- |
| [[oxytocin-intranasal\|Oxytocin (intranasal)]] | `established_RCT_mixed` | [[INT-0061]] |
| [[carbetocin\|Carbetocin]] | `mechanistic_only_autism` | _atlas-pending_ |
| [[vasopressin\|Arginine vasopressin (intranasal)]] | `preliminary_RCT_subset` | [[INT-0131]] |

## Cross-cutting indices

- [[01_Lifecycle_Windows|Lifecycle window eligibility matrix]] — every peptide × every developmental window
- [[02_Evidence_Tiers|Evidence-tier methodology]]
- [[03_Safety_Pediatric_Notes|Pediatric safety synthesis]]

## Dataview queries (Obsidian)

Use these inside Obsidian (requires Dataview plugin):

```dataview
TABLE class AS "Class", evidence_tier AS "Evidence", atlas_int AS "Atlas"
FROM "peptides"
WHERE !contains(file.name, "_MOC") AND !contains(file.name, "0")
SORT class ASC, file.name ASC
```

```dataview
TABLE evidence_tier AS "Evidence", atlas_int AS "Atlas"
FROM "peptides"
WHERE contains(tags, "#peptide/social-neuropeptide")
SORT evidence_tier ASC
```

```dataview
LIST
FROM "peptides"
WHERE contains(tags, "#status/atlas-promotion-candidate")
```

## Promotion workflow (from vault to canonical atlas)

1. Curator reviews vault peptide page
2. Verifies any PMID claims via PubMed esummary
3. Authors INT-XXXX row in `v2.0_scored/interventions.csv` with verified citations
4. Re-runs scoring; verifies calibration anchor (INT-0001 ≥ 80)
5. Updates this MOC: changes `atlas_int: pending` to `atlas_int: INT-XXXX` in the peptide page frontmatter
6. Commits with PMIDs in commit message
