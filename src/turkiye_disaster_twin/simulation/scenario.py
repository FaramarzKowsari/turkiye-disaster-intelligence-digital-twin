from __future__ import annotations

from collections.abc import Hashable, Iterable
from dataclasses import dataclass
from math import asin, cos, exp, radians, sin, sqrt
from random import Random
from typing import Any

import networkx as nx


@dataclass(frozen=True)
class EdgeRisk:
    edge_id: tuple[Hashable, Hashable, Hashable]
    failure_probability: float
    distance_km: float


@dataclass(frozen=True)
class Incident:
    node: Hashable
    severity: int


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance in kilometres."""
    radius_km = 6371.0088
    phi1, phi2 = radians(lat1), radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lon2 - lon1)
    value = (
        sin(dphi / 2) ** 2
        + cos(phi1) * cos(phi2) * sin(dlambda / 2) ** 2
    )
    return 2 * radius_km * asin(sqrt(value))


def edge_disruption_risks(
    graph: nx.MultiDiGraph,
    *,
    epicenter_lat: float,
    epicenter_lon: float,
    severity: float,
    decay_km: float = 8.0,
) -> list[EdgeRisk]:
    """Create transparent synthetic disruption probabilities for graph edges.

    This is a controlled stress-test proxy, not an engineering fragility model.
    ``severity`` is clamped to [0, 1]. Probability decays exponentially with
    edge-midpoint distance from the scenario centre.
    """
    stress = min(max(float(severity), 0.0), 1.0)
    decay = max(float(decay_km), 0.1)
    risks: list[EdgeRisk] = []

    for u, v, key in graph.edges(keys=True):
        u_data = graph.nodes[u]
        v_data = graph.nodes[v]
        mid_lat = (float(u_data["y"]) + float(v_data["y"])) / 2
        mid_lon = (float(u_data["x"]) + float(v_data["x"])) / 2
        distance = haversine_km(epicenter_lat, epicenter_lon, mid_lat, mid_lon)
        probability = stress * exp(-distance / decay)
        risks.append(
            EdgeRisk(
                edge_id=(u, v, key),
                failure_probability=min(max(probability, 0.0), 1.0),
                distance_km=distance,
            )
        )

    return risks


def sample_failed_edges(
    risks: Iterable[EdgeRisk],
    *,
    seed: int,
) -> set[tuple[Hashable, Hashable, Hashable]]:
    """Sample synthetic road failures reproducibly from explicit probabilities."""
    rng = Random(seed)
    failed: set[tuple[Hashable, Hashable, Hashable]] = set()

    for risk in risks:
        p = min(max(risk.failure_probability, 0.0), 1.0)
        if rng.random() < p:
            failed.add(risk.edge_id)

    return failed


def apply_failed_edges(
    graph: nx.MultiDiGraph,
    failed_edges: Iterable[tuple[Hashable, Hashable, Hashable]],
) -> nx.MultiDiGraph:
    """Return a graph copy with the sampled failed directed edges removed."""
    disrupted = graph.copy()
    for u, v, key in failed_edges:
        if disrupted.has_edge(u, v, key):
            disrupted.remove_edge(u, v, key)
    return disrupted


def sample_snapshot_entities(
    graph: nx.MultiDiGraph,
    *,
    incident_count: int,
    responder_count: int,
    epicenter_lat: float,
    epicenter_lon: float,
    seed: int,
    demand_decay_km: float = 6.0,
) -> tuple[list[Incident], list[Hashable]]:
    """Sample unique incident and responder nodes for a reproducible snapshot.

    Incident locations are weighted toward the scenario centre. Responders are
    sampled from the remaining graph nodes. Incident severity is synthetic 1–5.
    """
    nodes = list(graph.nodes)
    required = incident_count + responder_count
    if required > len(nodes):
        raise ValueError("Requested incidents and responders exceed available graph nodes.")

    rng = Random(seed)
    available = set(nodes)
    incidents: list[Incident] = []

    for _ in range(max(0, incident_count)):
        candidates = list(available)
        weights = []
        for node in candidates:
            data = graph.nodes[node]
            distance = haversine_km(
                epicenter_lat,
                epicenter_lon,
                float(data["y"]),
                float(data["x"]),
            )
            weights.append(exp(-distance / max(demand_decay_km, 0.1)) + 1e-12)

        node = rng.choices(candidates, weights=weights, k=1)[0]
        available.remove(node)
        severity = rng.randint(1, 5)
        incidents.append(Incident(node=node, severity=severity))

    responders = rng.sample(list(available), k=max(0, responder_count))
    return incidents, responders


def scenario_manifest(
    *,
    seed: int,
    severity: float,
    decay_km: float,
    incident_count: int,
    responder_count: int,
    failed_edge_count: int,
) -> dict[str, Any]:
    """Return serialisable provenance for one synthetic scenario realisation."""
    return {
        "scenario_type": "controlled_stochastic_stress_test",
        "seed": int(seed),
        "severity_control": float(severity),
        "distance_decay_km": float(decay_km),
        "incident_count": int(incident_count),
        "responder_count": int(responder_count),
        "failed_directed_edges": int(failed_edge_count),
        "damage_model_claim": False,
    }
