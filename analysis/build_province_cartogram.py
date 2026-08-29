"""Build the OCEANLINES 56-province reference cartogram.

This is an original adjacency-inspired atlas layout, not a geographic projection
or a redistribution of the Marine Regions Longhurst geometry.  Province codes,
names, basin membership, and biome membership are factual reference data drawn
from the cited Longhurst literature.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import pathlib


PROVINCES = {
    "Pacific": [
        ("BERS", "North Pacific epicontinental sea", "Polar"),
        ("PSAW", "Western Pacific subarctic gyres", "Westerlies"),
        ("NPPF", "North Pacific polar front", "Westerlies"),
        ("PSAE", "Eastern Pacific subarctic gyres", "Westerlies"),
        ("ALSK", "Alaska coastal downwelling", "Coastal"),
        ("KURO", "Kuroshio Current", "Westerlies"),
        ("NPSW", "Northwest Pacific subtropical", "Westerlies"),
        ("NPSE", "Northeast Pacific subtropical", "Westerlies"),
        ("CCAL", "Coastal California Current", "Coastal"),
        ("CHIN", "China Sea", "Coastal"),
        ("NPTG", "North Pacific tropical gyre", "Trades"),
        ("PNEC", "North Pacific equatorial countercurrent", "Trades"),
        ("CAMR", "Central American coast", "Coastal"),
        ("SUND", "Sunda–Arafura shelves", "Coastal"),
        ("WARM", "Western Pacific warm pool", "Trades"),
        ("PEQD", "Pacific equatorial divergence", "Trades"),
        ("HUMB", "Humboldt Current coast", "Coastal"),
        ("AUSE", "East Australian coast", "Coastal"),
        ("ARCH", "Archipelagic deep basins", "Trades"),
        ("SPSG", "South Pacific gyre", "Trades"),
        ("NEWZ", "New Zealand coast", "Coastal"),
        ("TASM", "Tasman Sea", "Westerlies"),
        ("OCAL", "Oceanic California Current", "Trades"),
    ],
    "Indian": [
        ("REDS", "Red Sea and Persian Gulf", "Coastal"),
        ("IND W", "Western India coast", "Coastal"),
        ("ARAB", "Northwest Arabian Sea upwelling", "Westerlies"),
        ("MONS", "Indian monsoon gyre", "Trades"),
        ("IND E", "Eastern India coast", "Coastal"),
        ("ISSG", "Indian South subtropical gyre", "Trades"),
        ("EAFR", "East African coast", "Coastal"),
        ("AUSW", "Western Australian and Indonesian coast", "Coastal"),
    ],
    "Atlantic": [
        ("ARCT", "Atlantic Arctic", "Polar"),
        ("SARC", "Atlantic sub-Arctic", "Polar"),
        ("NECS", "Northeast Atlantic shelves", "Coastal"),
        ("NWCS", "Northwest Atlantic shelves", "Coastal"),
        ("NADR", "North Atlantic Drift", "Westerlies"),
        ("GFST", "Gulf Stream", "Westerlies"),
        ("NAST E", "Northeast Atlantic subtropical gyre", "Westerlies"),
        ("NAST W", "Northwest Atlantic subtropical gyre", "Westerlies"),
        ("MEDI", "Mediterranean Sea", "Westerlies"),
        ("CNRY", "Canary Current coast", "Coastal"),
        ("NATR", "North Atlantic tropical gyre", "Trades"),
        ("CARB", "Caribbean", "Trades"),
        ("GUIA", "Guianas coast", "Coastal"),
        ("WTRA", "Western tropical Atlantic", "Trades"),
        ("ETRA", "Eastern tropical Atlantic", "Trades"),
        ("GUIN", "Guinea Current coast", "Coastal"),
        ("SATL", "South Atlantic gyre", "Trades"),
        ("BRAZ", "Brazil Current coast", "Coastal"),
        ("BENG", "Benguela Current coast", "Coastal"),
        ("FKLD", "Southwest Atlantic shelves", "Coastal"),
    ],
    "Southern": [
        ("SSTC", "South subtropical convergence", "Westerlies"),
        ("SANT", "Subantarctic water ring", "Westerlies"),
        ("ANTA", "Antarctic", "Polar"),
        ("APLR", "Austral polar", "Polar"),
    ],
    "Arctic": [("BPLR", "Boreal polar", "Polar")],
}

COLORS = {
    "Polar": ("#8bd8e8", "#06242d"),
    "Westerlies": ("#5eb8cf", "#041a21"),
    "Trades": ("#f1b65b", "#211407"),
    "Coastal": ("#72d3b0", "#052219"),
}

SOURCE_COMMIT = "ca96624a56bd078437bca8184e78163e5039ad19"
SOURCE_URL = f"https://raw.githubusercontent.com/nvkelso/natural-earth-vector/{SOURCE_COMMIT}/geojson/ne_110m_land.geojson"
EXPECTED_SOURCE_SHA256 = "9e0729ee253ca7d7a5c4ae9395fb1902264c5377c52e224d13dd85010e2835d9"

# Approximate open-ocean label/seed positions for an original nearest-neighbour
# cartogram. These are deliberately not published Longhurst boundary geometry:
# they place the vocabulary geographically so the real coast is inherited by
# the appropriate coastal province (ALSK at Alaska, HUMB at Peru/Chile, etc.).
PROVINCE_SEEDS = {
    "BPLR": (0, 79), "BERS": (-170, 58), "PSAW": (160, 48), "NPPF": (-175, 42),
    "PSAE": (-145, 49), "ALSK": (-148, 58), "KURO": (145, 35), "NPSW": (165, 28),
    "NPSE": (-135, 30), "CCAL": (-124, 36), "CHIN": (122, 24), "NPTG": (-165, 20),
    "PNEC": (-140, 9), "CAMR": (-92, 10), "SUND": (126, -5), "WARM": (150, 8),
    "PEQD": (-115, 0), "HUMB": (-82, -22), "AUSE": (156, -25), "ARCH": (140, -12),
    "SPSG": (-135, -28), "NEWZ": (174, -42), "TASM": (160, -38), "OCAL": (-132, 40),
    "REDS": (43, 18), "IND W": (70, 12), "ARAB": (59, 17), "MONS": (84, 5),
    "IND E": (88, 14), "ISSG": (82, -27), "EAFR": (48, -12), "AUSW": (108, -25),
    "ARCT": (-10, 72), "SARC": (-28, 60), "NECS": (2, 55), "NWCS": (-58, 48),
    "NADR": (-30, 47), "GFST": (-68, 37), "NAST E": (-25, 30), "NAST W": (-55, 28),
    "MEDI": (17, 36), "CNRY": (-18, 24), "NATR": (-42, 16), "CARB": (-73, 16),
    "GUIA": (-50, 7), "WTRA": (-35, 3), "ETRA": (-5, 1), "GUIN": (3, 5),
    "SATL": (-22, -25), "BRAZ": (-43, -25), "BENG": (8, -24), "FKLD": (-58, -47),
    "SSTC": (20, -45), "SANT": (95, -53), "ANTA": (-110, -66), "APLR": (155, -64),
}


def tile_path(x0: float, y0: float, x1: float, y1: float, seed: int) -> str:
    """Return a deterministic irregular tile with corners shared by its box."""
    notch = 7 + seed % 9
    skew = (seed % 5 - 2) * 3
    return (
        f"M{x0:g},{y0:g} L{x1 - notch:g},{y0:g} "
        f"L{x1:g},{y0 + notch:g} L{x1 + skew:g},{y1 - notch:g} "
        f"L{x1 - notch:g},{y1:g} L{x0 + notch:g},{y1:g} "
        f"L{x0:g},{y1 - notch:g} L{x0 - skew:g},{y0 + notch:g} Z"
    )


def render_cluster(name: str, x: int, y: int, width: int, height: int, columns: int, monochrome: bool = False) -> str:
    provinces = PROVINCES[name]
    rows = (len(provinces) + columns - 1) // columns
    cell_w = width / columns
    cell_h = height / rows
    parts = [f'<g class="basin" id="{name.lower()}-provinces">']
    for index, (code, province, biome) in enumerate(provinces):
        row, column = divmod(index, columns)
        x0, y0 = x + column * cell_w, y + row * cell_h
        x1, y1 = x + (column + 1) * cell_w, y + (row + 1) * cell_h
        # Last incomplete row expands to the right edge instead of leaving ocean blank.
        if row == rows - 1 and index == len(provinces) - 1:
            x1 = x + width
        fill, ink = ("#d4dfdc", "#11282e") if monochrome else COLORS[biome]
        safe_name = html.escape(province)
        safe_code = html.escape(code)
        parts.append(
            f'<g class="province {biome.lower()}" tabindex="0">'
            f'<title>{safe_code} — {safe_name} · {name} · {biome} biome</title>'
            f'<path d="{tile_path(x0, y0, x1, y1, index + len(name))}" fill="{fill}"/>'
            f'<text x="{(x0+x1)/2:g}" y="{(y0+y1)/2 + 5:g}" fill="{ink}">{safe_code}</text>'
            f'</g>'
        )
    parts.append(
        f'<text class="basin-label" x="{x + width/2:g}" y="{y + height + 25:g}">{name.upper()}</text>'
    )
    parts.append("</g>")
    return "".join(parts)


def render_strip(name: str, y: int, height: int, monochrome: bool = False) -> str:
    provinces = PROVINCES[name]
    x, width = 92, 1416
    cell_w = width / len(provinces)
    parts = [f'<g class="basin" id="{name.lower()}-provinces">']
    for index, (code, province, biome) in enumerate(provinces):
        x0, x1 = x + index * cell_w, x + (index + 1) * cell_w
        fill, ink = ("#d4dfdc", "#11282e") if monochrome else COLORS[biome]
        parts.append(
            f'<g class="province {biome.lower()}" tabindex="0">'
            f'<title>{html.escape(code)} — {html.escape(province)} · {name} · {biome} biome</title>'
            f'<path d="{tile_path(x0, y, x1, y + height, 71 + index)}" fill="{fill}"/>'
            f'<text x="{(x0+x1)/2:g}" y="{y + height/2 + 5:g}" fill="{ink}">{html.escape(code)}</text>'
            f'</g>'
        )
    parts.append("</g>")
    return "".join(parts)


def geometry_rings(geometry: dict) -> list[list[tuple[float, float]]]:
    if geometry["type"] == "Polygon":
        polygons = [geometry["coordinates"]]
    elif geometry["type"] == "MultiPolygon":
        polygons = geometry["coordinates"]
    else:
        return []
    return [
        [(float(longitude), float(latitude)) for longitude, latitude in ring]
        for polygon in polygons
        for ring in polygon
    ]


def coastline_fingerprint(
    geojson: dict,
    longitude_minimum: float,
    longitude_maximum: float,
    screen_minimum: float,
    screen_maximum: float,
) -> str:
    """Compress real coastline segments into one narrow continental seam."""

    def project(longitude: float, latitude: float) -> tuple[float, float]:
        x = screen_minimum + (longitude - longitude_minimum) / (longitude_maximum - longitude_minimum) * (screen_maximum - screen_minimum)
        y = 242 + (84 - latitude) / 144 * 466
        return x, y

    commands: list[str] = []
    for feature in geojson["features"]:
        for ring in geometry_rings(feature["geometry"]):
            segment: list[tuple[float, float]] = []
            for longitude, latitude in ring:
                inside = longitude_minimum <= longitude <= longitude_maximum and -60 <= latitude <= 84
                if inside:
                    segment.append(project(longitude, latitude))
                elif len(segment) >= 2:
                    commands.append("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in segment))
                    segment = []
                else:
                    segment = []
            if len(segment) >= 2:
                commands.append("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in segment))
    return " ".join(commands)


def render_continental_context(geojson: dict) -> str:
    americas_left = coastline_fingerprint(geojson, -170, -30, 61, 91)
    americas_right = coastline_fingerprint(geojson, -170, -30, 1511, 1541)
    asia_australia = coastline_fingerprint(geojson, 20, 180, 748, 786)
    africa_europe = coastline_fingerprint(geojson, -25, 60, 1036, 1074)
    return f'''
  <g aria-label="Checksum-pinned continental coastline context">
    <path class="land-bed" d="M60 242H92V708H60Z M747 242H787V708H747Z M1035 242H1075V708H1035Z M1510 242H1542V708H1510Z"/>
    <path class="coastline" d="{americas_left}"/>
    <path class="coastline" d="{asia_australia}"/>
    <path class="coastline" d="{africa_europe}"/>
    <path class="coastline" d="{americas_right}"/>
    <text class="land-label" x="74" y="490" transform="rotate(-90 74 490)">AMERICAS</text>
    <text class="land-label" x="769" y="475" transform="rotate(-90 769 475)">ASIA · AUSTRALIA</text>
    <text class="land-label" x="1057" y="475" transform="rotate(-90 1057 475)">AFRICA · EUROPE</text>
    <text class="land-label" x="1530" y="480" transform="rotate(90 1530 480)">AMERICAS</text>
  </g>'''


def continent_hole_path(geojson: dict) -> str:
    """Return compressed filled continental silhouettes for the lakes study."""

    groups = {
        "americas": (-180.0, -20.0, 42.0, 140.0),
        "africa": (-25.0, 55.0, 990.0, 1112.0),
        "eurasia": (-20.0, 180.0, 700.0, 832.0),
    }
    paths: dict[str, list[str]] = {name: [] for name in groups}

    def clip_polygon(
        ring: list[tuple[float, float]],
        x_min: float,
        x_max: float,
        y_min: float,
        y_max: float,
    ) -> list[tuple[float, float]]:
        points = ring[:-1] if ring and ring[0] == ring[-1] else list(ring)

        def clip_edge(points, inside, intersect):
            if not points:
                return []
            output = []
            previous = points[-1]
            previous_inside = inside(previous)
            for current in points:
                current_inside = inside(current)
                if current_inside:
                    if not previous_inside:
                        output.append(intersect(previous, current))
                    output.append(current)
                elif previous_inside:
                    output.append(intersect(previous, current))
                previous, previous_inside = current, current_inside
            return output

        def vertical(boundary):
            def intersection(a, b):
                fraction = (boundary - a[0]) / (b[0] - a[0]) if b[0] != a[0] else 0
                return boundary, a[1] + fraction * (b[1] - a[1])
            return intersection

        def horizontal(boundary):
            def intersection(a, b):
                fraction = (boundary - a[1]) / (b[1] - a[1]) if b[1] != a[1] else 0
                return a[0] + fraction * (b[0] - a[0]), boundary
            return intersection

        points = clip_edge(points, lambda p: p[0] >= x_min, vertical(x_min))
        points = clip_edge(points, lambda p: p[0] <= x_max, vertical(x_max))
        points = clip_edge(points, lambda p: p[1] >= y_min, horizontal(y_min))
        return clip_edge(points, lambda p: p[1] <= y_max, horizontal(y_max))

    def project(ring: list[tuple[float, float]], group: str) -> str:
        lon_min, lon_max, x_min, x_max = groups[group]
        points = []
        for longitude, latitude in ring:
            longitude = max(lon_min, min(lon_max, longitude))
            latitude = max(-60.0, min(84.0, latitude))
            x = x_min + (longitude - lon_min) / (lon_max - lon_min) * (x_max - x_min)
            y = 242 + (84 - latitude) / 144 * 466
            points.append((x, y))
        return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in points) + " Z"

    windows = {
        "americas": [(-180.0, -20.0, -60.0, 84.0)],
        "africa": [(-25.0, 55.0, -40.0, 38.0)],
        # Eurasia is clipped in north and south windows because Natural Earth
        # stores Afro-Eurasia as one land polygon. Australia shares this hole.
        "eurasia": [(-20.0, 180.0, 30.0, 84.0), (35.0, 180.0, -15.0, 30.0), (110.0, 180.0, -50.0, -10.0)],
    }
    for feature in geojson["features"]:
        for ring in geometry_rings(feature["geometry"]):
            for group, boxes in windows.items():
                for box in boxes:
                    clipped = clip_polygon(ring, *box)
                    if len(clipped) >= 3:
                        longitudes = [longitude for longitude, _ in clipped]
                        latitudes = [latitude for _, latitude in clipped]
                        if (max(longitudes) - min(longitudes)) * (max(latitudes) - min(latitudes)) >= 1.0:
                            paths[group].append(project(clipped, group))

    americas = " ".join(paths["americas"])
    # Duplicate the cylindrical seam so both Atlantic and Pacific coast-facing
    # provinces terminate at the same recognizable continental cutout.
    # Translating the already projected path is cleaner and exactly symmetric.
    return (
        f'<path d="{americas}"/>'
        f'<path d="{americas}" transform="translate(1418 0)"/>'
        f'<path d="{" ".join(paths["eurasia"])}"/>'
        f'<path d="{" ".join(paths["africa"])}"/>'
    )


def clip_half_plane(
    polygon: list[tuple[float, float]],
    normal_x: float,
    normal_y: float,
    limit: float,
) -> list[tuple[float, float]]:
    """Clip a polygon to normal dot point <= limit."""
    if not polygon:
        return []
    result: list[tuple[float, float]] = []
    previous = polygon[-1]
    previous_value = normal_x * previous[0] + normal_y * previous[1] - limit
    for current in polygon:
        current_value = normal_x * current[0] + normal_y * current[1] - limit
        if current_value <= 0:
            if previous_value > 0:
                fraction = previous_value / (previous_value - current_value)
                result.append((
                    previous[0] + fraction * (current[0] - previous[0]),
                    previous[1] + fraction * (current[1] - previous[1]),
                ))
            result.append(current)
        elif previous_value <= 0:
            fraction = previous_value / (previous_value - current_value)
            result.append((
                previous[0] + fraction * (current[0] - previous[0]),
                previous[1] + fraction * (current[1] - previous[1]),
            ))
        previous, previous_value = current, current_value
    return result


def coastal_state_geometry(
    left: float = 92.0,
    top: float = 174.0,
    width: float = 1416.0,
    height: float = 644.0,
    latitude_top: float = 84.0,
    latitude_bottom: float = -72.0,
) -> tuple[str, list[str]]:
    """Build 56 periodic nearest-seed states and their label positions."""

    def project(longitude: float, latitude: float) -> tuple[float, float]:
        x = left + ((longitude + 180.0) % 360.0) / 360.0 * width
        y = top + (latitude_top - latitude) / (latitude_top - latitude_bottom) * height
        return x, y

    seeds = []
    lookup = {}
    for basin, provinces in PROVINCES.items():
        for code, name, biome in provinces:
            if code not in PROVINCE_SEEDS:
                raise ValueError(f"Missing coastal-state seed for {code}")
            x, y = project(*PROVINCE_SEEDS[code])
            item = (code, name, biome, basin, x, y)
            seeds.append(item)
            lookup[code] = item

    state_groups = []
    labels = []
    for code, name, biome, basin, seed_x, seed_y in seeds:
        pieces = []
        focus_box = None
        # Copies allow states at the dateline to appear on both map edges while
        # remaining one named province.
        for target_x in (seed_x - width, seed_x, seed_x + width):
            polygon = [(left, top), (left + width, top), (left + width, top + height), (left, top + height)]
            for other_code, _, _, _, other_x, other_y in seeds:
                for competitor_x in (other_x - width, other_x, other_x + width):
                    if other_code == code and abs(competitor_x - target_x) < 0.01:
                        continue
                    normal_x = competitor_x - target_x
                    normal_y = other_y - seed_y
                    limit = ((competitor_x * competitor_x + other_y * other_y)
                             - (target_x * target_x + seed_y * seed_y)) / 2.0
                    polygon = clip_half_plane(polygon, normal_x, normal_y, limit)
                    if not polygon:
                        break
                if not polygon:
                    break
            if len(polygon) >= 3:
                pieces.append("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in polygon) + " Z")
                if abs(target_x - seed_x) < 0.01:
                    xs, ys = [point[0] for point in polygon], [point[1] for point in polygon]
                    focus_box = (min(xs), min(ys), max(xs), max(ys))
        safe_code, safe_name = html.escape(code), html.escape(name)
        safe_id = code.lower().replace(" ", "-")
        if focus_box is None:
            focus_box = (seed_x - 35, seed_y - 35, seed_x + 35, seed_y + 35)
        viewbox = " ".join(f"{value:.1f}" for value in focus_box)
        state_groups.append(
            f'<g id="province-{safe_id}" class="province {biome.lower()}" tabindex="0" role="button" '
            f'data-code="{safe_code}" data-name="{safe_name}" data-basin="{html.escape(basin)}" '
            f'data-biome="{html.escape(biome)}" data-viewbox="{viewbox}" aria-label="Zoom to {safe_code}, {safe_name}">'
            f'<title>{safe_code} — {safe_name} · {basin} · approximate coastal-state cartogram</title>'
            f'<path d="{" ".join(pieces)}"/>'
            f'</g>'
        )
        labels.append(
            f'<text x="{seed_x:.1f}" y="{seed_y + 4:.1f}" data-code="{safe_code}">{safe_code}</text>'
        )
    return "".join(state_groups), labels


def projected_land_path(
    geojson: dict,
    left: float = 92.0,
    top: float = 174.0,
    width: float = 1416.0,
    height: float = 644.0,
    latitude_top: float = 84.0,
    latitude_bottom: float = -72.0,
) -> str:
    """Project Natural Earth land into the coastal-state map frame."""
    commands = []
    for feature in geojson["features"]:
        for ring in geometry_rings(feature["geometry"]):
            points = []
            for longitude, latitude in ring:
                x = left + (longitude + 180.0) / 360.0 * width
                bounded_latitude = max(latitude_bottom, min(latitude_top, latitude))
                y = top + (latitude_top - bounded_latitude) / (latitude_top - latitude_bottom) * height
                points.append((x, y))
            if len(points) >= 3:
                commands.append("M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in points) + " Z")
    return " ".join(commands)


def build_coastal_states_svg(geojson: dict, source_sha256: str) -> str:
    """Build the coast-owned province study requested after the lakes draft."""
    states, labels = coastal_state_geometry()
    land = projected_land_path(geojson)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1000" viewBox="0 0 1600 1000" role="img" aria-labelledby="title desc">
  <title id="title">OCEANLINES 56 coastal states study</title>
  <desc id="desc">A monochrome ocean-first map in which 56 approximate province states cover the world ocean. Real Natural Earth land is removed from the states, so coastal provinces inherit recognizable coastline edges. Internal boundaries are original nearest-seed approximations, not scientific Longhurst geometry.</desc>
  <metadata>Original OCEANLINES nearest-seed state geometry, MIT licensed. Coast edges use public-domain Natural Earth 1:110m land geometry, commit {SOURCE_COMMIT}, SHA-256 {source_sha256}, {SOURCE_URL}. Province seeds are approximate geographic placements; no geographic Longhurst boundary dataset is reproduced.</metadata>
  <defs>
    <mask id="ocean-only" maskUnits="userSpaceOnUse" x="0" y="0" width="1600" height="1000">
      <rect x="92" y="174" width="1416" height="644" fill="white"/>
      <path d="{land}" fill="black" fill-rule="evenodd"/>
    </mask>
  </defs>
  <style>
    .province path {{ fill:#d7dfdc; stroke:#183239; stroke-width:3.2; stroke-linejoin:round; vector-effect:non-scaling-stroke; }}
    .province:hover path,.province:focus path {{ fill:#f4f6f3; stroke:#07191e; stroke-width:6; }}
    .province:focus {{ outline:none; }}
    .labels text {{ fill:#10272d; font:900 10.5px ui-monospace,Consolas,monospace; text-anchor:middle; paint-order:stroke; stroke:#d7dfdc; stroke-width:3.2px; stroke-linejoin:round; pointer-events:none; }}
    .land-outline {{ fill:none; stroke:#879b9b; stroke-width:2; stroke-linejoin:round; vector-effect:non-scaling-stroke; }}
  </style>
  <rect width="1600" height="1000" fill="#06171c"/>
  <text x="72" y="70" fill="#b9cdca" font-family="ui-monospace,Consolas,monospace" font-size="13" font-weight="900" letter-spacing="2.2">EXPERIMENT 03C · COAST-OWNED STATES</text>
  <text x="72" y="123" fill="#eef4f1" font-family="Inter,Arial,sans-serif" font-size="46" font-weight="900" letter-spacing="-2">THE COAST BELONGS TO THE PROVINCE</text>
  <text x="1528" y="75" fill="#eef4f1" font-family="Inter,Arial,sans-serif" font-size="42" font-weight="950" text-anchor="end">56</text>
  <text x="1528" y="98" fill="#8da9a9" font-family="ui-monospace,Consolas,monospace" font-size="10" font-weight="800" letter-spacing="1.5" text-anchor="end">APPROXIMATE OCEAN STATES</text>
  <g mask="url(#ocean-only)">{states}</g>
  <path class="land-outline" d="{land}" fill-rule="evenodd" aria-label="Continents as negative-space lakes"/>
  <g class="labels" mask="url(#ocean-only)">{''.join(labels)}</g>
  <g transform="translate(92 872)" font-family="ui-monospace,Consolas,monospace">
    <text fill="#b9cdca" font-size="11" font-weight="900" letter-spacing="1.6">COAST-OWNED GEOMETRY</text>
    <text y="25" fill="#8da9a9" font-size="11">ALSK INHERITS ALASKA · HUMB INHERITS PERU/CHILE · BENG INHERITS SOUTHWEST AFRICA</text>
  </g>
  <g transform="translate(844 866)" font-family="ui-monospace,Consolas,monospace" font-size="10">
    <text fill="#eef4f1" font-weight="900" letter-spacing="1.4">ORIGINAL SCHEMATIC CARTOGRAM · NOT LONGHURST BOUNDARIES</text>
    <text y="22" fill="#8da9a9">Real coast edges; approximate nearest-seed internal borders and contacts.</text>
    <text y="38" fill="#8da9a9">The coastline is clipped into each province rather than overlaid as decoration.</text>
  </g>
  <text x="92" y="966" fill="#617d80" font-family="ui-monospace,Consolas,monospace" font-size="9">CLASSIC 56-PROVINCE VOCABULARY · NATURAL EARTH COASTS · ORIGINAL OCEANLINES STATE GEOMETRY</text>
</svg>'''


def build_interactive_states_svg(geojson: dict, source_sha256: str) -> str:
    """Build the Atlas 10 province ground in its existing 1600×1050 frame."""
    states, labels = coastal_state_geometry(60, 90, 1480, 740, 90, -90)
    land = projected_land_path(geojson, 60, 90, 1480, 740, 90, -90)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1050" viewBox="0 0 1600 1050" role="img" aria-labelledby="title desc">
  <title id="title">Interactive OCEANLINES 56-province ground</title>
  <desc id="desc">Selectable approximate ocean states with real coast-owned edges, aligned to every Atlas 10 conceptual and observed layer.</desc>
  <metadata>Original OCEANLINES nearest-seed geometry. Natural Earth 1:110m land, public domain, commit {SOURCE_COMMIT}, SHA-256 {source_sha256}. No geographic Longhurst boundary dataset is reproduced.</metadata>
  <defs><mask id="interactive-ocean-only"><rect x="60" y="90" width="1480" height="740" fill="white"/><path d="{land}" fill="black" fill-rule="evenodd"/></mask></defs>
  <style>
    .map-field {{ fill:#0b242b; }}
    .province path {{ fill:#d7dfdc; stroke:#183239; stroke-width:3; stroke-linejoin:round; vector-effect:non-scaling-stroke; transition:fill .15s,stroke .15s; }}
    .province:hover path,.province:focus path,.province.selected path {{ fill:#f4f6f3; stroke:#ffb454; stroke-width:5; }}
    .province:focus {{ outline:none; }}
    .province-labels text {{ fill:#10272d; font:900 10.5px ui-monospace,Consolas,monospace; text-anchor:middle; paint-order:stroke; stroke:#d7dfdc; stroke-width:3.2px; pointer-events:none; }}
    .land-outline {{ fill:none; stroke:#879b9b; stroke-width:2; stroke-linejoin:round; vector-effect:non-scaling-stroke; pointer-events:none; }}
  </style>
  <rect class="map-field" x="60" y="90" width="1480" height="740" rx="28"/>
  <g class="province-field" mask="url(#interactive-ocean-only)">{states}</g>
  <path class="land-outline" d="{land}" fill-rule="evenodd"/>
  <g class="province-labels" mask="url(#interactive-ocean-only)">{''.join(labels)}</g>
  <rect class="map-frame" x="60" y="90" width="1480" height="740" rx="28" fill="none" stroke="#456972" stroke-width="2"/>
</svg>'''


def build_lakes_svg(geojson: dict, source_sha256: str) -> str:
    count = sum(len(values) for values in PROVINCES.values())
    if count != 56:
        raise ValueError(f"Expected 56 provinces, found {count}")
    clusters = "".join(
        [
            render_strip("Arctic", 174, 64, monochrome=True),
            render_cluster("Pacific", 92, 256, 650, 424, 5, monochrome=True),
            render_cluster("Indian", 786, 256, 244, 424, 2, monochrome=True),
            render_cluster("Atlantic", 1074, 256, 434, 424, 4, monochrome=True),
            render_strip("Southern", 726, 92, monochrome=True),
        ]
    )
    holes = continent_hole_path(geojson)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1000" viewBox="0 0 1600 1000" role="img" aria-labelledby="title desc">
  <title id="title">OCEANLINES monochrome 56-province lakes cartogram</title>
  <desc id="desc">A monochrome state-map study of the classic 56 Longhurst surface-ocean provinces. Continents are compressed real-coastline holes cut out of the unified ocean field like lakes. Province shapes, sizes, and most internal adjacencies remain schematic and non-metric.</desc>
  <metadata>Original OCEANLINES province cartogram, MIT licensed. Continental cutouts use public-domain Natural Earth 1:110m land geometry, commit {SOURCE_COMMIT}, SHA-256 {source_sha256}, {SOURCE_URL}. The continental silhouettes are strongly compressed horizontally. No geographic Longhurst boundary dataset is reproduced.</metadata>
  <defs>
    <mask id="continent-cutouts" maskUnits="userSpaceOnUse" x="0" y="0" width="1600" height="1000">
      <rect width="1600" height="1000" fill="white"/>
      <g fill="black" fill-rule="evenodd">{holes}</g>
    </mask>
  </defs>
  <style>
    .province path {{ stroke:#183239; stroke-width:5; stroke-linejoin:round; transition:fill .15s,stroke .15s; }}
    .province text {{ font:900 15px ui-monospace,Consolas,monospace; text-anchor:middle; pointer-events:none; }}
    .province:focus {{ outline:none; }} .province:hover path,.province:focus path {{ fill:#f4f7f3; stroke:#06171c; stroke-width:8; }}
    .basin-label {{ fill:#587479; font:800 12px ui-monospace,Consolas,monospace; letter-spacing:4px; text-anchor:middle; }}
    .ocean-body {{ fill:#d4dfdc; stroke:#183239; stroke-width:5; }}
    .hole-outline {{ fill:none; stroke:#789398; stroke-width:2.5; stroke-linejoin:round; }}
    .hole-label {{ fill:#a8babc; font:800 8px ui-monospace,Consolas,monospace; letter-spacing:1.4px; text-anchor:middle; paint-order:stroke; stroke:#06171c; stroke-width:3px; }}
  </style>
  <rect width="1600" height="1000" fill="#06171c"/>
  <text x="72" y="70" fill="#b9cdca" font-family="ui-monospace,Consolas,monospace" font-size="13" font-weight="900" letter-spacing="2.2">EXPERIMENT 03B · CONTINENTS AS LAKES</text>
  <text x="72" y="123" fill="#eef4f1" font-family="Inter,Arial,sans-serif" font-size="46" font-weight="900" letter-spacing="-2">THE OCEAN, AS 56 PROVINCES</text>
  <text x="1528" y="75" fill="#eef4f1" font-family="Inter,Arial,sans-serif" font-size="42" font-weight="950" text-anchor="end">56</text>
  <text x="1528" y="98" fill="#8da9a9" font-family="ui-monospace,Consolas,monospace" font-size="10" font-weight="800" letter-spacing="1.5" text-anchor="end">ONE CONNECTED MAP</text>
  <g mask="url(#continent-cutouts)">
    <path class="ocean-body" d="M92 174H1508V818H92Z"/>
    {clusters}
  </g>
  <g class="hole-outline" aria-label="Continental holes cut from the province field">{holes}</g>
  <text class="hole-label" x="92" y="480" transform="rotate(-90 92 480)">AMERICAS</text>
  <text class="hole-label" x="1510" y="480" transform="rotate(90 1510 480)">AMERICAS</text>
  <text class="hole-label" x="765" y="470" transform="rotate(-90 765 470)">EURASIA · AUSTRALIA</text>
  <text class="hole-label" x="1053" y="500" transform="rotate(-90 1053 500)">AFRICA</text>
  <g transform="translate(92 872)" font-family="ui-monospace,Consolas,monospace">
    <text fill="#b9cdca" font-size="11" font-weight="900" letter-spacing="1.6">STATE-MAP STUDY</text>
    <text y="25" fill="#8da9a9" font-size="11">ONE FILL · 56 LABELED PIECES · CONTINENTS BECOME NEGATIVE SPACE</text>
  </g>
  <g transform="translate(844 866)" font-family="ui-monospace,Consolas,monospace" font-size="10">
    <text fill="#eef4f1" font-weight="900" letter-spacing="1.4">REFERENCE CARTOGRAM · NOT A PROJECTION</text>
    <text y="22" fill="#8da9a9">Real coastlines cut the edge pieces, but are horizontally compressed.</text>
    <text y="38" fill="#8da9a9">Province shape, size, distance, and most adjacency remain schematic.</text>
    <text y="62" fill="#8da9a9">The next study varies the 56 internal puzzle shapes.</text>
  </g>
  <text x="92" y="966" fill="#617d80" font-family="ui-monospace,Consolas,monospace" font-size="9">LONGHURST CLASSIC 56-PROVINCE IDENTITY · NATURAL EARTH CONTINENTAL CUTOUTS · ORIGINAL OCEANLINES LAYOUT</text>
</svg>'''


def build_svg(geojson: dict, source_sha256: str) -> str:
    count = sum(len(values) for values in PROVINCES.values())
    if count != 56:
        raise ValueError(f"Expected 56 provinces, found {count}")

    clusters = "".join(
        [
            render_strip("Arctic", 174, 64),
            render_cluster("Pacific", 92, 256, 650, 424, 5),
            render_cluster("Indian", 786, 256, 244, 424, 2),
            render_cluster("Atlantic", 1074, 256, 434, 424, 4),
            render_strip("Southern", 726, 92),
        ]
    )
    continental_context = render_continental_context(geojson)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1000" viewBox="0 0 1600 1000" role="img" aria-labelledby="title desc">
  <title id="title">OCEANLINES 56-province ocean cartogram</title>
  <desc id="desc">An original flat reference layout of the classic 56 Longhurst surface-ocean provinces. Pacific, Indian, and Atlantic province groups occupy most of the canvas, joined by an Arctic cap and a Southern Ocean base. Real Natural Earth coastlines are horizontally compressed into narrow continental fingerprints. Province shapes and areas remain schematic; hover or focus a province to read its full name.</desc>
  <metadata>Original OCEANLINES cartogram geometry, MIT licensed. Province identities follow the classic 56-province vocabulary discussed by Reygondeau et al. 2013, DOI 10.1002/gbc.20089, with OCAL and CCAL shown separately as in the older classification. Continental context uses public-domain Natural Earth 1:110m land geometry, commit {SOURCE_COMMIT}, SHA-256 {source_sha256}, {SOURCE_URL}. This graphic does not reproduce the CC-BY-NC-SA Marine Regions boundary dataset.</metadata>
  <style>
    .province path {{ stroke:#06171c; stroke-width:5; stroke-linejoin:round; transition:filter .15s,stroke .15s; }}
    .province text {{ font:900 15px ui-monospace,Consolas,monospace; text-anchor:middle; pointer-events:none; }}
    .province:focus {{ outline:none; }} .province:hover path,.province:focus path {{ stroke:#fff4d7; stroke-width:8; filter:brightness(1.12); }}
    .basin-label {{ fill:#76969a; font:800 12px ui-monospace,Consolas,monospace; letter-spacing:4px; text-anchor:middle; }}
    .land-bed {{ fill:#d7ddd5; opacity:.08; }}
    .coastline {{ fill:none; stroke:#d7ddd5; stroke-width:1.5; stroke-opacity:.48; stroke-linecap:round; stroke-linejoin:round; }}
    .land-label {{ fill:#c0d0cc; font:800 8px ui-monospace,Consolas,monospace; letter-spacing:1.4px; text-anchor:middle; paint-order:stroke; stroke:#243b3e; stroke-width:3px; }}
  </style>
  <rect width="1600" height="1000" fill="#06171c"/>
  <text x="72" y="70" fill="#67e4da" font-family="ui-monospace,Consolas,monospace" font-size="13" font-weight="900" letter-spacing="2.2">EXPERIMENT 03 · PROVINCE ATLAS</text>
  <text x="72" y="123" fill="#eef9f7" font-family="Inter,Arial,sans-serif" font-size="46" font-weight="900" letter-spacing="-2">THE OCEAN, DRAWN LIKE A COUNTRY</text>
  <text x="1528" y="75" fill="#ffb454" font-family="Inter,Arial,sans-serif" font-size="42" font-weight="950" text-anchor="end">56</text>
  <text x="1528" y="98" fill="#8da9a9" font-family="ui-monospace,Consolas,monospace" font-size="10" font-weight="800" letter-spacing="1.5" text-anchor="end">CLASSIC SURFACE PROVINCES</text>

{continental_context}
  {clusters}

  <g transform="translate(92 872)" font-family="ui-monospace,Consolas,monospace">
    <text fill="#67e4da" font-size="11" font-weight="900" letter-spacing="1.6">FOUR BIOMES</text>
    <rect y="20" width="23" height="23" rx="4" fill="#8bd8e8"/><text x="33" y="36" fill="#a9c0c0" font-size="11">POLAR</text>
    <rect x="128" y="20" width="23" height="23" rx="4" fill="#5eb8cf"/><text x="161" y="36" fill="#a9c0c0" font-size="11">WESTERLIES</text>
    <rect x="303" y="20" width="23" height="23" rx="4" fill="#f1b65b"/><text x="336" y="36" fill="#a9c0c0" font-size="11">TRADE WINDS</text>
    <rect x="477" y="20" width="23" height="23" rx="4" fill="#72d3b0"/><text x="510" y="36" fill="#a9c0c0" font-size="11">COASTAL</text>
  </g>
  <g transform="translate(844 866)" font-family="ui-monospace,Consolas,monospace" font-size="10">
    <text fill="#ffb454" font-weight="900" letter-spacing="1.4">REFERENCE CARTOGRAM · NOT A PROJECTION</text>
    <text y="22" fill="#8da9a9">Adjacency and basin order are emphasized; shape, area, distance,</text>
    <text y="38" fill="#8da9a9">direction, and exact coast contact are intentionally not preserved.</text>
    <text y="62" fill="#8da9a9">Static provinces are mean ecological references. Natural boundaries move.</text>
  </g>
  <text x="92" y="966" fill="#617d80" font-family="ui-monospace,Consolas,monospace" font-size="9">LONGHURST CLASSIC 56-PROVINCE REFERENCE · ORIGINAL OCEANLINES LAYOUT · DOI 10.1002/GBC.20089</text>
</svg>'''


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        default=pathlib.Path(__file__).resolve().parents[1] / "figures" / "oceanlines-province-atlas.svg",
    )
    parser.add_argument(
        "--lakes-output",
        type=pathlib.Path,
        default=pathlib.Path(__file__).resolve().parents[1] / "figures" / "oceanlines-province-atlas-lakes.svg",
    )
    parser.add_argument(
        "--coastal-states-output",
        type=pathlib.Path,
        default=pathlib.Path(__file__).resolve().parents[1] / "figures" / "oceanlines-province-atlas-coastal-states.svg",
    )
    parser.add_argument(
        "--interactive-states-output",
        type=pathlib.Path,
        default=pathlib.Path(__file__).resolve().parents[1] / "figures" / "oceanlines-province-atlas-interactive.svg",
    )
    parser.add_argument("--land-geojson", required=True, type=pathlib.Path)
    parser.add_argument(
        "--catalog-output",
        type=pathlib.Path,
        default=pathlib.Path(__file__).resolve().parents[1] / "research" / "longhurst-province-reference.csv",
    )
    args = parser.parse_args()
    payload = args.land_geojson.read_bytes()
    digest = hashlib.sha256(payload).hexdigest()
    if digest != EXPECTED_SOURCE_SHA256:
        raise SystemExit(f"Natural Earth source checksum mismatch: {digest}")
    geojson = json.loads(payload)
    args.output.write_text(build_svg(geojson, digest), encoding="utf-8", newline="\n")
    args.lakes_output.write_text(build_lakes_svg(geojson, digest), encoding="utf-8", newline="\n")
    args.coastal_states_output.write_text(build_coastal_states_svg(geojson, digest), encoding="utf-8", newline="\n")
    args.interactive_states_output.write_text(build_interactive_states_svg(geojson, digest), encoding="utf-8", newline="\n")
    with args.catalog_output.open("w", encoding="utf-8", newline="") as destination:
        writer = csv.writer(destination, lineterminator="\n")
        writer.writerow(("code", "province", "basin", "biome", "edition", "geometry_status"))
        for basin, provinces in PROVINCES.items():
            for code, province, biome in provinces:
                writer.writerow((code, province, basin, biome, "classic 56-province reference", "OCEANLINES non-metric cartogram"))
    print(args.output)
    print(args.lakes_output)
    print(args.coastal_states_output)
    print(args.interactive_states_output)
    print(args.catalog_output)


if __name__ == "__main__":
    main()
