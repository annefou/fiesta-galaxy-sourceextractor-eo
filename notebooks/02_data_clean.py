# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # 02 — Data clean
#
# Prepares the **single-channel 2D raster** that the Source Extractor tool expects
# ("light sources on a dark background"). The Black Marble radiance is already
# exactly that — bright cities on a dark Earth — so cleaning is light: keep one
# band, set non-finite/negative pixels to 0 (dark), and write a clean GeoTIFF.

# %%
from pathlib import Path
import numpy as np
import rioxarray  # noqa: F401
import xarray as xr

RAW, CLEAN = Path("../data/raw"), Path("../data/clean")
CLEAN.mkdir(parents=True, exist_ok=True)

da = xr.open_dataarray(RAW / "po_delta_nightlights.tif", engine="rasterio")
if "band" in da.dims:
    da = da.isel(band=0, drop=True)
da = da.where(np.isfinite(da), 0.0).clip(min=0.0)   # dark background = 0

out = CLEAN / "po_delta_nightlights.tif"
da.rio.to_raster(out, dtype="float32")
print(f"wrote {out.name}  shape={tuple(da.shape)}  "
      f"radiance min/median/max={float(da.min()):.2f}/{float(da.median()):.2f}/{float(da.max()):.2f}")
