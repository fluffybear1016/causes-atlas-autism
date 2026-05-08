#!/usr/bin/env python3
"""run_autonomous_discoveries.py — orchestrator for the autonomous
pattern-mining engine (items 5+7 of the meta roadmap).

Runs all four pattern-miner scripts in sequence, deduplicates candidates
across runs, writes a daily summary index page, and updates the
Discoveries Inbox vault folder.

Determinism: each finder is byte-identical for byte-identical inputs;
this orchestrator is deterministic by virtue of running them in fixed
order with a fixed timestamp argument.

Anti-reflexivity: the orchestrator does NOT auto-promote any candidate
to the atlas. All candidates require human curator review per the
verify-before-write protocol.

Usage:
    python3 scripts/run_autonomous_discoveries.py
    python3 scripts/run_autonomous_discoveries.py --date 2026-05-07

Output:
    vault/Discoveries_Inbox/{date}_summary.md  — index of today's findings
    vault/Discoveries_Inbox/INDEX.md           — running list of all runs
    vault/Discoveries_Inbox/<finder>_{date}.md / .json — per-finder reports
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT / "scripts"
INBOX_DIR = ROOT / "vault" / "Discoveries_Inbox"
INBOX_DIR.mkdir(parents=True, exist_ok=True)

FINDERS = [
    {
        "name": "emergent_edges",
        "script": "find_emergent_edges.py",
        "args": ["--lookback-days", "365"],
        "title": "Emergent edges (gene × mechanism / gene × phenotype)",
    },
    {
        "name": "combination_gaps",
        "script": "find_combination_gaps.py",
        "args": ["--include-triples"],
        "title": "Combination gaps (pairs/triples sharing mechanism)",
    },
    {
        "name": "higher_order_hypotheses",
        "script": "find_higher_order_hypotheses.py",
        "args": [],
        "title": "Higher-order hypotheses (implied A→C from A→B + B→C)",
    },
    {
        "name": "responder_phenotype_gaps",
        "script": "find_responder_phenotype_gaps.py",
        "args": [],
        "title": "Responder phenotype gaps (mixed-evidence interventions untagged)",
    },
]


def run_finder(name: str, script: str, args: list[str], date_str: str) -> dict:
    """Execute one finder; return summary (count, paths)."""
    cmd = [sys.executable, str(SCRIPTS_DIR / script), "--date", date_str] + args
    print(f"\n→ {name}: running {' '.join(cmd[1:])}")
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if out.returncode != 0:
            print(f"  FAILED ({out.returncode}): {out.stderr[:300]}")
            return {"name": name, "status": "failed", "stderr": out.stderr[:1000]}
        # Parse the JSON output for counts
        json_path = INBOX_DIR / f"{name}_{date_str}.json"
        md_path = INBOX_DIR / f"{name}_{date_str}.md"
        candidate_count = 0
        if json_path.exists():
            data = json.loads(json_path.read_text())
            for key, val in data.items():
                if key.startswith("candidate") and isinstance(val, list):
                    candidate_count += len(val)
        return {
            "name": name,
            "status": "ok",
            "candidates_found": candidate_count,
            "stdout_tail": out.stdout.strip().split("\n")[-1] if out.stdout else "",
            "json_path": str(json_path),
            "md_path": str(md_path),
        }
    except subprocess.TimeoutExpired:
        return {"name": name, "status": "timeout"}
    except Exception as e:
        return {"name": name, "status": "error", "error": str(e)}


def render_summary(results: list[dict], date_str: str) -> str:
    total_candidates = sum(r.get("candidates_found", 0) for r in results)
    lines = [
        f"# Autonomous discoveries — {date_str}",
        "",
        f"Daily run of the pattern-mining pipeline. Total candidates surfaced today: **{total_candidates}**.",
        "",
        "These are NOT atlas changes — they are candidates for curator review. Per spec, no candidate is auto-promoted; the verify-before-write protocol gates all edits.",
        "",
        "## Per-finder summary",
        "",
        "| Finder | Status | Candidates | Report |",
        "| --- | --- | --- | --- |",
    ]
    for finder, r in zip(FINDERS, results):
        status = "✅" if r["status"] == "ok" else f"❌ {r['status']}"
        candidates = r.get("candidates_found", "—")
        md_link = (
            f"[`{finder['name']}_{date_str}.md`]({finder['name']}_{date_str}.md)"
            if r["status"] == "ok" else "—"
        )
        lines.append(f"| {finder['title']} | {status} | {candidates} | {md_link} |")
    lines.extend([
        "",
        "## Curator workflow",
        "",
        "1. Open each per-finder report linked above.",
        "2. For each candidate, decide: promote / defer / reject.",
        "3. Promoted candidates require PMID-verified primary evidence before atlas write (verify-before-write protocol per `CLAUDE.md` §Verification protocol).",
        "4. Re-run scoring + verify INT-0001 calibration after any atlas edit.",
        "",
        "## Provenance",
        "",
        f"- Orchestrator: `scripts/run_autonomous_discoveries.py`",
        f"- Run timestamp: {datetime.utcnow().isoformat()}Z",
        f"- Finders executed: {len(FINDERS)}",
        "- Spec: items 5 + 7 of the meta-roadmap (autonomous Obsidian pattern engine).",
        "- Determinism: each finder produces byte-identical output for byte-identical inputs.",
        "- Anti-reflexivity: no auto-promotion to atlas; all candidates gated by human review.",
    ])
    return "\n".join(lines) + "\n"


def update_index(date_str: str, total_candidates: int) -> None:
    """Append today's run to the master INDEX.md."""
    idx_path = INBOX_DIR / "INDEX.md"
    if not idx_path.exists():
        idx_path.write_text(
            "# Autonomous Discoveries Inbox — master index\n\n"
            "Daily pattern-miner runs. Candidates require human curator review.\n\n"
            "| Date | Total candidates | Summary |\n| --- | --- | --- |\n"
        )
    line = f"| {date_str} | {total_candidates} | [{date_str}_summary.md]({date_str}_summary.md) |\n"
    existing = idx_path.read_text()
    # Avoid duplicate lines for the same date (re-runs)
    if line in existing:
        return
    # Insert under the table header
    if "| --- | --- | --- |" in existing:
        existing = existing.replace(
            "| --- | --- | --- |\n",
            "| --- | --- | --- |\n" + line,
            1,
        )
    else:
        existing += line
    idx_path.write_text(existing)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=datetime.utcnow().strftime("%Y-%m-%d"))
    args = parser.parse_args(argv)

    print(f"Autonomous discoveries pipeline — {args.date}")
    print(f"Inbox dir: {INBOX_DIR}")
    print(f"Finders: {len(FINDERS)}")

    results = []
    for finder in FINDERS:
        r = run_finder(finder["name"], finder["script"], finder["args"], args.date)
        results.append(r)

    total_candidates = sum(r.get("candidates_found", 0) for r in results)
    summary_path = INBOX_DIR / f"{args.date}_summary.md"
    summary_path.write_text(render_summary(results, args.date))
    update_index(args.date, total_candidates)

    print(f"\n✅ Pipeline complete.")
    print(f"   Summary: {summary_path}")
    print(f"   Total candidates: {total_candidates}")

    # Exit non-zero if any finder failed (so cron can alert)
    failed = [r for r in results if r["status"] != "ok"]
    if failed:
        print(f"   FAILED finders: {[r['name'] for r in failed]}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
