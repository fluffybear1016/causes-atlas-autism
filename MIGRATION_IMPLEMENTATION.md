# MIGRATION IMPLEMENTATION PLAN

**Binding documents:**
- `CAUSES_ATLAS_AUTISM_SPEC_v1.1.md` (canonical)
- `MIGRATION_PLAN.md` (migration constraints)
- `causes_atlas_schema_v0.1.xlsx` (legacy source, read-only)
- Schema headers already generated for all target tables

**Scope:** Prose-level execution blueprint. No code. No spec changes. The output of this plan is a deterministic, per-row mapping recipe that someone can mechanically translate into Python, Apps Script, or SQL.

---

## 1. Overall Migration Order

Twenty-one steps, ordered so every foreign key resolves at the moment it is written, and so every hand-edited score is demoted before any computed score is materialized. This restates §5 of `MIGRATION_PLAN.md`.

1. **Freeze legacy snapshot.** Archive `causes_atlas_schema_v0.1.xlsx` with a SHA-256 checksum; record checksum, filename, file size, and archive path in the migration audit record. All subsequent reads go through the archived copy.
2. **Stand up empty new schema.** Create every target tab from the generated schema headers. Zero rows. Confirm every live column and every `*_legacy` column is present on the right tab.
3. **Scaffold `node_aliases`.** Create the table and wire it so that every later step that assigns a new canonical ID or changes a prefix writes a matching alias row in the same transaction.
4. **Migrate `phenotypes`.** No FKs to other new tables. `top_*_ids` are routed into `*_legacy` columns only.
5. **Migrate `genes` (descriptive pass).** Assign `GEN-####` PKs. Descriptive columns only. No edges yet. Packed FK columns go into `*_legacy` only.
6. **Migrate `hypotheses` (from `causes`).** Reprefix `CAU-####` → `HYP-####`, write aliases. Remap `category` per spec §4.1 (pharmacological/dietary → other; preserve raw in `category_legacy`). Park all packed FKs in `*_legacy`.
7. **Migrate `interventions` (header pass).** Copy scalar fields; park `targets`, `source_pmids`, `source_anecdote_ids`, legacy `csrs_score`, and legacy `csrs_last_updated` in `*_legacy`. Leave live `csrs_score` null.
8. **Migrate `sources`** — one row per legacy `studies` row and one row per legacy `anecdotes` row. Remap `study_type` → `study_design` (observational → other; preserve raw in `raw_metadata.legacy_study_type`).
9. **Build `evidence_fragments`** — one default fragment per source.
10. **Build `evidence_links` from direct legacy FKs** on studies and anecdotes (`intervention_id`, `cause_id`). Effect direction normalized per spec §4.6 (legacy `null` → `neutral`).
11. **Extract `mechanisms`** from `causes.mechanism_summary` and `interventions.mechanism_summary`. Rules-first, LLM fallback flagged. Dedupe by canonical name; register variants in `node_aliases`.
12. **Build `hypothesis_mechanism_edges`** from the cause-side extraction.
13. **Build `intervention_mechanism_edges`** from the intervention-side extraction, **plus** from `interventions.targets` tokens classified as mechanisms/pathways. Manual review gate.
14. **Build `intervention_hypothesis_edges`** from `causes.mitigation_intervention_ids` (packed FKs parsed, `relation_type='cause_mitigation'`).
15. **Migrate `combinations`** and **`combination_members`.** Reprefix `CMB-####` → `COM-####`; write aliases; split packed member IDs; preserve raw in `*_legacy`.
16. **Build `gene_phenotype_edges`** from `genes.associated_phenotype_ids` (parsed from packed field; raw preserved in `genes.associated_phenotype_ids_legacy`).
17. **Build `intervention_gene_edges`** from `genes.linked_intervention_ids` **plus** from `interventions.targets` tokens classified as gene symbols.
18. **Resolve `csrs_components.evidence_pointers`** into `evidence_links` where the pointer is a resolvable ID; non-ID pointers (prose, sentinel values) go to the unresolved-pointer log.
19. **Run the deterministic scoring engine** once. This is not a data-migration step; it is the first computation pass over the freshly migrated graph. It writes live values into `confidence_score`, `evidence_strength`, `evidence_strength_aggregate`, `csrs_score`, `strength_score`, and emits `score_history` migration-delta rows per §3.22 below.
20. **Calibration test.** Assert leucovorin (`INT-0001`) `csrs_score ≥ 80` from Layer 1 aggregates alone. Failure is a scoring-engine or coverage bug, not a migration bug, and must be triaged before publication — per the v0.1 README.
21. **QA sweep + lock.** Orphan FK check, null-evidence node flagging, duplicate detection, semicolon-in-live-column detection, hand-score-in-live-column detection. Tag the migration run ID; freeze all logs; make it reproducible.

Tables that remain empty or near-empty after step 21 — `gene_mechanism_edges`, `gene_hypothesis_edges`, `mechanism_phenotype_edges`, `intervention_phenotype_edges`, most of `claims` — are populated in subsequent ingestion passes, not in this migration.

---

## 2. Nulls and Defaults

Global conventions applied uniformly across every table.

**Computed scores — always null on first migration.** Every live `confidence_score`, `evidence_strength`, `evidence_strength_aggregate`, `csrs_score`, `strength_score`, `evidence_count`, `evidence_quality_index`, `consistency_index`, `evidence_for_count`, `evidence_against_count`, `extraction_confidence` field is written as `null` (or left blank) by migration steps 3–18. These fields are populated exclusively by the scoring engine in step 19.

**Timestamps.**
- `created_at` = the migration run timestamp (single ISO-8601 UTC value assigned once at the start of the run, reused for every row created in the run, so every migrated row shares a provenance-obvious `created_at`).
- `last_updated` = same value as `created_at` on first migration.
- `date_ingested` on `sources` = migration run timestamp.
- `date_extracted` on `evidence_fragments` = migration run timestamp.
- `date_published` on `sources` = legacy `date_iso` for anecdotes, or `YYYY-01-01` (year-only fallback) for studies that only have a `year` — with a `raw_metadata.date_precision='year'` flag in that fallback case.
- `computed_at` on `score_history` = the scoring engine's timestamp (distinct from the migration timestamp) so migration provenance and scoring provenance do not collide.

**Status fields.**
- `hypotheses.status` = `active` for every migrated row whose legacy `category` is in the canonical enum or whose raw legacy value survives as `other`; `tentative` is not a valid value on `hypotheses` (spec §4.3 uses `tentative` only on phenotypes). No hypothesis starts `deprecated` or `contested` unless explicitly flagged in notes by manual review.
- `mechanisms.status` = `active` at creation. Mechanisms created from free-text extraction with low `extraction_confidence` are still `active` — low extraction confidence is captured on the fragment, not on the node.
- `phenotypes.status` = `active` for every migrated phenotype. Phenotypes described only in legacy `notes` without diagnostic_markers stay `active` and are flagged in the manual review queue.
- `genes.status` is not a spec column; genes have no status field (v1.1 §4.4). No default needed.
- `sources` has no status column per §4.5. No default needed.
- `interventions.status` = `active`. No intervention starts `experimental` unless legacy `notes` explicitly indicate it.
- `combinations.status` = `active`.
- All edge tables (`*_edges`) `.status` = `active`.

**Effect direction.** Default for an evidence_fragment derived from a study with a non-null `effect_size` and a significant `p_value` is `positive` unless the legacy `outcome` text signals a negative finding; otherwise `unclear`. For anecdotes, direct remap (`null` string → `neutral`, per spec §4.6). No row is written with `effect_direction='null'`.

**Polarity on edges** (`supporting | contradicting | neutral | unknown`). Default `unknown` at edge creation. Set by the scoring engine from the distribution of linked `evidence_fragments.effect_direction` in step 19.

**`relation_type` defaults** where the legacy data doesn't say:
- `hypothesis_mechanism_edges` → `acts_through`
- `mechanism_phenotype_edges` → `implicated_in`
- `gene_mechanism_edges` → `participates_in`
- `gene_phenotype_edges` → `associated_with`
- `intervention_mechanism_edges` → `modulates`
- `intervention_hypothesis_edges` → `cause_mitigation` only when derived from `causes.mitigation_intervention_ids`; otherwise `targets`
- `intervention_gene_edges` → `targets`

**Packed-FK legacy preservation.** Every `*_legacy` column is populated verbatim with the legacy cell content, including whitespace and delimiter exactly as stored in v0.1. No trimming, no sorting, no deduplication. The raw cell is the archival evidence.

**Missing data.** `null` / blank in a live column means "no data at migration time." It does not mean zero or negative. The scoring engine must handle null explicitly and not coerce it to 0.

---

## 3. Per-Table Implementation

One section per new table, in fill order. Each section states which legacy sheet(s) feed it, exactly what each column gets, where `*_legacy` content lands, and where a human review gate is required.

### 3.1 `node_aliases`

**Feeds from:** every other migration step that assigns a new ID or reprefixes a legacy one. Scaffolded first so subsequent steps can write aliases transactionally.

**Column-by-column:**
- `id` — newly assigned `ALS-######` (or equivalent prefix scheme; any stable integer is acceptable).
- `node_type` — enum per v1.1 §10.1: `hypothesis | mechanism | phenotype | gene | intervention | combination | source`.
- `node_id` — the new canonical ID of the node the alias points at.
- `alias` — the legacy ID string verbatim (e.g. `CAU-0001`, `CMB-0001`, `ANE-0099`). Non-ID aliases produced later by ingestion are not written during migration.
- `source` — literal `legacy_v0.1` for every row written during migration.
- `created_at` — migration run timestamp.

**Rows written during migration, by origin:**
- one per `causes` row: alias `CAU-####` → canonical `HYP-####`.
- one per `combinations` row: alias `CMB-####` → canonical `COM-####`.
- one per `anecdotes` row: alias `ANE-####` → canonical `SRC-######`.
- one per `studies` row where a natural secondary key exists (`PMID`, `DOI`): alias `PMID:##########` and/or `DOI:##########` → canonical `SRC-######`, so downstream references by PMID still resolve.
- one per `mechanisms` name variant discovered in free-text extraction: alias variant string → canonical `MEC-####`. These are written in step 11, not in step 3.
- one per `genes` row: alias `gene_symbol` → canonical `GEN-####`, and `ensembl_id` → canonical `GEN-####` when present.

**Manual review:** none at scaffold time; mechanism-name aliases in step 11 go through the manual review queue (noisy variants like "oxidative stress" vs "oxidative damage" vs "reactive oxygen species").

---

### 3.2 `phenotypes`

**Feeds from:** legacy `phenotypes` sheet.

**Column-by-column:**
- `id` — direct copy (`PHE-####` already matches spec).
- `name` — direct copy.
- `description` — **renamed** from legacy `phenotype_description`.
- `diagnostic_markers` — direct copy (plain text).
- `prevalence_estimate` — direct copy (free-text form preserved exactly).
- `status` — set to `active`.
- `created_at`, `last_updated` — migration timestamp.
- `notes` — direct copy.
- `top_intervention_ids_legacy` — verbatim copy of legacy `top_intervention_ids` (semicolon-packed, preserved as-is).
- `top_cause_ids_legacy` — verbatim copy of legacy `top_cause_ids`.

**Dropped from the new schema entirely** (no live column):
- `atlas_page_url` → not migrated (UI metadata per spec §1.8).
- `top_intervention_ids`, `top_cause_ids` in any live column (spec §4.3 forbids them).

**Manual review gates:**
- Every phenotype whose legacy `top_*_ids` lists imply mechanism or hypothesis edges that do not yet exist — these are not materialized in step 4; they enter the manual review queue and become candidate evidence edges later.
- PHE-0007 (`GABA/Cl- imbalance phenotype`) has `top_cause_ids = None` but a populated `top_intervention_ids` — already in legacy-only columns, so no action during step 4.

---

### 3.3 `genes` (descriptive pass)

**Feeds from:** legacy `genes` sheet.

**Column-by-column:**
- `id` — **newly assigned** `GEN-####`, monotonically numbered in the order of the legacy sheet (which is SFARI-first, OpenTargets-last). `gene_symbol` remains the natural unique key.
- `gene_symbol` — direct copy.
- `ensembl_id` — direct copy.
- `sfari_score` — direct copy; missing values (OpenTargets-only rows) written as `NA` to conform to spec §4.4 enum.
- `genetic_evidence_strength` — **renamed** from legacy `evidence_strength` (this is the one spec-sanctioned integer 1–5 field per §4.4).
- `opentargets_score` — direct copy.
- `gnomad_notes` — null at migration (not in legacy).
- `disgenet_score` — null at migration.
- `function_summary` — direct copy.
- `created_at`, `last_updated` — migration timestamp.
- `notes` — direct copy (preserves SFARI category text and report counts verbatim).
- `associated_phenotype_ids_legacy` — verbatim copy of legacy `associated_phenotype_ids` (packed). Consumed in step 16 to build `gene_phenotype_edges`.
- `linked_intervention_ids_legacy` — verbatim copy of legacy `linked_intervention_ids`. Consumed in step 17 to build `intervention_gene_edges`.

**Edges are NOT populated in step 5.** `gene_mechanism_edges`, `gene_hypothesis_edges`, `gene_phenotype_edges`, `intervention_gene_edges` all stay empty at this point.

**Manual review gates:**
- Uniqueness check on `(gene_symbol, ensembl_id)` before PK assignment. Any collision is flagged for manual deduplication.
- Any gene row with `associated_phenotype_ids` or `linked_intervention_ids` referencing IDs not present in `phenotypes` or `interventions` goes on the orphan log.

---

### 3.4 `hypotheses`

**Feeds from:** legacy `causes` sheet.

**Column-by-column:**
- `id` — **reprefixed** from legacy `CAU-####` → `HYP-####` (same integer, new prefix). Matching alias written to `node_aliases` transactionally.
- `name` — direct copy.
- `category` — remapped per spec §4.1:
  - legacy `environmental` → `environmental`
  - legacy `pharmacological` → `other`
  - legacy `dietary` → `other`
  - any other unexpected value → `other` with a manual review flag.
- `description` — direct copy from legacy `mechanism_summary` (demoted: this is a prose description, not a mechanism edge source, until step 11 extracts mechanisms from the same text).
- `affected_population` — direct copy.
- `status` — set to `active`.
- `confidence_score`, `evidence_count`, `evidence_quality_index`, `consistency_index` — null.
- `created_at`, `last_updated` — migration timestamp.
- `notes` — direct copy.
- `category_legacy` — verbatim raw legacy `category` value (preserves the distinction between `pharmacological`, `dietary`, and other).
- `evidence_strength_legacy` — verbatim copy of legacy `evidence_strength` (1–5 hand-edited).
- `epidemiological_strength_legacy` — verbatim copy of legacy `epidemiological_strength`.
- `mitigation_intervention_ids_legacy` — verbatim copy (packed). Consumed in step 14.
- `source_pmids_legacy` — verbatim copy (packed). Consumed in step 10 and step 12.
- `csrs_score_legacy` — verbatim copy (null in all 30 legacy rows, but column exists).
- `csrs_last_updated_legacy` — verbatim copy (null in all 30 legacy rows).

**Dropped from the new schema entirely:** `atlas_page_url`.

**Manual review gates:**
- Every `causes` row whose `category` falls to `other` via the `pharmacological`/`dietary` remap (at least 3 observed: `CAU-0001`, `CAU-0002`, `CAU-0003`).
- `CAU-0001` (FOLR1 autoantibodies / cerebral folate deficiency) is the calibration anchor — must migrate cleanly so leucovorin's downstream `csrs_score` can recover.

---

### 3.5 `interventions` (header pass)

**Feeds from:** legacy `interventions` sheet.

**Column-by-column:**
- `id` — direct copy (`INT-####`).
- `name`, `category`, `directionality` — direct copy. Legacy values observed (`drug`, `supplement`, `treatment`) are subsets of spec enums; validate every row against the spec enums; any out-of-enum value goes to the unclassified-enum log.
- `mechanism_summary` — direct copy as a placeholder string. This field becomes spec-compliant (a short summary *derived from graph mechanisms*) only after step 13 populates `intervention_mechanism_edges`; the live value may be replaced by the scoring/summary layer later.
- `dose_range`, `cost_per_month_usd`, `otc_or_rx`, `pediatric_safe` — direct copy. Validate enums (`otc_or_rx`, `pediatric_safe`) against spec §6.1; out-of-enum values go to the unclassified-enum log.
- `csrs_score` — null. (Live score is populated by the scoring engine in step 19.)
- `csrs_last_updated` — null.
- `status` — set to `active`.
- `created_at`, `last_updated` — migration timestamp.
- `notes` — direct copy.
- `targets_legacy` — verbatim copy of legacy `targets` (semicolon-packed). Consumed in step 13 and step 17.
- `source_pmids_legacy` — verbatim copy. Consumed in step 10.
- `source_anecdote_ids_legacy` — verbatim copy. Consumed in step 10.
- `csrs_score_legacy` — verbatim copy of legacy `csrs_score`.
- `csrs_last_updated_legacy` — verbatim copy of legacy `csrs_last_updated`.

**Dropped from the new schema entirely:** `atlas_page_url`.

**Edges are NOT populated in step 7.** `intervention_mechanism_edges`, `intervention_hypothesis_edges`, `intervention_phenotype_edges`, `intervention_gene_edges` stay empty at this point.

**Manual review gates:** none at header pass; every `targets` token and every `mechanism_summary` clause enters the review queue for step 13.

---

### 3.6 `sources`

**Feeds from:** legacy `studies` sheet (778 rows) AND legacy `anecdotes` sheet (520 rows). Two independent loaders, one target tab.

**Column-by-column (studies loader):**
- `id` — newly assigned `SRC-######`, monotonically numbered.
- `type` — derived from legacy `study_type`: `review`/`meta_analysis` → `review`; all other study_type values → `study`.
- `platform` — literal `pubmed`.
- `external_id` — legacy `pmid`.
- `title` — direct copy.
- `url` — legacy `full_text_url` if present, else null.
- `date_published` — `{legacy year}-01-01` with `raw_metadata.date_precision='year'`.
- `date_ingested` — migration timestamp.
- `study_design` — remap from legacy `study_type`:
  - `rct` → `rct`
  - `case_series` → `case_series`
  - `review` → `review`
  - `meta_analysis` → `meta_analysis`
  - `mechanistic` → `mechanistic`
  - **`observational` → `other`** (per spec §4.5 v1.1)
  - anything else → `other`, logged.
- `sample_size` — **renamed** from legacy `n_subjects`. Nullable.
- `model_system` — null at migration (not in legacy studies).
- `raw_metadata` — JSON object carrying: `doi`, `authors`, `year`, `journal`, `abstract`, `legacy_study_type` (raw pre-remap value, critical for the 313 observational rows), `legacy_replicated` (`yes | partial | unknown | no`), and `date_precision`.
- `notes` — null at migration.

**Column-by-column (anecdotes loader):**
- `id` — newly assigned `SRC-######`, continuing the numbering. Alias `ANE-####` → new `SRC-######` written to `node_aliases`.
- `type` — `anecdote` for legacy `source='reddit'` with a parent/patient reporter; `social` for legacy `source='youtube'` with high engagement or clinician/researcher reporter. Tie-breaker is `reporter_population`: `parent`/`patient` → `anecdote`; `clinician`/`researcher` → `social`; `unknown` → `anecdote`. The choice is recorded in `raw_metadata.legacy_anecdote_type_rule`.
- `platform` — **renamed** from legacy `source` (`reddit`, `youtube`).
- `external_id` — parsed from legacy `url` (Reddit comment ID or YouTube video ID).
- `title` — null (anecdotes don't have a canonical title; legacy `raw_text_excerpt` is usually the thread title but is stored as evidence text).
- `url` — direct copy.
- `date_published` — legacy `date_iso`; null-permitted for rows missing it (e.g. YouTube row 300).
- `date_ingested` — migration timestamp.
- `study_design` — null (not applicable).
- `sample_size` — null.
- `model_system` — `human` by default for anecdotes; null if ambiguous.
- `raw_metadata` — JSON object carrying: `legacy_anecdote_id` (`ANE-####`), `reporter_population`, `engagement`, `legacy_mechanism_match`, `legacy_contradicting_literature`, `raw_text_excerpt_full` (if longer than what lands on the fragment), and `legacy_anecdote_type_rule`.
- `notes` — direct copy of legacy anecdote `notes`.

**Manual review gates:**
- Every `studies` row with `study_type='observational'` is flagged for future cohort-vs-case_control classification (313 rows).
- Every `anecdotes` row with `date_iso=null` or `raw_text_excerpt` shorter than a threshold (title-only) is flagged for body-text backfill.
- Duplicate detection on `external_id` (PMID) across studies — e.g. near-duplicate pair at rows 5 and 100 (Hendren 2016 methyl-B12) — flagged for source-level dedup.

---

### 3.7 `evidence_fragments`

**Feeds from:** legacy `studies` sheet (one default fragment per study) and legacy `anecdotes` sheet (one fragment per anecdote).

**Column-by-column (study-derived fragments):**
- `id` — newly assigned `EVD-######`.
- `source_id` — FK to the `sources.id` created in step 8.
- `fragment_type` — derived from legacy `study_type`: `mechanistic` → `mechanism`; `review`/`meta_analysis` → `result` with a downweight flag recorded in `structured_payload.is_secondary_literature`; everything else → `result`.
- `text_excerpt` — extractive snippet from legacy `abstract`, capped at spec length limit. Full abstract already preserved in `sources.raw_metadata.abstract`.
- `structured_payload` — JSON object: `outcome` (legacy free text), `effect_size` (legacy string + parsed numeric when possible), `p_value` (legacy string + parsed numeric when possible), `replicated` (legacy enum), `legacy_intervention_id`, `legacy_cause_id`, `is_secondary_literature` (bool), `abstract_char_count`.
- `effect_direction` — rule-based inference from `outcome` text + `effect_size` sign + `p_value` significance:
  - positive effect_size + p_value below 0.05 and outcome text not describing deterioration → `positive`
  - negative effect_size + p_value below 0.05 → `negative`
  - p_value above 0.05 or labeled null/ns → `neutral`
  - mixed legacy `replicated`=`partial` with conflicting phrasing → `mixed`
  - anything else → `unclear`.
- `strength_score` — null at migration. (Computed by scoring engine in step 19 per spec §7.1.)
- `extraction_method` — `rule_based` for rows where the rule above produced a definitive direction; `llm_assisted` for rows where an LLM fallback was invoked (to be flagged explicitly in the extraction log); `manual` for any post-migration hand-edit (none at migration time).
- `extraction_confidence` — null at migration.
- `date_extracted` — migration timestamp.
- `notes` — null at migration.

**Column-by-column (anecdote-derived fragments):**
- `id` — newly assigned `EVD-######`, continuing numbering.
- `source_id` — FK to the anecdote-sourced `sources.id`.
- `fragment_type` — `anecdote`.
- `text_excerpt` — legacy `raw_text_excerpt`.
- `structured_payload` — JSON object: `reporter_population`, `engagement`, `legacy_intervention_id`, `legacy_cause_id`, `legacy_mechanism_match` (bool), `legacy_contradicting_literature` (bool). Both legacy booleans are stored but **must not** be consumed by the scoring engine per spec §4.6 (they lack explicit provenance and are demoted per MIGRATION_PLAN §3.5).
- `effect_direction` — legacy `reported_outcome` remapped per spec §4.6:
  - `positive` → `positive`
  - `negative` → `negative`
  - `null` (the string) → `neutral`
  - `mixed` → `mixed`
  - anything else → `unclear`.
- `strength_score` — null at migration.
- `extraction_method` — `rule_based`.
- `extraction_confidence` — null at migration.
- `date_extracted` — migration timestamp.

**Manual review gates:**
- Every fragment with `effect_direction='unclear'` goes on the review queue.
- Every anecdote fragment whose source has `reporter_population='unknown'` is tagged for low-tier `strength_score` floor in step 19 (205 rows).
- Every anecdote fragment whose `text_excerpt` length is below threshold (title-only) is tagged for body-text backfill.

---

### 3.8 `claims` (optional)

**Feeds from:** none during migration. No legacy sheet holds normalized claim sentences.

**Populated in migration:** zero rows.

**Rationale:** Spec §4.7 marks `claims` as optional. Post-migration ingestion can begin populating it (especially for RCTs and meta-analyses) once the canonical-statement generator is built. Not in scope for this migration.

---

### 3.9 `evidence_links` (direct legacy FK pass — step 10)

**Feeds from:** legacy `studies` and legacy `anecdotes` — the `intervention_id` and `cause_id` cells that used to be direct FKs on evidence rows.

**Rows written (studies loader):** for every `studies` row, up to two rows depending on FK population:
- if `intervention_id` is non-null → `evidence_links(target_type='intervention', target_id=legacy intervention_id, ...)`
- if `cause_id` is non-null → `evidence_links(target_type='hypothesis', target_id=reprefixed HYP-#### of legacy CAU-####, ...)`

**Rows written (anecdotes loader):** same pattern per anecdote row.

**Column-by-column:**
- `id` — newly assigned.
- `evidence_fragment_id` — FK to the fragment created in step 9 for that source row.
- `claim_id` — null at migration.
- `target_type` — `intervention` or `hypothesis` per the branch above.
- `target_id` — the intervention's canonical `INT-####` or the hypothesis's reprefixed `HYP-####`.
- `effect_direction` — copied from the parent fragment's `effect_direction` **relative to the target**. For anecdote fragments where legacy `contradicting_literature=True` and the target is a hypothesis, `effect_direction` may be `contradicting` rather than `positive` — this is the one place the legacy boolean is consulted, and it is logged explicitly.
- `weight` — null at migration. (Scoring engine sets it in step 19.)
- `context_scope` — copied from anecdote `reporter_population` when meaningful (e.g. `"reporter=parent"`); null for studies.
- `created_at` — migration timestamp.
- `notes` — null.

**Manual review gates:**
- Every link where `effect_direction='contradicting'` vs. a hypothesis (triggered by the anecdote boolean) is flagged — the legacy boolean's provenance is unknown, and the flag prevents it from silently influencing `consistency_index` until reviewed.
- Every orphan link (target_id references an ID not in the canonical table) goes to the orphan-FK log and is withheld from the data until resolved.

---

### 3.10 `mechanisms`

**Feeds from:** free-text fields on `causes.mechanism_summary`, `interventions.mechanism_summary`, and `interventions.targets`. Also hand-seeded from spec §4.2 examples (oxidative stress, neuroinflammation, impaired methylation, BBB dysfunction, microglial activation, synaptic pruning abnormalities, GABA/glutamate imbalance, gut–brain axis disruption, mTOR pathway dysregulation).

**Step 11 procedure:**
1. **Seed the canonical mechanism list** with the nine spec examples. Each becomes a row with `category` assigned from §4.2's enum (e.g. oxidative stress → `oxidative`, neuroinflammation → `immune_inflammatory`). `MEC-0001` through `MEC-0009` are reserved for these seeds.
2. **Rule-based extraction pass** over all 60 `interventions.mechanism_summary` cells and all 30 `causes.mechanism_summary` cells. Vocabulary matches against a controlled list of mechanism phrases (oxidative stress, inflammation, methylation cycle, BBB, microglial, synaptic pruning, GABA, glutamate, gut–brain, mTOR, NRF2, HSF1, etc.).
3. **LLM fallback** only where rule-based extraction returns nothing for a cell that clearly names a mechanism. LLM output flagged as `llm_assisted` on the downstream evidence fragment, never on the `mechanisms` node.
4. **Canonical name assignment.** Each extracted mechanism phrase resolves to a canonical name; variants are written to `node_aliases` (`node_type='mechanism'`).
5. **Dedup.** Before writing a new `MEC-####`, check `node_aliases` for an existing canonical resolution.

**Column-by-column:**
- `id` — newly assigned `MEC-####`.
- `name` — canonical mechanism name.
- `category` — enum per spec §4.2.
- `description` — null at migration (can be backfilled later from external ontologies).
- `status` — `active`.
- `evidence_strength` — null.
- `kegg_ids`, `reactome_ids`, `opentargets_ids` — null at migration; backfilled in a later ingestion pass.
- `created_at`, `last_updated` — migration timestamp.
- `notes` — null.

**Manual review gates:**
- Every LLM-assisted extraction.
- Every mechanism phrase that appears in only one legacy cell (likely noise).
- Every near-duplicate candidate pair surfaced by string-similarity check.
- Intervention `targets` tokens classified as "mechanism" vs "gene" vs "pathway" — token classifier output reviewed before step 13.

---

### 3.11 `hypothesis_mechanism_edges`

**Feeds from:** step 11's extraction output for `causes.mechanism_summary` cells.

**Column-by-column:**
- `id` — newly assigned.
- `hypothesis_id` — the reprefixed `HYP-####` of the cause that contributed the mechanism_summary.
- `mechanism_id` — the `MEC-####` of the extracted mechanism.
- `relation_type` — default `acts_through` per §2.
- `polarity` — `unknown` at migration.
- `evidence_for_count`, `evidence_against_count`, `evidence_strength_aggregate` — null.
- `context_scope` — null unless the cause's `affected_population` field provides it (e.g. `"pregnancy"`).
- `status` — `active`.
- `created_at`, `last_updated` — migration timestamp.

**Evidence links on the edge:** every fragment from legacy `studies` rows that had `cause_id` pointing at the source cause, and that also matched the extracted mechanism phrase in its abstract (rule-based), gets an `evidence_links(target_type='hypothesis_mechanism_edge', target_id=this edge's id)` row. Abstract-matching failures skip this secondary link.

**Manual review gates:**
- Every edge whose `mechanism_id` was created via LLM fallback.
- Every hypothesis that ends step 12 with zero edges (a cause with no extractable mechanism text).

---

### 3.12 `intervention_mechanism_edges`

**Feeds from:**
1. `interventions.mechanism_summary` extraction (same pipeline as step 11).
2. `interventions.targets` tokens classified as mechanism/pathway (e.g. "folate metabolism", "methylation cycle", "NRF2 pathway", "oxidative stress").

**Column-by-column:**
- `id` — newly assigned.
- `intervention_id` — canonical `INT-####`.
- `mechanism_id` — canonical `MEC-####`.
- `relation_type` — default `modulates`. `targets` in §6.2 is reserved for drugs with pharmacologically specific mechanistic targets — assigned only when the extracted phrase is explicitly a named pathway the intervention is known to act on (manual review).
- `polarity` — `unknown`.
- Remaining aggregates — null.
- `context_scope` — null.
- `status` — `active`.
- `created_at`, `last_updated` — migration timestamp.

**Evidence links:** every study fragment whose legacy `intervention_id` matches this intervention, and whose abstract mentions the extracted mechanism, gets an `evidence_links` row against this edge. Same pattern for anecdote fragments.

**Manual review gates:**
- Every `targets` token. The `targets` column mixes genes, mechanisms, and pathways with no delimiter convention; classification is human-gated.
- Every `intervention_mechanism_edge` whose `relation_type='targets'` — human blessing required before the scoring engine weights it higher than `modulates`.

---

### 3.13 `intervention_hypothesis_edges`

**Feeds from:** legacy `causes.mitigation_intervention_ids` (semicolon-packed; 30 cause rows, most with 0 or 1 entry, some with multiple).

**Step 14 procedure:** for each non-null `mitigation_intervention_ids` cell on a cause row, split on `;`, trim whitespace, and emit one edge per non-empty token.

**Column-by-column:**
- `id` — newly assigned.
- `intervention_id` — the token (`INT-####`).
- `hypothesis_id` — the reprefixed `HYP-####` of the cause row.
- `relation_type` — `cause_mitigation`.
- `polarity` — `supporting` at migration (the legacy relationship was "this intervention mitigates this cause"; it's a claim that wants `supporting` evidence).
- Aggregates — null.
- `context_scope` — null.
- `status` — `active`.
- `created_at`, `last_updated` — migration timestamp.

**Evidence links:** every study fragment whose legacy `(intervention_id, cause_id)` pair matches the edge's `(intervention_id, hypothesis_id)` gets an `evidence_links(target_type='intervention_hypothesis_edge', target_id=this edge's id)` row. 110 study rows had both legacy FKs populated — those are the candidates.

**Manual review gates:**
- Every edge with zero supporting evidence fragments at end of step 14 (i.e. claimed but unsupported by any study) is flagged `status_review_required`.
- Every orphan token (intervention ID referenced but absent from `interventions`) goes to the orphan-FK log.

---

### 3.14 `combinations`

**Feeds from:** legacy `combinations` sheet (4 rows).

**Column-by-column:**
- `id` — **reprefixed** from `CMB-####` → `COM-####` (same integer). Alias written to `node_aliases`.
- `name` — direct copy.
- `description` — concatenation of legacy `evidence_summary` and legacy `notes` where `evidence_summary` is prose. If `evidence_summary` is empty, direct copy of `notes`.
- `rationale` — direct copy.
- `interaction_warnings` — **direct copy from legacy `interaction_warnings`** (canonical per spec v1.1 §6.6).
- `csrs_score` — null.
- `csrs_last_updated` — null.
- `status` — `active`.
- `created_at`, `last_updated` — migration timestamp.
- `notes` — direct copy (may be a duplicate of what's in `description`; preserve both).
- `member_intervention_ids_legacy` — verbatim copy of legacy `member_intervention_ids` (packed). Consumed in step 15b below.
- `csrs_score_legacy` — verbatim copy.
- `csrs_last_updated_legacy` — verbatim copy.

**Dropped from the new schema entirely:** `atlas_page_url`, `evidence_summary` as a standalone field (rolled into `description`).

**Manual review gate:**
- `CMB-0003` (GFCF combo) has `member_intervention_ids=None` — zero-member combination. Flagged.

---

### 3.15 `combination_members`

**Feeds from:** legacy `combinations.member_intervention_ids` packed field.

**Step 15b procedure:** for each legacy combination row with a non-empty `member_intervention_ids`, split on `;`, trim whitespace, and emit one `combination_members` row per non-empty token.

**Column-by-column:**
- `id` — newly assigned.
- `combination_id` — reprefixed `COM-####`.
- `intervention_id` — the token (`INT-####`).
- `role` — null at migration (no `role` information in legacy).
- `created_at` — migration timestamp.

**Manual review gates:**
- Every token that doesn't resolve to an existing `interventions.id` → orphan-FK log.
- Every combination ending step 15b with zero members (expected: `COM-0003`) stays as a zero-member combo and is flagged in the low-evidence scoring path.

---

### 3.16 `gene_phenotype_edges`

**Feeds from:** legacy `genes.associated_phenotype_ids` (packed; a minority of the 1,564 gene rows have anything here).

**Step 16 procedure:** for each gene row with a non-empty `associated_phenotype_ids`, split on `;`, trim whitespace, and emit one edge per non-empty token.

**Column-by-column:**
- `id` — newly assigned.
- `gene_id` — `GEN-####`.
- `phenotype_id` — the token (`PHE-####`).
- `relation_type` — default `associated_with` per §2. Upgrade to `syndromic_cause_of` only when legacy `sfari_score='S'` AND the phenotype is a known syndromic subtype (manual review; applies to e.g. FMR1 → PHE-0006, TSC1/TSC2 → PHE-0005).
- `polarity` — `supporting` at migration (legacy list implies a supported association).
- Aggregates — null.
- `context_scope` — null.
- `status` — `active`.
- `created_at`, `last_updated` — migration timestamp.

**Evidence links:** none at migration. These edges start empty of explicit evidence — they are claims-without-provenance carried forward from v0.1 and will accumulate evidence through subsequent ingestion.

**Manual review gates:**
- Every edge at creation (because the legacy list lacks provenance). Each edge is tagged `provenance='legacy_v0.1'` in the migration log so a later ingestion pass can replace or corroborate it.
- Upgrades to `relation_type='syndromic_cause_of'` — human-gated.

---

### 3.17 `intervention_gene_edges`

**Feeds from:**
1. Legacy `genes.linked_intervention_ids` (packed).
2. Legacy `interventions.targets` tokens classified as gene symbols (step 13's classifier output).

**Column-by-column:**
- `id` — newly assigned.
- `intervention_id` — `INT-####`.
- `gene_id` — `GEN-####` (looked up from `gene_symbol` for the `targets` branch).
- `relation_type` — default `targets`.
- `polarity` — `supporting`.
- Aggregates — null.
- `context_scope` — null.
- `status` — `active`.
- `created_at`, `last_updated` — migration timestamp.

**Evidence links:** none at migration (same reasoning as gene_phenotype_edges).

**Manual review gates:**
- Every `targets` token classified as a gene symbol.
- Every duplicate edge (same intervention_id + gene_id from both the genes branch and the targets branch) — deduplicated with the provenance of both branches preserved in `notes`.

---

### 3.18 `gene_mechanism_edges`

**Feeds from:** nothing legacy. Populated in subsequent ingestion passes from KEGG, Reactome, OpenTargets, and STRING.

**Rows written during migration:** zero.

**Rationale:** Spec §5.3 is clean and the legacy sheet has no column expressing this relation. Populating it requires external ontology pulls that are part of ingestion, not migration.

---

### 3.19 `gene_hypothesis_edges`

**Feeds from:** nothing legacy. Optional table per spec §5.4.

**Rows written during migration:** zero.

---

### 3.20 `mechanism_phenotype_edges`

**Feeds from:** nothing legacy directly. Can be bootstrapped from legacy `phenotypes.diagnostic_markers` and `phenotypes.description` via a second extraction pass, but this is ingestion, not migration.

**Rows written during migration:** zero.

**Rationale:** Mechanism-to-phenotype chaining requires text mining of the phenotype prose, which is out of the initial migration's rule-based budget. Deferred to a named ingestion task.

---

### 3.21 `intervention_phenotype_edges`

**Feeds from:** legacy `phenotypes.top_intervention_ids` is tempting, but those lists are claims-without-polarity-or-evidence and are explicitly dropped from core per spec §4.3. They remain in `phenotypes.top_intervention_ids_legacy`.

**Rows written during migration:** zero.

**Rationale:** Real intervention-phenotype edges must be supported by evidence fragments that name both the intervention and the phenotype. That's an ingestion task.

---

### 3.22 `score_history`

**Feeds from:** the scoring engine's output in step 19, and from the migration delta on hand-edited legacy scores.

**Rows written during migration:** one row per node that gained a live computed score in step 19 (hypotheses, mechanisms, interventions, combinations, and any relevant edges). Additionally, one row per node whose legacy hand-edited score was replaced by a computed value — these are the "migration delta" rows.

**Column-by-column (migration-delta rows):**
- `id` — newly assigned.
- `target_type` — `hypothesis | mechanism | phenotype | gene | intervention | combination`.
- `target_id` — canonical ID.
- `score_type` — `confidence` for hypotheses, `csrs` for interventions and combinations, `other` for aggregates that don't have a first-class name yet.
- `old_score` — the legacy hand-edited value, copied from the row's `*_legacy` column (e.g. `interventions.csrs_score_legacy`, `hypotheses.evidence_strength_legacy`, etc.).
- `new_score` — the scoring engine's output in step 19.
- `component_breakdown` — JSON object of the scoring engine's per-component contributions.
- `evidence_delta_ids` — list of `evidence_fragment_id`s that the scoring engine used to produce `new_score`. For migration-delta rows, this is the full initial set (not a delta against a prior computed score — there wasn't one).
- `computed_at` — the scoring engine's timestamp from step 19, not the migration timestamp.

**Column-by-column (first-computation rows for nodes without a legacy score):** same columns, `old_score=null`.

**Manual review gates:**
- Every node where `|new_score - old_score| > 25` on a 0–100 scale (or equivalent on 0–1) is flagged. These are the cases where the migration swung a hand-edited number far from what the graph supports — worth investigating whether the graph is under-covered or the hand number was wrong.
- Leucovorin (`INT-0001`) specifically: if `new_score < 80`, block migration lock until triaged.

---

## 4. Migration Logging and Audit Trail

Per spec §1.6 (auditability), §9.2 (no overwrites without history), and §10.2 (ontology changes logged), the migration itself must be fully reconstructible from its logs. The following artifacts are produced during migration and persisted alongside the migrated data.

**Migration run header.** One record per run: migration run ID (e.g. `mig-2026-04-24T...`), migration timestamp, spec version (`v1.1`), legacy file SHA-256, legacy file size, operator identity, software version (tool name + build). Every log row references this run ID.

**Per-row mapping log.** One row per legacy row, per target table it contributed to. Fields: run ID, legacy sheet, legacy row number, legacy primary key (PMID, CAU-####, INT-####, etc.), target table, target row PK, operation (`copy | rename | remap | split | derived | skipped`), notes. This is the ground-truth trace from legacy row to new row(s) — the single source of truth when reconstructing provenance.

**`*_legacy` preservation log.** Sanity check, not a data table: a report that asserts every non-null legacy cell from a packed-FK or deprecated-score column is preserved verbatim in exactly one `*_legacy` column. If any cell is lost, the migration fails closed.

**Enum remap log.** Every row where a legacy enum value was coerced to the canonical enum: run ID, legacy sheet, legacy row, column, legacy value, new value, reason. Drives the canonical-enum distribution report (e.g. "313 observational → other", "3 pharmacological → other", "3 null → neutral on anecdote rows").

**Orphan FK log.** Every legacy FK token (in any packed or direct FK field) that doesn't resolve to a canonical target. Fields: run ID, source sheet/row, source column, token, expected target type. Written during steps 10, 13, 14, 15, 16, 17. These rows are not written to edge tables; they are withheld until resolved.

**Unresolved pointer log.** Specifically for `csrs_components.evidence_pointers` — pointers that are neither PMIDs nor ANE-IDs nor canonical IDs (e.g. `"FOLR1 autoantibodies"`, `"Functional med community adoption"`, `"n/a"`). Fields: run ID, legacy row, intervention_id, component, pointer text, reason unresolvable.

**Manual review queue.** Flat list of every row or cell flagged by any of the manual review gates in §3 of this document. Fields: run ID, queue category (per MIGRATION_PLAN.md §4), target table, target row PK, legacy row PK, reason, priority. Sorted by priority so reviewers start at the top.

**Extraction log.** For mechanism extraction from free text: run ID, source sheet/row, source column, extracted phrase, canonical mechanism name (if resolved), extraction method (`rule_based` or `llm_assisted`), confidence, review flag. Required so the LLM-assisted rows can be reviewed independently of rule-based rows.

**Duplicate detection log.** Near-duplicate candidate pairs surfaced by uniqueness checks: source (sheet/table), field, candidate A, candidate B, similarity metric, decision (`merged | distinct | deferred`). Applied to `sources.external_id`, `hypotheses.name`, `mechanisms.name`, `genes.(gene_symbol, ensembl_id)`, `sources.title` (for near-duplicate PMIDs like the two 2016 Hendren methyl-B12 entries).

**`node_aliases` emission log.** Every alias written, grouped by `node_type`. Acts as the authoritative map of legacy-ID → canonical-ID for future systems.

**Score-migration delta report.** Tabular: target type, target ID, legacy score, computed score, delta, component breakdown. Highlights the large deltas (|Δ| > threshold) with a recommended review disposition.

**QA sweep report.** Final check: orphan-FK count, null-evidence-node count, semicolon-in-live-column count (must be zero), hand-score-in-live-column count (must be zero), duplicate-source count, calibration-test pass/fail (leucovorin ≥ 80).

**Migration exception file.** The union of everything the migration couldn't auto-process: unresolved pointers, orphan FKs, failed enum remaps, zero-coverage edges, and anything flagged for manual review. This is the worklist handed to the reviewer after migration lock.

**Retention.** All logs are retained indefinitely, keyed by migration run ID. A migration can only be "un-locked" by producing a new run with a new ID; the prior run's logs remain immutable. Reproducibility requires only the legacy file + the migration code + the logs.

---

**End of MIGRATION_IMPLEMENTATION.md.**
