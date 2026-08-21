---
skill: roles-check
topic: atlas-07-polar-mirrors
date: 2026-08-21
reviewed_atlas_commit: 666c2b3
role_set_commit: 262f3e7
role_set: .roles/ROLE.md
roles_used: 8
p1_count: 0
p2_count: 0
verdict: APPROVED
---

# OCEANLINES Atlas 07 polar-mirrors role review

Standard-depth review of Atlas 07 commit `666c2b3`, which renders aligned
40–90° polar caps from the fixed NOAA OISST v2.1 display fields.

## Artifact and role selection

Artifact type: polar scientific cartography, browser raster projection,
accessible canvas, public explanation, and release candidate. All eight roles
apply because projection, orientation, missingness, physics, accessibility,
reproducibility, public status, and planetary comparison intersect.

## CURRENT — physical oceanography

| # | Finding | Severity | Evidence | Recommendation |
|---|---|---|---|---|
| 1 | Mirrors remain surface fields, not bathymetry, sea ice, circulation, heat content, or transport. | P3 | polar summary | Keep this boundary adjacent. |
| 2 | The view exposes land/ocean geometry without treating it as a solid frontal wall. | P3 | cap render and copy | Require velocity budgets for flow claims. |
| 3 | Visual symmetry is explicitly separated from physical equivalence. | P3 | footer and orientation note | Preserve mechanism-first interpretation. |

## SOUNDER — climate-data stewardship

| # | Finding | Severity | Evidence | Recommendation |
|---|---|---|---|---|
| 1 | Both caps sample the active committed two-degree field through the existing coordinate contract. | P3 | `renderPolarMirror` | Keep grid snapping shared with the map. |
| 2 | Beige remains land or missing rather than a categorical coastline mask. | P3 | method text | Add a separate mask before attribution. |
| 3 | Date, variable, baseline, error meaning, source, and checksum remain inherited from the fixed artifacts. | P3 | metadata panel | Preserve provenance across projections. |

## CHART — ocean cartography

| # | Finding | Severity | Evidence | Recommendation |
|---|---|---|---|---|
| 1 | The 40–90° radial azimuthal-equidistant sampling is named beside the panels. | P3 | polar method | Keep projection and cap extent visible. |
| 2 | Both panels use 0° at top and 90°E right, with the unconventional mirrored south orientation explicit. | P3 | introduction and ARIA | Never present the south panel without this note. |
| 3 | Shared graticules, active palette, and separately snapped ring circles make comparison consistent. | P3 | canvas renderer | Couple future projection changes to tests. |

## BEACON — public-science editing

| # | Finding | Severity | Evidence | Recommendation |
|---|---|---|---|---|
| 1 | “Polar mirrors” is memorable while the orientation and non-equivalence caveats remain immediate. | P3 | section heading and copy | Keep name and caveat together. |
| 2 | Sampled north/south coordinates are reported rather than implying an exact common row. | P3 | dynamic summary | Preserve sampled coordinates. |
| 3 | Readers can move from image to ring table, ladder, source, and method in one page. | P3 | atlas layout | Keep quantitative alternatives nearby. |

## HARBOR — accessibility

| # | Finding | Severity | Evidence | Recommendation |
|---|---|---|---|---|
| 1 | Both canvases have dynamic names and descriptions covering field, ring, and orientation. | P3 | canvas ARIA | Keep descriptions synchronized. |
| 2 | Selection is redundant through dashed amber circles, text, ring strips, and a semantic table. | P3 | renderer and ring section | Preserve non-color selection. |
| 3 | Mirrors stack at narrow widths; no interaction depends on pointer or motion. | P3 | responsive CSS | Retain one-column reflow. |

## KEEL — reproducibility engineering

| # | Finding | Severity | Evidence | Recommendation |
|---|---|---|---|---|
| 1 | The offline suite has 42 passing tests covering projection, orientation, boundaries, and accessibility hooks. | P3 | test suite | Keep static contracts plus browser smoke test. |
| 2 | A real browser renders both caps and reconstructs the 64° selection in anomaly mode. | P3 | headless render | Repeat against Pages. |
| 3 | Projection is deterministic browser code over committed arrays with no new network or generated artifact. | P3 | diff | Keep providers outside merge gates. |

## LOGBOOK — repository stewardship

| # | Finding | Severity | Evidence | Recommendation |
|---|---|---|---|---|
| 1 | Atlas 07 has immutable code, `0.8.0` citation candidate, milestone, tests, and review. | P3 | Git and repository files | Tag only merged main. |
| 2 | Publication remains pending until protected checks, Pages, and release evidence exist. | P3 | checklist | Reconcile status afterward. |
| 3 | No private names, machine paths, new assets, secrets, or license changes enter the repository. | P3 | boundary scan | Preserve public isolation. |

## ORBIT — planetary comparison

| # | Finding | Severity | Evidence | Recommendation |
|---|---|---|---|---|
| 1 | Mirrored geometry is explicitly not evidence of shared Earth/gas-giant dynamics. | P3 | footer and summary | Keep visual rhyme subordinate to mechanism. |
| 2 | The paired view demonstrates how boundary conditions alter bands even under aligned coordinates. | P3 | north/south caps | Compare forcing and depth before transfer. |
| 3 | No planetary retrieval is implied by the terrestrial surface product. | P3 | Atlas scope | Require planetary kernels for future co-plots. |

## Synthesis

```text
Roles reviewed: 8
P1 blockers: 0  |  P2 issues: 0  |  P3 confirmed controls: 24

Verdict: APPROVED

Top finding: The aligned caps make polar boundary geometry immediately legible
while explicitly declaring the mirrored south orientation and inferential limit.

Cross-role consensus: Projection, orientation, active field, product
missingness, sampled rings, text alternatives, and physical boundaries agree.
```

## Amend

No P1 or P2 amendment remains for `666c2b3`. Next safeguards:

1. Merge only after both protected hosted checks pass.
2. Verify both live cap canvases and the 64° summary after Pages deploys.
3. Publish `v0.8.0` from merged main without moving earlier tags.
