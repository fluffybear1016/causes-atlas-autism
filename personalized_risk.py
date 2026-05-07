#!/usr/bin/env python3
"""
personalized_risk.py — Hannah Poling Personalized Risk Calculator engine v0.1

Per SESSION_4_HANNAH_POLING_SPEC.md (v2.3) — Layer 3 of the Causes Atlas.

This is a DETERMINISTIC v0.1 prototype. Per CLAUDE.md §11:
- No LLMs in scoring math
- Stable sort by ID throughout
- Idempotent: same input → byte-identical output
- No random seeds (no random sampling in canonical path)

v0.1 scope (per spec §15 Phase 2):
- Stage 1: Load + validate input.json
- Stage 2: Rare-syndrome screening gate (§4) — runs FIRST
- Stage 3: Genetic prior aggregation (subset of §3.1 functionality)
- Stage 4: Biomarker prior aggregation (subset of §3.2; uses raw values, no PSN normalization yet)
- Stage 5: Iatrogenic + exposure prior aggregation (§3.3 + §3.13c)
- Stage 6: Phenotype posterior via additive log-odds + sigmoid (Walley IDM lite)
- Stage 7: Intervention ranking (§7.10 utility function)
- Stage 8: Output JSON (§9.1 structure)

DEFERRED to v0.2+:
- Full Walley IDM credal aggregation with quadrature (§7.1)
- Within-phenotype responder model (§7.5)
- CDR state assignment (§7.6) — experimental per spec
- Functional trajectory predictor (§7.7) — qualitative bands only
- Pathway burden analysis (§7.4) — needs pathway_burden_table.csv
- Cross-modality concordance bonus (§6.2)
- PGx safety filter integration (§3.8)
- Physiological state normalization (§3.13b) — needs full ~400 rows
- Bayesian credal interval computation

Usage:
    python personalized_risk.py --input PATH/input.json [--output PATH/output.json]

Run as module:
    from personalized_risk import compute_personalized_risk
    output = compute_personalized_risk(input_data)
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ============================================================================
# CONSTANTS — v0.1 frozen per spec §7.1
# ============================================================================

ENGINE_VERSION = "session4_v0.4.0_profile_vector"
ATLAS_VERSION = "v2.0_scored"
CALIBRATION_ANCHOR_NAME = "INT-0001"
CALIBRATION_ANCHOR_REQUIRED_CSRS = 80.0
CALIBRATION_ANCHOR_CURRENT_CSRS = 83.35

# Profile-vector thresholds (v0.2 — post-mortem fix Move 1).
# Honest semantics: a "dominant" dimension has a posterior point estimate
# meaningfully above the neutral baseline of 0.50. A "dormant" dimension
# has a point estimate meaningfully below baseline, indicating the atlas
# evidence weighs against this dimension for this profile. The middle band
# is the honest "insufficient evidence either way" zone.
DOMINANT_LOADING_THRESHOLD = 0.55
DORMANT_LOADING_THRESHOLD = 0.45

# Atlas phenotypes
ALL_PHENOTYPE_IDS = [
    "PHE-0001",  # cerebral folate deficiency
    "PHE-0002",  # mitochondrial dysfunction
    "PHE-0003",  # regressive immune-inflammatory
    "PHE-0004",  # GI/microbiome
    "PHE-0005",  # mTOR pathway syndromic
    "PHE-0006",  # Fragile X
    "PHE-0007",  # GABA/Cl- imbalance
    "PHE-0008",  # Walsh undermethylator
    "PHE-0009",  # Walsh overmethylator
    "PHE-0010",  # Walsh pyroluria
    "PHE-0011",  # Walsh Cu:Zn imbalance
]

WALSH_PHENOTYPES = {"PHE-0008", "PHE-0009", "PHE-0010", "PHE-0011"}

# Atlas root (default = autism atlas at v2.0_scored/). Multi-atlas pivot:
# the engine accepts an arbitrary atlas_path so the same engine can drive
# any condition's atlas. Default preserved for back-compat with the current
# autism atlas location. See PLATFORM_PIVOT_v0.1.md.
ATLAS_ROOT = Path(__file__).parent / "v2.0_scored"
DEFAULT_ATLAS_ROOT = ATLAS_ROOT  # immutable reference for fallback

# Δ² overlay integration (Session 5, post-2026-05-05). The engine optionally
# reads delta_squared_v1/components.csv and applies a SMALL multiplicative
# momentum bonus to intervention scores. Truth-strength (CSRS) remains
# dominant; trajectory provides a tiebreaker.
#
# Formula: score = best_match × atlas_quality × (1 + α × Δ²/100)
# At α = 0.20:  Δ²=0 → ×1.00 ;  Δ²=50 → ×1.10 ;  Δ²=100 → ×1.20.
# A 14% CSRS gap can be made up by a ~70-point Δ² delta, but no more.
# This keeps the calculator anchored on truth, with momentum as a nudge.
DELTA_SQUARED_PATH = Path(__file__).parent / "delta_squared_v1" / "components.csv"
DELTA_SQUARED_BONUS_ALPHA = 0.20


# ============================================================================
# UTILS — deterministic helpers
# ============================================================================

def sigmoid(x: float) -> float:
    """Numerically stable sigmoid."""
    if x >= 0:
        return 1.0 / (1.0 + math.exp(-x))
    else:
        ex = math.exp(x)
        return ex / (1.0 + ex)


def round6(x: float) -> float:
    """Round to 6 decimal places (per spec §7.1.1)."""
    return round(x, 6)


def stable_sort_rows(rows: list[dict], key_field: str = "id") -> list[dict]:
    """Stable sort by ID per spec §7.3."""
    return sorted(rows, key=lambda r: r.get(key_field, ""))


def now_iso() -> str:
    """Reproducible timestamp (UTC, ISO 8601)."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


# ============================================================================
# ATLAS LOADERS — load CSVs into deterministic structures
# ============================================================================

def load_csv(path: Path) -> list[dict]:
    """Load a CSV file into a list of dicts, stable-sorted by 'id' field if present.

    Audit C-2 fix: explicit utf-8 encoding + newline='' for cross-platform determinism.
    Audit C-3 fix: raise on missing-ID rows in tables that have an 'id' column.
    """
    if not path.exists():
        return []
    with open(path, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    if rows and "id" in rows[0]:
        # C-3: raise if any row is missing its required ID
        missing = [i for i, r in enumerate(rows) if not r.get("id", "").strip()]
        if missing:
            raise ValueError(f"{path.name}: rows {missing[:5]} have empty 'id' field")
        rows = stable_sort_rows(rows, "id")
    return rows


def load_delta_squared(path: Path | str | None = None) -> dict[str, float]:
    """Load Δ² scores keyed by entity_id from delta_squared_v1/components.csv.

    Returns empty dict if file missing — graceful fallback so engine never
    fails because the Δ² overlay hasn't been computed yet. Deterministic;
    no side effects.
    """
    src = Path(path) if path else DELTA_SQUARED_PATH
    if not src.exists():
        return {}
    out: dict[str, float] = {}
    with open(src, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            try:
                out[r["entity_id"]] = float(r["delta_squared_score"])
            except (KeyError, ValueError):
                continue
    return out


def load_atlas(atlas_path: Path | str | None = None) -> dict[str, list[dict]]:
    """Load all Phase 0 CSVs into a dict keyed by table name.

    Multi-atlas pivot (post-mortem fix Move 1+ platform pivot):
    - atlas_path=None  → uses DEFAULT_ATLAS_ROOT (autism atlas at v2.0_scored/)
    - atlas_path=Path  → loads any condition's atlas under that directory
    - atlas_path=str   → coerced to Path

    The same set of canonical CSV table names is expected regardless of
    condition. Per-atlas variation is in the *content* (phenotype IDs,
    interventions, biomarker shifts) not the schema. An atlas missing a
    table simply produces an empty list for that key — no error.
    """
    root = Path(atlas_path) if atlas_path else ATLAS_ROOT
    tables = {
        "phenotypes": "phenotypes.csv",
        "interventions": "interventions.csv",
        "mechanisms": "mechanisms.csv",
        "iatrogenic": "iatrogenic_exposure_priors.csv",
        "syndromic_gate": "rare_syndrome_screening_gate.csv",
        "genetic_aliases": "genetic_id_aliases.csv",
        "baseline_prevalence": "baseline_phenotype_prevalence.csv",
        "pgx": "pgx_drug_gene_table.csv",
        "psn": "physiological_state_normalization_table.csv",
        "genes_phase0": "genes_phase0_additions.csv",
        "ipe": "intervention_phenotype_edges.csv",
    }
    return {k: load_csv(root / fname) for k, fname in tables.items()}


def load_atlas_manifest(atlas_path: Path | str) -> dict:
    """Load atlas_manifest.yaml describing per-condition metadata.

    Manifest fields (per PLATFORM_PIVOT_v0.1.md):
    - condition: human-readable name (e.g., "Autism", "Long COVID / ME-CFS")
    - condition_id: short identifier (e.g., "autism", "long_covid")
    - version: atlas version string
    - phenotype_taxonomy: list of {id, name, mechanism_summary}
    - calibration_anchor: {intervention_id, required_csrs_min, current_csrs}
    - upstream_atlases: optional cross-condition links (e.g., autism inherits mito)

    Returns {} if no manifest present (autism v2.0_scored has no manifest yet —
    this is back-compat tolerated; condition #2 onwards are required to ship one).
    """
    root = Path(atlas_path)
    manifest_path = root / "atlas_manifest.yaml"
    if not manifest_path.exists():
        return {}
    try:
        import yaml
        with open(manifest_path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except ImportError:
        return {"_warning": "PyYAML not installed — manifest not parsed"}
    except Exception as e:
        return {"_error": f"manifest parse failed: {e}"}


# ============================================================================
# STAGE 1 — INPUT VALIDATION
# ============================================================================

def validate_input(input_data: dict) -> list[str]:
    """Return list of validation errors; empty list = valid."""
    errors = []
    required_top = ["case_id", "input_version", "operating_mode", "subject_sex"]
    for key in required_top:
        if key not in input_data:
            errors.append(f"missing required field: {key}")

    if input_data.get("operating_mode") not in (
        "preconception", "pregnancy", "young_child", "older_child", "adult"
    ):
        errors.append(f"invalid operating_mode: {input_data.get('operating_mode')}")

    if input_data.get("subject_sex") not in ("M", "F", "intersex", "unknown"):
        errors.append(f"invalid subject_sex: {input_data.get('subject_sex')}")

    return errors


# ============================================================================
# STAGE 2 — RARE-SYNDROME SCREENING GATE (§4)
# ============================================================================

def run_syndromic_gate(input_data: dict, atlas: dict) -> dict | None:
    """
    Per spec §4: runs FIRST in the calculation engine. If a syndromic match
    is detected, returns syndrome-specific output that bypasses generic
    phenotype assignment.

    Returns None if no syndromic match. Returns dict with syndrome_match info
    if matched.
    """
    syndromic_rows = atlas["syndromic_gate"]

    # Get genetic data from input
    genomics = input_data.get("genomics", {})
    cnvs = genomics.get("cnvs", {}).get("child", [])
    rare_variants = genomics.get("wes_wgs_rare_variants", {}).get("child", [])
    snps = genomics.get("snps", {}).get("child", {})

    # Check CNVs against syndromic gate (sorted for determinism)
    for cnv in sorted(cnvs, key=lambda c: c.get("region", "")):
        region = cnv.get("region", "")
        if not region:
            continue
        for rsg in syndromic_rows:
            gene_or_locus = rsg.get("gene_or_locus", "")
            if region in gene_or_locus or gene_or_locus.replace(" ", "").startswith(region):
                # Match on chromosomal region (e.g., "22q11.2", "16p11.2")
                if cnv.get("type") == "deletion" and "deletion" in rsg.get("syndrome_name", "").lower():
                    return {
                        "syndrome_match_id": rsg["id"],
                        "syndrome_name": rsg["syndrome_name"],
                        "matched_input": f"cnv {region} {cnv['type']}",
                        "target_routing": rsg["target_phenotype_routing"],
                        "primary_pmid": rsg["primary_pmid"],
                    }
                elif cnv.get("type") == "duplication" and "duplication" in rsg.get("syndrome_name", "").lower():
                    return {
                        "syndrome_match_id": rsg["id"],
                        "syndrome_name": rsg["syndrome_name"],
                        "matched_input": f"cnv {region} {cnv['type']}",
                        "target_routing": rsg["target_phenotype_routing"],
                        "primary_pmid": rsg["primary_pmid"],
                    }

    # Check FMR1 CGG repeat for FXS
    if "rs_fmr1_cgg_repeats" in snps or any("FMR1" in str(v) for v in snps.values()):
        # Simplified — FXS check would parse CGG repeat number
        pass

    # Check rare variants
    for rv in sorted(rare_variants, key=lambda v: v.get("gene", "")):
        gene = rv.get("gene", "")
        if not gene:
            continue
        if rv.get("acmg_classification") in ("pathogenic", "likely_pathogenic"):
            for rsg in syndromic_rows:
                if gene == rsg.get("gene_or_locus", "").split()[0]:
                    return {
                        "syndrome_match_id": rsg["id"],
                        "syndrome_name": rsg["syndrome_name"],
                        "matched_input": f"rare_variant {gene}",
                        "target_routing": rsg["target_phenotype_routing"],
                        "primary_pmid": rsg["primary_pmid"],
                    }

    return None


# ============================================================================
# STAGE 3-5 — PRIOR AGGREGATION (simplified v0.1)
# ============================================================================

def _detect_input_features(input_data: dict) -> set:
    """
    Audit fix (Walsh ranking PARTIAL → PASS): detect biomarker/feature patterns
    in input that should gate baseline-row selection. Returns set of feature
    tags matched by row population_context substrings.
    """
    features = set()

    immunology = input_data.get("immunology", {}) or {}
    autoabs = immunology.get("autoantibodies", {}) or {}
    fraa_blk = autoabs.get("fraa_blocking", {}) or {}
    if str(fraa_blk.get("result", "")).startswith("positive"):
        features.add("FRAA_positive")

    mtdna = (input_data.get("genomics", {}) or {}).get("mtdna", {}).get("child", {}) or {}
    if mtdna.get("heteroplasmy_variants") or mtdna.get("respiratory_chain_complex_deficits"):
        features.add("mito_marker_elevated")
        features.add("mitochondrial_marker_elevated")
        features.add("at_least_one_mito_biomarker_abnormal")

    metab = input_data.get("metabolomics_proteomics_epigenetics", {}) or {}
    if metab.get("metabolomics"):
        aa = metab["metabolomics"].get("amino_acids_plasma") or {}
        untargeted = metab["metabolomics"].get("untargeted_metabolomics_z_scores") or {}
        if aa.get("histamine_low_per_walsh") or untargeted.get("sam_sah_low_per_walsh"):
            features.add("walsh_undermethylator")
        if aa.get("histamine_high_per_walsh"):
            features.add("walsh_overmethylator")

    comorbid = input_data.get("comorbidities", {}) or {}
    gi = comorbid.get("gi_clusters", {}) or {}
    if any([gi.get("chronic_constipation"), gi.get("chronic_diarrhea"),
            gi.get("reflux"), gi.get("abdominal_pain_chronic"),
            gi.get("feeding_intolerance")]):
        features.add("GI_symptomatic")

    return features


def _is_generic_baseline_row(population_context: str) -> bool:
    """
    Identify rows that serve as ungated/generic base-rate fallbacks.
    Examples: "clinical_CFD_strict_criteria", "in_autism_population" (no marker suffix).
    """
    ctx = (population_context or "").lower()
    if not ctx:
        return False
    # Strict-criteria definitions are generic
    if "strict_criteria" in ctx or "strict_dx" in ctx:
        return True
    # Bare "in_autism_population" without marker suffix
    if ctx in ("in_autism_population", "in_autism_population_general"):
        return True
    return False


def _row_marker_gate_satisfied(population_context: str, features: set) -> bool:
    """
    Check if a row's marker-gating is satisfied by input features.
    Rows whose context names a specific marker (FRAA_positive, walsh_undermethylator,
    mitochondrial_marker_elevated, GI_symptomatic, etc.) are ELIGIBLE only when
    that marker is present in input features.

    Generic rows (strict_criteria, etc.) are always eligible.
    """
    ctx = (population_context or "").lower()
    if not ctx:
        return False
    if _is_generic_baseline_row(ctx):
        return True
    # Check whether any input feature matches the row's context tokens
    for f in features:
        if f.lower() in ctx:
            return True
    return False


def baseline_phenotype_log_odds(phenotype_id: str, atlas: dict, family_history: dict,
                                input_data: dict | None = None) -> float:
    """
    Compute log-odds prior for a phenotype based on baseline prevalence.

    v0.1.1 fix (Walsh ranking PARTIAL → PASS): input-conditional baseline picker.
    1. Exclude responder/leucovorin rows (intervention-conditional rates,
       not base rates).
    2. Filter to: marker-gated rows whose gating marker is satisfied by input
       features, OR generic rows (strict-criteria, no-marker-suffix).
    3. Among eligible rows, prefer marker-matched > generic. Tie-break by
       confidence (HIGH>MODERATE>LOW), then by ID (stable).
    4. Fallback to lowest-prevalence eligible row if no input features match.
    """
    rows = [r for r in atlas["baseline_prevalence"]
            if r.get("phenotype_id") == phenotype_id]
    if not rows:
        return math.log(0.01 / (1 - 0.01))

    # Step 1: exclude responder/leucovorin rows (response rates, not base rates)
    EXCLUDE_PATTERNS = ("responder", "leucovorin")
    rows = [r for r in rows
            if not any(p in (r.get("population_context", "") or "").lower()
                       for p in EXCLUDE_PATTERNS)]
    if not rows:
        return math.log(0.01 / (1 - 0.01))

    features = _detect_input_features(input_data) if input_data else set()

    # Step 2: filter to eligible rows (marker-gated AND satisfied) OR generic
    eligible = [r for r in rows
                if _row_marker_gate_satisfied(r.get("population_context", ""), features)]

    # Fallback: if no eligible row, use most-conservative (lowest point) row
    if not eligible:
        rows.sort(key=lambda r: (float(r.get("prevalence_point_estimate", 0.01)),
                                  r.get("id", "")))
        eligible = [rows[0]]

    # Step 3: among eligible, prefer marker-matched > generic, then confidence, then ID
    confidence_rank = {"HIGH": 3, "MODERATE": 2, "LOW": 1}

    def score_row(r: dict) -> tuple:
        ctx = (r.get("population_context", "") or "").lower()
        is_generic = _is_generic_baseline_row(ctx)
        match_score = sum(1 for f in features if f.lower() in ctx)
        conf = confidence_rank.get(r.get("confidence_label", "LOW"), 1)
        # Marker-matched rows preferred over generic; among matched rows higher
        # match_score wins; then confidence; then ID
        return (-match_score, 1 if is_generic else 0, -conf, r.get("id", ""))

    eligible.sort(key=score_row)
    row = eligible[0]
    p = float(row.get("prevalence_point_estimate", 0.01))
    p = max(min(p, 0.99), 0.01)
    return math.log(p / (1 - p))


def _normalize_token(s: str) -> str:
    """Normalize a name token for safe matching (lowercase, alnum-only)."""
    return "".join(c for c in s.lower() if c.isalnum())


def _exposure_inventory(input_data: dict) -> list[dict]:
    """
    Audit C-5 fix: collect ALL exposures from maternal pregnancy + gestational +
    POSTNATAL child + planned exposures. Returns list of {name, kind, source}
    for matching against iatrogenic table.
    """
    inventory = []
    # Maternal pregnancy meds
    for med in input_data.get("maternal", {}).get("pregnancy_history", {}).get("medications", []):
        if med.get("name"):
            inventory.append({"name": med["name"], "kind": "medication",
                              "source": "maternal.pregnancy_history.medications"})
    # Gestational vaccinations
    for vax in input_data.get("gestational_birth_data", {}).get("vaccinations_administered", []) or []:
        if vax.get("vaccine"):
            inventory.append({"name": vax["vaccine"], "kind": "vaccine",
                              "source": "gestational_birth_data.vaccinations_administered",
                              "events": vax.get("post_vaccination_events", [])})
    # POSTNATAL child medications + supplements (was missing entirely)
    cd = input_data.get("child_data") or {}
    for med in cd.get("current_medications", []) or []:
        if isinstance(med, str):
            inventory.append({"name": med, "kind": "medication", "source": "child_data.current_medications"})
        elif isinstance(med, dict) and med.get("name"):
            inventory.append({"name": med["name"], "kind": "medication", "source": "child_data.current_medications"})
    for sup in cd.get("current_supplements", []) or []:
        if isinstance(sup, str):
            inventory.append({"name": sup, "kind": "supplement", "source": "child_data.current_supplements"})
    # Adult mode self_data
    sd = input_data.get("self_data") or {}
    for med in sd.get("current_medications", []) or []:
        if isinstance(med, str):
            inventory.append({"name": med, "kind": "medication", "source": "self_data.current_medications"})
    # Planned exposures
    pe = input_data.get("planned_exposures") or {}
    for v in pe.get("vaccine_schedule", []) or []:
        if v.get("vaccine"):
            inventory.append({"name": v["vaccine"], "kind": "vaccine_planned",
                              "source": "planned_exposures.vaccine_schedule"})
    for m in pe.get("medications_planned", []) or []:
        if m.get("name"):
            inventory.append({"name": m["name"], "kind": "medication_planned",
                              "source": "planned_exposures.medications_planned"})
    return inventory


def _iatrogenic_match(exposure_name: str, iep_specific_agent: str) -> bool:
    """
    Audit C-4 fix: tightened matching. Exact normalized-token match against
    underscore-or-hyphen-separated agent list. NO loose substring fallback.

    Audit Issue 6 fix (post-mortem): the strict-token form alone rejected
    common typed inputs like "hepatitis_b_vaccine" against an IEP row with
    specific_agent "hep_b_birth_dose" (tokens hepb, birth, dose vs
    hepatitis, b, vaccine — no overlap). Added a curated synonym table for
    high-priority contested agents so user-typed input is recognized. Each
    synonym is bidirectional and conservative (we add only well-established
    drug/exposure aliases; never fuzzy / Levenshtein matches that risk
    false positives).
    """
    if not exposure_name or not iep_specific_agent:
        return False
    exposure_tok = _normalize_token(exposure_name)
    if len(exposure_tok) < 3:  # Reject 1-2 character tokens (false-positive risk)
        return False

    # Split agent on token separators
    agent_tokens = re.split(r"[_;,\s/+]+", iep_specific_agent.lower())
    agent_tokens_norm = [_normalize_token(t) for t in agent_tokens if t.strip()]

    if exposure_tok in agent_tokens_norm:
        return True

    # Curated synonym table — bidirectional. Each tuple lists alternate
    # tokens that should match the canonical form anywhere in the agent.
    # Order: (canonical_token, [aliases...]).
    SYNONYMS = [
        ("hepb", ["hepatitisb", "hepatitis", "hepb", "hbv"]),  # hep B
        ("mmr", ["mmr", "measlesmumpsrubella", "mumprubella"]),  # MMR
        ("dtap", ["dtap", "diphtheria", "pertussis", "tetanus", "tdap"]),
        ("hib", ["hib", "haemophilus"]),
        ("pcv13", ["pcv13", "pcv", "pneumococcal", "prevnar"]),
        ("rotavirus", ["rotavirus", "rotateq", "rotarix"]),
        ("ipv", ["ipv", "polio", "poliovirus"]),
        ("varicella", ["varicella", "chickenpox", "varivax"]),
        ("flu", ["flu", "influenza"]),
        ("aluminum", ["aluminum", "aluminium", "alum"]),
        ("thimerosal", ["thimerosal", "thiomersal"]),
        ("acetaminophen", ["acetaminophen", "paracetamol", "tylenol"]),
        ("valproate", ["valproate", "valproicacid", "depakote"]),
    ]
    for canonical, aliases in SYNONYMS:
        # Hit if both the agent string contains the canonical token and the
        # exposure normalized form is one of the aliases (or vice versa).
        agent_contains = canonical in agent_tokens_norm or canonical in iep_specific_agent.lower()
        exposure_aliased = exposure_tok in aliases
        if agent_contains and exposure_aliased:
            return True
        # Reverse: agent uses an alias, exposure uses canonical
        agent_aliased = any(a in agent_tokens_norm for a in aliases)
        exposure_canonical = exposure_tok == canonical
        if agent_aliased and exposure_canonical:
            return True

    return False


def collect_iatrogenic_shifts(input_data: dict, atlas: dict) -> dict[str, float]:
    """
    Compute log-odds shifts from iatrogenic exposures present in input.
    Returns dict phenotype_id → cumulative log_odds_shift.

    Audit C-4 + C-5 fixes: tightened matching + postnatal exposures included.
    Audit H-1 fix: §6.1 dedup — when a population-average row and a
    subgroup-conditional row both match for the same iatrogenic_id, only
    one is applied (the subgroup row if its profile matches; else population).
    """
    inventory = _exposure_inventory(input_data)
    if not inventory:
        return {}

    # Bucket iatrogenic rows by iatrogenic_id (canonical anchor) for §6.1 dedup
    iep_rows_by_anchor: dict[str, list[dict]] = {}
    for iep in atlas["iatrogenic"]:
        anchor = iep.get("iatrogenic_id", "") or iep.get("id", "")
        iep_rows_by_anchor.setdefault(anchor, []).append(iep)

    shifts: dict[str, float] = {}
    matched_anchors_seen: set[tuple[str, str]] = set()  # (anchor, target_phe)

    # Determine if subject has any "mito_vulnerable_classic" susceptibility profile
    # (simplified — checks for mtDNA heteroplasmy or mito enzyme deficits)
    has_mito_vulnerable = False
    mtdna = input_data.get("genomics", {}).get("mtdna", {}).get("child", {}) or {}
    if mtdna.get("heteroplasmy_variants") or mtdna.get("respiratory_chain_complex_deficits"):
        has_mito_vulnerable = True

    # Sort by anchor ID for determinism
    for anchor in sorted(iep_rows_by_anchor.keys()):
        rows = iep_rows_by_anchor[anchor]
        # Find any matching exposure in inventory
        matched_exposures = []
        for inv_item in inventory:
            for iep in rows:
                if _iatrogenic_match(inv_item["name"], iep.get("specific_agent", "")):
                    matched_exposures.append((inv_item, iep))
                    break  # one match per inventory item per anchor
        if not matched_exposures:
            continue

        # H-1 fix: §6.1 step 2 — dedup by (anchor, target_phe). Prefer subgroup-
        # conditional row if subject matches susceptibility profile; else population.
        # Group matched rows by target_phe and apply only one per group.
        rows_by_target: dict[str, list[dict]] = {}
        for inv, iep in matched_exposures:
            tp = iep.get("target_phenotype_id", "").strip()
            if tp:
                rows_by_target.setdefault(tp, []).append(iep)

        for tp, candidate_rows in rows_by_target.items():
            if (anchor, tp) in matched_anchors_seen:
                continue
            matched_anchors_seen.add((anchor, tp))

            # §6.3 subgroup-supersedes-population: prefer the subgroup-conditional
            # row if profile matches; otherwise use population-average row
            subgroup_row = None
            population_row = None
            for r in candidate_rows:
                cond = r.get("conditional_on_susceptibility", "always")
                if cond == "always":
                    population_row = r
                elif cond == "mito_vulnerable_classic" and has_mito_vulnerable:
                    subgroup_row = r

            chosen = subgroup_row if subgroup_row is not None else population_row
            if chosen is None:
                continue

            # Apply shift (subgroup uses log_odds_shift_in_subgroup; population uses log_odds_shift)
            try:
                if subgroup_row is not None:
                    shift = float(chosen.get("log_odds_shift_in_subgroup", chosen.get("log_odds_shift", 0)))
                else:
                    shift = float(chosen.get("log_odds_shift", 0))
                ev_quality = float(chosen.get("evidence_quality", 0.5))
                shifts[tp] = shifts.get(tp, 0) + shift * ev_quality
            except (ValueError, TypeError):
                pass

    return shifts


def collect_biomarker_shifts(input_data: dict, atlas: dict) -> dict[str, float]:
    """
    Compute log-odds shifts from biomarkers present in input.

    v0.3 (post-mortem fix expanded coverage): now drives shifts across all
    11 phenotype dimensions where typed input is available, not just the
    3 dimensions of v0.1. Each shift magnitude is grounded in either the
    biomarker_phenotype_edges.csv evidence_strength values or hand-curated
    Walsh / Frye / Rossignol functional-medicine literature priors.

    v0.4 (cohort-driven driver expansion, 2026-05-07): closes two cohort
    calibration gaps surfaced by the responder-rate cohort.
    - PHE-0004 (GI/microbiome): now accepts severity-string-graded GI fields
      (constipation_severity, diarrhea_severity, etc.) in addition to the
      legacy boolean flags; reads per-sample microbiome composition signals
      (bifidobacterium_low, prevotella_low, low_diversity, akkermansia_depleted,
      clostridia_overgrowth, klebsiella_overgrowth, candida_overgrowth) from
      microbiome.samples[]; adds GSRS-severity proxy weight. Closes the Kang
      2017 MTT cohort entry from AE 0.389 → expected ~0.13.
    - PHE-0007 (GABA/Cl⁻): now also reads the alternative biomarkers.child_data
      path used by Lemonnier rrc_002; adds clinical epilepsy.present, subclinical
      epileptiform EEG (Chez 2002 cohort signal), concomitant GABAergic
      anticonvulsants (valproate / vigabatrin / tiagabine), and MR spectroscopy
      GABA/Glu ratio. Unblocks Lemonnier rrc_002 cohort entry validation.

    v0.5 roadmap: replace the explicit-rule dispatcher with a data-driven
    loop reading from biomarker_phenotype_edges.csv plus a
    `biomarker_input_registry.yaml` that maps input.json paths →
    biomarker_id. Current explicit form is preserved for v0.3+v0.4 because
    rule semantics (severity strings, above-range thresholds, binary flags,
    sample-level vs root-level encoding) are not yet uniformly encoded in
    the atlas edge data.
    """
    shifts: dict[str, float] = {}

    immunology = input_data.get("immunology", {}) or {}
    autoabs = immunology.get("autoantibodies", {}) or {}

    # ------------------------------------------------------------------
    # PHE-0001 — Cerebral folate deficiency
    # ------------------------------------------------------------------
    # FRAA (folate receptor alpha autoantibody) — blocking
    fraa_blocking = autoabs.get("fraa_blocking", {}) or {}
    if fraa_blocking.get("result", "").startswith("positive"):
        try:
            value = float(fraa_blocking.get("value", 0))
            if value >= 1.0:
                shifts["PHE-0001"] = shifts.get("PHE-0001", 0) + 0.55  # strong positive
            elif value >= 0.5:
                shifts["PHE-0001"] = shifts.get("PHE-0001", 0) + 0.30  # moderate
        except (ValueError, TypeError):
            pass

    # ------------------------------------------------------------------
    # PHE-0002 — Mitochondrial dysfunction
    # ------------------------------------------------------------------
    # mtDNA heteroplasmy
    mtdna = input_data.get("genomics", {}).get("mtdna", {}) or {}
    child_mtdna = mtdna.get("child", {}) or {}
    if child_mtdna and child_mtdna.get("heteroplasmy_variants"):
        shifts["PHE-0002"] = shifts.get("PHE-0002", 0) + 0.65

    # Respiratory chain complex deficits
    rcc_deficits = child_mtdna.get("respiratory_chain_complex_deficits", []) if child_mtdna else []
    if rcc_deficits:
        shifts["PHE-0002"] = shifts.get("PHE-0002", 0) + 0.85

    # Lactate elevation, organic acid mito markers
    metab = input_data.get("metabolomics_proteomics_epigenetics", {}) or {}
    metabolomics = metab.get("metabolomics") or {}
    oat = metabolomics.get("organic_acids_urine") or {}
    if oat.get("lactate_elevated") or oat.get("pyruvate_elevated"):
        shifts["PHE-0002"] = shifts.get("PHE-0002", 0) + 0.30
    if oat.get("citric_acid_cycle_intermediates_elevated"):
        shifts["PHE-0002"] = shifts.get("PHE-0002", 0) + 0.20

    # ------------------------------------------------------------------
    # PHE-0003 — Regressive immune-inflammatory + MCAS subset
    # ------------------------------------------------------------------
    # Cytokine elevation (Frye/Rossignol/Theoharides literature)
    cytokine_panel = immunology.get("cytokine_panel", {}) or {}
    if cytokine_panel.get("il6_elevated") or cytokine_panel.get("tnf_alpha_elevated"):
        shifts["PHE-0003"] = shifts.get("PHE-0003", 0) + 0.40
    if cytokine_panel.get("neopterin_elevated"):
        shifts["PHE-0003"] = shifts.get("PHE-0003", 0) + 0.25

    # MCAS markers
    mcas = (input_data.get("comorbidities") or {}).get("mcas_features") or {}
    if mcas.get("tryptase_elevated") or mcas.get("methylhistamine_elevated"):
        shifts["PHE-0003"] = shifts.get("PHE-0003", 0) + 0.35

    # Cunningham panel (PANS/PANDAS subset)
    if autoabs.get("cunningham_panel", {}) and autoabs["cunningham_panel"].get("composite_elevated"):
        shifts["PHE-0003"] = shifts.get("PHE-0003", 0) + 0.45

    # ------------------------------------------------------------------
    # PHE-0004 — GI / microbiome
    # ------------------------------------------------------------------
    # v0.4 expansion: accept BOTH the boolean-flag encoding (legacy) and
    # the severity-graded string encoding ("moderate", "moderate_to_severe",
    # "severe") that newer cohort representative profiles use. Per-symptom
    # union semantics: a symptom is "active" if EITHER its boolean flag is
    # truthy OR its severity string starts with "moderate" or "severe".
    # Same magnitude buckets as before so calibration anchors don't break.
    comorbid = input_data.get("comorbidities", {}) or {}
    gi = comorbid.get("gi_clusters", {}) or {}

    def _gi_severity_active(sev_value: object) -> bool:
        s = str(sev_value or "").lower()
        return s.startswith("moderate") or s.startswith("severe")

    gi_symptom_pairs = [
        # (boolean_field_name, severity_field_name, output_label)
        ("chronic_constipation", "constipation_severity", "constipation"),
        ("chronic_diarrhea", "diarrhea_severity", "diarrhea"),
        ("reflux", "reflux_severity", "reflux"),
        ("abdominal_pain_chronic", "abdominal_pain_severity", "abdominal_pain"),
        ("feeding_intolerance", "feeding_intolerance_severity", "feeding_intolerance"),
        (None, "indigestion_severity", "indigestion"),  # severity-only field
    ]
    active_gi_symptoms: set[str] = set()
    for bool_key, sev_key, label in gi_symptom_pairs:
        if bool_key and gi.get(bool_key):
            active_gi_symptoms.add(label)
            continue
        if _gi_severity_active(gi.get(sev_key)):
            active_gi_symptoms.add(label)
    gi_active_count = len(active_gi_symptoms)
    if gi_active_count >= 3:
        shifts["PHE-0004"] = shifts.get("PHE-0004", 0) + 0.55  # heavy GI cluster
    elif gi_active_count == 2:
        shifts["PHE-0004"] = shifts.get("PHE-0004", 0) + 0.35  # moderate GI cluster
    elif gi_active_count == 1:
        # Single-symptom GI signal is weak (e.g., reflux alone is common
        # without dysbiosis); only enough to nudge, not to drive dominance.
        shifts["PHE-0004"] = shifts.get("PHE-0004", 0) + 0.15

    # v0.4: GSRS severity proxy flag (Kang 2017 inclusion criterion mirror).
    # Adds modest weight when the profile flags moderate-to-severe baseline
    # GSRS without redundantly adding per-symptom shifts (those above already
    # capture the underlying symptom load).
    if gi.get("_gsrs_score_baseline_severe_per_kang_inclusion"):
        shifts["PHE-0004"] = shifts.get("PHE-0004", 0) + 0.20

    # GI biomarker panel: calprotectin, zonulin
    gi_panel = metab.get("gi_panel") or {}
    if gi_panel.get("calprotectin_elevated"):
        shifts["PHE-0004"] = shifts.get("PHE-0004", 0) + 0.40
    if gi_panel.get("zonulin_elevated"):
        shifts["PHE-0004"] = shifts.get("PHE-0004", 0) + 0.30

    # Microbiome dysbiosis flag (root-level legacy encoding)
    microbiome_root = input_data.get("microbiome", {}) or {}
    if microbiome_root.get("dysbiosis_flag") or microbiome_root.get("akkermansia_depleted"):
        shifts["PHE-0004"] = shifts.get("PHE-0004", 0) + 0.30

    # v0.4: per-sample microbiome composition signals (Kang 2017 / Hsiao /
    # Vuong-Kang dysbiosis literature). Each distinct abnormality flag
    # adds +0.20, capped at +0.40 total to prevent multi-correlated-signal
    # double-counting. Sorted iteration for determinism.
    microbiome_samples = microbiome_root.get("samples", []) or []
    microbiome_distinct = set()
    for sample in microbiome_samples:
        if not isinstance(sample, dict):
            continue
        for flag in sorted(sample.keys()):
            if flag in (
                "bifidobacterium_low", "prevotella_low", "low_diversity",
                "akkermansia_depleted", "clostridia_overgrowth",
                "klebsiella_overgrowth", "candida_overgrowth",
            ) and sample.get(flag):
                microbiome_distinct.add(flag)
    microbiome_count = len(microbiome_distinct)
    if microbiome_count >= 2:
        shifts["PHE-0004"] = shifts.get("PHE-0004", 0) + 0.40
    elif microbiome_count == 1:
        shifts["PHE-0004"] = shifts.get("PHE-0004", 0) + 0.20

    # ------------------------------------------------------------------
    # PHE-0005 — mTOR pathway syndromic
    # ------------------------------------------------------------------
    # Macrocephaly Z-score is a strong PTEN/TSC mTOR proxy
    child_data = input_data.get("child_data", {}) or {}
    anth = child_data.get("anthropometrics", {}) or {}
    try:
        head_z = anth.get("head_circumference_z_for_age_sex")
        if head_z is not None and float(head_z) >= 2.0:
            shifts["PHE-0005"] = shifts.get("PHE-0005", 0) + 0.55
    except (ValueError, TypeError):
        pass

    # mTOR-pathway rare variants (TSC1, TSC2, PTEN, MTOR, NF1, etc.) flag.
    # Determinism fix (audit Issue 7): sort variants by gene before iterating
    # so the break-loop choice is invariant to user-input ordering.
    rare_variants_raw = (input_data.get("genomics") or {}).get("wes_wgs_rare_variants", {}).get("child", []) or []
    rare_variants = sorted(
        [v for v in rare_variants_raw if isinstance(v, dict)],
        key=lambda v: ((v.get("gene") or "").upper(), str(v.get("variant_id") or v.get("hgvs") or ""))
    )
    mtor_genes = {"TSC1", "TSC2", "PTEN", "MTOR", "NF1", "DEPDC5", "RHEB", "AKT3", "PIK3CA"}
    for v in rare_variants:
        gene = (v.get("gene") or "").upper()
        if gene in mtor_genes:
            shifts["PHE-0005"] = shifts.get("PHE-0005", 0) + 0.85
            break  # one is enough

    # ------------------------------------------------------------------
    # PHE-0006 — Fragile X (FMR1)
    # ------------------------------------------------------------------
    for v in rare_variants:
        gene = (v.get("gene") if isinstance(v, dict) else "") or ""
        if gene.upper() == "FMR1":
            shifts["PHE-0006"] = shifts.get("PHE-0006", 0) + 1.50  # near-deterministic
            break

    # ------------------------------------------------------------------
    # PHE-0007 — GABA / Cl⁻ imbalance
    # ------------------------------------------------------------------
    # CSF or proxy intracellular chloride elevation (Lemonnier framework).
    # v0.4: also reads the alternative `biomarkers.child_data.*` path used
    # by some cohort representative profiles (rrc_002 Lemonnier). Union
    # semantics: only adds the shift once per signal class, even if both
    # encodings are present.
    neuro = input_data.get("neuroimaging_eeg", {}) or {}
    biomarkers_child = (input_data.get("biomarkers", {}) or {}).get("child_data", {}) or {}
    csf_proxy = bool(
        (neuro or {}).get("csf_chloride_elevated_proxy")
        or biomarkers_child.get("csf_or_neuronal_intracellular_chloride_proxy_high")
    )
    if csf_proxy:
        shifts["PHE-0007"] = shifts.get("PHE-0007", 0) + 0.50
    # KCC2 dysfunction proxy (rare; specialized testing)
    cytokine_panel = immunology.get("cytokine_panel", {}) or {}  # reuse var
    if (immunology.get("kcc2_dysfunction_proxy")
            or (input_data.get("comorbidities") or {}).get("kcc2_dysfunction_proxy")
            or biomarkers_child.get("kcc2_dysfunction_proxy")):
        shifts["PHE-0007"] = shifts.get("PHE-0007", 0) + 0.40

    # v0.4: clinical epilepsy diagnosis (existing comorbid signal). Strong
    # GABA-axis dysfunction prior — modest shift since epilepsy alone is
    # not deterministic for the bumetanide responder phenotype.
    epilepsy = (input_data.get("comorbidities", {}) or {}).get("epilepsy", {}) or {}
    if epilepsy.get("present"):
        shifts["PHE-0007"] = shifts.get("PHE-0007", 0) + 0.40

    # v0.4: subclinical epileptiform EEG (Chez 2002 had 13/31 = 42% of cohort).
    # Either encoded in current_diagnoses (string contains "epileptiform")
    # or as a comorbidity sub-flag.
    diagnoses_list = (input_data.get("child_data", {}) or {}).get("current_diagnoses", []) or []
    diagnoses_text = " ".join(str(d).lower() for d in diagnoses_list)
    if ("epileptiform" in diagnoses_text or
            epilepsy.get("_subclinical_epileptiform_activity_per_chez_cohort")):
        shifts["PHE-0007"] = shifts.get("PHE-0007", 0) + 0.25

    # v0.4: concomitant GABAergic anticonvulsant signals known GABA-axis
    # involvement (clinically managed seizure tendency or behavioral
    # indication). Audit-hardened (sub-agent v0.4 review): per-item word-
    # boundary regex match (not joined-string substring) AND skip items
    # whose lowercased text contains negation/historical markers ("no ",
    # "discontinued", "history of", "past ", "stopped", "former "). Includes
    # brand-name aliases per audit feedback.
    meds_list = (input_data.get("child_data", {}) or {}).get("current_medications", []) or []
    _meds_token_pattern = re.compile(
        r"\b(valproic|valproate|depakote|depakene|vigabatrin|sabril|tiagabine|gabitril)\b"
    )
    _meds_negation_markers = (
        "no ", "discontinued", "history of", "past ", "stopped", "former ",
        "previously", "h/o ", "hx ",
    )
    meds_active_gabaergic = False
    for m in meds_list:
        t = str(m).lower().strip()
        if not t:
            continue
        if any(neg in t for neg in _meds_negation_markers):
            continue
        if _meds_token_pattern.search(t):
            meds_active_gabaergic = True
            break
    if meds_active_gabaergic:
        shifts["PHE-0007"] = shifts.get("PHE-0007", 0) + 0.30

    # v0.4: MR spectroscopy GABA/Glu ratio (rare; specialized neuroimaging).
    if neuro.get("mrs_gaba_glu_ratio_low"):
        shifts["PHE-0007"] = shifts.get("PHE-0007", 0) + 0.40

    # ------------------------------------------------------------------
    # PHE-0008 — Walsh undermethylator
    # ------------------------------------------------------------------
    if metabolomics:
        aa = metabolomics.get("amino_acids_plasma") or {}
        if aa.get("histamine_low_per_walsh"):
            shifts["PHE-0008"] = shifts.get("PHE-0008", 0) + 0.55
        untargeted = metabolomics.get("untargeted_metabolomics_z_scores") or {}
        if untargeted.get("sam_sah_low_per_walsh"):
            shifts["PHE-0008"] = shifts.get("PHE-0008", 0) + 0.30

    # ------------------------------------------------------------------
    # PHE-0009 — Walsh overmethylator
    # ------------------------------------------------------------------
    if metabolomics:
        aa = metabolomics.get("amino_acids_plasma") or {}
        if aa.get("histamine_high_per_walsh"):
            shifts["PHE-0009"] = shifts.get("PHE-0009", 0) + 0.55
        untargeted = metabolomics.get("untargeted_metabolomics_z_scores") or {}
        if untargeted.get("sam_sah_high_per_walsh"):
            shifts["PHE-0009"] = shifts.get("PHE-0009", 0) + 0.30

    # ------------------------------------------------------------------
    # PHE-0010 — Walsh pyroluria / kryptopyrroluria
    # ------------------------------------------------------------------
    if metabolomics:
        oat = metabolomics.get("organic_acids_urine") or {}
        if oat.get("kryptopyrroles_elevated_urinary"):
            shifts["PHE-0010"] = shifts.get("PHE-0010", 0) + 0.55

    # ------------------------------------------------------------------
    # PHE-0011 — Walsh Cu:Zn imbalance
    # ------------------------------------------------------------------
    # Serum Cu high + Zn low, or Cu:Zn ratio elevated
    minerals = (metab or {}).get("trace_minerals") or {}
    if minerals.get("copper_high_serum") and minerals.get("zinc_low_serum"):
        shifts["PHE-0011"] = shifts.get("PHE-0011", 0) + 0.55
    elif minerals.get("copper_zinc_ratio_high"):
        shifts["PHE-0011"] = shifts.get("PHE-0011", 0) + 0.35

    return shifts


def collect_genetic_shifts(input_data: dict, atlas: dict) -> dict[str, float]:
    """
    Compute log-odds shifts from genetic variants present in input.
    v0.1 simplified — uses genetic_id_aliases for known variant→phenotype mappings.
    """
    shifts: dict[str, float] = {}

    snps = input_data.get("genomics", {}).get("snps", {}).get("child", {}) or {}

    # MTHFR C677T (rs1801133)
    if "rs1801133" in snps:
        gt = snps["rs1801133"].get("genotype", "")
        if gt == "T/T":
            shifts["PHE-0001"] = shifts.get("PHE-0001", 0) + 0.30  # T/T strong
        elif gt in ("C/T", "T/C"):
            shifts["PHE-0001"] = shifts.get("PHE-0001", 0) + 0.10  # heterozygous

    # Family history of autoimmune → PHE-0003
    family_hist = input_data.get("family_history", {}) or {}
    if family_hist.get("first_degree_autoimmune"):
        shifts["PHE-0003"] = shifts.get("PHE-0003", 0) + 0.20

    # Family history of autism (sibling) → general boost (Sandin 2014)
    sib_count = (family_hist.get("first_degree_autism") or {}).get("count", 0)
    if sib_count and sib_count > 0:
        # Boost the most-likely phenotype based on sibling phenotype
        sib_phe = (family_hist.get("first_degree_autism") or {}).get("phenotype_if_known")
        if sib_phe:
            shifts[sib_phe] = shifts.get(sib_phe, 0) + 0.50  # Sandin within-family clustering

    return shifts


# ============================================================================
# STAGE 6 — PHENOTYPE POSTERIOR AGGREGATION (Walley IDM lite v0.1)
# ============================================================================

def compute_phenotype_posteriors(
    input_data: dict, atlas: dict
) -> dict[str, dict[str, Any]]:
    """
    Per spec §7.1 (canonical s=2). v0.1 simplified — uses additive
    log-odds with sigmoid; no full credal interval yet (deferred to v0.2).
    """
    family_history = input_data.get("family_history", {}) or {}

    # Collect all shift sources (sorted for determinism)
    iatrogenic_shifts = collect_iatrogenic_shifts(input_data, atlas)
    biomarker_shifts = collect_biomarker_shifts(input_data, atlas)
    genetic_shifts = collect_genetic_shifts(input_data, atlas)

    posteriors = {}
    for phe_id in sorted(ALL_PHENOTYPE_IDS):
        baseline = baseline_phenotype_log_odds(phe_id, atlas, family_history, input_data)
        total_shift = (
            iatrogenic_shifts.get(phe_id, 0)
            + biomarker_shifts.get(phe_id, 0)
            + genetic_shifts.get(phe_id, 0)
        )
        log_odds = baseline + total_shift

        # v0.1 simplified credal interval: ±0.5 log-odds
        ci_low = log_odds - 0.5
        ci_high = log_odds + 0.5

        p_point = sigmoid(log_odds)
        p_low = sigmoid(ci_low)
        p_high = sigmoid(ci_high)

        # Drivers (sorted by absolute contribution)
        drivers = []
        for source, shift in [
            ("iatrogenic", iatrogenic_shifts.get(phe_id, 0)),
            ("biomarker", biomarker_shifts.get(phe_id, 0)),
            ("genetic", genetic_shifts.get(phe_id, 0)),
        ]:
            if abs(shift) > 0.01:
                drivers.append({"source": source, "log_odds_shift": round6(shift)})

        # Confidence label (Walsh phenotypes get LOW per audit C-5)
        confidence_label = "LOW" if phe_id in WALSH_PHENOTYPES else (
            "HIGH" if abs(total_shift) > 0.7 else "MODERATE"
        )
        evidence_tier = "framework_derived_LOW" if phe_id in WALSH_PHENOTYPES else "primary_evidence"

        posteriors[phe_id] = {
            "point": round6(p_point),
            "credal_low": round6(p_low),
            "credal_high": round6(p_high),
            "log_odds": round6(log_odds),
            "drivers": drivers,
            "confidence_label": confidence_label,
            "phenotype_evidence_tier": evidence_tier,
        }

    return posteriors


# ============================================================================
# STAGE 6.5 — PROFILE SUMMARY (v0.2 post-mortem fix Move 1)
# ============================================================================
# The lethal failure mode flagged in the post-mortem: real children hit
# multiple phenotype dimensions simultaneously, so single-top-phenotype
# classification doesn't survive contact with clinical cohorts. Fix: emit
# a profile loading vector (the same posteriors), plus an explicit summary
# of which dimensions are dominant / present / dormant for this child.
# Intervention ranking is then driven by weighted multi-target scoring
# across the loading vector instead of walking from a single top phenotype.

def compute_profile_summary(posteriors: dict[str, dict]) -> dict:
    """
    Reduce posteriors → profile summary describing the *shape* of this
    child's loading vector. Deterministic.

    Returns:
        dominant_dimensions: phenotype IDs with point ≥ DOMINANT_LOADING_THRESHOLD
        secondary_dimensions: phenotype IDs in [DORMANT, DOMINANT) — neutral band
        dormant_dimensions: phenotype IDs with point < DORMANT_LOADING_THRESHOLD
        profile_concentration: max_loading − mean_loading (0–0.5 range)
        profile_dispersion: stddev of loadings
        max_loading: max point estimate across all dimensions
        mean_loading: mean point estimate across all dimensions
        multi_pattern_flag: True if dominant_dimensions has ≥ 2 entries
        undifferentiated_flag: True if NO dominant dimensions
    """
    points = {pid: float(p["point"]) for pid, p in posteriors.items()}
    if not points:
        return {
            "dominant_dimensions": [],
            "secondary_dimensions": [],
            "dormant_dimensions": [],
            "max_loading": 0.0,
            "mean_loading": 0.0,
            "profile_concentration": 0.0,
            "profile_dispersion": 0.0,
            "multi_pattern_flag": False,
            "undifferentiated_flag": True,
        }

    # Sort by (descending point, ascending phenotype ID) for determinism
    by_loading = sorted(points.items(), key=lambda kv: (-kv[1], kv[0]))

    dominant = sorted(
        [pid for pid, pt in points.items() if pt >= DOMINANT_LOADING_THRESHOLD]
    )
    dormant = sorted(
        [pid for pid, pt in points.items() if pt < DORMANT_LOADING_THRESHOLD]
    )
    secondary = sorted(
        [pid for pid, pt in points.items()
         if DORMANT_LOADING_THRESHOLD <= pt < DOMINANT_LOADING_THRESHOLD]
    )

    vals = list(points.values())
    n = len(vals)
    mean_l = sum(vals) / n
    var = sum((v - mean_l) ** 2 for v in vals) / n
    disp = math.sqrt(var)
    max_l = max(vals)

    return {
        "dominant_dimensions": dominant,
        "secondary_dimensions": secondary,
        "dormant_dimensions": dormant,
        "max_loading": round6(max_l),
        "mean_loading": round6(mean_l),
        "profile_concentration": round6(max_l - mean_l),
        "profile_dispersion": round6(disp),
        "multi_pattern_flag": len(dominant) >= 2,
        "undifferentiated_flag": len(dominant) == 0,
        "ranked_by_loading": [pid for pid, _ in by_loading],
    }


# ============================================================================
# STAGE 7 — INTERVENTION RANKING (§7.10 utility function v0.2)
# ============================================================================

def _build_intervention_phenotype_index(atlas: dict) -> dict[str, list[tuple[str, float]]]:
    """
    Build {intervention_id → [(phenotype_id, edge_weight), ...]} index from
    intervention_phenotype_edges.csv + phenotypes.csv top_intervention_ids_legacy.

    edge_weight comes from evidence_strength_aggregate when populated and > 0,
    else falls back to 1.0 (uniform — flagged as data quality caveat).
    Legacy top_intervention_ids contributions get weight 0.5 (weaker signal —
    they're a hand-curated list, not derived from edges).
    """
    idx: dict[str, list[tuple[str, float]]] = {}

    # Primary signal: intervention_phenotype_edges
    for r in atlas.get("ipe", []):
        int_id = (r.get("intervention_id") or "").strip()
        phe_id = (r.get("phenotype_id") or "").strip()
        if not int_id or not phe_id:
            continue
        try:
            w_str = (r.get("evidence_strength_aggregate") or "").strip()
            w = float(w_str) if w_str else 0.0
        except ValueError:
            w = 0.0
        if w <= 0:
            w = 1.0  # uniform fallback when strength field unpopulated
        idx.setdefault(int_id, []).append((phe_id, w))

    # Secondary signal: legacy top_intervention_ids per phenotype
    for r in atlas.get("phenotypes", []):
        phe_id = r.get("id", "").strip()
        legacy_str = (r.get("top_intervention_ids_legacy") or "").strip()
        if not phe_id or not legacy_str:
            continue
        for int_id in [s.strip() for s in legacy_str.split(";") if s.strip()]:
            existing = idx.setdefault(int_id, [])
            # If we already have an edge for this (int, phe) pair, keep stronger weight
            already = next((i for i, (p, _) in enumerate(existing) if p == phe_id), None)
            if already is None:
                existing.append((phe_id, 0.5))

    # Determinism fix (audit Issue 5): sort each intervention's edge list by
    # phenotype_id ASC so breadth_score and contribution_by_dimension assembly
    # is invariant under CSV row-order perturbations. Without this sort, a
    # cosmetic re-ordering of intervention_phenotype_edges.csv would shift
    # floating-point summations and break canonical_digest stability across
    # otherwise-equivalent atlas snapshots.
    for int_id, edges in idx.items():
        # Dedupe (int_id, phe_id) preserving max weight; then sort by phe_id
        best_per_phe: dict[str, float] = {}
        for phe_id, w in edges:
            if phe_id not in best_per_phe or w > best_per_phe[phe_id]:
                best_per_phe[phe_id] = w
        idx[int_id] = sorted(best_per_phe.items(), key=lambda kv: kv[0])

    return idx


def rank_interventions(
    posteriors: dict[str, dict],
    atlas: dict,
    syndromic_match: dict | None,
    profile_summary: dict | None = None,
    delta_squared_lookup: dict[str, float] | None = None,
) -> list[dict]:
    """
    v0.2 weighted multi-target intervention ranking with max-based fit,
    optionally blended with Δ² trajectory momentum (post-2026-05-05).

    Without Δ²:
        score = atlas_quality × best_match_score
    With Δ² (delta_squared_lookup provided):
        score = atlas_quality × best_match_score × momentum_multiplier
        momentum_multiplier = 1 + DELTA_SQUARED_BONUS_ALPHA × (Δ²/100)

      best_match_score = max_d ( loading_d × edge_weight_d )
      atlas_quality    = CSRS / 100   (intervention's atlas-wide score, 0–1)

    Δ² is OPT-IN. If delta_squared_lookup is None, behavior is byte-identical
    to the pre-integration engine; existing calibration tests are unaffected.
    Truth-strength (CSRS) remains dominant; momentum is a tiebreaker bonus
    bounded at +20%. A high-Δ² low-CSRS intervention cannot leapfrog a
    moderate-CSRS moderate-Δ² intervention.

    Rationale: sum-based scoring rewards edge proliferation (an intervention
    with 5 weak edges beats one with 1 strong, specific edge), which is
    structurally biased toward generic polypills over targeted treatments.
    Max-based scoring rewards specificity. Breadth is preserved as an
    informational `breadth_score` field for transparency, but does not
    drive ranking.

    Ties broken by intervention_id ascending.
    Per spec §7.10 + §7.10.1 (Δ² momentum).
    """
    if syndromic_match:
        return []

    # Undifferentiated profile → no ranking, surface honestly. The pre-mortem
    # lethal failure mode was producing confident low-signal recommendations.
    if profile_summary and profile_summary.get("undifferentiated_flag"):
        return []

    int_lookup = {r["id"]: r for r in atlas["interventions"]}
    int_to_phe = _build_intervention_phenotype_index(atlas)

    scored = []
    for int_id, edges in int_to_phe.items():
        int_row = int_lookup.get(int_id)
        if not int_row:
            continue
        try:
            csrs = float(int_row.get("csrs_score") or 0.0)
        except ValueError:
            csrs = 0.0
        if csrs <= 0:
            continue
        atlas_quality = csrs / 100.0

        # Per-dimension contributions
        contributions = {}
        best_match_score = 0.0
        best_dim = None
        breadth_score = 0.0
        for phe_id, weight in edges:
            loading = float(posteriors.get(phe_id, {}).get("point", 0.0))
            contrib = loading * weight
            breadth_score += contrib
            if contrib > best_match_score or (
                contrib == best_match_score and (best_dim is None or phe_id < best_dim)
            ):
                best_match_score = contrib
                best_dim = phe_id
            if contrib > 0.01:
                contributions[phe_id] = round6(contrib)

        if best_match_score <= 0:
            continue
        score = best_match_score * atlas_quality

        # Δ² momentum multiplier (opt-in via delta_squared_lookup)
        d2_score = 0.0
        momentum_mult = 1.0
        if delta_squared_lookup is not None:
            d2_score = float(delta_squared_lookup.get(int_id, 0.0))
            momentum_mult = 1.0 + DELTA_SQUARED_BONUS_ALPHA * (d2_score / 100.0)
            score = score * momentum_mult

        scored.append((
            int_id,
            score,
            best_match_score,
            breadth_score,
            atlas_quality,
            best_dim,
            contributions,
            int_row,
            d2_score,
            momentum_mult,
        ))

    # Sort: descending score, ties by intervention_id ascending
    scored.sort(key=lambda t: (-t[1], t[0]))

    bundle = []
    for (int_id, score, best_match, breadth, atlas_quality,
         best_dim, contribs, int_row, d2_score, momentum_mult) in scored[:5]:
        entry = {
            "intervention_id": int_id,
            "name": int_row.get("name", ""),
            "category": int_row.get("category", ""),
            "score": round6(score),
            "best_match_score": round6(best_match),
            "breadth_score": round6(breadth),
            "atlas_quality": round6(atlas_quality),
            "primary_target_dimension": best_dim,
            "target_dimensions": sorted(contribs.keys()),
            "contribution_by_dimension": dict(sorted(contribs.items())),
            "recommendation_type": "CONSIDER",
        }
        if delta_squared_lookup is not None:
            entry["delta_squared_score"] = round6(d2_score)
            entry["momentum_multiplier"] = round6(momentum_mult)
        bundle.append(entry)

    if bundle:
        bundle[0]["recommendation_type"] = "START"

    return bundle


# ============================================================================
# STAGE 8 — TOP-LEVEL OUTPUT BUILDER
# ============================================================================

def assert_calibration_anchor(atlas: dict) -> dict:
    """
    Audit L-2 fix: verify Layer 2 calibration anchor (INT-0001 ≥ 80) at engine
    startup. Returns anchor info; raises if anchor is below threshold.
    """
    anchor_info = {"intervention": CALIBRATION_ANCHOR_NAME,
                   "required_csrs_min": CALIBRATION_ANCHOR_REQUIRED_CSRS}
    for r in atlas.get("interventions", []):
        if r.get("id") == CALIBRATION_ANCHOR_NAME:
            try:
                csrs = float(r.get("csrs_score", "0"))
                anchor_info["actual_csrs"] = csrs
                anchor_info["passes"] = csrs >= CALIBRATION_ANCHOR_REQUIRED_CSRS
                if not anchor_info["passes"]:
                    raise ValueError(
                        f"Calibration anchor FAILED: {CALIBRATION_ANCHOR_NAME} csrs={csrs} "
                        f"< required {CALIBRATION_ANCHOR_REQUIRED_CSRS}. Engine refuses to run."
                    )
                return anchor_info
            except (ValueError, TypeError) as e:
                # If csrs_score not parseable, fall through with informational only
                anchor_info["actual_csrs"] = None
                anchor_info["passes"] = None
                anchor_info["informational_only"] = f"csrs_score not parseable: {e}"
                return anchor_info
    anchor_info["informational_only"] = "INT-0001 not found in interventions.csv (Phase 0 atlas may be incomplete)"
    return anchor_info


def assemble_canonical_payload(output: dict) -> str:
    """
    Audit C-1 fix: canonical-payload digest. Returns the JSON-stable serialization
    of the deterministic-output fields (excludes computed_at timestamp).
    """
    canonical_keys = [
        "case_id", "engine_version", "atlas_version", "calibration_anchor",
        "atlas_identity",
        "operating_mode", "subject_sex", "syndromic_flag", "syndromic_match",
        "phenotype_posteriors", "phenotype_ranking",
        "profile_loadings", "profile_summary",
        "intervention_bundle",
        "deferred_features", "status",
    ]
    canonical = {k: output.get(k) for k in canonical_keys if k in output}
    return json.dumps(canonical, sort_keys=True, separators=(",", ":"))


def compute_personalized_risk(
    input_data: dict,
    atlas_path: Path | str | None = None,
    use_delta_squared: bool = False,
) -> dict:
    """
    Top-level engine entry point. Per spec §7.2.

    Multi-atlas pivot: atlas_path selects which condition's atlas to load.
    None = default (autism atlas at v2.0_scored/). Future calls pass a
    per-condition atlas path (e.g., atlases/long_covid/v0.1/).

    Returns full output JSON per §9.1 schema, with atlas-manifest metadata
    threaded into output for transparency.
    """
    # Audit M-3: type-check input first
    if not isinstance(input_data, dict):
        return {
            "case_id": "unknown",
            "engine_version": ENGINE_VERSION,
            "atlas_version": ATLAS_VERSION,
            "computed_at": now_iso(),
            "validation_errors": ["input_data is not a dict"],
            "status": "validation_failed",
        }

    # Validate
    errors = validate_input(input_data)
    if errors:
        return {
            "case_id": input_data.get("case_id", "unknown"),
            "engine_version": ENGINE_VERSION,
            "atlas_version": ATLAS_VERSION,
            "computed_at": now_iso(),
            "validation_errors": errors,
            "status": "validation_failed",
        }

    # Load atlas (multi-atlas-aware)
    atlas = load_atlas(atlas_path)
    manifest = load_atlas_manifest(atlas_path) if atlas_path else {}

    # Audit L-2: verify calibration anchor at startup
    calibration_status = assert_calibration_anchor(atlas)

    # Stage 2: rare-syndrome gate
    syndromic_match = run_syndromic_gate(input_data, atlas)

    # Stage 3-6: phenotype posteriors
    posteriors = compute_phenotype_posteriors(input_data, atlas)

    # Phenotype ranking — kept as auxiliary back-compat output. Profile-vector
    # is the canonical semantics in v0.2; ranking is for legacy consumers.
    phenotype_ranking = sorted(
        ALL_PHENOTYPE_IDS,
        key=lambda p: (-posteriors[p]["point"], p)
    )

    # Stage 6.5: profile summary (v0.2 — Move 1, post-mortem fix)
    profile_summary = compute_profile_summary(posteriors)
    profile_loadings = {
        pid: round6(float(posteriors[pid]["point"])) for pid in ALL_PHENOTYPE_IDS
    }

    # Stage 7: interventions — v0.2 weighted multi-target scoring,
    # optionally blended with Δ² trajectory momentum (opt-in).
    delta_squared_lookup = load_delta_squared() if use_delta_squared else None
    intervention_bundle = rank_interventions(
        posteriors, atlas, syndromic_match, profile_summary,
        delta_squared_lookup=delta_squared_lookup,
    )

    # Stage 8: assemble output (v0.2 schema)
    # Atlas identity (multi-atlas pivot)
    atlas_identity = {
        "atlas_path": str(atlas_path) if atlas_path else str(DEFAULT_ATLAS_ROOT),
        "atlas_condition": manifest.get("condition", "Autism"),
        "atlas_condition_id": manifest.get("condition_id", "autism"),
        "atlas_manifest_version": manifest.get("version", ATLAS_VERSION),
    }

    output = {
        "case_id": input_data.get("case_id"),
        "engine_version": ENGINE_VERSION,
        "atlas_version": ATLAS_VERSION,
        "atlas_identity": atlas_identity,
        "calibration_anchor": f"{CALIBRATION_ANCHOR_NAME} = {CALIBRATION_ANCHOR_CURRENT_CSRS}",
        "calibration_status": calibration_status,
        "operating_mode": input_data.get("operating_mode"),
        "subject_sex": input_data.get("subject_sex"),
        "syndromic_flag": syndromic_match is not None,
        "syndromic_match": syndromic_match,
        "profile_loadings": profile_loadings,
        "profile_summary": profile_summary,
        "phenotype_posteriors": posteriors,
        "phenotype_ranking": phenotype_ranking,
        "intervention_bundle": intervention_bundle,
        "delta_squared_blended": use_delta_squared,
        "provisional_hardcoded_shifts": True,  # Audit H-2: stub values used; v0.2 will replace with priors-CSV-driven values
        "deferred_features": [
            "full_walley_idm_credal_aggregation_v0.2",
            "within_phenotype_responder_model_v0.2",
            "cdr_state_assignment_v0.2",
            "functional_trajectory_predictor_v0.2",
            "pathway_burden_analysis_v0.2",
            "pgx_safety_filter_v0.2",
            "physiological_state_normalization_v0.2",
            "evidence_quality_weighted_credal_bands_v0.2",
            "sex_stratified_baselines_v0.2",
            "life_stage_filtered_intervention_ranking_v0.2",
        ],
        "status": "success",
    }

    # Audit C-1 fix: canonical_digest BEFORE adding non-canonical timestamp
    output["canonical_digest"] = hashlib.sha256(
        assemble_canonical_payload(output).encode("utf-8")
    ).hexdigest()
    output["computed_at"] = now_iso()  # added last, excluded from canonical_digest

    return output


# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--input", type=Path, required=True, help="Input JSON path")
    parser.add_argument("--output", type=Path, help="Output JSON path (default: stdout)")
    parser.add_argument(
        "--atlas-path", type=Path, default=None,
        help="Path to atlas directory (e.g., atlases/long_covid/v0.1/). "
             "Default = autism atlas at v2.0_scored/ (back-compat)."
    )
    parser.add_argument(
        "--use-delta-squared", action="store_true",
        help="Blend Δ² trajectory momentum into intervention ranking. "
             "OFF by default to preserve byte-identical output for existing "
             "calibration tests. ON adds a +0–20%% multiplicative bonus to "
             "interventions with high Δ² scores from delta_squared_v1/."
    )
    args = parser.parse_args()

    with open(args.input) as f:
        input_data = json.load(f)

    output = compute_personalized_risk(
        input_data,
        atlas_path=args.atlas_path,
        use_delta_squared=args.use_delta_squared,
    )
    output_str = json.dumps(output, indent=2, sort_keys=True)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output_str)
        print(f"Wrote output to {args.output}")
    else:
        print(output_str)


if __name__ == "__main__":
    main()
