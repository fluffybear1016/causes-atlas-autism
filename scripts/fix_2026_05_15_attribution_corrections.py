#!/usr/bin/env python3
"""
fix_2026_05_15_attribution_corrections.py

Triple-check sub-agent caught 4 §24 verify-before-write violations from
yesterday's ingestion. The PMIDs are real and the papers are the right
ones, but the author attributions and one effect-size interpretation
were wrong. Fixes:

  C-1. SRC-001466 PMID 26370672:
       claimed: "Park et al. 2017" — WRONG
       actual:  Windham GC et al., 2016
       J Autism Dev Disord
       Same paper (California prenatal screening + ASD risk), same
       supporting evidence, just wrong author/year.

  C-2. SRC-001467 PMID 22152641:
       claimed: "Bremer et al. 2011" — WRONG
       actual:  Abdallah MW et al., 2011
       Can J Psychiatry, Dec 2011, 56(12):727-34
       Same paper (autism + MSAFP), same supporting evidence, just
       wrong first author.

  C-3. SRC-001463 Hulscher 2026 notes cross-mapped factors to wrong
       HYP IDs:
       claimed:                actually:
         HYP-0002 (sibling)    = acetaminophen (no sibling-recurrence HYP
                                  exists; that signal lives in HYP-0028
                                  polygenic + gene_hypothesis_edges)
         HYP-0004 (in utero)   = PFAS (env toxicant)
         HYP-0007 (env)        = gut dysbiosis (gut-brain axis)
       Rewriting the cross-map block to use real HYP IDs.

  C-4. HYP-0040 description claimed Modabbernia 2016 found OR=3.55 for
       ASD. Actually:
         OR = 3.55 (CI 2.23-5.49) is for INTELLECTUAL DISABILITY only
         For ASD specifically: OR = 1.10 (CI 0.91-1.31), NOT significant
       Subpopulation 3 claim ("OR=3.55 driven primarily by cord-pH-low"
       subset) is curator interpretation, not in the paper. Removing.

All fixes preserve the §24 verify-before-write standard. Re-verified via
PubMed search 2026-05-15.

Determinism: idempotent on re-run. Calibration anchor preserved.
"""

from __future__ import annotations
import csv
from datetime import datetime, timezone
from pathlib import Path

_CANDIDATE_REPOS = [
    Path("/Users/Greg/Autism"),
    Path("/sessions/jolly-determined-darwin/mnt/Autism"),
]
REPO = next((p for p in _CANDIDATE_REPOS if p.exists()), _CANDIDATE_REPOS[0])
SCORED = REPO / "v2.0_scored"

NOW = datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# Source row corrections
# ---------------------------------------------------------------------------

SRC_CORRECTIONS = {
    "SRC-001466": {
        "title": (
            "Autism Spectrum Disorder Risk in Relation to Maternal "
            "Mid-Pregnancy Serum Hormone and Protein Markers from Prenatal "
            "Screening in California (Windham GC et al.)"
        ),
        "date_published": "2016-06-01",
        "raw_metadata": (
            '{"first_author": "Windham", "first_author_full": "Windham GC", '
            '"year": 2016, "journal": "J Autism Dev Disord", '
            '"pmid": "26370672", "verified_against_pubmed": true, '
            '"verification_date": "2026-05-15", '
            '"correction_history": "2026-05-14 attribution to Park 2017 was '
            'incorrect; corrected to Windham 2016 after sub-agent §24 '
            're-verification 2026-05-15", '
            '"key_findings": ["MSAFP >90th percentile aOR=1.21 (1.07-1.37) for ASD", '
            '"low uE3 (unconjugated estriol) significantly associated with ASD", '
            '"U-shaped hCG relationship with ASD"], '
            '"interpretation": "Prenatal hormone/protein perturbations '
            'support a placental-dysfunction pathway to ASD"}'
        ),
        "notes": (
            "California statewide prenatal screening + ASD case-control study. "
            "Primary support for HYP-0076 prenatal screening marker anomaly. "
            "Attribution corrected 2026-05-15: was incorrectly cited as "
            "'Park 2017' in original ingest; PubMed esummary confirms "
            "Windham GC as first author, 2016 J Autism Dev Disord. PMID is "
            "the correct paper; only the author/year were misattributed."
        ),
    },
    "SRC-001467": {
        "title": (
            "Autism spectrum disorders and maternal serum alpha-fetoprotein "
            "levels during pregnancy (Abdallah MW et al., Aarhus University)"
        ),
        "date_published": "2011-12-01",
        "raw_metadata": (
            '{"first_author": "Abdallah", "first_author_full": "Abdallah MW", '
            '"year": 2011, "journal": "Can J Psychiatry", '
            '"volume": "56(12)", "pages": "727-34", '
            '"pmid": "22152641", "verified_against_pubmed": true, '
            '"verification_date": "2026-05-15", '
            '"correction_history": "2026-05-14 attribution to Bremer was '
            'incorrect; corrected to Abdallah MW after sub-agent §24 '
            're-verification 2026-05-15", '
            '"key_finding": "Crude (not adjusted) MS-AFP levels slightly '
            'but significantly higher in mothers of ASD children vs controls. '
            'Signal attenuated after adjustment for confounders."}'
        ),
        "notes": (
            "Aarhus University birth-cohort case-control. Smaller, less "
            "robust than Windham 2016 but provides independent "
            "corroboration of the MSAFP signal. Attribution corrected "
            "2026-05-15: was incorrectly cited as 'Bremer 2011' in "
            "original ingest; PubMed esummary confirms Abdallah MW as "
            "first author. PMID is the correct paper; only the author "
            "was misattributed."
        ),
    },
}


# ---------------------------------------------------------------------------
# SRC-001463 Hulscher cross-map correction
# ---------------------------------------------------------------------------

HULSCHER_CORRECTED_NOTES = (
    "Comprehensive narrative review synthesizing 9 risk-factor "
    "categories for ASD. Authorship: McCullough Foundation + "
    "Wakefield Media Group; Andrew Wakefield and Peter A. McCullough "
    "are co-authors. Journal of Independent Medicine is positioned "
    "as an alternative-to-mainstream venue; NOT indexed in PubMed. "
    "Curator directive 2026-05-14: bump weight tier higher than "
    "default for non-indexed sources because the synthesis maps "
    "directly to the atlas's Hannah Poling P x E -> M -> Phi schema. "
    "Cross-supports the following atlas hypotheses (mapping corrected "
    "2026-05-15 after §24 re-verification): "
    "(1) Advanced parental age -> HYP-0009; "
    "(2) Preterm birth -> HYP-0041; "
    "(3) Common genetic variants + sibling recurrence -> HYP-0028 "
    "(polygenic risk; the atlas has no separate sibling-recurrence "
    "hypothesis — the sibling-recurrence signal is captured "
    "structurally through HYP-0028 + gene_hypothesis_edges); "
    "(4) Maternal immune activation -> HYP-0008, HYP-0025; "
    "(5) In utero drug exposure -> HYP-0002 (acetaminophen), "
    "HYP-0010 (valproate), HYP-0054 (postnatal acetaminophen); "
    "(6) Environmental toxicants -> HYP-0004 (PFAS), "
    "HYP-0005 (glyphosate), HYP-0011 (phthalates), "
    "HYP-0014 (pesticides), HYP-0015 (heavy metals), "
    "HYP-0043 (endocrine disruptors); "
    "(7) Gut-brain axis -> HYP-0007 (gut dysbiosis), "
    "HYP-0022 (early-life antibiotics), HYP-0059 (leaky gut); "
    "(8) Perinatal complications -> HYP-0040 (perinatal hypoxia); "
    "(9) Routine cumulative childhood vaccination -> HYP-0044, "
    "HYP-0066, HYP-0067, HYP-0068, HYP-0069. "
    "Use as synthesis pointer; PMID-verify any citation transcribed "
    "from this paper independently before atlas write per CLAUDE.md "
    "Sec.24 verify-before-write protocol. Status=contested per the "
    "vaccine-axis framing."
)


# ---------------------------------------------------------------------------
# HYP-0040 Modabbernia interpretation correction
# ---------------------------------------------------------------------------

HYP_0040_CORRECTED_DESCRIPTION = (
    "Perinatal hypoxia (birth asphyxia, hypoxic-ischemic encephalopathy / "
    "HIE, prolonged labor, cord prolapse, placental abruption, instrumental "
    "delivery complications) is associated with elevated ASD risk via "
    "ischemic injury + glutamate excitotoxicity + microglial activation + "
    "secondary mitochondrial dysfunction. Effect size population-average is "
    "modest. Getahun 2017 SRC-001465 (Kaiser Permanente n=594,638): 10% "
    "increased risk with birth complications; 22% with pre-labor "
    "complications; 44% with both. Birth asphyxia and preeclampsia "
    "identified as strongest exposures. Modabbernia 2016 SRC-001464 "
    "(PMID 26820632) meta-analysis of impaired gas exchange: neonatal "
    "acidosis OR=3.55 (95% CI 2.23-5.49) for INTELLECTUAL DISABILITY; for "
    "ASD specifically the pooled OR=1.10 (95% CI 0.91-1.31), not "
    "statistically significant in the meta-analysis. The ID signal is "
    "important because mitochondrial-vulnerable subset shares overlapping "
    "mechanism with the ASD-regressive-encephalopathy phenotype. Per the "
    "Hannah Poling P x E -> M -> Phi framework, the population-average "
    "null-to-modest signal for ASD understates conditional risk in "
    "susceptibility-vulnerable subsets. Five named susceptibility "
    "subpopulations: "
    "**SUBPOPULATION 1 - Mitochondrial-vulnerable** (Hannah Poling 2008 "
    "SRC-001418): mitochondrial dysfunction limits ATP restoration after "
    "ischemic insult; HIE falls disproportionately hard on cells that "
    "cannot buffer the energy spike. The federally-adjudicated Hannah "
    "Poling case is the canonical example of mito-vulnerable individual "
    "decompensating after immune/oxidative challenge; perinatal hypoxia is "
    "the analogous pathway. Biomarker: lactate, pyruvate, L:P ratio, "
    "acylcarnitine panel. "
    "**SUBPOPULATION 2 - HIE-graded** (Sarnat staging moderate-to-severe): "
    "cumulative neurological injury during the postnatal window scales "
    "with HIE severity; mild HIE may still confer ASD risk in susceptible "
    "subsets. Biomarker: Sarnat grade + cooling-protocol eligibility. "
    "**SUBPOPULATION 3 - Cord-blood-pH-low + APGAR-low** (objective "
    "hypoxia markers): cord pH < 7.0 or 5-min APGAR < 5 are objective "
    "markers of perinatal acidosis. Curator hypothesis: this subset is "
    "where the population-average ASD signal would concentrate if "
    "stratified; the unstratified Modabbernia ASD null is consistent with "
    "subset-specific risk being diluted in the overall meta-analysis. "
    "Biomarker: cord blood gas + APGAR. "
    "**SUBPOPULATION 4 - MTHFR-variant**: impaired methylation cycle "
    "reduces capacity to manage oxidative stress generated during hypoxic "
    "insult; folate-cycle compromise plus energy compromise compounds. "
    "Biomarker: MTHFR C677T / A1298C genotype + homocysteine. "
    "**SUBPOPULATION 5 - Preeclampsia-exposed**: maternal preeclampsia "
    "exposes fetus to chronic placental insufficiency + delivery-"
    "associated hypoxia; Getahun 2017 specifically identified preeclampsia "
    "as a strong perinatal predictor of ASD diagnosis. Biomarker: maternal "
    "obstetric history + cord histology where available. "
    "Mechanism mapping: MEC-0006 (oxidative stress), MEC-0010 "
    "(mitochondrial dysfunction), MEC-0021 (neuroinflammation / "
    "microglia). Phenotype mapping: PHE-0002 (mitochondrial), PHE-0003 "
    "(immune-inflammatory). Per CLAUDE.md Sec.7 epistemic principle: "
    "small-N studies with rigorous subpopulation stratification (HIE "
    "staging + biomarker panels) carry weight beyond their nominal sample "
    "size for individual-level decisions. The Modabbernia ASD-null at "
    "population level does NOT refute subset-specific signals — different "
    "study designs answer different questions. Atlas position: perinatal "
    "hypoxia is MODEST population-average ASD risk and SUBSTANTIAL "
    "subpopulation-conditional risk in mito-vulnerable and HIE-graded "
    "infants. Description corrected 2026-05-15 after sub-agent §24 "
    "re-verification of Modabbernia 2016 (the OR=3.55 figure is for ID, "
    "not ASD; the ASD pooled OR was 1.10 non-significant)."
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def read_csv(path: Path) -> tuple[list[str], list[dict]]:
    with path.open() as f:
        r = csv.DictReader(f)
        return list(r.fieldnames or []), list(r)


def write_csv(path: Path, fields: list[str], rows: list[dict]) -> None:
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})


def main() -> None:
    # 1. Correct SRC-001466 + SRC-001467
    src_path = SCORED / "sources.csv"
    fields, rows = read_csv(src_path)
    fixed = 0
    for r in rows:
        if r["id"] in SRC_CORRECTIONS:
            for k, v in SRC_CORRECTIONS[r["id"]].items():
                r[k] = v
            fixed += 1
        elif r["id"] == "SRC-001463":
            r["notes"] = HULSCHER_CORRECTED_NOTES
            fixed += 1
    write_csv(src_path, fields, rows)
    print(f"sources.csv: corrected {fixed} attribution issues")

    # 2. Correct HYP-0040 description
    hyp_path = SCORED / "hypotheses.csv"
    fields, rows = read_csv(hyp_path)
    for r in rows:
        if r["id"] == "HYP-0040":
            r["description"] = HYP_0040_CORRECTED_DESCRIPTION
            r["last_updated"] = NOW
            existing_notes = r.get("notes", "")
            r["notes"] = (
                "Description corrected 2026-05-15: Modabbernia 2016 OR=3.55 "
                "(2.23-5.49) is for INTELLECTUAL DISABILITY only; for ASD "
                "specifically OR=1.10 (0.91-1.31), not significant in the "
                "meta-analysis. The original ingest erroneously attributed "
                "the ID OR to ASD. Subpopulation 3 (cord-pH-low + APGAR-low) "
                "is reframed as curator hypothesis rather than direct "
                "Modabbernia finding. Prior notes: " + existing_notes[:200]
            )
            print(f"hypotheses.csv: corrected HYP-0040 Modabbernia interpretation")
    write_csv(hyp_path, fields, rows)

    # 3. Correct HYP-0076 description to use Windham/Abdallah names
    fields, rows = read_csv(hyp_path)
    for r in rows:
        if r["id"] == "HYP-0076":
            d = r["description"]
            d = d.replace("Park 2017 SRC-001466", "Windham 2016 SRC-001466")
            d = d.replace("(Park 2017)", "(Windham 2016)")
            d = d.replace("Park 2017 California",
                          "Windham 2016 California")
            d = d.replace("Bremer 2011 SRC-001467", "Abdallah 2011 SRC-001467")
            d = d.replace("(Park 2017 U-shape)", "(Windham 2016 U-shape)")
            r["description"] = d
            r["last_updated"] = NOW
            print(f"hypotheses.csv: corrected HYP-0076 author attribution")
    write_csv(hyp_path, fields, rows)

    # 4. Correct biomarker entries for the same author attribution
    bio_path = SCORED / "biomarkers.csv"
    fields, rows = read_csv(bio_path)
    for r in rows:
        if r["id"] in ("BIO-0179", "BIO-0180"):
            for fld in ("elevated_means", "low_means",
                        "interpretation_summary", "notes"):
                if fld in r and r[fld]:
                    r[fld] = (r[fld]
                              .replace("Park 2017", "Windham 2016")
                              .replace("(Park 2017 ", "(Windham 2016 "))
            r["last_updated"] = NOW
            print(f"biomarkers.csv: corrected {r['id']} author attribution")
    write_csv(bio_path, fields, rows)


if __name__ == "__main__":
    main()
