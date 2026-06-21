# 02 — AIDA Sentence

> Run the pre-flight checklist in `docs/forrt-form-fields.md` § Pre-flight checklist before drafting.

**Form heading:** *"AIDA Sentence — Make structured scientific claims following the AIDA model"*

## Field-by-field draft

### AIDA sentence (textarea, required)

Atomic, Independent, Declarative, Absolute. One empirical finding. Ends with a full stop.

```
Artificial night-time light is present over approximately 18 percent of the Po Delta Natura 2000 protected area.
```

### Select related topics/tags (dropdown, optional)

Intended labels (pick from the platform vocabulary if present):

```
light pollution; remote sensing; protected areas
```

### Relates to this nanopublication (text input, required)

URI of the PCC question published in step 01.

```
<paste PCC URI from PUBLISHED.md step 01 after publishing>
```

### Supported by datasets (repeatable group, optional)

- NASA Black Marble VNP46A4 (VIIRS night lights): https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/products/VNP46A4/
- Natura 2000 (EU protected areas, EEA): https://www.eea.europa.eu/en/datahub/datahubitem-view/6fc8ad2d-195d-40f4-bdec-576e7d1268e4

### Supported by other publications (repeatable group, optional)

- SEP: Source Extraction and Photometry (Barbary 2016): https://doi.org/10.21105/joss.00058

> The earlier platform bug with both groups populated is fixed (2026-06-21).

## Publication note

After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` step 02.
