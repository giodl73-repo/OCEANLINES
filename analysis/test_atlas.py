import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
APP = ROOT / "atlas" / "app.js"
HTML = ROOT / "atlas" / "index.html"
CSS = ROOT / "atlas" / "styles.css"

class AtlasTests(unittest.TestCase):
    def test_public_surface_files_exist(self):
        for path in (APP, HTML, CSS, ROOT / "atlas" / "README.md", ROOT / "atlas" / "data" / "oisst-2026-08-01.js", ROOT / "atlas" / "data" / "oisst-anomaly-2026-08-01.js", ROOT / "atlas" / "data" / "oisst-error-2026-08-01.js"):
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
        for token in ('aria-live="polite"', 'aria-label="Atlas lens"', "ATLAS 07 · POLAR MIRRORS", "not a live analysis"):
            self.assertIn(token, source)

    def test_observed_map_declares_projection_and_text_equivalent(self):
        html = HTML.read_text(encoding="utf-8")
        app = APP.read_text(encoding="utf-8")
        for token in ("Equirectangular display", "antimeridian", "Non-color map summary", 'aria-describedby="map-a11y-summary projection-note"'):
            self.assertIn(token, html)
        for token in ("renderTextSummary", "warmer", "cooler", "latitudeBands"):
            self.assertIn(token, app)

    def test_conceptual_boundaries_are_explicitly_permeable(self):
        html = HTML.read_text(encoding="utf-8")
        figure = (ROOT / "figures" / "planetary-heat-geography.svg").read_text(encoding="utf-8")
        self.assertIn("Schematic, permeable, moving regions", html)
        self.assertIn("rather than quantitative or fixed boundaries", figure)

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
        self.assertIn("OCEANBELTS <small>reading lens</small>", HTML.read_text(encoding="utf-8"))

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
