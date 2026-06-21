# Snakefile — orchestrates the cross-discipline pipeline end-to-end.
#
# Each rule wraps a jupytext notebook (the notebook stays the source of truth).
# notebooks/03 runs the astronomy Source Extractor on usegalaxy.eu when a key is
# present (~/.galaxy_eu_key), else the byte-comparable local `sep` fallback.
#
# Usage:
#   snakemake --cores 1            # run everything
#   snakemake --cores 1 -n         # dry run

NOTEBOOKS = "notebooks"
DATA = "data"
RESULTS = "results"
FIGURES = "figures"


rule all:
    input:
        f"{FIGURES}/main_result.png",
        f"{RESULTS}/biodiversity_metrics.json",


# ---------- 01: Data download (Black Marble night lights + Natura 2000) ----------
rule data_download:
    output:
        f"{DATA}/raw/sources.json",
    log:
        f"{RESULTS}/logs/01_data_download.log",
    shell:
        f"cd {{NOTEBOOKS}} && jupytext --to notebook --execute 01_data_download.py 2>&1 | tee ../{{log}}"


# ---------- 02: Data clean (-> single-channel raster for Source Extractor) ----------
rule data_clean:
    input:
        f"{DATA}/raw/sources.json",
    output:
        f"{DATA}/clean/po_delta_nightlights.tif",
    shell:
        f"cd {{NOTEBOOKS}} && jupytext --to notebook --execute 02_data_clean.py"


# ---------- 03: Source extraction (Galaxy or local sep fallback) ----------
rule analysis:
    input:
        f"{DATA}/clean/po_delta_nightlights.tif",
    output:
        f"{RESULTS}/extraction_summary.json",
    shell:
        f"cd {{NOTEBOOKS}} && jupytext --to notebook --execute 03_analysis.py"


# ---------- 04: Biodiversity overlay + figures ----------
rule figures:
    input:
        f"{RESULTS}/extraction_summary.json",
    output:
        f"{FIGURES}/main_result.png",
        f"{RESULTS}/biodiversity_metrics.json",
    shell:
        f"cd {{NOTEBOOKS}} && jupytext --to notebook --execute 04_figures.py"
