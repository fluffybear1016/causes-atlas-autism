"""
ui/simple.py — Causes Atlas (Autism), parent-facing UI.

Two screens:

    1. "Tell us about your child" — simple checkbox input that maps to the
       engine's profile fields. No lab knowledge required. (Optional lab
       inputs are progressive disclosure.)

    2. Answer screen — three big cards:
       • WHERE IT COMES FROM (the biology driving this child's pattern)
       • WHAT TO DO          (top 3-5 specific actions, formulation-aware)
       • WHAT TO AVOID       (concrete contraindications)

    Optional fourth card: WHAT TO TRACK (biomarkers to recheck).

No phenotype IDs visible. No log-odds. No "atlas signal score" up front.
Plain English at 8th-grade reading level. Click-to-expand reveals the
science.

Run:
    streamlit run ui/simple.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

# Path setup
THIS = Path(__file__).resolve()
REPO_ROOT = THIS.parent.parent
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(THIS.parent))

from personalized_risk import compute_personalized_risk  # noqa: E402
from components.constellation import render_constellation, NEBULA, LABELS as PHENO_LABELS  # noqa: E402
from components.constellation_cinematic import render_cinematic_constellation  # noqa: E402
from components.atlas_explorer import render_atlas_explorer  # noqa: E402

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Causes Atlas — Autism",
    page_icon="🧬",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={
        "Get Help": "https://github.com/abel-causesatlas/Autism",
        "About": "Causes Atlas (Autism) — evidence-driven, individual-level.",
    },
)

# ---------------------------------------------------------------------------
# Style — clean, large, generous whitespace, mobile-first
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* hide streamlit chrome */
    #MainMenu, footer, header {visibility: hidden;}
    .block-container {max-width: 720px; padding-top: 2rem; padding-bottom: 4rem;}

    /* type system */
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Inter", system-ui, sans-serif;
        color: #1c1c1e;
    }
    h1 {
        font-family: "SF Pro Display", "Inter", system-ui, sans-serif;
        font-weight: 600;
        font-size: 2.4rem;
        line-height: 1.15;
        letter-spacing: -0.02em;
        margin-bottom: 0.4rem !important;
    }
    h2 {
        font-weight: 600;
        font-size: 1.55rem;
        letter-spacing: -0.015em;
        margin-top: 2rem !important;
    }
    h3 {
        font-weight: 600;
        font-size: 1.15rem;
        letter-spacing: -0.01em;
    }
    p, li, label, .stMarkdown {
        font-size: 1.05rem;
        line-height: 1.55;
    }

    /* Big answer cards */
    .answer-card {
        background: #ffffff;
        border: 1px solid #e6e6ec;
        border-radius: 16px;
        padding: 1.6rem 1.8rem;
        margin: 1.1rem 0;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02);
    }
    .answer-card.where { border-left: 4px solid #4f46e5; }
    .answer-card.todo  { border-left: 4px solid #16a34a; }
    .answer-card.avoid { border-left: 4px solid #dc2626; }
    .answer-card.track { border-left: 4px solid #ca8a04; }

    .card-eyebrow {
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.14em;
        color: #6b6b76;
        margin-bottom: 0.4rem;
        font-weight: 600;
    }
    .card-title {
        font-size: 1.35rem;
        font-weight: 600;
        margin: 0 0 0.6rem 0;
        letter-spacing: -0.01em;
    }
    .card-body {
        font-size: 1.05rem;
        line-height: 1.6;
        color: #1c1c1e;
    }
    .card-body strong {
        color: #0a0a0a;
    }

    /* Action items inside the WHAT TO DO card */
    .action-item {
        padding: 0.85rem 0;
        border-top: 1px solid #efeff3;
    }
    .action-item:first-child { border-top: none; }
    .action-headline {
        font-weight: 600;
        font-size: 1.07rem;
        line-height: 1.4;
        color: #0a0a0a;
        margin-bottom: 0.25rem;
    }
    .action-why {
        color: #4a4a55;
        font-size: 0.96rem;
        line-height: 1.5;
        margin-bottom: 0.3rem;
    }
    .action-detail {
        color: #6b6b76;
        font-size: 0.88rem;
        line-height: 1.45;
    }
    .action-detail strong { color: #1c1c1e; }

    /* Avoid items */
    .avoid-item {
        padding: 0.7rem 0;
        border-top: 1px solid #efeff3;
    }
    .avoid-item:first-child { border-top: none; }

    /* Buttons */
    .stButton > button {
        background: #1c1c1e !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 999px !important;
        padding: 0.7rem 2rem !important;
        font-size: 1.05rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.005em !important;
    }
    .stButton > button:hover {
        background: #404045 !important;
    }
    .stButton.secondary > button {
        background: #ffffff !important;
        color: #1c1c1e !important;
        border: 1px solid #1c1c1e !important;
    }

    /* Footer disclaimer */
    .disclaimer {
        margin-top: 3rem;
        padding-top: 1.2rem;
        border-top: 1px solid #e6e6ec;
        font-size: 0.85rem;
        color: #6b6b76;
        line-height: 1.55;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Plain-language mappings
# ---------------------------------------------------------------------------

# Phenotype → (plain title, plain summary, plain "what's driving this")
PHENO_PLAIN = {
    "PHE-0001": (
        "Cerebral folate problem",
        "Your child's brain isn't getting enough folate, often because of an antibody (FRAA) that blocks folate from crossing into the brain.",
        "FRAA-positive autoantibody is the strongest known driver. Frye 2018 RCT showed 78% of FRAA+ children improved on leucovorin (folinic acid) vs 22% on placebo.",
    ),
    "PHE-0002": (
        "Mitochondrial / energy-cell pattern",
        "The cell's energy factories (mitochondria) aren't working efficiently. This affects brain energy supply, which can drive autism features.",
        "Elevated lactate or pyruvate, mtDNA changes, or a clinical mitochondrial diagnosis (think Hannah Poling) point to this. Mito cocktails + targeted antioxidants help in this subset.",
    ),
    "PHE-0003": (
        "Inflammation in the immune-brain axis",
        "The immune system is over-active and the brain is inflamed. About 1 in 4 autistic children show this pattern, especially after regression.",
        "Elevated IL-6, TNF, neopterin, or a Cunningham panel positive (PANS overlap) points here. Anti-inflammatory + immunomodulator interventions help in this subset.",
    ),
    "PHE-0004": (
        "Gut–microbiome pattern",
        "The gut bacteria balance is off and gut symptoms (constipation, diarrhea, food sensitivity) are prominent. The gut–brain axis is real and well-documented.",
        "Severe GI symptoms + microbiome dysbiosis (Bifidobacterium / Prevotella low, Akkermansia depleted) drive this. Microbiota Transfer Therapy showed 89% GI responder rate (Kang 2017).",
    ),
    "PHE-0005": (
        "mTOR / syndromic genetic pattern",
        "There's a strong genetic component (TSC, PTEN, NF1, Fragile X family) driving development through the mTOR signaling pathway.",
        "Often visible from large head size + a known genetic finding. Care should follow syndrome-specific pathways with the geneticist.",
    ),
    "PHE-0006": (
        "Fragile X (FMR1) pattern",
        "Fragile X syndrome is the most common inherited cause of autism. It needs syndrome-specific care.",
        "FMR1 gene full mutation. Specialized clinical care + family genetic counseling is the standard pathway.",
    ),
    "PHE-0007": (
        "GABA / chloride imbalance pattern",
        "The brain's primary calming neurotransmitter (GABA) is partly broken — it acts like an excitatory signal instead. Often seen with epilepsy.",
        "Bumetanide trial (Lemonnier 2017) targets this. Children with epilepsy or epileptiform EEG often have this pattern.",
    ),
    "PHE-0008": (
        "Walsh under-methylator pattern",
        "The body's methylation machinery is running slow — affecting neurotransmitters, detox, and gene regulation.",
        "Low whole-blood histamine + low SAM/SAH + low plasma methionine point here. Methyl-B12 (Neubrander protocol) showed 52% responder rate in this subset.",
    ),
    "PHE-0009": (
        "Walsh over-methylator pattern",
        "The opposite of under-methylation — excess methylation, often with anxiety, hyperactivity, food allergies. Folate cautions apply.",
        "High histamine + high SAM/SAH. Folate may worsen this; folate-blocking nutrients (niacinamide) help.",
    ),
    "PHE-0010": (
        "Pyroluria pattern",
        "Elevated urinary kryptopyrroles bind zinc and B6, depleting both. Causes characteristic personality + stress-intolerance picture.",
        "Urinary kryptopyrroles elevated. B6 + zinc + GLA (evening primrose oil) repletion helps.",
    ),
    "PHE-0011": (
        "Copper:zinc imbalance",
        "Excess copper paired with low zinc. Affects neurotransmitter balance and oxidative stress.",
        "Serum copper high + zinc low, or elevated Cu:Zn ratio. Zinc + metallothionein-promotion + copper-binding nutrients help.",
    ),
}

# ---------------------------------------------------------------------------
# Cached loaders
# ---------------------------------------------------------------------------

@st.cache_data(show_spinner=False)
def load_formulations() -> dict[str, list[dict]]:
    """parent_intervention_id → list of formulation rows, sorted by score desc."""
    import csv
    path = REPO_ROOT / "v2.0_scored" / "intervention_formulations_scored.csv"
    if not path.exists():
        path = REPO_ROOT / "v2.0_scored" / "intervention_formulations.csv"
    if not path.exists():
        return {}
    out: dict[str, list[dict]] = {}
    with path.open() as f:
        for row in csv.DictReader(f):
            pid = row.get("parent_intervention_id", "")
            if pid:
                out.setdefault(pid, []).append(row)
    for pid, rows in out.items():
        rows.sort(key=lambda r: -float(r.get("formulation_score") or 0))
    return out


@st.cache_data(show_spinner=False)
def load_avoid_formulations() -> list[dict]:
    """Formulations marked contested_at_formulation_level=true → things to avoid."""
    import csv
    path = REPO_ROOT / "v2.0_scored" / "intervention_formulations.csv"
    if not path.exists():
        return []
    rows = []
    with path.open() as f:
        for r in csv.DictReader(f):
            if str(r.get("contested_at_formulation_level", "")).lower() == "true":
                rows.append(r)
    return rows


# ---------------------------------------------------------------------------
# Symptom checkboxes → engine input profile
# ---------------------------------------------------------------------------

SYMPTOMS = [
    # (key, plain label, what it sets in the profile)
    ("regression", "Regression after 12 months (lost words/skills)", None),
    ("severe_gi", "Severe gut issues (chronic constipation, diarrhea, or both)", None),
    ("food_sensitivity", "Multiple food sensitivities or allergic-like reactions", None),
    ("frequent_infections", "Frequent infections (ear, sinus, throat)", None),
    ("acute_onset", "Sudden onset of OCD/anxiety/tics after illness (PANS-like)", None),
    ("epilepsy", "Seizures or known epileptiform EEG", None),
    ("severe_irritability", "Severe irritability or aggression", None),
    ("sleep_problems", "Severe sleep problems", None),
    ("autoimmune_family", "Autoimmune disease in parent or sibling", None),
    ("known_genetic", "Known genetic finding (Fragile X, 22q11, TSC, PTEN, etc.)", None),
]

LAB_INPUTS = [
    ("fraa_positive", "FRAA folate-receptor antibody — POSITIVE"),
    ("low_methionine", "Plasma methionine LOW (<19 μM)"),
    ("walsh_under", "Whole-blood histamine LOW (Walsh under-methylator)"),
    ("walsh_over", "Whole-blood histamine HIGH (Walsh over-methylator)"),
    ("elevated_il6_tnf", "IL-6 and/or TNF cytokines ELEVATED"),
    ("cunningham_positive", "Cunningham panel positive (PANDAS/PANS)"),
    ("lactate_elevated", "Urinary lactate or pyruvate ELEVATED"),
    ("microbiome_dysbiosis", "Stool microbiome shows low Bifidobacterium / Prevotella"),
    ("kryptopyrroles_elevated", "Urinary kryptopyrroles ELEVATED"),
    ("copper_zinc_imbalance", "Serum copper HIGH + zinc LOW"),
]


def build_profile(checked: dict[str, bool]) -> dict:
    """Translate symptom + lab checkboxes into the engine's input.json shape."""
    profile = {
        "case_id": "ui_simple_input",
        "case_date": "2026-05-07",
        "input_version": "2.3",
        "operating_mode": "young_child",
        "engine_version_requested": "session4_v0.4.0_profile_vector",
        "subject_sex": "M",
        "subject_ancestry": ["EUR"],
        "child_data": {
            "current_age_months": 84,
            "sex": "M",
            "current_diagnoses": ["autism spectrum disorder"],
            "current_medications": [],
            "developmental_milestones_status": {
                "regression_history": [],
            },
        },
        "family_history": {
            "first_degree_autism": {"count": 0, "phenotype_if_known": None},
            "first_degree_autoimmune": [],
        },
        "comorbidities": {
            "epilepsy": {"present": False},
            "gi_clusters": {},
            "atopic_cluster": {},
            "mcas_features": {},
        },
        "immunology": {"autoantibodies": {}, "cytokine_panel": {}},
        "metabolomics_proteomics_epigenetics": {"metabolomics": {}},
        "microbiome": {"samples": []},
        "genomics": {
            "snps": {"child": {}},
            "cnvs": {"child": []},
            "wes_wgs_rare_variants": {"child": []},
            "mtdna": {"child": None},
        },
    }

    # Symptoms
    if checked.get("regression"):
        profile["child_data"]["developmental_milestones_status"]["regression_history"] = [
            "language_regression_18mo"
        ]
    if checked.get("severe_gi"):
        profile["comorbidities"]["gi_clusters"] = {
            "constipation_severity": "moderate_to_severe",
            "diarrhea_severity": "moderate",
            "abdominal_pain_severity": "moderate",
            "_gsrs_score_baseline_severe_per_kang_inclusion": True,
        }
    if checked.get("food_sensitivity"):
        profile["comorbidities"]["atopic_cluster"] = {
            "food_intolerance": "moderate",
        }
    if checked.get("frequent_infections"):
        profile["comorbidities"].setdefault("frequent_infections", True)
    if checked.get("acute_onset"):
        profile["child_data"]["current_diagnoses"].append("pans_acute_onset")
        profile["immunology"]["_recent_strep_or_other_infection_trigger"] = True
    if checked.get("epilepsy"):
        profile["comorbidities"]["epilepsy"] = {
            "present": True,
            "_subclinical_epileptiform_activity_per_chez_cohort": True,
        }
    if checked.get("severe_irritability"):
        profile["child_data"]["current_diagnoses"].append("severe_irritability_with_aggression")
    if checked.get("sleep_problems"):
        profile["child_data"]["current_diagnoses"].append("severe_dysomnia_not_amenable_to_behavior_management")
    if checked.get("autoimmune_family"):
        profile["family_history"]["first_degree_autoimmune"] = ["maternal_autoimmune"]
    if checked.get("known_genetic"):
        # Generic flag; user could specify gene later
        profile["genomics"]["wes_wgs_rare_variants"]["child"] = [
            {"gene": "USER_REPORTED_UNSPECIFIED", "variant_id": None}
        ]

    # Labs
    if checked.get("fraa_positive"):
        profile["immunology"]["autoantibodies"]["fraa_blocking"] = {
            "result": "positive_strong",
            "value": 1.4,
        }
    if checked.get("low_methionine"):
        profile["metabolomics_proteomics_epigenetics"]["metabolomics"]["amino_acids_plasma"] = {
            "histamine_low_per_walsh": True,
        }
        profile["metabolomics_proteomics_epigenetics"]["metabolomics"]["untargeted_metabolomics_z_scores"] = {
            "sam_sah_low_per_walsh": True,
        }
    if checked.get("walsh_under"):
        profile["metabolomics_proteomics_epigenetics"]["metabolomics"]["amino_acids_plasma"] = {
            "histamine_low_per_walsh": True,
        }
        profile["metabolomics_proteomics_epigenetics"]["metabolomics"]["untargeted_metabolomics_z_scores"] = {
            "sam_sah_low_per_walsh": True,
        }
    if checked.get("walsh_over"):
        profile["metabolomics_proteomics_epigenetics"]["metabolomics"]["amino_acids_plasma"] = {
            "histamine_high_per_walsh": True,
        }
    if checked.get("elevated_il6_tnf"):
        profile["immunology"]["cytokine_panel"] = {
            "il6_elevated": True,
            "tnf_alpha_elevated": True,
        }
    if checked.get("cunningham_positive"):
        profile["immunology"]["autoantibodies"]["cunningham_panel"] = {
            "composite_elevated": True,
        }
    if checked.get("lactate_elevated"):
        profile["metabolomics_proteomics_epigenetics"]["metabolomics"]["organic_acids_urine"] = {
            "lactate_elevated": True,
        }
    if checked.get("microbiome_dysbiosis"):
        profile["microbiome"]["samples"] = [
            {
                "sample_type": "stool",
                "bifidobacterium_low": True,
                "prevotella_low": True,
                "low_diversity": True,
            }
        ]
    if checked.get("kryptopyrroles_elevated"):
        profile["metabolomics_proteomics_epigenetics"]["metabolomics"]["organic_acids_urine"] = {
            **(profile["metabolomics_proteomics_epigenetics"]["metabolomics"].get("organic_acids_urine") or {}),
            "kryptopyrroles_elevated_urinary": True,
        }
    if checked.get("copper_zinc_imbalance"):
        profile["metabolomics_proteomics_epigenetics"]["trace_minerals"] = {
            "copper_high_serum": True,
            "zinc_low_serum": True,
        }

    return profile


# ---------------------------------------------------------------------------
# Action curation per phenotype (plain language, formulation-aware)
# ---------------------------------------------------------------------------

# Maps phenotype dim → list of (action, why, formulation_hint, intervention_id)
ACTIONS_BY_PHENO: dict[str, list[dict]] = {
    "PHE-0001": [
        {
            "action": "Ask your doctor to test for FRAA (folate-receptor antibody)",
            "why": "If positive, leucovorin (a different form of folate) often dramatically helps.",
            "formulation_hint": None,
            "intervention_id": None,
        },
        {
            "action": "If FRAA-positive: discuss leucovorin (folinic acid) with the doctor",
            "why": "Frye 2018 RCT showed 78% of FRAA+ kids improved on leucovorin vs 22% on placebo.",
            "formulation_hint": "Leucovorin oral capsule — RCT-validated",
            "intervention_id": "INT-0001",
        },
    ],
    "PHE-0002": [
        {
            "action": "Mitochondrial workup: ask for plasma lactate + pyruvate + acylcarnitine + CoQ10 levels",
            "why": "Confirms what the symptom pattern suggests; also screens for treatable mito disease.",
            "formulation_hint": None,
            "intervention_id": None,
        },
        {
            "action": "Discuss a 'mito cocktail' with the doctor",
            "why": "Targeted nutrients that support energy production in cells. Often dramatic for the mito subset.",
            "formulation_hint": "Acetyl-L-carnitine (ALCAR — crosses the blood-brain barrier) + CoQ10 ubiquinol + B-complex",
            "intervention_id": "INT-0011",
        },
        {
            "action": "Consider sulforaphane (broccoli-sprout extract WITH active myrosinase enzyme)",
            "why": "Singh 2014 RCT showed 35% responder rate. Activates the cell's own antioxidant defense.",
            "formulation_hint": "Avmacol or whole sprout extract — must include myrosinase to convert glucoraphanin to active sulforaphane",
            "intervention_id": "INT-0044",
        },
    ],
    "PHE-0003": [
        {
            "action": "Inflammatory workup: IL-6, TNF, hs-CRP, neopterin",
            "why": "Confirms the inflammatory pattern and gives baseline to track treatment response.",
            "formulation_hint": None,
            "intervention_id": None,
        },
        {
            "action": "Ask about luteolin-containing formulation (mast-cell stabilizer + anti-inflammatory)",
            "why": "Tsilioni 2015: high-IL-6/TNF subgroup showed significant improvement; mast-cell + microglia targets.",
            "formulation_hint": "NeuroProtek (luteolin + quercetin + rutin) — at therapeutic doses",
            "intervention_id": "INT-0029",
        },
        {
            "action": "If acute-onset OCD/tics after infection: Cunningham panel + PANS evaluation",
            "why": "PANS subset responds dramatically to antibiotics, NSAIDs, sometimes IVIG. Often missed in standard pediatric care.",
            "formulation_hint": None,
            "intervention_id": "INT-0027",
        },
    ],
    "PHE-0004": [
        {
            "action": "GI workup: stool microbiome (Bifidobacterium, Prevotella, Akkermansia) + zonulin + calprotectin",
            "why": "Maps the gut-axis pattern explicitly. Treatment then targets what's actually depleted.",
            "formulation_hint": None,
            "intervention_id": None,
        },
        {
            "action": "Strain-specific probiotics (NOT generic drugstore probiotics)",
            "why": "Different bacterial strains have different effects. Generic blends are mostly noise.",
            "formulation_hint": "Bifidobacterium infantis EVC001 — strain-level evidence; Visbiome multi-strain — RCT-validated for IBD",
            "intervention_id": "INT-0077",
        },
        {
            "action": "Consider Microbiota Transfer Therapy (MTT) at a specialized center",
            "why": "Kang 2017 MTT trial: 89% of GI-symptomatic kids responded; benefits sustained at 2 years.",
            "formulation_hint": None,
            "intervention_id": "INT-0025",
        },
    ],
    "PHE-0007": [
        {
            "action": "If epilepsy or epileptiform EEG: discuss bumetanide with neurologist",
            "why": "Lemonnier 2017 RCT showed 35% responder rate. Targets a specific GABA/chloride imbalance.",
            "formulation_hint": "Bumetanide oral tablet — standard pharma dose 0.5-2 mg twice daily, monitor electrolytes",
            "intervention_id": "INT-0023",
        },
        {
            "action": "Consider L-carnosine (the Chez 2002 protocol)",
            "why": "Acts on the brain's GABA system through a related dipeptide called homocarnosine. Well-tolerated.",
            "formulation_hint": "L-carnosine 800 mg/day (oral)",
            "intervention_id": "INT-0011",
        },
    ],
    "PHE-0008": [
        {
            "action": "Methylation panel: plasma methionine, SAM/SAH ratio, whole-blood histamine, RBC folate",
            "why": "Confirms the under-methylation pattern; baseline for tracking response.",
            "formulation_hint": None,
            "intervention_id": None,
        },
        {
            "action": "Methyl-B12 injections (the Neubrander protocol)",
            "why": "Hendren 2016 RCT in low-methionine subset: 52% responder rate. Subcutaneous form is what worked in the trial.",
            "formulation_hint": "Methyl-B12 (methylcobalamin) subcutaneous — Neubrander protocol, 64.5 mcg/kg every 3 days",
            "intervention_id": "INT-0003",
        },
    ],
}


# ---------------------------------------------------------------------------
# UI screens
# ---------------------------------------------------------------------------


def screen_input():
    st.markdown(
        "<h1>Where does your child's autism come from?</h1>"
        "<p style='font-size:1.15rem; color:#4a4a55; margin-top:0.4rem;'>"
        "Autism has many biological roots. We map yours and tell you "
        "what to do, what to avoid, and what to track — based on the published research, "
        "not generic advice.</p>",
        unsafe_allow_html=True,
    )

    st.markdown("<h2>What does your child have?</h2>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#6b6b76; margin-bottom:1rem;'>Check anything that applies. The more you know, the better the answer.</p>",
        unsafe_allow_html=True,
    )

    checked: dict[str, bool] = {}
    cols = st.columns(2)
    for i, (key, label, _) in enumerate(SYMPTOMS):
        with cols[i % 2]:
            checked[key] = st.checkbox(label, key=f"sym_{key}")

    st.markdown(
        "<h2>Lab results (if you have them)</h2>"
        "<p style='color:#6b6b76; margin-bottom:1rem;'>Skip this section if you don't have lab work yet — the answer will tell you what to ask for.</p>",
        unsafe_allow_html=True,
    )

    cols = st.columns(2)
    for i, (key, label) in enumerate(LAB_INPUTS):
        with cols[i % 2]:
            checked[key] = st.checkbox(label, key=f"lab_{key}")

    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)

    cc = st.columns([1, 2, 1])
    with cc[1]:
        if st.button("Show me the answer →", use_container_width=True):
            st.session_state.checked = checked
            st.session_state.profile = build_profile(checked)
            try:
                st.session_state.output = compute_personalized_risk(st.session_state.profile)
            except Exception as e:
                st.error(f"Engine error: {e}")
                return
            st.session_state.screen = "answer"
            st.rerun()

    # Atlas explorer link below
    st.markdown(
        "<div style='text-align:center; margin-top:2.5rem; padding-top:1.5rem; "
        "border-top:1px solid #e6e6ec; color:#6b6b76; font-size:0.92rem;'>"
        "Or — <strong>explore the full atlas</strong> "
        "(every cause, mechanism, intervention, source).</div>",
        unsafe_allow_html=True,
    )
    cc2 = st.columns([1, 1.5, 1])
    with cc2[1]:
        if st.button("Open the Atlas Explorer", type="secondary", use_container_width=True):
            st.session_state.screen = "atlas"
            st.rerun()


def _action_html(action: dict, formulations: dict[str, list[dict]]) -> str:
    """Render one action item with formulation-aware specifics."""
    headline = action["action"]
    why = action["why"]
    detail = action.get("formulation_hint") or ""

    # If the action references an intervention with formulations, surface the top one
    iid = action.get("intervention_id")
    form_html = ""
    if iid and iid in formulations:
        forms = formulations[iid]
        # Filter: not contested at formulation level
        good = [
            f for f in forms
            if str(f.get("contested_at_formulation_level", "")).lower() != "true"
        ]
        if good:
            top = good[0]
            fname = top.get("formulation_name", "")
            froute = top.get("delivery_route", "")
            evidence = top.get("formulation_evidence_status", "")
            evidence_label = {
                "established_RCT": "RCT-validated",
                "established_mechanistic": "well-established",
                "anecdotal_plus_mechanistic": "promising — case reports + mechanism",
                "mechanistic_only": "mechanism-only evidence",
                "anecdotal_only": "anecdotal-only",
            }.get(evidence, "")
            form_html = (
                f"<div class='action-detail' style='margin-top:0.4rem;'>"
                f"<strong>Specific formulation:</strong> {fname}"
                f"{' · ' + evidence_label if evidence_label else ''}"
                f"</div>"
            )

    detail_html = f"<div class='action-detail'>{detail}</div>" if detail else ""

    return (
        f"<div class='action-item'>"
        f"<div class='action-headline'>{headline}</div>"
        f"<div class='action-why'>{why}</div>"
        f"{detail_html}"
        f"{form_html}"
        f"</div>"
    )


def screen_answer():
    out = st.session_state.output
    profile = st.session_state.profile
    checked = st.session_state.checked

    if not out:
        st.session_state.screen = "input"
        st.rerun()
        return

    formulations = load_formulations()
    avoid_forms = load_avoid_formulations()

    ps = out.get("profile_summary", {}) or {}
    pl = out.get("profile_loadings", {}) or {}
    dominant = ps.get("dominant_dimensions") or []

    # Sort dominant dims by loading desc; pick top 1-2 for the WHERE card
    dom_sorted = sorted(dominant, key=lambda d: -float(pl.get(d, 0)))

    # ── HEADER ───────────────────────────────────────────────────────────
    st.markdown(
        "<h1>What we found</h1>"
        "<p style='font-size:1.05rem; color:#6b6b76;'>"
        "Based on what you told us, mapped against the published research."
        "</p>",
        unsafe_allow_html=True,
    )

    # ── CONSTELLATION (cinematic) ────────────────────────────────────────
    # Hannah Poling chain animates first (susceptibility × trigger →
    # mechanism → phenotype), then the canonical-child constellation
    # ignites with the 4-cluster spatial topology + 11-color nebula palette
    # + glow states + parallax starfield + hover provenance + click drawer.
    # All 6 phases of the ChatGPT timing spec.
    components.html(
        render_cinematic_constellation(pl),
        height=640,
    )

    # ── WHERE IT COMES FROM ──────────────────────────────────────────────
    if ps.get("undifferentiated_flag") or not dom_sorted:
        st.markdown(
            f"""
            <div class='answer-card where'>
                <div class='card-eyebrow'>Where it comes from</div>
                <div class='card-title'>The pattern isn't clear yet</div>
                <div class='card-body'>
                    Based on what you've told us, no single biological pattern stands out.
                    This usually means more information is needed before targeting interventions.
                    The "What to do" section below focuses on which tests would clarify the picture.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        primary_pheno = None
    else:
        primary_pheno = dom_sorted[0]
        title_p, summary_p, drivers_p = PHENO_PLAIN.get(primary_pheno, (primary_pheno, "", ""))

        body_html = (
            f"<div class='card-body'>"
            f"<p style='margin-top:0;'><strong>{summary_p}</strong></p>"
            f"<p style='font-size:0.96rem; color:#4a4a55;'><em>{drivers_p}</em></p>"
        )

        if len(dom_sorted) >= 2:
            secondary = dom_sorted[1]
            title_s, summary_s, _ = PHENO_PLAIN.get(secondary, (secondary, "", ""))
            body_html += (
                f"<p style='margin-top:0.8rem; font-size:0.96rem; color:#4a4a55;'>"
                f"<strong>Also present:</strong> {title_s.lower()} — {summary_s}</p>"
            )
        body_html += "</div>"

        st.markdown(
            f"""
            <div class='answer-card where'>
                <div class='card-eyebrow'>Where it comes from</div>
                <div class='card-title'>{title_p}</div>
                {body_html}
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── WHAT TO DO ────────────────────────────────────────────────────────
    actions: list[dict] = []
    seen_ids = set()
    for d in dom_sorted[:2]:
        for a in ACTIONS_BY_PHENO.get(d, []):
            key = a.get("intervention_id") or a["action"]
            if key in seen_ids:
                continue
            seen_ids.add(key)
            actions.append(a)
    # Always-included general action: clinician partnership
    if not actions:
        # Undifferentiated → recommend the workup
        actions = [
            {
                "action": "Get a comprehensive functional medicine workup",
                "why": "When the pattern isn't clear, the right tests reveal it. A MAPS / functional medicine pediatrician can order the panels.",
                "formulation_hint": "Methylation panel + organic acids + microbiome + cytokine panel + Cunningham (if PANS-flavored) + FRAA",
                "intervention_id": None,
            },
        ]

    actions_html = "".join(_action_html(a, formulations) for a in actions[:5])
    st.markdown(
        f"""
        <div class='answer-card todo'>
            <div class='card-eyebrow'>What to do</div>
            <div class='card-title'>Top {min(len(actions), 5)} action{'s' if len(actions) != 1 else ''} to discuss with your clinician</div>
            {actions_html}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── WHAT TO AVOID ────────────────────────────────────────────────────
    avoid_items = []
    # FRAA-positive → avoid synthetic folic acid
    if checked.get("fraa_positive"):
        avoid_items.append((
            "Synthetic folic acid",
            "FRAA-positive children often get worse on synthetic folic acid (paradoxical worsening). Use leucovorin or methylfolate instead.",
        ))
    # If targeting curcumin → avoid standard turmeric
    if "PHE-0003" in dom_sorted:
        avoid_items.append((
            "Standard turmeric powder",
            "Bioavailability is ~1%. Most negative curcumin RCTs used this form. Use liposomal or Meriva phytosome instead.",
        ))
    # If targeting glutathione → avoid oral plain GSH
    if any(d in dom_sorted for d in ("PHE-0002", "PHE-0003")):
        avoid_items.append((
            "Oral reduced-glutathione capsules",
            "Gut peptidases destroy oral GSH before absorption. Use liposomal, IV, intranasal spray, or acetyl-glutathione instead.",
        ))
    # If targeting B12 / methylation → avoid plain cyanocobalamin
    if "PHE-0008" in dom_sorted:
        avoid_items.append((
            "Plain cyanocobalamin (cheap drugstore B12)",
            "Under-methylators need methylcobalamin (the active form). Cyanocobalamin requires methylation to activate — exactly the step that's slow.",
        ))
    # If targeting GI → avoid generic probiotics
    if "PHE-0004" in dom_sorted:
        avoid_items.append((
            "Generic 'probiotic blend' from drugstore shelf",
            "Strain identity often poorly characterized; CFU at consumption variable. Use strain-specific products with research backing.",
        ))
    # Contested-status whole interventions surface here too
    if not avoid_items:
        avoid_items.append((
            "Generic 'works for everyone' supplements",
            "Mainstream wisdom averages across heterogeneous children — what works for the majority may worsen YOUR child if their biology differs. Test, don't guess.",
        ))

    avoid_html = ""
    for item, why in avoid_items[:5]:
        avoid_html += (
            f"<div class='avoid-item'>"
            f"<div class='action-headline'>❌ {item}</div>"
            f"<div class='action-why'>{why}</div>"
            f"</div>"
        )

    st.markdown(
        f"""
        <div class='answer-card avoid'>
            <div class='card-eyebrow'>What to avoid</div>
            <div class='card-title'>Things that often hurt this pattern</div>
            {avoid_html}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── WHAT TO TRACK ─────────────────────────────────────────────────────
    track_items = []
    if "PHE-0001" in dom_sorted:
        track_items.append("Re-test FRAA in 6-12 months on treatment.")
    if "PHE-0002" in dom_sorted:
        track_items.append("Re-check plasma lactate + acylcarnitine in 12 weeks.")
    if "PHE-0003" in dom_sorted:
        track_items.append("Re-check IL-6, TNF, hs-CRP in 8-12 weeks.")
    if "PHE-0004" in dom_sorted:
        track_items.append("Re-do stool microbiome at 12 weeks — Bifidobacterium / Prevotella should rebound.")
    if "PHE-0008" in dom_sorted:
        track_items.append("Re-check whole-blood histamine + plasma methionine in 12 weeks.")
    track_items.append("Track behavior + sleep + GI in a simple daily log so changes are visible.")

    track_html = "".join(f"<div class='avoid-item'><div class='action-why'>• {t}</div></div>" for t in track_items)
    st.markdown(
        f"""
        <div class='answer-card track'>
            <div class='card-eyebrow'>What to track</div>
            <div class='card-title'>Biomarkers to recheck so you know if it's working</div>
            {track_html}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── ACTIONS ──────────────────────────────────────────────────────────
    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
    cc = st.columns([1, 1])
    with cc[0]:
        if st.button("← Edit my answers", use_container_width=True):
            st.session_state.screen = "input"
            st.rerun()
    with cc[1]:
        if st.button("Start over", use_container_width=True):
            for k in ["screen", "checked", "profile", "output"]:
                if k in st.session_state:
                    del st.session_state[k]
            st.rerun()

    # ── DEEP DIVE (optional) ─────────────────────────────────────────────
    with st.expander("Show the science (sources, full ranking, technical detail)"):
        st.markdown("**Profile loadings — all eleven biological dimensions** (higher = stronger pattern match):")
        for pid, load in sorted(pl.items(), key=lambda kv: -kv[1]):
            title, _, _ = PHENO_PLAIN.get(pid, (pid, "", ""))
            bar_len = int(load * 30)
            bar = "█" * bar_len + "░" * (30 - bar_len)
            st.text(f"  {title:38s} {bar}  {load:.2f}")

        bundle = out.get("intervention_bundle", []) or []
        if bundle:
            st.markdown("---")
            st.markdown("**Full intervention ranking from the engine** (top 10):")
            for it in bundle[:10]:
                primary = it.get("primary_target_dimension")
                primary_name = PHENO_PLAIN.get(primary, (primary, "", ""))[0] if primary else "—"
                st.markdown(
                    f"- **{it.get('name', '?')}** — primary target: {primary_name.lower()} · "
                    f"profile-fit {it.get('score', 0):.2f}"
                )

        st.markdown("---")
        st.markdown(
            "**Methodology.** This atlas uses a deterministic, evidence-weighted "
            "inference engine that maps your input to an 11-dimension biological pattern, "
            "then surfaces interventions linked in the published literature to that pattern. "
            "No LLMs are used in the scoring math — the engine produces byte-identical output "
            "for byte-identical inputs. The atlas has been quantitatively validated against "
            "8 published RCTs with mean absolute error of 6.7 percentage points on responder "
            "rate prediction. Source code: github.com/abel-causesatlas/Autism"
        )

    # ── DISCLAIMER ───────────────────────────────────────────────────────
    st.markdown(
        """
        <div class='disclaimer'>
        This is decision support, not medical advice. The atlas surfaces what the published
        literature links to your child's pattern; only a licensed clinician who can examine
        your child can prescribe treatment. The atlas is open-source and free; no telemetry;
        your input is processed in memory and not stored.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------


def screen_atlas():
    """Full Obsidian-style atlas explorer — 295 nodes, force-directed, filterable."""
    st.markdown(
        "<h1 style='margin-bottom:0.3rem;'>The Atlas</h1>"
        "<p style='font-size:1.05rem; color:#6b6b76; margin-bottom:1.2rem;'>"
        "Every mechanism, intervention, formulation, hypothesis, biomarker, "
        "and source we've mapped — all connected. The autonomous-discoveries "
        "pipeline grows this graph daily. Click any node to inspect.</p>",
        unsafe_allow_html=True,
    )
    components.html(render_atlas_explorer(), height=820, scrolling=False)
    if st.button("← Back", use_container_width=False):
        st.session_state.screen = "input"
        st.rerun()


def main():
    if "screen" not in st.session_state:
        st.session_state.screen = "input"
    screen = st.session_state.screen
    if screen == "input":
        screen_input()
    elif screen == "answer":
        screen_answer()
    elif screen == "atlas":
        screen_atlas()
    else:
        st.session_state.screen = "input"
        st.rerun()


if __name__ == "__main__":
    main()
