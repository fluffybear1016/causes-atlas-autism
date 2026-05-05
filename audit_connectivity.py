#!/usr/bin/env python3
"""
audit_connectivity.py — Read-only audit of v2.0_scored/.

For every entity in the atlas, count incoming/outgoing edges of every
relevant type. Flag orphans. Produce a ranked under-connection report
written to vault/CONNECTIVITY_AUDIT.md. Does not modify v2.0_scored/.
"""

from __future__ import annotations

import csv
import re
from collections import defaultdict
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "v2.0_scored"
OUT = ROOT / "vault" / "CONNECTIVITY_AUDIT.md"

_FN_BAD = re.compile(r"[\\/:*?\"<>|\[\]#^]")
_WS = re.compile(r"\s+")


def sanitize(s: str, n: int = 80) -> str:
    if not s:
        return ""
    s = _FN_BAD.sub(" ", s)
    s = "".join(c for c in s if c.isprintable())
    s = _WS.sub(" ", s).strip().rstrip(". ")
    return s[:n].rstrip() if len(s) > n else s


def read(name: str) -> list[dict]:
    p = SRC / name
    if not p.exists():
        return []
    with open(p, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


hypotheses = read("hypotheses.csv")
mechanisms = read("mechanisms.csv")
interventions = read("interventions.csv")
combinations = read("combinations.csv")
phenotypes = read("phenotypes.csv")
genes = read("genes.csv")
sources = read("sources.csv")
evidence_fragments = read("evidence_fragments.csv")
evidence_links = read("evidence_links.csv")

hme = read("hypothesis_mechanism_edges.csv")
ihe = read("intervention_hypothesis_edges.csv")
ime = read("intervention_mechanism_edges.csv")
ige = read("intervention_gene_edges.csv")
ipe = read("intervention_phenotype_edges.csv")
mpe = read("mechanism_phenotype_edges.csv")
ghe = read("gene_hypothesis_edges.csv")
gme = read("gene_mechanism_edges.csv")
gpe = read("gene_phenotype_edges.csv")
hhe = read("hypothesis_hypothesis_edges.csv")
combo_members = read("combination_members.csv")

# -------- label tables (for wiki-links into the existing vault) ---------
label = {}
for r in hypotheses:
    label[r["id"]] = f"{r['id']} {sanitize(r.get('name', ''))}".strip()
for r in mechanisms:
    label[r["id"]] = f"{r['id']} {sanitize(r.get('name', ''))}".strip()
for r in interventions:
    label[r["id"]] = f"{r['id']} {sanitize(r.get('name', ''))}".strip()
for r in combinations:
    label[r["id"]] = f"{r['id']} {sanitize(r.get('name', ''))}".strip()
for r in phenotypes:
    label[r["id"]] = f"{r['id']} {sanitize(r.get('name', ''))}".strip()
for r in genes:
    label[r["id"]] = f"{r['id']} {sanitize(r.get('gene_symbol', ''))}".strip()
for r in sources:
    plat = r.get("platform", "")
    ext = (r.get("external_id") or "").strip()
    title = (r.get("title") or "").strip()
    if plat == "pubmed" and ext:
        part = ext
    elif title:
        part = title
    else:
        part = plat or "source"
    label[r["id"]] = f"{r['id']} {sanitize(part)}".strip()


def wl(eid: str) -> str:
    """Wiki-link, except for genes (which have no per-note files) — render
    those as inline-code so the report still reads cleanly inside Obsidian."""
    if eid.startswith("GEN-"):
        return f"`{label.get(eid, eid)}`"
    return f"[[{label.get(eid, eid)}]]"


# -------- count edges per entity ---------
counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))


def tally(rows, a_field, b_field, a_kind, b_kind):
    for r in rows:
        a = (r.get(a_field) or "").strip()
        b = (r.get(b_field) or "").strip()
        if a:
            counts[a][b_kind] += 1
        if b:
            counts[b][a_kind] += 1


tally(hme, "hypothesis_id", "mechanism_id", "hypothesis", "mechanism")
tally(ihe, "intervention_id", "hypothesis_id", "intervention", "hypothesis")
tally(ime, "intervention_id", "mechanism_id", "intervention", "mechanism")
tally(ige, "intervention_id", "gene_id", "intervention", "gene")
tally(ipe, "intervention_id", "phenotype_id", "intervention", "phenotype")
tally(mpe, "mechanism_id", "phenotype_id", "mechanism", "phenotype")
tally(ghe, "gene_id", "hypothesis_id", "gene", "hypothesis")
tally(gme, "gene_id", "mechanism_id", "gene", "mechanism")
tally(gpe, "gene_id", "phenotype_id", "gene", "phenotype")
# hypothesis-hypothesis: count both as upstream and downstream
for r in hhe:
    u = (r.get("upstream_hypothesis_id") or "").strip()
    d = (r.get("downstream_hypothesis_id") or "").strip()
    if u:
        counts[u]["hypothesis_downstream"] += 1
    if d:
        counts[d]["hypothesis_upstream"] += 1
# combinations
for r in combo_members:
    c = (r.get("combination_id") or "").strip()
    i = (r.get("intervention_id") or "").strip()
    if c:
        counts[c]["intervention_member"] += 1
    if i:
        counts[i]["combination"] += 1
# evidence (count each entity's source-citations)
evd_to_src = {e["id"]: e.get("source_id", "") for e in evidence_fragments}
for r in evidence_links:
    tid = (r.get("target_id") or "").strip()
    fid = (r.get("evidence_fragment_id") or "").strip()
    if tid and fid and evd_to_src.get(fid):
        counts[tid]["source_citations"] += 1
# sources outgoing = number of evidence_fragments
for e in evidence_fragments:
    sid = (e.get("source_id") or "").strip()
    if sid:
        counts[sid]["evidence_fragments"] += 1


# -------- helpers for the report ---------

def total_edges(eid: str) -> int:
    return sum(counts.get(eid, {}).values())


def fmt_count_line(eid: str, fields: list[str]) -> str:
    c = counts.get(eid, {})
    parts = [f"{f}={c.get(f, 0)}" for f in fields]
    return ", ".join(parts)


# -------- write the report ---------
OUT.parent.mkdir(parents=True, exist_ok=True)
out = []
out.append("---")
out.append("type: audit")
out.append('title: "Connectivity audit — v2.0_scored"')
out.append("---")
out.append("")
out.append("# Connectivity audit")
out.append("")
out.append("Read-only pass over `v2.0_scored/`. Counts every edge of every type "
           "for every entity. Goal: surface where the graph is sparse so we can "
           "fill it in before factorial combinations.")
out.append("")

# ---- summary numbers ----
out.append("## Edge-table summary")
out.append("")
out.append("| Edge table | Rows | Notes |")
out.append("|------------|------|-------|")
out.append(f"| hypothesis_mechanism_edges | {len(hme)} | possible: {len(hypotheses)*len(mechanisms)} |")
out.append(f"| intervention_hypothesis_edges | {len(ihe)} | possible: {len(interventions)*len(hypotheses)} |")
out.append(f"| intervention_mechanism_edges | {len(ime)} | possible: {len(interventions)*len(mechanisms)} |")
out.append(f"| intervention_gene_edges | {len(ige)} | possible: {len(interventions)*len(genes)} |")
out.append(f"| intervention_phenotype_edges | {len(ipe)} | **0 rows — completely empty** |")
out.append(f"| mechanism_phenotype_edges | {len(mpe)} | possible: {len(mechanisms)*len(phenotypes)} |")
out.append(f"| gene_hypothesis_edges | {len(ghe)} | only {len(ghe)} for {len(genes)} genes |")
out.append(f"| gene_mechanism_edges | {len(gme)} | only {len(gme)} for {len(genes)} genes |")
out.append(f"| gene_phenotype_edges | {len(gpe)} | only {len(gpe)} for {len(genes)} genes |")
out.append(f"| hypothesis_hypothesis_edges | {len(hhe)} | possible: {len(hypotheses)*(len(hypotheses)-1)} |")
out.append(f"| combination_members | {len(combo_members)} | for {len(combinations)} combinations |")
out.append(f"| evidence_links | {len(evidence_links)} | from {len(evidence_fragments)} fragments |")
out.append("")

# ---- per-type orphan + sparsity tables ----
def section(title: str, rows: list[dict], fields: list[str], id_field: str = "id"):
    out.append(f"## {title}")
    out.append("")
    totals = [total_edges(r[id_field]) for r in rows]
    if totals:
        out.append(f"- Min edges: **{min(totals)}**, median: **{int(median(totals))}**, "
                   f"max: **{max(totals)}**")
        orphans = [r for r in rows if total_edges(r[id_field]) == 0]
        out.append(f"- Orphans (zero edges of any type): **{len(orphans)}**")
        out.append("")
    if orphans:
        out.append("### Orphans")
        out.append("")
        for r in orphans:
            out.append(f"- {wl(r[id_field])}")
        out.append("")
    # bottom-decile / under-connected
    sorted_rows = sorted(rows, key=lambda r: total_edges(r[id_field]))
    cutoff = max(10, len(rows) // 10)
    weak = sorted_rows[:cutoff]
    out.append(f"### Bottom-{cutoff} by total edges")
    out.append("")
    out.append("| ID | Name | Total | Breakdown |")
    out.append("|----|------|-------|-----------|")
    for r in weak:
        eid = r[id_field]
        total = total_edges(eid)
        out.append(f"| {eid} | {wl(eid)} | {total} | {fmt_count_line(eid, fields)} |")
    out.append("")


section(
    "Hypotheses (70)",
    hypotheses,
    ["mechanism", "intervention", "gene", "hypothesis_upstream",
     "hypothesis_downstream", "source_citations"],
)
section(
    "Mechanisms (33)",
    mechanisms,
    ["hypothesis", "intervention", "gene", "phenotype", "source_citations"],
)
section(
    "Interventions (99)",
    interventions,
    ["hypothesis", "mechanism", "gene", "phenotype", "combination",
     "source_citations"],
)
section(
    "Phenotypes (7)",
    phenotypes,
    ["mechanism", "intervention", "gene", "source_citations"],
)
section(
    "Combinations (5)",
    combinations,
    ["intervention_member"],
)

# Genes — too many to dump per-entry; report aggregates only.
out.append("## Genes (1564)")
out.append("")
gene_totals = [total_edges(g["id"]) for g in genes]
zero_genes = sum(1 for t in gene_totals if t == 0)
ge_count = sum(1 for t in gene_totals if t == 0 or t == 1)
out.append(f"- Total genes: **{len(genes)}**")
out.append(f"- Genes with zero edges (orphans): **{zero_genes}**")
out.append(f"- Genes with ≤1 edge: **{ge_count}**")
out.append(f"- Genes with ≥2 edges: **{len(genes) - ge_count}**")
out.append(f"- Median edges per gene: **{median(gene_totals) if gene_totals else 0}**")
out.append(f"- Max edges any single gene: **{max(gene_totals) if gene_totals else 0}**")
out.append("")
# Top-20 most-connected genes
top_genes = sorted(genes, key=lambda g: -total_edges(g["id"]))[:20]
out.append("### Top 20 most-connected genes")
out.append("")
out.append("| ID | Symbol | Total edges | hypothesis | mechanism | phenotype | intervention |")
out.append("|----|--------|-------------|------------|-----------|-----------|--------------|")
for g in top_genes:
    gid = g["id"]
    c = counts.get(gid, {})
    out.append(
        f"| {gid} | `{g.get('gene_symbol','')}` | {total_edges(gid)} | "
        f"{c.get('hypothesis',0)} | {c.get('mechanism',0)} | "
        f"{c.get('phenotype',0)} | {c.get('intervention',0)} |"
    )
out.append("")

# ---- prioritized to-do ----
out.append("## Prioritized fix-list (deterministic ranking)")
out.append("")
todos = []
todos.append(
    ("P0 — completely empty edge table",
     "**`intervention_phenotype_edges` has 0 rows.** No intervention is "
     "directly tied to any of the 7 phenotypes. This is the single biggest "
     "structural gap. Easiest fix: walk transitively "
     "`intervention → hypothesis|mechanism → phenotype` and emit derived "
     "edges with `relation_type = derived_via_walk` so the spec's "
     "deterministic-only rule isn't violated.")
)
todos.append(
    ("P1 — gene linkage near-empty",
     f"Only {len(ghe)} gene→hypothesis, {len(gme)} gene→mechanism, "
     f"{len(gpe)} gene→phenotype edges exist for **{len(genes)} genes**. "
     "Genes are loaded but largely floating. SFARI/OpenTargets scores are "
     "in `genes.csv` but no semantic connection to the rest of the graph. "
     "Most genes are effectively decoration right now. Fix: cross-walk "
     "SFARI gene → known phenotype categories (Fragile X → PHE-0006, "
     "Rett → its phenotype, etc.), plus opentargets_score to seed "
     "gene→hypothesis weight.")
)
todos.append(
    ("P2 — hypothesis→hypothesis sparse",
     f"Only {len(hhe)} cause→cause edges among {len(hypotheses)} hypotheses. "
     "Many hypotheses sit in isolation when they're known to be upstream/"
     "downstream of others (e.g., maternal infection → cytokine storm → "
     "neuroinflammation; PFAS exposure → oxidative stress; glyphosate → "
     "gut dysbiosis). Fix: pass over hypotheses sharing mechanism IDs and "
     "propose upstream/downstream candidates for review.")
)
todos.append(
    ("P3 — phenotype connection asymmetry",
     "Only 7 phenotypes total. With `intervention_phenotype_edges` empty "
     "and `gene_phenotype_edges` at 9 rows, the phenotype layer is "
     "essentially a stub. Either expand the phenotype list (the spec "
     "implies more granular phenotypes are valuable) or accept it as a "
     "small high-level taxonomy and at minimum fully connect every "
     "intervention/mechanism that touches each phenotype.")
)
todos.append(
    ("P4 — combinations under-developed",
     f"Only {len(combinations)} hand-curated combinations. v2.1 explicitly "
     "exists to score the 4,851 intervention pairs. Don't run it until P0–P3 "
     "are addressed because pair-scoring inherits from edge data — and "
     "garbage-in is worse at the combinatorial layer.")
)
for i, (head, body) in enumerate(todos, 1):
    out.append(f"### {i}. {head}")
    out.append("")
    out.append(body)
    out.append("")

# ---- Layer 2 (CSRS) sanity check ----
out.append("## Calibration sanity")
out.append("")
leuco = next((it for it in interventions if it["id"] == "INT-0001"), None)
if leuco:
    try:
        s = float(leuco.get("csrs_score", "0"))
    except ValueError:
        s = 0.0
    status = "PASS ✅" if s >= 80 else "FAIL ❌"
    out.append(f"INT-0001 Leucovorin: **{s}** ({status}). Spec requires ≥ 80.")
out.append("")

OUT.write_text("\n".join(out) + "\n", encoding="utf-8")
print(f"Wrote {OUT}")
print(f"Lines: {len(out)}")
