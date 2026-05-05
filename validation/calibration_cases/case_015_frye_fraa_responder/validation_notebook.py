#!/usr/bin/env python3
"""validation_notebook.py — case_015_frye_fraa_responder

BioMysteryBench-aligned validation per spec §24.5. Phase 2 will add engine
assertions; this version validates STRUCTURE.
"""
import json, sys, csv
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required.", file=sys.stderr); sys.exit(1)

CASE_DIR = Path(__file__).parent
ATLAS_ROOT = CASE_DIR.parent.parent.parent
ATLAS_CSV_DIR = ATLAS_ROOT / "v2.0_scored"


def load_atlas_ids():
    ids = {"phe": set(), "int": set()}
    files = {"phe": "phenotypes.csv", "int": "interventions.csv"}
    for key, fname in files.items():
        p = ATLAS_CSV_DIR / fname
        if not p.exists(): continue
        with open(p) as f:
            for r in csv.DictReader(f):
                ids[key].add(r["id"])
    return ids


def main():
    print(f"Validating case_015_frye_fraa_responder")
    failures = []

    # Load input
    try:
        with open(CASE_DIR / "input.json") as f:
            input_data = json.load(f)
        print(f"  [1/5] input.json loaded — mode={input_data['operating_mode']} sex={input_data['subject_sex']}")
    except Exception as e:
        failures.append(f"input.json failed: {e}")

    # Load expected
    try:
        with open(CASE_DIR / "expected_output.yaml") as f:
            expected = yaml.safe_load(f)
        print(f"  [2/5] expected_output.yaml — top={expected['expected_top_phenotype']} p∈[{expected['expected_phenotype_p_floor']},{expected['expected_phenotype_p_ceiling']}]")
    except Exception as e:
        failures.append(f"expected_output.yaml failed: {e}")
        expected = None

    # Atlas ID validation
    if expected:
        atlas = load_atlas_ids()
        if expected["expected_top_phenotype"] not in atlas["phe"]:
            failures.append(f"top phenotype {expected['expected_top_phenotype']} not in atlas")
        bad = [i for i in expected.get("expected_top_3_intervention_ids", []) if i not in atlas["int"]]
        if bad:
            failures.append(f"unknown interventions: {bad}")
        else:
            print(f"  [3/5] atlas IDs valid — {len(expected.get('expected_top_3_intervention_ids', []))} intervention IDs")

    # FRAA-positive in input?
    fraa_pos = input_data.get("immunology", {}).get("autoantibodies", {}).get("fraa_blocking", {})
    if fraa_pos and fraa_pos.get("result", "").startswith("positive"):
        print(f"  [4/5] FRAA blocking positive in input ({fraa_pos['value']} {fraa_pos['unit']}) — supports PHE-0001 routing")
    else:
        failures.append("FRAA blocking not positive in input — case profile inconsistent")

    # Provenance
    if (CASE_DIR / "case_provenance.md").exists():
        print(f"  [5/5] case_provenance.md present")
    else:
        failures.append("case_provenance.md missing")

    if failures:
        print(f"\nFAILURES: {failures}")
        sys.exit(1)
    print("\nVALIDATION PASSED (structural; engine assertions deferred to Phase 2)")
    sys.exit(0)


if __name__ == "__main__":
    main()
