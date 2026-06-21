# 04 — FORRT Replication Study

> Run the pre-flight checklist in `docs/forrt-form-fields.md` § Pre-flight checklist before drafting. Method verified against `notebooks/01–04` + `scripts/source_extractor.py`.

## Field-by-field draft

### Short URI suffix for study ID (text input, required)

```
po-delta-sourceextractor-study
```

### Label/name of replication study (text input, required)

```
Astronomy Source Extractor applied to satellite night lights over the Po Delta
```

### Study type (dropdown, required)

- [ ] Reproduction Study — direct reproduction: same methodology, same tools.
- [x] Replication Study — replication with different methodology or conditions.
- [ ] Reproduction/Replication Study — both.

*Rationale: the Galaxy Source Extractor tool and its parameters are unchanged; the **conditions** differ — terrestrial satellite night-lights instead of astronomical sky images. Same tool, new data domain → Replication Study.*

### Search for a FORRT claim (search/select, required)

```
<paste Claim URI from PUBLISHED.md step 03 after publishing>
```

### Describe what part of the claim is reproduced/replicated (textarea, required)

Scope only — no method, no results.

```
Whether the astronomy source-extraction workflow, applied to satellite night-lights imagery of the Po Delta region, detects lit settlements as discrete sources and yields a measure of the extent of artificial light within the Po Delta Natura 2000 protected area. In scope: settlement detection and a light-extent metric for the Po Delta from a single annual VIIRS composite, plus the proximity of detected settlements to the protected area. Out of scope: temporal trends, species-level biodiversity impacts, comparison against a dedicated Earth-observation settlement product, and sub-pixel or low-radiance light.
```

### Describe how the claim is reproduced/replicated (textarea, required)

Method in plain prose — no result numbers.

```
A NASA Black Marble (VNP46A4) annual VIIRS night-lights composite over the eastern Po Valley / Po Delta (tile h19v04) was retrieved via earthaccess, the radiance band extracted and written as a single-channel GeoTIFF (water/dark background, bright settlements). This was run through the Galaxy astronomy "source-extractor" tool (astroteam/source_extractor_astro_tool, built on SEP) on usegalaxy.eu via BioBlend, at tool defaults: detection threshold 1.5x the global background RMS, minimum area 5 pixels, deblending (nthresh 32, cont 0.005), background mesh 64x64. The tool returns a source catalog (position, flux, shape), a segmentation map and a sources overlay. The catalog and the radiance field were overlaid on the EU Natura 2000 polygons (EEA): the light-extent metric is the fraction of Po Delta pixels with radiance above 1 nW/cm^2/sr, and nearby settlements are catalog sources within ~10 km of the protected area. A local SEP path reproduces the catalog for credential-free runs.
```

### Describe any deviations from original methodology (textarea, optional)

```
The Source Extractor tool is normally applied to astronomical sky images (FITS); here the input is a terrestrial satellite night-lights raster (GeoTIFF). Detection parameters are left at the tool defaults; no other changes were made to the tool or workflow.
```

### Search keywords (Wikidata) (multi-select, optional)

- light pollution
- protected area

### Search discipline (Wikidata) (search, optional)

- remote sensing

## Publication note

After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` step 04.
