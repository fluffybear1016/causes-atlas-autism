#!/usr/bin/env python3
"""Fix biomarker layer audit findings.

1. Patch INDEX.md de-snake_case (PANS PANDAS not Pans Pandas, etc.)
2. Add 12 gap-fill biomarkers (child vitamin D, urinary porphyrins, FUT2, oxalate, CYP variants, autoimmune encephalitis antibodies, salivary CAR, lipid panel, ApoE, etc.)
3. Fix BIO-0099 Cu:Zn upper bound (1.0 → 1.2)
4. Add age_caveat to BIO-0103 ferritin
5. Add atlas connections for brain biomarkers BIO-0144-0157 that lack them
6. Fix BIO-0014 whole-blood histamine — add hypotheses_tests
7. Fix BIO-0050 kynurenic acid wording (QUIN/KYN → QUIN/KYNA)
"""
import csv, datetime as dt, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NOW = dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')

# ============================================================
# 1. Load existing biomarkers
# ============================================================
biomarkers_path = ROOT/"v2.0_scored"/"biomarkers.csv"
fields = list(csv.DictReader(open(biomarkers_path)).fieldnames)
rows = list(csv.DictReader(open(biomarkers_path)))
print(f"Loaded {len(rows)} existing biomarkers")

# Map for lookups
by_id = {r["id"]: r for r in rows}

# ============================================================
# 2. Apply individual fixes to existing rows
# ============================================================
# BIO-0014 whole-blood histamine — add hypotheses_tests
if "BIO-0014" in by_id:
    by_id["BIO-0014"]["hypotheses_tests"] = "HYP-0001"
    print("  ✓ BIO-0014: added HYP-0001")

# BIO-0050 kynurenic acid — fix wording
for r in rows:
    if r["name"].lower().startswith("kynurenic"):
        r["interpretation_summary"] = "QUIN/KYNA ratio is most informative for inflammation-driven shift"
        print(f"  ✓ {r['id']}: fixed QUIN/KYNA wording")

# BIO-0099 Cu:Zn ratio fix upper bound
for r in rows:
    if "cu:zn" in r["name"].lower() or "cu/zn" in r["name"].lower():
        r["reference_high"] = "1.2"
        r["interpretation_summary"] = "Walsh framework: optimal ≤1.0; >1.2 = copper overload phenotype"
        print(f"  ✓ {r['id']}: Cu:Zn ratio reference_high → 1.2")

# BIO-0103 ferritin age caveat
for r in rows:
    if r["name"].lower().startswith("ferritin"):
        r["age_caveat"] = "Pediatric ranges differ substantially: infants 10-200 ng/mL; toddlers 7-140; school-age 10-150. >30 is functional optimal floor but normal infants may run lower."
        r["reference_low"] = "10"  # broader pediatric floor
        print(f"  ✓ {r['id']}: ferritin age_caveat added, reference_low → 10")

# Brain biomarkers BIO-0144 through BIO-0157 — fill missing atlas connections
brain_connections = {
    "MRI cortical thickness": ("MEC-0006", "PHE-0007", "", "HYP-0073"),
    "Total brain volume": ("MEC-0006", "", "", "HYP-0071,HYP-0073"),
    "DTI fractional anisotropy": ("MEC-0006", "", "", "HYP-0073"),
    "Resting-state fMRI": ("MEC-0006", "", "", "HYP-0073"),
    "1H-MRS NAA": ("MEC-0007,MEC-0010,MEC-0020", "", "", "HYP-0006,HYP-0071"),
    "PET-TSPO": ("MEC-0002,MEC-0005", "PHE-0003", "INT-0102,INT-0006", "HYP-0008"),
    "EEG resting-state": ("MEC-0007,MEC-0020", "", "", "HYP-0071"),
    "ERP P300": ("MEC-0006,MEC-0020", "", "", "HYP-0073"),
    "ERP MMN": ("MEC-0006,MEC-0020", "", "", "HYP-0073"),
    "ERP N170": ("MEC-0006", "", "", "HYP-0073"),
    "qEEG coherence": ("MEC-0006,MEC-0020", "", "", "HYP-0071"),
    "Gaze fixation pattern": ("MEC-0006", "", "", "HYP-0073"),
    "Pupillometry": ("MEC-0019", "", "", ""),
    "CSF cytokines": ("MEC-0002,MEC-0005", "PHE-0003", "INT-0102,INT-0006", "HYP-0008"),
    "CSF tau": ("MEC-0006", "", "", "HYP-0073"),
    "Serum BDNF": ("MEC-0028", "", "", "HYP-0073"),
    "Serum S100": ("MEC-0004,MEC-0005", "", "", "HYP-0008"),
    "Serum GFAP": ("MEC-0005", "", "", "HYP-0008"),
    "Serum neurofilament": ("MEC-0006", "", "", "HYP-0073"),
    "Serum tau": ("MEC-0006", "", "", "HYP-0073"),
}
for r in rows:
    for key, (mec, phe, intv, hyp) in brain_connections.items():
        if key.lower() in r["name"].lower() and not r.get("mechanisms_indicated"):
            r["mechanisms_indicated"] = mec
            if phe: r["phenotypes_stratified"] = phe
            if intv: r["interventions_modulates"] = intv
            if hyp: r["hypotheses_tests"] = hyp
            r["last_updated"] = NOW
            print(f"  ✓ {r['id']}: brain biomarker connections wired")
            break

# ============================================================
# 3. Add 14 gap-fill biomarkers
# ============================================================
# Find next available BIO-NNNN
existing_ids = {int(r["id"].split("-")[1]) for r in rows}
next_n = max(existing_ids) + 1

def make(name, **kw):
    global next_n
    out = {f: "" for f in fields}
    out["id"] = f"BIO-{next_n:04d}"
    out["name"] = name
    out["created_at"] = NOW
    out["last_updated"] = NOW
    out["test_availability"] = "commercial"
    for k, v in kw.items():
        out[k] = v
    next_n += 1
    return out

# Gap-fill list — high-priority additions per audit
gapfills = [
    make("Vitamin D 25-OH (child / direct)",
         category="trace_minerals", subcategory="essential_vitamin",
         sample_type="serum", units="ng/mL",
         reference_low="30", reference_high="80",
         reference_optimal_low="40", reference_optimal_high="60",
         what_it_measures="Direct child vitamin D status — most-studied single nutrient biomarker in autism",
         low_means="Vitamin D deficiency (<30 ng/mL) very common in autism; immune dysregulation + serotonin synthesis (TPH2) impacts",
         interpretation_summary="Target 40-60 ng/mL for autism. Most pediatric mainstream 'normal' (>20) is inadequate.",
         mechanisms_indicated="MEC-0002,MEC-0029",
         hypotheses_tests="HYP-0045,HYP-0062",
         clia_status="CLIA", test_availability="standard_clinical",
         test_cost_usd_low="40", test_cost_usd_high="80",
         lab_options="Quest, LabCorp"),

    make("Urinary porphyrins (heavy metal body burden surrogate)",
         category="heavy_metals", subcategory="body_burden_surrogate",
         sample_type="urine_24h", units="μg/g creatinine",
         what_it_measures="Porphyrin profile reflecting heavy metal interference with heme synthesis",
         elevated_means="Mercury and/or other heavy metal body burden suggested",
         interpretation_summary="Coproporphyrin / pentacarboxyporphyrin / precoproporphyrin patterns specific for mercury; clinically used in autism heavy-metal subgroup workup",
         mechanisms_indicated="MEC-0001,MEC-0010",
         hypotheses_tests="HYP-0015,HYP-0069",
         lab_options="Doctor's Data, Lab Corp",
         test_cost_usd_low="100", test_cost_usd_high="250"),

    make("FUT2 secretor status genotype",
         category="genetic_snp", subcategory="microbiome_genetic",
         sample_type="buccal_or_blood", units="genotype (secretor/non-secretor)",
         what_it_measures="FUT2 alpha-1,2-fucosyltransferase variant; non-secretors have altered B12 absorption + microbiome composition",
         interpretation_summary="Non-secretors (~20% population) have lower B12, less Bifidobacterium, different microbiome — affects autism workup interpretation",
         snp_dependence="self",
         mechanisms_indicated="MEC-0008",
         hypotheses_tests="HYP-0007,HYP-0056",
         test_availability="commercial_dtc",
         lab_options="23andMe, SelfDecode"),

    make("Urinary oxalate",
         category="oat_microbial", subcategory="oxalate",
         sample_type="urine_24h_or_spot", units="mmol/g creatinine",
         what_it_measures="Oxalate excretion — high oxalate ↔ Candida + GI permeability + mito stress",
         elevated_means="Oxalate overload; GI absorption issues + Candida + low-oxalate diet candidate",
         interpretation_summary="Per Susan Costen Owens / Trying Low Oxalates framework",
         mechanisms_indicated="MEC-0008,MEC-0010",
         hypotheses_tests="HYP-0007,HYP-0061",
         lab_options="Mosaic OAT, Great Plains"),

    make("CYP2D6 genotype",
         category="genetic_snp", subcategory="pharmacogenomic",
         sample_type="buccal_or_blood", units="phenotype (poor/intermediate/normal/rapid/ultra-rapid metabolizer)",
         what_it_measures="CYP2D6 drug-metabolism variant — affects SSRI, antipsychotic, atomoxetine, codeine response",
         interpretation_summary="Critical pre-prescription test for autistic kids being prescribed psychotropics. Ultra-rapid metabolizers can have toxic effects at standard doses; poor metabolizers can have no effect.",
         snp_dependence="self",
         test_availability="standard_clinical",
         clia_status="CLIA",
         lab_options="GeneSight, Genomind, Tempus PGx, standard clinical labs"),

    make("CYP3A4 / CYP3A5 genotype",
         category="genetic_snp", subcategory="pharmacogenomic",
         sample_type="buccal_or_blood", units="phenotype",
         what_it_measures="CYP3A4/5 metabolism — affects benzodiazepines, statins, immunosuppressants (rapamycin)",
         interpretation_summary="Important for rapamycin dosing in TSC/PTEN autism subgroups",
         snp_dependence="self",
         interventions_modulates="INT-0036",
         test_availability="standard_clinical",
         clia_status="CLIA"),

    make("CYP2C19 genotype",
         category="genetic_snp", subcategory="pharmacogenomic",
         sample_type="buccal_or_blood", units="phenotype",
         what_it_measures="CYP2C19 metabolism — affects PPIs, SSRIs (citalopram, escitalopram), clobazam",
         interpretation_summary="Common SSRI metabolism variant; pediatric prescribing implications",
         snp_dependence="self",
         test_availability="standard_clinical",
         clia_status="CLIA"),

    make("Anti-NMDA receptor antibodies",
         category="autoimmune", subcategory="autoimmune_encephalitis",
         sample_type="serum_or_csf", units="titer",
         what_it_measures="Anti-NMDA receptor encephalitis screen — distinct from PANS/PANDAS",
         elevated_means="Autoimmune encephalitis; immunotherapy candidate",
         interpretation_summary="CSF testing more sensitive than serum",
         mechanisms_indicated="MEC-0002,MEC-0020",
         hypotheses_tests="HYP-0026,HYP-0051",
         clia_status="CLIA",
         lab_options="Mayo Clinic, ARUP, Quest"),

    make("Anti-MOG (myelin oligodendrocyte glycoprotein)",
         category="autoimmune", subcategory="autoimmune_encephalitis",
         sample_type="serum_or_csf", units="titer",
         what_it_measures="MOG antibody disease screen; CNS demyelination",
         hypotheses_tests="HYP-0051",
         clia_status="CLIA",
         lab_options="Mayo Clinic"),

    make("Anti-GAD65 antibodies",
         category="autoimmune", subcategory="autoimmune_encephalitis",
         sample_type="serum_or_csf", units="titer",
         what_it_measures="GAD65 autoimmunity — affects GABA synthesis; rare encephalitis cause",
         interpretation_summary="Connects to GABA developmental switch hypothesis",
         mechanisms_indicated="MEC-0007,MEC-0034",
         hypotheses_tests="HYP-0071",
         clia_status="CLIA"),

    make("Salivary cortisol awakening response (CAR)",
         category="endocrine", subcategory="hpa_axis_alternative",
         sample_type="saliva_morning", units="nmol/L composite",
         what_it_measures="Cortisol awakening response — HPA axis alternative to DUTCH",
         interpretation_summary="4-point morning saliva (waking, +30min, +45min, +60min); reveals HPA reactivity that single morning cortisol misses",
         mechanisms_indicated="MEC-0016",
         hypotheses_tests="HYP-0036,HYP-0037",
         test_availability="specialty",
         lab_options="ZRT Lab, Genova"),

    make("Lipid panel (TC, LDL, HDL, triglycerides)",
         category="endocrine", subcategory="metabolic",
         sample_type="serum", units="mg/dL composite",
         what_it_measures="Lipid metabolism; emerging metabolic-autism overlap",
         interpretation_summary="Low total cholesterol can indicate Smith-Lemli-Opitz; high triglycerides ↔ insulin resistance subgroup",
         mechanisms_indicated="MEC-0011,MEC-0012",
         hypotheses_tests="HYP-0018,HYP-0019",
         clia_status="CLIA", test_availability="standard_clinical"),

    make("ApoE genotype",
         category="genetic_snp", subcategory="lipid_genetic",
         sample_type="buccal_or_blood", units="genotype (E2/E3/E4)",
         what_it_measures="Apolipoprotein E variant — lipid metabolism, neuroinflammation, BBB permeability",
         interpretation_summary="E4 carriers more vulnerable to neuroinflammation + BBB disruption; emerging autism research relevance",
         snp_dependence="self",
         mechanisms_indicated="MEC-0004,MEC-0031",
         test_availability="commercial_dtc",
         lab_options="23andMe, ApoE-specific clinical tests"),

    make("Comprehensive Stool Analysis (GI-MAP / CDSA composite)",
         category="gi_barrier", subcategory="comprehensive_panel",
         sample_type="stool", units="qPCR composite",
         what_it_measures="Strain-level bacterial / fungal / parasite / viral quantification + barrier + inflammation markers",
         interpretation_summary="Per Diagnostic Solutions Lab GI-MAP framework; complements OAT (which measures metabolites, not organisms)",
         mechanisms_indicated="MEC-0008",
         phenotypes_stratified="PHE-0004",
         hypotheses_tests="HYP-0007,HYP-0056,HYP-0057,HYP-0061",
         interventions_modulates="INT-0076,INT-0025",
         test_availability="specialty",
         lab_options="Diagnostic Solutions Lab (GI-MAP), Doctor's Data CDSA, Genova GI Effects",
         test_cost_usd_low="350", test_cost_usd_high="500"),
]

print(f"\nAdding {len(gapfills)} new biomarkers (BIO-{next_n - len(gapfills):04d} through BIO-{next_n-1:04d})")

rows.extend(gapfills)
all_rows = rows  # for clarity

# ============================================================
# 4. Rebuild edge tables from scratch (clean state)
# ============================================================
def rebuild_edges(all_rows):
    bme, bpe, bie, bhe = [], [], [], []
    bme_n = bpe_n = bie_n = bhe_n = 1
    for b in all_rows:
        for m in (b.get("mechanisms_indicated") or "").split(","):
            m = m.strip()
            if not m: continue
            bme.append({"id": f"BME-{bme_n:05d}", "biomarker_id": b["id"], "mechanism_id": m,
                        "relationship_type": "indicates_dysfunction",
                        "evidence_strength": "0.50", "polarity": "supporting",
                        "created_at": NOW, "notes": f"{b['name']} indicates {m}"})
            bme_n += 1
        for p in (b.get("phenotypes_stratified") or "").split(","):
            p = p.strip()
            if not p: continue
            bpe.append({"id": f"BPE-{bpe_n:05d}", "biomarker_id": b["id"], "phenotype_id": p,
                        "relationship_type": "stratifies", "evidence_strength": "0.55",
                        "created_at": NOW, "notes": f"{b['name']} stratifies {p}"})
            bpe_n += 1
        for it in (b.get("interventions_modulates") or "").split(","):
            it = it.strip()
            if not it: continue
            bie.append({"id": f"BIE-{bie_n:05d}", "biomarker_id": b["id"], "intervention_id": it,
                        "relationship_type": "predicts_response", "direction": "normalize",
                        "evidence_strength": "0.50",
                        "created_at": NOW, "notes": f"{b['name']} predicts response to {it}"})
            bie_n += 1
        for h in (b.get("hypotheses_tests") or "").split(","):
            h = h.strip()
            if not h: continue
            bhe.append({"id": f"BHE-{bhe_n:05d}", "biomarker_id": b["id"], "hypothesis_id": h,
                        "relationship_type": "tests", "evidence_strength": "0.50",
                        "created_at": NOW, "notes": f"{b['name']} tests {h}"})
            bhe_n += 1
    return bme, bpe, bie, bhe

bme, bpe, bie, bhe = rebuild_edges(all_rows)
print(f"\nRebuilt edges: BME={len(bme)}, BPE={len(bpe)}, BIE={len(bie)}, BHE={len(bhe)}")

# ============================================================
# 5. Write CSVs
# ============================================================
edge_fields = {
    "BME": ["id","biomarker_id","mechanism_id","relationship_type","evidence_strength","polarity","created_at","notes"],
    "BPE": ["id","biomarker_id","phenotype_id","relationship_type","evidence_strength","created_at","notes"],
    "BIE": ["id","biomarker_id","intervention_id","relationship_type","direction","evidence_strength","created_at","notes"],
    "BHE": ["id","biomarker_id","hypothesis_id","relationship_type","evidence_strength","created_at","notes"],
}

def write_csv(path, fnames, rs):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fnames)
        w.writeheader()
        for r in rs:
            w.writerow({k: r.get(k, "") for k in fnames})

for d in [ROOT/"v2.0_scored", ROOT/"v2.0.1_expanded"]:
    write_csv(d/"biomarkers.csv", fields, all_rows)
    write_csv(d/"biomarker_mechanism_edges.csv", edge_fields["BME"], bme)
    write_csv(d/"biomarker_phenotype_edges.csv", edge_fields["BPE"], bpe)
    write_csv(d/"biomarker_intervention_edges.csv", edge_fields["BIE"], bie)
    write_csv(d/"biomarker_hypothesis_edges.csv", edge_fields["BHE"], bhe)
    print(f"  {d.name}/: rewrote 5 CSVs")

print(f"\n{len(all_rows)} biomarkers total now (was 164, added {len(gapfills)})")
