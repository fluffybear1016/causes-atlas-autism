#!/usr/bin/env python3
"""
patch_iep_evidence_balance_v02.py

Apply targeted evidence-balance population to iatrogenic_exposure_priors.csv.
Every PMID in PATCHES below has been pre-verified against PubMed esummary.
Idempotent: safe to re-run.

Verified-clean PMIDs used in this patch:
  - 12421889 Madsen 2002 NEJM (MMR/autism null)
  - 15877763 Honda 2005 J Child Psychol Psychiatry (Yokohama natural experiment)
  - 19128068 Gerber & Offit 2009 Clin Infect Dis (vaccine-autism review)
  - 22001122 Mitkus 2011 Vaccine (aluminum pharmacokinetics — already present)
  - 26948677 Gherardi 2016 Morphologie (aluminum harm position)
  - 30831578 Hviid 2019 Ann Intern Med (MMR cohort 657k children)
  - 30986133 DeStefano & Shimabukuro 2019 Annu Rev Virol (MMR review)
  - 40658954 Andersson 2025 Ann Intern Med (Danish aluminum-adsorbed-vaccines cohort)
  - 41468671 Crépeaux 2026 J Trace Elem Med Biol (aluminum-harm position 2026)

Per CLAUDE.md verify-before-write hard rule.
"""
from __future__ import annotations
import csv
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CSV_PATH = REPO / "v2.0_scored" / "iatrogenic_exposure_priors.csv"

# Patches keyed by row id. Each value can specify:
#   - primary_pmids_set: replace primary_pmids with this set (semicolon-joined)
#   - countervailing_pmids_set: replace countervailing with this set
#   - notes_append: append text to notes field
#   - notes_search_replace: dict for in-place text fix
PATCHES = {
    "IEP-00021": {
        "primary_pmids_set": "15877763;12421889;30831578;30986133;19128068",
        "countervailing_pmids_set": "",  # Wakefield 1998 retracted; FOIA contested evidence in atlas as SRC-001415..001419
        "notes_append": (
            " | v0.2 Move 3: primary_pmids strengthened with Madsen 2002 NEJM (PMID 12421889), "
            "Hviid 2019 Ann Intern Med (PMID 30831578), DeStefano 2019 Annu Rev Virol (PMID 30986133), "
            "Gerber & Offit 2009 Clin Infect Dis (PMID 19128068). Countervailing-evidence position "
            "is documented in atlas FOIA sources SRC-001415..001419 (not PMID-citeable); "
            "Wakefield 1998 retracted and excluded."
        ),
    },
    "IEP-00026": {
        "primary_pmids_set": "22001122;40658954",
        "countervailing_pmids_set": "26948677;41468671",
        "notes_append": (
            " | v0.2 Move 3: primary_pmids strengthened with Andersson 2025 Ann Intern Med Danish "
            "nationwide cohort (PMID 40658954). Countervailing-evidence-position populated with "
            "Gherardi 2016 Morphologie (PMID 26948677) and Crépeaux 2026 J Trace Elem Med Biol "
            "(PMID 41468671) per epistemic balance requirement."
        ),
    },
}


def main():
    if not CSV_PATH.exists():
        print(f"ERROR: {CSV_PATH} not found", file=sys.stderr)
        sys.exit(2)

    with open(CSV_PATH, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)
        rows = list(reader)

    changes = 0
    for r in rows:
        rid = r.get("id")
        if rid not in PATCHES:
            continue
        patch = PATCHES[rid]
        before = (r.get("primary_pmids", ""), r.get("countervailing_evidence_pmids", ""), r.get("notes", ""))

        if "primary_pmids_set" in patch:
            r["primary_pmids"] = patch["primary_pmids_set"]
        if "countervailing_pmids_set" in patch:
            r["countervailing_evidence_pmids"] = patch["countervailing_pmids_set"]
        if "notes_append" in patch:
            existing = r.get("notes", "") or ""
            # Idempotent: don't append if marker already present
            marker = "v0.2 Move 3"
            if marker not in existing:
                r["notes"] = existing + patch["notes_append"]

        after = (r.get("primary_pmids", ""), r.get("countervailing_evidence_pmids", ""), r.get("notes", ""))
        if before != after:
            changes += 1
            print(f"  patched {rid}:")
            if before[0] != after[0]:
                print(f"    primary_pmids: '{before[0]}' → '{after[0]}'")
            if before[1] != after[1]:
                print(f"    countervailing: '{before[1]}' → '{after[1]}'")

    if changes == 0:
        print("No changes needed (already up to date or no matching rows).")
        return

    with open(CSV_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nWrote {changes} row patches to {CSV_PATH}")


if __name__ == "__main__":
    main()
