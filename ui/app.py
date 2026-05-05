"""
ui/app.py — Causes Atlas (autism) — research prototype v0.3

Public-facing UI for the Causes Atlas — a deterministic, evidence-balanced,
continuously-ingested knowledge graph of autism causation, phenotypes,
biomarkers, and interventions, with an individual-level profile-vector
computation over the underlying causal graph.

The internal framework principle (susceptibility × trigger → mechanism →
phenotype) is documented in CLAUDE.md / spec; it does not ride on the
public surface.

This UI is a thin front-end over `personalized_risk.py`. The engine is the
source of truth; the UI adds tier-aware framing, calibration-case quick-load,
and disclosure. No clinical recommendations are provided.

Run:
    pip install streamlit
    streamlit run ui/app.py
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import streamlit as st

# ---------------------------------------------------------------------------
# Path resolution — UI lives at <repo>/ui/, engine at <repo>/personalized_risk.py
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from personalized_risk import (  # noqa: E402
    ATLAS_VERSION,
    CALIBRATION_ANCHOR_CURRENT_CSRS,
    CALIBRATION_ANCHOR_NAME,
    CALIBRATION_ANCHOR_REQUIRED_CSRS,
    ENGINE_VERSION,
    compute_personalized_risk,
    load_atlas,
)

CALIBRATION_DIR = REPO_ROOT / "validation" / "calibration_cases"
ATLAS_CSV_DIR = REPO_ROOT / "v2.0_scored"


# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Causes Atlas — Autism Profile",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------------------------
# Cached loaders
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def cached_load_atlas() -> dict:
    """Load atlas CSVs once per session."""
    return load_atlas()


@st.cache_data(show_spinner=False)
def list_calibration_cases() -> list[str]:
    if not CALIBRATION_DIR.exists():
        return []
    return sorted([p.name for p in CALIBRATION_DIR.iterdir() if p.is_dir()])


@st.cache_data(show_spinner=False)
def load_calibration_input(case_name: str) -> dict | None:
    p = CALIBRATION_DIR / case_name / "input.json"
    if not p.exists():
        return None
    with open(p) as f:
        return json.load(f)


@st.cache_data(show_spinner=False)
def load_calibration_expected(case_name: str) -> str | None:
    p = CALIBRATION_DIR / case_name / "expected_output.yaml"
    if not p.exists():
        return None
    return p.read_text()


# ---------------------------------------------------------------------------
# Disclaimer text
# ---------------------------------------------------------------------------
RESEARCH_BANNER = (
    "**RESEARCH PROTOTYPE — NOT FOR CLINICAL USE.** "
    "This tool is a deterministic research demonstration of an autism causation "
    "knowledge graph. It is not FDA-cleared, not a medical device, and not a "
    "substitute for medical advice. No data you enter here is transmitted off "
    "your machine; the engine runs locally."
)

LONG_DISCLAIMER = """
### Full disclaimer

This software is a **research prototype** of the *Causes Atlas (Autism)* —
an evidence-driven, deterministic knowledge graph of autism causation,
phenotypes, biomarkers, and interventions. It computes an individual-level
profile (`P(Φ | susceptibility, trigger) ≠ P(Φ | trigger)`) as a Layer 3
personalized-risk computation over the underlying causal graph.

**What this is**
- A deterministic, auditable scoring engine. Same input always produces the
  same output, with a `canonical_digest` SHA-256 over the deterministic-output
  fields for byte-equality testing.
- A way to surface, for a hypothetical individual profile, which phenotype
  clusters the published literature (as encoded in the atlas) suggests are
  more or less likely, and which interventions the atlas links to those
  phenotypes.
- An explicit map of evidence — every prior shift is grounded in PMID-verified
  literature; the underlying CSVs are inspectable.

**What this is NOT**
- Not a diagnosis. Not a prediction of any individual outcome.
- Not a substitute for evaluation by a qualified clinician.
- Not validated against any prospective cohort. Calibration is at the
  knowledge-graph level (e.g., the leucovorin anchor) and against four
  literature-derived calibration cases.
- Not a vaccine-policy recommendation engine. The atlas records primary
  evidence at appropriate weight; recommendations require clinical context
  this tool cannot capture.

**Determinism + verification**
- No LLMs in scoring math. No random seeds.
- All PMIDs in the atlas are PubMed-verified per the BioMysteryBench-aligned
  protocol (CLAUDE.md §Verification protocol).
- Many atlas hypotheses (vaccines, aluminum adjuvants, glyphosate, etc.) are
  flagged `status: contested` and remain so regardless of effect direction.

**Known limitations of v0.1**
- Many priors are stub log-odds (e.g., FRAA +0.55, MTHFR T/T +0.30) — not yet
  population-calibrated.
- Walley IDM credal aggregation is a simplified band, not full quadrature.
- Within-phenotype responder, CDR state, functional trajectory predictor,
  and pathway burden are deferred to v0.2.
"""


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## Causes Atlas")
    st.caption("Autism Profile — research prototype")

    tier = st.radio(
        "View mode",
        options=["Researcher", "Clinician", "Family / Curious"],
        index=0,
        help=(
            "Researcher: full reasoning trace, log-odds, drivers, deferred-features list. "
            "Clinician: phenotype posteriors + intervention rationale framed for handoff. "
            "Family / Curious: simplified language, 'questions to ask your doctor' framing."
        ),
    )

    st.markdown("---")
    st.markdown("**Engine**")
    st.code(ENGINE_VERSION, language=None)
    st.markdown("**Atlas**")
    st.code(ATLAS_VERSION, language=None)
    st.markdown("**Calibration anchor**")
    st.code(
        f"{CALIBRATION_ANCHOR_NAME} = {CALIBRATION_ANCHOR_CURRENT_CSRS}\n"
        f"required ≥ {CALIBRATION_ANCHOR_REQUIRED_CSRS}",
        language=None,
    )

    st.markdown("---")
    st.caption(
        "Open source — research prototype. "
        "All computation runs locally. No telemetry."
    )


# ---------------------------------------------------------------------------
# Top banner
# ---------------------------------------------------------------------------
st.title("Causes Atlas — Autism Profile")
st.caption(
    "Individual-level profile across 11 phenotype dimensions · "
    "deterministic, evidence-balanced, continuously ingested · research prototype"
)
st.warning(RESEARCH_BANNER)


# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------
tab_welcome, tab_run, tab_atlas, tab_contested, tab_freshness, tab_method, tab_about = st.tabs(
    [
        "Welcome",
        "Run profile",
        "Atlas explorer",
        "Contested entities",
        "Freshness",
        "Methodology",
        "About / Disclaimer",
    ]
)


# ===========================================================================
# Tab 0 — Welcome (FM for the masses entry point)
# ===========================================================================
with tab_welcome:
    st.markdown(
        """
### Autism isn't one thing.
We mapped every thing it is.

The atlas is a curated, continuously-ingested, evidence-balanced knowledge
graph of autism causation, phenotypes, biomarkers, and interventions —
treated as **eleven biological pattern dimensions**, not a single
classification.

Your child isn't a phenotype. **They're a shape on the map.**
"""
    )

    st.markdown("---")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("#### What you can do here")
        st.markdown(
            "- **Run a profile** — see how a child's biomarker / genetic / "
            "exposure profile loads across the eleven dimensions.\n"
            "- **Explore the atlas** — browse the underlying entities (genes, "
            "biomarkers, interventions) by table.\n"
            "- **Inspect contested entities** — every contested claim shows "
            "the mainstream consensus *and* the alternative evidence."
        )
    with c2:
        st.markdown("#### What this is built on")
        st.markdown(
            "- **1,420+** primary sources, every PMID PubMed-verified.\n"
            "- **11** biological phenotype dimensions across the autism map.\n"
            "- **178** measurable biomarkers linked to dimensions.\n"
            "- **137** interventions scored by composite suffering-reduction.\n"
            "- **Daily** PubMed ingestion — visible on the Freshness tab."
        )
    with c3:
        st.markdown("#### What this is not")
        st.markdown(
            "- Not a diagnosis or a prediction of any individual outcome.\n"
            "- Not a substitute for clinical judgement.\n"
            "- Not a regulated medical device.\n"
            "- Not finished — it is a research prototype that *shows its work*."
        )

    st.markdown("---")
    st.markdown(
        "#### How to read a profile\n"
        "When you run a profile, you'll get a **loading vector** across the "
        "eleven dimensions. Three flags tell you the *shape*:\n"
        "- **Focal** — one dimension clearly dominates. Targeted intervention "
        "candidates surface.\n"
        "- **Multi-pattern** — two or more dimensions co-dominate. Multi-target "
        "intervention candidates surface.\n"
        "- **Undifferentiated** — no dimension exceeds the threshold. The "
        "honest answer is: *more measurement is needed*, and the engine "
        "refuses to confidently rank interventions on insufficient signal."
    )

    st.markdown(
        "#### How to read a contested entity\n"
        "For every claim the literature is split on — vaccines, aluminum "
        "adjuvants, glyphosate, certain medications — the atlas records "
        "**both views at equal prominence**. The mainstream consensus position "
        "is shown first; the contested-evidence position appears beside it. "
        "The atlas does not pick a side; it preserves the shape of the "
        "real evidence landscape so individual decisions can be made with "
        "the full picture."
    )

    st.markdown(
        "#### How to read freshness\n"
        "The Freshness tab shows the live PubMed ingestion log. New papers "
        "ingested today, candidates awaiting curation, recent daily runs. "
        "If you can see the freshness log, the atlas is alive; if it stops, "
        "we say so."
    )

    st.markdown("---")
    st.caption(
        "Designed for functional-medicine practitioners and the families they "
        "serve. Built deterministic, open-source, and verification-first so "
        "anyone can audit the work."
    )


# ===========================================================================
# Tab 1 — Run calculator
# ===========================================================================
with tab_run:
    st.subheader("Step 1 — Provide a case")

    cases = list_calibration_cases()
    # Plain-language friendly labels mapped to the underlying case ids.
    CASE_LABEL_MAP = {
        "case_011_hannah_poling": "Mitochondrial vulnerability + multi-vaccine challenge (mtDNA / federally adjudicated 2008)",
        "case_015_frye_fraa_responder": "Cerebral folate deficiency / FRAA-positive responder profile (Frye 2018)",
        "case_020_walsh_undermethylator": "Walsh-framework undermethylator biotype (Pfeiffer / Walsh)",
        "case_026_22q11_deletion": "22q11.2 deletion syndrome (DiGeorge / VCFS) — syndromic gate test",
    }

    def _case_label(case_id: str) -> str:
        return CASE_LABEL_MAP.get(case_id, case_id)

    label_to_case = {_case_label(c): c for c in cases}
    case_options = ["(choose a sample profile)"] + list(label_to_case.keys()) + ["Upload my own input.json"]
    selection_label = st.selectbox(
        "Pick a sample profile from the literature, or upload your own input",
        options=case_options,
        index=0,
    )
    selection = label_to_case.get(selection_label, selection_label)

    input_data: dict | None = None
    case_label = None

    if selection in cases:
        input_data = load_calibration_input(selection)
        case_label = selection
        if input_data is None:
            st.error(f"Could not load profile data for {_case_label(selection)}")
        else:
            st.success(
                f"Loaded **{_case_label(selection)}** "
                f"({len(json.dumps(input_data))} bytes of profile data)"
            )

    elif selection == "Upload my own input.json":
        uploaded = st.file_uploader(
            "Upload an input.json conforming to the §3 schema",
            type=["json"],
            help="See SESSION_4_HANNAH_POLING_SPEC.md §3 for the input schema.",
        )
        if uploaded is not None:
            try:
                input_data = json.loads(uploaded.read().decode("utf-8"))
                case_label = uploaded.name
                st.success(f"Loaded `{uploaded.name}`")
            except Exception as exc:
                st.error(f"Could not parse JSON: {exc}")

    if input_data is not None:
        with st.expander("Inspect raw input.json", expanded=False):
            st.json(input_data)

        st.subheader("Step 2 — Run engine")
        if st.button("Compute personalized risk", type="primary", width="stretch"):
            with st.spinner("Running deterministic engine..."):
                output = compute_personalized_risk(input_data)
            st.session_state["last_output"] = output
            st.session_state["last_case_label"] = case_label

    # -----------------------------------------------------------------------
    # Render output (if we have one)
    # -----------------------------------------------------------------------
    output = st.session_state.get("last_output")
    if output is not None:
        st.markdown("---")
        st.subheader("Step 3 — Results")

        if output.get("status") != "success":
            st.error(f"Engine status: {output.get('status')}")
            errs = output.get("validation_errors") or []
            for e in errs:
                st.markdown(f"- `{e}`")
        else:
            # ---- Header strip: calibration + digest + flags ----
            col1, col2, col3, col4 = st.columns([1.1, 1.1, 1.6, 1.2])
            cal = output.get("calibration_status", {})
            col1.metric(
                "Calibration anchor",
                f"{cal.get('actual_csrs', '—')}",
                f"≥ {cal.get('required_csrs_min', '—')} required",
            )
            col2.metric(
                "Anchor passes",
                "yes" if cal.get("passes") else "NO",
            )
            digest = output.get("canonical_digest", "")
            col3.text_input(
                "canonical_digest (sha256)",
                value=digest,
                disabled=True,
                help="Byte-stable hash over deterministic output fields. Re-running the same input gives the same digest.",
            )
            col4.metric(
                "Operating mode",
                output.get("operating_mode") or "—",
            )

            # ---- Syndromic gate ----
            if output.get("syndromic_flag"):
                sm = output.get("syndromic_match", {}) or {}
                st.error(
                    f"**Rare-syndrome screening gate triggered** — "
                    f"{sm.get('syndrome_name', '?')} "
                    f"(`{sm.get('syndrome_match_id', '?')}` · "
                    f"matched on `{sm.get('matched_input', '?')}`)"
                )
                st.caption(
                    "Per spec §4, syndromic cases route to syndrome-specific output. "
                    "Generic phenotype posteriors below are emitted for transparency "
                    "but should be interpreted in light of the syndromic finding."
                )
                with st.expander("Syndromic match detail", expanded=True):
                    st.json(sm)
            else:
                st.info("Rare-syndrome screening gate did not trigger.")

            # ---- Profile loadings (v0.3 — replaces classification semantics) ----
            st.markdown("### Profile shape")
            ps = output.get("profile_summary", {}) or {}
            pl = output.get("profile_loadings", {}) or {}
            posteriors = output.get("phenotype_posteriors", {}) or {}
            ranking = output.get("phenotype_ranking", [])
            atlas = cached_load_atlas()
            phe_names = {r["id"]: r.get("name", "") for r in atlas.get("phenotypes", [])}

            # Profile-shape summary line
            dom = ps.get("dominant_dimensions", []) or []
            sec = ps.get("secondary_dimensions", []) or []
            multi = bool(ps.get("multi_pattern_flag"))
            undiff = bool(ps.get("undifferentiated_flag"))
            conc = ps.get("profile_concentration", 0.0)
            if undiff:
                shape_label = "**undifferentiated** — no dimension exceeds the dominance threshold"
                shape_color = "warning"
            elif multi:
                shape_label = f"**multi-pattern** — dominant: {', '.join(dom)}"
                shape_color = "info"
            else:
                shape_label = f"**focal** — dominant: {', '.join(dom) if dom else '—'}"
                shape_color = "success"
            st.markdown(
                f"{shape_label}  ·  concentration {conc:.3f}  ·  "
                f"max loading {ps.get('max_loading', 0):.3f}  ·  "
                f"dispersion {ps.get('profile_dispersion', 0):.3f}"
            )

            # Horizontal loading bars across all 11 dimensions
            st.markdown("**Loadings across the eleven phenotype dimensions**")
            DOMINANT_T = 0.55
            DORMANT_T = 0.45
            for phe_id in sorted(pl.keys()):
                loading = float(pl[phe_id])
                name = phe_names.get(phe_id, "")
                if loading >= DOMINANT_T:
                    band = "🟢"
                elif loading < DORMANT_T:
                    band = "⚫"
                else:
                    band = "⚪"
                bar_w = int(loading * 30)  # 30-char bar
                bar = "█" * bar_w + "░" * (30 - bar_w)
                # Use columns for stable layout
                c1, c2, c3, c4 = st.columns([0.6, 1.2, 2.5, 0.6])
                c1.text(f"{band} {phe_id}")
                c2.text(name[:28])
                c3.text(bar)
                c4.text(f"{loading:.3f}")

            st.caption(
                "🟢 dominant (≥0.55) · ⚪ secondary/neutral · ⚫ dormant (<0.45). "
                "Profile vector replaces single-phenotype classification (post-v0.2). "
                "A child has a *shape* across the dimensions, not a single category."
            )

            st.markdown("#### Per-dimension detail")
            st.caption(
                "Point estimate + Walley IDM-lite credal interval, confidence "
                "label, evidence tier, drivers. Click a dimension to expand."
            )

            for phe_id in ranking:
                p = posteriors.get(phe_id, {})
                point = p.get("point", 0.0)
                lo = p.get("credal_low", 0.0)
                hi = p.get("credal_high", 0.0)
                conf = p.get("confidence_label", "")
                tier_evid = p.get("phenotype_evidence_tier", "—")
                drivers = p.get("drivers", [])
                log_odds = p.get("log_odds", 0.0)

                name = phe_names.get(phe_id, "")
                header_label = f"**{phe_id}** — {name}"

                with st.expander(
                    f"{header_label}  ·  point {point:.3f}  ·  [{lo:.3f}, {hi:.3f}]  ·  {conf}",
                    expanded=(phe_id == ranking[0]),
                ):
                    cA, cB, cC = st.columns(3)
                    cA.metric("Point", f"{point:.3f}")
                    cB.metric("Credal low", f"{lo:.3f}")
                    cC.metric("Credal high", f"{hi:.3f}")

                    if tier == "Researcher":
                        st.caption(
                            f"log-odds = {log_odds:+.3f}  ·  evidence tier = "
                            f"{tier_evid}  ·  {len(drivers)} driver(s)"
                        )
                        if drivers:
                            st.markdown("**Drivers**")
                            st.dataframe(
                                drivers,
                                width="stretch",
                                hide_index=True,
                            )
                        else:
                            st.caption("No drivers contributed for this phenotype.")
                    elif tier == "Clinician":
                        if drivers:
                            sources = sorted({d.get("source", "?") for d in drivers})
                            st.markdown(
                                "**Evidence channels driving this posterior:** "
                                + ", ".join(sources)
                            )
                        else:
                            st.caption("No specific drivers in this profile.")
                        st.caption(
                            f"Evidence tier of phenotype itself: {tier_evid}"
                        )
                    else:  # Family / Curious
                        st.markdown(
                            "**Plain-language summary** — this is the engine's "
                            "estimate of how strongly the literature linked to this "
                            "child's profile points toward this phenotype cluster, "
                            "compared to a generic baseline. It is not a diagnosis."
                        )
                        if drivers:
                            sources = sorted({d.get("source", "?") for d in drivers})
                            st.markdown(
                                "**What's driving this estimate:** "
                                + ", ".join(sources)
                            )

            # ---- Intervention bundle ----
            st.markdown("### Intervention ranking")
            ib = output.get("intervention_bundle", [])
            if not ib:
                st.caption(
                    "No interventions ranked. (Syndromic cases bypass the "
                    "generic intervention bundle per spec §4.)"
                )
            else:
                for item in ib:
                    cols = st.columns([1.0, 2.0, 1.2, 1.4, 1.4])
                    cols[0].markdown(f"**{item.get('intervention_id', '?')}**")
                    cols[1].markdown(item.get("name", ""))
                    cols[2].markdown(f"_{item.get('recommendation_type', '')}_")
                    primary_dim = item.get("primary_target_dimension") or "—"
                    targets = item.get("target_dimensions") or []
                    target_summary = (
                        f"`{primary_dim}`"
                        + (f" (+{len(targets)-1} more)" if len(targets) > 1 else "")
                    )
                    cols[3].markdown(f"target: {target_summary}")
                    score = float(item.get("score", 0.0) or 0.0)
                    best = float(item.get("best_match_score", 0.0) or 0.0)
                    cols[4].markdown(
                        f"score {score:.3f} · best-match {best:.3f}"
                    )

            # ---- Tier-specific extras ----
            if tier == "Researcher":
                st.markdown("### Researcher detail")
                with st.expander("Full output JSON", expanded=False):
                    st.json(output)
                with st.expander("Deferred features (v0.2 roadmap)"):
                    for f in output.get("deferred_features", []):
                        st.markdown(f"- `{f}`")
                if output.get("provisional_hardcoded_shifts"):
                    st.warning(
                        "`provisional_hardcoded_shifts: true` — many log-odds "
                        "values in v0.1 are stub priors pending priors-CSV "
                        "calibration. Treat magnitudes as illustrative."
                    )
            elif tier == "Clinician":
                st.markdown("### Clinician handoff")
                st.markdown(
                    "*The following is generated content for clinician review. "
                    "It is not a recommendation — it is a summary of what the "
                    "atlas links to this profile.*"
                )
                handoff_lines = [
                    f"- Case ID: `{output.get('case_id', '?')}`",
                    f"- Operating mode: `{output.get('operating_mode', '?')}`, sex: `{output.get('subject_sex', '?')}`",
                    f"- Calibration anchor: {CALIBRATION_ANCHOR_NAME} = "
                    f"{cal.get('actual_csrs', '—')} (required ≥ "
                    f"{cal.get('required_csrs_min', '—')})",
                ]
                if output.get("syndromic_flag"):
                    sm = output.get("syndromic_match", {}) or {}
                    handoff_lines.append(
                        f"- **Syndromic gate triggered**: "
                        f"{sm.get('syndrome_name', '?')} "
                        f"({sm.get('syndrome_match_id', '?')}) — "
                        f"route to syndrome-specific workup ({sm.get('target_routing', '?')}); "
                        f"primary ref PMID {sm.get('primary_pmid', '?')}"
                    )
                top = ranking[0] if ranking else None
                if top:
                    p = posteriors.get(top, {})
                    handoff_lines.append(
                        f"- Top phenotype: `{top}` "
                        f"({phe_names.get(top, '')}) — "
                        f"point {p.get('point', 0):.3f} "
                        f"[{p.get('credal_low', 0):.3f}, {p.get('credal_high', 0):.3f}]"
                    )
                if ib:
                    top_int = ib[0]
                    handoff_lines.append(
                        f"- Top atlas-linked intervention: "
                        f"`{top_int.get('intervention_id', '?')}` "
                        f"({top_int.get('name', '')})"
                    )
                handoff_lines.append(
                    f"- Engine: `{ENGINE_VERSION}`, atlas: `{ATLAS_VERSION}`, "
                    f"digest: `{digest[:16]}…`"
                )
                st.markdown("\n".join(handoff_lines))
                st.caption(
                    "Clinical interpretation requires full chart review. "
                    "v0.1 priors include stub log-odds; treat magnitudes as illustrative."
                )
            else:
                st.markdown("### Questions to discuss with your clinician")
                top = ranking[0] if ranking else None
                if output.get("syndromic_flag"):
                    sm = output.get("syndromic_match", {}) or {}
                    st.markdown(
                        f"- The atlas matched a known genetic syndrome pattern "
                        f"(*{sm.get('syndrome_name', '?')}*). Has your clinician "
                        f"discussed targeted workup for this?"
                    )
                if top:
                    p = posteriors.get(top, {})
                    st.markdown(
                        f"- The top-ranked phenotype cluster from the atlas is "
                        f"**{phe_names.get(top, top)}** "
                        f"(estimated probability ≈ {p.get('point', 0):.2f}). "
                        f"What workup or next steps are appropriate to "
                        f"investigate this cluster in our specific situation?"
                    )
                if ib:
                    top_int = ib[0]
                    st.markdown(
                        f"- The literature in the atlas links "
                        f"**{top_int.get('name', '')}** to this phenotype cluster. "
                        f"Is this appropriate to consider for our child? "
                        f"What evidence supports it, what doesn't?"
                    )
                st.caption(
                    "These are conversation prompts only. The engine cannot "
                    "make clinical decisions for you or your child."
                )

            # ---- Download ----
            st.markdown("### Download")
            st.download_button(
                "Download output.json",
                data=json.dumps(output, indent=2, sort_keys=True),
                file_name=f"output_{st.session_state.get('last_case_label','case')}.json",
                mime="application/json",
                width="stretch",
            )


# ===========================================================================
# Tab 2 — Atlas explorer
# ===========================================================================
with tab_atlas:
    st.subheader("Atlas explorer")
    st.caption(
        "Read-only view of the underlying knowledge graph. "
        "All entities are PMID-verified per CLAUDE.md verification protocol."
    )

    atlas = cached_load_atlas()

    counts = {k: len(v) for k, v in atlas.items()}
    st.markdown("**Atlas counts**")
    st.dataframe(
        [{"table": k, "rows": v} for k, v in sorted(counts.items())],
        width="stretch",
        hide_index=True,
    )

    sub_explore = st.selectbox(
        "Browse table",
        options=[
            "phenotypes",
            "interventions",
            "biomarkers",
            "iatrogenic_exposure_priors",
            "rare_syndrome_screening_gate",
            "baseline_phenotype_prevalence",
        ],
    )

    rows = atlas.get(sub_explore, [])
    if not rows:
        st.info(f"No rows in `{sub_explore}`.")
    else:
        # Show ID / name / status-like columns first
        priority_cols = [
            c
            for c in ["id", "name", "syndrome", "category", "status", "csrs_score"]
            if c in rows[0]
        ]
        other_cols = [c for c in rows[0].keys() if c not in priority_cols]
        col_order = priority_cols + other_cols

        q = st.text_input(
            "Filter (substring match across all columns)", value=""
        ).strip().lower()
        if q:
            filtered = [r for r in rows if any(q in str(v).lower() for v in r.values())]
        else:
            filtered = rows

        st.caption(f"Showing {len(filtered)} of {len(rows)} rows")
        st.dataframe(
            [{c: r.get(c, "") for c in col_order} for r in filtered[:500]],
            width="stretch",
            hide_index=True,
        )
        if len(filtered) > 500:
            st.caption("(truncated to 500 rows)")


# ===========================================================================
# Tab 3 — Contested entities (mainstream consensus + supporting/opposing)
# ===========================================================================
with tab_contested:
    st.subheader("Contested entities — evidence shown both ways")
    st.caption(
        "Every contested row in the atlas displays the mainstream regulatory "
        "consensus position **at equal prominence** with the contested-evidence "
        "position. Both views are recorded; the atlas does not pick a side. "
        "This is the structural defense against single-sided framing."
    )

    atlas = cached_load_atlas()

    def _render_contested_row(r, label_field, supporting_field, opposing_field, extra_meta_keys=None):
        """Render a single contested row with mainstream consensus first, then balanced PMIDs."""
        consensus = (r.get("mainstream_consensus_position") or "").strip()
        if consensus:
            st.markdown("**Mainstream consensus position** (what major medical bodies say)")
            st.markdown(f"> {consensus}")
        else:
            st.warning("Mainstream consensus position not yet populated for this row.")

        st.markdown("---")
        st.markdown("**Contested-evidence position** (what the atlas records as alternative evidence)")

        if extra_meta_keys:
            meta_strs = [f"`{k}`: {r.get(k,'—')}" for k in extra_meta_keys if r.get(k)]
            if meta_strs:
                st.caption(" · ".join(meta_strs))

        if supporting_field or opposing_field:
            sup_val = (r.get(supporting_field) or "").strip() if supporting_field else ""
            opp_val = (r.get(opposing_field) or "").strip() if opposing_field else ""
            col_s, col_o = st.columns(2)
            with col_s:
                st.markdown("*Primary (supporting):*")
                if sup_val:
                    for p in sup_val.split(";"):
                        p = p.strip()
                        if p:
                            st.markdown(f"- [PMID {p}](https://pubmed.ncbi.nlm.nih.gov/{p}/)")
                else:
                    st.caption("(none populated)")
            with col_o:
                st.markdown("*Countervailing (opposing):*")
                if opp_val:
                    for p in opp_val.split(";"):
                        p = p.strip()
                        if p:
                            st.markdown(f"- [PMID {p}](https://pubmed.ncbi.nlm.nih.gov/{p}/)")
                else:
                    st.caption("(none populated)")
        else:
            st.caption(
                "PMID lists for this entity flow through the atlas's evidence_links "
                "graph rather than per-row supporting/opposing fields. The "
                "mainstream consensus position above is the structural balance."
            )

        notes = (r.get("notes") or "").strip()
        if notes:
            st.markdown("---")
            st.markdown("**Atlas notes**")
            st.markdown(f"_{notes[:600]}_{'…' if len(notes) > 600 else ''}")

    def _section(title, rows, label_field, supporting_field, opposing_field, extra_meta_keys, label_template):
        contested = [r for r in rows if (r.get("status") or "").lower() == "contested"]
        st.markdown(f"### {title}")
        st.caption(f"{len(contested)} contested rows of {len(rows)} total in this table.")
        if not contested:
            st.info(f"No contested rows in {title}.")
            return
        for r in contested:
            label = label_template(r)
            with st.expander(label, expanded=False):
                _render_contested_row(r, label_field, supporting_field, opposing_field, extra_meta_keys)

    # Iatrogenic exposures (vaccines, medications, environmental)
    _section(
        "Iatrogenic & environmental exposures",
        atlas.get("iatrogenic", []),
        label_field="specific_agent",
        supporting_field="primary_pmids",
        opposing_field="countervailing_evidence_pmids",
        extra_meta_keys=["target_phenotype_id", "log_odds_shift", "evidence_quality"],
        label_template=lambda r: (
            f"**{r.get('id','?')}**  ·  {(r.get('specific_agent') or '').replace('_',' ')}  "
            f"·  target {r.get('target_phenotype_id','—')}  ·  log_odds_shift {r.get('log_odds_shift','—')}"
        ),
    )

    st.markdown("---")

    # Causation hypotheses
    _section(
        "Causation hypotheses",
        atlas.get("hypotheses", []),
        label_field="name",
        supporting_field=None,
        opposing_field=None,
        extra_meta_keys=None,
        label_template=lambda r: f"**{r.get('id','?')}**  ·  {r.get('name','?')[:80]}",
    )

    st.markdown("---")

    # Interventions
    _section(
        "Interventions",
        atlas.get("interventions", []),
        label_field="name",
        supporting_field=None,
        opposing_field=None,
        extra_meta_keys=["category", "csrs_score"],
        label_template=lambda r: f"**{r.get('id','?')}**  ·  {r.get('name','?')[:60]}",
    )

    st.markdown("---")
    st.caption(
        "Other prior tables (rare_syndrome_screening_gate, "
        "baseline_phenotype_prevalence, genetic_id_aliases, pgx_drug_gene_table, "
        "physiological_state_normalization) carry the supporting/opposing PMID "
        "schema from Phase B. Most of those rows are mainstream-accepted "
        "(syndromes, prevalence estimates, CPIC pharmacogenomics) and don't have "
        "contested status — but the schema is in place for any future row that "
        "earns the contested flag."
    )


# ===========================================================================
# Tab 4 — Freshness (continuous ingestion log)
# ===========================================================================
with tab_freshness:
    st.subheader("Freshness — continuous ingestion log")
    st.caption(
        "Daily PubMed ingestion via `scripts/continuous_ingestion.py`. Every new "
        "candidate passes through the verify-before-write protocol before being "
        "queued for human curation. This page reads `freshness/freshness.json`. "
        "If you don't see today's run, the daily cron has not yet executed."
    )

    fresh_path = REPO_ROOT / "freshness" / "freshness.json"
    if not fresh_path.exists():
        st.warning(
            "No freshness data yet. Run `python scripts/continuous_ingestion.py "
            "--commit` then `python scripts/build_freshness_page.py` to populate."
        )
    else:
        try:
            fresh = json.loads(fresh_path.read_text())
        except Exception as e:
            st.error(f"Could not read freshness.json: {e}")
            fresh = {}

        c1, c2, c3 = st.columns(3)
        c1.metric("Atlas PMIDs", fresh.get("atlas_pmid_count", "—"))
        c2.metric("In curation queue", fresh.get("queue_size", "—"))
        c3.metric("Daily logs", len(fresh.get("last_30_daily_logs", [])))

        st.caption(f"freshness.json generated at: `{fresh.get('generated_at_utc','?')}`")

        st.markdown("### Recent daily ingestion runs")
        logs = fresh.get("last_30_daily_logs", []) or []
        if not logs:
            st.caption("No daily runs logged yet.")
        else:
            for log in reversed(logs):
                st.markdown(
                    f"- `{log.get('run_at_utc','?')}` — "
                    f"queries: {log.get('queries_run',0)}, "
                    f"candidates: {log.get('candidates_found',0)}, "
                    f"verified+queued: {log.get('verified_added_to_queue',0)}, "
                    f"atlas size: {log.get('atlas_pmid_count','?')}"
                )

        st.markdown("### Curation queue (50 most recent)")
        preview = fresh.get("queue_preview", []) or []
        if not preview:
            st.caption("Queue is empty.")
        else:
            for q in preview[:50]:
                pmid = q.get("pmid", "?")
                st.markdown(
                    f"- [PMID {pmid}](https://pubmed.ncbi.nlm.nih.gov/{pmid}/)  ·  "
                    f"_{q.get('journal','?')} {q.get('pubdate','')}_  ·  "
                    f"{q.get('title','')[:120]}"
                )

    st.markdown("---")
    st.caption(
        "**Why this page exists:** the lethal failure mode for any knowledge "
        "graph is becoming stale and unfalsifiable. Publishing the live "
        "ingestion log makes 'your atlas is out of date' falsifiable in real "
        "time, and turns the verification protocol from a defensive measure "
        "into a public feature."
    )


# ===========================================================================
# Tab 5 — Methodology
# ===========================================================================
with tab_method:
    st.subheader("Methodology — what this engine does")

    st.markdown(
        """
**Pipeline (per `SESSION_4_HANNAH_POLING_SPEC.md` §15 Phase 2):**

1. **Load + validate input** against the §3 schema.
2. **Rare-syndrome screening gate (§4).** If a known monogenic / CNV
   syndrome (22q11.2 deletion, FXS, RTT, TSC, PTEN, etc.) is present,
   the engine routes to syndrome-specific output before generic
   phenotype assignment.
3. **Genetic prior aggregation (§3.1).** Variants in `genetic_id_aliases`
   contribute log-odds shifts to phenotype priors.
4. **Biomarker prior aggregation (§3.2).** Out-of-range biomarker values
   contribute log-odds shifts. v0.1 uses raw values (no physiological-
   state normalization yet).
5. **Iatrogenic / exposure aggregation (§3.3, §3.13c).** Maternal,
   gestational, *and postnatal* (audit fix C-5) exposures contribute
   shifts where they match `iatrogenic_exposure_priors` rows.
6. **Phenotype posterior** = `sigmoid(log-odds_baseline + Σ shifts)`,
   with §6 conflict resolution (subgroup-conditional rows supersede
   population-average for the same anchor).
7. **Intervention ranking (§7.10).** Each phenotype's atlas-linked
   interventions are weighted by phenotype posterior and CSRS.
8. **Canonical digest.** SHA-256 over deterministic-output fields
   (excluding the timestamp) — re-running the same input gives the
   same digest.

**What's deferred to v0.2:**
"""
    )
    deferred = [
        "Full Walley IDM credal aggregation with quadrature (§7.1)",
        "Within-phenotype responder model (§7.5)",
        "CDR state assignment (§7.6) — experimental per spec",
        "Functional trajectory predictor (§7.7) — qualitative bands only",
        "Pathway burden analysis (§7.4) — needs pathway_burden_table.csv",
        "Cross-modality concordance bonus (§6.2)",
        "PGx safety filter integration (§3.8)",
        "Physiological state normalization full scale-up (§3.13b)",
        "Evidence-quality-weighted credal bands",
        "Sex-stratified baselines + life-stage-filtered intervention ranking",
    ]
    for d in deferred:
        st.markdown(f"- {d}")

    st.markdown("**Calibration**")
    st.markdown(
        f"- INT-0001 leucovorin CSRS = **{CALIBRATION_ANCHOR_CURRENT_CSRS}** "
        f"(required ≥ {CALIBRATION_ANCHOR_REQUIRED_CSRS}). The engine refuses "
        f"to run if this anchor fails."
    )
    st.markdown(
        "- Four literature-derived calibration cases (mtDNA-heteroplasmy + "
        "multi-vaccine challenge profile [federally adjudicated 2008], "
        "Frye FRAA-responder, Walsh undermethylator, 22q11.2 deletion) "
        "currently pass against v0.2 profile-vector expectations."
    )

    st.markdown("**Determinism guarantees**")
    st.markdown(
        "- No LLMs in scoring math. No random seeds. Stable sort by ID. "
        "Idempotent ingestion via `node_aliases`. UTF-8 + `newline=''` CSV "
        "loading. SHA-256 canonical digest over deterministic fields."
    )


# ===========================================================================
# Tab 4 — About / Disclaimer
# ===========================================================================
with tab_about:
    st.markdown(LONG_DISCLAIMER)
    st.markdown("---")
    st.markdown("### Open source")
    st.markdown(
        "The engine, atlas CSVs, calibration cases, and this UI are intended "
        "for open release at v0.1-alpha. See `MASTER_README.md`, "
        "`SESSION_4_HANNAH_POLING_SPEC.md`, and `CLAUDE.md` for full framing."
    )
    st.markdown("### Citation")
    st.markdown(
        "If you use this work, please cite the Causes Atlas (Autism) v0.1-alpha "
        "and the underlying primary sources (PMIDs are tracked per row in the "
        "atlas CSVs)."
    )
    st.markdown("### Contact")
    st.markdown(
        "This is a research prototype released for transparency and feedback. "
        "Bug reports, missing primary evidence, and methodology critique are "
        "all welcome."
    )
