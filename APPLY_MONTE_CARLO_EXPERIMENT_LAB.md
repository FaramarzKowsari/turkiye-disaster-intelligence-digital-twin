# Monte Carlo Experiment Lab — v0.3

This patch adds the first repeated-experiment layer to the Türkiye Disaster
Intelligence Digital Twin.

## New research capabilities

- matched Monte Carlo realisations,
- multiple disruption-severity levels,
- identical stochastic scenarios for Greedy and Global algorithms,
- raw realisation-level result table,
- approximate 95% confidence intervals for mean metrics,
- paired Greedy-minus-Global comparisons,
- Global win-rate summaries,
- P90 response sensitivity curves,
- CSV download for Power BI, Tableau, R, Python or spreadsheet analysis,
- trilingual Streamlit Experiment Lab,
- trilingual README and GitHub Pages update,
- author branding preserved.

## Scientific boundary

The network-disruption and incident-demand layers remain synthetic stress tests.
They are not official damage forecasts, engineering fragility assessments,
casualty estimates or operational emergency-routing recommendations.

## Apply with GitHub Desktop

1. Extract this ZIP directly into the repository root.
2. Allow Windows to replace:
   - `app/streamlit_app.py`
   - `README.md`
   - `docs/index.html`
3. New files will also be added under:
   - `src/turkiye_disaster_twin/simulation/experiment.py`
   - `tests/test_experiment.py`
   - `docs/experiment_lab.md`
4. Open GitHub Desktop.
5. Commit with:

   `Add Monte Carlo experiment lab and uncertainty analysis`

6. Push origin.
7. Wait for CI and GitHub Pages.

## Local validation performed before packaging

- Python compile: PASS
- Full test suite: 15 passed

The public Streamlit UI intentionally caps realisations per severity to keep
hosted graph-routing workloads responsive. The experiment engine itself is not
restricted to that UI limit.
