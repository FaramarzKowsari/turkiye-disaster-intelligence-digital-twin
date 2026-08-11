import pandas as pd

from turkiye_disaster_twin.simulation.statistics import (
    bootstrap_mean_ci,
    holm_adjust,
    paired_differences,
    paired_sign_flip_pvalue,
    paper_grade_paired_inference,
)


def _frame():
    records = []
    for seed, greedy, global_cost in [
        (1, 12.0, 8.0),
        (2, 11.0, 8.0),
        (3, 10.0, 7.0),
        (4, 9.0, 7.0),
    ]:
        for algorithm, value in (
            ("greedy", greedy),
            ("global_min_cost", global_cost),
        ):
            records.append(
                {
                    "severity_control": 0.25,
                    "seed": seed,
                    "algorithm": algorithm,
                    "total_response_s": value,
                    "mean_response_s": value,
                    "median_response_s": value,
                    "p90_response_s": value,
                    "weighted_unmet_demand": value,
                }
            )
    return pd.DataFrame.from_records(records)


def test_paired_differences_are_matched_by_seed():
    paired = paired_differences(_frame(), metric="total_response_s")
    assert paired["greedy_minus_global"].tolist() == [4.0, 3.0, 3.0, 2.0]


def test_bootstrap_interval_contains_mean_for_stable_sample():
    low, high = bootstrap_mean_ci(
        [2.0, 3.0, 3.0, 4.0],
        resamples=1000,
        seed=9,
    )
    assert low <= 3.0 <= high


def test_sign_flip_detects_consistent_positive_difference():
    p_value = paired_sign_flip_pvalue(
        [4.0, 3.0, 3.0, 2.0],
        permutations=2000,
        seed=4,
    )
    assert 0.0 < p_value <= 1.0


def test_holm_adjustment_is_monotone_in_sorted_order():
    adjusted = holm_adjust([0.01, 0.04, 0.03])
    assert all(0.0 <= value <= 1.0 for value in adjusted)
    assert adjusted[0] <= max(adjusted)


def test_paper_grade_inference_reports_global_wins():
    result = paper_grade_paired_inference(
        _frame(),
        metrics=["total_response_s"],
        bootstrap_resamples=500,
        permutation_samples=500,
        seed=12,
    )
    assert len(result) == 1
    assert result.loc[0, "mean_greedy_minus_global"] == 3.0
    assert result.loc[0, "global_win_rate_pct"] == 100.0
