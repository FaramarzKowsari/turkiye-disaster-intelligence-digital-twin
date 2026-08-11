import pandas as pd

from turkiye_disaster_twin.simulation.phase_transition import (
    _global_from_costs,
    _greedy_from_costs,
    marginal_resource_gains,
    phase_surface_summary,
    resource_frontier,
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
