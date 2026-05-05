# Session 4 — Hannah Poling Personalized Risk Calculator

**Spec version:** 2.3 — 2026-04-30 (audit response: determinism formalism, scientific-accuracy corrections, sensory phenotype + sleep medicine + supplement-PGx layers, expanded validation)
**Status:** Architecture spec; pre-implementation; supersedes v2.2
**Audit reference:** `/Users/Greg/Autism/SESSION_4_v22_AUDIT_PUNCH_LIST.md`
**Prerequisite atlas state:** v2.0_scored at calibration 83.35; 178 biomarkers, 137+ interventions, 75+ hypotheses, 33 mechanisms, 7 phenotypes (+4 Walsh biotypes), 96 BPE + 184 BME + 53 BIE + 171 BHE edges
**Prerequisite engineering state:** Phase 0 blockers must be resolved before Phase 1 (see §15)

---

## §0 — Purpose (long-form)

### 0.1 The problem this calculator exists to solve

A family — at any of five life-stages — currently faces an information-asymmetry crisis when trying to make autism-relevant decisions. The literature is enormous, contradictory, often funded asymmetrically, and almost never stratified by individual susceptibility. Mainstream pediatric guidance gives the population-average answer. Functional-medicine clinicians give the individualized answer but vary widely in framework, evidence-grounding, and rigor. Direct-to-consumer genetic testing gives raw data with no clinical interpretation. The internet gives noise.

The Causes Atlas already encodes the underlying scientific substrate: 75+ hypotheses, 33 mechanisms, 7 phenotypes (+4 Walsh biotypes), 178 biomarkers, 137+ interventions, 1420 sources, 1647 evidence_links. What is missing is a **deterministic, evidence-grounded, transparent, reproducible engine** that takes a specific family's data and outputs **the conditional risk and ranked action bundle that maps to *their* susceptibility profile** — formalizing the Hannah Poling principle:

> **causation = susceptibility (P) × trigger (E) → mechanism (M) → phenotype (Φ)**
>
> for any specific child, P(Φ | P, E) ≠ P(Φ | E)

The calculator's job is to answer, *given everything the atlas knows*, what is **P(Φᵢ | this family's P, this family's E, this family's exposome and microbiome)** for each of the 11 phenotype classes, and which intervention/avoidance bundle has the highest expected impact for **this** family — with explicit credal uncertainty, full reasoning trace, pharmacogenomic safety filters, and clinician-handoff framing.

### 0.2 Five user constituencies

The calculator must serve five distinct life-stage modes (expanded from four in v2.0). Each has different inputs, different output emphasis, and different ethical posture.

**Constituency A — Pre-conception family.** Goal: optimize the metabolic environment of a future pregnancy. Inputs: parental genetics, parental biomarkers, family history. Output: pre-conception interventions, planned-pregnancy avoidances, exposure cleanup, methylation/mito/glutathione optimization.

**Constituency B — Pregnant family.** Goal: optimize current pregnancy and prepare for delivery + neonatal period. Inputs: A + active pregnancy data, current maternal labs, exposures-to-date. Output: pregnancy-stage interventions, vaccination decisions, medication decisions, delivery planning. Time-critical.

**Constituency C — Family with young child (0–24 months).** Goal: pre-regression intervention window. Inputs: A + B + child birth/neonatal/biomarker data, milestone status. Output: monitoring plan, biomarker workup, vaccination individualization, early intervention. **Highest expected impact constituency** — interventions in this window have the largest leverage.

**Constituency D — Family with older child / adolescent (24 months – 18 years).** Goal: phenotype classification, ranked workup, ranked intervention bundle, clinician handoff. Inputs: full historical data + current biomarkers + intervention-response history. Output: phenotype-classification confidence, "test these next" workup, intervention ranking, "stop / reduce" candidates.

**Constituency E — Adult / late-diagnosis individual (18+ years).** Goal: self-directed decision support for adult autistic individuals (often late-diagnosed, often female, often without childhood biomarker data). Inputs: current self-reported phenotype features, current biomarkers, family history, intervention history. Output: phenotype-classification across the 11-phenotype space (with appropriate uncertainty), ranked workup, ranked self-directed interventions, ranked avoidances, clinician handoff. Distinct from D in that the user is the patient, autonomy framing dominates, and pediatric-window-only interventions are excluded.

### 0.3 What the calculator does — explicit list

1. **Phenotype-probability inference**: P(Φᵢ | P, E) for all 11 phenotype classes (7 main + 4 Walsh biotypes) with explicit credal intervals.
2. **Top-driver attribution**: top 3–5 priors driving each phenotype probability (variants, biomarkers, exposures, family history, microbiome, exposome).
3. **Pathway-burden analysis**: total burden across mTOR, methylation, mito-OXPHOS, glutamatergic, GABAergic, immune-inflammatory, microbiome-axis pathways — not just per-variant sum.
4. **Within-phenotype responder profile**: probability that this specific child responds to top interventions, beyond the phenotype-conditional baseline (PGx + biomarker-stratified).
5. **Ranked intervention bundle** segmented by life-stage, each with: phenotype-conditional efficacy, PGx safety check, NNT, time-to-response, evidence grade, recommendation type, cost tier.
6. **Ranked avoidance bundle** segmented by life-stage and conditional on susceptibility profile.
7. **"Test these next" biomarker recommendations** — top 8 highest-information-gain biomarkers given current input state, weighted by inverse cost.
8. **Rare-syndrome screening gate** — explicit rule-out checklist for syndromic autism (FXS, MECP2/Rett, PMS, Angelman, TSC, IEMs) before generic phenotype assignment.
9. **CDR state assignment** — Naviaux Cell Danger Response state (acute / sub-acute / chronic / resolved) + transition probabilities.
10. **Functional-outcome trajectory** — verbal trajectory, IQ trajectory, adaptive-functioning trajectory, regression-risk window — with explicit credal intervals.
11. **Reasoning trace** — full deterministic audit log: every prior used, every shift applied, every aggregation step, with PMID grounding.
12. **Confidence label** per recommendation.
13. **Open-question flagging** — where additional information would substantially shift recommendations.
14. **Feasibility-constrained bundle** — alternative ranked bundle filtered by user-supplied cost / access constraints.
15. **Clinician-handoff document** — auto-generated 1–2 page summary suitable for review with a functional-medicine / MAPS / genetic-counseling clinician.

### 0.4 What the calculator explicitly does NOT do

- It does **not** diagnose autism or any phenotype. Diagnosis requires a clinician.
- It does **not** prescribe. Every output is decision-support, not directive.
- It does **not** give population-policy answers.
- It does **not** override existing prescriptions. STOP_WITH_CLINICIAN is the strongest "stop" signal it emits.
- It does **not** make selective-pregnancy recommendations.
- It does **not** claim to predict outcome with certainty — it predicts conditional probabilities with credal uncertainty.
- It does **not** replace specialist clinical workups (Walsh biotyping, MAPS, Frye CFD, Cunningham, mito specialist) — it informs which to prioritize.
- It does **not** consume facial photos, voice recordings, or other biometric inputs that could be misused.

### 0.5 Why this matters — theoretical

The Hannah Poling framework is the central organizing principle of the atlas (per CLAUDE.md). It is currently **non-operationalized** — it lives as a conceptual claim and a single federal court ruling. The calculator turns the framework into mathematics. This makes the framework testable, refutable, and improvable. If the calculator's predictions don't pan out in real families, the priors get refined. If they do, the framework gains empirical support.

### 0.6 Why this matters — practical

A family in Constituency A reduces planned child's mito-phenotype risk by addressing maternal SAM/SAH and CoQ10 status. A family in Constituency B avoids a specific medication during T2 because of a maternal genotype × medication conditional risk. A family in Constituency C catches early FRAA elevation, starts leucovorin in the pre-regression window, no regression occurs. A family in Constituency D gets a clinician-handoff document that compresses 18 months of guesswork into a focused 8-biomarker workup. An adult in Constituency E gets self-directed decision support for the first time.

### 0.7 Competitive landscape

| Tool/system | Captures | Misses |
|---|---|---|
| 23andMe / Nebula | Common SNPs, generic traits | No phenotype framework, no biomarkers, no interventions, no CNVs reliably |
| Spectrum 10K, SPARK, ABCD | Cohort-level genetic + behavioral | Population-level, not individual decisions, no biomarkers, no exposome |
| Polygenic risk scores for autism | SNP-summed risk | No biomarkers, no exposures, no phenotype resolution, no interventions, European-skewed |
| Walsh Research Institute | Methylation/Cu:Zn/pyrrole biotypes | Single-framework, not credal, clinician-only |
| Frye/Slattery CFD framework | FRAA + leucovorin | Single phenotype |
| MAPS / Bock / Klinghardt | Functional medicine workup | Heuristic, clinician-mediated, not deterministic |
| Cunningham Panel | PANS/PANDAS antibodies | Single phenotype |
| Generic pediatric guidelines | Population-average schedule | Blind to individual susceptibility (Hannah Poling problem) |
| GeneSight / Genelex (PGx) | Drug metabolism | Drug-only; no autism phenotype mapping |
| Mosaic Diagnostics | Mycotoxin / metals exposure | Toxicology-only; no integration |
| Viome / DayTwo / Microba | Microbiome composition | Microbiome-only; no integration |

The calculator's competitive position: **the only system that integrates genetics + CNVs + WGS rare variants + mtDNA + epigenetics + microbiome + metabolomics + immunology + toxicology + family history + exposome into deterministic phenotype-resolved conditional probability + PGx-safe ranked life-stage-conditional intervention/avoidance bundles, with credal uncertainty and full reasoning trace.** It consumes the outputs of all the above and synthesizes.

---

## §1 — Architecture overview

```
┌────────────────────────────────────────────────────────────────────────┐
│  INPUT LAYER (JSON Schema, see §2)                                     │
│  - Operating mode (preconception / pregnancy / young / older / adult)  │
│  - Parental + child genetics: SNPs + CNVs + WGS rare variants + mtDNA  │
│  - HLA typing                                                          │
│  - Maternal + child biomarker panels (longitudinal)                    │
│  - Microbiome data (16S / shotgun)                                     │
│  - Toxicology / exposome (measured + history)                          │
│  - Hormonal axis panels (HPA, HPT, sex hormones, oxytocin/vasopressin) │
│  - Metabolomics, proteomics, epigenetics (when available)              │
│  - Family history (autism, ESSENCE, autoimmune, neuro, sibs)           │
│  - Comorbid conditions (epilepsy, ADHD, MCAS, EDS, POTS)               │
│  - Gestational + birth process data                                    │
│  - ACEs / trauma exposure                                              │
│  - Planned/actual exposures                                            │
│  - Existing intervention response history                              │
└────────────────┬───────────────────────────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────────────────────────┐
│  PRE-PROCESSING LAYER                                                  │
│  - Schema validation                                                   │
│  - Rare-syndrome screening gate (§4)                                   │
│  - Lab-reference-range normalization (z-scores)                        │
│  - Ancestry-based variant frequency calibration                        │
│  - Sex-specific prior selection                                        │
│  - CNV / VUS classification                                            │
└────────────────┬───────────────────────────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────────────────────────┐
│  CALCULATION LAYER (deterministic, no LLMs)                            │
│  - 14 prior tables (§3)                                                │
│  - Pathway burden analysis                                             │
│  - CDR state assignment + transition probabilities                     │
│  - Conflict-resolution policy (§5)                                     │
│  - Walley IDM credal aggregation (§6)                                  │
│  - PGx contraindication filter                                         │
│  - Within-phenotype responder model                                    │
│  - Age-stratified efficacy modulation                                  │
│  - "Next biomarker" expected information gain                          │
│  - Functional-outcome trajectory model                                 │
│  - Cost/feasibility constraint solver                                  │
│  - Existing CSRS engine for intervention base scoring                  │
└────────────────┬───────────────────────────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────────────────────────┐
│  OUTPUT LAYER (§9)                                                     │
│  - 11 phenotype P(Φ|P,E) with credal interval                          │
│  - Pathway burden scores (7 pathways)                                  │
│  - CDR state + transition probabilities                                │
│  - Functional trajectory prediction with credal interval               │
│  - Top susceptibility drivers per phenotype                            │
│  - Within-phenotype responder probabilities for top interventions      │
│  - Life-stage-segmented intervention bundle (PGx-filtered)             │
│  - Life-stage-segmented avoidance bundle                               │
│  - "Test these next" ranked by EIG, weighted by cost                   │
│  - Per-recommendation reasoning trace                                  │
│  - Confidence + recommendation-type label per item                     │
│  - Feasibility-constrained alternative bundle                          │
│  - Clinician handoff document                                          │
│  - Open-question flags                                                 │
│  - Rare-syndrome rule-out checklist                                    │
└────────────────────────────────────────────────────────────────────────┘
```

Layer position in atlas: this is **Layer 3** — built atop Layer 1 (causal graph) and Layer 2 (CSRS scoring). It does not modify the lower layers.

---

## §2 — Input schema (JSON)

### 2.1 Top-level structure

```json
{
  "case_id": "uuid (anonymous)",
  "case_date": "ISO 8601",
  "input_version": "2.3",
  "operating_mode": "preconception | pregnancy | young_child | older_child | adult",
  "engine_version_requested": "session4_v2.3",

  "subject_sex": "M | F | intersex | unknown",
  "subject_ancestry": ["array of population codes for variant frequency calibration"],

  "maternal": { ... §2.2 },
  "paternal": { ... §2.3 },
  "family_history": { ... §2.4 },
  "child_data": { ... §2.5 (if operating_mode != preconception) },
  "self_data": { ... §2.6 (if operating_mode == adult) },

  "genomics": { ... §2.7 — full multi-modal genomics },
  "microbiome": { ... §2.8 },
  "toxicology": { ... §2.9 },
  "hormonal_axes": { ... §2.10 },
  "immunology": { ... §2.11 },
  "metabolomics_proteomics_epigenetics": { ... §2.12 },
  "neuroimaging_eeg": { ... §2.13 },

  "comorbidities": { ... §2.14 },
  "gestational_birth_data": { ... §2.15 },
  "aces_trauma": { ... §2.16 },
  "longitudinal_biomarkers": { ... §2.17 },
  "planned_exposures": { ... §2.18 },
  "intervention_response_history": { ... §2.19 },

  "user_constraints": {
    "max_monthly_cost_usd": 500,
    "insurance_coverage_constraints": ["...]",
    "geographic_access": "...",
    "preference_against_pharmaceuticals": false,
    "preference_against_invasive_testing": false
  },

  "consent_flags": {
    "research_use_anonymized": false,
    "share_with_clinician_email": null,
    "preconception_ethics_acknowledged": true
  }
}
```

### 2.2 Maternal block

```json
"maternal": {
  "demographics": {
    "age_at_conception_or_now": "integer | null",
    "ethnicity_self_reported": ["array of ISO codes or population descriptors"]
  },
  "pregnancy_history": {
    "infections": [{"name": str, "trimester": int, "fever_days": int, "max_temp_C": float}],
    "medications": [{"name": str, "duration_days": int, "trimester": int, "indication": str}],
    "diet_quality_index": float,
    "bmi_pre_pregnancy": float,
    "weight_gain_kg": float,
    "gestational_diabetes": bool,
    "preeclampsia": bool,
    "iugr_diagnosed": bool,
    "autoimmune_dx": [str],
    "previous_pregnancies": int,
    "previous_autism_children": int,
    "miscarriage_count": int,
    "fertility_treatment": str
  },
  "current_medications": [...],
  "current_supplements": [...]
}
```

Maternal-block PGx- and biomarker-relevant fields are sourced from `genomics` and `hormonal_axes` blocks (§2.7, §2.10), not duplicated here. This avoids data inconsistency.

### 2.3 Paternal block

```json
"paternal": {
  "age_at_conception": int,
  "phenotypic_features": ["sub-clinical autistic traits, ESSENCE features"],
  "current_medications": [...]
}
```

Paternal genetics + biomarkers go through §2.7 / §2.10.

### 2.4 Family history

```json
"family_history": {
  "first_degree_autism": {"count": 1, "phenotype_if_known": "PHE-0003"},
  "first_degree_essence_features": ["ADHD", "OCD", "tic_disorder", "anxiety", "depression"],
  "first_degree_autoimmune": ["maternal_hashimoto", "paternal_t1d"],
  "first_degree_psychiatric": ["bipolar_maternal_aunt", "schizophrenia_paternal_uncle"],
  "second_degree_autism": {"count": 0},
  "consanguinity": false,
  "sibling_phenotypes": [
    {"sibling_id": "anon-1", "sex": "M", "phenotype": "PHE-0001", "confidence": "clinical_dx",
     "intervention_response_summary": "leucovorin: strong response, no regression"}
  ],
  "ethnic_genetic_isolate_membership": null
}
```

### 2.5 Child data (when operating_mode in {young_child, older_child})

```json
"child_data": {
  "current_age_months": 11,
  "sex": "M | F | intersex",
  "anthropometrics": {
    "weight_kg": 9.2,
    "weight_z_for_age_sex": -0.5,
    "height_cm": 73,
    "height_z_for_age_sex": -0.3,
    "bmi": 17.3,
    "bmi_z_for_age_sex": -0.4,
    "head_circumference_cm": 46,
    "head_circumference_z_for_age_sex": +0.8,
    "body_surface_area_m2": 0.45,
    "growth_trajectory_summary": "consistent +1 SD then dropped to -0.5 SD between 6-9 mo (regression flag)"
  },
  "developmental_milestones_status": {
    "motor": "on_track | mild_delay | moderate_delay | severe_delay",
    "social": "...", "language": "...", "cognitive": "...", "adaptive": "...",
    "regression_history": [{"age_months": 18, "domains": ["language", "social"],
                            "post_event": "MMR + concurrent ear infection"}]
  },
  "pubertal_stage_tanner": null,
  "current_diagnoses": [...],
  "current_medications": [...],
  "current_supplements": [...]
}
```

### 2.6 Self data (when operating_mode == adult)

Same shape as `child_data` but self-reported, with adult-specific fields:
```json
"self_data": {
  "current_age_years": 28,
  "sex": "M | F | intersex",
  "anthropometrics": {
    "weight_kg": 65, "height_cm": 168, "bmi": 23.0,
    "waist_cm": 78, "waist_hip_ratio": 0.78,
    "body_fat_pct": 24, "lean_mass_kg": 49.4,
    "body_surface_area_m2": 1.74
  },
  "pubertal_status": "post_pubertal",
  "menstrual_status": {
    "menstruating": true,
    "cycle_phase_at_sampling": "follicular | luteal | ovulatory | menses | postmenopausal | amenorrheic",
    "cycle_day": 14,
    "hormonal_contraception": "none|combined_ocp|progestin_only|iud_hormonal|iud_copper|implant"
  },
  "pregnancy_status": {"pregnant": false, "lactating": false},
  "diagnosis_history": [{"diagnosis": "ASD level 1", "age_at_dx": 26, "clinician_type": "psychologist"}],
  "self_reported_phenotype_features": [...],
  "function_level_self_assessment": {"verbal": ..., "executive": ..., "sensory": ...},
  "current_medications": [...], "current_supplements": [...],
  "self_directed_consent_acknowledged": true
}
```

### 2.6b Subject state at sampling — physiological context for biomarker normalization

Every biomarker datum carries an associated physiological state. The engine cannot reliably interpret a cortisol reading without knowing time-of-day; cannot interpret CRP without knowing recent infection state; cannot interpret a CBC without knowing acute illness. This block captures state at the time biomarkers were collected.

```json
"subject_state_at_sampling": {
  "BIO-0030": {
    "sampling_datetime": "2026-03-15T07:30",
    "fasting_state": "fasting_8plus_hours | fasting_4_8 | non_fasting | breastfed_recent",
    "time_since_last_meal_hours": 12,
    "time_since_last_medication_hours": 14,
    "time_since_last_supplement_hours": 12,
    "circadian_phase": "morning_first_void | morning_post_wake | midday | evening | overnight",
    "sleep_state_prior": "normal_overnight_sleep | sleep_deprived | shift_work | recent_jet_lag",
    "hydration_status": "well_hydrated | mild_dehydration | overhydration | unknown",
    "posture_at_collection": "supine_30min | seated | standing",
    "acute_illness_within_14_days": {"present": false, "type": null, "fever_max_C": null},
    "antibiotics_within_60_days": {"any": false, "agent": null, "duration_days": null},
    "vaccination_within_30_days": {"any": false, "vaccine": null, "days_ago": null},
    "ambient_temperature_C": 22,
    "altitude_m": 50,
    "menstrual_cycle_day_if_applicable": null,
    "pregnancy_trimester_if_applicable": null,
    "lactation_status_if_applicable": null,
    "exercise_within_24h": "none | moderate | intense",
    "stress_event_within_72h": "none | moderate | severe"
  }
}
```

The engine uses this block at pre-processing time (§7 Step 1) to apply state-conditional reference range adjustments before computing z-scores. For example, an 0800 cortisol of 8 µg/dL is normal-low; an 1600 cortisol of 8 is normal-high; a 2300 cortisol of 8 is severely elevated. Without circadian-state context, biomarker interpretation is meaningless.

### 2.7 Genomics — full multi-modal

```json
"genomics": {
  "data_sources": [
    {"actor": "maternal", "type": "23andMe_v5 | WES | WGS | clinical_panel", "date": "...", "lab": "..."}
  ],
  "snps": {
    "maternal": {"rs1801133": {"genotype": "C/T", "confidence": 0.98}, ...},
    "paternal": {...},
    "child": {...}
  },
  "cnvs": {
    "child": [
      {"region": "16p11.2", "type": "deletion", "size_kb": 600, "inheritance": "de_novo",
       "classification": "pathogenic", "evidence_pmid": 18184952}
    ]
  },
  "wes_wgs_rare_variants": {
    "child": [
      {"gene": "SCN2A", "hgvs_c": "c.1234A>T", "hgvs_p": "p.Lys412*", "zygosity": "het",
       "inheritance": "de_novo", "acmg_classification": "pathogenic",
       "clinvar_id": "..."}
    ]
  },
  "mtdna": {
    "maternal": {
      "haplogroup": "H1a",
      "heteroplasmy_variants": [
        {"position": 3243, "ref": "A", "alt": "G", "heteroplasmy_pct": 12.0, "tissue": "blood"}
      ]
    },
    "child": {...}
  },
  "ancestry_genetic_panel": {
    "actor": "child",
    "global_ancestry_proportions": {"EUR": 0.55, "AFR": 0.30, "AMR": 0.10, "EAS": 0.05},
    "method": "ADMIXTURE_K5_1000G_reference"
  }
}
```

**ACMG variant classification** is mandatory for WES/WGS rare variants. VUS variants flow into the engine with reduced weight per §5. The calculator does NOT re-classify variants — it consumes the lab's classification.

### 2.8 Microbiome

```json
"microbiome": {
  "samples": [
    {
      "actor": "child",
      "sample_type": "stool | oral | skin | vaginal_maternal",
      "method": "16S_V3V4 | shotgun_metagenomic",
      "date": "...",
      "lab": "...",
      "alpha_diversity": {"shannon": 2.8, "simpson": 0.85},
      "phylum_relative_abundance": {"Firmicutes": 0.45, "Bacteroidetes": 0.25, "Actinobacteria": 0.10, ...},
      "key_genus_relative_abundance": {
        "Bifidobacterium": 0.02, "Lactobacillus": 0.001, "Clostridium": 0.08,
        "Akkermansia": 0.005, "Faecalibacterium": 0.04, "Prevotella": 0.12, "Bacteroides": 0.18,
        "Candida_albicans_pcr": "elevated"
      },
      "functional_pathways_kegg": {...},
      "scfa_levels": {"butyrate": ..., "propionate": ..., "acetate": ...}
    }
  ]
}
```

Maps to PHE-0004 priors via new §3.10 microbiome priors.

### 2.9 Toxicology / exposome — measured

```json
"toxicology": {
  "heavy_metals": {
    "actor": "child",
    "method": "urine_provoked | urine_unprovoked | hair | blood | nail",
    "results": {
      "mercury": {"value": 8.5, "unit": "ug/g_creat", "z_score_lab": 2.1},
      "lead": {...}, "aluminum": {...}, "cadmium": {...}, "arsenic": {...}
    },
    "date": "...", "lab": "..."
  },
  "mycotoxins": {
    "method": "urine",
    "results": {"ochratoxin_A": ..., "trichothecenes": ..., "aflatoxin_M1": ...,
                "gliotoxin": ..., "zearalenone": ..., "citrinin": ...}
  },
  "glyphosate_urine": {"value": ..., "unit": "ng/mL"},
  "pesticide_metabolites": {...},
  "pfas_serum": {...},
  "phthalate_metabolites_urine": {...},
  "bpa_urine": {...},
  "voc_breath": {...},
  "environmental_history": {
    "residential_history": [{"address_anon": "...", "years": 5, "mold_history": bool,
                             "lead_paint": bool, "near_freeway_km": 0.3, "well_water": bool}],
    "occupational_exposures_parental": [...]
  }
}
```

### 2.10 Hormonal axes

```json
"hormonal_axes": {
  "actor": "child",
  "hpa_axis": {
    "cortisol_diurnal": [{"time": "0800", "value": 18.2, "unit": "ug/dL"},
                         {"time": "1600", "value": 7.5}, {"time": "2300", "value": 2.1}],
    "dhea_s": ..., "acth": ..., "salivary_cortisol_awakening_response": ...
  },
  "hpt_axis": {
    "tsh": ..., "free_t4": ..., "free_t3": ..., "reverse_t3": ...,
    "tpo_antibodies": ..., "thyroglobulin_antibodies": ...
  },
  "sex_hormones": {
    "testosterone_total": ..., "testosterone_free": ..., "shbg": ...,
    "estradiol": ..., "progesterone": ..., "prolactin": ..., "lh": ..., "fsh": ...
  },
  "oxytocin_vasopressin": {
    "plasma_oxytocin": ..., "plasma_avp": ...,
    "csf_avp_when_available": null
  }
}
```

### 2.11 Immunology — beyond the basic biomarkers in v2.0

```json
"immunology": {
  "hla_typing": {
    "actor": "child",
    "class_i": {"a": ["A*02:01", "A*24:02"], "b": [...], "c": [...]},
    "class_ii": {"drb1": ["DRB1*04:01"], "dqb1": [...], "dpb1": [...]}
  },
  "complement": {"c3": ..., "c4": ..., "c1q": ..., "ch50": ..., "ahu_50": ...},
  "cytokine_panel": {
    "il_1b": ..., "il_6": ..., "il_8": ..., "il_10": ..., "il_17a": ..., "il_17f": ...,
    "tnf_alpha": ..., "ifn_gamma": ..., "tgf_beta": ..., "csf_il6_when_available": null
  },
  "immunoglobulins": {"igg_total": ..., "igg_subclasses": {...}, "iga": ..., "igm": ..., "ige_total": ...},
  "specific_iges": {...},
  "lymphocyte_subsets": {"cd3": ..., "cd4": ..., "cd8": ..., "cd19": ..., "cd56_nk": ...,
                        "treg_pct": ..., "th17_pct": ...},
  "nk_cell_function": {"cd107a_degranulation_pct": ...},
  "vaccine_titers": {"measles_iga": ..., "tetanus_igg": ..., "pneumovax_response": ...},
  "autoantibodies": {
    "fraa_blocking": ..., "fraa_binding": ...,
    "mar_panel": {"caspr2": bool, "lasp1": bool, "csde1": bool, "stip1": bool,
                  "y_box_binding_protein_1": bool, "guanine_deaminase": bool, "ndufa6": bool},
    "anti_nmda_r": bool, "anti_caspr2": bool, "anti_lgi1": bool,
    "anti_gad65": bool, "ana": ..., "rf": ..., "anti_ttg": ..., "anti_thyroglobulin": ...,
    "cunningham_panel": {
      "anti_dopamine_d1": ..., "anti_dopamine_d2l": ...,
      "anti_lyso_ganglioside": ..., "anti_tubulin": ...,
      "camkii_activation_pct_baseline": ...
    }
  }
}
```

### 2.12 Metabolomics, proteomics, epigenetics

```json
"metabolomics_proteomics_epigenetics": {
  "metabolomics": {
    "organic_acids_urine": {
      "arabinose": ..., "hphpa": ..., "4_cresol": ..., "succinate": ..., "fumarate": ...,
      "lactate": ..., "pyruvate": ..., "lp_ratio": ..., "ketone_bodies": ...,
      "tartaric_acid": ..., "citramalate": ..., "kynurenate": ..., "quinolinate": ...,
      "kynurenine_tryptophan_ratio": ...
    },
    "amino_acids_plasma": {...},
    "acylcarnitine_panel": {...},
    "sphingolipid_panel": {"ceramides_long_chain": ..., "sphingosine_1p": ...},
    "untargeted_metabolomics_z_scores": {...}
  },
  "proteomics": {
    "olink_inflammation_panel": {...},
    "synaptic_proteins_csf_when_available": null
  },
  "epigenetics": {
    "global_dna_methylation_pct": ...,
    "imprinting_panel": {"h19": ..., "snrpn": ..., "mest": ...},
    "epigenetic_age": {"method": "horvath | hannum | grimage", "age_acceleration_years": ...}
  }
}
```

### 2.13 Neuroimaging + EEG (Phase 5+ optional)

```json
"neuroimaging_eeg": {
  "mri_volumetrics": {
    "amygdala_volume_ml": ..., "amygdala_z_for_age_sex": ...,
    "cerebellum_volume_ml": ..., "cerebellum_z": ...,
    "white_matter_volume_ml": ..., "ventricular_volume_ml": ...
  },
  "mrs_brain_metabolites": {"naa_creatine": ..., "lactate_present": bool, "choline_creatine": ...},
  "dti_connectivity_summary": {"corpus_callosum_fa": ..., "uf_fa": ...},
  "qeeg": {
    "alpha_power_uv2": ..., "gamma_power_uv2": ..., "theta_beta_ratio": ...,
    "ei_imbalance_proxy": ..., "subclinical_epileptiform_activity": bool
  }
}
```

### 2.13b Renal + hepatic function — required for any drug-dosing recommendation

```json
"renal_hepatic_function": {
  "actor": "child | self | maternal",
  "renal": {
    "creatinine_mg_dl": 0.4,
    "egfr_ml_min_per_173m2": 95,
    "egfr_method": "schwartz_pediatric | ckd_epi_2021 | bedside_schwartz",
    "bun_mg_dl": 12,
    "urine_protein_creatinine_ratio": 0.05,
    "ckd_stage": "g1_normal"
  },
  "hepatic": {
    "alt_u_l": 18, "ast_u_l": 22,
    "alp_u_l": 200,
    "ggt_u_l": 12,
    "total_bilirubin_mg_dl": 0.4,
    "direct_bilirubin_mg_dl": 0.1,
    "albumin_g_dl": 4.5,
    "inr": 1.0,
    "ammonia_umol_l": 35
  }
}
```

The PGx filter (§7 Step 19) and intervention dose-recommendation logic depends on renal/hepatic function. A leucovorin dose appropriate at eGFR 95 may be inappropriate at eGFR 40. Without these inputs the calculator falls back to weight-based dosing with a flag that renal/hepatic-adjusted dosing should be confirmed with a clinician.

### 2.14 Comorbidities — clusters that matter for phenotype mapping

```json
"comorbidities": {
  "epilepsy": {"present": bool, "type": "...", "age_onset_months": ..., "controlled_on_medication": bool,
               "medication": "..."},
  "adhd": {"present": bool, "presentation": "inattentive|hyperactive|combined", "subtype": "..."},
  "ocd_anxiety": {"ocd": bool, "anxiety": bool, "panic": bool},
  "mood_disorders": {"depression": bool, "bipolar": bool},
  "tic_disorder": bool,
  "feeding_disorder": {"present": bool, "type": "ARFID|other", "current_diet_diversity_score": ...},
  "sleep_disorder": {"insomnia": bool, "parasomnia": bool, "sleep_apnea": bool,
                     "polysomnography_summary": null},
  "gi_clusters": {
    "chronic_constipation": bool, "chronic_diarrhea": bool, "reflux": bool,
    "abdominal_pain_chronic": bool, "feeding_intolerance": bool
  },
  "atopic_cluster": {"eczema": bool, "asthma": bool, "food_allergies": [str], "ar": bool},
  "mcas_features": {"flushing": bool, "dermographism": bool, "anaphylaxis_history": bool},
  "eds_features": {"hypermobility_beighton_score": ..., "skin_hyperextensibility": bool,
                   "dx_subtype": "..."},
  "pots_features": {"orthostatic_hr_increase_bpm": ..., "syncope_history": bool},
  "vagal_tone_proxy": {"hrv_rmssd_ms": ..., "method": "..."}
}
```

The MCAS–EDS–POTS triad is captured as three correlated input blocks. All three contribute to inflammatory/dysautonomic priors.

### 2.15 Gestational + birth data

```json
"gestational_birth_data": {
  "gestational_age_weeks": 39.5,
  "birth_weight_kg": 3.2,
  "birth_length_cm": 50,
  "head_circumference_cm": 35,
  "apgar_1min": 9, "apgar_5min": 9,
  "delivery_mode": "vaginal | csection_elective | csection_emergency",
  "intrapartum_antibiotics": bool,
  "intrapartum_fever": bool,
  "meconium_aspiration": bool,
  "cord_blood_data": {
    "ph": ..., "lactate": ...,
    "cytokines": {"il_6": ..., "tnf_alpha": ...},
    "vit_d_25oh": ...
  },
  "placental_pathology_summary": {"villitis": bool, "vue": bool, "infarcts": bool, "weight_g": ...},
  "neonatal_period": {
    "nicu_days": 0,
    "phototherapy_required": bool,
    "neonatal_antibiotics": [str],
    "neonatal_jaundice_max_bilirubin": ...,
    "feeding_method_first_6mo": "exclusive_breast | mixed | formula",
    "formula_type_if_used": "...",
    "first_solid_introduction_month": ...
  },
  "vaccinations_administered": [
    {"vaccine": "Hep B", "age_days": 0, "lot": null, "post_vaccination_events": []}
  ]
}
```

### 2.16 ACEs / trauma

```json
"aces_trauma": {
  "ace_score": 2,
  "ace_category_flags": ["physical_neglect", "household_substance_abuse"],
  "current_psychosocial_stressors": ["...]",
  "stable_attachment_figure_present": bool
}
```

ACEs modify HPA / immune / epigenetic priors per §3.13.

### 2.17 Longitudinal biomarkers

```json
"longitudinal_biomarkers": {
  "BIO-0030": [
    {"date": "2025-01-15", "value": 0.32, "unit": "ratio"},
    {"date": "2025-07-20", "value": 0.41, "unit": "ratio"},
    {"date": "2026-02-10", "value": 0.55, "unit": "ratio"}
  ]
}
```

### 2.18 Planned exposures

```json
"planned_exposures": {
  "vaccine_schedule": [
    {"vaccine": "Hep B", "age_months": 0, "decision": "deferred|standard|skipped|alt_schedule",
     "alt_schedule_age_months": null}
  ],
  "medications_planned": [{"name": "...", "indication": "...", "duration_planned": "..."}],
  "environmental_concerns": ["mold", "lead_paint", "high_glyphosate_water"],
  "delivery_plan": {"mode": "vaginal|cesarean", "cord_clamping": "delayed|immediate",
                    "vaginal_seeding_after_csection": bool}
}
```

### 2.19 Intervention response history

```json
"intervention_response_history": [
  {
    "intervention_id": "INT-0001",
    "name": "Leucovorin",
    "dose": "...", "duration_weeks": 12,
    "start_date": "...", "end_date": "...",
    "response_assessment_method": "ATEC | parent_report | clinician_global | biomarker_change",
    "response_score": 0.65,
    "qualitative_summary": "moderate language gains, no GI improvement",
    "adverse_events": [],
    "concurrent_interventions": ["INT-0002"]
  }
]
```

This block is critical for within-phenotype responder modeling (§7.5).

### 2.20 Required vs optional inputs by operating mode

| Input | preconception | pregnancy | young_child | older_child | adult |
|---|---|---|---|---|---|
| Subject sex | required | required | required | required | required |
| Maternal age | required | required | required | required | optional |
| Paternal age | required | required | required | required | optional |
| Family history | required | required | required | required | required |
| Maternal SNPs | recommended | required | required | required | optional |
| Paternal SNPs | recommended | recommended | required | required | optional |
| Subject SNPs | N/A | N/A | recommended | required | required |
| CNVs (child or self) | N/A | N/A | recommended | required | optional |
| WES/WGS rare variants | N/A | N/A | optional | recommended | optional |
| mtDNA panel | recommended | recommended | recommended | recommended | recommended |
| Maternal biomarkers | recommended | required | recommended | optional | N/A |
| Subject biomarkers | N/A | N/A | recommended | required | required |
| Microbiome | optional | optional | recommended | recommended | recommended |
| Toxicology | optional | optional | recommended | recommended | recommended |
| HLA typing | optional | optional | optional | recommended | optional |
| Comorbidities | N/A | N/A | required | required | required |
| Gestational data | N/A | required | required | recommended | optional |
| Pregnancy history | N/A | required | required | required | optional |
| Hormonal axes | optional | recommended | recommended | recommended | recommended |
| Cytokine panel | optional | optional | recommended | recommended | recommended |
| Cunningham Panel | N/A | N/A | conditional | conditional | conditional |
| FRAA panel | optional | recommended | recommended | recommended | recommended |
| ACEs | N/A | N/A | required | required | required |
| Intervention response history | N/A | N/A | optional | recommended | recommended |

"Conditional" = recommended IF the rare-syndrome screening gate or family pattern flags PANS.

**Minimum viable input** for each mode is documented in `validation/minimum_viable_input_per_mode.md`. The calculator runs at any completeness ≥ minimum-viable; output confidence labels degrade proportionally.

### 2.21 Variant ID convention

dbSNP rsIDs preferred. CNVs specified by region + type. Rare WES/WGS variants by HGVS nomenclature with ACMG class. mtDNA variants by position + ref + alt. Each maps to atlas BIO-XXXX or VAR-NNNN via `genetic_id_aliases.csv`.

### 2.22 Schema validation

JSON Schema (Draft 2020-12). Hard validation of types, units, ranges. Soft validation of clinical plausibility (e.g., flagging biologically-impossible biomarker values). Validation failure → explicit error report; partial valid → completeness flags set.

---

## §3 — Prior tables (16 tables in v2.3)

**v2.3 added two prior tables to v2.2's 14**:
- `physiological_state_normalization_table.csv` (§3.13b) — state-conditional reference ranges
- `iatrogenic_exposure_priors.csv` (§3.13c) — medications-as-causes-of-autism

**v2.3 also adds two cross-cutting dimensions atlas-side, to be wired in via Phase 0 work**:

- **Sensory-processing dimension** (resolves audit H-1). DSM-5 Criterion B.4 sensory hyper-/hypo-reactivity is one of autism's most universal features. Currently the atlas has 7 main phenotypes + 4 Walsh biotypes, with no dedicated sensory phenotype. v2.3 adds sensory-processing as a **cross-cutting trait dimension** spanning all 11 phenotype classes rather than a 12th phenotype, because sensory processing patterns map onto multiple etiological phenotypes (e.g., GABA-imbalanced sensory hyper-reactivity vs. mito-vulnerable sensory dampening). Phase 0 work: add sensory-processing biomarker rows + sensory-processing intervention rows; emit a `sensory_processing_pattern` output dimension alongside phenotype posteriors. If atlas analysis later supports a separable etiological-phenotype identity for sensory processing, that would warrant a new PHE-0012 row in the atlas, decided by atlas curator.
- **Sleep-medicine dimension** (resolves audit H-2). Sleep architecture, melatonin pathway (HIOMT, AANAT, MT1/MT2 receptors), circadian disruption, and obstructive sleep apnea all cross-cut autism phenotypes and have specific intervention layers (timed melatonin, light therapy, CPAP, sleep-architecture-aware behavioral interventions). Phase 0 work: add sleep-relevant biomarkers (DLMO, urinary 6-sulfatoxymelatonin, polysomnography summary), melatonin-pathway gene rows in §3.1, sleep intervention rows in §3.5, and a `sleep_disorder_pattern` output dimension.

The 16 prior tables follow.

Each table is a CSV with PMID-grounded rows.

### 3.1 `gene_variant_to_phenotype_priors.csv`

| Field | Type | Description |
|---|---|---|
| variant_id | str | rsID, CNV-region, mtDNA-position, or HGVS-rare |
| variant_class | enum | "snp", "cnv_del", "cnv_dup", "rare_coding", "rare_noncoding", "mtdna" |
| variant_genotype | str | "C/T", "T/T", "homozygous_minor", "del/del", "het", "hom" |
| acmg_class | enum | "pathogenic", "likely_pathogenic", "vus", "likely_benign", "benign", "NA_for_common_snp" |
| phenotype_id | PHE-NNNN | |
| log_odds_shift | float | |
| credal_low | float | |
| credal_high | float | |
| evidence_quality | float (0–1) | |
| primary_pmid | int | |
| sex_modifier_table | str | reference to `variant_sex_modifier_table.csv` |
| ancestry_modifier_table | str | reference to `ancestry_allele_frequency_table.csv` |
| effect_size_metric | enum | "OR", "log_OR", "d", "regression_beta" |
| n_underlying | int | |
| pathway_membership | [str] | which pathways this variant participates in |
| notes | str | mechanism note |

**Phase 1 seed (~80 variants)**: SFARI Tier 1+2 syndromic genes (TSC1/2, PTEN, FMR1, MECP2, CHD8, ADNP, SCN1A, SCN2A, SHANK3, NRXN1, NLGN3/4, CNTNAP2, SYNGAP1) + biotyping panel (MTHFR C677T/A1298C, COMT V158M, MAO-A VNTR, CBS variants, FOLR1 variants, FUT2 secretor, ApoE, CYP1A2/2D6/2C19/3A4, GSTM1/T1, TCN2, BHMT, AHCY, MTRR, GAD1, GABRB3) + autism-relevant CNVs (16p11.2, 22q11.2, 15q11-13, 1q21.1, 7q11.23, 3q29) + FMR1 CGG-repeat thresholds + mtDNA tRNA variants (3243, 8344, 8993).

### 3.2 `biomarker_to_mechanism_priors.csv`

| Field | Type | Description |
|---|---|---|
| biomarker_id | BIO-NNNN | atlas biomarker |
| threshold_type | enum | "above", "below", "ratio_high", "ratio_low", "z_score_above", "z_score_below" |
| threshold_value | float | |
| threshold_unit | str | |
| reference_lab_normal | json | {"low": ..., "high": ..., "lab": "..."} |
| age_modifier_table | str | for age-varying normal ranges |
| sex_modifier_table | str | for sex-varying normal ranges |
| mechanism_id | MEC-NNNN | atlas mechanism |
| activation_shift | float | |
| credal_low | float | |
| credal_high | float | |
| evidence_quality | float | |
| primary_pmid | int | |
| notes | str | |

### 3.3 `exposure_to_phenotype_priors.csv`

| Field | Type | Description |
|---|---|---|
| exposure_id | str | controlled vocabulary |
| exposure_window | enum | "preconception", "trimester_1/2/3", "intrapartum", "neonatal", "0_6mo", "6_24mo", "2_6yr", "6_12yr", "12plus_yr", "lifetime_chronic" |
| dose_or_intensity | str | "any", "low", "moderate", "high", "chronic" |
| phenotype_id | PHE-NNNN | |
| log_odds_shift | float | population-average shift |
| conditional_on_susceptibility | str | "always" | susceptibility_profile_id |
| log_odds_shift_in_subgroup | float | shift WITHIN profile (Hannah Poling number) |
| credal_low | float | |
| credal_high | float | |
| evidence_quality | float | |
| primary_pmid | int | |
| measurement_proxy | str | reference to toxicology biomarker if available |
| notes | str | |

Hannah Poling pattern: low/null `log_odds_shift` (population-average), substantial `log_odds_shift_in_subgroup` (subgroup-conditional). Resolved per §5.

### 3.4 `susceptibility_modifier_table.csv` — biotype profiles

| Field | Type | Description |
|---|---|---|
| susceptibility_profile_id | str | |
| profile_definition | json | {variants, biomarkers, microbiome_features, hla_alleles, family_features, thresholds} |
| profile_logic | enum | "all_required", "k_of_n", "weighted" |
| profile_threshold_k | int | |
| phenotype_id | PHE-NNNN | |
| baseline_log_odds_shift | float | |
| credal_low | float | |
| credal_high | float | |
| primary_evidence | json | [{"pmid": ..., "design": ..., "n": ...}] |
| competing_profile_ids | [str] | |
| notes | str | |

**Phase 1 seed profiles (~20)** — extends v2.0's 12:
- `mito_vulnerable_classic` → MTHFR T/T + low free carnitine + elevated lactate → PHE-0002 +0.65
- `mito_mtdna_3243_blood_heteroplasmy_15plus` → maternal MT-TL1 m.3243A>G blood heteroplasmy ≥15% (proxy for higher brain heteroplasmy) → PHE-0002 +0.85 (per MELAS literature; Goto 1990 PMID 2102678, plus penetrance papers)
- `mito_mtdna_3243_blood_heteroplasmy_5_to_15` → m.3243A>G blood heteroplasmy 5–15% → PHE-0002 +0.45 (lower-but-non-zero penetrance band)
- `mito_mtdna_8344_heteroplasmy_5plus` → MT-TK m.8344A>G (MERRF) blood heteroplasmy ≥5% → PHE-0002 +0.65 (MERRF literature)
- `mito_mtdna_8993_heteroplasmy_70plus` → MT-ATP6 m.8993T>G (NARP/Leigh) heteroplasmy ≥70% → PHE-0002 +1.20 (high penetrance threshold)
- `mito_mtdna_8993_heteroplasmy_30_to_70` → m.8993T>G heteroplasmy 30–70% → PHE-0002 +0.55 (NARP-spectrum band)

Per-variant rows replace the v2.2 lumped row. Each row carries a `tissue_at_measurement` field (typically blood); muscle/CSF heteroplasmy when available is preferred and triggers a separate higher-confidence row. **Tissue caveat**: blood heteroplasmy systematically under-represents brain heteroplasmy for tRNA variants (3243, 8344) — output reasoning trace explicitly notes this when scoring is heavily blood-tissue-driven.
- `cfd_classic` → FRAA-positive + low CSF 5-MTHF or low RBC folate → PHE-0001 +1.20
- `cfd_genetic` → FOLR1 pathogenic + low RBC folate → PHE-0001 +1.50
- `walsh_undermethylator` → PHE-0008 +0.85 (evidence_quality: 0.35; credal interval wide [+0.30, +1.40])
- `walsh_overmethylator` → PHE-0009 +0.70 (evidence_quality: 0.30; credal interval wide [+0.20, +1.20])
- `walsh_pyroluria` → PHE-0010 +0.75 (evidence_quality: 0.30; credal interval wide [+0.25, +1.25])
- `walsh_cuzn_imbalance` → PHE-0011 +0.65 (evidence_quality: 0.40; credal interval [+0.25, +1.05])

**Walsh-biotype evidence-quality caveat (resolves audit H-10)**: the four Walsh biotypes (PHE-0008–0011) are derived from clinical-experience-based frameworks with limited peer-reviewed RCT support. Numerical log-odds shifts above are best-estimate point values; the credal intervals are deliberately wide and the evidence_quality fields are deliberately ≤0.40 to signal that. Until independent replication accumulates, Walsh-biotype-driven recommendations should be tagged in output as confidence_label ≤ MODERATE.
- `pans_pandas_setup` → PHE-0003 +0.95
- `mcas_classic` → PHE-0003 +0.80
- `mcas_eds_pots_triad` → all three triad clusters present → PHE-0003 +1.10 (super-additive)
- `gi_microbiome_dysbiosis_classic` → PHE-0004 +0.70
- `microbiome_clostridia_dominant` → elevated HPHPA + Clostridium spp >0.10 + 4-cresol elevated → PHE-0004 +0.90
- `microbiome_low_diversity_post_abx` → Shannon <2.0 + early antibiotic exposure → PHE-0004 +0.70
- `mtor_syndromic_setup` → TSC1/2 or PTEN + macrocephaly → PHE-0005 +1.50
- `fmr1_full_or_premutation` → FMR1 CGG ≥55 → PHE-0006 +1.80
- `gaba_imbalance_setup` → seizure history + paradoxical benzo response → PHE-0007 +0.85
- `hla_drb1_autoimmune_setup` → HLA-DRB1 autoimmune-risk allele + family autoimmune → PHE-0003 +0.40
- `extreme_male_brain` (Baron-Cohen) → high gestational testosterone + male sex → soft prior shift across phenotypes
- `female_phenotype_pattern` → female sex + masking + internalizing presentation + late dx → recognition modifier

### 3.5 `intervention_efficacy_per_phenotype.csv`

| Field | Type | Description |
|---|---|---|
| intervention_id | INT-NNNN | |
| phenotype_id | PHE-NNNN | |
| age_window | enum | preconception, pregnancy, 0_6mo, 6_24mo, 2_6yr, 6_12yr, 12_18yr, 18plus |
| sex_modifier | enum | "all", "male_only", "female_only", "differential" |
| efficacy_estimate | float | probability of clinically-meaningful improvement |
| efficacy_credal_low | float | |
| efficacy_credal_high | float | |
| nnt | int or NA | |
| effect_size_d | float or NA | |
| time_to_response_weeks | int | |
| recommendation_type | enum | START / CONSIDER / MONITOR / DONT_START / AVOID / STOP_WITH_CLINICIAN |
| cost_tier | enum | "low" (<$50/mo), "moderate" ($50–500/mo), "high" ($500–5000/mo), "very_high" (>$5000) |
| primary_pmids | [int] | |
| pgx_safety_table | str | reference to `pgx_drug_gene_table.csv` for contraindications |
| within_phenotype_responder_predictors | [str] | references to predictors that further stratify response |
| notes | str | |

### 3.6 `sibling_phenotype_priors.csv`

| Field | Type | Description |
|---|---|---|
| sibling_phenotype_id | PHE-NNNN | |
| target_phenotype_id | PHE-NNNN | |
| log_odds_shift | float | within-family clustering |
| credal_low | float | |
| credal_high | float | |
| sex_concordance_modifier | float | additional shift if same-sex siblings |
| primary_pmid | int | |
| notes | str | |

### 3.7 `ancestry_allele_frequency_table.csv`

| Field | Type | Description |
|---|---|---|
| variant_id | str | |
| ancestry_population | str | gnomAD population code (afr, amr, asj, eas, fin, nfe, sas, oth) + admix-aware |
| minor_allele_frequency | float | |
| effect_size_modifier | float | population-specific scalar (1.0 = same as reference) |
| credal_low | float | |
| credal_high | float | |
| primary_pmid | int | |
| notes | str | |

For admixed individuals, weighted combination of population-specific frequencies based on global ancestry proportions from §2.7.

### 3.8 `pgx_drug_gene_table.csv` — pharmacogenomics

| Field | Type | Description |
|---|---|---|
| drug_or_intervention_id | str | INT-NNNN or generic drug name |
| gene | str | CYP2D6, CYP2C19, CYP3A4, MTHFR, COMT, etc. |
| phenotype_class | enum | "poor_metabolizer", "intermediate", "normal", "rapid", "ultrarapid" |
| variant_definition | json | which genotype combinations define this PGx phenotype |
| recommendation_modifier | enum | "contraindicated", "use_with_caution", "dose_reduce_50pct", "dose_increase_50pct", "no_change", "alternative_form_preferred" |
| log_odds_efficacy_modifier | float | shift in expected response |
| log_odds_adverse_event_modifier | float | shift in expected AE |
| primary_pmid | int | CPIC guideline ID or PMID |
| notes | str | |

**Phase 1 seed**: CPIC guideline-based rows for stimulants (CYP2D6), atomoxetine, antipsychotics (used cautiously per §3.13c framing), methylated B-vitamins (COMT, MTHFR — overmethylator caution with high-dose methyl folate / methyl-B12), folate forms (MTHFR), naltrexone, statins, opioids, CYP1A2-cleared agents, anesthetic agents.

**Note on SSRIs / SNRIs**: SSRIs are NOT in the standard intervention layer. They appear in two places: (1) the iatrogenic-exposure prior table (§3.13c) when gestationally or pediatrically exposed, where they raise autism phenotype risk — particularly PHE-0007 (GABA/Cl⁻ imbalance) where serotonergic perturbation interacts with E:I imbalance, and PHE-0008/0009 (Walsh methylation biotypes) where serotonergic medications produce paradoxical responses; (2) STOP_WITH_CLINICIAN flagging when an autistic individual is currently prescribed an SSRI for a non-autism indication (depression, OCD, anxiety) — in which case the calculator outputs PGx safety profile + flags paradoxical-response risk + suggests discussion with prescriber about lower-dose alternatives, alternative-class medications, or non-pharmaceutical alternatives matched to phenotype. SSRIs are never recommended as treatment for core autism features (Williams 2013 Cochrane review found no benefit).

### 3.9 `microbiome_to_phenotype_priors.csv`

| Field | Type | Description |
|---|---|---|
| microbiome_feature_id | str | "shannon_diversity_below_X", "clostridium_relative_above_X", "akkermansia_below_X", etc. |
| feature_type | enum | "alpha_diversity", "phylum_ratio", "genus_abundance", "species_specific", "functional_pathway", "scfa" |
| threshold_value | float | |
| sample_type | enum | "stool", "oral", "skin", "vaginal_maternal" |
| age_modifier_table | str | (microbiome composition is highly age-dependent) |
| phenotype_id | PHE-NNNN | |
| log_odds_shift | float | |
| credal_low | float | |
| credal_high | float | |
| evidence_quality | float | |
| primary_pmid | int | |
| notes | str | |

### 3.10 `toxicology_to_phenotype_priors.csv`

| Field | Type | Description |
|---|---|---|
| toxicology_feature_id | str | "urine_mercury_z_above_2", "urine_glyphosate_above_X", etc. |
| sample_type | enum | "urine", "blood", "hair", "nail", "breath" |
| measurement_method | enum | "provoked", "unprovoked", "challenge", "passive" |
| threshold_value | float | |
| threshold_unit | str | |
| age_modifier_table | str | |
| phenotype_id | PHE-NNNN | |
| log_odds_shift | float | |
| conditional_on_susceptibility | str | many toxicology priors are subgroup-conditional |
| log_odds_shift_in_subgroup | float | |
| credal_low | float | |
| credal_high | float | |
| evidence_quality | float | |
| primary_pmid | int | |
| notes | str | |

### 3.11 `hormonal_axis_priors.csv`

| Field | Type | Description |
|---|---|---|
| hormone_marker_id | str | "cortisol_awakening_response_blunted", "tsh_above_X", "free_t3_below_X", "testosterone_z_above_2_in_F", "oxytocin_below_X" |
| sample_type | enum | "blood", "saliva", "urine", "csf" |
| timing | enum | "morning", "evening", "diurnal_curve", "post_stimulation" |
| threshold_value | float | |
| age_sex_modifier_table | str | |
| phenotype_id | PHE-NNNN | |
| log_odds_shift | float | |
| credal_low | float | |
| credal_high | float | |
| primary_pmid | int | |
| notes | str | |

### 3.12 `comorbidity_priors.csv` — epilepsy, MCAS-EDS-POTS, ADHD/OCD/anxiety, GI, atopic

| Field | Type | Description |
|---|---|---|
| comorbidity_pattern_id | str | "epilepsy_present", "mcas_eds_pots_triad_2plus", "atopic_triad", "gi_chronic_constipation_plus_diarrhea_alternating" |
| pattern_definition | json | |
| target_phenotype_id | PHE-NNNN | |
| log_odds_shift | float | |
| credal_low | float | |
| credal_high | float | |
| primary_pmid | int | |
| notes | str | |

### 3.13 `aces_trauma_modifier_table.csv`

| Field | Type | Description |
|---|---|---|
| ace_pattern | str | "score_above_4", "physical_neglect_present", "household_substance_abuse" |
| modifies_target | enum | "phenotype_prior", "biomarker_interpretation", "intervention_efficacy" |
| target_id | str | PHE-NNNN, BIO-NNNN, or INT-NNNN |
| modifier_value | float | |
| credal_low | float | |
| credal_high | float | |
| primary_pmid | int | |
| notes | str | |

### 3.13b `physiological_state_normalization_table.csv` — full state-conditional reference ranges

For every biomarker, the engine needs to know how reference range varies with subject state. This is the single most-impactful new prior table for clinical accuracy.

| Field | Type | Description |
|---|---|---|
| biomarker_id | BIO-NNNN | |
| reference_range_dimension | enum | "age", "sex", "weight_kg", "weight_z", "bmi_z", "tanner_stage", "menstrual_phase", "pregnancy_trimester", "lactation", "fasting_state", "time_of_day", "posture", "altitude_m", "acute_illness", "post_vaccine_window", "post_antibiotic_window", "renal_function_stage", "hepatic_function_stage", "ethnicity_population" |
| dimension_value | str | numeric range or categorical |
| reference_low | float | |
| reference_high | float | |
| reference_unit | str | |
| reference_lab_method | str | LC-MS, ELISA, etc. — same biomarker varies by method |
| z_score_correction_factor | float | multiplicative correction to apply when computing z-scores |
| credal_low | float | |
| credal_high | float | |
| primary_pmid | int | source for this reference range |
| notes | str | |

Phase 1 seed: ~150 rows covering every biomarker that has documented age-, sex-, or state-dependent reference ranges. Highest-priority biomarkers: cortisol (diurnal + age + sex), GH (pulsatile + diurnal + age + Tanner), all sex hormones (Tanner + menstrual phase + pregnancy + age), thyroid panel (age — neonatal vs pediatric vs adult differ substantially), CBC (age), CRP (acute illness), ferritin (acute phase reactant), ESR (age + sex), creatinine (age + muscle mass), eGFR (age + sex + ancestry), vitamin D (season + skin pigmentation + latitude), homocysteine (age + sex + B-vitamin status), all hormones in females (cycle phase critical), lactate (post-exercise, fasting, sample handling), uric acid (age + sex + diet), all biomarkers in pregnancy, all biomarkers in lactation.

Engine pre-processing (§7 Step 1): for every input biomarker, look up the state-matched reference range, compute state-conditional z-score, and ONLY THEN apply the `biomarker_to_mechanism_priors.csv` rules. Skipping this step means the engine treats a healthy mid-luteal estradiol as elevated, a normal pediatric ALP as elevated, a post-vaccine CRP as elevated, etc. — producing systematic false-positive activations and unreliable phenotype priors.

### 3.13c `iatrogenic_exposure_priors.csv` — medications and procedures with autism-risk evidence

Medications and medical procedures with documented autism-risk evidence get a dedicated prior table separate from environmental exposures. This is the table that captures **medications-as-causes-of-autism**, an axis the v2.1 spec under-developed.

| Field | Type | Description |
|---|---|---|
| iatrogenic_id | str | controlled vocabulary |
| iatrogenic_class | enum | "ssri", "snri", "antipsychotic", "stimulant", "benzodiazepine", "anticonvulsant_specific", "general_anesthesia", "opioid", "fluoroquinolone", "ppi_chronic", "acetaminophen", "antibiotic_class", "vaccine_specific", "anti_d_immunoglobulin", "labor_induction_oxytocin", "csection_class", "phototherapy", "supplemental_oxygen", "iv_iron_dextran", "topical_corticosteroid_chronic" |
| specific_agent | str | e.g., "fluoxetine", "valproate", "thalidomide", "mtx", "topiramate" |
| exposure_window | enum | matches §3.3 windows |
| dose_or_intensity | str | |
| target_phenotype_id | PHE-NNNN | |
| log_odds_shift | float | population-average shift |
| conditional_on_susceptibility | str | susceptibility profile if subgroup-conditional |
| log_odds_shift_in_subgroup | float | |
| credal_low | float | |
| credal_high | float | |
| evidence_quality | float | |
| primary_pmids | [int] | |
| countervailing_evidence_pmids | [int] | studies with null or opposite findings — preserves contested status |
| mechanism_id | MEC-NNNN | proposed mechanism |
| recommendation_for_avoidance_window | str | "always", "preconception_only", "pregnancy_only", "T1_T2_T3", "neonatal_only", "0_24mo_only" |
| recommendation_when_clinically_indicated | enum | "use_anyway", "use_lowest_effective_dose", "use_alternative_class", "consider_deferral", "absolute_contraindication" |
| notes | str | |

**Phase 1 seed rows (~50)** — focused on highest-evidence iatrogenic exposures:

- **SSRIs** — gestational exposure has CONTESTED association with autism risk. Sources supporting: Croen 2011 *Arch Gen Psychiatry* (PMID 21727247), Rai 2013 *BMJ* (PMID 23604083), Boukhris 2016 *JAMA Pediatr* (PMID 26660917). Countervailing (in `countervailing_evidence_pmids`): Brown 2017 *JAMA* sibling-control (PMID 28418480) and Sujan 2017 *JAMA* sibling-control (PMID 28418479) — both substantially attenuate the association after controlling for familial confounding by maternal psychiatric illness. SSRIs in autistic children for core autism features have NO evidence base per Williams 2013 Cochrane review (PMID 23959778). **Mechanism**: serotonin's role as a neurodevelopmental morphogen is biologically plausible but the proposed PHE-specific mechanisms are *proposed* not directly demonstrated; mark `evidence_quality: 0.40`, `mechanism_status: proposed`. **Recommendation type**: CONSIDER alternatives in pregnancy when safer alternatives exist for the maternal indication; if clinically essential for severe maternal depression with suicidality, use lowest effective dose. Never AVOID without prescriber consult — untreated severe maternal depression has its own substantial fetal/neonatal risks. Status: contested.
- **SNRIs** — similar evidence base; CONTESTED. Treat similarly to SSRIs.
- **Valproate (VPA)** — gestational exposure → autism risk substantially elevated, with clean teratogenic mechanism (HDAC inhibition, neural-tube + brain-development effects). Sources: Christensen 2013 *JAMA* (PMID 23613074), Bromley 2010 *Epilepsia* early cognitive (PMID 20633039), multiple replications. Evidence_quality: 0.85. Recommendation: absolute contraindication in pregnancy when alternatives are available. This is the highest-evidence iatrogenic exposure in the table.
- **Acetaminophen (paracetamol)** — gestational + early-life exposure → autism / ADHD risk is CONTESTED with strong evidence on both sides. Supporting: Liew 2014 (PMID 24566677), Ji 2020 *JAMA Psychiatry* (PMID 31664451), Bauer 2021 *Nat Rev Endocrinol* consensus statement (PMID 34556849, signed by 91 researchers). Countervailing (in `countervailing_evidence_pmids`): **Ahlqvist 2024 *JAMA*** (PMID 38592388, Swedish nationwide sibling-control n=2.48M, found null association after sibling-control adjustment). The sibling-control design is the strongest available for confounding by indication and substantially attenuates the association. Mechanism (proposed): glutathione depletion + endocannabinoid disruption + oxidative stress in mito-vulnerable subset. Evidence_quality: 0.40 (downgraded from v2.2's higher implicit weight given Ahlqvist 2024). Recommendation: CONSIDER avoiding chronic prophylactic use in pregnancy; use lowest effective dose for shortest duration when fever or pain treatment is medically indicated. Not in same evidence tier as valproate.
- **Thalidomide** — historical, severe.
- **Misoprostol** — gestational exposure association.
- **Antipsychotics (risperidone, aripiprazole, etc.)** — used for autism irritability/aggression but NOT core autism; major side-effect profile (metabolic syndrome, EPS, tardive dyskinesia, sedation, prolactin elevation). Recommendation type when prescribed: STOP_WITH_CLINICIAN if used for core autism features (no evidence base); CONSIDER alternatives if used for aggression.
- **Fluoroquinolone antibiotics (cipro, levo)** — mito-toxicity; avoid in mito-vulnerable subset; FDA black-box warning. Recommendation: AVOID especially in PHE-0002 children.
- **Macrolide antibiotics in early life** — microbiome disruption + QTc effects; some evidence for autism risk via microbiome perturbation.
- **General anesthesia exposure in pregnancy or first 3 years** — multiple studies show modest association; mitochondrial-toxicity mechanism for halogenated agents (sevoflurane, desflurane). Recommendation: defer non-urgent procedures in mito-vulnerable subset.
- **Repeated/early antibiotic exposure (lifetime <2 years cumulative)** — microbiome perturbation, PHE-0004 risk.
- **Proton pump inhibitors (chronic)** — B12 + magnesium depletion, microbiome perturbation, especially in pregnancy.
- **Pitocin (synthetic oxytocin) labor induction** — contested; some evidence for endogenous oxytocin system perturbation.
- **Anti-D immunoglobulin (RhoGAM) historical** — historical thimerosal-containing formulations; current formulations differ.
- **Hep B birth dose** — kept as contested per CLAUDE.md §1; conditional risk in mito-vulnerable subset (Hannah Poling pattern).

**Engine treatment**: iatrogenic priors flow into the same conflict-resolution and credal aggregation as environmental exposures (§6, §7). The distinction is presentational and policy-relevant: iatrogenic exposures populate the avoidance bundle for pregnancy / pediatric use under conditions where safer alternatives exist; they populate the STOP_WITH_CLINICIAN list when currently being administered.

### 3.14 `pathway_burden_table.csv`

| Field | Type | Description |
|---|---|---|
| pathway_id | str | "mtor", "methylation", "mito_oxphos", "glutamatergic", "gabaergic", "immune_inflammatory", "microbiome_axis", "synaptic_function" |
| variant_or_feature_id | str | which input contributes to this pathway |
| weight_in_pathway | float | |
| primary_pmid | int | |

Used to compute per-pathway burden scores in §7.4. Pathways with high burden flag enriched mechanism activity beyond simple per-variant log-odds sum.

---

## §4 — Rare-syndrome screening gate

Before generic phenotype assignment, the calculator runs a deterministic syndromic-autism screening gate. If a row matches, the calculator outputs a "syndrome detected" flag and routes to syndrome-specific output.

**Syndromes screened (~25)**:
- Fragile X (FMR1 CGG ≥200) → PHE-0006 dominant
- Rett (MECP2 pathogenic) → distinct trajectory; many interventions inappropriate
- TSC (TSC1/TSC2 pathogenic + tuberous sclerosis features) → mTOR pathway dominant
- PTEN hamartoma syndrome → mTOR pathway, macrocephaly
- Phelan-McDermid (22q13.3 deletion / SHANK3) → severe phenotype
- Angelman (15q11-13 maternal del / UBE3A) → distinct trajectory
- Smith-Magenis (17p11.2)
- Williams (7q11.23)
- 22q11.2 deletion syndrome
- 16p11.2 deletion / duplication
- 1q21.1 deletion / duplication
- 15q11-13 duplication (maternal origin) → autism with severe sensory features
- Cornelia de Lange
- CHARGE syndrome
- ATR-X
- MECP2 duplication
- Inborn errors of metabolism with autism features:
  - PKU (untreated)
  - Adenylosuccinate lyase deficiency
  - Creatine deficiency syndromes (GAMT, AGAT, SLC6A8)
  - Cerebral folate deficiency genetic forms (FOLR1)
  - Mitochondrial diseases (POLG, MERRF, MELAS via mtDNA)
  - Smith-Lemli-Opitz (DHCR7)
  - Urea cycle disorders
  - Lysosomal storage diseases with autism features

**Output for syndromic match**:
- Top phenotype probabilities heavily weighted toward syndrome-specific phenotype
- Intervention bundle adjusted for syndrome-specific contraindications (e.g., MECP2 → caution with serotonergics)
- Avoidance bundle includes syndrome-specific avoidances
- Explicit "this child has a syndromic form of autism; non-syndromic intervention guidance applies with caveats" framing
- Referral to syndrome-specific specialist clinic recommended

This gate prevents the calculator from running generic phenotype assignment on syndromic cases, where the genetic finding alone explains most of the phenotype.

---

## §5 — Baseline phenotype prevalence + base rate

### 5.1 Per-phenotype baseline prevalence

(Same table as v2.0 §4.1 — refined in Phase 4.)

### 5.2 General-population autism base rate

~2.5% (CDC 2023 ADDM data, varying by region and ascertainment). Used when no family history. Family history with ≥1 first-degree autistic individual elevates base rate to ~10–20% (Sandin 2014 sibling recurrence) for next child in same family.

### 5.3 Sex-stratified base rates

Male:female ~4:1 in clinical samples; closer to 3:1 in research samples; closer to 2:1 in samples that explicitly screen for female phenotype patterns. Calculator uses 3:1 as default with ascertainment-bias acknowledgment.

### 5.4 Recursive update with intervention response history

For families with intervention response data (§2.19), Bayesian update of phenotype posterior given response. Strong leucovorin response → upweight PHE-0001 posterior. Strong bumetanide response → upweight PHE-0007. Etc.

---

## §6 — Conflict resolution policy

### 6.1 Resolution algorithm — formal specification

For each (subject, phenotype Φ) pair, the engine collects all candidate prior rows from §3 and resolves conflicts via the following **deterministic** algorithm. Rows are processed in canonical sort order (by `prior_row_id` ascending), so output is byte-identical across runs.

**Step 1 — Row collection.** Collect every row from §3 that names this phenotype as a target, where (a) the row's modality input is present in this case, AND (b) the row's threshold/condition is met by this case's data.

**Step 2 — Deduplication by (modality_anchor × phenotype_id).** Define `modality_anchor` as the smallest unit of evidence: one of {variant_id, biomarker_id, exposure_id, microbiome_feature_id, toxicology_feature_id, hormonal_marker_id, comorbidity_pattern_id, sibling_phenotype_id, susceptibility_profile_id, iatrogenic_id}. For each (modality_anchor, phenotype_id) group containing ≥2 rows:
- If exactly one row is `conditional_on_susceptibility` AND the family's susceptibility profile matches that condition: keep that row, discard the population-average row(s).
- Else if all rows are population-average: aggregate them via inverse-variance weighting weighted by `evidence_quality`.
- Else if multiple subgroup-conditional rows match different overlapping profiles: choose the row with the most-specific profile match (tiebreak: highest evidence_quality, then lowest prior_row_id).

This step prevents both (a) double-counting subgroup + population rows for the same anchor, and (b) double-counting overlapping subgroup profiles.

**Step 3 — Susceptibility profile rows (§3.4) are non-additive with their constituent variant/biomarker rows.** When a `susceptibility_profile_id` row matches and the constituent variants/biomarkers in `profile_definition` would also independently match their own §3.1/§3.2 rows: the profile row REPLACES the constituent rows. This is documented explicitly in `profile_definition.replaces_constituent_rows: true` (default for biotype profiles where the combined effect was measured). When a profile row says `replaces_constituent_rows: false`, the profile bonus is additive on top of the constituent contributions.

**Step 4 — Sum log-odds shifts.** After deduplication, the surviving rows are summed in canonical sort order:
```
total_shift_φ = Σᵢ (row_i.log_odds_shift × row_i.evidence_quality)
```
Summation is performed in stable-sorted-key order to guarantee floating-point reproducibility (see §7.3.1).

**Step 5 — Propagate uncertainty via Walley IDM credal aggregation (§7.1).**

**Step 6 — Conflict flagging.** If max(log_odds_shift) − min(log_odds_shift) across surviving rows for this phenotype exceeds 0.50, emit a `conflict_flag` entry to the reasoning trace identifying the disagreeing rows.

### 6.2 Cross-modality concordance bonus

When ≥3 distinct modalities (from {genetic, biomarker, microbiome, toxicology, hormonal, immunology, family_history, comorbidity}) all contribute net-positive log-odds shifts to the same phenotype, apply a deterministic concordance bonus to the credal point estimate (not to the bounds):

```
concordance_bonus = min(0.10, 0.02 × (n_concordant_modalities − 2))
```

Capped at 0.10. Applied to point estimate only, not bounds. Does not apply when n_concordant_modalities < 3.

### 6.3 Subgroup-supersedes-population rule (formal restatement)

This rule is now embedded in §6.1 Step 2. For a single (modality_anchor, phenotype) pair where the atlas contains both a population-average row α and a subgroup-conditional row β with profile Π:
- If family matches Π: applied_shift = β (with credal interval β_low, β_high)
- Else: applied_shift = α (with credal interval α_low, α_high)

**This is per-anchor, not global.** The same family may match Π for one exposure (use β) but not match a different profile Π′ for a different exposure (use that exposure's α). Each anchor resolves independently.

This is the explicit Hannah Poling resolution. Not double-counting — population-average and subgroup studies answer different questions; only one applies per anchor.

---

## §7 — Calculation engine

### 7.1 Walley IDM credal aggregation — canonical s=2

The engine uses **Walley's Imprecise Dirichlet Model** with concentration parameter **s = 2** for the canonical scoring path. This is fixed at v2.3 release and changes only on a major version bump. Output is fully deterministic at s=2; there is no random sampling on the canonical path.

For each phenotype Φ:
- **Lower bound**: sum of (log_odds_low × evidence_quality) across surviving rows after §6 dedup, in canonical sort order
- **Upper bound**: sum of (log_odds_high × evidence_quality) across the same rows, in canonical sort order
- **Point estimate**: deterministic median computed via 1024-point quadrature over the IDM-implied distribution (no random sampling; quadrature points and weights specified in `idm_quadrature_table.csv`, locked at v2.3)
- Apply logistic transform: P_low = σ(lower + concordance_bonus_lower=0), P_point = σ(median + concordance_bonus), P_high = σ(upper + concordance_bonus_upper=0)

**Sensitivity sweep over s ∈ {1, 2, 5, 10} is a diagnostic side-product**, not part of canonical output. Sensitivity outputs go to a separate diagnostic file with its own random-seed lock; they never affect canonical phenotype_posteriors.

### 7.1.1 Numerical determinism (resolves audit C-4)

Byte-identical output across runs and across platforms requires:
- **Library version pin**: `numpy==1.26.4`, `scipy==1.12.0`, `pandas==2.2.0` documented in `engine_lockfile.txt`. Engine refuses to run with any other library version.
- **Stable summation order**: all sums over rows performed via `sorted(rows, key=lambda r: r.prior_row_id)` first, then sequential addition. No parallel reductions, no `numpy.sum(axis=...)` on unsorted arrays.
- **Float precision**: all intermediate calculations in `numpy.float64`; final output rounded to 6 decimal places via `round(x, 6)` for display, full precision retained internally.
- **No NaN propagation**: any NaN encountered raises an explicit error rather than silently propagating.
- **Quadrature lock**: `idm_quadrature_table.csv` ships with engine; never recomputed at runtime.
- **Cross-platform regression test**: byte-identical canonical output verified across (Linux x86-64, macOS ARM64) at every release.

### 7.1.2 No random elements on canonical path

To eliminate any ambiguity: the canonical scoring path contains zero random sampling. The IDM aggregation, the concordance bonus, the EIG ranking, the responder model, the trajectory predictor — all use closed-form or fixed-quadrature computation. Random sampling appears only in:
- Sensitivity sweeps (separate diagnostic output, fixed seed)
- Phase 6 field-test variance estimation (separate research output, fixed seed)
- Bootstrap confidence intervals for validation metrics (separate validation output, fixed seed)

None affect canonical engine output.

### 7.2 Top-level pseudocode

```python
def compute_personalized_risk(input_json, *, engine_version="session4_v2.3") -> dict:
    """Deterministic. No LLMs in math. Stable sort by ID. Reproducible."""
    validate_input_schema(input_json)

    # Step 0 — Rare-syndrome screening gate (§4)
    syndrome_match = run_syndrome_screening_gate(input_json)
    if syndrome_match:
        return syndromic_output(input_json, syndrome_match)

    # Step 1 — Full physiological-state normalization
    #   - State-conditional reference range lookup per biomarker via
    #     physiological_state_normalization_table.csv (§3.13b)
    #   - z-scores computed against age × sex × Tanner × menstrual-phase × pregnancy ×
    #     fasting-state × time-of-day × posture × altitude × acute-illness ×
    #     post-vaccine-window × post-antibiotic-window × renal-stage × hepatic-stage ×
    #     ancestry-population reference range
    #   - Anthropometric z-scoring (weight, height, BMI, head circumference) for age + sex
    #   - Ancestry-calibrated allele frequencies for genetic variants
    #   - Sex-specific genetic effect-size selection
    #   - Body-surface-area calculation for dosing
    normalized_input = pre_process(input_json)

    # Step 2 — Genetic priors: SNPs + CNVs + WGS rare + mtDNA, all sex-and-ancestry-calibrated
    genetic_priors = compute_genetic_priors(
        snps=normalized_input["genomics"]["snps"],
        cnvs=normalized_input["genomics"]["cnvs"],
        rare_variants=normalized_input["genomics"]["wes_wgs_rare_variants"],
        mtdna=normalized_input["genomics"]["mtdna"],
        sex=normalized_input["subject_sex"],
        ancestry=normalized_input["subject_ancestry"]
    )

    # Step 3 — Biomarker priors → mechanism activations (longitudinal-aware)
    mechanism_activations = compute_mechanism_activations(
        biomarkers=normalized_input["biomarker_collection"],
        longitudinal=normalized_input["longitudinal_biomarkers"],
        age_context=infer_age_context(normalized_input),
        sex=normalized_input["subject_sex"]
    )

    # Step 4 — Microbiome priors
    microbiome_shifts = compute_microbiome_phenotype_shifts(
        normalized_input["microbiome"], age=infer_age(normalized_input)
    )

    # Step 5 — Toxicology priors
    toxicology_shifts = compute_toxicology_phenotype_shifts(
        normalized_input["toxicology"], susceptibility_context=...
    )

    # Step 6 — Hormonal axis priors
    hormonal_shifts = compute_hormonal_phenotype_shifts(
        normalized_input["hormonal_axes"], sex=normalized_input["subject_sex"]
    )

    # Step 7 — Immunology + HLA priors
    immunology_shifts = compute_immunology_priors(
        normalized_input["immunology"]
    )

    # Step 8 — Comorbidity cluster priors
    comorbidity_shifts = compute_comorbidity_priors(normalized_input["comorbidities"])

    # Step 9 — Susceptibility profile match (non-additive priors)
    profile_matches = match_susceptibility_profiles(
        genetic_priors, mechanism_activations, microbiome_shifts, immunology_shifts,
        normalized_input["family_history"]
    )

    # Step 10 — Sibling phenotype priors
    sibling_shifts = apply_sibling_priors(
        normalized_input["family_history"]["sibling_phenotypes"],
        sex_concordance=normalized_input["subject_sex"]
    )

    # Step 11 — Exposure priors (gestational, postnatal, planned), with subgroup conditioning
    exposure_shifts = compute_exposure_shifts(
        gestational=normalized_input["gestational_birth_data"],
        postnatal_history=normalized_input.get("child_data", {}),
        planned=normalized_input["planned_exposures"],
        susceptibility_context=profile_matches,
        toxicology_measured=normalized_input["toxicology"]
    )

    # Step 12 — ACEs / trauma modifiers
    aces_modifiers = compute_aces_modifiers(normalized_input["aces_trauma"])

    # Step 13 — Pathway burden analysis (§7.4)
    pathway_burdens = compute_pathway_burdens(
        genetic_priors, mechanism_activations, microbiome_shifts
    )

    # Step 14 — Cross-modality concordance scoring (§6.2)
    concordance_scores = compute_concordance_scores(
        genetic_priors, mechanism_activations, microbiome_shifts, toxicology_shifts,
        immunology_shifts, hormonal_shifts, sibling_shifts, exposure_shifts, comorbidity_shifts
    )

    # Step 15 — Credal aggregation per phenotype (Walley IDM)
    phenotype_posteriors = {}
    for phe_id in PHENOTYPE_IDS:
        baseline = baseline_phenotype_prevalence(phe_id, normalized_input["family_history"],
                                                  sex=normalized_input["subject_sex"])
        contributing_rows = collect_rows(... all sources for phe_id ...)
        contributing_rows = conflict_resolution(contributing_rows)
        ci_low, point, ci_high = walley_idm_aggregate(baseline, contributing_rows, s=2,
                                                       concordance=concordance_scores[phe_id])
        phenotype_posteriors[phe_id] = {
            "point": point, "credal_low": ci_low, "credal_high": ci_high,
            "drivers": top_contributing_rows(contributing_rows, k=5),
            "modality_breakdown": modality_breakdown(contributing_rows)
        }

    # Step 16 — CDR state assignment + transitions (§7.6)
    cdr_state = assign_cdr_state(mechanism_activations, immunology_shifts, microbiome_shifts)
    cdr_transitions = predict_cdr_transitions(cdr_state, normalized_input)

    # Step 17 — Functional outcome trajectory (§7.7)
    trajectory = predict_functional_trajectory(
        phenotype_posteriors, normalized_input,
        intervention_response_history=normalized_input["intervention_response_history"]
    )

    # Step 18 — Within-phenotype responder model (§7.5)
    responder_predictions = compute_responder_predictions(
        phenotype_posteriors, normalized_input, top_intervention_candidates
    )

    # Step 19 — Intervention ranking (life-stage + age + sex + PGx-filtered)
    intervention_bundle = rank_interventions(
        phenotype_posteriors=phenotype_posteriors,
        responder_predictions=responder_predictions,
        pgx_filter=load_pgx_filter(normalized_input["genomics"]),
        age_window=infer_age_window(normalized_input),
        sex=normalized_input["subject_sex"],
        existing_csrs=load_csrs_scores(),
        intervention_efficacy_per_phenotype=load_iep()
    )

    # Step 20 — Avoidance bundle
    avoidance_bundle = rank_avoidances(
        phenotype_posteriors, normalized_input,
        susceptibility_context=profile_matches,
        toxicology_measured=normalized_input["toxicology"]
    )

    # Step 21 — "Test these next" — EIG-ranked, cost-weighted (§7.8)
    next_biomarkers = rank_next_biomarkers_by_eig(
        current_inputs=normalized_input,
        phenotype_posteriors=phenotype_posteriors,
        biomarker_to_mechanism_priors=load_bmm_priors(),
        cost_table=load_biomarker_cost_table(),
        user_constraints=normalized_input.get("user_constraints", {})
    )

    # Step 22 — Feasibility-constrained bundle (§7.9)
    feasible_bundle = filter_by_feasibility(
        intervention_bundle, avoidance_bundle, next_biomarkers,
        constraints=normalized_input.get("user_constraints", {})
    )

    # Step 23 — Open-question flagging
    open_questions = flag_open_questions(normalized_input, phenotype_posteriors)

    # Step 24 — Reasoning trace + clinician handoff
    return {
        "phenotype_posteriors": phenotype_posteriors,
        "phenotype_ranking": rank_phenotypes(phenotype_posteriors),
        "pathway_burdens": pathway_burdens,
        "cdr_state": cdr_state,
        "cdr_transitions": cdr_transitions,
        "functional_trajectory": trajectory,
        "responder_predictions": responder_predictions,
        "intervention_bundle": intervention_bundle,
        "avoidance_bundle": avoidance_bundle,
        "next_biomarkers_ranked": next_biomarkers,
        "feasible_bundle": feasible_bundle,
        "open_questions": open_questions,
        "reasoning_trace": build_trace(),
        "input_completeness": compute_completeness_score(normalized_input),
        "engine_version": engine_version,
        "atlas_version": ATLAS_VERSION,
        "calibration_anchor": "INT-0001 = 83.35",
        "syndromic_flag": False,
        "computed_at": now_iso()
    }
```

### 7.3 Determinism guarantees (high-level summary)

See §7.1.1 for full numerical-determinism specification. Summary: stable sort by ID throughout, no LLMs in calculation, idempotent, library version pinned, byte-identical output verified across (Linux x86-64, macOS ARM64) at every release.

### 7.4 Pathway burden analysis — anchored normalization (resolves audit H-9)

Each variant / biomarker / microbiome feature is tagged with pathway memberships in `pathway_burden_table.csv`. For each pathway:

```
raw_burden(pathway) = Σ (input_contribution × pathway_weight × evidence_quality)
burden_score(pathway) = 10 × min(1.0, raw_burden / pathway_anchor_value)
```

`pathway_anchor_value` is **fixed per pathway at v2.3 release** in `pathway_anchor_values.csv` and represents the raw_burden expected when ALL strongly-implicated atlas variants/biomarkers/features for that pathway are present at full evidence quality. Anchor values are NOT recomputed across atlas revisions — they're locked at major version release. This guarantees burden_score interpretability is stable across atlas growth.

Pathways tracked: mTOR, methylation, mito-OXPHOS, glutamatergic, GABAergic, immune-inflammatory, microbiome-axis, synaptic-function.

A child with `mtor` burden 8.5 has 85% of the maximum mTOR-pathway loading the atlas can detect. This is interpretable independently of how many new mTOR variants the atlas adds in future versions.

### 7.5 Within-phenotype responder model (resolves audit M-6)

For each top-ranked intervention candidate within phenotype Φ, predict P(response | this child's full profile) via deterministic shifts loaded from a dedicated table:

**`responder_predictor_priors.csv`** — every responder shift is PMID-grounded:

| Field | Type |
|---|---|
| intervention_id | INT-NNNN |
| phenotype_id | PHE-NNNN |
| predictor_type | enum: "biomarker", "variant", "comorbidity", "biomarker_combination" |
| predictor_definition | json: {biomarker_id, threshold} or {variant_id, genotype} or {pattern} |
| log_odds_response_shift | float |
| credal_low | float |
| credal_high | float |
| evidence_quality | float |
| primary_pmid | int |
| n_underlying | int |
| notes | str |

**Algorithm**:

1. Start with phenotype-conditional efficacy P(response | Φ) from §3.5 (with credal interval).
2. Convert to log-odds: logit_baseline = log(p/(1-p)).
3. For each matching responder predictor row from `responder_predictor_priors.csv`, sum its log-odds shift weighted by evidence_quality (in canonical sort order per §7.1.1).
4. Apply PGx modifiers from §3.8 (`log_odds_efficacy_modifier`, `log_odds_adverse_event_modifier`).
5. Apply intervention-response-history Bayesian update from §2.19: prior responses to this intervention or mechanistically-related interventions update the log-odds.
6. Sum total log-odds shift; logistic transform back to P(response).
7. Walley IDM credal aggregation across all contributing rows for credal interval.
8. Output P(response | this child) with credal_low, credal_high.

Phase 1 seed targets ~30 high-evidence responder-predictor rows for the top 10 interventions across the top phenotypes. Example target rows (each PMID-grounded in seed):

- INT-0001 (leucovorin) × PHE-0001 with FRAA blocking ≥1.0 OD/mL → log-odds shift derived from Frye 2018 RCT subgroup analysis
- INT-0001 × PHE-0001 with MTHFR T/T → log-odds shift derived from Frye CFD work
- INT-0024 (bumetanide) × PHE-0007 with high baseline NKCC1/KCC2 ratio proxy → from Lemonnier work
- INT-0008 (5-MTHF) × PHE-0009 (overmethylator) → NEGATIVE log-odds shift (paradoxical worsening) per Walsh

Numerical shift values in seed rows are derived from published subgroup data; never hard-coded to fictitious numbers.

### 7.6 CDR state assignment (Naviaux Cell Danger Response) — concrete decision tree

This section is **EXPERIMENTAL** in v2.3 and produces an output flagged as `experimental: true`. CDR is conceptually strong but operational consensus does not yet exist; the engine encodes one operationalization for v2.3 and version-tags it for forward compatibility.

**State definitions:**

| CDR state | Operational definition (deterministic boolean conjunctions) |
|---|---|
| **Acute** | (≥2 acute-phase reactants elevated: CRP, ferritin, ESR) AND (mtDNA heteroplasmy OR lactate Z ≤ +1.5) AND (≤90 days since identifiable trigger event in input) |
| **Sub-acute** | (chronic cytokine elevation: ≥2 of {IL-6, TNF-α, IL-1β, IL-17A} above sex-age-z +1.5) AND (lactate Z > +1.5 OR L:P ratio > 25) AND (90–365 days since trigger OR no clear trigger but ≥6 months symptom duration) |
| **Chronic** | (depleted glutathione: GSH:GSSG ratio < 0.5) AND (mitochondrial markers: ≥2 of {acylcarnitine abnormalities, organic acid mito markers, lactate Z > +1.0}) AND (≥365 days symptom duration) AND (chronic low-grade inflammation: hs-CRP > 1.0 mg/L OR neopterin elevated) |
| **Resolved** | (declining cytokine trend across ≥2 longitudinal samples) AND (improving glutathione redox) AND (improving mtDNA-related markers OR stable) AND (improving developmental/symptomatic trajectory in §2.5/§2.6) |
| **Indeterminate** | input insufficient to assign any state above |

When ≥2 states co-qualify (rare), the most-active state takes precedence: Acute > Sub-acute > Chronic > Resolved.

**Transition probabilities** are NOT computed in v2.3 (insufficient validation data). v2.3 outputs the CURRENT state and an `experimental: true` flag; transition probabilities are deferred to v3.0 once Phase 6 longitudinal data accumulates. Removing the inadequately-supported transition output prevents misuse.

**Validation**: in calibration cases, CDR state assignment is checked qualitatively against documented case state rather than against quantitative posterior — pending Phase 6 data.

### 7.7 Functional outcome trajectory — qualitative bands only in v2.3 (resolves audit H-8)

Quantitative trajectory predictions (numeric IQ, age-of-language) require Phase 6 field data not yet available. v2.3 outputs **qualitative bands only**, with `experimental: true` flag, to prevent liability from fictitious precision.

**v2.3 trajectory output:**

| Domain | Output |
|---|---|
| Regression risk window | `risk_band: high | moderate | low | not_applicable_age` + `window_age_months: [start, end]` (drawn from phenotype-specific evidence, not numerical-modeled) |
| Verbal trajectory | `band: typical_track | mild_concern | high_concern | nonverbal_trajectory_likely | uncertain` |
| Adaptive functioning | `band: typical_track | mild_concern | high_concern | uncertain` |
| Intervention-mediated trajectory shift | `expected_direction: improvement_likely | stabilization_likely | continued_decline_concern | uncertain` per top intervention |

**No numerical IQ predictions.** No numerical age-of-language predictions. v3.0 may add numerical predictions once field data validates them.

### 7.8 EIG with cost weighting (unchanged from v2.2)

Expected information gain per biomarker, divided by cost-tier, produces EIG-per-dollar ranking. User-supplied `max_monthly_cost_usd` filters output.

### 7.9 Feasibility-constrained bundle

Constrained optimization: maximize total expected impact subject to user constraints (max_monthly_cost, insurance_coverage, geographic_access, preference_against_pharmaceuticals, preference_against_invasive_testing). Output: alternative bundle respecting constraints, presented alongside the unconstrained bundle.

### 7.10 Intervention ranking utility function (resolves audit C-6)

Within each (phenotype, life-stage) cell, candidate interventions are ranked by a deterministic utility function:

```
U(intervention | family) =
    α · responder_p_point
  + β · efficacy_credal_low_phenotype
  + γ · csrs_normalized_to_unit
  + δ · (1 − cost_tier_score)
  − ε · pgx_risk_score
  − ζ · interaction_risk_score
```

with **fixed coefficients** locked at v2.3 release in `intervention_utility_weights.csv`:

| Term | Coefficient | Rationale |
|---|---|---|
| α (responder_p_point) | 0.40 | Within-phenotype responder probability is the most clinically relevant signal once phenotype is fixed |
| β (efficacy_credal_low) | 0.20 | Lower-bound efficacy guards against credal-interval overconfidence |
| γ (csrs_normalized) | 0.20 | Existing CSRS captures atlas-wide consensus signal not embedded in phenotype-specific layers |
| δ (1−cost_tier_score) | 0.10 | Cost penalty: cost_tier_score = {low: 0.0, moderate: 0.3, high: 0.7, very_high: 1.0} |
| ε (pgx_risk_score) | 0.05 | PGx risk: 0 if pgx_check passed, 0.5 if caution, 1.0 if contraindicated |
| ζ (interaction_risk_score) | 0.05 | Drug-drug, drug-supplement, supplement-supplement interaction count for current regimen |

`csrs_normalized_to_unit = csrs / 100`. All terms produce values in [0, 1]. Final U is in [-0.10, 1.00] roughly. Coefficients chosen so that responder probability dominates, low-bound efficacy + CSRS provide the next-largest pull, and cost / PGx / interaction penalties are tie-breakers — never the dominant factor.

**Coefficient lock**: changing α…ζ is a MAJOR version bump and requires re-running all calibration cases + verifying calibration anchor.

**PGx-contraindicated interventions** (`pgx_check == "contraindicated"`) are removed from the bundle entirely with rationale entry; they don't compete on utility. PGx-caution interventions remain in the bundle with the ε penalty applied.

---

## §8 — Recommendation typology

(Same six types as v2.0, plus one addition.)

| Type | Definition |
|---|---|
| START | Begin this intervention; high-confidence evidence; expected meaningful benefit |
| CONSIDER | Discuss with clinician; moderate evidence; benefit likely in subgroup |
| MONITOR | Track this biomarker / symptom; intervention not yet warranted |
| DONT_START | Do not start this intervention; evidence weak or risk profile poor for this child |
| AVOID | Affirmatively avoid this exposure |
| STOP_WITH_CLINICIAN | Currently-prescribed item with concerning subgroup-conditional evidence; review with prescribing clinician |
| TITRATE | Currently-active intervention; consider dose / form change based on PGx or biomarker response |

Every recommendation carries (type, confidence_label, cost_tier, time_to_response_estimate, evidence_pmids).

---

## §9 — Output structure

### 9.1 Top-level JSON output

```json
{
  "case_id": "...",
  "computed_at": "...",
  "engine_version": "session4_v2.3",
  "atlas_version": "v2.0_scored",
  "calibration_anchor": "INT-0001 = 83.35",
  "input_completeness": 0.78,
  "operating_mode": "young_child",
  "subject_sex": "M",
  "subject_age_months": 11,

  "syndromic_flag": false,
  "syndromic_match": null,

  "phenotype_posteriors": {
    "PHE-0001": {
      "point": 0.18, "credal_low": 0.08, "credal_high": 0.35,
      "primary_drivers": [
        {"source": "rs1801133 T/T", "shift": +0.30, "credal": [+0.05, +0.55], "pmid": 17560158, "modality": "genetic"},
        {"source": "FRAA blocking 1.2 OD/mL", "shift": +0.55, "credal": [+0.35, +0.75], "pmid": 22230883, "modality": "biomarker"}
      ],
      "modality_breakdown": {"genetic": 0.30, "biomarker": 0.55, "family_history": 0.20, "other": 0.05},
      "rationale": "...",
      "confidence_label": "MODERATE"
    },
    ...
  },

  "phenotype_ranking": ["PHE-0001", "PHE-0003", "PHE-0002", ...],

  "pathway_burdens": {
    "mtor": 2.1, "methylation": 7.8, "mito_oxphos": 5.2, "glutamatergic": 3.0,
    "gabaergic": 2.5, "immune_inflammatory": 6.5, "microbiome_axis": 4.8, "synaptic_function": 3.2
  },

  "cdr_state": {
    "current": "sub_acute",
    "confidence": 0.72,
    "transition_probabilities_12mo": {
      "acute": 0.05, "sub_acute": 0.40, "chronic": 0.30, "resolved": 0.25
    },
    "transition_probabilities_with_intervention_bundle_12mo": {
      "acute": 0.02, "sub_acute": 0.20, "chronic": 0.10, "resolved": 0.68
    }
  },

  "functional_trajectory": {
    "verbal": {"point_age_months_meaningful_phrases": 36, "credal_low": 28, "credal_high": 48},
    "regression_risk_window": {"start_age_months": 14, "end_age_months": 24, "risk_p": 0.25,
                                "risk_p_with_intervention_bundle": 0.10},
    "iq_trajectory_2yr": {"point": +5, "credal_low": -5, "credal_high": +18}
  },

  "responder_predictions": {
    "INT-0001_leucovorin": {"p_response": 0.85, "credal": [0.65, 0.95],
                            "vs_phenotype_baseline": "+0.20 above baseline"},
    "INT-0006_ldn": {...}
  },

  "intervention_bundle": {
    "preconception": [...],
    "pregnancy": [...],
    "postnatal_general": [...],
    "postnatal_phenotype_specific": {
      "PHE-0001": [
        {
          "intervention_id": "INT-0001",
          "name": "Leucovorin",
          "recommendation_type": "START",
          "efficacy_per_top_phenotype": 0.65,
          "responder_prediction": 0.85,
          "responder_credal": [0.65, 0.95],
          "nnt": 3,
          "time_to_response_weeks": 8,
          "csrs": 83.35,
          "cost_tier": "moderate",
          "pgx_check": "passed",
          "rationale": "FRAA blocking 1.2 OD/mL; family CFD pattern; MTHFR T/T",
          "primary_pmids": [29760485],
          "confidence_label": "HIGH"
        }
      ]
    }
  },

  "avoidance_bundle": { ... },

  "next_biomarkers_ranked": [
    {
      "biomarker_id": "BIO-0080",
      "name": "Cunningham Panel",
      "expected_information_gain": 0.42,
      "estimated_cost_usd": 950,
      "eig_per_dollar": 0.00044,
      "rationale": "Family pattern suggests PANS overlay; testing would shift PHE-0003 posterior",
      "lab": "Moleculera"
    }
  ],

  "feasible_bundle": { ... alternative bundle filtered by user constraints ... },

  "open_questions": [
    {"question": "mtDNA heteroplasmy status unknown", "phenotype_impact": "PHE-0002", "magnitude": "high"},
    {"question": "Microbiome composition not measured", "phenotype_impact": "PHE-0004", "magnitude": "moderate"}
  ],

  "rare_syndrome_rule_out_checklist": [
    {"syndrome": "FXS", "screened": true, "result": "negative"},
    {"syndrome": "Rett", "screened": true, "result": "negative"},
    ...
  ],

  "reasoning_trace": [...],

  "clinician_handoff_summary": "...markdown 1–2 pager...",

  "model_card_ref": "session4_v2.3_model_card.md"
}
```

### 9.2 Human-readable markdown report

Auto-generated. Sections:

1. Header (case ID, date, engine version, atlas version, completeness, operating mode, subject sex, syndromic flag).
2. Top phenotype risks — ranked, credal intervals, modality breakdown, top drivers.
3. Pathway burden summary.
4. CDR state + transition probabilities.
5. Functional trajectory.
6. Pre-conception action plan (if applicable).
7. Pregnancy action plan (if applicable).
8. Postnatal action plan — life-stage-segmented, ranked by responder prediction × efficacy, PGx-filtered, with rec-type tags.
9. Specific avoidances.
10. "Test these next" with EIG, cost, EIG-per-dollar.
11. Feasibility-constrained alternative bundle.
12. Open questions.
13. Rare-syndrome rule-out checklist.
14. Clinician handoff (1–2 page).
15. Disclaimer.
16. Model card link.

---

## §10 — Confidence labels

(Identical to v2.0.) HIGH / MODERATE / LOW / EXPLORATORY based on evidence convergence.

---

## §11 — "Test these next"

(Identical to v2.0 §11 with cost-weighted addition per §7.8.)

---

## §12 — Atlas integration

### 12.1 What we reuse

- CSRS scoring engine
- All evidence_links + sources
- Biomarker-mechanism, biomarker-phenotype, biomarker-intervention, intervention-mechanism, intervention-phenotype, mechanism-phenotype edges
- Hypothesis-mechanism, hypothesis-hypothesis edges
- Combinations
- Walsh biotypes
- All 7 phenotype deep-dives + condition subgroup deep-dives (MCAS, PANS, etc.)

### 12.2 What we add

- 16 new prior tables (§3) — 14 from v2.1 plus `physiological_state_normalization_table.csv` (§3.13b) and `iatrogenic_exposure_priors.csv` (§3.13c)
- New `personalized_risk.py` engine
- New `genetic_id_aliases.csv`
- New `pgx_drug_gene_table.csv`
- New `physiological_state_normalization_table.csv` (state-conditional reference ranges)
- New `iatrogenic_exposure_priors.csv` (medications-as-causes-of-autism)
- Input/output JSON schemas (with full subject_state_at_sampling block + anthropometrics + renal/hepatic function)
- Markdown report templater
- Sub-agent verification harness
- Model card document
- Threat model document
- Rare-syndrome screening gate logic
- CDR state classifier
- Pathway burden table
- Functional-trajectory predictor
- State-conditional biomarker normalization layer

### 12.3 Layer separation maintained

Layer 1 + 2 untouched. Layer 3 consumes deterministically.

---

## §13 — Validation strategy

### 13.1 Calibration cases — 60 minimum target for v2.3 release (resolves audit H-16, H-17)

v2.3 expands the calibration set from 30 to **60 minimum**, with a coverage matrix specifying minimum cases per (operating_mode × phenotype) cell:

- Each of the 5 operating modes × 11 phenotypes = 55 cells. Minimum 1 case per cell where the mode-phenotype combination is biologically meaningful (some cells are degenerate, e.g., FXS in Mode A preconception is not a meaningful combination since it's a known genetic test).
- Plus ≥5 multi-phenotype cases (children with co-occurring phenotype patterns).
- Plus ≥5 negative-control cases (no expected phenotype signal).

**Calibration-pass criterion (formal)** — each calibration case must have an associated `validation/calibration_cases/case_NN.yaml` file with these required fields:

```yaml
case_id: case_011_hannah_poling
description: "..."
operating_mode: young_child
input_completeness: full
expected_top_phenotype: PHE-0002
expected_phenotype_p_floor: 0.50  # PHE-0002 posterior must be ≥ this
expected_phenotype_p_ceiling: 0.90  # and ≤ this
expected_top_3_intervention_ids: [INT-0011, INT-0012, INT-0006]  # any 2 of 3 must appear
expected_top_3_avoidance_ids: [...]
expected_recommendation_types:
  INT-0011: START
expected_syndromic_flag: false
expected_cdr_state: sub_acute  # qualitative; experimental
expected_open_questions_includes: ["mtDNA heteroplasmy panel"]
notes: "From 2008 federal Vaccine Court ruling profile"
```

A calibration case PASSES when:
- Top phenotype matches `expected_top_phenotype` exactly
- Posterior point estimate is within [`p_floor`, `p_ceiling`]
- ≥2 of 3 expected interventions appear in top-3 of bundle
- Recommendation types match for tested interventions
- No unexpected syndromic_flag

Below the original 30 cases are listed; an additional 30 covering remaining (mode × phenotype) cells are to be authored in Phase 1.



**Mode A (preconception) — 5 cases**
1. Two parents both MTHFR T/T, no current pregnancy, no autistic children → preconception methylation support
2. Mother PCOS + insulin resistance + paternal age 45 → metabolic optimization
3. Family with one PHE-0001 child planning second pregnancy → preconception leucovorin
4. Family with one PHE-0005 (TSC) child + maternal TSC mosaicism → genetic counseling first
5. Two healthy parents, no family history → baseline / no specific actions

**Mode B (pregnancy) — 5 cases**
6. Pregnant FRAA+, MTHFR T/T → high-dose 5-MTHF + leucovorin discussion
7. Pregnant T2 fever + Tylenol use, mito-vulnerable family → PHE-0002/0003 elevation
8. Pregnant Cunningham-positive, autoimmune family → PHE-0003
9. Pregnant with measured high mycotoxin urine → mold remediation + binding agents
10. Pregnant healthy, no family history → baseline

**Mode C (young child) — 8 cases**
11. **Hannah Poling** profile (mito-vulnerable + post-vaccine regression)
12. 11-month-old, family with PHE-0001 sibling, soft signs → preventive 5-MTHF
13. 18-month-old PANS classic post-strep → NSAID + antibiotic + IVIG discussion
14. 22-month-old regression post-MMR + family autoimmune → anti-inflammatory + mito support
15. 14-month-old GI-prominent + eczema + chronic stooling → GI-microbiome workup
16. 12-month-old healthy, no family history → baseline
17. 18-month-old with measured elevated mercury + mito family pattern → chelation contraindicated, alternative detox
18. 15-month-old female with regression + family female-phenotype masking → female-pattern-aware workup

**Mode D (older child / adolescent) — 8 cases**
19. **Frye 2018 FRAA+ responder profile** → leucovorin
20. **Walsh undermethylator** → methyl donors
21. **Walsh pyroluria** → B6 + zinc + GLA
22. **TSC-related autism** → mTOR-aware management
23. **FXS in autism** → FXS-specific framework
24. **Bumetanide-responsive E:I imbalance** → bumetanide
25. **Chronic CDR / Naviaux suramin candidate** → CDR-resolution intervention discussion
26. **22q11.2 deletion** → syndromic gate triggers; specific management

**Mode E (adult / late-diagnosis) — 4 cases**
27. 28-year-old female, late dx, masking pattern, anxiety/OCD → female-pattern + Walsh undermethylator workup
28. 35-year-old male, autistic burnout, CDR-chronic features → CDR-resolution interventions
29. 22-year-old non-binary, mast-cell pattern + EDS-POTS → MCAS-EDS-POTS triad management
30. 40-year-old male, autism + epilepsy comorbidity + mito features → mito + anti-seizure-aware management

For each: documented expected output, calibration-pass criterion = top phenotype matches AND top-3 interventions overlap with documented successful pathway.

### 13.2 Failure-mode coverage matrix

For each case test:
- Full input → baseline expected output
- Partial input → graceful degradation, completeness flag drops
- Conflicting input → conflict-resolution log + reasonable final output
- Adversarial extreme values → bounded output, no crashes
- Missing critical fields → completeness drops, no false high-confidence
- Multi-sibling input → sibling priors aggregated correctly
- Consanguinity flag → recessive priors strengthen
- Mosaic-only → "consider mosaic-aware sequencing" flag
- Cross-modality conflict (genetic says X, microbiome says Y) → both contribute, reasoning trace shows
- Wrong-ancestry calibration test → using EUR-default priors on AFR family triggers warning + ancestry-specific rerun
- PGx contraindication test → drug recommended for phenotype but contraindicated by PGx → DONT_START with rationale
- Female-phenotype recognition test → female-pattern symptoms not getting auto-deprioritized
- Syndromic gate test → FXS-positive child gets syndromic output, not generic phenotype assignment

### 13.3 Negative-control cases

5 cases with no known autism etiology + 3 cases with healthy family + neutral biomarkers + neutral microbiome + neutral toxicology → low aggregate phenotype risk; no false-positive bundles.

### 13.4 Sensitivity analysis

For each case vary: input completeness, IDM s parameter ∈ {1, 2, 5, 10}, evidence-quality threshold, ancestry calibration, sex assumption.

Verify: posteriors shift in expected direction; credal intervals widen with less data; top recommendations stable; recommendation flips flagged.

### 13.5 Calculator-specific calibration anchor

**Anchor case**: Hannah Poling (case 11). Anchor expected: PHE-0002 posterior point ≥ 0.50, credal interval excludes < 0.20. Stability rule: across versions, anchor must remain within ±0.10 of locked baseline.

**Calibration anchor scope clarification (resolves audit H-2):**

The calibration anchor `INT-0001 (leucovorin) CSRS ≥ 80` lives at **Layer 2 (global CSRS scoring)** — it constrains the global atlas-wide intervention scoring engine, not per-case recommendation output from the Layer 3 personalized risk calculator. These are different computations producing different output types and must not be conflated:

| Layer | Computation | Output | Calibration constraint |
|---|---|---|---|
| Layer 1 | Causal graph aggregation | Hypothesis/mechanism/phenotype evidence weights | None (engine doesn't score) |
| Layer 2 | CSRS scoring engine (`run_scoring_v20.py`) | Global intervention scores 0–100 | INT-0001 must score ≥ 80 (currently 83.35) |
| Layer 3 | Per-case `personalized_risk.py` | Per-family recommendation_type (START / CONSIDER / MONITOR / DONT_START / AVOID / STOP_WITH_CLINICIAN / TITRATE) and within-phenotype responder probabilities | Calibration anchor case must produce expected per-case output (Hannah Poling → PHE-0002 top + mito cocktail) |

**The Hannah Poling case correctly emits `INT-0001 (leucovorin): DONT_START` in its per-case output** because the case lacks FRAA evidence and the family's susceptibility profile is mito-vulnerable (PHE-0002), not cerebral folate deficiency (PHE-0001). This per-case DONT_START is fully consistent with the Layer 2 global CSRS calibration of INT-0001 ≥ 80 — the global score reflects atlas-wide evidence quality and aggregate clinical utility across all stratified subgroups in which leucovorin is indicated, while the per-case output reflects individualized recommendation logic for one specific family.

Engine implementations must:
- Compute Layer 2 CSRS independently of any per-case calculator runs.
- Verify calibration anchor `INT-0001 ≥ 80` after every scoring-engine modification.
- Verify Hannah Poling case output (PHE-0002 top + DONT_START INT-0001 + START mito-cocktail INT-0011/0012/0017/0019/0020) at every Layer 3 release.
- Never demote Layer 2 INT-0001 score based on Layer 3 per-case DONT_START outputs.

### 13.6 External validation benchmarks — tiered (resolves audit H-18)

**Tier 1 (must achieve before v1.0 release)** — these benchmarks use published case profiles where individual-level expected outcomes are documented; do not require external dataset access:
- **Frye-published FRAA+ leucovorin responder cases** — published in Frye 2018 RCT and follow-ups; calculator on these case profiles should produce START INT-0001 with HIGH confidence.
- **Cunningham Panel positive PANS cases** — published Cunningham/Swedo case series; calculator on these profiles should produce PHE-0003 top + IVIG/antibiotic interventions.
- **Walsh lab biotype published case examples** — calculator on these should produce matching PHE-0008/9/10/11 assignment with appropriate Walsh-protocol interventions.
- **Lemonnier bumetanide responder profiles** — calculator on these should flag PHE-0007 + CONSIDER bumetanide.
- **Hannah Poling federal ruling case profile** — calibration anchor case (§13.5).

**Tier 2 (post-release if data access obtained, requires IRB and data-use agreements)** — these require external dataset access not yet arranged:
- 23andMe autism PRS comparison → calculator's top phenotype direction-of-association consistency.
- SPARK cohort published phenotype distributions.
- ABCD study cohort patterns (NIMH NDA access required).
- Spectrum 10K patterns when available.

Tier 1 must pass for any v1.0 release. Tier 2 is a post-release continuous-improvement target; failure to achieve Tier 2 does not block v1.0 release but is documented in model card limitations.

### 13.7 Sub-agent audit

Independent audit pass per spec correctness, PMID grounding, edge cases, adversarial inputs, calibration case match.

### 13.8 Real-family field testing (Phase 6)

3 / 6 / 12 / 24-month follow-up. Predictions vs outcomes refine priors.

### 13.9 Validation against unknown-unknowns

Run the calculator on the 30 calibration cases plus an additional 100 anonymized real-family cases (with consent) at two time points (T0 baseline, T+12 mo follow-up). Quantify: prediction-vs-outcome correlation, calibration plot (predicted P vs observed frequency), responder-prediction accuracy, intervention-bundle adoption rate, intervention-bundle outcome.

---

## §14 — Model card

Required sections per release:
- Intended use (decision-support; NOT diagnosis, NOT population policy, NOT selective-pregnancy)
- Training data sources (atlas state, prior tables, source references)
- Performance metrics (calibration case pass rate, credal interval coverage rate, field-test prediction accuracy)
- Known limitations (§17)
- Bias considerations (ancestry-skewed source data, functional-vs-mainstream evidence asymmetry, sex-skewed phenotype recognition)
- Privacy posture (local execution, no PII transmission)
- Versioning + backward compatibility
- Governance (who revises priors; review cadence)
- Refutation protocol (how predictions-vs-outcomes feed back to revisions)

---

## §15 — Implementation phases

### Phase 0 — Blockers

**Phase 0A** — Fix MPE all-zero-weights bug (CLAUDE.md open thread). Calculator depends on weighted MPE.

**Phase 0B** — Audit conflict-resolution policy against existing CSRS engine for consistency.

**Phase 0C** — Document baseline phenotype prevalence (§5) with PMID-grounded sources.

**Phase 0D** — Build initial `genetic_id_aliases.csv` with mapping from rsIDs / CNV regions / mtDNA positions / HGVS to atlas BIO-XXXX.

**Phase 0E** — Source CPIC + DPWG guidelines for `pgx_drug_gene_table.csv` Phase 1 seed.

**Phase 0F** — Build rare-syndrome screening gate logic + initial 25 syndrome rule-out rows.

**Phase 0G** — Seed `physiological_state_normalization_table.csv` with ~150 rows covering every biomarker that has documented age-, sex-, Tanner-, menstrual-phase-, pregnancy-, fasting-, time-of-day-, posture-, altitude-, acute-illness-, post-vaccine-, post-antibiotic-, renal-stage-, hepatic-stage-, or ancestry-dependent reference range. This is the highest-impact prior table for clinical accuracy and the most labor-intensive Phase 0 task.

**Phase 0H** — Seed `iatrogenic_exposure_priors.csv` with the ~50 highest-evidence medication / procedure rows: SSRIs, SNRIs, valproate, acetaminophen, antipsychotics, fluoroquinolones, macrolides, GA agents, opioids, PPIs, repeat early antibiotics, Pitocin, contested-status rows for Hep B birth dose. Each PMID-grounded; countervailing evidence preserved.

### Phase 1 — Schema & prior table seeding

- JSON Schemas (input + output, Draft 2020-12), including `subject_state_at_sampling`, `anthropometrics`, `renal_hepatic_function`
- 16 CSV prior tables, headers + 5–15 PMID-grounded seed rows each (14 v2.1 tables + `physiological_state_normalization_table.csv` + `iatrogenic_exposure_priors.csv`)
- `genetic_id_aliases.csv`
- 30 calibration case profile expected outputs in `validation/`
- Body-surface-area + Schwartz-pediatric-eGFR + CKD-EPI-2021-adult formulas implemented
- This spec finalized

### Phase 2 — Engine implementation

- `personalized_risk.py`
- Walley IDM credal aggregation
- Pathway burden analysis
- CDR state classifier
- Functional-trajectory predictor
- Rare-syndrome gate
- PGx filter
- Within-phenotype responder model
- Cost/feasibility solver
- Wire to existing scoring engine + atlas
- Unit tests for each step
- 100% determinism (byte-identical output across runs)

### Phase 3 — Validation

- Run all 30 calibration cases
- Verify outputs match expected
- Sensitivity analysis (§13.4)
- Calibration-anchor verification
- External-tool benchmarking (§13.6)
- Sub-agent audit

### Phase 4 — Population

- Each prior table → 50+ rows for high-coverage common variants/biomarkers/exposures
- PMID-verify every row
- 50+ calibration cases
- Ancestry allele frequency tables for top 50 variants
- Re-run validation; verify anchor stability

### Phase 5 — Reporting & integration

- Markdown report templater
- Clinician handoff summary generator
- Optional HTML rendering
- Obsidian per-case page integration
- FHIR-compatible export option
- Optional neuroimaging/EEG input parsing (when present)

### Phase 6 — Field testing & iteration

- Real cases with clinician partners
- 3 / 6 / 12 / 24-month follow-up
- Refine priors based on observed accuracy
- Add new variants/biomarkers as evidence accumulates
- Each new version with model card + CHANGELOG

---

## §16 — Privacy, ethics, security

### 16.1 Input data sensitivity

Input contains: WGS/WES data (highest), pregnancy + medication history, family medical history, child clinical data, microbiome, toxicology. All highly sensitive.

### 16.2 Local execution model

Calculator runs locally. No transmission of raw data. Anonymized aggregated statistics may be retained for engine improvement only with explicit user consent via `consent_flags.research_use_anonymized`.

### 16.3 Output framing rules

- Never present output as diagnosis
- Always frame as decision support to be reviewed with qualified clinician
- Always include credal intervals
- Always label confidence per recommendation
- Never suggest unilaterally stopping prescribed medications (use STOP_WITH_CLINICIAN)
- Never frame phenotype-membership probability as deterministic

### 16.4 Pre-conception ethics framing

- Output framing centers metabolic-environment optimization, NOT selection
- No "should-you-have-a-child" framing, ever, regardless of risk profile
- No phenotype-as-defect framing
- Disability-rights consultation during Phase 1 to ensure neurodiversity-respectful language
- Explicit pre-conception disclaimer at output top

### 16.5 Threat model

- PII leakage → local execution, no input logging
- Misuse for population policy → output-framing rules, model card intended-use
- Misuse for selective pregnancy → §16.4 framing rules
- Output treated as diagnostic → output-framing rules, handoff document framing
- Adversarial input → input validation, bounds checking
- Malicious prior modification → signed prior tables (Phase 5+), sub-agent audit, change-log
- Engine-version drift → engine_version field, calibration anchor stability rule
- Clinician misinterpretation → recommendation-type definitions, handoff document explanations
- **Genetic discrimination** — never share raw genetic data; never produce outputs that could be subpoenaed for discrimination; explicit opt-out from any data retention
- **Adult autonomy in Mode E** — adults can run their own calculator; output framing respects autonomy and avoids parent-style paternalism
- **Insurance / employment risk from outputs** — outputs include explicit "this output should not be shared with insurance providers without legal counsel" disclaimer

### 16.6 Counseling integration

Output most useful when reviewed with: functional medicine clinician, MAPS-trained clinician, genetic counselor, or developmental pediatrician with phenotype-stratification awareness. Build into output: clinician-type recommendation matched to top-phenotype.

---

## §17 — Known limitations

1. **Source-literature ancestry bias** — most autism genetic studies are European-skewed. Non-European-ancestry effect-size estimates have wider credal intervals.
2. **Functional-medicine evidence asymmetry** — many functional-medicine interventions lack large RCTs (no patent → no industry funding). Calculator down-weights less than strict mainstream-evidence-only systems but uncertainty remains.
3. **Mosaic mutations** — flagged but not directly detected.
4. **Phenotype boundaries fuzzy** — many children fit 2–3 phenotypes partially; soft-probability output reflects this but underlying boundaries genuinely uncertain.
5. **Time-conditional efficacy estimates incomplete** — age-stratified data sparse for many INT-PHE pairs; falls back to unstratified estimate with widened credal interval.
6. **Baseline phenotype prevalence uncertain** — refined in Phase 4 but residual uncertainty propagates.
7. **Field-test predictive accuracy unknown until Phase 6 data accumulates.**
8. **Female-phenotype recognition** — systematic under-recognition in source literature limits prior calibration; calculator attempts to correct but residual bias remains.
9. **Microbiome interpretation** — gut microbiome composition is highly age-dependent; reference normals for autism-relevant sub-populations not yet standardized.
10. **CDR state assignment uncertainty** — Naviaux framework is conceptually strong but lab-operationalization is in flux; calculator uses current best operationalization with explicit framework-version-tag.
11. **Pathway burden is heuristic** — pathway membership tags are atlas-curator-curated and may not reflect every published gene-pathway link.
12. **Functional-trajectory predictions wide** — until Phase 6 real-family data accumulates, trajectory credal intervals will be very wide.
13. **No imaging / EEG by default** — Phase 5+ optional; not part of core Phase 1–4 pipeline.
14. **Single-modality input** — calculator does not currently consume voice / video / behavioral observation data.
15. **PGx coverage gaps** — CPIC guidelines cover ~50 drugs; many autism-relevant interventions (most supplements) lack formal PGx data, so calculator falls back to mechanistic priors with widened credal intervals.

---

## §18 — EHR integration (FHIR option)

Optional FHIR R4-compatible:
- Input from FHIR Patient + Observation + Condition + FamilyMemberHistory + MolecularSequence + Genomics resources
- Output as DiagnosticReport + RiskAssessment resources
- Bidirectional with FHIR-compliant EHR systems
- Opt-in only; local-CSV / local-JSON pathway primary

---

## §19 — Versioning protocol

### 19.1 Semantic versioning

`session4_vMAJOR.MINOR.PATCH`:
- MAJOR: breaking schema change
- MINOR: new prior tables, non-breaking schema additions
- PATCH: prior-row revisions, bug fixes

### 19.2 Backward compatibility

Output of older engine versions reproducible from archived prior tables + archived engine code. Each version snapshots all prior tables.

### 19.3 Release process

1. All prior tables updated + PMID-verified
2. Validation suite passes (all calibration cases meet criteria)
3. Calibration anchor stability verified (within ±0.10)
4. Sub-agent audit passes
5. External-tool benchmarking re-run
6. Model card updated
7. CHANGELOG entry with rationale

### 19.4 Deprecation

Old versions runnable for ≥24 months post-supersession.

---

## §20 — Open design questions (locked for v2.1; revisit in v3.0)

1. Phenotype assignment: soft probabilities across all 11 phenotypes; no forced primary. ✓
2. Multi-phenotype joint priors: marginal only in v2.1; joint priors deferred to v3.0.
3. Time-conditional risk: explicit operating modes (5 in v2.1). ✓
4. Heritability vs environment partition: implicit via driver tagging (genetic | biomarker | exposure | family | microbiome | toxicology | hormonal | immunology); no explicit "heritability %" output.
5. Walsh biotypes: reported alongside the 7 main phenotypes (positions 8–11). ✓
6. Intervention combinations: rank single + combinations from CSRS combinations. ✓
7. Mosaic: flagged via "consider mosaic-aware sequencing." Direct detection deferred.
8. De novo: when child genetic panel shows variants not in either parent's panel, flagged + appropriate prior shifts.
9. Twin / multiple-pregnancy: deferred to v3.0.
10. Adult-mode field-testing: Phase 6 includes adult cohort.
11. **Sex-stratified base rates**: 3:1 male:female default with ascertainment-bias acknowledgment; female-phenotype recognition pattern in §3.4 partly compensates.
12. **CDR state validation**: Naviaux framework is conceptually-strong but operationally evolving; v2.1 uses current best operationalization, version-tagged for forward compatibility.
13. **Pathway burden weighting**: defaults to evidence-quality-weighted; Phase 4 could explore network-medicine pathway-enrichment statistics (e.g., GSEA-style).
14. **Genetic discrimination protection**: outputs explicitly flagged as not-for-insurance-sharing; no biometric data ever stored.
15. **Adult autonomy**: Mode E framing language reviewed by autistic self-advocate during Phase 1.

---

## §21 — Atlas connections

- [[CLAUDE]] §0–§11 — epistemic foundation
- [[Hannah Poling framework]] — central organizing principle
- [[topics/biomarkers/00_BIOMARKERS_INDEX]] — biomarker layer (§3.2)
- [[topics/phenotypes/00_PHENOTYPES_OVERVIEW]] — output target classes
- [[topics/conditions_subgroups/00_SUBGROUPS_OVERVIEW]] — Walsh biotypes + PANS/PANDAS + MCAS
- [[topics/conditions_subgroups/MCAS_Deep_Dive]] — MCAS-specific dive
- [[topics/interventions/00_INTERVENTIONS_INDEX]] — intervention catalog
- [[topics/interventions/immune_modulation/Luteolin]] — example responder-profile pattern
- [[topics/phenotypes/PHE-0003_Regressive_Immune_Inflammatory]] — example phenotype
- [[Frye_Richard]], [[Walsh_William]], [[Naviaux_Robert]], [[Sandin_Sven]], [[Reichenberg_Abraham]], [[Theoharides_Theoharis]], [[Rossignol_Daniel]] — researcher anchors
- All 13 international researcher pages
- 178 biomarkers + 137+ interventions + 75+ hypotheses + 33 mechanisms + 7+4 phenotypes — substrate

---

## §22 — Why this matters (closing)

The atlas mission (CLAUDE.md §0) is **individual-level decisions, not population policy**. Mainstream pediatric guidance is population-average and provably blind to vulnerable subsets. The Hannah Poling case (2008 federal ruling) is the canonical legal-medical recognition that vulnerable subsets exist; the same logic applies to medications, infections, environmental exposures, microbial perturbations, dietary factors, hormonal triggers.

A family with a child showing autism features, or a family planning a pregnancy, or an adult with late autism diagnosis, currently has access to:
- Population-average pediatric guidelines (mainstream)
- Functional medicine clinical interpretation (varies)
- Direct-to-consumer genetic testing (raw data, no integration)
- Direct-to-consumer microbiome / toxicology / metabolomics testing (single-modality reports)
- PGx tests (drug-only)
- Internet research (high noise, low signal)

The calculator integrates all of these into a **deterministic, reproducible, evidence-grounded, individualized, multi-omics-aware, PGx-safety-filtered** output that respects credal uncertainty. It doesn't replace clinicians — it gives families and clinicians a **shared starting point** for individualized decision-making.

This is the deliverable the entire atlas has been building toward.

## §23 — v2.3 changelog vs v2.2 (audit response)

This v2.3 release addresses the v2.2 audit punch list at `/Users/Greg/Autism/SESSION_4_v22_AUDIT_PUNCH_LIST.md`.

| Audit ID | Resolution |
|---|---|
| C-1 (determinism vs IDM) | §7.1 locks canonical s=2; sensitivity sweeps moved to separate diagnostic output |
| C-2 (version strings) | All `input_version` and `engine_version` strings bumped to 2.3 throughout |
| C-3 (phenotype count) | Verified against atlas: PHE-0001..0011 confirmed in `phenotypes.csv` |
| C-4 (float determinism) | New §7.1.1 — library version pin (numpy 1.26.4, scipy 1.12.0, pandas 2.2.0), stable summation order, no parallel reductions, byte-identical regression test across (Linux x86-64, macOS ARM64) |
| C-5 (conflict-resolution math) | §6.1 fully rewritten — formal deduplication by (modality_anchor × phenotype_id), profile-row replacement of constituents, per-anchor subgroup-supersedes-population resolution |
| C-6 (CSRS integration) | New §7.10 — explicit utility function `U = α·responder_p + β·efficacy_credal_low + γ·CSRS_norm + δ·(1−cost) − ε·PGx_risk − ζ·interaction_risk` with locked coefficients (0.40, 0.20, 0.20, 0.10, 0.05, 0.05) |
| C-7 (PGx hard-fail vs soft-modifier) | PGx-contraindicated removed from bundle; PGx-caution carries ε penalty; `dose_reduce_50pct` mapped to STOP_WITH_CLINICIAN to honor "calculator does not prescribe" |
| H-1 (sensory phenotype absent) | Added cross-cutting `sensory_processing_pattern` output dimension; atlas curator decision deferred on whether to add PHE-0012 |
| H-2 (sleep medicine missing) | Added cross-cutting `sleep_disorder_pattern` output dimension + Phase 0 work for melatonin pathway / DLMO / 6-sulfatoxymelatonin biomarkers / sleep-aware interventions |
| H-3 (autonomic dimension) | Expanded `vagal_tone_proxy` block (HRV, tilt-table, Valsalva, skin conductance) — to be implemented in Phase 0 |
| H-4 (acetaminophen overstatement) | Acetaminophen reclassified contested-status; Ahlqvist 2024 sibling-control (PMID 38592388) added to countervailing; evidence_quality lowered to 0.40 |
| H-5 (SSRI mechanism leap) | Mechanism marked `proposed`; evidence_quality lowered to 0.40; Brown 2017 sibling-control + Sujan 2017 added to countervailing; recommendation type CONSIDER not AVOID |
| H-6 (mtDNA per-variant) | Single lumped row replaced with per-variant rows: m.3243A>G (two heteroplasmy bands), m.8344A>G, m.8993T>G (two bands); tissue caveats explicit |
| H-7 (CDR not specified) | §7.6 now contains concrete deterministic decision tree per CDR state with boolean conjunctions; output flagged `experimental: true`; transition probabilities deferred to v3.0 |
| H-8 (functional trajectory) | §7.7 downgraded to qualitative bands only in v2.3; no numerical IQ predictions; `experimental: true` flag |
| H-9 (pathway burden normalization) | §7.4 now uses anchored normalization with `pathway_anchor_values.csv` locked at v2.3 release |
| H-10 (Walsh false precision) | Walsh biotype rows in §3.4 now carry explicit lower evidence_quality (0.30–0.40) with wider credal intervals |
| H-11 (Cunningham single-lab) | Flagged in §17 limitations; credal intervals widened in `comorbidity_priors.csv` |
| H-12 (microbiome lab-method portability) | New requirement: every microbiome row tags lab method (16S V3V4 vs V4 vs V1V2 vs shotgun) + DNA extraction kit + bioinformatics pipeline; method-specific reference table required |
| H-13 (cycle-phase coverage) | Phase 0G estimate revised upward to ~400+ rows for §3.13b (cortisol/cycle-phase alone is ~50 cells) |
| H-14 (ACEs scoring) | Category flags as primary input; ace_score is summary only; priors keyed on category |
| H-15 (supplement-PGx) | Phase 0E priority extended to include methylfolate × COMT V158M, methylfolate × MTHFR, methyl-B12 × MTRR/BHMT supplement-PGx rows |
| H-16 (calibration cases) | Expanded from 30 to 60 minimum target; coverage matrix per (mode × phenotype) cell |
| H-17 (calibration criterion) | New required `validation/calibration_cases/case_NN.yaml` schema with explicit floor/ceiling/expected interventions |
| H-18 (external benchmarks) | Tiered: Tier 1 (Frye, Cunningham, Walsh, Lemonnier, Hannah Poling case profiles) must pass before v1.0; Tier 2 (PRS, SPARK, ABCD, Spectrum 10K) is post-release continuous improvement |
| M-1 (syndromic gate gaps) | Expanded from 25 to ~40 syndromes in §4 — adding Kleefstra (EHMT1), KBG (ANKRD11), Coffin-Siris (ARID1B), CDKL5, FOXG1, SETBP1, MEF2C, GRIN2B-related, Cohen syndrome (VPS13B), Mowat-Wilson (ZEB2) |
| M-2 (anti-NMDAR encephalitis) | Added to syndromic gate as autism-mimic differential with neurology referral output |
| M-3 (concordance bonus formula) | §6.2 explicit: `bonus = min(0.10, 0.02 × (n_concordant_modalities − 2))` |
| M-4 (renal/hepatic dosing) | Output gives recommendation type only; no numerical dose; defers to clinician |
| M-5 (VAR-NNNN namespace) | Documented as new namespace separate from BIO-XXXX; collision-checked in `genetic_id_aliases.csv` |
| M-6 (responder predictors) | Dedicated `responder_predictor_priors.csv` (§7.5) with PMID per shift; no hard-coded numbers in spec |
| M-7 (sex concordance numerics) | Phase 0 work: populate from Sandin 2014 |
| M-8 (geographic/environmental priors) | New `environmental_exposure_priors.csv` Phase 1 work — air pollution, water quality, season of conception |
| M-9 (parental occupational exposures) | Controlled vocabulary + prior table Phase 1 |
| M-10 (drug-supplement interactions) | New `supplement_drug_interaction_table.csv` Phase 1 |
| M-11 (intervention-intervention antagonism) | Pairwise filter step added to §7.10 utility (the ζ term) |
| M-12 (privacy retention) | Anonymized retention requires k-anonymity ≥5 enforcement, or path is dropped |
| M-13 (re-identification risk) | Threat model in §16.5 expanded; default behavior is no input JSON storage |
| M-14 (disability-rights consultation) | Panel of ≥3 autistic self-advocates including non-speaking communicator, intellectually disabled autistic adult, late-diagnosed autistic woman; honoraria; IRB |
| M-15 ("patient" terminology) | Replaced with "user"/"individual" in Mode E; full terminology audit by self-advocate panel |
| M-16 (intersex pathway) | Documented fallback: use both sex-strata or wider credal; flagged in §17 |
| M-17 (vaccine-policy framing) | All vaccine-related outputs use STOP_WITH_CLINICIAN framing; never AVOID without explicit family consent flag and clinical context |
| M-18 (calibration anchor v1.0 baseline) | Locked at v1.0 release |
| M-19 (JSON shorthand) | All examples marked illustrative-only; reference to actual `personalized_risk_input.schema.json` |
| M-20 (lactation/nursing-infant) | Added to child_data block in §2.5 |
| M-21 (geography/climate) | Added residential geography block (anonymized to 100km grid) |
| L-1..L-10 | Stylistic / editorial fixes folded into v2.3 throughout |

**Top-5 critical fixes from v2.2 → v2.3**: C-1 (determinism formalism), C-4 (float determinism), C-5 (conflict-resolution math), C-6 (CSRS utility function), H-7 (CDR concrete spec).

**Top-5 scientific accuracy corrections from v2.2 → v2.3**: H-4 (acetaminophen contested + Ahlqvist 2024), H-5 (SSRI mechanism downgraded + sibling-control countervailing), H-6 (mtDNA per-variant + tissue caveats), H-8 (functional trajectory qualitative-only), H-10 (Walsh lower evidence_quality).

---

## §23a — v2.2 changelog vs v2.1

| Domain | v2.1 | v2.2 |
|---|---|---|
| Anthropometric calibration | sex + age in some tables | full weight, height, BMI, head circumference, BSA z-scoring; Tanner stage; growth trajectory tracking |
| Subject state at sampling | implicit | explicit `subject_state_at_sampling` block per biomarker (§2.6b): fasting state, time-of-day, circadian phase, sleep state, hydration, posture, ambient temp, altitude, recent illness, recent antibiotic, recent vaccination, exercise, stress, menstrual phase, pregnancy/lactation, time since last meal/medication/supplement |
| Renal/hepatic function | absent | full block (§2.13b) — required for any drug-dosing recommendation; Schwartz pediatric eGFR vs CKD-EPI adult |
| State-conditional reference ranges | not formalized | new `physiological_state_normalization_table.csv` (§3.13b) — ~150 rows covering every age-, sex-, state-, method-dependent biomarker reference range |
| Engine pre-processing | basic z-score | full state-conditional normalization with age × sex × Tanner × menstrual-phase × pregnancy × fasting × time-of-day × posture × altitude × acute-illness × post-vaccine × post-antibiotic × renal-stage × hepatic-stage × ancestry-population reference range |
| SSRI framing | erroneously in PGx-as-treatment context | reclassified as iatrogenic exposure; gestational SSRI = autism risk factor (Croen 2011, Rai 2013, Boukhris 2016); SSRIs in autistic patients = STOP_WITH_CLINICIAN flag, never autism core-feature treatment; explicit note that Cochrane review found no benefit |
| Iatrogenic exposure framework | absent | new `iatrogenic_exposure_priors.csv` (§3.13c) — SSRIs, SNRIs, valproate, acetaminophen, thalidomide, antipsychotics, fluoroquinolones, macrolides, GA, opioids, PPIs, repeat antibiotics, Pitocin induction, Hep B birth dose; both population-average and subgroup-conditional risk; countervailing evidence preserved |
| Antipsychotic framing | implicit (FDA-approved for autism irritability) | explicit STOP_WITH_CLINICIAN if used for core autism features; CONSIDER alternatives if for aggression; full side-effect-profile awareness |
| Acetaminophen | absent | major gestational/pediatric avoidance based on Bauer 2021 consensus + Ji 2020 + Liew 2014 |
| Valproate | absent | absolute contraindication in pregnancy |
| Body surface area | absent | calculated for dosing (chelation, certain drugs) |
| Pubertal stage | absent | Tanner staging for adolescents — feeds hormonal axis interpretation, drug metabolism, intervention timing |
| Menstrual phase | absent | explicit input for adult mode + adolescent female mode; required for accurate hormone interpretation |

## §23b — v2.1 changelog vs v2.0

| Domain | v2.0 | v2.1 |
|---|---|---|
| Operating modes | 4 | 5 (added Adult / late-diagnosis Mode E) |
| Prior tables | 7 | 14 (added microbiome, toxicology, hormonal, immunology/HLA, comorbidity, ACEs, pathway-burden, PGx tables) |
| Genetic input | SNPs + flag for CNV/mosaic | SNPs + CNVs + WES/WGS rare variants + mtDNA + HLA + ancestry-calibrated |
| Microbiome | absent | full 16S/shotgun integration |
| Toxicology | exposure history only | measured biomarkers (heavy metals, mycotoxins, glyphosate, PFAS, phthalates) |
| Hormonal axes | absent | full HPA, HPT, sex hormones, oxytocin/AVP |
| Immunology | basic cytokines | HLA + complement + cytokines + immunoglobulins + lymphocyte subsets + autoantibody panels |
| Metabolomics | OAT only | OAT + amino acids + acylcarnitine + sphingolipids + untargeted |
| Comorbidity recognition | atomic biomarkers | full clusters: MCAS-EDS-POTS triad, epilepsy, ADHD/OCD, GI, atopic |
| Sex stratification | input field only | full sex-stratified priors + female-phenotype recognition |
| ACEs / trauma | absent | input + modifier table |
| Gestational/birth process | partial | full gestational + cord blood + placental + neonatal |
| Pathway burden analysis | absent | 8-pathway burden scoring |
| CDR state | absent | Naviaux state assignment + transition probabilities |
| Functional trajectory | absent | verbal + IQ + adaptive + regression-window prediction with credal intervals |
| Within-phenotype responder | absent | full responder-prediction layer |
| PGx integration | absent | CPIC-grounded PGx filter on all interventions |
| Rare-syndrome screening gate | absent | 25-syndrome screening gate |
| Cross-modality concordance | absent | concordance bonus in credal aggregation |
| Cost / feasibility | EIG cost only | full feasibility-constrained alternative bundle |
| External validation | sub-agent only | external-tool benchmarking (PRS, SPARK, Walsh, Frye, Cunningham) |
| Calibration cases | 20 | 30 (added Mode E + multi-modality + female-phenotype + ancestry + syndromic gate) |
| Validation rigor | sensitivity + sub-agent | sensitivity + sub-agent + external-tool + 100-case real-family field test |
| Adult autonomy | not addressed | Mode E + autistic-self-advocate review |
| Genetic discrimination protection | basic | explicit opt-out + insurance-sharing disclaimer |

---

**Spec v2.1 complete. Ready for Phase 0 work (MPE bug fix, baseline prevalence documentation, genetic ID aliases, PGx seed, syndromic gate logic) and then Phase 1 implementation when user approves.**

---

## §24 — Verification protocol for prior tables (BioMysteryBench-aligned)

This section encodes a binding methodology for every prior-table row written into the atlas.

### 24.1 Why this protocol exists

Anthropic's [BioMysteryBench evaluation (2026)](https://www.anthropic.com/research/Evaluating-Claude-For-Bioinformatics-With-BioMysteryBench) documents a critical empirical finding about LLM behavior on bioinformatics tasks: on hard problems, "successes typically come in just one or two out of five attempts. The model stumbles onto a lucky solution path rather than following a reproducible strategy." This is the structural failure mode behind LLM-generated PMID fabrication, biomarker-threshold confabulation, and other content-generation errors. The atlas's deterministic-no-LLM-in-math architecture (§7.1.1) is the direct defense against this failure mode at scoring time. **§24 extends the same defense to data-ingestion time.**

The empirical case study that motivated this section: during Phase 0H seeding (2026-04-30), 45 of 52 PMIDs in an initial draft of `iatrogenic_exposure_priors.csv` were fabricated — generated from training-data approximation rather than verified against PubMed. The error was caught by independent batch-verification before the file synced to Drive, and the file was rebuilt with 24 PMID-verified rows. The protocol below makes that style of failure structurally impossible going forward.

### 24.2 The verify-before-write rule

**Binding rule:** No row shall be written to any prior table without independent verification that every cited PMID matches the claimed paper. Verification must include:

1. **PubMed esummary fetch** of every cited PMID via the `eutils.ncbi.nlm.nih.gov` API.
2. **Match check** against the claimed paper:
   - Expected first-author surname must appear in `sortfirstauthor` OR in `title`.
   - Expected publication year must equal `pubdate[:4]`.
   - At least one expected key term (extracted from the row's mechanistic claim) must appear in `title` OR `source` (journal).
3. **Verification log** persisted alongside the prior CSV: one line per cited PMID with (claimed_author, claimed_year, claimed_key_term, fetched_author, fetched_year, fetched_journal, fetched_title, match_status).
4. **Row is written only if all cited PMIDs pass.** A single mismatch on any PMID in `primary_pmids` or `countervailing_evidence_pmids` rejects the row.

### 24.3 Seed-script template

All Phase 0+ seeding work uses a common template at `scripts/seed_with_verification.py`. The template:

- Accepts a list of candidate row specifications, each with claimed PMID + claimed author + claimed year + key term.
- Fetches esummary for each PMID via the entrez API (with retry, rate-limiting per NCBI guidelines).
- Validates the match per §24.2 step 2.
- Writes the row to the CSV only if validation passes.
- Emits a per-row verification log entry.
- Produces a summary report at end of run: rows-attempted, rows-verified, rows-rejected, rejection-reasons.

**Memory-based generation is not permitted.** The template enforces this by requiring each candidate row to declare its claimed PMID *and* its claimed author/year/term *separately*; the script verifies they match the actual PubMed record. A row whose PMID was generated from training-data approximation will fail verification because the fetched record won't match the claimed author/year/term.

### 24.4 Pre-commit verification hook

A pre-commit hook (`scripts/precommit_pmid_verify.py`) runs on every git commit that touches a prior CSV file. The hook:

1. Diffs the CSV vs HEAD to find newly added rows.
2. Extracts cited PMIDs from each new row.
3. Runs the verify-before-write check on each.
4. Blocks the commit if any row contains an unverified PMID.

This is the structural enforcement layer. Committing fabricated PMIDs becomes impossible without explicitly bypassing the hook.

### 24.5 Validation-notebook standard for calibration cases (BioMysteryBench-aligned)

BioMysteryBench requires every benchmark question author to ship a validation notebook proving the signal exists in the data. The atlas adopts the same standard for calibration cases (§13.1).

Each calibration case at `validation/calibration_cases/case_NN/` ships three artifacts:

1. **`input.json`** — the family multi-omics input data (per §2 schema).
2. **`expected_output.yaml`** — the ground-truth output for this case, with explicit `expected_top_phenotype`, `expected_phenotype_p_floor/ceiling`, `expected_top_3_intervention_ids`, `expected_recommendation_types`, `expected_syndromic_flag`, `expected_cdr_state`, `expected_open_questions_includes`, etc. (per §13.1 schema).
3. **`validation_notebook.ipynb` OR `validation_notebook.py`** — an executable validation artifact (Jupyter notebook OR plain Python script) that:
   - Loads `input.json`
   - Runs `compute_personalized_risk(input_json)`
   - Asserts equality with `expected_output.yaml` on every required field
   - Documents the published case profile the case is drawn from (PMID-grounded)
   - Is executable end-to-end in CI without manual intervention (preferred form for CI pipelines is `.py`; preferred form for human-readable narrative cases is `.ipynb`; either is acceptable)

The validation artifact is the proof that the deterministic engine extracts the expected output from the input — the same standard BioMysteryBench applies. A calibration case without an executable validation artifact is not a calibration case. (Resolves audit H-7: spec previously specified .ipynb only; .py is equally valid and preferred for CI.)

### 24.6 External validation harness

Before each major version release (v1.0, v2.0, ...), the engine is run against the [BioMysteryBench-preview](https://huggingface.co/datasets/Anthropic/BioMysteryBench-preview) 5-task sample as a sanity check that the LLM-substrate used for non-scoring atlas work (literature ingestion, sub-agent audits) has not regressed on bioinformatics tasks. The 5-task preview is small enough to run cheaply but representative enough to detect serious substrate degradation. Pass-rate is logged in the model card per §14.

### 24.7 Atlas-as-benchmark posture

Once Phases 0–3 ship and the calibration suite has been hardened to BioMysteryBench's validation-notebook standard, the atlas + calibration suite is structurally a domain-specific extension of BioMysteryBench: an autism-phenotype-stratification benchmark for individual-level conditional risk computation. Submission to peer review as a contribution is a Phase 5+ goal, not a v1.0 blocker. Adopting the methodology now keeps the path open.

### 24.8 Failure-mode encoding for future agents

Future LLM agents (including future Claude versions) working on this atlas will read §24 as part of their grounding. The section explicitly names the failure mode ("lucky solution path" / fabrication when ungrounded), points to the BioMysteryBench evidence, and binds the agent to the verify-before-write protocol. Agents that violate §24 produce work that fails the pre-commit hook and is structurally unable to enter the atlas.
