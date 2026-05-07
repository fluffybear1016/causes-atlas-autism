#!/usr/bin/env python3
"""
DEPRECATED — this script has moved to scripts/compute_delta_squared.py
as part of the v1.1 production integration (2026-05-05).

This stub re-execs the new location so any cron job / CI invocation that
still points at the old path keeps working with a clear warning.

Remove this stub once nothing references it.
"""
import os, sys, pathlib, subprocess
new = pathlib.Path(__file__).resolve().parent / "scripts" / "compute_delta_squared.py"
sys.stderr.write(
    "[DEPRECATED] compute_delta_squared.py at repo root has moved to "
    "scripts/compute_delta_squared.py. Update your invocation. "
    "Re-execing the new location now.\n"
)
sys.exit(subprocess.run([sys.executable, str(new)] + sys.argv[1:]).returncode)
