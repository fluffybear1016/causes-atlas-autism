---
type: gene_index
---

# Genes — Index

All 1564 genes in the atlas. Per spec, individual gene notes are not generated (would be 1,500+ files of pure noise).

## Dataview

```dataview
TABLE gene_symbol, sfari_score, genetic_evidence_strength, opentargets_score, function_summary
FROM "genes"
WHERE type = "gene_index"
```

*(The Dataview block above is a placeholder; the static table below is the deterministic dump of `v2.0_scored/genes.csv`, sorted by gene id.)*

## Static table

| ID | Symbol | SFARI | Genetic evidence | OpenTargets | DisGeNET | Function |
|----|--------|-------|------------------|-------------|----------|----------|
| GEN-0001 | FOLR1 | S | 4 | 0.62 |  | Folate receptor 1; transports folate across blood-brain barrier; target of autoantibodies in cerebral folate deficiency. |
| GEN-0002 | MTHFR | 3 | 3 | 0.45 |  | Methylenetetrahydrofolate reductase; common C677T variant reduces enzyme activity; affects folate metabolism and methylation. |
| GEN-0003 | SHANK3 | 1 | 5 | 0.5283 |  | Postsynaptic scaffolding protein; haploinsufficiency causes Phelan-McDermid syndrome; ~75% of carriers have ASD. |
| GEN-0004 | MECP2 | S | 5 | 0.4929 |  | Methyl-CpG binding protein; loss-of-function causes Rett syndrome; gain-of-function causes MECP2 duplication syndrome. |
| GEN-0005 | FMR1 | S | 5 | 0.85 |  | Fragile X mental retardation 1; CGG expansion silences gene; ~50% of Fragile X individuals meet ASD criteria. |
| GEN-0006 | TSC1 | S | 5 | 0.83 |  | Tuberous sclerosis 1; mTOR pathway negative regulator; TSC variants ~50% have ASD. |
| GEN-0007 | TSC2 | S | 5 | 0.4385 |  | Tuberous sclerosis 2; mTOR pathway negative regulator; TSC variants ~50% have ASD. |
| GEN-0008 | PTEN | 1 | 4 | 0.3679 |  | Phosphatase and tensin homolog; mTOR pathway regulator; PTEN variants associated with macrocephaly + autism. |
| GEN-0009 | CHD8 | 1 | 5 | 0.7932 |  | Chromodomain helicase DNA binding protein 8; one of the most frequently disrupted genes in autism; macrocephaly + GI symptoms common. |
| GEN-0010 | NRF2 (NFE2L2) | Not in SFARI | 3 | 0.41 |  | Nuclear factor erythroid 2-related factor 2; master regulator of antioxidant response; activated by sulforaphane. |
| GEN-0011 | ABAT | 2 | 2 |  |  | 4-aminobutyrate aminotransferase |
| GEN-0012 | ABCA10 | 2 | 1 |  |  | ATP-binding cassette, sub-family A (ABC1), member 10 |
| GEN-0013 | ABCA13 | 2 | 4 |  |  | ATP binding cassette subfamily A member 13 |
| GEN-0014 | ABCA2 | 3 | 2 |  |  | ATP binding cassette subfamily A member 2 |
| GEN-0015 | ABCA7 | 2 | 2 |  |  | ATP-binding cassette, sub-family A (ABC1), member 7 |
| GEN-0016 | ABCE1 | 1 | 2 |  |  | ATP binding cassette subfamily E member 1 |
| GEN-0017 | ABL2 | 3 | 3 |  |  | ABL proto-oncogene 2, non-receptor tyrosine kinase |
| GEN-0018 | ACAP2 | 2 | 2 |  |  | ArfGAP with coiled-coil, ankyrin repeat and PH domains 2 |
| GEN-0019 | ACE | 2 | 2 |  |  | angiotensin I converting enzyme |
| GEN-0020 | ACHE | 2 | 2 | 0.2954 |  | Acetylcholinesterase (Yt blood group) |
| GEN-0021 | ACTB | S | 3 |  |  | actin beta |
| GEN-0022 | ACTL6B | S | 4 | 0.5215 |  | actin like 6B |
| GEN-0023 | ACTN4 | 2 | 2 |  |  | actinin alpha 4 |
| GEN-0024 | ACY1 | S | 3 |  |  | aminoacylase 1 |
| GEN-0025 | ADA | 2 | 2 |  |  | adenosine deaminase |
| GEN-0026 | ADCY1 | 3 | 1 |  |  | adenylate cyclase 1 |
| GEN-0027 | ADCY3 | 2 | 1 |  |  | adenylate cyclase 3 |
| GEN-0028 | ADCY5 | 2 | 3 |  |  | Adenylate cyclase 5 |
| GEN-0029 | ADGRB1 | 3 | 3 |  |  | adhesion G protein-coupled receptor B1 |
| GEN-0030 | ADGRL1 | S | 2 |  |  | adhesion G protein-coupled receptor L1 |
| GEN-0031 | ADK | 2 | 1 |  |  | adenosine kinase |
| GEN-0032 | ADNP | S | 5 | 0.3541 |  | Activity-dependent neuroprotector homeobox |
| GEN-0033 | ADORA3 | 2 | 1 |  |  | Adenosine A3 receptor |
| GEN-0034 | ADSL | S | 2 |  |  | adenylosuccinate lyase |
| GEN-0035 | ADSS2 | 2 | 1 |  |  | adenylosuccinate synthase 2 |
| GEN-0036 | AFF2 | 1 | 5 |  |  | AF4/FMR2 family, member 2 |
| GEN-0037 | AGAP1 | 2 | 3 |  |  | ArfGAP with GTPase domain, ankyrin repeat and PH domain 1 |
| GEN-0038 | AGAP2 | 2 | 2 |  |  | ArfGAP with GTPase domain, ankyrin repeat and PH domain 2 |
| GEN-0039 | AGAP5 | 3 | 1 |  |  | ArfGAP with GTPase domain, ankyrin repeat and PH domain 5 |
| GEN-0040 | AGBL4 | 2 | 2 |  |  | ATP/GTP binding protein-like 4 |
| GEN-0041 | AGMO | 2 | 2 |  |  | alkylglycerol monooxygenase |
| GEN-0042 | AGO1 | 2 | 4 |  |  | argonaute 1, RISC catalytic component |
| GEN-0043 | AGO2 | S | 1 |  |  | argonaute RISC catalytic component 2 |
| GEN-0044 | AGO3 | 2 | 3 |  |  | argonaute RISC catalytic component 3 |
| GEN-0045 | AGO4 | 2 | 2 |  |  | argonaute RISC catalytic component 4 |
| GEN-0046 | AGTR2 | 2 | 2 |  |  | angiotensin II receptor, type 2 |
| GEN-0047 | AHDC1 | S | 5 |  |  | AT-hook DNA binding motif containing 1 |
| GEN-0048 | AHI1 | S | 5 |  |  | Abelson helper integration site 1 |
| GEN-0049 | AHNAK | 2 | 2 |  |  | AHNAKnucleoprotein |
| GEN-0050 | AKAP9 | 2 | 3 |  |  | A kinase (PRKA) anchor protein 9 |
| GEN-0051 | ALDH1A3 | S | 2 | 0.2712 |  | aldehyde dehydrogenase 1 family member A3 |
| GEN-0052 | ALDH1L1 | 3 | 2 |  |  | aldehyde dehydrogenase 1 family member L1 |
| GEN-0053 | ALDH5A1 | S | 5 | 0.2882 |  | aldehyde dehydrogenase 5 family, member A1 (succinate-semialdehyde dehydrogenase ) |
| GEN-0054 | ALG6 | S | 1 |  |  | ALG6, alpha-1,3-glucosyltransferase |
| GEN-0055 | AMPD1 | 2 | 2 | 0.1869 |  | Adenosine monophosphate deaminase 1 |
| GEN-0056 | AMT | 2 | 1 |  |  | Aminomethyltransferase |
| GEN-0057 | ANK2 | 1 | 5 | 0.3826 |  | Ankyrin 2, neuronal |
| GEN-0058 | ANK3 | 1 | 5 | 0.3073 |  | ankyrin 3 |
| GEN-0059 | ANKRD11 | S | 5 | 0.236 |  | ankyrin repeat domain 11 |
| GEN-0060 | ADORA2A | 2 | 2 |  |  | adenosine A2a receptor |
| GEN-0061 | ANKRD17 | S | 2 |  |  | ankyrin repeat domain 17 |
| GEN-0062 | ANKS1B | S | 2 | 0.2462 |  | ankyrin repeat and sterile alpha motif domain containing 1B |
| GEN-0063 | ANP32A | 1 | 2 |  |  | acidic nuclear phosphoprotein 32 family member A |
| GEN-0064 | ANXA1 | 2 | 1 |  |  | Annexin A1 |
| GEN-0065 | AP1S2 | S | 2 |  |  | adaptor related protein complex 1 sigma 2 subunit |
| GEN-0066 | AP2M1 | 2 | 3 |  |  | adaptor related protein complex 2 subunit mu 1 |
| GEN-0067 | AP2S1 | 1 | 2 |  |  | adaptor related protein complex 2 subunit sigma 1 |
| GEN-0068 | APBA2 | 2 | 3 |  |  | amyloid beta (A4) precursor protein-binding, family A, member 2 |
| GEN-0069 | ADRB2 | 2 | 3 |  |  | adrenergic, beta-2-, receptor, surface |
| GEN-0070 | APBB1 | 2 | 2 |  |  | amyloid beta precursor protein binding family B member 1 |
| GEN-0071 | APH1A | 2 | 1 |  |  | APH1A gamma secretase subunit |
| GEN-0072 | AR | 2 | 3 |  |  | androgen receptor |
| GEN-0073 | ARF3 | 1 | 2 | 0.2661 |  | ADP ribosylation factor 3 |
| GEN-0074 | ARHGAP11B | 2 | 1 |  |  | Rho GTPase activating protein 11B |
| GEN-0075 | ARHGAP30 | 3 | 1 |  |  | Rho GTPase activating protein 30 |
| GEN-0076 | ARHGAP32 | 2 | 3 |  |  | Rho GTPase activating protein 32 |
| GEN-0077 | ARHGAP5 | 2 | 2 |  |  | Rho GTPase activating protein 5 |
| GEN-0078 | ARHGEF10 | 2 | 2 |  |  | Rho guanine nucleotide exchange factor 10 |
| GEN-0079 | ARHGEF2 | 3 | 2 |  |  | Rho/Rac guanine nucleotide exchange factor 2 |
| GEN-0080 | ARHGEF9 | S | 5 | 0.1614 |  | Cdc42 guanine nucleotide exchange factor (GEF) 9 |
| GEN-0081 | ARID1A | S | 2 |  |  | AT-rich interaction domain 1A |
| GEN-0082 | ARID1B | S | 5 | 0.4535 |  | AT-rich interaction domain 1B |
| GEN-0083 | ARID2 | S | 5 |  |  | AT-rich interaction domain 2 |
| GEN-0084 | ARNT2 | 2 | 4 |  |  | aryl-hydrocarbon receptor nuclear translocator 2 |
| GEN-0085 | ARX | S | 5 |  |  | aristaless related homeobox |
| GEN-0086 | ASAP2 | 2 | 2 |  |  | ArfGAP with SH3 domain, ankyrin repeat and PH domain 2 |
| GEN-0087 | ASB11 | 3 | 2 |  |  | ankyrin repeat and SOCS box containing 11 |
| GEN-0088 | ASB14 | 2 | 2 |  |  | ankyrin repeat and SOCS box containing 14 |
| GEN-0089 | ASH1L | 1 | 5 | 0.2907 |  | Ash1 (absent, small, or homeotic)-like (Drosophila) |
| GEN-0090 | ASMT | 2 | 3 |  |  | acetylserotonin O-methyltransferase |
| GEN-0091 | ASPM | 2 | 4 |  |  | abnormal spindle microtubule assembly |
| GEN-0092 | ASTN2 | 2 | 4 |  |  | astrotactin 2 |
| GEN-0093 | ASXL3 | S | 5 | 0.4647 |  | Additional sex combs like 3 (Drosophila) |
| GEN-0094 | ATP10A | 2 | 3 | 0.3356 |  | Probable phospholipid-transporting ATPase VA |
| GEN-0095 | ATP1A1 | S | 3 |  |  | ATPase Na+/K+ transporting subunit alpha 1 |
| GEN-0096 | ATP1A3 | S | 5 |  |  | ATPase Na+/K+ transporting subunit alpha 3 |
| GEN-0097 | ATP2B1 | S | 1 | 0.2587 |  | ATPase plasma membrane Ca2+ transporting 1 |
| GEN-0098 | ATP2B2 | 2 | 4 |  |  | ATPase, Ca++ transporting, plasma membrane 2 |
| GEN-0099 | ATP6V0A2 | 2 | 2 |  |  | ATPase H+ transporting V0 subunit a2 |
| GEN-0100 | ATP9A | S | 2 |  |  | ATPase phospholipid transporting 9A |
| GEN-0101 | ATRX | 1 | 5 |  |  | alpha thalassemia/mental retardation syndrome X-linked |
| GEN-0102 | ATXN2 | 3 | 1 |  |  | ataxin 2 |
| GEN-0103 | AUTS2 | 1 | 5 | 0.4887 |  | activator of transcription and developmental regulatorAUTS2 |
| GEN-0104 | AVPR1A | 2 | 4 | 0.3597 |  | arginine vasopressin receptor 1A |
| GEN-0105 | AZGP1 | 2 | 1 |  |  | alpha-2-glycoprotein 1, zinc-binding |
| GEN-0106 | BACE1 | 3 | 1 |  |  | beta-secretase 1 |
| GEN-0107 | BAIAP2L1 | 3 | 2 |  |  | BAR/IMD domain containing adaptor protein 2 like 1 |
| GEN-0108 | BAZ2B | 1 | 2 |  |  | bromodomain adjacent to zinc finger domain 2B |
| GEN-0109 | BBS4 | 2 | 2 |  |  | Bardet-Biedl syndrome 4 |
| GEN-0110 | BCAS1 | 2 | 2 |  |  | breast carcinoma amplified sequence 1 |
| GEN-0111 | BCKDK | 1 | 3 |  |  | Branched chain ketoacid dehydrogenase kinase |
| GEN-0112 | BCL11A | S | 5 | 0.3403 |  | B-cell CLL/lymphoma 11A (zinc finger protein) |
| GEN-0113 | BCL11B | 3 | 3 | 0.4232 |  | BCL11 transcription factor B |
| GEN-0114 | BCORL1 | S | 3 |  |  | BCL6 corepressor like 1 |
| GEN-0115 | BICRA | S | 2 |  |  | BRD4 interacting chromatin remodeling complex associated protein |
| GEN-0116 | BIRC6 | 2 | 4 | 0.333 |  | Baculoviral IAP repeat containing 6 |
| GEN-0117 | BRAF | S | 5 |  |  | v-raf murine sarcoma viral oncogene homolog B |
| GEN-0118 | BRCA2 | 2 | 3 |  |  | breast cancer 2, early onset |
| GEN-0119 | BRD4 | 2 | 3 |  |  | bromodomain containing 4 |
| GEN-0120 | BRINP3 | 3 | 1 |  |  | BMP/retinoic acid inducible neural specific 3 |
| GEN-0121 | BRSK2 | S | 4 | 0.4484 |  | BR serine/threonine kinase 2 |
| GEN-0122 | BRWD3 | S | 3 |  |  | bromodomain and WD repeat domain containing 3 |
| GEN-0123 | BSN | 3 | 3 |  |  | bassoon presynaptic cytomatrix protein |
| GEN-0124 | BST1 | 2 | 2 |  |  | bone marrow stromal cell antigen 1 |
| GEN-0125 | BTAF1 | 2 | 3 |  |  | RNA polymerase II, B-TFIID transcription factor-associated, 170kDa (Mot1 homolog, S. cerevisiae) |
| GEN-0126 | BTRC | 2 | 1 |  |  | beta-transducin repeat containing E3 ubiquitin protein ligase |
| GEN-0127 | C12orf57 | S | 4 |  |  | Chromosome 12 open reading frame 57 |
| GEN-0128 | C15orf62 | 2 | 1 |  |  | chromosome 15 open reading frame 62 |
| GEN-0129 | C4B | 2 | 2 |  |  | complement component 4B |
| GEN-0130 | CA6 | 2 | 2 |  |  | carbonic anhydrase VI |
| GEN-0131 | CACNA1A | S | 5 |  |  | Calcium channel, voltage-dependent, P/Q type, alpha 1A subunit |
| GEN-0132 | ASB9 | 3 | 1 |  |  | ankyrin repeat and SOCS box containing 9 |
| GEN-0133 | AVPR1B | 2 | 2 | 0.2512 |  | arginine vasopressin receptor 1B |
| GEN-0134 | BICDL1 | 2 | 1 |  |  | BICD family like cargo adaptor 1 |
| GEN-0135 | CACNA1B | 2 | 4 |  |  | calcium voltage-gated channel subunit alpha1 B |
| GEN-0136 | CACNA1C | S | 5 | 0.4278 |  | calcium channel, voltage-dependent, L type, alpha 1C subunit |
| GEN-0137 | CACNA1D | 2 | 4 |  |  | calcium channel, voltage-dependent, L type, alpha 1D |
| GEN-0138 | CACNA1E | 1 | 5 |  |  | calcium voltage-gated channel subunit alpha1 E |
| GEN-0139 | CACNA1F | 2 | 3 |  |  | calcium channel, voltage-dependent, alpha 1F |
| GEN-0140 | CACNA1G | 2 | 4 |  |  | calcium channel, voltage-dependent, T type, alpha 1G subunit |
| GEN-0141 | CACNA1H | 2 | 4 |  |  | calcium channel, voltage-dependent, alpha 1H subunit |
| GEN-0142 | CACNA1I | 2 | 3 | 0.3863 |  | Calcium channel, voltage-dependent, T type, alpha 1I subunit |
| GEN-0143 | CACNA2D1 | 2 | 3 |  |  | calcium voltage-gated channel auxiliary subunit alpha2delta 1 |
| GEN-0144 | CACNA2D3 | 1 | 4 |  |  | Calcium channel, voltage-dependent, alpha 2/delta subunit 3 |
| GEN-0145 | CACNB1 | 3 | 1 |  |  | calcium voltage-gated channel auxiliary subunit beta 1 |
| GEN-0146 | CACNB2 | 2 | 3 | 0.242 |  | Calcium channel, voltage-dependent, beta 2 subunit |
| GEN-0147 | CACNG2 | 2 | 2 |  |  | calcium voltage-gated channel auxiliary subunit gamma 2 |
| GEN-0148 | CADM1 | 2 | 3 |  |  | cell adhesion molecule 1 |
| GEN-0149 | CADM2 | 2 | 2 | 0.2917 |  | Cell adhesion molecule 2 |
| GEN-0150 | CADPS | 2 | 2 | 0.2428 |  | calcium dependent secretion activator |
| GEN-0151 | CADPS2 | 2 | 3 |  |  | Ca2+-dependent activator protein for secretion 2 |
| GEN-0152 | CAMK2A | S | 4 |  |  | calcium/calmodulin dependent protein kinase II alpha |
| GEN-0153 | CAMK2B | S | 3 |  |  | calcium/calmodulin dependent protein kinase II beta |
| GEN-0154 | CAMK2D | S | 1 |  |  | calcium/calmodulin dependent protein kinase II delta |
| GEN-0155 | CAMK4 | 2 | 2 | 0.4661 |  | calcium/calmodulin dependent protein kinase IV |
| GEN-0156 | CAMTA2 | 1 | 1 |  |  | calmodulin binding transcription activator 2 |
| GEN-0157 | CAPN12 | 2 | 2 |  |  | Calpain 12 |
| GEN-0158 | CAPRIN1 | 1 | 2 | 0.2702 |  | Cell cycle associated protein 1 |
| GEN-0159 | CAPZA2 | 3 | 1 |  |  | capping actin protein of muscle Z-line subunit alpha 2 |
| GEN-0160 | CARD11 | 2 | 1 |  |  | caspase recruitment domain family member 11 |
| GEN-0161 | CASK | 1 | 5 |  |  | calcium/calmodulin dependent serine protein kinase |
| GEN-0162 | CASKIN1 | 2 | 2 |  |  | CASK interacting protein 1 |
| GEN-0163 | CASZ1 | 1 | 3 |  |  | castor zinc finger 1 |
| GEN-0164 | CAT | 3 | 1 |  |  | catalase |
| GEN-0165 | CBX1 | S | 1 |  |  | chromobox 1 |
| GEN-0166 | CBX4 | 3 | 1 |  |  | chromobox 4 |
| GEN-0167 | CC2D1A | 2 | 4 | 0.2627 |  | Coiled-coil and C2 domain containing 1A |
| GEN-0168 | CCDC88C | 2 | 3 |  |  | Coiled-coil domain containing 88C |
| GEN-0169 | CCDC91 | 2 | 2 |  |  | coiled-coil domain containing 91 |
| GEN-0170 | CCIN | 2 | 1 |  |  | calicin |
| GEN-0171 | CCNG1 | 2 | 1 |  |  | cyclin G1 |
| GEN-0172 | CCNK | S | 2 |  |  | cyclin K |
| GEN-0173 | CCSER1 | 2 | 1 |  |  | coiled-coil serine rich protein 1 |
| GEN-0174 | CCT4 | 2 | 1 |  |  | Chaperonin containing TCP1, subunit 4 (delta) |
| GEN-0175 | CD276 | 2 | 1 |  |  | CD276molecule |
| GEN-0176 | CD38 | 2 | 3 |  |  | CD38 molecule |
| GEN-0177 | CDC42BPB | 2 | 3 | 0.296 |  | CDC42 binding protein kinase beta (DMPK-like) |
| GEN-0178 | CDH10 | 2 | 3 |  |  | cadherin 10, type 2 (T2-cadherin) |
| GEN-0179 | CDH11 | 2 | 2 |  |  | cadherin 11 |
| GEN-0180 | CDH13 | 2 | 2 |  |  | cadherin 13 |
| GEN-0181 | CDH2 | S | 2 |  |  | cadherin 2 |
| GEN-0182 | CDH22 | 2 | 2 |  |  | cadherin-like 22 |
| GEN-0183 | CDH8 | 2 | 3 | 0.3506 |  | cadherin 8, type 2 |
| GEN-0184 | CDH9 | 2 | 2 |  |  | cadherin 9, type 2 (T1-cadherin) |
| GEN-0185 | CDK13 | S | 5 | 0.341 |  | cyclin dependent kinase 13 |
| GEN-0186 | CDK16 | 2 | 1 |  |  | cyclin dependent kinase 16 |
| GEN-0187 | CDK19 | S | 2 |  |  | cyclin dependent kinase 19 |
| GEN-0188 | CDK5RAP2 | 3 | 3 |  |  | CDK5 regulatory subunit associated protein 2 |
| GEN-0189 | CDK8 | S | 2 |  |  | cyclin dependent kinase 8 |
| GEN-0190 | CDKL5 | S | 5 | 0.4133 |  | cyclin-dependent kinase-like 5 |
| GEN-0191 | CDON | 3 | 2 |  |  | cell adhesion associated, oncogene regulated |
| GEN-0192 | CECR2 | 2 | 1 |  |  | CECR2, histone acetyl-lysine reader |
| GEN-0193 | CELF2 | S | 2 |  |  | CUGBP Elav-like family member 2 |
| GEN-0194 | CELF4 | 1 | 4 |  |  | CUGBP, Elav-like family member 4 |
| GEN-0195 | CELF6 | 2 | 2 |  |  | CUGBP, Elav-like family member 6 |
| GEN-0196 | CEP135 | 2 | 2 |  |  | centrosomal protein 135 |
| GEN-0197 | CEP290 | S | 4 |  |  | Centrosomal protein 290kDa |
| GEN-0198 | CEP41 | 2 | 2 |  |  | testis specific, 14 |
| GEN-0199 | CERT1 | S | 2 |  |  | ceramide transporter 1 |
| GEN-0200 | CGNL1 | 2 | 2 |  |  | Cingulin-like 1 |
| GEN-0201 | CHAMP1 | S | 5 |  |  | chromosome alignment maintaining phosphoprotein 1 |
| GEN-0202 | CHD1 | S | 4 |  |  | chromodomain helicase DNA binding protein 1 |
| GEN-0203 | CHD2 | S | 5 | 0.4926 |  | Chromodomain helicase DNA binding protein 2 |
| GEN-0204 | CD99L2 | 2 | 1 |  |  | CD99 molecule like 2 |
| GEN-0205 | CHD3 | S | 5 |  |  | chromodomain helicase DNA binding protein 3 |
| GEN-0206 | CHD4 | S | 2 |  |  | chromodomain helicase DNA binding protein 4 |
| GEN-0207 | CHD7 | S | 5 |  |  | chromodomain helicase DNA binding protein 7 |
| GEN-0208 | CHD9 | 3 | 2 |  |  | chromodomain helicase DNA binding protein 9 |
| GEN-0209 | CHKB | S | 3 |  |  | Choline kinase beta |
| GEN-0210 | CHM | 3 | 2 |  |  | CHMRab escort protein |
| GEN-0211 | CHMP1A | 2 | 2 |  |  | charged multivesicular body protein 1A |
| GEN-0212 | CHRM3 | 2 | 2 |  |  | cholinergic receptor muscarinic 3 |
| GEN-0213 | CHRNA7 | 2 | 4 |  |  | cholinergic receptor, nicotinic, alpha 7 |
| GEN-0214 | CHRNB3 | 2 | 1 |  |  | cholinergic receptor nicotinic beta 3 subunit |
| GEN-0215 | CHST2 | 3 | 1 |  |  | carbohydrate sulfotransferase 2 |
| GEN-0216 | CIB2 | 2 | 1 |  |  | Calcium and integrin binding family member 2 |
| GEN-0217 | CIC | 1 | 5 | 0.2827 |  | capicua transcriptional repressor |
| GEN-0218 | CLASP1 | 2 | 2 |  |  | cytoplasmic linker associated protein 1 |
| GEN-0219 | CLCN4 | S | 4 |  |  | chloride voltage-gated channel 4 |
| GEN-0220 | CLIP2 | 3 | 1 |  |  | CAP-Gly domain containing linker protein 2 |
| GEN-0221 | CLN8 | 2 | 2 |  |  | Ceroid-lipofuscinosis, neuronal 8 (epilepsy, progressive with mental retardation) |
| GEN-0222 | CLTC | 3 | 2 |  |  | clathrin heavy chain |
| GEN-0223 | CLTCL1 | 2 | 2 |  |  | clathrin, heavy chain-like 1 |
| GEN-0224 | CMIP | 2 | 2 |  |  | c-Maf inducing protein |
| GEN-0225 | CMPK2 | 2 | 1 |  |  | cytidine/uridine monophosphate kinase 2 |
| GEN-0226 | CNGB3 | 2 | 2 |  |  | cyclic nucleotide gated channel beta 3 |
| GEN-0227 | CNKSR2 | S | 4 | 0.2785 |  | connector enhancer of kinase suppressor of Ras 2 |
| GEN-0228 | CNOT1 | S | 3 | 0.244 |  | CCR4-NOT transcription complex subunit 1 |
| GEN-0229 | CNOT3 | S | 5 |  |  | CCR4-NOT transcription complex subunit 3 |
| GEN-0230 | CNR1 | 2 | 2 | 0.2291 |  | cannabinoid receptor 1 (brain) |
| GEN-0231 | CNTN3 | 2 | 2 |  |  | contactin 3 |
| GEN-0232 | CNTN4 | 2 | 4 | 0.3853 |  | contactin 4 |
| GEN-0233 | CNTN5 | 2 | 3 |  |  | Contactin 5 |
| GEN-0234 | CNTN6 | 2 | 4 | 0.2691 |  | Contactin 6 |
| GEN-0235 | CNTNAP2 | S | 5 | 0.5939 |  | contactin associated protein-like 2 |
| GEN-0236 | CNTNAP3 | 2 | 2 |  |  | contactin associated protein-like 3 |
| GEN-0237 | CNTNAP4 | 2 | 4 |  |  | Contactin associated protein-like 4 |
| GEN-0238 | CNTNAP5 | 2 | 4 |  |  | contactin associated protein-like 5 |
| GEN-0239 | COL12A1 | 3 | 2 |  |  | collagen type XII alpha 1 chain |
| GEN-0240 | COL28A1 | 2 | 2 |  |  | collagen type XXVIII alpha 1 chain |
| GEN-0241 | CORO1A | 1 | 1 | 0.1477 |  | coronin 1A |
| GEN-0242 | CPEB4 | 2 | 1 |  |  | cytoplasmic polyadenylation element binding protein 4 |
| GEN-0243 | CPSF7 | 1 | 2 |  |  | cleavage and polyadenylation specific factor 7 |
| GEN-0244 | CPT2 | 2 | 2 |  |  | carnitine palmitoyltransferase 2 |
| GEN-0245 | CPZ | 2 | 2 |  |  | carboxypeptidase Z |
| GEN-0246 | CREBBP | S | 5 |  |  | CREB binding protein |
| GEN-0247 | CRMP1 | 3 | 2 |  |  | collapsin response mediator protein 1 |
| GEN-0248 | CSDE1 | S | 2 | 0.3746 |  | cold shock domain containing E1 |
| GEN-0249 | CSMD1 | 2 | 4 | 0.4141 |  | CUB and Sushi multiple domains 1 |
| GEN-0250 | CSMD2 | 3 | 2 |  |  | CUB and Sushi multiple domains 2 |
| GEN-0251 | CSMD3 | 3 | 3 |  |  | CUB and Sushi multiple domains 3 |
| GEN-0252 | CSNK1E | 2 | 2 |  |  | casein kinase 1 epsilon |
| GEN-0253 | CSNK1G1 | S | 2 | 0.3721 |  | casein kinase 1 gamma 1 |
| GEN-0254 | CSNK2A1 | S | 5 | 0.2686 |  | casein kinase 2 alpha 1 |
| GEN-0255 | CSNK2B | S | 3 | 0.2894 |  | casein kinase 2 beta |
| GEN-0256 | CTCF | S | 5 | 0.1508 |  | CCCTC-binding factor |
| GEN-0257 | CTNNA2 | S | 2 |  |  | catenin alpha 2 |
| GEN-0258 | CTNNA3 | 2 | 4 |  |  | catenin (cadherin-associated protein), alpha 3 |
| GEN-0259 | CTNNB1 | 1 | 5 | 0.296 |  | catenin beta 1 |
| GEN-0260 | CTNND1 | 2 | 1 |  |  | catenin delta 1 |
| GEN-0261 | CTNND2 | 2 | 4 |  |  | Catenin (cadherin-associated protein), delta 2 |
| GEN-0262 | CTPS1 | 3 | 1 |  |  | CTP synthase 1 |
| GEN-0263 | CTR9 | S | 2 |  |  | CTR9homolog, Paf1/RNA polymerase II complex component |
| GEN-0264 | CTTNBP2 | 2 | 4 |  |  | cortactin binding protein 2 |
| GEN-0265 | CUL2 | 3 | 2 |  |  | cullin 2 |
| GEN-0266 | CUL3 | 1 | 5 | 0.4213 |  | Cullin 3 |
| GEN-0267 | CUL4B | S | 2 |  |  | cullin 4B |
| GEN-0268 | CUL7 | 2 | 3 |  |  | Cullin 7 |
| GEN-0269 | CUX1 | 2 | 4 |  |  | cut like homeobox 1 |
| GEN-0270 | CUX2 | S | 4 |  |  | cut like homeobox 2 |
| GEN-0271 | CX3CR1 | 2 | 1 |  |  | Chemokine (C-X3-C motif) receptor 1 |
| GEN-0272 | CXXC5 | 3 | 2 |  |  | CXXC finger protein 5 |
| GEN-0273 | CYFIP1 | 2 | 4 | 0.1534 |  | cytoplasmic FMR1 interacting protein 1 |
| GEN-0274 | CYFIP2 | 3 | 3 |  |  | cytoplasmic FMR1 interacting protein 2 |
| GEN-0275 | CYLC2 | 2 | 1 |  |  | cylicin, basic protein of sperm head cytoskeleton 2 |
| GEN-0276 | CYP11B1 | 2 | 2 |  |  | cytochrome P450, family 11, subfamily B, polypeptide 1 |
| GEN-0277 | CYP27A1 | S | 2 |  |  | cytochrome P450 family 27 subfamily A member 1 |
| GEN-0278 | DAGLA | 2 | 2 |  |  | diacylglycerol lipase alpha |
| GEN-0279 | DAPP1 | 2 | 1 |  |  | Dual adaptor of phosphotyrosine and 3-phosphoinositides |
| GEN-0280 | DCC | 2 | 2 | 0.4562 |  | DCCnetrin 1 receptor |
| GEN-0281 | DDC | 2 | 2 |  |  | dopa decarboxylase |
| GEN-0282 | DDHD2 | 2 | 2 |  |  | DDHD domain containing 2 |
| GEN-0283 | DDX23 | S | 1 |  |  | DEAD-box helicase 23 |
| GEN-0284 | DDX3X | S | 5 |  |  | DEAD (Asp-Glu-Ala-Asp) box helicase 3, X-linked |
| GEN-0285 | DDX53 | 2 | 2 |  |  | DEAD (Asp-Glu-Ala-Asp) box polypeptide 53 |
| GEN-0286 | DEAF1 | S | 5 | 0.4592 |  | DEAF1 transcription factor |
| GEN-0287 | DENND2B | S | 2 |  |  | DENN domain containing 2B |
| GEN-0288 | DENR | 2 | 2 |  |  | density-regulated protein |
| GEN-0289 | DEPDC5 | S | 5 |  |  | DEP domain containing 5 |
| GEN-0290 | DGKI | 3 | 2 | 0.1969 |  | diacylglycerol kinase iota |
| GEN-0291 | DHCR7 | S | 5 |  |  | 7-dehydrocholesterol reductase |
| GEN-0292 | DHX30 | S | 3 | 0.2598 |  | DExH-box helicase 30 |
| GEN-0293 | DHX9 | S | 2 |  |  | DExH-box helicase 9 |
| GEN-0294 | DIP2A | 1 | 4 | 0.3596 |  | DIP2 disco-interacting protein 2 homolog A (Drosophila) |
| GEN-0295 | DIP2C | 2 | 2 |  |  | disco interacting protein 2 homolog C |
| GEN-0296 | DIPK2A | 2 | 1 |  |  | divergent protein kinase domain 2A |
| GEN-0297 | DISC1 | 2 | 4 |  |  | disrupted in schizophrenia 1 |
| GEN-0298 | DIXDC1 | 2 | 2 |  |  | DIX domain containing 1 |
| GEN-0299 | DLG1 | 2 | 2 |  |  | discs large MAGUK scaffold protein 1 |
| GEN-0300 | DLG2 | 2 | 4 |  |  | discs large MAGUK scaffold protein 2 |
| GEN-0301 | DLG4 | 1 | 5 | 0.3425 |  | discs large MAGUK scaffold protein 4 |
| GEN-0302 | DLGAP1 | 2 | 3 |  |  | DLG associated protein 1 |
| GEN-0303 | DLGAP2 | 2 | 4 |  |  | discs, large (Drosophila) homolog-associated protein 2 |
| GEN-0304 | DLGAP3 | 2 | 3 |  |  | DLG associated protein 3 |
| GEN-0305 | DLL1 | S | 2 |  |  | delta like canonical Notch ligand 1 |
| GEN-0306 | DLX3 | 2 | 1 |  |  | distal-less homeobox 3 |
| GEN-0307 | DLX6 | 2 | 3 |  |  | distal-less homeobox 6 |
| GEN-0308 | DMD | S | 5 |  |  | dystrophin (muscular dystrophy, Duchenne and Becker types) |
| GEN-0309 | DMPK | S | 3 |  |  | dystrophia myotonica-protein kinase |
| GEN-0310 | DMWD | 2 | 1 |  |  | DM1 locus, WD repeat containing |
| GEN-0311 | DMXL2 | 2 | 3 | 0.408 |  | Dmx-like 2 |
| GEN-0312 | DNAH10 | 2 | 3 |  |  | Dynein, axonemal, heavy chain 10 |
| GEN-0313 | DNAH17 | 2 | 3 |  |  | dynein axonemal heavy chain 17 |
| GEN-0314 | DNAH3 | 2 | 3 |  |  | dynein axonemal heavy chain 3 |
| GEN-0315 | DNAJC5 | 3 | 2 |  |  | DnaJ heat shock protein family (Hsp40) member C5 |
| GEN-0316 | DNER | 2 | 1 |  |  | Delta/notch-like EGF repeat containing |
| GEN-0317 | DNM1 | 3 | 3 |  |  | dynamin 1 |
| GEN-0318 | DNMT3A | S | 5 | 0.4132 |  | DNA (cytosine-5-)-methyltransferase 3 alpha |
| GEN-0319 | DOCK1 | 2 | 1 |  |  | Dedicator of cytokinesis 1 |
| GEN-0320 | DOCK4 | 2 | 3 |  |  | Dedicator of cytokinesis 4 |
| GEN-0321 | DOCK8 | 2 | 3 |  |  | dedicator of cytokinesis 8 |
| GEN-0322 | DOLK | S | 2 |  |  | dolichol kinase |
| GEN-0323 | DOT1L | S | 2 |  |  | DOT1 like histone lysine methyltransferase |
| GEN-0324 | DPP10 | 2 | 3 |  |  | Dipeptidyl-peptidase 10 |
| GEN-0325 | DPP3 | 2 | 1 |  |  | dipeptidyl peptidase 3 |
| GEN-0326 | DPP4 | 2 | 2 | 0.315 |  | Dipeptidyl-peptidase 4 |
| GEN-0327 | DPP6 | 2 | 4 |  |  | dipeptidyl-peptidase 6 |
| GEN-0328 | DPYD | 2 | 4 | 0.3584 |  | dihydropyrimidine dehydrogenase |
| GEN-0329 | DPYSL2 | 1 | 4 |  |  | dihydropyrimidinase like 2 |
| GEN-0330 | DPYSL3 | 2 | 1 |  |  | dihydropyrimidinase like 3 |
| GEN-0331 | DPYSL5 | 3 | 1 |  |  | dihydropyrimidinase like 5 |
| GEN-0332 | DRD2 | 2 | 4 | 0.7165 |  | Dopamine receptor D2 |
| GEN-0333 | DRD3 | 2 | 2 | 0.3724 |  | dopamine receptor D3 |
| GEN-0334 | DSCAM | 1 | 5 | 0.1545 |  | Down syndrome cell adhesion molecule |
| GEN-0335 | DST | 2 | 3 | 0.3462 |  | Dystonin |
| GEN-0336 | DUSP15 | 2 | 2 |  |  | dual specificity phosphatase 15 |
| GEN-0337 | DVL3 | 2 | 2 |  |  | Dishevelled segment polarity protein 3 |
| GEN-0338 | DYDC1 | 2 | 1 |  |  | DPY30 domain containing 1 |
| GEN-0339 | DYDC2 | 2 | 1 |  |  | DPY30 domain containing 2 |
| GEN-0340 | DYNC1H1 | 1 | 5 | 0.4247 |  | dynein cytoplasmic 1 heavy chain 1 |
| GEN-0341 | DYRK1A | S | 5 | 0.405 |  | Dual-specificity tyrosine-(Y)-phosphorylation regulated kinase 1A |
| GEN-0342 | DLX2 | 2 | 3 |  |  | distal-less homeobox 2 |
| GEN-0343 | DRD1 | 2 | 1 |  |  | Dopamine receptor D1 |
| GEN-0344 | EBF3 | S | 5 | 0.3768 |  | early B-cell factor 3 |
| GEN-0345 | ECPAS | 2 | 2 |  |  | Ecm29 proteasome adaptor and scaffold |
| GEN-0346 | EEF1A2 | S | 5 |  |  | Eukaryotic translation elongation factor 1 alpha 2 |
| GEN-0347 | EFR3A | 2 | 3 |  |  | EFR3 homolog A (S. cerevisiae) |
| GEN-0348 | EGR3 | 2 | 1 |  |  | early growth response 3 |
| GEN-0349 | EHMT1 | S | 5 | 0.395 |  | Euchromatic histone-lysine N-methyltransferase 1 |
| GEN-0350 | EIF3F | 3 | 2 |  |  | eukaryotic translation initiation factor 3 subunit F |
| GEN-0351 | EIF3G | 1 | 2 |  |  | eukaryotic translation initiation factor 3 subunit G |
| GEN-0352 | EIF4E | 2 | 4 | 0.4192 |  | eukaryotic translation initiation factor 4E |
| GEN-0353 | EIF4G1 | 3 | 1 |  |  | eukaryotic translation initiation factor 4 gamma 1 |
| GEN-0354 | EIF5A | 3 | 1 |  |  | eukaryotic translation initiation factor 5A |
| GEN-0355 | ELAVL2 | 2 | 2 | 0.2039 |  | ELAV like neuron-specific RNA binding protein 2 |
| GEN-0356 | ELAVL3 | 1 | 2 |  |  | ELAV like neuron-specific RNA binding protein 3 |
| GEN-0357 | ELOVL2 | 2 | 1 |  |  | ELOVL fatty acid elongase 2 |
| GEN-0358 | ELP2 | S | 2 |  |  | elongator acetyltransferase complex subunit 2 |
| GEN-0359 | ELP4 | 2 | 2 | 0.337 |  | Elongator acetyltransferase complex subunit 4 |
| GEN-0360 | EMSY | 2 | 2 |  |  | EMSY, BRCA2 interacting transcriptional repressor |
| GEN-0361 | EN2 | 2 | 4 |  |  | engrailed homolog 2 |
| GEN-0362 | ENOX2 | 3 | 1 |  |  | ecto-NOX disulfide-thiol exchanger 2 |
| GEN-0363 | ENPP1 | 3 | 2 |  |  | ectonucleotide pyrophosphatase/phosphodiesterase 1 |
| GEN-0364 | EP300 | S | 5 | 0.1813 |  | E1A binding protein p300 |
| GEN-0365 | EP400 | 2 | 3 |  |  | E1A binding protein p400 |
| GEN-0366 | EPC2 | 2 | 2 |  |  | Enhancer of polycomb homolog 2 (Drosophila) |
| GEN-0367 | EPHA1 | 2 | 2 |  |  | EPH receptor A1 |
| GEN-0368 | EPHB1 | 3 | 3 |  |  | EPH receptor B1 |
| GEN-0369 | EPHB2 | 2 | 3 |  |  | EPH receptor B2 |
| GEN-0370 | EPPK1 | 2 | 3 |  |  | epiplakin 1 |
| GEN-0371 | ERBIN | 2 | 2 |  |  | erbb2 interacting protein |
| GEN-0372 | ERMN | 2 | 1 |  |  | ermin |
| GEN-0373 | ESR2 | 2 | 2 | 0.267 |  | estrogen receptor 2 (ER beta) |
| GEN-0374 | ESRRB | 2 | 2 |  |  | estrogen-related receptor beta |
| GEN-0375 | ETFB | 2 | 2 |  |  | Electron-transfer-flavoprotein, beta polypeptide |
| GEN-0376 | EXOC3 | 2 | 1 |  |  | exocyst complex component 3 |
| GEN-0377 | EXOC5 | 2 | 1 |  |  | exocyst complex component 5 |
| GEN-0378 | EXOC6 | 2 | 1 |  |  | exocyst complex component 6 |
| GEN-0379 | EXOC6B | 2 | 2 |  |  | exocyst complex component 6B |
| GEN-0380 | EXT1 | 2 | 2 |  |  | Exostosin 1 |
| GEN-0381 | FABP4 | 3 | 1 |  |  | fatty acid binding protein 4 |
| GEN-0382 | FABP5 | 2 | 2 |  |  | fatty acid binding protein 5 (psoriasis-associated) |
| GEN-0383 | FAM47A | 2 | 1 |  |  | family with sequence similarity 47 member A |
| GEN-0384 | FAM98C | 2 | 1 | 0.2587 |  | family with sequence similarity 98 member C |
| GEN-0385 | FAN1 | 2 | 2 |  |  | FANCD2/FANCI-associated nuclease 1 |
| GEN-0386 | FAT1 | 2 | 3 |  |  | FAT atypical cadherin 1 |
| GEN-0387 | FBN1 | 2 | 4 | 0.056 |  | Fibrillin 1 |
| GEN-0388 | FBRSL1 | S | 2 |  |  | fibrosin like 1 |
| GEN-0389 | FBXL13 | 3 | 1 |  |  | F-box and leucine rich repeat protein 13 |
| GEN-0390 | FBXO11 | S | 4 |  |  | F-box protein 11 |
| GEN-0391 | FBXO33 | 2 | 2 |  |  | F-box protein 33 |
| GEN-0392 | FBXO40 | 2 | 2 |  |  | F-box protein 40 |
| GEN-0393 | FCRL6 | 2 | 2 |  |  | Fc receptor like 6 |
| GEN-0394 | FEZF2 | 2 | 3 |  |  | FEZ family zinc finger 2 |
| GEN-0395 | FGA | 2 | 2 |  |  | Fibrinogen alpha chain |
| GEN-0396 | FGF13 | S | 1 |  |  | fibroblast growth factor 13 |
| GEN-0397 | FGF14 | 3 | 1 |  |  | fibroblast growth factor 14 |
| GEN-0398 | FGFR1 | 2 | 2 | 0.2765 |  | fibroblast growth factor receptor 1 |
| GEN-0399 | FHIT | 2 | 3 | 0.2513 |  | fragile histidine triad gene |
| GEN-0400 | FLNA | 3 | 3 |  |  | filamin A |
| GEN-0401 | ERG | 2 | 1 |  |  | ERG, ETS transcription factor |
| GEN-0402 | FOXG1 | S | 5 | 0.2373 |  | Forkhead box G1 |
| GEN-0403 | FOXP1 | S | 5 | 0.5332 |  | forkhead box P1 |
| GEN-0404 | FOXP2 | 1 | 5 |  |  | forkhead box P2 |
| GEN-0405 | FRG1 | 2 | 1 |  |  | FSHD region gene 1 |
| GEN-0406 | FRK | 2 | 1 |  |  | fyn-related kinase |
| GEN-0407 | FRMD5 | S | 2 |  |  | FERM domain containing 5 |
| GEN-0408 | FRMPD4 | S | 3 |  |  | FERM and PDZ domain containing 4 |
| GEN-0409 | FRRS1L | 3 | 1 |  |  | ferric chelate reductase 1 like |
| GEN-0410 | FRYL | S | 3 |  |  | FRY like transcription coactivator |
| GEN-0411 | FXN | 3 | 1 |  |  | frataxin |
| GEN-0412 | G3BP2 | 2 | 2 |  |  | G3BP stress granule assembly factor 2 |
| GEN-0413 | GABBR2 | S | 4 | 0.3264 |  | gamma-aminobutyric acid type B receptor subunit 2 |
| GEN-0414 | GABRA2 | 3 | 2 |  |  | gamma-aminobutyric acid type A receptor subunit alpha2 |
| GEN-0415 | GABRA3 | S | 1 |  |  | Gamma-aminobutyric acid (GABA) A receptor, alpha 3 |
| GEN-0416 | GABRA4 | 2 | 3 |  |  | gamma-aminobutyric acid (GABA) A receptor, alpha 4 |
| GEN-0417 | GABRB2 | 1 | 2 |  |  | gamma-aminobutyric acid type A receptor subunit beta2 |
| GEN-0418 | GABRB3 | 1 | 5 |  |  | gamma-aminobutyric acid (GABA) A receptor, beta 3 |
| GEN-0419 | GABRG2 | 3 | 3 |  |  | gamma-aminobutyric acid type A receptor subunit gamma 2 |
| GEN-0420 | GABRG3 | 2 | 3 |  |  | gamma-aminobutyric acid type A receptor gamma3 subunit |
| GEN-0421 | GALNT10 | 2 | 2 | 0.378 |  | polypeptide N-acetylgalactosaminyltransferase 10 |
| GEN-0422 | GALNT13 | 2 | 2 |  |  | polypeptide N-acetylgalactosaminyltransferase 13 |
| GEN-0423 | GALNT14 | 2 | 2 |  |  | polypeptide N-acetylgalactosaminyltransferase 14 |
| GEN-0424 | GALNT2 | S | 2 |  |  | polypeptide N-acetylgalactosaminyltransferase 2 |
| GEN-0425 | GALNT8 | 2 | 1 |  |  | polypeptide N-acetylgalactosaminyltransferase 8 |
| GEN-0426 | GAS2 | 2 | 1 |  |  | Growth arrest-specific 2 |
| GEN-0427 | GATM | S | 1 |  |  | Glycine amidinotransferase (L-arginine:glycine amidinotransferase) |
| GEN-0428 | GBE1 | 2 | 2 |  |  | 1,4-alpha-glucan branching enzyme 1 |
| GEN-0429 | GDA | 2 | 1 |  |  | guanine deaminase |
| GEN-0430 | GFAP | 1 | 1 |  |  | glial fibrillary acidic protein |
| GEN-0431 | GGNBP2 | 2 | 1 |  |  | gametogenetin binding protein 2 |
| GEN-0432 | GIGYF1 | 1 | 5 | 0.5434 |  | GRB10 interacting GYF protein 1 |
| GEN-0433 | GIGYF2 | 1 | 3 | 0.3059 |  | GRB10 interacting GYF protein 2 |
| GEN-0434 | GLI3 | 3 | 2 | 0.0862 |  | GLI family zinc finger 3 |
| GEN-0435 | GLIS1 | 2 | 1 |  |  | GLIS family zinc finger 1 |
| GEN-0436 | GLO1 | 2 | 3 |  |  | glyoxalase I |
| GEN-0437 | GLRA2 | 2 | 4 |  |  | glycine receptor, alpha 2 |
| GEN-0438 | GNAI1 | S | 2 |  |  | G protein subunit alpha i1 |
| GEN-0439 | GNAS | 2 | 3 |  |  | GNAS complex locus |
| GEN-0440 | GNB1L | 2 | 1 |  |  | guanine nucleotide binding protein (G protein), beta polypeptide 1-like |
| GEN-0441 | GNB2 | S | 2 |  |  | G protein subunit beta 2 |
| GEN-0442 | GPC4 | 2 | 1 |  |  | glypican 4 |
| GEN-0443 | GPC5 | 3 | 2 |  |  | glypican 5 |
| GEN-0444 | GPC6 | 2 | 2 |  |  | glypican 6 |
| GEN-0445 | GPD2 | 2 | 2 | 0.1442 |  | glycerol-3-phosphate dehydrogenase 2 |
| GEN-0446 | GPHN | 2 | 3 |  |  | Gephyrin |
| GEN-0447 | GPR37 | 2 | 1 |  |  | G protein-coupled receptor 37 |
| GEN-0448 | GPR85 | 2 | 2 |  |  | G protein-coupled receptor 85 |
| GEN-0449 | GPX1 | 2 | 2 |  |  | glutathione peroxidase 1 |
| GEN-0450 | GRB10 | 3 | 3 |  |  | growth factor receptor bound protein 10 |
| GEN-0451 | GRIA1 | 2 | 4 | 0.3193 |  | glutamate ionotropic receptor AMPA type subunit 1 |
| GEN-0452 | GRIA2 | 1 | 4 |  |  | glutamate ionotropic receptor AMPA type subunit 2 |
| GEN-0453 | GRIA3 | S | 4 |  |  | glutamate ionotropic receptor AMPA type subunit 3 |
| GEN-0454 | GRID1 | 2 | 2 |  |  | Glutamate receptor, ionotropic, delta 1 |
| GEN-0455 | GRID2 | 2 | 3 | 0.2473 |  | glutamate receptor, ionotropic, delta 2 |
| GEN-0456 | GRID2IP | 2 | 2 |  |  | Grid2 interacting protein |
| GEN-0457 | GRIK2 | 2 | 4 |  |  | glutamate ionotropic receptor kainate type subunit 2 |
| GEN-0458 | GRIK3 | 2 | 2 |  |  | glutamate ionotropic receptor kainate type subunit 3 |
| GEN-0459 | GRIK4 | 2 | 2 |  |  | Glutamate receptor, ionotropic, kainate 4 |
| GEN-0460 | GRIK5 | 2 | 3 |  |  | Glutamate receptor, ionotropic, kainate 5 |
| GEN-0461 | GRIN1 | 1 | 5 | 0.3348 |  | Glutamate receptor, ionotropic, N-methyl D-aspartate 1 |
| GEN-0462 | GRIN2A | 1 | 5 | 0.4523 |  | glutamate receptor, ionotropic, N-methyl D-aspartate 2A |
| GEN-0463 | GRIN2B | 1 | 5 | 0.6242 |  | glutamate receptor, inotropic, N-methyl D-apartate 2B |
| GEN-0464 | GRIP1 | 2 | 4 |  |  | glutamate receptor interacting protein 1 |
| GEN-0465 | GRK4 | 2 | 2 |  |  | G protein-coupled receptor kinase 4 |
| GEN-0466 | GRM5 | 2 | 3 | 0.3574 |  | glutamate metabotropic receptor 5 |
| GEN-0467 | GRM7 | 2 | 4 |  |  | Glutamate receptor, metabotropic 7 |
| GEN-0468 | GTF2I | 2 | 3 |  |  | general transcription factor IIi |
| GEN-0469 | GUCY1A2 | 2 | 1 |  |  | guanylate cyclase 1 soluble subunit alpha 2 |
| GEN-0470 | H1-4 | S | 3 |  |  | H1.4 linker histone, cluster member |
| GEN-0471 | H2BC11 | 2 | 1 |  |  | H2B clustered histone 11 |
| GEN-0472 | H3-3B | S | 2 |  |  | H3.3 histone B |
| GEN-0473 | H4C11 | S | 1 |  |  | H4 clustered histone 11 |
| GEN-0474 | H4C3 | S | 1 |  |  | H4 clustered histone 3 |
| GEN-0475 | H4C5 | S | 2 |  |  | H4 clustered histone 5 |
| GEN-0476 | HACE1 | 3 | 3 |  |  | HECT domain and ankyrin repeat containing E3 ubiquitin protein ligase 1 |
| GEN-0477 | HCFC1 | S | 3 |  |  | host cell factor C1 |
| GEN-0478 | HCN1 | 3 | 3 |  |  | Hyperpolarization activated cyclic nucleotide-gated potassium channel 1 |
| GEN-0479 | HDAC4 | S | 4 |  |  | histone deacetylase 4 |
| GEN-0480 | HDAC8 | S | 3 |  |  | histone deacetylase 8 |
| GEN-0481 | HDLBP | 1 | 2 |  |  | high density lipoprotein binding protein |
| GEN-0482 | HECTD1 | 3 | 2 |  |  | HECT domain E3 ubiquitin protein ligase 1 |
| GEN-0483 | HECTD4 | 1 | 3 | 0.2896 |  | HECT domain E3 ubiquitin protein ligase 4 |
| GEN-0484 | HECW2 | 2 | 4 |  |  | HECT, C2 and WW domain containing E3 ubiquitin protein ligase 2 |
| GEN-0485 | HEPACAM | S | 3 | 0.2696 |  | hepatic and glial cell adhesion molecule |
| GEN-0486 | HERC1 | S | 3 |  |  | HECT and RLD domain containing E3 ubiquitin protein ligase family member 1 |
| GEN-0487 | HERC2 | S | 3 |  |  | HECT and RLD domain containing E3 ubiquitin protein ligase 2 |
| GEN-0488 | HIVEP2 | S | 4 |  |  | HIVEP zinc finger 2 |
| GEN-0489 | HIVEP3 | 2 | 3 |  |  | human immunodeficiency virus type I enhancer binding protein 3 |
| GEN-0490 | HLA-DPB1 | 2 | 1 |  |  | major histocompatibility complex, class II, DP beta 1 |
| GEN-0491 | HNRNPD | S | 2 |  |  | heterogeneous nuclear ribonucleoprotein D |
| GEN-0492 | HNRNPF | 2 | 1 |  |  | heterogeneous nuclear ribonucleoprotein F |
| GEN-0493 | HNRNPH2 | 1 | 5 |  |  | heterogeneous nuclear ribonucleoprotein H2 |
| GEN-0494 | HNRNPK | S | 3 |  |  | heterogeneous nuclear ribonucleoprotein K |
| GEN-0495 | HNRNPL | 3 | 1 |  |  | heterogeneous nuclear ribonucleoprotein L |
| GEN-0496 | HNRNPR | S | 2 |  |  | heterogeneous nuclear ribonucleoprotein R |
| GEN-0497 | HNRNPU | S | 5 |  |  | heterogeneous nuclear ribonucleoprotein U |
| GEN-0498 | HNRNPUL2 | S | 1 |  |  | heterogeneous nuclear ribonucleoprotein U like 2 |
| GEN-0499 | HOMER1 | 2 | 2 |  |  | Homer homolog 1 (Drosophila) |
| GEN-0500 | HOXA1 | S | 4 |  |  | homeobox A1 |
| GEN-0501 | HRAS | 1 | 3 |  |  | v-Ha-ras Harvey rat sarcoma viral oncogene homolog |
| GEN-0502 | HS3ST5 | 2 | 2 |  |  | heparan sulfate (glucosamine) 3-O-sulfotransferase 5 |
| GEN-0503 | HSD11B1 | 2 | 2 |  |  | hydroxysteroid (11-beta) dehydrogenase 1 |
| GEN-0504 | HTR1B | 2 | 2 |  |  | 5-hydroxytryptamine (serotonin) receptor 1B |
| GEN-0505 | GSTM1 | 2 | 1 |  |  | glutathione S-transferase M1 |
| GEN-0506 | HLA-A | 2 | 3 |  |  | major histocompatibility complex, class I, A |
| GEN-0507 | HTR3A | 2 | 2 |  |  | 5-hydroxytryptamine (serotonin) receptor 3A |
| GEN-0508 | HTR3C | 3 | 2 |  |  | 5-hydroxytryptamine (serotonin) receptor 3, family member C |
| GEN-0509 | HUWE1 | S | 5 |  |  | HECT, UBA and WWE domain containing 1, E3 ubiquitin protein ligase |
| GEN-0510 | HYDIN | 2 | 2 |  |  | HYDIN, axonemal central pair apparatus protein |
| GEN-0511 | ICA1 | 2 | 3 |  |  | islet cell autoantigen 1 |
| GEN-0512 | IGF1 | 3 | 2 |  |  | insulin like growth factor 1 |
| GEN-0513 | IKZF1 | 3 | 2 |  |  | IKAROS family zinc finger 1 |
| GEN-0514 | IL1R2 | 2 | 2 |  |  | interleukin 1 receptor, type II |
| GEN-0515 | HLA-B | 2 | 2 |  |  | Major histocompatibility complex, class I, B |
| GEN-0516 | HLA-DRB1 | 2 | 3 |  |  | major histocompatibility complex, class II, DR beta 1 |
| GEN-0517 | HLA-G | 2 | 1 |  |  | major histocompatibility complex, class I, G |
| GEN-0518 | HMGN1 | 2 | 1 |  |  | high mobility group nucleosome binding domain 1 |
| GEN-0519 | HTR2C | 3 | 3 | 0.606 |  | 5-hydroxytryptamine receptor 2C |
| GEN-0520 | IL1RAPL1 | 2 | 4 |  |  | interleukin 1 receptor accessory protein-like 1 |
| GEN-0521 | IL1RAPL2 | 2 | 1 |  |  | interleukin 1 receptor accessory protein-like 2 |
| GEN-0522 | ILF2 | 2 | 2 |  |  | Interleukin enhancer binding factor 2 |
| GEN-0523 | IMMP2L | 2 | 4 | 0.201 |  | IMP2 inner mitochondrial membrane peptidase-like (S. cerevisiae) |
| GEN-0524 | INPP1 | 2 | 2 |  |  | inositol polyphosphate-1-phosphatase |
| GEN-0525 | INTS1 | S | 3 |  |  | integrator complex subunit 1 |
| GEN-0526 | INTS6 | 2 | 2 |  |  | Integrator complex subunit 6 |
| GEN-0527 | IQGAP3 | 2 | 2 |  |  | IQ motif containing GTPase activating protein 3 |
| GEN-0528 | IQSEC2 | S | 5 | 0.3362 |  | IQ motif and Sec7 domain 2 |
| GEN-0529 | IRF2BPL | S | 4 | 0.3636 |  | Interferon regulatory factor 2 binding protein-like |
| GEN-0530 | IRX5 | S | 1 |  |  | iroquois homeobox 5 |
| GEN-0531 | ITGA8 | 3 | 2 |  |  | integrin subunit alpha 8 |
| GEN-0532 | ITGB3 | 2 | 4 |  |  | integrin, beta 3 (platelet glycoprotein IIIa, antigen CD61) |
| GEN-0533 | ITPR1 | 2 | 4 |  |  | inositol 1,4,5-trisphosphate receptor type 1 |
| GEN-0534 | ITSN1 | 2 | 3 |  |  | intersectin 1 |
| GEN-0535 | JARID2 | 2 | 4 | 0.2688 |  | jumonji and AT-rich interaction domain containing 2 |
| GEN-0536 | JMJD1C | 2 | 3 | 0.3996 |  | jumonji domain containing 1C |
| GEN-0537 | KANK1 | 2 | 4 |  |  | KN motif and ankyrin repeat domains 1 |
| GEN-0538 | KANSL1 | S | 3 |  |  | KAT8 regulatory NSL complex subunit 1 |
| GEN-0539 | KAT2B | 2 | 2 |  |  | K(lysine) acetyltransferase 2B |
| GEN-0540 | KAT6A | S | 5 | 0.4303 |  | K(lysine) acetyltransferase 6A |
| GEN-0541 | KAT6B | 3 | 3 |  |  | lysine acetyltransferase 6B |
| GEN-0542 | KATNAL1 | 2 | 1 |  |  | katanin catalytic subunit A1 like 1 |
| GEN-0543 | KATNAL2 | 1 | 4 |  |  | Katanin p60 subunit A-like 2 |
| GEN-0544 | KCNA2 | 3 | 3 |  |  | potassium voltage-gated channel subfamily A member 2 |
| GEN-0545 | KCNA3 | 3 | 1 |  |  | potassium voltage-gated channel subfamily A member 3 |
| GEN-0546 | KCNB1 | S | 5 | 0.3489 |  | potassium voltage-gated channel subfamily B member 1 |
| GEN-0547 | KCNC1 | 2 | 3 |  |  | potassium voltage-gated channel subfamily C member 1 |
| GEN-0548 | KCNC2 | 3 | 3 |  |  | potassium voltage-gated channel subfamily C member 2 |
| GEN-0549 | KCND2 | 2 | 3 |  |  | potassium voltage-gated channel subfamily D member 2 |
| GEN-0550 | KCND3 | 2 | 4 |  |  | potassium voltage-gated channel subfamily D member 3 |
| GEN-0551 | KCNH1 | S | 2 |  |  | potassium voltage-gated channel subfamily H member 1 |
| GEN-0552 | KCNH5 | 3 | 2 |  |  | potassium voltage-gated channel subfamily H member 5 |
| GEN-0553 | KCNH7 | 3 | 3 |  |  | potassium voltage-gated channel subfamily H member 7 |
| GEN-0554 | KCNJ10 | 2 | 4 |  |  | potassium voltage-gated channel subfamily J member 10 |
| GEN-0555 | KCNJ15 | 2 | 1 |  |  | potassium voltage-gated channel subfamily J member 15 |
| GEN-0556 | KCNK7 | 2 | 1 |  |  | potassium two pore domain channel subfamily K member 7 |
| GEN-0557 | KCNMA1 | 2 | 4 | 0.3195 |  | potassium large conductance calcium-activated channel, subfamily M, alpha member 1 |
| GEN-0558 | KCNN2 | 3 | 2 | 0.178 |  | potassium calcium-activated channel subfamily N member 2 |
| GEN-0559 | KCNQ2 | 1 | 5 |  |  | potassium voltage-gated channel subfamily Q member 2 |
| GEN-0560 | KCNQ3 | 1 | 5 | 0.1428 |  | potassium voltage-gated channel subfamily Q member 3 |
| GEN-0561 | KCNS3 | 2 | 2 | 0.3326 |  | potassium voltage-gated channel modifier subfamily S member 3 |
| GEN-0562 | KCTD13 | 2 | 2 |  |  | Potassium channel tetramerisation domain containing 13 |
| GEN-0563 | KDM1A | 3 | 2 |  |  | lysine demethylase 1A |
| GEN-0564 | KDM1B | 2 | 1 |  |  | lysine demethylase 1B |
| GEN-0565 | KDM2A | 3 | 3 |  |  | lysine demethylase 2A |
| GEN-0566 | KDM2B | 1 | 3 |  |  | lysine demethylase 2B |
| GEN-0567 | KDM3A | 3 | 1 |  |  | lysine demethylase 3A |
| GEN-0568 | KDM3B | S | 2 | 0.28 |  | lysine demethylase 3B |
| GEN-0569 | KDM4B | 2 | 2 |  |  | lysine demethylase 4B |
| GEN-0570 | KDM4C | 2 | 1 |  |  | lysine demethylase 4C |
| GEN-0571 | KDM5A | 2 | 2 | 0.3722 |  | lysine demethylase 5A |
| GEN-0572 | KDM5B | 1 | 5 | 0.4662 |  | Lysine (K)-specific demethylase 5B |
| GEN-0573 | KDM5C | 1 | 5 |  |  | lysine demethylase 5C |
| GEN-0574 | KDM6A | 2 | 4 | 0.3408 |  | lysine demethylase 6A |
| GEN-0575 | KDM6B | 1 | 5 | 0.2598 |  | Lysine (K)-specific demethylase 6B |
| GEN-0576 | KHDRBS2 | 2 | 1 |  |  | KH domain containing, RNA binding, signal transduction associated 2 |
| GEN-0577 | KIAA0232 | 1 | 1 |  |  | KIAA0232 |
| GEN-0578 | KIAA1586 | 2 | 2 |  |  | KIAA1586 |
| GEN-0579 | KIF13B | 2 | 2 |  |  | Kinesin family member 13B |
| GEN-0580 | KIF14 | 2 | 2 |  |  | kinesin family member 14 |
| GEN-0581 | KIF1A | S | 4 |  |  | kinesin family member 1A |
| GEN-0582 | KIF5C | S | 4 |  |  | Kinesin family member 5C |
| GEN-0583 | KIRREL3 | 2 | 4 | 0.365 |  | Kin of IRRE like 3 (Drosophila) |
| GEN-0584 | KIZ | 3 | 2 | 0.41 |  | kizuna centrosomal protein |
| GEN-0585 | KLF16 | 2 | 1 |  |  | Kruppel like factor 16 |
| GEN-0586 | KLF7 | 3 | 3 |  |  | Kruppel like factor 7 |
| GEN-0587 | KLHL20 | 1 | 2 |  |  | kelch like family member 20 |
| GEN-0588 | KMT2A | S | 5 | 0.3106 |  | Lysine (K)-specific methyltransferase 2A |
| GEN-0589 | KMT2B | 3 | 3 | 0.2886 |  | lysine methyltransferase 2B |
| GEN-0590 | KMT2C | S | 5 | 0.4054 |  | Lysine (K)-specific methyltransferase 2C |
| GEN-0591 | KMT2D | 3 | 3 | 0.3477 |  | lysine methyltransferase 2D |
| GEN-0592 | KMT2E | S | 5 | 0.4905 |  | Lysine (K)-specific methyltransferase 2E |
| GEN-0593 | KMT5B | 1 | 5 | 0.3354 |  | lysine methyltransferase 5B |
| GEN-0594 | KNG1 | 3 | 1 |  |  | kininogen 1 |
| GEN-0595 | KPTN | S | 2 |  |  | kaptin, actin binding protein |
| GEN-0596 | KRR1 | 2 | 1 |  |  | KRR1, small subunit (SSU) processome component, homolog (yeast) |
| GEN-0597 | KRT26 | 2 | 2 |  |  | keratin 26 |
| GEN-0598 | LAMA1 | 2 | 4 |  |  | Laminin, alpha 1 |
| GEN-0599 | LAMB1 | 2 | 3 | 0.3391 |  | laminin, beta 1 |
| GEN-0600 | LARP1 | 3 | 1 |  |  | La ribonucleoprotein 1, translational regulator |
| GEN-0601 | LAS1L | 3 | 2 |  |  | LAS1 like ribosome biogenesis factor |
| GEN-0602 | LDB1 | 1 | 1 |  |  | LIM domain binding 1 |
| GEN-0603 | LDLR | 3 | 1 |  |  | low density lipoprotein receptor |
| GEN-0604 | LEMD3 | 2 | 1 |  |  | LEM domain containing 3 |
| GEN-0605 | LEO1 | 2 | 2 |  |  | LEO1 homolog, Paf1/RNA polymerase II complex component |
| GEN-0606 | LEP | 2 | 1 |  |  | Leptin |
| GEN-0607 | LHX2 | 2 | 2 |  |  | LIM homeobox 2 |
| GEN-0608 | LILRB2 | 2 | 1 |  |  | leukocyte immunoglobulin like receptor B2 |
| GEN-0609 | LIN7B | 2 | 1 |  |  | lin-7 homolog B, crumbs cell polarity complex component |
| GEN-0610 | LMTK3 | 3 | 2 |  |  | lemur tyrosine kinase 3 |
| GEN-0611 | LMX1B | 2 | 1 |  |  | LIM homeobox transcription factor 1 beta |
| GEN-0612 | LNPK | S | 2 |  |  | lunapark, ER junction formation factor |
| GEN-0613 | LRBA | 2 | 3 |  |  | LPS-responsive vesicle trafficking, beach and anchor containing |
| GEN-0614 | LRFN2 | 2 | 2 |  |  | leucine rich repeat and fibronectin type III domain containing 2 |
| GEN-0615 | LRFN5 | 2 | 2 |  |  | leucine rich repeat and fibronectin type III domain containing 5 |
| GEN-0616 | LRP1 | 2 | 3 |  |  | LDL receptor related protein 1 |
| GEN-0617 | LRP2 | 2 | 4 |  |  | LDL receptor related protein 2 |
| GEN-0618 | LRRC1 | 2 | 2 |  |  | leucine rich repeat containing 1 |
| GEN-0619 | LRRC4 | 2 | 2 |  |  | leucine rich repeat containing 4 |
| GEN-0620 | LRRC4C | 1 | 1 |  |  | leucine rich repeat containing 4C |
| GEN-0621 | LZTR1 | 1 | 5 | 0.3326 |  | Leucine-zipper-like transcription regulator 1 |
| GEN-0622 | MACF1 | S | 3 |  |  | microtubule actin crosslinking factor 1 |
| GEN-0623 | MACROD2 | 2 | 4 | 0.2258 |  | MACRO domain containing 2 |
| GEN-0624 | MAGEC3 | 1 | 2 |  |  | MAGE family member C3 |
| GEN-0625 | MAGEL2 | S | 5 |  |  | MAGE-like 2 |
| GEN-0626 | MAOA | 2 | 4 | 0.3522 |  | monoamine oxidase A |
| GEN-0627 | MAOB | 2 | 2 |  |  | monoamine oxidase B |
| GEN-0628 | MAP1A | 1 | 1 |  |  | microtubule associated protein 1A |
| GEN-0629 | MAP1B | 2 | 4 | 0.2321 |  | microtubule associated protein 1B |
| GEN-0630 | MAP4K1 | 3 | 2 |  |  | mitogen-activated protein kinase kinase kinase kinase 1 |
| GEN-0631 | MAP4K4 | 2 | 1 |  |  | mitogen-activated protein kinase kinase kinase kinase 4 |
| GEN-0632 | MAPK3 | 2 | 2 |  |  | mitogen-activated protein kinase 3 |
| GEN-0633 | MAPK8IP1 | 3 | 1 |  |  | mitogen-activated protein kinase 8 interacting protein 1 |
| GEN-0634 | MAPK8IP3 | S | 3 |  |  | mitogen-activated protein kinase 8 interacting protein 3 |
| GEN-0635 | MAPT | 3 | 2 |  |  | microtubule associated protein tau |
| GEN-0636 | MARK1 | 2 | 3 |  |  | microtubule affinity regulating kinase 1 |
| GEN-0637 | MARK2 | 2 | 3 | 0.5699 |  | microtubule affinity regulating kinase 2 |
| GEN-0638 | MAST1 | 3 | 2 |  |  | microtubule associated serine/threonine kinase 1 |
| GEN-0639 | MAST3 | 3 | 2 | 0.1553 |  | microtubule associated serine/threonine kinase 3 |
| GEN-0640 | MBD1 | 2 | 2 |  |  | methyl-CpG binding domain protein 1 |
| GEN-0641 | MBD3 | 2 | 1 |  |  | methyl-CpG binding domain protein 3 |
| GEN-0642 | MBD4 | 2 | 2 |  |  | methyl-CpG binding domain protein 4 |
| GEN-0643 | MBD5 | S | 5 | 0.4554 |  | Methyl-CpG binding domain protein 5 |
| GEN-0644 | MBD6 | 2 | 1 |  |  | Methyl-CpG binding domain protein 6 |
| GEN-0645 | MBOAT7 | S | 5 |  |  | membrane bound O-acyltransferase domain containing 7 |
| GEN-0646 | MCM4 | 2 | 1 |  |  | minichromosome maintenance complex component 4 |
| GEN-0647 | MCM6 | 2 | 1 |  |  | minichromosome maintenance complex component 6 |
| GEN-0648 | MCPH1 | 2 | 4 |  |  | microcephalin 1 |
| GEN-0649 | MDGA2 | 2 | 3 |  |  | MAM domain containing glycosylphosphatidylinositol anchor 2 |
| GEN-0650 | LZTS2 | 2 | 1 |  |  | leucine zipper, putative tumor suppressor 2 |
| GEN-0651 | MAPT-AS1 | 2 | 1 |  |  | MAPT antisense RNA 1 |
| GEN-0652 | MED12L | S | 2 |  |  | mediator complex subunit 12L |
| GEN-0653 | MED13 | S | 5 |  |  | mediator complex subunit 13 |
| GEN-0654 | MED13L | S | 5 | 0.2878 |  | Mediator complex subunit 13-like |
| GEN-0655 | MED23 | 2 | 1 |  |  | mediator complex subunit 23 |
| GEN-0656 | MEF2C | S | 5 | 0.5533 |  | myocyte enhancer factor 2C |
| GEN-0657 | MEGF10 | 2 | 2 |  |  | multiple EGF like domains 10 |
| GEN-0658 | MEGF11 | 2 | 2 |  |  | multiple EGF like domains 11 |
| GEN-0659 | MEIS2 | S | 4 | 0.1982 |  | Meis homeobox 2 |
| GEN-0660 | MEMO1 | 2 | 1 |  |  | mediator of cell motility 1 |
| GEN-0661 | MET | 2 | 4 |  |  | met proto-oncogene (hepatocyte growth factor receptor) |
| GEN-0662 | METTL14 | 3 | 2 |  |  | methyltransferase 14, N6-adenosine-methyltransferase non-catalytic subunit |
| GEN-0663 | METTL26 | 2 | 1 |  |  | methyltransferase like 26 |
| GEN-0664 | MFRP | 2 | 2 |  |  | Membrane frizzled-related protein |
| GEN-0665 | MIB1 | 2 | 3 |  |  | Mindbomb E3 ubiquitin protein ligase 1 |
| GEN-0666 | MINK1 | 3 | 2 |  |  | misshapen like kinase 1 |
| GEN-0667 | MIR137 | 2 | 3 |  |  | microRNA 137 |
| GEN-0668 | MKRN1 | 3 | 1 |  |  | makorin ring finger protein 1 |
| GEN-0669 | MKX | 1 | 1 |  |  | mohawk homeobox |
| GEN-0670 | MLANA | 2 | 1 |  |  | melan-A |
| GEN-0671 | MRTFB | 2 | 3 |  |  | myocardin related transcription factor B |
| GEN-0672 | MSANTD2 | 2 | 1 |  |  | Myb/SANT DNA binding domain containing 2 |
| GEN-0673 | MSL2 | 3 | 2 | 0.37 |  | MSL complex subunit 2 |
| GEN-0674 | MSL3 | S | 2 |  |  | MSL complex subunit 3 |
| GEN-0675 | MSR1 | 2 | 2 |  |  | macrophage scavenger receptor 1 |
| GEN-0676 | MSRA | 3 | 3 |  |  | methionine sulfoxide reductase A |
| GEN-0677 | MSX2 | S | 1 |  |  | msh homeobox 2 |
| GEN-0678 | MTF1 | 2 | 2 |  |  | metal-regulatory transcription factor 1 |
| GEN-0679 | MTOR | S | 5 |  |  | mechanistic target of rapamycin kinase |
| GEN-0680 | MTSS2 | S | 2 |  |  | MTSS I-BAR domain containing 2 |
| GEN-0681 | MUC12 | 2 | 2 |  |  | mucin 12, cell surface associated |
| GEN-0682 | MUC4 | 2 | 3 |  |  | mucin 4, cell surface associated |
| GEN-0683 | MYCBP2 | 1 | 3 |  |  | MYC binding protein 2 |
| GEN-0684 | MYH10 | 2 | 2 |  |  | myosin heavy chain 10 |
| GEN-0685 | MYH4 | 2 | 2 |  |  | Myosin, heavy chain 4, skeletal muscle |
| GEN-0686 | MYH9 | 2 | 2 |  |  | myosin heavy chain 9 |
| GEN-0687 | MYLK | 3 | 2 |  |  | myosin light chain kinase |
| GEN-0688 | MYO16 | 2 | 3 |  |  | myosin XVI |
| GEN-0689 | MYO1E | 2 | 2 |  |  | myosin IE |
| GEN-0690 | MYO5A | 2 | 2 |  |  | myosin VA |
| GEN-0691 | MYO5C | 2 | 2 |  |  | myosin VC |
| GEN-0692 | MYO7A | 3 | 2 |  |  | myosin VIIA |
| GEN-0693 | MYO9B | 2 | 3 |  |  | Myosin IXB |
| GEN-0694 | MYOCD | 3 | 1 |  |  | myocardin |
| GEN-0695 | MYT1L | 1 | 5 | 0.3759 |  | Myelin transcription factor 1-like |
| GEN-0696 | MNT | 2 | 1 |  |  | MAX network transcriptional repressor |
| GEN-0697 | NAA10 | S | 3 |  |  | N-alpha-acetyltransferase 10, NatA catalytic subunit |
| GEN-0698 | NAA15 | S | 5 | 0.3932 |  | N(alpha)-acetyltransferase 15, NatA auxiliary subunit |
| GEN-0699 | NAALADL2 | 2 | 2 |  |  | N-acetylated alpha-linked acidic dipeptidase-like 2 |
| GEN-0700 | NACC1 | S | 3 |  |  | nucleus accumbens associated 1 |
| GEN-0701 | NASP | 3 | 1 |  |  | nuclear autoantigenic sperm protein |
| GEN-0702 | NAV2 | 2 | 3 |  |  | neuron navigator 2 |
| GEN-0703 | MSNP1AS | 2 | 3 |  |  | Moesinpseudogene 1, antisense |
| GEN-0704 | NAV3 | 2 | 2 |  |  | neuron navigator 3 |
| GEN-0705 | NBEA | S | 5 | 0.3471 |  | neurobeachin |
| GEN-0706 | NCAPH2 | 3 | 1 |  |  | non-SMC condensin II complex subunit H2 |
| GEN-0707 | NCKAP1 | 1 | 4 | 0.4006 |  | NCK-associated protein 1 |
| GEN-0708 | NCKAP5 | 2 | 1 |  |  | NCK-associated protein 5 |
| GEN-0709 | NCOA1 | 1 | 1 |  |  | nuclear receptor coactivator 1 |
| GEN-0710 | NCOR1 | 2 | 3 |  |  | nuclear receptor corepressor 1 |
| GEN-0711 | NDUFA5 | 2 | 1 |  |  | NADH dehydrogenase (ubiquinone) 1 alpha subcomplex, 5, 13kDa |
| GEN-0712 | NEDD4 | 3 | 1 |  |  | NEDD4E3 ubiquitin protein ligase |
| GEN-0713 | NEGR1 | 2 | 2 | 0.481 |  | neuronal growth regulator 1 |
| GEN-0714 | NEO1 | 2 | 1 |  |  | Neogenin 1 |
| GEN-0715 | NEXMIF | 1 | 5 |  |  | neurite extension and migration factor |
| GEN-0716 | NF1 | S | 5 | 0.3193 |  | neurofibromin 1 (neurofibromatosis, von Recklinghausen disease, Watson disease) |
| GEN-0717 | NFE2L3 | 2 | 2 |  |  | nuclear factor, erythroid 2 like 3 |
| GEN-0718 | NFIA | 2 | 4 |  |  | nuclear factor I/A |
| GEN-0719 | NFIB | S | 2 |  |  | nuclear factor I B |
| GEN-0720 | NFIX | S | 5 |  |  | nuclear factor I/X (CCAAT-binding transcription factor) |
| GEN-0721 | NINL | 2 | 3 | 0.1485 |  | Ninein-like |
| GEN-0722 | NIPA1 | 2 | 2 |  |  | non imprinted in Prader-Willi/Angelman syndrome 1 |
| GEN-0723 | NIPA2 | 2 | 1 |  |  | non imprinted in Prader-Willi/Angelman syndrome 2 |
| GEN-0724 | NIPBL | S | 5 |  |  | Nipped-B homolog (Drosophila) |
| GEN-0725 | NKX2-2 | 3 | 1 |  |  | NK2 homeobox 2 |
| GEN-0726 | NLGN1 | 2 | 4 |  |  | neuroligin 1 |
| GEN-0727 | NLGN2 | 1 | 4 |  |  | Neuroligin 2 |
| GEN-0728 | NLGN3 | 1 | 5 | 0.7269 |  | neuroligin 3 |
| GEN-0729 | NLGN4X | 1 | 5 | 0.6274 |  | neuroligin 4, X-linked |
| GEN-0730 | NLGN4Y | 2 | 2 |  |  | neuroligin 4, Y-linked |
| GEN-0731 | NMT1 | 3 | 1 |  |  | N-myristoyltransferase 1 |
| GEN-0732 | NOTCH1 | 2 | 3 |  |  | notch receptor 1 |
| GEN-0733 | NOVA2 | S | 1 |  |  | NOVA alternative splicing regulator 2 |
| GEN-0734 | NPAS3 | 3 | 2 | 0.376 |  | neuronal PAS domain protein 3 |
| GEN-0735 | NPFFR2 | 3 | 2 |  |  | neuropeptide FF receptor 2 |
| GEN-0736 | NPTN | 3 | 1 |  |  | neuroplastin |
| GEN-0737 | NR1D1 | 2 | 1 |  |  | nuclear receptor subfamily 1 group D member 1 |
| GEN-0738 | NR2F1 | S | 5 | 0.3524 |  | nuclear receptor subfamily 2 group F member 1 |
| GEN-0739 | NR3C2 | S | 3 | 0.4505 |  | Nuclear receptor subfamily 3, group C, member 2 |
| GEN-0740 | NR4A2 | 1 | 5 | 0.2685 |  | nuclear receptor subfamily 4 group A member 2 |
| GEN-0741 | NRCAM | 2 | 2 |  |  | neuronal cell adhesion molecule |
| GEN-0742 | NRP2 | 2 | 3 |  |  | neuropilin 2 |
| GEN-0743 | NRXN1 | 1 | 5 | 0.6143 |  | neurexin 1 |
| GEN-0744 | NRXN2 | 1 | 4 | 0.4796 |  | neurexin 2 |
| GEN-0745 | NRXN3 | 1 | 5 | 0.1725 |  | neurexin 3 |
| GEN-0746 | NSD1 | S | 5 |  |  | nuclear receptor binding SET domain protein 1 |
| GEN-0747 | NSD2 | S | 4 |  |  | nuclear receptor binding SET domain protein 2 |
| GEN-0748 | NSMCE3 | 2 | 2 |  |  | NSE3 homolog, SMC5-SMC6 complex component |
| GEN-0749 | NTNG1 | S | 2 |  |  | netrin G1 |
| GEN-0750 | NTNG2 | S | 2 |  |  | netrin G2 |
| GEN-0751 | NTRK1 | 2 | 3 |  |  | neurotrophic tyrosine kinase, receptor, type 1 |
| GEN-0752 | NTRK2 | S | 3 |  |  | neurotrophic receptor tyrosine kinase 2 |
| GEN-0753 | NTRK3 | 2 | 4 | 0.2728 |  | neurotrophic tyrosine kinase, receptor, type 3 |
| GEN-0754 | NUAK1 | 2 | 2 |  |  | NUAK family, SNF1-like kinase, 1 |
| GEN-0755 | NUDCD2 | 2 | 1 |  |  | NudC domain containing 2 |
| GEN-0756 | NUP133 | 2 | 2 |  |  | nucleoporin 133kDa |
| GEN-0757 | NUP155 | 1 | 2 |  |  | nucleoporin 155 |
| GEN-0758 | NXF1 | 3 | 1 |  |  | nuclear RNA export factor 1 |
| GEN-0759 | NXPH1 | 2 | 2 |  |  | neurexophilin 1 |
| GEN-0760 | NPAS2 | 2 | 1 |  |  | neuronal PAS domain protein 2 |
| GEN-0761 | OCRL | S | 3 |  |  | oculocerebrorenal syndrome of Lowe |
| GEN-0762 | OFD1 | 2 | 2 |  |  | OFD1, centriole and centriolar satellite protein |
| GEN-0763 | OPHN1 | 2 | 4 |  |  | oligophrenin 1 |
| GEN-0764 | OR1C1 | 2 | 1 |  |  | olfactory receptor, family 1, subfamily C, member 1 |
| GEN-0765 | OR2M4 | 2 | 1 |  |  | Olfactory receptor, family 2, subfamily M, member 4 |
| GEN-0766 | OR2T10 | 2 | 1 |  |  | olfactory receptor family 2 subfamily T member 10 |
| GEN-0767 | OR52M1 | 2 | 1 |  |  | Olfactory receptor, family 52, subfamily M, member 1 |
| GEN-0768 | OTUD7A | 2 | 3 |  |  | OTU deubiquitinase 7A |
| GEN-0769 | OTX1 | 2 | 1 |  |  | orthodenticle homeobox 1 |
| GEN-0770 | OXT | 2 | 2 |  |  | oxytocin/neurophysin I prepropeptide |
| GEN-0771 | OXTR | 2 | 4 | 0.547 |  | oxytocin receptor |
| GEN-0772 | P2RX5 | 2 | 2 |  |  | Purinergic receptor P2X, ligand gated ion channel, 5 |
| GEN-0773 | P4HA2 | 2 | 2 |  |  | Prolyl 4-hydroxylase, alpha polypeptide II |
| GEN-0774 | PABPC1 | S | 2 |  |  | poly(A) binding protein cytoplasmic 1 |
| GEN-0775 | PACS1 | S | 5 |  |  | phosphofurin acidic cluster sorting protein 1 |
| GEN-0776 | PACS2 | S | 3 |  |  | phosphofurin acidic cluster sorting protein 2 |
| GEN-0777 | PAFAH1B2 | 2 | 1 |  |  | platelet activating factor acetylhydrolase 1b catalytic subunit 2 |
| GEN-0778 | PAH | 1 | 3 | 0.2045 |  | Phenylalanine hydroxylase |
| GEN-0779 | PAK1 | S | 2 |  |  | p21 (RAC1) activated kinase 1 |
| GEN-0780 | PAK2 | 2 | 2 |  |  | p21 (RAC1) activated kinase 2 |
| GEN-0781 | PAPOLG | 2 | 2 |  |  | poly(A) polymerase gamma |
| GEN-0782 | PARD3B | 2 | 3 | 0.2661 |  | Par-3 partitioning defective 3 homolog B (C. elegans) |
| GEN-0783 | PATJ | 2 | 2 |  |  | PATJ, crumbs cell polarity complex component |
| GEN-0784 | PAX5 | 1 | 3 |  |  | Paired box 5 |
| GEN-0785 | PAX6 | S | 3 | 0.2735 |  | Paired box 6 |
| GEN-0786 | PBX1 | 2 | 2 | 0.3431 |  | PBX homeobox 1 |
| GEN-0787 | PC | 3 | 2 |  |  | pyruvate carboxylase |
| GEN-0788 | PCCA | S | 3 |  |  | propionyl-CoA carboxylase alpha subunit |
| GEN-0789 | PCCB | S | 3 |  |  | propionyl-CoA carboxylase beta subunit |
| GEN-0790 | PCDH10 | 2 | 3 |  |  | protocadherin 10 |
| GEN-0791 | PCDH11X | 2 | 2 |  |  | protocadherin 11 X-linked |
| GEN-0792 | PCDH15 | 2 | 4 |  |  | protocadherin related 15 |
| GEN-0793 | PCDH19 | S | 5 |  |  | protocadherin 19 |
| GEN-0794 | PCDH9 | 2 | 3 |  |  | protocadherin 9 |
| GEN-0795 | PCDHA1 | 2 | 2 |  |  | Protocadherin alpha 1 |
| GEN-0796 | PCDHA10 | 2 | 2 |  |  | Protocadherin alpha 10 |
| GEN-0797 | PCDHA11 | 2 | 2 |  |  | Protocadherin alpha 11 |
| GEN-0798 | PCDHA12 | 2 | 2 |  |  | Protocadherin alpha 12 |
| GEN-0799 | PCDHA13 | 2 | 2 |  |  | Protocadherin alpha 13 |
| GEN-0800 | PCDHA2 | 2 | 2 |  |  | Protocadherin alpha 2 |
| GEN-0801 | PCDHA3 | 2 | 2 |  |  | Protocadherin alpha 3 |
| GEN-0802 | PCDHA4 | 2 | 2 |  |  | Protocadherin alpha 4 |
| GEN-0803 | PCDHA5 | 2 | 2 |  |  | Protocadherin alpha 5 |
| GEN-0804 | PCDHA6 | 2 | 1 |  |  | Protocadherin alpha 6 |
| GEN-0805 | PCDHA7 | 2 | 2 |  |  | Protocadherin alpha 7 |
| GEN-0806 | PCDHA8 | 2 | 2 |  |  | Protocadherin alpha 8 |
| GEN-0807 | PCDHA9 | 2 | 2 |  |  | Protocadherin alpha 9 |
| GEN-0808 | PCDHAC1 | 2 | 2 |  |  | Protocadherin alpha subfamily C, 1 |
| GEN-0809 | PCDHAC2 | 2 | 1 |  |  | Protocadherin alpha subfamily C, 2 |
| GEN-0810 | PCLO | 2 | 3 | 0.3021 |  | piccolo presynaptic cytomatrix protein |
| GEN-0811 | PCM1 | 2 | 2 |  |  | pericentriolar material 1 |
| GEN-0812 | PDCD1 | 2 | 1 |  |  | programmed cell death 1 |
| GEN-0813 | PDE1C | 2 | 1 |  |  | phosphodiesterase 1C |
| GEN-0814 | PDE3B | 3 | 2 |  |  | phosphodiesterase 3B |
| GEN-0815 | PDHA1 | 3 | 2 |  |  | pyruvate dehydrogenase E1 subunit alpha 1 |
| GEN-0816 | PDK2 | 2 | 2 |  |  | pyruvate dehydrogenase kinase 2 |
| GEN-0817 | PDZD8 | S | 2 |  |  | PDZ domain containing 8 |
| GEN-0818 | PEBP4 | 3 | 1 |  |  | phosphatidylethanolamine binding protein 4 |
| GEN-0819 | PER1 | 2 | 3 |  |  | period homolog 1 (Drosophila) |
| GEN-0820 | PER2 | 2 | 2 |  |  | period circadian clock 2 |
| GEN-0821 | PEX7 | 2 | 2 |  |  | peroxisomal biogenesis factor 7 |
| GEN-0822 | PHF12 | 1 | 2 |  |  | PHD finger protein 12 |
| GEN-0823 | PHF14 | 3 | 2 | 0.1857 |  | PHD finger protein 14 |
| GEN-0824 | PHF2 | 1 | 2 |  |  | PHD finger protein 2 |
| GEN-0825 | PHF21A | S | 5 |  |  | PHD finger protein 21A |
| GEN-0826 | PHF3 | 1 | 2 |  |  | PHD finger protein 3 |
| GEN-0827 | PHF7 | 2 | 1 |  |  | PHD finger protein 7 |
| GEN-0828 | PHF8 | S | 4 |  |  | PHD finger protein 8 |
| GEN-0829 | PHIP | S | 5 |  |  | pleckstrin homology domain interacting protein |
| GEN-0830 | PHLPP1 | 3 | 2 |  |  | PH domain and leucine rich repeat protein phosphatase 1 |
| GEN-0831 | PHRF1 | 2 | 2 |  |  | PHD and ring finger domains 1 |
| GEN-0832 | PIK3CA | 3 | 3 |  |  | phosphatidylinositol-4,5-bisphosphate 3-kinase catalytic subunit alpha |
| GEN-0833 | PIK3CG | 2 | 2 |  |  | phosphoinositide-3-kinase, catalytic, gamma polypeptide |
| GEN-0834 | PIK3R2 | S | 3 |  |  | phosphoinositide-3-kinase regulatory subunit 2 |
| GEN-0835 | PITX1 | 2 | 2 | 0.0335 |  | paired-like homeodomain 1 |
| GEN-0836 | PJA1 | S | 2 | 0.3445 |  | praja ring finger ubiquitin ligase 1 |
| GEN-0837 | PKD1 | 3 | 3 |  |  | polycystin 1, transient receptor potential channel interacting |
| GEN-0838 | PLAA | 3 | 2 |  |  | phospholipase A2 activating protein |
| GEN-0839 | PLAUR | 2 | 1 |  |  | Plasminogen activator, urokinase receptor |
| GEN-0840 | PLCB1 | 2 | 2 |  |  | phospholipase C, beta 1 (phosphoinositide-specific) |
| GEN-0841 | PLCD4 | 2 | 2 |  |  | phospholipase C delta 4 |
| GEN-0842 | PLEKHA8 | 3 | 1 |  |  | pleckstrin homology domain containing A8 |
| GEN-0843 | PLN | 2 | 2 |  |  | phospholamban |
| GEN-0844 | PLPPR4 | 3 | 2 |  |  | phospholipid phosphatase related 4 |
| GEN-0845 | PLXNA3 | 2 | 3 | 0.161 |  | plexin A3 |
| GEN-0846 | PLXNA4 | 2 | 2 |  |  | Plexin A4 |
| GEN-0847 | PLXNB1 | 2 | 2 |  |  | plexin B1 |
| GEN-0848 | PNPLA7 | 2 | 2 |  |  | patatin like phospholipase domain containing 7 |
| GEN-0849 | POGZ | S | 5 | 0.5726 |  | Pogo transposable element with ZNF domain |
| GEN-0850 | PHB1 | 2 | 1 |  |  | prohibitin 1 |
| GEN-0851 | POLA2 | 2 | 2 |  |  | DNA polymerase alpha 2, accessory subunit |
| GEN-0852 | POLR2A | S | 3 | 0.3696 |  | RNA polymerase II subunit A |
| GEN-0853 | POLR3A | S | 3 |  |  | RNA polymerase III subunit A |
| GEN-0854 | POMGNT1 | S | 3 |  |  | protein O-linked mannose N-acetylglucosaminyltransferase 1 (beta 1,2-) |
| GEN-0855 | POMT1 | 2 | 2 |  |  | protein O-mannosyltransferase 1 |
| GEN-0856 | PON1 | 2 | 2 |  |  | paraoxonase 1 |
| GEN-0857 | POT1 | 2 | 1 |  |  | Protection of telomeres 1 homolog (S. pombe) |
| GEN-0858 | POU3F3 | S | 2 |  |  | POU class 3 homeobox 3 |
| GEN-0859 | PPFIA1 | 2 | 2 |  |  | PTPRF interacting protein alpha 1 |
| GEN-0860 | PPFIA3 | S | 2 |  |  | PTPRF interacting protein alpha 3 |
| GEN-0861 | PPM1D | S | 3 |  |  | protein phosphatase, Mg2+/Mn2+ dependent 1D |
| GEN-0862 | PPP1R1B | 2 | 1 |  |  | Protein phosphatase 1, regulatory (inhibitor) subunit 1B |
| GEN-0863 | PPP1R9B | 1 | 2 |  |  | protein phosphatase 1 regulatory subunit 9B |
| GEN-0864 | PPP2CA | S | 2 |  |  | protein phosphatase 2 catalytic subunit alpha |
| GEN-0865 | PPP2R1B | 2 | 2 |  |  | protein phosphatase 2 regulatory subunit A, beta |
| GEN-0866 | PPP2R5C | S | 2 |  |  | protein phosphatase 2 regulatory subunit B'gamma |
| GEN-0867 | PPP2R5D | S | 5 |  |  | Protein phosphatase 2, regulatory subunit B', delta |
| GEN-0868 | PPP3CA | S | 3 |  |  | protein phosphatase 3 catalytic subunit alpha |
| GEN-0869 | PPP5C | 1 | 1 |  |  | protein phosphatase 5 catalytic subunit |
| GEN-0870 | PREX1 | 2 | 2 |  |  | Phosphatidylinositol-3,4,5-trisphosphate-dependent Rac exchange factor 1 |
| GEN-0871 | PRICKLE1 | 2 | 2 |  |  | Prickle homolog 1 (Drosophila) |
| GEN-0872 | PRICKLE2 | 2 | 2 |  |  | prickle planar cell polarity protein 2 |
| GEN-0873 | PRKAR1B | 2 | 2 |  |  | protein kinase cAMP-dependent type I regulatory subunit beta |
| GEN-0874 | PRKCA | 2 | 2 |  |  | protein kinase C alpha |
| GEN-0875 | PRKCB | 2 | 2 |  |  | protein kinase C beta |
| GEN-0876 | PRKD1 | S | 2 |  |  | Protein kinase D1 |
| GEN-0877 | PRKD2 | 2 | 1 |  |  | protein kinase D2 |
| GEN-0878 | PRKDC | 2 | 2 |  |  | protein kinase, DNA-activated, catalytic polypeptide |
| GEN-0879 | PRKN | 2 | 4 | 0.339 |  | parkin RBR E3 ubiquitin protein ligase |
| GEN-0880 | PRMT9 | 1 | 1 |  |  | protein arginine methyltransferase 9 |
| GEN-0881 | PRODH | S | 3 |  |  | Proline dehydrogenase (oxidase) 1 |
| GEN-0882 | PRPF19 | 3 | 1 |  |  | pre-mRNA processing factor 19 |
| GEN-0883 | PRPF39 | 2 | 1 |  |  | pre-mRNA processing factor 39 |
| GEN-0884 | PRPF8 | S | 3 |  |  | pre-mRNA processing factor 8 |
| GEN-0885 | PRR12 | S | 3 | 0.4863 |  | proline rich 12 |
| GEN-0886 | PRR14L | 1 | 2 |  |  | proline rich 14 like |
| GEN-0887 | PRR25 | 3 | 1 |  |  | proline rich 25 |
| GEN-0888 | PRUNE2 | 2 | 3 |  |  | prune homolog 2 |
| GEN-0889 | PSD3 | 2 | 2 |  |  | pleckstrin and Sec7 domain containing 3 |
| GEN-0890 | PSMC5 | 3 | 1 |  |  | proteasome 26S subunit, ATPase 5 |
| GEN-0891 | PSMD11 | 1 | 1 |  |  | proteasome 26S subunit, non-ATPase 11 |
| GEN-0892 | PSMD12 | S | 2 |  |  | proteasome 26S subunit, non-ATPase 12 |
| GEN-0893 | PSMD6 | 1 | 1 |  |  | proteasome 26S subunit, non-ATPase 6 |
| GEN-0894 | PTBP2 | 2 | 2 | 0.2842 |  | polypyrimidine tract binding protein 2 |
| GEN-0895 | PTCH1 | 3 | 3 |  |  | patched 1 |
| GEN-0896 | PTCHD1 | 1 | 5 | 0.634 |  | patched domain containing 1 |
| GEN-0897 | PTCHD1-AS | 2 | 1 |  |  | PTCHD1antisense RNA (head to head) |
| GEN-0898 | PTDSS1 | 3 | 2 |  |  | phosphatidylserine synthase 1 |
| GEN-0899 | PTGS2 | 2 | 2 |  |  | prostaglandin-endoperoxide synthase 2 |
| GEN-0900 | PTK7 | 1 | 2 |  |  | Protein tyrosine kinase 7 (inactive) |
| GEN-0901 | PTPN11 | S | 5 | 0.2671 |  | protein tyrosine phosphatase, non-receptor type 11 |
| GEN-0902 | PTPN4 | S | 2 |  |  | protein tyrosine phosphatase non-receptor type 4 |
| GEN-0903 | PTPRB | 2 | 2 |  |  | protein tyrosine phosphatase, receptor type B |
| GEN-0904 | PTPRC | 2 | 3 |  |  | protein tyrosine phosphatase, receptor type, C |
| GEN-0905 | PTPRD | 2 | 3 |  |  | protein tyrosine phosphatase receptor type D |
| GEN-0906 | PTPRS | 3 | 3 |  |  | protein tyrosine phosphatase receptor type S |
| GEN-0907 | PTPRT | 2 | 3 | 0.3339 |  | protein tyrosine phosphatase, receptor type, T |
| GEN-0908 | PUF60 | S | 2 |  |  | poly(U) binding splicing factor 60 |
| GEN-0909 | PXDN | 2 | 3 |  |  | peroxidasin |
| GEN-0910 | PYHIN1 | 2 | 1 |  |  | Pyrin and HIN domain family, member 1 |
| GEN-0911 | QRICH1 | 2 | 4 |  |  | glutamine rich 1 |
| GEN-0912 | RAB11FIP4 | 3 | 1 |  |  | RAB11 family interacting protein 4 |
| GEN-0913 | RAB11FIP5 | 2 | 2 |  |  | RAB11 family interacting protein 5 |
| GEN-0914 | RAB2A | 2 | 2 |  |  | RAB2A, member RAS oncogene family |
| GEN-0915 | RAB39B | 2 | 4 |  |  | RAB39B, member RAS oncogene family |
| GEN-0916 | RAB43 | 2 | 1 |  |  | RAB43, member RAS oncogene family |
| GEN-0917 | RAC1 | S | 3 |  |  | Rac family small GTPase 1 |
| GEN-0918 | RAD21 | S | 2 |  |  | RAD21cohesin complex component |
| GEN-0919 | RAD21L1 | 2 | 1 |  |  | RAD21 cohesin complex component like 1 |
| GEN-0920 | RAI1 | S | 5 | 0.204 |  | retinoic acid induced 1 |
| GEN-0921 | RALA | S | 2 |  |  | RAS like proto-oncogene A |
| GEN-0922 | RALGAPB | 1 | 2 |  |  | Ral GTPase activating protein non-catalytic beta subunit |
| GEN-0923 | RANBP17 | 2 | 3 | 0.1469 |  | RAN binding protein 17 |
| GEN-0924 | RAP1A | 3 | 1 |  |  | RAP1A, member of RAS oncogene family |
| GEN-0925 | RAPGEF4 | 2 | 4 |  |  | Rap guanine nucleotide exchange factor (GEF) 4 |
| GEN-0926 | RASSF5 | 2 | 1 |  |  | Ras association domain family member 5 |
| GEN-0927 | RBBP5 | 2 | 2 |  |  | RB binding protein 5, histone lysine methyltransferase complex subunit |
| GEN-0928 | RBFOX1 | 2 | 4 | 0.3819 |  | RNA binding protein, fox-1 homolog (C. elegans) 1 |
| GEN-0929 | RBM27 | 2 | 2 |  |  | RNA binding motif protein 27 |
| GEN-0930 | REEP3 | 2 | 1 |  |  | receptor accessory protein 3 |
| GEN-0931 | RELN | 1 | 5 |  |  | Reelin |
| GEN-0932 | RERE | S | 5 | 0.2927 |  | Arginine-glutamic acid dipeptide (RE) repeats |
| GEN-0933 | RFX3 | 1 | 3 | 0.4123 |  | regulatory factor X3 |
| GEN-0934 | RFX4 | S | 2 | 0.3702 |  | regulatory factor X4 |
| GEN-0935 | RFX7 | S | 1 |  |  | regulatory factor X7 |
| GEN-0936 | RGS7 | 2 | 2 |  |  | regulator of G-protein signaling 7 |
| GEN-0937 | RHEB | S | 1 |  |  | Ras homolog, mTORC1 binding |
| GEN-0938 | RHOXF1 | 2 | 1 |  |  | Rhox homeobox family, member 1 |
| GEN-0939 | RICTOR | 3 | 1 |  |  | RPTOR independent companion of MTOR complex 2 |
| GEN-0940 | RIMS1 | 1 | 3 | 0.2845 |  | Regulating synaptic membrane exocytosis 1 |
| GEN-0941 | RIMS2 | S | 2 |  |  | regulating synaptic membrane exocytosis 2 |
| GEN-0942 | RIMS3 | 2 | 1 |  |  | regulating synaptic membrane exocytosis 3 |
| GEN-0943 | RIT2 | 2 | 1 |  |  | Ras-like without CAAX 2 |
| GEN-0944 | RLIM | S | 2 |  |  | Ring finger protein, LIM domain interacting |
| GEN-0945 | RNF135 | S | 2 | 0.3436 |  | Ring finger protein 135 |
| GEN-0946 | RNF25 | 2 | 1 |  |  | ring finger protein 25 |
| GEN-0947 | RNF38 | 2 | 1 |  |  | ring finger protein 38 |
| GEN-0948 | RNU2-2 | S | 1 |  |  | RNA, U2 small nuclear 2 |
| GEN-0949 | RNU4-2 | S | 4 |  |  | RNA, U4 small nuclear 2 |
| GEN-0950 | RNU5B-1 | S | 1 |  |  | RNA, U5B small nuclear 1 |
| GEN-0951 | ROBO2 | 2 | 3 |  |  | roundabout guidance receptor 2 |
| GEN-0952 | RORA | S | 5 | 0.2906 |  | RAR-related orphan receptor A |
| GEN-0953 | RORB | S | 4 | 0.1756 |  | RAR related orphan receptor B |
| GEN-0954 | RP11-1407O15.2 | 2 | 1 |  |  |  |
| GEN-0955 | RPH3A | 3 | 2 |  |  | rabphilin 3A |
| GEN-0956 | RPL10 | 2 | 3 | 0.3731 |  | ribosomal protein L10 |
| GEN-0957 | RPS6KA2 | 2 | 2 | 0.333 |  | ribosomal protein S6 kinase, 90kDa, polypeptide 2 |
| GEN-0958 | RPS6KA3 | S | 5 |  |  | Ribosomal protein S6 kinase, 90kDa, polypeptide 3 |
| GEN-0959 | RSRC1 | S | 2 | 0.4071 |  | arginine and serine rich coiled-coil 1 |
| GEN-0960 | RUNX1T1 | 1 | 2 | 0.3056 |  | RUNX1 partner transcriptional co-repressor 1 |
| GEN-0961 | SACS | 2 | 3 |  |  | sacsin molecular chaperone |
| GEN-0962 | SAE1 | 2 | 1 |  |  | SUMO1 activating enzyme subunit 1 |
| GEN-0963 | SAMD11 | 2 | 1 |  |  | sterile alpha motif domain containing 11 |
| GEN-0964 | SASH1 | 2 | 1 |  |  | SAM and SH3 domain containing 1 |
| GEN-0965 | RPS10P2-AS1 | 2 | 1 |  |  | ribosomal protein S10 pseudogene 2 anti-sense 1 |
| GEN-0966 | SATB1 | S | 2 | 0.1426 |  | SATB homeobox 1 |
| GEN-0967 | SATB2 | S | 5 | 0.2635 |  | SATB homeobox 2 |
| GEN-0968 | SBF1 | 2 | 3 | 0.2661 |  | SET binding factor 1 |
| GEN-0969 | SCAF1 | 2 | 1 |  |  | SR-related CTD associated factor 1 |
| GEN-0970 | SCAF4 | S | 2 |  |  | SR-related CTD associated factor 4 |
| GEN-0971 | SCFD2 | 2 | 2 |  |  | sec1 family domain containing 2 |
| GEN-0972 | SCGN | 3 | 1 |  |  | secretagogin, EF-hand calcium binding protein |
| GEN-0973 | SCN1A | S | 5 | 0.4556 |  | sodium channel, voltage-gated, type I, alpha subunit |
| GEN-0974 | SCN2A | 1 | 5 | 0.5425 |  | sodium channel, voltage-gated, type II, alpha subunit |
| GEN-0975 | SCN3A | 3 | 3 |  |  | sodium voltage-gated channel alpha subunit 3 |
| GEN-0976 | SCN4A | 2 | 2 |  |  | Sodium channel, voltage gated, type IV alpha subunit |
| GEN-0977 | SCN8A | 1 | 5 | 0.3187 |  | sodium channel, voltage gated, type VIII, alpha subunit |
| GEN-0978 | SCN9A | 2 | 4 |  |  | sodium voltage-gated channel alpha subunit 9 |
| GEN-0979 | SCP2 | 2 | 1 |  |  | sterol carrier protein 2 |
| GEN-0980 | SDC2 | 2 | 1 |  |  | syndecan 2 (heparan sulfate proteoglycan 1, cell surface-associated, fibroglycan ) |
| GEN-0981 | SEMA5A | 2 | 4 |  |  | sema domain, seven thrombospondin repeats (type 1 and type 1-like), transmembrane domain (TM) and short cytoplasmic domain, (semaphorin) 5A |
| GEN-0982 | SENP1 | 3 | 1 |  |  | SUMO specific peptidase 1 |
| GEN-0983 | SENP6 | 3 | 1 |  |  | SUMO specific peptidase 6 |
| GEN-0984 | SERPINE1 | 2 | 1 |  |  | serpin family E member 1 |
| GEN-0985 | SET | 2 | 2 |  |  | SETnuclear proto-oncogene |
| GEN-0986 | SETBP1 | 1 | 5 |  |  | SET binding protein 1 |
| GEN-0987 | SETD1A | S | 4 | 0.2672 |  | SET domain containing 1A, histone lysine methyltransferase |
| GEN-0988 | SETD1B | S | 5 |  |  | SET domain containing 1B |
| GEN-0989 | SETD2 | 1 | 5 | 0.2983 |  | SET domain containing 2 |
| GEN-0990 | SETD5 | S | 5 | 0.2965 |  | SET domain containing 5 |
| GEN-0991 | SETDB1 | 2 | 2 |  |  | SET domain, bifurcated 1 |
| GEN-0992 | SETDB2 | 2 | 1 |  |  | SET domain, bifurcated 2 |
| GEN-0993 | SEZ6L2 | 2 | 2 |  |  | SEZ6L2 seizure related 6 homolog (mouse)-like 2 |
| GEN-0994 | SF1 | 1 | 1 |  |  | splicing factor 1 |
| GEN-0995 | SF3B1 | 2 | 2 | 0.1833 |  | splicing factor 3b subunit 1 |
| GEN-0996 | SGSH | S | 3 |  |  | N-sulfoglucosamine sulfohydrolase |
| GEN-0997 | SGSM3 | 2 | 2 |  |  | Small G protein signaling modulator 3 |
| GEN-0998 | SH3RF1 | 3 | 2 |  |  | SH3 domain containing ring finger 1 |
| GEN-0999 | SH3RF3 | 2 | 2 |  |  | SH3 domain containing ring finger 3 |
| GEN-1000 | SHANK1 | 2 | 4 | 0.5779 |  | SH3 and multiple ankyrin repeat domains 1 |
| GEN-1001 | SHANK2 | 1 | 5 | 0.7253 |  | SH3 and multiple ankyrin repeat domains 2 |
| GEN-1002 | SHOX | 2 | 1 |  |  | short stature homeobox |
| GEN-1003 | SIK1 | S | 2 |  |  | Salt-inducible kinase 1 |
| GEN-1004 | SIN3A | S | 4 | 0.3932 |  | SIN3 transcription regulator family member A |
| GEN-1005 | SIN3B | S | 2 |  |  | SIN3 transcription regulator family member B |
| GEN-1006 | SKI | 1 | 2 |  |  | SKIproto-oncogene |
| GEN-1007 | SLC12A5 | 2 | 3 |  |  | Solute carrier family 12 (potassium/chloride transporter), member 5 |
| GEN-1008 | SLC1A1 | 2 | 4 |  |  | solute carrier family 1 (neuronal/epithelial high affinity glutamate transporter, system Xag), member 1 |
| GEN-1009 | SLC1A2 | 3 | 3 |  |  | Solute carrier family 1 (glial high affinity glutamate transporter), member 2 |
| GEN-1010 | SLC22A9 | 2 | 2 |  |  | solute carrier family 22 member 9 |
| GEN-1011 | SLC23A1 | 3 | 2 |  |  | solute carrier family 23 member 1 |
| GEN-1012 | SLC24A2 | 2 | 1 |  |  | solute carrier family 24 member 2 |
| GEN-1013 | SLC25A12 | 2 | 4 |  |  | solute carrier family 25 (mitochondrial carrier, Aralar), member 12 |
| GEN-1014 | SLC25A39 | 2 | 1 |  |  | solute carrier family 25 member 39 |
| GEN-1015 | SLC27A4 | 2 | 1 |  |  | Solute carrier family 27 (fatty acid transporter), member 4 |
| GEN-1016 | SLC29A4 | 2 | 1 |  |  | solute carrier family 29 member 4 |
| GEN-1017 | SLC35G1 | 2 | 1 |  |  | solute carrier family 35 member G1 |
| GEN-1018 | SLC38A10 | 2 | 1 |  |  | solute carrier family 38, member 10 |
| GEN-1019 | SLC45A1 | S | 2 |  |  | solute carrier family 45 member 1 |
| GEN-1020 | SLC4A10 | 2 | 3 |  |  | solute carrier family 4, sodium bicarbonate transporter-like, member 10 |
| GEN-1021 | SLC6A1 | S | 5 | 0.2693 |  | Solute carrier family 6 (neurotransmitter transporter), member 1 |
| GEN-1022 | SLC6A3 | 2 | 4 |  |  | Solute carrier family 6 (neurotransmitter transporter), member 3 |
| GEN-1023 | SLC6A4 | 2 | 4 | 0.399 |  | solute carrier family 6 (neurotransmitter transporter, serotonin), member 4 |
| GEN-1024 | SLC6A8 | 2 | 4 |  |  | solute carrier family 6 (neurotransmitter transporter, creatine), member 8 |
| GEN-1025 | SLC7A3 | 2 | 1 |  |  | Solute carrier family 7 (cationic amino acid transporter, y+ system), member 3 |
| GEN-1026 | SLC7A5 | 2 | 2 |  |  | solute carrier family 7 member 5 |
| GEN-1027 | SLC7A7 | 2 | 2 |  |  | solute carrier family 7 member 7 |
| GEN-1028 | SLC9A1 | S | 2 |  |  | solute carrier family 9 member A1 |
| GEN-1029 | SLC9A6 | S | 5 |  |  | solute carrier family 9 (sodium/hydrogen exchanger), member 6 |
| GEN-1030 | SLC9A9 | 2 | 4 | 0.5281 |  | solute carrier family 9 (sodium/hydrogen exchanger), member 9 |
| GEN-1031 | SLCO1B3 | 2 | 2 |  |  | Solute carrier organic anion transporter family, member 1B3 |
| GEN-1032 | SLFN5 | 3 | 1 |  |  | schlafen family member 5 |
| GEN-1033 | SLITRK2 | S | 2 |  |  | SLIT and NTRK like family member 2 |
| GEN-1034 | SLITRK5 | 2 | 3 | 0.4172 |  | SLIT and NTRK like family member 5 |
| GEN-1035 | SMAD4 | 2 | 4 |  |  | SMAD family member 4 |
| GEN-1036 | SMAP2 | 2 | 2 |  |  | small ArfGAP2 |
| GEN-1037 | SMARCA1 | 1 | 1 |  |  | SNF2 related chromatin remodeling ATPase 1 |
| GEN-1038 | SMARCA2 | S | 5 |  |  | SWI/SNF related, matrix associated, actin dependent regulator of chromatin, subfamily a, member 2 |
| GEN-1039 | SMARCA4 | 1 | 5 |  |  | SWI/SNF related, matrix associated, actin dependent regulator of chromatin, subfamily a, member 4 |
| GEN-1040 | SMARCC2 | S | 5 |  |  | SWI/SNF related, matrix associated, actin dependent regulator of chromatin, subfamily c, member 2 |
| GEN-1041 | SMC1A | S | 5 |  |  | structural maintenance of chromosomes 1A |
| GEN-1042 | SMC3 | S | 4 | 0.2592 |  | structural maintenance of chromosomes 3 |
| GEN-1043 | SMG6 | 2 | 2 |  |  | SMG6, nonsense mediated mRNA decay factor |
| GEN-1044 | SMURF1 | 2 | 1 |  |  | SMAD specific E3 ubiquitin protein ligase 1 |
| GEN-1045 | SNAP25 | 2 | 3 |  |  | Synaptosomal-associated protein, 25kDa |
| GEN-1046 | SNCAIP | 3 | 1 |  |  | synuclein alpha interacting protein |
| GEN-1047 | SND1 | 2 | 3 |  |  | staphylococcal nuclease and tudor domain containing 1 |
| GEN-1048 | SNTG2 | 2 | 2 |  |  | syntrophin gamma 2 |
| GEN-1049 | SNX14 | S | 3 |  |  | Sorting nexin 14 |
| GEN-1050 | SNX5 | 2 | 2 |  |  | sorting nexin 5 |
| GEN-1051 | SOD1 | 2 | 1 |  |  | superoxide dismutase 1 |
| GEN-1052 | SON | S | 5 |  |  | SONDNA binding protein |
| GEN-1053 | SORCS3 | 2 | 2 | 0.4421 |  | sortilin related VPS10 domain containing receptor 3 |
| GEN-1054 | SOS2 | 1 | 2 |  |  | SOS Ras/Rho guanine nucleotide exchange factor 2 |
| GEN-1055 | SOX5 | S | 5 |  |  | SRY-box 5 |
| GEN-1056 | SOX6 | S | 2 |  |  | SRY-box transcription factor 6 |
| GEN-1057 | SPARCL1 | 2 | 2 |  |  | SPARC like 1 |
| GEN-1058 | SPAST | 1 | 4 |  |  | Spastin |
| GEN-1059 | SPEN | 2 | 4 | 0.2696 |  | spenfamily transcriptional repressor |
| GEN-1060 | SPP2 | 2 | 1 |  |  | secreted phosphoprotein 2 |
| GEN-1061 | SPRY2 | 2 | 1 |  |  | sprouty RTK signaling antagonist 2 |
| GEN-1062 | SPTAN1 | 3 | 3 |  |  | spectrin alpha, non-erythrocytic 1 |
| GEN-1063 | SPTBN1 | S | 4 |  |  | spectrin beta, non-erythrocytic 1 |
| GEN-1064 | SRCAP | 1 | 4 | 0.1609 |  | Snf2 related CREBBP activator protein |
| GEN-1065 | SRGAP3 | 2 | 2 |  |  | SLIT-ROBO Rho GTPase activating protein 3 |
| GEN-1066 | SRPRA | 1 | 1 |  |  | SRP receptor subunit alpha |
| GEN-1067 | SRRM2 | S | 4 |  |  | serine/arginine repetitive matrix 2 |
| GEN-1068 | SRSF1 | S | 1 |  |  | serine and arginine rich splicing factor 1 |
| GEN-1069 | SRSF11 | 2 | 2 |  |  | serine and arginine rich splicing factor 11 |
| GEN-1070 | SSR4 | 3 | 1 |  |  | signal sequence receptor subunit 4 |
| GEN-1071 | SSRP1 | 2 | 1 |  |  | structure specific recognition protein 1 |
| GEN-1072 | ST7 | 2 | 1 |  |  | suppression of tumorigenicity 7 |
| GEN-1073 | ST8SIA2 | 2 | 3 |  |  | ST8 alpha-N-acetyl-neuraminide alpha-2,8-sialyltransferase 2 |
| GEN-1074 | STAG1 | S | 3 | 0.2968 |  | stromal antigen 1 |
| GEN-1075 | STX1A | 2 | 2 | 0.4421 |  | Syntaxin 1A (brain) |
| GEN-1076 | STXBP1 | S | 5 | 0.4642 |  | Syntaxin binding protein 1 |
| GEN-1077 | SLC22A15 | 2 | 1 |  |  | Solute carrier family 22, member 15 |
| GEN-1078 | SLC25A27 | 2 | 1 |  |  | solute carrier family 25 member 27 |
| GEN-1079 | SLC35B1 | 2 | 1 |  |  | solute carrier family 35 member B1 |
| GEN-1080 | STK39 | 2 | 2 |  |  | serine threonine kinase 39 (STE20/SPS1 homolog, yeast) |
| GEN-1081 | STXBP5 | 2 | 2 |  |  | Syntaxin binding protein 5 (tomosyn) |
| GEN-1082 | STYK1 | 2 | 1 |  |  | Serine/threonine/tyrosine kinase 1 |
| GEN-1083 | SUPT16H | S | 3 |  |  | SPT16 homolog, facilitates chromatin remodeling subunit |
| GEN-1084 | SYAP1 | 2 | 1 |  |  | Synapse associated protein 1 |
| GEN-1085 | SYBU | 3 | 1 |  |  | syntabulin |
| GEN-1086 | SYCE1 | 3 | 1 |  |  | synaptonemal complex central element protein 1 |
| GEN-1087 | SYN1 | 1 | 5 |  |  | Synapsin 1 |
| GEN-1088 | SYN2 | 2 | 2 |  |  | Synapsin II |
| GEN-1089 | SYNCRIP | 2 | 3 | 0.5203 |  | synaptotagmin binding cytoplasmic RNA interacting protein |
| GEN-1090 | SYNE1 | 2 | 4 | 0.2949 |  | spectrin repeat containing, nuclear envelope 1 |
| GEN-1091 | SYNGAP1 | S | 5 |  |  | synaptic Ras GTPase activating protein 1 |
| GEN-1092 | SYNJ1 | 2 | 1 |  |  | synaptojanin 1 |
| GEN-1093 | SYP | 3 | 2 |  |  | synaptophysin |
| GEN-1094 | SYT1 | S | 3 | 0.3135 |  | synaptotagmin 1 |
| GEN-1095 | SYT17 | 2 | 2 |  |  | synaptotagmin XVII |
| GEN-1096 | TAF1 | S | 4 |  |  | TATA-box binding protein associated factor 1 |
| GEN-1097 | TAF1C | 2 | 2 |  |  | TATA-box binding protein associated factor, RNA polymerase I subunit C |
| GEN-1098 | TAF4 | S | 2 |  |  | TATA-box binding protein associated factor 4 |
| GEN-1099 | TAF6 | 2 | 2 |  |  | TATA-box binding protein associated factor 6 |
| GEN-1100 | TANC2 | S | 5 | 0.3692 |  | etratricopeptide repeat, ankyrin repeat and coiled-coil containing 2 |
| GEN-1101 | TAOK1 | S | 3 |  |  | TAO kinase 1 |
| GEN-1102 | TAOK2 | 2 | 3 | 0.1446 |  | TAO kinase 2 |
| GEN-1103 | TBC1D23 | S | 2 |  |  | TBC1 domain family member 23 |
| GEN-1104 | TBC1D31 | 2 | 2 |  |  | TBC1 domain family, member 31 |
| GEN-1105 | TBC1D5 | 2 | 3 |  |  | TBC1 domain family, member 5 |
| GEN-1106 | TBCB | 3 | 1 |  |  | tubulin folding cofactor B |
| GEN-1107 | TBCEL | 1 | 1 |  |  | tubulin folding cofactor E like |
| GEN-1108 | TBCK | S | 2 |  |  | TBC1 domain containing kinase |
| GEN-1109 | TBL1XR1 | 1 | 5 | 0.4074 |  | transducin beta like 1 X-linked receptor 1 |
| GEN-1110 | TBR1 | 1 | 5 | 0.8165 |  | T-box, brain, 1 |
| GEN-1111 | TBX1 | S | 2 |  |  | T-box 1 |
| GEN-1112 | TBX22 | 3 | 1 |  |  | T-box transcription factor 22 |
| GEN-1113 | TCEAL1 | S | 1 |  |  | transcription elongation factor A like 1 |
| GEN-1114 | TCF12 | 3 | 2 | 0.4255 |  | transcription factor 12 |
| GEN-1115 | TCF20 | S | 5 | 0.5059 |  | Transcription factor 20 (AR1) |
| GEN-1116 | TCF4 | S | 5 | 0.5166 |  | Transcription factor 4 |
| GEN-1117 | TCF7L2 | 1 | 3 | 0.4652 |  | Transcription factor 7-like 2 (T-cell specific, HMG-box) |
| GEN-1118 | TECTA | 2 | 3 |  |  | tectorin alpha |
| GEN-1119 | TEK | 1 | 1 |  |  | TEKreceptortyrosine kinase |
| GEN-1120 | TERB2 | 2 | 1 |  |  | telomere repeat binding bouquet formation protein 2 |
| GEN-1121 | TERF2 | 2 | 2 |  |  | Telomeric repeat binding factor 2 |
| GEN-1122 | TET2 | 2 | 2 | 0.3121 |  | Tet methylcytosine dioxygenase 2 |
| GEN-1123 | TET3 | S | 2 |  |  | tet methylcytosine dioxygenase 3 |
| GEN-1124 | TFB2M | 3 | 1 |  |  | transcription factor B2, mitochondrial |
| GEN-1125 | TFE3 | S | 2 |  |  | transcription factor binding to IGHM enhancer 3 |
| GEN-1126 | TGM1 | 3 | 1 |  |  | transglutaminase 1 |
| GEN-1127 | THBS1 | 2 | 2 | 0.3382 |  | Thrombospondin 1 |
| GEN-1128 | THRA | 2 | 2 |  |  | thyroid hormone receptor alpha |
| GEN-1129 | TLE3 | 1 | 2 |  |  | TLE family member 3, transcriptional corepressor |
| GEN-1130 | TLK2 | S | 5 | 0.1865 |  | tousled-like kinase 2 |
| GEN-1131 | TLN2 | 3 | 2 |  |  | talin 2 |
| GEN-1132 | TM4SF19 | 2 | 2 |  |  | transmembrane 4 L six family member 19 |
| GEN-1133 | TM4SF20 | S | 1 |  |  | Transmembrane 4 L six family member 20 |
| GEN-1134 | TM9SF4 | 1 | 2 |  |  | transmembrane 9 superfamily member 4 |
| GEN-1135 | TMEM134 | 3 | 1 |  |  | transmembrane protein 134 |
| GEN-1136 | TMEM39B | 2 | 2 |  |  | transmembrane protein 39B |
| GEN-1137 | TMLHE | 2 | 3 | 0.6367 |  | trimethyllysine hydroxylase, epsilon |
| GEN-1138 | TNPO3 | 3 | 2 |  |  | transportin 3 |
| GEN-1139 | TNRC6B | 2 | 4 | 0.4279 |  | Trinucleotide repeat containing 6B |
| GEN-1140 | TNRC6C | 2 | 2 |  |  | trinucleotide repeat containing adaptor 6C |
| GEN-1141 | TNS2 | 3 | 1 |  |  | tensin 2 |
| GEN-1142 | TOP2B | 2 | 2 | 0.263 |  | DNA topoisomerase II beta |
| GEN-1143 | TOP3B | 2 | 2 |  |  | Topoisomerase (DNA) III beta |
| GEN-1144 | TPO | 2 | 1 |  |  | Thyroid peroxidase |
| GEN-1145 | TRAF7 | S | 3 |  |  | TNF receptor associated factor 7 |
| GEN-1146 | TRAP1 | 3 | 1 |  |  | TNF receptor associated protein 1 |
| GEN-1147 | TRAPPC2L | 3 | 1 |  |  | trafficking protein particle complex 2 like |
| GEN-1148 | TRAPPC6B | S | 2 |  |  | trafficking protein particle complex 6B |
| GEN-1149 | TRAPPC9 | 2 | 4 | 0.4106 |  | trafficking protein particle complex 9 |
| GEN-1150 | TRIM23 | 1 | 2 |  |  | tripartite motif containing 23 |
| GEN-1151 | TRIM32 | 3 | 2 |  |  | tripartite motif containing 32 |
| GEN-1152 | TRIM33 | 2 | 1 |  |  | Tripartite motif containing 33 |
| GEN-1153 | TRIM8 | S | 2 |  |  | tripartite motif containing 8 |
| GEN-1154 | TRIO | 1 | 5 |  |  | Trio Rho guanine nucleotide exchange factor |
| GEN-1155 | TRIP12 | S | 5 |  |  | Thyroid hormone receptor interactor 12 |
| GEN-1156 | TRPC4 | 3 | 2 |  |  | transient receptor potential cation channel subfamily C member 4 |
| GEN-1157 | TRPC5 | 3 | 3 |  |  | transient receptor potential cation channel subfamily C member 5 |
| GEN-1158 | TRPC6 | 2 | 2 |  |  | Transient receptor potential cation channel, subfamily C, member 6 |
| GEN-1159 | TRPM1 | 2 | 2 |  |  | transient receptor potential cation channel subfamily M member 1 |
| GEN-1160 | TRPM3 | S | 4 |  |  | transient receptor potential cation channel subfamily M member 3 |
| GEN-1161 | TRPM6 | 3 | 2 |  |  | transient receptor potential cation channel subfamily M member 6 |
| GEN-1162 | TRPM7 | 3 | 2 |  |  | transient receptor potential cation channel subfamily M member 7 |
| GEN-1163 | TRRAP | S | 5 | 0.4183 |  | transformation/transcription domain associated protein |
| GEN-1164 | TBL1X | 2 | 1 |  |  | transducin (beta)-like 1X-linked |
| GEN-1165 | TDO2 | 2 | 1 |  |  | tryptophan 2,3-dioxygenase |
| GEN-1166 | TSHZ1 | 1 | 2 |  |  | teashirt zinc finger homeobox 1 |
| GEN-1167 | TSHZ3 | 1 | 2 | 0.2643 |  | teashirt zinc finger homeobox 3 |
| GEN-1168 | TSPAN17 | 2 | 1 |  |  | tetraspanin 17 |
| GEN-1169 | TSPAN4 | 2 | 2 |  |  | tetraspanin 4 |
| GEN-1170 | TSPAN7 | 2 | 3 |  |  | tetraspanin 7 |
| GEN-1171 | TSPOAP1 | 2 | 2 |  |  | TSPO associated protein 1 |
| GEN-1172 | TSPYL2 | 3 | 2 |  |  | TSPY like 2 |
| GEN-1173 | TTI2 | S | 1 |  |  | TELO2 interacting protein 2 |
| GEN-1174 | TTN | S | 5 |  |  | titin |
| GEN-1175 | TUBGCP5 | 2 | 2 |  |  | tubulin, gamma complex associated protein 5 |
| GEN-1176 | U2AF2 | 3 | 2 |  |  | U2 small nuclear RNA auxiliary factor 2 |
| GEN-1177 | UBAP2L | 1 | 2 |  |  | ubiquitin associated protein 2 like |
| GEN-1178 | UBE3A | S | 5 |  |  | ubiquitin protein ligase E3A |
| GEN-1179 | UBE3C | 2 | 2 |  |  | Ubiquitin protein ligase E3C |
| GEN-1180 | UBN2 | 2 | 2 | 0.2668 |  | ubinuclein 2 |
| GEN-1181 | UBR1 | 1 | 2 |  |  | ubiquitin protein ligase E3 component n-recognin 1 |
| GEN-1182 | UBR3 | 2 | 2 |  |  | ubiquitin protein ligase E3 component n-recognin 3 |
| GEN-1183 | UBR5 | 2 | 3 |  |  | ubiquitin protein ligase E3 component n-recognin 5 |
| GEN-1184 | UGGT1 | S | 2 |  |  | UDP-glucose glycoprotein glucosyltransferase 1 |
| GEN-1185 | UIMC1 | 2 | 2 |  |  | ubiquitin interaction motif containing 1 |
| GEN-1186 | UNC13A | S | 3 |  |  | unc-13 homolog A |
| GEN-1187 | UNC5D | 3 | 2 |  |  | unc-5 netrin receptor D |
| GEN-1188 | UNC79 | 2 | 3 |  |  | unc-79 homolog, NALCN channel complex subunit |
| GEN-1189 | UNC80 | 2 | 3 |  |  | unc-80 homolog, NALCN activator |
| GEN-1190 | UPF2 | 2 | 3 | 0.3347 |  | UPF2, regulator of nonsense mediated mRNA decay |
| GEN-1191 | UPF3B | S | 5 |  |  | UPF3B, regulator of nonsense mediated mRNA decay |
| GEN-1192 | USH2A | 2 | 3 |  |  | usherin |
| GEN-1193 | USP15 | 2 | 2 |  |  | ubiquitin specific peptidase 15 |
| GEN-1194 | USP24 | 3 | 3 |  |  | ubiquitin specific peptidase 24 |
| GEN-1195 | USP27X | 3 | 2 |  |  | ubiquitin specific peptidase 27 X-linked |
| GEN-1196 | USP30 | 3 | 1 |  |  | ubiquitin specific peptidase 30 |
| GEN-1197 | USP45 | 2 | 2 |  |  | Ubiquitin specific peptidase 45 |
| GEN-1198 | USP7 | S | 4 |  |  | Ubiquitin specific peptidase 7 (herpes virus-associated) |
| GEN-1199 | USP9X | S | 5 |  |  | ubiquitin specific peptidase 9 X-linked |
| GEN-1200 | USP9Y | 2 | 1 |  |  | ubiquitin specific peptidase 9, Y-linked |
| GEN-1201 | VAMP2 | S | 1 |  |  | vesicle associated membrane protein 2 |
| GEN-1202 | VCP | 3 | 2 |  |  | valosin containing protein |
| GEN-1203 | VEZF1 | 1 | 1 |  |  | vascular endothelial zinc finger 1 |
| GEN-1204 | VIL1 | 2 | 1 |  |  | Villin 1 |
| GEN-1205 | VPS13B | S | 5 | 0.3378 |  | vacuolar protein sorting 13 homolog B (yeast) |
| GEN-1206 | VPS54 | 3 | 1 |  |  | VPS54subunit of GARP complex |
| GEN-1207 | VSIG4 | 2 | 1 |  |  | V-set and immunoglobulin domain containing 4 |
| GEN-1208 | VWA7 | 3 | 1 |  |  | von Willebrand factor A domain containing 7 |
| GEN-1209 | WAC | S | 5 |  |  | WW domain containing adaptor with coiled-coil |
| GEN-1210 | WASF1 | S | 2 |  |  | WAS protein family member 1 |
| GEN-1211 | WDFY3 | 1 | 5 | 0.3232 |  | WD repeat and FYVE domain containing 3 |
| GEN-1212 | WDFY4 | 2 | 3 |  |  | WDFY family member 4 |
| GEN-1213 | WDR26 | S | 3 |  |  | WD repeat domain 26 |
| GEN-1214 | WDR37 | 3 | 2 | 0.3701 |  | WD repeat domain 37 |
| GEN-1215 | WDR5 | S | 1 |  |  | WD repeat domain 5 |
| GEN-1216 | WNK3 | 2 | 2 | 0.2674 |  | WNK lysine deficient protein kinase 3 |
| GEN-1217 | WNT1 | 2 | 2 |  |  | Wingless-type MMTV integration site family, member 1 |
| GEN-1218 | WWOX | 2 | 4 | 0.3415 |  | WW domain containing oxidoreductase |
| GEN-1219 | WWP1 | 3 | 1 |  |  | WW domain containing E3 ubiquitin protein ligase 1 |
| GEN-1220 | XPC | S | 3 |  |  | xeroderma pigmentosum, complementation group C |
| GEN-1221 | XPO1 | 2 | 3 |  |  | exportin 1 |
| GEN-1222 | XRCC6 | 3 | 1 |  |  | X-ray repair cross complementing 6 |
| GEN-1223 | YEATS2 | 2 | 2 |  |  | YEATS domain containing 2 |
| GEN-1224 | YTHDC2 | 2 | 2 |  |  | YTH domain containing 2 |
| GEN-1225 | YWHAE | 2 | 2 |  |  | tyrosine 3-monooxygenase/tryptophan 5-monooxygenase activation protein epsilon |
| GEN-1226 | YWHAG | S | 4 |  |  | tyrosine 3-monooxygenase/tryptophan 5-monooxygenase activation protein gamma |
| GEN-1227 | YWHAZ | 3 | 3 |  |  | tyrosine 3-monooxygenase/tryptophan 5-monooxygenase activation protein zeta |
| GEN-1228 | YY1 | S | 3 |  |  | YY1transcription factor |
| GEN-1229 | ZBTB16 | 2 | 1 | 0.0801 |  | Zinc finger and BTB domain containing 16 |
| GEN-1230 | ZBTB18 | S | 4 |  |  | zinc finger and BTB domain containing 18 |
| GEN-1231 | ZBTB20 | S | 5 |  |  | Zinc finger and BTB domain containing 20 |
| GEN-1232 | ZBTB21 | 1 | 1 |  |  | zinc finger and BTB domain containing 21 |
| GEN-1233 | ZBTB47 | 3 | 1 |  |  | zinc finger and BTB domain containing 47 |
| GEN-1234 | ZBTB7A | S | 1 |  |  | zinc finger and BTB domain containing 7A |
| GEN-1235 | ZC3H11A | 2 | 1 |  |  | zinc finger CCCH-type containing 11A |
| GEN-1236 | ZC3H4 | 2 | 2 |  |  | zinc finger CCCH-type containing 4 |
| GEN-1237 | ZEB2 | 3 | 2 |  |  | zinc finger E-box binding homeobox 2 |
| GEN-1238 | ZFHX3 | S | 4 |  |  | zinc finger homeobox 3 |
| GEN-1239 | UBE2H | 2 | 1 |  |  | ubiquitin-conjugating enzyme E2H (UBC8 homolog, yeast) |
| GEN-1240 | VASH1 | 2 | 1 |  |  | vasohibin 1 |
| GEN-1241 | ZFHX4 | S | 2 |  |  | zinc finger homeobox 4 |
| GEN-1242 | ZFX | S | 2 |  |  | zinc finger protein X-linked |
| GEN-1243 | ZFYVE26 | 2 | 2 |  |  | zinc finger FYVE-type containing 26 |
| GEN-1244 | ZFYVE9 | 3 | 2 |  |  | zinc finger FYVE-type containing 9 |
| GEN-1245 | ZMIZ1 | S | 3 |  |  | zinc finger MIZ-type containing 1 |
| GEN-1246 | ZMYM2 | S | 3 |  |  | zinc finger MYM-type containing 2 |
| GEN-1247 | ZMYM3 | S | 2 |  |  | zinc finger MYM-type containing 3 |
| GEN-1248 | ZMYND11 | 2 | 4 |  |  | Zinc finger, MYND-type containing 11 |
| GEN-1249 | ZMYND8 | S | 2 |  |  | zinc finger MYND-type containing 8 |
| GEN-1250 | ZNF18 | 2 | 1 |  |  | zinc finger protein 18 |
| GEN-1251 | ZNF292 | S | 4 | 0.2612 |  | zinc finger protein 292 |
| GEN-1252 | VDR | 2 | 3 |  |  | vitamin D receptor |
| GEN-1253 | ZNF385B | 2 | 1 |  |  | Zinc finger protein 385B |
| GEN-1254 | ZNF462 | S | 5 |  |  | Zinc finger protein 462 |
| GEN-1255 | ZNF517 | 2 | 2 |  |  | Zinc finger protein 517 |
| GEN-1256 | ZNF532 | 3 | 1 |  |  | zinc finger protein 532 |
| GEN-1257 | ZNF536 | 3 | 3 |  |  | zinc finger protein 536 |
| GEN-1258 | ZNF548 | 2 | 1 |  |  | zinc finger protein 548 |
| GEN-1259 | ZNF559 | 2 | 3 |  |  | Zinc finger protein 559 |
| GEN-1260 | ZNF626 | 2 | 1 |  |  | zinc finger protein 626 |
| GEN-1261 | ZNF644 | 3 | 1 |  |  | zinc finger protein 644 |
| GEN-1262 | ZNF711 | 2 | 2 |  |  | zinc finger protein 711 |
| GEN-1263 | ZNF713 | 2 | 1 |  |  | Zinc finger protein 713 |
| GEN-1264 | ZNF774 | 2 | 1 |  |  | Zinc finger protein 774 |
| GEN-1265 | ZNF804A | 2 | 4 | 0.3146 |  | Zinc finger protein 804A |
| GEN-1266 | ZNF827 | 2 | 1 |  |  | Zinc finger protein 827 |
| GEN-1267 | ZNF865 | 1 | 2 |  |  | zinc finger protein 865 |
| GEN-1268 | ZSWIM6 | S | 2 | 0.3503 |  | zinc finger SWIM-type containing 6 |
| GEN-1269 | ZWILCH | 2 | 2 |  |  | zwilchkinetochore protein |
| GEN-1270 | TRPV4 |  | 4 | 0.7259 |  |  |
| GEN-1271 | HOXD13 |  | 1 | 0.1003 |  |  |
| GEN-1272 | EVX2 |  | 1 | 0.094 |  |  |
| GEN-1273 | HOXA13 |  | 1 | 0.0904 |  |  |
| GEN-1274 | GDF5 |  | 1 | 0.0883 |  |  |
| GEN-1275 | HOXD12 |  | 1 | 0.0858 |  |  |
| GEN-1276 | LRP4 |  | 1 | 0.0847 |  |  |
| GEN-1277 | SHH |  | 1 | 0.2619 |  |  |
| GEN-1278 | TBX4 |  | 1 | 0.078 |  |  |
| GEN-1279 | BMPR1B |  | 1 | 0.073 |  |  |
| GEN-1280 | LMBR1 |  | 1 | 0.0712 |  |  |
| GEN-1281 | IHH |  | 1 | 0.0711 |  |  |
| GEN-1282 | TP63 |  | 1 | 0.0654 |  |  |
| GEN-1283 | PORCN |  | 1 | 0.0647 |  |  |
| GEN-1284 | FBN2 |  | 1 | 0.0647 |  |  |
| GEN-1285 | LRP5L |  | 1 | 0.0639 |  |  |
| GEN-1286 | LRP5 |  | 1 | 0.0639 |  |  |
| GEN-1287 | FURIN |  | 1 | 0.2597 |  |  |
| GEN-1288 | SFRP2 |  | 1 | 0.0632 |  |  |
| GEN-1289 | FMN1 |  | 1 | 0.063 |  |  |
| GEN-1290 | SALL4 |  | 1 | 0.0596 |  |  |
| GEN-1291 | ROR2 |  | 1 | 0.0539 |  |  |
| GEN-1292 | EPYC |  | 1 | 0.0535 |  |  |
| GEN-1293 | MECOM |  | 1 | 0.0476 |  |  |
| GEN-1294 | SPRY4 |  | 1 | 0.0473 |  |  |
| GEN-1295 | HOXD11 |  | 1 | 0.0453 |  |  |
| GEN-1296 | ADAMTS17 |  | 1 | 0.0418 |  |  |
| GEN-1297 | MIR92A1 |  | 1 | 0.0418 |  |  |
| GEN-1298 | RSPO2 |  | 1 | 0.0404 |  |  |
| GEN-1299 | DNASE1L2 |  | 1 | 0.0404 |  |  |
| GEN-1300 | CANT1 |  | 1 | 0.0404 |  |  |
| GEN-1301 | GAS1 |  | 1 | 0.0404 |  |  |
| GEN-1302 | GKN2 |  | 1 | 0.0402 |  |  |
| GEN-1303 | MATN3 |  | 1 | 0.036 |  |  |
| GEN-1304 | COMP |  | 1 | 0.0357 |  |  |
| GEN-1305 | COL11A1 |  | 2 | 0.3298 |  |  |
| GEN-1306 | BGN |  | 1 | 0.032 |  |  |
| GEN-1307 | HTR1A |  | 3 | 0.6267 |  |  |
| GEN-1308 | HTR2A |  | 3 | 0.6257 |  |  |
| GEN-1309 | POLG |  | 3 | 0.565 |  |  |
| GEN-1310 | WFS1 |  | 3 | 0.5264 |  |  |
| GEN-1311 | POLGARF |  | 2 | 0.472 |  |  |
| GEN-1312 | TRANK1 |  | 2 | 0.4649 |  |  |
| GEN-1313 | KAT8 |  | 2 | 0.4625 |  |  |
| GEN-1314 | PIDD1 |  | 2 | 0.4624 |  |  |
| GEN-1315 | IGSF9B |  | 2 | 0.4543 |  |  |
| GEN-1316 | MTNR1A |  | 2 | 0.4509 |  |  |
| GEN-1317 | MTNR1B |  | 2 | 0.4509 |  |  |
| GEN-1318 | FES |  | 2 | 0.4486 |  |  |
| GEN-1319 | SLC39A8 |  | 2 | 0.445 |  |  |
| GEN-1320 | SOX7 |  | 2 | 0.4436 |  |  |
| GEN-1321 | RGS6 |  | 2 | 0.4214 |  |  |
| GEN-1322 | GJB2 |  | 2 | 0.4163 |  |  |
| GEN-1323 | PPP1R16B |  | 2 | 0.4051 |  |  |
| GEN-1324 | SHISA9 |  | 2 | 0.3951 |  |  |
| GEN-1325 | SRPK2 |  | 2 | 0.3946 |  |  |
| GEN-1326 | GRM3 |  | 2 | 0.3893 |  |  |
| GEN-1327 | ESAM |  | 2 | 0.384 |  |  |
| GEN-1328 | TSNARE1 |  | 2 | 0.3811 |  |  |
| GEN-1329 | NONO |  | 2 | 0.3705 |  |  |
| GEN-1330 | RNASEH2B |  | 2 | 0.3701 |  |  |
| GEN-1331 | FBXW11 |  | 2 | 0.3696 |  |  |
| GEN-1332 | SMARCD1 |  | 2 | 0.3696 |  |  |
| GEN-1333 | SCTR |  | 2 | 0.3692 |  |  |
| GEN-1334 | CHRNA3 |  | 2 | 0.3666 |  |  |
| GEN-1335 | SNX19 |  | 2 | 0.3526 |  |  |
| GEN-1336 | SDK1 |  | 2 | 0.3492 |  |  |
| GEN-1337 | ANAPC4 |  | 2 | 0.347 |  |  |
| GEN-1338 | SREK1IP1 |  | 2 | 0.3443 |  |  |
| GEN-1339 | ITIH3 |  | 2 | 0.3438 |  |  |
| GEN-1340 | TOP1 |  | 2 | 0.3416 |  |  |
| GEN-1341 | FASN |  | 2 | 0.3412 |  |  |
| GEN-1342 | MAP2K1 |  | 2 | 0.3409 |  |  |
| GEN-1343 | HK1 |  | 2 | 0.3408 |  |  |
| GEN-1344 | ATP6V0A1 |  | 2 | 0.34 |  |  |
| GEN-1345 | TTLL7 |  | 2 | 0.339 |  |  |
| GEN-1346 | RPE65 |  | 2 | 0.3378 |  |  |
| GEN-1347 | POU3F2 |  | 2 | 0.3373 |  |  |
| GEN-1348 | LMAN2L |  | 2 | 0.3366 |  |  |
| GEN-1349 | FANCI |  | 2 | 0.3361 |  |  |
| GEN-1350 | NALCN |  | 2 | 0.3359 |  |  |
| GEN-1351 | MOCOS |  | 2 | 0.3348 |  |  |
| GEN-1352 | GSPT2 |  | 2 | 0.3345 |  |  |
| GEN-1353 | SLC9A3 |  | 2 | 0.3337 |  |  |
| GEN-1354 | KCNK9 |  | 2 | 0.3335 |  |  |
| GEN-1355 | MYT1 |  | 2 | 0.333 |  |  |
| GEN-1356 | ACACB |  | 2 | 0.333 |  |  |
| GEN-1357 | SPG11 |  | 2 | 0.333 |  |  |
| GEN-1358 | MCM3AP |  | 2 | 0.3326 |  |  |
| GEN-1359 | SLC3A1 |  | 2 | 0.3326 |  |  |
| GEN-1360 | RRP8 |  | 2 | 0.3326 |  |  |
| GEN-1361 | STARD9 |  | 2 | 0.3326 |  |  |
| GEN-1362 | TECPR2 |  | 2 | 0.3326 |  |  |
| GEN-1363 | CLSTN3 |  | 2 | 0.3326 |  |  |
| GEN-1364 | MCCC2 |  | 2 | 0.3326 |  |  |
| GEN-1365 | LARP4B |  | 2 | 0.3326 |  |  |
| GEN-1366 | SMG9 |  | 2 | 0.3326 |  |  |
| GEN-1367 | PAFAH1B3 |  | 2 | 0.3326 |  |  |
| GEN-1368 | TUB |  | 2 | 0.3326 |  |  |
| GEN-1369 | CHRNA1 |  | 2 | 0.3326 |  |  |
| GEN-1370 | SRD5A3 |  | 2 | 0.3326 |  |  |
| GEN-1371 | LINS1 |  | 2 | 0.3326 |  |  |
| GEN-1372 | ACADVL |  | 2 | 0.3326 |  |  |
| GEN-1373 | SLC22A23 |  | 2 | 0.3282 |  |  |
| GEN-1374 | ZGRF1 |  | 2 | 0.3234 |  |  |
| GEN-1375 | THOC7 |  | 2 | 0.3231 |  |  |
| GEN-1376 | CLSTN2 |  | 2 | 0.3191 |  |  |
| GEN-1377 | MAD1L1 |  | 2 | 0.3183 |  |  |
| GEN-1378 | DUSP6 |  | 2 | 0.3179 |  |  |
| GEN-1379 | NOVA1 |  | 2 | 0.3129 |  |  |
| GEN-1380 | TFAP2B |  | 2 | 0.3123 |  |  |
| GEN-1381 | COA8 |  | 2 | 0.3118 |  |  |
| GEN-1382 | XRN2 |  | 2 | 0.3097 |  |  |
| GEN-1383 | AP3B2 |  | 2 | 0.3096 |  |  |
| GEN-1384 | CALN1 |  | 2 | 0.3095 |  |  |
| GEN-1385 | KCNG2 |  | 2 | 0.3094 |  |  |
| GEN-1386 | UTY |  | 2 | 0.3082 |  |  |
| GEN-1387 | ARHGAP15 |  | 2 | 0.3073 |  |  |
| GEN-1388 | SLC12A1 |  | 2 | 0.3068 |  |  |
| GEN-1389 | NKX2-1 |  | 2 | 0.3068 |  |  |
| GEN-1390 | GRIN3B |  | 2 | 0.3067 |  |  |
| GEN-1391 | GABBR1 |  | 2 | 0.3045 |  |  |
| GEN-1392 | TNRC6A |  | 2 | 0.3044 |  |  |
| GEN-1393 | ERCC4 |  | 2 | 0.3023 |  |  |
| GEN-1394 | MRPS33 |  | 2 | 0.3021 |  |  |
| GEN-1395 | EIF1AY |  | 2 | 0.3016 |  |  |
| GEN-1396 | PTPRF |  | 2 | 0.3012 |  |  |
| GEN-1397 | ST3GAL3 |  | 2 | 0.3009 |  |  |
| GEN-1398 | OLFM4 |  | 2 | 0.3009 |  |  |
| GEN-1399 | KCNQ5 |  | 1 | 0.3 |  |  |
| GEN-1400 | GATB |  | 1 | 0.2988 |  |  |
| GEN-1401 | SEMA6D |  | 1 | 0.2987 |  |  |
| GEN-1402 | TYW5 |  | 1 | 0.2984 |  |  |
| GEN-1403 | CNNM4 |  | 1 | 0.2984 |  |  |
| GEN-1404 | TMEM170B |  | 1 | 0.2983 |  |  |
| GEN-1405 | GRIN2D |  | 1 | 0.297 |  |  |
| GEN-1406 | ZMIZ2 |  | 1 | 0.296 |  |  |
| GEN-1407 | GRIN3A |  | 1 | 0.2959 |  |  |
| GEN-1408 | GRAMD1B |  | 1 | 0.2958 |  |  |
| GEN-1409 | CEP104 |  | 1 | 0.2957 |  |  |
| GEN-1410 | GRIN2C |  | 1 | 0.2954 |  |  |
| GEN-1411 | TANK |  | 1 | 0.2954 |  |  |
| GEN-1412 | CALU |  | 1 | 0.295 |  |  |
| GEN-1413 | MAIP1 |  | 1 | 0.2944 |  |  |
| GEN-1414 | CLCN3 |  | 1 | 0.2935 |  |  |
| GEN-1415 | MED27 |  | 1 | 0.2917 |  |  |
| GEN-1416 | SNAP91 |  | 1 | 0.2909 |  |  |
| GEN-1417 | NRGN |  | 1 | 0.2904 |  |  |
| GEN-1418 | GPR26 |  | 1 | 0.2878 |  |  |
| GEN-1419 | SNX29 |  | 1 | 0.2877 |  |  |
| GEN-1420 | PPP2R2D |  | 1 | 0.2846 |  |  |
| GEN-1421 | PLEKHG7 |  | 1 | 0.2845 |  |  |
| GEN-1422 | PELI1 |  | 1 | 0.2838 |  |  |
| GEN-1423 | ENOX1 |  | 1 | 0.283 |  |  |
| GEN-1424 | GSK3B |  | 1 | 0.282 |  |  |
| GEN-1425 | ARPP21 |  | 1 | 0.2819 |  |  |
| GEN-1426 | PAM |  | 1 | 0.2806 |  |  |
| GEN-1427 | ADRA2B |  | 1 | 0.2806 |  |  |
| GEN-1428 | ADRA2A |  | 1 | 0.2781 |  |  |
| GEN-1429 | KCNJ6 |  | 1 | 0.2776 |  |  |
| GEN-1430 | ADRA2C |  | 1 | 0.2776 |  |  |
| GEN-1431 | NMUR2 |  | 1 | 0.2768 |  |  |
| GEN-1432 | IMPA1 |  | 1 | 0.2767 |  |  |
| GEN-1433 | RPL17 |  | 1 | 0.2752 |  |  |
| GEN-1434 | ZNF608 |  | 1 | 0.2745 |  |  |
| GEN-1435 | TMEM161B |  | 1 | 0.2742 |  |  |
| GEN-1436 | MYO18A |  | 1 | 0.2731 |  |  |
| GEN-1437 | WDR45 |  | 1 | 0.2723 |  |  |
| GEN-1438 | AS3MT |  | 1 | 0.2718 |  |  |
| GEN-1439 | MOCS2 |  | 1 | 0.2706 |  |  |
| GEN-1440 | CAMK2G |  | 1 | 0.2689 |  |  |
| GEN-1441 | SLC6A2 |  | 1 | 0.2687 |  |  |
| GEN-1442 | SMARCB1 |  | 1 | 0.2684 |  |  |
| GEN-1443 | GSDME |  | 1 | 0.2677 |  |  |
| GEN-1444 | ASXL2 |  | 1 | 0.2665 |  |  |
| GEN-1445 | AEBP1 |  | 1 | 0.2661 |  |  |
| GEN-1446 | PQBP1 |  | 1 | 0.2661 |  |  |
| GEN-1447 | RPL36 |  | 1 | 0.2661 |  |  |
| GEN-1448 | EED |  | 1 | 0.2661 |  |  |
| GEN-1449 | MICOS13 |  | 1 | 0.2661 |  |  |
| GEN-1450 | SLC30A9 |  | 1 | 0.2638 |  |  |
| GEN-1451 | BAG5 |  | 1 | 0.2638 |  |  |
| GEN-1452 | NMB |  | 1 | 0.2615 |  |  |
| GEN-1453 | ASXL1 |  | 1 | 0.2611 |  |  |
| GEN-1454 | ARIH2 |  | 1 | 0.2608 |  |  |
| GEN-1455 | FOXN1 |  | 1 | 0.2606 |  |  |
| GEN-1456 | NGEF |  | 1 | 0.2603 |  |  |
| GEN-1457 | GNB1 |  | 1 | 0.2598 |  |  |
| GEN-1458 | ASPA |  | 1 | 0.2596 |  |  |
| GEN-1459 | CUBN |  | 1 | 0.2594 |  |  |
| GEN-1460 | GSK3A |  | 1 | 0.2592 |  |  |
| GEN-1461 | SRD5A2 |  | 1 | 0.2591 |  |  |
| GEN-1462 | TACR3 |  | 1 | 0.2587 |  |  |
| GEN-1463 | SPATA22 |  | 1 | 0.2587 |  |  |
| GEN-1464 | DCLK3 |  | 1 | 0.2575 |  |  |
| GEN-1465 | PSMG1 |  | 1 | 0.2574 |  |  |
| GEN-1466 | SPAG16 |  | 1 | 0.254 |  |  |
| GEN-1467 | EFL1 |  | 1 | 0.2529 |  |  |
| GEN-1468 | ASTN1 |  | 1 | 0.2522 |  |  |
| GEN-1469 | VRK2 |  | 1 | 0.2522 |  |  |
| GEN-1470 | MRTFA |  | 1 | 0.2506 |  |  |
| GEN-1471 | LMOD1 |  | 1 | 0.2499 |  |  |
| GEN-1472 | AVPR2 |  | 1 | 0.2392 |  |  |
| GEN-1473 | TFAP2D |  | 1 | 0.2389 |  |  |
| GEN-1474 | NAA11 |  | 1 | 0.2363 |  |  |
| GEN-1475 | GALNT3 |  | 1 | 0.2361 |  |  |
| GEN-1476 | PODXL |  | 1 | 0.236 |  |  |
| GEN-1477 | SCMH1 |  | 1 | 0.2345 |  |  |
| GEN-1478 | IGDCC4 |  | 1 | 0.2337 |  |  |
| GEN-1479 | BRINP2 |  | 1 | 0.2336 |  |  |
| GEN-1480 | SPPL2C |  | 1 | 0.2335 |  |  |
| GEN-1481 | CNNM2 |  | 1 | 0.2264 |  |  |
| GEN-1482 | ITIH1 |  | 1 | 0.225 |  |  |
| GEN-1483 | ARFGEF2 |  | 1 | 0.2246 |  |  |
| GEN-1484 | FSIP2 |  | 1 | 0.2236 |  |  |
| GEN-1485 | FOXO3 |  | 1 | 0.2225 |  |  |
| GEN-1486 | ZNF638 |  | 1 | 0.2225 |  |  |
| GEN-1487 | PLCL2 |  | 1 | 0.2202 |  |  |
| GEN-1488 | SIGMAR1 |  | 1 | 0.2167 |  |  |
| GEN-1489 | TENM2 |  | 1 | 0.2102 |  |  |
| GEN-1490 | DRD4 |  | 1 | 0.2082 |  |  |
| GEN-1491 | PALS2 |  | 1 | 0.208 |  |  |
| GEN-1492 | CSF3R |  | 1 | 0.2074 |  |  |
| GEN-1493 | FGGY |  | 1 | 0.2071 |  |  |
| GEN-1494 | CWC22 |  | 1 | 0.2062 |  |  |
| GEN-1495 | AKAP6 |  | 1 | 0.2058 |  |  |
| GEN-1496 | ARL6IP4 |  | 1 | 0.2055 |  |  |
| GEN-1497 | RBL2 |  | 1 | 0.2048 |  |  |
| GEN-1498 | EXOC4 |  | 1 | 0.2041 |  |  |
| GEN-1499 | LUZP2 |  | 1 | 0.2036 |  |  |
| GEN-1500 | CA10 |  | 1 | 0.2022 |  |  |
| GEN-1501 | RWDD3 |  | 1 | 0.2021 |  |  |
| GEN-1502 | PLCL1 |  | 1 | 0.2 |  |  |
| GEN-1503 | HNRNPA1L3 |  | 1 | 0.1999 |  |  |
| GEN-1504 | CXADR |  | 1 | 0.1999 |  |  |
| GEN-1505 | MPHOSPH9 |  | 1 | 0.1998 |  |  |
| GEN-1506 | LSM5 |  | 1 | 0.1997 |  |  |
| GEN-1507 | CCDC68 |  | 1 | 0.198 |  |  |
| GEN-1508 | CHRM1 |  | 1 | 0.1978 |  |  |
| GEN-1509 | SOX14 |  | 1 | 0.1956 |  |  |
| GEN-1510 | DEPDC1 |  | 1 | 0.1953 |  |  |
| GEN-1511 | RCOR2 |  | 1 | 0.1942 |  |  |
| GEN-1512 | NREP |  | 1 | 0.1931 |  |  |
| GEN-1513 | PCDH17 |  | 1 | 0.1925 |  |  |
| GEN-1514 | SNRPN |  | 1 | 0.1924 |  |  |
| GEN-1515 | SGCZ |  | 1 | 0.192 |  |  |
| GEN-1516 | NAA80 |  | 1 | 0.1911 |  |  |
| GEN-1517 | FTCDNL1 |  | 1 | 0.1898 |  |  |
| GEN-1518 | ALPK3 |  | 1 | 0.1869 |  |  |
| GEN-1519 | RB1 |  | 1 | 0.1852 |  |  |
| GEN-1520 | KCNV1 |  | 1 | 0.184 |  |  |
| GEN-1521 | CSE1L |  | 1 | 0.1811 |  |  |
| GEN-1522 | ERLIN1 |  | 1 | 0.1809 |  |  |
| GEN-1523 | PMFBP1 |  | 1 | 0.1808 |  |  |
| GEN-1524 | FADS1 |  | 1 | 0.18 |  |  |
| GEN-1525 | IER5L |  | 1 | 0.1797 |  |  |
| GEN-1526 | SNURF |  | 1 | 0.1788 |  |  |
| GEN-1527 | LPAR2 |  | 1 | 0.1783 |  |  |
| GEN-1528 | RBKS |  | 1 | 0.1765 |  |  |
| GEN-1529 | PPM1E |  | 1 | 0.1762 |  |  |
| GEN-1530 | NR1D2 |  | 1 | 0.1761 |  |  |
| GEN-1531 | TNIP2 |  | 1 | 0.1737 |  |  |
| GEN-1532 | CYSTM1 |  | 1 | 0.1723 |  |  |
| GEN-1533 | PPIP5K2 |  | 1 | 0.1721 |  |  |
| GEN-1534 | NT5DC2 |  | 1 | 0.1714 |  |  |
| GEN-1535 | GMIP |  | 1 | 0.1712 |  |  |
| GEN-1536 | DOC2A |  | 1 | 0.169 |  |  |
| GEN-1537 | PBX4 |  | 1 | 0.1688 |  |  |
| GEN-1538 | EPHA3 |  | 1 | 0.1658 |  |  |
| GEN-1539 | CWF19L1 |  | 1 | 0.1647 |  |  |
| GEN-1540 | DBN1 |  | 1 | 0.1643 |  |  |
| GEN-1541 | SHOX2 |  | 1 | 0.1632 |  |  |
| GEN-1542 | AKTIP |  | 1 | 0.1613 |  |  |
| GEN-1543 | WNT4 |  | 1 | 0.1594 |  |  |
| GEN-1544 | PEF1 |  | 1 | 0.1576 |  |  |
| GEN-1545 | ARL5B |  | 1 | 0.1571 |  |  |
| GEN-1546 | MDK |  | 1 | 0.1565 |  |  |
| GEN-1547 | BEND4 |  | 1 | 0.1562 |  |  |
| GEN-1548 | DDN |  | 1 | 0.1553 |  |  |
| GEN-1549 | DCAF16 |  | 1 | 0.1552 |  |  |
| GEN-1550 | FAM53C |  | 1 | 0.1544 |  |  |
| GEN-1551 | C2orf69 |  | 1 | 0.1527 |  |  |
| GEN-1552 | PLXNA2 |  | 1 | 0.1498 |  |  |
| GEN-1553 | LRGUK |  | 1 | 0.1495 |  |  |
| GEN-1554 | IKBIP |  | 1 | 0.1488 |  |  |
| GEN-1555 | SPTBN5 |  | 1 | 0.1484 |  |  |
| GEN-1556 | ATOH1 |  | 1 | 0.1483 |  |  |
| GEN-1557 | MRPL33 |  | 1 | 0.1481 |  |  |
| GEN-1558 | MROH5 |  | 1 | 0.1476 |  |  |
| GEN-1559 | MGAT3 |  | 1 | 0.1472 |  |  |
| GEN-1560 | NUF2 |  | 1 | 0.147 |  |  |
| GEN-1561 | CHRM4 |  | 1 | 0.1465 |  |  |
| GEN-1562 | CYP2D7 |  | 1 | 0.1455 |  |  |
| GEN-1563 | DAOA |  | 1 | 0.144 |  |  |
| GEN-1564 | ATXN7 |  | 1 | 0.1436 |  |  |
