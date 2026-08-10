from turkiye_disaster_twin.simulation.baselines import Assignment
from turkiye_disaster_twin.simulation.metrics import response_metrics
from turkiye_disaster_twin.simulation.scenario import Incident


def test_response_metrics_tracks_weighted_unmet_demand():
    incidents = [
        Incident(node="i1", severity=2),
        Incident(node="i2", severity=5),
    ]
    assignments = [
        Assignment(incident="i1", responder="r1", travel_time=30.0),
    ]

    metrics = response_metrics(assignments, incidents)

    assert metrics.assigned == 1
    assert metrics.unreachable == 1
    assert metrics.reachability_pct == 50.0
    assert metrics.weighted_unmet_demand == 5
    assert metrics.mean_response_s == 30.0
