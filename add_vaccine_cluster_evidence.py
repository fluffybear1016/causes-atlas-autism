#!/usr/bin/env python3
"""Add 18 new vaccine-autism contested-positive primary sources + Tripedia
package insert as regulatory document. Apply CLAUDE.md §1/§3/§9/§10 source
quality tiering. Identify and tag the 6 subpopulation signal patterns.

Per CLAUDE.md §9: this isn't one signal, it's six biologically-defined
subpopulation signals — extract each.
"""
import csv, datetime as dt, json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NOW = dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')

# Sources to add (PMID 21058170 Gallagher 2010 + PMID 21623535 Delong 2011 already exist)
new_sources_data = [
    # SRC-001429 Singh 2002 — MMR/MBP autoimmunity primary research
    ("SRC-001429", "study", "pubmed", "12145534",
     "Abnormal measles-mumps-rubella antibodies and CNS autoimmunity in children with autism (Singh 2002)",
     "https://pubmed.ncbi.nlm.nih.gov/12145534/", "2002-07-01", "case_control",
     "125", 0.40,
     "MBP autoimmunity subset signal: 60% of autism had unique MMR antibody; 90% of those had MBP autoantibodies. Concrete subpopulation.",
     "Singh group (Utah State); criticized by mainstream but peer-reviewed primary research. CLAUDE.md §1: not authoritative dismissal.",
     ["HYP-0044", "HYP-0068"],
     "positive",
    ),
    # SRC-001430 Walker 2006 — metallothionein/HSP mechanistic
    ("SRC-001430", "study", "pubmed", "16870260",
     "Cultured lymphocytes from autistic children and non-autistic siblings up-regulate heat shock protein RNA in response to thimerosal challenge (Walker 2006)",
     "https://pubmed.ncbi.nlm.nih.gov/16870260/", "2006-09-01", "mechanistic",
     "", 0.40,
     "MT-deficient subset signal: autism lymphocytes fail to up-regulate metallothionein after thimerosal, instead trigger heat shock response. Concrete biomarker subset.",
     "Wake Forest; methodologically solid; mainstream-published. Demonstrates differential cellular response — exactly the subgroup analysis CLAUDE.md §7 calls for.",
     ["HYP-0044", "HYP-0069"],
     "positive",
    ),
    # SRC-001431 Tomljenovic-Shaw 2011 — Aluminum Hill criteria ecological
    ("SRC-001431", "study", "pubmed", "22099159",
     "Do aluminum vaccine adjuvants contribute to the rising prevalence of autism? (Tomljenovic & Shaw 2011)",
     "https://pubmed.ncbi.nlm.nih.gov/22099159/", "2011-11-01", "ecological",
     "", 0.30,
     "Aluminum-Al-burden ecological correlation across 7 Western countries; Hill criteria applied. Tomljenovic-Shaw group criticized by mainstream as ecological-correlation-prone but peer-reviewed.",
     "Univ British Columbia; criticized but published. CLAUDE.md §1 — not authoritative dismissal.",
     ["HYP-0067", "HYP-0044"],
     "positive",
    ),
    # SRC-001432 Singh 2003 — measles antibody serology
    ("SRC-001432", "study", "pubmed", "12849883",
     "Elevated levels of measles antibodies in children with autism (Singh 2003)",
     "https://pubmed.ncbi.nlm.nih.gov/12849883/", "2003-04-01", "case_control",
     "", 0.30,
     "Reinforces MBP-autoimmune subset: 83% of autism had unique anti-measles antibody to 74kDa protein.",
     "Singh group follow-up to 2002 paper. Same subpopulation signal.",
     ["HYP-0044", "HYP-0068"],
     "positive",
    ),
    # SRC-001433 Li 2014 — mouse thimerosal mechanistic
    ("SRC-001433", "study", "pubmed", "24675092",
     "Transcriptomic analyses of neurotoxic effects in mouse brain after intermittent neonatal administration of thimerosal (Li 2014)",
     "https://pubmed.ncbi.nlm.nih.gov/24675092/", "2014-06-01", "animal",
     "", 0.25,
     "Mouse mechanistic: thimerosal at 20× human dose induces neurodevelopment delay, social deficits, gender-specific endocrine dysregulation (males affected). Supraphysiological dose limits direct human inference but shows mechanism exists.",
     "Chinese Academy of Sciences. CAVEAT: 20× human dose. Strength 0.25 — animal + supraphysiological.",
     ["HYP-0069", "HYP-0044"],
     "positive",
    ),
    # SRC-001434 Hooker 2014 (the methodological critique paper, NOT the retracted reanalysis)
    ("SRC-001434", "study", "pubmed", "24995277",
     "Methodological issues and evidence of malfeasance in research purporting to show thimerosal in vaccines is safe (Hooker 2014)",
     "https://pubmed.ncbi.nlm.nih.gov/24995277/", "2014-06-01", "review",
     "", 0.15,
     "Methodological critique of CDC-coauthored thimerosal-safety studies. References same internal CDC study showing 7.6-fold autism risk increase that Verstraeten Generation Zero (SRC-001415) found.",
     "Hooker advocacy-adjacent + co-authors include Geier group + paid-publication concerns about BioMed Res Int. Down-weighted per CLAUDE.md §3.",
     ["HYP-0044", "HYP-0069"],
     "positive",
    ),
    # SRC-001435 Richmand 2011 — Conjugate vaccine hypothesis (Med Hypotheses)
    ("SRC-001435", "study", "pubmed", "21993250",
     "Hypothesis: conjugate vaccines may predispose children to autism spectrum disorders (Richmand 2011)",
     "https://pubmed.ncbi.nlm.nih.gov/21993250/", "2011-12-01", "hypothesis_paper",
     "", 0.15,
     "Subset signal: conjugate vaccine immune deviation during myelination window. Hib intro in US 1988, Denmark 1993, Israel 1994 correlates with ASD increases 4-5 yrs later. Mechanistic plausibility but ecological evidence only.",
     "Med Hypotheses is hypothesis-only journal. Strength 0.15 per CLAUDE.md §2.",
     ["HYP-0044"],
     "positive",
    ),
    # SRC-001436 Ratajczak 2011 — autism causes review
    ("SRC-001436", "study", "pubmed", "21299355",
     "Theoretical aspects of autism: causes — a review (Ratajczak 2011)",
     "https://pubmed.ncbi.nlm.nih.gov/21299355/", "2011-01-01", "review",
     "", 0.25,
     "Comprehensive review summarizing genetic, viral, and post-vaccination encephalitis as documented autism causes. J Immunotoxicol peer-reviewed.",
     "Mainstream peer-reviewed review.",
     ["HYP-0044", "HYP-0008"],
     "positive",
    ),
    # SRC-001437 Bernard 2001 — foundational mercury hypothesis
    ("SRC-001437", "study", "pubmed", "11339848",
     "Autism: a novel form of mercury poisoning (Bernard 2001)",
     "https://pubmed.ncbi.nlm.nih.gov/11339848/", "2001-04-01", "hypothesis_paper",
     "", 0.15,
     "Foundational mercury-autism hypothesis. SafeMinds-affiliated authors. Med Hypotheses journal. Hypothesis-tier paper but historically influential.",
     "SafeMinds advocacy origin. CLAUDE.md §3 — down-weighted but recorded as primary contested-positive document.",
     ["HYP-0069", "HYP-0044"],
     "positive",
    ),
    # SRC-001438 Bernard 2002 — short Mol Psychiatry suppl follow-up
    ("SRC-001438", "study", "pubmed", "12142947",
     "The role of mercury in the pathogenesis of autism (Bernard 2002)",
     "https://pubmed.ncbi.nlm.nih.gov/12142947/", "2002-01-01", "review",
     "", 0.15,
     "Brief Mol Psychiatry supplement update on mercury-autism hypothesis.",
     "SafeMinds. CLAUDE.md §3 — down-weighted.",
     ["HYP-0069"],
     "positive",
    ),
    # SRC-001439 Geier 2007a — case series mercury encephalopathy
    ("SRC-001439", "study", "pubmed", "17454560",
     "A case series of children with apparent mercury toxic encephalopathies manifesting with clinical symptoms of regressive autistic disorders (Geier 2007)",
     "https://pubmed.ncbi.nlm.nih.gov/17454560/", "2007-05-01", "case_series",
     "9", 0.10,
     "Poor-mercury-excreter subset signal: case series n=9, regressive autism, elevated androgens, decreased glutathione, post-chelation mercury excretion. Specific responder profile.",
     "Geier group — license revocations + advocacy + paid-publication. Strength 0.10 per CLAUDE.md §3, but recorded for subpopulation pattern.",
     ["HYP-0069", "HYP-0044"],
     "positive",
    ),
    # SRC-001440 Geier 2008 — comprehensive mercury review
    ("SRC-001440", "study", "pubmed", "19106436",
     "A comprehensive review of mercury provoked autism (Geier 2008)",
     "https://pubmed.ncbi.nlm.nih.gov/19106436/", "2008-10-01", "review",
     "", 0.10,
     "Geier group comprehensive review of mercury-autism mechanism + treatment evidence.",
     "Geier group + Indian J Med Res. Strength 0.10 per CLAUDE.md §3.",
     ["HYP-0069", "HYP-0044"],
     "positive",
    ),
    # SRC-001441 Geier 2007b — Rho(D) prenatal mercury exposure
    ("SRC-001441", "study", "pubmed", "17674242",
     "A prospective study of thimerosal-containing Rho(D)-immune globulin administration as a risk factor for autistic disorders (Geier 2007)",
     "https://pubmed.ncbi.nlm.nih.gov/17674242/", "2007-05-01", "case_control",
     "53", 0.15,
     "Rh-negative-mother subset signal: 28% of ASD cases had Rh-neg mothers vs 14% controls (OR 2.35). All Rh-neg mothers received thimerosal-Rho(D) during pregnancy. Specific demographic.",
     "Geier group. Strength 0.15 — concrete subpopulation finding but Geier methodological concerns.",
     ["HYP-0069"],
     "positive",
    ),
    # SRC-001442 Geier 2005 — testosterone-mercury hypothesis (Lupron protocol basis)
    ("SRC-001442", "study", "pubmed", "15780490",
     "The potential importance of steroids in the treatment of autistic spectrum disorders and other disorders involving mercury toxicity (Geier 2005)",
     "https://pubmed.ncbi.nlm.nih.gov/15780490/", "2005-01-01", "hypothesis_paper",
     "", 0.10,
     "Testosterone × mercury subset hypothesis: testosterone potentiates mercury toxicity; partial explanation of male:female 4:1 ratio. Basis for Geier Lupron protocol that contributed to license revocations.",
     "Geier hypothesis paper. Med Hypotheses. Lupron-protocol basis (license revocation context). Strength 0.10 per CLAUDE.md §3.",
     ["HYP-0069"],
     "positive",
    ),
    # SRC-001443 Holmes 2003 — baby haircut mercury (poor excreter signal)
    ("SRC-001443", "study", "pubmed", "12933322",
     "Reduced levels of mercury in first baby haircuts of autistic children (Holmes 2003)",
     "https://pubmed.ncbi.nlm.nih.gov/12933322/", "2003-07-01", "case_control",
     "139", 0.15,
     "Poor-mercury-excreter subset signal: autism kids had LOWER hair mercury (0.47 ppm) vs controls (3.63 ppm) despite HIGHER exposure (Rho-D, amalgams). Implies retained internally. Concrete biomarker hypothesis.",
     "SafeMinds-affiliated (Holmes/Blaxill/Haley). CLAUDE.md §3 — down-weighted but concrete subpopulation signal.",
     ["HYP-0069"],
     "positive",
    ),
    # SRC-001444 Blaylock 2008 — immunoexcitotoxicity central mechanism
    ("SRC-001444", "study", "pubmed", "19043938",
     "A possible central mechanism in autism spectrum disorders, part 1 — immunoexcitotoxicity (Blaylock 2008)",
     "https://pubmed.ncbi.nlm.nih.gov/19043938/", "2008-11-01", "review",
     "", 0.10,
     "Synthesis: chronic microglial activation + glutamate excitotoxicity + cytokine TNF-α modulation as central mechanism linking vaccines, aluminum, ethylmercury, food allergies, gut dysbiosis. Coined 'immunoexcitotoxicity'.",
     "Blaylock advocacy-adjacent + Alt Ther Health Med journal. Strength 0.10 per CLAUDE.md §3, but mechanism concept (microglial priming) is now mainstream-validated (Bilbo 2018, etc.).",
     ["HYP-0044", "HYP-0067", "HYP-0069", "HYP-0008"],
     "positive",
    ),
    # SRC-001445 Rose 2011 — Editorial on conjugate vaccines (down-weighted)
    ("SRC-001445", "study", "pubmed", "21907498",
     "Conjugate vaccines and autism (Rose 2011, Editorial)",
     "https://pubmed.ncbi.nlm.nih.gov/21907498/", "2011-12-01", "editorial",
     "", 0.10,
     "Editorial commentary on Richmand 2011 conjugate vaccine hypothesis paper.",
     "Editorial — CLAUDE.md §2 down-weights to 0.10.",
     ["HYP-0044"],
     "unknown",
    ),
    # SRC-001446 Chhawchharia 2014 — Comment on Hooker/Thompson
    ("SRC-001446", "study", "pubmed", "25377033",
     "Commentary — Controversies surrounding mercury in vaccines: autism denial as impediment to universal immunisation (Chhawchharia 2014)",
     "https://pubmed.ncbi.nlm.nih.gov/25377033/", "2014-10-01", "comment",
     "", 0.05,
     "Commentary on Thompson whistleblower / Hooker reanalysis claims. Indian J Med Ethics.",
     "Comment — CLAUDE.md §2 down-weights to 0.05.",
     ["HYP-0044", "HYP-0068"],
     "positive",
    ),
]

# Tripedia package insert as regulatory document
tripedia_source = (
    "SRC-001447", "regulatory_document", "fda_manufacturer_insert", "tripedia_dtap_insert",
    "Tripedia (DTaP) Diphtheria and Tetanus Toxoids and Acellular Pertussis Vaccine Adsorbed — Sanofi Pasteur package insert (FDA-approved). Lists autism as adverse event reported during post-approval use.",
    "https://www.fda.gov/media/74035/download",  # FDA-archived insert (best available; manufacturer no longer markets product but insert remains in FDA records)
    "2005-12-01", "regulatory_document",
    "",
    0.30,  # primary regulatory document, but insert itself flags passive surveillance limits
    "Manufacturer-listed adverse event in FDA-approved insert. Per CLAUDE.md §1+§4, primary regulatory document carries weight.",
    ("Tripedia DTaP insert (Sanofi Pasteur, FDA-approved): 'Adverse events reported during "
     "post-approval use of Tripedia vaccine include idiopathic thrombocytopenic purpura, "
     "SIDS, anaphylactic reaction, cellulitis, AUTISM, convulsion/grand mal convulsion, "
     "encephalopathy, hypotonia, neuropathy, somnolence and apnea.' IMPORTANT CAVEAT from "
     "the document itself: 'Events were included in this list because of the seriousness "
     "or frequency of reporting. Because these events are reported voluntarily from a "
     "population of uncertain size, it is not always possible to reliably estimate their "
     "frequencies or to establish a causal relationship to components of Tripedia "
     "vaccine.' This is passive-surveillance reporting, not causal inference. But the "
     "manufacturer + FDA explicitly listing autism as a reported post-approval adverse "
     "event is a significant primary-document fact, especially read alongside the "
     "Hannah Poling federal court ruling (SRC-001418)."),
    ["HYP-0044"],
    "positive",
)

# Build src records
src_fields_required = ["id","type","platform","external_id","title","url",
                       "date_published","date_ingested","study_design",
                       "sample_size","model_system","raw_metadata","notes"]

new_sources = []
new_fragments = []
new_links = []
link_id = 1670  # next available EVL ID

evd_id = 1430  # next available EVD ID

for entry in new_sources_data:
    sid, stype, plat, ext, title, url, date, design, samp, strength, fragment_text_short, notes_short, target_hyps, direction = entry
    new_sources.append({
        "id": sid, "type": stype, "platform": plat, "external_id": ext,
        "title": title, "url": url,
        "date_published": date, "date_ingested": NOW,
        "study_design": design, "sample_size": samp,
        "model_system": "human" if "mouse" not in title.lower() else "mouse",
        "raw_metadata": json.dumps({"pmid": ext, "year": int(date.split("-")[0])}),
        "notes": notes_short,
    })
    fid = f"EVD-{evd_id:06d}"
    new_fragments.append({
        "id": fid, "source_id": sid, "fragment_type": "result",
        "text_excerpt": fragment_text_short,
        "structured_payload": json.dumps({
            "subpopulation_signal": fragment_text_short,
            "primary": True,
            "is_secondary_literature": design in ("review","editorial","comment"),
        }),
        "effect_direction": direction, "strength_score": f"{strength:.2f}",
        "extraction_method": "manual", "extraction_confidence": "0.85",
        "date_extracted": NOW, "notes": "",
    })
    for hid in target_hyps:
        new_links.append({
            "id": f"EVL-{link_id:06d}",
            "evidence_fragment_id": fid, "claim_id": "",
            "target_type": "hypothesis", "target_id": hid,
            "effect_direction": direction, "weight": "", "context_scope": "",
            "created_at": NOW, "notes": notes_short[:80],
        })
        link_id += 1
    evd_id += 1

# Add Tripedia insert
sid, stype, plat, ext, title, url, date, design, samp, strength, notes_short, fragment_text, target_hyps, direction = tripedia_source
new_sources.append({
    "id": sid, "type": stype, "platform": plat, "external_id": ext,
    "title": title, "url": url,
    "date_published": date, "date_ingested": NOW,
    "study_design": design, "sample_size": samp,
    "model_system": "human", "raw_metadata": json.dumps({"document_type": "fda_package_insert", "manufacturer": "Sanofi Pasteur"}),
    "notes": notes_short,
})
fid = f"EVD-{evd_id:06d}"
new_fragments.append({
    "id": fid, "source_id": sid, "fragment_type": "regulatory",
    "text_excerpt": fragment_text,
    "structured_payload": json.dumps({
        "document_type": "FDA-approved package insert",
        "manufacturer": "Sanofi Pasteur",
        "passive_surveillance": True,
        "causal_inference": False,
        "primary": True,
        "is_secondary_literature": False,
    }),
    "effect_direction": direction, "strength_score": "0.30",
    "extraction_method": "manual", "extraction_confidence": "0.95",
    "date_extracted": NOW, "notes": "Regulatory primary document. Per CLAUDE.md §4, primary regulatory documents are tier-1 evidence.",
})
for hid in target_hyps:
    new_links.append({
        "id": f"EVL-{link_id:06d}",
        "evidence_fragment_id": fid, "claim_id": "",
        "target_type": "hypothesis", "target_id": hid,
        "effect_direction": direction, "weight": "", "context_scope": "",
        "created_at": NOW, "notes": "Tripedia insert lists autism as post-approval adverse event",
    })
    link_id += 1

# Append to canonical CSVs
def append(path, fields, new_rows, id_field="id"):
    rows = list(csv.DictReader(open(path)))
    existing = {r[id_field] for r in rows}
    added = 0
    for r in new_rows:
        if r[id_field] in existing: continue
        out = {f: r.get(f, "") for f in fields}
        rows.append(out); added += 1
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
    return added

for d in [ROOT/"v2.0_scored", ROOT/"v2.0.1_expanded"]:
    print(f"\n{d.name}:")
    src_fields = list(csv.DictReader(open(d/"sources.csv")).fieldnames)
    n = append(d/"sources.csv", src_fields, new_sources)
    print(f"  sources.csv: +{n}")
    frag_fields = list(csv.DictReader(open(d/"evidence_fragments.csv")).fieldnames)
    n = append(d/"evidence_fragments.csv", frag_fields, new_fragments)
    print(f"  evidence_fragments.csv: +{n}")
    link_fields = list(csv.DictReader(open(d/"evidence_links.csv")).fieldnames)
    n = append(d/"evidence_links.csv", link_fields, new_links)
    print(f"  evidence_links.csv: +{n}")

# Update HYP-0044 description with the 6 subpopulation signals analysis
print()
print("Updating HYP-0044 with subpopulation signal pattern analysis...")
new_044_desc = (
    "Childhood vaccine schedule as a contested autism causal factor. Per CLAUDE.md "
    "§9 (mixed evidence is heterogeneity, not absence) — published primary evidence "
    "is NOT a single signal but at least SIX biologically-defined subpopulation "
    "signals, each with its own mechanism and biomarker. Mainstream studies "
    "averaging across these subpopulations find null because each is small and "
    "each has different drivers. The atlas preserves all six.\n\n"
    "**SUBPOPULATION 1 — Poor mercury excreter** (Holmes 2003 SRC-001443): autism "
    "kids had LOWER hair mercury (0.47 ppm) vs controls (3.63 ppm) despite HIGHER "
    "exposure — consistent with retained internally. Biomarker: hair mercury "
    "elimination ratio.\n\n"
    "**SUBPOPULATION 2 — Metallothionein-deficient** (Walker 2006 SRC-001430): "
    "lymphocytes from autism kids fail to up-regulate metallothionein when challenged "
    "with thimerosal, instead trigger heat shock response. Biomarker: MT gene "
    "expression panel + heat shock response gene panel.\n\n"
    "**SUBPOPULATION 3 — MBP-autoimmune** (Singh 2002 SRC-001429, Singh 2003 "
    "SRC-001432): 60% of autism cases had unique anti-MMR antibody (specifically "
    "to measles HA 73-75kDa); 90% of those positive for myelin basic protein "
    "autoantibodies. Biomarker: MBP autoantibody panel + measles HA antibody.\n\n"
    "**SUBPOPULATION 4 — Rh-negative mother + prenatal Rho(D) exposure** (Geier "
    "2007 SRC-001441): 28% of ASD cases had Rh-neg mothers vs 14% controls "
    "(OR 2.35); all received thimerosal-Rho(D)-immune globulin during pregnancy "
    "(pre-2001 formulation). Biomarker: maternal Rh status + gestational Rho(D) "
    "history. NOTE: thimerosal removed from Rho(D) post-2001, so this is a "
    "historical-cohort signal.\n\n"
    "**SUBPOPULATION 5 — Aluminum-burden cumulative** (Tomljenovic 2011 SRC-001431): "
    "ecological correlation across 7 Western countries between Al adjuvant exposure "
    "schedule and ASD prevalence (Pearson r=0.89-0.94). Biomarker: schedule "
    "Al-burden calculation; possibly serum/CSF aluminum.\n\n"
    "**SUBPOPULATION 6 — Conjugate vaccine immune deviation during myelination** "
    "(Richmand 2011 SRC-001435): hypothesis that Hib/Pneumococcal conjugate "
    "vaccines deviate immune system from carbohydrate hypo-responsiveness during "
    "myelination window (peak ~6mo-2y). Mechanism plausible; ecological evidence "
    "only. Biomarker: timing-of-conjugate-exposure vs myelination window.\n\n"
    "**Mechanistic synthesis** (Blaylock 2008 SRC-001444 — the immunoexcitotoxicity "
    "framework): chronic microglial priming + glutamate excitotoxicity + cytokine "
    "TNF-α modulation. Note that the microglial-priming part of this framework is "
    "now mainstream-validated (Bilbo 2018, Tetreault 2012, Vargas 2005). Connects "
    "to MEC-0002 neuroinflammation, MEC-0005 microglial activation, MEC-0007 "
    "GABA/glutamate.\n\n"
    "**Regulatory-document evidence**: Tripedia (DTaP) FDA-approved package insert "
    "(SRC-001447) lists autism as adverse event reported during post-approval use. "
    "Insert flags passive-surveillance limitations; not causal inference. But "
    "manufacturer-listed primary regulatory document.\n\n"
    "**Federal court evidence**: Hannah Poling 2008 (SRC-001418) — federally-"
    "adjudicated case where mitochondrial-vulnerable child decompensated into "
    "regressive ASD-features encephalopathy after vaccine challenge. Establishes "
    "additional susceptibility-tier subpopulation: **mitochondrial-vulnerable "
    "subset**.\n\n"
    "Per CLAUDE.md §1, §5, §9, status=contested permanent. Per atlas mission, "
    "individual-level resolution: a child whose biomarkers indicate one or more "
    "of these subpopulations carries a different conditional risk than the "
    "population average. The personalized risk calculator (Session 4) will use "
    "these subpopulation profiles to stratify."
)
new_044_notes = (
    "Status=contested permanent. Six subpopulation signals identified per CLAUDE.md "
    "§9: poor-mercury-excreter, MT-deficient, MBP-autoimmune, Rh-neg-mother + "
    "prenatal Rho(D), Al-burden cumulative, conjugate-vaccine immune-deviation. "
    "Plus mito-vulnerable (Hannah Poling). Mainstream null studies don't refute "
    "subpopulation-specific signals — different study designs answer different "
    "questions."
)

for d in [ROOT/"v2.0_scored", ROOT/"v2.0.1_expanded"]:
    p = d/"hypotheses.csv"
    rows = list(csv.DictReader(open(p)))
    fields = list(csv.DictReader(open(p)).fieldnames)
    for r in rows:
        if r["id"] == "HYP-0044":
            r["description"] = new_044_desc
            r["notes"] = new_044_notes
            r["last_updated"] = NOW
    with open(p, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
    print(f"  {d.name}/hypotheses.csv: HYP-0044 updated with subpopulation pattern analysis")

print()
print(f"Done. Added {len(new_sources)} sources, {len(new_fragments)} fragments, {len(new_links)} links.")
print("HYP-0044 now elucidates the 6+1 subpopulation signal pattern.")
print()
print("Next: re-run scoring + verify INT-0001 + rebuild vault.")
