import hashlib
import importlib.util
import json
import pathlib
import unittest


MODULE_PATH = pathlib.Path(__file__).with_name("fetch_oisst_snapshot.py")
SPEC = importlib.util.spec_from_file_location("fetch_oisst_snapshot", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


class OisstSnapshotTests(unittest.TestCase):
    def test_query_uses_fixed_final_collection_and_surface(self):
        url = MODULE.build_query("2026-08-01", 8)
        self.assertIn(MODULE.DATASET_ID, url)
        self.assertIn("sst", url)
        self.assertIn("2026-08-01T12:00:00Z", url)
        self.assertIn(":8:", url)
        self.assertIn("%5B", url)
        self.assertNotIn("[", url)

    def test_anomaly_query_and_metadata_declare_baseline(self):
        url = MODULE.build_query("2026-08-01", 8, "anom")
        self.assertIn("?anom%5B", url)
        raw = b"".join(
            f"2026-08-01T12:00:00Z,0.0,{lat},{lon},1.25\n".encode()
            for lat in range(40)
            for lon in range(40)
        )
        payload = MODULE.package(raw, "2026-08-01", 8, "2026-08-21T00:00:00Z", "anom")
        self.assertEqual("1971-2000 climatological mean", payload["baseline"])
        self.assertIn("not absolute temperature", payload["boundary"])

    def test_ncss_query_targets_same_final_daily_file(self):
        url = MODULE.build_ncss_query("2026-08-01", 8, "anom")
        self.assertIn("202608/oisst-avhrr-v02r01.20260801.nc", url)
        self.assertIn("var=anom", url)
        self.assertIn("horizStride=8", url)
        self.assertIn("accept=netcdf3", url)

    def test_parse_quantizes_and_preserves_missing(self):
        raw = (
            b"2026-08-01T12:00:00Z,0.0,-1.0,0.0,20.125\n"
            b"2026-08-01T12:00:00Z,0.0,-1.0,2.0,NaN\n"
            b"2026-08-01T12:00:00Z,0.0,1.0,0.0,-1.8\n"
            b"2026-08-01T12:00:00Z,0.0,1.0,2.0,3.0\n"
        )
        values, latitudes, longitudes = MODULE.parse_rows(raw)
        self.assertEqual([2012, None, -180, 300], values)
        self.assertEqual([-1.0, -1.0, 1.0, 1.0], latitudes)
        self.assertEqual([0.0, 2.0, 0.0, 2.0], longitudes)

    def test_package_records_shape_hash_and_boundary(self):
        raw = b"".join(
            f"2026-08-01T12:00:00Z,0.0,{lat},{lon},20.0\n".encode()
            for lat in range(40)
            for lon in range(40)
        )
        payload = MODULE.package(raw, "2026-08-01", 8, "2026-08-21T00:00:00Z")
        self.assertEqual([40, 40], payload["shape"])
        self.assertEqual(hashlib.sha256(raw).hexdigest(), payload["source_sha256"])
        self.assertEqual(1600, payload["summary"]["valid_ocean_cells"])
        self.assertIn("not full-depth heat content", payload["boundary"])

    def test_committed_snapshot_has_expected_provenance(self):
        artifact = MODULE_PATH.parents[1] / "atlas" / "data" / "oisst-2026-08-01.js"
        lines = artifact.read_text(encoding="utf-8").splitlines()
        payload = json.loads(lines[1].removeprefix("window.OCEANLINES_OISST=").removesuffix(";"))
        self.assertEqual([90, 180], payload["shape"])
        self.assertEqual("2026-08-01", payload["date"])
        self.assertEqual(16200, len(payload["values_c_hundredths"]))
        valid = [value for value in payload["values_c_hundredths"] if value is not None]
        self.assertGreater(len(valid), 10000)
        self.assertGreater(max(valid) / 100, 30)
        self.assertRegex(payload["source_sha256"], r"^[0-9a-f]{64}$")

    def test_committed_anomaly_has_baseline_and_distinct_global(self):
        artifact = MODULE_PATH.parents[1] / "atlas" / "data" / "oisst-anomaly-2026-08-01.js"
        lines = artifact.read_text(encoding="utf-8").splitlines()
        payload = json.loads(lines[1].removeprefix("window.OCEANLINES_OISST_ANOMALY=").removesuffix(";"))
        self.assertEqual("anom", payload["variable_id"])
        self.assertEqual("1971-2000 climatological mean", payload["baseline"])
        self.assertEqual([90, 180], payload["shape"])
        self.assertRegex(payload["source_sha256"], r"^[0-9a-f]{64}$")


if __name__ == "__main__":
    unittest.main()
