#!/usr/bin/env python3
"""Add Verstraeten 'Generation Zero' (1999 CDC VSD preliminary) to the atlas
as a contested-positive source for HYP-0066. Plus add the modern public
fact-check / Annenberg rebuttal as a contested-null counter-source.

The atlas spec §0/§1.1/§9.1: contested hypotheses keep contested status,
all evidence sides are recorded, scoring engine weighs by study size + design.
Generation Zero is preliminary/non-peer-reviewed → low extraction_confidence
and the design is 'preliminary_analysis' (lower weight than RCT/cohort).
"""

import csv, datetime as dt, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC_DIR = ROOT / "v2.0_scored"
EXP_DIR = ROOT / "v2.0.1_expanded"
NOW = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")

# --- New sources ----------------------------------------------------------
new_sources = [
    {
        "id": "SRC-001415",
        "type": "internal_doc",
        "platform": "cdc_foia",
        "external_id": "generation_zero_1999",
        "title": "Generation Zero — Thomas Verstraeten's first analyses of "
                 "vaccine mercury exposure and neurodevelopmental disorders "
                 "(VSD preliminary, Nov-Dec 1999)",
        "url": "https://childrenshealthdefense.org/government/foia/"
               "generation-zero-thomas-verstraetens-first-analyses-link-"
               "vaccine-mercury-exposure-risk-diagnosis-selected-neuro-"
               "developmental-disorders/",
        "date_published": "1999-12-01",
        "date_ingested": NOW,
        "study_design": "preliminary_analysis",
        "sample_size": "",
        "model_system": "",
        "raw_metadata": json.dumps({
            "doi": "",
            "year": 1999,
            "format": "internal_email_and_powerpoint",
            "peer_reviewed": False,
            "released_via": "FOIA",
            "subsequent_publication": "Verstraeten 2003 Pediatrics PMID 14595043 (null)",
            "key_finding": "Highest mercury-exposure cohort showed 11.35x "
                           "relative risk for autism vs. lowest-exposure; "
                           "preliminary, did not survive Phase 2 reanalysis",
            "controversy": "RFK Jr. and Children's Health Defense cite the "
                           "11.35x figure (often quoted as +1,135% or "
                           "rounded rhetorically to '10,000%') as evidence "
                           "of a buried CDC autism signal; mainstream "
                           "epidemiology counters that the preliminary "
                           "signal disappeared with proper denominators "
                           "and cohort matching in the published Verstraeten "
                           "2003 analysis."
        }),
        "notes": "Preliminary, non-peer-reviewed. Recorded for completeness "
                 "of the contested evidence landscape per spec §0 / §1.1 / §9.1.",
    },
    {
        "id": "SRC-001416",
        "type": "factcheck",
        "platform": "annenberg_factcheck",
        "external_id": "factcheck_rfk_2023_autism",
        "title": "FactCheck.org / Annenberg Public Policy Center — "
                 "'What RFK Jr. Gets Wrong About Autism' (rebuttal of the "
                 "Generation Zero / 1,135% / hep-B-causes-autism narrative)",
        "url": "https://www.factcheck.org/2023/08/scicheck-what-rfk-jr-gets-"
               "wrong-about-autism/",
        "date_published": "2023-08-01",
        "date_ingested": NOW,
        "study_design": "factcheck_review",
        "sample_size": "",
        "model_system": "",
        "raw_metadata": json.dumps({
            "year": 2023,
            "format": "fact_check_article",
            "peer_reviewed": False,
            "summarizes": "Verstraeten 2003 + IOM 2011 + DeStefano 2013 + "
                          "Andersson 2025; rebuts the Generation Zero 11.35x "
                          "framing as preliminary signal that didn't survive "
                          "proper analysis.",
        }),
        "notes": "Mainstream-consensus rebuttal source; balances the "
                 "Generation Zero positive evidence with the published-"
                 "literature null.",
    },
    {
        "id": "SRC-001417",
        "type": "factcheck",
        "platform": "annenberg_factcheck",
        "external_id": "annenberg_kennedy_flawed_paper",
        "title": "Annenberg Public Policy Center — 'Kennedy Cites Flawed "
                 "Paper in Bid to Justify Vaccine-Autism Link' (analysis of "
                 "Hooker/Geier/Mawson methodological problems and CDC's "
                 "non-suppression of vaccine safety data)",
        "url": "https://www.annenbergpublicpolicycenter.org/factcheck-org-"
               "kennedy-cites-flawed-paper-in-bid-to-justify-vaccine-autism-"
               "link/",
        "date_published": "2025-09-01",
        "date_ingested": NOW,
        "study_design": "factcheck_review",
        "sample_size": "",
        "model_system": "",
        "raw_metadata": json.dumps({
            "year": 2025,
            "format": "fact_check_article",
            "peer_reviewed": False,
        }),
        "notes": "Recent (2025) Annenberg/FactCheck rebuttal of the broader "
                 "vaccine-autism narrative as advanced by HHS Secretary "
                 "Kennedy.",
    },
]

# --- New evidence fragments ----------------------------------------------
new_fragments = [
    {
        "id": "EVD-001415",
        "source_id": "SRC-001415",
        "fragment_type": "result",
        "text_excerpt": (
            "Generation Zero preliminary analysis (Nov-Dec 1999, Verstraeten "
            "et al., CDC Vaccine Safety Datalink): the highest mercury-"
            "exposure cohort (>62.5 μg cumulative ethylmercury by 3 months) "
            "showed an estimated 11.35x relative risk for autism diagnosis "
            "vs. the lowest-exposure cohort. This finding is the source of "
            "the public '1,135% increase' / '~10,000% increase' framing. "
            "Phase 2 reanalysis with corrected denominators, broader "
            "diagnosis windows, and cohort matching reduced the signal to "
            "non-significance; the published 2003 Pediatrics paper "
            "(PMID 14595043) reports null. Preliminary, non-peer-reviewed."
        ),
        "structured_payload": json.dumps({
            "outcome": "Autism diagnosis (ICD-9 299.0)",
            "effect_size": "RR = 11.35 (highest vs. lowest mercury exposure)",
            "p_value": "preliminary; not formally tested in published form",
            "replicated": "no — superseded by Verstraeten 2003 Pediatrics null",
            "preliminary": True,
            "is_secondary_literature": False,
        }),
        "effect_direction": "positive",
        "strength_score": 0.20,  # low — preliminary, single internal analysis
        "extraction_method": "manual",
        "extraction_confidence": 0.7,
        "date_extracted": NOW,
        "notes": "Preliminary CDC internal analysis released via FOIA. "
                 "Recorded per spec §0 / §1.1 to preserve contested evidence "
                 "landscape. Strength_score deliberately low to reflect "
                 "non-peer-reviewed, single-analysis, superseded-by-published.",
    },
    {
        "id": "EVD-001416",
        "source_id": "SRC-001416",
        "fragment_type": "result",
        "text_excerpt": (
            "FactCheck.org / Annenberg 2023: Compiles peer-reviewed evidence "
            "(Verstraeten 2003, IOM 2011, DeStefano 2013, Hviid 2003, "
            "Andersson 2025) showing no causal association between hepatitis "
            "B vaccination, thimerosal exposure, or aluminum adjuvants and "
            "autism. Notes that the Generation Zero 11.35x preliminary "
            "signal disappeared after correct denominators and cohort "
            "matching were applied in Verstraeten Phase 2."
        ),
        "structured_payload": json.dumps({
            "summarizes_studies": "Verstraeten 2003; IOM 2011; DeStefano 2013; "
                                  "Hviid 2003; Andersson 2025",
            "is_secondary_literature": True,
        }),
        "effect_direction": "negative",
        "strength_score": 0.45,
        "extraction_method": "manual",
        "extraction_confidence": 0.85,
        "date_extracted": NOW,
        "notes": "Secondary literature synthesis. Counter-balances Generation "
                 "Zero in the contested evidence pool.",
    },
    {
        "id": "EVD-001417",
        "source_id": "SRC-001417",
        "fragment_type": "result",
        "text_excerpt": (
            "Annenberg 2025: Reviews HHS Secretary Kennedy's claims that "
            "Hooker/Geier/Mawson papers and 'buried CDC studies' (Generation "
            "Zero) prove a vaccine-autism link, concludes the cited papers "
            "have severe methodological problems (selection bias, "
            "uncontrolled confounding, statistical errors) and the "
            "Generation Zero preliminary signal was not suppressed but "
            "rather superseded by the published Verstraeten 2003 null."
        ),
        "structured_payload": json.dumps({
            "year": 2025,
            "is_secondary_literature": True,
        }),
        "effect_direction": "negative",
        "strength_score": 0.45,
        "extraction_method": "manual",
        "extraction_confidence": 0.85,
        "date_extracted": NOW,
        "notes": "2025 Annenberg fact-check directly addressing the Generation "
                 "Zero / Kennedy narrative.",
    },
]

# --- New evidence links ---------------------------------------------------
new_links = [
    {
        "id": "EVL-001634",
        "evidence_fragment_id": "EVD-001415",
        "claim_id": "",
        "target_type": "hypothesis",
        "target_id": "HYP-0066",
        "effect_direction": "positive",
        "weight": "",
        "context_scope": "",
        "created_at": NOW,
        "notes": "Generation Zero preliminary 11.35x positive signal",
    },
    {
        "id": "EVL-001635",
        "evidence_fragment_id": "EVD-001416",
        "claim_id": "",
        "target_type": "hypothesis",
        "target_id": "HYP-0066",
        "effect_direction": "negative",
        "weight": "",
        "context_scope": "",
        "created_at": NOW,
        "notes": "FactCheck/Annenberg synthesis null",
    },
    {
        "id": "EVL-001636",
        "evidence_fragment_id": "EVD-001417",
        "claim_id": "",
        "target_type": "hypothesis",
        "target_id": "HYP-0066",
        "effect_direction": "negative",
        "weight": "",
        "context_scope": "",
        "created_at": NOW,
        "notes": "Annenberg 2025 rebuttal of Kennedy / Generation Zero claim",
    },
    # Also link Generation Zero to HYP-0044 (Childhood vaccine exposure -
    # contested), HYP-0067 (Aluminum adjuvant), HYP-0069 (Thimerosal), since
    # the same evidence cluster informs all of those.
    {
        "id": "EVL-001637",
        "evidence_fragment_id": "EVD-001415",
        "claim_id": "",
        "target_type": "hypothesis",
        "target_id": "HYP-0069",
        "effect_direction": "positive",
        "weight": "",
        "context_scope": "",
        "created_at": NOW,
        "notes": "Generation Zero is fundamentally a thimerosal-exposure analysis",
    },
    {
        "id": "EVL-001638",
        "evidence_fragment_id": "EVD-001416",
        "claim_id": "",
        "target_type": "hypothesis",
        "target_id": "HYP-0069",
        "effect_direction": "negative",
        "weight": "",
        "context_scope": "",
        "created_at": NOW,
        "notes": "Same FactCheck synthesis applies to thimerosal hypothesis",
    },
]

# --- Apply to both v2.0_scored and v2.0.1_expanded ------------------------
def append_to(path, fields, new_rows):
    rows = list(csv.DictReader(open(path)))
    existing_ids = {r["id"] for r in rows}
    added = 0
    for r in new_rows:
        if r["id"] in existing_ids:
            continue
        # Ensure row matches schema
        out = {f: r.get(f, "") for f in fields}
        rows.append(out)
        added += 1
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(f"  {path.name}: +{added} rows ({len(rows)} total)")

src_fields = list(csv.DictReader(open(SRC_DIR / "sources.csv")).fieldnames)
frag_fields = list(csv.DictReader(open(SRC_DIR / "evidence_fragments.csv")).fieldnames)
link_fields = list(csv.DictReader(open(SRC_DIR / "evidence_links.csv")).fieldnames)

print("Adding Generation Zero + FactCheck/Annenberg sources...")
for d in [SRC_DIR, EXP_DIR]:
    print(f"\n{d.name}:")
    append_to(d / "sources.csv",            src_fields, new_sources)
    append_to(d / "evidence_fragments.csv", frag_fields, new_fragments)
    append_to(d / "evidence_links.csv",     link_fields, new_links)

# Update HYP-0066 description to mention Generation Zero
print("\nUpdating HYP-0066 description and notes...")
for d in [SRC_DIR, EXP_DIR]:
    hp = d / "hypotheses.csv"
    rows = list(csv.DictReader(open(hp)))
    fields = list(csv.DictReader(open(hp)).fieldnames)
    for r in rows:
        if r["id"] != "HYP-0066":
            continue
        new_desc = (
            "Day-of-birth hepatitis B vaccination has been hypothesized as a "
            "specific autism risk factor distinct from the broader childhood "
            "vaccine schedule, on the basis of (a) the neonatal developmental "
            "window, (b) aluminum adjuvant content (~250 mcg per dose), and "
            "(c) the small marginal risk-benefit ratio in non-endemic "
            "populations where maternal HBsAg is negative. Positive evidence: "
            "Verstraeten 'Generation Zero' 1999 CDC VSD preliminary analysis "
            "(11.35x relative risk for highest-mercury-exposure cohort, "
            "preliminary and superseded; SRC-001415); Gallagher & Goodman "
            "2010 NHIS analysis (3x odds ratio in male neonates). Null "
            "evidence: published Verstraeten 2003 Pediatrics; IOM 2011; "
            "Andersson 2025 Danish nationwide cohort (n=1.2M); Annenberg/"
            "FactCheck 2023 + 2025 syntheses. Public framing: HHS Secretary "
            "RFK Jr. cites the 11.35x Generation Zero figure (commonly "
            "quoted as +1,135% or rounded rhetorically to '10,000%') as "
            "buried CDC evidence; mainstream consensus is that the "
            "preliminary signal didn't survive proper analysis. Per spec "
            "§1.1 and §9.1, status=contested permanent; engine scores from "
            "the evidence mix — currently tilted toward the null per study "
            "size and design but with the Generation Zero preliminary "
            "preserved in the contested-positive pool."
        )
        r["description"] = new_desc
        r["notes"] = ("Status=contested permanent; positive=Generation Zero "
                      "1999 preliminary (SRC-001415) + Gallagher 2010; "
                      "null=Verstraeten 2003 + IOM 2011 + Andersson 2025; "
                      "RFK Jr / Children's Health Defense public framing "
                      "captured via Annenberg/FactCheck rebuttals "
                      "(SRC-001416, SRC-001417). ACIP Sep 2025 review of "
                      "universal birth-dose recommendation noted.")
        r["last_updated"] = NOW
    with open(hp, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(f"  {hp.name}: updated HYP-0066")

print("\nDone.")
