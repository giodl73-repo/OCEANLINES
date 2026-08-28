const zones = [
  { id: "indo-pacific-warm-pool", n: 1, name: "Indo-Pacific Warm Pool", kind: "reservoir", label: "Heat continent", role: "persistent reservoir", depth: "surface / upper ocean", clock: "persistent; seasonally breathing", evidence: "conceptual · O18", x: 85, y: 42.4, families: ["heatmass", "oceanbelts"], summary: "The largest persistent expanse of very warm surface water: a continent-like reservoir whose edge moves with threshold, season, and dataset.", boundary: "A warm surface footprint is not a full-depth heat-content integral, and its diagnostic boundary is not a material wall.", source: "https://www.climate.gov/news-features/featured-images/warm-pool-indo-pacific-ocean-has-almost-doubled-size-changing-global" },
  { id: "western-hemisphere-warm-pool", n: 2, name: "Western Hemisphere Warm Pool", kind: "reservoir", label: "Seasonal heat continent", role: "seasonal reservoir", depth: "surface / upper ocean", clock: "seasonal expansion", evidence: "conceptual · O19", x: 31.3, y: 41, families: ["heatmass"], summary: "A seasonally connected warm-water province spanning parts of the tropical eastern Pacific, Gulf of Mexico, Caribbean, and western tropical Atlantic.", boundary: "Central America divides the ocean basins even when a temperature threshold visually joins the warm regions.", source: "https://www.aoml.noaa.gov/phod/research/tav/awp/" },
  { id: "northeast-pacific-blob", n: 3, name: "Northeast Pacific Blob", kind: "transient", label: "Heat blob", role: "marine heatwave anomaly", depth: "surface with subsurface remnant", clock: "episodic / multi-year", evidence: "observational · O20–O21", x: 12.8, y: 27.1, families: ["heatmass"], summary: "A named marine heatwave demonstrates why a heat blob is an event relative to a baseline—not a permanent ocean province.", boundary: "Its surface expression does not determine its full-depth energy or prove a single cause.", source: "https://doi.org/10.1002/2016GL071039" },
  { id: "el-nino-tongue", n: 4, name: "El Niño Tongue", kind: "transient", label: "Heat tongue", role: "basin-scale anomaly", depth: "surface / thermocline coupled", clock: "interannual", evidence: "conceptual", x: 18.1, y: 44.8, families: ["heatmass", "oceanbelts"], summary: "An eastward-reaching equatorial anomaly: a tongue because its geometry and evolution matter as much as its peak temperature.", boundary: "The atlas shape is schematic and is not an event declaration or an ENSO index.", source: "../SOURCE-REGISTER.md" },
  { id: "gulf-stream", n: 5, name: "Gulf Stream", kind: "pathway", label: "Heat river", role: "western boundary current", depth: "surface intensified; deep structure", clock: "persistent and variable", evidence: "conceptual · O2", x: 33.8, y: 30, families: ["oceanrealms", "oceanbelts"], summary: "A narrow, fast pathway that exports warm water poleward and sheds moving rings into the surrounding ocean.", boundary: "Current speed and water temperature do not, by themselves, give heat transport across a section.", source: "https://www.whoi.edu/ocean-learning-hub/ocean-topics/how-the-ocean-works/ocean-circulation/currents-gyres-eddies/" },
  { id: "kuroshio", n: 6, name: "Kuroshio", kind: "pathway", label: "Heat river", role: "western boundary current", depth: "surface intensified; deep structure", clock: "persistent and variable", evidence: "conceptual · O2", x: 87.2, y: 30.5, families: ["oceanrealms", "oceanbelts"], summary: "The North Pacific counterpart in the map grammar: a swift boundary current, extension, and ring-forming system.", boundary: "The analogy to the Gulf Stream is structural, not an assertion of identical forcing, geometry, or transport.", source: "https://www.whoi.edu/ocean-learning-hub/ocean-topics/how-the-ocean-works/ocean-circulation/currents-gyres-eddies/" },
  { id: "agulhas", n: 7, name: "Agulhas System", kind: "pathway", label: "River and moving islands", role: "boundary current / leakage", depth: "upper ocean to intermediate", clock: "persistent with episodic rings", evidence: "conceptual", x: 56.6, y: 59.5, families: ["oceanrealms"], summary: "A current system whose retroflection and rings make exchange look less like a pipe and more like parcels escaping a moving border.", boundary: "The marker does not quantify leakage or attribute downstream climate effects.", source: "../SOURCE-REGISTER.md" },
  { id: "antarctic-circumpolar-current", n: 8, name: "Antarctic Circumpolar Current", kind: "pathway", label: "Circumpolar belt", role: "fronted zonal current", depth: "deep-reaching fronts", clock: "persistent and meandering", evidence: "observational · O4, O8–O9", x: 78.8, y: 67, families: ["oceanrealms", "oceanbelts"], summary: "Earth's clearest ocean belt: a deep-reaching, eastward current whose fronts inhibit exchange while eddies and regional pathways leak heat across them.", boundary: "The ACC is not a solid cold wall and Drake Passage is not a thermal plug.", source: "https://doi.org/10.1175/JPO-D-19-0266.1" },
  { id: "circumpolar-deep-water", n: 9, name: "Circumpolar Deep Water", kind: "buried", label: "Buried heat continent", role: "subsurface reservoir / source water", depth: "intermediate to deep; region dependent", clock: "persistent with changing access", evidence: "synthesis · O10, O14", x: 49.4, y: 66.7, families: ["heatmass", "oceanrealms"], summary: "Relatively warm subsurface water can approach Antarctic margins beneath a cold surface, making vertical structure central to ice-shelf exposure.", boundary: "Offshore presence does not equal delivery to a cavity; fronts, shelf breaks, troughs, mixing, and winds intervene.", source: "https://doi.org/10.1029/2018RG000624" },
  { id: "atlantic-water-arctic", n: 10, name: "Atlantic Water in the Arctic", kind: "buried", label: "Buried heat continent", role: "subsurface inflow and reservoir", depth: "below the cold, fresh halocline", clock: "persistent and variable", evidence: "observational synthesis · O22", x: 57.5, y: 16.2, families: ["heatmass", "oceanrealms"], summary: "Warm Atlantic-origin water can sit beneath a colder, fresher lid: the Arctic example of why the surface can conceal a large thermal contrast.", boundary: "Subsurface temperature does not determine when, where, or how much heat reaches sea ice or the atmosphere.", source: "https://doi.org/10.3389/fmars.2019.00416" },
  { id: "drake-passage", n: 11, name: "Drake Passage", kind: "gate", label: "Heat gate", role: "circumpolar transport section", depth: "full water column", clock: "persistent geometry; variable flow", evidence: "observational / modeled · O4–O7", x: 33.1, y: 66.1, families: ["oceanrealms", "oceanbelts"], summary: "The narrowest major gate on the circumpolar route. It makes ACC transport measurable and exposes how geometry reorganizes global circulation.", boundary: "Closing the gate in a model changes many coupled circulations; it is not equivalent to simply sending warm water south.", source: "https://doi.org/10.1175/JCLI-D-15-0554.1" },
  { id: "indonesian-throughflow", n: 12, name: "Indonesian Throughflow", kind: "gate", label: "Archipelagic heat gate", role: "inter-basin exchange", depth: "multiple constrained passages", clock: "persistent and variable", evidence: "conceptual", x: 80.5, y: 46.2, families: ["oceanrealms"], summary: "A branching tropical gate where land geometry constrains exchange between the Pacific and Indian oceans.", boundary: "A point marker hides multiple straits, vertical structure, tides, mixing, and seasonal reversals.", source: "../SOURCE-REGISTER.md" }
];

const markers = document.querySelector("#markers");
const count = document.querySelector("#visible-count");
const fields = Object.fromEntries(["index", "name", "kind", "summary", "role", "depth", "clock", "evidence", "boundary", "source"].map(key => [key, document.querySelector(`#zone-${key}`)]));
let selectedZone = zones[0];
let currentMode = "conceptual";
let probeCell = null;
let ringLatitude = 64;

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
  const cellWidth = Math.abs(data.longitude.step) / 360 * canvas.width;
  const cellHeight = Math.abs(data.latitude.step) / 180 * canvas.height;
  context.fillStyle = "#30454b";
  context.fillRect(0, 0, canvas.width, canvas.height);
  const domainNorth = data.latitude.start + (rows - 1) * data.latitude.step + Math.abs(data.latitude.step) / 2;
  const domainSouth = data.latitude.start - Math.abs(data.latitude.step) / 2;
  context.fillStyle = "#c8bda5";
  context.fillRect(0, (90 - domainNorth) / 180 * canvas.height, canvas.width, (domainNorth - domainSouth) / 180 * canvas.height);
  data.values_c_hundredths.forEach((encoded, index) => {
    if (encoded === null) return;
    const row = Math.floor(index / columns);
    const column = index % columns;
    const longitude = normalizedLongitude(data.longitude.start + column * data.longitude.step);
    const latitude = data.latitude.start + row * data.latitude.step;
    const x = (longitude + 180) / 360 * canvas.width - cellWidth / 2;
    const y = (90 - latitude) / 180 * canvas.height - cellHeight / 2;
    context.fillStyle = colorFunction(encoded / 100);
    context.fillRect(x, y, Math.ceil(cellWidth), Math.ceil(cellHeight));
    if (x < 0) context.fillRect(x + canvas.width, y, Math.ceil(cellWidth), Math.ceil(cellHeight));
    if (x + cellWidth > canvas.width) context.fillRect(x - canvas.width, y, Math.ceil(cellWidth), Math.ceil(cellHeight));
  });
  context.strokeStyle = "rgba(255,255,255,.24)";
  context.lineWidth = 1;
  for (let longitude = 60; longitude < 360; longitude += 60) {
    context.beginPath(); context.moveTo(longitude / 360 * canvas.width, 0); context.lineTo(longitude / 360 * canvas.width, canvas.height); context.stroke();
  }
  for (let latitude = 30; latitude < 180; latitude += 30) {
    context.beginPath(); context.moveTo(0, latitude / 180 * canvas.height); context.lineTo(canvas.width, latitude / 180 * canvas.height); context.stroke();
  }
  if (data.schema === "oceanlines.oisst.snapshot.v2") {
    const rings = pairedRingRows(ringLatitude, data);
    for (const [ring, color] of [[rings.north, "#5ee2d6"], [rings.south, "#ff6f61"]]) {
      const y = (90 - ring.latitude) / 180 * canvas.height;
      context.beginPath(); context.moveTo(0, y); context.lineTo(canvas.width, y);
      context.strokeStyle = "#071b22"; context.lineWidth = 5; context.stroke();
      context.beginPath(); context.moveTo(0, y); context.lineTo(canvas.width, y);
      context.strokeStyle = color; context.lineWidth = 2; context.setLineDash([8, 5]); context.stroke();
      context.setLineDash([]);
    }
  }
  if (probeCell) {
    const displayProbe = probeCellFromCoordinates(probeCell.latitude, probeCell.longitude, data);
    const x = (displayProbe.longitude + 180) / 360 * canvas.width;
    const y = (90 - displayProbe.latitude) / 180 * canvas.height;
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
  const subsurface = mode === "argo700";
  const error = mode === "error";
  const fieldClass = anomaly || subsurface ? "REFERENCE-BASED" : error ? "UNCERTAINTY" : "ABSOLUTE";
  fields.index.textContent = `ATLAS 09 · ${fieldClass} ${subsurface ? "PRESSURE-LAYER" : "SURFACE"} FIELD`;
  fields.name.textContent = subsurface ? "700 dbar Temperature Anomaly" : anomaly ? "SST Anomaly" : error ? "Estimated SST Analysis Error" : "Sea Surface Temperature";
  fields.kind.textContent = subsurface ? `SCRIPPS RG ARGO · ${data.month}` : `NOAA OISST V2.1 · ${data.date}`;
  fields.summary.textContent = subsurface
    ? `Objectively mapped potential-temperature anomaly at ${data.pressure_dbar.toFixed(0)} dbar across ${summary.valid_ocean_cells.toLocaleString()} displayed cells. Range: ${summary.minimum_c.toFixed(2)}–${summary.maximum_c.toFixed(2)}°C.`
    : anomaly
    ? `Departure from NOAA's 1971–2000 daily climatology across ${summary.valid_ocean_cells.toLocaleString()} displayed ocean cells. Range: ${summary.minimum_c.toFixed(1)}–${summary.maximum_c.toFixed(1)}°C.`
    : error
      ? `Time-matched estimated analysis error across ${summary.valid_ocean_cells.toLocaleString()} displayed ocean cells. Range: ${summary.minimum_c.toFixed(2)}–${summary.maximum_c.toFixed(2)}°C.`
    : `Absolute surface temperature across ${summary.valid_ocean_cells.toLocaleString()} displayed ocean cells. Range: ${summary.minimum_c.toFixed(1)}–${summary.maximum_c.toFixed(1)}°C.`;
  fields.role.textContent = subsurface ? "subsurface departure from climatology" : anomaly ? "surface departure from climatology" : error ? "estimated surface analysis uncertainty" : "absolute surface thermal field";
  fields.depth.textContent = subsurface ? `${data.pressure_dbar.toFixed(0)} dbar pressure surface · not a fixed geometric depth` : "sea surface · 0 m product level";
  fields.clock.textContent = subsurface ? `monthly extension · ${data.month}` : `one day · ${data.date}`;
  fields.evidence.textContent = subsurface ? "Argo-only objective analysis · D2" : "observational analysis · D1";
  fields.boundary.textContent = data.boundary;
  fields.source.href = subsurface ? data.query_url : data.doi;
  fields.source.textContent = subsurface ? "Open the fixed Scripps product →" : "Open NOAA dataset record →";
  document.querySelector("#map-insight").textContent = subsurface
    ? "This is the atlas's first look below the surface: July 2026 departure from the RG seasonal climatology at 700 dbar. It reveals depth-specific change, but not absolute warmth, water-column heat content, circulation, or delivery onto the Antarctic shelf."
    : anomaly
    ? "This one-day surface map shows where temperature departed from the 1971–2000 daily baseline. It shows the pattern, not why it occurred or how much heat is stored below the surface."
    : error
      ? "This layer shows where the surface analysis carries higher or lower estimated error. It qualifies the mapped product; it is not forecast error or full-budget uncertainty."
      : "This one-day surface map shows the familiar warm tropics and cold poles, plus regional structure. Absolute surface temperature is not an anomaly, full-depth heat content, or heat transport.";
}

const latitudeBands = [
  ["Arctic", 60, 90],
  ["Northern midlatitudes", 30, 60],
  ["Tropics", -30, 30],
  ["Southern midlatitudes", -60, -30],
  ["Southern Ocean", -90, -60]
];

function valuePhrase(value, mode, includeSign = false) {
  if (mode === "anomaly" || mode === "argo700") {
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
  const fieldName = mode === "argo700" ? "700 dbar potential-temperature anomaly relative to the RG 2019 climatology" : mode === "anomaly" ? "SST anomaly relative to 1971–2000" : mode === "error" ? "estimated SST analysis error" : "absolute sea surface temperature";
  document.querySelector("#map-a11y-summary").textContent = `Text equivalent for ${fieldName} on ${data.date || data.month}: five latitude-band rows report mean, range, and valid-cell count. Missing and land cells are excluded.`;
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

function pairedRingRows(magnitude, data = window.OCEANLINES_OISST) {
  const bounded = Math.max(0, Math.min(89, Math.abs(magnitude)));
  const north = probeCellFromCoordinates(bounded, 0, data);
  const south = probeCellFromCoordinates(-bounded, 0, data);
  return { requested: bounded, north: { row: north.row, latitude: north.latitude }, south: { row: south.row, latitude: south.latitude } };
}

function longestCyclicRun(flags) {
  if (flags.every(Boolean)) return flags.length;
  let longest = 0;
  let current = 0;
  for (let index = 0; index < flags.length * 2; index += 1) {
    current = flags[index % flags.length] ? Math.min(current + 1, flags.length) : 0;
    longest = Math.max(longest, current);
  }
  return longest;
}

function ringStatistics(data, ring, geometryData = window.OCEANLINES_OISST) {
  const columns = data.shape[1];
  const encoded = data.values_c_hundredths.slice(ring.row * columns, (ring.row + 1) * columns);
  const geometryEncoded = geometryData.values_c_hundredths.slice(ring.row * columns, (ring.row + 1) * columns);
  const ocean = geometryEncoded.map(value => value !== null);
  const values = encoded.filter(value => value !== null).map(value => value / 100);
  const arcs = ocean.every(Boolean) ? 1 : ocean.reduce((count, value, index) => count + (value && !ocean[(index - 1 + columns) % columns] ? 1 : 0), 0);
  const mean = values.length ? values.reduce((total, value) => total + value, 0) / values.length : null;
  return {
    encoded,
    valid: values.length,
    coverage: values.length / columns * 100,
    arcs,
    longestDegrees: longestCyclicRun(ocean) * Math.abs(data.longitude.step),
    mean,
    minimum: values.length ? Math.min(...values) : null,
    maximum: values.length ? Math.max(...values) : null
  };
}

function renderRingStrip(canvas, data, statistics, colorFunction) {
  const context = canvas.getContext("2d");
  const columns = data.shape[1];
  const width = canvas.width / columns;
  context.fillStyle = "#c8bda5";
  context.fillRect(0, 0, canvas.width, canvas.height);
  statistics.encoded.forEach((value, column) => {
    if (value === null) return;
    const longitude = normalizedLongitude(data.longitude.start + column * data.longitude.step);
    const x = (longitude + 180) / 360 * canvas.width - width / 2;
    context.fillStyle = colorFunction(value / 100);
    context.fillRect(x, 0, Math.ceil(width), canvas.height);
    if (x < 0) context.fillRect(x + canvas.width, 0, Math.ceil(width), canvas.height);
    if (x + width > canvas.width) context.fillRect(x - canvas.width, 0, Math.ceil(width), canvas.height);
  });
  context.strokeStyle = "rgba(255,255,255,.45)";
  for (let longitude = 60; longitude < 360; longitude += 60) {
    context.beginPath(); context.moveTo(longitude / 360 * canvas.width, 0); context.lineTo(longitude / 360 * canvas.width, canvas.height); context.stroke();
  }
}

function renderRingComparison(data, mode, colorFunction) {
  const rings = pairedRingRows(ringLatitude, data);
  const specifications = [
    ["north", "Northern", rings.north, document.querySelector("#north-ring")],
    ["south", "Southern", rings.south, document.querySelector("#south-ring")]
  ];
  const body = document.querySelector("#ring-body");
  body.replaceChildren();
  const summaries = [];
  for (const [id, name, ring, canvas] of specifications) {
    const statistics = ringStatistics(data, ring);
    renderRingStrip(canvas, data, statistics, colorFunction);
    const coordinate = coordinatePhrase(ring.latitude, "N", "S");
    document.querySelector(`#${id}-ring-label`).textContent = `${name} ring · ${coordinate}`;
    canvas.setAttribute("aria-label", `${name} longitude strip at ${coordinate}; land-or-missing gaps use beige and the displayed field uses the active map scale.`);
    const row = document.createElement("tr");
    const range = statistics.mean === null ? "No ocean values" : `${valuePhrase(statistics.mean, mode)} mean; ${valuePhrase(statistics.minimum, mode)} to ${valuePhrase(statistics.maximum, mode)}`;
    const cells = [`${name} · ${coordinate}`, `${statistics.valid}/${data.shape[1]} cells · ${statistics.coverage.toFixed(1)}%`, String(statistics.arcs), `${statistics.longestDegrees.toFixed(0)}° longitude`, range];
    cells.forEach((content, index) => {
      const cell = document.createElement(index === 0 ? "th" : "td");
      if (index === 0) cell.scope = "row";
      cell.textContent = content;
      row.append(cell);
    });
    body.append(row);
    summaries.push(`${name} ${coordinate}: ${statistics.coverage.toFixed(1)}% analyzed-water coverage in ${statistics.arcs} arc${statistics.arcs === 1 ? "" : "s"}; longest ${statistics.longestDegrees.toFixed(0)}°`);
  }
  const fieldName = mode === "anomaly" ? "SST anomaly" : mode === "error" ? "estimated analysis error" : "absolute SST";
  document.querySelector("#ring-summary").textContent = `${summaries.join(". ")}. Display-grid geometry with ${fieldName}; not a current, barrier strength, heat-content, or transport measurement.`;
  document.querySelector("#ring-caption").textContent = `Latitude-ring geometry and ${fieldName} statistics; values are not area-weighted.`;
  renderPolarMirrors(data, mode, colorFunction);
  renderLatitudeLadder();
}

function renderPolarMirror(canvas, data, colorFunction, hemisphere) {
  const context = canvas.getContext("2d");
  const size = canvas.width;
  const center = size / 2;
  const radius = center - 10;
  const capLatitude = 40;
  const image = context.createImageData(size, size);
  const colorCache = new Map();
  const [rows, columns] = data.shape;
  const background = [6, 23, 28];
  const missing = [200, 189, 165];
  const colorFor = encoded => {
    if (encoded === null) return missing;
    if (!colorCache.has(encoded)) colorCache.set(encoded, colorFunction(encoded / 100).match(/\d+/g).map(Number));
    return colorCache.get(encoded);
  };
  for (let y = 0; y < size; y += 1) {
    for (let x = 0; x < size; x += 1) {
      const dx = x + 0.5 - center;
      const dy = y + 0.5 - center;
      const distance = Math.hypot(dx, dy);
      let color = background;
      if (distance <= radius) {
        const magnitude = 90 - distance / radius * (90 - capLatitude);
        const latitude = hemisphere === "north" ? magnitude : -magnitude;
        const longitude = Math.atan2(dx, -dy) * 180 / Math.PI;
        const cell = probeCellFromCoordinates(latitude, longitude, data);
        color = colorFor(data.values_c_hundredths[cell.row * columns + cell.column]);
      }
      const offset = (y * size + x) * 4;
      image.data[offset] = color[0];
      image.data[offset + 1] = color[1];
      image.data[offset + 2] = color[2];
      image.data[offset + 3] = 255;
    }
  }
  context.putImageData(image, 0, 0);
  context.strokeStyle = "rgba(255,255,255,.35)";
  context.lineWidth = 1;
  for (const latitude of [40, 60, 80]) {
    const ringRadius = (90 - latitude) / (90 - capLatitude) * radius;
    context.beginPath(); context.arc(center, center, ringRadius, 0, Math.PI * 2); context.stroke();
  }
  for (let longitude = 0; longitude < 360; longitude += 90) {
    const angle = longitude * Math.PI / 180;
    context.beginPath(); context.moveTo(center, center);
    context.lineTo(center + Math.sin(angle) * radius, center - Math.cos(angle) * radius); context.stroke();
  }
  const selected = pairedRingRows(ringLatitude, data)[hemisphere];
  const selectedMagnitude = Math.abs(selected.latitude);
  const selectedVisible = selectedMagnitude >= capLatitude;
  if (selectedVisible) {
    const selectedRadius = (90 - selectedMagnitude) / (90 - capLatitude) * radius;
    context.beginPath(); context.arc(center, center, selectedRadius, 0, Math.PI * 2);
    context.strokeStyle = "#071b22"; context.lineWidth = 6; context.stroke();
    context.beginPath(); context.arc(center, center, selectedRadius, 0, Math.PI * 2);
    context.strokeStyle = "#ffb250"; context.lineWidth = 2; context.setLineDash([9, 6]); context.stroke();
    context.setLineDash([]);
  }
  return { selected, selectedVisible };
}

function renderPolarMirrors(data, mode, colorFunction) {
  const northCanvas = document.querySelector("#north-polar");
  const southCanvas = document.querySelector("#south-polar");
  const north = renderPolarMirror(northCanvas, data, colorFunction, "north");
  const south = renderPolarMirror(southCanvas, data, colorFunction, "south");
  const fieldName = mode === "anomaly" ? "SST anomaly" : mode === "error" ? "estimated analysis error" : "absolute SST";
  const selectedText = north.selectedVisible && south.selectedVisible
    ? `Amber circles mark sampled ${coordinatePhrase(north.selected.latitude, "N", "S")} and ${coordinatePhrase(south.selected.latitude, "N", "S")}.`
    : `The selected ${ringLatitude.toFixed(1)}° request lies outside at least one 40–90° cap, so no out-of-domain circle is drawn.`;
  const orientation = "Both caps place 0° longitude at top and 90°E at right; the south is an intentional comparison mirror.";
  document.querySelector("#polar-summary").textContent = `${fieldName} on ${data.date}. ${selectedText} ${orientation} Surface display only; not bathymetry, sea ice, circulation, or heat transport.`;
  northCanvas.setAttribute("aria-label", `Northern 40–90° polar cap showing ${fieldName}. ${selectedText} ${orientation}`);
  southCanvas.setAttribute("aria-label", `Southern 40–90° polar comparison mirror showing ${fieldName}. ${selectedText} ${orientation}`);
}

function latitudeLadder(data = window.OCEANLINES_OISST) {
  const ladder = [];
  for (let magnitude = 0; magnitude <= 88; magnitude += 2) {
    const rings = pairedRingRows(magnitude, data);
    ladder.push({
      magnitude,
      north: { ...rings.north, ...ringStatistics(data, rings.north, data) },
      south: { ...rings.south, ...ringStatistics(data, rings.south, data) }
    });
  }
  return ladder;
}

function renderLatitudeLadder() {
  const data = window.OCEANLINES_OISST;
  const ladder = latitudeLadder(data);
  const canvas = document.querySelector("#continuity-chart");
  const context = canvas.getContext("2d");
  const margin = { left: 54, right: 20, top: 20, bottom: 42 };
  const width = canvas.width - margin.left - margin.right;
  const height = canvas.height - margin.top - margin.bottom;
  const xFor = magnitude => margin.left + Math.min(88, magnitude) / 88 * width;
  const yFor = coverage => margin.top + (100 - coverage) / 100 * height;
  context.fillStyle = "#06171c";
  context.fillRect(0, 0, canvas.width, canvas.height);
  context.font = "11px ui-monospace, monospace";
  context.textAlign = "right";
  context.textBaseline = "middle";
  for (const coverage of [0, 25, 50, 75, 100]) {
    const y = yFor(coverage);
    context.beginPath(); context.moveTo(margin.left, y); context.lineTo(canvas.width - margin.right, y);
    context.strokeStyle = "rgba(146,170,169,.25)"; context.lineWidth = 1; context.stroke();
    context.fillStyle = "#92aaa9"; context.fillText(`${coverage}%`, margin.left - 8, y);
  }
  context.textAlign = "center";
  context.textBaseline = "top";
  for (const magnitude of [0, 30, 60, 88]) {
    const x = xFor(magnitude);
    context.beginPath(); context.moveTo(x, margin.top); context.lineTo(x, canvas.height - margin.bottom);
    context.strokeStyle = "rgba(146,170,169,.14)"; context.stroke();
    context.fillStyle = "#92aaa9"; context.fillText(`${magnitude}°`, x, canvas.height - margin.bottom + 10);
  }
  const drawSeries = (hemisphere, color, dashed) => {
    context.beginPath();
    ladder.forEach((point, index) => {
      const x = xFor(point.magnitude);
      const y = yFor(point[hemisphere].coverage);
      if (index === 0) context.moveTo(x, y); else context.lineTo(x, y);
    });
    context.strokeStyle = "#071b22"; context.lineWidth = 7; context.setLineDash([]); context.stroke();
    context.strokeStyle = color; context.lineWidth = 3; context.setLineDash(dashed ? [10, 7] : []); context.stroke();
    context.setLineDash([]);
  };
  drawSeries("north", "#5ee2d6", false);
  drawSeries("south", "#ff6f61", true);
  const selected = pairedRingRows(ringLatitude, data);
  const selectedNorth = ringStatistics(data, selected.north, data);
  const selectedSouth = ringStatistics(data, selected.south, data);
  const selectedX = xFor(ringLatitude);
  context.beginPath(); context.moveTo(selectedX, margin.top); context.lineTo(selectedX, canvas.height - margin.bottom);
  context.strokeStyle = "#ffb250"; context.lineWidth = 2; context.stroke();
  for (const [statistics, color] of [[selectedNorth, "#5ee2d6"], [selectedSouth, "#ff6f61"]]) {
    context.beginPath(); context.arc(selectedX, yFor(statistics.coverage), 6, 0, Math.PI * 2);
    context.fillStyle = color; context.fill(); context.strokeStyle = "#071b22"; context.lineWidth = 3; context.stroke();
  }
  const body = document.querySelector("#continuity-body");
  body.replaceChildren();
  ladder.forEach(point => {
    const row = document.createElement("tr");
    const cells = [
      `${point.magnitude}°`,
      coordinatePhrase(point.north.latitude, "N", "S"),
      `${point.north.valid}/${data.shape[1]} · ${point.north.coverage.toFixed(1)}%`,
      `${point.north.arcs} / ${point.north.longestDegrees.toFixed(0)}°`,
      coordinatePhrase(point.south.latitude, "N", "S"),
      `${point.south.valid}/${data.shape[1]} · ${point.south.coverage.toFixed(1)}%`,
      `${point.south.arcs} / ${point.south.longestDegrees.toFixed(0)}°`
    ];
    cells.forEach((content, index) => {
      const cell = document.createElement(index === 0 ? "th" : "td");
      if (index === 0) cell.scope = "row";
      cell.textContent = content;
      row.append(cell);
    });
    body.append(row);
  });
  const nearCircumpolar = hemisphere => ladder.find(point => point[hemisphere].coverage >= 95 && point[hemisphere].longestDegrees >= 300);
  const northThreshold = nearCircumpolar("north");
  const southThreshold = nearCircumpolar("south");
  const selectedText = `Selected ${ringLatitude.toFixed(1)}° request: north ${selectedNorth.coverage.toFixed(1)}%, south ${selectedSouth.coverage.toFixed(1)}%.`;
  const thresholdText = `First scan rows meeting the declared ≥95% coverage and ≥300° longest-arc threshold: south ${southThreshold.magnitude}° request (${coordinatePhrase(southThreshold.south.latitude, "N", "S")}); north ${northThreshold.magnitude}° request (${coordinatePhrase(northThreshold.north.latitude, "N", "S")}).`;
  document.querySelector("#continuity-summary").textContent = `${thresholdText} ${selectedText} Product-mask topology only; not a circulation boundary.`;
  canvas.setAttribute("aria-label", `Latitude continuity ladder. Northern coverage is a solid line and southern coverage is dashed. ${thresholdText} ${selectedText}`);
}

function coordinatePhrase(value, positive, negative) {
  if (Math.abs(value) < 0.005) return "0.00°";
  return `${Math.abs(value).toFixed(2)}°${value > 0 ? positive : negative}`;
}

function probeValue(data, latitude, longitude, mode) {
  const cell = probeCellFromCoordinates(latitude, longitude, data);
  const encoded = data.values_c_hundredths[cell.row * data.shape[1] + cell.column];
  if (encoded === null) return "land or missing";
  return valuePhrase(encoded / 100, mode);
}

function activeObservedField() {
  if (currentMode === "argo700") return [window.OCEANLINES_ARGO_TEMPERATURE_ANOMALY, anomalyColor];
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
    url.searchParams.delete("ring");
  } else {
    url.searchParams.set("mode", currentMode);
    url.searchParams.set("ring", ringLatitude.toFixed(3));
    if (probeCell) {
      url.searchParams.set("lat", probeCell.latitude.toFixed(3));
      url.searchParams.set("lon", probeCell.longitude.toFixed(3));
    }
  }
  window.history.replaceState({}, "", url);
}

function setRingLatitude(latitude, updateUrl = true) {
  if (!Number.isFinite(latitude)) return;
  ringLatitude = Math.max(0, Math.min(89, Math.abs(latitude)));
  document.querySelector("#ring-lat").value = ringLatitude.toFixed(3);
  if (currentMode !== "conceptual") {
    const [data, colorFunction] = activeObservedField();
    renderObservedField(data, colorFunction);
    if (currentMode !== "argo700") renderRingComparison(data, currentMode, colorFunction);
  }
  if (updateUrl) updateAtlasUrl();
}

function inspectCoordinates(latitude, longitude, updateUrl = true) {
  if (!Number.isFinite(latitude) || !Number.isFinite(longitude)) return;
  const [activeData] = activeObservedField();
  probeCell = probeCellFromCoordinates(latitude, longitude, activeData);
  document.querySelector("#probe-lat").value = probeCell.latitude.toFixed(3);
  document.querySelector("#probe-lon").value = probeCell.longitude.toFixed(3);
  const location = `${coordinatePhrase(probeCell.latitude, "N", "S")}, ${coordinatePhrase(probeCell.longitude, "E", "W")}`;
  const sst = probeValue(window.OCEANLINES_OISST, probeCell.latitude, probeCell.longitude, "sst");
  const anomaly = probeValue(window.OCEANLINES_OISST_ANOMALY, probeCell.latitude, probeCell.longitude, "anomaly");
  const error = probeValue(window.OCEANLINES_OISST_ERROR, probeCell.latitude, probeCell.longitude, "error");
  const argo = probeValue(window.OCEANLINES_ARGO_TEMPERATURE_ANOMALY, probeCell.latitude, probeCell.longitude, "argo700");
  document.querySelector("#probe-result").textContent = `Nearest active display cell · ${location}. SST: ${sst}. SST anomaly: ${anomaly}. Estimated analysis error: ${error}. 700 dbar Argo anomaly: ${argo}. Products are sampled on their own grids; none is heat content or transport.`;
  const [data, colorFunction] = activeObservedField();
  renderObservedField(data, colorFunction);
  if (updateUrl) updateAtlasUrl();
}

function setMapMode(mode) {
  if (mode === "observed") mode = "sst";
  const observed = mode !== "conceptual";
  const anomaly = mode === "anomaly";
  const subsurface = mode === "argo700";
  const error = mode === "error";
  currentMode = mode;
  const data = subsurface ? window.OCEANLINES_ARGO_TEMPERATURE_ANOMALY : anomaly ? window.OCEANLINES_OISST_ANOMALY : error ? window.OCEANLINES_OISST_ERROR : window.OCEANLINES_OISST;
  document.querySelectorAll(".map-mode").forEach(button => {
    const active = button.dataset.mode === mode;
    button.classList.toggle("active", active);
    button.setAttribute("aria-pressed", String(active));
  });
  document.querySelector("#conceptual-map").hidden = observed;
  document.querySelector("#sst-canvas").hidden = !observed;
  document.querySelector("#observed-stamp").hidden = !observed;
  document.querySelector("#temperature-key").hidden = !observed;
  document.querySelector("#temperature-key").classList.toggle("anomaly", anomaly || subsurface);
  document.querySelector("#temperature-key").classList.toggle("error", error);
  document.querySelector("#ring-comparison").hidden = subsurface;
  document.querySelector("#map-data-summary").hidden = !observed;
  document.querySelector("#conceptual-actions").hidden = observed;
  document.querySelector("#map-reference-labels").hidden = !observed;
  document.querySelector(".atlas-shell").classList.toggle("observed-mode", observed);
  markers.hidden = observed;
  document.querySelector("#map-stage").classList.toggle("observed", observed);
  document.querySelectorAll(".lens").forEach(button => { button.disabled = observed; });
  document.querySelector("#observed-title").textContent = subsurface ? "ARGO ANALYSIS · 700 DBAR ANOMALY" : anomaly ? "OBSERVATIONAL · SURFACE ANOMALY" : error ? "OBSERVATIONAL · ESTIMATED ERROR" : "OBSERVATIONAL · ABSOLUTE SURFACE";
  document.querySelector("#observed-status").textContent = subsurface ? "SCRIPPS RG · JULY 2026 · 2004–2018 REFERENCE" : anomaly ? "NOAA OISST v2.1 · 1971–2000 BASELINE" : error ? "NOAA OISST v2.1 · TIME-MATCHED ERROR" : "NOAA OISST v2.1 · FINAL · 2026-08-01";
  document.querySelector("#scale-min").textContent = anomaly || subsurface ? "−5°C cooler" : error ? "0.1°C lower" : "−2°C";
  document.querySelector("#scale-mid").textContent = anomaly || subsurface ? "0°C baseline" : error ? "0.35°C" : "15°C";
  document.querySelector("#scale-max").textContent = anomaly || subsurface ? "+5°C warmer" : error ? "0.6°C higher" : "32°C";
  document.querySelector("#temperature-key").setAttribute("aria-label", subsurface ? "700 dbar temperature anomaly scale from five degrees cooler to five degrees warmer than the RG baseline" : anomaly ? "SST anomaly scale from five degrees cooler to five degrees warmer than baseline" : error ? "Estimated analysis error scale from lower to higher error" : "Absolute sea surface temperature color scale");
  const canvas = document.querySelector("#sst-canvas");
  canvas.setAttribute("aria-label", subsurface ? "Scripps RG Argo potential-temperature anomaly at 700 dbar for July 2026, displayed on a two-degree equirectangular grid from 64.5 degrees south to 79.5 degrees north." : anomaly ? "NOAA OISST anomaly for 1 August 2026 relative to 1971 to 2000, displayed on a two-degree equirectangular grid." : error ? "NOAA OISST estimated analysis error for 1 August 2026, displayed on a two-degree equirectangular grid." : "NOAA OISST absolute sea surface temperature for 1 August 2026, displayed on a two-degree equirectangular grid.");
  document.querySelector("#map-note").innerHTML = observed
    ? `<span></span> ${subsurface ? "700 dbar anomaly · RG 2019 seasonal reference · July 2026 · symmetric ±5°C display clamp · 64.5°S–79.5°N · slate outside source domain" : anomaly ? "SST anomaly · 1971–2000 reference · symmetric ±5°C display clamp" : error ? "estimated analysis error · 0.1–0.6°C display clamp" : "absolute SST"} · equirectangular · antimeridian seam · 2° display stride`
    : "<span></span> Schematic, permeable, moving regions · not fixed boundaries · not a live analysis";
  if (observed) {
    renderObservedField(data, anomaly || subsurface ? anomalyColor : error ? errorColor : temperatureColor);
    showObservedMetadata(data, mode);
    renderTextSummary(data, mode);
    if (!subsurface) renderRingComparison(data, mode, anomaly ? anomalyColor : error ? errorColor : temperatureColor);
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

  const item = document.createElement("li");
  const directoryButton = document.createElement("button");
  directoryButton.type = "button";
  directoryButton.innerHTML = `<span>${String(zone.n).padStart(2, "0")}</span> ${zone.name}`;
  directoryButton.addEventListener("click", () => {
    document.querySelector('.lens[data-lens="all"]').click();
    selectZone(zone);
    document.querySelector("#zone-panel").scrollIntoView({ block: "start" });
  });
  item.append(directoryButton);
  document.querySelector("#zone-directory-list").append(item);
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
document.querySelector("#ring-form").addEventListener("submit", event => {
  event.preventDefault();
  setRingLatitude(Number(document.querySelector("#ring-lat").value));
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
if (requestedParameters.has("ring")) setRingLatitude(Number(requestedParameters.get("ring")), false);
if (["observed", "sst", "anomaly", "argo700", "error"].includes(requestedMode)) setMapMode(requestedMode);
if (currentMode !== "conceptual" && requestedParameters.has("lat") && requestedParameters.has("lon")) {
  inspectCoordinates(Number(requestedParameters.get("lat")), Number(requestedParameters.get("lon")));
}
