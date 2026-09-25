"""Schematic of the classical Hydra grafting experiment (poster subsection 2.5).

Three upright hydras in one row: donor (piece of hypostome marked) and host; a curved
arrow carries the piece into the middle of the host body column; a block arrow leads to
the host with an induced secondary axis at the graft site.
No labels.

Run from the poster2 folder:  python scripts/graft_schematic.py
Output: generated/graft_schematic.{pdf,png}
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrow, FancyArrowPatch, Polygon

OUT = Path(__file__).resolve().parent.parent / "generated"
OUT.mkdir(exist_ok=True)

PAPER, INK = "#F4F6F5", "#1E2A30"
BODY = "#D6DADC"          # neutral grey tissue
GRAFT = "#D0703C"         # poster copper = head (organizer) tissue
FIG_W, FIG_H = 15.6, 6.6  # cm, 1:1 on the poster
LW = 1.4                  # outline width


def rot(pts, ang, origin):
    c, s = np.cos(ang), np.sin(ang)
    R = np.array([[c, -s], [s, c]])
    return (np.atleast_2d(pts) - origin) @ R.T + origin


def body_local(h, w, foot=True):
    """Body outline in local coordinates: foot at (0,0), head at (0,h)."""
    t = np.linspace(0, 1, 80)
    half = (0.05 + 0.065 * np.sin(np.pi * t ** 0.85) ** 1.1 + 0.02 * t ** 3) * w
    if not foot:
        half[:10] = half[10]
    ys = t * h
    right = np.column_stack([half, ys])
    left = np.column_stack([-half[::-1], ys[::-1]])
    a = np.linspace(0, np.pi, 20)
    dome = np.column_stack([half[-1] * np.cos(a), h + 0.05 * w * np.sin(a)])
    return np.vstack([right, dome[1:-1], left])


def tentacle_local(p0, direction, length, wave, phase):
    s = np.linspace(0, 1, 40)
    d = np.asarray(direction, float)
    d = d / np.linalg.norm(d)
    n = np.array([-d[1], d[0]])
    return (np.asarray(p0) + np.outer(s * length, d)
            + np.outer(wave * length * np.sin(2.2 * np.pi * s + phase) * s, n))


def stroke(ax, pts, lw, z=2):
    ax.plot(pts[:, 0], pts[:, 1], color=INK, lw=lw + 2 * LW, solid_capstyle="round", zorder=z)
    ax.plot(pts[:, 0], pts[:, 1], color=BODY, lw=lw, solid_capstyle="round", zorder=z + 1)


TENT = [(-0.9, 0.8), (-0.45, 1.0), (0.05, 1.0), (0.5, 1.0), (0.9, 0.8)]


class Hydra:
    """A Hydra with its foot at `foot`, pointing in direction `ang` (0 = up, +90 deg = left)."""

    def __init__(self, foot, h, ang_deg):
        self.foot = np.asarray(foot, float)
        self.h = h
        self.ang = np.deg2rad(ang_deg)

    def to_world(self, pts):
        return rot(np.asarray(pts) + self.foot, self.ang, self.foot)

    def at(self, s, side=0.0):
        """World point at fraction s of the body length, side offset in units of h."""
        return self.to_world([[side * self.h, s * self.h]])[0]

    def draw(self, ax, tent_len=0.2, width=0.5):
        h = self.h
        head = np.array([0.0, h + 0.01 * h])
        for i, d in enumerate(TENT):
            stroke(ax, self.to_world(tentacle_local(head, d, tent_len * h, 0.06, i * 1.3)), 3.0)
        ax.add_patch(Polygon(self.to_world(body_local(h, width * h)), closed=True, fc=BODY, ec=INK,
                             lw=LW, zorder=4))

    def secondary_axis(self, ax, s, side_sign):
        """Induced axis leaving the body at fraction s; side_sign selects the flank."""
        h = self.h
        L = 0.22 * h
        base_local = np.array([side_sign * 0.06 * h, s * h])
        a_loc = -side_sign * np.deg2rad(62)            # tilted towards the head
        shape = body_local(L + 0.05 * h, 0.45 * h, foot=False) + base_local - [0, 0.05 * h]
        local = rot(shape, a_loc, base_local)
        head_l = rot([base_local + [0, L]], a_loc, base_local)[0]
        for i, d in enumerate([(-1.0, 0.5), (-0.3, 1.0), (0.4, 1.0), (1.0, 0.45)]):
            dd = rot([d], a_loc, np.zeros(2))[0]
            stroke(ax, self.to_world(tentacle_local(head_l, dd, 0.13 * h, 0.05, i)), 2.5)
        ax.add_patch(Polygon(self.to_world(local), closed=True, fc=BODY, ec=INK, lw=LW,
                             zorder=3.5))


def main():
    fig = plt.figure(figsize=(FIG_W / 2.54, FIG_H / 2.54), facecolor=PAPER)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, FIG_W)
    ax.set_ylim(0, FIG_H)
    ax.set_aspect("equal")
    ax.axis("off")

    h, y0 = 4.4, 0.35
    # upright hydras in one row: donor, host  ->  host with secondary axis
    donor = Hydra((1.9, y0), h, 0)
    host = Hydra((5.6, y0), h, 0)
    donor.draw(ax, tent_len=0.3, width=0.85)
    host.draw(ax, tent_len=0.3, width=0.85)

    piece = donor.at(0.99)
    ax.add_patch(Circle(piece, 0.065 * h, fc=GRAFT, ec=INK, lw=LW, zorder=6))
    g = host.at(0.5, side=0.11)                     # right flank, middle of the column
    ax.add_patch(Circle(g, 0.065 * h, fc=GRAFT, ec=INK, lw=LW, zorder=6))
    ax.add_patch(FancyArrowPatch(piece + [0.3, 0.05], g + [0.05, 0.4],
                                 connectionstyle="arc3,rad=-0.45",
                                 arrowstyle="simple,head_width=0.8,head_length=0.7,tail_width=0.28",
                                 mutation_scale=14, fc="white", ec=INK, lw=LW, zorder=7))

    # block arrow: induction
    ya = y0 + 0.5 * h
    ax.add_patch(FancyArrow(7.6, ya, 2.6, 0, width=0.7, head_width=1.4, head_length=0.9,
                            length_includes_head=True, fc="white", ec=INK, lw=LW, zorder=5))

    # host with the induced secondary axis at the graft site (right flank)
    res = Hydra((12.2, y0), h, 0)
    res.draw(ax, tent_len=0.3, width=0.85)
    res.secondary_axis(ax, 0.5, side_sign=1)

    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"graft_schematic.{ext}", facecolor=PAPER, dpi=300)


if __name__ == "__main__":
    main()
