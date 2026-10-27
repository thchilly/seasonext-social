"""Photo version of the Aposelemis figure (27 Oct 2026).

A photograph of the reservoir fills the top of the square; a navy gradient
rises from the bottom so the title and the four storage values read in white.
OAK announcements up to 8 Oct; 26 Oct from a press report (creta24).

Run from the repository root: python3 <this folder>/figure.py
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from matplotlib.patches import Rectangle

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "scripts"))
import brand  # noqa: E402

PHOTO = HERE / "photo.webp"
FULL = 17.58 / 0.70  # about 25 million m3
# (date, million m3, value label, from an OAK announcement)
STORAGE = [
    ("30 Sep", 9.26, "9.3", True),
    ("4 Oct", 12.7, "12.7", True),
    ("8 Oct", 17.58, "17.6", True),
    ("26 Oct", 20.6, "20.6", False),
]
WHITE = "#ffffff"
SOFT = "#c9d1df"  # light text on navy


def background():
    """Photo scaled to cover the top, with navy gradients top and bottom (RGB array)."""
    n = brand.SIZE_PX
    img = Image.open(PHOTO).convert("RGB")
    h = int(n * 0.70)
    w = round(img.width * h / img.height)
    img = img.resize((w, h), Image.LANCZOS)
    x0 = (w - n) // 2 + 40  # keep the church and the houses in frame
    img = img.crop((x0, 0, x0 + n, h))
    out = np.empty((n, n, 3))
    navy = np.array([int(brand.NAVY[i:i + 2], 16) for i in (1, 3, 5)]) / 255
    out[:] = navy
    out[:h] = np.asarray(img) / 255
    y = np.arange(n)[:, None, None] / n
    # Bottom: transparent at 40 % of the height, solid navy by 70 %.
    a = np.clip((y - 0.40) / 0.30, 0, 1) ** 1.3
    # Top: a light veil behind the masthead.
    a = np.maximum(a, 0.55 * np.clip(1 - y / 0.16, 0, 1))
    return out * (1 - a) + navy * a


def light_logo():
    """The logo for a dark background: lettering white, blue parts lightened."""
    img = plt.imread(str(brand.LOGO)).copy()
    rgb = img[..., :3]
    blue = (rgb.max(axis=2) - rgb.min(axis=2)) > 0.15
    light = np.array([int(brand.BLUE_LIGHT[i:i + 2], 16) for i in (1, 3, 5)]) / 255
    rgb[blue] = light
    rgb[~blue] = 1.0
    return img


def main():
    brand.setup()
    fig = brand.canvas()
    fig.add_axes([0, 0, 1, 1]).imshow(background(), aspect="auto", interpolation="lanczos")
    fig.axes[0].axis("off")

    L, R = brand.LEFT, brand.RIGHT
    fig.add_artist(plt.Line2D([L, R], [0.955, 0.955], color=WHITE, lw=1.4))
    fig.text(L, 0.938, "EVENT IN CONTEXT", color=WHITE, fontsize=7.5, fontweight="semibold", va="top")
    logo = light_logo()
    box = OffsetImage(logo, zoom=0.22 * brand.SIZE_PX / logo.shape[1] / (brand.DPI / 72),
                      interpolation="lanczos", resample=True)
    fig.add_artist(AnnotationBbox(box, (R, 0.943), xycoords="figure fraction",
                                  box_alignment=(1, 1), frameon=False))

    fig.text(L, 0.540, "How the storm nearly\nrefilled Aposelemis", color=WHITE, fontsize=21,
             fontweight="semibold", fontfamily=brand.SERIF, va="top", linespacing=1.0)
    fig.text(L, 0.382, "Water stored in the reservoir that supplies Heraklion, after the storm of\n"
             "30 September to 4 October 2026. Million cubic metres; full is about 25.",
             color=SOFT, fontsize=8.5, va="top", linespacing=1.3)

    # Four columns: value, date, and a gauge filled to the share of capacity.
    cw = (R - L) / 4
    for i, (day, v, label, oak) in enumerate(STORAGE):
        x = L + i * cw
        fig.text(x, 0.245, label, color=WHITE, fontsize=22, fontweight="semibold",
                 fontfamily=brand.SERIF, va="baseline")
        share = f"{v / FULL * 100:.0f}% full"
        fig.text(x, 0.205, f"{day}  ·  {share}", color=SOFT, fontsize=8, va="top")
        gw, gy, gh = cw - 0.03, 0.150, 0.016
        fig.add_artist(Rectangle((x, gy), gw, gh, transform=fig.transFigure, lw=0.8,
                                 edgecolor=brand.BLUE_LIGHT, facecolor="none"))
        fig.add_artist(Rectangle((x, gy), gw * v / FULL, gh, transform=fig.transFigure, lw=0,
                                 facecolor=brand.BLUE_MID if oak else "none",
                                 hatch=None if oak else "////", edgecolor=brand.BLUE_MID))

    fig.text(L, 0.118, "Values from OAK announcements; 26 Oct (hatched) from a press report.",
             color=SOFT, fontsize=7, va="top")
    fig.add_artist(plt.Line2D([L, R], [0.06, 0.06], color="#3a4458", lw=0.8))
    fig.text(L, 0.049,
             "Data: Crete Development Organisation (OAK) via politica.gr, neakriti and LatoNews; 26 Oct: creta24.\n"
             "Full level derived from OAK's 70% on 8 Oct. Photo: Sfendyli, Aposelemis reservoir, 25 Oct 2026, Konstantinos Frantzeskakis.",
             color="#8f99ab", fontsize=5.4, va="top", linespacing=1.2)
    print(brand.save(fig, HERE / "image.png"))


if __name__ == "__main__":
    main()
