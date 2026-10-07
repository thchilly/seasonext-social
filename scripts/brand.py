"""SEASONEXT look for social media figures: colours, fonts, canvas, header, footer.

Every post figure is a 1350 x 1350 px square (works on LinkedIn, X and Bluesky
feeds) on warm off-white paper, laid out like a journal page:

- a masthead: a navy rule, the series name on the left, the logo on the right;
- a serif title and a short sans-serif subtitle;
- the content;
- a compact footer with the data credits.

Typefaces (brand/fonts/): Source Serif 4 for titles and headline numbers, Barlow
(a DIN-style face close to the logo lettering) for labels, data and credits.
"""

import textwrap
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.offsetbox import AnnotationBbox, OffsetImage

ROOT = Path(__file__).resolve().parents[1]  # repository root
BRAND_DIR = ROOT / "brand"
LOGO = BRAND_DIR / "logo" / "seasonext_logo.png"
EMBLEM = BRAND_DIR / "logo" / "seasonext_emblem.png"

# Sampled from the SEASONEXT logo.
NAVY = "#151d2c"
BLUE = "#4d71b1"
BLUE_MID = "#7994c4"
BLUE_LIGHT = "#a5b6d7"
BLUE_PALE = "#d0d9e9"
# Supporting colours (not in the logo).
WARM = "#c0703f"  # dry / warm pole, opposite of BLUE
WARM_PALE = "#ecd2bf"
INK_2 = "#4a5262"  # secondary text
INK_3 = "#8a909c"  # muted text, past-year dots
RULE = "#dcd8cf"  # hairlines, tuned to the paper
PAPER = "#faf8f3"  # warm off-white

SERIF = "Source Serif 4"
SANS = "Barlow"

DPI = 270  # 5 x 5 inch canvas
SIZE_PX = 5 * DPI  # 1350 px
LEFT, RIGHT = 0.06, 0.94


def setup():
    """Register the brand fonts and set matplotlib defaults (sans by default)."""
    for f in sorted((BRAND_DIR / "fonts").glob("*.[ot]tf")):
        font_manager.fontManager.addfont(str(f))
    plt.rcParams.update(
        {
            "font.family": SANS,
            "font.size": 10,
            "text.color": NAVY,
            "axes.edgecolor": RULE,
            "axes.labelcolor": INK_2,
            "axes.linewidth": 0.6,
            "xtick.color": INK_2,
            "ytick.color": INK_2,
            "xtick.major.width": 0.6,
            "ytick.major.width": 0.6,
            "figure.facecolor": PAPER,
            "axes.facecolor": PAPER,
            "savefig.facecolor": PAPER,
        }
    )


def canvas():
    """A blank square figure in brand defaults."""
    size = SIZE_PX / DPI
    return plt.figure(figsize=(size, size), dpi=DPI)


def header(fig, series, title, subtitle=None, wrap=38, size=19, sub_wrap=80):
    """Masthead (rule, series name, logo), serif title, optional subtitle.

    Returns the figure y just below the header, so content can start there.
    """
    fig.add_artist(plt.Line2D([LEFT, RIGHT], [0.955, 0.955], color=NAVY, lw=1.4))
    fig.text(LEFT, 0.938, series.upper(), color=BLUE, fontsize=7.5, fontweight="semibold",
             va="top", fontfamily=SANS)
    if LOGO.exists():
        img = plt.imread(str(LOGO))
        # About 22 % of the canvas width, resampled smoothly.
        box = OffsetImage(img, zoom=0.22 * SIZE_PX / img.shape[1] / (DPI / 72),
                          interpolation="lanczos", resample=True)
        fig.add_artist(AnnotationBbox(box, (RIGHT, 0.943), xycoords="figure fraction",
                                      box_alignment=(1, 1), frameon=False))

    lines = textwrap.wrap(title, wrap)
    t = fig.text(LEFT, 0.875, "\n".join(lines), color=NAVY, fontsize=size, fontweight="semibold",
                 va="top", fontfamily=SERIF, linespacing=1.0)
    # Shrink the title a little if it runs past the right margin.
    while _right(fig, t) > RIGHT and t.get_fontsize() > 15:
        t.set_fontsize(t.get_fontsize() - 0.5)
    y = _bottom(fig, t) - 0.022
    if subtitle:
        subtitle = "\n".join(textwrap.wrap(subtitle, sub_wrap)) if "\n" not in subtitle else subtitle
        t = fig.text(LEFT, y, subtitle, color=INK_2, fontsize=9.5, va="top", linespacing=1.25,
                     fontfamily=SANS)
        y = _bottom(fig, t) - 0.01
    return y


def _right(fig, text):
    """Figure-fraction x of the right edge of a text artist, as rendered."""
    box = text.get_window_extent(renderer=fig.canvas.get_renderer())
    return box.x1 / fig.bbox.width


def _bottom(fig, text):
    """Figure-fraction y of the lowest point of a text artist, as rendered."""
    box = text.get_window_extent(renderer=fig.canvas.get_renderer())
    return box.y0 / fig.bbox.height


def footer(fig, credit):
    """Hairline and data credits across the full width, at most two lines."""
    fig.add_artist(plt.Line2D([LEFT, RIGHT], [0.06, 0.06], color=RULE, lw=0.8))
    fig.text(LEFT, 0.049, credit, color=INK_3, fontsize=5.4, va="top", linespacing=1.2,
             fontfamily=SANS)


def save(fig, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=DPI)
    plt.close(fig)
    return path
