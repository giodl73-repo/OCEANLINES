import csv
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
APP = ROOT / "atlas" / "app.js"
HTML = ROOT / "atlas" / "index.html"
CSS = ROOT / "atlas" / "styles.css"
RESEARCH_HTML = ROOT / "research" / "index.html"
REFERENCES = ROOT / "REFERENCES.bib"

class AtlasTests(unittest.TestCase):
    def test_public_surface_files_exist(self):
        for path in (APP, HTML, CSS, RESEARCH_HTML, REFERENCES, ROOT / "REVIEW-GUIDE.md", ROOT / "PREVIEW-STATUS.md", ROOT / "research" / "styles.css", ROOT / "research" / "zone-catalog.csv", ROOT / "research" / "claims-ledger.csv", ROOT / "atlas" / "README.md", ROOT / "figures" / "oceanlines-fluid-geography.svg", ROOT / "figures" / "oceanlines-fluid-geography-interactive.svg", ROOT / "atlas" / "data" / "oisst-2026-08-01.js", ROOT / "atlas" / "data" / "oisst-anomaly-2026-08-01.js", ROOT / "atlas" / "data" / "oisst-error-2026-08-01.js"):
            self.assertTrue(path.is_file(), path)

    def test_zone_catalog_has_unique_numbered_records(self):
        source = APP.read_text(encoding="utf-8")
        ids = re.findall(r'id: "([a-z0-9-]+)"', source)
        numbers = [int(value) for value in re.findall(r'\bn: (\d+),', source)]
        self.assertEqual(12, len(ids))
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(list(range(1, 13)), numbers)

    def test_zone_records_declare_measurement_boundaries(self):
        source = APP.read_text(encoding="utf-8")
        for field in ("boundary", "depth", "evidence", "source"):
            self.assertEqual(12, len(re.findall(rf'\b{field}: "', source)), field)

    def test_html_has_accessibility_and_status_cues(self):
        source = HTML.read_text(encoding="utf-8")
        for token in ('aria-live="polite"', 'aria-label="Atlas lens"', "ATLAS 08 · REVIEW PREVIEW", "not a live analysis"):
            self.assertIn(token, source)

    def test_readme_and_atlas_expose_clear_entry_routes(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        html = HTML.read_text(encoding="utf-8")
        for token in ("## Enter OCEANLINES", "Explore the interactive Atlas 08 preview", "Open the full annotated map", "Read the field guide", "Open the research note", "Check every source"):
            self.assertIn(token, readme)
        for target in ("../figures/oceanlines-fluid-geography.svg", "../HEATMASS.md", "../research/", "README.md", "../SOURCE-REGISTER.md"):
            self.assertIn(f'href="{target}"', html)

    def test_research_note_separates_claims_and_records_data_receipts(self):
        source = RESEARCH_HTML.read_text(encoding="utf-8")
        for token in ("What can be concluded now?", "Does not establish", "What exact bytes are displayed?", "Which papers carry the argument?", "England et al. (2017)", "Goldner, Herold &amp; Huber (2014)", "10.25921/RE9P-PT57", "54fde8766119da6856fff827b64946626eae3f61959792f962f296efb5baacd3", "a6756b88ecfe5e3c0307b7566ba142e3f9ddb8ebaa8823a5d08f9d3a3a1529e2", "24ae585b4b591b19d7b360fe8df3f9620e28f9754e8aa3e21bcb0860bc864ba6", "does not replace external scientific peer review"):
            self.assertIn(token, source)
        for target in re.findall(r'(?:href|src)="(\.\.?/[^"#]+)"', source):
            self.assertTrue((RESEARCH_HTML.parent / target).resolve().exists(), target)

    def test_corrected_primary_source_attributions_are_preserved(self):
        source_register = (ROOT / "SOURCE-REGISTER.md").read_text(encoding="utf-8")
        for token in ("England et al. 2017", "Hodel et al. 2021", "Rosevear et al. 2025"):
            self.assertIn(token, source_register)
        for stale in ("Hutchinson et al. 2017", "Touzeau et al. 2021", "Jenkins 2025"):
            self.assertNotIn(stale, source_register)

    def test_bibliography_and_optional_review_handoff_are_complete(self):
        bibliography = REFERENCES.read_text(encoding="utf-8")
        review = (ROOT / "REVIEW-GUIDE.md").read_text(encoding="utf-8")
        entries = re.findall(r"^@article\{([^,]+),", bibliography, re.MULTILINE)
        dois = re.findall(r"^  doi\s+= \{([^}]+)\}", bibliography, re.MULTILINE)
        self.assertEqual(15, len(entries))
        self.assertEqual(15, len(set(entries)))
        self.assertEqual(15, len(dois))
        self.assertEqual(15, len(set(value.lower() for value in dois)))
        self.assertIn('href="../REFERENCES.bib" download', RESEARCH_HTML.read_text(encoding="utf-8"))
        for token in ("no expectation of endorsement", "not requesting public association", "Any one of these is enough"):
            self.assertIn(token, review)

    def test_machine_readable_research_exports_match_the_atlas_contract(self):
        with (ROOT / "research" / "zone-catalog.csv").open(encoding="utf-8", newline="") as source:
            zones = list(csv.DictReader(source))
        with (ROOT / "research" / "claims-ledger.csv").open(encoding="utf-8", newline="") as source:
            claims = list(csv.DictReader(source))
        app = APP.read_text(encoding="utf-8")
        app_pairs = re.findall(r'id: "([a-z0-9-]+)", n: \d+, name: "([^"]+)"', app)
        self.assertEqual(app_pairs, [(zone["id"], zone["name"]) for zone in zones])
        self.assertEqual([str(value) for value in range(1, 13)], [zone["number"] for zone in zones])
        self.assertTrue(all(zone["inferential_boundary"] and zone["primary_or_register_source"] for zone in zones))
        self.assertTrue(all("·" not in zone["evidence_class"] for zone in zones))
        self.assertEqual("O18", zones[0]["source_ids"])
        self.assertEqual(["C1", "C2", "C3", "C4"], [claim["claim_id"] for claim in claims])
        self.assertTrue(all(claim["does_not_establish"] and claim["references"] for claim in claims))
        self.assertIn("gateway-only causation", claims[-1]["does_not_establish"])

    def test_preview_status_distinguishes_private_branch_from_public_release(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        status = (ROOT / "PREVIEW-STATUS.md").read_text(encoding="utf-8")
        checklist = (ROOT / "PUBLICATION-CHECKLIST.md").read_text(encoding="utf-8")
        self.assertIn("released Atlas 07", readme)
        self.assertIn("private Atlas 08", readme)
        self.assertIn("APPROVED FOR PRIVATE PREVIEW", readme)
        for token in ("has not replaced the released Atlas 07", "has not been pushed from this branch", "Still not present", "Decisions deliberately still open"):
            self.assertIn(token, status)
        self.assertIn("- [ ] Obtain owner visual approval", checklist)
        self.assertIn("- [ ] Decide whether to promote", checklist)

    def test_preview_has_progressive_disclosure_and_mobile_zone_directory(self):
        html = HTML.read_text(encoding="utf-8")
        app = APP.read_text(encoding="utf-8")
        css = CSS.read_text(encoding="utf-8")
        for token in ('id="map-insight"', 'class="ring-workbench"', 'class="advanced-diagnostics"', "Inspect the paired rings", "Open polar mirrors and the latitude continuity ladder", 'id="zone-directory-list"', "Open the full-size map"):
            self.assertIn(token, html)
        for token in ('document.querySelector("#zone-directory-list").append(item)', "scrollIntoView"):
            self.assertIn(token, app)
        self.assertIn("OCEANLINES Atlas 08 Preview", html)
        self.assertIn(".lens[data-lens=\"all\"]", app)
        self.assertIn(".atlas-shell.observed-mode .zone-panel", css)

    def test_observed_map_has_reference_labels_and_three_tick_legend(self):
        html = HTML.read_text(encoding="utf-8")
        app = APP.read_text(encoding="utf-8")
        for token in ('id="map-reference-labels"', "PACIFIC", "ATLANTIC", "INDIAN", "EQUATOR", 'id="scale-mid"'):
            self.assertIn(token, html)
        for token in ('"0°C baseline"', '"0.35°C"', '"15°C"'):
            self.assertIn(token, app)

    def test_preview_replaces_false_precision_claim_and_separates_nearby_markers(self):
        html = HTML.read_text(encoding="utf-8")
        app = APP.read_text(encoding="utf-8")
        self.assertNotIn("false precision", html.lower())
        self.assertIn("Limits</strong> stated beside every view", html)
        self.assertIn("geometry comparison, not physical equivalence", html)
        self.assertIn('id: "indonesian-throughflow"', app)
        self.assertIn("x: 80.5, y: 46.2", app)

    def test_observed_map_declares_projection_and_text_equivalent(self):
        html = HTML.read_text(encoding="utf-8")
        app = APP.read_text(encoding="utf-8")
        for token in ("Equirectangular display", "antimeridian", "Non-color map summary", 'aria-describedby="map-a11y-summary projection-note"'):
            self.assertIn(token, html)
        for token in ("renderTextSummary", "warmer", "cooler", "latitudeBands"):
            self.assertIn(token, app)

    def test_conceptual_boundaries_are_explicitly_permeable(self):
        html = HTML.read_text(encoding="utf-8")
        figure = (ROOT / "figures" / "oceanlines-fluid-geography.svg").read_text(encoding="utf-8")
        self.assertIn("Schematic, permeable, moving regions", html)
        self.assertIn("schematic, permeable, and moving rather than measured boundaries", figure)

    def test_conceptual_map_uses_pinned_natural_earth_geometry(self):
        html = HTML.read_text(encoding="utf-8")
        figure = (ROOT / "figures" / "oceanlines-fluid-geography.svg").read_text(encoding="utf-8")
        interactive_figure = (ROOT / "figures" / "oceanlines-fluid-geography-interactive.svg").read_text(encoding="utf-8")
        builder = (ROOT / "analysis" / "build_fluid_geography.py").read_text(encoding="utf-8")
        self.assertIn("oceanlines-fluid-geography-interactive.svg", html)
        self.assertIn("ca96624a56bd078437bca8184e78163e5039ad19", figure)
        self.assertIn("9e0729ee253ca7d7a5c4ae9395fb1902264c5377c52e224d13dd85010e2835d9", builder)
        self.assertEqual(12, figure.count('class="callout"'))
        self.assertEqual(0, interactive_figure.count('class="callout"'))

    def test_observed_layer_is_explicitly_surface_only(self):
        html = HTML.read_text(encoding="utf-8")
        data = (ROOT / "atlas" / "data" / "oisst-2026-08-01.js").read_text(encoding="utf-8")
        self.assertIn("Observed SST", html)
        self.assertIn("OBSERVATIONAL · SURFACE", html)
        self.assertIn("not full-depth heat content", data)

    def test_anomaly_mode_declares_reference_period(self):
        html = HTML.read_text(encoding="utf-8")
        app = APP.read_text(encoding="utf-8")
        self.assertIn('data-mode="anomaly"', html)
        self.assertIn("1971–2000", app)

    def test_error_mode_is_time_matched_and_bounded(self):
        html = HTML.read_text(encoding="utf-8")
        app = APP.read_text(encoding="utf-8")
        self.assertIn('data-mode="error"', html)
        self.assertIn("TIME-MATCHED ERROR", app)
        self.assertIn("not forecast error", (ROOT / "atlas" / "data" / "oisst-error-2026-08-01.js").read_text(encoding="utf-8"))

    def test_oceanbelts_is_labeled_as_reading_lens(self):
        source = HTML.read_text(encoding="utf-8")
        self.assertIn("HEATMASS <small>reservoirs + anomalies</small>", source)
        self.assertIn("OCEANREALMS <small>currents + gates</small>", source)
        self.assertIn("OCEANBELTS <small>planetary reading lens</small>", source)

    def test_coordinate_probe_has_pointer_keyboard_and_text_paths(self):
        html = HTML.read_text(encoding="utf-8")
        app = APP.read_text(encoding="utf-8")
        for token in ('id="coordinate-probe"', 'id="probe-lat"', 'id="probe-lon"', 'id="probe-result"', 'aria-live="polite"'):
            self.assertIn(token, html)
        for token in ("probeCellFromCoordinates", "inspectCoordinates", 'addEventListener("click"', 'addEventListener("submit"', "Nearest 2° display cell"):
            self.assertIn(token, app)

    def test_coordinate_probe_is_bookmarkable_and_reports_all_fields(self):
        source = APP.read_text(encoding="utf-8")
        for token in ('searchParams.set("mode"', 'searchParams.set("lat"', 'searchParams.set("lon"', 'searchParams.delete("mode"', "OCEANLINES_OISST_ANOMALY", "OCEANLINES_OISST_ERROR", "not heat content or transport"):
            self.assertIn(token, source)

    def test_polar_rings_have_visual_text_and_keyboard_paths(self):
        html = HTML.read_text(encoding="utf-8")
        app = APP.read_text(encoding="utf-8")
        for token in ('id="ring-form"', 'id="ring-lat"', 'id="north-ring"', 'id="south-ring"', 'id="ring-summary"', 'id="ring-body"'):
            self.assertIn(token, html)
        for token in ("pairedRingRows", "longestCyclicRun", "ringStatistics", "geometryData = window.OCEANLINES_OISST", "renderRingComparison", 'searchParams.set("ring"', "not a current, barrier strength, heat-content, or transport measurement"):
            self.assertIn(token, app)

    def test_polar_ring_claim_is_geometry_not_transport(self):
        html = HTML.read_text(encoding="utf-8")
        for token in ("Land-or-missing gaps expose analyzed-water continuity", "do not measure currents or heat transport", "Analyzed-water coverage", "Longest arc"):
            self.assertIn(token, html)

    def test_latitude_ladder_has_chart_and_complete_text_table(self):
        html = HTML.read_text(encoding="utf-8")
        app = APP.read_text(encoding="utf-8")
        for token in ('id="continuity-chart"', 'id="continuity-summary"', 'id="continuity-method"', 'id="continuity-body"', "Open the complete 45-pair scan"):
            self.assertIn(token, html)
        for token in ("latitudeLadder", "renderLatitudeLadder", "magnitude <= 88", "coverage >= 95", "longestDegrees >= 300", "Product-mask topology only; not a circulation boundary"):
            self.assertIn(token, app)

    def test_latitude_ladder_uses_redundant_line_patterns(self):
        html = HTML.read_text(encoding="utf-8")
        css = CSS.read_text(encoding="utf-8")
        self.assertIn("Northern rows · solid", html)
        self.assertIn("Southern rows · dashed", html)
        self.assertIn("border-top-style: dashed", css)

    def test_polar_mirrors_declare_projection_and_orientation(self):
        html = HTML.read_text(encoding="utf-8")
        app = APP.read_text(encoding="utf-8")
        for token in ('id="north-polar"', 'id="south-polar"', 'id="polar-method"', 'id="polar-summary"', "radial azimuthal-equidistant", "intentionally mirrors the southern cap"):
            self.assertIn(token, html)
        for token in ("renderPolarMirror", "renderPolarMirrors", "const capLatitude = 40", "Math.atan2(dx, -dy)", 'hemisphere === "north"', "intentional comparison mirror"):
            self.assertIn(token, app)

    def test_polar_mirrors_have_text_and_non_color_selected_ring(self):
        html = HTML.read_text(encoding="utf-8")
        app = APP.read_text(encoding="utf-8")
        self.assertIn("Beige means land or missing", html)
        self.assertIn("amber circle is the selected ring", html)
        self.assertIn("context.setLineDash([9, 6])", app)
        self.assertIn("not bathymetry, sea ice, circulation, or heat transport", app)

    def test_local_links_resolve(self):
        source = HTML.read_text(encoding="utf-8")
        for target in re.findall(r'(?:href|src)="(\.\.?/[^"#]+)"', source):
            self.assertTrue((HTML.parent / target).resolve().exists(), target)

if __name__ == "__main__":
    unittest.main()
