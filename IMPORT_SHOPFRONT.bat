@echo off
REM ============================================================
REM  IMPORT THE 5 SHOP-FRONT SCREENSHOTS INTO Portfolio\images\
REM ============================================================
REM  Double-click this file.
REM  Takes the 5 most recently pasted images out of the Claude
REM  uploads folder and copies them in as marketplace-01.png ...
REM  marketplace-05.png, oldest first so the order matches the
REM  order they were sent.
REM
REM  RUN THIS BEFORE PASTING ANYTHING ELSE INTO THE CHAT -
REM  "most recent" is the only handle these files give us.
REM  Check the timestamps it prints before pushing.
REM ============================================================
cd /d "%~dp0"

echo.
echo ====================================================
echo   IMPORTING SHOP-FRONT SCREENSHOTS
echo ====================================================
echo.

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0_import_shopfront.ps1" -Count 5 -Prefix "marketplace-" < NUL > import_shopfront_log.txt 2>&1
set RC=%ERRORLEVEL%

type import_shopfront_log.txt

echo.
echo ====================================================
if "%RC%"=="0" (
  echo   DONE - check the timestamps above.
) else (
  echo   FAILED ^(exit %RC%^) - reason is above.
)
echo ====================================================
echo.
pause
