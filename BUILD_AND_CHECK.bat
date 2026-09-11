@echo off
REM ============================================================
REM  BUILD THE PORTFOLIO, THEN CHECK IT - one double-click
REM ------------------------------------------------------------
REM  Runs, in the only order that is safe:
REM    1. build.py            rebuilds site\ from content.py
REM    2. check_portfolio.py  captions, missing images, dead links
REM    3. tests\test_chat.js  the on-site assistant, against the
REM                           BUILT page, so it tests what ships
REM    4. git                 how far ahead of GitHub you are
REM
REM  Everything is also written to build_check_log.txt so Claude
REM  can read the result without needing your terminal.
REM
REM  Two details that are NOT cosmetic:
REM    python -u   unbuffered. Without it Python holds its output
REM                until it exits, so a run that hangs leaves an
REM                empty log and you cannot tell how far it got.
REM    < NUL       empty stdin. If anything ever stops to ask a
REM                question it gets EOF and fails fast, instead
REM                of waiting forever on a keystroke.
REM
REM  Safe to run repeatedly. build.py rewrites site\ from
REM  content.py and images\ every time - that is by design.
REM ============================================================
cd /d "%~dp0"
set LOG=build_check_log.txt

echo ============================================================ > "%LOG%"
echo  PORTFOLIO BUILD AND CHECK >> "%LOG%"
echo  %DATE% %TIME% >> "%LOG%"
echo ============================================================ >> "%LOG%"
echo. >> "%LOG%"
echo ---------- 0. WHICH PYTHON ---------- >> "%LOG%"
where python >> "%LOG%" 2>&1
python -V >> "%LOG%" 2>&1
echo. >> "%LOG%"

echo [1/4] Building site\ from content.py ...
echo ---------- 1. BUILD (build.py) ---------- >> "%LOG%"
python -u build.py < NUL >> "%LOG%" 2>&1
set BUILDRC=%ERRORLEVEL%
echo    exit code %BUILDRC% >> "%LOG%"
echo. >> "%LOG%"

if not "%BUILDRC%"=="0" (
  echo.
  echo  *** BUILD FAILED - stopping here. ***
  echo  The reason is in build_check_log.txt
  echo  Nothing was pushed.
  echo  BUILD FAILED - checks below were NOT run. >> "%LOG%"
  echo.
  pause
  exit /b 1
)

echo [2/4] Checking captions, images and links ...
echo ---------- 2. CHECK (check_portfolio.py) ---------- >> "%LOG%"
python -u check_portfolio.py < NUL >> "%LOG%" 2>&1
echo    exit code %ERRORLEVEL% >> "%LOG%"
echo. >> "%LOG%"

echo [3/4] Testing the on-site assistant ...
echo ---------- 3. CHAT TESTS (tests\test_chat.js) ---------- >> "%LOG%"
node tests\test_chat.js < NUL >> "%LOG%" 2>&1
echo    exit code %ERRORLEVEL% >> "%LOG%"
echo. >> "%LOG%"

echo [4/4] Reading git state ...
echo ---------- 4. GIT ---------- >> "%LOG%"
git fetch origin < NUL >> "%LOG%" 2>&1
echo behind/ahead vs origin/main: >> "%LOG%"
git rev-list --left-right --count origin/main...HEAD < NUL >> "%LOG%" 2>&1
echo. >> "%LOG%"
echo changed files: >> "%LOG%"
git status --short < NUL >> "%LOG%" 2>&1
echo. >> "%LOG%"

echo ============================================================ >> "%LOG%"
echo  DONE >> "%LOG%"
echo ============================================================ >> "%LOG%"

echo.
echo  Done. Full result is in build_check_log.txt
echo.
echo  If the checks are clean, the next step is PUSH_PORTFOLIO.bat
echo.
pause
