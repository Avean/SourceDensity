"""Plot actual Warsaw-solver snapshots for poster subsection 3.4.

Input CSV files are written by run_rho_static_dynamic.jl.  This script only
formats those results; it contains no model equations or synthetic profiles.

Run from poster2 after the Julia wrapper:
  python scripts/plot_rho_static_dynamic_solver.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch


ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "generated" / "rho_static_dynamic_data"
OUT = ROOT / "generated"

PAPER, INK, MID, RULE = "#F4F6F5", "#1E2A30", "#66747A", "#CFD8DA"
PETROL, U, RHO = "#123B4A", "#C61826", "#7B4FA0"
FIG_W, FIG_H = 38.6, 13.2
ML, PW, GAP = 1.4, 8.5, 3.0
PH, Y_BOTTOM, Y_TOP = 3.25, 1.0, 7.55
FS = dict(label=16, title=16, arrow=15, note=14)


def read(case, t):
    path = DATA / f"{case}_t{t:05d}.csv"
    return np.loadtxt(path, delimiter=",", skiprows=1, unpack=True)


def setup_fonts():
    from matplotlib import font_manager
    names = {f.name for f in font_manager.fontManager.ttflist}
    font = next((n for n in ("Arial", "Liberation Sans") if n in names), "DejaVu Sans")
    plt.rcParams.update({"font.family": font, "pdf.fonttype": 42, "mathtext.fontset": "cm"})


def add_panel(fig, x_cm, y_cm, x, u, rho, umax, *, ylabel=False):
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
    axu.set_ylim(0, umax)
    axu.fill_between(x, 0, u, color=U, alpha=0.16, lw=0)
    axu.plot(x, u, color=U, lw=2.25)
    rho_max = max(1e-6, rho.max())
    axr.set_ylim(0, rho_max * 1.10)
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


def label(fig, ax, text, color=U):
    fig.text(ax.get_position().x0, ax.get_position().y1 + 0.03, text, color=color,
             fontsize=FS["note"], fontweight="bold", ha="left")


def main():
    setup_fonts()
    times = (0, 100, 1000)
    records = {case: [read(case, t) for t in times] for case in ("static", "dynamic")}
    umax = 1.10 * max(data[1].max() for row in records.values() for data in row)
    fig = plt.figure(figsize=(FIG_W / 2.54, FIG_H / 2.54), facecolor=PAPER)
    xs = (ML, ML + PW + GAP, ML + 2 * (PW + GAP))

    top = [add_panel(fig, xp, Y_TOP, *data, umax, ylabel=(i == 0))
           for i, (xp, data) in enumerate(zip(xs, records["static"]))]
    fig.text(ML / FIG_W, (Y_TOP + PH + 0.47) / FIG_H, r"static $\rho(x)$", color=PETROL,
             fontsize=FS["title"], fontweight="bold", ha="left")
    fig.text((ML + 8.4) / FIG_W, (Y_TOP + PH + 0.49) / FIG_H,
             "fixed source density", color=MID, fontsize=FS["note"], ha="left")
    label(fig, top[0], r"$t=0$: two wound-like perturbations", MID)
    label(fig, top[1], r"$t=100$: selected pattern")
    label(fig, top[2], r"$t=1000$: retained pattern")
    arrow(fig, top[0], top[1], "selection")
    arrow(fig, top[1], top[2], "pinned")

    bottom = [add_panel(fig, xp, Y_BOTTOM, *data, umax, ylabel=(i == 0))
              for i, (xp, data) in enumerate(zip(xs, records["dynamic"]))]
    fig.text(ML / FIG_W, (Y_BOTTOM + PH + 0.47) / FIG_H, r"dynamic $\rho(x,t)$", color=PETROL,
             fontsize=FS["title"], fontweight="bold", ha="left")
    fig.text((ML + 8.4) / FIG_W, (Y_BOTTOM + PH + 0.49) / FIG_H,
             r"$\tau=10^3$, $D_{sd}=15/\tau$", color=MID, fontsize=FS["note"], ha="left")
    label(fig, bottom[0], r"$t=0$: same initial condition", MID)
    label(fig, bottom[1], r"$t=100$: transient response")
    label(fig, bottom[2], r"$t=1000$: evolving source density")
    arrow(fig, bottom[0], bottom[1], "selection")
    arrow(fig, bottom[1], bottom[2], r"$\rho$ evolves")

    fig.text(ML / FIG_W, 0.23 / FIG_H,
             r"Actual TRBDF2 solver output; static and dynamic cases use the same initial wounds.",
             color=PETROL, fontsize=FS["note"], fontweight="bold", ha="left", va="bottom")
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"rho_static_dynamic_solver.{ext}", facecolor=PAPER, dpi=300)


if __name__ == "__main__":
    main()
