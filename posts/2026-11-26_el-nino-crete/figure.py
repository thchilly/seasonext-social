"""Figure for the El Nino field-news post (planned 26 Nov 2026).

Winter (December-February) rainfall over Crete's land points in ERA5 against the
winter value of NOAA's Relative Oceanic Nino Index (RONI), 1950-51 to 2025-26.
Strong El Nino winters (RONI >= 1.5) are labelled; the latest observed RONI
(Aug-Oct 2026) is marked.

Data (cache/, never committed):
- ERA5 monthly means over the Crete box, 1950-2026, fetched with
  scripts/fetch_forecast_vs_reality.fetch_era5 into cache/enso/;
- https://www.cpc.ncep.noaa.gov/data/indices/RONI.ascii.txt -> cache/enso/RONI.ascii.txt
Run from the repository root: python3 <this folder>/figure.py
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import brand  # noqa: E402

xr.set_options(use_bottleneck=False)
CACHE = ROOT / "cache" / "enso"
STRONG = 1.5


def winter_rain():
    ds = xr.concat([xr.open_dataset(f) for f in sorted(CACHE.glob("era5_crete_monthly_*.nc"))], "valid_time")
    land = ds["lsm"].isel(valid_time=0) > 0.5
    w = np.cos(np.deg2rad(ds.latitude)) * land
    pr = ((ds["tp"].astype("float64") * w).sum(["latitude", "longitude"]) / w.sum()).to_series() * 1000
    pr = pr * pr.index.days_in_month  # m/day -> mm/month
    pr.index = pd.PeriodIndex(pr.index, freq="M")
    years = range(1951, pr.index.max().year + 1)
    return pd.Series({y: sum(pr[pd.Period(p, "M")] for p in (f"{y - 1}-12", f"{y}-01", f"{y}-02"))
                      for y in years if pd.Period(f"{y}-02", "M") in pr.index})


def roni():
    r = pd.read_csv(CACHE / "RONI.ascii.txt", sep=r"\s+")
    return r[r.SEAS == "DJF"].set_index("YR").ANOM, r.iloc[-1]


def main():
    djf, last = roni()
    d = pd.DataFrame({"rain": winter_rain(), "roni": djf}).dropna()
    r = np.corrcoef(d.roni, d.rain)[0, 1]
    d["rank"] = d.rain.rank(ascending=False).astype(int)
    strong = d[d.roni >= STRONG]
    print(len(d), "winters, r =", round(r, 3), "latest", last.SEAS, last.YR, last.ANOM)
    print(strong.sort_values("roni", ascending=False))

    brand.setup()
    fig = brand.canvas()
    top = brand.header(
        fig,
        "Field news",
        "A strong El Niño says little about winter rain in Crete",
        f"Winter (December to February) rain over Crete in each of {len(d)} winters, 1950-51 to\n"
        "2025-26, against the strength of El Niño (right) or La Niña (left) that winter.",
        wrap=34, size=18,
    )
    ax = fig.add_axes([0.13, 0.25, 0.79, top - 0.28])
    ax.axvspan(STRONG, 3.0, color=brand.BLUE_PALE, alpha=0.45, lw=0, zorder=0)
    ax.text(1.54, 445, "Strong\nEl Niño", ha="left", va="top", fontsize=7.5, color=brand.BLUE,
            fontweight="semibold", linespacing=1.05)
    ax.axhline(d.rain.median(), color=brand.RULE, lw=0.8, zorder=1)
    ax.text(-2.15, d.rain.median() + 6, f"middle winter, {d.rain.median():.0f} mm", fontsize=6.8,
            color=brand.INK_3, va="bottom")
    weak = d[d.roni < STRONG]
    ax.scatter(weak.roni, weak.rain, s=16, color=brand.INK_3, alpha=0.75, lw=0, zorder=2)
    ax.scatter(strong.roni, strong.rain, s=30, color=brand.NAVY, lw=0, zorder=3)
    offsets = {1983: (6, 0), 2016: (6, 0), 1998: (6, -2), 1992: (6, 3), 1958: (-6, 0), 1973: (-6, 4), 1966: (-6, 0)}
    for y, row in strong.iterrows():
        dx, dy = offsets.get(y, (6, 0))
        ax.annotate(f"{y - 1}-{str(y)[2:]}", (row.roni, row.rain), xytext=(dx, dy), textcoords="offset points",
                    ha="center" if dx == 0 else ("left" if dx > 0 else "right"), va=("bottom" if dy > 0 else "top") if dx == 0 else "center", fontsize=7, color=brand.NAVY,
                    fontweight="semibold")
    ax.axvline(last.ANOM, color=brand.WARM, lw=1.0, ls=(0, (3, 3)), zorder=1)
    ax.text(last.ANOM + 0.05, 445, f"Now: {last.ANOM:.1f}\n(Aug-Oct 2026)", ha="left", va="top",
            fontsize=7, color=brand.WARM, fontweight="semibold", linespacing=1.1)
    ax.set_xlim(-2.2, 3.0)
    ax.set_ylim(100, 450)
    ax.set_xticks([-2, -1, 0, 1, 2])
    ax.set_xticklabels(["-2", "-1", "0", "+1", "+2"], fontsize=7.5)
    ax.set_yticks([100, 200, 300, 400])
    ax.set_yticklabels(["100", "200", "300", "400 mm"], fontsize=7.5)
    ax.set_xlabel("Winter El Niño index (RONI, °C): negative La Niña, positive El Niño", fontsize=7.5, color=brand.INK_2)
    for s in ("right", "top"):
        ax.spines[s].set_visible(False)

    fig.text(0.06, 0.155,
             f"Correlation {r:.2f}: El Niño explains about {round(100 * r * r)}% of the ups and downs of Crete's\n"
             f"winter rain. Strong El Niño winters ranged from the {d.loc[strong.rain.idxmax(), 'rank']}st wettest "
             f"to the driest of {len(d)}.",
             fontsize=8.6, fontweight="semibold", color=brand.NAVY, va="top", linespacing=1.25)
    brand.footer(
        fig,
        "Rain: ERA5, Crete land points, December-February. Contains modified Copernicus Climate Change Service information 2026.\n"
        "El Niño index: NOAA Climate Prediction Center, Relative Oceanic Niño Index (RONI), December-February and August-October 2026.",
    )
    print(brand.save(fig, HERE / "image.png"))


if __name__ == "__main__":
    main()
