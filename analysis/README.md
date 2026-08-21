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
rectangular grid, quantizes SST or anomaly to integer hundredths of a degree
Celsius, and writes a compact browser artifact with query and checksum
provenance. The ERDDAP/CSV backend uses the standard library. The NCSS/NetCDF
fallback requires `requirements-observations.txt`.

```powershell
python fetch_oisst_snapshot.py --date 2026-08-01 --stride 8 `
  --retrieved-at 2026-08-21T14:00:00Z `
  --output ../atlas/data/oisst-2026-08-01.js

python fetch_oisst_snapshot.py --backend ncss --variable anom `
  --date 2026-08-01 --stride 8 `
  --retrieved-at 2026-08-21T14:00:00Z `
  --output ../atlas/data/oisst-anomaly-2026-08-01.js
```
