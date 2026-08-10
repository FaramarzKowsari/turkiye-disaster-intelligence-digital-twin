import networkx as nx

from turkiye_disaster_twin.simulation.baselines import greedy_nearest_responder


def test_greedy_nearest_responder():
    g = nx.Graph()
    g.add_edge("r1", "i1", travel_time=5)
    g.add_edge("r2", "i1", travel_time=2)

    result = greedy_nearest_responder(
        g,
        responders=["r1", "r2"],
        incidents=["i1"],
    )

    assert len(result) == 1
    assert result[0].responder == "r2"
    assert result[0].travel_time == 2
