---
skill: roles-check
topic: oceanlines-atlases
date: 2026-08-21
reviewed_atlas_commit: 31765f3
role_set: .roles/ROLE.md
roles_used: 8
p1_count: 1
verdict: NEEDS-WORK
---

# OCEANLINES Atlas 00–02 role review

This review supersedes the provisional portfolio-governance audit. It applies
OCEANLINES' own functional role roster to Atlas 00 (`10cf92b`), Atlas 01
(`cd7f1b9`), and Atlas 02 (`31765f3`). The roles are quality-control lenses,
not simulated people or a substitute for external scientific peer review.

## Artifact and role selection

| Atlas | Evidence class | Historical validation |
|---|---|---|
| 00 | interactive conceptual geography | 10 tests passed at its commit |
| 01 | fixed NOAA OISST absolute SST | 15 tests passed at its commit |
| 02 | fixed NOAA OISST absolute SST and referenced anomaly | 19 tests passed at its commit |

All eight roles apply because this is simultaneously an ocean-physics claim,
derived climate-data product, map, public explanation, interactive interface,
reproducible artifact, public repository, and Earth/planet comparison project.

## CURRENT — physical oceanography

| # | Finding | Severity | Evidence | Recommendation |
|---|---|---|---|---|
| 1 | The measurement firewall consistently separates temperature, heat content, anomaly, and transport. | P3 | root README; `OCEANREALMS.md`; all atlas modes | Preserve this as a release invariant. |
| 2 | Atlas 00's named footprints are deliberately schematic, but their crisp shapes can still be read as fixed material boundaries. | P2 | conceptual SVG, markers, and atlas evidence note | Add “schematic and permeable” directly to the conceptual-map legend, not only the details panel. |
| 3 | The Drake Passage counterfactual is presented as a circulation reorganization with model-dependent feedbacks, not “closure means Antarctica melts.” | P3 | `OCEANREALMS.md` gateway table and qualification | Retain the explicit separation among sea ice, shelves, and grounded ice. |

## SOUNDER — climate-data stewardship

| # | Finding | Severity | Evidence | Recommendation |
|---|---|---|---|---|
| 1 | Both observed layers carry product, date, query, retrieval time, grid shape, units, and source-response SHA-256 provenance. | P3 | committed data artifacts; snapshot tests | Preserve exact provenance in every new layer. |
| 2 | Atlas 02's anomaly artifact uses the current metadata schema, while the earlier SST artifact lacks the same explicit `variable_id` and `baseline` fields. | P2 | `atlas/data/oisst-*.js` | Regenerate SST through the current packager and validate a shared schema. |
| 3 | Missing and land cells are preserved, but the next declared confidence layer—OISST estimated error—has not been implemented. | P2 | atlas README and project status | Add the time-matched error field before making spatial-confidence claims. |

## CHART — ocean cartography

| # | Finding | Severity | Evidence | Recommendation |
|---|---|---|---|---|
| 1 | Conceptual, absolute, and anomaly modes have separate labels, legends, palettes, and inferential boundaries. | P3 | mode controls and `setMode` behavior | Keep evidence class visible through every interaction. |
| 2 | The anomaly scale is zero-centered and symmetrically clipped, with the unclipped sampled range disclosed. | P3 | atlas README, artifact summary, palette code | Add a visible clipped-value cue if local values are later inspectable. |
| 3 | The observed raster is displayed as a rectangular world map without an explicit projection or longitude-seam statement. | P2 | canvas renderer and atlas README | Declare the equirectangular display convention and coordinate seam beside the map. |

## BEACON — public-science editing

| # | Finding | Severity | Evidence | Recommendation |
|---|---|---|---|---|
| 1 | The land-analogy vocabulary is memorable and the root README immediately warns that provinces move, leak, split, and merge. | P3 | root opening and HEATMASS grammar | Repeat that warning in the interactive conceptual mode. |
| 2 | Atlas 02 clearly says the anomaly is neither absolute temperature nor causal attribution. | P3 | atlas README and selected-mode boundary | Preserve the paired “shows / cannot establish” pattern. |
| 3 | “Heat continent” and “gate” remain vulnerable to being repeated as a wall/blockage claim when seen without the surrounding prose. | P2 | conceptual labels and social-share context | Give every standalone figure a one-sentence permeability and budget caveat. |

## HARBOR — accessibility

| # | Finding | Severity | Evidence | Recommendation |
|---|---|---|---|---|
| 1 | The interface uses semantic sections, labeled controls, `aria-pressed`, keyboard-native buttons, visible focus styles, and an `aria-live` details panel. | P3 | `atlas/index.html` and styles | Retain these contracts in interaction tests. |
| 2 | The canvas has one static label even though it alternates between absolute SST and anomaly, so its accessible name can contradict the active mode. | P2 | `#sst-canvas` label and mode switching | Update the canvas accessible name and description on every mode change. |
| 3 | Observed values are conveyed primarily through color; the side panel reports global metadata but not an equivalent spatial data summary. | P2 | raster, legend, and observed-mode panel | Add a textual regional/value exploration path and redundant sign encoding for anomaly. |

## KEEL — reproducibility engineering

| # | Finding | Severity | Evidence | Recommendation |
|---|---|---|---|---|
| 1 | The repository has 22 passing local tests but no CI workflow, so no automated gate blocks a broken public revision. | P1 | local full-suite run; no `.github/workflows` | Add offline CI for Python discovery, Python compilation, JavaScript syntax, and role contracts. |
| 2 | Default tests validate committed artifacts without contacting NOAA, which makes the main gate deterministic. | P3 | unit-test structure | Keep live acquisition outside the required merge gate. |
| 3 | NCSS query construction is tested, but the optional NetCDF parser has no local fixture exercising dimensions, masks, and coordinate order. | P2 | `parse_netcdf` and snapshot tests | Add a minimal local NetCDF fixture in an optional dependency job. |

## LOGBOOK — repository stewardship

| # | Finding | Severity | Evidence | Recommendation |
|---|---|---|---|---|
| 1 | License, citation, source register, public scope, and remote status are explicit. | P3 | root public files | Keep the remote line truthful until publication. |
| 2 | The publication checklist now names the selected owner, installed roles, unresolved P1 review work, missing CI, remote creation, scan, and push separately. | P3 | `PUBLICATION-CHECKLIST.md` | Change each item only when evidence exists. |
| 3 | Atlas milestones are recoverable from Git but lack one public table joining commit, evidence class, role verdict, and data date. | P2 | Git history and README status | Add a compact milestone ledger before the first tagged release. |

## ORBIT — planetary comparison

| # | Finding | Severity | Evidence | Recommendation |
|---|---|---|---|---|
| 1 | `OCEANBELTS.md` explicitly separates visible color, brightness temperature, kinetic temperature, composition, heat content, and transport. | P3 | measurement ladder and failure tests | Preserve this as the comparison firewall. |
| 2 | The comparison is organized around transferable mechanisms such as jets, potential-vorticity gradients, eddies, and thermal-wind constraints rather than similar stripes alone. | P3 | Earth/planet translation table | Add nondimensional regime values when the atlas becomes quantitative. |
| 3 | The interactive atlas exposes an OCEANBELTS lens but currently supplies no planetary observed layer, so a reader may expect a comparison the map does not yet deliver. | P2 | lens control versus available modes | Label OCEANBELTS as a reading lens until a sourced planetary layer exists. |

## Synthesis

```text
Roles reviewed: 8
P1 blockers: 1  |  P2 issues: 11  |  P3 notes: 12

Verdict: NEEDS-WORK

Blocking finding: OCEANLINES has a deterministic local suite but no public CI
gate. The scientific language is careful and the observed layers are unusually
well bounded; the largest remaining science-facing gaps are a unified artifact
schema, displayed uncertainty, and accessible non-color spatial inspection.
```

## Amend

1. Add the offline CI gate and require all 22 current checks.
2. Align the two OISST artifacts to one schema and add the estimated-error layer.
3. Declare the map projection/seam and provide mode-aware, non-color access to
   observed spatial values.
