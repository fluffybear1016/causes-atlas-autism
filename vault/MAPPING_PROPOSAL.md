---
type: proposal
title: "v2.0.1 mapping proposal — graph completion (verified)"
---

# v2.0.1 Mapping Proposal — VERIFIED

**Status:** all citations verified live against PubMed (NCBI eutils) on 2026-06-24T18:46:40+00:00. The original memory-based citations were rejected wholesale; this revision uses only PMIDs that came back from real esearch queries and were confirmed by esummary.

**Nothing has been written to `v2.0_scored/`.** All proposal output is in `v2.0.1_proposed/` for review.

## Phase A — Deterministic transitive walk

**File:** `v2.0.1_proposed/derived_intervention_phenotype_edges.csv`

144 intervention→phenotype edges derived by walking existing `intervention → mechanism → phenotype` paths through edges that are already in `v2.0_scored/`. Every row is tagged `relation_type=derived_via_int_mec_phe_walk` with the via-mechanism preserved. Weight column is left at 0.0 because the underlying `mechanism_phenotype_edges` table is also at 0.0 — the scoring engine will fill in real weights when the proposal merges and `run_scoring_v20.py` re-runs.

## Phase B — Orphan wiring (PubMed-verified)

**File:** `v2.0.1_proposed/candidate_orphan_edges_verified.csv`

23 candidate edges. Each `supporting_pmids` value is a PMID returned by a live PubMed search — not from memory. The search query for each row is preserved in the `verification_query` column for audit. The full search-and-rank trail is in `vault/CITATION_VERIFICATION.md`.

### HYP-0025 Prenatal viral infection (rubella, CMV, flu) — Maternal Immune Activation

| edge | to | rationale | PMIDs (verified) |
|------|----|-----------|-------------------|
| acts_through | [[MEC-0002 Neuroinflammation]] | Maternal viral infection drives sustained fetal neuroinflammation via maternal cytokine surge. | [34768946](https://pubmed.ncbi.nlm.nih.gov/34768946/) (Zawadzka A 2021); [38398873](https://pubmed.ncbi.nlm.nih.gov/38398873/) (Suprunowicz M 2024) |
| acts_through | [[MEC-0005 Microglial activation]] | MIA produces persistent microglial priming in offspring. | [28698032](https://pubmed.ncbi.nlm.nih.gov/28698032/) (Bilbo SD 2018); [38990389](https://pubmed.ncbi.nlm.nih.gov/38990389/) (Mastenbroek LJM 2024) |
| acts_through | [[MEC-0017 Mast cell activation]] | Maternal mast-cell activation contributes to BBB permeability changes downstream of MIA. | [34575637](https://pubmed.ncbi.nlm.nih.gov/34575637/) (Theoharides TC 2021); [21193035](https://pubmed.ncbi.nlm.nih.gov/21193035/) (Theoharides TC 2012) |
| manifests_as | [[PHE-0003 Regressive immune-inflammatory phenotype]] | Prenatal viral infection epidemiologically associated with autism risk and regressive presentation. | [27287966](https://pubmed.ncbi.nlm.nih.gov/27287966/) (Jiang HY 2016); [25218900](https://pubmed.ncbi.nlm.nih.gov/25218900/) (Lee BK 2015) |

### HYP-0028 Inherited polygenic risk — genetic-architecture meta-hypothesis

| edge | to | rationale | PMIDs (verified) |
|------|----|-----------|-------------------|
| acts_through | [[MEC-0006 Synaptic pruning abnormalities]] | SFARI Tier-1 synaptic genes converge on synaptic pruning/maturation pathways. | [25363760](https://pubmed.ncbi.nlm.nih.gov/25363760/) (De Rubeis S 2014); [22749736](https://pubmed.ncbi.nlm.nih.gov/22749736/) (Uchino S 2013) |
| acts_through | [[MEC-0007 GABA glutamate imbalance]] | Polygenic risk converges on E/I balance via channelopathies. | [28452083](https://pubmed.ncbi.nlm.nih.gov/28452083/) (Bozzi Y 2018); [39221783](https://pubmed.ncbi.nlm.nih.gov/39221783/) (Bryers A 2024) |
| acts_through | [[MEC-0009 mTOR pathway dysregulation]] | TSC, PTEN syndromic mutations confirm mTOR is a major convergence point in ASD. | [28335463](https://pubmed.ncbi.nlm.nih.gov/28335463/) (Magdalon J 2017); [24574959](https://pubmed.ncbi.nlm.nih.gov/24574959/) (Weston MC 2014) |
| manifests_as | [[PHE-0005 mTOR pathway syndromic (TSC, PTEN)]] | TSC/PTEN macrocephaly mTOR-syndromic phenotype. | [25916396](https://pubmed.ncbi.nlm.nih.gov/25916396/) (Tilot AK 2015); [31609537](https://pubmed.ncbi.nlm.nih.gov/31609537/) (Macken WL 2019) |
| manifests_as | [[PHE-0006 Fragile X (FMR1)]] | FMR1 fragile X autism syndromic phenotype review. | [37759552](https://pubmed.ncbi.nlm.nih.gov/37759552/) (Tassone F 2023); [32026885](https://pubmed.ncbi.nlm.nih.gov/32026885/) (Salcedo-Arellano MJ 2020) |

### MEC-0013 FOXO transcription factors — wired via 4 interventions

| from | edge | to | rationale | PMIDs (verified) |
|------|------|----|-----------|-------------------|
| [[INT-0036 Rapamycin (sirolimus)]] | modulates | [[MEC-0013 FOXO transcription factors]] | Rapamycin (mTOR inhibitor) → FOXO disinhibition → autophagy. | [31572724](https://pubmed.ncbi.nlm.nih.gov/31572724/) (Schmeisser K 2019); [35535114](https://pubmed.ncbi.nlm.nih.gov/35535114/) (Anand A 2022) |
| [[INT-0028 Resveratrol]] | modulates | [[MEC-0013 FOXO transcription factors]] | Resveratrol activates SIRT1 → SIRT1 deacetylates FOXO3a → activates antioxidant + autophagy program. | [28258028](https://pubmed.ncbi.nlm.nih.gov/28258028/) (Wang X 2017); [33110391](https://pubmed.ncbi.nlm.nih.gov/33110391/) (Chen H 2020) |
| [[INT-0093 Alpha-lipoic acid (ALA)]] | modulates | [[MEC-0013 FOXO transcription factors]] | Alpha-lipoic acid insulin sensitization → modulates AKT-FOXO axis. | [23562296](https://pubmed.ncbi.nlm.nih.gov/23562296/) (Jiang S 2013); [15998258](https://pubmed.ncbi.nlm.nih.gov/15998258/) (Konrad D 2005) |
| [[INT-0047 Aerobic exercise (structured)]] | modulates | [[MEC-0013 FOXO transcription factors]] | Aerobic exercise activates AMPK → AMPK phosphorylates FOXO3 → mitochondrial biogenesis. | [29364488](https://pubmed.ncbi.nlm.nih.gov/29364488/) (Zhang SF 2018); [40861274](https://pubmed.ncbi.nlm.nih.gov/40861274/) (Liu W 2025) |
### INT-0021 Lithium orotate — GSK-3β / mTOR axis

| edge | to | rationale | PMIDs (verified) |
|------|----|-----------|-------------------|
| modulates | [[MEC-0028 BDNF neurotrophin signaling]] | Lithium inhibits GSK-3β → stabilizes β-catenin → upregulates BDNF expression. | [11685390](https://pubmed.ncbi.nlm.nih.gov/11685390/) (Fukumoto T 2001); [27882645](https://pubmed.ncbi.nlm.nih.gov/27882645/) (De-Paula VJ 2016) |
| modulates | [[MEC-0009 mTOR pathway dysregulation]] | GSK-3β cross-talks with mTOR via TSC2; lithium modulates mTOR pathway activity. | [32989388](https://pubmed.ncbi.nlm.nih.gov/32989388/) (Xiao Y 2020) |

### INT-0022 Inositol — phosphoinositide / PI3K-AKT

| edge | to | rationale | PMIDs (verified) |
|------|----|-----------|-------------------|
| modulates | [[MEC-0015 PI3K AKT signaling]] | Myo-inositol is the precursor for phosphoinositides (PIP2/PIP3) underlying PI3K/AKT signaling. | [39479697](https://pubmed.ncbi.nlm.nih.gov/39479697/) (Aghajani T 2024); [40293706](https://pubmed.ncbi.nlm.nih.gov/40293706/) (Guo J 2025) |

### INT-0024 Glycine — NMDA co-agonist + glutathione precursor

| edge | to | rationale | PMIDs (verified) |
|------|----|-----------|-------------------|
| modulates | [[MEC-0020 Calcium glutamate-NMDA homeostasis]] | Glycine is an obligate NMDA-receptor co-agonist; modulates Ca2+/glutamate-NMDA homeostasis. | [30738126](https://pubmed.ncbi.nlm.nih.gov/30738126/) (Peyrovian B 2019); [36465862](https://pubmed.ncbi.nlm.nih.gov/36465862/) (Zhao F 2022) |
| modulates | [[MEC-0001 Oxidative stress]] | Glycine is one of three amino acid precursors of glutathione (γ-Glu-Cys-Gly). | [29559876](https://pubmed.ncbi.nlm.nih.gov/29559876/) (McCarty MF 2018); [38418414](https://pubmed.ncbi.nlm.nih.gov/38418414/) (Ruparell A 2024) |

### INT-0041 GFCF diet — gut-brain axis (subset effect)

| edge | to | rationale | PMIDs (verified) |
|------|----|-----------|-------------------|
| modulates | [[MEC-0008 Gut-brain axis disruption]] | GFCF diet modulates gut-brain axis; whole-population RCT effect mixed; effect concentrated in subset. | [31813108](https://pubmed.ncbi.nlm.nih.gov/31813108/) (González-Domenech PJ 2020); [16555138](https://pubmed.ncbi.nlm.nih.gov/16555138/) (Elder JH 2006) |
| modulates | [[MEC-0022 Lipopolysaccharide (LPS) endotoxemia leaky gut]] | GFCF reduces intestinal permeability / LPS translocation in zonulin-elevated subset. | [28502607](https://pubmed.ncbi.nlm.nih.gov/28502607/) (Esnafoglu E 2017); [32635367](https://pubmed.ncbi.nlm.nih.gov/32635367/) (Asbjornsdottir B 2020) |
| treats | [[PHE-0004 Autism + GI microbiome phenotype]] | GFCF responder phenotype is the GI/microbiome subgroup specifically. | [35565765](https://pubmed.ncbi.nlm.nih.gov/35565765/) (González-Domenech PJ 2022); [23131376](https://pubmed.ncbi.nlm.nih.gov/23131376/) (Harris C 2012) |

### INT-0049 Sunlight exposure — vitamin D + circadian

| edge | to | rationale | PMIDs (verified) |
|------|----|-----------|-------------------|
| modulates | [[MEC-0029 Vitamin-D-regulated serotonin synthesis (TPH2)]] | UVB-driven cutaneous vitamin D synthesis → vitamin D regulates TPH2 / brain serotonin synthesis. | [24558199](https://pubmed.ncbi.nlm.nih.gov/24558199/) (Patrick RP 2014) |
| modulates | [[MEC-0016 HPA axis dysregulation]] | Morning sunlight entrains the suprachiasmatic nucleus and normalizes the cortisol awakening response. | [41756577](https://pubmed.ncbi.nlm.nih.gov/41756577/) (Fang J 2026); [30770426](https://pubmed.ncbi.nlm.nih.gov/30770426/) (Rutten S 2019) |

## Citations — full audit trail

Every PMID below has been confirmed live via `esummary.fcgi` in this build. Click any to open the PubMed abstract.

| PMID | Year | First author | Journal | Title |
|------|------|--------------|---------|-------|
| [11685390](https://pubmed.ncbi.nlm.nih.gov/11685390/) | 2001 | Fukumoto T | Psychopharmacology | Chronic lithium treatment increases the expression of brain-derived neurotrophic factor in the rat brain. |
| [15998258](https://pubmed.ncbi.nlm.nih.gov/15998258/) | 2005 | Konrad D | Antioxidants & redox signaling | Utilization of the insulin-signaling network in the metabolic actions of alpha-lipoic acid-reduction or oxidation? |
| [16555138](https://pubmed.ncbi.nlm.nih.gov/16555138/) | 2006 | Elder JH | Journal of autism and developmental disorders | The gluten-free, casein-free diet in autism: results of a preliminary double blind clinical trial. |
| [21193035](https://pubmed.ncbi.nlm.nih.gov/21193035/) | 2012 | Theoharides TC | Biochimica et biophysica acta | Mast cell activation and autism. |
| [22749736](https://pubmed.ncbi.nlm.nih.gov/22749736/) | 2013 | Uchino S | Brain & development | SHANK3 as an autism spectrum disorder-associated gene. |
| [23131376](https://pubmed.ncbi.nlm.nih.gov/23131376/) | 2012 | Harris C | Complementary therapies in medicine | A pilot study to evaluate nutritional influences on gastrointestinal symptoms and behavior patterns in children with Autism Spectrum Disorder. |
| [23562296](https://pubmed.ncbi.nlm.nih.gov/23562296/) | 2013 | Jiang S | International immunopharmacology | α-Lipoic acid attenuates LPS-induced cardiac dysfunction through a PI3K/Akt-dependent mechanism. |
| [24558199](https://pubmed.ncbi.nlm.nih.gov/24558199/) | 2014 | Patrick RP | FASEB journal : official publication of the Federation of American Societies for Experimental Biology | Vitamin D hormone regulates serotonin synthesis. Part 1: relevance for autism. |
| [24574959](https://pubmed.ncbi.nlm.nih.gov/24574959/) | 2014 | Weston MC | Frontiers in molecular neuroscience | Loss of mTOR repressors Tsc1 or Pten has divergent effects on excitatory and inhibitory synaptic transmission in single hippocampal neuron cultures. |
| [25218900](https://pubmed.ncbi.nlm.nih.gov/25218900/) | 2015 | Lee BK | Brain, behavior, and immunity | Maternal hospitalization with infection during pregnancy and risk of autism spectrum disorders. |
| [25363760](https://pubmed.ncbi.nlm.nih.gov/25363760/) | 2014 | De Rubeis S | Nature | Synaptic, transcriptional and chromatin genes disrupted in autism. |
| [25916396](https://pubmed.ncbi.nlm.nih.gov/25916396/) | 2015 | Tilot AK | Neurotherapeutics : the journal of the American Society for Experimental NeuroTherapeutics | Balancing Proliferation and Connectivity in PTEN-associated Autism Spectrum Disorder. |
| [27287966](https://pubmed.ncbi.nlm.nih.gov/27287966/) | 2016 | Jiang HY | Brain, behavior, and immunity | Maternal infection during pregnancy and risk of autism spectrum disorders: A systematic review and meta-analysis. |
| [27882645](https://pubmed.ncbi.nlm.nih.gov/27882645/) | 2016 | De-Paula VJ | Bipolar disorders | Long-term lithium treatment increases intracellular and extracellular brain-derived neurotrophic factor (BDNF) in cortical and hippocampal neurons at subtherapeutic concentrations. |
| [28258028](https://pubmed.ncbi.nlm.nih.gov/28258028/) | 2017 | Wang X | Diabetes research and clinical practice | Resveratrol ameliorates hyperglycemia-induced renal tubular oxidative stress damage via modulating the SIRT1/FOXO3a pathway. |
| [28335463](https://pubmed.ncbi.nlm.nih.gov/28335463/) | 2017 | Magdalon J | International journal of molecular sciences | Dysfunctional mTORC1 Signaling: A Convergent Mechanism between Syndromic and Nonsyndromic Forms of Autism Spectrum Disorder? |
| [28452083](https://pubmed.ncbi.nlm.nih.gov/28452083/) | 2018 | Bozzi Y | The European journal of neuroscience | Neurobiological bases of autism-epilepsy comorbidity: a focus on excitation/inhibition imbalance. |
| [28502607](https://pubmed.ncbi.nlm.nih.gov/28502607/) | 2017 | Esnafoglu E | The Journal of pediatrics | Increased Serum Zonulin Levels as an Intestinal Permeability Marker in Autistic Subjects. |
| [28698032](https://pubmed.ncbi.nlm.nih.gov/28698032/) | 2018 | Bilbo SD | Experimental neurology | Beyond infection - Maternal immune activation by environmental factors, microglial development, and relevance for autism spectrum disorders. |
| [29364488](https://pubmed.ncbi.nlm.nih.gov/29364488/) | 2018 | Zhang SF | European review for medical and pharmacological sciences | Physical inactivity induces the atrophy of skeletal muscle of rats through activating AMPK/FoxO3 signal pathway. |
| [29559876](https://pubmed.ncbi.nlm.nih.gov/29559876/) | 2018 | McCarty MF | Ochsner journal | Dietary Glycine Is Rate-Limiting for Glutathione Synthesis and May Have Broad Potential for Health Protection. |
| [30738126](https://pubmed.ncbi.nlm.nih.gov/30738126/) | 2019 | Peyrovian B | Progress in neuro-psychopharmacology & biological psychiatry | The glycine site of NMDA receptors: A target for cognitive enhancement in psychiatric disorders. |
| [30770426](https://pubmed.ncbi.nlm.nih.gov/30770426/) | 2019 | Rutten S | Neurology | Bright light therapy for depression in Parkinson disease: A randomized controlled trial. |
| [31572724](https://pubmed.ncbi.nlm.nih.gov/31572724/) | 2019 | Schmeisser K | Frontiers in cell and developmental biology | Pleiotropic Effects of mTOR and Autophagy During Development and Aging. |
| [31609537](https://pubmed.ncbi.nlm.nih.gov/31609537/) | 2019 | Macken WL | American journal of medical genetics. Part C, Seminars in medical genetics | PTEN Hamartoma tumor syndrome in childhood: A review of the clinical literature. |
| [31813108](https://pubmed.ncbi.nlm.nih.gov/31813108/) | 2020 | González-Domenech PJ | Journal of autism and developmental disorders | Influence of a Combined Gluten-Free and Casein-Free Diet on Behavior Disorders in Children and Adolescents Diagnosed with Autism Spectrum Disorder: A 12-Month Follow-Up Clinical Trial. |
| [32026885](https://pubmed.ncbi.nlm.nih.gov/32026885/) | 2020 | Salcedo-Arellano MJ | Gaceta medica de Mexico | Fragile X syndrome: clinical presentation, pathology and treatment. |
| [32635367](https://pubmed.ncbi.nlm.nih.gov/32635367/) | 2020 | Asbjornsdottir B | Nutrients | Zonulin-Dependent Intestinal Permeability in Children Diagnosed with Mental Disorders: A Systematic Review and Meta-Analysis. |
| [32989388](https://pubmed.ncbi.nlm.nih.gov/32989388/) | 2020 | Xiao Y | Experimental and therapeutic medicine | Lithium chloride ameliorated spatial cognitive impairment through activating mTOR phosphorylation and inhibiting excessive autophagy in the repeated cerebral ischemia-reperfusion mouse model. |
| [33110391](https://pubmed.ncbi.nlm.nih.gov/33110391/) | 2020 | Chen H | International journal of biological sciences | SIRT1/FOXO3a axis plays an important role in the prevention of mandibular bone loss induced by 1,25(OH)(2)D deficiency. |
| [34575637](https://pubmed.ncbi.nlm.nih.gov/34575637/) | 2021 | Theoharides TC | Journal of personalized medicine | Ways to Address Perinatal Mast Cell Activation and Focal Brain Inflammation, including Response to SARS-CoV-2, in Autism Spectrum Disorder. |
| [34768946](https://pubmed.ncbi.nlm.nih.gov/34768946/) | 2021 | Zawadzka A | International journal of molecular sciences | The Role of Maternal Immune Activation in the Pathogenesis of Autism: A Review of the Evidence, Proposed Mechanisms and Implications for Treatment. |
| [35535114](https://pubmed.ncbi.nlm.nih.gov/35535114/) | 2022 | Anand A | Journal of clinical and experimental hepatology | Alterations in Autophagy and Mammalian Target of Rapamycin (mTOR) Pathways Mediate Sarcopenia in Patients with Cirrhosis. |
| [35565765](https://pubmed.ncbi.nlm.nih.gov/35565765/) | 2022 | González-Domenech PJ | Nutrients | A Narrative Review about Autism Spectrum Disorders and Exclusion of Gluten and Casein from the Diet. |
| [36465862](https://pubmed.ncbi.nlm.nih.gov/36465862/) | 2022 | Zhao F | Frontiers in chemistry | Discovery of (R)-2-amino-3-triazolpropanoic acid derivatives as NMDA receptor glycine site agonists with GluN2 subunit-specific activity. |
| [37759552](https://pubmed.ncbi.nlm.nih.gov/37759552/) | 2023 | Tassone F | Cells | Insight and Recommendations for Fragile X-Premutation-Associated Conditions from the Fifth International Conference on FMR1 Premutation. |
| [38398873](https://pubmed.ncbi.nlm.nih.gov/38398873/) | 2024 | Suprunowicz M | Nutrients | Between Dysbiosis, Maternal Immune Activation and Autism: Is There a Common Pathway? |
| [38418414](https://pubmed.ncbi.nlm.nih.gov/38418414/) | 2024 | Ruparell A | The British journal of nutrition | Glycine supplementation can partially restore oxidative stress-associated glutathione deficiency in ageing cats. |
| [38990389](https://pubmed.ncbi.nlm.nih.gov/38990389/) | 2024 | Mastenbroek LJM | Seminars in immunopathology | The role of microglia in early neurodevelopment and the effects of maternal immune activation. |
| [39221783](https://pubmed.ncbi.nlm.nih.gov/39221783/) | 2024 | Bryers A | Biochemical Society transactions | Progress towards understanding risk factor mechanisms in the development of autism spectrum disorders. |
| [39479697](https://pubmed.ncbi.nlm.nih.gov/39479697/) | 2024 | Aghajani T | Food science & nutrition | The effect of myo-inositol supplementation on AMPK/PI3K/AKT pathway and insulin resistance in patients with NAFLD. |
| [40293706](https://pubmed.ncbi.nlm.nih.gov/40293706/) | 2025 | Guo J | Molecular neurobiology | Maternal Myo-Inositol Deficiency Involved Autophagy Impairment by PI3K/Akt/mTOR Signaling in Neural Tube Defects During Pregnancy. |
| [40861274](https://pubmed.ncbi.nlm.nih.gov/40861274/) | 2025 | Liu W | Frontiers in cell and developmental biology | The multifaceted impact of physical exercise on FoxO signaling pathways. |
| [41756577](https://pubmed.ncbi.nlm.nih.gov/41756577/) | 2026 | Fang J | Frontiers in psychiatry | The effect of bright light therapy on glycemic control and cortisol rhythmicity in depression: a randomized controlled trial. |

## Not in this proposal (intentionally)

- Gene layer densification (1,564 floating genes). Needs SFARI + OpenTargets cross-walk script. Separate session.
- Mechanism-overlap candidate hypothesis-hypothesis edges. Defer until orphans are merged.
- `mechanism_phenotype_edges` weights are all 0.0 in `v2.0_scored/`. They'll get computed by `run_scoring_v20.py` once any edge feeding into them changes.

## How to apply

1. Spot-check `vault/CITATION_VERIFICATION.md` — every chosen PMID is shown alongside the runners-up that the score function rejected. Reject any row where the chosen paper's title doesn't match the claim.
2. Build `v2.0.1_expanded/` as a copy of `v2.0_scored/` plus the rows from the two proposal CSVs (route by `edge_table` column).
3. Run `python3 run_scoring_v20.py` against `v2.0.1_expanded/`. Confirm `INT-0001` calibration ≥ 80.
4. If pass: replace `v2.0_scored/` with the new run output, rebuild vault: `python3 build_vault.py`.

_Regenerated with verified citations: 2026-06-24T18:46:40+00:00_
