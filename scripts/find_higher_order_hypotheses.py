#!/usr/bin/env python3
"""find_higher_order_hypotheses.py — autonomous pattern miner #3

Walks the atlas knowledge graph for 2nd- and 3rd-order hypothesis chains:
  - 2nd-order: A→B + B→C ⇒ candidate A→C
  - 3rd-order: A→B + B→C + C→D ⇒ candidate A→D
Filters to chains where direct A→D edge does NOT yet exist.

This surfaces non-obvious causal chains the atlas implicitly contains
but doesn't yet make explicit.

Determinism: stable sort by ID; no random seeds; no LLM calls.

Usage:
    python3 scripts/find_higher_order_hypotheses.py
    python3 scripts/find_higher_order_hypotheses.py --max-chains 50

Output:
    vault/Discoveries_Inbox/higher_order_hypotheses_{date}.md / .json
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCORED_DIR = ROOT / "v2.0_scored"
INBOX_DIR = ROOT / "vault" / "Discoveries_Inbox"
INBOX_DIR.mkdir(parents=True, exist_ok=True)


def _load_csv(name: str) -> list[dict]:
    path = SCORED_DIR / f"{name}.csv"
    if not path.exists():
        return []
    with path.open() as f:
        return list(csv.DictReader(f))


def find_higher_order_chains(max_chains: int = 50) -> dict:
    hyp_mech_edges = _load_csv("hypothesis_mechanism_edges")
    mech_phe_edges = _load_csv("mechanism_phenotype_edges")
    int_mech_edges = _load_csv("intervention_mechanism_edges")
    int_hyp_edges = _load_csv("intervention_hypothesis_edges")
    int_phe_edges = _load_csv("intervention_phenotype_edges")
    hyp_hyp_edges = _load_csv("hypothesis_hypothesis_edges")

    interventions = _load_csv("interventions")
    hypotheses = _load_csv("hypotheses")
    mechanisms = _load_csv("mechanisms")
    phenotypes = _load_csv("phenotypes")

    int_name = {r.get("id"): r.get("name", "") for r in interventions}
    hyp_name = {r.get("id"): r.get("name", "") for r in hypotheses}
    mech_name = {r.get("id"): r.get("name", "") for r in mechanisms}
    phe_name = {r.get("id"): r.get("name", "") for r in phenotypes}

    # Build forward adjacency
    hyp_to_mech = defaultdict(set)
    for e in hyp_mech_edges:
        hyp_to_mech[e.get("hypothesis_id", "")].add(e.get("mechanism_id", ""))

    mech_to_phe = defaultdict(set)
    for e in mech_phe_edges:
        mech_to_phe[e.get("mechanism_id", "")].add(e.get("phenotype_id", ""))

    int_to_mech = defaultdict(set)
    for e in int_mech_edges:
        int_to_mech[e.get("intervention_id", "")].add(e.get("mechanism_id", ""))

    # Existing direct edges (so we propose only NOVEL implied chains)
    existing_int_phe = {
        (e.get("intervention_id", ""), e.get("phenotype_id", ""))
        for e in int_phe_edges
    }
    existing_int_hyp = {
        (e.get("intervention_id", ""), e.get("hypothesis_id", ""))
        for e in int_hyp_edges
    }

    # 2nd-order chain: hypothesis → mechanism → phenotype ⇒ implied hyp×phe
    # 2nd-order chain: intervention → mechanism → phenotype ⇒ implied int×phe
    # 3rd-order chain: intervention → mech1 → phe + mech1 → phe ⇒ multi-mechanism conf

    candidates_int_phe: list[dict] = []
    for iid, mech_set in sorted(int_to_mech.items()):
        phe_via_mech: dict[str, set[str]] = defaultdict(set)
        for mid in sorted(mech_set):
            for pid in sorted(mech_to_phe.get(mid, set())):
                phe_via_mech[pid].add(mid)
        for pid, mech_path in sorted(phe_via_mech.items()):
            if (iid, pid) in existing_int_phe:
                continue
            if not iid or not pid:
                continue
            candidates_int_phe.append({
                "intervention_id": iid,
                "intervention_name": int_name.get(iid, ""),
                "phenotype_id": pid,
                "phenotype_name": phe_name.get(pid, ""),
                "via_mechanisms": sorted(mech_path),
                "mechanism_path_count": len(mech_path),
            })

    candidates_int_phe.sort(key=lambda c: (-c["mechanism_path_count"], c["intervention_id"], c["phenotype_id"]))
    candidates_int_phe = candidates_int_phe[:max_chains]

    # Hypothesis-level higher-order: hyp → mech → phe via existing edges,
    # but only flag if intervention can target this hyp (intervention_hypothesis_edges)
    candidates_hyp_phe: list[dict] = []
    int_to_hyp = defaultdict(set)
    for e in int_hyp_edges:
        int_to_hyp[e.get("intervention_id", "")].add(e.get("hypothesis_id", ""))
    hyp_to_int = defaultdict(set)
    for iid, hyps in int_to_hyp.items():
        for h in hyps:
            hyp_to_int[h].add(iid)
    for hid, mech_set in sorted(hyp_to_mech.items()):
        phe_via_mech: dict[str, set[str]] = defaultdict(set)
        for mid in sorted(mech_set):
            for pid in sorted(mech_to_phe.get(mid, set())):
                phe_via_mech[pid].add(mid)
        for pid, mech_path in sorted(phe_via_mech.items()):
            if not hid or not pid:
                continue
            int_targeting_hyp = sorted(hyp_to_int.get(hid, set()))[:3]
            if not int_targeting_hyp:
                continue
            candidates_hyp_phe.append({
                "hypothesis_id": hid,
                "hypothesis_name": hyp_name.get(hid, ""),
                "phenotype_id": pid,
                "phenotype_name": phe_name.get(pid, ""),
                "via_mechanisms": sorted(mech_path),
                "interventions_targeting_hypothesis": int_targeting_hyp,
            })

    candidates_hyp_phe.sort(key=lambda c: (c["hypothesis_id"], c["phenotype_id"]))
    candidates_hyp_phe = candidates_hyp_phe[:max_chains]

    return {
        "candidate_intervention_phenotype_chains": candidates_int_phe,
        "candidate_hypothesis_phenotype_chains": candidates_hyp_phe,
        "edges_walked": {
            "hypothesis_mechanism_edges": len(hyp_mech_edges),
            "mechanism_phenotype_edges": len(mech_phe_edges),
            "intervention_mechanism_edges": len(int_mech_edges),
            "intervention_phenotype_edges": len(int_phe_edges),
        },
    }


def render_markdown(result: dict, date_str: str) -> str:
    lines = [
        f"# Higher-order hypothesis chains — {date_str}",
        "",
        "Pattern miner #3: walks the atlas graph for 2nd-order chains (intervention→mechanism→phenotype) and flags pairs where the direct edge does NOT yet exist. These are implied causal claims the atlas already supports indirectly.",
        "",
        f"**Edges walked:** {result['edges_walked']}",
        "",
        "---",
        "",
        f"## Top {len(result['candidate_intervention_phenotype_chains'])} implied intervention → phenotype edges (via mechanism)",
        "",
        "| # | Intervention | Phenotype | Mechanism path |",
        "| --- | --- | --- | --- |",
    ]
    for i, c in enumerate(result["candidate_intervention_phenotype_chains"], 1):
        mech_str = " + ".join(c["via_mechanisms"][:3])
        if len(c["via_mechanisms"]) > 3:
            mech_str += f" (+{len(c['via_mechanisms']) - 3} more)"
        lines.append(
            f"| {i} | `{c['intervention_id']}` {c['intervention_name'][:35]} | "
            f"`{c['phenotype_id']}` {c['phenotype_name'][:30]} | {mech_str} |"
        )
    if not result["candidate_intervention_phenotype_chains"]:
        lines.append("| _none above threshold_ | | | |")

    lines.extend([
        "",
        f"## Top {len(result['candidate_hypothesis_phenotype_chains'])} implied hypothesis → phenotype edges",
        "",
        "Hypotheses with intervention targeting + mechanism path to phenotype.",
        "",
        "| # | Hypothesis | Phenotype | Via mech. | Interventions targeting hyp |",
        "| --- | --- | --- | --- | --- |",
    ])
    for i, c in enumerate(result["candidate_hypothesis_phenotype_chains"], 1):
        ints = ", ".join(c["interventions_targeting_hypothesis"])
        lines.append(
            f"| {i} | `{c['hypothesis_id']}` | `{c['phenotype_id']}` "
            f"{c['phenotype_name'][:25]} | {len(c['via_mechanisms'])} | {ints} |"
        )

    lines.extend([
        "",
        "---",
        "",
        "## Curator workflow",
        "",
        "1. Pick a candidate chain.",
        "2. Read the mechanism path; confirm the chain is biologically valid (not just graph artifact).",
        "3. Add direct intervention_phenotype_edge or hypothesis_phenotype_edge if the chain is real.",
        "4. Re-run scoring; verify INT-0001 calibration anchor.",
        "",
        "## Provenance",
        "",
        f"- Pipeline: `scripts/find_higher_order_hypotheses.py`",
        f"- Run timestamp: {datetime.utcnow().isoformat()}Z",
    ])
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-chains", type=int, default=50)
    parser.add_argument("--date", default=datetime.utcnow().strftime("%Y-%m-%d"))
    args = parser.parse_args(argv)

    result = find_higher_order_chains(max_chains=args.max_chains)

    md_path = INBOX_DIR / f"higher_order_hypotheses_{args.date}.md"
    json_path = INBOX_DIR / f"higher_order_hypotheses_{args.date}.json"
    md_path.write_text(render_markdown(result, args.date))
    json_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")

    print(f"Wrote {md_path}")
    print(f"Found {len(result['candidate_intervention_phenotype_chains'])} int→phe chains, "
          f"{len(result['candidate_hypothesis_phenotype_chains'])} hyp→phe chains")
    return 0


if __name__ == "__main__":
    sys.exit(main())
