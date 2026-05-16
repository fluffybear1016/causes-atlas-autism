---
title: "How to bill the workup — a strategy guide for autism families and their clinicians"
status: draft v0.1 — 2026-05-16
companion_csv: v2.0_scored/billing_codes.csv
audience: high-agency parent + the clinician she's working with
---

# Executive summary

The functional-medicine workup for autism is real medicine. It is also, on
paper, a labyrinth of cash-pay specialty labs, off-label prescriptions,
and supplements that the IRS classifies as "general health." Most of the
public-facing material tells you, falsely, that none of this is billable.
The truth is more nuanced, and the nuances matter.

This guide collapses the work of mapping every test and high-volume
intervention in the curated bioKids/Causes Atlas list against current
US payer policy (CMS, BCBS, UHC, Aetna, Cigna), the IRS HSA/FSA rules,
and the lab/pharmacy direct-pay rate cards. The companion CSV
(`v2.0_scored/billing_codes.csv`) contains the structured codes; this
document is the strategy.

Three claims worth printing on a card and handing to your pediatrician:

1. **Genetic tests are mostly insurance-covered when ordered correctly.**
   Chromosomal microarray, Fragile X, whole exome sequencing — these are
   ACMG-recommended first-tier tests for autism / unexplained
   developmental delay. The denial rate is low when the order carries
   F84.0 (autism), F70-F79 (ID), or F80-F89 (DD/communication) ICD-10
   anchors plus documentation that prior workup was unrevealing.
2. **Functional-medicine specialty labs are mostly cash-pay.** Mosaic
   OAT, GI-MAP, Cunningham Panel, FRAT, Doctor's Data methylation, IntellxxDNA,
   Quadrant Clarifi — none are covered by any commercial plan as of
   2026. About half of Cunningham Panel orders get partial
   reimbursement when patients self-submit superbills; the rest of
   these labs almost never reimburse.
3. **HSA/FSA is materially better than insurance for FM autism care
   in most households.** Insurance covers ~30-40% of the FM workup
   cost across the full curated list at the household level (mostly
   the genetics + standard labs). HSA/FSA, with proper Letters of
   Medical Necessity, covers ~75-85% of the FM workup cost at full
   marginal-tax savings (effectively 22-37% off depending on bracket).
   The two stack — use insurance where it works, HSA/FSA where it
   doesn't.

The single biggest billing hack for autism families: **order the
genetic workup first, document a diagnosis, then use that diagnosis to
unlock everything downstream** — biomarker-deficiency labs, formulated
prescriptions, and HSA/FSA LMN coverage for supplements and equipment.

---

# The three billing paths

Every test and intervention in the atlas falls into one of three
financial paths. Knowing which path a given item lives on tells you
who to ask, what to document, and where to expect denial.

## Path 1 — Insurance-friendly (covered under autism Dx, F84.0)

Items that are covered by most commercial plans, Medicare, and
Medicaid when billed correctly with appropriate ICD-10 anchors. This
is where you start.

**Genetic / cytogenetic:**

- **Chromosomal microarray (TEST-0007)** — CPT 81229. ACMG first-tier;
  covered for any unexplained DD/ID/ASD. Yield is ~15-20% of cases.
  Single denials are rare; appeal points to ACMG technical standards.
- **Fragile X PCR + reflex methylation (TEST-0008)** — CPT 81243
  (and 81244 if reflex). Covered for unexplained ID/DD/ASD, especially
  boys with macrocephaly + intellectual deficit. ~$200-400 if it
  weren't covered.
- **Whole exome sequencing (TEST-0009)** — CPT 81415 (proband) + 81416
  (each comparator, up to 2). Prior auth required; coverage post-2020
  improved substantially. Trio sequencing preferred. AAP first-line
  recommendation for unexplained DD/ID. If CMA + FXS are negative,
  most plans approve.

**Standard clinical labs:**

- **CBC + CMP + lipid panel (TEST-0046)** — CPT 80053 + 85025 + 80061.
  Annual well-child CMP is covered $0 copay under the ACA preventive-
  care mandate. Add-on testing on the same encounter under a
  diagnostic ICD-10 is covered as diagnostic, not preventive.
- **Plasma lactate / pyruvate / L:P ratio (TEST-0015)** — CPT 83605 +
  84210. Cover with G93.41 metabolic encephalopathy, E88.40
  mitochondrial disease unspecified, E87.2 acidosis. Pre-analytical
  handling matters: deproteinize lactate within minutes or values
  spike.
- **Acylcarnitine profile (TEST-0016)** — CPT 82017. Cover with
  E71.30 fatty acid oxidation defect or E88.40 mito.
- **Plasma amino acids (TEST-0018)** — CPT 82139. Cover with E72.9
  amino acid disorder unspecified or R62.51 failure to thrive.
- **Plasma copper + zinc + ceruloplasmin (TEST-0042)** — Standard
  Quest/LabCorp orders; ~$80-200 covered with autism dx (F84.0)
  plus PHE-0011 / Walsh-overload screening rationale.
- **Comprehensive thyroid panel (TEST-0044)** — Cover with autism +
  family hx autoimmune thyroid; full panel including anti-TPO +
  anti-Tg + reverse T3 is the FM-grade order.
- **Ferritin + iron panel (TEST-0045)** — Cheap, covered, often
  overlooked. Low ferritin is a real driver in autism + RLS / sleep
  / behavior.
- **Vitamin D 25-OH (TEST-0043)** — CPT 82306. Covered first-time
  under E55.9 (deficiency screen) for at-risk patient; thereafter
  cover under documented deficiency.

**FDA-approved drugs for autism / TSC indications:**

- **Aripiprazole (INT-0141)** — Generic Tier 1-2; FDA-approved for
  irritability associated with autistic disorder ages 6-17. No prior
  auth needed for label indication. Single most-reliably covered
  drug in the atlas for autism.
- **Risperidone (INT-0142)** — Also FDA-approved for autism
  irritability; same coverage posture as aripiprazole.
- **Sirolimus (INT-0036)** — Generic covered for TSC with Q85.1
  diagnosis; off-label for autism without TSC is denied universally.
- **Leucovorin (INT-0001)** — Generic widely covered Tier 1-2. The
  2025 FDA label expansion adding cerebral folate deficiency (E53.8)
  triggers mandatory Medicaid coverage. For autism specifically, the
  cleanest order is "leucovorin 25mg PO daily for cerebral folate
  deficiency E53.8" not "leucovorin for autism F84.0" — same drug,
  approved indication unlocks coverage.

**Strategic note:** The above items are roughly 30-40% of the cost of
a full FM autism workup at retail. If you do nothing else, get these.

## Path 2 — HSA / FSA eligible (with LMN)

Items that no commercial plan covers, but that HSA/FSA accounts
reimburse with a Letter of Medical Necessity. Use this path for the
specialty labs, compounded prescriptions, supplements, and equipment.

**Letter of Medical Necessity (LMN) template:**

The LMN must include patient name + DOB, the diagnosis with ICD-10
code, a 2-4 sentence medical necessity statement, the specific
recommendation (item or service), duration of recommendation, and the
licensed clinician's signature with credentials and date.

The IRS standard is the "but-for" test: would you have purchased this
but for the diagnosed condition? If yes, it's HSA/FSA eligible. If
no (general wellness), it isn't.

**Specialty lab tests via HSA/FSA:**

- **Mosaic OAT (TEST-0010)** — $299-399 cash. HSA/FSA covers as
  diagnostic test. Mosaic provides superbill; rare commercial
  reimbursement.
- **Doctor's Data methylation profile (TEST-0012)** — $180-300.
  HSA/FSA covers. Insurance reimbursement via superbill is
  unpredictable.
- **GI-MAP (TEST-0025)** — $359-500. HSA/FSA covers. Diagnostic
  Solutions is OON with all plans; superbill submitted by patient.
- **Cunningham Panel (TEST-0020)** — $995. HSA/FSA covers.
  Moleculera attempts insurance billing on first round; ~50% partial
  reimbursement rate; patient pays $495 deposit upfront.
- **FRAT test (TEST-0014)** — $295-595. HSA/FSA covers. Never
  insurance-reimbursed; cash-pay only.
- **Quadrant Clarifi ASD (TEST-0090)** — $989. HSA/FSA covers.
  No insurance coverage as of 2026 despite FDA Breakthrough Device.
- **IntellxxDNA (TEST-0006)** — $500-1500. HSA/FSA covers with LMN.
  Practitioner-only; never insurance-billable.
- **TruDiagnostic TruAge / DunedinPACE (TEST-0089)** — $229-499.
  HSA/FSA covers. No CPT code, no insurance path.
- **23andMe Health (TEST-0001)** — $99-199. Up to $174 HSA/FSA
  reimbursable per IRS ruling for health-only kits. Ancestry-only
  kits NOT eligible.

**Compounded prescriptions via HSA/FSA:**

- **Methyl-B12 injections (INT-0003)** — $30-150/month at compounding
  pharmacy. HSA/FSA covers the cash cost. Insurance covers J3420
  cyanocobalamin only; methylcobalamin specifically usually requires
  cash + HSA.
- **LDN (INT-0006)** — $30-80/month at compounding pharmacy.
  HSA/FSA covers. Insurance almost never covers compounded LDN.
- **Compounded liquid leucovorin** — for kids who can't swallow
  tablets, $40-150/month. Pill form is insurance-covered; compounded
  liquid usually isn't but HSA/FSA covers.
- **Intranasal oxytocin (INT-0061)** — $150-300/month. HSA/FSA covers.
  Note: SOARS-B 2021 NEJM null result has further weakened any
  insurance argument; OOP is now the only realistic path.

**Supplements via HSA/FSA + LMN:**

- **Omega-3 EPA + DHA (INT-0014)** — $15-80/month
- **Vitamin D3 (INT-0013)** — $5-30/month; requires documented
  deficiency labs first
- **Magnesium glycinate (INT-0015)** — $8-30/month
- **Sulforaphane (INT-0002)** — $30-60/month for Avmacol or
  equivalent
- **Methyl-B12 sublingual (INT-0008)** — $15-40/month
- **CoQ10 / ubiquinol (INT-0011)** — $30-80/month
- **L-carnitine (INT-0012)** — $20-60/month

All require LMN. The IRS "but-for" test is the operative standard;
the clinician's documentation that "this supplement is being used to
treat the patient's diagnosed autism / mitochondrial dysfunction /
methylation defect / GI dysbiosis" makes the difference.

**Equipment + therapy via HSA/FSA + LMN:**

- **Infrared sauna (INT-0048)** — $1500-5000 for home unit. HSA/FSA
  covers with LMN citing chronic pain, autonomic dysregulation, or
  mold-related illness. This is the single biggest HSA/FSA play in
  the FM toolkit — the hardware amortizes over years.
- **HBOT chamber** — soft-shell home units $4500-10,000; HSA/FSA
  covers with LMN.
- **Methylation-friendly water filter / air purifier** — partial
  HSA/FSA coverage with LMN for documented mold or chemical sensitivity.

**Diet via HSA/FSA (limited):**

- **Gluten-free items (INT-0041)** — Only the incremental cost above
  standard equivalents is reimbursable, and only with celiac disease
  (K90.0) or wheat allergy (Z91.012) documented. Casein-free has no
  IRS recognition. The receipt-tracking burden is high; most families
  don't bother with this one.

## Path 3 — Cash-pay only

Items where neither insurance nor HSA/FSA reliably work. Counsel
families honestly that these are OOP.

- **FMT (INT-0076)** — investigational for autism; clinical trial
  enrollment only. Cash-pay clinics offshore $15,000-40,000.
- **Stem cell therapy** — investigational; clinical trial or offshore
  cash-pay.
- **Hyperbaric oxygen at clinic** (vs home unit which is HSA-eligible)
  — $80-150 per session; some clinics accept HSA/FSA per visit but
  most don't.
- **Most contested heavy metal protocols** — DMSA challenge testing,
  chelation outside FDA-approved indications, etc.

---

# Specific test-by-test playbook (for the pediatrician)

For each curated test, the line for the clinician to say to insurance.

| Test | Order this way | If denied, appeal point |
|---|---|---|
| TEST-0007 CMA | CPT 81229, ICD-10 F84.0 or F70-F79 (whichever is established). State "ACMG first-tier test for unexplained ASD/DD; prior workup unrevealing." | Cite ACMG 2013 Technical Standards; appeal at first-level review. Approval rate post-appeal is >90%. |
| TEST-0008 Fragile X | CPT 81243 (PCR) +/- 81244 (reflex methylation). ICD-10 F84.0 + male sex + macrocephaly if applicable. | Standard of care; denial is unusual. Cite AAP autism workup guidelines. |
| TEST-0009 WES | CPT 81415 + 81416 x2 (trio). Submit prior auth with documented negative CMA + Fragile X + clinical findings (regression, dysmorphism, multi-system involvement). | Peer-to-peer with medical director citing GeneDx published yield data and AAP first-line recommendation. |
| TEST-0014 FRAT | Cash-pay. Bill clinician E/M (99213/99214) separately for ordering + interpretation. | No appeal path. Document responder rationale in chart for downstream leucovorin coverage. |
| TEST-0015 Lactate/pyruvate | CPT 83605 + 84210 with G93.41 metabolic encephalopathy or E88.40 mito. Pair with acylcarnitine 82017. | Pre-analytical handling failures cause re-orders, not denials. |
| TEST-0010 OAT | Cash-pay through Mosaic. Patient self-submits superbill for rare partial reimbursement. | Genova Organix Comprehensive (TEST-0011) has insurance-billable option at $179 copay through Genova-Connect. |
| TEST-0020 Cunningham | $495 deposit + Moleculera-attempted insurance billing. ICD-10 anchor strongest as F95.x acute tic disorder + G93.41 + recent strep. | When Aetna denies "experimental," ~50% of patients get partial commercial reimbursement on appeal with peer-to-peer. |
| TEST-0090 Clarifi | Cash-pay $989. No insurance path. | No appeal. |
| TEST-0012 DD methylation | Cash-pay $180-300. Alternative: Quest/LabCorp homocysteine (83090) + MMA (83921) + plasma B12 (82607) + RBC folate (82747) for $40-200, insurance-covered. | 90% of clinical signal at full insurance coverage via the Quest path. |
| TEST-0089 TruAge | Cash-pay $229-499. HSA/FSA only. | No appeal. |
| TEST-0006 IntellxxDNA | Cash-pay through practitioner $500-1500. | No appeal. |
| TEST-0016 Mayo ACRN | CPT 82017 with E71.30 or E88.40. Order alongside lactate/pyruvate + carnitine. | Standard order; denial rare with mito ICD-10. |
| TEST-0025 GI-MAP | Cash-pay through DSL with superbill. Strong LMN citing K59.x chronic GI + suspected dysbiosis. | Quest GI Pathogen Panel PCR (CPT 87507) is insurance-covered at $150-300 with K59 / R19 / K90 ICD-10 — covers ~30% of GI-MAP markers. |
| TEST-0018 Plasma AA | CPT 82139 with E72.9 or R62.51. Pair with newborn metabolic screen retrieval. | Standard order; denial rare with E70-E72 ICD-10. |
| TEST-0001 23andMe | Cash-pay $99-199. Use health-only kit (not ancestry-only) for HSA/FSA eligibility. | No appeal; up to $174 HSA/FSA reimbursable per 2019 IRS ruling. |
| TEST-0005 StrateGene | Cash-pay $75-150. Software-only product. HSA/FSA eligible with LMN. | No appeal. |
| TEST-0046 CBC+CMP+lipid | Standard preventive lab + diagnostic add-ons. ACA-mandated $0 annual CMP. | Denial extremely rare. |
| TEST-0043 Vit D | CPT 82306 with E55.9 first time, repeat under documented deficiency. | Routine screening (Z13.220) denied by Medicare; document deficiency to unlock retest coverage. |
| TEST-0112 Biomesight | Cash-pay $99-149. HSA/FSA eligibility ambiguous; LMN improves odds. | No appeal. |

---

# Why prescription insurance is different (and harder)

Lab testing has a clean billing logic: one CPT code, one ICD-10
anchor, one payer policy. Prescriptions are messier because of three
overlapping layers:

1. **Formulary tier.** Each commercial plan has 4-5 tiers. Tier 1
   generic, Tier 2 preferred brand, Tier 3 non-preferred, Tier 4
   specialty, Tier 5 self-pay (excluded). A drug's tier dictates
   copay AND whether prior authorization is required.
2. **Prior authorization (PA).** For Tier 3-4 drugs and for off-label
   indications of Tier 1-2 drugs, the prescriber must submit clinical
   justification before the prescription will be filled. PA approval
   typically requires (a) the FDA-labeled indication OR (b) failed
   first-line alternatives OR (c) compendia support (USP DI, AHFS,
   DRUGDEX) for off-label use.
3. **Peer-to-peer review.** When PA is denied, the prescriber can
   request a peer-to-peer call with the plan's medical director.
   ~50% of initial denials get overturned at peer-to-peer; this is
   the single highest-yield intervention a parent can ask their
   clinician to do.

**Off-label coverage strategies that actually work:**

- **Document FDA-labeled indication first.** Aripiprazole IS FDA-
  labeled for autism irritability. Leucovorin IS FDA-labeled for
  cerebral folate deficiency. Sirolimus IS FDA-labeled for TSC.
  If your child meets the labeled indication, prescribe under it.
  The autism F84.0 diagnosis is incidental to the prescribing
  ICD-10.

- **Compendia citation.** USP DI, AHFS Drug Information, and DRUGDEX
  recognize many off-label uses. CMS and most commercial plans defer
  to these compendia for off-label coverage decisions. For methyl-B12
  in autism: AHFS recognizes cobalamin deficiency states broadly,
  which the prescriber can cite.

- **Step therapy documentation.** If a Tier 3-4 drug requires "failure
  of first-line alternatives" before approval, the chart must show
  documentation of those failures. For LDN: document failure of
  standard sleep medications, anxiolytics, or pain modulators (as
  applicable to the indication being treated).

- **Single-case agreement (SCA).** For unusual situations where
  standard PA paths don't fit, the prescriber can request an SCA
  from the plan. SCAs are individualized contracts and require
  detailed clinical justification. Most useful for compounded
  medications and specialty pharmacy access.

- **Peer-to-peer with named-physician backup.** When peer-to-peer is
  requested, the most successful clinicians come prepared with two
  things: (1) primary literature supporting the indication; (2) the
  name of a peer specialist (board-certified pediatric immunologist,
  geneticist, integrative medicine specialist) who endorses the
  protocol. The plan medical director defaults to specialist authority.

**Drugs in the curated list and their realistic coverage posture:**

| Drug | FDA label | Coverage for autism use | Realistic OOP |
|---|---|---|---|
| Aripiprazole (INT-0141) | Autism irritability 6-17 | Always covered | $5-50/mo generic |
| Risperidone (INT-0142) | Autism irritability 5-16 | Always covered | $10-40/mo generic |
| Leucovorin (INT-0001) | Cerebral folate deficiency (2025) | Usually covered under E53.8 | $9-36/mo tablets; $40-150 compounded liquid |
| Sirolimus (INT-0036) | TSC, transplant | Covered with Q85.1; denied without TSC | $50/mo generic with TSC; $400-800 brand |
| Methyl-B12 injection (INT-0003) | B12 deficiency | Sometimes covered with E53.8 documented deficiency | $30-150/mo compounded |
| LDN (INT-0006) | Naltrexone for opioid/alcohol UD | Almost never covered | $30-80/mo compounded |
| IVIG (INT-0143) | Primary immune deficiency | Covered with D80.x documented | $5,000-20,000/cycle |
| Intranasal oxytocin (INT-0061) | None in US | Never covered | $150-300/mo compounded |
| Slenyto-equivalent melatonin (INT-0046) | EU/UK only | Never covered in US | $30-80/mo compounded |
| Bumetanide (INT-0005) | Loop diuretic for edema | Off-label autism never covered | $10-30/mo generic; titrate carefully |

---

# Common denial reasons and how to respond

Five denial patterns account for the majority of FM-workup denials:

**1. "Experimental / investigational" denial.**
Used by Aetna for Cunningham Panel; UHC and BCBS for some pediatric
WES indications; most plans for compounded LDN and intranasal
oxytocin.

Response: cite peer-reviewed published evidence supporting the
specific indication; request peer-to-peer review; if denied at
peer-to-peer, file external review per state insurance commissioner
process. Some states (CA, NY, MA) have strong external review
provisions for pediatric specialty care.

**2. "Not medically necessary" denial.**
Used for off-label uses, redundant testing, and tests with weak
ICD-10 anchoring.

Response: re-order with stronger ICD-10 documentation. If the
clinical question is mitochondrial dysfunction, F84.0 alone isn't
enough — add E88.40 or G93.41. If methylation, add E53.8 or D52.1.
Build the medical-necessity case in the chart note before submitting.

**3. "Out-of-network lab" denial.**
Most FM specialty labs (Mosaic, Diagnostic Solutions, Moleculera,
Doctor's Data, IntellxxDNA, Quadrant) are OON with all commercial
plans.

Response: patient self-submits the superbill (HCFA-1500 form
generated by the lab) to their insurer with diagnosis codes filled
in. Reimbursement rate is 10-30% typically; some plans give nothing.
Document the attempt for HSA/FSA fallback path. Do NOT pay the lab
twice; if the patient self-submits and gets reimbursed, the
reimbursement goes to the patient because the patient paid the lab
directly upfront.

**4. "Compounded medication not covered" denial.**
Standard for LDN, methyl-B12, intranasal oxytocin, compounded liquid
leucovorin.

Response: this is mostly a hard "no" from insurance. The path is
HSA/FSA cash-pay through a compounding pharmacy that explicitly
accepts HSA/FSA cards (Empower, Belmar, ParkAve, Skip's, Hopewell).

**5. "Prior authorization required" denial.**
For Tier 3-4 drugs, off-label uses, and high-cost specialty drugs
(IVIG, sirolimus, biologics).

Response: prescriber submits PA with clinical documentation. If
denied, request peer-to-peer. For IVIG specifically, document
hypogammaglobulinemia or IgG subclass deficiency in workup — without
measured immune deficiency, no plan will approve.

---

# The HSA/FSA strategy in depth

For a family with available pre-tax dollars, HSA/FSA is the single
most cost-effective vehicle for FM autism care. Worked example:

A family with a 32% marginal federal tax rate plus 5% state tax pays
~37 cents on every after-tax dollar. Spending $5,000 of after-tax
income on FM care costs ~$7,937 of pre-tax income. Spending $5,000
through HSA/FSA costs exactly $5,000 of pre-tax income — a savings
of $2,937 (37%) per $5,000 spent.

**Annual HSA/FSA contribution limits (2026):**

- FSA: $3,300 individual
- HSA: $4,300 individual / $8,550 family
- HSA carries year over year, FSA largely use-it-or-lose-it (most
  plans have $640 carryover or 2.5-month grace period)

**Items that almost certainly qualify with LMN (high confidence):**

- Specialty diagnostic tests
- Compounded prescriptions
- Sauna, HBOT chamber, light therapy equipment (with LMN)
- Magnesium, omega-3, vitamin D (with documented deficiency labs)
- 23andMe health-only kit

**Items where HSA/FSA administrator interpretation varies:**

- Probiotic supplements
- "Adaptogenic" herbal supplements (ashwagandha, etc.)
- Specific bioidentical compounded creams
- Functional medicine practitioner consult fees (most do NOT accept,
  but a growing minority do via HSA card directly)

**LMN best practices:**

1. The LMN must be dated BEFORE the purchase, not after.
2. The LMN should be specific to the item, not blanket "all
   supplements for autism."
3. The LMN should include duration of recommendation (commonly 12
   months, then re-issue).
4. Keep the receipt and the LMN paired in your records for at least
   3 years (IRS audit window).
5. Services like Truemed, Real Foods Health Coach, and similar
   provide LMN-issuance workflows that integrate with HSA card
   payment processing.

---

# A worked example: total cost breakdown

A representative family doing the high-leverage curated workup:

| Item | Retail | Insurance covers | HSA/FSA covers cash portion | Net OOP |
|---|---|---|---|---|
| 23andMe Health | $129 | $0 | $129 (up to $174) | $0 net (HSA) |
| StrateGene | $75 | $0 | $75 (LMN) | $0 net (HSA) |
| Chromosomal microarray | $1500 | $1500 | n/a | $0 |
| Fragile X | $400 | $400 | n/a | $0 |
| Whole exome trio | $4500 | $4200 | $300 (with LMN) | $0 net |
| CBC+CMP+lipid | $80 | $80 | n/a | $0 |
| Vitamin D 25-OH | $80 | $80 | n/a | $0 |
| Lactate / pyruvate | $150 | $150 | n/a | $0 |
| Acylcarnitine profile | $300 | $300 | n/a | $0 |
| Plasma amino acids | $250 | $250 | n/a | $0 |
| FRAT test | $595 | $0 | $595 (LMN) | $0 net (HSA) |
| Mosaic OAT | $399 | $0 | $399 (LMN) | $0 net (HSA) |
| GI-MAP | $400 | $0 | $400 (LMN) | $0 net (HSA) |
| Doctor's Data methylation | $250 | $0 | $250 (LMN) | $0 net (HSA) |
| Aripiprazole or risperidone (if indicated) | $30/mo | $25/mo | $5/mo | $5/mo copay |
| Leucovorin (tablets) | $36/mo | $30/mo | $6/mo | $6/mo copay |
| Methyl-B12 compounded | $80/mo | $0 | $80/mo (LMN) | $0 (HSA) |
| LDN compounded | $50/mo | $0 | $50/mo (LMN) | $0 (HSA) |
| Omega-3 | $40/mo | $0 | $40/mo (LMN) | $0 (HSA) |
| Vitamin D3 | $15/mo | $0 | $15/mo (LMN, deficiency-documented) | $0 (HSA) |
| Sulforaphane | $50/mo | $0 | $50/mo (LMN) | $0 (HSA) |
| Magnesium glycinate | $20/mo | $0 | $20/mo (LMN) | $0 (HSA) |
| **One-time test bundle** | **$9,108** | **$6,960** | **$2,148** | **$0 net** |
| **Monthly prescription/supplement** | **~$320/mo** | **~$55/mo** | **~$261/mo** | **~$11/mo copay** |

**Total annual** (one-time tests + 12 months of ongoing care):
~$12,948 retail; ~$7,620 covered by insurance; ~$5,280 covered by
HSA/FSA pre-tax; ~$130/year net OOP for the family with HSA capacity.

A family WITHOUT HSA/FSA capacity has ~$5,280/year net OOP — still
better than the $12,948 retail figure but materially worse than the
HSA-enabled family.

This is why HSA/FSA matters. The functional medicine autism workup
is theoretically expensive; in practice, with insurance + HSA/FSA
+ LMN, the marginal cost to a high-income household is ~$130/year.

---

# What to do if you have neither HSA/FSA nor strong insurance

For Medicaid-only or no-HSA families, the curated workup is realistic
but more constrained:

1. **Maximize insurance-covered items.** Chromosomal microarray,
   Fragile X, WES, CBC/CMP, lactate, acylcarnitine, amino acids,
   thyroid, ferritin, vitamin D, copper/zinc. These cover ~$3,800
   of the workup at $0-50 copay across the board.

2. **Use insurance-covered drugs first.** Aripiprazole, risperidone,
   leucovorin (under cerebral folate dx), B12 deficiency injection
   (cyanocobalamin under documented deficiency).

3. **Skip the high-cost specialty labs that have insurance-billable
   alternatives.** Use Quest homocysteine + MMA + plasma B12 + RBC
   folate ($40-200, insurance-covered) instead of Doctor's Data
   methylation ($180-300, cash). Use Quest GI Pathogen Panel
   ($150-300, insurance-covered) instead of GI-MAP ($359-500, cash).
   Use Quest copper + zinc + ceruloplasmin (insurance-covered)
   instead of relying on Doctor's Data hair elements.

4. **Defer FM specialty labs until a strong clinical question warrants
   them.** FRAT, Cunningham Panel, OAT, IntellxxDNA, Clarifi are
   expensive cash-pay. Order one at a time, on the clinical question
   it answers best, after the foundation workup has been done.

5. **Cash-pay supplements at lowest-cost honest brands.** Carlson,
   Nordic Naturals, Pure Encapsulations, NOW Foods, Doctor's Best —
   no fancy formulations, just clean ingredients. Therapeutic-dose
   omega-3 + vitamin D + magnesium = $30-50/month total for a child.

---

# Bottom line

The functional medicine autism workup is more billable than the
field's reputation suggests. The genetics layer is insurance-covered
nearly universally. The standard labs are covered. The FDA-approved
drugs are covered. The specialty FM tests and compounded
prescriptions are HSA/FSA-eligible with proper documentation. The
gap that remains — FMT, stem cell therapy, contested chelation —
is small relative to the actionable atlas footprint.

The single highest-leverage thing a clinician can do for an FM autism
family: **write the Letter of Medical Necessity correctly.** That one
document unlocks 60-70% of the cost coverage that families otherwise
believe they have to pay cash for.

The single highest-leverage thing a parent can do: **maximize HSA
contributions in years of expected diagnostic spending.** If you're
planning to do the curated workup, front-load your HSA contribution
in January (HSA contributions are deductible AND triple-tax-advantaged).

The atlas's clinician-network model (per ACTIONABLE_REPORT_PRODUCT_SPEC.md)
makes both of these scalable. The clinician of record owns the LMN
issuance, the prior auth, and the peer-to-peer reviews. The atlas
provides the substrate evidence and the billing intelligence
(this document + the companion CSV). Together, this is what
unscales gracefully — every family doesn't need to relearn the
billing landscape from scratch.

---

*Draft v0.1 written 2026-05-16. Companion to
v2.0_scored/billing_codes.csv. Treat all coverage claims as
"typical posture" — every plan is different and every claim requires
verification with the specific patient's benefits. This document is
not legal or tax advice; it is a structured map of the payer
landscape as it stands in May 2026.*
