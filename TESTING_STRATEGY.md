---
title: "Testing Strategy — autism workup catalog companion"
status: v0.1 — 2026-05-15
companion_doc: v2.0_scored/tests_catalog.csv
audience: parents + clinicians using the actionable functional medicine report
---

# Testing Strategy

A four-tier testing framework that maps cleanly onto the atlas's eleven
phenotype dimensions. Built for a parent who has $300, $1000, or $5000
to spend and wants to know — in that order — what she gets for each
increment.

The framework presumes the foundational principle of the atlas: the
individual-level question `P(Φ | P, E)` matters more than the
population-average `P(Φ | E)`. A child's specific susceptibility profile
determines what to test, in what order, and how to act on results.
Population-average pediatric medicine prescribes the same workup to
every child; the atlas prescribes the workup that the child's clinical
picture warrants.

## Executive summary — the four tiers

| Tier | Budget | What it answers | When you do it |
|---|---|---|---|
| **Foundation** | $300–600 | "What's the broad biology of THIS child?" | First, on every child |
| **Phenotype-specific** | $500–1500 | "Which of the 11 phenotypes is dominant here?" | After Foundation results suggest a direction |
| **Confirmatory** | $1000–3500 | "Is the specific subtype confirmed before committing to expensive treatment?" | When a $300+/mo intervention is being considered |
| **Emerging / specialty** | varies | "What new tools could refine the picture?" | Optional add-ons, research-grade |

You do not need every test. You need the ones the child's clinical
picture warrants. The catalog at `v2.0_scored/tests_catalog.csv` is
exhaustive on purpose so families and clinicians can pick what fits.

---

## Tier 1 — Foundation (do these on every child)

The foundation tier costs $300–600 and delivers ~70% of the
actionable information you'll ever get from testing. Every autistic
child should have this regardless of phenotype suspicion.

### 1. 23andMe Health + Ancestry kit ($99–199) — `TEST-0001`

The lowest-friction entry point into the atlas. Saliva, home-collected,
done.

Why it's foundational: the raw `.txt` download covers MTHFR (C677T,
A1298C), COMT V158M, MAO-A, MTRR, MTR, CBS, BHMT, VDR, GST/GPX, FOLR1
region, and APOE — the full methylation and detox SNP map plus
neurotransmitter-handling SNPs.

Caveat: 23andMe's 2025 bankruptcy means the long-term availability of
their service is uncertain. Download the raw data within 30 days of
receiving results. AncestryDNA (`TEST-0002`) is a comparable
alternative.

**What you do with the data:** upload the `.txt` to two free analyzers:

- **Genetic Genie** (`TEST-0003`, free): methylation cycle SNPs in a
  Yasko-style pathway diagram. Free.
- **NutraHacker** (`TEST-0004`, $22–57): detoxification + supplements-
  to-avoid list. Useful complement to Genetic Genie.

Optional upgrade: **StrateGene** (`TEST-0005`, $75–150) by Dr. Ben Lynch
gives a more clinical pathway-context view of the same SNPs. Best
single mid-tier post-processing tool. **IntellxxDNA NeuroGenomic**
(`TEST-0006`, $500–1500) is the clinician-ordered equivalent — denser
than DTC tools but requires a prescriber and is not insurance-covered.

### 2. Mosaic Diagnostics OAT ($300–400) — `TEST-0010`

Single most informative urine test for autism. 76 markers covering:
- **Yeast / fungal overgrowth** (arabinose, tartaric acid, citramalic acid)
- **Clostridia metabolites** (HPHPA — implicated in dopamine elevation,
  4-cresol — *C. difficile* marker, DHPPA — beneficial)
- **Oxalates** (often elevated in autism; informs calcium citrate +
  hydration protocol)
- **Krebs cycle / mitochondrial intermediates** (citrate, succinate,
  fumarate, malate)
- **Neurotransmitter metabolites** (HVA, VMA, 5-HIAA, quinolinic,
  kynurenic — the kynurenine pathway is highly autism-relevant)
- **B-vitamin functional status** (MMA → B12, kynurenate → B6, FIGlu → folate)

First-morning urine, collected at home, mailed in. ~14–21 day turnaround.

The Genova alternative (Organix, `TEST-0011`, $319–449) is comparable
and bills insurance (~$150 copay). Choose whichever your practitioner is
familiar with reading.

### 3. Standard methylation labs (~$80–200 via Quest/LabCorp) — `TEST-0013`

The 90% solution at Tier 1 pricing. Ask the pediatrician (or order
direct through Quest/LabCorp consumer portal) for:

- **Plasma homocysteine** (BIO-0005) — single most actionable
  methylation marker
- **Methylmalonic acid (MMA)** (BIO-0008) — functional B12
- **Plasma total B12** + **RBC folate** (BIO-0009, BIO-0012)
- **Active B12 (holotranscobalamin)** (BIO-0010) — if available
- **Pyridoxal-5-phosphate (P5P)** (BIO-0013, `TEST-0064`) — active B6

This identifies functional B12, folate, and B6 status. Insurance
typically covers all of these.

Upgrade path: **Doctor's Data Methylation Profile Plasma** (`TEST-0012`,
$180–300) adds SAM, SAH, SAM/SAH ratio, methionine, cystathionine,
cysteine — the full Walsh-protocol panel.

### 4. Baseline labs — CBC + CMP + thyroid + iron + Vit D ($150–400)

Often skipped or done piecemeal. Should be ordered as a panel before
specialty tests:

- **CBC + CMP + lipids** (`TEST-0046`) — rules out anemia, infection,
  liver/kidney issues
- **Comprehensive thyroid** (`TEST-0044`) — TSH + free T4 + free T3 +
  reverse T3 + anti-TPO + anti-Tg. Not just TSH.
- **Ferritin + iron panel** (`TEST-0045`) — ferritin <50 ng/mL drives
  sleep/behavior in subset
- **Vitamin D 25-OH** (`TEST-0043`) — target 40–70 ng/mL (above
  mainstream's >30 threshold)
- **hs-CRP + ESR** (`TEST-0047`) — systemic inflammation baseline

All insurance-covered with standard pediatrician order.

### 5. Genetic first-tier — CMA + Fragile X (often insurance-covered)

For any child with autism, ID, or DD diagnosis, the ACMG
recommends CMA and Fragile X as first-tier tests:

- **Chromosomal microarray** (`TEST-0007`, $300–2000) — picks up
  15–20% of autism cases (15q11-q13, 16p11.2, 22q11.2, etc.)
- **Fragile X CGG repeat** (`TEST-0008`, $200–400) — 1–2% of autism
  cases

Both are usually insurance-covered with an autism/DD diagnosis. If
WES (`TEST-0009`) is being considered later, CMA must come first.

### Foundation tier total cost

Out-of-pocket if no insurance:
- 23andMe + analyzers: ~$120
- Mosaic OAT: ~$350
- Doctor's Data methylation: ~$250 (skip if doing standard labs first)
- Baseline labs + Vit D + thyroid: ~$300
- CMA + Fragile X (when insurance covers): $0
- **Total ~$700 out-of-pocket / $300 if pediatrician orders the
  baseline labs through insurance**

This is the minimum viable workup. Most actionable findings come from
this tier.

---

## Tier 2 — Phenotype-specific (do based on Tier 1 results)

After Tier 1, the picture usually points to one or two of the eleven
phenotypes. Tier 2 confirms the phenotype and refines the intervention
target. Listed by phenotype.

### PHE-0001 Cerebral folate deficiency — leucovorin responder

**Tier 2 test:** **FRAA — folate receptor alpha autoantibody**
(`TEST-0014`, $200–400).

Single most important biomarker in the entire atlas. Positive in ~70%
of autistic children per multiple studies. Frye 2018 RCT used FRAA
status to stratify the leucovorin responder cohort and saw a 50%+
language gain in FRAA+ children. INT-0001 leucovorin is the
calibration anchor of the entire atlas (CSRS 83.35) because of FRAA.

Workflow: if Tier 1 OAT shows neurotransmitter metabolite patterns
consistent with low brain folate (low HVA, low 5-HIAA), and/or
methylation cycle anomalies, order FRAA. If positive, a leucovorin
trial (0.5–2 mg/kg/day) is well-supported.

If FRAA is positive, your child is the calibration child for the atlas.

### PHE-0002 Mitochondrial dysfunction

**Tier 2 tests:**

- **Plasma lactate + pyruvate + L:P ratio** (`TEST-0015`, $30–150) —
  if L:P >25, respiratory-chain dysfunction is likely
- **Mayo acylcarnitine profile** (`TEST-0016`, $150–400) — 17% of
  autistic children show abnormal AC profiles per Frye 2013
  (PMID 23340503)
- **Plasma carnitine** (`TEST-0017`, $80–200) — substrate availability

These can be bundled as **Quest Mitochondrial Function Panel**
(`TEST-0108`, $200–500) for cost savings.

Action threshold: if L:P >25 + abnormal AC profile + clinical features
(fatigue, exercise intolerance, regression, multisystem involvement), a
mito cocktail (CoQ10, L-carnitine, B-vitamins, riboflavin, creatine)
is well-supported. This is the **Hannah Poling slot** — the
susceptibility tier that the federal vaccine court adjudicated.

### PHE-0003 Regressive immune-inflammatory

**Tier 2 tests:**

- **Cytokine panel** (`TEST-0049`, $250–500) — IL-6, TNF-α, IL-17 elevation
  suggests neuroinflammation
- **IgG/IgA/IgM/IgE totals + IgG subclasses** (`TEST-0069`,
  `TEST-0070`, $80–300) — required before IVIG consideration
- **ANA + ASCA + anti-thyroid antibodies** (`TEST-0048`, $80–250) —
  autoimmune signal

If the picture is regression at 18–36 months + family history of
autoimmunity + GI inflammation, the PHE-0003 trajectory is established.

### PHE-0004 GI / microbiome

**Tier 2 tests:**

- **GI-MAP** (`TEST-0025`, $400–500) — comprehensive qPCR stool panel;
  most-used in FM autism practice
- Or **Genova GI Effects** (`TEST-0026`, $429–449) — alternative
  3-day collection; insurance billable

If specifically chasing leaky gut:
- **Serum zonulin** (`TEST-0076`, $80–200) — quick yes/no
- **Lactulose/mannitol challenge** (`TEST-0028`, $150–300) — direct
  in-vivo permeability test

If GI symptoms + bloating + cyclic patterns:
- **SIBO hydrogen + methane breath test** (`TEST-0029`, $150–350)
- **Stool calprotectin** (`TEST-0075`, $100–200) — insurance-covered
  IBD screen

### PHE-0005 mTOR pathway syndromic

If macrocephaly + features:
- **TSC1/TSC2 sequencing** (`TEST-0059`, $800–2000)
- **PTEN sequencing** (`TEST-0060`, $500–1500)
- Or order **SFARI gene panel** (`TEST-0105`, $300–1500) or **WES**
  (`TEST-0009`, $1000–5000) for broader coverage

Positive TSC = rapamycin/sirolimus is FDA-approved. Direct treatment
implication.

### PHE-0006 Fragile X

Already covered at Tier 1 via FMR1 CGG repeat (`TEST-0008`).

Also confirm with:
- **MECP2 sequencing** (`TEST-0057`, $500–1500) for Rett (girls
  especially)
- **UBE3A methylation** (`TEST-0058`, $400–1500) for Angelman

### PHE-0007 GABA/Cl− imbalance — bumetanide responder

Currently no commercial biomarker. The "test" is the response trial
itself (Lemonnier 2017 framework). Specialty EEG (`TEST-0114`) may
guide candidacy but isn't widely available.

### PHE-0008 MCAS overlap

**Tier 2 tests:**

- **Serum tryptase baseline + flare** (`TEST-0021`, $50–150) — WHO
  diagnostic criterion is >20% above baseline + 2 ng/mL during a flare
- **24h urine N-methylhistamine** (`TEST-0022`, $150–250)
- **24h urine prostaglandin D2 / 11β-PGF2α** (`TEST-0023`, $200–400)
- **Serum chromogranin A** (`TEST-0024`, $80–200)

At least one mediator must rise during a flare for WHO MCAS criteria.
Practical: H1+H2 antihistamine trial is the cheapest "diagnostic."

### PHE-0009 PANS / PANDAS

**Tier 2 panel** (order as bundle, not individually):

- **Strep PCR / culture** (`TEST-0110`) — active infection rule-out
- **ASO + anti-DNase B** (`TEST-0071`, $40–120) — recent strep
- **Mycoplasma IgG + IgM** (`TEST-0072`, $80–200) — common PANS
  trigger
- **Cunningham Panel** (`TEST-0020`, $995) — five autoimmune
  antibodies; gold-standard PANDAS test

Only order Cunningham if sudden-onset OCD/tics/regression + recent
infection. Don't use as autism screen.

Lyme panel (`TEST-0073`, $300–800) only if tick exposure history.

### PHE-0010 Walsh undermethylator / PHE-0011 Walsh metallothionein-deficient

**Tier 2 Walsh-protocol panel:**

- **Whole-blood histamine** (`TEST-0041`, $80–150) — Walsh methylation
  biotype proxy
- **Plasma copper + zinc + ceruloplasmin** (`TEST-0042`, $80–200) —
  for PHE-0011 Cu:Zn imbalance
- **Kryptopyrrole quantitative urine** (`TEST-0040`, $80–150) — PHE-0010
  pyroluria marker; light-protected sample required

Walsh framework requires the **SAM/SAH ratio from Doctor's Data
methylation profile** at Tier 1 (`TEST-0012`) as the keystone. The
biotype is then refined with whole-blood histamine + kryptopyrroles.

### Tier 2 cost stratification

Most families do one PHE-specific path:

- Folate-focused (PHE-0001): ~$300 (FRAA only)
- Mito-focused (PHE-0002): ~$500 (Mito panel)
- GI-focused (PHE-0004): ~$500 (GI-MAP)
- Immune-focused (PHE-0003 / PHE-0009): ~$1500 (Cunningham + ASO +
  IgG subclass + cytokine panel)
- MCAS-focused (PHE-0008): ~$500 (tryptase + 24h urine mediators)
- Walsh-focused (PHE-0008/9/10/11): ~$500 (DD methylation + WB
  histamine + Cu/Zn + kryptopyrroles)

---

## Tier 3 — Confirmatory / advanced

Order at this tier only if:
1. A $300+/month intervention is being considered, or
2. Tier 1+2 results are ambiguous and a decision hinges on
   clarification, or
3. Specific family history (autoimmunity, mito disease, prenatal
   complications) raises an unresolved question.

### Maternal records retrieval (low-cost, high-leverage)

Three records that cost ~$0–50 and may directly inform the atlas:

- **Mid-pregnancy serum (MSAFP/quad screen)** (`TEST-0083`) → BIO-0179
- **First-trimester PAPP-A** (`TEST-0084`) → BIO-0180
- **Cord blood gas + APGAR retrieval** (`TEST-0085`) → HYP-0040 hypoxia
  susceptibility

Atypical multiples-of-median in MSAFP/PAPP-A predict autism risk in
documented atlas evidence. Cord pH <7.10 or 5-min APGAR <7 confirms
HYP-0040 perinatal hypoxia susceptibility — directly relevant to the
Hannah Poling mitochondrial-vulnerability tier.

Always start here — these records are free or near-free if mom kept
her OB records or the hospital can retrieve them.

### Advanced genetics — WES

**Whole exome sequencing** (`TEST-0009`, $1000–5000) is the canonical
escalation after CMA + Fragile X come back negative. AAP recommends
WES as first-line for global DD/ID. ~25–30% diagnostic yield in
unexplained ASD/ID.

Trio sequencing (proband + both parents) is more interpretable but
more expensive.

### Advanced mitochondrial

If acylcarnitine profile + L:P ratio elevated but inconclusive:

- **Plasma very-long-chain fatty acids (VLCFA)** (`TEST-0099`, $150–400) —
  peroxisomal disorders (ALD, Refsum)
- **Plasma ammonia + uric acid** (`TEST-0100`, $30–80) — urea cycle
- **Glutathione redox (GSH/GSSG)** (`TEST-0066`, $120–250) — James
  biochemistry framework
- **8-OHdG urinary** (`TEST-0067`, $80–150)
- **F2-isoprostanes urinary** (`TEST-0068`, $80–200) — Mayo's preferred

Muscle biopsy is the diagnostic gold standard for mito disease but
invasive; reserve for confirmed clinical suspicion.

### Mold / mycotoxins

If the family lives in a water-damaged building, has visible mold, or
the child has chronic congestion + behavior dysregulation + immune
issues:

- **Mosaic MycoTOX** (`TEST-0030`, $300–400) — ELISA, 11 mycotoxins
- **RealTime Labs panel** (`TEST-0031`, $399–639) — strongest on
  Stachybotrys trichothecenes
- **Vibrant Total Tox Burden** (`TEST-0032`, $400–700) — LC-MS/MS,
  includes heavy metals + chemicals + PFAS

Pair with **Aspergillus species on stool/OAT** to distinguish endogenous
colonization vs exogenous exposure. **HLA-DR/DQ haplotype**
(`TEST-0101`, $200–400) only if pursuing Shoemaker CIRS framework
(contested).

### Heavy metals

- **Quicksilver Mercury Tri-Test** (`TEST-0034`, $405–490) — only
  commercially-available mercury speciation test; distinguishes
  seafood vs amalgam vs environmental sources
- **Quicksilver Blood Metals Panel** (`TEST-0035`, $150–300) — 16
  elements; standard exposure screen
- **Hair Tissue Mineral Analysis** (`TEST-0033`, $99–200) — cheap 2–3
  month exposure proxy; reference ranges differ between labs;
  **Tier 3 contested**

**Avoid DMSA-provoked urine testing** (`TEST-0036`, $200–400) unless
under specialty supervision — mainstream medical bodies explicitly
disavow provoked-urine reference ranges, and DMSA itself carries risk
of mineral depletion in already-depleted children. **Tier 3 contested.**

### Food sensitivity (proceed with skepticism)

- **True IgE specific allergy** (`TEST-0052`, $80–250) — mainstream-
  validated; real anaphylaxis risk
- **Wheat Zoomer** (`TEST-0050`, $300–450) — wheat reactivity +
  permeability bundle
- **Cyrex Array 10** (`TEST-0051`, $300–500) — 180-food IgG/IgA panel

The IgG/IgA approach (Wheat Zoomer, Cyrex Array 10, Mosaic IgG panels)
is mainstream-disputed. AAAAI does not endorse IgG food sensitivity
testing. **Tier 3 contested.** A 4-week elimination/reintroduction
trial is often more diagnostic than the panel result itself.

### Hormone / HPA axis

For prepubertal children, **DUTCH Adrenal** (`TEST-0038`, $200–350) or
**ZRT 4-point saliva cortisol** (`TEST-0039`, $150–250) is the right
choice — diurnal cortisol curve only, no sex hormones.

Full **DUTCH Complete** (`TEST-0037`, $300–700) is uninformative
pre-puberty (sex hormones don't matter yet) — defer until Tanner stage 4+.

### Pharmacogenomics — only if on medication

If the child is on or starting psychotropic medication:
- **Genomind** (`TEST-0053`, $300–750)
- **GeneSight** (`TEST-0054`, $300–1100) — most-used in pediatric psych
- **OneOme RightMed** (`TEST-0055`, $200–400) — broader drug coverage

Mainstream caution: FDA has warned against PGx tests with unapproved
claims, and AACAP notes PGx may inform but should not dictate
pediatric psychiatric prescribing. **Tier 2** but use as one input, not
gospel.

### Sleep + neurology

- **Polysomnography** (`TEST-0081`, $1000–5000) — only if OSA suspected
  (snoring + behavior). OSA in 30–65% of autism per published reports.
- **EEG awake/sleep** (`TEST-0079`, $300–2000) — only if seizures or
  regression with focal features
- **Brain MRI** (`TEST-0082`, $500–3000) — only with neuro-focal signs,
  micro/macrocephaly, or refractory seizures
- **qEEG** (`TEST-0080`, $228–1500) — research-grade, contested for
  clinical use, often paired with neurofeedback

---

## Tier 4 — Emerging / experimental

These are recent (post-2020) commercial offerings or research-grade
tests where the evidence is still maturing. Flag as informational
only, not action-driving.

- **Clarifi ASD salivary microRNA** (`TEST-0090`, $989) — Quadrant
  Biosciences epigenetic ASD aid-in-diagnosis; FDA Breakthrough Device
  designation. 82% sensitivity / 88% specificity claimed. Not a
  standalone diagnostic.
- **NeuroPointDX NPDX ASD blood test** (`TEST-0091`) — 32 plasma
  amines stratified into 4 autism metabotypes. Validation maturing.
- **TruDiagnostic TruAge / DunedinPACE** (`TEST-0089`, $229–499) —
  epigenetic biological age. Validated 20–70yo only; pediatric use
  experimental. Useful for parental health, rarely for child.
- **GlycanAge** (`TEST-0106`, $179–279) — IgG glycosylation
  inflammation aging proxy. Adult-validated.
- **HRV wearables** (Oura `TEST-0086`, Apple Watch `TEST-0087`,
  Whoop `TEST-0088`) — consumer-grade autonomic monitoring. Not
  validated for clinical ASD use, but useful for older
  cooperative kids tracking regulation patterns.
- **SARS-CoV-2 immune memory panel** (`TEST-0103`) — for documented
  post-COVID neurodevelopmental regression cases only.

---

## Interpretation framework per phenotype

Each phenotype tier in the catalog corresponds to a specific
intervention bundle. The pattern: **biomarker → mechanism → intervention**.

| Phenotype | Test results that confirm | Primary intervention |
|---|---|---|
| PHE-0001 CFD | FRAA+ | High-dose leucovorin (INT-0001) |
| PHE-0002 Mito | L:P>25, abnormal AC, low free carnitine | Mito cocktail (INT-0011, INT-0012) |
| PHE-0003 Immune | Cytokine elevation + autoimmune antibodies + IgG subclass deficit | LDN, IVIG, methylprednisolone protocols |
| PHE-0004 GI | Dysbiosis on GI-MAP, elevated zonulin, high HPHPA on OAT | Probiotics, antimicrobials, GFCF trial, FMT |
| PHE-0005 mTOR syndromic | TSC1/2 or PTEN variant on WES | Sirolimus/rapamycin (off-label except TSC) |
| PHE-0006 Fragile X | FMR1 CGG >200 | Phenotype-targeted clinical trials |
| PHE-0007 GABA/Cl− | EEG signature, clinical response trial | Bumetanide |
| PHE-0008 MCAS | Tryptase or mediator elevation | H1+H2, cromolyn, ketotifen, luteolin |
| PHE-0009 PANS/PANDAS | Cunningham+, ASO+, sudden onset | Antibiotics, IVIG, NSAIDs, LDN |
| PHE-0010 Pyroluria | Kryptopyrroles >20 µg/dL, low whole-blood histamine | B6/P5P + zinc + GLA + magnesium |
| PHE-0011 Cu:Zn imbalance | Cu:Zn >1.2, low ceruloplasmin | Zinc supplementation, molybdenum, metallothionein protocol |

---

## Cost stratification — three accessibility tiers

### "$300 workup" (insurance-leveraged minimum)

Order through pediatrician with autism diagnosis. Insurance typically
covers all of these:

- CBC + CMP + lipids
- Comprehensive thyroid + anti-TPO + anti-Tg
- Ferritin + iron panel
- Vit D 25-OH
- Homocysteine + MMA + RBC folate + plasma B12
- CMA + Fragile X
- ASO + anti-DNase B if PANS suspected
- Standard mineral panel
- hs-CRP

Out-of-pocket: copay + bloodwork fees, often $100–300 total.

This is the minimum-viable workup. ~40% of actionable signal.

### "$1000 workup" (Foundation tier)

Add to the $300 workup:
- 23andMe + Genetic Genie/NutraHacker analysis (~$120)
- Mosaic OAT (~$350)
- FRAA (~$300) if folate-cycle picture suggests it

Out-of-pocket: ~$700–1000 total. ~70% of actionable signal.

### "$3000 workup" (Foundation + one PHE-specific path)

Add to the $1000 workup, **one** phenotype-specific bundle:

- Folate: FRAA + DD methylation = +$500
- Mito: Mayo AC + lactate/pyruvate + carnitine = +$700
- GI: GI-MAP + zonulin = +$600
- Immune: Cytokine panel + IgG subclasses + ANA = +$1000
- PANS: Cunningham + ASO + Mycoplasma + IgG subclasses = +$1500
- MCAS: Tryptase + 24h N-methylhistamine + PGD2 = +$700
- Walsh: DD methylation + WB histamine + Cu/Zn + kryptopyrroles = +$700

Out-of-pocket: ~$1700–3000. ~85% of actionable signal.

### "$5000+ workup" (Foundation + advanced + WES)

Add WES ($1000–3000), mold panel ($400), advanced mito (VLCFA + GSH +
F2-iso, ~$500), DUTCH Adrenal ($300), and one Tier 2 PHE bundle of
your choice.

Out-of-pocket: ~$5000+. ~95% of actionable signal. Diminishing
returns above this.

---

## Honest evidence-tier disclosure

Per the atlas's epistemic principles, every test is tagged in
`tests_catalog.csv` with `evidence_tier`:

| Tier | What it means | Examples |
|---|---|---|
| **Tier 1** | Clinical-grade — CLIA-certified, peer-reviewed validation, standard of care | CMA, Fragile X, lactate/pyruvate, MAYO acylcarnitine, tryptase, calprotectin |
| **Tier 2** | Functional-medicine standard — CLIA-certified, widely used in FM practice, less mainstream RCT validation | GI-MAP, OAT, DD methylation, FRAA*, DUTCH |
| **Tier 3** | Contested — used in FM but mainstream-disputed | DMSA-provoked urine, IgG food panels, urinary neurotransmitters, HTMA, kryptopyrroles, qEEG, casein/gluten urine peptides |
| **Tier 4** | Emerging — newer, less validated | Clarifi ASD, NeuroPointDX, TruAge in pediatrics, GlycanAge |
| **Tier 5** | Experimental | Research-only assays not yet commercial |

*FRAA is a special case: clinical-grade evidence base via Frye 2018 RCT
(PMID 27752075) but only available through specialty research labs.

The atlas does **not** dismiss Tier 3 tests. It records them and
weights them appropriately. Per epistemic principle §9, mixed
published evidence usually reflects responder-subset heterogeneity,
not absence of effect. The catalog flags `contested=TRUE` so families
and clinicians can act with eyes open.

---

## When to escalate to specialty care

The atlas's testing catalog is foundational, not a substitute for
clinical care. Escalate to specialists when:

- **Pediatric neurologist**: regression with neurologic features
  (seizures, focal signs, abnormal movements), abnormal EEG, refractory
  sleep dysregulation, motor stereotypies suggesting tic disorder.
- **Clinical geneticist**: dysmorphic features, family history of
  intellectual disability, micro/macrocephaly, multi-system involvement
  before WES is ordered.
- **Pediatric immunologist**: recurrent infections, IgG subclass
  deficiency, suspected primary immune deficiency, IVIG decision.
- **Pediatric GI**: refractory GI symptoms, blood in stool, elevated
  calprotectin >250 µg/g, suspected IBD or eosinophilic
  esophagitis.
- **Pediatric mito specialist** (rare): mito-disease-pattern features
  (multisystem, exercise intolerance, ophthalmoplegia, deafness) + L:P
  elevation, before muscle biopsy.
- **Functional medicine pediatrician (MAPS / Frye / Walsh-trained)**:
  for integrating multi-lab results and designing individualized
  intervention protocols. The atlas's testing catalog feeds directly
  into this workflow.

---

## What the catalog does NOT contain

These are deliberate gaps you should know about:

- **In-house clinical exam** (developmental assessment, ADOS-2, sensory
  profiles) — domain of developmental pediatricians and speech/OT/PT
  evaluators. Out of scope here.
- **Imaging beyond brain MRI** — abdominal imaging, cardiac echo, etc.
  are condition-specific and ordered as clinically indicated.
- **Newborn screen detailed state-by-state coverage** — varies by state;
  retrieval (`TEST-0061`) is universally recommended but the panel
  contents differ.
- **Outside-US-only tests** (e.g., Australian / European-only FM
  panels) — included only if also US-available.
- **Many minor variations** of cytokine panels, oxidative-stress
  panels, etc. — the catalog covers representative offerings; specific
  practitioner preferences will vary.

---

## How to use the catalog programmatically

`v2.0_scored/tests_catalog.csv` is structured for the actionable
report pipeline. Each row has:

- `maps_to_phenotype_ids` — comma-separated PHE IDs the test informs
- `maps_to_biomarker_ids` — BIO IDs the test directly measures
- `maps_to_mechanism_ids` / `maps_to_hypothesis_ids` /
  `maps_to_intervention_ids` — atlas-wide cross-references

So a downstream report engine that knows the child's profile vector
(which PHE-X are flagged) can pull `WHERE maps_to_phenotype_ids
CONTAINS 'PHE-XXXX'` and rank by `evidence_tier`, `cost_usd_low`, and
`pediatric_available` to produce a child-specific testing roadmap.

The catalog is meant as the foundation data layer for the actionable
report product spec — every test recommended in the report should
have a row here.

---

## Summary — one paragraph

For a $300 budget, do the insurance-leveraged baseline (CMA + Fragile X
+ thyroid + Vit D + homocysteine + MMA + RBC folate + ferritin + CRP).
For $1000, add Mosaic OAT + 23andMe with free post-processing. For
$3000, add one phenotype-specific bundle based on Tier 1 results
(FRAA if folate-cycle pattern, mito panel if energy/regression
pattern, GI-MAP if gut-dominant, Cunningham if PANS-pattern, Walsh
panel if Walsh-pattern). Above $3000, returns diminish — WES + advanced
metabolic adds capacity for rare findings. The single most important
test in the entire atlas is **FRAA (`TEST-0014`)** — if positive, your
child is on the calibration anchor path that defines the atlas's
strongest evidence base (INT-0001 leucovorin, Frye 2018 RCT,
CSRS 83.35). Order it second, after the standard methylation labs
confirm the cerebral folate biochemistry pattern.
