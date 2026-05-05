#!/usr/bin/env python3
"""
audit_evidence_balance.py

Asserts the evidence-balance schema is populated across prior tables.
Defangs the curation-bias / omission-attack vector identified in the
pre-mortem: every row tagged `contested` MUST have both `primary_pmids`
and `countervailing_evidence_pmids` populated. Non-contested rows MAY
have countervailing empty but get a warning.

Currently audits:
- v2.0_scored/iatrogenic_exposure_priors.csv

Exit 0 if no failures (warnings allowed). Exit 1 if any failure.
"""
from __future__ import annotations
import csv
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ATLAS_DIR = REPO / "v2.0_scored"

# ANSI colors
R = "\033[31m"
Y = "\033[33m"
G = "\033[32m"
N = "\033[0m"

TABLES_WITH_EVIDENCE_BALANCE = {
    "iatrogenic_exposure_priors.csv": {
        "supporting_field": "primary_pmids",
        "opposing_field": "countervailing_evidence_pmids",
        "status_field": "status",
        "id_field": "id",
        "row_label_field": "specific_agent",
        "consensus_field": "mainstream_consensus_position",  # Move 6b
    },
    "rare_syndrome_screening_gate.csv": {
        "supporting_field": "primary_pmid",
        "opposing_field": "countervailing_evidence_pmids",
        "status_field": "status",
        "id_field": "id",
        "row_label_field": "syndrome_name",
        # No consensus field needed — RSG entries are mostly mainstream-accepted
        # syndromes (22q11.2 deletion, FXS, RTT) where there is no contested
        # framing to balance.
    },
    "baseline_phenotype_prevalence.csv": {
        "supporting_field": "primary_pmid",
        "opposing_field": "countervailing_evidence_pmids",
        "status_field": "status",
        "id_field": "id",
        "row_label_field": "phenotype_id",
    },
    "genetic_id_aliases.csv": {
        "supporting_field": "primary_pmid",
        "opposing_field": "countervailing_evidence_pmids",
        "status_field": "status",
        "id_field": "id",
        "row_label_field": "common_name",
    },
    "pgx_drug_gene_table.csv": {
        "supporting_field": "primary_pmid",
        "opposing_field": "countervailing_evidence_pmids",
        "status_field": "status",
        "id_field": "id",
        "row_label_field": "drug_or_intervention_id",
    },
    "physiological_state_normalization_table.csv": {
        "supporting_field": "primary_pmid",
        "opposing_field": "countervailing_evidence_pmids",
        "status_field": None,  # PSN table has no status field; warnings only
        "id_field": "biomarker_id",
        "row_label_field": "row_type",
    },
    "hypotheses.csv": {
        "supporting_field": None,  # hypotheses don't have direct PMID lists; via evidence_links
        "opposing_field": None,
        "status_field": "status",
        "id_field": "id",
        "row_label_field": "name",
        "consensus_field": "mainstream_consensus_position",  # Phase C
    },
    "interventions.csv": {
        "supporting_field": None,  # interventions cite via source_pmids_legacy
        "opposing_field": None,
        "status_field": "status",
        "id_field": "id",
        "row_label_field": "name",
        "consensus_field": "mainstream_consensus_position",  # Phase C
    },
}


def audit_table(path: Path, cfg: dict) -> tuple[list[str], list[str]]:
    failures = []
    warnings = []
    if not path.exists():
        return failures, [f"{path.name} not found (skipping)"]
    with open(path, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    sup = cfg.get("supporting_field")
    opp = cfg.get("opposing_field")
    sf = cfg.get("status_field")
    idf = cfg["id_field"]
    lblf = cfg["row_label_field"]
    consensus_f = cfg.get("consensus_field")

    for r in rows:
        row_id = r.get(idf, "?")
        label = r.get(lblf, "") or ""
        status = (r.get(sf) or "").strip().lower() if sf else ""
        sup_val = (r.get(sup) or "").strip() if sup else None
        opp_val = (r.get(opp) or "").strip() if opp else None
        consensus_val = (r.get(consensus_f) or "").strip() if consensus_f else None

        if status == "contested":
            if sup is not None and not sup_val:
                failures.append(
                    f"  {row_id} ({label[:30]}): contested but {sup} EMPTY — supporting evidence is required"
                )
            if opp is not None and not opp_val:
                failures.append(
                    f"  {row_id} ({label[:30]}): contested but {opp} EMPTY — opposing evidence is required to defang omission attack"
                )
            if consensus_f and not consensus_val:
                failures.append(
                    f"  {row_id} ({label[:30]}): contested but {consensus_f} EMPTY — mainstream consensus position required (Move 6b)"
                )
        else:
            if sup is not None and not sup_val:
                warnings.append(
                    f"  {row_id} ({label[:30]}): {sf}={status}, {sup} empty"
                )
            if opp is not None and not opp_val:
                warnings.append(
                    f"  {row_id} ({label[:30]}): {sf}={status}, {opp} empty (consider populating for completeness)"
                )

    return failures, warnings


def main():
    print("Evidence-balance audit\n")
    total_failures = 0
    total_warnings = 0
    for fname, cfg in TABLES_WITH_EVIDENCE_BALANCE.items():
        path = ATLAS_DIR / fname
        print(f"--- {fname} ---")
        failures, warnings = audit_table(path, cfg)
        if not failures and not warnings:
            print(f"  {G}OK{N} all rows have balanced evidence")
        if failures:
            print(f"  {R}FAILURES ({len(failures)}):{N}")
            for f in failures:
                print(f"  {R}{f}{N}")
        if warnings:
            print(f"  {Y}WARNINGS ({len(warnings)}):{N}")
            for w in warnings[:20]:
                print(f"  {Y}{w}{N}")
            if len(warnings) > 20:
                print(f"  {Y}  ... +{len(warnings)-20} more{N}")
        total_failures += len(failures)
        total_warnings += len(warnings)
        print()

    print(f"\nSummary: {total_failures} failures, {total_warnings} warnings")
    sys.exit(0 if total_failures == 0 else 1)


if __name__ == "__main__":
    main()
