#!/usr/bin/env python3
"""Ingest:
  1. Naviaux 2026 PMID 41902612 — '3-Hit Metabolic Signaling Model for ASD'
     (Autism Research, peer-reviewed, ~0.50 strength)
  2. McCullough Foundation Report 2025 — Zenodo DOI 10.5281/zenodo.17451259
     'Determinants of Autism Spectrum Disorder' (preprint, ~0.20 strength)

Per CLAUDE.md:
  - Naviaux 2026: peer-reviewed Autism Research → SRC type=study, study_design=review/theoretical
  - McCullough Foundation: Zenodo preprint, foundation/advocacy authorship including Wakefield
    → SRC type=advocacy/preprint, study_design=preprint, low strength_score
"""
import csv, datetime as dt, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NOW = dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')

# === New sources ===
new_sources = [
    {
        "id": "SRC-001448",
        "type": "study",
        "platform": "pubmed",
        "external_id": "41902612",
        "title": ("The 3-Hit Metabolic Signaling Model for Autism Spectrum "
                  "Disorder: A Summary (Naviaux 2026, Autism Research)"),
        "url": "https://pubmed.ncbi.nlm.nih.gov/41902612/",
        "date_published": "2026-03-28",
        "date_ingested": NOW,
        "study_design": "theoretical_review",
        "sample_size": "",
        "model_system": "human",
        "raw_metadata": json.dumps({
            "pmid": "41902612", "year": 2026, "doi": "10.1002/aur.70228",
            "journal": "Autism Research", "peer_reviewed": True,
        }),
        "notes": ("Peer-reviewed framework synthesis (Autism Research 2026). "
                  "3-Hit Metabolic Signaling Model: (1) inherited genetic/"
                  "epigenetic variants sensitizing mito + Ca + purinergic "
                  "signaling; (2) early prenatal/postnatal CDR activation by "
                  "infection/immune/toxicant; (3) prolonged or recurrent CDR "
                  "triggers 3-6 months between late 1st trimester and 18-36 "
                  "months of age. PKU cited as proof-of-principle. Major "
                  "framework update from Naviaux's earlier CDR theory."),
    },
    {
        "id": "SRC-001449",
        "type": "preprint",
        "platform": "zenodo",
        "external_id": "10.5281/zenodo.17451259",
        "title": ("McCullough Foundation Report: Determinants of Autism "
                  "Spectrum Disorder (Hulscher, Leake, Troupe, Rogers, "
                  "Cosgrove, Mead, Craven, Radetich, Wakefield, McCullough; "
                  "October 2025, Zenodo preprint)"),
        "url": "https://zenodo.org/records/17451259",
        "date_published": "2025-10-27",
        "date_ingested": NOW,
        "study_design": "preprint",
        "sample_size": "136",
        "model_system": "human",
        "raw_metadata": json.dumps({
            "doi": "10.5281/zenodo.17451259", "year": 2025,
            "platform": "Zenodo (open repository)",
            "peer_reviewed": False,
            "authors_total": 10,
            "authors_notable": "Andrew Wakefield (Lancet 1998 retraction; "
                              "license revoked); Peter McCullough (ABIM cert "
                              "revoked 2025); rest mostly McCullough Foundation staff",
            "study_count_reviewed": 136,
            "study_count_positive": 107,
            "study_count_neutral": 29,
            "key_findings": "12 vaxxed-vs-unvaccinated comparisons consistently "
                          "showed lower chronic disease + ASD in unvaccinated; "
                          "neutral studies critiqued for absent unvaccinated "
                          "controls + registry misclassification + averaged "
                          "estimates obscuring vulnerable-subgroup effects; "
                          "positive studies span epidemiologic, clinical, "
                          "mechanistic, neuropathologic, case-report evidence",
        }),
        "notes": ("Zenodo PREPRINT — NOT peer-reviewed. Per CLAUDE.md §1+§3: "
                  "primary document but foundation/advocacy authorship "
                  "(McCullough Foundation, Wakefield) requires down-weighting. "
                  "However, the report's METHODOLOGICAL FRAMING — that null "
                  "studies obscure vulnerable-subgroup effects through "
                  "averaging — is consistent with CLAUDE.md §9 (mixed "
                  "evidence = heterogeneity, not absence). Strength_score "
                  "0.20 reflects preprint-tier + author concerns balanced "
                  "against substantive 136-study review and methodological "
                  "synthesis aligned with atlas's own §9 principle."),
    },
]

# === New evidence fragments ===
new_fragments = [
    {
        "id": "EVD-001448",
        "source_id": "SRC-001448",
        "fragment_type": "result",
        "text_excerpt": (
            "Naviaux 2026 (Autism Research, PMID 41902612): proposes the "
            "3-Hit Metabolic Signaling Model for ASD, in which autism arises "
            "from sequential interaction of (1) inherited genetic/epigenetic "
            "variants sensitizing mitochondrial metabolism, intracellular "
            "calcium handling, and purinergic signaling to environmental "
            "change; (2) early prenatal or postnatal activation of the cell "
            "danger response (CDR) by infection, immune dysregulation, "
            "metabolic disturbance, or environmental toxicant exposure; and "
            "(3) prolonged or recurrent exposure to CDR-activating triggers "
            "for 3-6 months between the late 1st trimester and 18-36 months "
            "of age. The CDR is initiated by extracellular ATP (eATP)-"
            "associated purinergic signaling and mitochondrial changes that "
            "are resource- and energy-intensive. Persistent CDR activation "
            "during the critical neurodevelopmental window is proposed to "
            "sensitize developing cells to eATP-related signaling, leading "
            "to false alarms and chemical/immune/neurosensory under- and "
            "over-responsivity. PKU cited as proof-of-principle: untreated "
            "PKU historically caused intellectual disability and autistic "
            "features; universal newborn screening + early treatment "
            "interrupts the sequence and prevents/decreases these outcomes."
        ),
        "structured_payload": json.dumps({
            "framework": "3-hit_metabolic_signaling_model",
            "design": "peer_reviewed_theoretical_review",
            "hits": ["genetic/epigenetic mito+Ca+purinergic sensitization",
                     "early CDR activation by environmental triggers",
                     "prolonged/recurrent CDR for 3-6mo in 1st trimester to 18-36mo window"],
            "core_mechanism": "extracellular ATP purinergic signaling + mitochondrial CDR",
            "proof_of_principle": "PKU",
            "author": "Naviaux RK",
            "is_secondary_literature": False,
            "primary": True,
            "peer_reviewed": True,
        }),
        "effect_direction": "positive",
        "strength_score": "0.50",
        "extraction_method": "manual",
        "extraction_confidence": "0.95",
        "date_extracted": NOW,
        "notes": ("Major framework update by Naviaux. Connects CDR theory + "
                  "purinergic signaling + mito to ASD via 3-hit susceptibility "
                  "× early-trigger × prolonged-window structure. Aligns with "
                  "atlas's Hannah Poling framework (P × E → Φ)."),
    },
    {
        "id": "EVD-001449",
        "source_id": "SRC-001449",
        "fragment_type": "result",
        "text_excerpt": (
            "McCullough Foundation 2025 (Zenodo preprint, DOI 10.5281/"
            "zenodo.17451259): comprehensive review of 136 studies on "
            "childhood vaccines or vaccine excipients in relation to ASD. "
            "RESULTS: 107 of 136 studies (79%) inferred a possible link "
            "between immunization or vaccine components and ASD or other "
            "neurodevelopmental disorders, based on epidemiologic, clinical, "
            "mechanistic, neuropathologic, and case-report evidence of "
            "developmental regression. 29 of 136 (21%) found neutral risks "
            "or no association. 12 studies directly comparing routinely "
            "immunized vs completely unvaccinated children/young adults "
            "consistently demonstrated superior health outcomes (lower "
            "chronic medical problems and neuropsychiatric disorders "
            "including ASD) among the unvaccinated. METHODOLOGICAL CRITIQUE: "
            "neutral-association studies undermined by (a) absence of "
            "genuine unvaccinated control group — partial/unverified "
            "immunization even among those classified as 'unvaccinated', "
            "(b) registry misclassification, (c) ecological confounding, "
            "(d) averaged estimates obscuring effects within vulnerable "
            "subgroups. Authors include Andrew Wakefield (license revoked) "
            "and Peter McCullough (ABIM cert revoked 2025); pre-print not "
            "peer-reviewed. CLAUDE.md §3 down-weights for authorship + "
            "advocacy organization. Per CLAUDE.md §1, retained as primary "
            "document with explicitly low strength_score reflecting these "
            "concerns. Per CLAUDE.md §9, the report's core methodological "
            "argument (averaging obscures vulnerable-subgroup effects) is "
            "actually consistent with the atlas's own epistemic position."
        ),
        "structured_payload": json.dumps({
            "design": "preprint_review_synthesis",
            "studies_reviewed": 136,
            "positive_inferences": 107,
            "neutral_inferences": 29,
            "vaxxed_vs_unvaxxed_comparisons": 12,
            "methodological_critique_targets": [
                "absent genuine unvaccinated controls",
                "registry misclassification",
                "ecological confounding",
                "averaged estimates obscuring vulnerable subgroups",
            ],
            "preprint_status": "Zenodo, not peer-reviewed",
            "author_concerns": ["Andrew Wakefield (license revoked)",
                                "Peter McCullough (ABIM revoked 2025)"],
            "is_secondary_literature": True,
            "primary": False,
            "peer_reviewed": False,
            "is_advocacy_organization": True,
        }),
        "effect_direction": "positive",
        "strength_score": "0.20",
        "extraction_method": "manual",
        "extraction_confidence": "0.85",
        "date_extracted": NOW,
        "notes": ("Down-weighted per CLAUDE.md §3 (advocacy + Wakefield/"
                  "McCullough authorship). Retained per CLAUDE.md §1 (one "
                  "input, not authoritative). The methodological argument "
                  "about averaged-estimates-obscuring-subgroup-effects "
                  "aligns with atlas §9 and is the report's most "
                  "defensible contribution."),
    },
]

# === Evidence links ===
new_links = []
link_id = 1700
links_def = [
    # Naviaux 2026 → multiple mechanisms (3-hit framework spans many)
    ("EVD-001448", "mechanism", "MEC-0010", "positive",
     "Mitochondrial dysfunction is hit-1 substrate"),
    ("EVD-001448", "mechanism", "MEC-0014", "positive",
     "SIRTUIN/NAD+ purinergic signaling = CDR mechanism"),
    ("EVD-001448", "mechanism", "MEC-0020", "positive",
     "Calcium handling = hit-1 substrate"),
    ("EVD-001448", "hypothesis", "HYP-0006", "positive",
     "Hit-1 mitochondrial vulnerability"),
    ("EVD-001448", "hypothesis", "HYP-0008", "positive",
     "Hit-2 maternal immune activation = CDR trigger"),
    ("EVD-001448", "hypothesis", "HYP-0028", "positive",
     "Hit-1 inherited genetic substrate = polygenic risk"),
    ("EVD-001448", "hypothesis", "HYP-0073", "positive",
     "3-6mo CDR trigger window = developmental timing principle"),
    ("EVD-001448", "phenotype", "PHE-0002", "positive",
     "Mitochondrial dysfunction phenotype = direct CDR signature"),

    # McCullough Foundation Report → contested vaccine cluster
    ("EVD-001449", "hypothesis", "HYP-0044", "positive",
     "136-study review with 107 positive inferences"),
    ("EVD-001449", "hypothesis", "HYP-0066", "positive",
     "Hep B birth-dose subset signal"),
    ("EVD-001449", "hypothesis", "HYP-0067", "positive",
     "Aluminum adjuvant subset signal"),
    ("EVD-001449", "hypothesis", "HYP-0068", "positive",
     "MMR subset signal"),
    ("EVD-001449", "hypothesis", "HYP-0069", "positive",
     "Thimerosal subset signal"),
]
for fid, ttype, tid, direction, note in links_def:
    new_links.append({
        "id": f"EVL-{link_id:06d}",
        "evidence_fragment_id": fid, "claim_id": "",
        "target_type": ttype, "target_id": tid,
        "effect_direction": direction, "weight": "", "context_scope": "",
        "created_at": NOW, "notes": note,
    })
    link_id += 1

# === Append to canonical CSVs ===
def append(path, fields, rows_to_add, id_field="id"):
    rows = list(csv.DictReader(open(path)))
    existing = {r[id_field] for r in rows}
    added = 0
    for r in rows_to_add:
        if r[id_field] in existing: continue
        out = {f: r.get(f, "") for f in fields}
        rows.append(out); added += 1
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
    return added

for d in [ROOT/"v2.0_scored", ROOT/"v2.0.1_expanded"]:
    print(f"\n{d.name}:")
    src_fields = list(csv.DictReader(open(d/"sources.csv")).fieldnames)
    n = append(d/"sources.csv", src_fields, new_sources)
    print(f"  sources.csv: +{n}")
    frag_fields = list(csv.DictReader(open(d/"evidence_fragments.csv")).fieldnames)
    n = append(d/"evidence_fragments.csv", frag_fields, new_fragments)
    print(f"  evidence_fragments.csv: +{n}")
    link_fields = list(csv.DictReader(open(d/"evidence_links.csv")).fieldnames)
    n = append(d/"evidence_links.csv", link_fields, new_links)
    print(f"  evidence_links.csv: +{n}")

print()
print("Done. Next: run scoring, verify INT-0001 calibration, rebuild vault.")
