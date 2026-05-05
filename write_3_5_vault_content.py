#!/usr/bin/env python3
"""3.5F + 3.5G + 3.5H — vault content.

Writes:
  topics/interventions/drug_repurposing/<DrugName>.md  (12 drugs)
  topics/interventions/peptides/<PeptideName>.md  (10 peptides)
  topics/interventions/mitochondrial/Life_Stage_Mito_Protocols.md
  topics/protocols/00_PROTOCOLS_INDEX.md (new section indexing protocols.csv)
  topics/conditions_subgroups/PANS_PANDAS_Deep_Dive.md
  topics/conditions_subgroups/MCAS_Deep_Dive.md
  topics/conditions_subgroups/Walsh_Biotypes.md
"""
from pathlib import Path
import datetime as dt

NOW = dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')
VAULT = Path("/sessions/jolly-determined-darwin/mnt/Autism/vault")

def write_md(rel_path, content):
    p = VAULT / rel_path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)
    print(f"  ✓ {rel_path}")

# ============================================================
# 3.5F — Drug repurposing per-drug deep dives
# ============================================================
print("Writing drug repurposing deep dives...")

write_md("topics/interventions/drug_repurposing/Rapamycin.md",
"""---
id: DRUG-Rapamycin
type: intervention_deep_dive
class: drug_repurposing
intervention: INT-0036
audience: clinician, parent
---

# Rapamycin (sirolimus) — mTOR Inhibitor for Autism

**Atlas record:** [[INT-0036 Rapamycin (sirolimus)]] — csrs **67.0**
**Mechanism:** mTOR pathway inhibition
**FDA approved for:** Tuberous sclerosis-associated SEGA, immunosuppression in transplant
**Off-label autism use:** TSC1/TSC2-positive children + select PTEN/NF1/PI3K-pathway variant cases

## Why this matters

Rapamycin is the **single most precision-targeted drug in autism medicine when matched to the right genotype**. mTOR-pathway hyperactivation drives over-proliferation of dendritic spines, impaired synaptic pruning, and altered metabolic state. Loss-of-function variants in TSC1/TSC2 (tuberous sclerosis), PTEN (PTEN hamartoma syndrome), or related pathway components cause autism via this mechanism. Rapamycin directly inhibits mTOR; in animal models (and emerging human studies), it reverses autism-relevant phenotypes in genotype-positive subjects.

## When to consider

**Strong indication:**
- Confirmed TSC1/TSC2 mutation (tuberous sclerosis complex)
- Confirmed PTEN mutation (PTEN hamartoma syndrome)
- NF1 (neurofibromatosis type 1) with autism features
- Confirmed mTOR-pathway variant on autism gene panel / WES
- SEGA (subependymal giant cell astrocytoma) management — FDA-approved indication overlapping autism

**Weaker indication:**
- General autism without genetic evidence of mTOR pathway involvement
- Idiopathic autism

## Dosing

- **Children:** 0.5–2 mg twice weekly typical starting; titrated to trough levels 5–15 ng/mL
- **Adults:** 1–6 mg/day depending on indication
- **Monitoring:** trough levels, CBC, LFTs, lipids, kidney function, immune response

## Mechanism + biology

mTOR is the master regulator of protein synthesis, autophagy, ribosome biogenesis, and metabolism. mTORC1 hyperactivation in TSC/PTEN/NF1 syndromes drives:
- Excessive synaptic protein synthesis (translates into excitatory dominance)
- Impaired autophagy (cellular quality control)
- Excess dendritic spine density
- Altered neuronal morphology
- Metabolic dysregulation

Rapamycin inhibits mTORC1 directly, normalizing these downstream consequences.

## Evidence base

- **TSC trials** — multiple Phase 2-3 trials; FDA approval for SEGA management; emerging autism outcome data
- **PTEN syndrome trials** — smaller cohorts; positive signals
- **Animal models** — extensively documented in TSC mouse models; reversal of autism-relevant phenotypes
- **Human off-label** — increasing pediatric off-label experience under tertiary genetics + neurology supervision

## Practical workflow

1. **Genetic confirmation first.** CMA + Fragile X + autism gene panel + WES if indicated. mTOR-pathway variant required for evidence-based use.
2. **Specialist referral.** Pediatric geneticist + neurologist familiar with rapamycin pediatric dosing.
3. **Pre-treatment labs.** CBC, CMP, lipids, fasting glucose, baseline immune panel.
4. **Titration.** Start low; titrate by trough levels.
5. **Ongoing monitoring.** Trough levels every 2-4 weeks during titration; quarterly thereafter.

## Atlas connections

- [[INT-0036 Rapamycin (sirolimus)]] — formal entry
- [[HYP-0029 Tuberous sclerosis (TSC1/TSC2)]]
- [[HYP-0030 PTEN hamartoma syndrome]]
- [[MEC-0009 mTOR pathway dysregulation]]
- [[BIO-0170 CYP3A4 _ CYP3A5 genotype]] — affects rapamycin metabolism / dosing
- [[topics/interventions/drug_repurposing/00_DRUG_REPURPOSING_OVERVIEW]]
""")

write_md("topics/interventions/drug_repurposing/Bumetanide.md",
"""---
id: DRUG-Bumetanide
type: intervention_deep_dive
class: drug_repurposing
intervention: INT-0110
audience: clinician, parent
---

# Bumetanide — NKCC1 Inhibitor for Autism

**Atlas record:** new INT (Bumetanide for autism, distinct from diuretic indication)
**Mechanism:** NKCC1 inhibitor → forces GABA developmental switch
**FDA approved for:** Edema (loop diuretic)
**Off-label autism use:** Chloride-imbalance subgroup with failed GABA developmental switch

## Why this matters

Per [[BenAri_Yehezkel]]'s framework, GABA is *excitatory* in the developing brain (high intracellular chloride), then switches to *inhibitory* as the brain matures (NKCC1→KCC2 transition). When this switch fails — chronically high intracellular Cl⁻ — the brain remains in excitatory-dominant state, manifesting as seizure susceptibility, sensory hypersensitivity, repetitive behavior, anxiety. Bumetanide directly inhibits NKCC1, lowering intracellular chloride and forcing the GABA switch toward inhibitory mode.

## When to consider

**Strong indication:**
- Seizure susceptibility or comorbid epilepsy
- Severe sensory hypersensitivity
- High anxiety / repetitive behavior baseline
- Documented chloride imbalance (research panels)

**Weaker indication:**
- Idiopathic autism without chloride-imbalance markers
- Primary genetic syndromic ASD

## Dosing

- **Children:** 0.5–2 mg/day, BID divided
- **Potassium monitoring required** (loop diuretic effect)
- **Hypokalemia is the dose-limiting side effect**

## Evidence base

Multiple Phase 2 and Phase 3 trials; mixed primary outcomes per [[CLAUDE]] §9 effect heterogeneity. Subgroup analysis where possible shows responder profile is the chloride-imbalanced + sensory-hyperreactive child. Lemonnier 2012 + Lemonnier 2017 trials established the framework; Phase 3 2022-23 mixed but consistent with subgroup signal dilution in unstratified populations.

## Atlas connections

- [[BenAri_Yehezkel]] — GABA developmental switch foundational researcher
- [[HYP-0071 Brainstem_pons hypoplasia + GABA developmental switch failure]]
- [[MEC-0034 GABA developmental polarity switch (NKCC1_KCC2)]]
- [[topics/interventions/drug_repurposing/00_DRUG_REPURPOSING_OVERVIEW]]
""")

write_md("topics/interventions/drug_repurposing/Suramin.md",
"""---
id: DRUG-Suramin
type: intervention_deep_dive
class: drug_repurposing
intervention: INT-0111
audience: clinician, researcher
---

# Suramin — Antipurinergic Therapy for Autism

**Atlas record:** new INT (Suramin low-dose for autism)
**Mechanism:** Purinergic receptor antagonist (P2X / P2Y); interrupts cell danger response (CDR)
**FDA approved for:** African trypanosomiasis (sleeping sickness)
**Off-label autism use:** Concept-validated by Naviaux 2017; not commercially available for autism in US

## Why this matters

[[Naviaux_Robert]]'s 3-Hit framework places persistent activation of the cell danger response (CDR) at the center of autism pathophysiology. CDR is initiated by extracellular ATP (eATP) and purinergic signaling. Suramin blocks purinergic receptors, theoretically interrupting the "stuck" CDR state. Naviaux 2017 ([[SRC pmid 28695149]]) Phase I/II RCT showed core symptom improvements with single low-dose infusion.

## When to consider

**Research / compassionate use only.** Not commercially available for autism. Toxicity profile (peripheral neuropathy, adrenal insufficiency at chronic doses) limits broad clinical use.

## Atlas connections

- [[Naviaux_Robert]] — framework architect
- [[SRC-001448 41902612]] — 3-Hit framework synthesis paper
- [[HYP-0006 Mitochondrial dysfunction]]
- [[MEC-0014 SIRTUIN _ NAD+ metabolism]] — purinergic-NAD+ intersection
- [[topics/interventions/drug_repurposing/00_DRUG_REPURPOSING_OVERVIEW]]
""")

# Continue with more drug pages — keeping them concise
for name, content in [
    ("Memantine", "NMDA receptor antagonist; Alzheimer's-approved; mixed RCT signal in autism subgroups; dose 5–20 mg/day. Atlas: [[INT-0038]]."),
    ("Metformin", "AMPK activator + microbiome modulator; emerging autism / metabolic-overlap relevance. Caution: mitochondrial impact in vulnerable kids. Atlas: [[INT-0037]]."),
    ("Pioglitazone", "PPAR-γ agonist; anti-inflammatory; emerging in chronic neuroinflammation. Caution: weight gain, fluid retention. Atlas: new INT."),
    ("Minocycline", "Tetracycline microglial modulator; anti-inflammatory; long clinical history. Caution: permanent skin discoloration with long-term use. Atlas: new INT."),
    ("Allopregnanolone_Ganaxolone", "Endogenous neurosteroid; positive GABA-A modulator. Ganaxolone FDA-approved for CDKL5. Calming/anxiolytic; emerging epileptic ASD use. Atlas: new INT."),
    ("Trehalose", "Disaccharide; promotes autophagy/mitophagy. Emerging neurodegenerative + neurodevelopmental use. Dose 5-15 g/day. Atlas: new INT."),
    ("Lovastatin", "Statin with FXR / cholesterol-pathway effects; preclinical Fragile X work. Caution: mitochondrially toxic, CoQ10-depleting. Atlas: new INT."),
    ("Low_Dose_Ivermectin", "Microbiome modulator per [[Hazan_Sabine]] observation: increases Bifidobacterium 24h in some, depletes in others (sequencing-guided decision). Atlas: observational."),
    ("Vancomycin_Oral", "Non-absorbable; targets Clostridia overgrowth (elevated HPHPA, 4-cresol). Sandler 2000 case series. Atlas: new INT."),
    ("Valacyclovir", "Antiviral for HHV-6 / EBV reactivation contexts. Long-term low-dose suppression in chronic-infection subgroup. Atlas: new INT."),
]:
    write_md(f"topics/interventions/drug_repurposing/{name}.md",
f"""---
id: DRUG-{name}
type: intervention_deep_dive_stub
class: drug_repurposing
audience: clinician, parent
---

# {name.replace('_',' ')}

{content}

## Atlas connections

- [[topics/interventions/drug_repurposing/00_DRUG_REPURPOSING_OVERVIEW]]
- [[topics/interventions/00_INTERVENTIONS_INDEX]]
- [[CLAUDE]] §9 effect-heterogeneity principle (mixed RCT interpretation)

*This is a stub deep-dive page. Full content pending continued curation per CLAUDE.md Session 3.5F roadmap.*
""")

# ============================================================
# 3.5G — Peptide deep dives
# ============================================================
print("\nWriting peptide deep dives...")

write_md("topics/interventions/peptides/Oxytocin.md",
"""---
id: PEPTIDE-Oxytocin
type: intervention_deep_dive
class: peptides
intervention: INT-0061
audience: clinician, parent
---

# Intranasal Oxytocin for Autism

**Atlas record:** [[INT-0061 Intranasal oxytocin]] — csrs **53.7**
**Mechanism:** Synthetic neuropeptide; binds oxytocin receptors; modulates social-cognition circuits via amygdala/PFC
**Status:** Emerging therapy; FDA approved as Pitocin for labor; off-label for autism social communication

## Evidence

Multiple RCTs including Parker 2017 and Sikich 2021 — mixed primary outcomes consistent with [[CLAUDE]] §9 effect heterogeneity. Subgroup signal: low-baseline-oxytocin + high-anxiety profiles tend to respond better. [[Hollander_Eric]] runs trials at Albert Einstein.

## Dosing

- 16-32 IU per dose, 1-2x daily intranasal
- Trial duration typically 6-12 weeks for response assessment

## Atlas connections

- [[Hollander_Eric]]
- [[HYP-0034 Oxytocin system dysregulation]]
- [[BIO-0118 Oxytocin]]
- [[topics/interventions/peptides/00_PEPTIDES_OVERVIEW]]
""")

for name, content in [
    ("Vasopressin", "Closely related to oxytocin; complementary social-bonding mechanism. Sex-differentiated effects. Less studied than oxytocin in autism. Per Carter framework."),
    ("IGF_1", "Insulin-like growth factor 1 (mecasermin). FDA-approved for primary IGFD. Best evidence in **SHANK3 / Phelan-McDermid syndrome** — rescues synaptic protein synthesis defects. Per [[Hollander_Eric]] Phase 2 trials."),
    ("BPC_157", "Pentadecapeptide derived from gastric protective protein. Strong preclinical anti-inflammatory + gut-protective + neuroprotective. No autism RCT — mechanism strong, clinical evidence absent. Atlas: [[INT-0062]]."),
    ("Selank", "Synthetic tuftsin analog. Anxiolytic + nootropic in animal models. Russian human studies show anxiolytic effect. Speculative for autism. Atlas: [[INT-0063]]."),
    ("Semax", "ACTH(4-10) analog. Nootropic + BDNF-promoting in animal models. Russian human cognitive-enhancement studies. Speculative for autism. Atlas: [[INT-0064]]."),
    ("Cerebrolysin", "Porcine brain-derived peptide mixture. Trophic effects via neurotrophin-like activity. Used widely in Eastern European pediatric autism protocols. Not FDA-approved in US. Atlas: [[INT-0065]]."),
    ("Exorphins_Casomorphin_Gluteomorphin", "Opioid-like peptides from incomplete digestion of gluten/casein. Biological substrate for GFCF diet effect. Cross BBB in some children with intestinal hyperpermeability. Bind μ-opioid receptors; affect mood/behavior/sensory. Reichelt + Knivsberg foundational research."),
    ("Gut_Peptides_PYY_GLP1_Ghrelin", "Endogenous gut peptides regulating satiety, gut-brain signaling, mood. Increasingly studied in metabolic-psychiatric overlap. Microbiome modulates production. Emerging autism research."),
    ("Antimicrobial_Peptides", "Defensins, cathelicidins (LL-37). Endogenous antimicrobial peptides; first-line innate immunity. Vitamin D drives cathelicidin expression. Dysregulated in some autism subgroups."),
    ("Mito_Peptides_Humanin_MOTS_c", "Mitochondria-encoded peptides. Humanin (16S rRNA): anti-apoptotic, neuroprotective, anti-inflammatory. MOTS-c (12S rRNA): metabolic regulation, exercise-mimetic. Emerging research; minimal autism work yet."),
]:
    write_md(f"topics/interventions/peptides/{name}.md",
f"""---
id: PEPTIDE-{name}
type: intervention_deep_dive_stub
class: peptides
audience: clinician
---

# {name.replace('_',' ')}

{content}

## Atlas connections

- [[topics/interventions/peptides/00_PEPTIDES_OVERVIEW]]
- [[topics/interventions/00_INTERVENTIONS_INDEX]]

*This is a stub deep-dive page. Full content pending continued curation per CLAUDE.md Session 3.5G roadmap.*
""")

# ============================================================
# 3.5H — Life-stage mitochondrial protocols
# ============================================================
print("\nWriting 3.5H life-stage mito protocol...")

write_md("topics/interventions/mitochondrial/Life_Stage_Mito_Protocols.md",
"""---
id: LIFE-STAGE-MITO-PROTOCOLS
type: protocol_deep_dive
class: mitochondrial
audience: clinician, parent_advanced
---

# Life-Stage Mitochondrial Protocols for Autism Prevention + Support

Per CLAUDE.md §Session 3.5H roadmap. This page operationalizes mitochondrial support across the developmental timeline — preconception, pregnancy, birth, infancy, early childhood, school-age. Each life stage has specific risks + specific interventions.

## Why life-stage matters

Per [[Naviaux_Robert]]'s 3-Hit framework: Hit-1 (genetic/epigenetic mito sensitization) is established at conception; Hit-2 (early CDR trigger) typically falls in late 1st trimester through 18-36 months; Hit-3 (persistent CDR during the developmental window) is the prevention target. Mitochondrial-supportive interventions at each stage reduce overall risk and improve outcomes if autism is already established.

## 1. Preconception (both parents, 6+ months pre-conception)

**Goal:** Optimize gametic mitochondrial quality + parental methylation cycle status

**Both parents:**
- Mitochondrial cocktail: CoQ10 (ubiquinol) 100-200 mg/day, L-carnitine 500 mg 2x daily, B-vitamin complex (methylated forms), vitamin C 500-1000 mg, vitamin E 200 IU, alpha-lipoic acid 200 mg, magnesium glycinate 200-400 mg
- Methyl-donor support calibrated to each parent's MTHFR/COMT/CBS profile
- DHA / omega-3: 1000-2000 mg combined EPA+DHA daily
- Targeted antioxidants: NAC 600-1200 mg, glutathione precursors
- Avoidance: glyphosate, plastic exposures, mitotoxic medications (statins, valproate), alcohol, smoking

**Maternal-specific:**
- Comprehensive mitochondrial workup if family history (lactate/pyruvate/acylcarnitine)
- Maternal mtDNA panel if family history
- Optimization to ferritin 50-150, vitamin D 50-80 ng/mL, B12 >500

**Paternal-specific:**
- Sperm DNA fragmentation testing
- 6-month preconception optimization cycle (spermatogenesis takes ~74 days)
- Avoid heat exposure (saunas, hot tubs, laptop on lap)
- Body composition optimization

## 2. Pregnancy (months 1-9)

**Goal:** Maintain maternal mito function during fetal neurodevelopment

- Maternal mito cocktail (calibrated to pregnancy-safe doses)
- DHA / omega-3 sufficiency — most prenatal vitamins inadequate
- Choline 450+ mg/day (most prenatals provide ~50 mg)
- Methylated folate (5-MTHF) NOT folic acid for MTHFR-positive mothers
- Avoidance: valproate (strongly contraindicated), acetaminophen where avoidable, glyphosate-residue foods, mercury-rich fish
- Monitor: maternal CRP, glucose, thyroid (full panel), 25-OH-D, ferritin
- Stress regulation (cortisol affects fetal HPA programming)

## 3. Birth + early postnatal (0-3 months)

**Goal:** Preserve mitochondrial integrity during the high-stress birth transition

- Vaginal birth where possible (microbiome seeding has metabolic implications)
- Breastfeeding (mitochondrially superior to formula)
- Avoidance of unnecessary medical interventions (especially vitamin K1 + Hep B + tylenol stack at birth — discuss timing with knowledgeable pediatrician per [[topics/conditions_subgroups/00_SUBGROUPS_OVERVIEW]])
- Skin-to-skin contact (autonomic / vagal regulation)
- Avoid antibiotic exposure unless clinically necessary

## 4. Infancy (3-18 months)

**Goal:** Identify metabolic vulnerability early; intervene before regression window closes

- Watch for: hypotonia, poor feeding, regression, frequent illness, prolonged jaundice
- If any vulnerability markers — early mitochondrial workup (lactate, acylcarnitine, ammonia)
- If mito-vulnerable: pediatric mito cocktail (CoQ10, carnitine, B-vitamins, magnesium) under physician supervision
- Avoidance: unnecessary antibiotics, mitotoxic medications, prolonged fasting, severe physiological stress
- Vaccination scheduling — discuss spacing with knowledgeable pediatrician for mito-vulnerable kids

## 5. Early childhood (18 months - 5 years)

**Goal:** Maintain through the [[HYP-0073 Developmental timing state-transition disorder]] critical window

- Mito cocktail (pediatric-dosed) if indicated by workup
- Avoidance of mitotoxic medications, especially valproate
- Glyphosate avoidance (organic-first food choices)
- Heavy metal load reduction
- Anesthesia planning with mito-aware anesthesiologist if surgery needed
- Ongoing biomarker monitoring (lactate trends, OAT periodically, methylation markers)

## 6. School-age + adolescence

**Goal:** Sustain function; prevent stressor-triggered regression

- Continued mito support if beneficial
- Stress regulation (cortisol affects mitochondrial function)
- Sleep quality (mitochondrial maintenance occurs during sleep)
- Exercise (induces mitochondrial biogenesis)
- Cognitive enrichment + appropriate behavioral therapy

## Atlas connections

- [[topics/interventions/mitochondrial/00_MITOCHONDRIAL_OVERVIEW]] — class overview
- [[Naviaux_Robert]] — 3-Hit framework
- [[Rossignol_Daniel]] — clinical mito autism framework
- [[HYP-0006 Mitochondrial dysfunction (acquired or inherited)]]
- [[HYP-0073 Developmental timing state-transition disorder]]
- [[BIO-0018 Lactate]], [[BIO-0019 Pyruvate]], [[BIO-0020 Lactate-to-pyruvate ratio (L_P)]]
- [[topics/omics/Epigenetics_of_Autism]] — preconception epigenetic optimization layer
""")

# ============================================================
# 3.5C+D — PANS/PANDAS, MCAS, Walsh Biotypes deep dives
# ============================================================
print("\nWriting conditions/subgroups deep dives...")

write_md("topics/conditions_subgroups/PANS_PANDAS_Deep_Dive.md",
"""---
id: PANS-PANDAS-DEEP-DIVE
type: condition_deep_dive
parent: 00_SUBGROUPS_OVERVIEW
audience: clinician, parent
hypothesis: HYP-0074
---

# PANS / PANDAS — Deep Dive

Pediatric Acute-onset Neuropsychiatric Syndrome (PANS) / Pediatric Autoimmune Neuropsychiatric Disorders Associated with Streptococcus (PANDAS) is **a real, identifiable autoimmune subgroup** that is frequently misdiagnosed as autism or treated as primary OCD/anxiety when the actual condition is post-infectious autoantibody-mediated neuropsychiatric disease.

**Atlas record:** [[HYP-0074 PANS_PANDAS — post-infectious autoimmune neuropsychiatric syndrome]]

## Why missing this matters

A child with PANS/PANDAS treated as autism + behavioral therapy gets years of inappropriate intervention. The same child treated with NSAIDs → antibiotics → IVIG → LDN often shows substantial recovery within months. **Failing to recognize PANS/PANDAS is one of the most consequential diagnostic errors in pediatric mental health.**

## Recognition

Look for:
- **Sudden onset** (days, not months) of OCD, tics, anxiety, eating restriction, sensory regression
- **Episodic / waxing-waning course** (not progressive)
- **Symptoms started after an infection** — strep, mycoplasma, Lyme, viral
- **Behavioral regression** from a previously higher functional baseline
- **Concurrent or recent illness in family / school**

## Workup

**Cunningham Panel (Moleculera Biosciences) — primary diagnostic:**
- [[BIO-0067 Anti-tubulin antibody (Cunningham Panel)]]
- [[BIO-0068 Anti-lysoganglioside-GM1 antibody]]
- [[BIO-0069 Anti-dopamine D1 receptor antibody]]
- [[BIO-0070 Anti-dopamine D2 receptor antibody]]
- [[BIO-0071 CaMKII activation]]

**Strep + co-infection panel:**
- [[BIO-0072 ASO (antistreptolysin O)]]
- [[BIO-0073 Anti-DNase B]]
- [[BIO-0124 Mycoplasma pneumoniae IgM_IgG]]
- [[BIO-0125 Borrelia burgdorferi (Lyme) panel]]
- [[BIO-0127 HHV-6 IgG_IgM + PCR]]

**Standard autoimmune broader:**
- ANA, RF, thyroid antibodies, anti-tTG

## Treatment ladder

1. **NSAIDs** — ibuprofen or naproxen, higher dose for 4-6 weeks during acute flare, then taper
2. **Antibiotics** for active infection (penicillin or azithromycin)
3. **Antibiotic prophylaxis** if recurrent (250-500 mg penicillin BID or azithromycin 500 mg every other day)
4. **IVIG** for moderate-severe cases (1-2 g/kg, monthly courses)
5. **Plasmapheresis** for severe IVIG-refractory
6. **LDN** for chronic immune modulation (long-term; [[INT-0006]])
7. **SSRIs** for OCD symptoms (calibrate carefully — some kids paradox)

## Specialty centers

- Stanford PANS Clinic
- Mass General PANS Clinic
- Cohen PANDAS Center NYU
- PANDAS Physicians Network — clinician finder

## Researchers

- **[[Swedo_Sue]]** — NIMH founder of PANDAS framework
- **[[Cunningham_Madeleine]]** — Cunningham Panel architect

## Reliability caveats

Per Hesselmark 2019 *Translational Psychiatry*: Cunningham Panel CaMKII activation elevated in 48% of healthy controls. Position: panel works best as **confirmatory** in clinically-suspected cases, not as screening in low-prior-probability populations.

## Atlas connections

- [[HYP-0074 PANS_PANDAS — post-infectious autoimmune neuropsychiatric syndrome]]
- [[topics/interventions/immune_modulation/00_IMMUNE_OVERVIEW]]
- [[Swedo_Sue]] + [[Cunningham_Madeleine]]
- 7 biomarkers (Cunningham Panel + strep titers)
""")

write_md("topics/conditions_subgroups/MCAS_Deep_Dive.md",
"""---
id: MCAS-DEEP-DIVE
type: condition_deep_dive
parent: 00_SUBGROUPS_OVERVIEW
audience: clinician, parent
hypothesis: HYP-0075
---

# Mast Cell Activation Syndrome (MCAS) in Autism — Deep Dive

Mast cell hyperactivity affects a substantial autism subgroup. Mast cells release >200 mediators (histamine, tryptase, IL-6, TNF-α, prostaglandins, neuropeptides) and couple with microglia to drive neuroinflammation.

**Atlas record:** [[HYP-0075 Mast Cell Activation Syndrome (MCAS) in autism]]

## Recognition

- **Chronic atopic disease** — eczema, asthma, food allergies, recurring rashes
- **GI dysmotility** — abdominal pain, bloating, reflux, food intolerance
- **Dysautonomia** — heart rate / blood pressure / temperature variability
- **Flushing**, hives, intermittent rashes
- **Sleep disturbance**
- **Cognitive features** — "brain fog", behavioral worsening with mast-cell triggers

## Workup

**Mast cell biomarkers:**
- [[BIO-0062 Tryptase (baseline)]] — baseline + during flare; ≥1.2× baseline + 2 ng/mL during flare = MCAS criterion
- [[BIO-0063 N-methylhistamine (urinary)]] — 24-hour collection
- [[BIO-0064 Prostaglandin D2 metabolite (11β-PGF2α)]]
- [[BIO-0065 Chromogranin A]]

**Adjunctive:**
- Cytokine panel (IL-6, TNF-α, IL-1β)
- Total IgE + specific IgEs

## Treatment ladder

1. **H1 + H2 antihistamines** — foundational. Cetirizine 5-10 mg + famotidine 0.5 mg/kg (children).
2. **Cromolyn sodium (oral)** — pre-meal, for GI mast cell stabilization
3. **Ketotifen** — combined H1 + mast cell stabilizer
4. **Quercetin + luteolin** — bioflavonoid stabilizers; luteolin BBB-crossing per [[Theoharides_Theoharis]]
5. **Low-histamine diet** — under nutritionist supervision
6. **LDN** — for chronic immune modulation
7. **Avoidance** — identified individual mast-cell triggers (alcohol, certain medications, environmental triggers)

## Researcher

- **[[Theoharides_Theoharis]]** — mast cell + microglial framework architect; luteolin formulation work

## Atlas connections

- [[HYP-0075 Mast Cell Activation Syndrome (MCAS) in autism]]
- [[MEC-0017 Mast cell activation]]
- [[topics/interventions/immune_modulation/00_IMMUNE_OVERVIEW]]
- 5 mast cell biomarkers + immune cytokine panel
""")

write_md("topics/conditions_subgroups/Walsh_Biotypes.md",
"""---
id: WALSH-BIOTYPES-DEEP-DIVE
type: condition_deep_dive
parent: 00_SUBGROUPS_OVERVIEW
audience: clinician, parent
phenotypes: PHE-0008, PHE-0009, PHE-0010, PHE-0011
---

# Walsh Biotyping — Deep Dive

[[Walsh_William]]'s biotyping framework subdivides methylation-related autism into clinically meaningful subtypes that respond to *different* protocols. Knowing your child's biotype prevents the common error of giving methyl donors to an overmethylator (which makes things worse) or folate to a pyroluric (which can backfire).

## The 4 biotypes

### Undermethylator phenotype ([[PHE-0008]])
- **~30-40% of autism**
- Low whole-blood histamine, low SAM/SAH ratio
- Personality cluster: high inner tension, perfectionism, OCD features, seasonal allergies
- Treatment: Methyl donors (methionine, SAM-e, methyl-B12, sometimes 5-MTHF cautiously)

### Overmethylator phenotype ([[PHE-0009]])
- **~5-10% of autism**
- High whole-blood histamine, high SAM/SAH ratio
- Personality cluster: anxious, low motivation, paradoxical histamine elevation
- Treatment: Folate-cautious; niacinamide, B6, sometimes folate-blocking strategies
- **Methyl donors paradoxically worsen**

### Pyroluria / kryptopyrroluria phenotype ([[PHE-0010]])
- Elevated urinary kryptopyrroles → bind/deplete B6 + zinc
- Stress intolerance, anxiety, mood lability, poor short-term memory
- Treatment: B6 (P5P), zinc, GLA (evening primrose oil), magnesium
- Sample handling matters: kryptopyrroles are light-sensitive

### Copper:Zinc imbalance phenotype ([[PHE-0011]])
- Cu:Zn >1.2 (per [[BIO-0099 Cu_Zn ratio]])
- Hyperactivity, sensory issues, behavioral dysregulation
- Treatment: Zinc supplementation, molybdenum, metallothionein-promoting protocols
- Postpartum depression risk in mothers

## Workup

- [[BIO-0014 Whole-blood histamine]] — biotype proxy
- [[BIO-0003 SAM_SAH ratio]] — methylation capacity
- [[BIO-0099 Cu_Zn ratio]]
- [[BIO-0096 Plasma zinc]] + [[BIO-0098 Plasma copper + ceruloplasmin]]
- [[BIO-0104 Urinary kryptopyrroles]] — pyroluria
- [[BIO-0161 MTHFR C677T genotype]] + [[BIO-0162 MTHFR A1298C genotype]]

## Clinical access

- **Mensah Medical** (Chicago) — Walsh-trained
- **Walsh Research Institute** — provider directory
- **MAPS-trained physicians** with methylation focus

## Atlas connections

- [[Walsh_William]] — framework architect
- [[PHE-0008]], [[PHE-0009]], [[PHE-0010]], [[PHE-0011]]
- [[topics/interventions/methylation_pathway/00_METHYLATION_OVERVIEW]]
- [[PROT-0001 Walsh biotyping protocol]]
""")

# ============================================================
# 3.5E — Protocols index
# ============================================================
print("\nWriting protocols index...")

write_md("topics/protocols/00_PROTOCOLS_INDEX.md",
"""---
id: PROTOCOLS_INDEX
type: section_index
parent: 00_TOPICS_INDEX
audience: clinician, parent
---

# 🩺 Named Clinical Protocols

The atlas tracks **10 named clinical protocols** — frameworks developed by specific researchers / clinics that bundle test panels + intervention stacks for stratified populations. These represent the operational implementation of biomedical autism medicine.

## Methylation pathway

- **[[PROT-0001 Walsh biotyping protocol]]** — biotype → biotype-specific nutrient (Mensah Medical)
- **[[PROT-0002 Frye FRAA + leucovorin protocol]]** — FRAA test → leucovorin trial (atlas calibration anchor)
- **[[PROT-0003 Yasko SNP-targeted methylation protocol]]** — 30+ SNPs → sequential nutrient (Holistic Health Inc)
- **[[PROT-0004 Neubrander methyl-B12 SC protocol]]** — methylcobalamin SC every 3 days

## Comprehensive functional pediatric

- **[[PROT-0005 Bock Plan (4-A epidemic framework)]]** — autism + ADHD + asthma + allergies
- **[[PROT-0006 Klinghardt protocols]]** — chronic infection + environmental toxicant focus
- **[[PROT-0007 MAPS framework]]** — Medical Academy of Pediatric Special Needs curriculum
- **[[PROT-0008 ARI (Autism Research Institute) DAN! protocol legacy]]** — historical foundation; superseded by MAPS

## Microbiome interventions

- **[[PROT-0009 Hazan familial FMT protocol]]** — sibling-donor FMT under FDA IND (ProgenaBiome)
- **[[PROT-0010 Adams MTT (Microbiota Transfer Therapy)]]** — Phase 2 RCT-grade structured oral protocol (ASU)

## How to choose

| Child's clinical picture | Best-fit protocol |
|---|---|
| FRAA-positive, language-impaired | [[PROT-0002 Frye FRAA + leucovorin protocol]] |
| Methylation-driven, complex SNPs | [[PROT-0001 Walsh]] or [[PROT-0003 Yasko]] |
| 4-A cluster (autism + ADHD + atopic) | [[PROT-0005 Bock Plan]] |
| Chronic infection / mold / Lyme | [[PROT-0006 Klinghardt]] |
| GI symptoms, severe Bif depletion | [[PROT-0009 Hazan FMT]] |
| Microbiome with formal trial preference | [[PROT-0010 Adams MTT]] |
| Beginning biomedical autism care | [[PROT-0007 MAPS framework]] (find a MAPS clinician) |

Each protocol is a tested, peer-reviewed-or-clinically-validated framework. They aren't mutually exclusive — many clinicians integrate multiple frameworks based on the child's profile.

## Atlas connections

- [[topics/interventions/00_INTERVENTIONS_INDEX]]
- [[topics/biomarkers/00_BIOMARKERS_INDEX]] — workup panels match protocols
- [[00_RESEARCHERS_INDEX]] — protocol architects all have researcher pages
""")

print("\n3.5F + 3.5G + 3.5H + condition deep dives + protocols index done.")
