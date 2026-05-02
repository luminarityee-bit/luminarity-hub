@echo off
chcp 65001 >nul
title LUMINARITY HUB - Ενημέρωση Ειδικών Όρων
cd /d "%~dp0"
where python >nul 2>nul
if errorlevel 1 (
  where py >nul 2>nul
  if errorlevel 1 (
    echo.
    echo [!] Δεν βρέθηκε Python. Κατέβασέ το από https://www.python.org/downloads/
    echo     και επανέλαβε.
    echo.
    pause
    exit /b 1
  )
  py "scripts\rebuild_terms.py"
) else (
  python "scripts\rebuild_terms.py"
)
