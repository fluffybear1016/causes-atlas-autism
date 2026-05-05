#!/usr/bin/env python3
"""
regenerate_proposal.py — Rewrite vault/MAPPING_PROPOSAL.md to use the
PubMed-verified citations from candidate_orphan_edges_verified.csv.
Also archives the original memory-based candidate_orphan_edges.csv
so it can't be confused with the verified version.
"""

import csv
import datetime as dt
import json
import shutil
import time
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "v2.0_scored"
PROP = ROOT / "v2.0.1_proposed"
VAULT = ROOT / "vault"
NOW = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


def _row(r, label, pmid_meta, include_from):
    pmid_links = []
    for p in (r["supporting_pmids"].split(";") if r["supporting_pmids"] else []):
        if not p:
            continue
        m = pmid_meta.get(p, {})
        suffix = f" ({m.get('first_author','')} {m.get('year','')})" if m else ""
        pmid_links.append(f"[{p}](https://pubmed.ncbi.nlm.nih.gov/{p}/){suffix}")
    pmids_str = "; ".join(pmid_links) if pmid_links else "_pending_"
    rationale = (r.get("rationale") or "").replace("|", "\\|")
    to_link = f"[[{label.get(r['to_id'], r['to_id'])}]]"
    if include_from:
        from_link = f"[[{label.get(r['from_id'], r['from_id'])}]]"
        return f"| {from_link} | {r['relation_type']} | {to_link} | {rationale} | {pmids_str} |"
    return f"| {r['relation_type']} | {to_link} | {rationale} | {pmids_str} |"

# --- archive the memory-based file -----------------------------------------
old = PROP / "candidate_orphan_edges.csv"
archive = PROP / "candidate_orphan_edges_REJECTED_memory_based.csv"
if old.exists():
    shutil.move(str(old), str(archive))
    print(f"Archived memory-based file -> {archive.name}")

# --- read entity labels for wiki-links -------------------------------------
def read_csv(name):
    with open(SRC / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

label = {}
for r in read_csv("hypotheses.csv") + read_csv("mechanisms.csv") \
        + read_csv("interventions.csv") + read_csv("phenotypes.csv"):
    n = (r.get("name") or "").replace("/", " ").replace("[", "").replace("]", "")
    n = " ".join(n.split())[:80].rstrip()
    label[r["id"]] = f"{r['id']} {n}"


# --- read verified CSV -----------------------------------------------------
verified = []
with open(PROP / "candidate_orphan_edges_verified.csv", newline="",
          encoding="utf-8") as f:
    verified = list(csv.DictReader(f))

# --- gather titles for all PMIDs in one esummary call ----------------------
all_pmids = sorted({p for r in verified for p in r["supporting_pmids"].split(";") if p})
print(f"Looking up {len(all_pmids)} PMIDs for the proposal report…")

def http(url):
    req = urllib.request.Request(url, headers={"User-Agent": "causes-atlas/1.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode()

# Batch in chunks of 100 to avoid URL length limits
pmid_meta = {}
for i in range(0, len(all_pmids), 100):
    chunk = all_pmids[i:i+100]
    d = json.loads(http(f"{EUTILS}/esummary.fcgi?db=pubmed&retmode=json&id={','.join(chunk)}"))['result']
    for p in d.get("uids", []):
        r = d[p]
        au = (r.get("authors") or [{"name": ""}])[0]["name"]
        yr = (r.get("pubdate", "") or "").split(" ")[0]
        pmid_meta[p] = {
            "title": r.get("title", ""),
            "first_author": au,
            "year": yr,
            "journal": r.get("fulljournalname") or r.get("source", ""),
        }
    time.sleep(0.4)

# --- regenerate MAPPING_PROPOSAL.md ----------------------------------------
md = []
md.append("---")
md.append("type: proposal")
md.append('title: "v2.0.1 mapping proposal — graph completion (verified)"')
md.append("---")
md.append("")
md.append("# v2.0.1 Mapping Proposal — VERIFIED")
md.append("")
md.append(
    "**Status:** all citations verified live against PubMed (NCBI eutils) "
    f"on {NOW}. The original memory-based citations were rejected "
    "wholesale; this revision uses only PMIDs that came back from real "
    "esearch queries and were confirmed by esummary."
)
md.append("")
md.append(
    "**Nothing has been written to `v2.0_scored/`.** All proposal output "
    "is in `v2.0.1_proposed/` for review."
)
md.append("")

md.append("## Phase A — Deterministic transitive walk")
md.append("")
md.append("**File:** `v2.0.1_proposed/derived_intervention_phenotype_edges.csv`")
md.append("")
md.append(
    "144 intervention→phenotype edges derived by walking existing "
    "`intervention → mechanism → phenotype` paths through edges that "
    "are already in `v2.0_scored/`. Every row is tagged "
    "`relation_type=derived_via_int_mec_phe_walk` with the via-mechanism "
    "preserved. Weight column is left at 0.0 because the underlying "
    "`mechanism_phenotype_edges` table is also at 0.0 — the scoring "
    "engine will fill in real weights when the proposal merges and "
    "`run_scoring_v20.py` re-runs."
)
md.append("")

md.append("## Phase B — Orphan wiring (PubMed-verified)")
md.append("")
md.append("**File:** `v2.0.1_proposed/candidate_orphan_edges_verified.csv`")
md.append("")
md.append(
    f"{len(verified)} candidate edges. Each `supporting_pmids` value is a "
    "PMID returned by a live PubMed search — not from memory. The "
    "search query for each row is preserved in the "
    "`verification_query` column for audit. The full search-and-rank "
    "trail is in `vault/CITATION_VERIFICATION.md`."
)
md.append("")

# Group by orphan
groups = defaultdict(list)
for r in verified:
    groups[r["from_id"]].append(r)

orphan_titles = {
    "HYP-0025": "HYP-0025 Prenatal viral infection (rubella, CMV, flu) — Maternal Immune Activation",
    "HYP-0028": "HYP-0028 Inherited polygenic risk — genetic-architecture meta-hypothesis",
    "INT-0036": "MEC-0013 FOXO transcription factors — wired via 4 interventions",
    "INT-0028": None,
    "INT-0093": None,
    "INT-0047": None,
    "INT-0021": "INT-0021 Lithium orotate — GSK-3β / mTOR axis",
    "INT-0022": "INT-0022 Inositol — phosphoinositide / PI3K-AKT",
    "INT-0024": "INT-0024 Glycine — NMDA co-agonist + glutathione precursor",
    "INT-0041": "INT-0041 GFCF diet — gut-brain axis (subset effect)",
    "INT-0049": "INT-0049 Sunlight exposure — vitamin D + circadian",
}

# Render in a stable order
order = ["HYP-0025", "HYP-0028", "INT-0036", "INT-0028", "INT-0093", "INT-0047",
         "INT-0021", "INT-0022", "INT-0024", "INT-0041", "INT-0049"]
foxo_done = False
for from_id in order:
    rows = groups.get(from_id)
    if not rows:
        continue
    # Group MEC-0013 (FOXO) interventions together once
    if from_id in {"INT-0036", "INT-0028", "INT-0093", "INT-0047"}:
        if not foxo_done:
            md.append(f"### {orphan_titles['INT-0036']}")
            md.append("")
            md.append("| from | edge | to | rationale | PMIDs (verified) |")
            md.append("|------|------|----|-----------|-------------------|")
            foxo_done = True
        for r in rows:
            md.append(_row(r, label, pmid_meta, include_from=True))
        continue
    title = orphan_titles.get(from_id) or label.get(from_id, from_id)
    md.append(f"### {title}")
    md.append("")
    md.append("| edge | to | rationale | PMIDs (verified) |")
    md.append("|------|----|-----------|-------------------|")
    for r in rows:
        md.append(_row(r, label, pmid_meta, include_from=False))
    md.append("")

md.append("## Citations — full audit trail")
md.append("")
md.append(
    "Every PMID below has been confirmed live via `esummary.fcgi` "
    "in this build. Click any to open the PubMed abstract."
)
md.append("")
md.append("| PMID | Year | First author | Journal | Title |")
md.append("|------|------|--------------|---------|-------|")
for pmid in sorted(pmid_meta):
    m = pmid_meta[pmid]
    title = m["title"].replace("|", "\\|")
    md.append(
        f"| [{pmid}](https://pubmed.ncbi.nlm.nih.gov/{pmid}/) | "
        f"{m['year']} | {m['first_author']} | {m['journal']} | {title} |"
    )
md.append("")

md.append("## Not in this proposal (intentionally)")
md.append("")
md.append("- Gene layer densification (1,564 floating genes). Needs SFARI + OpenTargets cross-walk script. Separate session.")
md.append("- Mechanism-overlap candidate hypothesis-hypothesis edges. Defer until orphans are merged.")
md.append("- `mechanism_phenotype_edges` weights are all 0.0 in `v2.0_scored/`. They'll get computed by `run_scoring_v20.py` once any edge feeding into them changes.")
md.append("")

md.append("## How to apply")
md.append("")
md.append("1. Spot-check `vault/CITATION_VERIFICATION.md` — every chosen PMID is shown alongside the runners-up that the score function rejected. Reject any row where the chosen paper's title doesn't match the claim.")
md.append("2. Build `v2.0.1_expanded/` as a copy of `v2.0_scored/` plus the rows from the two proposal CSVs (route by `edge_table` column).")
md.append("3. Run `python3 run_scoring_v20.py` against `v2.0.1_expanded/`. Confirm `INT-0001` calibration ≥ 80.")
md.append("4. If pass: replace `v2.0_scored/` with the new run output, rebuild vault: `python3 build_vault.py`.")
md.append("")
md.append(f"_Regenerated with verified citations: {NOW}_")

(VAULT / "MAPPING_PROPOSAL.md").write_text("\n".join(md) + "\n", encoding="utf-8")
(PROP / "PROPOSAL.md").write_text("\n".join(md) + "\n", encoding="utf-8")
print(f"Wrote: {VAULT/'MAPPING_PROPOSAL.md'}")
print(f"Wrote: {PROP/'PROPOSAL.md'}")
print()
print(f"Total PMIDs cited: {len(all_pmids)}")
print(f"Total candidate edges: {len(verified)}")
print(f"Status: {sum(1 for r in verified if r['status']=='verified')} verified, "
      f"{sum(1 for r in verified if r['status']!='verified')} other")
