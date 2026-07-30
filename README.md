# On the Role of Source Density in Hydra Patterning and Regeneration Models

This repository contains a work-in-progress mathematical study of pattern
formation, regeneration, and positional memory in *Hydra*.

The manuscript revisits Gierer--Meinhardt-type activator--inhibitor systems and
asks which qualitative mechanisms are already present in the classical
two-equation model and which require an additional source-density field.

## Current mathematical focus

The model audit distinguishes three two-equation regimes:

- without production terms, the system has a unique positive homogeneous
  steady state and no resting state.
- basal inhibitor production introduces a stable zero state and can produce
  two additional positive steady states.
- activator and inhibitor production leads to a cubic steady-state equation
  and a transition between one and three nonnegative homogeneous states.

For these regimes, the manuscript develops explicit existence conditions,
linear stability criteria, and possible diffusion-driven instability. In the
three-state activator-production regime, the middle state is unstable and the
two outer states satisfy an ordering relation that constrains their possible
stability configurations.

The later sections examine whether source density is needed for regeneration,
how it may encode positional memory, and how a separate hysteretic
head-identity variable could distinguish transient activator peaks from stable
morphological commitment.

## Main questions

- Which regeneration mechanisms already occur in a two-variable
  activator--inhibitor system?
- When does inhibitor production create a stable resting state and permit
  bistability?
- How does activator production change the number and stability of homogeneous
  steady states?
- What positional information is missing from the two-equation model?
- Can source density encode positional memory without determining pattern
  formation itself?

## Repository structure

```text
.
|-- main.tex
|-- packages.tex
|-- sections/
|   |-- 00_abstract.tex
|   |-- 01_introduction.tex
|   |-- 02_gm_model_audit.tex
|   |-- 03_regeneration_and_pattern_formation.tex
|   |-- 04_source_density_and_positional_memory.tex
|   |-- 05_head_identity_extension.tex
|   `-- 06_discussion.tex
|-- bib/
|   `-- references.bib
`-- figures/
```

The current compiled manuscript is available as [`main.pdf`](main.pdf).

## Building the manuscript

A standard LaTeX installation with `latexmk` is sufficient:

```bash
latexmk -pdf -synctex=1 main.tex
```

To remove auxiliary build files:

```bash
latexmk -c
```

Each file in `sections/` declares `main.tex` as its root document, which allows
editors such as VS Code with LaTeX Workshop to compile and synchronize the
manuscript correctly while a section file is open.

## Project status

The two-equation model audit now contains numbered propositions, proofs, and
remarks for the principal production regimes. The sections on regeneration,
source-density dynamics, positional memory, head identity, numerical
experiments, figures, and references remain under active development.
