"""Profile images for the SEASONEXT accounts (X, Bluesky, LinkedIn).

- Avatar: the SEASONEXT emblem centred on white, square. Platforms crop avatars to
  a circle, so the emblem is kept inside the inscribed circle.
- Header: Crete shaded by mean annual rainfall (CLIMADAT-Grid 1981-2019) with the
  tagline. 3:1, which suits both X (1500 x 500) and Bluesky (3000 x 1000). The
  bottom-left corner stays empty because both platforms put the avatar there.

Usage
-----
    python scripts/profile_images.py        # writes to profile/
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from matplotlib.colors import LinearSegmentedColormap

import brand

xr.set_options(use_bottleneck=False)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "profile"
REFERENCE = ROOT / "reference" / "climadat_crete_pr_1981-2019.nc"


def avatar(size_px):
    fig = plt.figure(figsize=(1, 1), dpi=size_px)
    fig.patch.set_facecolor(brand.PAPER)
    img = plt.imread(str(brand.EMBLEM))
    h, w = img.shape[:2]
    width = 0.62  # fraction of the canvas; the emblem's corners stay inside the circle
    height = width * h / w
    ax = fig.add_axes([(1 - width) / 2, (1 - height) / 2, width, height])
    ax.imshow(img, interpolation="lanczos")
    ax.axis("off")
    path = OUT / f"avatar_{size_px}.png"
    fig.savefig(path, dpi=size_px)
    plt.close(fig)
    return path


def header(width_px):
    brand.setup()
    crete = xr.open_dataset(REFERENCE)["pr_annual"]

    dpi = width_px / 15
    fig = plt.figure(figsize=(15, 5), dpi=dpi)
    fig.patch.set_facecolor(brand.PAPER)
    cmap = LinearSegmentedColormap.from_list(
        "brand_blues", ["#eef2f8", brand.BLUE_PALE, brand.BLUE_LIGHT, brand.BLUE_MID, brand.BLUE]
    )
    ax = fig.add_axes([0.30, 0.04, 0.68, 0.70])
    ax.pcolormesh(crete.lon, crete.lat, crete.values, cmap=cmap, vmin=300, vmax=1600,
                  shading="auto", rasterized=True)
    ax.set_aspect(1 / np.cos(np.deg2rad(35.3)))
    ax.axis("off")

    fig.text(0.04, 0.86, "Seasonal hydrological outlooks", fontsize=34, fontweight="bold",
             color=brand.NAVY, va="top")
    fig.text(0.04, 0.70, "for water extremes", fontsize=34, fontweight="bold",
             color=brand.BLUE, va="top")
    fig.text(0.98, 0.04, "Crete, mean annual rainfall 1981-2019 (CLIMADAT-Grid, Varotsos et al. 2025)",
             fontsize=9, color=brand.INK_3, ha="right", va="bottom")
    path = OUT / f"header_{width_px}x{width_px // 3}.png"
    fig.savefig(path, dpi=dpi)
    plt.close(fig)
    return path


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for p in (avatar(400), avatar(1000), header(1500), header(3000)):
        print(p)
