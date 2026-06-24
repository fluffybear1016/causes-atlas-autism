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

# ── Curated must-have starter set ──────────────────────────────────────
# Hand-picked by curator priority, NOT auto-ranked. 23andMe is removed
# from this list (it communicates "consumer health kit", not "clinical-
# grade pediatric panel" — it stays in the catalog as a budget option
# but is not what we lead with). The must-haves are the panels every
# FM-trained pediatrician orders before considering subtype-specific work.
# MUST-HAVE — AUTISM-SPECIFIC tests. Each maps to an autism phenotype
# or has autism-specific responder data. NOT generic FM workup.
MUST_HAVE_TEST_IDS = [
    "TEST-0014",  # FRAA panel — autism-specific (Frye 2018 RCT, 78% FRAA+ responder rate)
    "TEST-0015",  # Plasma lactate / pyruvate / L:P ratio — autism mito overlap 30-80% (Rossignol 2011 meta)
    "TEST-0010",  # Mosaic OAT — autism-specific metabolites (arabinose, HPHPA, quinolinic acid)
    "TEST-0020",  # Cunningham Panel — autism-regressive subset (PANS overlap)
    "TEST-0008",  # Fragile X (FMR1 CGG repeat) — autism-syndromic 2-6% of cases
    "TEST-0116",  # MitoSwab buccal mito enzymes — non-invasive mito dysfunction confirmation
    "TEST-0117",  # CSF 5-MTHF — definitive cerebral folate deficiency test (anchor to INT-0001)
]

# EPIGENETIC METHYLATION — DNA methylation + biological age. Distinct from
# the biochemical methylation cycle (SAM/SAH/homocysteine) which lives in
# the foundation tier. This section is emerging-tier (mostly T4) but
# autism-relevant: maternal stress + nutrient methylation patterns + the
# specific autism-saliva-RNA biomarker panel.
EPIGENETIC_TEST_IDS = [
    "TEST-0090",  # Quadrant Biosciences Clarifi ASD — autism-specific salivary RNA panel (T4 emerging)
    "TEST-0012",  # Doctor's Data Methylation Profile — methylation cycle SNPs + biochemistry (T2)
    "TEST-0089",  # TruDiagnostic TruAge + DunedinPACE — epigenetic biological age (T4 emerging)
    "TEST-0119",  # EarliPoint FDA-cleared eye-tracking aid-in-diagnosis
    "TEST-0120",  # LinusBio ClearStrand-ASD hair-strand exposure profiling
]

# Aspirational / high-end tier — for moms who can afford the full workup
HIGH_END_TEST_IDS = [
    "TEST-0006",  # IntellxxDNA NeuroGenomic — Frye-aligned premium nutrigenomic
    "TEST-0009",  # Whole exome sequencing (WES) — full clinical genome
    "TEST-0016",  # Mayo Acylcarnitine profile — mitochondrial deep-dive
    "TEST-0122",  # Genova NutrEval — consolidated FM panel (replaces 5+ orders)
    "TEST-0129",  # Mayo mtDNA whole-genome sequencing
    "TEST-0118",  # CSF neurotransmitter metabolites — catches treatable AADC / sepiapterin defects
    "TEST-0131",  # Anti-neural autoimmune encephalitis panel — anti-NMDAR + GAD65 + VGKC
]

# Budget entry tier — DTC, lowest cost, useful starting point
BUDGET_TEST_IDS = [
    "TEST-0001",  # 23andMe raw genotyping ($99-199) — analyze via StrateGene
    "TEST-0005",  # StrateGene — free + Sequencing.com upload of raw data
    "TEST-0046",  # CBC + CMP + lipid panel — baseline insurance-covered
    "TEST-0043",  # Vitamin D 25-OH — cheap and universal
    "TEST-0121",  # Tiny Health pediatric microbiome — best 0-4 yr option
    "TEST-0127",  # Plasma vitamin A — restricted-eater phenotype
]

# ── Cross-phenotype universal foundation interventions ─────────────────
# Things almost every FM-trained doc starts with regardless of phenotype.
# These are OTC, low-cost, broadly safe, evidence-supported across multiple
# atlas phenotypes. ~$50-100/mo total. Cited so mom can see why each.
UNIVERSAL_FOUNDATION_INT_IDS = [
    "INT-0014",  # Omega-3 (EPA + DHA) — neuroinflammation, neurodev support
    "INT-0013",  # Vitamin D3 — autism cohort deficiency near-universal
    "INT-0015",  # Magnesium glycinate — calming, NMDA/GABA
    "INT-0046",  # Sleep architecture + melatonin — broad benefit
    "INT-0041",  # GFCF diet trial — large responder subset
]

# ── Mom-language "types of autism" labels ──────────────────────────────
# Same 11 phenotypes that already live in phenotypes.csv, surfaced with
# warmer naming so a non-technical parent can identify her child's
# presentation without needing to know the technical term.
AUTISM_TYPE_LABELS = {
    "PHE-0001": "Cerebral folate deficiency",
    "PHE-0002": "Mitochondrial-vulnerable",
    "PHE-0003": "Immune-inflammatory · regressive",
    "PHE-0004": "Gut–brain axis",
    "PHE-0005": "mTOR-syndromic",
    "PHE-0006": "Fragile X · FMR1",
    "PHE-0007": "GABA-imbalance",
    "PHE-0008": "MCAS overlap · mast-cell",
    "PHE-0009": "PANS / PANDAS · post-infectious",
    "PHE-0010": "Walsh undermethylator",
    "PHE-0011": "Walsh metallothionein-deficient",
}

# ── Functional-medicine resources for the footer ───────────────────────
# Curator-tier annotated. Tier 1 = scientific-clinical lineage; Tier 2 =
# parent-community; Tier 3 = activist-oriented (still useful but framing
# differs). Mom should know the tier of what she's reading.
FM_RESOURCES = [
    {"name": "MAPS doctor directory", "url": "https://medmaps.org",
     "tier": "T1", "what": "find a trained FM pediatrics clinician"},
    {"name": "Autism Research Institute", "url": "https://autism.org",
     "tier": "T1", "what": "Bernie Rimland's lineage; biomedical research"},
    {"name": "Walsh Research Institute", "url": "https://walshinstitute.org",
     "tier": "T1", "what": "methylation / metallothionein phenotypes; Walsh"},
    {"name": "Documenting Hope", "url": "https://documentinghope.com",
     "tier": "T2", "what": "parent-recovery project; protocols + outcomes"},
    {"name": "TACA", "url": "https://tacanow.org",
     "tier": "T2", "what": "parent community + practical resource library"},
]

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
billing = read_csv("billing_codes.csv")  # 2026-05-16: insurance + HSA/FSA scalability
billing_by_entity: dict[str, dict] = {}
for b in billing:
    eid = b.get("entity_id", "") or ""
    if eid:
        billing_by_entity[eid] = b

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

# Curated IDs are ALWAYS included regardless of CAP_TESTS — these are
# the ones the start-dock references, so they must render no matter what.
curated_ids = (set(MUST_HAVE_TEST_IDS) | set(HIGH_END_TEST_IDS) |
               set(BUDGET_TEST_IDS) | set(EPIGENETIC_TEST_IDS))
tests_ranked = sorted(tests, key=test_priority, reverse=True)
tests_curated = [t for t in tests_ranked if t.get("test_id") in curated_ids]
tests_other   = [t for t in tests_ranked if t.get("test_id") not in curated_ids]
tests_sorted  = tests_curated + tests_other[:max(0, CAP_TESTS - len(tests_curated))]
for t in sorted(tests_sorted, key=lambda r: r.get("test_id", "")):
    tid = t.get("test_id", "")
    if not tid:
        continue
    tier_raw = (t.get("evidence_tier") or "").lower()
    size = 3.5 if "tier1" in tier_raw else 2.8 if "tier2" in tier_raw else 2.2
    # Walk maps_to_intervention_ids so the test card can render the
    # actionable downstream: "if this test shows X, consider these
    # interventions." Mom's "what do I DO with this result" answer.
    mi_field = t.get("maps_to_intervention_ids", "") or ""
    mi_list = [x.strip() for x in mi_field.replace(";", ",").split(",")
               if x.strip()][:6]
    # Pull billing metadata: CPT codes, ICD-10 anchor, insurance posture,
    # HSA/FSA eligibility, self-pay range. This is how families
    # actually pay for FM-autism care at scale.
    bill = billing_by_entity.get(tid, {})

    # Classify collection mode: at-home (mouth swab, finger prick, urine,
    # stool, hair, dried-blood-spot) vs clinic (venipuncture). High-agency
    # moms strongly prefer at-home — comfort + scientific integrity at scale.
    sm_raw = (t.get("sample_type", "") or "").lower()
    AT_HOME_SAMPLES = (
        "saliva", "urine", "stool", "hair", "buccal", "swab",
        "dried_blood_spot", "dried_urine", "breath", "wearable",
        "upload",
    )
    CLINIC_SAMPLES = (
        "serum", "plasma", "blood", "marrow", "eeg",
    )
    is_at_home = any(k in sm_raw for k in AT_HOME_SAMPLES) and \
                 not any(k in sm_raw for k in CLINIC_SAMPLES)
    # Hybrid (e.g. "blood_or_saliva") → mark hybrid so mom sees "at-home option available"
    is_hybrid = (
        any(k in sm_raw for k in AT_HOME_SAMPLES) and
        any(k in sm_raw for k in CLINIC_SAMPLES)
    )
    collection_mode = "at-home" if is_at_home else ("hybrid" if is_hybrid else "clinic")

    add_node(tid, "T", t.get("test_name", "") or tid, size, extra={
        "pr": (t.get("provider", "") or "")[:48],
        "sm": (t.get("sample_type", "") or "")[:24],
        "cl": t.get("cost_usd_low", ""),
        "ch": t.get("cost_usd_high", ""),
        "td": t.get("turnaround_days", ""),
        "tr": (t.get("evidence_tier") or "").replace("Tier", "T").strip()[:5],
        "dtc": (t.get("direct_to_consumer", "") or "").upper() == "TRUE",
        "rx": (t.get("clinician_required", "") or "").upper() == "TRUE",
        "wm": (t.get("what_it_measures", "") or "")[:140],
        "uc": (t.get("specific_use_cases", "") or "")[:120],
        "wr": (t.get("what_results_indicate", "") or "")[:160],
        "mi": mi_list,
        # Order + collection mode
        "or": (t.get("source_url", "") or "")[:200],
        "cm": collection_mode,
        # Billing
        "cpt": (bill.get("cpt_codes") or "")[:80],
        "icd": (bill.get("icd10_anchor") or "")[:30],
        "ins": (bill.get("insurance_tier") or "")[:40],
        "pa":  (bill.get("prior_auth_typical") or "")[:20],
        "hsa": (bill.get("hsa_fsa_eligible") or "")[:12],
        "cn":  (bill.get("coverage_notes") or "")[:200],
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
    --text:    #e3ddcd;
    --text-mute:#9c968a;
    --text-vmute:#6b6760;
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

  /* ── LEFT START-HERE DOCK — always visible, idiot-proof entry ──── */
  /* What a mom sees the moment she lands. Three sections: where to
     start (1-line), the 5 starter tests with prices, what's emerged
     since yesterday. Click any test to jump to it on the map. The map
     is for exploration; this dock is for action. */
  .start-dock {
    position: fixed; left: 30px; top: 50%;
    transform: translateY(-50%);
    width: 320px; max-height: 78vh; overflow-y: auto;
    background: rgba(8, 11, 18, 0.78); backdrop-filter: blur(10px);
    border: 1px solid var(--line);
    z-index: 9;
    padding: 20px 22px 22px;
    font-family: ui-serif, "Iowan Old Style", Garamond, serif;
    pointer-events: auto;
    scrollbar-width: thin;
    scrollbar-color: var(--line-hi) transparent;
  }
  .start-dock::-webkit-scrollbar { width: 4px; }
  .start-dock::-webkit-scrollbar-thumb { background: var(--line-hi); }
  .start-dock .sd-section { margin-bottom: 22px; }
  .start-dock .sd-section:last-child { margin-bottom: 0; }
  .start-dock .sd-label {
    font-family: ui-monospace, monospace;
    font-size: 9.5px; letter-spacing: 0.24em;
    text-transform: uppercase; color: var(--gold);
    margin-bottom: 10px; padding-bottom: 6px;
    border-bottom: 1px solid var(--line);
  }
  .start-dock .sd-intro {
    font-size: 12.5px; color: var(--text); line-height: 1.55;
    font-style: italic;
  }
  .start-dock .sd-intro-block {
    margin-bottom: 22px;
    padding-bottom: 16px;
    border-bottom: 1px solid var(--line);
  }
  .start-dock .sd-welcome {
    font-family: ui-serif, "Iowan Old Style", "Apple Garamond", Georgia, serif;
    font-size: 18px; letter-spacing: 0.01em;
    color: var(--text); line-height: 1.3;
    margin-bottom: 8px;
  }
  .start-dock .sd-tag {
    font-size: 12px; line-height: 1.55;
    color: var(--text-mute); font-style: italic;
  }
  .start-dock .sd-test {
    font-size: 12px; line-height: 1.4;
    padding: 9px 0;
    border-bottom: 1px dashed var(--line);
    cursor: pointer;
    transition: color 200ms;
  }
  .start-dock .sd-test:last-child { border-bottom: none; }
  .start-dock .sd-test:hover .sd-test-name { color: var(--gold); }
  .start-dock .sd-test-name {
    color: var(--text);
    transition: color 200ms;
  }
  .start-dock .sd-test-meta {
    display: block; color: var(--text-mute);
    font-size: 10.5px; margin-top: 3px;
    letter-spacing: 0.02em;
  }
  .start-dock .sd-pill {
    display: inline-block; padding: 1px 5px;
    border: 1px solid var(--line-hi); border-radius: 3px;
    font-family: ui-monospace, monospace; font-size: 9px;
    letter-spacing: 0.18em; text-transform: uppercase;
    color: var(--text-mute); margin-left: 4px;
  }
  .start-dock .sd-pill.gold { color: var(--gold); border-color: var(--gold-dim); }
  .start-dock .sd-feed {
    font-size: 11.5px; line-height: 1.5;
    padding: 6px 0; color: var(--text-mute);
  }
  .start-dock .sd-feed-tag {
    color: var(--gold); font-family: ui-monospace, monospace;
    font-size: 9.5px; margin-right: 6px;
    letter-spacing: 0.12em;
  }
  .start-dock .sd-footer {
    margin-top: 18px; padding-top: 12px;
    border-top: 1px solid var(--line);
    font-size: 10px; letter-spacing: 0.14em;
    text-transform: uppercase; color: var(--text-vmute);
  }
  .start-dock .sd-footer a {
    color: var(--gold); text-decoration: none;
  }
  /* On narrower windows, collapse to a toggle button instead of always-open */
  @media (max-width: 1100px) {
    .start-dock { display: none; }
  }

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

  /* ── DATA UPLOAD UI ────────────────────────────────────────────── */
  .upload-btn {
    position: fixed; top: 22px; left: 50%; transform: translateX(-50%);
    z-index: 15;
    background: rgba(8,11,18,0.78); backdrop-filter: blur(8px);
    border: 1px solid var(--gold-dim); color: var(--gold);
    font: inherit; cursor: pointer; text-align: center;
    padding: 8px 22px; line-height: 1.45;
    transition: color 300ms, border-color 300ms, background 300ms;
  }
  .upload-btn:hover {
    color: var(--text); border-color: var(--gold);
    background: rgba(12,14,22,0.92);
  }
  .upload-btn.has-data {
    color: var(--gold); border-color: var(--gold);
    background: rgba(232,196,110,0.08);
  }
  .upload-btn .ub-main {
    display: block;
    font-size: 10.5px; letter-spacing: 0.22em;
    text-transform: uppercase;
  }
  .upload-btn .ub-sub {
    display: block;
    font-size: 9px; letter-spacing: 0.26em;
    text-transform: uppercase;
    color: var(--text-vmute);
    margin-top: 2px;
  }
  .upload-btn:hover .ub-sub { color: var(--text-mute); }
  .upload-btn .dot {
    display: inline-block; width: 6px; height: 6px;
    border-radius: 50%; background: var(--gold);
    box-shadow: 0 0 6px var(--gold);
    margin-right: 8px; vertical-align: middle;
  }
  .user-data {
    position: fixed; top: 68px; left: 50%; transform: translateX(-50%);
    z-index: 14;
    background: rgba(8,11,18,0.85); backdrop-filter: blur(8px);
    border: 1px solid var(--gold-dim);
    padding: 6px 16px;
    font-size: 10.5px; letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--text); pointer-events: none;
    display: none; white-space: nowrap;
  }
  .user-data.on { display: block; }
  .user-data .gold { color: var(--gold); }

  .modal-backdrop {
    position: fixed; inset: 0; z-index: 100;
    background: rgba(5,8,16,0.88); backdrop-filter: blur(12px);
    display: none; align-items: flex-start; justify-content: center;
    padding: 40px 24px;
    overflow-y: auto;
  }
  .modal-backdrop.on { display: flex; }
  .modal {
    width: clamp(320px, 90vw, 720px);
    background: rgba(12,14,22,0.98);
    border: 1px solid var(--gold-dim);
    color: var(--text);
    padding: 28px 32px 32px;
    position: relative;
  }
  .modal .m-close {
    position: absolute; top: 14px; right: 18px;
    background: transparent; border: none;
    color: var(--text-mute); font-size: 24px;
    cursor: pointer; padding: 4px 10px; line-height: 1;
  }
  .modal .m-close:hover { color: var(--text); }
  .modal .m-title {
    font-size: 18px; letter-spacing: 0.04em;
    color: var(--node); margin-bottom: 4px;
  }
  .modal .m-sub {
    font-size: 11px; letter-spacing: 0.18em;
    color: var(--text-mute); text-transform: uppercase;
    margin-bottom: 18px;
  }
  .modal .m-privacy {
    display: flex; gap: 10px; align-items: flex-start;
    padding: 10px 14px; margin-bottom: 18px;
    background: rgba(232,196,110,0.06);
    border: 1px solid var(--gold-dim);
    font-size: 11.5px; line-height: 1.55; color: var(--text);
  }
  .modal .m-privacy .pdot {
    width: 6px; height: 6px; border-radius: 50%;
    background: var(--gold); margin-top: 6px; flex-shrink: 0;
  }
  .modal .m-tabs {
    display: flex; gap: 0;
    border-bottom: 1px solid var(--line);
    margin-bottom: 22px;
    overflow-x: auto;
  }
  .modal .m-tab {
    background: transparent; border: none;
    color: var(--text-mute); font: inherit;
    font-size: 11px; letter-spacing: 0.2em;
    text-transform: uppercase; white-space: nowrap;
    padding: 11px 18px; cursor: pointer;
    border-bottom: 2px solid transparent;
    margin-bottom: -1px;
    transition: color 200ms, border-color 200ms;
  }
  .modal .m-tab:hover { color: var(--text); }
  .modal .m-tab.on { color: var(--gold); border-bottom-color: var(--gold); }
  .modal .m-pane { display: none; }
  .modal .m-pane.on { display: block; }
  .modal .m-drop {
    border: 1px dashed var(--line-hi);
    padding: 36px 24px; text-align: center;
    cursor: pointer; transition: border-color 200ms, background 200ms;
    margin-bottom: 12px;
  }
  .modal .m-drop:hover, .modal .m-drop.drag {
    border-color: var(--gold); background: rgba(232,196,110,0.04);
  }
  .modal .m-drop-title {
    font-size: 13px; letter-spacing: 0.04em; color: var(--text);
    margin-bottom: 6px;
  }
  .modal .m-drop-sub {
    font-size: 11px; letter-spacing: 0.14em; color: var(--text-mute);
    text-transform: uppercase;
  }
  .modal .m-status {
    font-family: ui-monospace, monospace; font-size: 11px;
    color: var(--gold); padding: 8px 12px;
    border: 1px solid var(--gold-dim);
    margin-bottom: 14px; display: none;
    line-height: 1.5;
  }
  .modal .m-status.on { display: block; }
  .modal .m-status.err { color: #f0a090; border-color: #6e2222; }
  .modal .m-help {
    font-size: 11.5px; color: var(--text-mute);
    line-height: 1.6; margin-bottom: 14px;
  }
  .modal .m-paste {
    width: 100%; min-height: 120px;
    background: rgba(8,11,18,0.6);
    border: 1px solid var(--line);
    color: var(--text); font: inherit;
    font-family: ui-monospace, monospace; font-size: 11.5px;
    padding: 10px 12px; resize: vertical; margin-bottom: 12px;
  }
  .modal .m-paste:focus { outline: none; border-color: var(--gold-dim); }
  .modal .m-form-grid {
    display: grid; grid-template-columns: 1fr 1fr;
    gap: 14px 18px;
  }
  .modal .m-field { display: flex; flex-direction: column; font-size: 12px; }
  .modal .m-field label {
    font-size: 10px; letter-spacing: 0.18em;
    text-transform: uppercase; color: var(--text-mute);
    margin-bottom: 4px;
  }
  .modal .m-field .units {
    color: var(--text-vmute); font-size: 9.5px;
    text-transform: none; letter-spacing: 0.04em; margin-left: 6px;
  }
  .modal .m-field input {
    background: rgba(8,11,18,0.5);
    border: 1px solid var(--line);
    color: var(--text); font: inherit; font-size: 12.5px;
    padding: 7px 10px; outline: none;
  }
  .modal .m-field input:focus { border-color: var(--gold-dim); }
  .modal .m-field input.high { color: #f0a890; border-color: #6e3a22; }
  .modal .m-field input.low  { color: #b4c8e8; border-color: #2a4060; }
  .modal .m-field .ref {
    font-size: 9.5px; color: var(--text-vmute);
    margin-top: 3px; letter-spacing: 0.04em;
  }
  .modal .m-save {
    background: var(--gold); border: none; color: var(--void);
    font: inherit; font-size: 11px; letter-spacing: 0.24em;
    text-transform: uppercase; padding: 12px 28px;
    cursor: pointer; margin-top: 18px;
    transition: background 200ms;
  }
  .modal .m-save:hover { background: #f0d080; }
  .modal .m-clear {
    background: transparent; border: 1px solid var(--line);
    color: var(--text-mute); font: inherit; font-size: 10px;
    letter-spacing: 0.22em; text-transform: uppercase;
    padding: 9px 14px; cursor: pointer; margin-top: 18px;
    margin-left: 10px;
    transition: color 200ms, border-color 200ms;
  }
  .modal .m-clear:hover { color: var(--text); border-color: var(--line-hi); }

  /* mobile bottom-dock toggle button */
  .mobile-dock-btn {
    display: none;
    position: fixed; bottom: 78px; left: 14px;
    z-index: 13;
    background: rgba(8,11,18,0.85); backdrop-filter: blur(8px);
    border: 1px solid var(--line-hi); color: var(--text);
    font: inherit; font-size: 9.5px; letter-spacing: 0.2em;
    padding: 9px 14px; cursor: pointer; text-transform: uppercase;
  }
  .mobile-dock-btn.on { color: var(--gold); border-color: var(--gold-dim); }

  /* ── TOP FINDINGS SYNTHESIS (executive summary panel) ──────────── */
  /* Sits at the top of the report. Prioritized, clustered, mom-actionable. */
  .r-synth {
    background: rgba(232,196,110,0.04);
    border: 1px solid var(--gold-dim);
    padding: 24px 28px 26px;
    margin-bottom: 36px;
  }
  .r-synth-eyebrow {
    font-size: 9.5px; letter-spacing: 0.34em;
    text-transform: uppercase; color: var(--gold);
    margin-bottom: 10px;
  }
  .r-synth-headline {
    font-size: 20px; color: var(--node); line-height: 1.3;
    letter-spacing: -0.005em; margin-bottom: 18px;
  }
  .r-synth-section {
    margin-top: 22px;
  }
  .r-synth-label {
    font-size: 9px; letter-spacing: 0.26em;
    text-transform: uppercase; color: var(--gold);
    margin-bottom: 10px; padding-bottom: 6px;
    border-bottom: 1px solid var(--line);
  }
  .r-synth-action {
    padding: 11px 0;
    border-bottom: 1px dashed var(--line);
    font-size: 13px; line-height: 1.55;
  }
  .r-synth-action:last-child { border-bottom: none; }
  .r-synth-action .num {
    display: inline-block; width: 18px;
    color: var(--gold); font-family: ui-monospace, monospace;
    font-size: 11px; vertical-align: top;
  }
  .r-synth-action .body { display: inline-block; width: calc(100% - 22px); }
  .r-synth-action .head {
    color: var(--node); font-size: 14px; margin-bottom: 3px;
  }
  .r-synth-action .why {
    color: var(--text-mute); font-size: 12px; line-height: 1.5;
  }
  .r-synth-cluster {
    padding: 12px 14px;
    background: rgba(8,11,18,0.4);
    border-left: 2px solid var(--line-hi);
    margin-bottom: 10px;
    font-size: 12.5px; line-height: 1.55;
  }
  .r-synth-cluster.sev-2 { border-left-color: var(--gold-dim); }
  .r-synth-cluster.sev-3 { border-left-color: var(--gold); }
  .r-synth-cluster-head {
    display: flex; justify-content: space-between; align-items: baseline;
    margin-bottom: 5px;
  }
  .r-synth-cluster-name {
    color: var(--node); font-size: 13.5px;
    letter-spacing: 0.01em;
  }
  .r-synth-cluster-load {
    font-family: ui-monospace, monospace;
    font-size: 10px; letter-spacing: 0.14em;
    color: var(--gold); text-transform: uppercase;
  }
  .r-synth-cluster-genes {
    font-family: ui-monospace, monospace;
    color: var(--text-mute); font-size: 11px;
    letter-spacing: 0.04em;
  }
  .r-synth-avoid {
    font-size: 12.5px; line-height: 1.55;
    color: var(--text);
  }
  .r-synth-avoid li {
    margin-bottom: 5px; padding-left: 12px;
    text-indent: -12px; list-style: none;
  }
  .r-synth-avoid li:before {
    content: "·"; color: var(--gold); margin-right: 10px; font-weight: bold;
  }
  .r-synth-sources {
    margin-top: 22px; padding-top: 14px;
    border-top: 1px solid var(--line);
    font-size: 10px; letter-spacing: 0.06em;
    color: var(--text-vmute); line-height: 1.55;
  }

  /* "see all 52 variants" toggle for the detail section */
  .r-collapse-toggle {
    background: transparent; border: 1px solid var(--line-hi);
    color: var(--text-mute); font: inherit;
    font-size: 10.5px; letter-spacing: 0.2em;
    text-transform: uppercase; padding: 9px 16px;
    cursor: pointer; margin-bottom: 14px;
    transition: color 200ms, border-color 200ms;
  }
  .r-collapse-toggle:hover {
    color: var(--text); border-color: var(--gold-dim);
  }
  .r-collapsed { display: none; }

  /* ── REPORT OVERLAY (Ive-restrained) ───────────────────────────── */
  /* What the substrate is FOR. Auto-opens after upload save.
     Single column, generous spacing, hairline gold rules, serif body. */
  .report-overlay {
    position: fixed; inset: 0; z-index: 110;
    background: rgba(5,8,16,0.97); backdrop-filter: blur(14px);
    display: none; overflow-y: auto;
    padding: 60px 24px 60px;
    animation: r-fade 600ms ease;
  }
  @keyframes r-fade { from { opacity: 0; } to { opacity: 1; } }
  .report-overlay.on { display: block; }
  .report {
    max-width: 680px; margin: 0 auto;
    color: var(--text);
    font-family: ui-serif, "Iowan Old Style", Garamond, serif;
    position: relative;
    padding-bottom: 80px;
  }
  .r-close {
    position: fixed; top: 22px; right: 28px;
    background: transparent; border: 1px solid var(--line-hi);
    color: var(--text-mute); font-size: 22px;
    cursor: pointer; padding: 6px 14px; line-height: 1;
    z-index: 5;
  }
  .r-close:hover { color: var(--text); border-color: var(--gold-dim); }
  .r-header { margin-bottom: 40px; }
  .r-eyebrow {
    font-size: 10px; letter-spacing: 0.34em;
    text-transform: uppercase; color: var(--gold);
    margin-bottom: 14px;
  }
  .r-title {
    font-size: 32px; letter-spacing: -0.01em;
    color: var(--node); line-height: 1.15;
    margin-bottom: 10px;
  }
  .r-sub {
    font-size: 12px; letter-spacing: 0.16em;
    color: var(--text-mute); text-transform: uppercase;
  }
  .r-section { margin-bottom: 38px; }
  .r-section-label {
    font-size: 9.5px; letter-spacing: 0.28em;
    text-transform: uppercase; color: var(--gold);
    padding-bottom: 8px; margin-bottom: 14px;
    border-bottom: 1px solid var(--line);
  }
  .r-summary {
    font-size: 14px; line-height: 1.65; color: var(--text);
  }
  .r-summary .pill {
    display: inline-block;
    font-family: ui-monospace, monospace;
    font-size: 10px; letter-spacing: 0.14em;
    text-transform: uppercase; color: var(--gold);
    border: 1px solid var(--gold-dim);
    padding: 2px 8px; margin-right: 6px; margin-bottom: 6px;
  }
  .r-phe {
    padding: 14px 0;
    border-bottom: 1px dashed var(--line);
  }
  .r-phe:last-child { border-bottom: none; }
  .r-phe-head {
    display: flex; align-items: baseline; justify-content: space-between;
    margin-bottom: 6px;
  }
  .r-phe-name {
    font-size: 16px; color: var(--node);
    letter-spacing: 0.01em;
  }
  .r-phe-pct {
    font-family: ui-monospace, monospace;
    font-size: 16px; color: var(--gold);
    font-variant-numeric: tabular-nums;
  }
  .r-phe-evidence {
    font-size: 12px; color: var(--text-mute); line-height: 1.55;
  }
  .r-phe-bar {
    height: 2px; background: var(--line);
    margin-top: 8px; overflow: hidden;
  }
  .r-phe-bar-fill {
    height: 100%; background: var(--gold);
    transform-origin: left;
    transform: scaleX(0);
    animation: r-bar 1200ms ease forwards;
  }
  @keyframes r-bar { to { transform: scaleX(var(--r-fill, 1)); } }
  .r-variant {
    padding: 16px 18px; margin-bottom: 12px;
    background: rgba(8,11,18,0.55);
    border-left: 2px solid var(--line-hi);
  }
  .r-variant.sev-1 { border-left-color: var(--gold-dim); }
  .r-variant.sev-2 { border-left-color: var(--gold); }
  .r-variant.sev-3 { border-left-color: var(--gold);
                      background: rgba(232,196,110,0.06); }
  .r-var-head {
    display: flex; align-items: baseline; justify-content: space-between;
    margin-bottom: 6px; gap: 12px;
  }
  .r-var-gene {
    font-size: 15px; color: var(--node);
    letter-spacing: 0.01em;
  }
  .r-var-name {
    font-size: 12px; color: var(--text-mute);
    margin-left: 8px; letter-spacing: 0.04em;
  }
  .r-var-geno {
    font-family: ui-monospace, monospace;
    font-size: 12.5px; letter-spacing: 0.12em;
    color: var(--gold);
    border: 1px solid var(--gold-dim);
    padding: 2px 10px;
    white-space: nowrap;
  }
  .r-var-effect {
    font-size: 13px; color: var(--text);
    margin-bottom: 4px;
  }
  .r-var-detail {
    font-size: 12px; color: var(--text-mute);
    line-height: 1.55; margin-bottom: 10px;
    font-style: italic;
  }
  .r-var-row {
    display: grid; grid-template-columns: 86px 1fr;
    gap: 12px; padding: 4px 0;
    font-size: 12.5px; line-height: 1.5;
  }
  .r-var-row-label {
    font-family: ui-monospace, monospace; font-size: 9.5px;
    letter-spacing: 0.22em; color: var(--gold);
    text-transform: uppercase; padding-top: 3px;
  }
  .r-var-row-content { color: var(--text); }
  .r-var-row-content .pill {
    display: inline-block;
    font-family: ui-monospace, monospace; font-size: 9px;
    letter-spacing: 0.18em; text-transform: uppercase;
    color: var(--text-mute);
    border: 1px solid var(--line-hi);
    padding: 1px 6px; margin: 0 4px 4px 0;
  }
  .r-var-row-content .pill.atlas {
    color: var(--gold); border-color: var(--gold-dim);
  }

  .r-oor {
    display: grid;
    grid-template-columns: 1fr auto auto;
    gap: 8px 18px;
    font-size: 13px;
  }
  .r-oor-name { color: var(--text); }
  .r-oor-val {
    font-family: ui-monospace, monospace;
    color: var(--text);
  }
  .r-oor-flag {
    font-family: ui-monospace, monospace;
    font-size: 9.5px; letter-spacing: 0.2em;
    text-transform: uppercase;
    padding: 1px 8px; border: 1px solid;
    align-self: center;
  }
  .r-oor-flag.high { color: #f0a890; border-color: #6e3a22; }
  .r-oor-flag.low  { color: #b4c8e8; border-color: #2a4060; }
  .r-int {
    padding: 14px 0;
    border-bottom: 1px dashed var(--line);
  }
  .r-int:last-child { border-bottom: none; }
  .r-int-name {
    font-size: 15px; color: var(--text);
    margin-bottom: 4px;
  }
  .r-int-meta {
    font-family: ui-monospace, monospace;
    font-size: 10.5px; letter-spacing: 0.14em;
    color: var(--text-mute); text-transform: uppercase;
    margin-bottom: 6px;
  }
  .r-int-meta .gold { color: var(--gold); }
  .r-int-rationale {
    font-size: 12.5px; color: var(--text-mute);
    line-height: 1.55;
  }
  .r-test {
    display: grid;
    grid-template-columns: 1fr auto auto;
    gap: 6px 18px;
    padding: 11px 0;
    border-bottom: 1px dashed var(--line);
    font-size: 13px;
  }
  .r-test:last-child { border-bottom: none; }
  .r-test-name { color: var(--text); }
  .r-test-meta {
    font-family: ui-monospace, monospace; font-size: 10px;
    color: var(--text-mute); letter-spacing: 0.12em;
    text-transform: uppercase; align-self: center;
  }
  .r-test-cost {
    font-family: ui-monospace, monospace;
    color: var(--gold); font-variant-numeric: tabular-nums;
    align-self: center;
  }
  .r-empty {
    color: var(--text-mute); font-size: 13px;
    font-style: italic; padding: 6px 0;
  }
  .r-disclaimer {
    margin-top: 50px; padding: 22px 24px;
    background: rgba(232,196,110,0.04);
    border: 1px solid var(--gold-dim);
    font-size: 11.5px; line-height: 1.6; color: var(--text);
  }
  .r-disclaimer strong { color: var(--gold); font-weight: 400; letter-spacing: 0.04em; }
  .r-footer {
    display: flex; gap: 12px; flex-wrap: wrap;
    margin-top: 36px;
  }
  .r-btn {
    background: transparent; border: 1px solid var(--gold-dim);
    color: var(--gold); font: inherit;
    font-size: 10.5px; letter-spacing: 0.22em;
    text-transform: uppercase;
    padding: 12px 22px; cursor: pointer;
    transition: color 200ms, border-color 200ms, background 200ms;
  }
  .r-btn:hover { color: var(--node); border-color: var(--gold); background: rgba(232,196,110,0.06); }
  .r-btn.primary {
    background: var(--gold); color: var(--void);
  }
  .r-btn.primary:hover { background: #f0d080; color: var(--void); }

  /* View-Report banner that replaces the small "your data" line */
  .view-report {
    position: fixed; top: 76px; left: 50%; transform: translateX(-50%);
    z-index: 14;
    background: rgba(232,196,110,0.10); backdrop-filter: blur(8px);
    border: 1px solid var(--gold); color: var(--gold);
    font: inherit; font-size: 10.5px; letter-spacing: 0.22em;
    padding: 9px 22px; cursor: pointer; text-transform: uppercase;
    display: none;
    transition: background 200ms, color 200ms;
  }
  .view-report.on { display: inline-block; }
  .view-report:hover { background: rgba(232,196,110,0.18); color: var(--node); }
  .view-report .dot {
    display: inline-block; width: 6px; height: 6px;
    border-radius: 50%; background: var(--gold);
    box-shadow: 0 0 8px var(--gold);
    margin-right: 10px; vertical-align: middle;
    animation: ingest-pulse 1.8s ease-in-out infinite;
  }

  /* Generating animation in the upload modal */
  .m-generating {
    text-align: center; padding: 32px 24px;
    color: var(--gold);
    font-size: 13px; letter-spacing: 0.16em;
    text-transform: uppercase;
    display: none;
  }
  .m-generating.on { display: block; }
  .m-gen-dots span {
    display: inline-block; width: 6px; height: 6px;
    border-radius: 50%; background: var(--gold);
    margin: 0 4px; opacity: 0.3;
    animation: r-gen 1.4s ease-in-out infinite;
  }
  .m-gen-dots span:nth-child(2) { animation-delay: 0.2s; }
  .m-gen-dots span:nth-child(3) { animation-delay: 0.4s; }
  @keyframes r-gen {
    0%, 60%, 100% { opacity: 0.3; transform: scale(0.9); }
    30%           { opacity: 1.0; transform: scale(1.2); }
  }

  /* ── MOBILE RESPONSIVE ─────────────────────────────────────────── */
  @media (max-width: 768px) {
    .overlay.tl { top: 12px; left: 14px; font-size: 9px; }
    .overlay.tl .title { font-size: 11px; letter-spacing: 0.24em; }
    .overlay.tr { top: 12px; right: 14px; font-size: 8.5px; max-width: 42vw; }
    .overlay.tr .num { font-size: 9px; }
    .overlay.bl { bottom: 14px; left: 14px; font-size: 9px; }

    .upload-btn {
      top: auto; bottom: 144px; left: 14px; transform: none;
      padding: 7px 14px;
    }
    .upload-btn .ub-main { font-size: 9.5px; letter-spacing: 0.16em; }
    .upload-btn .ub-sub  { font-size: 8.5px; letter-spacing: 0.18em; }
    .user-data {
      top: auto; bottom: 184px; left: 14px; right: 14px; transform: none;
      font-size: 9px; letter-spacing: 0.12em; padding: 6px 12px;
      white-space: normal; text-align: center;
    }

    .manifesto-inner { font-size: clamp(34px, 11vw, 64px); }

    /* dock becomes a bottom strip */
    .dock {
      bottom: 14px; right: 14px; left: 14px;
      align-items: stretch;
    }
    .dock .input { width: 100%; font-size: 12px; padding: 10px 12px; }
    .dock .toggle { font-size: 9.5px; padding: 9px 12px; letter-spacing: 0.18em; }
    .dock .presets { max-width: 100%; }
    .dock.open .presets { max-height: 240px; }

    /* left start-dock becomes a full-screen overlay opened by a button */
    .start-dock {
      display: none !important;
      position: fixed; top: 0; left: 0; right: 0; bottom: 0;
      width: 100vw; height: 100vh; max-height: none; transform: none;
      padding: 58px 22px 110px;
      z-index: 11;
    }
    .start-dock.mobile-on { display: block !important; }
    .mobile-dock-btn { display: block; }

    /* action card slides up from bottom, full width */
    .action-card {
      width: 100%; left: 0; right: 0; bottom: 0;
      transform: translateY(20px);
      padding: 18px 22px 28px;
      max-height: 65vh; overflow-y: auto;
      border-left: none; border-right: none; border-bottom: none;
    }
    .action-card.on { transform: translateY(0); }
    .action-card .ac-name { font-size: 15px; }
    .action-card .ac-pe { font-size: 12.5px; line-height: 1.5; }
    .action-card .ac-row {
      grid-template-columns: 1fr;
      gap: 4px; padding: 8px 0; font-size: 12px;
    }
    .action-card .ac-label { font-size: 9px; padding-top: 0; }

    .modal-backdrop { padding: 20px 12px; }
    .modal { padding: 22px 20px 26px; }
    .modal .m-form-grid { grid-template-columns: 1fr; gap: 10px; }
    .modal .m-tab { padding: 10px 14px; font-size: 10px; }

    /* report on mobile */
    .report-overlay { padding: 50px 16px 40px; }
    .r-close { top: 14px; right: 14px; }
    .r-title { font-size: 24px; }
    .r-section { margin-bottom: 30px; }
    .r-oor { grid-template-columns: 1fr auto; gap: 4px 12px; }
    .r-oor-flag { grid-column: 1 / -1; justify-self: start; margin-bottom: 6px; }
    .r-test { grid-template-columns: 1fr auto; }
    .r-test-meta { grid-column: 1 / -1; }
    .r-footer .r-btn { font-size: 9.5px; padding: 11px 16px; letter-spacing: 0.18em; }
    .view-report { top: auto; bottom: 220px; left: 14px; right: 14px; transform: none; }

    /* hover label hidden on touch */
    .hover-label { display: none !important; }
  }

  /* ─── Welcome state overlay (first-visit gate) ───────────────────── */
  .welcome {
    position: fixed; inset: 0; z-index: 9000;
    display: none;
    background: radial-gradient(ellipse at center,
      rgba(8,11,18,0.92) 0%,
      rgba(5,8,16,0.98) 100%);
    align-items: center; justify-content: center;
    opacity: 0;
    transition: opacity 700ms ease;
  }
  .welcome.on {
    display: flex;
    opacity: 1;
  }
  .welcome.fading {
    opacity: 0;
    pointer-events: none;
  }
  .welcome-inner {
    text-align: center;
    max-width: 640px;
    padding: 0 32px;
  }
  .welcome-eyebrow {
    font-family: ui-monospace, monospace;
    font-size: 10px; letter-spacing: 0.42em;
    text-transform: uppercase;
    color: var(--text-mute);
    margin-bottom: 28px;
    opacity: 0;
    animation: w-fadeUp 1100ms ease 200ms forwards;
  }
  .welcome-hero {
    font-family: ui-serif, "Iowan Old Style", "Apple Garamond", Georgia, serif;
    font-size: 34px; line-height: 1.32;
    color: var(--text);
    margin-bottom: 40px;
    opacity: 0;
    animation: w-fadeUp 1300ms ease 500ms forwards;
  }
  .welcome-cta {
    background: transparent;
    border: 1px solid var(--gold);
    color: var(--text);
    font: inherit;
    font-size: 12px; letter-spacing: 0.32em;
    text-transform: uppercase;
    padding: 13px 38px;
    cursor: pointer;
    transition: background 200ms, color 200ms, border-color 200ms;
    opacity: 0;
    animation: w-fadeUp 1100ms ease 900ms forwards;
  }
  .welcome-cta:hover {
    background: rgba(207, 168, 87, 0.06);
    color: var(--gold);
  }
  .welcome-skip {
    display: block;
    margin-top: 22px;
    color: var(--text-mute);
    font-size: 11px; letter-spacing: 0.16em;
    text-decoration: none;
    cursor: pointer;
    opacity: 0;
    animation: w-fadeUp 1100ms ease 1200ms forwards;
    transition: color 200ms;
  }
  .welcome-skip:hover { color: var(--text); }
  @keyframes w-fadeUp {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
  }
  body.welcome-active .overlay,
  body.welcome-active .dock,
  body.welcome-active .start-dock,
  body.welcome-active .view-report,
  body.welcome-active .upload-btn,
  body.welcome-active #upload-btn,
  body.welcome-active .mobile-dock-btn,
  body.welcome-active .legend,
  body.welcome-active .manifesto,
  body.welcome-active .map-caption { display: none !important; }
  body.welcome-active canvas { opacity: 0.30; }

  /* ─── Map caption (post-welcome single-line) ──────────────────────── */
  .map-caption {
    position: fixed;
    left: 50%; bottom: 84px;
    transform: translateX(-50%);
    max-width: 640px;
    width: calc(100% - 64px);
    text-align: center;
    pointer-events: none;
    opacity: 0;
    transition: opacity 1400ms ease 1800ms;
    z-index: 50;
  }
  .map-caption.ready { opacity: 1; }
  .map-caption.dim   { opacity: 0.20; transition: opacity 700ms ease; }
  .map-caption.hidden { opacity: 0; transition: opacity 700ms ease; }
  .map-caption .map-caption-text {
    font-family: ui-serif, "Iowan Old Style", "Apple Garamond", Georgia, serif;
    font-size: 13px;
    font-style: italic;
    line-height: 1.5;
    color: var(--text-mute);
  }
  @media (max-width: 720px) {
    .map-caption { bottom: 96px; }
    .map-caption .map-caption-text { font-size: 12px; }
  }
</style>
</head>
<body>

<!-- Welcome state overlay: first-visit gate -->
<div class="welcome on" id="welcome">
  <div class="welcome-inner">
    <div class="welcome-eyebrow">Causes Atlas · Autism</div>
    <div class="welcome-hero">A second opinion for your child,<br>drawn from the evidence.</div>
    <button class="welcome-cta" id="welcome-begin">Begin</button>
    <a class="welcome-skip" id="welcome-skip" tabindex="0">or explore the map →</a>
  </div>
</div>

<!-- ghost manifesto behind the graph -->
<div class="manifesto">
  <div class="manifesto-inner">
    Population&nbsp;average<br>
    <em>is&nbsp;not</em><br>
    your&nbsp;child
  </div>
</div>

<canvas id="c"></canvas>

<div class="map-caption" id="map-caption">
  <div class="map-caption-text">
    Every peer-reviewed paper, every gene mapped to autism, every federal record, every clinical trial, every Reddit thread, every X post — weighted, connected, scored, refreshed daily.
  </div>
</div>

<div class="overlay tl">
  <div class="title">Causes Atlas</div>
  <div class="vmute" style="margin-top:5px;">Autism</div>
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
  <button class="toggle" id="toggle">see an example</button>
</div>

<div class="hover-label" id="hover"></div>

<!-- Upload-my-data button (top-center) + your-data summary banner -->
<button class="upload-btn" id="upload-btn">
  <span class="ub-main">Upload my Genetics · Bloodwork · Health Reports</span>
  <span class="ub-sub">Private · stays in your browser</span>
</button>
<div class="user-data" id="user-data"></div>

<!-- Mobile bottom-left starter-dock toggle -->
<button class="mobile-dock-btn" id="mobile-dock-btn">starter tests</button>

<!-- Upload modal -->
<div class="modal-backdrop" id="upload-modal">
  <div class="modal">
    <button class="m-close" id="m-close">×</button>
    <div class="m-title">Bring your data into the map</div>
    <div class="m-sub">private · client-side only · stays in your browser</div>
    <div class="m-privacy">
      <div class="pdot"></div>
      <div>
        Files parsed entirely in your browser. Nothing is sent to any server. Your data is saved in this browser's local storage on this device only. Clear it any time below.
        <div id="m-freshness" style="margin-top:8px;font-family:ui-monospace,monospace;font-size:10px;letter-spacing:0.14em;color:var(--text-mute);text-transform:uppercase;"></div>
        <button id="m-reset-all" style="display:none;margin-top:10px;background:transparent;border:1px solid #6e3a22;color:#f0a890;font:inherit;font-size:9.5px;letter-spacing:0.2em;text-transform:uppercase;padding:6px 12px;cursor:pointer;">Reset ALL my data (start fresh)</button>
      </div>
    </div>
    <div class="m-tabs">
      <button class="m-tab on" data-pane="pdf">lab pdf</button>
      <button class="m-tab" data-pane="genetics">raw dna file</button>
      <button class="m-tab" data-pane="bloodwork">blood work form</button>
    </div>
    <div class="m-pane on" id="pane-pdf">
      <div class="m-drop" id="pdf-drop">
        <input type="file" id="pdf-file" style="display:none" accept=".pdf,application/pdf" multiple />
        <div class="m-drop-title">Drop your lab PDFs here or click to choose</div>
        <div class="m-drop-sub">Quest · LabCorp · Genova · Mosaic · Invitae · GeneDx · 23andMe report · any PDF</div>
      </div>
      <div class="m-status" id="pdf-status"></div>
      <div class="m-help">
        We read the PDF in your browser and scan for both biomarker values (vitamin D, ferritin, homocysteine, IGF-1, …) and gene mentions (MTHFR, FOLR1, MTR, …). Anything found lights up its node on the map and pre-fills the blood-work form. Multiple PDFs at once is fine. <strong>For scanned PDFs without a text layer</strong>, use the paste box below as a fallback.
      </div>
      <details style="margin-top:14px;">
        <summary style="cursor:pointer;font-size:10.5px;letter-spacing:0.18em;text-transform:uppercase;color:var(--text-mute);">or paste lab text directly</summary>
        <textarea class="m-paste" id="pdf-paste" rows="8" placeholder="Paste lab text here…" style="margin-top:10px;"></textarea>
        <button class="m-save" id="pdf-extract" style="margin-top:0;">extract from pasted text →</button>
      </details>
    </div>
    <div class="m-pane" id="pane-genetics">
      <div class="m-drop" id="g-drop">
        <input type="file" id="g-file" style="display:none" accept=".txt,.csv,.vcf,.tsv" />
        <div class="m-drop-title">Drop your raw DNA file or click to choose</div>
        <div class="m-drop-sub">23andMe · AncestryDNA · MyHeritage · VCF</div>
      </div>
      <div class="m-status" id="g-status"></div>
      <div class="m-help">
        Raw genotype file (the big .txt file from your DNA-test provider, not the report PDF — for PDF reports use the Lab PDF tab). On 23andMe: Settings → Browse Raw Data → Download. On AncestryDNA: Settings → DNA → Download Raw DNA Data.
      </div>
      <button class="m-clear" id="g-clear" style="margin-left:0;display:none;">clear my genetics</button>
    </div>
    <div class="m-pane" id="pane-bloodwork">
      <div class="m-help">
        Type values from your most recent lab work. Skip what you don't have. The graph lights up matching biomarker nodes and the phenotypes they stratify. Values outside reference range are color-flagged.
      </div>
      <div class="m-form-grid" id="bw-form"></div>
      <button class="m-save" id="bw-save">save &amp; generate my report</button>
      <button class="m-clear" id="bw-clear">clear</button>
    </div>
    <!-- "generating your report" intermediate state, shown for ~1.5s after save -->
    <div class="m-generating" id="m-generating">
      <div>Reading your data against the atlas…</div>
      <div class="m-gen-dots" style="margin-top:16px;"><span></span><span></span><span></span></div>
    </div>
  </div>
</div>

<!-- View-report button (top-center, replaces "your data" line when data exists) -->
<button class="view-report" id="view-report"><span class="dot"></span>View your report</button>

<!-- ── PERSONALIZED REPORT OVERLAY ─────────────────────────────────── -->
<div class="report-overlay" id="report-overlay">
  <div class="report">
    <button class="r-close" id="r-close">×</button>
    <div class="r-header">
      <div class="r-eyebrow">Causes Atlas · your child's map</div>
      <div class="r-title" id="r-title">Your data, read against the atlas</div>
      <div class="r-sub" id="r-sub">Generated · just now</div>
    </div>

    <!-- TOP-OF-REPORT EXECUTIVE SYNTHESIS — clusters, top actions, top tests, what to avoid -->
    <div class="r-synth" id="r-synth" style="display:none;">
      <div class="r-synth-eyebrow">Top findings · prioritized</div>
      <div class="r-synth-headline" id="r-synth-headline"></div>

      <div class="r-synth-section">
        <div class="r-synth-label">Top 5 actions, prioritized</div>
        <div id="r-synth-actions"></div>
      </div>

      <div class="r-synth-section">
        <div class="r-synth-label">Gene clusters · highest load first</div>
        <div id="r-synth-clusters"></div>
      </div>

      <div class="r-synth-section">
        <div class="r-synth-label">Top 5 tests to order next</div>
        <div id="r-synth-tests"></div>
      </div>

      <div class="r-synth-section">
        <div class="r-synth-label">What to avoid · safety filters</div>
        <ul class="r-synth-avoid" id="r-synth-avoid"></ul>
      </div>

      <div class="r-synth-sources" id="r-synth-sources"></div>
    </div>

    <div class="r-section">
      <div class="r-section-label">Your data</div>
      <div class="r-summary" id="r-summary"></div>
    </div>

    <div class="r-section">
      <div class="r-section-label">Best phenotype matches</div>
      <div id="r-phenotypes"></div>
    </div>

    <div class="r-section" id="r-section-variants" style="display:none;">
      <div class="r-section-label">Your gene variants · full detail</div>
      <button class="r-collapse-toggle" id="r-variants-toggle">Show all variants (detail view)</button>
      <div id="r-variants" class="r-collapsed"></div>
    </div>

    <div class="r-section" id="r-section-oor">
      <div class="r-section-label">Out of optimal range</div>
      <div id="r-oor"></div>
    </div>

    <div class="r-section">
      <div class="r-section-label">What to discuss with your functional medicine doctor</div>
      <div id="r-actions"></div>
    </div>

    <div class="r-section">
      <div class="r-section-label">Tests to consider next</div>
      <div id="r-tests"></div>
    </div>

    <div class="r-disclaimer">
      <strong>Important:</strong> this map is generated by an evidence-weighted inference engine reading atlas data against the values you uploaded. It is not medical advice. The patterns are real; the action plan should be discussed with a functional medicine practitioner familiar with your child's full clinical history. <strong>INT-0001 Leucovorin CSRS 83.35</strong> is the atlas calibration anchor and has not drifted across major revisions.
    </div>

    <div class="r-footer">
      <button class="r-btn primary" id="r-obsidian">Download Obsidian profile (.md)</button>
      <button class="r-btn" id="r-graph">View on graph</button>
      <button class="r-btn" id="r-download">Print / save as PDF</button>
      <button class="r-btn" id="r-reupload">Re-upload labs</button>
    </div>
  </div>
</div>

<!-- FM-actionable card: bottom-center reveal on phenotype-click -->
<div class="action-card" id="ac"></div>

<!-- LEFT START-HERE DOCK: always-visible action surface for high-agency moms -->
<div class="start-dock" id="sd">
  <div class="sd-intro-block">
    <div class="sd-welcome">Your child's map.</div>
    <div class="sd-tag">An evidence-based second opinion — built one child at a time, not from population averages.</div>
  </div>
  <div class="sd-section">
    <div class="sd-label">Types of autism</div>
    <div id="sd-types"></div>
  </div>
  <div class="sd-section">
    <div class="sd-label">Must-have tests · autism-specific</div>
    <div id="sd-musthave"></div>
  </div>
  <div class="sd-section">
    <div class="sd-label">Epigenetic methylation</div>
    <div id="sd-epigenetic"></div>
  </div>
  <div class="sd-section">
    <div class="sd-label">Universal foundation</div>
    <div id="sd-foundation"></div>
  </div>
  <div class="sd-section">
    <div class="sd-label">High-end · full workup</div>
    <div id="sd-highend"></div>
  </div>
  <div class="sd-section">
    <div class="sd-label">Budget entry</div>
    <div id="sd-budget"></div>
  </div>
  <div class="sd-section">
    <div class="sd-label">Today's literature</div>
    <div id="sd-feed"></div>
  </div>
  <div class="sd-section">
    <div class="sd-label">Functional medicine</div>
    <div id="sd-resources"></div>
  </div>
  <div class="sd-footer">
    <a href="TESTING_STRATEGY.md" target="_blank">full strategy →</a>
    &nbsp;·&nbsp; 11 types · 50 tests · daily feed
  </div>
</div>

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
const STARTERS = __STARTERS__;        // curated must-have/high-end/budget + foundation + types + resources
const VAULT_PATHS = __VAULT_PATHS__;  // atlas_id → canonical Obsidian filename stem

// ── canvas + DPR ───────────────────────────────────────────────────
const canvas = document.getElementById('c');
const ctx = canvas.getContext('2d');

// Guard createRadialGradient against non-finite values. d3-force can
// transiently emit NaN positions while the simulation is settling, and
// 1/scale can blow up if scale ever reaches 0 during a pinch-zoom. Any
// of those propagating to a gradient throws a hard browser error and
// kills the render loop. Replace bad inputs with a no-op gradient.
(function () {
  const _orig = ctx.createRadialGradient.bind(ctx);
  ctx.createRadialGradient = function (x0, y0, r0, x1, y1, r1) {
    if (!Number.isFinite(x0) || !Number.isFinite(y0) || !Number.isFinite(r0) ||
        !Number.isFinite(x1) || !Number.isFinite(y1) || !Number.isFinite(r1) ||
        r0 < 0 || r1 < 0) {
      return _orig(0, 0, 0, 0, 0, 1);
    }
    return _orig(x0, y0, r0, x1, y1, r1);
  };
  const _origLin = ctx.createLinearGradient.bind(ctx);
  ctx.createLinearGradient = function (x0, y0, x1, y1) {
    if (!Number.isFinite(x0) || !Number.isFinite(y0) ||
        !Number.isFinite(x1) || !Number.isFinite(y1)) {
      return _origLin(0, 0, 1, 0);
    }
    return _origLin(x0, y0, x1, y1);
  };
})();
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

// ── TEST-CLICK ACTION CARD ───────────────────────────────────────────
// When mom clicks a test (either on the map or in the left dock), render
// a test-centric action card: what the test is, what results indicate,
// and the SPECIFIC interventions / combinations / lifestyle items linked
// to that test. The actionable bridge from "ordered a test" → "got result"
// → "now what do I actually DO." This is the high-agency-mom path.
function renderActionCardForTest(test) {
  if (!test) { acEl.classList.remove('on'); return; }
  const dtcPill = test.dtc
    ? '<span class="pill gold">direct-to-consumer</span>'
    : (test.rx ? '<span class="pill">rx required</span>' : '');
  const tierPill = test.tr ? '<span class="pill">' + test.tr + '</span>' : '';
  const cost = test.cl
    ? '$' + test.cl + (test.ch && test.ch !== test.cl ? '–' + test.ch : '')
    : 'cost varies';
  const provider = test.pr || 'multiple providers';
  const sample = test.sm || '';
  const turnaround = test.td ? test.td + ' days' : '';
  const wm = test.wm || '';
  const wr = test.wr || '';

  // Mapped interventions: walk node.mi for direct test→intervention
  // links, plus walk test→phenotype→intervention as fallback if direct
  // list is sparse.
  const ints = [];
  const seenInts = new Set();
  if (test.mi && test.mi.length) {
    for (const iid of test.mi) {
      const i = nodes.find(n => n.id === iid);
      if (i && !seenInts.has(i.id)) { ints.push(i); seenInts.add(i.id); }
    }
  }
  // Fallback: walk test→phenotype→intervention if direct map is thin
  if (ints.length < 3) {
    for (const l of links) {
      if (l.source.id !== test.id && l.target.id !== test.id) continue;
      const other = (l.source.id === test.id) ? l.target : l.source;
      if (other.t !== 'P') continue;
      for (const l2 of links) {
        const isLinkToPhe = (l2.target.id === other.id || l2.source.id === other.id);
        if (!isLinkToPhe) continue;
        const candidate = (l2.source.id === other.id) ? l2.target : l2.source;
        if (candidate.t === 'I' && !seenInts.has(candidate.id)) {
          ints.push(candidate);
          seenInts.add(candidate.id);
        }
        if (ints.length >= 5) break;
      }
      if (ints.length >= 5) break;
    }
  }
  ints.sort((a, b) => b.s - a.s);
  const topInts = ints.slice(0, 4);

  // Universal foundation (always-applies regardless of result)
  const foundationIds = STARTERS.foundation || [];
  const foundationNodes = foundationIds
    .map(id => nodes.find(n => n.id === id))
    .filter(Boolean);

  let interventionsHtml = '';
  for (const i of topInts) {
    const dose = i.do ? '<span class="meta">' + i.do + '</span>' : '';
    const cst = i.co ? '<span class="meta">$' + i.co + '/mo</span>' : '';
    const rg = i.rg ? '<span class="pill">' + i.rg + '</span>' : '';
    const c  = i.c  ? '<span class="pill">' + i.c + '</span>' : '';
    interventionsHtml += '<div class="item"><strong>' + i.l + '</strong>' +
                         rg + c + (dose ? ' ' + dose : '') +
                         (cst ? ' ' + cst : '') + '</div>';
  }
  if (!interventionsHtml) {
    interventionsHtml = '<div class="meta">No direct intervention mapping; ' +
                        'see phenotype-specific action cards via the map.</div>';
  }

  let foundationHtml = '';
  for (const f of foundationNodes.slice(0, 3)) {
    foundationHtml += '<div class="item"><strong>' + f.l + '</strong>' +
                      (f.co ? '<span class="meta">$' + f.co + '/mo</span>' : '') +
                      '</div>';
  }

  const html = '' +
    '<button class="ac-close" onclick="clearReveal();">×</button>' +
    '<div class="ac-head">' +
      '<div class="ac-name">' + test.l + '</div>' +
      '<div class="ac-id">' + test.id + ' · test panel</div>' +
    '</div>' +
    '<div class="ac-pe">' +
      provider + ' · ' + sample + ' · ' + cost +
      (turnaround ? ' · ' + turnaround : '') +
      '  ' + dtcPill + tierPill +
      // Collection mode badge — at-home / hybrid / clinic
      (test.cm === 'at-home'
        ? '<span class="pill gold" style="margin-left:6px;">at-home</span>'
        : test.cm === 'hybrid'
          ? '<span class="pill gold" style="margin-left:6px;">at-home option</span>'
          : '<span class="pill" style="margin-left:6px;">clinic draw</span>') +
    '</div>' +
    // Action row — ORDER + BILL links. The actionable bridge from
    // "I see this test" to "I'm ordering it now."
    renderOrderRow(test) +
    (wm ? '<div class="ac-row">' +
      '<div class="ac-label">Measures</div>' +
      '<div class="ac-content">' + wm + '</div>' +
    '</div>' : '') +
    (wr ? '<div class="ac-row">' +
      '<div class="ac-label">Results mean</div>' +
      '<div class="ac-content">' + wr + '</div>' +
    '</div>' : '') +
    '<div class="ac-row">' +
      '<div class="ac-label">If positive · do</div>' +
      '<div class="ac-content">' + interventionsHtml + '</div>' +
    '</div>' +
    (foundationHtml ? '<div class="ac-row">' +
      '<div class="ac-label">Always · regardless</div>' +
      '<div class="ac-content">' + foundationHtml + '</div>' +
    '</div>' : '') +
    renderBillingRow(test) +
    '<div class="ac-footer">' +
      '<a href="TESTING_STRATEGY.md" target="_blank" ' +
      'style="color:var(--gold);text-decoration:none;letter-spacing:0.14em;">' +
      'full testing strategy →</a>' +
      ' &nbsp; <a href="BILLING_STRATEGY.md" target="_blank" ' +
      'style="color:var(--gold);text-decoration:none;letter-spacing:0.14em;">' +
      'billing strategy →</a>' +
      ' &nbsp;·&nbsp; ' +
      'not medical advice. discuss with a functional / integrative ' +
      'pediatrics clinician before acting.' +
    '</div>';

  acEl.innerHTML = html;
  acEl.classList.add('on');
  // Mark this as a test-reveal so the existing clearReveal() works.
  revealedPhenotype = test;
  revealedSet = new Set([test.id, ...topInts.map(n => n.id),
                                  ...foundationNodes.slice(0,3).map(n => n.id)]);
}

// Helper: render the action row — ORDER button + BILL-via-insurance link.
// Makes the test card fully transactional: see it, order it, bill it.
function renderOrderRow(test) {
  const orderUrl = test.or || '';
  const ins = (test.ins || '').toLowerCase();
  const cpt = test.cpt || '';
  const insuranceFriendly = ins.indexOf('covered') >= 0 &&
                            ins.indexOf('never') < 0 &&
                            ins.indexOf('rarely') < 0;
  let html = '<div class="ac-row">' +
    '<div class="ac-label">Get it</div>' +
    '<div class="ac-content" style="display:flex;flex-wrap:wrap;gap:8px;">';
  if (orderUrl) {
    const ctaLabel = test.dtc ? 'order direct →' : 'provider page →';
    html += '<a href="' + orderUrl + '" target="_blank" rel="noopener" ' +
            'style="display:inline-block;padding:7px 14px;' +
            'background:var(--gold);color:var(--void);' +
            'font-family:ui-monospace,monospace;font-size:10.5px;' +
            'letter-spacing:0.18em;text-transform:uppercase;' +
            'text-decoration:none;border-radius:2px;">' + ctaLabel + '</a>';
  }
  if (insuranceFriendly && cpt) {
    html += '<a href="BILLING_STRATEGY.md" target="_blank" rel="noopener" ' +
            'style="display:inline-block;padding:7px 14px;' +
            'background:transparent;border:1px solid var(--gold-dim);' +
            'color:var(--gold);font-family:ui-monospace,monospace;' +
            'font-size:10.5px;letter-spacing:0.18em;text-transform:uppercase;' +
            'text-decoration:none;border-radius:2px;">' +
            'bill via insurance →</a>';
  }
  if ((test.hsa || '').toLowerCase().startsWith('yes')) {
    html += '<a href="BILLING_STRATEGY.md#path-2-hsa-fsa" target="_blank" ' +
            'rel="noopener" style="display:inline-block;padding:7px 14px;' +
            'background:transparent;border:1px solid var(--gold-dim);' +
            'color:var(--gold);font-family:ui-monospace,monospace;' +
            'font-size:10.5px;letter-spacing:0.18em;text-transform:uppercase;' +
            'text-decoration:none;border-radius:2px;">' +
            'pay with HSA/FSA →</a>';
  }
  html += '</div></div>';
  return html;
}

// Helper: render the insurance/HSA-FSA billing row for a test action card.
// Honest framing — for most FM-autism tests insurance is "rarely_covered";
// HSA/FSA with Letter of Medical Necessity is the scalable path.
function renderBillingRow(test) {
  const cpt = test.cpt || '';
  const icd = test.icd || '';
  const ins = (test.ins || '').toLowerCase();
  const pa  = test.pa || '';
  const hsa = (test.hsa || '').toLowerCase();
  if (!cpt && !icd && !ins) return '';

  const insLabel = {
    'always_covered':   '<span class="pill gold">covered</span>',
    'usually_covered':  '<span class="pill gold">usually covered</span>',
    'sometimes_covered':'<span class="pill">sometimes covered</span>',
    'rarely_covered':   '<span class="pill">rarely covered</span>',
    'never_covered':    '<span class="pill">never covered</span>',
  }[ins] || '';
  const hsaLabel = (hsa === 'yes' || hsa === 'yes_with_lmn')
    ? '<span class="pill gold">HSA/FSA</span>' : '';

  const billStr = [];
  if (cpt) billStr.push('CPT&nbsp;' + cpt);
  if (icd) billStr.push('ICD-10&nbsp;' + icd);
  if (pa && pa !== 'no') billStr.push('prior auth ' + pa);

  return '<div class="ac-row">' +
    '<div class="ac-label">Insurance</div>' +
    '<div class="ac-content">' +
      insLabel + hsaLabel +
      (billStr.length ? '<div class="meta" style="margin-top:6px;display:block;">' +
                         billStr.join(' · ') + '</div>' : '') +
      (test.cn ? '<div class="meta" style="margin-top:4px;display:block;">' +
                 test.cn + '</div>' : '') +
    '</div>' +
  '</div>';
}

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
  } else if (best && best.t === 'T') {
    // Click a test node on the map → open test action card (interventions,
    // foundation, what-to-do-with-result)
    if (revealedPhenotype && revealedPhenotype.id === best.id) {
      clearReveal();
    } else {
      renderActionCardForTest(best);
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
    toggle.textContent = 'see an example';
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
    toggle.textContent = 'see an example';
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
    toggle.textContent = 'see an example';
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

    // user-data ring — any gene or biomarker the family has uploaded.
    // Always rendered at full strength regardless of filter so mom can
    // visually find "her child's nodes" anywhere on the map.
    if (window.userMatchedIds && window.userMatchedIds.has(n.id)) {
      ctx.strokeStyle = `rgba(232,196,110,0.95)`;
      ctx.lineWidth = 1.4/scale;
      ctx.beginPath();
      ctx.arc(n.x, n.y, n.s + 3.2, 0, Math.PI*2);
      ctx.stroke();
      // soft halo
      const halo = ctx.createRadialGradient(n.x, n.y, n.s + 2, n.x, n.y, n.s + 9);
      halo.addColorStop(0, 'rgba(232,196,110,0.32)');
      halo.addColorStop(1, 'rgba(232,196,110,0)');
      ctx.fillStyle = halo;
      ctx.beginPath(); ctx.arc(n.x, n.y, n.s + 9, 0, Math.PI*2); ctx.fill();
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

// ── RETENTION via localStorage ───────────────────────────────────────
// Daily-return metric is the primary measure of consumer-surface success
// (per CLAUDE.md). The substrate updates daily — the intake feed brings
// 30-40 new papers, Δ² shifts trajectory weights, combinations get
// promoted. The retention layer makes mom AWARE of that motion when she
// returns. localStorage stores: last_visit timestamp, count of papers
// she last saw, set of tests she's marked "ordered" or "result-in".
(function() {
  if (typeof localStorage === 'undefined') return;
  const NS = 'causes_atlas_v1.';
  const now = Date.now();
  const lastVisit = parseInt(localStorage.getItem(NS + 'last_visit') || '0', 10);
  const lastFeedCount = parseInt(localStorage.getItem(NS + 'last_feed') || '0', 10);
  const currentFeedCount = (INTAKE && INTAKE.candidates) ? INTAKE.candidates.length : 0;

  // First-visit banner suppressed; only show on day-2+ return
  if (lastVisit && now - lastVisit > 60 * 60 * 1000) {
    const daysSince = Math.max(1, Math.floor((now - lastVisit) / (24 * 60 * 60 * 1000)));
    const newPapers = Math.max(0, currentFeedCount - lastFeedCount);
    const banner = document.createElement('div');
    banner.style.cssText =
      'position:fixed; top:78px; left:30px; z-index:11; ' +
      'background:rgba(8,11,18,0.92); backdrop-filter:blur(8px); ' +
      'border:1px solid var(--gold-dim); padding:10px 16px; ' +
      'font-family:ui-serif,Garamond,serif; font-size:12px; ' +
      'color:var(--text); max-width:300px; line-height:1.5; ' +
      'opacity:0; transition:opacity 1200ms ease 600ms; ' +
      'pointer-events:auto;';
    const dayLabel = daysSince === 1 ? '1 day' : daysSince + ' days';
    const paperLabel = newPapers === 0 ? 'no new papers'
                     : newPapers === 1 ? '1 new paper'
                     : newPapers + ' new papers';
    banner.innerHTML =
      '<div style="color:var(--gold);font-family:ui-monospace,monospace;' +
      'font-size:9.5px;letter-spacing:0.22em;text-transform:uppercase;' +
      'margin-bottom:4px;">Welcome back</div>' +
      'Last visit: ' + dayLabel + ' ago.<br>' +
      paperLabel + ' since.<br>' +
      '<span style="color:var(--text-mute);font-size:11px;">' +
      'The substrate is doing daily work. Check today\'s literature ' +
      'in the dock.</span>';
    document.body.appendChild(banner);
    requestAnimationFrame(() => { banner.style.opacity = '1'; });
    setTimeout(() => {
      banner.style.opacity = '0';
      setTimeout(() => banner.remove(), 1500);
    }, 9000);
  }

  // Update on every visit so daily-return tracking works
  localStorage.setItem(NS + 'last_visit', String(now));
  localStorage.setItem(NS + 'last_feed', String(currentFeedCount));

  // Expose helpers for clicking "I ordered" / "Result in" on test cards
  // (UI for these is future work; the storage layer is ready)
  window.markTestOrdered = function(testId) {
    const key = NS + 'test_ordered_' + testId;
    localStorage.setItem(key, String(Date.now()));
  };
  window.markResultIn = function(testId) {
    const key = NS + 'test_result_' + testId;
    localStorage.setItem(key, String(Date.now()));
  };
  window.getTestStatus = function(testId) {
    return {
      ordered: parseInt(localStorage.getItem(NS + 'test_ordered_' + testId) || '0', 10),
      result_in: parseInt(localStorage.getItem(NS + 'test_result_' + testId) || '0', 10),
    };
  };
})();

// ── START-HERE LEFT DOCK ─────────────────────────────────────────────
// Always-visible action surface. Curated sections in priority order:
// (1) Types of autism — click any to open its action card
// (2) Must-have tests — the 5 panels every FM doc orders first
// (3) Universal foundation — 5 interventions that cross all phenotypes
// (4) High-end full workup — for moms who can afford the premium tier
// (5) Budget entry — DTC affordable starting point
// (6) Today's literature — daily-refreshed PubMed scanner output
// (7) Functional medicine resources — MAPS / ARI / Walsh
(function() {
  // Helper: focus the map on a node (pan + zoom + pulse it)
  function focusNode(id) {
    const node = nodes.find(x => x.id === id);
    if (!node) return;
    targetOx = -node.x * scale;
    targetOy = -node.y * scale;
    targetScale = 1.8;
    pulses.push({node: node, t: 0, dur: 2.2});
  }

  // Helper: render a list of test nodes into a container.
  // Click → pan to the test on the map + open its action card showing
  // what to do with the result.
  function renderTestList(containerId, ids) {
    const container = document.getElementById(containerId);
    if (!container) return;
    for (const tid of ids) {
      const t = DATA.nodes.find(n => n.id === tid);
      if (!t) continue;
      const dtcPill = t.dtc ? '<span class="sd-pill gold">DTC</span>' :
                      (t.rx ? '<span class="sd-pill">Rx</span>' : '');
      const tierPill = t.tr ? '<span class="sd-pill">' + t.tr + '</span>' : '';
      const homePill = t.cm === 'at-home'
        ? '<span class="sd-pill gold">at-home</span>'
        : t.cm === 'hybrid'
          ? '<span class="sd-pill">at-home option</span>'
          : '';
      const cost = t.cl
        ? '$' + t.cl + (t.ch && t.ch !== t.cl ? '-' + t.ch : '')
        : '';
      const meta = [t.pr, t.sm, cost, t.td ? t.td + 'd' : '']
                   .filter(Boolean).join(' · ');
      const item = document.createElement('div');
      item.className = 'sd-test';
      item.innerHTML =
        '<div class="sd-test-name">' + t.l + homePill + dtcPill + tierPill + '</div>' +
        '<span class="sd-test-meta">' + meta + '</span>';
      item.addEventListener('click', () => {
        focusNode(t.id);
        const liveNode = nodes.find(n => n.id === t.id);
        setTimeout(() => renderActionCardForTest(liveNode || t), 320);
      });
      container.appendChild(item);
    }
  }

  // (1) Types of autism — clickable list opens phenotype action card
  const typesEl = document.getElementById('sd-types');
  if (typesEl) {
    for (const pid of STARTERS.types) {
      const phe = DATA.nodes.find(n => n.id === pid.id);
      if (!phe) continue;
      const item = document.createElement('div');
      item.className = 'sd-test';
      item.innerHTML = '<div class="sd-test-name">' + pid.label + '</div>' +
                       '<span class="sd-test-meta">' + pid.id + '</span>';
      item.addEventListener('click', () => {
        // Pan to phenotype + open action card
        focusNode(pid.id);
        // Defer reveal so the pan completes first
        setTimeout(() => revealForPhenotype(phe), 320);
      });
      typesEl.appendChild(item);
    }
  }

  // (2) Must-have tests — autism-specific
  renderTestList('sd-musthave', STARTERS.must_have);

  // (2b) Epigenetic methylation
  renderTestList('sd-epigenetic', STARTERS.epigenetic);

  // (3) Universal foundation — interventions across all phenotypes
  const foundEl = document.getElementById('sd-foundation');
  if (foundEl) {
    for (const iid of STARTERS.foundation) {
      const i = DATA.nodes.find(n => n.id === iid);
      if (!i) continue;
      const dosePill = i.rg ? '<span class="sd-pill">' + i.rg + '</span>' : '';
      const cost = i.co ? '$' + i.co + '/mo' : '';
      const meta = [i.c, i.do, cost].filter(Boolean).join(' · ');
      const item = document.createElement('div');
      item.className = 'sd-test';
      item.innerHTML =
        '<div class="sd-test-name">' + i.l + dosePill + '</div>' +
        '<span class="sd-test-meta">' + meta + '</span>';
      item.addEventListener('click', () => focusNode(i.id));
      foundEl.appendChild(item);
    }
  }

  // (4) High-end full workup
  renderTestList('sd-highend', STARTERS.high_end);

  // (5) Budget entry
  renderTestList('sd-budget', STARTERS.budget);

  // (6) Today's literature feed
  const sdFeed = document.getElementById('sd-feed');
  if (sdFeed) {
    if (INTAKE && INTAKE.candidates && INTAKE.candidates.length) {
      const tagLabels = {
        'P': 'predisposition', 'E': 'exposure', 'M': 'mechanism',
        'PHI': 'phenotype', 'SYNTHESIS': 'RCT/meta',
      };
      for (const c of INTAKE.candidates.slice(0, 5)) {
        const tagShort = (c.intake_tag || '?').substring(0, 3);
        const tagFull = tagLabels[c.intake_tag] || c.intake_tag;
        const item = document.createElement('div');
        item.className = 'sd-feed';
        item.innerHTML =
          '<span class="sd-feed-tag" title="' + tagFull + '">' +
          '[' + tagShort + ']' + '</span>' +
          (c.title || '').substring(0, 80) +
          (c.first_author ? ' <span style="color:var(--text-vmute);">· ' +
                            c.first_author + '</span>' : '');
        sdFeed.appendChild(item);
      }
    } else {
      sdFeed.innerHTML = '<div class="sd-feed">' +
        '<span class="sd-feed-tag">[ — ]</span>' +
        'Intake feed refreshing. Daily scan runs at 07:00 UTC.</div>';
    }
  }

  // (7) FM resources — external links to credible canon
  const sdRes = document.getElementById('sd-resources');
  if (sdRes && STARTERS.resources) {
    for (const r of STARTERS.resources) {
      const tierPill = r.tier ? '<span class="sd-pill">' + r.tier + '</span>' : '';
      const item = document.createElement('div');
      item.className = 'sd-test';
      item.innerHTML =
        '<div class="sd-test-name">' +
        '<a href="' + r.url + '" target="_blank" rel="noopener" ' +
        'style="color:var(--text);text-decoration:none;">' + r.name + '</a>' +
        tierPill + '</div>' +
        '<span class="sd-test-meta">' + r.what + '</span>';
      sdRes.appendChild(item);
    }
  }
})();

// ── DATA UPLOAD + MOBILE TOUCH ──────────────────────────────────────
// Client-side genetics + blood work upload. Files never leave the
// browser. Stored in localStorage. Matched gene + biomarker nodes get
// a persistent gold ring on the map regardless of active filter.
(function setupUpload() {
  'use strict';

  // gene_symbol → node_id lookup
  const geneByLabel = {};
  for (const n of nodes) {
    if (n.t === 'G' && n.l) geneByLabel[n.l.toUpperCase()] = n.id;
  }
  // biomarker_label (lowercased) → node_id lookup
  const bioByLabel = {};
  for (const n of nodes) {
    if (n.t === 'B' && n.l) bioByLabel[n.l.toLowerCase()] = n.id;
  }

  // Curated biomarker form fields. Each label is matched against the
  // atlas biomarker layer with aliases. Reference ranges follow the
  // optimal-range conventions from the biomarkers.csv where available.
  const BIOMARKER_FIELDS = [
    { k:'vitd25', l:'25-OH Vitamin D', u:'ng/mL', rL:30, rH:80,
      a:['25-hydroxy','vitamin d','25-OH','25(OH)D','vitamin d, 25']},
    { k:'ferritin', l:'Ferritin', u:'ng/mL', rL:30, rH:200, a:['ferritin']},
    { k:'homocysteine', l:'Homocysteine', u:'μmol/L', rL:4, rH:8, a:['homocysteine']},
    { k:'mma', l:'Methylmalonic acid', u:'nmol/L', rL:0, rH:270, a:['methylmalonic','MMA']},
    { k:'b12', l:'Vitamin B12', u:'pg/mL', rL:500, rH:1200, a:['B12','cobalamin']},
    { k:'folate_rbc', l:'RBC Folate', u:'ng/mL', rL:400, rH:800, a:['RBC folate','red cell folate']},
    { k:'tsh', l:'TSH', u:'mIU/L', rL:0.5, rH:2.5, a:['TSH','thyroid stimulating']},
    { k:'ft4', l:'Free T4', u:'ng/dL', rL:1.0, rH:1.5, a:['free T4','FT4']},
    { k:'ft3', l:'Free T3', u:'pg/mL', rL:3.0, rH:4.5, a:['free T3','FT3']},
    { k:'zinc', l:'Zinc, plasma', u:'μg/dL', rL:70, rH:110, a:['zinc']},
    { k:'copper', l:'Copper, plasma', u:'μg/dL', rL:70, rH:140, a:['copper']},
    { k:'ceruloplasmin', l:'Ceruloplasmin', u:'mg/dL', rL:20, rH:35, a:['ceruloplasmin']},
    { k:'mag_rbc', l:'Magnesium, RBC', u:'mg/dL', rL:4.2, rH:6.8, a:['magnesium RBC','red cell magnesium']},
    { k:'lactate', l:'Lactate', u:'mmol/L', rL:0.5, rH:2.0, a:['lactate','lactic acid']},
    { k:'pyruvate', l:'Pyruvate', u:'mg/dL', rL:0.3, rH:0.9, a:['pyruvate']},
    { k:'ammonia', l:'Ammonia', u:'μmol/L', rL:15, rH:45, a:['ammonia']},
    { k:'igg', l:'Immunoglobulin G', u:'mg/dL', rL:700, rH:1600, a:['IgG','immunoglobulin G']},
    { k:'iga', l:'Immunoglobulin A', u:'mg/dL', rL:70, rH:400, a:['IgA','immunoglobulin A']},
    { k:'igm', l:'Immunoglobulin M', u:'mg/dL', rL:40, rH:230, a:['IgM','immunoglobulin M']},
    { k:'crp', l:'hs-CRP', u:'mg/L', rL:0, rH:1.0, a:['hs-CRP','C-reactive','CRP']},
    { k:'igf1', l:'IGF-1', u:'ng/mL', rL:90, rH:280, a:['IGF-1','IGF1','somatomedin']},
    { k:'cortisol_am', l:'Cortisol (AM serum)', u:'μg/dL', rL:8, rH:22, a:['cortisol','AM cortisol']},
    { k:'glucose_f', l:'Fasting glucose', u:'mg/dL', rL:70, rH:99, a:['glucose','fasting glucose']},
    { k:'insulin_f', l:'Fasting insulin', u:'μIU/mL', rL:2, rH:10, a:['insulin']},
    { k:'hba1c', l:'HbA1c', u:'%', rL:4.5, rH:5.6, a:['HbA1c','hemoglobin A1c','A1c']},
    { k:'lead', l:'Lead, blood', u:'μg/dL', rL:0, rH:3.5, a:['lead','Pb']},
    { k:'mercury', l:'Mercury, blood', u:'μg/L', rL:0, rH:5, a:['mercury','Hg']},
    { k:'arsenic', l:'Arsenic', u:'μg/L', rL:0, rH:50, a:['arsenic']},
    { k:'tryptase', l:'Tryptase', u:'ng/mL', rL:0, rH:11, a:['tryptase']},
    { k:'fraa_block', l:'FRAA blocking', u:'units', rL:0, rH:0.21, a:['FRAA blocking','folate receptor blocking']},
    { k:'fraa_bind', l:'FRAA binding', u:'pmol', rL:0, rH:0.5, a:['FRAA binding','folate receptor binding']},
    { k:'sam', l:'S-adenosylmethionine', u:'nmol/L', rL:70, rH:125, a:['SAM','adenosylmethionine']},
    { k:'sah', l:'S-adenosylhomocysteine', u:'nmol/L', rL:10, rH:30, a:['SAH','adenosylhomocysteine']},
    { k:'gsh_gssg', l:'GSH/GSSG ratio', u:'', rL:10, rH:100, a:['GSH/GSSG','glutathione ratio']},
    { k:'ldl', l:'LDL cholesterol', u:'mg/dL', rL:0, rH:100, a:['LDL','low density']},
    { k:'hdl', l:'HDL cholesterol', u:'mg/dL', rL:40, rH:100, a:['HDL','high density']},
    { k:'trig', l:'Triglycerides', u:'mg/dL', rL:0, rH:150, a:['triglycerides']},
    { k:'ast', l:'AST', u:'U/L', rL:10, rH:40, a:['AST','aspartate']},
    { k:'alt', l:'ALT', u:'U/L', rL:7, rH:40, a:['ALT','alanine']},
    { k:'wbc', l:'WBC', u:'×10³/μL', rL:4.5, rH:11, a:['WBC','white blood']}
  ];

  // ── VARIANT KNOWLEDGE BASE ────────────────────────────────────
  // Per-variant, per-genotype interpretation curated from clinical
  // genetics / functional medicine literature. Genotype letters are
  // sorted alphabetically before lookup (so "TC" is queried as "CT").
  // Severity: 0 = wild type, 1 = heterozygous mild, 2 = homozygous
  // significant, 3 = compound/high-impact.
  // do = consider · av = avoid · li = lifestyle · ai = atlas intervention IDs
  // to weight up in ranking.
  const VARIANT_DB = {
    'rs1801133': { g:'MTHFR', n:'C677T (A222V)', r:'Folate-cycle methylation',
      e: {
        CC: { f:'wild', sev:0, msg:'Normal enzyme activity' },
        CT: { f:'het',  sev:1, msg:'~35% reduced enzyme activity',
              d:'Mild folate-cycle impairment under stress, alcohol, or low B-vitamin intake.',
              do:['Methylfolate (5-MTHF) over folic acid','Methyl-B12'],
              av:['High-dose synthetic folic acid'],
              li:['Daily leafy greens','Limit alcohol','Monitor homocysteine'],
              ai:['INT-0001','INT-0008'] },
        TT: { f:'hom',  sev:2, msg:'~70% reduced enzyme activity',
              d:'Substantially impaired methylation. Homocysteine often elevated; B12 cycle strained.',
              do:['Methylfolate at therapeutic dose','Methyl-B12 sublingual or sub-Q','TMG (trimethylglycine) backup'],
              av:['Folic acid in any supplement','High alcohol intake'],
              li:['Heavy emphasis on leafy greens','Monitor homocysteine 6-month','Stress is methylation-draining'],
              ai:['INT-0001','INT-0008'] }
      } },
    'rs1801131': { g:'MTHFR', n:'A1298C (E429A)', r:'Folate cycle (BH4 branch)',
      e: {
        AA: { f:'wild', sev:0, msg:'Normal activity' },
        AC: { f:'het',  sev:1, msg:'~15–20% reduced activity',
              d:'Affects BH4 regeneration → may impact neurotransmitter synthesis and nitric oxide.',
              do:['Methylfolate (5-MTHF) 400–800 mcg standard','BH4 cofactor support (folate + B-vitamins)'],
              li:['Mood and dopamine stability with green vegetables']},
        CC: { f:'hom',  sev:2, msg:'~30–40% reduced activity (estimates vary by study)',
              d:'BH4 cycle impacted. Compound C677T+/A1298C+ heterozygote = 50–60% reduction.',
              do:['Methylfolate 400–800 mcg standard; 1–5 mg under clinician care if compound-het','Consider BH4 cofactor support under FM guidance'],
              av:['Synthetic folic acid in supplements'],
              li:['Adequate magnesium and B6','Stress management']}
      } },
    'rs1805087': { g:'MTR', n:'A2756G (D919G)', r:'Methionine synthase · B12 utilization',
      e: {
        AA: { f:'wild', sev:0, msg:'Normal activity' },
        AG: { f:'het',  sev:1, msg:'Mildly reduced methionine synthesis',
              d:'Slower B12-dependent recycling of homocysteine to methionine.',
              do:['Methylcobalamin (methyl-B12) preferentially'],
              li:['B12-rich foods: eggs, fish, organ meats']},
        GG: { f:'hom',  sev:2, msg:'Reduced methionine synthase activity',
              d:'B12-mediated methylation downstream of folate is impaired.',
              do:['Methyl-B12 sublingual or sub-Q','Methylfolate paired'],
              li:['Regular B12 monitoring']}
      } },
    'rs1801394': { g:'MTRR', n:'A66G (I22M)', r:'MS reductase · B12 regeneration',
      e: {
        AA: { f:'wild', sev:0, msg:'Normal activity' },
        AG: { f:'het',  sev:1, msg:'Mildly impaired MTR recycling',
              d:'Slower regeneration of methionine synthase; functional B12 deficiency risk.',
              do:['Methyl-B12','Riboflavin (B2) as cofactor']},
        GG: { f:'hom',  sev:2, msg:'Significantly impaired MTR recycling',
              d:'Common in autism and Down syndrome cohorts; pairs poorly with MTHFR TT.',
              do:['Higher-dose methyl-B12','Riboflavin cofactor','Methylfolate'],
              li:['Avoid nitrous oxide (depletes B12)']}
      } },
    'rs234706': { g:'CBS', n:'C699T', r:'Sulfation pathway',
      e: {
        CC: { f:'wild', sev:0, msg:'Normal activity' },
        CT: { f:'het',  sev:1, msg:'Variant present (clinical significance contested)',
              d:'The Yasko CBS "upregulation" framework is contested in the primary literature — early studies suggested increased activity, later replication has been mixed. Symptomatic-only intervention.',
              do:['If symptomatic with ammonia/sulfur intolerance: molybdenum 200–500 mcg, taurine 500–1000 mg trial under clinician guidance'],
              li:['No restrictions if asymptomatic']},
        TT: { f:'hom',  sev:1, msg:'Variant present (clinical significance contested)',
              d:'Contested in primary literature. The Yasko functional-medicine framework around sulfur restriction is widely used in practice but not RCT-validated. If symptomatic, molybdenum + taurine support may help.',
              do:['Symptomatic-only: molybdenum 200–500 mcg, taurine 500–1000 mg, under clinician guidance'],
              av:['Aggressive methyl-B12 or methylfolate without symptom monitoring'],
              li:['Sulfur-food trial-and-elimination only if symptomatic']}
      } },
    'rs4680': { g:'COMT', n:'V158M (rs4680)', r:'Catecholamine clearance',
      e: {
        GG: { f:'wild', sev:0, msg:'Fast COMT ("warrior") · Val/Val · 3–4× higher enzyme activity',
              d:'Rapid dopamine clearance. May benefit from extra catecholamine support.',
              li:['Tyrosine-containing foods','Adequate magnesium','Stress can transiently boost performance'] },
        AG: { f:'het',  sev:1, msg:'Moderate COMT ("mixed") · Val/Met',
              d:'Balanced catecholamine handling.',
              li:['Standard balanced approach to methyl donors'] },
        AA: { f:'hom',  sev:2, msg:'Slow COMT ("worrier") · Met/Met · 3–4× slower enzyme activity',
              d:'Slow catecholamine breakdown; dopamine + adrenaline linger longer. Practitioner-reported (not RCT-evidenced) sensitivity to high-dose methyl donors — start low and titrate slowly if used.',
              do:['Methyl donors (SAMe, methyl-B12, methylfolate): start low, titrate slowly','Magnesium 400 mg','Vitamin C'],
              av:['Excess caffeine'],
              li:['Stress management is high-leverage','Sleep regularity']}
      } },
    'rs4633': { g:'COMT', n:'H62H (rs4633)', r:'COMT silent variant (linked to rs4680)',
      e: {
        CC: { f:'wild', sev:0, msg:'Linked to fast COMT' },
        CT: { f:'het',  sev:1, msg:'Linked to moderate COMT' },
        TT: { f:'hom',  sev:2, msg:'Linked to slow COMT (Met/Met haplotype)',
              d:'Reinforces interpretation of rs4680 in same direction.',
              li:['See rs4680 lifestyle notes']}
      } },
    'rs4880': { g:'SOD2', n:'A16V (rs4880)', r:'Mitochondrial superoxide dismutase',
      e: {
        AA: { f:'wild', sev:0, msg:'Higher mitochondrial targeting (Ala/Ala)' },
        AG: { f:'het',  sev:1, msg:'Mixed mitochondrial SOD2 import',
              li:['Antioxidant-rich diet']},
        GG: { f:'hom',  sev:2, msg:'Reduced mito SOD2 (Val/Val)',
              d:'Lower mitochondrial superoxide clearance → higher oxidative stress, mito vulnerability.',
              do:['Mito antioxidants (CoQ10, alpha-lipoic acid, NAC)','Methylene blue under guidance'],
              av:['Glyphosate / pesticide exposure (mito stress)'],
              li:['Colorful plant polyphenols','Resistance + zone-2 cardio for mito biogenesis'],
              ai:['INT-0042','INT-0008']}
      } },
    'rs1695':   { g:'GSTP1', n:'I105V (rs1695)', r:'Glutathione conjugation',
      e: {
        AA: { f:'wild', sev:0, msg:'Higher GSTP1 activity (Ile/Ile)' },
        AG: { f:'het',  sev:1, msg:'Moderately reduced GSTP1',
              li:['Sulforaphane-rich foods (broccoli sprouts)','NAC 600 mg']},
        GG: { f:'hom',  sev:2, msg:'Significantly reduced GSTP1 (Val/Val)',
              d:'Impaired phase-II detoxification — slower clearance of xenobiotics and oxidants.',
              do:['NAC 600–1200 mg','Liposomal glutathione','Sulforaphane (BroccoMax) daily'],
              av:['Heavy chemical exposures (paints, solvents, smoke)'],
              li:['Filtered water and air','Choose organic produce on the EWG dirty list']}
      } },
    'rs1138272': { g:'GSTP1', n:'A114V', r:'Glutathione conjugation',
      e: {
        CC: { f:'wild', sev:0, msg:'Normal activity' },
        CT: { f:'het',  sev:1, msg:'Mildly reduced GSTP1 activity',
              li:['Cruciferous vegetables daily']},
        TT: { f:'hom',  sev:2, msg:'Significantly reduced',
              d:'Compound with rs1695 → more pronounced detox impairment.',
              do:['NAC + sulforaphane','Glutathione precursors']}
      } },
    'rs6265':   { g:'BDNF', n:'V66M (Val66Met)', r:'Neurotrophic · learning',
      e: {
        GG: { f:'wild', sev:0, msg:'Val/Val · normal BDNF secretion' },
        AG: { f:'het',  sev:1, msg:'Val/Met · reduced activity-dependent BDNF secretion',
              d:'Lower neurotrophic support for synaptic plasticity. Exercise and learning load drive BDNF more important.',
              do:['7-keto DHEA','Lion\'s Mane mushroom','Omega-3 DHA'],
              li:['Zone-2 aerobic exercise (BDNF inducer)','Cognitive load via learning','Adequate sleep']},
        AA: { f:'hom',  sev:2, msg:'Met/Met · materially reduced activity-dependent secretion',
              d:'Stronger phenotype: associated with anxiety, depression risk, slower implicit learning.',
              do:['Lion\'s Mane','High-DHA omega-3','Curcumin','Cocoa flavanols'],
              li:['Daily aerobic exercise is high-leverage','Novel learning weekly','Cold exposure (mild BDNF inducer)']}
      } },
    'rs53576':  { g:'OXTR', n:'rs53576', r:'Oxytocin receptor · social bonding',
      e: {
        AA: { f:'hom', sev:1, msg:'A/A · less sensitive OXT receptor',
              d:'Meta-analysis effect size for sociality is small (Cohen\'s d ≈ 0.11). Behavioral interventions and bonding routines are evidence-supported; intranasal oxytocin trials in autism have shown mixed results (SOARS-B 2021 negative).',
              do:['Behavioral interventions','Touch and bonding routines','Intranasal oxytocin only under specialist guidance with realistic expectations']},
        AG: { f:'het', sev:0, msg:'A/G · intermediate' },
        GG: { f:'wild', sev:0, msg:'G/G · standard OXTR sensitivity' }
      } },
    'rs2298444': { g:'FOLR1', n:'rs2298444', r:'Folate receptor alpha',
      e: {
        CC: { f:'wild', sev:0, msg:'Normal FOLR1' },
        CT: { f:'het', sev:1, msg:'Mildly altered FOLR1 expression',
              do:['Methylfolate; consider leucovorin if FRAA antibody positive']},
        TT: { f:'hom', sev:2, msg:'Altered FOLR1 expression',
              d:'Cerebral folate handling may be impacted; test FRAA antibodies.',
              do:['Leucovorin (folinic acid) per Frye protocol if FRAA+'],
              ai:['INT-0001']}
      } },
    'rs1051266': { g:'SLC19A1', n:'H27R (rs1051266)', r:'Reduced folate carrier',
      e: {
        AA: { f:'wild', sev:0, msg:'Normal RFC1' },
        AG: { f:'het', sev:1, msg:'Mildly reduced folate cellular uptake',
              do:['Methylfolate']},
        GG: { f:'hom', sev:2, msg:'Reduced folate uptake',
              d:'Lower cellular folate availability; relevant alongside MTHFR variants.',
              do:['Methylfolate at higher dose'],
              ai:['INT-0001']}
      } },
    'rs2228570': { g:'VDR', n:'FokI (rs2228570)', r:'Vitamin D receptor',
      e: {
        AA: { f:'hom', sev:1, msg:'f/f · shorter VDR protein, lower activity',
              do:['Vitamin D3 5000 IU + K2 100 mcg','Target 25-OH-D 50-80 ng/mL']},
        AG: { f:'het', sev:0, msg:'F/f · intermediate' },
        GG: { f:'wild', sev:0, msg:'F/F · longer VDR protein' }
      } },
    'rs731236':  { g:'VDR', n:'TaqI (rs731236)', r:'Vitamin D receptor',
      e: {
        AA: { f:'hom', sev:1, msg:'tt · altered VDR activity',
              do:['Vitamin D3 + magnesium + K2 stack']},
        AG: { f:'het', sev:0, msg:'Tt · intermediate' },
        GG: { f:'wild', sev:0, msg:'TT · standard VDR activity' }
      } },
    'rs1544410': { g:'VDR', n:'BsmI (rs1544410)', r:'Vitamin D receptor',
      e: {
        AA: { f:'hom', sev:1, msg:'bb · associated with lower BMD and immune effects',
              do:['Adequate vitamin D3 + magnesium']},
        AG: { f:'het', sev:0, msg:'Bb · intermediate' },
        GG: { f:'wild', sev:0, msg:'BB · standard' }
      } },
    'rs429358': { g:'APOE', n:'rs429358 (combined with rs7412)', r:'Lipid handling · neuroinflammation',
      e: {
        TT: { f:'wild', sev:0, msg:'No e4 from this SNP (need rs7412 to determine ε2/ε3)' },
        CT: { f:'het', sev:2, msg:'One e4 allele',
              d:'APOE ε4 carrier: increased Alzheimer risk, altered fatty acid trafficking, higher saturated-fat sensitivity.',
              do:['DHA-rich omega-3 (algae or fish)','Monitor lipids and ApoB','Mediterranean-leaning diet'],
              av:['Saturated fat in excess','Smoking'],
              li:['Aerobic exercise reduces APOE4-related cognitive decline','Quality sleep critical']},
        CC: { f:'hom', sev:3, msg:'Two e4 alleles (ε4/ε4)',
              d:'Strongest hereditary signal for late-onset Alzheimer. Strong response to lifestyle intervention.',
              do:['DHA daily','ApoB-targeted lipid management','Resistance + aerobic exercise'],
              av:['Saturated fat','Alcohol','Poor sleep'],
              li:['Strict cardiometabolic discipline','Annual cognitive baseline testing']}
      } },
    'rs7412':   { g:'APOE', n:'rs7412 (combined with rs429358)', r:'Lipid handling',
      e: {
        CC: { f:'wild', sev:0, msg:'Standard ApoE (no e2 from this SNP)' },
        CT: { f:'het', sev:1, msg:'One e2 allele (lower LDL receptor binding)',
              li:['Mixed metabolic effects depending on rs429358 status']},
        TT: { f:'hom', sev:2, msg:'Two e2 alleles (ε2/ε2)',
              d:'Reduced LDL receptor binding; rare cardiometabolic patterns.'}
      } },
    'rs3892097': { g:'CYP2D6', n:'*4 (rs3892097)', r:'Phase-I drug metabolism · CPIC-guided',
      e: {
        GG: { f:'wild', sev:0, msg:'Normal CYP2D6' },
        AG: { f:'het', sev:1, msg:'Intermediate metabolizer',
              d:'Affects metabolism of ~25% of common drugs (SSRIs, opioids, antipsychotics). Per CPIC guidelines.',
              do:['PGx-aware prescribing — share with prescriber','Lower starting doses on CYP2D6-substrate meds']},
        AA: { f:'hom', sev:2, msg:'Poor metabolizer (CYP2D6 *4/*4)',
              d:'Significantly reduced metabolism. Per CPIC: psychiatric meds (paroxetine, fluoxetine, venlafaxine, tricyclics, several antipsychotics) need dose adjustment or alternatives.',
              do:['Full PGx panel before starting psychiatric meds','Disclose to all prescribers'],
              av:['Codeine: poor metabolizers get INSUFFICIENT pain relief (not toxicity) — request a non-codeine analgesic. (Codeine toxicity risk is the separate ultra-rapid metabolizer phenotype.)']}
      } },
    'rs4244285': { g:'CYP2C19', n:'*2 (rs4244285)', r:'Phase-I drug metabolism',
      e: {
        GG: { f:'wild', sev:0, msg:'Normal CYP2C19' },
        AG: { f:'het', sev:1, msg:'Intermediate metabolizer',
              do:['PGx awareness for PPI, clopidogrel, SSRIs']},
        AA: { f:'hom', sev:2, msg:'Poor metabolizer',
              d:'Slow clearance of PPIs, clopidogrel (Plavix), citalopram. Higher exposure → side effects more likely.',
              do:['Disclose to prescribers','Lower starting doses on relevant meds']}
      } },
    'rs1801105': { g:'DAO', n:'rs1801105', r:'Histamine degradation',
      e: {
        GG: { f:'wild', sev:0, msg:'Normal DAO activity' },
        AG: { f:'het', sev:1, msg:'Mildly reduced histamine clearance',
              li:['Low-histamine diet trial if symptomatic']},
        AA: { f:'hom', sev:2, msg:'Significantly reduced DAO activity',
              d:'Higher histamine load → flushing, headaches, gut symptoms, mast-cell features.',
              do:['DAO enzyme supplements with meals','Quercetin','Vitamin C 1g'],
              av:['Aged cheese, fermented foods, leftover meat, alcohol, vinegar'],
              li:['Low-histamine diet trial']}
      } },
    'rs2073837': { g:'HNMT', n:'rs2073837', r:'Histamine N-methylation',
      e: {
        AA: { f:'wild', sev:0, msg:'Normal HNMT' },
        AG: { f:'het', sev:1, msg:'Mildly reduced HNMT activity' },
        GG: { f:'hom', sev:2, msg:'Reduced HNMT activity',
              d:'Slower secondary histamine clearance.',
              do:['Quercetin','SAMe (provides methyl donors)']}
      } },
    'rs1800562': { g:'HFE', n:'C282Y', r:'Iron handling · hemochromatosis',
      e: {
        GG: { f:'wild', sev:0, msg:'Normal iron handling' },
        AG: { f:'het', sev:1, msg:'Hemochromatosis carrier',
              d:'Modestly elevated iron-storage tendency. Most carriers don\'t develop overload — monitor if symptomatic.',
              li:['Don\'t routinely take iron supplements without testing']},
        AA: { f:'hom', sev:2, msg:'Genotype consistent with hereditary hemochromatosis risk',
              d:'Clinical penetrance is incomplete: ~1 in 4 male homozygotes and ~1 in 10 female homozygotes develop iron-overload disease. Many remain asymptomatic lifelong. Confirm with annual ferritin + transferrin saturation.',
              do:['Annual ferritin + transferrin saturation','Therapeutic phlebotomy ONLY if ferritin elevated (typically >300 ng/mL men, >200 women) or transferrin sat >45%','Genetic counselor consult'],
              av:['Iron supplements without testing','Heavy red meat + alcohol combinations']}
      } },
    'rs1799945': { g:'HFE', n:'H63D', r:'Iron absorption',
      e: {
        CC: { f:'wild', sev:0, msg:'Normal' },
        CG: { f:'het', sev:1, msg:'H63D carrier' },
        GG: { f:'hom', sev:2, msg:'H63D homozygous · mild iron-overload risk',
              do:['Periodic iron panel (especially if combined with C282Y)']}
      } },
    'rs1800629': { g:'TNF', n:'-308 G>A (rs1800629)', r:'Pro-inflammatory cytokine',
      e: {
        GG: { f:'wild', sev:0, msg:'Standard TNF expression' },
        AG: { f:'het', sev:1, msg:'Higher TNF expression on stimulation',
              li:['Anti-inflammatory diet','Curcumin','Omega-3']},
        AA: { f:'hom', sev:2, msg:'Materially higher inflammatory response',
              d:'Stronger inflammatory cytokine output; auto-immune and inflammation risk.',
              do:['Curcumin','Resveratrol','Omega-3 DHA','LDN (under FM guidance) if symptomatic'],
              av:['Heavy seed oil intake','Chronic sleep deprivation'],
              li:['Mediterranean-style diet','Regular exercise']}
      } },
    'rs1800795': { g:'IL6', n:'-174 G>C (rs1800795)', r:'Pro-inflammatory cytokine',
      e: {
        GG: { f:'wild', sev:0, msg:'Standard IL-6 expression' },
        CG: { f:'het', sev:1, msg:'Modified IL-6 induction' },
        CC: { f:'hom', sev:2, msg:'Altered IL-6 expression',
              d:'Inflammatory signaling phenotype; relevant for autoimmunity and metabolic risk.',
              do:['Curcumin','Resveratrol','Omega-3'],
              li:['Sleep hygiene','Stress regulation']}
      } },
    'rs662':    { g:'PON1', n:'Q192R (rs662)', r:'Organophosphate detox',
      e: {
        AA: { f:'wild', sev:0, msg:'Q/Q · slow paraoxonase' },
        AG: { f:'het', sev:1, msg:'Q/R · intermediate paraoxonase',
              li:['Avoid pesticide exposure']},
        GG: { f:'hom', sev:2, msg:'R/R · altered organophosphate handling',
              d:'Different specificity for organophosphate detox; environmental exposure matters more.',
              av:['Pesticide-treated produce (use EWG dirty dozen list)','Lawn chemicals'],
              li:['Choose organic on dirty-list produce','Filter water']}
      } },
    'rs1799853': { g:'CYP2C9', n:'*2 (rs1799853)', r:'Drug metabolism (warfarin, NSAIDs)',
      e: {
        CC: { f:'wild', sev:0, msg:'Normal' },
        CT: { f:'het', sev:1, msg:'Intermediate metabolizer',
              do:['PGx-aware NSAID and warfarin dosing']},
        TT: { f:'hom', sev:2, msg:'Poor metabolizer',
              d:'Lower warfarin requirement; higher GI-bleed risk on NSAIDs.',
              do:['Disclose to prescribers','Lower starting doses on warfarin']}
      } },
    'rs1799930': { g:'NAT2', n:'R197Q (NAT2 *6)', r:'Acetylation phase-II',
      e: {
        GG: { f:'wild', sev:0, msg:'Rapid acetylator' },
        AG: { f:'het', sev:1, msg:'Intermediate acetylator' },
        AA: { f:'hom', sev:2, msg:'Slow acetylator',
              d:'Slower clearance of aromatic amines and certain drugs; bladder cancer risk modestly elevated with smoking exposure.',
              av:['Smoking (especially)','Char-grilled meats in excess']}
      } },
    'rs1800497': { g:'DRD2', n:'Taq1A (rs1800497)', r:'Dopamine D2 receptor',
      e: {
        GG: { f:'wild', sev:0, msg:'A2/A2 · normal D2 receptor density' },
        AG: { f:'het', sev:1, msg:'A1/A2 · ~30% lower D2 receptor density',
              li:['Adequate tyrosine intake','Exercise as dopamine inducer']},
        AA: { f:'hom', sev:2, msg:'A1/A1 · ~40% lower D2 receptor density',
              d:'Lower dopamine receptor availability; reward sensitivity and addiction risk may differ.',
              do:['Tyrosine 500 mg','Mucuna pruriens (L-DOPA precursor) under guidance'],
              li:['Structured reward (don\'t rely on novelty)','Quality sleep']}
      } },
    'rs6313':   { g:'HTR2A', n:'T102C (rs6313)', r:'Serotonin 2A receptor',
      e: {
        AA: { f:'wild', sev:0, msg:'Standard 5-HT2A expression' },
        AG: { f:'het', sev:1, msg:'Modified 5-HT2A density' },
        GG: { f:'hom', sev:2, msg:'Altered 5-HT2A density',
              d:'Associated with differential response to SSRIs and mood phenotypes.',
              do:['PGx-aware SSRI selection']}
      } },
    'rs6311':   { g:'HTR2A', n:'C1438T (rs6311)', r:'5-HT2A promoter',
      e: {
        CC: { f:'wild', sev:0, msg:'Standard expression' },
        CT: { f:'het', sev:1, msg:'Intermediate expression' },
        TT: { f:'hom', sev:1, msg:'Higher 5-HT2A expression',
              d:'May affect anxiety and SSRI response trajectory.'}
      } }
  };

  // Build rsID → gene fallback for matches not in VARIANT_DB
  const RSID_TO_GENE = {};
  for (const rsid of Object.keys(VARIANT_DB)) {
    RSID_TO_GENE[rsid] = VARIANT_DB[rsid].g;
  }
  // Extra rsIDs that have a gene but no curated variant interpretation yet
  Object.assign(RSID_TO_GENE, {
    'rs2236225':'MTHFD1','rs6347':'SLC6A3',
    'rs7997012':'HTR2A','rs1799732':'DRD2',
    'rs25531':'SLC6A4','rs4795541':'SLC6A4','rs6321':'SLC6A4',
    'rs56164415':'BDNF','rs2254298':'OXTR','rs2230197':'OXT',
    'rs366631':'GSTM1','rs1801280':'NAT2','rs1799931':'NAT2',
    'rs4148323':'UGT1A1','rs1056827':'CYP1B1','rs1056836':'CYP1B1',
    'rs1048943':'CYP1A1','rs4646903':'CYP1A1','rs1057910':'CYP2C9',
    'rs4986893':'CYP2C19','rs1065852':'CYP2D6','rs2032582':'ABCB1',
    'rs769407':'GAD1','rs2058725':'GAD1','rs10491734':'GRIK2',
    'rs11558538':'HNMT','rs7975232':'VDR','rs5742905':'CBS',
    'rs3736771':'SHANK3','rs6766410':'SCN1A','rs1057079':'MTOR',
    'rs854560':'PON1','rs13266634':'SLC30A8','rs2070424':'SOD1',
    'rs1050450':'GPX1','rs17856199':'GCLC','rs17883901':'GCLC',
    'rs7873784':'TLR4','rs6214':'IGF1','rs5742612':'IGF1',
    'rs2228145':'IL6R','rs7501331':'BCMO1','rs193922753':'RYR1',
    'rs3733890':'BHMT'
  });

  // DOM refs
  const btnUpload = document.getElementById('upload-btn');
  const modal     = document.getElementById('upload-modal');
  const mClose    = document.getElementById('m-close');
  const userData  = document.getElementById('user-data');
  const bwForm    = document.getElementById('bw-form');

  // build the blood-work form
  for (const f of BIOMARKER_FIELDS) {
    const w = document.createElement('div');
    w.className = 'm-field';
    const unit = f.u ? '<span class="units">' + f.u + '</span>' : '';
    w.innerHTML =
      '<label>' + f.l + unit + '</label>' +
      '<input type="number" step="any" data-k="' + f.k + '" />' +
      '<div class="ref">ref: ' + f.rL + '–' + f.rH + (f.u ? ' ' + f.u : '') + '</div>';
    bwForm.appendChild(w);
  }

  // storage helpers
  function getStored() {
    try {
      return {
        genetics:   JSON.parse(localStorage.getItem('cwa_genetics_v1')   || 'null'),
        biomarkers: JSON.parse(localStorage.getItem('cwa_biomarkers_v1') || 'null')
      };
    } catch (e) { return { genetics:null, biomarkers:null }; }
  }
  function saveGenetics(data) {
    localStorage.setItem('cwa_genetics_v1', JSON.stringify(data));
    updateBanner(); applyUserData();
  }
  function saveBiomarkers(values) {
    localStorage.setItem('cwa_biomarkers_v1', JSON.stringify(values));
    updateBanner(); applyUserData();
  }

  function updateBanner() {
    const s = getStored();
    const has = !!(s.genetics || s.biomarkers);
    const viewReportBtn = document.getElementById('view-report');
    if (has) {
      userData.classList.remove('on');                  // hide tiny summary line
      viewReportBtn.classList.add('on');                // show the call-to-action
      btnUpload.classList.add('has-data');
      btnUpload.innerHTML =
        '<span class="ub-main"><span class="dot"></span>Update my data</span>' +
        '<span class="ub-sub">Re-upload anytime · private</span>';
    } else {
      userData.classList.remove('on');
      viewReportBtn.classList.remove('on');
      btnUpload.classList.remove('has-data');
      btnUpload.innerHTML =
        '<span class="ub-main">Upload my Genetics · Bloodwork · Health Reports</span>' +
        '<span class="ub-sub">Private · stays in your browser</span>';
    }
  }

  function applyUserData() {
    const s = getStored();
    window.userMatchedIds = new Set();
    if (s.genetics) {
      for (const gid of s.genetics.matchedGenes) window.userMatchedIds.add(gid);
    }
    if (s.biomarkers) {
      for (const k of Object.keys(s.biomarkers)) {
        const v = s.biomarkers[k];
        if (v.nodeId) window.userMatchedIds.add(v.nodeId);
      }
    }
  }

  // ── PHENOTYPE-MATCH REPORT ENGINE ───────────────────────────────
  // For each matched gene/biomarker, traverse the atlas to compute its
  // affinity to every phenotype using direct edges + one-hop bridges
  // (gene→mechanism→phenotype, gene→hypothesis→mechanism→phenotype,
  // biomarker→mechanism→phenotype, biomarker→hypothesis→mechanism→phe).
  // Then rank phenotypes by aggregate score, find top interventions
  // and tests per top phenotype. Pure client-side, runs from the same
  // (nodes, links) data the graph uses.

  const nodeMap = new Map(nodes.map(n => [n.id, n]));

  // Pre-index edges by source and by kind for fast lookup
  const edgesBySrc = new Map();
  const edgesByTgt = new Map();
  for (const l of links) {
    const sId = (l.source && l.source.id) || l.source;
    const tId = (l.target && l.target.id) || l.target;
    if (!edgesBySrc.has(sId)) edgesBySrc.set(sId, []);
    edgesBySrc.get(sId).push({ tgt: tId, w: l.w, k: l.k });
    if (!edgesByTgt.has(tId)) edgesByTgt.set(tId, []);
    edgesByTgt.get(tId).push({ src: sId, w: l.w, k: l.k });
  }

  // For a given node ID, return affinity to each phenotype
  // via direct + one-hop + two-hop traversal. Conservative weights.
  function affinityToPhenotypes(originId, originType) {
    const aff = new Map();        // phenotype_id → weight
    const out = edgesBySrc.get(originId) || [];

    for (const e of out) {
      // direct gene→phenotype or biomarker→phenotype
      if (e.k === 'gp' || e.k === 'bp') {
        aff.set(e.tgt, (aff.get(e.tgt) || 0) + e.w * 1.0);
        continue;
      }
      // gene→mechanism / biomarker→mechanism → look for mechanism→phenotype
      if (e.k === 'gm' || e.k === 'bm') {
        const mech = e.tgt;
        const mechOut = edgesBySrc.get(mech) || [];
        for (const e2 of mechOut) {
          if (e2.k === 'mp') {
            aff.set(e2.tgt, (aff.get(e2.tgt) || 0) + e.w * e2.w * 0.7);
          }
        }
        continue;
      }
      // gene→hypothesis / biomarker→hypothesis → hypothesis→mechanism → mech→phe
      if (e.k === 'gh' || e.k === 'bh') {
        const hyp = e.tgt;
        const hypOut = edgesBySrc.get(hyp) || [];
        for (const e2 of hypOut) {
          if (e2.k === 'hm') {
            const mech2 = e2.tgt;
            const mech2Out = edgesBySrc.get(mech2) || [];
            for (const e3 of mech2Out) {
              if (e3.k === 'mp') {
                aff.set(e3.tgt, (aff.get(e3.tgt) || 0) + e.w * e2.w * e3.w * 0.4);
              }
            }
          }
        }
      }
    }
    return aff;
  }

  // Top interventions for a phenotype, ranked by edge_weight * csrs
  function topInterventionsForPhenotype(pId, k) {
    const candidates = [];
    const inEdges = edgesByTgt.get(pId) || [];
    for (const e of inEdges) {
      if (e.k !== 'ip') continue;
      const intNode = nodeMap.get(e.src);
      if (!intNode || intNode.t !== 'I') continue;
      const csrs = parseFloat(intNode.sc) || 0;
      candidates.push({
        node: intNode,
        score: e.w * 0.6 + (csrs / 100) * 0.4,
        edge_w: e.w, csrs
      });
    }
    candidates.sort((a, b) => b.score - a.score);
    return candidates.slice(0, k || 5);
  }

  // Top tests for a phenotype, ranked by tier and cost
  function topTestsForPhenotype(pId, k) {
    const candidates = [];
    const inEdges = edgesByTgt.get(pId) || [];
    for (const e of inEdges) {
      if (e.k !== 'tp') continue;
      const testNode = nodeMap.get(e.src);
      if (!testNode || testNode.t !== 'T') continue;
      candidates.push({ node: testNode, edge_w: e.w });
    }
    // tier prefix sort: T1 > T2 > T3 > T4; then ascending cost
    function tierRank(tr) {
      if (!tr) return 99;
      const m = String(tr).match(/T(\d)/i);
      return m ? parseInt(m[1], 10) : 99;
    }
    candidates.sort((a, b) => {
      const ta = tierRank(a.node.tr), tb = tierRank(b.node.tr);
      if (ta !== tb) return ta - tb;
      const ca = parseFloat(a.node.cl) || 9999;
      const cb = parseFloat(b.node.cl) || 9999;
      return ca - cb;
    });
    return candidates.slice(0, k || 5);
  }

  function generateReport() {
    const s = getStored();
    if (!s.genetics && !s.biomarkers) return null;

    const matchedGenes = new Set(s.genetics?.matchedGenes || []);
    const bioById = {};
    if (s.biomarkers) {
      for (const k of Object.keys(s.biomarkers)) {
        const v = s.biomarkers[k];
        if (v.nodeId) bioById[v.nodeId] = v;
      }
    }

    // Per-phenotype score + which matches contributed
    const pScores = new Map();
    function add(pId, weight, contribLabel, contribType, originLabel) {
      if (!pScores.has(pId)) {
        pScores.set(pId, { score: 0, contribs: [] });
      }
      const e = pScores.get(pId);
      e.score += weight;
      e.contribs.push({ type: contribType, label: contribLabel, weight, originLabel });
    }

    for (const gid of matchedGenes) {
      const gNode = nodeMap.get(gid);
      const gLabel = gNode ? gNode.l : gid;
      const aff = affinityToPhenotypes(gid, 'G');
      for (const [pid, w] of aff) add(pid, w, gLabel, 'gene', gLabel);
    }
    for (const bid of Object.keys(bioById)) {
      const bNode = nodeMap.get(bid);
      const bLabel = bNode ? bNode.l : bid;
      const bioVal = bioById[bid];
      const oorMult = (bioVal.flag === 'high' || bioVal.flag === 'low') ? 2.0 : 0.6;
      const aff = affinityToPhenotypes(bid, 'B');
      for (const [pid, w] of aff) add(pid, w * oorMult, bLabel, 'biomarker', bLabel);
    }

    // Rank phenotypes
    const ranked = [];
    for (const [pid, data] of pScores) {
      const pNode = nodeMap.get(pid);
      if (!pNode) continue;
      ranked.push({ id: pid, node: pNode, score: data.score, contribs: data.contribs });
    }
    ranked.sort((a, b) => b.score - a.score);

    // Normalize to percentage of top score
    const topScore = ranked.length ? ranked[0].score : 1;
    for (const r of ranked) {
      r.pct = topScore ? Math.round((r.score / topScore) * 100) : 0;
    }

    const topPhenotypes = ranked.slice(0, 3);

    // Top interventions across the top phenotypes (dedup by id)
    const intSeen = new Set();
    const topInts = [];
    for (const p of topPhenotypes) {
      for (const ic of topInterventionsForPhenotype(p.id, 8)) {
        if (intSeen.has(ic.node.id)) continue;
        intSeen.add(ic.node.id);
        topInts.push({ ...ic, forPhenotype: p.node.l });
        if (topInts.length >= 5) break;
      }
      if (topInts.length >= 5) break;
    }

    // Top tests across top phenotypes (dedup, exclude tests user already did
    // by approximating: if a test is named after a biomarker the user entered)
    const enteredBioLabels = new Set(
      Object.values(s.biomarkers || {}).map(v => (v.label || '').toLowerCase())
    );
    function testAlreadyDone(testNode) {
      // Conservative substring match: only suppress a test when its full
      // name contains the entered biomarker label AND the label is at
      // least 6 chars (avoids "B12" suppressing "B12 functional test").
      const tn = (testNode.l || '').toLowerCase();
      for (const bl of enteredBioLabels) {
        if (bl && bl.length >= 6 && tn.indexOf(bl) >= 0) return true;
      }
      return false;
    }
    const testSeen = new Set();
    const topTests = [];
    for (const p of topPhenotypes) {
      for (const tc of topTestsForPhenotype(p.id, 6)) {
        if (testSeen.has(tc.node.id)) continue;
        if (testAlreadyDone(tc.node)) continue;
        testSeen.add(tc.node.id);
        topTests.push({ ...tc, forPhenotype: p.node.l });
        if (topTests.length >= 5) break;
      }
      if (topTests.length >= 5) break;
    }

    // Out-of-range biomarkers list
    const oor = Object.values(s.biomarkers || {})
      .filter(v => v.flag === 'high' || v.flag === 'low');

    // Variants flagged by the curated VARIANT_DB (only those with sev > 0)
    const matchedVariants = (s.genetics && s.genetics.matchedVariants) || [];

    // Atlas-intervention boost from variant recommendations.
    // If a variant recommends an atlas intervention (e.g., INT-0001 leucovorin
    // for MTHFR TT), push that intervention to the top of the actions list.
    const variantBoostedInts = new Set();
    for (const v of matchedVariants) {
      for (const aiId of (v.atlasInts || [])) variantBoostedInts.add(aiId);
    }
    // Re-order topInts so variant-boosted ones float to the top
    if (variantBoostedInts.size > 0) {
      const boosted = [], rest = [];
      for (const it of topInts) {
        if (variantBoostedInts.has(it.node.id)) boosted.push(it);
        else rest.push(it);
      }
      topInts.length = 0;
      for (const it of boosted) topInts.push(it);
      for (const it of rest) topInts.push(it);
    }

    return {
      genetics: s.genetics,
      biomarkers: s.biomarkers,
      matchedGeneCount: matchedGenes.size,
      matchedVariants,
      bioCount: Object.keys(s.biomarkers || {}).length,
      topPhenotypes,
      topInterventions: topInts,
      topTests,
      outOfRange: oor,
    };
  }

  // ── GENE-CLUSTER TAXONOMY ───────────────────────────────────────
  // Based on Walsh Research Institute + Lynch "Dirty Genes" + Yasko +
  // Frye + MAPS for Autism framework. 8 functional axes plus a 9th
  // cross-cutting "nutrient handling" axis. Each gene maps to ≥1 cluster.
  const CLUSTERS = [
    { id:'methylation', name:'Methylation cycle',
      desc:'Folate / B12 / SAMe handling',
      genes:['MTHFR','MTR','MTRR','BHMT','AHCY','SHMT1','MTHFD1','SLC19A1','FOLR1','C677T','A1298C','V158M'] },
    { id:'redox', name:'Glutathione & redox',
      desc:'Master antioxidant + oxidative-stress defense',
      genes:['GCLC','GCLM','GPX1','GSTP1','GSTM1','GSTT1','SOD1','SOD2','CAT','NQO1','A16V'] },
    { id:'mito', name:'Mitochondrial function',
      desc:'Energy + biogenesis + cellular powerhouse',
      genes:['TOMM40','PPARGC1A','SOD2','NDUFS7','MFN2','OPA1','POLG','A16V'] },
    { id:'sulfation', name:'Sulfation & sulfur handling',
      desc:'CBS pathway · sulfite / sulfate / taurine',
      genes:['CBS','SUOX','MOCS1','MOCS2','SULT1A1'] },
    { id:'coag', name:'Coagulation',
      desc:'Clotting cascade · hypercoagulability axis',
      genes:['F5','F2','F11','F13A1','SERPINC1','SERPIND1','ABO','VWF','PROC','PROS1','THBD','MTHFR'] },
    { id:'detox', name:'Phase I / II detoxification',
      desc:'Drug + xenobiotic + estrogen metabolism',
      genes:['CYP1A1','CYP1A2','CYP1B1','CYP2C9','CYP2C19','CYP2D6','CYP3A4','CYP19A1','NAT2','PON1','UGT1A1','ABCB1','GSTP1','GSTM1'] },
    { id:'inflam', name:'Inflammation & immune',
      desc:'Cytokines · NF-κB · vascular adhesion',
      genes:['TNF','IL6','IL1A','IL1B','IL10','IL17A','IL33','IL1RL1','STAT1','STAT3','ICAM1','VCAM1','NFKB1','CRP','TLR2','TLR4','IL6R'] },
    { id:'neuro', name:'Neurotransmitter & behavior',
      desc:'Dopamine · serotonin · BDNF · oxytocin',
      genes:['BDNF','DRD2','DRD4','HTR2A','HTR1A','SLC6A3','SLC6A4','MAOA','MAOB','COMT','OXTR','OXT','GAD1','GRIK2','SHANK3','NRXN1','NLGN3','NLGN4X','CNTNAP2','MECP2','FMR1'] },
    { id:'nutr', name:'Nutrient handling',
      desc:'Vitamin D · iron · glucose · choline · lipids',
      genes:['VDR','HFE','TCF7L2','KCNJ11','KCNQ1','ENPP1','LEPR','PEMT','APOE','MC1R','BCMO1','SLC30A8','IGF1','ADIPOQ','I405V','Y402H','CFH','CETP'] }
  ];

  // Build reverse index: gene → array of cluster ids
  const geneToClusters = new Map();
  for (const c of CLUSTERS) {
    for (const g of c.genes) {
      if (!geneToClusters.has(g)) geneToClusters.set(g, []);
      geneToClusters.get(g).push(c.id);
    }
  }
  // Quick lookup of cluster meta by id
  const clusterById = Object.fromEntries(CLUSTERS.map(c => [c.id, c]));

  // Severity-load math: for each cluster, aggregate severity points
  // from matched variants. Variant severity 3 = 4 pts, 2 = 2 pts, 1 = 1 pt.
  // Protective variants subtract 0.5 pts (capped at floor 0).
  function clusterLoads(variants) {
    const loads = {};
    for (const c of CLUSTERS) loads[c.id] = {
      cluster: c, score: 0, variants: [], topActions: new Set(),
      topAvoid: new Set(), topLifestyle: new Set()
    };
    for (const v of (variants || [])) {
      const clusterIds = geneToClusters.get(v.gene) || [];
      const sev = v.severity || 0;
      const points = sev === 3 ? 4 : sev === 2 ? 2 : sev === 1 ? 1 : -0.5;
      for (const cid of clusterIds) {
        if (!loads[cid]) continue;
        loads[cid].score += points;
        loads[cid].variants.push(v);
        for (const x of (v.consider || [])) loads[cid].topActions.add(x);
        for (const x of (v.avoid || []))    loads[cid].topAvoid.add(x);
        for (const x of (v.lifestyle || [])) loads[cid].topLifestyle.add(x);
      }
    }
    // Cap and rank
    const ranked = Object.values(loads)
      .filter(l => l.score > 0)
      .sort((a, b) => b.score - a.score);
    return ranked;
  }

  // Top-5 priority actions, derived from highest-severity variants.
  // Each action carries: action text, which gene(s) it serves, why.
  function topPriorityActions(rep) {
    if (!rep.matchedVariants || !rep.matchedVariants.length) return [];

    const actions = [];
    // Bucket 1: severity-3 variants get their own dedicated action
    for (const v of rep.matchedVariants) {
      if (v.severity < 3) continue;
      if (actions.length >= 5) break;
      const first = (v.consider && v.consider[0]) || 'discuss with FM clinician';
      actions.push({
        head: v.gene + (v.oddsRatio ? ' (OR ' + v.oddsRatio.toFixed(2) + ')' : '') + ' — ' + first,
        why: v.detail || v.effect,
        gene: v.gene,
        priority: 100 - actions.length
      });
    }
    // Bucket 2: phenotype-ranked top atlas intervention (one per phenotype)
    if (actions.length < 5 && rep.topInterventions && rep.topInterventions.length) {
      for (const it of rep.topInterventions) {
        if (actions.length >= 5) break;
        const csrs = (it.node.sc && parseFloat(it.node.sc) > 0)
          ? ' (CSRS ' + parseFloat(it.node.sc).toFixed(1) + ')' : '';
        actions.push({
          head: it.node.l + csrs,
          why: 'Ranked for ' + it.forPhenotype,
          gene: '',
          priority: 50 - actions.length
        });
      }
    }
    return actions.slice(0, 5);
  }

  // What to avoid — collect from variants + add safety filters
  function topAvoidItems(rep) {
    const seen = new Set();
    const items = [];
    for (const v of (rep.matchedVariants || [])) {
      if (v.severity < 2) continue;
      for (const a of (v.avoid || [])) {
        const key = a.toLowerCase().replace(/[^a-z0-9]/g, '').slice(0, 30);
        if (seen.has(key)) continue;
        seen.add(key);
        items.push({ text: a, gene: v.gene });
        if (items.length >= 8) break;
      }
      if (items.length >= 8) break;
    }
    return items;
  }

  function renderSynthesis(rep) {
    const synthEl = document.getElementById('r-synth');
    // Only show synthesis if there's meaningful variant data
    if (!rep.matchedVariants || rep.matchedVariants.length < 3) {
      synthEl.style.display = 'none';
      return;
    }
    synthEl.style.display = 'block';

    // Headline
    const sev3 = rep.matchedVariants.filter(v => v.severity === 3).length;
    const sev2 = rep.matchedVariants.filter(v => v.severity === 2).length;
    const sev1 = rep.matchedVariants.filter(v => v.severity === 1).length;
    const prot = rep.matchedVariants.filter(v => v.severity === 0).length;
    const oor = rep.outOfRange.length;
    let headline;
    if (sev3 >= 3) {
      headline = 'Several high-impact variants surfaced — prioritize the top items below and bring the .md profile to your FM doctor.';
    } else if (sev3 >= 1) {
      headline = 'One or more high-impact variants surfaced — discuss the top items below with a functional medicine clinician.';
    } else if (sev2 >= 5) {
      headline = 'A cluster of moderately-elevated variants — lifestyle and supplement strategy below.';
    } else {
      headline = 'Most variants are mildly elevated. The atlas-ranked items below have the most defensible evidence base.';
    }
    document.getElementById('r-synth-headline').textContent = headline;

    // Top actions
    const actions = topPriorityActions(rep);
    document.getElementById('r-synth-actions').innerHTML = actions.length
      ? actions.map((a, i) => (
          '<div class="r-synth-action">' +
            '<span class="num">' + (i + 1) + '.</span>' +
            '<span class="body">' +
              '<div class="head">' + a.head + '</div>' +
              '<div class="why">' + (a.why || '') + '</div>' +
            '</span>' +
          '</div>'
        )).join('')
      : '<div class="r-empty">Not enough data to rank actions yet — upload more biomarkers or genetics.</div>';

    // Clusters
    const loads = clusterLoads(rep.matchedVariants);
    const topClusters = loads.slice(0, 6);
    document.getElementById('r-synth-clusters').innerHTML = topClusters.length
      ? topClusters.map(l => {
          const sevClass = l.score >= 6 ? 'sev-3' : l.score >= 3 ? 'sev-2' : '';
          const loadLabel = l.score >= 6 ? 'HIGH LOAD' : l.score >= 3 ? 'MODERATE' : 'mild';
          // Surface unique genes contributing
          const genes = Array.from(new Set(l.variants.map(v => v.gene))).join(' · ');
          return (
            '<div class="r-synth-cluster ' + sevClass + '">' +
              '<div class="r-synth-cluster-head">' +
                '<div class="r-synth-cluster-name">' + l.cluster.name + '</div>' +
                '<div class="r-synth-cluster-load">' + loadLabel + ' · ' + l.variants.length + ' var</div>' +
              '</div>' +
              '<div class="r-synth-cluster-genes">' + l.cluster.desc + ' · ' + genes + '</div>' +
            '</div>'
          );
        }).join('')
      : '<div class="r-empty">No clusters identified.</div>';

    // Tests
    const tests = (rep.topTests || []).slice(0, 5);
    document.getElementById('r-synth-tests').innerHTML = tests.length
      ? tests.map(tc => {
          const t = tc.node;
          const cost = t.cl ? '$' + t.cl + (t.ch && t.ch !== t.cl ? '–' + t.ch : '') : '';
          return (
            '<div class="r-synth-action">' +
              '<span class="body">' +
                '<div class="head">' + t.l + (cost ? '<span style="float:right;color:var(--gold);font-family:ui-monospace,monospace;font-size:12px;">' + cost + '</span>' : '') + '</div>' +
                '<div class="why">' +
                  (t.tr ? t.tr + ' · ' : '') +
                  (t.sm ? t.sm + ' · ' : '') +
                  'for ' + tc.forPhenotype +
                '</div>' +
              '</span>' +
            '</div>'
          );
        }).join('')
      : '<div class="r-empty">No tests ranked yet.</div>';

    // What to avoid
    const avoids = topAvoidItems(rep);
    document.getElementById('r-synth-avoid').innerHTML = avoids.length
      ? avoids.map(a =>
          '<li><strong>' + a.gene + ':</strong> ' + a.text + '</li>'
        ).join('')
      : '<li>No specific avoid items flagged from current variants.</li>';

    // Sources / verification stamp
    document.getElementById('r-synth-sources').innerHTML =
      'Verified against: ClinVar · PharmGKB / CPIC guidelines · GeneReviews (NCBI) · ' +
      'AAO Preferred Practice Patterns · MAPS for Autism Physicians framework · ' +
      'Walsh Research · Frye protocols (cerebral folate / leucovorin / mito) · ' +
      'Lynch \"Dirty Genes\" framework. ' +
      '<br>Cluster taxonomy: Walsh + Lynch + Yasko + Frye + MAPS · 9 functional axes. ' +
      '<br><br><strong>Allele encoding caveat:</strong> Some variants (e.g., SOD2 A16V, HFE) ' +
      'are reported on different strands by different platforms. If a result here seems opposite to your ' +
      'IntellxxDNA or 23andMe interpretation, verify the platform\'s strand convention.';
  }

  function renderReport() {
    const rep = generateReport();
    if (!rep) return false;

    // ── synthesis panel at top
    renderSynthesis(rep);

    // ── header sub
    const when = rep.genetics?.uploadedAt || Date.now();
    const ago = Math.round((Date.now() - when) / 1000);
    const agoStr = ago < 60 ? 'just now'
                 : ago < 3600 ? Math.round(ago / 60) + ' min ago'
                 : ago < 86400 ? Math.round(ago / 3600) + ' hr ago'
                 : Math.round(ago / 86400) + ' d ago';
    document.getElementById('r-sub').textContent = 'Generated · ' + agoStr;

    // ── Your data
    const summary = [];
    if (rep.matchedGeneCount > 0) {
      summary.push('<span class="pill">' + rep.matchedGeneCount + ' genes matched</span>');
    }
    if (rep.matchedVariants && rep.matchedVariants.length > 0) {
      summary.push('<span class="pill">' + rep.matchedVariants.length + ' actionable variants</span>');
    }
    if (rep.bioCount > 0) {
      summary.push('<span class="pill">' + rep.bioCount + ' biomarkers</span>');
    }
    if (rep.outOfRange.length > 0) {
      summary.push('<span class="pill">' + rep.outOfRange.length + ' out of range</span>');
    }
    let summaryText = summary.join(' ');
    if (rep.matchedGeneCount > 0) {
      const labels = [];
      for (const gid of (rep.genetics?.matchedGenes || [])) {
        const n = nodeMap.get(gid);
        if (n) labels.push(n.l);
        if (labels.length >= 12) break;
      }
      if (labels.length) {
        summaryText += '<div style="margin-top:10px;font-size:12px;color:var(--text-mute);line-height:1.55;">' +
          'Atlas genes detected: ' + labels.join(', ') +
          (rep.matchedGeneCount > labels.length ? ', and ' + (rep.matchedGeneCount - labels.length) + ' more' : '') +
          '</div>';
      }
    }
    document.getElementById('r-summary').innerHTML = summaryText || '<span class="r-empty">No data yet — close this and upload.</span>';

    // ── Top phenotypes
    const peHost = document.getElementById('r-phenotypes');
    if (rep.topPhenotypes.length === 0) {
      peHost.innerHTML = '<div class="r-empty">No phenotype matches yet — upload at least one biomarker or genetic file.</div>';
    } else {
      peHost.innerHTML = rep.topPhenotypes.map(p => {
        // Dedup contributing labels by name, keep top 5 by weight
        const seen = new Set();
        const top = [];
        for (const c of p.contribs.sort((a, b) => b.weight - a.weight)) {
          if (seen.has(c.label)) continue;
          seen.add(c.label); top.push(c.label);
          if (top.length >= 5) break;
        }
        const fill = Math.min(1, Math.max(0.06, p.score / Math.max(1, rep.topPhenotypes[0].score)));
        const atlasIdLine =
          '<div style="font-family:ui-monospace,monospace;font-size:9px;letter-spacing:0.22em;color:var(--text-vmute);text-transform:uppercase;margin-top:4px;">atlas · ' + p.id + '</div>';
        return (
          '<div class="r-phe">' +
            '<div class="r-phe-head">' +
              '<div class="r-phe-name">' + p.node.l + '</div>' +
              '<div class="r-phe-pct">' + p.pct + '%</div>' +
            '</div>' +
            '<div class="r-phe-evidence">Matches: ' + top.join(' · ') + '</div>' +
            atlasIdLine +
            '<div class="r-phe-bar"><div class="r-phe-bar-fill" style="--r-fill:' + fill + '"></div></div>' +
          '</div>'
        );
      }).join('');
    }

    // ── Gene variants (curated effect interpretations)
    const varHost = document.getElementById('r-variants');
    const varSection = document.getElementById('r-section-variants');
    if (!rep.matchedVariants || rep.matchedVariants.length === 0) {
      varSection.style.display = 'none';
    } else {
      varSection.style.display = '';
      varHost.innerHTML = rep.matchedVariants.map(v => {
        const sev = 'sev-' + v.severity;
        function rowFor(label, items, pillClass) {
          if (!items || !items.length) return '';
          const pills = items.map(it =>
            '<span class="pill' + (pillClass ? ' ' + pillClass : '') + '">' + it + '</span>'
          ).join('');
          return (
            '<div class="r-var-row">' +
              '<div class="r-var-row-label">' + label + '</div>' +
              '<div class="r-var-row-content">' + pills + '</div>' +
            '</div>'
          );
        }
        // atlasInts → atlas-intervention pills labeled by lookup
        const atlasIntLabels = (v.atlasInts || []).map(id => {
          const n = nodeMap.get(id);
          return n ? n.l + ' (' + id + ')' : id;
        });
        const consider = (v.consider || []).slice();
        if (atlasIntLabels.length) {
          for (const lbl of atlasIntLabels) consider.unshift(lbl);
        }
        const detailLine = v.detail
          ? '<div class="r-var-detail">' + v.detail + '</div>' : '';
        const roleLine = v.role
          ? '<div class="r-var-name" style="margin:0 0 8px 0;display:block;">' + v.role + '</div>'
          : '';
        const zygPill = v.zygosity === 'hom'
          ? 'homozygous'
          : v.zygosity === 'het' ? 'heterozygous' : v.zygosity;
        // Source attribution: IntellxxDNA variants get OR + provenance
        const srcLine = v.source
          ? '<div style="font-family:ui-monospace,monospace;font-size:9.5px;letter-spacing:0.18em;color:var(--text-vmute);text-transform:uppercase;margin-top:6px;">source: ' + v.source +
            (v.oddsRatio ? ' · OR ' + v.oddsRatio.toFixed(2) : '') +
            (v.prevalence ? ' · prevalence ' + v.prevalence : '') +
            '</div>'
          : '';
        return (
          '<div class="r-variant ' + sev + '">' +
            '<div class="r-var-head">' +
              '<div class="r-var-gene">' + v.gene +
                '<span class="r-var-name">' + v.name + '</span></div>' +
              '<div class="r-var-geno">' + v.genotype + ' · ' + zygPill + '</div>' +
            '</div>' +
            roleLine +
            '<div class="r-var-effect">' + v.effect + '</div>' +
            detailLine +
            rowFor('Consider', consider, 'atlas') +
            rowFor('Avoid', v.avoid) +
            rowFor('Lifestyle', v.lifestyle) +
            srcLine +
          '</div>'
        );
      }).join('');
    }

    // ── Out of range
    const oorHost = document.getElementById('r-oor');
    const oorSection = document.getElementById('r-section-oor');
    if (rep.outOfRange.length === 0) {
      oorSection.style.display = 'none';
    } else {
      oorSection.style.display = '';
      oorHost.innerHTML = rep.outOfRange.map(v => {
        const idLine = v.nodeId
          ? '<div style="grid-column:1/-1;font-family:ui-monospace,monospace;font-size:9px;letter-spacing:0.22em;color:var(--text-vmute);text-transform:uppercase;margin-top:-4px;margin-bottom:6px;">atlas · ' + v.nodeId + (v.source ? ' · ' + v.source : '') + '</div>'
          : (v.source ? '<div style="grid-column:1/-1;font-family:ui-monospace,monospace;font-size:9px;letter-spacing:0.22em;color:var(--text-vmute);text-transform:uppercase;margin-top:-4px;margin-bottom:6px;">source · ' + v.source + '</div>' : '');
        return (
          '<div class="r-oor-name">' + v.label + '</div>' +
          '<div class="r-oor-val">' + v.value + ' ' + (v.unit || '') + '</div>' +
          '<div class="r-oor-flag ' + v.flag + '">' + v.flag + '</div>' +
          idLine
        );
      }).join('');
    }

    // ── Top interventions
    const actHost = document.getElementById('r-actions');
    if (rep.topInterventions.length === 0) {
      actHost.innerHTML = '<div class="r-empty">No intervention rankings yet — add biomarker data for sharper ranking.</div>';
    } else {
      actHost.innerHTML = rep.topInterventions.map(it => {
        const i = it.node;
        const csrs = (i.sc && parseFloat(i.sc) > 0)
          ? '<span class="gold">CSRS ' + parseFloat(i.sc).toFixed(1) + '</span>' : '';
        const dose = i.do ? ' · ' + i.do : '';
        const cost = i.co ? ' · $' + i.co + '/mo' : '';
        const reg = i.rg ? ' · ' + i.rg.toUpperCase() : '';
        return (
          '<div class="r-int">' +
            '<div class="r-int-name">' + i.l + '</div>' +
            '<div class="r-int-meta">' +
              i.id + (csrs ? ' · ' + csrs : '') + (reg) +
            '</div>' +
            '<div class="r-int-rationale">' +
              'Ranked for ' + it.forPhenotype +
              (dose ? ' · dose: ' + i.do : '') +
              (cost ? ' · ~$' + i.co + '/mo' : '') +
            '</div>' +
          '</div>'
        );
      }).join('');
    }

    // ── Top tests
    const testHost = document.getElementById('r-tests');
    if (rep.topTests.length === 0) {
      testHost.innerHTML = '<div class="r-empty">No further tests prioritized — your current data is already covering the matched phenotypes well.</div>';
    } else {
      testHost.innerHTML = rep.topTests.map(tc => {
        const t = tc.node;
        const cost = t.cl
          ? '$' + t.cl + (t.ch && t.ch !== t.cl ? '–' + t.ch : '')
          : '';
        const meta = [];
        if (t.tr) meta.push(t.tr);
        if (t.sm) meta.push(t.sm);
        if (t.td) meta.push(t.td + 'd');
        if (t.dtc) meta.push('DTC');
        else if (t.rx) meta.push('Rx');
        meta.push('for ' + tc.forPhenotype);
        return (
          '<div class="r-test">' +
            '<div class="r-test-name">' + t.l + '</div>' +
            '<div class="r-test-cost">' + cost + '</div>' +
            '<div class="r-test-meta">' + meta.join(' · ') + '</div>' +
          '</div>'
        );
      }).join('');
    }

    return true;
  }

  // ── OBSIDIAN PROFILE EXPORTER ───────────────────────────────────
  // Generate a markdown profile that, when dropped into the vault,
  // produces a clickable patient sub-graph in Obsidian. Every match
  // becomes a wikilink to the canonical vault page name.

  // Build wikilink text. If the atlas ID resolves to a real vault page
  // (via VAULT_PATHS), use that filename so Obsidian opens the right page.
  // Falls back to a friendly stub link.
  function wlByID(id, friendlyLabel) {
    if (!id) return friendlyLabel || '';
    if (VAULT_PATHS[id]) {
      return '[[' + VAULT_PATHS[id] + ']]';
    }
    // Unresolved — use ID + label as a friendly stub
    if (friendlyLabel) {
      return '[[' + id + '|' + friendlyLabel + ']]';
    }
    return '[[' + id + ']]';
  }
  function wlGene(symbol) {
    if (!symbol) return '';
    const key = 'GENE:' + symbol.toUpperCase();
    if (VAULT_PATHS[key]) return '[[' + VAULT_PATHS[key] + ']]';
    return '[[' + symbol + ']]';
  }

  function generateObsidianProfile() {
    const rep = generateReport();
    if (!rep) return null;
    const now = new Date();
    const dateISO = now.toISOString().slice(0, 10);
    const lines = [];
    lines.push('---');
    lines.push('atlas-profile: causes-atlas');
    lines.push('generated: ' + now.toISOString());
    lines.push('source: client-side · localStorage');
    lines.push('tags: [patient-profile, atlas-derived]');
    lines.push('---');
    lines.push('');
    lines.push('# Patient profile · ' + dateISO);
    lines.push('');
    lines.push('> Generated by reading uploaded data against the Causes Atlas.');
    lines.push('> Every wikilink resolves to its atlas vault page. Open in Obsidian → graph view shows this patient\'s sub-network. Not medical advice.');
    lines.push('');
    lines.push('## Summary');
    lines.push('');
    if (rep.matchedGeneCount) lines.push('- **' + rep.matchedGeneCount + ' atlas genes matched**');
    if (rep.matchedVariants && rep.matchedVariants.length) lines.push('- **' + rep.matchedVariants.length + ' actionable variants**');
    if (rep.bioCount) lines.push('- **' + rep.bioCount + ' biomarkers measured**');
    if (rep.outOfRange.length) lines.push('- **' + rep.outOfRange.length + ' out of optimal range**');
    if (rep.genetics && rep.genetics.format) lines.push('- Genomics source: ' + rep.genetics.format);
    lines.push('');

    if (rep.topPhenotypes.length) {
      lines.push('## Top phenotype matches');
      lines.push('');
      for (const p of rep.topPhenotypes) {
        lines.push('### ' + wlByID(p.id, p.node.l) + ' · **' + p.pct + '%**');
        const contribs = p.contribs.slice(0, 6).map(c => c.label).join(' · ');
        if (contribs) lines.push('Matches: ' + contribs);
        lines.push('');
      }
    }

    if (rep.matchedVariants && rep.matchedVariants.length) {
      lines.push('## Gene variants');
      lines.push('');
      for (const v of rep.matchedVariants) {
        let header = '### ' + wlGene(v.gene) + ' · ' + v.name;
        if (v.zygosity) header += ' (' + v.zygosity + ')';
        if (v.oddsRatio) header += ' · OR ' + v.oddsRatio.toFixed(2);
        lines.push(header.trim());
        if (v.role) lines.push('*' + v.role + '*');
        lines.push('');
        lines.push('**Effect:** ' + v.effect);
        if (v.detail) { lines.push(''); lines.push(v.detail); }
        if (v.consider && v.consider.length) {
          lines.push(''); lines.push('**Consider:** ' + v.consider.join(' · '));
        }
        if (v.avoid && v.avoid.length) {
          lines.push('**Avoid:** ' + v.avoid.join(' · '));
        }
        if (v.lifestyle && v.lifestyle.length) {
          lines.push('**Lifestyle:** ' + v.lifestyle.join(' · '));
        }
        if (v.atlasInts && v.atlasInts.length) {
          const atlasInts = v.atlasInts.map(id => {
            const n = nodeMap.get(id);
            return wlByID(id, n ? n.l : id);
          }).join(' · ');
          lines.push('**Atlas interventions:** ' + atlasInts);
        }
        if (v.source) {
          lines.push('');
          lines.push('— source: ' + v.source +
            (v.prevalence ? ' · prevalence ' + v.prevalence : ''));
        }
        lines.push('');
      }
    }

    if (rep.outOfRange.length) {
      lines.push('## Out of optimal range');
      lines.push('');
      lines.push('| Biomarker | Value | Range | Flag | Source |');
      lines.push('|---|---|---|---|---|');
      for (const b of rep.outOfRange) {
        const link = b.nodeId ? wlByID(b.nodeId, b.label) : b.label;
        lines.push('| ' + link +
          ' | ' + b.value + ' ' + (b.unit || '') +
          ' | ' + (b.refRange || '') +
          ' | **' + (b.flag || '').toUpperCase() + '**' +
          ' | ' + (b.source || '') + ' |');
      }
      lines.push('');
    }

    if (rep.topInterventions.length) {
      lines.push('## What to discuss with your functional medicine doctor');
      lines.push('');
      for (const it of rep.topInterventions) {
        const i = it.node;
        let line = '- ' + wlByID(i.id, i.l);
        if (i.sc && parseFloat(i.sc) > 0) line += ' · **CSRS ' + parseFloat(i.sc).toFixed(1) + '**';
        line += ' · for ' + it.forPhenotype;
        if (i.do) line += '\n  · dose: ' + i.do;
        if (i.co) line += '\n  · cost: ~$' + i.co + '/mo';
        if (i.rg) line += '\n  · ' + i.rg.toUpperCase();
        lines.push(line);
      }
      lines.push('');
    }

    if (rep.topTests.length) {
      lines.push('## Tests to consider next');
      lines.push('');
      for (const tc of rep.topTests) {
        const t = tc.node;
        let line = '- ' + wlByID(t.id, t.l);
        if (t.cl) line += ' · $' + t.cl + (t.ch && t.ch !== t.cl ? '–' + t.ch : '');
        if (t.tr) line += ' · ' + t.tr;
        if (t.sm) line += ' · ' + t.sm;
        if (t.td) line += ' · ' + t.td + 'd turnaround';
        line += ' · for ' + tc.forPhenotype;
        lines.push(line);
      }
      lines.push('');
    }

    lines.push('## Atlas connection');
    lines.push('');
    lines.push('This profile was generated by reading uploaded data against the [[00_INDEX|Causes Atlas]] graph. Every wikilink above resolves to its atlas vault page.');
    lines.push('');
    lines.push('Calibration anchor: ' + wlByID('INT-0001', 'Leucovorin (folinic acid)') + ' · **CSRS 83.35** (non-drifted across major revisions).');
    lines.push('');
    lines.push('To explore in Obsidian:');
    lines.push('1. Drop this file into `vault/profiles/`');
    lines.push('2. Open in Obsidian → the graph view shows this patient\'s sub-network');
    lines.push('3. Click any wikilink to drill into the corresponding atlas page');
    lines.push('');
    lines.push('---');
    lines.push('');
    lines.push('*Not medical advice. Discuss with a licensed functional medicine practitioner familiar with the full clinical history. The atlas is for individual-level decisions, not population policy.*');
    lines.push('');
    return lines.join('\n');
  }

  function downloadObsidianProfile() {
    const md = generateObsidianProfile();
    if (!md) return;
    const blob = new Blob([md], { type: 'text/markdown;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    const dateISO = new Date().toISOString().slice(0, 10);
    a.href = url;
    a.download = 'atlas-profile-' + dateISO + '.md';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(() => URL.revokeObjectURL(url), 500);
  }

  // ── REPORT MODAL OPEN / CLOSE WIRING ────────────────────────────
  const reportOverlay = document.getElementById('report-overlay');
  const rClose       = document.getElementById('r-close');
  const rGraphBtn    = document.getElementById('r-graph');
  const rDownloadBtn = document.getElementById('r-download');
  const rReupBtn     = document.getElementById('r-reupload');
  const rObsidianBtn = document.getElementById('r-obsidian');
  const viewReportBtn = document.getElementById('view-report');

  function openReport() {
    if (!renderReport()) return;
    reportOverlay.classList.add('on');
    document.body.style.overflow = 'hidden';
  }
  function closeReport() {
    reportOverlay.classList.remove('on');
    document.body.style.overflow = '';
  }
  rClose.addEventListener('click', closeReport);
  rGraphBtn.addEventListener('click', closeReport);
  rDownloadBtn.addEventListener('click', () => window.print());
  rObsidianBtn.addEventListener('click', () => {
    rObsidianBtn.textContent = 'generating…';
    setTimeout(() => {
      downloadObsidianProfile();
      rObsidianBtn.textContent = 'Downloaded ✓';
      setTimeout(() => rObsidianBtn.textContent = 'Download Obsidian profile (.md)', 1800);
    }, 150);
  });
  rReupBtn.addEventListener('click', () => {
    closeReport();
    modal.classList.add('on');
  });
  viewReportBtn.addEventListener('click', openReport);
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && reportOverlay.classList.contains('on')) closeReport();
  });

  // Wire the "see all variants" toggle for the detail section
  const variantsToggle = document.getElementById('r-variants-toggle');
  if (variantsToggle) {
    variantsToggle.addEventListener('click', () => {
      const detail = document.getElementById('r-variants');
      const hidden = detail.classList.toggle('r-collapsed');
      variantsToggle.textContent = hidden
        ? 'Show all variants (detail view)'
        : 'Hide variant detail';
    });
  }

  // Show a brief "generating" state, then slide in the report
  const mGenerating = document.getElementById('m-generating');
  function showReportAfterSave() {
    // hide modal panes + tabs, show generating state
    document.querySelectorAll('.m-pane').forEach(p => p.classList.remove('on'));
    document.querySelector('.m-tabs').style.display = 'none';
    mGenerating.classList.add('on');
    setTimeout(() => {
      modal.classList.remove('on');
      mGenerating.classList.remove('on');
      document.querySelector('.m-tabs').style.display = '';
      // Re-show whichever pane the user was on (don't force-reset to PDF tab).
      // If none active for some reason, fall back to PDF.
      const anyTabOn = document.querySelector('.m-tab.on');
      if (!anyTabOn) {
        document.querySelector('.m-tab[data-pane="pdf"]').classList.add('on');
        document.getElementById('pane-pdf').classList.add('on');
      } else {
        const paneId = 'pane-' + anyTabOn.dataset.pane;
        document.getElementById(paneId).classList.add('on');
      }
      openReport();
    }, 1500);
  }
  window.__showReportAfterSave = showReportAfterSave;

  // tabs
  for (const t of document.querySelectorAll('.m-tab')) {
    t.addEventListener('click', () => {
      document.querySelectorAll('.m-tab').forEach(x => x.classList.remove('on'));
      document.querySelectorAll('.m-pane').forEach(p => p.classList.remove('on'));
      t.classList.add('on');
      document.getElementById('pane-' + t.dataset.pane).classList.add('on');
    });
  }

  // Freshness display + full-reset wiring
  const freshnessEl = document.getElementById('m-freshness');
  const resetAllBtn = document.getElementById('m-reset-all');
  function updateFreshness() {
    const s = getStored();
    if (!s.genetics && !s.biomarkers) {
      freshnessEl.textContent = 'no data uploaded yet';
      resetAllBtn.style.display = 'none';
      return;
    }
    const parts = [];
    if (s.genetics && s.genetics.uploadedAt) {
      const ago = Math.round((Date.now() - s.genetics.uploadedAt) / 86400000);
      parts.push('genetics · ' + (ago < 1 ? 'today' : ago + 'd ago'));
    }
    if (s.biomarkers) {
      parts.push('biomarkers · ' + Object.keys(s.biomarkers).length + ' entries');
    }
    freshnessEl.textContent = 'your stored data: ' + parts.join(' · ');
    resetAllBtn.style.display = 'inline-block';
  }
  resetAllBtn.addEventListener('click', () => {
    if (!confirm('Erase all uploaded data (genetics + biomarkers + variants)? This cannot be undone — the report will be empty until you upload again.')) return;
    localStorage.removeItem('cwa_genetics_v1');
    localStorage.removeItem('cwa_biomarkers_v1');
    // Reset form
    for (const input of bwForm.querySelectorAll('input')) {
      input.value = '';
      input.classList.remove('high', 'low');
    }
    if (pdfPaste) pdfPaste.value = '';
    pdfStatus.classList.remove('on');
    gStatus.classList.remove('on');
    if (gClear) gClear.style.display = 'none';
    updateBanner();
    applyUserData();
    updateFreshness();
    resetAllBtn.textContent = '✓ all data erased';
    setTimeout(() => resetAllBtn.textContent = 'Reset ALL my data (start fresh)', 2000);
  });

  // modal open/close
  btnUpload.addEventListener('click', () => { updateFreshness(); modal.classList.add('on'); });
  mClose.addEventListener('click', () => modal.classList.remove('on'));
  modal.addEventListener('click', e => {
    if (e.target === modal) modal.classList.remove('on');
  });
  // ESC closes
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && modal.classList.contains('on')) {
      modal.classList.remove('on');
    }
  });

  // ── GENETICS UPLOAD ────────────────────────────────────────────
  const gDrop   = document.getElementById('g-drop');
  const gFile   = document.getElementById('g-file');
  const gStatus = document.getElementById('g-status');
  const gClear  = document.getElementById('g-clear');

  gDrop.addEventListener('click', () => gFile.click());
  gDrop.addEventListener('dragover', e => { e.preventDefault(); gDrop.classList.add('drag'); });
  gDrop.addEventListener('dragleave', () => gDrop.classList.remove('drag'));
  gDrop.addEventListener('drop', e => {
    e.preventDefault(); gDrop.classList.remove('drag');
    if (e.dataTransfer.files.length) handleGeneticsFile(e.dataTransfer.files[0]);
  });
  gFile.addEventListener('change', e => {
    if (e.target.files.length) handleGeneticsFile(e.target.files[0]);
  });
  gClear.addEventListener('click', () => {
    localStorage.removeItem('cwa_genetics_v1');
    updateBanner(); applyUserData();
    gStatus.classList.remove('on');
    gClear.style.display = 'none';
  });

  function handleGeneticsFile(file) {
    gStatus.classList.remove('err');
    gStatus.classList.add('on');
    gStatus.textContent = 'parsing ' + file.name + ' (' + Math.round(file.size/1024) + ' KB)…';
    const reader = new FileReader();
    reader.onload = e => {
      try {
        const res = parseGenetics(e.target.result);
        if (!res.variants.length) {
          gStatus.classList.add('err');
          gStatus.textContent = 'could not recognize this file format. supported: 23andMe, AncestryDNA, MyHeritage, VCF';
          return;
        }
        const { matchedGenes, matchedVariants } = matchVariantsToAtlas(res.variants);
        if (matchedGenes.length === 0 && matchedVariants.length === 0) {
          gStatus.classList.add('err');
          gStatus.textContent = res.format + ' · ' +
            res.variants.length.toLocaleString() + ' variants read · 0 matched. ' +
            'This file may use a chip that excludes the rsIDs the atlas tracks — try uploading a PDF report from the same provider.';
          return;
        }
        gStatus.textContent = res.format + ' · ' +
          res.variants.length.toLocaleString() + ' variants read · ' +
          matchedGenes.length + ' genes · ' + matchedVariants.length + ' actionable variants · generating your report…';
        saveGenetics({
          format: res.format,
          uploadedAt: Date.now(),
          variantCount: res.variants.length,
          matchedGenes: matchedGenes,
          matchedVariants: matchedVariants
        });
        gClear.style.display = 'inline-block';
        setTimeout(() => window.__showReportAfterSave && window.__showReportAfterSave(), 900);
      } catch (err) {
        gStatus.classList.add('err');
        gStatus.textContent = 'parse error: ' + (err.message || err);
      }
    };
    reader.readAsText(file);
  }

  function parseGenetics(text) {
    const head = text.slice(0, 3000);
    let format = 'unknown';
    if (/23andMe/i.test(head))                       format = '23andMe';
    else if (/AncestryDNA/i.test(head))              format = 'AncestryDNA';
    else if (/MyHeritage/i.test(head))               format = 'MyHeritage';
    else if (/^##fileformat=VCF/im.test(head))       format = 'VCF';
    else if (/^#?\s*rsid\b/im.test(head))            format = '23andMe-like';

    const variants = [];
    const lines = text.split('\n');

    function normGenotype(gt) {
      // Strip non-letter chars, uppercase, sort letters alphabetically so
      // "TC" → "CT", "CT" → "CT", "T C" → "CT".
      if (!gt) return '';
      const letters = gt.replace(/[^ACGT]/gi, '').toUpperCase().split('');
      if (letters.length < 2) return letters.join('');
      return letters.sort().join('').slice(0, 2);
    }

    if (format === 'VCF') {
      for (const line of lines) {
        if (!line || line.startsWith('#')) continue;
        const parts = line.split('\t');
        if (parts.length < 8) continue;
        const rsid = parts[2] || '';
        const ref = (parts[3] || '').toUpperCase();
        const alt = (parts[4] || '').toUpperCase();
        const info = parts[7] || '';
        let gene = '';
        const m = info.match(/(?:^|;)(?:GENE|GENEINFO|gene_symbol|Gene)=([A-Z0-9\-]+)/i);
        if (m) gene = m[1].toUpperCase();
        if (!gene) {
          const a = info.match(/ANN=[^|]*\|[^|]*\|[^|]*\|([A-Z0-9\-]+)/i);
          if (a) gene = a[1].toUpperCase();
        }
        // VCF GT field — parts[8] is FORMAT, parts[9..] are samples
        let gt = '';
        if (parts[8] && parts[9]) {
          const formatFields = parts[8].split(':');
          const sampleFields = parts[9].split(':');
          const gtIdx = formatFields.indexOf('GT');
          if (gtIdx >= 0) {
            const gtStr = sampleFields[gtIdx] || '';
            // 0/0 = wild homo, 0/1 = het, 1/1 = alt homo
            if (gtStr.includes('0/0') || gtStr.includes('0|0')) gt = ref + ref;
            else if (gtStr.includes('1/1') || gtStr.includes('1|1')) gt = alt + alt;
            else if (/[01][\/|][01]/.test(gtStr)) gt = ref + alt;
          }
        }
        variants.push({ rsid, gene, genotype: normGenotype(gt) });
      }
    } else if (format === 'MyHeritage') {
      for (const line of lines) {
        if (!line || line.startsWith('#') || /^"?RSID/i.test(line)) continue;
        const parts = line.replace(/"/g,'').split(',');
        if (parts.length < 5) continue;
        const a1 = (parts[3] || '').toUpperCase();
        const a2 = (parts[4] || '').toUpperCase();
        variants.push({ rsid: parts[0], genotype: normGenotype(a1 + a2) });
      }
    } else {
      for (const line of lines) {
        if (!line || line.startsWith('#')) continue;
        const parts = line.split(/\s+/);
        if (parts.length < 4) continue;
        if (parts[0] === 'rsid' || parts[0] === 'RSID') continue;
        // 23andMe: rsid chrom pos genotype (2-letter)
        // AncestryDNA: rsid chrom pos allele1 allele2
        let gt;
        if (parts.length >= 5 && parts[3].length === 1 && parts[4].length === 1) {
          gt = parts[3] + parts[4];
        } else {
          gt = parts[3];
        }
        variants.push({ rsid: parts[0], genotype: normGenotype(gt) });
      }
    }
    return { format, variants };
  }

  // Returns { matchedGenes: [id, ...], matchedVariants: [{rsid, gene, name, role,
  // genotype, severity, effect, detail, do, av, li, atlasInts}, ...] }
  function matchVariantsToAtlas(variants) {
    const geneIds = new Set();
    const matchedVariants = [];
    const seenRsids = new Set();
    for (const v of variants) {
      // Avoid duplicates (some files list rsIDs more than once)
      if (v.rsid && seenRsids.has(v.rsid)) continue;
      if (v.rsid) seenRsids.add(v.rsid);

      // VCF gene= header
      if (v.gene) {
        const gid = geneByLabel[v.gene];
        if (gid) geneIds.add(gid);
      }

      // rsid → gene
      let sym = null;
      if (v.rsid && RSID_TO_GENE[v.rsid]) {
        sym = RSID_TO_GENE[v.rsid];
        const gid = geneByLabel[sym];
        if (gid) geneIds.add(gid);
      }

      // rsid + genotype → curated variant interpretation
      if (v.rsid && v.genotype && VARIANT_DB[v.rsid]) {
        const def = VARIANT_DB[v.rsid];
        const effects = def.e || {};
        const eff = effects[v.genotype];
        if (eff && eff.sev > 0) {     // only report variants of any effect
          matchedVariants.push({
            rsid:     v.rsid,
            gene:     def.g,
            name:     def.n,
            role:     def.r || '',
            genotype: v.genotype,
            zygosity: eff.f,
            severity: eff.sev,
            effect:   eff.msg,
            detail:   eff.d || '',
            consider: eff.do || [],
            avoid:    eff.av || [],
            lifestyle:eff.li || [],
            atlasInts:eff.ai || []
          });
        }
      }
    }
    // Sort variants by severity (high first), then gene name
    matchedVariants.sort((a, b) => b.severity - a.severity || a.gene.localeCompare(b.gene));
    return { matchedGenes: Array.from(geneIds), matchedVariants };
  }

  // ── BLOOD-WORK FORM ────────────────────────────────────────────
  const bwSave  = document.getElementById('bw-save');
  const bwClear = document.getElementById('bw-clear');

  function loadStoredBiomarkers() {
    const s = getStored();
    if (s.biomarkers) {
      for (const k of Object.keys(s.biomarkers)) {
        const input = bwForm.querySelector('input[data-k="' + k + '"]');
        if (input) {
          input.value = s.biomarkers[k].value;
          flagInput(input, s.biomarkers[k].flag);
        }
      }
    }
  }
  function flagInput(input, flag) {
    input.classList.remove('high', 'low');
    if (flag === 'high') input.classList.add('high');
    else if (flag === 'low') input.classList.add('low');
  }
  loadStoredBiomarkers();

  function findBiomarkerNodeId(field) {
    const lcLabel = field.l.toLowerCase();
    if (bioByLabel[lcLabel]) return bioByLabel[lcLabel];
    for (const alias of (field.a || [])) {
      const lcAlias = alias.toLowerCase();
      for (const bk of Object.keys(bioByLabel)) {
        if (bk.indexOf(lcAlias) >= 0) return bioByLabel[bk];
      }
    }
    return null;
  }

  bwSave.addEventListener('click', () => {
    // Preserve any biomarkers extracted from PDFs that aren't in the form
    // (e.g. OAT organic acids, raw Ulta labels). Merge form values on top.
    const out = JSON.parse(localStorage.getItem('cwa_biomarkers_v1') || '{}');
    let any = Object.keys(out).length > 0;
    for (const f of BIOMARKER_FIELDS) {
      const input = bwForm.querySelector('input[data-k="' + f.k + '"]');
      if (!input || !input.value) continue;
      const v = parseFloat(input.value);
      if (Number.isNaN(v)) continue;
      let flag = 'normal';
      if (v < f.rL) flag = 'low';
      else if (v > f.rH) flag = 'high';
      flagInput(input, flag);
      out[f.k] = {
        value: v, unit: f.u, flag, label: f.l,
        refRange: f.rL + '-' + f.rH,
        source: 'manual entry',
        nodeId: findBiomarkerNodeId(f)
      };
      any = true;
    }
    saveBiomarkers(out);
    if (any) {
      window.__showReportAfterSave && window.__showReportAfterSave();
    } else {
      bwSave.textContent = 'add at least one value';
      setTimeout(() => bwSave.textContent = 'save & generate my report', 1800);
    }
  });

  bwClear.addEventListener('click', () => {
    localStorage.removeItem('cwa_biomarkers_v1');
    for (const input of bwForm.querySelectorAll('input')) {
      input.value = '';
      input.classList.remove('high', 'low');
    }
    updateBanner(); applyUserData();
  });

  // ── PDF UPLOAD + PASTE EXTRACTION ──────────────────────────────
  const pdfPaste   = document.getElementById('pdf-paste');
  const pdfExtract = document.getElementById('pdf-extract');
  const pdfStatus  = document.getElementById('pdf-status');
  const pdfDrop    = document.getElementById('pdf-drop');
  const pdfFile    = document.getElementById('pdf-file');

  // Build a gene-symbol set for matching gene mentions in PDF text.
  // Strict word-boundary, uppercase-only — gene symbols look like
  // [A-Z][A-Z0-9-]{1,8}. This keeps false positives near zero.
  const ATLAS_GENE_SYMBOLS = new Set(Object.keys(geneByLabel));

  // PDF.js is lazy-loaded only when the user actually uploads a PDF
  let _pdfJsLoading = null;
  function ensurePdfJs() {
    if (window.pdfjsLib) return Promise.resolve(window.pdfjsLib);
    if (_pdfJsLoading)   return _pdfJsLoading;
    _pdfJsLoading = new Promise((resolve, reject) => {
      const s = document.createElement('script');
      s.src = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js';
      s.crossOrigin = 'anonymous';
      s.onload = () => {
        try {
          window.pdfjsLib.GlobalWorkerOptions.workerSrc =
            'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
          resolve(window.pdfjsLib);
        } catch (e) { reject(e); }
      };
      s.onerror = () => reject(new Error('failed to load PDF parser from CDN'));
      document.head.appendChild(s);
    });
    return _pdfJsLoading;
  }

  pdfDrop.addEventListener('click', () => pdfFile.click());
  pdfDrop.addEventListener('dragover', e => { e.preventDefault(); pdfDrop.classList.add('drag'); });
  pdfDrop.addEventListener('dragleave', () => pdfDrop.classList.remove('drag'));
  pdfDrop.addEventListener('drop', e => {
    e.preventDefault(); pdfDrop.classList.remove('drag');
    if (e.dataTransfer.files.length) handlePdfFiles(Array.from(e.dataTransfer.files));
  });
  pdfFile.addEventListener('change', e => {
    if (e.target.files.length) handlePdfFiles(Array.from(e.target.files));
  });

  async function handlePdfFiles(files) {
    pdfStatus.classList.add('on');
    pdfStatus.classList.remove('err');
    pdfStatus.textContent = 'loading PDF parser…';
    try {
      const pdfjs = await ensurePdfJs();
      let allText = '';
      let totalPages = 0;
      for (let fi = 0; fi < files.length; fi++) {
        const file = files[fi];
        pdfStatus.textContent = 'reading ' + file.name + ' (' + Math.round(file.size/1024) + ' KB)…';
        const buf = await file.arrayBuffer();
        const pdf = await pdfjs.getDocument({ data: buf }).promise;
        for (let p = 1; p <= pdf.numPages; p++) {
          pdfStatus.textContent = 'file ' + (fi+1) + '/' + files.length +
            ' · page ' + p + '/' + pdf.numPages + ' · ' + file.name;
          const page = await pdf.getPage(p);
          const content = await page.getTextContent();
          allText += content.items.map(it => it.str).join(' ') + '\n';
          totalPages++;
        }
      }
      if (!allText || allText.length < 50) {
        pdfStatus.classList.add('err');
        pdfStatus.textContent = 'this PDF has no extractable text layer (probably a scan). Paste the lab text manually using the box below.';
        return;
      }
      const result = extractFromText(allText);
      // Pretty doc-type label for the status line
      const docTypeLabel = ({
        intellxx: 'IntellxxDNA genomics report',
        truhealth: 'TruHealth epigenetic report',
        metabolomics: 'Diagnostic Solutions OMX metabolomics',
        ulta: 'Ulta Lab Tests / Quest blood work',
        quest_or_labcorp: 'Quest / LabCorp blood work',
        '23andme_report': '23andMe health report',
        galleri: 'Galleri (cfDNA methylation)',
        generic: 'general PDF'
      })[result.docType] || result.docType;
      const summary = [
        'detected: ' + docTypeLabel,
        files.length + ' PDF' + (files.length>1?'s':''),
        totalPages + ' pages',
        result.bioCount + ' biomarker' + (result.bioCount===1?'':'s'),
        result.geneCount + ' gene' + (result.geneCount===1?'':'s'),
        result.matchedVariants.length + ' variant' + (result.matchedVariants.length===1?'':'s')
      ].join(' · ');
      pdfStatus.textContent = summary;

      // TruHealth fallback — empty extraction means font-encoding bug
      if (result.docType === 'truhealth' && result.bioCount === 0) {
        pdfStatus.classList.add('err');
        pdfStatus.textContent = 'TruHealth PDFs use font-subset encoding that this parser can\'t fully read. We detected the format but couldn\'t extract values automatically. Please enter your key markers (Vitamin A, B-vitamins, Toxins, Stress, etc.) manually in the Blood Work tab.';
        return;
      }

      // Merge matched genes into genetics store
      if (result.geneCount > 0 || result.matchedVariants.length > 0) {
        const existing = JSON.parse(localStorage.getItem('cwa_genetics_v1') || 'null') || {
          format: docTypeLabel, uploadedAt: Date.now(),
          variantCount: 0, matchedGenes: [], matchedVariants: []
        };
        const gset = new Set(existing.matchedGenes);
        for (const gid of result.matchedGenes) gset.add(gid);
        existing.matchedGenes = Array.from(gset);
        // Dedup variants by gene+effect signature
        const vSeen = new Set(
          (existing.matchedVariants || []).map(v => v.gene + '|' + v.genotype + '|' + (v.oddsRatio || ''))
        );
        const merged = (existing.matchedVariants || []).slice();
        for (const v of result.matchedVariants) {
          const sig = v.gene + '|' + v.genotype + '|' + (v.oddsRatio || '');
          if (vSeen.has(sig)) continue;
          vSeen.add(sig);
          merged.push(v);
        }
        merged.sort((a, b) =>
          (b.severity || 0) - (a.severity || 0) ||
          (b.oddsRatio || 0) - (a.oddsRatio || 0));
        existing.matchedVariants = merged;
        existing.uploadedAt = Date.now();
        existing.format = docTypeLabel;
        saveGenetics(existing);
      }

      // Auto-save extracted biomarkers (both form-mapped and arbitrary)
      if (result.bioCount > 0) {
        const out = JSON.parse(localStorage.getItem('cwa_biomarkers_v1') || '{}');
        for (const b of result.biomarkers) {
          out[b.key] = {
            value: b.value, unit: b.unit, flag: b.flag,
            label: b.label, refRange: b.refRange,
            source: b.source,
            nodeId: findBiomarkerNodeIdByLabel(b.label)
          };
        }
        saveBiomarkers(out);
      }
      if (result.bioCount > 0 || result.geneCount > 0 || result.matchedVariants.length > 0) {
        setTimeout(() => window.__showReportAfterSave && window.__showReportAfterSave(), 1100);
      } else {
        pdfStatus.classList.add('err');
        pdfStatus.textContent = summary + ' — nothing matched. Try a different file or use the blood-work form.';
      }
    } catch (err) {
      pdfStatus.classList.add('err');
      pdfStatus.textContent = 'parse error: ' + (err.message || err);
    }
  }

  // Helper: find biomarker node by free-text label (handles arbitrary
  // extracted labels like "Hydroxykynurenine" that aren't in the curated form)
  function findBiomarkerNodeIdByLabel(label) {
    if (!label) return null;
    const lc = label.toLowerCase();
    if (bioByLabel[lc]) return bioByLabel[lc];
    // try substring match
    for (const bk of Object.keys(bioByLabel)) {
      if (bk.indexOf(lc) >= 0 || lc.indexOf(bk) >= 0) return bioByLabel[bk];
    }
    return null;
  }

  // ── DOCUMENT-TYPE CLASSIFIER ────────────────────────────────────
  // Detects the report provider from text signatures and dispatches
  // to a format-specific parser. Critical because one regex on
  // everything produces nonsense readings ("Copper 2000 μg/dL").
  function detectDocType(text) {
    const head = text.slice(0, 4000);
    if (/IntellxxDNA|Intelligent\s+Science\.\s+Intelligent\s+Living|IXXD/i.test(head)) return 'intellxx';
    if (/TruHealth|TruDiagnostic|trudiagnostic\.com/i.test(head)) return 'truhealth';
    if (/Diagnostic\s+Solutions\s+Laboratory|nmol\/mg\s+Creatinine|METABOLOMIC\s+SIGNATURE|OMX\s+Urine/i.test(text.slice(0, 8000))) return 'metabolomics';
    if (/Ulta\s+Lab\s+Tests|UltaLabTests\.com/i.test(head)) return 'ulta';
    if (/Quest\s+Diagnostics|LabCorp|Laboratory\s+Corporation/i.test(head)) return 'quest_or_labcorp';
    if (/23andMe|raw\s+genetic\s+data/i.test(head)) return '23andme_report';
    if (/Galleri|methylated\s+cfDNA/i.test(head)) return 'galleri';
    return 'generic';
  }

  // ── INTELLXXDNA PARSER ──────────────────────────────────────────
  // Pattern: GENE  ALLELE  PREVALENCE%  N_VARIANTS  ODDS_RATIO
  // Sample/template genes shown in the intro pages are skipped.
  // Each real variant becomes a matchedVariant with the OR translated
  // into severity (OR >= 2 = sev 3, 1.5-2 = sev 2, 1-1.5 = sev 1, <1 = benefit).
  const INTELLXX_SAMPLE_GENES = new Set(['TIMP2','FGG','CETP','5HT2A','GABRA2']);
  // Curated interpretations for IntellxxDNA's high-impact variants.
  // Where the source PDF has its own recommendations we surface them
  // alongside our atlas-based notes. Conservative claims; clinician-bound.
  const INTELLXX_NOTES = {
    'F5':   { name:'Factor V Leiden', role:'Coagulation · heritable hypercoagulability',
              detail:'Heterozygote VTE risk roughly 4–7× baseline; on combined estrogen OCs/HRT, VTE risk jumps to 11–41× baseline. ACOG considers estrogen-containing contraceptives contraindicated in F5 carriers WITH prior VTE or strong family history; asymptomatic heterozygotes should make informed-choice decisions with their clinician (progestin-only, IUD, or non-hormonal options are preferred).',
              consider:['HEMATOLOGY CONSULTATION before surgery or pregnancy','Discuss anticoagulation prophylaxis around surgery / long-haul travel with clinician','Pycnogenol may have modest platelet-aggregation benefit (adjunct only)','Nattokinase / lumbrokinase NOT validated as clinical anticoagulants — adjunct discussion only with clinician'],
              avoid:['Combined estrogen-containing OCs / HRT without hematology guidance','Corticosteroids without clinician oversight','Prolonged immobility'],
              lifestyle:['Compression stockings on long flights','Adequate hydration','Surgical / pregnancy prophylaxis discussion mandatory'] },
    'F11':  { name:'Factor XI', role:'Coagulation',
              detail:'Modulates thrombin generation. Elevation increases clotting risk; protective allele exists.',
              consider:['Nattokinase, lumbrokinase, bromelain','Curcumin','Vitamin E'] },
    'IL6':  { name:'Interleukin-6', role:'Pro-inflammatory cytokine',
              detail:'IL-6 upregulation phenotype; platelet activation and inflammatory load.',
              consider:['Curcumin','Resveratrol','Omega-3 DHA','Pycnogenol','Berberine'],
              lifestyle:['Anti-inflammatory diet','Stress regulation','Quality sleep'] },
    'ABO':  { name:'ABO Blood Group', role:'Hematology',
              detail:'Non-O blood types associate with higher Von Willebrand factor and stickier platelets.',
              consider:['Pycnogenol, curcumin, bromelain, rutin, luteolin','Nattokinase'] },
    'SERPINC1':{ name:'Antithrombin III', role:'Coagulation',
              detail:'Lower antithrombin → higher fibrin and clotting tendency.',
              consider:['Pycnogenol','Nattokinase','Quercetin','Curcumin'] },
    'TNF':  { name:'TNF-α', role:'Pro-inflammatory cytokine',
              detail:'Materially higher inflammatory cytokine output.',
              consider:['Curcumin','Resveratrol','Omega-3','Boswellia'],
              avoid:['Heavy seed oil intake'] },
    'IL1A': { name:'Interleukin-1α', role:'Inflammation',
              detail:'Higher IL-1α expression; relevant for chronic inflammatory states.',
              consider:['Curcumin','Quercetin','Omega-3'] },
    'IL1B': { name:'Interleukin-1β', role:'Inflammation',
              detail:'Higher IL-1β; NLRP3 inflammasome relevance.',
              consider:['Curcumin','Sulforaphane','Quercetin'] },
    'IL33': { name:'Interleukin-33', role:'Alarmin / mucosal immunity',
              detail:'IL-33 modulation; allergic/asthma + tissue-repair relevance.' },
    'IL1RL1':{ name:'IL-33 receptor (ST2)', role:'Inflammation receptor' },
    'ICAM1':{ name:'ICAM-1', role:'Vascular adhesion',
              detail:'Endothelial adhesion molecule; cardiovascular and inflammatory.' },
    'TOMM40':{ name:'TOMM40', role:'Mitochondrial import + APOE-linked',
              detail:'Tightly linked to APOE locus; relevant for cognitive aging.',
              consider:['DHA-rich omega-3','Mediterranean-leaning diet','Aerobic exercise'] },
    'GCLC': { name:'Glutamate-cysteine ligase', role:'Glutathione synthesis',
              detail:'Rate-limiting for glutathione synthesis. Variants impair detox + redox.',
              consider:['NAC 600-1200 mg','Liposomal glutathione','Sulforaphane (broccoli sprouts)','Glycine + cysteine + glutamine'] },
    'GPX1': { name:'Glutathione peroxidase 1', role:'Antioxidant · selenium-dependent',
              detail:'Variants reduce peroxide clearance.',
              consider:['Selenium 100-200 mcg (brazil nuts)','NAC','Vitamin E mixed tocopherols'] },
    'CFH':  { name:'Complement Factor H', role:'AMD / complement regulation',
              detail:'Y402H variant raises age-related macular degeneration risk substantially.',
              consider:['Lutein 10 mg + Zeaxanthin 2 mg','Omega-3 DHA','Zinc 25 mg + copper 2 mg'],
              lifestyle:['UV-protective eyewear','Smoking cessation','Annual eye exam'] },
    'STAT3':{ name:'STAT3', role:'JAK-STAT inflammatory signaling' },
    'CYP1A2':{ name:'CYP1A2', role:'Caffeine + xenobiotic metabolism',
              detail:'Slow metabolizer phenotype; caffeine half-life extended.',
              avoid:['Excess caffeine','High char-grilled meat'] },
    'CYP19A1':{ name:'Aromatase', role:'Estrogen biosynthesis' },
    'NOS3': { name:'Endothelial NOS', role:'Nitric oxide / vascular',
              detail:'Reduced eNOS activity; cardiovascular endothelial relevance.',
              consider:['Beetroot / dietary nitrate','L-arginine + L-citrulline','Pycnogenol'] },
    'TCF7L2':{ name:'TCF7L2', role:'Wnt / insulin secretion',
              detail:'Strong T2D risk variant. Insulin sensitivity matters more than usual.',
              consider:['Berberine 500 mg 2-3x','Inositol','Cinnamon'],
              lifestyle:['Continuous glucose monitoring trial','Resistance training','Low-glycemic eating'] },
    'KCNJ11':{ name:'KCNJ11', role:'Pancreatic K-ATP channel · diabetes' },
    'KCNQ1':{ name:'KCNQ1', role:'Cardiac K+ channel · long-QT / diabetes' },
    'ADIPOQ':{ name:'Adiponectin', role:'Insulin sensitivity adipokine' },
    'PPARGC1A':{ name:'PGC-1α', role:'Mitochondrial biogenesis',
              detail:'Master regulator of mitochondrial biogenesis. Variants reduce mito quality + endurance capacity.',
              consider:['CoQ10 100-200 mg','PQQ 20 mg','Resveratrol','Cold exposure (mito biogenesis cue)'],
              lifestyle:['Zone-2 cardio (mito biogenesis)','Resistance training','Adequate sleep'] },
    'IGF1': { name:'IGF-1', role:'Growth factor / longevity tradeoff' },
    'SLC30A8':{ name:'Zinc transporter 8', role:'Pancreatic β-cell zinc handling' },
    'LEPR': { name:'Leptin receptor', role:'Satiety / energy balance' },
    'MC1R': { name:'Melanocortin-1 receptor', role:'Pigment + sun sensitivity',
              detail:'Variants associated with fair skin, melanoma risk, anesthesia sensitivity.',
              consider:['Vitamin D (sun-conscious)','Polypodium leucotomos'],
              lifestyle:['Strict sun protection','Annual skin check'] },
    'ZFHX3':{ name:'ZFHX3', role:'Atrial fibrillation / cardiac' },
    'PEMT': { name:'PEMT', role:'Choline / phosphatidylcholine synthesis',
              detail:'Variants increase choline requirements; relevant for liver and brain.',
              consider:['Choline 425-550 mg','Phosphatidylcholine','Eggs'] },
    'PICALM':{ name:'PICALM', role:'Endocytosis · cognitive aging' },
    'CLPTM1L':{ name:'CLPTM1L', role:'Telomerase / lung cancer risk' },
    'ENPP1':{ name:'ENPP1', role:'Insulin signaling' },
    'FOXO3':{ name:'FOXO3', role:'Longevity transcription factor' },
    'GCLM': { name:'Glutamate-cysteine ligase modifier', role:'Glutathione synthesis cofactor' },
    'PON1': { name:'Paraoxonase 1', role:'Organophosphate detox',
              detail:'Variants alter pesticide and lipid-peroxide clearance.',
              avoid:['Pesticide-treated produce (EWG dirty dozen)','Lawn chemicals'],
              consider:['Mediterranean diet','Quercetin'] },
    'STAT1':{ name:'STAT1', role:'Interferon signaling' },
    'C677T':{ name:'MTHFR C677T', role:'Folate cycle (alias label, see MTHFR)' },
    'V158M':{ name:'COMT V158M', role:'Catecholamine clearance (alias label)' },
    'A16V': { name:'SOD2 A16V', role:'Mitochondrial SOD2 (alias label)' },
    'Y402H':{ name:'CFH Y402H', role:'AMD complement (alias label)' },
    'I405V':{ name:'CETP I405V', role:'HDL / longevity (alias label)' }
  };

  function parseIntellxxDNA(text) {
    const variants = [];
    const matchedGenes = new Set();
    // Strict table-row pattern: GENE_TOKEN  ALLELE  PREVALENCE%  N_VARIANTS  ODDS_RATIO
    const re = /\b([A-Z][A-Z0-9]{1,9})\s+([ACGT])\s+(\d+(?:\.\d+)?\s*%?)\s+(\d+)\s+(\d+\.\d+)\b/g;
    const seen = new Set();
    let m;
    while ((m = re.exec(text)) !== null) {
      const gene = m[1];
      const allele = m[2];
      const prevalence = m[3];
      const nVars = parseInt(m[4], 10);
      const odds = parseFloat(m[5]);
      if (INTELLXX_SAMPLE_GENES.has(gene)) continue;
      if (odds < 0 || odds > 50) continue;       // sanity
      if (nVars > 4 || nVars < 1) continue;
      const key = gene + ':' + allele + ':' + odds.toFixed(2);
      if (seen.has(key)) continue;
      seen.add(key);

      // gene → atlas match
      const gid = geneByLabel[gene];
      if (gid) matchedGenes.add(gid);

      // severity from odds ratio
      let severity;
      if (odds >= 2.5)      severity = 3;
      else if (odds >= 1.5) severity = 2;
      else if (odds >= 1.0) severity = 1;
      else                  severity = 0; // benefit (skip from report unless we want to show)

      const interp = INTELLXX_NOTES[gene] || null;
      // Build variant object — preserve OR for transparency
      variants.push({
        rsid: '',
        gene: gene,
        name: (interp && interp.name) || gene,
        role: (interp && interp.role) || '',
        genotype: allele + ' allele',
        zygosity: nVars === 2 ? 'hom' : nVars === 1 ? 'het' : '',
        severity: severity,
        effect: 'Odds ratio ' + odds.toFixed(2) + ' · ' + (
          odds >= 2.5 ? 'significantly elevated risk' :
          odds >= 1.5 ? 'moderately elevated risk' :
          odds >= 1.0 ? 'mildly elevated risk' :
                        'protective variant'),
        detail: (interp && interp.detail) || '',
        consider: (interp && interp.consider) || [],
        avoid:    (interp && interp.avoid) || [],
        lifestyle:(interp && interp.lifestyle) || [],
        atlasInts:(interp && interp.atlasInts) || [],
        source: 'IntellxxDNA',
        oddsRatio: odds,
        prevalence: prevalence,
        variantCount: nVars
      });
    }
    // Sort by severity desc, then by OR desc
    variants.sort((a, b) =>
      b.severity - a.severity ||
      (b.oddsRatio || 0) - (a.oddsRatio || 0));
    return { matchedGenes: Array.from(matchedGenes), matchedVariants: variants };
  }

  // ── ULTA / QUEST CLIA PARSER ───────────────────────────────────
  // Pattern (per text extraction):
  //   [BIOMARKER NAME] [VALUE] [optional L|H]
  //   [date][ref range with units] [lab code]
  // The L/H flag is EXPLICIT in the source — no need to invent heuristic flags.
  const ULTA_LABEL_TO_FIELD = {
    'cholesterol, total': 'cholesterol_total',
    'triglycerides': 'trig',
    'hdl cholesterol': 'hdl',
    'ldl-cholesterol': 'ldl', 'ldl cholesterol': 'ldl',
    'hs crp': 'crp', 'hs-crp': 'crp',
    'glucose': 'glucose_f', 'fasting glucose': 'glucose_f',
    'ast': 'ast', 'alt': 'alt',
    'vitamin b6, plasma': 'b6', 'vitamin b6': 'b6',
    'vitamin b12': 'b12',
    'folate, serum': 'folate_rbc',
    'immunoglobulin g': 'igg',
    'interleukin 6 (il 6), serum': 'il6', 'il-6': 'il6',
    'tnf alpha, highly sensitive': 'tnfa', 'tnf-alpha': 'tnfa',
    'hemoglobin': 'hgb',
    'mcv': 'mcv','mch':'mch','mchc':'mchc',
    'rdw':'rdw','mpv':'mpv','platelet count':'plt',
    'white blood cell count':'wbc','red blood cell count':'rbc',
    'sodium':'na','potassium':'k','chloride':'cl','carbon dioxide':'co2',
    'calcium':'ca','urea nitrogen (bun)':'bun','creatinine':'creat',
    'egfr':'egfr','protein, total':'protein','albumin':'alb',
    'globulin':'glb','bilirubin, total':'tbili','alkaline phosphatase':'alp'
  };

  // Map fields to display labels + units (so we can render any extracted
  // biomarker even if it's not in the curated form list).
  function parseUltaCLIA(text) {
    const biomarkers = [];
    // Match: LABEL VALUE [L|H]\n date REF_RANGE units
    // Greedy LABEL up to value, value is digits[.digits], then optional flag, then newline
    const re = /([A-Z][A-Z0-9, ()/\-]+?)\s+([<>]?\s*\d+\.?\d*)\s*([LH])?\s*\n\s*\d{2}\/\d{2}\/\d{2}\s*([^a-z\n]*?)\s*(mg\/dL|ng\/mL|pg\/mL|μg\/dL|ug\/dL|mcg\/dL|U\/L|mmol\/L|mIU\/L|μIU\/mL|fL|pg|%|g\/dL|Thousand\/uL|Million\/uL|cells\/uL|nmol\/L|μmol\/L|umol\/L)/g;
    let m;
    while ((m = re.exec(text)) !== null) {
      const rawLabel = m[1].trim();
      const valStr = m[2].replace(/\s+/g, '');
      const flag = (m[3] || '').toLowerCase();
      const refRange = (m[4] || '').trim();
      const unit = m[5];
      // Skip commentary lines that accidentally match
      if (rawLabel.length < 3 || rawLabel.length > 50) continue;
      if (/COMMENT|REFERENCE|LEGEND|FASTING:|REPORTED/i.test(rawLabel)) continue;
      const v = parseFloat(valStr.replace(/^[<>]/, ''));
      if (Number.isNaN(v)) continue;
      // Skip implausible values
      if (v < 0 || v > 1e6) continue;
      // Normalize label
      const lcLabel = rawLabel.toLowerCase().replace(/\s+/g, ' ').trim();
      const fieldKey = ULTA_LABEL_TO_FIELD[lcLabel] || null;
      let flagFinal = flag === 'h' ? 'high' : flag === 'l' ? 'low' : 'normal';
      biomarkers.push({
        key: fieldKey || ('ulta_' + lcLabel.replace(/[^a-z0-9]/g, '_').slice(0, 40)),
        label: rawLabel.replace(/\b\w/g, c => c.toUpperCase()),
        value: v,
        unit: unit,
        flag: flagFinal,
        refRange: refRange,
        source: 'Ulta Labs / Quest'
      });
    }
    return { biomarkers };
  }

  // ── DIAGNOSTIC SOLUTIONS METABOLOMICS (OMX Urine) PARSER ───────
  // Each marker block in the text is roughly:
  //   [VALUE] [optional H]
  //   [REFERENCE: "< X" or "X - Y"]
  //   nmol/mg Creatinine
  //   [Marker Name]
  //   [Enzyme + cofactor]
  // Values flagged "H" or beyond reference upper bound are surfaced.
  function parseMetabolomicsOAT(text) {
    const biomarkers = [];
    // Pattern: value [optional H] \n reference \n nmol/mg... \n marker name
    const re = /(?:^|\n)\s*(<DL|\d+\.?\d*)\s*(H|L)?\s*\n\s*([<>]?\s*\d+\.?\d*\s*(?:-\s*\d+\.?\d*)?)\s*\n\s*nmol\/mg Creatinine\s*\n\s*([A-Za-z][A-Za-z0-9\-,'\s]+?)\s*\n/g;
    let m;
    while ((m = re.exec(text)) !== null) {
      const valStr = m[1];
      const flag = (m[2] || '').toUpperCase();
      const refRaw = m[3].trim();
      const marker = m[4].trim();
      if (valStr === '<DL') continue;  // below detection limit — skip
      const v = parseFloat(valStr);
      if (Number.isNaN(v)) continue;
      // Parse ref range
      let refLow = null, refHigh = null;
      const m1 = refRaw.match(/^<\s*(\d+\.?\d*)/);
      const m2 = refRaw.match(/^(\d+\.?\d*)\s*-\s*(\d+\.?\d*)/);
      if (m1) refHigh = parseFloat(m1[1]);
      else if (m2) { refLow = parseFloat(m2[1]); refHigh = parseFloat(m2[2]); }
      let flagFinal = 'normal';
      if (flag === 'H') flagFinal = 'high';
      else if (flag === 'L') flagFinal = 'low';
      else if (refHigh !== null && v > refHigh) flagFinal = 'high';
      else if (refLow !== null && v < refLow) flagFinal = 'low';

      biomarkers.push({
        key: 'oat_' + marker.toLowerCase().replace(/[^a-z0-9]/g, '_').slice(0, 40),
        label: marker,
        value: v,
        unit: 'nmol/mg Cr',
        flag: flagFinal,
        refRange: refRaw,
        source: 'OMX / Organic Acids'
      });
    }
    return { biomarkers };
  }

  // ── TRUHEALTH (epigenetic percentile) parser ───────────────────
  // TruDiagnostic PDFs often use font-subset encoding that breaks
  // simple text extraction. We detect the format and surface a
  // warning + a manual-entry path rather than fabricate readings.
  function parseTruHealth(text) {
    // Try to extract any visible "Name ... XX%" pairs.
    const biomarkers = [];
    const re = /([A-Z][A-Za-z0-9 +\(\)\-]{2,30})\s+(\d{1,3})\s*%/g;
    let m;
    while ((m = re.exec(text)) !== null) {
      const label = m[1].trim();
      const pct = parseInt(m[2], 10);
      if (pct < 0 || pct > 100) continue;
      if (label.length < 3 || /page|http|reference|score|range/i.test(label)) continue;
      const flag = pct < 20 ? 'low' : pct > 80 ? 'high' : 'normal';
      biomarkers.push({
        key: 'tru_' + label.toLowerCase().replace(/[^a-z0-9]/g, '_').slice(0, 40),
        label: label,
        value: pct,
        unit: 'percentile',
        flag: flag,
        refRange: '20-80 normal',
        source: 'TruHealth epigenetic'
      });
    }
    return { biomarkers };
  }

  // ── GENERIC FALLBACK with physiological-plausibility gates ─────
  // For PDFs we don't recognize. The killer fix: REJECT any extracted
  // value outside 0.1× refLow to 5× refHigh as a probable extraction
  // error rather than an extreme reading. Atlas previously fabricated
  // "Copper 2000 μg/dL" from a misplaced odds ratio — never again.
  function parseGenericBloodwork(text) {
    const biomarkers = [];
    for (const f of BIOMARKER_FIELDS) {
      const aliases = (f.a || []).concat([f.l]);
      let matched = null;
      for (const alias of aliases) {
        const esc = alias.replace(/[\s\-\/\(\)\.]/g, '\\s*');
        // Require value to be CLOSE to the label (≤40 chars), AND require
        // the surrounding context to NOT be an odds-ratio pattern.
        const re = new RegExp(esc + '[^\\d\\-\\.]{0,40}?(\\d+\\.?\\d*)', 'i');
        const m = text.match(re);
        if (m) { matched = parseFloat(m[1]); break; }
      }
      if (matched == null || Number.isNaN(matched)) continue;
      // PHYSIOLOGICAL-PLAUSIBILITY GATE — reject extreme outliers.
      const minPlaus = f.rL * 0.1;
      const maxPlaus = f.rH * 5;
      if (matched < minPlaus || matched > maxPlaus) continue;
      let flag = 'normal';
      if (matched < f.rL) flag = 'low';
      else if (matched > f.rH) flag = 'high';
      biomarkers.push({
        key: f.k, label: f.l, value: matched, unit: f.u,
        flag, refRange: f.rL + '-' + f.rH, source: 'generic'
      });
    }
    return { biomarkers };
  }

  // ── MAIN EXTRACTION DISPATCHER ─────────────────────────────────
  // Returns: { docType, biomarkers, matchedGenes, matchedVariants, geneCount, bioCount }
  function extractFromText(text) {
    const docType = detectDocType(text);
    let result = {
      docType,
      biomarkers: [],
      matchedGenes: [],
      matchedVariants: [],
      geneCount: 0,
      bioCount: 0
    };

    if (docType === 'intellxx') {
      const { matchedGenes, matchedVariants } = parseIntellxxDNA(text);
      result.matchedGenes = matchedGenes;
      result.matchedVariants = matchedVariants;
      // Do NOT run biomarker extraction on a pure-genomics PDF
    } else if (docType === 'ulta' || docType === 'quest_or_labcorp') {
      const { biomarkers } = parseUltaCLIA(text);
      result.biomarkers = biomarkers;
    } else if (docType === 'metabolomics') {
      const { biomarkers } = parseMetabolomicsOAT(text);
      result.biomarkers = biomarkers;
    } else if (docType === 'truhealth') {
      const { biomarkers } = parseTruHealth(text);
      result.biomarkers = biomarkers;
      // If empty (font issue), caller surfaces a manual-entry hint
    } else {
      // Generic / unknown — try both biomarker and gene extraction with gates
      const { biomarkers } = parseGenericBloodwork(text);
      result.biomarkers = biomarkers;
      // Generic gene detection — strict uppercase whole-word + atlas-set check
      const seen = new Set();
      const reGene = /\b([A-Z][A-Z0-9]{1,8}(?:-[A-Z0-9]{1,4})?)\b/g;
      let g;
      while ((g = reGene.exec(text)) !== null) {
        const sym = g[1];
        if (ATLAS_GENE_SYMBOLS.has(sym)) seen.add(geneByLabel[sym]);
      }
      result.matchedGenes = Array.from(seen);
    }

    // Sync extracted biomarkers into the form so they're savable
    // and also auto-saveable from the caller. Apply form values for
    // any field that maps to a known BIOMARKER_FIELDS key.
    for (const b of result.biomarkers) {
      const input = bwForm.querySelector('input[data-k="' + b.key + '"]');
      if (input && !input.value && b.value != null) {
        input.value = b.value;
        if (b.flag === 'high') input.classList.add('high');
        else if (b.flag === 'low') input.classList.add('low');
      }
    }

    result.bioCount = result.biomarkers.length;
    result.geneCount = result.matchedGenes.length;
    return result;
  }

  pdfExtract.addEventListener('click', () => {
    const text = pdfPaste.value;
    if (!text || text.length < 50) {
      pdfStatus.classList.add('on'); pdfStatus.classList.add('err');
      pdfStatus.textContent = 'paste some lab text first';
      return;
    }
    const result = extractFromText(text);
    // Merge matched genes + variants into genetics store
    if (result.geneCount > 0 || result.matchedVariants.length > 0) {
      const existing = JSON.parse(localStorage.getItem('cwa_genetics_v1') || 'null') || {
        format: 'pasted text', uploadedAt: Date.now(),
        variantCount: 0, matchedGenes: [], matchedVariants: []
      };
      const gset = new Set(existing.matchedGenes);
      for (const gid of result.matchedGenes) gset.add(gid);
      existing.matchedGenes = Array.from(gset);
      const vSeen = new Set((existing.matchedVariants || []).map(v =>
        v.gene + '|' + v.genotype + '|' + (v.oddsRatio || '')));
      const merged = (existing.matchedVariants || []).slice();
      for (const v of result.matchedVariants) {
        const sig = v.gene + '|' + v.genotype + '|' + (v.oddsRatio || '');
        if (vSeen.has(sig)) continue;
        vSeen.add(sig); merged.push(v);
      }
      merged.sort((a, b) => (b.severity || 0) - (a.severity || 0)
                          || (b.oddsRatio || 0) - (a.oddsRatio || 0));
      existing.matchedVariants = merged;
      existing.uploadedAt = Date.now();
      saveGenetics(existing);
    }
    // Auto-save extracted biomarkers directly from result.biomarkers
    if (result.bioCount > 0) {
      const out = JSON.parse(localStorage.getItem('cwa_biomarkers_v1') || '{}');
      for (const b of result.biomarkers) {
        out[b.key] = {
          value: b.value, unit: b.unit, flag: b.flag, label: b.label,
          refRange: b.refRange, source: b.source,
          nodeId: findBiomarkerNodeIdByLabel(b.label)
        };
      }
      saveBiomarkers(out);
    }
    pdfStatus.classList.add('on'); pdfStatus.classList.remove('err');
    pdfStatus.textContent = 'extracted ' + result.bioCount + ' biomarkers · ' +
      result.geneCount + ' genes · ' + result.matchedVariants.length + ' variants · generating your report…';
    if (result.bioCount > 0 || result.geneCount > 0 || result.matchedVariants.length > 0) {
      setTimeout(() => window.__showReportAfterSave && window.__showReportAfterSave(), 1100);
    }
  });

  // ── MOBILE START-DOCK TOGGLE ──────────────────────────────────
  const mobileDockBtn = document.getElementById('mobile-dock-btn');
  const startDock     = document.getElementById('sd');
  if (mobileDockBtn && startDock) {
    mobileDockBtn.addEventListener('click', () => {
      startDock.classList.toggle('mobile-on');
      mobileDockBtn.classList.toggle('on');
      mobileDockBtn.textContent =
        startDock.classList.contains('mobile-on') ? 'close' : 'starter tests';
    });
  }

  // ── TOUCH HANDLERS FOR CANVAS (pan + pinch zoom) ──────────────
  let tStart = null;
  let lastTDist = null;
  canvas.addEventListener('touchstart', e => {
    if (e.touches.length === 1) {
      tStart = {
        x: e.touches[0].clientX, y: e.touches[0].clientY,
        ox: targetOx, oy: targetOy
      };
    } else if (e.touches.length === 2) {
      const dx = e.touches[0].clientX - e.touches[1].clientX;
      const dy = e.touches[0].clientY - e.touches[1].clientY;
      lastTDist = Math.hypot(dx, dy);
    }
    lastUserAction = performance.now();
  }, { passive: true });
  canvas.addEventListener('touchmove', e => {
    if (e.touches.length === 1 && tStart) {
      targetOx = tStart.ox + (e.touches[0].clientX - tStart.x);
      targetOy = tStart.oy + (e.touches[0].clientY - tStart.y);
    } else if (e.touches.length === 2) {
      const dx = e.touches[0].clientX - e.touches[1].clientX;
      const dy = e.touches[0].clientY - e.touches[1].clientY;
      const dist = Math.hypot(dx, dy);
      if (lastTDist) {
        const k = dist / lastTDist;
        targetScale = Math.max(0.3, Math.min(4, targetScale * k));
      }
      lastTDist = dist;
    }
  }, { passive: true });
  canvas.addEventListener('touchend', () => {
    tStart = null; lastTDist = null;
  });

  // initialize
  updateBanner();
  applyUserData();
})();
</script>

<script>
// Welcome state + map caption — runs after main IIFE; preserved by build script.
(function () {
  'use strict';

  const welcomeEl = document.getElementById('welcome');
  const beginBtn  = document.getElementById('welcome-begin');
  const skipBtn   = document.getElementById('welcome-skip');

  function lsGet(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function lsSet(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }

  const HAS_GEN  = !!lsGet('cwa_genetics_v1');
  const HAS_BIO  = !!lsGet('cwa_biomarkers_v1');
  const HAS_DISM = !!lsGet('cwa_welcome_dismissed_v1');
  const isFirstVisit = !HAS_GEN && !HAS_BIO && !HAS_DISM;

  function startMapCaption(delay) {
    const cap = document.getElementById('map-caption');
    if (!cap) return;
    setTimeout(() => cap.classList.add('ready'), delay || 200);

    let dimmed = false;
    function dim() {
      if (dimmed) return;
      dimmed = true;
      cap.classList.add('dim');
      setTimeout(() => cap.classList.add('hidden'), 3000);
    }
    ['click', 'wheel', 'touchstart', 'keydown'].forEach(ev =>
      window.addEventListener(ev, dim, { once: true, passive: true })
    );
    setTimeout(dim, 12000);
  }

  function dismissWelcome(setDismissedFlag) {
    if (!welcomeEl) return;
    welcomeEl.classList.add('fading');
    welcomeEl.classList.remove('on');
    document.body.classList.remove('welcome-active');
    if (setDismissedFlag) lsSet('cwa_welcome_dismissed_v1', '1');
    setTimeout(() => { welcomeEl.style.display = 'none'; }, 700);
    startMapCaption(200);
  }

  if (isFirstVisit && welcomeEl) {
    document.body.classList.add('welcome-active');

    if (beginBtn) {
      beginBtn.addEventListener('click', () => {
        dismissWelcome(true);
        setTimeout(() => {
          const ub = document.getElementById('upload-btn');
          if (ub && typeof ub.click === 'function') ub.click();
        }, 900);
      });
    }

    if (skipBtn) {
      skipBtn.addEventListener('click', () => dismissWelcome(true));
    }

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && welcomeEl.classList.contains('on')) {
        dismissWelcome(true);
      }
    });
  } else if (welcomeEl) {
    welcomeEl.classList.remove('on');
    welcomeEl.style.display = 'none';
    startMapCaption(200);
  } else {
    startMapCaption(200);
  }
})();
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

# Build the STARTERS payload — curated lists + autism-type labels
starters_payload = {
    "must_have": MUST_HAVE_TEST_IDS,
    "epigenetic": EPIGENETIC_TEST_IDS,
    "high_end":  HIGH_END_TEST_IDS,
    "budget":    BUDGET_TEST_IDS,
    "foundation": UNIVERSAL_FOUNDATION_INT_IDS,
    "types": [{"id": pid, "label": label}
              for pid, label in AUTISM_TYPE_LABELS.items()],
    "resources": FM_RESOURCES,
}

# ── VAULT PATH LOOKUP ──────────────────────────────────────────────
# Scan the vault directory and map atlas_id → canonical filename (stem).
# Used at runtime in the Obsidian profile exporter to produce wikilinks
# that resolve when the user drops the exported .md into their vault.
import re as _re_vault
vault_paths: dict = {}
vault_dir = _REPO / "vault"
if vault_dir.exists():
    for subdir in ("phenotypes", "interventions", "biomarkers",
                   "mechanisms", "hypotheses", "combinations",
                   "genes", "peptides", "tests", "researchers", "topics"):
        d = vault_dir / subdir
        if not d.exists(): continue
        for f in d.iterdir():
            if not f.suffix == ".md": continue
            stem = f.stem
            # IDs at start of filename
            m = _re_vault.match(r"^([A-Z]+-\d+)\b", stem)
            if m:
                vault_paths[m.group(1)] = stem
            # Gene-symbol named pages (currently sparse but auto-picks-up
            # any future gene .md files added to vault/genes/)
            elif subdir == "genes":
                vault_paths["GENE:" + stem.upper()] = stem
            # (Researcher / topic / peptide pages are not currently linked
            # from the patient profile export; add a wlDoc helper if/when needed.)

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
                 json.dumps(intake_feed_for_js, separators=(",", ":")))
        .replace("__STARTERS__",
                 json.dumps(starters_payload, separators=(",", ":")))
        .replace("__VAULT_PATHS__",
                 json.dumps(vault_paths, separators=(",", ":"))))

OUT.write_text(html)
print(f"wrote {OUT} ({OUT.stat().st_size//1024} KB)")
