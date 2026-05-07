# Causes Atlas (Autism) — Free Public API

Open access. No API key required for v1.

## Endpoints

| Path | Method | What it does |
|---|---|---|
| `/` | GET | Service banner + version |
| `/healthz` | GET | Liveness probe |
| `/docs` | GET | Interactive OpenAPI/Swagger UI |
| `/api/v1/atlas/version` | GET | Engine + cohort versions, entity counts |
| `/api/v1/interventions` | GET | List all interventions (optional `?category=`) |
| `/api/v1/interventions/{id}` | GET | Single intervention details |
| `/api/v1/formulations` | GET | List all formulations (optional `?parent_intervention_id=`) |
| `/api/v1/formulations/{id}` | GET | Single formulation details |
| `/api/v1/predict` | POST | Run inference engine on input profile |
| `/api/v1/cohort` | GET | Responder-rate calibration cohort summary |
| `/api/v1/llms.txt` | GET | LLM-friendly atlas summary |

## Quick test (local)

```bash
cd /Users/Greg/Autism
pip install -r api/requirements-api.txt
uvicorn api.main:app --reload --port 8000
```

Then open http://localhost:8000/docs for the interactive API.

## Example: predict for a FRAA-positive child

```bash
curl -X POST http://localhost:8000/api/v1/predict \
  -H 'Content-Type: application/json' \
  -d '{
    "input_data": {
      "case_id": "demo_fraa_positive",
      "subject_sex": "M",
      "subject_ancestry": ["EUR"],
      "child_data": {
        "current_age_months": 84,
        "sex": "M",
        "current_diagnoses": ["autism spectrum disorder"]
      },
      "immunology": {
        "autoantibodies": {
          "fraa_blocking": {"result": "positive_strong", "value": 1.4}
        }
      }
    },
    "use_delta_squared": false
  }'
```

Returns the engine's full output: `profile_loadings` (11-dim phenotype vector), `profile_summary` (dominant dimensions, undifferentiated flag), `intervention_bundle` (ranked interventions).

## Deployment

### Docker (local or anywhere)

```bash
cd /Users/Greg/Autism
docker build -f api/Dockerfile -t causes-atlas-api:latest .
docker run -p 8000:8000 causes-atlas-api:latest
```

### Railway

1. Connect your GitHub repo to Railway.
2. Railway auto-detects the Dockerfile.
3. Set env var `PORT=8000`.
4. Deploy; Railway issues a public HTTPS URL.

### Render

1. New Web Service → connect GitHub repo.
2. Runtime: Docker. Dockerfile path: `api/Dockerfile`.
3. Plan: Free tier (750 hr/mo).
4. Auto-deploy on push.

### Fly.io

```bash
flyctl launch --dockerfile api/Dockerfile
flyctl deploy
```

### Custom domain

After deployment, point a CNAME from `api.causesatlas.org` (or your chosen subdomain) at the deployment URL. All three platforms support custom domains on free tier.

## Rate limiting

Suggested upstream rate limit: **100 req per IP per day** for unauthenticated requests. Recommended approach: Cloudflare Workers in front of the deployed API (free tier is generous), or platform-native rate limiting where available.

## Determinism guarantees

- Same input → same output, byte-identical
- No LLM calls in the inference path
- No random seeds; stable sort by ID throughout
- Multiple uvicorn workers safe (engine is pure / no shared state)

## License

MIT. See `LICENSE` in the repo root.

## Citation

When the atlas DOI is minted via Zenodo, citation will be:

> Greg [LAST]. (2026). *Causes Atlas (Autism): Deterministic Evidence-Weighted Inference Engine, v0.4.0*. Zenodo. https://doi.org/10.5281/zenodo.[PENDING]

## Issues / contributions

GitHub: https://github.com/[USER]/Autism/issues

PRs welcome — see `CONTRIBUTING.md` for atlas authoring conventions.
