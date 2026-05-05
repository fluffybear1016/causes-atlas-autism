#!/usr/bin/env python3
"""Fix all PMID errors in PHE-0001 through PHE-0007 deep-dive pages.

All corrected PMIDs verified against PubMed esummary in this session.
"""
import re
from pathlib import Path

VAULT = Path("/sessions/jolly-determined-darwin/mnt/Autism/vault/topics/phenotypes")

# (old_pmid, new_pmid, journal_correction_optional, year_correction_optional)
FIXES = [
    # PHE-0001
    ("16207918", "15888699", None, None),  # Ramaekers 2005 NEJM
    ("17560158", "18461502", None, None),  # Ramaekers 2007 Neuropediatrics
    ("29274926", "29394471", None, None),  # Quadros 2018 Autism Res

    # PHE-0002
    ("21577169", "21289536", None, None),  # Frye + Rossignol 2011 Pediatr Res

    # PHE-0003
    ("20471091", "20674603", None, None),  # Morgan 2010 Biol Psychiatry
    ("21277364", "20705131", None, None),  # Ashwood 2011 Brain Behav Immun
    ("20148275", "20414802", "J Autism Dev Disord", None),  # Atladottir 2010 - was Pediatrics, actually JADD

    # PHE-0004
    ("16950528", "16950524", None, None),  # MacFabe 2007
    ("21858229", "21949732", None, None),  # Williams 2011 PLoS One
    ("22251724", "22233678", None, None),  # Williams 2012 mBio
    ("30971155", "30967657", None, None),  # Kang 2019 Sci Rep

    # PHE-0005
    ("21135472", "21047224", None, None),  # Krueger 2010 NEJM
    ("22810587", "22763451", None, None),  # Tsai 2012 Nature
    ("25577400", "25916396", None, None),  # Tilot 2015
    ("26077438", "26289574", None, None),  # Bourgeron 2015
    ("26472759", "26472761", None, None),  # Sahin Sur 2015 Science

    # PHE-0006
    ("9114013", "9144249", None, None),    # Comery 1997 PNAS
    ("10982861", "11007554", None, None),  # Irwin 2000 Cereb Cortex
    ("15165737", "15219735", None, None),  # Bear Huber Warren 2004 Trends Neurosci
    ("26819194", "26764156", None, None),  # Berry-Kravis 2016 Sci Transl Med
    ("28694768", "28596820", None, None),  # Ethridge 2017 Mol Autism

    # PHE-0007
    ("23192802", "23233021", None, None),  # Lemonnier 2012 bumetanide RCT
    ("28418403", "28485727", None, None),  # Lemonnier 2017 replication
    ("23022711", "23360806", None, None),  # Sgado 2013 Exp Neurol
    ("24503854", "24503856", None, None),  # Tyzio 2014 Science
    ("26843281", "26711497", None, None),  # Robertson 2016 Curr Biol
]

# Note for Atladottir: change journal too — was claimed Pediatrics, actually J Autism Dev Disord
# Also Ethridge 2017 — was Transl Psychiatry, actually Mol Autism

JOURNAL_FIXES = {
    "20414802": ("Pediatrics", "J Autism Dev Disord"),  # in PHE-0003 we cited Pediatrics
    "28596820": ("Transl Psychiatry", "Mol Autism"),    # in PHE-0006 we cited Transl Psychiatry
}


def main():
    total_fixes = 0
    for page_path in sorted(VAULT.glob("PHE-*.md")):
        text = page_path.read_text()
        original = text
        for old, new, _, _ in FIXES:
            # Replace in link text [PMID OLD] and URL pubmed.ncbi.nlm.nih.gov/OLD/
            text = text.replace(f"[PMID {old}]", f"[PMID {new}]")
            text = text.replace(f"pubmed.ncbi.nlm.nih.gov/{old}/", f"pubmed.ncbi.nlm.nih.gov/{new}/")
        # Apply journal fixes selectively per-paper
        for new_pmid, (old_journal, new_journal) in JOURNAL_FIXES.items():
            # only fix lines containing this specific PMID
            lines = text.split('\n')
            for i, line in enumerate(lines):
                if f"PMID {new_pmid}" in line and f"*{old_journal}*" in line:
                    lines[i] = line.replace(f"*{old_journal}*", f"*{new_journal}*")
            text = '\n'.join(lines)
        if text != original:
            page_path.write_text(text)
            n = sum(1 for old, new, _, _ in FIXES if f"[PMID {new}]" in text and f"[PMID {old}]" in original)
            total_fixes += n
            print(f"Updated {page_path.name}: {n} PMID fixes applied")
    print(f"\nTotal PMID corrections: {total_fixes}")


if __name__ == "__main__":
    main()
