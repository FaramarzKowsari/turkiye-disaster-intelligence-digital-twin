# Scenario engine CI hotfix — final lint issue

GitHub Actions reports one remaining Ruff rule:

`RUF046 Value being cast to int is already an integer`

The fix changes:

`weight=max(0, int(round(cost * 1000)))`

to:

`weight=max(0, round(cost * 1000))`

No algorithmic behaviour changes: `round(x)` without `ndigits` already returns an integer.

## Apply

Extract into the repository root and replace:

`src/turkiye_disaster_twin/simulation/baselines.py`

Commit message:

`Fix final scenario engine Ruff lint issue`

Then push to `main`.
