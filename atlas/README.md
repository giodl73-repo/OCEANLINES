# Atlas 03

Atlas 03 separates four views: the conceptual twelve-zone geography, absolute
NOAA OISST v2.1 sea surface temperature, NOAA's published SST anomaly, and its
time-matched estimated analysis error for 1 August 2026.

Serve the repository root locally so relative links resolve:

```powershell
python -m http.server 8000
```

Then open `http://localhost:8000/atlas/`.

## Evidence status

Every displayed footprint and marker in the conceptual view is schematic. A
zone record declares its role, depth, clock, evidence class, source, and
inferential boundary. The observed views are fixed daily surface analyses.
Neither is a live product or a full-depth heat-content map. The anomaly is
relative to NOAA's 1971–2000 climatology; it is not absolute temperature.
The anomaly palette is centered at zero and clamped symmetrically at ±5°C;
the details panel reports the unclamped sampled range.
The error layer is an OISST product field, not forecast error, a confidence
interval, or uncertainty in full-depth heat content.

Observed fields use an equirectangular display centered on 0° longitude, with
the antimeridian at the left/right seam. A non-color table reports mean, range,
and valid-cell count for five latitude bands. Those summaries are not
area-weighted and do not replace local inspection.

## Rebuild the observed layer

The committed layer is a 2-degree display sampling of NOAA's native 0.25-degree
final product. Temperatures retain 0.01°C precision; land and missing cells are
preserved. The artifact records its exact query and source-response checksum.

```powershell
python -m pip install -r requirements-observations.txt
python analysis/fetch_oisst_snapshot.py `
  --backend ncss `
  --variable sst `
  --date 2026-08-01 `
  --stride 8 `
  --retrieved-at 2026-08-21T14:00:00Z `
  --output atlas/data/oisst-2026-08-01.js

python analysis/fetch_oisst_snapshot.py `
  --backend ncss `
  --variable anom `
  --date 2026-08-01 `
  --stride 8 `
  --retrieved-at 2026-08-21T14:00:00Z `
  --output atlas/data/oisst-anomaly-2026-08-01.js

python analysis/fetch_oisst_snapshot.py `
  --backend ncss `
  --variable err `
  --date 2026-08-01 `
  --stride 8 `
  --retrieved-at 2026-08-21T14:00:00Z `
  --output atlas/data/oisst-error-2026-08-01.js
```

| Layer | Candidate source | What it may show | What it may not establish |
|---|---|---|---|
| surface temperature | NOAA OISST v2.1 | **implemented:** spatially complete daily SST field | full-depth heat content |
| surface anomaly | NOAA OISST v2.1 | **implemented:** departure from 1971–2000 daily climatology | absolute temperature, heat content, or cause |
| estimated analysis error | NOAA OISST v2.1 | **implemented:** spatial variation in time-matched surface analysis uncertainty | forecast error, confidence interval, or full-budget uncertainty |
| subsurface temperature/salinity | Argo gridded products | vertical water-column structure | unsampled fine-scale pathways |
| surface current | NASA PO.DAAC OSCAR | mixed-layer velocity estimate | full-depth heat transport |
| dynamically consistent state | ECCO v4r4 | modeled/assimilated budgets and transports | observation-only truth |
| bathymetry and gates | GEBCO grid | geometric constraints and section context | circulation by itself |
| sea ice | NOAA/NSIDC CDR | polar ice concentration | subsurface ocean heat delivery |

Any observational release must name the product version, retrieval date,
temporal aggregation, depth support, baseline, transformation code, and license.
All three committed OISST artifacts conform to
`oceanlines.oisst.snapshot.v2` and retain source-response SHA-256 checksums.
