#!/usr/bin/env python3
"""
scripts/intake/intake_orchestrator.py — single entry point that runs all
intake scanners and writes a unified daily summary.

Runs (in order):
  1. pubmed_rss_scanner.py            (always; works in CI + locally)
  2. browser_social_scanner.py        (local only; skipped if Playwright
                                       missing)

All candidates land in vault/Discoveries_Inbox/. Per CLAUDE.md Sec.24,
nothing is auto-promoted to the canonical atlas — curator review +
PMID re-verification gate all writes.

Run command:
  python3 scripts/intake/intake_orchestrator.py
  python3 scripts/intake/intake_orchestrator.py --skip-social
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

_CANDIDATE_REPOS = [
    Path("/Users/Greg/Autism"),
    Path("/sessions/jolly-determined-darwin/mnt/Autism"),
]
REPO = next((p for p in _CANDIDATE_REPOS if p.exists()), _CANDIDATE_REPOS[0])
INBOX = REPO / "vault" / "Discoveries_Inbox"
SCANNERS = {
    "pubmed":  REPO / "scripts/intake/pubmed_rss_scanner.py",
    "social":  REPO / "scripts/intake/browser_social_scanner.py",
}


def run_scanner(name: str, args: list[str]) -> dict:
    """Run a scanner subprocess and capture exit status."""
    script = SCANNERS[name]
    print(f"\n=== {name} scanner ===")
    print(f"  {script}")
    try:
        result = subprocess.run(
            [sys.executable, str(script), *args],
            cwd=str(REPO),
            capture_output=True,
            text=True,
            timeout=300,
        )
        print(result.stdout[-2000:] if result.stdout else "(no stdout)")
        if result.returncode != 0:
            print(f"  Exit code: {result.returncode}")
            if result.stderr:
                print(f"  stderr: {result.stderr[-500:]}")
        return {
            "scanner": name,
            "exit_code": result.returncode,
            "stdout_tail": result.stdout[-500:] if result.stdout else "",
            "stderr_tail": result.stderr[-500:] if result.stderr else "",
        }
    except subprocess.TimeoutExpired:
        print(f"  TIMEOUT after 300s")
        return {"scanner": name, "exit_code": -1, "error": "timeout"}
    except Exception as e:
        print(f"  ERROR: {e}")
        return {"scanner": name, "exit_code": -2, "error": str(e)}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-social", action="store_true",
                    help="Skip the browser-based Twitter/Reddit scanner "
                         "(useful in CI where Playwright is unavailable)")
    ap.add_argument("--max-per-query", type=int, default=10)
    args = ap.parse_args(argv)

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    print(f"Intake orchestrator — {today}")
    print(f"Repo: {REPO}")
    print(f"Inbox: {INBOX}")

    results = []
    results.append(run_scanner("pubmed", [
        "--max-per-query", str(args.max_per_query),
    ]))

    if not args.skip_social:
        results.append(run_scanner("social", []))

    # Write orchestrator summary
    summary = {
        "date": today,
        "scanners": results,
    }
    INBOX.mkdir(parents=True, exist_ok=True)
    summary_path = INBOX / f"intake_summary_{today}.json"
    summary_path.write_text(json.dumps(summary, indent=2))
    print(f"\nWrote {summary_path}")

    any_failed = any(r.get("exit_code", 0) != 0 for r in results)
    return 0 if not any_failed else 1


if __name__ == "__main__":
    sys.exit(main())
