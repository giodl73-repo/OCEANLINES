"""Build the OCEANLINES 56-province reference cartogram.

This is an original adjacency-inspired atlas layout, not a geographic projection
or a redistribution of the Marine Regions Longhurst geometry.  Province codes,
names, basin membership, and biome membership are factual reference data drawn
from the cited Longhurst literature.
"""

from __future__ import annotations

import argparse
import csv
import html
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


def build_svg() -> str:
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
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1000" viewBox="0 0 1600 1000" role="img" aria-labelledby="title desc">
  <title id="title">OCEANLINES 56-province ocean cartogram</title>
  <desc id="desc">An original flat reference layout of the classic 56 Longhurst surface-ocean provinces. Pacific, Indian, and Atlantic province groups occupy most of the canvas, joined by an Arctic cap and a Southern Ocean base. Narrow pale land ribbons provide continental context. Shapes and areas are schematic; hover or focus a province to read its full name.</desc>
  <metadata>Original OCEANLINES cartogram geometry, MIT licensed. Province identities follow the classic 56-province vocabulary discussed by Reygondeau et al. 2013, DOI 10.1002/gbc.20089, with OCAL and CCAL shown separately as in the older classification. This graphic does not reproduce the CC-BY-NC-SA Marine Regions boundary dataset.</metadata>
  <style>
    .province path {{ stroke:#06171c; stroke-width:5; stroke-linejoin:round; transition:filter .15s,stroke .15s; }}
    .province text {{ font:900 15px ui-monospace,Consolas,monospace; text-anchor:middle; pointer-events:none; }}
    .province:focus {{ outline:none; }} .province:hover path,.province:focus path {{ stroke:#fff4d7; stroke-width:8; filter:brightness(1.12); }}
    .basin-label {{ fill:#76969a; font:800 12px ui-monospace,Consolas,monospace; letter-spacing:4px; text-anchor:middle; }}
    .land {{ fill:#d7ddd5; opacity:.26; stroke:#d7ddd5; stroke-width:2; }}
    .land-label {{ fill:#8da4a2; font:700 9px ui-monospace,Consolas,monospace; letter-spacing:1.6px; text-anchor:middle; }}
  </style>
  <rect width="1600" height="1000" fill="#06171c"/>
  <text x="72" y="70" fill="#67e4da" font-family="ui-monospace,Consolas,monospace" font-size="13" font-weight="900" letter-spacing="2.2">EXPERIMENT 03 · PROVINCE ATLAS</text>
  <text x="72" y="123" fill="#eef9f7" font-family="Inter,Arial,sans-serif" font-size="46" font-weight="900" letter-spacing="-2">THE OCEAN, DRAWN LIKE A COUNTRY</text>
  <text x="1528" y="75" fill="#ffb454" font-family="Inter,Arial,sans-serif" font-size="42" font-weight="950" text-anchor="end">56</text>
  <text x="1528" y="98" fill="#8da9a9" font-family="ui-monospace,Consolas,monospace" font-size="10" font-weight="800" letter-spacing="1.5" text-anchor="end">CLASSIC SURFACE PROVINCES</text>

  <g aria-label="Continental context">
    <path class="land" d="M64 272L88 256L93 358L74 390L92 449L74 508L93 579L84 680L61 704Z"/>
    <text class="land-label" x="72" y="490" transform="rotate(-90 72 490)">AMERICAS</text>
    <path class="land" d="M748 257L777 273L771 346L786 377L769 430L785 487L774 554L789 620L758 680Z"/>
    <text class="land-label" x="770" y="475" transform="rotate(-90 770 475)">ASIA · AUSTRALIA</text>
    <path class="land" d="M1037 257L1067 273L1054 340L1073 395L1055 462L1072 533L1058 601L1070 680L1041 667Z"/>
    <text class="land-label" x="1057" y="475" transform="rotate(-90 1057 475)">AFRICA</text>
    <path class="land" d="M1514 256L1538 272L1532 355L1542 414L1525 473L1540 541L1523 605L1536 679L1512 695Z"/>
    <text class="land-label" x="1531" y="480" transform="rotate(90 1531 480)">AMERICAS</text>
  </g>
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
        "--catalog-output",
        type=pathlib.Path,
        default=pathlib.Path(__file__).resolve().parents[1] / "research" / "longhurst-province-reference.csv",
    )
    args = parser.parse_args()
    args.output.write_text(build_svg(), encoding="utf-8", newline="\n")
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
