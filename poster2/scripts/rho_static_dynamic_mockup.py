"""Visual prototype for poster subsection 3.4: static versus dynamic rho.

This script is deliberately a layout prototype, not a quantitative simulation
of the full Gierer-Meinhardt system.  It keeps the experimental comparison
clean: both rows start from the same two wound-like perturbations of u and the
same zig-zag source-density profile.  In the static row rho remains fixed and
pins the two peaks; in the dynamic row rho smooths out and the final u profile
is a Turing-selected pattern.

Replace the functions `u_static` and `u_dynamic` with Julia solver snapshots
once the numerical experiment is chosen.  The plot layout and colour system can
then remain unchanged.

Run from poster2:
    python scripts/rho_static_dynamic_mockup.py

Outputs:
    generated/rho_static_dynamic_mockup.pdf
    generated/rho_static_dynamic_mockup.png
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch


ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "generated"
OUT.mkdir(exist_ok=True)

# Poster palette -------------------------------------------------------------
PAPER, INK, MID, RULE = "#F4F6F5", "#1E2A30", "#66747A", "#CFD8DA"
PETROL, COPPER = "#123B4A", "#D0703C"
U, RHO = "#C61826", "#7B4FA0"

# Geometry in centimetres, matching the 38.6 cm poster column ----------------
FIG_W, FIG_H = 38.6, 13.2
ML, MR = 1.4, 0.6
PW, PH = 8.5, 3.25                 # one panel: u above rho
GAP = 3.0
Y_BOTTOM, Y_TOP = 1.0, 7.55
FS = dict(tick=13, label=16, title=16, arrow=15, note=14)

X1, X2 = 0.20, 0.90
x = np.linspace(0.0, 1.0, 900)


def zigzag(x):
    """Three ramp segments, reset at x1 and x2 as in the proposed rho(x)."""
    return np.piecewise(
        x,
        [x < X1, (x >= X1) & (x < X2), x >= X2],
        [lambda z: 0.20 + 2.20 * z,
         lambda z: 0.20 + 2.20 * (z - X1),
         lambda z: 0.20 + 2.20 * (z - X2)],
    )


def gauss(x, centre, width, height):
    return height * np.exp(-0.5 * ((x - centre) / width) ** 2)


def wounds(x):
    """u=0 except for two equal, narrow wound-like perturbations."""
    return gauss(x, X1, 0.025, 0.40) + gauss(x, X2, 0.025, 0.40)


def u_static(stage):
    if stage == 0:
        return wounds(x)
    # the profile selected by fixed rho, kept at both late snapshots
    return gauss(x, X1, 0.055, 3.45) + gauss(x, X2, 0.055, 3.45)


def rho_dynamic(stage):
    r0 = zigzag(x)
    if stage == 0:
        return r0
    if stage == 1:
        return 0.60 * r0 + 0.40 * (0.45 + 0.80 * x)
    return 0.45 + 0.80 * x


def u_dynamic(stage):
    if stage == 0:
        return wounds(x)
    if stage == 1:
        # peaks still sit at the two positions imposed by the initial rho
        return gauss(x, X1, 0.055, 3.20) + gauss(x, X2, 0.055, 3.20)
    # after rho relaxes, the final pattern is selected by the AI dynamics
    return (gauss(x, 0.12, 0.052, 3.20) + gauss(x, 0.49, 0.052, 3.20)
            + gauss(x, 0.82, 0.052, 3.20))


def setup_fonts():
    from matplotlib import font_manager
    names = {f.name for f in font_manager.fontManager.ttflist}
    font = next((n for n in ("Arial", "Liberation Sans") if n in names), "DejaVu Sans")
    plt.rcParams.update({"font.family": font, "pdf.fonttype": 42, "mathtext.fontset": "cm"})


def add_panel(fig, x_cm, y_cm, u, rho, *, ylabel=False):
    """One compact panel: u on top, rho below, sharing the x coordinate."""
    axu = fig.add_axes([x_cm / FIG_W, (y_cm + 1.03) / FIG_H, PW / FIG_W, 2.22 / FIG_H])
    axr = fig.add_axes([x_cm / FIG_W, y_cm / FIG_H, PW / FIG_W, 0.78 / FIG_H])
    for ax in (axu, axr):
        ax.set_facecolor(PAPER)
        ax.set_xlim(0, 1)
        ax.set_xticks([])
        ax.set_yticks([])
        for side in ("top", "right", "left"):
            ax.spines[side].set_visible(False)
        ax.spines["bottom"].set_color(INK)
    axu.set_ylim(0, 3.75)
    axu.fill_between(x, 0, u, color=U, alpha=0.16, lw=0)
    axu.plot(x, u, color=U, lw=2.25)
    axr.set_ylim(0, 1.55)
    axr.fill_between(x, 0, rho, color=RHO, alpha=0.20, lw=0)
    axr.plot(x, rho, color=RHO, lw=2.15)
    if ylabel:
        axu.text(-0.08, 0.50, r"$u$", transform=axu.transAxes, color=U,
                 fontsize=FS["label"] + 2, ha="right", va="center")
        axr.text(-0.08, 0.48, r"$\rho$", transform=axr.transAxes, color=RHO,
                 fontsize=FS["label"] + 2, ha="right", va="center")
    return axu


def arrow(fig, left_ax, right_ax, label):
    b1, b2 = left_ax.get_position(), right_ax.get_position()
    y = b1.y0 + 0.58 * b1.height
    x0, x1 = b1.x1 + 0.28 / FIG_W, b2.x0 - 0.42 / FIG_W
    fig.patches.append(FancyArrowPatch((x0, y), (x1, y), transform=fig.transFigure,
                                       arrowstyle="-|>", mutation_scale=15, lw=2.0,
                                       color=PETROL))
    fig.text((x0 + x1) / 2, y + 0.30 / FIG_H, label, ha="center", va="bottom",
             fontsize=FS["arrow"], color=PETROL, fontweight="bold")


def row_title(fig, y_cm, title, subtitle):
    fig.text(ML / FIG_W, (y_cm + PH + 0.47) / FIG_H, title, color=PETROL,
             fontsize=FS["title"], fontweight="bold", ha="left", va="bottom")
    fig.text((ML + 8.4) / FIG_W, (y_cm + PH + 0.49) / FIG_H, subtitle, color=MID,
             fontsize=FS["note"], ha="left", va="bottom")


def main():
    setup_fonts()
    fig = plt.figure(figsize=(FIG_W / 2.54, FIG_H / 2.54), facecolor=PAPER)
    x0, x1, x2 = ML, ML + PW + GAP, ML + 2 * (PW + GAP)

    # Static rho: same selected state persists at t=10.
    top = [add_panel(fig, xp, Y_TOP, u_static(i), zigzag(x), ylabel=(i == 0))
           for i, xp in enumerate((x0, x1, x2))]
    row_title(fig, Y_TOP, r"static $\rho(x)$", "fixed source density pins peak position")
    fig.text(top[1].get_position().x0, top[1].get_position().y1 + 0.03,
             "two selected peaks", color=U, fontsize=FS["note"], fontweight="bold", ha="left")
    fig.text(top[2].get_position().x0, top[2].get_position().y1 + 0.03,
             "same pinned pattern", color=U, fontsize=FS["note"], fontweight="bold", ha="left")
    arrow(fig, top[0], top[1], "selection")
    arrow(fig, top[1], top[2], r"$t=10$")

    # Dynamic rho: identical early selection, but rho relaxes and releases it.
    bottom = [add_panel(fig, xp, Y_BOTTOM, u_dynamic(i), rho_dynamic(i), ylabel=(i == 0))
              for i, xp in enumerate((x0, x1, x2))]
    row_title(fig, Y_BOTTOM, r"dynamic $\rho(x,t)$", "transient positional memory")
    fig.text(bottom[1].get_position().x0, bottom[1].get_position().y1 + 0.03,
             "metastable two-peak state", color=U, fontsize=FS["note"], fontweight="bold", ha="left")
    fig.text(bottom[2].get_position().x0, bottom[2].get_position().y1 + 0.03,
             "Turing-selected pattern", color=U, fontsize=FS["note"], fontweight="bold", ha="left")
    arrow(fig, bottom[0], bottom[1], "selection")
    arrow(fig, bottom[1], bottom[2], r"$\rho$ relaxes")

    fig.text(ML / FIG_W, 0.23 / FIG_H,
             r"Fixed $\rho$ stores position indefinitely; dynamic $\rho$ selects it early, then releases the pattern.",
             color=PETROL, fontsize=FS["note"], fontweight="bold", ha="left", va="bottom")
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"rho_static_dynamic_mockup.{ext}", facecolor=PAPER, dpi=300)


if __name__ == "__main__":
    main()

