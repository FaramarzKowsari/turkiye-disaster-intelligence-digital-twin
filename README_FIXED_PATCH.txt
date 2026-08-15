FIXED OSF DOI INTEGRATION PATCH
================================

This corrected package replaces the earlier PowerShell patch.

Why the earlier one failed
--------------------------
The previous package used a PowerShell script that produced a parser error before execution.
Because it was a parser error, the old script did NOT modify repository files.

This version uses Python instead of PowerShell and is intended for the existing Python-based repository.

How to use
----------
1. Delete the old APPLY_OSF_DOI_UPDATE.ps1 / .bat files from the repository root if they are still there.
2. Extract this NEW ZIP directly into the repository root (the folder containing README.md).
3. Double-click APPLY_OSF_DOI_UPDATE.bat.
4. Wait for:
   SUCCESS: OSF DOI integration completed.
5. Open GitHub Desktop.
6. Review changes.
7. Commit message:
   Add accepted OSF registration DOI and open-science record
8. Push origin.

Safety
------
The patch validates the expected repository structure before writing.
It creates a timestamped backup folder in the repository root before changing files.
It is designed to avoid duplicate OSF DOI entries if run again.

OSF Registration DOI
--------------------
10.17605/OSF.IO/ZTJXK


V3 FIX
------
This version fixes a Windows error that occurred when the patch files were extracted
directly into the repository root. In that situation OSF_REGISTRATION.md and
docs/osf-registration.html were already at their destination paths, and the previous
script tried to copy each file onto itself.

If the previous V2 run reached a WinError 32 at shutil.copy2(), the main repository
updates had already been written before that final copy step. Running V3 is safe:
it verifies/reuses the DOI additions and skips same-file copies.
