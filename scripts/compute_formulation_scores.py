#!/usr/bin/env python3
"""compute_formulation_scores.py

Supplementary scoring layer for intervention_formulations.csv.

CRITICAL: this script does NOT modify the existing intervention-level
scoring engine (`run_scoring_v20.py`). It is purely additive.

The existing intervention-level CSRS scores in `v2.0_scored/interventions.csv`
remain authoritative — including the calibration anchor INT-0001 = 83.35.
This module computes a SUPPLEMENTARY per-formulation score that the UI/API
can surface to give users formulation-specific recommendations.

Methodological premise (per epistemic principle: "negative orthogonal-
formulation studies should not ruin a formulation built on its own
mechanism + anecdotal evidence"):

    formulation_score(F) =
        own_evidence_strength(F)                                  # what F has on its own
      + INHERITANCE_FACTOR * parent_intervention_csrs(F.parent)    # fractional inheritance
      - 0  (orthogonal-formulation negative evidence does NOT propagate down)

Where:
    own_evidence_strength(F) is mapped from F.formulation_evidence_status:
        established_RCT             -> 70
        established_mechanistic     -> 55
        anecdotal_plus_mechanistic  -> 45
        mechanistic_only            -> 35
        anecdotal_only              -> 30
        untested                    -> 15
        contested                   -> 20  (formulation-specific contested)

    parent_intervention_csrs is read from interventions.csv

    INHERITANCE_FACTOR = 0.30 (one-third of molecule-level evidence
        propagates down to formulation; orthogonal-formulation negative
        evidence does NOT propagate)

Formulation-specific contested status (`contested_at_formulation_level`) is
respected — these formulations get the contested score and are clearly
flagged. But `contested_at_molecule_level_only` formulations DO NOT inherit
the molecule-level contested flag — that's the whole point of this layer.

Output:
    v2.0_scored/intervention_formulations_scored.csv
    (original CSV + 'formulation_score' column + 'score_components' breakdown)

Determinism: stable sort by formulation_id; no random ops; no LLM calls.

Usage:
    cd /Users/Greg/Autism
    python3 scripts/compute_formulation_scores.py
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCORED_DIR = ROOT / "v2.0_scored"
FORMULATIONS_PATH = SCORED_DIR / "intervention_formulations.csv"
INTERVENTIONS_PATH = SCORED_DIR / "interventions.csv"
OUTPUT_PATH = SCORED_DIR / "intervention_formulations_scored.csv"

INHERITANCE_FACTOR = 0.30  # fraction of molecule-level CSRS that inherits

EVIDENCE_STATUS_BASE_SCORE = {
    "established_RCT": 70,
    "established_mechanistic": 55,
    "anecdotal_plus_mechanistic": 45,
    "mechanistic_only": 35,
    "anecdotal_only": 30,
    "untested": 15,
    "contested": 20,
}


def load_intervention_csrs() -> dict[str, float]:
    """Read intervention-level CSRS scores from existing scored output."""
    csrs_map = {}
    with INTERVENTIONS_PATH.open() as f:
        reader = csv.DictReader(f)
        # Locate the CSRS column — atlas may use 'csrs' or 'csrs_score' or similar
        # Standard canonical column name per spec is 'csrs'
        for row in reader:
            int_id = row.get("intervention_id") or row.get("id")
            csrs_value = row.get("csrs") or row.get("csrs_score") or row.get("score")
            if int_id and csrs_value:
                try:
                    csrs_map[int_id] = float(csrs_value)
                except (ValueError, TypeError):
                    pass
    return csrs_map


def compute_formulation_score(
    formulation_status: str,
    parent_csrs: float,
    contested_at_formulation_level: bool,
) -> tuple[float, dict]:
    """
    Compute the supplementary score for a single formulation.

    Returns (score, components_dict) for transparency.
    """
    own = EVIDENCE_STATUS_BASE_SCORE.get(formulation_status, 15)
    inherited = INHERITANCE_FACTOR * parent_csrs

    # If the formulation itself is contested, don't add inherited evidence
    # bonus on top of an already-low own score — that would muddy the
    # signal. Use just the own contested score.
    if contested_at_formulation_level:
        score = own
    else:
        score = own + inherited

    # Cap at 100 for sanity
    score = min(score, 100.0)
    score = max(score, 0.0)

    return score, {
        "own_evidence_score": round(own, 2),
        "parent_csrs": round(parent_csrs, 2),
        "inherited_score": round(inherited, 2),
        "inheritance_factor": INHERITANCE_FACTOR,
        "contested_at_formulation_level": contested_at_formulation_level,
    }


def main() -> None:
    csrs_map = load_intervention_csrs()
    print(f"Loaded {len(csrs_map)} intervention CSRS scores from {INTERVENTIONS_PATH.name}")

    rows_in = []
    with FORMULATIONS_PATH.open() as f:
        reader = csv.DictReader(f)
        fieldnames_in = reader.fieldnames or []
        for row in reader:
            rows_in.append(row)

    print(f"Loaded {len(rows_in)} formulations from {FORMULATIONS_PATH.name}")

    # Stable sort by formulation_id for determinism
    rows_in.sort(key=lambda r: r.get("formulation_id", ""))

    rows_out = []
    fieldnames_out = list(fieldnames_in) + [
        "formulation_score",
        "score_own_evidence",
        "score_parent_csrs",
        "score_inherited",
    ]

    for row in rows_in:
        fid = row.get("formulation_id", "")
        parent_id = row.get("parent_intervention_id", "")
        status = row.get("formulation_evidence_status", "untested")
        contested_form = str(row.get("contested_at_formulation_level", "")).lower() == "true"

        parent_csrs = csrs_map.get(parent_id, 50.0)  # fallback to neutral
        if parent_id not in csrs_map:
            print(f"  WARN: {fid} parent {parent_id} not found in interventions.csv (using neutral 50)")

        score, components = compute_formulation_score(status, parent_csrs, contested_form)

        out_row = dict(row)
        out_row["formulation_score"] = round(score, 2)
        out_row["score_own_evidence"] = components["own_evidence_score"]
        out_row["score_parent_csrs"] = components["parent_csrs"]
        out_row["score_inherited"] = components["inherited_score"]
        rows_out.append(out_row)

    with OUTPUT_PATH.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames_out)
        writer.writeheader()
        writer.writerows(rows_out)

    print(f"\nWrote {len(rows_out)} scored formulations to {OUTPUT_PATH.name}")
    print()
    print("Top 10 formulations by score:")
    rows_out_sorted = sorted(rows_out, key=lambda r: -float(r["formulation_score"]))
    for row in rows_out_sorted[:10]:
        print(
            f"  {row['formulation_id']:9s}  {float(row['formulation_score']):6.2f}  "
            f"({row['parent_intervention_id']})  {row['formulation_name'][:60]}"
        )

    print()
    print("Verification — INT-0001 leucovorin parent CSRS unchanged:")
    leucovorin_csrs = csrs_map.get("INT-0001", None)
    if leucovorin_csrs is not None:
        print(f"  INT-0001 CSRS = {leucovorin_csrs:.2f}  (calibration anchor must remain ≥80)")
        if leucovorin_csrs >= 80.0:
            print("  CALIBRATION ANCHOR HOLDS")
        else:
            print(f"  WARNING: calibration anchor below 80")
    else:
        print("  WARN: INT-0001 not found in interventions.csv")


if __name__ == "__main__":
    main()
