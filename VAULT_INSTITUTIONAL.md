# Causes Atlas — Deterministic Evidence-Ingestion Substrate

> Federal-grade reference document. Describes the atlas's automated ingestion + curator-gated promotion architecture in language appropriate for HHS, NIH, FDA, and academic-medical-center reviewers. Companion to VAULT.md (the operational orchestrator file).

---

## Architectural summary

The Causes Atlas is a **deterministic evidence-ingestion substrate with curator-gated promotion workflows**. The substrate operates a five-stage pipeline that runs continuously without human intervention. All atlas modifications require explicit curator approval before propagating to the canonical scored state.

```
Ingestion ─→ Verification ─→ Inference ─→ Discovery ─→ Curation
```

| Stage | Function | Human gate |
|---|---|---|
| Ingestion | Automated PubMed RSS retrieval, full-text extraction, structured field population | None — fully automated |
| Verification | PubMed esummary cross-check (author + year + key term match) | None — fully automated; refuses non-matching records |
| Inference | Deterministic phenotype-loading vector computation; same input → byte-identical output | None — auditable mathematics, no language-model calls |
| Discovery | Pattern miners scan the atlas state for emergent cross-domain candidates (gene × mechanism, intervention combination gaps, higher-order causal chains, responder-phenotype gaps) | None — output to read-only inbox |
| Curation | Human reviewer evaluates discovery candidates, approves or rejects atlas modifications | **Required** — no automated promotion to canonical scored state |

This architecture provides the auditability federal review requires. Every atlas claim traces to a PMID-verified primary source. Every scoring computation reproduces byte-identical across machines. Every discovery candidate documents its provenance.

---

## Operating pipelines

### Continuous ingestion subsystem

A scheduled retrieval process runs daily at 06:00 UTC, fetching newly indexed PubMed records matching curated query patterns relevant to the atlas's scope. Each candidate record is verified against PubMed esummary before any structured field is written. Records failing verification are rejected and logged. Records passing verification enter the discovery candidate queue. **The substrate cannot ingest a fabricated PMID.** This is enforced at the code level, not by policy.

### Pattern-discovery subsystem

A scheduled analytical process runs daily at 07:00 UTC, executing four deterministic finders against the current atlas state:

1. **Emergent edges** — gene × mechanism / gene × phenotype co-mention candidates exceeding configurable threshold
2. **Combination gaps** — intervention pairs/triples sharing biological mechanism not yet captured as combination entities
3. **Higher-order causal chains** — graph-walk for n-th-order chains (intervention → mechanism → phenotype) where direct edges do not exist
4. **Responder-phenotype gaps** — interventions with mainstream-mixed-evidence status not yet tagged with a responder-phenotype profile

Output is written to a read-only inbox. **No discovery candidate is promoted to atlas state without explicit curator review.** This is the curator-gated promotion protocol.

### Trajectory-tracking subsystem

A research-attention velocity analysis (Δ²) runs continuously, tracking five components per atlas entity: recency acceleration, cross-design convergence, subset-validation signal, replication independence, and trajectory-mismatch (contested-status entities with tier-1 primary records). Output identifies entities where the evidence base is accelerating, distinguishing trajectory from steady-state truth-strength.

The Δ² subsystem includes a **code-enforced anti-reflexivity audit**: it tests Spearman rank correlation between previous-run rankings and inter-run new-source counts. If correlation exceeds 0.70 (curator behavior preferentially feeding already-trending entities), the pipeline halts. This is the structural defense against reflexive evidence-base inflation.

### Validation subsystem

The substrate maintains a calibration cohort of n=8 published RCTs with full-text-extracted responder rates. The deterministic engine is benchmarked against this cohort daily. Current cohort mean absolute error: 0.067 (6.7 percentage points). Restricted to entries within engine biomarker-driver coverage (n=7): MAE = 0.049. Four entries below 3% absolute error span three mechanistically independent intervention classes (oxidative stress, methylation, GABA/Cl⁻ axis); a fifth entry (inflammation, AE 0.069) extends the spread to four independent axes at sub-7% — structural replication.

The **calibration anchor protocol** requires that the leucovorin intervention (INT-0001) maintain an atlas signal score ≥80 across all atlas modifications. Any modification that would cause regression below this threshold halts the modification.

---

## Curator-gated promotion workflow

All atlas state modifications follow this protocol:

1. Discovery candidate enters the read-only inbox via the pattern-discovery or continuous-ingestion subsystem
2. Curator reviews the candidate against atlas methodological standards (epistemic principles §2-§9, see [`CLAUDE.md`](CLAUDE.md))
3. If candidate is supported by PMID-verified primary evidence, curator authors atlas modification
4. Modification re-runs scoring engine
5. Calibration anchor protocol verifies INT-0001 ≥ 80
6. Determinism verification: scoring outputs reproduce byte-identical across consecutive runs
7. Modification commits to canonical scored state with PMID + reasoning in commit log

Modifications failing any verification step do not proceed. Modifications that bypass the curator review step are rejected at the version-control level (path-allowlist enforcement on automated processes).

---

## Determinism guarantees

The substrate makes three explicit determinism guarantees, all code-enforced:

1. **Scoring determinism** — same input → byte-identical output across runs and machines. No random seeds, no LLM calls in scoring math, no time-dependent state.
2. **Provenance determinism** — every atlas claim traces to a specific PMID with verification timestamp.
3. **Visualization determinism** — even the pattern-discovery output and visualization layer use deterministic seeding so reloads produce identical results.

These guarantees are verified continuously: 3-run byte-identical determinism tests gate every automated pipeline run. Pipeline halts on any drift.

---

## Open-source substrate positioning

The substrate is **MIT-licensed open source**. The architecture is condition-agnostic. Autism is the first fully instantiated atlas; the same engine, scoring protocol, verification protocol, discovery pipeline, and validation framework operate on any chronic condition where effect heterogeneity dominates the published literature.

Already supported: Long COVID atlas v0.1 (manifest + phenotype taxonomy + verified primary sources, separate branch). Architecture supports forking to ME/CFS, Lyme disease + co-infections, Ehlers-Danlos / hypermobility spectrum, PANS/PANDAS, polycystic ovary syndrome, attention-deficit/hyperactivity disorder, mood disorders, or any condition where mainstream meta-analytic methods systematically dilute biologically distinct subgroup signals.

**Core thesis: shared infrastructure, condition-specific evidence graphs.** The substrate provides reproducible methodology; condition-specific instantiations provide domain expertise.

---

## Replication for other research communities

Research groups, patient advocacy organizations, federal agencies, or academic medical centers may fork the substrate to instantiate condition-specific atlases. Substrate components include:

- The 22-entity-table canonical schema (`v2.0_scored/` reference structure)
- The deterministic inference engine (`personalized_risk.py`, condition-agnostic via `--atlas-path` flag)
- The verification protocol (`scripts/seed_with_verification.py`)
- The pattern-discovery suite (`scripts/find_*.py` × 4 + `scripts/run_autonomous_discoveries.py`)
- The trajectory-tracking subsystem (`scripts/compute_delta_squared.py`)
- The calibration framework (`scripts/validate_v02_calibration.py`, `scripts/compute_responder_mae.py`)
- Repository-level governance documentation (`CONTRIBUTING.md`, `ATLAS_OS_README.md`)

Curator commitment for a new condition atlas is approximately one full-time-equivalent for initial seeding, transitioning to 0.2–0.3 FTE for ongoing curation as the discovery pipeline matures. The substrate carries the analytical load; the curator provides domain expertise and gatekeeping.

---

## Compliance posture

- **Open-source MIT license** — no vendor lock-in, no vendor capture, full forkability for community oversight
- **No telemetry** — substrate does not transmit user data
- **No protected health information processing** — substrate operates on published literature; clinical deployment for PHI requires HIPAA-compliant hosting tier with executed Business Associate Agreement
- **Deterministic auditability** — every scoring computation reproduces byte-identical, supporting regulatory review and continuous monitoring
- **Source-quality hierarchy enforced** — source weights tied to study design and source type via published criteria; industry-funded research, advocacy content, and fact-check journalism are explicitly down-weighted but not erased

---

## Citation

Greg [LAST]. (2026). *Causes Atlas: Deterministic Evidence-Ingestion Substrate for Condition-Specific Causal Inference. Engine v0.4.0.* MIT License. Repository: github.com/abel-causesatlas/Autism. Citation DOI: pending Zenodo deposit.

---

*This document is the federal-grade companion to [`VAULT.md`](VAULT.md). The two files describe the same architecture in different registers: `VAULT.md` is the operational orchestrator file (instructions to AI agents reading the vault); this document is the institutional reference for federal, regulatory, and academic-medical-center review.*
