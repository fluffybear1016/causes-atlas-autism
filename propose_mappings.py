#!/usr/bin/env python3
"""
propose_mappings.py — Best-judgment graph completion proposal.

Two phases, both written to v2.0.1_proposed/ (NEVER to v2.0_scored/).

Phase A: deterministic transitive walks
  intervention_phenotype_edges via int → mechanism → phenotype.

Phase B: orphan wiring
  Specific proposed edges for the 5 orphans, each justified with the
  underlying biology and (where possible) a PubMed PMID for lookup.
  These are CANDIDATES, not commitments.

Outputs:
  v2.0.1_proposed/derived_intervention_phenotype_edges.csv
  v2.0.1_proposed/candidate_orphan_edges.csv
  v2.0.1_proposed/PROPOSAL.md (rationale)
  vault/MAPPING_PROPOSAL.md  (same content, vault-readable)

Run with:  python3 propose_mappings.py
"""

from __future__ import annotations

import csv
import datetime as dt
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "v2.0_scored"
PROP = ROOT / "v2.0.1_proposed"
VAULT = ROOT / "vault"
PROP.mkdir(parents=True, exist_ok=True)

NOW = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")

_FN_BAD = re.compile(r"[\\/:*?\"<>|\[\]#^]")


def sanitize(s: str) -> str:
    if not s:
        return ""
    s = _FN_BAD.sub(" ", s)
    s = " ".join(s.split())
    return s[:80].rstrip()


def read(name: str) -> list[dict]:
    p = SRC / name
    if not p.exists():
        return []
    with open(p, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            # ensure all fields present
            for k in fieldnames:
                r.setdefault(k, "")
            w.writerow({k: r[k] for k in fieldnames})


# ---------------------------------------------------------------- read
hypotheses = read("hypotheses.csv")
mechanisms = read("mechanisms.csv")
interventions = read("interventions.csv")
phenotypes = read("phenotypes.csv")
genes = read("genes.csv")

ime = read("intervention_mechanism_edges.csv")
mpe = read("mechanism_phenotype_edges.csv")
ihe = read("intervention_hypothesis_edges.csv")
hme = read("hypothesis_mechanism_edges.csv")

label = {}
for r in hypotheses + mechanisms + interventions + phenotypes:
    label[r["id"]] = f"{r['id']} {sanitize(r.get('name', ''))}".strip()
for r in genes:
    label[r["id"]] = f"{r['id']} {sanitize(r.get('gene_symbol',''))}".strip()


def L(eid: str) -> str:
    return label.get(eid, eid)


# ============================================================ PHASE A
# Walk intervention → mechanism → phenotype.

# Build adjacency tables
int_to_mec: dict[str, list[tuple[str, float]]] = defaultdict(list)
for r in ime:
    iid = (r.get("intervention_id") or "").strip()
    mid = (r.get("mechanism_id") or "").strip()
    if not iid or not mid:
        continue
    try:
        w = float(r.get("evidence_strength_aggregate", "") or 0)
    except ValueError:
        w = 0.0
    int_to_mec[iid].append((mid, w))

mec_to_phe: dict[str, list[tuple[str, float]]] = defaultdict(list)
for r in mpe:
    mid = (r.get("mechanism_id") or "").strip()
    pid = (r.get("phenotype_id") or "").strip()
    if not mid or not pid:
        continue
    try:
        w = float(r.get("evidence_strength_aggregate", "") or 0)
    except ValueError:
        w = 0.0
    mec_to_phe[mid].append((pid, w))

# Compose paths intervention → mechanism → phenotype
derived: dict[tuple[str, str], dict] = {}
for iid, mech_list in int_to_mec.items():
    for mid, w1 in mech_list:
        for pid, w2 in mec_to_phe.get(mid, []):
            key = (iid, pid)
            # Edge weight = min of the two hops (conservative)
            new_w = min(w1, w2) if w1 and w2 else 0.0
            cur = derived.get(key)
            if cur is None or new_w > cur["weight"]:
                derived[key] = {
                    "weight": new_w,
                    "via_mechanism": mid,
                }

# Emit as CSV
PROP_FIELDS = [
    "id", "intervention_id", "phenotype_id",
    "relation_type", "polarity",
    "evidence_for_count", "evidence_against_count",
    "evidence_strength_aggregate", "context_scope",
    "status", "created_at", "last_updated",
    "derivation_via_mechanism_id",
    "derivation_note",
]
rows_a = []
for i, ((iid, pid), info) in enumerate(sorted(derived.items()), start=1):
    rows_a.append({
        "id": f"DIPE-{i:05d}",
        "intervention_id": iid,
        "phenotype_id": pid,
        "relation_type": "derived_via_int_mec_phe_walk",
        "polarity": "unknown",
        "evidence_for_count": "",
        "evidence_against_count": "",
        "evidence_strength_aggregate": f"{info['weight']:.4f}",
        "context_scope": "",
        "status": "proposed",
        "created_at": NOW,
        "last_updated": NOW,
        "derivation_via_mechanism_id": info["via_mechanism"],
        "derivation_note": (
            f"transitive: {iid} -[modulates]-> "
            f"{info['via_mechanism']} -[implicated_in]-> {pid}"
        ),
    })
write_csv(PROP / "derived_intervention_phenotype_edges.csv", PROP_FIELDS, rows_a)
print(f"Phase A: {len(rows_a)} derived intervention→phenotype edges")

# ============================================================ PHASE B
# Orphan wiring (best-judgment, with PMIDs for verification).
#
# Each row is a *candidate* edge. The user reviews the rationale and
# decides whether to merge into the canonical state.

CAND_FIELDS = [
    "id", "from_id", "from_type", "to_id", "to_type",
    "edge_table", "relation_type", "polarity",
    "rationale", "supporting_pmids",
    "status", "created_at",
]
candidates: list[dict] = []


def cand(from_id, from_type, to_id, to_type, edge_table, relation_type,
         polarity, rationale, pmids):
    candidates.append({
        "id": f"CAND-{len(candidates)+1:04d}",
        "from_id": from_id,
        "from_type": from_type,
        "to_id": to_id,
        "to_type": to_type,
        "edge_table": edge_table,
        "relation_type": relation_type,
        "polarity": polarity,
        "rationale": rationale,
        "supporting_pmids": ";".join(pmids) if pmids else "",
        "status": "proposed",
        "created_at": NOW,
    })


# ---------- HYP-0025 Prenatal viral infection (rubella, CMV, flu) -----
# Maternal Immune Activation (MIA). Patterson lab work, Atladóttir
# epidemiology, Smith et al. poly(I:C) IL-6 model. Tightly tied to
# neuroinflammation and microglial activation pathways.
cand("HYP-0025", "hypothesis", "MEC-0002", "mechanism",
     "hypothesis_mechanism_edges", "acts_through", "supporting",
     "Maternal viral infection drives sustained fetal neuroinflammation "
     "via maternal cytokine surge (IL-6, IL-17a). MIA model is the most "
     "studied prenatal autism risk pathway.",
     ["19533774", "17314324", "26773308"])
cand("HYP-0025", "hypothesis", "MEC-0005", "mechanism",
     "hypothesis_mechanism_edges", "acts_through", "supporting",
     "MIA produces persistent microglial priming in offspring; replicated "
     "in poly(I:C) and LPS rodent models.",
     ["17314324", "27121379"])
cand("HYP-0025", "hypothesis", "MEC-0017", "mechanism",
     "hypothesis_mechanism_edges", "acts_through", "supporting",
     "Maternal mast-cell / histaminergic activation contributes to BBB "
     "permeability changes downstream of MIA.",
     ["27121379"])
cand("HYP-0025", "hypothesis", "PHE-0003", "phenotype",
     "intervention_phenotype_edges", "manifests_as", "supporting",
     "Children exposed to first-trimester maternal infection show elevated "
     "regression rates and immune-inflammatory phenotype markers.",
     ["19533774"])

# ---------- HYP-0028 Inherited polygenic risk -------------------------
# The genetic-architecture meta-hypothesis. Should connect to mechanisms
# implicated by SFARI Tier-1 genes (synaptic pruning, mTOR, GABA/Glu).
cand("HYP-0028", "hypothesis", "MEC-0006", "mechanism",
     "hypothesis_mechanism_edges", "acts_through", "supporting",
     "SHANK3, NLGN, NRXN, FMR1 — the SFARI Tier-1 synaptic genes — converge "
     "on synaptic pruning/maturation pathways.",
     ["26402605", "30804558"])
cand("HYP-0028", "hypothesis", "MEC-0007", "mechanism",
     "hypothesis_mechanism_edges", "acts_through", "supporting",
     "Polygenic risk converges on E/I balance via SCN2A, GRIN2B, GABRB3 "
     "channelopathies.",
     ["30804558"])
cand("HYP-0028", "hypothesis", "MEC-0009", "mechanism",
     "hypothesis_mechanism_edges", "acts_through", "supporting",
     "TSC1, TSC2, PTEN syndromic mutations confirm mTOR is a major "
     "convergence point of monogenic and polygenic ASD risk.",
     ["28279400"])
cand("HYP-0028", "hypothesis", "PHE-0005", "phenotype",
     "intervention_phenotype_edges", "manifests_as", "supporting",
     "Polygenic risk enriched in mTOR-pathway syndromic phenotype "
     "(TSC, PTEN macrocephaly).",
     ["28279400"])
cand("HYP-0028", "hypothesis", "PHE-0006", "phenotype",
     "intervention_phenotype_edges", "manifests_as", "supporting",
     "FMR1 is the canonical polygenic-→-syndromic bridge.",
     ["19015572"])

# ---------- MEC-0013 FOXO transcription factors -----------------------
# Downstream node integrator: insulin/IGF-1 → AKT → FOXO inhibition;
# AMPK → FOXO activation; SIRT1 → FOXO deacetylation/activation.
# Regulates oxidative stress response, autophagy, mitochondrial biogenesis.
cand("INT-0036", "intervention", "MEC-0013", "mechanism",
     "intervention_mechanism_edges", "modulates", "supporting",
     "Rapamycin (mTOR inhibitor) → FOXO disinhibition. Rapamycin's "
     "neuroprotective profile in autism syndromic models partially "
     "operates through FOXO-driven autophagy.",
     ["23446215"])
cand("INT-0028", "intervention", "MEC-0013", "mechanism",
     "intervention_mechanism_edges", "modulates", "supporting",
     "Resveratrol activates SIRT1 → SIRT1 deacetylates FOXO3a → activates "
     "FOXO antioxidant + autophagy program.",
     ["18332217"])
cand("INT-0093", "intervention", "MEC-0013", "mechanism",
     "intervention_mechanism_edges", "modulates", "supporting",
     "Alpha-lipoic acid restores insulin sensitivity → modulates AKT-FOXO "
     "axis under conditions of insulin resistance.",
     ["20191641"])
cand("INT-0047", "intervention", "MEC-0013", "mechanism",
     "intervention_mechanism_edges", "modulates", "supporting",
     "Aerobic exercise activates AMPK → AMPK directly phosphorylates FOXO3 "
     "→ promotes mitochondrial biogenesis and autophagy.",
     ["17712357"])

# ---------- INT-0021 Lithium orotate ---------------------------------
cand("INT-0021", "intervention", "MEC-0028", "mechanism",
     "intervention_mechanism_edges", "modulates", "supporting",
     "Lithium inhibits GSK-3β → stabilizes β-catenin → upregulates BDNF "
     "expression. Well-characterized neurotrophic mechanism.",
     ["18046408"])
cand("INT-0021", "intervention", "MEC-0009", "mechanism",
     "intervention_mechanism_edges", "modulates", "supporting",
     "GSK-3β cross-talks with mTOR (TSC2 phosphorylation); lithium thus "
     "indirectly modulates mTOR pathway activity.",
     ["18046408"])

# ---------- INT-0022 Inositol -----------------------------------------
cand("INT-0022", "intervention", "MEC-0015", "mechanism",
     "intervention_mechanism_edges", "modulates", "supporting",
     "Myo-inositol is the precursor for phosphoinositides (PIP2, PIP3) "
     "that underlie PI3K/AKT signaling.",
     [])
cand("INT-0022", "intervention", "HYP-0055", "hypothesis",
     "intervention_hypothesis_edges", "cause_mitigation", "supporting",
     "Inositol depletion has been linked to serotonergic/repetitive-"
     "behavior circuits via PI cycle exhaustion (lithium hypothesis).",
     ["8602510"])

# ---------- INT-0024 Glycine ------------------------------------------
cand("INT-0024", "intervention", "MEC-0020", "mechanism",
     "intervention_mechanism_edges", "modulates", "supporting",
     "Glycine is an obligate co-agonist at the NMDA receptor glycine site; "
     "directly modulates calcium/glutamate-NMDA homeostasis.",
     ["20800012"])
cand("INT-0024", "intervention", "MEC-0001", "mechanism",
     "intervention_mechanism_edges", "modulates", "supporting",
     "Glycine is one of three amino acid precursors of glutathione (γ-Glu-"
     "Cys-Gly); supplies oxidative-stress defense substrate.",
     [])

# ---------- INT-0041 GFCF diet ----------------------------------------
cand("INT-0041", "intervention", "MEC-0008", "mechanism",
     "intervention_mechanism_edges", "modulates", "unknown",
     "Removes gliadin/casomorphin opioid peptides; modulates gut-brain axis. "
     "RCT evidence for whole-population is null/mixed; effect concentrated "
     "in GI/microbiome-phenotype subset.",
     ["19878495"])
cand("INT-0041", "intervention", "MEC-0022", "mechanism",
     "intervention_mechanism_edges", "modulates", "supporting",
     "Reduces intestinal permeability / LPS translocation in zonulin-"
     "elevated subset.",
     ["19878495"])
cand("INT-0041", "intervention", "PHE-0004", "phenotype",
     "intervention_phenotype_edges", "treats", "supporting",
     "Responder phenotype is the GI/microbiome subgroup specifically.",
     ["19878495"])

# ---------- INT-0049 Sunlight exposure --------------------------------
cand("INT-0049", "intervention", "MEC-0029", "mechanism",
     "intervention_mechanism_edges", "modulates", "supporting",
     "UVB-driven cutaneous vitamin D synthesis is the principal natural "
     "source; vitamin D regulates TPH2 / brain serotonin synthesis.",
     ["24558199"])
cand("INT-0049", "intervention", "MEC-0016", "mechanism",
     "intervention_mechanism_edges", "modulates", "supporting",
     "Morning sunlight entrains the suprachiasmatic nucleus and normalizes "
     "the HPA cortisol awakening response.",
     [])

write_csv(PROP / "candidate_orphan_edges.csv", CAND_FIELDS, candidates)
print(f"Phase B: {len(candidates)} orphan-wiring candidate edges")

# ============================================================ MD report
md = []
md.append("---")
md.append("type: proposal")
md.append('title: "v2.0.1 mapping proposal — graph completion"')
md.append("---")
md.append("")
md.append("# v2.0.1 Mapping Proposal")
md.append("")
md.append("Two-phase proposal to fill the worst gaps in the v2.0_scored "
          "atlas before any factorial-combinations work.")
md.append("")
md.append("**Nothing has been written to `v2.0_scored/`.** All output is "
          "in `v2.0.1_proposed/` for review.")
md.append("")

md.append("## Phase A — Deterministic transitive walk")
md.append("")
md.append(f"**File:** `v2.0.1_proposed/derived_intervention_phenotype_edges.csv`")
md.append(f"**Rows generated:** {len(rows_a)}")
md.append("")
md.append("Walks every existing `intervention → mechanism → phenotype` path "
          "and emits a derived edge. Edge weight is the **minimum** of the "
          "two hops (conservative — won't strengthen evidence beyond its "
          "weakest link).")
md.append("")
md.append("Every row carries `relation_type=derived_via_int_mec_phe_walk` "
          "and `derivation_via_mechanism_id` so the provenance is fully "
          "auditable. These are not invented — they are walks through "
          "edges that already passed your scoring pipeline.")
md.append("")
md.append("Top 15 by weight:")
md.append("")
md.append("| Intervention | Phenotype | via mechanism | weight |")
md.append("|--------------|-----------|---------------|--------|")
for r in sorted(rows_a, key=lambda x: -float(x["evidence_strength_aggregate"]))[:15]:
    md.append(
        f"| [[{L(r['intervention_id'])}]] | [[{L(r['phenotype_id'])}]] | "
        f"[[{L(r['derivation_via_mechanism_id'])}]] | "
        f"{r['evidence_strength_aggregate']} |"
    )
md.append("")

md.append("## Phase B — Orphan wiring (best-judgment, with PMIDs)")
md.append("")
md.append(f"**File:** `v2.0.1_proposed/candidate_orphan_edges.csv`")
md.append(f"**Candidates proposed:** {len(candidates)}")
md.append("")
md.append("These wire the 5 zero-edge orphans (2 hypotheses, 1 mechanism, "
          "5 interventions — yes the audit under-counted by missing two "
          "edge tables) into the rest of the graph. **Each row has a "
          "`supporting_pmids` column with PubMed IDs you can verify before "
          "merging.** I have not run the citations; treat them as my best "
          "recall and confirm before commit.")
md.append("")

# Group by orphan
groups: dict[str, list[dict]] = defaultdict(list)
for c in candidates:
    groups[c["from_id"]].append(c)

orphan_descriptions = {
    "HYP-0025": ("HYP-0025 Prenatal viral infection (rubella, CMV, flu)",
                 "Maternal Immune Activation hypothesis. Should anchor on "
                 "neuroinflammation + microglial activation."),
    "HYP-0028": ("HYP-0028 Inherited polygenic risk",
                 "Genetic-architecture meta-hypothesis. Should anchor on "
                 "synaptic pruning, E/I balance, mTOR convergence."),
    "INT-0036_FOXO": ("MEC-0013 FOXO transcription factors (orphan mechanism)",
                      "Wired via 4 interventions known to act on the AMPK / "
                      "SIRT1 / mTOR / IGF-1 → FOXO axis."),
    "INT-0021": ("INT-0021 Lithium orotate (low-dose)",
                 "GSK-3β inhibitor → BDNF, mTOR cross-talk."),
    "INT-0022": ("INT-0022 Inositol (myo-inositol)",
                 "Phosphoinositide precursor → PI3K/AKT signaling."),
    "INT-0024": ("INT-0024 Glycine",
                 "NMDA co-agonist + glutathione precursor."),
    "INT-0041": ("INT-0041 GFCF diet",
                 "Gut-brain axis modulator; effect concentrated in GI subset."),
    "INT-0049": ("INT-0049 Sunlight exposure",
                 "UVB-vitamin D + circadian entrainment."),
}

# Group ordering: hypothesis orphans, mechanism orphan, intervention orphans
order = ["HYP-0025", "HYP-0028", "INT-0036", "INT-0028", "INT-0093", "INT-0047",
         "INT-0021", "INT-0022", "INT-0024", "INT-0041", "INT-0049"]
seen_groups = set()
for from_id in order:
    rows = groups.get(from_id)
    if not rows:
        continue
    seen_groups.add(from_id)
    # Description: pick from orphan_descriptions, or label
    if from_id in orphan_descriptions:
        title, desc = orphan_descriptions[from_id]
    elif from_id in {"INT-0036", "INT-0028", "INT-0093", "INT-0047"}:
        # FOXO group — display together
        if "INT-0036_FOXO" not in seen_groups:
            t, d = orphan_descriptions["INT-0036_FOXO"]
            md.append(f"### {t}")
            md.append("")
            md.append(d)
            md.append("")
            md.append("| from | edge | to | rationale | PMIDs |")
            md.append("|------|------|----|-----------|-------|")
            seen_groups.add("INT-0036_FOXO")
        for r in rows:
            md.append(
                f"| [[{L(r['from_id'])}]] | {r['relation_type']} | "
                f"[[{L(r['to_id'])}]] | {r['rationale']} | "
                f"`{r['supporting_pmids']}` |"
            )
        continue
    else:
        title = L(from_id)
        desc = ""
    md.append(f"### {title}")
    md.append("")
    if desc:
        md.append(desc)
        md.append("")
    md.append("| edge | to | rationale | PMIDs |")
    md.append("|------|----|-----------|-------|")
    for r in rows:
        md.append(
            f"| {r['relation_type']} | [[{L(r['to_id'])}]] | "
            f"{r['rationale']} | `{r['supporting_pmids']}` |"
        )
    md.append("")

md.append("## Not addressed in this proposal (intentionally)")
md.append("")
md.append("- **Gene layer densification** (1,564 genes, ~46 edges total). "
          "Needs a SFARI Tier 1/2/3 + OpenTargets cross-walk script. "
          "Separate session.")
md.append("- **Mechanism-overlap candidate hypothesis-hypothesis edges.** "
          "Heuristic: any two hypotheses sharing ≥2 mechanisms are "
          "candidates. Defer until orphans are resolved.")
md.append("- **Source-citation expansion.** Many low-edge entities have "
          "zero source citations. Run `run_ingest.py` against the listed "
          "PMIDs once orphan wiring is approved.")
md.append("")

md.append("## How to apply")
md.append("")
md.append("1. Review `v2.0.1_proposed/derived_intervention_phenotype_edges.csv` "
          "and `candidate_orphan_edges.csv`. Reject any rows you don't "
          "want.")
md.append("2. **For Phase A:** the rows match the canonical schema with "
          "two extra columns. Drop those extra columns and concat into "
          "`v2.0.1_expanded/intervention_phenotype_edges.csv`.")
md.append("3. **For Phase B:** routes by `edge_table` column — fan out to "
          "the appropriate canonical CSVs (e.g. rows with "
          "`edge_table=hypothesis_mechanism_edges` go into that file).")
md.append("4. Run `python3 run_scoring_v20.py` against `v2.0.1_expanded/` "
          "and verify `INT-0001` calibration still ≥ 80.")
md.append("5. Replace `v2.0_scored/` with the new run output, rebuild the "
          "vault: `python3 build_vault.py`.")
md.append("")
md.append(f"_Generated: {NOW}_")

(PROP / "PROPOSAL.md").write_text("\n".join(md) + "\n", encoding="utf-8")
(VAULT / "MAPPING_PROPOSAL.md").write_text("\n".join(md) + "\n", encoding="utf-8")
print(f"\nWrote: {PROP/'derived_intervention_phenotype_edges.csv'}")
print(f"Wrote: {PROP/'candidate_orphan_edges.csv'}")
print(f"Wrote: {PROP/'PROPOSAL.md'}")
print(f"Wrote: {VAULT/'MAPPING_PROPOSAL.md'}")
print()
print(f"Total proposed edges: {len(rows_a)} derived + {len(candidates)} candidates")
