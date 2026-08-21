# Contributing

OCEANLINES welcomes corrections, source improvements, map concepts, and
reproducible data layers.

Every contribution should preserve these boundaries:

- distinguish temperature, heat content, anomaly, and transport;
- declare depth, time interval, spatial support, and reference state;
- identify each artifact as conceptual, observational, modeled, or quantitative;
- cite the source supporting each scientific claim;
- state what the cited evidence cannot establish;
- keep surface products separate from full-depth inference;
- allow negative, regional, non-transfer, and observationally unresolved results.

Run the local checks before proposing a change:

```powershell
cd analysis
python -m unittest test_heat_zone_ledger.py
python -m py_compile heat_zone_ledger.py test_heat_zone_ledger.py
```

SVG figures must contain a `<title>` and `<desc>` accessibility element and
must remain legible at their declared view-box size.
