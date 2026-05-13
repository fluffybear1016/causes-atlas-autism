#!/usr/bin/env python3
"""
Second pass: clean up duplicate INT entries surfaced by re-audit after
fix_combination_members_integrity.py.

Discoveries after pass-1:
  - INT-0144 Cromolyn sodium (just added) duplicates pre-existing
    INT-0103 Cromolyn sodium (oral)
  - INT-0105 Quercetin duplicates INT-0029 Quercetin (older + scored)
  - INT-0118 N-acetylcysteine duplicates INT-0004 NAC (older + scored)
  - audit's keyword match also flags COM-0008/0024 missing INT-0055
    (combo INT) and COM-0013/0014 missing INT-0056 (combo INT) — these
    are false positives because INT-0055 / INT-0056 ARE combos
    themselves (category='combo'), not standalone components. Update
    audit to filter category='combo' so it stops flagging combos as
    members of other combos.

Plan:
  1. Redirect references:
     INT-0144 → INT-0103 (in formulations + combination_members)
     INT-0105 → INT-0029 (no external refs found, but defensive sweep)
     INT-0118 → INT-0004 (no external refs found, but defensive sweep)
  2. Delete duplicate rows from interventions.csv (INT-0144, INT-0105,
     INT-0118).
  3. Patch pre_handoff_audit.py to skip category='combo' entries when
     suggesting that "ingredient X has INT row but is not in member list."

Determinism: idempotent on re-run (already-deleted INTs are skipped).
"""

from __future__ import annotations

import csv
from pathlib import Path

_CANDIDATE_REPOS = [
    Path("/Users/Greg/Autism"),
    Path("/sessions/jolly-determined-darwin/mnt/Autism"),
]
REPO = next((p for p in _CANDIDATE_REPOS if p.exists()), _CANDIDATE_REPOS[0])
SCORED = REPO / "v2.0_scored"
SCRIPTS = REPO / "scripts"

INT_CSV = SCORED / "interventions.csv"
FRM_CSV = SCORED / "intervention_formulations.csv"
FRM_SCORED_CSV = SCORED / "intervention_formulations_scored.csv"
CMM_CSV = SCORED / "combination_members.csv"


REDIRECTS = {
    "INT-0144": "INT-0103",  # Cromolyn — use pre-existing entry
    "INT-0105": "INT-0029",  # Quercetin
    "INT-0118": "INT-0004",  # NAC
}

DELETE_IDS = set(REDIRECTS.keys())


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


def redirect_value(row: dict, fields: list[str]) -> bool:
    """Redirect any field in `fields` from old -> new INT id. Returns True
    if any field was changed."""
    changed = False
    for fld in fields:
        v = row.get(fld)
        if v in REDIRECTS:
            row[fld] = REDIRECTS[v]
            changed = True
    return changed


def main() -> None:
    # --- 1. Redirect refs in formulations ------------------------------------
    for frm_path in [FRM_CSV, FRM_SCORED_CSV]:
        if not frm_path.exists():
            continue
        fns, rows = read_csv(frm_path)
        parent_field = "parent_intervention_id" if "parent_intervention_id" in fns else "intervention_id"
        n = sum(1 for r in rows if r.get(parent_field) in REDIRECTS)
        for r in rows:
            redirect_value(r, [parent_field])
        write_csv(frm_path, fns, rows)
        print(f"{frm_path.name}: {n} parent redirects")

    # --- 2. Redirect refs in combination_members -----------------------------
    fns, rows = read_csv(CMM_CSV)
    n = sum(1 for r in rows if r.get("intervention_id") in REDIRECTS)
    new_rows = []
    seen_pairs: set[tuple[str, str]] = set()
    for r in rows:
        redirect_value(r, ["intervention_id"])
        key = (r["combination_id"], r["intervention_id"])
        if key in seen_pairs:
            continue  # drop dup created by redirect
        seen_pairs.add(key)
        new_rows.append(r)
    write_csv(CMM_CSV, fns, new_rows)
    print(
        f"combination_members.csv: {n} redirects, dropped "
        f"{len(rows) - len(new_rows)} duplicate pairs"
    )

    # --- 3. Delete duplicate INT rows ----------------------------------------
    fns, rows = read_csv(INT_CSV)
    before = len(rows)
    rows = [r for r in rows if r.get("id") not in DELETE_IDS]
    removed = before - len(rows)
    write_csv(INT_CSV, fns, rows)
    print(f"interventions.csv: removed {removed} duplicate rows ({len(rows)} total)")

    # --- 4. Patch pre_handoff_audit.py to skip combo INTs --------------------
    # (Patched manually 2026-05-09; this block kept as a no-op for idempotency.)
    audit_path = SCRIPTS / "pre_handoff_audit.py"
    src = audit_path.read_text()
    marker = "INGREDIENT_KEYWORD_TO_INT"
    if False and marker in src and "skip_combo_categories" not in src:
        # Inject a category filter where the audit looks up INT entries
        # by keyword. We do this by adding a guard right where the loop
        # iterates over the interventions corpus.
        needle = "for _int_id, _name, _category in self._interventions:"
        if needle in src:
            src = src.replace(
                needle,
                # mark patched + skip combo category
                "# Patch 2026-05-09: skip combo-category INTs (skip_combo_categories)\n            for _int_id, _name, _category in self._interventions:\n                if _category == 'combo':\n                    continue",
                1,
            )
            audit_path.write_text(src)
            print("pre_handoff_audit.py: patched to skip category='combo'")
        else:
            # Fallback: locate the ingredient-loop function differently
            needle2 = "for int_id, int_name, int_category in interventions_for_keyword_match"
            if needle2 in src:
                src = src.replace(
                    needle2,
                    "for int_id, int_name, int_category in interventions_for_keyword_match:\n            if int_category == 'combo':\n                continue\n        ".rstrip() + needle2.split(":")[0] + ":",
                    1,
                )
                audit_path.write_text(src)
                print("pre_handoff_audit.py: patched via fallback needle")
            else:
                print(
                    "pre_handoff_audit.py: no known patch needle found — "
                    "leaving file untouched (audit will continue to over-flag "
                    "combo INT entries; investigate manually)"
                )
    else:
        print("pre_handoff_audit.py: marker already present or no marker — skipping patch")


if __name__ == "__main__":
    main()
