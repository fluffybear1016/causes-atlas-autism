#!/usr/bin/env python3
"""
test_delta_squared_reflexivity.py — proves the reflexivity audit's FAIL
path actually halts the pipeline.

Approach: synthesize a fake score_history.csv that places top-source-count
entities at the BOTTOM of the previous-run ranking. Sources are then "new"
relative to that fake prev run if their ingestion time post-dates it. The
correlation between current-run new-source-count and prev-run rank should
be very high (curator fed the top of the literature), and the audit
should FAIL.

The test uses a temp working directory so it doesn't touch real history.

Exit:
  0 = audit correctly fired FAIL on the synthetic reflexive scenario
  1 = audit DID NOT fire FAIL (defense is broken; investigate)
"""

from __future__ import annotations
import csv, json, os, pathlib, shutil, subprocess, sys, tempfile
from datetime import datetime, timezone, timedelta
from collections import Counter, defaultdict

REPO   = pathlib.Path(__file__).resolve().parent.parent
ENGINE = REPO / "scripts" / "compute_delta_squared.py"
ATLAS  = REPO / "v2.0_scored"

def main():
    if not ENGINE.exists():
        print(f"FAIL: engine not found at {ENGINE}"); sys.exit(1)

    # 1. Stage a copy of the atlas in a temp workspace, with a fake prev-run
    #    timestamp set BEFORE the current sources' ingestion times so that
    #    the audit treats them as "newly ingested".
    with tempfile.TemporaryDirectory(prefix="d2_reflex_test_") as td:
        tmp = pathlib.Path(td)
        tmp_repo  = tmp / "repo"
        tmp_atlas = tmp_repo / "v2.0_scored"
        tmp_out   = tmp_repo / "delta_squared_v1"
        tmp_out.mkdir(parents=True)
        # Copy only the CSVs the engine reads
        tmp_atlas.mkdir(parents=True)
        for fname in ["sources.csv","evidence_fragments.csv","evidence_links.csv",
                      "hypotheses.csv","interventions.csv","mechanisms.csv"]:
            shutil.copy2(ATLAS / fname, tmp_atlas / fname)
        # Copy engine (we need it to run from this fake repo root)
        scripts_dir = tmp_repo / "scripts"; scripts_dir.mkdir()
        shutil.copy2(ENGINE, scripts_dir / "compute_delta_squared.py")

        # 2. Compute per-entity source counts to build a synthetic prev-run
        #    history where high-source-count entities are RANKED LOW (high
        #    prev_rank ID). When the audit then sees those same entities
        #    "received many new sources", correlation between low rank and
        #    new-source count maps to high "rank=high → new sources=many"
        #    after the engine's sign convention, producing FAIL.
        ent_src_counts = Counter()
        frag2src = {r["id"]: r["source_id"]
                    for r in csv.DictReader(open(tmp_atlas / "evidence_fragments.csv"))}
        for r in csv.DictReader(open(tmp_atlas / "evidence_links.csv")):
            sid = frag2src.get(r["evidence_fragment_id"])
            if sid:
                ent_src_counts[(r["target_type"], r["target_id"])] += 1

        # Build synthetic ranking: order = ASCENDING by source count
        # (so the entities with the MOST sources get the WORST prev_rank).
        # Then when those high-source entities receive "new" sources, the
        # audit's sign convention (xs_signed = -prev_rank, ys = new_sources)
        # gives strong NEGATIVE correlation. To produce a FAIL via the
        # POSITIVE threshold, we need the OPPOSITE: entities with MANY
        # new sources should have the BEST (lowest) prev_rank.
        ranked = sorted(ent_src_counts.items(), key=lambda kv: -kv[1])
        # Best prev_rank (1) goes to the entity with the most sources
        # (Hypothesis / Intervention with most sources). If ALL of those
        # get treated as "newly ingested", and they're ranked 1, 2, 3...,
        # the audit sees: "the top-prev-ranked entities received the most
        # new sources" → reflexivity FAIL. Synthesize the prev-run history
        # with exactly that ordering.

        prev_run_ts = (datetime.now(timezone.utc) - timedelta(days=400)).isoformat(timespec="seconds")
        with open(tmp_out / "score_history.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["run_timestamp","entity_type","entity_id","delta_squared_score",
                        "c1_recency_accel","c2_design_convergence","c3_subset_validation",
                        "c4_replication","c5_trajectory_mismatch","n_sources"])
            # Synthetic scores: highest score for entity with most sources
            max_count = max(ent_src_counts.values()) if ent_src_counts else 1
            for (etype, eid), count in ranked:
                synth_score = 100.0 * count / max_count  # rank-preserving
                w.writerow([prev_run_ts, etype, eid, round(synth_score, 2),
                            0, 0, 0, 0, 0, count])

        # 3. Run the engine in tmp_repo. It should detect that all the
        #    high-prev-rank entities got "new sources" (because all real
        #    sources were ingested in 2026-04, which post-dates our fake
        #    400-days-ago prev-run timestamp). The audit fires FAIL.
        env = os.environ.copy()
        proc = subprocess.run(
            [sys.executable, str(scripts_dir / "compute_delta_squared.py")],
            cwd=str(tmp_repo), env=env, capture_output=True, text=True, timeout=60)
        print("--- stdout ---")
        print(proc.stdout)
        print("--- stderr ---")
        print(proc.stderr)

        # 4. Check audit result
        rs_path = tmp_out / "reflexivity_status.txt"
        if not rs_path.exists():
            print("FAIL: reflexivity_status.txt not produced by engine")
            sys.exit(1)
        text = rs_path.read_text()
        # Read run_summary.json to get the spearman_r
        with open(tmp_out / "run_summary.json") as f:
            summary = json.load(f)
        rstatus = summary["reflexivity"]["status"]
        rval    = summary["reflexivity"]["spearman_r"]
        n_fed   = summary["reflexivity"]["n_entities"]
        print(f"\n=== synthetic reflexive scenario ===")
        print(f"  status:    {rstatus}")
        print(f"  spearman:  {rval}")
        print(f"  entities:  {n_fed}")
        print(f"  exit code: {proc.returncode}")

        if rstatus == "FAIL" and proc.returncode != 0:
            print("\nREFLEXIVITY AUDIT TEST PASSED — defense fires correctly under attack.")
            sys.exit(0)
        else:
            print(f"\nREFLEXIVITY AUDIT TEST FAILED — expected status=FAIL "
                  f"+ non-zero exit, got status={rstatus} exit={proc.returncode}")
            sys.exit(1)

if __name__ == "__main__":
    main()
