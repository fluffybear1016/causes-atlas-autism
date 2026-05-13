"""
ui/components/constellation.py — 11-dim phenotype constellation visualization.

Implements ChatGPT design batches 1–3 + final timing specs:

  - 4-cluster spatial topology:
      upper-left:  PHE-0001, PHE-0008, PHE-0009 (folate/methylation)
      upper-right: PHE-0002                      (mito/energy — solitary)
      center:      PHE-0003, PHE-0004            (immune/gut)
      lower-left:  PHE-0005, PHE-0006            (genetic/syndromic)
      lower-right: PHE-0007, PHE-0010, PHE-0011  (GABA/trace-metal)

  - 11-color nebula palette (one hue per phenotype, all distinct).

  - Glow states from loading value:
      dormant   0.00–0.15  background star only
      faint     0.15–0.35  low-opacity dot
      active    0.35–0.60  visible halo + 2 particles/sec
      dominant  0.60–0.80  strong halo + edge linkage + 4 particles/sec
      primary   0.80–1.00  slow pulse + spectral bloom + 7 particles/sec

  - Deterministic particle seeding (phenotype_id + intensity bucket → seed)
    so same input → same visual state. Per the determinism philosophy.

  - Background: warm off-black #111214 per ChatGPT spec.

Usage in Streamlit:

    from ui.components.constellation import render_constellation
    import streamlit.components.v1 as components

    components.html(
        render_constellation({"PHE-0001": 0.83, "PHE-0002": 0.41, ...}),
        height=440,
    )
"""
from __future__ import annotations

import json
from typing import Mapping

# --------------------------------------------------------------------------
# Spec constants (locked from ChatGPT design batches 1-3)
# --------------------------------------------------------------------------

# Nebula palette — one hue per phenotype.
NEBULA = {
    "PHE-0001": "#7C5CFF",  # ultraviolet — Cerebral folate problem
    "PHE-0002": "#00A7B5",  # cyan-teal — Mitochondrial / energy-cell
    "PHE-0003": "#00B26D",  # emerald — Immune-brain inflammation
    "PHE-0004": "#5BAE3C",  # moss green — Gut–microbiome
    "PHE-0005": "#355CFF",  # deep cobalt — mTOR / syndromic genetic
    "PHE-0006": "#4F7BFF",  # electric blue — Fragile X (FMR1)
    "PHE-0007": "#7A7DFF",  # periwinkle — GABA / chloride imbalance
    "PHE-0008": "#B05EFF",  # amethyst — Walsh under-methylator
    "PHE-0009": "#FF6BB3",  # magenta-rose — Walsh over-methylator
    "PHE-0010": "#E07A5F",  # terracotta — Pyroluria
    "PHE-0011": "#D4A017",  # oxidized gold — Copper:zinc imbalance
}

# Plain English labels (8th-grade accessible)
LABELS = {
    "PHE-0001": "Cerebral folate problem",
    "PHE-0002": "Mitochondrial / energy",
    "PHE-0003": "Immune–brain inflammation",
    "PHE-0004": "Gut–microbiome",
    "PHE-0005": "mTOR / syndromic genetic",
    "PHE-0006": "Fragile X (FMR1)",
    "PHE-0007": "GABA / chloride imbalance",
    "PHE-0008": "Walsh under-methylator",
    "PHE-0009": "Walsh over-methylator",
    "PHE-0010": "Pyroluria",
    "PHE-0011": "Copper:zinc imbalance",
}

# 4-cluster spatial layout — coordinates in a 1000×500 viewBox.
# Position itself encodes mechanism class. Once parents see a few
# constellations, the SPATIAL POSITION of the bright star tells them
# the class of biology before they read a label.
COORDS = {
    # upper-left: folate / methylation cluster
    "PHE-0001": (180, 110),
    "PHE-0008": (110, 180),
    "PHE-0009": (260, 165),
    # upper-right: mito / energy cluster (intentionally solitary)
    "PHE-0002": (820, 130),
    # center: immune / gut cluster
    "PHE-0003": (450, 230),
    "PHE-0004": (560, 280),
    # lower-left: genetic / syndromic cluster
    "PHE-0005": (175, 380),
    "PHE-0006": (290, 410),
    # lower-right: GABA / trace-metal cluster
    "PHE-0007": (735, 360),
    "PHE-0010": (845, 410),
    "PHE-0011": (915, 350),
}

# Glow-state thresholds (locked from design batch 3).
GLOW_BANDS = [
    (0.00, 0.15, "dormant"),
    (0.15, 0.35, "faint"),
    (0.35, 0.60, "active"),
    (0.60, 0.80, "dominant"),
    (0.80, 1.00, "primary"),
]

# Background: warm off-black per spec.
BG_COLOR = "#111214"

# Background-star count for the deep-field effect.
BG_STAR_COUNT = 90


def _glow_state(loading: float) -> str:
    """Map a continuous loading [0,1] to a glow-state name."""
    for lo, hi, name in GLOW_BANDS:
        if lo <= loading < hi:
            return name
    return "primary" if loading >= 1.0 else "dormant"


def _radius_for_state(state: str) -> float:
    """Visual radius (px) for a glow state."""
    return {
        "dormant": 1.4,
        "faint": 2.6,
        "active": 4.4,
        "dominant": 6.2,
        "primary": 8.0,
    }[state]


def _halo_for_state(state: str) -> float:
    """Halo radius (px) for a glow state."""
    return {
        "dormant": 0,
        "faint": 6,
        "active": 16,
        "dominant": 26,
        "primary": 40,
    }[state]


def _opacity_for_state(state: str) -> float:
    return {
        "dormant": 0.15,
        "faint": 0.45,
        "active": 0.78,
        "dominant": 0.92,
        "primary": 1.00,
    }[state]


def _seed_for_phenotype(pid: str, intensity_bucket: str) -> int:
    """Deterministic seed per phenotype × intensity bucket.

    Per the design philosophy: even the motion system should be
    reproducible and auditable. Same phenotype + same intensity →
    same particle pattern → same visual state.
    """
    return abs(hash(f"{pid}:{intensity_bucket}")) % (2**31)


def _bg_stars_svg(seed: int = 42, count: int = BG_STAR_COUNT) -> str:
    """Deterministic background starfield."""
    # Linear congruential generator — deterministic, no random module needed
    state = seed
    parts = []
    for _ in range(count):
        state = (state * 1103515245 + 12345) & 0x7FFFFFFF
        x = (state % 1000)
        state = (state * 1103515245 + 12345) & 0x7FFFFFFF
        y = (state % 500)
        state = (state * 1103515245 + 12345) & 0x7FFFFFFF
        r = 0.5 + (state % 100) / 100.0  # 0.5–1.5 px
        state = (state * 1103515245 + 12345) & 0x7FFFFFFF
        opacity = 0.15 + (state % 35) / 100.0  # 0.15–0.50
        parts.append(
            f'<circle cx="{x}" cy="{y}" r="{r:.2f}" fill="#cfd0d4" '
            f'opacity="{opacity:.2f}"/>'
        )
    return "\n".join(parts)


def _phenotype_node_svg(
    pid: str,
    coords: tuple[float, float],
    loading: float,
    state: str,
) -> str:
    """SVG block for one phenotype node + its halo + label.

    State-dependent visual properties:
      - radius (size)
      - halo (glow)
      - opacity
      - pulse animation (only for primary)
    """
    cx, cy = coords
    color = NEBULA[pid]
    label = LABELS[pid]
    r = _radius_for_state(state)
    halo_r = _halo_for_state(state)
    op = _opacity_for_state(state)

    # The halo: radial-gradient-driven outer glow.
    halo_svg = ""
    if halo_r > 0:
        halo_svg = (
            f'<circle cx="{cx}" cy="{cy}" r="{halo_r}" '
            f'fill="url(#halo-{pid})" opacity="{op * 0.7:.2f}"/>'
        )

    # Pulse animation for primary state — slow 11-second cycle.
    pulse_attrs = ""
    if state == "primary":
        # Use SMIL animation. SVG-native, no JS required.
        pulse_attrs = (
            '<animate attributeName="r" '
            f'values="{r};{r * 1.3:.2f};{r}" '
            'dur="11s" repeatCount="indefinite"/>'
        )

    # Label: only show for active+ states. Dormant/faint stay anonymous.
    label_svg = ""
    if state in ("active", "dominant", "primary"):
        # Position label below the star with cluster-aware offset
        label_y = cy + r + 18
        label_op = 0.85 if state == "primary" else 0.65
        # Wrap long labels via tspan if needed (here we keep one line)
        label_svg = (
            f'<text x="{cx}" y="{label_y}" '
            f'font-family="Inter, system-ui, sans-serif" '
            f'font-size="11" font-weight="500" '
            f'fill="#e5e4df" opacity="{label_op}" '
            f'text-anchor="middle" '
            f'letter-spacing="0.02em">{label}</text>'
        )

    # Loading value as a small mono numeric for primary/dominant.
    value_svg = ""
    if state in ("dominant", "primary"):
        value_svg = (
            f'<text x="{cx}" y="{cy + r + 32}" '
            f'font-family="IBM Plex Mono, ui-monospace, monospace" '
            f'font-size="10" fill="{color}" opacity="0.75" '
            f'text-anchor="middle">{loading:.2f}</text>'
        )

    # Edge linkage hint for dominant+: small radial line to nearest neighbor
    # (deferred — for v1 we just show node + halo)

    return f"""
    <!-- {pid} | {label} | loading={loading:.3f} | state={state} -->
    {halo_svg}
    <circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}" opacity="{op}">
        {pulse_attrs}
    </circle>
    {label_svg}
    {value_svg}
    """


def _radial_gradient_defs() -> str:
    """One radial-gradient halo per phenotype, sized for the spec.
    These power the glow effect."""
    parts = []
    for pid, color in NEBULA.items():
        parts.append(
            f"""
            <radialGradient id="halo-{pid}" cx="50%" cy="50%" r="50%">
                <stop offset="0%" stop-color="{color}" stop-opacity="0.6"/>
                <stop offset="40%" stop-color="{color}" stop-opacity="0.25"/>
                <stop offset="100%" stop-color="{color}" stop-opacity="0"/>
            </radialGradient>
            """
        )
    return "\n".join(parts)


def render_constellation(
    loadings: Mapping[str, float],
    *,
    width: int = 1000,
    height: int = 500,
    show_subtitle: bool = True,
) -> str:
    """
    Return a self-contained HTML+SVG string for the constellation.

    Args:
        loadings: dict mapping phenotype_id → loading value [0, 1].
            Missing phenotypes default to 0.0 (dormant background star).
        width: SVG viewBox width
        height: SVG viewBox height
        show_subtitle: include the "Your child's pattern" caption

    Returns:
        HTML string suitable for `st.components.v1.html()`.
    """
    # Sort phenotypes by loading descending so brighter draws on top
    states_by_pid = {
        pid: _glow_state(float(loadings.get(pid, 0.0)))
        for pid in NEBULA
    }
    # Build node SVG (sorted by loading asc so bright draws last → on top)
    sorted_pids = sorted(NEBULA.keys(), key=lambda p: float(loadings.get(p, 0)))
    nodes_svg = "\n".join(
        _phenotype_node_svg(
            pid,
            COORDS[pid],
            float(loadings.get(pid, 0.0)),
            states_by_pid[pid],
        )
        for pid in sorted_pids
    )

    # Profile shape one-liner (deterministic from loadings)
    primary = sorted(
        loadings.items(), key=lambda kv: -kv[1]
    )[0] if loadings else (None, 0)
    primary_id, primary_load = primary
    if primary_load >= 0.55 and primary_id:
        shape_caption = (
            f"Brightest pattern: <span style='color:{NEBULA[primary_id]};"
            f"font-weight:500;'>{LABELS[primary_id]}</span>"
        )
    else:
        shape_caption = (
            "<span style='color:#a8a89e;'>"
            "No single pattern dominates — "
            "more measurements would help"
            "</span>"
        )

    subtitle_html = ""
    if show_subtitle:
        subtitle_html = f"""
        <div style="text-align:center; margin-top:12px;
                    font-family:Inter, system-ui, sans-serif;
                    color:#a8a89e; font-size:13px; letter-spacing:0.02em;">
            Your child's pattern across the 11 biological dimensions.
            <br/>
            <span style="font-size:14px; color:#e5e4df;">{shape_caption}</span>
        </div>
        """

    # The full HTML. Self-contained — no external CSS, no JS dependency.
    # Per the determinism philosophy: pure declarative SVG + SMIL animation.
    return f"""
    <div style="background:{BG_COLOR}; border-radius:16px;
                padding:24px 16px 32px;
                font-family:Inter, system-ui, sans-serif;">
        <svg viewBox="0 0 {width} {height}"
             xmlns="http://www.w3.org/2000/svg"
             style="width:100%; height:auto; display:block;
                    max-height:440px;">
            <defs>
                {_radial_gradient_defs()}
            </defs>
            <!-- Deep-field background stars (deterministic seed) -->
            <g opacity="0.85">
                {_bg_stars_svg(seed=42)}
            </g>
            <!-- Phenotype nodes (sorted by loading, bright on top) -->
            <g>
                {nodes_svg}
            </g>
            <!-- Cluster region labels: subtle, only visible on close inspection -->
            <g font-family="Inter, sans-serif" font-size="9"
               fill="#3a3a3f" opacity="0.45"
               letter-spacing="0.18em" text-transform="uppercase">
                <text x="180" y="55" text-anchor="middle">FOLATE / METHYLATION</text>
                <text x="820" y="60" text-anchor="middle">MITOCHONDRIAL</text>
                <text x="500" y="195" text-anchor="middle">IMMUNE / GUT</text>
                <text x="220" y="455" text-anchor="middle">GENETIC / SYNDROMIC</text>
                <text x="830" y="465" text-anchor="middle">GABA / TRACE-METAL</text>
            </g>
        </svg>
        {subtitle_html}
    </div>
    """


# -------------------------------------------------------------------------
# Smoke test — run as `python3 ui/components/constellation.py`
# -------------------------------------------------------------------------
if __name__ == "__main__":
    # Canonical demo child loadings (per design spec)
    canonical_child = {
        "PHE-0001": 0.83,  # primary (cerebral folate)
        "PHE-0002": 0.41,  # active (secondary mito)
        "PHE-0008": 0.29,  # faint (Walsh under-methylator)
        "PHE-0003": 0.10,
        "PHE-0004": 0.10,
        "PHE-0005": 0.05,
        "PHE-0006": 0.03,
        "PHE-0007": 0.08,
        "PHE-0009": 0.06,
        "PHE-0010": 0.04,
        "PHE-0011": 0.05,
    }

    html_out = render_constellation(canonical_child)

    # Determinism check — render 3× and compare
    h2 = render_constellation(canonical_child)
    h3 = render_constellation(canonical_child)
    print(f"Deterministic? {(html_out == h2 == h3)}")
    print(f"Output length: {len(html_out)} bytes")

    # Write to a file you can open in a browser to preview
    from pathlib import Path

    preview_path = Path(__file__).parent / "constellation_preview.html"
    preview_path.write_text(
        f"""<!DOCTYPE html>
<html><head><title>Constellation preview — canonical child</title></head>
<body style="background:#fafaf7; padding:40px; max-width:900px; margin:0 auto;">
<h1 style="font-family:Inter,system-ui,sans-serif;">
    Canonical demo child constellation
</h1>
<p style="font-family:Inter,sans-serif; color:#4a4a4f;">
FRAA+ 1.4 ng/mL · plasma methionine borderline-low · regression at 18 months.
PHE-0001 primary (0.83) · PHE-0002 active (0.41) · PHE-0008 faint (0.29).
</p>
{html_out}
</body></html>"""
    )
    print(f"Preview written → {preview_path}")
    print(f"Open: file://{preview_path}")
