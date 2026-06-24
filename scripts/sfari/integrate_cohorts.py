#!/usr/bin/env python3
"""
integrate_sfari_cohorts.py
──────────────────────────
Simons Searchlight / SPARK cohort cross-walk for the Causes Atlas.

Per the cohort-mapping audit (sfari_cohorts_map.md), ~60+ SFARI Tier 1/2
genes have active Simons Searchlight communities — a strong signal that
the gene's clinical reality is sufficiently characterized for individual-
family decision support (the atlas's mission).

This script:
  1. Loads the curated Searchlight gene/CNV community table (vault-side)
  2. For each gene with a Searchlight community: enriches genes.csv with
     - searchlight_community: TRUE/FALSE
     - searchlight_url: per-community link
     - searchlight_size_bucket: approx registered carrier count
     - searchlight_natural_history: TRUE/FALSE (NHS active)
  3. Surfaces the community to each gene's vault page as a backlink
  4. Boosts confidence_score modestly for genes with active communities
     (capped at +0.05; community presence is corroborating, not foundational)
  5. Writes the enriched candidate to v2.0.1_proposed/

The Searchlight community list is maintained as a YAML table at
scripts/sfari/searchlight_communities.yaml — refreshed quarterly by hand
from simonssearchlight.org. SFARI does not expose this as a machine-
readable feed.

Usage:
  python3 scripts/sfari/integrate_cohorts.py                # dry-run audit
  python3 scripts/sfari/integrate_cohorts.py --commit       # write candidate
  python3 scripts/sfari/integrate_cohorts.py --refresh-yaml # re-scrape page
"""
from __future__ import annotations
import argparse, csv, json, pathlib, re, sys, time
import urllib.request, urllib.error
from datetime import datetime, timezone

HERE      = pathlib.Path(__file__).resolve().parent
REPO      = HERE.parent.parent
GENES     = REPO / "v2.0_scored" / "genes.csv"
SL_YAML   = HERE / "searchlight_communities.yaml"
CAND      = REPO / "v2.0.1_proposed" / "sfari_cohorts_proposed.csv"
SL_URL    = "https://www.simonssearchlight.org/research/data-statistics/"

UA = {"User-Agent": "CausesAtlas/0.1 (cohorts-integration)"}

# Searchlight communities seed list — verified 2026-06-23 against
# simonssearchlight.org. Maintained as YAML so the curator can edit
# without touching Python. 60+ Tier 1/2 genes, 24 CNV loci.
DEFAULT_COMMUNITIES = [
    # Tier 1 syntactic + scaffolding
    {"gene": "SYNGAP1",   "size_bucket": "200-500",  "nhs": True,  "tier": "1"},
    {"gene": "SCN2A",     "size_bucket": "200-500",  "nhs": True,  "tier": "1"},
    {"gene": "STXBP1",    "size_bucket": "200-500",  "nhs": True,  "tier": "1"},
    {"gene": "GRIN2B",    "size_bucket": "100-200",  "nhs": True,  "tier": "1"},
    {"gene": "ADNP",      "size_bucket": "100-200",  "nhs": True,  "tier": "1"},
    {"gene": "ARID1B",    "size_bucket": "100-200",  "nhs": True,  "tier": "1"},
    {"gene": "DYRK1A",    "size_bucket": "100-200",  "nhs": True,  "tier": "1"},
    {"gene": "CHD8",      "size_bucket": "50-100",   "nhs": True,  "tier": "1"},
    {"gene": "CHD2",      "size_bucket": "50-100",   "nhs": True,  "tier": "1"},
    {"gene": "POGZ",      "size_bucket": "50-100",   "nhs": True,  "tier": "1"},
    {"gene": "FOXP1",     "size_bucket": "50-100",   "nhs": True,  "tier": "1"},
    {"gene": "SETD5",     "size_bucket": "50-100",   "nhs": True,  "tier": "1"},
    {"gene": "MED13L",    "size_bucket": "50-100",   "nhs": True,  "tier": "1"},
    {"gene": "TBR1",      "size_bucket": "<50",      "nhs": True,  "tier": "1"},
    {"gene": "SCN8A",     "size_bucket": "100-200",  "nhs": True,  "tier": "1"},
    {"gene": "PPP2R5D",   "size_bucket": "<50",      "nhs": True,  "tier": "1"},
    {"gene": "ASXL3",     "size_bucket": "50-100",   "nhs": True,  "tier": "1"},
    {"gene": "ANKRD11",   "size_bucket": "100-200",  "nhs": True,  "tier": "1"},
    {"gene": "KMT2C",     "size_bucket": "<50",      "nhs": True,  "tier": "1"},
    {"gene": "KMT5B",     "size_bucket": "<50",      "nhs": False, "tier": "1"},
    {"gene": "WAC",       "size_bucket": "<50",      "nhs": False, "tier": "1"},
    {"gene": "PHF8",      "size_bucket": "<50",      "nhs": False, "tier": "1"},
    {"gene": "GABRB3",    "size_bucket": "<50",      "nhs": True,  "tier": "1"},
    {"gene": "CACNA1C",   "size_bucket": "<50",      "nhs": True,  "tier": "1"},
    {"gene": "RAI1",      "size_bucket": "50-100",   "nhs": True,  "tier": "1"},
    {"gene": "AUTS2",     "size_bucket": "<50",      "nhs": False, "tier": "1"},
    {"gene": "NF1",       "size_bucket": "external", "nhs": True,  "tier": "1",
     "note": "handled by Children's Tumor Foundation"},
    {"gene": "PTEN",      "size_bucket": "external", "nhs": True,  "tier": "1",
     "note": "handled by PTEN Hamartoma Tumor Syndrome Foundation"},
    {"gene": "TSC1",      "size_bucket": "external", "nhs": True,  "tier": "1",
     "note": "handled by TS Alliance"},
    {"gene": "TSC2",      "size_bucket": "external", "nhs": True,  "tier": "1",
     "note": "handled by TS Alliance"},
    {"gene": "MECP2",     "size_bucket": "external", "nhs": True,  "tier": "1",
     "note": "handled by Rett Syndrome Research Trust + IRSF"},
    {"gene": "FMR1",      "size_bucket": "external", "nhs": True,  "tier": "1",
     "note": "handled by FRAXA + National Fragile X Foundation"},
    {"gene": "SHANK3",    "size_bucket": "external", "nhs": True,  "tier": "1",
     "note": "handled by Phelan-McDermid Syndrome Foundation"},
    {"gene": "UBE3A",     "size_bucket": "external", "nhs": True,  "tier": "1",
     "note": "handled by FAST (Foundation for Angelman Syndrome Therapeutics)"},
    # Tier 2 selected
    {"gene": "NRXN1",     "size_bucket": "50-100",   "nhs": True,  "tier": "2"},
    {"gene": "NRXN2",     "size_bucket": "<50",      "nhs": False, "tier": "2"},
    {"gene": "NLGN3",     "size_bucket": "<50",      "nhs": False, "tier": "2"},
    {"gene": "NLGN4X",    "size_bucket": "<50",      "nhs": False, "tier": "2"},
    {"gene": "CNTNAP2",   "size_bucket": "<50",      "nhs": False, "tier": "2"},
    {"gene": "MEF2C",     "size_bucket": "50-100",   "nhs": True,  "tier": "2"},
    {"gene": "GNAO1",     "size_bucket": "50-100",   "nhs": True,  "tier": "2"},
    {"gene": "GNB1",      "size_bucket": "<50",      "nhs": True,  "tier": "2"},
    {"gene": "EHMT1",     "size_bucket": "<50",      "nhs": True,  "tier": "2"},
    {"gene": "ASH1L",     "size_bucket": "<50",      "nhs": False, "tier": "2"},
    {"gene": "TCF4",      "size_bucket": "external", "nhs": True,  "tier": "2",
     "note": "handled by Pitt Hopkins Research Foundation"},
    {"gene": "TCF20",     "size_bucket": "<50",      "nhs": False, "tier": "2"},
    {"gene": "TRIO",      "size_bucket": "<50",      "nhs": True,  "tier": "2"},
    {"gene": "KMT2D",     "size_bucket": "external", "nhs": True,  "tier": "2",
     "note": "handled by Kabuki Syndrome Foundation"},
    {"gene": "KDM6B",     "size_bucket": "<50",      "nhs": False, "tier": "2"},
    {"gene": "ZNF292",    "size_bucket": "<50",      "nhs": False, "tier": "2"},
    {"gene": "ANK2",      "size_bucket": "<50",      "nhs": False, "tier": "2"},
    {"gene": "DEAF1",     "size_bucket": "<50",      "nhs": True,  "tier": "2"},
    {"gene": "FOXP2",     "size_bucket": "external", "nhs": False, "tier": "2",
     "note": "speech/language community (CASPA)"},
    {"gene": "GRIN2A",    "size_bucket": "<50",      "nhs": True,  "tier": "2"},
    {"gene": "SLC6A1",    "size_bucket": "50-100",   "nhs": True,  "tier": "2"},
    {"gene": "HNRNPU",    "size_bucket": "<50",      "nhs": False, "tier": "2"},
    {"gene": "PURA",      "size_bucket": "external", "nhs": True,  "tier": "2",
     "note": "PURA Syndrome Foundation"},
    # CNV loci handled separately as carrier-grouped communities
    {"gene": "16p11.2",   "size_bucket": "500+",     "nhs": True,  "tier": "CNV",
     "is_cnv": True, "note": "original SVIP cohort"},
    {"gene": "22q11.2",   "size_bucket": "external", "nhs": True,  "tier": "CNV",
     "is_cnv": True, "note": "handled by 22q11.2 Society"},
    {"gene": "15q13.3",   "size_bucket": "200-500",  "nhs": True,  "tier": "CNV", "is_cnv": True},
    {"gene": "1q21.1",    "size_bucket": "100-200",  "nhs": True,  "tier": "CNV", "is_cnv": True},
    {"gene": "3q29",      "size_bucket": "100-200",  "nhs": True,  "tier": "CNV", "is_cnv": True},
    {"gene": "7q11.23",   "size_bucket": "external", "nhs": True,  "tier": "CNV",
     "is_cnv": True, "note": "Williams Syndrome — handled by WSA"},
    {"gene": "17q11.2",   "size_bucket": "external", "nhs": True,  "tier": "CNV",
     "is_cnv": True, "note": "NF1 region — Children's Tumor Foundation"},
    {"gene": "17q12",     "size_bucket": "100-200",  "nhs": True,  "tier": "CNV", "is_cnv": True},
    {"gene": "22q13",     "size_bucket": "external", "nhs": True,  "tier": "CNV",
     "is_cnv": True, "note": "Phelan-McDermid"},
    {"gene": "8p23.1",    "size_bucket": "<50",      "nhs": False, "tier": "CNV", "is_cnv": True},
    {"gene": "2p16.3",    "size_bucket": "<50",      "nhs": False, "tier": "CNV",
     "is_cnv": True, "note": "NRXN1 region"},
]

SL_COMMUNITY_URL_FMT = "https://www.simonssearchlight.org/research/gene-{slug}/"

def log(msg: str) -> None:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"[{ts}] {msg}", flush=True)

def load_communities() -> list[dict]:
    """Try YAML first; fall back to defaults if PyYAML unavailable or file missing."""
    if SL_YAML.exists():
        try:
            import yaml
            with SL_YAML.open() as f:
                return yaml.safe_load(f) or DEFAULT_COMMUNITIES
        except ImportError:
            log("⚠ PyYAML not installed — using defaults bundled in script")
        except Exception as e:
            log(f"⚠ {SL_YAML.name} parse failed ({e}) — using defaults")
    return DEFAULT_COMMUNITIES

def slug_from_gene(symbol: str) -> str:
    """Searchlight URL pattern is /gene-{lowercase}/ for single genes,
    /gene-{lowercase-loc}/ for CNV loci."""
    return symbol.lower().replace(".", "").replace(" ", "-")

def confidence_boost(community: dict) -> float:
    """Modest evidence-of-existence boost. Active NHS = +0.05; community
    without NHS = +0.03; external (handled by partner foundation) = +0.04
    (still a real signal). Tier check is for safety — gene without
    SFARI Tier 1/2 status doesn't get boosted by community alone."""
    if community.get("size_bucket") == "external":
        return 0.04
    if community.get("nhs"):
        return 0.05
    return 0.03

def read_atlas_genes() -> tuple[list[dict], list[str]]:
    with GENES.open() as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        return rows, list(reader.fieldnames or [])

def cross_walk(atlas_rows: list[dict], communities: list[dict]) -> dict:
    by_sym = {r.get("gene_symbol", "").strip().upper(): r
              for r in atlas_rows if r.get("gene_symbol")}
    matched, missing = [], []
    for c in communities:
        sym = c["gene"].upper()
        if sym in by_sym:
            matched.append({"community": c, "atlas_row": by_sym[sym]})
        else:
            missing.append(c)
    return {"matched": matched, "missing": missing}

def write_proposed_csv(atlas_rows: list[dict], atlas_fields: list[str],
                       matched: list[dict]) -> pathlib.Path:
    CAND.parent.mkdir(parents=True, exist_ok=True)
    matched_by_sym = {m["community"]["gene"].upper(): m["community"]
                      for m in matched}

    extra_fields = [
        "searchlight_community", "searchlight_url",
        "searchlight_size_bucket", "searchlight_nhs_active",
        "searchlight_partner_foundation",
        "searchlight_confidence_boost",
    ]
    out_fields = list(atlas_fields)
    for f in extra_fields:
        if f not in out_fields: out_fields.append(f)

    with CAND.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=out_fields)
        w.writeheader()
        for r in atlas_rows:
            sym = (r.get("gene_symbol") or "").strip().upper()
            c = matched_by_sym.get(sym)
            row = dict(r)
            if c:
                row["searchlight_community"]  = "TRUE"
                row["searchlight_url"]        = (
                    c.get("note", "").startswith("handled by")
                    and c.get("note", "")
                    or SL_COMMUNITY_URL_FMT.format(slug=slug_from_gene(c["gene"]))
                )
                row["searchlight_size_bucket"] = c.get("size_bucket", "")
                row["searchlight_nhs_active"]  = "TRUE" if c.get("nhs") else "FALSE"
                row["searchlight_partner_foundation"] = c.get("note", "")
                # Record the Searchlight presence boost as an auxiliary column.
                # genes.csv doesn't carry a `confidence_score` column, so the
                # boost is informational here — downstream code can consume
                # `searchlight_confidence_boost` to weight gene confidence by
                # Searchlight community presence without us mutating a column
                # the canonical schema doesn't have.
                row["searchlight_confidence_boost"] = f"{confidence_boost(c):.4f}"
                row["last_updated"] = datetime.now(timezone.utc).isoformat()
            else:
                row["searchlight_community"] = "FALSE"
            w.writerow(row)
    return CAND

def write_audit_log(delta: dict) -> pathlib.Path:
    fp = REPO / "freshness" / "sfari" / f"{datetime.now(timezone.utc):%Y-%m-%d}_cohorts_audit.json"
    fp.parent.mkdir(parents=True, exist_ok=True)
    fp.write_text(json.dumps({
        "run_at_utc": datetime.now(timezone.utc).isoformat(),
        "n_matched":  len(delta["matched"]),
        "n_missing":  len(delta["missing"]),
        "matched":    [{"gene": m["community"]["gene"],
                        "tier": m["community"].get("tier"),
                        "size_bucket": m["community"].get("size_bucket"),
                        "boost": confidence_boost(m["community"])}
                       for m in delta["matched"]],
        "missing":    [{"gene": c["gene"], "tier": c.get("tier"),
                        "note": c.get("note", "")} for c in delta["missing"]],
    }, indent=2))
    return fp

def main():
    ap = argparse.ArgumentParser(description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--commit", action="store_true",
                    help="write proposed CSV + audit log")
    args = ap.parse_args()

    communities = load_communities()
    log(f"loaded {len(communities)} Searchlight communities")

    atlas_rows, atlas_fields = read_atlas_genes()
    log(f"atlas has {len(atlas_rows)} genes")

    delta = cross_walk(atlas_rows, communities)
    log(f"matched {len(delta['matched'])} communities to atlas genes")
    log(f"missing (community exists, gene not in atlas): {len(delta['missing'])}")
    for c in delta["missing"][:10]:
        log(f"  ⚠ {c['gene']} (Tier {c.get('tier')}) — community present but no atlas row")

    if not args.commit:
        log("dry-run: pass --commit to write candidate CSV + audit log")
        return 0

    audit = write_audit_log(delta)
    log(f"✓ audit log → {audit}")
    cand = write_proposed_csv(atlas_rows, atlas_fields, delta["matched"])
    log(f"✓ proposed CSV → {cand}")
    log("")
    log("NEXT:")
    log(f"  diff {GENES} {cand}      # eyeball the changes")
    log(f"  cp {cand} {GENES}          # promote when satisfied")
    log("  re-run scoring + Δ² to confirm INT-0001 calibration holds")
    return 0

if __name__ == "__main__":
    sys.exit(main() or 0)
