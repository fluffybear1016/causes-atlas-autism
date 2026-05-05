#!/usr/bin/env python3
"""
run_expansion_v14.py — Causes Atlas (Autism) v1.4 microbiome layer

Reads:  expanded_output_v13/*.csv
Writes: expanded_output_v14/*.csv

v1.4 mission: deepen the microbiome / gut-brain axis layer of the atlas.
Currently HYP-0007 (gut microbiome dysbiosis) and MEC-0008 (gut-brain
axis disruption) are the only microbiome-specific nodes. Real microbiome
science distinguishes specific taxa (Bifidobacterium, Clostridia,
Bacteroides, Akkermansia, Faecalibacterium, Lactobacillus), specific
metabolites (SCFAs, p-cresol, 4-EPS, LPS), specific mechanisms (vagal
afferents, immune signaling, BBB permeability, neurotransmitter
synthesis, HPA axis), and specific interventions (FMT, strain-specific
probiotics, prebiotics, postbiotics, antimicrobial pre-FMT, S. boulardii).

Adds:
  6 new microbial mechanisms
  6 new microbiome-specific hypotheses (taxa-specific dysbioses,
                                          leaky gut, microbial metabolite)
  10 new interventions (FMT, strain-specific probiotics, prebiotics,
                         postbiotics, antimicrobials)
  9 new landmark sources (Hsiao 2013, Kang 2017+2019, Sharon 2019,
                            Hazan 2024, p-cresol mechanism, meta-analyses)
  Cross-pollination edges connecting microbiome layer to existing
  hypotheses (HYP-0007 microbiome, HYP-0022 antibiotics, HYP-0004 PFAS,
  HYP-0005 glyphosate, etc.) and to phenotypes (PHE-0004 GI/microbiome,
  PHE-0001 CFD, PHE-0003 regressive, etc.)

Per spec v1.1 §1.1: contested claims included with proper provenance.
Per spec §1.2: evidence-driven, not factorial.
Per spec §7.3: no hand-edited live scores.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

INPUT_DIR = Path("expanded_output_v13")
OUTPUT_DIR = Path("expanded_output_v14")


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")


def pad_id(prefix: str, n: int, width: int) -> str:
    return f"{prefix}-{str(n).zfill(width)}"


# ---------------------------------------------------------------------------
# v1.4 content
# ---------------------------------------------------------------------------

NEW_MECHANISMS = [
    # name, category, kegg_ids, reactome_ids, opentargets_ids, notes
    ("Short-chain fatty acid (SCFA) signaling",
     "microbial", "hsa00640", "R-HSA-1430728", "",
     "Butyrate, acetate, propionate produced by Faecalibacterium, "
     "Roseburia, Eubacterium. Modulate microglial maturation, BBB "
     "integrity, T-reg differentiation. Both protective (low dose) "
     "and toxic (high propionate animal models)."),
    ("Lipopolysaccharide (LPS) endotoxemia / leaky gut",
     "immune_inflammatory", "hsa04621", "R-HSA-446203", "",
     "Increased intestinal permeability allows LPS translocation; "
     "TLR4 activation drives systemic + neuroinflammation. Reported "
     "elevated in autism cohorts."),
    ("Tryptophan-kynurenine metabolism",
     "metabolic", "hsa00380", "R-HSA-71240", "",
     "Microbial diversion of tryptophan to kynurenine pathway "
     "(reducing serotonin synthesis) and to indoles (AhR signaling). "
     "Altered ratios reported in autism."),
    ("p-cresol / 4-EPS aromatic metabolite production",
     "microbial", "hsa00360", "", "",
     "Clostridia produce p-cresol from tyrosine; reaches brain, "
     "inhibits dopamine-β-hydroxylase. 4-EPS produced by Bacteroides "
     "fragilis-deficient gut induces autism-like behavior in mice "
     "(Hsiao 2013)."),
    ("Bile acid metabolism / FXR signaling",
     "metabolic", "hsa00120", "R-HSA-159418", "",
     "Microbial deconjugation and 7α-dehydroxylation of primary bile "
     "acids; secondary bile acids signal via FXR/TGR5 to regulate "
     "metabolism, inflammation, neuronal function."),
    ("Microbial GABA / neurotransmitter synthesis",
     "microbial", "hsa00410", "", "",
     "Specific Lactobacillus and Bifidobacterium strains produce GABA, "
     "serotonin precursors, dopamine. Bifidobacterium-deficient autism "
     "cohorts may have reduced microbial GABA contribution."),
]


NEW_HYPOTHESES = [
    # name, category, description, affected_population, notes
    ("Bifidobacterium depletion (autism-specific)",
     "microbial",
     "Multi-meta-analyses show consistent reduction in Bifidobacterium "
     "abundance (esp. B. longum, B. breve, B. infantis) in autism vs. "
     "neurotypical children. Bifidobacteria produce GABA, modulate "
     "immune tone, protect epithelial integrity. Hazan 2024 case "
     "documents Bifidobacterium 0% → 1.56% post-FMT with verbal "
     "emergence.",
     "Population-wide signal in autism cohorts",
     "Iglesias-Vázquez 2020 meta-analysis n=1972."),

    ("Clostridia overgrowth / dysbiotic fermentation",
     "microbial",
     "Elevated Clostridium species (esp. C. histolyticum group, "
     "C. perfringens) reported in autism cohorts. Clostridia produce "
     "p-cresol, 4-ethylphenyl sulfate, propionate at high levels — "
     "all linked to autism-like behavior in animal models.",
     "Subset, especially with GI symptoms",
     "Finegold 2002, 2010; consume-GABA hypothesis."),

    ("Akkermansia / Faecalibacterium depletion",
     "microbial",
     "Reduced Akkermansia muciniphila and Faecalibacterium prausnitzii "
     "(major butyrate producers) reported in autism cohorts. Both "
     "protect mucin layer and produce SCFAs.",
     "Subset; mucin barrier compromise",
     "Pulikkan 2018; Liu 2022."),

    ("Intestinal barrier permeability ('leaky gut')",
     "immune",
     "Elevated zonulin, lactulose-mannitol ratio, and serum LPS "
     "reported in autism. Permits microbial metabolite translocation "
     "and chronic immune activation. Distinct from microbiome "
     "composition itself.",
     "~25-50% of autism cases",
     "de Magistris 2010."),

    ("Microbial p-cresol / 4-EPS metabolite excess",
     "microbial",
     "Elevated urinary and plasma p-cresol and 4-EPS in autism; "
     "mechanism via tyrosine metabolism by Clostridia. Inhibits "
     "catecholamine synthesis (Bermudez-Martin 2021); induces "
     "autism-like behavior in mice (Hsiao 2013).",
     "Subset with elevated metabolites",
     "Strong mouse mechanistic; correlational human."),

    ("Fungal dysbiosis / candida overgrowth",
     "microbial",
     "Elevated Candida (especially C. albicans) reported in autism "
     "GI subset; produces propionic acid, ammonia, biofilms. Anecdotal "
     "antifungal response common in functional/integrative protocols.",
     "Subset; biomarker-defined",
     "Less well peer-reviewed; functional med tradition strong."),
]


NEW_INTERVENTIONS = [
    # name, category, directionality, mechanism_summary, dose,
    # cost, otc_or_rx, pediatric_safe, notes
    ("Fecal microbiota transplantation (FMT)",
     "drug", "treatment",
     "Whole microbiota transfer from healthy donor (often familial). "
     "Kang 2017 open-label MTT showed sustained 45% reduction in "
     "ASD symptoms 2 years post; Hazan 2024 familial sibling FMT "
     "case report showed nonverbal → verbal emergence with "
     "Bifidobacterium restoration.",
     "Single 300 mL infusion or multi-dose over 8 weeks", 5000,
     "rx", "uncertain",
     "Kang 2017+2019 sustained outcomes; Hazan 2024."),

    ("Bifidobacterium infantis / longum probiotic",
     "supplement", "treatment",
     "Strain-specific probiotic targeting documented Bifidobacterium "
     "depletion in autism. B. infantis 35624 (Align) and B. longum "
     "BB536 most-studied.",
     "10-20 billion CFU/day", 35, "otc", "yes",
     "More targeted than multi-strain INT-0025."),

    ("Lactobacillus rhamnosus GG",
     "supplement", "treatment",
     "Most-studied probiotic strain; produces GABA, modulates immune "
     "tone, reduces intestinal permeability. Some autism RCTs positive.",
     "10 billion CFU/day", 25, "otc", "yes",
     "Parracho 2010, Santocchi 2020."),

    ("Saccharomyces boulardii (yeast probiotic)",
     "supplement", "treatment",
     "Non-colonizing yeast probiotic; antagonist to Candida and "
     "C. difficile. Used in functional autism protocols for fungal "
     "dysbiosis.",
     "5-10 billion CFU/day", 20, "otc", "yes",
     "Parker 2018."),

    ("Akkermansia muciniphila (live)",
     "supplement", "treatment",
     "Mucin-degrading commensal that paradoxically thickens the "
     "mucin layer; modulates metabolism and BBB integrity. Pasteurized "
     "form FDA novel-food approved.",
     "10^9 CFU/day", 60, "otc", "uncertain",
     "Newly available; emerging interest."),

    ("Human milk oligosaccharides (HMOs)",
     "supplement", "prevention",
     "2'-fucosyllactose (2'-FL) and lacto-N-neotetraose (LNnT); "
     "Bifidobacterium-specific prebiotic. Selectively expand "
     "Bifidobacteria; restore infant-like gut.",
     "1-3 g/day", 35, "otc", "yes",
     "Infant formula fortification widespread."),

    ("Galactooligosaccharides (GOS) / fructooligosaccharides (FOS)",
     "supplement", "treatment",
     "Prebiotic fibers that selectively feed Bifidobacterium and "
     "Faecalibacterium; raise SCFA production.",
     "5-10 g/day", 15, "otc", "yes",
     "Grimaldi 2018 RCT positive in ASD."),

    ("Sodium butyrate (postbiotic)",
     "supplement", "treatment",
     "Direct delivery of butyrate; bypasses fermentation. HDAC "
     "inhibitor, T-reg promoter, BBB protector. Autism animal "
     "models positive.",
     "150-450 mg/day", 25, "otc", "uncertain",
     "Animal models stronger than human RCT base."),

    ("Vancomycin (oral, transient pre-FMT)",
     "drug", "cause_mitigation",
     "Non-absorbed antibiotic used short-term to clear pathogenic "
     "Clostridia before FMT or microbiome reset. NOT systemic "
     "antibiotic — gut-only.",
     "125-500 mg 4x/day, 10-14 days", 200, "rx", "uncertain",
     "Sandler 2000 (transient improvement); Hazan 2024 pre-FMT."),

    ("Antifungal protocol (nystatin / fluconazole, targeted)",
     "drug", "treatment",
     "Targeted antifungal therapy for documented Candida overgrowth "
     "in autism subset. Empirically used in functional medicine; "
     "controversial mainstream.",
     "Per pediatric dosing", 80, "rx", "uncertain",
     "Less peer-reviewed; functional med tradition."),
]


# Landmark sources with target_links per source
NEW_LANDMARKS = [
    # (pmid, title, year, design, sample_size, type, author, targets)
    ("24315484", "Microbiota modulate behavioral and physiological "
     "abnormalities associated with neurodevelopmental disorders",
     2013, "mechanistic", 0, "study", "Hsiao",
     [("hypothesis", "Microbial p-cresol / 4-EPS metabolite excess",
       "positive"),
      ("hypothesis", "Intestinal barrier permeability ('leaky gut')",
       "positive"),
      ("mechanism", "p-cresol / 4-EPS aromatic metabolite production",
       "positive"),
      ("mechanism",
       "Lipopolysaccharide (LPS) endotoxemia / leaky gut",
       "positive")]),

    ("28122648", "Microbiota Transfer Therapy alters gut ecosystem "
     "and improves gastrointestinal and autism symptoms: an "
     "open-label study", 2017, "case_series", 18, "study", "Kang",
     [("intervention", "Fecal microbiota transplantation (FMT)",
       "positive"),
      ("hypothesis", "Bifidobacterium depletion (autism-specific)",
       "positive"),
      ("hypothesis",
       "Gut microbiome dysbiosis / dysbiotic fermentation",
       "positive"),
      ("phenotype", "PHE-0004", "positive")]),

    ("30971960", "Long-term benefit of Microbiota Transfer Therapy "
     "on autism symptoms and gut microbiota", 2019, "case_series",
     18, "study", "Kang",
     [("intervention", "Fecal microbiota transplantation (FMT)",
       "positive"),
      ("hypothesis",
       "Gut microbiome dysbiosis / dysbiotic fermentation",
       "positive")]),

    ("38715916", "Improvements in Gut Microbiome Composition and "
     "Clinical Symptoms Following Familial Fecal Microbiota "
     "Transplantation in a Nineteen-Year-Old Adolescent With Severe "
     "Autism", 2024, "case_series", 1, "study", "Hazan",
     [("intervention", "Fecal microbiota transplantation (FMT)",
       "positive"),
      ("intervention",
       "Bifidobacterium infantis / longum probiotic", "positive"),
      ("intervention",
       "Vancomycin (oral, transient pre-FMT)", "positive"),
      ("hypothesis", "Bifidobacterium depletion (autism-specific)",
       "positive"),
      ("phenotype", "PHE-0004", "positive")]),

    ("31182656", "Human gut microbiota from autism spectrum disorder "
     "promote behavioral symptoms in mice", 2019, "mechanistic", 0,
     "study", "Sharon",
     [("hypothesis",
       "Gut microbiome dysbiosis / dysbiotic fermentation",
       "positive"),
      ("mechanism",
       "Microbial GABA / neurotransmitter synthesis", "positive")]),

    ("34238386", "The microbial metabolite p-Cresol induces "
     "autistic-like behaviors in mice by remodeling the gut "
     "microbiota", 2021, "mechanistic", 0, "study", "Bermudez-Martin",
     [("hypothesis", "Microbial p-cresol / 4-EPS metabolite excess",
       "positive"),
      ("mechanism", "p-cresol / 4-EPS aromatic metabolite production",
       "positive"),
      ("hypothesis", "Clostridia overgrowth / dysbiotic fermentation",
       "positive")]),

    ("33087514", "Distinct Fecal and Plasma Metabolites in Children "
     "with Autism Spectrum Disorders and Their Modulation after "
     "Microbiota Transfer Therapy", 2020, "case_control", 18,
     "study", "Kang",
     [("intervention", "Fecal microbiota transplantation (FMT)",
       "positive"),
      ("mechanism", "Tryptophan-kynurenine metabolism", "positive"),
      ("hypothesis", "Microbial p-cresol / 4-EPS metabolite excess",
       "positive")]),

    ("36195961", "Multi-angle meta-analysis of the gut microbiome "
     "in Autism Spectrum Disorder", 2022, "meta_analysis", 1972,
     "review", "Andreo-Martinez",
     [("hypothesis", "Bifidobacterium depletion (autism-specific)",
       "positive"),
      ("hypothesis", "Akkermansia / Faecalibacterium depletion",
       "positive"),
      ("hypothesis",
       "Gut microbiome dysbiosis / dysbiotic fermentation",
       "positive")]),

    ("19833000", "Gastrointestinal microflora studies in late-onset "
     "autism", 2002, "case_control", 35, "study", "Finegold",
     [("hypothesis", "Clostridia overgrowth / dysbiotic fermentation",
       "positive")]),

    ("20542896", "Alterations of the intestinal barrier in patients "
     "with autism spectrum disorders and in their first-degree "
     "relatives", 2010, "case_control", 90, "study", "de-Magistris",
     [("hypothesis", "Intestinal barrier permeability ('leaky gut')",
       "positive"),
      ("mechanism",
       "Lipopolysaccharide (LPS) endotoxemia / leaky gut",
       "positive")]),

    ("29456502", "Gut microbial dysbiosis is associated with autism "
     "spectrum disorder phenotype severity", 2018, "case_control",
     30, "study", "Pulikkan",
     [("hypothesis", "Akkermansia / Faecalibacterium depletion",
       "positive")]),

    ("30030781", "Prebiotic intervention with B-GOS in children "
     "with autism spectrum disorders", 2018, "rct", 30, "study",
     "Grimaldi",
     [("intervention",
       "Galactooligosaccharides (GOS) / fructooligosaccharides (FOS)",
       "positive"),
      ("hypothesis", "Bifidobacterium depletion (autism-specific)",
       "positive")]),

    ("32219074", "Gut to brain dysbiosis: mechanisms linking western "
     "diet consumption, the microbiome, and cognitive impairment",
     2020, "review", 0, "review", "Noble",
     [("hypothesis",
       "Ultra-processed food / Western diet pattern", "positive"),
      ("mechanism", "Short-chain fatty acid (SCFA) signaling",
       "positive"),
      ("mechanism",
       "Lipopolysaccharide (LPS) endotoxemia / leaky gut",
       "positive")]),

    ("10888984", "Short-term benefit from oral vancomycin treatment "
     "of regressive-onset autism", 2000, "rct", 11, "study",
     "Sandler",
     [("intervention", "Vancomycin (oral, transient pre-FMT)",
       "positive"),
      ("hypothesis", "Clostridia overgrowth / dysbiotic fermentation",
       "positive")]),

    ("32414977", "Two-randomized controlled trials of probiotic "
     "supplementation in children with autism spectrum disorder",
     2020, "rct", 85, "study", "Santocchi",
     [("intervention", "Lactobacillus rhamnosus GG", "positive"),
      ("intervention", "Probiotics (multi-strain)", "positive"),
      ("hypothesis",
       "Gut microbiome dysbiosis / dysbiotic fermentation",
       "positive")]),
]


# Edge specifications connecting microbiome layer
NEW_HYP_MECH_LINKS = [
    ("Bifidobacterium depletion (autism-specific)",
     "Microbial GABA / neurotransmitter synthesis"),
    ("Bifidobacterium depletion (autism-specific)",
     "Short-chain fatty acid (SCFA) signaling"),
    ("Clostridia overgrowth / dysbiotic fermentation",
     "p-cresol / 4-EPS aromatic metabolite production"),
    ("Clostridia overgrowth / dysbiotic fermentation",
     "Tryptophan-kynurenine metabolism"),
    ("Akkermansia / Faecalibacterium depletion",
     "Short-chain fatty acid (SCFA) signaling"),
    ("Akkermansia / Faecalibacterium depletion",
     "Lipopolysaccharide (LPS) endotoxemia / leaky gut"),
    ("Intestinal barrier permeability ('leaky gut')",
     "Lipopolysaccharide (LPS) endotoxemia / leaky gut"),
    ("Intestinal barrier permeability ('leaky gut')",
     "Neuroinflammation"),
    ("Microbial p-cresol / 4-EPS metabolite excess",
     "p-cresol / 4-EPS aromatic metabolite production"),
    ("Microbial p-cresol / 4-EPS metabolite excess",
     "GABA/glutamate imbalance"),
    ("Fungal dysbiosis / candida overgrowth",
     "Lipopolysaccharide (LPS) endotoxemia / leaky gut"),
    # Existing hypotheses to new mechanisms
    ("Gut microbiome dysbiosis / dysbiotic fermentation",
     "Short-chain fatty acid (SCFA) signaling"),
    ("Gut microbiome dysbiosis / dysbiotic fermentation",
     "Tryptophan-kynurenine metabolism"),
    ("Gut microbiome dysbiosis / dysbiotic fermentation",
     "Bile acid metabolism / FXR signaling"),
    ("Gut microbiome dysbiosis / dysbiotic fermentation",
     "Microbial GABA / neurotransmitter synthesis"),
    ("Early-life antibiotics (especially first year)",
     "Microbial GABA / neurotransmitter synthesis"),
    ("Early-life antibiotics (especially first year)",
     "Short-chain fatty acid (SCFA) signaling"),
    ("Cesarean section delivery",
     "Microbial GABA / neurotransmitter synthesis"),
    ("Glyphosate exposure (food + water)",
     "Tryptophan-kynurenine metabolism"),
]

NEW_MECH_PHEN_LINKS = [
    # microbial mechanisms → GI/microbiome phenotype (PHE-0004) and others
    ("Short-chain fatty acid (SCFA) signaling", "PHE-0004"),
    ("Lipopolysaccharide (LPS) endotoxemia / leaky gut", "PHE-0004"),
    ("Lipopolysaccharide (LPS) endotoxemia / leaky gut", "PHE-0003"),
    ("Tryptophan-kynurenine metabolism", "PHE-0004"),
    ("p-cresol / 4-EPS aromatic metabolite production", "PHE-0004"),
    ("Bile acid metabolism / FXR signaling", "PHE-0004"),
    ("Microbial GABA / neurotransmitter synthesis", "PHE-0004"),
    ("Microbial GABA / neurotransmitter synthesis", "PHE-0007"),
]

NEW_INT_HYP_LINKS = [
    # cause_mitigation: intervention targets specific microbiome hypothesis
    ("Fecal microbiota transplantation (FMT)",
     "Bifidobacterium depletion (autism-specific)"),
    ("Fecal microbiota transplantation (FMT)",
     "Clostridia overgrowth / dysbiotic fermentation"),
    ("Fecal microbiota transplantation (FMT)",
     "Akkermansia / Faecalibacterium depletion"),
    ("Fecal microbiota transplantation (FMT)",
     "Intestinal barrier permeability ('leaky gut')"),
    ("Fecal microbiota transplantation (FMT)",
     "Gut microbiome dysbiosis / dysbiotic fermentation"),
    ("Bifidobacterium infantis / longum probiotic",
     "Bifidobacterium depletion (autism-specific)"),
    ("Lactobacillus rhamnosus GG",
     "Intestinal barrier permeability ('leaky gut')"),
    ("Lactobacillus rhamnosus GG",
     "Gut microbiome dysbiosis / dysbiotic fermentation"),
    ("Saccharomyces boulardii (yeast probiotic)",
     "Fungal dysbiosis / candida overgrowth"),
    ("Akkermansia muciniphila (live)",
     "Akkermansia / Faecalibacterium depletion"),
    ("Akkermansia muciniphila (live)",
     "Intestinal barrier permeability ('leaky gut')"),
    ("Human milk oligosaccharides (HMOs)",
     "Bifidobacterium depletion (autism-specific)"),
    ("Galactooligosaccharides (GOS) / fructooligosaccharides (FOS)",
     "Bifidobacterium depletion (autism-specific)"),
    ("Galactooligosaccharides (GOS) / fructooligosaccharides (FOS)",
     "Akkermansia / Faecalibacterium depletion"),
    ("Sodium butyrate (postbiotic)",
     "Intestinal barrier permeability ('leaky gut')"),
    ("Vancomycin (oral, transient pre-FMT)",
     "Clostridia overgrowth / dysbiotic fermentation"),
    ("Antifungal protocol (nystatin / fluconazole, targeted)",
     "Fungal dysbiosis / candida overgrowth"),
    # Existing interventions to new microbiome hypotheses
    ("Probiotics (multi-strain)",
     "Bifidobacterium depletion (autism-specific)"),
    ("Probiotics (multi-strain)",
     "Akkermansia / Faecalibacterium depletion"),
]

NEW_INT_MECH_LINKS = [
    ("Fecal microbiota transplantation (FMT)",
     "Microbial GABA / neurotransmitter synthesis"),
    ("Fecal microbiota transplantation (FMT)",
     "Short-chain fatty acid (SCFA) signaling"),
    ("Fecal microbiota transplantation (FMT)",
     "Lipopolysaccharide (LPS) endotoxemia / leaky gut"),
    ("Bifidobacterium infantis / longum probiotic",
     "Microbial GABA / neurotransmitter synthesis"),
    ("Bifidobacterium infantis / longum probiotic",
     "Short-chain fatty acid (SCFA) signaling"),
    ("Lactobacillus rhamnosus GG",
     "Microbial GABA / neurotransmitter synthesis"),
    ("Saccharomyces boulardii (yeast probiotic)",
     "Lipopolysaccharide (LPS) endotoxemia / leaky gut"),
    ("Akkermansia muciniphila (live)",
     "Lipopolysaccharide (LPS) endotoxemia / leaky gut"),
    ("Human milk oligosaccharides (HMOs)",
     "Microbial GABA / neurotransmitter synthesis"),
    ("Galactooligosaccharides (GOS) / fructooligosaccharides (FOS)",
     "Short-chain fatty acid (SCFA) signaling"),
    ("Sodium butyrate (postbiotic)",
     "Short-chain fatty acid (SCFA) signaling"),
    ("Vancomycin (oral, transient pre-FMT)",
     "p-cresol / 4-EPS aromatic metabolite production"),
    ("Antifungal protocol (nystatin / fluconazole, targeted)",
     "Lipopolysaccharide (LPS) endotoxemia / leaky gut"),
]


# ---------------------------------------------------------------------------
# Expansion logic (mirrors run_expansion.py / run_expansion_v13.py)
# ---------------------------------------------------------------------------

def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    ts = now_iso()

    print(f"[v1.4] running at {ts}")
    print(f"[v1.4] reading from {INPUT_DIR}/")
    tables = {}
    for csv in sorted(INPUT_DIR.glob("*.csv")):
        tables[csv.stem] = pd.read_csv(
            csv, dtype=str, keep_default_na=False)

    # Lookup maps
    mech_name_to_id = {r["name"]: r["id"]
                       for _, r in tables["mechanisms"].iterrows()}
    hyp_name_to_id = {r["name"]: r["id"]
                      for _, r in tables["hypotheses"].iterrows()}
    int_name_to_id = {r["name"]: r["id"]
                      for _, r in tables["interventions"].iterrows()}
    gene_symbol_to_id = {r["gene_symbol"]: r["id"]
                         for _, r in tables["genes"].iterrows()}

    def next_n(table_name, prefix):
        df = tables[table_name]
        if df.empty: return 1
        nums = []
        for i in df["id"].dropna():
            m = re.match(rf"^{prefix}-(\d+)$", str(i))
            if m: nums.append(int(m.group(1)))
        return (max(nums) if nums else 0) + 1

    next_mec = next_n("mechanisms", "MEC")
    next_hyp = next_n("hypotheses", "HYP")
    next_int = next_n("interventions", "INT")
    next_src = next_n("sources", "SRC")
    next_evd = next_n("evidence_fragments", "EVD")
    next_evl = next_n("evidence_links", "EVL")
    next_hme = next_n("hypothesis_mechanism_edges", "HME")
    next_mpe = next_n("mechanism_phenotype_edges", "MPE")
    next_ime = next_n("intervention_mechanism_edges", "IME")
    next_ihe = next_n("intervention_hypothesis_edges", "IHE")

    # ---- mechanisms ----
    new_mec = []
    for name, cat, kegg, react, ot, notes in NEW_MECHANISMS:
        if name in mech_name_to_id: continue
        mid = pad_id("MEC", next_mec, 4); next_mec += 1
        mech_name_to_id[name] = mid
        new_mec.append({
            "id": mid, "name": name, "category": cat,
            "description": "", "status": "active",
            "evidence_strength": "",
            "kegg_ids": kegg, "reactome_ids": react,
            "opentargets_ids": ot,
            "created_at": ts, "last_updated": ts, "notes": notes,
        })
    if new_mec:
        tables["mechanisms"] = pd.concat(
            [tables["mechanisms"], pd.DataFrame(new_mec)],
            ignore_index=True)
        print(f"[v1.4] mechanisms: +{len(new_mec)}")

    # ---- hypotheses ----
    new_hyp = []
    for name, cat, desc, pop, notes in NEW_HYPOTHESES:
        if name in hyp_name_to_id: continue
        hid = pad_id("HYP", next_hyp, 4); next_hyp += 1
        hyp_name_to_id[name] = hid
        new_hyp.append({
            "id": hid, "name": name, "category": cat,
            "description": desc, "affected_population": pop,
            "status": "active",
            "confidence_score": "", "evidence_count": "",
            "evidence_quality_index": "", "consistency_index": "",
            "created_at": ts, "last_updated": ts, "notes": notes,
            "category_legacy": "", "evidence_strength_legacy": "",
            "epidemiological_strength_legacy": "",
            "mitigation_intervention_ids_legacy": "",
            "source_pmids_legacy": "",
            "csrs_score_legacy": "", "csrs_last_updated_legacy": "",
        })
    if new_hyp:
        tables["hypotheses"] = pd.concat(
            [tables["hypotheses"], pd.DataFrame(new_hyp)],
            ignore_index=True)
        print(f"[v1.4] hypotheses: +{len(new_hyp)}")

    # ---- interventions ----
    new_int = []
    for (name, cat, dirn, mech, dose, cost, otc, ped,
         notes) in NEW_INTERVENTIONS:
        if name in int_name_to_id: continue
        iid = pad_id("INT", next_int, 4); next_int += 1
        int_name_to_id[name] = iid
        new_int.append({
            "id": iid, "name": name, "category": cat,
            "directionality": dirn, "mechanism_summary": mech,
            "dose_range": dose, "cost_per_month_usd": str(cost),
            "otc_or_rx": otc, "pediatric_safe": ped,
            "csrs_score": "", "csrs_last_updated": "",
            "status": "active",
            "created_at": ts, "last_updated": ts, "notes": notes,
            "targets_legacy": "", "source_pmids_legacy": "",
            "source_anecdote_ids_legacy": "",
            "csrs_score_legacy": "", "csrs_last_updated_legacy": "",
        })
    if new_int:
        tables["interventions"] = pd.concat(
            [tables["interventions"], pd.DataFrame(new_int)],
            ignore_index=True)
        print(f"[v1.4] interventions: +{len(new_int)}")

    # ---- sources + evidence_fragments + evidence_links ----
    new_src, new_evd, new_evl = [], [], []
    skipped = []
    for (pmid, title, year, design, n, stype, author,
         targets) in NEW_LANDMARKS:
        sid = pad_id("SRC", next_src, 6); next_src += 1
        new_src.append({
            "id": sid, "type": stype, "platform": "pubmed",
            "external_id": pmid, "title": title,
            "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
            "date_published": f"{year}-01-01", "date_ingested": ts,
            "study_design": design,
            "sample_size": str(n) if n else "",
            "model_system": "human" if design != "mechanistic"
                            else "animal",
            "raw_metadata": json.dumps({
                "year": year, "first_author": author,
                "added_in": "v1.4_microbiome_expansion",
            }, sort_keys=True),
            "notes": "",
        })
        eid = pad_id("EVD", next_evd, 6); next_evd += 1
        default_dir = targets[0][2] if targets else "positive"
        new_evd.append({
            "id": eid, "source_id": sid,
            "fragment_type": "result" if design != "mechanistic"
                              else "mechanism",
            "text_excerpt": title[:480],
            "structured_payload": json.dumps({
                "first_author": author, "design": design,
                "sample_size": n, "year": year,
                "added_in": "v1.4_microbiome_expansion",
            }, sort_keys=True),
            "effect_direction": default_dir,
            "strength_score": "",
            "extraction_method": "manual",
            "extraction_confidence": "1.00",
            "date_extracted": ts, "notes": "",
        })
        for ttype, name, direction in targets:
            if ttype == "gene":
                tid = gene_symbol_to_id.get(name)
            elif ttype == "hypothesis":
                tid = hyp_name_to_id.get(name)
            elif ttype == "intervention":
                tid = int_name_to_id.get(name)
            elif ttype == "mechanism":
                tid = mech_name_to_id.get(name)
            elif ttype == "phenotype":
                tid = name  # already PHE-XXXX
            else:
                tid = None
            if not tid:
                skipped.append((pmid, ttype, name)); continue
            elid = pad_id("EVL", next_evl, 6); next_evl += 1
            new_evl.append({
                "id": elid, "evidence_fragment_id": eid,
                "claim_id": "",
                "target_type": ttype, "target_id": tid,
                "effect_direction": direction,
                "weight": "", "context_scope": "",
                "created_at": ts, "notes": "",
            })

    tables["sources"] = pd.concat(
        [tables["sources"], pd.DataFrame(new_src)], ignore_index=True)
    tables["evidence_fragments"] = pd.concat(
        [tables["evidence_fragments"], pd.DataFrame(new_evd)],
        ignore_index=True)
    tables["evidence_links"] = pd.concat(
        [tables["evidence_links"], pd.DataFrame(new_evl)],
        ignore_index=True)
    print(f"[v1.4] sources: +{len(new_src)}, evidence_fragments: "
          f"+{len(new_evd)}, evidence_links: +{len(new_evl)}")
    if skipped:
        print(f"[v1.4] skipped {len(skipped)} unresolvable targets:")
        for pmid, ttype, name in skipped[:10]:
            print(f"  PMID {pmid}: {ttype}={name}")

    # ---- new edges ----
    def add_edges(table_name, prefix, src_col, dst_col, lookups,
                  pairs, relation_type):
        nonlocal tables
        n_start = next_n(table_name, prefix)
        rows = []
        n = n_start
        for src_name, dst_name in pairs:
            sid = lookups[0].get(src_name)
            did = lookups[1].get(dst_name)
            if not sid or not did: continue
            eid = pad_id(prefix, n, 5); n += 1
            rows.append({
                "id": eid, src_col: sid, dst_col: did,
                "relation_type": relation_type,
                "polarity": "supporting",
                "evidence_for_count": "",
                "evidence_against_count": "",
                "evidence_strength_aggregate": "",
                "context_scope": "", "status": "active",
                "created_at": ts, "last_updated": ts,
            })
        if rows:
            tables[table_name] = pd.concat(
                [tables[table_name], pd.DataFrame(rows)],
                ignore_index=True)
        return len(rows)

    # hypothesis_mechanism_edges
    n_hme = add_edges(
        "hypothesis_mechanism_edges", "HME",
        "hypothesis_id", "mechanism_id",
        (hyp_name_to_id, mech_name_to_id),
        NEW_HYP_MECH_LINKS, "acts_through")
    print(f"[v1.4] hypothesis_mechanism_edges: +{n_hme}")

    # mechanism_phenotype_edges (phenotype is PHE-XXXX direct)
    rows = []
    n = next_n("mechanism_phenotype_edges", "MPE")
    for mech_name, phen_id in NEW_MECH_PHEN_LINKS:
        mid = mech_name_to_id.get(mech_name)
        if not mid: continue
        eid = pad_id("MPE", n, 5); n += 1
        rows.append({
            "id": eid, "mechanism_id": mid, "phenotype_id": phen_id,
            "relation_type": "implicated_in", "polarity": "supporting",
            "evidence_for_count": "", "evidence_against_count": "",
            "evidence_strength_aggregate": "",
            "context_scope": "", "status": "active",
            "created_at": ts, "last_updated": ts,
        })
    if rows:
        tables["mechanism_phenotype_edges"] = pd.concat(
            [tables["mechanism_phenotype_edges"], pd.DataFrame(rows)],
            ignore_index=True)
    print(f"[v1.4] mechanism_phenotype_edges: +{len(rows)}")

    # intervention_hypothesis_edges
    n_ihe = add_edges(
        "intervention_hypothesis_edges", "IHE",
        "intervention_id", "hypothesis_id",
        (int_name_to_id, hyp_name_to_id),
        NEW_INT_HYP_LINKS, "cause_mitigation")
    print(f"[v1.4] intervention_hypothesis_edges: +{n_ihe}")

    # intervention_mechanism_edges
    n_ime = add_edges(
        "intervention_mechanism_edges", "IME",
        "intervention_id", "mechanism_id",
        (int_name_to_id, mech_name_to_id),
        NEW_INT_MECH_LINKS, "modulates")
    print(f"[v1.4] intervention_mechanism_edges: +{n_ime}")

    # ---- write ----
    for name, df in tables.items():
        target = OUTPUT_DIR / f"{name}.csv"
        df.to_csv(target, index=False, encoding="utf-8")

    summary = {
        "expansion_version": "v1.4_microbiome",
        "run_timestamp": ts,
        "added": {
            "mechanisms": len(new_mec),
            "hypotheses": len(new_hyp),
            "interventions": len(new_int),
            "sources": len(new_src),
            "evidence_fragments": len(new_evd),
            "evidence_links": len(new_evl),
            "hypothesis_mechanism_edges": n_hme,
            "mechanism_phenotype_edges": len(rows),
            "intervention_mechanism_edges": n_ime,
            "intervention_hypothesis_edges": n_ihe,
        },
        "skipped_targets": len(skipped),
    }
    Path("expansion_v14_summary.json").write_text(
        json.dumps(summary, indent=2))
    print()
    print("=" * 60)
    print("v1.4 MICROBIOME EXPANSION COMPLETE")
    print(json.dumps(summary["added"], indent=2))


if __name__ == "__main__":
    main()
