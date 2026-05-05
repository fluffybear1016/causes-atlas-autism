#!/usr/bin/env python3
"""Retry script for unfixable cases using shorter keyword queries."""
import csv, json, re, urllib.request, urllib.parse, time, datetime as dt
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
NOW = dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')

def http(url):
    req = urllib.request.Request(url, headers={"User-Agent": "causes-atlas/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r: return r.read().decode()

def title_overlap(a, b, min_len=5):
    aw = set(w.lower() for w in re.findall(r"[A-Za-z]+", a) if len(w) >= min_len)
    bw = set(w.lower() for w in re.findall(r"[A-Za-z]+", b) if len(w) >= min_len)
    if not aw or not bw: return 0.0
    return len(aw & bw) / min(len(aw), len(bw))

def smart_search(title):
    """More aggressive search: extract distinctive keywords."""
    # Strategy 1: Take first 8 distinctive words
    words = [w for w in re.findall(r"[A-Za-z]+", title) if len(w) >= 5]
    # Skip very common autism-research words to keep query distinctive
    skip = {"autism", "spectrum", "disorder", "children", "study", "review", "analysis", "trial"}
    keywords = [w for w in words if w.lower() not in skip][:8]
    if len(keywords) < 3: keywords = words[:8]

    queries = [
        " ".join(keywords[:6]),  # most distinctive 6
        " ".join(keywords[:8]),  # 8 keywords
        " ".join(words[:6]) + " autism",  # 6 + autism
    ]

    for q in queries:
        try:
            url = f"{EUTILS}/esearch.fcgi?db=pubmed&retmode=json&retmax=5&term={urllib.parse.quote(q)}"
            d = json.loads(http(url))
            ids = d.get("esearchresult", {}).get("idlist", [])
            if not ids:
                time.sleep(0.2); continue
            time.sleep(0.2)
            d2 = json.loads(http(f"{EUTILS}/esummary.fcgi?db=pubmed&retmode=json&id={','.join(ids[:5])}"))
            best = None
            for pmid in ids[:5]:
                r = d2.get("result", {}).get(pmid, {})
                if not r.get("title"): continue
                ov = title_overlap(title, r["title"])
                if best is None or ov > best[2]:
                    best = (pmid, r["title"], ov,
                            r.get("pubdate","")[:4], r.get("source",""),
                            [a.get("name","") for a in r.get("authors",[])[:3]])
            if best and best[2] >= 0.50:
                return best
            time.sleep(0.2)
        except:
            time.sleep(0.2); continue
    return None

# Load previous fix output
prev = json.loads(open(ROOT/"v2.0.1_proposed"/"pmid_fixes_applied.json").read())
unfixable = prev["unfixable"]
print(f"Retrying {len(unfixable)} unfixable cases with smarter queries…")

CKPT = ROOT / "v2.0.1_proposed" / "pmid_retry_checkpoint.json"
if CKPT.exists():
    cp = json.loads(open(CKPT).read())
    new_fixes = cp.get("new_fixes", [])
    flagged = cp.get("flagged", [])
    still_unfixable = cp.get("still_unfixable", [])
    start_idx = cp.get("next_idx", 0)
    print(f"Resuming retry at index {start_idx}")
else:
    new_fixes = []; still_unfixable = []; flagged = []; start_idx = 0

for i in range(start_idx, len(unfixable)):
    u = unfixable[i]
    if not u["atlas_title"].strip():
        still_unfixable.append({**u, "retry_reason": "empty_atlas_title"})
        continue
    if (i+1) % 3 == 0:
        with open(CKPT, "w") as f:
            json.dump({"new_fixes": new_fixes, "flagged": flagged, "still_unfixable": still_unfixable, "next_idx": i+1}, f)
        print(f"  {i+1}/{len(unfixable)} fixed={len(new_fixes)} flagged={len(flagged)} stuck={len(still_unfixable)}")
    result = smart_search(u["atlas_title"])
    if result is None:
        still_unfixable.append({**u, "retry_reason": "no_match_after_retry"})
        continue
    pmid, ret_title, ov, yr, journal, authors = result
    if ov >= 0.50:
        new_fixes.append({
            "src_id": u["src_id"], "old_pmid": u["pmid"], "new_pmid": pmid,
            "old_title": u["atlas_title"], "new_title": ret_title, "overlap": round(ov, 2),
            "year": yr, "journal": journal, "authors": ", ".join(authors),
        })
    else:
        flagged.append({**u, "candidate_pmid": pmid, "candidate_title": ret_title,
                       "candidate_overlap": round(ov,2)})
    time.sleep(0.2)

print(f"\nResults: {len(new_fixes)} new fixes, {len(flagged)} flagged, {len(still_unfixable)} still unfixable")

# Apply fixes
fix_map = {f["src_id"]: f for f in new_fixes}
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
        try: meta = json.loads(r.get("raw_metadata", "{}") or "{}")
        except: meta = {}
        meta.update({"pmid": fix["new_pmid"], "year": fix["year"], "journal": fix["journal"],
                    "pmid_corrected_from": fix["old_pmid"],
                    "pmid_correction_date": NOW,
                    "pmid_correction_overlap": fix["overlap"],
                    "pmid_correction_method": "smart_keyword_retry",
                    "verified_against_pubmed": True})
        r["raw_metadata"] = json.dumps(meta)
        n += 1
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
    print(f"  {d.name}/sources.csv: {n} additional rows updated")

# Save retry report
with open(ROOT/"v2.0.1_proposed"/"pmid_fixes_retry.json", "w") as f:
    json.dump({"new_fixes": new_fixes, "flagged": flagged, "still_unfixable": still_unfixable}, f, indent=2)
print(f"Retry report: {ROOT}/v2.0.1_proposed/pmid_fixes_retry.json")
