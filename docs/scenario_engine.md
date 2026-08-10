# Monte Carlo Post-Earthquake Scenario Engine — v0.2

## Scientific purpose

This milestone introduces a controlled stochastic stress-test environment for comparing
emergency-routing policies under identical network disruptions.

It is **not** an earthquake damage model.

## Scenario mechanics

For each road edge, the simulator calculates a transparent probability:

`p(edge failure) = severity_control × exp(-distance_to_scenario_centre / decay_km)`

The probability is intentionally simple and auditable. It will later be replaced or calibrated
with defensible hazard/vulnerability evidence if suitable data are available.

## Reproducibility

Each scenario records:

- random seed,
- disruption severity control,
- distance decay,
- incident count,
- responder count,
- sampled directed-edge failures.

The exact same seed and graph can reproduce the same synthetic realisation.

## Baselines

### B0 — Sequential greedy nearest responder
Incidents are processed in order and assigned to the nearest unused reachable responder.

### B1 — Global minimum-cost assignment
All reachable responder-to-incident path costs are calculated. A maximum-cardinality,
minimum-cost flow then finds a globally efficient one-to-one snapshot assignment.

The second method is not assumed to be superior. Results are measured.

## Metrics

- assigned incidents
- unreachable incidents
- reachability percentage
- mean response time
- median response time
- p90 response time
- total response time
- severity-weighted unmet demand

## Next milestone

Run many seeds and severity levels to create confidence intervals and sensitivity curves,
then introduce capacity, repeated dispatch, hospital constraints and district-level fairness.
