#!/usr/bin/env python3
"""For each mismatched PMID, search PubMed by atlas-stored title, find the correct PMID, update sources.csv.

Process:
  1. Load v2.0.1_proposed/atlas_citation_audit.json (mismatches list)
  2. For each mismatch with non-empty atlas_title:
       a. PubMed esearch for title
       b. esummary on top result
       c. If new title overlaps >= 0.50 with atlas title → high confidence, update
       d. If 0.30-0.50 → flag for human review
       e. If <0.30 → leave as-is, mark unfixable
  3. Update v2.0_scored/sources.csv (and v2.0.1_expanded) with corrections
  4. Write fix report

Cautious: only updates where confidence is high. Sources with empty atlas titles
or very-low-overlap candidates are left for manual review.
"""
import csv, json, re, urllib.request, urllib.parse, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
AUDIT = ROOT / "v2.0.1_proposed" / "atlas_citation_audit.json"
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

def http(url):
    req = urllib.request.Request(url, headers={"User-Agent": "causes-atlas/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r: return r.read().decode()

def title_overlap(a, b, min_len=5):
    aw = set(w.lower() for w in re.findall(r"[A-Za-z]+", a) if len(w) >= min_len)
    bw = set(w.lower() for w in re.findall(r"[A-Za-z]+", b) if len(w) >= min_len)
    if not aw or not bw: return 0.0
    return len(aw & bw) / min(len(aw), len(bw))

def search_title(title):
    """Find best PubMed match for a title. Returns (pmid, returned_title, overlap) or None."""
    # First try the title verbatim, with [Title] field tag
    q = title[:200]  # limit length
    url = f"{EUTILS}/esearch.fcgi?db=pubmed&retmode=json&retmax=5&term=" + urllib.parse.quote(q + "[Title]")
    try:
        d = json.loads(http(url))
        ids = d.get("esearchresult", {}).get("idlist", [])
        if not ids:
            # Fallback: drop [Title] tag, use general search
            url = f"{EUTILS}/esearch.fcgi?db=pubmed&retmode=json&retmax=5&term=" + urllib.parse.quote(q)
            time.sleep(0.2)
            d = json.loads(http(url))
            ids = d.get("esearchresult", {}).get("idlist", [])
        if not ids: return None
        time.sleep(0.2)
        d2 = json.loads(http(f"{EUTILS}/esummary.fcgi?db=pubmed&retmode=json&id={','.join(ids[:3])}"))
        candidates = []
        for pmid in ids[:3]:
            r = d2.get("result", {}).get(pmid, {})
            if r.get("title"):
                ov = title_overlap(title, r["title"])
                candidates.append((pmid, r["title"], ov,
                                   r.get("pubdate", "")[:4],
                                   r.get("source", ""),
                                   [a.get("name","") for a in r.get("authors",[])[:3]]))
        candidates.sort(key=lambda x: -x[2])
        return candidates[0] if candidates else None
    except Exception as e:
        return None

# === Load audit ===
audit = json.loads(open(AUDIT).read())
mismatches = audit["mismatches"]
print(f"Auditing {len(mismatches)} mismatched citations…")

# === Search for each ===
fixes = []  # list of {src_id, old_pmid, new_pmid, old_title, new_title, overlap}
unfixable = []
flagged = []

# Resume from checkpoint if exists
CKPT = ROOT / "v2.0.1_proposed" / "pmid_fix_checkpoint.json"
if CKPT.exists():
    try:
        cp = json.loads(open(CKPT).read())
        fixes = cp.get("fixes", [])
        flagged = cp.get("flagged", [])
        unfixable = cp.get("unfixable", [])
        start_idx = cp.get("next_idx", 0)
        print(f"Resuming from checkpoint at index {start_idx} (fixes={len(fixes)}, flagged={len(flagged)}, unfixable={len(unfixable)})")
    except:
        start_idx = 0
else:
    start_idx = 0

for i in range(start_idx, len(mismatches)):
    m = mismatches[i]
    title = m["atlas_title"]
    if not title.strip():
        unfixable.append({**m, "reason": "empty_atlas_title"})
        continue
    if (i+1) % 5 == 0:
        # Save checkpoint
        with open(CKPT, "w") as f:
            json.dump({"fixes": fixes, "flagged": flagged, "unfixable": unfixable, "next_idx": i+1}, f)
        print(f"  ...{i+1}/{len(mismatches)} (fixed {len(fixes)}, flagged {len(flagged)}, unfixable {len(unfixable)})")
    result = search_title(title)
    if result is None:
        unfixable.append({**m, "reason": "no_pubmed_match"})
        continue
    pmid, ret_title, ov, yr, journal, authors = result
    if ov >= 0.50:
        fixes.append({
            "src_id": m["src_id"], "old_pmid": m["pmid"], "new_pmid": pmid,
            "old_title": title, "new_title": ret_title, "overlap": round(ov, 2),
            "year": yr, "journal": journal, "authors": ", ".join(authors),
        })
    elif ov >= 0.30:
        flagged.append({**m, "candidate_pmid": pmid, "candidate_title": ret_title,
                       "candidate_overlap": round(ov, 2),
                       "candidate_year": yr, "candidate_journal": journal,
                       "candidate_authors": ", ".join(authors)})
    else:
        unfixable.append({**m, "reason": "low_overlap_with_top_candidate", "best_candidate": pmid, "best_overlap": round(ov,2)})
    time.sleep(0.2)

# Final checkpoint
with open(CKPT, "w") as f:
    json.dump({"fixes": fixes, "flagged": flagged, "unfixable": unfixable, "next_idx": len(mismatches), "complete": True}, f)

print(f"\nResults: {len(fixes)} high-confidence fixes, {len(flagged)} flagged for review, {len(unfixable)} unfixable")

# === Apply fixes to sources.csv (v2.0_scored AND v2.0.1_expanded) ===
import datetime as dt
NOW = dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')

if fixes:
    fix_map = {f["src_id"]: f for f in fixes}
    for d in [ROOT/"v2.0_scored", ROOT/"v2.0.1_expanded"]:
        path = d / "sources.csv"
        rows = list(csv.DictReader(open(path)))
        fields = list(csv.DictReader(open(path)).fieldnames)
        n = 0
        for r in rows:
            if r["id"] not in fix_map: continue
            fix = fix_map[r["id"]]
            r["external_id"] = fix["new_pmid"]
            r["title"] = fix["new_title"]
            r["url"] = f"https://pubmed.ncbi.nlm.nih.gov/{fix['new_pmid']}/"
            r["date_published"] = f"{fix['year']}-01-01" if fix["year"] else r["date_published"]
            try:
                meta = json.loads(r.get("raw_metadata", "{}") or "{}")
            except:
                meta = {}
            meta.update({"pmid": fix["new_pmid"], "year": fix["year"],
                        "journal": fix["journal"],
                        "pmid_corrected_from": fix["old_pmid"],
                        "pmid_correction_date": NOW,
                        "pmid_correction_overlap": fix["overlap"],
                        "verified_against_pubmed": True})
            r["raw_metadata"] = json.dumps(meta)
            note_extra = (f" [PMID corrected from {fix['old_pmid']} → {fix['new_pmid']} "
                         f"on {NOW[:10]} via title-search verification (overlap {fix['overlap']})]")
            if note_extra not in (r.get("notes") or ""):
                r["notes"] = (r.get("notes","") or "") + note_extra
            n += 1
        with open(path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
        print(f"  {d.name}/sources.csv: {n} rows updated")

# Write reports
out = ROOT / "v2.0.1_proposed"
out.mkdir(exist_ok=True)
with open(out / "pmid_fixes_applied.json", "w") as f:
    json.dump({"fixes": fixes, "flagged": flagged, "unfixable": unfixable}, f, indent=2)

print(f"\nReports written to {out}/pmid_fixes_applied.json")
print(f"\nSUMMARY:")
print(f"  HIGH-CONFIDENCE FIXES APPLIED: {len(fixes)}")
print(f"  FLAGGED FOR REVIEW (0.30-0.50): {len(flagged)}")
print(f"  UNFIXABLE: {len(unfixable)}")
