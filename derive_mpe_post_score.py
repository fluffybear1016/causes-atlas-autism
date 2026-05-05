#!/usr/bin/env python3
"""Re-derive mechanism_phenotype_edges.evidence_strength_aggregate in
scored_output_v20/ after the scoring engine wipes them to 0.

Same derivation as session1_finishing.py task 1, but applied to the scored
output directory rather than v2.0_scored / v2.0.1_expanded inputs (the
scoring engine ignores MPE strengths during its passes; we restore them
post-hoc so vault rendering / downstream analytics see the right numbers).
"""
import csv, datetime as dt
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIRS = [ROOT/"scored_output_v20", ROOT/"v2.0_scored", ROOT/"v2.0.1_expanded"]
NOW = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")

def read(d, name): return list(csv.DictReader(open(d / name)))

for d in DIRS:
    if not (d / "mechanism_phenotype_edges.csv").exists():
        continue
    mpe = read(d, "mechanism_phenotype_edges.csv")
    if not mpe: continue
    ime = read(d, "intervention_mechanism_edges.csv")
    ipe = read(d, "intervention_phenotype_edges.csv")
    hme = read(d, "hypothesis_mechanism_edges.csv")
    hyps = {h["id"]: h for h in read(d, "hypotheses.csv")}

    int_phenotypes = {}
    for r in ipe:
        int_phenotypes.setdefault(r["intervention_id"], set()).add(r["phenotype_id"])

    int_mech_strength = {}
    for r in ime:
        try: s = float(r.get("evidence_strength_aggregate") or 0)
        except ValueError: s = 0
        int_mech_strength.setdefault(r["intervention_id"], {})[r["mechanism_id"]] = s

    hyp_mech_strength = {}
    for r in hme:
        try: s = float(r.get("evidence_strength_aggregate") or 0)
        except ValueError: s = 0
        hyp_mech_strength.setdefault(r["hypothesis_id"], {})[r["mechanism_id"]] = s

    fields = list(csv.DictReader(open(d / "mechanism_phenotype_edges.csv")).fieldnames)
    new_mpe = []
    updates = 0
    for r in mpe:
        m_id = r["mechanism_id"]; p_id = r["phenotype_id"]
        candidates = []
        for iid, mech_strs in int_mech_strength.items():
            if m_id in mech_strs and p_id in int_phenotypes.get(iid, set()):
                candidates.append(mech_strs[m_id])
        for hid, mech_strs in hyp_mech_strength.items():
            if m_id in mech_strs:
                try: conf = float(hyps[hid].get("confidence_score", "0") or 0)
                except (ValueError, KeyError): conf = 0
                if conf >= 0.5:
                    candidates.append(mech_strs[m_id] * conf)
        w = max(candidates) if candidates else 0.20
        old = float(r.get("evidence_strength_aggregate") or 0)
        if abs(w - old) > 0.001:
            updates += 1
        r["evidence_strength_aggregate"] = f"{w:.4f}"
        r["last_updated"] = NOW
        new_mpe.append(r)

    with open(d / "mechanism_phenotype_edges.csv", "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=fields); wr.writeheader(); wr.writerows(new_mpe)
    print(f"  {d.name}/mechanism_phenotype_edges.csv: {updates} edges updated, {len(new_mpe)} total")
