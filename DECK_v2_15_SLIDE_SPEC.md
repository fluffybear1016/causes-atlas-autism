# DECK v2 — 15-slide spec, 5-act structure

> Restructured per ChatGPT feedback after the substrate-thesis upgrade. The substrate is no longer slide 13 — it's introduced quietly in Act 2 as shadow architecture under the autism story, then made explicit in Act 4. **The most important slide is the substrate transition slide (slide 6)** — the moment the audience realizes "this is infrastructure for mechanistic medicine," not "another autism platform."

---

## The category-jump risk (read this before producing any slide)

**Biggest strategic risk:** being perceived as a vertical autism application instead of a substrate company.

**Deck structure determines which category investors and federal reviewers assign you to.**

That category assignment controls:
- valuation ceiling
- institutional interest
- government relevance
- strategic inevitability

If the audience sees "autism" before they see "substrate," they categorize accordingly and the substrate framing becomes an upsell rather than the thesis. Once that frame locks in, it's extremely hard to escape.

**The deck must introduce substrate as shadow architecture early.** Autism is the proof, not the identity.

---

## Aesthetic targets (locked)

- **Yes:** Palantir × CERN × Arc Institute × early DeepMind systems diagrams
- **No:** modern biotech gradient sludge, startup SaaS architecture, cloud infrastructure marketing visuals

Specifically:
- Sparse layouts. Generous whitespace.
- Monospace for data and IDs (IBM Plex Mono).
- Sans-serif for titles + body (Inter or SF Pro Display).
- No drop shadows. No gradients on UI chrome. No skeuomorphism.
- Colors: ink (#1a1a1f), paper (#fbfaf6), moat (#2c2826), single accent (#5e5cb8), warn-red (#b3261e), green (#2e7d32).
- Tone: defense-grade restraint. Scientific knowledge reactor. Not "fun" or "approachable."

---

## 5-act structure

```
Act 1 — The averaging failure        slides 1–3
Act 2 — Deterministic inference engine slides 4–6
Act 3 — Autism atlas as proof         slides 7–9
Act 4 — Validation + institutionalization slides 10–12
Act 5 — National scientific substrate  slides 13–15
```

Each act has a single load-bearing claim. Slides within an act build that claim.

---

## Slide-by-slide spec

### ACT 1 — The averaging failure

**Slide 1 — Cover**

- Title: *Causes Atlas*
- Subtitle: *An open, deterministic substrate for condition-specific causal inference atlases*
- Footer phrase: *Shared infrastructure, condition-specific evidence graphs.*
- Visual: small, restrained constellation icon (one PHE node primary + 2 dim secondaries) — hints at the architecture without revealing it.
- Authors + license + DOI footer
- **Do NOT** put "autism" in the title or subtitle. Autism is in the proof, not the masthead.

**Slide 2 — The averaging problem (the thesis slide)**

- Headline: *Population-average research systematically dilutes biologically distinct responder subgroups.*
- Visual: one large diluted bell curve splitting into 4–6 stacked subgroup curves below it (folate / mitochondrial / immune / gut / GABA / methylation). The aggregate looks null; the subgroups are clearly heterogeneous.
- Body sentence: *A treatment showing "no significant effect" in aggregate may conceal a strong effect in a biologically coherent subgroup. This failure mode is not occasional — it is structural.*
- Footer pull-quote: *Mainstream meta-analytic methods cannot resolve mechanistic heterogeneity.*

**Slide 3 — The Hannah Poling framework**

- Headline: *Federal precedent for individual-level, susceptibility-conditional causation.*
- Hannah Poling chain diagram: `Susceptibility (P) × Trigger (E) → Mechanism (M) → Phenotype (Φ)`
- Body: federally-adjudicated 2008 Vaccine Court ruling formally established that vaccine challenge "significantly aggravated an underlying mitochondrial disorder, which predisposed her to deficits in cellular energy metabolism, and manifested as a regressive encephalopathy with features of autism spectrum disorder."
- Pull-quote: *Conditional risk P(Φ|P,E) is a different quantity from population-average risk P(Φ|E). Different study designs answer different questions.*
- Note: this is when "autism" first appears, but only as the *example* in the federal precedent — not as the project's identity.

### ACT 2 — Deterministic inference engine

**Slide 4 — A new computational substrate is required**

- Headline: *Resolving subgroup heterogeneity at scale requires a substrate that mainstream analytic methods cannot provide.*
- Three constraints listed:
  - Determinism (same input → byte-identical output, byte-identical across machines)
  - Provenance (every claim traces to a PMID-verified primary source)
  - Conditional inference (substrate must compute P(Φ | profile), not P(Φ))
- Subtle: this is the first explicit substrate language. Don't oversell it yet.

**Slide 5 — Determinism (the federal-trust slide)**

- Headline: *Same input → byte-identical output.*
- Sub-bullets:
  - No language-model calls in scoring math
  - Stable sort by ID; no random seeds
  - Idempotent ingestion via node-aliases
  - 3-run byte-identical determinism tests gate every automated pipeline run
- Pull-quote: *Federal infrastructure cannot operate on tools that drift.*
- Visual: minimal — three terminal output blocks showing the same MAE = 0.0665 from three consecutive runs.

**Slide 6 — The cathedral slide**

> *This is the slide where the audience phase-transitions from "interesting research tooling" to "federal-scale scientific infrastructure." If this slide doesn't land, nothing else does. **Slide 6 must visually slow time.** The audience should unconsciously realize: "the company just became much larger than the application." That emotional expansion is the entire game.*

**Strict layout — no exceptions:**

```
┌─────────────────────────────────────────────────┐
│                                                 │
│   The Substrate                                 │  ← title only, restrained
│                                                 │
│                                                 │
│         [ 6-layer diagram, large, centered ]    │  ← museum-style spacing
│                                                 │
│                                                 │
│                                                 │
│                                                 │
│   Shared infrastructure,                        │  ← single sentence
│   condition-specific evidence graphs.           │     bottom-anchored
│                                                 │
└─────────────────────────────────────────────────┘
```

**What this slide MUST contain:**
- Title: *The Substrate* (or *Shared Evidence Infrastructure*) — restrained, no marketing language
- Diagram: the 6-layer artifact (`ui/components/substrate_diagram.html` is the source). Render at high resolution; embed as a single static image. Do NOT use animation or build-in transitions on this slide.
- Footer sentence: *Shared infrastructure, condition-specific evidence graphs.*

**What this slide MUST NOT contain:**
- ❌ Paragraphs of explanatory text
- ❌ Bullet points
- ❌ Sub-headers
- ❌ Icons or chrome around the diagram
- ❌ Build-in animations or stagger transitions
- ❌ Slide-number indicators (suppress for this one slide)

**Why no paragraph:**

Paragraphs create interpretive narrowing, cognitive friction, and defensive reading behavior. The audience's job on this slide is to *complete the implications themselves* — that creates ownership, inevitability, intellectual participation. Explanation reduces perceived depth.

The slide should feel **discovered, not sold**.

**Negative space + slow time:**

This is the cathedral slide. More negative space than any other slide in the deck. No motion. The viewer's eyes have time to traverse the layers. The implications cascade silently in their head. The category reassignment ("oh — this is not an autism company") happens without any verbal prompting.

**Hold time on this slide:** at least 25-30 seconds even if no one says anything. Resist the urge to fill the silence.

### ACT 3 — Autism atlas as proof

> *Now autism appears as the first instantiation. This is the proof, not the company. Phrase choice: "autism instantiation," "autism atlas," "first fully scored atlas." Avoid "our autism platform."*

**Slide 7 — Autism atlas: the first fully instantiated atlas**

- Headline: *Autism instantiation: 1,462 primary sources, 11 phenotype dimensions, 137 interventions, 52 formulations.*
- Architecture: showing how the autism atlas slots into Layer 5 of the substrate diagram (use a small substrate-diagram inset top-right with L5 highlighted).
- Counts strip: 95 hyp / 34 mech / 11 phe / 137 int / 52 frm / 1564 genes / 178 bio / 1462 src.
- Edge counts: 117 hyp-mech / 171 int-mech / 148 int-phe.

**Slide 8 — Knowledge graph (the demo)**

- Visual: a screenshot of `atlas_explorer_preview.html` showing the 295-node force graph in **Research mode**. Top stats banner visible.
- Caption: *Live atlas explorer. Force-directed. Contested-edge dual-color. Filterable. Click any node → entity drawer with PMID provenance.*
- Pull-quote (small, bottom): *The atlas grows daily via the autonomous-discoveries pipeline. No human curates the connection-finding step.*

**Slide 9 — Formulation-aware evidence (the methodological differentiator)**

- Headline: *Negative orthogonal-formulation evidence does not cascade.*
- Three side-by-side cards (curcumin example):
  - Standard turmeric powder · 1% bioavail · contested · FRM-0016 · score 20
  - Liposomal curcumin · 40-50× bioavail · anecdotal+mechanistic · FRM-0017 · score 69
  - Curcumin Meriva (phytosome) · 29× bioavail · established_mechanistic · FRM-0018 · score ~70
- Body: *Mainstream meta-analyses average across formulations and dilute signal. The substrate distinguishes formulation-level evidence from molecule-level evidence. A negative oral-curcumin RCT does not impugn liposomal curcumin's score.*
- Pull-quote: *This is methodologically novel. Mainstream evidence synthesis collapses what the substrate preserves.*

### ACT 4 — Validation + institutionalization

**Slide 10 — Validation against published RCTs**

- Headline: *Cohort responder-rate MAE = 0.067 across n=8 published autism RCTs.*
- Visual: the validation scatter plot with 4 dot classes:
  - Filled indigo: INT-0001 leucovorin (calibration anchor)
  - Emerald: 4 sub-3% AE entries (structural replication cluster)
  - Graphite: within-coverage (Frye, Tsilioni, Kang)
  - Oxide-red hollow: Owen aripiprazole (the documented outlier)
- Annotation arrow on emerald cluster: *4 sub-3% errors across 3 independent mechanism axes (oxidative stress, methylation, GABA/Cl⁻); 5 sub-7% errors across 4 axes when inflammation is included.*
- Pull-quote (small): *Structural replication across independent mechanism axes is not chance.*

**Slide 11 — Contested-evidence preservation**

- Headline: *Contested status is preserved, not erased.*
- Visual: zoomed-in detail of the dual-color edge from the atlas explorer. Show one specific contested edge with proportional weighting:
  - Negative side: 12 PMIDs · tier-weighted score 0.62
  - Positive side: 8 PMIDs · tier-weighted score 0.74
- Body: *Both directions of evidence remain visible at appropriate weights. The substrate does not collapse contested debates into mainstream-consensus framing. Federal regulators see what the literature actually shows.*
- Note: this is the slide that signals to RFK Jr.-aligned reviewers that the substrate respects the evidence, not the consensus narrative.

**Slide 12 — Autonomous discovery pipeline**

- Headline: *The atlas grows daily. No team required.*
- Visual: a stylized depiction of the four pattern miners running daily, output to read-only inbox, curator-gated promotion.
- One concrete example: *Daily run surfaces ~150 candidate findings. Curator reviews. Promotion to atlas requires PMID-verified primary evidence + calibration anchor protocol pass.*
- Pull-quote: *Curator-gated promotion. No language model writes to the canonical scored state.*

### ACT 5 — National scientific substrate

**Slide 13 — Multi-atlas substrate**

- Visual: substrate diagram again, but with L5 expanded to show:
  - Autism atlas (fully instantiated · n=8 RCT validated)
  - Long COVID atlas (v0.1 seeded)
  - Autoimmune atlas (architecture supports)
  - Future forks (community-extensible)
- Body: *Shared infrastructure, condition-specific evidence graphs. The same engine, scoring protocol, verification protocol, and validation framework operate on any chronic condition where effect heterogeneity dominates.*

**Slide 14 — Open-source positioning**

- Headline: *MIT-licensed. No vendor lock-in. No vendor capture.*
- Bullets:
  - All code, atlas data, validation artifacts: github.com/abel-causesatlas/Autism
  - Citation DOI: pending Zenodo deposit
  - Forkable for any chronic-condition community
  - Substrate-level governance via CONTRIBUTING.md hard rules
- Pull-quote: *The substrate is national infrastructure. National infrastructure cannot be vendor-captured.*

**Slide 15 — The asks**

- Title: *Requested federal partnership*
- Three concrete asks:
  1. **HHS evaluation** as federal reference substrate for condition-specific causal-inference atlases
  2. **NIH-supported cohort expansion** of the autism instantiation from n=8 to n=20+ RCTs
  3. **HIPAA-compliant clinical-deployment partnership** for individual-patient deployment beyond the published-literature substrate
- Closing pull-quote (centered, ~24px): *This becomes part of how science itself is conducted.*
- Footer: Atlas anchor INT-0001 = 83.35 · Engine v0.4.0 · github.com/abel-causesatlas/Autism · MIT · DOI pending

---

## Production notes

- **Slide 6 is the critical artifact.** Use `ui/components/substrate_diagram.html` (already built). Render at 2400×1600 or higher; export as PDF; embed in Keynote/PowerPoint.
- **Slide 8 needs a real screenshot** of the atlas explorer in Research mode at a state that shows the contested edges visible. After atlas explorer v2 is rendered, take that screenshot and embed.
- **Slide 10 needs the validation scatter** as a Plotly chart exported to high-res PNG.
- All slides use the same color palette + typography as the substrate diagram for visual consistency.
- Avoid Microsoft Office defaults (default chart styles, default fonts, default bullet markers). Override every default.

---

## What changes from the previous deck spec

| v1 (old) | v2 (current) |
|---|---|
| Substrate appears at slide 13 | Substrate-as-shadow at slide 4 → explicit at slide 6 → multi-atlas at slide 13 |
| 4 acts | 5 acts |
| Autism = identity | Autism = proof-of-concept |
| Slide 13 was "multi-atlas substrate" | Slide 6 is the substrate-transition slide; slide 13 is multi-atlas elaboration |
| "We built a better autism framework" | "Open substrate for condition-specific causal inference atlases" |
| Targeting autism funders | Targeting federal scientific-infrastructure funders |

The category jump from "autism analytics" to "scientific operating system for subgroup inference" is the single most important strategic move in this deck. Everything is structured around making that jump as efficient as possible.

---

*Author: Greg [LAST]. License: MIT. Citation DOI: pending Zenodo deposit. Last updated: 2026-05-08.*
