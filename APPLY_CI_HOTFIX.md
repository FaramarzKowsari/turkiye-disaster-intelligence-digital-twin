# CI lint hotfix

This patch fixes the three Ruff lint failures from commit:

`Complete research-grade starter scaffold`

Changes:
- sort standard-library imports in `cli.py`;
- import `Hashable` from `collections.abc` in `baselines.py`;
- import `Hashable` and `Iterable` from `collections.abc` in `scenario.py`.

Apply:
1. Extract this ZIP into the repository root and allow replacement of the three files.
2. Open GitHub Desktop.
3. Commit with:
   `Fix Ruff lint errors in starter scaffold`
4. Push origin.
5. GitHub Actions should start automatically.
