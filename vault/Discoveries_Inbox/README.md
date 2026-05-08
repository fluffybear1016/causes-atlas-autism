# Discoveries Inbox

This folder is the **autonomous pattern-mining inbox**. The pipeline at `scripts/run_autonomous_discoveries.py` runs daily (via `.github/workflows/autonomous-discoveries.yml`) and writes candidate findings here for human curator review.

## What lands here

Four pattern miners run daily:

1. **Emergent edges** (`find_emergent_edges.py`) — gene × mechanism / gene × phenotype co-mention candidates from recent atlas sources. Surfaces edges the atlas implicitly contains but doesn't yet make explicit.

2. **Combination gaps** (`find_combination_gaps.py`) — intervention pairs/triples that share ≥1 mechanism but are not yet captured in any combination. Candidate synergies for review.

3. **Higher-order hypotheses** (`find_higher_order_hypotheses.py`) — graph-walk for 2nd-order chains (intervention → mechanism → phenotype) where the direct edge does NOT yet exist.

4. **Responder phenotype gaps** (`find_responder_phenotype_gaps.py`) — interventions with mainstream-mixed-evidence status that have not yet been tagged with a responder-phenotype profile. Per `CLAUDE.md` epistemic principle §9: mixed evidence is almost always effect heterogeneity.

## What does NOT happen here

- **No candidate is auto-promoted to the atlas.** All findings require human curator review.
- **No PMIDs are written** without verification per the verify-before-write protocol.
- **No edges are added** to scoring CSVs by the daemon. The daemon only writes Markdown / JSON reports here.

## Workflow

When you have time:

1. Pick the most recent `<date>_summary.md` to see the day's findings.
2. Drill into the per-finder Markdown reports.
3. For each candidate:
   - **Promote**: if mechanism-grounded AND PMID-verified primary evidence exists → add the edge to the appropriate scoring CSV. Re-run scoring. Verify INT-0001 calibration anchor still holds.
   - **Defer**: if interesting but evidence not yet sufficient → leave in inbox; finder will resurface it tomorrow.
   - **Reject**: if false positive (graph artifact, coincidental co-mention) → no action; finder may resurface but you can ignore.

## Determinism

Each finder produces byte-identical output for byte-identical inputs. Reruns the same day overwrite that day's reports cleanly. Reruns on a different day produce a new dated set.

## Anti-reflexivity defense

The autonomous pipeline does **not** preferentially feed already-prominent entities. It scans the whole atlas state each run. The Δ² engine has its own anti-reflexivity audit (`compute_delta_squared.py`) that flags if curator behavior starts preferentially ingesting already-trending entities.

## Provenance

- Orchestrator: `scripts/run_autonomous_discoveries.py`
- Cron: `.github/workflows/autonomous-discoveries.yml` (07:00 UTC daily)
- Spec: items 5 + 7 of the meta-roadmap (autonomous Obsidian pattern engine)

## Master index

See `INDEX.md` for the running list of all daily runs.
