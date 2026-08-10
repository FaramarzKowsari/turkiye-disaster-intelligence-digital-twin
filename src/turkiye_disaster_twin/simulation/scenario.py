from __future__ import annotations

from collections.abc import Hashable, Iterable
from dataclasses import dataclass
from random import Random


@dataclass(frozen=True)
class EdgeRisk:
    edge_id: Hashable
    failure_probability: float


def sample_failed_edges(
    risks: Iterable[EdgeRisk],
    *,
    seed: int,
) -> set[Hashable]:
    """Sample synthetic road failures for a controlled experimental scenario.

    This is explicitly a scenario generator, not a real earthquake damage model.
    """
    rng = Random(seed)
    failed: set[Hashable] = set()

    for risk in risks:
        p = min(max(risk.failure_probability, 0.0), 1.0)
        if rng.random() < p:
            failed.add(risk.edge_id)

    return failed
