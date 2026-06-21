# 05 — FORRT Replication Outcome

> Run the pre-flight checklist in `docs/forrt-form-fields.md` § Pre-flight checklist before drafting. Numbers verified against `results/biodiversity_metrics.json` + `results/galaxy_provenance.json`.

## Field-by-field draft

### Short URI suffix for outcome ID (text input, required)

```
po-delta-light-intrusion-outcome
```

### Plain-text label for the outcome (text input, required)

```
Source Extractor catalogs 453 settlements; ~18.5% of the Po Delta is lit
```

### Search for a FORRT replication study (search/select, required)

```
<paste Study URI from PUBLISHED.md step 04 after publishing>
```

### Repository URL (text input, required)

```
https://github.com/annefou/fiesta-galaxy-sourceextractor-eo
```

### Completion date (date picker, required)

```
2026-06-21
```

### Validation status (dropdown, required)

- [x] Validated
- [ ] PartiallySupported
- [ ] Contradicted

*The astronomy tool successfully detects settlements from night lights and yields the light-extent measure; the descriptive claim (~18% of the Po Delta lit) holds.*

### Confidence level (dropdown, required)

```
Moderate
```

*One region, one annual composite; adequate evidence, single-method.*

### Describe the overall conclusion about the original claim (textarea, required)

```
An astronomy source-detection tool — Source Extractor (SExtractor / SEP) — run unchanged through Galaxy on VIIRS night lights, detects and catalogs lit settlements just as it catalogs stars, and turns that catalog into a biodiversity-impact measure. The Po Delta Natura 2000 protected area is darker than its surroundings (mean night radiance 0.96 vs 4.11 nW/cm^2/sr region-wide) and so remains a relative dark refuge, but artificial light already covers about 18.5 percent of its area and 145 detected settlements lie within roughly 10 km of it — a measurable encroachment of light pollution on a nocturnal-biodiversity wetland. This confirms the cross-discipline transfer: a FAIR, well-described Galaxy tool from astronomy does useful Earth-observation / biodiversity work without modification.
```

### Describe the evidence that supports your conclusion (textarea, required)

```
Po Delta / eastern Po Valley, NASA Black Marble VNP46A4 (VIIRS) 2021 annual composite (tile h19v04), run on usegalaxy.eu. Source Extractor cataloged 453 settlements region-wide (position, flux, size). Inside Natura 2000 sites the mean radiance is 1.34; inside the Po Delta it is 0.96, versus 4.11 region-wide. 18.5 percent of the Po Delta area exceeds 1 nW/cm^2/sr (lit); 145 cataloged settlements fall within ~10 km of the Po Delta. The Galaxy run and a local SEP reimplementation give the same catalog (453 settlements both ways). Provenance: results/galaxy_provenance.json (Galaxy history + parameters); figures/main_result.png.
```

### Describe what limits the conclusions of the study (textarea, optional)

```
This is a single annual snapshot, not a temporal trend, over one region. Night-lights radiance is a proxy for human presence and artificial-light exposure, not a direct biodiversity measurement, and "lit" uses a single 1 nW/cm^2/sr threshold. In the most intensely lit parts of the Po plain the background is no longer dark, so source detection there is less clean — the method works best at the refuge/city edge, like the Po Delta. Agreement between the Galaxy and local runs demonstrates reproducibility, not independent external validation, since both use the same SEP algorithm.
```

## Publication note

After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` step 05.
