#!/usr/bin/env python3
"""
Session 2: gene-layer completion + hypothesis-hypothesis mechanism overlap.

Per CLAUDE.md (Session 2 priority order):
  1. SFARI Tier 3 cross-walk (177 genes) with polarity=unknown
  2. No-SFARI cross-walk (295 OpenTargets-only) with polarity=unknown
  3. Un-wired SFARI Syndromic genes (those without specific phenotype/mech
     linkage already) — wire to HYP-0028 with polarity=unknown
  4. Hypothesis-hypothesis mechanism-overlap candidate proposal
     (every hyp-pair sharing ≥2 mechanisms gets a proposed edge)

The engine's polarity_unknown multiplier (0.85) provides appropriate
down-weighting vs. supporting (1.00) for the curated Tier 1+2 set.
"""
import csv, datetime as dt
from collections import defaultdict
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC_DIR = ROOT / "v2.0_scored"
EXP_DIR = ROOT / "v2.0.1_expanded"
PROP_DIR = ROOT / "v2.0.1_proposed"
NOW = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")

genes = list(csv.DictReader(open(SRC_DIR / "genes.csv")))
existing_ghe = list(csv.DictReader(open(SRC_DIR / "gene_hypothesis_edges.csv")))
ghe_pairs = {(r["gene_id"], r["hypothesis_id"]) for r in existing_ghe}

# Categorize remaining genes
tier3 = [g for g in genes if g["sfari_score"] == "3"]
no_sfari = [g for g in genes if not (g["sfari_score"] or "").strip()
            or g["sfari_score"] == "Not in SFARI"]
syndromic = [g for g in genes if g["sfari_score"] == "S"]

# For syndromic, identify which are already linked (specifically) to phenotypes
gpe = list(csv.DictReader(open(SRC_DIR / "gene_phenotype_edges.csv")))
linked_to_phe = {r["gene_id"] for r in gpe}
gme = list(csv.DictReader(open(SRC_DIR / "gene_mechanism_edges.csv")))
linked_to_mech = {r["gene_id"] for r in gme}

# A syndromic gene is "specifically wired" if it has direct phe or mech edge
specifically_wired_syndromic = {g["id"] for g in syndromic
                                if g["id"] in linked_to_phe
                                or g["id"] in linked_to_mech}
unwired_syndromic = [g for g in syndromic
                     if g["id"] not in specifically_wired_syndromic]

print("Gene category breakdown:")
print(f"  SFARI Tier 3 (suggestive):        {len(tier3)}")
print(f"  No SFARI score (OpenTargets-only): {len(no_sfari)}")
print(f"  Syndromic (S):                    {len(syndromic)}")
print(f"    of which specifically wired:    {len(specifically_wired_syndromic)}")
print(f"    of which un-wired:              {len(unwired_syndromic)}")

# ============================================================
# STEP 1: Bulk-link remaining genes → HYP-0028 with polarity=unknown
# ============================================================
print()
print("STEP 1: Wiring remaining genes to HYP-0028 polygenic risk with polarity=unknown")

new_edges = []
to_wire = tier3 + no_sfari + unwired_syndromic
seen = set()
for g in to_wire:
    if g["id"] in seen: continue
    seen.add(g["id"])
    if (g["id"], "HYP-0028") in ghe_pairs:
        continue
    # Build rationale based on evidence source
    if g["sfari_score"] == "3":
        rationale = "SFARI Tier 3 (suggestive evidence) ASD risk gene"
    elif g["sfari_score"] == "S":
        rationale = (f"SFARI Syndromic gene; gene_symbol={g['gene_symbol']} "
                     f"causes a syndrome that includes ASD as a feature")
    else:
        ot_score = g["opentargets_score"] or "0"
        rationale = (f"OpenTargets-only ASD-associated gene "
                     f"(opentargets_score={ot_score}); not in SFARI curated list")
    new_edges.append({
        "gene_id": g["id"],
        "hypothesis_id": "HYP-0028",
        "relation_type": "risk_factor_for",
        "polarity": "unknown",  # weaker evidence tier
        "rationale": rationale,
    })
print(f"  Generating {len(new_edges)} new gene→HYP-0028 edges")

# Append to gene_hypothesis_edges.csv in canonical
fields = list(csv.DictReader(open(SRC_DIR / "gene_hypothesis_edges.csv")).fieldnames)
existing_max = 0
for r in existing_ghe:
    try: existing_max = max(existing_max, int(r["id"].split("-")[-1]))
    except (ValueError, IndexError): pass

for d in [SRC_DIR, EXP_DIR]:
    p = d / "gene_hypothesis_edges.csv"
    rows = list(csv.DictReader(open(p)))
    cur_pairs = {(r["gene_id"], r["hypothesis_id"]) for r in rows}
    cur_max = 0
    for r in rows:
        try: cur_max = max(cur_max, int(r["id"].split("-")[-1]))
        except (ValueError, IndexError): pass
    added = 0
    for ne in new_edges:
        if (ne["gene_id"], ne["hypothesis_id"]) in cur_pairs: continue
        cur_max += 1
        new_row = {f: "" for f in fields}
        new_row["id"] = f"GHE-{cur_max:05d}"
        new_row["gene_id"] = ne["gene_id"]
        new_row["hypothesis_id"] = ne["hypothesis_id"]
        new_row["relation_type"] = ne["relation_type"]
        new_row["polarity"] = ne["polarity"]
        new_row["evidence_strength_aggregate"] = "0.0"
        if "status" in fields: new_row["status"] = "active"
        if "created_at" in fields: new_row["created_at"] = NOW
        if "last_updated" in fields: new_row["last_updated"] = NOW
        rows.append(new_row); added += 1
    with open(p, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
    print(f"  {d.name}/gene_hypothesis_edges.csv: +{added} (now {len(rows)} total)")

# ============================================================
# STEP 2: Hypothesis-hypothesis mechanism-overlap candidates
# ============================================================
print()
print("STEP 2: Generating hypothesis-hypothesis mechanism-overlap candidates")

hyps = list(csv.DictReader(open(SRC_DIR / "hypotheses.csv")))
hme = list(csv.DictReader(open(SRC_DIR / "hypothesis_mechanism_edges.csv")))
existing_hhe = list(csv.DictReader(open(SRC_DIR / "hypothesis_hypothesis_edges.csv")))
existing_hh_pairs = set()
for r in existing_hhe:
    u, dn = r.get("upstream_hypothesis_id",""), r.get("downstream_hypothesis_id","")
    existing_hh_pairs.add((u, dn))
    existing_hh_pairs.add((dn, u))  # bidirectional dedupe

# Build hyp -> mechanisms set
hyp_mechs = defaultdict(set)
for r in hme:
    hyp_mechs[r["hypothesis_id"]].add(r["mechanism_id"])

# Find pairs with >= 2 shared mechanisms
candidates = []
for h1, h2 in combinations(sorted(hyp_mechs.keys()), 2):
    if (h1, h2) in existing_hh_pairs:
        continue
    shared = hyp_mechs[h1] & hyp_mechs[h2]
    if len(shared) >= 2:
        candidates.append({
            "h1": h1, "h2": h2,
            "shared_mechanisms": sorted(shared),
            "n_shared": len(shared),
        })

# Sort by number of shared mechanisms (most shared first)
candidates.sort(key=lambda c: -c["n_shared"])
print(f"  {len(candidates)} candidate pairs with ≥2 shared mechanisms")

# Save as proposal CSV (these are CANDIDATES, not auto-merged)
hyp_lookup = {h["id"]: h for h in hyps}
fields = ["id", "h1_id", "h1_name", "h2_id", "h2_name",
          "n_shared_mechanisms", "shared_mechanism_ids",
          "h1_confidence", "h2_confidence", "rationale", "status", "created_at"]

with open(PROP_DIR / "candidate_hyp_hyp_edges.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields); w.writeheader()
    for i, c in enumerate(candidates, 1):
        h1, h2 = c["h1"], c["h2"]
        w.writerow({
            "id": f"CANDHH-{i:04d}",
            "h1_id": h1, "h1_name": hyp_lookup[h1]["name"][:80],
            "h2_id": h2, "h2_name": hyp_lookup[h2]["name"][:80],
            "n_shared_mechanisms": c["n_shared"],
            "shared_mechanism_ids": ";".join(c["shared_mechanisms"]),
            "h1_confidence": hyp_lookup[h1]["confidence_score"],
            "h2_confidence": hyp_lookup[h2]["confidence_score"],
            "rationale": (f"Both hypotheses act through {c['n_shared']} "
                          f"shared mechanisms; suggests possible upstream/"
                          f"downstream or co-cause relationship; needs "
                          f"directional review."),
            "status": "proposed",
            "created_at": NOW,
        })
print(f"  Wrote {len(candidates)} candidates to v2.0.1_proposed/candidate_hyp_hyp_edges.csv")

# Print top 10 candidates for visibility
print()
print("Top 10 candidates by shared mechanism count:")
for c in candidates[:10]:
    h1, h2 = c["h1"], c["h2"]
    print(f"  {h1} ↔ {h2}  ({c['n_shared']} shared)  "
          f"{hyp_lookup[h1]['name'][:35]:<37} ↔ {hyp_lookup[h2]['name'][:35]}")

print()
print("Session 2 ingestion complete.")
print("Next: re-run scoring + verify INT-0001 calibration + rebuild vault.")
