#!/usr/bin/env python3
"""
Combined Session 1 leftovers + Session 3 source-quality audit.

Tasks:
  1. Audit ALL 894 PubMed sources by pubtype (not just 'other').
     Reclassify any Editorial/Letter/Comment/News found at any tier.
  2. Classify YouTube sources by channel pattern (academic/clinical/news/advocacy).
     Down-weight advocacy.
  3. Grep all hypothesis/intervention descriptions for COVID/flu vaccine
     refs in prevention messaging.
  4. Patch build_vault.py to render source-level `notes` field.
  5. Archive v2.0.1_proposed/ intermediate files.

Updates both v2.0_scored and v2.0.1_expanded.
"""

import csv, datetime as dt, json, re, time, urllib.parse, urllib.request, shutil
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC_DIR = ROOT / "v2.0_scored"
EXP_DIR = ROOT / "v2.0.1_expanded"
PROP_DIR = ROOT / "v2.0.1_proposed"
NOW = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
def http(url):
    req = urllib.request.Request(url, headers={"User-Agent": "causes-atlas/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r: return r.read().decode()

# ============================================================
# TASK 1: Full PubMed pubtype audit (all 894, not just 'other')
# ============================================================
print("=" * 60)
print("TASK 1: Full PubMed pubtype audit (all 894 sources)")
print("=" * 60)

sources = list(csv.DictReader(open(SRC_DIR / "sources.csv")))
pubmed = [s for s in sources if s["platform"] == "pubmed"]
all_pmids = [s["external_id"] for s in pubmed if s["external_id"]]
print(f"Querying pubtype for {len(all_pmids)} PubMed sources in batches…")

pubtypes = {}
for i in range(0, len(all_pmids), 100):
    batch = all_pmids[i:i+100]
    try:
        d = json.loads(http(f"{EUTILS}/esummary.fcgi?db=pubmed&retmode=json&id={','.join(batch)}"))['result']
        for p in d.get('uids', []):
            pubtypes[p] = d.get(p, {}).get('pubtype', [])
        time.sleep(0.35)
    except Exception as e:
        print(f"  WARN: batch {i//100} failed: {e}")
        time.sleep(2)

# Map pubtype to study_design
EDITORIAL_TYPES = {'Editorial', 'Letter', 'Comment', 'News', 'Personal Narrative',
                   'Interview', 'Biography', 'Address', 'Newspaper Article'}
def map_pubtype(pubtype_list):
    if 'Editorial' in pubtype_list: return 'editorial'
    if 'News' in pubtype_list or 'Newspaper Article' in pubtype_list: return 'news'
    if 'Letter' in pubtype_list: return 'letter'
    if 'Comment' in pubtype_list: return 'comment'
    if 'Personal Narrative' in pubtype_list or 'Biography' in pubtype_list \
       or 'Interview' in pubtype_list or 'Address' in pubtype_list: return 'narrative'
    return None

reclassifications = {}
for s in pubmed:
    pmid = s["external_id"]
    pt = pubtypes.get(pmid, [])
    new_design = map_pubtype(pt)
    if new_design and s["study_design"] != new_design:
        reclassifications[s["id"]] = (s["study_design"], new_design, pt)

print(f"  {len(reclassifications)} sources to reclassify")
type_counter = Counter(v[1] for v in reclassifications.values())
print(f"  Distribution: {dict(type_counter)}")

# Apply reclassifications
for d in [SRC_DIR, EXP_DIR]:
    p = d / "sources.csv"
    rows = list(csv.DictReader(open(p)))
    fields = list(csv.DictReader(open(p)).fieldnames)
    changed = 0
    for r in rows:
        if r["id"] in reclassifications:
            r["study_design"] = reclassifications[r["id"]][1]
            changed += 1
    with open(p, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
    print(f"  {d.name}/sources.csv: {changed} reclassified")

# Save audit log
with open(PROP_DIR / "pubmed_full_audit_session3.json", "w") as f:
    json.dump({
        "run_at": NOW,
        "total_pubmed_audited": len(all_pmids),
        "reclassified": [
            {"source_id": sid, "old": old, "new": new, "pubtypes": pt}
            for sid, (old, new, pt) in reclassifications.items()
        ],
    }, f, indent=2)
print(f"  Audit log: v2.0.1_proposed/pubmed_full_audit_session3.json")


# ============================================================
# TASK 2: YouTube channel classification
# ============================================================
print()
print("=" * 60)
print("TASK 2: YouTube channel classification")
print("=" * 60)

yt = [s for s in sources if s["platform"] == "youtube"]

# Channel patterns extracted from `notes` field (format: "channel: NAME · ...")
def get_channel(s):
    notes = s.get("notes") or ""
    m = re.match(r'channel:\s*([^·]+)', notes)
    if m: return m.group(1).strip()
    return ""

# Classify
ACADEMIC_PATTERNS = [
    'autism research institute', 'mind institute', 'uc davis health',
    'harvard medical', 'stanford', 'mayo clinic', 'cleveland clinic',
    'massachusetts general', 'autism science foundation', 'nih ',
    'national institutes', 'academy of pediatrics',
    'columbia university', 'hopkins', 'duke ', 'penn medicine',
    'autism speaks', 'autism canada',
]
CLINICAL_PATTERNS = [
    'doctor', 'dr.', 'dr ', 'md,', 'md ', ', md', 'phd ',
    ', phd', 'ms,', 'lcsw',
]
NEWS_PATTERNS = [
    'news', 'cnn', 'cbs', 'fox', 'abc', 'nbc', 'cnbc', 'bbc',
    'reuters', 'bloomberg', 'wsj', 'washington post', 'nytimes',
    'newsnation', 'newsmax',
]
ADVOCACY_PATTERNS = [
    "children's health defense", 'childrenshealthdefense',
    'highwire', 'del bigtree', 'del-bigtree',
    'rfk', 'kennedy jr',
    'james lyons-weiler', 'lyons-weiler',
    'ican', 'informed consent action',
    'autism action network', 'safeminds',
    'vaccine choice', 'naturalnews', 'natural news',
    'mercola', 'mike adams',
]

def classify_yt(s):
    ch = get_channel(s).lower()
    title = (s.get("title") or "").lower()
    text = ch + " " + title
    for pat in ADVOCACY_PATTERNS:
        if pat in text: return 'advocacy'
    for pat in NEWS_PATTERNS:
        if pat in text: return 'news_video'
    for pat in ACADEMIC_PATTERNS:
        if pat in text: return 'academic_lecture'
    for pat in CLINICAL_PATTERNS:
        if pat in text: return 'clinical_explainer'
    return 'social'  # default — keep current

yt_class = Counter()
yt_reclass = {}
for s in yt:
    cls = classify_yt(s)
    yt_class[cls] += 1
    if cls in ('advocacy', 'news_video', 'academic_lecture', 'clinical_explainer'):
        yt_reclass[s["id"]] = cls

print(f"  YouTube classification:")
for c, n in yt_class.most_common():
    print(f"    {c}: {n}")

# Apply: type field changes (and study_design if applicable)
# advocacy -> type='advocacy' (W_SOURCE_TYPE 0.05)
# news_video -> type='social', study_design='news' (W_DESIGN 0.05)
# academic_lecture -> type='social' (keep), but mark notes
# clinical_explainer -> type='social' (keep), but mark notes
TYPE_MAP = {'advocacy': 'advocacy', 'news_video': 'social',
            'academic_lecture': 'social', 'clinical_explainer': 'social'}
DESIGN_MAP = {'news_video': 'news'}

for d in [SRC_DIR, EXP_DIR]:
    p = d / "sources.csv"
    rows = list(csv.DictReader(open(p)))
    fields = list(csv.DictReader(open(p)).fieldnames)
    changed = 0
    for r in rows:
        if r["id"] in yt_reclass:
            cls = yt_reclass[r["id"]]
            if cls in TYPE_MAP:
                r["type"] = TYPE_MAP[cls]
            if cls in DESIGN_MAP:
                r["study_design"] = DESIGN_MAP[cls]
            # tag in notes
            cur_notes = r.get("notes", "") or ""
            if f"yt_classified={cls}" not in cur_notes:
                r["notes"] = (cur_notes + " | " if cur_notes else "") + f"yt_classified={cls}"
            changed += 1
    with open(p, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
    print(f"  {d.name}/sources.csv: {changed} YouTube sources reclassified")


# ============================================================
# TASK 3: Grep prevention narratives for COVID/flu refs
# ============================================================
print()
print("=" * 60)
print("TASK 3: Audit prevention narratives for COVID/flu vaccine refs")
print("=" * 60)

PHRASES_TO_REMOVE = [
    "COVID vaccin", "covid vaccin", "Covid vaccin",
    "flu shot", "flu vaccin", "Flu shot", "Flu vaccin",
    "influenza vaccin", "Influenza vaccin",
]

# Search through hypothesis descriptions, intervention notes/descriptions
files_to_check = ['hypotheses.csv', 'interventions.csv', 'mechanisms.csv',
                  'phenotypes.csv', 'combinations.csv']
audit_hits = []
for fname in files_to_check:
    p = SRC_DIR / fname
    rows = list(csv.DictReader(open(p)))
    for r in rows:
        for col in ['description', 'notes', 'mechanism_summary', 'rationale',
                    'interaction_warnings']:
            txt = (r.get(col) or "")
            for phrase in PHRASES_TO_REMOVE:
                if phrase in txt:
                    audit_hits.append({
                        "file": fname, "id": r["id"],
                        "column": col, "phrase": phrase,
                        "context": txt[max(0,txt.find(phrase)-30):txt.find(phrase)+80]
                    })

print(f"  Found {len(audit_hits)} mentions of COVID/flu vaccine in atlas text")
for h in audit_hits[:10]:
    print(f"    {h['file']} {h['id']} [{h['column']}] '{h['phrase']}': ...{h['context']}...")
print(f"  (No automatic removal — these are description text. List saved for manual review.)")

with open(PROP_DIR / "covid_flu_vaccine_refs_to_review.json", "w") as f:
    json.dump(audit_hits, f, indent=2)


# ============================================================
# TASK 4: Patch build_vault.py to render source notes
# ============================================================
print()
print("=" * 60)
print("TASK 4: Patch build_vault.py to render source-level notes")
print("=" * 60)

bvp = ROOT / "build_vault.py"
content = bvp.read_text()
# Find the source-rendering section and add notes after PMID/DOI
old_block = '''    if pmid:
        body.append(f"\\n**PMID:** {pmid}\\n")
    if doi:
        body.append(f"\\n**DOI:** {doi}\\n")

    # Evidence fragments'''
new_block = '''    if pmid:
        body.append(f"\\n**PMID:** {pmid}\\n")
    if doi:
        body.append(f"\\n**DOI:** {doi}\\n")
    if s.get("notes"):
        body.append(f"\\n**Notes / methodological caveats:** {s['notes']}\\n")

    # Evidence fragments'''
if old_block in content:
    content = content.replace(old_block, new_block)
    bvp.write_text(content)
    print("  build_vault.py patched — source notes will now render in vault")
else:
    print("  WARN: build_vault.py block not found verbatim; manual check needed")


# ============================================================
# TASK 5: Archive v2.0.1_proposed/ intermediate files
# ============================================================
print()
print("=" * 60)
print("TASK 5: Archive v2.0.1_proposed/ intermediate files")
print("=" * 60)

archive = PROP_DIR / "_archived_session_iterations"
archive.mkdir(exist_ok=True)

# Files to archive (intermediate iterations from today's work)
to_archive = [
    "abstracts.txt", "abstracts.json", "abstract_review.md",
    "candidate_orphan_edges_REJECTED_memory_based.csv",
    "opinion_pieces_to_downweight.json",
    "hypothesis_phenotype_proposed.csv",
]
moved = 0
for fn in to_archive:
    p = PROP_DIR / fn
    if p.exists():
        try:
            shutil.move(str(p), str(archive / fn))
            moved += 1
        except OSError as e:
            print(f"  could not move {fn}: {e}")

print(f"  Archived {moved} intermediate files to v2.0.1_proposed/_archived_session_iterations/")

# Show what remains as "active" proposals
remaining = sorted([p.name for p in PROP_DIR.iterdir() if p.is_file()])
print(f"  Active proposals remaining ({len(remaining)}):")
for r in remaining:
    print(f"    {r}")


print()
print("Session 3 cleanup complete.")
print("Next: re-run scoring + verify INT-0001 calibration + rebuild vault.")
