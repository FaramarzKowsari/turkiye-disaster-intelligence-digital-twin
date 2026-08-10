# Scenario engine CI hotfix

Fixes the two Ruff errors reported by GitHub Actions:

1. Removes the unused `incident_map` local variable from `metrics.py`.
2. Removes the unnecessary `int(...)` wrapper around `nx.maximum_flow_value(...)`
   in `baselines.py`.

Apply to the repository root, then commit with:

`Fix scenario engine CI lint errors`

and push to `main`.
