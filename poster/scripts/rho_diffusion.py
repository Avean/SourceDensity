"""Source density spread by diffusion (poster subsection 3.4).

A stationary head (activator peak u) sits at x = 1. The source density follows
    tau * rho_t = D_rho * rho_xx + u - rho      (Neumann boundaries),
so its steady state solves (1 - D_rho d^2/dx^2) rho = u. Diffusion spreads rho away
from the head; D_rho sets how far the positional information reaches.

Main curve: intermediate D_rho. Thin dashed curves: too small / too large D_rho.
Run from the poster2 folder:  python scripts/rho_diffusion.py
Output: generated/rho_diffusion.{pdf,png}
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch
from scipy.linalg import solve_banded

sys.path.insert(0, str(Path(__file__).resolve().parent))
import regeneration_sims as R  # noqa: E402  (model, solver, palette)

OUT = R.OUT
RHO = "#7B4FA0"

# ================================================================ CONFIG
L, N = 1.0, 401
D_MAIN = 0.12                   # intermediate diffusion: usable gradient
D_SMALL, D_LARGE = 0.001, 2.0   # too small (stays localised) / too large (nearly flat)
FIG_W, FIG_H = 38.0, 6.2        # cm, 1:1 on the poster
FS = dict(tick=15, label=17, note=15)
# ================================================================


def head_profile():
    """Steady activator peak at x = 0 from the regeneration model, mirrored to x = 1."""
    x = np.linspace(0, L, N)
    dx = x[1] - x[0]
    u, _ = R.run(2.4 * np.exp(-(x / 0.05) ** 2), np.full(N, R.p_v / R.mu_v), dx, 300.0)
    return x, u[::-1]


def steady_rho(u, dx, D):
    r = D / dx**2
    ab = np.zeros((3, len(u)))
    ab[1] = 1 + 2 * r
    ab[0, 1:] = -r
    ab[2, :-1] = -r
    ab[0, 1] = -2 * r
    ab[2, -2] = -2 * r
    return solve_banded((1, 1), ab, u)


def main():
    from matplotlib import font_manager
    names = {f.name for f in font_manager.fontManager.ttflist}
    font = next((n for n in ("Arial", "Liberation Sans") if n in names), "DejaVu Sans")
    plt.rcParams.update({"font.family": font, "pdf.fonttype": 42, "mathtext.fontset": "cm"})

    x, u = head_profile()
    dx = x[1] - x[0]
    rho = {D: steady_rho(u, dx, D) for D in (D_SMALL, D_MAIN, D_LARGE)}
    s = 1.0                                     # rho drawn on the same scale as u (same mass)

    fig = plt.figure(figsize=(FIG_W / 2.54, FIG_H / 2.54), facecolor=R.PAPER)
    ax = fig.add_axes([1.2 / FIG_W, 0.4 / FIG_H, (FIG_W - 8.0) / FIG_W, (FIG_H - 0.7) / FIG_H])
    ax.set_facecolor(R.PAPER)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color(R.INK)
    ax.set_xlim(0, 1.0)
    ax.set_ylim(0, 4.2)
    ax.set_yticks([])
    ax.set_xticks([])

    # too small / too large diffusion (thin, dashed)
    for D in (D_SMALL, D_LARGE):
        ax.plot(x, s * rho[D], color=RHO, lw=1.6, ls=(0, (4, 3)), alpha=0.8)
    # intermediate diffusion + activator
    ax.fill_between(x, 0, s * rho[D_MAIN], color=RHO, alpha=0.22, lw=0)
    ax.plot(x, s * rho[D_MAIN], color=RHO, lw=2.6)
    ax.fill_between(x, 0, u, color=R.UCOL, alpha=0.15, lw=0)
    ax.plot(x, u, color=R.UCOL, lw=2.6)

    # annotations
    ax.add_patch(FancyArrowPatch((0.78, 2.6), (0.48, 2.6), arrowstyle="-|>",
                                 mutation_scale=16, lw=2.0, color=R.PETROL))
    ax.text(0.63, 2.75, "diffusion spreads it", ha="center", va="bottom",
            fontsize=FS["note"], color=R.PETROL, fontweight="bold")
    ax.text(1.02, 3.9, r"$u$", color=R.UCOL, fontsize=FS["label"] + 4, va="center",
            transform=ax.transData, clip_on=False)
    ax.text(1.02, 3.35, "activator,\nlocalises the head", color=R.MID, fontsize=FS["note"],
            va="top", linespacing=1.1, clip_on=False)
    y_r = s * rho[D_MAIN][-1]
    ax.text(1.02, y_r + 0.1, r"$\rho$", color=RHO, fontsize=FS["label"] + 4, va="center",
            clip_on=False)
    ax.text(1.02, y_r - 0.35, "source density,\nspread out", color=R.MID,
            fontsize=FS["note"], va="top", linespacing=1.1, clip_on=False)
    ax.text(0.02, s * rho[D_LARGE][0] + 0.12, r"$D_\rho$ too large", color=RHO,
            fontsize=FS["note"] - 1, va="bottom")
    i = np.searchsorted(x, 0.82)
    ax.text(0.81, s * rho[D_SMALL][i] + 0.1, r"$D_\rho$ too small", color=RHO,
            fontsize=FS["note"] - 1, ha="right", va="bottom")

    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"rho_diffusion.{ext}", facecolor=R.PAPER, dpi=300)


if __name__ == "__main__":
    main()
