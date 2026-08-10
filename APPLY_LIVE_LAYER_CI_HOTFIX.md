# Live data layer CI hotfix

This patch fixes all three Ruff errors reported by GitHub Actions:

1. Formats the long OSM import block.
2. Uses `datetime.UTC` instead of `timezone.utc`.
3. Keeps the intentionally broad exception handler only at the public Streamlit UI boundary,
   with a documented `# noqa: BLE001`.

## Apply

1. Extract this ZIP into the repository root.
2. Replace `app/streamlit_app.py`.
3. Open GitHub Desktop.
4. Commit with:

   `Fix live data layer CI lint errors`

5. Push origin.
