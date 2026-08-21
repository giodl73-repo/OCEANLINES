import hashlib
import importlib.util
import json
import pathlib
import tempfile
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

    def test_error_metadata_declares_uncertainty_boundary(self):
        raw = b"".join(
            f"2026-08-01T12:00:00Z,0.0,{lat},{lon},0.25\n".encode()
            for lat in range(40)
            for lon in range(40)
        )
        payload = MODULE.package(raw, "2026-08-01", 8, "2026-08-21T00:00:00Z", "err")
        self.assertEqual("err", payload["variable_id"])
        self.assertIsNone(payload["baseline"])
        self.assertIn("not forecast error", payload["boundary"])

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

    def test_netcdf_fixture_preserves_dimensions_order_and_mask(self):
        try:
            import netCDF4
            import numpy
        except ImportError:
            self.skipTest("optional netCDF4 fixture dependencies are not installed")
        with tempfile.TemporaryDirectory() as directory:
            fixture = pathlib.Path(directory) / "fixture.nc"
            with netCDF4.Dataset(fixture, "w", format="NETCDF3_CLASSIC") as dataset:
                dataset.createDimension("time", 1)
                dataset.createDimension("zlev", 1)
                dataset.createDimension("lat", 2)
                dataset.createDimension("lon", 3)
                dataset.createVariable("lat", "f4", ("lat",))[:] = [-1.0, 1.0]
                dataset.createVariable("lon", "f4", ("lon",))[:] = [0.0, 2.0, 4.0]
                field = dataset.createVariable("err", "f4", ("time", "zlev", "lat", "lon"), fill_value=-999.0)
                field[:] = numpy.ma.array(
                    [[[[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]]],
                    mask=[[[[False, True, False], [False, False, False]]]],
                )
            raw = fixture.read_bytes()
        values, latitudes, longitudes = MODULE.parse_netcdf(raw, "err")
        self.assertEqual([10, None, 30, 40, 50, 60], values)
        self.assertEqual([-1.0, -1.0, -1.0, 1.0, 1.0, 1.0], latitudes)
        self.assertEqual([0.0, 2.0, 4.0, 0.0, 2.0, 4.0], longitudes)

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
        self.assertEqual("oceanlines.oisst.snapshot.v2", payload["schema"])
        self.assertEqual("sst", payload["variable_id"])
        self.assertIsNone(payload["baseline"])
        self.assertEqual("netcdf3", payload["source_format"])
        self.assertIn("summary", payload)
        self.assertRegex(payload["source_sha256"], r"^[0-9a-f]{64}$")

    def test_committed_anomaly_has_baseline_and_distinct_global(self):
        artifact = MODULE_PATH.parents[1] / "atlas" / "data" / "oisst-anomaly-2026-08-01.js"
        lines = artifact.read_text(encoding="utf-8").splitlines()
        payload = json.loads(lines[1].removeprefix("window.OCEANLINES_OISST_ANOMALY=").removesuffix(";"))
        self.assertEqual("anom", payload["variable_id"])
        self.assertEqual("oceanlines.oisst.snapshot.v2", payload["schema"])
        self.assertEqual("1971-2000 climatological mean", payload["baseline"])
        self.assertEqual([90, 180], payload["shape"])
        self.assertRegex(payload["source_sha256"], r"^[0-9a-f]{64}$")

    def test_committed_error_matches_observed_grid(self):
        artifact = MODULE_PATH.parents[1] / "atlas" / "data" / "oisst-error-2026-08-01.js"
        lines = artifact.read_text(encoding="utf-8").splitlines()
        payload = json.loads(lines[1].removeprefix("window.OCEANLINES_OISST_ERROR=").removesuffix(";"))
        self.assertEqual("err", payload["variable_id"])
        self.assertEqual("oceanlines.oisst.snapshot.v2", payload["schema"])
        self.assertEqual([90, 180], payload["shape"])
        self.assertGreaterEqual(payload["summary"]["minimum_c"], 0)
        self.assertRegex(payload["source_sha256"], r"^[0-9a-f]{64}$")

    def test_probe_coordinate_uses_three_colocated_fields(self):
        root = MODULE_PATH.parents[1] / "atlas" / "data"
        specifications = (
            ("oisst-2026-08-01.js", "window.OCEANLINES_OISST=", -132),
            ("oisst-anomaly-2026-08-01.js", "window.OCEANLINES_OISST_ANOMALY=", -21),
            ("oisst-error-2026-08-01.js", "window.OCEANLINES_OISST_ERROR=", 31),
        )
        payloads = []
        for filename, prefix, expected in specifications:
            line = (root / filename).read_text(encoding="utf-8").splitlines()[1]
            payload = json.loads(line.removeprefix(prefix).removesuffix(";"))
            payloads.append(payload)
            row = round((-63.875 - payload["latitude"]["start"]) / payload["latitude"]["step"])
            longitude_360 = (-59.875 + 360) % 360
            column = round((longitude_360 - payload["longitude"]["start"]) / payload["longitude"]["step"])
            self.assertEqual(expected, payload["values_c_hundredths"][row * payload["shape"][1] + column])
        self.assertEqual(1, len({tuple(payload["shape"]) for payload in payloads}))
        self.assertEqual(1, len({json.dumps(payload["latitude"], sort_keys=True) for payload in payloads}))
        self.assertEqual(1, len({json.dumps(payload["longitude"], sort_keys=True) for payload in payloads}))


if __name__ == "__main__":
    unittest.main()
