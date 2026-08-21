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
let currentMode = "conceptual";
let probeCell = null;

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

function colorFromStops(value, stops) {
  const bounded = Math.max(stops[0][0], Math.min(stops.at(-1)[0], value));
  let upper = stops.findIndex(stop => stop[0] >= bounded);
  if (upper < 1) upper = 1;
  const [lowValue, lowColor] = stops[upper - 1];
  const [highValue, highColor] = stops[upper];
  const mix = (bounded - lowValue) / (highValue - lowValue);
  const color = lowColor.map((channel, index) => Math.round(channel + (highColor[index] - channel) * mix));
  return `rgb(${color.join(",")})`;
}

function temperatureColor(value) {
  return colorFromStops(value, [
    [-2, [216, 244, 255]], [0, [141, 211, 232]], [8, [43, 156, 189]],
    [16, [56, 182, 138]], [22, [242, 207, 91]], [28, [240, 120, 66]], [32, [185, 39, 53]]
  ]);
}

function anomalyColor(value) {
  return colorFromStops(value, [
    [-5, [35, 59, 131]], [-3, [61, 119, 184]], [-1, [155, 203, 225]],
    [0, [238, 233, 216]], [1, [241, 187, 120]], [3, [207, 91, 71]], [5, [124, 35, 69]]
  ]);
}

function errorColor(value) {
  return colorFromStops(value, [
    [0.1, [244, 241, 222]], [0.2, [184, 216, 186]], [0.3, [110, 182, 167]],
    [0.4, [223, 179, 92]], [0.5, [184, 76, 76]], [0.6, [99, 44, 85]]
  ]);
}

function renderObservedField(data, colorFunction) {
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
    context.fillStyle = colorFunction(encoded / 100);
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
  if (probeCell) {
    const shiftedColumn = (probeCell.column + columns / 2) % columns;
    const x = (shiftedColumn + 0.5) * cellWidth;
    const y = (rows - probeCell.row - 0.5) * cellHeight;
    context.beginPath();
    context.arc(x, y, 7, 0, Math.PI * 2);
    context.strokeStyle = "#071b22";
    context.lineWidth = 5;
    context.stroke();
    context.beginPath();
    context.moveTo(x - 10, y); context.lineTo(x + 10, y);
    context.moveTo(x, y - 10); context.lineTo(x, y + 10);
    context.strokeStyle = "#ffffff";
    context.lineWidth = 2;
    context.stroke();
  }
}

function showObservedMetadata(data, mode) {
  const valid = data.values_c_hundredths.filter(value => value !== null);
  const summary = data.summary || {
    valid_ocean_cells: valid.length,
    minimum_c: Math.min(...valid) / 100,
    maximum_c: Math.max(...valid) / 100
  };
  const anomaly = mode === "anomaly";
  const error = mode === "error";
  const fieldClass = anomaly ? "REFERENCE-BASED" : error ? "UNCERTAINTY" : "ABSOLUTE";
  fields.index.textContent = `ATLAS 04 · ${fieldClass} SURFACE FIELD`;
  fields.name.textContent = anomaly ? "SST Anomaly" : error ? "Estimated SST Analysis Error" : "Sea Surface Temperature";
  fields.kind.textContent = `NOAA OISST V2.1 · ${data.date}`;
  fields.summary.textContent = anomaly
    ? `Departure from NOAA's 1971–2000 daily climatology across ${summary.valid_ocean_cells.toLocaleString()} displayed ocean cells. Range: ${summary.minimum_c.toFixed(1)}–${summary.maximum_c.toFixed(1)}°C.`
    : error
      ? `Time-matched estimated analysis error across ${summary.valid_ocean_cells.toLocaleString()} displayed ocean cells. Range: ${summary.minimum_c.toFixed(2)}–${summary.maximum_c.toFixed(2)}°C.`
    : `Absolute surface temperature across ${summary.valid_ocean_cells.toLocaleString()} displayed ocean cells. Range: ${summary.minimum_c.toFixed(1)}–${summary.maximum_c.toFixed(1)}°C.`;
  fields.role.textContent = anomaly ? "surface departure from climatology" : error ? "estimated surface analysis uncertainty" : "absolute surface thermal field";
  fields.depth.textContent = "sea surface · 0 m product level";
  fields.clock.textContent = `one day · ${data.date}`;
  fields.evidence.textContent = "observational analysis · D1";
  fields.boundary.textContent = data.boundary;
  fields.source.href = data.doi;
  fields.source.textContent = "Open NOAA dataset record →";
}

const latitudeBands = [
  ["Arctic", 60, 90],
  ["Northern midlatitudes", 30, 60],
  ["Tropics", -30, 30],
  ["Southern midlatitudes", -60, -30],
  ["Southern Ocean", -90, -60]
];

function valuePhrase(value, mode, includeSign = false) {
  if (mode === "anomaly") {
    const sign = value > 0 ? "+" : value < 0 ? "−" : "";
    const direction = value > 0 ? "warmer" : value < 0 ? "cooler" : "at baseline";
    return `${sign}${Math.abs(value).toFixed(2)}°C ${direction}`;
  }
  const precision = mode === "error" ? 2 : 1;
  return `${includeSign && value > 0 ? "+" : ""}${value.toFixed(precision)}°C`;
}

function renderTextSummary(data, mode) {
  const [rows, columns] = data.shape;
  const table = document.querySelector("#summary-body");
  table.replaceChildren();
  for (const [name, south, north] of latitudeBands) {
    const values = [];
    for (let row = 0; row < rows; row += 1) {
      const latitude = data.latitude.start + row * data.latitude.step;
      const inBand = latitude >= south && (north === 90 ? latitude <= north : latitude < north);
      if (!inBand) continue;
      for (let column = 0; column < columns; column += 1) {
        const encoded = data.values_c_hundredths[row * columns + column];
        if (encoded !== null) values.push(encoded / 100);
      }
    }
    const mean = values.reduce((total, value) => total + value, 0) / values.length;
    const row = document.createElement("tr");
    const cells = [name, valuePhrase(mean, mode), `${valuePhrase(Math.min(...values), mode)} to ${valuePhrase(Math.max(...values), mode)}`, values.length.toLocaleString()];
    cells.forEach((content, index) => {
      const cell = document.createElement(index === 0 ? "th" : "td");
      if (index === 0) cell.scope = "row";
      cell.textContent = content;
      row.append(cell);
    });
    table.append(row);
  }
  const fieldName = mode === "anomaly" ? "SST anomaly relative to 1971–2000" : mode === "error" ? "estimated SST analysis error" : "absolute sea surface temperature";
  document.querySelector("#map-a11y-summary").textContent = `Text equivalent for ${fieldName} on ${data.date}: five latitude-band rows report mean, range, and valid-cell count. Missing and land cells are excluded.`;
  document.querySelector("#summary-caption").textContent = `Latitude-band statistics for ${fieldName}; values are not area-weighted.`;
}

function normalizedLongitude(longitude) {
  return ((longitude + 180) % 360 + 360) % 360 - 180;
}

function probeCellFromCoordinates(latitude, longitude, data = window.OCEANLINES_OISST) {
  const [rows, columns] = data.shape;
  const boundedLatitude = Math.max(-90, Math.min(90, latitude));
  const longitude360 = (normalizedLongitude(longitude) + 360) % 360;
  const row = Math.max(0, Math.min(rows - 1, Math.round((boundedLatitude - data.latitude.start) / data.latitude.step)));
  const rawColumn = Math.round((longitude360 - data.longitude.start) / data.longitude.step);
  const column = ((rawColumn % columns) + columns) % columns;
  return {
    row,
    column,
    latitude: data.latitude.start + row * data.latitude.step,
    longitude: normalizedLongitude(data.longitude.start + column * data.longitude.step)
  };
}

function coordinatePhrase(value, positive, negative) {
  if (Math.abs(value) < 0.005) return "0.00°";
  return `${Math.abs(value).toFixed(2)}°${value > 0 ? positive : negative}`;
}

function probeValue(data, cell, mode) {
  const encoded = data.values_c_hundredths[cell.row * data.shape[1] + cell.column];
  if (encoded === null) return "land or missing";
  return valuePhrase(encoded / 100, mode);
}

function activeObservedField() {
  if (currentMode === "anomaly") return [window.OCEANLINES_OISST_ANOMALY, anomalyColor];
  if (currentMode === "error") return [window.OCEANLINES_OISST_ERROR, errorColor];
  return [window.OCEANLINES_OISST, temperatureColor];
}

function updateAtlasUrl() {
  const url = new URL(window.location.href);
  if (currentMode === "conceptual") {
    url.searchParams.delete("mode");
    url.searchParams.delete("lat");
    url.searchParams.delete("lon");
  } else {
    url.searchParams.set("mode", currentMode);
    if (probeCell) {
      url.searchParams.set("lat", probeCell.latitude.toFixed(3));
      url.searchParams.set("lon", probeCell.longitude.toFixed(3));
    }
  }
  window.history.replaceState({}, "", url);
}

function inspectCoordinates(latitude, longitude, updateUrl = true) {
  if (!Number.isFinite(latitude) || !Number.isFinite(longitude)) return;
  probeCell = probeCellFromCoordinates(latitude, longitude);
  document.querySelector("#probe-lat").value = probeCell.latitude.toFixed(3);
  document.querySelector("#probe-lon").value = probeCell.longitude.toFixed(3);
  const location = `${coordinatePhrase(probeCell.latitude, "N", "S")}, ${coordinatePhrase(probeCell.longitude, "E", "W")}`;
  const sst = probeValue(window.OCEANLINES_OISST, probeCell, "sst");
  const anomaly = probeValue(window.OCEANLINES_OISST_ANOMALY, probeCell, "anomaly");
  const error = probeValue(window.OCEANLINES_OISST_ERROR, probeCell, "error");
  document.querySelector("#probe-result").textContent = `Nearest 2° display cell · ${location}. SST: ${sst}. Anomaly: ${anomaly}. Estimated analysis error: ${error}. Surface product values; not heat content or transport.`;
  const [data, colorFunction] = activeObservedField();
  renderObservedField(data, colorFunction);
  if (updateUrl) updateAtlasUrl();
}

function setMapMode(mode) {
  if (mode === "observed") mode = "sst";
  const observed = mode !== "conceptual";
  const anomaly = mode === "anomaly";
  const error = mode === "error";
  currentMode = mode;
  const data = anomaly ? window.OCEANLINES_OISST_ANOMALY : error ? window.OCEANLINES_OISST_ERROR : window.OCEANLINES_OISST;
  document.querySelectorAll(".map-mode").forEach(button => {
    const active = button.dataset.mode === mode;
    button.classList.toggle("active", active);
    button.setAttribute("aria-pressed", String(active));
  });
  document.querySelector("#conceptual-map").hidden = observed;
  document.querySelector("#sst-canvas").hidden = !observed;
  document.querySelector("#observed-stamp").hidden = !observed;
  document.querySelector("#temperature-key").hidden = !observed;
  document.querySelector("#temperature-key").classList.toggle("anomaly", anomaly);
  document.querySelector("#temperature-key").classList.toggle("error", error);
  document.querySelector("#map-data-summary").hidden = !observed;
  markers.hidden = observed;
  document.querySelector("#map-stage").classList.toggle("observed", observed);
  document.querySelectorAll(".lens").forEach(button => { button.disabled = observed; });
  document.querySelector("#observed-title").textContent = anomaly ? "OBSERVATIONAL · SURFACE ANOMALY" : error ? "OBSERVATIONAL · ESTIMATED ERROR" : "OBSERVATIONAL · ABSOLUTE SURFACE";
  document.querySelector("#observed-status").textContent = anomaly ? "NOAA OISST v2.1 · 1971–2000 BASELINE" : error ? "NOAA OISST v2.1 · TIME-MATCHED ERROR" : "NOAA OISST v2.1 · FINAL · 2026-08-01";
  document.querySelector("#scale-min").textContent = anomaly ? "−5°C cooler" : error ? "0.1°C lower" : "−2°C";
  document.querySelector("#scale-max").textContent = anomaly ? "+5°C warmer" : error ? "0.6°C higher" : "32°C";
  document.querySelector("#temperature-key").setAttribute("aria-label", anomaly ? "SST anomaly scale from five degrees cooler to five degrees warmer than baseline" : error ? "Estimated analysis error scale from lower to higher error" : "Absolute sea surface temperature color scale");
  const canvas = document.querySelector("#sst-canvas");
  canvas.setAttribute("aria-label", anomaly ? "NOAA OISST anomaly for 1 August 2026 relative to 1971 to 2000, displayed on a two-degree equirectangular grid." : error ? "NOAA OISST estimated analysis error for 1 August 2026, displayed on a two-degree equirectangular grid." : "NOAA OISST absolute sea surface temperature for 1 August 2026, displayed on a two-degree equirectangular grid.");
  document.querySelector("#map-note").innerHTML = observed
    ? `<span></span> ${anomaly ? "SST anomaly · 1971–2000 reference · symmetric ±5°C display clamp" : error ? "estimated analysis error · 0.1–0.6°C display clamp" : "absolute SST"} · equirectangular · antimeridian seam · 2° display stride`
    : "<span></span> Schematic, permeable, moving regions · not fixed boundaries · not a live analysis";
  if (observed) {
    renderObservedField(data, anomaly ? anomalyColor : error ? errorColor : temperatureColor);
    showObservedMetadata(data, mode);
    renderTextSummary(data, mode);
    if (probeCell) inspectCoordinates(probeCell.latitude, probeCell.longitude, false);
  } else selectZone(selectedZone);
  updateAtlasUrl();
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
document.querySelector("#coordinate-probe").addEventListener("submit", event => {
  event.preventDefault();
  inspectCoordinates(Number(document.querySelector("#probe-lat").value), Number(document.querySelector("#probe-lon").value));
});
document.querySelector("#sst-canvas").addEventListener("click", event => {
  const rectangle = event.currentTarget.getBoundingClientRect();
  const longitude = (event.clientX - rectangle.left) / rectangle.width * 360 - 180;
  const latitude = 90 - (event.clientY - rectangle.top) / rectangle.height * 180;
  inspectCoordinates(latitude, longitude);
});
selectZone(zones[0]);
const requestedParameters = new URLSearchParams(window.location.search);
const requestedMode = requestedParameters.get("mode");
if (["observed", "sst", "anomaly", "error"].includes(requestedMode)) setMapMode(requestedMode);
if (currentMode !== "conceptual" && requestedParameters.has("lat") && requestedParameters.has("lon")) {
  inspectCoordinates(Number(requestedParameters.get("lat")), Number(requestedParameters.get("lon")));
}
