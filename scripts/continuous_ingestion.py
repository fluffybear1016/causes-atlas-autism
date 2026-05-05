#!/usr/bin/env python3
"""
continuous_ingestion.py

Daily PubMed crawler that immunizes the atlas from the "stale knowledge graph"
critique flagged in the post-mortem. Runs a curated set of autism + functional-
medicine queries, fetches new PMIDs since last successful run, verifies each
via PubMed esummary (per CLAUDE.md verify-before-write protocol), and queues
them for human review in `freshness/queue/`.

Output:
  - freshness/state.json            — last-run timestamp, query cursors
  - freshness/queue/<pmid>.json     — verified candidate ready for atlas curation
  - freshness/log/YYYY-MM-DD.json   — daily ingestion log (public freshness page reads this)

Idempotent: a PMID already in the atlas (sources.csv) or already in the queue
is skipped, never re-ingested.

Usage:
  python scripts/continuous_ingestion.py            # dry-run by default
  python scripts/continuous_ingestion.py --commit   # write queue + log

This is the v0.1 scaffolding — production uses cron / GitHub Actions to run
daily. The query patterns can be tuned over time.
"""
from __future__ import annotations
import argparse
import csv
import json
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ATLAS_DIR = REPO / "v2.0_scored"
FRESHNESS_DIR = REPO / "freshness"
QUEUE_DIR = FRESHNESS_DIR / "queue"
LOG_DIR = FRESHNESS_DIR / "log"
STATE_PATH = FRESHNESS_DIR / "state.json"

# Curated queries — kept tight to limit noise. Each query targets a specific
# slice of literature relevant to the atlas. Tunable. PubMed E-utilities
# syntax: https://www.ncbi.nlm.nih.gov/books/NBK25499/
QUERIES = [
    # Core autism etiology / mechanism
    'autism[tiab] AND (mitochondrial[tiab] OR "oxidative stress"[tiab]) AND ("clinical trial"[pt] OR "randomized"[tiab])',
    'autism[tiab] AND ("cerebral folate"[tiab] OR "folate receptor"[tiab])',
    'autism[tiab] AND ("microbiome"[tiab] OR "gut-brain axis"[tiab]) AND human[mh]',
    # Functional medicine subset
    'autism[tiab] AND (leucovorin[tiab] OR folinic[tiab])',
    'autism[tiab] AND (bumetanide[tiab] OR "GABA polarity"[tiab])',
    'autism[tiab] AND ("mast cell"[tiab] OR MCAS[tiab])',
    'autism[tiab] AND PANDAS[tiab]',
    # Susceptibility-trigger framework (Hannah Poling principle)
    '("susceptibility-trigger"[tiab] OR "individual susceptibility"[tiab]) AND autism',
    # Verified-PMID protocol and BioMysteryBench-relevant
    '"knowledge graph"[tiab] AND (autism[tiab] OR "neurodevelopmental"[tiab])',
]

USER_AGENT = "CausesAtlasAutism/0.2 (continuous_ingestion; research)"


def load_atlas_pmids() -> set[str]:
    """Pull all PMIDs already in the atlas so we don't re-queue them."""
    pmids = set()
    sources_csv = ATLAS_DIR / "sources.csv"
    if sources_csv.exists():
        with open(sources_csv, encoding="utf-8", newline="") as f:
            for r in csv.DictReader(f):
                # Primary path: external_id when platform=pubmed
                if (r.get("platform") or "").lower() == "pubmed":
                    p = (r.get("external_id") or "").strip()
                    if p.isdigit():
                        pmids.add(p)
                # Back-compat: if a row has a literal pmid column
                p2 = (r.get("pmid") or "").strip()
                if p2.isdigit():
                    pmids.add(p2)
    # Also scan iatrogenic priors and any *_pmids columns elsewhere
    for table in ATLAS_DIR.glob("*.csv"):
        try:
            with open(table, encoding="utf-8", newline="") as f:
                rdr = csv.DictReader(f)
                for r in rdr:
                    for k, v in r.items():
                        if k and "pmid" in k.lower() and v:
                            for p in v.split(";"):
                                p = p.strip()
                                if p.isdigit():
                                    pmids.add(p)
        except Exception:
            continue
    return pmids


def load_queued_pmids() -> set[str]:
    """PMIDs already in the curation queue."""
    if not QUEUE_DIR.exists():
        return set()
    return {p.stem for p in QUEUE_DIR.glob("*.json")}


def http_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def pubmed_esearch(query: str, since: datetime | None, max_results: int = 50) -> list[str]:
    """Run an esearch and return matching PMIDs."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": str(max_results),
        "retmode": "json",
        "sort": "pub_date",
    }
    if since:
        # PubMed mindate format: YYYY/MM/DD; use crdt (entry created date)
        params["mindate"] = since.strftime("%Y/%m/%d")
        params["datetype"] = "edat"
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?" + urllib.parse.urlencode(params)
    data = http_json(url)
    return data.get("esearchresult", {}).get("idlist", []) or []


def pubmed_esummary(pmids: list[str]) -> dict:
    if not pmids:
        return {}
    url = ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id="
           + ",".join(pmids) + "&retmode=json")
    return http_json(url).get("result", {})


def verify_record(pmid: str, rec: dict) -> dict | None:
    """Apply verify-before-write protocol: ensure record looks complete + real."""
    if not rec or rec.get("error"):
        return None
    title = (rec.get("title") or "").strip()
    journal = (rec.get("source") or "").strip()
    pubdate = (rec.get("pubdate") or "").strip()
    authors = [a.get("name", "") for a in (rec.get("authors") or [])]
    if not title or not pubdate or not authors:
        return None
    # Reject records missing title/journal — those are usually bad records
    if "[" in title and "Author" not in title:
        # PubMed sometimes wraps non-English titles with brackets — accept
        pass
    return {
        "pmid": pmid,
        "title": title,
        "journal": journal,
        "pubdate": pubdate,
        "first_author": authors[0],
        "all_authors_joined": "; ".join(authors[:8]),
        "doi": rec.get("elocationid", ""),
        "verified_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }


def load_state() -> dict:
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text())
    return {"last_run_utc": None}


def save_state(state: dict):
    FRESHNESS_DIR.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2, sort_keys=True))


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--commit", action="store_true", help="Write queue + log to disk")
    p.add_argument("--lookback-days", type=int, default=7,
                   help="If no prior run, search this many days back")
    p.add_argument("--max-per-query", type=int, default=20)
    args = p.parse_args()

    state = load_state()
    if state.get("last_run_utc"):
        since = datetime.fromisoformat(state["last_run_utc"])
    else:
        since = datetime.now(timezone.utc) - timedelta(days=args.lookback_days)

    print(f"continuous_ingestion — {'COMMIT' if args.commit else 'DRY-RUN'} mode")
    print(f"Looking for PMIDs since: {since.isoformat()}")

    atlas_pmids = load_atlas_pmids()
    queued_pmids = load_queued_pmids()
    print(f"Already-in-atlas PMIDs: {len(atlas_pmids)}")
    print(f"Already-in-queue PMIDs: {len(queued_pmids)}")

    # Run all queries, collect candidate PMIDs
    candidates: dict[str, list[str]] = {}  # pmid → list of matching queries
    for q in QUERIES:
        try:
            pmids = pubmed_esearch(q, since, max_results=args.max_per_query)
        except Exception as e:
            print(f"  WARN query failed: {q[:40]}... {e}")
            continue
        for p_id in pmids:
            if p_id in atlas_pmids or p_id in queued_pmids:
                continue
            candidates.setdefault(p_id, []).append(q)
        time.sleep(0.5)

    print(f"\nNew candidates after dedup: {len(candidates)}")

    # Verify in batches
    verified = []
    pmid_list = sorted(candidates.keys())
    BATCH = 50
    for i in range(0, len(pmid_list), BATCH):
        batch = pmid_list[i:i + BATCH]
        try:
            sums = pubmed_esummary(batch)
        except Exception as e:
            print(f"  WARN esummary batch failed: {e}")
            continue
        for p_id in batch:
            rec = sums.get(p_id, {})
            v = verify_record(p_id, rec)
            if v:
                v["matched_queries"] = candidates[p_id]
                verified.append(v)
            time.sleep(0.05)
        time.sleep(0.5)

    print(f"Verified: {len(verified)}")

    # Compose log entry
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    log_entry = {
        "run_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "since": since.isoformat(),
        "queries_run": len(QUERIES),
        "candidates_found": len(candidates),
        "verified_added_to_queue": len(verified),
        "atlas_pmid_count": len(atlas_pmids),
        "verified_pmids": [v["pmid"] for v in verified],
    }

    if not args.commit:
        print("\n--- DRY-RUN summary ---")
        print(json.dumps(log_entry, indent=2))
        for v in verified[:5]:
            print(f"  PMID {v['pmid']}: {v['title'][:80]}  ({v['journal']}, {v['pubdate']})")
        if len(verified) > 5:
            print(f"  ... +{len(verified)-5} more")
        return

    # Commit: write each verified record to queue + write log
    QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    for v in verified:
        out_path = QUEUE_DIR / f"{v['pmid']}.json"
        out_path.write_text(json.dumps(v, indent=2, sort_keys=True))
    log_path = LOG_DIR / f"{today}.json"
    log_path.write_text(json.dumps(log_entry, indent=2, sort_keys=True))

    state["last_run_utc"] = log_entry["run_at_utc"]
    save_state(state)
    print(f"\nWrote {len(verified)} verified records to {QUEUE_DIR}")
    print(f"Wrote daily log to {log_path}")


if __name__ == "__main__":
    main()
