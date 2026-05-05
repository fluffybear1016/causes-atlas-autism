#!/usr/bin/env python3
"""Merge proposed gene-layer edges into v2.0.1_expanded, re-score, verify
calibration, then promote to v2.0_scored if it passes."""

import csv, datetime as dt, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROP = ROOT / "v2.0.1_proposed"
EXPANDED = ROOT / "v2.0.1_expanded"
SCORED_OUT = ROOT / "scored_output_v20"
NOW = dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')

# ---- Merge proposal rows into expanded edge tables ----
def merge_into(canonical_table, proposed_csv, prefix, fk_col):
    """Append proposed rows to a canonical edge table inside v2.0.1_expanded.
       Drops the extra `rationale` column from the proposal CSV."""
    target = EXPANDED / f"{canonical_table}.csv"
    with open(target, newline='') as f:
        rdr = csv.DictReader(f); fields = rdr.fieldnames; existing = list(rdr)
    # max id number for next-id assignment
    max_n = 0
    for e in existing:
        try: max_n = max(max_n, int(e['id'].split('-')[-1]))
        except (ValueError, IndexError): pass
    proposed = list(csv.DictReader(open(PROP / proposed_csv)))
    new_rows = []
    for p in proposed:
        max_n += 1
        new = {f: '' for f in fields}
        new['id'] = f"{prefix}-{max_n:05d}"
        new['gene_id'] = p['gene_id']
        new[fk_col] = p[fk_col]
        new['relation_type'] = p['relation_type']
        new['polarity'] = p['polarity']
        new['evidence_strength_aggregate'] = '0.0'
        if 'status' in fields: new['status'] = 'active'
        if 'created_at' in fields: new['created_at'] = NOW
        if 'last_updated' in fields: new['last_updated'] = NOW
        new_rows.append(new)
    with open(target, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader()
        w.writerows(existing + new_rows)
    print(f"  {canonical_table}.csv: {len(existing)} -> {len(existing)+len(new_rows)} rows (+{len(new_rows)})")

print("Merging gene-layer proposal into v2.0.1_expanded/")
merge_into('gene_hypothesis_edges', 'proposed_gene_hypothesis_edges.csv', 'GHE', 'hypothesis_id')
merge_into('gene_phenotype_edges',  'proposed_gene_phenotype_edges.csv',  'GPE', 'phenotype_id')
merge_into('gene_mechanism_edges',  'proposed_gene_mechanism_edges.csv',  'GME', 'mechanism_id')
print()

# ---- Run scoring ----
print("Running scoring on v2.0.1_expanded/ (with gene layer)…")
# Symlink expected input dir
expected_in = ROOT / 'expanded_output_v20'
if expected_in.is_symlink() or expected_in.exists():
    try: expected_in.unlink()
    except OSError: pass
try: expected_in.symlink_to(EXPANDED)
except FileExistsError: pass

proc = subprocess.run([sys.executable, str(ROOT/'run_scoring_v20.py')],
                      cwd=str(ROOT), capture_output=True, text=True, timeout=120)
out = proc.stdout.strip().splitlines()
for line in out[-15:]: print(f"  {line}")
if proc.returncode != 0:
    print("SCORING FAILED")
    print(proc.stderr[-2000:])
    sys.exit(1)

# ---- Verify calibration ----
print()
print("Calibration check…")
new_int = {r['id']: float(r['csrs_score'] or 0) for r in csv.DictReader(open(SCORED_OUT/'interventions.csv'))}
old_int = {r['id']: float(r['csrs_score'] or 0) for r in csv.DictReader(open(ROOT/'v2.0_scored'/'interventions.csv'))}

leuco = new_int['INT-0001']
print(f"  INT-0001 Leucovorin: {leuco:.2f} (was {old_int['INT-0001']:.2f}) — {'PASS' if leuco>=80 else 'FAIL'}")
if leuco < 80:
    print("CALIBRATION FAILED — not promoting. Inspect /tmp for details.")
    sys.exit(1)

# Top 10 deltas
print()
print(f"  {'rank':<5} {'ID':<10} {'name':<46} {'new':>7} {'old':>7} {'Δ':>7}")
new_rows = sorted([(r['id'], r['name'], float(r['csrs_score'])) for r in csv.DictReader(open(SCORED_OUT/'interventions.csv'))], key=lambda x: -x[2])
for i,(iid,nm,ns) in enumerate(new_rows[:10],1):
    os_ = old_int.get(iid,0)
    print(f"  {i:<5} {iid:<10} {nm[:44]:<46} {ns:>7.2f} {os_:>7.2f} {ns-os_:>+7.2f}")

# HYP-0028 confidence change
print()
hyp = {r['id']: r for r in csv.DictReader(open(SCORED_OUT/'hypotheses.csv'))}
oh  = {r['id']: r for r in csv.DictReader(open(ROOT/'v2.0_scored'/'hypotheses.csv'))}
h28 = hyp['HYP-0028']; ho28 = oh['HYP-0028']
print(f"  HYP-0028 Inherited polygenic risk:")
print(f"    confidence: {ho28['confidence_score']} -> {h28['confidence_score']}")
print(f"    evidence_count: {ho28['evidence_count']} -> {h28['evidence_count']}")

# ---- Promote ----
print()
print("Promoting v2.0.1 (with gene layer) -> v2.0_scored canonical")
SRC = ROOT / 'v2.0_scored'
# Backup current
backup = ROOT / 'v2.0_scored.before_gene_layer'
if backup.exists(): shutil.rmtree(backup, ignore_errors=True)
try:
    shutil.copytree(SRC, backup)
    print(f"  backup: -> {backup.name}/")
except Exception as e:
    print(f"  backup skipped: {e}")
# Replace SRC contents with scored output
for fn in SCORED_OUT.iterdir():
    if fn.is_file():
        shutil.copy2(fn, SRC / fn.name)
print(f"  v2.0_scored canonical updated.")

# Also promote to v2.0.1_scored
v201 = ROOT / 'v2.0.1_scored'
for fn in SCORED_OUT.iterdir():
    if fn.is_file():
        shutil.copy2(fn, v201 / fn.name)
print(f"  v2.0.1_scored snapshot updated.")

# Cleanup symlink
try: expected_in.unlink()
except OSError: pass

print()
print("Done. Next: rebuild vault.")
