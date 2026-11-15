# KPN groundwater memory — data and analytical code

This research archive supports the analysis of groundwater memory, drought characteristics and post-drought recovery in Kampinos National Park (KNP), Poland. It provides **monthly aggregated groundwater heads for 56 monitoring wells (January 1999–October 2025)**, metadata and archived quality flags, derived SGI and event records, three analytical notebooks, selected supplementary scripts and generated numerical outputs. The monthly input series preserve missing months and provider-flagged data. The original individual measurement records are held by KNP.

## Scope and reproducibility

The notebooks document construction of the Standardised Groundwater Index (SGI), estimation of groundwater memory, delineation of drought episodes and analysis of post-drought recovery and relapse as competing first outcomes. The scripts reproduce the primary cause-specific Cox models, Schoenfeld-residual screening, six-month time-split models, leave-one-well-out checks, spatial-block bootstrap and counts of drought runs eligible for post-drought follow-up. The numerical outputs include the results reported in Supplementary Tables S3–S5.

The archive supports reproduction of the principal analytical stages and selected sensitivity analyses. Some well-level resampling analyses and figure-production steps require additional code. The processed CSV files and saved outputs support independent checks of the reported results.

## Directory guide

- `data_input/` — monthly aggregated groundwater heads (`monthly_heads_m_asl.csv`), well metadata and provider quality flags.
- `data_processed/` — monthly SGI, groundwater memory, drought events and recovery-event records.
- `data_context/` — well coordinates (EPSG:2180) used for spatial calculations.
- `notebooks/01...03...` — notebooks for SGI and groundwater memory, drought-event metrics, and recovery and relapse.
- `scripts/` — executable Cox and selected sensitivity/eligibility analyses.
- `outputs/` — numerical outputs from the scripts, including results for Supplementary Tables S3–S5.
- `requirements.txt` — Python dependencies.

## Using the code

Install dependencies and start in the repository root:

```bash
python -m pip install -r requirements.txt
jupyter lab
```

Run notebooks `01`, `02`, and `03` in order where applicable. Selected scripts can be run separately:

```bash
python scripts/06_event_eligibility_bridge.py
python scripts/04_cox_diagnostics.py
python scripts/05_spatial_bootstrap.py --replicates 220
```

The scripts generate CSV outputs in `outputs/`. The spatial-block bootstrap assesses sensitivity of the adjusted cause-specific recovery hazard ratios to spatial clustering. It uses 4- and 8-km grid cells, two offsets at each grid size and 220 requested replicates per configuration. Cumulative incidence estimates the probability of recovery before relapse by a specified time. The cause-specific recovery hazard describes the instantaneous recovery rate among intervals still at risk of either outcome.

## Data origin and permitted use

**Source of groundwater monitoring data: Kampinos National Park (KNP), Poland.** Kampinos National Park confirmed that these public monitoring records could be redistributed with source attribution. Cite Kampinos National Park when using or redistributing the observations or their derivatives.

The MIT licence in `LICENSE` covers the original code and documentation. The monitoring records are subject to the source-attribution conditions above. The independent D/M/OUT classification was prepared using the project's GIS-derived context.

## Citing this archive

The archived release is available on Zenodo. Cite the archive and acknowledge Kampinos National Park as the source of the monitoring data.

Sawicka, K. (2026). *Groundwater memory and its relationship with multiscale drought persistence and recovery: Data and Python code* (v1.0.0). Zenodo. [https://doi.org/10.5281/zenodo.23662831](https://doi.org/10.5281/zenodo.23662831).
