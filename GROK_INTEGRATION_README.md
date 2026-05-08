# Grok API integration (item 6 of meta-roadmap)

X (Twitter) is a high-signal stream for autism research:

- Researchers post preprints + commentary
- Parents share anecdotal observations on interventions
- Contested-evidence debates surface earlier here than in journals
- Functional medicine clinicians publish protocols
- Atlas-relevant figures (Frye, Walsh, Klinghardt, Naviaux, etc.) are active

The Grok API (`api.x.ai`) provides:

- Live X search grounded responses
- LLM-style retrieval with verbatim post excerpts
- Author + date + URL + content extraction

This integration is scaffolded but **not auto-running** — it requires an API key (free dev tier exists; paid for higher volume).

## Setup

1. Create an account at https://console.x.ai
2. Generate an API key in the console
3. Export the key:
   ```bash
   export GROK_API_KEY=xai-...
   ```
4. (Optional) Choose a model:
   ```bash
   export GROK_MODEL=grok-2-latest  # default
   ```

## Usage

### Search X for a topic

```bash
# Recent FRAA folate autism discussion
python3 scripts/run_ingest_grok.py search \
    --query "FRAA folate autism" \
    --since 30d --max 20

# PANS / Cunningham panel
python3 scripts/run_ingest_grok.py search \
    --query "PANS PANDAS Cunningham" \
    --since 14d

# Specific researcher
python3 scripts/run_ingest_grok.py search \
    --query "@RichardEFrye autism" \
    --since 60d
```

Output: `freshness/grok_candidates_{date}.json` with verbatim post excerpts + author handles + URLs.

### Promote a candidate to the atlas

After review, use the existing paste-ingestion path:

```bash
python3 run_ingest.py paste \
    --title "X post by @RichardEFrye on FRAA-positive responder rate" \
    --platform x \
    --external_id "1234567890" \
    --type social \
    --year 2026 \
    --content "Verbatim post text here..."
```

The atlas tags X-derived sources as `source_type=social` and weights them at tier-5 level (lowest). To elevate weight, manually edit the source row with explicit reasoning per the spec.

## Verification protocol

Same hard rules as PMID ingestion (`CLAUDE.md` §Verification protocol):

1. **Author + date + content match.** Open the post URL directly; verify the post exists and matches Grok's excerpt.
2. **No memory-based fabrication.** Don't ingest a post Grok claims to have found if you can't verify it on X yourself.
3. **PMID-equivalent integrity.** X posts cite primary literature; chase those PMIDs and verify them on PubMed esummary before adding any atlas claim derived from the post.

## Use cases

| Use case | Query template | Frequency |
|---|---|---|
| Track a specific researcher | `@HandleName autism` | weekly |
| Surface emergent debate | `<biomarker> <intervention> autism` | daily |
| Find anecdotal cohort signal | `liposomal glutathione autism son daughter` | weekly |
| Watch contested-evidence shift | `<contested topic> evidence` | monthly |
| Conference live-tweets | `IMFAR <year> OR ACAM <year>` | event-driven |

## What this does NOT do

- **Does NOT auto-write to atlas.** Manual review + verify-before-write are required.
- **Does NOT bypass the source-quality hierarchy.** X posts are tier-5 by default.
- **Does NOT use Grok's LLM as a source of truth.** Grok is used only to SURFACE candidate X posts; the posts themselves are the source content.
- **Does NOT replace PubMed ingestion.** PubMed remains the canonical evidence stream; X is supplementary.

## Cost

xAI free tier (as of 2026-05): generous for low-volume curator queries. Estimated cost for daily use across the atlas: $0-15/month at moderate volume. See https://docs.x.ai/api for current pricing.

## Roadmap

- v0.1 (this session): scaffolded `run_ingest_grok.py` search command
- v0.2: GitHub Actions cron for auto-search on a curated query list
- v0.3: surface candidates in the Discoveries Inbox alongside pattern-miner output

Daily auto-search is intentionally NOT enabled in v0.1 — we want the curator to drive queries until the integration is field-tested.
