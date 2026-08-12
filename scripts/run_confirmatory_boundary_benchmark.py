from __future__ import annotations

import argparse
import os
import platform
import sys
from datetime import UTC, datetime
from pathlib import Path

from turkiye_disaster_twin.data.osm import load_drive_graph
from turkiye_disaster_twin.research.boundary import (
    boundary_estimates,
    monotonicity_audit,
    service_probability_curve,
    world_service_thresholds,
)
from turkiye_disaster_twin.research.phase_artifacts import (
    write_phase_transition_bundle,
)
from turkiye_disaster_twin.simulation.phase_transition import (
    marginal_resource_gains,
    paired_grid_inference,
    phase_surface_summary,
    resource_frontier,
    run_phase_transition_experiment,
)
from turkiye_disaster_twin.visualization import graph_center


def _parse_float_list(value: str) -> list[float]:
    values = [float(item.strip()) for item in value.split(",") if item.strip()]
    if len(values) < 2:
        raise argparse.ArgumentTypeError("At least two severity values are required.")
    return values


def _parse_int_list(value: str) -> list[int]:
    values = [int(item.strip()) for item in value.split(",") if item.strip()]
    if not values or any(item < 1 for item in values):
        raise argparse.ArgumentTypeError("Responder counts must be positive integers.")
    return values


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a high-resolution confirmatory reliability-boundary study."
    )
    parser.add_argument("--place", default="Beykoz, İstanbul, Türkiye")
    parser.add_argument(
        "--severities",
        type=_parse_float_list,
        default="0.130,0.135,0.140,0.145,0.150,0.1525,0.155,0.1575,0.160,0.1625,0.165",
    )
    parser.add_argument(
        "--responders",
        type=_parse_int_list,
        default="12,14,16,20,24,32",
    )
    parser.add_argument("--realizations", type=int, default=300)
    parser.add_argument("--incidents", type=int, default=10)
    parser.add_argument("--base-seed", type=int, default=7070)
    parser.add_argument("--target-reachability", type=float, default=80.0)
    parser.add_argument("--reliability-target", type=float, default=80.0)
    parser.add_argument("--bootstrap-resamples", type=int, default=5000)
    parser.add_argument("--permutation-samples", type=int, default=5000)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("artifacts/confirmatory-boundary"),
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()

    graph = load_drive_graph(args.place)
    epicenter_lat, epicenter_lon = graph_center(graph)

    raw = run_phase_transition_experiment(
        graph,
        epicenter_lat=epicenter_lat,
        epicenter_lon=epicenter_lon,
        severities=args.severities,
        responder_counts=args.responders,
        realizations=args.realizations,
        incident_count=args.incidents,
        base_seed=args.base_seed,
    )

    surface = phase_surface_summary(
        raw,
        collapse_threshold_pct=20.0,
        target_reachability_pct=args.target_reachability,
    )
    frontier = resource_frontier(
        raw,
        target_reachability_pct=args.target_reachability,
        reliability_target_pct=args.reliability_target,
    )
    marginal = marginal_resource_gains(surface)
    inference = paired_grid_inference(
        raw,
        bootstrap_resamples=3000,
        permutation_samples=args.permutation_samples,
        seed=args.base_seed,
    )

    probability_curve = service_probability_curve(
        raw,
        target_reachability_pct=args.target_reachability,
    )
    boundaries = boundary_estimates(
        raw,
        target_reachability_pct=args.target_reachability,
        reliability_target_pct=args.reliability_target,
        bootstrap_resamples=args.bootstrap_resamples,
        seed=args.base_seed,
    )
    thresholds = world_service_thresholds(
        raw,
        target_reachability_pct=args.target_reachability,
    )
    audit = monotonicity_audit(raw)

    metadata = {
        "project": "Türkiye Disaster Intelligence Digital Twin",
        "author": "Faramarz Kowsari",
        "schema_version": "confirmatory-boundary-v0.7",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "python_version": sys.version.split()[0],
        "platform": platform.platform(),
        "place": args.place,
        "severities": args.severities,
        "responder_counts": args.responders,
        "realizations_per_grid_cell": args.realizations,
        "incident_count": args.incidents,
        "base_seed": args.base_seed,
        "target_reachability_pct": args.target_reachability,
        "reliability_target_pct": args.reliability_target,
        "boundary_bootstrap_resamples": args.bootstrap_resamples,
        "permutation_samples": args.permutation_samples,
        "nested_responder_pool": True,
        "common_random_numbers_across_resource_levels": True,
        "common_random_numbers_across_severity_levels": True,
        "monotone_failure_coupling_across_severity": True,
        "boundary_curve_constraint": "weighted_pava_nonincreasing",
        "boundary_interpolation": "linear_between_adjacent_tested_severities",
        "boundary_bootstrap_unit": "stochastic_world_seed",
        "damage_model_claim": False,
        "scenario_type": "confirmatory_controlled_stochastic_stress_test",
        "git_sha": os.getenv("GITHUB_SHA"),
        "workflow_run_id": os.getenv("GITHUB_RUN_ID"),
        "workflow_run_attempt": os.getenv("GITHUB_RUN_ATTEMPT"),
    }

    outputs = write_phase_transition_bundle(
        args.output,
        raw=raw,
        surface=surface,
        frontier=frontier,
        marginal_gains=marginal,
        paired_inference=inference,
        metadata=metadata,
        extra_tables={
            "service_probability_curve": probability_curve,
            "boundary_estimates": boundaries,
            "world_service_thresholds": thresholds,
            "monotonicity_audit": audit,
        },
    )

    print(f"Wrote confirmatory boundary bundle to {args.output.resolve()}")
    for name, path in sorted(outputs.items()):
        print(f"{name}: {path}")


if __name__ == "__main__":
    main()
