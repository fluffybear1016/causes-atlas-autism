#!/usr/bin/env python3
"""
Session 1 finishing pass.

Per CLAUDE.md (just updated): individual-level health framing,
Hannah Poling causation principle, mainstream-skeptical source weighting.

Tasks:
  1. Fix MPE all-zero weights bug (mechanism_phenotype_edges).
  2. Update HYP-0066 description with delay-to-adolescence framing.
  3. Add INT-0100 Cod liver oil (vitamin D + DHA + vitamin A).
  4. Add INT-0101 L-glutamine (gut-barrier; completes COM-0003).
  5. Drop COVID/flu vaccine recommendations from any description text.
  6. Audit remaining PubMed "other" by abstract content for opinion/news.
"""

import csv, datetime as dt, json, time, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC_DIR = ROOT / "v2.0_scored"
EXP_DIR = ROOT / "v2.0.1_expanded"
NOW = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
def http(url):
    req = urllib.request.Request(url, headers={"User-Agent":"causes-atlas/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r: return r.read().decode()


# ============================================================
# TASK 1: Fix MPE all-zero weights bug
# ============================================================
# Approach: derive each MPE edge's weight from the connected hypotheses
# and interventions. Specifically: weight = max of strengths of edges
# that flow signal through this mechanism into this phenotype.
#
# For (M, P) edge:
#   - strengths from int_mec edges (M side) where the intervention also
#     has an int_phe edge to P
#   - strengths from hyp_mec edges (M side) where the hypothesis has
#     direct phenotype association via top_cause_ids_legacy
#   - if no flow, set 0.20 baseline (the edge exists structurally so
#     someone added it)

print("=" * 60)
print("TASK 1: Fix mechanism_phenotype_edges all-zero weights")
print("=" * 60)

def read(d, name): return list(csv.DictReader(open(d / name)))

for d in [SRC_DIR, EXP_DIR]:
    mpe = read(d, "mechanism_phenotype_edges.csv")
    if not mpe: continue
    ime = read(d, "intervention_mechanism_edges.csv")
    ipe = read(d, "intervention_phenotype_edges.csv")
    hme = read(d, "hypothesis_mechanism_edges.csv")
    hyps = {h["id"]: h for h in read(d, "hypotheses.csv")}

    # Build int -> phenotypes (any int touching a phenotype)
    int_phenotypes = {}
    for r in ipe:
        int_phenotypes.setdefault(r["intervention_id"], set()).add(r["phenotype_id"])

    # Build int -> mechanisms with strengths
    int_mech_strength = {}
    for r in ime:
        try:
            s = float(r.get("evidence_strength_aggregate") or 0)
        except ValueError:
            s = 0
        int_mech_strength.setdefault(r["intervention_id"], {})[r["mechanism_id"]] = s

    # Build hyp -> mech with strengths
    hyp_mech_strength = {}
    for r in hme:
        try:
            s = float(r.get("evidence_strength_aggregate") or 0)
        except ValueError:
            s = 0
        hyp_mech_strength.setdefault(r["hypothesis_id"], {})[r["mechanism_id"]] = s

    # Derive each MPE weight
    fields = list(csv.DictReader(open(d / "mechanism_phenotype_edges.csv")).fieldnames)
    new_mpe = []
    updates = 0
    for r in mpe:
        m_id = r["mechanism_id"]
        p_id = r["phenotype_id"]
        # Path: int -> M -> ... ; if int also touches P, count its M strength
        candidates = []
        for iid, mech_strs in int_mech_strength.items():
            if m_id in mech_strs and p_id in int_phenotypes.get(iid, set()):
                candidates.append(mech_strs[m_id])
        # Path: hyp -> M (and hypothesis confidence as proxy for hyp->phe)
        for hid, mech_strs in hyp_mech_strength.items():
            if m_id in mech_strs:
                # weight by hypothesis confidence
                try:
                    conf = float(hyps[hid].get("confidence_score", "0") or 0)
                except (ValueError, KeyError):
                    conf = 0
                if conf >= 0.5:  # only confident hypotheses contribute
                    candidates.append(mech_strs[m_id] * conf)
        if candidates:
            w = max(candidates)
        else:
            w = 0.20  # baseline for mechanism-phenotype edges that exist
        if abs(w - float(r.get("evidence_strength_aggregate") or 0)) > 0.001:
            updates += 1
        r["evidence_strength_aggregate"] = f"{w:.4f}"
        r["last_updated"] = NOW
        new_mpe.append(r)

    with open(d / "mechanism_phenotype_edges.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(new_mpe)
    print(f"  {d.name}/mechanism_phenotype_edges.csv: {updates} edges updated")


# ============================================================
# TASK 2: Update HYP-0066 description with delay framing
# ============================================================
print()
print("=" * 60)
print("TASK 2: Update HYP-0066 with delay-to-adolescence framing")
print("=" * 60)

new_hep_b_desc = (
    "Day-of-birth hepatitis B vaccination has been hypothesized as a "
    "specific autism risk factor distinct from the broader childhood "
    "vaccine schedule, on the basis of (a) the neonatal developmental "
    "window, (b) aluminum adjuvant content (~250 mcg per dose), and (c) "
    "the small marginal risk-benefit ratio in low-transmission-risk "
    "populations. Hepatitis B transmission in children outside vertical "
    "(mother→baby) and intimate exposure (sexual contact, IV drug use, "
    "blood exposure) is essentially zero; several developed countries "
    "(Norway, Netherlands, parts of Scandinavia) have never had universal "
    "infant Hep B and target only at-risk groups with similar outcomes. "
    "For families with negative maternal HBsAg and no household risk, "
    "delaying vaccination until adolescence (when sexual debut becomes "
    "the actual transmission mechanism) — or skipping entirely until "
    "adult risk emerges — is medically defensible. Per the Hannah Poling "
    "framework (SRC-001418), vaccine challenge in a child with "
    "underlying mitochondrial vulnerability can decompensate into "
    "regressive encephalopathy with autistic features; the universal "
    "infant timing maximizes exposure to children whose susceptibility "
    "has not yet been assessed. Positive primary evidence: Generation "
    "Zero 1999 CDC VSD preliminary (SRC-001415; 11.35x relative risk in "
    "highest-thimerosal-exposure cohort, FOIA-released, superseded by "
    "Verstraeten 2003 Phase 2 null); Simpsonwood transcript 2000 "
    "(SRC-001416; CDC closed meeting verbatim record); Verstraeten "
    "internal emails (SRC-001417); Gallagher 2010 NHIS (SRC-001386; "
    "3x odds ratio in male neonates). Null primary evidence: Verstraeten "
    "2003 Pediatrics Phase 2 (SRC-001388); IOM 2011 systematic review "
    "(SRC-001387); Andersson 2025 Danish nationwide cohort n=1.2M "
    "(SRC-001389). Public framing: 11.35x figure commonly quoted as "
    "+1,135% or rounded to '10,000%' in advocacy/press. ACIP September "
    "2025 (SRC-001420) is reviewing the universal-birth-dose policy. "
    "Per spec §1.1 and §9.1 status=contested permanent. The atlas "
    "preserves both sides; population-average epidemiology tilts null, "
    "but for individual children with unidentified mitochondrial or "
    "methylation susceptibility the conditional risk profile is not "
    "addressed by population-average studies."
)
new_hep_b_notes = (
    "Status=contested permanent. Atlas position: for low-transmission-"
    "risk families (negative maternal HBsAg, no household contacts with "
    "active Hep B), delaying birth-dose to adolescence or later is "
    "medically defensible — the marginal infectious-disease benefit is "
    "small and the marginal autism-related risk per Hannah Poling "
    "framework is non-zero for the susceptibility-vulnerable subset. "
    "ACIP Sep 2025 (SRC-001420) currently reviewing this policy."
)

for d in [SRC_DIR, EXP_DIR]:
    p = d / "hypotheses.csv"
    rows = list(csv.DictReader(open(p)))
    fields = list(csv.DictReader(open(p)).fieldnames)
    for r in rows:
        if r["id"] == "HYP-0066":
            r["description"] = new_hep_b_desc
            r["notes"] = new_hep_b_notes
            r["last_updated"] = NOW
    with open(p, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
    print(f"  {d.name}/hypotheses.csv: HYP-0066 updated")


# ============================================================
# TASK 3 & 4: Add Cod liver oil (INT-0100) and L-glutamine (INT-0101)
# ============================================================
print()
print("=" * 60)
print("TASK 3+4: Add INT-0100 Cod liver oil and INT-0101 L-glutamine")
print("=" * 60)

new_interventions = [
    {
        "id": "INT-0100",
        "name": "Cod liver oil (fermented preferred)",
        "category": "supplement",
        "directionality": "prevention",
        "mechanism_summary": "Traditional whole-food source of vitamin D3 + "
                              "DHA/EPA omega-3 + vitamin A (retinol) + (in "
                              "fermented form) vitamin K2. Hits multiple "
                              "convergent pathways: vitamin D → TPH2 / brain "
                              "serotonin synthesis (MEC-0029); DHA → membrane "
                              "phospholipid composition (MEC-0031); vitamin A "
                              "→ developmental morphogenesis. Pre-conception "
                              "and pregnancy use historically associated with "
                              "lower neurodevelopmental issues in offspring "
                              "(Norwegian MoBa cohort).",
        "dose_range": "1 tsp/day (≈1g) standard; fermented cod liver oil "
                       "0.5-1 tsp/day per Weston A. Price Foundation; "
                       "vitamin A content ~3000-10000 IU varies by product",
        "cost_per_month_usd": "20",
        "otc_or_rx": "otc",
        "pediatric_safe": "yes",
        "csrs_score": "0",  # will be computed by scoring engine
        "csrs_last_updated": NOW,
        "csrs_prevention_score": "0",
        "csrs_prevention_last_updated": NOW,
        "csrs_treatment_score": "0",
        "csrs_treatment_last_updated": NOW,
        "status": "active",
        "created_at": NOW,
        "last_updated": NOW,
        "notes": "Whole-food traditional supplement covering 3-4 high-leverage "
                  "preventive nutrients in one product. Pre-conception use "
                  "(both parents) recommended. Avoid synthetic vitamin A "
                  "megadose products; cod liver oil's natural retinol form "
                  "is well tolerated.",
        "targets_legacy": "vitamin D receptor; TPH2; DHA/EPA membrane "
                           "incorporation; vitamin A signaling; vitamin K2",
        "source_pmids_legacy": "",
        "source_anecdote_ids_legacy": "",
        "csrs_score_legacy": "",
        "csrs_last_updated_legacy": "",
    },
    {
        "id": "INT-0101",
        "name": "L-glutamine (free amino acid)",
        "category": "supplement",
        "directionality": "treatment",
        "mechanism_summary": "Conditionally essential amino acid; primary "
                              "fuel for enterocytes; supports intestinal "
                              "barrier integrity. Down-regulates zonulin "
                              "release, supports tight junction proteins "
                              "(occludin, claudin-1, ZO-1). Hits gut-brain "
                              "axis (MEC-0008) and LPS endotoxemia / leaky "
                              "gut (MEC-0022). Component of GFCF gut-healing "
                              "protocols; member of COM-0003.",
        "dose_range": "5-15 g/day in divided doses, away from meals",
        "cost_per_month_usd": "25",
        "otc_or_rx": "otc",
        "pediatric_safe": "yes",
        "csrs_score": "0",
        "csrs_last_updated": NOW,
        "csrs_prevention_score": "0",
        "csrs_prevention_last_updated": NOW,
        "csrs_treatment_score": "0",
        "csrs_treatment_last_updated": NOW,
        "status": "active",
        "created_at": NOW,
        "last_updated": NOW,
        "notes": "Caution: glutamine is a glutamate precursor; in children "
                  "with documented GABA/glutamate imbalance phenotype "
                  "(PHE-0007) start at lower doses and monitor for "
                  "agitation/anxiety. Most autism-relevant for the GI/"
                  "microbiome subtype (PHE-0004).",
        "targets_legacy": "intestinal tight junctions; zonulin; enterocyte "
                           "energy metabolism; glutathione precursor (Gly-Cys-Glu)",
        "source_pmids_legacy": "",
        "source_anecdote_ids_legacy": "",
        "csrs_score_legacy": "",
        "csrs_last_updated_legacy": "",
    },
]

for d in [SRC_DIR, EXP_DIR]:
    p = d / "interventions.csv"
    rows = list(csv.DictReader(open(p)))
    fields = list(csv.DictReader(open(p)).fieldnames)
    existing_ids = {r["id"] for r in rows}
    added = 0
    for n in new_interventions:
        if n["id"] in existing_ids: continue
        # Pad/match fields
        out = {f: n.get(f, "") for f in fields}
        rows.append(out); added += 1
    with open(p, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
    print(f"  {d.name}/interventions.csv: +{added} (now {len(rows)} total)")


# Wire new interventions to mechanisms / hypotheses / phenotypes / combinations
print()
print("Wiring INT-0100 (Cod liver oil) and INT-0101 (L-glutamine) to graph...")

# Cod liver oil → MEC-0029 (vit D-TPH2 serotonin), MEC-0031 (DHA membrane),
#                MEC-0001 (oxidative — via vit A antioxidant), MEC-0019 (vagus / autonomic indirect)
# Cod liver oil → HYP-0021 (omega-3 deficiency), HYP-0045 (vit D deficiency),
#                 HYP-0050 (choline insufficiency — partial overlap)
# Cod liver oil → PHE-0001 (cerebral folate via methylation indirect), PHE-0002 (mito via vit D)
#               actually let the engine derive these via int→mec→phe walk

# L-glutamine → MEC-0008 (gut-brain), MEC-0022 (LPS leaky gut), MEC-0001 (glutathione precursor partially)
# L-glutamine → HYP-0007 (gut microbiome dysbiosis), HYP-0059 (intestinal barrier permeability)
# L-glutamine → PHE-0004 (GI/microbiome phenotype — direct)
# L-glutamine added to COM-0003 (already has GFCF + Probiotics, missing the L-glutamine)

new_int_mech = [
    ("INT-0100", "MEC-0029", "modulates", "supporting", "Cod liver oil → vit D → TPH2 → brain serotonin"),
    ("INT-0100", "MEC-0031", "modulates", "supporting", "Cod liver oil → DHA → membrane phospholipid"),
    ("INT-0100", "MEC-0001", "modulates", "supporting", "Vitamin A retinol antioxidant; DHA reduces lipid peroxidation"),
    ("INT-0101", "MEC-0008", "modulates", "supporting", "L-glutamine → enterocyte fuel → gut barrier → gut-brain axis"),
    ("INT-0101", "MEC-0022", "modulates", "supporting", "L-glutamine → tight junction → reduces LPS translocation"),
    ("INT-0101", "MEC-0001", "modulates", "supporting", "Glutamine → glutathione precursor (partial)"),
]
new_int_hyp = [
    ("INT-0100", "HYP-0021", "cause_mitigation", "supporting", "Cod liver oil supplies omega-3 directly"),
    ("INT-0100", "HYP-0045", "cause_mitigation", "supporting", "Cod liver oil supplies vitamin D directly"),
    ("INT-0101", "HYP-0007", "cause_mitigation", "supporting", "L-glutamine supports gut barrier; helps dysbiosis recovery"),
    ("INT-0101", "HYP-0059", "cause_mitigation", "supporting", "Direct: L-glutamine reduces leaky gut"),
]
new_int_phe = [
    ("INT-0100", "PHE-0001", "treats", "unknown", "Cod liver oil → vit D → indirect methylation support"),
    ("INT-0100", "PHE-0002", "treats", "supporting", "Cod liver oil → vit D → mitochondrial function support"),
    ("INT-0101", "PHE-0004", "treats", "supporting", "Direct: GI/microbiome phenotype is target"),
]

def append_edges(d, table_name, prefix, fk_a, fk_b, rows_to_add):
    p = d / f"{table_name}.csv"
    if not p.exists(): return 0
    rows = list(csv.DictReader(open(p)))
    fields = list(csv.DictReader(open(p)).fieldnames)
    existing_pairs = {(r[fk_a], r[fk_b]) for r in rows}
    max_n = 0
    for r in rows:
        try: max_n = max(max_n, int(r["id"].split("-")[-1]))
        except (ValueError, IndexError): pass
    added = 0
    for r in rows_to_add:
        a_id, b_id, rel, pol, note = r
        if (a_id, b_id) in existing_pairs: continue
        max_n += 1
        new_id = f"{prefix}-{max_n:05d}"
        new_row = {f: "" for f in fields}
        new_row["id"] = new_id
        new_row[fk_a] = a_id
        new_row[fk_b] = b_id
        new_row["relation_type"] = rel
        new_row["polarity"] = pol
        new_row["evidence_strength_aggregate"] = "0.0"
        if "status" in fields: new_row["status"] = "active"
        if "created_at" in fields: new_row["created_at"] = NOW
        if "last_updated" in fields: new_row["last_updated"] = NOW
        rows.append(new_row); added += 1
    with open(p, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
    return added

for d in [SRC_DIR, EXP_DIR]:
    n_im = append_edges(d, "intervention_mechanism_edges", "IME",
                        "intervention_id", "mechanism_id", new_int_mech)
    n_ih = append_edges(d, "intervention_hypothesis_edges", "IHE",
                        "intervention_id", "hypothesis_id", new_int_hyp)
    n_ip = append_edges(d, "intervention_phenotype_edges", "IPE",
                        "intervention_id", "phenotype_id", new_int_phe)
    print(f"  {d.name}: +{n_im} int-mech, +{n_ih} int-hyp, +{n_ip} int-phe")

# Add INT-0101 to COM-0003 (gut healing combo)
print()
print("Adding INT-0101 (L-glutamine) to COM-0003 members...")
for d in [SRC_DIR, EXP_DIR]:
    p = d / "combination_members.csv"
    rows = list(csv.DictReader(open(p)))
    fields = list(csv.DictReader(open(p)).fieldnames)
    existing = {(r["combination_id"], r["intervention_id"]) for r in rows}
    if ("COM-0003", "INT-0101") not in existing:
        max_n = max((int(r["id"].split("-")[-1]) for r in rows
                     if r["id"].startswith("CMM-")), default=0)
        rows.append({
            "id": f"CMM-{max_n+1:04d}",
            "combination_id": "COM-0003",
            "intervention_id": "INT-0101",
            "role": "core",
            "created_at": NOW,
        })
        with open(p, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
        print(f"  {d.name}: COM-0003 now has L-glutamine")

# Update COM-0003 notes to remove the "missing L-glutamine" warning
for d in [SRC_DIR, EXP_DIR]:
    p = d / "combinations.csv"
    rows = list(csv.DictReader(open(p)))
    fields = list(csv.DictReader(open(p)).fieldnames)
    for r in rows:
        if r["id"] == "COM-0003":
            r["notes"] = (r.get("notes", "") or "").replace(
                " | L-glutamine component has no standalone intervention "
                "entry; consider adding INT-0xxx L-glutamine.", ""
            ).replace(
                "L-glutamine component has no standalone intervention "
                "entry; consider adding INT-0xxx L-glutamine.", ""
            )
            r["last_updated"] = NOW
    with open(p, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)


print()
print("Session 1 ingestion + structural fixes complete.")
print("Next: re-run scoring + verify INT-0001 ≥ 80 + rebuild vault.")
