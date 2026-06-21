# fiesta-galaxy-sourceextractor-eo

[![CI](https://github.com/annefou/fiesta-galaxy-sourceextractor-eo/actions/workflows/ci.yml/badge.svg)](https://github.com/annefou/fiesta-galaxy-sourceextractor-eo/actions/workflows/ci.yml)
[![Jupyter Book](https://github.com/annefou/fiesta-galaxy-sourceextractor-eo/actions/workflows/jupyter-book.yml/badge.svg)](https://annefou.github.io/fiesta-galaxy-sourceextractor-eo/)
[![Docker](https://github.com/annefou/fiesta-galaxy-sourceextractor-eo/actions/workflows/docker.yml/badge.svg)](https://github.com/annefou/fiesta-galaxy-sourceextractor-eo/pkgs/container/fiesta-galaxy-sourceextractor-eo)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20784962.svg)](https://doi.org/10.5281/zenodo.20784962)
[![FAIR4RS](https://img.shields.io/badge/FAIR4RS-conformant-brightgreen)](docs/fair4rs-checklist.md)
[![FORRT](https://img.shields.io/badge/FORRT-replication-blue)](https://forrt.org/)
[![Science Live](https://img.shields.io/badge/Science%20Live-nanopub%20chain-purple)](nanopubs/PUBLISHED.md)
[![RO-Crate](https://img.shields.io/badge/RO--Crate-1.2-orange)](ro-crate-metadata.json)
[![Software Heritage](https://archive.softwareheritage.org/badge/origin/https://github.com/annefou/fiesta-galaxy-sourceextractor-eo/)](https://archive.softwareheritage.org/browse/origin/?origin_url=https://github.com/annefou/fiesta-galaxy-sourceextractor-eo)

> **An astronomy source-detection tool, applied cross-discipline to Earth Observation.**
> Source Extractor (SExtractor / [SEP](https://doi.org/10.21105/joss.00058)) — built to find stars and galaxies — run **unchanged** through Galaxy on satellite **night lights** to catalog lit settlements, then used to measure light-pollution pressure on a **Natura 2000** biodiversity refuge.

Part of **OSCARS-FIESTA** (cross-image analysis *with Galaxy*) — a companion to [fiesta-galaxy-bioimageio-eo](https://github.com/annefou/fiesta-galaxy-bioimageio-eo). This is **not** a replication of a paper: it reuses the Galaxy astronomy **Source Extractor** tool (built on SEP, [Barbary 2016](https://doi.org/10.21105/joss.00058)) and applies it to Earth-observation data, producing a reproducible pipeline, a Zenodo-archived release with a citable DOI, and a Science Live nanopublication chain.

## Result

On a 2021 **NASA Black Marble** (VIIRS) night-lights scene of the **Po Valley / Po Delta** (Italy), Source Extractor — run on **usegalaxy.eu** — cataloged **453 lit settlements** (position, brightness, size). Overlaid on **Natura 2000**, this quantifies light-pollution intrusion on the **Po Delta**, a Ramsar/Natura 2000 migratory-bird wetland: the refuge is still relatively dark (mean radiance **0.96** vs **4.11** region-wide), but **18.5% of it is already lit** and **145 settlements press within ~10 km**. Artificial light at night is a documented stressor for nocturnal birds, insects, and bats — so this turns an astronomy catalog into a biodiversity-impact metric.

![Light pollution at the edge of a dark refuge](figures/main_result.png)

## Two ways to run — Galaxy first

This repo foregrounds the **Galaxy** path (FIESTA is about cross-image analysis *with Galaxy*):

- **Galaxy (showcased):** `notebooks/03_analysis.py` runs the astronomy [`source_extractor_astro_tool`](https://usegalaxy.eu/?tool_id=toolshed.g2.bx.psu.edu/repos/astroteam/source_extractor_astro_tool/source_extractor_astro_tool/0.0.1+galaxy0) on **usegalaxy.eu** via BioBlend (needs a usegalaxy.eu API key at `~/.galaxy_eu_key`).
- **Local fallback (CI / hermetic):** the *same library* offline (`sep`, which the Galaxy tool wraps) — gives the same catalog (453 settlements both ways) — so the Jupyter Book builds without a key.

---

## Quick start

```bash
git clone https://github.com/annefou/fiesta-galaxy-sourceextractor-eo.git
cd fiesta-galaxy-sourceextractor-eo
pixi install
pixi run snakemake --cores 1
```

(Pixi resolves `pixi.toml` against the per-platform `pixi.lock`, installs the env under `.pixi/`, and provides `pixi run` for any task without needing an `activate` step.)

Or with Docker:

```bash
docker run --rm ghcr.io/annefou/fiesta-galaxy-sourceextractor-eo:latest
```

The Jupyter Book version is at <https://annefou.github.io/fiesta-galaxy-sourceextractor-eo/>.

## Built from a template

This repository was created from [`sciencelivehub/forrt-replication-template`](https://github.com/sciencelivehub/forrt-replication-template). The template ships an operating manual for AI assistants ([`CLAUDE.md`](CLAUDE.md), [`AGENTS.md`](AGENTS.md)), domain conventions ([`DOMAIN.md`](DOMAIN.md)), and reference docs (`docs/`) so that an AI working only inside this repository can guide a researcher from "paper PDF + GitHub repo" to "published FORRT chain + Zenodo DOI" with no other context.

If you are reading this in a fresh fork, run [`/init-template`](.claude/skills/init-template/SKILL.md) inside Claude Code to substitute the placeholder tokens with your details. (For other AI tools, see [`docs/ai-portability.md`](docs/ai-portability.md).)

After `/init-template`, do these one-time setup steps to enable the full CI/CD path:

- **Enable GitHub Pages** at *Settings → Pages → Source: GitHub Actions*. Until enabled, the Jupyter Book build runs but the deploy step is skipped (CI stays green).
- All three workflows share one **readiness guard** (`.github/actions/check-ready`). Before `/init-template` runs, the `.template-uninitialised` sentinel makes them skip with an informative `::notice::` (badges stay green); `/init-template` deletes the sentinel, which activates them. They also skip while `notebooks/*.py` are still scaffolds (Phase 2). **Once you've published a nanopub chain** (real URIs in `nanopubs/PUBLISHED.md`), a skip is treated as a bug and **fails the run loudly** — so a finished replication can't sit on silently-green-but-empty CI.

## Repository structure

```
.
├── CLAUDE.md / AGENTS.md       # operating manual for AI assistants
├── DOMAIN.md                   # domain flavour (current: biodiversity + earth observation)
├── USER_PREFERENCES.md         # per-user style (edit on first clone)
├── README.md                   # this file
├── LICENSE                     # MIT
├── CITATION.cff                # how to cite
├── codemeta.json               # software metadata (CodeMeta-2.0)
├── ro-crate-metadata.json      # research object packaging (RO-Crate 1.2)
├── pixi.toml + pixi.lock       # pinned dependencies (single source of truth; lockfile is per-platform)
├── Dockerfile                  # container build
├── Snakefile                   # pipeline orchestration
├── myst.yml + index.md         # Jupyter Book scaffold
├── paper/                      # the source paper PDF
├── data/                       # downloaded artefacts (gitignored)
├── notebooks/                  # jupytext .py pipeline (01–04)
├── nanopubs/                   # FORRT chain drafts + published-URI registry
├── docs/                       # reference material
├── figures/                    # curated figures used in the Jupyter Book
├── .github/workflows/          # CI, Jupyter Book, Docker
└── .claude/                    # Claude Code agents, skills, sandbox config
```

## What you get

This template bakes in conventions that took multiple replications to discover. By using it, you inherit:

- **FAIR4RS conformance** — see [`docs/fair4rs-checklist.md`](docs/fair4rs-checklist.md) for the principle-by-principle mapping.
- **Self-contained data downloads** — the first notebook fetches everything; no manual data prep.
- **`pixi.toml` + `pixi.lock` as single source of truth** — local dev, Docker, and CI all install the same per-platform-pinned env.
- **`prefix-dev/setup-pixi`-based CI** — caches the env, runs the pipeline with `pixi run`, executes notebooks via a glob, fails fast on a stale lockfile.
- **Jupyter Book deployment** — auto-deploys to GitHub Pages with `BASE_URL` set correctly. (Don't put `base_url` in `myst.yml` — MyST silently ignores it.)
- **Docker + GHCR + Zenodo image archival** — `release` trigger pushes to GHCR and (optionally) archives to Zenodo for long-term preservation.
- **RO-Crate packaging** — the entire repo is a navigable Research Object via `ro-crate-metadata.json` (Process Run Crate + Workflow RO-Crate profiles).
- **Six-step FORRT chain workspace** — `nanopubs/drafts/` has a field-by-field skeleton for each step. `nanopubs/PUBLISHED.md` is the URI registry.
- **Layered AI guidance** — `CLAUDE.md` (universal) + `DOMAIN.md` (swappable per field) + `USER_PREFERENCES.md` (per-user). See [`docs/ai-portability.md`](docs/ai-portability.md) for non-Claude AI tools.
- **Sandbox by default** — `.claude/settings.json` denies file ops outside the repo, so a fresh AI session can't accidentally read `~/.ssh/` or write to `/etc/`.

## FORRT nanopublication chain — published

This work's FORRT chain is **published** on [platform.sciencelive4all.org](https://platform.sciencelive4all.org) (question-rooted, descriptive: PCC → AIDA → Claim → Study → Outcome → CiTO). Full registry in [`nanopubs/PUBLISHED.md`](nanopubs/PUBLISHED.md):

| Step | Nanopub |
|---|---|
| PCC question | [RAEDNajh…](https://w3id.org/sciencelive/np/RAEDNajh8Hz_fZbBRgOACKDxWrQYFfDYRks8-xxMEfKt4) |
| AIDA sentence | [RAzhINAb…](https://w3id.org/sciencelive/np/RAzhINAbh6Mdx4UojSiL1Wa4DHWf1RGiOeHXmOwVQLwhw) |
| FORRT Claim | [RA2fQHXq…](https://w3id.org/sciencelive/np/RA2fQHXqmUHhYm46lrCjeXBQbX-h5uFBWo479kkgG5yO8) |
| Replication Study | [RAyA6pt4…](https://w3id.org/sciencelive/np/RAyA6pt4EhMD7hZBXAwLJtBjsLYaYZQsoafauxS5BXjWw) |
| Replication Outcome | [RA7zowzp…](https://w3id.org/sciencelive/np/RA7zowzpxWmmoRaFkRtc6xLUf395EYHMi0QwYAuQKtBAw) |
| CiTO Citation | [RAHqfGVv…](https://w3id.org/sciencelive/np/RAHqfGVvNBhwPzjKGWjr1GS-63nziwc1Jqt0cm9EEMgJE) |
| Research Software | [RA7KdUpn…](https://w3id.org/sciencelive/np/RA7KdUpnRo8yQAOS1ne3L06a6jVNZvRMRX2YIHpSlm5JY) |

Optional further layers:

- **Research Software nanopub** — for reusable upstream tools (not demo repos). See [`docs/forrt-form-fields.md`](docs/forrt-form-fields.md) § Research Software.
- **Research Synthesis nanopub** — when this chain is part of a multi-chain story. See [`docs/forrt-form-fields.md`](docs/forrt-form-fields.md) § Research Synthesis.

## After publishing

When the chain is live and the FAIR4RS checklist is green, drafting an announcement post is the next step. See [`docs/announcement-template.md`](docs/announcement-template.md) for the structural template (vision-piece-first; the worked replication is the payoff, not the lead).

For lower-level nanopub work — retraction, superseding, batch publishing — see [`docs/programmatic-nanopubs.md`](docs/programmatic-nanopubs.md).

## Citation

If you use this work, please cite both:

- This software: [`CITATION.cff`](CITATION.cff) → concept DOI minted on first release.
- The reused method: Source Extractor / SEP — [10.21105/joss.00058](https://doi.org/10.21105/joss.00058).
- Data: NASA Black Marble (VIIRS night lights) and Natura 2000 (European Environment Agency).

## Acknowledgements

This repository was built from [`sciencelivehub/forrt-replication-template`](https://github.com/sciencelivehub/forrt-replication-template), part of the [Science Live platform](https://platform.sciencelive4all.org). The template is licensed MIT and contributions (especially new domain flavours under [`docs/domain-flavours/`](docs/domain-flavours/)) are welcome.
