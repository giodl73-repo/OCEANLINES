import math
import unittest

from heat_zone_ledger import (
    DEFAULT_ICE_DENSITY_KG_M3,
    DEFAULT_ICE_LATENT_HEAT_J_KG,
    DEFAULT_SEAWATER_DENSITY_KG_M3,
    DEFAULT_SEAWATER_HEAT_CAPACITY_J_KG_K,
    SECONDS_PER_DAY,
    from_heat_transport,
    from_water_volume,
)


class HeatZoneLedgerTests(unittest.TestCase):
    def test_one_cubic_kilometer_one_degree(self):
        result = from_water_volume(1.0, 1.0)
        expected_energy = (
            1.0e9
            * DEFAULT_SEAWATER_DENSITY_KG_M3
            * DEFAULT_SEAWATER_HEAT_CAPACITY_J_KG_K
        )
        expected_melt_kg = expected_energy / DEFAULT_ICE_LATENT_HEAT_J_KG
        self.assertEqual(result.input_mode, "water_volume_temperature_excess")
        self.assertTrue(math.isclose(result.gross_energy_j, expected_energy))
        self.assertTrue(math.isclose(result.ideal_latent_melt_kg, expected_melt_kg))
        self.assertTrue(
            math.isclose(
                result.ideal_latent_melt_km3_ice,
                expected_melt_kg / DEFAULT_ICE_DENSITY_KG_M3 / 1.0e9,
            )
        )

    def test_one_terawatt_one_day(self):
        result = from_heat_transport(1.0, 1.0)
        self.assertEqual(result.input_mode, "heat_transport_duration")
        self.assertEqual(result.gross_energy_j, 1.0e12 * SECONDS_PER_DAY)

    def test_efficiency_scales_delivered_not_gross_energy(self):
        full = from_heat_transport(2.0, 10.0)
        quarter = from_heat_transport(2.0, 10.0, transfer_efficiency=0.25)
        self.assertEqual(full.gross_energy_j, quarter.gross_energy_j)
        self.assertTrue(
            math.isclose(quarter.delivered_energy_j, 0.25 * full.delivered_energy_j)
        )
        self.assertTrue(
            math.isclose(
                quarter.ideal_latent_melt_kg, 0.25 * full.ideal_latent_melt_kg
            )
        )

    def test_zero_input_is_valid(self):
        result = from_water_volume(0.0, 3.0)
        self.assertEqual(result.delivered_energy_j, 0.0)
        self.assertEqual(result.ideal_latent_melt_kg, 0.0)

    def test_invalid_inputs_fail_closed(self):
        with self.assertRaises(ValueError):
            from_water_volume(-1.0, 1.0)
        with self.assertRaises(ValueError):
            from_heat_transport(1.0, -1.0)
        with self.assertRaises(ValueError):
            from_heat_transport(1.0, 1.0, transfer_efficiency=1.01)
        with self.assertRaises(ValueError):
            from_water_volume(1.0, float("nan"))


if __name__ == "__main__":
    unittest.main()
