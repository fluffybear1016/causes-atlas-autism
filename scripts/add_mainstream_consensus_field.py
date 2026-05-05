#!/usr/bin/env python3
"""
add_mainstream_consensus_field.py

Move 6b — adds a `mainstream_consensus_position` column to
iatrogenic_exposure_priors.csv and populates it for every contested row.

The single feature that immunizes the project against bad-faith framing:
every contested entity renders the mainstream-consensus position at equal
prominence with the contested-evidence position. Anyone reading any contested
page sees the mainstream view in equal type — the page itself disproves any
"this project is anti-vax" framing.

Idempotent: re-runnable. If the column exists, only updates empty cells
where contested rows need population.

Per CLAUDE.md epistemic principle 1 ("mainstream consensus is one input,
not authoritative") + post-mortem Move 6b.
"""
from __future__ import annotations
import csv
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CSV_PATH = REPO / "v2.0_scored" / "iatrogenic_exposure_priors.csv"

NEW_COLUMN = "mainstream_consensus_position"
INSERT_AFTER = "countervailing_evidence_pmids"

# Hand-curated mainstream consensus positions for each contested row.
# Tone: neutral, factual statement of the mainstream regulatory / society
# position. NOT advocacy. The contested-evidence position remains in the
# log_odds_shift, primary_pmids, and notes fields — both views coexist.
CONSENSUS = {
    "IEP-00001": (
        "ACOG and APA consider SSRIs broadly compatible with pregnancy when "
        "clinically indicated; risk of untreated maternal depression is "
        "weighted against signal. A small absolute increase in heterogeneous "
        "outcomes (cardiac, ASD, ADHD) has been reported in some cohorts but "
        "is generally judged confounded by indication."
    ),
    "IEP-00005": (
        "WHO, FDA, ACOG consider acetaminophen the preferred analgesic in "
        "pregnancy when clinically indicated. The 2021 multi-author consensus "
        "statement (PMID 34507921) calling for precautionary minimization is "
        "an emerging signal, not a guideline change."
    ),
    "IEP-00015": (
        "FDA SmartTots, ASA, and the GAS trial (Davidson 2016 Lancet PMID "
        "26507180; McCann 2019 PMID 30782342) support that brief single-"
        "exposure general anesthesia in young children does not cause "
        "measurable neurodevelopmental harm at population level. Caution is "
        "advised for prolonged or repeated exposures."
    ),
    "IEP-00019": (
        "WHO, ADA, AAP, CDC endorse community water fluoridation at the US "
        "optimal level (~0.7 mg/L) with substantial caries-prevention evidence. "
        "The Bashash/Green findings reflect prenatal fluoride at >2.5 mg/L — "
        "above optimal fluoridation. The 2024 NTP monograph (PMID 39172715) "
        "reports a low-confidence association between fluoride exposure above "
        "1.5 mg/L and lower IQ; below 1.5 mg/L the evidence is insufficient."
    ),
    "IEP-00022": (
        "Thimerosal was removed from US childhood vaccines (excluding some flu) "
        "by 2001 per a precautionary FDA/AAP position; subsequent large cohort "
        "studies (Verstraeten 2003 PMID 14595043; Madsen 2003) found no "
        "association between thimerosal exposure and autism. WHO continues to "
        "endorse thimerosal-containing multidose vaccines globally as safe."
    ),
    "IEP-00023": (
        "WHO, AAP, ACIP recommend universal hepatitis B birth-dose vaccination. "
        "Vertical-transmission mortality reduction is well established and "
        "outside dispute. ACIP September 2025 review retained the universal "
        "birth-dose recommendation. Mainstream epidemiology shows no "
        "population-average autism association."
    ),
    "IEP-00025": (
        "ACOG and APA consider SNRIs (venlafaxine, duloxetine) compatible with "
        "pregnancy when clinically indicated, with the same indication-confounded "
        "risk-benefit framing as SSRIs."
    ),
    "IEP-00026": (
        "FDA, WHO, EMA conclude aluminum adjuvants in pediatric vaccines remain "
        "below toxicokinetic harm thresholds (Mitkus 2011 PMID 22001122). "
        "Andersson 2025 Ann Intern Med Danish nationwide cohort (PMID 40658954) "
        "found no association between cumulative aluminum-adsorbed-vaccine "
        "exposure and chronic-disease outcomes."
    ),
    "IEP-00027": (
        "Same as IEP-00026 (this row encodes a subgroup-conditional alternative "
        "framing). Mainstream consensus per FDA/WHO/EMA: aluminum adjuvants in "
        "pediatric vaccines are safe at scheduled doses; the population-average "
        "association with chronic disease in nationwide cohort data is null "
        "(Andersson 2025 PMID 40658954)."
    ),
}


def main():
    if not CSV_PATH.exists():
        print(f"ERROR: {CSV_PATH} not found", file=sys.stderr)
        sys.exit(2)

    with open(CSV_PATH, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)
        rows = list(reader)

    # Add column if missing
    schema_changed = False
    if NEW_COLUMN not in fieldnames:
        try:
            insert_idx = fieldnames.index(INSERT_AFTER) + 1
        except ValueError:
            insert_idx = len(fieldnames)
        fieldnames.insert(insert_idx, NEW_COLUMN)
        for r in rows:
            r.setdefault(NEW_COLUMN, "")
        schema_changed = True
        print(f"Added column `{NEW_COLUMN}` after `{INSERT_AFTER}`")

    # Populate for contested rows
    populated = 0
    for r in rows:
        rid = r.get("id")
        status = (r.get("status") or "").strip().lower()
        existing = (r.get(NEW_COLUMN) or "").strip()
        if status == "contested" and rid in CONSENSUS and not existing:
            r[NEW_COLUMN] = CONSENSUS[rid]
            populated += 1
            print(f"  populated {rid}: {CONSENSUS[rid][:80]}…")

    if not schema_changed and populated == 0:
        print("No changes needed (already populated).")
        return

    with open(CSV_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nWrote {populated} mainstream_consensus_position cells (schema_changed={schema_changed})")


if __name__ == "__main__":
    main()
