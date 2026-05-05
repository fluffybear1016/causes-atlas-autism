---
id: PHE-0005-DEEP-DIVE
type: phenotype_deep_dive
parent: 00_PHENOTYPES_OVERVIEW
audience: clinician, researcher
phenotype: PHE-0005
---

# PHE-0005 — mTOR Pathway Syndromic Phenotype (TSC, PTEN)

## One-line summary

A small but mechanistically clear subset (~1–3% of autism) carries pathogenic variants in **negative regulators of the mTOR pathway** — most commonly **TSC1, TSC2, PTEN, NF1, AKT3, MTOR** itself, or related RAS-MAPK–PI3K–mTOR cascade members. The result is **constitutively elevated mTOR signaling**, dysregulated dendritic protein synthesis, abnormal dendritic spine morphology, and disrupted synaptic plasticity. **Rapamycin/sirolimus is FDA-approved for TSC** and represents the cleanest "molecular target → drug" story in autism.

## Neurobiochemistry

### The mTOR signaling cascade

mTOR (mechanistic Target Of Rapamycin) is a serine-threonine kinase that integrates growth signals, nutrient availability, and stress to regulate **protein synthesis, autophagy, ribosome biogenesis, and metabolism**. It exists as two complexes:

- **mTORC1** — Raptor-containing; rapamycin-sensitive; regulates translation (via 4E-BP1, S6K1) and autophagy (via ULK1)
- **mTORC2** — Rictor-containing; rapamycin-less-sensitive; regulates AKT, cytoskeleton

The cascade upstream:

```
Growth factors / insulin → RTK → PI3K → AKT → TSC1/TSC2 complex (inhibitor) → Rheb-GTP → mTORC1
Amino acids → Ragulator/RagGTPases → mTORC1 lysosomal recruitment
Energy stress → AMPK → TSC2 → mTORC1 inhibition
PTEN (phosphatase) → opposes PI3K → indirect mTORC1 inhibition
```

mTORC1 activates → **4E-BP1 phosphorylation** (releases eIF4E for cap-dependent translation) + **S6K1 phosphorylation** (phosphorylates rpS6, eIF4B, eEF2K). Net: protein synthesis is upregulated.

### How loss-of-function variants drive the phenotype

| Gene | Function | Loss-of-function consequence |
|---|---|---|
| **TSC1 / TSC2** | Hamartin / Tuberin — direct GAP for Rheb (mTORC1 OFF switch) | Rheb stays GTP-bound → constitutive mTORC1 activation |
| **PTEN** | Phosphatase — converts PIP3 → PIP2, opposes AKT activation | AKT hyperactive → TSC1/2 phosphorylated/inactivated → mTORC1 active |
| **NF1** | RasGAP — converts Ras-GTP → Ras-GDP | Ras hyperactive → MAPK + PI3K both activated; mTOR downstream |
| **DEPDC5** | GATOR1 component — amino acid sensing OFF switch | mTORC1 active under low-amino-acid conditions |
| **AKT3** | Direct AKT family kinase | Constitutive activation → mTORC1 |
| **STRADA, LKB1** | Regulators of AMPK | Loss of energy-sensing OFF switch |

**Net effect across all of these: mTORC1 stays ON when it should be regulated.** This is the "mTORopathy" core lesion — heterogeneous in genetic etiology but convergent at the pathway level.

### Dendritic protein synthesis dysregulation

In typical neurons, **local dendritic protein synthesis** at synapses is rapidly modulated by activity. Specific proteins are translated on-demand:
- AMPA receptor subunits
- PSD-95
- Arc (activity-regulated cytoskeleton-associated)
- CaMKII
- Synaptic adhesion molecules

mTORC1 controls the rate of this on-demand translation. **Constitutive mTORC1 activation → constant high baseline translation → loss of activity-dependent regulation**. The synapse cannot distinguish "fire and modify" from baseline — plasticity becomes uncoupled from activity.

This converges with [[PHE-0006 Fragile X (FMR1)|Fragile X]]: FMRP is an RNA-binding protein that **brakes** mTOR-driven translation. FMR1 loss → unbraked translation, similar to mTOR over-activation. Both phenotypes manifest with similar dendritic spine + synaptic abnormalities, even though the upstream lesion differs.

### Autophagy disruption

mTORC1 actively suppresses autophagy via ULK1 phosphorylation. Constitutive mTORC1 → **chronic autophagy suppression** → accumulation of damaged organelles, aggregated proteins, dysfunctional mitochondria. This is implicated in:
- **Cortical tubers** in TSC — abnormal cell types accumulating in malformed cortical patches
- **Macrocephaly** in PTEN syndrome — failure to prune cellular content
- **Mitochondrial dysfunction** secondary to mitophagy failure

### Cellular hypertrophy + macrocephaly

Persistent mTORC1 → cells grow larger (more protein synthesis, ribosome biogenesis, lipid synthesis). In neurons, this translates to:
- **Increased cell soma size**
- **Increased dendrite arbor complexity** (initially)
- **Macrocephaly** (especially PTEN — head circumference >97th percentile is one of the clinical screening criteria for PTEN testing in autism)

### Hypothesis-level mTOR phenotype heterogeneity

Within mTORopathy autism, sub-phenotypes:
- **Tuberous Sclerosis Complex (TSC)** — multisystem (cortical tubers, cardiac rhabdomyomas, renal angiomyolipomas, skin findings); ~50% have autism
- **PTEN Hamartoma Tumor Syndrome (Cowden, Bannayan-Riley-Ruvalcaba)** — macrocephaly, hamartomas, increased cancer risk, autism in subset
- **Megalencephaly-Capillary Malformation (MCAP)** — somatic PIK3CA / AKT3 / MTOR mosaic variants
- **Hemimegalencephaly** — somatic mTOR pathway variants in one hemisphere
- **Focal Cortical Dysplasia type II** — somatic TSC / DEPDC5 variants in the dysplastic region

## Biophysics

### Dendritic spine morphology

Healthy mature spines are **mushroom-shaped**: thin neck, large head, stable PSD with mature AMPA/NMDA receptors. Immature spines are **filopodial / thin / stubby**. In mTORopathy:
- **Increased spine density** (initially) — too many spines
- **Higher proportion immature filopodial / thin spines** — suggests pruning/maturation deficit
- **Larger spines on average** but with reduced functional clustering
- The same morphology is seen in FXS — convergent biophysics from divergent genetics

### Cortical tubers and biophysical heterogeneity

In TSC, cortical tubers are **focal regions of disrupted lamination** containing dysmorphic neurons (giant cells, balloon cells). These lesions are detectable on:
- **MRI cortical thickness** ([[BIO-0137]]) — focal abnormalities
- **MRI brain volumetry** ([[BIO-0138]]) — cortical tubers as discrete lesions
- **DTI fractional anisotropy** ([[BIO-0139]]) — reduced FA in white matter near tubers
- **PET-FDG** — focal hypometabolism in tubers

Tuber **burden + location** (tuber-to-brain ratio, frontal-temporal predominance) predicts autism risk in TSC more than any other variable.

### Glutamate-GABA imbalance

mTOR overactivation in cortex shifts E:I balance toward excitation:
- **Glutamate elevated** in cortical regions (1H-MRS [[BIO-0141]])
- **GABA reduced** relatively
- **Increased seizure risk** — TSC almost universally has epilepsy (>80%); PTEN spectrum has epilepsy in ~25%
- **Background EEG abnormalities** common

### Network connectivity disruption

[[BIO-0140 Resting-state fMRI default mode network connectivity]] in mTOR-pathway autism shows:
- **Hyperconnectivity** in some networks (especially in PTEN macrocephaly subset)
- **Hypoconnectivity** in long-range networks
- DTI white matter abnormalities correlating with severity

This biophysical signature partly overlaps with general autism connectomic patterns but is more pronounced in the syndromic form.

### EEG signatures

- **Epileptiform activity** — common (especially TSC, where infantile spasms are often the presenting feature)
- **Background slowing** during periods of high seizure burden
- [[BIO-0143 EEG resting-state spectral power]] often abnormal across multiple bands
- [[BIO-0144 ERP P300]] / [[BIO-0145 ERP MMN]] reduced — attention + auditory processing biomarkers

### Cerebellar involvement

Particularly in PTEN syndrome:
- **Cerebellar hypertrophy** in some PTEN cases (megalencephaly extends to cerebellum)
- **Lhermitte-Duclos disease** — dysplastic gangliocytoma of cerebellum, pathognomonic for Cowden syndrome
- Cerebellar contribution to autism phenotype includes motor coordination + procedural learning deficits

## Phenotype profile

### Recognition

**TSC red flags:**
- Infantile spasms (often first sign)
- Cardiac rhabdomyomas (prenatal ultrasound or neonatal echo)
- Hypopigmented "ash-leaf" macules on skin
- Subependymal nodules on brain MRI
- Family history of TSC (autosomal dominant; ~30% inherited, ~70% de novo)

**PTEN red flags:**
- **Macrocephaly** (head circumference >2.5 SD above mean, or >97.5th percentile) — **single most useful clinical autism screening flag for PTEN testing**
- Family history of cancers (breast, thyroid, endometrial, colon, kidney)
- Dermatologic findings (trichilemmomas, papillomatous lesions — usually adult-onset)
- Penile/glans pigmented macules in males (BRRS feature)

**General mTORopathy features in autism:**
- **Severe / global developmental delay** more common than mild ASD
- **Epilepsy** common
- **Hypotonia + motor delay**
- **Macrocephaly** disproportionately frequent
- **Autistic regression** less typical (more often plateaued from early infancy)

### Diagnostic biomarkers + workup

**Tier 1 (clinical):**
- Head circumference + growth charts (macrocephaly screening)
- Detailed family history (cancer, seizures, autism)
- Skin examination (hypopigmented macules, hamartomas)
- Echocardiogram (TSC suspicion)

**Tier 2 (genetic):**
- **Targeted gene panel: TSC1, TSC2, PTEN** for any child with:
  - Macrocephaly + autism, OR
  - Infantile spasms + autism, OR
  - Multiple café-au-lait or hypopigmented macules, OR
  - Family history of mTOR-pathway syndrome
- Whole-exome sequencing for broader pickup (DEPDC5, NF1, AKT3, MTOR, MCAP-associated)

**Tier 3 (imaging):**
- [[BIO-0137 MRI cortical thickness]] — tubers, dysplasia
- [[BIO-0138 Total brain volume / amygdala / cerebellar vermis volumetry]] — macrocephaly, cerebellar findings
- [[BIO-0139 DTI fractional anisotropy]] — white matter
- [[BIO-0141 1H-MRS NAA / choline / creatine / glutamate-GABA]] — glutamate excess
- [[BIO-0140 Resting-state fMRI default mode network connectivity]]

**Tier 4 (functional):**
- **EEG** — seizure activity, [[BIO-0143]] spectral power, [[BIO-0144]] P300, [[BIO-0145]] MMN
- Renal ultrasound (TSC angiomyolipoma surveillance)
- Ophthalmology (TSC retinal hamartomas)
- Dermatology
- Cancer surveillance (PTEN — adolescent/adult)

## Interventions matched to phenotype

**Direct mTOR pathway:**
- **[[INT-0036]] Rapamycin (sirolimus)** — FDA-approved for TSC angiomyolipomas + SEGAs; off-label for autism behavioral/cognitive phenotype
  - Pediatric off-label dosing aims for trough **3-7 ng/mL** (lower than the transplant-immunosuppression range of 5-15 ng/mL)
  - Monitoring: trough levels q3-6 months; lipids, blood counts, mucosal effects
  - See [[topics/interventions/drug_repurposing/Rapamycin]]
- **Everolimus** — FDA-approved for TSC SEGAs + epilepsy
- Both can reduce seizure frequency in TSC
- Behavioral / cognitive response in autism is mixed — some children show improvements; trial duration weeks to months for assessment

**Anti-seizure (in epilepsy-positive subsets):**
- **Vigabatrin** — first-line for TSC infantile spasms (irreversible visual field loss is the trade-off)
- **Cannabidiol** (Epidiolex) — FDA-approved for TSC seizures
- Standard AED selection per epileptologist

**Supportive (cross-phenotype):**
- Mitochondrial cocktail (mTOR overactivation suppresses mitophagy; mito support indirectly helps)
- Anti-inflammatory bundle (mTORC1 cross-talks with NF-κB)
- Standard developmental therapies (speech, OT, ABA-or-equivalent)

**Avoid in this phenotype:**
- Avoidance of growth-factor-rich high-dose protocols when not needed (could exacerbate mTOR activation in theory)
- Caution with high-dose insulin-stimulating regimens
- Surveillance for renal AMLs in TSC (sirolimus shrinks them; surgery if symptomatic)
- Cancer surveillance per syndrome (PTEN — breast/thyroid/colon screening)

**Specialty centers:**
- TSC Alliance Clinics network
- PTEN Clinical Research Consortium
- Children's Hospital genetics clinics with rapid panels

## Researchers

- **[[Sahin_Mustafa]]** — TSC + autism + neurology (Boston Children's)
- **[[Eichler_Evan]]** — high-risk gene discovery + de novo variants
- **[[Iossifov_Ivan]]** — Simons Simplex Collection genetics
- **[[Buxbaum_Joseph]]** — autism genetics (Mount Sinai)
- **[[Kwiatkowski_David]]** — TSC molecular biology
- **[[Eng_Charis]]** — PTEN clinical genetics

## Primary literature

- **Krueger DA, Northrup H. 2013** ([PMID 24053983](https://pubmed.ncbi.nlm.nih.gov/24053983/), *Pediatr Neurol*) — *"Tuberous sclerosis complex surveillance and management: recommendations of the 2012 International Tuberous Sclerosis Complex Consensus Conference"* — TSC clinical consensus
- **Northrup H, Krueger DA, et al. 2013** ([PMID 24053982](https://pubmed.ncbi.nlm.nih.gov/24053982/), *Pediatr Neurol*) — *"Tuberous sclerosis complex diagnostic criteria update"* — companion criteria paper
- **Krueger DA, Care MM, Holland K, et al. 2010** ([PMID 21047224](https://pubmed.ncbi.nlm.nih.gov/21047224/), *N Engl J Med*) — *"Everolimus for subependymal giant-cell astrocytomas in tuberous sclerosis"* — pivotal mTOR-inhibitor trial
- **Tilot AK, Frazier TW 2nd, Eng C. 2015** ([PMID 25916396](https://pubmed.ncbi.nlm.nih.gov/25916396/), *Neurotherapeutics*) — *"Balancing proliferation and connectivity in PTEN-associated autism spectrum disorder"* — PTEN biology synthesis
- **Sahin M, Sur M. 2015** ([PMID 26472761](https://pubmed.ncbi.nlm.nih.gov/26472761/), *Science*) — *"Genes, circuits, and precision therapies for autism and related neurodevelopmental disorders"* — mTOR + circuit biology synthesis
- **Tsai PT, Hull C, Chu Y, et al. 2012** ([PMID 22763451](https://pubmed.ncbi.nlm.nih.gov/22763451/), *Nature*) — *"Autistic-like behaviour and cerebellar dysfunction in Purkinje cell Tsc1 mutant mice"* — cerebellar Tsc1 mouse model
- **Bourgeron T. 2015** ([PMID 26289574](https://pubmed.ncbi.nlm.nih.gov/26289574/), *Nat Rev Neurosci*) — *"From the genetic architecture to synaptic plasticity in autism spectrum disorder"* — synapse genetics framework

## Atlas connections

- [[PHE-0005 mTOR pathway syndromic (TSC, PTEN)]] — atlas record
- [[HYP-0029 mTOR pathway syndromic (TSC_PTEN)]] — hypothesis record
- [[topics/interventions/drug_repurposing/Rapamycin]] — primary intervention
- [[topics/interventions/drug_repurposing/00_DRUG_REPURPOSING_OVERVIEW]] — class overview
- [[Sahin_Mustafa]] + [[Eichler_Evan]] + others — researchers
- [[Hannah Poling framework]] — strong-genetic-susceptibility example
