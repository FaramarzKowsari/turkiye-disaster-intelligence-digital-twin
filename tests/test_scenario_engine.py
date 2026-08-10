import networkx as nx

from turkiye_disaster_twin.simulation.scenario import (
    apply_failed_edges,
    edge_disruption_risks,
    sample_failed_edges,
)


def _graph():
    graph = nx.MultiDiGraph()
    graph.add_node("near-a", x=29.0, y=41.0)
    graph.add_node("near-b", x=29.001, y=41.001)
    graph.add_node("far-a", x=30.0, y=42.0)
    graph.add_node("far-b", x=30.001, y=42.001)
    graph.add_edge("near-a", "near-b", key=0, travel_time=10)
    graph.add_edge("far-a", "far-b", key=0, travel_time=10)
    return graph


def test_risk_decays_with_distance():
    risks = edge_disruption_risks(
        _graph(),
        epicenter_lat=41.0,
        epicenter_lon=29.0,
        severity=0.8,
        decay_km=10,
    )
    probability = {risk.edge_id: risk.failure_probability for risk in risks}
    assert probability[("near-a", "near-b", 0)] > probability[("far-a", "far-b", 0)]


def test_failed_edge_sampling_is_reproducible():
    risks = edge_disruption_risks(
        _graph(),
        epicenter_lat=41.0,
        epicenter_lon=29.0,
        severity=0.8,
    )
    assert sample_failed_edges(risks, seed=42) == sample_failed_edges(risks, seed=42)


def test_apply_failed_edges_does_not_mutate_original():
    graph = _graph()
    disrupted = apply_failed_edges(graph, {("near-a", "near-b", 0)})
    assert graph.has_edge("near-a", "near-b", 0)
    assert not disrupted.has_edge("near-a", "near-b", 0)
