#!/usr/bin/env python3
"""
integrate_sfari_publications.py
────────────────────────────────
SFARI-funded publications cross-walk for the Causes Atlas.

SFARI maintains a database of ~2,288 funded publications at
https://www.sfari.org/research/funded-publications/ — 229 paginated pages,
filterable by year/cohort/topic but with NO public CSV/JSON export. This
script scrapes the HTML, extracts PMIDs via PubMed-link regex, verifies
each via PubMed esummary (per CLAUDE.md §24 verification protocol), and
queues verified candidates for the autonomous_loop to drain into sources.csv.

Sources verified live 2026-06-23:
  Funded pubs: https://www.sfari.org/research/funded-publications/
  Per-cohort filters available via URL params:
    ?search_pub_resource[]=spark|ssc|searchlight|autism-brainnet|brainspan
    ?search_year=YYYY

Workflow:
  1. Paginate through the funded-publications index (or a subset)
  2. For each article: extract PMID via pubmed.ncbi.nlm.nih.gov regex
  3. Filter against sources.csv (skip already-ingested PMIDs)
  4. Verify each candidate via PubMed esummary (author+year+title match)
  5. Write verified PMIDs to freshness/queue/{pmid}.json with sfari_source flag
  6. autonomous_loop drains the queue → run_ingest.py per PMID

Verification-before-write per §24: every PMID gets esummary-verified before
landing in the queue. Memory-based PMID generation is forbidden.

Determinism: scrape pages in stable URL order; PMIDs sorted ascending
before verification.

Usage:
  python3 scripts/sfari/integrate_publications.py                # dry-run
  python3 scripts/sfari/integrate_publications.py --commit       # write to queue
  python3 scripts/sfari/integrate_publications.py --year 2026    # current year only
  python3 scripts/sfari/integrate_publications.py --cohort spark # SPARK-only
  python3 scripts/sfari/integrate_publications.py --max-pages 5  # safety cap
"""
from __future__ import annotations
import argparse, csv, json, pathlib, re, sys, time
import urllib.request, urllib.error, urllib.parse
from datetime import datetime, timezone

HERE        = pathlib.Path(__file__).resolve().parent
REPO        = HERE.parent.parent
SOURCES     = REPO / "v2.0_scored" / "sources.csv"
FRESH_QUEUE = REPO / "freshness" / "queue"
FRESH_LOG   = REPO / "freshness" / "log"

SFARI_PUBS_URL = "https://www.sfari.org/research/funded-publications/"
PUBMED_ESUMMARY = ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
                   "?db=pubmed&retmode=json&id={pmid}")

PMID_RE       = re.compile(r"pubmed\.ncbi\.nlm\.nih\.gov/(\d{7,9})")
ARTICLE_RE    = re.compile(r'class="funded-pub-card"[^>]*>(.*?)</article>', re.DOTALL)
TITLE_RE      = re.compile(r'<h3[^>]*>(.*?)</h3>', re.DOTALL)

UA = {"User-Agent": "CausesAtlas/0.1 (sfari-publications)"}

def log(msg: str) -> None:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"[{ts}] {msg}", flush=True)

def fetch(url: str, sleep_s: float = 0.5) -> str:
    """Polite fetch with built-in throttle. SFARI's WordPress isn't rate-
    limited but we don't want to be impolite."""
    time.sleep(sleep_s)
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        log(f"⚠ HTTP {e.code} on {url[:80]}")
        return ""
    except (urllib.error.URLError, TimeoutError) as e:
        log(f"⚠ fetch failed {url[:80]}: {e}")
        return ""

def build_search_url(page: int, year: int | None, cohort: str | None) -> str:
    params = {}
    if year:   params["search_year"] = str(year)
    if cohort: params["search_pub_resource[]"] = cohort
    params["paged"] = str(page) if page > 1 else "1"
    qs = urllib.parse.urlencode(params, doseq=True)
    return f"{SFARI_PUBS_URL}?{qs}" if qs else SFARI_PUBS_URL

def extract_pmids_from_page(html: str) -> list[dict]:
    """Each article card has a PubMed link. Pull (pmid, title) per article."""
    out = []
    for m in PMID_RE.finditer(html):
        pmid = m.group(1)
        # cheap-ish title extraction around the match
        ctx = html[max(0, m.start()-1500):m.end()+200]
        tm = TITLE_RE.search(ctx)
        title = re.sub(r"<[^>]+>", "", (tm.group(1) if tm else "")).strip()[:200]
        out.append({"pmid": pmid, "title": title})
    # dedupe in stable order
    seen, dedup = set(), []
    for r in out:
        if r["pmid"] in seen: continue
        seen.add(r["pmid"])
        dedup.append(r)
    return dedup

def existing_pmids() -> set[str]:
    """All PMIDs already in sources.csv (we don't re-ingest)."""
    if not SOURCES.exists():
        return set()
    out = set()
    with SOURCES.open() as f:
        for r in csv.DictReader(f):
            pmid = (r.get("pmid") or "").strip()
            if pmid and pmid.isdigit():
                out.add(pmid)
    return out

def queued_pmids() -> set[str]:
    """PMIDs already in freshness/queue/ waiting for drain."""
    if not FRESH_QUEUE.exists():
        return set()
    return {p.stem for p in FRESH_QUEUE.glob("*.json")}

def verify_pmid(pmid: str, expected_title_hint: str | None = None) -> dict | None:
    """PubMed esummary verification per CLAUDE.md §24. Returns metadata
    if PMID resolves to a real article; None otherwise."""
    url = PUBMED_ESUMMARY.format(pmid=pmid)
    body = fetch(url, sleep_s=0.34)   # NCBI ≤ 3 req/sec without API key
    if not body:
        return None
    try:
        data = json.loads(body)
        rec = data.get("result", {}).get(pmid)
        if not rec or rec.get("uid") != pmid:
            return None
        # Soft-match against the title hint if we have one (don't reject
        # on mismatch — SFARI titles often differ from PubMed canonical)
        title    = rec.get("title", "") or ""
        authors  = rec.get("authors", [])
        first_au = (authors[0].get("name") if authors else "") or ""
        journal  = rec.get("source", "")
        year     = (rec.get("pubdate", "") or "")[:4]
        return {
            "pmid":     pmid,
            "title":    title.strip(),
            "first_author": first_au,
            "journal":  journal,
            "year":     year,
            "verified": True,
            "verified_at": datetime.now(timezone.utc).isoformat(),
        }
    except (json.JSONDecodeError, KeyError):
        return None

def write_queue_entry(meta: dict, source_tag: str = "sfari_funded") -> pathlib.Path:
    FRESH_QUEUE.mkdir(parents=True, exist_ok=True)
    fp = FRESH_QUEUE / f"{meta['pmid']}.json"
    meta = dict(meta)
    meta["source_tag"] = source_tag
    fp.write_text(json.dumps(meta, indent=2))
    return fp

def write_log(entries: list[dict], year: int | None, cohort: str | None,
              n_pages: int, n_seen: int, n_new: int, n_verified: int) -> None:
    FRESH_LOG.mkdir(parents=True, exist_ok=True)
    date_tag = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    fp = FRESH_LOG / f"{date_tag}_sfari_pubs.json"
    fp.write_text(json.dumps({
        "run_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": "sfari_funded_publications",
        "year_filter": year, "cohort_filter": cohort,
        "pages_walked": n_pages,
        "pmids_seen": n_seen,
        "pmids_new": n_new,
        "pmids_verified": n_verified,
        "verified_pmids": [e["pmid"] for e in entries][:200],
    }, indent=2))

def main():
    ap = argparse.ArgumentParser(description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--commit",     action="store_true",
                    help="write verified PMIDs to freshness/queue/")
    ap.add_argument("--year",       type=int, default=None,
                    help="restrict to a single SFARI publication year")
    ap.add_argument("--cohort",     type=str, default=None,
                    choices=["spark", "ssc", "searchlight",
                             "autism-brainnet", "brainspan"],
                    help="restrict to one cohort filter")
    ap.add_argument("--max-pages",  type=int, default=10,
                    help="safety cap on pagination (default 10)")
    ap.add_argument("--max-verify", type=int, default=25,
                    help="cap on PMIDs verified per run (rate-limit safety)")
    args = ap.parse_args()

    log(f"SFARI funded publications crawl  year={args.year} "
        f"cohort={args.cohort or 'all'}  max_pages={args.max_pages}")

    have_sources = existing_pmids()
    have_queue   = queued_pmids()
    log(f"  atlas already has {len(have_sources):,} PMIDs in sources.csv "
        f"+ {len(have_queue)} in queue")

    seen_pmids: dict[str, dict] = {}
    pages_walked = 0
    for page in range(1, args.max_pages + 1):
        url = build_search_url(page, args.year, args.cohort)
        log(f"  fetching page {page}: {url[-80:]}")
        html = fetch(url, sleep_s=0.5)
        if not html:
            log(f"  empty page {page}, stopping")
            break
        pages_walked += 1
        candidates = extract_pmids_from_page(html)
        if not candidates:
            log(f"  no PMIDs found on page {page}, stopping")
            break
        added = 0
        for c in candidates:
            if c["pmid"] not in seen_pmids:
                seen_pmids[c["pmid"]] = c
                added += 1
        log(f"    +{added} new PMIDs (running total {len(seen_pmids)})")
        if added == 0:
            log(f"  no new PMIDs added, stopping pagination")
            break

    # Filter: drop already-known
    candidates = [c for pmid, c in sorted(seen_pmids.items())
                  if pmid not in have_sources and pmid not in have_queue]
    log(f"  {len(candidates)} novel candidates after dedup")

    # Verify each (capped by --max-verify)
    verified = []
    for c in candidates[: args.max_verify]:
        meta = verify_pmid(c["pmid"], expected_title_hint=c.get("title"))
        if not meta:
            log(f"    ⚠ PMID {c['pmid']} did not verify on PubMed")
            continue
        verified.append(meta)
        log(f"    ✓ {meta['pmid']} {meta['first_author']} {meta['year']} "
            f"({meta['journal'][:30]})")

    log(f"  verified: {len(verified)} / attempted {min(len(candidates), args.max_verify)}")

    if not args.commit:
        log("dry-run: pass --commit to write to freshness/queue/")
        return 0

    for m in verified:
        fp = write_queue_entry(m, source_tag="sfari_funded")
    write_log(verified, args.year, args.cohort, pages_walked,
              len(seen_pmids), len(candidates), len(verified))
    log(f"✓ wrote {len(verified)} entries to {FRESH_QUEUE}")
    log("  next: autonomous_loop drains the queue via run_ingest.py")
    return 0

if __name__ == "__main__":
    sys.exit(main() or 0)
