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
# # 01 — Data download
#
# Fetches the two inputs for this cross-discipline example over the **Po Delta /
# eastern Po Valley** (Italy):
#
# 1. **NASA Black Marble** (VIIRS) annual night-lights radiance — the image the
#    *astronomy* Source Extractor tool will run on (cities = "sources" on a dark
#    background, just like stars). Via `earthaccess` (NASA Earthdata).
# 2. **Natura 2000** protected areas (EU, European Environment Agency) — the
#    biodiversity layer used to measure light-pollution intrusion on the Po Delta.
#
# **Credentials:** Black Marble needs a free **NASA Earthdata** login. `earthaccess`
# reads `~/.netrc` (`machine urs.earthdata.nasa.gov login … password …`). In CI,
# write `~/.netrc` from the `EARTHDATA_NETRC_BASE64` secret (see `.github/workflows`).
# Natura 2000 needs no credentials.

# %%
import json
import time
from pathlib import Path

import numpy as np
import h5py
import xarray as xr
import rioxarray  # noqa: F401
import geopandas as gpd
import earthaccess


def retry(fn, tries=5, delay=10):
    """NASA URS / LAADS occasionally hiccup — retry network calls with backoff."""
    for i in range(tries):
        try:
            return fn()
        except Exception as e:  # noqa: BLE001 — transient network/auth errors
            if i == tries - 1:
                raise
            print(f"    retry {i + 1}/{tries} after: {str(e)[:80]}")
            time.sleep(delay * (i + 1))

RAW = Path("../data/raw")
RAW.mkdir(parents=True, exist_ok=True)

BBOX = (10.5, 44.3, 13.3, 46.0)        # Po Delta + eastern Po Valley
YEAR = "2022"                           # latest annual composite returned (A2021)
DATASET = "AllAngle_Composite_Snow_Free"

# %% [markdown]
# ## 1. NASA Black Marble night lights (VNP46A4)

# %%
nl_tif = RAW / "po_delta_nightlights.tif"
if nl_tif.exists():
    print("night lights: cached")
else:
    def _fetch():
        earthaccess.login(strategy="netrc")
        res = earthaccess.search_data(short_name="VNP46A4", bounding_box=BBOX,
                                      temporal=(f"{YEAR}-01-01", f"{YEAR}-12-31"))
        g = next(x for x in res if "h19v04" in x.data_links()[0])
        return Path(earthaccess.download(g, str(RAW))[0])

    fn = retry(_fetch)
    with h5py.File(fn, "r") as h:
        p = []
        h.visititems(lambda n, o: p.append(n) if n.endswith(DATASET) else None)
        ds = h[p[0]]
        arr = ds[...].astype("float32")
        fill = float(np.asarray(ds.attrs.get("_FillValue", -999.9)).ravel()[0])
    arr[arr == fill] = np.nan
    n = arr.shape[0]                                  # tile h19v04: 10-20E, 40-50N
    lon = 10.0 + (np.arange(n) + 0.5) * 10.0 / n
    lat = 50.0 - (np.arange(n) + 0.5) * 10.0 / n
    da = xr.DataArray(arr, coords={"y": lat, "x": lon}, dims=("y", "x"), name="radiance")
    da.rio.write_crs("EPSG:4326", inplace=True)
    da.rio.clip_box(*BBOX).fillna(0.0).rio.to_raster(nl_tif, dtype="float32")
    print("wrote", nl_tif.name)

# %% [markdown]
# ## 2. Natura 2000 protected areas (EEA, EU open data)

# %%
n2k = RAW / "natura2000_podelta.geojson"
if n2k.exists():
    print("Natura 2000: cached")
else:
    base = ("https://bio.discomap.eea.europa.eu/arcgis/rest/services/"
            "ProtectedSites/Natura2000_Dyna_WM/MapServer/0/query")
    params = {"geometry": ",".join(map(str, BBOX)), "geometryType": "esriGeometryEnvelope",
              "inSR": "4326", "spatialRel": "esriSpatialRelIntersects",
              "outFields": "SITECODE,SITENAME,SITETYPE", "outSR": "4326", "f": "geojson"}
    url = base + "?" + "&".join(f"{k}={v}" for k, v in params.items())
    retry(lambda: gpd.read_file(url).to_file(n2k, driver="GeoJSON"))
    print("wrote", n2k.name)

# %% [markdown]
# ## Source log

# %%
SOURCES = [
    {"name": "NASA Black Marble VNP46A4 (VIIRS annual night lights)",
     "provider": "NASA LAADS DAAC via earthaccess", "license": "public-domain (NASA)",
     "bbox": BBOX, "tile": "h19v04"},
    {"name": "Natura 2000 (EU protected areas)",
     "provider": "European Environment Agency (Discomap ArcGIS REST)",
     "license": "EEA standard re-use", "bbox": BBOX},
]
(RAW / "sources.json").write_text(json.dumps({"sources": SOURCES}, indent=2))
print("logged sources")
