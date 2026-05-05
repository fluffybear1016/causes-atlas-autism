{\rtf1\ansi\ansicpg1252\cocoartf2868
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 # CAUSES ATLAS \'97 AUTISM\
## Canonical Architecture & Schema Spec\
\
**Version:** 1.0  \
**Date:** 2026\uc0\u8209 04\u8209 24  \
**Owner:** Gregory J. Rigano, Esq.  \
**Status:** Canonical spec \'97 all work must conform to this document.\
\
This file is the **single source of truth** for the Autism Causes Atlas architecture, schema, scoring, and ingestion behavior.  \
Every agent or code change MUST align with this spec or clearly mark deviations as \'93Proposed Extension\'94 with justification.\
\
---\
\
## 0. Objective\
\
We are not defining the causes or treatments of autism.  \
We are building a system that **discovers, scores, and updates causal hypotheses** over time \'97 a living knowledge graph plus deterministic scoring engine.\
\
The system must:\
\
- Map all plausible autism\uc0\u8209 relevant hypotheses (environmental, biological, genetic, immunological, metabolic, microbial, social, behavioral, etc.).\
- Track mechanisms and pathways that connect those hypotheses to observable phenotypes and outcomes.\
- Integrate top\uc0\u8209 down sources (peer\u8209 reviewed literature, datasets, registries) with bottom\u8209 up sources (anecdotes, social media, real\u8209 world signals).\
- Update confidence dynamically and **deterministically** as new evidence arrives.\
- Preserve uncertainty and contradiction; avoid premature conclusions.\
- Support a derived decision layer (interventions, combinations, scores) **without contaminating discovery**.\
- Remain open\uc0\u8209 ended so new hypotheses, evidence types, pathways, and interventions can be added without redesign.\
\
---\
\
## 1. Core Principles\
\
1. **No assumed truth**\
   - Hypotheses, mechanisms, phenotypes, and interventions are not \'93true\'94 or \'93false.\'94  \
     They have **scores** and **states** based on evidence.\
\
2. **Evidence moves scores \'97 not opinions**\
   - Only structured evidence records, routed through deterministic functions, can change confidence.\
\
3. **Contradiction is a first\uc0\u8209 class object**\
   - Positive, negative, null, and mixed findings are represented explicitly.\
   - \'93Contested\'94 is a valid long\uc0\u8209 term state.\
\
4. **Two layers, strict separation**\
   - **Layer 1 (Core Causal Graph):** hypotheses, mechanisms, phenotypes, genes, evidence, and edges.\
   - **Layer 2 (Derived Decision Layer):** interventions, combinations, and graph\uc0\u8209 derived scores (e.g., CSRS\u8209 style).\
\
5. **No LLMs in scoring**\
   - Scoring is pure, deterministic code over the schema.\
   - LLMs are allowed only for:\
     - extraction/structuring of raw evidence,\
     - summarization,\
     - drafting human\uc0\u8209 readable pages,\
     - proposing ontology changes (flagged for human review).\
\
6. **Auditability**\
   - Every score and edge must be traceable back to:\
     - specific evidence records,\
     - deterministic rules,\
     - and a timestamped computation.\
\
7. **Google\uc0\u8209 Sheets\u8209 first, graph\u8209 ready schema**\
   - Persistence in v1 is Google Sheets with CSV export.\
   - Schema is normalized: **no semicolon lists as primary relationships**.\
   - Design as if we will migrate to Postgres/BigQuery/Neo4j later.\
\
---\
\
## 2. System Architecture Overview\
\
### 2.1 Two\uc0\u8209 Layer Architecture\
\
**Layer 1 \'97 Core Causal Graph (Unbiased)**\
\
Node types (at minimum):\
\
- `hypotheses`\
- `mechanisms`\
- `phenotypes`\
- `genes`\
- `sources` (artifacts)\
- `evidence_fragments`\
- `claims` (optional but recommended)\
- Typed edge/link tables between these entities\
\
**Layer 2 \'97 Derived Decision Layer**\
\
Node types:\
\
- `interventions`\
- `combinations`\
\
Derived structures:\
\
- `intervention_*` link tables (to hypotheses, mechanisms, phenotypes, genes)\
- `csrs_components` (or equivalent breakdown)\
- `csrs_history` / score history\
\
**Critical rule:**  \
Layer 2 may only read **aggregates from Layer 1**, never raw evidence rows directly for scoring.\
\
---\
\
## 3. Persistence Model\
\
### 3.1 Google Sheets & CSV\
\
- One tab = one table.\
- Every tab must export cleanly to CSV.\
- Use stable IDs.\
- Use explicit foreign keys.\
- Use normalized linking tables instead of multi\uc0\u8209 ID cells.\
\
### 3.2 ID and FK Conventions\
\
- IDs are string, prefix + zero\uc0\u8209 padded integer, e.g. `HYP-0001`, `MEC-0001`, `PHE-0001`, `GEN-0001`, `INT-0001`, etc.\
- Foreign keys always refer to these IDs.\
- Legacy semicolon lists from `causes_atlas_schema_v0.1.xlsx` are allowed only in `*_legacy` fields and may not be relied on by new code.\
\
---\
\
## 4. Core Entities (Layer 1)\
\
### 4.1 Table: `hypotheses`\
\
**Purpose:**  \
Represents any proposed driver, contributor, modifier, or correlate of autism.\
\
**Examples:**\
\
- Environmental toxin exposure (PFAS, heavy metals, pesticides, air pollution)\
- Mitochondrial dysfunction\
- Immune dysregulation / maternal immune activation\
- Microbiome alteration / dysbiosis\
- Genetic variation (de novo, inherited, CNVs)\
- Epigenetic modification\
- Perinatal hypoxia, infection, medication exposure\
- Social/behavioral exposures\
\
**Columns (minimum):**\
\
- `id` \'97 string, PK, e.g. `HYP-0001`\
- `name` \'97 canonical name\
- `category` \'97 enum: `environmental | genetic | immune | metabolic | microbial | perinatal | behavioral | social | epigenetic | other`\
- `description` \'97 plain\uc0\u8209 language description\
- `status` \'97 enum: `active | weak | disproven | contested | deprecated`\
- `confidence_score` \'97 float [0, 1], computed only\
- `evidence_count` \'97 int, computed\
- `evidence_quality_index` \'97 float [0, 1], computed\
- `consistency_index` \'97 float [0, 1], computed; penalty for high disagreement\
- `created_at` \'97 ISO\uc0\u8209 8601\
- `last_updated` \'97 ISO\uc0\u8209 8601\
- `notes` \'97 free text\
\
**No hand\uc0\u8209 edited scores.**\
\
---\
\
### 4.2 Table: `mechanisms`\
\
**Purpose:**  \
Biological/physiological processes linking hypotheses to phenotypes.\
\
**Examples:**\
\
- Oxidative stress\
- Neuroinflammation\
- Impaired methylation\
- BBB dysfunction\
- Microglial activation\
- Synaptic pruning abnormalities\
- GABA/glutamate imbalance\
- Gut\'96brain axis disruption\
- mTOR pathway dysregulation\
\
**Columns:**\
\
- `id` \'97 PK, e.g. `MEC-0001`\
- `name`\
- `category` \'97 enum: `oxidative | immune_inflammatory | metabolic | neural | endocrine | microbial | vascular | hormonal | other`\
- `description`\
- `status` \'97 enum: `active | weak | disproven | contested | deprecated`\
- `evidence_strength` \'97 float [0, 1], computed\
- `kegg_ids` \'97 optional, comma/semicolon string (for external pathway IDs)\
- `reactome_ids` \'97 optional\
- `opentargets_ids` \'97 optional\
- `created_at`\
- `last_updated`\
- `notes`\
\
---\
\
### 4.3 Table: `phenotypes`\
\
**Purpose:**  \
Observable autism subtypes / clusters / presentations.\
\
**Examples:**\
\
- Regression subtype\
- High\uc0\u8209 inflammatory profile\
- Mitochondrial subtype\
- GI\uc0\u8209 dominant subtype\
- Sensory\uc0\u8209 dominant subtype\
- Minimally verbal / nonverbal subtype\
- Sleep\uc0\u8209 disturbance\u8209 dominant subtype\
\
**Columns:**\
\
- `id` \'97 PK, e.g. `PHE-0001`\
- `name`\
- `description`\
- `diagnostic_markers` \'97 plain text; structured markers may move to a `biomarkers` table later\
- `prevalence_estimate` \'97 string or numeric + range (e.g. `"0.10\'960.15"`)\
- `status` \'97 enum: `active | tentative | deprecated`\
- `created_at`\
- `last_updated`\
- `notes`\
\
**Important:**  \
No direct `top_intervention_ids` or `top_cause_ids` fields in core. Those belong in derived views or Layer 2 tables.\
\
---\
\
### 4.4 Table: `genes`\
\
**Purpose:**  \
Genetic layer (seeded from SFARI, enriched by DisGeNET, ClinVar, gnomAD, OpenTargets, etc.).\
\
**Columns:**\
\
- `id` \'97 PK, e.g. `GEN-0001`\
- `gene_symbol`\
- `ensembl_id`\
- `sfari_score` \'97 enum: `1 | 2 | 3 | S | NA`\
- `genetic_evidence_strength` \'97 int 1\'965\
- `opentargets_score` \'97 float [0, 1]\
- `gnomad_notes` \'97 free text (variant burden)\
- `disgenet_score` \'97 float [0, 1], optional\
- `function_summary` \'97 plain English\
- `created_at`\
- `last_updated`\
- `notes`\
\
---\
\
### 4.5 Table: `sources` (artifacts)\
\
**Purpose:**  \
One row per artifact (paper, dataset, post, video, registry entry, etc.).\
\
**Columns:**\
\
- `id` \'97 PK, e.g. `SRC-000001`\
- `type` \'97 enum: `study | preprint | review | dataset | clinical | registry | anecdote | social | environmental | trial | other`\
- `platform` \'97 e.g. `pubmed | europe_pmc | biorxiv | medrxiv | reddit | youtube | x | epa | usgs | ctgov | openfda | dailyMed | rxnorm | who_ictrp | oecd | other`\
- `external_id` \'97 e.g. `PMID`, `DOI`, `Reddit id`, `YouTube video id`, `X status id`, `NCT id`\
- `title` \'97 for literature/registries\
- `url`\
- `date_published` \'97 ISO\uc0\u8209 8601\
- `date_ingested` \'97 ISO\uc0\u8209 8601\
- `study_design` \'97 for relevant sources: `rct | cohort | case_control | case_series | mechanistic | meta_analysis | review | animal | in_vitro | in_silico | epigenetic | transgenerational | other`\
- `sample_size` \'97 numeric, nullable\
- `model_system` \'97 e.g. `human`, `mouse`, `cell_line`, `rat`, etc.\
- `raw_metadata` \'97 JSON string or text blob\
- `notes`\
\
---\
\
### 4.6 Table: `evidence_fragments`\
\
**Purpose:**  \
Atomic pieces of evidence extracted from a source artifact (e.g., a specific result, table row, paragraph, or snippet).\
\
**Columns:**\
\
- `id` \'97 PK, e.g. `EVD-000001`\
- `source_id` \'97 FK \uc0\u8594  `sources.id`\
- `fragment_type` \'97 enum: `result | effect_size | association | mechanism | anecdote | observation | safety_signal | exposure_measure | other`\
- `text_excerpt` \'97 key text, up to length limit\
- `structured_payload` \'97 optional JSON/serialized structure (effect size, OR, HR, etc.)\
- `effect_direction` \'97 enum: `positive | negative | neutral | mixed | unclear` (relative to linked hypothesis/edge)\
- `strength_score` \'97 float [0, 1], function of:\
  - source type & quality,\
  - study design,\
  - sample size,\
  - risk of bias,\
  - etc.\
- `extraction_method` \'97 enum: `rule_based | llm_assisted | manual`\
- `extraction_confidence` \'97 float [0, 1]\
- `date_extracted`\
- `notes`\
\
---\
\
### 4.7 Table: `claims` (optional but recommended)\
\
**Purpose:**  \
Normalized propositions like \'93prenatal valproate exposure increases autism risk\'94 or \'93sulforaphane reduces irritability in ASD.\'94\
\
**Columns:**\
\
- `id` \'97 PK, e.g. `CLM-000001`\
- `canonical_statement` \'97 normalized English sentence\
- `statement_hash` \'97 hash to catch near\uc0\u8209 duplicates\
- `created_at`\
- `last_updated`\
- `notes`\
\
**Claims are linked to fragments and nodes via linking tables (below).**\
\
---\
\
## 5. Relationship / Edge Model\
\
All relationships are represented in separate linking tables.  \
\
### 5.1 Table: `hypothesis_mechanism_edges`\
\
**Purpose:**  \
Edges between hypotheses and mechanisms.\
\
**Columns:**\
\
- `id`\
- `hypothesis_id`\
- `mechanism_id`\
- `relation_type` \'97 enum: `acts_through | associated_with | modulated_by | leads_to`\
- `polarity` \'97 enum: `supporting | contradicting | neutral | unknown`\
- `evidence_for_count` \'97 int, computed\
- `evidence_against_count` \'97 int, computed\
- `evidence_strength_aggregate` \'97 float [0, 1], computed\
- `context_scope` \'97 string (e.g. age range, phenotype subset, geography)\
- `status` \'97 `active | deprecated`\
- `created_at`\
- `last_updated`\
\
Analogous linking tables follow the same pattern:\
\
### 5.2 Table: `mechanism_phenotype_edges`\
\
- `id`\
- `mechanism_id`\
- `phenotype_id`\
- `relation_type` \'97 e.g. `implicated_in | characteristic_of`\
- plus the same evidence/ status/ timestamps fields as above.\
\
### 5.3 Table: `gene_mechanism_edges`\
\
- `id`\
- `gene_id`\
- `mechanism_id`\
- `relation_type` \'97 e.g. `participates_in | regulates | risk_factor_for`\
- plus evidence fields.\
\
### 5.4 Table: `gene_hypothesis_edges` (optional)\
\
- `id`\
- `gene_id`\
- `hypothesis_id`\
- `relation_type`\
- evidence fields.\
\
---\
\
### 5.5 Table: `evidence_links`\
\
**Purpose:**  \
Connect evidence fragments (and optionally claims) to any node or edge they touch.\
\
**Columns:**\
\
- `id`\
- `evidence_fragment_id` \'97 FK \uc0\u8594  `evidence_fragments.id`\
- `claim_id` \'97 FK \uc0\u8594  `claims.id`, nullable\
- `target_type` \'97 enum: `hypothesis | mechanism | phenotype | gene | hypothesis_mechanism_edge | mechanism_phenotype_edge | gene_mechanism_edge | intervention | combination`\
- `target_id`\
- `effect_direction` \'97 `positive | negative | neutral | mixed | unclear` (relative to target)\
- `weight` \'97 float [0, 1], contribution to target score\
- `context_scope` \'97 as above\
- `created_at`\
- `notes`\
\
---\
\
## 6. Layer 2: Interventions & Combinations\
\
### 6.1 Table: `interventions`\
\
**Purpose:**  \
Downstream, derived layer for decision\uc0\u8209 relevant entities.\
\
**Columns:**\
\
- `id` \'97 PK, e.g. `INT-0001`\
- `name` \'97 canonical name\
- `category` \'97 enum: `drug | supplement | food | diet | herb | lifestyle | environmental | generational | combo_seed | other`\
- `directionality` \'97 enum: `treatment | prevention | cause_mitigation | generational`\
- `mechanism_summary` \'97 2\'964 sentence summary (derived from graph)\
- `dose_range` \'97 free text\
- `cost_per_month_usd` \'97 numeric\
- `otc_or_rx` \'97 enum: `otc | rx | lifestyle | environmental`\
- `pediatric_safe` \'97 enum: `yes | no | uncertain | age_restricted`\
- **No direct raw evidence fields here** (papers/anecdotes should be reachable via graph).\
- `csrs_score` (or equivalent) \'97 numeric (e.g. 0\'96100), computed only\
- `csrs_last_updated` \'97 ISO\uc0\u8209 8601\
- `status` \'97 `active | experimental | deprecated`\
- `created_at`\
- `last_updated`\
- `notes`\
\
### 6.2 Table: `intervention_mechanism_edges`\
\
- `id`\
- `intervention_id`\
- `mechanism_id`\
- `relation_type` \'97 e.g. `targets | modulates | supports`\
- evidence fields/aggregates similar to core edges.\
\
### 6.3 Table: `intervention_hypothesis_edges`\
\
### 6.4 Table: `intervention_phenotype_edges`\
\
### 6.5 Table: `intervention_gene_edges`\
\
All following the same pattern: IDs, FKs, relation_type, evidence aggregates, context, status, timestamps.\
\
### 6.6 Table: `combinations`\
\
**Purpose:**  \
First\uc0\u8209 class combinations of interventions.\
\
**Columns:**\
\
- `id` \'97 PK, e.g. `COM-0001`\
- `name`\
- `description`\
- `rationale`\
- `csrs_score` \'97 computed only\
- `csrs_last_updated`\
- `status`\
- `created_at`\
- `last_updated`\
- `notes`\
\
### 6.7 Table: `combination_members`\
\
- `id`\
- `combination_id`\
- `intervention_id`\
- `role` \'97 optional (e.g. `core | adjunct | supportive`)\
- `created_at`\
\
---\
\
## 7. Evidence Quality and Scoring Engine\
\
### 7.1 Evidence\uc0\u8209 quality components (for hypotheses/mechanisms/phenotypes/genes)\
\
The **confidence score** for core nodes is a deterministic function of:\
\
- `evidence_count` \'97 number of independent sources.\
- `evidence_quality` \'97 function of:\
  - study type (RCT > cohort > case\uc0\u8209 control > case\u8209 series > mechanistic > anecdote),\
  - sample size,\
  - replication/meta\uc0\u8209 analysis,\
  - registry/dataset robustness.\
- `consistency` \'97 degree of agreement across effect directions.\
- `mechanism_coherence` \'97 overlap with high\uc0\u8209 confidence biological pathways (KEGG, Reactome, OpenTargets).\
- `genetic_support` \'97 SFARI + OpenTargets + variant burden (for genetic hypotheses).\
- `cross_phenotype_convergence` \'97 number and coherence of phenotypes implicated.\
- `epigenetic/generational` evidence.\
- `trend/emerging_signal` \'97 recent increase in evidence (all types).\
- `in_silico_functional` (optional).\
- `replication/independence` \'97 diversity of institutions/countries.\
- `source_type_diversity` \'97 mixture of studies, datasets, clinical, registry, anecdotes, etc.\
\
You do NOT need to fix exact weights in this spec, but you must:\
\
- Define each component clearly.\
- Provide pseudo\uc0\u8209 formulas for how node scores are computed from evidence and edges.\
- State clearly that these live in config and can be tuned, but reruns are deterministic.\
\
### 7.2 Intervention / CSRS\uc0\u8209 style scoring (Layer 2)\
\
Intervention/combination scores are derived only from:\
\
- Which hypotheses they target.\
- The strength of those hypotheses and mechanisms in the graph.\
- Evidence of effect on relevant phenotypes.\
- Genetic coherence (where applicable).\
- Safety/practicality (from FAERS, DailyMed, cost, OTC/Rx, pediatric safety).\
- Trend/emerging signals (including social signals with low base weight).\
- Combination synergy where applicable.\
\
**Forbidden:**  \
No direct \'93count studies where `intervention_id = X`\'94 or \'93count anecdotes with `intervention_id = X`\'94 in scoring. All such counts must be routed through Layer 1 nodes/edges and their evidence aggregates.\
\
---\
\
## 8. Ingestion System\
\
### 8.1 Top\uc0\u8209 down inputs\
\
- **Literature**\
  - PubMed E\uc0\u8209 utilities\
  - Europe PMC\
  - SemMedDB\
  - bioRxiv\
  - medRxiv\
\
- **Biology / functional**\
  - OpenTargets (GraphQL)\
  - KEGG\
  - Reactome\
  - STRING\
  - GTEx\
  - ChEMBL\
  - AlphaFold\
  - LINCS L1000 / Clue.io (optional)\
\
- **Genetics**\
  - SFARI Gene (CSV)\
  - DisGeNET\
  - ClinVar\
  - gnomAD\
\
- **Clinical / regulatory**\
  - ClinicalTrials.gov v2\
  - OpenFDA FAERS\
  - DailyMed\
  - RxNorm\
  - WHO ICTRP\
\
- **Environmental**\
  - EPA ECHO\
  - EPA Air Quality System\
  - USGS Water Quality\
  - State environmental databases\
  - OECD / WHO exposure registries\
\
### 8.2 Bottom\uc0\u8209 up inputs\
\
- Reddit (autism\uc0\u8209 related subreddits, public JSON/PRAW)\
- YouTube (captions + metadata via YouTube Data API)\
- X (Twitter):\
  - Browser\uc0\u8209 visible pages,\
  - compliance\uc0\u8209 aware scraping/automation,\
  - and/or Grok/xAI or similar for real\uc0\u8209 time X access as soon as available.\
- Blogs, forums, parent/clinician websites (RSS or sitemap\uc0\u8209 based).\
- Podcasts (transcripts where available).\
\
### 8.3 Ingestion pipeline (per artifact)\
\
1. Fetch & parse.\
2. Create/append `sources` row.\
3. Extract `evidence_fragments`:\
   - Prefer deterministic pattern/keyword/structure rules.\
   - Use LLM only when rules fail to capture necessary structure.\
4. For each fragment, infer:\
   - effect_direction,\
   - strength_score,\
   - candidate links to hypotheses/mechanisms/phenotypes/genes/interventions.\
5. Create `evidence_links` rows:\
   - deterministic rules first (based on keywords, ontology mappings, IDs).\
   - LLM suggestions flagged as low\uc0\u8209 confidence until confirmed.\
6. Recompute relevant node and edge scores using deterministic scoring engine.\
7. Append `score_history` records capturing:\
   - old score,\
   - new score,\
   - component breakdown,\
   - evidence that changed.\
\
---\
\
## 9. Contradiction, Uncertainty, & Temporal Behavior\
\
### 9.1 Contradiction\
\
- Every `evidence_link` carries an `effect_direction`.\
- Node/edge `consistency_index` reflects the distribution of positive/negative/neutral evidence.\
- Hypotheses, mechanisms, phenotypes, and interventions can have status `contested`.\
\
### 9.2 Temporal\
\
- `score_history` table:\
  - `id`\
  - `target_type` (`hypothesis | mechanism | phenotype | gene | intervention | combination`)\
  - `target_id`\
  - `score_type` (`confidence | csrs | other`)\
  - `old_score`\
  - `new_score`\
  - `component_breakdown` (JSON)\
  - `evidence_delta_ids` (list of `evidence_fragment_id`s)\
  - `computed_at`\
\
No overwriting without history.\
\
---\
\
## 10. Ontology Governance\
\
### 10.1 Canonical vs aliases\
\
Add a `node_aliases` table:\
\
- `id`\
- `node_type` (`hypothesis | mechanism | phenotype | gene | intervention`)\
- `node_id`\
- `alias`\
- `source` (who/what introduced alias)\
- `created_at`\
\
### 10.2 Merge / split / deprecate\
\
- Duplicates detected by string similarity and manual review.\
- Merges tracked via a `merged_into` field or dedicated `node_merges` table.\
- Deprecated nodes retain IDs, flagged `status = deprecated`, but no longer accumulate new evidence.\
\
All ontology changes should be:\
\
- Logged,\
- Justified,\
- Optionally assisted by LLM proposals but finalized by human judgment.\
\
---\
\
## 11. Migration from `causes_atlas_schema_v0.1.xlsx`\
\
### 11.1 General approach\
\
- Treat `causes_atlas_schema_v0.1.xlsx` as a **legacy seed**, not the target.\
- Use its:\
  - interventions,\
  - causes,\
  - studies,\
  - anecdotes,\
  - combinations,\
  - phenotypes,\
  - genes,\
  - csrscomponents  \
  as seed content to be rewritten into the new schema.\
\
### 11.2 Example mappings (high level)\
\
- `interventions` sheet \uc0\u8594  `interventions` + `intervention_*_edges` tables, with `sourcepmids` / `sourceanecdoteids` turned into proper `evidence_links`.\
- `causes` sheet \uc0\u8594  `hypotheses` table + possibly `hypothesis_mechanism_edges`.\
- `studies` sheet \uc0\u8594  `sources` (type=study) + `evidence_fragments`.\
- `anecdotes` sheet \uc0\u8594  `sources` (type=anecdote|social) + `evidence_fragments`.\
- `combinations` sheet \uc0\u8594  `combinations` + `combination_members`.\
- `phenotypes` sheet \uc0\u8594  `phenotypes` table, dropping direct `topinterventionids` in core.\
- `genes` sheet \uc0\u8594  `genes` + gene\u8209 related linking tables.\
- `csrscomponents` sheet \uc0\u8594  legacy view to be replaced by new, graph\u8209 based components for interventions.\
\
A separate migration doc can list all column\uc0\u8209 by\u8209 column mappings; this spec sets the target, not the mechanical script.\
\
---\
\
## 12. What To Avoid\
\
- No direct ranking of interventions from raw counts in `studies` or `anecdotes` tables.\
- No semicolon\uc0\u8209 packed foreign keys in new tables (only in legacy import fields).\
- No freezing of today\'92s narratives as permanent truths.\
- No LLM judgments inside scoring.\
- No \'93answers\'94 pages masquerading as medical advice; all outputs are descriptive and cited.\
\
---\
\
## 13. How Agents Must Use This Spec\
\
For every task (schema design, ingestion, migration, scoring, UI):\
\
1. Re\uc0\u8209 read this spec and ensure your plan fits the architecture.\
2. If you propose any change that conflicts with this spec, mark it as:\
   - `PROPOSED EXTENSION`, and explain:\
     - what changes,\
     - why,\
     - and what downstream impact it has.\
3. Never introduce new entities or fields that conflict with this spec silently.\
4. Keep all new tables and fields documented here once accepted.\
\
This spec is a living document. Changes must be deliberate and versioned, not implicit in code or prompts.\
}