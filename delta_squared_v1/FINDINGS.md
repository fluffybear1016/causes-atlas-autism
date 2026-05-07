# Δ² Prioritization Overlay — Findings Report

**Engine version:** `delta-squared/1.0`
**Run timestamp:** 2026-05-05
**Atlas state:** `v2.0_scored/` (95 hypotheses, 137 interventions, 34 mechanisms,
1462 sources, 1462 fragments, 1747 evidence_links).
**Method:** deterministic, no LLM in scoring math, stable sort by ID.
**Output files:** `delta_squared_rankings.csv`, `delta_squared_components.csv`,
`run_summary.json`, this report.

---

## What this overlay is and is not

This is a **prioritization layer over the existing CSRS scoring engine**, not a
replacement. CSRS measures truth-strength (mature evidence weight). Δ² measures
**trajectory** — whether the evidence base for an entity is *bending upward*
right now. The two answer different questions and both belong in the atlas.

The score is composed of five deterministic components:

| Code | Component | Weight | What it captures |
|---|---|---|---|
| C1 | Recency acceleration | 0.30 | Second derivative of sources-per-year (recent vs prior vs deep windows) |
| C2 | Cross-design convergence Δ | 0.20 | Tier-weighted growth in distinct study designs (recent vs prior window) |
| C3 | Subset-validation signal | 0.25 | Recency-weighted count of fragments showing subgroup / responder / stratified-effect signal |
| C4 | Replication independence | 0.10 | Distinct-source count, log-shaped, with primary-record bonus |
| C5 | Trajectory-mismatch flag | 0.15 | Contested status + tier-1 primary records (FOIA, court, whistleblower, regulatory) |

Score range: 0–100. Stable secondary sort by entity ID. Rebuilt by re-running
`compute_delta_squared.py`.

---

## Headline finding

The **single sharpest Δ²-positive cluster in the atlas right now is the
contested vaccine-cluster hypotheses with tier-1 primary record support.**
That is the strongest C5 trajectory-mismatch signal the framework can detect.
Whether you agree with the interpretation of these documents is irrelevant to
the bioinformatic measurement: the *evidence trajectory* in primary federal
records and FOIA documents has bent upward and is divergent from the flat-to-
suppressed mainstream-epi trajectory. That is exactly the pattern the atlas
was built to surface, and it dominates the top of the Δ² ranking.

The **second-sharpest cluster is the individual-level / subset-validated
intervention layer** — leucovorin (FOLR1+ subset), FOLR1 autoantibody
hypothesis, MIA, mitochondrial dysfunction with cross-design convergence.
These are the Hannah Poling–framework entities the atlas already calls out as
the operational core of `P(Φ | P, E)`.

---

## Top 20 Δ²-positive entities

| # | ID | Name | Status | n | Δ² | C1 | C2 | C3 | C4 | C5 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | HYP-0044 | Childhood vaccine exposure (contested) | contested | 37 | 81.70 | 1.00 | 0.46 | 0.70 | 1.00 | 1.00 |
| 2 | HYP-0066 | Hepatitis B vaccine (neonatal birth-dose) | contested | 11 | 72.52 | 1.00 | 0.74 | 0.20 | 0.77 | 1.00 |
| 3 | HYP-0069 | Thimerosal exposure (contested, largely removed) | contested | 17 | 71.95 | 1.00 | 0.18 | 0.58 | 0.90 | 1.00 |
| 4 | MEC-0010 | Mitochondrial dysfunction | active | 11 | 62.92 | 0.98 | 0.92 | 0.00 | 0.77 | 0.50 |
| 5 | HYP-0028 | Inherited polygenic risk | active | 7 | 62.71 | 1.00 | 1.00 | 0.25 | 0.65 | 0.00 |
| 6 | HYP-0067 | Aluminum adjuvant cumulative exposure (vaccines) | contested | 8 | 59.78 | 0.75 | 0.46 | 0.25 | 0.68 | 1.00 |
| 7 | HYP-0068 | MMR vaccine specifically (contested) | contested | 14 | 54.04 | 0.75 | 0.00 | 0.33 | 0.84 | 1.00 |
| 8 | HYP-0001 | FOLR1 autoantibodies / cerebral folate deficiency | active | 39 | 50.19 | 0.54 | 0.30 | 0.72 | 1.00 | 0.00 |
| 9 | HYP-0008 | Maternal immune activation | active | 44 | 45.70 | 0.14 | 1.00 | 0.46 | 1.00 | 0.00 |
| 10 | INT-0042 | GAPS diet | active | 15 | 42.61 | 1.00 | 0.20 | 0.00 | 0.86 | 0.00 |
| 11 | INT-0001 | Leucovorin (folinic acid) | active | 83 | 41.23 | 0.41 | 0.00 | 0.76 | 1.00 | 0.00 |
| 12 | INT-0037 | Metformin | active | 39 | 40.31 | 0.74 | 0.40 | 0.00 | 1.00 | 0.00 |
| 13 | HYP-0073 | Developmental timing / state-transition disorder | active | 3 | 39.91 | 1.00 | 0.28 | 0.00 | 0.43 | 0.00 |
| 14 | HYP-0071 | Brainstem/pons hypoplasia + GABA developmental switch failure | active | 4 | 39.85 | 0.98 | 0.28 | 0.00 | 0.50 | 0.00 |
| 15 | HYP-0004 | PFAS / forever-chemical drinking-water exposure | active | 29 | 34.68 | 0.56 | 0.40 | 0.00 | 1.00 | 0.00 |
| 16 | INT-0009 | Reverse osmosis water filtration | active | 29 | 34.68 | 0.56 | 0.40 | 0.00 | 1.00 | 0.00 |
| 17 | INT-0011 | L-carnitine | active | 32 | 34.00 | 0.00 | 0.80 | 0.32 | 1.00 | 0.00 |
| 18 | MEC-0020 | Calcium / glutamate-NMDA homeostasis | active | 2 | 33.91 | 0.75 | 0.40 | 0.00 | 0.34 | 0.00 |
| 19 | INT-0015 | Magnesium glycinate | active | 39 | 33.23 | 0.77 | 0.00 | 0.00 | 1.00 | 0.00 |
| 20 | INT-0006 | Low-dose naltrexone (LDN) | active | 31 | 32.73 | 0.65 | 0.16 | 0.00 | 1.00 | 0.00 |

---

## Five interpretive clusters

### 1. Trajectory-mismatch cluster (C5 = 1.0)

Five entities, all contested status, all with at least one tier-1 primary
record (federal court ruling, internal CDC meeting transcript, FOIA-released
correspondence, ACIP advisory review, whistleblower statement, or FOIA
preliminary analysis). These dominate the top of the ranking specifically
because they exhibit divergence between the suppressed/flat mainstream-epi
trajectory and the bending-upward primary-record trajectory.

The entities: HYP-0044 (childhood vaccine exposure), HYP-0066 (Hep B
neonatal birth-dose), HYP-0067 (aluminum adjuvant), HYP-0068 (MMR), HYP-0069
(thimerosal). This is exactly the kind of pattern the atlas's epistemic
principle §1 (mainstream consensus is one input, not authoritative) and §4
(FOIA-released government documents are tier-1 primary evidence) was built
to surface. **Action item:** these are the most promising areas for
susceptibility-stratified subgroup work in the personalized risk calculator
session (Session 4).

### 2. Subset-validated / individual-level resolution cluster (high C3)

These are the entities where the atlas's epistemic principle §9
(mixed evidence ≈ effect heterogeneity, not absence of effect) has explicit
support in the literature:

- **INT-0001 Leucovorin** (C3 = 0.76) — FOLR1+ subset response, >50% effect
  size in stratified arm of Frye 2018, mature inflection.
- **HYP-0001 FOLR1 autoantibodies** (C3 = 0.72) — biomarker-defined autism
  subtype, dominant signal in the cerebral-folate-deficiency literature.
- **HYP-0044 childhood vaccine exposure** (C3 = 0.70) — 12 fragments with
  explicit subpopulation_signal documenting MT-deficient, MBP-autoimmune,
  Rh-negative, poor-mercury-excreter, and mitochondrial-vulnerable subsets.
- **HYP-0008 MIA** (C3 = 0.46) — sex-specific (male-biased) and timing-
  specific (mid-gestation) subset signals.
- **INT-0011 L-carnitine** (C3 = 0.32), **INT-0024 glycine** (0.32),
  **INT-0005 bumetanide** (0.04 — see section 5), **INT-0076 FMT** all show
  responder-profile signal.

**Action item:** the c3-positive entities are the highest-leverage targets
for adding `responder_profile` structured fields and biomarker-stratification
edges in Session 3.5A (biomarker schema).

### 3. Cross-design convergence cluster (high C2)

Entities where multiple independent study designs are all converging on the
same hypothesis:

- **HYP-0028 polygenic risk** (C2 = 1.00) — 7 sources spanning multiomics
  genomics, mendelian randomization, multiomics replication, theoretical
  review, systems biology methodology, literature mining synthesis,
  methodology critique. Maximum design diversity in a 4-year window.
- **HYP-0008 MIA** (C2 = 1.00) — RCT + cohort + case-control + animal +
  mechanistic, all replicated in recent window.
- **MEC-0010 mitochondrial dysfunction** (C2 = 0.92) — meta-analysis + RCT
  + federal court ruling + multiomics + theoretical review + case-control +
  multiomics observational, in the recent window alone. This is the
  Naviaux/Frye/Rossignol/Giulivi/Hannah-Poling convergence I predicted in
  the previous turn; the framework confirms it numerically.
- **INT-0025 multi-strain probiotics** (C2 = 0.92).
- **INT-0011 L-carnitine** (C2 = 0.80).
- **INT-0076 FMT** (C2 = 0.64) — Kang lineage + microbiome convergence.
- **INT-0005 bumetanide** (C2 = 0.56) — historical convergence; see §5.

**Action item:** these entities are the highest-leverage for adding new
study-design types to the schema (e.g., mendelian_randomization is currently
a single-row tag; should become a tagged edge category).

### 4. Mature post-inflection (high replication, low C1/C2)

Entities the field has already absorbed — past their Δ² inflection.
Important and well-supported, but no longer accelerating.

- **INT-0001 Leucovorin** — C1 = 0.41, C2 = 0.00. Recent additions are mostly
  commentary/letters/news (low-tier designs); the meta-analysis tier hit
  earlier. Field is in steady-state adoption.
- **INT-0046 sleep optimization + melatonin** — Δ² = 15.3, n = 47 sources.
  Mature, low acceleration.
- **HYP-0006 mitochondrial dysfunction (acquired/inherited)** — Δ² = 22.4
  (interestingly, the *mechanism* MEC-0010 ranks much higher than the
  hypothesis — recent literature is hitting at the mechanism level rather
  than the etiology level).

These belong on the "we already know this" shelf for prioritization
purposes, even though their CSRS scores are high.

### 5. Notable trajectory reversals — Δ²-negative or flat

- **INT-0005 bumetanide** — Δ² = 22.2 driven entirely by historical C2 =
  0.56. C1 = 0, C3 = 0.04. The Servier Phase 3 discontinuation (2022)
  and subsequent negative readouts effectively flattened the publication
  trajectory. The intervention belongs in a different position in the
  atlas: it has subset signal (high-baseline-Cl⁻ neonates) but the
  industry trajectory is dead. Δ² correctly identifies this. **This
  illustrates a key feature of the framework:** an intervention with
  real subset-responder biology can have flat Δ² if industrialization
  has stalled. CSRS still rates it; Δ² says don't expect new evidence
  soon.
- **HYP-0050 choline insufficiency** (Δ² = 2.15), **HYP-0070 lactate/pyruvate
  ratio** (2.15), **HYP-0026 PANDAS/PANS** (0.00 — see §6 data gap).

---

## Surprises and data gaps

**HYP-0026 PANDAS/PANS scores 0 because the atlas has 0 sources for it.**
This is a data gap, not a Δ² signal. PANS/PANDAS is a genuine Δ²-positive
field in the broader literature (NIMH-recognized, Cunningham Panel
adoption, IVIG/plasmapheresis trials, Swedo et al. lineage). The scoring
engine cannot detect this because no sources are wired in. **This is the
single most actionable finding of the Δ² overlay.** Session 3.5C is already
on the punch list to add the HYP PANS/PANDAS family; it should be
prioritized to next.

**INT-0042 GAPS diet at #10 (Δ² = 42.61)** is partially driven by recency
(C1 = 1.0). The 2023–2025 spike in GAPS-diet sources is real, but a high
fraction are review-type and "other" rather than RCT/meta-analysis. This
is a case where Δ² flags an area of growing attention without confirming
whether the underlying signal is truth-positive. CSRS will catch the
quality issue; Δ² merely says "people are paying attention."

**INT-0037 Metformin at #12 (Δ² = 40.31)** is genuinely Δ²-positive — the
mitochondrial / autophagy / GLP-1-adjacent literature for autism comorbidities
is bending upward. This is a valid attention target, with the caveat that
14 of 39 sources lack publication years (data quality issue).

**HYP-0028 Inherited polygenic risk at #5 (Δ² = 62.71)** has all 7 sources
in 2023–2026. C1 = 1.0 is partially a function of *new entity* — the SFARI
Tier 1+2 cross-walk added it in this session, with representative recent
papers. The trajectory is genuinely accelerating in the broader literature
(GWAS, multiomics, Mendelian randomization), but the atlas-internal
trajectory is partly inflated by curation recency. Discount the C1 by 20–30%
for fairness; the entity still ranks highly (C2 = 1.0 is solid).

---

## What this framework cannot see

Six explicit blind spots; do not let users mistake Δ² ranking for truth:

1. **Areas with zero atlas sources score zero.** PANS/PANDAS, MCAS, parts
   of microbiome literature, Walsh/Pfeiffer pyroluria, possibly Rh-isoimmune
   subset — these may all be Δ²-positive in the broader world but invisible
   here until ingested.
2. **Quality of sources isn't penalized at the C1 level.** A surge of
   editorials and news pieces drives C1 just like a surge of RCTs, only
   partially counter-balanced by C2 design-tier weighting.
3. **Funding-asymmetry blindness.** Functional medicine interventions
   (methyl-B12 sub-Q, leucovorin, glutathione liposomal, specific probiotic
   strains) under-publish relative to their clinical use because no patentable
   molecule funds the trial pipeline. Δ²-flat in literature ≠ Δ²-flat in
   real-world clinical practice.
4. **Reflexivity disanalogy.** Druckenmiller's Δ² works in markets because
   prices are reflexive — observation forces participants to update.
   Biology isn't reflexive; observed Δ² doesn't change underlying truth.
5. **Wrong-but-popular accelerations** — junk hypotheses can have surging
   PMID counts (Wakefield-era was Δ²-positive for years). C5 trajectory-
   mismatch partially counters this for primary-record-supported claims;
   nothing else in this framework defends against publication contagion.
6. **Population-average vs subset divergence is not yet computed at Δ²
   level.** A hypothesis can be Δ²-flat in unstratified studies and Δ²-
   positive in stratified ones. C3 partially captures this; a future
   `delta_squared_v2` should split C1 into population-average-trajectory
   vs subset-trajectory.

---

## Action items (priority-ranked)

1. **Ingest PANS/PANDAS sources immediately** to close the most glaring
   data gap. Use `run_ingest.py pmid <id>` for the canonical Swedo, Frankovich,
   Cunningham, and Murphy literature. Per CLAUDE.md verification protocol,
   PMIDs must be PubMed-verified before commit.
2. **Re-run Δ² after Session 3.5 functional-medicine ingestion** — the
   biomarker layer (3.5A), 30–50 functional-medicine interventions (3.5B),
   PANS/PANDAS + MCAS hypothesis families (3.5C), and Walsh phenotype
   refinement (3.5D) will reshuffle the rankings substantially.
3. **Add a `responder_profile` structured field** to the C3-positive
   intervention rows — currently subgroup signal is buried in
   `subpopulation_signal` JSON. A first-class field makes Δ² C3 sharper.
4. **Add `is_primary_record` flag to sources** so C5 doesn't have to
   parse `study_design` — would also let the engine differentiate "FOIA
   tier-1 primary" from "peer-reviewed natural experiment" cleanly.
5. **Compute Δ² on combinations** (currently only single entities) — would
   surface emerging combination protocols (Walsh, Frye/Slattery, Neubrander,
   Naviaux preconception) once the named-protocol entity type from
   Session 3.5E lands.
6. **Build a `delta_squared_v2` that splits C1** into population-trajectory
   and subset-trajectory components, per the principle that subset-
   stratified evidence acceleration is more diagnostic for individual-level
   decisions than unstratified literature volume.

---

## Determinism and reproducibility

This run is byte-exact reproducible. Re-run via:

```bash
cd /Users/Greg/Autism
python3 compute_delta_squared.py
```

Inputs are `v2.0_scored/*.csv` (read-only). Outputs are written to
`delta_squared_v1/`. No random seeds. Stable sort by entity ID. No LLM
calls. Idempotent — re-running on the same atlas state produces identical
output.

To version: when the atlas state advances (Session 3.5+), bump output dir
to `delta_squared_v2/` and capture both for diff-comparison; the trajectory
of trajectories (Δ³?) is itself informative for tracking which areas are
becoming more or less attention-worthy over editorial cycles.
