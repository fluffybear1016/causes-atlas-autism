---
id: TOPIC-TESTING-PRIORITY
type: testing_strategy
audience: parent, clinician
purpose: The ranked test ladder for an autism family — what to order in what order, why, and what the atlas does with each.
last_updated: 2026-06-23
post_sfari_integration: true
---

# Autism testing priority ladder

> **Bottom line:** SPARK (free Whole Exome Sequencing) + FRAA test cover ~80%
> of the decision-relevant ground for an autistic child. 23andMe is the
> cheapest paid genetic test but it is **not the best for autism** — it misses
> the rare and de novo variants where most monogenic autism signal lives.
> Use it only as a fast adjunct for the functional-medicine methylation
> panel (MTHFR, COMT, GST) while waiting for SPARK results.

The atlas integrates [[SFARI Gene]] as a tier-1 backbone (1,277 graded
autism-associated genes, refreshed quarterly). Test selection below is
ordered to maximize evidence-per-dollar against that backbone.

## Tier 1 — order today, every autism family

### SPARK Whole Exome Sequencing
- **Cost:** FREE
- **Turnaround:** 6–12 months
- **What it covers:** rare + de novo variants across all ~20,000
  protein-coding genes. This is where the bulk of monogenic autism
  signal lives — common-SNP chips miss it entirely.
- **Sponsor:** Simons Foundation Autism Research Initiative ([[SFARI]])
- **Enroll:** `sparkforautism.org` — eligibility is having a child with
  professional ASD diagnosis.
- **What you get back:** clinically actionable findings (~10–15% of
  families receive a diagnostic variant), interpretation from a
  board-certified genetic counselor, and entry into [[Simons Searchlight]]
  natural-history studies if your child's variant is in one of the 184
  gene communities (SYNGAP1, SCN2A, STXBP1, CHD8, etc.).
- **Atlas integration:** when results come back, upload to the atlas's
  intake — the report stratifies interventions against every SFARI
  Tier 1/2 variant detected and surfaces active Searchlight communities.

### Invitae Autism Spectrum Disorder panel
- **Cost:** $250–$400 (insurance often covers when ordered clinically)
- **Turnaround:** 2–4 weeks
- **What it covers:** ~100 of the highest-confidence SFARI Tier 1 genes,
  CLIA-certified clinical-grade sequencing.
- **Order through:** pediatrician, developmental pediatrician, or
  geneticist. Many functional medicine practitioners can order it.
- **Why both this AND SPARK:** Invitae is fast and clinical-grade, SPARK
  is comprehensive and free but slow. Run them in parallel.

### Folate Receptor Alpha Autoantibody (FRAA) blocking-antibody test
- **Cost:** $200–$400
- **Turnaround:** 3–6 weeks
- **Lab:** Religious Sisters of Mercy / Iliad Neurosciences (Ramaekers
  blocking assay specifically — confirm with the ordering lab; the
  Cunningham Panel uses different assays and is NOT the same test)
- **What it catches:** maternal or postnatal autoantibodies to FOLR1
  (folate receptor alpha) that block folate transport across the
  blood-brain barrier.
- **Why this is in Tier 1:** it is **the single most important biomarker
  for predicting [[INT-0001]] leucovorin response in autism.** The atlas
  calibration anchor — INT-0001 Leucovorin CSRS 83.35 — is grounded in
  Frye 2018's stratified RCT showing 50%+ effect size in the
  FRAA-positive subset.
- **Atlas hypothesis:** [[HYP-0001]] FOLR1 autoantibodies / cerebral
  folate deficiency. ~10–25% of autism cases are FRAA-positive.
- **Particularly indicated if:** language regression, communication delay,
  or any cerebral-folate-deficiency clinical pattern.

## Tier 2 — order based on suspected phenotype

### Whole Genome Sequencing (WGS)
- **Cost:** $200–$400 (Nebula Genomics, Dante Labs)
- **Turnaround:** 4–8 weeks
- **Adds vs WES:** non-coding regions, structural variation detection.
  Not all autism risk is in coding regions; ~10% of monogenic signal is
  in regulatory regions WES misses.
- **When to consider:** if SPARK + Invitae come back negative but the
  clinical picture strongly suggests a genetic cause. Or as a first-line
  if budget allows and you don't want to wait for SPARK.

### Organic Acids Test (OAT)
- **Cost:** $300
- **Turnaround:** 2–3 weeks
- **Lab:** Mosaic Diagnostics (formerly Great Plains Labs), Genova
- **What it catches:** urine markers of mitochondrial dysfunction
  (lactate, pyruvate, citric acid cycle intermediates), oxidative
  stress (8-OHdG, F2-isoprostanes), and microbial-metabolite excess
  (arabinose, HPHPA, 4-cresol from clostridia).
- **Atlas mechanisms it stratifies:** [[MEC-0010]] Mitochondrial
  dysfunction, [[MEC-0021]] SCFA signaling, [[MEC-0024]] p-cresol /
  4-EPS aromatic metabolite production.
- **Particularly indicated if:** regression after illness, fatigue,
  GI symptoms, suspected mito or fungal/clostridia overgrowth.

### GI-MAP or Genova GI Effects
- **Cost:** $300–$500
- **Turnaround:** 2–3 weeks
- **What it catches:** microbiome composition by qPCR, gut pathogens,
  inflammation markers (calprotectin, secretory IgA, zonulin),
  beneficial-bacteria deficits.
- **Atlas phenotype it stratifies:** [[PHE-0004]] Gut-brain axis
  phenotype. Atlas hypotheses [[HYP-0007]] (microbiome dysbiosis),
  [[HYP-0056]] (Bifidobacterium depletion), [[HYP-0059]] (intestinal
  barrier permeability).
- **Particularly indicated if:** any GI symptoms (constipation,
  diarrhea, bloating, food sensitivities, eczema).

## Tier 3 — useful but secondary

### 23andMe / AncestryDNA raw data
- **Cost:** $99–$199
- **Turnaround:** 4–6 weeks
- **What it actually catches:** ~600,000–700,000 *common* SNPs (minor
  allele frequency > 1%). Misses rare variants entirely.
- **Why it's NOT the best autism test:** common SNPs explain a small
  fraction of autism risk vs the rare and de novo variants WES catches.
- **Useful for:** the functional-medicine methylation panel — MTHFR
  C677T/A1298C, COMT Val158Met, MAOA, GST family, FUT2, VDR. The atlas
  parses raw data and stratifies these.
- **The honest order:** if SPARK is enrolled and Invitae is being ordered
  clinically, 23andMe is **optional**, not essential. If neither of
  those is in motion yet, 23andMe is a reasonable fast-and-cheap starter.
- **The atlas accepts:** 23andMe v5 raw data file, AncestryDNA raw,
  MyHeritage raw, VCF — all upload-supported.

### IntellxxDNA
- **Cost:** $400–$700
- **Turnaround:** 4–6 weeks
- **What it catches:** ~700 SNPs curated for functional medicine
  (methylation, detox, neurotransmitter, mitochondrial, inflammation).
- **Pre-interpreted by:** clinician-friendly report (Lynch / Walsh /
  Yasko frameworks).
- **Useful for:** patients whose functional medicine doctor is already
  IntellxxDNA-literate. Redundant if the family is using the atlas
  directly with 23andMe raw data — the atlas does the same stratification
  more rigorously and at no marginal cost.

### Pharmacogenetics (GeneSight, Genomind)
- **Cost:** $300–$400 (insurance often covers in mental-health context)
- **What it catches:** CYP450 drug-metabolism variants relevant to
  psychiatric medication choice.
- **Useful only if:** psychiatric medication is on the table for this
  child. For most autism families this is Tier 4.

## Symptom-targeted biomarker workup (parallel to genetics)

These are not genetic tests but are essential phenotyping. Order in
parallel with genetics; don't wait for sequencing results.

| Symptom / suspicion | Test | Atlas hypothesis |
|---|---|---|
| Language regression, FRAA suspected | FRAA blocking-antibody (above) | [[HYP-0001]] |
| Mitochondrial decompensation pattern | Lactate, pyruvate, L:P ratio, free + total carnitine, acylcarnitine profile, CoQ10, GDF-15 | [[HYP-0006]], [[MEC-0010]] |
| GI symptoms | GI-MAP (above), zonulin, fecal calprotectin, sIgA | [[PHE-0004]] cluster |
| Methylation status | Homocysteine, MMA, vitamin B12, RBC folate, SAM, SAH | [[MEC-0003]] |
| Oxidative stress | GSH, GSSG, GSH/GSSG ratio, 8-OHdG, F2-isoprostanes | [[MEC-0001]] |
| Mast cell / histamine | Tryptase, methylhistamine, chromogranin A | [[HYP-0075]] MCAS |
| Autoimmune neuropsych onset (PANS/PANDAS) | Cunningham Panel, ASO, anti-DNase B, mycoplasma titers | [[HYP-0074]] |
| Immune dysregulation | CBC w/ diff, IgG/A/M/E, IgG subclasses, T/B cell panel, complement | [[HYP-0008]], [[MEC-0002]] |
| Thyroid | Full panel: TSH, free T3, free T4, reverse T3, TPO + Tg antibodies | [[HYP-0048]] |
| Heavy metals | Hair mineral analysis (screening), urine porphyrins (mercury-specific), provoked urine challenge (specialist) | [[HYP-0015]] |
| Endocrine | DUTCH (urine hormones + cortisol pattern) | [[MEC-0016]] HPA axis |

## What to upload to the atlas

The atlas's intake (UPDATE MY DATA modal on the URL) accepts:

- **Lab PDFs** — Quest, LabCorp, Genova, Mosaic, Invitae, GeneDx,
  23andMe reports, any PDF. Biomarkers + gene mentions auto-extracted.
- **Raw DNA files** — 23andMe v5, AncestryDNA, MyHeritage, VCF.
- **Manual blood-work form** — reference ranges shown; values outside
  range are flagged in the report.

After upload, the atlas generates a report that:

1. Matches the child to one or more of the 11 atlas phenotype subtypes
2. Flags out-of-range biomarkers with severity
3. Ranks atlas interventions (CSRS-scored) by phenotype match
4. Surfaces the highest-yield next tests to order
5. Notes any active Simons Searchlight communities for matched genes
6. Lists safety contraindications based on detected variants
7. Generates an Obsidian-compatible markdown profile of the child

## Cost summary (US, 2026)

| Path | Cost | Coverage |
|---|---|---|
| Minimum viable: SPARK + 23andMe Health | $199 | Free WES (slow) + functional-medicine SNPs (fast) |
| Standard recommended: SPARK + Invitae + FRAA | $450–$800 (often partly insurance-covered) | All autism gene panels + cerebral folate biomarker |
| Comprehensive: SPARK + Invitae + FRAA + OAT + GI-MAP | $1,050–$1,800 | Genetics + metabolic + microbiome |
| Maximalist: all of the above + WGS + DUTCH + Cunningham + IgG sublcasses | $2,000–$3,500 | Full functional-medicine workup |

## A note on insurance

Many functional medicine tests are NOT insurance-covered. However:

- Invitae ASD panel is frequently covered with a clinical diagnosis
- GeneSight is often covered in psychiatric context
- Standard labs (vitamin D, ferritin, homocysteine, MMA, thyroid panel,
  CBC, comprehensive metabolic) are virtually always covered
- FRAA is rarely covered but is one of the highest-yield tests
- 23andMe + Promethease / Genetic Genie is not "medical" testing per
  insurance categories — out-of-pocket only

## Related vault pages

- [[INT-0001]] Leucovorin (folinic acid) — the calibration anchor
- [[HYP-0001]] FOLR1 autoantibodies / cerebral folate deficiency
- [[SFARI]] — SFARI integration overview
- [[Simons Searchlight]] — gene-specific communities
- [[Hannah Poling framework]] — central organizing principle for individual-level resolution
- [[CLAUDE]] — the 11 epistemic principles
