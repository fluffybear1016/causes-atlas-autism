#!/usr/bin/env python3
"""Verify all PMIDs in the 7 phenotype deep-dive pages against PubMed.

Output: per-PMID title + first authors + year, and flag suspected mismatches.
"""
import re
import json
import time
import urllib.request
from pathlib import Path

VAULT = Path("/sessions/jolly-determined-darwin/mnt/Autism/vault/topics/phenotypes")

# Pattern: capture link-text PMID + URL PMID + claimed title
# example: ([PMID 12345](https://pubmed.ncbi.nlm.nih.gov/12345/), *Cell*) — *"Title"*
PATTERN = re.compile(
    r'\[PMID (\d+)\]\(https://pubmed\.ncbi\.nlm\.nih\.gov/(\d+)/\)[^*]*\*([^*]+)\*[^*]*—\s*\*"([^"]+)"',
    re.MULTILINE
)


def fetch_summary(pmid):
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={pmid}&retmode=json"
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            data = json.load(resp)
        rec = data.get('result', {}).get(pmid)
        if not rec or rec.get('error'):
            return None
        return {
            'pmid': pmid,
            'title': rec.get('title', ''),
            'authors': [a['name'] for a in rec.get('authors', [])][:3],
            'pubdate': rec.get('pubdate', ''),
            'source': rec.get('source', ''),
        }
    except Exception as e:
        return {'error': str(e)}


def main():
    issues = []
    seen_pmids = set()
    pages = sorted(VAULT.glob("PHE-*.md"))
    for page in pages:
        text = page.read_text()
        matches = PATTERN.findall(text)
        for link_pmid, url_pmid, journal, title_claim in matches:
            if link_pmid != url_pmid:
                issues.append(f"  MISMATCH in {page.name}: link {link_pmid} vs URL {url_pmid} — title claim: {title_claim[:60]}")
            else:
                # Verify against PubMed (rate-limit)
                if link_pmid in seen_pmids:
                    continue
                seen_pmids.add(link_pmid)

    print(f"Found {len(seen_pmids)} unique PMIDs across {len(pages)} pages")
    if issues:
        print("\nLink/URL mismatches:")
        for i in issues:
            print(i)

    # Now verify all unique PMIDs against PubMed
    print("\nVerifying titles against PubMed...")
    for pmid in sorted(seen_pmids):
        s = fetch_summary(pmid)
        if not s:
            print(f"  {pmid}: NOT FOUND")
            continue
        if s.get('error'):
            print(f"  {pmid}: ERROR {s['error']}")
            continue
        first_author = s['authors'][0] if s['authors'] else "?"
        print(f"  {pmid}: {first_author} {s['pubdate'][:4]} — {s['title'][:90]}")
        time.sleep(0.34)  # PubMed rate limit ~3/sec

    return issues


if __name__ == "__main__":
    main()
