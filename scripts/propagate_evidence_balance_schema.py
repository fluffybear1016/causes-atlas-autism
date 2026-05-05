#!/usr/bin/env python3
"""
propagate_evidence_balance_schema.py

Phase B of post-mortem fix completion. Adds the evidence-balance schema to
all 5 prior tables (rare_syndrome_screening_gate, baseline_phenotype_prevalence,
genetic_id_aliases, pgx_drug_gene_table, physiological_state_normalization_table).

For each table, adds:
  - countervailing_evidence_pmids (semicolon-joined PMID list, default empty)
  - evidence_balance (auto-computed: supporting_count − opposing_count)

The actual countervailing PMIDs are NOT fabricated — they remain empty for
backfill via the verify-before-write protocol in subsequent sessions.

Idempotent: safe to re-run. Only adds columns if missing; only re-computes
evidence_balance.
"""
from __future__ import annotations
import csv
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ATLAS_DIR = REPO / "v2.0_scored"

# Tables that need evidence-balance schema. For each, specify:
# - file: csv filename
# - supporting_field: existing field carrying primary PMIDs (singular or list)
# - insert_after: column to insert new fields after
TABLES = [
    {
        "file": "iatrogenic_exposure_priors.csv",
        "supporting_field": "primary_pmids",
        "insert_after": "countervailing_evidence_pmids",
    },
    {
        "file": "rare_syndrome_screening_gate.csv",
        "supporting_field": "primary_pmid",
        "insert_after": "primary_pmid",
    },
    {
        "file": "baseline_phenotype_prevalence.csv",
        "supporting_field": "primary_pmid",
        "insert_after": "primary_pmid",
    },
    {
        "file": "genetic_id_aliases.csv",
        "supporting_field": "primary_pmid",
        "insert_after": "primary_pmid",
    },
    {
        "file": "pgx_drug_gene_table.csv",
        "supporting_field": "primary_pmid",
        "insert_after": "primary_pmid",
    },
    {
        "file": "physiological_state_normalization_table.csv",
        "supporting_field": "primary_pmid",
        "insert_after": "primary_pmid",
    },
]


def count_pmids(s: str) -> int:
    if not s or not s.strip():
        return 0
    return sum(1 for p in s.split(";") if p.strip().isdigit())


def main():
    total_changes = 0
    for cfg in TABLES:
        path = ATLAS_DIR / cfg["file"]
        if not path.exists():
            print(f"SKIP {cfg['file']} — not found")
            continue
        with open(path, encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            fieldnames = list(reader.fieldnames)
            rows = list(reader)

        sup = cfg["supporting_field"]
        ins_after = cfg["insert_after"]

        added_columns = []
        # Add countervailing_evidence_pmids
        if "countervailing_evidence_pmids" not in fieldnames:
            try:
                idx = fieldnames.index(ins_after) + 1
            except ValueError:
                idx = len(fieldnames)
            fieldnames.insert(idx, "countervailing_evidence_pmids")
            for r in rows:
                r["countervailing_evidence_pmids"] = ""
            added_columns.append("countervailing_evidence_pmids")

        # Add evidence_balance
        if "evidence_balance" not in fieldnames:
            try:
                idx = fieldnames.index("countervailing_evidence_pmids") + 1
            except ValueError:
                idx = len(fieldnames)
            fieldnames.insert(idx, "evidence_balance")
            added_columns.append("evidence_balance")

        # Recompute evidence_balance for all rows
        for r in rows:
            sup_count = count_pmids(r.get(sup, ""))
            opp_count = count_pmids(r.get("countervailing_evidence_pmids", ""))
            # Simple integer balance; UI can normalize for display
            r["evidence_balance"] = str(sup_count - opp_count)

        with open(path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        if added_columns:
            print(f"  {cfg['file']}: added columns {added_columns}; "
                  f"recomputed evidence_balance on {len(rows)} rows")
        else:
            print(f"  {cfg['file']}: schema OK; recomputed evidence_balance on {len(rows)} rows")
        total_changes += 1

    print(f"\nProcessed {total_changes} tables.")


if __name__ == "__main__":
    main()
