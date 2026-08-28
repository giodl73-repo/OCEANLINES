# Abyssal Heat: Source or Transport?

## Status

This is a source-qualified collaboration case, not a replication. It records
an open test suggested by Stephanie Buchanan's public research log and defines
what OCEANLINES would need to map and check it independently. No focal input
fields, solver outputs, or derived masks have been imported into OCEANLINES.

## The question

Observed abyssal warming can reflect at least two different kinds of change:

1. a change in heat entering the ocean near the seafloor; or
2. a change in how circulation carries existing heat into the observed volume.

Those mechanisms may coexist, but a map of hot crust or known vents cannot by
itself establish either one. The decisive object is a budget on a declared
three-dimensional volume, with source, transport, storage, and uncertainty
kept separate.

## Four layers that must not be collapsed

| Layer | What it can show | What it cannot establish alone |
|---|---|---|
| Observed abyssal warming | the location, depth range, period, and uncertainty of a temperature tendency | the heat source or transport pathway |
| Conductive seafloor heat flux | an estimated spatial source field in watts per square metre | direct measurement in every cell or changing delivery to abyssal water |
| Lithosphere and vent opportunity | crustal age, spreading setting, and known or inferred vent locations | complete vent coverage, discharge power, or a global causal attribution |
| Circulation-mediated delivery | where a tagged source is carried under a specified velocity field and solver | truth independent of the reanalysis, remapping, boundary conditions, and numerics |

Temperature tendency, integrated heat content, source power, boundary heat
flux, and the fraction of a tagged source delivered to a target are different
quantities. OCEANLINES will not substitute one for another.

## What the public research log reports

Buchanan's 20 August 2026 article compares an observed abyssal-warming
acceleration footprint with inferred seafloor heat-source fields. The values
below are **author-reported and have not been independently reproduced by
OCEANLINES**.

| Reported diagnostic | Conductive field | Broader lithospheric estimate | Hydrothermal residual |
|---|---:|---:|---:|
| Approximate global power | 16.8 TW | 28.9 TW | 12.2 TW |
| Available/required power under the positive-warming footprint | 0.25 | 0.33 | 0.08 |
| Spatial correlation with warming acceleration | 0.026 | 0.026 | 0.019 |
| Required change in delivered-source fraction | 0.496 | 0.288 | 0.683 |

The article also reports:

- a bottom-intensification contrast of about `-4.60e-5 K yr^-2`, opposite the
  sign expected from a simple bottom-up geothermal fingerprint;
- temperature/salinity compensation in 99.97% of paired cells;
- 721 InterRidge vent fields, including 666 classified as active or inferred
  active, and optimistic opportunity-cover fractions near 8%; and
- a remaining actual-circulation-versus-repeating-climatology transport test
  that was still in progress when the article was published.

These reported diagnostics weaken a simple claim that the mapped warming is
dominated by local geothermal input. They do not eliminate circulation-driven
redistribution, unresolved sources, observation error, or alternative
definitions of the target volume.

The independent observational anchor is Johnson (2026), which estimates that
globally averaged 4000–6000 dbar warming rose from `5.4 ± 4.9 TW` in 1988 to
`20.2 ± 3.9 TW` in 2018. The 2000–4000 dbar layer did not show a statistically
significant acceleration in that analysis. Those are sparse-hydrography,
globally averaged estimates—not a causal map of geothermal influence.

## The clean transport experiment

The useful comparison changes one thing: the velocity history.

| Held identical | Compared |
|---|---|
| source field and normalization | monthly changing ORAS5 circulation for the declared period |
| target mask and vertical coordinates | the same months replaced by a repeating seasonal climatology |
| initial tracer and integration window | |
| ocean grid, source-to-ocean remapping, solver, boundaries, diffusion, time step, and output schedule | |

Before running it, the analysis must define:

- the exact geographic and vertical target support;
- whether `f` means target inventory/source input, target boundary flux/source
  input, or another dimensionally explicit ratio;
- the time interval over which both numerator and denominator are accumulated;
- treatment of heat leaving the domain or target; and
- the sign and magnitude that would count as evidence against the proposed
  circulation mechanism.

The primary contrast is

`delta_f_circ(t) = f_actual(t) - f_climatology(t)`.

It must be accompanied by, rather than substituted for:

- source and tracer conservation residuals through time;
- remap coverage, overlap, and power-conservation checks, including the ORCA
  tripolar fold;
- separate target inventory and target-boundary-flux diagnostics;
- basin, height-above-bottom, target-mask, diffusion, and resolution
  sensitivity tests; and
- uncertainty inherited from the observations and source construction.

## Evidence needed for an independent OCEANLINES result

To turn this case into maps or a reproduced result, OCEANLINES needs:

1. input source fields with provider, product, version, units, license, URLs,
   retrieval dates, and checksums;
2. the warming-acceleration field, uncertainty, positive-footprint rule, ocean
   mask, depth coordinates, and transformations;
3. exact ORAS5 variables, release/version, grid, monthly interval, and access
   recipe;
4. source-to-ocean remap weights plus coverage and conserved-power receipts;
5. solver source/version, configuration, numerical operators, boundary
   conditions, time-step record, and conservation log; and
6. matched actual and climatological outputs sufficient to recompute every
   plotted diagnostic.

Without those artifacts, OCEANLINES can faithfully map the question and the
reported claims, but it cannot label a figure as reproduced.

## What OCEANLINES can contribute

- a public four-layer atlas that keeps observation, source opportunity, and
  modeled delivery visually distinct;
- co-located inspection of warming, bathymetry, crustal context, vents, and
  tagged transport without implying that overlap proves causation;
- a compact provenance receipt for every field and transformation;
- deterministic remap, conservation, and metric checks; and
- accessible maps that state what each view shows and cannot show.

The immediate handoff and questions are in
[Stephanie Buchanan collaboration note](STEPHANIE-BUCHANAN-COLLABORATION.md).

## Stop conditions

OCEANLINES will pause causal interpretation if the compared experiments differ
in more than their declared velocity treatment, if the delivered fraction is
not dimensionally defined, if remapping fails its power-conservation check, or
if the result cannot be regenerated from shareable inputs and configuration.

## Sources

- [Buchanan (2026), *Can Heat From Below Explain the Abyssal Warming Acceleration?*](https://stephanieskystory.com/research-log/geothermal-hydrothermal-mechanism-part1) (accessed 2026-08-28)
- [Johnson (2026), *Observed Multi-Decadal Acceleration of Globally Averaged Abyssal Ocean Warming*](https://doi.org/10.1029/2026GL124104)
- [Desbruyeres et al. (2016), *Deep and abyssal ocean warming from 35 years of repeat hydrography*](https://doi.org/10.1002/2016GL070413)
- [Davies (2013), *Global map of solid Earth surface heat flow*](https://doi.org/10.1002/ggge.20271)
- [Seton et al. (2020), present-day oceanic crustal age and spreading parameters](https://doi.org/10.1029/2020GC009214)
- [InterRidge Vents Database v3.4](https://doi.org/10.1594/PANGAEA.917894)
- [Zuo et al. (2019), *The ECMWF operational ensemble reanalysis-analysis system for ocean and sea ice: a description of the system and assessment*](https://doi.org/10.5194/os-15-779-2019)
