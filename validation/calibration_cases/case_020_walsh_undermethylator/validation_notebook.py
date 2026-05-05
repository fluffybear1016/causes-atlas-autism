#!/usr/bin/env python3
"""validation_notebook.py — case_020_walsh_undermethylator"""
import json, sys, csv
from pathlib import Path
try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required.", file=sys.stderr); sys.exit(1)

CASE_DIR = Path(__file__).parent
ATLAS_CSV_DIR = CASE_DIR.parent.parent.parent / "v2.0_scored"


def main():
    print(f"Validating case_020_walsh_undermethylator")
    failures = []
    try:
        with open(CASE_DIR / "input.json") as f: input_data = json.load(f)
        print(f"  [1/5] input.json loaded — mode={input_data['operating_mode']} sex={input_data['subject_sex']}")
    except Exception as e: failures.append(f"input.json: {e}")

    try:
        with open(CASE_DIR / "expected_output.yaml") as f: expected = yaml.safe_load(f)
        print(f"  [2/5] expected_output.yaml — top={expected['expected_top_phenotype']}")
    except Exception as e: failures.append(f"expected_output: {e}"); expected = None

    if expected:
        with open(ATLAS_CSV_DIR / "phenotypes.csv") as f: phe = set(r['id'] for r in csv.DictReader(f))
        with open(ATLAS_CSV_DIR / "interventions.csv") as f: ints = set(r['id'] for r in csv.DictReader(f))
        if expected["expected_top_phenotype"] not in phe:
            failures.append(f"top phenotype not in atlas")
        bad = [i for i in expected.get("expected_top_3_intervention_ids", []) if i not in ints]
        if bad: failures.append(f"unknown interventions: {bad}")
        else: print(f"  [3/5] atlas IDs valid")

    metab = input_data.get("metabolomics_proteomics_epigenetics", {}).get("metabolomics", {})
    aa = metab.get("amino_acids_plasma") or {}
    untargeted = metab.get("untargeted_metabolomics_z_scores") or {}
    if aa.get("histamine_low_per_walsh") and untargeted.get("sam_sah_low_per_walsh"):
        print(f"  [4/5] Walsh undermethylator markers present (low whole-blood histamine + low SAM/SAH)")
    else:
        failures.append("Walsh undermethylator markers absent — case profile inconsistent")

    if (CASE_DIR / "case_provenance.md").exists():
        print(f"  [5/5] case_provenance.md present")
    else: failures.append("case_provenance missing")

    if failures:
        print(f"\nFAILURES: {failures}"); sys.exit(1)
    print("\nVALIDATION PASSED (structural; engine assertions deferred to Phase 2)")
    sys.exit(0)


if __name__ == "__main__": main()
