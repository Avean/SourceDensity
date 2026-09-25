"""History-dependent pattern selection for poster subsection 2.5.

Same model and parameters as regeneration_sims.py.
Top row   : start near the diffusion-unstable state E+ (small noise), t -> infinity
            - small domain L = 0.5  -> one peak
            - large domain L = 3    -> several peaks
Bottom row: the same small-domain start -> one peak, then uniform growth
            (L multiplied by 2^(1/14) per step, short relaxation after each step)
            L = 0.5 -> 1 -> 2 -> 3 : the single peak persists.
All panels share one x-scale (cm per unit length); both rows have equal width.
Initial states are drawn with the noise magnified x5 (the simulation uses 1 %).

Run from the poster2 folder:  python scripts/pattern_history_sims.py
Output: generated/pattern_history.{pdf,png}
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import regeneration_sims as R  # noqa: E402

OUT = R.OUT
PTS_PER_UNIT = 400
L_SMALL, L_LARGE = 0.5, 3.0
SEED, NOISE, NOISE_SHOW = 1, 0.01, 5
T_DDI, T_STEP, T_END = 600.0, 10.0, 600.0
STEPS_PER_DOUBLING = 14
SNAPSHOTS = (1.0, 2.0, 3.0)
U_PLUS, V_PLUS = 1.0, 3.0      # E+ for the poster parameters

# ---------------------------------------------------------------- layout (cm, 1:1 on poster)
FIG_W, FIG_H = 38.6, 10.4
ML, MR = 2.0, 0.6                # left / right margin
ROW_W = FIG_W - ML - MR
GAP2 = 2.2                       # arrow gap in the bottom row
SCALE = (ROW_W - 4 * GAP2) / (2 * L_SMALL + 1.0 + 2.0 + L_LARGE)   # cm per unit
GAP1 = 2.2                       # arrow gap in the top row
SEP1 = ROW_W - SCALE * (2 * L_SMALL + 2 * L_LARGE) - 2 * GAP1       # gap between pairs
PH = 2.8                         # panel height
Y_BOTTOM, Y_TOP = 1.15, 1.15 + 2.8 + 2.35
FS = dict(tick=16, label=16, title=16, arrow=15, note=15)


def grid(L):
    n = int(round(PTS_PER_UNIT * L)) + 1
    x = np.linspace(0, L, n)
    return x, x[1] - x[0]


def ddi(L):
    """Returns grid, initial noise (u) and the final state."""
    x, dx = grid(L)
    rng = np.random.default_rng(SEED)
    nu = NOISE * rng.standard_normal(len(x))
    u = U_PLUS + nu
    v = V_PLUS + NOISE * rng.standard_normal(len(x))
    u, v = R.run(u, v, dx, T_DDI)
    return x, nu, u, v


def grow(x, u, v):
    """Uniform stretching from L_SMALL to L_LARGE, keeping snapshots at SNAPSHOTS."""
    snaps = []
    L = x[-1]
    k = 0
    while L < L_LARGE - 1e-9:
        k += 1
        Ln = min(L_SMALL * 2 ** (k / STEPS_PER_DOUBLING), L_LARGE)
        xn, dxn = grid(Ln)
        u, v = np.interp(xn * L / Ln, x, u), np.interp(xn * L / Ln, x, v)
        x, L = xn, Ln
        u, v = R.run(u, v, dxn, T_STEP)
        if any(abs(L - s) < 1e-6 for s in SNAPSHOTS):
            if abs(L - L_LARGE) < 1e-6:
                u, v = R.run(u, v, dxn, T_END)
            snaps.append((x, u))
    return snaps


def peaks(x, u, thr=0.5):
    p = [i for i in range(1, len(x) - 1) if u[i] > u[i - 1] and u[i] >= u[i + 1] and u[i] > thr]
    if u[0] > thr and u[0] >= u[1]:
        p = [0] + p
    if u[-1] > thr and u[-1] >= u[-2]:
        p = p + [len(x) - 1]
    return len(p)


def style(ax, L, ylabel=False):
    ax.set_facecolor(R.PAPER)
    ax.set_xlim(0, L)
    ax.set_ylim(0, 4.3)
    ax.set_xticks(np.arange(0, L + 1e-9, 0.5 if L <= 1 else 1.0))
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda t, _: f"{t:g}"))
    ax.set_yticks([0, 4])
    ax.tick_params(labelsize=FS["tick"], colors=R.INK, length=3, pad=2)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    for sp in ("left", "bottom"):
        ax.spines[sp].set_color(R.INK)
    ax.grid(color=R.RULE, lw=0.7)
    ax.set_axisbelow(True)
    if ylabel:
        ax.set_ylabel("u", color=R.UCOL, fontsize=FS["label"], labelpad=12, rotation=0, va="center")


def profile(ax, x, u, eplus_line=False):
    if eplus_line:
        ax.axhline(U_PLUS, color=R.MID, lw=1.5, ls=(0, (4, 3)))
    ax.fill_between(x, 0, u, color=R.UCOL, alpha=0.15, lw=0)
    ax.plot(x, u, color=R.UCOL, lw=2.0)


def initial(ax, x, nu):
    """Initial state E+ + noise, noise magnified for visibility."""
    un = U_PLUS + NOISE_SHOW * nu
    ax.fill_between(x, 0, un, color=R.UCOL, alpha=0.15, lw=0)
    ax.plot(x, un, color=R.UCOL, lw=1.0)
    ax.axhline(U_PLUS, color=R.MID, lw=1.5, ls=(0, (4, 3)), zorder=3)


def add_axes(fig, x0_cm, y0_cm, L):
    return fig.add_axes([x0_cm / FIG_W, y0_cm / FIG_H, SCALE * L / FIG_W, PH / FIG_H])


def arrow(fig, ax1, ax2, label):
    b1, b2 = ax1.get_position(), ax2.get_position()
    y = b1.y0 + 0.45 * b1.height
    x0, x1 = b1.x1 + 0.3 / FIG_W, b2.x0 - 0.7 / FIG_W
    fig.patches.append(FancyArrowPatch((x0, y), (x1, y), transform=fig.transFigure,
                                       arrowstyle="-|>", mutation_scale=15, lw=2.0,
                                       color=R.PETROL))
    fig.text((x0 + x1) / 2, y + 0.25 / FIG_H, label, ha="center", va="bottom",
             fontsize=FS["arrow"], color=R.PETROL, fontweight="bold", linespacing=1.0)


def title(fig, ax, text):
    b = ax.get_position()
    fig.text(b.x0, b.y1 + 0.3 / FIG_H, text, fontsize=FS["title"], fontweight="bold",
             color=R.PETROL, ha="left", va="bottom")


def note(ax, text, color):
    ax.text(1.0, 1.04, text, transform=ax.transAxes, ha="right", va="bottom",
            fontsize=FS["note"], fontweight="bold", color=color, linespacing=1.0)


def main():
    from matplotlib import font_manager
    names = {f.name for f in font_manager.fontManager.ttflist}
    font = next((n for n in ("Arial", "Liberation Sans") if n in names), "DejaVu Sans")
    plt.rcParams.update({"font.family": font, "pdf.fonttype": 42})

    xs, ns, us, vs = ddi(L_SMALL)
    xl, nl, ul, _ = ddi(L_LARGE)
    snaps = grow(xs, us, vs)

    fig = plt.figure(figsize=(FIG_W / 2.54, FIG_H / 2.54), facecolor=R.PAPER)

    # ---------------- top row: two independent DDI experiments
    x0 = ML
    a0 = add_axes(fig, x0, Y_TOP, L_SMALL); x0 += SCALE * L_SMALL + GAP1
    a1 = add_axes(fig, x0, Y_TOP, L_SMALL); x0 += SCALE * L_SMALL + SEP1
    a2 = add_axes(fig, x0, Y_TOP, L_LARGE); x0 += SCALE * L_LARGE + GAP1
    a3 = add_axes(fig, x0, Y_TOP, L_LARGE)
    for ax, L in ((a0, L_SMALL), (a1, L_SMALL), (a2, L_LARGE), (a3, L_LARGE)):
        style(ax, L, ylabel=(ax is a0))
    initial(a0, xs, ns)
    profile(a1, xs, us, eplus_line=True)
    initial(a2, xl, nl)
    profile(a3, xl, ul, eplus_line=True)
    title(fig, a0, "small domain")
    title(fig, a2, "large domain")
    note(a3, "several peaks", R.UCOL)
    arrow(fig, a0, a1, r"$t\to\infty$")
    arrow(fig, a2, a3, r"$t\to\infty$")

    # ---------------- bottom row: same small start, then growth
    x0 = ML
    b0 = add_axes(fig, x0, Y_BOTTOM, L_SMALL); x0 += SCALE * L_SMALL + GAP2
    b1 = add_axes(fig, x0, Y_BOTTOM, L_SMALL); x0 += SCALE * L_SMALL + GAP2
    style(b0, L_SMALL, ylabel=True)
    style(b1, L_SMALL)
    initial(b0, xs, ns)
    profile(b1, xs, us, eplus_line=True)
    axes = [b0, b1]
    for x, u in snaps:
        L = x[-1]
        ax = add_axes(fig, x0, Y_BOTTOM, L); x0 += SCALE * L + GAP2
        style(ax, L)
        profile(ax, x, u, eplus_line=True)
        axes.append(ax)
    title(fig, b0, "small domain, then growth")
    note(axes[-1], "one peak", R.UCOL)
    arrow(fig, b0, b1, r"$t\to\infty$")
    for a, b in zip(axes[1:-1], axes[2:]):
        arrow(fig, a, b, "growth")

    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"pattern_history.{ext}", facecolor=R.PAPER, dpi=300)
    print("scale %.2f cm/unit, sep %.2f cm" % (SCALE, SEP1))
    print("peaks: small DDI", peaks(xs, us), "| large DDI", peaks(xl, ul),
          "| grown", peaks(*snaps[-1]), "| snapshot L:", [round(float(s[0][-1]), 3) for s in snaps])


if __name__ == "__main__":
    main()
