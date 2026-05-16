#!/usr/bin/env python3
"""
build_living_graph.py
─────────────────────
Process v2.0_scored CSVs into a single self-contained HTML artifact that
renders the Causes Atlas as a breathing, self-organizing graph — the
cinematic surface. Karpathy-vault aesthetic, off-white nodes on deep
void, edge color encoded by source tier, slow node pulses. Multiple
susceptibility profiles + free-text intake so the graph reveals one
child's map in real time.

Output: /Users/Greg/Autism/living_graph.html

Determinism: stable sort by ID, no randomness in selection.
"""

from __future__ import annotations
import csv, json, pathlib, sys

_HERE = pathlib.Path(__file__).resolve().parent
_REPO = _HERE.parent
ROOT  = _REPO / "v2.0_scored"
OUT   = _REPO / "living_graph.html"

CAP_GENES         = 320
CAP_GENE_EDGES    = 260
CAP_INTERVENTIONS = 90
CAP_BIOMARKERS    = 80   # by edge-degree (how often referenced by other nodes)
CAP_COMBINATIONS  = 30   # all 25 fit; cap is defensive
CAP_TESTS         = 50   # top tests by leverage (Tier 1-2 DTC-friendly first)

# Sub-categorize interventions visually. Each I node gets a `c` field
# (category, drawn from interventions.csv `category` column). Peptides are
# flagged separately via the `p` field because they are the "next frontier"
# class — semantically a sub-type of supplement/drug, visually distinct.
INTERVENTION_PEPTIDE_KEYWORDS = (
    "peptide", "cerebrolysin", "selank", "semax", "oxytocin",
    "vasopressin", "bpc", "tb-500", "kpv", "ll-37", "thymosin",
    "igf-1", "sermorelin", "ipamorelin", "cjc-1295", "pacap",
    "vip", "epitalon", "carbetocin", "humanin", "mots-c", "p21",
    "dihexa", "ss-31", "tesamorelin", "elamipretide", "cortexin",
    "mecasermin",
)

# ── susceptibility profiles ───────────────────────────────────────────
# Each profile = keyword sets per node type. Seed nodes are matched by
# substring against label, then expanded one hop to capture connected
# mechanisms / interventions / phenotypes. The profile keys map 1-to-1
# to a JS-side toggle so the graph can switch reveals instantly.
PROFILES = [
    ("hp",      "Hannah Poling · mito + immune + contested-vaccine cluster", {
        "H": ("mitochondri", "vaccine", "aluminum", "alum", "thimerosal",
              "immune", "autoimmun", "hep b", "mmr", "encephalopath", "regress"),
        "M": ("mitochondri", "oxidative", "immune", "neuroinflam",
              "energy", "atp", "complex i", "glutathione"),
        "I": ("methylcobalamin", "coq10", "carnitine", "ubiquinol", "ldn",
              "ivig", "naltrexone", "glutathione", "creatine", "ribose",
              "nad", "leucovorin"),
        "P": ("regress", "encephalopath"),
    }),
    ("folr1",   "FOLR1+ · cerebral folate · leucovorin responder", {
        "H": ("folr1", "cerebral folate", "folate"),
        "M": ("folate", "methylation", "one-carbon"),
        "I": ("leucovorin", "folin", "folate", "5-methyl", "5-mthf"),
        "P": ("language", "speech", "communication"),
    }),
    ("mcas",    "MCAS · mast cell activation · histamine", {
        "H": ("mast", "mcas", "histamine", "allerg"),
        "M": ("histamine", "mast", "inflam"),
        "I": ("cromolyn", "ketotifen", "quercetin", "antihistamine",
              "ranitidine", "famotidine", "luteolin"),
        "P": ("gi", "sleep", "anxiety", "irritab"),
    }),
    ("pans",    "PANS / PANDAS · post-infectious autoimmune", {
        "H": ("pans", "pandas", "strep", "autoimmun", "obsess"),
        "M": ("autoimmune", "antibod", "basal ganglia", "neuroinflam"),
        "I": ("antibiotic", "ivig", "plasmapher", "ldn", "naltrexone",
              "nsaid", "azithro", "amoxi"),
        "P": ("ocd", "tic", "obsess", "anxiety", "regress"),
    }),
    ("methyl",  "Undermethylator · methylation cycle · Walsh phenotype", {
        "H": ("methyl", "sam", "homocyst", "mthfr", "one-carbon"),
        "M": ("methylation", "one-carbon", "sam", "methyl"),
        "I": ("methylcobalamin", "methylfolate", "sam-e", "tmg", "betaine",
              "b12", "b6", "p5p"),
        "P": (),
    }),
    ("mito",    "Mitochondrial-vulnerable", {
        "H": ("mito",),
        "M": ("mito", "energy", "atp", "complex", "oxidative"),
        "I": ("coq10", "ubiquinol", "carnitine", "creatine", "ribose",
              "nad", "pqq", "mito"),
        "P": ("regress", "fatigue"),
    }),
    ("gut",     "Gut–brain · microbiome · GI inflammation", {
        "H": ("gut", "microbiome", "gi ", "intestin", "leaky", "dysbio"),
        "M": ("microbiome", "endotox", "gi", "leaky", "tight junction", "scfa"),
        "I": ("probiotic", "bifid", "lactob", "butyrate", "glutamine",
              "gfcf", "low-fodmap"),
        "P": ("gi", "constipa", "diarrh"),
    }),
    ("hulscher", "Hulscher 9-factor framework · the full causation manifold", {
        "H": ("paternal age", "maternal age", "advanced", "preterm",
              "premature", "polygenic", "sfari", "sibling", "maternal immune",
              "MIA", "in utero", "valproate", "SSRI pregnancy", "pesticide",
              "phthalate", "BPA", "glyphosate", "PFAS", "heavy metal",
              "gut", "microbiome", "vaccine", "MMR", "thimerosal", "hep",
              "aluminum", "hypoxia", "asphyxia", "perinatal",
              "prenatal screening", "PAPP-A", "AFP"),
        "M": ("mitochondri", "neuroinflam", "oxidative", "methylation",
              "microbiome", "endotox", "placent"),
        "I": ("leucovorin", "methylcobalamin", "coq10", "carnitine",
              "omega-3", "DHA", "5-mthf", "folate", "ldn", "naltrexone",
              "sulforaphane", "ivig", "creatine"),
        "P": (),  # all phenotypes
    }),
]

# ── helpers ────────────────────────────────────────────────────────────
def read_csv(name: str) -> list[dict]:
    p = ROOT / name
    if not p.exists():
        return []
    with p.open() as f:
        return list(csv.DictReader(f))

def f(s, default: float = 0.0) -> float:
    try:    return float(s)
    except: return default

# ── load ───────────────────────────────────────────────────────────────
hyps  = read_csv("hypotheses.csv")
mecs  = read_csv("mechanisms.csv")
ints_ = read_csv("interventions.csv")
phes  = read_csv("phenotypes.csv")
genes = read_csv("genes.csv")

he   = read_csv("hypothesis_mechanism_edges.csv")
hh   = read_csv("hypothesis_hypothesis_edges.csv")
im_  = read_csv("intervention_mechanism_edges.csv")
ih   = read_csv("intervention_hypothesis_edges.csv")
ip_  = read_csv("intervention_phenotype_edges.csv")
mp   = read_csv("mechanism_phenotype_edges.csv")
gh   = read_csv("gene_hypothesis_edges.csv")
gm   = read_csv("gene_mechanism_edges.csv")

# 2026-05-14: extend living-graph layer with biomarkers + combinations.
# Adds two new node types (B, C) and their connecting edges. Makes the
# graph render the full causation manifold the user described —
# gene/variant -> mechanism/phenotype -> biomarker (what to test) ->
# intervention (what to do) -> combination (the actual stack).
bios = read_csv("biomarkers.csv")
combs = read_csv("combinations.csv")
cmms  = read_csv("combination_members.csv")
bie   = read_csv("biomarker_intervention_edges.csv")
bme   = read_csv("biomarker_mechanism_edges.csv")
bpe   = read_csv("biomarker_phenotype_edges.csv")
bhe   = read_csv("biomarker_hypothesis_edges.csv")
tests = read_csv("tests_catalog.csv")  # 2026-05-15: FM actionable test catalog

# ── plain-English phenotype descriptions for the action card ───────────
# These are mom-language one-liners used in the click-reveal card.
# Curator-written, not auto-generated, so the framing stays warm and
# non-clinical.
PHENOTYPE_PLAIN_ENGLISH = {
    "PHE-0001": "Antibodies block folate from reaching the brain. "
                 "The fix when this is the driver is dramatic.",
    "PHE-0002": "The cell's energy factories aren't keeping up. "
                 "Stressors hit harder than they would otherwise.",
    "PHE-0003": "The immune system is fighting the wrong fight, "
                 "and brain inflammation follows.",
    "PHE-0004": "Gut imbalance is sending the wrong signals to the brain. "
                 "Repair the gut, the signals normalize.",
    "PHE-0005": "Growth-signaling pathway running too hot. Often syndromic.",
    "PHE-0006": "Fragile X / FMR1 silencing. Targeted protein cascades "
                 "can be addressed directly.",
    "PHE-0007": "GABA hasn't matured from excitatory to inhibitory. "
                 "Brain stays over-aroused.",
    "PHE-0008": "Mast cells releasing histamine and inflammatory mediators "
                 "without an obvious trigger.",
    "PHE-0009": "Sudden-onset OCD / tics / regression after a strep or "
                 "viral infection — autoimmune attack on basal ganglia.",
    "PHE-0010": "Walsh undermethylator: methylation cycle running cold. "
                 "Common in autism; check before starting methyl-donors.",
    "PHE-0011": "Walsh metallothionein-deficient: copper:zinc imbalance "
                 "+ heavy-metal handling compromised.",
}

# Avoid / track guidance per phenotype (mom-actionable)
PHENOTYPE_AVOID = {
    "PHE-0001": "Synthetic folic acid (fortified foods, generic prenatals). "
                 "Methylated folate before FRAA testing in COMT++ kids.",
    "PHE-0002": "Mitochondrial toxins: fluoroquinolones, statins, valproate. "
                 "Avoid fasting in young children with mito-flag profile.",
    "PHE-0003": "NSAIDs during acute inflammation; high-histamine foods "
                 "until inflammation is settled.",
    "PHE-0004": "Sugar, alcohol-derived antibiotics (kids), unnecessary "
                 "antibiotic courses, glyphosate-treated grains.",
    "PHE-0005": "Most mTOR pathway agonists; consult specialist before "
                 "introducing new growth-signaling supplements.",
    "PHE-0006": "Sensory overload; check fragile-X-specific medication "
                 "considerations with geneticist.",
    "PHE-0007": "Glutamate-rich foods (MSG, hydrolyzed proteins, aged "
                 "cheeses) until GABA tone improves.",
    "PHE-0008": "High-histamine foods (aged, fermented, leftover); "
                 "trigger foods identified via elimination.",
    "PHE-0009": "Don't watch and wait if onset was sudden — treat "
                 "underlying infection + immune dysregulation.",
    "PHE-0010": "Folic acid (synthetic). Folate-fortified foods. "
                 "Start methyl donors LOW to avoid over-methylation.",
    "PHE-0011": "Copper-rich water (old plumbing); copper IUDs; "
                 "supplements containing copper.",
}

PHENOTYPE_TRACK = {
    "PHE-0001": "Re-check FRAA + behavior at 6 months. If responder, "
                 "speech / language milestones at 3-month intervals.",
    "PHE-0002": "Lactate + acylcarnitine at 6 months. Sleep, fatigue, "
                 "exercise tolerance weekly.",
    "PHE-0003": "Cytokines + CRP at 8-12 weeks. Sleep quality + GI + "
                 "behavior daily log.",
    "PHE-0004": "Repeat GI-MAP at 6 months. Stool consistency, food "
                 "tolerance, regression episodes weekly.",
    "PHE-0005": "Specialist follow-up. Imaging if indicated.",
    "PHE-0006": "Genetic counseling check-in. Targeted symptom tracking.",
    "PHE-0007": "EEG / qEEG if sleep-disturbed. Anxiety, agitation, "
                 "irritability daily.",
    "PHE-0008": "Histamine, tryptase at 3 months. Food-reaction diary daily.",
    "PHE-0009": "Cunningham Panel + behavior at 3 months. Tic frequency, "
                 "OCD severity, mood daily.",
    "PHE-0010": "SAM/SAH ratio at 8 weeks. Anxiety, sleep, behavior weekly.",
    "PHE-0011": "Cu:Zn ratio at 8 weeks. Behavior, sensory sensitivity weekly.",
}

# ── nodes ──────────────────────────────────────────────────────────────
nodes: list[dict] = []
node_ids: set[str] = set()
nodes_by_type: dict[str, list[dict]] = {
    "H": [], "M": [], "I": [], "P": [], "G": [],
    "B": [],   # biomarkers — "what to test" (marker level)
    "C": [],   # combinations — typed protocol stacks
    "T": [],   # tests — the FM-actionable diagnostic surface (panel level)
}

def add_node(nid, ntype, label, size, extra=None):
    if not nid or nid in node_ids:
        return
    node_ids.add(nid)
    extra = extra or {}
    # Build the searchable text. Include the label plus any classification
    # fields so that typing "peptide" lights up all I nodes whose category
    # is "peptide" even when the actual molecule name (e.g. "Cerebrolysin",
    # "Selank") doesn't contain that word. Same for "drug", "lifestyle", etc.
    search_parts = [(label or "").lower(), nid.lower()]
    if "c" in extra and extra["c"]:
        search_parts.append(str(extra["c"]).lower())
    # Type-class keywords so typing "biomarker", "combination", "hypothesis"
    # etc. surfaces the right nodes
    TYPE_KEYWORDS = {
        "H": "hypothesis cause exposure",
        "M": "mechanism pathway",
        "I": "intervention treatment",
        "P": "phenotype",
        "G": "gene variant",
        "B": "biomarker marker individual analyte",
        "C": "combination protocol stack",
        "T": "test panel diagnostic order labwork bloodwork saliva urine stool genetic",
    }
    search_parts.append(TYPE_KEYWORDS.get(ntype, ""))
    n = {
        "id": nid,
        "t":  ntype,
        "l":  (label or "")[:80],
        "ll": " ".join(search_parts),    # for free-text search (richer index)
        "s":  round(size, 3),
        "m":  0,                          # profile membership bitmask
    }
    n.update(extra)
    nodes.append(n)
    nodes_by_type[ntype].append(n)

for h in sorted(hyps, key=lambda r: r["id"]):
    conf = f(h.get("confidence_score", "0.5"))
    add_node(h["id"], "H", h.get("name") or h["id"], 4 + conf * 8)

mec_edge_count: dict[str, int] = {}
for e in he:
    mec_edge_count[e["mechanism_id"]] = mec_edge_count.get(e["mechanism_id"], 0) + 1
max_mec_edges = max(mec_edge_count.values()) if mec_edge_count else 1
for m in sorted(mecs, key=lambda r: r["id"]):
    centrality = mec_edge_count.get(m["id"], 0) / max_mec_edges
    add_node(m["id"], "M", m.get("name") or m["id"], 5 + centrality * 7)

# Build best-test lookup per phenotype from tests_catalog.csv.
# For each phenotype, pick the lowest-cost direct-to-consumer-friendly
# Tier 1 or Tier 2 test that maps to it. This is what mom should order.
best_test_for_phe: dict[str, dict] = {}
for t in tests:
    phe_field = t.get("maps_to_phenotype_ids", "") or ""
    if not phe_field:
        continue
    # Phenotype IDs may be ; or , separated
    phe_ids = [x.strip() for x in phe_field.replace(";", ",").split(",") if x.strip()]
    # Skip emerging / contested for the top recommendation; we want a
    # confident first-line test, not a frontier suggestion
    tier = (t.get("evidence_tier") or "").lower()
    if "tier3" in tier or "tier4" in tier or "tier5" in tier:
        continue
    for pid in phe_ids:
        # Pick lowest-cost test (proxy for accessibility)
        try:
            cost = float(t.get("cost_usd_low") or 9999)
        except ValueError:
            cost = 9999
        if pid not in best_test_for_phe or cost < best_test_for_phe[pid].get("_cost", 9999):
            best_test_for_phe[pid] = {
                "name": t.get("test_name", ""),
                "provider": t.get("provider", ""),
                "sample": t.get("sample_type", ""),
                "cost_lo": t.get("cost_usd_low", ""),
                "cost_hi": t.get("cost_usd_high", ""),
                "turnaround": t.get("turnaround_days", ""),
                "dtc": (t.get("direct_to_consumer", "") or "").upper() == "TRUE",
                "rx_required": (t.get("clinician_required", "") or "").upper() == "TRUE",
                "tier": t.get("evidence_tier", ""),
                "_cost": cost,
            }

for p in sorted(phes, key=lambda r: r["id"]):
    extra = {
        "pe": PHENOTYPE_PLAIN_ENGLISH.get(p["id"], ""),
        "av": PHENOTYPE_AVOID.get(p["id"], ""),
        "tk": PHENOTYPE_TRACK.get(p["id"], ""),
    }
    bt = best_test_for_phe.get(p["id"])
    if bt:
        extra["bt"] = {
            "name": bt["name"], "provider": bt["provider"],
            "sample": bt["sample"],
            "lo": bt["cost_lo"], "hi": bt["cost_hi"],
            "td": bt["turnaround"],
            "dtc": bt["dtc"], "rx": bt["rx_required"],
        }
    add_node(p["id"], "P", p.get("name") or p["id"], 13, extra=extra)

def int_size(row):
    for k in ("csrs_score", "csrs", "score"):
        if k in row and row[k]:
            return f(row[k]) / 100.0
    return f(row.get("confidence_score", "0.4"))
ints_sorted = sorted(ints_, key=lambda r: -int_size(r))[:CAP_INTERVENTIONS]
for i in sorted(ints_sorted, key=lambda r: r["id"]):
    cat = (i.get("category") or "").lower().strip()
    name_l = (i.get("name") or "").lower()
    # Override category with "peptide" if the intervention is a peptide
    # (matched by name) — peptides are the "next frontier" class, given
    # their own visual treatment downstream.
    if any(k in name_l for k in INTERVENTION_PEPTIDE_KEYWORDS):
        cat = "peptide"
    extra: dict = {
        "c": cat or "supplement",
        # FM-actionable card metadata
        "do": (i.get("dose_typical") or "")[:120],
        "co": (i.get("cost_estimate") or ""),
        "rg": (i.get("regulatory") or ""),  # rx | otc | rx_specialist
        "sf": (i.get("safety") or ""),       # yes | uncertain | monitored | no
        "sc": (i.get("csrs_score") or ""),   # atlas signal
    }
    if i["id"] == "INT-0001":
        extra["k"] = "INT-0001"
    add_node(i["id"], "I", i.get("name") or i["id"], 3 + int_size(i) * 8,
             extra=extra)

def gene_priority(row):
    for k in ("sfari_score", "tier", "confidence_score"):
        if k in row and row[k]:
            try: return -float(row[k])
            except: pass
    return 0
genes_sorted = sorted(genes, key=gene_priority)[:CAP_GENES]
for g in sorted(genes_sorted, key=lambda r: r.get("id", r.get("symbol", ""))):
    gid = g.get("id") or g.get("symbol") or ""
    add_node(gid, "G", g.get("symbol") or g.get("name") or gid, 1.6)

# ── edges ──────────────────────────────────────────────────────────────
links: list[dict] = []
def add_link(src, tgt, w, kind):
    if src in node_ids and tgt in node_ids:
        links.append({"s": src, "t": tgt, "w": round(w, 3), "k": kind})

for e in he:
    add_link(e["hypothesis_id"], e["mechanism_id"],
             f(e.get("evidence_strength_aggregate", "0.5")), "hm")
for e in hh:
    s = e.get("hypothesis_a_id") or e.get("source_id", "")
    t = e.get("hypothesis_b_id") or e.get("target_id", "")
    add_link(s, t, f(e.get("evidence_strength_aggregate",
                          e.get("weight", "0.5"))), "hh")
for e in im_:
    add_link(e["intervention_id"], e["mechanism_id"],
             f(e.get("evidence_strength_aggregate", "0.5")), "im")
for e in ih:
    add_link(e["intervention_id"], e["hypothesis_id"],
             f(e.get("evidence_strength_aggregate", "0.5")), "ih")
for e in ip_:
    add_link(e["intervention_id"], e["phenotype_id"],
             f(e.get("evidence_strength_aggregate", "0.5")), "ip")
for e in mp:
    add_link(e["mechanism_id"], e["phenotype_id"],
             f(e.get("evidence_strength_aggregate", "0.5")), "mp")
gh_sorted = sorted(gh, key=lambda r: -f(r.get("evidence_strength_aggregate", "0.5")))[:CAP_GENE_EDGES]
for e in gh_sorted:
    gid = e.get("gene_id") or e.get("gene_symbol")
    add_link(gid, e["hypothesis_id"],
             f(e.get("evidence_strength_aggregate", "0.5")), "gh")
for e in gm:
    gid = e.get("gene_id") or e.get("gene_symbol")
    add_link(gid, e["mechanism_id"],
             f(e.get("evidence_strength_aggregate", "0.5")), "gm")

# ── biomarkers (top-N by edge degree) ──────────────────────────────────
# "what to test" layer. Rank by total edge count across all biomarker_*
# tables, take top N so the graph stays legible.
bio_deg: dict[str, int] = {}
for e in bie:
    bio_deg[e["biomarker_id"]] = bio_deg.get(e["biomarker_id"], 0) + 1
for e in bme:
    bio_deg[e["biomarker_id"]] = bio_deg.get(e["biomarker_id"], 0) + 1
for e in bpe:
    bio_deg[e["biomarker_id"]] = bio_deg.get(e["biomarker_id"], 0) + 1
for e in bhe:
    bio_deg[e["biomarker_id"]] = bio_deg.get(e["biomarker_id"], 0) + 1
bios_sorted = sorted(bios, key=lambda r: -bio_deg.get(r["id"], 0))[:CAP_BIOMARKERS]
max_bio_deg = max(bio_deg.values()) if bio_deg else 1
for b in sorted(bios_sorted, key=lambda r: r["id"]):
    centrality = bio_deg.get(b["id"], 0) / max_bio_deg
    extra = {
        # FM-actionable card metadata
        "wt": (b.get("what_it_measures") or "")[:140],
        "em": (b.get("elevated_means") or "")[:160],
        "la": (b.get("lab_options") or "")[:120],
        "cl": (b.get("test_cost_usd_low") or ""),
        "ch": (b.get("test_cost_usd_high") or ""),
        "td": (b.get("turnaround_days") or ""),
        "st": (b.get("sample_type") or ""),
    }
    add_node(b["id"], "B", b.get("name") or b["id"], 2 + centrality * 5,
             extra=extra)

# biomarker edges (only to nodes already in the graph)
for e in bie:
    add_link(e["biomarker_id"], e["intervention_id"],
             f(e.get("evidence_strength", "0.5")), "bi")
for e in bme:
    add_link(e["biomarker_id"], e["mechanism_id"],
             f(e.get("evidence_strength", "0.5")), "bm")
for e in bpe:
    add_link(e["biomarker_id"], e["phenotype_id"],
             f(e.get("evidence_strength", "0.5")), "bp")
for e in bhe:
    add_link(e["biomarker_id"], e["hypothesis_id"],
             f(e.get("evidence_strength", "0.5")), "bh")

# ── combinations (typed protocol stacks) ───────────────────────────────
# Each combination is a node; its member interventions connect to it.
for c in sorted(combs, key=lambda r: r["id"])[:CAP_COMBINATIONS]:
    csrs = f(c.get("csrs_score") or c.get("csrs_treatment_score", "0.5"))
    size = 4 + (csrs / 100.0 if csrs > 1 else csrs) * 6
    add_node(c["id"], "C", c.get("name") or c["id"], size)

for m in cmms:
    add_link(m["combination_id"], m["intervention_id"], 0.7, "ci")

# ── tests (FM-actionable diagnostic panels) ────────────────────────────
# Render the top tests from tests_catalog.csv as TEAL T-nodes so the
# "what to test" surface is VISIBLE in the graph, not just in the action
# card. Ranking: Tier 1 > Tier 2; DTC-friendly first; lowest cost first
# within tier. This is the retention surface — the more obviously mom
# can find her actionable next step, the more she comes back.
def test_priority(t):
    tier_raw = (t.get("evidence_tier") or "").lower()
    if "tier1" in tier_raw:   tier_score = 4
    elif "tier2" in tier_raw: tier_score = 3
    elif "tier3" in tier_raw: tier_score = 1
    elif "tier4" in tier_raw: tier_score = 0.5
    else:                       tier_score = 2
    dtc = 1 if (t.get("direct_to_consumer") or "").upper() == "TRUE" else 0
    try:
        cost = float(t.get("cost_usd_low") or 9999)
    except ValueError:
        cost = 9999
    return (tier_score, dtc, -cost)

tests_sorted = sorted(tests, key=test_priority, reverse=True)[:CAP_TESTS]
for t in sorted(tests_sorted, key=lambda r: r.get("test_id", "")):
    tid = t.get("test_id", "")
    if not tid:
        continue
    tier_raw = (t.get("evidence_tier") or "").lower()
    size = 3.5 if "tier1" in tier_raw else 2.8 if "tier2" in tier_raw else 2.2
    add_node(tid, "T", t.get("test_name", "") or tid, size, extra={
        "pr": (t.get("provider", "") or "")[:48],
        "sm": (t.get("sample_type", "") or "")[:20],
        "cl": t.get("cost_usd_low", ""),
        "ch": t.get("cost_usd_high", ""),
        "td": t.get("turnaround_days", ""),
        "tr": (t.get("evidence_tier") or "").replace("Tier", "T").strip()[:5],
        "dtc": (t.get("direct_to_consumer", "") or "").upper() == "TRUE",
        "rx": (t.get("clinician_required", "") or "").upper() == "TRUE",
        "wm": (t.get("what_it_measures", "") or "")[:140],
        "uc": (t.get("specific_use_cases", "") or "")[:120],
    })

# Test → phenotype, test → biomarker, test → mechanism edges
def split_ids(s):
    if not s:
        return []
    return [x.strip() for x in s.replace(";", ",").split(",") if x.strip()]

for t in tests_sorted:
    tid = t.get("test_id", "")
    if not tid:
        continue
    for pid in split_ids(t.get("maps_to_phenotype_ids", "")):
        add_link(tid, pid, 0.7, "tp")
    for bid in split_ids(t.get("maps_to_biomarker_ids", "")):
        add_link(tid, bid, 0.6, "tb")
    for mid in split_ids(t.get("maps_to_mechanism_ids", "")):
        add_link(tid, mid, 0.5, "tm")

# adjacency for 1-hop profile expansion
adj: dict[str, set[str]] = {}
for l in links:
    adj.setdefault(l["s"], set()).add(l["t"])
    adj.setdefault(l["t"], set()).add(l["s"])

# ── compute per-profile masks ──────────────────────────────────────────
profile_info = [{"k": k, "label": label} for k, label, _ in PROFILES]
for bit, (key, _label, kw_by_type) in enumerate(PROFILES):
    seed: set[str] = set()
    for ntype, kws in kw_by_type.items():
        if not kws: continue
        for n in nodes_by_type[ntype]:
            if any(k in n["ll"] for k in kws):
                seed.add(n["id"])
    # one-hop expansion (twice — pulls phenotypes through interventions)
    for _ in range(2):
        new_ = set()
        for nid in list(seed):
            new_ |= adj.get(nid, set())
        seed |= new_
    for n in nodes:
        if n["id"] in seed:
            n["m"] |= (1 << bit)

# strip search-helper field after profile assignment? keep ll for free-text
# (it's already lowercase; modest size overhead but useful)

# ── stats ──────────────────────────────────────────────────────────────
stats = {
    "n_nodes": len(nodes),
    "n_links": len(links),
    "n_hyp": sum(1 for n in nodes if n["t"] == "H"),
    "n_mec": sum(1 for n in nodes if n["t"] == "M"),
    "n_int": sum(1 for n in nodes if n["t"] == "I"),
    "n_phe": sum(1 for n in nodes if n["t"] == "P"),
    "n_gen": sum(1 for n in nodes if n["t"] == "G"),
    "n_bio": sum(1 for n in nodes if n["t"] == "B"),
    "n_com": sum(1 for n in nodes if n["t"] == "C"),
    "n_test": sum(1 for n in nodes if n["t"] == "T"),
    "profiles": {p["k"]: sum(1 for n in nodes if n["m"] & (1<<i))
                 for i, p in enumerate(profile_info)},
}
print(json.dumps(stats, indent=2), file=sys.stderr)

# ── live intake feed (read by JS for the "X new in last Yh" ticker) ────
# The PubMed intake scanner writes vault/Discoveries_Inbox/.pubmed_last_run.json
# on every successful run + pubmed_intake_<YYYY-MM-DD>.json with the candidate
# list. The living graph reads these to display real liveness, not theatre.
intake = {"last_run": None, "latest_count": 0, "by_tag": {}}
inbox_dir = _REPO / "vault" / "Discoveries_Inbox"
last_run_file = inbox_dir / ".pubmed_last_run.json"
if last_run_file.exists():
    try:
        intake["last_run"] = json.loads(last_run_file.read_text()).get("last_run")
    except Exception:
        pass

# pick the most recent pubmed_intake_*.json
intake_jsons = sorted(inbox_dir.glob("pubmed_intake_*.json"),
                      reverse=True) if inbox_dir.exists() else []
if intake_jsons:
    try:
        latest = json.loads(intake_jsons[0].read_text())
        intake["latest_count"] = latest.get("candidates_total", 0)
        intake["by_tag"] = latest.get("candidates_by_tag", {})
        intake["scan_date"] = latest.get("scan_date")
    except Exception:
        pass

# ── HTML template ──────────────────────────────────────────────────────
HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Causes Atlas — Living Map</title>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<style>
  :root {
    --void:    #050810;
    --node:    #f0ebdc;
    --gold:    #e8c46e;
    --gold-dim:#7a6230;
    --cool:    #b4c8e8;
    --warm:    #d8b894;
    --gene:    #7a7770;
    --text:    #d8d2c4;
    --text-mute:#5a574e;
    --text-vmute:#33312c;
    --line:    #1a1d24;
    --line-hi: #2e3540;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body { width:100%; height:100%; overflow:hidden;
               background: var(--void); color: var(--text);
               font-family: ui-serif, "Iowan Old Style", "Apple Garamond",
                            Garamond, "Times New Roman", serif;
               font-weight: 400; letter-spacing: 0.01em;
               -webkit-font-smoothing: antialiased; }
  canvas { display: block; position: absolute; inset: 0;
           width: 100%; height: 100%; cursor: crosshair; }

  /* error overlay — only shown if something throws */
  .err { position: fixed; top: 50%; left: 50%;
         transform: translate(-50%, -50%); z-index: 100;
         max-width: 70vw; padding: 18px 22px;
         background: rgba(20,8,8,0.92); border: 1px solid #6e2222;
         color: #f0b4a0; font-family: ui-monospace, monospace;
         font-size: 12px; line-height: 1.5; white-space: pre-wrap;
         display: none; }
  .err.on { display: block; }

  /* ── manifesto ghost text — sits behind the graph ──────────────── */
  .manifesto {
    position: fixed; inset: 0; display: flex; align-items: center;
    justify-content: center; pointer-events: none; user-select: none;
    z-index: 0;
  }
  .manifesto-inner {
    font-family: ui-serif, "Iowan Old Style", Garamond, serif;
    font-weight: 400; font-size: clamp(48px, 9vw, 156px);
    line-height: 0.96; letter-spacing: -0.02em;
    color: #1a1d22; text-align: center;
    text-transform: uppercase;
    opacity: 0; transition: opacity 2400ms ease 800ms;
  }
  .manifesto-inner.ready { opacity: 1; }
  .manifesto-inner em { font-style: italic; color: #2a1f12; }

  /* ── corner chrome ─────────────────────────────────────────────── */
  .overlay { position: fixed; pointer-events: none;
             font-size: 10.5px; letter-spacing: 0.22em;
             text-transform: uppercase; color: var(--text-mute);
             user-select: none; z-index: 5; mix-blend-mode: screen; }
  .tl { top: 26px; left: 30px; }
  .tr { top: 26px; right: 30px; text-align: right; }
  .bl { bottom: 28px; left: 30px; }
  .title { font-size: 13px; letter-spacing: 0.34em; color: var(--text); }
  .num   { color: var(--text); font-variant-numeric: tabular-nums; }
  .dim   { color: var(--text-mute); }
  .vmute { color: var(--text-vmute); }
  .gold  { color: var(--gold); }

  /* pulsing dot next to "INGESTING" — sells the live loop */
  .ingest-dot {
    display: inline-block; width: 6px; height: 6px;
    border-radius: 50%; background: var(--gold);
    box-shadow: 0 0 8px var(--gold);
    margin-right: 8px; vertical-align: middle;
    animation: ingest-pulse 1.8s ease-in-out infinite;
  }
  @keyframes ingest-pulse {
    0%, 100% { opacity: 0.35; transform: scale(0.85); }
    50%      { opacity: 1.0;  transform: scale(1.15); }
  }

  /* ── profile dock — bottom right, opens upward ─────────────────── */
  .dock { position: fixed; bottom: 26px; right: 30px;
          z-index: 10; pointer-events: auto;
          display: flex; flex-direction: column; align-items: flex-end;
          gap: 8px; }
  .dock .input {
    width: clamp(260px, 30vw, 420px);
    background: rgba(8,11,18,0.6); backdrop-filter: blur(8px);
    border: 1px solid var(--line); color: var(--text);
    font: inherit; font-size: 13px; letter-spacing: 0.04em;
    padding: 11px 14px; outline: none;
    transition: border-color 400ms, background 400ms;
  }
  .dock .input::placeholder {
    color: var(--text-mute); font-style: italic;
    letter-spacing: 0.06em;
  }
  .dock .input:focus { border-color: var(--gold-dim);
                       background: rgba(12,14,22,0.75); }

  .dock .presets {
    display: flex; flex-direction: column; gap: 0;
    background: rgba(8,11,18,0.6); backdrop-filter: blur(8px);
    border: 1px solid var(--line); max-width: 420px;
    max-height: 0; overflow: hidden;
    transition: max-height 520ms ease;
  }
  .dock.open .presets { max-height: 360px; }
  .dock .preset {
    background: transparent; border: none; border-bottom: 1px solid var(--line);
    color: var(--text-mute); font: inherit; font-size: 10.5px;
    letter-spacing: 0.18em; text-transform: uppercase;
    padding: 10px 14px; cursor: pointer; text-align: right;
    transition: color 300ms, background 300ms;
  }
  .dock .preset:last-child { border-bottom: none; }
  .dock .preset:hover { color: var(--text); background: rgba(255,255,255,0.02); }
  .dock .preset.on { color: var(--gold); }
  .dock .toggle {
    background: transparent; border: 1px solid var(--line);
    color: var(--text-mute); font: inherit; font-size: 10.5px;
    letter-spacing: 0.22em; text-transform: uppercase;
    padding: 11px 16px; cursor: pointer;
    transition: color 300ms, border-color 300ms;
  }
  .dock .toggle:hover { color: var(--text); border-color: var(--line-hi); }
  .dock .toggle.on   { color: var(--gold); border-color: var(--gold-dim); }

  /* ── ACTION CARD — FM-actionable phenotype reveal ──────────────── */
  /* Appears bottom-center when a phenotype is clicked. The substrate's
     value made visible: TEST · DO · AVOID · TRACK. Mom-language. */
  .action-card {
    position: fixed; bottom: 28px; left: 50%; transform: translateX(-50%);
    z-index: 12; pointer-events: auto;
    width: clamp(640px, 70vw, 880px);
    background: rgba(8, 11, 18, 0.92); backdrop-filter: blur(12px);
    border: 1px solid var(--gold-dim);
    color: var(--text);
    font-family: ui-serif, "Iowan Old Style", Garamond, serif;
    opacity: 0; transform: translateX(-50%) translateY(20px);
    transition: opacity 600ms ease, transform 600ms ease;
    padding: 22px 28px 24px;
  }
  .action-card.on {
    opacity: 1; transform: translateX(-50%) translateY(0);
  }
  .action-card .ac-head {
    display: flex; justify-content: space-between; align-items: baseline;
    border-bottom: 1px solid var(--line-hi);
    padding-bottom: 9px; margin-bottom: 14px;
  }
  .action-card .ac-name {
    font-size: 18px; letter-spacing: 0.02em; color: var(--node);
  }
  .action-card .ac-id {
    font-family: ui-monospace, monospace; font-size: 10px;
    letter-spacing: 0.22em; color: var(--text-mute);
    text-transform: uppercase;
  }
  .action-card .ac-pe {
    font-style: italic; font-size: 13.5px; color: var(--text);
    line-height: 1.45; margin-bottom: 16px;
    max-width: 560px;
  }
  .action-card .ac-row {
    display: grid; grid-template-columns: 88px 1fr;
    gap: 14px; padding: 10px 0;
    border-bottom: 1px solid var(--line);
    font-size: 12.5px; line-height: 1.5;
  }
  .action-card .ac-row:last-child { border-bottom: none; }
  .action-card .ac-label {
    font-family: ui-monospace, monospace; font-size: 9.5px;
    letter-spacing: 0.24em; color: var(--gold);
    text-transform: uppercase; padding-top: 2px;
  }
  .action-card .ac-content { color: var(--text); }
  .action-card .ac-content .meta {
    color: var(--text-mute); font-size: 11px;
    margin-left: 6px;
  }
  .action-card .ac-content .pill {
    display: inline-block; padding: 1px 6px;
    border: 1px solid var(--line-hi); border-radius: 3px;
    font-family: ui-monospace, monospace; font-size: 9.5px;
    letter-spacing: 0.18em; text-transform: uppercase;
    color: var(--text-mute); margin-left: 4px;
  }
  .action-card .ac-content .pill.gold { color: var(--gold); border-color: var(--gold-dim); }
  .action-card .ac-content .item {
    margin-bottom: 6px;
  }
  .action-card .ac-content .item:last-child { margin-bottom: 0; }
  .action-card .ac-close {
    position: absolute; top: 12px; right: 16px;
    background: transparent; border: none;
    color: var(--text-mute); font-size: 18px;
    cursor: pointer; padding: 4px 8px;
    line-height: 1;
  }
  .action-card .ac-close:hover { color: var(--text); }
  .action-card .ac-footer {
    margin-top: 14px; padding-top: 10px;
    border-top: 1px solid var(--line);
    font-size: 10.5px; letter-spacing: 0.14em;
    color: var(--text-vmute); text-transform: uppercase;
  }

  /* ── hover label ───────────────────────────────────────────────── */
  .hover-label {
    position: fixed; pointer-events: none; z-index: 8;
    font-family: ui-serif, Garamond, serif; font-size: 12px;
    color: rgba(240,235,220,0.92); letter-spacing: 0.02em;
    text-shadow: 0 0 8px rgba(0,0,0,0.9);
    opacity: 0; transition: opacity 220ms;
    white-space: nowrap;
  }
  .hover-label .meta {
    display: block; font-size: 9.5px; letter-spacing: 0.22em;
    color: var(--text-mute); text-transform: uppercase;
    margin-top: 3px;
  }
</style>
</head>
<body>

<!-- ghost manifesto behind the graph -->
<div class="manifesto">
  <div class="manifesto-inner">
    Population&nbsp;average<br>
    <em>is&nbsp;not</em><br>
    your&nbsp;child
  </div>
</div>

<canvas id="c"></canvas>

<div class="overlay tl">
  <div class="title">Causes Atlas</div>
  <div class="vmute" style="margin-top:5px;">Autism · v2.0 · reproducible</div>
  <div style="margin-top:14px;">
    <span class="ingest-dot"></span>
    <span class="vmute" style="letter-spacing:0.26em;">ingesting</span>
    <span class="num" id="papers" style="margin-left:10px;">__N_PAPERS__</span>
    <span class="vmute" style="margin-left:5px;">papers</span>
  </div>
  <div class="vmute" style="margin-top:4px;">
    last evidence
    <span id="last-ingest" class="num" style="margin-left:6px;">just now</span>
  </div>
</div>

<div class="overlay tr">
  <div class="num">__N_NODES__ nodes · __N_LINKS__ edges</div>
  <div class="vmute" style="margin-top:5px;">
    __N_HYP__ hyp · __N_MEC__ mec · __N_INT__ int · __N_PHE__ phe ·
    __N_BIO__ bio · __N_COM__ com · __N_TEST__ test · __N_GEN__ gen
  </div>
  <div class="vmute" style="margin-top:8px;">n=7 mae 0.049 · 4 sub-3% errors</div>
  <div class="vmute" style="margin-top:8px;">
    intake feed · <span id="intake-ticker">__INTAKE_TICKER__</span>
  </div>
</div>

<div class="overlay bl">
  <div class="vmute">int-0001 leucovorin csrs</div>
  <div class="gold num" style="font-size:14px;letter-spacing:0.16em;margin-top:3px;">83.35</div>
</div>

<div id="dock" class="dock">
  <div class="presets" id="presets"></div>
  <input class="input" id="search" type="text" autocomplete="off"
         spellcheck="false" placeholder="describe your child · a gene · a symptom" />
  <button class="toggle" id="toggle">load susceptibility profile</button>
</div>

<div class="hover-label" id="hover"></div>

<!-- FM-actionable card: bottom-center reveal on phenotype-click -->
<div class="action-card" id="ac"></div>

<div class="err" id="err"></div>
<script src="https://cdn.jsdelivr.net/npm/d3@7/dist/d3.min.js"
        crossorigin="anonymous"></script>
<script>
window.addEventListener('error', (e) => {
  const el = document.getElementById('err');
  el.textContent = '⚠ ' + (e.message || e.error || 'script error') +
                   '\n' + (e.filename || '') + ':' + (e.lineno || '');
  el.classList.add('on');
});
</script>
<script>
'use strict';

const DATA     = __DATA__;
const PROFILES = __PROFILES__;        // [{k, label}, ...] index = bit
const INTAKE   = __INTAKE_FEED__;     // recent PubMed candidates from cron

// ── canvas + DPR ───────────────────────────────────────────────────
const canvas = document.getElementById('c');
const ctx = canvas.getContext('2d');
let W = 0, H = 0, DPR = 1;
function resize() {
  DPR = window.devicePixelRatio || 1;
  W = window.innerWidth;
  H = window.innerHeight;
  canvas.style.width  = W + 'px';
  canvas.style.height = H + 'px';
  canvas.width  = Math.round(W * DPR);
  canvas.height = Math.round(H * DPR);
  ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
}
window.addEventListener('resize', resize); resize();

// ── color per type ─────────────────────────────────────────────────
// Off-white base palette with sparing color encoding. Restraint: every
// node lives in the same warm-grey spectrum; only category and centrality
// shift the hue. Cathedral palette, not consumer dashboard.
const TYPE_COLOR = {
  H: [240, 235, 220],   // hypotheses — bone-white
  M: [180, 200, 232],   // mechanisms — cool blue
  I: [232, 196, 110],   // interventions — warm gold (default)
  P: [216, 184, 148],   // phenotypes — warm tan, the destination
  G: [122, 119, 112],   // genes — deep grey, the substrate
  B: [165, 195, 200],   // biomarkers — pale cyan, individual markers
  C: [255, 215, 130],   // combinations — saturated gold, the typed stack
  T: [120, 220, 200],   // tests — vivid teal, the FM-actionable layer
};

// Intervention sub-category hue shifts (within the warm-gold spectrum,
// except peptides which get a distinct cool tint to read as "frontier").
// Applied only when a node's t === 'I' and a `c` field is present.
const INT_CATEGORY_COLOR = {
  drug:         [232, 196, 110],  // default gold
  supplement:   [240, 210, 145],  // softer cream-gold
  herb:         [200, 180, 110],  // muted olive-gold
  food:         [220, 200, 155],  // wheat
  lifestyle:    [205, 195, 165],  // pale parchment
  environmental:[185, 175, 150],  // dusk
  combo:        [255, 215, 130],  // bright gold (parent combos look like C)
  peptide:      [200, 220, 235],  // cool pale blue — the frontier
  endogenous:   [235, 215, 175],  // honey
};

// ── d3 check ───────────────────────────────────────────────────────
if (typeof d3 === 'undefined' || !d3.forceSimulation) {
  const el = document.getElementById('err');
  el.textContent = '⚠ d3 failed to load from CDN.\n' +
    'If you are on file://, your browser may be blocking the script.\n' +
    'Try: open Chrome DevTools → Console; or serve this file via a local HTTP server.';
  el.classList.add('on');
  throw new Error('d3 missing');
}

// ── prepare graph ──────────────────────────────────────────────────
// Pre-position nodes in a phyllotaxis spiral so the graph is visible
// from frame 1 — d3-force then relaxes it into its natural shape.
const PHI = Math.PI * (3 - Math.sqrt(5));
const nodes = DATA.nodes.map((n, i) => {
  const r = 10 * Math.sqrt(i + 1);
  const a = i * PHI;
  return { ...n, x: r * Math.cos(a), y: r * Math.sin(a), vx: 0, vy: 0 };
});
const idIdx = new Map(nodes.map(n => [n.id, n]));
const links = DATA.links
  .filter(l => idIdx.has(l.s) && idIdx.has(l.t))
  .map(l => ({ source: l.s, target: l.t, w: l.w, k: l.k }));

function chargeStrength(n) {
  if (n.t === 'P') return -1800;
  if (n.t === 'C') return -700;   // combinations — gravitate apart, they're protocols
  if (n.t === 'H') return -520;
  if (n.t === 'M') return -440;
  if (n.t === 'I') return -240;
  if (n.t === 'B') return -180;   // biomarkers — tighter cluster around their phenotype
  if (n.t === 'T') return -260;   // tests — slightly looser than biomarkers
  return -55;
}
function linkDistance(l) {
  const k = l.k;
  if (k === 'mp' || k === 'ip' || k === 'bp' || k === 'tp') return 80;
  if (k === 'hm' || k === 'im' || k === 'ih') return 56;
  if (k === 'bi' || k === 'bm' || k === 'bh') return 44;
  if (k === 'tb' || k === 'tm') return 52;  // test → biomarker / mechanism
  if (k === 'ci') return 38;
  if (k === 'hh') return 92;
  return 28;
}

const sim = d3.forceSimulation(nodes)
  .force('charge',  d3.forceManyBody().strength(chargeStrength).distanceMax(440))
  .force('link',    d3.forceLink(links).id(d => d.id)
                      .distance(linkDistance)
                      .strength(l => 0.15 + l.w * 0.4))
  .force('center',  d3.forceCenter(0, 0))
  .force('collide', d3.forceCollide().radius(d => d.s + 1.6).strength(0.85))
  .alpha(1).alphaDecay(0.012).velocityDecay(0.55)
  .on('tick', () => {});

// ── view (pan + zoom) ──────────────────────────────────────────────
let scale = 1.0, ox = 0, oy = 0;
let targetScale = 1.0, targetOx = 0, targetOy = 0;
let dragStart = null;
canvas.addEventListener('wheel', (e) => {
  e.preventDefault();
  const k = Math.exp(-e.deltaY * 0.0015);
  targetScale = Math.max(0.3, Math.min(4, targetScale * k));
  lastUserAction = performance.now();
}, { passive: false });
canvas.addEventListener('mousedown', (e) => {
  dragStart = { x: e.clientX, y: e.clientY, ox: targetOx, oy: targetOy };
  lastUserAction = performance.now();
});
window.addEventListener('mousemove', (e) => {
  if (dragStart) {
    targetOx = dragStart.ox + (e.clientX - dragStart.x);
    targetOy = dragStart.oy + (e.clientY - dragStart.y);
  }
});
window.addEventListener('mouseup', () => dragStart = null);

// ── profile + search state ─────────────────────────────────────────
let activeBit = -1;             // -1 = no profile
let searchTerm = '';
let searchHits = new Set();     // ids matching search
let activeMask = null;          // function(node) -> boolean
let isFiltering = false;

function recomputeFilter() {
  if (revealedPhenotype) {
    isFiltering = true;
  } else if (searchTerm) {
    searchHits.clear();
    const tokens = searchTerm.toLowerCase().split(/\s+/).filter(Boolean);
    for (const n of nodes) {
      if (tokens.every(t => n.ll.indexOf(t) >= 0)) searchHits.add(n.id);
    }
    isFiltering = searchHits.size > 0;
  } else if (activeBit >= 0) {
    isFiltering = true;
  } else {
    isFiltering = false;
  }
}

function inActive(n) {
  // Phenotype-click reveal takes precedence: ONLY the phenotype + its
  // top-5 evidence-weighted interventions + top-3 stratifying biomarkers
  // remain lit. Everything else fades to ghost. This is the "what to do /
  // what to test" answer in visual form.
  if (revealedPhenotype) {
    return revealedSet.has(n.id);
  }
  if (searchTerm) {
    if (searchHits.has(n.id)) return true;
    // one-hop bridge: light up neighbors of matched nodes too
    for (const l of links) {
      if (l.source.id && (
          (l.source.id === n.id && searchHits.has(l.target.id)) ||
          (l.target.id === n.id && searchHits.has(l.source.id))
      )) return true;
    }
    return false;
  }
  if (activeBit >= 0) return !!(n.m & (1 << activeBit));
  return true;
}

// ── pulses ─────────────────────────────────────────────────────────
const pulses = [];
const particles = [];                  // flowing along edges
let lastUserAction = performance.now();
let autoFitDone = false;

function neighborsOf(node) {
  const out = [];
  for (const l of links) {
    if (l.source === node) out.push(l.target);
    else if (l.target === node) out.push(l.source);
  }
  return out;
}

function propagatePulse(node, depth) {
  if (depth > 1) return;
  const nbs = neighborsOf(node);
  // sample up to 4 neighbors for the propagation step
  const k = Math.min(4, nbs.length);
  for (let i = 0; i < k; i++) {
    const nb = nbs[(Math.random() * nbs.length) | 0];
    if (!nb || nb.x === undefined) continue;
    setTimeout(() => {
      pulses.push({ node: nb, t: 0, dur: 850 - depth*200 });
      if (depth === 0 && Math.random() < 0.45) propagatePulse(nb, depth + 1);
    }, 220 + Math.random() * 180);
  }
}

function spawnPulse() {
  const candidates = isFiltering
    ? nodes.filter(n => inActive(n) && n.t !== 'G')
    : nodes.filter(n => n.t !== 'G');
  if (!candidates.length) return;
  const n = candidates[(Math.random() * candidates.length) | 0];
  pulses.push({ node: n, t: 0, dur: 1200 });
  propagatePulse(n, 0);
}
setInterval(spawnPulse, 1900);

function spawnParticle() {
  if (!links.length) return;
  // prefer edges within active filter when filtering
  let pool = links;
  if (isFiltering) {
    pool = links.filter(l => l.source && l.target &&
                             inActive(l.source) && inActive(l.target));
    if (!pool.length) pool = links;
  }
  const l = pool[(Math.random() * pool.length) | 0];
  if (!l || !l.source || !l.target || l.source.x === undefined) return;
  particles.push({ link: l, t: 0, dur: 1300 + Math.random() * 900 });
}
setInterval(spawnParticle, 180);   // ~5/sec — visible flow without overload

// ── ingestion events ──────────────────────────────────────────────
// Periodic "new evidence" comets fly in from off-screen, land on a
// hypothesis/mechanism/intervention node, trigger a pulse + propagation.
// This is the visual signature of an always-processing system.
const ingestEvents = [];
let papersCount   = __PAPERS_BASE__;      // baseline; ticks up per ingestion
let lastIngestAgo = 0;                    // ms since last ingest
let ingestStartT  = performance.now();

function spawnIngestEvent() {
  const pool = isFiltering
    ? nodes.filter(n => inActive(n) && (n.t === 'H' || n.t === 'M' || n.t === 'I'))
    : nodes.filter(n => n.t === 'H' || n.t === 'M' || n.t === 'I');
  if (!pool.length) return;
  const target = pool[(Math.random() * pool.length) | 0];
  // entry point: a long way outside the current viewport, in world coords
  const angle  = Math.random() * Math.PI * 2;
  const dist   = (Math.max(W, H) / Math.max(0.25, scale)) * 0.65;
  const sx = target.x + Math.cos(angle) * dist;
  const sy = target.y + Math.sin(angle) * dist;
  ingestEvents.push({ target, sx, sy, t: 0, dur: 1700, landed: false });
  papersCount += 1;
  ingestStartT = performance.now();
}
setInterval(spawnIngestEvent, 5800);
// fire one shortly after load so the user sees it within ~3 seconds
setTimeout(spawnIngestEvent, 2800);

// ── hover ──────────────────────────────────────────────────────────
let hover = null;
const hoverEl = document.getElementById('hover');
canvas.addEventListener('mousemove', (e) => {
  if (dragStart) { hoverEl.style.opacity = 0; return; }
  const mx = (e.clientX - W/2 - ox) / scale;
  const my = (e.clientY - H/2 - oy) / scale;
  let best = null, bd = 15*15;
  for (const n of nodes) {
    const dx = n.x - mx, dy = n.y - my;
    const r = n.s + 4, d2 = dx*dx + dy*dy;
    if (d2 < r*r + 14 && d2 < bd) { bd = d2; best = n; }
  }
  hover = best;
  if (best && best.t !== 'G') {
    const typeLabel = ({
      H:'Hypothesis', M:'Mechanism', I:'Intervention',
      P:'Phenotype',  B:'Biomarker',
      C:'Combination · typed stack',
      T:'Test · order this',
    })[best.t] || '';
    // Sub-category hint for interventions (drug/supplement/peptide/etc.)
    const subCat = (best.t === 'I' && best.c)
      ? ' · ' + best.c.toUpperCase()
      : '';
    // Tests get richer hover detail — provider + cost + sample + turnaround
    let meta = best.id + ' · ' + typeLabel + subCat;
    if (best.t === 'T') {
      const bits = [];
      if (best.pr) bits.push(best.pr);
      if (best.sm) bits.push(best.sm);
      if (best.cl && best.ch) bits.push('$' + best.cl + '-' + best.ch);
      else if (best.cl) bits.push('$' + best.cl);
      if (best.td) bits.push(best.td + 'd');
      if (best.dtc) bits.push('DTC');
      else if (best.rx) bits.push('Rx');
      if (best.tr) bits.push(best.tr);
      if (bits.length) meta += '<br>' + bits.join(' · ');
    }
    hoverEl.innerHTML = best.l + '<span class="meta">' + meta + '</span>';
    hoverEl.style.left = (e.clientX + 14) + 'px';
    hoverEl.style.top  = (e.clientY + 14) + 'px';
    hoverEl.style.opacity = 1;
  } else {
    hoverEl.style.opacity = 0;
  }
});
canvas.addEventListener('mouseleave', () => {
  hover = null; hoverEl.style.opacity = 0;
});

// ── phenotype-click reveal: "what would help" + "what to test" ───────
// Click on a phenotype node → the top-5 atlas-signal-weighted interventions
// AND the top-3 biomarkers that stratify it become the only highlighted
// nodes (everything else fades). Particles flow from those interventions
// toward the phenotype. This is the "what to do / what to test" visual
// answer — the most actionable interaction in the cinematic surface.
let revealedPhenotype = null;
let revealedSet = new Set();
const acEl = document.getElementById('ac');

function fmtRange(lo, hi, prefix) {
  if (!lo && !hi) return '';
  prefix = prefix || '';
  if (lo && hi && lo !== hi) return prefix + lo + '–' + hi;
  return prefix + (lo || hi);
}

function rxBadge(rg) {
  if (!rg) return '';
  if (rg.indexOf('rx') === 0) return '<span class="pill">rx</span>';
  if (rg === 'otc')      return '<span class="pill">otc</span>';
  if (rg === 'lifestyle')return '<span class="pill">lifestyle</span>';
  return '<span class="pill">' + rg + '</span>';
}

function tierBadge(sc) {
  if (!sc) return '';
  const v = parseFloat(sc);
  if (isNaN(v)) return '';
  if (v >= 75) return '<span class="pill gold">strong evidence</span>';
  if (v >= 55) return '<span class="pill">moderate</span>';
  return '<span class="pill">emerging</span>';
}

function renderActionCard(phe, topBios, topInts, topTests) {
  if (!phe) { acEl.classList.remove('on'); return; }
  const pe = phe.pe || '';
  const av = phe.av || '';
  const tk = phe.tk || '';
  const bt = phe.bt;
  topTests = topTests || [];

  // TEST section: top-3 actual test panels (T nodes) — these are the
  // FM-actionable panels mom can order. If none mapped, fall back to the
  // best-test field on the phenotype + top biomarkers.
  let testHtml = '';
  if (topTests.length) {
    for (const t of topTests) {
      const dtcStr = t.dtc ? '<span class="pill gold">direct-to-consumer</span>' :
                     t.rx ? '<span class="pill">rx</span>' : '';
      const tierStr = t.tr ? '<span class="pill">' + t.tr + '</span>' : '';
      const provider = t.pr ? t.pr : '';
      const sample = t.sm ? ' · ' + t.sm : '';
      const cost = t.cl ? ' · $' + fmtRange(t.cl, t.ch) : '';
      const td = t.td ? ' · ' + t.td + 'd' : '';
      const wm = t.wm ? '<br><span class="meta" style="margin-left:0;">' + t.wm + '</span>' : '';
      testHtml += '<div class="item"><strong>' + t.l + '</strong>' +
                  dtcStr + tierStr +
                  '<span class="meta">' + provider + sample + cost + td + '</span>' +
                  wm + '</div>';
    }
  } else if (bt) {
    const rxStr = bt.rx ? '<span class="pill">rx</span>' :
                  (bt.dtc ? '<span class="pill gold">direct-to-consumer</span>' : '');
    testHtml += '<div class="item"><strong>' + bt.name + '</strong>' + rxStr +
                '<span class="meta">' + bt.provider +
                ' · ' + bt.sample +
                (bt.lo ? ' · $' + fmtRange(bt.lo, bt.hi) : '') +
                (bt.td ? ' · ' + bt.td + 'd' : '') + '</span></div>';
    for (const b of topBios.slice(0, 2)) {
      const wt = b.wt ? ' — ' + b.wt.substring(0, 80) : '';
      const lab = b.la ? ' <span class="meta">' + b.la.substring(0, 60) +
                  (b.cl ? ' · $' + fmtRange(b.cl, b.ch) : '') + '</span>' : '';
      testHtml += '<div class="item"><strong>' + b.l + '</strong>' +
                  wt + lab + '</div>';
    }
  }
  if (!testHtml) testHtml = '<div class="meta">No mapped tests in atlas yet — pending curation</div>';

  // DO section: top 3 interventions
  let doHtml = '';
  for (const i of topInts.slice(0, 3)) {
    const dose = i.do ? '<span class="meta">' + i.do + '</span>' : '';
    const cost = i.co ? '<span class="meta">$' + i.co + '/mo</span>' : '';
    const cat = i.c ? '<span class="pill">' + i.c + '</span>' : '';
    doHtml += '<div class="item"><strong>' + i.l + '</strong>' +
              rxBadge(i.rg) + cat + tierBadge(i.sc) +
              (dose ? ' ' + dose : '') +
              (cost ? ' ' + cost : '') + '</div>';
  }
  if (!doHtml) doHtml = '<div class="meta">No mapped interventions in atlas yet</div>';

  const html = '' +
    '<button class="ac-close" onclick="clearReveal();">×</button>' +
    '<div class="ac-head">' +
      '<div class="ac-name">' + phe.l + '</div>' +
      '<div class="ac-id">' + phe.id + ' · phenotype</div>' +
    '</div>' +
    (pe ? '<div class="ac-pe">"' + pe + '"</div>' : '') +
    '<div class="ac-row">' +
      '<div class="ac-label">Test</div>' +
      '<div class="ac-content">' + testHtml + '</div>' +
    '</div>' +
    '<div class="ac-row">' +
      '<div class="ac-label">Do</div>' +
      '<div class="ac-content">' + doHtml + '</div>' +
    '</div>' +
    (av ? '<div class="ac-row">' +
      '<div class="ac-label">Avoid</div>' +
      '<div class="ac-content">' + av + '</div>' +
    '</div>' : '') +
    (tk ? '<div class="ac-row">' +
      '<div class="ac-label">Track</div>' +
      '<div class="ac-content">' + tk + '</div>' +
    '</div>' : '') +
    '<div class="ac-footer">' +
      '<a href="TESTING_STRATEGY.md" target="_blank" ' +
      'style="color:var(--gold);text-decoration:none;letter-spacing:0.14em;">' +
      'full testing strategy →</a>' +
      ' &nbsp;·&nbsp; ' +
      'not medical advice. discuss with a functional / integrative ' +
      'pediatrics clinician before acting.' +
    '</div>';
  acEl.innerHTML = html;
  acEl.classList.add('on');
}

function revealForPhenotype(phe) {
  // Collect intervention, biomarker, AND test candidates connected to this phenotype
  const intCandidates = [];
  const bioCandidates = [];
  const testCandidates = [];
  for (const l of links) {
    if (l.target.id === phe.id) {
      if (l.source.t === 'I') intCandidates.push({n: l.source, w: l.w});
      if (l.source.t === 'B') bioCandidates.push({n: l.source, w: l.w});
      if (l.source.t === 'T') testCandidates.push({n: l.source, w: l.w});
    }
    if (l.source.id === phe.id) {
      if (l.target.t === 'I') intCandidates.push({n: l.target, w: l.w});
      if (l.target.t === 'B') bioCandidates.push({n: l.target, w: l.w});
      if (l.target.t === 'T') testCandidates.push({n: l.target, w: l.w});
    }
  }
  // Rank by atlas-signal-weight (link weight; falls back to node size
  // which encodes CSRS / centrality)
  intCandidates.sort((a, b) => (b.w * b.n.s) - (a.w * a.n.s));
  bioCandidates.sort((a, b) => (b.w * b.n.s) - (a.w * a.n.s));
  // Tests: prefer Tier 1 + DTC-friendly + low cost (encoded in node.s
  // already; tier-1 tests sized 3.5, tier-2 2.8, tier-3 2.2)
  testCandidates.sort((a, b) => {
    const ts = b.n.s - a.n.s;
    if (Math.abs(ts) > 0.1) return ts;
    // tiebreak by lower cost (test.cl)
    const aCost = parseFloat(a.n.cl) || 9999;
    const bCost = parseFloat(b.n.cl) || 9999;
    return aCost - bCost;
  });
  const topInts = intCandidates.slice(0, 5).map(c => c.n);
  const topBios = bioCandidates.slice(0, 3).map(c => c.n);
  const topTests = testCandidates.slice(0, 3).map(c => c.n);
  // Emergent 2-hop: walk through mechanisms to find indirect connections
  // when direct edges are sparse. Add up to 4 mechanism nodes that bridge
  // the phenotype to the top interventions/biomarkers.
  const emergent = new Set();
  if (topInts.length + topBios.length < 5) {
    for (const l of links) {
      const ph_is_target = l.target.id === phe.id;
      const ph_is_source = l.source.id === phe.id;
      if (ph_is_target && l.source.t === 'M') emergent.add(l.source.id);
      if (ph_is_source && l.target.t === 'M') emergent.add(l.target.id);
    }
  }
  revealedSet = new Set([phe.id,
                         ...topInts.map(n => n.id),
                         ...topBios.map(n => n.id),
                         ...topTests.map(n => n.id),
                         ...Array.from(emergent).slice(0, 4)]);
  revealedPhenotype = phe;
  // Spawn particles from each top intervention toward the phenotype
  for (const ints of topInts) {
    for (const l of links) {
      if ((l.source.id === ints.id && l.target.id === phe.id) ||
          (l.target.id === ints.id && l.source.id === phe.id)) {
        for (let k = 0; k < 3; k++) {
          particles.push({
            link: l,
            t: k * 0.3,
            speed: 0.18 + Math.random() * 0.1,
            rev: l.source.id === phe.id,
          });
        }
      }
    }
  }
  // Pulse the phenotype itself
  pulses.push({node: phe, t: 0, dur: 1.8});
  renderActionCard(phe, topBios, topInts, topTests);
}

function clearReveal() {
  revealedPhenotype = null;
  revealedSet = new Set();
  acEl.classList.remove('on');
}
window.clearReveal = clearReveal;

canvas.addEventListener('click', (e) => {
  // Bail if we're in the middle of a drag (don't conflate pan-end with click)
  if (dragStart && (Math.abs(e.clientX - dragStart.startX) > 4 ||
                    Math.abs(e.clientY - dragStart.startY) > 4)) {
    return;
  }
  const mx = (e.clientX - W/2 - ox) / scale;
  const my = (e.clientY - H/2 - oy) / scale;
  let best = null, bd = 18*18;
  for (const n of nodes) {
    const dx = n.x - mx, dy = n.y - my;
    const d2 = dx*dx + dy*dy;
    if (d2 < bd) { bd = d2; best = n; }
  }
  if (best && best.t === 'P') {
    if (revealedPhenotype && revealedPhenotype.id === best.id) {
      clearReveal();   // click same phenotype again to dismiss
    } else {
      revealForPhenotype(best);
    }
  } else if (!best) {
    clearReveal();   // click empty space to dismiss
  }
});

// ── dock interactions ──────────────────────────────────────────────
const dock      = document.getElementById('dock');
const presetsEl = document.getElementById('presets');
const toggle    = document.getElementById('toggle');
const search    = document.getElementById('search');

PROFILES.forEach((p, i) => {
  const b = document.createElement('button');
  b.className = 'preset';
  b.textContent = p.label;
  b.dataset.bit = i;
  b.addEventListener('click', () => selectProfile(i));
  presetsEl.appendChild(b);
});
const resetBtn = document.createElement('button');
resetBtn.className = 'preset';
resetBtn.textContent = '— reset —';
resetBtn.addEventListener('click', () => selectProfile(-1));
presetsEl.appendChild(resetBtn);

toggle.addEventListener('click', () => {
  dock.classList.toggle('open');
});

function selectProfile(bit) {
  activeBit = bit;
  searchTerm = ''; search.value = ''; searchHits.clear();
  recomputeFilter();
  // recenter on subgraph centroid
  if (bit >= 0) {
    // bounding box of subgraph
    let xmin=Infinity, xmax=-Infinity, ymin=Infinity, ymax=-Infinity, n=0;
    for (const node of nodes) if (node.m & (1 << bit)) {
      if (node.x < xmin) xmin = node.x;
      if (node.x > xmax) xmax = node.x;
      if (node.y < ymin) ymin = node.y;
      if (node.y > ymax) ymax = node.y;
      n++;
    }
    if (n > 0) {
      const gw = Math.max(60, xmax - xmin), gh = Math.max(60, ymax - ymin);
      const pad = 0.62;
      targetScale = Math.min((W*pad)/gw, (H*pad)/gh, 2.2);
      targetOx = -((xmin + xmax)/2) * targetScale;
      targetOy = -((ymin + ymax)/2) * targetScale;
    }
    toggle.classList.add('on');
    toggle.textContent = PROFILES[bit].label.toLowerCase();
  } else {
    autoFitDone = false;        // re-run autoFit on reset
    toggle.classList.remove('on');
    toggle.textContent = 'load susceptibility profile';
  }
  // close menu
  dock.classList.remove('open');
  // update preset visuals
  presetsEl.querySelectorAll('.preset').forEach((el, i) => {
    el.classList.toggle('on', i === bit);
  });
}

search.addEventListener('input', () => {
  searchTerm = search.value.trim();
  if (searchTerm) {
    activeBit = -1;
    toggle.classList.remove('on');
    toggle.textContent = 'searching · ' + searchTerm;
    presetsEl.querySelectorAll('.preset').forEach(el => el.classList.remove('on'));
  } else {
    toggle.textContent = 'load susceptibility profile';
  }
  recomputeFilter();
  // soft recenter on search centroid
  if (searchHits.size > 0) {
    let sx = 0, sy = 0, n = 0;
    for (const id of searchHits) {
      const node = idIdx.get(id);
      if (node) { sx += node.x; sy += node.y; n++; }
    }
    if (n > 0) { targetOx = -sx/n; targetOy = -sy/n; targetScale = 1.35; }
  } else if (!searchTerm) {
    targetOx = 0; targetOy = 0; targetScale = 1.0;
  }
});
search.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    search.value = ''; searchTerm = ''; searchHits.clear();
    recomputeFilter();
    toggle.textContent = 'load susceptibility profile';
    targetOx = 0; targetOy = 0; targetScale = 1.0;
  }
});
window.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    selectProfile(-1);
    search.value = ''; searchTerm = ''; searchHits.clear();
    recomputeFilter();
  }
});

// ── render loop ────────────────────────────────────────────────────
let last = performance.now();
let startTime = performance.now();

function autoFit() {
  let xmin = Infinity, xmax = -Infinity, ymin = Infinity, ymax = -Infinity;
  for (const n of nodes) {
    if (n.x < xmin) xmin = n.x;
    if (n.x > xmax) xmax = n.x;
    if (n.y < ymin) ymin = n.y;
    if (n.y > ymax) ymax = n.y;
  }
  const gw = xmax - xmin, gh = ymax - ymin;
  if (gw < 50 || gh < 50) return;
  const pad = 0.78;            // fill ~78% of viewport
  const sx = (W * pad) / gw;
  const sy = (H * pad) / gh;
  targetScale = Math.min(sx, sy, 1.3);
  targetOx = -((xmin + xmax) / 2) * targetScale;
  targetOy = -((ymin + ymax) / 2) * targetScale;
}

function draw(now) {
  const dt = now - last; last = now;

  // auto-fit once after the sim has had time to relax
  if (!autoFitDone && (now - startTime) > 1600) {
    autoFit();
    autoFitDone = true;
  }

  // camera drift — slow Ken Burns oscillation when idle
  const idleMs = now - lastUserAction;
  if (idleMs > 4000 && !dragStart) {
    const t = (now - startTime) * 0.00012;
    const drift = Math.min(1, (idleMs - 4000) / 1500);   // ease-in
    targetOx += Math.sin(t) * 0.18 * drift;
    targetOy += Math.cos(t * 0.73) * 0.14 * drift;
  }

  scale += (targetScale - scale) * 0.06;
  ox    += (targetOx    - ox)    * 0.06;
  oy    += (targetOy    - oy)    * 0.06;

  if (sim.alpha() < 0.06) sim.alpha(0.06);    // keep it breathing
  sim.tick();

  // motion-blur fill — gentle trail
  ctx.fillStyle = 'rgba(5,8,16,0.94)';
  ctx.fillRect(0, 0, W, H);

  ctx.save();
  ctx.translate(W/2 + ox, H/2 + oy);
  ctx.scale(scale, scale);

  // ── edges ──
  ctx.lineWidth = 0.7 / scale;
  for (const l of links) {
    const s = l.source, t = l.target;
    if (!s || !t || s.x === undefined) continue;
    const sa = inActive(s), ta = inActive(t);
    let alpha;
    if (isFiltering) {
      if (sa && ta)        alpha = 0.16 + l.w * 0.55;
      else if (sa || ta)   alpha = 0.04 + l.w * 0.06;
      else                 alpha = 0.012 + l.w * 0.03;
    } else {
      alpha = 0.04 + l.w * 0.32;
    }
    // edges inside filtered set are warm gold; outside are cool/dim white
    if (isFiltering && sa && ta) {
      ctx.strokeStyle = `rgba(232,196,110,${alpha})`;
    } else {
      ctx.strokeStyle = `rgba(240,235,220,${alpha})`;
    }
    ctx.beginPath();
    ctx.moveTo(s.x, s.y);
    ctx.lineTo(t.x, t.y);
    ctx.stroke();
  }

  // ── particles flowing along edges ──
  for (let i = particles.length - 1; i >= 0; i--) {
    const p = particles[i];
    p.t += dt;
    const k = p.t / p.dur;
    if (k >= 1) { particles.splice(i, 1); continue; }
    const s = p.link.source, t = p.link.target;
    if (!s || !t || s.x === undefined) continue;
    // ease-in-out for a natural flow
    const e = k < 0.5 ? 2*k*k : 1 - Math.pow(-2*k + 2, 2)/2;
    const px = s.x + (t.x - s.x) * e;
    const py = s.y + (t.y - s.y) * e;
    const headA = Math.sin(k * Math.PI) * 0.85;
    const sa = inActive(s), ta = inActive(t);
    const col = (isFiltering && sa && ta) ? [232,196,110]
              : (isFiltering && !sa && !ta) ? [240,235,220]
              : [240,235,220];
    // soft glowing head
    const r = 4.5 / scale;
    const grad = ctx.createRadialGradient(px, py, 0, px, py, r*2.2);
    grad.addColorStop(0, `rgba(${col[0]},${col[1]},${col[2]},${headA})`);
    grad.addColorStop(0.45, `rgba(${col[0]},${col[1]},${col[2]},${headA*0.35})`);
    grad.addColorStop(1, `rgba(${col[0]},${col[1]},${col[2]},0)`);
    ctx.fillStyle = grad;
    ctx.beginPath(); ctx.arc(px, py, r*2.2, 0, Math.PI*2); ctx.fill();
    // trailing line
    const tx = s.x + (t.x - s.x) * Math.max(0, e - 0.08);
    const ty = s.y + (t.y - s.y) * Math.max(0, e - 0.08);
    ctx.strokeStyle = `rgba(${col[0]},${col[1]},${col[2]},${headA*0.55})`;
    ctx.lineWidth = 1.1 / scale;
    ctx.beginPath();
    ctx.moveTo(tx, ty); ctx.lineTo(px, py); ctx.stroke();
  }

  // ── ingestion comets (new evidence landing) ──
  for (let i = ingestEvents.length - 1; i >= 0; i--) {
    const ev = ingestEvents[i];
    ev.t += dt;
    const k = ev.t / ev.dur;
    if (k >= 1) {
      // landing — pulse the target and propagate
      pulses.push({ node: ev.target, t: 0, dur: 1200 });
      propagatePulse(ev.target, 0);
      ingestEvents.splice(i, 1);
      continue;
    }
    // ease-out into landing
    const e = 1 - Math.pow(1 - k, 3);
    const px = ev.sx + (ev.target.x - ev.sx) * e;
    const py = ev.sy + (ev.target.y - ev.sy) * e;
    const headA = Math.min(1, k * 3) * (1 - Math.pow(k, 4));
    // gold comet head
    const headR = 13 / scale;
    const grad = ctx.createRadialGradient(px, py, 0, px, py, headR);
    grad.addColorStop(0,   `rgba(248,222,150,${headA*0.95})`);
    grad.addColorStop(0.4, `rgba(232,196,110,${headA*0.45})`);
    grad.addColorStop(1,   `rgba(232,196,110,0)`);
    ctx.fillStyle = grad;
    ctx.beginPath(); ctx.arc(px, py, headR, 0, Math.PI*2); ctx.fill();
    // trail behind comet — fade along k
    const trailSteps = 8;
    for (let j = 1; j <= trailSteps; j++) {
      const tk = Math.max(0, e - j * 0.04);
      const tx = ev.sx + (ev.target.x - ev.sx) * tk;
      const ty = ev.sy + (ev.target.y - ev.sy) * tk;
      const a = headA * (1 - j / trailSteps) * 0.35;
      ctx.strokeStyle = `rgba(232,196,110,${a})`;
      ctx.lineWidth = (3 - j*0.25) / scale;
      ctx.beginPath();
      ctx.moveTo(tx, ty);
      const ntk = Math.max(0, e - (j-1) * 0.04);
      const ntx = ev.sx + (ev.target.x - ev.sx) * ntk;
      const nty = ev.sy + (ev.target.y - ev.sy) * ntk;
      ctx.lineTo(ntx, nty);
      ctx.stroke();
    }
  }

  // ── pulses (halos) ──
  for (let i = pulses.length - 1; i >= 0; i--) {
    const p = pulses[i];
    p.t += dt;
    const k = p.t / p.dur;
    if (k >= 1) { pulses.splice(i, 1); continue; }
    const n = p.node;
    const r = n.s + 6 + k * 28;
    const a = (1 - k) * 0.55;
    const col = (n.t === 'I' && n.c && INT_CATEGORY_COLOR[n.c])
                  ? INT_CATEGORY_COLOR[n.c]
                  : (TYPE_COLOR[n.t] || TYPE_COLOR.H);
    const grad = ctx.createRadialGradient(n.x, n.y, 0, n.x, n.y, r);
    grad.addColorStop(0, `rgba(${col[0]},${col[1]},${col[2]},${a*0.7})`);
    grad.addColorStop(1, `rgba(${col[0]},${col[1]},${col[2]},0)`);
    ctx.fillStyle = grad;
    ctx.beginPath(); ctx.arc(n.x, n.y, r, 0, Math.PI*2); ctx.fill();
  }

  // ── nodes ──
  for (const n of nodes) {
    const col = (n.t === 'I' && n.c && INT_CATEGORY_COLOR[n.c])
                  ? INT_CATEGORY_COLOR[n.c]
                  : (TYPE_COLOR[n.t] || TYPE_COLOR.H);
    const active = inActive(n);
    let alpha;
    if (isFiltering) alpha = active ? 1.0 : 0.08;
    else             alpha = (n.t === 'G' ? 0.58 : 0.96);
    if (hover === n) alpha = 1.0;

    if (n.t !== 'G') {
      const g = ctx.createRadialGradient(n.x, n.y, 0, n.x, n.y, n.s + 5);
      g.addColorStop(0, `rgba(${col[0]},${col[1]},${col[2]},${alpha*0.32})`);
      g.addColorStop(1, `rgba(${col[0]},${col[1]},${col[2]},0)`);
      ctx.fillStyle = g;
      ctx.beginPath(); ctx.arc(n.x, n.y, n.s+5, 0, Math.PI*2); ctx.fill();
    }

    ctx.fillStyle = `rgba(${col[0]},${col[1]},${col[2]},${alpha})`;
    ctx.beginPath();
    ctx.arc(n.x, n.y, n.s, 0, Math.PI*2);
    ctx.fill();

    // gold ring on INT-0001 — the calibration anchor, always findable
    if (n.k === 'INT-0001') {
      ctx.strokeStyle = `rgba(232,196,110,${0.55 + alpha*0.35})`;
      ctx.lineWidth = 0.9/scale;
      ctx.beginPath();
      ctx.arc(n.x, n.y, n.s + 4, 0, Math.PI*2);
      ctx.stroke();
    }

    // hover — silent edge highlight
    if (hover === n) {
      ctx.strokeStyle = 'rgba(240,235,220,0.6)';
      ctx.lineWidth = 0.5/scale;
      for (const l of links) {
        if (l.source === n || l.target === n) {
          ctx.beginPath();
          ctx.moveTo(l.source.x, l.source.y);
          ctx.lineTo(l.target.x, l.target.y);
          ctx.stroke();
        }
      }
    }
  }

  ctx.restore();

  requestAnimationFrame(draw);
}

// kickoff — manifesto fades in shortly after first paint
setTimeout(() => {
  document.querySelector('.manifesto-inner').classList.add('ready');
}, 750);
requestAnimationFrame(draw);

// ── status counter loop (counts seconds since last ingest, formats nicely) ──
const papersEl = document.getElementById('papers');
const lastEl   = document.getElementById('last-ingest');
function fmtAgo(ms) {
  const s = Math.floor(ms / 1000);
  if (s < 5)    return 'just now';
  if (s < 60)   return s + 's ago';
  const m = Math.floor(s / 60);
  if (m < 60)   return m + 'm ' + (s % 60) + 's ago';
  return Math.floor(m / 60) + 'h ago';
}
setInterval(() => {
  papersEl.textContent = papersCount.toLocaleString();
  lastEl.textContent   = fmtAgo(performance.now() - ingestStartT);
}, 500);

// ── intake ticker rotation — cycles through the actual PubMed scanner
// output every 8 seconds. Real liveness, not theatre.
const tickerEl = document.getElementById('intake-ticker');
if (tickerEl && INTAKE && INTAKE.candidates && INTAKE.candidates.length) {
  let tickerIdx = 0;
  function rotateTicker() {
    if (!INTAKE.candidates.length) return;
    const c = INTAKE.candidates[tickerIdx % INTAKE.candidates.length];
    tickerIdx++;
    const title = (c.title || '').slice(0, 72);
    const author = c.first_author || '';
    const tag = c.intake_tag || '?';
    tickerEl.style.opacity = '0.2';
    setTimeout(() => {
      tickerEl.innerHTML = '[' + tag + '] ' + title +
        (author ? ' · <span style="color:var(--text-vmute);">' + author + '</span>' : '');
      tickerEl.style.transition = 'opacity 600ms';
      tickerEl.style.opacity = '1';
    }, 600);
  }
  rotateTicker();
  setInterval(rotateTicker, 8200);
}
</script>
</body>
</html>
"""

# sources.csv row-count = the "papers" headline number; falls back to 1420
sources_count = len(read_csv("sources.csv")) or 1420

# Format intake ticker line
if intake.get("latest_count"):
    by_tag = intake.get("by_tag") or {}
    tag_str = " · ".join(
        f'{n} {t.lower()}' for t, n in sorted(by_tag.items(), key=lambda x: -x[1])[:3]
    )
    intake_ticker = (
        f'{intake["latest_count"]} candidates last scan · {tag_str}'
        if tag_str else f'{intake["latest_count"]} candidates last scan'
    )
elif intake.get("last_run"):
    intake_ticker = f'last scan {intake["last_run"]}'
else:
    intake_ticker = 'pubmed scanner standing by'

# Build the intake-feed candidates for the rotating ticker
intake_feed_for_js = {"candidates": []}
intake_jsons = sorted(inbox_dir.glob("pubmed_intake_*.json"),
                      reverse=True) if inbox_dir.exists() else []
if intake_jsons:
    try:
        latest = json.loads(intake_jsons[0].read_text())
        # Compact: only the fields the ticker needs
        intake_feed_for_js["candidates"] = [
            {
                "pmid": c.get("pmid", ""),
                "title": (c.get("title") or "")[:140],
                "first_author": c.get("first_author") or "",
                "intake_tag": c.get("intake_tag") or "",
                "intake_focus": c.get("intake_focus") or "",
            }
            for c in latest.get("candidates", [])[:40]
        ]
    except Exception:
        pass

html = (HTML
        .replace("__N_NODES__", str(stats["n_nodes"]))
        .replace("__N_LINKS__", str(stats["n_links"]))
        .replace("__N_HYP__", str(stats["n_hyp"]))
        .replace("__N_MEC__", str(stats["n_mec"]))
        .replace("__N_INT__", str(stats["n_int"]))
        .replace("__N_PHE__", str(stats["n_phe"]))
        .replace("__N_BIO__", str(stats["n_bio"]))
        .replace("__N_COM__", str(stats["n_com"]))
        .replace("__N_TEST__", str(stats["n_test"]))
        .replace("__N_GEN__", str(stats["n_gen"]))
        .replace("__INTAKE_TICKER__", intake_ticker)
        .replace("__N_PAPERS__", f"{sources_count:,}")
        .replace("__PAPERS_BASE__", str(sources_count))
        .replace("__DATA__",
                 json.dumps({"nodes": nodes, "links": links},
                            separators=(",", ":")))
        .replace("__PROFILES__",
                 json.dumps(profile_info, separators=(",", ":")))
        .replace("__INTAKE_FEED__",
                 json.dumps(intake_feed_for_js, separators=(",", ":"))))

OUT.write_text(html)
print(f"wrote {OUT} ({OUT.stat().st_size//1024} KB)")
