# Atlas 06

Atlas 06 separates four views: the conceptual twelve-zone geography, absolute
NOAA OISST v2.1 sea surface temperature, NOAA's published SST anomaly, and its
time-matched estimated analysis error for 1 August 2026. It adds a coordinate
probe that reports all three observed fields at the nearest display-grid cell
and a paired latitude-ring comparison that exposes analyzed-water continuity
north and south at one requested latitude magnitude. A latitude ladder extends
that comparison across 45 paired requests from 0° through 88°.

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

## Inspect a location

Click an observed map or enter latitude and longitude in the probe form. The
atlas snaps the request to the nearest two-degree display cell, marks that cell,
and reports absolute SST, referenced anomaly, and estimated analysis error
together. Land and missing values remain explicit.

Probe selections are bookmarkable:

```text
?mode=anomaly&lat=-63.875&lon=-59.875
```

The reported coordinates describe the sampled display cell, not the exact
pointer coordinate or NOAA's full native-resolution grid. All values remain
surface-product fields; the probe does not calculate heat content or transport.

## Compare polar rings

Choose a latitude magnitude to trace the active surface field across every
display longitude at both the northern and southern counterpart. Atlas 05
draws the two sampled rows on the map, renders longitude strips, and reports
valid SST-mask coverage, the number of separated water arcs, the longest
continuous water arc, and field statistics in text.

The default request of 64° snaps to the nearest available display rows:
64.125°N and 63.875°S. On the fixed snapshot, the northern row contains 46
ocean cells in seven arcs and the southern row contains 179 ocean cells in one
cyclic arc. The longest arcs are 28° and 358° of longitude respectively. These
are two-degree display-grid geometry diagnostics, not coast-resolution
estimates. The source mask combines land and missing values, so the atlas does
not assign a cause to every individual gap.

Ring selections are bookmarkable with `ring=64.000`. Analyzed-water continuity can
help explain why circumpolar geometry is possible in the south and interrupted
in the north, but this surface snapshot does not measure the ACC, frontal
barrier strength, heat content, or heat transport.

## Scan the latitude ladder

Atlas 06 plots canonical SST-mask coverage for every even requested latitude
magnitude from the equator through 88°. Northern rows use a solid line;
southern rows use a dashed line. The selected polar-ring request is marked on
the chart, and the complete 45-pair result is available as a semantic table.

For a declared diagnostic threshold of at least 95% analyzed-water coverage
and a longest cyclic water arc of at least 300° longitude, the first southern
scan match is the 48° request (47.875°S) and the first northern match is the 84°
request (84.125°N). The high-latitude northern result reflects the central
Arctic Ocean; the southern curve returns to zero over the Antarctic interior.
This threshold is not a coastline estimate, ACC edge, front, current boundary,
or transport diagnostic.

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
