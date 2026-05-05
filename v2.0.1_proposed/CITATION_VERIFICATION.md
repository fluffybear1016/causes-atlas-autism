---
type: citation_audit
title: "Citation verification — orphan-wiring proposal"
---

# Citation verification report

Every PMID in this report came from a live [NCBI eutils esearch](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi) call, not from memory. For each candidate edge in the orphan-wiring proposal, the search query is shown along with the top hits ranked by PubMed relevance + a deterministic title-overlap score. The chosen PMID is the highest-scoring hit where the title contains the expected biology terms.

_Run: 2026-04-28T02:13:59+00:00_

## CAND-0001: HYP-0025 → MEC-0002

**Edge table:** `hypothesis_mechanism_edges`  
**Relation:** `acts_through`  
**Claim:** Maternal viral infection drives sustained fetal neuroinflammation via maternal cytokine surge.  
**Query:** `maternal immune activation autism neuroinflammation cytokine`

**Chosen PMID:** [34768946](https://pubmed.ncbi.nlm.nih.gov/34768946/) — Zawadzka A (2021) *International journal of molecular sciences* — The Role of Maternal Immune Activation in the Pathogenesis of Autism: A Review of the Evidence, Proposed Mechanisms and Implications for Treatment.
**Second PMID:** [38398873](https://pubmed.ncbi.nlm.nih.gov/38398873/) — Suprunowicz M (2024) *Nutrients* — Between Dysbiosis, Maternal Immune Activation and Autism: Is There a Common Pathway?

Top candidates considered:

| Score | PMID | Year | First author | Journal | Title |
|------|------|------|--------------|---------|-------|
| 24 | [34768946](https://pubmed.ncbi.nlm.nih.gov/34768946/) | 2021 | Zawadzka A | International journal of molecular sciences | The Role of Maternal Immune Activation in the Pathogenesis of Autism: A Review of the Evidence, Prop… |
| 24 | [38398873](https://pubmed.ncbi.nlm.nih.gov/38398873/) | 2024 | Suprunowicz M | Nutrients | Between Dysbiosis, Maternal Immune Activation and Autism: Is There a Common Pathway? |
| 24 | [28698032](https://pubmed.ncbi.nlm.nih.gov/28698032/) | 2018 | Bilbo SD | Experimental neurology | Beyond infection - Maternal immune activation by environmental factors, microglial development, and … |
| 21 | [39182588](https://pubmed.ncbi.nlm.nih.gov/39182588/) | 2024 | Zeng X | Brain, behavior, and immunity | Exogenous PD-L1 binds to PD-1 to alleviate and prevent autism-like behaviors in maternal immune acti… |
| 16 | [38715090](https://pubmed.ncbi.nlm.nih.gov/38715090/) | 2024 | Osman HC | Journal of neuroinflammation | Impact of maternal immune activation and sex on placental and fetal brain cytokine and gene expressi… |

## CAND-0002: HYP-0025 → MEC-0005

**Edge table:** `hypothesis_mechanism_edges`  
**Relation:** `acts_through`  
**Claim:** MIA produces persistent microglial priming in offspring.  
**Query:** `maternal immune activation microglia offspring brain autism`

**Chosen PMID:** [28698032](https://pubmed.ncbi.nlm.nih.gov/28698032/) — Bilbo SD (2018) *Experimental neurology* — Beyond infection - Maternal immune activation by environmental factors, microglial development, and relevance for autism spectrum disorders.
**Second PMID:** [38990389](https://pubmed.ncbi.nlm.nih.gov/38990389/) — Mastenbroek LJM (2024) *Seminars in immunopathology* — The role of microglia in early neurodevelopment and the effects of maternal immune activation.

Top candidates considered:

| Score | PMID | Year | First author | Journal | Title |
|------|------|------|--------------|---------|-------|
| 20 | [28698032](https://pubmed.ncbi.nlm.nih.gov/28698032/) | 2018 | Bilbo SD | Experimental neurology | Beyond infection - Maternal immune activation by environmental factors, microglial development, and … |
| 19 | [38990389](https://pubmed.ncbi.nlm.nih.gov/38990389/) | 2024 | Mastenbroek LJM | Seminars in immunopathology | The role of microglia in early neurodevelopment and the effects of maternal immune activation. |
| 16 | [35963885](https://pubmed.ncbi.nlm.nih.gov/35963885/) | 2023 | Loayza M | Pediatric research | Maternal immune activation alters fetal and neonatal microglia phenotype and disrupts neurogenesis i… |
| 15 | [38848212](https://pubmed.ncbi.nlm.nih.gov/38848212/) | 2024 | Batorsky R | Cell reports | Hofbauer cells and fetal brain microglia share transcriptional profiles and responses to maternal di… |
| 14 | [34768946](https://pubmed.ncbi.nlm.nih.gov/34768946/) | 2021 | Zawadzka A | International journal of molecular sciences | The Role of Maternal Immune Activation in the Pathogenesis of Autism: A Review of the Evidence, Prop… |

## CAND-0003: HYP-0025 → MEC-0017

**Edge table:** `hypothesis_mechanism_edges`  
**Relation:** `acts_through`  
**Claim:** Maternal mast-cell activation contributes to BBB permeability changes downstream of MIA.  
**Query:** `mast cell activation autism brain blood-brain barrier`

**Chosen PMID:** [34575637](https://pubmed.ncbi.nlm.nih.gov/34575637/) — Theoharides TC (2021) *Journal of personalized medicine* — Ways to Address Perinatal Mast Cell Activation and Focal Brain Inflammation, including Response to SARS-CoV-2, in Autism Spectrum Disorder.
**Second PMID:** [21193035](https://pubmed.ncbi.nlm.nih.gov/21193035/) — Theoharides TC (2012) *Biochimica et biophysica acta* — Mast cell activation and autism.

Top candidates considered:

| Score | PMID | Year | First author | Journal | Title |
|------|------|------|--------------|---------|-------|
| 20 | [34575637](https://pubmed.ncbi.nlm.nih.gov/34575637/) | 2021 | Theoharides TC | Journal of personalized medicine | Ways to Address Perinatal Mast Cell Activation and Focal Brain Inflammation, including Response to S… |
| 18 | [21193035](https://pubmed.ncbi.nlm.nih.gov/21193035/) | 2012 | Theoharides TC | Biochimica et biophysica acta | Mast cell activation and autism. |
| 14 | [41751904](https://pubmed.ncbi.nlm.nih.gov/41751904/) | 2026 | Katiraei P | International journal of molecular sciences | Gut-Brain Inflammation and Disrupted Homeostasis Due to Activation of Mast Cells and Microglia. |
| 12 | [27351598](https://pubmed.ncbi.nlm.nih.gov/27351598/) | 2016 | Theoharides TC | Translational psychiatry | Atopic diseases and inflammation of the brain in the pathogenesis of autism spectrum disorders. |
| 12 | [33818491](https://pubmed.ncbi.nlm.nih.gov/33818491/) | 2021 | Bhuiyan P | Neural regeneration research | Neuroimmune connections between corticotropin-releasing hormone and mast cells: novel strategies for… |

## CAND-0004: HYP-0025 → PHE-0003

**Edge table:** `intervention_phenotype_edges`  
**Relation:** `manifests_as`  
**Claim:** Prenatal viral infection epidemiologically associated with autism risk and regressive presentation.  
**Query:** `maternal infection pregnancy autism risk epidemiology cohort`

**Chosen PMID:** [27287966](https://pubmed.ncbi.nlm.nih.gov/27287966/) — Jiang HY (2016) *Brain, behavior, and immunity* — Maternal infection during pregnancy and risk of autism spectrum disorders: A systematic review and meta-analysis.
**Second PMID:** [25218900](https://pubmed.ncbi.nlm.nih.gov/25218900/) — Lee BK (2015) *Brain, behavior, and immunity* — Maternal hospitalization with infection during pregnancy and risk of autism spectrum disorders.

Top candidates considered:

| Score | PMID | Year | First author | Journal | Title |
|------|------|------|--------------|---------|-------|
| 26 | [27287966](https://pubmed.ncbi.nlm.nih.gov/27287966/) | 2016 | Jiang HY | Brain, behavior, and immunity | Maternal infection during pregnancy and risk of autism spectrum disorders: A systematic review and m… |
| 22 | [25218900](https://pubmed.ncbi.nlm.nih.gov/25218900/) | 2015 | Lee BK | Brain, behavior, and immunity | Maternal hospitalization with infection during pregnancy and risk of autism spectrum disorders. |
| 22 | [36087610](https://pubmed.ncbi.nlm.nih.gov/36087610/) | 2022 | Brynge M | The lancet. Psychiatry | Maternal infection during pregnancy and likelihood of autism and intellectual disability in children… |
| 14 | [41166717](https://pubmed.ncbi.nlm.nih.gov/41166717/) | 2026 | Shook LL | Obstetrics and gynecology | Neurodevelopmental Outcomes of 3-Year-Old Children Exposed to Maternal Severe Acute Respiratory Synd… |
| 14 | [23337946](https://pubmed.ncbi.nlm.nih.gov/23337946/) | 2014 | Brown AS | Molecular psychiatry | Elevated maternal C-reactive protein and autism in a national birth cohort. |

## CAND-0005: HYP-0028 → MEC-0006

**Edge table:** `hypothesis_mechanism_edges`  
**Relation:** `acts_through`  
**Claim:** SFARI Tier-1 synaptic genes converge on synaptic pruning/maturation pathways.  
**Query:** `autism risk genes synapse synaptic pruning convergence SHANK NRXN`

**Chosen PMID:** _NONE — no relevant hit. Review needed._

Top candidates considered:

| Score | PMID | Year | First author | Journal | Title |
|------|------|------|--------------|---------|-------|

## CAND-0006: HYP-0028 → MEC-0007

**Edge table:** `hypothesis_mechanism_edges`  
**Relation:** `acts_through`  
**Claim:** Polygenic risk converges on E/I balance via channelopathies.  
**Query:** `autism excitation inhibition balance GABA glutamate genes`

**Chosen PMID:** [28452083](https://pubmed.ncbi.nlm.nih.gov/28452083/) — Bozzi Y (2018) *The European journal of neuroscience* — Neurobiological bases of autism-epilepsy comorbidity: a focus on excitation/inhibition imbalance.
**Second PMID:** [39221783](https://pubmed.ncbi.nlm.nih.gov/39221783/) — Bryers A (2024) *Biochemical Society transactions* — Progress towards understanding risk factor mechanisms in the development of autism spectrum disorders.

Top candidates considered:

| Score | PMID | Year | First author | Journal | Title |
|------|------|------|--------------|---------|-------|
| 14 | [28452083](https://pubmed.ncbi.nlm.nih.gov/28452083/) | 2018 | Bozzi Y | The European journal of neuroscience | Neurobiological bases of autism-epilepsy comorbidity: a focus on excitation/inhibition imbalance. |
| 11 | [39221783](https://pubmed.ncbi.nlm.nih.gov/39221783/) | 2024 | Bryers A | Biochemical Society transactions | Progress towards understanding risk factor mechanisms in the development of autism spectrum disorder… |
| 11 | [32428529](https://pubmed.ncbi.nlm.nih.gov/32428529/) | 2020 | Lenart J | Toxicology | Altered expression of glutamatergic and GABAergic genes in the valproic acid-induced rat model of au… |
| 9 | [15666334](https://pubmed.ncbi.nlm.nih.gov/15666334/) | 2004 | Polleux F | Mental retardation and developmental disabilities research reviews | Toward a developmental neurobiology of autism. |
| -44 | [34298906](https://pubmed.ncbi.nlm.nih.gov/34298906/) | 2021 | Bassetti D | International journal of molecular sciences | Effects of Mutations in TSC Genes on Neurodevelopment and Synaptic Transmission. |

## CAND-0007: HYP-0028 → MEC-0009

**Edge table:** `hypothesis_mechanism_edges`  
**Relation:** `acts_through`  
**Claim:** TSC, PTEN syndromic mutations confirm mTOR is a major convergence point in ASD.  
**Query:** `autism mTOR pathway TSC PTEN convergence review`

**Chosen PMID:** _NONE — no relevant hit. Review needed._

Top candidates considered:

| Score | PMID | Year | First author | Journal | Title |
|------|------|------|--------------|---------|-------|

## CAND-0008: HYP-0028 → PHE-0005

**Edge table:** `intervention_phenotype_edges`  
**Relation:** `manifests_as`  
**Claim:** TSC/PTEN macrocephaly mTOR-syndromic phenotype.  
**Query:** `PTEN macrocephaly autism mTOR clinical phenotype`

**Chosen PMID:** [25916396](https://pubmed.ncbi.nlm.nih.gov/25916396/) — Tilot AK (2015) *Neurotherapeutics : the journal of the American Society for Experimental NeuroTherapeutics* — Balancing Proliferation and Connectivity in PTEN-associated Autism Spectrum Disorder.
**Second PMID:** [31609537](https://pubmed.ncbi.nlm.nih.gov/31609537/) — Macken WL (2019) *American journal of medical genetics. Part C, Seminars in medical genetics* — PTEN Hamartoma tumor syndrome in childhood: A review of the clinical literature.

Top candidates considered:

| Score | PMID | Year | First author | Journal | Title |
|------|------|------|--------------|---------|-------|
| 17 | [25916396](https://pubmed.ncbi.nlm.nih.gov/25916396/) | 2015 | Tilot AK | Neurotherapeutics : the journal of the American Society for Experimental NeuroTherapeutics | Balancing Proliferation and Connectivity in PTEN-associated Autism Spectrum Disorder. |
| 12 | [31609537](https://pubmed.ncbi.nlm.nih.gov/31609537/) | 2019 | Macken WL | American journal of medical genetics. Part C, Seminars in medical genetics | PTEN Hamartoma tumor syndrome in childhood: A review of the clinical literature. |
| 10 | [40282429](https://pubmed.ncbi.nlm.nih.gov/40282429/) | 2025 | L'Erario FF | Genes | Clinical-Genetic Approach to Conditions with Macrocephaly and ASD/Behaviour Abnormalities: Variants … |
| 9 | [30301738](https://pubmed.ncbi.nlm.nih.gov/30301738/) | 2019 | Oliveira D | Journal of medical genetics | 10q23.31 microduplication encompassing PTEN decreases mTOR signalling activity and is associated wit… |
| 8 | [34048549](https://pubmed.ncbi.nlm.nih.gov/34048549/) | 2021 | Koboldt DC | Brain : a journal of neurology | PTEN somatic mutations contribute to spectrum of cerebral overgrowth. |

## CAND-0009: HYP-0028 → PHE-0006

**Edge table:** `intervention_phenotype_edges`  
**Relation:** `manifests_as`  
**Claim:** FMR1 fragile X autism syndromic phenotype review.  
**Query:** `FMR1 fragile X autism syndrome review clinical`

**Chosen PMID:** [37759552](https://pubmed.ncbi.nlm.nih.gov/37759552/) — Tassone F (2023) *Cells* — Insight and Recommendations for Fragile X-Premutation-Associated Conditions from the Fifth International Conference on FMR1 Premutation.
**Second PMID:** [32026885](https://pubmed.ncbi.nlm.nih.gov/32026885/) — Salcedo-Arellano MJ (2020) *Gaceta medica de Mexico* — Fragile X syndrome: clinical presentation, pathology and treatment.

Top candidates considered:

| Score | PMID | Year | First author | Journal | Title |
|------|------|------|--------------|---------|-------|
| 16 | [37759552](https://pubmed.ncbi.nlm.nih.gov/37759552/) | 2023 | Tassone F | Cells | Insight and Recommendations for Fragile X-Premutation-Associated Conditions from the Fifth Internati… |
| 13 | [32026885](https://pubmed.ncbi.nlm.nih.gov/32026885/) | 2020 | Salcedo-Arellano MJ | Gaceta medica de Mexico | Fragile X syndrome: clinical presentation, pathology and treatment. |
| 13 | [35216055](https://pubmed.ncbi.nlm.nih.gov/35216055/) | 2022 | Protic DD | International journal of molecular sciences | Fragile X Syndrome: From Molecular Aspect to Clinical Treatment. |
| 12 | [28960184](https://pubmed.ncbi.nlm.nih.gov/28960184/) | 2017 | Hagerman RJ | Nature reviews. Disease primers | Fragile X syndrome. |
| 12 | [37664646](https://pubmed.ncbi.nlm.nih.gov/37664646/) | 2023 | Acero-Garcés DO | Colombia medica (Cali, Colombia) | Fragile X Syndrome in children. |

## CAND-0010: INT-0036 → MEC-0013

**Edge table:** `intervention_mechanism_edges`  
**Relation:** `modulates`  
**Claim:** Rapamycin (mTOR inhibitor) → FOXO disinhibition → autophagy.  
**Query:** `rapamycin mTOR FOXO autophagy`

**Chosen PMID:** [31572724](https://pubmed.ncbi.nlm.nih.gov/31572724/) — Schmeisser K (2019) *Frontiers in cell and developmental biology* — Pleiotropic Effects of mTOR and Autophagy During Development and Aging.
**Second PMID:** [35535114](https://pubmed.ncbi.nlm.nih.gov/35535114/) — Anand A (2022) *Journal of clinical and experimental hepatology* — Alterations in Autophagy and Mammalian Target of Rapamycin (mTOR) Pathways Mediate Sarcopenia in Patients with Cirrhosis.

Top candidates considered:

| Score | PMID | Year | First author | Journal | Title |
|------|------|------|--------------|---------|-------|
| 12 | [31572724](https://pubmed.ncbi.nlm.nih.gov/31572724/) | 2019 | Schmeisser K | Frontiers in cell and developmental biology | Pleiotropic Effects of mTOR and Autophagy During Development and Aging. |
| 10 | [35535114](https://pubmed.ncbi.nlm.nih.gov/35535114/) | 2022 | Anand A | Journal of clinical and experimental hepatology | Alterations in Autophagy and Mammalian Target of Rapamycin (mTOR) Pathways Mediate Sarcopenia in Pat… |
| 9 | [30523761](https://pubmed.ncbi.nlm.nih.gov/30523761/) | 2019 | Lee JW | Autophagy | TLR4 (toll-like receptor 4) activation suppresses autophagy through inhibition of FOXO3 and impairs … |
| -44 | [34161185](https://pubmed.ncbi.nlm.nih.gov/34161185/) | 2021 | Kumariya S | Autophagy | Autophagy in ovary and polycystic ovary syndrome: role, dispute and future perspective. |
| -45 | [39113560](https://pubmed.ncbi.nlm.nih.gov/39113560/) | 2024 | Di Rienzo M | Autophagy | Role of AMBRA1 in mitophagy regulation: emerging evidence in aging-related diseases. |

## CAND-0011: INT-0028 → MEC-0013

**Edge table:** `intervention_mechanism_edges`  
**Relation:** `modulates`  
**Claim:** Resveratrol activates SIRT1 → SIRT1 deacetylates FOXO3a → activates antioxidant + autophagy program.  
**Query:** `resveratrol SIRT1 FOXO3 deacetylation`

**Chosen PMID:** [28258028](https://pubmed.ncbi.nlm.nih.gov/28258028/) — Wang X (2017) *Diabetes research and clinical practice* — Resveratrol ameliorates hyperglycemia-induced renal tubular oxidative stress damage via modulating the SIRT1/FOXO3a pathway.
**Second PMID:** [33110391](https://pubmed.ncbi.nlm.nih.gov/33110391/) — Chen H (2020) *International journal of biological sciences* — SIRT1/FOXO3a axis plays an important role in the prevention of mandibular bone loss induced by 1,25(OH)(2)D deficiency.

Top candidates considered:

| Score | PMID | Year | First author | Journal | Title |
|------|------|------|--------------|---------|-------|
| 13 | [28258028](https://pubmed.ncbi.nlm.nih.gov/28258028/) | 2017 | Wang X | Diabetes research and clinical practice | Resveratrol ameliorates hyperglycemia-induced renal tubular oxidative stress damage via modulating t… |
| 12 | [33110391](https://pubmed.ncbi.nlm.nih.gov/33110391/) | 2020 | Chen H | International journal of biological sciences | SIRT1/FOXO3a axis plays an important role in the prevention of mandibular bone loss induced by 1,25(… |
| 11 | [24040102](https://pubmed.ncbi.nlm.nih.gov/24040102/) | 2013 | Hori YS | PloS one | Regulation of FOXOs and p53 by SIRT1 modulators under oxidative stress. |
| 10 | [41596597](https://pubmed.ncbi.nlm.nih.gov/41596597/) | 2026 | Voros C | International journal of molecular sciences | Oxidative Stress and SIRT1-Nrf2 Anti-Ferroptotic Pathways in Granulosa Cells: A Molecular Key to Fol… |
| 7 | [21813271](https://pubmed.ncbi.nlm.nih.gov/21813271/) | 2012 | Yun JM | The Journal of nutritional biochemistry | Resveratrol up-regulates SIRT1 and inhibits cellular oxidative stress in the diabetic milieu: mechan… |

## CAND-0012: INT-0093 → MEC-0013

**Edge table:** `intervention_mechanism_edges`  
**Relation:** `modulates`  
**Claim:** Alpha-lipoic acid insulin sensitization → modulates AKT-FOXO axis.  
**Query:** `alpha lipoic acid AKT FOXO insulin signaling`

**Chosen PMID:** _NONE — no relevant hit. Review needed._

Top candidates considered:

| Score | PMID | Year | First author | Journal | Title |
|------|------|------|--------------|---------|-------|

## CAND-0013: INT-0047 → MEC-0013

**Edge table:** `intervention_mechanism_edges`  
**Relation:** `modulates`  
**Claim:** Aerobic exercise activates AMPK → AMPK phosphorylates FOXO3 → mitochondrial biogenesis.  
**Query:** `exercise AMPK FOXO3 mitochondrial biogenesis muscle`

**Chosen PMID:** [19262508](https://pubmed.ncbi.nlm.nih.gov/19262508/) — Cantó C (2009) *Nature* — AMPK regulates energy expenditure by modulating NAD+ metabolism and SIRT1 activity.

Top candidates considered:

| Score | PMID | Year | First author | Journal | Title |
|------|------|------|--------------|---------|-------|
| 7 | [19262508](https://pubmed.ncbi.nlm.nih.gov/19262508/) | 2009 | Cantó C | Nature | AMPK regulates energy expenditure by modulating NAD+ metabolism and SIRT1 activity. |

## CAND-0014: INT-0021 → MEC-0028

**Edge table:** `intervention_mechanism_edges`  
**Relation:** `modulates`  
**Claim:** Lithium inhibits GSK-3β → stabilizes β-catenin → upregulates BDNF expression.  
**Query:** `lithium GSK-3 BDNF beta-catenin neurotrophic`

**Chosen PMID:** [31325596](https://pubmed.ncbi.nlm.nih.gov/31325596/) — Li R (2019) *Brain research bulletin* — Lithium chloride promoted hematoma resolution after intracerebral hemorrhage through GSK-3β-mediated pathways-dependent microglia phagocytosis and M2-phenotype differentiation, angiogenesis and neurogenesis in a rat model.
**Second PMID:** [36843130](https://pubmed.ncbi.nlm.nih.gov/36843130/) — Mohamadian M (2023) *Naunyn-Schmiedeberg's archives of pharmacology* — Mood and behavior regulation: interaction of lithium and dopaminergic system.

Top candidates considered:

| Score | PMID | Year | First author | Journal | Title |
|------|------|------|--------------|---------|-------|
| 13 | [31325596](https://pubmed.ncbi.nlm.nih.gov/31325596/) | 2019 | Li R | Brain research bulletin | Lithium chloride promoted hematoma resolution after intracerebral hemorrhage through GSK-3β-mediated… |
| 11 | [36843130](https://pubmed.ncbi.nlm.nih.gov/36843130/) | 2023 | Mohamadian M | Naunyn-Schmiedeberg's archives of pharmacology | Mood and behavior regulation: interaction of lithium and dopaminergic system. |
| 10 | [19423950](https://pubmed.ncbi.nlm.nih.gov/19423950/) | 2009 | Wada A | Journal of pharmacological sciences | Lithium and neuropsychiatric therapeutics: neuroplasticity via glycogen synthase kinase-3beta, beta-… |
| 10 | [19523343](https://pubmed.ncbi.nlm.nih.gov/19523343/) | 2009 | Young W | Cell transplantation | Review of lithium effects on brain and blood. |
| 8 | [35018576](https://pubmed.ncbi.nlm.nih.gov/35018576/) | 2022 | Rana AK | Molecular neurobiology | Lithium therapy subdues neuroinflammation to maintain pyramidal cells arborization and rescues neuro… |

## CAND-0015: INT-0021 → MEC-0009

**Edge table:** `intervention_mechanism_edges`  
**Relation:** `modulates`  
**Claim:** GSK-3β cross-talks with mTOR via TSC2; lithium modulates mTOR pathway activity.  
**Query:** `lithium GSK-3 mTOR TSC2 signaling`

**Chosen PMID:** _NONE — no relevant hit. Review needed._

Top candidates considered:

| Score | PMID | Year | First author | Journal | Title |
|------|------|------|--------------|---------|-------|
| -48 | [15972957](https://pubmed.ncbi.nlm.nih.gov/15972957/) | 2005 | Mak BC | The American journal of pathology | Aberrant beta-catenin signaling in tuberous sclerosis. |

## CAND-0016: INT-0022 → MEC-0015

**Edge table:** `intervention_mechanism_edges`  
**Relation:** `modulates`  
**Claim:** Myo-inositol is the precursor for phosphoinositides (PIP2/PIP3) underlying PI3K/AKT signaling.  
**Query:** `myo-inositol phosphoinositide PI3K AKT signaling review`

**Chosen PMID:** [38151075](https://pubmed.ncbi.nlm.nih.gov/38151075/) — Li G (2024) *Biochemical pharmacology* — Research progress on phosphatidylinositol 4-kinase inhibitors.
**Second PMID:** [20922461](https://pubmed.ncbi.nlm.nih.gov/20922461/) — Castaneda CA (2010) *Cancer metastasis reviews* — The phosphatidyl inositol 3-kinase/AKT signaling pathway in breast cancer.

Top candidates considered:

| Score | PMID | Year | First author | Journal | Title |
|------|------|------|--------------|---------|-------|
| 10 | [38151075](https://pubmed.ncbi.nlm.nih.gov/38151075/) | 2024 | Li G | Biochemical pharmacology | Research progress on phosphatidylinositol 4-kinase inhibitors. |
| 10 | [20922461](https://pubmed.ncbi.nlm.nih.gov/20922461/) | 2010 | Castaneda CA | Cancer metastasis reviews | The phosphatidyl inositol 3-kinase/AKT signaling pathway in breast cancer. |
| -44 | [39485722](https://pubmed.ncbi.nlm.nih.gov/39485722/) | 2024 | Wang R | Cancer medicine | Important Roles of PI3K/AKT Signaling Pathway and Relevant Inhibitors in Prostate Cancer Progression… |
| -44 | [34279200](https://pubmed.ncbi.nlm.nih.gov/34279200/) | 2021 | Narayanankutty A | Current topics in medicinal chemistry | Inhibitory Potential of Dietary Nutraceuticals on Cellular PI3K/Akt Signaling: Implications in Cance… |
| -44 | [16516442](https://pubmed.ncbi.nlm.nih.gov/16516442/) | 2006 | Martelli AM | Cellular signalling | Intranuclear 3'-phosphoinositide metabolism and Akt signaling: new mechanisms for tumorigenesis and … |

## CAND-0017: INT-0024 → MEC-0020

**Edge table:** `intervention_mechanism_edges`  
**Relation:** `modulates`  
**Claim:** Glycine is an obligate NMDA-receptor co-agonist; modulates Ca2+/glutamate-NMDA homeostasis.  
**Query:** `glycine NMDA receptor co-agonist glycine site`

**Chosen PMID:** [30738126](https://pubmed.ncbi.nlm.nih.gov/30738126/) — Peyrovian B (2019) *Progress in neuro-psychopharmacology & biological psychiatry* — The glycine site of NMDA receptors: A target for cognitive enhancement in psychiatric disorders.
**Second PMID:** [36465862](https://pubmed.ncbi.nlm.nih.gov/36465862/) — Zhao F (2022) *Frontiers in chemistry* — Discovery of (R)-2-amino-3-triazolpropanoic acid derivatives as NMDA receptor glycine site agonists with GluN2 subunit-specific activity.

Top candidates considered:

| Score | PMID | Year | First author | Journal | Title |
|------|------|------|--------------|---------|-------|
| 20 | [30738126](https://pubmed.ncbi.nlm.nih.gov/30738126/) | 2019 | Peyrovian B | Progress in neuro-psychopharmacology & biological psychiatry | The glycine site of NMDA receptors: A target for cognitive enhancement in psychiatric disorders. |
| 17 | [36465862](https://pubmed.ncbi.nlm.nih.gov/36465862/) | 2022 | Zhao F | Frontiers in chemistry | Discovery of (R)-2-amino-3-triazolpropanoic acid derivatives as NMDA receptor glycine site agonists … |
| 16 | [24656981](https://pubmed.ncbi.nlm.nih.gov/24656981/) | 2014 | Zellinger C | Epilepsy research | Pre-treatment with the NMDA receptor glycine-binding site antagonist L-701,324 improves pharmacosens… |
| 16 | [25828272](https://pubmed.ncbi.nlm.nih.gov/25828272/) | 2015 | Shimomura H | Neuroscience research | Glycine plays a crucial role as a co-agonist of NMDA receptors in the neuronal circuit generating bo… |
| 15 | [19433577](https://pubmed.ncbi.nlm.nih.gov/19433577/) | 2009 | Zhang HX | The Journal of physiology | The glycine transport inhibitor sarcosine is an NMDA receptor co-agonist that differs from glycine. |

## CAND-0018: INT-0024 → MEC-0001

**Edge table:** `intervention_mechanism_edges`  
**Relation:** `modulates`  
**Claim:** Glycine is one of three amino acid precursors of glutathione (γ-Glu-Cys-Gly).  
**Query:** `glycine glutathione synthesis precursor supplementation`

**Chosen PMID:** [29559876](https://pubmed.ncbi.nlm.nih.gov/29559876/) — McCarty MF (2018) *Ochsner journal* — Dietary Glycine Is Rate-Limiting for Glutathione Synthesis and May Have Broad Potential for Health Protection.
**Second PMID:** [38418414](https://pubmed.ncbi.nlm.nih.gov/38418414/) — Ruparell A (2024) *The British journal of nutrition* — Glycine supplementation can partially restore oxidative stress-associated glutathione deficiency in ageing cats.

Top candidates considered:

| Score | PMID | Year | First author | Journal | Title |
|------|------|------|--------------|---------|-------|
| 18 | [29559876](https://pubmed.ncbi.nlm.nih.gov/29559876/) | 2018 | McCarty MF | Ochsner journal | Dietary Glycine Is Rate-Limiting for Glutathione Synthesis and May Have Broad Potential for Health P… |
| 15 | [38418414](https://pubmed.ncbi.nlm.nih.gov/38418414/) | 2024 | Ruparell A | The British journal of nutrition | Glycine supplementation can partially restore oxidative stress-associated glutathione deficiency in … |
| 15 | [20929994](https://pubmed.ncbi.nlm.nih.gov/20929994/) | 2011 | Sekhar RV | Diabetes care | Glutathione synthesis is diminished in patients with uncontrolled diabetes and restored by dietary s… |
| 15 | [21795440](https://pubmed.ncbi.nlm.nih.gov/21795440/) | 2011 | Sekhar RV | The American journal of clinical nutrition | Deficient synthesis of glutathione underlies oxidative stress in aging and can be corrected by dieta… |
| 14 | [24081740](https://pubmed.ncbi.nlm.nih.gov/24081740/) | 2014 | Nguyen D | The Journal of clinical endocrinology and metabolism | Effect of increasing glutathione with cysteine and glycine supplementation on mitochondrial fuel oxi… |

## CAND-0019: INT-0041 → MEC-0008

**Edge table:** `intervention_mechanism_edges`  
**Relation:** `modulates`  
**Claim:** GFCF diet modulates gut-brain axis; whole-population RCT effect mixed; effect concentrated in subset.  
**Query:** `gluten free casein free diet autism randomized trial`

**Chosen PMID:** [31813108](https://pubmed.ncbi.nlm.nih.gov/31813108/) — González-Domenech PJ (2020) *Journal of autism and developmental disorders* — Influence of a Combined Gluten-Free and Casein-Free Diet on Behavior Disorders in Children and Adolescents Diagnosed with Autism Spectrum Disorder: A 12-Month Follow-Up Clinical Trial.
**Second PMID:** [16555138](https://pubmed.ncbi.nlm.nih.gov/16555138/) — Elder JH (2006) *Journal of autism and developmental disorders* — The gluten-free, casein-free diet in autism: results of a preliminary double blind clinical trial.

Top candidates considered:

| Score | PMID | Year | First author | Journal | Title |
|------|------|------|--------------|---------|-------|
| 23 | [31813108](https://pubmed.ncbi.nlm.nih.gov/31813108/) | 2020 | González-Domenech PJ | Journal of autism and developmental disorders | Influence of a Combined Gluten-Free and Casein-Free Diet on Behavior Disorders in Children and Adole… |
| 22 | [16555138](https://pubmed.ncbi.nlm.nih.gov/16555138/) | 2006 | Elder JH | Journal of autism and developmental disorders | The gluten-free, casein-free diet in autism: results of a preliminary double blind clinical trial. |
| 18 | [28612113](https://pubmed.ncbi.nlm.nih.gov/28612113/) | 2018 | Piwowarczyk A | European journal of nutrition | Gluten- and casein-free diet and autism spectrum disorders in children: a systematic review. |
| 18 | [33026043](https://pubmed.ncbi.nlm.nih.gov/33026043/) | 2020 | Alamri ES | Saudi medical journal | Efficacy of gluten- and casein-free diets on autism spectrum disorders in children. |
| 17 | [24789114](https://pubmed.ncbi.nlm.nih.gov/24789114/) | 2014 | Marí-Bauset S | Journal of child neurology | Evidence of the gluten-free and casein-free diet in autism spectrum disorders: a systematic review. |

## CAND-0020: INT-0041 → MEC-0022

**Edge table:** `intervention_mechanism_edges`  
**Relation:** `modulates`  
**Claim:** GFCF reduces intestinal permeability / LPS translocation in zonulin-elevated subset.  
**Query:** `gluten zonulin intestinal permeability autism`

**Chosen PMID:** [29072974](https://pubmed.ncbi.nlm.nih.gov/29072974/) — Józefczuk J (2018) *Journal of medicinal food* — The Occurrence of Antibodies Against Gluten in Children with Autism Spectrum Disorders Does Not Correlate with Serological Markers of Impaired Intestinal Permeability.

Top candidates considered:

| Score | PMID | Year | First author | Journal | Title |
|------|------|------|--------------|---------|-------|
| 11 | [29072974](https://pubmed.ncbi.nlm.nih.gov/29072974/) | 2018 | Józefczuk J | Journal of medicinal food | The Occurrence of Antibodies Against Gluten in Children with Autism Spectrum Disorders Does Not Corr… |

## CAND-0021: INT-0041 → PHE-0004

**Edge table:** `intervention_phenotype_edges`  
**Relation:** `treats`  
**Claim:** GFCF responder phenotype is the GI/microbiome subgroup specifically.  
**Query:** `GFCF diet autism gastrointestinal symptoms responder`

**Chosen PMID:** [35565765](https://pubmed.ncbi.nlm.nih.gov/35565765/) — González-Domenech PJ (2022) *Nutrients* — A Narrative Review about Autism Spectrum Disorders and Exclusion of Gluten and Casein from the Diet.
**Second PMID:** [23131376](https://pubmed.ncbi.nlm.nih.gov/23131376/) — Harris C (2012) *Complementary therapies in medicine* — A pilot study to evaluate nutritional influences on gastrointestinal symptoms and behavior patterns in children with Autism Spectrum Disorder.

Top candidates considered:

| Score | PMID | Year | First author | Journal | Title |
|------|------|------|--------------|---------|-------|
| 12 | [35565765](https://pubmed.ncbi.nlm.nih.gov/35565765/) | 2022 | González-Domenech PJ | Nutrients | A Narrative Review about Autism Spectrum Disorders and Exclusion of Gluten and Casein from the Diet. |
| 9 | [23131376](https://pubmed.ncbi.nlm.nih.gov/23131376/) | 2012 | Harris C | Complementary therapies in medicine | A pilot study to evaluate nutritional influences on gastrointestinal symptoms and behavior patterns … |
| 9 | [28111520](https://pubmed.ncbi.nlm.nih.gov/28111520/) | 2015 | Elder JH | Nutrition and dietary supplements | A review of gluten- and casein-free diets for treatment of autism: 2005-2015. |
| 8 | [22564339](https://pubmed.ncbi.nlm.nih.gov/22564339/) | 2012 | Pennesi CM | Nutritional neuroscience | Effectiveness of the gluten-free, casein-free diet for children diagnosed with autism spectrum disor… |
| 8 | [23316152](https://pubmed.ncbi.nlm.nih.gov/23316152/) | 2012 | Whiteley P | Frontiers in human neuroscience | Gluten- and casein-free dietary intervention for autism spectrum conditions. |

## CAND-0022: INT-0049 → MEC-0029

**Edge table:** `intervention_mechanism_edges`  
**Relation:** `modulates`  
**Claim:** UVB-driven cutaneous vitamin D synthesis → vitamin D regulates TPH2 / brain serotonin synthesis.  
**Query:** `vitamin D TPH2 serotonin brain autism Patrick`

**Chosen PMID:** [24558199](https://pubmed.ncbi.nlm.nih.gov/24558199/) — Patrick RP (2014) *FASEB journal : official publication of the Federation of American Societies for Experimental Biology* — Vitamin D hormone regulates serotonin synthesis. Part 1: relevance for autism.

Top candidates considered:

| Score | PMID | Year | First author | Journal | Title |
|------|------|------|--------------|---------|-------|
| 17 | [24558199](https://pubmed.ncbi.nlm.nih.gov/24558199/) | 2014 | Patrick RP | FASEB journal : official publication of the Federation of American Societies for Experimental Biology | Vitamin D hormone regulates serotonin synthesis. Part 1: relevance for autism. |

## CAND-0023: INT-0049 → MEC-0016

**Edge table:** `intervention_mechanism_edges`  
**Relation:** `modulates`  
**Claim:** Morning sunlight entrains the suprachiasmatic nucleus and normalizes the cortisol awakening response.  
**Query:** `morning light exposure cortisol awakening circadian suprachiasmatic`

**Chosen PMID:** _NONE — no relevant hit. Review needed._

Top candidates considered:

| Score | PMID | Year | First author | Journal | Title |
|------|------|------|--------------|---------|-------|

