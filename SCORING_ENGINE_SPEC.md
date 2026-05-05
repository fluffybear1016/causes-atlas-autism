# SCORING ENGINE SPEC

**Version:** 1.0
**Anchored to:** `CAUSES_ATLAS_AUTISM_SPEC_v1.1.md` §7.1, §7.2, §7.3
**Companion to:** `MIGRATION_IMPLEMENTATION.md` step 19
**Status:** Canonical scoring spec. All weights tunable via config; computation deterministic.

This document specifies the scoring engine that turns the migrated graph into computed `confidence_score`, `evidence_strength`, `evidence_strength_aggregate`, `csrs_score`, and `strength_score` values, and emits one `score_history` row per change. It is **deterministic** — same inputs and same config produce identical outputs — and **LLM-free** (per spec §1.5 and §7.3).

---

## 1. Inputs and Outputs

**Reads** the migrated CSVs:
- Layer 1: `hypotheses`, `mechanisms`, `phenotypes`, `genes`, `sources`, `evidence_fragments`, `evidence_links`, `hypothesis_mechanism_edges`, `mechanism_phenotype_edges`, `gene_mechanism_edges`, `gene_hypothesis_edges`, `gene_phenotype_edges`
- Layer 2: `interventions`, `intervention_mechanism_edges`, `intervention_hypothesis_edges`, `intervention_phenotype_edges`, `intervention_gene_edges`, `combinations`, `combination_members`
- Read-only reference: `node_aliases`

**Writes** the same CSVs back with computed columns populated, plus:
- `score_history` — one row per node whose score moved from blank or from a `*_legacy` value to a computed value.

**Does not modify**:
- Any `*_legacy` column.
- Any descriptive scalar (name, category, dose_range, etc.).
- The structural relationships (no edges added or removed).

---

## 2. Scoring Configuration

All weights and tier values live in a single config dict at the top of `run_scoring.py`. None of them are hand-tuned per row; they are global knobs that produce a uniform scoring function across the whole graph. Re-runs with the same config are bitwise identical.

### 2.1 Study-design weights (`W_DESIGN`)

| Design | Weight |
|---|---|
| `meta_analysis` | 1.00 |
| `rct` | 0.95 |
| `cohort` | 0.75 |
| `case_control` | 0.70 |
| `case_series` | 0.45 |
| `mechanistic` | 0.35 |
| `review` | 0.55 (downweighted as secondary literature) |
| `animal` | 0.30 |
| `in_vitro` | 0.25 |
| `in_silico` | 0.20 |
| `epigenetic` | 0.50 |
| `transgenerational` | 0.50 |
| `other` | 0.50 |
| (null / not applicable) | 0.40 |

### 2.2 Source-type weights (`W_SOURCE_TYPE`)

| Type | Weight |
|---|---|
| `study` | 1.00 |
| `meta_analysis` | 1.00 |
| `review` | 0.70 |
| `preprint` | 0.85 |
| `clinical` | 0.90 |
| `registry` | 0.85 |
| `dataset` | 0.80 |
| `trial` | 0.95 |
| `environmental` | 0.70 |
| `anecdote` | 0.15 |
| `social` | 0.10 |
| `other` | 0.40 |

### 2.3 Sample-size factor (`f_n`)

| `sample_size` | Factor |
|---|---|
| ≥ 1000 | 1.00 |
| 100–999 | 0.85 |
| 50–99 | 0.70 |
| 20–49 | 0.55 |
| 1–19 | 0.40 |
| null | 0.50 |

### 2.4 Replication factor (`f_rep`)

(Read from `evidence_fragments.structured_payload.replicated`.)

| Value | Factor |
|---|---|
| `yes` | 1.00 |
| `partial` | 0.75 |
| `no` | 0.55 |
| `unknown` / null | 0.65 |

### 2.5 Effect-direction certainty (`f_dir`)

| `effect_direction` | Factor |
|---|---|
| `positive` | 1.00 |
| `negative` | 1.00 |
| `mixed` | 0.65 |
| `neutral` | 0.75 |
| `unclear` | 0.50 |

### 2.6 Hypothesis confidence component weights (`W_HYP`)

Sum to 1.0.

| Component | Weight |
|---|---|
| `evidence_quality_index` | 0.30 |
| `consistency_index` | 0.15 |
| `mechanism_coherence` | 0.20 |
| `genetic_support` | 0.15 |
| `cross_phenotype_convergence` | 0.10 |
| `source_type_diversity` | 0.05 |
| `replication_independence` | 0.05 |

### 2.7 CSRS component weights (`W_CSRS`)

Sum to 1.0. Component definitions in §6.

| Component | Weight |
|---|---|
| `hypothesis_alignment` | 0.25 |
| `mechanism_strength` | 0.20 |
| `phenotype_effect` | 0.10 |
| `genetic_coherence` | 0.10 |
| `safety_score` | 0.15 |
| `replication_score` | 0.10 |
| `trend_score` | 0.05 |
| `synergy_bonus` | 0.05 |

### 2.8 Safety mapping

| Field | Value | Score |
|---|---|---|
| `pediatric_safe` | `yes` | 1.00 |
| | `age_restricted` | 0.75 |
| | `uncertain` | 0.55 |
| | `no` | 0.20 |
| | null | 0.50 |
| `otc_or_rx` | `otc` | 1.00 |
| | `lifestyle` | 1.00 |
| | `environmental` | 0.95 |
| | `rx` | 0.80 |
| | null | 0.70 |
| `cost_per_month_usd` | 0 | 1.00 |
| | 1–25 | 0.95 |
| | 26–75 | 0.85 |
| | 76–200 | 0.65 |
| | > 200 | 0.45 |
| | null | 0.70 |

`safety_score = harmonic_mean(pediatric, otc_or_rx, cost)` — harmonic mean penalizes any single weak component, which matches how clinicians actually evaluate intervention safety.

### 2.9 Anti-domination caps

To prevent any single very-large evidence pool from dominating:

- **Social-evidence cap.** Anecdote + social fragments contribute at most `CAP_SOCIAL = 0.25` of any node's `evidence_quality_index`. Excess social fragments still count for `evidence_count` but their strength contribution is clamped.
- **Single-source cap.** No single `source_id` contributes more than `CAP_SINGLE_SOURCE = 0.30` of any node's `evidence_quality_index` (prevents one giant review from dominating).
- **Log-scaling.** `evidence_count` enters scores as `log(1 + n) / log(1 + N_REF)` with `N_REF = 50`, so a node with 500 weak studies doesn't dominate one with 5 strong RCTs.

### 2.10 CSRS scale

`csrs_score ∈ [0, 100]`. Final value = `100 × Σ(component × weight)` where each component is normalized to `[0, 1]`.

---

## 3. Per-Fragment Strength (`strength_score`)

Computed once per `evidence_fragment` row.

**For study/review/meta-analysis/preprint fragments:**

```
strength_score = w_design × f_n × f_rep × w_type × f_dir
```

clipped to `[0, 1]`, where:
- `w_design = W_DESIGN[sources.study_design]`
- `f_n = f_n_lookup(sources.sample_size)`
- `f_rep = f_rep_lookup(structured_payload.replicated)`
- `w_type = W_SOURCE_TYPE[sources.type]`
- `f_dir = f_dir_lookup(effect_direction)`

**For anecdote/social fragments:**

```
strength_score = w_type × f_dir × engagement_factor × reporter_factor
```

where:
- `engagement_factor`:
  - YouTube: `min(1.0, log(1 + view_count) / log(1 + 100000))` — saturates around 100K views
  - Reddit: `min(1.0, comment_count / 200)` — saturates at 200 comments
  - missing: 0.5
- `reporter_factor`:
  - `clinician` or `researcher`: 1.00
  - `patient`: 0.85
  - `parent`: 0.80
  - `unknown`: 0.55

`extraction_confidence` is set to `0.95` for `extraction_method='rule_based'`, `0.70` for `llm_assisted`, `1.00` for `manual`.

---

## 4. Node Aggregates (Pass 1)

For each Layer 1 node (hypothesis, mechanism, phenotype, gene), gather evidence_links targeting it and compute:

**`evidence_count`** — number of distinct `source_id` values (via `evidence_fragments.source_id`) backing this node. Distinct, not raw count of links.

**`evidence_quality_index ∈ [0, 1]`** — weighted mean of fragment `strength_score`, with the caps from §2.9 applied:

```
contributions = []
for each link targeting this node:
    s = fragment.strength_score × link.effect_direction_match
    contributions.append((source_id, source_type, s))

# apply single-source cap
group by source_id, cap each group's total contribution at CAP_SINGLE_SOURCE × Σall

# apply social cap
social_total = Σ contributions where source_type ∈ {anecdote, social}
non_social_total = Σ others
if social_total > CAP_SOCIAL × (social_total + non_social_total):
    scale social contributions down so social_total = CAP_SOCIAL × (social_total + non_social_total)

evidence_quality_index = (Σ capped contributions) / (1 + Σ capped contributions)
```

The final `x / (1 + x)` softplus ensures the index saturates near 1.0 without ever reaching it; this is intentional, because no real node should score 1.0 ("certain") from finite evidence.

**`consistency_index ∈ [0, 1]`** — based on Shannon entropy of the effect-direction distribution on links targeting this node:

```
counts = histogram of effect_direction over links
p = counts / Σcounts
H = -Σ p_i × log(p_i)
H_max = log(num_directions_observed)
consistency_index = 1 - H/H_max  if H_max > 0 else 1.0
```

A node with all-positive evidence has `consistency_index = 1.0`. A 50/50 positive/negative split has `consistency_index = 0.0`. Mixed-with-mostly-positive lands in between.

**`source_type_diversity ∈ [0, 1]`** — number of distinct `sources.type` values among contributing fragments, normalized by 5 (because 5 source types is a healthy ecosystem: study + clinical + registry + anecdote + dataset).

**`replication_independence ∈ [0, 1]`** — heuristic proxy: count of distinct authoring institutions/journals approximated by distinct `sources.platform × first_author` tuples. Since v1.1 doesn't store first_author as a structured field, we use distinct `sources.id` from positive-direction links as a stand-in. Saturates at 5 distinct sources.

---

## 5. Edge Aggregates (Pass 2)

For each edge table (hypothesis_mechanism_edges, intervention_mechanism_edges, etc.), compute:

**`evidence_for_count`, `evidence_against_count`** — direct counts of evidence_links targeting this edge specifically (target_type = the edge type, target_id = edge id), partitioned by `effect_direction`. In the migrated dataset, almost all edges have zero direct links; the aggregate is then derived from connected node strengths (next).

**`evidence_strength_aggregate ∈ [0, 1]`** — geometric mean of the two endpoint nodes' relevant scores, multiplied by edge polarity coefficient:

```
For hypothesis_mechanism_edge(h, m):
    base = sqrt(hypothesis[h].evidence_quality_index × mechanism[m].preliminary_strength)

For intervention_mechanism_edge(i, m):
    base = sqrt(intervention_evidence_quality[i] × mechanism[m].preliminary_strength)

polarity_coef = {supporting: 1.0, contradicting: -1.0, neutral: 0.0, unknown: 0.5}
evidence_strength_aggregate = max(0, base × polarity_coef)
```

Geometric mean is chosen because it penalizes asymmetry: an edge between a strong hypothesis and a weak mechanism shouldn't score as if both were equally strong.

`mechanism.preliminary_strength` in pass 2 = `mean(connected_hypotheses' evidence_quality_index) × (1 if seeded else 0.85)`. Seeded mechanisms (MEC-0001 through MEC-0010, listed in spec §4.2) get a small confidence prior because they're canonical biological pathways with abundant external literature; this is the only place we admit external prior knowledge into the score.

---

## 6. Final Node Scores (Pass 3)

### 6.1 Hypothesis `confidence_score ∈ [0, 1]`

```
confidence_score = (
    W_HYP[evidence_quality_index]      × evidence_quality_index
  + W_HYP[consistency_index]           × consistency_index
  + W_HYP[mechanism_coherence]         × mechanism_coherence
  + W_HYP[genetic_support]             × genetic_support
  + W_HYP[cross_phenotype_convergence] × cross_phenotype_convergence
  + W_HYP[source_type_diversity]       × source_type_diversity
  + W_HYP[replication_independence]    × replication_independence
)
```

where:

- `mechanism_coherence` = mean of `evidence_strength_aggregate` over outgoing `hypothesis_mechanism_edges` from this hypothesis (0 if no edges).
- `genetic_support` = (only for hypotheses with `category=genetic` or with linked genes) max of normalized SFARI score over `gene_hypothesis_edges`, fallback to mean of `opentargets_score` over linked genes. SFARI normalization: S=1.0, 1=0.95, 2=0.80, 3=0.60, NA=0.30. For non-genetic hypotheses, this term is set to 0.40 (neutral — no penalty for not being genetic).
- `cross_phenotype_convergence` = `min(1.0, n_distinct_phenotypes_reached / 3)` where reachability is via the path hypothesis → hypothesis_mechanism_edge → mechanism → mechanism_phenotype_edge → phenotype. (In the migrated dataset `mechanism_phenotype_edges` is empty, so this term is 0 for all hypotheses initially. The engine still computes it; it'll light up after ingestion.)

### 6.2 Mechanism `evidence_strength ∈ [0, 1]`

```
evidence_strength = mean over (
    incoming hypothesis_mechanism_edges' evidence_strength_aggregate,
    outgoing intervention_mechanism_edges' evidence_strength_aggregate,
    outgoing mechanism_phenotype_edges' evidence_strength_aggregate
), weighted by edge count in each direction.

If no edges: evidence_strength = 0.30 if seeded else 0.0
```

### 6.3 Phenotype `confidence_score`

Same shape as hypothesis but with mechanism-coherence drawn from incoming `mechanism_phenotype_edges`. With the migration's empty mech_phenotype edges, phenotypes start at low scores driven only by descriptive priors. Acceptable — phenotypes light up after ingestion.

### 6.4 Gene `evidence_strength` (computed)

Already has `genetic_evidence_strength` (legacy 1–5) and `opentargets_score` (external). The engine does **not** overwrite either. Genes are read-only sources of genetic_support to hypotheses.

---

## 7. Layer 2: CSRS for Interventions and Combinations (Pass 4)

Per spec §6.1 and §7.2 — derived only from Layer 1 aggregates, never from raw evidence counts.

### 7.1 Intervention CSRS components

For each intervention `i`:

**`hypothesis_alignment ∈ [0, 1]`** — weighted by edge polarity:
```
For each intervention_hypothesis_edge(i, h):
    contribution = hypothesis[h].confidence_score × polarity_coef(edge)
hypothesis_alignment = max over edges, fallback to mean if max is 0
```

**`mechanism_strength ∈ [0, 1]`** — same pattern over `intervention_mechanism_edges` and `mechanisms.evidence_strength`.

**`phenotype_effect ∈ [0, 1]`** — same pattern over `intervention_phenotype_edges`. Currently empty → 0 for all interventions.

**`genetic_coherence ∈ [0, 1]`** — mean of `opentargets_score` over `intervention_gene_edges`; fallback to 0.30 if no linked genes (neutral, not penalty).

**`safety_score ∈ [0, 1]`** — harmonic mean of three components from §2.8.

**`replication_score ∈ [0, 1]`** — `min(1.0, n_distinct_sources_via_evidence_links / 5)` where the count is over evidence_links targeting this intervention directly.

**`trend_score ∈ [0, 1]`** — fraction of evidence_links targeting this intervention whose `sources.date_published` is within the last 5 years. If no dates available: 0.50 (neutral).

**`synergy_bonus ∈ [0, 1]`** — for combo `intervention.category=combo` or `combo_seed`: 1.0 if at least 2 component mechanisms are independently supported (their `evidence_strength ≥ 0.5`); else 0.5. Non-combos: 0.0.

### 7.2 Final CSRS

```
csrs_score = 100 × (
    W_CSRS[hypothesis_alignment]   × hypothesis_alignment
  + W_CSRS[mechanism_strength]     × mechanism_strength
  + W_CSRS[phenotype_effect]       × phenotype_effect
  + W_CSRS[genetic_coherence]      × genetic_coherence
  + W_CSRS[safety_score]           × safety_score
  + W_CSRS[replication_score]      × replication_score
  + W_CSRS[trend_score]            × trend_score
  + W_CSRS[synergy_bonus]          × synergy_bonus
)
```

`csrs_last_updated` = engine run timestamp.

### 7.3 Combination CSRS

Same component structure, but:
- `hypothesis_alignment` = weighted sum of member-intervention scores via `combination_members`
- `mechanism_strength` = mean of member mechanism strengths, with a +0.1 bonus if members target ≥ 2 distinct mechanisms (true synergy signal)
- `safety_score` = harmonic mean over members (weakest member's safety dominates)
- `synergy_bonus` = 1.0 if ≥ 2 distinct mechanisms covered AND no contradicting interactions noted in `combinations.interaction_warnings`; else 0.5

---

## 8. score_history Emission (Pass 5)

For every node whose live computed column is now non-null, emit one `score_history` row:

```
id              = SCH-######
target_type     = "hypothesis" | "mechanism" | "phenotype" | "intervention" | "combination"
target_id       = canonical ID
score_type      = "confidence" | "csrs" | "other"
old_score       = value from corresponding *_legacy column if present, else ""
new_score       = the computed value
component_breakdown = JSON object of per-component contributions
evidence_delta_ids  = JSON list of evidence_fragment_ids that contributed
computed_at     = scoring engine run timestamp
```

The engine never deletes existing `score_history` rows; it only appends. On re-runs, we get an audit trail of how scores moved between runs.

---

## 9. Calibration Anchor

Per the v0.1 README and `MIGRATION_IMPLEMENTATION.md` step 20:

> Leucovorin (`INT-0001`) must score `csrs_score ≥ 80` from Layer 1 aggregates alone, anchored to the Frye 2018 RCT (`PMID 30097774`). If it doesn't, weights are wrong — fix before publishing.

The engine emits a structured calibration report at the end of every run:

```
Calibration test:
  INT-0001 Leucovorin
    csrs_score      = X.X / 100      [PASS / FAIL — threshold 80]
    hypothesis_alignment   = X.XX  (HYP-0001 confidence X.XX)
    mechanism_strength     = X.XX
    genetic_coherence      = X.XX  (GEN-0001 FOLR1)
    safety_score           = X.XX
    replication_score      = X.XX
```

A FAIL halts the run with a non-zero exit code so CI / migration locks trigger.

---

## 10. Determinism Guarantees

- **No non-deterministic floating-point.** All computations use plain Python `float`. No GPU. No parallelism that reorders sums.
- **Stable sort everywhere.** Edge enumeration, source enumeration, fragment enumeration all use lexicographic ID ordering before aggregation, so floating-point summation order is identical across runs.
- **No random seeds.** No Monte Carlo. No bootstrapping in v1.0 of the engine.
- **All weights in code constants.** Changing weights requires code review — no silent config drift.
- **Hash check.** The engine emits a SHA-256 of the concatenated config dict at startup. If anyone changes a weight without bumping the engine version, the hash flips and downstream systems can detect the drift.

---

## 11. What This Spec Does Not Do

- Does not ingest new data — that's the ingestion pipeline (spec §8.3).
- Does not propose ontology changes.
- Does not cleanse or correct evidence data.
- Does not run causal inference (no Bayesian networks, no DAG counterfactuals). v1.0 of the engine is purely associational + path-coherence.
- Does not write to non-canonical fields (no atlas_page_url, no UI metadata).

---

**End of SCORING_ENGINE_SPEC.md.**
