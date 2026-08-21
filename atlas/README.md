# Atlas 00

Atlas 00 is the dependency-free interactive public surface for OCEANLINES. It
uses the conceptual map and a structured twelve-zone catalog to demonstrate the
map grammar before observational rasters are introduced.

Serve the repository root locally so relative links resolve:

```powershell
python -m http.server 8000
```

Then open `http://localhost:8000/atlas/`.

## Evidence status

Every displayed footprint and marker is conceptual. A zone record declares its
role, depth, clock, evidence class, source, and inferential boundary. The atlas
does not download live data and makes no present-day forecast.

| Layer | Candidate source | What it may show | What it may not establish |
|---|---|---|---|
| surface temperature/anomaly | NOAA OISST v2.1 | spatially complete daily SST field | full-depth heat content |
| subsurface temperature/salinity | Argo gridded products | vertical water-column structure | unsampled fine-scale pathways |
| surface current | NASA PO.DAAC OSCAR | mixed-layer velocity estimate | full-depth heat transport |
| dynamically consistent state | ECCO v4r4 | modeled/assimilated budgets and transports | observation-only truth |
| bathymetry and gates | GEBCO grid | geometric constraints and section context | circulation by itself |
| sea ice | NOAA/NSIDC CDR | polar ice concentration | subsurface ocean heat delivery |

Any observational release must name the product version, retrieval date,
temporal aggregation, depth support, baseline, transformation code, and license.
