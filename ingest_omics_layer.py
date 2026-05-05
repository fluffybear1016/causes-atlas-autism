#!/usr/bin/env python3
"""Ingest the omics-layer source corpus into the atlas.

Adds 8 verified sources covering:
  - 5 multi-omics causal pathway primary studies (verified PMIDs)
  - 3 multi-omics methodology / synthesis / cautionary papers

Plus evidence_links wiring each to relevant atlas entities.

All PMIDs verified against PubMed esearch+esummary before commit.
"""
import csv, datetime as dt, json, urllib.request, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NOW = dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

def http(url):
    req = urllib.request.Request(url, headers={"User-Agent": "causes-atlas/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r: return r.read().decode()

# Verified PMIDs and design classifications
SRC_DEFS = [
    ("SRC-001455", "39870302", "study", "multiomics_observational",
     "Osama 2025 J Adv Res — integrative multi-omics (16S + metaproteomics + metabolomics + host fecal proteome) in severely autistic children. Identifies microbial driver taxa (Tyzzerella, Blautia, Klebsiella), differentially abundant bacterial enzymes from Bifidobacterium and Klebsiella, 25 altered metabolites including BBB-crossing compounds (glutamate, DOPAC), and host proteome changes (KLK1, TTR up; MPO, MUC13 down) consistent with neuroinflammation + barrier disruption. Cleanest current example of a multi-omics-supported gut→macromolecule→metabolite→neuroimmune pathway. Causality argued from cross-layer consistency, not formal MR.",
     "0.55"),

    ("SRC-001456", "40400531", "study", "mendelian_randomization",
     "Wang 2025 R Soc Open Sci — two-sample MR establishing genetically-instrumented causal chain: gut microbiota → blood metabolites → ASD. 15 taxa causally associated with ASD; 52 metabolites causally associated; mediation analysis identifies 9 metabolites mediating microbiota→ASD effects (e.g., 1-methyl-5-imidazoleacetate mediates ~12% of A. fermentans protective effect; pyridoxate mediates ~12% of Lachnospirales effect). Methodologically strong: explicit causal inference framework with sensitivity tests excluding pleiotropy. Limited to European cohorts.",
     "0.60"),

    ("SRC-001457", "41160232", "study", "multiomics_genomics",
     "Liao 2025 AMB Express — cross-tissue multi-omics integrating ASD GWAS (12.6M SNPs, 47 novel risk loci) + multi-region eQTL + epigenetic + microbiome data. Identifies cross-scale axis: genetic variation → epigenetic regulation → neuronal cell function. Strongest eQTL enrichment in cerebral cortex. Forward MR on 473 gut taxa identifies 24 with causal ASD associations. Tight junction pathway emerges as cross-tissue mechanism connecting genetic risk and microbiota.",
     "0.55"),

    ("SRC-001458", "40373085", "study", "multiomics_replication",
     "Liu 2025 PLOS ONE — multi-omics gene-prioritization analysis identifies SOX7 as causally implicated in ASD. Multi-dataset replication: 5 candidate genes from primary dataset, only SOX7 replicates in independent dataset. Significant associations in cerebellar hemisphere, hypothalamus, spinal cord. SOX7 is a Wnt-signaling transcription factor — ties into broader Wnt/neurodevelopmental pathway in ASD. Combines GWAS + RNA-seq + GTEx eQTL.",
     "0.40"),

    ("SRC-001459", "41421350", "study", "multiomics_microbial_genomics",
     "Sun 2026 Cell Reports Medicine — integrative multi-omics revealing microbial GENOMIC variants (not just composition) driving altered host-microbe interactions in ASD. Strain-level metagenomics + host omics. Shifts the field from 'microbiome composition' to 'microbiome strain genetics' as causal layer. Identifies bacterial genomic variants that change microbial functional capacity, which alters host pathway interactions, which contributes to ASD-relevant phenotypes.",
     "0.50"),

    ("SRC-001460", "40076702", "study", "systems_biology_methodology",
     "Remori 2025 IJMS — systems-biology framework for prioritizing ASD genes from large/noisy multi-omics datasets. Starts from high-confidence SFARI genes, expands through PPI graphs to derive ASD-enriched gene networks. Methodologically important because it formalizes the 'genome-anchored network' approach that anchors most multi-omics ASD work today.",
     "0.45"),

    ("SRC-001461", "39600653", "review", "literature_mining_synthesis",
     "Mongad 2024 Front Neurosci — comprehensive literature-mining review of multi-omics ASD studies. Maps decade-scale trends in which omics combinations are being used and which biological themes (synaptic, immune, mitochondrial, microbiome) emerge most consistently across integrative analyses. Field-level bibliometric synthesis.",
     "0.35"),

    ("SRC-001462", "37410704", "review", "methodology_critique",
     "Chicco 2023 PLOS Comput Biol — 'Ten quick tips for avoiding pitfalls in multi-omics data integration analyses.' Methodological cautionary review. Critical for interpreting any multi-omics ASD finding: warns that integration alone produces correlation; causal claims require explicit confounder handling, directionality tests (MR or perturbation), and biological validation. Underlies CLAUDE.md §1 + §9 epistemic principles for the omics layer.",
     "0.45"),
]

# Verify PMIDs once more before commit
print("Final PMID re-verification before commit…")
ids = [d[1] for d in SRC_DEFS]
batch_meta = json.loads(http(f"{EUTILS}/esummary.fcgi?db=pubmed&retmode=json&id={','.join(ids)}"))
verified_meta = {}
for d in SRC_DEFS:
    sid, pmid = d[0], d[1]
    r = batch_meta.get("result", {}).get(pmid, {})
    if not r.get("title"):
        print(f"  ✗ {sid} PMID {pmid}: NOT FOUND — aborting"); exit(1)
    verified_meta[pmid] = {
        "title": r.get("title", ""),
        "year": r.get("pubdate","")[:4],
        "journal": r.get("source",""),
        "authors": [a.get("name","") for a in r.get("authors",[])[:5]],
    }
    print(f"  ✓ {sid} PMID {pmid}: {r.get('title','')[:80]}")

# Build sources
new_sources = []
for sid, pmid, stype, design, descr, _strength in SRC_DEFS:
    m = verified_meta[pmid]
    new_sources.append({
        "id": sid, "type": stype, "platform": "pubmed", "external_id": pmid,
        "title": m["title"],
        "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
        "date_published": f"{m['year']}-01-01" if m["year"] else "",
        "date_ingested": NOW,
        "study_design": design,
        "sample_size": "",
        "model_system": "human",
        "raw_metadata": json.dumps({
            "pmid": pmid, "year": m["year"], "journal": m["journal"],
            "authors": m["authors"], "verified_against_pubmed": True,
            "ingested_via": "ingest_omics_layer.py",
        }),
        "notes": descr,
    })

# Build evidence fragments + links
new_fragments = []
new_links = []
frag_id = 1456  # next free EVD
link_id = 1740  # next free EVL

# (src_id, strength, frag_text, [(target_type, target_id, note), ...])
ENTITY_LINKS = {
    "SRC-001455": ("0.55",
                   "Multi-omics gut→brain causal chain: dysbiosis → microbial protein/enzyme shift → BBB-crossing metabolites → host immune/barrier protein dysregulation → neuroinflammation. Argued via cross-layer consistency.",
                   [("hypothesis", "HYP-0008", "Maternal/early immune activation downstream signature"),
                    ("hypothesis", "HYP-0044", "Multi-omics framing relevant to vaccine-immune cluster as one possible Hit-2 trigger"),
                    ("phenotype", "PHE-0004", "GI microbiome dysbiosis phenotype primary"),
                    ("mechanism", "MEC-0010", "Mitochondrial / metabolic mechanism mapping"),
                    ("intervention", "INT-0076", "FMT modifies the entire upstream layer"),
                    ("intervention", "INT-0025", "Probiotic restoration of upstream layer")]),
    "SRC-001456": ("0.60",
                   "Two-sample Mendelian randomization establishes formal genetically-instrumented causal chain: gut microbiota → blood metabolites → ASD, with mediation effect sizes. Highest-rigor causal-inference paper in current ASD multi-omics literature.",
                   [("hypothesis", "HYP-0008", "Microbiota-immune-CDR axis"),
                    ("hypothesis", "HYP-0028", "Genetic-instrument anchored"),
                    ("phenotype", "PHE-0004", "GI microbiome dysbiosis directly causal"),
                    ("intervention", "INT-0076", "FMT alters microbiota in causally-identified taxa")]),
    "SRC-001457": ("0.55",
                   "Cross-tissue multi-omics axis: genetic variation → epigenetic regulation → cortical eQTL → neuronal cell function. 47 novel ASD risk loci identified. Tight-junction pathway as gut-brain bridge. Forward MR on 473 gut taxa.",
                   [("hypothesis", "HYP-0028", "Inherited polygenic + cross-tissue regulatory chain"),
                    ("hypothesis", "HYP-0008", "Tight junction barrier-immune mechanism"),
                    ("phenotype", "PHE-0004", "GI dysbiosis MR-causal"),
                    ("mechanism", "MEC-0010", "Mitochondrial cross-tissue convergence")]),
    "SRC-001458": ("0.40",
                   "Multi-omics gene-prioritization replication identifies SOX7 (Wnt signaling transcription factor) as causally implicated in ASD. Cross-dataset replication strengthens the finding.",
                   [("hypothesis", "HYP-0028", "Specific causal gene identified via multi-omics replication"),
                    ("mechanism", "MEC-0020", "Wnt signaling intersects with synaptic / NMDA layer")]),
    "SRC-001459": ("0.50",
                   "Multi-omics microbial GENOMIC variants (strain-level) drive altered host-microbe interactions. Shifts gut-brain causation from 'microbiome composition' to 'microbiome strain genetics'.",
                   [("hypothesis", "HYP-0008", "Strain-genetic basis for individual-level susceptibility"),
                    ("phenotype", "PHE-0004", "Strain-resolved microbiome dysbiosis"),
                    ("intervention", "INT-0076", "FMT targets strain-level microbiome"),
                    ("intervention", "INT-0025", "Probiotic strain selection requires strain-level data")]),
    "SRC-001460": ("0.45",
                   "Systems-biology methodology paper — anchoring multi-omics analyses on high-confidence SFARI genes via PPI network expansion. The methodological backbone for genome-anchored multi-omics ASD work.",
                   [("hypothesis", "HYP-0028", "SFARI-anchored network framework")]),
    "SRC-001461": ("0.35",
                   "Bibliometric/literature-mining synthesis of decade-scale multi-omics ASD trends. Field-level meta-evidence rather than primary findings.",
                   [("hypothesis", "HYP-0028", "Field-level synthesis"),
                    ("hypothesis", "HYP-0006", "Mitochondrial theme recurrence in multi-omics literature"),
                    ("hypothesis", "HYP-0008", "Immune theme recurrence")]),
    "SRC-001462": ("0.45",
                   "Methodological cautionary review on multi-omics integration pitfalls. Critical for interpreting any multi-omics ASD finding. Warns: integration alone is correlational; causal claims need confounder handling + directionality tests + biological validation. Operationalizes CLAUDE.md §1+§9 for the omics layer.",
                   [("hypothesis", "HYP-0028", "Methodology constraint on multi-omics ASD claims")]),
}

for sid, (strength, frag_text, target_links) in ENTITY_LINKS.items():
    eid = f"EVD-{frag_id:06d}"
    new_fragments.append({
        "id": eid, "source_id": sid, "fragment_type": "result",
        "text_excerpt": frag_text,
        "structured_payload": json.dumps({
            "primary": True, "is_secondary_literature": False,
            "domain": "multi_omics", "verified_against_pubmed": True,
        }),
        "effect_direction": "positive",
        "strength_score": strength, "extraction_method": "manual",
        "extraction_confidence": "0.95",
        "date_extracted": NOW,
        "notes": "Multi-omics layer evidence per ingest_omics_layer.py.",
    })
    frag_id += 1
    for ttype, tid, note in target_links:
        new_links.append({
            "id": f"EVL-{link_id:06d}",
            "evidence_fragment_id": eid, "claim_id": "",
            "target_type": ttype, "target_id": tid,
            "effect_direction": "positive", "weight": "", "context_scope": "",
            "created_at": NOW, "notes": note,
        })
        link_id += 1

# Append helper
def append(path, fields, rows_to_add, id_field="id"):
    rows = list(csv.DictReader(open(path)))
    existing = {r[id_field] for r in rows}
    added = 0
    for r in rows_to_add:
        if r[id_field] in existing: continue
        out = {f: r.get(f, "") for f in fields}
        rows.append(out); added += 1
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
    return added

print()
for d in [ROOT/"v2.0_scored", ROOT/"v2.0.1_expanded"]:
    print(f"\n{d.name}:")
    src_fields = list(csv.DictReader(open(d/"sources.csv")).fieldnames)
    n = append(d/"sources.csv", src_fields, new_sources)
    print(f"  sources.csv: +{n}")
    frag_fields = list(csv.DictReader(open(d/"evidence_fragments.csv")).fieldnames)
    n = append(d/"evidence_fragments.csv", frag_fields, new_fragments)
    print(f"  evidence_fragments.csv: +{n}")
    link_fields = list(csv.DictReader(open(d/"evidence_links.csv")).fieldnames)
    n = append(d/"evidence_links.csv", link_fields, new_links)
    print(f"  evidence_links.csv: +{n}")

print("\nDone. Next: re-run scoring, derive MPE, rebuild vault.")
