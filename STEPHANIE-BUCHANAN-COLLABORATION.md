# Collaboration Note for Stephanie Buchanan

## Why we are reaching out

OCEANLINES is a public atlas project for ocean heat geography. Your research
log on abyssal warming identifies exactly the distinction the project is meant
to make visible: heat-source geography is not the same as circulation-mediated
heat delivery.

From the public article, we understand that the simple local-overlap tests,
bottom-intensification test, and temperature/salinity compensation test do not
support a dominant local geothermal fingerprint. The remaining discriminating
experiment compares tagged delivery under changing 2004–2024 ORAS5 circulation
with delivery under a repeating monthly climatology.

That summary is our reading of the public article. OCEANLINES has not received
or independently reproduced the focal input fields, masks, remapping, solver,
or outputs, so it does not present the reported numerical results as its own
verification.

## A concrete collaboration offer

If the underlying artifacts become shareable, OCEANLINES can contribute:

- a public four-layer map separating observed warming, conductive source,
  lithosphere/vent opportunity, and modeled delivery;
- an independent check of grid remapping, conserved source power, tracer
  conservation, and the actual-versus-climatology metric;
- co-located visual inspection without treating spatial overlap as causal
  evidence; and
- field-level source receipts so every public layer can be regenerated.

The proposed experiment and evidence contract are documented in
[Abyssal Heat: Source or Transport?](ABYSSAL-HEAT.md).

## Five questions

1. Which exact source datasets, versions, and transformations produced the
   conductive, lithospheric, and hydrothermal-residual fields?
2. How is the positive warming footprint defined horizontally and vertically,
   and how are observation uncertainty and unsampled cells represented?
3. What is the precise numerator, denominator, unit, and accumulation interval
   for the delivered-source fraction `f`?
4. Can the ORCA tripolar-fold remap weights and the coverage and
   power-conservation receipts be shared?
5. When practical, could the solver version/configuration and matched actual
   and climatological outputs be made available with checksums?

These are invitations to make a public result inspectable, not prerequisites
for discussing the scientific idea.

## Email draft

**Subject:** A public map and independent check for the abyssal-heat test

Hi Stephanie,

I read your research log on geothermal and hydrothermal explanations for the
abyssal warming acceleration. The distinction you draw between source power
and circulation-mediated delivery fits a public ocean-mapping project I have
been building called OCEANLINES.

I wrote a short, source-qualified collaboration note here:
https://github.com/giodl73-repo/OCEANLINES/blob/main/STEPHANIE-BUCHANAN-COLLABORATION.md

The project is here:
https://github.com/giodl73-repo/OCEANLINES

We have not reproduced your numerical results. If your input fields and
actual-versus-climatology transport outputs become shareable, I would be glad
to turn them into a four-layer public atlas and independently check the remap,
conservation, and delivered-fraction calculation. Would that be useful to you?

Best,
Gio
