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
# distinct, colorblind-aware colors: settlements = cyan dots (black-edged),
# Natura 2000 = green, Po Delta = bold yellow.
C_SET, C_N2K, C_DELTA = "#00ffff", "#00ff7f", "#ffe400"
ext = [bounds.left, bounds.right, bounds.bottom, bounds.top]
dxmin, dymin, dxmax, dymax = delta.total_bounds
zext = [dxmin - 0.15, dxmax + 0.15, dymin - 0.12, dymax + 0.12]   # zoom window

fig, (axL, axR) = plt.subplots(1, 2, figsize=(14, 7.8))

# --- left: regional view, all detected settlements ---
axL.imshow(np.log1p(rad), cmap="inferno", extent=ext, origin="upper")
g.boundary.plot(ax=axL, edgecolor=C_N2K, linewidth=1.1, alpha=0.9)
delta.boundary.plot(ax=axL, edgecolor=C_DELTA, linewidth=2.5)
axL.scatter(lon, lat, s=20, facecolor=C_SET, edgecolor="black", linewidths=0.3,
            label=f"{len(cat)} detected settlements")
axL.add_patch(plt.Rectangle((zext[0], zext[2]), zext[1] - zext[0], zext[3] - zext[2],
                            fill=False, edgecolor="white", linewidth=1.0, linestyle="--"))
axL.set_xlim(ext[0], ext[1]); axL.set_ylim(ext[2], ext[3])
axL.set_xlabel("longitude"); axL.set_ylabel("latitude")
axL.set_title("Po Valley night lights → settlements\n"
              "cyan = settlements · green = Natura 2000 · yellow = Po Delta", fontsize=11)
axL.legend(loc="lower left", fontsize=9, framealpha=0.75)

# --- right: zoom on the Po Delta refuge, with the metrics ---
axR.imshow(np.log1p(rad), cmap="inferno", extent=ext, origin="upper")
delta.boundary.plot(ax=axR, edgecolor=C_DELTA, linewidth=2.8)
sel = (lon > zext[0]) & (lon < zext[1]) & (lat > zext[2]) & (lat < zext[3])
axR.scatter(lon[sel], lat[sel], s=42, facecolor=C_SET, edgecolor="black", linewidths=0.5)
axR.set_xlim(zext[0], zext[1]); axR.set_ylim(zext[2], zext[3])
axR.set_xlabel("longitude"); axR.set_ylabel("latitude")
axR.set_title("Zoom: the Po Delta refuge (yellow)", fontsize=11)
txt = (f"Po Delta (Natura 2000):\n"
       f"• {metrics['po_delta_pct_lit']}% of its area already lit\n"
       f"• {metrics['settlements_within_10km_of_delta']} settlements within ~10 km\n"
       f"• mean light {metrics['po_delta_mean_radiance']} vs {metrics['region_mean_radiance']} region-wide")
axR.text(0.03, 0.03, txt, transform=axR.transAxes, fontsize=9.5, va="bottom",
         color="white", bbox=dict(boxstyle="round", facecolor="black", alpha=0.65))

fig.suptitle("Light pollution at the edge of a dark refuge",
             fontsize=22, fontweight="bold", y=0.99)
fig.text(0.5, 0.925, "An astronomy source-detection tool, run through Galaxy on satellite "
         "night lights, catalogs settlements and measures light pressure on the Po Delta",
         ha="center", fontsize=12, color="#333")
fig.tight_layout(rect=[0, 0.11, 1, 0.90])

# logos footer: FIESTA · Galaxy · OSCARS
import matplotlib.image as mpimg
LOGOS = FIGS / "logos"
for f, box in [("fiesta.png", [0.07, 0.005, 0.10, 0.105]),
               ("galaxy.png", [0.43, 0.03, 0.14, 0.06]),
               ("oscars.png", [0.80, 0.035, 0.14, 0.05])]:
    la = fig.add_axes(box); la.imshow(mpimg.imread(LOGOS / f)); la.axis("off")

fig.savefig(FIGS / "main_result.png", dpi=150, facecolor="white", bbox_inches="tight")
plt.show()
print("wrote figures/main_result.png")

# %% [markdown]
# ## What we found
#
# **1. The cross-discipline transfer works.** An astronomy source-detection tool —
# Source Extractor (SExtractor / SEP), built to find stars and galaxies — run
# *unchanged* through Galaxy on a VIIRS night-lights image, detected and cataloged
# **453 lit settlements** across the Po Valley. It produced exactly the outputs it
# makes for the sky (a source catalog with position, brightness and size, plus a
# segmentation map), only the input image came from a different discipline. No
# retraining, no code change. Lit settlements are compact bright sources on a dark
# background — morphologically like stars — so the tool's background estimation,
# thresholding and *deblending* apply directly (deblending separates adjacent towns
# that simple brightness thresholding would merge into one blob).
#
# **2. Light is pressing on the Po Delta refuge.** Overlaying the catalog and the
# night-lights field on Natura 2000 turns the astronomy output into a
# biodiversity-impact metric. The Po Delta — a Ramsar / Natura 2000 wetland and a
# key migratory-bird site — is still a relative **dark refuge** (mean night radiance
# **0.96** vs **4.11** region-wide), but artificial light already covers about
# **18.5 %** of its area, and **145 detected settlements lie within ~10 km** of it.
# Artificial light at night is a documented stressor for the nocturnal birds,
# insects and bats the wetland supports, so this is a measurable encroachment.
#
# **3. Honest caveats.** This is **one scene, one region, one annual composite
# (2021)** — a snapshot, not a trend. Night-lights radiance is a *proxy* for human
# presence, not a direct biodiversity measurement, and "lit" here is a simple
# 1 nW·cm⁻²·sr⁻¹ threshold. In the most intensely lit parts of the Po plain the
# background is no longer dark, so detections there are less clean — the method is
# happiest exactly where refuges meet cities, like the Po Delta edge. The Galaxy and
# local `sep` paths agree (453 settlements both ways), which confirms
# *reproducibility* — but both are the same algorithm, so that is consistency, not
# independent validation.
#
# **Takeaway.** A FAIR, well-described Galaxy tool from one discipline (astronomy)
# can be picked up and do genuinely useful work in another (Earth observation /
# biodiversity), because the metadata travels with it — the same point as the
# [BioImage.IO companion example](https://github.com/annefou/fiesta-galaxy-bioimageio-eo).
