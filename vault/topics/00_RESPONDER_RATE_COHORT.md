---
type: index
title: Responder-rate calibration cohort
cohort_version: v0.6_intervention_ids_corrected_2026_05_09
engine_version_required: session4_v0.2.0_profile_vector
---
# Responder-rate calibration cohort

Move 2 of the post-mortem fix plan: replace atlas-internal calibration with **literature-predictive** calibration. The engine, fed published baseline profiles from N stratified RCTs, should predict published responder rates within X% mean absolute error. This cohort is the credentialing-paper deliverable.


*13 PMID-verified entries; full-text responder-rate extraction pending for most.*


---


## rrc_001_frye_2018_leucovorin_fraa

- **RCT:** Frye RE 2018 *(Mol Psychiatry)*
- **PMID:** [27752075](https://pubmed.ncbi.nlm.nih.gov/27752075/)
- **Intervention:** `INT-0001` Leucovorin (folinic acid)
- **Target dimension:** `PHE-0001`
- **Status:** `full_text_extracted_2026_05_07`


*Stratification:* FRAA-positive (folate receptor alpha autoantibody)


---


## rrc_002_lemonnier_2017_bumetanide

- **RCT:** Lemonnier E 2017 *(Transl Psychiatry)*
- **PMID:** [28291262](https://pubmed.ncbi.nlm.nih.gov/28291262/)
- **Intervention:** `INT-0005` Bumetanide
- **Target dimension:** `PHE-0007`
- **Status:** `full_text_extracted_2026_05_07`


*Stratification:* Phase 2/3 cohort — atlas-tagged subgroup of high-baseline-intracellular-
Cl⁻ neonates / children. Lemonnier's later analyses show responder-
enriched effects in this subgroup; population-average response in
Phase 3 was modest. Engine should encode this stratification.


---


## rrc_003_singh_2014_sulforaphane

- **RCT:** Singh K 2014 *(Proc Natl Acad Sci USA)*
- **PMID:** [25313065](https://pubmed.ncbi.nlm.nih.gov/25313065/)
- **Intervention:** `INT-0002` Sulforaphane (broccoli sprout extract)
- **Target dimension:** `PHE-0002`
- **Status:** `full_text_extracted_2026_05_07`


*Stratification:* None (unstratified by biomarker). Trial inclusion was male age 13-27 with moderate-to-severe ASD. Cohort had unusually high prevalence of fever-responder phenotype (32/40 = 80% vs ~35% in general ASD populations) — a behavioral observation, not a stratification axis.


---


## rrc_004_hardan_2012_nac

- **RCT:** Hardan AY 2012 *(Biol Psychiatry)*
- **PMID:** [22342106](https://pubmed.ncbi.nlm.nih.gov/22342106/)
- **Intervention:** `INT-0004` N-Acetylcysteine (NAC)
- **Target dimension:** `PHE-0002`
- **Status:** `full_text_extracted_2026_05_07`


*Stratification:* Oxidative-stress / GSH:GSSG-low subset (mechanistic)


---


## rrc_005_chez_2002_carnosine

- **RCT:** Chez MG 2002 *(J Child Neurol)*
- **PMID:** [12585724](https://pubmed.ncbi.nlm.nih.gov/12585724/)
- **Intervention:** `INT-0140` L-carnosine (oral dipeptide)
- **Target dimension:** `PHE-0007`
- **Status:** `full_text_extracted_excluded_from_mae_2026_05_07`


*Stratification:* GABA-modulation framework (Chez hypothesis)


---


## rrc_006_hendren_2016_methyl_b12

- **RCT:** Hendren RL 2016 *(J Child Adolesc Psychopharmacol)*
- **PMID:** [26889605](https://pubmed.ncbi.nlm.nih.gov/26889605/)
- **Intervention:** `INT-0003` Methyl-B12 (subcutaneous methylcobalamin)
- **Target dimension:** `PHE-0008`
- **Status:** `full_text_extracted_2026_05_07`


*Stratification:* Methylation-deficiency subset (low SAM/SAH, elevated homocysteine);
Hendren stratified by methionine cycle markers.


---


## rrc_007_wright_2011_melatonin

- **RCT:** Wright B 2011 *(J Autism Dev Disord)*
- **PMID:** [20535539](https://pubmed.ncbi.nlm.nih.gov/20535539/)
- **Intervention:** `INT-0046` Sleep architecture optimization + melatonin
- **Target dimension:** `PHE-0007`
- **Status:** `full_text_extracted_excluded_from_mae_2026_05_07`


*Stratification:* Severe sleep disorder subset


---


## rrc_008_owen_2009_aripiprazole

- **RCT:** Owen R 2009 *(Pediatrics)*
- **PMID:** [19948625](https://pubmed.ncbi.nlm.nih.gov/19948625/)
- **Intervention:** `INT-0141` Aripiprazole
- **Target dimension:** `PHE-0003`
- **Status:** `full_text_extracted_2026_05_07`


*Stratification:* Irritability subset (ABC-I baseline ≥18)


---


## rrc_009_kang_2017_microbiota_transfer

- **RCT:** Kang DW 2017 *(Microbiome)*
- **PMID:** [28122648](https://pubmed.ncbi.nlm.nih.gov/28122648/)
- **Intervention:** `INT-0076` Fecal microbiota transplantation (FMT) [MTT closest canonical match]
- **Target dimension:** `PHE-0004`
- **Status:** `full_text_extracted_2026_05_07`


*Stratification:* GI-symptomatic + dysbiotic-microbiome subset


---


## rrc_010_rossignol_2012_hbot

- **RCT:** Rossignol DA 2012 *(Med Gas Res)*
- **PMID:** [22703610](https://pubmed.ncbi.nlm.nih.gov/22703610/)
- **Intervention:** `INT-0092` Hyperbaric oxygen therapy (HBOT)
- **Target dimension:** `PHE-0002`
- **Status:** `review_extracted_excluded_from_mae_2026_05_07`


*Stratification:* Mito-vulnerable + neuroinflammatory subset; Rossignol earlier work
stratified by pre-treatment GSH/GSSG and inflammatory markers.


---


## rrc_011_adams_2011_vitamin_mineral

- **RCT:** Adams JB 2011 *(BMC Pediatr)*
- **PMID:** [22151477](https://pubmed.ncbi.nlm.nih.gov/22151477/)
- **Intervention:** `INT-0142` Vitamin/mineral multinutrient supplement (Adams 2011 formulation)
- **Target dimension:** `PHE-0002`
- **Status:** `full_text_extracted_2026_05_07`


*Stratification:* Broad metabolic deficiency subset; Adams's later work stratified by
pre-treatment biomarker abnormalities.


---


## rrc_012_tsilioni_2015_luteolin

- **RCT:** Tsilioni I 2015 *(Transl Psychiatry)*
- **PMID:** [26418275](https://pubmed.ncbi.nlm.nih.gov/26418275/)
- **Intervention:** `INT-0106` Luteolin (BBB-crossing formulation)
- **Target dimension:** `PHE-0003`
- **Status:** `full_text_extracted_2026_05_07`


*Stratification:* Elevated TNF / IL-6 / mast-cell-marker subset; Theoharides framework.


---


## rrc_013_frankovich_2017_pans_treatment

- **RCT:** Frankovich J 2017 *(J Child Adolesc Psychopharmacol)*
- **PMID:** [36358107](https://pubmed.ncbi.nlm.nih.gov/36358107/)
- **Intervention:** `INT-0143` IVIG (intravenous immunoglobulin)
- **Target dimension:** `PHE-0003`
- **Status:** `guidelines_paper_excluded_from_mae_2026_05_07`


*Stratification:* PANS-positive subset (Cunningham panel composite + acute onset). Not
generic autism — PANS overlapping subset.


---
