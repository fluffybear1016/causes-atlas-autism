# CAUSES ATLAS — AUTISM
## Canonical Architecture & Schema Spec

**Version:** 1.1
**Date:** 2026-04-24
**Owner:** Gregory J. Rigano, Esq.
**Status:** Canonical spec — all work must conform to this document.

This file is the **single source of truth** for the Autism Causes Atlas architecture, schema, scoring, and ingestion behavior.
Every agent or code change MUST align with this spec or clearly mark deviations as "Proposed Extension" with justification.

---

## 0. Objective

We are not defining the causes or treatments of autism.
We are building a system that **discovers, scores, and updates causal hypotheses** over time — a living knowledge graph plus deterministic scoring engine.

The system must:

- Map all plausible autism-relevant hypotheses (environmental, biological, genetic, immunological, metabolic, microbial, social, behavioral, etc.).
- Track mechanisms and pathways that connect those hypotheses to observable phenotypes and outcomes.
- Integrate top-down sources (peer-reviewed literature, datasets, registries) with bottom-up sources (anecdotes, social media, real-world signals).
- Update confidence dynamically and **deterministically** as new evidence arrives.
- Preserve uncertainty and contradiction; avoid premature conclusions.
- Support a derived decision layer (interventions, combinations, scores) **without contaminating discovery**.
- Remain open-ended so new hypotheses, evidence types, pathways, and interventions can be added without redesign.

---

## 1. Core Principles

1. **No assumed truth**
   - Hypotheses, mechanisms, phenotypes, and interventions are not "true" or "false."
     They have **scores** and **states** based on evidence.

2. **Evidence moves scores — not opinions**
   - Only structured evidence records, routed through deterministic functions, can change confidence.

3. **Contradiction is a first-class object**
   - Positive, negative, null, and mixed findings are represented explicitly.
   - "Contested" is a valid long-term state.

4. **Two layers, strict separation**
   - **Layer 1 (Core Causal Graph):** hypotheses, mechanisms, phenotypes, genes, evidence, and edges.
   - **Layer 2 (Derived Decision Layer):** interventions, combinations, and graph-derived scores (e.g., CSRS-style).

5. **No LLMs in scoring**
   - Scoring is pure, deterministic code over the schema.
   - LLMs are allowed only for:
     - extraction/structuring of raw evidence,
     - summarization,
     - drafting human-readable pages,
     - proposing ontology changes (flagged for human review).

6. **Auditability**
   - Every score and edge must be traceable back to:
     - specific evidence records,
     - deterministic rules,
     - and a timestamped computation.

7. **Google-Sheets-first, graph-ready schema**
   - Persistence in v1 is Google Sheets with CSV export.
   - Schema is normalized: **no semicolon lists as primary relationships**.
   - Design as if we will migrate to Postgres/BigQuery/Neo4j later.

8. **UI metadata lives outside the schema**
   - Fields like `atlas_page_url` and any other page-builder or presentation-layer metadata are **not** part of the canonical schema.
   - They may live in a page-builder metadata store or be derived from IDs at render time, but they do not belong in the core tables or Layer 2 tables defined here.

---

## 2. System Architecture Overview

### 2.1 Two-Layer Architecture

**Layer 1 — Core Causal Graph (Unbiased)**

Node types (at minimum):

- `hypotheses`
- `mechanisms`
- `phenotypes`
- `genes`
- `sources` (artifacts)
- `evidence_fragments`
- `claims` (optional but recommended)
- Typed edge/link tables between these entities

**Layer 2 — Derived Decision Layer**

Node types:

- `interventions`
- `combinations`

Derived structures:

- `intervention_*` link tables (to hypotheses, mechanisms, phenotypes, genes)
- `csrs_components` (or equivalent breakdown)
- `csrs_history` / score history

**Critical rule:**
Layer 2 may only read **aggregates from Layer 1**, never raw evidence rows directly for scoring.

---

## 3. Persistence Model

### 3.1 Google Sheets & CSV

- One tab = one table.
- Every tab must export cleanly to CSV.
- Use stable IDs.
- Use explicit foreign keys.
- Use normalized linking tables instead of multi-ID cells.

### 3.2 ID and FK Conventions

- IDs are string, prefix + zero-padded integer, e.g. `HYP-0001`, `MEC-0001`, `PHE-0001`, `GEN-0001`, `INT-0001`, `COM-0001`, `SRC-000001`, `EVD-000001`.
- Foreign keys always refer to these IDs.
- Legacy semicolon lists from `causes_atlas_schema_v0.1.xlsx` are allowed only in `*_legacy` fields and may not be relied on by new code.

### 3.3 Legacy ID reprefixing

Legacy ID prefixes from `causes_atlas_schema_v0.1.xlsx` are remapped to canonical prefixes at migration time:

- `CAU-####` → `HYP-####` (legacy "causes" sheet becomes canonical `hypotheses`)
- `CMB-####` → `COM-####` (legacy "combinations" IDs align with canonical `COM-####`)

Every legacy ID — including `CAU-####`, `CMB-####`, `ANE-####` (anecdotes), and any other prefix that survives from v0.1 — **must** be recorded in `node_aliases` (§10.1) at migration time so legacy references (e.g. `studies.cause_id = CAU-0001`, `csrs_components.evidence_pointers = ANE-0001`) can be resolved unambiguously. No legacy ID is dropped silently.

---

## 4. Core Entities (Layer 1)

### 4.1 Table: `hypotheses`

**Purpose:**
Represents any proposed driver, contributor, modifier, or correlate of autism.

**Examples:**

- Environmental toxin exposure (PFAS, heavy metals, pesticides, air pollution)
- Mitochondrial dysfunction
- Immune dysregulation / maternal immune activation
- Microbiome alteration / dysbiosis
- Genetic variation (de novo, inherited, CNVs)
- Epigenetic modification
- Perinatal hypoxia, infection, medication exposure
- Social/behavioral exposures

**Columns (minimum):**

- `id` — string, PK, e.g. `HYP-0001`
- `name` — canonical name
- `category` — enum: `environmental | genetic | immune | metabolic | microbial | perinatal | behavioral | social | epigenetic | other`
- `description` — plain-language description
- `affected_population` — free text, **descriptive non-scoring metadata** (e.g. `"~10–25% of cases (subset)"`, `"Population-wide if exposed"`). Informational only; does not feed `confidence_score` or any derived Layer 2 score.
- `status` — enum: `active | weak | disproven | contested | deprecated`
- `confidence_score` — float [0, 1], computed only
- `evidence_count` — int, computed
- `evidence_quality_index` — float [0, 1], computed
- `consistency_index` — float [0, 1], computed; penalty for high disagreement
- `created_at` — ISO-8601
- `last_updated` — ISO-8601
- `notes` — free text

**Category enum behavior for legacy values:**
Legacy `causes.category` values that are not in the canonical enum map to `other` at migration time. In particular:

- legacy `pharmacological` → `other`
- legacy `dietary` → `other`

The original raw legacy value is preserved in `hypotheses.category_legacy` (or equivalently in `notes`) so future spec revisions can refine the enum without losing information.

**No hand-edited scores.**

---

### 4.2 Table: `mechanisms`

**Purpose:**
Biological/physiological processes linking hypotheses to phenotypes.

**Examples:**

- Oxidative stress
- Neuroinflammation
- Impaired methylation
- BBB dysfunction
- Microglial activation
- Synaptic pruning abnormalities
- GABA/glutamate imbalance
- Gut–brain axis disruption
- mTOR pathway dysregulation

**Columns:**

- `id` — PK, e.g. `MEC-0001`
- `name`
- `category` — enum: `oxidative | immune_inflammatory | metabolic | neural | endocrine | microbial | vascular | hormonal | other`
- `description`
- `status` — enum: `active | weak | disproven | contested | deprecated`
- `evidence_strength` — float [0, 1], computed
- `kegg_ids` — optional, comma/semicolon string (for external pathway IDs)
- `reactome_ids` — optional
- `opentargets_ids` — optional
- `created_at`
- `last_updated`
- `notes`

---

### 4.3 Table: `phenotypes`

**Purpose:**
Observable autism subtypes / clusters / presentations.

**Examples:**

- Regression subtype
- High-inflammatory profile
- Mitochondrial subtype
- GI-dominant subtype
- Sensory-dominant subtype
- Minimally verbal / nonverbal subtype
- Sleep-disturbance-dominant subtype

**Columns:**

- `id` — PK, e.g. `PHE-0001`
- `name`
- `description`
- `diagnostic_markers` — plain text; structured markers may move to a `biomarkers` table later
- `prevalence_estimate` — string or numeric + range (e.g. `"0.10–0.15"`)
- `status` — enum: `active | tentative | deprecated`
- `created_at`
- `last_updated`
- `notes`

**Important:**
No direct `top_intervention_ids` or `top_cause_ids` fields in core. Those belong in derived views or Layer 2 tables.

---

### 4.4 Table: `genes`

**Purpose:**
Genetic layer (seeded from SFARI, enriched by DisGeNET, ClinVar, gnomAD, OpenTargets, etc.).

**Columns:**

- `id` — PK, e.g. `GEN-0001`
- `gene_symbol`
- `ensembl_id`
- `sfari_score` — enum: `1 | 2 | 3 | S | NA`
- `genetic_evidence_strength` — int 1–5
- `opentargets_score` — float [0, 1]
- `gnomad_notes` — free text (variant burden)
- `disgenet_score` — float [0, 1], optional
- `function_summary` — plain English
- `created_at`
- `last_updated`
- `notes`

---

### 4.5 Table: `sources` (artifacts)

**Purpose:**
One row per artifact (paper, dataset, post, video, registry entry, etc.).

**Columns:**

- `id` — PK, e.g. `SRC-000001`
- `type` — enum: `study | preprint | review | dataset | clinical | registry | anecdote | social | environmental | trial | other`
- `platform` — e.g. `pubmed | europe_pmc | biorxiv | medrxiv | reddit | youtube | x | epa | usgs | ctgov | openfda | dailyMed | rxnorm | who_ictrp | oecd | other`
- `external_id` — e.g. `PMID`, `DOI`, `Reddit id`, `YouTube video id`, `X status id`, `NCT id`
- `title` — for literature/registries
- `url`
- `date_published` — ISO-8601
- `date_ingested` — ISO-8601
- `study_design` — for relevant sources: `rct | cohort | case_control | case_series | mechanistic | meta_analysis | review | animal | in_vitro | in_silico | epigenetic | transgenerational | other`
- `sample_size` — numeric, nullable
- `model_system` — e.g. `human`, `mouse`, `cell_line`, `rat`, etc.
- `raw_metadata` — JSON string or text blob
- `notes`

**`study_design` behavior for legacy values:**
Legacy `studies.study_type` values that are not in the canonical enum map to `other` at migration time. In particular:

- legacy `observational` → `other`

The original raw legacy value is preserved in `sources.raw_metadata` (e.g. under a `legacy_study_type` key) so the `observational` population (cohort vs. case-control) can be refined by a future pass without losing provenance.

---

### 4.6 Table: `evidence_fragments`

**Purpose:**
Atomic pieces of evidence extracted from a source artifact (e.g., a specific result, table row, paragraph, or snippet).

**Columns:**

- `id` — PK, e.g. `EVD-000001`
- `source_id` — FK → `sources.id`
- `fragment_type` — enum: `result | effect_size | association | mechanism | anecdote | observation | safety_signal | exposure_measure | other`
- `text_excerpt` — key text, up to length limit
- `structured_payload` — optional JSON/serialized structure (effect size, OR, HR, etc.)
- `effect_direction` — enum: `positive | negative | neutral | mixed | unclear` (relative to linked hypothesis/edge)
- `strength_score` — float [0, 1], function of:
  - source type & quality,
  - study design,
  - sample size,
  - risk of bias,
  - etc.
- `extraction_method` — enum: `rule_based | llm_assisted | manual`
- `extraction_confidence` — float [0, 1]
- `date_extracted`
- `notes`

**`effect_direction` canonicalization:**
The canonical neutral label is `neutral`. Legacy anecdote outcome values must be normalized at ingestion:

- legacy `null` (the string) → `neutral`
- legacy `positive` → `positive`
- legacy `negative` → `negative`
- legacy `mixed` → `mixed`
- anything else → `unclear`

`null` is not a valid `effect_direction` in any new record. Downstream systems must read `neutral` and nothing else for that case.

---

### 4.7 Table: `claims` (optional but recommended)

**Purpose:**
Normalized propositions like "prenatal valproate exposure increases autism risk" or "sulforaphane reduces irritability in ASD."

**Columns:**

- `id` — PK, e.g. `CLM-000001`
- `canonical_statement` — normalized English sentence
- `statement_hash` — hash to catch near-duplicates
- `created_at`
- `last_updated`
- `notes`

**Claims are linked to fragments and nodes via linking tables (below).**

---

## 5. Relationship / Edge Model

All relationships are represented in separate linking tables.

### 5.1 Table: `hypothesis_mechanism_edges`

**Purpose:**
Edges between hypotheses and mechanisms.

**Columns:**

- `id`
- `hypothesis_id`
- `mechanism_id`
- `relation_type` — enum: `acts_through | associated_with | modulated_by | leads_to`
- `polarity` — enum: `supporting | contradicting | neutral | unknown`
- `evidence_for_count` — int, computed
- `evidence_against_count` — int, computed
- `evidence_strength_aggregate` — float [0, 1], computed
- `context_scope` — string (e.g. age range, phenotype subset, geography)
- `status` — `active | deprecated`
- `created_at`
- `last_updated`

Analogous linking tables follow the same pattern:

### 5.2 Table: `mechanism_phenotype_edges`

- `id`
- `mechanism_id`
- `phenotype_id`
- `relation_type` — e.g. `implicated_in | characteristic_of`
- plus the same evidence / status / timestamps fields as above.

### 5.3 Table: `gene_mechanism_edges`

- `id`
- `gene_id`
- `mechanism_id`
- `relation_type` — e.g. `participates_in | regulates | risk_factor_for`
- plus evidence fields.

### 5.4 Table: `gene_hypothesis_edges` (optional)

- `id`
- `gene_id`
- `hypothesis_id`
- `relation_type`
- evidence fields.

### 5.5 Table: `gene_phenotype_edges`

**Purpose:**
Represent empirically observed gene↔phenotype associations even when the mechanism chain between them is incomplete. This table exists so that strong gene-to-subtype patterns (e.g. FMR1 → Fragile X phenotype, TSC1/TSC2 → mTOR syndromic phenotype, FOLR1 → cerebral folate deficiency phenotype) can be stored with provenance without forcing premature mechanism commitments.

Edges in this table are a complement to, not a substitute for, the gene → mechanism → phenotype chain expressed by `gene_mechanism_edges` + `mechanism_phenotype_edges`. When a mechanism chain is known and supported, both representations can coexist; the scoring engine will not double-count evidence.

**Columns:**

- `id`
- `gene_id`
- `phenotype_id`
- `relation_type` — enum: `associated_with | enriched_in | characteristic_of | syndromic_cause_of`
- `polarity` — enum: `supporting | contradicting | neutral | unknown`
- `evidence_for_count` — int, computed
- `evidence_against_count` — int, computed
- `evidence_strength_aggregate` — float [0, 1], computed
- `context_scope` — string (e.g. age range, population subset, geography)
- `status` — `active | deprecated`
- `created_at`
- `last_updated`

### 5.6 Table: `evidence_links`

**Purpose:**
Connect evidence fragments (and optionally claims) to any node or edge they touch.

**Columns:**

- `id`
- `evidence_fragment_id` — FK → `evidence_fragments.id`
- `claim_id` — FK → `claims.id`, nullable
- `target_type` — enum: `hypothesis | mechanism | phenotype | gene | hypothesis_mechanism_edge | mechanism_phenotype_edge | gene_mechanism_edge | gene_phenotype_edge | intervention | combination`
- `target_id`
- `effect_direction` — `positive | negative | neutral | mixed | unclear` (relative to target)
- `weight` — float [0, 1], contribution to target score
- `context_scope` — as above
- `created_at`
- `notes`

---

## 6. Layer 2: Interventions & Combinations

### 6.1 Table: `interventions`

**Purpose:**
Downstream, derived layer for decision-relevant entities.

**Columns:**

- `id` — PK, e.g. `INT-0001`
- `name` — canonical name
- `category` — enum: `drug | supplement | food | diet | herb | lifestyle | environmental | generational | combo_seed | other`
- `directionality` — enum: `treatment | prevention | cause_mitigation | generational`
- `mechanism_summary` — 2–4 sentence summary (derived from graph)
- `dose_range` — free text
- `cost_per_month_usd` — numeric
- `otc_or_rx` — enum: `otc | rx | lifestyle | environmental`
- `pediatric_safe` — enum: `yes | no | uncertain | age_restricted`
- **No direct raw evidence fields here** (papers/anecdotes should be reachable via graph).
- `csrs_score` (or equivalent) — numeric (e.g. 0–100), computed only
- `csrs_last_updated` — ISO-8601
- `status` — `active | experimental | deprecated`
- `created_at`
- `last_updated`
- `notes`

### 6.2 Table: `intervention_mechanism_edges`

- `id`
- `intervention_id`
- `mechanism_id`
- `relation_type` — e.g. `targets | modulates | supports`
- evidence fields / aggregates similar to core edges.

### 6.3 Table: `intervention_hypothesis_edges`

### 6.4 Table: `intervention_phenotype_edges`

### 6.5 Table: `intervention_gene_edges`

All following the same pattern: IDs, FKs, relation_type, evidence aggregates, context, status, timestamps.

### 6.6 Table: `combinations`

**Purpose:**
First-class combinations of interventions.

**Columns:**

- `id` — PK, e.g. `COM-0001`
- `name`
- `description`
- `rationale`
- `interaction_warnings` — free text. Safety-relevant notes about contraindications, drug–drug / supplement–drug interactions, monitoring requirements, population-specific cautions (e.g. `"Monitor for excess methylation symptoms in COMT++ children"`). This field is descriptive safety metadata; it does not drive scoring, but it is canonical schema and must survive ingestion.
- `csrs_score` — computed only
- `csrs_last_updated`
- `status`
- `created_at`
- `last_updated`
- `notes`

### 6.7 Table: `combination_members`

- `id`
- `combination_id`
- `intervention_id`
- `role` — optional (e.g. `core | adjunct | supportive`)
- `created_at`

---

## 7. Evidence Quality and Scoring Engine

### 7.1 Evidence-quality components (for hypotheses/mechanisms/phenotypes/genes)

The **confidence score** for core nodes is a deterministic function of:

- `evidence_count` — number of independent sources.
- `evidence_quality` — function of:
  - study type (RCT > cohort > case-control > case-series > mechanistic > anecdote),
  - sample size,
  - replication/meta-analysis,
  - registry/dataset robustness.
- `consistency` — degree of agreement across effect directions.
- `mechanism_coherence` — overlap with high-confidence biological pathways (KEGG, Reactome, OpenTargets).
- `genetic_support` — SFARI + OpenTargets + variant burden (for genetic hypotheses).
- `cross_phenotype_convergence` — number and coherence of phenotypes implicated.
- `epigenetic/generational` evidence.
- `trend/emerging_signal` — recent increase in evidence (all types).
- `in_silico_functional` (optional).
- `replication/independence` — diversity of institutions/countries.
- `source_type_diversity` — mixture of studies, datasets, clinical, registry, anecdotes, etc.

You do NOT need to fix exact weights in this spec, but you must:

- Define each component clearly.
- Provide pseudo-formulas for how node scores are computed from evidence and edges.
- State clearly that these live in config and can be tuned, but reruns are deterministic.

### 7.2 Intervention / CSRS-style scoring (Layer 2)

Intervention/combination scores are derived only from:

- Which hypotheses they target.
- The strength of those hypotheses and mechanisms in the graph.
- Evidence of effect on relevant phenotypes.
- Genetic coherence (where applicable).
- Safety/practicality (from FAERS, DailyMed, cost, OTC/Rx, pediatric safety).
- Trend/emerging signals (including social signals with low base weight).
- Combination synergy where applicable.

**Forbidden:**
No direct "count studies where `intervention_id = X`" or "count anecdotes with `intervention_id = X`" in scoring. All such counts must be routed through Layer 1 nodes/edges and their evidence aggregates.

### 7.3 Hand-edited scoring fields are archival only

Legacy scoring fields from `csrs_components` — specifically `weight_pct`, `raw_score_0_100`, `weighted_contribution`, and any analogous hand-edited numeric fields — are **archival only**. They may be retained for historical calibration reference (e.g. a legacy snapshot file or a `*_legacy` column), but they **do not survive as live columns** in the canonical schema and **do not participate in any current score computation**.

The only way a number enters a live score column (`confidence_score`, `evidence_strength`, `evidence_strength_aggregate`, `csrs_score`, `strength_score`, etc.) is as the deterministic output of the scoring engine defined in §7.1–§7.2, over structured evidence records. Configurable weights for the scoring engine live in config, not in data.

---

## 8. Ingestion System

### 8.1 Top-down inputs

- **Literature**
  - PubMed E-utilities
  - Europe PMC
  - SemMedDB
  - bioRxiv
  - medRxiv

- **Biology / functional**
  - OpenTargets (GraphQL)
  - KEGG
  - Reactome
  - STRING
  - GTEx
  - ChEMBL
  - AlphaFold
  - LINCS L1000 / Clue.io (optional)

- **Genetics**
  - SFARI Gene (CSV)
  - DisGeNET
  - ClinVar
  - gnomAD

- **Clinical / regulatory**
  - ClinicalTrials.gov v2
  - OpenFDA FAERS
  - DailyMed
  - RxNorm
  - WHO ICTRP

- **Environmental**
  - EPA ECHO
  - EPA Air Quality System
  - USGS Water Quality
  - State environmental databases
  - OECD / WHO exposure registries

### 8.2 Bottom-up inputs

- Reddit (autism-related subreddits, public JSON/PRAW)
- YouTube (captions + metadata via YouTube Data API)
- X (Twitter):
  - Browser-visible pages,
  - compliance-aware scraping/automation,
  - and/or Grok/xAI or similar for real-time X access as soon as available.
- Blogs, forums, parent/clinician websites (RSS or sitemap-based).
- Podcasts (transcripts where available).

### 8.3 Ingestion pipeline (per artifact)

1. Fetch & parse.
2. Create/append `sources` row.
3. Extract `evidence_fragments`:
   - Prefer deterministic pattern/keyword/structure rules.
   - Use LLM only when rules fail to capture necessary structure.
4. For each fragment, infer:
   - effect_direction (with legacy `null` → `neutral` normalization applied per §4.6),
   - strength_score,
   - candidate links to hypotheses/mechanisms/phenotypes/genes/interventions.
5. Create `evidence_links` rows:
   - deterministic rules first (based on keywords, ontology mappings, IDs).
   - LLM suggestions flagged as low-confidence until confirmed.
6. Recompute relevant node and edge scores using deterministic scoring engine.
7. Append `score_history` records capturing:
   - old score,
   - new score,
   - component breakdown,
   - evidence that changed.

---

## 9. Contradiction, Uncertainty, & Temporal Behavior

### 9.1 Contradiction

- Every `evidence_link` carries an `effect_direction`.
- Node/edge `consistency_index` reflects the distribution of positive/negative/neutral evidence.
- Hypotheses, mechanisms, phenotypes, and interventions can have status `contested`.

### 9.2 Temporal

- `score_history` table:
  - `id`
  - `target_type` (`hypothesis | mechanism | phenotype | gene | intervention | combination`)
  - `target_id`
  - `score_type` (`confidence | csrs | other`)
  - `old_score`
  - `new_score`
  - `component_breakdown` (JSON)
  - `evidence_delta_ids` (list of `evidence_fragment_id`s)
  - `computed_at`

No overwriting without history.

---

## 10. Ontology Governance

### 10.1 Canonical vs aliases

Add a `node_aliases` table:

- `id`
- `node_type` (`hypothesis | mechanism | phenotype | gene | intervention | combination | source`)
- `node_id`
- `alias`
- `source` (who/what introduced alias; e.g. `legacy_v0.1`, `ingestion_pipeline`, `manual`)
- `created_at`

**Migration use:** every legacy ID that is reprefixed or restructured at migration time — `CAU-####`, `CMB-####`, `ANE-####`, and any future legacy prefix — is recorded here as an alias of its canonical new ID. This guarantees that legacy references (in old exports, in free-text notes, in `csrs_components.evidence_pointers`, etc.) remain resolvable.

### 10.2 Merge / split / deprecate

- Duplicates detected by string similarity and manual review.
- Merges tracked via a `merged_into` field or dedicated `node_merges` table.
- Deprecated nodes retain IDs, flagged `status = deprecated`, but no longer accumulate new evidence.

All ontology changes should be:

- Logged,
- Justified,
- Optionally assisted by LLM proposals but finalized by human judgment.

---

## 11. Migration from `causes_atlas_schema_v0.1.xlsx`

### 11.1 General approach

- Treat `causes_atlas_schema_v0.1.xlsx` as a **legacy seed**, not the target.
- Use its:
  - interventions,
  - causes,
  - studies,
  - anecdotes,
  - combinations,
  - phenotypes,
  - genes,
  - csrscomponents
  as seed content to be rewritten into the new schema.

### 11.2 Example mappings (high level)

- `interventions` sheet → `interventions` + `intervention_*_edges` tables, with `sourcepmids` / `sourceanecdoteids` turned into proper `evidence_links`.
- `causes` sheet → `hypotheses` table + `hypothesis_mechanism_edges`. Legacy `CAU-####` IDs become `HYP-####`; legacy IDs are recorded in `node_aliases`. Legacy category values `pharmacological` and `dietary` map to canonical `other`, with the original raw value preserved per §4.1.
- `studies` sheet → `sources` (type=study) + `evidence_fragments`. Legacy `study_type = observational` maps to canonical `study_design = other`, with the original raw value preserved in `sources.raw_metadata` per §4.5.
- `anecdotes` sheet → `sources` (type=anecdote|social) + `evidence_fragments`. Legacy `reported_outcome` values are normalized to the canonical `effect_direction` enum per §4.6 (including `null` → `neutral`). Legacy `ANE-####` IDs are recorded in `node_aliases`.
- `combinations` sheet → `combinations` + `combination_members`. Legacy `CMB-####` IDs become `COM-####`; legacy IDs are recorded in `node_aliases`. Legacy `interaction_warnings` text lands in the canonical `combinations.interaction_warnings` field per §6.6.
- `phenotypes` sheet → `phenotypes` table, dropping direct `topinterventionids` / `topcauseids` in core (per §4.3) and preserving them only in `*_legacy` columns.
- `genes` sheet → `genes` + gene-related linking tables, including `gene_phenotype_edges` (§5.5) for legacy `associated_phenotype_ids`, `intervention_gene_edges` for legacy `linked_intervention_ids`, and — where evidence supports it — `gene_mechanism_edges` and `gene_hypothesis_edges`. Legacy `evidence_strength` (1–5) maps to `genes.genetic_evidence_strength`.
- `csrscomponents` sheet → **not** migrated as a live data table. Its `weight_pct` values may seed scoring-engine config; `raw_score_0_100` and `weighted_contribution` are archival only per §7.3; `evidence_pointers` are resolved into `evidence_links` where possible and logged otherwise.
- Legacy `atlas_page_url` fields on any sheet are **not** migrated into the canonical schema. They belong to page-builder / UI metadata only (§1.8).

A separate migration doc (`MIGRATION_PLAN.md`) lists all column-by-column mappings, manual-review queues, and ordering; this spec sets the target, not the mechanical script.

---

## 12. What To Avoid

- No direct ranking of interventions from raw counts in `studies` or `anecdotes` tables.
- No semicolon-packed foreign keys in new tables (only in legacy import fields).
- No freezing of today's narratives as permanent truths.
- No LLM judgments inside scoring.
- No "answers" pages masquerading as medical advice; all outputs are descriptive and cited.
- No hand-edited live score columns. Legacy `raw_score_0_100`, `weighted_contribution`, and similar hand-assigned numeric scoring fields are archival only (§7.3).
- No UI / page-builder metadata (e.g. `atlas_page_url`) in core or Layer 2 tables. Presentation-layer fields live outside the canonical schema (§1.8).

---

## 13. How Agents Must Use This Spec

For every task (schema design, ingestion, migration, scoring, UI):

1. Re-read this spec and ensure your plan fits the architecture.
2. If you propose any change that conflicts with this spec, mark it as:
   - `PROPOSED EXTENSION`, and explain:
     - what changes,
     - why,
     - and what downstream impact it has.
3. Never introduce new entities or fields that conflict with this spec silently.
4. Keep all new tables and fields documented here once accepted.

This spec is a living document. Changes must be deliberate and versioned, not implicit in code or prompts.

---

## Version 1.1 changes

Concrete additions and clarifications made in v1.1 relative to v1.0:

- **§1.8** — new principle: UI / page-builder metadata (e.g. `atlas_page_url`) is explicitly outside the canonical schema.
- **§3.2** — `COM-0001` added as a canonical ID prefix example for combinations.
- **§3.3** — new subsection codifying legacy ID reprefixing: `CAU-####` → `HYP-####` and `CMB-####` → `COM-####`, with mandatory `node_aliases` preservation of every legacy ID (including `ANE-####`).
- **§4.1** — added `affected_population` (free text, descriptive non-scoring metadata) to `hypotheses`; codified that legacy `causes.category` values `pharmacological` and `dietary` map to canonical `other`, with raw value preserved in a `category_legacy` field or `notes`.
- **§4.5** — codified that legacy `studies.study_type = observational` maps to canonical `study_design = other`, with the raw value preserved in `sources.raw_metadata`.
- **§4.6** — codified the canonical `effect_direction` normalization rule for legacy anecdote outcomes, specifically `null` → `neutral`; `null` is no longer a valid `effect_direction` value in any new record.
- **§5** — introduced new Layer 1 edge table `gene_phenotype_edges` (§5.5), with `evidence_links` renumbered to §5.6 and its `target_type` enum extended to include `gene_phenotype_edge`.
- **§6.6** — added `interaction_warnings` as a canonical free-text safety field on `combinations`.
- **§7.3** — new subsection declaring hand-edited scoring fields (`raw_score_0_100`, `weighted_contribution`, and analogs) archival only, never surviving as live schema columns.
- **§10.1** — `node_aliases.node_type` enum extended to include `combination` and `source`; migration-time use of `node_aliases` for every reprefixed legacy ID made explicit.
- **§11.2** — migration mappings updated to reflect the changes above (ID reprefixing, category / study_type remaps, effect_direction normalization, `gene_phenotype_edges` for gene↔phenotype seed data, `interaction_warnings` as canonical, `atlas_page_url` excluded).
- **§12** — "What To Avoid" extended with the two new prohibitions: hand-edited live score columns and UI metadata in core/Layer 2 tables.
