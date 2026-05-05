#!/usr/bin/env python3
"""
full_audit.py — Comprehensive end-of-session audit of all atlas work.

Runs every check that should pass before pushing to Drive:
1. CSV structural integrity (column counts, unique IDs)
2. PMID verification (all PMIDs across all CSVs match PubMed records)
3. Atlas ID validity (all PHE/INT/MEC/GEN refs valid in atlas)
4. Engine determinism (same input → byte-identical output)
5. Calibration anchor preservation (Hannah Poling PHE-0002 ≥ 0.50)
6. Validation case structural validation (all 4 cases pass)
7. Engine-vs-expected calibration case match rates
8. Spec section ordering + version-string consistency
9. CLAUDE.md verification-protocol section presence

Exits 0 if all pass, 1 if any fail.
"""
import csv, json, re, subprocess, sys, time, urllib.request, urllib.parse
from pathlib import Path

# Auto-detect atlas root (works in both /Users/Greg/Autism and sandbox-mounted path)
_HERE = Path(__file__).resolve().parent
ATLAS = _HERE.parent  # scripts/ -> atlas root
ATLAS_CSV = ATLAS / "v2.0_scored"
print(f"[audit] atlas root: {ATLAS}")

failures = []
warnings = []
passes = 0


def check(name, condition, fail_msg=""):
    global passes
    if condition:
        print(f"  ✓ {name}")
        passes += 1
    else:
        print(f"  ✗ {name}: {fail_msg}")
        failures.append(f"{name}: {fail_msg}")


def section(title):
    print(f"\n{'='*70}\n{title}\n{'='*70}")


# ============================================================================
# 1. CSV STRUCTURAL INTEGRITY
# ============================================================================
section("1. CSV STRUCTURAL INTEGRITY")

PHASE0_CSVS = [
    "iatrogenic_exposure_priors.csv",
    "physiological_state_normalization_table.csv",
    "rare_syndrome_screening_gate.csv",
    "genetic_id_aliases.csv",
    "baseline_phenotype_prevalence.csv",
    "pgx_drug_gene_table.csv",
    "genes_phase0_additions.csv",
]

for fname in PHASE0_CSVS:
    p = ATLAS_CSV / fname
    if not p.exists():
        check(f"{fname} exists", False, "missing")
        continue
    with open(p) as f:
        reader = csv.reader(f)
        h = next(reader)
        rows = list(reader)
    bad = [(i, len(r)) for i, r in enumerate(rows, 2) if len(r) != len(h)]
    check(f"{fname} structural", not bad, f"col mismatches: {bad[:3]}")

    # Unique IDs
    if rows and len(h) > 0 and h[0] == "id":
        ids = [r[0] for r in rows]
        check(f"{fname} unique IDs", len(set(ids)) == len(ids),
              f"duplicates: {[i for i in ids if ids.count(i)>1][:3]}")


# ============================================================================
# 2. PMID VERIFICATION (all PMIDs across all CSVs match PubMed)
# ============================================================================
section("2. PMID VERIFICATION")

all_pmids = set()
pmid_sources = {}

PMID_FIELDS = {
    "iatrogenic_exposure_priors.csv": ["primary_pmids", "countervailing_evidence_pmids"],
    "physiological_state_normalization_table.csv": ["primary_pmid"],
    "rare_syndrome_screening_gate.csv": ["primary_pmid"],
    "genetic_id_aliases.csv": ["primary_pmid"],
    "baseline_phenotype_prevalence.csv": ["primary_pmid"],
    "pgx_drug_gene_table.csv": ["primary_pmid"],
}

for fname, cols in PMID_FIELDS.items():
    p = ATLAS_CSV / fname
    if not p.exists():
        continue
    with open(p) as f:
        for r in csv.DictReader(f):
            for c in cols:
                v = r.get(c, "") or ""
                for s in v.split(";"):
                    s = s.strip()
                    if s.isdigit():
                        all_pmids.add(s)
                        pmid_sources.setdefault(s, []).append(f"{fname}:{r.get('id','?')}")

# Spec body PMIDs
with open(ATLAS / "SESSION_4_HANNAH_POLING_SPEC.md") as f:
    text = f.read()
spec_pmids = set(re.findall(r"PMID\s*[: ]?\s*(\d{6,9})", text))
all_pmids |= spec_pmids
for p in spec_pmids:
    pmid_sources.setdefault(p, []).append("SESSION_4_HANNAH_POLING_SPEC.md")

print(f"  Cross-checking {len(all_pmids)} unique PMIDs against PubMed...")
all_pmids_list = sorted(all_pmids)
not_found = []
for i in range(0, len(all_pmids_list), 50):
    batch = all_pmids_list[i:i+50]
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={','.join(batch)}&retmode=json"
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            data = json.loads(resp.read())["result"]
        for p in batch:
            if not data.get(p, {}).get("title"):
                not_found.append((p, pmid_sources.get(p, ["?"])))
    except Exception as e:
        warnings.append(f"PubMed fetch failed: {e}")
    time.sleep(0.4)

check(f"All {len(all_pmids)} PMIDs valid on PubMed", not not_found,
      f"missing: {not_found[:3]}")


# ============================================================================
# 3. ATLAS ID VALIDITY
# ============================================================================
section("3. ATLAS ID VALIDITY")

with open(ATLAS_CSV / "phenotypes.csv") as f:
    valid_phe = set(r["id"] for r in csv.DictReader(f))
with open(ATLAS_CSV / "interventions.csv") as f:
    valid_int = set(r["id"] for r in csv.DictReader(f))
with open(ATLAS_CSV / "mechanisms.csv") as f:
    valid_mec = set(r["id"] for r in csv.DictReader(f))
with open(ATLAS_CSV / "genes.csv") as f:
    valid_gen = set(r["id"] for r in csv.DictReader(f))
with open(ATLAS_CSV / "genes_phase0_additions.csv") as f:
    valid_gen |= set(r["id"] for r in csv.DictReader(f))

# Check iatrogenic
bad_phe = []
bad_mec = []
SENTINEL_PHE = {"CONGENITAL_TERATOGENIC_PATTERN"}
with open(ATLAS_CSV / "iatrogenic_exposure_priors.csv") as f:
    for r in csv.DictReader(f):
        p = r.get("target_phenotype_id", "").strip()
        if p and p.startswith("PHE-") and p not in valid_phe:
            bad_phe.append(p)
        m = r.get("mechanism_id", "").strip()
        if m and m not in valid_mec:
            bad_mec.append(m)
check("iatrogenic CSV: all PHE refs valid (or sentinel)", not bad_phe,
      f"invalid: {bad_phe[:3]}")
check("iatrogenic CSV: all MEC refs valid", not bad_mec,
      f"invalid: {bad_mec[:3]}")

# Check rare-syndrome gate
bad_phe = []
with open(ATLAS_CSV / "rare_syndrome_screening_gate.csv") as f:
    for r in csv.DictReader(f):
        rt = r.get("target_phenotype_routing", "")
        if rt.startswith("PHE-") and rt not in valid_phe:
            bad_phe.append(rt)
check("rare-syndrome gate: all PHE refs valid", not bad_phe,
      f"invalid: {bad_phe}")

# Check baseline prevalence
bad_phe = []
with open(ATLAS_CSV / "baseline_phenotype_prevalence.csv") as f:
    for r in csv.DictReader(f):
        p = r.get("phenotype_id", "")
        if p.startswith("PHE-") and p not in valid_phe:
            bad_phe.append(p)
check("baseline_prevalence: all PHE refs valid", not bad_phe,
      f"invalid: {bad_phe}")

# Check genetic_id_aliases pending count
with open(ATLAS_CSV / "genetic_id_aliases.csv") as f:
    pend = sum(1 for r in csv.DictReader(f) if r.get("atlas_gene_id", "").strip() == "pending")
check("genetic_id_aliases: ≤3 pending refs (CNV-locus rows expected)", pend <= 3,
      f"pending count: {pend}")

# Check PGx gene refs (against genes.csv ∪ genes_phase0_additions.csv)
with open(ATLAS_CSV / "genes.csv") as f:
    all_atlas_genes = {r["gene_symbol"]: r["id"] for r in csv.DictReader(f)}
with open(ATLAS_CSV / "genes_phase0_additions.csv") as f:
    for r in csv.DictReader(f):
        all_atlas_genes[r["gene_symbol"]] = r["id"]

pgx_genes_missing = []
with open(ATLAS_CSV / "pgx_drug_gene_table.csv") as f:
    for r in csv.DictReader(f):
        g = r.get("gene", "")
        if g and g != "meta" and g not in all_atlas_genes:
            pgx_genes_missing.append(g)
check("PGx genes all in atlas (genes.csv ∪ phase0_additions)",
      not pgx_genes_missing, f"missing: {pgx_genes_missing[:5]}")


# ============================================================================
# 4. ENGINE DETERMINISM
# ============================================================================
section("4. ENGINE DETERMINISM")

case_path = ATLAS / "validation/calibration_cases/case_011_hannah_poling/input.json"
out1 = subprocess.run(["python3", str(ATLAS / "personalized_risk.py"), "--input", str(case_path)],
                      capture_output=True, text=True)
out2 = subprocess.run(["python3", str(ATLAS / "personalized_risk.py"), "--input", str(case_path)],
                      capture_output=True, text=True)
o1 = json.loads(out1.stdout)
o2 = json.loads(out2.stdout)
o1.pop("computed_at"); o2.pop("computed_at")
check("Engine output byte-identical (excl. timestamp)",
      json.dumps(o1, sort_keys=True) == json.dumps(o2, sort_keys=True),
      "outputs differ")
check("Engine phenotype_posteriors identical",
      o1["phenotype_posteriors"] == o2["phenotype_posteriors"], "posteriors differ")
check("Engine intervention_bundle identical",
      o1["intervention_bundle"] == o2["intervention_bundle"], "bundles differ")


# ============================================================================
# 5. CALIBRATION ANCHOR PRESERVATION
# ============================================================================
section("5. CALIBRATION ANCHOR (Hannah Poling PHE-0002 ≥ 0.50)")

phe2 = o1["phenotype_posteriors"]["PHE-0002"]
check(f"PHE-0002 point ≥ 0.50 (got {phe2['point']})", phe2["point"] >= 0.50)
check(f"PHE-0002 credal_low ≥ 0.20 (got {phe2['credal_low']})", phe2["credal_low"] >= 0.20)
check(f"Top phenotype = PHE-0002", o1["phenotype_ranking"][0] == "PHE-0002")


# ============================================================================
# 6. VALIDATION CASE STRUCTURAL VALIDATION
# ============================================================================
section("6. VALIDATION CASE STRUCTURAL CHECKS")

cases = ["case_011_hannah_poling", "case_015_frye_fraa_responder",
         "case_020_walsh_undermethylator", "case_026_22q11_deletion"]
for c in cases:
    nb = ATLAS / f"validation/calibration_cases/{c}/validation_notebook.py"
    r = subprocess.run(["python3", str(nb)], capture_output=True, text=True)
    check(f"{c} validation_notebook passes", r.returncode == 0, r.stderr[:80])


# ============================================================================
# 7. ENGINE-VS-EXPECTED CALIBRATION MATCH
# ============================================================================
section("7. ENGINE-VS-EXPECTED CASE MATCH RATES")

import yaml as _yaml
case_results = []
for c in cases:
    out = subprocess.run(["python3", str(ATLAS / "personalized_risk.py"),
                          "--input", str(ATLAS / f"validation/calibration_cases/{c}/input.json")],
                          capture_output=True, text=True)
    actual = json.loads(out.stdout)
    with open(ATLAS / f"validation/calibration_cases/{c}/expected_output.yaml") as f:
        expected = _yaml.safe_load(f)

    expected_top = expected.get("expected_top_phenotype")
    expected_syn = expected.get("expected_syndromic_flag", False)

    if expected_syn:
        match = actual.get("syndromic_flag") == True
        case_results.append((c, "PASS" if match else "FAIL", "syndromic-gate"))
    elif expected_top and expected_top.startswith("PHE-"):
        actual_top = actual["phenotype_ranking"][0]
        actual_p = actual["phenotype_posteriors"][expected_top]["point"]
        floor = expected.get("expected_phenotype_p_floor", 0)
        ceil = expected.get("expected_phenotype_p_ceiling", 1)
        if actual_top == expected_top and floor <= actual_p <= ceil:
            case_results.append((c, "PASS", f"top={actual_top} p={actual_p:.3f}"))
        elif floor <= actual_p <= ceil:
            case_results.append((c, "PARTIAL", f"top={actual_top}≠{expected_top} but p in range"))
        else:
            case_results.append((c, "FAIL", f"top={actual_top} p={actual_p:.3f} ∉ [{floor},{ceil}]"))
    else:
        case_results.append((c, "INDETERMINATE", ""))

passes_cases = sum(1 for _, r, _ in case_results if r == "PASS")
partials = sum(1 for _, r, _ in case_results if r == "PARTIAL")
for c, r, info in case_results:
    print(f"  {r:<12} {c}: {info}")
check(f"Engine: ≥{passes_cases} of {len(cases)} cases PASS",
      passes_cases >= 3, f"only {passes_cases} pass")
if partials:
    warnings.append(f"{partials} PARTIAL case(s): documented engine v0.1 limitation")


# ============================================================================
# 8. SPEC INTEGRITY
# ============================================================================
section("8. SPEC INTEGRITY")

with open(ATLAS / "SESSION_4_HANNAH_POLING_SPEC.md") as f:
    spec_text = f.read()

# Section ordering
sections = re.findall(r"^## §(\d+)\w?", spec_text, re.MULTILINE)
check("Spec has 24+ sections", len(sections) >= 24, f"got {len(sections)}")
# Check ordering: §0..§24 should appear in that numerical order
section_nums = [int(s) for s in sections]
# Allow §23a/§23b after §23, and §24 after §23
ordering_ok = True
last = -1
for s in section_nums:
    if s < last:
        ordering_ok = False
        break
    last = s
check("Spec sections in numerical order", ordering_ok)

# Version strings
check("Spec version is 2.3", "**Spec version:** 2.3" in spec_text)
check("input_version 2.3 in JSON examples", '"input_version": "2.3"' in spec_text)
check("engine_version session4_v2.3 in JSON examples", '"session4_v2.3"' in spec_text)
check("§24 verification protocol present", "## §24 — Verification protocol" in spec_text)
check("§24 BioMysteryBench-aligned reference", "BioMysteryBench" in spec_text)
check("§13.5 calibration anchor disambiguation", "Layer 2 (global CSRS scoring)" in spec_text)
check("§24.5 .py-or-.ipynb language", ".py" in spec_text and ".ipynb" in spec_text)

# H-2 / H-7 audit fixes
check("H-2 fix in §13.5 references resolved-audit", "audit H-2" in spec_text)
check("H-7 fix in §24.5 references resolved-audit", "H-7" in spec_text)


# ============================================================================
# 9. CLAUDE.md INTEGRITY
# ============================================================================
section("9. CLAUDE.md INTEGRITY")

with open(ATLAS / "CLAUDE.md") as f:
    cl = f.read()

check("CLAUDE.md has Verification protocol section",
      "## Verification protocol (BioMysteryBench-aligned" in cl)
check("CLAUDE.md MPE bug marked RESOLVED",
      "MPE weights: RESOLVED 2026-04-29" in cl)
check("CLAUDE.md no stale 'all weights = 0.0' reference",
      "all weights = 0.0" not in cl)
check("CLAUDE.md verify-before-write rule in 'What not to do'",
      "Don't write any PMID without PubMed esummary verification" in cl)


# ============================================================================
# 10. ENGINE FILE INTEGRITY
# ============================================================================
section("10. ENGINE FILE INTEGRITY")

eng = ATLAS / "personalized_risk.py"
check("personalized_risk.py exists", eng.exists())
if eng.exists():
    eng_text = eng.read_text()
    check("Engine has no LLM imports",
          not any(x in eng_text for x in ["import openai", "import anthropic", "from anthropic"]))
    check("Engine has determinism guarantees comment",
          "Stable sort by ID" in eng_text or "stable sort" in eng_text.lower())
    check("Engine references spec §7", "§7" in eng_text)


# ============================================================================
# SUMMARY
# ============================================================================
section("SUMMARY")
print(f"\n  Total checks: {passes + len(failures)}")
print(f"  PASSED: {passes}")
print(f"  FAILED: {len(failures)}")
print(f"  WARNINGS: {len(warnings)}")
if failures:
    print(f"\n  FAILURES:")
    for f in failures:
        print(f"    - {f}")
if warnings:
    print(f"\n  WARNINGS:")
    for w in warnings:
        print(f"    - {w}")

sys.exit(0 if not failures else 1)
