# v0.4 CI import-order hotfix

GitHub Actions reported one Ruff import-order error in:

`src/turkiye_disaster_twin/research/artifacts.py`

This patch only reorders standard-library imports. No statistical or artifact
generation logic changes.

Commit message:

`Fix v0.4 research artifact import order`
