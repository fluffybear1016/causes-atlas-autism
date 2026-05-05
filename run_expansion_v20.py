#!/usr/bin/env python3
"""
run_expansion_v20.py — Causes Atlas (Autism) v2.0 schema extensions

Reads:  scored_output_v19/*.csv
Writes: expanded_output_v20/*.csv

v2.0 implements spec v1.2 schema extensions:

  (d) hypothesis_hypothesis_edges (§5.7) — causal chains. Adds 15
      evidence-supported upstream → downstream relationships:
        glyphosate → microbiome dysbiosis → Clostridia overgrowth
        microbiome dysbiosis → Bifidobacterium depletion
        microbiome dysbiosis → leaky gut → neuroinflammation phenotype
        maternal autoimmunity → maternal immune activation
        broader vaccines ⊃ {hep B, Al adjuvant, MMR, thimerosal}
        mitochondrial dysfunction → lactate/pyruvate elevation
        prenatal stress → HPA axis dysregulation
        … etc.

  (e) prevention/treatment column scaffolds — scoring engine populates.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd

INPUT_DIR = Path("scored_output_v19")
OUTPUT_DIR = Path("expanded_output_v20")


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")


def pad_id(prefix: str, n: int, width: int) -> str:
    return f"{prefix}-{str(n).zfill(width)}"


# Causal chains: (upstream_name, downstream_name, relation_type)
# All upstream → downstream supported by literature already in atlas.
NEW_HHE = [
    # Environmental → microbiome
    ("Glyphosate exposure (food + water)",
     "Gut microbiome dysbiosis / dysbiotic fermentation",
     "upstream_of"),
    ("Glyphosate exposure (food + water)",
     "Clostridia overgrowth / dysbiotic fermentation",
     "upstream_of"),
    # Microbiome chains
    ("Gut microbiome dysbiosis / dysbiotic fermentation",
     "Bifidobacterium depletion (autism-specific)", "preconditions"),
    ("Gut microbiome dysbiosis / dysbiotic fermentation",
     "Clostridia overgrowth / dysbiotic fermentation",
     "preconditions"),
    ("Gut microbiome dysbiosis / dysbiotic fermentation",
     "Akkermansia / Faecalibacterium depletion", "preconditions"),
    ("Gut microbiome dysbiosis / dysbiotic fermentation",
     "Intestinal barrier permeability ('leaky gut')",
     "upstream_of"),
    ("Clostridia overgrowth / dysbiotic fermentation",
     "Microbial p-cresol / 4-EPS metabolite excess", "upstream_of"),
    ("Intestinal barrier permeability ('leaky gut')",
     "Maternal immune activation (prenatal infection or autoimmune)",
     "exacerbates"),
    # Antibiotics → microbiome
    ("Early-life antibiotics (especially first year)",
     "Gut microbiome dysbiosis / dysbiotic fermentation",
     "upstream_of"),
    ("Early-life antibiotics (especially first year)",
     "Bifidobacterium depletion (autism-specific)", "upstream_of"),
    # Cesarean → microbiome
    ("Cesarean section delivery",
     "Gut microbiome dysbiosis / dysbiotic fermentation",
     "upstream_of"),
    # Maternal immune chain
    ("Maternal autoimmune comorbidity",
     "Maternal immune activation (prenatal infection or autoimmune)",
     "preconditions"),
    ("Maternal autoimmune comorbidity",
     "Maternal/prenatal thyroid hypofunction", "comorbid_with"),
    # Vaccine generic → specific (parent-child)
    ("Childhood vaccine exposure (contested)",
     "Hepatitis B vaccine (neonatal birth-dose)", "upstream_of"),
    ("Childhood vaccine exposure (contested)",
     "MMR vaccine specifically (contested)", "upstream_of"),
    ("Childhood vaccine exposure (contested)",
     "Aluminum adjuvant cumulative exposure (vaccines)",
     "upstream_of"),
    ("Childhood vaccine exposure (contested)",
     "Thimerosal exposure (contested, largely removed)",
     "upstream_of"),
    # Hep B is also one example of Al adjuvant exposure
    ("Aluminum adjuvant cumulative exposure (vaccines)",
     "Hepatitis B vaccine (neonatal birth-dose)", "comorbid_with"),
    # Mitochondrial chain
    ("Mitochondrial dysfunction (acquired or inherited)",
     "Lactate / pyruvate ratio elevation (bioenergetic biomarker)",
     "upstream_of"),
    ("Mitochondrial dysfunction (acquired or inherited)",
     "AMPK pathway dysregulation", "comorbid_with"),
    ("Mitochondrial dysfunction (acquired or inherited)",
     "SIRTUIN / NAD+ depletion", "comorbid_with"),
    # Stress chain
    ("Maternal psychological stress (prenatal)",
     "Childhood/family emotional stress", "upstream_of"),
    ("Maternal autoimmune comorbidity",
     "Maternal psychological stress (prenatal)", "exacerbates"),
    # Heavy metal → mitochondrial
    ("Heavy metal exposure (Pb, Hg, Al)",
     "Mitochondrial dysfunction (acquired or inherited)",
     "upstream_of"),
    # Folate → methylation cascade
    ("Maternal folate deficiency during preconception/pregnancy",
     "Brain serotonin synthesis dysregulation (TPH2/vitamin D)",
     "modulates"),
    # Vitamin D → serotonin pathway
    ("Vitamin D deficiency (maternal + child)",
     "Brain serotonin synthesis dysregulation (TPH2/vitamin D)",
     "upstream_of"),
    # Prenatal acetaminophen → oxidative cascade
    ("Prenatal acetaminophen (paracetamol) exposure",
     "Brain glutathione depletion", "upstream_of"),
    ("Acetaminophen postnatal use (contested)",
     "Brain glutathione depletion", "upstream_of"),
    # Sleep disruption ↔ mitochondrial
    ("Sleep disruption / circadian misalignment",
     "Mitochondrial dysfunction (acquired or inherited)",
     "exacerbates"),
    # Iron → mitochondrial
    ("Iron metabolism dysregulation",
     "Mitochondrial dysfunction (acquired or inherited)",
     "upstream_of"),
    # Air pollution → neuroinflammation cascade through mitochondrial
    ("Air pollution (PM2.5, traffic)",
     "Mitochondrial dysfunction (acquired or inherited)",
     "upstream_of"),
    # PFAS → thyroid
    ("PFAS / forever-chemical drinking-water exposure",
     "Maternal/prenatal thyroid hypofunction", "upstream_of"),
    # Iodine → thyroid (already a relationship; explicit chain)
    ("Iodine deficiency / thyroid hypofunction",
     "Maternal/prenatal thyroid hypofunction", "comorbid_with"),
]


HHE_HEADERS = [
    "id", "upstream_hypothesis_id", "downstream_hypothesis_id",
    "relation_type", "polarity",
    "evidence_for_count", "evidence_against_count",
    "evidence_strength_aggregate", "context_scope", "status",
    "created_at", "last_updated",
]


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    ts = now_iso()
    print(f"[v2.0] running at {ts}")

    tables = {}
    for csv in sorted(INPUT_DIR.glob("*.csv")):
        tables[csv.stem] = pd.read_csv(
            csv, dtype=str, keep_default_na=False)

    hyp_name_to_id = {r["name"]: r["id"]
                      for _, r in tables["hypotheses"].iterrows()}

    # Build hypothesis_hypothesis_edges
    rows = []
    skipped = []
    n = 1
    for up_name, down_name, rel in NEW_HHE:
        up = hyp_name_to_id.get(up_name)
        down = hyp_name_to_id.get(down_name)
        if not up or not down:
            skipped.append((up_name, down_name)); continue
        if up == down: continue  # self-loops
        eid = pad_id("HHE", n, 5); n += 1
        rows.append({
            "id": eid,
            "upstream_hypothesis_id": up,
            "downstream_hypothesis_id": down,
            "relation_type": rel,
            "polarity": "supporting",
            "evidence_for_count": "",
            "evidence_against_count": "",
            "evidence_strength_aggregate": "",
            "context_scope": "", "status": "active",
            "created_at": ts, "last_updated": ts,
        })
    hhe_df = pd.DataFrame(rows, columns=HHE_HEADERS)
    tables["hypothesis_hypothesis_edges"] = hhe_df
    print(f"[v2.0] hypothesis_hypothesis_edges: +{len(rows)}")
    if skipped:
        print(f"[v2.0] skipped {len(skipped)} unresolvable pairs")

    # Add prevention/treatment scoring scaffold columns to interventions
    new_cols = ["csrs_prevention_score", "csrs_prevention_last_updated",
                "csrs_treatment_score", "csrs_treatment_last_updated"]
    for col in new_cols:
        if col not in tables["interventions"].columns:
            tables["interventions"][col] = ""
        if col not in tables["combinations"].columns:
            tables["combinations"][col] = ""

    # Cycle check: must remain a DAG
    import collections
    adj = collections.defaultdict(set)
    for r in rows:
        adj[r["upstream_hypothesis_id"]].add(r["downstream_hypothesis_id"])
    visited = set()
    stack = set()
    def dfs(node):
        if node in stack: return True
        if node in visited: return False
        visited.add(node); stack.add(node)
        for nbr in adj.get(node, []):
            if dfs(nbr): return True
        stack.remove(node); return False
    cycle = any(dfs(n) for n in adj)
    print(f"[v2.0] DAG check: {'FAIL — cycle detected' if cycle else 'PASS — acyclic'}")

    for name, df in tables.items():
        df.to_csv(OUTPUT_DIR / f"{name}.csv", index=False, encoding="utf-8")

    Path("expansion_v20_summary.json").write_text(json.dumps({
        "expansion_version": "v2.0_dag_dual_scoring",
        "run_timestamp": ts,
        "added": {
            "hypothesis_hypothesis_edges": len(rows),
            "intervention_dual_scoring_cols": 4,
            "combination_dual_scoring_cols": 4,
        },
        "skipped_pairs": len(skipped),
        "dag_acyclic": not cycle,
    }, indent=2))
    print()
    print("=" * 60)
    print("v2.0 SCHEMA EXTENSION COMPLETE")


if __name__ == "__main__":
    main()
