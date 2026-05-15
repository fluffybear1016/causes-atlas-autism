#!/usr/bin/env python3
"""
precommit_field_outcomes_firewall.py

THE FIREWALL.

Per ACTIONABLE_REPORT_PRODUCT_SPEC.md §"Mitigation 2" and SIX_MONTH_
FAILURE_MODES.md, parent-submitted outcome data ("field outcomes") must
NEVER feed back into the scoring engine or the published responder-rate
cohort. Selection bias toward "it worked" would silently pull the
0.049 / 0.067 / 83.35 calibration anchors. Once that drift starts, the
atlas's published methodology becomes unsupportable.

This firewall mirrors §24 verify-before-write in spirit: instead of
PMID-fabrication detection, it detects scoring-engine code that touches
field_outcomes.csv.

The rules:
  1. Nothing in v2.0_scored/ (other than field_outcomes.csv itself) may
     reference or import field_outcomes.
  2. No file in scripts/ that produces calibration scores, cohort MAE,
     or CSRS may read from field_outcomes.csv.
  3. field_outcomes.csv is curator-write, engine-read-never.
  4. Surfaces that DO read field_outcomes (e.g. a future "parent
     community report" surface) must declare it explicitly via the
     allowlist below.

Allowlist (files explicitly permitted to read field_outcomes):
  - scripts/report/parent_community_view.py  (planned, not yet written)
  - scripts/intake/field_outcome_ingest.py   (planned, not yet written)

Run as a pre-commit hook OR manually:
  python3 scripts/precommit_field_outcomes_firewall.py
"""

from __future__ import annotations
import sys
from pathlib import Path

_CANDIDATE_REPOS = [
    Path("/Users/Greg/Autism"),
    Path("/sessions/jolly-determined-darwin/mnt/Autism"),
]
REPO = next((p for p in _CANDIDATE_REPOS if p.exists()), _CANDIDATE_REPOS[0])

# Files explicitly permitted to read field_outcomes.csv
ALLOWLIST = {
    "scripts/report/parent_community_view.py",
    "scripts/intake/field_outcome_ingest.py",
    "scripts/precommit_field_outcomes_firewall.py",  # this file
}

# Files / globs that MUST NOT touch field_outcomes
SCORING_ENGINE_PATHS = [
    "scripts/run_scoring_v20.py",
    "scripts/run_scoring*.py",
    "scripts/compute_responder_mae.py",
    "scripts/validate_v02_calibration.py",
    "scripts/compute_delta_squared.py",
    "scripts/compute_formulation_scores.py",
    "scripts/personalized_risk*.py",
]

# Strings that indicate scoring-engine code is reading field_outcomes
FORBIDDEN_PATTERNS = [
    "field_outcomes.csv",
    "field_outcomes_csv",
    "read_csv('field_outcomes",
    'read_csv("field_outcomes',
    "from.*field_outcome",
    "import.*field_outcome",
]


def find_violations() -> list[tuple[str, str, int, str]]:
    """Returns list of (path, pattern, line_num, line_text) violations."""
    violations = []
    scripts_dir = REPO / "scripts"
    scored_dir = REPO / "v2.0_scored"

    # Check scoring engine scripts
    for py_path in scripts_dir.rglob("*.py"):
        rel = py_path.relative_to(REPO).as_posix()
        if rel in ALLOWLIST:
            continue
        # Is this a scoring-engine file?
        is_engine = any(
            py_path.match(p) or rel == p
            for p in SCORING_ENGINE_PATHS
        )
        try:
            text = py_path.read_text()
        except (UnicodeDecodeError, OSError):
            continue
        for line_num, line in enumerate(text.split("\n"), 1):
            for pattern in FORBIDDEN_PATTERNS:
                if pattern in line:
                    # For non-engine files, also flag if not in allowlist
                    if is_engine or rel not in ALLOWLIST:
                        violations.append((rel, pattern, line_num, line.strip()))

    # Check v2.0_scored/ for stray field_outcomes references in
    # non-field-outcomes files
    if scored_dir.exists():
        for csv_path in scored_dir.glob("*.csv"):
            if csv_path.name == "field_outcomes.csv":
                continue
            try:
                text = csv_path.read_text()
            except (UnicodeDecodeError, OSError):
                continue
            if "field_outcomes" in text:
                violations.append((
                    csv_path.relative_to(REPO).as_posix(),
                    "field_outcomes",
                    0,
                    "CSV contains field_outcomes reference"
                ))

    return violations


def main() -> int:
    print("Running field_outcomes firewall check...")
    violations = find_violations()
    if violations:
        print()
        print("❌ FIREWALL VIOLATIONS:")
        print("   Scoring engine code may not read field_outcomes.csv.")
        print("   This protects the published calibration anchors from")
        print("   parent-reported-outcome selection bias drift.")
        print()
        for path, pattern, line_num, line in violations:
            print(f"  {path}:{line_num}")
            print(f"    forbidden pattern: {pattern!r}")
            print(f"    line: {line[:120]}")
            print()
        print("Fix options:")
        print("  1. Remove the field_outcomes reference from the scoring file")
        print("  2. If the reference is intentional for a parent-community")
        print("     surface, add the file path to ALLOWLIST in this script")
        return 1
    print("✅ Firewall clean: scoring engine has zero field_outcomes references")
    print("   Published 0.049 / 0.067 / 83.35 calibration anchors remain")
    print("   protected from outcome-feedback drift.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
