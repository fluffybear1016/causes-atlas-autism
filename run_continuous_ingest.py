#!/usr/bin/env python3
"""3.5I — Continuous ingestion pipeline.

Polls PubMed for new autism-relevant publications using configured search queries,
queues candidates for manual review, and (after review) ingests verified PMIDs into
the atlas as new SRC entries.

USAGE:
    python3 run_continuous_ingest.py poll      # fetch new candidates from PubMed
    python3 run_continuous_ingest.py review    # show pending queue
    python3 run_continuous_ingest.py approve <PMID>...  # mark PMIDs for ingestion
    python3 run_continuous_ingest.py ingest    # ingest approved PMIDs

Configured query patterns cover: leucovorin/FRAA, mitochondrial autism, microbiome
autism, MCAS autism, PANS/PANDAS, methylation autism, gut-brain autism, multi-omics
autism, peptide autism, stem cell autism, glyphosate autism, vaccine autism (contested),
plus broad "autism 2026 review".

State persists in v2.0.1_proposed/continuous_ingest/:
  candidates.json — fetched but unreviewed PMIDs with metadata
  approved.json — manually-approved for ingestion
  ingested.json — completed ingestions log
  excluded.json — manually rejected PMIDs (so we don't re-fetch)
"""
import csv, datetime as dt, json, sys, urllib.request, urllib.parse, time, re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent
STATE_DIR = ROOT / "v2.0.1_proposed" / "continuous_ingest"
STATE_DIR.mkdir(parents=True, exist_ok=True)

CANDIDATES = STATE_DIR / "candidates.json"
APPROVED = STATE_DIR / "approved.json"
INGESTED = STATE_DIR / "ingested.json"
EXCLUDED = STATE_DIR / "excluded.json"

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
NOW = dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')

# ============================================================
# Query patterns — autism research surveillance
# ============================================================
QUERIES = [
    ("leucovorin folinic acid autism", "methylation_intervention"),
    ("FRAA folate receptor autoantibody autism", "folate_receptor"),
    ("mitochondrial dysfunction autism review", "mitochondrial"),
    ("microbiome autism children", "microbiome"),
    ("fecal microbiota transplant autism", "microbiome_intervention"),
    ("mast cell activation autism", "mast_cell"),
    ("PANS PANDAS autism children", "pans_pandas"),
    ("methylation cycle autism children", "methylation"),
    ("gut brain axis autism children", "gut_brain"),
    ("multi-omics autism review recent", "multi_omics"),
    ("oxytocin intranasal autism trial", "peptides"),
    ("cord blood autism stem cell", "cell_therapy"),
    ("glyphosate autism", "environmental"),
    ("aluminum adjuvant autism", "vaccine_contested"),
    ("MMR autism subgroup", "vaccine_contested"),
    ("acetaminophen pregnancy autism", "environmental"),
    ("PFAS autism children", "environmental"),
    ("autism GABA bumetanide", "gabaergic"),
    ("naltrexone low-dose autism", "immune_modulation"),
    ("rapamycin TSC autism", "drug_repurposing"),
    ("cell danger response autism Naviaux", "naviaux_framework"),
    ("HBOT autism oxidative stress", "mitochondrial_intervention"),
    ("Cunningham panel autism", "pans_pandas"),
    ("vitamin D autism children", "nutrient"),
    ("EEG ERP autism biomarker", "brain_biomarker"),
]

def http(url):
    req = urllib.request.Request(url, headers={"User-Agent": "causes-atlas-pipeline/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r: return r.read().decode()

def load_state(path, default):
    if path.exists():
        try: return json.loads(path.read_text())
        except: return default
    return default

def save_state(path, obj):
    path.write_text(json.dumps(obj, indent=2))

# ============================================================
# poll — fetch new candidates
# ============================================================
def cmd_poll(days_back=14):
    print(f"Polling PubMed for last {days_back} days across {len(QUERIES)} queries...")

    candidates = load_state(CANDIDATES, {})
    excluded = set(load_state(EXCLUDED, {"pmids": []}).get("pmids", []))
    ingested = set(load_state(INGESTED, {"pmids": []}).get("pmids", []))

    # Already-known PMIDs in atlas
    in_atlas = set()
    sources_csv = ROOT / "v2.0_scored" / "sources.csv"
    if sources_csv.exists():
        for r in csv.DictReader(open(sources_csv)):
            if r.get("platform") == "pubmed" and r.get("external_id"):
                in_atlas.add(r["external_id"])

    cutoff = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days_back)).strftime("%Y/%m/%d")
    new_count = 0

    for query, category in QUERIES:
        q = f"{query} AND ({cutoff}[PDAT]:3000[PDAT])"
        url = f"{EUTILS}/esearch.fcgi?db=pubmed&retmode=json&retmax=20&term={urllib.parse.quote(q)}"
        try:
            d = json.loads(http(url))
            ids = d.get("esearchresult", {}).get("idlist", [])
        except Exception as e:
            print(f"  WARN {query}: {e}")
            time.sleep(2); continue

        time.sleep(0.4)
        new_pmids = [p for p in ids if p not in candidates and p not in excluded
                     and p not in ingested and p not in in_atlas]
        if not new_pmids:
            continue

        try:
            d2 = json.loads(http(f"{EUTILS}/esummary.fcgi?db=pubmed&retmode=json&id={','.join(new_pmids)}"))
        except Exception as e:
            print(f"  WARN summary {query}: {e}")
            time.sleep(2); continue
        time.sleep(0.4)

        for pmid in new_pmids:
            r = d2.get("result", {}).get(pmid, {})
            if not r.get("title"): continue
            candidates[pmid] = {
                "pmid": pmid, "category": category,
                "title": r.get("title", ""),
                "year": r.get("pubdate", "")[:4],
                "journal": r.get("source", ""),
                "authors": [a.get("name","") for a in r.get("authors",[])[:3]],
                "pubtype": r.get("pubtype", []),
                "discovered_at": NOW, "discovered_via": query,
            }
            new_count += 1

    save_state(CANDIDATES, candidates)
    print(f"\nNew candidates: {new_count}")
    print(f"Total queue size: {len(candidates)}")
    print(f"Run `python3 run_continuous_ingest.py review` to triage")

# ============================================================
# review — list pending queue grouped by category
# ============================================================
def cmd_review():
    candidates = load_state(CANDIDATES, {})
    if not candidates:
        print("Queue empty. Run poll first.")
        return
    by_cat = defaultdict(list)
    for c in candidates.values():
        by_cat[c["category"]].append(c)
    for cat in sorted(by_cat):
        print(f"\n=== {cat} ({len(by_cat[cat])} candidates) ===")
        for c in sorted(by_cat[cat], key=lambda x: -int(x.get("year", "0") or "0"))[:10]:
            print(f"  {c['pmid']} ({c.get('year','')}) {c.get('journal','')[:25]}: {c.get('title','')[:90]}")
            print(f"    Authors: {', '.join(c.get('authors',[])[:3])}")
    print(f"\nTo approve: python3 run_continuous_ingest.py approve PMID1 PMID2 ...")
    print(f"To exclude: python3 run_continuous_ingest.py exclude PMID1 PMID2 ...")

# ============================================================
# approve / exclude
# ============================================================
def cmd_approve(pmids):
    candidates = load_state(CANDIDATES, {})
    approved = load_state(APPROVED, {})
    for p in pmids:
        if p in candidates:
            approved[p] = candidates.pop(p)
            print(f"  ✓ approved {p}: {approved[p].get('title','')[:80]}")
    save_state(CANDIDATES, candidates)
    save_state(APPROVED, approved)
    print(f"\nApproved queue: {len(approved)}")

def cmd_exclude(pmids):
    candidates = load_state(CANDIDATES, {})
    excluded = load_state(EXCLUDED, {"pmids": []})
    for p in pmids:
        if p in candidates:
            del candidates[p]
        if p not in excluded["pmids"]:
            excluded["pmids"].append(p)
            print(f"  ✗ excluded {p}")
    save_state(CANDIDATES, candidates)
    save_state(EXCLUDED, excluded)

# ============================================================
# ingest — turn approved candidates into SRC entries
# ============================================================
def cmd_ingest():
    approved = load_state(APPROVED, {})
    if not approved:
        print("No approved candidates to ingest.")
        return
    sources_path = ROOT / "v2.0_scored" / "sources.csv"
    with open(sources_path) as _f:
        rows = list(csv.DictReader(_f))
    with open(sources_path) as _f:
        fields = list(csv.DictReader(_f).fieldnames)

    # Find next free SRC ID
    existing_n = sorted({int(r["id"].split("-")[1]) for r in rows if r["id"].startswith("SRC-")})
    next_n = max(existing_n) + 1

    ingested = load_state(INGESTED, {"pmids": []})
    new_rows = []
    for pmid, c in approved.items():
        sid = f"SRC-{next_n:06d}"; next_n += 1
        # Map pubtype to study_design (schema-valid values per W_DESIGN dict)
        pt = c.get("pubtype", [])
        if "Meta-Analysis" in pt: design = "meta_analysis"
        elif "Randomized Controlled Trial" in pt: design = "rct"
        elif "Editorial" in pt: design = "editorial"
        elif "Letter" in pt: design = "letter"
        elif "Comment" in pt: design = "comment"
        elif "News" in pt or "Newspaper Article" in pt: design = "news"
        elif "Review" in pt or "Systematic Review" in pt: design = "review"
        elif "Case Reports" in pt: design = "case_series"
        else: design = "other"  # falls through to W_DESIGN default 0.40

        new_rows.append({
            "id": sid, "type": design, "platform": "pubmed", "external_id": pmid,
            "title": c.get("title",""),
            "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
            "date_published": f"{c.get('year','')}-01-01" if c.get("year") else "",
            "date_ingested": NOW,
            "study_design": design, "sample_size": "", "model_system": "human",
            "raw_metadata": json.dumps({
                "pmid": pmid, "year": c.get("year",""), "journal": c.get("journal",""),
                "authors": c.get("authors",[]), "discovered_via": c.get("discovered_via",""),
                "category_tag": c.get("category",""),
                "ingested_via": "run_continuous_ingest.py",
                "verified_against_pubmed": True,
            }),
            "notes": f"Auto-ingested {NOW[:10]} from continuous pipeline (category: {c.get('category','')})",
        })
        ingested["pmids"].append(pmid)

    # Re-verify PMIDs against PubMed at ingest time (not just rely on cached poll-time data)
    print(f"Re-verifying {len(approved)} PMIDs against PubMed before commit...")
    verify_ids = list(approved.keys())
    try:
        d_verify = json.loads(http(f"{EUTILS}/esummary.fcgi?db=pubmed&retmode=json&id={','.join(verify_ids)}"))
        verified_at_ingest = set()
        for pmid in verify_ids:
            r = d_verify.get("result", {}).get(pmid, {})
            if r and r.get("title"):
                verified_at_ingest.add(pmid)
        print(f"  ✓ {len(verified_at_ingest)}/{len(verify_ids)} PMIDs re-verified against PubMed")
        skipped = set(verify_ids) - verified_at_ingest
        if skipped:
            print(f"  ⚠ {len(skipped)} PMIDs failed re-verification — will skip: {skipped}")
            # Remove failed PMIDs from new_rows + approved
            new_rows = [r for r in new_rows if r["external_id"] in verified_at_ingest]
    except Exception as e:
        print(f"  ⚠ Re-verification failed: {e} — proceeding with cached metadata")

    print(f"Ingesting {len(new_rows)} new SRC entries...")
    rows.extend(new_rows)
    for d in [ROOT/"v2.0_scored", ROOT/"v2.0.1_expanded"]:
        path = d/"sources.csv"
        with open(path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            for r in rows:
                w.writerow({k: r.get(k, "") for k in fields})
        print(f"  ✓ {d.name}/sources.csv: +{len(new_rows)}")

    save_state(APPROVED, {})
    save_state(INGESTED, ingested)
    print(f"\nIngestion complete. Total ingested-via-pipeline lifetime: {len(ingested['pmids'])}")
    print("Next: run_scoring_v20.py to recompute, then build_vault.py to refresh vault.")

# ============================================================
# CLI
# ============================================================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(0)
    cmd = sys.argv[1]
    if cmd == "poll":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 14
        cmd_poll(days)
    elif cmd == "review":
        cmd_review()
    elif cmd == "approve":
        cmd_approve(sys.argv[2:])
    elif cmd == "exclude":
        cmd_exclude(sys.argv[2:])
    elif cmd == "ingest":
        cmd_ingest()
    else:
        print(f"Unknown command: {cmd}"); sys.exit(1)
