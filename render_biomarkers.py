#!/usr/bin/env python3
"""Render BIO-NNNN biomarker pages + biomarkers/INDEX.md into the vault.

Runs after build_vault.py. Reads v2.0_scored/biomarkers.csv + edge tables.
Writes one .md per biomarker plus a master INDEX.md categorized.
"""
import csv, json, re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent
SRC_DIR = ROOT / "v2.0_scored"
VAULT_BIO = ROOT / "vault" / "biomarkers"
VAULT_BIO.mkdir(parents=True, exist_ok=True)

# Load
biomarkers = list(csv.DictReader(open(SRC_DIR/"biomarkers.csv")))
bme = list(csv.DictReader(open(SRC_DIR/"biomarker_mechanism_edges.csv")))
bpe = list(csv.DictReader(open(SRC_DIR/"biomarker_phenotype_edges.csv")))
bie = list(csv.DictReader(open(SRC_DIR/"biomarker_intervention_edges.csv")))
bhe = list(csv.DictReader(open(SRC_DIR/"biomarker_hypothesis_edges.csv")))

# Build label maps for atlas entities
def label_map(path, name_field="name"):
    out = {}
    for r in csv.DictReader(open(path)):
        out[r["id"]] = r.get(name_field, "")
    return out

mec_label = label_map(SRC_DIR/"mechanisms.csv")
phe_label = label_map(SRC_DIR/"phenotypes.csv")
int_label = label_map(SRC_DIR/"interventions.csv")
hyp_label = label_map(SRC_DIR/"hypotheses.csv")

# Edge maps
bme_by_bio = defaultdict(list)
for r in bme: bme_by_bio[r["biomarker_id"]].append(r)
bpe_by_bio = defaultdict(list)
for r in bpe: bpe_by_bio[r["biomarker_id"]].append(r)
bie_by_bio = defaultdict(list)
for r in bie: bie_by_bio[r["biomarker_id"]].append(r)
bhe_by_bio = defaultdict(list)
for r in bhe: bhe_by_bio[r["biomarker_id"]].append(r)

def san(s):
    """Filename-safe version."""
    s = re.sub(r'[\\/:*?"<>|\[\]#^/]', "_", s or "")
    return re.sub(r"\s+", " ", s).strip()[:80]

# Per-biomarker pages
for b in biomarkers:
    bid = b["id"]
    fname = f"{bid} {san(b['name'])}.md"
    body = []
    front = {
        "id": bid, "type": "biomarker",
        "name": b["name"], "category": b["category"],
        "subcategory": b["subcategory"], "sample_type": b["sample_type"],
        "units": b["units"], "test_availability": b["test_availability"],
    }
    body.append("---")
    for k, v in front.items():
        sv = str(v) if v is not None else ""
        if '"' in sv or "\n" in sv:
            sv = json.dumps(sv)
        body.append(f"{k}: {sv}")
    body.append("---\n")
    body.append(f"# {bid} — {b['name']}\n")

    if b.get("category"):
        body.append(f"**Category:** {b['category']}{' / ' + b['subcategory'] if b['subcategory'] else ''}\n")

    if b["sample_type"]:
        body.append(f"**Sample type:** {b['sample_type']}  ")
    if b["units"]:
        body.append(f"**Units:** {b['units']}  ")
    if b["reference_low"] or b["reference_high"]:
        body.append(f"**Reference range:** {b['reference_low']}–{b['reference_high']}  ")
    if b["reference_optimal_low"] or b["reference_optimal_high"]:
        body.append(f"**Optimal range:** {b['reference_optimal_low']}–{b['reference_optimal_high']}  ")
    if b["age_caveat"]:
        body.append(f"**Age caveat:** {b['age_caveat']}  ")
    body.append("")

    if b["what_it_measures"]:
        body.append(f"**What it measures:** {b['what_it_measures']}\n")
    if b["elevated_means"]:
        body.append(f"**Elevated means:** {b['elevated_means']}\n")
    if b["low_means"]:
        body.append(f"**Low means:** {b['low_means']}\n")
    if b["interpretation_summary"]:
        body.append(f"**Interpretation:** {b['interpretation_summary']}\n")
    if b["snp_dependence"]:
        body.append(f"**SNP dependence:** {b['snp_dependence']}\n")

    if b["test_availability"] or b["clia_status"] or b["lab_options"]:
        body.append("\n## Test logistics")
        if b["test_availability"]: body.append(f"- Availability: {b['test_availability']}")
        if b["clia_status"]: body.append(f"- CLIA: {b['clia_status']}")
        if b["lab_options"]: body.append(f"- Labs: {b['lab_options']}")
        if b["test_cost_usd_low"] or b["test_cost_usd_high"]:
            body.append(f"- Cost: ${b['test_cost_usd_low']}–${b['test_cost_usd_high']} USD")
        if b["turnaround_days"]: body.append(f"- Turnaround: {b['turnaround_days']} days")
        body.append("")

    # Atlas connections
    body.append("## Atlas connections\n")
    if bme_by_bio[bid]:
        body.append("**Mechanisms indicated:**")
        for r in bme_by_bio[bid]:
            mid = r["mechanism_id"]; ml = mec_label.get(mid, "")
            body.append(f"- [[{mid} {ml}]] — {r.get('relationship_type','')}")
    if bpe_by_bio[bid]:
        body.append("\n**Phenotypes stratified:**")
        for r in bpe_by_bio[bid]:
            pid = r["phenotype_id"]; pl = phe_label.get(pid, "")
            body.append(f"- [[{pid} {pl}]] — {r.get('relationship_type','')}")
    if bie_by_bio[bid]:
        body.append("\n**Interventions modulated:**")
        for r in bie_by_bio[bid]:
            iid = r["intervention_id"]; il = int_label.get(iid, "")
            body.append(f"- [[{iid} {il}]] — {r.get('relationship_type','')} ({r.get('direction','')})")
    if bhe_by_bio[bid]:
        body.append("\n**Hypotheses tested:**")
        for r in bhe_by_bio[bid]:
            hid = r["hypothesis_id"]; hl = hyp_label.get(hid, "")
            body.append(f"- [[{hid} {hl}]] — {r.get('relationship_type','')}")

    if b["key_pmids"]:
        body.append("\n## Primary literature\n")
        for pmid in b["key_pmids"].split(","):
            pmid = pmid.strip()
            if pmid:
                body.append(f"- PMID [{pmid}](https://pubmed.ncbi.nlm.nih.gov/{pmid}/)")

    if b["notes"]:
        body.append(f"\n## Notes\n\n{b['notes']}")

    (VAULT_BIO/fname).write_text("\n".join(body))

print(f"Wrote {len(biomarkers)} biomarker pages to {VAULT_BIO}/")

# Build INDEX.md categorized
idx = ["---", "id: BIOMARKERS_INDEX", "type: section_index",
       "purpose: Auto-generated catalog of all 164 biomarkers in the atlas",
       "---", "", "# 🧪 Biomarkers — Atlas Catalog", "",
       f"**{len(biomarkers)} biomarkers across {len(set(b['category'] for b in biomarkers))} categories.**",
       "", "For category overviews + decision-trees see [[topics/biomarkers/00_BIOMARKERS_INDEX]].",
       ""]

by_cat = defaultdict(list)
for b in biomarkers:
    by_cat[b["category"]].append(b)

cat_order = [
    "methylation_cycle", "folate_receptor", "mitochondrial", "oxidative_stress",
    "oat_microbial", "oat_neurotransmitter", "immune_inflammatory", "mast_cell",
    "pans_pandas", "heavy_metals", "environmental_chemicals", "maternal_parental",
    "trace_minerals", "pyroluria", "fatty_acids", "gi_barrier", "endocrine",
    "chronic_infection", "autoimmune",
    "brain_neuroimaging", "brain_electrophysiology", "brain_eye_autonomic",
    "brain_csf", "brain_peripheral",
    "heat_shock", "endocannabinoid", "genetic_snp",
]

CAT_PRETTY = {
    "methylation_cycle": "Methylation Cycle",
    "folate_receptor": "Folate Receptor",
    "mitochondrial": "Mitochondrial",
    "oxidative_stress": "Oxidative Stress",
    "oat_microbial": "OAT Microbial Metabolites",
    "oat_neurotransmitter": "OAT Neurotransmitter Metabolites",
    "immune_inflammatory": "Immune / Inflammatory",
    "mast_cell": "Mast Cell Activation",
    "pans_pandas": "PANS / PANDAS",
    "heavy_metals": "Heavy Metals / Toxicants",
    "environmental_chemicals": "Environmental Chemicals",
    "maternal_parental": "Maternal / Parental",
    "trace_minerals": "Trace Minerals",
    "pyroluria": "Pyroluria",
    "fatty_acids": "Fatty Acids",
    "gi_barrier": "GI / Barrier Function",
    "endocrine": "Endocrine / Hormonal",
    "chronic_infection": "Chronic Infection Panel",
    "autoimmune": "Autoimmune (broader)",
    "brain_neuroimaging": "🧠 Brain — Neuroimaging",
    "brain_electrophysiology": "🧠 Brain — Electrophysiology",
    "brain_eye_autonomic": "🧠 Brain — Eye Tracking + Autonomic",
    "brain_csf": "🧠 Brain — CSF",
    "brain_peripheral": "🧠 Brain — Peripheral (BDNF / S100β / GFAP / NfL)",
    "heat_shock": "Heat Shock Response",
    "endocannabinoid": "Endocannabinoid System",
    "genetic_snp": "Genetic SNPs",
}
for cat in cat_order:
    if cat not in by_cat: continue
    pretty = CAT_PRETTY.get(cat, cat.replace("_", " ").title())
    idx.append(f"## {pretty}")
    idx.append("")
    for b in sorted(by_cat[cat], key=lambda x: x["id"]):
        idx.append(f"- [[{b['id']} {san(b['name'])}|{b['id']} {b['name']}]]")
    idx.append("")

(VAULT_BIO/"INDEX.md").write_text("\n".join(idx))
print(f"Wrote INDEX.md")
