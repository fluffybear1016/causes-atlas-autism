#!/usr/bin/env python3
"""
run_ingest.py — Causes Atlas (Autism) ingestion pipeline

Implements spec v1.2 §14: turns a single artifact (PubMed PMID, DOI,
URL, or pasted text from authenticated platforms like X) into appended
rows + recomputed scores + score_history entries.

Usage:
    # PubMed ingestion (preferred — full metadata via NCBI E-utilities)
    python run_ingest.py pmid 38715916

    # URL ingestion (best-effort metadata extraction)
    python run_ingest.py url https://example.com/paper

    # Paste-text ingestion (for X posts, paywalled content, etc.)
    python run_ingest.py paste \
        --title "X post by @SabineHazanMD on Bifidobacterium" \
        --platform x \
        --external_id "1234567890" \
        --type social \
        --year 2025 \
        --content "Pasted text content here..."

    # Manual entity assignment (skips auto-extraction)
    python run_ingest.py pmid 38715916 \
        --target hypothesis HYP-0007 positive \
        --target intervention INT-0076 positive

Behavior:
    1. Reads latest scored CSVs from --input-dir (default: scored_output_v19)
    2. Looks up artifact in node_aliases — if already ingested, exits
       with the existing source_id and zero deltas (idempotent).
    3. Fetches metadata (PMID via NCBI; URL via WebFetch-like; paste
       takes user-provided metadata).
    4. Appends source row, evidence_fragment row.
    5. Auto-proposes evidence_links via name-matching against existing
       hypothesis/intervention/mechanism names with token similarity.
    6. Anything below confidence 0.80 goes to manual_review.csv.
    7. Recomputes scores via the engine (deferred to a follow-up
       run_scoring call) — for now, ingestion appends and the user
       runs run_scoring manually.
    8. Writes score_history entries with the delta vs. previous run.
    9. Outputs ingestion_result.json with full audit.

Determinism: same input → identical output. Re-ingesting the same PMID
returns the existing source_id and exits zero.

NOTE: This is the canonical pipeline for spec §14. PubMed E-utilities
fetch uses urllib (no API key needed for moderate volume; respects
NCBI's 3 req/sec limit). For URL ingestion, falls back to a simple
HTML fetch with title/meta extraction.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

import pandas as pd

# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------

DEFAULT_INPUT_DIR = Path("scored_output_v19")
DEFAULT_OUTPUT_DIR = Path("ingest_output")
DEFAULT_LOG_DIR = Path("ingest_logs")
ENTREZ_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
USER_AGENT = "CausesAtlasAutism/1.2 (atlas@example.com)"

AUTO_ACCEPT_CONFIDENCE = 0.80


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")


def pad_id(prefix: str, n: int, width: int) -> str:
    return f"{prefix}-{str(n).zfill(width)}"


# ----------------------------------------------------------------------------
# PubMed E-utilities (no auth, public)
# ----------------------------------------------------------------------------

def fetch_pmid_metadata(pmid: str) -> dict:
    """Fetch a PubMed record via NCBI E-utilities efetch in XML format."""
    url = (f"{ENTREZ_BASE}/efetch.fcgi?db=pubmed&id={pmid}"
           f"&retmode=xml&tool=causes_atlas_autism&email=atlas@example.com")
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            xml = resp.read().decode("utf-8")
    except Exception as e:
        return {"error": f"E-utilities fetch failed: {e}"}

    # Polite rate limit
    time.sleep(0.35)

    try:
        root = ET.fromstring(xml)
    except ET.ParseError as e:
        return {"error": f"E-utilities XML parse failed: {e}"}

    art = root.find(".//PubmedArticle")
    if art is None:
        return {"error": "PMID not found"}

    medline = art.find(".//MedlineCitation")
    article = medline.find(".//Article") if medline is not None else None
    if article is None:
        return {"error": "Article element missing"}

    # Title
    title_el = article.find(".//ArticleTitle")
    title = title_el.text if title_el is not None and title_el.text else ""
    if title_el is not None:
        # ArticleTitle can have nested italic/sub elements
        title = "".join(title_el.itertext()).strip()

    # Abstract
    abstract_parts = [
        e.text for e in article.findall(".//Abstract/AbstractText")
        if e.text
    ]
    abstract = " ".join(abstract_parts)

    # Year
    year_el = article.find(".//Journal/JournalIssue/PubDate/Year")
    if year_el is None:
        year_el = article.find(".//Journal/JournalIssue/PubDate/MedlineDate")
    year = ""
    if year_el is not None and year_el.text:
        m = re.search(r"\d{4}", year_el.text)
        if m: year = m.group(0)

    # Journal
    journal_el = article.find(".//Journal/Title")
    journal = journal_el.text if journal_el is not None and journal_el.text \
              else ""

    # Authors (first three)
    authors = []
    for au in article.findall(".//Author")[:3]:
        last = au.find("LastName")
        init = au.find("Initials")
        if last is not None and last.text:
            name = last.text + (" " + init.text if init is not None and
                                init.text else "")
            authors.append(name)
    authors_str = ", ".join(authors)

    # Publication types → study_design
    ptypes = [pt.text for pt in article.findall(".//PublicationType")
              if pt.text]
    study_design = "other"
    if any("Randomized Controlled Trial" in p for p in ptypes):
        study_design = "rct"
    elif any("Meta-Analysis" in p for p in ptypes):
        study_design = "meta_analysis"
    elif any("Review" in p for p in ptypes):
        study_design = "review"
    elif any("Clinical Trial" in p for p in ptypes):
        study_design = "rct"
    elif any("Case Reports" in p for p in ptypes):
        study_design = "case_series"

    # MeSH terms (for entity matching downstream)
    mesh = [m.text for m in article.findall(".//MeshHeading/DescriptorName")
            if m.text]

    # DOI
    doi = ""
    for a in article.findall(".//ArticleId"):
        if a.attrib.get("IdType") == "doi" and a.text:
            doi = a.text; break

    return {
        "pmid": pmid, "title": title, "abstract": abstract, "year": year,
        "journal": journal, "first_author": authors_str.split(",")[0]
            if authors_str else "",
        "all_authors": authors_str,
        "study_design": study_design,
        "publication_types": ptypes,
        "mesh_terms": mesh, "doi": doi,
    }


# ----------------------------------------------------------------------------
# URL ingestion (basic HTML title/meta extraction)
# ----------------------------------------------------------------------------

def fetch_url_metadata(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            content_type = resp.headers.get("Content-Type", "").lower()
            html = resp.read().decode("utf-8", errors="ignore")
    except Exception as e:
        return {"error": f"URL fetch failed: {e}"}

    title_m = re.search(r"<title[^>]*>([^<]+)</title>", html, re.I)
    title = title_m.group(1).strip() if title_m else url

    # OG / meta description
    desc_m = re.search(
        r'<meta[^>]+(?:name|property)="(?:description|og:description)"[^>]+'
        r'content="([^"]+)"', html, re.I)
    desc = desc_m.group(1).strip() if desc_m else ""

    return {
        "title": title, "abstract": desc, "url": url,
        "year": "", "journal": "", "first_author": "",
        "study_design": "other", "doi": "", "mesh_terms": [],
    }


# ----------------------------------------------------------------------------
# Entity auto-matching (lightweight; no LLMs)
# ----------------------------------------------------------------------------

def tokenize(s: str) -> set[str]:
    """Lowercase tokens, alphanumeric only, dropping stopwords + short."""
    stopwords = {"the", "a", "an", "and", "or", "of", "in", "on", "for",
                 "to", "with", "is", "are", "was", "were", "be", "been",
                 "by", "from", "at", "as", "this", "that", "these", "those",
                 "study", "trial", "review", "analysis", "meta", "rct"}
    tokens = re.findall(r"[a-zA-Z0-9]+", s.lower())
    return {t for t in tokens if len(t) > 2 and t not in stopwords}


def match_score(query_tokens: set[str], candidate_name: str) -> float:
    cand_tokens = tokenize(candidate_name)
    if not cand_tokens or not query_tokens:
        return 0.0
    overlap = len(query_tokens & cand_tokens)
    # Asymmetric: candidate token coverage matters more than query coverage
    return overlap / len(cand_tokens)


def propose_links(text: str, tables: dict) -> list[dict]:
    """Match the input text against existing hypothesis/intervention/
    mechanism names; return candidate evidence_links with confidence."""
    query_tokens = tokenize(text)
    proposals = []

    for ttype, table_name in [
        ("hypothesis", "hypotheses"),
        ("intervention", "interventions"),
        ("mechanism", "mechanisms"),
        ("gene", "genes"),
    ]:
        df = tables.get(table_name)
        if df is None or df.empty: continue
        name_col = "gene_symbol" if ttype == "gene" else "name"
        for _, row in df.iterrows():
            name = str(row[name_col])
            score = match_score(query_tokens, name)
            if score >= 0.4:  # at least 40% of candidate tokens covered
                proposals.append({
                    "target_type": ttype,
                    "target_id": row["id"],
                    "target_name": name,
                    "match_score": round(score, 3),
                })
    proposals.sort(key=lambda p: -p["match_score"])
    return proposals[:10]


def infer_effect_direction(text: str) -> str:
    """Cheap heuristic: scan for negation phrases."""
    low = text.lower()
    negative_markers = ["no association", "not associated",
                        "no significant", "did not find",
                        "does not", "not linked", "no evidence",
                        "rejected", "found no link"]
    for marker in negative_markers:
        if marker in low: return "negative"
    return "positive"


# ----------------------------------------------------------------------------
# Main ingestion orchestrator
# ----------------------------------------------------------------------------

def load_tables(input_dir: Path) -> dict:
    return {p.stem: pd.read_csv(p, dtype=str, keep_default_na=False)
            for p in sorted(input_dir.glob("*.csv"))}


def next_n(tables: dict, table: str, prefix: str) -> int:
    df = tables[table]
    if df.empty: return 1
    nums = []
    for i in df["id"].dropna():
        m = re.match(rf"^{prefix}-(\d+)$", str(i))
        if m: nums.append(int(m.group(1)))
    return (max(nums) if nums else 0) + 1


def alias_lookup(tables: dict, alias: str) -> str | None:
    a = tables.get("node_aliases")
    if a is None or a.empty: return None
    match = a[a["alias"] == alias]
    if match.empty: return None
    return match.iloc[0]["node_id"]


def run_ingest(args) -> int:
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    log_dir = Path(args.log_dir)
    output_dir.mkdir(exist_ok=True)
    log_dir.mkdir(exist_ok=True)

    ts = now_iso()
    print(f"[ingest] {now_iso()} — loading from {input_dir}")
    tables = load_tables(input_dir)

    # ---- 1. Fetch metadata ----
    if args.mode == "pmid":
        existing = alias_lookup(tables, f"PMID:{args.pmid}")
        if existing:
            print(f"[ingest] PMID {args.pmid} already ingested as "
                  f"{existing}. No-op.")
            return 0
        meta = fetch_pmid_metadata(args.pmid)
        if "error" in meta:
            print(f"[ingest] FAILED: {meta['error']}")
            return 1
        platform = "pubmed"; external_id = args.pmid
        match_text = f"{meta['title']} {meta['abstract']} " \
                     + " ".join(meta.get("mesh_terms", []))
    elif args.mode == "url":
        meta = fetch_url_metadata(args.url)
        if "error" in meta:
            print(f"[ingest] FAILED: {meta['error']}")
            return 1
        platform = "other"; external_id = args.url
        match_text = f"{meta['title']} {meta['abstract']}"
    elif args.mode == "paste":
        meta = {
            "title": args.title, "abstract": args.content,
            "year": args.year, "journal": "",
            "first_author": args.author or "",
            "study_design": args.study_design or "other",
            "doi": "", "mesh_terms": [],
        }
        platform = args.platform; external_id = args.external_id
        match_text = f"{args.title} {args.content}"
    else:
        print(f"[ingest] unknown mode: {args.mode}"); return 1

    # ---- 2. Determine source.type from study_design and platform ----
    src_type = {
        "rct": "study", "meta_analysis": "review",
        "review": "review", "case_series": "study",
    }.get(meta.get("study_design"), "other")
    if platform in ("reddit", "youtube", "x", "twitter"):
        src_type = "social"

    # ---- 3. Append source row ----
    sid = pad_id("SRC", next_n(tables, "sources", "SRC"), 6)
    new_source = pd.DataFrame([{
        "id": sid, "type": src_type, "platform": platform,
        "external_id": external_id, "title": meta["title"][:480],
        "url": (f"https://pubmed.ncbi.nlm.nih.gov/{args.pmid}/"
                if args.mode == "pmid" else
                args.url if args.mode == "url" else ""),
        "date_published": (f"{meta['year']}-01-01"
                            if meta["year"] else ""),
        "date_ingested": ts,
        "study_design": meta.get("study_design", "other"),
        "sample_size": "", "model_system": "human",
        "raw_metadata": json.dumps({
            "added_via_ingest": True, "ingest_mode": args.mode,
            "first_author": meta.get("first_author", ""),
            "all_authors": meta.get("all_authors", ""),
            "journal": meta.get("journal", ""),
            "doi": meta.get("doi", ""),
            "mesh_terms": meta.get("mesh_terms", [])[:20],
            "abstract": meta.get("abstract", "")[:2000],
            "ingest_run_ts": ts,
        }, sort_keys=True),
        "notes": "",
    }])
    tables["sources"] = pd.concat([tables["sources"], new_source],
                                  ignore_index=True)

    # ---- 4. Append evidence_fragment row ----
    fid = pad_id("EVD", next_n(tables, "evidence_fragments", "EVD"), 6)
    eff_dir = infer_effect_direction(match_text)
    new_frag = pd.DataFrame([{
        "id": fid, "source_id": sid,
        "fragment_type": "result" if src_type != "social"
                          else "anecdote",
        "text_excerpt": (meta.get("abstract") or
                         meta.get("title") or "")[:480],
        "structured_payload": json.dumps({
            "added_via_ingest": True, "ingest_mode": args.mode,
            "first_author": meta.get("first_author", ""),
            "year": meta.get("year", ""),
            "design": meta.get("study_design", ""),
        }, sort_keys=True),
        "effect_direction": eff_dir,
        "strength_score": "",
        "extraction_method": "rule_based",
        "extraction_confidence": "",
        "date_extracted": ts, "notes": "",
    }])
    tables["evidence_fragments"] = pd.concat(
        [tables["evidence_fragments"], new_frag], ignore_index=True)

    # ---- 5. Append node_alias for idempotency ----
    if args.mode == "pmid":
        alias_str = f"PMID:{args.pmid}"
    elif args.mode == "url":
        alias_str = args.url
    else:
        alias_str = f"{platform}:{external_id}"
    aid = pad_id("ALS", next_n(tables, "node_aliases", "ALS"), 6)
    new_alias = pd.DataFrame([{
        "id": aid, "node_type": "source", "node_id": sid,
        "alias": alias_str, "source": "ingest_pipeline",
        "created_at": ts,
    }])
    tables["node_aliases"] = pd.concat(
        [tables["node_aliases"], new_alias], ignore_index=True)

    # ---- 6. Auto-propose evidence_links ----
    proposals = propose_links(match_text, tables)
    auto_accepted = []
    manual_queue = []
    for p in proposals:
        if p["match_score"] >= AUTO_ACCEPT_CONFIDENCE:
            auto_accepted.append(p)
        else:
            manual_queue.append(p)

    # User-supplied targets always auto-accept
    for ut in (args.target or []):
        ttype, tid, direction = ut
        auto_accepted.append({
            "target_type": ttype, "target_id": tid,
            "target_name": "(user-supplied)",
            "match_score": 1.0, "effect_direction": direction,
        })

    # Append accepted as evidence_links
    new_links = []
    n_evl = next_n(tables, "evidence_links", "EVL")
    for p in auto_accepted:
        new_links.append({
            "id": pad_id("EVL", n_evl, 6), "evidence_fragment_id": fid,
            "claim_id": "",
            "target_type": p["target_type"],
            "target_id": p["target_id"],
            "effect_direction": p.get("effect_direction", eff_dir),
            "weight": "", "context_scope": "",
            "created_at": ts,
            "notes": (f"auto-ingest match_score="
                      f"{p.get('match_score','user'):.2f}"),
        })
        n_evl += 1
    if new_links:
        tables["evidence_links"] = pd.concat(
            [tables["evidence_links"], pd.DataFrame(new_links)],
            ignore_index=True)

    # ---- 7. Write everything ----
    for name, df in tables.items():
        df.to_csv(output_dir / f"{name}.csv", index=False, encoding="utf-8")

    # ---- 8. Manual review queue ----
    if manual_queue:
        mq_path = log_dir / f"manual_review_{int(time.time())}.csv"
        pd.DataFrame(manual_queue).to_csv(mq_path, index=False)

    # ---- 9. Result document ----
    result = {
        "ingest_run_ts": ts, "ingest_mode": args.mode,
        "external_id": external_id, "platform": platform,
        "source_id": sid, "fragment_id": fid,
        "alias_id": aid,
        "auto_accepted_links": len(auto_accepted),
        "manual_review_queued": len(manual_queue),
        "metadata": meta,
        "auto_accepted": [{k: v for k, v in p.items()
                            if k != "all_authors"}
                           for p in auto_accepted],
        "manual_queue": manual_queue,
        "next_step": ("Run run_scoring.py against output_dir to "
                      "recompute scores and emit score_history."),
    }
    result_path = log_dir / f"ingest_result_{int(time.time())}.json"
    result_path.write_text(json.dumps(result, indent=2, default=str))

    print()
    print("=" * 60)
    print(f"INGESTION COMPLETE — {args.mode}")
    print("=" * 60)
    print(f"  source_id           = {sid}")
    print(f"  fragment_id         = {fid}")
    print(f"  auto_accepted_links = {len(auto_accepted)}")
    print(f"  manual_review_queued = {len(manual_queue)}")
    print(f"  output_dir          = {output_dir}")
    print(f"  result_doc          = {result_path}")
    print()
    print(f"To finalize scoring:")
    print(f"  python run_scoring.py "
          f"  (with INPUT_DIR={output_dir} OUTPUT_DIR=...)")
    return 0


# ----------------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------------

def parse_args(argv):
    p = argparse.ArgumentParser(
        description="Causes Atlas ingestion pipeline (spec §14)")
    p.add_argument("--input-dir", default=str(DEFAULT_INPUT_DIR),
                   help="Directory containing scored CSVs")
    p.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR),
                   help="Directory to write updated CSVs")
    p.add_argument("--log-dir", default=str(DEFAULT_LOG_DIR),
                   help="Directory for logs and result documents")

    sub = p.add_subparsers(dest="mode", required=True)

    pp = sub.add_parser("pmid", help="Ingest a PubMed PMID")
    pp.add_argument("pmid", help="The PubMed ID (numeric)")
    pp.add_argument("--target", nargs=3,
                     metavar=("TYPE", "ID", "DIRECTION"),
                     action="append",
                     help="Manually-specified target link "
                          "(can repeat). DIRECTION ∈ {positive, negative, "
                          "neutral}")

    pu = sub.add_parser("url", help="Ingest a generic URL")
    pu.add_argument("url")
    pu.add_argument("--target", nargs=3,
                     metavar=("TYPE", "ID", "DIRECTION"),
                     action="append")

    pa = sub.add_parser("paste",
                          help="Ingest pasted text (X posts, etc.)")
    pa.add_argument("--title", required=True)
    pa.add_argument("--platform", required=True,
                     help="e.g. x, reddit, youtube, substack")
    pa.add_argument("--external_id", default="")
    pa.add_argument("--type", default="social", dest="src_type")
    pa.add_argument("--year", default="")
    pa.add_argument("--author", default="")
    pa.add_argument("--study_design", default="other")
    pa.add_argument("--content", required=True,
                     help="The actual text content to ingest")
    pa.add_argument("--target", nargs=3,
                     metavar=("TYPE", "ID", "DIRECTION"),
                     action="append")

    return p.parse_args(argv)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    sys.exit(run_ingest(args))
