---
id: TOPIC-Transcriptomics-Autism
type: topic_deep_dive
purpose: RNA-level analysis in autism — bulk + single-cell + iPSC-derived neurons; the cell-type-resolution revolution
key_atlas_links:
  - HYP-0028 (Inherited polygenic risk)
  - HYP-0008 (Maternal immune activation)
  - MEC-0020 (Calcium glutamate-NMDA homeostasis)
related_topic_pages:
  - Multi_Omics_Integration_for_Autism
  - Genomics_of_Autism
  - Epigenetics_of_Autism
status: live
---

# Transcriptomics in Autism — The Active Expression Layer

Transcriptomics measures the **set of RNA transcripts actually being produced** in a cell, tissue, or biofluid. It tells you not just which genes a child carries (genomics) but **which genes are actually being expressed and at what level**, in which cell types, at which developmental times. For autism — where genetic susceptibility is widespread but only a fraction of carriers develop the phenotype — transcriptomics is one of the most informative layers for understanding *which* susceptibility actually expresses as disease.

## Why transcriptomics matters for autism

Genomics tells you the substrate; transcriptomics tells you what's actually happening. This matters for autism because:

1. **Most autism risk genes are pleiotropic** — they affect many systems and many cell types. Knowing a child has a SHANK3 variant tells you risk; knowing how SHANK3 RNA is being expressed in their excitatory neurons vs interneurons tells you what's actually going wrong.

2. **Developmental timing matters intensely**. A gene that's normally expressed only in fetal brain may be silent by the time you can biopsy. Transcriptomic atlases of fetal vs adult brain (Allen Brain Atlas, BrainSpan, PsychENCODE) are critical for placing autism genetics in developmental context.

3. **Cell-type heterogeneity is the rule**. Bulk-tissue RNA-seq averages across all cell types in a sample. Excitatory neurons, inhibitory interneurons, microglia, astrocytes, and oligodendrocytes have very different transcriptomic profiles, and autism affects them differently. Single-cell RNA-seq is the technology that resolved this.

4. **iPSC-derived neurons enable controlled experiments**. Take fibroblasts from an autistic patient, reprogram to induced pluripotent stem cells, differentiate to neurons, and you have the patient's own neurons in a dish — controllable, transcriptome-readable, perturbable.

## What transcriptomics has shown about autism

### Bulk brain RNA-seq

Multiple studies of postmortem autistic brain (Voineagu et al., Gandal et al., others) consistently identify three convergent gene-expression modules:

1. **Synaptic / neuronal module — DOWNREGULATED.** Genes encoding synaptic proteins (PSD-95, Homer, SHANK family, glutamate receptors, GABA receptors), excitatory neuron markers, and synaptic plasticity machinery show systematic reduced expression in autistic cortex.

2. **Immune / microglial module — UPREGULATED.** Microglia-specific genes, complement system, MHC class I/II, cytokine signaling, and microglial activation markers are systematically elevated. This is direct transcriptomic evidence of the neuroinflammation framework underlying [[Theoharides_Theoharis]]'s mast cell/microglial coupling and the [[Naviaux_Robert]] cell danger response model.

3. **Chromatin remodeling module — DYSREGULATED.** CHD8 and the broader chromatin-modifier gene set show altered expression patterns, particularly in early developmental windows.

Cross-disorder comparisons (Gandal et al. 2018) show these patterns overlap substantially with schizophrenia and bipolar disorder, less with depression — consistent with shared genetic architecture and overlapping cellular biology across major neurodevelopmental and psychiatric conditions.

### Single-cell RNA-seq — the cell-type revolution

Bulk transcriptomic patterns can be misleading: they could reflect either changes within cells or changes in cellular composition. Single-cell RNA-seq (scRNA-seq) resolves this directly. Velmeshev et al. 2019 (*Science*), Wang et al. 2018, and subsequent studies established:

- **Upper-layer excitatory neurons** in autistic cortex show the most pronounced gene-expression changes, with downregulation of synaptic genes specifically in this cell type.
- **Microglia** show distinct activation signatures.
- **Inhibitory interneuron** changes are subtler but cell-type-specific.
- **Disease-relevant gene expression changes correlate with clinical severity** at the single-cell level.

This is the fourth-camp position from the methodological literature: cell-type resolution can resolve disputes that bulk integration cannot. Bulk-tissue differences can be driven by cellular composition shifts that masquerade as multi-omic "pathways" — single-cell separates the signals.

### iPSC-derived neurons

Patient-derived induced pluripotent stem cells, differentiated to neurons (cortical, GABAergic, dopaminergic, etc.), let you study the patient's own neuronal biology in a dish. Findings:

- **Synaptic gene expression deficits replicate** in vitro from the patient's own cells.
- **Excitation-inhibition balance abnormalities** are detectable transcriptomically and electrophysiologically.
- **Drug screening** is feasible — test specific compounds on patient-derived neurons before clinical use.
- **CRISPR correction** of patient mutations rescues some transcriptomic and functional defects, providing direct causal evidence.

The Pasca lab (Stanford) has been particularly influential here, advancing brain "assembloids" — iPSC-derived 3D models combining cortical, subcortical, and other regions — for transcriptomic + circuit-level autism modeling.

### Blood transcriptomics — the accessible biomarker

Brain tissue is inaccessible in living patients. Blood is. Multiple studies have shown that blood transcriptomic profiles in autism partially mirror brain expression patterns — particularly for immune and metabolic modules — providing a peripheral biomarker pathway. This is much weaker than direct brain analysis but clinically practical.

### Single-cell + spatial — the frontier

The current frontier combines:
- **Spatial transcriptomics** — measuring gene expression with preserved spatial location in tissue (10x Visium, MERFISH, others).
- **Single-cell + spatial integration** — knowing both the cell type and where it sits in the brain.
- **Developmental trajectories** — measuring transcriptomic changes across fetal, infant, child, adult timepoints.

For autism, this is producing the first cell-type + region-specific maps of which neurodevelopmental processes go wrong, when, and where. Multiple major consortia (PsychENCODE Phase II, BrainCV, others) are generating these atlases.

## What transcriptomics tells you clinically (right now)

In 2026, clinical transcriptomic testing for autism is **not yet standard**. Research-grade and clinically-available options include:

- **Blood RNA-seq panels** — emerging from research labs, available to specialty clinicians on a research-collaborative basis. Useful for identifying broad immune/inflammatory transcriptomic signatures.
- **Neurotypical-vs-autistic differential expression panels** — some commercial labs offer these, though clinical actionability varies.
- **iPSC-derived neuron screening** — research-only; available through specialized programs (Stanford Pasca lab, Salk, others) for severely affected individuals where intervention candidates are being explored.
- **Pharmacogenomic transcriptomics** — emerging combined panels that integrate genotype + expression for medication-response prediction.

Most clinically-relevant findings from autism transcriptomics in 2026 still arrive through their downstream consequences: through metabolomics ([[Metabolomics_in_Autism]]), through proteomics ([[Proteomics_in_Autism]]), and through clinical biomarker panels that capture the functional outputs of dysregulated transcription rather than transcription itself.

## Atlas connections

- **[[HYP-0028 Inherited polygenic risk]]** — transcriptomics shows how polygenic substrate plays out in expressed biology
- **[[HYP-0008 Maternal immune activation]]** — microglial activation transcriptomic signature is central evidence
- **[[HYP-0073 Developmental timing state-transition disorder]]** — developmental transcriptomic atlases define the windows
- **[[MEC-0020 Calcium glutamate-NMDA homeostasis]]** — synaptic gene downregulation is direct evidence
- **[[Geschwind_Daniel]]** — UCLA brain transcriptomics + brain-bank work is foundational
- **[[Naviaux_Robert]]** — CDR transcriptomic signatures are an emerging research area
- **[[Multi_Omics_Causal_Pathways_in_Autism]]** — multiple cited studies use transcriptomics as an integration layer

## Read further

- **PsychENCODE** — [psychencode.org](https://www.psychencode.org/) — major brain transcriptomic resource for psychiatric/neurodevelopmental disorders
- **Allen Brain Atlas** — [brain-map.org](https://www.brain-map.org/) — developmental + cell-type transcriptomic atlases
- **BrainSpan** — fetal-through-adult human brain transcriptomic atlas
- **Velmeshev et al. 2019 Science** — landmark single-cell ASD cortex study
- **Gandal et al. 2018 Science** — cross-disorder transcriptomic landscape

The transcriptomic layer is rapidly evolving. The tools (single-cell, spatial, iPSC) are now mature enough to resolve questions that bulk methods can't. Expect this layer to become increasingly clinically actionable over the next 5–10 years — particularly through pharmacogenomics + transcriptomics combined panels, and through iPSC-based personalized drug screening for severely affected individuals.
