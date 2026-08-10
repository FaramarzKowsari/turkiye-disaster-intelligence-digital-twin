# Multilingual branding patch

This patch introduces the permanent public-facing project identity.

## Included

- README in English, Turkish and Spanish (Spain)
- author photo and biography in README
- multilingual GitHub Pages site under `docs/`
- multilingual Streamlit deployment shell under `app/`
- author photo and biography on Pages and Streamlit
- Schema.org author metadata
- official profile links
- Streamlit optional dependency and deployment requirements

## Apply with GitHub Desktop

1. Extract this ZIP directly into the repository root.
2. Allow Windows to replace `README.md` and `pyproject.toml`.
3. Open GitHub Desktop.
4. Review the changes.
5. Commit with:

   `Add multilingual author-branded public interfaces`

6. Push origin.
7. Wait for CI to turn green.

## Enable GitHub Pages

After the push:

1. GitHub repository → **Settings**
2. **Pages**
3. Source: **Deploy from a branch**
4. Branch: `main`
5. Folder: `/docs`
6. Save

Expected public URL:

`https://faramarzkowsari.github.io/turkiye-disaster-intelligence-digital-twin/`

## Streamlit deployment

After the repository is stable, deploy:

`app/streamlit_app.py`

The application does not require a paid AI API key.
