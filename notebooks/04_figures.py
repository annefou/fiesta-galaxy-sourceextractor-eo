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
# # 04 — Figures: light pollution at the edge of a dark refuge
#
# Overlays the Source-Extractor **settlement catalog** and the night-lights field on
# **Natura 2000** protected areas, and quantifies artificial-light intrusion on the
# **Po Delta** — a Ramsar / Natura 2000 wetland and a key migratory-bird refuge.

# %%
from pathlib import Path
import json
import numpy as np
import rasterio
from rasterio.features import rasterize
import geopandas as gpd
from astropy.table import Table
import matplotlib.pyplot as plt

CLEAN, RAW, RES, FIGS = (Path("../data/clean"), Path("../data/raw"),
                         Path("../results"), Path("../figures"))
FIGS.mkdir(parents=True, exist_ok=True)
plt.style.use("seaborn-v0_8-whitegrid")
LIT = 1.0  # nW/cm^2/sr: a pixel above this carries artificial light

# %% [markdown]
# ## Load raster, protected areas, and the settlement catalog

# %%
with rasterio.open(CLEAN / "po_delta_nightlights.tif") as src:
    rad = src.read(1).astype("float32")
    transform, bounds = src.transform, src.bounds

g = gpd.read_file(RAW / "natura2000_podelta.geojson").to_crs(4326)
delta = g[g["SITENAME"].str.contains("Delta del Po|Sacca di Goro|Po di Volano",
                                     case=False, na=False)]

def mask_of(gdf):
    if gdf.empty:
        return np.zeros(rad.shape, bool)
    return rasterize(((geom, 1) for geom in gdf.geometry), out_shape=rad.shape,
                     transform=transform, fill=0).astype(bool)

m_all, m_delta = mask_of(g), mask_of(delta)

cat = Table.read(RES / "po_delta_nightlights__catalog.fits")
lon, lat = rasterio.transform.xy(transform, np.asarray(cat["y"]), np.asarray(cat["x"]))
lon, lat = np.asarray(lon), np.asarray(lat)

# %% [markdown]
# ## Light-intrusion metrics

# %%
dxmin, dymin, dxmax, dymax = delta.total_bounds
near = ((lon > dxmin - 0.1) & (lon < dxmax + 0.1) &
        (lat > dymin - 0.1) & (lat < dymax + 0.1))
metrics = {
    "settlements_total": int(len(cat)),
    "region_mean_radiance": round(float(rad.mean()), 2),
    "natura2000_mean_radiance": round(float(rad[m_all].mean()), 2),
    "po_delta_mean_radiance": round(float(rad[m_delta].mean()), 2),
    "po_delta_pct_lit": round(100 * float((rad[m_delta] > LIT).mean()), 1),
    "settlements_within_10km_of_delta": int(near.sum()),
}
(RES / "biodiversity_metrics.json").write_text(json.dumps(metrics, indent=2))
for k, v in metrics.items():
    print(f"  {k}: {v}")

# %% [markdown]
# ## Headline figure

# %%
fig, ax = plt.subplots(figsize=(9, 6.6))
ext = [bounds.left, bounds.right, bounds.bottom, bounds.top]
ax.imshow(np.log1p(rad), cmap="inferno", extent=ext, origin="upper")
g.boundary.plot(ax=ax, edgecolor="#39c5bb", linewidth=0.5, alpha=0.7)
delta.boundary.plot(ax=ax, edgecolor="#ffe400", linewidth=1.8)
ax.scatter(lon, lat, s=4, c="#39c5bb", alpha=0.6, linewidths=0,
           label=f"{len(cat)} settlements (Source Extractor)")
ax.set_xlim(ext[0], ext[1]); ax.set_ylim(ext[2], ext[3])
ax.set_xlabel("lon"); ax.set_ylabel("lat")
ax.set_title("Light pollution at the edge of a dark refuge\n"
             "astronomy Source Extractor on VIIRS night lights + Natura 2000 (Po Delta, yellow)")
ax.legend(loc="lower left", fontsize=8, framealpha=0.6)
fig.tight_layout()
fig.savefig(FIGS / "main_result.png", dpi=150, bbox_inches="tight")
plt.show()
print("wrote figures/main_result.png")
