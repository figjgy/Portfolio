@echo off
REM ============================================================
REM  IMPORT THE UPLOADED PUBMAT ZIP INTO Portfolio\images\
REM ============================================================
REM  Double-click this file.
REM  It unpacks the newest .zip sitting in the Claude uploads
REM  folder, copies every image into Portfolio\images\ renamed
REM  kpick-medical-01.jpg, -02.jpg ... and writes the full
REM  original -> new mapping into import_pubmats_log.txt so
REM  Claude can read the result without a terminal (gotcha 70).
REM
REM  It does NOT rebuild the site and does NOT push. Run
REM  PUSH_PORTFOLIO.bat afterwards, once Claude has wired the
REM  filenames into content.py.
REM ============================================================
cd /d "%~dp0"

echo.
echo ====================================================
echo   IMPORTING PUBMATS INTO Portfolio\images\
echo ====================================================
echo.

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0_import_pubmats.ps1" < NUL > import_pubmats_log.txt 2>&1
set RC=%ERRORLEVEL%

type import_pubmats_log.txt

echo.
echo ====================================================
if "%RC%"=="0" (
  echo   DONE - see the mapping above.
  echo   Tell Claude how many images were imported.
) else (
  echo   FAILED ^(exit %RC%^) - the reason is in the text above
  echo   and in import_pubmats_log.txt
)
echo ====================================================
echo.
pause
