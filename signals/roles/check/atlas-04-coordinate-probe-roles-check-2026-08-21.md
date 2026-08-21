---
skill: roles-check
topic: atlas-04-coordinate-probe
date: 2026-08-21
reviewed_atlas_commit: a4ae7ca
role_set_commit: 262f3e7
role_set: .roles/ROLE.md
roles_used: 8
p1_count: 0
p2_count: 0
verdict: APPROVED
---

# OCEANLINES Atlas 04 coordinate-probe role review

This standard-depth review applies all eight OCEANLINES functional roles to the
Atlas 04 implementation at commit `a4ae7ca`. The reviewed artifact adds a
pointer- and keyboard-accessible coordinate probe to the unchanged fixed
1 August 2026 NOAA OISST v2.1 surface fields.

## Artifact identification and role selection

Artifact type: interactive scientific map, browser code, public explanation,
and reproducible observational-data interface.

All roles apply because coordinate lookup joins physical interpretation, three
climate-data layers, projected map geometry, public wording, accessible input,
deterministic tests, release state, and the repository's planetary-comparison
boundary.

## CURRENT — physical oceanography

| # | Finding | Severity | Evidence | Recommendation |
|---|---|---|---|---|
| 1 | Each probe reports absolute SST, referenced anomaly, and estimated analysis error as separately named values. | P3 | probe readout | Preserve the three-field separation. |
| 2 | The readout explicitly says the sampled values are surface products, not heat content or transport. | P3 | `inspectCoordinates` output | Keep this boundary in every local-inspection surface. |
| 3 | The probe makes no causal or gateway inference from one selected cell. | P3 | interface and Atlas 04 README | Require spatial/temporal budgets before adding mechanism language. |

## SOUNDER — climate-data stewardship

| # | Finding | Severity | Evidence | Recommendation |
|---|---|---|---|---|
| 1 | All three values use one row/column after snapping against the shared v2 grid coordinates. | P3 | `probeCellFromCoordinates`; co-location regression test | Keep grid equality a required test. |
| 2 | Documentation distinguishes the two-degree display sample from NOAA's native-resolution grid and the raw pointer coordinate. | P3 | Atlas 04 “Inspect a location” section | Preserve this distinction if display stride changes. |
| 3 | Land and missing values remain explicit independently for each field rather than being coerced to zero. | P3 | `probeValue` | Keep per-variable missingness visible. |

## CHART — ocean cartography

| # | Finding | Severity | Evidence | Recommendation |
|---|---|---|---|---|
| 1 | Longitude snapping matches the renderer's antimeridian seam and 0° central meridian transformation. | P3 | renderer and snapping functions | Test any future projection change against the probe. |
| 2 | The selected cell receives a black-outlined white crosshair visible across warm, cool, light, and dark palette regions. | P3 | headless-browser anomaly render | Preserve redundant textual coordinates alongside the marker. |
| 3 | The URL stores normalized sampled coordinates, so a shared view reconstructs the same cell and map mode. | P3 | `updateAtlasUrl` and deep-link browser check | Treat query parameters as a public interface. |

## BEACON — public-science editing

| # | Finding | Severity | Evidence | Recommendation |
|---|---|---|---|---|
| 1 | The form explains snapping before interaction and reports the sampled coordinate afterward. | P3 | probe fieldset and output | Keep requested versus sampled location explicit. |
| 2 | One concise sentence presents SST, anomaly, error, and the inferential boundary without collapsing their meanings. | P3 | live output wording | Preserve field labels even when space is tight. |
| 3 | The Atlas 04 README includes a bookmark example and states what the probe does not calculate. | P3 | atlas documentation | Keep the example fixed to a non-sensitive public coordinate. |

## HARBOR — accessibility

| # | Finding | Severity | Evidence | Recommendation |
|---|---|---|---|---|
| 1 | Latitude and longitude have native labels, numeric constraints, decimal input hints, and a keyboard-native submit button. | P3 | coordinate form | Preserve native form behavior. |
| 2 | Pointer selection has a complete keyboard alternative, and results are announced through a polite live `output`. | P3 | canvas and form listeners; `aria-live` | Test both paths whenever probe behavior changes. |
| 3 | Visible focus, minimum control height, responsive two-column layout, crosshair, and text readout provide redundant access. | P3 | probe CSS and browser render | Retain the text result as the authoritative accessible output. |

## KEEL — reproducibility engineering

| # | Finding | Severity | Evidence | Recommendation |
|---|---|---|---|---|
| 1 | The suite now has 34 passing tests, including an exact three-field Southern Ocean cell fixture. | P3 | `test_probe_coordinate_uses_three_colocated_fields` | Keep expected values in stored hundredths. |
| 2 | A real headless-browser deep link reconstructs `63.88°S, 59.88°W` and the three expected formatted fields. | P3 | browser validation record | Repeat this smoke test before release. |
| 3 | Atlas 04 introduces no download, provider dependency, or transformed data artifact; existing offline CI remains sufficient. | P3 | diff from Atlas 03 | Keep live NOAA access outside merge checks. |

## LOGBOOK — repository stewardship

| # | Finding | Severity | Evidence | Recommendation |
|---|---|---|---|---|
| 1 | Atlas 04 has an immutable implementation commit, milestone row, `0.5.0` citation version, and dedicated review artifact. | P3 | Git, README, CFF, this review | Tag only the eventual merged commit. |
| 2 | Publication remains explicitly pending until the protected PR, hosted checks, Pages deployment, and release complete. | P3 | publication checklist | Change the item only after external evidence exists. |
| 3 | The work is isolated on `atlas/04-coordinate-probe` and does not alter any external portfolio worktree. | P3 | repository boundaries | Keep portfolio registration separate. |

## ORBIT — planetary comparison

| # | Finding | Severity | Evidence | Recommendation |
|---|---|---|---|---|
| 1 | Coordinate inspection remains Earth-only and does not imply a planetary observed layer. | P3 | available data and mode labels | Keep OCEANBELTS labeled as a reading lens. |
| 2 | Co-located separation of temperature, anomaly, and uncertainty strengthens the measurement discipline needed for later planetary retrievals. | P3 | probe output and OCEANBELTS firewall | Require analogous retrieval metadata before adding planetary probes. |
| 3 | No visual or coordinate similarity is presented as evidence of shared deep dynamics. | P3 | Atlas 04 scope | Preserve mechanism-first comparisons. |

## Synthesis

```text
Roles reviewed: 8
P1 blockers: 0  |  P2 issues: 0  |  P3 confirmed controls: 24

Verdict: APPROVED

Top finding: Atlas 04 turns three aligned observational layers into one
bookmarkable local evidence record while keeping their meanings separate.

Cross-role consensus: Coordinate precision, accessibility, and scientific
qualification agree because the sampled display cell—not the pointer—is the
single declared object across map, form, URL, output, documentation, and tests.
```

## Amend

No P1 or P2 amendment remains for commit `a4ae7ca`. The next safeguards are:

1. Merge only after both protected hosted checks pass.
2. Verify the Pages deployment with the documented deep link after merge.
3. Publish `v0.5.0` from the merged commit without moving the existing
   `v0.4.0` Atlas 03 tag.
