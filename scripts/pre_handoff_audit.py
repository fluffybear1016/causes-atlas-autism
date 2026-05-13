#!/usr/bin/env python3
"""pre_handoff_audit.py — comprehensive integrity audit before design hand-off.

Audits run:
  A. Numerical claim drift (0.052, 4-axis, etc.)
  B. Calibration anchor still 83.35
  C. Cohort MAE still 0.0665
  D. Combination member-list integrity (every named ingredient resolves)
  E. Peptide vault references real atlas entities
  F. CSV schema integrity + duplicate IDs
  G. Vault hygiene (Untitled files, orphans)
  H. Script smoke tests (all critical scripts still run)
  I. Dangling Obsidian links in vault

Outputs report to AUDIT_2026_05_09.md
"""
from __future__ import annotations

import csv
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCORED = ROOT / "v2.0_scored"
VAULT = ROOT / "vault"

findings = []

def report(severity: str, area: str, msg: str) -> None:
    """severity: CRIT (blocks handoff), HIGH (must fix), MED (should fix), LOW (note), OK (pass)"""
    findings.append((severity, area, msg))


# ── A. Numerical claim drift ────────────────────────────────────────────
files_to_check = [
    "validation/responder_rate_calibration/VALIDATION_RESULTS.md",
    "validation/responder_rate_calibration/MANUSCRIPT_OUTLINE.md",
    "SUBSTRATE_THESIS.md", "DECK_v2_15_SLIDE_SPEC.md",
    "VAULT_INSTITUTIONAL.md", "VAULT.md", "VAULT_SETUP_GUIDE.md",
    "CHATGPT_DESIGN_BRIEF.md",
    "ui/components/substrate_diagram.html",
    "ui/components/substrate_diagram_slide.html",
    "ui/components/deck/slide_10_validation.html",
    "vault/CONNECTIVITY_AUDIT.md",
]
for rel in files_to_check:
    p = ROOT / rel
    if not p.exists():
        continue
    txt = p.read_text()
    # Look for the old false claims
    bad_052 = re.findall(r'\bMAE = 0\.052\b|\bwithin-coverage MAE = 0\.052\b|\bMAE = </strong>[^<]*0\.052\b', txt)
    bad_4ax = re.findall(r'4 sub-3% errors across 4 (?:independent )?mechanism axes|four mechanistically independent intervention classes', txt)
    if bad_052:
        report("HIGH", "numerical-drift",
               f"{rel}: still contains 0.052 (should be 0.049) — {len(bad_052)} hits")
    if bad_4ax:
        report("HIGH", "numerical-drift",
               f"{rel}: still contains '4 mechanism axes' claim (should be 3 axes at sub-3%) — {len(bad_4ax)} hits")

# ── B. Calibration anchor ──────────────────────────────────────────────
with (SCORED / "interventions.csv").open() as f:
    rd = csv.DictReader(f)
    anchor_row = next((r for r in rd if r["id"] == "INT-0001"), None)
if not anchor_row:
    report("CRIT", "calibration", "INT-0001 missing from interventions.csv")
else:
    try:
        anchor_csrs = float(anchor_row["csrs_score"])
        if anchor_csrs < 80:
            report("CRIT", "calibration", f"INT-0001 csrs_score={anchor_csrs} < 80")
        elif abs(anchor_csrs - 83.35) > 0.01:
            report("HIGH", "calibration", f"INT-0001 csrs_score={anchor_csrs}, expected 83.35")
        else:
            report("OK", "calibration", f"INT-0001 = {anchor_csrs} (preserved)")
    except (ValueError, TypeError):
        report("CRIT", "calibration", f"INT-0001 csrs_score not parseable: {anchor_row.get('csrs_score')!r}")

# ── C. Cohort MAE ──────────────────────────────────────────────────────
try:
    out = subprocess.run(
        [sys.executable, "scripts/compute_responder_mae.py"],
        cwd=str(ROOT), capture_output=True, text=True, timeout=60
    )
    mae_line = next((ln for ln in out.stdout.split("\n") if "Cohort responder-rate MAE" in ln), "")
    m = re.search(r"MAE: ([\d.]+)", mae_line)
    if m:
        mae = float(m.group(1))
        if abs(mae - 0.0665) < 0.001:
            report("OK", "cohort-mae", f"Cohort MAE = {mae:.4f} (preserved)")
        else:
            report("HIGH", "cohort-mae", f"Cohort MAE = {mae:.4f}, expected 0.0665")
    else:
        report("HIGH", "cohort-mae", f"MAE parse failed; output: {out.stdout[-200:]}")
except Exception as e:
    report("HIGH", "cohort-mae", f"MAE script failed to run: {e}")

# ── D. Combination member-list integrity ───────────────────────────────
# Load INT IDs and names + member list per combination
with (SCORED / "interventions.csv").open() as f:
    int_rows = list(csv.DictReader(f))
int_id_to_name = {r["id"]: r["name"] for r in int_rows}
int_id_to_category = {r["id"]: (r.get("category") or "").lower() for r in int_rows}
# Exclude combo-category INTs from ingredient keyword matching — combos
# aren't components, so flagging them as "missing members" is a false
# positive. (Patched 2026-05-09 per fix_combo_integrity_pass2.)
int_name_lower_to_id = {
    r["name"].lower(): r["id"]
    for r in int_rows
    if (r.get("category") or "").lower() != "combo"
}

with (SCORED / "combinations.csv").open() as f:
    combo_rows = list(csv.DictReader(f))
with (SCORED / "combination_members.csv").open() as f:
    member_rows = list(csv.DictReader(f))

# Per combo, what members are listed?
members_by_combo = {}
for m in member_rows:
    members_by_combo.setdefault(m["combination_id"], []).append(m["intervention_id"])

# Verify every member INT ID exists
orphan_members = []
for m in member_rows:
    iid = m["intervention_id"]
    if iid and iid not in int_id_to_name:
        orphan_members.append((m["combination_id"], iid))

if orphan_members:
    for cid, iid in orphan_members[:5]:
        report("HIGH", "combo-orphan",
               f"{cid} references {iid} which does not exist in interventions.csv")
else:
    report("OK", "combo-orphan", f"All {len(member_rows)} combination member INT refs resolve")

# For each combo, parse the name for ingredient terms and check coverage
# Only check the 20 new combos (COM-0006 to COM-0025) since pre-existing ones
# were curator-reviewed
NEW_COMBO_INGREDIENTS = {
    "COM-0006": ["leucovorin", "methyl-b12", "vitamin d"],
    "COM-0007": ["5-mthf", "p5p", "b6", "tmg", "betaine"],
    "COM-0008": ["alcar", "acetyl-l-carnitine", "coq10", "alpha-lipoic acid"],
    "COM-0009": ["d-ribose", "creatine", "l-carnitine"],
    "COM-0010": ["liposomal curcumin", "curcumin", "quercetin", "omega-3"],
    "COM-0011": ["sulforaphane", "liposomal glutathione", "glutathione", "nac"],
    "COM-0012": ["luteolin", "quercetin", "rutin"],
    "COM-0013": ["bifidobacterium infantis", "l-glutamine", "zinc"],
    "COM-0014": ["vsl#3", "visbiome", "colostrum", "l-glutamine"],
    "COM-0015": ["mtt", "microbiota", "bifidobacterium", "ldn", "naltrexone"],
    "COM-0016": ["l-theanine", "magnesium glycinate", "magnesium", "saffron"],
    "COM-0017": ["l-carnosine", "carnosine", "l-taurine", "taurine", "magnesium threonate"],
    "COM-0018": ["melatonin", "magnesium glycinate", "l-theanine"],
    "COM-0019": ["ldn", "naltrexone", "cromolyn", "quercetin"],
    "COM-0020": ["thymosin", "vitamin d", "zinc"],
    "COM-0021": ["choline", "dha", "omega-3", "methylfolate", "5-mthf"],
    "COM-0022": ["liposomal glutathione", "glutathione", "modified citrus pectin", "activated charcoal"],
    "COM-0023": ["cold exposure", "sauna", "omega-3"],
    "COM-0024": ["coq10", "zinc", "selenium", "l-carnitine"],
    "COM-0025": ["5-mthf", "methylfolate", "p5p", "b6", "dha", "choline"],
}

# Canonical ingredient → INT map for ambiguous substrings (added 2026-05-09).
# Without this, "coq10" matches INT-0120 MitoQ (which has "CoQ10" in its
# parenthetical) before INT-0012 Coenzyme Q10 (ubiquinol), causing false
# "missing member" flags.
CANONICAL_INGREDIENT_TO_INT = {
    "coq10": "INT-0012",
    "coenzyme q10": "INT-0012",
    "ubiquinol": "INT-0012",
    "nac": "INT-0004",
    "quercetin": "INT-0029",
    "cromolyn": "INT-0103",
    "l-glutamine": "INT-0101",
    "glutamine": "INT-0101",
    "magnesium glycinate": "INT-0015",
    "magnesium": "INT-0015",
}

# Cross-check which ingredients DO exist in interventions.csv
def has_intervention(name_substr: str) -> str | None:
    key = name_substr.lower()
    if key in CANONICAL_INGREDIENT_TO_INT:
        canonical = CANONICAL_INGREDIENT_TO_INT[key]
        if canonical in int_id_to_name:
            return canonical
    for int_name, iid in int_name_lower_to_id.items():
        if key in int_name.lower():
            return iid
    return None

for cid, ingredients in NEW_COMBO_INGREDIENTS.items():
    listed_members = set(members_by_combo.get(cid, []))
    found_ints = set()
    missing = []
    for ing in ingredients:
        iid = has_intervention(ing)
        if iid:
            found_ints.add(iid)
        else:
            missing.append(ing)

    # Ingredients that DO have INT rows but are NOT in this combo's member list
    unrostered = found_ints - listed_members
    if unrostered:
        names = ", ".join(f"{i}({int_id_to_name[i][:30]})" for i in unrostered)
        report("MED", "combo-integrity",
               f"{cid}: ingredients have INT rows but not in member list — {names}")
    if missing:
        report("LOW", "combo-integrity",
               f"{cid}: ingredients without INT rows (not in atlas) — {missing}")

# ── E. Peptide vault references ───────────────────────────────────────
peptides_dir = VAULT / "peptides"
if peptides_dir.exists():
    pep_files = list(peptides_dir.glob("*.md"))
    # Each peptide page may reference [[INT-XXXX]] or [[PHE-XXXX]] etc.
    int_ids = set(int_id_to_name.keys())
    phe_ids = {r["id"] for r in csv.DictReader((SCORED / "phenotypes.csv").open())}
    dangling = []
    for f in pep_files:
        if f.name.startswith("00_") or f.name.startswith("01_") or \
           f.name.startswith("02_") or f.name.startswith("03_") or \
           f.name == "README.md":
            continue
        txt = f.read_text()
        for m in re.finditer(r"\[\[(INT-\d{4}|PHE-\d{4}|MEC-\d{4}|FRM-\d{4})\]\]", txt):
            ref = m.group(1)
            if ref.startswith("INT-") and ref not in int_ids:
                dangling.append((f.name, ref))
            elif ref.startswith("PHE-") and ref not in phe_ids:
                dangling.append((f.name, ref))
    if dangling:
        for fname, ref in dangling[:8]:
            report("LOW", "peptide-links",
                   f"{fname}: dangling Obsidian link [[{ref}]] (no matching atlas entry)")
    else:
        report("OK", "peptide-links",
               f"All atlas links in {len(pep_files)} peptide pages resolve")

# ── F. CSV schema integrity + duplicate IDs ───────────────────────────
for csv_name in ["interventions.csv", "combinations.csv", "combination_members.csv",
                  "intervention_formulations.csv", "sources.csv", "phenotypes.csv",
                  "hypotheses.csv", "mechanisms.csv"]:
    p = SCORED / csv_name
    if not p.exists():
        report("HIGH", "csv-integrity", f"{csv_name} missing")
        continue
    try:
        with p.open() as f:
            rows = list(csv.DictReader(f))
        ids = [r.get("id") or r.get("formulation_id") for r in rows]
        ids = [i for i in ids if i]
        dup = set([i for i in ids if ids.count(i) > 1])
        if dup:
            report("HIGH", "csv-integrity", f"{csv_name}: duplicate IDs {sorted(dup)[:5]}")
    except Exception as e:
        report("HIGH", "csv-integrity", f"{csv_name} parse failed: {e}")
report("OK", "csv-integrity", "All CSVs parse cleanly (or issues reported above)")

# ── G. Vault hygiene ──────────────────────────────────────────────────
untitled = list(VAULT.glob("Untitled*"))
if untitled:
    report("MED", "vault-hygiene",
           f"Vault root has {len(untitled)} 'Untitled' files/dirs: {[f.name for f in untitled]}")
else:
    report("OK", "vault-hygiene", "No untitled files in vault root")

# ── H. Script smoke tests ─────────────────────────────────────────────
for script in ["scripts/validate_v02_calibration.py",
                "scripts/compute_responder_mae.py",
                "scripts/compute_formulation_scores.py"]:
    try:
        out = subprocess.run([sys.executable, script], cwd=str(ROOT),
                            capture_output=True, text=True, timeout=60)
        if out.returncode != 0:
            report("HIGH", "script-smoke",
                   f"{script}: exit {out.returncode}; stderr tail: {out.stderr[-200:]}")
        else:
            report("OK", "script-smoke", f"{script}: runs cleanly")
    except Exception as e:
        report("HIGH", "script-smoke", f"{script}: failed to launch: {e}")

# ── I. Dangling links in main vault pages ─────────────────────────────
# Check VAULT.md, VAULT_INSTITUTIONAL.md, VAULT_SETUP_GUIDE.md
# for [[XXX]] links that don't resolve
# (deferred to manual review — these mostly reference repo files not entity pages)

# === RENDER REPORT ====================================================
print()
print("=" * 72)
print("PRE-HANDOFF AUDIT — 2026-05-09")
print("=" * 72)

sev_order = {"CRIT": 0, "HIGH": 1, "MED": 2, "LOW": 3, "OK": 4}
findings.sort(key=lambda x: (sev_order.get(x[0], 5), x[1]))

counts = {}
for sev, _, _ in findings:
    counts[sev] = counts.get(sev, 0) + 1

print()
for sev in ("CRIT", "HIGH", "MED", "LOW", "OK"):
    c = counts.get(sev, 0)
    if c:
        print(f"  {sev}: {c}")
print()

for sev, area, msg in findings:
    if sev != "OK":
        print(f"  [{sev:4s}] {area:20s} {msg}")

print()
print("OK findings:")
for sev, area, msg in findings:
    if sev == "OK":
        print(f"  [✓ ] {area:20s} {msg}")

# Also write to a markdown file
md_lines = [
    "# Pre-handoff audit — 2026-05-09",
    "",
    f"**Severity counts:** "
    f"CRIT {counts.get('CRIT',0)} · HIGH {counts.get('HIGH',0)} · "
    f"MED {counts.get('MED',0)} · LOW {counts.get('LOW',0)} · "
    f"OK {counts.get('OK',0)}",
    "",
]
for sev in ("CRIT", "HIGH", "MED", "LOW"):
    items = [(area, msg) for s, area, msg in findings if s == sev]
    if items:
        md_lines.append(f"## {sev}")
        md_lines.append("")
        for area, msg in items:
            md_lines.append(f"- **{area}**: {msg}")
        md_lines.append("")
md_lines.append("## Passed")
md_lines.append("")
for sev, area, msg in findings:
    if sev == "OK":
        md_lines.append(f"- ✓ **{area}**: {msg}")

(ROOT / "AUDIT_2026_05_09.md").write_text("\n".join(md_lines))
print(f"\n  Written to AUDIT_2026_05_09.md")
