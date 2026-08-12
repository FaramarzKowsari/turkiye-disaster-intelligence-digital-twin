@echo off
setlocal
cd /d "%~dp0"

if not exist pyproject.toml (
  echo ERROR: Run FINALIZE_V1.cmd from the repository root.
  pause
  exit /b 1
)

echo Removing development-time patch instruction files...
del /q APPLY_*.md 2>nul
del /q GITHUB_DESKTOP_UPLOAD.md 2>nul
if exist docs\paper_grade_pipeline.md del /q PAPER_GRADE_PIPELINE.md 2>nul

echo Cleanup complete.
echo Return to GitHub Desktop. The removed files should appear as deletions.
echo.
echo This script will now remove itself.
del /q "%~f0"
