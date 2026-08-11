from __future__ import annotations

from collections.abc import Iterable
from math import sqrt

import networkx as nx
import pandas as pd

from turkiye_disaster_twin.simulation.engine import run_snapshot

ALGORITHMS = ("greedy", "global_min_cost")
SUMMARY_METRICS = (
    "reachability_pct",
    "mean_response_s",
    "median_response_s",
    "p90_response_s",
    "total_response_s",
    "weighted_unmet_demand",
)


def run_monte_carlo_experiment(
    graph: nx.MultiDiGraph,
    *,
    epicenter_lat: float,
    epicenter_lon: float,
    severities: Iterable[float],
    realizations: int,
    incident_count: int,
    responder_count: int,
    base_seed: int = 1000,
    decay_km: float = 8.0,
) -> pd.DataFrame:
    """Run matched Monte Carlo realisations for both dispatch algorithms.

    Each severity/seed pair is evaluated by both algorithms on the exact same
    synthetic disruption, incident demand, and responder placement. This creates
    a paired experimental design instead of comparing unrelated random samples.
    """
    if realizations < 1:
        raise ValueError("realizations must be at least 1")

    severity_values = [float(value) for value in severities]
    if not severity_values:
        raise ValueError("At least one severity value is required.")

    records: list[dict[str, int | float | str | None]] = []

    for severity_index, severity in enumerate(severity_values):
        for realization in range(realizations):
            seed = int(base_seed + severity_index * 1_000_000 + realization)
            result = run_snapshot(
                graph,
                epicenter_lat=epicenter_lat,
                epicenter_lon=epicenter_lon,
                disruption_severity=severity,
                incident_count=incident_count,
                responder_count=responder_count,
                seed=seed,
                decay_km=decay_km,
            )

            for algorithm, metrics in (
                ("greedy", result.greedy_metrics),
                ("global_min_cost", result.global_metrics),
            ):
                record: dict[str, int | float | str | None] = {
                    "severity_control": severity,
                    "realization": realization,
                    "seed": seed,
                    "algorithm": algorithm,
                    "failed_directed_edges": len(result.failed_edges),
                    "incident_count": incident_count,
                    "responder_count": responder_count,
                }
                record.update(metrics.to_dict())
                records.append(record)

    return pd.DataFrame.from_records(records)


def summarise_experiment(frame: pd.DataFrame) -> pd.DataFrame:
    """Summarise means with approximate 95% confidence intervals.

    The interval uses 1.96 × standard error and is intended for exploratory
    sensitivity analysis. Paper-grade inference can later switch to bootstrap or
    model-based intervals without changing the raw experiment table.
    """
    required = {"severity_control", "algorithm", *SUMMARY_METRICS}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"Experiment frame is missing columns: {sorted(missing)}")

    records: list[dict[str, int | float | str | None]] = []

    grouped = frame.groupby(["severity_control", "algorithm"], sort=True)
    for (severity, algorithm), group in grouped:
        for metric in SUMMARY_METRICS:
            values = pd.to_numeric(group[metric], errors="coerce").dropna()
            n = int(values.size)
            if n == 0:
                continue

            mean_value = float(values.mean())
            std_value = 0.0 if n < 2 else float(values.std(ddof=1))
            half_width = 0.0 if n < 2 else 1.96 * std_value / sqrt(n)

            records.append(
                {
                    "severity_control": float(severity),
                    "algorithm": str(algorithm),
                    "metric": metric,
                    "n": n,
                    "mean": mean_value,
                    "std": std_value,
                    "ci95_low": mean_value - half_width,
                    "ci95_high": mean_value + half_width,
                }
            )

    return pd.DataFrame.from_records(records)


def paired_algorithm_comparison(
    frame: pd.DataFrame,
    *,
    metric: str = "total_response_s",
) -> pd.DataFrame:
    """Compare greedy and global assignment on matched severity/seed pairs.

    Positive ``greedy_minus_global`` means the global method achieved a lower
    value for the selected metric. The interpretation is valid for cost-like
    metrics such as response time or weighted unmet demand.
    """
    required = {"severity_control", "seed", "algorithm", metric}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"Experiment frame is missing columns: {sorted(missing)}")

    pivot = frame.pivot_table(
        index=["severity_control", "seed"],
        columns="algorithm",
        values=metric,
        aggfunc="first",
    ).reset_index()

    if not set(ALGORITHMS).issubset(pivot.columns):
        return pd.DataFrame(
            columns=[
                "severity_control",
                "n_pairs",
                "mean_greedy_minus_global",
                "ci95_low",
                "ci95_high",
                "global_win_rate_pct",
            ]
        )

    pivot["greedy_minus_global"] = pivot["greedy"] - pivot["global_min_cost"]
    records: list[dict[str, int | float]] = []

    for severity, group in pivot.groupby("severity_control", sort=True):
        deltas = pd.to_numeric(group["greedy_minus_global"], errors="coerce").dropna()
        n = int(deltas.size)
        if n == 0:
            continue

        mean_delta = float(deltas.mean())
        std_delta = 0.0 if n < 2 else float(deltas.std(ddof=1))
        half_width = 0.0 if n < 2 else 1.96 * std_delta / sqrt(n)
        win_rate = float((deltas > 0).mean() * 100.0)

        records.append(
            {
                "severity_control": float(severity),
                "n_pairs": n,
                "mean_greedy_minus_global": mean_delta,
                "ci95_low": mean_delta - half_width,
                "ci95_high": mean_delta + half_width,
                "global_win_rate_pct": win_rate,
            }
        )

    return pd.DataFrame.from_records(records)
