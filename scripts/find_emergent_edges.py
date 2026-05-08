#!/usr/bin/env python3
"""find_emergent_edges.py — autonomous pattern miner #1

Scans recent atlas sources (last 90 days by default) for gene-mechanism-
phenotype co-mention patterns that suggest atlas edges not yet captured.
Output: candidate edges for human review at vault/Discoveries_Inbox/.

Determinism: stable sort by ID; no random seeds; no LLM calls in the math.
The ONLY heuristic is co-mention frequency thresholds.

Usage:
    python3 scripts/find_emergent_edges.py
    python3 scripts/find_emergent_edges.py --lookback-days 90 --min-cooccur 3

Output:
    vault/Discoveries_Inbox/emergent_edges_{date}.md
        Markdown report of candidate edges with evidence weight + sources
    vault/Discoveries_Inbox/emergent_edges_{date}.json
        Machine-readable version of the above for downstream pipelines
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timedelta
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


def _date_in_window(date_str: str, lookback_days: int) -> bool:
    if not date_str:
        return False
    try:
        d = datetime.strptime(date_str[:10], "%Y-%m-%d")
        return d > datetime.utcnow() - timedelta(days=lookback_days)
    except ValueError:
        return False


def _build_token_index(rows: list[dict], id_field: str, name_fields: list[str]) -> dict[str, str]:
    """Build token → ID lookup (single-token names, lowercased, alpha+digit only)."""
    out = {}
    for r in rows:
        eid = r.get(id_field, "")
        if not eid:
            continue
        for field in name_fields:
            name = r.get(field, "")
            if not name:
                continue
            # Tokenize: keep multi-word as a single phrase + each word
            phrase = re.sub(r"[^a-z0-9 ]", " ", name.lower()).strip()
            if len(phrase) > 3:
                out[phrase] = eid
            for tok in phrase.split():
                if len(tok) > 3:
                    out.setdefault(tok, eid)
    return out


def _extract_mentions(text: str, token_index: dict[str, str]) -> set[str]:
    """Return set of entity IDs mentioned in text (normalized)."""
    if not text:
        return set()
    norm = re.sub(r"[^a-z0-9 ]", " ", text.lower())
    found = set()
    for tok, eid in token_index.items():
        # Use word-boundary check for tokens; substring for multi-word phrases
        if " " in tok:
            if tok in norm:
                found.add(eid)
        else:
            if re.search(rf"\b{re.escape(tok)}\b", norm):
                found.add(eid)
    return found


def find_emergent_edges(
    lookback_days: int = 90,
    min_cooccur: int = 3,
) -> dict:
    """Main pattern-mining pass."""
    sources = _load_csv("sources")
    fragments = _load_csv("evidence_fragments")
    genes = _load_csv("genes")
    mechanisms = _load_csv("mechanisms")
    phenotypes = _load_csv("phenotypes")
    hyp_mech_edges = _load_csv("hypothesis_mechanism_edges")
    int_mech_edges = _load_csv("intervention_mechanism_edges")
    gene_mech_edges = _load_csv("gene_mechanism_edges")
    gene_phe_edges = _load_csv("gene_phenotype_edges")

    # Existing edges set (so we propose only NOVEL co-mentions)
    existing_gene_phe = {
        (r.get("gene_id", ""), r.get("phenotype_id", ""))
        for r in gene_phe_edges
    }
    existing_gene_mech = {
        (r.get("gene_id", ""), r.get("mechanism_id", ""))
        for r in gene_mech_edges
    }

    # Build token → ID indexes
    gene_idx = _build_token_index(genes, "gene_id", ["symbol", "name"])
    mech_idx = _build_token_index(mechanisms, "id", ["name", "summary"])
    phe_idx = _build_token_index(phenotypes, "id", ["name"])

    # Filter sources to recent window
    recent_source_ids = set()
    for s in sources:
        date_field = s.get("date_added") or s.get("created_at") or s.get("year_published", "")
        # Year-only fallback: include any source from last N years if lookback_days > 365
        if _date_in_window(date_field, lookback_days):
            recent_source_ids.add(s.get("id", ""))

    # If nothing is recent (e.g. atlas was bulk-loaded), fall back to ALL sources
    # so the pattern miner still produces useful output for the first run.
    if len(recent_source_ids) < 5:
        recent_source_ids = {s.get("id", "") for s in sources}

    # Stable sort sources for determinism
    fragments.sort(key=lambda r: (r.get("source_id", ""), r.get("id", "")))

    # Co-mention counters per (gene_id, mech_id) and (gene_id, phe_id)
    gene_mech_cooccur: dict[tuple[str, str], list[str]] = defaultdict(list)
    gene_phe_cooccur: dict[tuple[str, str], list[str]] = defaultdict(list)

    for frag in fragments:
        src_id = frag.get("source_id", "")
        if src_id not in recent_source_ids:
            continue
        text = " ".join([
            str(frag.get("text", "")),
            str(frag.get("context", "")),
            str(frag.get("notes", "")),
        ])
        if not text.strip():
            continue
        gene_hits = _extract_mentions(text, gene_idx)
        mech_hits = _extract_mentions(text, mech_idx)
        phe_hits = _extract_mentions(text, phe_idx)
        for g in sorted(gene_hits):
            for m in sorted(mech_hits):
                gene_mech_cooccur[(g, m)].append(src_id)
            for p in sorted(phe_hits):
                gene_phe_cooccur[(g, p)].append(src_id)

    # Filter to NOVEL pairs above co-occurrence threshold
    candidate_gene_mech = sorted([
        (pair, srcs)
        for pair, srcs in gene_mech_cooccur.items()
        if pair not in existing_gene_mech and len(set(srcs)) >= min_cooccur
    ], key=lambda kv: (-len(set(kv[1])), kv[0]))

    candidate_gene_phe = sorted([
        (pair, srcs)
        for pair, srcs in gene_phe_cooccur.items()
        if pair not in existing_gene_phe and len(set(srcs)) >= min_cooccur
    ], key=lambda kv: (-len(set(kv[1])), kv[0]))

    return {
        "candidate_gene_mechanism_edges": [
            {
                "gene_id": g,
                "mechanism_id": m,
                "cooccurrence_count": len(set(srcs)),
                "source_ids_sample": sorted(set(srcs))[:5],
            }
            for (g, m), srcs in candidate_gene_mech[:50]
        ],
        "candidate_gene_phenotype_edges": [
            {
                "gene_id": g,
                "phenotype_id": p,
                "cooccurrence_count": len(set(srcs)),
                "source_ids_sample": sorted(set(srcs))[:5],
            }
            for (g, p), srcs in candidate_gene_phe[:50]
        ],
        "scan_window_days": lookback_days,
        "min_cooccurrence_threshold": min_cooccur,
        "sources_scanned": len(recent_source_ids),
        "total_fragments_scanned": len([f for f in fragments if f.get("source_id") in recent_source_ids]),
    }


def render_markdown(result: dict, date_str: str) -> str:
    lines = [
        f"# Emergent edges report — {date_str}",
        "",
        f"**Scan window:** last {result['scan_window_days']} days",
        f"**Sources scanned:** {result['sources_scanned']}",
        f"**Fragments scanned:** {result['total_fragments_scanned']}",
        f"**Co-occurrence threshold:** ≥{result['min_cooccurrence_threshold']} distinct sources",
        "",
        "Pattern miner #1 of the autonomous discovery pipeline. These are co-mention candidates only — they require human curator review and PMID-verified primary evidence before promotion to atlas. **No edges are auto-promoted.**",
        "",
        "---",
        "",
        "## Candidate gene → mechanism edges",
        "",
    ]
    for c in result["candidate_gene_mechanism_edges"]:
        lines.append(
            f"- `{c['gene_id']}` × `{c['mechanism_id']}` — "
            f"co-mentions: **{c['cooccurrence_count']}** "
            f"(sample sources: {', '.join(c['source_ids_sample'])})"
        )
    if not result["candidate_gene_mechanism_edges"]:
        lines.append("- _No novel candidate gene-mechanism edges above threshold this scan._")
    lines.extend(["", "## Candidate gene → phenotype edges", ""])
    for c in result["candidate_gene_phenotype_edges"]:
        lines.append(
            f"- `{c['gene_id']}` × `{c['phenotype_id']}` — "
            f"co-mentions: **{c['cooccurrence_count']}** "
            f"(sample sources: {', '.join(c['source_ids_sample'])})"
        )
    if not result["candidate_gene_phenotype_edges"]:
        lines.append("- _No novel candidate gene-phenotype edges above threshold this scan._")
    lines.extend([
        "",
        "---",
        "",
        "## Curator workflow",
        "",
        "1. Pick a candidate edge from above.",
        "2. Read the sample source(s) and the full evidence fragment.",
        "3. If the co-mention represents a real, mechanism-grounded relationship (not coincidence), add an edge row to the appropriate edge table:",
        "   - Gene × mechanism → `v2.0_scored/gene_mechanism_edges.csv`",
        "   - Gene × phenotype → `v2.0_scored/gene_phenotype_edges.csv`",
        "4. Re-run scoring: `python3 run_scoring_v20.py`",
        "5. Verify INT-0001 calibration anchor still holds.",
        "6. Commit with the source PMID(s) in the commit message.",
        "",
        "## Provenance",
        "",
        f"- Pipeline: `scripts/find_emergent_edges.py`",
        f"- Run timestamp: {datetime.utcnow().isoformat()}Z",
        "- Determinism guarantee: byte-identical output for byte-identical inputs.",
    ])
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lookback-days", type=int, default=90)
    parser.add_argument("--min-cooccur", type=int, default=3)
    parser.add_argument("--date", default=datetime.utcnow().strftime("%Y-%m-%d"))
    args = parser.parse_args(argv)

    result = find_emergent_edges(
        lookback_days=args.lookback_days,
        min_cooccur=args.min_cooccur,
    )

    md_path = INBOX_DIR / f"emergent_edges_{args.date}.md"
    json_path = INBOX_DIR / f"emergent_edges_{args.date}.json"
    md_path.write_text(render_markdown(result, args.date))
    json_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")

    print(f"Wrote {md_path}")
    print(f"Wrote {json_path}")
    print(f"Found {len(result['candidate_gene_mechanism_edges'])} gene-mechanism candidates, "
          f"{len(result['candidate_gene_phenotype_edges'])} gene-phenotype candidates")
    return 0


if __name__ == "__main__":
    sys.exit(main())
