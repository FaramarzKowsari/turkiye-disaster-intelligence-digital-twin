# Apply DOI + Project Documentation Update

This is a documentation-only update after the v1.0.0 research release. It does **not** modify the frozen scientific results.

## What changes

- Adds the Zenodo DOI badge and persistent identifiers throughout `README.md`.
- Updates `CITATION.cff` with the v1.0.0 DOI and Concept DOI.
- Adds a complete trilingual `ABOUT.md`.
- Upgrades the GitHub Pages `docs/index.html` landing page.
- Adds a detailed trilingual `docs/project.html` page covering architecture, data, methods, experiments, results, reproducibility, limitations and citation.
- Adds DOI metadata and links to `docs/research-findings.html`.
- Extends the site CSS and sitemap.
- Adds DOI references to `RELEASE_NOTES.md`, `REPRODUCIBILITY.md`, `ARCHITECTURE.md` and `CHANGELOG.md`.
- Includes exact values for the GitHub repository sidebar About settings in `GITHUB_ABOUT_SETTINGS.md`.

## Persistent identifiers

- Version DOI v1.0.0: `10.5281/zenodo.21903851`
- Concept DOI, all versions: `10.5281/zenodo.21903850`

## Apply

1. Extract this ZIP directly into the repository root.
2. Allow replacement of the existing files.
3. Open GitHub Desktop.
4. Review the changes.
5. Commit with:

   `Add DOI metadata and complete project documentation`

6. Push origin.
7. Wait for CI and GitHub Pages deployment to turn green.
8. In GitHub repository → **Code**, click the gear icon beside **About** and apply the values in `GITHUB_ABOUT_SETTINGS.md`.

The existing GitHub tag and Zenodo archive for v1.0.0 remain immutable; this update enriches the live repository and project website with the DOI minted after the release.
