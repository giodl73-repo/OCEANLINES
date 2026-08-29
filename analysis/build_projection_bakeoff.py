"""Build ocean-first projection prototypes and local heatmass plates.

The output is explanatory cartography, not a gridded heat product. Natural
Earth supplies pinned coastline reference geometry. Fluid features are one
shared schematic longitude/latitude overlay projected identically in each
candidate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable, Iterator, Sequence

from pyproj import CRS, Transformer


SOURCE_COMMIT = "ca96624a56bd078437bca8184e78163e5039ad19"
SOURCE_URL = f"https://raw.githubusercontent.com/nvkelso/natural-earth-vector/{SOURCE_COMMIT}/geojson/ne_110m_land.geojson"
EXPECTED_SOURCE_SHA256 = "9e0729ee253ca7d7a5c4ae9395fb1902264c5377c52e224d13dd85010e2835d9"
WIDTH = 900
HEIGHT = 760
MAP_BOX = (42.0, 112.0, 816.0, 530.0)
Point = tuple[float, float]
Projector = Callable[[float, float], Point]


@dataclass(frozen=True)
class Candidate:
    slug: str
    title: str
    subtitle: str
    property_label: str
    tradeoff: str
    projector: Projector
    frame: str


HEAT_POLYGONS: list[list[Point]] = [
    [(96, -3), (103, 5), (114, 9), (126, 7), (136, 11), (149, 8), (159, 3), (172, 1), (180, -3), (180, -14), (167, -16), (154, -12), (142, -15), (129, -10), (116, -12), (105, -8), (96, -3)],
    [(-180, -3), (-169, -4), (-158, -8), (-145, -12), (-151, -18), (-163, -18), (-175, -14), (-180, -14), (-180, -3)],
    [(-115, 5), (-108, 12), (-98, 15), (-88, 13), (-82, 18), (-72, 20), (-63, 16), (-56, 10), (-61, 4), (-72, 2), (-82, 6), (-91, 3), (-103, 6), (-115, 5)],
]
HEAT_SHELVES: list[list[Point]] = [
    [(105, -2), (115, 4), (126, 3), (137, 7), (149, 4), (160, -1), (173, -3)],
    [(-177, -7), (-166, -8), (-155, -12), (-149, -14)],
    [(-108, 8), (-98, 11), (-89, 9), (-80, 14), (-70, 15), (-62, 10)],
]
EL_NINO_POLYGON: list[Point] = [(172, 5), (190, 6), (215, 4), (240, 2), (267, -1), (280, -4), (274, -10), (248, -8), (220, -6), (194, -4), (172, -1), (172, 5)]
ARCTIC_WATER_POLYGON: list[Point] = [(-24, 55), (-8, 63), (10, 71), (39, 77), (74, 82), (113, 79), (126, 72), (97, 69), (60, 72), (28, 68), (4, 59), (-24, 55)]


def transformer(proj4: str) -> Transformer:
    spherical_geographic = CRS.from_proj4("+proj=longlat +R=1 +no_defs")
    return Transformer.from_crs(spherical_geographic, CRS.from_proj4(proj4), always_xy=True)


def spilhaus_projector() -> Projector:
    """Published Spilhaus oblique rotation followed by Adams Square II.

    The constants match the Spilhaus implementation added to PROJ 9.8. The
    installed Adams operator performs the final conformal square mapping.
    """

    adams = transformer("+proj=adams_ws2 +R=1 +units=m +no_defs")
    phi0 = math.radians(-49.56371678)
    azimuth = math.radians(40.17823482)
    rotation = math.radians(45.0)
    sin_alpha = -math.cos(phi0) * math.cos(azimuth)
    cos_alpha = math.sqrt(1.0 - sin_alpha * sin_alpha)
    lambda0 = math.atan2(math.tan(azimuth), -math.sin(phi0))
    beta = math.pi + math.atan2(-math.sin(azimuth), -math.tan(phi0))
    cos_rotation = math.cos(rotation)
    sin_rotation = math.sin(rotation)

    def project(longitude: float, latitude: float) -> Point:
        lam = math.radians(longitude)
        phi = math.radians(latitude)
        cos_phi = math.cos(phi)
        sin_phi = math.sin(phi)
        cos_lam = math.cos(lam - lambda0)
        sin_lam = math.sin(lam - lambda0)
        adams_phi = math.asin(max(-1.0, min(1.0, sin_alpha * sin_phi - cos_alpha * cos_phi * cos_lam)))
        adams_lam = beta + math.atan2(
            cos_phi * sin_lam,
            sin_alpha * cos_phi * cos_lam + cos_alpha * sin_phi,
        )
        adams_lam = (adams_lam + math.pi) % (2.0 * math.pi) - math.pi
        x_adams, y_adams = adams.transform(math.degrees(adams_lam), math.degrees(adams_phi))
        return (
            -(x_adams * cos_rotation + y_adams * sin_rotation),
            -(x_adams * -sin_rotation + y_adams * cos_rotation),
        )

    return project


def pyproj_projector(proj4: str) -> Projector:
    operation = transformer(proj4)

    def project(longitude: float, latitude: float) -> Point:
        return operation.transform(longitude, latitude)

    return project


def candidates() -> list[Candidate]:
    return [
        Candidate(
            "spilhaus",
            "SPILHAUS",
            "The continuity benchmark",
            "CONFORMAL · OCEAN UNBROKEN",
            "Local shape wins; apparent heatmass area does not.",
            spilhaus_projector(),
            "square",
        ),
        Candidate(
            "oceanic-goode",
            "OCEANIC GOODE",
            "The area benchmark",
            "EQUAL-AREA · INTERRUPTED",
            "Area compares honestly; ocean pathways meet lobe cuts.",
            pyproj_projector("+proj=igh_o +lon_0=-160 +R=1 +units=m +no_defs"),
            "wide",
        ),
        Candidate(
            "equal-earth",
            "EQUAL EARTH",
            "The flat-world benchmark",
            "EQUAL-AREA · FLAT",
            "Heatmass areas read clearly; the Africa seam still splits polar water.",
            pyproj_projector("+proj=eqearth +lon_0=-165 +R=1 +units=m +no_defs"),
            "wide",
        ),
        Candidate(
            "pelagos",
            "PELAGOS",
            "The OSW experiment",
            "EQUAL-AREA · SAHARA EDGE",
            "Ocean continuity leads; shape distortion grows toward Africa.",
            pyproj_projector("+proj=laea +lat_0=-20 +lon_0=-165 +R=1 +units=m +no_defs"),
            "circle",
        ),
    ]


def geometry_rings(geometry: dict) -> Iterator[list[Point]]:
    if geometry["type"] == "Polygon":
        polygons = [geometry["coordinates"]]
    elif geometry["type"] == "MultiPolygon":
        polygons = geometry["coordinates"]
    else:
        return
    for polygon in polygons:
        for ring in polygon:
            yield [(float(longitude), float(latitude)) for longitude, latitude in ring]


def all_rings(geojson: dict) -> Iterator[list[Point]]:
    for feature in geojson["features"]:
        yield from geometry_rings(feature["geometry"])


def densify(points: Sequence[Point], step: float = 2.0, close: bool = False) -> list[Point]:
    if len(points) < 2:
        return list(points)
    source = list(points)
    if close and source[0] != source[-1]:
        source.append(source[0])
    output: list[Point] = []
    for index, (start_lon, start_lat) in enumerate(source[:-1]):
        end_lon, end_lat = source[index + 1]
        delta_lon = (end_lon - start_lon + 180.0) % 360.0 - 180.0
        delta_lat = end_lat - start_lat
        count = max(1, math.ceil(max(abs(delta_lon), abs(delta_lat)) / step))
        for sample in range(count):
            fraction = sample / count
            output.append((start_lon + delta_lon * fraction, start_lat + delta_lat * fraction))
    output.append(source[-1])
    return output


def raw_bounds(project: Projector) -> tuple[float, float, float, float]:
    coordinates: list[Point] = []
    for latitude in range(-89, 90, 2):
        for longitude in range(-180, 181, 2):
            try:
                x, y = project(longitude, latitude)
            except (ValueError, OverflowError):
                continue
            if math.isfinite(x) and math.isfinite(y):
                coordinates.append((x, y))
    xs = [point[0] for point in coordinates]
    ys = [point[1] for point in coordinates]
    return min(xs), min(ys), max(xs), max(ys)


def screen_transform(
    bounds: tuple[float, float, float, float],
    box: tuple[float, float, float, float] = MAP_BOX,
) -> Callable[[Point], Point]:
    minimum_x, minimum_y, maximum_x, maximum_y = bounds
    box_x, box_y, box_width, box_height = box
    span_x = maximum_x - minimum_x
    span_y = maximum_y - minimum_y
    scale = min(box_width / span_x, box_height / span_y) * 0.95
    offset_x = box_x + (box_width - span_x * scale) / 2.0 - minimum_x * scale
    offset_y = box_y + (box_height - span_y * scale) / 2.0 + maximum_y * scale

    def transform(point: Point) -> Point:
        return offset_x + point[0] * scale, offset_y - point[1] * scale

    return transform


def local_bounds(project: Projector, extent: tuple[float, float, float, float]) -> tuple[float, float, float, float]:
    west, south, east, north = extent
    coordinates: list[Point] = []
    for row in range(31):
        latitude = south + (north - south) * row / 30
        for column in range(61):
            longitude = west + (east - west) * column / 60
            point = project(longitude, latitude)
            if math.isfinite(point[0]) and math.isfinite(point[1]):
                coordinates.append(point)
    xs = [point[0] for point in coordinates]
    ys = [point[1] for point in coordinates]
    return min(xs), min(ys), max(xs), max(ys)


def projected_segments(
    points: Sequence[Point],
    project: Projector,
    bounds: tuple[float, float, float, float],
    close: bool = False,
) -> list[list[Point]]:
    dense = densify(points, close=close)
    span = max(bounds[2] - bounds[0], bounds[3] - bounds[1])
    jump_limit = span * 0.16
    segments: list[list[Point]] = []
    segment: list[Point] = []
    previous: Point | None = None
    for longitude, latitude in dense:
        try:
            point = project(longitude, max(-89.999, min(89.999, latitude)))
        except (ValueError, OverflowError):
            point = (math.nan, math.nan)
        valid = math.isfinite(point[0]) and math.isfinite(point[1])
        jumped = previous is not None and valid and math.dist(previous, point) > jump_limit
        if not valid or jumped:
            if len(segment) >= 2:
                segments.append(segment)
            segment = []
        if valid:
            segment.append(point)
            previous = point
        else:
            previous = None
    if len(segment) >= 2:
        segments.append(segment)
    return segments


def svg_path(segments: Iterable[Sequence[Point]], screen: Callable[[Point], Point], close: bool = False) -> str:
    commands: list[str] = []
    for segment in segments:
        if len(segment) < 2:
            continue
        first_x, first_y = screen(segment[0])
        commands.append(f"M{first_x:.1f},{first_y:.1f}")
        for point in segment[1:]:
            x, y = screen(point)
            commands.append(f"L{x:.1f},{y:.1f}")
        if close and math.dist(segment[0], segment[-1]) < 1e-6:
            commands.append("Z")
    return "".join(commands)


def line_path(points: Sequence[Point], project: Projector, bounds: tuple[float, float, float, float], screen: Callable[[Point], Point]) -> str:
    return svg_path(projected_segments(points, project, bounds), screen)


def geographic_circle(longitude: float, latitude: float, radius_degrees: float) -> list[Point]:
    points: list[Point] = []
    longitude_scale = max(0.25, math.cos(math.radians(latitude)))
    for angle in range(0, 361, 6):
        radians = math.radians(angle)
        points.append((longitude + radius_degrees * math.cos(radians) / longitude_scale, latitude + radius_degrees * math.sin(radians)))
    return points


def geographic_blob(longitude: float, latitude: float, radius_degrees: float) -> list[Point]:
    points: list[Point] = []
    longitude_scale = max(0.25, math.cos(math.radians(latitude)))
    for angle in range(0, 361, 6):
        radians = math.radians(angle)
        local_radius = radius_degrees * (1.0 + 0.14 * math.sin(radians * 3.0) + 0.08 * math.cos(radians * 5.0))
        points.append((longitude + local_radius * math.cos(radians) / longitude_scale, latitude + local_radius * math.sin(radians)))
    return points


def render_candidate(candidate: Candidate, geojson: dict, source_sha256: str) -> str:
    bounds = raw_bounds(candidate.projector)
    screen = screen_transform(bounds)
    coastline_commands: list[str] = []
    for ring in all_rings(geojson):
        segments = projected_segments(ring, candidate.projector, bounds, close=True)
        coastline_commands.append(svg_path(segments, screen))
    coastlines = "".join(coastline_commands)

    graticule_commands: list[str] = []
    for latitude in range(-60, 61, 30):
        graticule_commands.append(line_path([(longitude, latitude) for longitude in range(-180, 181, 2)], candidate.projector, bounds, screen))
    for longitude in range(-150, 181, 30):
        graticule_commands.append(line_path([(longitude, latitude) for latitude in range(-88, 89, 2)], candidate.projector, bounds, screen))
    graticule = "".join(graticule_commands)

    heatmass_paths = "".join(
        f'<path class="heatmass" d="{svg_path(projected_segments(polygon, candidate.projector, bounds, close=True), screen, close=True)}"/>'
        for polygon in HEAT_POLYGONS
    )
    shelf_paths = "".join(
        f'<path class="shelf" d="{line_path(shelf, candidate.projector, bounds, screen)}"/>'
        for shelf in HEAT_SHELVES
    )

    fluid_lines = {
        "elnino": [(175, 0), (200, 0), (230, -1), (260, -2)],
        "gulf": [(-80, 25), (-73, 35), (-58, 43), (-38, 49)],
        "kuroshio": [(128, 22), (138, 34), (154, 40), (178, 43)],
        "agulhas": [(31, -29), (26, -38), (18, -43), (8, -42)],
        "arctic": [(-20, 58), (-5, 68), (22, 76), (62, 80), (105, 78)],
        "acc": [(longitude, -55 + 2.5 * math.sin(math.radians(longitude * 2))) for longitude in range(-180, 181, 2)],
    }
    paths = {name: line_path(points, candidate.projector, bounds, screen) for name, points in fluid_lines.items()}
    blob_segments = projected_segments(geographic_blob(-145, 45, 12), candidate.projector, bounds, close=True)
    blob = svg_path(blob_segments, screen, close=True)

    gate_symbols: list[str] = []
    for longitude, latitude in [(-68, -56), (123, -3)]:
        gate_x, gate_y = screen(candidate.projector(longitude, latitude))
        gate_symbols.append(f'<path class="gate" d="M{gate_x:.1f},{gate_y - 9:.1f}l9,9l-9,9l-9,-9Z"/>')
    gates = "".join(gate_symbols)

    singularity_note = "ANTIPODAL EDGE: SAHARA" if candidate.slug == "pelagos" else ""
    if candidate.frame == "circle":
        frame_shape = '<circle cx="450" cy="377" r="269"/>'
    elif candidate.frame == "square":
        frame_shape = '<rect x="185" y="112" width="530" height="530" rx="24"/>'
    else:
        frame_shape = '<rect x="42" y="112" width="816" height="530" rx="24"/>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">
  <title id="title">{candidate.title} ocean projection prototype</title>
  <desc id="desc">The {candidate.title} candidate projects the same schematic OSW heat reservoirs, transient anomaly, currents, and Antarctic Circumpolar Current over checksum-pinned Natural Earth coastlines. {candidate.tradeoff}</desc>
  <metadata>Natural Earth 1:110m land, public domain, commit {SOURCE_COMMIT}, SHA-256 {source_sha256}, {SOURCE_URL}. Projection rendering and conceptual overlays are original MIT-licensed OSW work. PELAGOS is an experimental aspect of Lambert azimuthal equal-area, not a new projection equation.</metadata>
  <defs>
    <linearGradient id="ocean" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#123f4c"/><stop offset="1" stop-color="#061922"/></linearGradient>
    <linearGradient id="heat" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#ffd46b"/><stop offset="1" stop-color="#ff8f4d"/></linearGradient>
    <radialGradient id="blob"><stop stop-color="#ff756d" stop-opacity=".72"/><stop offset="1" stop-color="#ff756d" stop-opacity=".08"/></radialGradient>
    <filter id="glow" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <clipPath id="map-clip">{frame_shape}</clipPath>
    <style>
      text {{ font-family: Inter, ui-sans-serif, system-ui, sans-serif; }}
      .grid {{ fill:none; stroke:#aad4d6; stroke-opacity:.12; stroke-width:1; }}
      .coast {{ fill:none; stroke:#a7c2c1; stroke-opacity:.32; stroke-width:1.15; vector-effect:non-scaling-stroke; }}
      .heatmass {{ fill:url(#heat); fill-opacity:.72; stroke:#ffd06b; stroke-width:3; stroke-linejoin:round; }}
      .shelf {{ fill:none; stroke:#ffe6a5; stroke-width:2; stroke-dasharray:12 8; stroke-linecap:round; stroke-opacity:.8; }}
      .anomaly {{ fill:url(#blob); stroke:#ff8d84; stroke-width:2.5; stroke-dasharray:9 7; }}
      .tongue {{ fill:none; stroke:#ff8178; stroke-width:26; stroke-linecap:round; stroke-dasharray:10 7; stroke-opacity:.7; }}
      .current {{ fill:none; stroke:#ffb454; stroke-width:8; stroke-linecap:round; filter:url(#glow); }}
      .acc {{ fill:none; stroke:#8eeaf2; stroke-width:9; stroke-dasharray:18 10; filter:url(#glow); }}
      .buried {{ fill:none; stroke:#b7a7ff; stroke-width:13; stroke-dasharray:10 7; stroke-linecap:round; stroke-opacity:.62; }}
      .gate {{ fill:#071b22; stroke:#67e4da; stroke-width:3; }}
    </style>
  </defs>
  <rect width="900" height="760" fill="#06171c"/>
  <text x="42" y="44" fill="#67e4da" font-size="15" font-weight="900" letter-spacing="3">OSW / PROJECTION LAB</text>
  <text x="42" y="79" fill="#eef9f7" font-size="30" font-weight="900">{candidate.title}</text>
  <text x="858" y="56" text-anchor="end" fill="#ffb454" font-size="12" font-weight="900" letter-spacing="1.8">{candidate.property_label}</text>
  <text x="858" y="79" text-anchor="end" fill="#8da9a9" font-size="13">{candidate.subtitle}</text>
  <g clip-path="url(#map-clip)">
    <rect x="42" y="108" width="816" height="538" fill="url(#ocean)"/>
    <path class="grid" d="{graticule}"/>
    {heatmass_paths}{shelf_paths}
    <path class="anomaly" d="{blob}"/>
    <path class="tongue" d="{paths['elnino']}"/>
    <path class="coast" d="{coastlines}"/>
    <path class="current" d="{paths['gulf']}"/><path class="current" d="{paths['kuroshio']}"/><path class="current" d="{paths['agulhas']}"/>
    <path class="buried" d="{paths['arctic']}"/>
    <path class="acc" d="{paths['acc']}"/>
    {gates}
  </g>
  <g fill="none" stroke="#49666b" stroke-width="1.5">{frame_shape}</g>
  <text x="42" y="680" fill="#eef9f7" font-size="16" font-weight="800">{candidate.tradeoff}</text>
  <text x="42" y="710" fill="#8da9a9" font-size="12">Same schematic features · same coastline source · projection changes only</text>
  <text x="858" y="710" text-anchor="end" fill="#ffb454" font-size="11" font-weight="800" letter-spacing="1.4">{singularity_note}</text>
  <g transform="translate(42 730)" font-size="9" font-weight="800"><path d="M0-3h25" stroke="#ffb454" stroke-width="12" stroke-linecap="round"/><text x="34" fill="#8da9a9">HEATMASS</text><circle cx="125" cy="-3" r="5" fill="#ff8d84"/><text x="137" fill="#8da9a9">ANOMALY</text><path d="M218-3h25" stroke="#ffb454" stroke-width="5"/><text x="251" fill="#8da9a9">CURRENT</text><path d="M324-3h27" stroke="#8eeaf2" stroke-width="5" stroke-dasharray="8 5"/><text x="359" fill="#8da9a9">ACC</text><path d="M405-3h25" stroke="#b7a7ff" stroke-width="7" stroke-dasharray="6 4"/><text x="438" fill="#8da9a9">BURIED INFLOW</text><path d="M560-10l7 7-7 7-7-7Z" fill="none" stroke="#67e4da" stroke-width="2"/><text x="575" fill="#8da9a9">GATE</text></g>
</svg>'''


def render_heatplates(geojson: dict, source_sha256: str) -> str:
    plate_width = 366
    plate_height = 346
    plate_gap = 18
    start_x = 30
    start_y = 132
    definitions = [
        {
            "number": "01", "title": "INDO-PACIFIC WARM POOL", "kind": "RESERVOIR",
            "center": (145, -5), "extent": (78, -30, 218, 28),
            "polygons": HEAT_POLYGONS[:2], "shelves": HEAT_SHELVES[:2], "class": "reservoir",
        },
        {
            "number": "02", "title": "WESTERN WARM POOL", "kind": "SEASONAL RESERVOIR",
            "center": (-85, 12), "extent": (-130, -8, -38, 35),
            "polygons": [HEAT_POLYGONS[2]], "shelves": [HEAT_SHELVES[2]], "class": "reservoir",
        },
        {
            "number": "03", "title": "NORTHEAST PACIFIC BLOB", "kind": "TRANSIENT ANOMALY",
            "center": (-145, 45), "extent": (-180, 20, -105, 70),
            "polygons": [geographic_blob(-145, 45, 12)], "shelves": [], "class": "anomaly",
        },
        {
            "number": "04", "title": "EL NIÑO TONGUE", "kind": "EQUATORIAL ANOMALY",
            "center": (-130, 0), "extent": (165, -22, 285, 22),
            "polygons": [EL_NINO_POLYGON], "shelves": [[(180, 1), (205, 1), (232, -1), (260, -4)]], "class": "tongue",
        },
        {
            "number": "05", "title": "ATLANTIC WATER / ARCTIC", "kind": "BURIED HEATMASS",
            "center": (48, 72), "extent": (-35, 48, 145, 89),
            "polygons": [ARCTIC_WATER_POLYGON], "shelves": [[(-12, 61), (14, 69), (45, 75), (80, 78), (112, 75)]], "class": "buried",
        },
        {
            "number": "06", "title": "CIRCUMPOLAR DEEP WATER", "kind": "ANNULAR HEATMASS",
            "center": (0, -90), "extent": (-180, -90, 180, -34),
            "polygons": [], "shelves": [], "class": "belt",
        },
    ]

    panels: list[str] = []
    for index, definition in enumerate(definitions):
        column = index % 3
        row = index // 3
        x = start_x + column * (plate_width + plate_gap)
        y = start_y + row * (plate_height + plate_gap)
        map_box = (x + 16, y + 70, plate_width - 32, plate_height - 88)
        center_lon, center_lat = definition["center"]
        project = pyproj_projector(f"+proj=laea +lat_0={center_lat} +lon_0={center_lon} +R=1 +units=m +no_defs")
        bounds = local_bounds(project, definition["extent"])
        screen = screen_transform(bounds, map_box)

        coastline_commands: list[str] = []
        for ring in all_rings(geojson):
            coastline_commands.append(svg_path(projected_segments(ring, project, bounds, close=True), screen))
        coastlines = "".join(coastline_commands)

        region_paths = "".join(
            f'<path class="plate-region {definition["class"]}" d="{svg_path(projected_segments(polygon, project, bounds, close=True), screen, close=True)}"/>'
            for polygon in definition["polygons"]
        )
        shelf_paths = "".join(
            f'<path class="plate-shelf" d="{line_path(shelf, project, bounds, screen)}"/>'
            for shelf in definition["shelves"]
        )
        if definition["class"] == "belt":
            outer = [(longitude, -46) for longitude in range(-180, 181, 3)]
            inner = [(longitude, -66) for longitude in range(180, -181, -3)]
            outer_segments = projected_segments(outer, project, bounds, close=True)
            inner_segments = projected_segments(inner, project, bounds, close=True)
            annulus = svg_path(outer_segments, screen, close=True) + svg_path(inner_segments, screen, close=True)
            region_paths = f'<path class="plate-region belt" fill-rule="evenodd" d="{annulus}"/>'
            shelf_paths = f'<path class="plate-shelf" d="{line_path([(longitude, -56) for longitude in range(-180, 181, 3)], project, bounds, screen)}"/>'

        clip_id = f"plate-clip-{index + 1}"
        panels.append(f'''
    <g class="plate">
      <rect x="{x}" y="{y}" width="{plate_width}" height="{plate_height}" rx="18" fill="#092129" stroke="#29484f"/>
      <text x="{x + 18}" y="{y + 28}" fill="#ffb454" font-size="11" font-weight="900">{definition["number"]}</text>
      <text x="{x + 48}" y="{y + 28}" fill="#eef9f7" font-size="14" font-weight="900">{definition["title"]}</text>
      <text x="{x + 48}" y="{y + 48}" fill="#8da9a9" font-size="10" font-weight="800" letter-spacing="1">{definition["kind"]}</text>
      <defs><clipPath id="{clip_id}"><rect x="{map_box[0]}" y="{map_box[1]}" width="{map_box[2]}" height="{map_box[3]}" rx="12"/></clipPath></defs>
      <g clip-path="url(#{clip_id})">
        <rect x="{map_box[0]}" y="{map_box[1]}" width="{map_box[2]}" height="{map_box[3]}" fill="url(#plate-ocean)"/>
        {region_paths}{shelf_paths}<path class="plate-coast" d="{coastlines}"/>
      </g>
      <rect x="{map_box[0]}" y="{map_box[1]}" width="{map_box[2]}" height="{map_box[3]}" rx="12" fill="none" stroke="#365961"/>
      <text x="{x + 18}" y="{y + plate_height - 9}" fill="#789497" font-size="9">LOCAL LAMBERT EQUAL-AREA · PANEL-SPECIFIC ZOOM</text>
    </g>''')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="900" viewBox="0 0 1200 900" role="img" aria-labelledby="title desc">
  <title id="title">OSW HEATPLATES</title>
  <desc id="desc">Six flat local equal-area panels show the individual schematic shapes of the Indo-Pacific warm pool, Western Hemisphere warm pool, Northeast Pacific Blob, El Niño tongue, buried Atlantic Water in the Arctic, and Circumpolar Deep Water. Every panel uses its own zoom, so footprint areas must not be compared.</desc>
  <metadata>Natural Earth 1:110m land, public domain, commit {SOURCE_COMMIT}, SHA-256 {source_sha256}, {SOURCE_URL}. Local Lambert equal-area views and schematic heat polygons are original MIT-licensed OSW work.</metadata>
  <defs>
    <linearGradient id="plate-ocean" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#123f4c"/><stop offset="1" stop-color="#061922"/></linearGradient>
    <linearGradient id="plate-heat" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#ffd46b"/><stop offset="1" stop-color="#ff8f4d"/></linearGradient>
    <style>
      text {{ font-family:Inter,ui-sans-serif,system-ui,sans-serif; }}
      .plate-coast {{ fill:none; stroke:#a7c2c1; stroke-opacity:.42; stroke-width:1.1; vector-effect:non-scaling-stroke; }}
      .plate-region {{ stroke-width:3; stroke-linejoin:round; }}
      .plate-region.reservoir {{ fill:url(#plate-heat); fill-opacity:.78; stroke:#ffd06b; }}
      .plate-region.anomaly,.plate-region.tongue {{ fill:#ff766c; fill-opacity:.48; stroke:#ff8d84; stroke-dasharray:9 7; }}
      .plate-region.buried {{ fill:#9c8bf2; fill-opacity:.4; stroke:#c5baff; stroke-dasharray:10 7; }}
      .plate-region.belt {{ fill:#8eeaf2; fill-opacity:.25; stroke:#8eeaf2; stroke-dasharray:14 9; }}
      .plate-shelf {{ fill:none; stroke:#fff0b8; stroke-opacity:.78; stroke-width:2; stroke-dasharray:12 8; stroke-linecap:round; }}
    </style>
  </defs>
  <rect width="1200" height="900" fill="#06171c"/>
  <text x="30" y="40" fill="#67e4da" font-size="15" font-weight="900" letter-spacing="3">OSW / SHAPE ATLAS</text>
  <text x="30" y="82" fill="#eef9f7" font-size="38" font-weight="950">HEATPLATES</text>
  <text x="1170" y="48" text-anchor="end" fill="#ffb454" font-size="12" font-weight="900" letter-spacing="1.8">SHAPE FIRST · NOT ONE WORLD MAP</text>
  <text x="1170" y="76" text-anchor="end" fill="#8da9a9" font-size="12">Schematic boundaries · local equal-area · zoom varies by panel</text>
  <rect x="30" y="96" width="1140" height="24" rx="12" fill="#112e34"/>
  <text x="600" y="112" text-anchor="middle" fill="#ffcf70" font-size="10" font-weight="900" letter-spacing="1.3">DO NOT COMPARE FOOTPRINT AREA ACROSS PANELS · EACH VIEW USES ITS OWN ZOOM</text>
  {''.join(panels)}
  <text x="30" y="882" fill="#789497" font-size="10">CONCEPTUAL SHAPE DIRECTORY · NOT OBSERVED THRESHOLDS · NOT HEAT CONTENT · NOT TRANSPORT</text>
</svg>'''


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--land-geojson", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    payload = args.land_geojson.read_bytes()
    digest = hashlib.sha256(payload).hexdigest()
    if digest != EXPECTED_SOURCE_SHA256:
        raise SystemExit(f"Natural Earth source checksum mismatch: {digest}")
    geojson = json.loads(payload)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for candidate in candidates():
        output = args.output_dir / f"osw-projection-{candidate.slug}.svg"
        output.write_text(render_candidate(candidate, geojson, digest), encoding="utf-8", newline="\n")
    heatplates_output = args.output_dir / "osw-heatplates.svg"
    heatplates_output.write_text(render_heatplates(geojson, digest), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
