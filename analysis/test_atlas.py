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
        for token in ('aria-live="polite"', 'aria-label="Atlas lens"', "ATLAS 04 · COORDINATE PROBE", "not a live analysis"):
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

    def test_local_links_resolve(self):
        source = HTML.read_text(encoding="utf-8")
        for target in re.findall(r'(?:href|src)="(\.\.?/[^"#]+)"', source):
            self.assertTrue((HTML.parent / target).resolve().exists(), target)

if __name__ == "__main__":
    unittest.main()
