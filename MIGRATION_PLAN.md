# MIGRATION PLAN — `causes_atlas_schema_v0.1.xlsx` → Causes Atlas (Autism) Canonical Schema

**Spec governed by:** `CAUSES_ATLAS_AUTISM_SPEC.md` v1.0 (2026-04-24)
**Legacy source:** `causes_atlas_schema_v0.1.xlsx` (v0.1, 2026-04-23, 8 data sheets + README)
**Status:** Planning document. No spec changes proposed. No code in this document.

This plan maps every legacy sheet into the canonical Layer 1 / Layer 2 architecture, preserves provenance, strips all hand-edited scores from the scoring path, and surfaces every ambiguity rather than resolving it silently.

---

## 1. Governing Constraints (Re-derived From Spec)

The migration is constrained by the following spec clauses. Every sheet-level mapping decision below is anchored to one or more of these.

1. **Layer 1 / Layer 2 separation (§2.1).** Hypotheses, mechanisms, phenotypes, genes, sources, evidence_fragments, claims, and their edges are Layer 1. Interventions, combinations, and CSRS-style scores are Layer 2. Layer 2 may read only Layer 1 *aggregates*, never raw evidence rows.
2. **No semicolon-packed FKs in new tables (§3.1, §3.2, §12).** Multi-ID cells survive only in `*_legacy` columns. All relationships are expressed as rows in linking tables.
3. **Evidence-first architecture (§4.5, §4.6, §5.5, §8.3).** Every score, edge, and derived claim must trace to one or more `evidence_fragments` via `evidence_links`. Interventions do not hold raw `source_pmids` / `source_anecdote_ids` columns.
4. **Mechanisms are a required first-class layer (§4.2, §5.1, §5.2, §5.3).** Hypotheses do not attach to phenotypes directly in core; they route through mechanisms.
5. **Interventions / CSRS are derived only from the graph (§6.1, §7.2).** "No direct 'count studies where `intervention_id = X`' … in scoring."
6. **No hand-edited scores anywhere (§4.1, §6.1, §12).** `confidence_score`, `csrs_score`, `evidence_strength`, and aggregates are computed-only.
7. **Contradiction and provenance preservation (§5.5, §7.1, §9.1, §9.2).** Every evidence row carries `effect_direction`; every node/edge carries a `consistency_index`; every score change appends to `score_history`.
8. **`contested` is a valid permanent state (§9.1).** Migration must not silently resolve conflicts.
9. **Auditability (§1.6).** Every migrated score must be reproducible from deterministic rules over explicit evidence rows.
10. **Legacy packed lists are tolerated only in `*_legacy` fields (§3.2, §11.1, §12).**

**Derived migration rule:** Anything in the workbook that looks like a score, ranking, or multi-ID relationship field either (a) becomes a linking table, (b) becomes an `*_legacy` archival column, or (c) is dropped from the new schema and recomputed.

---

## 2. Legacy Workbook Inventory (Observed)

Confirmed by inspection of the uploaded file:

| Sheet | Rows (data) | Cols | Primary role in v0.1 |
|---|---|---|---|
| `README` | 41 | 1 | Mission, usage, calibration seed |
| `interventions` | 60 | 16 | Intervention-first ranking + packed FKs |
| `causes` | 30 | 13 | Cause/hypothesis entries + packed FKs |
| `studies` | 778 | 16 | Literature, one row per PMID |
| `anecdotes` | 520 | 13 | Reddit + YouTube reports |
| `combinations` | 4 | 10 | Explicit combos |
| `phenotypes` | 7 | 9 | Subtypes + "top" FKs |
| `genes` | 1564 | 9 | SFARI + OpenTargets seed |
| `csrs_components` | 266 | 8 | Per-(intervention, component) hand scores |

**Observed data-quality signals (used throughout the mapping):**

- `targets`, `source_pmids`, `source_anecdote_ids`, `mitigation_intervention_ids`, `top_intervention_ids`, `top_cause_ids`, `associated_phenotype_ids`, `linked_intervention_ids`, `member_intervention_ids`, `evidence_pointers` are all **semicolon-packed** and violate §3.2 for the new schema. They must survive only in `*_legacy` columns on the migrated rows.
- Legacy `studies.study_type` enum includes **`observational`**, which is not in the spec `sources.study_design` enum.
- Legacy `causes.category` enum includes **`pharmacological`** and **`dietary`**, which are not in the spec `hypotheses.category` enum.
- Legacy `genes` uses `gene_symbol` as the natural key — there is no `GEN-####` ID yet. Spec §4.4 requires `GEN-0001`-style PKs.
- Legacy `anecdotes.reported_outcome` uses `null` (string) for the neutral case; spec §5.5 uses `neutral`.
- Legacy hand-edited scores present: `interventions.csrs_score`, `causes.evidence_strength`, `causes.epidemiological_strength`, `causes.csrs_score`, `genes.evidence_strength`, `genes.opentargets_score` (external), `csrs_components.weight_pct`, `csrs_components.raw_score_0_100`, `csrs_components.weighted_contribution`.
- `studies` has 601/778 rows with `intervention_id` populated, 266/778 with `cause_id`, 110/778 with both, 21/778 with neither.
- `csrs_components` only covers 11 distinct interventions out of 60 — the rest of the legacy CSRS values on `interventions` rows cannot be reproduced from this sheet.

---

## 3. Sheet-by-Sheet Migration Map

For each sheet: **purpose in v0.1 · new target table(s) · columns surviving · columns renamed · columns split · columns derived-only or deprecated · columns requiring manual review · data-quality notes.**

### 3.1 `README`

**Purpose (v0.1):** Mission statement, sheet index, Google Sheets usage, calibration seed statement (leucovorin / CFD phenotype target CSRS > 80), First Amendment posture, version/owner.

**Maps to:**
- Not a data table. Content is informational.
- Relevant operational items (calibration target, First Amendment posture) should be preserved in project documentation, **not** as rows in any new table.

| Legacy content | New home | Notes |
|---|---|---|
| Mission text | Project README (outside the canonical spec). | Not part of schema. |
| Sheet list | Superseded by this plan and the canonical schema. | Drop. |
| Google Sheets usage instructions | Operational runbook (ingestion docs). | Not part of schema. |
| Calibration seed (leucovorin ≥ 80, anchored in Frye 2018) | **Retain as a calibration test** for the scoring engine (§7.1/§7.2), not as data. | Becomes an automated assertion run after each score recomputation. |
| First Amendment posture | Project README. | Not part of schema. |
| VERSION 0.1 / DATE / OWNER | Archival provenance. | Record in the migration audit log (see §7 below). |

**Data-quality issue:** README describes the CSRS as "hand-tuned weights," which is explicitly forbidden for the *data* model by spec §6.1 and §7.2. Only *configurable weights* are allowed, in config — not in data.

---

### 3.2 `interventions`

**Purpose (v0.1):** The intervention-first ranking sheet — one row per candidate treatment/prevention, each with a single pre-baked `csrs_score` and semicolon lists of source PMIDs and anecdotes. This is the sheet the legacy system was built around.

**Maps to (Layer 2 core + derived edges into Layer 1):**
- `interventions` (Layer 2, §6.1)
- `intervention_mechanism_edges` (§6.2)
- `intervention_hypothesis_edges` (§6.3)
- `intervention_phenotype_edges` (§6.4) — populated later from graph derivation, not from this sheet
- `intervention_gene_edges` (§6.5)
- `evidence_links` (Layer 1, §5.5) — generated from `source_pmids` and `source_anecdote_ids` after `sources` and `evidence_fragments` rows exist

**Column-by-column:**

| Legacy column | Disposition | Target | Notes |
|---|---|---|---|
| `id` | **Survives unchanged** | `interventions.id` | Already matches `INT-####` convention. |
| `name` | Survives | `interventions.name` | — |
| `category` | Survives | `interventions.category` | Legacy values observed (`drug`, `supplement`) are a subset of spec enum. Validate all 60 rows against spec enum `drug | supplement | food | diet | herb | lifestyle | environmental | generational | combo_seed | other`. |
| `directionality` | Survives | `interventions.directionality` | Legacy `treatment` is in spec enum. Validate all rows against `treatment | prevention | cause_mitigation | generational`. |
| `targets` | **Split** across `intervention_gene_edges`, `intervention_mechanism_edges`, and (rarely) `intervention_hypothesis_edges` | Multiple edge tables | Packed, mixed-ontology field. Observed examples mix gene symbols ("FOLR1"), mechanisms ("oxidative stress", "methylation cycle"), pathway names ("NRF2 pathway"), and receptor/transporter references. Each token must be classified. **Manual review required.** Raw original preserved in `interventions.targets_legacy`. |
| `mechanism_summary` | **Survives but demoted** | `interventions.mechanism_summary` (description only, per §6.1 "2–4 sentence summary derived from graph") | In the new world this field is **derived** from graph mechanisms; during migration it is imported as a placeholder and flagged for recomputation after mechanism extraction. Source of truth shifts to `intervention_mechanism_edges`. |
| `dose_range` | Survives | `interventions.dose_range` | — |
| `cost_per_month_usd` | Survives | `interventions.cost_per_month_usd` | — |
| `otc_or_rx` | Survives | `interventions.otc_or_rx` | Validate against spec enum. |
| `pediatric_safe` | Survives | `interventions.pediatric_safe` | Validate against spec enum. |
| `source_pmids` | **Forbidden in new schema.** Split into `sources` + `evidence_fragments` + `evidence_links(target_type='intervention', target_id=INT-####)`. | `evidence_links` | Preserved in `interventions.source_pmids_legacy` until the `studies` sheet is migrated and `sources` rows exist. |
| `source_anecdote_ids` | **Forbidden.** Same treatment via anecdote `sources`. | `evidence_links` | Preserved in `interventions.source_anecdote_ids_legacy`. |
| `csrs_score` | **Deprecated as input.** Hand-edited; violates §6.1 "computed only." | `interventions.csrs_score_legacy` (archival) | The live `interventions.csrs_score` must be re-derived from the Layer 1 graph (§7.2). Legacy value kept only for calibration diff reporting. |
| `csrs_last_updated` | Deprecated as input | `interventions.csrs_last_updated_legacy` | Live field is populated by the scoring engine. |
| `atlas_page_url` | **Not in spec.** | `interventions.notes` or dropped | Atlas URL is a UI concern. If retained, route to page-builder metadata, not to the core schema. |
| `notes` | Survives | `interventions.notes` | — |

**New/empty columns per spec §6.1:** `status`, `created_at`, `last_updated` are set during migration. `csrs_score` is null until the first scoring run.

**Data-quality / normalization issues:**

1. `targets` mixes entity types without a delimiter convention beyond semicolons. Cannot be auto-resolved.
2. Many `mechanism_summary` entries describe multiple mechanisms in one cell (e.g. "NRF2 pathway; oxidative stress; HSF1; mitochondrial function") — each becomes a separate row in `mechanisms` + `intervention_mechanism_edges`.
3. Legacy `csrs_score` values will differ from recomputed values; every delta belongs in `score_history` with a one-time "migration" evidence_delta note.
4. `source_pmids` and `source_anecdote_ids` can reference rows not present in the legacy `studies`/`anecdotes` sheets. Orphan FKs must be flagged rather than silently dropped.

---

### 3.3 `causes`

**Purpose (v0.1):** One row per hypothesized cause of autism, with hand-edited `evidence_strength` and `epidemiological_strength` on a 1–5 scale, a free-text `mechanism_summary`, packed `mitigation_intervention_ids`, and packed `source_pmids`.

**Maps to (Layer 1):**
- `hypotheses` (§4.1)
- `mechanisms` (§4.2) — via extraction from `mechanism_summary`
- `hypothesis_mechanism_edges` (§5.1) — via extraction
- `intervention_hypothesis_edges` (§6.3) — derived from `mitigation_intervention_ids`
- `sources` + `evidence_fragments` + `evidence_links` — derived from `source_pmids`
- `node_aliases` — preserve legacy `CAU-####` IDs as aliases of new `HYP-####` IDs

**Column-by-column:**

| Legacy column | Disposition | Target | Notes |
|---|---|---|---|
| `id` (`CAU-####`) | **Renamed / reprefixed** to `HYP-####` | `hypotheses.id` | Spec §4.1 requires `HYP-####`. Preserve `CAU-####` in `node_aliases` (spec §10.1). See Blocking Ambiguity #1 for the alternative. |
| `name` | Survives | `hypotheses.name` | Canonical name. |
| `category` | **Partially survives; requires remap.** Legacy values observed: `pharmacological`, `environmental`, `dietary`. Spec enum: `environmental | genetic | immune | metabolic | microbial | perinatal | behavioral | social | epigenetic | other`. | `hypotheses.category` | `environmental` maps directly. `pharmacological` and `dietary` are not in spec — **Blocking Ambiguity #2.** |
| `evidence_strength` (1–5) | **Deprecated.** Hand-edited; violates §4.1 "No hand-edited scores." | `hypotheses.evidence_strength_legacy` (archival) | Live `confidence_score` is computed from evidence (§7.1). |
| `affected_population` | **Not in spec.** | `hypotheses.notes` (short-term) or PROPOSED EXTENSION | Useful epidemiological context. **PROPOSED EXTENSION:** add `hypotheses.affected_population` (free text). Flagged, not silently added. |
| `mitigation_intervention_ids` | **Forbidden as packed FK.** Split to `intervention_hypothesis_edges` with `relation_type='cause_mitigation'` or spec-equivalent. | `intervention_hypothesis_edges` | Preserve raw in `hypotheses.mitigation_intervention_ids_legacy`. |
| `source_pmids` | **Forbidden.** Split to `sources` + `evidence_fragments` + `evidence_links(target_type='hypothesis')`. | `evidence_links` | Preserve in `hypotheses.source_pmids_legacy`. |
| `epidemiological_strength` (1–5) | **Deprecated.** Hand-edited. | `hypotheses.epidemiological_strength_legacy` (archival) | Becomes a *component* fed into `confidence_score` via evidence aggregates, not a column. |
| `mechanism_summary` | **Demoted.** | `hypotheses.description` and, in parallel, source material for `mechanisms` extraction | Each mechanism referenced becomes a row in `mechanisms` + an edge in `hypothesis_mechanism_edges`. Manual review required for all 30 rows. |
| `csrs_score` | **Dropped entirely.** Spec §4.1 has no CSRS on hypotheses. | `hypotheses.csrs_score_legacy` (archival only if retention is required) | Hypotheses use `confidence_score`, not CSRS. |
| `csrs_last_updated` | Dropped entirely | `hypotheses.csrs_last_updated_legacy` | — |
| `atlas_page_url` | Dropped / UI | `hypotheses.notes` or outside schema | — |
| `notes` | Survives | `hypotheses.notes` | — |

**New spec-required columns on `hypotheses`:** `description`, `status`, `confidence_score` (computed null-initial), `evidence_count` (computed), `evidence_quality_index` (computed), `consistency_index` (computed), `created_at`, `last_updated`.

**Data-quality / normalization issues:**

1. `category` enum mismatch on `pharmacological` and `dietary` is the first blocker.
2. `mechanism_summary` free text — 30 rows, but each can generate 2–5 `mechanisms` rows. Mechanism extraction must be deterministic (rule-based first per §8.3) with LLM fallback flagged.
3. `evidence_strength` and `epidemiological_strength` were hand-tuned. They cannot feed `confidence_score`. They can *calibrate* the scoring engine but only after-the-fact.
4. Some legacy rows have `mitigation_intervention_ids = None` (e.g. prenatal acetaminophen). These produce zero edges, not sentinel rows.
5. Row 1 ("FOLR1 autoantibodies / cerebral folate deficiency") is the calibration anchor — it must migrate cleanly and recover `confidence_score` high enough for leucovorin to still hit CSRS > 80 downstream.

---

### 3.4 `studies`

**Purpose (v0.1):** Literature inventory, one row per PMID. Includes direct FKs to one intervention and one cause per row, plus outcome/effect/p-value/replication fields.

**Maps to (Layer 1):**
- `sources` (§4.5) with `type='study'` or `type='review'` or `type='preprint'` based on `study_type`
- `evidence_fragments` (§4.6) — **one fragment per `studies` row by default**; more fragments may be added later when abstract/full-text mining produces multiple extractable results
- `evidence_links` (§5.5) — from `intervention_id`, `cause_id`, and (via mechanism extraction) to mechanisms/phenotypes
- `claims` (§4.7) — optional; recommended for RCTs and meta-analyses where the claim is normalizable

**Column-by-column:**

| Legacy column | Disposition | Target | Notes |
|---|---|---|---|
| `pmid` | **Renamed** to `sources.external_id` (with `platform='pubmed'`) | `sources.external_id` | Also mirrored in `sources.raw_metadata` JSON for convenience. `sources.id` is a new `SRC-######` PK. |
| `doi` | Survives as structured metadata | `sources.raw_metadata` JSON | No dedicated `doi` column in spec §4.5; raw_metadata is the canonical location. |
| `title` | Survives | `sources.title` | — |
| `authors` | Survives as metadata | `sources.raw_metadata` JSON | — |
| `year` | Survives; also informs `sources.date_published` | `sources.date_published` (year only → `YYYY-01-01` fallback with note), `raw_metadata.year` | — |
| `journal` | Metadata | `sources.raw_metadata` JSON | No dedicated column in spec. |
| `study_type` | **Renamed** to `sources.study_design` | `sources.study_design` | Legacy values observed: `rct`, `observational`, `case_series`, `review`, `meta_analysis`, `mechanistic`. `observational` is not in the spec enum — **Blocking Ambiguity #3.** |
| `n_subjects` | **Renamed** to `sources.sample_size` | `sources.sample_size` | Numeric, nullable. |
| `intervention_id` | **Split.** Direct FK becomes one row in `evidence_links(target_type='intervention', target_id=...)`. | `evidence_links` | Preserve in `evidence_fragments.structured_payload.legacy_intervention_id`. In addition, on any `intervention_mechanism_edge` that extraction produces, the same fragment should link as supporting/contradicting evidence per §5.5. |
| `cause_id` | **Split.** Direct FK becomes `evidence_links(target_type='hypothesis', target_id=HYP-####)` (after CAU→HYP remap). | `evidence_links` | Same pattern as above. |
| `outcome` | Survives | `evidence_fragments.text_excerpt` or `structured_payload.outcome` | Free-text. Prefer `structured_payload.outcome` when parseable. |
| `effect_size` | Survives | `evidence_fragments.structured_payload.effect_size` | Free-text in legacy (mixes Cohen's d, %, raw deltas) — preserved as a string but parsed to numeric when possible. |
| `p_value` | Survives | `evidence_fragments.structured_payload.p_value` | Often a string (`<0.001`). Keep as string + parsed numeric when possible. |
| `replicated` | Survives | `evidence_fragments.structured_payload.replicated` | Legacy values `yes | partial | unknown | no`. Informs `consistency_index` and `evidence_quality_index` but is not itself a score. |
| `abstract` | Survives | `sources.raw_metadata.abstract` and/or `evidence_fragments.text_excerpt` | Prefer `raw_metadata.abstract` for the full text and copy an extractive excerpt (≤ spec length limit) into `evidence_fragments.text_excerpt`. |
| `full_text_url` | Survives | `sources.url` | Canonical URL. |

**Derived fields that the migration must populate on each `evidence_fragments` row:**

- `fragment_type` — `result` for RCTs/observational with an outcome; `mechanism` for `study_type='mechanistic'`; `review` collapses into a single fragment with `fragment_type='result'` and `strength_score` downweighted.
- `effect_direction` — inferred from `outcome` + `effect_size` + `p_value`. Rule-based first; LLM-assisted fallback is flagged in `extraction_method`.
- `strength_score` — deterministic function of `study_design`, `sample_size`, `replicated`, source type, registry robustness per §7.1. Not a hand number.
- `extraction_method` — `rule_based` for structured fields; `llm_assisted` for `outcome` parsing fallback.
- `extraction_confidence` — per-field; low when abstract-only.
- `date_extracted` — set at migration time.

**Data-quality / normalization issues:**

1. `study_type='observational'` appears on **313 of 778 rows** — the single largest study_type bucket — and is not in the spec enum. Must be classified as `cohort` vs `case_control` or routed to `other` with a structured note.
2. `study_type='review'` (356 rows) — reviews are valid sources but should not contribute independent evidence weight in scoring; `strength_score` must reflect this.
3. **667 rows (778 − 110 − 21) have only one of `intervention_id` or `cause_id` populated**, and **21 rows have neither.** Those 21 are orphan literature with no direct Layer 1 link and must either be deferred or linked via abstract mining.
4. Row 100 is a clear near-duplicate of row 5 (Hendren 2016 methyl-B12, different PMID and slightly different title). Real-world dedup is required; `statement_hash` on `claims` will help later but does not fire automatically at the `sources` level.
5. `effect_size` format is inconsistent: Cohen's d, percent change, prevalence ratios, raw deltas, and free-text descriptions are all represented. No automatic numeric normalization is safe.
6. `replicated='unknown'` is very common (especially rows ≥100) — these cannot be treated as `no` or `yes`; they must map to a `null`-equivalent and downweight `consistency_index` appropriately.
7. No `sources.platform` or `sources.type` in the legacy — must be assigned (`platform='pubmed'` by default, `type='study'` / `'review'` / `'meta_analysis'` derived from `study_type`).

---

### 3.5 `anecdotes`

**Purpose (v0.1):** Bottom-up evidence. One row per Reddit thread or YouTube video, with a single intervention FK or cause FK, a reporter population, a reported outcome, an engagement count, and two derived booleans.

**Maps to (Layer 1):**
- `sources` (§4.5) with `type='anecdote'` or `type='social'`
- `evidence_fragments` (§4.6) — one fragment per anecdote row, with low default `strength_score`
- `evidence_links` (§5.5)

**Column-by-column:**

| Legacy column | Disposition | Target | Notes |
|---|---|---|---|
| `id` (`ANE-####`) | **Preserved as alias.** New PK is `SRC-######`. | `sources.id` (new), `node_aliases` row recording old `ANE-####` | Many `evidence_pointers` in `csrs_components` refer to `ANE-####` — the alias table is load-bearing. |
| `source` (`reddit | youtube`) | **Renamed** to `sources.platform` | `sources.platform` | Legacy values map 1:1 (`reddit`, `youtube`). |
| `url` | Survives | `sources.url` | — |
| `date_iso` | **Renamed** to `sources.date_published` | `sources.date_published` | Some rows lack this (YouTube row 300 has no `date_iso`); permit null. |
| `intervention_id` | **Split** to `evidence_links(target_type='intervention')` | `evidence_links` | Preserve in `evidence_fragments.structured_payload.legacy_intervention_id`. |
| `cause_id` | **Split** to `evidence_links(target_type='hypothesis')` | `evidence_links` | Same. |
| `reporter_population` (`parent | patient | clinician | researcher | unknown`) | Survives as context | `evidence_fragments.structured_payload.reporter_population` and/or `evidence_links.context_scope` | 205 of 520 rows are `unknown` — they enter the graph at the lowest `strength_score` tier. |
| `reported_outcome` (`positive | negative | null | mixed`) | **Renamed** to `evidence_fragments.effect_direction` with value remap (`null` → `neutral`) | `evidence_fragments.effect_direction` | Spec §4.6 enum uses `neutral`, not `null`. |
| `engagement` | Survives as metadata | `evidence_fragments.structured_payload.engagement_count` | Informs `strength_score` at a low weight per §7.2 "social signals with low base weight." |
| `mechanism_match` (bool) | **Demoted.** Derived claim without explicit provenance. | `evidence_fragments.structured_payload.legacy_mechanism_match` (archival) | Do not use in scoring in the new schema; mechanism linkage must be via explicit `evidence_links` to a mechanism node. Manual review on `True` values to decide whether to materialize a real edge. |
| `contradicting_literature` (bool) | **Demoted.** Same reasoning. | `evidence_fragments.structured_payload.legacy_contradicting_literature` | If true, the fragment's `effect_direction` may still be `positive` for the intervention while `effect_direction` vs. a *hypothesis* is `contradicting` — the two are distinct per target_type. |
| `raw_text_excerpt` | Survives | `evidence_fragments.text_excerpt` | Often very short (the thread title). Strength downweighted accordingly. |
| `notes` | Survives | `evidence_fragments.notes` or `sources.notes` | — |

**Data-quality / normalization issues:**

1. `raw_text_excerpt` is often just the title of the Reddit/YouTube thread, not the content. `strength_score` must be floored low unless the fragment is expanded with body text.
2. `engagement` on YouTube (view counts, e.g. 119,479) vs. Reddit (comment counts, e.g. 144) is not normalized. Cannot be compared cross-platform without platform-specific bucketing.
3. `reported_outcome='positive'` on 495/520 rows is a strong selection bias; scoring must not treat the anecdote set as representative.
4. `mechanism_match` and `contradicting_literature` were generated by unspecified heuristics and cannot be trusted as evidence for or against mechanisms.
5. The legacy `ANE-####` IDs are referenced by both `interventions.source_anecdote_ids` and `csrs_components.evidence_pointers` — the alias map must be in place **before** those FKs are resolved.

---

### 3.6 `combinations`

**Purpose (v0.1):** Explicit combos of interventions, pre-scored with CSRS and flagged for safety.

**Maps to (Layer 2):**
- `combinations` (§6.6)
- `combination_members` (§6.7)

**Column-by-column:**

| Legacy column | Disposition | Target | Notes |
|---|---|---|---|
| `id` (`CMB-####`) | Survives | `combinations.id` — **proposed prefix remap to `COM-####`** per spec §6.6 | **Blocking Ambiguity #4:** Spec example uses `COM-0001`; legacy uses `CMB-0001`. Either remap IDs or change spec example. Preserve `CMB-####` in `node_aliases`. |
| `name` | Survives | `combinations.name` | — |
| `member_intervention_ids` | **Forbidden as packed FK.** Split to `combination_members` rows. | `combination_members` | Preserve in `combinations.member_intervention_ids_legacy`. Row 3 (`CMB-0003`, GFCF combo) has `None` — combination with zero members is a data-quality flag. |
| `rationale` | Survives | `combinations.rationale` | — |
| `evidence_summary` | **Not in spec.** | `combinations.description` (via concatenation) or `combinations.notes` | Prose; the underlying claims should be reified as evidence on the *member* interventions' edges, not on the combo itself. |
| `interaction_warnings` | **Not in spec.** Safety-relevant. | PROPOSED EXTENSION | **PROPOSED EXTENSION:** add `combinations.interaction_warnings` as free text, given safety implications. Flagged, not silently added. |
| `csrs_score` | **Deprecated as input.** | `combinations.csrs_score_legacy` | Live value recomputed from members per §7.2 "combination synergy where applicable." |
| `csrs_last_updated` | Deprecated as input | `combinations.csrs_last_updated_legacy` | — |
| `atlas_page_url` | Dropped / UI | outside schema | — |
| `notes` | Survives | `combinations.notes` | — |

**Data-quality / normalization issues:**

1. Row `CMB-0003` has `member_intervention_ids = None` — a combo with no members. Either the combo was under-specified or the intervention rows are missing. Manual review.
2. `evidence_summary` and `interaction_warnings` may reference PMIDs/ANE-IDs in free text. Any such references must be surfaced into proper `evidence_links` on member edges, not left as prose.
3. Legacy `csrs_score` is null on all four combos (per spec already). That's convenient — no archival value to defend.

---

### 3.7 `phenotypes`

**Purpose (v0.1):** Autism subtypes, each with diagnostic markers, prevalence, and packed `top_intervention_ids` and `top_cause_ids`.

**Maps to (Layer 1):**
- `phenotypes` (§4.3)
- `mechanism_phenotype_edges` (§5.2) — populated via later extraction, not from this sheet directly
- The `top_intervention_ids` and `top_cause_ids` fields are explicitly **forbidden in core** by spec §4.3: *"No direct `top_intervention_ids` or `top_cause_ids` fields in core. Those belong in derived views or Layer 2 tables."*

**Column-by-column:**

| Legacy column | Disposition | Target | Notes |
|---|---|---|---|
| `id` (`PHE-####`) | Survives | `phenotypes.id` | Matches spec. |
| `name` | Survives | `phenotypes.name` | — |
| `diagnostic_markers` | Survives as plain text | `phenotypes.diagnostic_markers` | Spec §4.3 note: "structured markers may move to a `biomarkers` table later." Not in scope here. |
| `prevalence_estimate` | Survives | `phenotypes.prevalence_estimate` | Mixed formatting (`"~10-25% of cases"`, `"~30-50%..."`, free text). Preserve as-is. |
| `top_intervention_ids` | **Dropped from core.** | `phenotypes.top_intervention_ids_legacy` only. Live view recomputed from graph. | Per spec §4.3, hard stop. The 5-item ranked list in PHE-0001, for example, cannot survive. |
| `top_cause_ids` | **Dropped from core.** | `phenotypes.top_cause_ids_legacy` only. | Same. |
| `phenotype_description` | **Renamed** to `phenotypes.description` | `phenotypes.description` | Spec uses `description`. |
| `atlas_page_url` | Dropped / UI | outside schema | — |
| `notes` | Survives | `phenotypes.notes` | — |

**New spec-required columns on `phenotypes`:** `status`, `created_at`, `last_updated`.

**Data-quality / normalization issues:**

1. PHE-0007 (`GABA/Cl- imbalance phenotype`) has `top_cause_ids = None` but a `top_intervention_ids` list — in the new schema, the intervention list is gone, and the phenotype has no cause edges from this sheet. It will rely on downstream mechanism edges.
2. Multiple legacy phenotype rows reference interventions (`INT-####`) and causes (`CAU-####`) without any explicit polarity or evidence. These semicolon lists are claims *without* provenance, which is exactly what the new schema forbids.
3. The legacy phenotype set (7 rows) is sparse. Mechanism → phenotype edges must be built out in a later step, not populated from this sheet.

---

### 3.8 `genes`

**Purpose (v0.1):** Genetic layer. 1,564 rows, seeded from SFARI + OpenTargets. Uses `gene_symbol` as the natural key. Includes packed FKs to phenotypes and interventions.

**Maps to (Layer 1):**
- `genes` (§4.4)
- `gene_mechanism_edges` (§5.3) — populated via later annotation (KEGG/Reactome/OpenTargets)
- `gene_hypothesis_edges` (§5.4, optional) — populated via later annotation
- `intervention_gene_edges` (§6.5) — from `linked_intervention_ids`
- **`gene_phenotype_edges`** — not in spec. See PROPOSED EXTENSION below.

**Column-by-column:**

| Legacy column | Disposition | Target | Notes |
|---|---|---|---|
| (implicit) gene PK | **Added.** Assign `GEN-####` at migration. | `genes.id` | Legacy uses `gene_symbol` as key. Preserve symbol as the natural unique key alongside the new PK. |
| `gene_symbol` | Survives | `genes.gene_symbol` | — |
| `ensembl_id` | Survives | `genes.ensembl_id` | — |
| `sfari_score` | Survives | `genes.sfari_score` | Legacy values include integers (`1`,`2`,`3`), `S`, and nulls for OpenTargets-only rows. Matches spec enum `1 | 2 | 3 | S | NA`; treat missing as `NA`. |
| `evidence_strength` (1–5) | **Renamed** to `genes.genetic_evidence_strength` | `genes.genetic_evidence_strength` | Spec §4.4 explicitly allows this as an `int 1–5`. This is the one place a numeric 1–5 integer is spec-sanctioned. |
| `associated_phenotype_ids` | **Forbidden as packed FK.** No edge table in spec links genes to phenotypes directly. | `genes.associated_phenotype_ids_legacy` only, or PROPOSED EXTENSION | **Blocking Ambiguity #5 / PROPOSED EXTENSION:** either add `gene_phenotype_edges` to the spec, or require all gene→phenotype claims to be routed via `gene_mechanism_edges` + `mechanism_phenotype_edges`. Not silently resolved. |
| `linked_intervention_ids` | **Forbidden as packed FK.** Split into `intervention_gene_edges`. | `intervention_gene_edges` | Preserve in `genes.linked_intervention_ids_legacy`. |
| `function_summary` | Survives | `genes.function_summary` | — |
| `opentargets_score` | Survives | `genes.opentargets_score` | External-system score; spec §4.4 explicitly allows it. |
| `notes` | Survives | `genes.notes` | Often carries SFARI category ("Rare Single Gene Mutation", "…Functional") and report counts — worth preserving verbatim. |

**New spec-required columns on `genes`:** `gnomad_notes`, `disgenet_score`, `created_at`, `last_updated`.

**Data-quality / normalization issues:**

1. Gene rows without `associated_phenotype_ids` or `linked_intervention_ids` (the vast majority past row ~50) are purely descriptive. That's fine — they sit in the table as candidates, with edge tables empty until real evidence arrives.
2. 1,564 gene rows is large enough that a uniqueness check on `gene_symbol` + `ensembl_id` is mandatory before assigning `GEN-####` PKs.
3. `opentargets_score` is external-source; its provenance belongs in `sources` (type='dataset', platform='opentargets') + `evidence_fragments`. For the migration, the numeric can survive on the gene row per spec, but a matching source artifact should also be recorded for auditability (§1.6).
4. Legacy row 5 (`MECP2`) has no `associated_phenotype_ids` and no linked intervention but is a top-tier gene. That's fine — it carries no edges in the migrated output.

---

### 3.9 `csrs_components`

**Purpose (v0.1):** Per-(intervention, component) breakdown with hand-edited `weight_pct`, `raw_score_0_100`, and `weighted_contribution`. This is the backing store for legacy `interventions.csrs_score`.

**Maps to:** **Nothing in the new data schema.** The whole sheet is a legacy artifact that violates §6.1, §7.1, and §7.2.

- `weight_pct` values become **scoring engine config seeds** — *not data* — living outside the schema per §7.1 "these live in config and can be tuned."
- `raw_score_0_100` values are discarded; they are the hand-edited scores the spec explicitly forbids.
- `evidence_pointers` are the only salvageable column. Each pointer (PMID, ANE-ID, gene symbol, mechanism name, combo ID, or free text like `"Frye + Ramaekers + multiple sites"`) must be re-expressed as a proper `evidence_links` row — or flagged as unresolvable.
- `computed_at_iso` becomes irrelevant (the scoring engine stamps `score_history.computed_at`).
- `notes` follow the pointers as annotations on the resulting `evidence_links` rows.

**Column-by-column:**

| Legacy column | Disposition | Target | Notes |
|---|---|---|---|
| `intervention_id` | Survives as the subject of resulting edges/links | `evidence_links.target_id` (target_type='intervention') or edge rows | — |
| `component` | **Demoted to config label.** | Scoring engine config (CSRS component taxonomy) | Legacy has 12 components (e.g. "PubMed Literature Strength", "Anecdotal Consistency (Reddit + X via Grok + YouTube)", "Mechanism + Biology Coherence"). Spec §7.2 implies a different component breakdown derived from graph aggregates. See Blocking Ambiguity #6. |
| `weight_pct` | **Demoted to config seed.** | Scoring engine config | Not data. |
| `raw_score_0_100` | **Discarded.** | — | Hand-edited; forbidden by §6.1 and §7.2. |
| `weighted_contribution` | **Discarded.** | — | Derived from discarded inputs. |
| `evidence_pointers` | **Split and resolved** into `evidence_links` where possible | `evidence_links` | Manual review on every row whose pointers are not resolvable IDs (e.g. "FOLR1 autoantibodies" text, "Functional med community adoption"). |
| `computed_at_iso` | Discarded | — | The scoring engine sets its own timestamps. |
| `notes` | Survives as annotation on resulting `evidence_links.notes` | `evidence_links.notes` | — |

**Data-quality / normalization issues:**

1. Only 11/60 interventions have CSRS component rows — a decisive signal that the legacy CSRS was never completed across the board. Any migration that treats `csrs_components` as authoritative for those 11 will falsely outrank the other 49.
2. `evidence_pointers` contains a heterogeneous mix: PMIDs (`30097774`), anecdote IDs (`ANE-0001`), gene symbols (`FOLR1`), combo IDs (`CMB-0001`), mechanism names (`"NRF2 pathway"`), descriptive phrases (`"Multi-team replication"`), and sentinel values (`"n/a"`). No deterministic resolver will catch all of them.
3. The 12 legacy components don't align 1:1 with the spec §7.2 scoring dimensions. A component map must be produced before the scoring engine is even written. This is config work, not data work, and is out of scope for the schema migration.

---

## 4. Manual Review Queue

The following kinds of rows will need a human in the loop before or during migration. Ordered by criticality.

1. **Anecdotes with `reporter_population='unknown'` (205 rows).** Default `strength_score` floor; confirm or reclassify per thread.
2. **Anecdotes with `mechanism_match=True` or `contradicting_literature=True` (hundreds).** Decide whether to materialize real `evidence_links` to a mechanism or hypothesis, or leave as legacy-only.
3. **YouTube anecdotes missing `date_iso`.** Check whether the platform-side date is recoverable before migration closes the source row.
4. **Anecdotes whose `raw_text_excerpt` is just a title.** Body text or transcript needed before the fragment is scoring-worthy.
5. **Intervention `targets` column — every non-null row (≥50).** Each semicolon-packed cell mixes genes, mechanisms, pathways, and receptors. Token-by-token classification is required before any `intervention_*_edges` rows are written.
6. **Intervention and cause `mechanism_summary` free text (60 + 30 rows).** Mechanism extraction per §8.3 — rules first, LLM fallback flagged. Every extracted mechanism that becomes a new `mechanisms` row needs a canonical name to avoid duplicate nodes.
7. **Causes with `category='pharmacological'` or `'dietary'` (at least 3 observed: CAU-0001, CAU-0002, CAU-0003).** Remap required per Blocking Ambiguity #2.
8. **Studies with `study_type='observational'` (313 rows).** Re-classify to `cohort` or `case_control` or route to `other` per Blocking Ambiguity #3.
9. **Studies with only `intervention_id` and no `cause_id` (491 rows) or vice versa (156 rows).** Decide whether to mine the abstract for the missing linkage or defer.
10. **Studies with neither `intervention_id` nor `cause_id` (21 rows).** Orphan literature — abstract mining required, or mark deferred.
11. **Studies with near-duplicate titles (e.g. the two 2016 Hendren methyl-B12 entries at rows 5 and 100).** Source-level dedup.
12. **Phenotype `top_intervention_ids` / `top_cause_ids` (all 7 rows).** These lists must be *explained* by evidence before any derived view reproduces them. They imply mechanism/hypothesis edges that do not exist in the current data.
13. **Combination `CMB-0003`** with empty `member_intervention_ids`. Either populate or deprecate.
14. **Genes with `associated_phenotype_ids` (small subset, but all of them).** Each must be routed either via the PROPOSED EXTENSION `gene_phenotype_edges` or through a mechanism chain; cannot be silently dropped.
15. **`csrs_components.evidence_pointers` rows with non-ID content (prose pointers).** Manual sourcing or drop with a logged reason.
16. **Intervention-first legacy artifacts that don't fit Layer 1.** For instance, an intervention whose only legacy provenance is `notes` text with no PMIDs and no anecdote IDs — it will sit in the new schema with zero evidence edges. Flag and decide: keep as low-confidence stub, or deprecate.

---

## 5. Migration Order of Operations

Each step is sequenced so that foreign keys resolve cleanly and no step depends on data the next step will produce.

1. **Freeze legacy snapshot.** Archive `causes_atlas_schema_v0.1.xlsx` with a checksum. Every later step references it read-only.
2. **Stand up empty new schema.** Create all spec §4–§6 tables plus `score_history`, `node_aliases`, and `*_legacy` columns on every migrated table. No rows yet.
3. **Migrate `phenotypes`.** No FKs to other new tables required. `top_*_ids` go to `*_legacy` only.
4. **Migrate `genes` (descriptive rows only).** Assign `GEN-####` PKs. Populate descriptive columns. Do not yet write `intervention_gene_edges` or any phenotype link.
5. **Migrate `hypotheses` (from `causes`).** Reprefix `CAU-####` → `HYP-####`, write alias rows. Remap `category` where unambiguous; park the ambiguous ones on a "needs review" queue but still load the row. Populate `*_legacy` columns. Do not yet create `mechanisms` or edges.
6. **Migrate `interventions` (header fields only).** Populate everything except `targets`, `source_pmids`, `source_anecdote_ids`, and `csrs_score` (which stays null). Preserve all four in `*_legacy` columns.
7. **Migrate `sources` from `studies`.** One `SRC-######` row per `studies` row; remap `study_type` → `study_design`; route abstract to `raw_metadata`; flag `observational` rows.
8. **Migrate `sources` from `anecdotes`.** One `SRC-######` row per `anecdotes` row; set `type='anecdote'` or `type='social'`; record alias `ANE-####`.
9. **Build `evidence_fragments`** — one default fragment per source row from steps 7 and 8. Populate `effect_direction` (with `null`→`neutral` remap for anecdotes), `strength_score` deterministically per §7.1, `extraction_method`, `extraction_confidence`.
10. **Build `evidence_links` from explicit legacy FKs.** For each `studies` row with a non-null `intervention_id`, write `evidence_links(target_type='intervention', target_id=...)`. Same for `cause_id` → `hypothesis`. Same for anecdotes.
11. **Extract `mechanisms` from `causes.mechanism_summary` and `interventions.mechanism_summary`.** Rule-based first (vocabulary match on oxidative stress, neuroinflammation, methylation, BBB, microglia, GABA/glutamate, gut-brain, mTOR, etc.); LLM fallback flagged in `evidence_fragments.extraction_method`. Create `mechanisms` rows; dedupe by canonical name; write `node_aliases` for variants.
12. **Build `hypothesis_mechanism_edges`** for each extracted mechanism from step 11's cause-side extraction; `evidence_links` point at the edge (via `target_type='hypothesis_mechanism_edge'`).
13. **Parse `interventions.targets` and build `intervention_mechanism_edges` + `intervention_gene_edges`.** Manual review gate — no automatic classification for ambiguous tokens.
14. **Build `intervention_hypothesis_edges`** from `causes.mitigation_intervention_ids` with `relation_type='cause_mitigation'` (spec §6.1 directionality enum already has the concept).
15. **Migrate `combinations` + `combination_members`** by splitting `member_intervention_ids`. Preserve `interaction_warnings` pending Blocking Ambiguity #7 / PROPOSED EXTENSION resolution.
16. **Process genes' packed FKs.** Write `intervention_gene_edges` from `linked_intervention_ids`. Park `associated_phenotype_ids` per Blocking Ambiguity #5.
17. **Resolve `csrs_components.evidence_pointers`** into `evidence_links` where possible. Everything unresolvable goes to a migration exception log.
18. **Run the deterministic scoring engine.** Populate `confidence_score` on hypotheses, `evidence_strength` on mechanisms, `csrs_score` on interventions and combinations, and write initial `score_history` rows.
19. **Run the calibration test.** Assert leucovorin's `csrs_score > 80` from Layer 1 aggregates alone. If it doesn't hit the threshold, the failure is a scoring-engine or evidence-coverage bug, not a migration bug — but it must be investigated before publication (per README).
20. **QA sweep.**
    - Orphan FK check: every `*_id` referenced in legacy semicolon fields that couldn't be resolved.
    - Null `evidence_links` on any hypothesis / mechanism / edge — flag as zero-evidence and set `status='tentative'` where the spec permits.
    - Duplicate detection on `sources.external_id` (PMID, URL), `hypotheses.name`, `mechanisms.name`, `genes.gene_symbol`.
    - Verify no semicolon characters appear in any new-schema FK column.
    - Verify no hand-edited score survives in a live column (all must be in `*_legacy`).
21. **Lock the migration.** Tag the migration run with a version id; store the exception log; make it reproducible.

---

## 6. Blocking Ambiguities

These must be resolved by the spec owner before the migration is safe to execute. Listed explicitly rather than silently resolved.

1. **Legacy `CAU-####` IDs vs. spec `HYP-####` IDs.** Option A: reprefix during migration, preserve old IDs in `node_aliases`. Option B: extend the spec to allow `CAU-####` as an alternative legal prefix. **Default recommendation:** Option A, because spec §4.1 is explicit; but any downstream system currently dereferencing `CAU-####` (e.g. `studies.cause_id`, `anecdotes.cause_id`) must be rewritten at migration time. Decision required.

2. **`causes.category` values `pharmacological` and `dietary` are not in the spec `hypotheses.category` enum (§4.1).** Spec enum: `environmental | genetic | immune | metabolic | microbial | perinatal | behavioral | social | epigenetic | other`. `pharmacological` could be routed to `other` with a note, or the enum could be extended. `dietary` could map to `behavioral`, `environmental`, or `other`. Not silently resolved.

3. **`studies.study_type='observational'` (313 rows) is not in the spec `sources.study_design` enum (§4.5).** Spec enum is: `rct | cohort | case_control | case_series | mechanistic | meta_analysis | review | animal | in_vitro | in_silico | epigenetic | transgenerational | other`. Split into `cohort` vs `case_control` requires per-row judgment. Default-to-`other` is safe but lossy. Decision required.

4. **`combinations` ID prefix.** Legacy `CMB-####` vs. spec `COM-####` (§6.6 example). Same choice as Ambiguity #1. Default recommendation: reprefix.

5. **Gene → phenotype relation has no spec edge table.** Spec has `gene_mechanism_edges` and optional `gene_hypothesis_edges`, but no `gene_phenotype_edges`. Legacy `genes.associated_phenotype_ids` semicolon lists imply direct gene→phenotype relations. **PROPOSED EXTENSION:** add `gene_phenotype_edges` with the standard (id, gene_id, phenotype_id, relation_type, evidence fields, status, timestamps) shape. Alternative: require every legacy gene→phenotype claim to be rerouted through a mechanism chain, which may lose fidelity. Decision required.

6. **CSRS component taxonomy.** Legacy `csrs_components` uses 12 components ("PubMed Literature Strength", "Anecdotal Consistency (Reddit + X via Grok + YouTube)", "Mechanism + Biology Coherence", "Genetic / Target Evidence", "Combination Synergy", "Epigenetic / Generational / Long-Term", "Trend / Emerging Signal (Grok-powered)", "In-Silico Functional Support", "Replication / Independence", "Safety & Practicality", "Clinical Trial Signals" — plus one gap). Spec §7.2 implies a different breakdown ("Which hypotheses they target", "strength of those hypotheses and mechanisms", "evidence of effect on phenotypes", "genetic coherence", "safety/practicality", "trend/emerging signals", "combination synergy"). A canonical mapping from legacy → spec components must be authored as scoring-engine config before CSRS can be recomputed deterministically. Decision required.

7. **`combinations.interaction_warnings` has no home in the spec.** Safety-critical field. **PROPOSED EXTENSION:** add `combinations.interaction_warnings` as free text. Not silently added. Decision required.

8. **`causes.affected_population` has no home in the spec.** Useful epidemiological context. **PROPOSED EXTENSION:** add `hypotheses.affected_population` as free text. Decision required.

9. **`studies.replicated` has no dedicated spec column.** Landing it in `evidence_fragments.structured_payload.replicated` is spec-legal but makes replication status harder to aggregate. Optional **PROPOSED EXTENSION:** a `sources.replicated` or `evidence_fragments.replicated` column. Lower priority; documenting only. Decision optional.

10. **`anecdotes.reported_outcome='null'` (3 rows) vs. spec `evidence_fragments.effect_direction` enum `neutral`.** The mapping is obvious (`null` → `neutral`) but must be formally blessed so downstream systems don't reintroduce `null` as a valid label.

11. **Intervention `atlas_page_url` and phenotype / cause / combo equivalents.** Not in spec. Decision: drop from schema, route to page-builder metadata outside the schema. Confirm.

12. **`csrs_components` rows referencing interventions *not* yet in the `interventions` sheet.** Observed sample shows 11/60 covered; verification needed that no `intervention_id` in `csrs_components` is orphaned against `interventions`. If orphans exist, they indicate the legacy sheet is internally inconsistent. Decision required on how to handle orphans.

---

## 7. Audit Trail Requirements for This Migration

Per spec §1.6, §9.2, and §10.2, the migration itself must be auditable. The execution plan should generate, at minimum:

- a migration run ID (timestamped),
- a checksummed archive of the legacy workbook,
- a per-row mapping log (legacy row → new row(s) → any `*_legacy` preservations),
- an exception log for every unresolved pointer, unclassified `targets` token, orphan FK, and manual-review flag,
- a `score_history` entry for every node whose score changes from a legacy hand-edited value to a computed value, with `evidence_delta_ids` listing the evidence that drove the recomputation,
- a `node_aliases` load for every legacy ID whose prefix changes (`CAU-####` → `HYP-####`, `ANE-####` → `SRC-######`, and if agreed `CMB-####` → `COM-####`).

No migration step should overwrite data without an entry in one of the above logs.

---

## 8. What This Plan Does Not Do

- Does not modify the canonical spec.
- Does not generate code.
- Does not execute migration steps.
- Does not resolve any Blocking Ambiguity silently.
- Does not define the scoring engine's weights or formulas — only identifies where legacy scoring must be discarded or demoted to config seeds.
- Does not decide the fate of legacy `atlas_page_url` fields beyond noting that they are out of scope for the canonical schema.

This plan is the input to a second document (implementation script + config) and a third document (scoring engine spec). Both are out of scope here.

---

**End of MIGRATION_PLAN.md.**
