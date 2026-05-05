#!/usr/bin/env python3
"""
compute_responder_mae.py

Move 2 of post-mortem fix plan. Runs every entry in
validation/responder_rate_calibration/cohort.yaml through the v0.2 engine
on its representative input profile, asserts the engine's expected
behavior (intervention rank, primary target dimension, dominant phenotype),
and reports per-entry pass/fail + cohort-level MAE on responder rates.

v0.1 scope (current scaffold):
- Asserts the structural expectations (correct top phenotype, correct
  intervention surfaces in top 5).
- Computes responder-rate MAE only for entries where
  `published_responder_rate` and `placebo_responder_rate` are populated
  with numeric values. Currently 0 entries — placeholders pending
  full-text extraction. The script will report `MAE = pending` until
  cohort entries are filled in.

Usage:
  python scripts/compute_responder_mae.py
  python scripts/compute_responder_mae.py --strict   # exit nonzero on any miss
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required.", file=sys.stderr)
    sys.exit(2)

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
from personalized_risk import compute_personalized_risk, ENGINE_VERSION  # noqa: E402

COHORT_YAML = REPO / "validation" / "responder_rate_calibration" / "cohort.yaml"


def is_numeric(x):
    return isinstance(x, (int, float))


def evaluate_entry(entry: dict, base_dir: Path) -> dict:
    """Run engine on representative input, check expectations, return result."""
    eid = entry.get("entry_id", "?")
    rep_path = base_dir / entry.get("representative_input_profile_path", "")

    result = {
        "entry_id": eid,
        "rct_pmid": entry.get("rct_pmid"),
        "intervention_id": entry.get("intervention_id"),
        "structural_pass": False,
        "structural_failures": [],
        "abs_error": None,
        "skipped": False,
    }

    # Honor documented engine-gap flags BEFORE filesystem check.
    expected = entry.get("expected_engine_behavior") or {}
    if expected.get("_expected_to_fail_until_engine_v03"):
        result["skipped"] = True
        result["skip_reason"] = "documented engine gap — assertion deferred"
        return result
    if expected.get("_representative_input_pending"):
        result["skipped"] = True
        result["skip_reason"] = "representative input profile pending authoring"
        return result

    if not rep_path.exists():
        result["skipped"] = True
        result["structural_failures"].append(f"representative input not found: {rep_path}")
        return result

    inp = json.loads(rep_path.read_text())
    out = compute_personalized_risk(inp)
    if out.get("status") != "success":
        result["structural_failures"].append(f"engine status: {out.get('status')}")
        return result

    expected = entry.get("expected_engine_behavior") or {}
    bundle = out.get("intervention_bundle", []) or []
    int_ids = [b["intervention_id"] for b in bundle]
    ps = out.get("profile_summary", {}) or {}
    dom = set(ps.get("dominant_dimensions") or [])

    target_int = entry.get("intervention_id")
    target_phe = entry.get("target_phenotype_id")

    # Intervention in top 5
    if expected.get("intervention_in_top_5") and target_int and target_int not in int_ids[:5]:
        result["structural_failures"].append(
            f"target intervention {target_int} not in top 5 (got {int_ids[:5]})"
        )

    # Intervention rank max
    rank_max = expected.get("intervention_rank_max")
    if rank_max and target_int:
        try:
            rank = int_ids.index(target_int) + 1
        except ValueError:
            rank = 999
        if rank > rank_max:
            result["structural_failures"].append(
                f"target {target_int} rank {rank} exceeds max {rank_max}"
            )

    # Primary target dimension
    pt = expected.get("primary_target_dimension")
    if pt and bundle:
        actual_pt = bundle[0].get("primary_target_dimension")
        if actual_pt != pt:
            result["structural_failures"].append(
                f"top intervention primary_target_dimension {actual_pt} != expected {pt}"
            )

    # Dominant dimensions must include
    must_dom = set(expected.get("profile_dominant_dimensions_must_include") or [])
    missing = must_dom - dom
    if missing:
        result["structural_failures"].append(
            f"profile dominant_dimensions missing {sorted(missing)} (got {sorted(dom)})"
        )

    result["structural_pass"] = len(result["structural_failures"]) == 0

    # Responder-rate MAE — only if both rates are numeric
    pub_rate = entry.get("published_responder_rate")
    pred_rate = None
    if target_phe:
        # v0.1: use loading on target dimension as proxy "engine-predicted prob of being a responder"
        # This is a simple, interpretable proxy. v0.2+ will replace with calibrated within-phenotype
        # responder model (deferred per spec §7.5).
        loadings = out.get("profile_loadings", {}) or {}
        pred_rate = float(loadings.get(target_phe, 0.0))
    placebo_rate = entry.get("placebo_responder_rate")
    if is_numeric(pub_rate) and is_numeric(pred_rate):
        result["published_responder_rate"] = pub_rate
        result["engine_predicted_proxy"] = pred_rate
        result["abs_error"] = abs(pub_rate - pred_rate)
        if is_numeric(placebo_rate):
            result["published_response_minus_placebo"] = pub_rate - placebo_rate

    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--strict", action="store_true",
                        help="Exit nonzero if any structural assertion fails")
    args = parser.parse_args()

    if not COHORT_YAML.exists():
        print(f"ERROR: cohort.yaml not found: {COHORT_YAML}", file=sys.stderr)
        sys.exit(2)
    cohort = yaml.safe_load(COHORT_YAML.read_text())

    print(f"Responder-rate calibration — engine: {ENGINE_VERSION}")
    print(f"Cohort version: {cohort.get('cohort_version')}\n")

    entries = cohort.get("entries") or []
    base_dir = COHORT_YAML.parent

    results = [evaluate_entry(e, base_dir) for e in entries]
    structural_pass = sum(1 for r in results if r["structural_pass"] and not r["skipped"])
    structural_total = sum(1 for r in results if not r["skipped"])
    skipped = sum(1 for r in results if r["skipped"])
    mae_entries = [r for r in results if isinstance(r.get("abs_error"), (int, float))]

    print(f"Entries: {len(entries)}  ·  evaluated: {structural_total}  ·  skipped: {skipped}")
    print(f"Structural pass: {structural_pass}/{structural_total}\n")

    for r in results:
        eid = r["entry_id"]
        flag = "SKIP" if r["skipped"] else ("PASS" if r["structural_pass"] else "FAIL")
        print(f"  [{flag}] {eid}  PMID {r.get('rct_pmid','?')}")
        if r.get("structural_failures"):
            for f in r["structural_failures"]:
                print(f"           - {f}")
        if r.get("abs_error") is not None:
            print(f"           pred_proxy={r['engine_predicted_proxy']:.3f}  "
                  f"published={r['published_responder_rate']:.3f}  "
                  f"abs_error={r['abs_error']:.3f}")

    if mae_entries:
        mae = sum(r["abs_error"] for r in mae_entries) / len(mae_entries)
        print(f"\nCohort responder-rate MAE: {mae:.4f}  (n={len(mae_entries)} entries with numeric rates)")
    else:
        print("\nCohort responder-rate MAE: pending — no entries have numeric responder rates yet.")
        print("Next step: full-text extraction of n_responder/n_total/responder_definition for each entry.")

    if args.strict:
        any_fail = any(not r["structural_pass"] for r in results if not r["skipped"])
        sys.exit(1 if any_fail else 0)


if __name__ == "__main__":
    main()
