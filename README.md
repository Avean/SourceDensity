# On the Role of Source Density in Hydra Patterning and Regeneration Models

This repository contains a work-in-progress mathematical study of pattern
formation, regeneration, and positional memory in *Hydra*.

The manuscript revisits Gierer--Meinhardt-type activator--inhibitor models and
asks which biological phenomena follow from the classical pattern-forming
mechanism itself, and which require an additional source-density field.

## Overview

Activator--inhibitor models can generate localized peaks and reproduce a basic
threshold response to a wound-like perturbation. This already provides a
minimal mathematical description of head regeneration.

Source density plays a different role. Rather than being necessary for pattern
formation itself, it can encode positional information retained by tissue and
help describe grafting and polarization experiments. The manuscript also
examines the limitations of dynamic source density and proposes a separate,
hysteretic head-identity variable as a mechanism for stable morphological
commitment.

The central questions are:

- Is source density necessary for regeneration or classical pattern formation?
- What positional information is missing from a two-variable
  activator--inhibitor model?
- Can a dynamic source-density field anchor a head at an arbitrary position?
- How can transient activator peaks be distinguished from established head
  identity?

## Conceptual structure

The models distinguish between four roles:

- \(u\): a fast, local head-activating signal;
- \(v\): a longer-range inhibitor;
- \(\rho\): a slowly evolving positional or source-density field;
- \(h\): a local head-identity variable with hysteresis.

This separation makes it possible to study pattern generation, positional
memory, and morphological commitment as related but distinct mechanisms.

## Repository structure

```text
.
├── main.tex
├── packages.tex
├── sections/
│   ├── 00_abstract.tex
│   ├── 01_introduction.tex
│   ├── 02_gm_model_audit.tex
│   ├── 03_regeneration_and_pattern_formation.tex
│   ├── 04_source_density_and_positional_memory.tex
│   ├── 05_head_identity_extension.tex
│   └── 06_discussion.tex
├── bib/
│   └── references.bib
└── figures/
```

The current compiled manuscript is available as [`main.pdf`](main.pdf).

## Building the manuscript

A standard LaTeX installation with `latexmk` is sufficient:

```bash
latexmk -pdf main.tex
```

To remove auxiliary build files:

```bash
latexmk -c
```

## Project status

The manuscript is under active development. The model audit and the core
regeneration argument are in place, while the sections on positional memory,
head identity, numerical experiments, figures, and biological references are
being expanded.

