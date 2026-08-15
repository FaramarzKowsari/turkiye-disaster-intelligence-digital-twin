OSF DOI INTEGRATION PATCH
==========================

Purpose
-------
Integrates the accepted OSF Registration DOI:
10.17605/OSF.IO/ZTJXK

into the existing Türkiye Disaster Intelligence Digital Twin repository.

How to use
----------
1. Download and extract this ZIP.
2. Copy/extract its contents into the ROOT of:
   turkiye-disaster-intelligence-digital-twin
   (the same folder that contains README.md)
3. Double-click:
   APPLY_OSF_DOI_UPDATE.bat
4. Wait for the green SUCCESS message.
5. Open GitHub Desktop.
6. Review the changed files.
7. Commit message:
   Add accepted OSF registration DOI and open-science record
8. Push origin.
9. Wait for GitHub Pages deployment to turn green.

Files patched
-------------
README.md
CITATION.cff
ABOUT.md
REPRODUCIBILITY.md
docs/index.html
docs/project.html
docs/research-findings.html
docs/sitemap.xml

Files added
-----------
OSF_REGISTRATION.md
docs/osf-registration.html

The patch is idempotent: if the DOI is already present, it will not add duplicate entries.
It validates required anchors before writing, so it should not partially modify the repository if the current file structure differs.
