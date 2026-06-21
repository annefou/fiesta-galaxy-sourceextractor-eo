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
# # 03 — Source extraction (astronomy tool on night lights)
#
# Runs the **astronomy Source Extractor** on the night-lights raster and reads back
# the **catalog of detected sources** = lit **settlements** (position, brightness/
# flux, size), plus the segmentation map and the sources overlay.
#
# **Two execution paths** (see `scripts/source_extractor.py`):
#
# - **Galaxy (showcased):** if `~/.galaxy_eu_key` is present, the tool runs on
#   **usegalaxy.eu** via BioBlend — the FIESTA result: cross-image analysis with Galaxy.
# - **Local fallback (CI):** otherwise the same library (`sep`, which the Galaxy tool
#   wraps) runs offline, so the Jupyter Book builds without a key.
#
# Set `FIESTA_ENGINE=local` to force the hermetic path.

# %%
import sys
from pathlib import Path
import pandas as pd
from astropy.table import Table

sys.path.insert(0, str(Path("../scripts").resolve()))
from source_extractor import segment, have_galaxy_key  # noqa: E402

CLEAN, RESULTS = Path("../data/clean"), Path("../results")
RESULTS.mkdir(parents=True, exist_ok=True)
print("execution path:", "Galaxy (usegalaxy.eu)" if have_galaxy_key()
      else "local sep fallback")

# %% [markdown]
# ## Run Source Extractor and read the settlement catalog

# %%
img = CLEAN / "po_delta_nightlights.tif"
out = segment(img, RESULTS)
print("engine:", out["engine"])

cat = Table.read(out["catalog"])
n = len(cat)
flux = cat["flux"] if "flux" in cat.colnames else None
print(f"settlements detected (sources): {n}")
if flux is not None:
    print(f"total cataloged light (sum flux): {float(flux.sum()):.0f}")
    print(f"brightest source flux:           {float(flux.max()):.0f}")

# persist a small summary for the figures notebook + provenance
summary = {"engine": out["engine"], "n_settlements": int(n),
           "total_flux": float(flux.sum()) if flux is not None else None}
pd.Series(summary).to_json(RESULTS / "extraction_summary.json")
summary

# %% [markdown]
# ## What this shows
#
# A tool built to find stars and galaxies, pointed at the night side of Europe,
# produces a catalog of lit settlements — the same outputs (catalog, segmentation,
# photometry), a new discipline. Notebook 04 overlays this on Natura 2000 to
# quantify light-pollution pressure on the Po Delta biodiversity refuge.
