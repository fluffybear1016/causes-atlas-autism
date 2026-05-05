#!/usr/bin/env python3
"""Fix incomplete Naviaux ingest from ingest_naviaux_mccullough.py.

Bug: EVD-001448 was already taken by the Tripedia fragment (SRC-001447),
so the Naviaux fragment was silently skipped, but evidence_links were still
written pointing to EVD-001448 (now Tripedia). Need to:

  1. Add the Naviaux fragment as EVD-001450 (next free ID).
  2. Repoint EVL-001703 through EVL-001707 (the Naviaux hypothesis/phenotype
     links that DID get added) from EVD-001448 → EVD-001450.
  3. Add the 3 Naviaux mechanism links that collided with EVL-001700-1702
     (MEC-0010, MEC-0014, MEC-0020) using new EVL IDs starting EVL-001713.

Both v2.0_scored and v2.0.1_expanded.
"""
import csv, datetime as dt, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NOW = dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')

# === Naviaux fragment, re-IDed to EVD-001450 ===
naviaux_frag = {
    "id": "EVD-001450",
    "source_id": "SRC-001448",
    "fragment_type": "result",
    "text_excerpt": (
        "Naviaux 2026 (Autism Research, PMID 41902612): proposes the "
        "3-Hit Metabolic Signaling Model for ASD, in which autism arises "
        "from sequential interaction of (1) inherited genetic/epigenetic "
        "variants sensitizing mitochondrial metabolism, intracellular "
        "calcium handling, and purinergic signaling to environmental "
        "change; (2) early prenatal or postnatal activation of the cell "
        "danger response (CDR) by infection, immune dysregulation, "
        "metabolic disturbance, or environmental toxicant exposure; and "
        "(3) prolonged or recurrent exposure to CDR-activating triggers "
        "for 3-6 months between the late 1st trimester and 18-36 months "
        "of age. The CDR is initiated by extracellular ATP (eATP)-"
        "associated purinergic signaling and mitochondrial changes that "
        "are resource- and energy-intensive. Persistent CDR activation "
        "during the critical neurodevelopmental window is proposed to "
        "sensitize developing cells to eATP-related signaling, leading "
        "to false alarms and chemical/immune/neurosensory under- and "
        "over-responsivity. PKU cited as proof-of-principle: untreated "
        "PKU historically caused intellectual disability and autistic "
        "features; universal newborn screening + early treatment "
        "interrupts the sequence and prevents/decreases these outcomes."
    ),
    "structured_payload": json.dumps({
        "framework": "3-hit_metabolic_signaling_model",
        "design": "peer_reviewed_theoretical_review",
        "hits": ["genetic/epigenetic mito+Ca+purinergic sensitization",
                 "early CDR activation by environmental triggers",
                 "prolonged/recurrent CDR for 3-6mo in 1st trimester to 18-36mo window"],
        "core_mechanism": "extracellular ATP purinergic signaling + mitochondrial CDR",
        "proof_of_principle": "PKU",
        "author": "Naviaux RK",
        "is_secondary_literature": False,
        "primary": True,
        "peer_reviewed": True,
    }),
    "effect_direction": "positive",
    "strength_score": "0.50",
    "extraction_method": "manual",
    "extraction_confidence": "0.95",
    "date_extracted": NOW,
    "notes": ("Major framework update by Naviaux. Connects CDR theory + "
              "purinergic signaling + mito to ASD via 3-hit susceptibility "
              "× early-trigger × prolonged-window structure. Aligns with "
              "atlas's Hannah Poling framework (P × E → Φ). "
              "Re-IDed from EVD-001448 to EVD-001450 because EVD-001448 "
              "was already used by Tripedia insert (SRC-001447)."),
}

# === The 5 Naviaux hyp/phe links that DID get appended but now point at the
# wrong fragment (Tripedia instead of Naviaux). Need to rewrite EVD-001448 →
# EVD-001450 ONLY for these specific EVL rows, not for legitimate Tripedia
# rows (EVL-001702 which points HYP-0044, pre-existing). ===
LINKS_TO_REPOINT = {"EVL-001703", "EVL-001704", "EVL-001705",
                    "EVL-001706", "EVL-001707"}

# === The 3 Naviaux mechanism links that collided as EVL-001700/1701/1702 and
# were skipped — re-add at new EVL IDs ===
new_mech_links_def = [
    ("MEC-0010", "Mitochondrial dysfunction is hit-1 substrate"),
    ("MEC-0014", "SIRTUIN/NAD+ purinergic signaling = CDR mechanism"),
    ("MEC-0020", "Calcium handling = hit-1 substrate"),
]

def fix_dir(d):
    print(f"\n{d.name}:")

    # 1. Add Naviaux fragment if not present
    fpath = d / "evidence_fragments.csv"
    rows = list(csv.DictReader(open(fpath)))
    fields = list(csv.DictReader(open(fpath)).fieldnames)
    existing = {r["id"] for r in rows}
    if "EVD-001450" not in existing:
        rows.append({f: naviaux_frag.get(f, "") for f in fields})
        with open(fpath, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader(); w.writerows(rows)
        print(f"  evidence_fragments.csv: added EVD-001450 (Naviaux)")
    else:
        print(f"  evidence_fragments.csv: EVD-001450 already present")

    # 2. Repoint Naviaux hyp/phe links from EVD-001448 → EVD-001450
    lpath = d / "evidence_links.csv"
    rows = list(csv.DictReader(open(lpath)))
    fields = list(csv.DictReader(open(lpath)).fieldnames)
    repointed = 0
    for r in rows:
        if r["id"] in LINKS_TO_REPOINT and r["evidence_fragment_id"] == "EVD-001448":
            r["evidence_fragment_id"] = "EVD-001450"
            repointed += 1

    # 3. Add the 3 missing Naviaux mechanism links at new EVL IDs
    existing_ids = {r["id"] for r in rows}
    next_id = max(int(r["id"].split("-")[1]) for r in rows) + 1
    added = 0
    for tid, note in new_mech_links_def:
        # Don't double-add if already present (idempotency)
        already = any(r["evidence_fragment_id"] == "EVD-001450"
                       and r["target_type"] == "mechanism"
                       and r["target_id"] == tid for r in rows)
        if already:
            continue
        new = {f: "" for f in fields}
        new.update({
            "id": f"EVL-{next_id:06d}",
            "evidence_fragment_id": "EVD-001450",
            "claim_id": "",
            "target_type": "mechanism",
            "target_id": tid,
            "effect_direction": "positive",
            "weight": "",
            "context_scope": "",
            "created_at": NOW,
            "notes": note,
        })
        rows.append(new); next_id += 1; added += 1

    with open(lpath, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(rows)
    print(f"  evidence_links.csv: repointed {repointed} (1448→1450), added {added} new mech links")

for d in [ROOT/"v2.0_scored", ROOT/"v2.0.1_expanded"]:
    fix_dir(d)

print("\nDone.")
