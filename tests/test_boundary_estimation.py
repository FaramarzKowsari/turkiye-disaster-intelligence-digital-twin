import numpy as np
import pandas as pd

from turkiye_disaster_twin.research.boundary import (
    boundary_estimates,
    monotonicity_audit,
    pava_nonincreasing,
    service_probability_curve,
    wilson_interval,
)


def test_pava_nonincreasing_repairs_local_reversal():
    fitted = pava_nonincreasing([90.0, 75.0, 80.0, 60.0])
    assert np.all(np.diff(fitted) <= 1e-12)
    assert np.allclose(fitted, [90.0, 77.5, 77.5, 60.0])


def test_wilson_interval_contains_observed_fraction():
    low, high = wilson_interval(80, 100)
    assert low < 0.80 < high


def _toy_boundary_frame() -> pd.DataFrame:
    rows = []
    severities = [0.14, 0.15, 0.16]

    for seed in range(100):
        for severity in severities:
            if severity == 0.14:
                reachability = 90.0
            elif severity == 0.15:
                reachability = 90.0 if seed < 90 else 70.0
            else:
                reachability = 90.0 if seed < 70 else 70.0

            rows.append(
                {
                    "algorithm": "global_min_cost",
                    "responder_count": 16,
                    "seed": seed,
                    "severity_control": severity,
                    "reachability_pct": reachability,
                    "failed_directed_edges": int(severity * 1000),
                }
            )

    return pd.DataFrame(rows)


def test_boundary_estimate_falls_between_bracketing_severities():
    frame = _toy_boundary_frame()
    estimates = boundary_estimates(
        frame,
        bootstrap_resamples=200,
        seed=123,
    )
    row = estimates.iloc[0]

    assert row["boundary_status"] == "within_grid"
    assert row["boundary_lower_severity"] == 0.15
    assert row["boundary_upper_severity"] == 0.16
    assert 0.15 < row["boundary_point_estimate"] < 0.16


def test_probability_curve_and_monotonicity_audit():
    frame = _toy_boundary_frame()
    curve = service_probability_curve(frame)
    audit = monotonicity_audit(frame)

    assert curve["service_probability_pct"].tolist() == [100.0, 90.0, 70.0]
    global_audit = audit[
        (audit["audit_type"] == "reachability_non_increasing")
        & (audit["algorithm"] == "global_min_cost")
    ]
    assert int(global_audit.iloc[0]["violations"]) == 0
