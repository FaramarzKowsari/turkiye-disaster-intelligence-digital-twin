import networkx as nx

from turkiye_disaster_twin.visualization import graph_center, graph_line_coordinates


def test_graph_line_coordinates_without_geometry():
    graph = nx.MultiDiGraph()
    graph.add_node("a", x=29.0, y=41.0)
    graph.add_node("b", x=29.1, y=41.1)
    graph.add_edge("a", "b")

    longitudes, latitudes = graph_line_coordinates(graph)

    assert longitudes == [29.0, 29.1, None]
    assert latitudes == [41.0, 41.1, None]


def test_graph_center():
    graph = nx.MultiDiGraph()
    graph.add_node("a", x=29.0, y=41.0)
    graph.add_node("b", x=29.2, y=41.2)

    latitude, longitude = graph_center(graph)

    assert latitude == 41.1
    assert longitude == 29.1
