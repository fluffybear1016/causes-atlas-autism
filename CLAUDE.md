# Causes Atlas (Autism) — Working Folder Context

## What this folder is

This is the working directory for the **Causes Atlas (Autism)** — an
evidence-driven knowledge graph mapping every known and speculated cause,
mechanism, phenotype, gene, intervention, and combination relevant to
autism, with a deterministic scoring engine.

The mission, per spec §0: map causation, correlation, prevention, and
treatment; cross-pollinate evidence; preserve uncertainty and contradiction;
strict Layer 1 (causal graph) vs Layer 2 (decision/CSRS) separation;
no LLMs in scoring; calibration anchor leucovorin INT-0001 must score ≥80.

## Mission framing — individual-level, not population-level

**The atlas serves individual / family clinical decisions, not population
policy.** Mainstream public-health calculations optimize for
population-average risk-benefit; the atlas optimizes for "what's right for
THIS specific child given THIS specific susceptibility profile."

This is the **Hannah Poling framework** — the atlas's central organizing
principle for causation:

  causation = susceptibility (P) × trigger (E) → mechanism (M) → phenotype (Φ)

For any specific child, the conditional risk `P(Φ | P, E)` matters more
than the population-average risk `P(Φ | E)`. A vaccine, infection,
medication, or environmental exposure that has minor population-average
risk can be catastrophic for a child with the relevant susceptibility
(genetic, mitochondrial, autoimmune, methylation, etc.).

The federally-adjudicated **Hannah Poling case (2008)** establishes this
formally: vaccine challenge "significantly aggravated an underlying
mitochondrial disorder, which predisposed her to deficits in cellular
energy metabolism, and manifested as a regressive encephalopathy with
features of autism spectrum disorder." n=1 binding legal finding,
mechanism recognized, principle applies broadly.

The end-state goal of the atlas is a **personalized risk calculator**:
given parental genetic testing + maternal biomarker panel + paternal
profile, output conditional probabilities across the 7 autism phenotypes
plus a ranked intervention/avoidance bundle for that specific family.

## Epistemic principles

These govern how evidence is weighed across the atlas:

1. **Mainstream consensus is one input, not authoritative.** Public health
   guidance, regulatory positions, and major-medical-society consensus are
   recorded as evidence but not given automatic high weight. They are
   subject to industry funding distortion, regulatory capture, liability
   protection asymmetries (e.g., 1986 Vaccine Injury Act removing legal
   accountability from vaccine manufacturers), and population-level
   averaging that obscures individual-level harm.

2. **Primary documents > secondary literature > opinion.** Source-quality
   hierarchy is enforced by the scoring engine's `W_DESIGN` and
   `W_SOURCE_TYPE` weights:

   | Tier | Examples | W_DESIGN range |
   |---|---|---|
   | Highest | meta_analysis, RCT, natural_experiment | 0.85–1.00 |
   | High | cohort, court_ruling, case_control | 0.40–0.75 |
   | Mid | review, case_series, mechanistic | 0.30–0.55 |
   | Low | preliminary_analysis, internal_correspondence, advisory_review | 0.20–0.30 |
   | Very low | editorial, letter, comment, in_vitro | 0.10–0.25 |
   | Bottom | news, factcheck_review, advocacy | 0.05 |

3. **Industry-funded research, fact-check journalism, and advocacy
   content are explicitly down-weighted.** Annenberg/FactCheck.org,
   Children's Health Defense advocacy framing, pharma-funded studies
   without independent replication, and similar non-primary sources are
   tagged and tier-5 weighted. They are **not erased** — the atlas
   preserves contested evidence per spec §0/§1.1 — but they don't get
   equal voice with primary federal records or peer-reviewed RCTs.

4. **FOIA-released government documents are tier-1 primary evidence**
   regardless of mainstream consensus on their interpretation.
   Generation Zero (1999), Simpsonwood transcript (2000), Verstraeten
   internal emails, William Thompson 2014 documents, Hannah Poling
   federal court ruling, ACIP meeting transcripts — these are recorded
   at high weight because they are unfiltered ground-zero records of
   how scientists / regulators / federal courts actually reasoned.

5. **Contested status is permanent.** Vaccines, aluminum adjuvants,
   thimerosal, hepatitis B birth-dose, glyphosate, etc. remain
   `status: contested` regardless of which direction the published
   epidemiology tilts. This is not "being neutral" — it's recognizing
   that the published epidemiology has known methodological limits
   (population averaging, lack of true-control unvaccinated cohorts in
   many cases, retrospective design, funding asymmetries) that don't
   resolve the underlying question for an individual susceptible child.

6. **Methodological power matters — but population-average studies don't
   settle individual-level questions.** A study's strength depends on
   what question it answers. A 1.2M-person nationwide cohort
   (Andersson 2025 Danish) has high statistical power for the
   *population-average* effect of an exposure but can completely mask
   significant effects in genetically or metabolically susceptible
   subgroups (the "averaging problem" / effect-heterogeneity dilution).
   For the atlas's stated mission — individual-level health decisions —
   large-cohort null findings do **not** automatically refute subgroup-
   specific signals. The Hannah Poling framework formalizes this:
   population-average risk `P(Φ|E)` and conditional risk `P(Φ|P,E)` are
   different quantities answered by different study designs. A 1% high-
   risk subgroup contributing a real effect can be statistically
   invisible in a study of average effects across the whole population.

7. **Subgroup analysis and effect-heterogeneity reporting are
   independently valuable.** Studies that examine "do certain genetic,
   metabolic, or susceptibility subgroups respond differently?" carry
   weight beyond their nominal sample size for individual-level
   decisions. Conversely, large population-average studies that don't
   report subgroup analyses are *less* informative for individual
   questions than their sample size suggests. Examples:
   - **Honda 2005 Japan MMR withdrawal** — natural experiment design
     compares defined birth cohorts before/after withdrawal at
     population scale; methodologically elegant for population-average
     question but still doesn't address mitochondrial-vulnerable subset.
   - **Hannah Poling 2008 federal ruling** — n=1 but explicitly
     identifies the susceptibility-trigger-mechanism-phenotype chain
     for the vulnerable subgroup, complementary to (not refuted by)
     Andersson-style null at population level.
   - **Frye 2018 leucovorin RCT** — small (n=48) but stratified by FOLR1
     autoantibody status, explicitly captured a 50%+ effect size in the
     positive-antibody subgroup that would have been diluted in any
     unstratified larger study.

   The atlas should therefore weight studies by **what question they
   answer** as well as by raw N. A small RCT with rigorous subgroup
   stratification can be more informative for individual-level decisions
   than a million-person cohort that only reports the average.

8. **Replication across study designs matters more than replication of
   the same design.** Cross-design convergence (e.g., RCT + cohort +
   natural experiment + mechanistic study all pointing the same
   direction) is much stronger evidence than five cohorts all using
   the same registry-linkage approach with the same population-average
   blind spots.

9. **Mixed published evidence is almost always effect heterogeneity,
   not absence of effect.** When the literature shows "some studies
   positive, some null" for an intervention or exposure, the
   bioinformatically-correct interpretation is rarely "no effect" —
   it's "effect in a subset, dilution in unstratified population
   studies." Investigative method: for every mixed-results entity,
   examine (a) study population characteristics (age, sex, baseline
   biomarkers, phenotype distribution), (b) intervention dose/duration
   variation, (c) outcome measure differences, (d) inclusion/exclusion
   criteria. Extract the responder profile and tag the intervention
   with its responder phenotype. Worked examples that this principle
   correctly explains:
   - **HBOT (hyperbaric oxygen)** — Rossignol work documents that pre-
     treatment mitochondrial / oxidative-stress markers predict
     response; mito-vulnerable subset responds, others don't.
   - **Bumetanide** — high-baseline-intracellular-chloride neonates
     respond; the rest don't. Explains Phase 3 mixed results.
   - **Folate megadosing / leucovorin** — FOLR1-autoantibody-positive
     subset responds dramatically; FOLR1-negative subset shows
     baseline or no response.
   - **GFCF diet** — zonulin-elevated / GI-symptomatic subset
     responds; non-GI-phenotype subset doesn't.
   - **IVIG** — works in PANS/PANDAS subset; null in unselected
     autism cohorts.
   - **Ketamine / NMDA modulators** — E:I-imbalanced subset responds.
   - **Hep B birth-dose autism risk** — population-average null;
     mitochondrial-vulnerability subset (Hannah Poling) demonstrably
     non-zero.

   The atlas tags each intervention/exposure with its known responder-
   phenotype profile. Contested-status entities get explicit
   responder-population analysis, not blanket null framing. Mainstream
   epidemiology that doesn't stratify by susceptibility tier is — by
   construction — incapable of refuting the responder-subset signal.

10. **Functional medicine operationalizes individual-level resolution.**
    The functional medicine framework (MAPS / Frye / Walsh / Klinghardt /
    ARI lineages) for autism — biomarker workup → phenotype stratification
    → individualized intervention bundles → biomarker re-testing → iterate
    — is the practical clinical implementation of `P(Φ|P,E)`. Mainstream
    pediatric medicine gives population-average interventions (often
    behavioral); functional medicine gives subset-targeted interventions
    based on each child's measured biology. Per atlas mission, this
    framework is treated as the operationalized form of the Hannah Poling
    individual-level resolution principle. High-evidence functional
    medicine claims (leucovorin for FOLR1+ subset, methyl-B12 for low-SAM
    subset, mito cocktails for mito-vulnerable subset, LDN for inflamed
    subset, mast cell stabilization for MCAS subset, antibiotics for PANS
    subset) get strong representation. Lower-evidence functional medicine
    claims are recorded with appropriate weight but **not dismissed for
    being non-mainstream** — much of functional medicine simply hasn't
    had population-average RCTs because of funding asymmetries (no patent
    on glutathione), not because the underlying biology is wrong.
    Mainstream evidence is mid at best for autism; functional medicine
    is more efficient because it stratifies before treating.

11. **Determinism is non-negotiable.** No LLMs in scoring math. No random
    seeds. Stable sort by ID. Idempotent ingestion via `node_aliases`.
    The atlas must produce identical output from identical input every
    time, including across major revisions of the underlying CSVs.

## Architecture

**Two-layer model:**
- **Layer 1 (causal graph):** hypotheses, mechanisms, phenotypes, genes,
  sources, evidence_fragments, evidence_links, and the edge tables linking
  them. Records what the literature claims about how autism arises.
- **Layer 2 (decision/CSRS):** interventions, combinations, scored with the
  Composite Suffering-Reduction Score (CSRS, 0–100). Records what to *do*
  about it. Pulls signal from Layer 1 deterministically.

**Calibration anchor:** INT-0001 Leucovorin must score ≥ 80. Current value:
**83.35**. Calibration history: 82.72 (v1.0) → 81.95 (v2.0) →
83.65 (v2.0.1 with derived intervention→phenotype edges + orphan wiring +
gene layer densification) → 83.35 (v2.0.1 final, after editorial
down-weighting).

## Canonical state (current, post-Session 2026-04-28)

`v2.0_scored/` is the authoritative current state. 22 CSVs, fully scored.

Counts: 70 hypotheses, 33 mechanisms, 99 interventions, 5 combinations,
7 phenotypes, 1564 genes (50% wired to graph as of this session, 49%
still floating pending Tier 3 + no-SFARI triage), 1420 sources, 1420
evidence_fragments, 1647 evidence_links, 33 hypothesis-hypothesis edges.

Edge table state:
| Table | Rows | Note |
|---|---|---|
| hypothesis_mechanism_edges | 117 | densified from 111 via orphan wiring |
| intervention_hypothesis_edges | 96 | unchanged |
| intervention_mechanism_edges | 164 | densified from 151 |
| intervention_phenotype_edges | 145 | was 0; 144 derived via int→mec→phe walk + 1 candidate |
| intervention_gene_edges | 9 | low; needs work |
| mechanism_phenotype_edges | 37 | weights populated 0.31–0.79 (post-scoring derivation applied 2026-04-29; bug resolved) |
| gene_hypothesis_edges | 796 | densified from 15 via SFARI Tier 1+2 cross-walk |
| gene_mechanism_edges | 38 | densified from 22 |
| gene_phenotype_edges | 13 | densified from 9 |
| hypothesis_hypothesis_edges | 33 | sparse; 4830 possible |
| combination_members | 23 | fixed pre-existing data integrity issues |
| evidence_links | 1647 | grew from 1633 |

**Do not edit `v2.0_scored/` files by hand.** Re-run the scoring pipeline.

Backups: `v2.0_scored.before_v201/` (pre-merge), `v2.0_scored.before_gene_layer/`
(pre-gene-densification).

## Versioned snapshots

`output/` and `scored_output/` = v1.0 baseline. `v1.2_expanded/`, then
`v1.2_scored/` through `v1.9_scored/` = the audit trail of every
expansion. Each pair (`vX.Y_expanded/` is the schema-extended state,
`vX.Y_scored/` is after the scoring pass).

`v2.0.1_expanded/` = inputs (v2.0_scored + merged proposals).
`v2.0.1_scored/` = current scored output snapshot.
`v2.0.1_proposed/` = proposal CSVs + audit reports for review.

## Scripts

**Core pipeline:**
- `run_migration.py` — original xlsx → 21-CSV normalization (one-time)
- `run_scoring_v20.py` — v2.0 scoring engine (current canonical)
- `run_ingest.py` — paper ingestion pipeline. Subcommands: `pmid <id>`,
  `url <url>`, `paste`. Idempotent via `node_aliases`.
- `run_expansion*.py` — v1.2 through v2.0 schema/data expansions
- `build_vault.py` — converts canonical CSVs → Obsidian markdown vault

**Audit + expansion (this session):**
- `audit_connectivity.py` — graph connectivity audit, writes to vault
- `propose_mappings.py` — generates Phase A merge candidates (transitive +
  curated) for orphan wiring
- `verify_citations.py` — verifies PMIDs against PubMed esearch+esummary
- `patch_needs_review.py` — broader-query fallback for citation verification
- `regenerate_proposal.py` — rebuilds MAPPING_PROPOSAL.md from verified CSV
- `apply_patches_and_score.py` — end-to-end merge + score + vault rebuild
- `densify_gene_layer.py` — SFARI Tier 1+2 → HYP-0028 + curated gene→mec/phe
- `merge_gene_layer.py` — gene-layer merge + score + verify calibration
- `add_generation_zero.py` — Generation Zero CDC FOIA + initial fact-check
  sources (fact-checks subsequently removed)
- `clean_sources.py` — removed fact-check secondary literature
- `add_phase_a_documents.py` — 5 FOIA / federal-record primary documents
- `add_honda_2005.py` — Honda 2005 Japan MMR-withdrawal natural experiment
- `audit_and_downweight.py` — reclassified 27 PubMed editorials/letters/
  comments; patched W_DESIGN + W_SOURCE_TYPE in scoring engine

**Drive sync:**
- `sync_to_drive.sh` — historical helper

## Specs

Read in order:
1. `MASTER_README.md` — single entry point, calibration history
2. `CAUSES_ATLAS_AUTISM_SPEC.md` (v1.0)
3. `CAUSES_ATLAS_AUTISM_SPEC_v1.1.md`
4. `CAUSES_ATLAS_AUTISM_SPEC_v1.2.md` — current canonical spec, includes
   §5.7 hypothesis_hypothesis_edges, §7.2.1 dual scoring, §14 ingestion
5. `MIGRATION_PLAN.md` and `MIGRATION_IMPLEMENTATION.md`
6. `SCORING_ENGINE_SPEC.md`

## Sync to Google Drive

Drive folder ID: `1E82AlaqZSjxIXKvEX2g2fIyPdEsoMPki`
([Autism in Drive](https://drive.google.com/drive/folders/1E82AlaqZSjxIXKvEX2g2fIyPdEsoMPki))

User has rclone configured. Steady-state sync command (with .DS_Store exclusion):

```bash
cd /Users/Greg/Autism
rclone sync . gdrive:Autism \
  --drive-import-formats csv --drive-export-formats csv \
  --exclude '.DS_Store' --exclude '.DS_Store/**' \
  --progress
```

**Caveat:** the `--drive-import-formats csv` flag uploads CSV files as
native Google Sheets, which can subtly alter formatting (leading zeros,
date strings, very long IDs). For bit-exact backup, drop that flag and
accept that Drive web UI won't preview the CSVs natively.

Re-runs are incremental (only changed files transfer).

## Schema rules (per spec)

- **Contested = permanent valid state.** Vaccines, alum, glyphosate, etc.
  remain `status: contested` regardless of evidence flow direction.
- **Anti-domination caps:** CAP_SOCIAL=0.25, CAP_SINGLE_SOURCE=0.30
- **Polarity coefficient `unknown` = 0.85** (rule-based extracted edges
  carry positive prior)
- **SOFTPLUS_ALPHA = 0.5** for `evidence_quality_index` curve
- **Mechanism strength = MAX of connected hypothesis confidence**
  (not average) — intentional: one strong mechanism connection establishes
  importance.
- **Genetic_support is transitive:** hypothesis → intervention → gene
  walks through `intervention_gene_edges`.
- **Determinism:** stable sort by ID, no random seeds, no LLMs in
  scoring math, idempotent ingestion via `node_aliases`.
- **Source quality enforced:** see Epistemic principles §2 above. Editorial,
  letter, comment, news, factcheck_review, advocacy types weighted
  0.05–0.10. Primary FOIA documents weighted 0.20–0.40 depending on
  document type.

## Recent session highlights (2026-04-27 to 2026-04-28)

**Major additions:**
- 145 derived intervention→phenotype edges (was 0)
- 781 SFARI Tier 1+2 → HYP-0028 polygenic risk edges
- 23 verified candidate orphan-wiring edges (43 PubMed-grounded PMIDs)
- 6 high-value primary documents:
  - SRC-001415 Verstraeten Generation Zero 1999 (FOIA preliminary)
  - SRC-001416 Simpsonwood transcript 2000 (CDC closed meeting, 259pp)
  - SRC-001417 Verstraeten internal emails 1999-2001 (FOIA)
  - SRC-001418 Hannah Poling federal Vaccine Court 2008 (binding ruling)
  - SRC-001419 William Thompson 2014 statement + documents (whistleblower)
  - SRC-001420 ACIP September 2025 Hep B birth-dose review
- SRC-001421 Honda 2005 Japan MMR-withdrawal natural experiment (peer-reviewed)

**Quality cleanup:**
- 27 PubMed editorials/letters/comments/news reclassified from study_design=
  "other" to actual pubtype, automatically down-weighted by patched
  W_DESIGN.
- W_DESIGN + W_SOURCE_TYPE patched with primary-document tiers and
  opinion-content downweights.
- Combination data integrity fixed (3 combos had missing members).

**Verified:**
- Every PMID added in this session was verified via PubMed esearch +
  esummary, with abstract-level review for the 23 candidate edges.
- INT-0001 calibration held throughout (81.95 → 83.65 → 83.35).

## Open expansion threads (priority order)

### Session 1 (immediate finishing)
- **MPE weights: RESOLVED 2026-04-29.** Post-scoring derivation populated
  all 37 mechanism_phenotype_edges with `evidence_strength_aggregate` in
  the 0.31–0.79 range. INT-0001 calibration anchor held at 83.35 (SCH-000108).
- **Update HYP-0066 description** with defensible delay-Hep-B-to-adolescence
  framing for low-transmission-risk families.
- **Add cod liver oil** as an intervention (vitamin D + DHA + vitamin A).
- **Add L-glutamine** as an intervention (completes COM-0003).
- **Drop COVID/flu vaccine references** from prevention messaging.
- **Audit remaining PubMed "other"** by abstract content (the pubtype
  filter caught 27; content-level review will catch more).
- **Cleanup `v2.0.1_proposed/`** intermediate files.

### Session 3.5 — Functional medicine layer expansion (NEXT, prioritized)

**3.5A — Biomarker schema + ingest 40-50 high-evidence biomarkers.**
Schema design first: new top-level entity type for measurable biomarkers
(or extension of existing schema). Each biomarker entry: name, sample
type (urine/blood/stool/hair), reference range, what mechanism it
indicates, what intervention modifies it, what phenotype it stratifies.
Then ingest: organic acids panel (OAT — arabinose, HPHPA, 4-cresol, etc.),
methylation panel (SAM/SAH, homocysteine, MMA, RBC folate), mito panel
(lactate, pyruvate, L:P ratio, acylcarnitine, CoQ10), oxidative stress
markers (GSH/GSSG, 8-OHdG, F2-isoprostanes), immune markers (Cunningham
Panel, tryptase, methylhistamine, cytokines), hormonal markers (full
thyroid, DUTCH cortisol+sex hormones, vasopressin). Each PMID-grounded.

**3.5B — Functional medicine intervention expansion (~30-50 entities).**
LDN, IVIG, cromolyn sodium, ketotifen, methyl-B12 sub-cutaneous protocols
(Frye/Neubrander), PQQ, MitoQ, NAD precursors (NMN, NR), creatine/D-ribose
at therapeutic doses, specific probiotic strains (B. infantis, L. reuteri
DSM 17938, L. plantarum LP-W74, B. longum 1714), antimicrobial protocols
(oregano, berberine, biofilm disruptors), antifungal rotations (nystatin,
caprylic, undecylenic), binding agents (chlorella, modified citrus
pectin, bentonite, charcoal), liposomal glutathione, sauna protocols
(infrared specifically), DMSA / EDTA chelation (mark contested).

**3.5C — Two new hypothesis families.**
**HYP PANS/PANDAS** — Pediatric Acute-onset Neuropsychiatric Syndrome /
Pediatric Autoimmune Neuropsychiatric Disorders Associated with
Streptococcus. Cunningham Panel diagnostic. Treatment: antibiotics,
NSAIDs, IVIG, plasmapheresis, LDN. Real, well-defined autoimmune subset.
**HYP MCAS** — Mast Cell Activation Syndrome. Tryptase + methylhistamine
+ chromogranin A diagnostic. Treatment: H1+H2 antihistamines, cromolyn,
ketotifen, low-histamine diet, quercetin. Increasingly recognized in
autism.

**3.5D — Walsh/Pfeiffer phenotype refinement.**
Add as phenotype subdivisions or new phenotypes:
- Undermethylator phenotype (low SAM/SAH, characteristic personality
  cluster, responds to methyl donors)
- Overmethylator phenotype (opposite; folate cautions)
- Pyroluria / kryptopyrroluria phenotype (high urinary kryptopyrroles,
  B6+zinc+GLA-responsive)
- Copper:zinc imbalance phenotype (Walsh research)

**3.5E — Named protocols / providers as new entity type.**
Walsh Research Institute protocols, Frye/Slattery cerebral folate
protocol, Neubrander methyl-B12 protocol, Bock Plan, Klinghardt protocols,
MAPS framework, ARI (Autism Research Institute), Pfeiffer Treatment
Center. Each linked to its specific test panel, intervention bundle, and
patient-population emphasis.

### Session 3.5 deferred items (after A-E)

- **3.5F Drug repurposing systematic mining** — lovastatin (FXR), amantadine,
  suramin (Naviaux), pioglitazone, minocycline, sulindac, trehalose,
  allopregnanolone, riluzole, acetazolamide, low-dose ivermectin,
  systematic OpenTargets / ClinicalTrials.gov scrape.
- **3.5G Peptide layer** — gluten/casein exorphins, oxytocin/vasopressin
  detail, gut peptides (PYY, GLP-1, ghrelin), AMPs, mito-derived peptides
  (humanin, MOTS-c).
- **3.5H Life-stage mitochondrial protocols** — preconception/pregnancy/
  birth/postnatal/childhood specific mito optimization protocols as
  combinations.
- **3.5I Continuous ingestion pipeline** — wire `run_ingest.py` to PubMed
  RSS feeds for autism + functional medicine query patterns, weekly auto-
  ingest with manual review queue.

### Session 4 (Hannah Poling framework as deliverable, now built on richer atlas)
- **Add `parental_factors.csv` schema** (variant + biomarker + exposure
  dimensions for both parents).
- **Add `gene_variant_to_phenotype_priors.csv`** (per-variant marginal
  risk shifts per phenotype).
- **Add `biomarker_to_mechanism_priors.csv`** (how biomarker thresholds
  map onto mechanism activity — leverages 3.5A biomarker layer).
- **Build `personalized_risk.py`** — takes parental profile JSON, returns
  conditional risk profile + ranked intervention bundle + explicit
  reasoning trace.

### Session 5 — Exhaustive factorial / permutation analysis
What you actually meant by "factorial combinations" — exhaustive
enumeration across the full causal manifold:
- All ~5,000 intervention pairs (the original v2.1 plan)
- Full **susceptibility × trigger × phenotype** conditional risk matrix
  (Hannah Poling at scale: thousands of genetic profiles × dozens of
  triggers × 7 phenotypes)
- All life-stage × intervention × phenotype matchings
- All biomarker → mechanism → intervention chains
- Mechanism-overlap-filtered intervention triples (~5K)
- Build as `run_combinations_v21.py`

### Session 6+ (strategic ongoing)
- **Bayesian credal aggregation upgrade** for the scoring engine — proper
  handling of contested-evidence credal sets rather than point estimates.
- **Mixed-evidence subgroup-extraction analysis** — for every mixed-RCT
  entity in the atlas, automatically identify the responder phenotype
  per principle §9.

## Δ² prioritization overlay (post-2026-05-05)

The Δ² (second-derivative / inflection-point) overlay is a **prioritization
layer over CSRS, not a replacement.** CSRS measures truth-strength
(steady-state evidence weight). Δ² measures *trajectory* — whether the
evidence base for an entity is bending upward right now. Both belong in
the atlas; they answer different questions.

**Architecture:**
- Engine: `scripts/compute_delta_squared.py` (deterministic, no LLM,
  stable sort by ID, sliding year windows computed from `current_year`).
- Outputs: `delta_squared_v1/`
  - `rankings.csv`, `components.csv` — current state, overwritten each run
  - `score_history.csv` — append-only timestamped history
  - `anomaly_flags.csv` — append-only single-source-dominance flags
  - `data_gaps.csv` — defined entities with zero ingested sources
  - `calibration_status.txt`, `run_summary.json` — pipeline-readable
    pass/fail
  - `FINDINGS.md` — interpretive report (manually curated)
- Determinism test: `scripts/test_delta_squared_determinism.py` — runs
  engine twice and asserts byte-identical `rankings.csv` + `components.csv`.
- Pipeline integration: invoked as Step 7 of `apply_patches_and_score.py`.
  Calibration failure halts the pipeline.

**Five components (weights sum to 1.0):**

| Code | Component | Weight | What it captures |
|---|---|---|---|
| C1 | Recency acceleration | 0.30 | Second derivative of sources-per-year |
| C2 | Cross-design convergence Δ | 0.20 | Tier-weighted growth in distinct study designs |
| C3 | Subset-validation | 0.25 | Recency-weighted stratified-effect signal hits |
| C4 | Replication independence | 0.10 | Distinct-source count, log-shaped |
| C5 | Trajectory-mismatch | 0.15 | Contested status + tier-1 primary records |

**Calibration anchors (must hold; regression halts pipeline):**

| Anchor | Check | Threshold | Protects |
|---|---|---|---|
| INT-0001 Leucovorin | score | ≥ 30 | Subset-validation signal for FOLR1+ |
| MEC-0010 Mitochondrial | score | ≥ 50 | Cross-design convergence cluster |
| HYP-0028 Polygenic risk | C2 | ≥ 0.85 | Maximum design diversity in recent window |
| HYP-0001 FOLR1 autoantibodies | C3 | ≥ 0.55 | Stratified-subset signal in literature |
| HYP-0044 / 66 / 67 / 68 / 69 (vaccine cluster) | C5 | = 1.00 | Trajectory-mismatch detection (contested + tier-1 primary) |

**Anti-reflexivity defense (code-enforced):**

The Druckenmiller analogy works in markets because markets are reflexive
— prices incorporate participant beliefs. Biology is not reflexive, but
**editorial behavior is.** If ingestion is preferentially directed at
already-Δ²-positive entities, those entities will look more accelerated
in the next run because the curator fed them more recent sources, not
because the field actually accelerated.

This is the framework's most insidious failure mode, and it is **defended
by code, not by discipline.** Every Δ² run executes `audit_reflexivity()`
which:

1. Reads `score_history.csv` to find the previous run's per-entity ranking.
2. Identifies sources whose `date_ingested` post-dates that run.
3. Maps the new sources to entities and computes Spearman rank correlation
   between previous-run rank and inter-run new-source count.
4. Classifies the result:
   - `r < 0.30` → PASS
   - `0.30 ≤ r < 0.70` → WARN (logged, not halted)
   - `r ≥ 0.70` → FAIL (engine exits non-zero, **pipeline halts**)
5. Writes append-only log `delta_squared_v1/reflexivity_audit.csv` and
   human-readable `reflexivity_status.txt`.

Tested under attack: `scripts/test_delta_squared_reflexivity.py`
synthesizes a scenario where the curator preferentially fed top-ranked
entities; the audit correctly fires FAIL with r=0.985 and halts.

Threshold tuning: edit `REFLEXIVITY_WARN_THRESHOLD` and
`REFLEXIVITY_FAIL_THRESHOLD` constants in the engine. Override of a FAIL
must be documented in the commit raising the threshold; otherwise the
defense reverts to default on next pull.

Recommended ingestion budget allocation (when planning sessions): drive by
external literature volume (PubMed query counts per entity keyword set)
or hypothesis-coverage gaps. The audit catches violations either way.

**Window auto-rolling:** windows are computed at runtime from
`datetime.utcnow().year`. No annual code change needed.

**Anomaly detection:** if any single source contributes more than 30%
of an entity's recent-window tier-weighted weight, the entity is flagged
for human review. Defends against single-study spike inflation
(e.g. Hassan-2025 copper paper-style claims with implausible effect sizes
that would otherwise drive C1 / C2 acceleration).

**Data gap watchlist:** `DATA_GAP_WATCHLIST` in the engine is a list of
defined-entity IDs that should have non-zero sources. Currently includes
HYP-0026 PANDAS/PANS — a known real Δ²-positive field that the atlas has
not yet ingested. Each run writes a `data_gaps.csv` flagging unsatisfied
entries. Close gaps via `run_ingest.py` per the verification protocol.

**Run command:**

```bash
cd /Users/Greg/Autism
python3 scripts/compute_delta_squared.py
```

Or as part of the canonical pipeline (Step 7 in `apply_patches_and_score.py`).

**Personalized-risk integration (opt-in).** `personalized_risk.py` accepts a
`--use-delta-squared` flag (or `use_delta_squared=True` in the API call)
that blends Δ² trajectory momentum into intervention ranking:

```
score = atlas_quality × best_match_score × (1 + α × Δ²/100)
```

with α = 0.20 (so Δ²=100 → ×1.20 momentum bonus, Δ²=0 → ×1.00). Truth-
strength (CSRS) remains dominant; momentum is a tiebreaker bounded at +20%.
A high-Δ² low-CSRS intervention cannot leapfrog a moderate-CSRS moderate-
Δ² intervention. Default behavior is OFF — when the flag is unset the
output is byte-identical to the pre-integration engine, so existing
calibration cases continue to pass without modification. When ON, each
ranked intervention's `delta_squared_score` and `momentum_multiplier`
appear in the bundle for transparency.

## Verification protocol (BioMysteryBench-aligned, post-2026-04-30)

**Binding rule for all future seeding work, ingestion, and citation:**

Anthropic's BioMysteryBench evaluation (April 2026) documented that on hard
bioinformatics tasks, current Claude models succeed via "lucky solution paths"
that don't replicate across attempts — i.e., the model fabricates plausible-
looking wrong answers when ungrounded. This is the structural failure mode
behind the 2026-04-30 incident in which 45 of 52 PMIDs in an initial draft of
`iatrogenic_exposure_priors.csv` were fabricated from training-data
approximation. The error was caught by independent batch-verification before
sync; the file was rebuilt with 24 PMID-verified rows.

**Hard rule going forward**: no row shall be written to any prior CSV without
PubMed esummary verification of every cited PMID. Verification must check
(author OR title contains expected surname) AND (year matches) AND (key term
appears in title OR journal). Verification log persisted alongside the CSV.
A pre-commit hook (`scripts/precommit_pmid_verify.py`) blocks commits with
unverified PMIDs.

Memory-based PMID generation by an LLM agent is **forbidden**. Use the
`scripts/seed_with_verification.py` template, which requires the agent to
declare claimed PMID + claimed author/year/key-term separately, and verifies
they match the actual PubMed record before the row is written.

This rule applies to:
- All Phase 0 prior-table seeding (§3.13b physiological state normalization,
  §3.13c iatrogenic exposures, §3.1 gene variants, etc.)
- Any new researcher page, deep-dive topic, intervention, biomarker, or
  hypothesis added to the atlas
- Any citation added to existing pages
- Any source row added to `sources.csv`

Full protocol documented in `SESSION_4_HANNAH_POLING_SPEC.md` §24.

## Retention as a first-class design principle (post-2026-05-15)

**Retention is the load-bearing metric for the consumer surface.** A
high-agency mom comes back to the atlas iff every visit produces a
new actionable insight — a new test to consider, a new intervention to
discuss with her clinician, a new connection between her child's
profile and emerging literature, a new "what changed since last week."
If a visit doesn't move her forward, she doesn't return. The substrate
quality is invisible to her until it shows up as something she can do
Monday morning.

**This is not engagement metrics for engagement's sake.** It is the
single behavioral proxy for whether the substrate's value is reaching
the individual. Per the atlas mission — individual-level, not
population-level — retention is the only way to know the
individual-level promise is being kept across time. A mom whose child
is improving comes back to track. A mom whose path forward gained
clarity comes back to act. A mom who reads contested-evidence framing
honestly comes back because she's tired of being condescended to.

**Design choices that serve retention** (in order of leverage):

1. **Actionable on every visit.** The action card surfaces the
   TEST·DO·AVOID·TRACK answer for any phenotype in one click. The full
   115-row test catalog is visible in the graph as T-nodes. The
   substrate's value is one click away every visit, not buried under
   navigation.

2. **Fresh content via the live intake feed.** The PubMed scanner runs
   daily; the top-right ticker cycles real new candidates. Mom sees
   "this thing is breathing" without our hand on the scale. Δ² gives
   us trajectory, not just truth-strength — and the trajectory is
   visible.

3. **Personal profile saved across visits.** [Future build] Mom
   uploads her child's profile once (genetic + biomarker + history);
   the graph + action card adapt to that profile on subsequent visits.
   The atlas remembers what her child is.

4. **Biomarker re-testing schedule with comparison.** [Future build]
   The action card's TRACK row becomes a calendar reminder + a
   "what changed" diff when she returns to upload re-test results.

5. **"What's new since your last visit"** [Future build] A diff layer
   that surfaces: new papers in her child's phenotype cluster, new
   atlas entries, new responder-rate data, new combinations promoted
   from the discovery pipeline.

6. **Honest framing as a retention driver.** Functional medicine moms
   are sophisticated. The contested-status discipline, the §24
   verification, the firewall against outcome-feedback drift — these
   are not constraints on the product, they are *features* mom comes
   back for. Honesty is rare in this market; honesty compounds.

**What to measure.** **Daily return rate is the primary metric** — a
high-agency mom should have a reason to open the atlas every day,
because every day there should be something new worth knowing for her
child specifically. Secondary metrics: day-7 and day-30 retention,
time-to-first-action-card-open per session, depth per session (number
of phenotypes/tests/interventions/biomarkers explored), profile-upload
rate, re-test-result upload rate (the ultimate retention signal — she
came back, with new data, because the path worked enough to keep
going).

**Why daily, not weekly.** The intake feed delivers ~30-40 new papers
per day across 12 query categories. Δ² shifts trajectory weights
nightly. New combinations get promoted from the discoveries inbox on
the curator's cadence. The substrate is doing real work every day —
the consumer surface must reflect that. The "Today's literature" panel
in the start-dock must show new content every visit; if it shows the
same content as yesterday, the substrate has failed to feed the loop.

**What NOT to do to retention.** Dark patterns. Notification spam.
Engagement-hacking. The atlas is an individual-level diagnostic
substrate, not a wellness-influencer feed. Retention earned by
honesty + actionability + accuracy. Anything else collapses the
methodology and the trust at the same time.

**The high-value rule:** every design and engineering decision
downstream of this is evaluated against "does it serve retention via
actionability, freshness, personalization, and honesty?" If it does,
ship it. If it doesn't, it's lower priority than something that does.
Retention as the proxy. Truth as the substrate. Both, not either.

## Field outcomes firewall (post-2026-05-15)

The atlas's published calibration anchors — cohort MAE = 0.0665 (n=8),
within-driver-coverage MAE = 0.049 (n=7), and INT-0001 Leucovorin
CSRS = 83.35 — are defended by PMID-verified RCT evidence only.
Parent-submitted outcome data ("field outcomes") would introduce
selection bias (parents preferentially report positive outcomes) and
could silently drift the published metrics. Once that drift begins, the
methodology becomes unsupportable to a federal evaluator.

**Hard rule:** `v2.0_scored/field_outcomes.csv` is curator-write,
scoring-engine-read-never. The firewall is code-enforced via
`scripts/precommit_field_outcomes_firewall.py`:

- Scoring-engine files (`run_scoring*.py`, `compute_responder_mae.py`,
  `validate_v02_calibration.py`, `compute_delta_squared.py`,
  `compute_formulation_scores.py`, `personalized_risk*.py`) must NOT
  reference `field_outcomes.csv`.
- `v2.0_scored/` CSVs other than `field_outcomes.csv` itself must NOT
  reference `field_outcomes`.
- Files that DO read field outcomes must be in the explicit ALLOWLIST
  (currently: planned future parent-community report surfaces only).

This mirrors the §24 PMID-verification firewall in structure: instead
of preventing PMID fabrication, it prevents outcome-feedback drift.
Both protect the atlas's published methodology from systematic bias
patterns the underlying epistemic principles couldn't catch via human
review alone.

See `ACTIONABLE_REPORT_PRODUCT_SPEC.md` §"Mitigation 2" for product-
level context and `SIX_MONTH_FAILURE_MODES.md` for the failure-mode
analysis that motivated this firewall.

## Design system & cinematic GTM layer

The atlas has **two communication surfaces with different brand languages.**
Confusing them collapses both.

**Surface 1 — Institutional (deck, atlas explorer, internal UI, investor
and researcher comms).** Palantir × CERN × Arc Institute. Heavy
typographic restraint, no emojis, no marketing voice. The word
"deterministic" never appears in public copy — use "reproducible" or
"stable." Density as authority. Slow, confident, institutional. The
aesthetic argument is *we have been here forever; we're only now
revealing ourselves.* The live design engagement (see "Active design
engagement" below) delivers against this surface.

**Surface 2 — Cinematic / cultural (landing page, films, X drops,
comms to parent communities, anything that touches culture rather than
capital).** Karpathy-vault aesthetic but encoded with meaning. Ive on
form (restraint, inevitability, UI vanishes into scene); the cultural
register on truth (no softening of the framing, real human cost made
visible, build in public via mysterious fragments rather than launch
events). Going "full Kanye" on this surface means **discipline about
which voice goes where** — Kanye-level restraint when speaking to
capital, Kanye-level unflinchingness when speaking about the missed
children. Not loud, never loud. Inevitable.

**The hero interaction (cinematic surface).** Default graph shows a
generic patient with most edges dim. Load a specific susceptibility
profile (Hannah Poling demo first) and a specific subgraph LIGHTS UP
while the rest fades to ghost. That sub-graph is the child's map.
This is the money shot — personalized resolution as visual revelation.
Population-average medicine literally fading in real time, replaced
by one child's truth. The emotional anchor over any cinematic is one
autism mom's voice — 30 seconds, real story, no narrator, no AI
voice, no music. A sub-bass pulse at ~60 bpm fires only when nodes
pulse. Silence between. Restraint as luxury.

**The wedge is autism, not "every medical condition."** Autism done
with such individual-level resolution that population-average
approaches look like malpractice. Other conditions tile in as their
mechanisms absorb into the atlas (mito, PANDAS/PANS, MCAS,
methylation, dysautonomia, dysmotility). The graph absorbs them
naturally. Don't pitch the absorption — let the graph show it.

**Color encoding (cinematic surface).** Deep navy near-black
background; off-white nodes (not pure white — pure white reads
clinical/sterile/hospital, off-white reads inevitable/civilizational);
edges color-graded by source tier — tier-1 FOIA / federal-record / RCT
primary edges glow warm (gold-amber), mainstream cohort epidemiology
cool blue, contested edges flicker subtly. Encode `W_DESIGN`,
`evidence_strength_aggregate`, Δ², polarity, and source-tier directly
in light. This is what the scoring engine gives this product that
Karpathy's vault doesn't — meaning per edge.

**Color encoding (institutional / atlas explorer).** Under review per
DESIGN_TEAM_HANDOFF.md. Current implementation uses 11 hues for
mechanism class — collapse to 5–6 superclasses likely wins for
first-look legibility.

**Typography.** Custom serif (Söhne Buch, GT Sectra, Editorial New,
or commissioned). Never Inter / Roboto / dataviz-library defaults.
The wordmark and typeface together carry the institutional weight.

**Naming.** "Causes Atlas (Autism)" is the internal / engineering
name only. Public-facing name is TBD — should be one word, Greek/Latin
medical root or fully abstract, no "AI," no "atlas," no descriptive
construction. Mission encoded by the graph, not the name.

### Active design engagement (P0 — opened 2026-05-12)

Repo: https://github.com/fluffybear1016/causes-atlas-autism
Entry doc: `DESIGN_TEAM_HANDOFF.md` (brand guardrails, 5-min
quickstart to open existing visual artifacts in a browser, P0/P1/P2
scope in §8)
Slide spec: `DECK_v2_15_SLIDE_SPEC.md`
Existing chrome: `ui/components/deck/_slide_chrome.css` — already-
built slides 1, 2, 10 show the system in action
Sanity-check before/after any change: `python3 scripts/pre_handoff_audit.py`
Expected: `0 CRIT / 0 HIGH / 0 MED / 12 LOW / 9 OK`. Anything else,
ping the data team before changing data files.
Regression commands (calibration + MAE) in `REGRESSION_2026_05_09.md`.

**P0 in priority order:**

1. **Slide 6 — the cathedral slide.** Load-bearing slide of the deck.
   Emotional beat, not data density. Spec under "Slide 6 — The
   cathedral slide" in `DECK_v2_15_SLIDE_SPEC.md`. Build on top of
   `ui/components/substrate_diagram_slide.html`.
2. **Slides 3, 4, 5, 7, 8, 9, 11, 12, 13, 14, 15.** Typography-heavy,
   share chrome with slides 1, 2, 10. Content per slide in
   `DECK_v2_15_SLIDE_SPEC.md`.
3. **Atlas explorer color encoding review.** Open
   `ui/components/atlas_explorer_preview.html`. Decide whether to
   collapse 11 hues → 5–6 superclasses for first-look legibility.

**Three ground-truth numbers — must appear verbatim in public copy:**

| Claim | Exact value to print |
|---|---|
| Within-driver coverage MAE (n=7) | `0.049` |
| Sub-3% errors spanning 3 mechanism axes | `4` (oxidative stress / methylation / GABA-Cl⁻) |
| INT-0001 Leucovorin CSRS (calibration anchor, never drifted) | `83.35` |

Do not paraphrase. Do not restate as "~5%" or "around 80." The exact
numbers are the proof. The non-drift of `83.35` across major revisions
is itself the argument.

**Hard word constraints (public copy / deck / atlas explorer):**
- Never "deterministic" — use "reproducible" or "stable."
- No emojis.
- No marketing voice. Institutional restraint only.
- Don't paraphrase the three ground-truth numbers.

**Deliver as PRs to:**
- `ui/components/deck/` — slides
- `ui/components/atlas_explorer.py` — explorer
- Open data-team questions → §10 of `DESIGN_TEAM_HANDOFF.md`

## What not to do

- Don't edit `v2.0_scored/` CSVs by hand — re-run the scoring pipeline.
- Don't add LLM calls to the scoring engine (spec violation; determinism).
- **Don't write any PMID without PubMed esummary verification** — see the
  Verification protocol section above. Memory-based PMID generation produces
  fabricated citations. Use `scripts/seed_with_verification.py`.
- Don't drop "contested" status from any hypothesis based on a single
  paper either way (spec §1.1, §9.1).
- Don't push to Drive with anything other than `rclone sync` (other
  paths bypass the manifest and break incremental updates).
- Don't commit secrets — the rclone OAuth token in
  `/Users/Greg/.config/rclone/rclone.conf` must never be checked in.
- **Don't let mainstream consensus override primary evidence.** If a
  FOIA-released government document or a peer-reviewed primary study
  contradicts the public-health guidance, both go in the atlas at
  appropriate weight; the engine integrates them.
- **Don't recommend population-level vaccination policy as if it were
  individual-level optimization.** Different objective function. The
  atlas is for individual / family decisions.
- **Don't add fact-check journalism, editorial commentary, or advocacy
  content as primary evidence.** They go in only if the user explicitly
  requests, with `study_design=editorial/letter/comment/news` or
  `type=advocacy/factcheck`, which auto-downweights them.
- **Don't paraphrase the three ground-truth numbers in public copy.**
  `MAE = 0.049` (n=7 within-driver coverage), `4` sub-3% errors across
  3 mechanism axes (oxidative stress / methylation / GABA-Cl⁻), and
  `INT-0001 Leucovorin CSRS = 83.35` appear exactly as written. Their
  precision and non-drift are the argument. "Around 5%" or "above 80"
  collapses the claim.
- **Don't use "deterministic" in public copy.** Use "reproducible" or
  "stable." (Internal CLAUDE.md / scripts / specs may use the term.)
- **Don't use emojis in the deck, atlas explorer, or any
  institutional surface.** Palantir × CERN × Arc Institute — restraint
  as authority.
- **Don't pitch "every medical condition" as the wedge.** Autism is
  the wedge; other conditions tile in as their mechanisms absorb into
  the graph. Pitch the depth, not the breadth.
- **Don't collapse the two brand surfaces.** Institutional surface
  (deck, explorer, capital comms) is Palantir/CERN/Arc restraint.
  Cinematic surface (films, X drops, parent-community comms) is
  Karpathy-vault aesthetic with Ive form + cultural unflinchingness.
  Marketing voice doesn't appear on either surface.
