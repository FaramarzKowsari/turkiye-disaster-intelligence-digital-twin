from turkiye_disaster_twin.simulation.scenario import EdgeRisk, sample_failed_edges


def test_scenario_is_reproducible():
    risks = [
        EdgeRisk("a", 0.2),
        EdgeRisk("b", 0.8),
        EdgeRisk("c", 0.5),
    ]
    assert sample_failed_edges(risks, seed=42) == sample_failed_edges(risks, seed=42)


def test_probability_bounds_are_clipped():
    risks = [
        EdgeRisk("never", -3.0),
        EdgeRisk("always", 5.0),
    ]
    failed = sample_failed_edges(risks, seed=1)
    assert "never" not in failed
    assert "always" in failed
