from __future__ import annotations

from math import sqrt

import numpy as np
import pandas as pd


def _required_columns(frame: pd.DataFrame) -> None:
    required = {
        "severity_control",
        "responder_count",
        "algorithm",
        "seed",
        "reachability_pct",
    }
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"Boundary frame is missing columns: {sorted(missing)}")


def wilson_interval(
    successes: int,
    total: int,
    *,
    z: float = 1.959963984540054,
) -> tuple[float, float]:
    """Wilson score interval for a binomial proportion."""
    if total < 1:
        raise ValueError("total must be positive")
    if successes < 0 or successes > total:
        raise ValueError("successes must be between zero and total")

    proportion = successes / total
    denominator = 1.0 + (z * z) / total
    center = (proportion + (z * z) / (2.0 * total)) / denominator
    radius = (
        z
        * sqrt(
            proportion * (1.0 - proportion) / total
            + (z * z) / (4.0 * total * total)
        )
        / denominator
    )
    return max(0.0, center - radius), min(1.0, center + radius)


def pava_nonincreasing(
    values: np.ndarray | list[float],
    weights: np.ndarray | list[float] | None = None,
) -> np.ndarray:
    """Weighted pooled-adjacent-violators fit constrained to be non-increasing."""
    y = np.asarray(values, dtype=float)
    if y.ndim != 1 or y.size == 0:
        raise ValueError("values must be a non-empty one-dimensional sequence")

    if weights is None:
        w = np.ones_like(y, dtype=float)
    else:
        w = np.asarray(weights, dtype=float)
        if w.shape != y.shape:
            raise ValueError("weights must have the same shape as values")
        if np.any(w <= 0):
            raise ValueError("weights must be strictly positive")

    blocks: list[dict[str, float | int]] = []
    for index, (value, weight) in enumerate(zip(y, w, strict=True)):
        blocks.append(
            {
                "start": index,
                "end": index,
                "weighted_sum": float(value * weight),
                "weight": float(weight),
            }
        )

        while len(blocks) >= 2:
            left = blocks[-2]
            right = blocks[-1]
            left_mean = float(left["weighted_sum"]) / float(left["weight"])
            right_mean = float(right["weighted_sum"]) / float(right["weight"])

            if left_mean >= right_mean - 1e-15:
                break

            merged = {
                "start": int(left["start"]),
                "end": int(right["end"]),
                "weighted_sum": float(left["weighted_sum"]) + float(right["weighted_sum"]),
                "weight": float(left["weight"]) + float(right["weight"]),
            }
            blocks[-2:] = [merged]

    fitted = np.empty_like(y, dtype=float)
    for block in blocks:
        block_mean = float(block["weighted_sum"]) / float(block["weight"])
        fitted[int(block["start"]) : int(block["end"]) + 1] = block_mean

    return fitted


def service_probability_curve(
    frame: pd.DataFrame,
    *,
    target_reachability_pct: float = 80.0,
) -> pd.DataFrame:
    """Estimate service probability and Wilson intervals on every grid cell."""
    _required_columns(frame)
    records: list[dict[str, float | int | str]] = []

    grouped = frame.groupby(
        ["algorithm", "responder_count", "severity_control"],
        sort=True,
    )
    for (algorithm, responder_count, severity), group in grouped:
        reachability = pd.to_numeric(
            group["reachability_pct"],
            errors="coerce",
        ).dropna()
        successes = int((reachability >= target_reachability_pct).sum())
        total = int(reachability.size)
        low, high = wilson_interval(successes, total)

        records.append(
            {
                "algorithm": str(algorithm),
                "responder_count": int(responder_count),
                "severity_control": float(severity),
                "n_worlds": total,
                "service_successes": successes,
                "service_probability_pct": successes / total * 100.0,
                "wilson_low_pct": low * 100.0,
                "wilson_high_pct": high * 100.0,
            }
        )

    result = pd.DataFrame.from_records(records)

    fitted_parts: list[pd.DataFrame] = []
    for (_algorithm, _responder_count), group in result.groupby(
        ["algorithm", "responder_count"],
        sort=False,
    ):
        ordered = group.sort_values("severity_control").copy()
        ordered["monotone_service_probability_pct"] = pava_nonincreasing(
            ordered["service_probability_pct"].to_numpy(dtype=float),
            ordered["n_worlds"].to_numpy(dtype=float),
        )
        fitted_parts.append(ordered)

    return pd.concat(fitted_parts, ignore_index=True).sort_values(
        ["algorithm", "responder_count", "severity_control"]
    ).reset_index(drop=True)


def _interpolate_boundary(
    severities: np.ndarray,
    probabilities_pct: np.ndarray,
    *,
    reliability_target_pct: float,
) -> dict[str, float | str | None]:
    if severities.size < 2:
        raise ValueError("At least two severity values are required")

    if probabilities_pct[0] < reliability_target_pct:
        return {
            "boundary_status": "below_grid",
            "boundary_lower_severity": None,
            "boundary_upper_severity": float(severities[0]),
            "boundary_point_estimate": None,
        }

    if probabilities_pct[-1] >= reliability_target_pct:
        return {
            "boundary_status": "above_grid",
            "boundary_lower_severity": float(severities[-1]),
            "boundary_upper_severity": None,
            "boundary_point_estimate": None,
        }

    for index in range(severities.size - 1):
        left_probability = probabilities_pct[index]
        right_probability = probabilities_pct[index + 1]

        if left_probability >= reliability_target_pct > right_probability:
            left_severity = float(severities[index])
            right_severity = float(severities[index + 1])

            if abs(left_probability - reliability_target_pct) < 1e-15:
                point = left_severity
            else:
                fraction = (
                    (left_probability - reliability_target_pct)
                    / (left_probability - right_probability)
                )
                point = left_severity + fraction * (right_severity - left_severity)

            return {
                "boundary_status": "within_grid",
                "boundary_lower_severity": left_severity,
                "boundary_upper_severity": right_severity,
                "boundary_point_estimate": float(point),
            }

    raise RuntimeError("Could not locate a reliability boundary on a monotone curve")


def boundary_estimates(
    frame: pd.DataFrame,
    *,
    target_reachability_pct: float = 80.0,
    reliability_target_pct: float = 80.0,
    bootstrap_resamples: int = 5000,
    seed: int = 7070,
) -> pd.DataFrame:
    """Estimate the 80/80-style boundary with a world-level cluster bootstrap.

    Each bootstrap resamples stochastic worlds, preserving the coupled severity
    trajectory inside each world. Empirical service probabilities are projected
    onto a non-increasing curve with weighted PAVA before interpolation.
    """
    _required_columns(frame)
    if bootstrap_resamples < 1:
        raise ValueError("bootstrap_resamples must be positive")

    records: list[dict[str, float | int | str | None]] = []

    grouped = frame.groupby(["algorithm", "responder_count"], sort=True)
    for group_index, ((algorithm, responder_count), group) in enumerate(grouped):
        pivot = group.pivot_table(
            index="seed",
            columns="severity_control",
            values="reachability_pct",
            aggfunc="first",
        ).sort_index(axis=1)

        if pivot.empty or pivot.shape[1] < 2:
            continue

        severities = pivot.columns.to_numpy(dtype=float)
        service = (pivot.to_numpy(dtype=float) >= target_reachability_pct).astype(float)
        raw_probabilities = service.mean(axis=0) * 100.0
        fitted_probabilities = pava_nonincreasing(raw_probabilities)

        estimate = _interpolate_boundary(
            severities,
            fitted_probabilities,
            reliability_target_pct=reliability_target_pct,
        )

        rng = np.random.default_rng(seed + group_index * 100_003)
        finite_bootstrap: list[float] = []
        below_grid = 0
        above_grid = 0

        for _ in range(bootstrap_resamples):
            sampled_indices = rng.integers(0, service.shape[0], size=service.shape[0])
            bootstrap_probabilities = service[sampled_indices].mean(axis=0) * 100.0
            fitted_bootstrap = pava_nonincreasing(bootstrap_probabilities)
            bootstrap_estimate = _interpolate_boundary(
                severities,
                fitted_bootstrap,
                reliability_target_pct=reliability_target_pct,
            )
            status = bootstrap_estimate["boundary_status"]

            if status == "within_grid":
                finite_bootstrap.append(
                    float(bootstrap_estimate["boundary_point_estimate"])
                )
            elif status == "below_grid":
                below_grid += 1
            else:
                above_grid += 1

        if finite_bootstrap:
            bootstrap_array = np.asarray(finite_bootstrap, dtype=float)
            ci_low = float(np.quantile(bootstrap_array, 0.025))
            ci_high = float(np.quantile(bootstrap_array, 0.975))
            bootstrap_median = float(np.median(bootstrap_array))
        else:
            ci_low = None
            ci_high = None
            bootstrap_median = None

        records.append(
            {
                "algorithm": str(algorithm),
                "responder_count": int(responder_count),
                "n_worlds": int(service.shape[0]),
                "target_reachability_pct": float(target_reachability_pct),
                "reliability_target_pct": float(reliability_target_pct),
                **estimate,
                "bootstrap_resamples": int(bootstrap_resamples),
                "bootstrap_finite_fraction": len(finite_bootstrap) / bootstrap_resamples,
                "bootstrap_below_grid_fraction": below_grid / bootstrap_resamples,
                "bootstrap_above_grid_fraction": above_grid / bootstrap_resamples,
                "bootstrap_boundary_median": bootstrap_median,
                "bootstrap_ci_low": ci_low,
                "bootstrap_ci_high": ci_high,
            }
        )

    return pd.DataFrame.from_records(records)


def world_service_thresholds(
    frame: pd.DataFrame,
    *,
    target_reachability_pct: float = 80.0,
) -> pd.DataFrame:
    """Describe each stochastic world's pass/fail transition across severity."""
    _required_columns(frame)
    records: list[dict[str, float | int | str | bool | None]] = []

    grouped = frame.groupby(
        ["algorithm", "responder_count", "seed"],
        sort=True,
    )
    for (algorithm, responder_count, seed), group in grouped:
        ordered = group.sort_values("severity_control")
        severities = ordered["severity_control"].to_numpy(dtype=float)
        service = (
            ordered["reachability_pct"].to_numpy(dtype=float)
            >= target_reachability_pct
        )

        passing = severities[service]
        failing = severities[~service]
        monotonicity_violations = int(np.sum(np.diff(service.astype(int)) > 0))

        records.append(
            {
                "algorithm": str(algorithm),
                "responder_count": int(responder_count),
                "seed": int(seed),
                "last_passing_severity": (
                    None if passing.size == 0 else float(passing.max())
                ),
                "first_failing_severity": (
                    None if failing.size == 0 else float(failing.min())
                ),
                "service_transition_monotonic": monotonicity_violations == 0,
                "service_transition_violations": monotonicity_violations,
            }
        )

    return pd.DataFrame.from_records(records)


def monotonicity_audit(frame: pd.DataFrame) -> pd.DataFrame:
    """Audit the coupled design at both the failure-field and service levels."""
    _required_columns(frame)
    records: list[dict[str, float | int | str | None]] = []

    edge_required = {"failed_directed_edges"}
    if edge_required.issubset(frame.columns):
        edge_frame = frame[
            ["seed", "severity_control", "failed_directed_edges"]
        ].drop_duplicates()

        transitions = 0
        violations = 0
        worlds = 0
        for _seed, group in edge_frame.groupby("seed", sort=True):
            values = group.sort_values("severity_control")[
                "failed_directed_edges"
            ].to_numpy(dtype=float)
            transitions += max(0, values.size - 1)
            violations += int(np.sum(np.diff(values) < 0))
            worlds += 1

        records.append(
            {
                "audit_type": "failed_edge_count_non_decreasing",
                "algorithm": None,
                "responder_count": None,
                "worlds": worlds,
                "transitions": transitions,
                "violations": violations,
                "violation_rate_pct": (
                    0.0 if transitions == 0 else violations / transitions * 100.0
                ),
            }
        )

    grouped = frame.groupby(["algorithm", "responder_count"], sort=True)
    for (algorithm, responder_count), group in grouped:
        transitions = 0
        violations = 0
        worlds = 0

        for _seed, world in group.groupby("seed", sort=True):
            values = world.sort_values("severity_control")[
                "reachability_pct"
            ].to_numpy(dtype=float)
            transitions += max(0, values.size - 1)
            violations += int(np.sum(np.diff(values) > 1e-12))
            worlds += 1

        records.append(
            {
                "audit_type": "reachability_non_increasing",
                "algorithm": str(algorithm),
                "responder_count": int(responder_count),
                "worlds": worlds,
                "transitions": transitions,
                "violations": violations,
                "violation_rate_pct": (
                    0.0 if transitions == 0 else violations / transitions * 100.0
                ),
            }
        )

    return pd.DataFrame.from_records(records)
