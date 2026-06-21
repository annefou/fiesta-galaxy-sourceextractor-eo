"""Run Source Extractor on an image — two ways, like the BioImage.IO example.

`run_on_galaxy()` invokes the *astronomy* Source Extractor tool
(`source_extractor_astro_tool`) on usegalaxy.eu via BioBlend — the showcased
FIESTA path (cross-image analysis *with Galaxy*). `run_local()` reproduces the
same detection offline with `sep` — the exact library the Galaxy tool wraps —
so CI and the Jupyter Book build hermetically without a key.

`segment()` picks Galaxy when a key is present, else the local fallback.
Set FIESTA_ENGINE=local|galaxy to force a path.

Detection parameters match the Galaxy tool defaults (SEP/SExtractor):
thresh=1.5*globalrms, minarea=5, deblend_nthresh=32, deblend_cont=0.005,
clean, background mesh bw=bh=64, filter fw=fh=3.
"""
from __future__ import annotations

import os
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GALAXY_URL = "https://usegalaxy.eu"
KEY_FILE = Path.home() / ".galaxy_eu_key"
CACHE = ROOT / "results" / ".galaxy_cache.json"
HISTORY = "FIESTA night lights Source Extractor"
TOOL = ("toolshed.g2.bx.psu.edu/repos/astroteam/source_extractor_astro_tool/"
        "source_extractor_astro_tool/0.0.1+galaxy0")
PARAMS = dict(thresh=1.5, err_option="float_globalrms", maskthresh=0.0, minarea=5,
              filter_case="default", filter_type="matched",
              deblend_nthresh=32, deblend_cont=0.005, clean=True, clean_param=1.0,
              bw=64, bh=64, fw=3, fh=3, fthresh=0.0)
# Galaxy output names -> local tags we keep
WANT = {"out_source_extraction_sources_picture": "sources",
        "out_source_extraction_segmentation_map_picture": "segmentation",
        "out_source_extraction_catalog_table": "catalog"}


def have_galaxy_key() -> bool:
    return KEY_FILE.exists() and bool(KEY_FILE.read_text().strip())


def catalog_count(fits_path) -> int:
    from astropy.table import Table
    return len(Table.read(fits_path))


# --------------------------------------------------------------------------- #
# Path A — the astronomy Source Extractor tool on usegalaxy.eu (BioBlend)
# --------------------------------------------------------------------------- #
def run_on_galaxy(image_path: Path, out_dir: Path) -> dict:
    import json
    from bioblend.galaxy import GalaxyInstance

    image_path, out_dir = Path(image_path), Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    gi = GalaxyInstance(GALAXY_URL, key=KEY_FILE.read_text().strip())
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    if not cache.get("history_id"):
        cache["history_id"] = gi.histories.create_history(HISTORY)["id"]
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        CACHE.write_text(json.dumps(cache, indent=2))
    hist = cache["history_id"]

    up = gi.tools.upload_file(str(image_path), hist, file_type="tiff")
    img_id = up["outputs"][0]["id"]
    gi.datasets.wait_for_dataset(img_id)

    run = gi.tools.run_tool(hist, TOOL,
                            tool_inputs={"input_file": {"src": "hda", "id": img_id}, **PARAMS})
    outs = {o["output_name"]: o["id"] for o in run["outputs"]}
    stem, paths = image_path.stem, {"engine": "galaxy:usegalaxy.eu"}
    for name, tag in WANT.items():
        ds_id = outs[name]
        gi.datasets.wait_for_dataset(ds_id)
        ext = gi.datasets.show_dataset(ds_id).get("extension", "dat")
        dest = out_dir / f"{stem}__{tag}.{ext}"
        gi.datasets.download_dataset(ds_id, file_path=str(dest), use_default_filename=False)
        paths[tag] = dest
    return paths


# --------------------------------------------------------------------------- #
# Path B — local same-library fallback (sep; hermetic, CI)
# --------------------------------------------------------------------------- #
def run_local(image_path: Path, out_dir: Path) -> dict:
    import numpy as np
    import rasterio
    import sep
    from astropy.table import Table
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Ellipse

    image_path, out_dir = Path(image_path), Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    with rasterio.open(image_path) as _src:
        data = np.ascontiguousarray(_src.read(1).astype(np.float32))
        profile = _src.profile

    bkg = sep.Background(data, bw=PARAMS["bw"], bh=PARAMS["bh"],
                         fw=PARAMS["fw"], fh=PARAMS["fh"])
    data_sub = data - bkg
    objects, segmap = sep.extract(
        data_sub, thresh=PARAMS["thresh"], err=bkg.globalrms, minarea=PARAMS["minarea"],
        deblend_nthresh=PARAMS["deblend_nthresh"], deblend_cont=PARAMS["deblend_cont"],
        clean=PARAMS["clean"], clean_param=PARAMS["clean_param"], segmentation_map=True)

    stem = image_path.stem
    cat = out_dir / f"{stem}__catalog.fits"
    Table(objects).write(cat, overwrite=True)
    seg = out_dir / f"{stem}__segmentation.tiff"
    prof = profile.copy(); prof.update(dtype="int32", count=1)
    with rasterio.open(seg, "w", **prof) as dst:
        dst.write(segmap.astype("int32"), 1)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.imshow(np.log1p(np.clip(data_sub, 0, None)), cmap="inferno", origin="upper")
    for o in objects:
        e = Ellipse((o["x"], o["y"]), 6 * o["a"], 6 * o["b"], angle=o["theta"] * 180 / np.pi)
        e.set_facecolor("none"); e.set_edgecolor("#39c5bb"); ax.add_artist(e)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(f"{len(objects)} sources (local sep)")
    src = out_dir / f"{stem}__sources.png"
    fig.savefig(src, dpi=140, bbox_inches="tight"); plt.close(fig)
    return {"catalog": cat, "segmentation": seg, "sources": src, "engine": "local:sep"}


def segment(image_path: Path, out_dir: Path, prefer_galaxy: bool = True) -> dict:
    engine = os.environ.get("FIESTA_ENGINE", "").lower()
    if engine == "local":
        return run_local(image_path, out_dir)
    if engine == "galaxy" or (prefer_galaxy and have_galaxy_key()):
        return run_on_galaxy(image_path, out_dir)
    return run_local(image_path, out_dir)
