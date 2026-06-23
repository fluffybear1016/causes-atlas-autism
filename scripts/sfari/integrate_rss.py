#!/usr/bin/env python3
"""
integrate_sfari_rss.py
──────────────────────
Daily ingestion of SFARI + The Transmitter RSS feeds, with PMID extraction
and verification per CLAUDE.md §24. Designed to run unattended on cron.

Feeds (verified live 2026-06-23):
  Transmitter:  https://www.thetransmitter.org/feed/    (sitewide)
  SFARI direct: https://www.sfari.org/feed/             (announcements)

The Transmitter rebranded from Spectrum News in 2024; the autism vertical
lives at /spectrum/ — we filter the sitewide feed for that URL substring.

What this script does:
  1. Polls each RSS feed
  2. Identifies new items not seen before (tracked by GUID, not URL — slugs
     change on WordPress edits but GUIDs are stable)
  3. For each new item: fetches the article body, extracts PMIDs via regex
  4. For each PMID: §24 verify via PubMed esummary
  5. Writes verified PMIDs to freshness/queue/ for autonomous_loop drain
  6. Logs the article itself to freshness/log/transmitter/ for trail

Anti-reflexivity defense: this script ONLY surfaces verified primary
literature — Transmitter coverage is journalism (tier 5 per CLAUDE.md §2),
the PMID it references is the primary source we actually want. Transmitter
title is preserved as metadata but doesn't get its own sources row.

Usage:
  python3 scripts/sfari/integrate_rss.py                 # dry-run
  python3 scripts/sfari/integrate_rss.py --commit        # write to queue
  python3 scripts/sfari/integrate_rss.py --feed transmitter
  python3 scripts/sfari/integrate_rss.py --feed sfari
  python3 scripts/sfari/integrate_rss.py --since 2026-06-01
"""
from __future__ import annotations
import argparse, csv, json, pathlib, re, sys, time
import urllib.request, urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

HERE        = pathlib.Path(__file__).resolve().parent
REPO        = HERE.parent.parent
SOURCES     = REPO / "v2.0_scored" / "sources.csv"
FRESH_QUEUE = REPO / "freshness" / "queue"
FRESH_LOG   = REPO / "freshness" / "log" / "transmitter"
STATE       = REPO / "freshness" / "sfari" / "rss_state.json"

FEEDS = {
    "transmitter": {
        "url":     "https://www.thetransmitter.org/feed/",
        "filter":  "/spectrum/",     # autism vertical only
        "source_tag": "transmitter_spectrum",
    },
    "sfari": {
        "url":     "https://www.sfari.org/feed/",
        "filter":  None,             # all SFARI direct news
        "source_tag": "sfari_news",
    },
}

PMID_PATTERNS = [
    re.compile(r"pubmed\.ncbi\.nlm\.nih\.gov/(\d{7,9})", re.IGNORECASE),
    re.compile(r"PubMed[:\s]+(\d{7,9})", re.IGNORECASE),
    re.compile(r"PMID[:\s]+(\d{7,9})", re.IGNORECASE),
]
DOI_RE = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b", re.IGNORECASE)
PUBMED_ESUMMARY = ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
                   "?db=pubmed&retmode=json&id={pmid}")
PUBMED_ESEARCH = ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
                  "?db=pubmed&retmode=json&term={term}")

UA = {"User-Agent": "CausesAtlas/0.1 (rss-integration)"}

def log(msg: str) -> None:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"[{ts}] {msg}", flush=True)

def fetch(url: str, sleep_s: float = 0.4) -> str:
    time.sleep(sleep_s)
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        log(f"⚠ HTTP {e.code} {url[:80]}")
        return ""
    except (urllib.error.URLError, TimeoutError) as e:
        log(f"⚠ {e} {url[:80]}")
        return ""

def load_state() -> dict:
    if STATE.exists():
        try:    return json.loads(STATE.read_text())
        except: pass
    return {"seen_guids": []}

def save_state(state: dict) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    # Cap guid history at 5,000 to keep state file bounded
    state["seen_guids"] = state.get("seen_guids", [])[-5000:]
    STATE.write_text(json.dumps(state, indent=2))

def parse_rss(xml_text: str) -> list[dict]:
    """Parse a standard RSS 2.0 feed. Returns items with guid/link/title/pubdate/desc."""
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as e:
        log(f"⚠ RSS parse error: {e}")
        return []
    ns = {"content": "http://purl.org/rss/1.0/modules/content/"}
    items = []
    for item in root.iter("item"):
        guid_el = item.find("guid")
        link_el = item.find("link")
        title_el = item.find("title")
        date_el = item.find("pubDate")
        desc_el = item.find("description")
        content_el = item.find("content:encoded", ns)
        items.append({
            "guid":    (guid_el.text or "").strip() if guid_el is not None else "",
            "link":    (link_el.text or "").strip() if link_el is not None else "",
            "title":   (title_el.text or "").strip() if title_el is not None else "",
            "pubdate": (date_el.text or "").strip() if date_el is not None else "",
            "desc":    (desc_el.text or "")        if desc_el is not None else "",
            "content": (content_el.text or "")     if content_el is not None else "",
        })
    return items

def filter_items(items: list[dict], substr_filter: str | None,
                 since: datetime | None) -> list[dict]:
    out = []
    for it in items:
        if substr_filter and substr_filter not in it["link"]:
            continue
        if since and it["pubdate"]:
            try:
                # RFC 822 date e.g. "Mon, 22 Jun 2026 14:30:00 +0000"
                from email.utils import parsedate_to_datetime
                d = parsedate_to_datetime(it["pubdate"])
                if d < since:
                    continue
            except Exception:
                pass
        out.append(it)
    return out

def extract_pmids_from_html(html_or_text: str) -> list[str]:
    seen = set()
    pmids = []
    for pat in PMID_PATTERNS:
        for m in pat.finditer(html_or_text):
            p = m.group(1)
            if p not in seen:
                seen.add(p); pmids.append(p)
    return pmids

def doi_to_pmid(doi: str) -> str | None:
    """Best-effort DOI → PMID via PubMed esearch."""
    import urllib.parse as up
    term = up.quote(f'{doi}[doi]')
    body = fetch(PUBMED_ESEARCH.format(term=term), sleep_s=0.34)
    if not body: return None
    try:
        d = json.loads(body)
        ids = d.get("esearchresult", {}).get("idlist") or []
        return ids[0] if ids else None
    except json.JSONDecodeError:
        return None

def verify_pmid(pmid: str) -> dict | None:
    body = fetch(PUBMED_ESUMMARY.format(pmid=pmid), sleep_s=0.34)
    if not body: return None
    try:
        d = json.loads(body)
        rec = d.get("result", {}).get(pmid)
        if not rec or rec.get("uid") != pmid:
            return None
        authors = rec.get("authors", [])
        return {
            "pmid": pmid,
            "title": (rec.get("title") or "").strip(),
            "first_author": (authors[0].get("name") if authors else ""),
            "journal": rec.get("source", ""),
            "year": (rec.get("pubdate", "") or "")[:4],
            "verified": True,
            "verified_at": datetime.now(timezone.utc).isoformat(),
        }
    except (json.JSONDecodeError, KeyError):
        return None

def existing_pmids() -> set[str]:
    if not SOURCES.exists(): return set()
    out = set()
    with SOURCES.open() as f:
        for r in csv.DictReader(f):
            p = (r.get("pmid") or "").strip()
            if p and p.isdigit(): out.add(p)
    return out

def queued_pmids() -> set[str]:
    if not FRESH_QUEUE.exists(): return set()
    return {p.stem for p in FRESH_QUEUE.glob("*.json")}

def write_article_log(feed_key: str, item: dict, pmids: list[dict]) -> None:
    FRESH_LOG.mkdir(parents=True, exist_ok=True)
    date_tag = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    fp = FRESH_LOG / f"{date_tag}_{feed_key}_articles.jsonl"
    rec = {
        "ingested_at": datetime.now(timezone.utc).isoformat(),
        "feed":   feed_key,
        "guid":   item["guid"],
        "link":   item["link"],
        "title":  item["title"],
        "pubdate": item["pubdate"],
        "verified_pmids": [p["pmid"] for p in pmids],
    }
    with fp.open("a") as f:
        f.write(json.dumps(rec) + "\n")

def write_queue_entry(meta: dict, source_tag: str, via_article: dict) -> pathlib.Path:
    FRESH_QUEUE.mkdir(parents=True, exist_ok=True)
    fp = FRESH_QUEUE / f"{meta['pmid']}.json"
    out = dict(meta)
    out["source_tag"]   = source_tag
    out["via_article"]  = {"title": via_article.get("title", ""),
                           "link":  via_article.get("link", ""),
                           "feed":  via_article.get("feed", "")}
    fp.write_text(json.dumps(out, indent=2))
    return fp

def main():
    ap = argparse.ArgumentParser(description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--commit", action="store_true")
    ap.add_argument("--feed",   choices=list(FEEDS.keys()) + ["all"], default="all")
    ap.add_argument("--since",  type=str, default=None,
                    help="ISO date — only ingest articles newer than this")
    ap.add_argument("--max-items",   type=int, default=30,
                    help="cap on RSS items processed per feed (safety)")
    ap.add_argument("--max-verify",  type=int, default=20,
                    help="cap on PMID verifications per run")
    args = ap.parse_args()

    state = load_state()
    seen_guids = set(state.get("seen_guids", []))
    since = None
    if args.since:
        try:
            since = datetime.fromisoformat(args.since).replace(tzinfo=timezone.utc)
        except ValueError:
            log(f"⚠ bad --since date {args.since}, ignoring")

    feeds_to_run = list(FEEDS.keys()) if args.feed == "all" else [args.feed]
    have_sources = existing_pmids()
    have_queue   = queued_pmids()
    log(f"atlas has {len(have_sources):,} PMIDs in sources + {len(have_queue)} in queue")

    total_verified = 0
    for feed_key in feeds_to_run:
        feed = FEEDS[feed_key]
        log(f"── feed: {feed_key}  ({feed['url']})")
        xml_text = fetch(feed["url"], sleep_s=0.3)
        if not xml_text:
            log("  ⚠ empty feed, skipping")
            continue
        items = parse_rss(xml_text)
        log(f"  parsed {len(items)} items")
        items = filter_items(items, feed["filter"], since)
        log(f"  {len(items)} after filter ({feed['filter'] or 'no filter'})")
        items = items[: args.max_items]

        for it in items:
            if not it["guid"]:
                continue
            if it["guid"] in seen_guids:
                continue
            seen_guids.add(it["guid"])

            # Fetch full article body if we don't have :encoded
            body = it.get("content") or it.get("desc") or ""
            if "pubmed" not in body.lower() and "pmid" not in body.lower() and it["link"]:
                article_html = fetch(it["link"], sleep_s=0.5)
                body = body + "\n\n" + article_html

            pmids = extract_pmids_from_html(body)
            verified_metas = []
            for pmid in pmids:
                if total_verified >= args.max_verify:
                    break
                if pmid in have_sources or pmid in have_queue:
                    continue
                meta = verify_pmid(pmid)
                if not meta:
                    continue
                verified_metas.append(meta)
                total_verified += 1

            if not verified_metas:
                continue

            log(f"  + {it['title'][:60]}  → {len(verified_metas)} verified PMIDs")
            if args.commit:
                via = dict(it); via["feed"] = feed_key
                for m in verified_metas:
                    write_queue_entry(m, feed["source_tag"], via)
                write_article_log(feed_key, it, verified_metas)

    if args.commit:
        state["seen_guids"] = sorted(seen_guids)
        save_state(state)
        log(f"✓ state saved ({len(seen_guids)} guids tracked)")
    log(f"total verified PMIDs: {total_verified}")
    if not args.commit:
        log("dry-run: pass --commit to persist queue + state")
    return 0

if __name__ == "__main__":
    sys.exit(main() or 0)
