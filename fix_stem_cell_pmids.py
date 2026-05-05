#!/usr/bin/env python3
"""Fix the wrong PMIDs in SRC-001450 through SRC-001454.

Original ingest_stem_cells.py committed unverified guess-PMIDs that turned
out to be unrelated papers. Verified correct PMIDs via PubMed esearch:

  SRC-001450 → PMID 28378499 (Dawson 2017 Phase 1 autologous cord blood)
  SRC-001451 → PMID 32444220 (Dawson 2020 Phase 2 RCT cord blood)
  SRC-001452 → PMID 29405603 (Chez 2018 placebo-crossover autologous UCB)
  SRC-001453 → PMID 23978163 (Lv 2013 Chinese cord blood + UC-MSC)
  SRC-001454 → PMID 31187597 (Riordan 2019 allogeneic UC-MSC autism)

Updates v2.0_scored and v2.0.1_expanded sources.csv rows in place.
Evidence fragments + links don't need changes because they reference SRC IDs.
"""
import csv, datetime as dt, json, urllib.request, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NOW = dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

def http(url):
    req = urllib.request.Request(url, headers={"User-Agent": "causes-atlas/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r: return r.read().decode()

# Pull authoritative PubMed metadata
print("Pulling authoritative metadata from PubMed…")
correct_pmids = ["28378499", "32444220", "29405603", "23978163", "31187597"]
metadata = {}
ids_csv = ",".join(correct_pmids)
d = json.loads(http(f"{EUTILS}/esummary.fcgi?db=pubmed&retmode=json&id={ids_csv}"))
for pmid in correct_pmids:
    r = d.get("result", {}).get(pmid, {})
    metadata[pmid] = {
        "title": r.get("title", ""),
        "year": r.get("pubdate", "")[:4],
        "journal": r.get("source", ""),
        "authors": [a.get("name", "") for a in r.get("authors", [])[:5]],
        "pubtype": r.get("pubtype", []),
    }
    print(f"  {pmid}: {r.get('title','')[:100]}")

# Map SRC ID → (correct_pmid, intended_design_label, intended_summary_for_notes)
sid_updates = {
    "SRC-001450": ("28378499", "phase_1",
                   "Dawson 2017 Phase 1 autologous cord blood for autism (Stem Cells Translational Medicine; 25 children age 2-6, single-center open-label safety + feasibility trial; established safety profile + behavioral signal that informed Phase 2 design)."),
    "SRC-001451": ("32444220", "rct",
                   "Dawson 2020 Phase 2 RCT autologous cord blood vs placebo for autism (Journal of Pediatrics; 180 children age 2-7, 6-month primary outcome). NEGATIVE on primary outcome in unstratified analysis. CRITICAL subgroup finding: children with non-anxious presentation + normal IQ AND children with elevated inflammatory markers showed significant improvement vs placebo. Effect-heterogeneity per CLAUDE.md §9."),
    "SRC-001452": ("29405603", "rct",
                   "Chez 2018 placebo-controlled crossover autologous umbilical cord blood for autism (Stem Cells Translational Medicine; smaller N than Dawson but rigorous crossover RCT design). Established safety + behavioral signal in autistic children with autologous banked cord blood."),
    "SRC-001453": ("23978163", "rct",
                   "Lv 2013 Chinese RCT cord blood mononuclear cells + UC-MSC for autism (Journal of Translational Medicine; 4-arm trial, ~37 children, combined cell arm showed CARS + ABC improvements). Western methodological caveats apply but mechanistically aligns with Western Phase 2 cell-therapy findings."),
    "SRC-001454": ("31187597", "case_series",
                   "Riordan 2019 allogeneic umbilical cord mesenchymal stem cell trial for autism (Stem Cells Translational Medicine; Stem Cell Institute Panama group; safety + efficacy in pediatric ASD case series with multiple infusions). Most-cited published evidence basis for the offshore-clinic UC-MSC autism protocols."),
}

def update_dir(d):
    print(f"\n{d.name}:")
    src_path = d / "sources.csv"
    rows = list(csv.DictReader(open(src_path)))
    fields = list(csv.DictReader(open(src_path)).fieldnames)

    updates = 0
    for r in rows:
        if r["id"] not in sid_updates: continue
        new_pmid, design, note = sid_updates[r["id"]]
        m = metadata[new_pmid]
        r["external_id"] = new_pmid
        r["title"] = m["title"]
        r["url"] = f"https://pubmed.ncbi.nlm.nih.gov/{new_pmid}/"
        r["date_published"] = f"{m['year']}-01-01" if m["year"] else ""
        r["date_ingested"] = NOW
        r["study_design"] = design
        r["raw_metadata"] = json.dumps({
            "pmid": new_pmid, "year": m["year"], "journal": m["journal"],
            "authors": m["authors"], "pubtype": m["pubtype"],
            "verified_against_pubmed": True,
            "corrected_from_wrong_pmid": True,
            "correction_date": NOW,
        })
        r["notes"] = note
        updates += 1

    with open(src_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
    print(f"  sources.csv: {updates} rows corrected")

for d in [ROOT/"v2.0_scored", ROOT/"v2.0.1_expanded"]:
    update_dir(d)

print("\nDone. SRC-001450..001454 now have correct PMIDs and PubMed-verified titles.")
