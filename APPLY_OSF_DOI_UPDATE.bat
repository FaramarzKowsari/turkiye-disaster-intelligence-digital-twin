@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if %errorlevel%==0 (
  py -3 "%~dp0APPLY_OSF_DOI_UPDATE.py"
  goto done
)

where python >nul 2>nul
if %errorlevel%==0 (
  python "%~dp0APPLY_OSF_DOI_UPDATE.py"
  goto done
)

echo.
echo ERROR: Python was not found.
echo This repository uses Python 3.11+, so install/enable Python and run this file again.
echo.

:done
echo.
pause
