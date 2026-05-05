#!/usr/bin/env python3
"""
validate_v02_calibration.py

Run all calibration cases through the v0.2 engine (profile-vector output)
and assert the new expected_* fields. Treats v0.2 expectations as the
authoritative test surface; v0.1 fields remain for back-compat but are
not enforced here.

Asserted v0.2 fields:
- expected_dominant_dimensions
- expected_dominant_dimensions_match_exact (bool)
- expected_undifferentiated_flag
- expected_multi_pattern_flag (optional)
- expected_profile_concentration_min (optional)
- expected_intervention_bundle_empty (optional)
- expected_top_intervention_primary_target_in (optional)
- expected_calibration_anchor_int_0001_in_top_5 (optional)
- expected_calibration_anchor_int_0001_rank_max (optional)

Exit 0 if all cases pass. Exit 1 with a per-case failure summary otherwise.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required (pip install pyyaml --break-system-packages)", file=sys.stderr)
    sys.exit(2)

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from personalized_risk import compute_personalized_risk, ENGINE_VERSION  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
CASES_DIR = REPO / "validation" / "calibration_cases"


def assert_v02(case_dir: Path) -> tuple[bool, list[str]]:
    failures = []
    case_id = case_dir.name

    # Load
    try:
        inp = json.load(open(case_dir / "input.json"))
    except Exception as e:
        return False, [f"input.json: {e}"]
    try:
        expected = yaml.safe_load(open(case_dir / "expected_output.yaml").read())
    except Exception as e:
        return False, [f"expected_output.yaml: {e}"]

    # Run
    out = compute_personalized_risk(inp)
    if out.get("status") != "success":
        return False, [f"engine status: {out.get('status')}"]

    ps = out.get("profile_summary") or {}
    pl = out.get("profile_loadings") or {}
    bundle = out.get("intervention_bundle") or []

    # ---- expected_dominant_dimensions ----
    expd = expected.get("expected_dominant_dimensions")
    actd = ps.get("dominant_dimensions") or []
    if expd is not None:
        exact = bool(expected.get("expected_dominant_dimensions_match_exact", True))
        if exact:
            if sorted(expd) != sorted(actd):
                failures.append(
                    f"dominant_dimensions exact-match failed: expected {expd} got {actd}"
                )
        else:
            # Loose check: every expected ID must appear (or list may be empty)
            missing = [p for p in expd if p not in actd]
            if missing:
                failures.append(
                    f"dominant_dimensions loose-match failed: missing {missing} from {actd}"
                )

    # ---- expected_undifferentiated_flag ----
    if "expected_undifferentiated_flag" in expected:
        exp_u = bool(expected["expected_undifferentiated_flag"])
        act_u = bool(ps.get("undifferentiated_flag"))
        if exp_u != act_u:
            failures.append(
                f"undifferentiated_flag: expected {exp_u} got {act_u}"
            )

    # ---- expected_multi_pattern_flag ----
    if "expected_multi_pattern_flag" in expected:
        exp_m = bool(expected["expected_multi_pattern_flag"])
        act_m = bool(ps.get("multi_pattern_flag"))
        if exp_m != act_m:
            failures.append(
                f"multi_pattern_flag: expected {exp_m} got {act_m}"
            )

    # ---- expected_profile_concentration_min ----
    if "expected_profile_concentration_min" in expected:
        exp_c = float(expected["expected_profile_concentration_min"])
        act_c = float(ps.get("profile_concentration") or 0.0)
        if act_c < exp_c:
            failures.append(
                f"profile_concentration too low: expected ≥ {exp_c} got {act_c:.3f}"
            )

    # ---- expected_intervention_bundle_empty ----
    if expected.get("expected_intervention_bundle_empty"):
        if len(bundle) > 0:
            failures.append(
                f"intervention_bundle expected empty, got {len(bundle)} entries"
            )

    # ---- expected_top_intervention_primary_target_in ----
    if "expected_top_intervention_primary_target_in" in expected:
        allowed = expected["expected_top_intervention_primary_target_in"] or []
        if bundle and allowed:
            primary = bundle[0].get("primary_target_dimension")
            if primary not in allowed:
                failures.append(
                    f"top intervention primary_target {primary} not in allowed set {allowed}"
                )
        elif bundle and not allowed:
            failures.append(
                f"top intervention exists but allowed-target list is empty"
            )

    # ---- discriminating bundle-shape assertions (audit Issue 2 fix) ----
    # When a non-empty bundle is expected, also verify the SHAPE of each
    # entry is what the UI consumes — not just the IDs. This catches engine
    # output schema drift that breaks the UI silently.
    if bundle and not expected.get("expected_intervention_bundle_empty"):
        # Every entry must carry the v0.2 schema fields the UI reads
        REQUIRED_FIELDS = [
            "intervention_id", "name", "score", "best_match_score",
            "primary_target_dimension", "target_dimensions",
            "recommendation_type",
        ]
        for i, entry in enumerate(bundle):
            for f in REQUIRED_FIELDS:
                if f not in entry:
                    failures.append(
                        f"intervention_bundle[{i}] missing required field `{f}`"
                    )
            # Score must be > 0 for any ranked entry
            try:
                if float(entry.get("score", 0)) <= 0:
                    failures.append(
                        f"intervention_bundle[{i}] {entry.get('intervention_id','?')} score is 0 or negative"
                    )
            except (TypeError, ValueError):
                failures.append(
                    f"intervention_bundle[{i}] score is not numeric: {entry.get('score')}"
                )
            # primary_target_dimension must be a real PHE-NNNN
            ptd = entry.get("primary_target_dimension")
            if ptd and not (isinstance(ptd, str) and ptd.startswith("PHE-")):
                failures.append(
                    f"intervention_bundle[{i}] primary_target_dimension `{ptd}` is not a valid PHE-NNNN id"
                )
            # target_dimensions ⊆ ALL phenotype IDs
            tds = entry.get("target_dimensions") or []
            for td in tds:
                if not (isinstance(td, str) and td.startswith("PHE-")):
                    failures.append(
                        f"intervention_bundle[{i}] target_dimensions contains invalid `{td}`"
                    )
        # First entry must be START
        if bundle[0].get("recommendation_type") != "START":
            failures.append(
                f"intervention_bundle[0] recommendation_type expected START got {bundle[0].get('recommendation_type')}"
            )

    # ---- calibration anchor expectations ----
    int_ids = [b["intervention_id"] for b in bundle]
    if "expected_calibration_anchor_int_0001_in_top_5" in expected:
        exp_in = bool(expected["expected_calibration_anchor_int_0001_in_top_5"])
        act_in = "INT-0001" in int_ids[:5]
        if exp_in != act_in:
            failures.append(
                f"INT-0001 in top 5: expected {exp_in} got {act_in} (bundle ids: {int_ids[:5]})"
            )
    if "expected_calibration_anchor_int_0001_rank_max" in expected:
        exp_rank = int(expected["expected_calibration_anchor_int_0001_rank_max"])
        try:
            act_rank = int_ids.index("INT-0001") + 1  # 1-indexed
        except ValueError:
            act_rank = 999
        if act_rank > exp_rank:
            failures.append(
                f"INT-0001 rank {act_rank} > max-allowed {exp_rank}"
            )

    return len(failures) == 0, failures


def main():
    print(f"v0.2 calibration validation — engine: {ENGINE_VERSION}\n")
    if not CASES_DIR.exists():
        print(f"ERROR: cases dir not found: {CASES_DIR}", file=sys.stderr)
        sys.exit(2)

    cases = sorted(p for p in CASES_DIR.iterdir() if p.is_dir())
    total_failures = 0
    for case_dir in cases:
        ok, failures = assert_v02(case_dir)
        if ok:
            print(f"  PASS  {case_dir.name}")
        else:
            print(f"  FAIL  {case_dir.name}")
            for f in failures:
                print(f"          - {f}")
            total_failures += 1

    print(f"\n{len(cases)} cases · {len(cases) - total_failures} pass · {total_failures} fail")
    sys.exit(0 if total_failures == 0 else 1)


if __name__ == "__main__":
    main()
