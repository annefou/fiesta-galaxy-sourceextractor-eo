# 07 — Research Software (optional layer)

> Run the pre-flight checklist in `docs/forrt-form-fields.md` § Pre-flight checklist before drafting.
>
> **Scope note:** the reusable artefact is the **parameterised Galaxy night-lights → settlements → biodiversity-overlay pipeline plus its BioBlend driver** (`scripts/source_extractor.py` + notebooks) — others can `git clone` it and point the same astronomy Source Extractor workflow at their own region / night-lights scene / protected-area layer. The upstream tool (SEP) and the Galaxy tool are credited separately at the CiTO step.

**Form heading:** *"Research Software — Describe research software with metadata including repository, supporting publications, and related resources."*

## Field-by-field draft

### URI of published software (text input, required)

Zenodo concept DOI (minted at the v0.1.0 release).

```
https://doi.org/10.5281/zenodo.20784962
```

### Software Title (text input, required)

```
FIESTA — Galaxy Source-Extractor pipeline for night-lights settlement detection and light-pollution biodiversity overlay
```

### Repository URL (text input, required)

```
https://github.com/annefou/fiesta-galaxy-sourceextractor-eo
```

### Research Project (text input, optional)

Back-link to the FORRT Claim at the head of the chain.

```
<paste Claim URI from PUBLISHED.md step 03 after publishing>
```

### License (text input, optional)

```
https://spdx.org/licenses/MIT.html
```

### Related Datasets (repeatable group, optional)

- https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/products/VNP46A4/
- https://www.eea.europa.eu/en/datahub/datahubitem-view/6fc8ad2d-195d-40f4-bdec-576e7d1268e4

### Related Publications (repeatable group, optional)

- `<paste Outcome URI from PUBLISHED.md step 05 after publishing>` (the FORRT Outcome this software implements)
- https://doi.org/10.21105/joss.00058 (SEP — the reused source-extraction method)

## Publication note

After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` step 07.
