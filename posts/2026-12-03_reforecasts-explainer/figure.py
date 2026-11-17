"""Figure for the re-forecast explainer (planned 3 Dec 2026).

For October rainfall over the Crete area (the four 1 deg grid cells 35-36 N,
23-27 E), forecasts started on 1 September: the middle third ("near normal") of
each C3S system's own re-forecasts 1993-2016, members and years pooled, exactly
as in scripts/forecast_vs_reality.py. A reference value of 37 mm is classified
against each system's own thirds.

Data: run `python3 scripts/fetch_forecast_vs_reality.py 2026-10` first.
Run from the repository root: python3 <this folder>/figure.py
"""

import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "scripts"))
import brand  # noqa: E402
import forecast_vs_reality as fvr  # noqa: E402

NAMES = {
    "ecmwf_51": "ECMWF", "ukmo_610": "UK Met Office", "meteo_france_9": "Météo-France",
    "dwd_22": "DWD", "cmcc_4": "CMCC", "ncep_2": "NCEP", "jma_4": "JMA",
    "eccc_4": "ECCC (system 4)", "eccc_5": "ECCC (system 5)", "bom_2": "BoM",
}
VALUE = 37  # mm, the example forecast value


def thirds():
    rows = []
    for path in sorted((fvr.DATA_DIR / "2026-10").glob("seas_*.grib")):
        df = fvr.system_members(path, "tprate", 10)
        ref = df[(df.year >= 1993) & (df.year <= 2016)].value
        lo, hi = np.quantile(ref, [1 / 3, 2 / 3])
        rows.append((NAMES[path.stem.removeprefix("seas_")], lo, hi))
    return sorted(rows, key=lambda r: r[2])


def main():
    rows = thirds()
    for name, lo, hi in rows:
        print(f"{name:18s} {lo:5.1f} {hi:5.1f} {'wet' if VALUE > hi else 'normal'}")
    brand.setup()
    fig = brand.canvas()
    top = brand.header(
        fig,
        "Did you know?",
        "Every forecast system has its own normal",
        "October rainfall over the Crete area in the re-forecasts of 10 Copernicus\n"
        "systems (1993-2016). Bars: each system's near-normal middle third.",
        wrap=24,
    )
    ax = fig.add_axes([0.25, 0.24, 0.53, top - 0.30])
    n = len(rows)
    for i, (name, lo, hi) in enumerate(rows):
        wet = VALUE > hi
        ax.plot([lo, hi], [i, i], color=brand.BLUE_PALE if wet else brand.RULE, lw=10,
                solid_capstyle="butt", zorder=1)
        ax.text(lo - 1.0, i, f"{lo:.0f}", ha="right", va="center", fontsize=7, color=brand.INK_3)
        if 0 <= VALUE - hi < 4:  # keep the number clear of the dot
            ax.text(hi - 0.8, i, f"{hi:.0f}", ha="right", va="center", fontsize=7, color=brand.INK_2)
        else:
            ax.text((hi + 1.0 if hi < VALUE else max(hi + 1.0, VALUE + 2.5)), i, f"{hi:.0f}", ha="left", va="center", fontsize=7, color=brand.INK_3)
        ax.text(-0.02, i, name, transform=ax.get_yaxis_transform(), ha="right", va="center",
                fontsize=8.5, color=brand.NAVY)
        ax.scatter([VALUE], [i], s=34, color=brand.BLUE if wet else brand.INK_3, zorder=3, lw=0)
        ax.text(1.03, i, "wetter" if wet else "near normal", transform=ax.get_yaxis_transform(),
                ha="left", va="center", fontsize=8, color=brand.BLUE if wet else brand.INK_2,
                fontweight="semibold" if wet else "normal")
    ax.axvline(VALUE, color=brand.NAVY, lw=0.8, ls=(0, (3, 3)), zorder=2)
    ax.text(VALUE, n - 0.35, f"A forecast of {VALUE} mm", ha="center", va="bottom", fontsize=8.5,
            color=brand.NAVY, fontweight="semibold")
    ax.set_xlim(0, 55)
    ax.set_ylim(-0.6, n - 0.1)
    ax.set_xticks([0, 10, 20, 30, 40, 50])
    ax.set_xticklabels([f"{v} mm" for v in (0, 10, 20, 30, 40, 50)], fontsize=7)
    ax.set_yticks([])
    for s in ("left", "right", "top"):
        ax.spines[s].set_visible(False)

    n_wet = sum(VALUE > hi for _, _, hi in rows)
    fig.text(0.06, 0.175, f"The same {VALUE} mm is wetter than normal for {n_wet} systems and near normal\n"
             f"for {n - n_wet}. So each forecast is judged against its own re-forecasts.",
             fontsize=8.8, fontweight="semibold", color=brand.NAVY, va="top", linespacing=1.25)
    brand.footer(
        fig,
        "Re-forecasts (hindcasts) of 10 C3S seasonal systems started 1 September 1993-2016, October, "
        "mean of the 1° grid cells 35-36° N, 23-27° E.\n"
        "Contains modified Copernicus Climate Change Service information 2026.",
    )
    print(brand.save(fig, HERE / "image.png"))


if __name__ == "__main__":
    main()
