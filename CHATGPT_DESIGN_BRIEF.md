# Causes Atlas (Autism) — Design brief for ChatGPT

> Paste everything below into ChatGPT (or any design-tooled AI) as a single brief. It's complete and self-contained. Ask for hi-fi mockups + visual system + a deck.

---

## TL;DR (read this first)

I'm building **Causes Atlas (Autism)** — an open-source, deterministic, evidence-weighted inference engine that maps every known and speculated cause of autism across 1,400+ peer-reviewed primary sources, and tells each family what's likely driving **their specific child's autism** + what to do about it.

It's not a chatbot. It's a knowledge graph + a math engine + a curated atlas of biomarkers, mechanisms, phenotypes, interventions, and formulations. **No LLMs in the scoring math** — same input always produces byte-identical output, which is why it can be used clinically and submitted to regulators.

I'm submitting it to **HHS under RFK Jr.** for potential adoption as the federal reference atlas for autism causation and intervention stratification. It's MIT-licensed and forkable for any chronic condition (Long COVID, ME/CFS, Lyme, EDS, PANS/PANDAS, PCOS, ADHD, mood disorders).

I need you to **design the visual system**: landing page, parent-facing UI, knowledge-graph view, deep-science view, and an HHS submission deck. The Obsidian-style force-directed knowledge graph is the killer demo — visualize the atlas as a living organism.

The aesthetic must be **medical-journal serious + Apple-Health accessible**. Not startup-bro. Not chatbot-style. Trustworthy enough that a tired parent at 11pm AND a federal policymaker AND a functional-medicine clinician all feel respected.

---

## 1. The mission (the why)

**Mainstream autism research is dominated by population-average studies that systematically dilute subgroup signals.** A trial showing "this intervention doesn't work" in 1,000 children may have hidden a 50% responder rate in the 100 children with a specific biomarker pattern. Effect heterogeneity is the rule, not the exception.

**The Causes Atlas operates under the Hannah Poling framework:**

```
causation = susceptibility (P) × trigger (E) → mechanism (M) → phenotype (Φ)
```

For any specific child, the **conditional risk P(Φ | P, E) matters more than the population-average risk P(Φ | E)**. A vaccine, infection, medication, or environmental exposure that has minor population-average risk can be catastrophic for a child with the relevant susceptibility (genetic, mitochondrial, autoimmune, methylation).

The federally-adjudicated **Hannah Poling case (2008)** establishes this formally: vaccine challenge "significantly aggravated an underlying mitochondrial disorder, which predisposed her to deficits in cellular energy metabolism, and manifested as a regressive encephalopathy with features of autism spectrum disorder." n=1 binding legal finding, mechanism recognized, principle applies broadly.

**Mainstream consensus is one input, not authoritative.** FOIA-released government documents, primary RCTs, and peer-reviewed mechanistic studies are tier-1 evidence. Industry-funded research, fact-check journalism, and advocacy content are explicitly down-weighted.

**Contested status is permanent.** Vaccines, aluminum adjuvants, thimerosal, glyphosate, etc. remain `status: contested` regardless of which direction the published epidemiology tilts. Both directions of evidence are preserved; the user sees both with appropriate weights.

---

## 2. What the atlas does (concretely)

A parent or clinician inputs what they know about the child:

- **Symptoms** (regression after 12 months, severe gut issues, frequent infections, acute-onset OCD/tics, seizures, severe irritability, sleep problems, autoimmune family history, known genetic finding, food sensitivities)
- **Lab results if available** (FRAA folate-receptor antibody, plasma methionine, IL-6/TNF, Cunningham panel, microbiome composition, organic acids, methylation markers, urinary kryptopyrroles, copper:zinc ratio)

The engine runs deterministically and outputs:

1. **WHERE IT COMES FROM** — the dominant biological pattern(s) driving this child's autism, in plain English. Pulled from an 11-dimension phenotype taxonomy:
   - Cerebral folate problem (PHE-0001) — FRAA blocks folate from crossing into brain
   - Mitochondrial / energy-cell pattern (PHE-0002) — Hannah Poling phenotype
   - Inflammation in immune-brain axis (PHE-0003) — IL-6/TNF subset, Tsilioni framework
   - Gut–microbiome pattern (PHE-0004) — Bifido/Prevotella low, Kang MTT subset
   - mTOR / syndromic genetic (PHE-0005) — TSC, PTEN, NF1
   - Fragile X (PHE-0006) — FMR1
   - GABA / chloride imbalance (PHE-0007) — Lemonnier bumetanide subset
   - Walsh under-methylator (PHE-0008) — low histamine, low SAM/SAH
   - Walsh over-methylator (PHE-0009)
   - Pyroluria (PHE-0010)
   - Copper:zinc imbalance (PHE-0011)

2. **WHAT TO DO** — top 3-5 specific actions to discuss with a clinician, **formulation-aware**. Not "consider folate" — but "**Leucovorin oral capsule (RCT-validated, Frye 2018, 78% responder rate in FRAA+ subgroup)**". Each action shows the why in one sentence + the specific formulation that worked in trials.

3. **WHAT TO AVOID** — concrete contraindications based on the child's profile. "Avoid synthetic folic acid (paradoxical worsening in FRAA+)." "Avoid standard turmeric powder (1% bioavailability — proven not to work in this form)."

4. **WHAT TO TRACK** — biomarkers to recheck in 8-12 weeks so you know if it's working.

5. **OPTIONAL: SHOW THE SCIENCE** — drill into all 11 phenotype loadings, full intervention ranking, citation list with PMIDs, evidence balance (positive vs negative studies), atlas signal scores, methodology.

---

## 3. The unique IP (what makes this different from every other autism resource)

These are the design hooks. Lean into them visually.

### A. Formulation-aware evidence elevation

Mainstream meta-analyses average across formulations and dilute signal. The atlas distinguishes:

- **Oral reduced glutathione** (FRM-0001, contested — gut peptidases destroy it) ≠ **Liposomal glutathione** (FRM-0003, mechanism-promising) ≠ **IV glutathione** (FRM-0002, well-established) ≠ **Intranasal glutathione** (FRM-0005, anecdotal+mechanistic, CNS-direct)

- **Standard turmeric powder** (FRM-0016, contested at 1% bioavail) ≠ **Liposomal curcumin** (FRM-0017, 40-50× bioavail) ≠ **Curcumin Meriva** (FRM-0018, 29× bioavail)

- **Synthetic folic acid** (FRM-0015, contested — paradoxical worsening in FRAA+) ≠ **Methylfolate / 5-MTHF** (FRM-0014) ≠ **Leucovorin** (FRM-0013, RCT-validated)

**Negative orthogonal-formulation evidence does NOT cascade down.** A negative oral-curcumin RCT does not impugn liposomal curcumin's score. This is methodologically important and visually compelling.

### B. Quantitative validation (the credibility moat)

The engine has been **quantitatively validated against 8 published autism RCTs**:

| Trial | Intervention | Stratifier | Predicted | Published | Error |
|---|---|---|---|---|---|
| Frye 2018 | Leucovorin | FRAA+ | 0.839 | 0.770 | 0.069 |
| Lemonnier 2017 | Bumetanide | high-Cl⁻ | 0.381 | 0.354 | **0.027** |
| Singh 2014 | Sulforaphane | unstratified | 0.366 | 0.346 | **0.020** |
| Hardan 2012 | NAC | unstratified | 0.366 | 0.357 | **0.009** |
| Hendren 2016 | Methyl-B12 | low methionine | 0.501 | 0.519 | 0.018 |
| Kang 2017 | Microbiota Transfer | GI dysbiosis | 0.760 | 0.889 | 0.129 |
| Tsilioni 2015 | Luteolin | IL-6/TNF+ | 0.332 | 0.263 | 0.069 |
| Owen 2009 | Aripiprazole | behavioral | 0.332 | 0.522 | 0.190 |

**n=8 cohort MAE = 0.067 (6.7 percentage points)**. n=7 within-driver-coverage MAE = 0.049. **4 sub-3% errors spanning 3 mechanistically independent intervention axes** (oxidative stress / methylation / GABA-Cl⁻) — structural replication across axes. This is the central peer-reviewable claim for the manuscript and the credibility argument for HHS.

### C. Determinism

No LLMs in the scoring math. Stable sort by ID. No random seeds. Idempotent ingestion. **Same input → byte-identical output across runs and across machines.** This is what makes it auditable and clinically/regulatorily usable. (The atlas-signal scores match across 3-run determinism tests.)

### D. The autonomous pattern engine

A daily cron job runs 4 finders against the atlas and surfaces emergent patterns:
1. **Emergent edges** — gene × mechanism / gene × phenotype co-mention candidates
2. **Combination gaps** — intervention pairs/triples sharing mechanisms not yet tested
3. **Higher-order hypotheses** — 2nd-order chains where direct edges don't exist
4. **Responder-phenotype gaps** — mixed-evidence interventions missing responder profile

Output → `Discoveries Inbox` Markdown reports. **No candidate is auto-promoted to atlas** — all gated by curator review. **First run surfaced 139 candidates.** Architecturally protected against reflexivity (curator behavior shouldn't drive which entities get more sources, which would bias rankings).

### E. Multi-atlas substrate (the OS thesis)

The same engine + scoring + verify-before-write protocol runs against any atlas. Long COVID v0.1 seed already exists. ME/CFS, Lyme, EDS, PANS, PCOS, ADHD, mood disorders are next forks. **Causes Atlas is an operating system** — autism is just the first instance.

---

## 4. Audience (design for all four)

| Audience | What they need | When |
|---|---|---|
| **Parents** | "Where does my child's autism come from? What do I do?" | 11pm, exhausted, on phone, before a doctor visit |
| **Functional medicine clinicians** | Biomarker panel to order + intervention bundle stratified by phenotype | During a 60-min consult |
| **Researchers** | Knowledge graph + which edges are weak / strong / contested | Building hypotheses + writing grants |
| **HHS / policymakers** | What does the evidence ACTUALLY show across subgroups? Is mainstream consensus complete? | Reviewing federal autism policy, vaccine injury, environmental exposures |

**The same UI must work for all four.** Progressive disclosure. Simple front. Optional drill-down to hardcore science.

---

## 5. Visual ambitions (the design challenge)

### A. The Obsidian-style knowledge graph (most important visual)

The atlas is a living force-directed graph with 7 node types:

- **Hypotheses** (95) — causal claims, e.g., "FRAA antibodies cause cerebral folate deficiency"
- **Mechanisms** (34) — biological pathways, e.g., "FOLR1 receptor blockade"
- **Phenotypes** (11) — the 11 dimensions above
- **Genes** (1,564 — SFARI Tier 1+2 + atlas additions)
- **Biomarkers** (178) — measurable indicators
- **Interventions** (137) — therapeutic options
- **Formulations** (52) — formulation-level resolution under interventions
- **Sources** (1,462) — primary literature with PMID + study design tier

Edges link them with weighted evidence-strength.

**Visualize this as a constellation that breathes.** Mainstream consensus = bright, contested = dim-but-glowing-with-edges. Researcher's view: zoom into a specific phenotype → see all causal hypotheses connected to it → see all interventions targeting those mechanisms → see all formulations under those interventions → see PMIDs grounding each edge. **This is the killer demo for HHS.** Make it look like a brain scan crossed with a star map.

Inspirations:
- **Obsidian Graph view** (the actual reference — but more refined)
- **The Causes/cycles diagrams in CDC's chronic-disease atlases** (but more alive)
- **Eigenfactor.org's research mapper** (force-directed, beautiful)
- **Daniel Bukszpan's "Diseases" infographics**
- **Bret Victor's "Magic Ink"** (precision + warmth)

### B. The 11-dimension phenotype constellation (per child)

When a parent submits their child's info, the engine returns an 11-dim loading vector. Visualize as a constellation: 11 stars, each star's brightness = loading on that dimension. **Dominant dimensions glow. The pattern shape tells the story.**

Different children produce visually distinct constellations:
- FRAA+ child → PHE-0001 bright, all others dim → **focal pattern**
- Severe GI + dysbiosis → PHE-0004 bright → **focal pattern**
- Multi-pattern child → 3+ dimensions partially lit → **complex pattern, layered approach needed**
- Undifferentiated child → all dim → **need more measurements**

### C. The Hannah Poling causation chain

```
Susceptibility (P)  ×  Trigger (E)  →  Mechanism (M)  →  Phenotype (Φ)
   genetic              vaccine           mito chain          regressive
   mitochondrial        infection         oxidative stress    encephalopathy
   autoimmune           medication        inflammation        autism subset
   methylation          environmental     methylation
                                          GABA/Cl⁻
```

This visual is the explanatory core. Show it horizontally with animated flow. **For each specific child, light up their actual P × E → M → Φ chain.** It tells the family what happened to their child as a story, not as jargon.

### D. The formulation comparison

When recommending an intervention, show formulations side-by-side as cards:

```
[ Standard Curcumin     ] [ Liposomal Curcumin   ] [ Curcumin Meriva       ]
[ powder | oral         ] [ liposomal capsule    ] [ phytosome capsule    ]
[ 1% bioavail           ] [ 40× bioavail         ] [ 29× bioavail         ]
[ ❌ Contested           ] [ ✓ Promising          ] [ ✓ Established        ]
[ Most negative RCTs    ] [ Inflammatory subset  ] [ Inflammatory subset  ]
[  used this form       ]  [ subset response      ] [ Documented in RCTs   ]
```

Color-code: red border for contested-at-formulation, green for established_RCT, amber for anecdotal+mechanistic.

### E. The Δ² research-attention velocity chart

Some entities are accelerating in the literature (more papers per year, more cross-design replication). Visualize this as a small sparkline trajectory next to each phenotype/intervention. **Inflection points = where to invest research attention.**

### F. The evidence-balance bar (for contested entities)

For any contested claim, show:

```
Negative evidence ▓▓▓▓▓░░░░░ Positive evidence
       12 PMIDs                   8 PMIDs
       Tier weight 0.62           Tier weight 0.74
```

**Both directions visible. Both weighted. Neither hidden.** This is the anti-flattening visual that distinguishes the atlas from advocacy or fact-check sources.

### G. The calibration-cohort plot

Predicted (engine output) on x-axis vs Published (RCT responder rate) on y-axis. 8 dots labeled with intervention names. Tight diagonal = engine validates against literature. **This is the credibility plot for HHS submission.**

---

## 6. Interaction model (what users do)

```
┌────────────────────────────────────────────────────┐
│ LANDING — "Where does autism come from?"           │
│                                                    │
│ Hero: large Obsidian-style knowledge graph view    │
│ that pulses + invites click. Below: one CTA        │
│ "Map my child's pattern →"                         │
└────────────────────────────────────────────────────┘
                         ↓
┌────────────────────────────────────────────────────┐
│ INPUT — "Tell us about your child"                 │
│                                                    │
│ Two columns of plain-language checkboxes:          │
│   What does your child have? (10 items)            │
│   Lab results, if you have them (10 items)         │
│ One CTA: "Show me the answer →"                    │
└────────────────────────────────────────────────────┘
                         ↓
┌────────────────────────────────────────────────────┐
│ ANSWER — "What we found"                           │
│                                                    │
│ Top: 11-dim CONSTELLATION (this child's pattern)   │
│                                                    │
│ Card 1 (purple): WHERE IT COMES FROM               │
│   Plain-language description of dominant pattern   │
│   + Hannah Poling chain visual for THIS child      │
│                                                    │
│ Card 2 (green): WHAT TO DO                         │
│   3-5 specific actions, formulation-aware          │
│   Each: action + why + specific formulation        │
│                                                    │
│ Card 3 (red): WHAT TO AVOID                        │
│   Concrete contraindications for THIS pattern      │
│                                                    │
│ Card 4 (gold): WHAT TO TRACK                       │
│   Biomarkers to recheck in 8-12 weeks              │
│                                                    │
│ [SHOW THE SCIENCE] expand:                         │
│   - Full 11-dim loadings + bar viz                 │
│   - Full intervention ranking + atlas signal       │
│   - Citation list with PMIDs + study-design tier   │
│   - Knowledge graph view zoomed to THIS child      │
│   - Evidence balance bars per claim                │
│   - Methodology + open-source link                 │
└────────────────────────────────────────────────────┘
                         ↓
┌────────────────────────────────────────────────────┐
│ EXPLORE THE ATLAS (separate route, not required)   │
│                                                    │
│ Full Obsidian graph view of the entire atlas       │
│ Filter by entity type, evidence tier, mechanism    │
│ Click any node → entity detail page                │
│ This is for researchers, clinicians, policymakers  │
└────────────────────────────────────────────────────┘
```

Mobile-first. The whole flow should work as well on a phone at 11pm as on a desktop in a clinic.

---

## 7. Brand / tone

- **Like:** Mayo Clinic + Wikipedia + Apple Health + a serious medical journal
- **Not like:** Headspace (too touchy-feely), startup-bro pitch decks, chatbot UIs, advocacy sites (Autism Speaks, Children's Health Defense — these have agenda baked in; the atlas does not)

**Voice:**
- Calm, precise, respectful
- Plain-language but never condescending
- Cites primary sources visibly
- Acknowledges uncertainty honestly
- Doesn't recommend treatment — it surfaces what literature links to the pattern; clinicians decide
- "What to discuss with your clinician" — never "what to do"

**Type:**
- Headlines: serious sans-serif (Inter, SF Pro Display, Söhne), generous letter-spacing tightening, weight 600
- Body: same family, weight 400, line-height 1.55, font-size 1.05rem minimum
- Data: monospaced for IDs and numerics (JetBrains Mono, IBM Plex Mono)

**Color** (suggest a palette but the constraint is):
- Primary ink: near-black `#1c1c1e`
- Background: warm white `#fafaf7` (not pure white — easier on eyes at 11pm)
- Accents: 4 hues for the 4 answer cards (purple/indigo, green, red, gold) — muted, not Bootstrap default
- Phenotype dimensions: distinct hues that look good on a constellation map (think nebula colors, not crayon box)
- Tier badges: graphite (tier 1), warm gray (tier 2), light stone (tier 3) — typography-only, not hue-coded

---

## 8. Specific deliverables I want from you (ChatGPT / design AI)

Give me:

1. **A complete visual system** — color palette (hex codes), typography scale, spacing scale, component library (cards, buttons, badges, modals)

2. **Hi-fi mockups** for these screens (mobile + desktop):
   a. Landing page with hero Obsidian-graph
   b. Input screen (checkbox flow)
   c. Answer screen with the 4 colored cards
   d. The 11-dim constellation visualization (for one example profile — FRAA+ child)
   e. The Hannah Poling chain visualization
   f. The formulation comparison cards (using curcumin example)
   g. The full atlas explorer (force-directed graph, filter sidebar)
   h. The evidence-balance bar
   i. The calibration-cohort scatter plot
   j. A single entity detail page (e.g., Leucovorin INT-0001)

3. **An HHS submission deck** (~15-20 slides): cover, problem statement, mainstream-consensus-is-incomplete framing, Hannah Poling principle, atlas overview, knowledge graph demo, validation result (the n=8 cohort plot), formulation-aware evidence example, multi-atlas substrate, open-source-and-determinism slide, asks. Tone: serious, technically precise, regulator-respectful.

4. **Logo concepts** (3-5 directions). Suggested motifs:
   - A constellation
   - A neuron with its synapses lit asymmetrically
   - A Hannah Poling-style causation chain abstracted into a glyph
   - A folate / methylation cycle ring
   - The atlas as a fingerprint (pattern unique to each child)

5. **One stunning hero animation concept** for the landing page — describe it in detail. The graph should feel alive without being noisy.

6. **Annotation of the existing Streamlit code** (`ui/simple.py`) explaining where the visual system needs to be retrofitted. We currently use Streamlit for the prototype; future is React/Next.js with the FastAPI backend the project already ships.

---

## 9. Constraints (these are non-negotiable)

- **Open source MIT license.** Everything visible, forkable, auditable.
- **Determinism.** No LLMs in scoring math. Mockups can show LLM-style explanations only as a CLEAR overlay tagged "explanation" on top of the deterministic engine output.
- **No telemetry / no login.** A parent can use it without making an account or sending data anywhere except the inference call.
- **Accessible.** WCAG AA contrast minimum. Mobile-first. Works on a 5-year-old phone.
- **Honest.** The atlas surfaces what the literature shows; it does NOT recommend treatment. "What to discuss with your clinician" framing throughout.
- **Contested-evidence preserved.** Both directions of evidence visible for any contested claim. No collapsing into mainstream-consensus framing.
- **Cited.** Every claim in the UI has a reachable PMID + study design tier. Click any claim → see the evidence balance bar.

---

## 10. What's already shipped (so you can ground mockups in real content)

These are real entities the design must accommodate:

### Real phenotype names (use these verbatim — they're already plain-English)

```
Cerebral folate problem
Mitochondrial / energy-cell pattern
Inflammation in the immune-brain axis
Gut–microbiome pattern
mTOR / syndromic genetic pattern
Fragile X (FMR1) pattern
GABA / chloride imbalance pattern
Walsh under-methylator pattern
Walsh over-methylator pattern
Pyroluria pattern
Copper:zinc imbalance
```

### Real top-scoring formulations (with their actual scores out of 100)

```
FRM-0013  Leucovorin (folinic acid) oral capsule       95.00  (RCT-validated)
FRM-0036  VSL#3 / Visbiome multi-strain probiotic      91.61  (RCT-validated)
FRM-0041  Melatonin standard release                   88.57  (RCT-validated)
FRM-0034  Bifidobacterium infantis EVC001              88.53  (RCT-validated)
FRM-0020  Acetyl-L-carnitine (ALCAR — BBB crossing)    85.51  (RCT-validated)
FRM-0047  L-carnosine 800mg (Chez 2002 protocol)       85.51  (RCT-validated)
FRM-0007  NAC oral capsule (Hardan 2012)               85.37  (RCT-validated)
FRM-0038  Bumetanide oral tablet (Lemonnier 2017)      84.97  (RCT-validated)
FRM-0014  Methylfolate (5-MTHF) oral                   77.77  (well-established)
FRM-0011  Methyl-B12 subcutaneous (Neubrander)         84.42  (RCT-validated)
FRM-0017  Curcumin liposomal                           69.42  (anecdotal+mechanistic)
FRM-0028  Sulforaphane w/ active myrosinase            84.57  (RCT-validated)
```

### Real contested-at-formulation-level (use as "what to avoid" examples)

```
FRM-0001  Glutathione (oral reduced GSH capsule)       contested  20.00
FRM-0015  Folic acid (synthetic) oral                  contested  20.00
FRM-0016  Curcumin standard (turmeric powder)          contested  20.00
FRM-0027  Vitamin D2 (ergocalciferol)                  contested
FRM-0029  Sulforaphane WITHOUT myrosinase              contested
FRM-0031  Quercetin dihydrate                          contested
FRM-0037  Generic multi-strain probiotic (drugstore)   contested
FRM-0051  Magnesium oxide                              contested
```

### Real cohort-validation data (use for the calibration plot)

n=8 entries; cohort MAE = 0.0665; 4 entries at AE ≤ 0.027 spanning 4 mechanism axes (oxidative stress / methylation / inflammation / GABA-Cl⁻). Engine version: `session4_v0.4.0_profile_vector`. Calibration anchor: INT-0001 leucovorin score 83.35 (must remain ≥80).

### Real atlas counts

- 95 hypotheses / 34 mechanisms / 11 phenotypes / 137 interventions / 52 formulations / 1,564 genes / 178 biomarkers / 1,462 sources
- 117 hypothesis–mechanism edges, 96 intervention–hypothesis edges, 145 intervention–phenotype edges, 38 gene–mechanism edges, 13 gene–phenotype edges, 33 hypothesis–hypothesis edges
- Δ² overlay tracks 5-component research-attention velocity per entity; first run surfaced 139 candidate discoveries for human review

### Real RCTs we've extracted and validated against

Frye 2018 (PMID 27752075) leucovorin / Lemonnier 2017 (PMID 28291262) bumetanide / Singh 2014 (PMID 25313065) sulforaphane / Hardan 2012 (PMID 22342106) NAC / Hendren 2016 (PMID 26889605) methyl-B12 / Owen 2009 (PMID 19948625) aripiprazole / Kang 2017 (PMID 28122648) microbiota transfer / Tsilioni 2015 (PMID 26418275) luteolin / Adams 2011 vitamin/mineral / Wright 2011 melatonin / Chez 2002 carnosine / Rossignol 2012 HBOT review / Frankovich 2017 PANS guidelines.

---

## 11. The HHS submission framing (for the deck)

The single most important thing the deck must communicate to a regulator:

> **"Mainstream autism research is methodologically incomplete because it averages across heterogeneous biological subgroups. The Causes Atlas operationalizes the Hannah Poling framework at scale: deterministic, evidence-weighted, individual-level. We have validated this engine against 8 published RCTs with mean absolute error of 6.7 percentage points on responder-rate prediction, with sub-3% errors across 4 independent mechanism axes — structural replication. We're submitting this to HHS as the federal reference atlas for autism causation and intervention stratification, fully open source, MIT-licensed. The same substrate generalizes to Long COVID, ME/CFS, Lyme, EDS, PANS, PCOS, ADHD, mood disorders."**

Slide topics:
1. Cover — atlas wordmark + tagline + RFK-Jr-aligned positioning
2. The averaging problem (population-average meta-analyses dilute subgroup signals)
3. Hannah Poling framework (the formal n=1 binding finding + the principle generalized)
4. Atlas overview (1,400 sources, 11 phenotypes, 137 interventions, 52 formulations)
5. Knowledge graph demo (Obsidian view, animated)
6. Determinism (no LLMs, byte-identical outputs, auditable)
7. Validation — n=8 cohort scatter plot
8. Formulation-aware example — curcumin / glutathione / folate as cases
9. Contested-evidence preservation (vaccines, glyphosate, etc.) with both directions of evidence visible
10. Δ² research-attention velocity (where the field is moving)
11. Autonomous discoveries pipeline (139 candidate findings surfaced from atlas in one daily run)
12. Multi-atlas substrate — Long COVID, ME/CFS, Lyme, EDS, PANS, PCOS, ADHD as next forks
13. Open-source MIT positioning (forkable, no vendor lock-in, no telemetry)
14. The asks: HHS adoption as federal reference atlas, NIH grant funding to expand cohort, partnership for a HIPAA-compliant clinical deployment pathway
15. Closing slide — "Submitted by: Greg [LAST]. Open source at github.com/abel-causesatlas/Autism. Atlas-signal anchor: leucovorin INT-0001 = 83.35."

---

## 12. The ask in one sentence

**Design a visual system, hi-fi mockups, and a 15-slide HHS submission deck for a deterministic, evidence-weighted, open-source autism causation atlas — with the Obsidian-style knowledge graph as the killer demo and the n=8 RCT validation as the credibility moat. Make it feel like a serious medical journal that a tired parent can also use at 11pm.**

---

## What to send back

1. Visual system (palette, type, spacing, component library)
2. Hi-fi mockups for all 10 screens listed in §8
3. HHS submission deck (15-20 slides)
4. Logo concepts (3-5 directions)
5. Hero animation concept description
6. Annotations on what to retrofit in the existing Streamlit prototype

Estimated turnaround: full system in a single response is aspirational; iterate in batches if needed. Start with palette + landing-page mockup + the Obsidian graph mockup — those three set the tone and let me approve the direction before you go deep.
