---
id: TOPIC-Genomics-Autism
type: topic_deep_dive
purpose: Elite-level synthesis of autism genetics — what 1564 atlas genes mean, how to use them clinically
key_atlas_links:
  - HYP-0028 (Inherited polygenic risk)
  - vault/genes/INDEX.md
related_topic_pages:
  - Epigenetics_of_Autism
status: live
---

# Genomics of Autism — Elite-Level Overview

This is a structured synthesis of where autism genetics actually stands as a field in 2026: what the 1,564 SFARI-database genes in the atlas mean, how rare-variant and polygenic risk architectures combine, what gene families matter clinically, what genetic testing actually tells you (and what it doesn't), and where pharmacogenomics fits. Written for a parent, family member, or clinician trying to understand what the genetics-forward part of autism research has actually established.

For the formal atlas record, see [[HYP-0028 Inherited polygenic risk]] and the gene-layer rendering at `vault/genes/INDEX.md`.

For the related but mechanistically distinct epigenetic layer (which is *modifiable* in ways genetics is not), see [[Epigenetics_of_Autism]].

## The two-architecture model

Autism genetics is best understood as **two simultaneously-operating architectures**, not one. Both contribute to overall risk; their relative weight differs across individuals.

### Architecture 1 — Rare large-effect variants

On thorough clinical genetic workup (CMA + Fragile X + autism gene panel + WES where indicated), roughly **20–30% of autism cases yield an identifiable rare large-effect genetic variant** that's plausibly causal in that individual. (The proportion depends heavily on what tests are run; CMA alone yields ~7-10%, adding WES can push the number higher.) These are typically:

- **De novo mutations** — variants that arose spontaneously in egg or sperm and weren't inherited from either parent.
- **Inherited mutations from carrier parents** with milder phenotype than the child.
- **Copy-number variants (CNVs)** — chromosomal deletions or duplications affecting many genes at once.

When a single rare variant is sufficient to push a child into autism phenotype, that gene becomes a **diagnosed cause** rather than a contributor. Examples: *FMR1* (Fragile X), *MECP2* (Rett syndrome — though now recognized as related but distinct), *TSC1/TSC2* (tuberous sclerosis), *PTEN* (PTEN hamartoma syndrome), *SHANK3* (Phelan-McDermid syndrome), *CHD8*, *SCN2A*, *SYNGAP1*, *ADNP*, and several dozen others.

Each of these is in the atlas's gene layer. Each has a defined inheritance pattern, biological mechanism, and (sometimes) targeted intervention possibility.

### Architecture 2 — Common-variant polygenic risk

The remaining ~70-80% of autism cases on clinical workup don't have a single identifiable rare variant — but autism is still highly heritable: **twin-study heritability estimates range 64-91%** (Tick et al. 2016 meta-analysis). This residual genetic risk is largely **polygenic** — distributed across thousands of common DNA variants, each contributing a small effect, summing into the total inherited burden. This is what [[HYP-0028 Inherited polygenic risk]] captures.

Quantitatively: SNP-based heritability estimates (capturing common variants alone) range ~17-50% depending on methodology and cohort. Common variants likely explain the largest single chunk of population-level autism risk; rare variants explain less of the population-level risk *but contribute outsized clinical impact when present in an individual*. (Gaugler et al. 2014, *Nature Genetics*: "most genetic risk for autism resides with common variation.")

Polygenic Risk Scores (PRS) for autism, derived from large-cohort GWAS studies (largely [[Chung_Wendy]]'s SPARK and [[Geschwind_Daniel]]-class work), can quantify the common-variant component. PRS is not yet clinically deployed but is a research tool that's getting closer. The atlas treats polygenic risk as the substrate on which environmental triggers act per the [[Hannah Poling framework]] — `causation = susceptibility (P) × trigger (E)`.

### Why both architectures matter

A child with a known rare variant (Fragile X, for example) is at extremely high risk for autism *regardless* of polygenic background. The variant is sufficient.

A child without a known rare variant but with high polygenic risk has elevated baseline susceptibility that interacts with environmental load — the [[Naviaux_Robert]] 3-Hit framework's Hit-1 substrate. They are vulnerable; whether they cross the threshold to clinical autism depends on Hit-2 (early trigger) and Hit-3 (persistent CDR during the window).

Most clinical genetic workups are calibrated to find Architecture 1 variants. Architecture 2 (polygenic) is increasingly accessible through commercial direct-to-consumer testing but is not standard clinical care yet.

## SFARI Gene database and the tier system

The atlas's 1,564 genes are pulled primarily from the SFARI Gene database (sfari.org/resource/sfari-gene/), maintained by the Simons Foundation Autism Research Initiative. Each gene gets a tier rating based on the strength of evidence linking it to autism.

| Tier | Label | Atlas notes |
|---|---|---|
| 1 | High Confidence | Wired to [[HYP-0028]] |
| 2 | Strong Candidate | Wired to [[HYP-0028]] |
| 3 | Suggestive Evidence | Atlas has but not all wired |
| S | Syndromic | Genes in defined autism-associated syndromes |

(Atlas state: 781 SFARI Tier 1+2 genes wired to HYP-0028 out of 1,564 total genes loaded. SFARI's own database has been recategorized periodically; consult [SFARI Gene statistics](https://gene.sfari.org/about-sfari-gene/statistics/) for current per-tier counts.)

A clinical genetic test result that lands in **Tier 1 or Tier S** is essentially diagnostic. A **Tier 2** finding is strongly suspicious. **Tier 3** findings should be interpreted carefully — the evidence is real but not definitive, and the child may have multiple Tier 3 variants whose combined effect is meaningful.

## Key gene families clinically

There are five gene families / pathways every parent should know about because they have either targeted intervention implications or substantial functional-medicine relevance.

### 1. SHANK family + synaptic structure (SHANK1/2/3, NLGN3/4, NRXN1, etc.)

These genes encode the molecular scaffolding of excitatory synapses. Loss-of-function variants disrupt synaptic protein density and dendritic spine morphology — directly connecting to [[Casanova_Manuel]]'s minicolumn pathology and [[MEC-0020 Calcium glutamate-NMDA homeostasis]].

**Clinical implications:** SHANK3 deletions cause Phelan-McDermid syndrome, which has been the target of [[Hollander_Eric]]'s IGF-1 trials — IGF-1 rescues synaptic protein synthesis in animal models. This is the cleanest example of genotype-stratified targeted intervention in autism trials.

### 2. mTOR pathway (TSC1, TSC2, PTEN, NF1, MTOR itself)

The mTOR pathway is a master regulator of cell growth, protein synthesis, and metabolism. Variants in mTOR-pathway genes cause syndromes (tuberous sclerosis, PTEN hamartoma, NF1) that have substantially elevated autism rates. Mechanistically: dysregulated mTOR signaling → over-proliferation of dendritic spines + impaired synaptic pruning + altered metabolic state.

**Clinical implications:** [[INT-0036 Rapamycin (sirolimus)]] is an mTOR inhibitor and is the most direct genotype-targeted intervention currently available. For children with TSC, PTEN, or strong mTOR-pathway findings, low-dose rapamycin under specialist supervision is an evidence-supported option. Multiple Phase 2 trials underway.

### 3. FMR1 / Fragile X spectrum

The single most common single-gene cause of inherited autism. FMR1 trinucleotide repeat expansion silences FMRP protein, which normally restrains synaptic translation. Without FMRP: excess protein synthesis at synapses, dysregulated mGluR5 signaling, characteristic phenotype.

**Clinical implications:** Diagnostic certainty matters — Fragile X kids have specific medical surveillance needs (joint hyperlaxity, mitral valve issues, premature ovarian failure in female carriers). Therapeutic targets including mGluR5 modulators have been investigated; early-stage adjunctive therapies. Family-counseling implications are substantial — Fragile X is X-linked with carrier mothers passing it to ~50% of male offspring.

### 4. Methylation-cycle / one-carbon metabolism (MTHFR, MTRR, MTR, COMT, CBS, BHMT, AHCY, MAT)

These genes encode the enzymes of the folate ↔ methionine ↔ transsulfuration cycles that [[James_Jill]]'s biochemistry work + [[Frye_Richard]]'s clinical translation + [[Walsh_William]]'s biotyping framework + [[Yasko_Amy]]'s SNP-targeted protocols all operate on. Common variants here (particularly MTHFR C677T and COMT V158M) significantly affect:

- How efficiently the child can methylate (DNA, neurotransmitters, lipids, proteins)
- How well they detoxify environmental chemicals
- How they respond to folate supplementation (folic acid vs methylated folate)
- How they handle homocysteine and oxidative stress

**Clinical implications:** SNP profile directly informs nutrient choice. MTHFR-positive kids should generally get methylated folate (5-MTHF) or folinic acid (leucovorin) rather than synthetic folic acid. Overmethylators (per [[Walsh_William]]'s biotype framework) need different strategy than undermethylators. This is the most clinically-actionable gene family in autism workup right now.

### 5. Mitochondrial-function genes (POLG, MT-* mitochondrial DNA variants, complex I/II/III/IV/V subunits, SLC25A19, etc.)

The genetic substrate for [[HYP-0006 Mitochondrial dysfunction (acquired or inherited)]] and the [[Naviaux_Robert]] 3-Hit Hit-1 pathway. Maternal mitochondrial DNA variants are particularly important because mitochondria are inherited maternally — meaning maternal mitochondrial-genetic vulnerability affects the child's CDR threshold from conception.

**Clinical implications:** A child with documented mitochondrial-gene findings warrants the [[Rossignol_Daniel]] mitochondrial cofactor protocol, careful avoidance of mitotoxic exposures (certain antibiotics, certain anesthetics, valproate, statins-in-genetically-vulnerable families), and consideration of stem cell therapy ([[Stem_Cell_Therapy_for_Autism]]) for the mitochondrial-transfer pathway. Mom's mitochondrial workup is informative for sibling planning.

## Clinical genetic testing in 2026 — what to actually order

The standard pediatric genetics consultation for autism in 2026 includes:

**First-line (insurance typically covers):**

1. **Chromosomal microarray (CMA / aCGH)** — detects copy-number variants. Yield 7–10% in clinically-evaluated autism. First-line per AAP/ACMG guidelines.
2. **Fragile X testing (FMR1 trinucleotide repeat)** — detects Fragile X syndrome. Yield 1–3% in autism. Always order regardless of family history.
3. **Karyotype** — detects gross chromosomal abnormalities (Down syndrome, sex chromosome variants). Limited but standard.

**Second-line (sometimes covered, often parent-paid):**

4. **Autism gene panel (NGS panel)** — sequences the high-confidence Tier 1 + S genes plus emerging Tier 2 candidates. Yield 5–15% additional beyond CMA + Fragile X. Multiple commercial labs offer (GeneDx, Invitae, Blueprint Genetics, Athena, others).
5. **Whole-exome sequencing (WES)** — sequences all protein-coding exons. Highest yield. Increasingly first-line for unexplained cases. Yield ~20% in well-selected autism cases.
6. **Whole-genome sequencing (WGS)** — sequences coding + non-coding regions including regulatory elements. Highest cost. Becoming the new standard for gene discovery; not yet routine clinical care.

**Methylation-cycle SNPs (parent-paid):**

7. **23andMe / SelfDecode / Nutrigenomic Test Panel (Yasko)** — direct-to-consumer SNP testing covering MTHFR, COMT, CBS, MAO, BHMT, AHCY, and other methylation-relevant SNPs. ~$200–300. Worth it for clinical-protocol calibration.

**Pharmacogenomic panel (clinical):**

8. **Pharmacogenomic SNP panel** — CYP2D6, CYP2C19, CYP3A4, MTHFR, others. Affects dose response to common medications (SSRIs, antipsychotics, ADHD meds). Increasingly clinically standard. Yield: high — about 90% of psychiatric medications have known PGx implications.

The right starter test order for a child newly diagnosed with autism is typically: CMA + Fragile X + FMR1 (insurance), plus a methylation-cycle SNP panel via 23andMe (parent-paid). Whole-exome should be ordered if first-line tests are negative.

## What genetic testing tells you (and what it doesn't)

**What it CAN tell you:**

- Whether the child has a rare large-effect variant (and if so, what syndrome and what to monitor for).
- Family-counseling and recurrence-risk information for sibling planning.
- Pharmacogenomic guidance for medications (SSRIs, antipsychotics, stimulants, anesthesia).
- Methylation-cycle SNP profile that directly informs nutrient supplementation choices.
- Mitochondrial-vulnerability indicators that inform protocol design and exposure-avoidance recommendations.

**What it CANNOT tell you:**

- Whether the child will respond to behavioral therapy.
- Whether the child will respond to leucovorin, FMT, or any specific intervention (FRAA testing, microbiome sequencing, biomarker panels do this — see [[Frye_Richard]], [[Hazan_Sabine]], [[Shaw_William]]).
- Whether environmental triggers contributed (you have to actually look for those — toxin panels, biomarker work).
- The functional severity or trajectory of the child's autism (these are partly genetic but heavily modulated by environment, intervention, and time).

Genetic testing is one input. It's a powerful one. It's not the whole answer.

## Pharmacogenomics — the most underutilized clinical use of autism genetics

When an autistic child is prescribed any psychiatric medication (SSRI, antipsychotic, stimulant, mood stabilizer), a pharmacogenomic panel substantially improves the match between drug and metabolizer status. CYP2D6 polymorphisms in particular dramatically affect SSRI metabolism — a poor metabolizer can have toxic levels at standard doses, while an ultra-rapid metabolizer gets no effect at standard doses. Standard pediatric prescribing usually ignores this.

Commercial pharmacogenomic panels (Genomind, GeneSight, Tempus PGx, others) are increasingly insurance-covered. For any autistic child being prescribed psychiatric medication, this should be a routine pre-prescription test.

## What's at the frontier (2026)

- **Polygenic Risk Score (PRS) clinical deployment.** Not standard yet but research-active. Will likely become a stratification tool within 5 years.
- **Whole-genome sequencing as standard of care.** Cost continues to drop. Likely first-line for unexplained autism within this decade.
- **Multi-omics integration.** Pulling genomics + transcriptomics + epigenomics + metabolomics into combined risk-stratification panels. Multiple academic centers building this; not yet clinical.
- **CRISPR-based gene therapy for monogenic autism.** Early animal-model stage. Probably 10+ years from clinical reality. Most likely first-targets: SHANK3, MECP2, FMR1.

## Atlas connections

- **[[HYP-0028 Inherited polygenic risk]]** — primary genomics hypothesis; 781 SFARI Tier 1+2 genes wired in.
- **[[Geschwind_Daniel]]** — UCLA autism transcriptomics, brain-bank, polygenic architecture.
- **[[Chung_Wendy]]** — SPARK cohort, the population-scale infrastructure.
- **[[Frye_Richard]], [[Walsh_William]], [[Yasko_Amy]], [[James_Jill]]** — methylation-cycle genetics → biochemistry → clinical protocol.
- **[[Naviaux_Robert]]** — genetic substrate as Hit-1 of the 3-Hit framework.
- **[[Hannah Poling framework]]** — `causation = P × E → M → Φ`. Genomics characterizes P.
- **[[Epigenetics_of_Autism]]** — the modifiable layer that interacts with this fixed genetic substrate.
- **[[Hollander_Eric]]** — IGF-1 in SHANK3 / Phelan-McDermid as cleanest genotype-stratified intervention example.

## Bottom line for parents

1. **Order CMA + Fragile X + FMR1 + a methylation-cycle SNP panel** for any newly-diagnosed autistic child. Costs are mostly insurance-covered or modest. Yield is meaningful.
2. **Add whole-exome sequencing** if first-line is negative. Yield ~20%. This finds the things first-line misses.
3. **Order pharmacogenomic panel BEFORE prescribing psychiatric medications.** Single most underutilized clinical use of genetics in pediatric psychiatry.
4. **Genetic testing tells you about the substrate, not the trajectory.** Even with a confirmed genetic finding, the child's developmental course depends heavily on environment, intervention, and time. The atlas's broader [[Hannah Poling framework]] and functional-medicine layer is what acts on the modifiable side of this equation.
5. **Cross-link your child's SNP profile with the methylation-cycle protocol architects.** [[Yasko_Amy]]'s framework is the most operationally detailed; [[Walsh_William]]'s biotyping is the most clinically-validated; [[Frye_Richard]]'s leucovorin protocol assumes calibration to MTHFR / methylation-cycle status.

Genetic testing is one of the highest-yield, highest-leverage workups available in autism medicine. It is also one of the most underutilized — most newly-diagnosed kids never get past CMA. Push for the full workup.
