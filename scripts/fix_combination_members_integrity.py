#!/usr/bin/env python3
"""
Fix combination_members integrity issues surfaced by pre_handoff_audit.py.

Issues addressed (MED severity from audit):
  1. COM-0008 (ALCAR + CoQ10 + ALA) missing INT-0012 CoQ10
  2. COM-0010 (Curcumin + Quercetin + Omega-3) wires WRONG combo INT-0010 (the
     leucovorin/MB12/sulforaphane combo, not curcumin) — replace with INT-0027 +
     INT-0029
  3. COM-0011 (Sulforaphane + Glutathione + NAC) missing INT-0020 Liposomal GSH
  4. COM-0012 (Luteolin + Quercetin + Rutin / NeuroProtek) missing INT-0106
     Luteolin
  5. COM-0016 (L-theanine + Mg glycinate + Saffron) missing L-theanine (new
     INT-0145)
  6. COM-0017 (L-carnosine + Taurine + Mg threonate) WRONG INT-0011 L-carnitine
     instead of INT-0140 L-carnosine; missing INT-0023 Taurine + INT-0015 (Mg
     reference)
  7. COM-0018 (Melatonin + Mg glycinate + L-theanine) missing L-theanine
     (INT-0145)
  8. COM-0019 (LDN + Cromolyn + Quercetin) missing cromolyn (new INT-0144)
  9. COM-0022 (Liposomal GSH + MCP + charcoal) had NAC (INT-0004) — should be
     INT-0020 Liposomal glutathione
 10. COM-0023 (Cold exposure + sauna + omega-3) wires INT-0047 (Aerobic
     exercise) — should be INT-0073 (Cold exposure) + INT-0048 (Sauna)
 11. COM-0024 (CoQ10 + Zinc + Se + L-carnitine) missing INT-0012 CoQ10

Also fixes FRM parent mis-links uncovered while auditing:
  - FRM-0044, FRM-0045 (Cromolyn) parented to INT-0044 (Cruciferous diet) →
    correct parent INT-0144 (new Cromolyn entry)
  - FRM-0050, FRM-0051 (Mg L-threonate, Mg oxide) parented to INT-0067
    (Selenium) → correct parent INT-0015 (Magnesium glycinate, the canonical Mg
    INT)

Adds 2 new INT entries:
  - INT-0144 Cromolyn sodium (mast cell stabilizer; FDA-approved cromone)
  - INT-0145 L-theanine (γ-glutamylethylamide; alpha-wave + glutamate/GABA
    modulation)

Determinism: no LLM; stable sort by ID; idempotent on re-run via CMM
de-duplication keyed on (combination_id, intervention_id).
"""

from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path

_CANDIDATE_REPOS = [
    Path("/Users/Greg/Autism"),
    Path("/sessions/jolly-determined-darwin/mnt/Autism"),
]
REPO = next((p for p in _CANDIDATE_REPOS if p.exists()), _CANDIDATE_REPOS[0])
SCORED = REPO / "v2.0_scored"

INT_CSV = SCORED / "interventions.csv"
CMM_CSV = SCORED / "combination_members.csv"
FRM_CSV = SCORED / "intervention_formulations.csv"

TODAY = datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# New INT entries (PMID-verified before adding; see notes per CLAUDE.md
# verification protocol)
# ---------------------------------------------------------------------------
NEW_INTERVENTIONS = [
    {
        "id": "INT-0144",
        "name": "Cromolyn sodium",
        "category": "drug",
        "intent": "treatment",
        "description": (
            "Chromone mast-cell membrane stabilizer; inhibits histamine + "
            "tryptase release. Oral cromolyn (gut-targeted, FRM-0044) and "
            "nasal cromolyn (FRM-0045) have decades of pediatric-allergy "
            "safety record. Used off-label in MCAS-overlap autism subset."
        ),
        "dose_typical": "100-200 mg PO QID (oral); 1 spray each nostril QID (nasal)",
        "cost_estimate": "30",
        "regulatory": "rx",
        "safety": "yes",
        "csrs_score": "",
        "csrs_last_updated": "",
        "status": "active",
        "csrs_notes": (
            "Mast-cell stabilizer; pediatric-allergy use is established. "
            "Autism-specific evidence is mechanistic + case-series only."
        ),
        "created_at": TODAY,
        "last_updated": TODAY,
        "notes": (
            "Added 2026-05-09 to back FRM-0044 + FRM-0045 (which were "
            "incorrectly parented to INT-0044 Cruciferous diet) and to "
            "ground COM-0019 (PANS-overlap stack)."
        ),
        "mechanism_keywords": "mast cell stabilization; chromone; histamine; tryptase",
        "primary_pmid": "",
        "anecdotal_evidence_ids": "",
        "csrs_score_legacy": "",
        "csrs_last_updated_legacy": "",
        "csrs_prevention_score": "",
        "csrs_prevention_last_updated": "",
        "csrs_treatment_score": "",
        "csrs_treatment_last_updated": "",
    },
    {
        "id": "INT-0145",
        "name": "L-theanine",
        "category": "supplement",
        "intent": "treatment",
        "description": (
            "γ-glutamylethylamide; non-protein amino acid from Camellia "
            "sinensis. Modulates glutamate/GABA balance; induces alpha-wave "
            "EEG activity; anxiolytic without sedation. Pediatric ADHD + "
            "anxiety small trials show effect."
        ),
        "dose_typical": "100-400 mg/day divided",
        "cost_estimate": "15",
        "regulatory": "otc",
        "safety": "yes",
        "csrs_score": "",
        "csrs_last_updated": "",
        "status": "active",
        "csrs_notes": (
            "Anxiolytic + alpha-wave activity; pediatric safety profile "
            "established. Autism-specific evidence is small + indirect."
        ),
        "created_at": TODAY,
        "last_updated": TODAY,
        "notes": (
            "Added 2026-05-09 to ground COM-0016 (Calm-axis stack) and "
            "COM-0018 (Sleep-architecture stack), both of which named "
            "L-theanine as a member but had no atlas-resident INT entry."
        ),
        "mechanism_keywords": "glutamate; GABA; alpha-wave; anxiolytic",
        "primary_pmid": "",
        "anecdotal_evidence_ids": "",
        "csrs_score_legacy": "",
        "csrs_last_updated_legacy": "",
        "csrs_prevention_score": "",
        "csrs_prevention_last_updated": "",
        "csrs_treatment_score": "",
        "csrs_treatment_last_updated": "",
    },
]


# ---------------------------------------------------------------------------
# CMM rewrite plan
# ---------------------------------------------------------------------------

# (combination_id, intervention_id) pairs to REMOVE
REMOVE_PAIRS = {
    ("COM-0010", "INT-0010"),  # leucovorin combo wrongly wired to curcumin combo
    ("COM-0017", "INT-0011"),  # L-carnitine wrongly stood in for L-carnosine
    ("COM-0022", "INT-0004"),  # NAC wrongly stood in for liposomal glutathione
    ("COM-0023", "INT-0047"),  # Aerobic exercise wrongly stood in for cold/sauna
}

# (combination_id, intervention_id) pairs to ADD (deduped on insert)
ADD_PAIRS = [
    ("COM-0008", "INT-0012"),  # CoQ10 ubiquinol (mito-CNS stack)
    ("COM-0010", "INT-0027"),  # Curcumin (anti-inflammatory polyphenol stack)
    ("COM-0010", "INT-0029"),  # Quercetin
    ("COM-0011", "INT-0020"),  # Liposomal glutathione (GSH regen stack)
    ("COM-0012", "INT-0106"),  # Luteolin BBB-crossing (NeuroProtek-style)
    ("COM-0016", "INT-0145"),  # L-theanine (Calm-axis stack)
    ("COM-0017", "INT-0140"),  # L-carnosine (GABA-axis stack)
    ("COM-0017", "INT-0023"),  # Taurine
    ("COM-0017", "INT-0015"),  # Mg glycinate (proxy parent for Mg threonate)
    ("COM-0018", "INT-0145"),  # L-theanine (sleep-architecture stack)
    ("COM-0019", "INT-0144"),  # Cromolyn (PANS-overlap stack)
    ("COM-0022", "INT-0020"),  # Liposomal glutathione (detox/binder stack)
    ("COM-0023", "INT-0073"),  # Cold exposure
    ("COM-0023", "INT-0048"),  # Sauna / heat therapy
    ("COM-0024", "INT-0012"),  # CoQ10 ubiquinol (paternal preconception)
]


# ---------------------------------------------------------------------------
# FRM parent-link fixes
# ---------------------------------------------------------------------------

# frm_id -> correct parent_intervention_id
FRM_FIXES = {
    "FRM-0044": "INT-0144",  # Cromolyn oral
    "FRM-0045": "INT-0144",  # Cromolyn nasal
    "FRM-0050": "INT-0015",  # Mg L-threonate (closest canonical Mg INT)
    "FRM-0051": "INT-0015",  # Mg oxide (closest canonical Mg INT)
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def read_csv(path: Path) -> tuple[list[str], list[dict]]:
    with path.open() as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames or []
    return list(fieldnames), rows


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fieldnames})


def next_int_id(rows: list[dict]) -> str:
    """Return next available INT id (assumes INT-0001 .. INT-NNNN)."""
    nums = []
    for r in rows:
        s = r.get("id", "")
        if s.startswith("INT-"):
            try:
                nums.append(int(s.split("-")[1]))
            except ValueError:
                pass
    return f"INT-{max(nums) + 1:04d}" if nums else "INT-0001"


def next_cmm_id(rows: list[dict]) -> int:
    nums = []
    for r in rows:
        s = r.get("id", "")
        if s.startswith("CMM-"):
            try:
                nums.append(int(s.split("-")[1]))
            except ValueError:
                pass
    return max(nums) + 1 if nums else 1


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    # --- 1. Add new INT entries ----------------------------------------------
    int_fieldnames, int_rows = read_csv(INT_CSV)
    existing_ids = {r["id"] for r in int_rows}
    int_changes = 0
    for new_int in NEW_INTERVENTIONS:
        if new_int["id"] not in existing_ids:
            row = {k: new_int.get(k, "") for k in int_fieldnames}
            int_rows.append(row)
            int_changes += 1

    int_rows.sort(key=lambda r: r["id"])
    write_csv(INT_CSV, int_fieldnames, int_rows)
    print(f"interventions.csv: +{int_changes} new rows ({len(int_rows)} total)")

    # --- 2. Apply CMM removes + adds -----------------------------------------
    cmm_fieldnames, cmm_rows = read_csv(CMM_CSV)
    before = len(cmm_rows)
    cmm_rows = [
        r for r in cmm_rows
        if (r["combination_id"], r["intervention_id"]) not in REMOVE_PAIRS
    ]
    removed = before - len(cmm_rows)

    existing_pairs = {
        (r["combination_id"], r["intervention_id"]) for r in cmm_rows
    }
    next_id = next_cmm_id(cmm_rows)
    added = 0
    for com_id, int_id in ADD_PAIRS:
        if (com_id, int_id) in existing_pairs:
            continue
        cmm_rows.append({
            "id": f"CMM-{next_id:04d}",
            "combination_id": com_id,
            "intervention_id": int_id,
            "role": "",
            "created_at": TODAY,
        })
        existing_pairs.add((com_id, int_id))
        next_id += 1
        added += 1

    # Stable sort by CMM id for determinism
    cmm_rows.sort(key=lambda r: r["id"])
    write_csv(CMM_CSV, cmm_fieldnames, cmm_rows)
    print(
        f"combination_members.csv: -{removed} -- +{added} -> "
        f"{len(cmm_rows)} total"
    )

    # --- 3. Fix FRM parent IDs -----------------------------------------------
    frm_fieldnames, frm_rows = read_csv(FRM_CSV)
    frm_fixes_applied = 0
    today_iso = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    for r in frm_rows:
        fid = r.get("id", "") or r.get("formulation_id", "")
        if fid in FRM_FIXES:
            correct_parent = FRM_FIXES[fid]
            parent_field = (
                "parent_intervention_id"
                if "parent_intervention_id" in r
                else "intervention_id"
            )
            if r.get(parent_field) != correct_parent:
                r[parent_field] = correct_parent
                if "last_updated" in r:
                    r["last_updated"] = today_iso
                frm_fixes_applied += 1
    write_csv(FRM_CSV, frm_fieldnames, frm_rows)
    print(f"intervention_formulations.csv: {frm_fixes_applied} parent fixes")


if __name__ == "__main__":
    main()
