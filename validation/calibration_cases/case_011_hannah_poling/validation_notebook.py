#!/usr/bin/env python3
"""
validation_notebook.py — case_011_hannah_poling

BioMysteryBench-aligned validation notebook (per spec §24.5).

Loads input.json + expected_output.yaml. When the engine
(personalized_risk.py) is implemented in Phase 2, this notebook runs the
engine on input.json and asserts equality with expected_output.yaml on
every required field.

Until Phase 2 implementation, this notebook validates STRUCTURE: that the
input.json parses, that expected_output.yaml parses, and that all referenced
atlas IDs (PHE-NNNN, INT-NNNN) exist in the atlas. Phase 2 lights up the
full engine assertions.

Run:
    python validation_notebook.py

Exits 0 on success, 1 on failure.
"""

import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. Install with: pip install --break-system-packages pyyaml", file=sys.stderr)
    sys.exit(1)

import csv

CASE_DIR = Path(__file__).parent
ATLAS_ROOT = CASE_DIR.parent.parent.parent  # /Users/Greg/Autism
ATLAS_CSV_DIR = ATLAS_ROOT / "v2.0_scored"


def load_atlas_ids():
    """Load valid atlas IDs for cross-checking."""
    ids = {"phe": set(), "int": set(), "mec": set(), "hyp": set(), "bio": set()}
    files = {
        "phe": "phenotypes.csv",
        "int": "interventions.csv",
        "mec": "mechanisms.csv",
        "hyp": "hypotheses.csv",
        "bio": "biomarkers.csv",
    }
    for key, fname in files.items():
        path = ATLAS_CSV_DIR / fname
        if not path.exists():
            print(f"WARN: atlas file not found: {path}")
            continue
        with open(path) as f:
            for r in csv.DictReader(f):
                ids[key].add(r["id"])
    return ids


def main():
    print(f"Validating case_011_hannah_poling at {CASE_DIR}")
    print()

    failures = []

    # 1. Load input.json
    print("[1/5] Loading input.json...")
    try:
        with open(CASE_DIR / "input.json") as f:
            input_data = json.load(f)
        print(f"      OK: input version {input_data.get('input_version')}, mode {input_data.get('operating_mode')}")
    except Exception as e:
        failures.append(f"input.json failed to load: {e}")
        print(f"      FAIL: {e}")
        input_data = None

    # 2. Load expected_output.yaml
    print("[2/5] Loading expected_output.yaml...")
    try:
        with open(CASE_DIR / "expected_output.yaml") as f:
            expected = yaml.safe_load(f)
        print(f"      OK: expected_top_phenotype={expected.get('expected_top_phenotype')}")
    except Exception as e:
        failures.append(f"expected_output.yaml failed to load: {e}")
        print(f"      FAIL: {e}")
        expected = None

    # 3. Cross-check referenced IDs against atlas
    print("[3/5] Cross-checking atlas IDs...")
    if expected:
        atlas_ids = load_atlas_ids()
        # Check expected_top_phenotype
        top_phe = expected.get("expected_top_phenotype")
        if top_phe and top_phe not in atlas_ids["phe"]:
            failures.append(f"expected_top_phenotype {top_phe} not in atlas phenotypes.csv")
            print(f"      FAIL: {top_phe} not in atlas")
        else:
            print(f"      OK: {top_phe} valid")

        # Check secondary phenotypes
        for phe_id in (expected.get("expected_phenotype_secondary_min_posterior") or {}):
            if phe_id not in atlas_ids["phe"]:
                failures.append(f"secondary phenotype {phe_id} not in atlas")

        # Check expected_top_3_intervention_ids
        bad_ints = []
        for int_id in expected.get("expected_top_3_intervention_ids", []):
            if int_id not in atlas_ids["int"]:
                bad_ints.append(int_id)
        if bad_ints:
            failures.append(f"intervention IDs not in atlas: {bad_ints}")
            print(f"      FAIL: invalid intervention IDs {bad_ints}")
        else:
            print(f"      OK: all {len(expected.get('expected_top_3_intervention_ids', []))} intervention IDs valid")

        # Check expected_recommendation_types interventions
        for int_id in (expected.get("expected_recommendation_types") or {}):
            if int_id not in atlas_ids["int"]:
                failures.append(f"recommendation_types intervention {int_id} not in atlas")

    # 4. Engine run (Phase 2 — placeholder until implementation)
    print("[4/5] Engine assertions (Phase 2 placeholder)...")
    engine_module_path = ATLAS_ROOT / "personalized_risk.py"
    if engine_module_path.exists():
        # When engine ships, import and run
        print(f"      ENGINE RUN: would invoke compute_personalized_risk(input_data) here")
        # TODO Phase 2:
        #   from personalized_risk import compute_personalized_risk
        #   actual = compute_personalized_risk(input_data)
        #   assert actual["phenotype_ranking"][0] == expected["expected_top_phenotype"]
        #   ...
    else:
        print(f"      DEFERRED: personalized_risk.py not yet implemented (Phase 2)")
        print(f"      Structural validation passed; engine assertions await Phase 2.")

    # 5. Provenance file present
    print("[5/5] Checking provenance file...")
    prov_path = CASE_DIR / "case_provenance.md"
    if prov_path.exists():
        print(f"      OK: case_provenance.md present ({prov_path.stat().st_size} bytes)")
    else:
        failures.append("case_provenance.md missing")
        print(f"      FAIL: case_provenance.md missing")

    print()
    if failures:
        print(f"VALIDATION FAILED — {len(failures)} issues:")
        for f in failures:
            print(f"  - {f}")
        sys.exit(1)
    else:
        print("VALIDATION PASSED (structural; engine assertions deferred to Phase 2)")
        sys.exit(0)


if __name__ == "__main__":
    main()
