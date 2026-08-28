---
skill: roles-check
topic: abyssal-heat-collaboration
date: 2026-08-28
reviewed_base_commit: ea00f59
reviewed_artifacts: ABYSSAL-HEAT.md, STEPHANIE-BUCHANAN-COLLABORATION.md, README.md, SOURCE-REGISTER.md, PUBLICATION-CHECKLIST.md
role_set_commit: 262f3e7
role_set: .roles/ROLE.md
roles_used: 5
p1_count: 0
p2_count: 0
verdict: APPROVED
---

# OCEANLINES abyssal-heat collaboration role review

Standard-depth review of the public abyssal-heat research intake and its
email-ready collaboration handoff, reviewed as a working-tree candidate based
on commit `ea00f59`.

## Artifact and role selection

Artifact type: scientific explanatory prose, source register, proposed
experiment contract, and public collaboration note. CURRENT, SOUNDER, BEACON,
KEEL, and LOGBOOK apply because physical attribution, external-data
provenance, public language, reproducibility, and publication state intersect.
CHART, HARBOR, and ORBIT are not selected because this change introduces no
new map, interface, accessibility interaction, or planetary comparison.

## CURRENT — physical oceanography

| # | Finding | Severity | Evidence | Recommendation |
|---|---|---|---|---|
| 1 | Temperature tendency, heat content, source power, transport, and delivered fraction remain distinct quantities. | P3 | four-layer table and measurement paragraph | Preserve the firewall in every later map. |
| 2 | Spatial overlap and correlation are not treated as mechanism; the actual-versus-climatology experiment targets circulation explicitly. | P3 | reported-results boundary and clean experiment | Keep the single-variable comparison. |
| 3 | Competing explanations and observation limits remain open after the simple geothermal fingerprint is weakened. | P3 | interpretation following the reported diagnostics | Require a closed target-volume budget for causal language. |

## SOUNDER — climate-data stewardship

| # | Finding | Severity | Evidence | Recommendation |
|---|---|---|---|---|
| 1 | Every admitted external source has a public URL and an explicit claim boundary in the source register. | P3 | O23–O25 and D7–D10 | Add versions and licenses when fields are acquired. |
| 2 | The focal numbers are visibly author-reported and the access date is recorded; no unreceipted field is presented as local evidence. | P3 | status, results preface, O24 | Preserve this label until independent regeneration. |
| 3 | The evidence contract requires provider, version, units, license, retrieval date, checksum, grid, transforms, and remap receipts. | P3 | evidence-needed section | Materialize one receipt per acquired field. |

## BEACON — public-science editing

| # | Finding | Severity | Evidence | Recommendation |
|---|---|---|---|---|
| 1 | “Source or transport?” gives a clear public question without claiming a resolved cause. | P3 | title and question section | Keep the question form until evidence closes it. |
| 2 | Each layer states both what it shows and what it cannot establish alone. | P3 | four-layer table | Reuse these boundaries beside future controls. |
| 3 | The handoff is concise about the offer, non-replication status, five requests, and a direct email action. | P3 | collaboration note | Link to the published files before sending. |

## KEEL — reproducibility engineering

| # | Finding | Severity | Evidence | Recommendation |
|---|---|---|---|---|
| 1 | The proposed comparison holds source, grid, solver, boundaries, numerics, target, and schedule fixed while changing velocity history. | P3 | clean experiment table | Encode these invariants in a future machine-readable run contract. |
| 2 | The delivered-fraction metric cannot silently change meaning because numerator, denominator, units, support, and interval are required in advance. | P3 | pre-run definitions | Add dimensional and conservation tests with the solver. |
| 3 | Existing offline validation remains green: 42 unit tests, Python compilation, and JavaScript syntax checks pass. | P3 | local validation on 2026-08-28 | Add focal tests only after shareable data or fixtures exist. |

## LOGBOOK — repository stewardship

| # | Finding | Severity | Evidence | Recommendation |
|---|---|---|---|---|
| 1 | README navigation, source register, and publication checklist agree that this is an intake, not a reproduced atlas result. | P3 | three repository documents | Update all three together when status changes. |
| 2 | The public-isolation scan finds no private project names, private pointers, or machine-local paths in Markdown. | P3 | boundary scan on 2026-08-28 | Repeat before commit and publication. |
| 3 | The checklist leaves data acquisition and independent reproduction visibly incomplete. | P3 | unchecked collaboration items | Do not tag a result release while either remains open. |

## Synthesis

```text
Roles reviewed: 5
P1 blockers: 0  |  P2 issues: 0  |  P3 confirmed controls: 15

Verdict: APPROVED

Top finding: The package makes a concrete collaboration offer while keeping
Stephanie Buchanan's reported calculations strictly separate from an
OCEANLINES-reproduced result.

Cross-role consensus: The physical quantities, source boundaries, public
language, experiment invariants, and repository status tell the same story.
```

## Amend

No P1 or P2 amendment remains. Three safeguards were applied or retained:

1. Place the non-replication status before all focal numerical claims.
2. Record the public-article access date and exact independent-evidence needs.
3. Leave acquisition and reproduction unchecked in the publication checklist.
