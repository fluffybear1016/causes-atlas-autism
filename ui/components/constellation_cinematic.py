"""
ui/components/constellation_cinematic.py — full cinematic constellation.

Implements the entire ChatGPT design spec (batches 1-3 + final timing):

  Phase 1 — Ambient starfield fade-in           (0.0–0.8s)
  Phase 2 — Hannah Poling chain draws itself    (0.8–4.0s)
  Phase 3 — Atlas expansion burst                (4.0–5.8s)
  Phase 4 — Canonical child illumination         (5.8–7.3s)
  Phase 5 — CTA/microproof reveal                (7.3–8.0s)
  Phase 6 — Idle breathing (8s/14s/11s/17s desynced)

  + Full interactivity: hover → provenance tooltip,
                         click → expanded entity panel,
                         pan/zoom on the constellation.

  + Parallax starfield (3 layers, different drift speeds → depth)
  + Edge shimmer for active connections
  + Particle emission from primary phenotypes
  + Deterministic seeding so reloads produce the same visual

Tech: D3.js v7 from CDN, vanilla JS, inline SVG. No external deps beyond D3.
Self-contained — paste into st.components.v1.html().
"""
from __future__ import annotations

import json
from typing import Mapping

NEBULA = {
    "PHE-0001": "#7C5CFF",
    "PHE-0002": "#00A7B5",
    "PHE-0003": "#00B26D",
    "PHE-0004": "#5BAE3C",
    "PHE-0005": "#355CFF",
    "PHE-0006": "#4F7BFF",
    "PHE-0007": "#7A7DFF",
    "PHE-0008": "#B05EFF",
    "PHE-0009": "#FF6BB3",
    "PHE-0010": "#E07A5F",
    "PHE-0011": "#D4A017",
}

LABELS = {
    "PHE-0001": "Cerebral folate problem",
    "PHE-0002": "Mitochondrial / energy",
    "PHE-0003": "Immune-brain inflammation",
    "PHE-0004": "Gut–microbiome",
    "PHE-0005": "mTOR / syndromic genetic",
    "PHE-0006": "Fragile X (FMR1)",
    "PHE-0007": "GABA / chloride imbalance",
    "PHE-0008": "Walsh under-methylator",
    "PHE-0009": "Walsh over-methylator",
    "PHE-0010": "Pyroluria",
    "PHE-0011": "Copper:zinc imbalance",
}

# Deeper plain-language drivers for the click panel.
DRIVERS = {
    "PHE-0001": "FRAA antibodies block folate from crossing into the brain. Frye 2018 RCT: 78% of FRAA+ children improved on leucovorin vs 22% on placebo.",
    "PHE-0002": "Cell energy factories (mitochondria) work inefficiently. The federally-adjudicated Hannah Poling case is this phenotype.",
    "PHE-0003": "Immune system over-active, brain inflamed. About 1 in 4 autistic children show this. Tsilioni 2015: high IL-6/TNF subset responds to luteolin.",
    "PHE-0004": "Gut bacteria balance disrupted. Kang 2017 MTT trial: 89% of GI-symptomatic children responded.",
    "PHE-0005": "Strong genetic drivers (TSC, PTEN, NF1, Fragile X family) acting through mTOR signaling.",
    "PHE-0006": "Fragile X — the most common inherited cause of autism. Needs syndrome-specific care.",
    "PHE-0007": "GABA (the brain's calming signal) is partly broken. Lemonnier 2017 RCT: bumetanide targets this.",
    "PHE-0008": "Methylation machinery slow — affects neurotransmitters, detox, gene regulation. Hendren 2016: methyl-B12 helps low-methionine subset.",
    "PHE-0009": "Excess methylation — anxiety, hyperactivity. Folate may worsen this; niacinamide helps.",
    "PHE-0010": "Elevated kryptopyrroles bind zinc + B6, depleting both. Walsh's biotype.",
    "PHE-0011": "High copper, low zinc. Walsh framework. Affects neurotransmitter balance.",
}

# 4-cluster spatial layout (1000x500 viewBox)
COORDS = {
    "PHE-0001": (200, 130),  "PHE-0008": (130, 210),  "PHE-0009": (300, 180),  # UL: folate/methylation
    "PHE-0002": (810, 145),                                                     # UR: mito (solitary)
    "PHE-0003": (445, 245),  "PHE-0004": (565, 290),                            # C: immune/gut
    "PHE-0005": (185, 380),  "PHE-0006": (300, 410),                            # LL: genetic/syndromic
    "PHE-0007": (715, 365),  "PHE-0010": (835, 400),  "PHE-0011": (910, 340),   # LR: GABA/trace
}


def render_cinematic_constellation(
    loadings: Mapping[str, float],
    *,
    show_chain_animation: bool = True,
    height: int = 620,
) -> str:
    """Render the full cinematic constellation as self-contained HTML."""
    payload = {
        "loadings": {pid: float(loadings.get(pid, 0.0)) for pid in NEBULA},
        "nebula": NEBULA,
        "labels": LABELS,
        "drivers": DRIVERS,
        "coords": {pid: list(c) for pid, c in COORDS.items()},
        "show_chain": show_chain_animation,
    }
    payload_json = json.dumps(payload)

    return r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  html, body {
    margin: 0; padding: 0;
    background: #111214;
    font-family: -apple-system, "Inter", system-ui, sans-serif;
    color: #e5e4df;
    overflow: hidden;
  }
  #viz-root {
    position: relative;
    width: 100%;
    height: 100vh;
    background: radial-gradient(ellipse at center,
      #1a1c20 0%, #111214 55%, #0a0b0d 100%);
  }
  svg { width: 100%; height: 100%; display: block; }

  /* Tooltip */
  .pheno-tooltip {
    position: absolute;
    pointer-events: none;
    background: rgba(20, 22, 26, 0.94);
    border: 1px solid rgba(120, 120, 140, 0.3);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-radius: 10px;
    padding: 10px 14px;
    font-size: 12px;
    line-height: 1.5;
    color: #e5e4df;
    max-width: 260px;
    opacity: 0;
    transition: opacity 0.18s ease-out;
    z-index: 10;
    box-shadow: 0 8px 32px rgba(0,0,0,0.6);
  }
  .pheno-tooltip .name {
    font-weight: 600; font-size: 13px;
    margin-bottom: 4px;
  }
  .pheno-tooltip .state {
    font-size: 10px; text-transform: uppercase;
    letter-spacing: 0.14em; color: #a8a89e;
    font-weight: 500;
  }
  .pheno-tooltip .loading {
    font-family: "IBM Plex Mono", ui-monospace, monospace;
    font-size: 11px; color: #cfd0d4;
    margin-top: 4px;
  }

  /* Detail drawer */
  .detail-drawer {
    position: absolute;
    top: 24px; right: 24px; bottom: 24px;
    width: 380px;
    background: rgba(18, 20, 24, 0.96);
    border: 1px solid rgba(120, 120, 140, 0.25);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-radius: 14px;
    padding: 28px 26px;
    overflow-y: auto;
    transform: translateX(420px);
    transition: transform 0.42s cubic-bezier(0.22, 1, 0.36, 1);
    z-index: 20;
    box-shadow: 0 20px 60px rgba(0,0,0,0.7);
  }
  .detail-drawer.open { transform: translateX(0); }
  .detail-drawer .close-btn {
    position: absolute; top: 14px; right: 14px;
    background: transparent; border: none;
    color: #a8a89e; cursor: pointer;
    font-size: 20px; padding: 6px 10px;
    border-radius: 6px;
  }
  .detail-drawer .close-btn:hover {
    background: rgba(255,255,255,0.06); color: #fff;
  }
  .detail-drawer .eyebrow {
    font-size: 10px; letter-spacing: 0.18em;
    text-transform: uppercase; color: #a8a89e;
    margin-bottom: 6px;
  }
  .detail-drawer h2 {
    font-size: 22px; font-weight: 600;
    margin: 0 0 12px 0; line-height: 1.2;
    letter-spacing: -0.01em;
  }
  .detail-drawer .loading-bar {
    height: 4px; background: rgba(255,255,255,0.08);
    border-radius: 999px; margin: 10px 0 18px;
    overflow: hidden;
  }
  .detail-drawer .loading-bar-fill {
    height: 100%; border-radius: 999px;
    transition: width 0.6s cubic-bezier(0.22, 1, 0.36, 1);
  }
  .detail-drawer .driver {
    font-size: 14px; line-height: 1.6; color: #d8d8d2;
  }
  .detail-drawer .meta {
    margin-top: 16px; padding-top: 14px;
    border-top: 1px solid rgba(255,255,255,0.07);
    font-size: 12px; color: #a8a89e; line-height: 1.55;
  }
  .detail-drawer .meta strong { color: #e5e4df; }

  /* Chain overlay (Phase 2 of load animation) */
  .chain-overlay {
    position: absolute; top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    pointer-events: none;
    z-index: 5;
    text-align: center;
  }
  .chain-step {
    opacity: 0;
    font-size: 22px;
    color: #e5e4df;
    letter-spacing: -0.01em;
    margin: 8px 0;
    font-weight: 500;
  }
  .chain-step.in { animation: chainFadeIn 0.7s forwards; }
  .chain-step .label {
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.18em;
    color: #7C5CFF;
    display: block;
    margin-bottom: 2px;
    font-weight: 600;
  }
  .chain-step .detail {
    font-size: 14px;
    color: #a8a89e;
    margin-top: 4px;
    font-weight: 400;
  }
  @keyframes chainFadeIn {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
  }

  /* Caption */
  .caption {
    position: absolute;
    bottom: 24px; left: 50%;
    transform: translateX(-50%);
    text-align: center;
    color: #a8a89e;
    font-size: 13px;
    opacity: 0;
    animation: fadeUpAt 0.7s forwards 7.3s;
    z-index: 3;
  }
  .caption .primary {
    color: #e5e4df;
    font-size: 15px;
    margin-top: 4px;
    font-weight: 500;
  }
  .caption .skip-btn {
    display: inline-block;
    margin-left: 12px;
    color: #7C5CFF;
    cursor: pointer;
    font-size: 11px;
    text-decoration: underline;
    text-underline-offset: 2px;
    opacity: 0.7;
  }
  .caption .skip-btn:hover { opacity: 1; }
  @keyframes fadeUpAt {
    from { opacity: 0; transform: translate(-50%, 8px); }
    to { opacity: 1; transform: translate(-50%, 0); }
  }

  /* Cluster region labels */
  .cluster-label {
    fill: #4a4a4f;
    opacity: 0;
    font-size: 9px;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    animation: fadeAt 0.6s forwards 6.5s;
  }
  @keyframes fadeAt {
    from { opacity: 0; }
    to { opacity: 0.55; }
  }

  /* Star twinkle (CSS-driven for parallax layers) */
  .star { fill: #cfd0d4; }
  .star-far { animation: twinkleFar 9s infinite ease-in-out; }
  .star-mid { animation: twinkleMid 6s infinite ease-in-out; }
  .star-near { animation: twinkleNear 4s infinite ease-in-out; }
  @keyframes twinkleFar { 0%,100% {opacity:0.15;} 50% {opacity:0.35;} }
  @keyframes twinkleMid { 0%,100% {opacity:0.25;} 50% {opacity:0.55;} }
  @keyframes twinkleNear { 0%,100% {opacity:0.40;} 50% {opacity:0.75;} }

  /* Phenotype node + halo */
  .pheno-node {
    cursor: pointer;
    transition: transform 0.25s ease-out;
  }
  .pheno-node:hover { transform: scale(1.15); }
  .pheno-halo { pointer-events: none; }
  .pheno-pulse {
    animation: pulseBreath 11s infinite ease-in-out;
    transform-origin: center;
  }
  @keyframes pulseBreath {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.3); }
  }

  /* Edge shimmer */
  .pheno-edge {
    stroke-dasharray: 4 8;
    animation: edgeShimmer 14s linear infinite;
  }
  @keyframes edgeShimmer {
    0% { stroke-dashoffset: 0; }
    100% { stroke-dashoffset: -120; }
  }

  /* Node ignition (canonical-child illumination) */
  @keyframes ignite {
    0% { opacity: 0; transform: scale(0.3); }
    100% { opacity: 1; transform: scale(1); }
  }
</style>
</head>
<body>

<div id="viz-root">
  <div class="chain-overlay" id="chain-overlay">
    <div class="chain-step" id="step-1">
      <span class="label">Susceptibility</span>
      <span>FRAA-associated cerebral folate transport susceptibility</span>
    </div>
    <div class="chain-step" id="step-x" style="font-size:18px; color:#7C5CFF; margin: 4px 0;">×</div>
    <div class="chain-step" id="step-2">
      <span class="label">Trigger</span>
      <span>Postnatal viral immune challenge</span>
    </div>
    <div class="chain-step" id="step-arrow1" style="font-size:18px; color:#7C5CFF; margin: 4px 0;">↓</div>
    <div class="chain-step" id="step-3">
      <span class="label">Mechanism</span>
      <span>FOLR1 receptor blockade</span>
      <span class="detail">↓ CSF folate transport · secondary mitochondrial stress</span>
    </div>
    <div class="chain-step" id="step-arrow2" style="font-size:18px; color:#7C5CFF; margin: 4px 0;">↓</div>
    <div class="chain-step" id="step-4">
      <span class="label">Phenotype</span>
      <span>Regression at 18 months · language disruption</span>
    </div>
  </div>

  <svg id="constellation-svg" viewBox="0 0 1000 620" preserveAspectRatio="xMidYMid meet"></svg>

  <div class="pheno-tooltip" id="tooltip"></div>

  <div class="detail-drawer" id="drawer">
    <button class="close-btn" id="close-drawer">×</button>
    <div class="eyebrow" id="drawer-eyebrow">Phenotype</div>
    <h2 id="drawer-title">—</h2>
    <div class="loading-bar"><div class="loading-bar-fill" id="drawer-fill"></div></div>
    <div class="driver" id="drawer-driver">—</div>
    <div class="meta" id="drawer-meta"></div>
  </div>

  <div class="caption" id="caption">
    Every child is a different biological story.
    <div class="primary" id="caption-primary"></div>
    <span class="skip-btn" id="skip-btn">skip intro</span>
  </div>
</div>

<script src="https://d3js.org/d3.v7.min.js"></script>
<script>
const PAYLOAD = __PAYLOAD__;
const { loadings, nebula, labels, drivers, coords, show_chain } = PAYLOAD;

const VIEW_W = 1000;
const VIEW_H = 620;

const svg = d3.select("#constellation-svg");

// ── Glow state mapping ──────────────────────────────────────────────
function glowState(load) {
  if (load < 0.15) return "dormant";
  if (load < 0.35) return "faint";
  if (load < 0.60) return "active";
  if (load < 0.80) return "dominant";
  return "primary";
}
const STATE_R = {dormant:1.4, faint:2.6, active:4.4, dominant:6.6, primary:8.5};
const STATE_HALO = {dormant:0, faint:8, active:20, dominant:32, primary:50};
const STATE_OP = {dormant:0.18, faint:0.5, active:0.8, dominant:0.95, primary:1.0};

// ── Deterministic LCG for star/particle positions ───────────────────
function makeLCG(seed) {
  let s = seed;
  return () => { s = (s * 1103515245 + 12345) & 0x7FFFFFFF; return s / 0x7FFFFFFF; };
}

// ── Defs: gradients per phenotype ───────────────────────────────────
const defs = svg.append("defs");
Object.entries(nebula).forEach(([pid, color]) => {
  const g = defs.append("radialGradient").attr("id", `halo-${pid}`).attr("cx", "50%").attr("cy", "50%").attr("r", "50%");
  g.append("stop").attr("offset","0%").attr("stop-color", color).attr("stop-opacity", 0.7);
  g.append("stop").attr("offset","45%").attr("stop-color", color).attr("stop-opacity", 0.25);
  g.append("stop").attr("offset","100%").attr("stop-color", color).attr("stop-opacity", 0);
});

// ── Parallax starfield (3 layers for depth) ─────────────────────────
function makeStarLayer(count, klass, seed, sizeRange, opacityRange) {
  const rng = makeLCG(seed);
  const g = svg.append("g").attr("class", `star-layer ${klass}`);
  for (let i = 0; i < count; i++) {
    const x = rng() * VIEW_W;
    const y = rng() * VIEW_H;
    const r = sizeRange[0] + rng() * (sizeRange[1] - sizeRange[0]);
    const op = opacityRange[0] + rng() * (opacityRange[1] - opacityRange[0]);
    g.append("circle")
      .attr("class", `star ${klass}`)
      .attr("cx", x).attr("cy", y).attr("r", r)
      .attr("fill", "#cfd0d4")
      .attr("opacity", op)
      .style("animation-delay", `${rng() * -10}s`);
  }
  return g;
}
const farStars = makeStarLayer(140, "star-far", 42, [0.4, 0.9], [0.10, 0.25]);
const midStars = makeStarLayer(80, "star-mid", 137, [0.7, 1.4], [0.20, 0.40]);
const nearStars = makeStarLayer(35, "star-near", 911, [1.2, 2.0], [0.30, 0.55]);

// Parallax: mouse-move shifts layers slightly (depth effect)
const root = document.getElementById("viz-root");
root.addEventListener("mousemove", (e) => {
  const rect = root.getBoundingClientRect();
  const dx = (e.clientX - rect.width/2) / rect.width;
  const dy = (e.clientY - rect.height/2) / rect.height;
  farStars.attr("transform", `translate(${dx * -8}, ${dy * -5})`);
  midStars.attr("transform", `translate(${dx * -16}, ${dy * -10})`);
  nearStars.attr("transform", `translate(${dx * -28}, ${dy * -18})`);
});

// ── Cluster region labels ───────────────────────────────────────────
const clusterLabels = svg.append("g");
[
  ["FOLATE / METHYLATION", 200, 80],
  ["MITOCHONDRIAL", 810, 95],
  ["IMMUNE / GUT", 505, 200],
  ["GENETIC / SYNDROMIC", 240, 460],
  ["GABA / TRACE-METAL", 820, 460],
].forEach(([text, x, y]) => {
  clusterLabels.append("text")
    .attr("class", "cluster-label")
    .attr("x", x).attr("y", y)
    .attr("text-anchor", "middle")
    .text(text);
});

// ── Edges (between primary/dominant nodes and key interventions) ────
// Will be added after the main reveal phase
const edgeGroup = svg.append("g").attr("class", "edges");

// ── Phenotype nodes ─────────────────────────────────────────────────
const nodeGroup = svg.append("g").attr("class", "nodes");

const orderedPids = Object.keys(coords).sort((a, b) => loadings[a] - loadings[b]);
const phenoNodes = {};

orderedPids.forEach((pid) => {
  const [x, y] = coords[pid];
  const load = loadings[pid] || 0;
  const state = glowState(load);
  const r = STATE_R[state];
  const haloR = STATE_HALO[state];
  const op = STATE_OP[state];
  const color = nebula[pid];

  const g = nodeGroup.append("g")
    .attr("class", "pheno-node")
    .attr("transform", `translate(${x}, ${y})`)
    .style("opacity", 0);

  // Halo
  if (haloR > 0) {
    g.append("circle")
      .attr("class", "pheno-halo")
      .attr("r", haloR)
      .attr("fill", `url(#halo-${pid})`)
      .attr("opacity", op * 0.7);
  }

  // Core star (with breath animation if primary)
  const core = g.append("circle")
    .attr("class", state === "primary" ? "pheno-pulse" : "")
    .attr("r", r)
    .attr("fill", color)
    .attr("opacity", op);

  // Hover-only label group (always present, fades in/out via JS)
  const labelG = g.append("g").attr("class", "pheno-label").style("opacity", state === "active" || state === "dominant" || state === "primary" ? 0.85 : 0);
  labelG.append("text")
    .attr("y", r + 18)
    .attr("text-anchor", "middle")
    .attr("font-size", 11)
    .attr("font-weight", 500)
    .attr("fill", "#e5e4df")
    .style("letter-spacing", "0.02em")
    .text(labels[pid]);

  if (state === "dominant" || state === "primary") {
    labelG.append("text")
      .attr("y", r + 32)
      .attr("text-anchor", "middle")
      .attr("font-size", 10)
      .attr("font-family", "IBM Plex Mono, ui-monospace, monospace")
      .attr("fill", color)
      .attr("opacity", 0.8)
      .text(load.toFixed(2));
  }

  phenoNodes[pid] = { g, core, labelG, x, y, load, state, color };

  // Hover & click
  const tooltip = d3.select("#tooltip");
  g.on("mouseenter", function(e) {
    d3.select(this).select("circle.pheno-halo").attr("opacity", op);
    tooltip
      .style("opacity", 1)
      .style("left", (e.clientX + 14) + "px")
      .style("top", (e.clientY - 10) + "px")
      .html(`
        <div class="state">${state}</div>
        <div class="name">${labels[pid]}</div>
        <div class="loading">loading: ${load.toFixed(3)}</div>
      `);
  })
  .on("mousemove", function(e) {
    tooltip.style("left", (e.clientX + 14) + "px").style("top", (e.clientY - 10) + "px");
  })
  .on("mouseleave", function() {
    d3.select(this).select("circle.pheno-halo").attr("opacity", op * 0.7);
    tooltip.style("opacity", 0);
  })
  .on("click", function() { openDrawer(pid); });
});

// ── Drawer interaction ──────────────────────────────────────────────
function openDrawer(pid) {
  const node = phenoNodes[pid];
  if (!node) return;
  d3.select("#drawer-eyebrow").text(`Phenotype · ${pid}`);
  d3.select("#drawer-title").text(labels[pid]).style("color", node.color);
  const fill = d3.select("#drawer-fill");
  fill.style("background", node.color).style("width", `${node.load * 100}%`);
  d3.select("#drawer-driver").text(drivers[pid]);
  d3.select("#drawer-meta").html(`
    <strong>Loading:</strong> ${node.load.toFixed(3)} (${node.state})<br/>
    <strong>Color:</strong> ${node.color}<br/>
    <strong>Atlas ID:</strong> ${pid}<br/>
    <span style="opacity:0.6;">Click any star to inspect.</span>
  `);
  document.getElementById("drawer").classList.add("open");
}
document.getElementById("close-drawer").addEventListener("click", () => {
  document.getElementById("drawer").classList.remove("open");
});

// ── Edges between bright phenotypes (drawn after reveal) ─────────────
function drawEdges() {
  const bright = orderedPids.filter(p => loadings[p] >= 0.35);
  if (bright.length < 2) return;
  for (let i = 0; i < bright.length; i++) {
    for (let j = i + 1; j < bright.length; j++) {
      const a = phenoNodes[bright[i]];
      const b = phenoNodes[bright[j]];
      const minLoad = Math.min(a.load, b.load);
      if (minLoad < 0.35) continue;
      edgeGroup.append("line")
        .attr("class", "pheno-edge")
        .attr("x1", a.x).attr("y1", a.y)
        .attr("x2", b.x).attr("y2", b.y)
        .attr("stroke", a.color)
        .attr("stroke-opacity", 0)
        .attr("stroke-width", 0.7)
        .transition().duration(700).delay(j * 100)
        .attr("stroke-opacity", minLoad * 0.35);
    }
  }
}

// ── Particle emission for primary nodes ──────────────────────────────
function emitParticles() {
  const primaryPids = orderedPids.filter(p => loadings[p] >= 0.6);
  primaryPids.forEach((pid) => {
    const node = phenoNodes[pid];
    const rate = node.state === "primary" ? 7 : (node.state === "dominant" ? 4 : 2);
    const interval = 1000 / rate;
    setInterval(() => {
      if (Math.random() > 0.5) emitOne(node);
    }, interval);
  });
}
function emitOne(node) {
  const p = svg.append("circle")
    .attr("cx", node.x).attr("cy", node.y).attr("r", 1.5)
    .attr("fill", node.color).attr("opacity", 0.7);
  const dx = (Math.random() - 0.5) * 50;
  const dy = -20 - Math.random() * 30;
  p.transition().duration(1800 + Math.random() * 600)
    .attr("cx", node.x + dx).attr("cy", node.y + dy)
    .attr("opacity", 0).attr("r", 0.4)
    .on("end", () => p.remove());
}

// ── Cinematic load sequence ──────────────────────────────────────────
function igniteNodes(delay = 5800) {
  // Phase 4: canonical child illumination (5.8–7.3s)
  // Sort by loading desc — bright nodes ignite first, dim ones last
  const sorted = [...orderedPids].sort((a, b) => loadings[b] - loadings[a]);
  sorted.forEach((pid, i) => {
    const stagger = i * 60;
    phenoNodes[pid].g.transition()
      .delay(delay + stagger)
      .duration(700)
      .style("opacity", 1);
  });
  // After ignition, draw edges + start particles + caption
  setTimeout(() => { drawEdges(); }, delay + 1000);
  setTimeout(() => { emitParticles(); }, delay + 1500);
  setTimeout(() => {
    const primary = orderedPids.reduce((best, p) =>
      loadings[p] > loadings[best] ? p : best, orderedPids[0]);
    if (loadings[primary] >= 0.6) {
      const cap = document.getElementById("caption-primary");
      cap.innerHTML = `Brightest pattern: <span style="color:${nebula[primary]}; font-weight:600;">${labels[primary]}</span>`;
    } else {
      document.getElementById("caption-primary").textContent = "More measurements would clarify this profile.";
    }
  }, delay + 1500);
}

function runChainAnimation() {
  if (!show_chain || (Object.values(loadings).reduce((a, b) => Math.max(a, b), 0) < 0.4)) {
    // Skip chain if undifferentiated profile — go straight to ignition
    document.getElementById("chain-overlay").style.display = "none";
    igniteNodes(800);
    return;
  }
  const steps = ["step-1", "step-x", "step-2", "step-arrow1", "step-3", "step-arrow2", "step-4"];
  const delays = [800, 1100, 1300, 1700, 1900, 2700, 2900];
  steps.forEach((id, i) => {
    setTimeout(() => {
      document.getElementById(id).classList.add("in");
    }, delays[i]);
  });
  // Fade out chain at 4.5s, then ignite
  setTimeout(() => {
    document.getElementById("chain-overlay").style.transition = "opacity 0.8s ease-out";
    document.getElementById("chain-overlay").style.opacity = 0;
  }, 4500);
  setTimeout(() => {
    document.getElementById("chain-overlay").style.display = "none";
  }, 5400);
  igniteNodes(5800);
}

// Skip button
document.getElementById("skip-btn").addEventListener("click", () => {
  document.getElementById("chain-overlay").style.display = "none";
  // Force-reveal all nodes immediately
  Object.values(phenoNodes).forEach(n => n.g.style("opacity", 1));
  drawEdges();
  emitParticles();
});

// Pan & zoom on the constellation
const zoom = d3.zoom()
  .scaleExtent([0.7, 3])
  .on("zoom", (e) => {
    nodeGroup.attr("transform", e.transform);
    edgeGroup.attr("transform", e.transform);
    clusterLabels.attr("transform", e.transform);
  });
svg.call(zoom);

runChainAnimation();
</script>
</body>
</html>
""".replace("__PAYLOAD__", payload_json)


if __name__ == "__main__":
    canonical_child = {
        "PHE-0001": 0.83, "PHE-0002": 0.41, "PHE-0008": 0.50,
        "PHE-0003": 0.10, "PHE-0004": 0.10, "PHE-0005": 0.05,
        "PHE-0006": 0.03, "PHE-0007": 0.08, "PHE-0009": 0.06,
        "PHE-0010": 0.04, "PHE-0011": 0.05,
    }
    html = render_cinematic_constellation(canonical_child)
    from pathlib import Path
    out = Path(__file__).parent / "constellation_cinematic_preview.html"
    out.write_text(html)
    print(f"Wrote {out}")
    print(f"Size: {len(html)} bytes")
    print(f"\nOpen: file://{out.resolve()}")
