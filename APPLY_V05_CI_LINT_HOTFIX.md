# v0.5 CI lint hotfix

This patch cleans the four Ruff issues reported after the v0.5 phase-transition commit.

Changes are intentionally non-algorithmic:

- removes the unused `Incident` import from `phase_transition.py`;
- removes redundant integer casts where the values are already integers;
- sorts the standard-library imports in `run_phase_transition_benchmark.py`;
- removes the unused `networkx` import from `tests/test_phase_transition.py`.

Apply to the repository root and commit with:

`Fix v0.5 phase-transition CI lint errors`

Then push to `main`.
