from __future__ import annotations

import osmnx as ox


def load_drive_graph(place: str = "Istanbul, Türkiye"):
    """Download a drivable OpenStreetMap network for the requested place."""
    graph = ox.graph_from_place(place, network_type="drive", simplify=True)
    graph = ox.add_edge_speeds(graph)
    graph = ox.add_edge_travel_times(graph)
    return graph


def load_emergency_facilities(place: str = "Istanbul, Türkiye"):
    """Load selected public emergency and health facilities from OpenStreetMap."""
    tags = {
        "amenity": ["hospital", "clinic", "fire_station"],
    }
    return ox.features_from_place(place, tags)
