"""Download the data behind a "monthly check" post: forecast vs what happened in Crete.

For a target month (e.g. 2026-09) this fetches:

1. ERA5 monthly means of 2 m temperature and total precipitation over a Crete box,
   1993 to the target year (what happened, and the 1993-2016 reference climate).
2. C3S seasonal forecasts started one month before the target month (lead 1 month,
   i.e. the forecast published roughly three weeks before the month began), for every
   contributing system, for the target year and the 1993-2016 hindcasts. The hindcasts
   give each system's own "normal" so tercile probabilities can be computed.

Sources (CDS, CC BY 4.0):
    reanalysis-era5-single-levels-monthly-means  (0.25 deg)
    seasonal-monthly-single-levels               (1 deg)

Usage
-----
    python fetch_monthly_check.py 2026-09

Output (never committed): cache/monthly_check/, the shared ERA5
reference file at the top level and the per-month files in <YYYY-MM>/.
"""

import sys
import tempfile
import zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import cdsapi
import xarray as xr

DATA_DIR = Path(__file__).resolve().parents[1] / "cache" / "monthly_check"

# N, W, S, E. ERA5 box hugs the island; the 1 deg seasonal box takes the
# surrounding grid points (lat 35-36 N, lon 23-27 E).
ERA5_AREA = [35.8, 23.4, 34.8, 26.4]
SEAS_AREA = [36, 23, 35, 27]

HINDCAST_YEARS = list(range(1993, 2017))

# C3S multi-system contributors (system numbers as of the Aug 2026 start).
SYSTEMS = [
    ("ecmwf", "51"),
    ("ukmo", "610"),
    ("meteo_france", "9"),
    ("dwd", "22"),
    ("cmcc", "4"),
    ("ncep", "2"),
    ("jma", "4"),
    ("eccc", "4"),
    ("eccc", "5"),
    ("bom", "2"),
]


def unzip_merge(src, target):
    """The CDS may return a zip of one NetCDF per step type; merge into one file."""
    if not zipfile.is_zipfile(src):
        src.rename(target)
        return
    with tempfile.TemporaryDirectory() as tmpdir:
        with zipfile.ZipFile(src) as zf:
            zf.extractall(tmpdir)
        parts = [xr.open_dataset(f) for f in sorted(Path(tmpdir).glob("*.nc"))]
        # Accumulated fields are stamped 06 UTC, instantaneous ones 00 UTC.
        aligned = [ds.assign_coords(valid_time=ds.valid_time.dt.floor("D")) for ds in parts]
        xr.merge(aligned, compat="override", join="exact").load().to_netcdf(target)
        for ds in parts:
            ds.close()
    src.unlink()


def fetch_era5(client, out_dir, years, months, label):
    target = out_dir / f"era5_crete_monthly_{label}.nc"
    if target.exists():
        return f"era5 {label}: skip (exists)"
    request = {
        "product_type": ["monthly_averaged_reanalysis"],
        "variable": ["2m_temperature", "total_precipitation", "land_sea_mask"],
        "year": [str(y) for y in years],
        "month": [f"{m:02d}" for m in months],
        "time": ["00:00"],
        "area": ERA5_AREA,
        "data_format": "netcdf",
        "download_format": "unarchived",
    }
    tmp = target.with_suffix(".part")
    client.retrieve("reanalysis-era5-single-levels-monthly-means", request).download(str(tmp))
    unzip_merge(tmp, target)
    return f"era5 {label}: done"


def fetch_system(client, out_dir, centre, system, start_year, start_month):
    target = out_dir / f"seas_{centre}_{system}.grib"
    if target.exists():
        return f"{centre} {system}: skip (exists)"
    request = {
        "originating_centre": centre,
        "system": system,
        "variable": ["2m_temperature", "total_precipitation"],
        "product_type": ["monthly_mean"],
        "year": [str(y) for y in HINDCAST_YEARS + [start_year]],
        "month": [f"{start_month:02d}"],
        "leadtime_month": ["2"],
        "area": SEAS_AREA,
        "data_format": "grib",
    }
    tmp = target.with_suffix(".part")
    client.retrieve("seasonal-monthly-single-levels", request).download(str(tmp))
    tmp.rename(target)
    return f"{centre} {system}: done"


def main():
    year, month = (int(x) for x in sys.argv[1].split("-"))
    start_year, start_month = (year, month - 1) if month > 1 else (year - 1, 12)
    out_dir = DATA_DIR / f"{year}-{month:02d}"
    out_dir.mkdir(parents=True, exist_ok=True)

    def run(task):
        try:
            return task(cdsapi.Client(quiet=True))
        except Exception as exc:
            return f"FAILED: {exc}"

    # The reference years are shared across months; the current year only up to
    # the target month (later months do not exist yet).
    hist_dir = DATA_DIR
    tasks = [
        lambda c: fetch_era5(c, hist_dir, range(1993, year), range(1, 13), f"1993-{year - 1}"),
        lambda c: fetch_era5(c, out_dir, [year], range(1, month + 1), f"{year}"),
    ]
    tasks += [
        (lambda c, oc=oc, s=s: fetch_system(c, out_dir, oc, s, start_year, start_month))
        for oc, s in SYSTEMS
    ]
    with ThreadPoolExecutor(max_workers=4) as pool:
        for result in pool.map(run, tasks):
            print(result, flush=True)


if __name__ == "__main__":
    main()
