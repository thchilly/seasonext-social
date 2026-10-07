"""Paper card: a square image for "published work" posts.

Three headline numbers and three or four one-line findings, with the citation.
The content of each card lives in a JSON file next to the post, e.g.

    {
      "kicker": "Published work",
      "title": "Which rainfall dataset can we trust in Greece?",
      "citation": "Papa & Koutroulis (2025), Atmospheric Research 315, 107888",
      "numbers": [["8", "gridded rainfall\\ndatasets"], ["304", "rain gauges"], ...],
      "findings": [["Most consistent overall", "CHELSA and AgERA5"], ...],
      "credit": "doi.org/10.1016/j.atmosres.2024.107888"
    }

Usage
-----
    python paper_card.py card.json out.png
"""

import json
import sys

import brand


def render(spec, out):
    brand.setup()
    fig = brand.canvas()
    top = brand.header(fig, spec["kicker"], spec["title"], spec["citation"])

    # Headline numbers.
    n = len(spec["numbers"])
    y = top - 0.05
    for i, (value, label) in enumerate(spec["numbers"]):
        x = 0.06 + i * 0.88 / n
        fig.text(x, y, value, fontsize=40, fontweight="bold", color=brand.BLUE, va="top")
        fig.text(x, y - 0.125, label, fontsize=10, color=brand.INK_2, va="top", linespacing=1.15)

    # Findings: hairline-separated rows, label left, answer right.
    y -= 0.27
    step = 0.075
    for label, answer in spec["findings"]:
        fig.add_artist(brand.plt.Line2D([0.06, 0.94], [y + 0.03, y + 0.03], color=brand.RULE, lw=0.8))
        fig.text(0.06, y, label, fontsize=10, color=brand.INK_2, va="center")
        fig.text(0.94, y, answer, fontsize=11, fontweight="semibold", color=brand.NAVY,
                 va="center", ha="right")
        y -= step
    fig.add_artist(brand.plt.Line2D([0.06, 0.94], [y + 0.03, y + 0.03], color=brand.RULE, lw=0.8))

    brand.footer(fig, spec.get("credit", ""))
    return brand.save(fig, out)


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        print(render(json.load(f), sys.argv[2]))
