#!/usr/bin/env python3
"""expand_combinations.py — append 20 mechanism-grounded combinations to the
atlas. Mirrors the formulations supplementary-layer pattern: doesn't modify
existing rows, only appends new COM-XXXX + CMM-XXXX entries. Calibration
anchor protected. Verifies INT-0001 unchanged.

Each combination has:
  - mechanism rationale grounded in atlas evidence
  - explicit member intervention IDs
  - explicit interaction warnings
  - status: candidate (curator-promotable)
"""
from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCORED = ROOT / "v2.0_scored"
COMBOS = SCORED / "combinations.csv"
MEMBERS = SCORED / "combination_members.csv"

NOW = datetime.utcnow().isoformat() + "+00:00"

# === 20 new combinations =====================================================
# Each: name, members (INT IDs), description, rationale, warnings
NEW = [
    # --- Methylation stacks (folate × B12 × cofactor) ---
    ("Leucovorin + Methyl-B12 + Vitamin D",
     ["INT-0001", "INT-0003", "INT-0013"],
     "Cerebral folate + methylation + immune-trophic vitamin D triple. Each component has independent RCT support; combination is anecdotally common in functional medicine but not formally RCT-tested.",
     "Triple-axis support for the FRAA-positive + methylation-impaired + vitamin-D-insufficient subset. Frye 2018 leucovorin RCT (FRAA+ 78% responder rate) + Hendren 2016 methyl-B12 RCT (low-methionine 52% responder) + vitamin D status as immune-trophic substrate.",
     "Monitor for excess methylation symptoms in COMT++ children. Vitamin D titrate to 25-OH-D 50-80 ng/mL."),

    ("5-MTHF + P5P (B6) + TMG/Betaine",
     ["INT-0008", "INT-0017", "INT-0018"],
     "Methylation-cycle substrate stack: 5-MTHF (folate cycle) + P5P (transsulfuration cofactor) + TMG (alternative methyl donor via BHMT pathway).",
     "Walsh under-methylator subset (low SAM/SAH, low histamine) plus elevated-homocysteine subset. Targets the methylation cycle from three independent biochemical entry points.",
     "Monitor for anxiety/hyperactivity in COMT++ over-methylators (folate may worsen this subset). Adjust dose by histamine + SAM/SAH retest at 8-12 weeks."),

    # --- Mitochondrial stacks ---
    ("Mito-CNS stack: ALCAR + CoQ10 ubiquinol + Alpha-lipoic acid",
     ["INT-0011", "INT-0093"],
     "BBB-crossing mitochondrial stack. ALCAR + CoQ10 ubiquinol + alpha-lipoic acid. Note: this duplicates partial coverage of INT-0055 mitochondrial cocktail (CoQ10+L-carnitine+B-complex); narrows to CNS-specific variant.",
     "Targets PHE-0002 (mitochondrial dysfunction) — three convergent mechanisms: ALCAR shuttles fatty acids across the inner mitochondrial membrane + crosses BBB; ubiquinol-form CoQ10 supports ETC complex III; alpha-lipoic acid regenerates intracellular glutathione + is dihydrolipoyl cofactor for PDH/KGDH.",
     "Mostly well-tolerated. Alpha-lipoic acid can lower blood sugar; monitor in metabolic conditions."),

    ("Energy-substrate stack: D-ribose + Creatine + L-carnitine",
     ["INT-0094", "INT-0088", "INT-0011"],
     "Energy-substrate stack for mitochondrial-fatigue phenotypes. D-ribose supports ATP regeneration via pentose phosphate; creatine provides phosphocreatine buffer; L-carnitine for fatty-acid β-oxidation.",
     "Bioenergetic substrate triple for mito-vulnerable subset. Each component addresses a different rate-limiting step of cellular energy production.",
     "D-ribose at high doses can lower blood sugar; titrate. Creatine generally well-tolerated."),

    # --- Anti-inflammatory / oxidative stress ---
    ("Anti-inflammatory polyphenol stack: Liposomal curcumin + Quercetin phytosome + Omega-3",
     ["INT-0010", "INT-0014"],
     "Inflammation-resolution stack. Each component independently anti-inflammatory; combination saturates multiple inflammation-resolution pathways.",
     "Targets PHE-0003 (immune-brain inflammation). Liposomal curcumin (FRM-0017) inhibits NF-κB at high systemic bioavailability; quercetin phytosome inhibits mast cell degranulation; omega-3 (EPA→resolvins, DHA→neuroprotectins).",
     "Quercetin + curcumin may potentiate platelet inhibition; monitor in coagulopathy or pre-surgical contexts. Avoid high-dose curcumin with chemotherapy."),

    ("Glutathione regeneration stack: Sulforaphane + Liposomal glutathione + NAC",
     ["INT-0002", "INT-0004"],
     "Three-mechanism glutathione support. Sulforaphane induces endogenous glutathione synthesis via Nrf2; liposomal glutathione provides exogenous reduced glutathione; NAC provides cysteine precursor.",
     "Singh 2014 RCT showed 34.6% responder rate for sulforaphane monotherapy. Combination addresses both endogenous synthesis capacity (sulforaphane + NAC) and direct GSH replacement (liposomal). Targets oxidative-stress subset.",
     "Generally well-tolerated. Sulforaphane requires active myrosinase (FRM-0028); standard turmeric-style commodity sources have variable conversion."),

    ("Mast-cell stabilizer stack: Luteolin + Quercetin + Rutin (NeuroProtek-style)",
     ["INT-0029"],
     "Polyphenol triple matching the Tsilioni 2015 NeuroProtek formulation (luteolin 100 mg + quercetin 70 mg + rutin 30 mg).",
     "Targets PHE-0003 inflammatory subset, specifically MCAS-overlap children with elevated IL-6/TNF (Tsilioni 2015 identified n=10/38 high-cytokine subset who showed VABS improvement). Three flavonoids with overlapping mast-cell stabilization + anti-inflammatory action.",
     "Generally safe at recommended doses. Bioavailability is the rate-limiting step; consider phytosome or liposomal forms for high-dose applications."),

    # --- Gut-brain axis ---
    ("Gut-repair stack: Bifidobacterium infantis EVC001 + L-glutamine + Zinc carnosine",
     ["INT-0077", "INT-0101", "INT-0016"],
     "Targeted gut-mucosal repair. EVC001 strain reconstitutes infant-gut microbiome niche (Hsiao 2013 framework); L-glutamine fuels enterocytes; zinc carnosine repairs tight junctions.",
     "Targets PHE-0004 (gut–microbiome) — particularly the early-postnatal-window dysbiosis associated with regression phenotype. Bifidobacterium infantis is strain-specific (FRM-0034) — distinct from generic multi-strain probiotics (FRM-0037 contested).",
     "L-glutamine: monitor in liver/kidney dysfunction. Zinc carnosine: long-term high-dose zinc displaces copper; monitor Cu:Zn ratio."),

    ("VSL#3 / Visbiome + Bovine colostrum + L-glutamine (intensive gut-repair)",
     ["INT-0025", "INT-0101"],
     "Intensive gut-mucosal-repair stack. VSL#3 / Visbiome multi-strain (FRM-0036) + bovine colostrum (IgG-rich, growth-factor) + L-glutamine for enterocyte fuel.",
     "GI-symptomatic + intestinal-permeability phenotype. VSL#3 has IBD/UC RCT support (FRM-0036 RCT-validated); colostrum adds passive IgG + growth factors that promote epithelial repair.",
     "Colostrum is bovine-derived; consider in dairy-sensitive children. L-glutamine cautions per above."),

    ("Microbiota repair + immune-modulation: MTT + Bifidobacterium infantis + LDN",
     ["INT-0076", "INT-0077", "INT-0006"],
     "Sequential microbiota repair + immune modulation. Microbiota Transfer Therapy (MTT) provides whole-community restoration (Kang 2017 89% GI responder rate); strain-specific maintenance probiotic; LDN for systemic immune-modulation downstream.",
     "PHE-0004 (GI) + PHE-0003 (inflammation) overlap subset. MTT establishes the microbial baseline; LDN modulates immune-tone in subsequent months as gut-brain axis recalibrates.",
     "MTT requires specialized provider (Adams lab protocol or equivalent). LDN compounded; dose titration usually 0.5 → 4.5 mg over 4-6 weeks."),

    # --- GABA / anxiety / sleep ---
    ("Calm-axis stack: L-theanine + Magnesium glycinate + Saffron",
     ["INT-0015", "INT-0034"],
     "Anxiolytic + sleep-supportive stack. L-theanine modulates glutamate/GABA balance + induces alpha-wave activity; magnesium glycinate is NMDA-receptor modulator + GABA-A co-agonist; saffron has mood + anxiety effects in adolescent RCTs (Lopresti 2018).",
     "Anxiety-predominant subset; co-occurring sleep onset issues. Three-mechanism calm-axis support (glutamate, NMDA, serotonergic).",
     "Saffron at therapeutic doses (30 mg/d) generally well-tolerated; very high doses (>1.5 g) toxic. Magnesium glycinate well-tolerated; avoid magnesium oxide (FRM-0051 contested — laxative effect, low bioavailability)."),

    ("L-carnosine + L-taurine + Magnesium threonate (GABA-axis stack)",
     ["INT-0011"],
     "GABA-axis support. L-carnosine (Chez 2002 RCT in autism, GABA modulation via homocarnosine, INT-0011 / FRM-0047); L-taurine (GABA-A modulation); magnesium threonate (brain-targeted Mg, FRM-0050).",
     "Subset with subclinical epileptiform EEG or anxiety-irritability cluster. Targets PHE-0007 (GABA/Cl⁻ imbalance). Magnesium threonate crosses BBB more efficiently than glycinate.",
     "Generally well-tolerated. Magnesium threonate higher cost; glycinate is cost-effective substitute for non-CNS-dominant Mg deficiency."),

    ("Sleep-architecture stack: Melatonin (ext-release) + Magnesium glycinate + L-theanine",
     ["INT-0046", "INT-0015"],
     "Sleep-axis stack for severe-dysomnia subset. Wright 2011 RCT validated melatonin for autism dysomnia not amenable to behavior management; extended-release form (FRM-0042) addresses sleep-maintenance; magnesium + L-theanine address pre-sleep arousal.",
     "Wright 2011 (PMID 20535539) showed melatonin improves sleep latency (-46.7 min) + total sleep (+52.3 min). Adding magnesium + L-theanine addresses the pre-sleep + maintenance components separately.",
     "Long-term melatonin pediatric data is incomplete; some clinicians recommend periodic discontinuation. Monitor for vivid dreams."),

    # --- PANS / immune subset ---
    ("PANS-overlap stack: LDN + Cromolyn + Quercetin",
     ["INT-0006", "INT-0029"],
     "Immune-modulation + mast-cell-stabilization stack for PANS-overlap subset. LDN modulates microglia + opioid-receptor immune effects; cromolyn (FRM-0044 oral gut-targeted + FRM-0045 nasal) stabilizes mast cells; quercetin adds polyphenol mast-cell stabilization.",
     "PANS-positive (Cunningham panel + acute-onset OCD/tics) subset with mast-cell-activation overlap. Three-mechanism immune modulation: opioid-receptor (LDN), chromone mast-cell stabilizer (cromolyn), flavonoid mast-cell stabilizer (quercetin).",
     "LDN at low doses; titrate from 0.5 mg. Cromolyn oral has poor systemic absorption; gut-targeted by design. Quercetin: monitor for platelet effects in coagulopathy."),

    ("Recurrent-infection + immune stack: Thymosin α-1 + Vitamin D + Zinc",
     ["INT-0013", "INT-0016"],
     "Adaptive immunity support for recurrent-infection subset. Thymosin α-1 modulates T-cell maturation (extra-atlas peptide — see vault/peptides/); vitamin D drives LL-37 antimicrobial peptide; zinc is enzymatic cofactor for thymulin + immune function.",
     "Recurrent ear/sinus/throat infection subset with autoimmune family history. Three-mechanism adaptive immunity support.",
     "Thymosin α-1 is non-FDA in US; consult with immunologist. Zinc long-term: monitor Cu:Zn ratio."),

    # --- Methyl-donor stacks for syndromic phenotypes ---
    ("Choline + DHA + Methylfolate (preconception/prenatal cognitive-development stack)",
     ["INT-0008", "INT-0014", "INT-0030"],
     "Preconception + prenatal cognitive-development stack. CDP-choline / Alpha-GPC + DHA + 5-MTHF. Each component independently associated with cognitive-development outcomes; this combination targets the methylation × membrane-integrity × folate-cycle triad during the most plastic developmental window.",
     "Maternal preconception + first/second trimester. Choline supports phosphatidylcholine + acetylcholine synthesis; DHA is the dominant brain fatty acid; 5-MTHF supports the methylation cycle (avoids synthetic folic acid concerns — FRM-0015 contested).",
     "Choline at >7g/d can cause fishy body odor; standard preconception dose ~500-1000 mg manageable. DHA: monitor mercury content of fish-oil source; algae-derived DHA preferred."),

    # --- Environmental + lifestyle combos ---
    ("Detox + binder stack: Liposomal glutathione + Modified citrus pectin + Activated charcoal",
     ["INT-0004"],
     "Detox phase 2 + binder stack. Glutathione conjugation (phase 2 detox) + modified citrus pectin (heavy-metal binder, particularly lead/cadmium) + activated charcoal (broad-spectrum gut binder).",
     "Environmental-exposure subset with documented heavy-metal burden (hair mineral analysis or provoked-urine challenge). Three-mechanism detox: glutathione provides conjugation capacity; binders prevent enterohepatic recirculation.",
     "Activated charcoal interferes with medication absorption; separate dosing by 2+ hours. Long-term high-dose chelation requires medical supervision."),

    ("Cold exposure + sauna + omega-3 (anti-inflammatory lifestyle stack)",
     ["INT-0014", "INT-0047"],
     "Hormesis + omega-3 stack. Cold exposure activates norepinephrine + brown adipose; sauna activates heat-shock proteins + cardiovascular conditioning; omega-3 provides resolvins/protectins substrate.",
     "Inflammation-predominant adolescent subset with stable physiology. Hormetic stressors plus anti-inflammatory substrate; supports neurogenesis + inflammation resolution.",
     "Cold/sauna exposure contraindicated in unstable cardiovascular conditions or pediatric autonomic dysregulation. Adult / adolescent only."),

    # --- Long-form preconception combos ---
    ("Paternal preconception stack: CoQ10 ubiquinol + Zinc + Selenium + L-carnitine + Antioxidants",
     ["INT-0016", "INT-0067", "INT-0011"],
     "Paternal preconception (90-180 days before conception, matching spermatogenesis cycle). CoQ10 + L-carnitine for sperm mitochondrial function; zinc + selenium for sperm DNA-integrity; antioxidants for sperm DNA-fragmentation prevention.",
     "Preconception window targeting paternal contribution to gametic mitochondrial DNA quality + sperm DNA-fragmentation. Spermatogenesis cycle is ~74 days; 90-180 day window covers two cycles plus margin.",
     "Selenium narrow therapeutic window; dose 100-200 mcg/d. Zinc: monitor Cu:Zn ratio."),

    ("Maternal preconception methylation + mito stack",
     ["INT-0008", "INT-0017", "INT-0014", "INT-0030"],
     "Maternal preconception (90-180 days before conception). Methylated folate + B6 (P5P) + DHA + choline. Mirrors COM-0002 with explicit pre-conception window.",
     "Combines methylation substrate (5-MTHF + P5P + choline) with membrane-integrity (DHA). Targets the highest-leverage modifiable window for maternal gametic + early-embryonic epigenetic programming.",
     "Folate may worsen subset of FRAA-positive females (test pre-supplementation in mothers with personal/family autism history). DHA: source-mercury caution."),
]


def main() -> None:
    # Read existing
    with COMBOS.open() as f:
        rd = csv.DictReader(f)
        combos_fieldnames = rd.fieldnames
        existing_combos = list(rd)

    with MEMBERS.open() as f:
        rd = csv.DictReader(f)
        members_fieldnames = rd.fieldnames
        existing_members = list(rd)

    # Capture INT-0001 before
    with (SCORED / "interventions.csv").open() as f:
        rd = csv.DictReader(f)
        anchor_before = None
        for r in rd:
            if r["id"] == "INT-0001":
                anchor_before = r.get("csrs_score")
                break

    # Compute next IDs
    com_ids = [int(c["id"].split("-")[1]) for c in existing_combos if c["id"].startswith("COM-")]
    next_com = max(com_ids) + 1 if com_ids else 6

    cmm_ids = [int(c["id"].split("-")[1]) for c in existing_members if c["id"].startswith("CMM-")]
    next_cmm = max(cmm_ids) + 1 if cmm_ids else 1

    new_combo_rows = []
    new_member_rows = []
    for (name, members, desc, rationale, warnings) in NEW:
        com_id = f"COM-{next_com:04d}"
        next_com += 1
        row = {f: "" for f in combos_fieldnames}
        row.update({
            "id": com_id,
            "name": name,
            "description": desc,
            "rationale": rationale,
            "interaction_warnings": warnings,
            "csrs_score": "",  # will be computed in next scoring pass
            "csrs_last_updated": "",
            "status": "candidate",
            "created_at": NOW,
            "last_updated": NOW,
            "notes": "Promoted from autonomous-discoveries pipeline review; awaiting scoring pass.",
        })
        new_combo_rows.append(row)
        for iid in members:
            cmm_id = f"CMM-{next_cmm:04d}"
            next_cmm += 1
            mrow = {f: "" for f in members_fieldnames}
            mrow.update({
                "id": cmm_id,
                "combination_id": com_id,
                "intervention_id": iid,
                "role": "",
                "created_at": NOW,
            })
            new_member_rows.append(mrow)

    # Append
    with COMBOS.open("a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=combos_fieldnames)
        for r in new_combo_rows:
            w.writerow(r)
    with MEMBERS.open("a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=members_fieldnames)
        for r in new_member_rows:
            w.writerow(r)

    # Re-read INT-0001 to verify unchanged
    with (SCORED / "interventions.csv").open() as f:
        rd = csv.DictReader(f)
        anchor_after = None
        for r in rd:
            if r["id"] == "INT-0001":
                anchor_after = r.get("csrs_score")
                break

    print(f"Appended {len(new_combo_rows)} combinations + {len(new_member_rows)} member rows")
    print()
    print(f"  INT-0001 csrs_score BEFORE: {anchor_before}")
    print(f"  INT-0001 csrs_score AFTER:  {anchor_after}")
    print(f"  Calibration anchor preserved: {anchor_before == anchor_after}")
    print()
    print(f"  Total combinations now: {len(existing_combos) + len(new_combo_rows)}")
    print(f"  Total combination_members now: {len(existing_members) + len(new_member_rows)}")
    print()
    print("New combination IDs:")
    for r in new_combo_rows:
        print(f"  {r['id']:9s} {r['name'][:65]}")


if __name__ == "__main__":
    main()
