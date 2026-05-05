# CAUSES ATLAS — AUTISM
## Canonical Architecture & Schema Spec

**Version:** 1.2
**Date:** 2026-04-27
**Owner:** Gregory J. Rigano, Esq.
**Status:** Canonical spec — all work must conform to this document.
**Predecessor:** v1.1

This v1.2 update incorporates three approved schema extensions surfaced by nine expansion cycles (v1.0 → v1.9):

- **§5.7 (NEW) `hypothesis_hypothesis_edges`** — supports causal chains (upstream → downstream hypotheses) so the graph can represent realities like "glyphosate exposure → microbiome dysbiosis → gut-brain disruption → behavior."
- **§7.2.1 (NEW) Prevention vs. treatment dual scoring** — `csrs_prevention_score` and `csrs_treatment_score` distinct from the unified `csrs_score`, so prevention-directionality interventions (methylated folate preconception, iodine, MBSR for maternal stress) get the prevention-specific weighting they deserve.
- **§14 (NEW) Ingestion pipeline contract** — formal interface for the `ingest()` function family that turns a single artifact (PMID, DOI, URL, pasted text) into appended rows + recomputed scores + score_history entries.

The rest of the spec is identical to v1.1. Sections renumbered only where new subsections were inserted.

---

## 0. Objective

We are not defining the causes or treatments of autism. We are building a system that **discovers, scores, and updates causal hypotheses** over time — a living knowledge graph plus deterministic scoring engine.

The system must:

- Map all plausible autism-relevant hypotheses (environmental, biological, genetic, immunological, metabolic, microbial, social, behavioral, etc.).
- Track mechanisms and pathways that connect those hypotheses to observable phenotypes and outcomes.
- Integrate top-down sources (peer-reviewed literature, datasets, registries) with bottom-up sources (anecdotes, social media, real-world signals).
- Update confidence dynamically and **deterministically** as new evidence arrives.
- Preserve uncertainty and contradiction; avoid premature conclusions.
- Support a derived decision layer (interventions, combinations, scores) **without contaminating discovery**.
- Remain open-ended so new hypotheses, evidence types, pathways, and interventions can be added without redesign.
- **(NEW v1.2)** Represent multi-step causal chains explicitly so upstream environmental causes can route through downstream biological consequences to phenotype.
- **(NEW v1.2)** Distinguish prevention from treatment scoring so the right interventions surface for the right life-stage decision.

---

## 1. Core Principles

(Identical to v1.1 — abbreviated here for space.)

1. No assumed truth; scores and states only.
2. Evidence moves scores — not opinions.
3. Contradiction is a first-class object; `contested` is a valid permanent state.
4. Two layers, strict separation: Layer 1 (causal graph) vs Layer 2 (decision).
5. No LLMs in scoring; deterministic code only.
6. Auditability: every score traces to evidence + rules + timestamp.
7. Google-Sheets-first, graph-ready normalized schema.
8. UI metadata lives outside the schema.

---

## 2. System Architecture Overview

(Identical to v1.1.)

---

## 3. Persistence Model

(Identical to v1.1: 3.1 Sheets/CSV; 3.2 ID conventions; 3.3 Legacy reprefixing CAU→HYP, CMB→COM with `node_aliases` preservation.)

---

## 4. Core Entities (Layer 1)

(Identical to v1.1: hypotheses, mechanisms, phenotypes, genes, sources, evidence_fragments, claims.)

---

## 5. Relationship / Edge Model

### 5.1 `hypothesis_mechanism_edges`
### 5.2 `mechanism_phenotype_edges`
### 5.3 `gene_mechanism_edges`
### 5.4 `gene_hypothesis_edges` (optional)
### 5.5 `gene_phenotype_edges` (added in v1.1)
### 5.6 `evidence_links`

(All identical to v1.1.)

### 5.7 (NEW v1.2) `hypothesis_hypothesis_edges`

**Purpose:**
Represent causal-chain relationships between hypotheses where one is upstream of another. Without this, the atlas can only model "this hypothesis causes autism" — not "this hypothesis causes another hypothesis which causes autism." Real autism causation is multi-step (glyphosate → microbiome dysbiosis → gut-brain disruption → behavior; maternal autoimmunity → maternal immune activation → fetal neuroinflammation → regression phenotype), so the schema must support this.

**Columns:**

- `id` — PK, e.g. `HHE-00001`
- `upstream_hypothesis_id` — FK → `hypotheses.id` (the cause)
- `downstream_hypothesis_id` — FK → `hypotheses.id` (the consequence)
- `relation_type` — enum: `upstream_of | exacerbates | modulates | preconditions | comorbid_with`
- `polarity` — enum: `supporting | contradicting | neutral | unknown`
- `evidence_for_count` — int, computed
- `evidence_against_count` — int, computed
- `evidence_strength_aggregate` — float [0, 1], computed
- `context_scope` — string (life stage, population subset)
- `status` — `active | deprecated`
- `created_at` — ISO-8601
- `last_updated` — ISO-8601

**Cycle prevention:**
The graph of `hypothesis_hypothesis_edges` must remain a DAG. The ingestion pipeline rejects edges that would close a cycle. Bidirectional relationships are represented as two distinct edges (A → B + B → A) and flagged for manual review.

**Scoring impact:**
A hypothesis's `confidence_score` (per §7.1) gains a small contribution from the *aggregate evidence on its outgoing upstream-of edges* — the engine recognizes that being mechanistically positioned upstream of a well-evidenced hypothesis is itself supportive evidence. The contribution is capped at 0.10 of total weight to avoid a single chain dominating.

**`evidence_links` extension:**
The `target_type` enum on `evidence_links` (§5.6) gains the value `hypothesis_hypothesis_edge` so individual papers can link directly to a causal-chain edge.

---

## 6. Layer 2: Interventions & Combinations

(Identical to v1.1.)

---

## 7. Evidence Quality and Scoring Engine

### 7.1 Evidence-quality components

(Identical to v1.1.)

### 7.2 Intervention / CSRS-style scoring

(Identical to v1.1.)

### 7.2.1 (NEW v1.2) Prevention vs. treatment dual scoring

The unified `csrs_score` is retained for backwards compatibility. v1.2 adds two new computed columns to `interventions` and `combinations`:

- **`csrs_prevention_score`** ∈ [0, 100] — applies when the intervention's `directionality` is `prevention` or `cause_mitigation`. Re-weighted to emphasize:
  - Safety (×1.5 vs unified weight) — prevention is given to people with no current condition
  - Cost-effectiveness (×1.3 vs unified weight) — population-scale interventions need to be affordable
  - Hypothesis alignment to upstream causes (via the new `hypothesis_hypothesis_edges`)
  - Maternal/preconception window relevance
  - Genetic coherence (down-weighted: prevention rarely targets genes)
- **`csrs_treatment_score`** ∈ [0, 100] — applies when `directionality` is `treatment`. Re-weighted to emphasize:
  - RCT evidence on the established phenotype
  - Mechanism strength on already-established disease
  - Replication
  - Down-weighted: trend signals (treatment for current condition isn't about emerging signals)

For interventions with `directionality` other than the above (e.g. `generational`), both scores are computed at neutral weighting and the system shows whichever is higher.

**Default display rule:** when querying the atlas for "best preventive interventions for women considering pregnancy," the system sorts by `csrs_prevention_score`. When querying "best treatments for an existing diagnosis," it sorts by `csrs_treatment_score`. The unified `csrs_score` is the single-context fallback.

**Column additions:**
- `interventions.csrs_prevention_score` (computed only)
- `interventions.csrs_treatment_score` (computed only)
- `interventions.csrs_prevention_last_updated` (ISO-8601)
- `interventions.csrs_treatment_last_updated` (ISO-8601)
- `combinations.csrs_prevention_score` (computed only)
- `combinations.csrs_treatment_score` (computed only)
- `combinations.csrs_prevention_last_updated` (ISO-8601)
- `combinations.csrs_treatment_last_updated` (ISO-8601)

### 7.3 Hand-edited scoring fields

(Identical to v1.1 — archival only.)

---

## 8. Ingestion System

(Identical to v1.1, but see §14 for the formal pipeline contract introduced in v1.2.)

---

## 9. Contradiction, Uncertainty & Temporal Behavior

(Identical to v1.1.)

---

## 10. Ontology Governance

(Identical to v1.1.)

---

## 11. Migration from v0.1

(Identical to v1.1.)

---

## 12. What To Avoid

(Identical to v1.1.)

---

## 13. How Agents Must Use This Spec

(Identical to v1.1.)

---

## 14. (NEW v1.2) Ingestion Pipeline Contract

The `ingest()` function family is the formal interface for adding new evidence to the atlas. It implements spec §8.3's per-artifact pipeline.

### 14.1 Supported input modalities

- `ingest_pmid(pmid)` — fetches from PubMed/E-utilities via NCBI's public API (no auth required); returns title, abstract, authors, year, journal, MeSH terms.
- `ingest_doi(doi)` — resolves DOI to publisher URL; falls back to ingest_url.
- `ingest_url(url)` — fetches arbitrary URL; uses content-type heuristics (HTML → readability extraction; PDF → pdfminer; text → as-is).
- `ingest_paste(text, source_metadata)` — accepts already-extracted text content (e.g. X/Twitter post pasted by user, paywalled article copied manually). The user provides minimal source_metadata: `{title, year, platform, external_id, type}`. This is the bridge that solves the X-authentication wall problem.

### 14.2 Per-call output contract

Each `ingest_*` call returns:

```
IngestResult:
  source_id: SRC-######      # the new sources row
  fragment_id: EVD-######    # the new evidence_fragments row
  proposed_links: [          # candidate evidence_links awaiting review
    { target_type, target_id, target_name, effect_direction, confidence }
  ]
  score_deltas: [             # how much downstream scores moved
    { node_id, score_type, old_score, new_score, components_changed }
  ]
  manual_review_flags: [...]  # anything the engine couldn't auto-resolve
```

### 14.3 Determinism guarantees

- Re-ingesting the same artifact (same PMID, DOI, or URL) produces identical row IDs and zero score deltas. Implemented via `node_aliases` lookup before allocating new IDs.
- Concurrent ingestion is serialized via a per-table monotonic ID counter.
- Score recomputation runs the unmodified scoring engine (§7.1, §7.2, §7.2.1) — no shortcut paths.

### 14.4 Manual-review budget

Auto-acceptance criteria: confidence ≥ 0.80 on entity recognition AND fragment_type ∈ {result, mechanism, association} AND no contradicting evidence within ±0.20 weight.

Anything below threshold goes to the manual review queue with a structured reason. The pipeline is honest about its limitations — it doesn't fabricate edges.

### 14.5 Provenance audit

Every row created by ingestion has `raw_metadata.added_via_ingest = true` and a back-pointer to the input artifact. Provenance is fully reconstructible.

---

**End of CAUSES_ATLAS_AUTISM_SPEC v1.2.**

## v1.2 changes (vs v1.1)

- **§5.7** new — `hypothesis_hypothesis_edges` schema for upstream-downstream causal chains.
- **§5.6** extended — `evidence_links.target_type` enum gains `hypothesis_hypothesis_edge`.
- **§7.2.1** new — `csrs_prevention_score` and `csrs_treatment_score` dual scoring with explicit weight profiles.
- **§4.1 / §6.1 / §6.6** column additions — `csrs_prevention_score`, `csrs_treatment_score`, and their `_last_updated` timestamps on `interventions` and `combinations`.
- **§14** new — formal ingestion pipeline contract covering PMID, DOI, URL, and paste-text modalities.
- **§14.4** new — manual-review budget criteria for auto-acceptance.
