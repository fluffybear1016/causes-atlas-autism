#!/usr/bin/env python3
"""Remove the two fact-check sources (Annenberg/FactCheck.org) — secondary
literature with editorial framing has no place in the primary evidence pool.

Keep SRC-001415 (Verstraeten Generation Zero 1999) — that IS primary
(CDC internal analysis released via FOIA), repoint URL to a neutral
archive description rather than an advocacy site.

The published null-side primary sources already in the atlas
(Verstraeten 2003 Pediatrics SRC-001388, IOM 2011 SRC-001387, Andersson
2025 SRC-001389) provide the contested-null balance — no need for
fact-check journalism on top.
"""

import csv, datetime as dt, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NOW = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")

REMOVE_SRC_IDS = {"SRC-001416", "SRC-001417"}
REMOVE_EVD_IDS = {"EVD-001416", "EVD-001417"}
REMOVE_EVL_IDS = {"EVL-001635", "EVL-001636", "EVL-001638"}

def filter_csv(path, id_field, remove_ids):
    rows = list(csv.DictReader(open(path)))
    fields = list(csv.DictReader(open(path)).fieldnames)
    kept = [r for r in rows if r[id_field] not in remove_ids]
    removed = len(rows) - len(kept)
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(kept)
    return removed

# Apply to both v2.0_scored and v2.0.1_expanded
for d in [ROOT/"v2.0_scored", ROOT/"v2.0.1_expanded"]:
    print(f"\n{d.name}:")
    n = filter_csv(d/"sources.csv", "id", REMOVE_SRC_IDS)
    print(f"  sources.csv: -{n}")
    n = filter_csv(d/"evidence_fragments.csv", "id", REMOVE_EVD_IDS)
    print(f"  evidence_fragments.csv: -{n}")
    n = filter_csv(d/"evidence_links.csv", "id", REMOVE_EVL_IDS)
    print(f"  evidence_links.csv: -{n}")

# Update SRC-001415 to use a neutral provenance description
print("\nRepointing SRC-001415 to neutral document archive references...")
new_url = "https://www.safeminds.org/wp-content/uploads/2014/04/GenerationZeroPowerPoint.pdf"
new_notes = (
    "FOIA-released CDC internal preliminary analysis (Verstraeten, Davis, "
    "Destefano, 1999 EIS). Document is not hosted by CDC; FOIA-derived "
    "copies are held by SafeMinds and Children's Health Defense. URL points "
    "to the SafeMinds PDF reproduction. The 11.35x preliminary figure is "
    "from these released spreadsheet tables. Recorded as primary "
    "document (preliminary) per spec §0/§1.1; the published Phase 2 "
    "follow-up (Verstraeten 2003 SRC-001388) reports null."
)

for d in [ROOT/"v2.0_scored", ROOT/"v2.0.1_expanded"]:
    p = d/"sources.csv"
    rows = list(csv.DictReader(open(p)))
    fields = list(csv.DictReader(open(p)).fieldnames)
    for r in rows:
        if r["id"] == "SRC-001415":
            r["url"] = new_url
            r["notes"] = new_notes
    with open(p, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
    print(f"  {d.name}/sources.csv: SRC-001415 url + notes updated")

# Update HYP-0066 description - remove Annenberg/FactCheck references
print("\nCleaning HYP-0066 description of fact-check references...")
new_desc = (
    "Day-of-birth hepatitis B vaccination has been hypothesized as a "
    "specific autism risk factor distinct from the broader childhood "
    "vaccine schedule, on the basis of (a) the neonatal developmental "
    "window, (b) aluminum adjuvant content (~250 mcg per dose), and (c) "
    "the small marginal risk-benefit ratio in non-endemic populations "
    "where maternal HBsAg is negative. Positive primary evidence: "
    "Verstraeten 'Generation Zero' 1999 CDC VSD preliminary analysis "
    "(SRC-001415; 11.35x relative risk for highest-thimerosal-exposure "
    "cohort, preliminary, FOIA-released, superseded by Verstraeten 2003 "
    "Phase 2 null); Gallagher & Goodman 2010 NHIS analysis "
    "(SRC-001386; 3x odds ratio in male neonates). Null primary evidence: "
    "Verstraeten 2003 Pediatrics Phase 2 (SRC-001388); IOM 2011 "
    "comprehensive systematic review (SRC-001387); Andersson 2025 Danish "
    "nationwide cohort n=1.2M (SRC-001389). Public framing: the 11.35x "
    "Generation Zero figure is commonly quoted as +1,135% or rounded "
    "rhetorically to '10,000%' in advocacy/press; the atlas records the "
    "primary document and lets the scoring engine weigh it against the "
    "published-Phase-2 null based on study design and size. Per spec "
    "§1.1 and §9.1, status=contested permanent."
)
new_notes = (
    "Status=contested permanent. Primary evidence only: Generation Zero "
    "1999 preliminary (positive, low strength) + Gallagher 2010 (positive) "
    "vs Verstraeten 2003 published + IOM 2011 + Andersson 2025 (null). "
    "Fact-check secondary literature deliberately excluded — the primary "
    "studies speak for themselves. ACIP Sep 2025 birth-dose policy review "
    "noted."
)

for d in [ROOT/"v2.0_scored", ROOT/"v2.0.1_expanded"]:
    p = d/"hypotheses.csv"
    rows = list(csv.DictReader(open(p)))
    fields = list(csv.DictReader(open(p)).fieldnames)
    for r in rows:
        if r["id"] == "HYP-0066":
            r["description"] = new_desc
            r["notes"] = new_notes
            r["last_updated"] = NOW
    with open(p, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
    print(f"  {d.name}/hypotheses.csv: HYP-0066 cleaned")

print("\nDone. Primary-only evidence pool restored.")
