from __future__ import annotations

from dataclasses import dataclass
from typing import Hashable

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
    """Assign each incident to the nearest unused responder."""
    available = set(responders)
    assignments: list[Assignment] = []

    for incident in incidents:
        best: tuple[float, Hashable] | None = None

        for responder in available:
            try:
                cost = nx.shortest_path_length(
                    graph, source=responder, target=incident, weight=weight
                )
            except nx.NetworkXNoPath:
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
