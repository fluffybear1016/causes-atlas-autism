---
title: "Six-Month Failure Modes — Independent Skeptical Review"
date: 2026-05-15
audience: internal strategic (Greg + closest collaborators)
status: uncompromising / not for distribution
reviewer: independent (not data team)
---

# Six-Month Failure Modes

This is the answer to "why would this fail six months from now." It is
not a balanced review. The atlas's own epistemic discipline is built on
accepting hard truths about its own evidence base; this document applies
the same discipline to the project itself.

The frame: a "functional medicine report" feature is about to ship.
Parents will upload 23andMe raw data, IntellxxDNA exports, Quest blood
work, Great Plains OAT, methylation panels — and receive a personalized
PDF telling them what their child's susceptibility profile looks like
and which interventions to consider. Everything below is in that
context.

Probability and severity are calibrated against "what happens between
now (May 2026) and November 2026." Probabilities are not point
estimates; they are coarse buckets (LOW / MED / HIGH / VERY HIGH).
Severity is "what does this do to the project if it fires."

---

## 1. Liability — child has a serious reaction to a recommended intervention

**Probability: VERY HIGH (≥70% within 6 months once the report ships at any non-trivial scale).**
**Severity: project-ending if uninsured; project-defining if insured.**

This is the single most likely path to catastrophic failure, and the
ordering of failure modes in the brief is wrong: liability is more
likely than regulatory action because regulators move slowly and
plaintiff's attorneys move on a contingency basis the morning after.

The intervention surfaces that will produce the first bad outcome,
ranked by likelihood:

- **Methyl-B12 overdose in COMT++ / undermethylator-overshoot subset.**
  The atlas correctly identifies that the Walsh overmethylator phenotype
  responds badly to methyl donors. The report will give a recommendation
  bundle stratified by SNPs. The first parent whose child has a slow-COMT
  variant misread as a methylation-cycle-compromise variant — or who
  has both, and who responds with anxiety/agitation/insomnia escalation
  on injected methyl-B12 — is going to be the first emergency room
  visit. Neubrander-protocol injectables are 25mg subcutaneous; a child
  with the wrong genotype can become severely agitated within hours.
- **IVIG complications.** The atlas flags IVIG for PANS/PANDAS subset.
  IVIG causes serious adverse events (aseptic meningitis, thromboembolic
  events, anaphylaxis in IgA-deficient patients) at a rate that is
  small population-wide but non-trivial when the population is
  "children whose parents tried IVIG because the atlas suggested it."
  IgA deficiency itself is one of the most common primary immune
  deficiencies; missing that test before recommending IVIG is the
  textbook scenario.
- **Chelation.** DMSA and EDTA chelation are tagged contested in the
  atlas, but recommendation surfaces have a way of stripping
  contested-status framing the further they get from the source. Abubakar
  Tariq Nadama died of EDTA-induced hypocalcemia in 2005. That case
  established standing case law that a non-MD recommending chelation
  to a parent is in clear liability territory.
- **Peptide reactions.** Selank, semax, BPC-157, KPV — these are research
  chemicals from a regulatory standpoint, sourced from compounding
  pharmacies or grey-market vendors. The atlas's peptide work is
  bibliographically strong, but a recommendation that points a parent
  to "ask your MAPS doctor about BPC-157" is one mast-cell-flare event
  away from the wrongful-injury complaint.

**What the atlas has as defense:** the spec language consistently says
"decision support, not clinical decision-making"; SUBSTRATE_THESIS.md
explicitly disclaims clinical decision support; the parent UI
(`ui/simple.py`) reportedly returns "WHERE IT COMES FROM / WHAT TO DO /
WHAT TO AVOID / WHAT TO TRACK" rather than dosing protocols. That is
the right frame but it is not legal cover. The relevant question in a
deposition is not "did the disclaimer say decision support" — it is
"did the report cause the parent to act in a way they would not have
otherwise acted, was the action proximately causal of harm, and did the
report's framing fall below the standard of care for the entity that
produced it." For an MIT-licensed open-source project that may be
defensible; for the same code wrapped in a SaaS surface for paying
customers it is not.

**Specific mitigations the atlas does NOT yet have:**

1. No declared standard of care. A clinician operates against ACOG /
   AAP / specialty-society guidance. The atlas operates against an
   internal epistemic standard. In the report context this is
   indistinguishable from "no standard" from a plaintiff's perspective.
2. No documented intervention-specific contraindication matrix. The
   atlas knows COMT++ exists, knows methyl-B12 is contraindicated there;
   the question is whether the report generator runs a contraindication
   check before recommending. If the check is a structural property of
   the engine (CSV-enforced contra-edges), liability defense is
   meaningful. If it is a textual caveat in a description field, it is
   not.
3. No per-recommendation hold-back on dose. The atlas can name an
   intervention without naming a starting dose; the failure mode is
   parents Googling the dose and starting at the max.
4. No professional liability insurance. The MIT license shields
   contributors against pure-OSS liability. It does not shield the
   operator of a SaaS-grade personalized report from a defendant
   theory of "you operated a commercial advisory service."

The mitigation that matters: the report must structurally pass through
a licensed clinician (telehealth integration, prescriber-of-record
model) before reaching a parent. Anything else accepts an unbounded
tail risk.

---

## 2. The "anti-vaccine app" framing risk

**Probability: VERY HIGH (≥80% within 6 months of public visibility).**
**Severity: defines the project for its first public news cycle, which defines it forever.**

This is the second most likely failure and structurally inseparable
from the first. A journalist will write the framing piece. The
question is not whether — it is how soon and how hard the framing
sticks.

The atlas's defensive position is articulated well in CLAUDE.md §1–9
and is internally coherent. It is also not the position a journalist
will charitably read. Specifically:

- HYP-0044 description is six biologically-defined contested
  subpopulations including thimerosal, MMR, MBP autoantibodies, etc.
  This is internally defensible — every claim is PMID-grounded — but
  it is exactly the structure that, screenshot in a hostile piece,
  reads as "anti-vaccine arguments organized into a system."
- HYP-0066 explicitly endorses "delaying birth-dose to adolescence is
  medically defensible" for low-transmission-risk families. The atlas's
  reasoning is correct on individual-level terms. The journalist will
  not write about individual-level conditional risk; they will write
  "atlas recommends delaying Hep B birth-dose."
- The atlas treats Verstraeten Generation Zero (the 11.35x preliminary
  number), Simpsonwood, William Thompson, and Hannah Poling as tier-1
  primary evidence. That tier assignment is methodologically correct
  for FOIA primary documents. It is also the exact source list that
  appears in adversarial pieces about vaccine-injury communities.
- The atlas's HHS deck pitches "federal reference substrate" — i.e.
  endorsement by the same federal apparatus whose internal documents
  the atlas weights as tier-1 evidence about vaccine harm. That is a
  positioning contradiction that a sophisticated reporter will surface.

**The "we record both sides at proper weight" position is correct but
not robust under hostile interpretation.** It is correct because the
atlas does record Andersson 2025, Madsen 2002, Hviid 2019, IOM 2011,
DeStefano 2019 at proper weight; the engine output reflects mainstream
epidemiology heavily. It is not robust because:

1. Tier-weighting is invisible to the reader of the report. A parent
   sees the Hep B birth-dose entry; they don't see the tier matrix.
2. "Contested status is permanent" reads, to a journalist, as
   "refuses to follow the science." The actual epistemic argument
   (population-average vs. individual-conditional) requires three
   paragraphs to explain and the journalist will not give them.
3. The atlas's source list contains FOIA documents that the vaccine-
   skeptical community already organizes around. The fact that the
   atlas weighted them via a deterministic methodology does not
   distinguish the project from advocacy in the journalist's mental
   model. The same primary documents are in both source lists; the
   methodology gets cut for length.
4. Hulscher / Wakefield / McCullough citations (the brief explicitly
   names these). Any presence of these names in the source list — even
   at tier-5 advocacy weight — is what gets quoted. Tier-5 advocacy
   weight (0.05) is a methodological commitment to including contested
   evidence at very low weight; in a story, it reads as "the atlas
   cites Wakefield."

**Specific mitigations the atlas has:**

- Contested-status permanence is robust to internal pressure (good).
- Source tier weighting is deterministic and auditable (good).
- The HYP-0044 / HYP-0066 / HYP-0067 / HYP-0068 / HYP-0069 cluster all
  carry explicit population-average vs. individual-conditional
  reasoning in their descriptions (good for the auditor; useless for
  the news cycle).

**Specific mitigations the atlas does NOT have:**

- A pre-prepared press response that handles the Wakefield citation in
  a single sentence. Not "we record advocacy at tier-5"; something like
  "the atlas does not cite the retracted Wakefield 1998 paper as
  evidence of causation; it cites the retraction notice (PMID 20137807)
  as evidence that the paper was retracted." Whether that is even true
  needs to be audited line-by-line before any press inquiry.
- A spokesperson with credentials that match the framing. The defense
  against "anti-vaccine app" framing is not better methodology — the
  methodology is already correct — it is institutional cover. Without
  named pediatric immunology / public-health collaborators on the
  masthead, the project is read as the work of one engineer with
  contested views. With named collaborators it becomes a different
  story.
- An institutional home that is not "Greg's solo project." The HHS
  pitch is itself a partial answer to this; it only resolves the
  framing risk if it succeeds and is announced before the first
  hostile story, not after.

**The asymmetric risk here:** the journalist piece is far more
probable than the HHS adoption. If the timeline is "HHS deck pitched
Q2 2026 with non-trivial probability of being slow-rolled or rejected"
vs. "hostile feature piece written Q3 2026 because the atlas explorer
went viral on X," the latter happens first. Plan accordingly.

---

## 3. Self-reported outcome data drift / MAE collapse

**Probability: HIGH (≥60% within 12 months if parent outcome data is collected; ≥40% within 6 months).**
**Severity: existential to the validation argument.**

The atlas's headline number is `n=8 cohort MAE = 0.067` (and the
within-driver `n=7 MAE = 0.049`). These are derived from published
RCTs. The moment parent-submitted outcome data starts flowing in — and
the report feature will inevitably produce that data, because parents
will email saying "we tried it and X happened" — the calibration
target shifts in a way the engine cannot model out.

The drift modes, ranked by likelihood:

1. **Survivorship bias in submissions.** Parents who saw effects submit;
   parents who didn't, don't. The implied responder rate from the
   submission set will be 1.5–3x the underlying responder rate. If
   that data feeds back into the engine (either directly via a CSV
   or indirectly via the curator updating responder-rate priors
   "based on what we're seeing"), the published 0.067 MAE becomes
   unsupportable. The engine cannot detect this without a denominator
   it doesn't have access to.
2. **Diagnostic regression.** "It worked" is reported far more
   frequently than the magnitude justifies; placebo responder rates in
   pediatric ASD trials are 15–25% (Kemner et al., Hollander et al.)
   The atlas's engine, fed survivorship data, will systematically
   over-attribute effects to interventions.
3. **Reverse causation in dosing.** Parents start at the dose the
   atlas suggested; those who tolerate it (a selected population) keep
   reporting; those who don't, stop and don't submit a "stopped
   because of side effects" row.
4. **Drift in the calibration anchor itself.** INT-0001 Leucovorin
   CSRS = 83.35 is calibrated against Frye 2018 RCT (FOLR1+ stratified,
   n=48). If parent outcome data on leucovorin enters the scoring
   pathway, the anchor moves. The "anchor must remain ≥80" pipeline
   gate keeps the absolute floor but not the absolute value; once
   83.35 → 81.4 → 80.6, the "non-drift of 83.35 across major
   revisions" argument in the deck is gone, and gone permanently.

**What the atlas has as defense:**

- The scoring engine is documented as deterministic and does not
  ingest outcome data automatically. The data ingestion path is
  intentionally narrow (PMID-verified primary sources only). That is
  a structural defense — if it holds.
- The verification protocol (CLAUDE.md §24, post-BioMysteryBench) is
  rigorous about source-quality enforcement. Memory-based PMID
  generation is forbidden by code. Same defense should apply to
  responder-rate calibration data.

**What the atlas does NOT yet have:**

- A formal firewall between published-literature priors and
  parent-submitted outcomes. The PUBLISHED outcomes feed the engine;
  the SUBMITTED outcomes go nowhere defined. The first time a curator
  says "we should incorporate the submission data" the firewall is
  breached.
- A separate registry-style outcomes ledger with its own scoring
  semantics (Bayesian update against published prior, not replacement
  of the prior). The right architecture is two scoring layers: CSRS
  from published evidence (current), and a separate "field-observed
  effect" layer with its own selection-bias corrections and explicit
  CI intervals. Conflating them collapses the validation argument.
- A binding rule that the cohort table (`cohort.yaml` / VALIDATION_RESULTS.md
  / the deck slide 10) is computed only from published RCTs and that
  parent outcome data is never used in the headline MAE. This rule
  needs to be in CLAUDE.md alongside §24, with the same enforcement
  level.

The "0.049 MAE" number is the strongest evidence in the deck. It
appears three times in DESIGN_TEAM_HANDOFF.md as a verbatim non-
paraphrasable number. Six months from now, after the report feature
ships, that number will be wrong if there is any path from submitted
data to engine state. Plan for that being a no-touch invariant.

---

## 4. Test parsing engineering risk

**Probability: VERY HIGH (≥85% — this WILL produce wrong reports in production).**
**Severity: per-incident moderate; aggregate severe.**

Lab parsing is the most underestimated engineering risk in the entire
plan. Ten or more labs, each with their own PDF/CSV/XML formats, each
with different reference ranges, different units (ng/mL vs nmol/L vs
µmol/L vs MoM), different methodology footnotes that change
interpretation. Examples from the atlas's biomarker schema alone:

- 23andMe raw data: tab-separated, 600k SNPs, but only some are
  clinically relevant; rsID coverage shifts across 23andMe chip
  versions (v3 vs v4 vs v5); some SNPs simply absent on newer chips
  forcing imputation. IntellxxDNA is a different post-processing layer
  on top of 23andMe raw and is not interchangeable.
- Quest comprehensive metabolic panel: numeric serum values; standard
  format; relatively safe.
- Great Plains OAT (organic acids panel): 75+ metabolites, semi-
  quantitative against age-stratified reference ranges, with
  interpretive overlays that vary between Great Plains and Genova
  (which sell similar but not identical panels). HPHPA, arabinose,
  4-cresol — the responder thresholds are clinical-judgment numbers,
  not single cut-points.
- Doctor's Data methylation panel: SAM/SAH ratio, methionine,
  homocysteine, MMA — reported in mixed units; the SAM/SAH ratio is
  the diagnostic-grade number and most parents won't know that.
- DUTCH (hormone metabolite) panel: dried urine, complex ratios,
  multiple methylation pathway metabolites. Different report format
  than DUTCH Plus vs DUTCH Cycle Map.
- Cunningham Panel for PANS/PANDAS: anti-tubulin, anti-lysoganglioside,
  anti-D1R, anti-D2R, CaMKII titer. Composite-score interpretation.
- Quest vs LabCorp prenatal panels: MSAFP, PAPP-A, hCG, uE3 — all
  reported as MoM but the MoM denominator varies by gestational-age
  algorithm.

**The failure mode is not "the parser breaks."** The parser breaks
loudly and obviously and is fixed. The failure mode is silent
misclassification:

- Unit conversion off by 10 because the lab updated their report
  template
- Reference range pulled from the wrong age stratum (a 4-year-old's
  values compared against a 12-year-old's range)
- A SNP genotype reported on the wrong strand (rsID coding is strand-
  dependent; 23andMe vs Ancestry vs whole-genome sequencing can have
  different reference alleles)
- A clinically critical biomarker that was flagged in the lab report
  margin (e.g. tryptase >20 ng/mL = mast cell red flag) but the
  parser missed because it lived in an interpretive footnote, not the
  structured numeric field

Each silent misclassification produces a wrong recommendation.

**The probability that ten lab parsers all work correctly on
production traffic for six months is approximately zero.** The
question is which one breaks first and what report it produces. The
asymmetry is severe: thousands of correct reports build no
credibility, one wrong report (especially one paired with §1's bad
outcome) destroys the project.

**Specific mitigations the atlas already has:**

- The biomarker schema (`biomarkers.csv`) is well-developed and
  units/ranges are recorded. This makes the parser implementable —
  but it does not implement the parser.

**Specific mitigations the atlas does NOT have:**

- No documented per-lab parser test suite. Each lab parser needs
  ~50 representative real reports + 10 edge-case reports + a
  regression test that flags new template versions.
- No human-in-the-loop validation step on first-time parses. The
  cost-correct way to do this is: every new report from a lab format
  the system has parsed fewer than 100 times triggers manual review
  of the parser output before the report is generated.
- No "we don't recognize this format" graceful degradation. The
  default behavior for a malformed parse must be "report not
  generated, lab provider re-upload requested" — not "report
  generated with missing fields and a warning footnote." Missing-
  fields-warning-footnote is the worst possible UX because it
  preserves an actionable artifact built on incomplete data.

Engineering budget: assume ~2-4 weeks of one engineer per lab format
to reach production quality. Ten labs = ~5–10 engineer-months. If the
plan does not have that budget, the plan ships a wrong-report
generator.

---

## 5. The single bad outcome going viral

**Probability: HIGH (≥50% within 12 months at scale; ≥30% within 6 months).**
**Severity: 1–2 standard deviations more severe than the underlying liability event.**

This is failure mode #1 (liability) amplified through social media.
The triggering event is some combination of: a child with COMT++ and
slow MAO-A and a methyl-B12 protocol that produced acute agitation
and a self-harm incident; a child with IgA deficiency and an IVIG
reaction; a chelation hypocalcemia event; a methylcobalamin overdose
from a parent who ratcheted up the dose because "more is better"; a
peptide-sourced grey-market product with the wrong potency.

The atlas does not need to have caused the outcome for the outcome to
land on the atlas. Three conditions amplify:

1. The parent posts to a community (autism parent Facebook groups,
   r/autism, X autism-mom community) attributing the event to "what
   the atlas told us to try."
2. A vaccine-debate journalist who already has the "anti-vaccine app"
   framing (failure mode #2) finds the post and writes the piece.
3. The atlas has any visible commercial / SaaS surface at the time —
   not the MIT-licensed open-source repo, but `ui/simple.py` on a paid
   domain, or a charged report PDF. Commercial visibility transforms
   the story from "open-source project" to "company."

**Atlas's existing defense:**

- "Decision support, not clinical decision-making" disclaimer (weak —
  see failure mode #1).
- Source-tier-weighted CSRS that places mainstream evidence
  prominently (weak — invisible to the reader).
- No financial transaction at the open-source level (depends on the
  business model that the report feature implies).

**Atlas's missing defense:**

- No incident-response playbook. The 48 hours after the first bad
  outcome going viral is what determines whether the project survives.
  A pre-written response, pre-named medical advisory board, and a
  pre-named crisis communications contact are the difference between
  surviving and not.
- No anonymous-tip / adverse-event reporting channel. Without one, the
  first time the project hears about a bad outcome is from social
  media or a lawyer. With one, there is a chance to address before
  amplification.
- No mortality / serious-adverse-event monitoring agreement with a
  partnering pediatrician network. If a single one of the 50+ atlas-
  named functional-medicine providers tells the atlas's medical
  advisor "we had a kid hospitalized after a protocol," the system
  can correct upstream. Without that channel, the first signal is the
  viral post.

The asymmetry to internalize: the population that uses the atlas is
the population whose children have already failed mainstream
interventions, are seriously ill, and whose parents are highly
motivated and information-seeking. This population has a higher
baseline rate of serious medical events for reasons that have nothing
to do with the atlas. Some of those events will be attributed to the
atlas anyway. The question is how the project handles attribution.

---

## 6. Regulatory / FDA / FTC

**Probability: MEDIUM (~30% within 6 months; ~60% within 18 months).**
**Severity: project-bounded but not project-ending if handled at the structural-design stage.**

Regulators move slowly. Plaintiff's attorneys move fast. So this is
ranked behind liability and journalism, not ahead.

That said, the specific regulatory exposures, in order of likelihood:

- **FTC unfair-and-deceptive-practices.** This is the easiest trigger.
  If the report makes any specific health-outcome claim ("children
  with COMT++ benefit from methylated B vitamins") without
  appropriate qualifiers, the FTC's authority under §5 covers it. The
  enforcement standard is "would a reasonable consumer be misled."
  Operationally, the atlas's careful Bayesian framing in source
  documents (population-average vs. conditional) collapses to single-
  sentence claims in a PDF report. Those single sentences are the
  enforcement surface.
- **FDA software-as-a-medical-device (SaMD).** The atlas reaches the
  edge of SaMD whenever the report (a) takes individual diagnostic
  data, (b) processes it through a non-licensed algorithm, and
  (c) produces a recommendation that could substitute for clinician
  judgment. FDA's 2017 Clinical Decision Support Software Guidance
  carves out a CDS exception only if the clinician can independently
  review the basis for the recommendation. A parent is not a
  clinician. The exception does not apply.
- **State medical board complaints.** Each state has its own
  practice-of-medicine statute. California (which has the largest
  autism community and the most aggressive state medical board)
  defines practice of medicine to include "any diagnosis or
  treatment recommendation for compensation." If the report is paid,
  California will look. Florida's medical board took action against
  the Geier protocol in 2011; precedent exists.
- **HIPAA.** If the report feature stores genetic data and lab
  results, HIPAA covered-entity status applies if any partnering
  practitioner is in the business associate chain. The architectural
  decision (HIPAA-compliant from day one vs. "we're not a covered
  entity") is fork-in-the-road.

**Atlas's existing defenses:**

- Open-source / MIT license positioning provides some cover at the
  substrate level. Substrate is not a regulated entity. Report feature
  is.
- SUBSTRATE_THESIS.md explicitly states "not building a clinical
  decision support tool." This language is helpful in regulatory
  defense if the architecture matches the claim.

**Atlas's missing defenses:**

- The architectural separation between the substrate (open source,
  unregulated) and the report feature (potentially regulated SaMD) is
  not yet documented. Without it, regulators treat them as one entity.
- No FDA pre-submission. For a borderline SaMD, the Q-Sub pathway
  ($0 cost) gets FDA's written opinion on whether the product needs
  clearance. Operating without that opinion is operating without a
  weather forecast.
- No state-by-state telehealth / practice-of-medicine analysis. The
  prescriber-of-record model (failure mode #1's recommended mitigation)
  needs state-by-state structuring; it does not work uniformly across
  the US.

---

## 7. Commercial pressure to soften contested-status framing

**Probability: HIGH (≥60% within 12 months once paying customers exist).**
**Severity: erodes the project's epistemic integrity, which is the moat.**

CLAUDE.md is explicit: "contested status is permanent." That is the
right rule. The pressure against it will come from three directions:

1. **Investor / institutional pressure.** If the project takes
   institutional money, the funder will quietly request softer
   framing on the vaccine cluster. Not in writing. The mechanism:
   "we'd like to introduce you to our advisors" → advisors include
   a public-health figure → advisor's review note in some
   stakeholder meeting includes "we suggest re-examining HYP-0066's
   language" → if the founder says no, the next round is harder.
2. **Customer pressure (the inverse).** Some fraction of the paying
   customer base is in the vaccine-skeptical community and wants
   contested HARDER, not softer — i.e. wants the atlas to drop
   "contested" and call HYP-0044 confirmed. This pressure is
   structurally symmetric to (1) and equally corrosive.
3. **Practitioner-network pressure.** MAPS doctors and DAN-lineage
   practitioners who become referral partners will push for the
   atlas's wording to match their own practice norms. Those norms
   include both directions.

The principle "contested status is permanent" survives only if it
survives unanimous direction-of-flow pressure. The risk is asymmetric:
softening costs nothing in the short run but every softening is
irreversible (the curator who first dropped a contested tag on a
hypothesis has set a precedent), and the cumulative effect over six
months is a re-tiered atlas.

**Atlas's existing defenses:**

- The pipeline-gating language in CLAUDE.md ("contested = permanent")
  is strong, but it is a norm, not a code-enforced rule.
- The verification protocol (§24) is code-enforced (precommit hook).
  Contested-permanence is not.

**Atlas's missing defenses:**

- No code-enforced gate on contested-status changes. The right
  enforcement: any commit that changes a hypothesis from `contested`
  to any other status must be signed by two named maintainers AND
  must reference an external preregistered analysis plan. This is the
  same model the FDA uses for pre-specified primary endpoints —
  you don't get to change the bar mid-study.
- No quarterly contested-status audit. Without it, drift is invisible.
  The auditor for this should not be the curator (conflict of
  interest); it should be an external named reviewer.
- No published list of which hypotheses are contested at each version
  release. Without it, drift cannot be detected by readers.

---

## 8. Practitioner capture

**Probability: HIGH (≥60% within 12 months).**
**Severity: moderate but reputation-corroding.**

The report feature implies a downstream step: "discuss this with a
MAPS-trained provider." Once that handoff exists, the atlas has a
referral product. Referral products generate kickbacks, formal or
informal. The asymmetry: a small number of high-volume MAPS practices
run $3K–$8K supplement protocols with margins that depend on volume.
Three failure modes here:

1. **Direct revenue share.** Practitioner X agrees to a paid referral.
   Atlas's recommendations subtly tilt toward X's preferred
   intervention bundle. The tilt is invisible because the
   methodology is transparent — but the atlas's curator chose what to
   ingest, and that ingestion choice biases output.
2. **Soft capture.** No money changes hands, but the curator socializes
   with the practitioner community, integrates their feedback, and
   over months the atlas absorbs a specific lineage's intervention
   preferences (Walsh / Frye / Klinghardt / MAPS / ARI). Each lineage
   has a known intervention bias. The atlas already lists these
   lineages explicitly in CLAUDE.md §3.5E as "named protocols /
   providers." That listing is the absorption surface.
3. **Reputation capture.** The atlas's credibility transfers to the
   practitioner network. A practitioner with weaker evidence base
   benefits from atlas association. The first $20K supplement protocol
   with no biomarker-stratified evidence base, sold under an "atlas-
   recommended" implication, damages everyone.

**Atlas's existing defenses:**

- MIT license + open source means no exclusive partnerships.
- CLAUDE.md "What not to do" includes "Don't add fact-check journalism,
  editorial commentary, or advocacy content as primary evidence" —
  the inverse rule (don't add practitioner advocacy content) is
  implicit but not explicit.

**Atlas's missing defenses:**

- No conflict-of-interest disclosure rule for curators. If the
  curator's spouse refers parents to a particular MAPS practice, that
  needs to be in a public disclosure.
- No published "we do not accept payments from labs, supplement
  companies, or practitioner networks" position. It belongs in
  SUBSTRATE_THESIS.md right after the MIT license sentence.
- No mechanism by which the atlas could test for practitioner-network
  effect on its own recommendations. The right test: blind two
  versions of the report (one with practitioner-network-derived
  ingestion, one without) and compare. No infrastructure for that
  yet exists.

---

## 9. Lab partner capture

**Probability: MEDIUM (~40% within 12 months).**
**Severity: lower than practitioner capture, but structurally similar.**

The biomarker schema already names Quest, LabCorp, Great Plains,
Doctor's Data, DUTCH, Genova, Diagnostic Solutions, Cunningham as
preferred lab providers. The first time one of these labs offers a
formal partnership (volume discount, white-label kit, revenue share
on referred testing), the atlas's recommendation surface becomes
their distribution channel.

The capture mechanism is more direct than practitioner capture
because labs have larger marketing budgets, more sophisticated B2B
partnerships, and a clearer revenue model (per-test margin). The
asymmetry: Great Plains OAT costs a parent ~$350; lab marginal cost
is ~$50; a 10% referral fee is $35 per test; at 1,000 reports/month
that is $35K/month of unbooked revenue the atlas could "leave on the
table" — a strong gravitational pull toward booking it.

**The structural defenses are the same as #8:**

- Published "no lab partnerships" position
- Periodic counter-blind testing (would a recommendation change if we
  swapped lab attribution)
- COI disclosure for curators

The lab-capture failure mode is slower than practitioner capture
because labs operate on B2B sales cycles. The 6-month horizon is
probably too short for it to fire — but the architectural decision
("will we accept lab partnerships, ever") should be made now, not
when the first deal hits the inbox.

---

## 10. Engine drift under data growth

**Probability: MEDIUM (~30% within 6 months; ~50% over the next 18 months).**
**Severity: existential to the validation argument; partially recoverable.**

INT-0001 Leucovorin CSRS = 83.35 is the calibration anchor. The
pipeline halts if it drops below 80. The implicit claim in
DESIGN_TEAM_HANDOFF.md is that this value has not drifted across
major revisions — and that non-drift is itself part of the proof.

The atlas's history (from CLAUDE.md) shows the anchor moving:
82.72 → 81.95 → 83.65 → 83.35 across recent revisions. That is
within the ≥80 invariant. But the second-derivative of "moves
within ±1.5" implies that 10× growth in content will likely move
the anchor out of the current band, possibly below 80, at which
point the pipeline halts and someone must decide whether to:

- Re-derive the engine constants (the SOFTPLUS_ALPHA = 0.5, the
  caps, the polarity coefficients) to restore the anchor — which is
  exactly the kind of re-derivation that erodes the "no drift"
  claim,
- Lower the anchor threshold from 80 → 75 → 70 — which is the
  same erosion via a different mechanism, or
- Accept the halt and stop ingesting new content.

The deeper problem: the validation argument in slide 10
(n=8 cohort MAE = 0.067) was computed against a specific atlas
state. New content changes the engine's recommendations on the
same RCT inputs. If the recommendations shift even slightly, the
MAE shifts. Over the next 6 months, with the planned 3.5A
biomarker layer expansion (40-50 biomarkers), 3.5B intervention
expansion (~30-50 entities), 3.5C two new hypothesis families,
and 3.5D phenotype refinement, the atlas grows by ~30-40% in
content. Each tier of growth perturbs the cohort.

**Existing defenses:**

- INT-0001 ≥ 80 invariant (good — but binary; doesn't constrain
  the actual value).
- Pipeline halt on calibration failure (good).
- Determinism test (good, but tests reproducibility-of-build, not
  semantic stability).

**Missing defenses:**

- No cohort regression test. The right architecture: any change to
  the atlas state runs the full 8-cohort MAE computation as a
  pre-commit step; any change that moves MAE by more than X
  percentage points halts the commit. The number "X" should be
  small (0.01 or so) and tightening over time.
- No documented sensitivity analysis. Which specific edges drive
  the INT-0001 score? Which removals would push it below 80? An
  attack-surface map of the calibration anchor.
- No semantic-versioning of engine outputs. If the engine produces
  meaningfully different outputs for the same input, that should
  be a major-version bump, and downstream consumers (the deck, the
  HHS pitch, the report) should be pinned to a specific engine
  version.

---

## 11. Cost-of-tests barrier / equity problem

**Probability: VERY HIGH (~95% — this is already true; the question is whether it bites).**
**Severity: low operationally; high for institutional positioning.**

A full functional medicine workup is $1,500–$5,000 out of pocket.
That filters the atlas's user base to the top decile of household
income (or families with HSA/FSA access and willingness to spend).
The HHS pitch ("federal reference substrate for chronic disease
heterogeneity") implicitly claims population-scale relevance. The
report feature, in its likely form, serves a population the HHS
mission specifically does not.

This is not a six-month liability — it is a positioning gap that
becomes acute when:

- HHS evaluators ask "who is your user base," and the answer
  honestly is "wealthy autism parents in California, New York, and
  Texas."
- A journalist piece (failure mode #2) adds the equity angle to
  the anti-vaccine framing: "boutique autism testing for the
  wealthy that promotes vaccine skepticism." This is a more
  damaging frame than either component alone.
- An academic critic publishes the responder-rate calibration
  with the observation that the n=8 RCTs were predominantly
  white-middle-class participants and the recommendation engine
  is not validated on non-white-middle-class populations.

**Existing defenses:**

- MIT license means anyone can fork. Doesn't help — most
  underrepresented users won't fork.
- Substrate framing ("condition-agnostic") is genuinely broader
  than autism. Doesn't help the autism-specific equity problem.

**Missing defenses:**

- No documented sliding-scale / free-access policy for the report
  feature.
- No partnership with Medicaid managed-care providers or community
  health centers. (Building one in 6 months is plausible if started
  now; not plausible if started in 9 months.)
- No equity-of-validation analysis. The cohort.yaml RCTs need to
  be examined for participant demographics; the atlas's
  recommendation surface needs to be tested for differential
  performance across demographic subgroups. This is the same
  bioethics critique that has accumulated against polygenic risk
  scores; the atlas inherits the critique by association unless it
  preempts it.

---

## 12. Federal / academic credibility erosion under success

**Probability: MEDIUM (~30%).**
**Severity: locked in for years if it happens.**

This is the inverse risk to #2 (anti-vaccine framing). If the HHS
deck succeeds — even partially — and federal money flows in, the
atlas's mainstream credibility increases. That is the point. The
risk: post-funding, the atlas drifts into "wellness app with HHS
imprimatur" framing because the commercial incentives push that
direction. Federal funders observe the drift and quietly disengage.
The reputational damage from "HHS funded this and walked away" is
worse than the damage from "HHS never funded it."

The drift vectors:

1. The atlas explorer becomes a consumer surface (it currently
   isn't — it's an institutional surface, per DESIGN_TEAM_HANDOFF.md
   §1's Palantir × CERN × Arc Institute brief). Once it serves the
   report feature, the visual register collapses.
2. The two-brand-surface discipline (institutional vs. cinematic)
   in CLAUDE.md is correct, but it survives only if the founder
   maintains it. A second hire (designer / marketer) who has not
   internalized the dual-surface discipline will collapse them.
3. The HHS / federal partnership generates a press release. The
   press release language is written by HHS comms staff. Their
   default voice is consumer-public-health. That voice
   contaminates the institutional surface.

**Existing defenses:**

- The two-brand-surface discipline is well-articulated in
  CLAUDE.md.
- DESIGN_TEAM_HANDOFF.md §4's language guardrails are explicit
  ("no 'deterministic' in public copy," "no emojis," "no
  marketing voice").

**Missing defenses:**

- No formal brand-discipline checklist before any
  press / partnership / public release. The right artifact: a
  one-page "before this goes out" review that explicitly maps the
  comms artifact to one of the two surfaces and gates merge on
  surface-discipline match.
- No founder-only veto on public-facing copy. Once a hire is
  empowered to publish, the discipline erodes by attrition.
- No "what we do not become" annual statement. The atlas's
  positioning needs an active negative: "the atlas is not, and
  will not become, X." Including: not a wellness brand, not a
  testing-kit vendor, not a practitioner-referral business, not a
  consumer telehealth surface.

---

## 13. Competitive moats — what stops a fast follower

**Probability of fast-follower entry: VERY HIGH (≥80% within 12 months).**
**Severity: depends entirely on the moat structure.**

Strategene, NutraHacker, MaxGen, IntellxxDNA, and several VC-backed
biotechs already operate adjacent to this space. None of them have the
atlas's epistemic discipline. All of them have more capital and more
go-to-market polish. A well-funded entrant could clone the surface
features (genetic upload → personalized report) in 9–12 months.

The atlas's actual moats, in order of robustness:

1. **The atlas itself — 1,420 PMID-verified primary sources, 95
   hypotheses, 295 nodes — and the verification discipline behind
   them.** This is the strongest moat, and it is methodological, not
   technical. A competitor can build a 295-node graph in a quarter;
   they cannot replicate "every PMID verified against PubMed
   esummary, with a precommit hook enforcing it" in a quarter. They
   will fabricate; their reports will contain hallucinated
   citations; in a year their credibility will collapse the moment
   anyone audits.
2. **The Hannah Poling P × E → M → Φ schema as a structural
   commitment.** Competitors will offer population-average framing
   because it is easier to market. The atlas's explicit
   individual-conditional framing is a positioning moat. But it is
   easy for a competitor to claim the same positioning without
   actually implementing the math.
3. **The two-layer architecture (Layer 1 causal graph + Layer 2
   CSRS scoring with deterministic engine).** This is a real
   technical asset. A competitor that ships a marketing-friendly
   version without the determinism property will look more polished
   and produce wrong-but-confident answers. The atlas's
   "reproducible lineage" claim has technical substance behind it.
4. **The contested-status discipline.** Hardest for competitors to
   replicate because it requires accepting commercial pressure
   without yielding. Most VC-backed competitors will yield.
5. **The cohort validation (n=8 RCTs MAE = 0.067).** This is the
   weakest moat because the cohort is published RCTs that anyone
   can use. Validation as a method is replicable. The atlas's
   number is currently the only such published number for an autism
   intervention recommender — but a competitor with $5M can buy a
   biostatistician and publish a competing number in 4-6 months.

**What does NOT moat:**

- Brand. The atlas does not yet have a public name. Whoever launches
  first with a polished consumer brand wins the brand race.
- Network effects. The atlas has no network effects in the current
  architecture; it is a database + engine, not a marketplace.
- Data scale. The atlas's data is published primary literature, which
  is public. The atlas's curation is the moat, not the data.
- Hannah Poling framing. It is a quotable framing, not a defensible
  IP position. A competitor can adopt the phrase tomorrow.

**The real strategic question:** is the atlas's moat one that
matters to the target buyer (HHS / NIH / academic medical centers) or
to the consumer (autism parents)? For HHS, the methodology moat is
strong — they will audit, and the audit will pass. For autism
parents, the methodology moat is invisible; they will compare reports
side-by-side and pick whichever looks more polished. The atlas's
positioning needs to choose: HHS-grade methodology (moat is strong;
TAM is narrow) or consumer-grade product (moat is weak; TAM is large).
Trying to be both yields the worst of each.

---

# Top 3 things to do in next 30 days

These are not "improvements." These are the three actions that change
the probability distribution on the failure modes above. Ranked by
expected leverage on the highest-probability + highest-severity
failures.

## 1. Insert a structural clinician layer between the report and the parent

**Addresses: failure modes 1, 5, 6 (the trio that fires together).**

Decide now whether the report feature will be (a) "you receive a PDF
report" or (b) "you book a telehealth consult with a licensed
clinician who reviews the atlas-generated draft and signs off on the
recommendations before they reach you." (b) is the only architecture
that survives the first liability event.

This is not a future feature. This is a present-tense architectural
choice. If the answer is (a), every other failure mode hardens by
2–3x. If the answer is (b), the cost is high (clinician network
build, state-by-state licensing, malpractice insurance) but the
probability-weighted catastrophe shrinks dramatically. Recommendation:
do not ship (a) under any framing.

Concrete actions:

- Identify 3–5 MAPS / functional-medicine pediatricians who would
  serve as clinician-of-record for the report layer. Begin
  conversations this week.
- Stand up a state-by-state telehealth-licensing analysis. The 3–5
  largest autism-population states (CA, TX, FL, NY, PA) cover the
  bulk of demand.
- Draft a malpractice-insurance term sheet. Even a $1M/$3M policy
  on the clinician-of-record entity is order-of-magnitude
  protective.
- In SUBSTRATE_THESIS.md add an explicit "what the report is and
  is not" section. "The report is a clinician-supervised draft;
  the clinician of record is the named signatory; no recommendation
  reaches a parent without clinician review." This text appears
  before any other description of the report.

## 2. Code-enforce the firewall between published evidence and parent-submitted outcomes

**Addresses: failure mode 3 (MAE collapse, the existential threat to the validation argument).**

The atlas's 0.049 MAE / 0.067 cohort MAE / 83.35 calibration anchor
are the strongest evidence in the deck. They survive only if the
ingestion path is structurally incapable of ingesting parent-
submitted outcome data into the scoring engine state.

Concrete actions:

- Add a binding rule to CLAUDE.md §24 (or as §25): "parent-submitted
  outcome data is never ingested into the scoring engine. The
  cohort.yaml file is computed only from published RCTs. Any commit
  touching cohort.yaml without a corresponding PubMed-verified RCT
  citation fails the precommit hook."
- Implement the precommit hook this week. Mirror the existing
  `scripts/precommit_pmid_verify.py` pattern.
- Stand up a separate outcomes-ledger schema (`field_outcomes.csv`)
  that has its own ID space, its own scoring semantics (no
  contribution to CSRS), and an explicit "this is selection-biased
  observational data; do not use for calibration" header. This
  separation is the firewall.
- Mark the n=8 cohort MAE computation as a fixed reference artifact
  with a date stamp and a hash of the contributing inputs. Future
  runs of `scripts/compute_responder_mae.py` should write to a
  versioned output, not overwrite the existing one.

## 3. Stand up the press / journalism response infrastructure before the first inquiry

**Addresses: failure modes 2, 5, 12 (the reputational triad).**

The first hostile inquiry will arrive within weeks of the first
public visibility milestone (the HHS deck, the explorer going viral
on X, the report feature launch — any of these). Plan for it now.

Concrete actions:

- Write the one-page "atlas position on vaccines" public document.
  Three sentences each on: (a) the methodology, (b) the
  population-average vs. individual-conditional distinction, and
  (c) what the atlas does and does not claim. This is harder than
  it sounds. Draft three iterations.
- Recruit a named medical advisory board, prioritizing one
  pediatric-immunology figure with public-mainstream credibility
  and one functional-medicine clinician with autism-community
  credibility. The composition itself is the message: the atlas
  spans both worlds with named accountable people.
- Audit the source list for any citation of retracted papers,
  Wakefield 1998 specifically, and any cited author whose name
  alone would headline a hostile piece. Confirm each citation is
  the retraction notice or a methodological critique, not the
  retracted claim itself.
- Identify and brief 2–3 sympathetic journalists who have written
  carefully about heterogeneous-causation autism research. The
  first call from a journalist is much better if the journalist is
  one you've spoken with first.
- Pre-write the "in response to today's reporting" statement and
  keep it in a `RESPONSE_KIT.md` (not checked into the public
  repo). Update it monthly.

---

# Coda

The atlas's methodological discipline is real. The verification
protocol (CLAUDE.md §24, post-BioMysteryBench), the determinism rule,
the contested-permanence rule, the tier-weighted scoring — these are
the right rules and they are unusual for a project of this size.

The atlas's positioning discipline is also real. The two-brand-surface
analysis, the substrate-not-application framing, the
individual-conditional epistemic argument — these are also unusual
and correct.

The atlas's commercial readiness is not real yet. The functional
medicine report feature, as planned, exposes the project to risks
that the methodology cannot defend against — because the risks are
liability, journalism, regulation, capture, and drift, not
methodology. Those are operational risks. They require operational
infrastructure (clinician layer, code-enforced firewalls, press
response, COI disclosure, contested-permanence enforcement) that
does not yet exist.

Six months from now, the most likely failure is some combination of
(1) a child reaction → (5) viral attribution → (2) journalism framing
→ erosion of (12) federal credibility. That sequence is a 30–40%
probability event over the 6-month horizon if the report ships in
its likely form without the clinician layer.

The good news: each of the three top-30-day actions reduces the
probability of that sequence by a meaningful factor. The atlas is at
the point where strategic discipline is going to determine survival,
not methodological discipline. The methodology is done; the strategy
is the open work.

---

*Reviewer note: this document was produced as an independent skeptical
review per Greg's request. It is not balanced and is not intended to
be — the request was "why this would fail," and the analysis above is
calibrated against that question. Items omitted that would balance the
picture: the atlas's substrate-framing strengths under HHS adoption,
the rigor of the verification protocol relative to peer projects, the
quality of the Hannah Poling framework as an epistemic primitive,
the unusual coherence of the two-brand-surface discipline. Those
strengths are real. They are also not what this document is for.*
