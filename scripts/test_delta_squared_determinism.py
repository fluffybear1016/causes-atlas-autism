#!/usr/bin/env python3
"""
test_delta_squared_determinism.py — runs the Δ² engine twice and asserts
byte-identical CSV output (excluding append-only history & timestamped
files). Determinism is a CLAUDE.md spec requirement; this catches drift.

Outputs:
  PASS → exit 0, prints summary
  FAIL → exit 1, prints diff for the first non-matching file

Run via: python3 scripts/test_delta_squared_determinism.py
"""

from __future__ import annotations
import hashlib, pathlib, shutil, subprocess, sys, tempfile

REPO        = pathlib.Path(__file__).resolve().parent.parent
ENGINE      = REPO / "scripts" / "compute_delta_squared.py"
OUTPUT_DIR  = REPO / "delta_squared_v1"

# Files we expect to be byte-identical across two runs (deterministic state).
# History and anomaly files append timestamped rows, so they ARE expected to
# differ; calibration_status.txt also has a timestamp; run_summary.json has a
# timestamp. We exclude those and check only the deterministic outputs.
DETERMINISTIC_FILES = ["rankings.csv", "components.csv"]

def md5(path: pathlib.Path) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def snapshot(label: str, work: pathlib.Path):
    """Run the engine and copy the deterministic outputs to work/<label>/."""
    rc = subprocess.run([sys.executable, str(ENGINE)], cwd=str(REPO))
    if rc.returncode != 0:
        print(f"FAIL: engine exited {rc.returncode} on run '{label}'")
        sys.exit(1)
    dest = work / label
    dest.mkdir(parents=True, exist_ok=True)
    for fname in DETERMINISTIC_FILES:
        shutil.copy2(OUTPUT_DIR / fname, dest / fname)
    return dest

def main():
    if not ENGINE.exists():
        print(f"FAIL: engine not found at {ENGINE}")
        sys.exit(1)
    with tempfile.TemporaryDirectory(prefix="d2_determinism_") as td:
        work = pathlib.Path(td)
        snap1 = snapshot("run1", work)
        snap2 = snapshot("run2", work)

        all_ok = True
        for fname in DETERMINISTIC_FILES:
            h1 = md5(snap1 / fname)
            h2 = md5(snap2 / fname)
            if h1 == h2:
                print(f"  [PASS] {fname:24s} md5={h1}")
            else:
                all_ok = False
                print(f"  [FAIL] {fname:24s} md5_run1={h1} md5_run2={h2}")
                # Show first diff line
                with open(snap1/fname) as f1, open(snap2/fname) as f2:
                    for i, (l1, l2) in enumerate(zip(f1, f2), 1):
                        if l1 != l2:
                            print(f"    first diff at line {i}:")
                            print(f"      run1: {l1.rstrip()}")
                            print(f"      run2: {l2.rstrip()}")
                            break
        if all_ok:
            print("\nDETERMINISM TEST PASSED")
            sys.exit(0)
        else:
            print("\nDETERMINISM TEST FAILED")
            sys.exit(1)

if __name__ == "__main__":
    main()
