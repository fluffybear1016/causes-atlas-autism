# Drive sync — what's where, and how to finish it

This document is the bridge between the local Cowork-mounted `Autism/` folder (which is complete) and your Google Drive folder (which has been partially synced via base64 uploads).

## TL;DR

**Local atlas:** complete. Verified 43 files, 14 versioned snapshots, 22 CSVs in `v2.0_scored/`. Calibration 81.95.

**Drive atlas:** partial. v1.0 baseline already there from earlier; selected v2.0 files added to `Autism/Atlas_v2.0/`. The 8 large CSVs (sources, evidence_fragments, evidence_links, score_history, genes, node_aliases, interventions, hypotheses) are too big for the inline base64 upload path.

**Finishing the sync:** one of two paths.

### Path A — gdrive CLI (recommended)

```bash
brew install gdrive            # macOS, or follow github.com/glotlabs/gdrive
gdrive about                    # one-time auth flow

cd ~/path/to/Autism             # local Cowork-synced folder
export AUTISM_DRIVE_FOLDER_ID="1E82AlaqZSjxIXKvEX2g2fIyPdEsoMPki"
bash sync_to_drive.sh
```

This pushes every file in the manifest to your Drive folder using the resumable upload API. No size limits.

### Path B — rclone

```bash
brew install rclone
rclone config                   # set up remote called "gdrive"

cd ~/path/to/Autism
export RCLONE_REMOTE="gdrive:Autism/Atlas_v2.0"
bash sync_to_drive.sh --rclone
```

Same effect, different tool.

### Path C — manual drag-and-drop

Open `Autism/` on your local computer and drag the contents into the Drive `Autism/` folder via your browser. Drive accepts files up to 5 TB this way.

## What's already in Drive (verified)

In `Autism/Atlas_v1/` (v1.0 baseline):
- 6 CSVs as native Google Sheets (hypotheses, mechanisms, phenotypes, interventions, combinations, combination_members)
- 11 edge-table CSVs as plain CSV files
- 4 log CSVs

In `Autism/Atlas_v2.0/` (v2.0, partial — uploaded today):
- MASTER_README.md
- CAUSES_ATLAS_AUTISM_SPEC_v1.2 (header excerpt)
- calibration.txt (proves leucovorin = 81.95)
- combinations.csv (Sheet, includes new dual-scoring columns)
- hypothesis_hypothesis_edges.csv (Sheet — the new v2.0 schema extension)

## What's local-only (need Path A/B/C above)

In `Autism/` root:
- 7 spec docs (MASTER_README.md, CAUSES_ATLAS_AUTISM_SPEC.md v1.0/v1.1/v1.2, MIGRATION_PLAN.md, MIGRATION_IMPLEMENTATION.md, SCORING_ENGINE_SPEC.md)
- 12 Python scripts (migration, scoring v1/v2, ingest pipeline, 9 expansion scripts)
- 9 expansion_v*_summary.json files
- This README, sync_to_drive.sh, reassemble.py, manifest.json

In `Autism/v2.0_scored/`: 22 files (all of v2.0 canonical state), of which the 8 large ones are also chunked into `chunks/` for backup distribution:
- sources.csv (1.8 MB, 17 chunks)
- evidence_fragments.csv (727 KB, 6 chunks)
- node_aliases.csv (417 KB)
- genes.csv (290 KB)
- score_history.csv (170 KB)
- evidence_links.csv (140 KB)
- interventions.csv (43 KB)
- hypotheses.csv (28 KB)

In `Autism/`: 13 versioned snapshots (`output/`, `scored_output/`, `v1.2_expanded/`, `v1.2_scored/` through `v1.9_scored/`) — the audit trail of how the atlas grew.

## After the sync runs

Verify by running on your local machine:

```bash
cd ~/path/to/Autism
python3 -c "
import json
m = json.load(open('manifest.json'))
print('atlas_version:', m['atlas_version'])
print('calibration:', m['calibration'])
print('totals:', m['totals'])
print('files in manifest:', len(m['files']))
"
```

Expected output:
```
atlas_version: v2.0
calibration: {'intervention': 'INT-0001 Leucovorin', 'csrs_score': 81.95,
              'threshold': 80, 'passed': True}
totals: {'hypotheses': 70, 'mechanisms': 33, 'phenotypes': 7,
         'genes': 1564, 'interventions': 99, 'combinations': 5,
         'sources': 1414, 'evidence_fragments': 1414,
         'evidence_links': 1633, 'node_aliases': 5299,
         'score_history': 518}
files in manifest: 55
```

## Why the upload-mechanism gap exists

The MCP `create_file` tool I (Claude) have access to requires the file's full contents as a base64 string in the tool call parameter. Tool parameters count against my output token budget (~32 KB practical limit per call). So files over ~50 KB raw don't fit in a single call. Path A/B/C above all sidestep this — they stream files via Drive's resumable upload API instead.

Once `sync_to_drive.sh` runs once, future syncs are incremental: only new/modified files transfer.

## After this initial sync, future workflow

```bash
# Add a new paper to the atlas (e.g. a new PMID you found)
python3 run_ingest.py pmid 38715916 --output-dir tmp_out --log-dir tmp_logs

# Re-score
python3 run_scoring_v20.py  # (point INPUT_DIR at tmp_out)

# Sync the updated atlas back to Drive
bash sync_to_drive.sh
```

That's the steady-state loop. Every paper you find adds value automatically.
