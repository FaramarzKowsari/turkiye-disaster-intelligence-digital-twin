from __future__ import annotations

from dataclasses import dataclass

import networkx as nx

from turkiye_disaster_twin.simulation.baselines import (
    Assignment,
    greedy_nearest_responder,
    min_cost_global_assignment,
)
from turkiye_disaster_twin.simulation.metrics import ResponseMetrics, response_metrics
from turkiye_disaster_twin.simulation.scenario import (
    Incident,
    apply_failed_edges,
    edge_disruption_risks,
    sample_failed_edges,
    sample_snapshot_entities,
    scenario_manifest,
)


@dataclass
class SnapshotResult:
    disrupted_graph: nx.MultiDiGraph
    failed_edges: set[tuple[object, object, object]]
    incidents: list[Incident]
    responders: list[object]
    greedy_assignments: list[Assignment]
    global_assignments: list[Assignment]
    greedy_metrics: ResponseMetrics
    global_metrics: ResponseMetrics
    manifest: dict[str, object]


def run_snapshot(
    graph: nx.MultiDiGraph,
    *,
    epicenter_lat: float,
    epicenter_lon: float,
    disruption_severity: float,
    incident_count: int,
    responder_count: int,
    seed: int,
    decay_km: float = 8.0,
) -> SnapshotResult:
    """Run one reproducible synthetic post-earthquake network stress test."""
    risks = edge_disruption_risks(
        graph,
        epicenter_lat=epicenter_lat,
        epicenter_lon=epicenter_lon,
        severity=disruption_severity,
        decay_km=decay_km,
    )
    failed_edges = sample_failed_edges(risks, seed=seed)
    disrupted = apply_failed_edges(graph, failed_edges)

    incidents, responders = sample_snapshot_entities(
        graph,
        incident_count=incident_count,
        responder_count=responder_count,
        epicenter_lat=epicenter_lat,
        epicenter_lon=epicenter_lon,
        seed=seed + 1,
    )
    incident_nodes = [incident.node for incident in incidents]

    greedy = greedy_nearest_responder(
        disrupted,
        responders=responders,
        incidents=incident_nodes,
    )
    global_optimum = min_cost_global_assignment(
        disrupted,
        responders=responders,
        incidents=incident_nodes,
    )

    return SnapshotResult(
        disrupted_graph=disrupted,
        failed_edges=failed_edges,
        incidents=incidents,
        responders=list(responders),
        greedy_assignments=greedy,
        global_assignments=global_optimum,
        greedy_metrics=response_metrics(greedy, incidents),
        global_metrics=response_metrics(global_optimum, incidents),
        manifest=scenario_manifest(
            seed=seed,
            severity=disruption_severity,
            decay_km=decay_km,
            incident_count=incident_count,
            responder_count=responder_count,
            failed_edge_count=len(failed_edges),
        ),
    )
