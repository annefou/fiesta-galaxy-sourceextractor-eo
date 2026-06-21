# 06 — CiTO Citation

> Run the pre-flight checklist in `docs/forrt-form-fields.md` § Pre-flight checklist before drafting.

**Description:** *"Declare citations between papers or other works, using Citation Typing Ontology"*

## Field-by-field draft

### Identifier for the citing creative work (text input, required)

URI of the Outcome published in step 05.

```
<paste Outcome URI from PUBLISHED.md step 05 after publishing>
```

### List citations (repeatable group, required ≥1)

Question-rooted, descriptive chain (no prior paper to confirm/dispute), so the citations credit the reused method and the data sources.

#### Citation 1 — the reused method (Source Extractor / SEP)

##### Citation Type (dropdown)

```
credits
```

##### DOI or other URL of the cited work (text input)

```
https://doi.org/10.21105/joss.00058
```

#### Citation 2 — night-lights data source

##### Citation Type (dropdown)

```
citesAsDataSource
```

##### DOI or other URL of the cited work (text input)

```
https://ladsweb.modaps.eosdis.nasa.gov/missions-and-measurements/products/VNP46A4/
```

#### Citation 3 — protected-area data source

##### Citation Type (dropdown)

```
citesAsDataSource
```

##### DOI or other URL of the cited work (text input)

```
https://www.eea.europa.eu/en/datahub/datahubitem-view/6fc8ad2d-195d-40f4-bdec-576e7d1268e4
```

## Publication note

After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` step 06. This completes the six-step chain. The optional Research Software nanopub is in `drafts/07_research_software.md`.
