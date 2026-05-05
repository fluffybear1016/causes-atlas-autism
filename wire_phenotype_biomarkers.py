#!/usr/bin/env python3
"""Wire biomarkers to phenotypes for PHE-0001 through PHE-0007 based on neurobiochem/biophysics deep-dives.

Idempotent: replaces biomarker_phenotype_edges.csv with full mapping.
Covers Tier 1 + Tier 2 biomarker associations from the 7 phenotype deep-dive pages.
Each edge represents 'biomarker stratifies / measures / characterizes phenotype'.
"""
import csv
import datetime
from pathlib import Path

ATLAS = Path("/sessions/jolly-determined-darwin/mnt/Autism/v2.0_scored")
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()

# (biomarker_id, phenotype_id, relationship_type, evidence_strength)
# strength 0.55 (default tier-1 marker), 0.45 (tier-2 supporting), 0.35 (tier-3 / research)
# matches existing strengths from previous wiring.

EDGES = [
    # ========== PHE-0001 Cerebral folate deficiency (existing 5 + adds) ==========
    ("BIO-0001", "PHE-0001", "stratifies", 0.55),  # SAM
    ("BIO-0003", "PHE-0001", "stratifies", 0.55),  # SAM/SAH
    ("BIO-0015", "PHE-0001", "stratifies", 0.65),  # FRAA blocking — tier-1 diagnostic
    ("BIO-0016", "PHE-0001", "stratifies", 0.65),  # FRAA binding — tier-1 diagnostic
    ("BIO-0017", "PHE-0001", "stratifies", 0.70),  # CSF 5-MTHF — gold standard
    ("BIO-0011", "PHE-0001", "supports", 0.35),    # Plasma folate — supporting (often normal)
    ("BIO-0005", "PHE-0001", "supports", 0.35),    # Homocysteine
    ("BIO-0046", "PHE-0001", "supports", 0.45),    # HVA — dopamine deficit downstream
    ("BIO-0048", "PHE-0001", "supports", 0.45),    # 5-HIAA — serotonin deficit downstream
    ("BIO-0089", "PHE-0001", "modifies_risk", 0.40),  # Maternal MTHFR

    # ========== PHE-0002 Mitochondrial dysfunction (existing 3 + adds) ==========
    ("BIO-0018", "PHE-0002", "stratifies", 0.65),  # Lactate
    ("BIO-0019", "PHE-0002", "stratifies", 0.55),  # Pyruvate
    ("BIO-0020", "PHE-0002", "stratifies", 0.70),  # L:P ratio — most specific
    ("BIO-0021", "PHE-0002", "stratifies", 0.60),  # Acylcarnitine
    ("BIO-0022", "PHE-0002", "stratifies", 0.55),  # Free + total carnitine
    ("BIO-0023", "PHE-0002", "supports", 0.40),    # Plasma ammonia
    ("BIO-0024", "PHE-0002", "supports", 0.40),    # CK
    ("BIO-0025", "PHE-0002", "supports", 0.45),    # CoQ10
    ("BIO-0026", "PHE-0002", "stratifies", 0.55),  # mtDNA copy number
    ("BIO-0027", "PHE-0002", "supports", 0.40),    # Krebs metabolites
    ("BIO-0028", "PHE-0002", "stratifies", 0.55),  # GSH
    ("BIO-0029", "PHE-0002", "stratifies", 0.55),  # GSSG
    ("BIO-0030", "PHE-0002", "stratifies", 0.65),  # GSH/GSSG ratio
    ("BIO-0031", "PHE-0002", "supports", 0.40),    # 8-OHdG
    ("BIO-0032", "PHE-0002", "supports", 0.40),    # F2-isoprostanes
    ("BIO-0141", "PHE-0002", "supports", 0.45),    # 1H-MRS lactate peak

    # ========== PHE-0003 Regressive immune-inflammatory (NEW — was 0) ==========
    ("BIO-0052", "PHE-0003", "stratifies", 0.55),  # hs-CRP
    ("BIO-0053", "PHE-0003", "supports", 0.40),    # ESR
    ("BIO-0054", "PHE-0003", "stratifies", 0.65),  # IL-6
    ("BIO-0055", "PHE-0003", "stratifies", 0.65),  # TNF-α
    ("BIO-0056", "PHE-0003", "stratifies", 0.60),  # IL-1β
    ("BIO-0057", "PHE-0003", "stratifies", 0.55),  # IL-17
    ("BIO-0058", "PHE-0003", "stratifies", 0.55),  # IL-10 (deficient)
    ("BIO-0059", "PHE-0003", "supports", 0.45),    # IFN-γ
    ("BIO-0060", "PHE-0003", "supports", 0.50),    # Complement C3 C4
    ("BIO-0061", "PHE-0003", "supports", 0.45),    # IgG/IgA/IgM/IgE
    ("BIO-0088", "PHE-0003", "stratifies", 0.65),  # Maternal MAR antibodies
    ("BIO-0091", "PHE-0003", "modifies_risk", 0.55),  # Maternal CRP pregnancy
    ("BIO-0092", "PHE-0003", "modifies_risk", 0.45),  # Maternal thyroid panel
    ("BIO-0142", "PHE-0003", "stratifies", 0.55),  # PET-TSPO microglia
    ("BIO-0151", "PHE-0003", "stratifies", 0.60),  # CSF cytokines
    ("BIO-0154", "PHE-0003", "supports", 0.45),    # Serum S100β
    ("BIO-0155", "PHE-0003", "supports", 0.45),    # Serum GFAP
    ("BIO-0156", "PHE-0003", "supports", 0.40),    # Serum NfL
    ("BIO-0172", "PHE-0003", "stratifies", 0.55),  # Anti-NMDA receptor
    ("BIO-0173", "PHE-0003", "supports", 0.45),    # Anti-MOG
    ("BIO-0133", "PHE-0003", "supports", 0.45),    # ANA + ENA
    ("BIO-0135", "PHE-0003", "supports", 0.40),    # Thyroid antibodies

    # ========== PHE-0004 GI / microbiome (existing 4 + adds) ==========
    ("BIO-0036", "PHE-0004", "stratifies", 0.65),  # Arabinose
    ("BIO-0037", "PHE-0004", "stratifies", 0.65),  # HPHPA
    ("BIO-0038", "PHE-0004", "stratifies", 0.65),  # 4-cresol
    ("BIO-0039", "PHE-0004", "supports", 0.45),    # Tartaric acid
    ("BIO-0040", "PHE-0004", "supports", 0.45),    # Citramalic
    ("BIO-0041", "PHE-0004", "supports", 0.40),    # Indican
    ("BIO-0042", "PHE-0004", "supports", 0.45),    # Hippuric
    ("BIO-0043", "PHE-0004", "supports", 0.40),    # IAA
    ("BIO-0044", "PHE-0004", "supports", 0.40),    # DHPPA
    ("BIO-0045", "PHE-0004", "supports", 0.40),    # 3-Hydroxy-2-methylbutyric
    ("BIO-0049", "PHE-0004", "supports", 0.45),    # Quinolinic
    ("BIO-0050", "PHE-0004", "supports", 0.45),    # Kynurenic
    ("BIO-0051", "PHE-0004", "supports", 0.50),    # Kyn/Trp ratio
    ("BIO-0109", "PHE-0004", "stratifies", 0.55),  # Zonulin
    ("BIO-0110", "PHE-0004", "stratifies", 0.55),  # LPS
    ("BIO-0111", "PHE-0004", "stratifies", 0.55),  # Calprotectin
    ("BIO-0112", "PHE-0004", "stratifies", 0.50),  # sIgA
    ("BIO-0113", "PHE-0004", "stratifies", 0.55),  # Lactulose:mannitol
    ("BIO-0131", "PHE-0004", "supports", 0.45),    # C. diff
    ("BIO-0132", "PHE-0004", "supports", 0.45),    # Candida IgG/IgA
    ("BIO-0167", "PHE-0004", "modifies_risk", 0.40),  # FUT2 secretor
    ("BIO-0178", "PHE-0004", "stratifies", 0.65),  # Comprehensive Stool Analysis

    # ========== PHE-0005 mTOR pathway syndromic (NEW — was 0) ==========
    ("BIO-0137", "PHE-0005", "stratifies", 0.65),  # MRI cortical thickness (tubers)
    ("BIO-0138", "PHE-0005", "stratifies", 0.65),  # Brain volumetry (macrocephaly)
    ("BIO-0139", "PHE-0005", "supports", 0.50),    # DTI white matter
    ("BIO-0140", "PHE-0005", "supports", 0.50),    # rs-fMRI DMN
    ("BIO-0141", "PHE-0005", "stratifies", 0.55),  # 1H-MRS glutamate excess
    ("BIO-0143", "PHE-0005", "stratifies", 0.55),  # EEG (seizure activity)
    ("BIO-0144", "PHE-0005", "supports", 0.40),    # P300

    # ========== PHE-0006 Fragile X (FMR1) (NEW — was 0) ==========
    ("BIO-0137", "PHE-0006", "supports", 0.45),    # MRI cortical thickness
    ("BIO-0138", "PHE-0006", "supports", 0.50),    # Brain volumetry (caudate, cerebellar vermis)
    ("BIO-0141", "PHE-0006", "stratifies", 0.55),  # 1H-MRS Glu/GABA
    ("BIO-0143", "PHE-0006", "stratifies", 0.65),  # EEG — characteristic patterns
    ("BIO-0144", "PHE-0006", "stratifies", 0.55),  # ERP P300
    ("BIO-0145", "PHE-0006", "stratifies", 0.55),  # ERP MMN
    ("BIO-0146", "PHE-0006", "stratifies", 0.55),  # ERP N170 face processing
    ("BIO-0147", "PHE-0006", "supports", 0.50),    # qEEG coherence
    ("BIO-0149", "PHE-0006", "stratifies", 0.55),  # Pupillometry sensory reactivity
    ("BIO-0150", "PHE-0006", "supports", 0.45),    # HRV autonomic
    ("BIO-0153", "PHE-0006", "supports", 0.45),    # BDNF research biomarker

    # ========== PHE-0007 GABA/Cl- imbalance (NEW — was 0) ==========
    ("BIO-0013", "PHE-0007", "supports", 0.45),    # P5P / B6 GABA cofactor
    ("BIO-0141", "PHE-0007", "stratifies", 0.65),  # 1H-MRS GABA/Glu — most specific
    ("BIO-0143", "PHE-0007", "stratifies", 0.65),  # EEG abnormalities
    ("BIO-0145", "PHE-0007", "stratifies", 0.60),  # ERP MMN — auditory inhibition
    ("BIO-0147", "PHE-0007", "stratifies", 0.55),  # qEEG coherence
    ("BIO-0149", "PHE-0007", "supports", 0.50),    # Pupillometry sensory load
    ("BIO-0150", "PHE-0007", "supports", 0.45),    # HRV
    ("BIO-0174", "PHE-0007", "supports", 0.45),    # Anti-GAD65 antibodies
]


def main():
    out = ATLAS / "biomarker_phenotype_edges.csv"
    rows = []
    rows.append(["id", "biomarker_id", "phenotype_id", "relationship_type",
                 "evidence_strength", "created_at", "notes"])

    # Load biomarkers names for note generation
    bio_names = {}
    with open(ATLAS / "biomarkers.csv") as f:
        reader = csv.DictReader(f)
        for r in reader:
            bio_names[r["id"]] = r["name"]

    for i, (bio_id, phe_id, rel, strength) in enumerate(EDGES, start=1):
        bio_name = bio_names.get(bio_id, bio_id)
        edge_id = f"BPE-{i:05d}"
        note = f"{bio_name} {rel} {phe_id}"
        rows.append([edge_id, bio_id, phe_id, rel, f"{strength:.2f}", NOW, note])

    with open(out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerows(rows)

    # Stats
    by_phe = {}
    for bio_id, phe_id, rel, strength in EDGES:
        by_phe.setdefault(phe_id, []).append(bio_id)

    print(f"Wrote {len(EDGES)} biomarker-phenotype edges to {out}")
    for phe in sorted(by_phe):
        print(f"  {phe}: {len(by_phe[phe])} edges")


if __name__ == "__main__":
    main()
