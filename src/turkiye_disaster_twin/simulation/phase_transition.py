from __future__ import annotations

from collections.abc import Hashable, Iterable
from statistics import mean

import networkx as nx
import numpy as np
import pandas as pd

from turkiye_disaster_twin.simulation.baselines import Assignment
from turkiye_disaster_twin.simulation.metrics import response_metrics
from turkiye_disaster_twin.simulation.scenario import (
    Incident,
    apply_failed_edges,
    edge_disruption_risks,
    sample_failed_edges,
    sample_snapshot_entities,
)
from turkiye_disaster_twin.simulation.statistics import (
    bootstrap_mean_ci,
    holm_adjust,
    paired_sign_flip_pvalue,
)

ALGORITHMS = ("greedy", "global_min_cost")
COST_METRICS = (
    "mean_response_s",
    "median_response_s",
    "p90_response_s",
    "total_response_s",
    "weighted_unmet_demand",
)


def _normalise_responder_counts(values: Iterable[int]) -> list[int]:
    counts = sorted({int(value) for value in values})
    if not counts or counts[0] < 1:
        raise ValueError("Responder counts must contain positive integers.")
    return counts


def _travel_time_costs(
    graph: nx.MultiDiGraph,
    responders: list[Hashable],
    incidents: list[Hashable],
    *,
    weight: str = "travel_time",
) -> dict[tuple[Hashable, Hashable], float]:
    """Compute all reachable responder-to-incident travel times efficiently.

    Dijkstra is run once per responder, then filtered to the incident set. The
    same matrix can be reused for every nested responder-count condition.
    """
    costs: dict[tuple[Hashable, Hashable], float] = {}
    incident_set = set(incidents)

    for responder in responders:
        try:
            lengths = nx.single_source_dijkstra_path_length(
                graph,
                source=responder,
                weight=weight,
            )
        except nx.NodeNotFound:
            continue

        for incident in incident_set.intersection(lengths):
            costs[(responder, incident)] = float(lengths[incident])

    return costs


def _greedy_from_costs(
    responders: list[Hashable],
    incidents: list[Hashable],
    costs: dict[tuple[Hashable, Hashable], float],
) -> list[Assignment]:
    """Sequential nearest-responder baseline using a precomputed cost matrix."""
    available = list(responders)
    assignments: list[Assignment] = []

    for incident in incidents:
        candidates = [
            (costs[(responder, incident)], index, responder)
            for index, responder in enumerate(available)
            if (responder, incident) in costs
        ]
        if not candidates:
            continue

        cost, _index, responder = min(candidates)
        assignments.append(
            Assignment(
                incident=incident,
                responder=responder,
                travel_time=float(cost),
            )
        )
        available.remove(responder)

        if not available:
            break

    return assignments


def _global_from_costs(
    responders: list[Hashable],
    incidents: list[Hashable],
    costs: dict[tuple[Hashable, Hashable], float],
) -> list[Assignment]:
    """Maximum-cardinality, minimum-cost one-to-one assignment from cached costs."""
    if not responders or not incidents:
        return []

    flow_graph = nx.DiGraph()
    source = ("source",)
    sink = ("sink",)
    responder_nodes = [("responder", index) for index in range(len(responders))]
    incident_nodes = [("incident", index) for index in range(len(incidents))]

    for node in responder_nodes:
        flow_graph.add_edge(source, node, capacity=1, weight=0)
    for node in incident_nodes:
        flow_graph.add_edge(node, sink, capacity=1, weight=0)

    pair_lookup: dict[tuple[int, int], float] = {}
    for responder_index, responder in enumerate(responders):
        for incident_index, incident in enumerate(incidents):
            cost = costs.get((responder, incident))
            if cost is None:
                continue

            pair_lookup[(responder_index, incident_index)] = cost
            flow_graph.add_edge(
                responder_nodes[responder_index],
                incident_nodes[incident_index],
                capacity=1,
                weight=max(0, round(cost * 1000)),
            )

    if not pair_lookup:
        return []

    cardinality = nx.maximum_flow_value(flow_graph, source, sink)
    if cardinality <= 0:
        return []

    for node in flow_graph.nodes:
        flow_graph.nodes[node]["demand"] = 0
    flow_graph.nodes[source]["demand"] = -cardinality
    flow_graph.nodes[sink]["demand"] = cardinality

    flow = nx.min_cost_flow(flow_graph)
    assignments: list[Assignment] = []

    for responder_index, responder_node in enumerate(responder_nodes):
        for incident_index, incident_node in enumerate(incident_nodes):
            if flow.get(responder_node, {}).get(incident_node, 0) <= 0:
                continue
            assignments.append(
                Assignment(
                    incident=incidents[incident_index],
                    responder=responders[responder_index],
                    travel_time=pair_lookup[(responder_index, incident_index)],
                )
            )

    return assignments


def run_phase_transition_experiment(
    graph: nx.MultiDiGraph,
    *,
    epicenter_lat: float,
    epicenter_lon: float,
    severities: Iterable[float],
    responder_counts: Iterable[int],
    realizations: int,
    incident_count: int,
    base_seed: int = 4040,
    decay_km: float = 8.0,
) -> pd.DataFrame:
    """Sweep disruption severity and nested responder availability.

    For each severity/seed pair, road failures and incident locations are sampled
    exactly once. A maximum responder pool is also sampled once; lower-resource
    conditions use deterministic prefixes of that same pool. This common-random-
    numbers design reduces noise when measuring the marginal value of resources.
    """
    if realizations < 1:
        raise ValueError("realizations must be at least 1")
    if incident_count < 1:
        raise ValueError("incident_count must be positive")

    severity_values = [float(value) for value in severities]
    if not severity_values:
        raise ValueError("At least one severity is required.")
    if any(value < 0.0 or value > 1.0 for value in severity_values):
        raise ValueError("Severity values must be between 0 and 1.")

    responder_values = _normalise_responder_counts(responder_counts)
    max_responders = max(responder_values)

    if incident_count + max_responders > graph.number_of_nodes():
        raise ValueError("The graph does not contain enough nodes for the requested entities.")

    records: list[dict[str, int | float | str | None]] = []

    for severity_index, severity in enumerate(severity_values):
        risks = edge_disruption_risks(
            graph,
            epicenter_lat=epicenter_lat,
            epicenter_lon=epicenter_lon,
            severity=severity,
            decay_km=decay_km,
        )

        for realization in range(realizations):
            seed = int(base_seed + severity_index * 1_000_000 + realization)
            failed_edges = sample_failed_edges(risks, seed=seed)
            disrupted = apply_failed_edges(graph, failed_edges)

            incidents, responder_pool = sample_snapshot_entities(
                graph,
                incident_count=incident_count,
                responder_count=max_responders,
                epicenter_lat=epicenter_lat,
                epicenter_lon=epicenter_lon,
                seed=seed + 1,
            )
            incident_nodes = [incident.node for incident in incidents]

            costs = _travel_time_costs(
                disrupted,
                list(responder_pool),
                incident_nodes,
            )

            for responder_count in responder_values:
                responders = list(responder_pool[:responder_count])

                greedy = _greedy_from_costs(
                    responders,
                    incident_nodes,
                    costs,
                )
                global_optimum = _global_from_costs(
                    responders,
                    incident_nodes,
                    costs,
                )

                for algorithm, assignments in (
                    ("greedy", greedy),
                    ("global_min_cost", global_optimum),
                ):
                    metrics = response_metrics(assignments, incidents)
                    record: dict[str, int | float | str | None] = {
                        "severity_control": severity,
                        "responder_count": responder_count,
                        "realization": realization,
                        "seed": seed,
                        "algorithm": algorithm,
                        "failed_directed_edges": len(failed_edges),
                        "incident_count": incident_count,
                    }
                    record.update(metrics.to_dict())
                    records.append(record)

    return pd.DataFrame.from_records(records)


def phase_surface_summary(
    frame: pd.DataFrame,
    *,
    collapse_threshold_pct: float = 20.0,
    target_reachability_pct: float = 80.0,
) -> pd.DataFrame:
    """Summarise service reliability across the severity × responder grid."""
    required = {
        "severity_control",
        "responder_count",
        "algorithm",
        "seed",
        "reachability_pct",
        "weighted_unmet_demand",
        "total_response_s",
        "p90_response_s",
        "assigned",
        "failed_directed_edges",
    }
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"Phase frame is missing columns: {sorted(missing)}")

    records: list[dict[str, int | float | str | None]] = []

    grouped = frame.groupby(
        ["severity_control", "responder_count", "algorithm"],
        sort=True,
    )
    for (severity, responder_count, algorithm), group in grouped:
        reachability = pd.to_numeric(group["reachability_pct"], errors="coerce")
        unmet = pd.to_numeric(group["weighted_unmet_demand"], errors="coerce")
        total = pd.to_numeric(group["total_response_s"], errors="coerce")
        p90 = pd.to_numeric(group["p90_response_s"], errors="coerce")

        records.append(
            {
                "severity_control": float(severity),
                "responder_count": int(responder_count),
                "algorithm": str(algorithm),
                "n_realizations": int(group["seed"].nunique()),
                "mean_reachability_pct": float(reachability.mean()),
                "mean_weighted_unmet_demand": float(unmet.mean()),
                "mean_total_response_s": float(total.mean()),
                "mean_p90_response_s": (
                    None if p90.dropna().empty else float(p90.mean())
                ),
                "collapse_probability_pct": float(
                    (reachability < collapse_threshold_pct).mean() * 100.0
                ),
                "target_service_probability_pct": float(
                    (reachability >= target_reachability_pct).mean() * 100.0
                ),
                "zero_assignment_probability_pct": float(
                    (pd.to_numeric(group["assigned"], errors="coerce") == 0).mean()
                    * 100.0
                ),
                "mean_failed_directed_edges": float(
                    pd.to_numeric(
                        group["failed_directed_edges"],
                        errors="coerce",
                    ).mean()
                ),
            }
        )

    return pd.DataFrame.from_records(records)


def resource_frontier(
    frame: pd.DataFrame,
    *,
    target_reachability_pct: float = 80.0,
    reliability_target_pct: float = 80.0,
) -> pd.DataFrame:
    """Find the minimum responder count meeting a service-reliability target."""
    required = {
        "severity_control",
        "responder_count",
        "algorithm",
        "reachability_pct",
    }
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"Phase frame is missing columns: {sorted(missing)}")

    records: list[dict[str, int | float | str | None]] = []

    grouped = frame.groupby(["severity_control", "algorithm"], sort=True)
    for (severity, algorithm), group in grouped:
        candidates = []
        for responder_count, condition in group.groupby("responder_count", sort=True):
            reachability = pd.to_numeric(
                condition["reachability_pct"],
                errors="coerce",
            ).dropna()
            if reachability.empty:
                continue

            candidates.append(
                {
                    "responder_count": int(responder_count),
                    "mean_reachability_pct": float(reachability.mean()),
                    "target_service_probability_pct": float(
                        (reachability >= target_reachability_pct).mean() * 100.0
                    ),
                }
            )

        qualifying = [
            candidate
            for candidate in candidates
            if candidate["target_service_probability_pct"] >= reliability_target_pct
        ]
        selected = min(
            qualifying,
            key=lambda item: item["responder_count"],
            default=None,
        )

        records.append(
            {
                "severity_control": float(severity),
                "algorithm": str(algorithm),
                "target_reachability_pct": float(target_reachability_pct),
                "reliability_target_pct": float(reliability_target_pct),
                "minimum_responders": (
                    None if selected is None else selected["responder_count"]
                ),
                "mean_reachability_at_frontier_pct": (
                    None if selected is None else selected["mean_reachability_pct"]
                ),
                "target_service_probability_at_frontier_pct": (
                    None
                    if selected is None
                    else selected["target_service_probability_pct"]
                ),
                "frontier_found": selected is not None,
            }
        )

    return pd.DataFrame.from_records(records)


def marginal_resource_gains(surface: pd.DataFrame) -> pd.DataFrame:
    """Measure adjacent gains from adding responders at fixed severity/algorithm."""
    required = {
        "severity_control",
        "responder_count",
        "algorithm",
        "mean_reachability_pct",
        "mean_weighted_unmet_demand",
        "collapse_probability_pct",
    }
    missing = required.difference(surface.columns)
    if missing:
        raise ValueError(f"Surface frame is missing columns: {sorted(missing)}")

    records: list[dict[str, int | float | str]] = []

    for (severity, algorithm), group in surface.groupby(
        ["severity_control", "algorithm"],
        sort=True,
    ):
        ordered = group.sort_values("responder_count")
        previous = None

        for row in ordered.to_dict("records"):
            if previous is not None:
                added = int(row["responder_count"] - previous["responder_count"])
                if added <= 0:
                    previous = row
                    continue

                records.append(
                    {
                        "severity_control": float(severity),
                        "algorithm": str(algorithm),
                        "responders_from": int(previous["responder_count"]),
                        "responders_to": int(row["responder_count"]),
                        "responders_added": added,
                        "reachability_gain_pct_points": float(
                            row["mean_reachability_pct"]
                            - previous["mean_reachability_pct"]
                        ),
                        "reachability_gain_per_added_responder": float(
                            (
                                row["mean_reachability_pct"]
                                - previous["mean_reachability_pct"]
                            )
                            / added
                        ),
                        "unmet_demand_reduction": float(
                            previous["mean_weighted_unmet_demand"]
                            - row["mean_weighted_unmet_demand"]
                        ),
                        "collapse_probability_reduction_pct_points": float(
                            previous["collapse_probability_pct"]
                            - row["collapse_probability_pct"]
                        ),
                    }
                )
            previous = row

    return pd.DataFrame.from_records(records)


def paired_grid_inference(
    frame: pd.DataFrame,
    *,
    metrics: Iterable[str] = COST_METRICS,
    bootstrap_resamples: int = 3000,
    permutation_samples: int = 5000,
    seed: int = 5050,
) -> pd.DataFrame:
    """Paired Greedy-vs-Global inference across severity × responder cells."""
    records: list[dict[str, int | float | str | None]] = []

    for metric_index, metric in enumerate(metrics):
        required = {
            "severity_control",
            "responder_count",
            "seed",
            "algorithm",
            metric,
        }
        missing = required.difference(frame.columns)
        if missing:
            raise ValueError(f"Phase frame is missing columns: {sorted(missing)}")

        pivot = frame.pivot_table(
            index=["severity_control", "responder_count", "seed"],
            columns="algorithm",
            values=metric,
            aggfunc="first",
        )

        if not set(ALGORITHMS).issubset(pivot.columns):
            continue

        paired = pivot[list(ALGORITHMS)].dropna().reset_index()
        paired["greedy_minus_global"] = paired["greedy"] - paired["global_min_cost"]

        metric_records: list[dict[str, int | float | str | None]] = []

        grouped = paired.groupby(
            ["severity_control", "responder_count"],
            sort=True,
        )
        for cell_index, ((severity, responder_count), group) in enumerate(grouped):
            values = pd.to_numeric(
                group["greedy_minus_global"],
                errors="coerce",
            ).dropna().to_numpy(dtype=float)
            if values.size == 0:
                continue

            local_seed = seed + metric_index * 100_000 + cell_index * 1_000
            ci_low, ci_high = bootstrap_mean_ci(
                values,
                resamples=bootstrap_resamples,
                seed=local_seed,
            )
            p_value = paired_sign_flip_pvalue(
                values,
                permutations=permutation_samples,
                seed=local_seed + 1,
            )
            standard_deviation = (
                float(values.std(ddof=1)) if values.size > 1 else 0.0
            )

            metric_records.append(
                {
                    "metric": metric,
                    "severity_control": float(severity),
                    "responder_count": int(responder_count),
                    "n_pairs": int(values.size),
                    "mean_greedy_minus_global": float(mean(values)),
                    "bootstrap_ci_low": ci_low,
                    "bootstrap_ci_high": ci_high,
                    "permutation_p_value": p_value,
                    "holm_adjusted_p_value": None,
                    "effect_size_dz": (
                        None
                        if values.size < 2 or standard_deviation == 0.0
                        else float(mean(values) / standard_deviation)
                    ),
                    "global_win_rate_pct": float((values > 0).mean() * 100.0),
                    "tie_rate_pct": float((values == 0).mean() * 100.0),
                }
            )

        adjusted = holm_adjust(
            record["permutation_p_value"] for record in metric_records
        )
        for record, adjusted_value in zip(metric_records, adjusted, strict=True):
            record["holm_adjusted_p_value"] = adjusted_value

        records.extend(metric_records)

    return pd.DataFrame.from_records(records)
