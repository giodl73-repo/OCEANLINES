# OSW project history

This record preserves changes in the project's way of seeing the ocean, not
only software releases. Atlas version status remains in `README.md` and
`PREVIEW-STATUS.md`.

## 2026-08-29 — Ocean States of the World

After the 56-state surface geography and 36 overlapping feature systems became
the center of the work, **OCEANLINES** no longer described the project: lines
were only one kind of ocean object. The project was renamed **OSW — Ocean
States of the World**. In ordinary conversation it may be called **The Ocean
States**.

The new name preserves the project's central map idea: ocean states can be
learned like the states on a familiar political map, while waters, currents,
fronts, seafloor structures, living systems, and events cross and overlap
them. “States” remains a visual and organizational analogy, not a claim that
the approximate provinces are sovereign, fixed, exhaustive through depth, or
published Longhurst boundary geometry.

Active code, artifacts, metadata, and interface branding use `OSW` and the
`osw-` filename prefix. Dated reviews below retain the former project name when
describing work performed before the rename.

The reviewed `atlas-08-private-preview` branch was subsequently pushed at the
owner's request. It is publicly visible for review but has not replaced Atlas
07 on `main` or GitHub Pages and is not a promoted release.

## 2026-08-29 — The ocean becomes a place

### The breakthrough

OCEANLINES found a complete surface geography: the classic Longhurst system of
four biomes and 56 named biogeochemical provinces. This changed the project from
an atlas of selected heat reservoirs, currents, fronts, and events into a map on
which **every surface-ocean location can first have a province identity**.

The owner recognized this as a hallmark moment. The central analogy became:

> The 56 provinces can be learned like states, while heatmasses, currents,
> fronts, blooms, and events cross them like larger moving systems.

### What was built

- `38c9352` identified Longhurst-style provinces as the strongest available
  complete surface cover.
- `9df16e7` created the first Province Atlas: an original state-like cartogram,
  a 56-row reference directory, and an explicit 54/56 edition boundary.
- `9ea0281` approved the first cartogram as an additive private experiment.
- `495ec4b` replaced decorative land seams with horizontally compressed,
  checksum-pinned Natural Earth coastlines—real continental fingerprints that
  orient the viewer without returning visual control to land.
- `2327cec` made the inversion literal in a monochrome state-map study:
  continents became negative-space holes cut directly from the unified province
  field, while the earlier four-biome plate remained preserved.

### What the first map means

The province identities, codes, basin memberships, and biomes are scientific
reference facts. The equal-ish beveled province shapes are not geographic
Longhurst boundaries and do not encode real area, distance, direction, exact
adjacency, or exact coast contact. That separation is now a permanent project
contract: **identity can be simplified; geometry must declare its truth.**

### The visual promise

The mature Province Atlas should hold two complementary truths:

1. **Equal voice** — a varied, contiguous puzzle cartogram in which every
   province has room to be recognized and remembered.
2. **True footprint** — a licensed or independently reproducible geographic
   reference in which province size, shape, contact, and uncertainty can be
   inspected honestly.

The intended hook is a stable code and color system that can move between those
views. The static Longhurst reference is only the beginning: natural ecological
boundaries move seasonally and interannually.

## 2026-08-29 — The provinces become the atlas

### The second breakthrough

The first state-map experiments still treated coastlines as decoration or as a
single hole punched through unrelated tiles. The owner supplied the decisive
correction: **the coastline must belong to the province itself**. ALSK should
inherit a recognizable Alaska edge; HUMB should inherit Peru and Chile; BENG
should inherit southwest Africa.

`ef5f37a` rebuilt the 56 pieces from approximate geographic seeds over a
complete ocean field and subtracted checksum-pinned Natural Earth land from
them. The internal borders remain original schematic geometry, but every
coast-facing piece now owns the real coastline it reaches. Continents became
the lakes inside the ocean-state map.

`a72074d` then made that geometry the common Atlas 10 ground. All six conceptual
lenses and the SST, SST-anomaly, Argo-depth-anomaly, and estimated-error modes
can be read without leaving the 56-state system. Every province is selectable,
keyboard operable, URL-addressable, and zoomable; changing views preserves the
selected geographic frame.

`96c2b91` replaced the 36 numbered point markers with selectable geographic
shapes. Established OCEANLINES artwork supplies the first heatmasses, currents,
gates, and buried waters; mechanism-specific regions, loops, seams, and seafloor
paths complete the catalog. The shapes remain declared schematic indexes—not
observed boundaries—but the map can now show what kind of ocean object crosses
each province instead of reducing every object to the same dot.

The durable interaction principle is:

> Select a province as the place. Then change the view to ask what waters,
> flows, edges, life, events, or observations cross that place.

This is still a reference cartogram—not validated Longhurst boundary geometry
and not a mechanism, budget, or material wall.
