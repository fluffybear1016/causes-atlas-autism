#!/usr/bin/env python3
"""Add Honda 2005 PMID 15877763 — Japan MMR-withdrawal natural experiment.

Honda H, Shimizu Y, Rutter M. 'No effect of MMR withdrawal on the incidence
of autism: a total population study.' J Child Psychol Psychiatry. 2005.

This is uniquely powerful because:
  - Japan WITHDREW MMR in 1993 due to aseptic meningitis (Urabe strain)
  - Switched to single-component vaccines
  - Honda et al. tracked autism in Yokohama before and after withdrawal
  - Autism rates CONTINUED TO RISE despite no MMR
  - Direct natural-experiment refutation of MMR-causes-autism for HYP-0068

Strength: high (peer-reviewed, total population, natural experiment design).
Direction: NEGATIVE for MMR causation hypotheses.
"""
import csv, datetime as dt, json, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NOW = dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')

# Fetch Honda 2005 metadata via eutils
EUTILS = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils'
def http(url):
    req = urllib.request.Request(url, headers={'User-Agent':'causes-atlas/1.0'})
    with urllib.request.urlopen(req, timeout=20) as r: return r.read().decode()

abstract_text = http(f"{EUTILS}/efetch.fcgi?db=pubmed&id=15877763&rettype=abstract&retmode=text")
print(abstract_text[:1500])
print("---")

# Source SRC-001421
new_source = {
    "id": "SRC-001421",
    "type": "study",
    "platform": "pubmed",
    "external_id": "15877763",
    "title": "No effect of MMR withdrawal on the incidence of autism: a "
             "total population study (Honda H, Shimizu Y, Rutter M; "
             "J Child Psychol Psychiatry 2005)",
    "url": "https://pubmed.ncbi.nlm.nih.gov/15877763/",
    "date_published": "2005-06-01",
    "date_ingested": NOW,
    "study_design": "natural_experiment",
    "sample_size": "31,426",
    "model_system": "human_pediatric_total_population",
    "raw_metadata": json.dumps({
        "doi": "10.1111/j.1469-7610.2005.01425.x",
        "year": 2005,
        "authors": "Honda H, Shimizu Y, Rutter M",
        "journal": "Journal of Child Psychology and Psychiatry",
        "design": "total_population_natural_experiment",
        "key_finding": "Japan withdrew MMR in 1993; autism cumulative incidence in "
                       "Yokohama continued to rise despite no MMR exposure in birth "
                       "cohorts after 1993. Direct refutation of MMR causal role "
                       "in population autism trends.",
        "peer_reviewed": True,
    }),
    "notes": "Peer-reviewed natural-experiment design. Strongest available "
             "epidemiological refutation of HYP-0068 (MMR-causes-autism).",
}

new_fragment = {
    "id": "EVD-001421",
    "source_id": "SRC-001421",
    "fragment_type": "result",
    "text_excerpt": (
        "Honda et al. 2005 (J Child Psychol Psychiatry, PMID 15877763): "
        "Yokohama City total-population autism incidence study (n=31,426 "
        "children). Japan withdrew MMR in 1993 due to aseptic meningitis "
        "from the Urabe mumps strain and replaced it with single-component "
        "measles, mumps, and rubella vaccines. Cumulative incidence of "
        "autism by age 7 in birth cohorts BEFORE MMR withdrawal: rising. "
        "AFTER MMR withdrawal (zero MMR exposure): incidence CONTINUED to "
        "rise. Significant up-trend in cumulative incidence both with and "
        "without MMR exposure. Conclusions: 'The significance of this "
        "finding is that MMR vaccination is most unlikely to be a main "
        "cause of ASD, that it cannot explain the rise over time in the "
        "incidence of ASD, and that withdrawal of MMR in countries where "
        "it is still being used cannot be expected to lead to a reduction "
        "in the incidence of ASD.'"
    ),
    "structured_payload": json.dumps({
        "outcome": "Cumulative incidence of autism by age 7",
        "effect_size": "Rising trend continued post-MMR-withdrawal",
        "p_value": "<0.0001 for upward trend",
        "design": "total_population_natural_experiment",
        "is_secondary_literature": False,
        "primary": True,
    }),
    "effect_direction": "negative",
    "strength_score": 0.55,  # natural experiment + total population — high
    "extraction_method": "manual",
    "extraction_confidence": 0.95,
    "date_extracted": NOW,
    "notes": "Natural-experiment design with total-population capture is "
             "uniquely powerful for the MMR-causation question. "
             "Strength_score 0.55 — one of the highest among null sources.",
}

# Wire to HYP-0068 (MMR specifically) and HYP-0044 (childhood schedule)
new_links = [
    ("EVL-001648", "EVD-001421", "hypothesis", "HYP-0068", "negative",
     "Direct natural-experiment refutation: MMR removal didn't reduce ASD"),
    ("EVL-001649", "EVD-001421", "hypothesis", "HYP-0044", "negative",
     "Population-scale evidence one major schedule change didn't shift ASD trend"),
]

# Append
def append_to(path, fields, rows_to_add, id_field='id'):
    rows = list(csv.DictReader(open(path)))
    existing_ids = {r[id_field] for r in rows}
    added = 0
    for r in rows_to_add:
        if r[id_field] in existing_ids: continue
        rows.append({f: r.get(f, '') for f in fields})
        added += 1
    with open(path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
    return added

link_rows = []
for lid, fid, ttype, tid, direction, note in new_links:
    link_rows.append({
        "id": lid, "evidence_fragment_id": fid, "claim_id": "",
        "target_type": ttype, "target_id": tid,
        "effect_direction": direction, "weight": "", "context_scope": "",
        "created_at": NOW, "notes": note,
    })

for d in [ROOT/"v2.0_scored", ROOT/"v2.0.1_expanded"]:
    s_fields = list(csv.DictReader(open(d/"sources.csv")).fieldnames)
    f_fields = list(csv.DictReader(open(d/"evidence_fragments.csv")).fieldnames)
    l_fields = list(csv.DictReader(open(d/"evidence_links.csv")).fieldnames)
    n_s = append_to(d/"sources.csv", s_fields, [new_source])
    n_f = append_to(d/"evidence_fragments.csv", f_fields, [new_fragment])
    n_l = append_to(d/"evidence_links.csv", l_fields, link_rows)
    print(f"{d.name}: +{n_s} sources, +{n_f} fragments, +{n_l} links")
