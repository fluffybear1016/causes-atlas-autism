#!/usr/bin/env python3
"""
apply_patches_and_score.py — End-to-end:
  1. Apply final PMID patches (5 candidate edges) after abstract review.
  2. Regenerate vault/MAPPING_PROPOSAL.md with the final verified list.
  3. Build v2.0.1_expanded/ = copy of v2.0_scored/ + merged proposal rows.
  4. Run the scoring engine on v2.0.1_expanded/.
  5. Confirm INT-0001 calibration ≥ 80.
  6. Rebuild the vault from v2.0.1_scored/.
"""

import csv
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "v2.0_scored"
PROP = ROOT / "v2.0.1_proposed"
EXPANDED = ROOT / "v2.0.1_expanded"
SCORED = ROOT / "v2.0.1_scored"

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

# Final patches based on abstract-level review
FINAL_PATCHES = {
    "CAND-0013": (["29364488", "40861274"], "AMPK/FoxO3 (Zhang 2018) + FoxO exercise review (Liu 2025)"),
    "CAND-0014": (["11685390", "27882645"], "Lithium → BDNF rat brain (Fukumoto 2001) + neuron culture (De-Paula 2016)"),
    "CAND-0015": (["32989388"], "Lithium chloride → mTOR phosphorylation (Xiao 2020); single direct ref."),
    "CAND-0016": (["39479697", "40293706"], "Myo-inositol → AMPK/PI3K/AKT (Aghajani 2024 RCT) + maternal myo-inositol → PI3K/Akt/mTOR (Guo 2025)"),
    "CAND-0020": (["28502607", "32635367"], "Serum zonulin elevated in ASD (Esnafoglu 2017) + zonulin/permeability meta-analysis (Asbjornsdottir 2020)"),
}

def http(url):
    req = urllib.request.Request(url, headers={"User-Agent":"causes-atlas/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r: return r.read().decode()

# === STEP 1: patch CSV ====================================================
print("="*72)
print("STEP 1: Patching candidate_orphan_edges_verified.csv with final picks")
print("="*72)
CSV_PATH = PROP / "candidate_orphan_edges_verified.csv"
rows = []
with open(CSV_PATH, newline="", encoding="utf-8") as f:
    rdr = csv.DictReader(f)
    fieldnames = rdr.fieldnames
    for row in rdr:
        if row["id"] in FINAL_PATCHES:
            new_pmids, note = FINAL_PATCHES[row["id"]]
            row["supporting_pmids"] = ";".join(new_pmids)
            row["status"] = "verified"
            row["verification_query"] = note
            print(f"  patched {row['id']}: PMIDs -> {new_pmids}")
        rows.append(row)
with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fieldnames); w.writeheader(); w.writerows(rows)

# === STEP 2: regenerate proposal MD with new PMIDs ========================
print()
print("="*72)
print("STEP 2: Regenerating MAPPING_PROPOSAL.md with abstract-verified PMIDs")
print("="*72)
subprocess.run([sys.executable, str(ROOT / "regenerate_proposal.py")], check=True)

# === STEP 3: build v2.0.1_expanded/ =======================================
print()
print("="*72)
print("STEP 3: Building v2.0.1_expanded/ (copy v2.0_scored/ + merge proposal)")
print("="*72)
if EXPANDED.exists():
    shutil.rmtree(EXPANDED)
shutil.copytree(SRC, EXPANDED)
print(f"  copied {SRC} -> {EXPANDED}")

# Merge derived intervention_phenotype edges (Phase A - 144 rows)
ipe_path = EXPANDED / "intervention_phenotype_edges.csv"
existing_ipe = []
with open(ipe_path, newline="", encoding="utf-8") as f:
    rdr = csv.DictReader(f); ipe_fields = rdr.fieldnames
    existing_ipe = list(rdr)
print(f"  existing intervention_phenotype_edges: {len(existing_ipe)} rows")

with open(PROP / "derived_intervention_phenotype_edges.csv", newline="", encoding="utf-8") as f:
    derived = list(csv.DictReader(f))
# Map derived columns to canonical IPE schema; drop the 2 extra columns
new_ipe_rows = []
next_id_n = 1
for d in derived:
    new_ipe_rows.append({
        "id": f"IPE-{next_id_n:05d}",
        "intervention_id": d["intervention_id"],
        "phenotype_id": d["phenotype_id"],
        "relation_type": d["relation_type"],
        "polarity": d["polarity"] or "unknown",
        "evidence_for_count": "",
        "evidence_against_count": "",
        "evidence_strength_aggregate": d["evidence_strength_aggregate"],
        "context_scope": "",
        "status": "active",  # mark as active so scoring engine includes them
        "created_at": d["created_at"],
        "last_updated": d["last_updated"],
    })
    next_id_n += 1
with open(ipe_path, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=ipe_fields); w.writeheader()
    w.writerows(existing_ipe + new_ipe_rows)
print(f"  appended {len(new_ipe_rows)} derived rows")

# Merge candidate_orphan_edges by routing each row to its destination edge_table
print("  routing candidate orphan edges to destination tables…")
# Group rows by edge_table
groups = {}
for r in rows:
    if r["status"] != "verified": continue
    groups.setdefault(r["edge_table"], []).append(r)

# id prefix per table, for picking next IDs
PREFIX = {
    "hypothesis_mechanism_edges": "HME",
    "intervention_hypothesis_edges": "IHE",
    "intervention_mechanism_edges": "IME",
    "intervention_phenotype_edges": "IPE",
    "mechanism_phenotype_edges": "MPE",
    "gene_hypothesis_edges": "GHE",
    "gene_mechanism_edges": "GME",
    "gene_phenotype_edges": "GPE",
    "intervention_gene_edges": "IGE",
}

# Special schema for hypothesis-phenotype: routed via "intervention_phenotype_edges"
# in the proposal (schema mismatch). Re-route hypothesis→phenotype rows somewhere else?
# Actually the canonical state has no hypothesis_phenotype_edges table. The cleanest
# route is to skip these and surface them as a separate proposal artifact.
# For now: emit them to a new "hypothesis_phenotype_proposed.csv" file.
hp_rows = []

for tbl, table_rows in groups.items():
    # Filter out hypothesis→phenotype mis-routed rows
    real_rows = []
    for r in table_rows:
        if r["from_id"].startswith("HYP-") and r["to_id"].startswith("PHE-"):
            hp_rows.append(r)
            continue
        real_rows.append(r)
    if not real_rows: continue
    if tbl not in PREFIX:
        print(f"  WARN: unknown edge_table '{tbl}' for {len(real_rows)} rows; skipping")
        continue
    target = EXPANDED / f"{tbl}.csv"
    if not target.exists():
        print(f"  WARN: {target.name} not present in v2.0_scored; skipping")
        continue
    with open(target, newline="", encoding="utf-8") as f:
        rdr = csv.DictReader(f); fields = rdr.fieldnames; existing = list(rdr)
    # Determine next ID number from existing IDs
    max_n = 0
    for e in existing:
        eid = e.get("id", "")
        try:
            n = int(eid.split("-")[-1])
            max_n = max(max_n, n)
        except (ValueError, IndexError): pass
    new_rows = []
    for r in real_rows:
        max_n += 1
        new_id = f"{PREFIX[tbl]}-{max_n:05d}"
        # Determine column names for from/to in this table
        if tbl.startswith("hypothesis_"):
            cols = ("hypothesis_id", tbl.split("_")[1] + "_id")
        elif tbl.startswith("intervention_"):
            cols = ("intervention_id", tbl.split("_")[1] + "_id")
        elif tbl.startswith("mechanism_"):
            cols = ("mechanism_id", "phenotype_id")
        elif tbl.startswith("gene_"):
            cols = ("gene_id", tbl.split("_")[1] + "_id")
        else:
            cols = ("from_id", "to_id")
        row = {f: "" for f in fields}
        row["id"] = new_id
        row[cols[0]] = r["from_id"]
        row[cols[1]] = r["to_id"]
        row["relation_type"] = r["relation_type"]
        row["polarity"] = r["polarity"] or "unknown"
        if "status" in fields: row["status"] = "active"
        if "created_at" in fields: row["created_at"] = r["created_at"]
        if "last_updated" in fields: row["last_updated"] = r["created_at"]
        if "notes" in fields: row["notes"] = f"merged from {r['id']}; PMIDs={r['supporting_pmids']}"
        new_rows.append(row)
    with open(target, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader()
        w.writerows(existing + new_rows)
    print(f"  appended {len(new_rows):3d} rows to {tbl}.csv")

# Save hypothesis→phenotype rows separately (no canonical table for them)
if hp_rows:
    hp_path = PROP / "hypothesis_phenotype_proposed.csv"
    with open(hp_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["id","hypothesis_id","phenotype_id",
            "relation_type","polarity","supporting_pmids","status","created_at"])
        w.writeheader()
        for r in hp_rows:
            w.writerow({
                "id": r["id"].replace("CAND-", "HPE-"),
                "hypothesis_id": r["from_id"], "phenotype_id": r["to_id"],
                "relation_type": r["relation_type"], "polarity": r["polarity"],
                "supporting_pmids": r["supporting_pmids"],
                "status": "proposed", "created_at": r["created_at"],
            })
    print(f"  saved {len(hp_rows)} hypothesis→phenotype rows to {hp_path.name}")
    print("    (no canonical hypothesis_phenotype_edges table; deferred)")

# === STEP 4: run the scoring engine =======================================
print()
print("="*72)
print("STEP 4: Running scoring engine on v2.0.1_expanded/")
print("="*72)

# The script has hardcoded paths. Use temp symlinks so we don't edit the script.
expected_in = ROOT / "expanded_output_v20"
expected_out = ROOT / "scored_output_v20"
# Save existing if present
saved_in = saved_out = None
if expected_in.exists() or expected_in.is_symlink():
    saved_in = ROOT / "expanded_output_v20.bak"
    if saved_in.exists() or saved_in.is_symlink():
        if saved_in.is_symlink(): saved_in.unlink()
        else: shutil.rmtree(saved_in)
    expected_in.rename(saved_in)
if expected_out.exists() or expected_out.is_symlink():
    saved_out = ROOT / "scored_output_v20.bak"
    if saved_out.exists() or saved_out.is_symlink():
        if saved_out.is_symlink(): saved_out.unlink()
        else: shutil.rmtree(saved_out)
    expected_out.rename(saved_out)

try:
    expected_in.symlink_to(EXPANDED)
    print(f"  symlink: expanded_output_v20 -> {EXPANDED.name}")
    proc = subprocess.run([sys.executable, str(ROOT / "run_scoring_v20.py")],
                          cwd=str(ROOT), capture_output=True, text=True, timeout=300)
    print("  scoring engine output:")
    for line in proc.stdout.splitlines()[-25:]: print(f"    {line}")
    if proc.returncode != 0:
        print("  STDERR:")
        for line in proc.stderr.splitlines()[-15:]: print(f"    {line}")
        raise RuntimeError(f"Scoring failed with exit {proc.returncode}")
    # Move output to v2.0.1_scored
    if SCORED.exists(): shutil.rmtree(SCORED)
    expected_out.rename(SCORED)
    print(f"  scored output -> {SCORED.name}/")
finally:
    # Cleanup symlinks
    if expected_in.is_symlink(): expected_in.unlink()
    if expected_out.exists() and expected_out.is_symlink():
        expected_out.unlink()
    # Restore originals
    if saved_in and saved_in.exists():
        saved_in.rename(expected_in)
    if saved_out and saved_out.exists():
        saved_out.rename(expected_out)

# === STEP 5: verify calibration ==========================================
print()
print("="*72)
print("STEP 5: Verifying INT-0001 Leucovorin calibration ≥ 80")
print("="*72)
with open(SCORED / "interventions.csv", newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        if r["id"] == "INT-0001":
            score = float(r.get("csrs_score", "0") or "0")
            status = "PASS ✅" if score >= 80 else "FAIL ❌"
            print(f"  INT-0001 csrs_score: {score} ({status})")
            assert score >= 80, f"Calibration FAILED: INT-0001 = {score} < 80"
            break

# Also print top 10 + delta from old
print()
print("  Top 10 interventions in v2.0.1_scored vs old v2.0_scored:")
old_scores = {r["id"]: float(r.get("csrs_score","0") or "0")
              for r in csv.DictReader(open(SRC/"interventions.csv"))}
new = list(csv.DictReader(open(SCORED/"interventions.csv")))
new.sort(key=lambda r: -float(r.get("csrs_score","0") or "0"))
print(f"  {'rank':<5} {'ID':<10} {'name':<50} {'new':>7} {'old':>7} {'Δ':>7}")
for i, r in enumerate(new[:10], 1):
    nm = r["name"][:48]
    new_s = float(r.get("csrs_score","0") or "0")
    old_s = old_scores.get(r["id"], 0)
    delta = new_s - old_s
    print(f"  {i:<5} {r['id']:<10} {nm:<50} {new_s:>7.2f} {old_s:>7.2f} {delta:>+7.2f}")

# === STEP 6: rebuild vault ==============================================
print()
print("="*72)
print("STEP 6: Rebuilding the vault from v2.0.1_scored/")
print("="*72)
# Save old v2.0_scored, swap in v2.0.1_scored as the canonical
backup = ROOT / "v2.0_scored.before_v201"
if backup.exists(): shutil.rmtree(backup)
shutil.copytree(SRC, backup)
print(f"  backup: v2.0_scored/ -> {backup.name}/")
# Promote scored tables into v2.0_scored/ WITHOUT wholesale-replacing the directory.
# The scoring engine writes a subset of tables (hypotheses, mechanisms, interventions,
# combinations, phenotypes, sources, evidence_*, edges, genes, etc.). Side tables that
# the engine doesn't score — biomarkers.csv, tests_catalog.csv, billing_codes.csv,
# field_outcomes.csv (CLAUDE.md firewalled), intervention_formulations*.csv,
# iatrogenic_exposure_priors.csv, baseline_phenotype_prevalence.csv,
# pgx_drug_gene_table.csv, physiological_state_normalization_table.csv,
# protocols.csv, rare_syndrome_screening_gate.csv, genes_phase0_additions.csv,
# genetic_id_aliases.csv, calibration.txt — must be preserved across the promotion.
# Prior implementation was `rmtree(SRC); copytree(SCORED, SRC)` which destroyed ~20
# canonical tables every promotion.
for child in SCORED.iterdir():
    dst = SRC / child.name
    if child.is_dir():
        if dst.exists(): shutil.rmtree(dst)
        shutil.copytree(child, dst)
    else:
        shutil.copy2(child, dst)
print(f"  v2.0.1_scored/ -> v2.0_scored/ (scored tables promoted; side tables preserved)")

proc = subprocess.run([sys.executable, str(ROOT / "build_vault.py")],
                      cwd=str(ROOT), capture_output=True, text=True, timeout=120)
for line in proc.stdout.splitlines()[-15:]: print(f"  {line}")
if proc.returncode != 0:
    for line in proc.stderr.splitlines()[-10:]: print(f"  STDERR: {line}")
    raise RuntimeError("Vault rebuild failed")

# === STEP 7: Δ² prioritization overlay ==================================
# Δ² (second-derivative / inflection-point) overlay measures TRAJECTORY of
# evidence accumulation per entity, not truth. Runs ON TOP of CSRS.
# Calibration anchors mirror CSRS's INT-0001 ≥ 80 discipline; if any anchor
# fails, the engine exits non-zero and halts the pipeline. See
# scripts/compute_delta_squared.py and delta_squared_v1/calibration_status.txt.
print()
print("="*72)
print("STEP 7: Δ² prioritization overlay")
print("="*72)
proc = subprocess.run(
    [sys.executable, str(ROOT / "scripts" / "compute_delta_squared.py")],
    cwd=str(ROOT), capture_output=True, text=True, timeout=60)
for line in proc.stdout.splitlines(): print(f"  {line}")
if proc.returncode != 0:
    for line in proc.stderr.splitlines()[-15:]: print(f"  STDERR: {line}")
    raise RuntimeError(
        f"Δ² engine failed (exit {proc.returncode}); calibration regression — pipeline halted")

print()
print("="*72)
print("DONE.")
print("="*72)
print(f"  v2.0.1_expanded/  = inputs (v2.0_scored + merged proposal)")
print(f"  v2.0.1_scored/    = scored output (preserved)")
print(f"  v2.0_scored/      = canonical state (now updated to v2.0.1)")
print(f"  v2.0_scored.before_v201/  = backup of pre-merge state")
print(f"  vault/            = rebuilt from new canonical")
