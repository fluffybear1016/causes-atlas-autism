---
id: DRUG-REPURPOSING-OVERVIEW
type: intervention_class_overview
class: drug_repurposing
parent: 00_INTERVENTIONS_INDEX
audience: parent, clinician
key_atlas_links:
  - INT-0036 (Rapamycin)
  - INT-0037 (Metformin)
  - INT-0006 (Low-dose naltrexone)
status: in_development
---

# 🔄 Drug Repurposing for Autism — Overview

Drug repurposing means using FDA-approved drugs from other indications off-label for autism, in stratified subgroups where mechanism predicts benefit. This is one of the highest-leverage approaches in pediatric biomedical autism medicine because:

1. The drugs are already approved for safety
2. They're commercially available
3. Cost is typically low (generic in most cases)
4. Mechanism is often well-characterized in the original indication

The catch: most autism trials of repurposed drugs are unstratified, producing mixed results that mainstream interpretation calls "doesn't work." Per [[CLAUDE]] §9, mixed results in unstratified trials almost always mean responder vs non-responder — the trick is identifying the right subgroup.

## When this class fits

Strong indication:
- Specific genetic finding that maps to a known drug target (TSC1/2 → rapamycin; SHANK3 → IGF-1)
- Specific mechanism finding from biomarker workup (NKCC1 chloride imbalance → bumetanide)
- Inflammatory subgroup unresponsive to first-line approaches
- Severe presentation where exotic approaches are warranted

Less ideal:
- First-line intervention before workup
- Casual "let's try this" — these are real drugs with real risks

## The repurposed drug catalog

Each drug in the atlas as INT-XXXX with formal evidence_links + sources. The deep-dive pages below will be built out systematically per CLAUDE.md Session 3.5F roadmap.

### Mechanism-targeted (gene-stratified) — highest precision

**[[topics/interventions/drug_repurposing/Rapamycin|Rapamycin (sirolimus)]]** ([[INT-0036]] — csrs 67.0)
- mTOR inhibitor; FDA-approved for TSC and immunosuppression
- Best evidence in TSC1/2, PTEN syndrome, NF1 — children with mTOR-pathway variants
- Dose: 0.5-2 mg twice weekly
- Contested but emerging as more accessible

**Bumetanide** *(deep-dive page pending)*
- NKCC1 inhibitor; FDA-approved diuretic
- Forces the GABA developmental switch in chloride-imbalance subgroup
- [[BenAri_Yehezkel]] foundational mechanism
- Phase 3 RCT mixed results (effect heterogeneity per [[CLAUDE]] §9 — large effect in chloride-imbalanced subgroup)
- Dose: 0.5-2 mg/day; potassium monitoring required

**Suramin (low-dose)** *(deep-dive page pending)*
- Antipurinergic agent
- [[Naviaux_Robert]] 2017 Phase I/II RCT showed core symptom improvements
- PMID 28695149
- Toxicity profile limits broad clinical use; not commercially available for autism in US
- Concept-validating for [[Naviaux_Robert]] 3-Hit framework

### Synaptic / glutamatergic modulators

**Memantine** ([[INT-0038]] — csrs 46.9)
- NMDA receptor antagonist; FDA-approved for Alzheimer's
- Mixed RCT results; some response in subgroups
- Dose: 5-20 mg/day

**Riluzole** ([[INT-0039]] — csrs 25.7)
- Glutamate modulator; FDA-approved for ALS
- Small autism trials with limited signal
- Dose: 50-200 mg/day

**Acamprosate** *(in development)*
- GABAergic modulator (originally for alcohol use disorder)
- Reduces excitatory tone; emerging research

### Metabolic / insulin-pathway

**Metformin** ([[INT-0037]] — csrs 62.4)
- AMPK activator + microbiome modulator
- Long-term clinical experience in diabetes; emerging autism / metabolic relevance
- Dose: 500-1000 mg/day
- Caution: Mitochondrial impact in vulnerable kids needs evaluation

**Pioglitazone** *(deep-dive page pending)*
- PPAR-γ agonist (diabetes drug)
- Anti-inflammatory; emerging in chronic neuroinflammation contexts
- Dose: 15-30 mg/day
- Caution: Weight gain, fluid retention

### Neuroinflammation / microglial-targeting

**[[topics/interventions/immune_modulation/00_IMMUNE_OVERVIEW|Low-dose naltrexone (LDN)]]** ([[INT-0006]] — csrs 50.6)
- Sub-clinical opioid receptor modulation; paradoxical anti-inflammatory
- Compounded prescription
- Covered in detail in immune modulation section

**Minocycline** *(deep-dive page pending)*
- Tetracycline with documented microglial-modulating activity
- Anti-inflammatory; long clinical history
- Dose: 50-100 mg twice daily
- Caution: Permanent skin discoloration possible with long-term use

**Sulindac** *(deep-dive page pending)*
- COX-2-selective NSAID
- Emerging neuroinflammation research

### Neurosteroids and hormonal

**Allopregnanolone** *(deep-dive page pending)*
- Endogenous neurosteroid; positive GABA-A modulator
- Available as ganaxolone (FDA-approved for CDKL5)
- Calming / anxiolytic; emerging research in epileptic ASD

**Oxytocin** *(see [[topics/interventions/peptides/00_PEPTIDES_OVERVIEW]])*
- Technically a peptide; covered in peptides section

### Cellular metabolism modulators

**Trehalose** *(deep-dive page pending)*
- Disaccharide; promotes autophagy and mitophagy
- Clearance of damaged mitochondria
- Emerging research in neurodegenerative + neurodevelopmental contexts
- Dose: typically 5-15 g/day

**Lovastatin** *(deep-dive page pending)*
- Statin with FXR / cholesterol pathway effects
- Some preclinical autism / Fragile X work
- Caution: Statins are mitochondrial-toxic (CoQ10 depletion)

### Microbiome modulators

**Low-dose ivermectin** *(in atlas as observation)*
- [[Hazan_Sabine]] documented microbiome effects (Bifidobacterium increases in 24 hours)
- Caution: [[Hazan_Sabine]] also warns can DEPLETE Bifidobacterium in young kids who still have intact populations
- Strain-specific decision; sequencing-guided

**Vancomycin (oral, non-absorbable)**
- Targets Clostridia overgrowth
- Anecdotal autism-behavior improvement when HPHPA elevated
- Use case-by-case under physician supervision

### Antiviral

**Valacyclovir / acyclovir** *(in development)*
- For HHV-6 / EBV reactivation contexts
- Some autism subgroups with chronic viral involvement

## How to use this class

This is **prescription-required, physician-supervised intervention territory**. The repurposed drugs in this class are not over-the-counter supplements. They require:

1. **Specific indication** — biomarker, genetic finding, or strong clinical rationale
2. **Knowledgeable prescriber** — MAPS-trained, functional medicine pediatrician, or specialist familiar with the specific drug
3. **Monitoring** — labs, side effect tracking, response measurement
4. **Calibration** — dosing requires titration

## Where the field is going

Per CLAUDE.md Session 3.5F roadmap:

- **Systematic OpenTargets / ClinicalTrials.gov scrape** for additional repurposing candidates
- **Per-drug deep-dive pages** for each candidate (Rapamycin, Bumetanide, Suramin, Memantine, Metformin, Pioglitazone, Minocycline, Allopregnanolone, Trehalose, Low-dose ivermectin)
- **Genotype-stratified intervention matching** — which child fits which drug
- **Combination / sequencing logic** — drug-drug interactions, ordering protocols

Multiple major academic centers run repurposed-drug autism trials:
- Duke ([[Kurtzberg_Joanne]]) — beyond cord blood
- Albert Einstein ([[Hollander_Eric]]) — IGF-1 SHANK3 trials
- UCSD ([[Naviaux_Robert]]) — antipurinergic line
- Various international groups

## Atlas connections

- **[[INT-0006 Low-dose naltrexone (LDN)]]**, **[[INT-0036 Rapamycin (sirolimus)]]**, **[[INT-0037 Metformin]]**, **[[INT-0038 Memantine]]**, **[[INT-0039 Riluzole]]** — formal atlas interventions
- **[[topics/interventions/immune_modulation/00_IMMUNE_OVERVIEW]]** — overlap on LDN, minocycline
- **[[BenAri_Yehezkel]]** — bumetanide / GABA developmental switch
- **[[Naviaux_Robert]]** — suramin / antipurinergic
- **[[Hollander_Eric]]** — IGF-1 / SHANK3 stratified pharmacology
- **[[CLAUDE]] §9** — effect heterogeneity principle for interpreting repurposed drug trial results

## Bottom line

Drug repurposing is the highest-precision intervention class when the right drug is matched to the right subgroup. Rapamycin in TSC kids, bumetanide in chloride-imbalanced kids, suramin in CDR-driven kids — these are mechanism-targeted in a way that broad-spectrum interventions can't be.

The catch is the matching. Without proper biomarker / genetic workup, repurposed drugs become guesswork. With proper workup, they can be transformative.

This section is in active development — per-drug deep-dive pages being built out systematically. Until those are live, individual drugs are documented in their atlas INT-XXXX records.
