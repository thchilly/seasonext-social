"""Figure for the "Crete's rainfall from west to east" explainer (planned 17 Dec 2026).

Map: CLIMADAT-Grid mean annual precipitation 1981-2019 (~1 km, land cells).
Labels: measured average yearly rainfall at NOA / meteo.gr stations, 2006-2025,
complete years only (scripts/noa_stations.py). Station positions are the towns
and villages, approximate (playbook section 6).
Profile: CLIMADAT island average in 0.25 degree longitude bands, west to east.

Run from the repository root: python3 <this folder>/figure.py
"""

import sys
from pathlib import Path

import numpy as np
import xarray as xr
from matplotlib.colors import LinearSegmentedColormap

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "scripts"))
import brand  # noqa: E402
import noa_stations  # noqa: E402

xr.set_options(use_bottleneck=False)
REFERENCE = HERE.parents[1] / "reference" / "climadat_crete_pr_1981-2019.nc"

# (label, lat, lon, NOA aliases, label offset in points)
STATIONS = [
    ("Chania", 35.51, 24.02, ["Chania"], (0, 9)),
    ("Samaria (Xyloskalo)", 35.307, 23.92, ["Samaria"], (0, -10)),
    ("Rethymno", 35.37, 24.47, ["Rethymno", "Rethimno", "Rethymnotown"], (0, 9)),
    ("Anogeia", 35.29, 24.885, ["Anogeia", "Anogia"], (0, -10)),
    ("Heraklion", 35.34, 25.13, ["Heraclion"], (0, 9)),
    ("Tzermiado", 35.197, 25.489, ["Tzermiado", "Tzermiadon"], (0, 9)),
    ("Ierapetra", 35.01, 25.74, ["Ierapetra"], (0, -10)),
    ("Sitia", 35.21, 26.10, ["Sitia"], (0, 9)),
]
BANDS = np.arange(23.45, 26.36, 0.25)


def main():
    annual = xr.open_dataset(REFERENCE)["pr_annual"].astype("float64")
    lon, lat = annual.lon.values, annual.lat.values

    brand.setup()
    fig = brand.canvas()
    top = brand.header(
        fig,
        "Did you know?",
        "Crete gets far more rain in the west and on its mountains",
        "Average yearly rainfall across the island.",
        wrap=40, size=17,
    )

    cmap = LinearSegmentedColormap.from_list(
        "brand_blues", ["#eef2f8", brand.BLUE_PALE, brand.BLUE_LIGHT, brand.BLUE_MID, brand.BLUE, brand.NAVY]
    )
    h = 0.84 * (lat.max() - lat.min()) / np.cos(np.deg2rad(35.3)) / (lon.max() - lon.min())
    ax = fig.add_axes([0.08, top - 0.015 - h, 0.84, h])
    ax.pcolormesh(lon, lat, annual.values, cmap=cmap, vmin=400, vmax=1800, shading="auto",
                  rasterized=True)
    for name, la, lo, aliases, off in STATIONS:
        mm = noa_stations.record(aliases)["annual_mean"]
        print(f"{name:22s} {mm:6.0f}")
        ax.scatter([lo], [la], s=22, color=brand.NAVY, edgecolor=brand.PAPER, lw=1.0, zorder=3)
        ax.annotate(f"{name}\n{round(mm, -1):,.0f} mm", (lo, la), xytext=off, textcoords="offset points",
                    ha="center", va="bottom" if off[1] > 0 else "top", fontsize=6.6,
                    fontweight="semibold", color=brand.NAVY, linespacing=1.05)
    ax.set_xlim(lon.min(), lon.max())
    ax.set_ylim(lat.min() - 0.02, lat.max() + 0.02)
    ax.set_aspect(1 / np.cos(np.deg2rad(35.3)))
    ax.axis("off")

    # Colour key
    y_key = top - 0.015 - h - 0.02
    kax = fig.add_axes([0.645, y_key, 0.265, 0.012])
    kax.imshow(np.linspace(0, 1, 256)[None, :], cmap=cmap, aspect="auto", extent=[400, 1800, 0, 1])
    kax.set_yticks([])
    kax.set_xticks([400, 800, 1200, 1800])
    kax.set_xticklabels(["400", "800", "1,200", "1,800"], fontsize=6.5)
    kax.tick_params(length=0, pad=2)
    for s in kax.spines.values():
        s.set_visible(False)
    fig.text(0.06, y_key + 0.006, "Shading: 1 km grid, 1981-2019, mm a year. Labels: stations, 2006-2025.",
             fontsize=6.8, color=brand.INK_2, va="center")

    # West-to-east profile
    groups = annual.groupby_bins("lon", BANDS)
    mids = np.array([(b.left + b.right) / 2 for b, _ in groups])
    means = np.array([float(v.mean()) for _, v in groups])
    west = float(annual.where(annual.lon < 24.5).mean())
    east = float(annual.where(annual.lon > 25.5).mean())
    print("bands", np.round(means), "west", round(west), "east", round(east))

    pax = fig.add_axes([0.10, 0.115, 0.80, y_key - 0.25])
    pax.bar(mids, means, width=0.22, color=brand.BLUE_MID, lw=0)
    for x, m in zip(mids, means):
        pax.text(x, m + 25, f"{round(m, -1):,.0f}", ha="center", va="bottom", fontsize=6.8, color=brand.INK_2)
    pax.set_xlim(BANDS[0], BANDS[-1])
    pax.set_ylim(0, 1250)
    pax.set_yticks([])
    pax.set_xticks([23.6, 24.0, 24.5, 25.1, 25.7, 26.2])
    pax.set_xticklabels(["Kissamos", "Chania", "Rethymno", "Heraklion", "Ierapetra", "Sitia"], fontsize=7)
    pax.tick_params(length=0)
    for s in ("left", "right", "top"):
        pax.spines[s].set_visible(False)
    fig.text(0.06, y_key - 0.045,
             f"West to east: about {round(west, -1):,.0f} mm a year on average west of Rethymno,\n"
             f"about {round(east, -1):,.0f} mm east of the Lasithi Plateau (1 km grid, 0.25° bands)",
             fontsize=8.4, fontweight="semibold", color=brand.NAVY, va="top", linespacing=1.25)

    brand.footer(
        fig,
        "Map and profile: CLIMADAT-Grid 1981-2019 mean annual precipitation (Varotsos et al. 2025, ESSD; CC BY 4.0). Gridded and station\n"
        "values differ. Stations: National Observatory of Athens / meteo.gr, monthly records 2006-2025, complete years; positions approximate.",
    )
    print(brand.save(fig, HERE / "image.png"))


if __name__ == "__main__":
    main()
