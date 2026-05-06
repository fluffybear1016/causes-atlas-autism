---
type: index
title: Responder-rate calibration cohort
cohort_version: v0.1_scaffold
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
- **Status:** `scaffold`


*Stratification:* FRAA-positive (folate receptor alpha autoantibody)


---


## rrc_002_lemonnier_2017_bumetanide

- **RCT:** Lemonnier E 2017 *(Transl Psychiatry)*
- **PMID:** [28291262](https://pubmed.ncbi.nlm.nih.gov/28291262/)
- **Intervention:** `INT-0023` Bumetanide
- **Target dimension:** `PHE-0007`
- **Status:** `scaffold_engine_gap`


*Stratification:* Phase 2/3 cohort — atlas-tagged subgroup of high-baseline-intracellular-
Cl⁻ neonates / children. Lemonnier's later analyses show responder-
enriched effects in this subgroup; population-average response in
Phase 3 was modest. Engine should encode this stratification.


---


## rrc_003_zimmerman_singh_2021_sulforaphane

- **RCT:** Zimmerman AW 2021 *(Mol Autism)*
- **PMID:** [34034808](https://pubmed.ncbi.nlm.nih.gov/34034808/)
- **Intervention:** `INT-0002` Sulforaphane (broccoli sprout extract)
- **Target dimension:** `PHE-0002`
- **Status:** `scaffold`


*Stratification:* Mito-vulnerable / oxidative-stress subset (Singh 2014 PNAS earlier work
showed responder enrichment in elevated-oxidative-stress profiles).


---


## rrc_004_hardan_2012_nac

- **RCT:** Hardan AY 2012 *(Biol Psychiatry)*
- **PMID:** [22342106](https://pubmed.ncbi.nlm.nih.gov/22342106/)
- **Intervention:** `INT-0029` N-acetylcysteine (NAC)
- **Target dimension:** `PHE-0002`
- **Status:** `scaffold`


*Stratification:* Oxidative-stress / GSH:GSSG-low subset (mechanistic)


---


## rrc_005_chez_2002_carnosine

- **RCT:** Chez MG 2002 *(J Child Neurol)*
- **PMID:** [12585724](https://pubmed.ncbi.nlm.nih.gov/12585724/)
- **Intervention:** `INT-0036` L-carnosine
- **Target dimension:** `PHE-0007`
- **Status:** `scaffold`


*Stratification:* GABA-modulation framework (Chez hypothesis)


---


## rrc_006_hendren_2016_methyl_b12

- **RCT:** Hendren RL 2016 *(J Child Adolesc Psychopharmacol)*
- **PMID:** [26889605](https://pubmed.ncbi.nlm.nih.gov/26889605/)
- **Intervention:** `INT-0003` Methyl-B12 (subcutaneous methylcobalamin)
- **Target dimension:** `PHE-0008`
- **Status:** `scaffold`


*Stratification:* Methylation-deficiency subset (low SAM/SAH, elevated homocysteine);
Hendren stratified by methionine cycle markers.


---


## rrc_007_wright_2011_melatonin

- **RCT:** Wright B 2011 *(J Autism Dev Disord)*
- **PMID:** [20535539](https://pubmed.ncbi.nlm.nih.gov/20535539/)
- **Intervention:** `INT-0042` Melatonin
- **Target dimension:** `PHE-0007`
- **Status:** `scaffold`


*Stratification:* Severe sleep disorder subset


---


## rrc_008_owen_2009_aripiprazole

- **RCT:** Owen R 2009 *(Pediatrics)*
- **PMID:** [19948625](https://pubmed.ncbi.nlm.nih.gov/19948625/)
- **Intervention:** `INT-0029` Aripiprazole
- **Target dimension:** `PHE-0003`
- **Status:** `scaffold`


*Stratification:* Irritability subset (ABC-I baseline ≥18)


---


## rrc_009_kang_2017_microbiota_transfer

- **RCT:** Kang DW 2017 *(Microbiome)*
- **PMID:** [28122648](https://pubmed.ncbi.nlm.nih.gov/28122648/)
- **Intervention:** `INT-0025` Microbiota Transfer Therapy (MTT)
- **Target dimension:** `PHE-0004`
- **Status:** `scaffold`


*Stratification:* GI-symptomatic + dysbiotic-microbiome subset


---


## rrc_010_rossignol_2012_hbot

- **RCT:** Rossignol DA 2012 *(Med Gas Res)*
- **PMID:** [22703610](https://pubmed.ncbi.nlm.nih.gov/22703610/)
- **Intervention:** `INT-0017` Hyperbaric Oxygen Therapy (HBOT)
- **Target dimension:** `PHE-0002`
- **Status:** `scaffold`


*Stratification:* Mito-vulnerable + neuroinflammatory subset; Rossignol earlier work
stratified by pre-treatment GSH/GSSG and inflammatory markers.


---


## rrc_011_adams_2011_vitamin_mineral

- **RCT:** Adams JB 2011 *(BMC Pediatr)*
- **PMID:** [22151477](https://pubmed.ncbi.nlm.nih.gov/22151477/)
- **Intervention:** `INT-0018` Vitamin/mineral multinutrient supplement (Adams formulation)
- **Target dimension:** `PHE-0002`
- **Status:** `scaffold`


*Stratification:* Broad metabolic deficiency subset; Adams's later work stratified by
pre-treatment biomarker abnormalities.


---


## rrc_012_tsilioni_2015_luteolin

- **RCT:** Tsilioni I 2015 *(Transl Psychiatry)*
- **PMID:** [26418275](https://pubmed.ncbi.nlm.nih.gov/26418275/)
- **Intervention:** `INT-0006` Luteolin formulation
- **Target dimension:** `PHE-0003`
- **Status:** `scaffold`


*Stratification:* Elevated TNF / IL-6 / mast-cell-marker subset; Theoharides framework.


---


## rrc_013_frankovich_2017_pans_treatment

- **RCT:** Frankovich J 2017 *(J Child Adolesc Psychopharmacol)*
- **PMID:** [36358107](https://pubmed.ncbi.nlm.nih.gov/36358107/)
- **Intervention:** `INT-0027` IVIG / immunomodulatory therapy (PANS subset)
- **Target dimension:** `PHE-0003`
- **Status:** `scaffold`


*Stratification:* PANS-positive subset (Cunningham panel composite + acute onset). Not
generic autism — PANS overlapping subset.


---
