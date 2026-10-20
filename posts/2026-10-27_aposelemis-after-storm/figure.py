"""Figure for the Aposelemis reservoir post (planned 27 Oct 2026).

Water stored in the Aposelemis reservoir after the storm of 30 September to
4 October 2026, as announced by the Crete Development Organisation (OAK) and
reported in the press. The full line (about 25 million m3) follows from OAK's
70 % at 17.58 million m3 on 8 October.

Run from the repository root: python3 <this folder>/figure.py
"""

import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "scripts"))  # <root>/scripts
import brand  # noqa: E402

# (date, million m3, label, from an OAK announcement)
STORAGE = [
    (date(2026, 9, 30), 9.26, "9.3", True),
    (date(2026, 10, 4), 12.7, "12.7", True),
    (date(2026, 10, 8), 17.58, "17.6 (70%)", True),
    (date(2026, 10, 16), 20.3, "over 20.3 (over 85%)", False),
]
FULL = 17.58 / 0.70  # about 25 million m3
STORM = (date(2026, 9, 30), date(2026, 10, 4))


def main():
    brand.setup()
    fig = brand.canvas()
    top = brand.header(
        fig,
        "Event in context",
        "Two weeks that nearly refilled Aposelemis",
        "Water stored in the Aposelemis reservoir, which supplies Heraklion,\n"
        "after the storm of 30 September to 4 October 2026. Million cubic metres.",
    )

    d0 = STORAGE[0][0]
    day = lambda d: (d - d0).days  # noqa: E731
    ax = fig.add_axes([0.10, 0.17, 0.80, top - 0.21])
    ax.axvspan(day(STORM[0]), day(STORM[1]), color=brand.BLUE_PALE, lw=0, zorder=0)
    ax.text((day(STORM[0]) + day(STORM[1])) / 2, 1.0, "storm\n30 Sep to 4 Oct",
            ha="center", va="bottom", fontsize=8, color=brand.BLUE)

    ax.axhline(FULL, color=brand.INK_3, lw=0.8, ls=(0, (4, 3)))
    ax.text(day(STORAGE[-1][0]) + 0.6, FULL + 0.4, "full: about 25", ha="right", va="bottom",
            fontsize=8.5, color=brand.INK_2)

    xs = [day(d) for d, *_ in STORAGE]
    ys = [v for _, v, *_ in STORAGE]
    ax.plot(xs[:3], ys[:3], color=brand.NAVY, lw=1.6, zorder=2)
    ax.plot(xs[2:], ys[2:], color=brand.NAVY, lw=1.2, ls=(0, (2, 2)), zorder=2)
    for x, (d, v, label, oak) in zip(xs, STORAGE):
        ax.scatter([x], [v], s=55, zorder=3, lw=1.5,
                   color=brand.NAVY if oak else brand.PAPER, edgecolor=brand.NAVY)
        last = x == xs[-1]
        ax.annotate(label, (x, v), xytext=(6 if last else 0, 10), textcoords="offset points",
                    ha="right" if last else "center",
                    va="bottom", fontsize=10, fontweight="semibold", color=brand.NAVY,
                    fontfamily=brand.SERIF)

    ax.set_xlim(-1.2, day(STORAGE[-1][0]) + 1.2)
    ax.set_ylim(0, 28)
    ax.set_xticks(xs)
    ax.set_xticklabels([d.strftime("%-d %b") for d, *_ in STORAGE], fontsize=9)
    ax.set_yticks([0, 5, 10, 15, 20, 25])
    ax.tick_params(axis="y", labelsize=8.5, length=0)
    ax.tick_params(axis="x", length=3)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)

    fig.text(0.10, 0.115, "Filled dots: OAK announcements. Open dot: press report (neakriti, 16 Oct).",
             fontsize=7.5, color=brand.INK_2, va="top")
    brand.footer(
        fig,
        "Data: Crete Development Organisation (OAK) announcements via politica.gr (4 Oct), neakriti (4 Oct) and LatoNews (8 Oct);\n"
        "16 Oct: neakriti. Full level derived from OAK's 70% on 8 Oct. Storage values are as announced, not independently measured.",
    )
    print(brand.save(fig, HERE / "image.png"))


if __name__ == "__main__":
    main()
