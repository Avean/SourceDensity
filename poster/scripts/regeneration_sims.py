"""Regeneration experiment for poster subsection 2.3.

Model (same parameters as the right phase portrait):
    u_t = Du u_xx + a u^2 / v - mu_u u
    v_t = Dv v_xx + b u^2 - mu_v v + p_v          (Neumann boundaries)

Row 1: steady head at x = 0  -> cut at x_c  -> no wound signal  -> decay to u = 0
Row 2: steady head at x = 0  -> cut at x_c  -> random wound near the cut -> head regrows

Scheme: IMEX Euler (implicit diffusion, explicit reaction).
Run from the poster2 folder:  python scripts/regeneration_sims.py
Output: generated/regeneration_sims.{pdf,png}
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch
from scipy.linalg import solve_banded

OUT = Path(__file__).resolve().parent.parent / "generated"
OUT.mkdir(exist_ok=True)

# ---------------------------------------------------------------- parameters
a, b, mu_u, mu_v, p_v = 1.5, 2.0, 0.5, 1.0, 1.0
Du, Dv = 0.0015, 0.08
L, N = 1.0, 401
X_CUT = 0.35                 # cut position
WOUND_W, WOUND_A = 0.05, 3.0  # wound: u ~ U(0, WOUND_A) on [X_CUT, X_CUT + WOUND_W]
SEED = 3
DT, T_SS = 0.01, 400.0

# ---------------------------------------------------------------- palette
PAPER, INK, MID, RULE = "#F4F6F5", "#1E2A30", "#66747A", "#CFD8DA"
UCOL, PETROL, COPPER = "#C61826", "#123B4A", "#D0703C"


def diffusion_matrix(n, dx, D):
    r = D * DT / dx**2
    ab = np.zeros((3, n))
    ab[1] = 1 + 2 * r
    ab[0, 1:] = -r
    ab[2, :-1] = -r
    ab[0, 1] = -2 * r          # Neumann via ghost points
    ab[2, -2] = -2 * r
    return ab


def run(u, v, dx, T):
    Au, Av = diffusion_matrix(len(u), dx, Du), diffusion_matrix(len(u), dx, Dv)
    for _ in range(int(round(T / DT))):
        f = a * u * u / v - mu_u * u
        g = b * u * u - mu_v * v + p_v
        u = np.maximum(solve_banded((1, 1), Au, u + DT * f), 0.0)
        v = solve_banded((1, 1), Av, v + DT * g)
    return u, v


def simulate():
    x = np.linspace(0, L, N)
    dx = x[1] - x[0]
    # 1) head at the left end: start at rest, localised perturbation at x = 0
    u0 = 2.4 * np.exp(-(x / 0.05) ** 2)
    v0 = np.full(N, p_v / mu_v)
    u_ss, v_ss = run(u0, v0, dx, T_SS)

    # 2) cut: keep [X_CUT, L]
    keep = x >= X_CUT - 1e-12
    xc, uc, vc = x[keep], u_ss[keep].copy(), v_ss[keep].copy()

    # 3a) no wound signal
    u_nw, _ = run(uc.copy(), vc.copy(), dx, T_SS)

    # 3b) wound: large random activator perturbation near the cut
    rng = np.random.default_rng(SEED)
    uw = uc.copy()
    band = xc <= X_CUT + WOUND_W
    uw[band] += rng.uniform(0, WOUND_A, band.sum())
    u_w, _ = run(uw.copy(), vc.copy(), dx, T_SS)
    return x, u_ss, xc, uc, uw, u_nw, u_w


# ---------------------------------------------------------------- figure layout (cm, 1:1 on poster)
FIG_W, FIG_H = 23.0, 7.7
ML, PW, GAP = 1.2, 5.6, 2.05          # left margin, panel width, arrow gap
MB, PH, RGAP, MT = 0.75, 2.3, 1.6, 0.8  # bottom margin, panel height, row gap, top
FS = dict(tick=14, label=14, title=14, arrow=13, note=12)


def panel(ax, x, u, *, cut_line=False, removed=False, wound=False):
    ax.set_facecolor(PAPER)
    if removed:
        ax.axvspan(0, X_CUT, color=RULE, alpha=0.55, lw=0)
        ax.text(X_CUT / 2, 3.5, "removed", ha="center", va="center",
                fontsize=FS["note"] - 1, color=MID)
    if wound:
        ax.axvspan(X_CUT, X_CUT + WOUND_W, color=COPPER, alpha=0.18, lw=0)
    ax.fill_between(x, 0, u, color=UCOL, alpha=0.15, lw=0)
    ax.plot(x, u, color=UCOL, lw=2.0)
    if cut_line:
        ax.axvline(X_CUT, color=UCOL, lw=1.8, ls=(0, (4, 3)))
    ax.set_xlim(0, L)
    ax.set_ylim(0, 4.3)
    ax.set_xticks([0, 0.5, 1])
    ax.set_yticks([0, 4])
    ax.tick_params(labelsize=FS["tick"], colors=INK, length=3, pad=2)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    for sp in ("left", "bottom"):
        ax.spines[sp].set_color(INK)
    ax.grid(color=RULE, lw=0.7)
    ax.set_axisbelow(True)


def arrow(fig, ax1, ax2, label):
    b1, b2 = ax1.get_position(), ax2.get_position()
    y = b1.y0 + 0.45 * b1.height
    x0, x1 = b1.x1 + 0.2 / FIG_W, b2.x0 - 0.55 / FIG_W
    fig.patches.append(FancyArrowPatch((x0, y), (x1, y), transform=fig.transFigure,
                                       arrowstyle="-|>", mutation_scale=15, lw=2.0,
                                       color=PETROL))
    fig.text((x0 + x1) / 2, y + 0.25 / FIG_H, label, ha="center", va="bottom",
             fontsize=FS["arrow"], color=PETROL, fontweight="bold", linespacing=1.0)


def main():
    from matplotlib import font_manager
    names = {f.name for f in font_manager.fontManager.ttflist}
    font = next((n for n in ("Arial", "Liberation Sans") if n in names), "DejaVu Sans")
    plt.rcParams.update({"font.family": font, "pdf.fonttype": 42})
    x, u_ss, xc, uc, uw, u_nw, u_w = simulate()

    fig = plt.figure(figsize=(FIG_W / 2.54, FIG_H / 2.54), facecolor=PAPER)
    fx = lambda cm: cm / FIG_W
    fy = lambda cm: cm / FIG_H
    rows = [(MB + PH + RGAP, "wound signal near the cut",
             [(x, u_ss, dict(cut_line=True)), (xc, uw, dict(removed=True, wound=True)),
              (xc, u_w, dict(removed=True))],
             ["cut +\nwound", r"$t\to\infty$"], "head\nregenerates"),
            (MB, "no wound signal",
             [(x, u_ss, dict(cut_line=True)), (xc, uc, dict(removed=True)),
              (xc, u_nw, dict(removed=True))],
             ["cut", r"$t\to\infty$"], "returns\nto rest")]
    for y0, title, panels, labels, result in rows:
        axes = []
        for i, (xx, uu, kw) in enumerate(panels):
            ax = fig.add_axes([fx(ML + i * (PW + GAP)), fy(y0), fx(PW), fy(PH)])
            panel(ax, xx, uu, **kw)
            if i == 0:
                ax.set_ylabel("u", color=UCOL, fontsize=FS["label"], labelpad=10, rotation=0, va="center")
            axes.append(ax)
        fig.text(fx(ML), fy(y0 + PH + 0.25), title, fontsize=FS["title"],
                 fontweight="bold", color=PETROL)
        axes[2].text(0.98, 0.95, result, transform=axes[2].transAxes, ha="right",
                     va="top", fontsize=FS["note"], fontweight="bold",
                     color=MID if result.startswith("returns") else UCOL, linespacing=1.0)
        arrow(fig, axes[0], axes[1], labels[0])
        arrow(fig, axes[1], axes[2], labels[1])
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"regeneration_sims.{ext}", facecolor=PAPER, dpi=300)
    print("max u after cut, no wound:", u_nw.max(), " with wound:", u_w.max(),
          " peak position:", xc[u_w.argmax()])


if __name__ == "__main__":
    main()
