from __future__ import annotations

from collections.abc import Hashable

import networkx as nx


def graph_line_coordinates(
    graph: nx.MultiDiGraph,
    *,
    max_edges: int = 4000,
) -> tuple[list[float | None], list[float | None]]:
    """Convert a road graph into Plotly-compatible lon/lat line arrays.

    A deterministic stride is used when the graph is larger than ``max_edges``.
    This keeps public deployments responsive while preserving network coverage.
    """
    edges = list(graph.edges(keys=True, data=True))
    if not edges:
        return [], []

    stride = max(1, len(edges) // max_edges)
    selected = edges[::stride][:max_edges]

    longitudes: list[float | None] = []
    latitudes: list[float | None] = []

    for u, v, _key, data in selected:
        geometry = data.get("geometry")

        if geometry is not None and hasattr(geometry, "coords"):
            coords = list(geometry.coords)
        else:
            coords = [
                (_node_value(graph, u, "x"), _node_value(graph, u, "y")),
                (_node_value(graph, v, "x"), _node_value(graph, v, "y")),
            ]

        for lon, lat in coords:
            longitudes.append(float(lon))
            latitudes.append(float(lat))

        longitudes.append(None)
        latitudes.append(None)

    return longitudes, latitudes


def graph_center(graph: nx.MultiDiGraph) -> tuple[float, float]:
    """Return mean latitude/longitude from graph nodes."""
    latitudes = [float(data["y"]) for _, data in graph.nodes(data=True) if "y" in data]
    longitudes = [float(data["x"]) for _, data in graph.nodes(data=True) if "x" in data]
    if not latitudes or not longitudes:
        return 41.0082, 28.9784
    return sum(latitudes) / len(latitudes), sum(longitudes) / len(longitudes)


def _node_value(graph: nx.MultiDiGraph, node: Hashable, key: str) -> float:
    value = graph.nodes[node].get(key)
    if value is None:
        raise ValueError(f"Graph node {node!r} has no {key!r} coordinate.")
    return float(value)


def selected_edge_line_coordinates(
    graph: nx.MultiDiGraph,
    edge_ids,
) -> tuple[list[float | None], list[float | None]]:
    """Convert selected edge IDs into Plotly-compatible line coordinates."""
    longitudes: list[float | None] = []
    latitudes: list[float | None] = []

    for u, v, key in edge_ids:
        data = graph.get_edge_data(u, v, key)
        if data is None:
            continue
        geometry = data.get("geometry")
        if geometry is not None and hasattr(geometry, "coords"):
            coords = list(geometry.coords)
        else:
            coords = [
                (_node_value(graph, u, "x"), _node_value(graph, u, "y")),
                (_node_value(graph, v, "x"), _node_value(graph, v, "y")),
            ]

        for lon, lat in coords:
            longitudes.append(float(lon))
            latitudes.append(float(lat))
        longitudes.append(None)
        latitudes.append(None)

    return longitudes, latitudes
