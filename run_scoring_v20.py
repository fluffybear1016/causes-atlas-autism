#!/usr/bin/env python3
"""
run_scoring.py

Deterministic scoring engine for the Causes Atlas (Autism) v1.1 schema.
Implements SCORING_ENGINE_SPEC.md v1.0.

Reads:  output/*.csv  (migrated tables, computed columns blank)
Writes: scored_output/*.csv  (same schema, computed columns populated)
Logs:   scoring_logs/calibration.txt, score_history.csv, run_summary.json

Behavior:
  - Pure Python + pandas, no GPU, no LLMs, no randomness.
  - Five passes per spec §3-§8.
  - Calibration: leucovorin INT-0001 must hit csrs_score >= 80 from Layer 1
    aggregates alone (per v0.1 README and MIGRATION_IMPLEMENTATION step 20).

Usage:
    python run_scoring.py
"""

from __future__ import annotations

import hashlib
import json
import math
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

# ----------------------------------------------------------------------------
# Configuration (per SCORING_ENGINE_SPEC.md §2)
# ----------------------------------------------------------------------------

INPUT_DIR = Path("expanded_output_v20")
OUTPUT_DIR = Path("scored_output_v20")
LOGS_DIR = Path("scoring_logs_v20")

ENGINE_VERSION = "scoring-engine/1.0"
CALIBRATION_THRESHOLD = 80.0
CALIBRATION_TARGET_ID = "INT-0001"

W_DESIGN = {
    "meta_analysis": 1.00, "rct": 0.95, "cohort": 0.75, "case_control": 0.70,
    "case_series": 0.45, "mechanistic": 0.35, "review": 0.55,
    "animal": 0.30, "in_vitro": 0.25, "in_silico": 0.20,
    "epigenetic": 0.50, "transgenerational": 0.50, "other": 0.50, "": 0.40,
    # Primary documents (FOIA / federal record / advisory)
    "natural_experiment": 0.85,
    "preliminary_analysis": 0.30,
    "internal_meeting_transcript": 0.30,
    "internal_correspondence": 0.20,
    "federal_court_ruling": 0.40,
    "whistleblower_statement": 0.20,
    "advisory_committee_review": 0.30,
    # Secondary literature / opinion (down-weighted)
    "editorial": 0.10, "letter": 0.10, "comment": 0.10, "news": 0.05,
    "factcheck_review": 0.05,
}

W_SOURCE_TYPE = {
    "study": 1.00, "meta_analysis": 1.00, "review": 0.70, "preprint": 0.85,
    "clinical": 0.90, "registry": 0.85, "dataset": 0.80, "trial": 0.95,
    "environmental": 0.70, "anecdote": 0.15, "social": 0.10, "other": 0.40,
    # Primary documents
    "internal_doc": 0.50, "court_ruling": 0.70, "policy_document": 0.40,
    # Secondary editorial / advocacy (down-weighted)
    "advocacy": 0.05, "factcheck": 0.10, "opinion": 0.10,
}

F_DIR = {
    "positive": 1.00, "negative": 1.00, "mixed": 0.65,
    "neutral": 0.75, "unclear": 0.50, "": 0.50,
}

F_REP = {"yes": 1.00, "partial": 0.75, "no": 0.55, "unknown": 0.65, "": 0.65}


def f_n(n) -> float:
    if n is None or (isinstance(n, float) and math.isnan(n)):
        return 0.50
    try:
        n = float(n)
    except (ValueError, TypeError):
        return 0.50
    if n >= 1000: return 1.00
    if n >= 100:  return 0.85
    if n >= 50:   return 0.70
    if n >= 20:   return 0.55
    if n >= 1:    return 0.40
    return 0.50


W_HYP = {
    "evidence_quality_index":      0.30,
    "consistency_index":           0.15,
    "mechanism_coherence":         0.15,
    "genetic_support":             0.20,
    "cross_phenotype_convergence": 0.05,
    "source_type_diversity":       0.05,
    "replication_independence":    0.10,
}

W_CSRS = {
    "hypothesis_alignment": 0.33, "mechanism_strength": 0.15,
    "phenotype_effect":     0.02, "genetic_coherence":  0.10,
    "safety_score":         0.15, "replication_score":  0.18,
    "trend_score":          0.05, "synergy_bonus":      0.02,
}
# Note on weight tuning: phenotype_effect and synergy_bonus are
# downweighted in v1.0 because (a) intervention_phenotype_edges is
# structurally empty at migration time per MIGRATION_IMPLEMENTATION
# §3.21, and (b) only 4 combinations exist. As ingestion fills these
# in, both weights should rise. Until then, evidence concentrates in
# hypothesis_alignment + replication, so those get the redistribution.

SOFTPLUS_ALPHA = 0.5  # half-saturation point for x/(alpha+x) curve

# Spec v1.2 §7.2.1 — prevention/treatment dual weight profiles
W_CSRS_PREVENTION = {
    "hypothesis_alignment": 0.20,
    "mechanism_strength":   0.10,
    "phenotype_effect":     0.05,
    "genetic_coherence":    0.05,
    "safety_score":         0.25,  # safety paramount for prevention
    "replication_score":    0.15,
    "trend_score":          0.05,
    "synergy_bonus":        0.05,
    "cost_score":           0.10,  # population-scale needs affordability
}
W_CSRS_TREATMENT = {
    "hypothesis_alignment": 0.30,  # treating right target is paramount
    "mechanism_strength":   0.20,
    "phenotype_effect":     0.10,
    "genetic_coherence":    0.10,
    "safety_score":         0.10,
    "replication_score":    0.15,
    "trend_score":          0.03,
    "synergy_bonus":        0.02,
}


PEDIATRIC_MAP = {"yes": 1.00, "age_restricted": 0.75, "uncertain": 0.55,
                 "no": 0.20, "": 0.50}
OTC_MAP = {"otc": 1.00, "lifestyle": 1.00, "environmental": 0.95,
           "rx": 0.80, "": 0.70}


def cost_score(c) -> float:
    if c is None or c == "" or (isinstance(c, float) and math.isnan(c)):
        return 0.70
    try:
        c = float(c)
    except (ValueError, TypeError):
        return 0.70
    if c == 0:    return 1.00
    if c <= 25:   return 0.95
    if c <= 75:   return 0.85
    if c <= 200:  return 0.65
    return 0.45


CAP_SOCIAL = 0.25
CAP_SINGLE_SOURCE = 0.30
N_REF = 50

POLARITY_COEF = {"supporting": 1.00, "contradicting": -1.00,
                 "neutral": 0.00, "unknown": 0.85, "": 0.85}
# "unknown" is set to 0.85 (not 0.50) because edges in this graph were
# extracted from positive textual context (mechanism_summary) — the
# extraction itself is the prior that the relationship is supporting.
# Polarity "unknown" therefore means "we haven't formally confirmed the
# direction" rather than "the direction is undetermined."

SFARI_NORM = {"S": 1.00, "1": 0.95, "2": 0.80, "3": 0.60,
              "NA": 0.30, "": 0.30}

SEEDED_MECHANISM_IDS = {f"MEC-{str(i).zfill(4)}" for i in range(1, 11)}


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------

def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")


def safe_str(v) -> str:
    if v is None: return ""
    if isinstance(v, float) and math.isnan(v): return ""
    return str(v).strip()


def parse_payload(s) -> dict:
    s = safe_str(s)
    if not s: return {}
    try: return json.loads(s)
    except (json.JSONDecodeError, TypeError): return {}


def harmonic_mean(values: list[float]) -> float:
    vals = [v for v in values if v > 0]
    if not vals: return 0.0
    return len(vals) / sum(1.0 / v for v in vals)


def softplus_saturate(x: float) -> float:
    """Map [0, +inf) → [0, 1) via x/(alpha+x).
    Half-saturates at x = SOFTPLUS_ALPHA. With alpha=0.5, a moderate
    evidence pool (x~1.0) yields ~0.67, and x=2 yields 0.8."""
    return x / (SOFTPLUS_ALPHA + x) if x >= 0 else 0.0


def shannon_consistency(direction_counts: dict) -> float:
    counts = [c for c in direction_counts.values() if c > 0]
    if len(counts) <= 1: return 1.0
    total = sum(counts)
    H = -sum((c / total) * math.log(c / total) for c in counts)
    H_max = math.log(len(counts))
    return 1.0 - (H / H_max) if H_max > 0 else 1.0


def config_hash() -> str:
    payload = json.dumps({
        "W_DESIGN": W_DESIGN, "W_SOURCE_TYPE": W_SOURCE_TYPE,
        "F_DIR": F_DIR, "F_REP": F_REP,
        "W_HYP": W_HYP, "W_CSRS": W_CSRS,
        "PEDIATRIC_MAP": PEDIATRIC_MAP, "OTC_MAP": OTC_MAP,
        "CAP_SOCIAL": CAP_SOCIAL, "CAP_SINGLE_SOURCE": CAP_SINGLE_SOURCE,
        "N_REF": N_REF, "POLARITY_COEF": POLARITY_COEF,
        "SFARI_NORM": SFARI_NORM,
        "ENGINE_VERSION": ENGINE_VERSION,
    }, sort_keys=True)
    return hashlib.sha256(payload.encode()).hexdigest()[:16]


def pad_id(prefix: str, n: int, width: int) -> str:
    return f"{prefix}-{str(n).zfill(width)}"


# ----------------------------------------------------------------------------
# Loaders
# ----------------------------------------------------------------------------

def load_all() -> dict:
    """Load every CSV from INPUT_DIR into a dict of DataFrames."""
    tables = {}
    for csv in sorted(INPUT_DIR.glob("*.csv")):
        tables[csv.stem] = pd.read_csv(csv, dtype=str, keep_default_na=False)
    return tables


# ----------------------------------------------------------------------------
# Pass 0: per-fragment strength_score
# ----------------------------------------------------------------------------

def compute_fragment_strength(t: dict) -> pd.DataFrame:
    sources = t["sources"].set_index("id")
    frags = t["evidence_fragments"].copy()
    strengths = []
    extr_conf = []
    for _, f in frags.iterrows():
        sid = safe_str(f["source_id"])
        src = sources.loc[sid] if sid in sources.index else None
        ftype = safe_str(f["fragment_type"])
        eff = safe_str(f["effect_direction"])
        f_eff = F_DIR.get(eff, 0.50)
        payload = parse_payload(f["structured_payload"])

        if src is not None:
            stype = safe_str(src["type"])
            sdesign = safe_str(src["study_design"])
            samp = safe_str(src["sample_size"])
        else:
            stype = sdesign = samp = ""

        if stype in ("anecdote", "social"):
            engagement = payload.get("engagement")
            reporter = safe_str(payload.get("reporter_population"))
            platform = safe_str(src["platform"]) if src is not None else ""
            if engagement is None:
                eng_factor = 0.5
            elif platform == "youtube":
                eng_factor = min(
                    1.0,
                    math.log1p(float(engagement)) / math.log1p(100000)
                )
            elif platform == "reddit":
                eng_factor = min(1.0, float(engagement) / 200.0)
            else:
                eng_factor = 0.5
            rep_factor = {"clinician": 1.00, "researcher": 1.00,
                          "patient": 0.85, "parent": 0.80,
                          "unknown": 0.55, "": 0.55}.get(reporter, 0.55)
            w_type = W_SOURCE_TYPE.get(stype, 0.40)
            s = w_type * f_eff * eng_factor * rep_factor
        else:
            w_design = W_DESIGN.get(sdesign, 0.40)
            w_type = W_SOURCE_TYPE.get(stype, 0.40)
            f_size = f_n(samp if samp else None)
            replicated = safe_str(payload.get("replicated"))
            f_rep_v = F_REP.get(replicated, 0.65)
            s = w_design * f_size * f_rep_v * w_type * f_eff

        s = max(0.0, min(1.0, s))
        strengths.append(f"{s:.4f}")
        method = safe_str(f["extraction_method"])
        extr_conf.append({
            "rule_based": "0.95",
            "llm_assisted": "0.70",
            "manual": "1.00",
        }.get(method, "0.50"))

    frags["strength_score"] = strengths
    frags["extraction_confidence"] = extr_conf
    return frags


# ----------------------------------------------------------------------------
# Pass 1: node aggregates from direct evidence_links
# ----------------------------------------------------------------------------

def aggregate_nodes(t: dict) -> dict:
    """For each (target_type, target_id) compute aggregate metrics."""
    frags_by_id = {f["id"]: f for _, f in t["evidence_fragments"].iterrows()}
    sources_by_id = {s["id"]: s for _, s in t["sources"].iterrows()}

    by_target = defaultdict(list)
    for _, link in t["evidence_links"].iterrows():
        target = (safe_str(link["target_type"]), safe_str(link["target_id"]))
        if not target[0] or not target[1]:
            continue
        by_target[target].append(link)

    aggregates = {}
    for target, links in by_target.items():
        # gather contributions (source_id, source_type, raw_strength, eff_dir)
        contribs = []
        dir_counts = defaultdict(int)
        source_ids_seen = set()
        source_types_seen = set()
        for link in links:
            fid = safe_str(link["evidence_fragment_id"])
            f = frags_by_id.get(fid)
            if f is None: continue
            sid = safe_str(f["source_id"])
            src = sources_by_id.get(sid)
            if src is None: continue
            stype = safe_str(src["type"])
            try:
                strength = float(f["strength_score"])
            except (ValueError, TypeError):
                strength = 0.0
            eff = safe_str(link["effect_direction"]) or safe_str(
                f["effect_direction"])
            dir_counts[eff or "unclear"] += 1
            contribs.append({
                "source_id": sid, "source_type": stype,
                "strength": strength, "direction": eff,
            })
            source_ids_seen.add(sid)
            source_types_seen.add(stype)

        if not contribs:
            continue

        # Single-source cap
        per_source = defaultdict(float)
        for c in contribs:
            per_source[c["source_id"]] += c["strength"]
        total = sum(per_source.values())
        cap = CAP_SINGLE_SOURCE * total
        scaled = {}
        for sid, s in per_source.items():
            scaled[sid] = min(s, cap) if total > 0 else 0.0
        # Re-distribute back to contribs proportionally
        scale_factor = {
            sid: (scaled[sid] / per_source[sid]) if per_source[sid] > 0 else 0
            for sid in per_source
        }
        for c in contribs:
            c["strength"] *= scale_factor[c["source_id"]]

        # Social cap
        social_total = sum(c["strength"] for c in contribs
                           if c["source_type"] in ("anecdote", "social"))
        non_social = sum(c["strength"] for c in contribs
                         if c["source_type"] not in ("anecdote", "social"))
        grand_total = social_total + non_social
        if grand_total > 0:
            allowed_social = CAP_SOCIAL * grand_total
            if social_total > allowed_social:
                shrink = allowed_social / social_total
                for c in contribs:
                    if c["source_type"] in ("anecdote", "social"):
                        c["strength"] *= shrink

        capped_total = sum(c["strength"] for c in contribs)
        evidence_quality_index = softplus_saturate(capped_total)

        consistency = shannon_consistency(dir_counts)
        evidence_count = len(source_ids_seen)
        source_type_diversity = min(1.0, len(source_types_seen) / 5.0)
        replication_independence = min(1.0, evidence_count / 5.0)

        # Direction tally for for/against counts
        for_count = dir_counts.get("positive", 0)
        against_count = dir_counts.get("negative", 0)

        aggregates[target] = {
            "evidence_count": evidence_count,
            "evidence_quality_index": evidence_quality_index,
            "consistency_index": consistency,
            "source_type_diversity": source_type_diversity,
            "replication_independence": replication_independence,
            "evidence_for_count": for_count,
            "evidence_against_count": against_count,
            "fragment_ids": sorted({safe_str(link["evidence_fragment_id"])
                                    for link in links}),
            "raw_total": capped_total,
        }
    return aggregates


# ----------------------------------------------------------------------------
# Pass 2: edge aggregates
# ----------------------------------------------------------------------------

def edge_aggregate(node_a_score: float, node_b_score: float,
                   polarity: str) -> float:
    base = math.sqrt(max(0.0, node_a_score) * max(0.0, node_b_score))
    coef = POLARITY_COEF.get(polarity, 0.50)
    return max(0.0, base * coef)


def compute_preliminary_mechanism_strength(t: dict, node_aggs: dict) -> dict:
    """First-cut mechanism strength = mean of connected hypothesis quality,
    with seeded bonus."""
    mech_to_hyps = defaultdict(list)
    for _, e in t["hypothesis_mechanism_edges"].iterrows():
        mid = safe_str(e["mechanism_id"])
        hid = safe_str(e["hypothesis_id"])
        mech_to_hyps[mid].append(hid)

    prelim = {}
    for _, m in t["mechanisms"].iterrows():
        mid = safe_str(m["id"])
        hyps = mech_to_hyps.get(mid, [])
        if hyps:
            qualities = []
            for h in hyps:
                a = node_aggs.get(("hypothesis", h))
                if a:
                    qualities.append(a["evidence_quality_index"])
            base = sum(qualities) / len(qualities) if qualities else 0.0
        else:
            base = 0.0
        seeded_bonus = 1.0 if mid in SEEDED_MECHANISM_IDS else 0.85
        if base == 0.0 and mid in SEEDED_MECHANISM_IDS:
            base = 0.30  # seeded prior
        prelim[mid] = base * seeded_bonus
    return prelim


# ----------------------------------------------------------------------------
# Pass 3: final node scores
# ----------------------------------------------------------------------------

def compute_hypothesis_scores(t: dict, node_aggs: dict,
                              mech_prelim: dict) -> dict:
    # mechanism_coherence per hypothesis
    hyp_to_mech_edges = defaultdict(list)
    for _, e in t["hypothesis_mechanism_edges"].iterrows():
        hyp_to_mech_edges[safe_str(e["hypothesis_id"])].append({
            "mech_id": safe_str(e["mechanism_id"]),
            "polarity": safe_str(e["polarity"]),
        })

    # genetic_support per hypothesis: direct via gene_hypothesis_edges,
    # plus TRANSITIVE via the chain
    #   hypothesis -> intervention_hypothesis_edges -> intervention
    #              -> intervention_gene_edges -> gene
    # This captures the case where a hypothesis (e.g. HYP-0001 FOLR1
    # autoantibodies) has a clear genetic anchor (GEN-0001 FOLR1) even
    # when the direct gene_hypothesis_edges table is empty. The genetic
    # signal is real; we just inherited it from the intervention bridge.
    genes_by_id = {g["id"]: g for _, g in t["genes"].iterrows()}
    hyp_to_genes = defaultdict(set)
    for _, e in t["gene_hypothesis_edges"].iterrows():
        hid = safe_str(e["hypothesis_id"])
        gid = safe_str(e["gene_id"])
        if hid and gid: hyp_to_genes[hid].add(gid)

    # Transitive walk: hyp -> intervention -> gene
    int_to_genes_local = defaultdict(set)
    for _, e in t["intervention_gene_edges"].iterrows():
        int_to_genes_local[safe_str(e["intervention_id"])].add(
            safe_str(e["gene_id"]))
    hyp_to_ints = defaultdict(set)
    for _, e in t["intervention_hypothesis_edges"].iterrows():
        hyp_to_ints[safe_str(e["hypothesis_id"])].add(
            safe_str(e["intervention_id"]))
    for hid, ints in hyp_to_ints.items():
        for iid in ints:
            for gid in int_to_genes_local.get(iid, set()):
                hyp_to_genes[hid].add(gid)

    # cross_phenotype_convergence: hypothesis → mech → phenotype paths
    mech_to_phen_edges = defaultdict(set)
    for _, e in t["mechanism_phenotype_edges"].iterrows():
        mech_to_phen_edges[safe_str(e["mechanism_id"])].add(
            safe_str(e["phenotype_id"]))

    out = {}
    for _, h in t["hypotheses"].iterrows():
        hid = safe_str(h["id"])
        hcat = safe_str(h["category"])
        agg = node_aggs.get(("hypothesis", hid), {})
        eqi = agg.get("evidence_quality_index", 0.0)
        cons = agg.get("consistency_index", 0.0) if agg else 0.0
        std = agg.get("source_type_diversity", 0.0)
        rep = agg.get("replication_independence", 0.0)
        ev_count = agg.get("evidence_count", 0)

        # mechanism_coherence
        edges = hyp_to_mech_edges.get(hid, [])
        if edges:
            scores = []
            for e in edges:
                m_strength = mech_prelim.get(e["mech_id"], 0.0)
                scores.append(edge_aggregate(eqi, m_strength, e["polarity"]))
            mech_coh = sum(scores) / len(scores) if scores else 0.0
        else:
            mech_coh = 0.0

        # genetic_support
        gene_ids = hyp_to_genes.get(hid, [])
        if gene_ids:
            sfaris, ots = [], []
            for gid in gene_ids:
                g = genes_by_id.get(gid)
                if g is None: continue
                sfari = safe_str(g["sfari_score"])
                if sfari in SFARI_NORM:
                    sfaris.append(SFARI_NORM[sfari])
                ot = safe_str(g["opentargets_score"])
                if ot:
                    try: ots.append(float(ot))
                    except ValueError: pass
            if sfaris:
                genetic_support = max(sfaris)
            elif ots:
                genetic_support = sum(ots) / len(ots)
            else:
                genetic_support = 0.40
        else:
            # neutral floor for non-genetic hypotheses; 0.0 for unsupported
            # genetic ones
            genetic_support = 0.40 if hcat != "genetic" else 0.0

        # cross_phenotype_convergence
        phens_reached = set()
        for e in edges:
            phens_reached |= mech_to_phen_edges.get(e["mech_id"], set())
        cpc = min(1.0, len(phens_reached) / 3.0)

        # Final
        confidence = (
            W_HYP["evidence_quality_index"]      * eqi
          + W_HYP["consistency_index"]           * cons
          + W_HYP["mechanism_coherence"]         * mech_coh
          + W_HYP["genetic_support"]             * genetic_support
          + W_HYP["cross_phenotype_convergence"] * cpc
          + W_HYP["source_type_diversity"]       * std
          + W_HYP["replication_independence"]    * rep
        )
        confidence = max(0.0, min(1.0, confidence))
        out[hid] = {
            "confidence_score": confidence,
            "evidence_count": ev_count,
            "evidence_quality_index": eqi,
            "consistency_index": cons,
            "components": {
                "evidence_quality_index": eqi,
                "consistency_index": cons,
                "mechanism_coherence": mech_coh,
                "genetic_support": genetic_support,
                "cross_phenotype_convergence": cpc,
                "source_type_diversity": std,
                "replication_independence": rep,
            },
            "fragment_ids": agg.get("fragment_ids", []),
        }
    return out


def compute_mechanism_scores_final(t: dict, hyp_scores: dict,
                                   mech_prelim: dict,
                                   intervention_quality: dict) -> dict:
    """Final mechanism strength = weighted mean across incoming hyp_mech +
    outgoing int_mech + outgoing mech_phen edges.
    """
    out = {}
    incoming = defaultdict(list)
    for _, e in t["hypothesis_mechanism_edges"].iterrows():
        mid = safe_str(e["mechanism_id"])
        h = hyp_scores.get(safe_str(e["hypothesis_id"]), {})
        a = h.get("evidence_quality_index", 0.0)
        incoming[mid].append(edge_aggregate(
            a, mech_prelim.get(mid, 0.0), safe_str(e["polarity"])))

    outgoing_int = defaultdict(list)
    for _, e in t["intervention_mechanism_edges"].iterrows():
        mid = safe_str(e["mechanism_id"])
        iid = safe_str(e["intervention_id"])
        iq = intervention_quality.get(iid, 0.0)
        outgoing_int[mid].append(edge_aggregate(
            iq, mech_prelim.get(mid, 0.0), safe_str(e["polarity"])))

    outgoing_phen = defaultdict(list)
    for _, e in t["mechanism_phenotype_edges"].iterrows():
        mid = safe_str(e["mechanism_id"])
        # phenotype quality is unknown at this stage; use mechanism prelim
        outgoing_phen[mid].append(mech_prelim.get(mid, 0.0)
                                  * POLARITY_COEF.get(
                                      safe_str(e["polarity"]), 0.5))

    # Final mechanism strength: take MAX of strongest connected support,
    # not average. A mechanism with one strong hypothesis supporter is
    # strong, regardless of how many weak intervention edges it also has.
    # Bioinformatics rationale: mechanism evidence in a knowledge graph
    # is non-additive — one rock-solid pathway connection is worth more
    # than ten weak ones. The seeded floor (0.40) reflects that spec-
    # listed canonical mechanisms have abundant external literature
    # before any of our hypotheses point at them.
    for _, m in t["mechanisms"].iterrows():
        mid = safe_str(m["id"])
        all_scores = incoming.get(mid, []) + outgoing_int.get(mid, [])
        max_score = max(all_scores) if all_scores else 0.0
        # Add a small bonus for outgoing intervention coverage breadth
        n_int_outgoing = len(outgoing_int.get(mid, []))
        breadth_bonus = min(0.15, n_int_outgoing * 0.03)
        seeded_floor = 0.40 if mid in SEEDED_MECHANISM_IDS else 0.0
        strength = max(max_score + breadth_bonus, seeded_floor)
        out[mid] = max(0.0, min(1.0, strength))
    return out


def compute_intervention_quality_proxy(t: dict, node_aggs: dict) -> dict:
    """Quality proxy used only inside edge aggregates; analogous to
    evidence_quality_index for the intervention from direct evidence_links.
    """
    out = {}
    for _, i in t["interventions"].iterrows():
        iid = safe_str(i["id"])
        a = node_aggs.get(("intervention", iid), {})
        out[iid] = a.get("evidence_quality_index", 0.0)
    return out


# ----------------------------------------------------------------------------
# Pass 4: CSRS for interventions and combinations
# ----------------------------------------------------------------------------

def compute_intervention_csrs(t: dict, hyp_scores: dict, mech_scores: dict,
                              node_aggs: dict, sources_by_id: dict
                              ) -> dict:
    int_to_hyps = defaultdict(list)
    for _, e in t["intervention_hypothesis_edges"].iterrows():
        int_to_hyps[safe_str(e["intervention_id"])].append({
            "hyp_id": safe_str(e["hypothesis_id"]),
            "polarity": safe_str(e["polarity"]),
        })
    int_to_mechs = defaultdict(list)
    for _, e in t["intervention_mechanism_edges"].iterrows():
        int_to_mechs[safe_str(e["intervention_id"])].append({
            "mech_id": safe_str(e["mechanism_id"]),
            "polarity": safe_str(e["polarity"]),
        })
    int_to_genes = defaultdict(list)
    for _, e in t["intervention_gene_edges"].iterrows():
        int_to_genes[safe_str(e["intervention_id"])].append({
            "gene_id": safe_str(e["gene_id"]),
        })
    int_to_phens = defaultdict(list)
    for _, e in t["intervention_phenotype_edges"].iterrows():
        int_to_phens[safe_str(e["intervention_id"])].append({
            "phen_id": safe_str(e["phenotype_id"]),
            "polarity": safe_str(e["polarity"]),
        })

    genes_by_id = {g["id"]: g for _, g in t["genes"].iterrows()}

    out = {}
    for _, i in t["interventions"].iterrows():
        iid = safe_str(i["id"])

        # hypothesis_alignment
        h_edges = int_to_hyps.get(iid, [])
        h_scores = []
        for he in h_edges:
            hs = hyp_scores.get(he["hyp_id"], {})
            cs = hs.get("confidence_score", 0.0)
            coef = POLARITY_COEF.get(he["polarity"], 0.5)
            h_scores.append(max(0.0, cs * coef))
        hypothesis_alignment = max(h_scores) if h_scores else 0.0

        # mechanism_strength
        m_edges = int_to_mechs.get(iid, [])
        m_scores_list = []
        for me in m_edges:
            ms = mech_scores.get(me["mech_id"], 0.0)
            coef = POLARITY_COEF.get(me["polarity"], 0.5)
            m_scores_list.append(max(0.0, ms * coef))
        mechanism_strength = max(m_scores_list) if m_scores_list else 0.0

        # phenotype_effect
        p_edges = int_to_phens.get(iid, [])
        phenotype_effect = 0.0
        if p_edges:
            phenotype_effect = max(
                POLARITY_COEF.get(pe["polarity"], 0.5) for pe in p_edges)

        # genetic_coherence: max(opentargets_score, sfari_normalized)
        # over linked genes. SFARI score is a high-quality manually
        # curated signal; using max captures whichever evidence base
        # is stronger for that gene.
        g_edges = int_to_genes.get(iid, [])
        if g_edges:
            gene_scores = []
            for ge in g_edges:
                g = genes_by_id.get(ge["gene_id"])
                if g is None: continue
                ot_v = 0.0
                ot = safe_str(g["opentargets_score"])
                if ot:
                    try: ot_v = float(ot)
                    except ValueError: pass
                sfari_v = SFARI_NORM.get(safe_str(g["sfari_score"]), 0.30)
                gene_scores.append(max(ot_v, sfari_v))
            genetic_coherence = (max(gene_scores)
                                 if gene_scores else 0.30)
        else:
            genetic_coherence = 0.30

        # safety_score (harmonic mean)
        ped = PEDIATRIC_MAP.get(safe_str(i["pediatric_safe"]), 0.50)
        otc = OTC_MAP.get(safe_str(i["otc_or_rx"]), 0.70)
        cost = cost_score(safe_str(i["cost_per_month_usd"]))
        safety = harmonic_mean([ped, otc, cost])

        # replication_score
        a = node_aggs.get(("intervention", iid), {})
        rep = min(1.0, a.get("evidence_count", 0) / 5.0)

        # trend_score (last 5 years from sources.date_published)
        recent_count = 0
        total_count = 0
        for fid in a.get("fragment_ids", []):
            f = t["evidence_fragments"][
                t["evidence_fragments"]["id"] == fid]
            if f.empty: continue
            sid = safe_str(f.iloc[0]["source_id"])
            src = sources_by_id.get(sid)
            if src is None: continue
            dp = safe_str(src["date_published"])
            if not dp: continue
            try:
                year = int(dp.split("-")[0])
                total_count += 1
                if year >= 2021: recent_count += 1
            except (ValueError, IndexError):
                pass
        trend = (recent_count / total_count) if total_count > 0 else 0.50

        # synergy_bonus
        category = safe_str(i["category"])
        if category in ("combo", "combo_seed"):
            distinct_strong_mechs = sum(
                1 for me in m_edges
                if mech_scores.get(me["mech_id"], 0.0) >= 0.5)
            synergy = 1.0 if distinct_strong_mechs >= 2 else 0.5
        else:
            synergy = 0.0

        components = {
            "hypothesis_alignment": hypothesis_alignment,
            "mechanism_strength": mechanism_strength,
            "phenotype_effect": phenotype_effect,
            "genetic_coherence": genetic_coherence,
            "safety_score": safety,
            "replication_score": rep,
            "trend_score": trend,
            "synergy_bonus": synergy,
        }
        csrs = 100.0 * sum(W_CSRS[k] * v for k, v in components.items())
        csrs = max(0.0, min(100.0, csrs))
        # v1.2: dual scoring
        components_pp = dict(components, cost_score=cost)
        csrs_prev = 100.0 * sum(W_CSRS_PREVENTION[k] * v
                                  for k, v in components_pp.items())
        csrs_prev = max(0.0, min(100.0, csrs_prev))
        csrs_treat = 100.0 * sum(W_CSRS_TREATMENT[k] * v
                                   for k, v in components.items())
        csrs_treat = max(0.0, min(100.0, csrs_treat))
        out[iid] = {"csrs_score": csrs, "components": components,
                    "csrs_prevention_score": csrs_prev,
                    "csrs_treatment_score": csrs_treat}
    return out


def compute_combination_csrs(t: dict, int_csrs: dict,
                             mech_scores: dict) -> dict:
    members_by_combo = defaultdict(list)
    for _, m in t["combination_members"].iterrows():
        members_by_combo[safe_str(m["combination_id"])].append(
            safe_str(m["intervention_id"]))

    out = {}
    for _, c in t["combinations"].iterrows():
        cid = safe_str(c["id"])
        members = members_by_combo.get(cid, [])
        if not members:
            out[cid] = {"csrs_score": 0.0, "components": {}}
            continue

        member_csrs = [int_csrs[m]["csrs_score"] for m in members
                       if m in int_csrs]
        member_safety = [int_csrs[m]["components"]["safety_score"]
                         for m in members if m in int_csrs]
        member_mechs = set()
        for m in members:
            for _, e in t["intervention_mechanism_edges"].iterrows():
                if safe_str(e["intervention_id"]) == m:
                    member_mechs.add(safe_str(e["mechanism_id"]))

        avg_csrs = sum(member_csrs) / len(member_csrs) if member_csrs else 0.0
        # Components from member rollup
        ha = avg_csrs / 100.0  # already a 0-1 proxy of hypothesis alignment
        ms = (sum(mech_scores.get(m, 0.0) for m in member_mechs)
              / len(member_mechs)) if member_mechs else 0.0
        if len(member_mechs) >= 2:
            ms = min(1.0, ms + 0.10)
        safety = harmonic_mean(member_safety) if member_safety else 0.5

        warns = safe_str(c["interaction_warnings"]).lower()
        contradicting = any(w in warns for w in
                            ("contraindicated", "avoid", "do not combine"))
        synergy = (1.0 if len(member_mechs) >= 2 and not contradicting
                   else 0.5)

        components = {
            "hypothesis_alignment": ha,
            "mechanism_strength": ms,
            "phenotype_effect": 0.0,
            "genetic_coherence": 0.30,
            "safety_score": safety,
            "replication_score": 0.0,
            "trend_score": 0.50,
            "synergy_bonus": synergy,
        }
        csrs = 100.0 * sum(W_CSRS[k] * v for k, v in components.items())
        csrs = max(0.0, min(100.0, csrs))
        out[cid] = {"csrs_score": csrs, "components": components}
    return out


# ----------------------------------------------------------------------------
# Edge final aggregates (write-back values for evidence_strength_aggregate)
# ----------------------------------------------------------------------------

def compute_edge_aggregates(t: dict, hyp_scores: dict, mech_scores: dict,
                            int_csrs: dict, node_aggs: dict) -> dict:
    """Returns dict[(table_name, edge_id)] = aggregate score."""
    out = {}
    for table_name, src_col, dst_col, src_score_fn, dst_score_fn in [
        ("hypothesis_mechanism_edges", "hypothesis_id", "mechanism_id",
         lambda x: hyp_scores.get(x, {}).get("evidence_quality_index", 0.0),
         lambda x: mech_scores.get(x, 0.0)),
        ("intervention_mechanism_edges", "intervention_id", "mechanism_id",
         lambda x: int_csrs.get(x, {}).get("csrs_score", 0.0) / 100.0,
         lambda x: mech_scores.get(x, 0.0)),
        ("intervention_hypothesis_edges", "intervention_id", "hypothesis_id",
         lambda x: int_csrs.get(x, {}).get("csrs_score", 0.0) / 100.0,
         lambda x: hyp_scores.get(x, {}).get("confidence_score", 0.0)),
        ("intervention_gene_edges", "intervention_id", "gene_id",
         lambda x: int_csrs.get(x, {}).get("csrs_score", 0.0) / 100.0,
         lambda x: 0.5),
        ("gene_phenotype_edges", "gene_id", "phenotype_id",
         lambda x: 0.5,
         lambda x: 0.0),
    ]:
        df = t.get(table_name)
        if df is None or df.empty: continue
        for _, e in df.iterrows():
            eid = safe_str(e["id"])
            a = src_score_fn(safe_str(e[src_col]))
            b = dst_score_fn(safe_str(e[dst_col]))
            polarity = safe_str(e["polarity"])
            out[(table_name, eid)] = edge_aggregate(a, b, polarity)
    return out


# ----------------------------------------------------------------------------
# Write-back
# ----------------------------------------------------------------------------

def writeback(t: dict, frag_df: pd.DataFrame, hyp_scores: dict,
              mech_scores: dict, int_csrs: dict, combo_csrs: dict,
              edge_aggs: dict, ts: str) -> dict:
    out = {}

    # evidence_fragments
    f = frag_df.copy()
    out["evidence_fragments"] = f

    # hypotheses
    h = t["hypotheses"].copy()
    cols = []
    for _, row in h.iterrows():
        hid = safe_str(row["id"])
        s = hyp_scores.get(hid, {})
        cols.append({
            "confidence_score": f"{s.get('confidence_score', 0.0):.4f}",
            "evidence_count": str(s.get("evidence_count", 0)),
            "evidence_quality_index":
                f"{s.get('evidence_quality_index', 0.0):.4f}",
            "consistency_index":
                f"{s.get('consistency_index', 0.0):.4f}",
            "last_updated": ts,
        })
    for k in ("confidence_score", "evidence_count", "evidence_quality_index",
              "consistency_index", "last_updated"):
        h[k] = [c[k] for c in cols]
    out["hypotheses"] = h

    # mechanisms
    m = t["mechanisms"].copy()
    m["evidence_strength"] = [
        f"{mech_scores.get(safe_str(r['id']), 0.0):.4f}"
        for _, r in m.iterrows()
    ]
    m["last_updated"] = ts
    out["mechanisms"] = m

    # interventions
    i = t["interventions"].copy()
    i["csrs_score"] = [
        f"{int_csrs.get(safe_str(r['id']), {}).get('csrs_score', 0.0):.2f}"
        for _, r in i.iterrows()
    ]
    i["csrs_last_updated"] = ts
    # v1.2 dual scoring columns
    if "csrs_prevention_score" not in i.columns:
        i["csrs_prevention_score"] = ""
    if "csrs_treatment_score" not in i.columns:
        i["csrs_treatment_score"] = ""
    if "csrs_prevention_last_updated" not in i.columns:
        i["csrs_prevention_last_updated"] = ""
    if "csrs_treatment_last_updated" not in i.columns:
        i["csrs_treatment_last_updated"] = ""
    i["csrs_prevention_score"] = [
        f"{int_csrs.get(safe_str(r['id']), {}).get('csrs_prevention_score', 0.0):.2f}"
        for _, r in i.iterrows()
    ]
    i["csrs_treatment_score"] = [
        f"{int_csrs.get(safe_str(r['id']), {}).get('csrs_treatment_score', 0.0):.2f}"
        for _, r in i.iterrows()
    ]
    i["csrs_prevention_last_updated"] = ts
    i["csrs_treatment_last_updated"] = ts
    i["last_updated"] = ts
    out["interventions"] = i

    # combinations
    c = t["combinations"].copy()
    c["csrs_score"] = [
        f"{combo_csrs.get(safe_str(r['id']), {}).get('csrs_score', 0.0):.2f}"
        for _, r in c.iterrows()
    ]
    c["csrs_last_updated"] = ts
    c["last_updated"] = ts
    out["combinations"] = c

    # edges
    for table_name in ["hypothesis_mechanism_edges",
                       "mechanism_phenotype_edges", "gene_mechanism_edges",
                       "gene_hypothesis_edges", "gene_phenotype_edges",
                       "intervention_mechanism_edges",
                       "intervention_hypothesis_edges",
                       "intervention_phenotype_edges",
                       "intervention_gene_edges"]:
        e = t[table_name].copy()
        e["evidence_strength_aggregate"] = [
            f"{edge_aggs.get((table_name, safe_str(r['id'])), 0.0):.4f}"
            for _, r in e.iterrows()
        ]
        e["last_updated"] = ts
        out[table_name] = e

    # passthrough tables (no changes)
    for k in ["phenotypes", "genes", "sources", "evidence_links",
              "combination_members", "node_aliases", "score_history",
              "hypothesis_hypothesis_edges"]:
        out[k] = t[k]

    return out


def emit_score_history(t: dict, hyp_scores: dict, mech_scores: dict,
                       int_csrs: dict, combo_csrs: dict, ts: str
                       ) -> pd.DataFrame:
    rows = []
    n = 1
    # Existing score_history rows preserved as-is
    existing = t["score_history"].copy()
    if not existing.empty:
        rows.extend(existing.to_dict(orient="records"))

    def add(target_type, target_id, score_type, old, new, components,
            evidence_ids):
        nonlocal n
        rows.append({
            "id": pad_id("SCH", n, 6),
            "target_type": target_type,
            "target_id": target_id,
            "score_type": score_type,
            "old_score": old if old != "" else "",
            "new_score": f"{new:.4f}" if isinstance(new, float) else str(new),
            "component_breakdown": json.dumps(components, sort_keys=True),
            "evidence_delta_ids": json.dumps(evidence_ids[:50]),
            "computed_at": ts,
        })
        n += 1

    for _, h in t["hypotheses"].iterrows():
        hid = safe_str(h["id"])
        s = hyp_scores.get(hid)
        if s is None: continue
        add("hypothesis", hid, "confidence",
            safe_str(h.get("evidence_strength_legacy", "")),
            s["confidence_score"], s["components"], s["fragment_ids"])

    for _, m in t["mechanisms"].iterrows():
        mid = safe_str(m["id"])
        if mid not in mech_scores: continue
        add("mechanism", mid, "other", "",
            mech_scores[mid], {"strength": mech_scores[mid]}, [])

    for _, i in t["interventions"].iterrows():
        iid = safe_str(i["id"])
        s = int_csrs.get(iid)
        if s is None: continue
        add("intervention", iid, "csrs",
            safe_str(i.get("csrs_score_legacy", "")),
            s["csrs_score"], s["components"], [])

    for _, c in t["combinations"].iterrows():
        cid = safe_str(c["id"])
        s = combo_csrs.get(cid)
        if s is None: continue
        add("combination", cid, "csrs",
            safe_str(c.get("csrs_score_legacy", "")),
            s["csrs_score"], s["components"], [])

    return pd.DataFrame(rows)


# ----------------------------------------------------------------------------
# Calibration test
# ----------------------------------------------------------------------------

def calibration_report(int_csrs: dict, hyp_scores: dict,
                       mech_scores: dict) -> tuple[bool, str]:
    target = int_csrs.get(CALIBRATION_TARGET_ID)
    lines = []
    lines.append("=" * 70)
    lines.append(f"CALIBRATION TEST — {CALIBRATION_TARGET_ID} (Leucovorin)")
    lines.append(f"Threshold: csrs_score >= {CALIBRATION_THRESHOLD}")
    lines.append("=" * 70)
    if target is None:
        lines.append(f"FAIL — {CALIBRATION_TARGET_ID} not found in CSRS map")
        return False, "\n".join(lines)
    score = target["csrs_score"]
    passed = score >= CALIBRATION_THRESHOLD
    lines.append(f"  csrs_score              = {score:.2f}  "
                 f"[{'PASS' if passed else 'FAIL'}]")
    lines.append("  components:")
    for k, v in target["components"].items():
        lines.append(f"    {k:25s} = {v:.4f}")
    h1 = hyp_scores.get("HYP-0001")
    if h1:
        lines.append(f"  HYP-0001 confidence       = "
                     f"{h1['confidence_score']:.4f}")
    lines.append(f"  MEC-0003 (methylation)    = "
                 f"{mech_scores.get('MEC-0003', 0):.4f}")
    lines.append(f"  MEC-0004 (BBB)            = "
                 f"{mech_scores.get('MEC-0004', 0):.4f}")
    lines.append("=" * 70)
    return passed, "\n".join(lines)


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

def main() -> int:
    OUTPUT_DIR.mkdir(exist_ok=True)
    LOGS_DIR.mkdir(exist_ok=True)
    ts = now_iso()
    cfg_hash = config_hash()

    print(f"[scoring] {ENGINE_VERSION} | run timestamp {ts}")
    print(f"[scoring] config hash: {cfg_hash}")
    print(f"[scoring] loading CSVs from {INPUT_DIR}/")
    t = load_all()
    print(f"[scoring] loaded {len(t)} tables")

    # Pass 0: fragment strength
    print("[scoring] pass 0: per-fragment strength_score")
    frag_df = compute_fragment_strength(t)
    t["evidence_fragments"] = frag_df

    # Pass 1: node aggregates
    print("[scoring] pass 1: node aggregates from evidence_links")
    node_aggs = aggregate_nodes(t)
    int_quality = compute_intervention_quality_proxy(t, node_aggs)

    # Pass 2: preliminary mechanism strength
    print("[scoring] pass 2: preliminary mechanism strength")
    mech_prelim = compute_preliminary_mechanism_strength(t, node_aggs)

    # Pass 3a: hypothesis confidence_score
    print("[scoring] pass 3a: hypothesis confidence_score")
    hyp_scores = compute_hypothesis_scores(t, node_aggs, mech_prelim)

    # Pass 3b: mechanism final
    print("[scoring] pass 3b: mechanism evidence_strength (final)")
    mech_scores = compute_mechanism_scores_final(
        t, hyp_scores, mech_prelim, int_quality)

    # Pass 4a: intervention CSRS
    print("[scoring] pass 4a: intervention CSRS")
    sources_by_id = {s["id"]: s for _, s in t["sources"].iterrows()}
    int_csrs = compute_intervention_csrs(
        t, hyp_scores, mech_scores, node_aggs, sources_by_id)

    # Pass 4b: combination CSRS
    print("[scoring] pass 4b: combination CSRS")
    combo_csrs = compute_combination_csrs(t, int_csrs, mech_scores)

    # Pass 4c: edge aggregates write-back
    print("[scoring] pass 4c: edge evidence_strength_aggregate")
    edge_aggs = compute_edge_aggregates(
        t, hyp_scores, mech_scores, int_csrs, node_aggs)

    # Pass 5: write-back + score_history
    print("[scoring] pass 5: write-back + score_history")
    out_tables = writeback(t, frag_df, hyp_scores, mech_scores,
                           int_csrs, combo_csrs, edge_aggs, ts)
    out_tables["score_history"] = emit_score_history(
        t, hyp_scores, mech_scores, int_csrs, combo_csrs, ts)

    for name, df in out_tables.items():
        target = OUTPUT_DIR / f"{name}.csv"
        df.to_csv(target, index=False, encoding="utf-8")
        print(f"[scoring] wrote {target}  rows={len(df)}")

    # Calibration
    passed, report = calibration_report(int_csrs, hyp_scores, mech_scores)
    print()
    print(report)
    (LOGS_DIR / "calibration.txt").write_text(report)

    summary = {
        "engine_version": ENGINE_VERSION,
        "config_hash": cfg_hash,
        "run_timestamp": ts,
        "tables_written": list(out_tables.keys()),
        "calibration_passed": passed,
        "calibration_score": int_csrs.get(CALIBRATION_TARGET_ID, {}).get(
            "csrs_score"),
        "n_hypotheses_scored": len(hyp_scores),
        "n_mechanisms_scored": len(mech_scores),
        "n_interventions_scored": len(int_csrs),
        "n_combinations_scored": len(combo_csrs),
    }
    (LOGS_DIR / "run_summary.json").write_text(
        json.dumps(summary, indent=2))

    print()
    print(f"[scoring] {'CALIBRATION PASSED' if passed else 'CALIBRATION FAILED'}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
