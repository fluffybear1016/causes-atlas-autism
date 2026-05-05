#!/usr/bin/env python3
"""Fix INT/HYP wikilink mismatches in PHE-0001 through PHE-0007 deep-dive pages.

Sub-agent audit found multiple ID-to-name mismatches. This script applies the
verified canonical mapping.
"""
import re
from pathlib import Path

VAULT = Path("/sessions/jolly-determined-darwin/mnt/Autism/vault/topics/phenotypes")

# (file, old_pattern, new_pattern, label)
FIXES = {
    "PHE-0002_Mitochondrial_Dysfunction.md": [
        # CoQ10/L-carnitine swap — INT-0011 is L-carnitine, INT-0012 is CoQ10
        ("**[[INT-0011]] CoQ10 (ubiquinol form preferred for absorption)**",
         "**[[INT-0012]] CoQ10 (ubiquinol form preferred for absorption)**"),
        ("**[[INT-0012]] L-carnitine**",
         "**[[INT-0011]] L-carnitine**"),
        # INT-0017 is B6, not B12 — use INT-0003 for methyl-B12
        ("**[[INT-0017]] Methyl-B12**",
         "**[[INT-0003]] Methyl-B12 (methylcobalamin)**"),
        # INT-0019 is SAMe, not riboflavin — drop the wikilink
        ("**[[INT-0019]] Riboflavin (B2)** — Complex I/II cofactor (FAD); 50-400 mg/day",
         "**Riboflavin (B2)** — Complex I/II cofactor (FAD); 50-400 mg/day"),
        # INT-0020 is glutathione, not thiamine — drop the wikilink
        ("**[[INT-0020]] Thiamine (B1)** — pyruvate dehydrogenase cofactor; high-dose form (TTFD or benfotiamine) for BBB",
         "**Thiamine (B1)** — pyruvate dehydrogenase cofactor; high-dose form (TTFD or benfotiamine) for BBB"),
        # INT-0055 is mitochondrial cocktail; NMN/NR is INT-0068 or INT-0121
        ("**[[INT-0055]] NAD+ precursors (NMN / NR)**",
         "**[[INT-0068]] NAD+ precursors (NMN / NR)**"),
    ],
    "PHE-0003_Regressive_Immune_Inflammatory.md": [
        # INT-0027 is curcumin, not IVIG. Drop wikilink for IVIG (no canonical IVIG INT)
        ("**[[INT-0027]] IVIG**",
         "**IVIG**"),
        # HYP-0008 is Maternal immune activation — correct! HYP-0026 is PANDAS — wrong label was given
        # The original linked HYP-0008 with label "Neuroinflammation" (wrong) and HYP-0026 with label "MIA" (wrong)
        # Fix labels to match canonical IDs
        ("- [[HYP-0008 Neuroinflammation _ microglial activation]] — hypothesis record",
         "- [[HYP-0008 Maternal immune activation (prenatal infection or autoimmune)]] — MIA hypothesis record"),
        ("- [[HYP-0026 Maternal immune activation]] — MIA hypothesis",
         "- [[HYP-0026 PANDAS_PANS triggers (strep, mycoplasma)]] — post-infectious overlap"),
    ],
    "PHE-0004_GI_Microbiome.md": [
        # INT-0042 is GAPS diet, not "additional barrier supports" — replace generic line
        ("- **[[INT-0042]]** — additional barrier supports",
         "- **[[INT-0101]] L-glutamine** — colonocyte fuel (already listed above; alternative SKU)"),
        # HYP-0022 is "Early-life antibiotics", not "Intestinal permeability". Use HYP-0059 instead
        ("- [[HYP-0022 Intestinal permeability]] — coupled hypothesis",
         "- [[HYP-0059 Intestinal barrier permeability ('leaky gut')]] — coupled hypothesis"),
    ],
    "PHE-0005_mTOR_Pathway_Syndromic.md": [
        # INT-0037 is Metformin, not Sirolimus. Drop the second wikilink (sirolimus = rapamycin = INT-0036)
        ("- **[[INT-0036]] / [[INT-0037]] Rapamycin / Sirolimus**",
         "- **[[INT-0036]] Rapamycin (sirolimus)**"),
    ],
    "PHE-0006_Fragile_X_FMR1.md": [
        # HYP-0027 is "De novo synaptic genes" — there's no canonical FXS HYP. Use a wikilink without ID number, or note as missing.
        ("- [[HYP-0027 Fragile X syndrome]] — hypothesis record",
         "- *(Fragile X-specific hypothesis not yet a separate atlas record; FXS is captured under [[HYP-0028 Polygenic risk burden (common variants)]] gene-layer linkage to FMR1)*"),
        # INT-0022 is Inositol, INT-0035 is CBD. Keep INT-0035 (CBD matches Zynerba context). Replace INT-0022 with general note.
        ("- [[INT-0022]] / [[INT-0035]] — interventions tagged to phenotype",
         "- [[INT-0035]] Cannabidiol (CBD) — Zynerba topical CBD trial"),
    ],
    "PHE-0007_GABA_Cl_Imbalance.md": [
        # INT-0023 is Taurine, not bumetanide. Bumetanide is INT-0005 (general) or INT-0123 (autism-specific). Use INT-0005 only.
        ("- **[[INT-0005]] / [[INT-0023]] Bumetanide**",
         "- **[[INT-0005]] Bumetanide**"),
        # INT-0024 is Glycine, not L-theanine. Drop the wikilink (no canonical L-theanine INT)
        ("- **[[INT-0024]] L-theanine**",
         "- **L-theanine**"),
        # INT-0023 in next section is taurine — but here it's listed as bumetanide. Already fixed above.
        # Check second instance:
        ("[[INT-0005]] / [[INT-0023]] — bumetanide",
         "[[INT-0005]] / [[INT-0123]] — bumetanide entries"),
        # HYP-0011 is "Phthalate exposure (prenatal+postnatal)", not GABA/Cl-. Use HYP-0071 instead.
        ("- [[HYP-0011 GABA_Cl- (NKCC1_KCC2) imbalance]] — hypothesis record",
         "- [[HYP-0071 Brainstem_pons hypoplasia + GABA developmental switch failure]] — closest canonical hypothesis (covers GABA developmental switch)"),
    ],
}


def main():
    total = 0
    for fname, fixlist in FIXES.items():
        path = VAULT / fname
        text = path.read_text()
        original = text
        applied = 0
        for old, new in fixlist:
            if old in text:
                text = text.replace(old, new)
                applied += 1
            else:
                print(f"  WARN: {fname}: pattern not found: {old[:60]}...")
        if text != original:
            path.write_text(text)
            total += applied
            print(f"Updated {fname}: {applied} fixes")
    print(f"\nTotal wikilink fixes: {total}")


if __name__ == "__main__":
    main()
