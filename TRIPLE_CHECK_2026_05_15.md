# Triple-check audit — 2026-05-15

Independent review of commits `83ec99f`, `8177196`, `13e89d6`, `3806b2b`,
`5dcc64d`, `bff6c10`, `7994846`. Engine state verified clean; PMID-level
inspection surfaced two §24 violations that should block the push.

---

## Critical findings (must fix before push)

### C-1. SRC-001466 — wrong first author. CLAUDE.md §24 violation.

`v2.0_scored/sources.csv:1467` claims PMID 26370672 was authored by
"Park" — the JSON `raw_metadata` says `"first_author": "Park"`, and the
title field says "(Park et al., n=2586 ASD cases vs 600,103 controls)".
The row is flagged `"verified_against_pubmed": true`.

PubMed esummary for PMID 26370672 returns:

```
Authors: ['Windham GC', 'Lyall K', 'Anderson M', 'Kharrazi M']
Source: J Autism Dev Disord
Year: 2016 Feb
```

The first author is **Windham GC**, not Park. The publication year is
**2016**, not 2017 as the row states. PMID + title + journal are
correct; the numeric findings (MSAFP aOR=1.21 (1.07–1.37) for >90th
percentile) verify against the actual paper. So this is exactly the
failure mode CLAUDE.md §24 warns about: memory-based author/year
attribution stuck onto a real PMID. The `verified_against_pubmed: true`
flag is itself false.

The wrong attribution propagates to:
- `v2.0_scored/hypotheses.csv:97` (HYP-0076 description, two occurrences
  of "Park 2017")
- `v2.0_scored/biomarkers.csv:180` (BIO-0179 MSAFP description, "Park
  2017 PMID 26370672 aOR=1.21")
- `v2.0_scored/biomarkers.csv:181` (BIO-0180 PAPP-A description, "Park
  2017")
- `vault/hypotheses/HYP-0076 ... .md` (two "Park 2017" mentions)
- `vault/sources/SRC-001466 26370672.md`

### C-2. SRC-001467 — wrong first author. Same §24 violation pattern.

`v2.0_scored/sources.csv:1468` claims PMID 22152641 was authored by
"Bremer" — `"first_author": "Bremer"`, title "Bremer et al.", and again
`"verified_against_pubmed": true`.

PubMed esummary for PMID 22152641 returns:

```
Authors: ['Abdallah MW', 'Grove J', 'Hougaard DM', 'Nørgaard-Pedersen B',
          'Ibrahimov F', 'Mortensen EL']
Source: Can J Psychiatry
Year: 2011 Dec
```

The first author is **Abdallah MW**, not Bremer. No "Bremer" appears
anywhere on the author list. Title, journal, year, and finding match;
only the attribution is fabricated. Propagates to HYP-0076 (one
mention), `vault/hypotheses/HYP-0076 ... .md`, `vault/sources/SRC-001467
22152641.md`.

### C-3. SRC-001463 — three Hulscher → atlas HYP mappings are wrong.

`v2.0_scored/sources.csv:1464` (SRC-001463) notes field cross-maps the
Hulscher 9-factor framework to atlas HYP IDs. Three of those mappings
are wrong:

| Hulscher factor (notes string) | Stated mapping | Actual HYP-XXXX label |
|---|---|---|
| "sibling" | HYP-0002 | HYP-0002 = "Prenatal acetaminophen (paracetamol) exposure" |
| "in utero drug" | HYP-0004 | HYP-0004 = "PFAS / forever-chemical drinking-water exposure" |
| (environmental toxicants) | HYP-0005 / HYP-0007 | HYP-0005 = glyphosate (correct), HYP-0007 = "Gut microbiome dysbiosis" (wrong cluster) |

The Hulscher review's "sibling_recurrence" factor has **no
corresponding HYP** in the current atlas (no sibling-recurrence
hypothesis exists). The "in utero drug exposure" factor maps cleanly to
HYP-0010 (valproate) and HYP-0002 (acetaminophen), but not to HYP-0004
(PFAS) — that's an environmental toxicant, not an in-utero drug.

These mistakes also live in the original ingest script
`scripts/ingest_2026_05_14_hulscher_perinatal_prenatal.py` if it was
the source of the mapping string, so a fresh re-run would regenerate
them.

### C-4. HYP-0040 description misstates Modabbernia 2016's ASD finding.

`v2.0_scored/hypotheses.csv:41` says:

> "Modabbernia 2016 meta-analysis SRC-001464 (PMID 26820632) found
> neonatal acidosis OR=3.55 (2.23-5.49) for intellectual disability;
> perinatal hypoxia signals also elevated for ASD."

Verified against PubMed: the OR=3.55 (2.23–5.49) is correct **for
intellectual disability**. For ASD specifically the meta-analysis found
OR=1.10 (95% CI 0.91–1.31) — **not statistically significant** (CI
crosses 1). "Perinatal hypoxia signals also elevated for ASD" reads as
if there was a positive significant signal; the paper says the
opposite. The same misleading wording appears verbatim in
`raw_metadata.key_finding` on SRC-001464.

This is not a fabricated number — it's a softened summary of a null
finding presented as positive support. It will undermine the atlas's
credibility if a reviewer pulls the paper.

---

## High-priority findings

### H-1. `vault/.obsidian/workspace.json` is tracked but Obsidian rewrites it on every open.

The file is tracked (`git ls-files vault/.obsidian/workspace.json` →
present), but every Obsidian session — and every `build_vault.py` run
that touches the vault — leaves the file dirty. The recurring
`.git/index.lock` collisions and the workspace.json churn in commits
`83ec99f` and `5dcc64d` (52 + 54 line diff each, content irrelevant) are
both consequences. `.gitignore` should add:

```
vault/.obsidian/workspace.json
vault/.obsidian/workspace*.json
```

and the existing tracked copy should be `git rm --cached`. Low risk,
saves noise on every commit.

### H-2. Hulscher (SRC-001463) study_design + weight.

Row has `study_design=review`, and CLAUDE.md task spec text mentioned
"W_DESIGN weight (0.50)". The engine constant in
`run_scoring_v20.py:47` is `"review": 0.55`. So W_DESIGN is 0.55, not
0.50. Minor — but the "bumped tier" curator directive in the notes is
not actually implemented in code: there is no per-source weight override
applied; the source gets the normal review-tier weight (0.55 W_DESIGN ×
0.70 W_SOURCE_TYPE). If "bumped" was meant to mean "treat at primary-
document tier despite being non-PubMed-indexed," that didn't happen.

If the intent is to actually bump weight, either (a) add a curator-
override column to `sources.csv` and patch the engine to honor it, or
(b) change `study_design` to something with a higher W_DESIGN. Right
now the curator-directive string in the notes has no functional effect
on scoring.

### H-3. Modabbernia 2016 OR=3.55 attached to HYP-0040 subpopulation 3.

HYP-0040 SUBPOPULATION 3 description says:

> "Cord pH < 7.0 or 5-min APGAR < 5 are objective markers of perinatal
> acidosis. Modabbernia 2016 OR=3.55 driven primarily by this subset."

The OR=3.55 in Modabbernia is the **intellectual disability** outcome,
not ASD, and not subset-stratified by cord pH (the meta-analysis
aggregates across studies that use various proxies for impaired gas
exchange). Saying "driven primarily by this subset" is interpretation,
not what the paper reports.

### H-4. PMID 26370672 publication year inconsistency.

The SRC-001466 `raw_metadata.year` is 2017. PubMed esummary returns
`pubdate: 2016 Feb`. (Springer published online late 2015, print Feb
2016.) Downstream in HYP-0076 and biomarker rows the year is repeated
as "Park 2017." Either pick "2016" everywhere or document the print-vs-
epub distinction. Same row also has `date_published: 2015-09-15` — so
the row has three different "years" for the same paper (2015, 2016,
2017). Choose one canonical and stick to it.

### H-5. Park-attribution may originate in `ingest_2026_05_14_hulscher_perinatal_prenatal.py`.

Worth checking whether the ingest script hardcodes the wrong author
strings. If it does and you re-run from clean state, the bug
regenerates. Manually rebuilding `sources.csv` won't help long-term
without fixing the script source-of-truth too.

---

## Medium-priority findings

### M-1. Δ²-related stale concept references.

`SIX_MONTH_FAILURE_MODES.md` and `ACTIONABLE_REPORT_PRODUCT_SPEC.md` are
new (16 KB + 51 KB). No spot checks revealed factual drift, but they're
large and brand-load-bearing — recommend a separate dedicated read-
through before they get cited externally. Quick metric check passed:
"BIO-0179, BIO-0180 and HYP-0076 prenatal screening" reference in
`ACTIONABLE_REPORT_PRODUCT_SPEC.md` matches actual atlas entities.
Atlas state has 140 interventions (`wc -l v2.0_scored/interventions.csv
== 141` incl. header), 181 biomarkers (incl. header), 30 peptide files —
all align with the n=140 figure if mentioned.

### M-2. Living graph "peptide" search returns only 2 hits.

Task spec mentioned "search for 'peptide' (should match Cerebrolysin,
Selank, etc.)". The atlas has no Selank, Semax, BPC-157, Epitalon, or
similar nootropic peptides as `interventions` rows — only Cerebrolysin
(INT-0065) and intranasal oxytocin appear in the `peptide` category.
The v0.6.1 search index correctly returns 2 nodes for "peptide" — the
spec's claim was probably aspirational. Not a bug, but the spec text
should be reworded to "matches the 2 peptide-category interventions."

### M-3. SRC-001465 (Getahun) `date_published` set to 2017-01-31; PubMed says 2017 Feb.

PubMed esummary says `pubdate: 2017 Feb`. The row says `2017-01-31`.
Both are within range (epub usually precedes print by 1 month) and
either is defensible. Trivial.

### M-4. `v2.0.1_proposed/hypothesis_phenotype_proposed.csv` has 4 lines.

Touched in `83ec99f` (commit message doesn't mention it). Worth a
sanity glance — but no integrity issues from a quick read.

---

## All-clear list

The following checked out cleanly:

- **Engine runs**:
  - `validate_v02_calibration.py`: 4/4 PASS (case_011, case_015,
    case_020, case_026).
  - `compute_responder_mae.py`: cohort MAE = 0.0665 (n=8). Matches
    expected.
  - `pre_handoff_audit.py`: `0 CRIT / 0 HIGH / 0 MED / 12 LOW / 9 OK`.
    The 12 LOW are pre-existing combo-ingredient → INT slug name
    mismatches in `pre_handoff_audit.py` itself (e.g. "p5p" not found
    as INT label) — not introduced by this session.
  - `build_vault.py`: clean rebuild, 0 unresolved wiki-link targets.
    Counts: 76 hypotheses (HYP-0076 added), 34 mechanisms, 140
    interventions, 25 combinations, 11 phenotypes, 1560 sources, 1 gene
    page.
- **INT-0001 calibration**: 83.35 preserved, unchanged across session.
- **Δ² calibration trajectory** (82.72 → 81.95 → 83.65 → 83.35)
  documented in CLAUDE.md; matches the project's own narrative.
- **PMID 26820632 (Modabbernia)**: verified — title, authors
  (Modabbernia A, Mollon J, Boffetta P, Reichenberg A), year (2016),
  journal (J Autism Dev Disord) all match `raw_metadata`. The OR=3.55
  for ID is real. (Only the ASD-elevation framing is the issue —
  see C-4.)
- **PMID 28099978 (Getahun)**: verified clean — first author Getahun D,
  year 2017, journal Am J Perinatol, sample size 594,638 all match. The
  10%/22%/44% birth-complication / pre-labor / both figures match the
  paper.
- **Intake pipeline scripts**: `scripts/intake/pubmed_rss_scanner.py`,
  `browser_social_scanner.py`, `intake_orchestrator.py`, and
  `scripts/ingest_2026_05_14_hulscher_perinatal_prenatal.py` all
  `py_compile` clean.
- **GitHub Actions workflow** (`.github/workflows/autonomous-discoveries.yml`):
  PubMed scanner step added at line 42–47; determinism gate (line 62–
  74), calibration-anchor smoke test (line 76–86), and v2.0_scored/-
  write defense (line 88–104) all intact.
- **Living graph v0.6.1** (`living_graph.html`):
  - DATA blob has 636 nodes / 1061 links (CLAUDE.md spec said "1061
    edges" — matches).
  - Node-type counts: G=320, I=90, B=80, H=76, M=34, C=25, P=11.
  - 8 PROFILES including `hulscher`.
  - TYPE_COLOR has entries for B and C node types.
  - Intervention `c` field (category) included in `ll` search index —
    verified on samples INT-0001 through INT-0005.
  - No `__XXX__` template markers remain.
- **vault/peptides/**: 30 files preserved.
- **vault/Discoveries_Inbox/pubmed_intake_2026-05-14.json/.md**: present.
- **HYP IDs in Hulscher mapping** (other than the 3 wrong ones in C-3):
  HYP-0009, HYP-0041, HYP-0028, HYP-0008, HYP-0025, HYP-0010,
  HYP-0011, HYP-0014, HYP-0043, HYP-0022, HYP-0044, HYP-0059,
  HYP-0066-0069 all exist and labels match the Hulscher mapping.
- **HYP-0076 prenatal screening marker anomaly**: new entry valid,
  CSRS 0.55, evidence-balance fields populated, mainstream-consensus
  field populated, source PMIDs (26370672; 22152641) match the actual
  source records.
- **BIO-0179 MSAFP + BIO-0180 PAPP-A**: schema integrity holds.
  Reference ranges (0.5–2.0 MoM, 0.7–1.5 MoM normal-of-normal) are
  conventional and defensible. The only issue is the "Park 2017"
  attribution carried over from C-1.

---

## Recommendation

**Do not push as-is.** Apply C-1 through C-4 first.

Concretely:

1. **Patch first_author fields and prose mentions** for SRC-001466
   (Park → Windham GC) and SRC-001467 (Bremer → Abdallah MW) across
   `v2.0_scored/sources.csv`, `hypotheses.csv` (HYP-0076), `biomarkers.csv`
   (BIO-0179 + BIO-0180), and the corresponding `vault/` markdown.
   Also fix the year on SRC-001466 (2017 → 2016).
2. **Fix the Hulscher HYP cross-mapping string** in SRC-001463 notes
   (and in the ingest script, if it lives there). Drop the "sibling →
   HYP-0002" claim entirely until a sibling-recurrence HYP exists;
   move "in utero drug" off HYP-0004.
3. **Fix the Modabbernia 2016 ASD framing** in HYP-0040 prose and in
   SRC-001464 raw_metadata: state explicitly that the ASD signal was
   non-significant (OR 1.10, 95% CI 0.91–1.31) while ID was OR 3.55.
   The HYP-0040 subpopulation-3 sentence claiming OR=3.55 is "driven
   primarily by this subset" should be removed or rewritten.
4. **Re-run** `build_vault.py` + `pre_handoff_audit.py` + the two
   validation scripts to confirm nothing breaks.
5. **Optional but worth it**: `.gitignore` for
   `vault/.obsidian/workspace.json` and `git rm --cached` the tracked
   copy.

C-1 and C-2 are the kind of failure mode CLAUDE.md §24 was written to
prevent — both rows have `"verified_against_pubmed": true` while
carrying fabricated author names. Shipping them silently sets a
precedent that the §24 protocol can be claimed without actually
performing the author check. That's worth catching before the push,
not after.

The engine itself is in good shape. Calibration anchor + cohort MAE +
audit gates all hold. The defects are at the citation-metadata layer.

---

*Audit performed 2026-05-15. All PubMed verifications via
`https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi`.*
