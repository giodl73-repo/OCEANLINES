#!/usr/bin/env python3
"""Deterministic scale calculator for ocean heat and idealized ice melt.

The calculator supports two distinct inputs:

1. a water volume and temperature excess above a declared reference; or
2. a heat-transport rate sustained for a declared duration.

Its ice-melt equivalent is an energy-unit conversion using latent heat only.
It is an upper-bound scale, not an ice-sheet forecast or a model of delivery,
mixing, sensible heating, circulation feedbacks, or mechanical ice loss.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass


DEFAULT_SEAWATER_DENSITY_KG_M3 = 1027.0
DEFAULT_SEAWATER_HEAT_CAPACITY_J_KG_K = 3990.0
DEFAULT_ICE_LATENT_HEAT_J_KG = 334000.0
DEFAULT_ICE_DENSITY_KG_M3 = 917.0
SECONDS_PER_DAY = 86400.0


@dataclass(frozen=True)
class HeatScale:
    input_mode: str
    gross_energy_j: float
    transfer_efficiency: float
    delivered_energy_j: float
    delivered_energy_pj: float
    ideal_latent_melt_kg: float
    ideal_latent_melt_gt: float
    ideal_latent_melt_km3_ice: float
    constants: dict[str, float]
    interpretation: str


def _finite_nonnegative(name: str, value: float) -> float:
    if not math.isfinite(value) or value < 0:
        raise ValueError(f"{name} must be finite and nonnegative")
    return value


def _validate_constants(
    seawater_density_kg_m3: float,
    seawater_heat_capacity_j_kg_k: float,
    ice_latent_heat_j_kg: float,
    ice_density_kg_m3: float,
) -> None:
    for name, value in (
        ("seawater_density_kg_m3", seawater_density_kg_m3),
        ("seawater_heat_capacity_j_kg_k", seawater_heat_capacity_j_kg_k),
        ("ice_latent_heat_j_kg", ice_latent_heat_j_kg),
        ("ice_density_kg_m3", ice_density_kg_m3),
    ):
        if not math.isfinite(value) or value <= 0:
            raise ValueError(f"{name} must be finite and positive")


def _result(
    *,
    input_mode: str,
    gross_energy_j: float,
    transfer_efficiency: float,
    seawater_density_kg_m3: float,
    seawater_heat_capacity_j_kg_k: float,
    ice_latent_heat_j_kg: float,
    ice_density_kg_m3: float,
) -> HeatScale:
    if not math.isfinite(transfer_efficiency) or not 0 <= transfer_efficiency <= 1:
        raise ValueError("transfer_efficiency must be between 0 and 1")
    _validate_constants(
        seawater_density_kg_m3,
        seawater_heat_capacity_j_kg_k,
        ice_latent_heat_j_kg,
        ice_density_kg_m3,
    )
    delivered = gross_energy_j * transfer_efficiency
    melt_kg = delivered / ice_latent_heat_j_kg
    melt_km3 = melt_kg / ice_density_kg_m3 / 1.0e9
    return HeatScale(
        input_mode=input_mode,
        gross_energy_j=gross_energy_j,
        transfer_efficiency=transfer_efficiency,
        delivered_energy_j=delivered,
        delivered_energy_pj=delivered / 1.0e15,
        ideal_latent_melt_kg=melt_kg,
        ideal_latent_melt_gt=melt_kg / 1.0e12,
        ideal_latent_melt_km3_ice=melt_km3,
        constants={
            "seawater_density_kg_m3": seawater_density_kg_m3,
            "seawater_heat_capacity_j_kg_k": seawater_heat_capacity_j_kg_k,
            "ice_latent_heat_j_kg": ice_latent_heat_j_kg,
            "ice_density_kg_m3": ice_density_kg_m3,
        },
        interpretation=(
            "Ideal latent-melt energy equivalent only. This is an upper-bound "
            "unit conversion, not a prediction of delivered ocean heat or ice loss."
        ),
    )


def from_water_volume(
    volume_km3: float,
    temperature_excess_c: float,
    *,
    transfer_efficiency: float = 1.0,
    seawater_density_kg_m3: float = DEFAULT_SEAWATER_DENSITY_KG_M3,
    seawater_heat_capacity_j_kg_k: float = DEFAULT_SEAWATER_HEAT_CAPACITY_J_KG_K,
    ice_latent_heat_j_kg: float = DEFAULT_ICE_LATENT_HEAT_J_KG,
    ice_density_kg_m3: float = DEFAULT_ICE_DENSITY_KG_M3,
) -> HeatScale:
    """Convert a water-volume temperature anomaly to an energy scale."""
    _finite_nonnegative("volume_km3", volume_km3)
    _finite_nonnegative("temperature_excess_c", temperature_excess_c)
    _validate_constants(
        seawater_density_kg_m3,
        seawater_heat_capacity_j_kg_k,
        ice_latent_heat_j_kg,
        ice_density_kg_m3,
    )
    water_mass_kg = volume_km3 * 1.0e9 * seawater_density_kg_m3
    gross_energy_j = (
        water_mass_kg
        * seawater_heat_capacity_j_kg_k
        * temperature_excess_c
    )
    return _result(
        input_mode="water_volume_temperature_excess",
        gross_energy_j=gross_energy_j,
        transfer_efficiency=transfer_efficiency,
        seawater_density_kg_m3=seawater_density_kg_m3,
        seawater_heat_capacity_j_kg_k=seawater_heat_capacity_j_kg_k,
        ice_latent_heat_j_kg=ice_latent_heat_j_kg,
        ice_density_kg_m3=ice_density_kg_m3,
    )


def from_heat_transport(
    power_tw: float,
    duration_days: float,
    *,
    transfer_efficiency: float = 1.0,
    seawater_density_kg_m3: float = DEFAULT_SEAWATER_DENSITY_KG_M3,
    seawater_heat_capacity_j_kg_k: float = DEFAULT_SEAWATER_HEAT_CAPACITY_J_KG_K,
    ice_latent_heat_j_kg: float = DEFAULT_ICE_LATENT_HEAT_J_KG,
    ice_density_kg_m3: float = DEFAULT_ICE_DENSITY_KG_M3,
) -> HeatScale:
    """Convert sustained heat transport to an integrated energy scale."""
    _finite_nonnegative("power_tw", power_tw)
    _finite_nonnegative("duration_days", duration_days)
    gross_energy_j = power_tw * 1.0e12 * duration_days * SECONDS_PER_DAY
    return _result(
        input_mode="heat_transport_duration",
        gross_energy_j=gross_energy_j,
        transfer_efficiency=transfer_efficiency,
        seawater_density_kg_m3=seawater_density_kg_m3,
        seawater_heat_capacity_j_kg_k=seawater_heat_capacity_j_kg_k,
        ice_latent_heat_j_kg=ice_latent_heat_j_kg,
        ice_density_kg_m3=ice_density_kg_m3,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--volume-km3", type=float)
    mode.add_argument("--power-tw", type=float)
    parser.add_argument("--temperature-excess-c", type=float)
    parser.add_argument("--duration-days", type=float)
    parser.add_argument("--transfer-efficiency", type=float, default=1.0)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.volume_km3 is not None:
        if args.temperature_excess_c is None or args.duration_days is not None:
            raise SystemExit(
                "--volume-km3 requires --temperature-excess-c and forbids --duration-days"
            )
        result = from_water_volume(
            args.volume_km3,
            args.temperature_excess_c,
            transfer_efficiency=args.transfer_efficiency,
        )
    else:
        if args.duration_days is None or args.temperature_excess_c is not None:
            raise SystemExit(
                "--power-tw requires --duration-days and forbids --temperature-excess-c"
            )
        result = from_heat_transport(
            args.power_tw,
            args.duration_days,
            transfer_efficiency=args.transfer_efficiency,
        )
    print(json.dumps(asdict(result), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
