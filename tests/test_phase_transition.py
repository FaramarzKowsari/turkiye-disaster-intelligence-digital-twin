from itertools import pairwise

import networkx as nx
import pandas as pd

from turkiye_disaster_twin.simulation.phase_transition import (
    _global_from_costs,
    _greedy_from_costs,
    marginal_resource_gains,
    phase_surface_summary,
    resource_frontier,
    run_phase_transition_experiment,
)


def test_cached_global_assignment_can_beat_greedy():
    responders = ["r1", "r2"]
    incidents = ["i1", "i2"]
    costs = {
        ("r1", "i1"): 1.0,
        ("r1", "i2"): 2.0,
        ("r2", "i1"): 2.0,
        ("r2", "i2"): 100.0,
    }

    greedy = _greedy_from_costs(responders, incidents, costs)
    global_optimum = _global_from_costs(responders, incidents, costs)

    assert sum(item.travel_time for item in greedy) == 101.0
    assert sum(item.travel_time for item in global_optimum) == 4.0


def test_phase_surface_and_frontier():
    rows = []
    for seed in range(5):
        for responders, reachability in ((4, 40.0), (8, 80.0), (12, 100.0)):
            rows.append(
                {
                    "severity_control": 0.10,
                    "responder_count": responders,
                    "algorithm": "global_min_cost",
                    "seed": seed,
                    "reachability_pct": reachability,
                    "weighted_unmet_demand": 10.0 - responders / 2,
                    "total_response_s": 100.0,
                    "p90_response_s": 50.0,
                    "assigned": int(reachability / 10),
                    "failed_directed_edges": 100,
                }
            )

    frame = pd.DataFrame(rows)
    surface = phase_surface_summary(
        frame,
        collapse_threshold_pct=20.0,
        target_reachability_pct=80.0,
    )
    frontier = resource_frontier(
        frame,
        target_reachability_pct=80.0,
        reliability_target_pct=80.0,
    )
    marginal = marginal_resource_gains(surface)

    assert frontier.loc[0, "minimum_responders"] == 8
    assert not marginal.empty
    assert surface["target_service_probability_pct"].max() == 100.0

def _small_routing_graph() -> nx.MultiDiGraph:
    graph = nx.MultiDiGraph()
    node_count = 14

    for node in range(node_count):
        graph.add_node(
            node,
            x=29.0 + node * 0.001,
            y=41.0 + node * 0.001,
        )

    for node in range(node_count - 1):
        graph.add_edge(node, node + 1, travel_time=10.0)
        graph.add_edge(node + 1, node, travel_time=10.0)

    for node in range(node_count - 2):
        graph.add_edge(node, node + 2, travel_time=16.0)
        graph.add_edge(node + 2, node, travel_time=16.0)

    return graph


def test_global_reachability_is_monotone_under_coupled_severity():
    frame = run_phase_transition_experiment(
        _small_routing_graph(),
        epicenter_lat=41.006,
        epicenter_lon=29.006,
        severities=[0.05, 0.15, 0.30, 0.50],
        responder_counts=[2, 4],
        realizations=8,
        incident_count=4,
        base_seed=9000,
        decay_km=2.0,
    )

    global_rows = frame[frame["algorithm"] == "global_min_cost"]

    for (_seed, _responders), group in global_rows.groupby(
        ["seed", "responder_count"]
    ):
        ordered = group.sort_values("severity_control")
        reachability = ordered["reachability_pct"].tolist()
        failed_edges = ordered["failed_directed_edges"].tolist()

        assert all(
            later <= earlier
            for earlier, later in pairwise(reachability)
        )
        assert all(
            later >= earlier
            for earlier, later in pairwise(failed_edges)
        )


def test_same_world_seed_is_reused_across_severity_levels():
    frame = run_phase_transition_experiment(
        _small_routing_graph(),
        epicenter_lat=41.006,
        epicenter_lon=29.006,
        severities=[0.10, 0.20, 0.30],
        responder_counts=[2],
        realizations=3,
        incident_count=3,
        base_seed=1200,
        decay_km=2.0,
    )

    seeds_per_realization = frame.groupby("realization")["seed"].nunique()
    assert seeds_per_realization.eq(1).all()

