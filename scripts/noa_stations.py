"""Monthly rainfall records of the NOA / meteo.gr automatic station network.

The National Observatory of Athens publishes one Excel file with the monthly
rainfall of every station in its network, 2006-2025 (one sheet per year; each
sheet also holds monthly minimum and maximum temperature extremes, not used here):
https://meteosearch.meteo.gr/Raw%20Materials/RECORDS_STATIONS_METEO_2006-2025.xlsx

Station names change spelling between years (Anogeia / Anogia, Tzermiado /
Tzermiadon), so a station is selected by a list of aliases. Daily and 10-minute
data need a free meteosearch account (limits: 30 files per day, 720 per user).

Usage
-----
    python noa_stations.py Anogeia,Anogia
"""

import subprocess
import sys
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parents[1] / "cache" / "stations"
URL = "https://meteosearch.meteo.gr/Raw%20Materials/RECORDS_STATIONS_METEO_2006-2025.xlsx"
XLSX = DATA_DIR / "RECORDS_STATIONS_METEO_2006-2025.xlsx"
CSV = DATA_DIR / "noa_monthly_rain_2006-2025.csv"


def download():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not XLSX.exists():
        # Python's default client is refused by the site's CDN; curl is served normally.
        subprocess.run(["curl", "-sSL", "-o", str(XLSX), URL], check=True)
    return XLSX


def monthly_rain():
    """Long table: station, station_gr, year, month, rain_mm (cached as CSV)."""
    if CSV.exists():
        return pd.read_csv(CSV)
    book = pd.ExcelFile(download())
    rows = []
    for sheet in book.sheet_names:
        df = book.parse(sheet, header=None)
        # The rainfall table runs from row 2 to the minimum temperature title.
        stop = next((i for i, v in df[1].items()
                     if isinstance(v, str) and "TEMPERATURE" in v.upper()), len(df))
        for _, r in df.iloc[2:stop].iterrows():
            if pd.isna(r[2]):
                continue
            for m in range(1, 13):
                rows.append((str(r[2]).strip(), str(r[1]).strip(), int(sheet), m,
                             pd.to_numeric(r[2 + m], errors="coerce")))
    out = pd.DataFrame(rows, columns=["station", "station_gr", "year", "month", "rain_mm"])
    out.to_csv(CSV, index=False)
    return out


def record(aliases):
    """Climatology of one station from its own record (complete years only)."""
    d = monthly_rain()
    table = d[d.station.isin(aliases)].groupby(["year", "month"]).rain_mm.mean().unstack()
    full = table.dropna()
    annual = full.sum(axis=1)
    wettest = table.stack().idxmax()
    return {
        "first_year": int(table.index.min()),
        "complete_years": len(full),
        "annual_mean": float(annual.mean()),
        "wettest_month_mm": float(table.max().max()),
        "wettest_month": f"{wettest[0]}-{wettest[1]:02d}",
        "october_mean": float(table[10].mean()),
    }


if __name__ == "__main__":
    print(record(sys.argv[1].split(",")))
