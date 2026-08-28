"""Build the OCEANLINES conceptual fluid-geography SVG.

The coastline is generated from Natural Earth 1:110m land geometry. All heat
reservoirs, paths, anomalies, buried layers, gates, and labels remain explicitly
conceptual OCEANLINES artwork.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
from pathlib import Path


WIDTH = 1600
HEIGHT = 1050
MAP_X = 60
MAP_Y = 90
MAP_WIDTH = 1480
MAP_HEIGHT = 740
EXPECTED_SOURCE_SHA256 = "9e0729ee253ca7d7a5c4ae9395fb1902264c5377c52e224d13dd85010e2835d9"
SOURCE_COMMIT = "ca96624a56bd078437bca8184e78163e5039ad19"
SOURCE_URL = (
    "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/"
    f"{SOURCE_COMMIT}/geojson/ne_110m_land.geojson"
)


def project(longitude: float, latitude: float) -> tuple[float, float]:
    x = MAP_X + (longitude + 180.0) / 360.0 * MAP_WIDTH
    y = MAP_Y + (90.0 - latitude) / 180.0 * MAP_HEIGHT
    return x, y


def ring_path(ring: list[list[float]]) -> str:
    commands: list[str] = []
    previous_longitude: float | None = None
    for longitude, latitude, *_ in ring:
        x, y = project(longitude, latitude)
        command = "M" if previous_longitude is None or abs(longitude - previous_longitude) > 180 else "L"
        commands.append(f"{command}{x:.1f},{y:.1f}")
        previous_longitude = longitude
    if commands:
        commands.append("Z")
    return " ".join(commands)


def land_path(geojson: dict) -> str:
    paths: list[str] = []
    for feature in geojson["features"]:
        geometry = feature["geometry"]
        coordinates = geometry["coordinates"]
        polygons = [coordinates] if geometry["type"] == "Polygon" else coordinates
        for polygon in polygons:
            for ring in polygon:
                paths.append(ring_path(ring))
    return " ".join(paths)


def callout(
    number: int,
    title: str,
    subtitle: str,
    label_x: int,
    label_y: int,
    target_x: int,
    target_y: int,
    accent: str,
    width: int = 230,
) -> str:
    start_x = label_x + width / 2
    start_y = label_y + 54
    return f"""
      <g class="callout">
        <path class="leader" d="M{start_x:.1f},{start_y:.1f} Q{start_x:.1f},{target_y:.1f} {target_x},{target_y}"/>
        <circle class="anchor" cx="{target_x}" cy="{target_y}" r="5" style="--accent:{accent}"/>
        <rect x="{label_x}" y="{label_y}" width="{width}" height="54" rx="11"/>
        <circle cx="{label_x + 27}" cy="{label_y + 27}" r="17" style="fill:{accent}"/>
        <text class="number" x="{label_x + 27}" y="{label_y + 32}">{number:02d}</text>
        <text class="label-title" x="{label_x + 55}" y="{label_y + 23}">{html.escape(title)}</text>
        <text class="label-subtitle" x="{label_x + 55}" y="{label_y + 41}">{html.escape(subtitle)}</text>
      </g>"""


def build_svg(coastline_path: str, source_sha256: str, include_callouts: bool = True) -> str:
    callouts = "".join(
        [
            callout(3, "Northeast Pacific Blob", "transient anomaly", 80, 170, 205, 285, "#ff766c", 250),
            callout(5, "Gulf Stream", "boundary heat pathway", 375, 165, 540, 315, "#ffb454", 220),
            callout(10, "Atlantic Water", "buried below Arctic lid", 680, 112, 920, 170, "#b7a7ff", 245),
            callout(6, "Kuroshio", "boundary heat pathway", 1270, 170, 1395, 320, "#ffb454", 220),
            callout(4, "El Niño tongue", "equatorial anomaly", 80, 450, 290, 470, "#ff766c", 225),
            callout(2, "Western warm pool", "seasonal reservoir", 385, 420, 500, 430, "#ffc862", 250),
            callout(1, "Indo-Pacific warm pool", "persistent reservoir", 1065, 405, 1360, 445, "#ffc862", 280),
            callout(12, "Indonesian Throughflow", "archipelagic gate", 1185, 505, 1288, 485, "#67e4da", 280),
            callout(11, "Drake Passage", "circumpolar gate", 150, 670, 530, 694, "#67e4da", 235),
            callout(9, "Circumpolar Deep Water", "buried reservoir", 455, 712, 790, 700, "#b7a7ff", 290),
            callout(7, "Agulhas system", "current + rings", 815, 610, 905, 625, "#ffb454", 225),
            callout(8, "Circumpolar Current", "fronted ocean belt", 1115, 695, 1260, 704, "#8eeaf2", 270),
        ]
    ) if include_callouts else ""

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">
  <title id="title">OCEANLINES fluid geography of Earth's ocean</title>
  <desc id="desc">An ocean-first conceptual map on Natural Earth coastlines. Twelve numbered callouts identify warm reservoirs, boundary-current pathways, transient anomalies, buried polar water masses, the Antarctic Circumpolar Current, and exchange gates. All heat shapes and pathways are schematic, permeable, and moving rather than measured boundaries. The figure does not calculate heat content or transport.</desc>
  <metadata>
    Natural Earth 1:110m land geometry, public domain, commit {SOURCE_COMMIT}, source SHA-256 {source_sha256}, {SOURCE_URL}. OCEANLINES conceptual overlays are original MIT-licensed artwork.
  </metadata>
  <defs>
    <linearGradient id="ocean" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#123d4b"/>
      <stop offset="0.47" stop-color="#0a2b39"/>
      <stop offset="1" stop-color="#071c29"/>
    </linearGradient>
    <radialGradient id="warmPool" cx="50%" cy="50%" r="55%">
      <stop offset="0" stop-color="#ffd66f" stop-opacity=".92"/>
      <stop offset=".45" stop-color="#ffad48" stop-opacity=".66"/>
      <stop offset="1" stop-color="#ff7d48" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="blob" cx="50%" cy="50%" r="55%">
      <stop offset="0" stop-color="#ff766c" stop-opacity=".54"/>
      <stop offset="1" stop-color="#ff766c" stop-opacity=".04"/>
    </radialGradient>
    <linearGradient id="buriedBand" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#8c7be7" stop-opacity=".08"/>
      <stop offset=".5" stop-color="#c1b4ff" stop-opacity=".48"/>
      <stop offset="1" stop-color="#8c7be7" stop-opacity=".08"/>
    </linearGradient>
    <pattern id="buriedPattern" width="14" height="14" patternUnits="userSpaceOnUse" patternTransform="rotate(28)">
      <rect width="14" height="14" fill="#8c7be7" fill-opacity=".12"/>
      <path d="M0 0V14" stroke="#cfc6ff" stroke-width="3" stroke-opacity=".4"/>
    </pattern>
    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="8" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="cardShadow" x="-20%" y="-30%" width="140%" height="170%">
      <feDropShadow dx="0" dy="5" stdDeviation="7" flood-color="#020b10" flood-opacity=".58"/>
    </filter>
    <marker id="warmArrow" viewBox="0 0 12 12" refX="10" refY="6" markerWidth="8" markerHeight="8" orient="auto"><path d="M1 1L11 6 1 11Z" fill="#ffb454"/></marker>
    <marker id="coldArrow" viewBox="0 0 12 12" refX="10" refY="6" markerWidth="8" markerHeight="8" orient="auto"><path d="M1 1L11 6 1 11Z" fill="#8eeaf2"/></marker>
    <clipPath id="mapClip"><rect x="{MAP_X}" y="{MAP_Y}" width="{MAP_WIDTH}" height="{MAP_HEIGHT}" rx="28"/></clipPath>
    <path id="landGeometry" fill-rule="evenodd" d="{coastline_path}"/>
    <style>
      text {{ font-family: Inter, ui-sans-serif, system-ui, sans-serif; }}
      .grid {{ fill:none; stroke:#b6e0e3; stroke-opacity:.12; stroke-width:1; }}
      .geo-label {{ fill:#b2d1d2; fill-opacity:.38; font-size:18px; font-weight:700; letter-spacing:5px; }}
      .land {{ fill:#182d31; stroke:#799395; stroke-width:1.5; vector-effect:non-scaling-stroke; }}
      .coast-glow {{ fill:none; stroke:#b7ccca; stroke-opacity:.2; stroke-width:5; vector-effect:non-scaling-stroke; }}
      .current-halo {{ fill:none; stroke:#031116; stroke-opacity:.72; stroke-width:17; stroke-linecap:round; stroke-linejoin:round; }}
      .current {{ fill:none; stroke:#ffb454; stroke-width:8; stroke-linecap:round; stroke-linejoin:round; filter:url(#softGlow); marker-end:url(#warmArrow); }}
      .acc-halo {{ fill:none; stroke:#031116; stroke-opacity:.76; stroke-width:20; }}
      .acc {{ fill:none; stroke:#8eeaf2; stroke-width:8; stroke-dasharray:20 11; filter:url(#softGlow); marker-end:url(#coldArrow); }}
      .gate {{ fill:#071b22; stroke:#67e4da; stroke-width:4; }}
      .callout .leader {{ fill:none; stroke:#a9c6c6; stroke-opacity:.5; stroke-width:1.5; }}
      .callout .anchor {{ fill:var(--accent); stroke:#071b22; stroke-width:3; }}
      .callout rect {{ fill:#071b22; fill-opacity:.9; stroke:#35555b; stroke-width:1; filter:url(#cardShadow); }}
      .callout .number {{ fill:#071b22; font-size:13px; font-weight:900; text-anchor:middle; }}
      .callout .label-title {{ fill:#eef9f7; font-size:14px; font-weight:750; }}
      .callout .label-subtitle {{ fill:#8da9a9; font-size:11px; }}
    </style>
  </defs>

  <rect width="1600" height="1050" fill="#06171c"/>
  <text x="60" y="43" fill="#67e4da" font-size="15" font-weight="900" letter-spacing="4">OCEANLINES / FLUID GEOGRAPHY</text>
  <text x="1540" y="43" text-anchor="end" fill="#ffb454" font-size="12" font-weight="800" letter-spacing="2.2">CONCEPTUAL ATLAS · NOT A HEAT BUDGET</text>

  <g clip-path="url(#mapClip)">
    <rect x="{MAP_X}" y="{MAP_Y}" width="{MAP_WIDTH}" height="{MAP_HEIGHT}" fill="url(#ocean)"/>
    <path class="grid" d="M60 275H1540M60 460H1540M60 645H1540M307 90V830M553 90V830M800 90V830M1047 90V830M1293 90V830"/>
    <text class="geo-label" x="210" y="470">PACIFIC</text>
    <text class="geo-label" x="650" y="465">ATLANTIC</text>
    <text class="geo-label" x="1015" y="500">INDIAN</text>
    <text class="geo-label" x="1310" y="470">PACIFIC</text>

    <path d="M60 674C280 650 490 679 735 660C970 642 1260 672 1540 652L1540 760C1280 742 1040 756 800 746C530 735 300 760 60 742Z" fill="url(#buriedBand)" stroke="#b7a7ff" stroke-opacity=".5" stroke-width="2" stroke-dasharray="11 8"/>
    <path d="M770 126C850 102 980 108 1058 146C1090 162 1078 203 1035 221C955 255 824 241 767 206C733 186 739 141 770 126Z" fill="url(#buriedPattern)" stroke="#b7a7ff" stroke-opacity=".6" stroke-width="2" stroke-dasharray="9 7"/>

    <ellipse cx="1345" cy="442" rx="255" ry="98" fill="url(#warmPool)" stroke="#ffc862" stroke-opacity=".72" stroke-width="2.5"/>
    <ellipse cx="73" cy="452" rx="180" ry="86" fill="url(#warmPool)" stroke="#ffc862" stroke-opacity=".48" stroke-width="2.5"/>
    <ellipse cx="485" cy="430" rx="180" ry="82" fill="url(#warmPool)" stroke="#ffc862" stroke-opacity=".68" stroke-width="2.5"/>
    <ellipse cx="205" cy="285" rx="132" ry="78" fill="url(#blob)" stroke="#ff8d84" stroke-width="2.5" stroke-dasharray="11 8"/>
    <path d="M60 444C145 422 250 428 365 451C435 465 485 478 540 500C460 520 375 515 288 493C195 470 121 473 60 480Z" fill="#ff766c" fill-opacity=".22" stroke="#ff8d84" stroke-width="2.5" stroke-dasharray="11 8"/>

    <use href="#landGeometry" class="coast-glow"/>
    <use href="#landGeometry" class="land"/>

    <path class="current-halo" d="M470 390C480 353 506 332 540 315C578 296 620 275 658 250"/>
    <path class="current" d="M470 390C480 353 506 332 540 315C578 296 620 275 658 250"/>
    <path class="current-halo" d="M1330 385C1340 350 1360 333 1395 320C1440 303 1480 282 1515 254"/>
    <path class="current" d="M1330 385C1340 350 1360 333 1395 320C1440 303 1480 282 1515 254"/>
    <path class="current-halo" d="M925 520C944 559 946 597 922 626C895 656 850 655 818 633"/>
    <path class="current" d="M925 520C944 559 946 597 922 626C895 656 850 655 818 633"/>
    <path class="acc-halo" d="M60 704C280 679 500 710 745 693C1002 675 1260 709 1540 690"/>
    <path class="acc" d="M60 704C280 679 500 710 745 693C1002 675 1260 709 1540 690"/>

    <g fill="none" stroke="#ffd06b" stroke-width="4">
      <path d="M602 292c-22-20-53 4-35 28c15 20 50 5 40-21c-8-21-38-20-50-3"/>
      <path d="M852 636c-22-20-53 4-35 28c15 20 50 5 40-21c-8-21-38-20-50-3"/>
      <path d="M1462 294c-20-18-48 4-31 26c14 18 45 4 36-19c-7-19-34-18-45-3"/>
    </g>

    <g>
      <path class="gate" d="M522 682l10 12-10 12-10-12Z"/>
      <path class="gate" d="M1288 470l10 12-10 12-10-12Z"/>
      <path class="gate" d="M905 612l10 12-10 12-10-12Z"/>
    </g>
    {callouts}
  </g>

  <rect x="{MAP_X}" y="{MAP_Y}" width="{MAP_WIDTH}" height="{MAP_HEIGHT}" rx="28" fill="none" stroke="#456972" stroke-width="2"/>

  <g transform="translate(60 858)">
    <text x="0" y="17" fill="#67e4da" font-size="12" font-weight="900" letter-spacing="2.5">READ THE MAP BY MECHANISM, NOT COLOR ALONE</text>
    <g transform="translate(0 38)">
      <rect width="282" height="96" rx="14" fill="#0a2229" stroke="#29484f"/>
      <ellipse cx="45" cy="47" rx="27" ry="18" fill="url(#warmPool)" stroke="#ffc862"/>
      <text x="84" y="39" fill="#eef9f7" font-size="14" font-weight="800">RESERVOIR</text><text x="84" y="61" fill="#8da9a9" font-size="11">persistent or seasonal heatmass</text>
    </g>
    <g transform="translate(299 38)">
      <rect width="282" height="96" rx="14" fill="#0a2229" stroke="#29484f"/>
      <path d="M20 58C43 30 62 31 84 50" fill="none" stroke="#ffb454" stroke-width="7" marker-end="url(#warmArrow)"/>
      <text x="104" y="39" fill="#eef9f7" font-size="14" font-weight="800">PATHWAY</text><text x="104" y="61" fill="#8da9a9" font-size="11">current carrying water and energy</text>
    </g>
    <g transform="translate(598 38)">
      <rect width="282" height="96" rx="14" fill="#0a2229" stroke="#29484f"/>
      <ellipse cx="45" cy="48" rx="28" ry="19" fill="url(#blob)" stroke="#ff8d84" stroke-dasharray="7 5"/>
      <text x="86" y="39" fill="#eef9f7" font-size="14" font-weight="800">ANOMALY</text><text x="86" y="61" fill="#8da9a9" font-size="11">temporary departure from baseline</text>
    </g>
    <g transform="translate(897 38)">
      <rect width="282" height="96" rx="14" fill="#0a2229" stroke="#29484f"/>
      <rect x="19" y="29" width="55" height="39" rx="8" fill="url(#buriedPattern)" stroke="#b7a7ff"/>
      <text x="91" y="39" fill="#eef9f7" font-size="14" font-weight="800">BURIED LAYER</text><text x="91" y="61" fill="#8da9a9" font-size="11">warm water below a cold or fresh lid</text>
    </g>
    <g transform="translate(1196 38)">
      <rect width="284" height="96" rx="14" fill="#0a2229" stroke="#29484f"/>
      <path class="gate" d="M42 34l13 14-13 14-13-14Z"/>
      <text x="84" y="39" fill="#eef9f7" font-size="14" font-weight="800">GATE</text><text x="84" y="61" fill="#8da9a9" font-size="11">section constraining exchange</text>
    </g>
    <text x="740" y="160" text-anchor="middle" fill="#789497" font-size="11">NATURAL EARTH COASTLINES · CONCEPTUAL OCEAN OVERLAYS · PERMEABLE, MOVING, DEPTH-DEPENDENT · NOT A LIVE ANALYSIS</text>
  </g>
</svg>
'''


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--land-geojson", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--interactive-output", type=Path)
    args = parser.parse_args()

    payload = args.land_geojson.read_bytes()
    digest = hashlib.sha256(payload).hexdigest()
    if digest != EXPECTED_SOURCE_SHA256:
        raise SystemExit(f"Natural Earth source checksum mismatch: {digest}")
    geojson = json.loads(payload)
    coastline_path = land_path(geojson)
    svg = build_svg(coastline_path, digest)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(svg, encoding="utf-8", newline="\n")
    if args.interactive_output:
        interactive_svg = build_svg(coastline_path, digest, include_callouts=False)
        args.interactive_output.parent.mkdir(parents=True, exist_ok=True)
        args.interactive_output.write_text(interactive_svg, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
