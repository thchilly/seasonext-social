"""Figure for the terciles explainer (planned 5 Nov 2026).

Schematic in the style of the Forecast vs reality figures: the 24 Septembers of
1993-2016 as dots placed by rank, 8 in each third, so the thirds have equal width.
Top: a forecast with no information (33/33/33). Bottom: the published forecast
for September 2026 from early August (19/32/49, posted on 13 Oct). The tercile
edges (9 and 22 mm) are the ERA5 values shown in that post.

Run from the repository root: python3 <this folder>/figure.py
"""

import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "scripts"))  # <root>/scripts
import brand  # noqa: E402

LABELS = ("drier than normal", "near normal", "wetter than normal")
TINTS = (brand.WARM, brand.INK_3, brand.BLUE)
EDGES_MM = (9, 22)
BLOCKS = [
    ("With no information", "Each third holds 8 of the 24 past Septembers, so each has a 1 in 3 chance.",
     (1 / 3, 1 / 3, 1 / 3)),
    ("A forecast that leans wet", "September 2026, forecast in early August: the odds shift towards the wet third.",
     (0.19, 0.32, 0.49)),
]


def band(fig, rect, probs):
    ax = fig.add_axes(rect)
    edges = [0, 1 / 3, 2 / 3, 1]
    for i in range(3):
        ax.axvspan(edges[i], edges[i + 1], color=TINTS[i], alpha=0.06 + 0.42 * probs[i], lw=0)
        mid = 0.5 * (edges[i] + edges[i + 1])
        ax.text(mid, 1.36, f"{probs[i] * 100:.0f}%", ha="center", va="bottom", fontsize=16,
                fontweight="semibold", color=brand.NAVY, fontfamily=brand.SERIF)
        ax.text(mid, 1.14, LABELS[i], ha="center", va="bottom", fontsize=7.5, color=brand.INK_2)
    for e, v in zip(edges[1:3], EDGES_MM):
        ax.axvline(e, color=brand.PAPER, lw=2)
        ax.text(e, -0.12, f"{v} mm", ha="center", va="top", fontsize=7, color=brand.INK_3)
    ranks = (np.arange(24) + 0.5) / 24
    ax.scatter(ranks, np.full(24, 0.5), s=16, color=brand.INK_3, lw=0, zorder=3)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")


def main():
    brand.setup()
    fig = brand.canvas()
    top = brand.header(
        fig,
        "Did you know?",
        "What a 49% chance of a wet month means",
        "Forecasts use three equal thirds of the past. Grey dots: the Septembers\n"
        "of 1993-2016 in Crete, ranked by rainfall, 8 in each third.",
    )
    for i, (title, line, probs) in enumerate(BLOCKS):
        bt = top - 0.005 - i * 0.28
        fig.text(0.06, bt, title, fontsize=13, fontweight="semibold", color=brand.NAVY,
                 fontfamily=brand.SERIF, va="top")
        fig.text(0.06, bt - 0.05, line, fontsize=8.5, color=brand.INK_2, va="top")
        band(fig, [0.06, bt - 0.225, 0.88, 0.065], probs)

    fig.text(0.06, 0.142, "A 49% chance of wet still leaves 51% for near normal or dry.\n"
             "Only a score kept over many months shows whether such odds can be trusted.",
             fontsize=8.8, fontweight="semibold", color=brand.NAVY, va="top", linespacing=1.25)
    brand.footer(
        fig,
        "Forecast: mean of 10 C3S seasonal systems started 1 August 2026 (Forecast vs reality, September 2026). "
        "Thirds: ERA5, Crete, 1993-2016.\nContains modified Copernicus Climate Change Service information 2026.",
    )
    print(brand.save(fig, HERE / "image.png"))


if __name__ == "__main__":
    main()
