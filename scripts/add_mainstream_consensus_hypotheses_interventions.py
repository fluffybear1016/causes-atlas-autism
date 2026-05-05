#!/usr/bin/env python3
"""
add_mainstream_consensus_hypotheses_interventions.py

Phase C — propagate Move 6 mainstream consensus rendering to hypotheses.csv
and interventions.csv. The single feature that immunizes the project against
bad-faith framing across the entire atlas, not just the iatrogenic table.

Adds `mainstream_consensus_position` column where missing and populates
for every contested row with neutral, factual mainstream-regulatory /
society-position content. Idempotent.
"""
from __future__ import annotations
import csv
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ATLAS_DIR = REPO / "v2.0_scored"

NEW_COLUMN = "mainstream_consensus_position"

HYPOTHESIS_CONSENSUS = {
    "HYP-0044": (  # Childhood vaccine exposure (contested)
        "WHO, CDC, AAP, NIH, and major medical societies recommend universal "
        "childhood vaccination per the standard schedule for prevention of "
        "vaccine-preventable infectious disease. Multiple large-scale cohort "
        "studies — Madsen 2002 NEJM (PMID 12421889), Hviid 2019 Ann Intern "
        "Med (PMID 30831578), DeStefano 2019 Annu Rev Virol (PMID 30986133) — "
        "find no association between MMR or other routine pediatric vaccines "
        "and autism at population level. Mainstream public-health position: "
        "benefit substantially exceeds risk at population level."
    ),
    "HYP-0054": (  # Acetaminophen postnatal
        "WHO and AAP consider acetaminophen the preferred analgesic and "
        "antipyretic for infants and young children when clinically indicated, "
        "due to the contraindication of NSAIDs and aspirin in this age group. "
        "The 2021 Bauer et al multi-author consensus statement (PMID 34507921) "
        "calling for precautionary minimization of pregnancy + early-life "
        "acetaminophen is an emerging signal, not a guideline change."
    ),
    "HYP-0066": (  # Hepatitis B birth-dose
        "WHO, AAP, ACIP recommend universal hepatitis B birth-dose vaccination. "
        "Vertical-transmission mortality reduction is well-established and "
        "outside dispute. ACIP September 2025 review retained the universal "
        "birth-dose recommendation. Mainstream epidemiology shows no "
        "population-average autism association."
    ),
    "HYP-0067": (  # Aluminum adjuvant cumulative
        "FDA, WHO, EMA, and major immunology bodies conclude that aluminum "
        "adjuvants in pediatric vaccines remain below toxicokinetic harm "
        "thresholds, supported by Mitkus 2011 Vaccine (PMID 22001122). "
        "Andersson 2025 Ann Intern Med Danish nationwide cohort (PMID "
        "40658954) found no association between cumulative aluminum-adsorbed-"
        "vaccine exposure and chronic-disease outcomes including autism, "
        "asthma, and autoimmune disease at population level."
    ),
    "HYP-0068": (  # MMR specifically
        "WHO, CDC, AAP, EMA, NHS recommend MMR vaccine on the standard "
        "schedule. Multiple large cohort studies — Madsen 2002 NEJM 537,000+ "
        "children (PMID 12421889); Hviid 2019 Ann Intern Med 657,000+ children "
        "(PMID 30831578); DeStefano 2019 Annu Rev Virol review (PMID 30986133); "
        "Honda 2005 Yokohama natural experiment (PMID 15877763) — find no "
        "association between MMR and autism. Wakefield 1998 paper was retracted "
        "by The Lancet in 2010 (PMID 20137807 retraction notice)."
    ),
    "HYP-0069": (  # Thimerosal
        "WHO continues to endorse thimerosal-containing multi-dose vaccines "
        "globally as safe and necessary for cold-chain logistics. Thimerosal "
        "was removed from US childhood vaccines (excluding some influenza "
        "formulations) by 2001 per a precautionary FDA / AAP joint statement. "
        "Subsequent large cohort studies — Verstraeten 2003 Pediatrics (PMID "
        "14595043), Madsen 2003, Heron 2004 — found no association between "
        "thimerosal exposure and autism at population level."
    ),
}

INTERVENTION_CONSENSUS = {
    "INT-0129": (  # Lovastatin (low-dose) — investigational use in autism
        "Statins (HMG-CoA reductase inhibitors including lovastatin) are FDA-"
        "approved and well-established for cardiovascular indications "
        "(hyperlipidemia, atherosclerotic disease). Their use in autism "
        "specifically — investigated by Frye et al for FXR / Ras-pathway "
        "modulation in subset cohorts — is investigational with limited "
        "published clinical evidence and is not a mainstream pediatric-"
        "neurology recommendation. Off-label use should be discussed with "
        "clinician oversight; CSRS in this atlas reflects mechanistic "
        "rationale + small published series, not population-validated efficacy."
    ),
}


def patch_table(filename: str, consensus_map: dict, status_field: str = "status",
                id_field: str = "id", insert_after: str | None = None) -> tuple[bool, int]:
    path = ATLAS_DIR / filename
    if not path.exists():
        return False, 0
    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)
        rows = list(reader)

    schema_changed = False
    if NEW_COLUMN not in fieldnames:
        if insert_after and insert_after in fieldnames:
            idx = fieldnames.index(insert_after) + 1
        else:
            idx = len(fieldnames)
        fieldnames.insert(idx, NEW_COLUMN)
        for r in rows:
            r.setdefault(NEW_COLUMN, "")
        schema_changed = True
        print(f"  {filename}: added column `{NEW_COLUMN}`")

    populated = 0
    for r in rows:
        rid = r.get(id_field)
        status = (r.get(status_field) or "").strip().lower()
        existing = (r.get(NEW_COLUMN) or "").strip()
        if status == "contested" and rid in consensus_map and not existing:
            r[NEW_COLUMN] = consensus_map[rid]
            populated += 1
            print(f"    populated {rid}: {consensus_map[rid][:80]}…")

    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return schema_changed, populated


def main():
    print("Phase C — mainstream consensus propagation\n")
    sc1, p1 = patch_table("hypotheses.csv", HYPOTHESIS_CONSENSUS, insert_after="status")
    sc2, p2 = patch_table("interventions.csv", INTERVENTION_CONSENSUS, insert_after="status")
    print(f"\nhypotheses.csv: schema_changed={sc1}, populated={p1}")
    print(f"interventions.csv: schema_changed={sc2}, populated={p2}")


if __name__ == "__main__":
    main()
