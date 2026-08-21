const zones = [
  { id: "indo-pacific-warm-pool", n: 1, name: "Indo-Pacific Warm Pool", kind: "reservoir", label: "Heat continent", role: "persistent reservoir", depth: "surface / upper ocean", clock: "persistent; seasonally breathing", evidence: "conceptual · O18", x: 77, y: 44, families: ["heatmass", "oceanbelts"], summary: "The largest persistent expanse of very warm surface water: a continent-like reservoir whose edge moves with threshold, season, and dataset.", boundary: "A warm surface footprint is not a full-depth heat-content integral, and its diagnostic boundary is not a material wall.", source: "https://www.climate.gov/news-features/featured-images/warm-pool-indo-pacific-ocean-has-almost-doubled-size-changing-global" },
  { id: "western-hemisphere-warm-pool", n: 2, name: "Western Hemisphere Warm Pool", kind: "reservoir", label: "Seasonal heat continent", role: "seasonal reservoir", depth: "surface / upper ocean", clock: "seasonal expansion", evidence: "conceptual · O19", x: 34, y: 44, families: ["heatmass"], summary: "A seasonally connected warm-water province spanning parts of the tropical eastern Pacific, Gulf of Mexico, Caribbean, and western tropical Atlantic.", boundary: "Central America divides the ocean basins even when a temperature threshold visually joins the warm regions.", source: "https://www.aoml.noaa.gov/phod/research/tav/awp/" },
  { id: "northeast-pacific-blob", n: 3, name: "Northeast Pacific Blob", kind: "transient", label: "Heat blob", role: "marine heatwave anomaly", depth: "surface with subsurface remnant", clock: "episodic / multi-year", evidence: "observational · O20–O21", x: 13, y: 27, families: ["heatmass"], summary: "A named marine heatwave demonstrates why a heat blob is an event relative to a baseline—not a permanent ocean province.", boundary: "Its surface expression does not determine its full-depth energy or prove a single cause.", source: "https://doi.org/10.1002/2016GL071039" },
  { id: "el-nino-tongue", n: 4, name: "El Niño Tongue", kind: "transient", label: "Heat tongue", role: "basin-scale anomaly", depth: "surface / thermocline coupled", clock: "interannual", evidence: "conceptual", x: 17, y: 45, families: ["heatmass", "oceanbelts"], summary: "An eastward-reaching equatorial anomaly: a tongue because its geometry and evolution matter as much as its peak temperature.", boundary: "The atlas shape is schematic and is not an event declaration or an ENSO index.", source: "../SOURCE-REGISTER.md" },
  { id: "gulf-stream", n: 5, name: "Gulf Stream", kind: "pathway", label: "Heat river", role: "western boundary current", depth: "surface intensified; deep structure", clock: "persistent and variable", evidence: "conceptual · O2", x: 31, y: 27, families: ["oceanrealms", "oceanbelts"], summary: "A narrow, fast pathway that exports warm water poleward and sheds moving rings into the surrounding ocean.", boundary: "Current speed and water temperature do not, by themselves, give heat transport across a section.", source: "https://www.whoi.edu/ocean-learning-hub/ocean-topics/how-the-ocean-works/ocean-circulation/currents-gyres-eddies/" },
  { id: "kuroshio", n: 6, name: "Kuroshio", kind: "pathway", label: "Heat river", role: "western boundary current", depth: "surface intensified; deep structure", clock: "persistent and variable", evidence: "conceptual · O2", x: 88, y: 29, families: ["oceanrealms", "oceanbelts"], summary: "The North Pacific counterpart in the map grammar: a swift boundary current, extension, and ring-forming system.", boundary: "The analogy to the Gulf Stream is structural, not an assertion of identical forcing, geometry, or transport.", source: "https://www.whoi.edu/ocean-learning-hub/ocean-topics/how-the-ocean-works/ocean-circulation/currents-gyres-eddies/" },
  { id: "agulhas", n: 7, name: "Agulhas System", kind: "pathway", label: "River and moving islands", role: "boundary current / leakage", depth: "upper ocean to intermediate", clock: "persistent with episodic rings", evidence: "conceptual", x: 55, y: 62, families: ["oceanrealms"], summary: "A current system whose retroflection and rings make exchange look less like a pipe and more like parcels escaping a moving border.", boundary: "The marker does not quantify leakage or attribute downstream climate effects.", source: "../SOURCE-REGISTER.md" },
  { id: "antarctic-circumpolar-current", n: 8, name: "Antarctic Circumpolar Current", kind: "pathway", label: "Circumpolar belt", role: "fronted zonal current", depth: "deep-reaching fronts", clock: "persistent and meandering", evidence: "observational · O4, O8–O9", x: 69, y: 66, families: ["oceanrealms", "oceanbelts"], summary: "Earth's clearest ocean belt: a deep-reaching, eastward current whose fronts inhibit exchange while eddies and regional pathways leak heat across them.", boundary: "The ACC is not a solid cold wall and Drake Passage is not a thermal plug.", source: "https://doi.org/10.1175/JPO-D-19-0266.1" },
  { id: "circumpolar-deep-water", n: 9, name: "Circumpolar Deep Water", kind: "buried", label: "Buried heat continent", role: "subsurface reservoir / source water", depth: "intermediate to deep; region dependent", clock: "persistent with changing access", evidence: "synthesis · O10, O14", x: 42, y: 65, families: ["heatmass", "oceanrealms"], summary: "Relatively warm subsurface water can approach Antarctic margins beneath a cold surface, making vertical structure central to ice-shelf exposure.", boundary: "Offshore presence does not equal delivery to a cavity; fronts, shelf breaks, troughs, mixing, and winds intervene.", source: "https://doi.org/10.1029/2018RG000624" },
  { id: "atlantic-water-arctic", n: 10, name: "Atlantic Water in the Arctic", kind: "buried", label: "Buried heat continent", role: "subsurface inflow and reservoir", depth: "below the cold, fresh halocline", clock: "persistent and variable", evidence: "observational synthesis · O22", x: 41, y: 16, families: ["heatmass", "oceanrealms"], summary: "Warm Atlantic-origin water can sit beneath a colder, fresher lid: the Arctic example of why the surface can conceal a large thermal contrast.", boundary: "Subsurface temperature does not determine when, where, or how much heat reaches sea ice or the atmosphere.", source: "https://doi.org/10.3389/fmars.2019.00416" },
  { id: "drake-passage", n: 11, name: "Drake Passage", kind: "gate", label: "Heat gate", role: "circumpolar transport section", depth: "full water column", clock: "persistent geometry; variable flow", evidence: "observational / modeled · O4–O7", x: 23, y: 66, families: ["oceanrealms", "oceanbelts"], summary: "The narrowest major gate on the circumpolar route. It makes ACC transport measurable and exposes how geometry reorganizes global circulation.", boundary: "Closing the gate in a model changes many coupled circulations; it is not equivalent to simply sending warm water south.", source: "https://doi.org/10.1175/JCLI-D-15-0554.1" },
  { id: "indonesian-throughflow", n: 12, name: "Indonesian Throughflow", kind: "gate", label: "Archipelagic heat gate", role: "inter-basin exchange", depth: "multiple constrained passages", clock: "persistent and variable", evidence: "conceptual", x: 75, y: 47, families: ["oceanrealms"], summary: "A branching tropical gate where land geometry constrains exchange between the Pacific and Indian oceans.", boundary: "A point marker hides multiple straits, vertical structure, tides, mixing, and seasonal reversals.", source: "../SOURCE-REGISTER.md" }
];

const markers = document.querySelector("#markers");
const count = document.querySelector("#visible-count");
const fields = Object.fromEntries(["index", "name", "kind", "summary", "role", "depth", "clock", "evidence", "boundary", "source"].map(key => [key, document.querySelector(`#zone-${key}`)]));
let selectedZone = zones[0];

function selectZone(zone) {
  selectedZone = zone;
  document.querySelectorAll(".marker").forEach(marker => marker.classList.toggle("selected", marker.dataset.id === zone.id));
  fields.index.textContent = `ZONE ${String(zone.n).padStart(2, "0")} · ${zone.label.toUpperCase()}`;
  fields.name.textContent = zone.name;
  fields.kind.textContent = zone.families.map(name => name.toUpperCase()).join(" · ");
  for (const key of ["summary", "role", "depth", "clock", "evidence", "boundary"]) fields[key].textContent = zone[key];
  fields.source.href = zone.source;
  fields.source.textContent = zone.source.startsWith("../") ? "Open the source register →" : "Open primary source →";
}

function temperatureColor(value) {
  const stops = [
    [-2, [216, 244, 255]], [0, [141, 211, 232]], [8, [43, 156, 189]],
    [16, [56, 182, 138]], [22, [242, 207, 91]], [28, [240, 120, 66]], [32, [185, 39, 53]]
  ];
  const bounded = Math.max(stops[0][0], Math.min(stops.at(-1)[0], value));
  let upper = stops.findIndex(stop => stop[0] >= bounded);
  if (upper < 1) upper = 1;
  const [lowValue, lowColor] = stops[upper - 1];
  const [highValue, highColor] = stops[upper];
  const mix = (bounded - lowValue) / (highValue - lowValue);
  const color = lowColor.map((channel, index) => Math.round(channel + (highColor[index] - channel) * mix));
  return `rgb(${color.join(",")})`;
}

function renderObservedSst() {
  const data = window.OCEANLINES_OISST;
  const canvas = document.querySelector("#sst-canvas");
  const context = canvas.getContext("2d");
  const [rows, columns] = data.shape;
  const cellWidth = canvas.width / columns;
  const cellHeight = canvas.height / rows;
  context.fillStyle = "#c8bda5";
  context.fillRect(0, 0, canvas.width, canvas.height);
  data.values_c_hundredths.forEach((encoded, index) => {
    if (encoded === null) return;
    const row = Math.floor(index / columns);
    const column = index % columns;
    const shiftedColumn = (column + columns / 2) % columns;
    context.fillStyle = temperatureColor(encoded / 100);
    context.fillRect(shiftedColumn * cellWidth, (rows - row - 1) * cellHeight, Math.ceil(cellWidth), Math.ceil(cellHeight));
  });
  context.strokeStyle = "rgba(255,255,255,.24)";
  context.lineWidth = 1;
  for (let longitude = 60; longitude < 360; longitude += 60) {
    context.beginPath(); context.moveTo(longitude / 360 * canvas.width, 0); context.lineTo(longitude / 360 * canvas.width, canvas.height); context.stroke();
  }
  for (let latitude = 30; latitude < 180; latitude += 30) {
    context.beginPath(); context.moveTo(0, latitude / 180 * canvas.height); context.lineTo(canvas.width, latitude / 180 * canvas.height); context.stroke();
  }
}

function showObservedMetadata() {
  const data = window.OCEANLINES_OISST;
  const valid = data.values_c_hundredths.filter(value => value !== null);
  const summary = data.summary || {
    valid_ocean_cells: valid.length,
    minimum_c: Math.min(...valid) / 100,
    maximum_c: Math.max(...valid) / 100
  };
  fields.index.textContent = "ATLAS 01 · OBSERVATIONAL SURFACE FIELD";
  fields.name.textContent = "Sea Surface Temperature";
  fields.kind.textContent = `NOAA OISST V2.1 · ${data.date}`;
  fields.summary.textContent = `A daily, spatially complete analysis sampled into ${summary.valid_ocean_cells.toLocaleString()} displayed ocean cells. Range: ${summary.minimum_c.toFixed(1)}–${summary.maximum_c.toFixed(1)}°C.`;
  fields.role.textContent = "surface thermal field";
  fields.depth.textContent = "sea surface · 0 m product level";
  fields.clock.textContent = `one day · ${data.date}`;
  fields.evidence.textContent = "observational analysis · D1";
  fields.boundary.textContent = data.boundary;
  fields.source.href = data.doi;
  fields.source.textContent = "Open NOAA dataset record →";
}

function setMapMode(mode) {
  const observed = mode === "observed";
  document.querySelectorAll(".map-mode").forEach(button => {
    const active = button.dataset.mode === mode;
    button.classList.toggle("active", active);
    button.setAttribute("aria-pressed", String(active));
  });
  document.querySelector("#conceptual-map").hidden = observed;
  document.querySelector("#sst-canvas").hidden = !observed;
  document.querySelector("#observed-stamp").hidden = !observed;
  document.querySelector("#temperature-key").hidden = !observed;
  markers.hidden = observed;
  document.querySelector("#map-stage").classList.toggle("observed", observed);
  document.querySelectorAll(".lens").forEach(button => { button.disabled = observed; });
  document.querySelector("#map-note").innerHTML = observed
    ? "<span></span> Observed SST · final product · 2° display stride from native 0.25° grid"
    : "<span></span> Schematic locations and pathways · not navigational · not a live analysis";
  if (observed) showObservedMetadata(); else selectZone(selectedZone);
}

for (const zone of zones) {
  const button = document.createElement("button");
  button.className = "marker";
  button.dataset.id = zone.id;
  button.dataset.kind = zone.kind;
  button.dataset.families = zone.families.join(" ");
  button.style.left = `${zone.x}%`;
  button.style.top = `${zone.y}%`;
  button.textContent = String(zone.n).padStart(2, "0");
  button.setAttribute("aria-label", `${zone.name}: ${zone.label}`);
  button.addEventListener("click", () => selectZone(zone));
  markers.append(button);
}

document.querySelectorAll(".lens").forEach(button => {
  button.addEventListener("click", () => {
    const lens = button.dataset.lens;
    document.querySelectorAll(".lens").forEach(item => {
      const active = item === button;
      item.classList.toggle("active", active);
      item.setAttribute("aria-pressed", String(active));
    });
    let visible = 0;
    document.querySelectorAll(".marker").forEach(marker => {
      const show = lens === "all" || marker.dataset.families.split(" ").includes(lens);
      marker.classList.toggle("filtered", !show);
      if (show) visible += 1;
    });
    count.textContent = visible;
  });
});

document.querySelectorAll(".map-mode").forEach(button => button.addEventListener("click", () => setMapMode(button.dataset.mode)));
renderObservedSst();
selectZone(zones[0]);
if (new URLSearchParams(window.location.search).get("mode") === "observed") setMapMode("observed");
