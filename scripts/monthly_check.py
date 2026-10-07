"""Monthly forecast check for Crete: what the seasonal forecasts said vs what happened.

For a target month, compares the C3S seasonal forecasts started one month earlier
(all contributing systems) with what ERA5 recorded over Crete, for rainfall and
2 m temperature. Everything is expressed in thirds ("terciles") of the 1993-2016
reference climate:

- Forecast: for each system, the share of its ensemble members that fall in the
  lower, middle and upper third of that system's own 1993-2016 hindcasts for the
  same start month and lead. The multi-system probability is the plain average of
  the systems (each system weighted equally).
- Observed: where the ERA5 value for the target month falls among the ERA5
  1993-2016 values for that calendar month (Crete land points only).

Run fetch_monthly_check.py first.

Usage
-----
    python monthly_check.py 2026-09 [--out DIR]
"""

import argparse
import calendar
import json
from pathlib import Path

import numpy as np
import pandas as pd
import xarray as xr

import brand

xr.set_options(use_bottleneck=False)

HERE = Path(__file__).resolve().parent
DATA_DIR = HERE.parent / "cache" / "monthly_check"
REF = (1993, 2016)
LABELS = {
    "pr": ("drier than normal", "near normal", "wetter than normal"),
    "t2m": ("cooler than normal", "near normal", "warmer than normal"),
}
SHORT = {"pr": ("dry", "normal", "wet"), "t2m": ("cool", "normal", "warm")}
# A forecast "leans" only if its most likely third has at least this chance
# (C3S maps of the most likely category start shading at 40 %).
LEAN = 0.40


def era5_series(year, month):
    """Crete land-mean ERA5 rainfall (mm/month) and temperature (deg C), one value per year."""
    files = sorted(DATA_DIR.glob("era5_crete_monthly_*.nc")) + [
        DATA_DIR / f"{year}-{month:02d}" / f"era5_crete_monthly_{year}.nc"
    ]
    ds = xr.concat([xr.open_dataset(f) for f in files], dim="valid_time")
    ds = ds.sel(valid_time=ds.valid_time.dt.month == month)
    land = ds["lsm"].isel(valid_time=0) > 0.5
    w = np.cos(np.deg2rad(ds.latitude)) * land
    days = calendar.monthrange(year, month)[1]

    def box(da):
        da = da.astype("float64")
        return (da * w).sum(["latitude", "longitude"]) / w.sum()

    years = ds.valid_time.dt.year.values
    pr = pd.Series(box(ds["tp"]).values * 1000 * days, index=years)  # m/day -> mm/month
    t2m = pd.Series(box(ds["t2m"]).values - 273.15, index=years)
    return {"pr": pr, "t2m": t2m}


def system_members(path, var, month):
    """Box-mean values of one system: DataFrame with columns year, value (one row per member)."""
    ds = xr.open_dataset(path, engine="cfgrib", backend_kwargs={"indexpath": ""})
    da = ds[var].astype("float64").mean(["latitude", "longitude"])
    df = da.to_dataframe(name="value").reset_index().dropna(subset=["value"])
    # Lagged systems initialise in the days before the nominal start; shift
    # forward to land in the nominal start month, then move to the target year.
    start = pd.to_datetime(df["time"]) + pd.Timedelta(days=25)
    df["year"] = start.dt.year + (start.dt.month > month).astype(int)
    if var == "tprate":
        df["value"] *= 86400 * 1000 * calendar.monthrange(2001, month)[1]
    else:
        df["value"] -= 273.15
    return df[["year", "value"]]


def tercile_probs(df, year):
    """Shares of the target-year members in each third of the system's own hindcast."""
    ref = df[(df.year >= REF[0]) & (df.year <= REF[1])].value
    lo, hi = np.quantile(ref, [1 / 3, 2 / 3])
    fc = df[df.year == year].value
    if fc.empty:
        return None
    return np.array([(fc < lo).mean(), ((fc >= lo) & (fc <= hi)).mean(), (fc > hi).mean()])


def forecast_probs(year, month):
    out = {"pr": {}, "t2m": {}}
    for path in sorted((DATA_DIR / f"{year}-{month:02d}").glob("seas_*.grib")):
        name = path.stem.removeprefix("seas_")
        for key, var in (("pr", "tprate"), ("t2m", "t2m")):
            p = tercile_probs(system_members(path, var, month), year)
            if p is not None:
                out[key][name] = p
    return out


def observed(series, year):
    ref = series.loc[REF[0]:REF[1]]
    lo, hi = np.quantile(ref, [1 / 3, 2 / 3])
    value = series.loc[year]
    category = 0 if value < lo else (2 if value > hi else 1)
    record = "high" if value >= series.max() else ("low" if value <= series.min() else None)
    return {"value": value, "lo": lo, "hi": hi, "mean": ref.mean(), "category": category,
            "ref": ref, "record": record, "since": int(series.index.min())}


def summarise(year, month):
    obs = era5_series(year, month)
    fc = forecast_probs(year, month)
    summary = {}
    for key in ("pr", "t2m"):
        o = observed(obs[key], year)
        probs = np.mean(list(fc[key].values()), axis=0)
        summary[key] = {
            "observed": o,
            "probs": probs,
            "systems": fc[key],
            "n_systems": len(fc[key]),
            "leaning": [int(np.argmax(p)) for p in fc[key].values()],
        }
    return summary


def draw_panel(fig, rect, key, s, unit, fmt, year, month):
    """One variable as three equal-width thirds of the reference years.

    Grey dots are the 24 reference years placed by rank (8 per third), so the
    thirds have equal width whatever the shape of the distribution. The target
    year is placed by where it falls among them. Forecast probability sets the
    tint strength of each third.
    """
    o, probs = s["observed"], s["probs"]
    ref = np.sort(o["ref"].values)
    n = len(ref)
    ranks = (np.arange(n) + 0.5) / n

    def pos(v):
        return float(np.clip(np.interp(v, ref, ranks, left=0.005, right=0.995), 0.005, 0.995))

    ax = fig.add_axes(rect)
    edges = [0, pos(o["lo"]), pos(o["hi"]), 1]
    tints = (brand.WARM, brand.INK_3, brand.BLUE) if key == "pr" else (brand.BLUE, brand.INK_3, brand.WARM)
    for i in range(3):
        ax.axvspan(edges[i], edges[i + 1], color=tints[i], alpha=0.06 + 0.42 * probs[i], lw=0)
        mid = 0.5 * (edges[i] + edges[i + 1])
        ax.text(mid, 1.36, f"{probs[i] * 100:.0f}%", ha="center", va="bottom",
                fontsize=15, fontweight="bold", color=brand.NAVY)
        ax.text(mid, 1.14, LABELS[key][i], ha="center", va="bottom", fontsize=7.5,
                color=brand.INK_2)
    for e, v in ((edges[1], o["lo"]), (edges[2], o["hi"])):
        ax.axvline(e, color=brand.PAPER, lw=2)
        ax.text(e, -0.12, f"{fmt(v)} {unit}", ha="center", va="top", fontsize=7,
                color=brand.INK_3)

    ax.scatter(ranks, np.full(n, 0.5), s=16, color=brand.INK_3, lw=0, zorder=3)
    x = pos(o["value"])
    ax.scatter([x], [0.5], s=170, color=brand.NAVY, zorder=4, edgecolor=brand.PAPER, lw=2,
               clip_on=False)
    label = f"{year}: {fmt(o['value'])} {unit}"
    mname = calendar.month_name[month]
    if o["record"] == "high":
        label += f", {'wettest' if key == 'pr' else 'warmest'} {mname} of {o['since']}-{year}"
    elif o["record"] == "low":
        label += f", {'driest' if key == 'pr' else 'coolest'} {mname} of {o['since']}-{year}"
    ha = "right" if x > 0.8 else ("left" if x < 0.2 else "center")
    anchor = {"right": 1.0, "left": 0.0, "center": x}[ha]
    ax.annotate(label, (anchor, 0.5), xytext=(0, -24),
                textcoords="offset points", ha=ha, va="top", fontsize=9,
                fontweight="bold", color=brand.NAVY)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    return ax


def verdict(key, s):
    """One-line verdict, following the rules in the playbook.

    - Signal: the forecast leans to its most likely third only if that third has
      at least LEAN (40 %); otherwise it is "no clear signal" and is not scored.
    - On the line: an observation within a tenth of the middle third's width of
      a boundary is described as on the line (see score() for how it is scored).
    - Otherwise: the observed third is named.
    """
    o, probs = s["observed"], s["probs"]
    words = SHORT[key]
    lean = int(np.argmax(probs))
    if probs[lean] < LEAN:
        head = f"No clear signal in the forecasts (largest chance {probs[lean] * 100:.0f}%)."
    else:
        head = f"Forecasts leaned {words[lean]} ({probs[lean] * 100:.0f}% chance)."
    margin = 0.1 * (o["hi"] - o["lo"])
    for edge, a, b in ((o["lo"], 0, 1), (o["hi"], 1, 2)):
        if abs(o["value"] - edge) < margin:
            return head + f" It came in right on the line between {words[a]} and {words[b]}."
    return head + f" It was {words[o['category']]}."


def score(s):
    """'hit', 'miss', 'on the line' or 'no signal' (for the running scorecard).

    "On the line" only when the observation sits within the margin of a boundary
    that touches the leaned third, i.e. when it could go either way. An
    observation on the line between two thirds the forecast did not lean to is
    a plain miss.
    """
    o, probs = s["observed"], s["probs"]
    lean = int(np.argmax(probs))
    if probs[lean] < LEAN:
        return "no signal"
    margin = 0.1 * (o["hi"] - o["lo"])
    for edge, a, b in ((o["lo"], 0, 1), (o["hi"], 1, 2)):
        if abs(o["value"] - edge) < margin and lean in (a, b):
            return "on the line"
    return "hit" if o["category"] == lean else "miss"


def render(year, month, summary, out):
    brand.setup()
    fig = brand.canvas()
    mname = calendar.month_name[month]
    prev = calendar.month_name[month - 1 if month > 1 else 12]
    brand.header(
        fig,
        "SEASONEXT monthly forecast check",
        f"{mname} {year} in Crete",
        f"What the seasonal forecasts said at the start of {prev}, and what\n"
        f"happened. Grey dots: the {mname}s of 1993-2016, in three equal thirds.",
    )
    specs = [
        ("pr", "Rainfall", "mm", lambda v: f"{v:.0f}", 0.49),
        ("t2m", "Temperature", "°C", lambda v: f"{v:.1f}", 0.18),
    ]
    for key, title, unit, fmt, y in specs:
        fig.text(0.06, y + 0.215, title, fontsize=12, fontweight="bold", color=brand.NAVY)
        fig.text(0.06, y + 0.19, verdict(key, summary[key]), fontsize=8.5, color=brand.INK_2)
        draw_panel(fig, [0.06, y, 0.88, 0.075], key, summary[key], unit, fmt, year, month)

    n = summary["pr"]["n_systems"]
    brand.footer(
        fig,
        f"Forecast: average of {n} C3S seasonal systems started 1 {prev} {year}.\n"
        f"Observed: ERA5, Crete land points. Thirds from 1993-2016.\n"
        f"Contains modified Copernicus Climate Change Service information {year}.",
    )
    return brand.save(fig, out)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("month", help="target month, YYYY-MM")
    parser.add_argument("--out", default=None)
    args = parser.parse_args()
    year, month = (int(x) for x in args.month.split("-"))
    summary = summarise(year, month)

    report = {}
    for key, s in summary.items():
        o = s["observed"]
        report[key] = {
            "observed_value": round(float(o["value"]), 2),
            "ref_mean": round(float(o["mean"]), 2),
            "tercile_edges": [round(float(o["lo"]), 2), round(float(o["hi"]), 2)],
            "observed_category": int(o["category"]),
            "score": score(s),
            "multi_system_probs": [round(float(p), 3) for p in s["probs"]],
            "per_system": {k: [round(float(x), 3) for x in v] for k, v in s["systems"].items()},
        }
    print(json.dumps(report, indent=2))

    out = Path(args.out) if args.out else DATA_DIR / f"{year}-{month:02d}" / "monthly_check.png"
    print(render(year, month, summary, out))


if __name__ == "__main__":
    main()
