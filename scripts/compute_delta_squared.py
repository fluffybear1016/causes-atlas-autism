#!/usr/bin/env python3
"""
compute_delta_squared.py — Δ² (second-derivative) prioritization overlay
for the Causes Atlas (Autism). Production version, integrated into the
canonical scoring pipeline via apply_patches_and_score.py.

Per CLAUDE.md: deterministic, no LLM calls, stable sort by ID, idempotent.
This is a PRIORITIZATION layer ON TOP OF the CSRS scoring engine, not a
replacement.

Δ² components (deterministic, computable from current v2.0_scored data):

  C1  Recency acceleration       — second derivative of sources-per-year
  C2  Cross-design convergence Δ — change in distinct study_design diversity
  C3  Subset-validation signal   — recency-weighted subpopulation_signal hits
  C4  Replication independence   — distinct-source count, capped + log-shaped
  C5  Trajectory-mismatch flag   — contested status + tier-1 primary records

Outputs (in delta_squared_v1/):
  rankings.csv             — ranked entity table (overwritten each run)
  components.csv           — per-component scores (overwritten each run)
  run_summary.json         — engine version, weights, windows, calibration result
  score_history.csv        — append-only timestamped history
  anomaly_flags.csv        — append-only single-source-dominance flags
  calibration_status.txt   — human-readable PASS/FAIL of all anchors
  data_gaps.csv            — entities with zero sources (gap detection)

Calibration anchors — these MUST pass or the script exits non-zero,
halting the pipeline. Mirrors CSRS's INT-0001 ≥ 80 discipline.

Sliding windows — all year windows computed from CURRENT_YEAR at runtime,
so the framework auto-rolls forward each January 1.
"""

from __future__ import annotations
import csv, json, math, os, sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
import pathlib

# --------------------------------------------------------------------------
# Paths
# --------------------------------------------------------------------------

REPO       = pathlib.Path(__file__).resolve().parent.parent
ATLAS_DIR  = REPO / "v2.0_scored"
OUTPUT_DIR = REPO / "delta_squared_v1"

# --------------------------------------------------------------------------
# Sliding windows — auto-roll on calendar
# --------------------------------------------------------------------------

CURRENT_YEAR  = datetime.now(timezone.utc).year
RECENT_WINDOW = tuple(range(CURRENT_YEAR - 3, CURRENT_YEAR + 1))   # 4-year recent
PRIOR_WINDOW  = tuple(range(CURRENT_YEAR - 7, CURRENT_YEAR - 3))   # 4-year prior
DEEP_WINDOW   = tuple(range(CURRENT_YEAR - 12, CURRENT_YEAR - 7))  # 5-year deep

# --------------------------------------------------------------------------
# Component weights (sum to 1.0)
# --------------------------------------------------------------------------

W_C1 = 0.30   # recency acceleration
W_C2 = 0.20   # cross-design convergence
W_C3 = 0.25   # subset-validation
W_C4 = 0.10   # replication independence
W_C5 = 0.15   # trajectory mismatch

assert abs(W_C1 + W_C2 + W_C3 + W_C4 + W_C5 - 1.0) < 1e-9

# --------------------------------------------------------------------------
# Study-design tier weights (mirrors W_DESIGN intent in scoring engine —
# CROSS-CHECK on every release; see test_delta_squared_determinism.py).
# --------------------------------------------------------------------------

DESIGN_TIER = {
    "meta_analysis":               1.00,
    "rct":                         1.00,
    "natural_experiment":          0.95,
    "federal_court_ruling":        0.95,
    "mendelian_randomization":     0.85,
    "multiomics_replication":      0.75,
    "cohort":                      0.70,
    "multiomics_observational":    0.70,
    "multiomics_genomics":         0.70,
    "multiomics_microbial_genomics": 0.70,
    "case_control":                0.65,
    "phase_1":                     0.55,
    "regulatory_document":         0.55,
    "mechanistic":                 0.50,
    "preprint":                    0.45,
    "internal_meeting_transcript": 0.45,
    "case_series":                 0.40,
    "internal_correspondence":     0.40,
    "whistleblower_statement":     0.40,
    "advisory_committee_review":   0.40,
    "animal":                      0.40,
    "systems_biology_methodology": 0.40,
    "ecological":                  0.35,
    "preliminary_analysis":        0.30,
    "review":                      0.30,
    "literature_mining_synthesis": 0.30,
    "methodology_critique":        0.30,
    "theoretical_review":          0.25,
    "hypothesis_paper":            0.25,
    "other":                       0.20,
    "":                            0.15,
    "editorial":                   0.10,
    "letter":                      0.10,
    "comment":                     0.10,
    "news":                        0.05,
}

TIER1_PRIMARY = {
    "federal_court_ruling",
    "internal_meeting_transcript",
    "internal_correspondence",
    "whistleblower_statement",
    "regulatory_document",
    "advisory_committee_review",
    "preliminary_analysis",
}

# --------------------------------------------------------------------------
# Calibration anchors — regression tests. Tightened with margin from
# current run so legitimate evolution doesn't false-fail; hard regressions
# halt the pipeline.
# --------------------------------------------------------------------------

CALIBRATION_ANCHORS = [
    # (entity_id, check_name, min_value, what_it_protects)
    ("INT-0001", "score",   30.0, "Leucovorin / FOLR1+ subset-validation signal must hold"),
    ("MEC-0010", "score",   50.0, "Mitochondrial dysfunction cross-design convergence must hold"),
    ("HYP-0028", "c2",       0.85, "Polygenic risk maximum design diversity must hold"),
    ("HYP-0001", "c3",       0.55, "FOLR1 autoantibodies subset-stratification signal must hold"),
    ("HYP-0044", "c5",       1.00, "Childhood vaccine exposure trajectory-mismatch must hold"),
    ("HYP-0066", "c5",       1.00, "Hep B birth-dose trajectory-mismatch must hold"),
    ("HYP-0067", "c5",       1.00, "Aluminum adjuvant trajectory-mismatch must hold"),
    ("HYP-0068", "c5",       1.00, "MMR trajectory-mismatch must hold"),
    ("HYP-0069", "c5",       1.00, "Thimerosal trajectory-mismatch must hold"),
]

# Single-source dominance threshold — if any one source contributes more
# than this fraction of an entity's recent-window weight, flag for review
# (defends against Hassan-2025-style single-study spike inflation).
ANOMALY_DOMINANCE_THRESHOLD = 0.30

# Data-gap entities — soft warning, not hard fail. PANS/PANDAS specifically
# is the flagship gap from the v1.0 findings report; we want a loud warning
# until it gets ingested.
DATA_GAP_WATCHLIST = ["HYP-0026"]   # PANDAS/PANS

# Reflexivity audit — code-enforced anti-reflexivity defense. If ingestion
# between Δ² runs preferentially fed already-high-ranked entities, the
# trajectory will look more accelerated next run because the curator fed
# it, not because the field accelerated. The audit detects this via rank
# correlation between previous-run rank and inter-run new-source count.
#
# Thresholds:
#   N < REFLEXIVITY_MIN_N entities receiving new sources -> insufficient data
#   N >= MIN_N AND |spearman_r| >= REFLEXIVITY_FAIL_THRESHOLD -> HARD FAIL
#   N >= MIN_N AND |spearman_r| >= REFLEXIVITY_WARN_THRESHOLD -> WARN
#   else -> PASS
REFLEXIVITY_MIN_N = 5
REFLEXIVITY_WARN_THRESHOLD = 0.30
REFLEXIVITY_FAIL_THRESHOLD = 0.70

# --------------------------------------------------------------------------
# Loaders
# --------------------------------------------------------------------------

def load_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def parse_year(date_str):
    if not date_str: return None
    try: return int(date_str[:4])
    except ValueError: return None

def parse_payload(s):
    if not s: return {}
    try: return json.loads(s)
    except Exception: return {}

# --------------------------------------------------------------------------
# Index build
# --------------------------------------------------------------------------

def build_entity_index(atlas_dir):
    src_rows = load_csv(atlas_dir / "sources.csv")
    sources = {r["id"]: {
        "year":     parse_year(r["date_published"]),
        "design":   (r["study_design"] or "").strip(),
        "n":        (int(r["sample_size"]) if r["sample_size"].isdigit() else None),
        "ingested": (r.get("date_ingested") or "").strip(),
    } for r in src_rows}

    frag_rows = load_csv(atlas_dir / "evidence_fragments.csv")
    fragments = {r["id"]: {
        "source_id": r["source_id"],
        "payload":   parse_payload(r.get("structured_payload","")),
        "text":      r.get("text_excerpt","") or "",
    } for r in frag_rows}

    link_rows = load_csv(atlas_dir / "evidence_links.csv")
    links = [(r["target_type"], r["target_id"], r["evidence_fragment_id"])
             for r in link_rows]

    hyp = {r["id"]: r for r in load_csv(atlas_dir / "hypotheses.csv")}
    itv = {r["id"]: r for r in load_csv(atlas_dir / "interventions.csv")}
    mec = {r["id"]: r for r in load_csv(atlas_dir / "mechanisms.csv")}
    return sources, fragments, links, hyp, itv, mec

def gather_evidence_per_entity(sources, fragments, links):
    entity_evidence = defaultdict(dict)
    for ttype, tid, fid in links:
        frag = fragments.get(fid)
        if not frag: continue
        sid = frag["source_id"]
        src = sources.get(sid)
        if not src: continue
        rec = {"source_id": sid, "year": src["year"], "design": src["design"],
               "payload": frag["payload"], "text": frag["text"]}
        entity_evidence[(ttype, tid)].setdefault(sid, rec)
    return {k: sorted(v.values(), key=lambda r: r["source_id"])
            for k, v in entity_evidence.items()}

# --------------------------------------------------------------------------
# Components
# --------------------------------------------------------------------------

def c1_recency_acceleration(records):
    by_year = Counter()
    for r in records:
        if r["year"]:
            by_year[r["year"]] += 1
    rate_recent = sum(by_year[y] for y in RECENT_WINDOW) / len(RECENT_WINDOW)
    rate_prior  = sum(by_year[y] for y in PRIOR_WINDOW)  / len(PRIOR_WINDOW)
    rate_deep   = sum(by_year[y] for y in DEEP_WINDOW)   / len(DEEP_WINDOW)
    delta2 = rate_recent - 2 * rate_prior + rate_deep
    denom  = max(rate_recent + rate_prior + rate_deep, 1.0)
    raw    = delta2 / denom
    if raw <= 0: return 0.0
    return min(1.0, raw * 1.5)

def c2_cross_design_convergence(records):
    def diversity(window_set):
        designs = set()
        for r in records:
            if r["year"] and r["year"] in window_set:
                designs.add(r["design"] or "")
        return sum(DESIGN_TIER.get(d, 0.15) for d in designs)
    delta = diversity(set(RECENT_WINDOW)) - diversity(set(PRIOR_WINDOW))
    if delta <= 0: return 0.0
    return min(1.0, delta / 2.5)

SUBSET_KEYWORDS = (
    "subgroup", "stratif", "responder", "non-responder", "subpopulation",
    "subset", "folr1", "high-baseline", "low-baseline", "high baseline",
    "low baseline", "high tone", "low tone", "tier 1", "tier 2",
    "phenotype-specific", "biomarker-positive", "biomarker positive",
    "antibody-positive", "panda", "pans", "mcas", "mito-vulnerable",
    "mitochondrial-vulnerable",
)

def c3_subset_validation(records):
    weight = 0.0
    for r in records:
        text = r["text"].lower()
        pld  = r["payload"]
        if not (pld.get("subpopulation_signal") or
                any(kw in text for kw in SUBSET_KEYWORDS)):
            continue
        y = r["year"] or 0
        if y >= CURRENT_YEAR - 3: mult = 1.0
        elif y >= CURRENT_YEAR - 7: mult = 0.6
        elif y >= CURRENT_YEAR - 12: mult = 0.3
        elif y > 0: mult = 0.1
        else: mult = 0.2
        if pld.get("primary"): mult *= 1.25
        weight += mult
    return min(1.0, weight / 5.0)

def c4_replication_independence(records):
    n = len({r["source_id"] for r in records})
    if n == 0: return 0.0
    return min(1.0, math.log1p(n) / math.log(25))

def c5_trajectory_mismatch(records, status):
    is_contested = (status == "contested")
    has_primary  = any(r["design"] in TIER1_PRIMARY for r in records)
    if is_contested and has_primary: return 1.0
    if has_primary: return 0.5
    if is_contested: return 0.3
    return 0.0

# --------------------------------------------------------------------------
# Anomaly detection — single-source dominance in recent window
# --------------------------------------------------------------------------

def detect_dominance_anomaly(records):
    """Return (top_source_id, fraction) if any one source's tier-weighted
    contribution to the recent window exceeds ANOMALY_DOMINANCE_THRESHOLD;
    else (None, 0.0). Defends against single-study spikes (e.g. Hassan-2025).
    """
    contrib = Counter()
    for r in records:
        if r["year"] and r["year"] in RECENT_WINDOW:
            w = DESIGN_TIER.get(r["design"], 0.15)
            contrib[r["source_id"]] += w
    total = sum(contrib.values())
    if total == 0: return (None, 0.0)
    top_src, top_w = contrib.most_common(1)[0]
    frac = top_w / total
    if frac >= ANOMALY_DOMINANCE_THRESHOLD and len(contrib) >= 2:
        return (top_src, frac)
    return (None, 0.0)

# --------------------------------------------------------------------------
# Reflexivity audit — code-enforced anti-reflexivity defense
# --------------------------------------------------------------------------

def _parse_iso_ts(s):
    """Parse ISO timestamp; return None on failure. Tolerant of timezone
    suffixes ('+00:00', 'Z') and missing-time formats."""
    if not s: return None
    s = s.strip().replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(s)
    except ValueError:
        # Date only
        try: return datetime.fromisoformat(s + "T00:00:00+00:00")
        except ValueError: return None

def _spearman(xs, ys):
    """Rank-based Pearson on tied-rank-averaged ranks. Deterministic.
    Returns 0.0 on degenerate input (constant series, len < 2)."""
    n = len(xs)
    if n < 2: return 0.0
    def rank(vals):
        idx = sorted(range(n), key=lambda i: vals[i])
        ranks = [0.0] * n
        i = 0
        while i < n:
            j = i
            while j + 1 < n and vals[idx[j+1]] == vals[idx[i]]:
                j += 1
            avg = (i + j) / 2.0 + 1.0
            for k in range(i, j+1):
                ranks[idx[k]] = avg
            i = j + 1
        return ranks
    rx, ry = rank(xs), rank(ys)
    mx, my = sum(rx)/n, sum(ry)/n
    num = sum((rx[i]-mx)*(ry[i]-my) for i in range(n))
    dx2 = sum((rx[i]-mx)**2 for i in range(n))
    dy2 = sum((ry[i]-my)**2 for i in range(n))
    if dx2 == 0 or dy2 == 0: return 0.0
    return num / math.sqrt(dx2 * dy2)

def audit_reflexivity(sources_meta, evidence, history_path, current_run_ts):
    """Detect curator-driven reflexive feedback into Δ² rankings.

    Reads score_history.csv to find previous run timestamp; for sources
    ingested AFTER that timestamp, maps them to entities and computes
    Spearman rank correlation between previous-run rank and inter-run
    new-source count. High positive correlation = the curator fed
    already-ranked entities, which is the reflexivity failure mode.

    Returns dict: {status, message, spearman_r, n_entities,
                   n_new_sources, prev_run_ts, top_5_fed}
    """
    out = {
        "status": "first_run",
        "message": "no prior Δ² run in history; reflexivity check inactive",
        "spearman_r": 0.0,
        "n_entities": 0,
        "n_new_sources": 0,
        "prev_run_ts": None,
        "top_5_fed": [],
    }

    if not history_path.exists():
        return out

    # Find previous run timestamp + per-entity rank from history
    prev_run_ts = None
    prev_run_scores = {}      # (type,id) -> score from prev run
    timestamps_seen = set()
    with open(history_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        timestamps_seen.add(r["run_timestamp"])
    # Find the most recent run timestamp STRICTLY before current run
    candidates = sorted(t for t in timestamps_seen if t < current_run_ts)
    if not candidates:
        return out
    prev_run_ts = candidates[-1]
    out["prev_run_ts"] = prev_run_ts
    for r in rows:
        if r["run_timestamp"] == prev_run_ts:
            prev_run_scores[(r["entity_type"], r["entity_id"])] = float(r["delta_squared_score"])

    if not prev_run_scores:
        out["status"] = "no_prev_data"
        out["message"] = f"prev run {prev_run_ts} found but no rows; aborting audit"
        return out

    # Compute previous-run rank: 1 = highest score; ties resolved by entity_id
    ranked = sorted(prev_run_scores.items(),
                    key=lambda kv: (-kv[1], kv[0][1]))
    prev_rank = {k: i+1 for i, (k, _s) in enumerate(ranked)}

    # Identify sources ingested after prev_run_ts
    prev_dt = _parse_iso_ts(prev_run_ts)
    if prev_dt is None:
        out["status"] = "parse_error"
        out["message"] = "couldn't parse prev_run_ts"
        return out
    new_source_ids = set()
    for sid, meta in sources_meta.items():
        ing_dt = _parse_iso_ts(meta.get("ingested",""))
        if ing_dt and ing_dt > prev_dt:
            new_source_ids.add(sid)
    out["n_new_sources"] = len(new_source_ids)

    # Map new sources to entities via evidence dict
    new_per_entity = Counter()
    for (etype, eid), recs in evidence.items():
        c = sum(1 for r in recs if r["source_id"] in new_source_ids)
        if c > 0: new_per_entity[(etype, eid)] = c

    out["n_entities"] = len(new_per_entity)

    if len(new_per_entity) < REFLEXIVITY_MIN_N:
        out["status"] = "insufficient_data"
        out["message"] = (f"{len(new_per_entity)} entities received new sources "
                          f"since prev run {prev_run_ts}; need >= {REFLEXIVITY_MIN_N} "
                          "for reflexivity test")
        # still expose the top-fed list even if test inactive
        for (k, v) in new_per_entity.most_common(5):
            out["top_5_fed"].append({
                "entity_type": k[0], "entity_id": k[1],
                "new_sources": v, "prev_rank": prev_rank.get(k, None),
            })
        return out

    # Compute Spearman: x = previous rank (lower = higher Δ²), y = new sources
    xs, ys = [], []
    for k, c in new_per_entity.items():
        if k in prev_rank:
            xs.append(prev_rank[k])
            ys.append(c)
    # Negate xs so that "high rank" (rank=1, top) -> high x, making the
    # natural sign: positive r = curator fed top-ranked entities.
    xs_signed = [-x for x in xs]
    r = _spearman(xs_signed, ys)
    out["spearman_r"] = round(r, 4)

    if r >= REFLEXIVITY_FAIL_THRESHOLD:
        out["status"] = "FAIL"
        out["message"] = (f"REFLEXIVITY DETECTED: Spearman r={r:.3f} >= "
                          f"{REFLEXIVITY_FAIL_THRESHOLD}. Curator preferentially "
                          f"fed {len(new_per_entity)} previously-top-ranked entities. "
                          "Pipeline halted. Either rebalance ingestion or override "
                          "by raising REFLEXIVITY_FAIL_THRESHOLD with documented "
                          "justification.")
    elif r >= REFLEXIVITY_WARN_THRESHOLD:
        out["status"] = "WARN"
        out["message"] = (f"reflexivity warning: Spearman r={r:.3f} >= "
                          f"{REFLEXIVITY_WARN_THRESHOLD}. Inter-run ingestion shows "
                          "moderate correlation with prior rank. Review which "
                          "entities received sources and confirm allocation was "
                          "driven by external literature volume or coverage gaps, "
                          "not by Δ² rank.")
    else:
        out["status"] = "PASS"
        out["message"] = (f"reflexivity check passed: Spearman r={r:.3f} < "
                          f"{REFLEXIVITY_WARN_THRESHOLD} across {len(new_per_entity)} "
                          "entities receiving new sources")

    # Top 5 fed entities
    for (k, v) in new_per_entity.most_common(5):
        out["top_5_fed"].append({
            "entity_type": k[0], "entity_id": k[1],
            "new_sources": v, "prev_rank": prev_rank.get(k, None),
        })
    return out

# --------------------------------------------------------------------------
# Driver
# --------------------------------------------------------------------------

def score_entity(records, status):
    c1 = c1_recency_acceleration(records)
    c2 = c2_cross_design_convergence(records)
    c3 = c3_subset_validation(records)
    c4 = c4_replication_independence(records)
    c5 = c5_trajectory_mismatch(records, status)
    score = 100.0 * (W_C1*c1 + W_C2*c2 + W_C3*c3 + W_C4*c4 + W_C5*c5)
    return score, (c1, c2, c3, c4, c5)

def check_calibration(component_rows):
    """Returns (passed: bool, results: list of (anchor_id, check, expected,
    actual, status)). Mirrors CSRS calibration discipline."""
    by_id = {r["entity_id"]: r for r in component_rows}
    results = []
    for entity_id, check, threshold, _why in CALIBRATION_ANCHORS:
        row = by_id.get(entity_id)
        if row is None:
            results.append((entity_id, check, threshold, None, "MISSING"))
            continue
        if check == "score":
            actual = float(row["delta_squared_score"])
        elif check.startswith("c"):
            actual = float(row[f"{check[0]}{check[1]}_" + {
                "c1":"recency_accel", "c2":"design_convergence",
                "c3":"subset_validation", "c4":"replication",
                "c5":"trajectory_mismatch"
            }[check]])
        else:
            results.append((entity_id, check, threshold, None, "UNKNOWN_CHECK"))
            continue
        # equality check for c5==1.0 anchors; minimum-threshold for others
        if check == "c5" and abs(threshold - 1.0) < 1e-6:
            ok = abs(actual - 1.0) < 1e-6
        else:
            ok = actual >= threshold
        results.append((entity_id, check, threshold, actual,
                        "PASS" if ok else "FAIL"))
    passed = all(r[4] == "PASS" for r in results)
    return passed, results

def main():
    sources, fragments, links, hyp, itv, mec = build_entity_index(ATLAS_DIR)
    evidence = gather_evidence_per_entity(sources, fragments, links)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    rankings_path     = OUTPUT_DIR / "rankings.csv"
    components_path   = OUTPUT_DIR / "components.csv"
    run_summary_path  = OUTPUT_DIR / "run_summary.json"
    history_path      = OUTPUT_DIR / "score_history.csv"
    anomalies_path    = OUTPUT_DIR / "anomaly_flags.csv"
    calibration_path  = OUTPUT_DIR / "calibration_status.txt"
    gaps_path         = OUTPUT_DIR / "data_gaps.csv"
    reflex_log_path   = OUTPUT_DIR / "reflexivity_audit.csv"
    reflex_status_path= OUTPUT_DIR / "reflexivity_status.txt"

    rows_rank, rows_comp, anomalies, gaps = [], [], [], []
    run_ts = datetime.now(timezone.utc).isoformat(timespec="seconds")

    for entity_type, lookup in (("hypothesis", hyp),
                                ("intervention", itv),
                                ("mechanism", mec)):
        for eid in sorted(lookup.keys()):
            recs   = evidence.get((entity_type, eid), [])
            status = lookup[eid].get("status","")
            name   = lookup[eid].get("name","")
            score, comps = score_entity(recs, status)
            n_sources = len({r["source_id"] for r in recs})

            rows_rank.append({
                "entity_type": entity_type, "entity_id": eid, "name": name,
                "status": status, "n_sources": n_sources,
                "delta_squared_score": round(score, 2),
            })
            rows_comp.append({
                "entity_type": entity_type, "entity_id": eid, "name": name,
                "status": status, "n_sources": n_sources,
                "c1_recency_accel":      round(comps[0], 4),
                "c2_design_convergence": round(comps[1], 4),
                "c3_subset_validation":  round(comps[2], 4),
                "c4_replication":        round(comps[3], 4),
                "c5_trajectory_mismatch":round(comps[4], 4),
                "delta_squared_score":   round(score, 2),
            })

            # anomaly flag
            top_src, frac = detect_dominance_anomaly(recs)
            if top_src:
                anomalies.append({
                    "run_timestamp": run_ts,
                    "entity_type":   entity_type,
                    "entity_id":     eid,
                    "name":          name,
                    "dominant_source_id": top_src,
                    "dominant_fraction":  round(frac, 3),
                    "delta_squared_score": round(score, 2),
                })

            # data-gap watchlist
            if eid in DATA_GAP_WATCHLIST and n_sources == 0:
                gaps.append({
                    "run_timestamp": run_ts,
                    "entity_type":   entity_type,
                    "entity_id":     eid,
                    "name":          name,
                    "n_sources":     0,
                    "note":          "Defined entity with zero ingested sources — data gap (Δ² flagship watchlist)",
                })

    # Stable descending sort
    rows_rank.sort(key=lambda r: (-r["delta_squared_score"], r["entity_id"]))
    rows_comp.sort(key=lambda r: (-r["delta_squared_score"], r["entity_id"]))

    # Write current state (overwrite)
    with open(rankings_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows_rank[0].keys())); w.writeheader(); w.writerows(rows_rank)
    with open(components_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows_comp[0].keys())); w.writeheader(); w.writerows(rows_comp)

    # Calibration check
    passed, results = check_calibration(rows_comp)

    # Reflexivity audit (reads history file BEFORE we append the current run)
    reflex = audit_reflexivity(sources, evidence, history_path, run_ts)

    # Combined pipeline pass: calibration must pass, AND reflexivity must
    # not have status FAIL (WARN, PASS, first_run, insufficient_data all OK)
    pipeline_pass = passed and (reflex["status"] != "FAIL")

    # Append-only history
    history_fields = ["run_timestamp", "entity_type", "entity_id",
                      "delta_squared_score", "c1_recency_accel",
                      "c2_design_convergence", "c3_subset_validation",
                      "c4_replication", "c5_trajectory_mismatch", "n_sources"]
    history_exists = history_path.exists()
    with open(history_path, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=history_fields)
        if not history_exists: w.writeheader()
        for r in rows_comp:
            w.writerow({"run_timestamp": run_ts,
                        "entity_type":   r["entity_type"],
                        "entity_id":     r["entity_id"],
                        "delta_squared_score": r["delta_squared_score"],
                        "c1_recency_accel":      r["c1_recency_accel"],
                        "c2_design_convergence": r["c2_design_convergence"],
                        "c3_subset_validation":  r["c3_subset_validation"],
                        "c4_replication":        r["c4_replication"],
                        "c5_trajectory_mismatch":r["c5_trajectory_mismatch"],
                        "n_sources":             r["n_sources"]})

    # Append-only anomalies
    if anomalies:
        anom_fields = ["run_timestamp","entity_type","entity_id","name",
                       "dominant_source_id","dominant_fraction",
                       "delta_squared_score"]
        anom_exists = anomalies_path.exists()
        with open(anomalies_path, "a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=anom_fields)
            if not anom_exists: w.writeheader()
            for a in anomalies: w.writerow(a)

    # Data gaps
    if gaps:
        gap_fields = ["run_timestamp","entity_type","entity_id","name","n_sources","note"]
        with open(gaps_path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=gap_fields); w.writeheader(); w.writerows(gaps)

    # Reflexivity audit log (append-only)
    reflex_log_fields = ["run_timestamp","prev_run_ts","status","spearman_r",
                         "n_entities","n_new_sources","message"]
    reflex_log_exists = reflex_log_path.exists()
    with open(reflex_log_path, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=reflex_log_fields)
        if not reflex_log_exists: w.writeheader()
        w.writerow({
            "run_timestamp":  run_ts,
            "prev_run_ts":    reflex.get("prev_run_ts") or "",
            "status":         reflex["status"],
            "spearman_r":     reflex["spearman_r"],
            "n_entities":     reflex["n_entities"],
            "n_new_sources":  reflex["n_new_sources"],
            "message":        reflex["message"],
        })

    # Reflexivity status (human-readable, overwritten each run)
    with open(reflex_status_path, "w", encoding="utf-8") as f:
        f.write("=" * 70 + "\n")
        f.write(f"Δ² REFLEXIVITY AUDIT — {run_ts}\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"  status:         {reflex['status']}\n")
        f.write(f"  prev_run_ts:    {reflex.get('prev_run_ts') or '(none)'}\n")
        f.write(f"  spearman_r:     {reflex['spearman_r']:.4f}\n")
        f.write(f"  n_entities_fed: {reflex['n_entities']}\n")
        f.write(f"  n_new_sources:  {reflex['n_new_sources']}\n")
        f.write(f"  warn threshold: {REFLEXIVITY_WARN_THRESHOLD}\n")
        f.write(f"  fail threshold: {REFLEXIVITY_FAIL_THRESHOLD}\n")
        f.write(f"\n  message: {reflex['message']}\n")
        if reflex["top_5_fed"]:
            f.write("\n  top 5 entities receiving new sources:\n")
            for t in reflex["top_5_fed"]:
                pr = t["prev_rank"]
                pr_s = f"{pr}" if pr is not None else "(unranked)"
                f.write(f"    {t['entity_type']:12s} {t['entity_id']:9s} "
                        f"new_sources={t['new_sources']:>3d}  prev_rank={pr_s}\n")
        f.write("\n" + "=" * 70 + "\n")
        f.write(f"OVERALL REFLEXIVITY: {reflex['status']}\n")
        f.write("=" * 70 + "\n")

    # Calibration human-readable status (now includes reflexivity result)
    with open(calibration_path, "w", encoding="utf-8") as f:
        f.write("=" * 70 + "\n")
        f.write(f"Δ² CALIBRATION STATUS — {run_ts}\n")
        f.write("=" * 70 + "\n\n")
        for entity_id, check, thresh, actual, status in results:
            actual_s = f"{actual:.4f}" if actual is not None else "MISSING"
            f.write(f"  [{status:7s}] {entity_id:9s} {check:6s} "
                    f"threshold={thresh:.4f} actual={actual_s}\n")
        f.write(f"\n  [{reflex['status']:7s}] reflexivity audit  "
                f"r={reflex['spearman_r']:.4f}  fail_at>={REFLEXIVITY_FAIL_THRESHOLD}\n")
        f.write("\n" + "=" * 70 + "\n")
        f.write(f"CALIBRATION: {'PASS' if passed else 'FAIL'}    "
                f"REFLEXIVITY: {reflex['status']}    "
                f"PIPELINE: {'PASS' if pipeline_pass else 'FAIL'}\n")
        f.write("=" * 70 + "\n")

    # Run summary
    with open(run_summary_path, "w", encoding="utf-8") as f:
        json.dump({
            "engine_version":     "delta-squared/1.1",
            "run_timestamp":      run_ts,
            "atlas_dir":          str(ATLAS_DIR),
            "current_year":       CURRENT_YEAR,
            "n_hypotheses":       len(hyp),
            "n_interventions":    len(itv),
            "n_mechanisms":       len(mec),
            "n_sources":          len(sources),
            "n_fragments":        len(fragments),
            "n_links":            len(links),
            "weights": {"C1":W_C1,"C2":W_C2,"C3":W_C3,"C4":W_C4,"C5":W_C5},
            "windows": {"recent": list(RECENT_WINDOW),
                        "prior":  list(PRIOR_WINDOW),
                        "deep":   list(DEEP_WINDOW)},
            "calibration_passed": passed,
            "calibration_results":[
                {"entity_id":eid,"check":chk,"threshold":t,"actual":a,"status":s}
                for eid,chk,t,a,s in results],
            "anomalies_count":    len(anomalies),
            "data_gaps_count":    len(gaps),
            "reflexivity":        reflex,
            "pipeline_pass":      pipeline_pass,
        }, f, indent=2)

    # Console summary
    print(f"Δ² engine v1.1 — {run_ts}")
    print(f"  scored {len(rows_rank)} entities ({len(hyp)} hyp, {len(itv)} int, {len(mec)} mec)")
    print(f"  windows: recent={list(RECENT_WINDOW)} prior={list(PRIOR_WINDOW)} deep={list(DEEP_WINDOW)}")
    print(f"  anomalies (single-source dominance >{ANOMALY_DOMINANCE_THRESHOLD:.0%}): {len(anomalies)}")
    print(f"  data gaps (watchlist): {len(gaps)}")
    print(f"  calibration: {'PASS' if passed else 'FAIL'}")
    print(f"  reflexivity: {reflex['status']} (r={reflex['spearman_r']:.4f}, "
          f"n_entities_fed={reflex['n_entities']}, n_new_sources={reflex['n_new_sources']})")

    if not passed:
        for eid, chk, t, a, s in results:
            if s != "PASS":
                a_s = f"{a:.4f}" if a is not None else "MISSING"
                print(f"    [{s}] {eid} {chk} expected>={t} got {a_s}")

    if reflex["status"] == "FAIL":
        print(f"  REFLEXIVITY HALT: {reflex['message']}")

    if not pipeline_pass:
        sys.exit(2)

    return 0

if __name__ == "__main__":
    sys.exit(main() or 0)
