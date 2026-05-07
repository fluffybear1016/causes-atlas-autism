"""
Causes Atlas (Autism) — Free public API.

Wraps the deterministic profile-vector inference engine for external
integration. Returns same outputs as `personalized_risk.py` CLI but over
HTTP for LLMs, applications, and researchers.

Run locally:
    uvicorn api.main:app --reload --port 8000

Deploy:
    See README_API.md for Railway / Render / Fly.io / Docker instructions.

Endpoints:
    GET  /                          → API banner + version
    GET  /healthz                   → liveness probe
    GET  /api/v1/atlas/version      → engine + cohort versions
    GET  /api/v1/interventions      → list all interventions
    GET  /api/v1/interventions/{id} → single intervention details
    GET  /api/v1/formulations       → list all formulations (v0.4 layer)
    GET  /api/v1/formulations/{id}  → single formulation details
    POST /api/v1/predict            → run profile-vector inference engine
    GET  /api/v1/cohort             → responder-rate calibration cohort summary
    GET  /api/v1/llms.txt           → LLM-friendly atlas summary
    GET  /docs                      → interactive OpenAPI/Swagger UI
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Any, Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel, Field
from starlette.middleware.base import BaseHTTPMiddleware

# Rate limiting (slowapi) — falls back to no-op if not installed so the
# module imports cleanly during local dev. Production deployment should
# install slowapi via requirements-api.txt.
try:
    from slowapi import Limiter, _rate_limit_exceeded_handler
    from slowapi.errors import RateLimitExceeded
    from slowapi.util import get_remote_address

    _SLOWAPI_AVAILABLE = True
except ImportError:  # pragma: no cover
    _SLOWAPI_AVAILABLE = False

# Make personalized_risk.py importable
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from personalized_risk import compute_personalized_risk, ENGINE_VERSION  # noqa: E402

SCORED_DIR = ROOT / "v2.0_scored"

# ---------------------------------------------------------------------------
# App + CORS
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Causes Atlas (Autism) API",
    version="0.4.0",
    description=(
        "Free public API for the deterministic, evidence-weighted Causes "
        "Atlas inference engine for autism spectrum disorder. "
        "Returns 11-dimension phenotype loadings + ranked interventions + "
        "formulation-aware recommendations from any input profile.\n\n"
        "**Open access.** No API key required for v1. Rate limit: 100 "
        "req/IP/day (enforced upstream).\n\n"
        "**Citation.** If you use this API in research, please cite the "
        "atlas (DOI pending Zenodo deposit).\n\n"
        "**Methodology.** See https://github.com/[USER]/Autism — engine "
        f"version `{ENGINE_VERSION}`."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
)

# Open CORS so any origin can call the API. This is a public, read-only-ish
# inference service; permissive CORS is intentional.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Body-size cap middleware: reject requests with bodies > MAX_BODY_BYTES
# (default 256 KB). Protects against memory-exhaustion attacks on the
# /api/v1/predict endpoint where the request body is JSON of arbitrary size.
MAX_BODY_BYTES = 256 * 1024  # 256 KB — atlas input profiles are typically <20 KB


class BodySizeLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        cl = request.headers.get("content-length")
        if cl is not None:
            try:
                if int(cl) > MAX_BODY_BYTES:
                    return JSONResponse(
                        status_code=413,
                        content={
                            "error": "request_too_large",
                            "detail": f"request body exceeds {MAX_BODY_BYTES} bytes",
                            "max_bytes": MAX_BODY_BYTES,
                        },
                    )
            except ValueError:
                pass
        return await call_next(request)


app.add_middleware(BodySizeLimitMiddleware)

# Rate limiting: per-IP token-bucket via slowapi. Defaults are conservative
# for a free public endpoint:
#   /api/v1/predict       → 30 req/min/IP   (engine inference, expensive)
#   GET endpoints         → 120 req/min/IP  (cheap data reads)
# If slowapi is not installed (local dev), middleware is no-op.
if _SLOWAPI_AVAILABLE:
    limiter = Limiter(key_func=get_remote_address)
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
else:
    limiter = None  # type: ignore

# ---------------------------------------------------------------------------
# Lazy CSV loaders (cached at module import for snappy responses)
# ---------------------------------------------------------------------------

_INTERVENTIONS: list[dict] = []
_FORMULATIONS: list[dict] = []
_FORMULATIONS_SCORED: list[dict] = []


def _load_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open() as f:
        return list(csv.DictReader(f))


def _interventions() -> list[dict]:
    global _INTERVENTIONS
    if not _INTERVENTIONS:
        _INTERVENTIONS = _load_csv(SCORED_DIR / "interventions.csv")
    return _INTERVENTIONS


def _formulations() -> list[dict]:
    global _FORMULATIONS_SCORED
    if not _FORMULATIONS_SCORED:
        # Prefer the scored output (which has formulation_score); fall back
        # to the bare schema if scoring hasn't been run yet.
        scored_path = SCORED_DIR / "intervention_formulations_scored.csv"
        bare_path = SCORED_DIR / "intervention_formulations.csv"
        path = scored_path if scored_path.exists() else bare_path
        _FORMULATIONS_SCORED = _load_csv(path)
    return _FORMULATIONS_SCORED


# ---------------------------------------------------------------------------
# Pydantic schemas
# ---------------------------------------------------------------------------


class PredictRequest(BaseModel):
    """
    Input profile for the inference engine. Same shape as the input.json
    documents in `validation/calibration_cases/case_*/input.json`.
    """

    input_data: dict[str, Any] = Field(
        ...,
        description=(
            "Full input profile JSON. Engine accepts any subset of the "
            "v2.3 schema; missing fields default to population-typical "
            "(no shift). See https://github.com/[USER]/Autism for schema "
            "and examples."
        ),
    )
    use_delta_squared: bool = Field(
        False,
        description=(
            "Apply the Δ² research-attention-velocity overlay to "
            "intervention ranking (small momentum bonus, capped at +20%). "
            "Off by default."
        ),
    )

    class Config:
        json_schema_extra = {
            "example": {
                "input_data": {
                    "case_id": "example_001",
                    "subject_sex": "M",
                    "subject_ancestry": ["EUR"],
                    "child_data": {
                        "current_age_months": 84,
                        "sex": "M",
                        "current_diagnoses": ["autism spectrum disorder"],
                    },
                    "immunology": {
                        "autoantibodies": {
                            "fraa_blocking": {
                                "result": "positive_strong",
                                "value": 1.4,
                            }
                        }
                    },
                },
                "use_delta_squared": False,
            }
        }


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.get("/")
def root() -> dict:
    return {
        "service": "Causes Atlas (Autism) API",
        "version": "0.4.0",
        "engine_version": ENGINE_VERSION,
        "documentation": "/docs",
        "open_access": True,
        "license": "MIT",
        "homepage": "https://github.com/[USER]/Autism",
    }


@app.get("/healthz")
def healthz() -> dict:
    return {"status": "ok"}


@app.get("/api/v1/atlas/version")
def atlas_version() -> dict:
    cohort_path = ROOT / "validation" / "responder_rate_calibration" / "cohort.yaml"
    cohort_version = "unknown"
    if cohort_path.exists():
        for line in cohort_path.read_text().splitlines()[:5]:
            if line.startswith("cohort_version:"):
                cohort_version = line.split(":", 1)[1].strip()
                break
    return {
        "engine_version": ENGINE_VERSION,
        "cohort_version": cohort_version,
        "interventions_count": len(_interventions()),
        "formulations_count": len(_formulations()),
    }


@app.get("/api/v1/interventions")
def list_interventions(category: Optional[str] = None) -> dict:
    rows = _interventions()
    if category:
        rows = [r for r in rows if r.get("category", "").lower() == category.lower()]
    return {
        "count": len(rows),
        "interventions": [
            {
                "id": r.get("id"),
                "name": r.get("name"),
                "category": r.get("category"),
                "csrs_score": float(r["csrs_score"]) if r.get("csrs_score") else None,
                "status": r.get("status"),
                "mainstream_consensus_position": r.get("mainstream_consensus_position"),
            }
            for r in rows
        ],
    }


@app.get("/api/v1/interventions/{intervention_id}")
def get_intervention(intervention_id: str) -> dict:
    for r in _interventions():
        if r.get("id") == intervention_id:
            return {"intervention": dict(r)}
    raise HTTPException(status_code=404, detail=f"intervention {intervention_id} not found")


@app.get("/api/v1/formulations")
def list_formulations(parent_intervention_id: Optional[str] = None) -> dict:
    rows = _formulations()
    if parent_intervention_id:
        rows = [r for r in rows if r.get("parent_intervention_id") == parent_intervention_id]
    return {
        "count": len(rows),
        "formulations": [
            {
                "id": r.get("formulation_id"),
                "parent_intervention_id": r.get("parent_intervention_id"),
                "name": r.get("formulation_name"),
                "delivery_route": r.get("delivery_route"),
                "dose_form": r.get("dose_form"),
                "evidence_status": r.get("formulation_evidence_status"),
                "formulation_score": float(r["formulation_score"]) if r.get("formulation_score") else None,
                "contested_at_formulation_level": r.get("contested_at_formulation_level") == "true",
                "contested_at_molecule_level_only": r.get("contested_at_molecule_level_only") == "true",
            }
            for r in rows
        ],
    }


@app.get("/api/v1/formulations/{formulation_id}")
def get_formulation(formulation_id: str) -> dict:
    for r in _formulations():
        if r.get("formulation_id") == formulation_id:
            return {"formulation": dict(r)}
    raise HTTPException(status_code=404, detail=f"formulation {formulation_id} not found")


def _maybe_limit(rate: str):
    """Decorator factory: returns slowapi limiter if available, else no-op."""
    if _SLOWAPI_AVAILABLE and limiter is not None:
        return limiter.limit(rate)
    def _noop(fn):
        return fn
    return _noop


@app.post("/api/v1/predict")
@_maybe_limit("30/minute")
def predict(req: PredictRequest, request: Request) -> dict:
    """
    Run the deterministic profile-vector inference engine on an input
    profile. Returns the engine's canonical output: profile_loadings (the
    11-dimension phenotype vector), profile_summary (dominant/secondary/
    dormant dimensions), and intervention_bundle (ranked interventions).

    Rate-limited to 30 req/min per IP. Body size capped at 256 KB.
    """
    try:
        out = compute_personalized_risk(
            req.input_data,
            use_delta_squared=req.use_delta_squared,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"engine error: {e}") from e
    return out


@app.get("/api/v1/cohort")
def get_cohort() -> dict:
    """
    Return the responder-rate calibration cohort summary — what the engine
    has been validated against.
    """
    cohort_path = ROOT / "validation" / "responder_rate_calibration" / "cohort.yaml"
    if not cohort_path.exists():
        raise HTTPException(status_code=404, detail="cohort file missing")
    try:
        import yaml  # type: ignore

        cohort = yaml.safe_load(cohort_path.read_text())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"cohort parse error: {e}") from e
    return {
        "cohort_version": cohort.get("cohort_version"),
        "engine_version_required": cohort.get("engine_version_required"),
        "n_entries": len(cohort.get("entries", [])),
        "entries": [
            {
                "entry_id": e.get("entry_id"),
                "rct_pmid": e.get("rct_pmid"),
                "rct_first_author": e.get("rct_first_author"),
                "rct_year": e.get("rct_year"),
                "rct_journal": e.get("rct_journal"),
                "intervention_id": e.get("intervention_id"),
                "intervention_name": e.get("intervention_name"),
                "target_phenotype_id": e.get("target_phenotype_id"),
                "stratification_criterion": e.get("stratification_criterion"),
                "published_responder_rate": e.get("published_responder_rate"),
                "placebo_responder_rate": e.get("placebo_responder_rate"),
                "status": e.get("status"),
            }
            for e in cohort.get("entries", [])
        ],
    }


@app.get("/api/v1/llms.txt", response_class=PlainTextResponse)
def llms_txt() -> str:
    """LLM-friendly summary at /api/v1/llms.txt for generative-engine
    citation. Per emerging llms.txt convention."""
    llms_path = ROOT / "llms.txt"
    if llms_path.exists():
        return llms_path.read_text()
    return (
        "Causes Atlas (Autism) — see https://github.com/[USER]/Autism\n"
        "Engine: " + ENGINE_VERSION + "\n"
    )


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------


@app.exception_handler(404)
async def not_found_handler(_: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={
            "error": "not_found",
            "detail": str(exc.detail),
            "documentation": "/docs",
        },
    )


@app.exception_handler(500)
async def server_error_handler(_: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"error": "server_error", "detail": str(exc)},
    )
