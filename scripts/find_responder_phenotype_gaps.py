#!/usr/bin/env python3
"""find_responder_phenotype_gaps.py — autonomous pattern miner #4

Identifies interventions with mainstream-mixed-evidence status that have
NOT yet been tagged with a responder-phenotype profile. Per CLAUDE.md
epistemic principle §9: "Mixed published evidence is almost always effect
heterogeneity, not absence of effect — extract responder phenotypes."

Triggers when:
  - intervention.status is "contested" OR mainstream_consensus_position
    contains words like "mixed", "weak", "insufficient", "no evidence"
  - AND no entry in intervention_formulations.csv with explicit
    `responder_population_notes`
  - AND no link in intervention_phenotype_edges to a stratified phenotype

Determinism: stable sort by ID; no random seeds; no LLM calls.

Usage:
    python3 scripts/find_responder_phenotype_gaps.py

Output:
    vault/Discoveries_Inbox/responder_phenotype_gaps_{date}.md / .json
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCORED_DIR = ROOT / "v2.0_scored"
INBOX_DIR = ROOT / "vault" / "Discoveries_Inbox"
INBOX_DIR.mkdir(parents=True, exist_ok=True)


def _load_csv(name: str) -> list[dict]:
    path = SCORED_DIR / f"{name}.csv"
    if not path.exists():
        return []
    with path.open() as f:
        return list(csv.DictReader(f))


MIXED_EVIDENCE_KEYWORDS = (
    "mixed", "weak", "insufficient", "no evidence", "negative",
    "null", "no benefit", "ineffective", "controversial", "contested",
    "unclear", "inconsistent", "limited",
)


def _has_mixed_evidence_signal(row: dict) -> bool:
    status = (row.get("status") or "").lower()
    consensus = (row.get("mainstream_consensus_position") or "").lower()
    if "contested" in status:
        return True
    for kw in MIXED_EVIDENCE_KEYWORDS:
        if kw in consensus:
            return True
    return False


def find_responder_phenotype_gaps() -> dict:
    interventions = _load_csv("interventions")
    formulations = _load_csv("intervention_formulations")
    int_phe_edges = _load_csv("intervention_phenotype_edges")

    # Map intervention_id → formulation rows with responder notes
    formulations_by_parent: dict[str, list[dict]] = {}
    for f in formulations:
        pid = f.get("parent_intervention_id", "")
        formulations_by_parent.setdefault(pid, []).append(f)

    has_responder_notes_at_form: set[str] = set()
    for pid, forms in formulations_by_parent.items():
        for f in forms:
            notes = (f.get("responder_population_notes") or "").strip()
            if notes and notes.lower() not in (
                "cohort baseline; frm-specific responder profile not established",
                "",
            ):
                has_responder_notes_at_form.add(pid)
                break

    # Map intervention_id → connected phenotypes via int_phe edges
    int_to_phe: dict[str, set[str]] = {}
    for e in int_phe_edges:
        iid = e.get("intervention_id", "")
        pid = e.get("phenotype_id", "")
        if iid and pid:
            int_to_phe.setdefault(iid, set()).add(pid)

    candidates = []
    for r in sorted(interventions, key=lambda x: x.get("id", "")):
        iid = r.get("id", "")
        if not iid:
            continue
        if not _has_mixed_evidence_signal(r):
            continue
        if iid in has_responder_notes_at_form:
            continue
        if int_to_phe.get(iid):
            continue
        try:
            csrs = float(r.get("csrs_score") or 0)
        except (ValueError, TypeError):
            csrs = 0.0
        candidates.append({
            "intervention_id": iid,
            "intervention_name": r.get("name", ""),
            "category": r.get("category", ""),
            "status": r.get("status", ""),
            "mainstream_consensus_position": r.get("mainstream_consensus_position", ""),
            "csrs_score": csrs,
            "mechanism_summary": (r.get("mechanism_summary") or "")[:200],
            "investigation_priority": "high" if csrs >= 60 else ("medium" if csrs >= 40 else "low"),
        })

    candidates.sort(key=lambda c: (-c["csrs_score"], c["intervention_id"]))

    return {
        "candidates": candidates,
        "total_interventions": len(interventions),
        "interventions_with_mixed_evidence": sum(
            1 for r in interventions if _has_mixed_evidence_signal(r)
        ),
        "interventions_with_responder_notes_at_formulation_level": len(has_responder_notes_at_form),
    }


def render_markdown(result: dict, date_str: str) -> str:
    lines = [
        f"# Responder phenotype gaps — {date_str}",
        "",
        "Pattern miner #4: surfaces interventions with mixed published evidence that have **not yet** been tagged with a responder-phenotype profile. Per `CLAUDE.md` §9: mixed evidence is almost always effect heterogeneity, not absence of effect.",
        "",
        f"**Total interventions:** {result['total_interventions']}",
        f"**Mixed-evidence interventions:** {result['interventions_with_mixed_evidence']}",
        f"**Interventions with formulation-level responder notes:** {result['interventions_with_responder_notes_at_formulation_level']}",
        f"**Gap candidates:** {len(result['candidates'])}",
        "",
        "---",
        "",
        f"## Top {min(20, len(result['candidates']))} responder-phenotype gap candidates",
        "",
        "| # | ID | Name | CSRS | Status | Priority |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for i, c in enumerate(result["candidates"][:20], 1):
        lines.append(
            f"| {i} | `{c['intervention_id']}` | {c['intervention_name'][:50]} | "
            f"{c['csrs_score']:.1f} | {c['status'][:25]} | "
            f"**{c['investigation_priority']}** |"
        )
    if not result["candidates"]:
        lines.append("| _no gaps detected this scan_ | | | | | |")

    lines.extend([
        "",
        "---",
        "",
        "## Curator workflow",
        "",
        "For each candidate above:",
        "",
        "1. **Investigate study heterogeneity.** Read 2-3 of the strongest negative trials + 2-3 of the strongest positive trials. Look for:",
        "   - Different patient populations (age, sex, baseline biomarkers, phenotype)",
        "   - Different formulations / doses / durations",
        "   - Different outcome measures",
        "   - Different inclusion/exclusion criteria",
        "",
        "2. **Extract responder profile.** Write the responder phenotype as concretely as possible:",
        "   - 'High pre-treatment FRAA + AND age >5 with severe verbal communication delay'",
        "   - 'Walsh undermethylator (low histamine + low SAM/SAH) AND no MTHFR T/T'",
        "   - 'GI-symptom-positive + microbiome dysbiosis + age >2'",
        "",
        "3. **Update atlas.** Either:",
        "   - Add a formulation row (`intervention_formulations.csv`) with `responder_population_notes`, OR",
        "   - Add an `intervention_phenotype_edge` linking to the responder phenotype dimension, OR",
        "   - Update `intervention.notes` with the responder profile.",
        "",
        "4. **Submit PMID-verified citations** for the responder-stratification claim.",
        "",
        "## Provenance",
        "",
        f"- Pipeline: `scripts/find_responder_phenotype_gaps.py`",
        f"- Run timestamp: {datetime.utcnow().isoformat()}Z",
    ])
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=datetime.utcnow().strftime("%Y-%m-%d"))
    args = parser.parse_args(argv)

    result = find_responder_phenotype_gaps()

    md_path = INBOX_DIR / f"responder_phenotype_gaps_{args.date}.md"
    json_path = INBOX_DIR / f"responder_phenotype_gaps_{args.date}.json"
    md_path.write_text(render_markdown(result, args.date))
    json_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")

    print(f"Wrote {md_path}")
    print(f"Found {len(result['candidates'])} responder-phenotype gap candidates")
    return 0


if __name__ == "__main__":
    sys.exit(main())
