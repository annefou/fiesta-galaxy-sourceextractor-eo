# fiesta-galaxy-sourceextractor-eo

> **An astronomy source-detection tool, applied cross-discipline to Earth Observation.**
>
> Part of OSCARS-FIESTA. Reuses the Galaxy astronomy **Source Extractor** tool (SEP, [10.21105/joss.00058](https://doi.org/10.21105/joss.00058)).

Source Extractor — built to find stars and galaxies — is run **unchanged** through Galaxy on **NASA Black Marble** night lights to catalog lit **settlements**, then overlaid on **Natura 2000** to measure light-pollution pressure on the **Po Delta** biodiversity refuge. On a 2021 Po Valley scene it cataloged **453 settlements**; the Po Delta is still relatively dark (radiance 0.96 vs 4.11 region-wide) but 18.5% is already lit and 145 settlements press within ~10 km. This repository produces:

- A reproducible pipeline (Snakefile + notebooks), runnable on Galaxy or via a same-library local fallback.
- A Science Live nanopublication chain documenting the claim, method, and outcome with provenance.
- A Zenodo-archived release (source + container image) with a citable DOI.

## Quick start

```bash
git clone https://github.com/annefou/fiesta-galaxy-sourceextractor-eo.git
cd fiesta-galaxy-sourceextractor-eo
pixi install
pixi run snakemake --cores 1
```

Or with Docker:

```bash
docker run --rm ghcr.io/annefou/fiesta-galaxy-sourceextractor-eo:latest
```

## Structure

- `paper/` — the source paper PDF (drop yours in there).
- `notebooks/` — jupytext `.py` notebooks that drive the pipeline.
- `data/` — downloaded by `notebooks/01_data_download.py`, never committed.
- `nanopubs/` — drafts of the FORRT chain field-by-field, plus the published-URI registry.
- `docs/` — operating manuals (FORRT form fields, chain decision tree, claim-type vocabulary).
- `figures/` — curated figures used in the Jupyter Book.

## Nanopublication chain

The FORRT chain for this work is **published** on the Science Live platform (full registry in [`nanopubs/PUBLISHED.md`](nanopubs/PUBLISHED.md)):

1. **PCC question** — [RAEDNajh…](https://w3id.org/sciencelive/np/RAEDNajh8Hz_fZbBRgOACKDxWrQYFfDYRks8-xxMEfKt4)
2. **AIDA sentence** — [RAzhINAb…](https://w3id.org/sciencelive/np/RAzhINAbh6Mdx4UojSiL1Wa4DHWf1RGiOeHXmOwVQLwhw)
3. **FORRT Claim** — [RA2fQHXq…](https://w3id.org/sciencelive/np/RA2fQHXqmUHhYm46lrCjeXBQbX-h5uFBWo479kkgG5yO8)
4. **Replication Study** — [RAyA6pt4…](https://w3id.org/sciencelive/np/RAyA6pt4EhMD7hZBXAwLJtBjsLYaYZQsoafauxS5BXjWw)
5. **Replication Outcome** — [RA7zowzp…](https://w3id.org/sciencelive/np/RA7zowzpxWmmoRaFkRtc6xLUf395EYHMi0QwYAuQKtBAw)
6. **CiTO Citation** — [RAHqfGVv…](https://w3id.org/sciencelive/np/RAHqfGVvNBhwPzjKGWjr1GS-63nziwc1Jqt0cm9EEMgJE)
7. **Research Software** — [RA7KdUpn…](https://w3id.org/sciencelive/np/RA7KdUpnRo8yQAOS1ne3L06a6jVNZvRMRX2YIHpSlm5JY)

## Citation

If you use this work, please cite this software ([`CITATION.cff`](CITATION.cff), DOI minted on first release), plus the reused method — Source Extractor / SEP ([10.21105/joss.00058](https://doi.org/10.21105/joss.00058)).
