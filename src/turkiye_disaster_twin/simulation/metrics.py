from __future__ import annotations

from dataclasses import asdict, dataclass
from statistics import mean, median

import numpy as np

from turkiye_disaster_twin.simulation.baselines import Assignment
from turkiye_disaster_twin.simulation.scenario import Incident


@dataclass(frozen=True)
class ResponseMetrics:
    incidents: int
    assigned: int
    unreachable: int
    reachability_pct: float
    mean_response_s: float | None
    median_response_s: float | None
    p90_response_s: float | None
    total_response_s: float
    weighted_unmet_demand: int

    def to_dict(self) -> dict[str, int | float | None]:
        return asdict(self)


def response_metrics(
    assignments: list[Assignment],
    incidents: list[Incident],
) -> ResponseMetrics:
    """Calculate snapshot response metrics without inventing operational meaning."""
    assigned_nodes = {assignment.incident for assignment in assignments}
    times = [float(assignment.travel_time) for assignment in assignments]

    unreachable_incidents = [
        incident for incident in incidents if incident.node not in assigned_nodes
    ]
    total = len(incidents)
    assigned = len(assigned_nodes)

    return ResponseMetrics(
        incidents=total,
        assigned=assigned,
        unreachable=total - assigned,
        reachability_pct=0.0 if total == 0 else 100.0 * assigned / total,
        mean_response_s=None if not times else float(mean(times)),
        median_response_s=None if not times else float(median(times)),
        p90_response_s=None if not times else float(np.percentile(times, 90)),
        total_response_s=float(sum(times)),
        weighted_unmet_demand=sum(incident.severity for incident in unreachable_incidents),
    )
