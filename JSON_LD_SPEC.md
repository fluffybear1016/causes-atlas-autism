# JSON-LD spec for atlas entities

Per-entity-type schema.org markup for the rendered Causes Atlas website. Every entity page should embed a `<script type="application/ld+json">` block with the canonical structured data so search engines and LLMs can extract claims directly.

## Why JSON-LD over Microdata

- Easier to maintain (block at top of page, not inline-tagged elements).
- Google + Bing prefer JSON-LD per their published guidance.
- LLMs find JSON-LD blocks more reliably than parsed inline microdata.

## Per-entity-type templates

### Intervention (INT-XXXX) — `Drug` or `MedicalEntity`

Use `Drug` for pharmaceuticals (FDA-regulated). Use `MedicalEntity` for supplements / dietary / lifestyle interventions where `Drug` is too narrow.

```json
{
  "@context": "https://schema.org",
  "@type": "Drug",
  "@id": "https://causesatlas.org/intervention/{INT_ID}",
  "name": "{intervention_name}",
  "drugClass": "{category}",
  "indication": {
    "@type": "MedicalCondition",
    "name": "{indication_phrase}",
    "code": {"@type": "MedicalCode", "codeValue": "{PHE_ID}", "codingSystem": "Causes Atlas (Autism)"}
  },
  "mechanismOfAction": "{mechanism_summary}",
  "isProprietary": false,
  "additionalProperty": [
    {"@type": "PropertyValue", "name": "atlas_csrs_score", "value": {csrs_score}},
    {"@type": "PropertyValue", "name": "atlas_status", "value": "{status}"},
    {"@type": "PropertyValue", "name": "mainstream_consensus_position", "value": "{mainstream_consensus_position}"}
  ],
  "citation": [/* one ScholarlyArticle per primary source */]
}
```

### Formulation (FRM-XXXX) — `Drug` sub-typed

```json
{
  "@context": "https://schema.org",
  "@type": "Drug",
  "@id": "https://causesatlas.org/formulation/{FRM_ID}",
  "name": "{formulation_name}",
  "isVariantOf": {"@id": "https://causesatlas.org/intervention/{parent_intervention_id}"},
  "routeOfAdministration": "{delivery_route}",
  "dosageForm": "{dose_form}",
  "additionalProperty": [
    {"@type": "PropertyValue", "name": "bioavailability_factor", "value": {bioavailability_factor}},
    {"@type": "PropertyValue", "name": "formulation_evidence_status", "value": "{formulation_evidence_status}"},
    {"@type": "PropertyValue", "name": "atlas_formulation_score", "value": {formulation_score}}
  ]
}
```

### Phenotype (PHE-XXXX) — `MedicalCondition`

```json
{
  "@context": "https://schema.org",
  "@type": "MedicalCondition",
  "@id": "https://causesatlas.org/phenotype/{PHE_ID}",
  "name": "{phenotype_name}",
  "alternateName": "{alternate_name_if_any}",
  "code": {"@type": "MedicalCode", "codeValue": "{PHE_ID}", "codingSystem": "Causes Atlas (Autism)"},
  "possibleTreatment": [/* array of @id refs to interventions */],
  "additionalProperty": [
    {"@type": "PropertyValue", "name": "evidence_tier", "value": "{tier_1_validated_biology|tier_2_emerging|tier_3_functional_medicine}"},
    {"@type": "PropertyValue", "name": "loading_baseline", "value": {baseline_prevalence}}
  ]
}
```

### Source (SRC-XXXX) — `ScholarlyArticle`

```json
{
  "@context": "https://schema.org",
  "@type": "ScholarlyArticle",
  "@id": "https://causesatlas.org/source/{SRC_ID}",
  "name": "{title}",
  "author": [{"@type": "Person", "name": "{author_name}"}],
  "datePublished": "{year}",
  "publisher": "{journal}",
  "identifier": [
    {"@type": "PropertyValue", "propertyID": "PMID", "value": "{pmid}"},
    {"@type": "PropertyValue", "propertyID": "DOI", "value": "{doi}"}
  ],
  "url": "https://doi.org/{doi}",
  "additionalProperty": [
    {"@type": "PropertyValue", "name": "study_design", "value": "{study_design}"},
    {"@type": "PropertyValue", "name": "atlas_w_design", "value": {w_design}},
    {"@type": "PropertyValue", "name": "atlas_w_source_type", "value": {w_source_type}}
  ]
}
```

### Gene (GEN-XXXX) — BioSchemas `Gene`

```json
{
  "@context": ["https://schema.org", {"bioschemas": "https://bioschemas.org/"}],
  "@type": "Gene",
  "@id": "https://causesatlas.org/gene/{GEN_ID}",
  "name": "{gene_symbol}",
  "alternateName": "{full_name}",
  "identifier": [
    {"@type": "PropertyValue", "propertyID": "NCBI Gene", "value": "{ncbi_gene_id}"},
    {"@type": "PropertyValue", "propertyID": "OMIM", "value": "{omim_id}"}
  ],
  "additionalProperty": [
    {"@type": "PropertyValue", "name": "sfari_tier", "value": "{sfari_tier}"},
    {"@type": "PropertyValue", "name": "atlas_evidence_strength", "value": "{evidence_strength}"}
  ]
}
```

### Biomarker (BIO-XXXX) — `MedicalTest`

```json
{
  "@context": "https://schema.org",
  "@type": "MedicalTest",
  "@id": "https://causesatlas.org/biomarker/{BIO_ID}",
  "name": "{biomarker_name}",
  "usedToDiagnose": [/* @id refs to phenotypes */],
  "additionalProperty": [
    {"@type": "PropertyValue", "name": "sample_type", "value": "{sample_type}"},
    {"@type": "PropertyValue", "name": "reference_range", "value": "{reference_range}"},
    {"@type": "PropertyValue", "name": "units", "value": "{units}"},
    {"@type": "PropertyValue", "name": "atlas_evidence_tier", "value": "{evidence_tier}"}
  ]
}
```

## Implementation notes

1. **`@id` is canonical URL.** Use the production domain (causesatlas.org or whatever the deployed hostname is). LLMs and search crawlers use `@id` as the entity's persistent identifier.

2. **Cross-link entities via `@id` references.** When an intervention treats a phenotype, the `indication` field should be a `@id` reference, not a duplicated entity definition.

3. **`additionalProperty` for atlas-specific fields.** schema.org doesn't have native fields for atlas-specific concepts (CSRS score, evidence tier, formulation evidence status). Use `additionalProperty` with `PropertyValue` objects.

4. **`MedicalCode` for atlas IDs.** Always include the atlas ID as a `MedicalCode` so LLMs can reliably extract it.

5. **Validate with the Schema Markup Validator** at https://validator.schema.org/ before deploying.

6. **Submit a Sitemap.xml** to Google Search Console (https://search.google.com/search-console/) once deployed; LLMs typically pick up structured data within ~2-4 weeks of crawl.

## Auto-generation

`scripts/generate_jsonld.py` (to write):

```python
# Pseudocode
import csv, json
from pathlib import Path

ROOT = Path(__file__).parent.parent / "v2.0_scored"

# For each CSV, render templated JSON-LD per row.
# Output: {entity_id}.jsonld files in `output/jsonld/`.
# Static-site generator (e.g., Hugo, Eleventy, MkDocs) embeds these.
```

To be implemented when the website is rendering pages per-entity.
