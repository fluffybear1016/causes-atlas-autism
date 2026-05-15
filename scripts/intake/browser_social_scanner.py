#!/usr/bin/env python3
"""
scripts/intake/browser_social_scanner.py — browser-based Twitter/X + Reddit
scanner.

Since the user does not yet have Twitter/Reddit API credentials, this
scanner uses Playwright (headless Chromium) to render specific accounts
and subreddits and extract candidate signals.

This file is the **scanner harness**: it lays out the target accounts and
subreddits, the per-source extraction rules, and the candidate-record
schema. Running it requires Playwright to be installed locally
(`pip install playwright && playwright install chromium`). On the user's
Mac with FileVault on, this is safe — no credentials are stored and no
authenticated browsing is performed (public-page scraping only).

CI compatibility: this scanner is intentionally OFF by default in the
GitHub Actions cron because GitHub-hosted runners block Twitter's
JS-rendered content and Reddit's rate limits. It's designed for local
cron on the user's machine. The PubMed RSS scanner runs in CI; this
scanner runs locally.

Hannah Poling P x E -> M -> Phi tagging: every candidate is tagged
P/E/M/PHI/SYNTHESIS by the orchestrator's classifier downstream.

Run command:
  python3 scripts/intake/browser_social_scanner.py
  python3 scripts/intake/browser_social_scanner.py --dry-run
  python3 scripts/intake/browser_social_scanner.py --source twitter
  python3 scripts/intake/browser_social_scanner.py --source reddit
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

_CANDIDATE_REPOS = [
    Path("/Users/Greg/Autism"),
    Path("/sessions/jolly-determined-darwin/mnt/Autism"),
]
REPO = next((p for p in _CANDIDATE_REPOS if p.exists()), _CANDIDATE_REPOS[0])
INBOX = REPO / "vault" / "Discoveries_Inbox"


# --------------------------------------------------------------------------
# Targets
# --------------------------------------------------------------------------

TWITTER_ACCOUNTS = [
    # Curator-curated researchers + advocates who routinely post primary
    # autism-research links. Public accounts only. Update list quarterly.
    {"handle": "NicHulscher",     "focus": "vaccine + iatrogenic + ASD"},
    {"handle": "P_McCulloughMD",  "focus": "vaccine + iatrogenic + ASD"},
    {"handle": "MASTERJOHN",      "focus": "methylation + nutrition + ASD"},
    {"handle": "DrAseemMalhotra", "focus": "iatrogenic + cardiometabolic"},
    {"handle": "RWMaloneMD",      "focus": "vaccine + immunology"},
    # Add mainstream researcher handles when known to post primary papers:
    {"handle": "DrFrye",          "focus": "mitochondrial + cerebral folate"},
    {"handle": "WalshInstitute",  "focus": "Walsh methylation phenotypes"},
    {"handle": "MAPSResearch",    "focus": "functional medicine ASD"},
]

REDDIT_SUBS = [
    {"name": "r/autism",                 "focus": "lived experience signal"},
    {"name": "r/ScienceBasedParenting",  "focus": "research-leaning parent community"},
    {"name": "r/medicine",               "focus": "clinician discussion"},
    {"name": "r/AskDocs",                "focus": "clinician answer thread"},
    {"name": "r/MTHFR",                  "focus": "methylation lived experience"},
    {"name": "r/PANS_PANDAS",            "focus": "PANS overlap signal"},
    {"name": "r/MCAS",                   "focus": "MCAS overlap signal"},
    {"name": "r/MitochondrialDiseases",  "focus": "mito-vulnerable subset signal"},
]


# --------------------------------------------------------------------------
# Extraction (Playwright-based)
# --------------------------------------------------------------------------

def have_playwright() -> bool:
    try:
        import playwright  # noqa: F401
        return True
    except ImportError:
        return False


def scrape_twitter(handles: list[dict], headless: bool = True) -> list[dict]:
    """Open each X account profile, extract recent post text + linked URLs.

    Note: Twitter's API restrictions make scraping fragile. This function
    captures public profile content; it does NOT log in. If X requires
    login (increasingly common), this returns an empty list and the
    orchestrator falls back to logging the failure.
    """
    if not have_playwright():
        print("  Playwright not installed. Install with:")
        print("    pip install playwright && playwright install chromium")
        return []

    from playwright.sync_api import sync_playwright

    candidates = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=headless)
        try:
            context = browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
                viewport={"width": 1280, "height": 1024},
            )
            page = context.new_page()
            for acct in handles:
                url = f"https://x.com/{acct['handle']}"
                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=15000)
                    page.wait_for_timeout(2000)
                    # Look for tweet-text containers; X uses
                    # data-testid="tweetText" for post bodies.
                    texts = page.locator('[data-testid="tweetText"]').all_text_contents()
                    links = page.locator('a[href*="pubmed.ncbi.nlm.nih.gov"], '
                                         'a[href*="doi.org"], '
                                         'a[href*="biorxiv"], '
                                         'a[href*="medrxiv"]').evaluate_all(
                        "els => els.map(e => e.href)"
                    )
                    candidates.append({
                        "source": "twitter",
                        "handle": acct["handle"],
                        "focus_hint": acct["focus"],
                        "url": url,
                        "post_count": len(texts),
                        "posts_sample": texts[:10],
                        "linked_papers": list(set(links)),
                        "scraped_at": datetime.now(timezone.utc).isoformat(),
                    })
                    print(f"  twitter:{acct['handle']:18s} posts={len(texts)} links={len(links)}")
                except Exception as e:
                    print(f"  twitter:{acct['handle']:18s} FAIL {type(e).__name__}: {e}")
                    candidates.append({
                        "source": "twitter",
                        "handle": acct["handle"],
                        "error": str(e),
                        "scraped_at": datetime.now(timezone.utc).isoformat(),
                    })
                time.sleep(2)  # be polite
        finally:
            browser.close()
    return candidates


def scrape_reddit(subs: list[dict], headless: bool = True) -> list[dict]:
    """Open each subreddit's `top weekly` view and extract post titles + links."""
    if not have_playwright():
        return []

    from playwright.sync_api import sync_playwright

    candidates = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=headless)
        try:
            context = browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
                viewport={"width": 1280, "height": 1024},
            )
            page = context.new_page()
            for sub in subs:
                slug = sub["name"].replace("r/", "").strip()
                url = f"https://old.reddit.com/r/{slug}/top/?sort=top&t=week"
                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=15000)
                    page.wait_for_timeout(1500)
                    titles = page.locator("a.title").all_text_contents()
                    hrefs = page.locator("a.title").evaluate_all(
                        "els => els.map(e => e.href)"
                    )
                    candidates.append({
                        "source": "reddit",
                        "subreddit": sub["name"],
                        "focus_hint": sub["focus"],
                        "url": url,
                        "post_count": len(titles),
                        "posts": [
                            {"title": t, "url": h}
                            for t, h in list(zip(titles, hrefs))[:25]
                        ],
                        "scraped_at": datetime.now(timezone.utc).isoformat(),
                    })
                    print(f"  reddit:{sub['name']:25s} posts={len(titles)}")
                except Exception as e:
                    print(f"  reddit:{sub['name']:25s} FAIL {type(e).__name__}: {e}")
                time.sleep(2)
        finally:
            browser.close()
    return candidates


# --------------------------------------------------------------------------
# Render
# --------------------------------------------------------------------------

def render_md(today: str, twitter: list[dict], reddit: list[dict]) -> str:
    lines = [
        f"# Browser social-signal intake — {today}",
        "",
        "Public-page scrape (no authenticated browsing) of curator-curated "
        "Twitter/X accounts and Reddit subreddits where primary autism-"
        "research links are routinely posted. Goal: surface PMIDs / DOIs / "
        "preprint URLs the PubMed RSS scanner would miss — papers that "
        "haven't been indexed yet, or that are being discussed before they "
        "are picked up by formal scanners.",
        "",
        "These are NOT atlas changes — candidates for curator review. Per "
        "CLAUDE.md Sec.24 verify-before-write, every claimed PMID/DOI must "
        "be re-verified before atlas write.",
        "",
        "## Targets",
        "",
        f"- Twitter/X accounts scanned: **{len(twitter)}**",
        f"- Reddit subreddits scanned: **{len(reddit)}**",
        "",
        "## Twitter/X signals",
        "",
    ]
    for t in twitter:
        if "error" in t:
            lines.append(f"### @{t['handle']} — error")
            lines.append(f"- focus: {t.get('focus_hint', '')}")
            lines.append(f"- error: `{t['error']}`")
            lines.append("")
            continue
        lines.append(f"### @{t['handle']} — {t.get('focus_hint', '')}")
        lines.append(f"- profile: {t['url']}")
        lines.append(f"- posts captured: {t['post_count']}")
        if t.get("linked_papers"):
            lines.append("- **Linked primary papers (PMID/DOI/preprint):**")
            for link in t["linked_papers"]:
                lines.append(f"  - {link}")
        lines.append("")

    lines.append("## Reddit signals")
    lines.append("")
    for r in reddit:
        lines.append(f"### {r['subreddit']} — {r.get('focus_hint', '')}")
        lines.append(f"- top-week URL: {r['url']}")
        lines.append(f"- posts captured: {r['post_count']}")
        for p in r.get("posts", [])[:5]:
            lines.append(f"  - [{p['title']}]({p['url']})")
        lines.append("")

    lines.extend([
        "## Curator workflow",
        "",
        "1. Open each linked-paper URL. Resolve to a PMID via PubMed if "
        "possible.",
        "2. PMID-verify (author + year + title-keyword) before any atlas "
        "write per CLAUDE.md Sec.24.",
        "3. If signal is a Reddit thread with lived-experience pattern "
        "(e.g. 'my child responded to leucovorin after FOLR1+ test'), "
        "create a responder-rate candidate in the cohort.yaml only after "
        "the underlying paper is found and PMID-verified.",
        "",
        "## Anti-reflexivity note",
        "",
        "Target list is fixed in this file. Editing the target list shifts "
        "what gets surfaced — if you find yourself only adding accounts "
        "that agree with the current atlas, the reflexivity audit will "
        "catch it on the next Delta-squared run.",
    ])
    return "\n".join(lines)


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", choices=["all", "twitter", "reddit"],
                    default="all")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-headless", action="store_true",
                    help="Show browser (useful for debugging)")
    args = ap.parse_args(argv)

    if not have_playwright():
        print("ERROR: Playwright not installed.")
        print("Install with:")
        print("  pip install playwright")
        print("  playwright install chromium")
        print()
        print("This scanner is designed for local cron on the user's Mac, "
              "not for GitHub Actions runners.")
        return 1

    twitter_data = []
    reddit_data = []

    if args.source in ("all", "twitter"):
        print("=== Twitter/X scan ===")
        if args.dry_run:
            print(f"  (dry-run: would scrape {len(TWITTER_ACCOUNTS)} accounts)")
        else:
            twitter_data = scrape_twitter(TWITTER_ACCOUNTS,
                                          headless=not args.no_headless)
        print()

    if args.source in ("all", "reddit"):
        print("=== Reddit scan ===")
        if args.dry_run:
            print(f"  (dry-run: would scrape {len(REDDIT_SUBS)} subreddits)")
        else:
            reddit_data = scrape_reddit(REDDIT_SUBS,
                                        headless=not args.no_headless)
        print()

    if args.dry_run:
        print("Dry run — no files written.")
        return 0

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    INBOX.mkdir(parents=True, exist_ok=True)
    md_path = INBOX / f"social_intake_{today}.md"
    json_path = INBOX / f"social_intake_{today}.json"
    json_path.write_text(json.dumps(
        {"date": today, "twitter": twitter_data, "reddit": reddit_data},
        indent=2,
    ))
    md_path.write_text(render_md(today, twitter_data, reddit_data))
    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
