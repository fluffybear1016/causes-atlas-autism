#!/usr/bin/env python3
"""run_ingest_grok.py — ingest X (Twitter) signal via the Grok API.

Item 6 of the meta-roadmap. X is a high-signal stream for autism /
biomarker / functional-medicine content (researchers, parents,
contested-evidence debate). Grok's API exposes search over X plus an
LLM that can answer questions ABOUT X content.

CRITICAL: same verify-before-write protocol as PMID ingestion. We do NOT
trust Grok's LLM responses as a source of truth. We use Grok only to
SURFACE candidate X posts; verification is human-in-the-loop with the
post's URL + author + content read directly.

Determinism: HTTP responses from Grok will not be byte-identical across
runs (X stream is dynamic). The script writes timestamped candidates
that downstream curator review processes per the standard workflow.

Usage:
    export GROK_API_KEY=...    # from https://console.x.ai
    python3 scripts/run_ingest_grok.py search --query "FRAA folate autism"
    python3 scripts/run_ingest_grok.py search --query "bumetanide autism" --max 20
    python3 scripts/run_ingest_grok.py search --query "PANS PANDAS Cunningham" --since 7d

Output:
    freshness/grok_candidates_{date}.json — candidate X posts for curator review

Environment variables:
    GROK_API_KEY  — required; xAI API key (https://console.x.ai)
    GROK_MODEL    — optional; defaults to "grok-2-latest"

Spec compliance:
    - Treats X posts as `study_design=other` and `source_type=social`
      (lowest tier weight per CLAUDE.md §source-quality hierarchy)
    - Down-weighted automatically in scoring; user must elevate manually
      with explicit reasoning if a post warrants higher weight
    - Verification metadata required: author handle + post URL + post date
      + key term match before any atlas write
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FRESHNESS_DIR = ROOT / "freshness"
FRESHNESS_DIR.mkdir(parents=True, exist_ok=True)

GROK_API_BASE = "https://api.x.ai/v1"
GROK_MODEL_DEFAULT = "grok-2-latest"
TIMEOUT_SECONDS = 30


def _post(endpoint: str, payload: dict, api_key: str) -> dict:
    """Make a POST request to the Grok API. Returns parsed JSON."""
    url = f"{GROK_API_BASE}{endpoint}"
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Grok API HTTP {e.code}: {body}") from e


def search_x(query: str, api_key: str, max_results: int = 10, since: str = "30d") -> dict:
    """
    Use Grok's chat completion endpoint with X-search-grounded mode to
    surface relevant recent posts. Returns the raw API response plus a
    parsed list of candidate posts.

    Note: as of v1, xAI's API uses `search_parameters` to enable live X
    search. The exact field names may evolve — see https://docs.x.ai for
    current spec. We construct the request to be compatible with the
    documented v1 schema.
    """
    payload = {
        "model": os.environ.get("GROK_MODEL", GROK_MODEL_DEFAULT),
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an unbiased research assistant indexing X (Twitter) "
                    "posts for an autism-causation atlas. Return ONLY a JSON "
                    "array of objects with fields: author_handle, post_url, "
                    "post_date_iso, content_excerpt, key_term_matches. Do NOT "
                    "summarize or interpret — return verbatim post excerpts only. "
                    "If no relevant posts are found, return an empty array."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Search X posts from the last {since} matching the query: "
                    f'"{query}". Return up to {max_results} most relevant posts. '
                    f"Output strictly JSON array; no surrounding prose."
                ),
            },
        ],
        "search_parameters": {
            "mode": "on",
            "sources": [{"type": "x"}],
            "max_search_results": max_results,
        },
        "temperature": 0,
    }

    raw = _post("/chat/completions", payload, api_key)

    # Parse the model's JSON response (defensive)
    candidates = []
    try:
        choice = raw.get("choices", [{}])[0]
        content = choice.get("message", {}).get("content", "")
        # Try to find a JSON array in the response
        first_bracket = content.find("[")
        last_bracket = content.rfind("]")
        if first_bracket != -1 and last_bracket > first_bracket:
            candidates = json.loads(content[first_bracket : last_bracket + 1])
    except (json.JSONDecodeError, IndexError, KeyError):
        pass

    return {
        "query": query,
        "since": since,
        "max_results": max_results,
        "raw_response": raw,
        "parsed_candidates": candidates,
    }


def write_candidates(query: str, search_result: dict, date_str: str) -> Path:
    """Write candidates to freshness/grok_candidates_{date}.json for curator review."""
    out_path = FRESHNESS_DIR / f"grok_candidates_{date_str}.json"
    existing = []
    if out_path.exists():
        try:
            existing = json.loads(out_path.read_text())
        except json.JSONDecodeError:
            existing = []

    record = {
        "query": query,
        "since": search_result["since"],
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "candidates": search_result["parsed_candidates"],
        "candidate_count": len(search_result["parsed_candidates"]),
    }
    existing.append(record)
    out_path.write_text(json.dumps(existing, indent=2, sort_keys=True) + "\n")
    return out_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("search", help="Search X via Grok API")
    s.add_argument("--query", required=True)
    s.add_argument("--max", type=int, default=10, dest="max_results")
    s.add_argument("--since", default="30d", help="lookback window (e.g. 7d, 30d)")
    s.add_argument("--date", default=datetime.utcnow().strftime("%Y-%m-%d"))

    args = parser.parse_args(argv)

    api_key = os.environ.get("GROK_API_KEY")
    if not api_key:
        print(
            "ERROR: GROK_API_KEY environment variable not set.\n"
            "  Get a key at https://console.x.ai\n"
            "  Then: export GROK_API_KEY=...",
            file=sys.stderr,
        )
        return 2

    if args.cmd == "search":
        try:
            result = search_x(
                args.query, api_key, max_results=args.max_results, since=args.since
            )
        except RuntimeError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            return 1
        out_path = write_candidates(args.query, result, args.date)
        print(f"Wrote {len(result['parsed_candidates'])} candidates → {out_path}")
        for c in result["parsed_candidates"][:5]:
            print(
                f"  • {c.get('author_handle', '?')} — "
                f"{c.get('content_excerpt', '')[:120]}"
            )
        print()
        print("Curator next steps:")
        print("  1. Open each candidate's post_url to verify it exists.")
        print(
            "  2. Confirm author + date + key term match per the verify-before-write "
            "protocol."
        )
        print(
            "  3. If valuable, run: `python3 run_ingest.py paste --platform x "
            "--external_id <post_id> ...`"
        )
        print(
            "  4. Source will be tagged source_type=social and weighted at "
            "tier-5 level. Manually elevate weight only with explicit reasoning."
        )
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
