from __future__ import annotations

from collections.abc import Hashable
from dataclasses import dataclass

import networkx as nx


@dataclass(frozen=True)
class Assignment:
    incident: Hashable
    responder: Hashable
    travel_time: float


def greedy_nearest_responder(
    graph: nx.Graph,
    *,
    responders: list[Hashable],
    incidents: list[Hashable],
    weight: str = "travel_time",
) -> list[Assignment]:
    """Assign incidents sequentially to the nearest currently unused responder."""
    available = set(responders)
    assignments: list[Assignment] = []

    for incident in incidents:
        best: tuple[float, Hashable] | None = None

        for responder in available:
            try:
                cost = nx.shortest_path_length(
                    graph,
                    source=responder,
                    target=incident,
                    weight=weight,
                )
            except (nx.NetworkXNoPath, nx.NodeNotFound):
                continue

            if best is None or cost < best[0]:
                best = (float(cost), responder)

        if best is None:
            continue

        cost, responder = best
        assignments.append(
            Assignment(
                incident=incident,
                responder=responder,
                travel_time=cost,
            )
        )
        available.remove(responder)

        if not available:
            break

    return assignments


def min_cost_global_assignment(
    graph: nx.Graph,
    *,
    responders: list[Hashable],
    incidents: list[Hashable],
    weight: str = "travel_time",
) -> list[Assignment]:
    """Find a globally minimum-cost one-to-one assignment for reachable pairs.

    A min-cost flow problem is built from all responder-to-incident shortest-path
    costs. The flow cardinality is first maximised, then that feasible cardinality
    is solved at minimum total travel cost.
    """
    if not responders or not incidents:
        return []

    flow_graph = nx.DiGraph()
    source = ("source",)
    sink = ("sink",)

    responder_nodes = [("responder", index) for index in range(len(responders))]
    incident_nodes = [("incident", index) for index in range(len(incidents))]

    for flow_node in responder_nodes:
        flow_graph.add_edge(source, flow_node, capacity=1, weight=0)

    for flow_node in incident_nodes:
        flow_graph.add_edge(flow_node, sink, capacity=1, weight=0)

    costs: dict[tuple[int, int], float] = {}
    for responder_index, responder in enumerate(responders):
        for incident_index, incident in enumerate(incidents):
            try:
                cost = float(
                    nx.shortest_path_length(
                        graph,
                        source=responder,
                        target=incident,
                        weight=weight,
                    )
                )
            except (nx.NetworkXNoPath, nx.NodeNotFound):
                continue

            costs[(responder_index, incident_index)] = cost
            flow_graph.add_edge(
                responder_nodes[responder_index],
                incident_nodes[incident_index],
                capacity=1,
                weight=max(0, round(cost * 1000)),
            )

    if not costs:
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
                    travel_time=costs[(responder_index, incident_index)],
                )
            )

    return assignments
