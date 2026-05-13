"""
ui/components/atlas_explorer.py — full Obsidian-style force-directed atlas explorer.

Shows the entire mapped atlas: phenotypes + interventions + formulations
+ mechanisms + hypotheses + key biomarkers + sources, with contested-edge
dual-color visualization, filter sidebar, click-to-drawer, pan/zoom.

This is the killer demo — visualizing the atlas as a living organism.

The atlas grows daily via the autonomous-discoveries pipeline; the
"last_updated" timestamp + node count make that visible to users.
"""
from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCORED = REPO_ROOT / "v2.0_scored"

NEBULA = {
    "PHE-0001": "#7C5CFF", "PHE-0002": "#00A7B5", "PHE-0003": "#00B26D",
    "PHE-0004": "#5BAE3C", "PHE-0005": "#355CFF", "PHE-0006": "#4F7BFF",
    "PHE-0007": "#7A7DFF", "PHE-0008": "#B05EFF", "PHE-0009": "#FF6BB3",
    "PHE-0010": "#E07A5F", "PHE-0011": "#D4A017",
}

# Visual style per entity type
TYPE_STYLE = {
    "phenotype":    {"shape": "circle", "size": 22, "ring": True},
    "intervention": {"shape": "pill",   "size": 10, "color": "#e5e4df"},
    "formulation":  {"shape": "diamond","size": 6,  "color": "#a8a89e"},
    "mechanism":    {"shape": "diamond","size": 12, "color": "#7BB3FF"},
    "hypothesis":   {"shape": "circle", "size": 9,  "color": "#FFB36B"},
    "biomarker":    {"shape": "ring",   "size": 7,  "color": "#5BAE3C"},
    "source":       {"shape": "dot",    "size": 2,  "color": "#3a3a3f"},
}


def _load_csv(name: str) -> list[dict]:
    p = SCORED / f"{name}.csv"
    if not p.exists():
        return []
    with p.open() as f:
        return list(csv.DictReader(f))


def build_atlas_payload(
    *,
    max_interventions: int = 60,
    max_hypotheses: int = 40,
    max_formulations: int = 40,
    max_biomarkers: int = 30,
    max_sources: int = 80,
) -> dict:
    """Read v2.0_scored/ and build a node+edge payload for D3."""
    interventions = _load_csv("interventions")
    hypotheses = _load_csv("hypotheses")
    mechanisms = _load_csv("mechanisms")
    phenotypes_csv = _load_csv("phenotypes")
    formulations = _load_csv("intervention_formulations_scored")
    if not formulations:
        formulations = _load_csv("intervention_formulations")
    biomarkers = _load_csv("biomarkers")
    sources = _load_csv("sources")

    int_mech_edges = _load_csv("intervention_mechanism_edges")
    int_phe_edges = _load_csv("intervention_phenotype_edges")
    int_hyp_edges = _load_csv("intervention_hypothesis_edges")
    hyp_mech_edges = _load_csv("hypothesis_mechanism_edges")
    hyp_hyp_edges = _load_csv("hypothesis_hypothesis_edges")

    # Filter to visible top-N
    def _csrs(r):
        try: return float(r.get("csrs_score") or 0)
        except (ValueError, TypeError): return 0.0

    int_top = sorted(interventions, key=lambda r: -_csrs(r))[:max_interventions]
    int_top_ids = {r["id"] for r in int_top}

    hyp_top = sorted(hypotheses,
        key=lambda r: -float(r.get("confidence") or r.get("csrs_score") or 0)
    )[:max_hypotheses]
    hyp_top_ids = {r["id"] for r in hyp_top}

    form_visible = sorted(formulations,
        key=lambda r: -float(r.get("formulation_score") or 0)
    )[:max_formulations]
    form_ids = {f.get("formulation_id") for f in form_visible}
    form_top_parent_ids = {f.get("parent_intervention_id") for f in form_visible}

    bio_top = biomarkers[:max_biomarkers]
    bio_ids = {b.get("id") for b in bio_top}

    src_top = sources[:max_sources]
    src_ids = {s.get("id") for s in src_top}

    # Build nodes list
    nodes = []
    for p in phenotypes_csv:
        pid = p.get("id")
        if pid not in NEBULA:
            continue
        nodes.append({
            "id": pid,
            "type": "phenotype",
            "name": p.get("name", pid),
            "color": NEBULA.get(pid, "#cfd0d4"),
            "score": 100.0,  # phenotypes are always highlighted
            "status": "tier_" + (p.get("evidence_tier") or "1"),
        })

    for r in int_top:
        contested = "contested" in (r.get("status", "") or "").lower()
        consensus = (r.get("mainstream_consensus_position") or "").lower()
        is_contested = contested or any(k in consensus for k in (
            "mixed", "weak", "insufficient", "contested"))
        nodes.append({
            "id": r["id"],
            "type": "intervention",
            "name": r.get("name", r["id"])[:50],
            "score": _csrs(r),
            "status": "contested" if is_contested else "active",
        })

    for f in form_visible:
        fscore = float(f.get("formulation_score") or 0)
        contested_form = str(f.get("contested_at_formulation_level", "")).lower() == "true"
        nodes.append({
            "id": f.get("formulation_id", "?"),
            "type": "formulation",
            "name": (f.get("formulation_name") or "")[:60],
            "score": fscore,
            "parent_intervention_id": f.get("parent_intervention_id"),
            "status": "contested" if contested_form else "active",
            "evidence": f.get("formulation_evidence_status", ""),
        })

    for m in mechanisms:
        nodes.append({
            "id": m.get("id", "?"),
            "type": "mechanism",
            "name": m.get("name", m.get("id"))[:50],
            "score": float(m.get("evidence_strength") or 50),
            "status": "active",
        })

    for h in hyp_top:
        consensus = (h.get("mainstream_consensus_position") or "").lower()
        is_contested = (h.get("status", "").lower() == "contested" or
                        any(k in consensus for k in ("mixed", "contested")))
        nodes.append({
            "id": h.get("id", "?"),
            "type": "hypothesis",
            "name": (h.get("name") or "")[:60],
            "score": float(h.get("confidence") or 50),
            "status": "contested" if is_contested else "active",
        })

    for b in bio_top:
        nodes.append({
            "id": b.get("id", "?"),
            "type": "biomarker",
            "name": (b.get("name") or "")[:50],
            "score": 50,
            "status": "active",
        })

    for s in src_top:
        nodes.append({
            "id": s.get("id", "?"),
            "type": "source",
            "name": (s.get("title") or s.get("id"))[:60],
            "pmid": s.get("pmid", ""),
            "score": 30,
            "status": "active",
        })

    node_ids = {n["id"] for n in nodes}

    # Build edges (filter to those with both endpoints visible)
    edges = []

    def _add(source, target, kind, weight=0.4, contested=False):
        if source in node_ids and target in node_ids:
            edges.append({"source": source, "target": target,
                          "kind": kind, "weight": weight,
                          "contested": contested})

    for e in int_mech_edges:
        _add(e.get("intervention_id"), e.get("mechanism_id"), "int-mech",
             float(e.get("weight") or 0.4))
    for e in int_phe_edges:
        _add(e.get("intervention_id"), e.get("phenotype_id"), "int-phe",
             float(e.get("evidence_strength_aggregate") or e.get("weight") or 0.4))
    for e in int_hyp_edges:
        _add(e.get("intervention_id"), e.get("hypothesis_id"), "int-hyp",
             float(e.get("weight") or 0.4))
    for e in hyp_mech_edges:
        _add(e.get("hypothesis_id"), e.get("mechanism_id"), "hyp-mech",
             float(e.get("weight") or 0.4))
    for e in hyp_hyp_edges:
        is_contested = (e.get("relationship_type", "") or "").lower() in ("contradicts","contested","disagrees")
        _add(e.get("source_hypothesis_id") or e.get("hypothesis_a"),
             e.get("target_hypothesis_id") or e.get("hypothesis_b"),
             "hyp-hyp", 0.4, contested=is_contested)
    for f in form_visible:
        _add(f.get("formulation_id"), f.get("parent_intervention_id"),
             "form-int", 0.6)

    # Counts for the "atlas at a glance" stats
    counts = {
        "phenotypes": sum(1 for n in nodes if n["type"]=="phenotype"),
        "interventions": sum(1 for n in nodes if n["type"]=="intervention"),
        "formulations": sum(1 for n in nodes if n["type"]=="formulation"),
        "mechanisms": sum(1 for n in nodes if n["type"]=="mechanism"),
        "hypotheses": sum(1 for n in nodes if n["type"]=="hypothesis"),
        "biomarkers": sum(1 for n in nodes if n["type"]=="biomarker"),
        "sources_visible": sum(1 for n in nodes if n["type"]=="source"),
        "edges": len(edges),
        "nodes_total_visible": len(nodes),
        "atlas_total_sources": len(sources),
        "atlas_total_genes": 1564,  # from atlas counts
    }

    return {"nodes": nodes, "edges": edges, "counts": counts,
            "last_updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")}


def render_atlas_explorer(payload: dict | None = None, *, height: int = 800) -> str:
    if payload is None:
        payload = build_atlas_payload()

    payload_json = json.dumps(payload)

    return r"""
<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
  html, body { margin:0; padding:0; background:#0a0b0d;
    font-family:-apple-system,Inter,system-ui,sans-serif; color:#e5e4df;
    overflow:hidden; }
  #atlas-root { position:relative; width:100%; height:100vh;
    background: radial-gradient(ellipse at 30% 30%, #15171c 0%, #0a0b0d 60%, #06070a 100%); }
  svg { width:100%; height:100%; display:block; cursor:grab; }
  svg:active { cursor:grabbing; }

  /* Top stats banner */
  .stats-banner {
    position:absolute; top:16px; left:50%; transform:translateX(-50%);
    background: rgba(20,22,26,0.78); backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border: 1px solid rgba(120,120,140,0.2);
    border-radius: 14px; padding: 12px 22px;
    display:flex; gap:28px; align-items:center;
    font-size:11px; color:#a8a89e; letter-spacing:0.04em;
    z-index:10; box-shadow:0 12px 40px rgba(0,0,0,0.6);
  }
  .stats-banner .stat { text-align:center; }
  .stats-banner .stat-num { color:#e5e4df; font-size:18px;
    font-weight:600; font-family:"IBM Plex Mono",ui-monospace,monospace;
    letter-spacing:-0.01em; display:block; }
  .stats-banner .stat-label { font-size:9px; text-transform:uppercase;
    letter-spacing:0.16em; margin-top:2px; }
  .stats-banner .pulse-dot {
    display:inline-block; width:7px; height:7px; border-radius:50%;
    background:#00B26D; box-shadow:0 0 10px #00B26D;
    animation: livePulse 2.4s infinite ease-in-out;
    margin-right:6px;
  }
  @keyframes livePulse { 0%,100%{opacity:0.5;} 50%{opacity:1;} }

  /* Filter sidebar */
  .filter-sidebar {
    position:absolute; top:88px; left:24px; width:230px;
    background: rgba(20,22,26,0.72); backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(120,120,140,0.2);
    border-radius: 14px; padding: 18px 18px;
    z-index: 10; max-height: 75vh; overflow-y:auto;
    box-shadow:0 12px 40px rgba(0,0,0,0.6);
  }
  .filter-sidebar h3 { margin:0 0 12px 0; font-size:11px;
    font-weight:600; letter-spacing:0.18em;
    text-transform:uppercase; color:#a8a89e; }
  .filter-group { margin-bottom: 16px; }
  .filter-group .label { font-size:10px;
    color:#7a7a7f; letter-spacing:0.12em;
    text-transform:uppercase; margin-bottom: 6px; }
  .filter-row { display:flex; align-items:center;
    padding: 4px 0; font-size:13px; cursor:pointer;
    transition: color 0.15s; user-select:none; }
  .filter-row:hover { color:#fff; }
  .filter-row .swatch { display:inline-block;
    width:9px; height:9px; border-radius:50%;
    margin-right:9px; flex-shrink:0; }
  .filter-row.disabled { opacity:0.35; }
  .filter-row .count {
    margin-left:auto; font-family:"IBM Plex Mono",ui-monospace,monospace;
    font-size:11px; color:#7a7a7f; }
  .search-box {
    width:100%; padding:8px 10px; box-sizing:border-box;
    background:rgba(255,255,255,0.05);
    border:1px solid rgba(120,120,140,0.25);
    border-radius:8px; color:#e5e4df; font-size:13px;
    margin-bottom:14px; outline:none;
    font-family:inherit;
  }
  .search-box:focus { border-color:#7C5CFF; }

  /* Tooltip */
  .a-tooltip {
    position:absolute; pointer-events:none;
    background: rgba(15,17,22,0.95); backdrop-filter: blur(16px);
    border: 1px solid rgba(120,120,140,0.3);
    border-radius: 10px; padding: 10px 14px;
    font-size:12px; line-height:1.5; max-width:280px;
    opacity:0; transition: opacity 0.15s; z-index:50;
    box-shadow:0 8px 32px rgba(0,0,0,0.7);
  }
  .a-tooltip .name { font-weight:600; font-size:13px; margin-bottom:3px; }
  .a-tooltip .type { font-size:9px; text-transform:uppercase;
    letter-spacing:0.16em; color:#a8a89e; }
  .a-tooltip .score { font-family:"IBM Plex Mono",ui-monospace,monospace;
    font-size:11px; color:#cfd0d4; margin-top:4px; }

  /* Drawer */
  .a-drawer {
    position:absolute; top:24px; right:24px; bottom:24px; width:380px;
    background:rgba(18,20,24,0.96); backdrop-filter: blur(20px);
    border:1px solid rgba(120,120,140,0.25);
    border-radius:14px; padding:28px 26px; overflow-y:auto;
    transform: translateX(420px);
    transition:transform 0.42s cubic-bezier(0.22,1,0.36,1);
    z-index:30; box-shadow:0 20px 60px rgba(0,0,0,0.7);
  }
  .a-drawer.open { transform: translateX(0); }
  .a-drawer .close-btn { position:absolute; top:14px; right:14px;
    background:transparent; border:none; color:#a8a89e; cursor:pointer;
    font-size:20px; padding:6px 10px; border-radius:6px; }
  .a-drawer .close-btn:hover { background:rgba(255,255,255,0.06); color:#fff; }
  .a-drawer h2 { font-size:21px; font-weight:600; margin:0 0 12px 0;
    letter-spacing:-0.01em; line-height:1.2; }
  .a-drawer .eyebrow { font-size:10px;
    letter-spacing:0.18em; text-transform:uppercase; color:#a8a89e;
    margin-bottom:6px; }
  .a-drawer .meta { font-size:13px; color:#cfd0d4; line-height:1.6;
    margin-top:8px; }
  .a-drawer .related { margin-top:18px; padding-top:14px;
    border-top:1px solid rgba(255,255,255,0.07); font-size:12px; }
  .a-drawer .related-item {
    display:flex; align-items:center; padding:6px 0;
    color:#a8a89e; cursor:pointer; transition:color 0.15s;
  }
  .a-drawer .related-item:hover { color:#fff; }
  .a-drawer .related-item .swatch {
    width:7px; height:7px; border-radius:50%; margin-right:8px;
  }

  /* Edge classes — contested edges only animate on hover (per design feedback) */
  .edge { stroke-opacity:0.18; stroke-width:0.6; pointer-events:none;
          transition: stroke-opacity 0.3s, stroke-width 0.3s; }
  .edge-contested {
    stroke-dasharray: 5 4;
    /* idle: no animation. hover: phase shimmer */
  }
  .edge-contested.shimmer-on {
    animation: contestedFlow 8s linear infinite;
  }
  @keyframes contestedFlow {
    0% { stroke-dashoffset: 0; }
    100% { stroke-dashoffset: -90; }
  }
  .edge-highlight { stroke-opacity:0.7; stroke-width:1.6; }
  .edge-faded { stroke-opacity:0.04 !important; }

  /* View-mode toggle */
  .mode-toggle {
    position:absolute; top:88px; right:24px;
    background:rgba(20,22,26,0.78); backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border:1px solid rgba(120,120,140,0.2);
    border-radius:999px; padding:4px;
    display:flex; z-index:11;
    box-shadow:0 12px 40px rgba(0,0,0,0.6);
  }
  .mode-toggle button {
    background:transparent; border:none;
    padding:7px 16px; border-radius:999px;
    color:#a8a89e; font-size:11px;
    letter-spacing:0.08em; cursor:pointer;
    font-family:inherit; font-weight:500;
    transition:all 0.18s;
  }
  .mode-toggle button:hover { color:#fff; }
  .mode-toggle button.active {
    background:rgba(124,92,255,0.25);
    color:#fff;
    box-shadow:inset 0 0 0 1px rgba(124,92,255,0.5);
  }

  /* Node states */
  .node { cursor:pointer; transition: filter 0.2s; }
  .node:hover { filter: drop-shadow(0 0 8px rgba(255,255,255,0.4)); }
  .node-faded { opacity: 0.12; }
  .node-contested-ring {
    fill:none; stroke:#B3261E; stroke-width:1; stroke-opacity:0.5;
    stroke-dasharray:3 2;
  }

  /* Star backdrop */
  .bg-star { fill:#cfd0d4; }
  .bg-star.twinkle1 { animation: tw1 9s infinite ease-in-out; }
  .bg-star.twinkle2 { animation: tw2 6s infinite ease-in-out; }
  @keyframes tw1 {0%,100%{opacity:0.1;}50%{opacity:0.3;}}
  @keyframes tw2 {0%,100%{opacity:0.2;}50%{opacity:0.5;}}

  /* Replicate CTA */
  .replicate-cta {
    position:absolute; bottom:24px; right:24px;
    background: rgba(124,92,255,0.15);
    border:1px solid rgba(124,92,255,0.5);
    border-radius:999px; padding:10px 18px; color:#9D89FF;
    font-size:12px; font-weight:500; letter-spacing:0.04em;
    cursor:pointer; transition:all 0.2s; z-index:10;
    text-decoration:none;
    backdrop-filter: blur(10px);
  }
  .replicate-cta:hover { background: rgba(124,92,255,0.25);
    color:#fff; transform: translateY(-1px); }
</style></head>
<body>
<div id="atlas-root">

  <div class="stats-banner">
    <div class="stat">
      <span class="pulse-dot"></span>
      <span style="font-size:10px; color:#00B26D;
                   text-transform:uppercase; letter-spacing:0.16em;">live</span>
    </div>
    <div class="stat"><span class="stat-num" id="ct-nodes">—</span>
      <span class="stat-label">visible nodes</span></div>
    <div class="stat"><span class="stat-num" id="ct-edges">—</span>
      <span class="stat-label">edges</span></div>
    <div class="stat"><span class="stat-num" id="ct-int">—</span>
      <span class="stat-label">interventions</span></div>
    <div class="stat"><span class="stat-num" id="ct-frm">—</span>
      <span class="stat-label">formulations</span></div>
    <div class="stat"><span class="stat-num" id="ct-hyp">—</span>
      <span class="stat-label">hypotheses</span></div>
    <div class="stat"><span class="stat-num" id="ct-src">—</span>
      <span class="stat-label">sources</span></div>
    <div class="stat"><span class="stat-num" id="ct-genes">1564</span>
      <span class="stat-label">genes (clustered)</span></div>
    <div class="stat"><span style="font-size:10px;
      color:#7a7a7f;">last refreshed<br/>
      <span id="updated" style="color:#cfd0d4; font-size:11px;
        font-family:'IBM Plex Mono',monospace;"></span></span></div>
  </div>

  <div class="mode-toggle" id="mode-toggle">
    <button data-mode="parent">Parent</button>
    <button data-mode="research" class="active">Research</button>
    <button data-mode="atlas">Atlas</button>
  </div>

  <div class="filter-sidebar">
    <input class="search-box" id="search" placeholder="search the atlas..." />

    <h3>Entity type</h3>
    <div class="filter-group" id="type-filters"></div>

    <h3>Status</h3>
    <div class="filter-group" id="status-filters">
      <div class="filter-row" data-status="active">
        <span class="swatch" style="background:#cfd0d4;"></span>
        active <span class="count" id="ct-active">0</span></div>
      <div class="filter-row" data-status="contested">
        <span class="swatch" style="background:#B3261E;"></span>
        contested <span class="count" id="ct-contested">0</span></div>
    </div>

    <h3 style="margin-top:8px;">Constellation</h3>
    <div class="filter-group" id="phe-filters"></div>
  </div>

  <svg id="atlas-svg"></svg>

  <div class="a-tooltip" id="tooltip"></div>

  <div class="a-drawer" id="drawer">
    <button class="close-btn" id="close-drawer">×</button>
    <div class="eyebrow" id="d-eyebrow">—</div>
    <h2 id="d-title">—</h2>
    <div class="meta" id="d-meta"></div>
    <div class="related" id="d-related"></div>
  </div>

  <a class="replicate-cta" href="#" id="replicate-link">
    Replicate this for your own knowledge →</a>
</div>

<script src="https://d3js.org/d3.v7.min.js"></script>
<script>
const PAYLOAD = __PAYLOAD__;
const NEBULA = __NEBULA__;
const TYPE_STYLE = {
  phenotype:    { color: null, size: 18, shape:"phenotype" },
  intervention: { color: "#e5e4df", size: 7, shape:"pill" },
  formulation:  { color: "#a8a89e", size: 4, shape:"diamond" },
  mechanism:    { color: "#7BB3FF", size: 9, shape:"diamond" },
  hypothesis:   { color: "#FFB36B", size: 6, shape:"circle" },
  biomarker:    { color: "#5BAE3C", size: 5, shape:"ring" },
  source:       { color: "#3a3a3f", size: 1.5, shape:"dot" },
};

const { nodes, edges, counts, last_updated } = PAYLOAD;

// Stats banner
document.getElementById("ct-nodes").textContent = counts.nodes_total_visible;
document.getElementById("ct-edges").textContent = counts.edges;
document.getElementById("ct-int").textContent = counts.interventions;
document.getElementById("ct-frm").textContent = counts.formulations;
document.getElementById("ct-hyp").textContent = counts.hypotheses;
document.getElementById("ct-src").textContent = counts.atlas_total_sources;
document.getElementById("updated").textContent = last_updated;

// Color for a node: phenotypes use NEBULA, others use type color
function nodeColor(n) {
  if (n.type === "phenotype") return NEBULA[n.id] || "#cfd0d4";
  if (n.type === "formulation" && n.parent_intervention_id) {
    // Inherit a hint from parent intervention's phenotype edge if available
  }
  return TYPE_STYLE[n.type]?.color || "#cfd0d4";
}

// SVG setup
const svg = d3.select("#atlas-svg");
const w = window.innerWidth, h = window.innerHeight;
svg.attr("viewBox", `0 0 ${w} ${h}`);

const root = svg.append("g");

// ── Background starfield (parallax) ─────────────────────────────────
function makeLCG(seed){let s=seed;return ()=>{s=(s*1103515245+12345)&0x7FFFFFFF;return s/0x7FFFFFFF;};}
const bg = root.append("g").attr("class","bg");
const rng = makeLCG(7);
for (let i = 0; i < 220; i++) {
  bg.append("circle")
    .attr("class", `bg-star twinkle${(i%2)+1}`)
    .attr("cx", rng() * w).attr("cy", rng() * h)
    .attr("r", 0.4 + rng() * 1.2)
    .attr("opacity", 0.15 + rng() * 0.4)
    .style("animation-delay", `${rng() * -10}s`);
}

const edgeGroup = root.append("g").attr("class","edges");
const nodeGroup = root.append("g").attr("class","nodes");

// ── Force simulation (tuned for fast equilibrium, not infinite jitter) ─
const sim = d3.forceSimulation(nodes)
  .force("link", d3.forceLink(edges).id(d => d.id).distance(d => {
    const k = d.kind;
    if (k === "form-int") return 32;
    if (k === "int-mech") return 80;
    if (k === "int-phe") return 100;
    if (k === "hyp-mech") return 70;
    if (k === "hyp-hyp") return 90;
    return 80;
  }).strength(0.18))
  .force("charge", d3.forceManyBody().strength(d => {
    const t = d.type;
    if (t === "phenotype") return -700;
    if (t === "intervention") return -260;
    if (t === "mechanism") return -350;
    if (t === "hypothesis") return -260;
    if (t === "formulation") return -50;
    if (t === "biomarker") return -100;
    return -30;
  }))
  .force("center", d3.forceCenter(w/2, h/2))
  .force("collide", d3.forceCollide().radius(d => (TYPE_STYLE[d.type]?.size || 6) + 4))
  // Aggressive alpha decay → reach equilibrium in ~5 seconds, then freeze.
  // This addresses ChatGPT design feedback A: graph should drift slowly,
  // not jitter continuously. Computational trustworthiness > biological liveness.
  .alphaDecay(0.04)
  .velocityDecay(0.5);

// After ~5 seconds, freeze positions to prevent perpetual drift
setTimeout(() => {
  sim.alphaTarget(0.0);
  // Soft-freeze: extremely low alpha but not stopped (allows hover interactions)
  sim.alpha(0.005);
}, 5500);

// ── Edges ──────────────────────────────────────────────────────────
const edgeSel = edgeGroup.selectAll("line")
  .data(edges).enter().append("line")
  .attr("class", d => "edge" + (d.contested ? " edge-contested" : ""))
  .attr("stroke", d => d.contested ? "#B3261E" : "#7a7a7f");

// Contested edges: dual-color rendering
edgeGroup.selectAll("line.edge-contested")
  .each(function(d){
    const ln = d3.select(this);
    ln.attr("stroke", "url(#contested-grad)");
  });

// Defs: contested gradient
const defs = svg.append("defs");
const cgrad = defs.append("linearGradient").attr("id", "contested-grad");
cgrad.append("stop").attr("offset","0%").attr("stop-color","#B3261E").attr("stop-opacity",0.7);
cgrad.append("stop").attr("offset","50%").attr("stop-color","#a8a89e").attr("stop-opacity",0.3);
cgrad.append("stop").attr("offset","100%").attr("stop-color","#00B26D").attr("stop-opacity",0.7);

// ── Nodes ──────────────────────────────────────────────────────────
const nodeSel = nodeGroup.selectAll("g")
  .data(nodes).enter().append("g")
  .attr("class", "node")
  .each(function(d) {
    const g = d3.select(this);
    const style = TYPE_STYLE[d.type];
    const color = nodeColor(d);
    if (d.type === "phenotype") {
      // Halo + core
      g.append("circle").attr("r", style.size * 1.6)
        .attr("fill", color).attr("opacity", 0.18);
      g.append("circle").attr("r", style.size).attr("fill", color);
    } else if (style.shape === "pill") {
      g.append("rect")
        .attr("x", -style.size).attr("y", -style.size * 0.45)
        .attr("width", style.size * 2).attr("height", style.size * 0.9)
        .attr("rx", style.size * 0.45)
        .attr("fill", color).attr("opacity", 0.85);
      if (d.status === "contested") {
        g.append("rect")
          .attr("x", -style.size - 2).attr("y", -style.size * 0.45 - 2)
          .attr("width", style.size * 2 + 4).attr("height", style.size * 0.9 + 4)
          .attr("rx", style.size * 0.45 + 2)
          .attr("fill", "none").attr("stroke", "#B3261E")
          .attr("stroke-width", 1).attr("stroke-dasharray", "2 2")
          .attr("opacity", 0.6);
      }
    } else if (style.shape === "diamond") {
      const s = style.size;
      g.append("polygon")
        .attr("points", `0,-${s} ${s},0 0,${s} -${s},0`)
        .attr("fill", color).attr("opacity", 0.85);
    } else if (style.shape === "ring") {
      g.append("circle").attr("r", style.size)
        .attr("fill", "none").attr("stroke", color).attr("stroke-width", 1.5)
        .attr("opacity", 0.85);
    } else {
      g.append("circle").attr("r", style.size).attr("fill", color)
        .attr("opacity", style.shape === "dot" ? 0.45 : 0.85);
    }

    // Always render label, but visibility controlled by zoom + view mode.
    // ChatGPT feedback C: adaptive label reveal thresholds.
    g.append("text")
      .attr("y", (style.size || 6) + 12)
      .attr("text-anchor", "middle")
      .attr("font-size", d.type === "phenotype" ? 10 : 9)
      .attr("font-weight", 500)
      .attr("fill", d.type === "phenotype" ? "#e5e4df" : "#a8a89e")
      .style("pointer-events", "none")
      .style("opacity", d.type === "phenotype" ? 1 :
             (d.type === "intervention" && d.score >= 70) ? 0.85 : 0)
      .text(d.name.slice(0, 28));
  })
  .call(d3.drag()
    .on("start", e => {
      if (!e.active) sim.alphaTarget(0.3).restart();
      e.subject.fx = e.subject.x; e.subject.fy = e.subject.y;
    })
    .on("drag", e => { e.subject.fx = e.x; e.subject.fy = e.y; })
    .on("end", e => {
      if (!e.active) sim.alphaTarget(0);
      e.subject.fx = null; e.subject.fy = null;
    }));

// Build neighbor index (1-hop) for hover-isolation
const neighbors = {};
edges.forEach(e => {
  const sid = e.source.id || e.source;
  const tid = e.target.id || e.target;
  (neighbors[sid] = neighbors[sid] || new Set()).add(tid);
  (neighbors[tid] = neighbors[tid] || new Set()).add(sid);
});

// Tooltip + drawer + neighborhood isolation on hover
const tooltip = d3.select("#tooltip");
nodeSel.on("mouseenter", (e, d) => {
  tooltip.style("opacity", 1)
    .style("left", (e.clientX + 14) + "px")
    .style("top", (e.clientY - 10) + "px")
    .html(`<div class="type">${d.type}${d.status === "contested" ? " · contested" : ""}</div>
           <div class="name">${d.name}</div>
           <div class="score">${d.id} · score ${d.score.toFixed(1)}</div>`);
  // ChatGPT feedback C: local neighborhood isolation on hover
  const nbrs = neighbors[d.id] || new Set();
  nodeSel.classed("node-faded", nd => nd.id !== d.id && !nbrs.has(nd.id));
  edgeSel
    .classed("edge-highlight", e2 => e2.source.id === d.id || e2.target.id === d.id)
    .classed("edge-faded", e2 => e2.source.id !== d.id && e2.target.id !== d.id)
    // ChatGPT feedback B: contested edges shimmer ONLY on hover, not idle
    .classed("shimmer-on", e2 =>
      e2.contested && (e2.source.id === d.id || e2.target.id === d.id));
})
.on("mousemove", (e) => {
  tooltip.style("left", (e.clientX + 14) + "px")
         .style("top", (e.clientY - 10) + "px");
})
.on("mouseleave", () => {
  tooltip.style("opacity", 0);
  nodeSel.classed("node-faded", false);
  edgeSel.classed("edge-highlight", false)
         .classed("edge-faded", false)
         .classed("shimmer-on", false);
  applyFilter();  // Re-apply filter state
})
.on("click", (e, d) => openDrawer(d));

function openDrawer(d) {
  document.getElementById("d-eyebrow").textContent =
    `${d.type} · ${d.id}${d.status==="contested" ? " · contested" : ""}`;
  const titleEl = document.getElementById("d-title");
  titleEl.textContent = d.name;
  titleEl.style.color = nodeColor(d);

  const meta = document.getElementById("d-meta");
  let metaHtml = `<strong>Score:</strong> ${d.score.toFixed(2)}<br/>`;
  if (d.evidence) metaHtml += `<strong>Evidence tier:</strong> ${d.evidence}<br/>`;
  if (d.parent_intervention_id) metaHtml += `<strong>Parent intervention:</strong> ${d.parent_intervention_id}<br/>`;
  if (d.pmid) metaHtml += `<strong>PMID:</strong> ${d.pmid}<br/>`;
  if (d.status === "contested") metaHtml += `<br/><span style="color:#FF6B6B;">⚠ Contested status — both directions of evidence preserved in atlas. Click related nodes to see countervailing evidence.</span>`;
  meta.innerHTML = metaHtml;

  // Related: nodes connected by edges
  const related = edges.filter(e => e.source.id === d.id || e.target.id === d.id)
    .map(e => e.source.id === d.id ? e.target : e.source).slice(0, 8);
  const relHtml = related.map(r => `
    <div class="related-item" data-id="${r.id}">
      <span class="swatch" style="background:${nodeColor(r)};"></span>
      <span style="margin-right:auto;">${r.name.slice(0, 38)}</span>
      <span style="font-family:monospace; font-size:10px; opacity:0.5;">${r.type}</span>
    </div>
  `).join("");
  document.getElementById("d-related").innerHTML =
    `<div style="font-size:10px; letter-spacing:0.16em;
       text-transform:uppercase; color:#7a7a7f; margin-bottom:8px;">
       connected (${related.length})</div>${relHtml || "<em>no connections in current view</em>"}`;
  document.querySelectorAll("#d-related .related-item").forEach(el => {
    el.addEventListener("click", () => {
      const id = el.dataset.id;
      const node = nodes.find(n => n.id === id);
      if (node) openDrawer(node);
    });
  });

  document.getElementById("drawer").classList.add("open");
}
document.getElementById("close-drawer").addEventListener("click", () => {
  document.getElementById("drawer").classList.remove("open");
});

// ── Filter sidebar (entity types) ─────────────────────────────────
const TYPES_ORDER = ["phenotype","intervention","formulation","mechanism","hypothesis","biomarker","source"];
const typeCounts = {}; nodes.forEach(n => { typeCounts[n.type] = (typeCounts[n.type]||0) + 1; });
const typeFilters = document.getElementById("type-filters");
const enabled = new Set(TYPES_ORDER);
TYPES_ORDER.forEach(t => {
  const row = document.createElement("div");
  row.className = "filter-row";
  row.dataset.type = t;
  const sw = TYPE_STYLE[t]?.color || "#cfd0d4";
  row.innerHTML = `<span class="swatch" style="background:${sw};"></span>
                   ${t}<span class="count">${typeCounts[t]||0}</span>`;
  row.addEventListener("click", () => {
    if (enabled.has(t)) { enabled.delete(t); row.classList.add("disabled"); }
    else { enabled.add(t); row.classList.remove("disabled"); }
    applyFilter();
  });
  typeFilters.appendChild(row);
});

// Status counts
document.getElementById("ct-active").textContent = nodes.filter(n => n.status==="active").length;
document.getElementById("ct-contested").textContent = nodes.filter(n => n.status==="contested").length;
const statusEnabled = new Set(["active","contested"]);
document.querySelectorAll("#status-filters .filter-row").forEach(row => {
  row.addEventListener("click", () => {
    const s = row.dataset.status;
    if (statusEnabled.has(s)) { statusEnabled.delete(s); row.classList.add("disabled"); }
    else { statusEnabled.add(s); row.classList.remove("disabled"); }
    applyFilter();
  });
});

// Phenotype filter: highlight one constellation
const pheFilters = document.getElementById("phe-filters");
let pheFocus = null;
[
  ["PHE-0001", "Cerebral folate"],
  ["PHE-0002", "Mitochondrial"],
  ["PHE-0003", "Immune-brain"],
  ["PHE-0004", "Gut–microbiome"],
  ["PHE-0007", "GABA / Cl⁻"],
  ["PHE-0008", "Walsh under-meth"],
].forEach(([pid, name]) => {
  const row = document.createElement("div");
  row.className = "filter-row";
  row.innerHTML = `<span class="swatch" style="background:${NEBULA[pid]};"></span>
                   ${name}`;
  row.addEventListener("click", () => {
    pheFocus = pheFocus === pid ? null : pid;
    document.querySelectorAll("#phe-filters .filter-row").forEach(r => r.classList.remove("disabled"));
    if (pheFocus) {
      document.querySelectorAll("#phe-filters .filter-row").forEach(r => {
        if (!r.innerHTML.includes(NEBULA[pheFocus])) r.classList.add("disabled");
      });
    }
    applyFilter();
  });
  pheFilters.appendChild(row);
});

// Search
let searchQ = "";
document.getElementById("search").addEventListener("input", e => {
  searchQ = e.target.value.toLowerCase().trim();
  applyFilter();
});

function applyFilter() {
  nodeSel.classed("node-faded", d => {
    let visible = enabled.has(d.type) && statusEnabled.has(d.status);
    if (searchQ) visible = visible && (
      d.name.toLowerCase().includes(searchQ) || d.id.toLowerCase().includes(searchQ));
    if (pheFocus && d.type !== "phenotype") {
      // Show only nodes connected to the focused phenotype
      const conn = edges.some(e =>
        (e.source.id === pheFocus && e.target.id === d.id) ||
        (e.target.id === pheFocus && e.source.id === d.id));
      visible = visible && conn;
    } else if (pheFocus && d.type === "phenotype") {
      visible = visible && d.id === pheFocus;
    }
    return !visible;
  });
  edgeSel.style("opacity", e => {
    const sv = enabled.has(e.source.type) && enabled.has(e.target.type) &&
               statusEnabled.has(e.source.status) && statusEnabled.has(e.target.status);
    if (!sv) return 0.03;
    if (pheFocus) {
      const conn = e.source.id === pheFocus || e.target.id === pheFocus;
      return conn ? 0.55 : 0.03;
    }
    return null;
  });
}

// ── Pan/zoom ───────────────────────────────────────────────────────
svg.call(d3.zoom().scaleExtent([0.4, 4]).on("zoom", e => {
  root.attr("transform", e.transform);
  // Adaptive label visibility — show more labels as user zooms in
  applyZoomLabels(e.transform.k);
}));

function applyZoomLabels(k) {
  // At zoom 1.0 (default): show only phenotypes + top-tier interventions
  // At zoom 1.5+: show all interventions
  // At zoom 2.5+: show formulations + hypotheses too
  nodeSel.selectAll("text").style("opacity", function(d) {
    if (d.type === "phenotype") return 1;
    if (d.type === "intervention") {
      if (k >= 1.5) return 0.85;
      return d.score >= 70 ? 0.85 : 0;
    }
    if (d.type === "hypothesis") return k >= 2.0 ? 0.7 : 0;
    if (d.type === "formulation") return k >= 2.5 ? 0.7 : 0;
    if (d.type === "mechanism") return k >= 1.8 ? 0.65 : 0;
    return k >= 3.0 ? 0.55 : 0;
  });
}

// ── View-mode toggle (Parent / Research / Atlas) ──────────────────
let viewMode = "research";
const VIEW_DENSITY = {
  parent:   {types: new Set(["phenotype","intervention"]),
             max_int: 12, label_score_threshold: 70},
  research: {types: new Set(["phenotype","intervention","formulation","mechanism","hypothesis","biomarker"]),
             max_int: 60, label_score_threshold: 60},
  atlas:    {types: new Set(["phenotype","intervention","formulation","mechanism","hypothesis","biomarker","source"]),
             max_int: 999, label_score_threshold: 0},
};

document.querySelectorAll("#mode-toggle button").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll("#mode-toggle button").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    viewMode = btn.dataset.mode;
    const cfg = VIEW_DENSITY[viewMode];
    // Update enabled set + sidebar
    enabled.clear();
    cfg.types.forEach(t => enabled.add(t));
    document.querySelectorAll("#type-filters .filter-row").forEach(row => {
      const t = row.dataset.type;
      if (cfg.types.has(t)) row.classList.remove("disabled");
      else row.classList.add("disabled");
    });
    // For "parent" mode: only show top N interventions by score
    if (viewMode === "parent") {
      const sortedInts = nodes.filter(n => n.type === "intervention")
        .sort((a, b) => b.score - a.score);
      const keepIds = new Set(sortedInts.slice(0, cfg.max_int).map(n => n.id));
      nodeSel.style("display", n =>
        (n.type === "intervention" && !keepIds.has(n.id)) ? "none" : null);
    } else {
      nodeSel.style("display", null);
    }
    applyFilter();
  });
});

// ── Tick ──────────────────────────────────────────────────────────
sim.on("tick", () => {
  edgeSel
    .attr("x1", d => d.source.x).attr("y1", d => d.source.y)
    .attr("x2", d => d.target.x).attr("y2", d => d.target.y);
  nodeSel.attr("transform", d => `translate(${d.x}, ${d.y})`);
});

// Replicate CTA
document.getElementById("replicate-link").addEventListener("click", e => {
  e.preventDefault();
  alert("See VAULT.md and VAULT_SETUP_GUIDE.md in the repo root for the full pattern. The same Connector / Briefer / Catcher pipeline you see running on this atlas (autonomous discoveries cron, Δ² overlay, daily ingestion) can be cloned for any chronic-condition knowledge base.");
});
</script>
</body></html>
""".replace("__PAYLOAD__", payload_json).replace("__NEBULA__", json.dumps(NEBULA))


if __name__ == "__main__":
    payload = build_atlas_payload()
    html = render_atlas_explorer(payload)
    out = Path(__file__).parent / "atlas_explorer_preview.html"
    out.write_text(html)
    print(f"Wrote {out}")
    print(f"Size: {len(html)} bytes")
    print()
    print(f"Atlas at-a-glance:")
    for k, v in payload["counts"].items():
        print(f"  {k}: {v}")
    print()
    print(f"Open: file://{out.resolve()}")
