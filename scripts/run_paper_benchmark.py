from __future__ import annotations

import argparse
import os
from pathlib import Path

from turkiye_disaster_twin.data.osm import load_drive_graph
from turkiye_disaster_twin.research.artifacts import (
    runtime_metadata,
    write_experiment_bundle,
)
from turkiye_disaster_twin.simulation.experiment import (
    run_monte_carlo_experiment,
    summarise_experiment,
)
from turkiye_disaster_twin.simulation.statistics import (
    paper_grade_paired_inference,
)
from turkiye_disaster_twin.visualization import graph_center


def _parse_severities(value: str) -> list[float]:
    severities = [float(item.strip()) for item in value.split(",") if item.strip()]
    if not severities:
        raise argparse.ArgumentTypeError("At least one severity is required.")
    if any(item < 0.0 or item > 1.0 for item in severities):
        raise argparse.ArgumentTypeError("Severities must be between 0 and 1.")
    return severities


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a paper-grade paired Monte Carlo benchmark."
    )
    parser.add_argument("--place", default="Beykoz, İstanbul, Türkiye")
    parser.add_argument("--severities", type=_parse_severities, default="0.10,0.25,0.40")
    parser.add_argument("--realizations", type=int, default=100)
    parser.add_argument("--incidents", type=int, default=10)
    parser.add_argument("--responders", type=int, default=8)
    parser.add_argument("--base-seed", type=int, default=2026)
    parser.add_argument("--bootstrap-resamples", type=int, default=5000)
    parser.add_argument("--permutation-samples", type=int, default=10000)
    parser.add_argument("--output", type=Path, default=Path("artifacts/paper-benchmark"))
    return parser


def main() -> None:
    args = build_parser().parse_args()

    if args.realizations < 1:
        raise ValueError("--realizations must be at least 1")
    if args.incidents < 1 or args.responders < 1:
        raise ValueError("--incidents and --responders must be positive")

    graph = load_drive_graph(args.place)
    epicenter_lat, epicenter_lon = graph_center(graph)

    raw = run_monte_carlo_experiment(
        graph,
        epicenter_lat=epicenter_lat,
        epicenter_lon=epicenter_lon,
        severities=args.severities,
        realizations=args.realizations,
        incident_count=args.incidents,
        responder_count=args.responders,
        base_seed=args.base_seed,
    )
    exploratory = summarise_experiment(raw)
    inference = paper_grade_paired_inference(
        raw,
        bootstrap_resamples=args.bootstrap_resamples,
        permutation_samples=args.permutation_samples,
        seed=args.base_seed,
    )

    metadata = runtime_metadata(
        {
            "project": "Türkiye Disaster Intelligence Digital Twin",
            "author": "Faramarz Kowsari",
            "place": args.place,
            "severities": args.severities,
            "realizations_per_severity": args.realizations,
            "incident_count": args.incidents,
            "responder_count": args.responders,
            "base_seed": args.base_seed,
            "bootstrap_resamples": args.bootstrap_resamples,
            "permutation_samples": args.permutation_samples,
            "git_sha": os.getenv("GITHUB_SHA"),
            "workflow_run_id": os.getenv("GITHUB_RUN_ID"),
            "damage_model_claim": False,
            "scenario_type": "controlled_stochastic_stress_test",
        }
    )

    outputs = write_experiment_bundle(
        args.output,
        raw=raw,
        exploratory_summary=exploratory,
        paired_inference=inference,
        metadata=metadata,
        require_parquet=True,
    )

    print(f"Wrote research bundle to {args.output.resolve()}")
    for name, path in sorted(outputs.items()):
        print(f"{name}: {path}")


if __name__ == "__main__":
    main()
