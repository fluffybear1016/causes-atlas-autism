---
id: TOPIC-TESTING-LADDER
type: testing_strategy
audience: parent, clinician
last_updated: 2026-06-23
post_sfari_integration: true
---

# Autism testing — what each test reveals, grouped by what it stratifies

This page maps the available autism-relevant tests to what they reveal
about a specific child's profile against the atlas's 11 phenotype
subtypes. The atlas is a knowledge layer — it surfaces what's measurable
and what each measurement implies. It does not recommend tests; the
ordering decision belongs to the clinician and family.

The atlas's calibration anchor is [[INT-0001]] Leucovorin (CSRS 83.35),
grounded in stratified-RCT evidence in the FOLR1-AA-positive subset
([[HYP-0001]]). This stratification is preserved across all test
selections below.

## Tests stratifying the cerebral folate phenotype (PHE-0001)

Phenotype: ~10–25% of autism cases. Atlas hypothesis: [[HYP-0001]]
FOLR1 autoantibodies block folate transport across the blood-brain
barrier. Clinical pattern: language regression, communication delay,
typically without GI symptoms.

| Test | What it measures | Cost | Turnaround | Notes |
|---|---|---|---|---|
| [[TEST-0014]] FRAA (Religious Sisters of Mercy / Iliad) | Folate receptor alpha blocking antibodies | $200–400 | 3–6 wk | Confirm Ramaekers blocking assay specifically; Cunningham Panel platforms use different methodology |
| [[TEST-0117]] CSF 5-MTHF (Mayo / Baylor) | Cerebrospinal fluid 5-methyltetrahydrofolate | clinician | invasive | Lumbar puncture; reserve for cases where leucovorin response is equivocal |
| [[TEST-0009]] WES / [[TEST-0105]] SFARI gene panel | Variants in FOLR1, MTHFR, DHFR, SHMT1 | varies | 2 wk – 12 mo | Gene-level findings inform mechanism but FRAA biomarker is more sensitive for autoantibody-driven cases |

## Tests stratifying mitochondrial vulnerability (PHE-0002)

Phenotype: regression after illness, fatigue, GI involvement, energy
demands of developmental milestones. Atlas mechanism: [[MEC-0010]]
Mitochondrial dysfunction.

| Test | What it measures | Cost | Turnaround | Notes |
|---|---|---|---|---|
| [[TEST-0015]] Plasma lactate / pyruvate / L:P ratio | Resting cellular energy state | $80–200 (insurance) | 1–2 wk | Standard mito stratification; elevated L:P or lactate is a screening positive |
| [[TEST-0010]] Mosaic Diagnostics OAT | Organic acids panel; 76 markers including mito intermediates, oxidative stress, microbial metabolites | $300 | 2–3 wk | Multi-axis stratification — same sample reveals mito, redox, gut |
| [[TEST-0116]] MitoSwab (Religen Dx) | Buccal mitochondrial enzyme assay; respiratory chain Complex I, II/III, IV | $400–500 | 3–5 wk | Direct enzyme functional assay; non-invasive |
| [[TEST-0129]] Mayo / Baylor mtDNA whole-genome | Full 16,569-bp mtDNA sequencing | clinician | 4–6 wk | When mtDNA heteroplasmy suspected; [[Hannah Poling framework]] context |

## Tests stratifying immune-inflammatory / regressive phenotype (PHE-0003)

Phenotype: post-infectious or vaccine-associated regression,
autoimmune comorbidity, neuroinflammatory clinical pattern.

| Test | What it measures | Cost | Turnaround |
|---|---|---|---|
| [[TEST-0020]] Cunningham Panel | Anti-D1, anti-D2, anti-lysoganglioside, anti-tubulin, CaM kinase II — PANDAS/PANS antibodies | $900 | 4–6 wk |
| CBC w/ diff + immunoglobulins | IgG, IgA, IgM subclasses, T/B cell panel | insurance | 1 wk |
| hs-CRP + ESR | Systemic inflammation | insurance | 1 wk |
| Anti-neural autoantibody panel | NMDAR, GAD65, VGKC encephalitis screen | $500–2000 | 2–4 wk |

## Tests stratifying gut-brain axis phenotype (PHE-0004)

Phenotype: any combination of GI symptoms (constipation, diarrhea,
bloating, food sensitivities), eczema, sleep disruption. Atlas
hypotheses: [[HYP-0007]] microbiome dysbiosis, [[HYP-0056]]
Bifidobacterium depletion, [[HYP-0059]] intestinal barrier permeability.

| Test | What it measures | Cost | Turnaround |
|---|---|---|---|
| GI-MAP (Diagnostic Solutions) | qPCR microbiome composition, pathogens, calprotectin, sIgA, zonulin | $300–500 | 2–3 wk |
| Genova GI Effects | Comprehensive stool panel including pancreatic markers and beneficial bacteria | $500 | 3 wk |
| [[TEST-0010]] OAT (same as above) | Microbial metabolite excess: arabinose (yeast), HPHPA + 4-cresol (clostridia) | $300 | 2–3 wk |

## Tests stratifying methylation pathway (PHE-0010 undermethylator / PHE-0011 metallothionein-deficient)

Walsh-research-derived phenotypes. Methylation cycle: [[MEC-0003]]
Impaired methylation.

| Test | What it measures | Cost | Turnaround |
|---|---|---|---|
| Homocysteine + methylmalonic acid | Methylation cycle bottleneck markers | insurance | 1 wk |
| RBC folate + serum B12 | Cofactor sufficiency | insurance | 1 wk |
| SAM / SAH ratio (Doctor's Data) | Methylation capacity | $150 | 2 wk |
| Whole-blood histamine | Walsh undermethylator marker | $150 | 2 wk |
| RBC Cu / Zn + ceruloplasmin | Walsh metallothionein-deficient signal | insurance | 1 wk |
| [[TEST-0090]] / methylation SNP panel | MTHFR C677T/A1298C, COMT, MTRR, MTR, BHMT, CBS | $80–250 | 1–4 wk |

## Gene-level testing pathways

Multiple paths exist for rare-variant and de novo variant discovery.
The atlas treats these as evidence-class equivalents — no preferred
provider — and surfaces the resulting variant data against the
[[SFARI]] gene database (1,277 graded genes, refreshed quarterly).

| Path | Coverage | Cost | Turnaround | Source |
|---|---|---|---|---|
| [[TEST-0105]] Invitae SFARI gene panel | ~100 highest-confidence SFARI Tier 1 genes; clinical-grade | $250–400 (insurance often covers) | 2–4 wk | clinician-ordered |
| [[TEST-0009]] Whole exome sequencing | ~20,000 protein-coding genes; clinical-grade | varies; insurance possible with diagnosis | 4–6 wk | clinician-ordered |
| [[TEST-0134]] SPARK | Research-cohort whole exome sequencing; clinical-grade interpretation returned by genetic counselor | $0 | 6–12 mo | participant-facing program of [[SFARI]] |
| [[TEST-0006]] IntellxxDNA NeuroGenomic | ~500 SNPs across methylation, neurotransmitter, mito, detox; pre-interpreted for functional medicine | $400–700 | 4–6 wk | direct-to-consumer with clinician interpretation |
| [[TEST-0001]] 23andMe Health + Ancestry | ~640,000 common SNPs; raw data downloadable; methylation/detox/folate variants only | $99–199 | 4–6 wk | direct-to-consumer |
| [[TEST-0005]] AncestryDNA | Common SNPs only; raw data downloadable | $99 | 4–6 wk | direct-to-consumer |

What 23andMe / AncestryDNA do NOT catch: rare and de novo variants.
Most monogenic autism signal lives in those classes. SNP arrays are
sufficient for the functional-medicine methylation panel
(MTHFR, COMT, MAOA, GST family, FUT2, VDR) and the atlas parses raw
data accordingly. They are not sufficient as a primary autism gene
panel.

## Targeted single-gene tests

When a specific syndromic gene is clinically suspected:

| Test | Gene | Atlas hypothesis / phenotype |
|---|---|---|
| [[TEST-0008]] Fragile X PCR + Southern blot | [[FMR1]] CGG repeat | [[PHE-0006]] Fragile X · FMR1 |
| [[TEST-0057]] MECP2 sequencing | [[MECP2]] | Rett spectrum |
| [[TEST-0059]] TSC1/TSC2 sequencing | [[TSC1]], [[TSC2]] | mTOR-syndromic |
| [[TEST-0060]] PTEN sequencing | [[PTEN]] | mTOR-syndromic |
| [[TEST-0123]] SHANK3 sequencing | [[SHANK3]] | Phelan-McDermid |
| [[TEST-0125]] CHD8 sequencing | [[CHD8]] | macrocephaly + ASD subgroup |

## Endocrine / metabolic adjuncts

| Test | What it measures |
|---|---|
| Thyroid full panel (TSH, fT3, fT4, rT3, TPO, Tg-Ab) | Thyroid function, autoimmune thyroid |
| DUTCH urine hormones + cortisol | HPA axis pattern, sex hormone metabolism |
| Comprehensive metabolic panel | Liver, kidney, electrolytes — baseline screening |
| Vitamin D 25-OH, ferritin, B12, RBC folate | Cofactor / micronutrient status |
| Hair mineral analysis | Toxic metal screening (Pb, Hg, Al); reserve for specialist interpretation |

## Cost notes

Costs vary by region and insurance. Several tests are insurance-covered
when ordered clinically: Fragile X PCR, Invitae ASD panel, comprehensive
metabolic panels, standard thyroid panels, lactate / pyruvate, vitamin
D, ferritin, homocysteine, methylmalonic acid, B12, RBC folate, hs-CRP,
ESR. Out-of-pocket only: most functional medicine specialty panels
(IntellxxDNA, OAT, GI-MAP, Genova, FRAA, MitoSwab, Cunningham Panel).

## How results are processed in the atlas

The atlas intake accepts:
- Lab PDFs from Quest, LabCorp, Genova, Mosaic, Invitae, GeneDx, 23andMe
  (PDF text extraction, biomarker + gene-mention parsing)
- Raw DNA files (23andMe v5, AncestryDNA, MyHeritage, VCF)
- Manual blood-work form entries (reference ranges shown inline)

All data is parsed client-side in the browser. Nothing is sent to a
server. Stored data lives in browser local storage only.

The generated report:
1. Matches the profile against the 11 atlas phenotype subtypes by
   biomarker pattern and variant signature
2. Flags out-of-range biomarkers with severity indication
3. Ranks atlas interventions (CSRS-scored, [[SFARI]]-cross-walked) by
   phenotype-match × atlas-gene-relevance × variant odds ratio
4. Surfaces tests that would further stratify the matched phenotype
5. Lists safety contraindications based on detected variants (e.g. F5 →
   estrogen contraindication, MTHFR → folic acid caution)
6. Notes [[Simons Searchlight]] communities for matched Tier 1/2 genes
7. Generates an Obsidian-compatible markdown profile for vault upload

## Related vault pages

- [[INT-0001]] — Leucovorin (calibration anchor)
- [[HYP-0001]] — FOLR1 autoantibodies / cerebral folate deficiency
- [[SFARI]] — gene-evidence backbone integration
- [[SPARK]] — Simons Foundation participant cohort
- [[Simons Searchlight]] — gene-community natural history program
- [[Hannah Poling framework]] — central organizing principle
- [[CLAUDE]] — the 11 epistemic principles
