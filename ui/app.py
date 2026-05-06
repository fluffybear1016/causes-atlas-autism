"""
ui/app.py — Causes Atlas (autism) — v0.4 (Jobs/Ive radical simplification)

Design directive: digestible and succinct. Default state minimal. Deep state
on demand. One thing on screen at a time. Plain English first; the technical
substrate is one click away, not in your face.
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import streamlit as st

# ---------------------------------------------------------------------------
# Path resolution
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from personalized_risk import (  # noqa: E402
    ATLAS_VERSION,
    CALIBRATION_ANCHOR_CURRENT_CSRS,
    CALIBRATION_ANCHOR_NAME,
    ENGINE_VERSION,
    compute_personalized_risk,
    load_atlas,
)

CALIBRATION_DIR = REPO_ROOT / "validation" / "calibration_cases"
ATLAS_CSV_DIR = REPO_ROOT / "v2.0_scored"


# ---------------------------------------------------------------------------
# Page config — narrow centered column, sidebar collapsed
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Causes Atlas — Autism",
    page_icon="◉",  # subtle constellation-suggestive favicon glyph
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ---------------------------------------------------------------------------
# Typography + palette (Jobs/Ive vibration)
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* Stone palette */
    :root {
        --bg: #FAFAF7;
        --ink: #1F1A14;
        --ink-soft: #5C5446;
        --ink-mute: #7A6F5C;
        --line: #E7E2D9;
        --line-soft: #F1ECE3;
        --accent: #1F1A14;
    }
    html, body, [class*="css"] {
        background: var(--bg) !important;
        color: var(--ink) !important;
        font-family: ui-sans-serif, -apple-system, "SF Pro Text", system-ui, sans-serif !important;
    }
    .stApp { background: var(--bg) !important; }
    .stApp [data-testid="stHeader"] { background: transparent !important; }

    /* Hide the default Streamlit chrome */
    #MainMenu, footer, header [data-testid="stStatusWidget"] { visibility: hidden; }

    /* Serif headlines — bigger, more confident */
    h1, h2, h3 {
        font-family: ui-serif, Georgia, "Times New Roman", serif !important;
        font-weight: 500 !important;
        letter-spacing: -0.02em !important;
        color: var(--ink) !important;
    }
    h1 {
        font-size: clamp(2.8rem, 5.8vw, 4.6rem) !important;
        line-height: 1.05 !important;
    }
    h2 {
        font-size: clamp(1.8rem, 3.2vw, 2.6rem) !important;
        line-height: 1.2 !important;
    }
    h3 { font-size: 1.2rem !important; line-height: 1.4 !important; }

    /* Widen the centered content column on desktop — Streamlit's default
       caps too tight for marketing-grade layout. Still reads on mobile. */
    .stApp .main .block-container {
        max-width: 920px !important;
        padding-top: 3rem !important;
        padding-bottom: 4rem !important;
    }
    @media (max-width: 900px) {
        .stApp .main .block-container {
            max-width: 100% !important;
            padding-left: 1.25rem !important;
            padding-right: 1.25rem !important;
        }
    }

    /* Body */
    p, li, .stMarkdown p, .stMarkdown li {
        color: var(--ink-soft) !important;
        font-size: 1.02rem !important;
        line-height: 1.65 !important;
    }
    .stMarkdown em, em { color: var(--ink-mute); }
    .stMarkdown strong, strong { color: var(--ink); }

    /* Buttons — Jobs/Ive pill */
    .stButton > button {
        background: var(--ink) !important;
        color: var(--bg) !important;
        border: 1px solid var(--ink) !important;
        border-radius: 999px !important;
        padding: 0.7rem 2rem !important;
        font-size: 0.85rem !important;
        letter-spacing: 0.15em !important;
        text-transform: uppercase !important;
        font-weight: 500 !important;
    }
    .stButton > button:hover {
        background: #2d251c !important;
        border-color: #2d251c !important;
    }
    .stButton > button[kind="secondary"] {
        background: transparent !important;
        color: var(--ink) !important;
        border: 1px solid var(--line) !important;
    }
    .stButton > button[kind="secondary"]:hover {
        border-color: var(--ink) !important;
    }

    /* Eyebrow text helper class */
    .eyebrow {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.3em;
        color: var(--ink-mute);
        margin-bottom: 1.5rem;
    }

    /* Quiet caption */
    .stCaption, [data-testid="stCaptionContainer"] {
        color: var(--ink-mute) !important;
    }

    /* Expander chrome — minimal */
    .streamlit-expanderHeader {
        background: transparent !important;
        border-bottom: 1px solid var(--line) !important;
        color: var(--ink) !important;
        font-weight: 500 !important;
    }
    [data-testid="stExpander"] {
        border: none !important;
    }
    [data-testid="stExpander"] details summary {
        color: var(--ink-mute) !important;
        font-size: 0.9rem !important;
    }

    /* Selectbox + radio, quieter */
    [data-baseweb="select"] > div {
        border-radius: 999px !important;
        border: 1px solid var(--line) !important;
        background: white !important;
    }

    /* Loading bar — replaces the ASCII chart */
    .lvbar {
        height: 6px; border-radius: 3px;
        background: var(--line-soft); position: relative;
        margin: 0.4rem 0;
    }
    .lvbar > .fill {
        position: absolute; top: 0; bottom: 0; left: 0;
        background: var(--ink); border-radius: 3px;
    }
    .lvrow {
        display: grid; grid-template-columns: 1.6rem 1fr 3.2rem;
        gap: 0.5rem; align-items: center; padding: 0.35rem 0;
        border-bottom: 1px solid var(--line-soft);
    }
    .lvrow .dot { width: 0.6rem; height: 0.6rem; border-radius: 50%; }
    .lvrow .dot.dom { background: var(--ink); box-shadow: 0 0 0 4px rgba(31,26,20,0.08); }
    .lvrow .dot.sec { background: var(--ink-mute); }
    .lvrow .dot.dor { background: var(--line); }
    .lvrow .name { font-size: 0.96rem; color: var(--ink); }
    .lvrow .name .sub { color: var(--ink-mute); font-style: italic; font-size: 0.85rem; margin-left: 0.5rem; }
    .lvrow .val { font-variant-numeric: tabular-nums; font-size: 0.9rem; color: var(--ink); text-align: right; }

    /* Verified badge */
    .verified-pill {
        display: inline-block; font-size: 0.72rem; letter-spacing: 0.18em;
        text-transform: uppercase; color: var(--ink-mute);
        border: 1px solid var(--line); border-radius: 999px;
        padding: 0.3rem 0.85rem; margin-right: 0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Phenotype display metadata (plain-English names for the eleven dimensions)
# ---------------------------------------------------------------------------
PHENOTYPE_DISPLAY = {
    "PHE-0001": ("Cerebral folate", "FRAA-mediated"),
    "PHE-0002": ("Mitochondrial", "energy metabolism"),
    "PHE-0003": ("Regressive", "immune-inflammatory"),
    "PHE-0004": ("GI / microbiome", "gut-brain axis"),
    "PHE-0005": ("mTOR", "syndromic / TSC, PTEN"),
    "PHE-0006": ("Fragile X", "FMR1 silencing"),
    "PHE-0007": ("GABA / Cl⁻", "E/I imbalance"),
    "PHE-0008": ("Undermethylator", "low SAM:SAH"),
    "PHE-0009": ("Overmethylator", "folate caution"),
    "PHE-0010": ("Pyroluria", "B6 + zinc deficiency"),
    "PHE-0011": ("Cu : Zn imbalance", "metallothionein"),
}

# Per-phenotype evidence tier (Fix 2 of post-ChatGPT-critique sweep).
# Tier 1 = validated biology, Tier 2 = emerging evidence, Tier 3 =
# functional-medicine biotype with limited population-level validation.
# The engine internally tags Walsh phenotypes (PHE-0008..0011) as
# `framework_derived_LOW` already; this surface makes the tier visible
# in the UI and the constellation visualization.
PHENOTYPE_TIER = {
    "PHE-0001": 2,  # cerebral folate — emerging (FRAA biomarker validated; trial RCTs limited)
    "PHE-0002": 1,  # mitochondrial — validated biology (decades of OXPHOS literature)
    "PHE-0003": 2,  # regressive immune-inflammatory — emerging (Frye/Rossignol)
    "PHE-0004": 2,  # GI/microbiome — emerging (Hsiao, Krajmalnik-Brown)
    "PHE-0005": 1,  # mTOR syndromic (TSC1/2, PTEN) — validated, monogenic
    "PHE-0006": 1,  # Fragile X (FMR1) — validated, monogenic
    "PHE-0007": 2,  # GABA/Cl⁻ (Lemonnier, Ben-Ari) — emerging
    "PHE-0008": 3,  # Walsh undermethylator — FM biotype, limited validation
    "PHE-0009": 3,  # Walsh overmethylator — FM biotype, limited validation
    "PHE-0010": 3,  # pyroluria — FM biotype, kryptopyrrole biomarker reproducibility weak
    "PHE-0011": 3,  # Cu:Zn — FM biotype, limited validation
}

TIER_LABEL = {
    1: "Validated biology",
    2: "Emerging evidence",
    3: "Functional-medicine biotype (limited validation)",
}

TIER_SHORT = {1: "Tier 1", 2: "Tier 2", 3: "Tier 3"}

# Plain-language case names for the four bundled profiles
SAMPLE_PROFILES = [
    {
        "id": "case_015_frye_fraa_responder",
        "title": "The cerebral-folate child",
        "subtitle": "FRAA-positive · responds to leucovorin",
        "summary": (
            "Profile based on the responder subgroup from Frye 2018. "
            "Folate-receptor autoantibodies block normal folate transport "
            "into the brain. Leucovorin bypasses the block."
        ),
    },
    {
        "id": "case_011_hannah_poling",
        "title": "The mitochondrial child",
        "subtitle": "mtDNA-vulnerable · the federally-adjudicated 2008 case",
        "summary": (
            "Underlying mitochondrial dysfunction unmasked by an immune "
            "challenge. Energy-metabolism support comes first; trigger "
            "avoidance comes second."
        ),
    },
    {
        "id": "case_020_walsh_undermethylator",
        "title": "The methylation child",
        "subtitle": "Walsh framework · undermethylator biotype",
        "summary": (
            "Low-SAM/SAH methylation pattern. The atlas does not yet have "
            "strong biomarker drivers for this dimension — engine returns "
            "an honest 'undifferentiated' result with current input."
        ),
    },
    {
        "id": "case_026_22q11_deletion",
        "title": "The syndromic child",
        "subtitle": "22q11.2 deletion · DiGeorge / VCFS",
        "summary": (
            "Detected genetic syndrome. The atlas routes to syndrome-"
            "specific care (cardiology, immunology, psychiatric "
            "surveillance) rather than running the generic recommendation "
            "engine."
        ),
    },
]


# ---------------------------------------------------------------------------
# Cached loaders
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def cached_load_atlas() -> dict:
    return load_atlas()


@st.cache_data(show_spinner=False)
def load_input(case_id: str) -> dict | None:
    p = CALIBRATION_DIR / case_id / "input.json"
    if not p.exists():
        return None
    with open(p) as f:
        return json.load(f)


@st.cache_data(show_spinner=False)
def load_freshness() -> dict | None:
    p = REPO_ROOT / "freshness" / "freshness.json"
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text())
    except Exception:
        return None


# ---------------------------------------------------------------------------
# PMID → study-design lookup (Fix 5 of post-ChatGPT-critique sweep).
# Used in the contested-entities tab so each cited PMID carries its evidence
# tier — defangs ChatGPT's "epistemically flattening" critique. Equal
# *visibility* of both contested positions; *unequal weight* per citation.
# ---------------------------------------------------------------------------

# Per CLAUDE.md epistemic principles §2: source-quality hierarchy.
# Maps study_design → numeric tier (1 = highest, 5 = bottom).
PMID_DESIGN_TIER = {
    "meta_analysis": 1,
    "rct": 1,
    "natural_experiment": 1,
    "cohort": 2,
    "case_control": 2,
    "court_ruling": 2,
    "review": 3,
    "case_series": 3,
    "mechanistic": 3,
    "hypothesis_paper": 3,
    "preliminary_analysis": 4,
    "internal_correspondence": 4,
    "advisory_review": 4,
    "editorial": 5,
    "letter": 5,
    "comment": 5,
    "news": 5,
    "factcheck_review": 5,
    "advocacy": 5,
    "preprint": 4,
    "in_vitro": 4,
    "other": 4,
}

PMID_TIER_LABEL = {
    1: "tier 1 (RCT / meta-analysis / natural experiment)",
    2: "tier 2 (cohort / case-control / federal court ruling)",
    3: "tier 3 (review / case series / mechanistic)",
    4: "tier 4 (preliminary / advisory / preprint)",
    5: "tier 5 (editorial / letter / comment / news)",
}

PMID_TIER_COLOR = {
    1: "#1F1A14",  # near-black — strongest
    2: "#3F3628",  # dark stone
    3: "#5C5446",  # mid stone
    4: "#7A6F5C",  # light stone
    5: "#A89F8E",  # palest — weakest
}


@st.cache_data(show_spinner=False)
def pmid_metadata_lookup() -> dict[str, dict]:
    """Build {pmid → {design, tier, journal, year, first_author}} from sources.csv.

    Used to render evidence-tier metadata next to each PMID in the
    contested-entities UI. Cached for the session.
    """
    out: dict[str, dict] = {}
    src_path = ATLAS_CSV_DIR / "sources.csv"
    if not src_path.exists():
        return out
    with open(src_path, encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            if (r.get("platform") or "").lower() != "pubmed":
                continue
            pmid = (r.get("external_id") or "").strip()
            if not pmid.isdigit():
                continue
            design_raw = (r.get("study_design") or "").strip().lower()
            tier = PMID_DESIGN_TIER.get(design_raw, None)
            out[pmid] = {
                "design": design_raw,
                "tier": tier,
                "title": (r.get("title") or "").strip(),
                "date_published": (r.get("date_published") or "").strip(),
                "sample_size": (r.get("sample_size") or "").strip(),
            }
    return out


def render_pmid_with_tier(pmid: str) -> str:
    """Return HTML markup for a PMID link annotated with evidence tier."""
    pmid = pmid.strip()
    if not pmid.isdigit():
        return ""
    lookup = pmid_metadata_lookup()
    meta = lookup.get(pmid)
    base = f'<a href="https://pubmed.ncbi.nlm.nih.gov/{pmid}/" target="_blank" rel="noopener" style="color:var(--ink); text-decoration:none; border-bottom:1px solid var(--line);">PMID {pmid}</a>'
    if not meta:
        return f"<li style='margin:0.4rem 0; font-size:0.92rem;'>{base} <span style='color:var(--ink-mute); font-size:0.78rem;'>· (not in atlas sources)</span></li>"
    tier = meta.get("tier")
    design = meta.get("design") or "unknown design"
    n = meta.get("sample_size")
    n_str = f" · n={n}" if n else ""
    if tier:
        color = PMID_TIER_COLOR[tier]
        tier_pill = (
            f'<span style="font-size:0.68rem; letter-spacing:0.14em; '
            f'text-transform:uppercase; color:{color}; border:1px solid {color}; '
            f'border-radius:999px; padding:0.1rem 0.5rem; margin-left:0.6rem;" '
            f'title="{PMID_TIER_LABEL[tier]}">T{tier}</span>'
        )
    else:
        tier_pill = ""
    return (
        f"<li style='margin:0.45rem 0; font-size:0.92rem; line-height:1.45;'>"
        f"{base} {tier_pill}"
        f"<span style='color:var(--ink-mute); font-size:0.78rem; margin-left:0.5rem;'>"
        f"{design.replace('_',' ')}{n_str}"
        f"</span>"
        f"</li>"
    )


# ---------------------------------------------------------------------------
# State machine
# ---------------------------------------------------------------------------
if "step" not in st.session_state:
    st.session_state.step = "hero"
if "selected_case" not in st.session_state:
    st.session_state.selected_case = None
if "last_output" not in st.session_state:
    st.session_state.last_output = None


def go_to(step: str):
    st.session_state.step = step
    st.rerun()


# ---------------------------------------------------------------------------
# Step 0 — HERO
# ---------------------------------------------------------------------------
def _hero_constellation_svg() -> str:
    """Decorative constellation for the hero — quiet supporting role, not
    competing with the type. 11 nodes, AUTISM at center, low opacity so the
    title carries the visual hierarchy."""
    POSITIONS = [
        (600, 90), (870, 175), (980, 380), (940, 600), (770, 740),
        (530, 790), (290, 740), (130, 600), (90, 380), (200, 175), (470, 90)
    ]
    cx, cy = 535, 420
    parts = ['<svg viewBox="0 0 1070 880" xmlns="http://www.w3.org/2000/svg" style="width:100%; max-width:380px; height:auto; display:block; margin:0 auto; opacity:0.5;">']
    # ring connections
    for i, (x, y) in enumerate(POSITIONS):
        x2, y2 = POSITIONS[(i + 1) % len(POSITIONS)]
        parts.append(f'<line x1="{x}" y1="{y}" x2="{x2}" y2="{y2}" stroke="#E7E2D9" stroke-width="1"/>')
    # spokes
    for x, y in POSITIONS:
        parts.append(f'<line x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" stroke="#F1ECE3" stroke-width="1"/>')
    # nodes
    for x, y in POSITIONS:
        parts.append(f'<circle cx="{x}" cy="{y}" r="6" fill="#1F1A14" fill-opacity="0.85"/>')
    # center
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="4" fill="#A89F8E"/>')
    parts.append(f'<text x="{cx}" y="{cy+34}" text-anchor="middle" font-size="14" fill="#5C5446" letter-spacing="3" font-family="ui-serif, Georgia, serif">AUTISM</text>')
    parts.append("</svg>")
    return "".join(parts)


def render_hero():
    st.markdown("<div style='height:2vh'></div>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style='text-align:center;'>
            <div class='eyebrow'>The Causes Atlas · Autism</div>
            <h1 style='margin-top:1.2rem;'>
                Treat the child,<br>
                <em style='color: var(--ink-mute);'>not the diagnosis.</em>
            </h1>
            <p style='margin-top:2.4rem; font-size: clamp(1.05rem, 1.4vw, 1.25rem); color: var(--ink-soft); max-width:46ch; margin-left:auto; margin-right:auto; line-height:1.6;'>
                An open, deterministic, evidence-weighted knowledge graph
                that maps your child's biology to literature-linked
                interventions — with the uncertainty made visible.
            </p>
        </div>
        <div style='height:2vh'></div>
        {_hero_constellation_svg()}
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div style='height:3vh'></div>", unsafe_allow_html=True)
    c = st.columns([1, 1.4, 1])
    with c[1]:
        if st.button("Map a profile", use_container_width=True):
            go_to("pick")
    st.markdown("<div style='height:5vh'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style='text-align:center; color: var(--ink-mute); font-size:0.74rem; letter-spacing:0.22em; text-transform:uppercase;'>
            Open · deterministic · evidence-weighted · continuously ingested
        </div>
        <div style='text-align:center; color: var(--ink-mute); font-size:0.78rem; margin-top:1rem; max-width:54ch; margin-left:auto; margin-right:auto; font-style:italic;'>
            Research prototype. Decision support, not a diagnostic device.
            The atlas surfaces what the literature links to a child's profile;
            it does not predict treatment response or recommend interventions.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Step 1 — PICK A PROFILE
# ---------------------------------------------------------------------------
def render_pick():
    st.markdown(
        """
        <div style='text-align:center;'>
            <div class='eyebrow'>Pick one</div>
            <h2>Four children. Four different shapes.</h2>
            <p style='max-width:48ch; margin: 1rem auto 0; color: var(--ink-soft);'>
                Each profile below comes from real published literature. Pick one
                to see how the atlas reads it. Your own data isn't required to start.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div style='height:3vh'></div>", unsafe_allow_html=True)

    for prof in SAMPLE_PROFILES:
        with st.container():
            st.markdown(
                f"""
                <div style='border: 1px solid var(--line); border-radius: 14px; padding: 1.5rem 1.75rem; margin-bottom: 1rem; background: white;'>
                    <div style='font-family: ui-serif, Georgia, serif; font-size: 1.3rem; color: var(--ink); margin-bottom: 0.25rem;'>
                        {prof['title']}
                    </div>
                    <div style='font-size: 0.82rem; letter-spacing: 0.12em; text-transform: uppercase; color: var(--ink-mute); margin-bottom: 0.85rem;'>
                        {prof['subtitle']}
                    </div>
                    <div style='font-size: 0.96rem; line-height: 1.55; color: var(--ink-soft);'>
                        {prof['summary']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            cols = st.columns([4, 2])
            with cols[1]:
                if st.button(f"See profile", key=f"pick_{prof['id']}", use_container_width=True):
                    inp = load_input(prof["id"])
                    if inp is None:
                        st.error("Profile data not found.")
                    else:
                        with st.spinner("Reading the atlas..."):
                            st.session_state.last_output = compute_personalized_risk(inp)
                        st.session_state.selected_case = prof
                        go_to("result")

    st.markdown("<div style='height:3vh'></div>", unsafe_allow_html=True)
    cc = st.columns([1, 2, 1])
    with cc[1]:
        if st.button("← back", key="back_pick", type="secondary", use_container_width=True):
            go_to("hero")


# ---------------------------------------------------------------------------
# Step 2 — RESULT
# ---------------------------------------------------------------------------
def render_constellation_svg(loadings: dict[str, float], dominant: list[str]) -> str:
    """11-node constellation SVG with this child's loadings as halo intensity.

    Fix 2: nodes are now visually tier-differentiated:
      - Tier 1 (validated biology):     solid filled circle
      - Tier 2 (emerging evidence):     filled circle + thin solid ring
      - Tier 3 (FM biotype, limited):   filled circle + dashed ring + tier badge
    Halo intensity still indicates this child's loading on the dimension.
    """
    POSITIONS = {
        "PHE-0001": (600, 90), "PHE-0002": (870, 175), "PHE-0003": (980, 380),
        "PHE-0004": (940, 600), "PHE-0005": (770, 740), "PHE-0006": (530, 790),
        "PHE-0007": (290, 740), "PHE-0008": (130, 600), "PHE-0009": (90, 380),
        "PHE-0010": (200, 175), "PHE-0011": (470, 90),
    }
    cx, cy = 535, 420
    svg = ['<svg viewBox="0 0 1070 880" xmlns="http://www.w3.org/2000/svg" style="width:100%; height:auto; max-width:720px; display:block; margin:0 auto;" font-family="ui-serif, Georgia, serif">']
    # radial guides
    for pid, (x, y) in POSITIONS.items():
        svg.append(f'<line x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" stroke="#F1ECE3" stroke-width="1"/>')
    # center
    svg.append(f'<circle cx="{cx}" cy="{cy}" r="3" fill="#A89F8E"/>')
    svg.append(f'<text x="{cx}" y="{cy+36}" text-anchor="middle" font-size="14" fill="#5C5446" letter-spacing="3">AUTISM</text>')
    # nodes with halos sized by loading + tier-differentiated rings
    for pid, (x, y) in POSITIONS.items():
        load = float(loadings.get(pid, 0.5))
        is_dom = pid in dominant
        tier = PHENOTYPE_TIER.get(pid, 2)
        # halo radius scales with loading above 0.5
        halo_r = max(8, int(8 + (load - 0.5) * 60)) if load > 0.5 else 8
        halo_op = max(0.05, min(0.45, (load - 0.5) * 1.8)) if load > 0.5 else 0.05
        if is_dom:
            svg.append(f'<circle cx="{x}" cy="{y}" r="{halo_r+10}" fill="#1F1A14" fill-opacity="{halo_op}"/>')
            svg.append(f'<circle cx="{x}" cy="{y}" r="{halo_r}" fill="#1F1A14" fill-opacity="0.18"/>')
        node_fill = "#1F1A14" if is_dom else "#7A6F5C" if load >= 0.45 else "#C8C0AF"
        node_r = 7 if is_dom else 5
        svg.append(f'<circle cx="{x}" cy="{y}" r="{node_r}" fill="{node_fill}"/>')
        # Tier ring overlay
        if tier == 2:
            # Solid thin ring for emerging evidence
            svg.append(f'<circle cx="{x}" cy="{y}" r="{node_r+5}" fill="none" stroke="#1F1A14" stroke-width="1" stroke-opacity="0.45"/>')
        elif tier == 3:
            # Dashed ring + small "FM" badge for FM biotype
            svg.append(f'<circle cx="{x}" cy="{y}" r="{node_r+5}" fill="none" stroke="#7A6F5C" stroke-width="1" stroke-dasharray="3,3" stroke-opacity="0.7"/>')
        # labels
        name, sub = PHENOTYPE_DISPLAY.get(pid, (pid, ""))
        label_above = y < cy - 50
        label_right = x > cx + 30
        label_left = x < cx - 30
        if label_above:
            tx, ty, anchor = x, y - 28, "middle"
            ty2 = ty + 18
            ty3 = ty - 18  # tier badge above name
        elif label_right:
            tx, ty, anchor = x + 18, y + 5, "start"
            ty2 = ty + 16
            ty3 = ty - 14
        elif label_left:
            tx, ty, anchor = x - 18, y + 5, "end"
            ty2 = ty + 16
            ty3 = ty - 14
        else:
            tx, ty, anchor = x, y + 36, "middle"
            ty2 = ty + 16
            ty3 = ty - 18
        weight = "600" if is_dom else "500"
        opacity = 1.0 if is_dom else 0.85 if load >= 0.45 else 0.5
        # FM-biotype tier-3 badge above the name
        if tier == 3:
            svg.append(f'<text x="{tx}" y="{ty3}" text-anchor="{anchor}" font-size="9" fill="#7A6F5C" letter-spacing="2" font-family="ui-sans-serif, sans-serif" opacity="{opacity}">FM BIOTYPE</text>')
        svg.append(f'<text x="{tx}" y="{ty}" text-anchor="{anchor}" font-size="17" fill="#1F1A14" font-weight="{weight}" opacity="{opacity}">{name}</text>')
        svg.append(f'<text x="{tx}" y="{ty2}" text-anchor="{anchor}" font-size="12" fill="#7A6F5C" font-style="italic" opacity="{opacity}">{sub}</text>')

    # Tier legend (bottom-right corner)
    svg.append('<g transform="translate(820,830)" font-family="ui-sans-serif, sans-serif">')
    svg.append('<text x="0" y="0" font-size="9" fill="#7A6F5C" letter-spacing="2">EVIDENCE TIER</text>')
    svg.append('<circle cx="8" cy="14" r="5" fill="#1F1A14"/>')
    svg.append('<text x="20" y="17" font-size="10" fill="#5C5446">Tier 1 — validated biology</text>')
    svg.append('<circle cx="8" cy="30" r="5" fill="#7A6F5C"/>')
    svg.append('<circle cx="8" cy="30" r="9" fill="none" stroke="#1F1A14" stroke-width="1" stroke-opacity="0.45"/>')
    svg.append('<text x="20" y="33" font-size="10" fill="#5C5446">Tier 2 — emerging evidence</text>')
    svg.append('<circle cx="8" cy="46" r="5" fill="#7A6F5C"/>')
    svg.append('<circle cx="8" cy="46" r="9" fill="none" stroke="#7A6F5C" stroke-width="1" stroke-dasharray="3,3" stroke-opacity="0.7"/>')
    svg.append('<text x="20" y="49" font-size="10" fill="#5C5446">Tier 3 — FM biotype (limited validation)</text>')
    svg.append('</g>')

    svg.append("</svg>")
    return "".join(svg)


def plain_english_narrative(output: dict, profile: dict) -> str:
    """Generate a single-sentence-or-two summary of the profile shape."""
    if output.get("syndromic_flag"):
        sm = output.get("syndromic_match", {}) or {}
        return (
            f"The atlas detected a known genetic-syndrome pattern — "
            f"**{sm.get('syndrome_name','?')}**. Most decisions for this "
            f"child should follow the syndrome-specific care pathway "
            f"(cardiology, immunology, surveillance). The generic "
            f"profile below is shown for transparency only."
        )
    ps = output.get("profile_summary", {}) or {}
    if ps.get("undifferentiated_flag"):
        return (
            "This profile doesn't have a clear shape yet — no single "
            "biological pattern dominates given the available input. "
            "The atlas's honest answer: **measure more before deciding**. "
            "Look at the deeper view below to see which dimensions are "
            "closest to the threshold."
        )
    dom = ps.get("dominant_dimensions", []) or []
    if len(dom) == 1:
        name = PHENOTYPE_DISPLAY.get(dom[0], (dom[0], ""))[0]
        return (
            f"This child's biology points clearly toward **{name.lower()} "
            f"dysfunction**. The literature linked to this pattern points "
            f"first to a small set of targeted interventions, listed below."
        )
    if len(dom) >= 2:
        names = [PHENOTYPE_DISPLAY.get(d, (d, ""))[0].lower() for d in dom]
        joined = ", ".join(names[:-1]) + " and " + names[-1] if len(names) > 1 else names[0]
        return (
            f"This child shows **multiple overlapping patterns**: "
            f"{joined}. Strategy: target the strongest one first, "
            f"then layer the others as biomarkers respond."
        )
    return ""


def render_result():
    out = st.session_state.last_output
    profile = st.session_state.selected_case
    if not out or not profile:
        go_to("hero")
        return

    st.markdown(
        f"""
        <div style='text-align:center;'>
            <div class='eyebrow'>{profile['subtitle']}</div>
            <h1>{profile['title']}</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Plain-English narrative
    st.markdown("<div style='height:2vh'></div>", unsafe_allow_html=True)
    narrative = plain_english_narrative(out, profile)
    if narrative:
        st.markdown(
            f"<div style='font-size:1.15rem; line-height:1.65; color: var(--ink); max-width:48ch; margin: 0 auto; text-align:center;'>{narrative}</div>",
            unsafe_allow_html=True,
        )

    # Constellation
    st.markdown("<div style='height:4vh'></div>", unsafe_allow_html=True)
    pl = out.get("profile_loadings", {}) or {}
    ps = out.get("profile_summary", {}) or {}
    dominant = ps.get("dominant_dimensions", []) or []
    st.markdown(render_constellation_svg(pl, dominant), unsafe_allow_html=True)
    st.markdown(
        "<div style='text-align:center; color:var(--ink-mute); font-size:0.85rem; margin-top:1rem;'>"
        "Each node is a biological pattern. The brighter the node, the more this child's profile loads into it."
        "</div>",
        unsafe_allow_html=True,
    )

    # Interventions the atlas links to this profile (citation-surfacing,
    # not recommendation. Fix 3 of post-ChatGPT-critique sweep: dropped
    # "First-line / Also consider" verbs to stay clearly out of FDA SaMD
    # territory. The atlas surfaces what the published literature links to
    # this profile shape; it does not recommend any intervention.)
    bundle = out.get("intervention_bundle", []) or []
    if bundle and not out.get("syndromic_flag"):
        st.markdown("<div style='height:5vh'></div>", unsafe_allow_html=True)
        st.markdown(
            "<div style='text-align:center;'><div class='eyebrow'>"
            "What the literature links to this profile</div></div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<div style='text-align:center; color:var(--ink-mute); font-size:0.88rem; max-width:48ch; margin:0.5rem auto 1.5rem; line-height:1.55;'>"
            "<em>The atlas surfaces interventions linked in the published literature "
            "to this profile's strongest dimensions. It does not recommend treatment. "
            "Decisions are for clinicians.</em>"
            "</div>",
            unsafe_allow_html=True,
        )
        for i, item in enumerate(bundle[:3]):
            primary_dim = item.get("primary_target_dimension")
            primary_name = PHENOTYPE_DISPLAY.get(primary_dim, (primary_dim or "?", ""))[0]
            target_dims = item.get("target_dimensions") or []
            n_links = max(1, len(target_dims))
            score = float(item.get("score", 0.0) or 0.0)
            atlas_q = float(item.get("atlas_quality", 0.0) or 0.0) * 100.0
            st.markdown(
                f"""
                <div style='border-bottom: 1px solid var(--line); padding: 1.1rem 0;'>
                    <div style='display:flex; justify-content:space-between; align-items:baseline; gap:1rem;'>
                        <div>
                            <div style='font-family: ui-serif, Georgia, serif; font-size: 1.2rem; color: var(--ink);'>
                                {item.get('name','?')}
                            </div>
                            <div style='font-size: 0.88rem; color: var(--ink-mute); margin-top: 0.2rem;'>
                                Linked to <strong style='color:var(--ink-soft);'>{primary_name.lower()}</strong>
                                via {n_links} atlas edge{'s' if n_links != 1 else ''}
                                · atlas signal {atlas_q:.0f}/100
                            </div>
                        </div>
                        <div style='font-size: 0.7rem; letter-spacing: 0.16em; text-transform: uppercase; color: var(--ink-mute); white-space: nowrap; text-align: right;'>
                            profile-fit {score:.2f}
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Action buttons
    st.markdown("<div style='height:5vh'></div>", unsafe_allow_html=True)
    cc = st.columns([1, 1, 1])
    with cc[0]:
        if st.button("Try another", type="secondary", use_container_width=True):
            go_to("pick")
    with cc[2]:
        if st.button("Start over", type="secondary", use_container_width=True):
            go_to("hero")

    # Deep view — single expander, optional
    st.markdown("<div style='height:4vh'></div>", unsafe_allow_html=True)
    with st.expander("Show the technical view", expanded=False):
        st.markdown(
            "**Profile loadings — all eleven dimensions** "
            "<span style='font-size:0.8rem; color:var(--ink-mute); font-weight:normal;'>"
            "(tier badge indicates per-dimension evidence strength)</span>",
            unsafe_allow_html=True,
        )
        for pid in sorted(pl.keys()):
            load = float(pl[pid])
            name, sub = PHENOTYPE_DISPLAY.get(pid, (pid, ""))
            tier = PHENOTYPE_TIER.get(pid, 2)
            cls = "dom" if load >= 0.55 else "sec" if load >= 0.45 else "dor"
            pct = max(0, min(100, load * 100))
            tier_color = {1: "#1F1A14", 2: "#5C5446", 3: "#A89F8E"}[tier]
            tier_label = TIER_SHORT[tier]
            tier_full = TIER_LABEL[tier]
            st.markdown(
                f"""
                <div class='lvrow'>
                    <div class='dot {cls}'></div>
                    <div>
                        <div class='name'>{name}<span class='sub'>{sub}</span>
                            <span style='font-size:0.7rem; letter-spacing:0.12em; text-transform:uppercase; color:{tier_color}; border:1px solid {tier_color}; border-radius:999px; padding:0.1rem 0.5rem; margin-left:0.6rem;' title='{tier_full}'>{tier_label}</span>
                        </div>
                        <div class='lvbar'><div class='fill' style='width:{pct:.1f}%'></div></div>
                    </div>
                    <div class='val'>{load:.2f}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("---")
        st.markdown("**Profile shape**")
        flags = []
        if ps.get("multi_pattern_flag"):
            flags.append("multi-pattern")
        if ps.get("undifferentiated_flag"):
            flags.append("undifferentiated")
        if not flags:
            flags.append("focal")
        st.markdown(
            f"- shape: `{', '.join(flags)}`  \n"
            f"- profile concentration: `{ps.get('profile_concentration', 0):.3f}`  \n"
            f"- max loading: `{ps.get('max_loading', 0):.3f}`  \n"
            f"- dominant dimensions: `{ps.get('dominant_dimensions') or '(none)'}`"
        )

        if bundle:
            st.markdown("---")
            st.markdown("**Full intervention ranking (top 5)**")
            for it in bundle:
                st.markdown(
                    f"- `{it['intervention_id']}` {it['name']} · "
                    f"score `{it.get('score', 0):.3f}` · "
                    f"primary target `{it.get('primary_target_dimension','?')}` · "
                    f"`{it.get('recommendation_type','')}`"
                )

        st.markdown("---")
        st.markdown(
            f"<div style='font-size:0.85rem; color:var(--ink-mute);'>"
            f"<span class='verified-pill'>verified</span>"
            f"inference engine `{ENGINE_VERSION}` · atlas `{ATLAS_VERSION}` · "
            f"atlas-signal anchor `{CALIBRATION_ANCHOR_NAME} = "
            f"{CALIBRATION_ANCHOR_CURRENT_CSRS}` (≥ 80 required for engine to run)"
            f"</div>"
            f"<div style='font-size:0.78rem; color:var(--ink-mute); margin-top:0.6rem; font-style:italic;'>"
            f"The atlas signal is a heuristic composite of evidence type, replication "
            f"count, and source-quality tier. Not a validated meta-analytic effect-size "
            f"estimator. Treat magnitudes as ordinal."
            f"</div>"
            f"<div style='font-size:0.78rem; color:var(--ink-mute); margin-top:0.6rem; word-break:break-all;'>"
            f"canonical_digest: <code style='font-size:0.7rem;'>{out.get('canonical_digest','')}</code>"
            f"</div>",
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------------------------
# Always-visible footer expander — Behind the scenes
# ---------------------------------------------------------------------------
def render_footer():
    st.markdown("<div style='height:8vh'></div>", unsafe_allow_html=True)
    st.markdown(
        "<div style='border-top: 1px solid var(--line); padding-top: 2rem;'></div>",
        unsafe_allow_html=True,
    )
    with st.expander("Behind the scenes — how this is built", expanded=False):
        st.markdown(
            "<div style='font-size:0.78rem; letter-spacing:0.18em; text-transform:uppercase; color: var(--ink-mute); margin-bottom:0.6rem;'>Choose a section</div>",
            unsafe_allow_html=True,
        )
        sub_tab = st.radio(
            "Section",
            ["What this is", "Eleven dimensions", "Contested entities", "Live updates", "Methodology", "Disclaimer"],
            horizontal=False,
            label_visibility="collapsed",
        )
        st.markdown("<div style='height:1rem; border-top:1px solid var(--line); margin-top:0.5rem;'></div>", unsafe_allow_html=True)

        if sub_tab == "What this is":
            st.markdown(
                """
                The Causes Atlas is the first **open, deterministic,
                evidence-weighted knowledge graph for stratifying autism-
                related biological signals and mapping them to literature-
                linked interventions with explicit uncertainty.**

                The atlas treats autism as **eleven biological pattern
                dimensions** — not a single label, and not all weighted
                equally (see the Eleven dimensions tab for the per-pattern
                evidence tier). Every child has a profile *across* those
                dimensions; no single dimension is a diagnosis.

                The engine is an **evidence-weighted inference engine**, not
                a clinical-prediction model: it surfaces what the published
                literature links to a child's profile, with each link
                carrying its underlying study design and replication count.
                It does not predict treatment response. It does not
                recommend interventions.

                **What you can verify yourself:** every PMID is PubMed-
                checked before being allowed in (verify-before-write). Every
                contested claim shows mainstream consensus and contested
                evidence side by side, with each citation carrying its own
                study design. The whole graph is open source, deterministic,
                and reproducible — same input → same SHA-256 digest, every
                time.

                **What this is not:** a diagnostic device. A regulated
                medical device. A substitute for clinical judgment. A
                validated population-level prediction tool. A protocol
                library or course.
                """
            )

        elif sub_tab == "Eleven dimensions":
            st.markdown(
                "Each dimension carries an explicit **evidence tier**. The "
                "atlas does not pretend they are on equal footing — Fragile X "
                "(monogenic, decades of biology) and pyroluria (a functional-"
                "medicine biotype with limited population validation) are "
                "different epistemic objects."
            )
            for tier in (1, 2, 3):
                pids = sorted(p for p, t in PHENOTYPE_TIER.items() if t == tier)
                tier_color = {1: "#1F1A14", 2: "#5C5446", 3: "#A89F8E"}[tier]
                st.markdown(
                    f"""
                    <div style='margin-top:1.4rem; margin-bottom:0.6rem;'>
                        <span style='font-size:0.72rem; letter-spacing:0.18em; text-transform:uppercase; color:{tier_color}; border:1px solid {tier_color}; border-radius:999px; padding:0.2rem 0.7rem;'>
                            {TIER_SHORT[tier]} — {TIER_LABEL[tier]}
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                for pid in pids:
                    name, sub = PHENOTYPE_DISPLAY[pid]
                    st.markdown(f"- **{name}** — *{sub}*")

        elif sub_tab == "Contested entities":
            st.markdown(
                "For every claim the literature is split on — vaccines, "
                "aluminum adjuvants, certain medications, prenatal exposures — "
                "the atlas records **both views with equal visibility**, but "
                "**not equal weight**. Each PMID below carries its own study-"
                "design tier; an RCT is not a letter-to-the-editor. The "
                "atlas does not pick a side; it preserves the actual shape "
                "of the evidence landscape."
            )
            atlas = cached_load_atlas()
            iep_rows = atlas.get("iatrogenic", [])
            contested = [r for r in iep_rows if (r.get("status") or "").lower() == "contested"]
            st.caption(
                f"{len(contested)} contested rows in iatrogenic exposure priors. "
                f"Tier badges per PMID: T1 (RCT/meta-analysis/natural experiment) → "
                f"T5 (editorial/letter/comment)."
            )
            for r in contested:
                agent = (r.get("specific_agent") or "").replace("_", " ").title()
                with st.expander(agent):
                    # Mainstream consensus FIRST, in equal prominence
                    consensus = (r.get("mainstream_consensus_position") or "").strip()
                    if consensus:
                        st.markdown("**Mainstream consensus position**")
                        st.markdown(f"> {consensus}")
                    else:
                        st.warning("Mainstream consensus position not yet populated.")

                    st.markdown("---")
                    st.markdown("**Citations — both positions, weighted by study design**")

                    sup_pmids = [p.strip() for p in (r.get("primary_pmids") or "").split(";") if p.strip()]
                    opp_pmids = [p.strip() for p in (r.get("countervailing_evidence_pmids") or "").split(";") if p.strip()]

                    col_s, col_o = st.columns(2)
                    with col_s:
                        st.markdown("*Primary (supporting the row's stated effect):*")
                        if sup_pmids:
                            html = "<ul style='list-style:none; padding:0; margin:0;'>"
                            for p in sup_pmids:
                                html += render_pmid_with_tier(p)
                            html += "</ul>"
                            st.markdown(html, unsafe_allow_html=True)
                        else:
                            st.caption("(none populated yet)")
                    with col_o:
                        st.markdown("*Countervailing (against the row's stated effect):*")
                        if opp_pmids:
                            html = "<ul style='list-style:none; padding:0; margin:0;'>"
                            for p in opp_pmids:
                                html += render_pmid_with_tier(p)
                            html += "</ul>"
                            st.markdown(html, unsafe_allow_html=True)
                        else:
                            st.caption("(none populated yet)")

        elif sub_tab == "Live updates":
            fresh = load_freshness()
            if not fresh:
                st.info("The continuous-ingestion log will appear here once the daily cron has run at least once.")
            else:
                c1, c2, c3 = st.columns(3)
                c1.metric("Atlas PMIDs", fresh.get("atlas_pmid_count", "—"))
                c2.metric("In curation queue", fresh.get("queue_size", "—"))
                c3.metric("Daily logs", len(fresh.get("last_30_daily_logs", [])))
                logs = fresh.get("last_30_daily_logs", []) or []
                if logs:
                    st.markdown("**Recent runs**")
                    for log in reversed(logs[-5:]):
                        st.markdown(
                            f"- `{log.get('run_at_utc','?')}` — "
                            f"verified+queued: {log.get('verified_added_to_queue',0)}"
                        )
                st.caption(
                    "Daily PubMed ingestion runs every morning. New papers "
                    "pass the verify-before-write protocol before being queued "
                    "for human curation. The fact that this log is live is the "
                    "atlas's defense against staleness."
                )

        elif sub_tab == "Methodology":
            st.markdown(
                """
                **The engine — what it actually is.** A deterministic,
                evidence-weighted inference engine over the atlas knowledge
                graph. Not a causal model (we don't run interventional
                studies). Not a prediction model (no prospective cohort
                validation). It is a structured reading of what the
                published literature links to a profile shape.

                **The pipeline.** Each child's input — biomarkers, genetics,
                exposures — maps through the atlas into a loading vector
                across eleven biological pattern dimensions, each carrying
                its own evidence tier (Tier 1 validated → Tier 3 functional-
                medicine biotype). Per-dimension log-odds shifts → sigmoid →
                probability.

                **Intervention surfacing.** For each candidate intervention
                in the atlas, score = best (loading × edge_weight) across
                this child's dimensions, weighted by the intervention's
                **atlas signal** (a heuristic composite of evidence type,
                replication count, source-quality tier — *not* a validated
                meta-analytic effect-size estimator; treat magnitudes as
                ordinal). Specificity is rewarded; broad polypills are not.
                The output is a ranked *citation surface*, not a
                recommendation.

                **Determinism.** No LLMs in the inference math. No random
                seeds. Same input → same output → same SHA-256 digest.
                Re-running this profile a hundred times produces the same
                answer a hundred times.

                **Verification.** Every PMID in the atlas is verified
                against PubMed esummary before it is allowed in. Memory-
                based citation generation is forbidden by protocol. In
                live testing, the protocol caught 9 of 23 fabricated PMIDs
                an LLM tried to insert — direct evidence the discipline
                works.

                **Δ² (research-attention velocity).** A separate engine
                tracks which entities are *accelerating* in the literature
                (recency × cross-design convergence × subset validation ×
                replication independence × trajectory mismatch). Important:
                Δ² is **research-attention velocity, not truth velocity**.
                A fast-rising entity may be correct, faddish, or funded;
                Δ² doesn't decide. Anti-reflexivity discipline halts the
                pipeline if curator behavior correlates with prior Δ²
                rankings.
                """
            )

        elif sub_tab == "Disclaimer":
            st.markdown(
                """
                **Research prototype. Not for clinical use.**

                - Not FDA-cleared. Not a medical device.
                - Not a substitute for evaluation by a qualified clinician.
                - Not validated against any prospective cohort. Calibration
                  is at the atlas level and against four literature-derived
                  cases.
                - Many priors are stub log-odds pending population calibration.
                - The atlas does not pick sides on contested topics; it
                  records both views.
                """
            )

    st.markdown(
        f"<div style='text-align:center; color: var(--ink-mute); font-size:0.7rem; letter-spacing:0.2em; text-transform:uppercase; margin-top:2rem;'>"
        f"the causes atlas · v0.4 · open source"
        f"</div>",
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Top-level dispatch
# ---------------------------------------------------------------------------
step = st.session_state.step
if step == "hero":
    render_hero()
elif step == "pick":
    render_pick()
elif step == "result":
    render_result()
else:
    render_hero()

render_footer()
