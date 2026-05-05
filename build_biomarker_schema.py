#!/usr/bin/env python3
"""Session 3.5A — Biomarker entity layer.

Creates:
  v2.0_scored/biomarkers.csv          — atomic biomarker entries
  v2.0_scored/biomarker_mechanism_edges.csv   — BME wiring
  v2.0_scored/biomarker_phenotype_edges.csv   — BPE wiring
  v2.0_scored/biomarker_intervention_edges.csv — BIE wiring
  v2.0_scored/biomarker_hypothesis_edges.csv  — BHE wiring

Same schema duplicated in v2.0.1_expanded/ (atlas convention).

Ingests ~120 biomarkers across 20 categories:
  1. Methylation cycle / one-carbon
  2. Folate-receptor / cerebral folate
  3. Mitochondrial
  4. Oxidative stress
  5. OAT microbial metabolites
  6. OAT neurotransmitter metabolites
  7. Immune / inflammatory cytokines
  8. Mast cell activation
  9. PANS/PANDAS antibody
  10. Heavy metals / toxicants
  11. Environmental chemicals (phthalates/BPA/PFAS/OPs/mycotoxins)
  12. Maternal / parental
  13. Trace minerals
  14. Pyroluria
  15. Fatty acid status
  16. GI / barrier function
  17. Endocrine / hormonal
  18. Chronic infection panel
  19. Autoimmune broader
  20. NEUROBIOLOGY / brain biomarkers (neuroimaging, EEG/ERP, eye-tracking, CSF, blood-brain)

Wires to existing HYP/MEC/INT/PHE entities. Does not change scoring engine
(parallel layer; non-disruptive to existing CSRS calibration).
"""
import csv, datetime as dt, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NOW = dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')

# ============================================================
# SCHEMA: biomarkers.csv
# ============================================================
BIOMARKER_FIELDS = [
    "id", "name", "category", "subcategory", "alternate_names",
    "sample_type", "units", "reference_low", "reference_high",
    "reference_optimal_low", "reference_optimal_high", "age_caveat",
    "what_it_measures", "elevated_means", "low_means",
    "test_availability", "test_cost_usd_low", "test_cost_usd_high",
    "turnaround_days", "clia_status", "lab_options",
    "snp_dependence", "interpretation_summary",
    "mechanisms_indicated", "phenotypes_stratified",
    "interventions_modulates", "hypotheses_tests",
    "key_pmids", "created_at", "last_updated", "notes",
]

# ============================================================
# 120+ BIOMARKERS — comprehensive bioinformatics-grade catalog
# ============================================================
B = []  # accumulator
def add(**kw):
    kw.setdefault("created_at", NOW)
    kw.setdefault("last_updated", NOW)
    kw.setdefault("alternate_names", "")
    kw.setdefault("subcategory", "")
    kw.setdefault("age_caveat", "")
    kw.setdefault("snp_dependence", "")
    kw.setdefault("test_cost_usd_low", "")
    kw.setdefault("test_cost_usd_high", "")
    kw.setdefault("turnaround_days", "")
    kw.setdefault("clia_status", "")
    kw.setdefault("lab_options", "")
    kw.setdefault("mechanisms_indicated", "")
    kw.setdefault("phenotypes_stratified", "")
    kw.setdefault("interventions_modulates", "")
    kw.setdefault("hypotheses_tests", "")
    kw.setdefault("key_pmids", "")
    kw.setdefault("notes", "")
    kw.setdefault("test_availability", "commercial")
    kw.setdefault("interpretation_summary", "")
    kw.setdefault("reference_optimal_low", "")
    kw.setdefault("reference_optimal_high", "")
    B.append(kw)

# Helper for sequential IDs
def bid(n): return f"BIO-{n:04d}"

i = 1
def nxt():
    global i
    out = bid(i); i += 1; return out

# ────────────────────────────────────────────────────────────
# CATEGORY 1: METHYLATION CYCLE / ONE-CARBON
# ────────────────────────────────────────────────────────────
add(id=nxt(), name="S-adenosylmethionine (SAM)",
    category="methylation_cycle", subcategory="methyl_donor",
    sample_type="plasma", units="nmol/L", reference_low="70", reference_high="125",
    what_it_measures="Universal methyl donor; substrate for all methyltransferases",
    elevated_means="Overmethylator phenotype; folate caution; potential mania risk",
    low_means="Undermethylator phenotype; impaired DNA/protein/lipid methylation",
    interpretation_summary="Paired with SAH to compute SAM/SAH ratio (methylation capacity)",
    mechanisms_indicated="MEC-0003", phenotypes_stratified="PHE-0001",
    interventions_modulates="INT-0001,INT-0008", hypotheses_tests="HYP-0001",
    key_pmids="15585776", lab_options="Doctor's Data, Genova",
    test_cost_usd_low="80", test_cost_usd_high="180", clia_status="CLIA",
    notes="Foundational methylation biomarker per James Jill 2004 Am J Clin Nutr framework.")

add(id=nxt(), name="S-adenosylhomocysteine (SAH)",
    category="methylation_cycle", sample_type="plasma", units="nmol/L",
    reference_low="10", reference_high="30",
    what_it_measures="Methyltransferase product; rises when methylation outflow blocked",
    elevated_means="Methylation-cycle inhibition; usually paired with low SAM/SAH ratio",
    low_means="Generally non-pathological",
    mechanisms_indicated="MEC-0003", interventions_modulates="INT-0001,INT-0008",
    hypotheses_tests="HYP-0001", key_pmids="15585776",
    lab_options="Doctor's Data, Genova", test_cost_usd_low="80", test_cost_usd_high="180")

add(id=nxt(), name="SAM/SAH ratio",
    category="methylation_cycle", subcategory="methylation_capacity",
    sample_type="plasma", units="ratio",
    reference_low="3.0", reference_high="6.0",
    reference_optimal_low="4.0", reference_optimal_high="6.0",
    what_it_measures="Net methylation capacity — the single most informative methylation biomarker",
    low_means="Impaired methylation; undermethylator state; leucovorin/methyl-B12 candidate",
    elevated_means="Overmethylator state; folate caution",
    snp_dependence="MTHFR C677T, MTRR, MTR, BHMT all affect interpretation",
    mechanisms_indicated="MEC-0003", phenotypes_stratified="PHE-0001",
    interventions_modulates="INT-0001,INT-0008", hypotheses_tests="HYP-0001,HYP-0003",
    key_pmids="15585776,19056591", lab_options="Doctor's Data DDI methylation panel",
    notes="Per Walsh biotyping framework + James biochemistry foundation.")

add(id=nxt(), name="Plasma methionine",
    category="methylation_cycle", sample_type="plasma", units="μmol/L",
    reference_low="15", reference_high="40",
    what_it_measures="Methionine cycle substrate; derived from dietary intake + remethylation",
    low_means="Methionine cycle compromise; consider methyl-B12 + betaine",
    elevated_means="Possible MAT defect (rare) or supplementation",
    mechanisms_indicated="MEC-0003", interventions_modulates="INT-0001",
    hypotheses_tests="HYP-0001", key_pmids="15585776")

add(id=nxt(), name="Homocysteine",
    category="methylation_cycle", sample_type="plasma", units="μmol/L",
    reference_low="3.5", reference_high="10",
    reference_optimal_high="7",
    what_it_measures="Methionine-cycle intermediate; remethylation + transsulfuration capacity",
    elevated_means="B12/folate/B6 insufficiency; CBS pathway slowdown; cardiovascular + neurodegenerative risk",
    low_means="Normal or slight CBS upregulation",
    snp_dependence="MTHFR, CBS, MTRR genotype changes interpretation",
    mechanisms_indicated="MEC-0003", interventions_modulates="INT-0001,INT-0008",
    hypotheses_tests="HYP-0001,HYP-0003", key_pmids="15585776",
    test_availability="standard_clinical", test_cost_usd_low="40", test_cost_usd_high="100",
    clia_status="CLIA", lab_options="Quest, LabCorp")

add(id=nxt(), name="Cysteine",
    category="methylation_cycle", subcategory="transsulfuration",
    sample_type="plasma", units="μmol/L", reference_low="200", reference_high="350",
    what_it_measures="Transsulfuration product; substrate for glutathione synthesis",
    low_means="Glutathione synthesis precursor depletion",
    interventions_modulates="INT-0001", hypotheses_tests="HYP-0063",
    key_pmids="15585776")

add(id=nxt(), name="Taurine",
    category="methylation_cycle", subcategory="transsulfuration",
    sample_type="plasma", units="μmol/L", reference_low="50", reference_high="180",
    what_it_measures="Transsulfuration end-product; bile acid conjugation; GABA-like inhibitory",
    low_means="Transsulfuration insufficiency",
    mechanisms_indicated="MEC-0003,MEC-0007", key_pmids="15585776")

add(id=nxt(), name="Methylmalonic acid (MMA)",
    category="methylation_cycle", subcategory="b12_functional",
    sample_type="serum_or_urine", units="nmol/L",
    reference_low="0", reference_high="270",
    what_it_measures="Functional B12 status — elevated when B12 cofactor activity is insufficient regardless of plasma B12 level",
    elevated_means="Functional B12 deficiency even if plasma B12 normal",
    interpretation_summary="More sensitive than plasma B12 alone for cellular B12 status",
    interventions_modulates="INT-0001", hypotheses_tests="HYP-0001",
    test_availability="standard_clinical", clia_status="CLIA", lab_options="Quest, LabCorp")

add(id=nxt(), name="Plasma B12 (cobalamin)",
    category="methylation_cycle", sample_type="serum", units="pg/mL",
    reference_low="200", reference_high="900",
    reference_optimal_low="500",
    what_it_measures="Total cobalamin; gross B12 sufficiency",
    low_means="Functional B12 deficiency likely (confirm with MMA + holotranscobalamin)",
    interpretation_summary="Should be >500 pg/mL in autistic kids; mainstream 'normal' often inadequate",
    interventions_modulates="INT-0001", clia_status="CLIA")

add(id=nxt(), name="Holotranscobalamin (active B12)",
    category="methylation_cycle", sample_type="plasma", units="pmol/L",
    reference_low="35", reference_high="170",
    what_it_measures="Biologically-active B12 fraction (transcobalamin-bound)",
    interpretation_summary="More specific than total B12 for cellular delivery",
    interventions_modulates="INT-0001", clia_status="CLIA",
    test_availability="specialty_clinical")

add(id=nxt(), name="Plasma folate",
    category="methylation_cycle", sample_type="serum", units="ng/mL",
    reference_low="3", reference_high="20",
    interpretation_summary="Acute folate status; reflects recent intake",
    interventions_modulates="INT-0001,INT-0008",
    hypotheses_tests="HYP-0003", test_availability="standard_clinical",
    clia_status="CLIA")

add(id=nxt(), name="RBC folate",
    category="methylation_cycle", sample_type="whole_blood_rbc", units="ng/mL",
    reference_low="280", reference_high="800",
    interpretation_summary="Long-term folate status (4+ months); preferred over plasma",
    snp_dependence="MTHFR C677T affects 5-MTHF activation efficiency",
    interventions_modulates="INT-0001,INT-0008",
    hypotheses_tests="HYP-0003", clia_status="CLIA")

add(id=nxt(), name="Pyridoxal-5-phosphate (P5P / active B6)",
    category="methylation_cycle", subcategory="cofactor",
    sample_type="plasma", units="ng/mL", reference_low="5", reference_high="50",
    what_it_measures="Active B6 form; cofactor for >100 enzymes including transsulfuration, kynurenine pathway",
    low_means="B6 cofactor insufficiency; pyroluria risk if low",
    mechanisms_indicated="MEC-0003,MEC-0023", clia_status="CLIA")

add(id=nxt(), name="Whole-blood histamine",
    category="methylation_cycle", subcategory="biotype_proxy",
    sample_type="whole_blood", units="ng/mL",
    reference_low="40", reference_high="80",
    what_it_measures="Walsh biotype proxy — methylation status indicator",
    elevated_means="Overmethylator phenotype likely",
    low_means="Undermethylator phenotype likely",
    interpretation_summary="Per Walsh biotyping; used clinically since 1970s",
    mechanisms_indicated="MEC-0003,MEC-0017",
    interventions_modulates="INT-0001",
    test_availability="specialty_clinical",
    lab_options="Direct Healthcare, ALCAT")

# ────────────────────────────────────────────────────────────
# CATEGORY 2: FOLATE-RECEPTOR / CEREBRAL FOLATE
# ────────────────────────────────────────────────────────────
add(id=nxt(), name="FRAA (folate receptor alpha autoantibody) — blocking",
    category="folate_receptor", subcategory="autoantibody",
    sample_type="serum", units="pmol/mL FBA",
    reference_low="0", reference_high="0.5",
    what_it_measures="Autoantibody blocking folate transport across blood-brain barrier",
    elevated_means="Cerebral folate deficiency likely; leucovorin candidate",
    interpretation_summary="The single most important biomarker for predicting leucovorin response in autism",
    mechanisms_indicated="MEC-0003,MEC-0004",
    phenotypes_stratified="PHE-0001",
    interventions_modulates="INT-0001",
    hypotheses_tests="HYP-0001",
    key_pmids="27752075",
    test_availability="specialty_research_lab",
    lab_options="Religious Sisters of Mercy / Ramaekers lab; some commercial",
    test_cost_usd_low="200", test_cost_usd_high="400",
    notes="Frye 2018 RCT used this stratification. ~70-75% of autistic children FRAA+.")

add(id=nxt(), name="FRAA (folate receptor alpha autoantibody) — binding",
    category="folate_receptor", subcategory="autoantibody",
    sample_type="serum", units="pmol/mL FRA",
    reference_low="0", reference_high="2.0",
    what_it_measures="Autoantibody binding (not necessarily blocking) folate receptor",
    interpretation_summary="Less specific than blocking but useful when blocking is borderline",
    mechanisms_indicated="MEC-0004", phenotypes_stratified="PHE-0001",
    interventions_modulates="INT-0001", hypotheses_tests="HYP-0001",
    key_pmids="27752075", lab_options="Religious Sisters of Mercy")

add(id=nxt(), name="CSF 5-MTHF",
    category="folate_receptor", subcategory="cerebral_folate_direct",
    sample_type="cerebrospinal_fluid", units="nmol/L",
    reference_low="40", reference_high="180",
    what_it_measures="Direct measurement of cerebral folate; gold-standard for cerebral folate deficiency diagnosis",
    low_means="Cerebral folate deficiency confirmed; high-dose leucovorin indicated",
    interpretation_summary="Invasive (lumbar puncture); reserved for confirmed clinical suspicion. CSF/serum ratio <1 is diagnostic for transport defect.",
    mechanisms_indicated="MEC-0003,MEC-0004", phenotypes_stratified="PHE-0001",
    interventions_modulates="INT-0001", hypotheses_tests="HYP-0001",
    test_availability="research_or_specialist", clia_status="CLIA",
    notes="Diagnostic gold standard but invasive. Most workups stop at FRAA + clinical response trial.")

# ────────────────────────────────────────────────────────────
# CATEGORY 3: MITOCHONDRIAL
# ────────────────────────────────────────────────────────────
add(id=nxt(), name="Lactate",
    category="mitochondrial", subcategory="anaerobic_shift",
    sample_type="plasma", units="mmol/L",
    reference_low="0.5", reference_high="2.2",
    what_it_measures="Anaerobic metabolism marker; rises when oxidative phosphorylation can't meet ATP demand",
    elevated_means="Mitochondrial dysfunction; pyruvate dehydrogenase deficiency; respiratory chain defect",
    interpretation_summary="Compare resting vs post-exertion; resting elevation more concerning",
    mechanisms_indicated="MEC-0010", phenotypes_stratified="PHE-0002",
    interventions_modulates="", hypotheses_tests="HYP-0006,HYP-0070",
    key_pmids="21263444",
    test_availability="standard_clinical", clia_status="CLIA",
    test_cost_usd_low="20", test_cost_usd_high="60")

add(id=nxt(), name="Pyruvate",
    category="mitochondrial", sample_type="plasma", units="mmol/L",
    reference_low="0.04", reference_high="0.10",
    what_it_measures="Glycolysis end-product; substrate for pyruvate dehydrogenase",
    interpretation_summary="Always paired with lactate to compute L:P ratio",
    mechanisms_indicated="MEC-0010", hypotheses_tests="HYP-0006,HYP-0070",
    key_pmids="21263444", clia_status="CLIA")

add(id=nxt(), name="Lactate-to-pyruvate ratio (L:P)",
    category="mitochondrial", subcategory="oxphos_indicator",
    sample_type="plasma", units="ratio", reference_low="10", reference_high="25",
    what_it_measures="Most sensitive biochemical screen for respiratory-chain deficiency",
    elevated_means="L:P > 25 suggests OXPHOS / respiratory chain dysfunction",
    interpretation_summary="More informative than lactate alone; primary screen for mito disease",
    mechanisms_indicated="MEC-0010", phenotypes_stratified="PHE-0002",
    hypotheses_tests="HYP-0006,HYP-0070", key_pmids="21263444",
    notes="Calibration anchor for HYP-0070.")

add(id=nxt(), name="Acylcarnitine profile",
    category="mitochondrial", subcategory="fatty_acid_oxidation",
    sample_type="plasma_or_dbs", units="μmol/L composite",
    what_it_measures="Fatty acid oxidation defects; carnitine metabolism",
    elevated_means="Specific patterns indicate specific FAO defects (MCAD, VLCAD, etc.)",
    interpretation_summary="Newborn-screen tier panel; covers ~40 individual species",
    mechanisms_indicated="MEC-0010", phenotypes_stratified="PHE-0002",
    hypotheses_tests="HYP-0006", clia_status="CLIA",
    test_availability="standard_clinical")

add(id=nxt(), name="Free + total carnitine",
    category="mitochondrial", subcategory="cofactor",
    sample_type="plasma", units="μmol/L",
    reference_low="35", reference_high="80",
    what_it_measures="Carnitine substrate sufficiency for fatty acid transport into mitochondria",
    low_means="Carnitine deficiency; supplementation indicated",
    mechanisms_indicated="MEC-0010", interventions_modulates="",
    hypotheses_tests="HYP-0006", clia_status="CLIA")

add(id=nxt(), name="Plasma ammonia",
    category="mitochondrial", subcategory="urea_cycle",
    sample_type="plasma", units="μmol/L",
    reference_low="0", reference_high="50",
    what_it_measures="Urea cycle / mitochondrial nitrogen disposal",
    elevated_means="Urea cycle defect, valproate toxicity, mitochondrial overflow",
    mechanisms_indicated="MEC-0010", hypotheses_tests="HYP-0006",
    clia_status="CLIA")

add(id=nxt(), name="Creatine kinase (CK)",
    category="mitochondrial", subcategory="muscle_metabolism",
    sample_type="serum", units="U/L",
    reference_low="30", reference_high="200",
    what_it_measures="Muscle damage / mitochondrial myopathy marker",
    elevated_means="Mitochondrial myopathy possible; rule out other causes",
    mechanisms_indicated="MEC-0010", hypotheses_tests="HYP-0006",
    clia_status="CLIA", test_availability="standard_clinical")

add(id=nxt(), name="CoQ10 (ubiquinone)",
    category="mitochondrial", subcategory="cofactor",
    sample_type="plasma", units="μg/mL",
    reference_low="0.5", reference_high="2.0",
    what_it_measures="Respiratory chain electron carrier; statin-depletable",
    low_means="CoQ10 supplementation indicated; statin-induced or primary deficiency",
    mechanisms_indicated="MEC-0010", interventions_modulates="",
    hypotheses_tests="HYP-0006", test_cost_usd_low="120", test_cost_usd_high="200")

add(id=nxt(), name="mtDNA copy number",
    category="mitochondrial", subcategory="quantitative_genetics",
    sample_type="whole_blood_or_buccal", units="ratio",
    what_it_measures="Mitochondrial DNA quantity per cell; depletion = less ATP capacity",
    interpretation_summary="Research-grade; specialty mito-disease centers",
    mechanisms_indicated="MEC-0010", hypotheses_tests="HYP-0006",
    test_availability="specialty_research")

add(id=nxt(), name="Krebs cycle metabolites (citrate/succinate/fumarate/malate)",
    category="mitochondrial", subcategory="oxphos_intermediates",
    sample_type="urine_oat", units="μmol/g creatinine composite",
    what_it_measures="OAT panel coverage of citric acid cycle; abnormal patterns indicate specific complex deficiencies",
    interpretation_summary="Mosaic OAT covers these as standard panel components",
    mechanisms_indicated="MEC-0010", hypotheses_tests="HYP-0006",
    lab_options="Mosaic OAT, Genova ION")

# ────────────────────────────────────────────────────────────
# CATEGORY 4: OXIDATIVE STRESS
# ────────────────────────────────────────────────────────────
add(id=nxt(), name="Reduced glutathione (GSH)",
    category="oxidative_stress", subcategory="antioxidant",
    sample_type="rbc_or_whole_blood", units="μmol/L",
    reference_low="900", reference_high="1500",
    what_it_measures="Active reduced glutathione; brain's primary antioxidant",
    low_means="Antioxidant depletion; oxidative stress; NAC + glycine + glutamine indicated",
    mechanisms_indicated="MEC-0001",
    interventions_modulates="INT-0001",
    hypotheses_tests="HYP-0063", key_pmids="15585776",
    test_availability="specialty_clinical")

add(id=nxt(), name="Oxidized glutathione (GSSG)",
    category="oxidative_stress", sample_type="rbc_or_whole_blood",
    units="μmol/L", reference_low="20", reference_high="50",
    what_it_measures="Oxidized glutathione fraction",
    elevated_means="Oxidative stress consuming reduced glutathione",
    mechanisms_indicated="MEC-0001", hypotheses_tests="HYP-0063",
    key_pmids="15585776")

add(id=nxt(), name="GSH/GSSG ratio",
    category="oxidative_stress", subcategory="redox_status",
    sample_type="rbc_or_whole_blood", units="ratio",
    reference_low="20", reference_high="100", reference_optimal_low="50",
    what_it_measures="Redox status — most informative single oxidative stress biomarker",
    low_means="Significant oxidative stress; antioxidant intervention high priority",
    mechanisms_indicated="MEC-0001", hypotheses_tests="HYP-0063",
    key_pmids="15585776,19056591",
    notes="James 2004/2009 framework primary biomarker.")

add(id=nxt(), name="8-hydroxy-2-deoxyguanosine (8-OHdG)",
    category="oxidative_stress", subcategory="dna_oxidation",
    sample_type="urine_24h", units="μg/g creatinine",
    reference_low="0", reference_high="10",
    what_it_measures="Oxidative DNA damage marker",
    elevated_means="Genomic oxidative stress; antioxidant intervention indicated",
    mechanisms_indicated="MEC-0001",
    test_availability="specialty_clinical",
    lab_options="Mosaic, Doctor's Data, Genova")

add(id=nxt(), name="F2-isoprostanes",
    category="oxidative_stress", subcategory="lipid_peroxidation",
    sample_type="urine_or_plasma", units="ng/mL",
    what_it_measures="Lipid peroxidation marker; arachidonic acid oxidation product",
    elevated_means="Lipid oxidative damage; high omega-3 + antioxidants",
    mechanisms_indicated="MEC-0001",
    test_availability="research_to_specialty")

add(id=nxt(), name="Malondialdehyde (MDA)",
    category="oxidative_stress", subcategory="lipid_peroxidation",
    sample_type="serum", units="μmol/L",
    what_it_measures="Lipid peroxidation breakdown product",
    elevated_means="Lipid oxidative stress active",
    mechanisms_indicated="MEC-0001")

add(id=nxt(), name="Superoxide dismutase (SOD) activity",
    category="oxidative_stress", subcategory="antioxidant_enzyme",
    sample_type="rbc", units="U/g Hb",
    what_it_measures="Mn-SOD + Cu/Zn-SOD enzymatic activity",
    low_means="Reduced antioxidant defense capacity",
    mechanisms_indicated="MEC-0001", test_availability="specialty_clinical")

add(id=nxt(), name="Total antioxidant capacity (TEAC/TAC)",
    category="oxidative_stress", subcategory="composite",
    sample_type="serum", units="mmol Trolox eq/L",
    what_it_measures="Composite antioxidant defense capacity",
    low_means="Net antioxidant insufficiency",
    mechanisms_indicated="MEC-0001")

# ────────────────────────────────────────────────────────────
# CATEGORY 5: OAT MICROBIAL METABOLITES
# ────────────────────────────────────────────────────────────
add(id=nxt(), name="Arabinose",
    category="oat_microbial", subcategory="fungal_marker",
    sample_type="urine", units="mmol/mol creatinine", reference_high="29",
    what_it_measures="Yeast/Candida fermentation product; primary fungal overgrowth marker",
    elevated_means="Candida overgrowth; antifungal protocol candidate",
    mechanisms_indicated="MEC-0008", phenotypes_stratified="PHE-0004",
    interventions_modulates="INT-0025,INT-0076", hypotheses_tests="HYP-0007,HYP-0061",
    lab_options="Mosaic OAT, Great Plains Lab",
    test_cost_usd_low="300", test_cost_usd_high="400",
    notes="Per Shaw William framework. Most-clinically-actionable single OAT marker.")

add(id=nxt(), name="HPHPA (3-(3-hydroxyphenyl)-3-hydroxypropionic acid)",
    category="oat_microbial", subcategory="clostridia_marker",
    sample_type="urine", units="mmol/mol creatinine", reference_high="220",
    what_it_measures="Clostridia metabolite; inhibits dopamine beta-hydroxylase",
    elevated_means="Clostridia overgrowth; behavioral/dopamine effects; targeted antibiotic candidate",
    mechanisms_indicated="MEC-0008,MEC-0024",
    phenotypes_stratified="PHE-0004",
    interventions_modulates="INT-0076,INT-0025",
    hypotheses_tests="HYP-0007,HYP-0057,HYP-0060",
    lab_options="Mosaic OAT")

add(id=nxt(), name="4-cresol (p-cresol)",
    category="oat_microbial", subcategory="clostridia_marker",
    sample_type="urine", units="mmol/mol creatinine",
    what_it_measures="Aromatic-amino-acid Clostridia metabolite; behavioral severity correlate",
    elevated_means="Clostridia overgrowth; correlates with autism severity scores",
    mechanisms_indicated="MEC-0024", phenotypes_stratified="PHE-0004",
    interventions_modulates="INT-0076,INT-0025",
    hypotheses_tests="HYP-0007,HYP-0057,HYP-0060",
    lab_options="Mosaic OAT")

add(id=nxt(), name="Tartaric acid",
    category="oat_microbial", subcategory="fungal_marker",
    sample_type="urine", units="mmol/mol creatinine",
    what_it_measures="Fungal fermentation product",
    elevated_means="Fungal/yeast overgrowth",
    mechanisms_indicated="MEC-0008", interventions_modulates="INT-0025",
    hypotheses_tests="HYP-0061", lab_options="Mosaic OAT")

add(id=nxt(), name="Citramalic acid",
    category="oat_microbial", subcategory="fungal_marker",
    sample_type="urine", units="mmol/mol creatinine",
    what_it_measures="Fungal metabolite",
    elevated_means="Fungal overgrowth",
    hypotheses_tests="HYP-0061", lab_options="Mosaic OAT")

add(id=nxt(), name="Indican",
    category="oat_microbial", subcategory="bacterial_putrefaction",
    sample_type="urine", units="qualitative or quantitative",
    what_it_measures="Bacterial tryptophan putrefaction product",
    elevated_means="Bacterial overgrowth + protein putrefaction in gut",
    mechanisms_indicated="MEC-0008", lab_options="Mosaic OAT, Great Plains")

add(id=nxt(), name="Hippuric acid",
    category="oat_microbial", subcategory="microbial_aromatic",
    sample_type="urine", units="mmol/mol creatinine",
    what_it_measures="Microbial benzoate metabolism",
    interpretation_summary="Variable interpretation; depends on diet + microbial composition",
    lab_options="Mosaic OAT")

add(id=nxt(), name="Indol-3-acetic acid (IAA)",
    category="oat_microbial", subcategory="tryptophan_microbial",
    sample_type="urine", units="mmol/mol creatinine",
    what_it_measures="Tryptophan-derived microbial metabolite (AhR ligand)",
    mechanisms_indicated="MEC-0023", lab_options="Mosaic OAT")

add(id=nxt(), name="3,4-dihydroxyphenylpropionic acid (DHPPA)",
    category="oat_microbial", subcategory="clostridia_marker",
    sample_type="urine", units="mmol/mol creatinine",
    what_it_measures="Clostridia tyrosine metabolite",
    interventions_modulates="INT-0076", lab_options="Mosaic OAT")

add(id=nxt(), name="3-Hydroxy-2-methylbutyric acid",
    category="oat_microbial", subcategory="bacterial_overgrowth",
    sample_type="urine", units="mmol/mol creatinine",
    what_it_measures="Bacterial branched-chain amino acid metabolism",
    lab_options="Mosaic OAT")

# ────────────────────────────────────────────────────────────
# CATEGORY 6: OAT NEUROTRANSMITTER METABOLITES
# ────────────────────────────────────────────────────────────
add(id=nxt(), name="Homovanillic acid (HVA)",
    category="oat_neurotransmitter", subcategory="dopamine_metabolite",
    sample_type="urine", units="mmol/mol creatinine",
    what_it_measures="Dopamine end-metabolite; dopaminergic tone",
    interpretation_summary="Pair with VMA; HPHPA can artificially lower HVA via DBH inhibition",
    mechanisms_indicated="MEC-0007", lab_options="Mosaic OAT")

add(id=nxt(), name="Vanillylmandelic acid (VMA)",
    category="oat_neurotransmitter", subcategory="norepinephrine_metabolite",
    sample_type="urine", units="mmol/mol creatinine",
    what_it_measures="Norepinephrine end-metabolite",
    mechanisms_indicated="MEC-0007", lab_options="Mosaic OAT")

add(id=nxt(), name="5-hydroxyindoleacetic acid (5-HIAA)",
    category="oat_neurotransmitter", subcategory="serotonin_metabolite",
    sample_type="urine", units="mmol/mol creatinine",
    what_it_measures="Serotonin end-metabolite; serotonin pathway readout",
    mechanisms_indicated="MEC-0023", hypotheses_tests="HYP-0062",
    lab_options="Mosaic OAT")

add(id=nxt(), name="Quinolinic acid",
    category="oat_neurotransmitter", subcategory="kynurenine_pathway",
    sample_type="urine", units="mmol/mol creatinine",
    what_it_measures="Kynurenine-pathway NMDA agonist; neurotoxic at elevation",
    elevated_means="Pro-inflammatory kynurenine shift; tryptophan diverted away from serotonin",
    mechanisms_indicated="MEC-0023,MEC-0020", lab_options="Mosaic OAT")

add(id=nxt(), name="Kynurenic acid",
    category="oat_neurotransmitter", subcategory="kynurenine_pathway",
    sample_type="urine", units="mmol/mol creatinine",
    what_it_measures="Kynurenine-pathway NMDA antagonist; neuroprotective",
    interpretation_summary="QUIN/KYN ratio is most informative",
    mechanisms_indicated="MEC-0023")

add(id=nxt(), name="Kynurenine/tryptophan ratio",
    category="oat_neurotransmitter", subcategory="ido_activity",
    sample_type="plasma", units="ratio",
    what_it_measures="IDO/TDO activity; inflammation-driven tryptophan depletion",
    elevated_means="Inflammation diverting tryptophan to kynurenine pathway",
    mechanisms_indicated="MEC-0002,MEC-0023")

# ────────────────────────────────────────────────────────────
# CATEGORY 7: IMMUNE / INFLAMMATORY CYTOKINES
# ────────────────────────────────────────────────────────────
add(id=nxt(), name="High-sensitivity CRP (hs-CRP)",
    category="immune_inflammatory", subcategory="acute_phase",
    sample_type="serum", units="mg/L", reference_high="3.0",
    reference_optimal_high="1.0",
    what_it_measures="Systemic inflammation",
    elevated_means="Active inflammation; >3 = high cardiovascular + neurodevelopmental risk",
    mechanisms_indicated="MEC-0002", hypotheses_tests="HYP-0008",
    test_availability="standard_clinical", clia_status="CLIA",
    test_cost_usd_low="20", test_cost_usd_high="50")

add(id=nxt(), name="ESR (erythrocyte sedimentation rate)",
    category="immune_inflammatory", subcategory="acute_phase",
    sample_type="whole_blood", units="mm/hr",
    what_it_measures="Indirect inflammation marker; less specific than CRP",
    mechanisms_indicated="MEC-0002", clia_status="CLIA")

add(id=nxt(), name="IL-6 (interleukin-6)",
    category="immune_inflammatory", subcategory="cytokine",
    sample_type="serum", units="pg/mL", reference_high="5",
    what_it_measures="Pro-inflammatory cytokine; elevated in many ASD subgroups",
    elevated_means="Active inflammation; cell therapy responder profile per Dawson 2020 subgroup analysis",
    mechanisms_indicated="MEC-0002,MEC-0005", hypotheses_tests="HYP-0008",
    interventions_modulates="INT-0102,INT-0006",
    test_availability="specialty_clinical")

add(id=nxt(), name="TNF-α (tumor necrosis factor alpha)",
    category="immune_inflammatory", subcategory="cytokine",
    sample_type="serum", units="pg/mL",
    what_it_measures="Master pro-inflammatory cytokine; central node in autism inflammation networks",
    elevated_means="Active TNF-driven inflammation",
    mechanisms_indicated="MEC-0002,MEC-0005", hypotheses_tests="HYP-0008",
    interventions_modulates="INT-0102,INT-0006",
    test_availability="specialty_clinical")

add(id=nxt(), name="IL-1β (interleukin-1 beta)",
    category="immune_inflammatory", subcategory="cytokine",
    sample_type="serum", units="pg/mL",
    what_it_measures="NLRP3-inflammasome cytokine; microglial activation",
    mechanisms_indicated="MEC-0002,MEC-0005", hypotheses_tests="HYP-0008")

add(id=nxt(), name="IL-17",
    category="immune_inflammatory", subcategory="cytokine",
    sample_type="serum", units="pg/mL",
    what_it_measures="Th17 axis; IL-17a drives autoimmune-spectrum inflammation",
    mechanisms_indicated="MEC-0002", hypotheses_tests="HYP-0008")

add(id=nxt(), name="IL-10",
    category="immune_inflammatory", subcategory="cytokine",
    sample_type="serum", units="pg/mL",
    what_it_measures="Anti-inflammatory cytokine; Treg activity proxy",
    low_means="Inadequate immune regulation",
    mechanisms_indicated="MEC-0002")

add(id=nxt(), name="IFN-γ (interferon gamma)",
    category="immune_inflammatory", subcategory="cytokine",
    sample_type="serum", units="pg/mL",
    what_it_measures="Th1 axis; chronic-infection / cellular-immunity marker",
    mechanisms_indicated="MEC-0002")

add(id=nxt(), name="Complement C3, C4",
    category="immune_inflammatory", subcategory="complement",
    sample_type="serum", units="mg/dL",
    what_it_measures="Complement system activity; neuroinflammation marker (C1q, C3 elevated in ASD postmortem)",
    mechanisms_indicated="MEC-0002,MEC-0005", clia_status="CLIA")

add(id=nxt(), name="Total IgG / IgA / IgM / IgE + IgG subclasses",
    category="immune_inflammatory", subcategory="immunoglobulin",
    sample_type="serum", units="mg/dL",
    what_it_measures="Humoral immunity status + atopic profile",
    interpretation_summary="Low IgA common in ASD; IgG subclass deficiency ↔ recurrent infection",
    mechanisms_indicated="MEC-0002", clia_status="CLIA")

# ────────────────────────────────────────────────────────────
# CATEGORY 8: MAST CELL ACTIVATION
# ────────────────────────────────────────────────────────────
add(id=nxt(), name="Tryptase (baseline)",
    category="mast_cell", subcategory="primary_diagnostic",
    sample_type="serum", units="ng/mL", reference_high="11.4",
    what_it_measures="Mast cell mediator; baseline elevation suggests mastocytosis/MCAS",
    elevated_means=">11.4 = abnormal; >20 = mastocytosis; ≥1.2x baseline + 2 ng/mL during flare = MCAS",
    mechanisms_indicated="MEC-0017", hypotheses_tests="HYP-0008",
    interventions_modulates="", clia_status="CLIA",
    notes="Per Theoharides framework. Most-specific single MCAS marker.")

add(id=nxt(), name="N-methylhistamine (urinary)",
    category="mast_cell", subcategory="histamine_metabolite",
    sample_type="urine_24h", units="μg/g creatinine",
    what_it_measures="Histamine release marker; more stable than histamine itself",
    elevated_means="Mast cell or basophil histamine release",
    mechanisms_indicated="MEC-0017", clia_status="CLIA",
    test_availability="specialty_clinical")

add(id=nxt(), name="Prostaglandin D2 metabolite (11β-PGF2α)",
    category="mast_cell", subcategory="prostaglandin",
    sample_type="urine_24h", units="ng/g creatinine",
    what_it_measures="Mast cell prostaglandin release",
    mechanisms_indicated="MEC-0017", clia_status="CLIA")

add(id=nxt(), name="Chromogranin A",
    category="mast_cell", subcategory="neuroendocrine",
    sample_type="serum", units="ng/mL",
    what_it_measures="Neuroendocrine cell + mast cell granule protein",
    mechanisms_indicated="MEC-0017", clia_status="CLIA")

add(id=nxt(), name="Heparin (mast cell)",
    category="mast_cell", subcategory="granule_marker",
    sample_type="plasma", units="varies",
    what_it_measures="Mast cell granule heparin release",
    test_availability="research")

# ────────────────────────────────────────────────────────────
# CATEGORY 9: PANS/PANDAS ANTIBODY (Cunningham Panel)
# ────────────────────────────────────────────────────────────
add(id=nxt(), name="Anti-tubulin antibody (Cunningham Panel)",
    category="pans_pandas", subcategory="cunningham_panel",
    sample_type="serum", units="titer",
    what_it_measures="Anti-neuronal antibody cross-reacting with neuronal cytoskeleton",
    elevated_means="PANS/PANDAS likely; immune therapy candidate",
    mechanisms_indicated="MEC-0002", hypotheses_tests="HYP-0026",
    interventions_modulates="INT-0006",
    test_availability="specialty",
    lab_options="Moleculera Biosciences",
    test_cost_usd_low="900", test_cost_usd_high="1100",
    notes="Per Cunningham Madeleine framework. Composite score predicts immune-therapy response.")

add(id=nxt(), name="Anti-lysoganglioside-GM1 antibody",
    category="pans_pandas", subcategory="cunningham_panel",
    sample_type="serum", units="titer",
    what_it_measures="Anti-neuronal antibody cross-reacting with neuronal ganglioside",
    mechanisms_indicated="MEC-0002", hypotheses_tests="HYP-0026",
    lab_options="Moleculera")

add(id=nxt(), name="Anti-dopamine D1 receptor antibody",
    category="pans_pandas", subcategory="cunningham_panel",
    sample_type="serum", units="titer",
    what_it_measures="Anti-D1 receptor autoantibody",
    mechanisms_indicated="MEC-0002,MEC-0007",
    hypotheses_tests="HYP-0026", lab_options="Moleculera")

add(id=nxt(), name="Anti-dopamine D2 receptor antibody",
    category="pans_pandas", subcategory="cunningham_panel",
    sample_type="serum", units="titer",
    what_it_measures="Anti-D2 receptor autoantibody; correlates with OCD/tic features",
    mechanisms_indicated="MEC-0002,MEC-0007",
    hypotheses_tests="HYP-0026", lab_options="Moleculera")

add(id=nxt(), name="CaMKII activation",
    category="pans_pandas", subcategory="cunningham_panel",
    sample_type="serum", units="% activation",
    what_it_measures="Calcium/calmodulin-dependent kinase II activation by patient serum on neuronal cells; composite functional readout of Cunningham Panel",
    elevated_means="Active anti-neuronal antibody-mediated dysfunction; immune therapy responder",
    interpretation_summary="Most-clinically-actionable single output of Cunningham Panel",
    mechanisms_indicated="MEC-0002", hypotheses_tests="HYP-0026",
    lab_options="Moleculera",
    notes="Reliability critique per Hesselmark 2019 — panel works best as confirmatory in clinically-suspected cases.")

add(id=nxt(), name="ASO (antistreptolysin O)",
    category="pans_pandas", subcategory="strep_titer",
    sample_type="serum", units="IU/mL",
    what_it_measures="Recent or active group A strep infection",
    interpretation_summary="Combined with anti-DNase B for full strep workup",
    mechanisms_indicated="MEC-0002", hypotheses_tests="HYP-0026",
    clia_status="CLIA", test_availability="standard_clinical")

add(id=nxt(), name="Anti-DNase B",
    category="pans_pandas", subcategory="strep_titer",
    sample_type="serum", units="IU/mL",
    what_it_measures="Strep infection marker; rises later than ASO",
    mechanisms_indicated="MEC-0002", hypotheses_tests="HYP-0026",
    clia_status="CLIA")

# ────────────────────────────────────────────────────────────
# CATEGORY 10: HEAVY METALS / TOXICANTS
# ────────────────────────────────────────────────────────────
add(id=nxt(), name="Hair mercury",
    category="heavy_metals", subcategory="long_term_exposure",
    sample_type="hair", units="μg/g",
    what_it_measures="Long-term mercury exposure (months); reflects body-burden",
    interpretation_summary="Hair > urinary for chronic exposure assessment",
    mechanisms_indicated="MEC-0001,MEC-0010",
    hypotheses_tests="HYP-0015,HYP-0069",
    lab_options="Doctor's Data, Quicksilver Scientific",
    test_cost_usd_low="80", test_cost_usd_high="150")

add(id=nxt(), name="Hair lead",
    category="heavy_metals", subcategory="long_term_exposure",
    sample_type="hair", units="μg/g",
    what_it_measures="Long-term lead exposure",
    mechanisms_indicated="MEC-0001",
    hypotheses_tests="HYP-0015", lab_options="Doctor's Data")

add(id=nxt(), name="Urine mercury (provoked or unprovoked)",
    category="heavy_metals", subcategory="excretion",
    sample_type="urine", units="μg/g creatinine",
    what_it_measures="Acute mercury excretion; provoked test (DMSA challenge) reveals body-burden",
    interpretation_summary="Provoked vs unprovoked interpretation differs substantially",
    mechanisms_indicated="MEC-0001,MEC-0010", hypotheses_tests="HYP-0015,HYP-0069",
    lab_options="Doctor's Data, Quicksilver, Genova")

add(id=nxt(), name="Urine lead",
    category="heavy_metals", subcategory="excretion",
    sample_type="urine", units="μg/g creatinine",
    mechanisms_indicated="MEC-0001", hypotheses_tests="HYP-0015",
    lab_options="Doctor's Data")

add(id=nxt(), name="Urine cadmium",
    category="heavy_metals", subcategory="excretion",
    sample_type="urine", units="μg/g creatinine",
    mechanisms_indicated="MEC-0001", hypotheses_tests="HYP-0015")

add(id=nxt(), name="Urine arsenic",
    category="heavy_metals", subcategory="excretion",
    sample_type="urine", units="μg/g creatinine",
    interpretation_summary="Speciation matters: inorganic vs organic (rice/seafood)",
    mechanisms_indicated="MEC-0001", hypotheses_tests="HYP-0015")

add(id=nxt(), name="Urine aluminum",
    category="heavy_metals", subcategory="excretion",
    sample_type="urine", units="μg/g creatinine",
    what_it_measures="Aluminum body burden / excretion",
    interpretation_summary="Best paired with provocation challenge for body-burden assessment",
    mechanisms_indicated="MEC-0032", hypotheses_tests="HYP-0067",
    lab_options="Doctor's Data")

add(id=nxt(), name="Urine glyphosate + AMPA",
    category="heavy_metals", subcategory="agrochemical",
    sample_type="urine", units="μg/g creatinine",
    what_it_measures="Recent glyphosate exposure",
    interpretation_summary="Glyphosate disrupts methylation cycle, microbiome (shikimate pathway), sulfate metabolism",
    mechanisms_indicated="MEC-0003,MEC-0008",
    hypotheses_tests="HYP-0005",
    lab_options="HRI Labs, Mosaic Diagnostics, Great Plains",
    test_cost_usd_low="100", test_cost_usd_high="200",
    notes="Per Seneff Stephanie framework.")

# ────────────────────────────────────────────────────────────
# CATEGORY 11: ENVIRONMENTAL CHEMICALS
# ────────────────────────────────────────────────────────────
add(id=nxt(), name="Phthalate metabolites (composite — MEP, MBP, MEHP, others)",
    category="environmental_chemicals", subcategory="endocrine_disruptor",
    sample_type="urine", units="μg/g creatinine composite",
    what_it_measures="Phthalate exposure burden; endocrine disruption",
    mechanisms_indicated="MEC-0008,MEC-0016",
    hypotheses_tests="HYP-0011,HYP-0043",
    lab_options="Mosaic GPL-TOX, Genova")

add(id=nxt(), name="Bisphenol A (BPA)",
    category="environmental_chemicals", subcategory="endocrine_disruptor",
    sample_type="urine", units="μg/g creatinine",
    mechanisms_indicated="MEC-0016",
    hypotheses_tests="HYP-0012,HYP-0043",
    lab_options="Mosaic GPL-TOX")

add(id=nxt(), name="PFAS / PFOA composite",
    category="environmental_chemicals", subcategory="forever_chemicals",
    sample_type="serum", units="ng/mL composite",
    what_it_measures="Per- and polyfluoroalkyl substances body burden",
    interpretation_summary="Half-lives of years; reflects long-term exposure",
    mechanisms_indicated="MEC-0001,MEC-0016",
    hypotheses_tests="HYP-0004",
    lab_options="Quest, specialty environmental labs")

add(id=nxt(), name="Organophosphate metabolites (DAPs)",
    category="environmental_chemicals", subcategory="pesticide",
    sample_type="urine", units="μmol/g creatinine composite",
    what_it_measures="Recent organophosphate pesticide exposure (dialkyl phosphates)",
    mechanisms_indicated="MEC-0001",
    hypotheses_tests="HYP-0014",
    lab_options="research labs, some specialty")

add(id=nxt(), name="Mycotoxin panel (aflatoxin, ochratoxin, gliotoxin, trichothecenes)",
    category="environmental_chemicals", subcategory="mycotoxin",
    sample_type="urine", units="ng/g creatinine composite",
    what_it_measures="Mold-derived mycotoxin body burden",
    mechanisms_indicated="MEC-0001,MEC-0002",
    hypotheses_tests="HYP-0016",
    lab_options="Mosaic MycoTOX, Real Time Lab",
    test_cost_usd_low="300", test_cost_usd_high="500")

add(id=nxt(), name="Volatile solvents (composite)",
    category="environmental_chemicals", subcategory="solvent",
    sample_type="urine", units="μg/g creatinine",
    what_it_measures="Benzene, toluene, xylene, styrene exposure",
    mechanisms_indicated="MEC-0001",
    lab_options="Mosaic GPL-TOX")

# ────────────────────────────────────────────────────────────
# CATEGORY 12: MATERNAL / PARENTAL BIOMARKERS
# ────────────────────────────────────────────────────────────
add(id=nxt(), name="Maternal anti-fetal-brain antibodies (MAR Antibodies)",
    category="maternal_parental", subcategory="autoantibody",
    sample_type="maternal_serum", units="positive/negative + specific antigens",
    what_it_measures="Maternal autoantibodies cross-reacting with fetal brain antigens",
    elevated_means="Maternal autoantibody-related autism subgroup; autoantibody-related ASD diagnosis",
    interpretation_summary="Per Braunschweig / Van de Water framework; ~20% of mothers of autistic children test positive",
    mechanisms_indicated="MEC-0002", hypotheses_tests="HYP-0008,HYP-0051",
    test_availability="specialty_research",
    lab_options="UC Davis MIND Institute (research)")

add(id=nxt(), name="Maternal MTHFR genotype",
    category="maternal_parental", subcategory="genetic",
    sample_type="maternal_buccal_or_blood", units="genotype (CC/CT/TT for C677T; AA/AC/CC for A1298C)",
    what_it_measures="Maternal MTHFR variant status — affects folate cycle in pregnancy",
    interpretation_summary="Maternal C677T TT genotype + low folate elevates fetal NTD + ASD risk",
    snp_dependence="self",
    mechanisms_indicated="MEC-0003",
    hypotheses_tests="HYP-0003",
    interventions_modulates="INT-0008",
    test_availability="standard_clinical_or_dtc",
    lab_options="23andMe, Quest, LabCorp")

add(id=nxt(), name="Maternal serum vitamin D (during pregnancy)",
    category="maternal_parental", subcategory="nutritional",
    sample_type="maternal_serum", units="ng/mL", reference_low="30", reference_high="80",
    reference_optimal_low="40", reference_optimal_high="60",
    what_it_measures="Maternal vitamin D status during pregnancy — fetal neurodevelopment input",
    low_means="Maternal D deficiency; offspring autism + general neurodevelopmental risk elevated",
    mechanisms_indicated="MEC-0002,MEC-0029",
    hypotheses_tests="HYP-0020,HYP-0045",
    interventions_modulates="",
    clia_status="CLIA", test_availability="standard_clinical")

add(id=nxt(), name="Maternal CRP during pregnancy",
    category="maternal_parental", subcategory="inflammation",
    sample_type="maternal_serum", units="mg/L",
    what_it_measures="Maternal systemic inflammation during pregnancy",
    elevated_means="Maternal immune activation risk; neuroinflammation-mediated developmental risk to fetus",
    mechanisms_indicated="MEC-0002",
    hypotheses_tests="HYP-0008")

add(id=nxt(), name="Maternal thyroid panel during pregnancy",
    category="maternal_parental", subcategory="endocrine",
    sample_type="maternal_serum", units="composite",
    what_it_measures="Maternal TSH, FT3, FT4, TPO antibodies during pregnancy",
    interpretation_summary="Maternal hypothyroidism (even subclinical) elevates offspring neurodevelopmental risk",
    mechanisms_indicated="MEC-0016",
    hypotheses_tests="HYP-0035,HYP-0048",
    clia_status="CLIA")

add(id=nxt(), name="Cord blood acetaminophen / acetaminophen-protein adducts",
    category="maternal_parental", subcategory="exposure_marker",
    sample_type="cord_blood", units="ng/mL",
    what_it_measures="Direct measurement of fetal acetaminophen exposure at birth",
    elevated_means="Documented fetal acetaminophen exposure; per Ji 2020 acetaminophen-ADHD/ASD literature",
    mechanisms_indicated="MEC-0001",
    hypotheses_tests="HYP-0002",
    test_availability="research_only",
    notes="Ji 2020 cord-blood biomarker study evidence (PMID 32519281).")

add(id=nxt(), name="Cord-blood methylation signature",
    category="maternal_parental", subcategory="epigenetic",
    sample_type="cord_blood", units="composite methylation array",
    what_it_measures="Newborn methylation profile reflecting in-utero environment",
    interpretation_summary="Research-grade; predictive for autism in some emerging analyses",
    mechanisms_indicated="MEC-0003",
    hypotheses_tests="HYP-0072",
    test_availability="research_only")

add(id=nxt(), name="Paternal age",
    category="maternal_parental", subcategory="epidemiologic",
    sample_type="self_report", units="years",
    what_it_measures="Paternal age at conception",
    elevated_means="Older paternal age (>40) elevates de novo mutation rate + sperm methylation drift",
    interpretation_summary="Strong epidemiological signal; mechanistically epigenetic + de novo SNV",
    mechanisms_indicated="MEC-0003",
    hypotheses_tests="HYP-0009,HYP-0072")

# ────────────────────────────────────────────────────────────
# CATEGORY 13: TRACE MINERALS
# ────────────────────────────────────────────────────────────
add(id=nxt(), name="Plasma zinc",
    category="trace_minerals", subcategory="essential",
    sample_type="plasma", units="μg/dL", reference_low="70", reference_high="120",
    what_it_measures="Zinc status; cofactor for >300 enzymes",
    low_means="Zinc deficiency; pyroluria; copper-overload secondary",
    interventions_modulates="",
    hypotheses_tests="HYP-0046", clia_status="CLIA")

add(id=nxt(), name="RBC zinc",
    category="trace_minerals", subcategory="essential",
    sample_type="rbc", units="μmol/L",
    interpretation_summary="More sensitive than plasma for cellular zinc status",
    hypotheses_tests="HYP-0046",
    test_availability="specialty_clinical")

add(id=nxt(), name="Plasma copper + ceruloplasmin",
    category="trace_minerals", subcategory="essential",
    sample_type="serum", units="μg/dL",
    what_it_measures="Copper status; free vs ceruloplasmin-bound",
    elevated_means="Copper overload; Walsh framework biotype",
    hypotheses_tests="HYP-0046", clia_status="CLIA",
    notes="Per Walsh William framework. Free copper > 25% of total = overload.")

add(id=nxt(), name="Cu:Zn ratio",
    category="trace_minerals", subcategory="balance",
    sample_type="plasma", units="ratio",
    reference_low="0.7", reference_high="1.0",
    what_it_measures="Copper-to-zinc balance; key Walsh biotype indicator",
    elevated_means="Copper overload phenotype; hyperactivity, sensory issues",
    hypotheses_tests="HYP-0046",
    notes="Per Walsh framework.")

add(id=nxt(), name="RBC magnesium",
    category="trace_minerals", subcategory="essential",
    sample_type="rbc", units="mg/dL",
    interpretation_summary="More sensitive than serum Mg (which is tightly regulated)",
    hypotheses_tests="HYP-0047",
    test_availability="specialty_clinical")

add(id=nxt(), name="Urinary iodine",
    category="trace_minerals", subcategory="essential",
    sample_type="urine_24h_or_spot", units="μg/L",
    reference_low="100", reference_high="300",
    what_it_measures="Iodine status; thyroid function precursor",
    low_means="Iodine deficiency; thyroid hypofunction risk",
    mechanisms_indicated="MEC-0016",
    hypotheses_tests="HYP-0048",
    clia_status="CLIA")

add(id=nxt(), name="Selenium",
    category="trace_minerals", subcategory="essential",
    sample_type="serum_or_rbc", units="μg/L",
    what_it_measures="Selenium status; glutathione peroxidase cofactor",
    hypotheses_tests="HYP-0049",
    clia_status="CLIA")

add(id=nxt(), name="Ferritin",
    category="trace_minerals", subcategory="iron_storage",
    sample_type="serum", units="ng/mL",
    reference_low="30", reference_high="200",
    what_it_measures="Iron storage; common deficiency in autistic kids",
    low_means="Iron deficiency without anemia; common in restricted-diet ASD",
    hypotheses_tests="HYP-0052", clia_status="CLIA")

# ────────────────────────────────────────────────────────────
# CATEGORY 14: PYROLURIA
# ────────────────────────────────────────────────────────────
add(id=nxt(), name="Urinary kryptopyrroles",
    category="pyroluria", subcategory="diagnostic",
    sample_type="urine", units="μg/dL",
    reference_high="20",
    what_it_measures="Kryptopyrroles bind/deplete B6 + zinc",
    elevated_means="Pyroluria phenotype; B6 + zinc + GLA + magnesium protocol",
    interpretation_summary="Sample handling matters — light-sensitive; freeze immediately",
    interventions_modulates="",
    hypotheses_tests="HYP-0046",
    test_availability="specialty",
    lab_options="Direct Healthcare, ALCAT, Bio-Center Labs",
    notes="Per Walsh framework + Pfeiffer Treatment Center historical work.")

# ────────────────────────────────────────────────────────────
# CATEGORY 15: FATTY ACID STATUS
# ────────────────────────────────────────────────────────────
add(id=nxt(), name="RBC omega-3 index (EPA + DHA)",
    category="fatty_acids", subcategory="essential",
    sample_type="rbc", units="% of total fatty acids",
    reference_low="8", reference_optimal_low="8",
    what_it_measures="Long-term omega-3 status",
    low_means="Omega-3 insufficiency; supplementation indicated",
    mechanisms_indicated="MEC-0031",
    hypotheses_tests="HYP-0021,HYP-0064",
    interventions_modulates="",
    test_availability="specialty",
    lab_options="OmegaQuant, Quest")

add(id=nxt(), name="Omega-6/omega-3 ratio",
    category="fatty_acids", subcategory="balance",
    sample_type="rbc", units="ratio",
    reference_optimal_low="2", reference_optimal_high="4",
    what_it_measures="Pro-/anti-inflammatory fatty acid balance",
    elevated_means="Pro-inflammatory diet; modern Western >15:1",
    mechanisms_indicated="MEC-0002,MEC-0031",
    hypotheses_tests="HYP-0021")

add(id=nxt(), name="Trans-fatty acid fraction",
    category="fatty_acids", subcategory="adverse",
    sample_type="rbc", units="% of total",
    elevated_means="Industrial trans-fat exposure; mostly historical now")

add(id=nxt(), name="Mead acid (essential FA deficiency marker)",
    category="fatty_acids", subcategory="deficiency_indicator",
    sample_type="rbc", units="%",
    elevated_means="Essential fatty acid deficiency; severe restricted-diet ASD")

# ────────────────────────────────────────────────────────────
# CATEGORY 16: GI / BARRIER FUNCTION
# ────────────────────────────────────────────────────────────
add(id=nxt(), name="Zonulin",
    category="gi_barrier", subcategory="permeability_marker",
    sample_type="serum_or_stool", units="ng/mL",
    what_it_measures="Tight-junction regulator; intestinal permeability marker",
    elevated_means="Increased intestinal permeability; 'leaky gut'",
    mechanisms_indicated="MEC-0008,MEC-0022",
    hypotheses_tests="HYP-0007,HYP-0059",
    test_availability="specialty",
    lab_options="Doctor's Data, Genova")

add(id=nxt(), name="Lipopolysaccharide (LPS) / endotoxin",
    category="gi_barrier", subcategory="endotoxemia",
    sample_type="serum", units="EU/mL",
    what_it_measures="Bacterial endotoxin in systemic circulation; barrier breach",
    elevated_means="Translocation of gut bacterial products; metabolic endotoxemia",
    mechanisms_indicated="MEC-0008,MEC-0022",
    hypotheses_tests="HYP-0059",
    test_availability="specialty_research")

add(id=nxt(), name="Calprotectin (fecal)",
    category="gi_barrier", subcategory="gi_inflammation",
    sample_type="stool", units="μg/g",
    reference_high="50",
    what_it_measures="Neutrophilic gut inflammation; elevated in IBD + chronic GI inflammation",
    elevated_means="Active GI inflammation; targeted GI workup indicated",
    mechanisms_indicated="MEC-0008",
    hypotheses_tests="HYP-0007", clia_status="CLIA",
    test_availability="standard_clinical")

add(id=nxt(), name="Secretory IgA (sIgA)",
    category="gi_barrier", subcategory="mucosal_immunity",
    sample_type="stool_or_saliva", units="mg/dL",
    what_it_measures="Mucosal immune defense capacity",
    low_means="Compromised mucosal immunity",
    elevated_means="Active mucosal immune challenge",
    mechanisms_indicated="MEC-0008", lab_options="Doctor's Data")

add(id=nxt(), name="Lactulose:mannitol ratio",
    category="gi_barrier", subcategory="permeability_test",
    sample_type="urine_post_challenge", units="ratio",
    what_it_measures="Functional intestinal permeability test (gold standard)",
    elevated_means="Increased permeability; leaky gut confirmed",
    mechanisms_indicated="MEC-0008,MEC-0022",
    hypotheses_tests="HYP-0059",
    test_availability="specialty",
    lab_options="Genova")

# ────────────────────────────────────────────────────────────
# CATEGORY 17: ENDOCRINE / HORMONAL
# ────────────────────────────────────────────────────────────
add(id=nxt(), name="Full thyroid panel (TSH, FT3, FT4, rT3, TPO, TgAb)",
    category="endocrine", subcategory="thyroid",
    sample_type="serum", units="composite",
    what_it_measures="Comprehensive thyroid function + autoimmunity",
    interpretation_summary="Standard pediatric thyroid panel often misses subclinical hypothyroidism",
    mechanisms_indicated="MEC-0016",
    hypotheses_tests="HYP-0035,HYP-0048",
    clia_status="CLIA")

add(id=nxt(), name="DUTCH cortisol (4-point + free + total)",
    category="endocrine", subcategory="hpa_axis",
    sample_type="urine_dried", units="ng/mg creatinine composite",
    what_it_measures="Comprehensive HPA axis function — diurnal rhythm + total + free cortisol",
    interpretation_summary="Per Precision Analytical DUTCH panel; reveals patterns serum cortisol misses",
    mechanisms_indicated="MEC-0016",
    hypotheses_tests="HYP-0036,HYP-0037",
    test_availability="specialty",
    lab_options="Precision Analytical (DUTCH)")

add(id=nxt(), name="DHEA-S",
    category="endocrine", subcategory="steroid",
    sample_type="serum", units="μg/dL",
    what_it_measures="Adrenal androgen precursor; HPA reserve",
    mechanisms_indicated="MEC-0016", clia_status="CLIA")

add(id=nxt(), name="Sex hormones (estradiol, progesterone, testosterone — DUTCH metabolites)",
    category="endocrine", subcategory="sex_hormones",
    sample_type="urine_dried", units="composite",
    what_it_measures="Sex hormone status + metabolism patterns",
    interpretation_summary="Particularly relevant in adolescent ASD presentations",
    mechanisms_indicated="MEC-0016",
    test_availability="specialty",
    lab_options="DUTCH")

add(id=nxt(), name="Vasopressin (AVP)",
    category="endocrine", subcategory="neuropeptide",
    sample_type="serum_or_csf", units="pg/mL",
    what_it_measures="Vasopressin neuropeptide; social bonding mechanism",
    interpretation_summary="Research-grade; complementary to oxytocin; Carter framework",
    mechanisms_indicated="",
    hypotheses_tests="HYP-0034",
    test_availability="research")

add(id=nxt(), name="Oxytocin",
    category="endocrine", subcategory="neuropeptide",
    sample_type="plasma_or_csf", units="pg/mL",
    what_it_measures="Oxytocin neuropeptide; social cognition mechanism",
    mechanisms_indicated="",
    hypotheses_tests="HYP-0034",
    interventions_modulates="INT-0061",
    test_availability="research_specialty")

add(id=nxt(), name="Melatonin (saliva or urinary 6-sulfatoxymelatonin)",
    category="endocrine", subcategory="circadian",
    sample_type="saliva_4_point_or_urine", units="pg/mL or μg/24h",
    what_it_measures="Circadian melatonin pattern; sleep-onset capability",
    low_means="Melatonin deficiency; supplementation candidate",
    interpretation_summary="ASD frequently shows blunted melatonin rise",
    mechanisms_indicated="",
    hypotheses_tests="HYP-0039",
    test_availability="specialty",
    lab_options="DUTCH, Genova")

add(id=nxt(), name="Insulin / HOMA-IR",
    category="endocrine", subcategory="insulin_resistance",
    sample_type="serum", units="μIU/mL + ratio",
    what_it_measures="Insulin sensitivity; metabolic dysfunction marker",
    elevated_means="Insulin resistance; emerging autism / metabolic overlap",
    mechanisms_indicated="MEC-0011,MEC-0012",
    hypotheses_tests="HYP-0018,HYP-0019",
    interventions_modulates="INT-0037",
    clia_status="CLIA")

add(id=nxt(), name="IGF-1 + IGFBP-3",
    category="endocrine", subcategory="growth_factor",
    sample_type="serum", units="ng/mL",
    what_it_measures="Insulin-like growth factor axis; growth + neurodevelopment",
    mechanisms_indicated="MEC-0012",
    hypotheses_tests="HYP-0032",
    interventions_modulates="",
    clia_status="CLIA")

# ────────────────────────────────────────────────────────────
# CATEGORY 18: CHRONIC INFECTION PANEL
# ────────────────────────────────────────────────────────────
add(id=nxt(), name="Mycoplasma pneumoniae IgM/IgG",
    category="chronic_infection", subcategory="bacterial",
    sample_type="serum", units="titer",
    what_it_measures="Mycoplasma infection — frequent PANS trigger",
    hypotheses_tests="HYP-0026", clia_status="CLIA")

add(id=nxt(), name="Borrelia burgdorferi (Lyme) panel",
    category="chronic_infection", subcategory="tick_borne",
    sample_type="serum", units="titer + Western blot",
    what_it_measures="Lyme disease antibodies",
    interpretation_summary="ELISA + Western blot; igenex preferred for chronic suspicion",
    hypotheses_tests="HYP-0026",
    lab_options="Igenex, Quest")

add(id=nxt(), name="Babesia + Bartonella (tick-borne co-infections)",
    category="chronic_infection", subcategory="tick_borne",
    sample_type="serum", units="titer",
    what_it_measures="Lyme co-infection panel",
    lab_options="Igenex")

add(id=nxt(), name="HHV-6 IgG/IgM + PCR",
    category="chronic_infection", subcategory="herpesvirus",
    sample_type="serum_plasma", units="titer + viral load",
    what_it_measures="HHV-6 infection / reactivation status",
    elevated_means="Active or reactivated HHV-6 — emerging neuroimmune relevance",
    hypotheses_tests="HYP-0026,HYP-0008",
    test_availability="specialty",
    lab_options="ARUP, Quest")

add(id=nxt(), name="EBV panel (VCA-IgG, VCA-IgM, EA, EBNA)",
    category="chronic_infection", subcategory="herpesvirus",
    sample_type="serum", units="titer",
    what_it_measures="Epstein-Barr Virus infection stage",
    interpretation_summary="EA elevation suggests reactivation; pattern more informative than single titer",
    clia_status="CLIA")

add(id=nxt(), name="CMV IgG/IgM",
    category="chronic_infection", subcategory="herpesvirus",
    sample_type="serum", units="titer",
    interpretation_summary="Congenital CMV is a recognized cause of neurodevelopmental issues",
    hypotheses_tests="HYP-0025",
    clia_status="CLIA")

add(id=nxt(), name="Toxoplasma IgG/IgM",
    category="chronic_infection", subcategory="parasite",
    sample_type="serum", units="titer",
    interpretation_summary="Maternal toxoplasmosis is a TORCH-class infection cause",
    hypotheses_tests="HYP-0025",
    clia_status="CLIA")

add(id=nxt(), name="Rubella IgG (immune status / maternal exposure history)",
    category="chronic_infection", subcategory="immune_status",
    sample_type="serum", units="IU/mL",
    interpretation_summary="Maternal congenital rubella syndrome is the classical environmental ASD cause",
    hypotheses_tests="HYP-0025",
    clia_status="CLIA")

add(id=nxt(), name="C. difficile toxin (stool)",
    category="chronic_infection", subcategory="gi_pathogen",
    sample_type="stool", units="positive/negative + toxin",
    what_it_measures="C. difficile colonization / active infection",
    mechanisms_indicated="MEC-0008",
    hypotheses_tests="HYP-0007,HYP-0057",
    interventions_modulates="INT-0076", clia_status="CLIA")

add(id=nxt(), name="Candida IgG + IgA",
    category="chronic_infection", subcategory="fungal",
    sample_type="serum", units="EU/mL",
    what_it_measures="Systemic fungal exposure / colonization",
    interpretation_summary="Best paired with urinary arabinose for Candida picture",
    mechanisms_indicated="MEC-0008",
    hypotheses_tests="HYP-0061")

# ────────────────────────────────────────────────────────────
# CATEGORY 19: AUTOIMMUNE BROADER
# ────────────────────────────────────────────────────────────
add(id=nxt(), name="ANA + extractable nuclear antigens",
    category="autoimmune", subcategory="systemic",
    sample_type="serum", units="titer + pattern",
    what_it_measures="Anti-nuclear antibodies; systemic autoimmunity screen",
    mechanisms_indicated="MEC-0002",
    hypotheses_tests="HYP-0051", clia_status="CLIA")

add(id=nxt(), name="Anti-tTG IgA + Anti-DGP IgA/IgG",
    category="autoimmune", subcategory="celiac",
    sample_type="serum", units="U/mL",
    what_it_measures="Celiac disease autoimmunity (anti-transglutaminase, anti-deamidated gliadin peptides)",
    elevated_means="Celiac disease likely; gluten-free diet medically indicated",
    mechanisms_indicated="MEC-0008,MEC-0022", clia_status="CLIA")

add(id=nxt(), name="Thyroid antibodies (TPO + Tg)",
    category="autoimmune", subcategory="thyroid",
    sample_type="serum", units="IU/mL",
    what_it_measures="Hashimoto's thyroiditis screen",
    elevated_means="Thyroid autoimmunity; often coexists with broader autoimmune profile",
    hypotheses_tests="HYP-0048,HYP-0051", clia_status="CLIA")

add(id=nxt(), name="Anti-cardiolipin / anti-phospholipid",
    category="autoimmune", subcategory="phospholipid",
    sample_type="serum", units="titer",
    what_it_measures="Antiphospholipid syndrome screen; coagulation autoimmunity",
    hypotheses_tests="HYP-0051", clia_status="CLIA")

# ────────────────────────────────────────────────────────────
# CATEGORY 20: NEUROBIOLOGY / BRAIN BIOMARKERS
# ────────────────────────────────────────────────────────────

# Neuroimaging
add(id=nxt(), name="MRI cortical thickness (region-specific)",
    category="brain_neuroimaging", subcategory="structural_mri",
    sample_type="mri_imaging", units="mm",
    what_it_measures="Cortical thickness in autism-relevant regions (STS, fusiform face area, prefrontal)",
    interpretation_summary="ASD shows region-specific thickness alterations; not yet clinically diagnostic but research-anchor",
    mechanisms_indicated="MEC-0006",
    hypotheses_tests="HYP-0073",
    test_availability="research")

add(id=nxt(), name="Total brain volume / amygdala / cerebellar vermis volumetry",
    category="brain_neuroimaging", subcategory="structural_mri",
    sample_type="mri_imaging", units="mm³",
    what_it_measures="Volumetric MRI abnormalities — early brain overgrowth + amygdala enlargement classical findings",
    interpretation_summary="Courchesne early brain overgrowth framework; cerebellar vermis hypoplasia in some",
    mechanisms_indicated="MEC-0006",
    hypotheses_tests="HYP-0071,HYP-0073",
    test_availability="research")

add(id=nxt(), name="DTI fractional anisotropy (white matter tracts)",
    category="brain_neuroimaging", subcategory="white_matter",
    sample_type="dti_mri", units="dimensionless",
    what_it_measures="White matter integrity; corpus callosum + arcuate fasciculus + cingulum changes",
    interpretation_summary="Reduced FA in long-range tracts; underlying connectivity-disorder hypothesis",
    mechanisms_indicated="MEC-0006",
    hypotheses_tests="HYP-0073",
    test_availability="research")

add(id=nxt(), name="Resting-state fMRI default mode network connectivity",
    category="brain_neuroimaging", subcategory="functional_mri",
    sample_type="fmri", units="connectivity z-score",
    what_it_measures="DMN functional connectivity; ASD shows local hyperconnectivity + long-distance hypoconnectivity",
    mechanisms_indicated="MEC-0006",
    hypotheses_tests="HYP-0073",
    test_availability="research")

add(id=nxt(), name="1H-MRS NAA / choline / creatine / glutamate-GABA",
    category="brain_neuroimaging", subcategory="spectroscopy",
    sample_type="mrs", units="ratio + concentrations",
    what_it_measures="In-vivo brain neurochemistry — neuronal viability (NAA), membrane turnover (Cho), energy buffer (Cr), excit/inhib balance",
    interpretation_summary="Reduced NAA in ASD; elevated glutamate/GABA ratio in some regions",
    mechanisms_indicated="MEC-0007,MEC-0010,MEC-0020",
    hypotheses_tests="HYP-0006,HYP-0071",
    test_availability="research")

add(id=nxt(), name="PET-TSPO (translocator protein — microglial activation)",
    category="brain_neuroimaging", subcategory="pet",
    sample_type="pet_imaging", units="binding potential",
    what_it_measures="In-vivo microglial activation — neuroinflammation imaging",
    elevated_means="Active neuroinflammation; emerging biomarker for inflammatory ASD subgroup",
    mechanisms_indicated="MEC-0002,MEC-0005",
    hypotheses_tests="HYP-0008",
    test_availability="research_only",
    notes="Cutting-edge; will become clinically actionable as PET-TSPO ligands mature.")

# Electrophysiology
add(id=nxt(), name="EEG resting-state spectral power (gamma/beta/alpha)",
    category="brain_electrophysiology", subcategory="resting_eeg",
    sample_type="eeg", units="power spectral density",
    what_it_measures="Resting-state EEG power; ASD shows characteristic gamma-band abnormalities",
    interpretation_summary="Gamma-band abnormalities reflect cortical excitation/inhibition imbalance",
    mechanisms_indicated="MEC-0007,MEC-0020",
    hypotheses_tests="HYP-0071",
    test_availability="specialty_clinical_research")

add(id=nxt(), name="ERP P300 amplitude / latency",
    category="brain_electrophysiology", subcategory="erp",
    sample_type="eeg_evoked", units="μV + ms",
    what_it_measures="Attention / cognitive processing event-related potential",
    interpretation_summary="Reduced P300 amplitude common in ASD; attention/discrimination correlate",
    test_availability="research")

add(id=nxt(), name="ERP MMN (mismatch negativity)",
    category="brain_electrophysiology", subcategory="erp",
    sample_type="eeg_evoked", units="μV + ms",
    what_it_measures="Auditory deviance detection; preconscious sensory processing",
    interpretation_summary="Atypical MMN in ASD; sensory-processing biomarker",
    test_availability="research")

add(id=nxt(), name="ERP N170 (face processing)",
    category="brain_electrophysiology", subcategory="erp",
    sample_type="eeg_evoked", units="μV + ms",
    what_it_measures="Face-specific occipitotemporal response; social-cognition correlate",
    interpretation_summary="Atypical N170 in ASD; social-information processing biomarker",
    test_availability="research")

add(id=nxt(), name="qEEG coherence pattern",
    category="brain_electrophysiology", subcategory="qeeg",
    sample_type="eeg", units="coherence + asymmetry pattern",
    what_it_measures="Quantitative EEG connectivity patterns",
    interpretation_summary="Characteristic ASD coherence patterns; some clinical neurofeedback application",
    test_availability="specialty_clinical")

# Eye-tracking + autonomic
add(id=nxt(), name="Gaze fixation pattern (eye-tracking)",
    category="brain_eye_autonomic", subcategory="eye_tracking",
    sample_type="eye_tracking", units="dwell time + pattern",
    what_it_measures="Atypical face/eye fixation patterns characteristic of ASD",
    interpretation_summary="Pelphrey/Klin framework; reduced eye-region fixation",
    test_availability="research_specialty",
    notes="Increasingly available in specialized clinics. EarliPoint and other commercial platforms emerging.")

add(id=nxt(), name="Pupillometry / pupil response",
    category="brain_eye_autonomic", subcategory="autonomic",
    sample_type="eye_tracking", units="pupil diameter dynamics",
    what_it_measures="Autonomic readout via pupil dynamics",
    interpretation_summary="Atypical pupil light response and task-evoked dilation in ASD",
    test_availability="research")

add(id=nxt(), name="Heart rate variability (HRV)",
    category="brain_eye_autonomic", subcategory="autonomic",
    sample_type="ecg", units="rMSSD + SDNN + HF/LF",
    what_it_measures="Vagal tone / autonomic regulation",
    low_means="Reduced parasympathetic regulation; dysautonomia common in ASD + MCAS overlap",
    interpretation_summary="Polyvagal framework; many wearable devices measure (Polar, Whoop, Oura)",
    mechanisms_indicated="MEC-0019",
    test_availability="commercial_wearable_or_clinical")

# CSF (when measured)
add(id=nxt(), name="CSF cytokines",
    category="brain_csf", subcategory="csf_inflammation",
    sample_type="csf", units="pg/mL composite",
    what_it_measures="Direct CNS cytokine measurement (IL-6, TNF-α, IL-1β, others)",
    interpretation_summary="Invasive but most direct neuroinflammation measure",
    mechanisms_indicated="MEC-0002,MEC-0005",
    hypotheses_tests="HYP-0008",
    test_availability="research_or_clinical_indication")

add(id=nxt(), name="CSF tau / NfL",
    category="brain_csf", subcategory="neuronal_injury",
    sample_type="csf", units="pg/mL",
    what_it_measures="Neuronal injury markers — emerging in autism research",
    interpretation_summary="Rare in autism; may be relevant in regressive subgroup",
    test_availability="research_clinical")

# Brain-derived peripheral
add(id=nxt(), name="Serum BDNF (brain-derived neurotrophic factor)",
    category="brain_peripheral", subcategory="neurotrophic",
    sample_type="serum", units="ng/mL",
    what_it_measures="Neurotrophin reflecting CNS plasticity / neurogenesis",
    interpretation_summary="Mixed findings in ASD — both elevated and reduced reported in subgroups",
    mechanisms_indicated="",
    hypotheses_tests="HYP-0073",
    test_availability="specialty_research")

add(id=nxt(), name="Serum S100β (astrocyte marker / BBB disruption)",
    category="brain_peripheral", subcategory="astrocyte",
    sample_type="serum", units="μg/L",
    what_it_measures="Astrocyte injury / BBB permeability marker",
    elevated_means="BBB disruption; emerging neuroinflammation biomarker",
    mechanisms_indicated="MEC-0004,MEC-0005",
    hypotheses_tests="HYP-0008", clia_status="CLIA",
    test_availability="specialty_research")

add(id=nxt(), name="Serum GFAP (glial fibrillary acidic protein)",
    category="brain_peripheral", subcategory="astrocyte",
    sample_type="serum", units="pg/mL",
    what_it_measures="Astrocyte activation marker; elevated in many neurological conditions",
    mechanisms_indicated="MEC-0005",
    test_availability="research_to_specialty")

add(id=nxt(), name="Serum neurofilament light chain (NfL)",
    category="brain_peripheral", subcategory="neuronal_injury",
    sample_type="serum", units="pg/mL",
    what_it_measures="Axonal damage marker — emerging biomarker of CNS neuronal injury",
    interpretation_summary="Rising clinical use; emerging in pediatric neurodevelopmental contexts",
    test_availability="specialty_research")

add(id=nxt(), name="Serum tau",
    category="brain_peripheral", subcategory="neuronal_injury",
    sample_type="serum", units="pg/mL",
    what_it_measures="Neuronal microtubule-associated protein; neurodegeneration marker",
    interpretation_summary="Limited but emerging autism-relevance",
    test_availability="research")

# ────────────────────────────────────────────────────────────
# CATEGORY 21: HEAT SHOCK / FEVER EFFECT
# ────────────────────────────────────────────────────────────
add(id=nxt(), name="HSP70 / HSP90 plasma levels",
    category="heat_shock", subcategory="stress_response",
    sample_type="plasma", units="ng/mL",
    what_it_measures="Heat shock protein induction; cellular stress response capacity",
    interpretation_summary="Per Curran fever-effect framework; HSP70 induction may underlie 'fever improves autism' subgroup",
    mechanisms_indicated="MEC-0027",
    hypotheses_tests="HYP-0065",
    test_availability="research")

# ────────────────────────────────────────────────────────────
# CATEGORY 22: ENDOCANNABINOID
# ────────────────────────────────────────────────────────────
add(id=nxt(), name="Anandamide (AEA)",
    category="endocannabinoid", subcategory="endocannabinoid",
    sample_type="plasma", units="pmol/mL",
    what_it_measures="Primary endocannabinoid; CB1/CB2 receptor agonist",
    mechanisms_indicated="MEC-0018",
    hypotheses_tests="HYP-0055",
    test_availability="research")

add(id=nxt(), name="2-arachidonoylglycerol (2-AG)",
    category="endocannabinoid", subcategory="endocannabinoid",
    sample_type="plasma", units="pmol/mL",
    what_it_measures="Major endocannabinoid; full CB1/CB2 agonist",
    mechanisms_indicated="MEC-0018",
    hypotheses_tests="HYP-0055",
    test_availability="research")

# ────────────────────────────────────────────────────────────
# CATEGORY 23: METHYLATION-CYCLE GENETIC SNPS (overlap with genes layer)
# ────────────────────────────────────────────────────────────
add(id=nxt(), name="MTHFR C677T genotype",
    category="genetic_snp", subcategory="methylation_genetic",
    sample_type="buccal_or_blood", units="genotype (CC/CT/TT)",
    what_it_measures="C677T variant — affects 5-MTHF activation efficiency",
    interpretation_summary="TT homozygous: 70% reduction in MTHFR activity; needs methylated folate not folic acid",
    snp_dependence="self",
    mechanisms_indicated="MEC-0003",
    hypotheses_tests="HYP-0001,HYP-0003",
    interventions_modulates="INT-0008",
    test_availability="commercial_dtc",
    lab_options="23andMe, Quest, LabCorp")

add(id=nxt(), name="MTHFR A1298C genotype",
    category="genetic_snp", subcategory="methylation_genetic",
    sample_type="buccal_or_blood", units="genotype (AA/AC/CC)",
    what_it_measures="A1298C variant — affects MTHFR activity differently than C677T",
    snp_dependence="self",
    mechanisms_indicated="MEC-0003",
    hypotheses_tests="HYP-0001",
    test_availability="commercial_dtc")

add(id=nxt(), name="COMT V158M (Val/Met) genotype",
    category="genetic_snp", subcategory="catecholamine_genetic",
    sample_type="buccal_or_blood", units="genotype (Val/Val, Val/Met, Met/Met)",
    what_it_measures="Catechol-O-methyltransferase variant — affects dopamine breakdown",
    interpretation_summary="Met/Met = slow COMT, more sensitive to methyl donors; affects stimulant + SSRI response",
    snp_dependence="self",
    mechanisms_indicated="MEC-0003,MEC-0007",
    test_availability="commercial_dtc")

add(id=nxt(), name="CBS upregulation variants",
    category="genetic_snp", subcategory="transsulfuration_genetic",
    sample_type="buccal_or_blood", units="genotype",
    what_it_measures="Cystathionine beta-synthase upregulators — accelerate transsulfuration",
    snp_dependence="self",
    mechanisms_indicated="MEC-0003")

# ────────────────────────────────────────────────────────────
# Final sanity print
# ────────────────────────────────────────────────────────────
print(f"Defined {len(B)} biomarkers across {len(set(b['category'] for b in B))} categories")

# ============================================================
# Build edge tables (BME, BPE, BIE, BHE) from biomarker entries
# ============================================================
BME = []  # biomarker_mechanism_edges
BPE = []  # biomarker_phenotype_edges
BIE = []  # biomarker_intervention_edges
BHE = []  # biomarker_hypothesis_edges

bme_id = 1; bpe_id = 1; bie_id = 1; bhe_id = 1

for b in B:
    for m in (b.get("mechanisms_indicated") or "").split(","):
        m = m.strip()
        if not m: continue
        BME.append({
            "id": f"BME-{bme_id:05d}",
            "biomarker_id": b["id"], "mechanism_id": m,
            "relationship_type": "indicates_dysfunction",
            "evidence_strength": "0.50", "polarity": "supporting",
            "created_at": NOW, "notes": f"{b['name']} indicates {m}"
        }); bme_id += 1
    for p in (b.get("phenotypes_stratified") or "").split(","):
        p = p.strip()
        if not p: continue
        BPE.append({
            "id": f"BPE-{bpe_id:05d}",
            "biomarker_id": b["id"], "phenotype_id": p,
            "relationship_type": "stratifies",
            "evidence_strength": "0.55",
            "created_at": NOW, "notes": f"{b['name']} stratifies {p}"
        }); bpe_id += 1
    for it in (b.get("interventions_modulates") or "").split(","):
        it = it.strip()
        if not it: continue
        BIE.append({
            "id": f"BIE-{bie_id:05d}",
            "biomarker_id": b["id"], "intervention_id": it,
            "relationship_type": "predicts_response",
            "direction": "normalize", "evidence_strength": "0.50",
            "created_at": NOW, "notes": f"{b['name']} predicts response to {it}"
        }); bie_id += 1
    for h in (b.get("hypotheses_tests") or "").split(","):
        h = h.strip()
        if not h: continue
        BHE.append({
            "id": f"BHE-{bhe_id:05d}",
            "biomarker_id": b["id"], "hypothesis_id": h,
            "relationship_type": "tests",
            "evidence_strength": "0.50",
            "created_at": NOW, "notes": f"{b['name']} tests {h}"
        }); bhe_id += 1

print(f"Edge tables: BME={len(BME)}, BPE={len(BPE)}, BIE={len(BIE)}, BHE={len(BHE)}")

# ============================================================
# Write CSVs
# ============================================================
def write_csv(path, fields, rows):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})

EDGE_FIELDS = {
    "BME": ["id","biomarker_id","mechanism_id","relationship_type","evidence_strength","polarity","created_at","notes"],
    "BPE": ["id","biomarker_id","phenotype_id","relationship_type","evidence_strength","created_at","notes"],
    "BIE": ["id","biomarker_id","intervention_id","relationship_type","direction","evidence_strength","created_at","notes"],
    "BHE": ["id","biomarker_id","hypothesis_id","relationship_type","evidence_strength","created_at","notes"],
}

for d in [ROOT/"v2.0_scored", ROOT/"v2.0.1_expanded"]:
    write_csv(d/"biomarkers.csv", BIOMARKER_FIELDS, B)
    write_csv(d/"biomarker_mechanism_edges.csv", EDGE_FIELDS["BME"], BME)
    write_csv(d/"biomarker_phenotype_edges.csv", EDGE_FIELDS["BPE"], BPE)
    write_csv(d/"biomarker_intervention_edges.csv", EDGE_FIELDS["BIE"], BIE)
    write_csv(d/"biomarker_hypothesis_edges.csv", EDGE_FIELDS["BHE"], BHE)
    print(f"  {d.name}/: wrote biomarkers + 4 edge tables")

print(f"\nDone. Biomarker layer ingested.")
