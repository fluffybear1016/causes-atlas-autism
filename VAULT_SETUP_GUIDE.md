# VAULT_SETUP_GUIDE — Replicate this for your own knowledge

> The same Connector / Briefer / Catcher pattern that runs on the Causes Atlas runs on any knowledge base. Whether you're a solo researcher mapping a chronic condition, a parent tracking your child's interventions and biomarkers over years, or a clinician building an evidence base for your practice — the architecture is the same. This guide tells you how to clone it.

---

## What you're cloning

The Causes Atlas runs four pipelines in parallel:

```
Reader     → ingests new content (PubMed, X, podcasts, voice notes)
              into the vault automatically
Connector  → finds connections between fresh and old notes overnight
              (deterministic; no LLMs in the math)
Velocity   → tracks research-attention trajectory per entity
              (Δ² overlay; flags accelerating signals)
Briefer    → writes a 3-finding morning brief + a weekly synthesis
              into your inbox by 6 AM
Catcher    → captures any voice/text idea from your phone via
              Telegram bot, lands in inbox in 30s
```

This is the **cyrilXBT solo-trader-second-brain pattern** ($120/mo, $30K/mo returns, no Bloomberg, no team). Adapted here for medical research, but it generalizes to any domain where evidence accumulates faster than you can read it.

---

## The 4-question synthesis (the engine of compounding)

Run this prompt against your vault every Monday. **It is the highest-leverage 15 minutes of the week**:

```
Read the entire vault. Focus on everything added in the last 7 days.

I want four things:

1. EMERGING THESIS — What idea am I building toward without having
   stated it explicitly yet? What position is forming in my thinking?

2. CONTRADICTIONS — What have I saved recently that contradicts
   something I believed before? Show me both sides from my own notes.

3. KNOWLEDGE GAPS — Based on what I am reading and thinking about,
   what am I clearly NOT reading that I should be? What perspective
   is missing?

4. ONE ACTION — Given everything in this vault, what is the single
   highest-leverage thing I could do or think about this week?

Be direct. Challenge me. Do not summarize what I already know.
```

After three months of weekly synthesis, the vault knows your thinking better than you do. After six months, the gap between you and someone who started later is uncloseable by working harder. Only by starting earlier.

---

## Setup in one weekend

### Hour 1 — Five-folder structure

```
~/your-vault/
  inbox/        ← all unprocessed captures land here first
  notes/        ← processed articles, highlights, podcast transcripts
  ideas/        ← your own thinking, observations, voice notes
  projects/     ← active work, one folder per project
  VAULT.md      ← the orchestrator instruction file (see below)
```

That's it. Don't over-engineer. Five folders. When in doubt, put it in `inbox/`.

### Hour 2 — Capture without friction

Pick the tools that match your domain:

| Domain | Capture stack |
|---|---|
| Trader / investor | Readwise (articles), Airr (podcasts), Telegram bot (voice/text), Twitter bookmarks via Readwise |
| Researcher / academic | Zotero → Obsidian, PubMed RSS, ResearchGate alerts, Telegram bot |
| Parent / family-health | Telegram bot (symptom log, food log, supplement reactions), photo OCR for lab reports, voice memo for doctor visits |
| Clinician | Granola or Otter for visit transcripts, Telegram bot for shower-thoughts, RSS for new RCTs in your specialty |
| **Causes Atlas equivalent** | `run_ingest.py pmid <ID>` (PMID), `run_ingest_grok.py search` (X), `run_ingest.py paste` (any text) |

**The rule:** if capturing something takes more than 10 seconds of manual effort, you'll stop doing it under cognitive load. Optimize aggressively for friction-zero.

### Hour 3 — Author your VAULT.md

This is the most important file. Without it, every AI agent reading your vault starts cold. With it, the agent has been your collaborator for months.

Template:

```markdown
# VAULT.md

> The orchestrator file. Tells any AI reading this vault what to do.

## Who I am
Name: [your name]
Work: [what you do, specific]
Focus: [the one thing you're getting better at right now]
Goals 2026: [3 specific outcomes]

## Current projects
Active: [what you're building]
Stuck on: [where you need thinking help]
Next milestone: [what done looks like]

## How this vault works
inbox/      unprocessed captures, file here first
notes/      processed articles, research, transcripts
ideas/      my own thinking
projects/   active work folders

## What I want from any AI reading this
- Surface connections I haven't seen
- Challenge my assumptions before agreeing
- When I ask what to focus on, answer from vault context, not generically
- Flag when something I believe contradicts something I saved earlier
- Cite specific notes by filename + date when making claims

## Pipelines running on this vault
[Reader / Connector / Velocity / Briefer / Catcher per your stack]

## Wake me only when
- A fresh note contradicts my active thesis, OR
- A candidate finding has confidence ≥0.90, OR
- [some domain-specific tripwire]

## Update weekly (5 minutes Monday morning)
- Current projects section
- "What I'm reading and thinking about" section
- Add new pipeline if one was set up this week
```

### Hour 4 — Daily brief automation

Pick one of:

**Option A — N8N (cyrilXBT pattern, web-based):**
1. Self-host N8N or use cloud (free tier)
2. Workflow: cron 6 AM → fetch vault contents from last 24h → send to Claude API → write response to `inbox/brief-{date}.md`
3. ~30 minutes to build with their UI

**Option B — GitHub Actions (Causes Atlas pattern):**
1. Repo with vault as folder
2. `.github/workflows/morning_brief.yml` runs at 6 AM UTC
3. Calls a Python script that reads the vault, sends to Claude API, commits brief back
4. ~20 minutes to set up

**Option C — Cron + shell script (simplest):**
1. Local script that reads vault, calls Claude CLI, writes to inbox
2. crontab entry: `0 6 * * 1-5 /path/to/morning_brief.sh`
3. ~15 minutes

Whichever option, **the prompt is what matters**. Use the morning brief prompt from VAULT.md or the cyrilXBT version.

### Hour 5 — Weekly synthesis (manual, 15 min)

Don't automate this one yet. The 4-question prompt is so high-leverage that you want the friction of opening Claude (or your AI of choice) and pasting it manually so you actually read the response.

Block 15 minutes every Monday. Calendar it. Do not skip in week 2 because the vault feels empty. The vault is never too empty to find something worth thinking about.

### Hour 6 — Telegram capture bot (optional but life-changing)

For voice/text capture from your phone:
1. Create a Telegram bot via @BotFather (5 min)
2. N8N workflow: Telegram trigger → format as markdown → write to `inbox/{date}-quick-capture.md`
3. Now any thought that hits you in the car / walking / shower goes into the vault in 30 seconds

---

## How the Causes Atlas does this

Mapped to the cyrilXBT pattern:

| cyrilXBT pipeline | Causes Atlas equivalent |
|---|---|
| Reader (Readwise + Twitter + Kindle) | `.github/workflows/daily_ingestion.yml` + PubMed RSS + `run_ingest_grok.py` |
| Listener (Airr + Whisper) | Not used (atlas is text-only); could add for clinical-conference recordings |
| Catcher (Telegram bot) | `run_ingest.py paste` for ad-hoc; could add Telegram for X-bookmark capture |
| Connector (overnight graph update) | `run_autonomous_discoveries.py` (4 pattern miners + orchestrator) |
| Briefer (6 AM morning brief) | Not yet automated — VAULT.md provides the prompt; daily Discoveries_Inbox is its current form |
| Mobile (iPhone voice query) | Not yet built — would be the Streamlit / FastAPI parent UI on mobile |

What's already running:
- **Daily ingestion** (06:00 UTC) — PubMed RSS for new autism research, verify-before-write
- **Autonomous discoveries** (07:00 UTC) — 4 pattern miners, output to Discoveries Inbox
- **Δ² research-attention velocity** — tracks evidence-trajectory per entity
- **Anti-reflexivity audit** — code-enforced check that ingestion isn't preferentially feeding already-trending entities

What's missing that you'd add for a personal vault:
- A 6 AM Briefer that emails/pushes the day's connections (the Causes Atlas writes to a Markdown inbox; for personal use you'd want push notifications)
- Voice query layer (the Mobile pipeline)

---

## What changes after 1, 3, 6, 12 months

| Time | What it feels like |
|---|---|
| **1 month** | A useful tool. You're saving more, losing fewer ideas. The morning brief occasionally surfaces something interesting. |
| **3 months** | Different. Claude connects month-1 to month-3 things. You ask about a current problem; it finds the relevant note from 8 weeks ago you'd forgotten. |
| **6 months** | A record of every belief you held + changed. Every question you sat with + the answer that emerged. Every pattern that showed up in your reading before you consciously named it. |
| **12 months** | The AI that's been reading your mind while you lived your life. Your competitor who starts the system 6 months after you isn't behind on setup — they're behind on 6 months of compounding connections. That gap doesn't close by working harder. |

---

## Start today with five notes

The most common reason people never build this system is that it feels like too much to set up at once.

Don't try to build the whole stack in a weekend. **Start with five notes**:
1. Five articles you've been meaning to read
2. Or five ideas that have been sitting in your head
3. Or five questions you keep returning to

Put them in a folder. Connect Claude. Ask it to find connections across those five notes.

It will find something you missed. It always does. **That moment** — when Claude surfaces a connection between two things you thought were unrelated — is when the system stops being a concept and starts being something you want to feed every day.

Then you build pipelines around it.

---

## Why we're publishing this

The Causes Atlas is open-source MIT. The whole substrate — engine, scoring, verification protocol, autonomous discoveries pipeline, Δ² overlay — is forkable for any chronic condition. But the substrate is also forkable for **any knowledge domain**: trading (cyrilXBT), academic research, clinical practice, parenting, journalism, anything where evidence accumulates faster than you can read it.

The architecture is open. The principles are open (verify-before-write, contested-evidence preservation, determinism, individual-level over population-level, Hannah Poling framework as the framing principle for any heterogeneous-effect domain). The code is open.

People can replicate this. They should.

---

## Resources

- **Causes Atlas repo**: https://github.com/abel-causesatlas/Autism (MIT license)
- **cyrilXBT thread on Twitter** ([@cyrilXBT](https://x.com/cyrilXBT)) — N8N workflows, CLAUDE.md templates
- **VAULT.md** in the repo root — the orchestrator file we use
- **ATLAS_OS_README.md** — multi-atlas substrate documentation
- **CONTRIBUTING.md** — hard rules + verify-before-write protocol

---

*Author: Greg [LAST]. License: MIT.*
*The Causes Atlas substrate is open source. Same engine + protocol works for any complex chronic condition or any knowledge domain.*
