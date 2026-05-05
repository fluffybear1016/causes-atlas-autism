#!/usr/bin/env python3
"""
build_vault.py — Deterministic transform from v2.0_scored/ CSVs to an
Obsidian vault under vault/. One .md per entity (except genes, which get
a single INDEX.md), wiki-linked across the graph.

Read-only on v2.0_scored/. Writes to vault/. No judgment calls. No invented
links. If a CSV cell is empty, the corresponding link/field is omitted.
"""

from __future__ import annotations

import csv
import json
import os
import re
import shutil
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

# --------------------------------------------------------------------------
# Paths
# --------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent
SRC_DIR = ROOT / "v2.0_scored"
VAULT = ROOT / "vault"

ENTITY_DIRS = {
    "hypothesis": VAULT / "hypotheses",
    "mechanism": VAULT / "mechanisms",
    "intervention": VAULT / "interventions",
    "combination": VAULT / "combinations",
    "phenotype": VAULT / "phenotypes",
    "source": VAULT / "sources",
    "gene": VAULT / "genes",
}

# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

# Avoid characters that break filenames or wiki-link parsing.
_FN_BAD = re.compile(r"[\\/:*?\"<>|\[\]#^]")
_WS = re.compile(r"\s+")


def sanitize_name(name: str, maxlen: int = 80) -> str:
    """Filesystem- and wiki-link-safe rendering of a free-text name.

    Rule: replace any character that breaks filenames or Obsidian wiki-links
    with a single space, collapse whitespace, strip, truncate.
    """
    if not name:
        return ""
    # Replace path-/wiki-breaking chars with space
    s = _FN_BAD.sub(" ", name)
    # Drop control chars
    s = "".join(ch for ch in s if ch.isprintable())
    # Collapse whitespace
    s = _WS.sub(" ", s).strip()
    # Strip trailing dots/spaces (Windows-hostile but harmless on macOS too)
    s = s.rstrip(". ")
    if len(s) > maxlen:
        s = s[:maxlen].rstrip()
    return s


def yaml_value(v: Any) -> str:
    """Render a value as a YAML scalar. Numbers and booleans pass through;
    strings get single-quoted with internal single-quotes doubled. None and
    empty strings produce ``""`` (so the key is still present and Dataview
    can see it as null/blank rather than missing).
    """
    if v is None or v == "":
        return '""'
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return repr(v)
    s = str(v)
    # Try numeric first
    try:
        f = float(s)
        if f == int(f) and "." not in s and "e" not in s.lower():
            return str(int(f))
        return s
    except ValueError:
        pass
    # Boolean strings
    low = s.strip().lower()
    if low in ("true", "false"):
        return low
    # Quote everything else
    s = s.replace("\\", "\\\\").replace("'", "''")
    return f"'{s}'"


def yaml_list(items: list) -> str:
    if not items:
        return "[]"
    parts = [yaml_value(i) for i in items]
    return "[" + ", ".join(parts) + "]"


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def split_semicolon(s: str | None) -> list[str]:
    if not s:
        return []
    return [x.strip() for x in s.split(";") if x.strip()]


def parse_year(date_published: str, raw_metadata: str) -> str:
    if date_published:
        m = re.match(r"(\d{4})", date_published)
        if m:
            return m.group(1)
    if raw_metadata:
        try:
            d = json.loads(raw_metadata)
            y = d.get("year")
            if y:
                return str(y)
        except Exception:
            pass
    return ""


def parse_doi(raw_metadata: str) -> str:
    if not raw_metadata:
        return ""
    try:
        d = json.loads(raw_metadata)
        return str(d.get("doi") or "")
    except Exception:
        return ""


# --------------------------------------------------------------------------
# Load CSVs
# --------------------------------------------------------------------------

print(f"Reading from {SRC_DIR}")
hypotheses = read_csv(SRC_DIR / "hypotheses.csv")
mechanisms = read_csv(SRC_DIR / "mechanisms.csv")
interventions = read_csv(SRC_DIR / "interventions.csv")
combinations = read_csv(SRC_DIR / "combinations.csv")
phenotypes = read_csv(SRC_DIR / "phenotypes.csv")
sources = read_csv(SRC_DIR / "sources.csv")
genes = read_csv(SRC_DIR / "genes.csv")
evidence_fragments = read_csv(SRC_DIR / "evidence_fragments.csv")
evidence_links = read_csv(SRC_DIR / "evidence_links.csv")

hme = read_csv(SRC_DIR / "hypothesis_mechanism_edges.csv")
ihe = read_csv(SRC_DIR / "intervention_hypothesis_edges.csv")
ime = read_csv(SRC_DIR / "intervention_mechanism_edges.csv")
ige = read_csv(SRC_DIR / "intervention_gene_edges.csv")
ipe = read_csv(SRC_DIR / "intervention_phenotype_edges.csv")
mpe = read_csv(SRC_DIR / "mechanism_phenotype_edges.csv")
ghe = read_csv(SRC_DIR / "gene_hypothesis_edges.csv")
gme = read_csv(SRC_DIR / "gene_mechanism_edges.csv")
gpe = read_csv(SRC_DIR / "gene_phenotype_edges.csv")
hhe = read_csv(SRC_DIR / "hypothesis_hypothesis_edges.csv")
combo_members = read_csv(SRC_DIR / "combination_members.csv")

# Stable sort everything by id
for tbl in (
    hypotheses, mechanisms, interventions, combinations, phenotypes,
    sources, genes, evidence_fragments, evidence_links,
    hme, ihe, ime, ige, ipe, mpe, ghe, gme, gpe, hhe, combo_members,
):
    tbl.sort(key=lambda r: r.get("id", ""))

print(
    f"Loaded: {len(hypotheses)} hypotheses, {len(mechanisms)} mechanisms, "
    f"{len(interventions)} interventions, {len(combinations)} combinations, "
    f"{len(phenotypes)} phenotypes, {len(sources)} sources, {len(genes)} genes"
)
print(
    f"        {len(evidence_fragments)} evidence_fragments, "
    f"{len(evidence_links)} evidence_links, {len(hhe)} hypothesis_hypothesis_edges"
)

# --------------------------------------------------------------------------
# Build filename / wiki-link target tables
# --------------------------------------------------------------------------

# Each entity gets a single canonical "<ID> <name>" label that doubles as
# its filename stem and its wiki-link target.

label_by_id: dict[str, str] = {}
type_by_id: dict[str, str] = {}


def register(entity_type: str, _id: str, label_part: str) -> str:
    label = f"{_id} {sanitize_name(label_part)}".strip()
    label_by_id[_id] = label
    type_by_id[_id] = entity_type
    return label


for r in hypotheses:
    register("hypothesis", r["id"], r.get("name", ""))
for r in mechanisms:
    register("mechanism", r["id"], r.get("name", ""))
for r in interventions:
    register("intervention", r["id"], r.get("name", ""))
for r in combinations:
    register("combination", r["id"], r.get("name", ""))
for r in phenotypes:
    register("phenotype", r["id"], r.get("name", ""))

# Genes: per spec, do NOT generate per-gene .md files. Keep a separate
# label table so we can render plain-text references that point at the
# single genes/INDEX.md (rather than dangling wiki-links).
gene_label: dict[str, str] = {}
for r in genes:
    gene_label[r["id"]] = f"{r['id']} {sanitize_name(r.get('gene_symbol', ''))}".strip()
    type_by_id[r["id"]] = "gene"

# Sources: pmid if pubmed and present; else short title; else platform tag.
for r in sources:
    pid = r["id"]
    plat = r.get("platform", "")
    ext = (r.get("external_id") or "").strip()
    title = (r.get("title") or "").strip()
    if plat == "pubmed" and ext:
        label_part = ext  # PMID
    elif title:
        label_part = title
    else:
        label_part = plat or "source"
    register("source", pid, label_part)


def link(entity_id: str | None, missing: list | None = None) -> str | None:
    """Return ``[[<canonical label>]]`` for an id, or None if unknown."""
    if not entity_id:
        return None
    lbl = label_by_id.get(entity_id)
    if lbl is None:
        if missing is not None:
            missing.append(entity_id)
        return None
    return f"[[{lbl}]]"


# --------------------------------------------------------------------------
# Build edge indexes
# --------------------------------------------------------------------------

# Edges as (source_id) -> [related_id, ...] and reverse.

def index_edges(rows: list[dict], a: str, b: str) -> tuple[dict, dict]:
    fwd: dict[str, list[str]] = defaultdict(list)
    rev: dict[str, list[str]] = defaultdict(list)
    seen: set = set()
    for r in rows:
        ka = (r.get(a) or "").strip()
        kb = (r.get(b) or "").strip()
        if not ka or not kb:
            continue
        key = (ka, kb)
        if key in seen:
            continue
        seen.add(key)
        fwd[ka].append(kb)
        rev[kb].append(ka)
    for d in (fwd, rev):
        for k in d:
            # Stable sort by id so output order is deterministic
            d[k].sort()
    return fwd, rev


# hypothesis <-> mechanism
hyp_to_mec, mec_to_hyp = index_edges(hme, "hypothesis_id", "mechanism_id")
# intervention <-> hypothesis
int_to_hyp, hyp_to_int = index_edges(ihe, "intervention_id", "hypothesis_id")
# intervention <-> mechanism
int_to_mec, mec_to_int = index_edges(ime, "intervention_id", "mechanism_id")
# intervention <-> gene
int_to_gen, gen_to_int = index_edges(ige, "intervention_id", "gene_id")
# intervention <-> phenotype
int_to_phe, phe_to_int = index_edges(ipe, "intervention_id", "phenotype_id")
# mechanism <-> phenotype
mec_to_phe, phe_to_mec = index_edges(mpe, "mechanism_id", "phenotype_id")
# gene <-> hypothesis / mechanism / phenotype
gen_to_hyp, hyp_to_gen = index_edges(ghe, "gene_id", "hypothesis_id")
gen_to_mec, mec_to_gen = index_edges(gme, "gene_id", "mechanism_id")
gen_to_phe, phe_to_gen = index_edges(gpe, "gene_id", "phenotype_id")
# hypothesis upstream/downstream
hyp_upstream_of, hyp_downstream_of = index_edges(
    hhe, "upstream_hypothesis_id", "downstream_hypothesis_id"
)

# combinations -> members
com_to_int: dict[str, list[str]] = defaultdict(list)
int_to_com: dict[str, list[str]] = defaultdict(list)
for r in combo_members:
    cid, iid = r.get("combination_id", ""), r.get("intervention_id", "")
    if cid and iid:
        com_to_int[cid].append(iid)
        int_to_com[iid].append(cid)
for d in (com_to_int, int_to_com):
    for k in d:
        d[k].sort()

# evidence: source_id -> [evidence_fragment rows]
src_to_evd: dict[str, list[dict]] = defaultdict(list)
for r in evidence_fragments:
    src_to_evd[r.get("source_id", "")].append(r)
for k in src_to_evd:
    src_to_evd[k].sort(key=lambda x: x["id"])

# evidence_fragment_id -> [(target_type, target_id, effect_direction)]
evd_to_targets: dict[str, list[tuple[str, str, str]]] = defaultdict(list)
for r in evidence_links:
    fid = r.get("evidence_fragment_id", "")
    tt = r.get("target_type", "")
    tid = r.get("target_id", "")
    if not fid or not tt or not tid:
        continue
    evd_to_targets[fid].append((tt, tid, r.get("effect_direction", "")))
for k in evd_to_targets:
    evd_to_targets[k].sort()

# Reverse: target -> sources that cite it (via evidence_fragments+links)
tgt_to_sources: dict[str, set[str]] = defaultdict(set)
evd_by_id: dict[str, dict] = {r["id"]: r for r in evidence_fragments}
for r in evidence_links:
    fid = r.get("evidence_fragment_id", "")
    tid = r.get("target_id", "")
    if not fid or not tid:
        continue
    evd = evd_by_id.get(fid)
    if not evd:
        continue
    sid = evd.get("source_id", "")
    if sid:
        tgt_to_sources[tid].add(sid)


# --------------------------------------------------------------------------
# Output helpers
# --------------------------------------------------------------------------

missing_links: list[str] = []  # Track all unresolved targets


def fm(d: dict[str, Any]) -> str:
    """Render a frontmatter block. Lists become YAML inline arrays."""
    lines = ["---"]
    for k, v in d.items():
        if isinstance(v, list):
            lines.append(f"{k}: {yaml_list(v)}")
        else:
            lines.append(f"{k}: {yaml_value(v)}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def link_list(ids: list[str], header: str, out: list[str]) -> None:
    """Emit a section header plus a bullet list of resolved wiki-links.

    Genes get rendered as plain text (since they don't have individual
    notes), with a tail-link to the single ``vault/genes/INDEX.md``.
    """
    if not ids:
        return
    out.append(f"\n## {header}\n")
    for i in ids:
        if i.startswith("GEN-"):
            sym = gene_label.get(i, i)
            out.append(f"- `{sym}` (see [[INDEX|genes/INDEX]])")
            continue
        lk = link(i, missing_links)
        if lk:
            out.append(f"- {lk}")


def write_md(folder: Path, label: str, body: str) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    (folder / f"{label}.md").write_text(body, encoding="utf-8")


# --------------------------------------------------------------------------
# Wipe vault and recreate
# --------------------------------------------------------------------------

if VAULT.exists():
    # Sandbox may block file deletion; use ignore_errors and continue.
    # Files will be overwritten in place; stale files (entities removed
    # from the canonical CSVs) will need a manual cleanup.
    # PRESERVE manually-curated subdirectories (researchers/) — these
    # are hand-written content not derived from the canonical CSVs.
    # Top-level preserved subdirs (recursively preserved by virtue of being skipped)
    PRESERVE = {"researchers", "topics", "biomarkers"}
    # Hand-written files at vault root (not auto-generated)
    PRESERVE_FILES = {
        "01_PARENT_QUICK_START.md",
        "Hannah Poling framework.md",
        "CLAUDE.md",
    }
    for child in VAULT.iterdir():
        if child.name in PRESERVE:
            continue
        if child.name in PRESERVE_FILES:
            continue
        if child.is_dir():
            shutil.rmtree(child, ignore_errors=True)
        else:
            try:
                child.unlink()
            except Exception:
                pass
VAULT.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------------------------------
# Hypotheses
# --------------------------------------------------------------------------

print("\nWriting hypotheses…")
for h in hypotheses:
    hid = h["id"]
    label = label_by_id[hid]
    contested = (h.get("status", "") == "contested")
    front = {
        "id": hid,
        "type": "hypothesis",
        "name": h.get("name", ""),
        "category": h.get("category", ""),
        "status": h.get("status", ""),
        "contested": contested,
        "confidence_score": h.get("confidence_score", ""),
        "evidence_count": h.get("evidence_count", ""),
        "evidence_quality_index": h.get("evidence_quality_index", ""),
        "consistency_index": h.get("consistency_index", ""),
        "polarity": "",  # spec asked for this; not present per row, leave blank
        "last_updated": h.get("last_updated", ""),
    }
    body = [fm(front), f"# {label}\n"]
    if h.get("description"):
        body.append(f"\n{h['description']}\n")
    if h.get("affected_population"):
        body.append(f"\n**Affected population:** {h['affected_population']}\n")
    if h.get("notes"):
        body.append(f"\n**Notes:** {h['notes']}\n")

    link_list(hyp_to_mec.get(hid, []), "Mechanisms", body)
    link_list(hyp_to_int.get(hid, []), "Interventions", body)
    link_list(hyp_to_gen.get(hid, []), "Genes", body)
    link_list(hyp_upstream_of.get(hid, []), "Downstream hypotheses (this is upstream of)", body)
    link_list(hyp_downstream_of.get(hid, []), "Upstream hypotheses (this is downstream of)", body)
    link_list(sorted(tgt_to_sources.get(hid, set())), "Sources", body)

    write_md(ENTITY_DIRS["hypothesis"], label, "\n".join(body) + "\n")

# --------------------------------------------------------------------------
# Mechanisms
# --------------------------------------------------------------------------

print("Writing mechanisms…")
for m in mechanisms:
    mid = m["id"]
    label = label_by_id[mid]
    front = {
        "id": mid,
        "type": "mechanism",
        "name": m.get("name", ""),
        "category": m.get("category", ""),
        "kegg_ids": split_semicolon(m.get("kegg_ids")),
        "reactome_ids": split_semicolon(m.get("reactome_ids")),
        "evidence_strength": m.get("evidence_strength", ""),
        "status": m.get("status", ""),
        "last_updated": m.get("last_updated", ""),
    }
    body = [fm(front), f"# {label}\n"]
    if m.get("description"):
        body.append(f"\n{m['description']}\n")
    if m.get("notes"):
        body.append(f"\n**Notes:** {m['notes']}\n")

    link_list(mec_to_hyp.get(mid, []), "Hypotheses", body)
    link_list(mec_to_int.get(mid, []), "Interventions", body)
    link_list(mec_to_gen.get(mid, []), "Genes", body)
    link_list(mec_to_phe.get(mid, []), "Phenotypes", body)
    link_list(sorted(tgt_to_sources.get(mid, set())), "Sources", body)

    write_md(ENTITY_DIRS["mechanism"], label, "\n".join(body) + "\n")

# --------------------------------------------------------------------------
# Interventions
# --------------------------------------------------------------------------

print("Writing interventions…")
for it in interventions:
    iid = it["id"]
    label = label_by_id[iid]
    front = {
        "id": iid,
        "type": "intervention",
        "name": it.get("name", ""),
        "category": it.get("category", ""),
        "modality": it.get("category", ""),  # spec asked for "modality"
        "directionality": it.get("directionality", ""),
        "csrs_score": it.get("csrs_score", ""),
        "csrs_prevention_score": it.get("csrs_prevention_score", ""),
        "csrs_treatment_score": it.get("csrs_treatment_score", ""),
        "status": it.get("status", ""),
        "otc_or_rx": it.get("otc_or_rx", ""),
        "pediatric_safe": it.get("pediatric_safe", ""),
        "cost_per_month_usd": it.get("cost_per_month_usd", ""),
        "dose_range": it.get("dose_range", ""),
        "last_updated": it.get("last_updated", ""),
    }
    body = [fm(front), f"# {label}\n"]
    if it.get("mechanism_summary"):
        body.append(f"\n{it['mechanism_summary']}\n")
    if it.get("dose_range"):
        body.append(f"\n**Dose range:** {it['dose_range']}\n")
    if it.get("cost_per_month_usd"):
        body.append(f"\n**Cost per month (USD):** {it['cost_per_month_usd']}\n")
    if it.get("notes"):
        body.append(f"\n**Notes / warnings:** {it['notes']}\n")

    link_list(int_to_hyp.get(iid, []), "Hypotheses", body)
    link_list(int_to_mec.get(iid, []), "Mechanisms", body)
    link_list(int_to_gen.get(iid, []), "Genes", body)
    link_list(int_to_phe.get(iid, []), "Phenotypes", body)
    link_list(int_to_com.get(iid, []), "Combinations", body)
    link_list(sorted(tgt_to_sources.get(iid, set())), "Sources", body)

    write_md(ENTITY_DIRS["intervention"], label, "\n".join(body) + "\n")

# --------------------------------------------------------------------------
# Combinations
# --------------------------------------------------------------------------

print("Writing combinations…")
for c in combinations:
    cid = c["id"]
    label = label_by_id[cid]
    members = com_to_int.get(cid, [])
    front = {
        "id": cid,
        "type": "combination",
        "name": c.get("name", ""),
        "csrs_score": c.get("csrs_score", ""),
        "csrs_prevention_score": c.get("csrs_prevention_score", ""),
        "csrs_treatment_score": c.get("csrs_treatment_score", ""),
        "status": c.get("status", ""),
        "member_intervention_ids": members,
        "last_updated": c.get("last_updated", ""),
    }
    body = [fm(front), f"# {label}\n"]
    if c.get("description"):
        body.append(f"\n{c['description']}\n")
    if c.get("rationale"):
        body.append(f"\n## Rationale\n\n{c['rationale']}\n")
    if c.get("interaction_warnings"):
        body.append(f"\n## Interaction warnings\n\n{c['interaction_warnings']}\n")
    if c.get("notes"):
        body.append(f"\n**Notes:** {c['notes']}\n")

    link_list(members, "Members", body)

    write_md(ENTITY_DIRS["combination"], label, "\n".join(body) + "\n")

# --------------------------------------------------------------------------
# Phenotypes
# --------------------------------------------------------------------------

print("Writing phenotypes…")
for p in phenotypes:
    pid = p["id"]
    label = label_by_id[pid]
    front = {
        "id": pid,
        "type": "phenotype",
        "name": p.get("name", ""),
        "prevalence_estimate": p.get("prevalence_estimate", ""),
        "status": p.get("status", ""),
        "last_updated": p.get("last_updated", ""),
    }
    body = [fm(front), f"# {label}\n"]
    if p.get("description"):
        body.append(f"\n{p['description']}\n")
    if p.get("diagnostic_markers"):
        body.append(f"\n**Diagnostic markers:** {p['diagnostic_markers']}\n")
    if p.get("notes"):
        body.append(f"\n**Notes:** {p['notes']}\n")

    link_list(phe_to_mec.get(pid, []), "Mechanisms", body)
    link_list(phe_to_int.get(pid, []), "Interventions", body)
    link_list(phe_to_gen.get(pid, []), "Genes", body)
    link_list(sorted(tgt_to_sources.get(pid, set())), "Sources", body)

    write_md(ENTITY_DIRS["phenotype"], label, "\n".join(body) + "\n")

# --------------------------------------------------------------------------
# Sources
# --------------------------------------------------------------------------

print("Writing sources…")
for s in sources:
    sid = s["id"]
    label = label_by_id[sid]
    plat = s.get("platform", "")
    ext = (s.get("external_id") or "").strip()
    title = s.get("title", "")
    raw = s.get("raw_metadata", "")
    pmid = ext if plat == "pubmed" else ""
    doi = parse_doi(raw)
    year = parse_year(s.get("date_published", ""), raw)

    # Aggregate effect_direction across this source's evidence_fragments
    eff_dirs = sorted({
        e.get("effect_direction", "") for e in src_to_evd.get(sid, [])
        if e.get("effect_direction")
    })
    effect_direction = ";".join(eff_dirs)

    # Targets cited by this source (deduped, sorted by id)
    targets_seen: set[tuple[str, str]] = set()
    targets: list[tuple[str, str]] = []
    for evd in src_to_evd.get(sid, []):
        for tt, tid, _ in evd_to_targets.get(evd["id"], []):
            key = (tt, tid)
            if key in targets_seen:
                continue
            targets_seen.add(key)
            targets.append(key)
    targets.sort(key=lambda x: (x[0], x[1]))

    front = {
        "id": sid,
        "type": "source",
        "platform": plat,
        "pmid": pmid,
        "doi": doi,
        "year": year,
        "study_type": s.get("study_design", ""),
        "study_design": s.get("study_design", ""),
        "sample_size": s.get("sample_size", ""),
        "effect_direction": effect_direction,
        "url": s.get("url", ""),
        "model_system": s.get("model_system", ""),
        "date_published": s.get("date_published", ""),
        "date_ingested": s.get("date_ingested", ""),
    }
    body = [fm(front), f"# {label}\n"]
    if title:
        body.append(f"\n**Title:** {title}\n")
    if s.get("url"):
        body.append(f"\n**URL:** {s['url']}\n")
    if pmid:
        body.append(f"\n**PMID:** {pmid}\n")
    if doi:
        body.append(f"\n**DOI:** {doi}\n")
    if s.get("notes"):
        body.append(f"\n**Notes / methodological caveats:** {s['notes']}\n")

    # Evidence fragments
    if src_to_evd.get(sid):
        body.append("\n## Evidence fragments\n")
        for evd in src_to_evd[sid]:
            eid = evd["id"]
            ftype = evd.get("fragment_type", "")
            ed = evd.get("effect_direction", "")
            text = evd.get("text_excerpt", "").strip()
            body.append(
                f"\n### {eid}"
                + (f" — {ftype}" if ftype else "")
                + (f" ({ed})" if ed else "")
                + "\n"
            )
            if text:
                # Render as a blockquote so multi-line excerpts read well
                quoted = "\n".join("> " + ln for ln in text.splitlines())
                body.append(f"\n{quoted}\n")
            tgt_links = []
            for tt, tid, _ in evd_to_targets.get(eid, []):
                if tid.startswith("GEN-"):
                    tgt_links.append(f"{tt}: `{gene_label.get(tid, tid)}`")
                    continue
                lk = link(tid, missing_links)
                if lk:
                    tgt_links.append(f"{tt}: {lk}")
            if tgt_links:
                body.append("\n**Supports:** " + "; ".join(tgt_links) + "\n")

    # Roll-up of all targets cited by this source as wiki-link bullets
    if targets:
        body.append("\n## Cited entities\n")
        for tt, tid in targets:
            if tid.startswith("GEN-"):
                body.append(f"- {tt}: `{gene_label.get(tid, tid)}` (see [[INDEX|genes/INDEX]])")
                continue
            lk = link(tid, missing_links)
            if lk:
                body.append(f"- {tt}: {lk}")

    write_md(ENTITY_DIRS["source"], label, "\n".join(body) + "\n")

# --------------------------------------------------------------------------
# Genes — single INDEX.md with a Dataview-style table
# --------------------------------------------------------------------------

print("Writing genes/INDEX.md…")
gene_lines: list[str] = []
gene_lines.append("---")
gene_lines.append("type: gene_index")
gene_lines.append("---")
gene_lines.append("")
gene_lines.append("# Genes — Index")
gene_lines.append("")
gene_lines.append(f"All {len(genes)} genes in the atlas. Per spec, individual "
                  "gene notes are not generated (would be 1,500+ files of pure noise).")
gene_lines.append("")
gene_lines.append("## Dataview")
gene_lines.append("")
gene_lines.append("```dataview")
gene_lines.append("TABLE gene_symbol, sfari_score, genetic_evidence_strength, opentargets_score, function_summary")
gene_lines.append("FROM \"genes\"")
gene_lines.append("WHERE type = \"gene_index\"")
gene_lines.append("```")
gene_lines.append("")
gene_lines.append(
    "*(The Dataview block above is a placeholder; the static table below is the "
    "deterministic dump of `v2.0_scored/genes.csv`, sorted by gene id.)*"
)
gene_lines.append("")
gene_lines.append("## Static table")
gene_lines.append("")
gene_lines.append("| ID | Symbol | SFARI | Genetic evidence | OpenTargets | DisGeNET | Function |")
gene_lines.append("|----|--------|-------|------------------|-------------|----------|----------|")
for g in genes:
    sym = g.get("gene_symbol", "")
    fn = (g.get("function_summary") or "").replace("|", "\\|").replace("\n", " ")
    if len(fn) > 200:
        fn = fn[:200] + "…"
    gene_lines.append(
        "| {gid} | {sym} | {sfari} | {gen} | {ot} | {dis} | {fn} |".format(
            gid=g["id"],
            sym=sym,
            sfari=g.get("sfari_score", ""),
            gen=g.get("genetic_evidence_strength", ""),
            ot=g.get("opentargets_score", ""),
            dis=g.get("disgenet_score", ""),
            fn=fn,
        )
    )

ENTITY_DIRS["gene"].mkdir(parents=True, exist_ok=True)
(ENTITY_DIRS["gene"] / "INDEX.md").write_text(
    "\n".join(gene_lines) + "\n", encoding="utf-8"
)

# Note: the spec's instructions list "vault/genes/INDEX.md" not per-gene
# files, so we do NOT register/wiki-link to individual gene pages. Existing
# wiki-links to gene IDs in mechanism/intervention/etc. notes will resolve
# to nothing (intentionally). Convert those references to plain text instead
# of wiki-links: rewrite once at the end.

# --------------------------------------------------------------------------
# Top-level dashboard 00_INDEX.md
# --------------------------------------------------------------------------

print("Writing 00_INDEX.md…")

# Read calibration.txt and run_summary.json
calibration_text = ""
if (SRC_DIR / "calibration.txt").exists():
    calibration_text = (SRC_DIR / "calibration.txt").read_text(encoding="utf-8").strip()
run_summary_text = ""
if (SRC_DIR / "run_summary.json").exists():
    try:
        rs = json.loads((SRC_DIR / "run_summary.json").read_text(encoding="utf-8"))
        run_summary_text = json.dumps(rs, indent=2)
    except Exception:
        run_summary_text = (SRC_DIR / "run_summary.json").read_text(encoding="utf-8")

idx = []
idx.append("---")
idx.append("type: index")
idx.append('title: "Causes Atlas (Autism) — Vault Index"')
idx.append("---")
idx.append("")
idx.append("# Causes Atlas (Autism)")
idx.append("")
idx.append(
    "Generated from `v2.0_scored/`. One markdown note per entity (except genes, "
    "which live in a single index). All cross-references are `[[wiki-links]]` "
    "so the graph view renders the causal DAG natively."
)
idx.append("")
idx.append("## Counts")
idx.append("")
idx.append(f"- Hypotheses: **{len(hypotheses)}**")
idx.append(f"- Mechanisms: **{len(mechanisms)}**")
idx.append(f"- Interventions: **{len(interventions)}**")
idx.append(f"- Combinations: **{len(combinations)}**")
idx.append(f"- Phenotypes: **{len(phenotypes)}**")
idx.append(f"- Genes: **{len(genes)}** (see [[INDEX|genes/INDEX]])")
idx.append(f"- Sources: **{len(sources)}**")
idx.append(f"- Evidence fragments: **{len(evidence_fragments)}**")
idx.append(f"- Evidence links: **{len(evidence_links)}**")
idx.append(f"- Hypothesis→hypothesis edges: **{len(hhe)}**")
idx.append("")

# Top-10 interventions by csrs_score
def to_float(s):
    try:
        return float(s)
    except Exception:
        return float("-inf")

top_int = sorted(
    interventions,
    key=lambda r: (-to_float(r.get("csrs_score", "")), r["id"]),
)[:10]
idx.append("## Top 10 interventions (by CSRS)")
idx.append("")
idx.append("| Rank | ID | Name | CSRS | Prevention | Treatment | Modality |")
idx.append("|------|----|------|------|-----------|-----------|----------|")
for i, it in enumerate(top_int, 1):
    lk = link(it["id"]) or it["id"]
    idx.append(
        f"| {i} | {it['id']} | {lk} | "
        f"{it.get('csrs_score', '')} | "
        f"{it.get('csrs_prevention_score', '')} | "
        f"{it.get('csrs_treatment_score', '')} | "
        f"{it.get('category', '')} |"
    )
idx.append("")

# Top-5 combinations by csrs_score
top_com = sorted(
    combinations,
    key=lambda r: (-to_float(r.get("csrs_score", "")), r["id"]),
)[:5]
idx.append("## Top 5 combinations (by CSRS)")
idx.append("")
idx.append("| Rank | ID | Name | CSRS |")
idx.append("|------|----|------|------|")
for i, c in enumerate(top_com, 1):
    lk = link(c["id"]) or c["id"]
    idx.append(f"| {i} | {c['id']} | {lk} | {c.get('csrs_score', '')} |")
idx.append("")

# Contested hypotheses
contested = [h for h in hypotheses if h.get("status", "") == "contested"]
contested.sort(key=lambda r: r["id"])
idx.append(f"## Contested hypotheses ({len(contested)})")
idx.append("")
if contested:
    for h in contested:
        lk = link(h["id"]) or h["id"]
        idx.append(f"- {lk} — confidence {h.get('confidence_score', '')}")
else:
    idx.append("_None._")
idx.append("")

# Recently scored interventions (top 10 by csrs_last_updated)
def sort_key_recent(r):
    return r.get("csrs_last_updated") or r.get("last_updated") or ""

recent = sorted(
    interventions,
    key=lambda r: (sort_key_recent(r), r["id"]),
    reverse=True,
)[:10]
idx.append("## Recently scored (top 10 interventions by csrs_last_updated)")
idx.append("")
idx.append("| ID | Name | CSRS | Last updated |")
idx.append("|----|------|------|--------------|")
for it in recent:
    lk = link(it["id"]) or it["id"]
    idx.append(
        f"| {it['id']} | {lk} | {it.get('csrs_score', '')} | "
        f"{it.get('csrs_last_updated', '')} |"
    )
idx.append("")

# Calibration status
idx.append("## Calibration status")
idx.append("")
idx.append("Anchor: **INT-0001 Leucovorin** must score ≥ 80.")
leuco = next((it for it in interventions if it["id"] == "INT-0001"), None)
if leuco:
    score = to_float(leuco.get("csrs_score", ""))
    status = "PASS ✅" if score >= 80 else "FAIL ❌"
    lk = link("INT-0001") or "INT-0001"
    idx.append(f"- Current score: **{leuco.get('csrs_score', '')}** ({status})")
    idx.append(f"- Link: {lk}")
idx.append("")
if calibration_text:
    idx.append("### `calibration.txt`")
    idx.append("")
    idx.append("```")
    idx.append(calibration_text)
    idx.append("```")
    idx.append("")
if run_summary_text:
    idx.append("### `run_summary.json`")
    idx.append("")
    idx.append("```json")
    idx.append(run_summary_text)
    idx.append("```")
    idx.append("")

# Dataview queries
idx.append("## Dataview queries")
idx.append("")
idx.append("Top interventions by CSRS:")
idx.append("")
idx.append("```dataview")
idx.append("TABLE csrs_score, csrs_prevention_score, csrs_treatment_score, modality")
idx.append("FROM \"interventions\"")
idx.append("WHERE type = \"intervention\"")
idx.append("SORT csrs_score DESC")
idx.append("LIMIT 25")
idx.append("```")
idx.append("")
idx.append("Contested hypotheses:")
idx.append("")
idx.append("```dataview")
idx.append("TABLE confidence_score, evidence_count")
idx.append("FROM \"hypotheses\"")
idx.append("WHERE contested = true")
idx.append("SORT confidence_score DESC")
idx.append("```")
idx.append("")
idx.append("Top combinations:")
idx.append("")
idx.append("```dataview")
idx.append("TABLE csrs_score, member_intervention_ids")
idx.append("FROM \"combinations\"")
idx.append("WHERE type = \"combination\"")
idx.append("SORT csrs_score DESC")
idx.append("```")
idx.append("")

(VAULT / "00_INDEX.md").write_text("\n".join(idx) + "\n", encoding="utf-8")

# --------------------------------------------------------------------------
# Wiki-link resolution report
# --------------------------------------------------------------------------

print("\nDone writing files.")
print()
print("File counts:")
for sub in ("hypotheses", "mechanisms", "interventions", "combinations",
            "phenotypes", "sources"):
    n = len(list((VAULT / sub).glob("*.md")))
    print(f"  vault/{sub}/  -> {n}")
n = len(list((VAULT / "genes").glob("*.md")))
print(f"  vault/genes/  -> {n}")
print(f"  vault/00_INDEX.md  -> {(VAULT / '00_INDEX.md').exists()}")

# Summarize unresolved wiki-link targets
unresolved = sorted(set(missing_links))
print()
print(f"Unresolved wiki-link targets: {len(unresolved)}")
if unresolved:
    by_prefix: dict[str, int] = defaultdict(int)
    for u in unresolved:
        by_prefix[u.split("-")[0]] += 1
    for p, c in sorted(by_prefix.items()):
        print(f"  {p}-* -> {c}")
    if len(unresolved) <= 20:
        for u in unresolved:
            print(f"    - {u}")
    else:
        print(f"    (first 20 shown)")
        for u in unresolved[:20]:
            print(f"    - {u}")

# Verify the calibration anchor link is in INT-0001's note
leuco_label = label_by_id.get("INT-0001")
if leuco_label:
    p = ENTITY_DIRS["intervention"] / f"{leuco_label}.md"
    if p.exists():
        print(f"\nINT-0001 note: {p.relative_to(ROOT)}")

print("\nVault built at:", VAULT)
