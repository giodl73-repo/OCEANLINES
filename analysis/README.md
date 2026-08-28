# Heat-scale ledger

`heat_zone_ledger.py` converts either a water-volume temperature excess or a
sustained heat-transport rate into integrated energy and an ideal latent-melt
equivalent.

The result is an upper-bound unit conversion. It is not a heat-delivery model,
ice-sheet response model, or sea-level forecast.

```powershell
python heat_zone_ledger.py --volume-km3 1 --temperature-excess-c 1
python heat_zone_ledger.py --power-tw 1 --duration-days 365.25
python -m unittest test_heat_zone_ledger.py
```

Defaults are documented in `--help`; calculations use the Python standard
library only.

## OISST snapshot pipeline

`fetch_oisst_snapshot.py` retrieves a fixed NOAA/NCEI subset, validates its
rectangular grid, quantizes SST, anomaly, or estimated analysis error to integer
hundredths of a degree Celsius, and writes a compact browser artifact with query
and checksum provenance. The ERDDAP/CSV backend uses the standard library. The
NCSS/NetCDF backend used by the committed artifacts requires
`requirements-observations.txt`.

```powershell
python -m pip install -r ../requirements-observations.txt
python fetch_oisst_snapshot.py --backend ncss --date 2026-08-01 --stride 8 `
  --retrieved-at 2026-08-21T14:00:00Z `
  --output ../atlas/data/oisst-2026-08-01.js

python fetch_oisst_snapshot.py --backend ncss --variable anom `
  --date 2026-08-01 --stride 8 `
  --retrieved-at 2026-08-21T14:00:00Z `
  --output ../atlas/data/oisst-anomaly-2026-08-01.js

python fetch_oisst_snapshot.py --backend ncss --variable err `
  --date 2026-08-01 --stride 8 `
  --retrieved-at 2026-08-21T14:00:00Z `
  --output ../atlas/data/oisst-error-2026-08-01.js
```

## RG Argo pressure-layer pipeline

`fetch_argo_snapshot.py` packages one exact pressure level from a fixed monthly
Scripps RG Argo extension. The first committed layer is July 2026 potential-
temperature anomaly at 700 dbar, sampled from the native 1-degree grid at a
2-degree display stride. It preserves the compressed source checksum, product
version, baseline, grid extent, and missing values.

```powershell
python fetch_argo_snapshot.py `
  --month 2026-07 `
  --pressure-dbar 700 `
  --stride 2 `
  --retrieved-at 2026-08-28T19:02:31Z `
  --output ../atlas/data/argo-temperature-anomaly-700dbar-2026-07.js

python -m unittest test_argo_snapshot.py
```

This is an objectively mapped anomaly at one pressure surface. It is not raw
float coverage, absolute temperature, water-column heat content, or transport.
The product grid ends at 64.5°S, so it cannot diagnose Antarctic shelf or
ice-cavity heat delivery.
