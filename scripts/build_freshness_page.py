#!/usr/bin/env python3
"""
build_freshness_page.py

Aggregates freshness/log/*.json + freshness/queue/*.json + sources.csv into a
single public freshness.json that the UI / public freshness page reads. This
is the "your atlas is stale" defense: anyone visiting /freshness sees the
live ingestion log.

Output:
  freshness/freshness.json
"""
from __future__ import annotations
import csv
import json
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ATLAS_DIR = REPO / "v2.0_scored"
FRESHNESS_DIR = REPO / "freshness"
QUEUE_DIR = FRESHNESS_DIR / "queue"
LOG_DIR = FRESHNESS_DIR / "log"
OUT_PATH = FRESHNESS_DIR / "freshness.json"


def main():
    FRESHNESS_DIR.mkdir(parents=True, exist_ok=True)

    # Atlas pmid count — sources.csv uses external_id when platform == pubmed
    atlas_pmids = set()
    sources_csv = ATLAS_DIR / "sources.csv"
    if sources_csv.exists():
        with open(sources_csv, encoding="utf-8", newline="") as f:
            for r in csv.DictReader(f):
                if (r.get("platform") or "").lower() == "pubmed":
                    p = (r.get("external_id") or "").strip()
                    if p.isdigit():
                        atlas_pmids.add(p)

    # Queue
    queue_files = sorted(QUEUE_DIR.glob("*.json")) if QUEUE_DIR.exists() else []
    queue_records = []
    for q in queue_files:
        try:
            queue_records.append(json.loads(q.read_text()))
        except Exception:
            continue
    # Sort by pubdate descending (most recent first); fallback to PMID
    def sort_key(r):
        return (r.get("pubdate") or "", r.get("pmid") or "")
    queue_records.sort(key=sort_key, reverse=True)

    # Daily log
    log_files = sorted(LOG_DIR.glob("*.json")) if LOG_DIR.exists() else []
    daily_logs = []
    for f in log_files[-30:]:  # last 30 days
        try:
            daily_logs.append(json.loads(f.read_text()))
        except Exception:
            continue

    out = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "atlas_pmid_count": len(atlas_pmids),
        "queue_size": len(queue_records),
        "last_30_daily_logs": daily_logs,
        "queue_preview": [
            {
                "pmid": r.get("pmid"),
                "title": (r.get("title") or "")[:160],
                "journal": r.get("journal"),
                "pubdate": r.get("pubdate"),
                "first_author": r.get("first_author"),
                "matched_queries_count": len(r.get("matched_queries", []) or []),
            }
            for r in queue_records[:50]
        ],
    }

    OUT_PATH.write_text(json.dumps(out, indent=2, sort_keys=True))
    print(f"Wrote freshness.json:")
    print(f"  atlas_pmid_count: {out['atlas_pmid_count']}")
    print(f"  queue_size: {out['queue_size']}")
    print(f"  daily_logs: {len(daily_logs)}")


if __name__ == "__main__":
    main()
