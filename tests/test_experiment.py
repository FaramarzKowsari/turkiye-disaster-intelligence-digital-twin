import networkx as nx

from turkiye_disaster_twin.simulation.experiment import (
    paired_algorithm_comparison,
    run_monte_carlo_experiment,
    summarise_experiment,
)


def _dense_graph() -> nx.MultiDiGraph:
    graph = nx.MultiDiGraph()
    for index in range(6):
        graph.add_node(index, x=29.0 + index * 0.001, y=41.0 + index * 0.001)

    for source in range(6):
        for target in range(6):
            if source == target:
                continue
            graph.add_edge(
                source,
                target,
                travel_time=abs(source - target) + 1,
            )
    return graph


def test_experiment_produces_paired_rows():
    frame = run_monte_carlo_experiment(
        _dense_graph(),
        epicenter_lat=41.0,
        epicenter_lon=29.0,
        severities=[0.0, 0.1],
        realizations=3,
        incident_count=2,
        responder_count=2,
        base_seed=10,
    )

    assert len(frame) == 12
    assert set(frame["algorithm"]) == {"greedy", "global_min_cost"}
    assert frame.groupby(["severity_control", "seed"]).size().eq(2).all()


def test_experiment_summary_contains_confidence_bounds():
    frame = run_monte_carlo_experiment(
        _dense_graph(),
        epicenter_lat=41.0,
        epicenter_lon=29.0,
        severities=[0.0],
        realizations=3,
        incident_count=2,
        responder_count=2,
        base_seed=30,
    )
    summary = summarise_experiment(frame)

    assert not summary.empty
    assert {"mean", "ci95_low", "ci95_high"} <= set(summary.columns)
    assert set(summary["algorithm"]) == {"greedy", "global_min_cost"}


def test_paired_comparison_uses_matching_seeds():
    frame = run_monte_carlo_experiment(
        _dense_graph(),
        epicenter_lat=41.0,
        epicenter_lon=29.0,
        severities=[0.0],
        realizations=4,
        incident_count=2,
        responder_count=2,
        base_seed=50,
    )
    comparison = paired_algorithm_comparison(frame)

    assert comparison.loc[0, "n_pairs"] == 4
    assert comparison.loc[0, "mean_greedy_minus_global"] >= 0
