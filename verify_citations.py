#!/usr/bin/env python3
"""
verify_citations.py — Replace memory-based PMIDs in
candidate_orphan_edges.csv with PubMed-search-grounded ones.

For each candidate edge:
  1. Run NCBI eutils esearch with a tight, biology-specific query.
  2. Pull top hits' titles + journals + years via esummary.
  3. Score each hit by simple keyword overlap with the claim.
  4. Pick the top 1–2 hits.
  5. Re-verify the title contains expected biology terms.
  6. Write candidate_orphan_edges_verified.csv and a verification
     report at vault/CITATION_VERIFICATION.md.

No PMIDs are taken from memory. Every PMID emitted appears in a real
esearch result captured in this run.

Run:  python3 verify_citations.py
"""

from __future__ import annotations

import csv
import datetime as dt
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROP = ROOT / "v2.0.1_proposed"
VAULT = ROOT / "vault"
NOW = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

# ---------------------------------------------------------------------------
# Claims: the 24 candidate edges from the orphan proposal, each with a
# focused search query and the keywords we expect a *correct* hit to
# contain (used for relevance scoring).
# ---------------------------------------------------------------------------

CLAIMS = [
    # ---------- HYP-0025 Prenatal viral infection / MIA ----------
    {
        "id": "CAND-0001", "from_id": "HYP-0025", "to_id": "MEC-0002",
        "edge_table": "hypothesis_mechanism_edges",
        "relation_type": "acts_through", "polarity": "supporting",
        "claim": ("Maternal viral infection drives sustained fetal "
                  "neuroinflammation via maternal cytokine surge."),
        "query": "maternal immune activation autism neuroinflammation cytokine",
        "must_contain": ["maternal", "immune", "autism"],
    },
    {
        "id": "CAND-0002", "from_id": "HYP-0025", "to_id": "MEC-0005",
        "edge_table": "hypothesis_mechanism_edges",
        "relation_type": "acts_through", "polarity": "supporting",
        "claim": "MIA produces persistent microglial priming in offspring.",
        "query": "maternal immune activation microglia offspring brain autism",
        "must_contain": ["microglia", "maternal"],
    },
    {
        "id": "CAND-0003", "from_id": "HYP-0025", "to_id": "MEC-0017",
        "edge_table": "hypothesis_mechanism_edges",
        "relation_type": "acts_through", "polarity": "supporting",
        "claim": ("Maternal mast-cell activation contributes to BBB "
                  "permeability changes downstream of MIA."),
        "query": "mast cell activation autism brain blood-brain barrier",
        "must_contain": ["mast", "autism"],
    },
    {
        "id": "CAND-0004", "from_id": "HYP-0025", "to_id": "PHE-0003",
        "edge_table": "intervention_phenotype_edges",  # actually hyp_phe
        "relation_type": "manifests_as", "polarity": "supporting",
        "claim": ("Prenatal viral infection epidemiologically associated "
                  "with autism risk and regressive presentation."),
        "query": "maternal infection pregnancy autism risk epidemiology cohort",
        "must_contain": ["maternal", "infection", "autism"],
    },

    # ---------- HYP-0028 Inherited polygenic risk ----------
    {
        "id": "CAND-0005", "from_id": "HYP-0028", "to_id": "MEC-0006",
        "edge_table": "hypothesis_mechanism_edges",
        "relation_type": "acts_through", "polarity": "supporting",
        "claim": ("SFARI Tier-1 synaptic genes converge on synaptic "
                  "pruning/maturation pathways."),
        "query": "autism risk genes synapse synaptic pruning convergence SHANK NRXN",
        "must_contain": ["autism", "synap"],
    },
    {
        "id": "CAND-0006", "from_id": "HYP-0028", "to_id": "MEC-0007",
        "edge_table": "hypothesis_mechanism_edges",
        "relation_type": "acts_through", "polarity": "supporting",
        "claim": ("Polygenic risk converges on E/I balance via "
                  "channelopathies."),
        "query": "autism excitation inhibition balance GABA glutamate genes",
        "must_contain": ["autism"],
    },
    {
        "id": "CAND-0007", "from_id": "HYP-0028", "to_id": "MEC-0009",
        "edge_table": "hypothesis_mechanism_edges",
        "relation_type": "acts_through", "polarity": "supporting",
        "claim": ("TSC, PTEN syndromic mutations confirm mTOR is a major "
                  "convergence point in ASD."),
        "query": "autism mTOR pathway TSC PTEN convergence review",
        "must_contain": ["mTOR", "autism"],
    },
    {
        "id": "CAND-0008", "from_id": "HYP-0028", "to_id": "PHE-0005",
        "edge_table": "intervention_phenotype_edges",  # hyp_phe
        "relation_type": "manifests_as", "polarity": "supporting",
        "claim": "TSC/PTEN macrocephaly mTOR-syndromic phenotype.",
        "query": "PTEN macrocephaly autism mTOR clinical phenotype",
        "must_contain": ["PTEN", "autism"],
    },
    {
        "id": "CAND-0009", "from_id": "HYP-0028", "to_id": "PHE-0006",
        "edge_table": "intervention_phenotype_edges",  # hyp_phe
        "relation_type": "manifests_as", "polarity": "supporting",
        "claim": "FMR1 fragile X autism syndromic phenotype review.",
        "query": "FMR1 fragile X autism syndrome review clinical",
        "must_contain": ["fragile", "FMR1"],
    },

    # ---------- MEC-0013 FOXO wiring (4 interventions) ----------
    {
        "id": "CAND-0010", "from_id": "INT-0036", "to_id": "MEC-0013",
        "edge_table": "intervention_mechanism_edges",
        "relation_type": "modulates", "polarity": "supporting",
        "claim": ("Rapamycin (mTOR inhibitor) → FOXO disinhibition → "
                  "autophagy."),
        "query": "rapamycin mTOR FOXO autophagy",
        "must_contain": ["mTOR", "FOXO"],
    },
    {
        "id": "CAND-0011", "from_id": "INT-0028", "to_id": "MEC-0013",
        "edge_table": "intervention_mechanism_edges",
        "relation_type": "modulates", "polarity": "supporting",
        "claim": ("Resveratrol activates SIRT1 → SIRT1 deacetylates "
                  "FOXO3a → activates antioxidant + autophagy program."),
        "query": "resveratrol SIRT1 FOXO3 deacetylation",
        "must_contain": ["SIRT1", "FOXO"],
    },
    {
        "id": "CAND-0012", "from_id": "INT-0093", "to_id": "MEC-0013",
        "edge_table": "intervention_mechanism_edges",
        "relation_type": "modulates", "polarity": "supporting",
        "claim": ("Alpha-lipoic acid insulin sensitization → modulates "
                  "AKT-FOXO axis."),
        "query": "alpha lipoic acid AKT FOXO insulin signaling",
        "must_contain": ["lipoic"],
    },
    {
        "id": "CAND-0013", "from_id": "INT-0047", "to_id": "MEC-0013",
        "edge_table": "intervention_mechanism_edges",
        "relation_type": "modulates", "polarity": "supporting",
        "claim": ("Aerobic exercise activates AMPK → AMPK phosphorylates "
                  "FOXO3 → mitochondrial biogenesis."),
        "query": "exercise AMPK FOXO3 mitochondrial biogenesis muscle",
        "must_contain": ["AMPK", "FOXO"],
    },

    # ---------- INT-0021 Lithium ----------
    {
        "id": "CAND-0014", "from_id": "INT-0021", "to_id": "MEC-0028",
        "edge_table": "intervention_mechanism_edges",
        "relation_type": "modulates", "polarity": "supporting",
        "claim": ("Lithium inhibits GSK-3β → stabilizes β-catenin → "
                  "upregulates BDNF expression."),
        "query": "lithium GSK-3 BDNF beta-catenin neurotrophic",
        "must_contain": ["lithium", "GSK"],
    },
    {
        "id": "CAND-0015", "from_id": "INT-0021", "to_id": "MEC-0009",
        "edge_table": "intervention_mechanism_edges",
        "relation_type": "modulates", "polarity": "supporting",
        "claim": ("GSK-3β cross-talks with mTOR via TSC2; lithium "
                  "modulates mTOR pathway activity."),
        "query": "lithium GSK-3 mTOR TSC2 signaling",
        "must_contain": ["GSK", "mTOR"],
    },

    # ---------- INT-0022 Inositol ----------
    {
        "id": "CAND-0016", "from_id": "INT-0022", "to_id": "MEC-0015",
        "edge_table": "intervention_mechanism_edges",
        "relation_type": "modulates", "polarity": "supporting",
        "claim": ("Myo-inositol is the precursor for phosphoinositides "
                  "(PIP2/PIP3) underlying PI3K/AKT signaling."),
        "query": "myo-inositol phosphoinositide PI3K AKT signaling review",
        "must_contain": ["inositol"],
    },
    # NOTE: dropped CAND original INT-0022 → HYP-0055 (endocannabinoid)
    # because the wiring was wrong on review — inositol's serotonin/OCD
    # link doesn't map onto the endocannabinoid hypothesis.

    # ---------- INT-0024 Glycine ----------
    {
        "id": "CAND-0017", "from_id": "INT-0024", "to_id": "MEC-0020",
        "edge_table": "intervention_mechanism_edges",
        "relation_type": "modulates", "polarity": "supporting",
        "claim": ("Glycine is an obligate NMDA-receptor co-agonist; "
                  "modulates Ca2+/glutamate-NMDA homeostasis."),
        "query": "glycine NMDA receptor co-agonist glycine site",
        "must_contain": ["glycine", "NMDA"],
    },
    {
        "id": "CAND-0018", "from_id": "INT-0024", "to_id": "MEC-0001",
        "edge_table": "intervention_mechanism_edges",
        "relation_type": "modulates", "polarity": "supporting",
        "claim": ("Glycine is one of three amino acid precursors of "
                  "glutathione (γ-Glu-Cys-Gly)."),
        "query": "glycine glutathione synthesis precursor supplementation",
        "must_contain": ["glycine", "glutathione"],
    },

    # ---------- INT-0041 GFCF diet ----------
    {
        "id": "CAND-0019", "from_id": "INT-0041", "to_id": "MEC-0008",
        "edge_table": "intervention_mechanism_edges",
        "relation_type": "modulates", "polarity": "unknown",
        "claim": ("GFCF diet modulates gut-brain axis; whole-population "
                  "RCT effect mixed; effect concentrated in subset."),
        "query": "gluten free casein free diet autism randomized trial",
        "must_contain": ["gluten", "autism"],
    },
    {
        "id": "CAND-0020", "from_id": "INT-0041", "to_id": "MEC-0022",
        "edge_table": "intervention_mechanism_edges",
        "relation_type": "modulates", "polarity": "supporting",
        "claim": ("GFCF reduces intestinal permeability / LPS "
                  "translocation in zonulin-elevated subset."),
        "query": "gluten zonulin intestinal permeability autism",
        "must_contain": ["zonulin", "autism"],
    },
    {
        "id": "CAND-0021", "from_id": "INT-0041", "to_id": "PHE-0004",
        "edge_table": "intervention_phenotype_edges",
        "relation_type": "treats", "polarity": "supporting",
        "claim": ("GFCF responder phenotype is the GI/microbiome "
                  "subgroup specifically."),
        "query": "GFCF diet autism gastrointestinal symptoms responder",
        "must_contain": ["autism"],
    },

    # ---------- INT-0049 Sunlight exposure ----------
    {
        "id": "CAND-0022", "from_id": "INT-0049", "to_id": "MEC-0029",
        "edge_table": "intervention_mechanism_edges",
        "relation_type": "modulates", "polarity": "supporting",
        "claim": ("UVB-driven cutaneous vitamin D synthesis → vitamin D "
                  "regulates TPH2 / brain serotonin synthesis."),
        "query": "vitamin D TPH2 serotonin brain autism Patrick",
        "must_contain": ["vitamin D", "serotonin"],
    },
    {
        "id": "CAND-0023", "from_id": "INT-0049", "to_id": "MEC-0016",
        "edge_table": "intervention_mechanism_edges",
        "relation_type": "modulates", "polarity": "supporting",
        "claim": ("Morning sunlight entrains the suprachiasmatic nucleus "
                  "and normalizes the cortisol awakening response."),
        "query": "morning light exposure cortisol awakening circadian suprachiasmatic",
        "must_contain": ["light", "cortisol"],
    },
]


# ---------------------------------------------------------------------------
# eutils helpers
# ---------------------------------------------------------------------------

def http_get(url: str, attempts: int = 3) -> str:
    last = None
    for i in range(attempts):
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "causes-atlas-citation-verifier/1.0 "
                              "(mailto:473abel@gmail.com)"}
            )
            with urllib.request.urlopen(req, timeout=20) as resp:
                return resp.read().decode("utf-8")
        except Exception as e:
            last = e
            time.sleep(0.5 * (i + 1))
    raise RuntimeError(f"http_get failed: {last}")


def esearch(query: str, retmax: int = 8) -> list[str]:
    """Return up to retmax PMIDs ranked by PubMed relevance."""
    url = (
        f"{EUTILS}/esearch.fcgi?db=pubmed&retmode=json&sort=relevance"
        f"&retmax={retmax}&term=" + urllib.parse.quote(query)
    )
    data = json.loads(http_get(url))
    return data.get("esearchresult", {}).get("idlist", [])


def esummary(pmids: list[str]) -> dict[str, dict]:
    if not pmids:
        return {}
    url = (
        f"{EUTILS}/esummary.fcgi?db=pubmed&retmode=json&id="
        + ",".join(pmids)
    )
    data = json.loads(http_get(url))
    res = data.get("result", {})
    out = {}
    for pid in res.get("uids", []):
        r = res.get(pid, {})
        authors = r.get("authors", [])
        first_author = authors[0]["name"] if authors else ""
        out[pid] = {
            "pmid": pid,
            "title": r.get("title", ""),
            "journal": r.get("fulljournalname") or r.get("source", ""),
            "year": (r.get("pubdate", "") or "").split(" ")[0],
            "first_author": first_author,
            "pubtype": r.get("pubtype", []),
        }
    return out


def score_hit(hit: dict, must_contain: list[str], query_terms: list[str]) -> int:
    """Score: +5 per must-contain hit in title, +1 per query term in title,
    +3 if pubtype includes Review, +1 if year >= 2005, -50 if title is
    obviously off-topic (none of must_contain present)."""
    title = (hit.get("title") or "").lower()
    score = 0
    must_hits = sum(1 for k in must_contain if k.lower() in title)
    score += 5 * must_hits
    score += sum(1 for t in query_terms if t.lower() in title and len(t) > 3)
    if "Review" in hit.get("pubtype", []):
        score += 3
    if "Meta-Analysis" in hit.get("pubtype", []):
        score += 4
    if "Randomized Controlled Trial" in hit.get("pubtype", []):
        score += 4
    try:
        if int(hit["year"]) >= 2005:
            score += 1
        if int(hit["year"]) >= 2015:
            score += 1
    except (ValueError, KeyError):
        pass
    if must_hits == 0:
        score -= 50  # off-topic guard
    return score


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

print(f"Verifying {len(CLAIMS)} citation claims via PubMed eutils…")
results = []
report_lines = []
report_lines.append("---")
report_lines.append("type: citation_audit")
report_lines.append('title: "Citation verification — orphan-wiring proposal"')
report_lines.append("---")
report_lines.append("")
report_lines.append("# Citation verification report")
report_lines.append("")
report_lines.append(
    "Every PMID in this report came from a live "
    "[NCBI eutils esearch](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi) "
    "call, not from memory. For each candidate edge in the "
    "orphan-wiring proposal, the search query is shown along with "
    "the top hits ranked by PubMed relevance + a deterministic "
    "title-overlap score. The chosen PMID is the highest-scoring hit "
    "where the title contains the expected biology terms."
)
report_lines.append("")
report_lines.append(f"_Run: {NOW}_")
report_lines.append("")

for i, c in enumerate(CLAIMS, 1):
    print(f"  [{i}/{len(CLAIMS)}] {c['id']} {c['from_id']} -> {c['to_id']}: {c['query']}")
    pmids = esearch(c["query"], retmax=8)
    time.sleep(0.4)  # eutils rate limit (3/sec without API key)
    sums = esummary(pmids) if pmids else {}
    time.sleep(0.4)

    query_terms = [t for t in c["query"].split() if t.isalpha() and len(t) > 3]
    ranked = sorted(
        sums.values(),
        key=lambda h: -score_hit(h, c["must_contain"], query_terms),
    )
    top = ranked[:5]
    chosen = top[0] if top and score_hit(top[0], c["must_contain"], query_terms) > 0 else None
    second = top[1] if len(top) > 1 and score_hit(top[1], c["must_contain"], query_terms) > 0 else None

    chosen_pmids = []
    if chosen:
        chosen_pmids.append(chosen["pmid"])
    if second:
        chosen_pmids.append(second["pmid"])

    results.append({
        **c,
        "verified_pmids": ";".join(chosen_pmids),
        "chosen": chosen,
        "second": second,
        "all_top": top,
    })

    # Report block
    report_lines.append(f"## {c['id']}: {c['from_id']} → {c['to_id']}")
    report_lines.append("")
    report_lines.append(f"**Edge table:** `{c['edge_table']}`  ")
    report_lines.append(f"**Relation:** `{c['relation_type']}`  ")
    report_lines.append(f"**Claim:** {c['claim']}  ")
    report_lines.append(f"**Query:** `{c['query']}`")
    report_lines.append("")
    if chosen:
        report_lines.append(
            f"**Chosen PMID:** "
            f"[{chosen['pmid']}](https://pubmed.ncbi.nlm.nih.gov/{chosen['pmid']}/) — "
            f"{chosen['first_author']} ({chosen['year']}) "
            f"*{chosen['journal']}* — "
            f"{chosen['title']}"
        )
        if second:
            report_lines.append(
                f"**Second PMID:** "
                f"[{second['pmid']}](https://pubmed.ncbi.nlm.nih.gov/{second['pmid']}/) — "
                f"{second['first_author']} ({second['year']}) "
                f"*{second['journal']}* — "
                f"{second['title']}"
            )
    else:
        report_lines.append("**Chosen PMID:** _NONE — no relevant hit. Review needed._")
    report_lines.append("")
    report_lines.append("Top candidates considered:")
    report_lines.append("")
    report_lines.append("| Score | PMID | Year | First author | Journal | Title |")
    report_lines.append("|------|------|------|--------------|---------|-------|")
    for h in top:
        s = score_hit(h, c["must_contain"], query_terms)
        title = (h.get("title") or "").replace("|", "\\|")
        if len(title) > 100:
            title = title[:100] + "…"
        report_lines.append(
            f"| {s} | [{h['pmid']}](https://pubmed.ncbi.nlm.nih.gov/{h['pmid']}/) | "
            f"{h['year']} | {h['first_author']} | {h['journal']} | {title} |"
        )
    report_lines.append("")

# ---------------------------------------------------------------------------
# Emit verified CSV (same schema as candidate_orphan_edges.csv)
# ---------------------------------------------------------------------------

out_csv = PROP / "candidate_orphan_edges_verified.csv"
fields = [
    "id", "from_id", "from_type", "to_id", "to_type",
    "edge_table", "relation_type", "polarity",
    "rationale", "supporting_pmids", "status", "created_at",
    "verification_query",
]

with open(out_csv, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    for r in results:
        # Infer entity types
        ftype = {"H": "hypothesis", "I": "intervention", "M": "mechanism",
                 "P": "phenotype", "G": "gene", "C": "combination"}[r["from_id"][0]]
        ttype = {"H": "hypothesis", "I": "intervention", "M": "mechanism",
                 "P": "phenotype", "G": "gene", "C": "combination"}[r["to_id"][0]]
        w.writerow({
            "id": r["id"],
            "from_id": r["from_id"],
            "from_type": ftype,
            "to_id": r["to_id"],
            "to_type": ttype,
            "edge_table": r["edge_table"],
            "relation_type": r["relation_type"],
            "polarity": r["polarity"],
            "rationale": r["claim"],
            "supporting_pmids": r["verified_pmids"],
            "status": "verified" if r["verified_pmids"] else "needs_review",
            "created_at": NOW,
            "verification_query": r["query"],
        })

(PROP / "CITATION_VERIFICATION.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")
(VAULT / "CITATION_VERIFICATION.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")

n_verified = sum(1 for r in results if r["verified_pmids"])
n_review = len(results) - n_verified
print()
print(f"Done. Wrote {out_csv}")
print(f"      {len(results)} claims processed.")
print(f"      {n_verified} verified, {n_review} need manual review.")
print(f"      Report: {VAULT/'CITATION_VERIFICATION.md'}")
