# Atlas 01

Atlas 01 is the dependency-free interactive public surface for OCEANLINES. It
pairs the conceptual twelve-zone map with the first observational layer: NOAA
OISST v2.1 sea surface temperature for 1 August 2026.

Serve the repository root locally so relative links resolve:

```powershell
python -m http.server 8000
```

Then open `http://localhost:8000/atlas/`.

## Evidence status

Every displayed footprint and marker in the conceptual view is schematic. A
zone record declares its role, depth, clock, evidence class, source, and
inferential boundary. The observed view is a fixed daily surface analysis. It
is neither a live product nor a full-depth heat-content map.

## Rebuild the observed layer

The committed layer is a 2-degree display sampling of NOAA's native 0.25-degree
final product. Temperatures retain 0.01°C precision; land and missing cells are
preserved. The artifact records its exact query and source-response checksum.

```powershell
python analysis/fetch_oisst_snapshot.py `
  --date 2026-08-01 `
  --stride 8 `
  --retrieved-at 2026-08-21T14:00:00Z `
  --output atlas/data/oisst-2026-08-01.js
```

| Layer | Candidate source | What it may show | What it may not establish |
|---|---|---|---|
| surface temperature | NOAA OISST v2.1 | **implemented:** spatially complete daily SST field | full-depth heat content |
| subsurface temperature/salinity | Argo gridded products | vertical water-column structure | unsampled fine-scale pathways |
| surface current | NASA PO.DAAC OSCAR | mixed-layer velocity estimate | full-depth heat transport |
| dynamically consistent state | ECCO v4r4 | modeled/assimilated budgets and transports | observation-only truth |
| bathymetry and gates | GEBCO grid | geometric constraints and section context | circulation by itself |
| sea ice | NOAA/NSIDC CDR | polar ice concentration | subsurface ocean heat delivery |

Any observational release must name the product version, retrieval date,
temporal aggregation, depth support, baseline, transformation code, and license.
