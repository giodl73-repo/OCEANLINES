# Atlas 08 preview status

Atlas 08 is a private review branch. It has not replaced the released Atlas 07,
has not been pushed from this branch, and is not represented as a new version in
`CITATION.cff`.

## Reviewed components

| Component | Reviewed source commit | Native verdict | Review |
|---|---|---|---|
| Ocean-first conceptual map and interactive integration | `762a7de` | APPROVED for private preview | [fluid-geography review](signals/roles/check/ocean-first-fluid-geography-roles-check-2026-08-28.md) |
| Researcher-facing claims and data receipt | `c57e5a6` | APPROVED for private preview | [evidence-note review](signals/roles/check/researcher-evidence-note-roles-check-2026-08-28.md) |
| Claim-level fifteen-source literature spine | `a93999f` | APPROVED for private preview | [literature-spine review](signals/roles/check/claim-level-literature-spine-roles-check-2026-08-28.md) |
| Machine-readable zone and claims exports | `7d673df` | APPROVED for private preview | [research-export review](signals/roles/check/machine-readable-research-exports-roles-check-2026-08-28.md) |

The review commits that record those verdicts follow their source commits in
Git history. Each approval is scoped to a private preview and does not replace
external scientific peer review.

## Evidence state

- **Unchanged observational layer:** final NOAA/NCEI OISST v2.1 surface
  temperature, anomaly, and estimated-analysis-error fields for 2026-08-01.
- **New presentation layer:** pinned Natural Earth coastline geometry,
  redesigned conceptual overlays, clearer evidence modes, and researcher routes.
- **New research handoff:** bounded claims, exact source-response receipts,
  primary-literature mapping, BibTeX, optional review prompts, and CSV exports.
- **Still not present:** depth-resolved heat content, section heat transport,
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
4. Which quantitative layer should follow: depth-resolved structure,
   bathymetry/sea ice, or dynamically consistent heat transport.

Until those decisions are made, repository links may expose Atlas 08 on this
branch while public URLs and citation metadata continue to describe Atlas 07.
