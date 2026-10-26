# KPN groundwater memory — data and analytical code (repository v3)

This research archive supports the analysis of groundwater memory, drought characteristics and post-drought recovery in Kampinos National Park (KPN), Poland. It provides **monthly aggregated groundwater heads for 56 monitoring wells (January 1999–October 2025)**, metadata and archived quality flags, derived SGI and event records, three analytical notebooks, selected supplementary scripts and generated numerical outputs. The monthly input series preserve missing months and provider-flagged data; the archive is not a replacement for the original individual measurement records held by KPN.

## Scope and reproducibility

The notebook and script collection documents and supports reproduction of **principal analytical stages and selected supplementary sensitivity analyses**, rather than offering an end-to-end automated rebuild of every figure, table, permutation test and uncertainty estimate in the paper. The processed CSV files and saved outputs are included both to support checks and to make the reported intermediate and supplementary results accessible without rerunning computational procedures. **A saved output is not, by itself, evidence that every analysis in the article can be reproduced from this archive.**

The original three notebooks are retained unchanged from v2. The scripts added in v3 support the primary cause-specific Cox fits, diagnostic screening, six-month time-split models, leave-one-well-out checks, the spatial-block Cox bootstrap and the reconciliation of drought-event eligibility. Other reported analyses, including the archived exploratory AR(1) pilot, certain well-level bootstrap/permutation tests and some cartographic products, are **not fully reproducible using the supplied code**. In particular, the legacy AR(1) pilot was not recalibrated for the current SGI implementation.

## Directory guide

- `data_input/` — monthly aggregated groundwater heads (`monthly_heads_m_asl.csv`), well metadata and provider quality flags.
- `data_processed/` — monthly SGI, groundwater memory, drought events and recovery-event records.
- `data_context/` — well coordinates (EPSG:2180) used for spatial calculations.
- `notebooks/01...03...` — reference analyses for SGI/memory, drought-event metrics and competing-outcome recovery.
- `scripts/` — executable Cox and selected sensitivity/eligibility analyses.
- `outputs/` — archived numeric results from those scripts (including S3–S5 support tables); these files are retained intentionally.
- `requirements.txt` — Python dependencies; `AUDIT_V3.md` — description of analytical checks and qualifications.

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

The scripts generate CSV outputs in `outputs/`. Spatial bootstrap uses well-level blocks, four- and eight-kilometre grids with two offsets and a fixed random seed, with 220 requested replicates per configuration; its purpose is sensitivity to spatial clustering, not physical attribution. Cox hazard ratios and cumulative incidence estimates describe different estimands and must not be equated.

## Data origin and permitted use

**Source of groundwater monitoring data: Kampinos National Park (KPN), Poland.** KPN confirmed by email that no separate written authorization was required to share these public monitoring data, provided the source was acknowledged. Cite the original provider when using or redistributing the observations or derivatives. The precise wording and scope of that confirmation should be retained in project records; this README does not purport to grant rights beyond the provider's terms.

The `LICENSE` file applies to **original code and documentation only**, not automatically to the underlying KPN monitoring data. The independent D/M/OUT classification was prepared using the project's GIS-derived context.

## Citing this archive

Cite the associated research article, Kampinos National Park as the monitoring-data source, and the persistent archive DOI **once assigned**. No DOI is asserted here before deposit. This is the clarified-scope distribution of v3; source data and numerical outputs have not been recalculated or altered.
