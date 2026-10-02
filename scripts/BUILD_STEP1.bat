@echo off
REM ============================================================
REM  STEP 1 ONLY - build the site, unbuffered, nothing can block
REM ------------------------------------------------------------
REM  Diagnostic version of BUILD_AND_CHECK.bat. Three differences
REM  that matter:
REM    python -u   unbuffered, so the log fills in as it runs
REM                instead of staying empty until the end
REM    < NUL       stdin is empty, so if anything ever asks a
REM                question it gets EOF instead of waiting for a
REM                keystroke forever
REM    where python  proves WHICH python is being used before
REM                  blaming the script
REM  Writes build_step1_log.txt. Safe: build.py only rewrites
REM  site\ from content.py and images\.
REM ============================================================
cd /d "%~dp0"
set LOG=build_step1_log.txt

echo BUILD STEP 1 - %DATE% %TIME% > "%LOG%"
echo. >> "%LOG%"
echo ---------- which python ---------- >> "%LOG%"
where python >> "%LOG%" 2>&1
python -V >> "%LOG%" 2>&1
echo. >> "%LOG%"
echo ---------- build.py (unbuffered) ---------- >> "%LOG%"
python -u build.py < NUL >> "%LOG%" 2>&1
echo. >> "%LOG%"
echo exit code %ERRORLEVEL% >> "%LOG%"
echo FINISHED >> "%LOG%"

echo.
echo  Done - see build_step1_log.txt
echo.
pause
