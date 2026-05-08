#!/usr/bin/env python3
"""find_combination_gaps.py — autonomous pattern miner #2

Identifies pairs (and triples) of interventions that share ≥1 mechanism
but are NOT yet listed together in any combination_members entry. These
are candidate combinations for synergy testing.

Determinism: stable sort by ID; no random seeds; no LLM calls.

Usage:
    python3 scripts/find_combination_gaps.py
    python3 scripts/find_combination_gaps.py --max-pairs 100 --include-triples

Output:
    vault/Discoveries_Inbox/combination_gaps_{date}.md / .json
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from datetime import datetime
from itertools import combinations
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


def find_combination_gaps(
    max_pairs: int = 50,
    include_triples: bool = False,
    min_csrs: float = 50.0,
) -> dict:
    interventions = _load_csv("interventions")
    int_mech_edges = _load_csv("intervention_mechanism_edges")
    combinations_csv = _load_csv("combinations")
    combination_members = _load_csv("combination_members")

    # Map intervention_id → set of mechanism_ids
    int_mechs: dict[str, set[str]] = defaultdict(set)
    for e in int_mech_edges:
        iid = e.get("intervention_id", "")
        mid = e.get("mechanism_id", "")
        if iid and mid:
            int_mechs[iid].add(mid)

    # Map intervention_id → name + csrs
    int_meta = {}
    for r in interventions:
        iid = r.get("id", "")
        try:
            csrs = float(r.get("csrs_score") or 0)
        except (ValueError, TypeError):
            csrs = 0.0
        if iid:
            int_meta[iid] = {
                "name": r.get("name", ""),
                "category": r.get("category", ""),
                "csrs": csrs,
                "status": r.get("status", ""),
            }

    # Existing combination membership: which (sorted-tuple) sets are already combined
    combos_by_id: dict[str, set[str]] = defaultdict(set)
    for cm in combination_members:
        cid = cm.get("combination_id", "")
        iid = cm.get("intervention_id", "")
        if cid and iid:
            combos_by_id[cid].add(iid)
    existing_combos = {tuple(sorted(s)) for s in combos_by_id.values()}

    # Helper: is the set already a combination, or a subset of one?
    def is_already_combined(int_set: tuple[str, ...]) -> bool:
        s = set(int_set)
        for combo in existing_combos:
            if s.issubset(set(combo)):
                return True
        return False

    # Filter to high-CSRS interventions for tractable combinatorial space
    eligible_ids = sorted([
        iid for iid, meta in int_meta.items()
        if meta["csrs"] >= min_csrs and iid in int_mechs
    ])

    # Pair generation: stable iteration order
    candidate_pairs = []
    for a, b in combinations(eligible_ids, 2):
        shared = int_mechs[a] & int_mechs[b]
        if len(shared) >= 1 and not is_already_combined((a, b)):
            candidate_pairs.append({
                "interventions": [a, b],
                "intervention_names": [int_meta[a]["name"], int_meta[b]["name"]],
                "shared_mechanisms": sorted(shared),
                "shared_count": len(shared),
                "csrs_sum": int_meta[a]["csrs"] + int_meta[b]["csrs"],
                "csrs_min": min(int_meta[a]["csrs"], int_meta[b]["csrs"]),
            })
    candidate_pairs.sort(key=lambda c: (-c["shared_count"], -c["csrs_sum"], c["interventions"]))
    candidate_pairs = candidate_pairs[:max_pairs]

    candidate_triples: list[dict] = []
    if include_triples:
        for a, b, c in combinations(eligible_ids[:30], 3):  # cap at top 30 to limit O(n³)
            shared = int_mechs[a] & int_mechs[b] & int_mechs[c]
            if len(shared) >= 1 and not is_already_combined((a, b, c)):
                candidate_triples.append({
                    "interventions": [a, b, c],
                    "intervention_names": [int_meta[a]["name"], int_meta[b]["name"], int_meta[c]["name"]],
                    "shared_mechanisms": sorted(shared),
                    "shared_count": len(shared),
                    "csrs_sum": int_meta[a]["csrs"] + int_meta[b]["csrs"] + int_meta[c]["csrs"],
                })
        candidate_triples.sort(key=lambda c: (-c["shared_count"], -c["csrs_sum"], c["interventions"]))
        candidate_triples = candidate_triples[:max_pairs // 2]

    return {
        "candidate_pairs": candidate_pairs,
        "candidate_triples": candidate_triples,
        "min_csrs_threshold": min_csrs,
        "eligible_interventions_count": len(eligible_ids),
        "existing_combination_count": len(existing_combos),
    }


def render_markdown(result: dict, date_str: str) -> str:
    lines = [
        f"# Combination gaps report — {date_str}",
        "",
        f"**Eligible interventions** (CSRS ≥ {result['min_csrs_threshold']}): {result['eligible_interventions_count']}",
        f"**Existing combinations:** {result['existing_combination_count']}",
        "",
        "Pattern miner #2 of the autonomous discovery pipeline. These are intervention pairs/triples that share ≥1 mechanism but are NOT yet captured in any combination. They are candidate synergies for review.",
        "",
        "**Important caveat:** mechanism overlap does NOT guarantee synergy. Some shared-mechanism pairs are antagonistic (both upregulate same pathway → ceiling effect; both deplete same cofactor → depletion). Curator review must consider direction-of-effect.",
        "",
        "---",
        "",
        f"## Top {len(result['candidate_pairs'])} candidate intervention pairs",
        "",
        "| # | Interventions | Shared mech. | CSRS sum |",
        "| --- | --- | --- | --- |",
    ]
    for i, c in enumerate(result["candidate_pairs"], 1):
        names = " + ".join(c["intervention_names"])
        ids = " + ".join(c["interventions"])
        mechs = ", ".join(c["shared_mechanisms"][:3])
        if len(c["shared_mechanisms"]) > 3:
            mechs += f" (+{len(c['shared_mechanisms']) - 3} more)"
        lines.append(
            f"| {i} | **{names}** ({ids}) | {mechs} | {c['csrs_sum']:.1f} |"
        )
    if not result["candidate_pairs"]:
        lines.append("| _none above threshold this scan_ | | | |")

    if result["candidate_triples"]:
        lines.extend(["", f"## Top {len(result['candidate_triples'])} candidate intervention triples", ""])
        lines.append("| # | Interventions | Shared mech. | CSRS sum |")
        lines.append("| --- | --- | --- | --- |")
        for i, c in enumerate(result["candidate_triples"], 1):
            names = " + ".join(c["intervention_names"])
            mechs = ", ".join(c["shared_mechanisms"][:3])
            lines.append(
                f"| {i} | **{names}** | {mechs} | {c['csrs_sum']:.1f} |"
            )

    lines.extend([
        "",
        "---",
        "",
        "## Curator workflow",
        "",
        "1. Pick a candidate pair/triple from above.",
        "2. Read the shared mechanism description(s); confirm direction-of-effect (synergistic vs antagonistic vs ceiling).",
        "3. Search PubMed for any prior trial / case report / mechanistic study of this combination.",
        "4. If a real combination synergy exists, add a row to `v2.0_scored/combinations.csv` and `v2.0_scored/combination_members.csv`.",
        "5. Re-run scoring; verify INT-0001 calibration.",
        "6. Commit with PMIDs in commit message.",
        "",
        "## Provenance",
        "",
        f"- Pipeline: `scripts/find_combination_gaps.py`",
        f"- Run timestamp: {datetime.utcnow().isoformat()}Z",
    ])
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-pairs", type=int, default=50)
    parser.add_argument("--include-triples", action="store_true")
    parser.add_argument("--min-csrs", type=float, default=50.0)
    parser.add_argument("--date", default=datetime.utcnow().strftime("%Y-%m-%d"))
    args = parser.parse_args(argv)

    result = find_combination_gaps(
        max_pairs=args.max_pairs,
        include_triples=args.include_triples,
        min_csrs=args.min_csrs,
    )

    md_path = INBOX_DIR / f"combination_gaps_{args.date}.md"
    json_path = INBOX_DIR / f"combination_gaps_{args.date}.json"
    md_path.write_text(render_markdown(result, args.date))
    json_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")

    print(f"Wrote {md_path}")
    print(f"Found {len(result['candidate_pairs'])} candidate pairs, {len(result['candidate_triples'])} triples")
    return 0


if __name__ == "__main__":
    sys.exit(main())
