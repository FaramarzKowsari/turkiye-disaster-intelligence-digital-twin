from __future__ import annotations

import geopandas as gpd
import osmnx as ox
import pandas as pd

EMERGENCY_TAGS = {
    "amenity": ["hospital", "clinic", "fire_station"],
}


def load_drive_graph(place: str):
    """Download a drivable OpenStreetMap graph and add estimated travel times."""
    graph = ox.graph.graph_from_place(
        place,
        network_type="drive",
        simplify=True,
        retain_all=False,
    )
    graph = ox.routing.add_edge_speeds(graph)
    graph = ox.routing.add_edge_travel_times(graph)
    return graph


def load_emergency_facilities(place: str) -> gpd.GeoDataFrame:
    """Download selected emergency and health facilities from OpenStreetMap."""
    return ox.features.features_from_place(place, EMERGENCY_TAGS)


def facility_points(features: gpd.GeoDataFrame) -> pd.DataFrame:
    """Convert point/polygon OSM facilities into display-ready representative points."""
    columns = ["name", "category", "latitude", "longitude", "source"]
    if features.empty:
        return pd.DataFrame(columns=columns)

    frame = features.copy()
    if frame.crs is None:
        frame = frame.set_crs("EPSG:4326")
    else:
        frame = frame.to_crs("EPSG:4326")

    points = frame.geometry.representative_point()
    names = frame["name"] if "name" in frame.columns else pd.Series(pd.NA, index=frame.index)
    amenity = (
        frame["amenity"] if "amenity" in frame.columns else pd.Series("facility", index=frame.index)
    )

    result = pd.DataFrame(
        {
            "name": names.fillna("Unnamed facility").astype(str).to_numpy(),
            "category": amenity.fillna("facility").astype(str).to_numpy(),
            "latitude": points.y.to_numpy(),
            "longitude": points.x.to_numpy(),
            "source": "OpenStreetMap",
        }
    )
    return result.dropna(subset=["latitude", "longitude"]).reset_index(drop=True)
