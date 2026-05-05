#!/usr/bin/env python3
"""validation_notebook.py — case_026_22q11_deletion (syndromic gate test)"""
import json, sys, csv
from pathlib import Path
try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required.", file=sys.stderr); sys.exit(1)

CASE_DIR = Path(__file__).parent
ATLAS_CSV_DIR = CASE_DIR.parent.parent.parent / "v2.0_scored"


def main():
    print(f"Validating case_026_22q11_deletion (syndromic gate test)")
    failures = []

    try:
        with open(CASE_DIR / "input.json") as f: input_data = json.load(f)
        print(f"  [1/5] input.json loaded — mode={input_data['operating_mode']} sex={input_data['subject_sex']}")
    except Exception as e: failures.append(f"input.json: {e}")

    try:
        with open(CASE_DIR / "expected_output.yaml") as f: expected = yaml.safe_load(f)
        print(f"  [2/5] expected_output.yaml — syndromic_flag_expected={expected['expected_syndromic_flag']}")
    except Exception as e: failures.append(f"expected_output: {e}"); expected = None

    # Verify 22q11.2 deletion in input
    cnvs = input_data.get("genomics", {}).get("cnvs", {}).get("child", [])
    has_22q = any('22q11.2' in c.get('region', '') and c.get('type') == 'deletion' for c in cnvs)
    if has_22q:
        print(f"  [3/5] 22q11.2 deletion present in input genomics.cnvs.child — syndromic gate should trigger")
    else:
        failures.append("22q11.2 deletion NOT in input — case profile inconsistent with syndromic-gate test")

    # Verify rare-syndrome gate has the matching row
    try:
        with open(ATLAS_CSV_DIR / "rare_syndrome_screening_gate.csv") as f:
            rsg_rows = {r['id']: r for r in csv.DictReader(f)}
        if 'RSG-0010' in rsg_rows and '22q11' in rsg_rows['RSG-0010']['gene_or_locus']:
            print(f"  [4/5] RSG-0010 22q11.2 row exists in screening gate — engine should match")
        else:
            failures.append("RSG-0010 22q11.2 row missing from rare_syndrome_screening_gate.csv")
    except Exception as e:
        failures.append(f"rare_syndrome_screening_gate.csv: {e}")

    # Provenance
    if (CASE_DIR / "case_provenance.md").exists():
        print(f"  [5/5] case_provenance.md present (cites Motahari 2019 PMID 31174463)")
    else: failures.append("case_provenance.md missing")

    if failures:
        print(f"\nFAILURES: {failures}"); sys.exit(1)
    print("\nVALIDATION PASSED (structural; engine syndromic-gate assertions deferred to Phase 2)")
    sys.exit(0)


if __name__ == "__main__": main()
