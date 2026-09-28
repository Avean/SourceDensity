"""Grafts in the two-equation model, poster subsection 2.5.

Same model and parameters as regeneration_sims.py, on a domain of length L = 2.
Two rows, each: steady head at x = 0 -> activator pulse (graft) -> t -> infinity.
Top    : graft close to the head (x/L = 0.12) -> the pulse vanishes, no new head.
Bottom : graft further away (x/L = 0.42)    -> a second peak survives and drifts
         to the model-selected position 2L/3; the head at x = 0 stays.

Run from the poster2 folder:  python scripts/graft_drift_sims.py
Output: generated/graft_drift.{pdf,png}
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import regeneration_sims as R  # noqa: E402  (shared model, solver and palette)

OUT = R.OUT
L = 2.0
N = int(400 * L) + 1
X_NEAR, X_FAR, A_PULSE, W_PULSE = 0.12, 0.42, 3.0, 0.04   # pulse positions as fraction of L
T_HEAD, T_FINAL = 300.0, 5000.0

# ---------------------------------------------------------------- layout (cm, 1:1 on poster)
FIG_W, FIG_H = 38.0, 9.9
ML, PW, GAP = 1.4, 10.0, 2.9
MB, PH, RGAP = 1.0, 2.8, 2.3
FS = dict(tick=16, label=16, title=16, arrow=15, note=15)


def simulate(x_pulse):
    x = np.linspace(0, L, N)
    dx = x[1] - x[0]
    u, v = R.run(2.4 * np.exp(-(x / 0.05) ** 2), np.full(N, R.p_v / R.mu_v), dx, T_HEAD)
    pulse = A_PULSE * np.exp(-((x - x_pulse * L) / (W_PULSE * L)) ** 2)
    u1 = u + pulse
    u_end, _ = R.run(u1.copy(), v.copy(), dx, T_FINAL)
    return x / L, u, u1, u_end, pulse


def style(ax):
    ax.set_facecolor(R.PAPER)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 4.3)
    ax.set_xticks([0, 1 / 3, 2 / 3, 1])
    ax.set_xticklabels(["0", "1/3", "2/3", "1"])
    ax.set_yticks([0, 4])
    ax.tick_params(labelsize=FS["tick"], colors=R.INK, length=3, pad=2)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    for sp in ("left", "bottom"):
        ax.spines[sp].set_color(R.INK)
    ax.grid(color=R.RULE, lw=0.7)
    ax.set_axisbelow(True)


def profile(ax, x, u):
    ax.fill_between(x, 0, u, color=R.UCOL, alpha=0.15, lw=0)
    ax.plot(x, u, color=R.UCOL, lw=2.0)


def arrow(fig, ax1, ax2, label):
    b1, b2 = ax1.get_position(), ax2.get_position()
    y = b1.y0 + 0.45 * b1.height
    x0, x1 = b1.x1 + 0.3 / FIG_W, b2.x0 - 0.7 / FIG_W
    fig.patches.append(FancyArrowPatch((x0, y), (x1, y), transform=fig.transFigure,
                                       arrowstyle="-|>", mutation_scale=15, lw=2.0,
                                       color=R.PETROL))
    fig.text((x0 + x1) / 2, y + 0.25 / FIG_H, label, ha="center", va="bottom",
             fontsize=FS["arrow"], color=R.PETROL, fontweight="bold", linespacing=1.0)


def row(fig, y0, x_pulse, title, drift):
    xs, u_head, u_pulse, u_end, pulse = simulate(x_pulse)
    axes = [fig.add_axes([(ML + i * (PW + GAP)) / FIG_W, y0 / FIG_H, PW / FIG_W, PH / FIG_H])
            for i in range(3)]
    for ax in axes:
        style(ax)
    axes[0].set_ylabel("u", color=R.UCOL, fontsize=FS["label"], labelpad=12, rotation=0, va="center")
    fig.text(ML / FIG_W, (y0 + PH + 0.3) / FIG_H, title, fontsize=FS["title"],
             fontweight="bold", color=R.PETROL, ha="left", va="bottom")

    profile(axes[0], xs, u_head)                                   # 1) head
    axes[1].axvspan(x_pulse - 2 * W_PULSE, x_pulse + 2 * W_PULSE, color=R.COPPER,
                    alpha=0.18, lw=0)
    profile(axes[1], xs, u_pulse)                                  # 2) head + graft
    profile(axes[2], xs, u_end)                                    # 3) final state
    axes[2].plot(xs, pulse, color=R.MID, lw=1.8, ls=(0, (4, 3)))
    if drift:
        x_new = xs[np.argmax(np.where(xs > 0.2, u_end, 0))]
        axes[2].axvline(2 / 3, color=R.PETROL, lw=1.2, ls=":")
        y_arr = 3.75
        axes[2].annotate("", xy=(x_new, y_arr), xytext=(x_pulse, y_arr),
                         arrowprops=dict(arrowstyle="<|-|>", color=R.PETROL, lw=1.8,
                                         mutation_scale=13, shrinkA=0, shrinkB=0))
        axes[2].text((x_pulse + x_new) / 2, y_arr + 0.15, "drift", ha="center",
                     va="bottom", fontsize=FS["note"], fontweight="bold", color=R.PETROL)
        axes[2].text(1.0, 1.04, "peak at 2/3", transform=axes[2].transAxes, ha="right",
                     va="bottom", fontsize=FS["note"], fontweight="bold", color=R.UCOL)
        info = x_new
    else:
        axes[2].text(1.0, 1.04, "graft vanishes", transform=axes[2].transAxes, ha="right",
                     va="bottom", fontsize=FS["note"], fontweight="bold", color=R.MID)
        info = float(u_end[xs > 0.3].max())
    arrow(fig, axes[0], axes[1], "graft")
    arrow(fig, axes[1], axes[2], r"$t\to\infty$")
    return info


def main():
    from matplotlib import font_manager
    names = {f.name for f in font_manager.fontManager.ttflist}
    font = next((n for n in ("Arial", "Liberation Sans") if n in names), "DejaVu Sans")
    plt.rcParams.update({"font.family": font, "pdf.fonttype": 42})

    fig = plt.figure(figsize=(FIG_W / 2.54, FIG_H / 2.54), facecolor=R.PAPER)
    near = row(fig, MB + PH + RGAP, X_NEAR, "graft close to the head", drift=False)
    far = row(fig, MB, X_FAR, "graft further away", drift=True)
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"graft_drift.{ext}", facecolor=R.PAPER, dpi=300)
    print("near: max u away from head =", round(near, 5), "| far: new peak at x/L =",
          round(float(far), 4))


if __name__ == "__main__":
    main()
