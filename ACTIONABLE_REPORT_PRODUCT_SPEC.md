---
title: "Actionable functional medicine report — product spec"
status: draft v0.1 — 2026-05-14
audience: founder + future product agent
companion_doc: SIX_MONTH_FAILURE_MODES.md
---

# The actionable functional medicine report

## The customer

A mother of a child diagnosed with — or showing early signs of — autism
spectrum disorder. She is functional-medicine-aware: she has heard of
MAPS, ARI, Walsh, Frye. She is willing to spend $500-$5000 on tests if
the report makes the results actionable. She does NOT trust population-
average pediatric medicine to give her child-specific guidance. She is
NOT looking for a diagnosis (she already has one). She wants to know:

  1. What is driving MY child's specific presentation?
  2. What can I test to find out more?
  3. When the tests come back, what do they mean?
  4. What can I do — concretely, today — based on what I learn?
  5. How will I know if it's working?

## The analog the founder uses

The founder's own experience model: he uploaded three reports —
**IntellxxDNA** (saliva-based nutrigenomic panel), **TruAge
TruDiagnostic** (epigenetic biological-age + inflammation), and **Quest
Diagnostics** (standard blood panel + extras) — to a personalized
longevity service. He got back an integrated, actionable, "here is your
specific roadmap" report. He wants that experience for autism families.

This is the correct product instinct. The functional medicine community
in autism is already doing this manually — practitioners with $500-$2000
intake fees synthesize multi-lab workups into personalized
recommendations. The atlas can do it at scale, with the substrate's
evidence-tiering visible, and at a fraction of the cost.

## The data inputs (what a mom uploads)

In rough priority order by leverage, with the atlas's BIO-XXXX entries
that interpret each test:

### Tier 1 — high-leverage, low-cost (do these first)

1. **23andMe / AncestryDNA raw data** ($0 if already done; ~$99 if new)
   → run through SNP→variant analyzer
   → maps to atlas gene entries (FOLR1, MTHFR, COMT, MTRR, MTR, MAOA,
     SHANK3 *risk SNPs*, TSC1/2, FMR1 CGG repeat surrogate, etc.)
   → outputs susceptibility profile (P-slot in P×E→M→Φ)

2. **Organic Acids Test (OAT)** — Great Plains Laboratory or Mosaic
   Diagnostics; ~$300
   → 76 metabolic markers (oxalates, arabinose, HPHPA, 4-cresol, quinolinic
     acid, kynurenic acid, citrate cycle, fatty acid oxidation, B-vitamin
     markers, neurotransmitter metabolites)
   → maps to atlas BIO entries (urine_oxalate, arabinose, HPHPA,
     4_cresol, quinolinic, mma_methylmalonic, fia, hpla, glutaric, etc.)
   → outputs mechanism activity (M-slot)

3. **Methylation panel** — Doctor's Data, ZRT, or Genova Diagnostics;
   ~$250
   → SAM, SAH, SAM/SAH ratio, methylcobalamin, methylfolate,
     homocysteine, MMA, RBC folate
   → maps to BIO-0001 (SAM), BIO-0002 (SAH), homocysteine, etc.
   → outputs methylation phenotype (Walsh under-/over-methylator)

### Tier 2 — phenotype-specific (do based on Tier 1 results)

4. **Cunningham Panel** (Moleculera Labs; ~$925) — only if PANS/PANDAS
   suspected (sudden onset OCD/tics/behavioral regression after strep)
   → CaM kinase II, anti-D1, anti-D2, anti-lysoganglioside, anti-tubulin
   → maps to PHE-0009 PANS overlap
   → outputs immune-autoreactivity phenotype

5. **Comprehensive Stool Analysis** — GI-MAP from Diagnostic Solutions;
   ~$400 — only if GI symptoms or regression with GI onset
   → 16 commensal panels, pathogens, parasites, candida, zonulin,
     calprotectin, beta-glucuronidase, secretory IgA
   → maps to PHE-0004 GI/microbiome phenotype
   → outputs gut-axis phenotype

6. **Mitochondrial panel** — Mayo Clinic, Genova, or specialty labs;
   ~$500
   → lactate, pyruvate, L:P ratio, acylcarnitine profile, CoQ10, B-vits
   → maps to PHE-0002 mitochondrial
   → outputs mito-vulnerability tier (Hannah Poling slot)

7. **Mast cell / MCAS markers** — Quest or LabCorp; ~$300
   → tryptase, plasma histamine, urine N-methylhistamine,
     prostaglandin D2, chromogranin A
   → maps to PHE-0008 MCAS overlap

### Tier 3 — confirmatory / advanced (do if Tier 1 + 2 suggest a path)

8. **Maternal serum prenatal screening retrieve** — if mom kept records
   from her pregnancy → MSAFP, PAPP-A, hCG, uE3 multiples-of-median
   → maps to BIO-0179, BIO-0180 and HYP-0076 prenatal screening
     marker anomaly

9. **Heavy metal panel** — Doctor's Data hair or provoked urine; ~$200
   → mercury, lead, aluminum, cadmium, arsenic
   → maps to HYP-0015, HYP-0067

10. **Mycotoxin panel** — RealTime Labs or Vibrant; ~$350 — only if mold
   exposure suspected (water-damaged building history)
   → maps to HYP-0054 / mold cluster

11. **Epigenetic biological age** — TruAge TruDiagnostic; ~$300
   → DunedinPACE pace-of-aging, intrinsic + extrinsic biological age,
     specific tissue age clocks
   → useful but lower leverage for autism specifically; better for
     longevity work; include as optional add-on

## The report structure

For each child profile, output a five-section report:

### Section 1 — Profile (one screen)

A plain-English paragraph: *"Your child's results suggest a
[mitochondrial-vulnerable + methylation-impaired + GI-axis] phenotype
profile. The strongest signal is X. The next-strongest is Y. There are
no findings that suggest [PANS / MCAS / cerebral folate deficiency]
based on the tests you uploaded."*

Color-coded confidence meter for each phenotype dimension (PHE-0001
through PHE-0011) — green/yellow/grey indicating strong-positive,
modest-positive, no-signal.

### Section 2 — What we tested and what we found

A table: every result the mom uploaded, what it measures (plain
English), what it shows (her child's value vs reference + optimal
ranges from the atlas BIO entries), and what the atlas says about what
that means.

This is the educational layer. The mom understands her child's profile
not just as numbers but as biology. Every claim has its PMID source
clickable for the curious / for the practitioner she'll share it with.

### Section 3 — What to do (the actionable layer)

The intervention bundle, ranked by:

- **Atlas signal weight** for her child's specific phenotype profile
- **Cost** (lowest first within tier)
- **Reversibility** (lifestyle/dietary first, supplements next, drugs
  with monitoring last)
- **Safety profile** (mainstream-consensus interventions first;
  contested-status interventions last with explicit warnings)

For each intervention, the report shows:
- What it is, what it does
- Dose range typical in published literature
- Expected effect size (from cohort.yaml responder data when available)
- Who tends to respond (the susceptibility filter)
- Who should NOT take it (the contraindication filter — e.g., methyl-B12
  in COMT++ requires titration)
- Specific formulation guidance (FRM entries — 5-MTHF over folic acid,
  ubiquinol over ubiquinone, etc.)
- **Mandatory disclosure: "consult with a clinician trained in
  functional/integrative pediatrics before starting"**

### Section 4 — What to avoid (the contraindication layer)

The mirror of section 3:
- Foods / nutrients that worsen specific phenotypes
- Drugs from the iatrogenic_exposure_priors table that present higher
  risk for her child's specific susceptibility profile (e.g., children
  with mitochondrial vulnerability should consider extra caution around
  fluoroquinolone antibiotics, certain anesthetics, etc.)
- For the vaccine cluster: this is sensitive ground. The report does NOT
  recommend skipping vaccines. It DOES report what the atlas says about
  susceptibility-specific timing-and-spacing considerations, framed
  explicitly as "discuss with your pediatrician — the atlas records the
  contested evidence at appropriate tier weighting."

### Section 5 — How to track (the iteration layer)

Specific biomarkers to retest at 3 / 6 / 12 month intervals to know
whether the intervention bundle is working. The atlas BIO entries
already have "what to track" framing.

Plus a parent-facing daily/weekly observation log:
- Sleep quality, GI symptoms, language milestones, sensory tolerance,
  social engagement, stim frequency
- Standardized once-monthly behavior questionnaire (e.g., short-form
  ATEC, ABC, or VABS-3 subset depending on age)

This is the **outcome-feedback loop** — and it is the most dangerous
part of the product.

---

## The danger layer

The sub-agent's independent failure-mode review (see
`SIX_MONTH_FAILURE_MODES.md`) identified the highest-probability
6-month catastrophe as a sequence:

  child reaction → viral social attribution → hostile press framing →
  federal credibility erosion

Probability of that full sequence firing within 6 months under current
planned architecture: **estimated 30-40%**.

The mitigations are not optional. They are the product, as much as the
report is.

### Mitigation 1 — Clinician-of-record telehealth layer

**The report does NOT ship directly to parents.** A licensed
clinician (MD, DO, ND, NP) with functional/integrative training
reviews the report before it's released. The clinician can:

- Confirm or modify recommendations
- Add child-specific titration guidance
- Veto interventions that aren't appropriate
- Establish a longitudinal relationship for follow-up

The clinician of record is the legal accountability layer. The atlas
provides the substrate; the clinician owns the recommendation.

This solves four problems simultaneously:
- Liability (the clinician carries professional liability insurance)
- "Practicing medicine without a license" regulatory risk
- The single-bad-outcome viral risk (a clinician caught the issue, not
  an algorithm)
- The functional medicine practitioner network problem (we curate which
  clinicians can be of record; we set the standard)

Revenue: clinician network fees (the clinician charges $100-300 for the
review consult; atlas takes a small platform fee, not test-referral
fees).

### Mitigation 2 — Code-enforced firewall between published evidence and parent-submitted outcomes

The current §24 verify-before-write protocol firewalls PMID
fabrication. We need an analogous firewall for outcome data:

- Parent-submitted outcomes land in a separate table:
  `field_outcomes.csv` with strict schema
- The scoring engine has zero read access to `field_outcomes.csv`
- The published responder-rate calibration (n=8 cohort MAE = 0.067)
  remains fixed against PMID-verified RCTs ONLY
- Field outcomes are surfaced separately as a "parent community report"
  with explicit selection-bias disclaimer
- Precommit hook enforces the firewall (any code that imports
  `field_outcomes` and writes to `v2.0_scored/` is rejected)

This protects the engine's published methodology from outcome-feedback
drift. The 0.049 / 0.067 / 83.35 numbers stay defensible.

### Mitigation 3 — Press-response infrastructure ready before the first inquiry

When the first journalist calls (and one will), the response must
already exist:

- Named medical advisory board spanning mainstream pediatrics +
  functional/integrative medicine (Frye, Walsh-trained MDs, Adams,
  Naviaux on the FM side; mainstream pediatric immunology + autism
  research on the other)
- Line-by-line audit of every Wakefield-co-authored source in the atlas
  with explicit treatment of how it's weighted (currently SRC-001463
  Hulscher is the main one; W_DESIGN 0.50 is non-default)
- A pre-written response kit explaining the methodology in 30 seconds,
  60 seconds, and 5 minutes
- Specific framing: "we record contested evidence at appropriate tier
  weighting; the atlas does not endorse any specific causal claim — it
  reports what the literature says with verifiable provenance"

### Mitigation 4 — The two-tier business model

Inspired by sub-agent's observation that HHS-grade methodology (narrow
TAM) and consumer product (large TAM) pull in opposite directions:

**Tier A — Institutional license** (HHS, NIH, academic medical centers,
patient registries, therapeutics companies). This is the slide-6
cathedral pitch. Charges hundreds of thousands per institution. Keeps
the methodology gold-standard.

**Tier B — Clinician-mediated parent report** (the actionable
functional medicine report described above). Distributed through the
clinician network. Charges $100-300 per report consult, atlas takes a
platform fee. The clinician owns the patient relationship.

**Critical:** Tier B never sells directly to parents. The clinician is
always between the atlas and the parent. This is the structural firewall
that keeps the methodology defensible.

---

## What changes about the engine

Modest. The substrate is mostly already there:

1. **Add an upload-parser layer** — `scripts/parsers/` directory with
   one parser per major lab. Start with the top 5 (23andMe, Great Plains
   OAT, Doctor's Data methylation, Quest standard, Mayo mitochondrial).
   Each parser normalizes lab-specific format to a common JSON profile.
   Engineering risk: high. See sub-agent's review for sizing.

2. **Add a report-generation layer** — `scripts/report/` directory.
   Takes the normalized profile + the atlas data + the clinician-review
   metadata → produces the 5-section report as a templated HTML or PDF.

3. **Add the clinician-review interface** — a separate web app where
   the clinician sees the auto-generated draft report, can annotate /
   modify / veto, and signs off. Out of scope for this session; design
   spec to be written later.

4. **Add `field_outcomes.csv` schema** — separate from `v2.0_scored/`.
   Precommit hook enforces firewall. Documented in `INGESTION_SCHEMA.md`
   §additions.

5. **NO changes to the scoring engine's existing calibration logic.**
   INT-0001 = 83.35 stays the anchor. Published responder-rate cohort
   stays PMID-verified only. The actionable report is downstream of the
   substrate; it doesn't modify the substrate.

## What changes about the living graph (cinematic surface)

Smaller changes, but they make the surface match the product:

1. **Phenotype-click action**: when a parent clicks (or hovers long on)
   a phenotype node, the top-5 atlas-signal-weighted interventions for
   that phenotype + the top-3 biomarkers that stratify it surface as
   highlighted nodes with edges pulsing toward the phenotype. This is
   the "what to do / what to test" interactive answer in the graph.

2. **Constellation kanye-mode**: deepen the void. Stars (the dim
   distant background nodes) get more parallax — slower zoom rate than
   foreground. The aesthetic gets closer to "infinite library" feeling.
   Subtle, not loud.

3. **"YOUR CHILD" callout**: when a profile is loaded, ghost-text in
   the bottom-left says (silently, no animation) the profile name —
   "Hannah Poling · mitochondrial + immune + contested-vaccine".

4. **The four-stage reveal**: when a profile loads, the graph fades the
   non-active nodes first, THEN highlights the active ones, THEN draws
   the edges connecting them, THEN starts particles flowing along the
   strongest edges. The phase-by-phase reveal makes pattern emergence
   visible.

## Priority order — what to build first

In sequence (each step is gated by completion of the previous):

1. **First** — Stand up the medical advisory board (the mitigation that
   blocks all other downstream risk)
2. **Second** — Write `field_outcomes.csv` firewall code + precommit
   hook
3. **Third** — Build parsers for top-3 labs (23andMe raw data, Great
   Plains OAT, Doctor's Data methylation)
4. **Fourth** — Build the report-generation layer as HTML output
5. **Fifth** — Build the clinician-review web interface
6. **Sixth** — Pilot with 5-10 clinician/parent pairs
7. **Seventh** — Public launch in clinician-network model only

The living graph and HHS deck continue in parallel — they're the
institutional/cinematic surfaces, separate from the consumer/clinician
product layer.

## Companion docs

- `SIX_MONTH_FAILURE_MODES.md` — sub-agent's independent risk review
  (cited liberally throughout this spec)
- `INGESTION_SCHEMA.md` — Hannah Poling P×E→M→Φ rules for atlas writes
- `DESIGN_TEAM_HANDOFF.md` — institutional brand positioning for the
  cinematic / deck surfaces
- `CLAUDE.md` — verification protocol §24; epistemic principles §1-9

---

*Draft v0.1 written 2026-05-14. Companion to SIX_MONTH_FAILURE_MODES.md.
This document is intentionally incomplete — the clinician-network
architecture and the parser engineering spec are out of scope for this
draft and will be written in dedicated follow-up specs.*
