"""Figure for the Crete floods post (30 Sep to 4 Oct 2026).

Five-day station totals (National Observatory of Athens / meteo.gr, preliminary,
article of 2026-10-05) against each station's own record: its average year and
its wettest month in the NOA monthly records 2006-2025 (complete years only).
The map shows CLIMADAT-Grid 1981-2019 mean annual rainfall as background;
station positions on it are the villages, approximate.

Run from the repository root: python <this folder>/figure.py
"""

import sys
from pathlib import Path

import numpy as np
import xarray as xr

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "scripts"))  # <root>/scripts
import brand  # noqa: E402
import noa_stations  # noqa: E402

xr.set_options(use_bottleneck=False)
REFERENCE = HERE.parents[1] / "reference" / "climadat_crete_pr_1981-2019.nc"

# meteo.gr 2026-10-05 (entryID 4340): article text values, the conservative ones.
# Coordinates are the villages / Samaria gorge entrance, approximate.
# NOA record aliases: "Samaria" (Samaria National Park) is taken to be the
# Xyloskalo station; the separate gorge station is "Samariagorge".
# (name, lat, lon, mm, reported as "over", map label above the dot, NOA aliases)
STATIONS = [
    ("Samaria (Xyloskalo)", 35.307, 23.920, 840, True, True, ["Samaria"]),
    ("Anogeia", 35.290, 24.885, 640, True, True, ["Anogeia", "Anogia"]),
    ("Tzermiado, Lasithi Plateau", 35.197, 25.489, 448, False, False, ["Tzermiado", "Tzermiadon"]),
]
CRETE = dict(lat=slice(34.8, 35.72), lon=slice(23.45, 26.35))


def main():
    annual = xr.open_dataset(REFERENCE)["pr_annual"].astype("float64")

    brand.setup()
    fig = brand.canvas()
    top = brand.header(
        fig,
        "Event in context",
        "Months of rain in five days",
        "Crete, 30 September to 4 October 2026. Rain at three stations,\n"
        "measured against each station's own record (2006-2025).",
    )

    # Map: typical yearly rainfall over Crete, stations on top.
    crete = annual.sel(**CRETE)
    ax = fig.add_axes([0.06, top - 0.205, 0.88, 0.185])
    lon, lat = crete.lon.values, crete.lat.values
    from matplotlib.colors import LinearSegmentedColormap

    cmap = LinearSegmentedColormap.from_list(
        "brand_blues", ["#eef2f8", brand.BLUE_PALE, brand.BLUE_LIGHT, brand.BLUE_MID, brand.BLUE]
    )
    ax.pcolormesh(lon, lat, crete.values, cmap=cmap, vmin=300, vmax=1600, shading="auto",
                  rasterized=True)
    for name, la, lo, mm, _, above, _ in STATIONS:
        ax.scatter([lo], [la], s=46, color=brand.NAVY, edgecolor=brand.PAPER, lw=1.5, zorder=3)
        short = name.split(",")[0].split(" (")[0]
        ax.annotate(short, (lo, la), xytext=(0, 9 if above else -9), textcoords="offset points",
                    ha="center", va="bottom" if above else "top", fontsize=8,
                    fontweight="semibold", color=brand.NAVY)
    ax.set_xlim(lon.min(), lon.max())
    ax.set_ylim(lat.min(), lat.max())
    ax.set_aspect(1 / np.cos(np.deg2rad(35.3)))
    ax.axis("off")
    fig.text(0.94, top - 0.21, "Map: typical yearly rainfall, 300 mm (pale) to 1,600 mm (dark)",
             ha="right", va="top", fontsize=6.5, color=brand.INK_3)

    # Rows: five-day total (dark) over the station's average year (pale), same
    # scale. Below each bar: share of an average year, and the station's wettest
    # month on record.
    x0, width = 0.06, 0.88
    y = top - 0.305
    vmax = 1700
    for name, la, lo, mm, over, _, aliases in STATIONS:
        rec = noa_stations.record(aliases)
        normal, wettest = rec["annual_mean"], rec["wettest_month_mm"]
        share = round(mm / normal * 20) * 5
        fig.text(x0, y + 0.032, name, fontsize=11.5, fontweight="semibold", color=brand.NAVY,
                 va="bottom", fontfamily=brand.SERIF)
        fig.text(x0 + width, y + 0.032, f"about {share}% of an average year ({round(normal, -1):,.0f} mm)",
                 fontsize=9, color=brand.INK_2, va="bottom", ha="right")
        bar = fig.add_axes([x0, y - 0.005, width, 0.03])
        bar.barh(0, normal, height=1, color=brand.BLUE_PALE, lw=0)
        bar.barh(0, mm, height=1, color=brand.NAVY, lw=0)
        bar.text(mm / 2, 0, f"{'over ' if over else ''}{mm} mm in 5 days", fontsize=8.5,
                 color=brand.PAPER, va="center", ha="center", fontweight="semibold")
        bar.set_xlim(0, vmax)
        bar.set_ylim(-0.5, 0.5)
        bar.axis("off")
        if mm > wettest:
            fig.text(x0, y - 0.015,
                     f"More than any month on record (since {rec['first_year']}; previous high "
                     f"{wettest:,.0f} mm)",
                     fontsize=8, color=brand.WARM, fontweight="semibold", va="top")
        else:
            fig.text(x0, y - 0.015,
                     f"Wettest month on record (since {rec['first_year']}): {wettest:,.0f} mm",
                     fontsize=8, color=brand.INK_3, va="top")
        y -= 0.135

    brand.footer(
        fig,
        "Rain: National Observatory of Athens / meteo.gr stations; event totals preliminary (5 Oct 2026), records 2006-2025.\n"
        "Map: CLIMADAT-Grid 1981-2019 mean annual rainfall (Varotsos et al. 2025, CC BY 4.0).",
    )
    print(brand.save(fig, HERE / "image.png"))


if __name__ == "__main__":
    main()
