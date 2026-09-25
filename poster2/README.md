# Poster 2 — A0 portrait

- `poster.tex` — portrait poster (petrol + copper, 3 sections with subsections).
  Build: `latexmk -xelatex poster.tex` (Arial if installed, otherwise Liberation Sans).
- `poster.pdf` — current build.
- `assets/` — original images plus processed versions:
  - `livshits_h2f_experiment_transparent.png` — white background removed, cropped.
  - `heidelberg_logo_white.png` — logo text/line recoloured to white for the dark header.
- `scripts/process_assets.py` — regenerates the processed assets.
