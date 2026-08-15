from __future__ import annotations

from pathlib import Path
import re
import shutil
import sys
from datetime import datetime

OSF_DOI = "10.17605/OSF.IO/ZTJXK"
OSF_URL = "https://doi.org/10.17605/OSF.IO/ZTJXK"
OSF_RECORD = "https://osf.io/ztjxk"
OSF_PROJECT = "https://osf.io/2r4cv"

ZENODO_VERSION = "10.5281/zenodo.21903851"
ZENODO_CONCEPT = "10.5281/zenodo.21903850"

PATCH_ROOT = Path(__file__).resolve().parent

def find_repo_root() -> Path:
    candidates = [PATCH_ROOT, Path.cwd()]
    for c in candidates:
        if (c / "README.md").exists() and (c / "docs").is_dir():
            return c.resolve()
    print("ERROR: Repository root not found.")
    print("Extract this ZIP into the repository root — the folder that contains README.md — then run APPLY_OSF_DOI_UPDATE.bat again.")
    sys.exit(2)

ROOT = find_repo_root()

FILES = {
    "README.md": ROOT / "README.md",
    "CITATION.cff": ROOT / "CITATION.cff",
    "ABOUT.md": ROOT / "ABOUT.md",
    "REPRODUCIBILITY.md": ROOT / "REPRODUCIBILITY.md",
    "docs/index.html": ROOT / "docs" / "index.html",
    "docs/project.html": ROOT / "docs" / "project.html",
    "docs/research-findings.html": ROOT / "docs" / "research-findings.html",
    "docs/sitemap.xml": ROOT / "docs" / "sitemap.xml",
}

missing = [name for name, path in FILES.items() if not path.exists()]
if missing:
    print("ERROR: Required repository files are missing:")
    for m in missing:
        print("  -", m)
    print("No repository files were modified.")
    sys.exit(3)

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")

def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"{label}: required anchor not found")
    return text.replace(old, new, 1)

def regex_sub_once(text: str, pattern: str, repl: str, label: str, flags=0) -> str:
    new, n = re.subn(pattern, repl, text, count=1, flags=flags)
    if n != 1:
        raise RuntimeError(f"{label}: required pattern not found")
    return new

pending: dict[Path, str] = {}
notes: list[str] = []

# ---------------- README.md ----------------
path = FILES["README.md"]
text = read(path)
if OSF_DOI not in text:
    # Badge after Zenodo badge.
    badge_pattern = (
        r'(?P<block>  <a href="https://doi\.org/10\.5281/zenodo\.21903850">\s*'
        r'<img alt="DOI" src="https://img\.shields\.io/badge/DOI-10\.5281%2Fzenodo\.21903850-blue\.svg">\s*'
        r'</a>)'
    )
    osf_badge = (
        '\n  <a href="https://doi.org/10.17605/OSF.IO/ZTJXK">\n'
        '    <img alt="OSF Registration DOI" '
        'src="https://img.shields.io/badge/OSF%20Registration-10.17605%2FOSF.IO%2FZTJXK-2D6A4F.svg">\n'
        '  </a>'
    )
    text = regex_sub_once(text, badge_pattern, r'\g<block>' + osf_badge, "README badge", re.S)

    nav = '  <a href="https://doi.org/10.5281/zenodo.21903851">Zenodo v1.0.0</a>'
    text = replace_once(
        text, nav,
        nav + ' ·\n  <a href="https://doi.org/10.17605/OSF.IO/ZTJXK">OSF Registration</a>',
        "README navigation"
    )

    # Add OSF identifier after the three language-specific Concept DOI list items.
    concept_lines = [
        '- **Concept DOI (all versions):** [10.5281/zenodo.21903850](https://doi.org/10.5281/zenodo.21903850)',
        "- **Concept DOI (tüm sürümler):** [10.5281/zenodo.21903850](https://doi.org/10.5281/zenodo.21903850)",
        "- **Concept DOI (todas las versiones):** [10.5281/zenodo.21903850](https://doi.org/10.5281/zenodo.21903850)",
    ]
    additions = [
        f"- **OSF Registration DOI (accepted retrospective Open-Ended Registration):** [{OSF_DOI}]({OSF_URL})",
        f"- **OSF Registration DOI (kabul edilmiş retrospektif Open-Ended Registration):** [{OSF_DOI}]({OSF_URL})",
        f"- **DOI del registro OSF (registro abierto retrospectivo aceptado):** [{OSF_DOI}]({OSF_URL})",
    ]
    for anchor, addition in zip(concept_lines, additions):
        text = replace_once(text, anchor, anchor + "\n" + addition, "README persistent identifiers")

    citation_concept = '**Concept DOI:** [10.5281/zenodo.21903850](https://doi.org/10.5281/zenodo.21903850)  '
    text = replace_once(
        text, citation_concept,
        citation_concept + f"\n**OSF Registration DOI:** [{OSF_DOI}]({OSF_URL})  ",
        "README citation DOI"
    )

    citation_intro = "Please use [`CITATION.cff`](CITATION.cff) for machine-readable citation metadata."
    text = replace_once(
        text, citation_intro,
        citation_intro + f" The research methodology and provenance are additionally preserved in an accepted retrospective [Open-Ended OSF Registration]({OSF_URL}).",
        "README citation intro"
    )
    notes.append("README.md")
pending[path] = text

# ---------------- CITATION.cff ----------------
path = FILES["CITATION.cff"]
text = read(path)
if OSF_DOI not in text:
    old_message = (
        'message: "If you use this software or its research results, cite the frozen v1.0.0 release '
        'with DOI 10.5281/zenodo.21903851. Use the Concept DOI 10.5281/zenodo.21903850 when referring '
        'to the project across versions."'
    )
    new_message = (
        'message: "If you use this software or its research results, cite the frozen v1.0.0 release '
        'with DOI 10.5281/zenodo.21903851. Use the Concept DOI 10.5281/zenodo.21903850 when referring '
        'to the project across versions. The accepted retrospective Open-Ended OSF Registration '
        'documenting methodology and provenance is DOI 10.17605/OSF.IO/ZTJXK."'
    )
    text = replace_once(text, old_message, new_message, "CITATION message")

    concept_block = (
        '  - type: doi\n'
        '    value: 10.5281/zenodo.21903850\n'
        '    description: "Concept DOI representing all versions of the project"'
    )
    osf_block = (
        '\n  - type: doi\n'
        '    value: 10.17605/OSF.IO/ZTJXK\n'
        '    description: "Accepted retrospective Open-Ended OSF Registration documenting research methodology and provenance"'
    )
    text = replace_once(text, concept_block, concept_block + osf_block, "CITATION identifiers")

    keyword = "  - network reliability"
    text = replace_once(text, keyword, keyword + "\n  - open science", "CITATION keywords")

    abstract_end = "  world-cluster bootstrap inference."
    text = replace_once(
        text, abstract_end,
        abstract_end
        + "\n  The methodology and provenance are additionally preserved in an accepted retrospective"
        + "\n  Open-Ended OSF Registration (DOI 10.17605/OSF.IO/ZTJXK).",
        "CITATION abstract"
    )
    notes.append("CITATION.cff")
pending[path] = text

# ---------------- ABOUT.md ----------------
path = FILES["ABOUT.md"]
text = read(path)
if OSF_DOI not in text:
    en = "- **Concept DOI — all versions:** https://doi.org/10.5281/zenodo.21903850"
    text = replace_once(text, en, en + f"\n- **Accepted OSF Registration DOI:** {OSF_URL}", "ABOUT English DOI")

    current = "### Current scientific release"
    osf_section = (
        "### Open Science registration\n\n"
        "The completed research design, computational methodology, estimands, inferential procedures "
        "and provenance are preserved in an **accepted retrospective Open-Ended OSF Registration**. "
        "It documents an already completed computational investigation and must not be interpreted "
        "as a preregistration.\n\n"
        f"- **Registration DOI:** {OSF_URL}\n"
        f"- **OSF record:** {OSF_RECORD}\n"
        f"- **Associated OSF project:** {OSF_PROJECT}\n\n"
    )
    text = replace_once(text, current, osf_section + current, "ABOUT OSF section")

    tr = "- **Tüm sürümler için Concept DOI:** https://doi.org/10.5281/zenodo.21903850"
    text = replace_once(text, tr, tr + f"\n- **Kabul edilmiş OSF Registration DOI:** {OSF_URL}", "ABOUT Turkish DOI")

    es = "- **Concept DOI para todas las versiones:** https://doi.org/10.5281/zenodo.21903850"
    text = replace_once(text, es, es + f"\n- **DOI del registro OSF aceptado:** {OSF_URL}", "ABOUT Spanish DOI")
    notes.append("ABOUT.md")
pending[path] = text

# ---------------- REPRODUCIBILITY.md ----------------
path = FILES["REPRODUCIBILITY.md"]
text = read(path)
if OSF_DOI not in text:
    anchor = "versions of the research software record."
    addition = (
        "\n\nThe completed methodology and provenance are also archived in an **accepted retrospective\n"
        f"Open-Ended OSF Registration**, DOI **[{OSF_DOI}]({OSF_URL})**. This registration formalizes\n"
        "the already completed computational research cycle and is not a preregistration."
    )
    text = replace_once(text, anchor, anchor + addition, "REPRODUCIBILITY OSF paragraph")
    notes.append("REPRODUCIBILITY.md")
pending[path] = text

# ---------------- docs/index.html ----------------
path = FILES["docs/index.html"]
text = read(path)
if OSF_DOI not in text:
    concept_json = '      "https://doi.org/10.5281/zenodo.21903850"'
    text = replace_once(
        text, concept_json,
        concept_json + ',\n      "https://doi.org/10.17605/OSF.IO/ZTJXK"',
        "index JSON-LD"
    )

    version_button = '<a class="button" href="https://doi.org/10.5281/zenodo.21903851">DOI v1.0.0</a>'
    text = replace_once(
        text, version_button,
        version_button + '\n        <a class="button" href="https://doi.org/10.17605/OSF.IO/ZTJXK">OSF Registration DOI</a>',
        "index OSF button"
    )

    concept_span = (
        '<span data-en="Concept DOI 10.5281/zenodo.21903850 represents the project across all versions." '
        'data-tr="Concept DOI 10.5281/zenodo.21903850 projenin tüm sürümlerini temsil eder." '
        'data-es="Concept DOI 10.5281/zenodo.21903850 representa el proyecto a través de todas sus versiones.">'
        'Concept DOI 10.5281/zenodo.21903850 represents the project across all versions.</span>'
    )
    osf_span = '<span><a href="https://doi.org/10.17605/OSF.IO/ZTJXK">Accepted retrospective OSF Registration · 10.17605/OSF.IO/ZTJXK</a></span>'
    text = replace_once(text, concept_span, concept_span + "\n      " + osf_span, "index DOI banner")

    old_footer = (
        '<footer><div class="wrap footer-grid"><span>Türkiye Disaster Intelligence Digital Twin · v1.0.0 · Faramarz Kowsari</span>'
        '<a href="https://doi.org/10.5281/zenodo.21903851">DOI 10.5281/zenodo.21903851</a></div></footer>'
    )
    new_footer = (
        '<footer><div class="wrap footer-grid"><span>Türkiye Disaster Intelligence Digital Twin · v1.0.0 · Faramarz Kowsari</span>'
        '<span><a href="https://doi.org/10.5281/zenodo.21903851">Zenodo DOI</a> · '
        '<a href="https://doi.org/10.17605/OSF.IO/ZTJXK">OSF Registration DOI</a></span></div></footer>'
    )
    text = replace_once(text, old_footer, new_footer, "index footer")
    notes.append("docs/index.html")
pending[path] = text

# ---------------- docs/project.html ----------------
path = FILES["docs/project.html"]
text = read(path)
if OSF_DOI not in text:
    concept_json = '      "https://doi.org/10.5281/zenodo.21903850"'
    text = replace_once(
        text, concept_json,
        concept_json + ',\n      "https://doi.org/10.17605/OSF.IO/ZTJXK"',
        "project JSON-LD"
    )

    concept_button_start = '<a class="button" href="https://doi.org/10.5281/zenodo.21903850"'
    text = replace_once(
        text, concept_button_start,
        '<a class="button" href="https://doi.org/10.17605/OSF.IO/ZTJXK">Accepted OSF Registration</a>\n        ' + concept_button_start,
        "project OSF button"
    )

    doi_strong = '<strong>v1.0.0 DOI · 10.5281/zenodo.21903851</strong>'
    text = replace_once(
        text, doi_strong,
        doi_strong + '\n      <strong><a href="https://doi.org/10.17605/OSF.IO/ZTJXK">OSF Registration DOI · 10.17605/OSF.IO/ZTJXK</a></strong>',
        "project DOI banner"
    )
    notes.append("docs/project.html")
pending[path] = text

# ---------------- docs/research-findings.html ----------------
path = FILES["docs/research-findings.html"]
text = read(path)
if OSF_DOI not in text:
    old_links = (
        '<div class="page-links"><a href="project.html" data-en="Full project" data-tr="Tam proje" '
        'data-es="Proyecto completo">Full project</a><a href="https://doi.org/10.5281/zenodo.21903851">DOI</a></div>'
    )
    new_links = (
        '<div class="page-links"><a href="project.html" data-en="Full project" data-tr="Tam proje" '
        'data-es="Proyecto completo">Full project</a><a href="https://doi.org/10.5281/zenodo.21903851">Zenodo DOI</a>'
        '<a href="https://doi.org/10.17605/OSF.IO/ZTJXK">OSF Registration</a></div>'
    )
    text = replace_once(text, old_links, new_links, "findings header")

    concept = '<span><a href="https://doi.org/10.5281/zenodo.21903850">Concept DOI · 10.5281/zenodo.21903850</a></span>'
    text = replace_once(
        text, concept,
        concept + '\n      <span><a href="https://doi.org/10.17605/OSF.IO/ZTJXK">OSF Registration DOI · 10.17605/OSF.IO/ZTJXK</a></span>',
        "findings DOI banner"
    )
    notes.append("docs/research-findings.html")
pending[path] = text

# ---------------- docs/sitemap.xml ----------------
path = FILES["docs/sitemap.xml"]
text = read(path)
if "osf-registration.html" not in text:
    entry = (
        "  <url>\n"
        "    <loc>https://faramarzkowsari.github.io/turkiye-disaster-intelligence-digital-twin/osf-registration.html</loc>\n"
        "    <lastmod>2026-08-14</lastmod>\n"
        "  </url>\n"
    )
    text = replace_once(text, "</urlset>", entry + "</urlset>", "sitemap OSF page")
text = text.replace("<lastmod>2026-08-12</lastmod>", "<lastmod>2026-08-14</lastmod>")
pending[path] = text
if "docs/sitemap.xml" not in notes:
    notes.append("docs/sitemap.xml")

# Validate core DOI presence before writing.
core = [
    FILES["README.md"],
    FILES["CITATION.cff"],
    FILES["ABOUT.md"],
    FILES["REPRODUCIBILITY.md"],
    FILES["docs/index.html"],
    FILES["docs/project.html"],
    FILES["docs/research-findings.html"],
]
for p in core:
    if OSF_DOI not in pending[p]:
        raise RuntimeError(f"Validation failed: OSF DOI missing after patch preparation in {p.name}")

# Back up all files before changing anything.
backup = ROOT / (".osf_doi_backup_" + datetime.now().strftime("%Y%m%d_%H%M%S"))
backup.mkdir(parents=True, exist_ok=False)
for name, p in FILES.items():
    dest = backup / name
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(p, dest)

# Write all prepared changes.
for p, content in pending.items():
    p.write_text(content, encoding="utf-8", newline="\n")

# Add/update static registration documentation.
# When the patch is extracted directly into the repository root, PATCH_ROOT == ROOT.
# In that case source and destination are the same file, so do not copy it onto itself.
for rel in [Path("OSF_REGISTRATION.md"), Path("docs/osf-registration.html")]:
    src = PATCH_ROOT / rel
    if not src.exists():
        raise RuntimeError(f"Patch asset missing: {src}")
    dst = ROOT / rel
    dst.parent.mkdir(parents=True, exist_ok=True)

    try:
        same_file = src.resolve() == dst.resolve()
    except OSError:
        same_file = False

    if not same_file:
        shutil.copy2(src, dst)

print()
print("SUCCESS: OSF DOI integration completed.")
print("Repository:", ROOT)
print("OSF Registration DOI:", OSF_DOI)
print("Backup created:", backup.name)
print()
print("Updated/verified:")
for n in notes:
    print("  -", n)
print("  - OSF_REGISTRATION.md")
print("  - docs/osf-registration.html")
print()
print("Next:")
print("1. Open GitHub Desktop.")
print("2. Review the changed files.")
print("3. Commit message:")
print("   Add accepted OSF registration DOI and open-science record")
print("4. Push origin.")
