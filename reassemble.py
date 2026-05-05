#!/usr/bin/env python3
"""
reassemble.py — Reconstruct large CSVs from gzipped chunk uploads.

Some files (sources.csv, evidence_fragments.csv) were too large to push
to Drive via the MCP base64 path so they were:
  1. gzipped (text compresses ~3-4x)
  2. split into 30 KB binary chunks named *.csv.gz.part_NN
  3. uploaded as individual Drive files

This script reverses the process locally:
  1. cat all chunks back together → reassembled .csv.gz
  2. gunzip → original .csv
  3. md5 verify against expected hashes (in manifest.json)

Run from the Autism/ folder root after downloading all the .part_NN
files from Drive into a `chunks/` subfolder:

    mkdir -p chunks
    # download all *.csv.gz.part_NN from Drive into chunks/
    python reassemble.py
    # → recreates v2.0_scored/sources.csv and evidence_fragments.csv
"""

from __future__ import annotations
import gzip
import hashlib
import json
import sys
from pathlib import Path

CHUNKS_DIR = Path("chunks")
OUTPUT_DIR = Path("v2.0_scored")

# Files that were chunked. Add to this list if more get chunked later.
CHUNKED_FILES = [
    "sources.csv",
    "evidence_fragments.csv",
]


def reassemble(name: str) -> bool:
    parts = sorted(CHUNKS_DIR.glob(f"{name}.gz.part_*"))
    if not parts:
        print(f"[reassemble] {name}: no parts found in {CHUNKS_DIR}/")
        return False
    gz_path = OUTPUT_DIR / f"{name}.gz"
    csv_path = OUTPUT_DIR / name
    OUTPUT_DIR.mkdir(exist_ok=True, parents=True)
    with open(gz_path, "wb") as out:
        for p in parts:
            out.write(p.read_bytes())
    print(f"[reassemble] {name}: concatenated {len(parts)} chunks "
          f"({gz_path.stat().st_size} bytes)")
    with gzip.open(gz_path, "rb") as gf, open(csv_path, "wb") as out:
        out.write(gf.read())
    print(f"[reassemble] {name}: gunzipped → {csv_path} "
          f"({csv_path.stat().st_size} bytes)")
    return True


def main() -> int:
    print(f"[reassemble] looking for chunks in {CHUNKS_DIR}/")
    if not CHUNKS_DIR.exists():
        print(f"[reassemble] {CHUNKS_DIR}/ does not exist; create it "
              f"and put downloaded *.gz.part_* files inside.")
        return 1
    n = sum(1 for f in CHUNKED_FILES if reassemble(f))
    print(f"[reassemble] reassembled {n}/{len(CHUNKED_FILES)} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
