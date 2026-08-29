# Atlas 08–10 private-preview status

Atlas 08 is a private review branch. It has not replaced the released Atlas 07,
has not been pushed from this branch, and is not represented as a new version in
`CITATION.cff`.

Atlas 09 is the current native-role-approved working draft on top of that
approved private preview. It adds one fixed Scripps RG Argo pressure-layer
anomaly. Owner visual approval and any public promotion remain open.

Atlas 10 is the current native-role-approved working draft. It extends that
exact monthly source into a four-level 10/300/700/1000 dbar anomaly ladder.
Owner visual approval and public promotion remain open.

## Reviewed components

| Component | Reviewed source commit | Native verdict | Review |
|---|---|---|---|
| Ocean-first conceptual map and interactive integration | `762a7de` | APPROVED for private preview | [fluid-geography review](signals/roles/check/ocean-first-fluid-geography-roles-check-2026-08-28.md) |
| Researcher-facing claims and data receipt | `c57e5a6` | APPROVED for private preview | [evidence-note review](signals/roles/check/researcher-evidence-note-roles-check-2026-08-28.md) |
| Claim-level fifteen-source literature spine | `a93999f` | APPROVED for private preview | [literature-spine review](signals/roles/check/claim-level-literature-spine-roles-check-2026-08-28.md) |
| Machine-readable zone and claims exports | `7d673df` | APPROVED for private preview | [research-export review](signals/roles/check/machine-readable-research-exports-roles-check-2026-08-28.md) |
| Atlas 09 RG Argo 700 dbar anomaly | `ef6662e` | APPROVED by native roles; owner visual review open | [Atlas 09 depth review](signals/roles/check/atlas-09-argo-700dbar-roles-check-2026-08-28.md) |
| Atlas 10 RG Argo depth ladder | `2756f1e` | APPROVED by native roles; owner visual review open | [Atlas 10 depth-ladder review](signals/roles/check/atlas-10-argo-depth-ladder-roles-check-2026-08-28.md) |
| PELAGOS projection laboratory | `92345ec`, `dbe8165` | APPROVED as a private experiment; default-atlas adoption open | [PELAGOS native-role review](signals/roles/check/pelagos-projection-laboratory-roles-check-2026-08-29.md) |

The review commits that record those verdicts follow their source commits in
Git history. Each approval is scoped to a private preview and does not replace
external scientific peer review.

## Evidence state

- **Unchanged observational layer:** final NOAA/NCEI OISST v2.1 surface
  temperature, anomaly, and estimated-analysis-error fields for 2026-08-01.
- **New reviewed depth layer:** July 2026 Scripps RG Argo potential-
  temperature anomaly at 700 dbar, sampled to a 2-degree display grid. It is
  an objectively mapped anomaly, not absolute temperature or heat content, and
  its 64.5°S limit excludes the Antarctic shelf and ice cavities.
- **New reviewed depth-ladder extension:** same-source anomalies at 10, 300,
  and 1000 dbar, pressure controls, bookmark state, and four-level probe output.
- **New presentation layer:** pinned Natural Earth coastline geometry,
  redesigned conceptual overlays, land-reference and water-first treatments,
  clearer evidence modes, researcher routes, and a three-candidate ocean-first
  projection laboratory. PELAGOS remains an experimental equal-area aspect,
  not the default atlas projection.
- **New research handoff:** bounded claims, exact source-response receipts,
  primary-literature mapping, BibTeX, optional review prompts, and CSV exports.
- **Still not present:** depth-integrated heat content, section heat transport,
  bathymetric gate diagnostics, sea-ice coupling, or validated zone boundaries.

## Validation state

Run the default offline checks from the repository root:

```powershell
python -m unittest analysis.test_atlas
node --check atlas/app.js
node --check analysis/export_research_tables.js
node analysis/export_research_tables.js
```

The current export contract contains twelve ordered zones and four bounded
claims. Source refreshes remain explicit network operations and are not part of
the default offline gate.

## Decisions deliberately still open

1. Owner visual approval of the complete private preview.
2. Whether Atlas 08 should replace Atlas 07 on the public site.
3. Whether a promoted release should retain `0.8.x` or receive a new version.
4. Whether Atlas 09's first pressure layer should be promoted after owner
   visual review.
5. Which quantitative layer should follow: absolute vertical structure,
   bathymetry/sea ice, or dynamically consistent heat transport.
6. Whether Atlas 10's pressure ladder should replace the single-level Atlas 09
   preview after owner visual review.
7. Whether PELAGOS should remain a projection study, receive quantitative
   distortion diagnostics, or become an interactive atlas option.

Until those decisions are made, repository links may expose Atlas 10 on this
branch while public URLs and citation metadata continue to describe Atlas 07.
