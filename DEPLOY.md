# Deploy — getting Causes Atlas (Autism) to a live public URL

Two surfaces to deploy, and they can be deployed independently:

1. **Calculator app** (interactive, runs the engine) → Streamlit Community Cloud (free).
2. **Landing page** (static, narrative, Jobs/Ive design) → Vercel, Netlify, or GitHub Pages (all free).

## Surface 1 — Calculator app (Streamlit Community Cloud)

**Time to live URL:** ~5 minutes from a fresh GitHub repo.

### Prerequisites

- GitHub account.
- A public GitHub repo containing this codebase.
- A Streamlit Community Cloud account (sign in with GitHub at https://share.streamlit.io).

### Steps

1. **Push the repo to GitHub.** From the project root:

   ```bash
   git init
   git add .
   git commit -m "Initial commit — Causes Atlas (autism) v0.3"
   gh repo create causes-atlas-autism --public --source=. --push
   # or: create the repo on github.com, then:
   #   git remote add origin https://github.com/<you>/causes-atlas-autism.git
   #   git branch -M main
   #   git push -u origin main
   ```

2. **Go to https://share.streamlit.io** and sign in with the GitHub account
   that owns the repo.

3. Click **New app** → fill in:
   - **Repository**: `<your-username>/causes-atlas-autism`
   - **Branch**: `main`
   - **Main file path**: `ui/app.py`
   - **Python version**: `3.11`
   - **App URL**: choose a subdomain (e.g., `causes-atlas-autism`)

4. Click **Deploy**. Build takes ~3 min on the first deploy
   (Streamlit clones the repo, installs `requirements.txt`, then boots).

5. You'll get a URL of the form:
   ```
   https://causes-atlas-autism.streamlit.app
   ```
   That's the live URL. Share it.

### What's already configured for you

- `requirements.txt` at the repo root — Streamlit Cloud picks this up
  automatically. Pinned: `streamlit>=1.40`, `pyyaml>=6.0`.
- `.streamlit/config.toml` — stone-palette light theme, no telemetry,
  minimal toolbar.
- The app imports `personalized_risk.py` from the repo root via
  `Path(__file__).resolve().parent.parent` so the deploy works without
  any path tweaks.

### Daily PubMed ingestion (optional but recommended)

The repo ships with `.github/workflows/daily_ingestion.yml` that runs
`scripts/continuous_ingestion.py` daily and commits the freshness log
back to the repo. To enable:

1. On the repo's GitHub page → **Settings** → **Actions** → **General**
   → enable Actions.
2. Under **Workflow permissions**, set "Read and write permissions"
   so the bot can commit the freshness log back.
3. The cron fires at 06:00 UTC every day. After ~24h you'll see a
   fresh entry under `freshness/log/<date>.json` and the app's Freshness
   tab will show today's run.

### Updating the live app

Streamlit Cloud auto-redeploys on every git push to the deployed branch.
Push, wait ~30s, refresh the URL.

---

## Surface 2 — Landing page (Vercel / Netlify / GitHub Pages)

**Time to live URL:** ~2 minutes.

### Option A — GitHub Pages (free, simplest)

The landing page (`ui/landing.html`) is a single self-contained HTML file
with inline CSS — no build step.

1. On the GitHub repo → **Settings** → **Pages**.
2. **Source**: Deploy from a branch.
3. **Branch**: `main`, folder: `/ (root)`.
4. Save. After ~30s the page is live at:
   ```
   https://<your-username>.github.io/causes-atlas-autism/ui/landing.html
   ```

5. Optionally redirect the repo root: copy `ui/landing.html` to
   `index.html` at the repo root, and the URL becomes:
   ```
   https://<your-username>.github.io/causes-atlas-autism/
   ```

### Option B — Vercel (custom domain, prettier URL)

```bash
npm install -g vercel
cd /Users/Greg/Autism
vercel deploy --prod
```

Vercel auto-detects the static `ui/landing.html`. To set up a custom
domain (e.g., `causesatlas.org`):
- `vercel domains add causesatlas.org`
- Configure DNS per Vercel's instructions.

### Option C — Netlify (drag-and-drop)

1. Go to https://app.netlify.com/drop.
2. Drag the `/Users/Greg/Autism/ui` folder onto the page.
3. Live in <60 seconds at a `*.netlify.app` URL.

### Linking landing → calculator

The landing page's "Begin" button is configured to open
`https://causes-atlas-autism.streamlit.app` (or whatever you set).
Edit `ui/landing.html` → search for `data-calculator-url` and replace
with your actual deployed Streamlit URL.

---

## Surface 3 (later) — Custom-domain hosted web app

When the Streamlit prototype's research-y feel becomes the bottleneck,
move to a Next.js / FastAPI hosted app at `causesatlas.org` (or similar)
with `/calculator`, `/atlas`, `/freshness`, `/contested` routes. The
engine code (`personalized_risk.py`) ports over directly — it's pure
Python with stdlib-only deps.

This is the v0.4 deliverable, not v0.3.

---

## Privacy + safety on a public URL

- The calculator runs the engine **server-side on the Streamlit Cloud
  worker**. Inputs do leave your machine (they're sent to the worker
  and processed there).
- For PHI-sensitive use, do not deploy to a public free tier; either run
  locally (recommended for any actual patient data), or move to a HIPAA-
  compliant hosting tier with a BAA.
- All four bundled calibration cases are synthetic, literature-derived
  cohort-level profiles. No real patient data ships with the repo.
- The engine produces no telemetry; the daily PubMed cron uses NCBI
  E-utilities (public, no key required for low-volume daily use).
