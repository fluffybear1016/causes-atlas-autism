#!/usr/bin/env python3
"""
densify_gene_layer.py — Wire 1,564 floating genes into the rest of the
graph using deterministic SFARI/biology cross-walks.

Three passes, all defensible:

  Pass 1 — SFARI Tier 1 + 2 genes → HYP-0028 (Inherited polygenic risk).
           These are exactly the substrate of the polygenic risk hypothesis.
           Provenance: SFARI gene score is the evidence.

  Pass 2 — Specific syndromic genes → matching phenotype.
           Curated, ~10 mappings, every one well-established biology.

  Pass 3 — Specific genes → specific mechanism (curated, ~25 mappings).
           Only well-known direct mechanism contributions.

Outputs candidate CSVs to v2.0.1_proposed/ for review before merge.
"""

import csv
import datetime as dt
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "v2.0_scored"
PROP = ROOT / "v2.0.1_proposed"
NOW = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def read(name): return list(csv.DictReader(open(SRC / name)))


genes = read("genes.csv")
existing_ghe = read("gene_hypothesis_edges.csv")
existing_gme = read("gene_mechanism_edges.csv")
existing_gpe = read("gene_phenotype_edges.csv")

# Index existing edges to skip dupes
ghe_pairs = {(r["gene_id"], r["hypothesis_id"]) for r in existing_ghe}
gme_pairs = {(r["gene_id"], r["mechanism_id"]) for r in existing_gme}
gpe_pairs = {(r["gene_id"], r["phenotype_id"]) for r in existing_gpe}

gene_by_symbol = {g["gene_symbol"]: g for g in genes}
gene_by_id = {g["id"]: g for g in genes}

# --------------------------------------------------------------------------
# PASS 1: SFARI Tier 1 + 2 → HYP-0028 (Inherited polygenic risk)
# --------------------------------------------------------------------------
# SFARI Tier 1 = "high confidence" — supported by ≥3 de novo mutations or strong
# convergent evidence. Tier 2 = "strong candidate". Both are core substrate of
# inherited polygenic ASD risk.
pass1 = []
for g in genes:
    if g["sfari_score"] not in ("1", "2"):
        continue
    if (g["id"], "HYP-0028") in ghe_pairs:
        continue
    pass1.append({
        "gene_id": g["id"],
        "hypothesis_id": "HYP-0028",
        "relation_type": "risk_factor_for",
        "polarity": "supporting",
        "rationale": f"SFARI score {g['sfari_score']} ASD risk gene (SFARI Gene database)",
    })
print(f"PASS 1: {len(pass1)} SFARI Tier 1+2 → HYP-0028 polygenic risk edges")

# --------------------------------------------------------------------------
# PASS 2: Specific syndromic gene → specific phenotype (curated)
# --------------------------------------------------------------------------
# Each mapping is textbook biology, verifiable in any major review.
SYN_GENE_TO_PHE = [
    ("FOLR1",  "PHE-0001", "FOLR1 autoantibody → cerebral folate deficiency phenotype"),
    ("FMR1",   "PHE-0006", "FMR1 CGG-repeat expansion → Fragile X phenotype"),
    ("TSC1",   "PHE-0005", "TSC1 mutation → tuberous sclerosis (mTOR-syndromic)"),
    ("TSC2",   "PHE-0005", "TSC2 mutation → tuberous sclerosis (mTOR-syndromic)"),
    ("PTEN",   "PHE-0005", "PTEN mutation → Cowden/PHTS macrocephaly autism (mTOR-syndromic)"),
    # Mitochondrial phenotype: nuclear mitochondrial genes
    ("POLG",   "PHE-0002", "POLG → mitochondrial DNA depletion → mito dysfunction phenotype"),
    ("SURF1",  "PHE-0002", "SURF1 → Leigh syndrome / complex IV deficiency"),
    # GABA/Cl- imbalance phenotype (PHE-0007)
    ("GABRB3", "PHE-0007", "GABRB3 → GABA-A receptor → Cl- imbalance subset"),
    ("GABRA3", "PHE-0007", "GABRA3 → GABA-A receptor → Cl- imbalance subset"),
    ("SLC12A5","PHE-0007", "KCC2 → developmental Cl- gradient inversion"),
]
pass2 = []
for sym, pid, rationale in SYN_GENE_TO_PHE:
    g = gene_by_symbol.get(sym)
    if not g:
        print(f"  PASS 2 skip: {sym} not in gene catalog")
        continue
    if (g["id"], pid) in gpe_pairs:
        continue
    pass2.append({
        "gene_id": g["id"],
        "phenotype_id": pid,
        "relation_type": "syndromic_cause_of",
        "polarity": "supporting",
        "rationale": rationale,
    })
print(f"PASS 2: {len(pass2)} specific syndromic gene → phenotype edges")

# --------------------------------------------------------------------------
# PASS 3: Specific gene → specific mechanism (curated)
# --------------------------------------------------------------------------
GENE_TO_MEC = [
    # mTOR pathway
    ("TSC1",     "MEC-0009", "TSC1 inactivation → mTORC1 hyperactivation"),
    ("TSC2",     "MEC-0009", "TSC2 inactivation → mTORC1 hyperactivation"),
    ("PTEN",     "MEC-0009", "PTEN loss → PIP3 ↑ → mTORC1 hyperactivation"),
    ("PIK3CA",   "MEC-0009", "PIK3CA gain-of-function → mTORC1 hyperactivation"),
    ("AKT3",     "MEC-0009", "AKT3 → mTORC1 axis"),
    ("MTOR",     "MEC-0009", "MTOR — direct"),
    # PI3K/AKT
    ("PIK3CA",   "MEC-0015", "PIK3CA — catalytic subunit of PI3K"),
    ("PTEN",     "MEC-0015", "PTEN antagonizes PI3K/AKT signaling"),
    ("AKT3",     "MEC-0015", "AKT3 — direct"),
    # Synaptic pruning / neuronal architecture
    ("SHANK3",   "MEC-0006", "SHANK3 postsynaptic scaffolding → synapse maturation"),
    ("SHANK1",   "MEC-0006", "SHANK1 — synaptic scaffolding"),
    ("SHANK2",   "MEC-0006", "SHANK2 — synaptic scaffolding"),
    ("NLGN3",    "MEC-0006", "NLGN3 — postsynaptic adhesion → synapse formation"),
    ("NLGN4",    "MEC-0006", "NLGN4 — postsynaptic adhesion"),
    ("NLGN4X",   "MEC-0006", "NLGN4X — X-linked NLGN4"),
    ("NRXN1",    "MEC-0006", "NRXN1 — presynaptic adhesion"),
    ("NRXN2",    "MEC-0006", "NRXN2 — presynaptic adhesion"),
    ("FMR1",     "MEC-0006", "FMR1 (FMRP) regulates local synaptic translation"),
    ("MECP2",    "MEC-0006", "MECP2 — chromatin regulator critical for mature neuron function"),
    # GABA/glutamate / E:I balance
    ("SCN2A",    "MEC-0007", "SCN2A — voltage-gated Na+ channel; E:I imbalance"),
    ("SCN1A",    "MEC-0007", "SCN1A — Na+ channel; E:I imbalance"),
    ("GRIN2B",   "MEC-0007", "GRIN2B — NMDAR subunit; glutamatergic E:I"),
    ("GRIN2A",   "MEC-0007", "GRIN2A — NMDAR subunit; glutamatergic E:I"),
    ("GABRB3",   "MEC-0007", "GABRB3 — GABA-A receptor → inhibitory tone"),
    ("GABRA3",   "MEC-0007", "GABRA3 — GABA-A receptor"),
    ("GABRB2",   "MEC-0007", "GABRB2 — GABA-A receptor"),
    # Calcium / glutamate-NMDA homeostasis
    ("GRIN2B",   "MEC-0020", "NMDAR Ca2+ permeability"),
    ("GRIN1",    "MEC-0020", "NMDAR obligate subunit"),
    ("CACNA1C",  "MEC-0020", "CaV1.2 — L-type Ca2+ channel"),
    # BDNF / neurotrophin signaling
    ("BDNF",     "MEC-0028", "BDNF — direct"),
    ("NTRK2",    "MEC-0028", "TrkB — BDNF receptor"),
    # Folate metabolism
    ("FOLR1",    "MEC-0003", "FOLR1 — folate transporter, methylation cycle"),
    ("MTHFR",    "MEC-0003", "MTHFR — folate cycle bottleneck"),
    ("MTRR",     "MEC-0003", "MTRR — methionine synthase reductase"),
    # Mitochondrial function
    ("POLG",     "MEC-0010", "POLG — mtDNA polymerase"),
    ("SURF1",    "MEC-0010", "SURF1 — complex IV assembly"),
]
pass3 = []
for sym, mid, rationale in GENE_TO_MEC:
    g = gene_by_symbol.get(sym)
    if not g:
        print(f"  PASS 3 skip: {sym} not in gene catalog")
        continue
    if (g["id"], mid) in gme_pairs:
        continue
    pass3.append({
        "gene_id": g["id"],
        "mechanism_id": mid,
        "relation_type": "participates_in",
        "polarity": "supporting",
        "rationale": rationale,
    })
print(f"PASS 3: {len(pass3)} specific gene → mechanism edges")

# --------------------------------------------------------------------------
# Write proposal CSVs
# --------------------------------------------------------------------------
PROP.mkdir(exist_ok=True)

# Pass 1: gene_hypothesis_edges proposal
ghe_fields = ["id","gene_id","hypothesis_id","relation_type","polarity",
              "evidence_for_count","evidence_against_count",
              "evidence_strength_aggregate","context_scope","status",
              "created_at","last_updated","rationale"]
with open(PROP / "proposed_gene_hypothesis_edges.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=ghe_fields); w.writeheader()
    for i, r in enumerate(pass1, 1):
        w.writerow({"id": f"PGHE-{i:05d}", **r,
                    "evidence_for_count": "",
                    "evidence_against_count": "",
                    "evidence_strength_aggregate": "0.0",
                    "context_scope": "",
                    "status": "proposed",
                    "created_at": NOW, "last_updated": NOW})

# Pass 2: gene_phenotype_edges proposal
gpe_fields = ["id","gene_id","phenotype_id","relation_type","polarity",
              "evidence_for_count","evidence_against_count",
              "evidence_strength_aggregate","context_scope","status",
              "created_at","last_updated","rationale"]
with open(PROP / "proposed_gene_phenotype_edges.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=gpe_fields); w.writeheader()
    for i, r in enumerate(pass2, 1):
        w.writerow({"id": f"PGPE-{i:05d}", **r,
                    "evidence_for_count": "", "evidence_against_count": "",
                    "evidence_strength_aggregate": "0.0",
                    "context_scope": "", "status": "proposed",
                    "created_at": NOW, "last_updated": NOW})

# Pass 3: gene_mechanism_edges proposal
gme_fields = ["id","gene_id","mechanism_id","relation_type","polarity",
              "evidence_for_count","evidence_against_count",
              "evidence_strength_aggregate","context_scope","status",
              "created_at","last_updated","rationale"]
with open(PROP / "proposed_gene_mechanism_edges.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=gme_fields); w.writeheader()
    for i, r in enumerate(pass3, 1):
        w.writerow({"id": f"PGME-{i:05d}", **r,
                    "evidence_for_count": "", "evidence_against_count": "",
                    "evidence_strength_aggregate": "0.0",
                    "context_scope": "", "status": "proposed",
                    "created_at": NOW, "last_updated": NOW})

print()
print(f"Total new gene-layer edges proposed: {len(pass1)+len(pass2)+len(pass3)}")
print(f"  proposed_gene_hypothesis_edges.csv: {len(pass1)}")
print(f"  proposed_gene_phenotype_edges.csv:  {len(pass2)}")
print(f"  proposed_gene_mechanism_edges.csv:  {len(pass3)}")
