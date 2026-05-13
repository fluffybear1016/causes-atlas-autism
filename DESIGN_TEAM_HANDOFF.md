---
title: "Causes Atlas — Design Team Handoff"
audience: external design / UI agent
status: ready
last_updated: 2026-05-09
maintainer: data team (Greg)
---

# Design team handoff

Single entry point for the parallel design agent. Read this first.

This document is intentionally short. It tells you (1) what the product
is, (2) what to design, (3) what's already built (read this before
duplicating work), (4) the non-negotiables, and (5) where to look for
deeper context if you want it.

---

## 1. What it is, in one paragraph

The Causes Atlas is a **provenance-preserving, reproducible substrate
for condition-specific causal inference**. Autism is the proof-of-concept
condition. The substrate ingests primary research at PMID granularity,
maintains typed claims with evidence balance (supporting / opposing /
contested), and emits an individual-level intervention bundle for a given
biomarker + susceptibility profile. The headline validation result is
**n=8 cohort MAE = 0.067; n=7 within-driver-coverage MAE = 0.049, with
4 sub-3-percentage-point errors spanning 3 mechanistically independent
intervention axes (oxidative stress, methylation, GABA-Cl⁻)**.

Calibration anchor INT-0001 Leucovorin holds at **CSRS = 83.35**
(must remain ≥ 80; halts the pipeline if it drifts).

The substrate is positioned as **shared open infrastructure** that
multiple condition atlases plug into — autism today, Long COVID and
others next. Funding pitch is HHS / NIH / academic medical centers /
patient registries / therapeutics programs.

---

## 2. What to design

The product surfaces you should be aware of, in priority order:

### 2.1 HHS deck (15 slides, 5 acts)
Spec lives in `DECK_v2_15_SLIDE_SPEC.md`. Slides 1, 2, 10 are built as
HTML mocks (see §3 below). The remaining 11 slides need design — most
are typography-heavy and can be authored in Keynote with the existing
chrome.

**Act structure:**
- Act I (slides 1–3): Hook + framing. "Mainstream averages mask
  subset signal."
- Act II (slides 4–6): The substrate. Layered architecture with
  provenance + typed claims + evidence balance.
- Act III (slides 7–9): The autism proof-of-concept. n=8 cohort, 295
  nodes, 81 typed combinations.
- Act IV (slides 10–12): Validation + replication. The MAE figure,
  the 3-axis structural replication argument, anti-reflexivity audit.
- Act V (slides 13–15): Roadmap + ask. Long COVID next; institutional
  partnership.

### 2.2 Atlas explorer (live web surface)
Obsidian-style force-directed graph of all 295 nodes. View-mode toggle
(Parent / Research / Atlas), adaptive label reveal, neighborhood
isolation on hover. Already built at `ui/components/atlas_explorer.py`
+ `atlas_explorer_preview.html`.

If you redesign: keep the three view modes; keep neighborhood isolation;
keep adaptive labels. Don't add modes — keep the surface legible.

### 2.3 Parent-facing UI (`ui/simple.py`)
Streamlit app. Single-page step-machine that asks for biomarkers +
susceptibility profile and returns a four-card answer:
"WHERE IT COMES FROM / WHAT TO DO / WHAT TO AVOID / WHAT TO TRACK."
Already shipped. Don't redesign the card framing — it's what the user
explicitly asked for after rejecting the prior version as "not
actionable."

---

## 3. What's already built (don't re-do)

| Surface | Path | Status |
| --- | --- | --- |
| 16:9 substrate diagram | `ui/components/substrate_diagram_slide.html` | done — gravitational L3, institutional minimalism |
| 8.5×11 substrate diagram | `ui/components/substrate_diagram.html` | done — paper variant |
| Slide 1 (cover) | `ui/components/deck/slide_01_cover.html` | done |
| Slide 2 (averaging problem) | `ui/components/deck/slide_02_averaging.html` | done |
| Slide 10 (validation scatter) | `ui/components/deck/slide_10_validation.html` | done |
| Slide chrome (CSS) | `ui/components/deck/_slide_chrome.css` | done — typography, color, layout vars |
| Cinematic constellation | `ui/components/constellation_cinematic.py` | done — Hannah Poling chain animation |
| Atlas explorer v2 | `ui/components/atlas_explorer.py` | done — 295 nodes, force-directed |
| Parent UI (Streamlit) | `ui/simple.py` | done — WHERE IT COMES FROM / WHAT TO DO / WHAT TO AVOID / WHAT TO TRACK |
| Free public API | `api/main.py` + `Dockerfile` | done — FastAPI |
| Free atlas OS positioning | `ATLAS_OS_README.md`, `CONTRIBUTING.md` | done |

---

## 4. Non-negotiables (will fail HHS review if violated)

**Language guardrails** (these are not stylistic preferences, they're
positioning; ChatGPT design review flagged each one specifically):

1. **Do not say "deterministic" outside of code-and-pipeline context.**
   Determinism is a property of the build, not a claim about truth.
   Public-facing copy uses: "provenance-preserving," "reproducible
   lineage," "typed claims," "audit-resolvable."
2. **Do not say "no LLMs in scoring math."** Say "no language-model
   calls in the scoring path." (Same thing, less in-group.)
3. **Do not pitch the atlas as autism analytics.** The pitch is
   substrate. Autism is one condition; Long COVID is in the queue. The
   slide deck framing is "shared infrastructure," not "we figured out
   autism."
4. **Mainstream consensus is one input, not authoritative.** Don't
   visually privilege it. Evidence balance (supporting / opposing /
   contested) is shown side-by-side with weight, not stacked.
5. **Hannah Poling framework is the central organizing principle.**
   `causation = susceptibility (P) × trigger (E) → mechanism (M) → phenotype (Φ)`.
   This is the chain animation in `constellation_cinematic.py`. Don't
   simplify it away.

**Visual guardrails:**

6. **Aesthetic reference: Palantir × CERN × Arc Institute.** Defense-
   grade institutional minimalism. Not "consumer wellness app."
7. **No emojis.** Anywhere. Including the deck. Including button
   labels. (User said this explicitly in the prior session.)
8. **No L6 "aspirational logo cloud" sprawl.** The institutional
   adoption layer in the substrate diagram shows exactly five
   institutions: HHS · NIH · Academic Medical Centers · Patient
   Registries · Therapeutics Programs.

**Numerical claims** (each was independently re-derived and verified
against `cohort.yaml` + the engine output):

9. **n=8 cohort MAE = 0.0665.** Round to 0.067 in copy.
10. **n=7 within-driver-coverage MAE = 0.049.** Not 0.052 — that was
    an earlier arithmetic error; do not reintroduce it.
11. **4 sub-3-percentage-point errors spanning 3 mechanism axes,**
    not 4. Hardan NAC and Singh sulforaphane are both upstream of
    glutathione regeneration; counting them as separate axes was
    overstating.
12. **INT-0001 Leucovorin CSRS = 83.35.** Calibration anchor; cited as
    proof the scoring path doesn't drift across changes.

---

## 5. Where to look for deeper context

If you have specific questions, the source docs are:

- **`CHATGPT_DESIGN_BRIEF.md`** — the brief I sent to ChatGPT for
  collaborative design review. Most useful single document.
- **`DECK_v2_15_SLIDE_SPEC.md`** — slide-by-slide spec.
- **`SUBSTRATE_THESIS.md`** — the long-form substrate framing.
- **`VAULT_INSTITUTIONAL.md`** — the federally-safe translation of the
  atlas mission (used for HHS / NIH framing).
- **`validation/responder_rate_calibration/VALIDATION_RESULTS.md`** —
  the cohort table + MAE breakdown.
- **`MASTER_README.md`** — the engineering README.
- **`CLAUDE.md`** — the project-level operating instructions for AI
  collaborators (you are one). Worth skimming for the epistemic
  principles + verification protocol.

---

## 6. Integrity status at handoff

Pre-handoff audit (`scripts/pre_handoff_audit.py`) ran 2026-05-09 with:

- **0** CRIT / HIGH / MED findings.
- **12** LOW findings (all informational: combination descriptions
  mention ingredients like 'rutin' or 'colostrum' that are not
  promoted to canonical INT entries; not a design concern).
- **9** OK checks (calibration anchor, cohort MAE, combo orphan
  resolution, CSV schema, peptide-vault links, three script smoke
  tests, vault hygiene).

Regenerate at any time with:

```bash
cd /Users/Greg/Autism
python3 scripts/pre_handoff_audit.py
# writes AUDIT_2026_05_09.md
```

If you want to verify the validation numbers yourself:

```bash
python3 scripts/validate_v02_calibration.py
# expect: 4 cases · 4 pass · 0 fail
python3 scripts/compute_responder_mae.py
# expect: Cohort responder-rate MAE: 0.0665 (n=8)
```

---

## 7. First five minutes (quickstart)

```bash
# 1. clone
git clone https://github.com/fluffybear1016/causes-atlas-autism.git
cd causes-atlas-autism

# 2. read these four files in order (15 min total)
open DESIGN_TEAM_HANDOFF.md       # this doc
open DECK_v2_15_SLIDE_SPEC.md     # slide-by-slide content for all 15
open SUBSTRATE_THESIS.md          # the long-form pitch
open CHATGPT_DESIGN_BRIEF.md      # the design-review brief

# 3. open the existing visual artifacts in a browser
open ui/components/substrate_diagram_slide.html
open ui/components/deck/slide_01_cover.html
open ui/components/deck/slide_02_averaging.html
open ui/components/deck/slide_10_validation.html
open ui/components/atlas_explorer_preview.html
open ui/components/constellation_cinematic_preview.html

# 4. run the parent UI locally (optional)
pip install streamlit pyyaml
streamlit run ui/simple.py

# 5. verify nothing has drifted since handoff
python3 scripts/pre_handoff_audit.py
# expect: 0 CRIT / 0 HIGH / 0 MED / 12 LOW / 9 OK
```

## 8. Scope of the design engagement (proposed)

In priority order. Push back if priorities should swap.

**P0 — must ship for HHS deck:**
- Slide 6 (the substrate / cathedral slide) — design treatment on top
  of `ui/components/substrate_diagram_slide.html`. This is the
  single most important slide. Spec §`Slide 6 — The cathedral slide`
  in `DECK_v2_15_SLIDE_SPEC.md` is unusually specific because the
  emotional beat matters more than the data.
- Slides 3, 4, 5 (Hannah Poling framework / new substrate required /
  determinism) — typography-heavy, share chrome with slides 1, 2.
- Slides 7, 8, 9 (autism atlas + knowledge graph + formulation-aware
  evidence) — slide 8 needs a high-res screenshot of the atlas
  explorer at a state showing contested edges.
- Slides 11, 12 (contested-evidence preservation + autonomous
  discovery) — typography-heavy.
- Slides 13, 14, 15 (multi-atlas / open source / asks) — typography-
  heavy closeout.

**P1 — for the live web surface:**
- Atlas explorer color encoding review (11 hues vs. 5-6 superclasses;
  see §7 question 3).
- Parent UI step-machine: trim from 6 steps if possible (§7 question 4).

**P2 — nice-to-have:**
- High-res PDF export of the substrate diagram for printing.
- Animated transitions in the constellation cinematic component.

## 10. Open questions for the design team

The data team would like opinions on:

1. **Deck typography.** Current chrome uses a stark serif headline +
   monospace data label. Is this the right register for HHS, or should
   the headline lean sans?
2. **Slide 10 scatter plot.** Currently rendered with d3. Should we
   move to a static PNG / vector for print fidelity, or keep it live
   so the cohort can grow without rebuilding the deck?
3. **Atlas explorer color encoding.** Mechanism class is encoded by
   hue (currently 11 distinct hues). Is 11 too many? Should mechanism
   classes collapse to 5-6 superclasses for first-look legibility?
4. **Parent UI step-machine length.** Currently 6 steps. Some test
   parents found it long. Are there steps we can fold or defer?

Direct your answers / mocks back to Greg via the cowork session, or
drop them into `ui/components/deck/` and `ui/simple.py` as PRs.

---

*Generated 2026-05-09 after pre-handoff audit reached 0 HIGH / 0 MED.*
*Calibration: INT-0001 = 83.35 · Cohort MAE = 0.0665 · 295 atlas nodes.*
