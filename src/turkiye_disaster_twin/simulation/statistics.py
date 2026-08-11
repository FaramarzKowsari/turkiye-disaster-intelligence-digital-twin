from __future__ import annotations

from collections.abc import Iterable

import numpy as np
import pandas as pd

ALGORITHM_COLUMNS = ("greedy", "global_min_cost")
DEFAULT_COST_METRICS = (
    "mean_response_s",
    "median_response_s",
    "p90_response_s",
    "total_response_s",
    "weighted_unmet_demand",
)


def paired_differences(frame: pd.DataFrame, *, metric: str) -> pd.DataFrame:
    """Return matched Greedy-minus-Global differences for one metric.

    Positive differences mean the global minimum-cost method achieved a lower
    value for cost-like metrics such as response time or unmet demand.
    """
    required = {"severity_control", "seed", "algorithm", metric}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"Experiment frame is missing columns: {sorted(missing)}")

    pivot = frame.pivot_table(
        index=["severity_control", "seed"],
        columns="algorithm",
        values=metric,
        aggfunc="first",
    )

    if not set(ALGORITHM_COLUMNS).issubset(pivot.columns):
        return pd.DataFrame(
            columns=[
                "severity_control",
                "seed",
                "greedy",
                "global_min_cost",
                "greedy_minus_global",
            ]
        )

    paired = pivot[list(ALGORITHM_COLUMNS)].dropna().reset_index()
    paired["greedy_minus_global"] = paired["greedy"] - paired["global_min_cost"]
    return paired


def bootstrap_mean_ci(
    values: Iterable[float],
    *,
    confidence: float = 0.95,
    resamples: int = 5000,
    seed: int = 2026,
    batch_size: int = 512,
) -> tuple[float, float]:
    """Bootstrap a percentile confidence interval for the sample mean."""
    sample = np.asarray(list(values), dtype=float)
    sample = sample[np.isfinite(sample)]

    if sample.size == 0:
        raise ValueError("At least one finite value is required.")
    if not 0.0 < confidence < 1.0:
        raise ValueError("confidence must be between 0 and 1")
    if resamples < 1:
        raise ValueError("resamples must be at least 1")

    if sample.size == 1:
        value = float(sample[0])
        return value, value

    rng = np.random.default_rng(seed)
    bootstrap_means = np.empty(resamples, dtype=float)

    for start in range(0, resamples, batch_size):
        stop = min(start + batch_size, resamples)
        indices = rng.integers(
            0,
            sample.size,
            size=(stop - start, sample.size),
        )
        bootstrap_means[start:stop] = sample[indices].mean(axis=1)

    alpha = 1.0 - confidence
    low, high = np.quantile(
        bootstrap_means,
        [alpha / 2.0, 1.0 - alpha / 2.0],
    )
    return float(low), float(high)


def paired_sign_flip_pvalue(
    values: Iterable[float],
    *,
    permutations: int = 10000,
    seed: int = 2026,
    batch_size: int = 512,
) -> float:
    """Two-sided paired sign-flip permutation test for a non-zero mean difference."""
    sample = np.asarray(list(values), dtype=float)
    sample = sample[np.isfinite(sample)]

    if sample.size == 0:
        raise ValueError("At least one finite paired difference is required.")
    if permutations < 1:
        raise ValueError("permutations must be at least 1")

    observed = abs(float(sample.mean()))
    rng = np.random.default_rng(seed)
    extreme = 0

    for start in range(0, permutations, batch_size):
        stop = min(start + batch_size, permutations)
        signs = rng.choice(
            np.array([-1.0, 1.0]),
            size=(stop - start, sample.size),
        )
        permuted = (signs * sample).mean(axis=1)
        extreme += int(np.count_nonzero(np.abs(permuted) >= observed))

    return float((extreme + 1) / (permutations + 1))


def holm_adjust(p_values: Iterable[float]) -> list[float]:
    """Holm family-wise error-rate correction."""
    values = np.asarray(list(p_values), dtype=float)
    if values.size == 0:
        return []

    order = np.argsort(values)
    adjusted = np.empty_like(values)
    running = 0.0
    total = values.size

    for rank, index in enumerate(order):
        candidate = min(1.0, float((total - rank) * values[index]))
        running = max(running, candidate)
        adjusted[index] = running

    return adjusted.tolist()


def paper_grade_paired_inference(
    frame: pd.DataFrame,
    *,
    metrics: Iterable[str] = DEFAULT_COST_METRICS,
    bootstrap_resamples: int = 5000,
    permutation_samples: int = 10000,
    confidence: float = 0.95,
    seed: int = 2026,
) -> pd.DataFrame:
    """Produce paired effect estimates, bootstrap CIs and permutation p-values.

    Statistical tests are performed separately for each severity and metric.
    Holm correction is then applied across severities within each metric.
    """
    records: list[dict[str, int | float | str | None]] = []

    for metric_index, metric in enumerate(metrics):
        paired = paired_differences(frame, metric=metric)
        if paired.empty:
            continue

        metric_records: list[dict[str, int | float | str | None]] = []

        for severity_index, (severity, group) in enumerate(
            paired.groupby("severity_control", sort=True)
        ):
            deltas = pd.to_numeric(
                group["greedy_minus_global"],
                errors="coerce",
            ).dropna()
            if deltas.empty:
                continue

            values = deltas.to_numpy(dtype=float)
            mean_delta = float(values.mean())
            median_delta = float(np.median(values))
            std_delta = float(values.std(ddof=1)) if values.size > 1 else 0.0
            effect_size_dz = (
                None
                if values.size < 2 or std_delta == 0.0
                else float(mean_delta / std_delta)
            )

            local_seed = seed + metric_index * 100_000 + severity_index * 1_000
            ci_low, ci_high = bootstrap_mean_ci(
                values,
                confidence=confidence,
                resamples=bootstrap_resamples,
                seed=local_seed,
            )
            p_value = paired_sign_flip_pvalue(
                values,
                permutations=permutation_samples,
                seed=local_seed + 1,
            )

            metric_records.append(
                {
                    "metric": metric,
                    "severity_control": float(severity),
                    "n_pairs": int(values.size),
                    "mean_greedy_minus_global": mean_delta,
                    "median_greedy_minus_global": median_delta,
                    "bootstrap_ci_low": ci_low,
                    "bootstrap_ci_high": ci_high,
                    "permutation_p_value": p_value,
                    "holm_adjusted_p_value": None,
                    "effect_size_dz": effect_size_dz,
                    "global_win_rate_pct": float((values > 0).mean() * 100.0),
                    "tie_rate_pct": float((values == 0).mean() * 100.0),
                }
            )

        adjusted = holm_adjust(
            record["permutation_p_value"] for record in metric_records
        )
        for record, adjusted_value in zip(metric_records, adjusted, strict=True):
            record["holm_adjusted_p_value"] = adjusted_value

        records.extend(metric_records)

    return pd.DataFrame.from_records(records)
