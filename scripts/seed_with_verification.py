#!/usr/bin/env python3
"""
seed_with_verification.py

Verify-before-write seed-script template for atlas prior-table seeding.

Encodes the BioMysteryBench-aligned protocol from CLAUDE.md "Verification
protocol" section + SESSION_4_HANNAH_POLING_SPEC.md §24.

Background: Anthropic's BioMysteryBench evaluation (April 2026) documented
that LLMs succeed on hard bioinformatics tasks via "lucky solution paths"
that don't replicate. The structural failure mode produces fabricated
plausible-looking wrong answers when ungrounded — including fabricated
PMIDs that look correct but reference unrelated papers. The atlas's
2026-04-30 Phase 0H seeding had 45 of 52 PMIDs fabricated until caught
by triple-check verification.

This script enforces verify-before-write for every row written to a prior
table.

Usage:
    python scripts/seed_with_verification.py \\
        --candidates path/to/candidates.yaml \\
        --output path/to/output.csv \\
        --log path/to/verification.log \\
        [--dry-run]

Candidates YAML schema (per row):
    - row_id: IEP-00001
      claimed_pmid: 23613074
      claimed_first_author: Christensen
      claimed_year: 2013
      claimed_key_terms: [valproate, autism]
      claimed_journal_substring: JAMA  # optional
      row_data:
        # full CSV row dict; will be written verbatim if verification passes
        iatrogenic_id: gestational_valproate
        ...
"""

import argparse
import csv
import json
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML required. Install with: pip install --break-system-packages pyyaml", file=sys.stderr)
    sys.exit(1)


ESUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
RATE_LIMIT_SECONDS = 0.4  # NCBI guideline: max 3/sec without API key


def fetch_pubmed_summary(pmids):
    """Batch fetch PubMed esummary for a list of PMID strings."""
    if not pmids:
        return {}
    pmids_str = ",".join(str(p) for p in pmids)
    url = f"{ESUMMARY_URL}?db=pubmed&id={pmids_str}&retmode=json"
    with urllib.request.urlopen(url, timeout=30) as resp:
        data = json.loads(resp.read())
    return data.get("result", {})


def verify_pmid_match(pmid, summary, claimed_author, claimed_year, claimed_key_terms,
                     claimed_journal_substring=None):
    """
    Returns (passed: bool, fail_reason: str|None, fetched: dict).
    """
    if not summary or not summary.get("title"):
        return False, f"PMID {pmid} not found in PubMed", {}

    title = summary.get("title", "").lower()
    fetched_author = summary.get("sortfirstauthor", "").lower()
    fetched_year = summary.get("pubdate", "")[:4]
    fetched_journal = summary.get("source", "")

    fetched = {
        "title": title[:120],
        "author": fetched_author,
        "year": fetched_year,
        "journal": fetched_journal,
    }

    # Check 1: author
    claimed_author_l = claimed_author.lower().strip()
    if claimed_author_l not in fetched_author and claimed_author_l not in title:
        return False, (
            f"author mismatch: claimed={claimed_author!r} "
            f"fetched_author={fetched_author!r} title='{title[:60]}'"
        ), fetched

    # Check 2: year
    if str(claimed_year) != fetched_year:
        return False, f"year mismatch: claimed={claimed_year} fetched={fetched_year}", fetched

    # Check 3: at least one key term in title or journal
    terms_lower = [t.lower() for t in claimed_key_terms]
    if not any(t in title or t in fetched_journal.lower() for t in terms_lower):
        return False, (
            f"no key term matched: claimed_terms={claimed_key_terms} "
            f"title='{title[:60]}' journal='{fetched_journal}'"
        ), fetched

    # Check 4: optional journal substring
    if claimed_journal_substring:
        if claimed_journal_substring.lower() not in fetched_journal.lower():
            return False, (
                f"journal substring mismatch: claimed={claimed_journal_substring!r} "
                f"fetched={fetched_journal!r}"
            ), fetched

    return True, None, fetched


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--candidates", required=True, type=Path,
                        help="Path to candidates YAML file")
    parser.add_argument("--output", required=True, type=Path,
                        help="Path to output CSV (rows appended only if verified)")
    parser.add_argument("--log", required=True, type=Path,
                        help="Path to verification log file")
    parser.add_argument("--dry-run", action="store_true",
                        help="Run verification but do not write CSV")
    parser.add_argument("--allow-empty-pmids", action="store_true",
                        help="Allow rows with no claimed_pmid (e.g., contested-status placeholders)")
    args = parser.parse_args()

    if not args.candidates.exists():
        print(f"ERROR: candidates file not found: {args.candidates}", file=sys.stderr)
        sys.exit(2)

    with open(args.candidates) as f:
        candidates = yaml.safe_load(f)

    if not isinstance(candidates, list):
        print(f"ERROR: candidates YAML must be a list of row specs", file=sys.stderr)
        sys.exit(2)

    print(f"Loaded {len(candidates)} candidate rows from {args.candidates}")

    # Pre-collect all unique PMIDs for batch fetch
    all_pmids = set()
    for cand in candidates:
        pmid = cand.get("claimed_pmid")
        if pmid:
            all_pmids.add(str(pmid))
        # Also handle countervailing
        for cv in cand.get("countervailing_claims", []):
            if cv.get("claimed_pmid"):
                all_pmids.add(str(cv["claimed_pmid"]))

    if not all_pmids and not args.allow_empty_pmids:
        print(f"ERROR: no PMIDs in any candidate. Use --allow-empty-pmids if intended.", file=sys.stderr)
        sys.exit(2)

    # Batch fetch (chunks of 25 to be safe)
    summaries = {}
    pmid_list = sorted(all_pmids)
    for i in range(0, len(pmid_list), 25):
        batch = pmid_list[i:i+25]
        print(f"  Fetching PubMed esummary batch {i+1}-{i+len(batch)} of {len(pmid_list)}...")
        try:
            fetched = fetch_pubmed_summary(batch)
            summaries.update(fetched)
        except Exception as e:
            print(f"  ERROR: PubMed fetch failed for batch: {e}", file=sys.stderr)
            sys.exit(3)
        time.sleep(RATE_LIMIT_SECONDS)

    print(f"Fetched {len([k for k in summaries if k != 'uids'])} PubMed records")

    # Verify each candidate
    verified_rows = []
    rejected = []
    log_entries = []
    log_entries.append(f"# Verification run: {datetime.utcnow().isoformat()}Z")
    log_entries.append(f"# candidates: {args.candidates}")
    log_entries.append(f"# output: {args.output}")
    log_entries.append(f"# Total candidates: {len(candidates)}")
    log_entries.append("")

    for cand in candidates:
        row_id = cand.get("row_id", "<unknown>")
        primary_pmid = cand.get("claimed_pmid")
        countervailing = cand.get("countervailing_claims", [])

        all_passed = True
        row_log = [f"## Row {row_id}"]

        # Verify primary PMID
        if primary_pmid:
            summary = summaries.get(str(primary_pmid), {})
            passed, fail_reason, fetched = verify_pmid_match(
                primary_pmid, summary,
                cand["claimed_first_author"],
                cand["claimed_year"],
                cand.get("claimed_key_terms", []),
                cand.get("claimed_journal_substring"),
            )
            row_log.append(
                f"  primary PMID {primary_pmid}: "
                f"{'PASS' if passed else 'FAIL'} "
                f"claimed=({cand['claimed_first_author']} {cand['claimed_year']}) "
                f"fetched=({fetched.get('author','')} {fetched.get('year','')}) "
                f"title='{fetched.get('title','')}'"
            )
            if not passed:
                all_passed = False
                row_log.append(f"    REASON: {fail_reason}")
        elif not args.allow_empty_pmids:
            all_passed = False
            row_log.append(f"  PMID empty and --allow-empty-pmids not set: REJECT")

        # Verify countervailing PMIDs
        for cv in countervailing:
            cv_pmid = cv.get("claimed_pmid")
            if not cv_pmid:
                continue
            summary = summaries.get(str(cv_pmid), {})
            passed, fail_reason, fetched = verify_pmid_match(
                cv_pmid, summary,
                cv["claimed_first_author"],
                cv["claimed_year"],
                cv.get("claimed_key_terms", []),
                cv.get("claimed_journal_substring"),
            )
            row_log.append(
                f"  countervailing PMID {cv_pmid}: "
                f"{'PASS' if passed else 'FAIL'} "
                f"claimed=({cv['claimed_first_author']} {cv['claimed_year']}) "
                f"fetched=({fetched.get('author','')} {fetched.get('year','')})"
            )
            if not passed:
                all_passed = False
                row_log.append(f"    REASON: {fail_reason}")

        if all_passed:
            verified_rows.append(cand["row_data"])
            row_log.append(f"  VERDICT: VERIFIED — row will be written")
        else:
            rejected.append((row_id, row_log))
            row_log.append(f"  VERDICT: REJECTED — row will NOT be written")

        log_entries.extend(row_log)
        log_entries.append("")

    # Summary
    summary_block = [
        "",
        "## Summary",
        f"Total candidates: {len(candidates)}",
        f"Verified (will write): {len(verified_rows)}",
        f"Rejected: {len(rejected)}",
    ]
    if rejected:
        summary_block.append(f"Rejected row IDs: {[r[0] for r in rejected]}")
    log_entries.extend(summary_block)

    # Write log
    args.log.parent.mkdir(parents=True, exist_ok=True)
    with open(args.log, "w") as f:
        f.write("\n".join(log_entries))
    print(f"\nWrote verification log: {args.log}")

    # Print summary to stdout
    print("\n".join(summary_block))

    # Write CSV (idempotent: skip rows whose full content already exists in output)
    if not args.dry_run and verified_rows:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        new_file = not args.output.exists()
        existing_row_keys = set()
        existing_header = None
        if not new_file:
            # Load existing rows to detect duplicates
            with open(args.output) as f:
                reader = csv.DictReader(f)
                existing_header = reader.fieldnames
                for r in reader:
                    # Use full-row content as the dedup key (field-order independent)
                    key = tuple(sorted((k, str(v)) for k, v in r.items()))
                    existing_row_keys.add(key)
            print(f"  Loaded {len(existing_row_keys)} existing rows for dedup check")

        if new_file:
            fieldnames = list(verified_rows[0].keys())
            with open(args.output, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for row in verified_rows:
                    writer.writerow(row)
            written_count = len(verified_rows)
            duplicate_count = 0
        else:
            written_count = 0
            duplicate_count = 0
            with open(args.output, "a", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=existing_header)
                for row in verified_rows:
                    # Ensure all keys exist (matching the existing header)
                    full_row = {k: str(row.get(k, "")) for k in existing_header}
                    key = tuple(sorted(full_row.items()))
                    if key in existing_row_keys:
                        duplicate_count += 1
                        continue
                    existing_row_keys.add(key)
                    writer.writerow(full_row)
                    written_count += 1
        if duplicate_count:
            print(f"Skipped {duplicate_count} rows already present in {args.output} (idempotent)")
        print(f"Wrote {written_count} new rows to {args.output}")
    elif args.dry_run:
        print(f"DRY RUN: would write {len(verified_rows)} verified rows to {args.output}")

    # Exit code: 0 if all verified, 1 if any rejected (caller decides whether to fail CI)
    sys.exit(0 if not rejected else 1)


if __name__ == "__main__":
    main()
