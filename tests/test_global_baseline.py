import networkx as nx

from turkiye_disaster_twin.simulation.baselines import (
    greedy_nearest_responder,
    min_cost_global_assignment,
)


def test_global_assignment_can_beat_sequential_greedy():
    graph = nx.DiGraph()
    graph.add_edge("r1", "i1", travel_time=1)
    graph.add_edge("r1", "i2", travel_time=2)
    graph.add_edge("r2", "i1", travel_time=2)
    graph.add_edge("r2", "i2", travel_time=100)

    greedy = greedy_nearest_responder(
        graph,
        responders=["r1", "r2"],
        incidents=["i1", "i2"],
    )
    global_optimum = min_cost_global_assignment(
        graph,
        responders=["r1", "r2"],
        incidents=["i1", "i2"],
    )

    assert sum(item.travel_time for item in global_optimum) == 4
    assert sum(item.travel_time for item in greedy) == 101
