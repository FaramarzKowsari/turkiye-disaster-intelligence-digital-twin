# Apply live-data milestone with GitHub Desktop

1. Extract this ZIP directly into the repository root.
2. Allow replacement of:
   - `app/streamlit_app.py`
   - `pyproject.toml`
   - `.github/workflows/ci.yml`
   - `src/turkiye_disaster_twin/data/afad.py`
   - `src/turkiye_disaster_twin/data/osm.py`
3. Open GitHub Desktop.
4. Commit with:

   `Add live AFAD and OSM digital twin data layer`

5. Push origin.
6. Wait for CI to turn green.

New scientific functionality:

- AFAD event normalisation
- district-scale İstanbul OSM road graph
- OSM hospital/clinic/fire-station layer
- MapLibre/Plotly live map
- trilingual Streamlit interface preserved
- author photo and biography preserved
- unit tests for event schema and graph visualisation

No API key is required.
