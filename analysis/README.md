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
