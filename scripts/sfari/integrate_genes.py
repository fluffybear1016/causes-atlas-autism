#!/usr/bin/env python3
"""
integrate_sfari_genes.py
────────────────────────
SFARI Gene database integration for the Causes Atlas.

The atlas's gene layer was last refreshed 2026-04-24. SFARI Gene Q1 2026
(released 2026-05-01) added 174 net Tier-1+2 genes and introduced the EAGLE
scoring system. This script refreshes the canonical gene table and surfaces
deltas for review per the §24 verification protocol.

Sources (verified live 2026-06-23):
  Gene scores:   https://gene.sfari.org/.../download-csv.php?api-endpoint=genes
  Animal models: https://gene.sfari.org/.../download-csv.php?api-endpoint=animal-genes
  CNVs:          https://gene.sfari.org/.../download-csv.php?api-endpoint=cnvs

What this script does:
  1. Downloads the latest SFARI Gene CSV (1,277 rows as of Q1 2026)
  2. Cross-walks by gene_symbol to v2.0_scored/genes.csv (1,564 atlas rows)
  3. Computes delta: score changes, new SFARI entries, atlas-only genes
  4. Writes delta report to freshness/sfari/YYYY-MM-DD_sfari_delta.json
  5. Writes NEW genes to Discoveries_Inbox/SFARI-{symbol}.md for human triage
  6. Writes a candidate updated_genes.csv with added columns:
       ensembl_id (canonical, replacing legacy)
       sfari_chromosome
       sfari_genetic_category   (multi-valued; pipe-delimited)
       sfari_syndromic_flag     (Boolean, separated from numeric score)
       sfari_eagle_score        (float; new Schaaf-2020 ClinGen-derived signal)
       sfari_number_of_reports  (int; evidence count)
       sfari_quarter            (YYYY-Qn release tag)
       sfari_url                (per-gene deep-link)
  7. Does NOT auto-promote anything to v2.0_scored/genes.csv — human approval
     gate enforced via apply-flag pattern, identical to run_ingest.py.

Calibration safety: re-densifying the Tier-1+2 → HYP-0028 polygenic edges
is left to densify_gene_layer.py running after this script. Calibration
regression (INT-0001 < 80) halts the autonomous loop downstream.

Determinism: stable sort by gene_symbol throughout; no random seeds.

Usage:
  python3 scripts/sfari/integrate_genes.py                  # dry-run audit
  python3 scripts/sfari/integrate_genes.py --commit         # write candidates
  python3 scripts/sfari/integrate_genes.py --apply          # promote to canonical
"""
from __future__ import annotations
import argparse, csv, hashlib, json, pathlib, re, sys
import urllib.request, urllib.error
from datetime import datetime, timezone

HERE     = pathlib.Path(__file__).resolve().parent
REPO     = HERE.parent.parent
GENES    = REPO / "v2.0_scored" / "genes.csv"
FRESH    = REPO / "freshness" / "sfari"
INBOX    = REPO / "vault" / "Discoveries_Inbox"
RAW_DIR  = REPO / "raw" / "sfari"
CAND     = REPO / "v2.0.1_proposed" / "sfari_genes_proposed.csv"

SFARI_CSV_URL = "https://gene.sfari.org/wp-content/themes/sfari-gene/utilities/download-csv.php?api-endpoint=genes"
SFARI_GENE_URL_FMT = "https://gene.sfari.org/database/human-gene/{symbol}"
ATTRIBUTION = ("SFARI Gene © Simons Foundation Autism Research Initiative. "
               "Source data public-domain; curation attributed.")

def log(msg: str) -> None:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"[{ts}] {msg}", flush=True)

def fetch_sfari_csv() -> bytes:
    """Pull the SFARI Gene CSV. Treat outages as soft failures."""
    req = urllib.request.Request(SFARI_CSV_URL,
            headers={"User-Agent": "CausesAtlas/0.1 (atlas-loop@sfari-integration)"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read()
    except (urllib.error.URLError, TimeoutError) as e:
        log(f"⚠ SFARI fetch failed: {e}")
        raise SystemExit(2)

def detect_quarter() -> str:
    """Best-effort SFARI release quarter tag from current date.
    SFARI publishes quarterly: Q1 late Apr/May, Q2 late Jul/Aug,
    Q3 late Oct/Nov, Q4 mid-Jan."""
    now = datetime.now(timezone.utc)
    y, m = now.year, now.month
    # If we're before this quarter's release window, label as previous quarter
    if   m <= 1:               return f"{y-1}-Q4"
    elif m <= 4:               return f"{y}-Q1"
    elif m <= 7:               return f"{y}-Q2"
    elif m <= 10:              return f"{y}-Q3"
    else:                      return f"{y}-Q4"

def parse_sfari_csv(raw: bytes) -> list[dict]:
    """Parse the SFARI CSV. Schema verified 2026-06-23:
        status, gene-symbol, gene-name, ensembl-id, chromosome,
        genetic-category, gene-score, syndromic, eagle, number-of-reports
    """
    text = raw.decode("utf-8", errors="replace")
    reader = csv.DictReader(text.splitlines())
    out = []
    for row in reader:
        sym = (row.get("gene-symbol") or "").strip()
        if not sym:
            continue
        out.append({
            "symbol":            sym,
            "name":              (row.get("gene-name") or "").strip(),
            "ensembl_id":        (row.get("ensembl-id") or "").strip(),
            "chromosome":        (row.get("chromosome") or "").strip(),
            "genetic_category":  (row.get("genetic-category") or "").strip(),
            "score":             (row.get("gene-score") or "").strip(),
            "syndromic":         _to_bool(row.get("syndromic")),
            "eagle":             _to_float(row.get("eagle")),
            "n_reports":         _to_int(row.get("number-of-reports")),
        })
    return sorted(out, key=lambda r: r["symbol"])

def _to_bool(v):
    if v is None: return False
    s = str(v).strip().lower()
    return s in ("1", "true", "yes", "y")

def _to_float(v):
    if v in (None, ""): return None
    try:    return float(v)
    except: return None

def _to_int(v):
    if v in (None, ""): return None
    try:    return int(float(v))
    except: return None

def read_atlas_genes() -> tuple[list[dict], list[str]]:
    with GENES.open() as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        return rows, list(reader.fieldnames or [])

def cross_walk(atlas_rows: list[dict], sfari_rows: list[dict]) -> dict:
    """Return delta object: { changed, new_in_sfari, atlas_only, unchanged }"""
    atlas_by_sym = {r.get("gene_symbol", "").strip().upper(): r
                    for r in atlas_rows if r.get("gene_symbol")}
    sfari_by_sym = {r["symbol"].upper(): r for r in sfari_rows}

    changed, unchanged, new_in_sfari, atlas_only = [], [], [], []
    for sym, s in sfari_by_sym.items():
        if sym in atlas_by_sym:
            a = atlas_by_sym[sym]
            old_score = (a.get("sfari_score") or "").strip()
            new_score = s["score"] or ("S" if s["syndromic"] and not s["score"] else "")
            if old_score != new_score:
                changed.append({"symbol": sym, "old": old_score, "new": new_score,
                                "atlas_id": a.get("id", "")})
            else:
                unchanged.append(sym)
        else:
            new_in_sfari.append(s)

    for sym, a in atlas_by_sym.items():
        if sym not in sfari_by_sym:
            old_score = (a.get("sfari_score") or "").strip()
            if old_score:  # was scored, now absent → SFARI dropped it
                atlas_only.append({"symbol": sym, "had_score": old_score,
                                   "atlas_id": a.get("id", "")})

    return {
        "changed": sorted(changed, key=lambda r: r["symbol"]),
        "new_in_sfari": sorted(new_in_sfari, key=lambda r: r["symbol"]),
        "atlas_only": sorted(atlas_only, key=lambda r: r["symbol"]),
        "n_unchanged": len(unchanged),
        "n_atlas_total": len(atlas_by_sym),
        "n_sfari_total": len(sfari_by_sym),
    }

def write_delta_report(delta: dict, raw_sha256: str, quarter: str) -> pathlib.Path:
    FRESH.mkdir(parents=True, exist_ok=True)
    fp = FRESH / f"{datetime.now(timezone.utc):%Y-%m-%d}_sfari_delta.json"
    fp.write_text(json.dumps({
        "run_at_utc":   datetime.now(timezone.utc).isoformat(),
        "sfari_quarter": quarter,
        "raw_sha256":   raw_sha256,
        "n_changed":     len(delta["changed"]),
        "n_new":         len(delta["new_in_sfari"]),
        "n_atlas_only":  len(delta["atlas_only"]),
        "n_unchanged":   delta["n_unchanged"],
        "n_atlas":       delta["n_atlas_total"],
        "n_sfari":       delta["n_sfari_total"],
        "changed":       delta["changed"][:200],
        "new":           [{"symbol": r["symbol"], "score": r["score"],
                          "name": r["name"], "n_reports": r["n_reports"]}
                         for r in delta["new_in_sfari"][:200]],
        "atlas_only":    delta["atlas_only"][:200],
        "attribution":   ATTRIBUTION,
    }, indent=2))
    return fp

def write_discoveries_inbox(new_in_sfari: list[dict], quarter: str) -> int:
    """Stub a Discoveries_Inbox/SFARI-{symbol}.md per new gene. Human-review-gated."""
    INBOX.mkdir(parents=True, exist_ok=True)
    n_written = 0
    for s in new_in_sfari:
        sym = s["symbol"]
        fp = INBOX / f"SFARI-{sym}.md"
        if fp.exists():
            continue
        url = SFARI_GENE_URL_FMT.format(symbol=sym)
        score_tag = s["score"] or ("S" if s["syndromic"] else "—")
        body = f"""---
id: DI-SFARI-{sym}
source: sfari_gene
status: pending_review
proposed_score: {score_tag}
syndromic: {s["syndromic"]}
eagle: {s["eagle"] if s["eagle"] is not None else ""}
n_reports: {s["n_reports"] if s["n_reports"] is not None else ""}
ensembl_id: {s["ensembl_id"]}
chromosome: {s["chromosome"]}
genetic_category: {s["genetic_category"]}
sfari_quarter: {quarter}
created_at: {datetime.now(timezone.utc).isoformat()}
---

# {sym} — SFARI Gene candidate

**Name:** {s["name"] or sym}
**SFARI score:** {score_tag}  (syndromic: {"yes" if s["syndromic"] else "no"})
**EAGLE score:** {s["eagle"] if s["eagle"] is not None else "—"}
**Reports:** {s["n_reports"] if s["n_reports"] is not None else "—"}
**Genetic category:** {s["genetic_category"] or "—"}
**Chromosome:** {s["chromosome"] or "—"}  ·  **Ensembl:** {s["ensembl_id"] or "—"}

[SFARI Gene evidence page →]({url})

## Triage

This gene is in SFARI Gene ({quarter}) but not yet in `v2.0_scored/genes.csv`.
For promotion to the canonical atlas, a curator should:

1. Verify the SFARI page reports actual ASD-linked evidence (template page render
   ≠ real curation — cross-check that gene-name and reports match).
2. Decide on `GEN-XXXX` ID assignment.
3. Add gene_hypothesis_edge to HYP-0028 (polygenic risk) for score 1 or 2 genes.
4. Decide whether the gene warrants a stand-alone vault page in `genes/`.

## Auto-curation prompt (Karpathy second-brain pattern)

```
Read SFARI gene page for {sym} at {url}. Summarize: what mechanism this gene
implicates, what existing atlas hypothesis it would connect to, what
intervention pages should backlink. Ground every claim with a PMID verified
via PubMed esummary per §24. File output here as "## Curator notes".
```
"""
        fp.write_text(body)
        n_written += 1
    return n_written

def write_proposed_csv(atlas_rows: list[dict], atlas_fields: list[str],
                       sfari_rows: list[dict], quarter: str) -> pathlib.Path:
    """Write a candidate updated genes.csv to v2.0.1_proposed/.
    Does NOT modify v2.0_scored/. Apply happens through apply_patches_and_score.py
    after human approval."""
    CAND.parent.mkdir(parents=True, exist_ok=True)
    sfari_by_sym = {r["symbol"].upper(): r for r in sfari_rows}
    # Add new columns at the end so existing readers don't break
    extra_fields = [
        "sfari_chromosome", "sfari_genetic_category", "sfari_syndromic_flag",
        "sfari_eagle_score", "sfari_number_of_reports", "sfari_quarter", "sfari_url",
    ]
    out_fields = list(atlas_fields)
    for f in extra_fields:
        if f not in out_fields:
            out_fields.append(f)
    with CAND.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=out_fields)
        w.writeheader()
        for r in atlas_rows:
            sym = (r.get("gene_symbol") or "").strip().upper()
            s = sfari_by_sym.get(sym)
            row = dict(r)
            if s:
                row["sfari_score"] = s["score"] or ("S" if s["syndromic"] else row.get("sfari_score", ""))
                row["sfari_chromosome"]      = s["chromosome"]
                row["sfari_genetic_category"]= s["genetic_category"]
                row["sfari_syndromic_flag"]  = "TRUE" if s["syndromic"] else "FALSE"
                row["sfari_eagle_score"]     = s["eagle"] if s["eagle"] is not None else ""
                row["sfari_number_of_reports"]= s["n_reports"] if s["n_reports"] is not None else ""
                row["sfari_quarter"]         = quarter
                row["sfari_url"]             = SFARI_GENE_URL_FMT.format(symbol=sym)
                # Backfill ensembl_id only if empty in atlas (preserve curated)
                if not row.get("ensembl_id"):
                    row["ensembl_id"] = s["ensembl_id"]
                row["last_updated"] = datetime.now(timezone.utc).isoformat()
            w.writerow(row)
    return CAND

def main():
    ap = argparse.ArgumentParser(description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--commit",  action="store_true",
                    help="write delta report + Discoveries_Inbox stubs + proposed CSV")
    ap.add_argument("--apply",   action="store_true",
                    help="promote sfari_genes_proposed.csv → v2.0_scored/genes.csv "
                         "(use only after human review of the delta report)")
    ap.add_argument("--raw-only", action="store_true",
                    help="just download + cache the raw CSV, no cross-walk")
    args = ap.parse_args()

    if args.apply:
        # Apply path: read proposed, copy to canonical
        if not CAND.exists():
            log(f"⚠ proposed CSV missing at {CAND} — run without --apply first")
            sys.exit(1)
        import shutil
        BACKUP = REPO / "v2.0_scored.before_sfari" / "genes.csv"
        BACKUP.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(GENES, BACKUP)
        shutil.copy(CAND, GENES)
        log(f"✓ applied {CAND.name} → {GENES.name} (backup: {BACKUP})")
        log(f"  next step: re-run densify_gene_layer.py to refresh HYP-0028 edges")
        log(f"  then: apply_patches_and_score.py to verify calibration (INT-0001 ≥ 80)")
        return 0

    log(f"fetching SFARI Gene CSV from {SFARI_CSV_URL[:80]}…")
    raw = fetch_sfari_csv()
    sha = hashlib.sha256(raw).hexdigest()[:16]
    quarter = detect_quarter()
    log(f"  size={len(raw):,}B sha256={sha} quarter={quarter}")

    if args.raw_only:
        RAW_DIR.mkdir(parents=True, exist_ok=True)
        fp = RAW_DIR / f"{datetime.now(timezone.utc):%Y-%m-%d}_genes_{quarter}_{sha}.csv"
        fp.write_bytes(raw)
        log(f"  saved raw CSV: {fp}")
        return 0

    sfari_rows = parse_sfari_csv(raw)
    log(f"  parsed {len(sfari_rows)} SFARI gene rows")

    atlas_rows, atlas_fields = read_atlas_genes()
    log(f"  atlas has {len(atlas_rows)} genes")

    delta = cross_walk(atlas_rows, sfari_rows)
    log(f"  delta: {len(delta['changed'])} changed scores, "
        f"{len(delta['new_in_sfari'])} new in SFARI, "
        f"{len(delta['atlas_only'])} atlas-only, "
        f"{delta['n_unchanged']} unchanged")

    if not args.commit:
        log("dry-run: pass --commit to write delta report + Discoveries_Inbox + proposed CSV")
        return 0

    rpt = write_delta_report(delta, sha, quarter)
    log(f"  ✓ delta report → {rpt}")

    n_inbox = write_discoveries_inbox(delta["new_in_sfari"], quarter)
    log(f"  ✓ wrote {n_inbox} Discoveries_Inbox stubs")

    cand = write_proposed_csv(atlas_rows, atlas_fields, sfari_rows, quarter)
    log(f"  ✓ proposed CSV → {cand}")

    log("")
    log("REVIEW BEFORE PROMOTING:")
    log(f"  1. Open delta report: {rpt}")
    log(f"  2. Triage Discoveries_Inbox stubs: {INBOX}/SFARI-*.md")
    log(f"  3. Diff proposed vs canonical: diff {GENES} {cand}")
    log(f"  4. When approved: python3 scripts/sfari/integrate_genes.py --apply")
    log(f"  5. Re-densify: python3 densify_gene_layer.py")
    log(f"  6. Re-score: python3 apply_patches_and_score.py")
    log(f"  7. Verify INT-0001 calibration anchor ≥ 80")
    return 0

if __name__ == "__main__":
    sys.exit(main() or 0)
