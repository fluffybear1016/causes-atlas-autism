#!/usr/bin/env python3
"""Fix PMID errors in newly-added international researcher pages.

All corrected PMIDs verified against PubMed esummary.
"""
from pathlib import Path

VAULT = Path("/sessions/jolly-determined-darwin/mnt/Autism/vault/researchers")

FIXES = [
    # Kato 2000 mito bipolar
    ("11167002", "11256685"),
    # Honda 2005 MMR
    ("15858242", "15877763"),
    # Gillberg/Cederlund 2005 -> 2004 actually
    ("16113843", "15473168"),
    # Dziobek 2006 MASC
    ("16868840", "16755332"),
    # Dziobek 2008
    ("17915214", "17990089"),
    # Gillberg 2010 ESSENCE
    ("20371160", "20634041"),
    # Anckarsäter CATSS
    ("21223434", "22506305"),
    # Dinstein 2011 Neuron
    ("21278241", "21689606"),
    # Sandin 2012 maternal age
    ("22916015", "22525954"),
    # Bolte 2014 RATSS
    ("23892712", "24735654"),
    # Lundström 2015 BMJ
    ("25922072", "25922345"),
    # Dinstein 2015 Trends Cogn Sci
    ("26052920", "25979849"),
    # Bourgeron 2015 Nat Rev Neurosci
    ("26077438", "26289574"),
    # Kato/Nishioka 2023 mol psychiatry mosaic
    ("37156942", "37248276"),
]

# Also fix journal claims that were wrong
JOURNAL_FIXES = {
    "15473168": ("J Autism Dev Disord", "Dev Med Child Neurol"),  # Cederlund 2004
}

# Author order fix for the Kato 2023 mosaic paper — first author is Nishioka, not Kataoka
TEXT_FIXES = {
    "Kato_Tadafumi.md": [
        ("Kataoka M, Matoba N, Sawada T, Kazuno AA, Ishiwata M, Fujii K, Matsuo K, Takata A, Kato T. 2023",
         "Nishioka M, Kazuno AA, Iwamoto K, Bundo M, Kato T, Takata A, et al. 2023"),
    ],
}


def main():
    total = 0
    for page in sorted(VAULT.glob("*.md")):
        text = page.read_text()
        original = text
        for old, new in FIXES:
            text = text.replace(f"[PMID {old}]", f"[PMID {new}]")
            text = text.replace(f"pubmed.ncbi.nlm.nih.gov/{old}/", f"pubmed.ncbi.nlm.nih.gov/{new}/")
        for new_pmid, (old_journal, new_journal) in JOURNAL_FIXES.items():
            lines = text.split('\n')
            for i, line in enumerate(lines):
                if f"PMID {new_pmid}" in line and f"*{old_journal}*" in line:
                    lines[i] = line.replace(f"*{old_journal}*", f"*{new_journal}*")
            text = '\n'.join(lines)
        if page.name in TEXT_FIXES:
            for old, new in TEXT_FIXES[page.name]:
                if old in text:
                    text = text.replace(old, new)
        if text != original:
            page.write_text(text)
            n = sum(1 for old, new in FIXES if f"[PMID {new}]" in text and f"[PMID {old}]" in original)
            total += n
            print(f"Updated {page.name}")
    print(f"Total fixes: {total}")


if __name__ == "__main__":
    main()
