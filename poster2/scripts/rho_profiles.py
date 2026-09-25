"""Figures for poster subsection 3.2 (prescribed source density rho(x)).

1) generated/hydra_rho.{pdf,png}
   Hydra (line art extracted from assets/hydra_rho_source.png, recoloured to poster ink)
   next to the source gradient rho(x), x = 0 (foot) ... L (head).
2) generated/rho_profiles.{pdf,png}
   Two grafted configurations (Livshits et al. style cylinders, U = upper, L = lower
   body-column piece, arrow = original polarity) and the resulting rho(x):
     drawn horizontally: x = 0 (foot, left) ... L (head, right)
     oriented       L | U : rho increases monotonically
     anti-oriented  U | L : rho increases, drops at the junction, increases again

Everything that is likely to be tweaked is collected in the CONFIG block below.
Run from the poster2 folder:  python scripts/rho_profiles.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse, FancyArrowPatch, Polygon, Rectangle
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "generated"
OUT.mkdir(exist_ok=True)

# ================================================================ CONFIG
PAPER, INK, MID, RULE = "#F4F6F5", "#1E2A30", "#66747A", "#CFD8DA"
RHO = "#7B4FA0"                      # poster colour of rho
U_COL, L_COL = "#E632E6", "#3FD23F"  # upper / lower tissue (Livshits colours)

RHO_MIN, RHO_MAX = 0.2, 1.0          # oriented profile: rho(0) -> rho(L)


def rho_oriented(x):
    """x in [0, 1] (foot -> head)."""
    return RHO_MIN + (RHO_MAX - RHO_MIN) * x


def rho_anti(x):
    """L piece on top of U piece: each piece keeps its own (rising) rho values."""
    mid = 0.5 * (RHO_MIN + RHO_MAX)
    lower_half = mid + (RHO_MAX - mid) * (x / 0.5)            # U piece at the bottom
    upper_half = RHO_MIN + (mid - RHO_MIN) * ((x - 0.5) / 0.5)  # L piece on top
    return np.where(x < 0.5, lower_half, upper_half)


FS = dict(tick=15, label=17, title=16)
HYDRA_FIG = (17.0, 5.0)              # cm (width, height), 1:1 on the poster
HYDRA_STRETCH = 3.8                  # horizontal stretch of the hydra drawing (1 = true shape)
PROFILE_FIG = (38.0, 4.4)            # cm
# ================================================================


def setup_fonts():
    from matplotlib import font_manager
    names = {f.name for f in font_manager.fontManager.ttflist}
    font = next((n for n in ("Arial", "Liberation Sans") if n in names), "DejaVu Sans")
    plt.rcParams.update({"font.family": font, "pdf.fonttype": 42, "mathtext.fontset": "cm"})


def hydra_rgba():
    """Line art from the source image: brightness -> opacity of poster ink."""
    src = np.array(Image.open(ROOT / "assets" / "hydra_rho_source.png").convert("L"), float)
    crop = src[100:1310, 25:545] / 255.0
    alpha = np.clip((crop - 0.06) / 0.6, 0, 1) ** 0.8
    ink = np.array([int(INK[i:i + 2], 16) for i in (1, 3, 5)]) / 255.0
    rgba = np.zeros(crop.shape + (4,))
    rgba[..., :3] = ink
    rgba[..., 3] = alpha
    return rgba


def style_vertical(ax, xmax=1.0):
    ax.set_facecolor(PAPER)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    for sp in ("left", "bottom"):
        ax.spines[sp].set_color(INK)
    ax.set_xlim(0, 1.12)
    ax.set_ylim(0, xmax)
    ax.set_xticks([])
    ax.set_yticks([0, xmax])
    ax.set_yticklabels(["0", "L"])
    ax.tick_params(labelsize=FS["tick"], colors=INK, length=3)
    ax.set_ylabel("x", color=INK, fontsize=FS["label"], rotation=0, labelpad=8, va="center")
    ax.set_xlabel(r"$\rho(x)$", color=RHO, fontsize=FS["label"], labelpad=2)


def fill_profile(ax, x, r):
    ax.fill_betweenx(x, 0, r, color=RHO, alpha=0.28, lw=0)
    ax.plot(r, x, color=RHO, lw=2.4)


def figure_hydra():
    """Horizontal hydra (foot left, head right) with rho(x) drawn above it."""
    _, H = HYDRA_FIG
    img = np.rot90(hydra_rgba(), k=-1)               # head now points to the right
    n_rows, n_cols = img.shape[:2]
    c_foot, c_head = 1210 - 1190, 1210 - 420          # columns of foot / hypostome
    h_img = 2.1                                       # cm
    w_img = h_img * n_cols / n_rows * HYDRA_STRETCH
    left = 2.0
    W = left + w_img + 0.2
    fig = plt.figure(figsize=(W / 2.54, H / 2.54), facecolor=PAPER)
    axh = fig.add_axes([left / W, 0.05 / H, w_img / W, h_img / H])
    axh.imshow(img, interpolation="lanczos", aspect="auto")
    axh.axis("off")
    # rho plot above, aligned with foot (x = 0) and hypostome (x = L)
    xf = left + w_img * c_foot / n_cols
    xh = left + w_img * c_head / n_cols
    axr = fig.add_axes([xf / W, (h_img + 0.3) / H, (xh - xf) / W, (H - h_img - 0.45) / H])
    axr.set_facecolor(PAPER)
    for sp in ("top", "right"):
        axr.spines[sp].set_visible(False)
    for sp in ("left", "bottom"):
        axr.spines[sp].set_color(INK)
    x = np.linspace(0, 1, 400)
    r = rho_oriented(x)
    axr.fill_between(x, 0, r, color=RHO, alpha=0.28, lw=0)
    axr.plot(x, r, color=RHO, lw=2.4)
    axr.set_xlim(0, 1)
    axr.set_ylim(0, 1.1)
    axr.set_yticks([])
    axr.set_xticks([])
    axr.tick_params(labelsize=FS["tick"], colors=INK, length=3, pad=1)
    axr.set_ylabel(r"$\rho(x)$", color=RHO, fontsize=FS["label"], rotation=0,
                   labelpad=30, va="center")
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"hydra_rho.{ext}", facecolor=PAPER, dpi=300)


def cylinder_h(ax, x0, yc, w, h, col, letter):
    """Cylinder lying horizontally (axis along x), left end at x0."""
    ax.add_patch(Ellipse((x0, yc), 0.28 * h, h, fc=col, ec=INK, lw=1.2, zorder=1))
    ax.add_patch(Rectangle((x0, yc - h / 2), w, h, fc=col, ec=INK, lw=1.2, zorder=2))
    ax.add_patch(Ellipse((x0 + w, yc), 0.28 * h, h, fc=col, ec=INK, lw=1.2, zorder=3))
    ax.text(x0 + w / 2, yc, letter, ha="center", va="center", fontsize=15,
            fontweight="bold", color="white", zorder=4)


def graft_icon_h(ax, left, right):
    """Two pieces side by side (foot on the left, head on the right), polarity arrows."""
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    w, h = 0.40, 0.46
    for i, (col, let) in enumerate((left, right)):
        x0 = 0.08 + i * 0.46
        cylinder_h(ax, x0, 0.62, w, h, col, let)
        ax.add_patch(FancyArrowPatch((x0, 0.14), (x0 + w, 0.14), arrowstyle="-|>",
                                     mutation_scale=11, lw=1.5, color=INK))


def style_horizontal(ax):
    ax.set_facecolor(PAPER)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    for sp in ("left", "bottom"):
        ax.spines[sp].set_color(INK)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.1)
    ax.set_yticks([])
    ax.set_xticks([])
    ax.set_ylabel(r"$\rho$", color=RHO, fontsize=FS["label"], rotation=0, labelpad=10,
                  va="center")


def figure_profiles():
    W, H = PROFILE_FIG
    fig = plt.figure(figsize=(W / 2.54, H / 2.54), facecolor=PAPER)
    x = np.linspace(0, 1, 800)
    # (title, left piece, right piece, profile); x = 0 foot (left) ... L head (right)
    cases = [("oriented", (L_COL, "L"), (U_COL, "U"), rho_oriented(x)),
             ("anti-oriented", (U_COL, "U"), (L_COL, "L"), rho_anti(x))]
    panel_w = W / 2
    y0, ph = 0.75, H - 1.55
    for i, (title, left, right, r) in enumerate(cases):
        x0 = i * panel_w
        fig.text((x0 + 0.2) / W, (H - 0.35) / H, title, fontsize=FS["title"],
                 fontweight="bold", color="#123B4A", ha="left", va="center")
        axi = fig.add_axes([(x0 + 0.2) / W, y0 / H, 4.6 / W, ph / H])
        graft_icon_h(axi, left, right)
        axp = fig.add_axes([(x0 + 5.8) / W, y0 / H, (panel_w - 6.6) / W, ph / H])
        style_horizontal(axp)
        axp.axvline(0.5, color=MID, lw=1.2, ls=(0, (4, 3)))
        axp.fill_between(x, 0, r, color=RHO, alpha=0.28, lw=0)
        axp.plot(x, r, color=RHO, lw=2.4)
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"rho_profiles.{ext}", facecolor=PAPER, dpi=300)


if __name__ == "__main__":
    setup_fonts()
    figure_hydra()
    figure_profiles()
    print("written: generated/hydra_rho.*, generated/rho_profiles.*")
