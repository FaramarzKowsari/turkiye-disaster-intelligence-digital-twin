# Monte Carlo Experiment Lab — v0.3

## Research objective

The v0.3 milestone moves the project from a single synthetic snapshot to a matched experimental
framework. The purpose is to measure how dispatch policies behave across repeated uncertainty, not
to select an algorithm from one visually attractive scenario.

## Paired design

For each disruption severity and random seed, both algorithms receive exactly the same:

- sampled directed road interruptions,
- synthetic emergency incidents,
- incident severities,
- responder locations,
- road graph and travel-time weights.

This makes algorithm differences paired within each stochastic realisation.

## Algorithms

- `greedy`: sequential nearest-unused-responder baseline.
- `global_min_cost`: maximum-cardinality minimum-cost snapshot assignment.

## Raw experiment schema

Each algorithm/scenario row contains:

- severity control,
- realisation index,
- seed,
- algorithm,
- failed directed-edge count,
- incident and responder counts,
- assigned and unreachable incidents,
- reachability percentage,
- mean / median / p90 response time,
- total response time,
- severity-weighted unmet demand.

## Uncertainty summary

The first research release reports an **approximate 95% confidence interval for the mean** using:

`mean ± 1.96 × sample_standard_deviation / sqrt(n)`

This is deliberately labelled approximate. A later paper-grade milestone can introduce bootstrap,
hierarchical models or other inference methods while retaining the same raw experiment table.

## Paired comparison

For cost-like metrics such as total response time, the experiment layer computes:

`greedy_minus_global = greedy_metric - global_metric`

Positive values favour the global assignment. The summary reports the mean paired difference,
approximate 95% interval and the percentage of matched realisations in which Global is lower.

## Public deployment limits

The Streamlit interface caps the number of realisations per severity to protect the hosted app from
long graph-routing workloads. This is a deployment constraint, not a limitation of the experiment
engine.

## Scientific boundary

All disruption and incident-demand layers remain synthetic stress tests. They are not official
damage forecasts, engineering fragility assessments, casualty estimates or operational routing
recommendations.
