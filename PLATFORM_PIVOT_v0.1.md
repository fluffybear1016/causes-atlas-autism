# Platform Pivot v0.1 — from autism atlas to multi-condition functional-medicine knowledge graph

**Date:** 2026-05-05
**Status:** committed, executing
**Author:** post-mortem-driven strategic pivot

## What this is

The Causes Atlas (Autism) is the first instance of a domain-general
**functional-medicine knowledge graph platform**. Going forward, the project
is a multi-atlas system — one atlas per condition — sharing a single engine,
verification protocol, continuous-ingestion pipeline, evidence-balance
schema, and freshness-log infrastructure.

**Aspiration:** the canonical evidence-graph layer for functional medicine.
The clinician-facing tagline is *"Google for functional medicine"* — a
single, trusted knowledge surface across every condition where the
mainstream's population-average answer doesn't fit the individual.

**Architecture metaphor:** the substrate is shaped like **GitHub + OncoKB**,
not Google. Versioned, forkable, openly auditable, citation-grounded,
contributable by the community. Search is one access pattern; the deeper
value is canonical, verified, condition-stratified evidence integration
that no competing tool currently provides for functional medicine.

## Why now

The autism atlas just survived a documented post-mortem fix cycle. The
engineering substrate is in place: deterministic engine, profile-vector
output, evidence-balance schema, mainstream-consensus rendering,
continuous PubMed ingestion with verify-before-write, and a UI that
publishes its work. The lethal failure mode (classification semantics)
is gone. The marginal cost of adding a second condition is now
*architecture* — not science — and architecture is a one-time investment
that compounds across every future condition.

The window: functional-medicine clinical practice is growing ~20% YoY,
~500 high-volume MAPS / ARI / Walsh / IFM-trained practitioners in the
US, plus thousands of adjacent integrative-medicine clinicians, and
*nobody* offers them a canonical, verified, multi-condition knowledge
graph. The closest competitors (LiveWello, Nutrahacker, Genova, Rupa
Health, IFM protocol library, Bredesen's ReCODE platform) are either
single-purpose (one variant, one panel, one protocol), unverified
(citation-less protocols), or not knowledge-graph-shaped at all
(course platforms, lab-ordering services).

## What changes

| Concern | Autism-only (today) | Multi-atlas (going forward) |
|---|---|---|
| Atlas storage | `v2.0_scored/` | `atlases/<condition>/<version>/` per condition |
| Engine | Hardcoded ATLAS_ROOT | `--atlas-path` CLI + function arg |
| Phenotype taxonomy | 11 autism-specific | Per-condition; declared in atlas manifest |
| Biomarker registry | Autism-specific | Shared across atlases (mito, immune, methylation, etc. are universal) |
| Verify-before-write | ✓ | ✓ (unchanged — condition-agnostic) |
| Continuous ingestion | autism queries | Per-atlas query patterns; shared pipeline |
| Evidence balance | iatrogenic_exposure_priors.csv | Every prior table in every atlas |
| Mainstream consensus rendering | iatrogenic table | Every contested entity in every atlas |
| Calibration anchor | INT-0001 leucovorin = 83.35 | Per-atlas anchor declared in manifest |
| UI | autism-specific Streamlit | Atlas-selector + condition-aware rendering |

## What stays the same

- Determinism (no LLMs in scoring math, canonical_digest sha256)
- Verify-before-write protocol — universal across all atlases
- Walley IDM credal aggregation
- Profile-vector semantics (replaces classification) — universal
- max-based intervention scoring (CSRS × max(loading × edge_weight))
- Evidence balance schema (primary_pmids + countervailing_evidence_pmids)
- Mainstream consensus position field
- Continuous ingestion + freshness page (one per atlas + a federated index)

## Condition prioritization framework

Each candidate condition scored on:

1. **FM-clinician relevance.** Are MAPS/IFM/Walsh/Bredesen/Frye/Rossignol-tier practitioners already triaging this by biomarker patterns? Higher = better.
2. **Mainstream whitespace.** Does mainstream medicine have a population-average answer that obviously doesn't fit individuals? Higher = more value-add for FM.
3. **Stratifiability.** Is the condition genuinely heterogeneous along measurable biomarker dimensions? Higher = better engine fit.
4. **Mechanistic overlap with existing atlas.** Does it reuse mito / immune / methylation / microbiome dimensions already in autism atlas? Higher = lower architecture cost.
5. **Political radioactivity.** Vaccine/Lyme-tier framing risk? Lower = better launch.
6. **Patient population motivation.** Will affected patients actively use the tool / push their clinicians to use it? Higher = better adoption flywheel.
7. **Available literature.** N papers/year + N stratified RCTs? Higher = better calibration cohort feasibility.

| Condition | FM-rel | Whitespace | Stratifiable | Overlap | Radio (lower=better) | Patient-motiv | Literature | Total |
|---|---|---|---|---|---|---|---|---|
| Autism | 5 | 5 | 5 | — | 4 | 5 | 5 | (already done) |
| **Long COVID / ME-CFS** | **5** | **5** | **5** | **5** | **4** | **5** | **5** | **34** |
| PCOS | 5 | 4 | 5 | 3 | 5 | 5 | 4 | 31 |
| Hashimoto's / autoimmune thyroid | 5 | 4 | 5 | 4 | 5 | 4 | 4 | 31 |
| Alzheimer's / cognitive decline | 5 | 5 | 5 | 4 | 3 | 4 | 5 | 31 |
| MCAS | 5 | 4 | 4 | 5 | 4 | 4 | 3 | 29 |
| SIBO / IBS | 4 | 3 | 4 | 4 | 5 | 4 | 4 | 28 |
| Chronic Lyme | 5 | 5 | 4 | 4 | 1 (RADIOACTIVE) | 5 | 3 | 27 |
| Depression / anxiety FM workup | 4 | 3 | 4 | 4 | 4 | 4 | 4 | 27 |
| Cardiometabolic / lipid subfractionation | 3 | 3 | 5 | 2 | 5 | 3 | 5 | 26 |

(Each cell scored 1–5; higher = more favorable.)

**Decision: condition #2 = Long COVID / ME-CFS.** Highest total score, highest mechanistic overlap with autism (mito + immune + autonomic + MCAS + microbiome reuse 5 of the existing dimensions), largest unmet clinical need post-2020, exploding literature, mainstream has zero accepted protocol.

Conditions #3–#5 to seed in months 4–6: PCOS, Hashimoto's, Alzheimer's. PCOS is the easiest political win; Hashimoto's is the highest-volume FM workup; Alzheimer's is the highest-leverage research-tier credentialing event (Bredesen's ReCODE protocol is famous, our atlas would be the open verifiable counterpart).

## Long COVID atlas v0.1 — phenotype taxonomy

Provisional. Each phenotype must be defended by ≥3 PMID-verified primary
sources before the atlas ships v1.0. Mechanistic overlap with autism noted.

| ID | Name | Mechanism summary | Reuses autism dim |
|---|---|---|---|
| LC-PHE-0001 | Mitochondrial dysfunction post-viral | OXPHOS deficit, lactate elevation, exercise intolerance / PEM | autism PHE-0002 |
| LC-PHE-0002 | Autonomic dysfunction (POTS / dysautonomia) | Sympathetic overdrive, vagal tone deficit, orthostatic intolerance | NEW |
| LC-PHE-0003 | Mast cell activation (LC-MCAS) | Tryptase, methylhistamine elevation, histamine intolerance | autism PHE-0003 + MCAS hypothesis |
| LC-PHE-0004 | Neuroinflammation / brain fog | TNFα, IL-6, neopterin, BBB disruption proxies | autism PHE-0003 |
| LC-PHE-0005 | Microbiome dysbiosis post-viral | Akkermansia loss, Faecalibacterium loss, dysbiosis index | autism PHE-0004 |
| LC-PHE-0006 | Microvascular / coagulopathy / amyloid microclots | Fibrinaloid microclots (Pretorius), elevated d-dimer, vWF | NEW |
| LC-PHE-0007 | Post-viral autoimmune | New-onset autoantibodies, GPCR autoabs, ANA conversion | partial overlap autism PHE-0003 |
| LC-PHE-0008 | Persistent SARS-CoV-2 reservoir | Spike protein in tissue/blood, viral RNA persistence | NEW |
| LC-PHE-0009 | HPA-axis / hormonal dysregulation | Low cortisol, low DHEA, thyroid conversion deficit | NEW |

Calibration anchor candidate: **low-dose naltrexone (LDN)** in the
neuroinflammation + autoimmune subset; published responder rates from
multiple cohort studies. Final selection deferred until v0.2 atlas
seeding completes.

## Sequencing for next 6 months — multi-atlas pivot

| Month | Engineering deliverable | Content deliverable |
|---|---|---|
| 1 (current) | Engine generalized to `--atlas-path`; atlas manifest schema; autism atlas migrated under `atlases/autism/`; UI atlas-selector | Long COVID atlas v0.1 seed (manifest + phenotype taxonomy + 5+ verified PMIDs) |
| 2 | Cross-atlas biomarker registry (shared mito / immune / methylation panels); cross-atlas profile aggregation (a patient with autism + Long COVID gets combined loadings) | Long COVID atlas to ~50 sources; PCOS atlas seed |
| 3 | Atlas contribution model (PR-shaped — anyone can submit a verified PMID via GitHub PR; CI runs verify-before-write) | Long COVID + PCOS to ~200 sources each; Long COVID responder-rate calibration cohort to 10 entries |
| 4 | Hosted web app (Vercel/Render); atlas index page; per-condition `/atlas/<condition>` routes; clinician account model | Hashimoto's atlas seed |
| 5 | Multi-atlas validation paper draft (preprint to Patterns / npj Digital Medicine); CPIC-style structured data export for clinical decision support integrations | Alzheimer's atlas seed (Bredesen-protocol-aware) |
| 6 | API for FM lab partners (Genova, Doctor's Data, Vibrant) to push results directly into engine inputs; first 50 FM clinicians actively using the tool | Cohort of ~30 stratified RCTs across all atlases for the validation paper |

## Business model thesis

The atlas itself is **open source, forkable, free** — that's the only way
to win the canonical-knowledge-layer position. The defensibility comes
from:

1. **Maintenance velocity.** The continuous-ingestion + verify-before-write pipeline running 365 days/year per atlas is hard to replicate, hard to fake, and observable to anyone (the freshness page).
2. **Verification pedigree.** Every PMID cited is verified; every contested entity carries both sides + mainstream consensus. This is genuinely hard to do retroactively at scale, and once we're 12 months ahead, no one catches up.
3. **Network effects.** Clinicians contribute outcome data → engine recalibrates → recommendations get better → more clinicians adopt → more outcome data. Same shape as OncoKB's contributor model.

Revenue layers (in order of likelihood):
- **Lab partnership integrations.** Genova / Doctor's Data / Vibrant pay $10–50k/year to have their panel results auto-ingested into the engine. They get clinician retention; we get the canonical clinical-decision interpretation layer for their data.
- **Clinician-facing premium tier.** Free for individuals; $50–200/mo for high-volume practices that want patient longitudinal tracking + bulk profile generation + outcome-capture for cohort calibration.
- **Pharma / supplement-company licensing.** Companies pay to have their products evaluated under the same atlas-internal scoring framework — like LDL-C target reviews under CPIC. $25–250k/year per intervention class.
- **Research-license API.** Academic groups pay $5–25k/year for bulk API access for their own studies (mirrors OncoKB's commercial-license model).

Founder-fundable target: $2M seed at $10M cap on the canonical-knowledge-layer thesis after Long COVID atlas + 50 clinician adopters demonstrates traction. Confidence: MODERATE on this trajectory; HIGH on the underlying defensibility thesis.

## What this pivot is NOT

- **Not** a clinical decision support tool that replaces clinician judgment. The engine surfaces what the literature links to a profile; clinicians decide.
- **Not** a regulated medical device. Research/decision-support category, not 510(k) / De Novo.
- **Not** a content-marketing / course platform. We don't compete with IFM courses or Bredesen's ReCODE training programs — we're the substrate those courses cite from.
- **Not** an anti-mainstream advocacy project. Every contested entity carries the mainstream consensus position at equal prominence; the atlas records both sides because individual susceptibility may modify population-average risk.

## Open strategic questions (no engineering substitute)

1. **Public-org structure.** Foundation (Mozilla / Wikimedia model)? B-corp? Standard Delaware C-corp with open-source repo? Materially affects how lab partners and pharma engage. Recommendation pending tax + IP-counsel review.

2. **Data sharing with FM lab partners.** Do we ingest patient-identifiable lab results (HIPAA / BAA territory) or only de-identified responder cohorts? The first is much more powerful, much more regulated. Recommendation: start with de-identified cohorts only; layer in patient-identified workflows after SOC-2 + HIPAA compliance.

3. **Contribution governance.** Who can merge a PR that adds a contested-status entity? At v0.1 it's the founder; at v1.0 it has to be a curation board. Recommendation: bootstrap a 5-person scientific advisory board by month 6 — 2 FM clinicians, 2 academic researchers, 1 statistician.

## What survives 2027

The verification protocol, the continuous-ingestion pipeline, the evidence-
balance schema, and the per-condition atlas-instance architecture — all
domain-general, all defensible. If autism atlas plus Long COVID atlas plus
PCOS atlas plus Hashimoto's atlas all run on the same substrate and all
publish their freshness logs, **the substrate becomes the moat**, regardless
of which individual condition's atlas gets the most clinical adoption first.

The lethal failure mode to avoid: getting stuck in autism-only mode for
another six months, missing the window where Long COVID functional-medicine
practice consolidates its workflow around someone else's tool. Long COVID
clinical practice is being defined right now — there's a 24-month window
from May 2026 to be the canonical knowledge layer for it.
