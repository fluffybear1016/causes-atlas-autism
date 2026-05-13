# peptides/ — README

This folder is the comprehensive peptide knowledge surface for the Causes Atlas. Built 2026-05-09 from `scripts/build_peptide_vault.py`.

## What's here

| File | Purpose |
| --- | --- |
| `00_MOC_Peptides.md` | Map of content — browse by mechanism class, with Dataview queries |
| `01_Lifecycle_Windows.md` | Lifecycle-window eligibility matrix (preconception → adolescence) |
| `02_Evidence_Tiers.md` | Evidence-tier methodology, rule of thumb for atlas promotion |
| `03_Safety_Pediatric_Notes.md` | Cross-cutting pediatric safety synthesis |
| `<slug>.md` × 25 | Individual peptide pages, one per peptide |

## Scope

Every peptide that may plausibly affect the lifecycle window from **6 months preconception through end of brain development** (adolescence). Coverage spans:

- Social neuropeptides (oxytocin, vasopressin, carbetocin)
- Neurotrophic mixtures (cerebrolysin, cortexin)
- Nootropic peptides (semax, selank, P21, dihexa)
- Mitochondrial peptides (humanin, MOTS-c, SS-31/elamipretide)
- Regenerative + anti-inflammatory (BPC-157, TB-500, KPV, LL-37)
- Growth-axis peptides (sermorelin, tesamorelin, ipamorelin, CJC-1295, IGF-1)
- Developmental neuropeptides (PACAP, VIP)
- Pineal peptides (epitalon)
- Immune modulators (thymosin α-1)

## Rebuild

```bash
cd /Users/Greg/Autism
python3 scripts/build_peptide_vault.py
```

Edit `scripts/build_peptide_vault.py` PEPTIDES list, re-run, regenerate.

## Promotion to canonical atlas

Vault peptide pages are research scaffolds. Promotion to canonical scoring (`v2.0_scored/interventions.csv` + `sources.csv`) requires PMID-verified primary evidence per `CLAUDE.md` §Verification protocol. Ten peptides are already promoted (oxytocin, BPC-157, selank, semax, cerebrolysin, vasopressin, IGF-1, LL-37, humanin, MOTS-c); the remaining 15 are vault-only.

## Goal

This database is positioned to become the dominant open-source knowledge surface for peptides in neurodevelopmental medicine. Scope is autism-first, but most peptides apply broadly (cognitive aging, neurodegeneration, regenerative medicine). The substrate is condition-agnostic; the data is autism-specific.

## Caveats

- Evidence tiers are explicit per page; honor them
- Most peptides have minimal pediatric RCT data (pediatric safety category D-E for many)
- Russian / Eastern European clinical-use peptides (cerebrolysin, cortexin, semax, selank) have decades of clinical use but minimal Western RCT validation
- Growth-axis peptides (sermorelin, tesamorelin, ipamorelin, CJC-1295) are adult-only-validated; no pediatric autism data
- Vault-only research scaffolds should NOT be used to recommend treatment without curator review + clinician input
