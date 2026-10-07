"""SEASONEXT look for social media figures: colours, fonts, canvas, header, footer.

Every post figure is a 1080 x 1080 px square (works on LinkedIn, X and Bluesky
feeds) built on the same canvas: a small kicker line, a title, an optional
subtitle, the content, and a footer with the data credit and the logo.

Brand assets live in brand/: the official logo and emblem (brand/logo/) and
Barlow (brand/fonts/), a free DIN-style face close to the logo lettering.
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
RULE = "#dfe3ea"  # hairlines
PAPER = "#ffffff"

SIZE_PX = 1080
DPI = 216  # 5 x 5 inch canvas


def setup():
    """Register the brand font and set matplotlib defaults."""
    family = "DejaVu Sans"
    for f in sorted((BRAND_DIR / "fonts").glob("*.[ot]tf")):
        font_manager.fontManager.addfont(str(f))
        family = font_manager.FontProperties(fname=str(f)).get_name()
    plt.rcParams.update(
        {
            "font.family": family,
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
    return family


def canvas():
    """A blank square figure in brand defaults."""
    size = SIZE_PX / DPI
    return plt.figure(figsize=(size, size), dpi=DPI)


def header(fig, kicker, title, subtitle=None):
    """Kicker (small caps in brand blue), bold title and an optional subtitle.

    The title wraps at about 42 characters. Returns the figure y just below the
    header, so content can start there.
    """
    lines = textwrap.wrap(title, 42)
    fig.text(0.06, 0.945, kicker.upper(), color=BLUE, fontsize=8.5,
             fontweight="semibold", va="top")
    fig.text(0.06, 0.912, "\n".join(lines), color=NAVY, fontsize=17, fontweight="bold",
             va="top", linespacing=1.05)
    y = 0.912 - 0.058 * len(lines)
    if subtitle:
        fig.text(0.06, y, subtitle, color=INK_2, fontsize=10, va="top", linespacing=1.2)
        y -= 0.04 * (subtitle.count("\n") + 1)
    return y


def footer(fig, credit):
    """Thin rule, data credit on the left, logo on the right."""
    fig.add_artist(plt.Line2D([0.06, 0.94], [0.095, 0.095], color=RULE, lw=0.8))
    fig.text(0.06, 0.075, credit, color=INK_3, fontsize=6, va="top", linespacing=1.25)
    if LOGO.exists():
        img = plt.imread(str(LOGO))
        # About 22 % of the canvas width; OffsetImage scales by dpi / 72.
        box = OffsetImage(img, zoom=0.22 * SIZE_PX / img.shape[1] / (DPI / 72))
        fig.add_artist(AnnotationBbox(box, (0.94, 0.048), xycoords="figure fraction",
                                      box_alignment=(1, 0.5), frameon=False))


def save(fig, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=DPI)
    plt.close(fig)
    return path
