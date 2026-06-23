#!/usr/bin/env python3
"""
run_all.py
──────────
Cadence-aware orchestrator for the SFARI integration suite. Designed to be
invoked once a day from autonomous_loop.py; each sub-script runs only on
its appropriate cadence so we don't hammer SFARI's servers.

Cadences:
  - integrate_genes.py        QUARTERLY     (~90 days since last run)
  - integrate_publications.py WEEKLY        (~7 days since last run)
  - integrate_rss.py          DAILY         (every invocation)
  - integrate_cohorts.py      QUARTERLY     (community list rarely changes)

State is tracked in freshness/sfari/cadence_state.json so cron / launchd
can call this every day and the right things happen at the right time.

Anti-reflexivity & verification: every PMID surfaced lands in the
verified-queue gate per CLAUDE.md §24; nothing auto-promotes to
v2.0_scored/ without human review. The single exception is the
autonomous_loop drain of the queue, which calls run_ingest.py with
PubMed esummary verification at each step.

Usage:
  python3 scripts/sfari/run_all.py                 # follow cadence
  python3 scripts/sfari/run_all.py --force-all     # run everything now
  python3 scripts/sfari/run_all.py --force genes   # force one script
  python3 scripts/sfari/run_all.py --dry-run       # log without committing
"""
from __future__ import annotations
import argparse, json, pathlib, subprocess, sys
from datetime import datetime, timezone, timedelta

HERE   = pathlib.Path(__file__).resolve().parent
REPO   = HERE.parent.parent
STATE  = REPO / "freshness" / "sfari" / "cadence_state.json"

CADENCES = {
    "genes":        {"interval_days": 90, "script": HERE / "integrate_genes.py"},
    "publications": {"interval_days":  7, "script": HERE / "integrate_publications.py"},
    "rss":          {"interval_days":  1, "script": HERE / "integrate_rss.py"},
    "cohorts":      {"interval_days": 90, "script": HERE / "integrate_cohorts.py"},
}

def log(msg: str) -> None:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"[{ts}] sfari/run_all  {msg}", flush=True)

def load_state() -> dict:
    if STATE.exists():
        try: return json.loads(STATE.read_text())
        except: pass
    return {}

def save_state(state: dict) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, indent=2))

def needs_run(name: str, state: dict) -> bool:
    last = state.get(name, {}).get("last_run_utc")
    if not last: return True
    try:
        last_dt = datetime.fromisoformat(last.replace("Z", "+00:00"))
    except ValueError:
        return True
    interval = timedelta(days=CADENCES[name]["interval_days"])
    return datetime.now(timezone.utc) - last_dt >= interval

def run_one(name: str, dry: bool) -> int:
    cfg = CADENCES[name]
    cmd = ["python3", str(cfg["script"])]
    if not dry:
        cmd.append("--commit")
    log(f"→ running {name}: {' '.join(cmd[-3:])}")
    r = subprocess.run(cmd, cwd=REPO)
    if r.returncode != 0:
        log(f"⚠ {name} exit {r.returncode}")
    return r.returncode

def main():
    ap = argparse.ArgumentParser(description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run",   action="store_true")
    ap.add_argument("--force-all", action="store_true",
                    help="ignore cadence; run every script")
    ap.add_argument("--force",     choices=list(CADENCES.keys()),
                    help="ignore cadence for one script")
    args = ap.parse_args()

    state = load_state()
    log(f"state: {json.dumps({k: state.get(k, {}).get('last_run_utc') for k in CADENCES}, default=str)}")

    ran_any = False
    for name in ["genes", "cohorts", "publications", "rss"]:    # stable order
        should_run = (
            args.force_all
            or args.force == name
            or needs_run(name, state)
        )
        if not should_run:
            log(f"  skip {name} (not due — last {state.get(name, {}).get('last_run_utc')})")
            continue
        rc = run_one(name, args.dry_run)
        ran_any = True
        if rc == 0 and not args.dry_run:
            state[name] = {
                "last_run_utc": datetime.now(timezone.utc).isoformat(),
                "exit_code": rc,
            }

    if not args.dry_run:
        save_state(state)

    if not ran_any:
        log("nothing was due. next run will check again tomorrow.")
    return 0

if __name__ == "__main__":
    sys.exit(main() or 0)
