#!/usr/bin/env python3
"""
run_migration.py

Migration of causes_atlas_schema_v0.1.xlsx into the normalized Causes Atlas
(Autism) v1.1 schema. One runnable script, Python 3 + pandas.

Binding documents:
  - CAUSES_ATLAS_AUTISM_SPEC_v1.1.md
  - MIGRATION_PLAN.md
  - MIGRATION_IMPLEMENTATION.md

Behavior:
  - Reads the legacy workbook.
  - Builds every target table as an in-memory DataFrame.
  - Writes one CSV per table to output/.
  - Writes logs (orphan FKs, unresolved pointers, manual review queue,
    enum remaps, node_aliases emission, per-row mapping log) to logs/.
  - Does NOT compute any score. Computed columns are left blank.
  - Uses a single run-wide migration timestamp for all created_at / last_updated
    / date_ingested / date_extracted on migrated rows.

Usage:
    pip install pandas openpyxl
    python run_migration.py

Expects the legacy file in the current working directory:
    causes_atlas_schema_v0.1.xlsx
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

# ----------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------

LEGACY_FILE = "causes_atlas_schema_v0.1.xlsx"
OUTPUT_DIR = Path("output")
LOGS_DIR = Path("logs")

# Spec v1.1 enums — used for validation and remap.
HYPOTHESIS_CATEGORY_ENUM = {
    "environmental", "genetic", "immune", "metabolic", "microbial",
    "perinatal", "behavioral", "social", "epigenetic", "other",
}
HYPOTHESIS_CATEGORY_LEGACY_REMAP = {
    "environmental": "environmental",
    "pharmacological": "other",
    "dietary": "other",
}

STUDY_DESIGN_ENUM = {
    "rct", "cohort", "case_control", "case_series", "mechanistic",
    "meta_analysis", "review", "animal", "in_vitro", "in_silico",
    "epigenetic", "transgenerational", "other",
}
STUDY_TYPE_LEGACY_REMAP = {
    "rct": "rct",
    "case_series": "case_series",
    "review": "review",
    "meta_analysis": "meta_analysis",
    "mechanistic": "mechanistic",
    "observational": "other",  # per spec v1.1 §4.5
}

ANECDOTE_OUTCOME_REMAP = {
    "positive": "positive",
    "negative": "negative",
    "null": "neutral",        # per spec v1.1 §4.6
    "mixed": "mixed",
}

# Seed mechanisms per spec §4.2 examples — always present in the new table,
# regardless of what extraction finds.
SEED_MECHANISMS = [
    ("Oxidative stress", "oxidative"),
    ("Neuroinflammation", "immune_inflammatory"),
    ("Impaired methylation", "metabolic"),
    ("BBB dysfunction", "vascular"),
    ("Microglial activation", "immune_inflammatory"),
    ("Synaptic pruning abnormalities", "neural"),
    ("GABA/glutamate imbalance", "neural"),
    ("Gut-brain axis disruption", "microbial"),
    ("mTOR pathway dysregulation", "metabolic"),
]

# Controlled vocabulary for rule-based mechanism extraction from free text.
# Keys are lowercased phrases to search; values are canonical names matching
# entries in SEED_MECHANISMS or extensions of it.
MECHANISM_VOCAB = {
    "oxidative stress": "Oxidative stress",
    "oxidative damage": "Oxidative stress",
    "reactive oxygen species": "Oxidative stress",
    "nrf2": "Oxidative stress",
    "neuroinflammation": "Neuroinflammation",
    "neuroinflammatory": "Neuroinflammation",
    "inflammation": "Neuroinflammation",
    "cytokine": "Neuroinflammation",
    "methylation": "Impaired methylation",
    "folate": "Impaired methylation",
    "homocysteine": "Impaired methylation",
    "blood-brain barrier": "BBB dysfunction",
    "blood brain barrier": "BBB dysfunction",
    "bbb": "BBB dysfunction",
    "microglia": "Microglial activation",
    "microglial": "Microglial activation",
    "synaptic pruning": "Synaptic pruning abnormalities",
    "synaptic": "Synaptic pruning abnormalities",
    "gaba": "GABA/glutamate imbalance",
    "glutamate": "GABA/glutamate imbalance",
    "gaba/glutamate": "GABA/glutamate imbalance",
    "gut-brain": "Gut-brain axis disruption",
    "gut brain": "Gut-brain axis disruption",
    "microbiome": "Gut-brain axis disruption",
    "dysbiosis": "Gut-brain axis disruption",
    "mtor": "mTOR pathway dysregulation",
    "mitochondrial": "Mitochondrial dysfunction",
}

# Mitochondrial dysfunction isn't in the nine spec examples but is called out
# as a hypothesis/mechanism example across both spec and legacy text. Added
# when encountered. We keep a registry of extra canonical names we coin here.
EXTRA_SEED_MECHANISMS = [
    ("Mitochondrial dysfunction", "metabolic"),
]

# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------

def now_iso() -> str:
    """Single run-wide migration timestamp (UTC, ISO-8601)."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")


def split_packed(value) -> list[str]:
    """Split a semicolon-packed legacy cell into a list of clean tokens.
    Returns [] for None/NaN/empty."""
    if value is None:
        return []
    if isinstance(value, float) and pd.isna(value):
        return []
    s = str(value).strip()
    if not s or s.lower() == "none" or s.lower() == "nan":
        return []
    return [tok.strip() for tok in s.split(";") if tok.strip()]


def reprefix(legacy_id: str, new_prefix: str) -> str:
    """Swap the prefix on a legacy ID of the form 'XXX-####'."""
    m = re.match(r"^[A-Za-z]+-(\d+)$", str(legacy_id).strip())
    if not m:
        return str(legacy_id)
    return f"{new_prefix}-{m.group(1)}"


def pad_id(prefix: str, n: int, width: int) -> str:
    return f"{prefix}-{str(n).zfill(width)}"


def to_json_str(d: dict) -> str:
    """JSON-encode a dict for embedding in a single CSV cell.
    Drops None keys to keep cells compact."""
    clean = {k: v for k, v in d.items() if v is not None and v != ""}
    return json.dumps(clean, ensure_ascii=False)


def nullable(v):
    """Normalize pandas NaN/None to empty string for CSV output."""
    if v is None:
        return ""
    if isinstance(v, float) and pd.isna(v):
        return ""
    return v


# ----------------------------------------------------------------------------
# Schema header contracts — exactly the headers defined previously.
# ----------------------------------------------------------------------------

HEADERS = {
    "hypotheses": [
        "id", "name", "category", "description", "affected_population",
        "status", "confidence_score", "evidence_count",
        "evidence_quality_index", "consistency_index",
        "created_at", "last_updated", "notes",
        "category_legacy", "evidence_strength_legacy",
        "epidemiological_strength_legacy",
        "mitigation_intervention_ids_legacy", "source_pmids_legacy",
        "csrs_score_legacy", "csrs_last_updated_legacy",
    ],
    "mechanisms": [
        "id", "name", "category", "description", "status",
        "evidence_strength", "kegg_ids", "reactome_ids",
        "opentargets_ids", "created_at", "last_updated", "notes",
    ],
    "phenotypes": [
        "id", "name", "description", "diagnostic_markers",
        "prevalence_estimate", "status", "created_at", "last_updated",
        "notes", "top_intervention_ids_legacy", "top_cause_ids_legacy",
    ],
    "genes": [
        "id", "gene_symbol", "ensembl_id", "sfari_score",
        "genetic_evidence_strength", "opentargets_score",
        "gnomad_notes", "disgenet_score", "function_summary",
        "created_at", "last_updated", "notes",
        "associated_phenotype_ids_legacy",
        "linked_intervention_ids_legacy",
    ],
    "sources": [
        "id", "type", "platform", "external_id", "title", "url",
        "date_published", "date_ingested", "study_design",
        "sample_size", "model_system", "raw_metadata", "notes",
    ],
    "evidence_fragments": [
        "id", "source_id", "fragment_type", "text_excerpt",
        "structured_payload", "effect_direction", "strength_score",
        "extraction_method", "extraction_confidence", "date_extracted",
        "notes",
    ],
    "evidence_links": [
        "id", "evidence_fragment_id", "claim_id", "target_type",
        "target_id", "effect_direction", "weight", "context_scope",
        "created_at", "notes",
    ],
    "interventions": [
        "id", "name", "category", "directionality",
        "mechanism_summary", "dose_range", "cost_per_month_usd",
        "otc_or_rx", "pediatric_safe", "csrs_score",
        "csrs_last_updated", "status", "created_at", "last_updated",
        "notes", "targets_legacy", "source_pmids_legacy",
        "source_anecdote_ids_legacy", "csrs_score_legacy",
        "csrs_last_updated_legacy",
    ],
    "combinations": [
        "id", "name", "description", "rationale",
        "interaction_warnings", "csrs_score", "csrs_last_updated",
        "status", "created_at", "last_updated", "notes",
        "member_intervention_ids_legacy", "csrs_score_legacy",
        "csrs_last_updated_legacy",
    ],
    "combination_members": [
        "id", "combination_id", "intervention_id", "role", "created_at",
    ],
    "node_aliases": [
        "id", "node_type", "node_id", "alias", "source", "created_at",
    ],
    "score_history": [
        "id", "target_type", "target_id", "score_type", "old_score",
        "new_score", "component_breakdown", "evidence_delta_ids",
        "computed_at",
    ],
    # Edge tables — uniform shape.
    "hypothesis_mechanism_edges": [
        "id", "hypothesis_id", "mechanism_id", "relation_type",
        "polarity", "evidence_for_count", "evidence_against_count",
        "evidence_strength_aggregate", "context_scope", "status",
        "created_at", "last_updated",
    ],
    "mechanism_phenotype_edges": [
        "id", "mechanism_id", "phenotype_id", "relation_type",
        "polarity", "evidence_for_count", "evidence_against_count",
        "evidence_strength_aggregate", "context_scope", "status",
        "created_at", "last_updated",
    ],
    "gene_mechanism_edges": [
        "id", "gene_id", "mechanism_id", "relation_type",
        "polarity", "evidence_for_count", "evidence_against_count",
        "evidence_strength_aggregate", "context_scope", "status",
        "created_at", "last_updated",
    ],
    "gene_hypothesis_edges": [
        "id", "gene_id", "hypothesis_id", "relation_type",
        "polarity", "evidence_for_count", "evidence_against_count",
        "evidence_strength_aggregate", "context_scope", "status",
        "created_at", "last_updated",
    ],
    "gene_phenotype_edges": [
        "id", "gene_id", "phenotype_id", "relation_type",
        "polarity", "evidence_for_count", "evidence_against_count",
        "evidence_strength_aggregate", "context_scope", "status",
        "created_at", "last_updated",
    ],
    "intervention_mechanism_edges": [
        "id", "intervention_id", "mechanism_id", "relation_type",
        "polarity", "evidence_for_count", "evidence_against_count",
        "evidence_strength_aggregate", "context_scope", "status",
        "created_at", "last_updated",
    ],
    "intervention_hypothesis_edges": [
        "id", "intervention_id", "hypothesis_id", "relation_type",
        "polarity", "evidence_for_count", "evidence_against_count",
        "evidence_strength_aggregate", "context_scope", "status",
        "created_at", "last_updated",
    ],
    "intervention_phenotype_edges": [
        "id", "intervention_id", "phenotype_id", "relation_type",
        "polarity", "evidence_for_count", "evidence_against_count",
        "evidence_strength_aggregate", "context_scope", "status",
        "created_at", "last_updated",
    ],
    "intervention_gene_edges": [
        "id", "intervention_id", "gene_id", "relation_type",
        "polarity", "evidence_for_count", "evidence_against_count",
        "evidence_strength_aggregate", "context_scope", "status",
        "created_at", "last_updated",
    ],
}


# ----------------------------------------------------------------------------
# Aliases registry (shared across builders)
# ----------------------------------------------------------------------------

class AliasRegistry:
    """Keeps a running list of (node_type, node_id, alias) tuples so every
    builder can register aliases without re-reading CSVs."""
    def __init__(self, run_ts: str):
        self._rows = []
        self._run_ts = run_ts
        self._next = 1

    def add(self, node_type: str, node_id: str, alias: str,
            source: str = "legacy_v0.1"):
        if alias is None or str(alias).strip() == "":
            return
        self._rows.append({
            "id": pad_id("ALS", self._next, 6),
            "node_type": node_type,
            "node_id": node_id,
            "alias": alias,
            "source": source,
            "created_at": self._run_ts,
        })
        self._next += 1

    def to_df(self) -> pd.DataFrame:
        df = pd.DataFrame(self._rows, columns=HEADERS["node_aliases"])
        return df


# ----------------------------------------------------------------------------
# Log buffers
# ----------------------------------------------------------------------------

class LogBuffer:
    """Accumulates log rows and writes them to logs/*.csv at the end."""
    def __init__(self):
        self.orphan_fks = []
        self.unresolved_pointers = []
        self.manual_review = []
        self.enum_remaps = []
        self.row_map = []
        self.extraction = []

    def orphan(self, source_sheet, source_row, column, token, expected):
        self.orphan_fks.append({
            "source_sheet": source_sheet,
            "source_row": source_row,
            "source_column": column,
            "token": token,
            "expected_target_type": expected,
        })

    def unresolved(self, row, intervention_id, component, pointer, reason):
        self.unresolved_pointers.append({
            "legacy_row": row,
            "intervention_id": intervention_id,
            "component": component,
            "pointer": pointer,
            "reason": reason,
        })

    def review(self, category, target_table, target_id, legacy_row, reason,
               priority="normal"):
        self.manual_review.append({
            "category": category,
            "target_table": target_table,
            "target_id": target_id,
            "legacy_row": legacy_row,
            "reason": reason,
            "priority": priority,
        })

    def remap(self, sheet, row, column, old, new, reason):
        self.enum_remaps.append({
            "sheet": sheet, "row": row, "column": column,
            "old_value": old, "new_value": new, "reason": reason,
        })

    def mapped(self, sheet, row, pk, table, new_pk, op, note=""):
        self.row_map.append({
            "legacy_sheet": sheet, "legacy_row": row, "legacy_pk": pk,
            "target_table": table, "target_pk": new_pk,
            "operation": op, "notes": note,
        })

    def extracted(self, sheet, row, column, phrase, canonical, method,
                  flagged=False):
        self.extraction.append({
            "sheet": sheet, "row": row, "column": column,
            "phrase": phrase, "canonical": canonical,
            "method": method, "flagged": flagged,
        })

    def flush(self, logs_dir: Path):
        def write(name, rows, cols):
            df = pd.DataFrame(rows, columns=cols) if rows else pd.DataFrame(
                columns=cols)
            df.to_csv(logs_dir / name, index=False)
        write("orphan_fks.csv", self.orphan_fks,
              ["source_sheet", "source_row", "source_column",
               "token", "expected_target_type"])
        write("unresolved_pointers.csv", self.unresolved_pointers,
              ["legacy_row", "intervention_id", "component",
               "pointer", "reason"])
        write("manual_review_queue.csv", self.manual_review,
              ["category", "target_table", "target_id", "legacy_row",
               "reason", "priority"])
        write("enum_remaps.csv", self.enum_remaps,
              ["sheet", "row", "column", "old_value", "new_value",
               "reason"])
        write("row_mapping.csv", self.row_map,
              ["legacy_sheet", "legacy_row", "legacy_pk",
               "target_table", "target_pk", "operation", "notes"])
        write("extraction_log.csv", self.extraction,
              ["sheet", "row", "column", "phrase", "canonical",
               "method", "flagged"])


# ----------------------------------------------------------------------------
# Loaders
# ----------------------------------------------------------------------------

def load_legacy(path: str) -> dict[str, pd.DataFrame]:
    xl = pd.ExcelFile(path)
    dfs = {}
    for name in xl.sheet_names:
        dfs[name] = xl.parse(name)
    return dfs


# ----------------------------------------------------------------------------
# Builders — Priority tables (fully implemented)
# ----------------------------------------------------------------------------

def build_phenotypes(legacy: dict, ts: str, aliases: AliasRegistry,
                     logs: LogBuffer) -> pd.DataFrame:
    src = legacy["phenotypes"]
    rows = []
    for i, r in src.iterrows():
        rid = str(r["id"]).strip()
        rows.append({
            "id": rid,
            "name": nullable(r.get("name")),
            "description": nullable(r.get("phenotype_description")),
            "diagnostic_markers": nullable(r.get("diagnostic_markers")),
            "prevalence_estimate": nullable(r.get("prevalence_estimate")),
            "status": "active",
            "created_at": ts,
            "last_updated": ts,
            "notes": nullable(r.get("notes")),
            "top_intervention_ids_legacy":
                nullable(r.get("top_intervention_ids")),
            "top_cause_ids_legacy": nullable(r.get("top_cause_ids")),
        })
        aliases.add("phenotype", rid, rid)
        logs.mapped("phenotypes", i + 2, rid, "phenotypes", rid, "copy")
        if r.get("top_intervention_ids") or r.get("top_cause_ids"):
            logs.review("phenotype_top_lists", "phenotypes", rid, i + 2,
                        "top_* IDs in legacy-only columns; no edges written")
    return pd.DataFrame(rows, columns=HEADERS["phenotypes"])


def build_genes(legacy: dict, ts: str, aliases: AliasRegistry,
                logs: LogBuffer) -> tuple[pd.DataFrame, dict]:
    """Returns (df, symbol_to_gen_id) so downstream edge builders can look up
    the GEN-#### PK by gene_symbol."""
    src = legacy["genes"]
    rows = []
    symbol_to_id = {}
    for i, r in src.iterrows():
        gen_id = pad_id("GEN", i + 1, 4)
        symbol = str(r.get("gene_symbol") or "").strip()
        if symbol:
            symbol_to_id[symbol] = gen_id
            aliases.add("gene", gen_id, symbol)
        ensembl = str(r.get("ensembl_id") or "").strip()
        if ensembl:
            aliases.add("gene", gen_id, ensembl)
        sfari = r.get("sfari_score")
        sfari = nullable(sfari) if sfari not in (None, "", float("nan")) \
            else "NA"
        rows.append({
            "id": gen_id,
            "gene_symbol": symbol,
            "ensembl_id": ensembl,
            "sfari_score": sfari,
            "genetic_evidence_strength":
                nullable(r.get("evidence_strength")),
            "opentargets_score": nullable(r.get("opentargets_score")),
            "gnomad_notes": "",
            "disgenet_score": "",
            "function_summary": nullable(r.get("function_summary")),
            "created_at": ts,
            "last_updated": ts,
            "notes": nullable(r.get("notes")),
            "associated_phenotype_ids_legacy":
                nullable(r.get("associated_phenotype_ids")),
            "linked_intervention_ids_legacy":
                nullable(r.get("linked_intervention_ids")),
        })
        logs.mapped("genes", i + 2, symbol, "genes", gen_id,
                    "copy+assign_pk")
    df = pd.DataFrame(rows, columns=HEADERS["genes"])
    return df, symbol_to_id


def build_hypotheses(legacy: dict, ts: str, aliases: AliasRegistry,
                     logs: LogBuffer) -> pd.DataFrame:
    src = legacy["causes"]
    rows = []
    for i, r in src.iterrows():
        legacy_id = str(r["id"]).strip()
        new_id = reprefix(legacy_id, "HYP")
        raw_cat = str(r.get("category") or "").strip().lower()
        new_cat = HYPOTHESIS_CATEGORY_LEGACY_REMAP.get(
            raw_cat, "other" if raw_cat not in HYPOTHESIS_CATEGORY_ENUM
            else raw_cat)
        if new_cat != raw_cat:
            logs.remap("causes", i + 2, "category", raw_cat, new_cat,
                       "not in canonical enum; coerced to 'other'")
            logs.review("hypothesis_category_remap", "hypotheses", new_id,
                        i + 2,
                        f"legacy category '{raw_cat}' mapped to 'other'")
        rows.append({
            "id": new_id,
            "name": nullable(r.get("name")),
            "category": new_cat,
            "description": nullable(r.get("mechanism_summary")),
            "affected_population": nullable(r.get("affected_population")),
            "status": "active",
            "confidence_score": "",
            "evidence_count": "",
            "evidence_quality_index": "",
            "consistency_index": "",
            "created_at": ts,
            "last_updated": ts,
            "notes": nullable(r.get("notes")),
            "category_legacy": raw_cat,
            "evidence_strength_legacy":
                nullable(r.get("evidence_strength")),
            "epidemiological_strength_legacy":
                nullable(r.get("epidemiological_strength")),
            "mitigation_intervention_ids_legacy":
                nullable(r.get("mitigation_intervention_ids")),
            "source_pmids_legacy": nullable(r.get("source_pmids")),
            "csrs_score_legacy": nullable(r.get("csrs_score")),
            "csrs_last_updated_legacy":
                nullable(r.get("csrs_last_updated")),
        })
        aliases.add("hypothesis", new_id, legacy_id)
        logs.mapped("causes", i + 2, legacy_id, "hypotheses", new_id,
                    "reprefix+copy")
    return pd.DataFrame(rows, columns=HEADERS["hypotheses"])


def build_interventions(legacy: dict, ts: str, aliases: AliasRegistry,
                        logs: LogBuffer) -> pd.DataFrame:
    src = legacy["interventions"]
    rows = []
    for i, r in src.iterrows():
        rid = str(r["id"]).strip()
        rows.append({
            "id": rid,
            "name": nullable(r.get("name")),
            "category": nullable(r.get("category")),
            "directionality": nullable(r.get("directionality")),
            "mechanism_summary": nullable(r.get("mechanism_summary")),
            "dose_range": nullable(r.get("dose_range")),
            "cost_per_month_usd": nullable(r.get("cost_per_month_usd")),
            "otc_or_rx": nullable(r.get("otc_or_rx")),
            "pediatric_safe": nullable(r.get("pediatric_safe")),
            "csrs_score": "",
            "csrs_last_updated": "",
            "status": "active",
            "created_at": ts,
            "last_updated": ts,
            "notes": nullable(r.get("notes")),
            "targets_legacy": nullable(r.get("targets")),
            "source_pmids_legacy": nullable(r.get("source_pmids")),
            "source_anecdote_ids_legacy":
                nullable(r.get("source_anecdote_ids")),
            "csrs_score_legacy": nullable(r.get("csrs_score")),
            "csrs_last_updated_legacy":
                nullable(r.get("csrs_last_updated")),
        })
        aliases.add("intervention", rid, rid)
        logs.mapped("interventions", i + 2, rid, "interventions", rid,
                    "copy")
    return pd.DataFrame(rows, columns=HEADERS["interventions"])


def build_combinations(legacy: dict, ts: str, aliases: AliasRegistry,
                       logs: LogBuffer) -> pd.DataFrame:
    src = legacy["combinations"]
    rows = []
    for i, r in src.iterrows():
        legacy_id = str(r["id"]).strip()
        new_id = reprefix(legacy_id, "COM")
        description_parts = []
        if r.get("evidence_summary"):
            description_parts.append(str(r["evidence_summary"]))
        rows.append({
            "id": new_id,
            "name": nullable(r.get("name")),
            "description": " | ".join(description_parts),
            "rationale": nullable(r.get("rationale")),
            "interaction_warnings":
                nullable(r.get("interaction_warnings")),
            "csrs_score": "",
            "csrs_last_updated": "",
            "status": "active",
            "created_at": ts,
            "last_updated": ts,
            "notes": nullable(r.get("notes")),
            "member_intervention_ids_legacy":
                nullable(r.get("member_intervention_ids")),
            "csrs_score_legacy": nullable(r.get("csrs_score")),
            "csrs_last_updated_legacy":
                nullable(r.get("csrs_last_updated")),
        })
        aliases.add("combination", new_id, legacy_id)
        logs.mapped("combinations", i + 2, legacy_id, "combinations",
                    new_id, "reprefix+copy")
        if not split_packed(r.get("member_intervention_ids")):
            logs.review("combination_zero_members", "combinations", new_id,
                        i + 2, "combination has zero members")
    return pd.DataFrame(rows, columns=HEADERS["combinations"])


def build_combination_members(legacy: dict, ts: str,
                              intervention_ids: set,
                              logs: LogBuffer) -> pd.DataFrame:
    src = legacy["combinations"]
    rows = []
    n = 1
    for i, r in src.iterrows():
        legacy_combo = str(r["id"]).strip()
        new_combo = reprefix(legacy_combo, "COM")
        for token in split_packed(r.get("member_intervention_ids")):
            if token not in intervention_ids:
                logs.orphan("combinations", i + 2,
                            "member_intervention_ids", token,
                            "intervention")
                continue
            rows.append({
                "id": pad_id("CMM", n, 4),
                "combination_id": new_combo,
                "intervention_id": token,
                "role": "",
                "created_at": ts,
            })
            n += 1
    return pd.DataFrame(rows, columns=HEADERS["combination_members"])


def build_sources(legacy: dict, ts: str, aliases: AliasRegistry,
                  logs: LogBuffer) -> tuple[pd.DataFrame, dict, dict]:
    """Returns (df, study_pmid_to_src, anecdote_id_to_src)."""
    rows = []
    study_map: dict[str, str] = {}     # PMID (str) → SRC-######
    anecdote_map: dict[str, str] = {}  # ANE-#### → SRC-######
    n = 1

    # ---- Studies ----
    studies = legacy["studies"]
    for i, r in studies.iterrows():
        sid = pad_id("SRC", n, 6)
        n += 1
        pmid = str(r.get("pmid") or "").strip()
        raw_type = str(r.get("study_type") or "").strip().lower()
        new_design = STUDY_TYPE_LEGACY_REMAP.get(raw_type)
        if new_design is None:
            new_design = "other" if raw_type else ""
        if raw_type and new_design != raw_type:
            logs.remap("studies", i + 2, "study_type", raw_type,
                       new_design,
                       "mapped per spec §4.5 study_design enum")
        src_type = "review" if new_design in ("review", "meta_analysis") \
            else "study"
        year = r.get("year")
        date_pub = ""
        date_precision = ""
        year_int = None
        if pd.notna(year) and str(year).strip() not in ("", "nan"):
            m_year = re.search(r"\b(\d{4})\b", str(year))
            if m_year:
                try:
                    year_int = int(m_year.group(1))
                    date_pub = f"{year_int}-01-01"
                    date_precision = "year"
                except (ValueError, TypeError):
                    year_int = None
        raw_meta = {
            "doi": nullable(r.get("doi")) or None,
            "authors": nullable(r.get("authors")) or None,
            "year": year_int,
            "journal": nullable(r.get("journal")) or None,
            "abstract": nullable(r.get("abstract")) or None,
            "legacy_study_type": raw_type or None,
            "legacy_replicated":
                nullable(r.get("replicated")) or None,
            "date_precision": date_precision or None,
        }
        rows.append({
            "id": sid,
            "type": src_type,
            "platform": "pubmed",
            "external_id": pmid,
            "title": nullable(r.get("title")),
            "url": nullable(r.get("full_text_url")),
            "date_published": date_pub,
            "date_ingested": ts,
            "study_design": new_design,
            "sample_size": nullable(r.get("n_subjects")),
            "model_system": "",
            "raw_metadata": to_json_str(raw_meta),
            "notes": "",
        })
        if pmid:
            study_map[pmid] = sid
            aliases.add("source", sid, f"PMID:{pmid}")
        doi = nullable(r.get("doi"))
        if doi:
            aliases.add("source", sid, f"DOI:{doi}")
        logs.mapped("studies", i + 2, pmid or f"row{i+2}", "sources", sid,
                    "copy+assign_pk")
        if raw_type == "observational":
            logs.review("observational_reclassify", "sources", sid, i + 2,
                        "study_type=observational remapped to other; "
                        "cohort vs case_control refinement pending")

    # ---- Anecdotes ----
    anecdotes = legacy["anecdotes"]
    for i, r in anecdotes.iterrows():
        sid = pad_id("SRC", n, 6)
        n += 1
        legacy_ane = str(r.get("id") or "").strip()
        platform = str(r.get("source") or "").strip().lower()
        reporter = str(r.get("reporter_population") or "").strip().lower()
        # Decision rule per MIGRATION_IMPLEMENTATION.md §3.6.
        if platform == "youtube" and reporter in ("clinician", "researcher"):
            src_type = "social"
        else:
            src_type = "anecdote"
        raw_meta = {
            "legacy_anecdote_id": legacy_ane or None,
            "reporter_population": reporter or None,
            "engagement": None if pd.isna(r.get("engagement"))
                else int(r.get("engagement"))
                if pd.notna(r.get("engagement")) else None,
            "legacy_mechanism_match": bool(r.get("mechanism_match"))
                if pd.notna(r.get("mechanism_match")) else None,
            "legacy_contradicting_literature":
                bool(r.get("contradicting_literature"))
                if pd.notna(r.get("contradicting_literature")) else None,
            "raw_text_excerpt_full": nullable(r.get("raw_text_excerpt"))
                or None,
            "legacy_anecdote_type_rule":
                "youtube+clinician_or_researcher→social else anecdote",
        }
        date_pub = nullable(r.get("date_iso"))
        rows.append({
            "id": sid,
            "type": src_type,
            "platform": platform,
            "external_id": "",   # parsed external ID left for ingestion
            "title": "",
            "url": nullable(r.get("url")),
            "date_published": date_pub,
            "date_ingested": ts,
            "study_design": "",
            "sample_size": "",
            "model_system": "human",
            "raw_metadata": to_json_str(raw_meta),
            "notes": nullable(r.get("notes")),
        })
        if legacy_ane:
            anecdote_map[legacy_ane] = sid
            aliases.add("source", sid, legacy_ane)
        logs.mapped("anecdotes", i + 2, legacy_ane, "sources", sid,
                    "copy+assign_pk+reprefix")
        if reporter == "unknown":
            logs.review("anecdote_reporter_unknown", "sources", sid, i + 2,
                        "reporter_population=unknown; low strength tier")
        if not date_pub:
            logs.review("anecdote_missing_date", "sources", sid, i + 2,
                        "date_iso missing in legacy")

    df = pd.DataFrame(rows, columns=HEADERS["sources"])
    return df, study_map, anecdote_map


def _infer_effect_direction_study(outcome, effect_size, p_value,
                                  replicated) -> str:
    """Rule-based inference matching MIGRATION_IMPLEMENTATION.md §3.7."""
    out_l = str(outcome or "").lower()
    eff_l = str(effect_size or "").lower()
    p_l = str(p_value or "").lower()
    rep_l = str(replicated or "").lower()
    is_significant = any(tok in p_l for tok in
                         ("<0.00", "<0.01", "<0.05", "p<0.05"))
    if "p=0" in p_l and not any(x in p_l for x in
                                ("p=0.5", "p=0.6", "p=0.7", "p=0.8",
                                 "p=0.9", "p=0.06", "p=0.07",
                                 "p=0.08", "p=0.09", "p=0.10")):
        is_significant = True
    neg_phrases = ["no effect", "null", "non-significant",
                   "no significant", "failed"]
    deterioration = any(tok in out_l for tok in
                        ("worse", "deterior", "adverse"))
    explicitly_negative = any(tok in eff_l for tok in ("-", "reduc")) \
        and deterioration
    if explicitly_negative:
        return "negative"
    if is_significant and not any(p in out_l for p in neg_phrases):
        return "positive"
    if any(p in out_l for p in neg_phrases):
        return "neutral"
    if rep_l == "partial":
        return "mixed"
    return "unclear"


def build_evidence_fragments(legacy: dict, ts: str,
                             study_map: dict, anecdote_map: dict,
                             logs: LogBuffer
                             ) -> tuple[pd.DataFrame, dict, dict]:
    """Returns (df, study_fragment_map, anecdote_fragment_map) where the
    maps go from legacy row PK to the EVD-###### id."""
    rows = []
    n = 1
    study_frag_map: dict[str, str] = {}     # PMID → EVD-######
    anecdote_frag_map: dict[str, str] = {}  # ANE-#### → EVD-######

    # ---- Studies ----
    studies = legacy["studies"]
    for i, r in studies.iterrows():
        fid = pad_id("EVD", n, 6)
        n += 1
        pmid = str(r.get("pmid") or "").strip()
        sid = study_map.get(pmid, "")
        raw_type = str(r.get("study_type") or "").strip().lower()
        if raw_type == "mechanistic":
            frag_type = "mechanism"
        else:
            frag_type = "result"
        payload = {
            "outcome": nullable(r.get("outcome")) or None,
            "effect_size": nullable(r.get("effect_size")) or None,
            "p_value": nullable(r.get("p_value")) or None,
            "replicated": nullable(r.get("replicated")) or None,
            "legacy_intervention_id":
                nullable(r.get("intervention_id")) or None,
            "legacy_cause_id": nullable(r.get("cause_id")) or None,
            "is_secondary_literature":
                raw_type in ("review", "meta_analysis"),
        }
        abstract = str(r.get("abstract") or "")
        text_excerpt = abstract[:500] if abstract else ""
        eff_dir = _infer_effect_direction_study(
            r.get("outcome"), r.get("effect_size"),
            r.get("p_value"), r.get("replicated"))
        rows.append({
            "id": fid,
            "source_id": sid,
            "fragment_type": frag_type,
            "text_excerpt": text_excerpt,
            "structured_payload": to_json_str(payload),
            "effect_direction": eff_dir,
            "strength_score": "",
            "extraction_method": "rule_based",
            "extraction_confidence": "",
            "date_extracted": ts,
            "notes": "",
        })
        if pmid:
            study_frag_map[pmid] = fid
        if eff_dir == "unclear":
            logs.review("fragment_unclear_effect",
                        "evidence_fragments", fid, i + 2,
                        "effect_direction unresolved by rules")

    # ---- Anecdotes ----
    anecdotes = legacy["anecdotes"]
    for i, r in anecdotes.iterrows():
        fid = pad_id("EVD", n, 6)
        n += 1
        legacy_ane = str(r.get("id") or "").strip()
        sid = anecdote_map.get(legacy_ane, "")
        raw_outcome = str(r.get("reported_outcome") or "").strip().lower()
        eff_dir = ANECDOTE_OUTCOME_REMAP.get(raw_outcome, "unclear")
        if raw_outcome and eff_dir != raw_outcome:
            logs.remap("anecdotes", i + 2, "reported_outcome",
                       raw_outcome, eff_dir,
                       "null→neutral per spec §4.6")
        payload = {
            "reporter_population":
                nullable(r.get("reporter_population")) or None,
            "engagement": int(r["engagement"])
                if pd.notna(r.get("engagement")) else None,
            "legacy_intervention_id":
                nullable(r.get("intervention_id")) or None,
            "legacy_cause_id": nullable(r.get("cause_id")) or None,
            "legacy_mechanism_match":
                bool(r["mechanism_match"])
                if pd.notna(r.get("mechanism_match")) else None,
            "legacy_contradicting_literature":
                bool(r["contradicting_literature"])
                if pd.notna(r.get("contradicting_literature"))
                else None,
        }
        rows.append({
            "id": fid,
            "source_id": sid,
            "fragment_type": "anecdote",
            "text_excerpt": nullable(r.get("raw_text_excerpt")),
            "structured_payload": to_json_str(payload),
            "effect_direction": eff_dir,
            "strength_score": "",
            "extraction_method": "rule_based",
            "extraction_confidence": "",
            "date_extracted": ts,
            "notes": "",
        })
        if legacy_ane:
            anecdote_frag_map[legacy_ane] = fid

    df = pd.DataFrame(rows, columns=HEADERS["evidence_fragments"])
    return df, study_frag_map, anecdote_frag_map


def build_evidence_links(legacy: dict, ts: str,
                         study_frag_map: dict, anecdote_frag_map: dict,
                         intervention_ids: set,
                         hypothesis_reprefix: dict,
                         logs: LogBuffer) -> pd.DataFrame:
    rows = []
    n = 1

    # ---- From studies ----
    studies = legacy["studies"]
    for i, r in studies.iterrows():
        pmid = str(r.get("pmid") or "").strip()
        fid = study_frag_map.get(pmid)
        if not fid:
            continue
        int_id = nullable(r.get("intervention_id"))
        cau_id = nullable(r.get("cause_id"))
        # Pull parent fragment's effect_direction (recomputed here to keep
        # the function self-contained — same rule as above).
        eff_dir = _infer_effect_direction_study(
            r.get("outcome"), r.get("effect_size"),
            r.get("p_value"), r.get("replicated"))
        if int_id:
            if int_id not in intervention_ids:
                logs.orphan("studies", i + 2, "intervention_id",
                            int_id, "intervention")
            else:
                rows.append({
                    "id": pad_id("EVL", n, 6),
                    "evidence_fragment_id": fid,
                    "claim_id": "",
                    "target_type": "intervention",
                    "target_id": int_id,
                    "effect_direction": eff_dir,
                    "weight": "",
                    "context_scope": "",
                    "created_at": ts,
                    "notes": "",
                })
                n += 1
        if cau_id:
            new_hyp = hypothesis_reprefix.get(cau_id)
            if not new_hyp:
                logs.orphan("studies", i + 2, "cause_id", cau_id,
                            "hypothesis")
            else:
                rows.append({
                    "id": pad_id("EVL", n, 6),
                    "evidence_fragment_id": fid,
                    "claim_id": "",
                    "target_type": "hypothesis",
                    "target_id": new_hyp,
                    "effect_direction": eff_dir,
                    "weight": "",
                    "context_scope": "",
                    "created_at": ts,
                    "notes": "",
                })
                n += 1

    # ---- From anecdotes ----
    anecdotes = legacy["anecdotes"]
    for i, r in anecdotes.iterrows():
        legacy_ane = str(r.get("id") or "").strip()
        fid = anecdote_frag_map.get(legacy_ane)
        if not fid:
            continue
        raw_outcome = str(r.get("reported_outcome") or "").strip().lower()
        eff_dir = ANECDOTE_OUTCOME_REMAP.get(raw_outcome, "unclear")
        contradicts = bool(r.get("contradicting_literature")) \
            if pd.notna(r.get("contradicting_literature")) else False
        reporter = nullable(r.get("reporter_population"))
        ctx = f"reporter={reporter}" if reporter else ""
        int_id = nullable(r.get("intervention_id"))
        cau_id = nullable(r.get("cause_id"))
        if int_id:
            if int_id not in intervention_ids:
                logs.orphan("anecdotes", i + 2, "intervention_id",
                            int_id, "intervention")
            else:
                rows.append({
                    "id": pad_id("EVL", n, 6),
                    "evidence_fragment_id": fid,
                    "claim_id": "",
                    "target_type": "intervention",
                    "target_id": int_id,
                    "effect_direction": eff_dir,
                    "weight": "",
                    "context_scope": ctx,
                    "created_at": ts,
                    "notes": "",
                })
                n += 1
        if cau_id:
            new_hyp = hypothesis_reprefix.get(cau_id)
            if not new_hyp:
                logs.orphan("anecdotes", i + 2, "cause_id", cau_id,
                            "hypothesis")
            else:
                # Legacy contradicting_literature → contradicting direction
                # when the anecdote is linked to a hypothesis.
                h_dir = "negative" if contradicts else eff_dir
                if contradicts:
                    logs.review("contradicting_literature_anecdote",
                                "evidence_links", "", i + 2,
                                "legacy bool contradicting_literature=True "
                                "flipped effect_direction to negative vs. "
                                "hypothesis")
                rows.append({
                    "id": pad_id("EVL", n, 6),
                    "evidence_fragment_id": fid,
                    "claim_id": "",
                    "target_type": "hypothesis",
                    "target_id": new_hyp,
                    "effect_direction": h_dir,
                    "weight": "",
                    "context_scope": ctx,
                    "created_at": ts,
                    "notes": "",
                })
                n += 1

    return pd.DataFrame(rows, columns=HEADERS["evidence_links"])


# ----------------------------------------------------------------------------
# Empty-shell builder (for tables that stay empty at migration time, per
# MIGRATION_IMPLEMENTATION.md §3.18–§3.21).
# ----------------------------------------------------------------------------

def empty_df(table_name: str) -> pd.DataFrame:
    return pd.DataFrame(columns=HEADERS[table_name])


# ----------------------------------------------------------------------------
# Pattern: edge-table builders for the edges that DO get rows at migration.
# These are shown as working scaffolds — extend the rule-based extraction as
# the mechanism vocabulary grows. See MIGRATION_IMPLEMENTATION.md §3.11–§3.17.
# ----------------------------------------------------------------------------

def _extract_mechanism_phrases(text: str) -> list[str]:
    if not text:
        return []
    low = str(text).lower()
    found = []
    for phrase, canonical in MECHANISM_VOCAB.items():
        if phrase in low and canonical not in found:
            found.append(canonical)
    return found


def build_mechanisms(legacy: dict, ts: str, aliases: AliasRegistry,
                     logs: LogBuffer) -> tuple[pd.DataFrame, dict]:
    """Builds the mechanisms table (seeds + extracted canonical names).
    Returns (df, name_to_id)."""
    seen: dict[str, str] = {}
    rows = []
    # Seed rows first (MEC-0001 … MEC-0009 + extras).
    for i, (name, cat) in enumerate(SEED_MECHANISMS + EXTRA_SEED_MECHANISMS):
        mid = pad_id("MEC", i + 1, 4)
        seen[name] = mid
        rows.append({
            "id": mid, "name": name, "category": cat,
            "description": "", "status": "active",
            "evidence_strength": "", "kegg_ids": "", "reactome_ids": "",
            "opentargets_ids": "", "created_at": ts, "last_updated": ts,
            "notes": "seeded from spec §4.2 examples",
        })
        aliases.add("mechanism", mid, name)
    # Extract from causes + interventions mechanism_summary.
    for sheet_name in ("causes", "interventions"):
        df = legacy[sheet_name]
        for i, r in df.iterrows():
            text = r.get("mechanism_summary")
            for canonical in _extract_mechanism_phrases(text):
                logs.extracted(sheet_name, i + 2, "mechanism_summary",
                               canonical, canonical, "rule_based")
                if canonical not in seen:
                    mid = pad_id("MEC", len(seen) + 1, 4)
                    seen[canonical] = mid
                    rows.append({
                        "id": mid, "name": canonical, "category": "other",
                        "description": "", "status": "active",
                        "evidence_strength": "", "kegg_ids": "",
                        "reactome_ids": "", "opentargets_ids": "",
                        "created_at": ts, "last_updated": ts,
                        "notes": f"extracted from {sheet_name}",
                    })
                    aliases.add("mechanism", mid, canonical)
    df = pd.DataFrame(rows, columns=HEADERS["mechanisms"])
    return df, seen


def build_hypothesis_mechanism_edges(legacy: dict, ts: str,
                                     mechanism_ids: dict,
                                     logs: LogBuffer) -> pd.DataFrame:
    rows = []
    n = 1
    for i, r in legacy["causes"].iterrows():
        hyp_id = reprefix(str(r["id"]), "HYP")
        for canonical in _extract_mechanism_phrases(r.get("mechanism_summary")):
            mid = mechanism_ids.get(canonical)
            if not mid:
                continue
            rows.append({
                "id": pad_id("HME", n, 5),
                "hypothesis_id": hyp_id,
                "mechanism_id": mid,
                "relation_type": "acts_through",
                "polarity": "unknown",
                "evidence_for_count": "", "evidence_against_count": "",
                "evidence_strength_aggregate": "",
                "context_scope": "", "status": "active",
                "created_at": ts, "last_updated": ts,
            })
            n += 1
    return pd.DataFrame(rows, columns=HEADERS["hypothesis_mechanism_edges"])


def build_intervention_mechanism_edges(legacy: dict, ts: str,
                                       mechanism_ids: dict,
                                       logs: LogBuffer) -> pd.DataFrame:
    rows = []
    n = 1
    for i, r in legacy["interventions"].iterrows():
        int_id = str(r["id"]).strip()
        text = " ".join([
            str(r.get("mechanism_summary") or ""),
            str(r.get("targets") or ""),
        ])
        for canonical in _extract_mechanism_phrases(text):
            mid = mechanism_ids.get(canonical)
            if not mid:
                continue
            rows.append({
                "id": pad_id("IME", n, 5),
                "intervention_id": int_id,
                "mechanism_id": mid,
                "relation_type": "modulates",
                "polarity": "unknown",
                "evidence_for_count": "", "evidence_against_count": "",
                "evidence_strength_aggregate": "",
                "context_scope": "", "status": "active",
                "created_at": ts, "last_updated": ts,
            })
            n += 1
    return pd.DataFrame(rows, columns=HEADERS["intervention_mechanism_edges"])


def build_intervention_hypothesis_edges(legacy: dict, ts: str,
                                        intervention_ids: set,
                                        hypothesis_reprefix: dict,
                                        logs: LogBuffer) -> pd.DataFrame:
    rows = []
    n = 1
    for i, r in legacy["causes"].iterrows():
        hyp_id = reprefix(str(r["id"]), "HYP")
        for token in split_packed(r.get("mitigation_intervention_ids")):
            if token not in intervention_ids:
                logs.orphan("causes", i + 2,
                            "mitigation_intervention_ids", token,
                            "intervention")
                continue
            rows.append({
                "id": pad_id("IHE", n, 5),
                "intervention_id": token,
                "hypothesis_id": hyp_id,
                "relation_type": "cause_mitigation",
                "polarity": "supporting",
                "evidence_for_count": "", "evidence_against_count": "",
                "evidence_strength_aggregate": "",
                "context_scope": "", "status": "active",
                "created_at": ts, "last_updated": ts,
            })
            n += 1
    return pd.DataFrame(rows, columns=HEADERS["intervention_hypothesis_edges"])


def build_gene_phenotype_edges(legacy: dict, ts: str,
                               symbol_to_gen: dict, phenotype_ids: set,
                               logs: LogBuffer) -> pd.DataFrame:
    rows = []
    n = 1
    for i, r in legacy["genes"].iterrows():
        symbol = str(r.get("gene_symbol") or "").strip()
        gen = symbol_to_gen.get(symbol)
        for token in split_packed(r.get("associated_phenotype_ids")):
            if token not in phenotype_ids:
                logs.orphan("genes", i + 2, "associated_phenotype_ids",
                            token, "phenotype")
                continue
            if not gen:
                continue
            sfari = str(r.get("sfari_score") or "").strip()
            rel = "syndromic_cause_of" if sfari == "S" else "associated_with"
            if rel == "syndromic_cause_of":
                logs.review("gene_phenotype_syndromic", "gene_phenotype_edges",
                            "", i + 2,
                            f"SFARI=S gene {symbol}→{token}; confirm "
                            "syndromic_cause_of")
            rows.append({
                "id": pad_id("GPE", n, 5),
                "gene_id": gen,
                "phenotype_id": token,
                "relation_type": rel,
                "polarity": "supporting",
                "evidence_for_count": "", "evidence_against_count": "",
                "evidence_strength_aggregate": "",
                "context_scope": "", "status": "active",
                "created_at": ts, "last_updated": ts,
            })
            n += 1
    return pd.DataFrame(rows, columns=HEADERS["gene_phenotype_edges"])


def build_intervention_gene_edges(legacy: dict, ts: str,
                                  symbol_to_gen: dict,
                                  intervention_ids: set,
                                  logs: LogBuffer) -> pd.DataFrame:
    """Populates from legacy genes.linked_intervention_ids. (The
    interventions.targets → gene classification branch is deferred to
    manual review; not auto-populated.)"""
    rows = []
    n = 1
    seen = set()
    for i, r in legacy["genes"].iterrows():
        symbol = str(r.get("gene_symbol") or "").strip()
        gen = symbol_to_gen.get(symbol)
        for token in split_packed(r.get("linked_intervention_ids")):
            if token not in intervention_ids:
                logs.orphan("genes", i + 2, "linked_intervention_ids",
                            token, "intervention")
                continue
            key = (token, gen)
            if key in seen or not gen:
                continue
            seen.add(key)
            rows.append({
                "id": pad_id("IGE", n, 5),
                "intervention_id": token,
                "gene_id": gen,
                "relation_type": "targets",
                "polarity": "supporting",
                "evidence_for_count": "", "evidence_against_count": "",
                "evidence_strength_aggregate": "",
                "context_scope": "", "status": "active",
                "created_at": ts, "last_updated": ts,
            })
            n += 1
    return pd.DataFrame(rows, columns=HEADERS["intervention_gene_edges"])


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    LOGS_DIR.mkdir(exist_ok=True)

    ts = now_iso()
    aliases = AliasRegistry(ts)
    logs = LogBuffer()

    print(f"[migration] run timestamp: {ts}")
    print(f"[migration] loading {LEGACY_FILE}")
    legacy = load_legacy(LEGACY_FILE)

    # -- Priority tables --
    phenotypes = build_phenotypes(legacy, ts, aliases, logs)
    genes_df, symbol_to_gen = build_genes(legacy, ts, aliases, logs)
    hypotheses = build_hypotheses(legacy, ts, aliases, logs)
    interventions = build_interventions(legacy, ts, aliases, logs)
    combinations = build_combinations(legacy, ts, aliases, logs)

    intervention_ids = set(interventions["id"])
    phenotype_ids = set(phenotypes["id"])
    hypothesis_reprefix = {
        f"CAU-{row['id'][4:]}": row["id"]
        for _, row in hypotheses.iterrows()
    }

    combination_members = build_combination_members(
        legacy, ts, intervention_ids, logs)
    sources, study_map, anecdote_map = build_sources(
        legacy, ts, aliases, logs)
    evidence_fragments, study_frag_map, anecdote_frag_map = \
        build_evidence_fragments(
            legacy, ts, study_map, anecdote_map, logs)
    evidence_links = build_evidence_links(
        legacy, ts, study_frag_map, anecdote_frag_map,
        intervention_ids, hypothesis_reprefix, logs)

    # -- Mechanism extraction + edges --
    mechanisms, mech_name_to_id = build_mechanisms(
        legacy, ts, aliases, logs)
    hm_edges = build_hypothesis_mechanism_edges(
        legacy, ts, mech_name_to_id, logs)
    im_edges = build_intervention_mechanism_edges(
        legacy, ts, mech_name_to_id, logs)
    ih_edges = build_intervention_hypothesis_edges(
        legacy, ts, intervention_ids, hypothesis_reprefix, logs)
    gp_edges = build_gene_phenotype_edges(
        legacy, ts, symbol_to_gen, phenotype_ids, logs)
    ig_edges = build_intervention_gene_edges(
        legacy, ts, symbol_to_gen, intervention_ids, logs)

    # -- Empty-at-migration tables --
    mech_phen_edges = empty_df("mechanism_phenotype_edges")
    gene_mech_edges = empty_df("gene_mechanism_edges")
    gene_hyp_edges = empty_df("gene_hypothesis_edges")
    int_phen_edges = empty_df("intervention_phenotype_edges")
    score_history = empty_df("score_history")

    # -- node_aliases (flush last so it contains every entry) --
    node_aliases = aliases.to_df()

    # -- Write every CSV --
    outputs = {
        "hypotheses.csv": hypotheses,
        "mechanisms.csv": mechanisms,
        "phenotypes.csv": phenotypes,
        "genes.csv": genes_df,
        "sources.csv": sources,
        "evidence_fragments.csv": evidence_fragments,
        "evidence_links.csv": evidence_links,
        "hypothesis_mechanism_edges.csv": hm_edges,
        "mechanism_phenotype_edges.csv": mech_phen_edges,
        "gene_mechanism_edges.csv": gene_mech_edges,
        "gene_hypothesis_edges.csv": gene_hyp_edges,
        "gene_phenotype_edges.csv": gp_edges,
        "interventions.csv": interventions,
        "intervention_mechanism_edges.csv": im_edges,
        "intervention_hypothesis_edges.csv": ih_edges,
        "intervention_phenotype_edges.csv": int_phen_edges,
        "intervention_gene_edges.csv": ig_edges,
        "combinations.csv": combinations,
        "combination_members.csv": combination_members,
        "node_aliases.csv": node_aliases,
        "score_history.csv": score_history,
    }
    for filename, df in outputs.items():
        target = OUTPUT_DIR / filename
        df.to_csv(target, index=False, encoding="utf-8")
        print(f"[migration] wrote {target}  rows={len(df)}")

    # -- Logs --
    logs.flush(LOGS_DIR)
    print(f"[migration] wrote logs to {LOGS_DIR}/")
    print("[migration] done.")


if __name__ == "__main__":
    main()
