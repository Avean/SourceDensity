"""Prepare poster assets so they sit on the poster background.

- livshits_h2f_experiment.png : white background -> transparent (colour-to-alpha)
- heidelberg_logo.png         : black text/line -> white, for the dark petrol header
- tursch_cut_tied.png         : white background -> poster paper colour, soft fade at edges
- steichele2024_control_regeneration.jpg, kadu2012_grafting.jpg
                              : white gaps / frames -> poster paper colour

Run from the poster2 folder:  python scripts/process_assets.py
"""
from pathlib import Path

import numpy as np
from PIL import Image

ASSETS = Path(__file__).resolve().parent.parent / "assets"


def white_to_alpha(rgba: np.ndarray) -> np.ndarray:
    """GIMP-style colour-to-alpha for white: keeps anti-aliasing clean."""
    rgb = rgba[..., :3].astype(float) / 255.0
    a0 = rgba[..., 3].astype(float) / 255.0
    alpha = (1.0 - rgb).max(axis=-1)                      # distance from white
    safe = np.where(alpha > 0, alpha, 1.0)[..., None]
    col = (rgb - (1.0 - alpha)[..., None]) / safe          # un-premultiply
    out = np.empty_like(rgba)
    out[..., :3] = np.clip(col * 255 + 0.5, 0, 255).astype(np.uint8)
    out[..., 3] = np.clip(alpha * a0 * 255 + 0.5, 0, 255).astype(np.uint8)
    return out


def neutral_to_white(rgba: np.ndarray, sat_max: float = 0.12) -> np.ndarray:
    """Recolour neutral (grey/black) pixels to white, keep saturated ones (the seal)."""
    rgb = rgba[..., :3].astype(float) / 255.0
    mx, mn = rgb.max(axis=-1), rgb.min(axis=-1)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    neutral = (sat < sat_max) & (rgba[..., 3] > 0)
    out = rgba.copy()
    out[neutral, :3] = 255
    return out


PAPER = np.array([0xF4, 0xF6, 0xF5], dtype=float) / 255.0


def to_paper(rgba: np.ndarray, feather: int = 14) -> np.ndarray:
    """Multiply-blend onto the poster paper colour (white -> paper) and fade light
    pixels near the border smoothly into paper, so the figure has no visible edge."""
    rgb = rgba[..., :3].astype(float) / 255.0
    a = rgba[..., 3:4].astype(float) / 255.0
    rgb = rgb * a + (1.0 - a)                     # flatten any transparency onto white
    rgb = rgb * PAPER                             # white becomes paper, content ~unchanged
    h, w = rgb.shape[:2]
    y, x = np.mgrid[0:h, 0:w]
    d = np.minimum.reduce([x, y, w - 1 - x, h - 1 - y]).astype(float)
    t = np.clip(d / feather, 0, 1)
    fade = (t * t * (3 - 2 * t))[..., None]       # smoothstep 0 at edge -> 1 inside
    light = np.clip((rgb.mean(axis=-1, keepdims=True) - 0.55) / 0.3, 0, 1)
    k = 1 - (1 - fade) * light                    # only fade light (background) pixels
    rgb = rgb * k + PAPER * (1 - k)
    out = np.empty((h, w, 4), dtype=np.uint8)
    out[..., :3] = np.clip(rgb * 255 + 0.5, 0, 255).astype(np.uint8)
    out[..., 3] = 255
    return out


def main() -> None:
    liv = np.array(Image.open(ASSETS / "livshits_h2f_experiment.png").convert("RGBA"))
    liv_t = Image.fromarray(white_to_alpha(liv))
    liv_t = liv_t.crop(liv_t.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox())
    liv_t.save(ASSETS / "livshits_h2f_experiment_transparent.png")

    logo = np.array(Image.open(ASSETS / "heidelberg_logo.png").convert("RGBA"))
    Image.fromarray(neutral_to_white(logo)).save(ASSETS / "heidelberg_logo_white.png")

    cut = np.array(Image.open(ASSETS / "tursch_cut_tied.png").convert("RGBA"))
    Image.fromarray(to_paper(cut)).save(ASSETS / "tursch_cut_tied_paper.png")

    for name in ("steichele2024_control_regeneration", "kadu2012_grafting"):
        im = np.array(Image.open(ASSETS / f"{name}.jpg").convert("RGBA"))
        Image.fromarray(to_paper(im, feather=4)).save(ASSETS / f"{name}_paper.png")


if __name__ == "__main__":
    main()
