#!/usr/bin/env bash
# sync_to_drive.sh — push the entire Autism atlas to your Google Drive
# folder using the github.com/googleworkspace/cli or rclone.
#
# Run this LOCALLY on your machine after installing one of:
#   1) https://github.com/googleworkspace/cli  (recommended)
#   2) https://rclone.org/drive/                 (alternative)
#
# Both bypass the base64 upload limit MCP hits — they stream files via
# Drive's resumable upload API directly.
#
# Usage (option 1 — gdrive CLI):
#     # 1. Install: brew install gdrive
#     # 2. Authenticate: gdrive about
#     # 3. Find your Autism folder ID in Drive (URL after /folders/)
#     export AUTISM_DRIVE_FOLDER_ID="1E82AlaqZSjxIXKvEX2g2fIyPdEsoMPki"
#     bash sync_to_drive.sh
#
# Usage (option 2 — rclone):
#     # 1. Install: brew install rclone
#     # 2. Configure: rclone config (set up Drive remote called "gdrive")
#     # 3. Run:
#     export RCLONE_REMOTE="gdrive:Autism"
#     bash sync_to_drive.sh --rclone

set -euo pipefail

ATLAS_DIR="$(cd "$(dirname "$0")" && pwd)"
echo "[sync] Atlas root: $ATLAS_DIR"

if [[ "${1:-}" == "--rclone" ]]; then
    : "${RCLONE_REMOTE:?Set RCLONE_REMOTE=gdrive:Autism (or your remote)}"
    echo "[sync] Using rclone → $RCLONE_REMOTE"
    rclone sync \
        --include "*.md" --include "*.py" --include "*.json" \
        --include "v2.0_scored/**" \
        --include "logs/**" --include "scoring_logs/**" \
        --progress --check-first \
        "$ATLAS_DIR" "$RCLONE_REMOTE"
    echo "[sync] rclone sync complete"
    exit 0
fi

: "${AUTISM_DRIVE_FOLDER_ID:?Set AUTISM_DRIVE_FOLDER_ID=<your Drive folder ID>}"
echo "[sync] Using gdrive CLI → folder $AUTISM_DRIVE_FOLDER_ID"

# Ensure Atlas_v2.0 subfolder exists in Drive
SUBF=$(gdrive files list \
    --query "name = 'Atlas_v2.0' and '$AUTISM_DRIVE_FOLDER_ID' in parents and trashed = false" \
    --skip-header --max 1 | awk '{print $1}')
if [[ -z "${SUBF:-}" ]]; then
    SUBF=$(gdrive files mkdir Atlas_v2.0 \
            --parent "$AUTISM_DRIVE_FOLDER_ID" | awk '/Id:/ {print $2}')
    echo "[sync] created Drive folder Atlas_v2.0 → $SUBF"
else
    echo "[sync] using existing Drive folder Atlas_v2.0 → $SUBF"
fi

# Upload spec docs and scripts
for f in MASTER_README.md \
         CAUSES_ATLAS_AUTISM_SPEC.md \
         CAUSES_ATLAS_AUTISM_SPEC_v1.1.md \
         CAUSES_ATLAS_AUTISM_SPEC_v1.2.md \
         MIGRATION_PLAN.md \
         MIGRATION_IMPLEMENTATION.md \
         SCORING_ENGINE_SPEC.md \
         run_migration.py \
         run_scoring.py run_scoring_v20.py \
         run_ingest.py \
         run_expansion.py \
         run_expansion_v13.py run_expansion_v14.py run_expansion_v15.py \
         run_expansion_v16.py run_expansion_v17.py run_expansion_v18.py \
         run_expansion_v19.py run_expansion_v20.py \
         expansion_summary.json \
         expansion_v13_summary.json expansion_v14_summary.json \
         expansion_v15_summary.json expansion_v16_summary.json \
         expansion_v17_summary.json expansion_v18_summary.json \
         expansion_v19_summary.json expansion_v20_summary.json \
         sync_to_drive.sh reassemble.py manifest.json \
         README_DRIVE_SYNC.md; do
    if [[ -f "$ATLAS_DIR/$f" ]]; then
        echo "[sync] uploading $f"
        gdrive files upload --parent "$SUBF" "$ATLAS_DIR/$f" >/dev/null
    fi
done

# Upload v2.0_scored CSVs (the latest canonical state)
V20_SUBF=$(gdrive files mkdir v2.0_scored --parent "$SUBF" 2>/dev/null \
    | awk '/Id:/ {print $2}')
[[ -z "${V20_SUBF:-}" ]] && V20_SUBF=$(gdrive files list \
    --query "name = 'v2.0_scored' and '$SUBF' in parents and trashed = false" \
    --skip-header --max 1 | awk '{print $1}')

for f in "$ATLAS_DIR"/v2.0_scored/*.csv "$ATLAS_DIR"/v2.0_scored/*.txt \
         "$ATLAS_DIR"/v2.0_scored/*.json; do
    [[ -f "$f" ]] || continue
    echo "[sync] v2.0_scored/$(basename "$f")"
    gdrive files upload --parent "$V20_SUBF" "$f" >/dev/null
done

echo "[sync] done — Drive folder is now in sync with local atlas"
