#!/usr/bin/env python3
"""
autonomous_loop.py
──────────────────
Closed-loop orchestrator for the Causes Atlas. Removes the human from
the steady-state ingestion loop while honoring the verify-before-write
protocol from CLAUDE.md §Verification protocol.

Pipeline:

  1. continuous_ingestion.py --commit
       → queries PubMed for new autism / functional-medicine papers,
         verifies each candidate via esummary, writes verified PMIDs
         to freshness/queue/

  2. drain the verified queue
       → for each queued PMID, call run_ingest.py pmid <id>, which
         appends to sources.csv + evidence_links + node_aliases.
         Idempotent: PMIDs already in the atlas are skipped.

  3. apply_patches_and_score.py  (full scoring + Δ² + reflexivity audit)

  4. build_living_graph.py  → regenerates living_graph.html

  5. (optional) push to hosting  (rsync / gh-pages / vercel deploy)

Modes:

  --once       run one full cycle and exit (default)
  --watch N    loop every N minutes (use with caution; set up launchd
               or cron for true unattended operation, see below)
  --dry-run    don't write — log what each step would do
  --max-papers N  cap candidates per cycle (default 5; safety rail)

Anti-reflexivity defense: the verify gate (continuous_ingestion's
PubMed esummary check) MUST pass for every PMID before run_ingest is
invoked. This script never bypasses verification, even in --dry-run.

Determinism: stable-sorted queue traversal; subprocess calls inherit
deterministic environment from build_living_graph.py.

To make this truly unattended on macOS:

    1. ln -s ~/Autism/scripts/autonomous_loop.py /usr/local/bin/atlas-loop
    2. Place ~/Library/LaunchAgents/com.causes-atlas.loop.plist:

         <?xml version="1.0" encoding="UTF-8"?>
         <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
           "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
         <plist version="1.0">
         <dict>
           <key>Label</key><string>com.causes-atlas.loop</string>
           <key>ProgramArguments</key>
             <array>
               <string>/usr/local/bin/python3</string>
               <string>/Users/Greg/Autism/scripts/autonomous_loop.py</string>
               <string>--once</string>
             </array>
           <key>StartInterval</key><integer>21600</integer>   <!-- 6h -->
           <key>StandardOutPath</key>
             <string>/Users/Greg/Autism/logs/loop.log</string>
           <key>StandardErrorPath</key>
             <string>/Users/Greg/Autism/logs/loop.err</string>
         </dict>
         </plist>

    3. launchctl load ~/Library/LaunchAgents/com.causes-atlas.loop.plist

Six hours is a sensible cadence — PubMed indexes new papers in batches
and rate limits per IP. Anything faster wastes calls without finding
more evidence. The artifact regenerates with whatever landed; visitors
see fresh state on every page load.
"""
from __future__ import annotations
import argparse
import json
import pathlib
import subprocess
import sys
import time

HERE   = pathlib.Path(__file__).resolve().parent
REPO   = HERE.parent
QUEUE  = REPO / "freshness" / "queue"
LOGDIR = REPO / "logs"
LOGDIR.mkdir(exist_ok=True)

def log(msg: str) -> None:
    ts = time.strftime("%Y-%m-%dT%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)

def run(cmd: list[str], dry: bool, label: str) -> int:
    log(f"→ {label}: {' '.join(cmd)}")
    if dry:
        log(f"  (dry-run, skipped)")
        return 0
    r = subprocess.run(cmd, cwd=REPO)
    if r.returncode != 0:
        log(f"  ⚠ {label} exit {r.returncode}")
    return r.returncode

def step_discover(dry: bool) -> int:
    """Run continuous_ingestion to discover + verify candidates."""
    return run(
        ["python3", "scripts/continuous_ingestion.py"] + ([] if dry else ["--commit"]),
        dry=False,  # continuous_ingestion handles its own --commit flag
        label="discover (PubMed → freshness/queue)",
    )

def step_drain_queue(dry: bool, max_papers: int) -> int:
    """For each verified PMID in the queue, run run_ingest.py pmid <id>."""
    if not QUEUE.exists():
        log(f"  no queue directory at {QUEUE} — nothing to drain")
        return 0
    queued = sorted(QUEUE.glob("*.json"))[:max_papers]
    if not queued:
        log("  queue is empty — nothing to drain this cycle")
        return 0
    log(f"  draining {len(queued)} verified candidate(s)")
    for q in queued:
        try:
            meta = json.loads(q.read_text())
            pmid = str(meta.get("pmid") or q.stem)
        except Exception as e:
            log(f"  ⚠ couldn't parse {q.name}: {e}")
            continue
        rc = run(
            ["python3", "run_ingest.py", "pmid", pmid],
            dry=dry,
            label=f"ingest PMID {pmid}",
        )
        if rc == 0 and not dry:
            # move out of queue → archive on success
            archive = QUEUE.parent / "archive"
            archive.mkdir(exist_ok=True)
            q.rename(archive / q.name)
    return 0

def step_rescore(dry: bool) -> int:
    """Run the canonical scoring + Δ² pipeline."""
    return run(
        ["python3", "apply_patches_and_score.py"],
        dry=dry,
        label="rescore + Δ²",
    )

def step_rebuild_visual(dry: bool) -> int:
    """Regenerate living_graph.html from the updated CSVs."""
    return run(
        ["python3", "scripts/build_living_graph.py"],
        dry=dry,
        label="rebuild living_graph.html",
    )

def step_deploy(dry: bool) -> int:
    """Optional push to hosting. No-op until configured.

    To enable: set ATLAS_DEPLOY_CMD env var, e.g.:
        export ATLAS_DEPLOY_CMD="vercel --prod /Users/Greg/Autism/living_graph.html"
    """
    import os
    cmd = os.environ.get("ATLAS_DEPLOY_CMD")
    if not cmd:
        log("  ATLAS_DEPLOY_CMD not set — skipping deploy step")
        return 0
    return run(cmd.split(), dry=dry, label="deploy")

def one_cycle(args) -> int:
    log("─── cycle start ───")
    rc = step_discover(args.dry_run)
    if rc != 0: log("discovery failed; continuing to drain whatever's queued")
    rc = step_drain_queue(args.dry_run, args.max_papers)
    if rc != 0: log("queue drain had errors; continuing")
    rc = step_rescore(args.dry_run)
    if rc != 0:
        log("⚠ rescore failed — calibration regression likely, ABORTING")
        return rc
    rc = step_rebuild_visual(args.dry_run)
    if rc != 0:
        log("⚠ visual rebuild failed")
        return rc
    rc = step_deploy(args.dry_run)
    log("─── cycle complete ───")
    return rc

def main():
    ap = argparse.ArgumentParser(description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--once",  action="store_true",
                    help="run one cycle and exit (default)")
    ap.add_argument("--watch", type=int, metavar="MIN", default=0,
                    help="loop forever, sleeping N minutes between cycles")
    ap.add_argument("--dry-run", action="store_true",
                    help="log what would happen without writing")
    ap.add_argument("--max-papers", type=int, default=5,
                    help="cap candidates ingested per cycle (default 5)")
    args = ap.parse_args()

    if args.watch:
        log(f"watch mode: cycling every {args.watch} minutes")
        while True:
            try:
                one_cycle(args)
            except KeyboardInterrupt:
                log("interrupted, exiting"); return 0
            except Exception as e:
                log(f"⚠ uncaught: {e}")
            log(f"sleeping {args.watch}m before next cycle")
            time.sleep(args.watch * 60)
    else:
        return one_cycle(args)

if __name__ == "__main__":
    sys.exit(main() or 0)
