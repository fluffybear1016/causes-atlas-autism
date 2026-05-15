#!/usr/bin/env python3
"""
scripts/intake/pubmed_rss_scanner.py — daily PubMed E-utilities scanner.

Queries PubMed for autism / ASD / neurodevelopment papers added since the
last run, classifies each into the Hannah Poling P x E -> M -> Phi schema,
and writes candidates to vault/Discoveries_Inbox/. NOTHING is auto-promoted
to the canonical atlas — every candidate is curator-gated per CLAUDE.md
Sec.24 verify-before-write protocol.

Architecture:
  * Uses NCBI E-utilities esearch + esummary (no API key required for
    standard rate-limit; user can set NCBI_API_KEY env var for higher limits)
  * State file at vault/Discoveries_Inbox/.pubmed_last_run.json tracks the
    last successful run date so we only fetch new papers
  * Determinism: stable sort by PMID; identical input -> identical output
  * Anti-reflexivity: scanner does not preferentially target already-high-
    Delta-squared entities; query terms are static and broad

Query terms (configurable in QUERIES below):
  Each query has a target hypothesis cluster and a P/E/M/Phi tag for the
  intake classifier to use.

Run command:
  python3 scripts/intake/pubmed_rss_scanner.py
  python3 scripts/intake/pubmed_rss_scanner.py --dry-run         # show what would be fetched
  python3 scripts/intake/pubmed_rss_scanner.py --since 2026-04-01 # force backdate
  python3 scripts/intake/pubmed_rss_scanner.py --max-per-query 5  # rate limit

Output: vault/Discoveries_Inbox/pubmed_intake_<YYYY-MM-DD>.{md,json}
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
import urllib.parse
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta
from pathlib import Path
from xml.etree import ElementTree as ET

_CANDIDATE_REPOS = [
    Path("/Users/Greg/Autism"),
    Path("/sessions/jolly-determined-darwin/mnt/Autism"),
]
REPO = next((p for p in _CANDIDATE_REPOS if p.exists()), _CANDIDATE_REPOS[0])
INBOX = REPO / "vault" / "Discoveries_Inbox"
STATE = INBOX / ".pubmed_last_run.json"
SOURCES_CSV = REPO / "v2.0_scored" / "sources.csv"

NCBI_API_KEY = os.environ.get("NCBI_API_KEY", "")
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

# --------------------------------------------------------------------------
# Query set — covers the Hannah Poling P x E -> M -> Phi factor matrix
# --------------------------------------------------------------------------
# Each query specifies:
#   tag       : intake classifier hint (P / E / M / PHI / SYNTHESIS)
#   focus     : which hypothesis cluster the result is most relevant to
#   query     : PubMed search string
#
# Queries are intentionally broad. The intake_classifier downstream sorts
# results by relevance.

QUERIES = [
    {"tag": "E", "focus": "perinatal_hypoxia",
     "query": "(autism[Title/Abstract]) AND (perinatal hypoxia OR birth asphyxia OR HIE OR neonatal encephalopathy)"},
    {"tag": "P", "focus": "prenatal_screening_markers",
     "query": "(autism[Title/Abstract]) AND (alpha-fetoprotein OR AFP OR PAPP-A OR maternal serum screening OR NIPT)"},
    {"tag": "E", "focus": "maternal_immune_activation",
     "query": "(autism[Title/Abstract]) AND (maternal immune activation OR maternal fever OR cytokine pregnancy)"},
    {"tag": "P", "focus": "advanced_parental_age",
     "query": "(autism[Title/Abstract]) AND (advanced paternal age OR advanced maternal age OR de novo mutation)"},
    {"tag": "E", "focus": "in_utero_drug",
     "query": "(autism[Title/Abstract]) AND (valproate OR SSRI pregnancy OR acetaminophen OR teratogen)"},
    {"tag": "E", "focus": "environmental_toxicants",
     "query": "(autism[Title/Abstract]) AND (glyphosate OR pesticide OR phthalate OR BPA OR PFAS OR heavy metal)"},
    {"tag": "M", "focus": "mitochondrial_mechanism",
     "query": "(autism[Title/Abstract]) AND (mitochondrial dysfunction OR oxidative phosphorylation OR complex I deficiency)"},
    {"tag": "M", "focus": "gut_brain_axis",
     "query": "(autism[Title/Abstract]) AND (gut-brain axis OR microbiome OR dysbiosis OR intestinal permeability)"},
    {"tag": "M", "focus": "methylation_cycle",
     "query": "(autism[Title/Abstract]) AND (methylation OR FOLR1 OR cerebral folate OR MTHFR)"},
    {"tag": "E", "focus": "vaccine_axis",
     "query": "(autism[Title/Abstract]) AND (vaccine OR aluminum adjuvant OR thimerosal OR MMR OR hepatitis B)"},
    {"tag": "PHI", "focus": "phenotype_subtyping",
     "query": "(autism[Title/Abstract]) AND (subtype OR phenotype cluster OR endophenotype OR stratified)"},
    {"tag": "SYNTHESIS", "focus": "responder_subgroup_RCT",
     "query": "(autism[Title/Abstract]) AND (randomized controlled trial[Publication Type] OR responder analysis OR biomarker stratified)"},
]


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

def http_get(url: str, retries: int = 3, backoff: float = 1.5) -> str:
    """GET with simple retry. Returns response body as str."""
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=20) as r:
                return r.read().decode("utf-8")
        except (urllib.error.URLError, urllib.error.HTTPError) as e:
            if attempt == retries - 1:
                raise
            time.sleep(backoff ** (attempt + 1))
    return ""


def esearch_pmids(query: str, since: str, until: str, retmax: int = 50) -> list[str]:
    """PubMed esearch — returns PMID list for query within date window."""
    params = {
        "db": "pubmed",
        "term": f"{query} AND ({since}:{until}[edat])",
        "retmode": "json",
        "retmax": str(retmax),
        "sort": "date",
    }
    if NCBI_API_KEY:
        params["api_key"] = NCBI_API_KEY
    url = f"{EUTILS}/esearch.fcgi?" + urllib.parse.urlencode(params)
    body = http_get(url)
    try:
        data = json.loads(body)
        return data.get("esearchresult", {}).get("idlist", [])
    except json.JSONDecodeError:
        return []


def esummary_records(pmids: list[str]) -> list[dict]:
    """PubMed esummary — returns title/authors/journal/year per PMID."""
    if not pmids:
        return []
    params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "json",
    }
    if NCBI_API_KEY:
        params["api_key"] = NCBI_API_KEY
    url = f"{EUTILS}/esummary.fcgi?" + urllib.parse.urlencode(params)
    body = http_get(url)
    try:
        data = json.loads(body)
        result = data.get("result", {})
        records = []
        for pmid in pmids:
            r = result.get(pmid)
            if not r:
                continue
            authors = r.get("authors") or []
            first_author = authors[0].get("name", "") if authors else ""
            records.append({
                "pmid": pmid,
                "title": r.get("title", ""),
                "first_author": first_author,
                "journal": r.get("fulljournalname", "") or r.get("source", ""),
                "pubdate": r.get("pubdate", ""),
                "doi": next(
                    (a.get("value", "") for a in r.get("articleids", [])
                     if a.get("idtype") == "doi"),
                    "",
                ),
            })
        return records
    except json.JSONDecodeError:
        return []


def load_state() -> dict:
    if STATE.exists():
        try:
            return json.loads(STATE.read_text())
        except json.JSONDecodeError:
            pass
    return {}


def save_state(state: dict) -> None:
    INBOX.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, indent=2, sort_keys=True))


def existing_pmids() -> set[str]:
    """PMIDs already in sources.csv — used to de-dup intake."""
    pmids = set()
    if not SOURCES_CSV.exists():
        return pmids
    with SOURCES_CSV.open() as f:
        for r in csv.DictReader(f):
            if r.get("platform") == "pubmed" and r.get("external_id"):
                pmids.add(r["external_id"])
    return pmids


# --------------------------------------------------------------------------
# Main scan
# --------------------------------------------------------------------------

def scan(since_date: str, until_date: str, max_per_query: int, dry_run: bool) -> dict:
    state = load_state()
    known = existing_pmids()
    print(f"PubMed intake scan: {since_date} → {until_date}")
    print(f"  Already-ingested PMIDs in sources.csv: {len(known)}")
    print(f"  Queries: {len(QUERIES)}  max_per_query: {max_per_query}  dry_run: {dry_run}")
    print()

    all_candidates: list[dict] = []
    seen_pmids: set[str] = set()

    for q in QUERIES:
        print(f"  → {q['tag']:9s} {q['focus']:30s}", end=" ")
        try:
            pmids = esearch_pmids(q["query"], since_date, until_date,
                                  retmax=max_per_query)
        except Exception as e:
            print(f"FAIL {e}")
            continue

        # Drop PMIDs already in atlas or already surfaced by another query this run
        new_pmids = [p for p in pmids
                     if p not in known and p not in seen_pmids]
        seen_pmids.update(new_pmids)

        records = esummary_records(new_pmids) if new_pmids else []
        print(f"raw={len(pmids):3d}  new={len(new_pmids):3d}")
        for rec in records:
            all_candidates.append({
                **rec,
                "intake_tag": q["tag"],
                "intake_focus": q["focus"],
            })
        time.sleep(0.4)  # NCBI rate limit etiquette

    # Stable sort by PMID for determinism
    all_candidates.sort(key=lambda r: r["pmid"])

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    summary = {
        "scan_date": today,
        "since": since_date,
        "until": until_date,
        "queries_run": len(QUERIES),
        "candidates_total": len(all_candidates),
        "candidates_by_tag": {},
        "candidates": all_candidates,
    }
    for c in all_candidates:
        summary["candidates_by_tag"].setdefault(c["intake_tag"], 0)
        summary["candidates_by_tag"][c["intake_tag"]] += 1

    print()
    print(f"Total candidates: {len(all_candidates)}")
    for tag, n in sorted(summary["candidates_by_tag"].items()):
        print(f"  {tag}: {n}")

    if not dry_run:
        INBOX.mkdir(parents=True, exist_ok=True)
        json_path = INBOX / f"pubmed_intake_{today}.json"
        md_path = INBOX / f"pubmed_intake_{today}.md"
        json_path.write_text(json.dumps(summary, indent=2))
        md_path.write_text(render_md(summary))
        print(f"\nWrote {json_path}")
        print(f"Wrote {md_path}")

        # Update state
        state["last_run"] = today
        state["last_until"] = until_date
        save_state(state)

    return summary


def render_md(summary: dict) -> str:
    lines = [
        f"# PubMed intake — {summary['scan_date']}",
        "",
        f"Daily scan of PubMed E-utilities for autism / ASD / "
        f"neurodevelopment papers added between **{summary['since']}** "
        f"and **{summary['until']}**.",
        "",
        f"Candidates surfaced: **{summary['candidates_total']}** across "
        f"{summary['queries_run']} queries.",
        "",
        "These are NOT atlas changes — candidates for curator review. "
        "Per CLAUDE.md Sec.24, every PMID must be independently re-verified "
        "via PubMed esummary before atlas write (the scanner uses esummary "
        "for surfacing but the canonical atlas write must use "
        "`scripts/seed_with_verification.py`).",
        "",
        "## Per-tag summary",
        "",
        "| Tag | Count | Slot in P x E -> M -> Phi |",
        "| --- | ----- | ------------------------- |",
    ]
    tag_meaning = {
        "P": "Predisposition (genetic / biomarker / susceptibility)",
        "E": "Exposure / trigger (environmental / iatrogenic / perinatal)",
        "M": "Mechanism (biological pathway)",
        "PHI": "Phenotype (clinical presentation / subtyping)",
        "SYNTHESIS": "Cross-cutting (RCT, meta-analysis, responder analysis)",
    }
    for tag in ["P", "E", "M", "PHI", "SYNTHESIS"]:
        n = summary["candidates_by_tag"].get(tag, 0)
        lines.append(f"| {tag} | {n} | {tag_meaning[tag]} |")
    lines.extend([
        "",
        "## Candidates",
        "",
    ])
    for c in summary["candidates"]:
        lines.append(
            f"- **PMID {c['pmid']}** [{c['intake_tag']}/{c['intake_focus']}] "
            f"{c['first_author']} {c['pubdate']} — *{c['title']}* "
            f"({c['journal']})"
        )
        if c.get("doi"):
            lines.append(f"  DOI: {c['doi']}")
        lines.append(
            f"  → [PubMed](https://pubmed.ncbi.nlm.nih.gov/{c['pmid']}/)"
        )
        lines.append("")
    lines.extend([
        "## Curator workflow",
        "",
        "For each candidate, decide:",
        "1. **Promote** — add to atlas via "
        "`python3 scripts/seed_with_verification.py` after independent PMID "
        "re-verification + claim/PMID consistency check",
        "2. **Defer** — keep in inbox; not high-leverage enough yet",
        "3. **Reject** — fundamental methodology issue or duplicate of "
        "existing source",
        "",
        "Atlas writes must follow Sec.24 protocol: PubMed esummary verifies "
        "author + year + key-term match BEFORE the row is written. "
        "Memory-based PMID generation is forbidden.",
        "",
        "## Determinism + anti-reflexivity",
        "",
        "- Scanner produces byte-identical output for byte-identical "
        "(time-window, query, PubMed state) inputs.",
        "- Query terms are static and broad; the scanner does NOT "
        "preferentially target high-Delta-squared entities (anti-reflexivity).",
        "- All candidates gated by human review; nothing auto-promotes to the "
        "canonical atlas.",
    ])
    return "\n".join(lines)


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", help="YYYY-MM-DD (default: 7 days ago)")
    ap.add_argument("--until", help="YYYY-MM-DD (default: today)")
    ap.add_argument("--max-per-query", type=int, default=10)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    today = datetime.now(timezone.utc).date()
    until = args.until or today.strftime("%Y/%m/%d")
    if args.since:
        since = args.since.replace("-", "/")
    else:
        state = load_state()
        if state.get("last_until"):
            since = state["last_until"]
        else:
            since = (today - timedelta(days=7)).strftime("%Y/%m/%d")

    scan(since, until, args.max_per_query, args.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
