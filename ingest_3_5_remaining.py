#!/usr/bin/env python3
"""Session 3.5 remaining — atlas entity additions.

3.5C — 2 new HYPs (PANS/PANDAS + MCAS)
3.5D — 4 new PHEs (Walsh biotypes: undermethylator, overmethylator, pyroluria, Cu:Zn imbalance)
3.5B — ~35 new INTs (functional medicine expansion)
3.5E — new protocols.csv entity type (Walsh, Frye, Yasko, Neubrander, Bock, Klinghardt, MAPS, ARI)

All wired to existing entities. Calibration-non-disruptive
(adds parallel evidence/edges, doesn't change INT-0001 pathway scores).
"""
import csv, datetime as dt, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NOW = dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')

# ============================================================
# 3.5C — Two new hypothesis families
# ============================================================
new_hyps = [
    {
        "id": "HYP-0074",
        "name": "PANS/PANDAS — post-infectious autoimmune neuropsychiatric syndrome",
        "category": "immune_autoimmune",
        "description": "Pediatric Acute-onset Neuropsychiatric Syndrome (PANS) / Pediatric Autoimmune Neuropsychiatric Disorders Associated with Streptococcus (PANDAS) — a real, identifiable autoimmune subgroup of children whose neuropsychiatric symptoms (often labeled regressive autism) are post-infectious and immunologically driven. Anti-neuronal antibodies cross-reacting with basal ganglia (anti-tubulin, anti-lysoganglioside, anti-D1/D2, CaMKII activation). Per Swedo / Cunningham framework. Treatable via NSAIDs, antibiotics, IVIG, plasmapheresis, LDN.",
        "affected_population": "Pediatric, sudden-onset OCD/tics/anxiety/sensory regression; typically post-strep, mycoplasma, Lyme, viral infection",
        "status": "active",
        "confidence_score": "0.65",
        "evidence_count": "0",
        "evidence_quality_index": "0",
        "consistency_index": "0",
        "created_at": NOW, "last_updated": NOW,
        "notes": "Diagnostic via Cunningham Panel + clinical course + infection history. Per Swedo (NIMH) + Cunningham (OUHSC) frameworks. Researchers: Swedo_Sue, Cunningham_Madeleine.",
    },
    {
        "id": "HYP-0075",
        "name": "Mast Cell Activation Syndrome (MCAS) in autism",
        "category": "immune_autoimmune",
        "description": "Mast cell hyperactivity affecting GI, autonomic, dermatologic, and neuroinflammatory systems in a substantial autism subgroup. Per Theoharides framework: mast cells + microglia coupling drives autism-relevant neuroinflammation. Diagnostic via tryptase + N-methylhistamine + PGD2 metabolite + chromogranin A. Treatable via H1+H2 antihistamines, cromolyn, ketotifen, luteolin, quercetin.",
        "affected_population": "Children with chronic atopic disease, GI dysmotility, dysautonomia, flushing, behavioral worsening with mast-cell triggers",
        "status": "active",
        "confidence_score": "0.60",
        "evidence_count": "0",
        "evidence_quality_index": "0",
        "consistency_index": "0",
        "created_at": NOW, "last_updated": NOW,
        "notes": "Per Theoharides framework; mast cells release >200 mediators including histamine, tryptase, IL-6, TNF-α. Researcher: Theoharides_Theoharis.",
    },
]

# ============================================================
# 3.5D — Walsh biotype phenotype refinement (4 new PHEs)
# ============================================================
new_phes = [
    {
        "id": "PHE-0008",
        "name": "Undermethylator phenotype (Walsh)",
        "description": "Low whole-blood histamine, low SAM/SAH ratio. Personality cluster: high inner tension, perfectionism, OCD features, seasonal allergies. ~30-40% of autism per Walsh framework. Treatment: methyl donors (methionine, SAM-e, methyl-B12, sometimes 5-MTHF cautiously).",
        "diagnostic_markers": "Low whole-blood histamine; low SAM/SAH ratio; clinical personality cluster",
        "prevalence_estimate": "30-40% of autism",
        "status": "active",
        "created_at": NOW, "last_updated": NOW,
        "notes": "Per Walsh Research Institute framework. Researcher: Walsh_William.",
    },
    {
        "id": "PHE-0009",
        "name": "Overmethylator phenotype (Walsh)",
        "description": "High whole-blood histamine, high SAM/SAH ratio. Personality cluster: anxious, low motivation, paradoxical histamine elevation. ~5-10% of autism per Walsh. Treatment: folate-cautious; niacinamide, B6, sometimes folate-blocking strategies.",
        "diagnostic_markers": "High whole-blood histamine; high SAM/SAH ratio",
        "prevalence_estimate": "5-10% of autism",
        "status": "active",
        "created_at": NOW, "last_updated": NOW,
        "notes": "Per Walsh framework. Methyl donors can paradoxically worsen.",
    },
    {
        "id": "PHE-0010",
        "name": "Pyroluria / kryptopyrroluria phenotype",
        "description": "Elevated urinary kryptopyrroles which bind and deplete B6 + zinc. Stress intolerance, anxiety, mood lability, poor short-term memory, peculiar fruity-smelling sweat under stress. Treatment: B6 (P5P), zinc, GLA (evening primrose oil), magnesium.",
        "diagnostic_markers": "Elevated urinary kryptopyrroles (>20 μg/dL); clinical stress-reactivity profile",
        "prevalence_estimate": "10-20% of autism",
        "status": "active",
        "created_at": NOW, "last_updated": NOW,
        "notes": "Per Walsh / Pfeiffer Treatment Center historical work. Sample handling matters — light-sensitive.",
    },
    {
        "id": "PHE-0011",
        "name": "Copper:zinc imbalance phenotype",
        "description": "Elevated free copper + low zinc (Cu:Zn >1.2 per Walsh framework). Hyperactivity, sensory issues, behavioral dysregulation. Postpartum depression risk in mothers. Treatment: zinc supplementation, molybdenum, metallothionein-promoting protocols.",
        "diagnostic_markers": "Elevated plasma copper; low plasma zinc; Cu:Zn ratio >1.2",
        "prevalence_estimate": "15-25% of autism, often with hyperactive/aggressive features",
        "status": "active",
        "created_at": NOW, "last_updated": NOW,
        "notes": "Per Walsh framework.",
    },
]

# ============================================================
# 3.5B — Functional medicine intervention expansion
# ============================================================
def mki(idx, name, **kw):
    out = {f: "" for f in [
        "id","name","category","directionality","mechanism_summary","dose_range",
        "cost_per_month_usd","otc_or_rx","pediatric_safe","csrs_score",
        "csrs_last_updated","status","created_at","last_updated","notes",
        "targets_legacy","source_pmids_legacy","source_anecdote_ids_legacy",
        "csrs_score_legacy","csrs_last_updated_legacy",
        "csrs_prevention_score","csrs_prevention_last_updated",
        "csrs_treatment_score","csrs_treatment_last_updated"]}
    out["id"] = f"INT-{idx:04d}"
    out["name"] = name
    out["created_at"] = NOW
    out["last_updated"] = NOW
    out["status"] = "active"
    for k,v in kw.items(): out[k] = v
    return out

next_int = 103  # last existing was INT-0102
new_ints = []

# Mast cell stabilizers + antihistamines (5)
new_ints.extend([
    mki(next_int, "Cromolyn sodium (oral)", category="drug", directionality="treatment",
        mechanism_summary="Mast cell stabilizer; pre-meal for GI mast cell stabilization",
        dose_range="100-200 mg pre-meal QID", otc_or_rx="rx",
        notes="MCAS/PHE-0008 candidate per Theoharides framework"),
    mki(next_int+1, "Ketotifen", category="drug", directionality="treatment",
        mechanism_summary="Combined H1 antihistamine + mast cell stabilizer",
        dose_range="1-4 mg/day", otc_or_rx="rx",
        notes="MCAS protocol; compounded available"),
    mki(next_int+2, "Quercetin", category="supplement", directionality="treatment",
        mechanism_summary="Bioflavonoid mast cell stabilizer; anti-inflammatory",
        dose_range="250-1000 mg twice daily", otc_or_rx="otc",
        notes="MCAS adjunct; well-tolerated"),
    mki(next_int+3, "Luteolin (BBB-crossing formulation)", category="supplement", directionality="treatment",
        mechanism_summary="BBB-crossing bioflavonoid; stabilizes mast cells AND microglia",
        dose_range="50-200 mg/day per formulation", otc_or_rx="otc",
        notes="Per Theoharides framework. NeuroProtek and similar formulations."),
    mki(next_int+4, "H1+H2 antihistamine combination", category="drug", directionality="treatment",
        mechanism_summary="Cetirizine/fexofenadine (H1) + famotidine (H2) — foundational MCAS",
        dose_range="age-appropriate cetirizine 5-10mg + famotidine 0.5mg/kg",
        otc_or_rx="otc",
        notes="Foundational MCAS protocol. Loratadine alternative for daytime."),
])
next_int += 5

# Antifungals (4)
new_ints.extend([
    mki(next_int, "Nystatin (oral non-systemic)", category="drug", directionality="treatment",
        mechanism_summary="Polyene antifungal; non-absorbable; targets gut Candida",
        dose_range="500K-1M units 4x daily", otc_or_rx="rx",
        notes="First-line for elevated arabinose / Candida overgrowth"),
    mki(next_int+1, "Caprylic acid (C8 fatty acid)", category="supplement", directionality="treatment",
        mechanism_summary="Medium-chain fatty acid antifungal",
        dose_range="500-1500 mg with meals", otc_or_rx="otc"),
    mki(next_int+2, "Undecylenic acid", category="supplement", directionality="treatment",
        mechanism_summary="Antifungal; complementary to nystatin",
        dose_range="450-900 mg/day", otc_or_rx="otc"),
    mki(next_int+3, "Biofilm disruptors (lumbrokinase / NAC / lactoferrin)", category="supplement",
        directionality="treatment",
        mechanism_summary="Biofilm-degrading enzymes + chelators; pre-antifungal/antimicrobial",
        dose_range="varies; typical 30-60 min before antimicrobial",
        otc_or_rx="otc"),
])
next_int += 4

# Antimicrobials (3)
new_ints.extend([
    mki(next_int, "Vancomycin (oral, non-absorbable)", category="drug", directionality="treatment",
        mechanism_summary="Targets Clostridia overgrowth; non-systemic",
        dose_range="125-500 mg 4x daily for 10-14 days", otc_or_rx="rx",
        notes="For elevated HPHPA / Clostridia (Sandler 2000 case series)"),
    mki(next_int+1, "Saccharomyces boulardii", category="supplement", directionality="treatment",
        mechanism_summary="Probiotic yeast; targets C. diff + Clostridia",
        dose_range="5-10 billion CFU 2x daily", otc_or_rx="otc"),
    mki(next_int+2, "Berberine", category="supplement", directionality="treatment",
        mechanism_summary="Plant alkaloid; antimicrobial + AMPK activation",
        dose_range="500 mg 2-3x daily", otc_or_rx="otc"),
])
next_int += 3

# Methylation pathway specific (4)
new_ints.extend([
    mki(next_int, "Methyl-B12 (subcutaneous Neubrander protocol)", category="supplement",
        directionality="treatment",
        mechanism_summary="Methylcobalamin SC; bypasses B12 metabolic blocks",
        dose_range="~64.5 mcg/kg every 3 days SC",
        otc_or_rx="rx_compounded",
        notes="Per Neubrander_James protocol. Methylated folate often co-administered."),
    mki(next_int+1, "SAM-e (S-adenosylmethionine)", category="supplement", directionality="treatment",
        mechanism_summary="Direct methyl donor; bypasses cycle defects",
        dose_range="100-400 mg/day (children)", otc_or_rx="otc",
        notes="Undermethylators per Walsh; not for overmethylators or bipolar-spectrum"),
    mki(next_int+2, "Betaine / TMG (trimethylglycine)", category="supplement", directionality="treatment",
        mechanism_summary="BHMT pathway methyl donor; lowers homocysteine",
        dose_range="500-3000 mg/day", otc_or_rx="otc",
        notes="Especially when homocysteine elevated"),
    mki(next_int+3, "N-acetylcysteine (NAC)", category="supplement", directionality="treatment",
        mechanism_summary="Glutathione precursor; antioxidant",
        dose_range="600-2400 mg/day", otc_or_rx="otc",
        notes="Foundational glutathione support"),
])
next_int += 4

# Mitochondrial advanced (4)
new_ints.extend([
    mki(next_int, "PQQ (pyrroloquinoline quinone)", category="supplement", directionality="treatment",
        mechanism_summary="Mitochondrial biogenesis promoter",
        dose_range="10-20 mg/day", otc_or_rx="otc"),
    mki(next_int+1, "MitoQ (mito-targeted CoQ10)", category="supplement", directionality="treatment",
        mechanism_summary="Mitochondria-targeted CoQ10 analog",
        dose_range="10-20 mg/day", otc_or_rx="otc"),
    mki(next_int+2, "NAD+ precursors (NMN/NR)", category="supplement", directionality="treatment",
        mechanism_summary="Boost cellular NAD+; sirtuin pathway support",
        dose_range="250-500 mg/day", otc_or_rx="otc"),
    mki(next_int+3, "Methylene blue (low-dose)", category="drug", directionality="treatment",
        mechanism_summary="Alternative electron carrier; methemoglobin caution",
        dose_range="0.5-2 mg/kg/day low-dose; varies", otc_or_rx="rx",
        notes="Emerging; methemoglobinemia risk; G6PD contraindication"),
])
next_int += 4

# Drug repurposing additions per 3.5F (8)
new_ints.extend([
    mki(next_int, "Bumetanide (NKCC1 inhibitor for autism)", category="drug", directionality="treatment",
        mechanism_summary="NKCC1 inhibitor; forces GABA developmental switch in chloride-imbalance subgroup",
        dose_range="0.5-2 mg/day; potassium monitoring required", otc_or_rx="rx",
        notes="Per Ben-Ari framework; Phase 3 mixed but subgroup-positive."),
    mki(next_int+1, "Suramin (low-dose, antipurinergic)", category="drug", directionality="treatment",
        mechanism_summary="Antipurinergic; Naviaux CDR framework",
        dose_range="20 mg/kg single IV (research dosing)", otc_or_rx="rx_research",
        notes="Naviaux 2017 PMID 28695149 phase I/II; toxicity limits broad use"),
    mki(next_int+2, "Pioglitazone (PPAR-γ agonist)", category="drug", directionality="treatment",
        mechanism_summary="PPAR-γ agonist; anti-inflammatory; insulin-sensitizer",
        dose_range="15-30 mg/day", otc_or_rx="rx",
        notes="Emerging neuroinflammation use; weight gain caution"),
    mki(next_int+3, "Minocycline (microglial modulator)", category="drug", directionality="treatment",
        mechanism_summary="Tetracycline with microglial-modulating activity",
        dose_range="50-100 mg twice daily", otc_or_rx="rx",
        notes="Anti-inflammatory; long-term skin pigmentation caution"),
    mki(next_int+4, "Allopregnanolone / ganaxolone", category="drug", directionality="treatment",
        mechanism_summary="Endogenous neurosteroid; positive GABA-A modulator",
        dose_range="varies; ganaxolone FDA-approved for CDKL5",
        otc_or_rx="rx",
        notes="Calming; emerging research in epileptic ASD"),
    mki(next_int+5, "Trehalose (autophagy promoter)", category="supplement", directionality="treatment",
        mechanism_summary="Disaccharide; promotes autophagy and mitophagy",
        dose_range="5-15 g/day", otc_or_rx="otc"),
    mki(next_int+6, "Lovastatin (low-dose)", category="drug", directionality="treatment",
        mechanism_summary="Statin with FXR / cholesterol effects; preclinical Fragile X work",
        dose_range="contested; not for general autism use",
        otc_or_rx="rx",
        notes="Caution: mitochondrially toxic; CoQ10 depletion"),
    mki(next_int+7, "Valacyclovir / acyclovir (HHV-6/EBV reactivation)", category="drug",
        directionality="treatment",
        mechanism_summary="Antiviral for chronic herpesvirus reactivation",
        dose_range="varies; long-term low-dose suppression",
        otc_or_rx="rx"),
])
next_int += 8

# Peptides per 3.5G (5)
new_ints.extend([
    mki(next_int, "Vasopressin (intranasal)", category="supplement", directionality="treatment",
        mechanism_summary="Neuropeptide; social bonding mechanism (complementary to oxytocin)",
        dose_range="varies; research-grade", otc_or_rx="rx_research"),
    mki(next_int+1, "IGF-1 (mecasermin)", category="drug", directionality="treatment",
        mechanism_summary="Insulin-like growth factor 1; SHANK3-stratified intervention",
        dose_range="varies; FDA-approved for primary IGFD",
        otc_or_rx="rx",
        notes="Per Hollander framework for Phelan-McDermid syndrome; off-label autism"),
    mki(next_int+2, "Antimicrobial peptides (cathelicidin/LL-37)", category="endogenous",
        directionality="treatment",
        mechanism_summary="Endogenous AMP; vitamin-D-driven; first-line innate immunity",
        dose_range="indirect via vitamin D status", otc_or_rx="endogenous"),
    mki(next_int+3, "Humanin (mito-derived peptide)", category="supplement", directionality="treatment",
        mechanism_summary="Mitochondrial 16S-rRNA encoded peptide; anti-apoptotic + neuroprotective",
        dose_range="research-grade", otc_or_rx="research"),
    mki(next_int+4, "MOTS-c (mito-derived peptide)", category="supplement", directionality="treatment",
        mechanism_summary="Mitochondrial 12S-rRNA peptide; metabolic + exercise-mimetic effects",
        dose_range="research-grade", otc_or_rx="research"),
])
next_int += 5

# Hormonal/neurosteroid (2)
new_ints.extend([
    mki(next_int, "Pregnenolone (low-dose)", category="supplement", directionality="treatment",
        mechanism_summary="Master neurosteroid; precursor for cortisol/DHEA/allopregnanolone",
        dose_range="10-30 mg/day", otc_or_rx="otc",
        notes="Use cautiously in children; existing INT-0069 covers"),
    mki(next_int+1, "Vitamin D high-dose (deficiency-correction)", category="supplement",
        directionality="treatment",
        mechanism_summary="Cholecalciferol; immune/serotonin/methylation effects",
        dose_range="2000-5000 IU/day calibrated to 25-OH-D", otc_or_rx="otc",
        notes="Foundational; calibrated to BIO-0165"),
])
next_int += 2

print(f"Adding {len(new_hyps)} HYPs, {len(new_phes)} PHEs, {len(new_ints)} INTs")

# ============================================================
# 3.5E — Named protocols/providers as new entity type
# ============================================================
PROTOCOL_FIELDS = [
    "id","name","provider","origin_year","framework_class","description",
    "test_panel","intervention_stack","target_population",
    "evidence_strength","clinical_availability","cost_estimate",
    "key_researcher_id","key_pmids","created_at","last_updated","notes",
]

protocols = [
    {"id":"PROT-0001","name":"Walsh biotyping protocol","provider":"Walsh Research Institute / Mensah Medical",
     "origin_year":"1970s, refined 2000s","framework_class":"methylation_biotyping",
     "description":"Whole-blood histamine + Cu:Zn + plasma zinc + ceruloplasmin + urinary kryptopyrroles biotype the child into undermethylator/overmethylator/pyroluria/Cu:Zn-overload subtypes; targeted nutrient protocol per biotype",
     "test_panel":"Whole-blood histamine; SAM/SAH; Cu/Zn/Cu:Zn; ceruloplasmin; kryptopyrroles; B6/P5P; methylation SNPs",
     "intervention_stack":"Biotype-specific: methyl donors for under; folate-cautious for over; B6/zinc/GLA for pyroluria; zinc/molybdenum for Cu overload",
     "target_population":"All autistic children with methylation involvement",
     "evidence_strength":"Decades clinical experience; limited large RCTs",
     "clinical_availability":"Mensah Medical (Chicago); Walsh-trained clinicians worldwide",
     "cost_estimate":"$1500-3000 initial workup",
     "key_researcher_id":"Walsh_William",
     "created_at":NOW,"last_updated":NOW,
     "notes":"See PHE-0008/0009/0010/0011 for biotype phenotype entries"},

    {"id":"PROT-0002","name":"Frye FRAA + leucovorin protocol","provider":"Drfryemdphd.com / multiple MAPS clinicians",
     "origin_year":"2010s","framework_class":"folate_pathway",
     "description":"FRAA antibody panel → if positive, leucovorin (folinic acid) trial 0.5-2 mg/kg/day stratified by FRAA status",
     "test_panel":"FRAA blocking + binding; CSF 5-MTHF if confirmable",
     "intervention_stack":"Leucovorin first-line; methyl-B12 + 5-MTHF + cofactors; calibrated by SNP profile",
     "target_population":"FRAA-positive (~70-75% of autism); language-impaired ASD",
     "evidence_strength":"RCT-grade (Frye 2018 PMID 27752075); calibration anchor in atlas",
     "clinical_availability":"MAPS-trained physicians + Frye consultations",
     "cost_estimate":"$300-500 FRAA test + $50-100/month leucovorin",
     "key_researcher_id":"Frye_Richard",
     "key_pmids":"27752075",
     "created_at":NOW,"last_updated":NOW,
     "notes":"Highest-evidence pediatric biomedical autism protocol"},

    {"id":"PROT-0003","name":"Yasko SNP-targeted methylation protocol","provider":"Holistic Health Inc / dr Amy Yasko",
     "origin_year":"2000s","framework_class":"methylation_genetic",
     "description":"30+ methylation-cycle SNPs (MTHFR/MTRR/MTR/COMT/CBS/BHMT/AHCY/MAT/SUOX/NOS) drive sequential nutrient-introduction protocol; clear toxicants → support transsulfuration → B12/B6 → methyl donors",
     "test_panel":"23andMe + StrateGene/SelfDecode/Yasko Nutrigenomic Panel",
     "intervention_stack":"Sequential SNP-calibrated nutrients + RNA support",
     "target_population":"Methylation-driven ASD; complex multi-SNP profiles",
     "evidence_strength":"Mechanistic + clinical; not large RCT",
     "clinical_availability":"Holistic Health Inc + Yasko-trained clinicians",
     "cost_estimate":"varies; SNP panel ~$200-400 + protocol stack",
     "key_researcher_id":"Yasko_Amy",
     "created_at":NOW,"last_updated":NOW},

    {"id":"PROT-0004","name":"Neubrander methyl-B12 SC protocol","provider":"Neubrander Clinic / MAPS clinicians",
     "origin_year":"early 2000s","framework_class":"methylation_pathway",
     "description":"Subcutaneous methylcobalamin every-3-days dosing protocol for autism methylation support",
     "test_panel":"B12 + MMA + SAM/SAH + methylation SNPs",
     "intervention_stack":"Methylcobalamin SC ~64.5 mcg/kg every 3 days; often combined with leucovorin",
     "target_population":"B12/methylation-deficient autism subgroup",
     "evidence_strength":"Decades clinical; limited large trials",
     "clinical_availability":"MAPS-trained physicians; compounding pharmacy required",
     "cost_estimate":"$50-150/month for compounded methyl-B12",
     "key_researcher_id":"Neubrander_James",
     "created_at":NOW,"last_updated":NOW},

    {"id":"PROT-0005","name":"Bock Plan (4-A epidemic framework)","provider":"Bock Integrative Medicine",
     "origin_year":"2000s","framework_class":"functional_pediatric_general",
     "description":"Comprehensive layered biomedical protocol: foundational (food/sleep/environment) → gut healing → detoxification → methylation/mitochondrial → immune/neurotransmitter",
     "test_panel":"Comprehensive food sensitivity; metals; gut microbiome; methylation; mitochondrial; neurotransmitters",
     "intervention_stack":"Multi-domain layered protocol",
     "target_population":"Autism + ADHD + asthma + allergies (4-A) cluster",
     "evidence_strength":"Clinical-volume; book-published",
     "clinical_availability":"Bock Integrative Medicine (NY/Manhattan); telehealth",
     "key_researcher_id":"Bock_Kenneth",
     "created_at":NOW,"last_updated":NOW},

    {"id":"PROT-0006","name":"Klinghardt protocols","provider":"Sophia Health Institute / Klinghardt-trained",
     "origin_year":"2000s","framework_class":"chronic_infection_environmental",
     "description":"Five-tier protocol: detox → reduction of biotoxins → mitochondrial support → autonomic regulation → trauma/cognitive integration. Heavy emphasis on Lyme + tick-borne + mold + heavy-metal subgroups",
     "test_panel":"Heavy metals; mycotoxins; Lyme + co-infections; ART/autonomic-response testing",
     "intervention_stack":"Biotoxin binders + Lyme protocols + KMT (Klinghardt Matrix Therapy)",
     "target_population":"Chronic-infection / environmental-toxicant subgroup",
     "evidence_strength":"Clinical experience; limited peer-review",
     "clinical_availability":"Sophia Health Institute + Klinghardt-trained worldwide",
     "key_researcher_id":"",
     "created_at":NOW,"last_updated":NOW,
     "notes":"More controversial; emphasis on chronic biotoxin / Lyme subset"},

    {"id":"PROT-0007","name":"MAPS framework (Medical Academy of Pediatric Special Needs)","provider":"MAPS-trained clinicians",
     "origin_year":"2010s","framework_class":"functional_pediatric_curriculum",
     "description":"Standardized training curriculum for biomedical pediatric autism care; integrates Frye / Walsh / Bock / Yasko / Neubrander frameworks; certification program",
     "test_panel":"Comprehensive biomedical workup",
     "intervention_stack":"Multi-framework integrated; protocols vary by clinician",
     "target_population":"Biomedical autism + special-needs pediatrics",
     "evidence_strength":"Aggregates underlying frameworks",
     "clinical_availability":"MAPS-trained clinicians worldwide; certification searchable",
     "created_at":NOW,"last_updated":NOW,
     "notes":"Most-common 'who do I find' answer for biomedical autism care"},

    {"id":"PROT-0008","name":"ARI (Autism Research Institute) DAN! protocol legacy","provider":"ARI / functional medicine community",
     "origin_year":"1990s-2000s","framework_class":"foundational_biomedical",
     "description":"Foundational biomedical autism protocol from ARI (Defeat Autism Now!) era; established gluten/casein-free diet, methyl-B12, leucovorin, antifungal protocols, chelation; predecessor to MAPS",
     "test_panel":"Original biomedical workup",
     "intervention_stack":"Diet + supplements + targeted protocols",
     "target_population":"Foundational biomedical autism",
     "evidence_strength":"Historical foundation; many components later supported in RCT",
     "clinical_availability":"DAN! formally retired; superseded by MAPS",
     "created_at":NOW,"last_updated":NOW,
     "notes":"Historical foundation; DAN! certifications no longer issued"},

    {"id":"PROT-0009","name":"Hazan familial FMT protocol","provider":"ProgenaBiome / Sabine Hazan FDA IND",
     "origin_year":"2020s","framework_class":"microbiome_intervention",
     "description":"Sibling-donor FMT under FDA IND with full pre/post sequencing; iterative reflorization targeting Bifidobacterium restoration",
     "test_panel":"Full microbiome sequencing pre/post (ProgenaBiome)",
     "intervention_stack":"Sibling-donor FMT + diet + targeted probiotics",
     "target_population":"Severe ASD with documented Bifidobacterium depletion / microbiome dysbiosis",
     "evidence_strength":"FDA IND + ACG award + peer-reviewed case (PMID 38715916); twins case",
     "clinical_availability":"ProgenaBiome (Ventura CA) under FDA IND NCT04878718",
     "cost_estimate":"varies; research-clinic basis",
     "key_researcher_id":"Hazan_Sabine",
     "key_pmids":"38715916",
     "created_at":NOW,"last_updated":NOW},

    {"id":"PROT-0010","name":"Adams MTT (Microbiota Transfer Therapy)","provider":"Arizona State University",
     "origin_year":"2017","framework_class":"microbiome_intervention",
     "description":"Structured 2-week antibiotic preconditioning + microbiota dosing + prolonged oral maintenance phase. Peer-reviewed Phase 2 trial.",
     "test_panel":"Standard ASD biomedical + microbiome composition",
     "intervention_stack":"MTT structured protocol",
     "target_population":"Autism with GI involvement",
     "evidence_strength":"Phase 2 RCT-grade; 2-year sustained outcomes",
     "clinical_availability":"ASU clinical trial enrollment",
     "key_researcher_id":"Adams_James",
     "key_pmids":"28122648,30967657",
     "created_at":NOW,"last_updated":NOW},
]

print(f"Adding {len(protocols)} protocols (new entity type)")

# ============================================================
# Append to CSVs
# ============================================================
def append_csv(path, fields, new_rows, key="id"):
    rows = list(csv.DictReader(open(path)))
    existing = {r[key] for r in rows}
    added = 0
    for r in new_rows:
        if r[key] in existing: continue
        out = {f: r.get(f, "") for f in fields}
        rows.append(out); added += 1
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
    return added

for d in [ROOT/"v2.0_scored", ROOT/"v2.0.1_expanded"]:
    print(f"\n{d.name}:")
    hyp_fields = list(csv.DictReader(open(d/"hypotheses.csv")).fieldnames)
    n = append_csv(d/"hypotheses.csv", hyp_fields, new_hyps)
    print(f"  hypotheses.csv: +{n}")

    phe_fields = list(csv.DictReader(open(d/"phenotypes.csv")).fieldnames)
    n = append_csv(d/"phenotypes.csv", phe_fields, new_phes)
    print(f"  phenotypes.csv: +{n}")

    int_fields = list(csv.DictReader(open(d/"interventions.csv")).fieldnames)
    n = append_csv(d/"interventions.csv", int_fields, new_ints)
    print(f"  interventions.csv: +{n}")

    # New protocols.csv
    with open(d/"protocols.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=PROTOCOL_FIELDS)
        w.writeheader()
        for r in protocols:
            w.writerow({k: r.get(k, "") for k in PROTOCOL_FIELDS})
    print(f"  protocols.csv: created with {len(protocols)} rows")

print("\nDone. 3.5C+D+B+E atlas additions complete.")
