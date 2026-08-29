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


def render_cluster(name: str, x: int, y: int, width: int, height: int, columns: int) -> str:
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
        fill, ink = COLORS[biome]
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


def render_strip(name: str, y: int, height: int) -> str:
    provinces = PROVINCES[name]
    x, width = 92, 1416
    cell_w = width / len(provinces)
    parts = [f'<g class="basin" id="{name.lower()}-provinces">']
    for index, (code, province, biome) in enumerate(provinces):
        x0, x1 = x + index * cell_w, x + (index + 1) * cell_w
        fill, ink = COLORS[biome]
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
    with args.catalog_output.open("w", encoding="utf-8", newline="") as destination:
        writer = csv.writer(destination, lineterminator="\n")
        writer.writerow(("code", "province", "basin", "biome", "edition", "geometry_status"))
        for basin, provinces in PROVINCES.items():
            for code, province, biome in provinces:
                writer.writerow((code, province, basin, biome, "classic 56-province reference", "OCEANLINES non-metric cartogram"))
    print(args.output)
    print(args.catalog_output)


if __name__ == "__main__":
    main()
