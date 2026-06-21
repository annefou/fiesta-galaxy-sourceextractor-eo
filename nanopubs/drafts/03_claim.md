# 03 — FORRT Claim

> Run the pre-flight checklist in `docs/forrt-form-fields.md` § Pre-flight checklist before drafting.

**Form heading:** *"FORRT Claim — Declare an original claim according to FORRT, linking it to an AIDA sentence with a specific FORRT type."*

## Field-by-field draft

### Short URI suffix as claim ID (text input, required)

```
po-delta-light-intrusion
```

### Label of the claim (text input, required)

```
Light-pollution intrusion on the Po Delta protected area
```

### Search for an AIDA sentence (search/select, required)

URI of the AIDA published in step 02.

```
<paste AIDA URI from PUBLISHED.md step 02 after publishing>
```

### Type of FORRT claim (dropdown, required)

See `docs/claim-type-vocabulary.md`.

- [ ] computational performance
- [ ] scalability
- [ ] data quality
- [ ] data governance
- [x] descriptive pattern
- [ ] model performance
- [ ] statistical significance

*Rationale: the claim asserts an observed empirical fact about the world — the extent of artificial light over a protected area — which is a `descriptive pattern` (the source-extraction tool is the instrument; the pattern is the claim).*

### Source URI (text input, optional)

Full URL form.

```
https://github.com/annefou/fiesta-galaxy-sourceextractor-eo
```

## Publication note

After publishing, paste the resulting URI into `nanopubs/PUBLISHED.md` step 03.
