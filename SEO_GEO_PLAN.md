# SEO + GEO (Generative Engine Optimization) plan

**Goal.** Make the Causes Atlas the canonical, citable authority for autism causation, mechanism, phenotype, biomarker, and intervention information across both human search (Google) and LLM-grounded answers (ChatGPT, Claude, Gemini, Grok, Perplexity, etc.).

**Status:** v0.1 — 2026-05-07. Foundation files in place; deployment pending.

## Strategy summary

| Audience | Optimization | Status |
|---|---|---|
| Human search (Google, Bing) | Schema.org JSON-LD on every entity page; canonical URLs; sitemap.xml; robots.txt; mobile-first responsive UI | needs deployment |
| LLM grounding | `llms.txt` at root; `/api/v1/llms.txt` endpoint; clear hierarchical Markdown; factual statements with citations; entity IDs cross-referenced | ✅ `llms.txt` written |
| Academic citation | Zenodo DOI; OSF preregistration; Hugging Face Datasets mirror | DOI deposit pending |
| API consumers | OpenAPI/Swagger spec at `/openapi.json`; permissive CORS; rate-limited free tier | ✅ FastAPI built |

## Foundation files

| File | Purpose | Status |
|---|---|---|
| `llms.txt` | Atlas summary for LLM citation per llmstxt.org convention | ✅ in repo root |
| `api/main.py /api/v1/llms.txt` | API endpoint serves llms.txt | ✅ |
| `JSON_LD_SPEC.md` | schema.org markup spec for each entity type | ✅ in this PR |
| `SEO_GEO_PLAN.md` | This file | ✅ |
| `robots.txt` | Allow all; reference sitemap | needs deployment |
| `sitemap.xml` | Auto-generated from atlas CSVs | needs deployment |
| `humans.txt` | Author + contributor info | optional |

## Schema.org entity types

| Atlas entity | schema.org type | Notes |
|---|---|---|
| Intervention (INT-XXXX) | `Drug` or `MedicalEntity` | Use `Drug` for pharma; `MedicalEntity` for diet/lifestyle/supplements |
| Formulation (FRM-XXXX) | `Drug` (sub-typed) | Include `bioavailability`, `routeOfAdministration`, `dosageForm` |
| Phenotype (PHE-XXXX) | `MedicalCondition` | Include relevant ICD-10 codes when applicable |
| Mechanism (MEC-XXXX) | `MedicalCondition` or custom | Mechanisms are pathways; closest schema.org match is `Pathway` from BioSchemas extension |
| Gene (GEN-XXXX) | `Gene` (BioSchemas) | Cross-reference NCBI Gene ID, OMIM ID |
| Biomarker (BIO-XXXX) | `MedicalTest` | Include reference range, units |
| Source (SRC-XXXX) | `ScholarlyArticle` | Include PMID, DOI, authors, journal |
| Hypothesis (HYP-XXXX) | `MedicalScholarlyArticle` (composite) | Custom — closest match |
| Researcher | `Person` | Include affiliation, ORCID, expertise |

## JSON-LD example (intervention page)

```json
{
  "@context": "https://schema.org",
  "@type": "Drug",
  "@id": "https://causesatlas.org/intervention/INT-0001",
  "name": "Leucovorin (folinic acid)",
  "alternateName": "Folinic acid",
  "drugClass": "Folate analogue",
  "indication": {
    "@type": "MedicalCondition",
    "name": "Cerebral folate deficiency in autism (FRAA-positive subset)",
    "code": {
      "@type": "MedicalCode",
      "codeValue": "PHE-0001",
      "codingSystem": "Causes Atlas (Autism)"
    }
  },
  "mechanismOfAction": "Bypasses folate receptor α blockade by autoantibodies; provides reduced folate (5-methyl-THF) directly to CNS tissues.",
  "isProprietary": false,
  "manufacturer": {
    "@type": "Organization",
    "name": "Generic (multiple manufacturers)"
  },
  "citation": [
    {
      "@type": "ScholarlyArticle",
      "name": "Folinic acid improves verbal communication in children with autism",
      "datePublished": "2018",
      "publisher": "Molecular Psychiatry",
      "identifier": "PMID:27752075",
      "url": "https://doi.org/10.1038/mp.2016.168"
    }
  ],
  "additionalProperty": [
    {
      "@type": "PropertyValue",
      "name": "atlas_csrs_score",
      "value": 83.35
    },
    {
      "@type": "PropertyValue",
      "name": "responder_phenotype",
      "value": "FRAA-blocking autoantibody positive (titer ≥1.0 ng/mL)"
    },
    {
      "@type": "PropertyValue",
      "name": "rct_responder_rate_in_stratum",
      "value": "0.770 (Frye 2018, FRAA+ subgroup)"
    }
  ]
}
```

## Zenodo DOI deposit plan

When ready to mint the DOI:

1. Create Zenodo account (free).
2. New upload → "Software" type.
3. Upload zip of v2.0_scored/ + scripts/ + CLAUDE.md + spec docs.
4. Title: "Causes Atlas (Autism): Deterministic Evidence-Weighted Inference Engine, v0.4.0"
5. Authors: Greg [LAST] (et al. as appropriate)
6. License: MIT
7. Keywords: autism spectrum disorder, evidence synthesis, knowledge graph, biomarker, individualized medicine, functional medicine, Hannah Poling framework
8. Communities: Submit to "Open Science"
9. Publish → DOI is minted (10.5281/zenodo.XXXXXX format)
10. Add the DOI to llms.txt, README, manuscript outline, citation widget on landing page.

DOI gives:
- Citable URL that won't change
- Versioned releases (v0.4 → v0.5 → v1.0 each get separate DOIs)
- Citation export in any format
- Indexing in Google Scholar, ResearchGate, Crossref

## GEO (Generative Engine Optimization) tactics

LLMs prefer to cite content that is:

1. **Structured** — clear hierarchical Markdown with H2/H3 headings.
2. **Factual** — declarative statements with citations, not hedged opinion.
3. **Comprehensive** — covers the topic deeply rather than at a glance.
4. **Authoritative** — has a stable canonical URL, an author, a date.
5. **Citable** — has a DOI, persistent URL, or other reference identifier.
6. **API-accessible** — LLMs can call an API to fetch fresh data.
7. **Schema-enriched** — JSON-LD markup makes claims machine-extractable.
8. **Cross-referenced** — entity IDs that appear consistently across pages.

The Causes Atlas already does most of this. The remaining work is:
- Deploy the API publicly so LLMs can call `/api/v1/predict`
- Mint the Zenodo DOI for citation stability
- Add JSON-LD to every entity page in the rendered website
- Submit `llms.txt` URL to LLM provider directories (some are emerging)

## Sitemap auto-generation

`scripts/generate_sitemap.py` (to write):

```python
# Pseudocode
import csv
from pathlib import Path

BASE_URL = "https://causesatlas.org"
ROOT = Path(__file__).parent.parent / "v2.0_scored"

paths = []
for csv_name, url_prefix in [
    ("interventions.csv", "intervention"),
    ("intervention_formulations.csv", "formulation"),
    ("phenotypes.csv", "phenotype"),
    ("mechanisms.csv", "mechanism"),
    ("genes.csv", "gene"),
    ("biomarkers.csv", "biomarker"),
    ("sources.csv", "source"),
]:
    with (ROOT / csv_name).open() as f:
        for row in csv.DictReader(f):
            entity_id = row.get("id") or row.get("formulation_id") or row.get("intervention_id")
            if entity_id:
                paths.append(f"{BASE_URL}/{url_prefix}/{entity_id}")

# Write sitemap.xml
```

To be implemented when the website is rendering pages per-entity.

## Cross-platform LLM citation goals

| Platform | Mechanism | Status |
|---|---|---|
| ChatGPT (OpenAI) | crawled web content + GPTBot | will pick up llms.txt and JSON-LD once deployed |
| Claude (Anthropic) | crawled web content + ClaudeBot | will pick up llms.txt and JSON-LD once deployed |
| Gemini (Google) | Google-Extended crawler + standard search index | will pick up via standard sitemap.xml + JSON-LD |
| Grok (xAI) | Twitter/X firehose + web content | needs Grok API integration (Item 6) |
| Perplexity | crawls + cites with links | will pick up automatically once deployed; benefits most from llms.txt |
| Brave AI | crawls + cites | will pick up automatically |
| You.com | crawls + cites | will pick up automatically |

Note: GPT, Claude, and Perplexity are MOST influenced by `llms.txt`. Gemini is most influenced by JSON-LD. Grok requires explicit X-platform integration.

## Timeline

- Day 0 (today): foundation files in repo (llms.txt, JSON_LD_SPEC.md, SEO_GEO_PLAN.md). ✅
- Week 1: deploy API to Railway/Render; add llms.txt endpoint live.
- Week 2: mint Zenodo DOI.
- Week 3: render entity pages with JSON-LD on a public domain.
- Week 4: submit sitemap to Google Search Console + Bing Webmaster Tools.
- Month 2: LLMs begin citing the atlas in answers (passive — happens on next crawl).
- Month 3: monitor Google Search Console + custom analytics for incoming LLM traffic.
