"""Static vs dynamic source density (poster subsection 3.4).

Model (as in 3.2/3.3):
    u_t = Du u_xx + rho a u^2 / v - mu_u u
    v_t = Dv v_xx + rho b u^2 - mu_v v + p_v
    static : rho(x) fixed (asymmetric zig-zag)
    dynamic: tau rho_t = D_rho rho_xx + u - rho,  rho(0, x) = zig-zag
Start: u = 0 with a random wound at the two zig-zag points.
Static rho keeps two heads at the zig-zag points; dynamic rho holds them only for a
while (t ~ 10) and then relaxes to the Turing pattern (boundary peaks).

Run from the poster2 folder:  python scripts/rho_static_dynamic.py
Output: generated/rho_static.{pdf,png}, generated/rho_dynamic.{pdf,png};
simulation cache in generated/rho_static_dynamic_*.npz.
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
import regeneration_sims as R  # noqa: E402

OUT = R.OUT
RHO = "#7B4FA0"

# ================================================================ CONFIG
L = 3.0
X1, X2 = 0.2, 0.9                 # zig-zag break points (fraction of L)
RHO0, RHO1 = 0.8, 1.0             # rho = RHO0 + RHO1 * (x/L - last break point)
TAU, D_RHO = 1.0, 0.1             # dynamic source density
WOUND_W, WOUND_A, SEED = 0.02, 3.0, 1
T_MID, T_END = 10.0, 5000.0
PPU, DT = 100, 0.03               # grid points per unit length, time step
FIG_W, FIG_H = 38.0, 11.0         # cm, 1:1 on the poster
FS = dict(tick=14, label=15, title=15, arrow=14, note=14)
# ================================================================


def zigzag(s):
    return np.where(s < X1, RHO0 + RHO1 * s,
                    np.where(s < X2, RHO0 + RHO1 * (s - X1), RHO0 + RHO1 * (s - X2)))


def matrix(N, dx, D):
    r = D * DT / dx**2
    ab = np.zeros((3, N))
    ab[1] = 1 + 2 * r
    ab[0, 1:] = -r
    ab[2, :-1] = -r
    ab[0, 1] = -2 * r
    ab[2, -2] = -2 * r
    return ab


def simulate(dynamic):
    N = int(PPU * L) + 1
    x = np.linspace(0, L, N)
    s = x / L
    dx = x[1] - x[0]
    Au, Av, Ar = matrix(N, dx, R.Du), matrix(N, dx, R.Dv), matrix(N, dx, D_RHO / TAU)
    rho = zigzag(s)
    rng = np.random.default_rng(SEED)
    u = np.zeros(N)
    band = (abs(s - X1) < WOUND_W) | (abs(s - X2) < WOUND_W)
    u[band] = rng.uniform(0, WOUND_A, band.sum())
    v = np.full(N, R.p_v / R.mu_v)
    snaps = [(u.copy(), rho.copy())]
    t = 0.0
    for T in (T_MID, T_END):
        for _ in range(int(round((T - t) / DT))):
            f = rho * R.a * u * u / v - R.mu_u * u
            g = rho * R.b * u * u - R.mu_v * v + R.p_v
            un = np.maximum(solve_banded((1, 1), Au, u + DT * f), 0)
            v = solve_banded((1, 1), Av, v + DT * g)
            if dynamic:
                rho = solve_banded((1, 1), Ar, rho + DT / TAU * (u - rho))
            u = un
        t = T
        snaps.append((u.copy(), rho.copy()))
    return s, snaps


def cached(dynamic):
    f = OUT / f"rho_static_dynamic_{'dyn' if dynamic else 'static'}.npz"
    key = np.array([L, X1, X2, RHO0, RHO1, TAU, D_RHO, WOUND_W, WOUND_A, SEED, T_MID, T_END, PPU, DT])
    if f.exists():
        d = np.load(f)
        if np.array_equal(d["key"], key):
            return d["s"], [(d[f"u{i}"], d[f"r{i}"]) for i in range(3)]
    s, snaps = simulate(dynamic)
    np.savez(f, key=key, s=s, **{f"u{i}": u for i, (u, _) in enumerate(snaps)},
             **{f"r{i}": r for i, (_, r) in enumerate(snaps)})
    return s, snaps


def style(ax, ymax, yticks):
    ax.set_facecolor(R.PAPER)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    for sp in ("left", "bottom"):
        ax.spines[sp].set_color(R.INK)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, ymax)
    ax.set_xticks([])
    ax.set_yticks(yticks)
    ax.tick_params(labelsize=FS["tick"], colors=R.INK, length=3, pad=2)


def panel(fig, x0, y0, w, s, u, r, ylabels=False, wound=False):
    """u on top, rho strip below."""
    hu, hr, gap = 2.6, 1.0, 0.25
    axu = fig.add_axes([x0 / FIG_W, (y0 + hr + gap) / FIG_H, w / FIG_W, hu / FIG_H])
    axr = fig.add_axes([x0 / FIG_W, y0 / FIG_H, w / FIG_W, hr / FIG_H])
    style(axu, 6.0, [0, 5])
    style(axr, 2.0, [])
    for xb in (X1, X2):
        for ax in (axu, axr):
            ax.axvline(xb, color=R.MID, lw=1.0, ls=(0, (3, 3)))
    if wound:
        for xb in (X1, X2):
            axu.axvspan(xb - WOUND_W, xb + WOUND_W, color=R.COPPER, alpha=0.18, lw=0)
    axu.fill_between(s, 0, u, color=R.UCOL, alpha=0.15, lw=0)
    axu.plot(s, u, color=R.UCOL, lw=1.8)
    axr.fill_between(s, 0, r, color=RHO, alpha=0.28, lw=0)
    axr.plot(s, r, color=RHO, lw=1.8)
    if ylabels:
        axu.set_ylabel("u", color=R.UCOL, fontsize=FS["label"], rotation=0, labelpad=12,
                       va="center")
        axr.set_ylabel(r"$\rho$", color=RHO, fontsize=FS["label"] + 2, rotation=0,
                       labelpad=12, va="center")
    return axu


def arrow(fig, a1, a2, label):
    b1, b2 = a1.get_position(), a2.get_position()
    y = b1.y0 + 0.4 * b1.height
    x0, x1 = b1.x1 + 0.3 / FIG_W, b2.x0 - 0.6 / FIG_W
    fig.patches.append(FancyArrowPatch((x0, y), (x1, y), transform=fig.transFigure,
                                       arrowstyle="-|>", mutation_scale=15, lw=2.0,
                                       color=R.PETROL))
    fig.text((x0 + x1) / 2, y + 0.25 / FIG_H, label, ha="center", va="bottom",
             fontsize=FS["arrow"], color=R.PETROL, fontweight="bold")


def main():
    from matplotlib import font_manager
    names = {f.name for f in font_manager.fontManager.ttflist}
    font = next((n for n in ("Arial", "Liberation Sans") if n in names), "DejaVu Sans")
    plt.rcParams.update({"font.family": font, "pdf.fonttype": 42, "mathtext.fontset": "cm"})

    s, st = cached(False)
    _, dy = cached(True)

    ML, W, GAP = 1.2, 10.3, 2.5
    cols = [ML + i * (W + GAP) for i in range(3)]
    y0 = 0.3
    H1 = 4.5 + y0 + 0.6                               # height of one row figure

    # ---- static rho: two columns (start -> t -> infinity)
    fig = plt.figure(figsize=(FIG_W / 2.54, H1 / 2.54), facecolor=R.PAPER)
    global FIG_H
    FIG_H = H1
    fig.text(ML / FIG_W, (y0 + 4.1) / FIG_H, r"static $\rho(x)$", fontsize=FS["title"],
             fontweight="bold", color=R.PETROL)
    a0 = panel(fig, cols[0], y0, W, s, st[0][0], st[0][1], ylabels=True, wound=True)
    a2 = panel(fig, cols[2], y0, W, s, st[2][0], st[2][1])
    arrow(fig, a0, a2, r"$t\to\infty$")
    a2.text(1.0, 1.04, "heads stay at the graft", transform=a2.transAxes, ha="right",
            va="bottom", fontsize=FS["note"], fontweight="bold", color=R.UCOL)
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"rho_static.{ext}", facecolor=R.PAPER, dpi=300)

    # ---- dynamic rho: three columns (start -> t_mid -> t -> infinity)
    fig = plt.figure(figsize=(FIG_W / 2.54, H1 / 2.54), facecolor=R.PAPER)
    fig.text(ML / FIG_W, (y0 + 4.1) / FIG_H, r"dynamic $\rho(t,x)$", fontsize=FS["title"],
             fontweight="bold", color=R.PETROL)
    b0 = panel(fig, cols[0], y0, W, s, dy[0][0], dy[0][1], ylabels=True, wound=True)
    b1 = panel(fig, cols[1], y0, W, s, dy[1][0], dy[1][1])
    b2 = panel(fig, cols[2], y0, W, s, dy[2][0], dy[2][1])
    arrow(fig, b0, b1, rf"$t={T_MID:g}$")
    arrow(fig, b1, b2, r"$t\to\infty$")
    b2.text(1.0, 1.04, "Turing pattern", transform=b2.transAxes, ha="right", va="bottom",
            fontsize=FS["note"], fontweight="bold", color=R.MID)
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"rho_dynamic.{ext}", facecolor=R.PAPER, dpi=300)

    def pk(u):
        return [round(float(s[i]), 2) for i in range(1, len(s) - 1)
                if u[i] > u[i - 1] and u[i] >= u[i + 1] and u[i] > 0.5] + \
               ([0.0] if u[0] > 0.5 and u[0] >= u[1] else []) + \
               ([1.0] if u[-1] > 0.5 and u[-1] >= u[-2] else [])
    print("static peaks:", pk(st[2][0]), "| dynamic t_mid:", pk(dy[1][0]), "end:", pk(dy[2][0]))


if __name__ == "__main__":
    main()
