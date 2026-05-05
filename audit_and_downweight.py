#!/usr/bin/env python3
"""
Audit existing sources and down-weight opinion / editorial / advocacy
content per spec §0 mission ('preserve uncertainty and contradiction')
balanced against user directive ('pure science not opinion').

Three actions:
  1. Reclassify the 27 flagged PubMed editorials/letters/comments/news from
     study_design='other' to study_design=<editorial|letter|comment|news>.
     The scoring engine's W_DESIGN dict needs these weights added.
  2. Add low-weight entries to W_DESIGN in run_scoring_v20.py:
       editorial=0.10, letter=0.10, comment=0.10, news=0.05,
       internal_doc / cdc_foia / court_ruling = appropriate primary weights
  3. Audit YouTube source channel/title patterns; reclassify clearly
     advocacy-channel content from type='social' to type='advocacy' (which
     the engine doesn't have, so it'll default low at 0.40 ... or we add
     advocacy=0.10 to W_SOURCE_TYPE).

Effect: the scoring engine recomputes strength_score from study_design + type
on next run, automatically down-weighting these sources without any
strength_score table modification.
"""
import csv, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# ============================================================
# STEP 1: reclassify the 27 flagged PubMed editorials
# ============================================================
flagged = json.load(open(ROOT/'v2.0.1_proposed/opinion_pieces_to_downweight.json'))

def map_pubtype_to_design(pubtypes):
    if 'Editorial' in pubtypes: return 'editorial'
    if 'News' in pubtypes: return 'news'
    if 'Letter' in pubtypes: return 'letter'
    if 'Comment' in pubtypes: return 'comment'
    return 'other'

src_id_to_design = {f['source_id']: map_pubtype_to_design(f['pubtypes']) for f in flagged}

print(f"STEP 1: Reclassifying {len(src_id_to_design)} PubMed sources from study_design='other'")
for d in [ROOT/'v2.0_scored', ROOT/'v2.0.1_expanded']:
    p = d/'sources.csv'
    rows = list(csv.DictReader(open(p)))
    fields = list(csv.DictReader(open(p)).fieldnames)
    changed = 0
    for r in rows:
        if r['id'] in src_id_to_design:
            r['study_design'] = src_id_to_design[r['id']]
            changed += 1
    with open(p, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
    print(f"  {d.name}/sources.csv: {changed} rows reclassified")

# ============================================================
# STEP 2: audit YouTube sources and flag advocacy channels
# ============================================================
sources = list(csv.DictReader(open(ROOT/'v2.0_scored/sources.csv')))
yt = [s for s in sources if s['platform'] == 'youtube']

# Channel patterns that indicate advocacy/opinion (not academic/clinical)
ADVOCACY_PATTERNS = [
    'children\'s health defense', 'childrenshealthdefense',
    'highwirewithdelbigtree', 'highwire', 'del bigtree',
    'rfk jr', 'robertfkennedyjr', 'robert kennedy',
    'james lyons-weiler', 'lyons-weiler',
    'mary holland', 'maryhollandical',
    'ican', 'informed consent action network',
    'autism action network',
    'vaccinerisksawareness', 'vaccinechoice',
    # 'natural news' - misinformation site
    'naturalnews',
]
# Conversely, academic / clinical patterns to keep at current weight
ACADEMIC_PATTERNS = [
    'autism research institute', 'tacanow', 'taca',
    'stanford university', 'harvard medical', 'nih',
    'mayo clinic', 'cleveland clinic', 'massachusetts general',
    'autism science foundation', 'autism speaks',
    'doctor', 'md ', ' md,', 'professor', 'phd',
]

advocacy_yt = []
academic_yt = []
unclassified_yt = []
for s in yt:
    t = (s.get('title') or '').lower()
    u = (s.get('url') or '').lower()
    n = (s.get('notes') or '').lower()
    text = f"{t} {u} {n}"
    if any(p in text for p in ADVOCACY_PATTERNS):
        advocacy_yt.append(s)
    elif any(p in text for p in ACADEMIC_PATTERNS):
        academic_yt.append(s)
    else:
        unclassified_yt.append(s)

print()
print(f"STEP 2: YouTube source audit ({len(yt)} total)")
print(f"  advocacy patterns matched: {len(advocacy_yt)}")
print(f"  academic patterns matched: {len(academic_yt)}")
print(f"  unclassified (kept at current weight): {len(unclassified_yt)}")

# Reclassify advocacy YouTube to type='advocacy'
print()
print(f"  Reclassifying {len(advocacy_yt)} advocacy YouTube sources type=social -> type=advocacy")
advocacy_ids = {s['id'] for s in advocacy_yt}
for d in [ROOT/'v2.0_scored', ROOT/'v2.0.1_expanded']:
    p = d/'sources.csv'
    rows = list(csv.DictReader(open(p)))
    fields = list(csv.DictReader(open(p)).fieldnames)
    changed = 0
    for r in rows:
        if r['id'] in advocacy_ids:
            r['type'] = 'advocacy'
            changed += 1
    with open(p, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
    print(f"    {d.name}/sources.csv: {changed} rows reclassified")

# ============================================================
# STEP 3: patch W_DESIGN and W_SOURCE_TYPE in run_scoring_v20.py
# ============================================================
print()
print("STEP 3: Patching W_DESIGN + W_SOURCE_TYPE in run_scoring_v20.py")
script = ROOT/'run_scoring_v20.py'
content = script.read_text()

# Replace W_DESIGN block
old_wdesign = '''W_DESIGN = {
    "meta_analysis": 1.00, "rct": 0.95, "cohort": 0.75, "case_control": 0.70,
    "case_series": 0.45, "mechanistic": 0.35, "review": 0.55,
    "animal": 0.30, "in_vitro": 0.25, "in_silico": 0.20,
    "epigenetic": 0.50, "transgenerational": 0.50, "other": 0.50, "": 0.40,
}'''
new_wdesign = '''W_DESIGN = {
    "meta_analysis": 1.00, "rct": 0.95, "cohort": 0.75, "case_control": 0.70,
    "case_series": 0.45, "mechanistic": 0.35, "review": 0.55,
    "animal": 0.30, "in_vitro": 0.25, "in_silico": 0.20,
    "epigenetic": 0.50, "transgenerational": 0.50, "other": 0.50, "": 0.40,
    # Primary documents (FOIA / federal record / advisory)
    "natural_experiment": 0.85,
    "preliminary_analysis": 0.30,
    "internal_meeting_transcript": 0.30,
    "internal_correspondence": 0.20,
    "federal_court_ruling": 0.40,
    "whistleblower_statement": 0.20,
    "advisory_committee_review": 0.30,
    # Secondary literature / opinion (down-weighted)
    "editorial": 0.10, "letter": 0.10, "comment": 0.10, "news": 0.05,
    "factcheck_review": 0.05,
}'''

old_wstype = '''W_SOURCE_TYPE = {
    "study": 1.00, "meta_analysis": 1.00, "review": 0.70, "preprint": 0.85,
    "clinical": 0.90, "registry": 0.85, "dataset": 0.80, "trial": 0.95,
    "environmental": 0.70, "anecdote": 0.15, "social": 0.10, "other": 0.40,
}'''
new_wstype = '''W_SOURCE_TYPE = {
    "study": 1.00, "meta_analysis": 1.00, "review": 0.70, "preprint": 0.85,
    "clinical": 0.90, "registry": 0.85, "dataset": 0.80, "trial": 0.95,
    "environmental": 0.70, "anecdote": 0.15, "social": 0.10, "other": 0.40,
    # Primary documents
    "internal_doc": 0.50, "court_ruling": 0.70, "policy_document": 0.40,
    # Secondary editorial / advocacy (down-weighted)
    "advocacy": 0.05, "factcheck": 0.10, "opinion": 0.10,
}'''

if old_wdesign in content:
    content = content.replace(old_wdesign, new_wdesign)
    print("  W_DESIGN patched")
else:
    print("  WARNING: W_DESIGN block not found verbatim — manual check needed")

if old_wstype in content:
    content = content.replace(old_wstype, new_wstype)
    print("  W_SOURCE_TYPE patched")
else:
    print("  WARNING: W_SOURCE_TYPE block not found verbatim — manual check needed")

script.write_text(content)
print("  run_scoring_v20.py written")
print()
print("Done. Run scoring next, then rebuild vault.")
