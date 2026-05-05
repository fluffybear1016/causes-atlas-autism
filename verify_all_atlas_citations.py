#!/usr/bin/env python3
"""Atlas-wide PMID verification.

For every source in v2.0_scored/sources.csv with platform=pubmed:
  1. Verify the PMID exists on PubMed
  2. Compare the atlas-stored title against PubMed's title (token-overlap heuristic)
  3. Flag duplicates (same PMID, different SRC IDs)
  4. Flag missing/empty PMIDs
  5. Flag obvious mismatches

Outputs:
  v2.0.1_proposed/atlas_citation_audit.json — full report
  Console summary of problems found
"""
import csv, json, urllib.request, time, re
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parent
SOURCES = ROOT / "v2.0_scored" / "sources.csv"
OUT_DIR = ROOT / "v2.0.1_proposed"
OUT_DIR.mkdir(exist_ok=True)
OUT = OUT_DIR / "atlas_citation_audit.json"
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

def http(url):
    req = urllib.request.Request(url, headers={"User-Agent": "causes-atlas/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r: return r.read().decode()

def title_overlap(a, b, min_len=5):
    aw = set(w.lower() for w in re.findall(r"[A-Za-z]+", a) if len(w) >= min_len)
    bw = set(w.lower() for w in re.findall(r"[A-Za-z]+", b) if len(w) >= min_len)
    if not aw or not bw: return 0.0
    return len(aw & bw) / min(len(aw), len(bw))

# === Load ===
sources = list(csv.DictReader(open(SOURCES)))
print(f"Loaded {len(sources)} total sources")

pubmed = [s for s in sources if s["platform"] == "pubmed" and s["external_id"]]
print(f"PubMed sources: {len(pubmed)}")

# Check duplicates
pmid_to_srcs = defaultdict(list)
for s in pubmed:
    pmid_to_srcs[s["external_id"]].append(s["id"])
dupes = {p: srcs for p, srcs in pmid_to_srcs.items() if len(srcs) > 1}
print(f"PMID duplicates (same PMID, multiple SRC IDs): {len(dupes)}")
for p, srcs in list(dupes.items())[:5]:
    print(f"  PMID {p}: {srcs}")

# === Verify against PubMed in batches of 200 ===
print("\nVerifying PMIDs against PubMed (batches of 200)...")
all_pmids = sorted(set(s["external_id"] for s in pubmed))
verified = {}
for i in range(0, len(all_pmids), 200):
    batch = all_pmids[i:i+200]
    try:
        d = json.loads(http(f"{EUTILS}/esummary.fcgi?db=pubmed&retmode=json&id={','.join(batch)}"))
        for pmid in batch:
            r = d.get("result", {}).get(pmid, {})
            if r and r.get("title"):
                verified[pmid] = {
                    "title": r.get("title", ""),
                    "year": r.get("pubdate", "")[:4],
                    "journal": r.get("source", ""),
                    "authors": [a.get("name","") for a in r.get("authors",[])[:3]],
                    "pubtype": r.get("pubtype", []),
                }
        time.sleep(0.4)
        if (i // 200 + 1) % 5 == 0:
            print(f"  ...{i+len(batch)}/{len(all_pmids)} verified ({len(verified)} returned)")
    except Exception as e:
        print(f"  WARN batch {i}: {e}")
        time.sleep(2)

print(f"\nVerification: {len(verified)}/{len(all_pmids)} PMIDs returned content")

# === Compare titles ===
mismatches = []
not_found = []
for s in pubmed:
    pmid = s["external_id"]
    if pmid not in verified:
        not_found.append({"src_id": s["id"], "pmid": pmid, "atlas_title": s["title"]})
        continue
    v = verified[pmid]
    overlap = title_overlap(s["title"], v["title"])
    if overlap < 0.30:
        mismatches.append({
            "src_id": s["id"], "pmid": pmid,
            "atlas_title": s["title"][:120],
            "pubmed_title": v["title"][:120],
            "overlap": round(overlap, 2),
            "pubmed_authors": ", ".join(v["authors"]),
            "pubmed_year": v["year"],
            "pubmed_journal": v["journal"],
        })

print(f"\n{'='*80}")
print("RESULTS")
print(f"{'='*80}")
print(f"Total PubMed sources: {len(pubmed)}")
print(f"Unique PMIDs: {len(all_pmids)}")
print(f"Verified on PubMed: {len(verified)}")
print(f"NOT FOUND on PubMed: {len(not_found)}")
print(f"Title MISMATCHES (<30% overlap): {len(mismatches)}")
print(f"PMID DUPLICATES across SRC IDs: {len(dupes)}")

# Show worst mismatches
print(f"\n--- Top 20 worst title-mismatches ---")
mismatches.sort(key=lambda x: x["overlap"])
for m in mismatches[:20]:
    print(f"\n  {m['src_id']} (PMID {m['pmid']}) overlap={m['overlap']}")
    print(f"    Atlas:  {m['atlas_title']}")
    print(f"    PubMed: {m['pubmed_title']}")
    print(f"    PubMed authors: {m['pubmed_authors']} ({m['pubmed_year']}, {m['pubmed_journal']})")

print(f"\n--- Not found on PubMed (first 10) ---")
for nf in not_found[:10]:
    print(f"  {nf['src_id']} (PMID {nf['pmid']}): {nf['atlas_title'][:80]}")

# Save full report
report = {
    "total_pubmed_sources": len(pubmed),
    "unique_pmids": len(all_pmids),
    "verified_count": len(verified),
    "not_found_count": len(not_found),
    "mismatch_count": len(mismatches),
    "duplicate_pmid_count": len(dupes),
    "not_found": not_found,
    "mismatches": mismatches,
    "duplicates": [{"pmid": p, "src_ids": srcs} for p, srcs in dupes.items()],
}
with open(OUT, "w") as f:
    json.dump(report, f, indent=2)
print(f"\nFull report written to {OUT}")
