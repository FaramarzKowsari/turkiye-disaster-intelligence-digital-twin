# Paper-Grade Experiment Pipeline — v0.4

## Purpose

v0.4 separates the lightweight public Streamlit experience from large, reproducible research
campaigns. The normal CI remains fast; large benchmarks are launched explicitly through the
**Research Benchmark** GitHub Actions workflow.

## Statistical design

Each random seed defines a matched synthetic scenario. Greedy and Global Minimum-Cost Assignment
are evaluated on the same disrupted road graph, incident set and responder placement.

For cost-like metrics, the principal paired quantity is:

`delta = Greedy - Global`

Positive delta means the global method achieved a lower cost.

The pipeline reports:

- mean paired difference,
- median paired difference,
- percentile bootstrap confidence interval for the mean difference,
- two-sided paired sign-flip permutation p-value,
- Holm-adjusted p-value across severities within a metric,
- paired effect size `d_z`,
- global-method win rate,
- tie rate.

## Why bootstrap and permutation inference

The earlier v0.3 confidence intervals used a normal approximation. v0.4 keeps those exploratory
summaries but adds resampling-based inference that does not require a normality assumption for
the paired difference distribution.

## Reproducibility bundle

Every Research Benchmark run produces:

- `raw_experiments.csv`
- `raw_experiments.parquet`
- `exploratory_summary.csv`
- `exploratory_summary.parquet`
- `paired_inference.csv`
- `paired_inference.parquet`
- `manifest.json`
- `SHA256SUMS`

The manifest records experiment inputs, random seed, software/runtime metadata and GitHub run
identifiers when available.

## Running on GitHub

Go to:

**Actions → Research Benchmark → Run workflow**

Choose:

- pilot district,
- 100 / 500 / 1000 realisations per severity,
- severity values,
- incident and responder counts,
- base seed.

When the workflow finishes, download the generated artifact from the workflow run.

## Scientific boundary

This pipeline evaluates a controlled stochastic network stress test. The synthetic edge
disruptions are not certified road-damage probabilities, the incident layer is not a casualty
forecast, and the output is not an official emergency-routing recommendation.
