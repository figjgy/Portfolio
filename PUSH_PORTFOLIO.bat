@echo off
setlocal enabledelayedexpansion
REM ============================================================
REM  PUSH THE PORTFOLIO TO GITHUB  ->  Vercel redeploys by itself
REM ============================================================
REM  Double-click this file.
REM
REM  2026-09-14 REWRITE. The old version reported SUCCESS while
REM  pushing nothing, because of two faults that hid each other:
REM    * git push output was NOT redirected to the log, so the one
REM      line that matters ("Everything up-to-date" / "rejected")
REM      was only ever on screen and never readable afterwards.
REM    * "nothing to commit" and "commit failed" both produced an
REM      EMPTY section 3, so they could not be told apart.
REM  An empty push is exit code 0. Exit 0 is NOT proof of a deploy.
REM  Everything below is logged, including the ahead/behind counts.
REM ============================================================
cd /d "%~dp0"
set LOG=push_log.txt

echo ==================================================== > %LOG%
echo   PORTFOLIO BUILD, CHECK, COMMIT ^& PUSH >> %LOG%
echo   %DATE% %TIME% >> %LOG%
echo ==================================================== >> %LOG%

echo.
echo ====================================================
echo   PORTFOLIO DEPLOYMENT TO GITHUB ^& VERCEL
echo ====================================================
echo.

REM ---------- 0. environment, so a failure can be blamed correctly ----------
echo ---------- 0. ENVIRONMENT ---------- >> %LOG%
where git >> %LOG% 2>&1
where python >> %LOG% 2>&1
git remote -v >> %LOG% 2>&1
git branch --show-current >> %LOG% 2>&1

REM ---------- 0b. PULL IN ANY NEW ARTWORK, AUTOMATICALLY ----------
REM  Added 2026-09-14 because the import had become a SECOND double-click and
REM  that was a step Jamie never used to need. It runs itself now, and it is
REM  safe to leave in: the importer matches the zip BY NAME, and the guard
REM  below means it does nothing at all once the images are already in.
REM  Silent when there is nothing to do - no output, no questions, no failure.
if not exist "images\kpick-medical-01.*" (
  powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0_import_pubmats.ps1" < NUL >> %LOG% 2>&1
)

echo [1/6] Rebuilding site from content.py ...
echo ---------- 1. BUILD ---------- >> %LOG%
python -u build.py < NUL >> %LOG% 2>&1
set BUILDRC=%ERRORLEVEL%
echo    exit code %BUILDRC% >> %LOG%
if not "%BUILDRC%"=="0" (
  echo. & echo  [ERROR] Build failed. See push_log.txt. Nothing was pushed. & echo.
  pause & exit /b 1
)
echo    Build successful.

echo.
echo [2/6] Verifying consistency ...
echo ---------- 2. CHECK ---------- >> %LOG%
python -u check_portfolio.py < NUL >> %LOG% 2>&1
set CHECKRC=%ERRORLEVEL%
echo    exit code %CHECKRC% >> %LOG%
if not "%CHECKRC%"=="0" (
  echo. & echo  [ERROR] Consistency check failed. See push_log.txt. Nothing was pushed. & echo.
  pause & exit /b 1
)
echo    Consistency check passed.

REM ---------- 2b. THE JS TESTS. This gate did not exist before 2026-09-14,
REM  and its absence is exactly how commit 318cc79 (cursor halo, 3D card
REM  tilt, nav dropdown removed) reached the live site unverified.
REM  check_portfolio.py inspects captions, files and links - it has never
REM  executed a single line of JavaScript. BUILD_AND_CHECK.bat ran these
REM  tests; the PUSH path did not, so the one route that actually deploys
REM  was the one route with no JS check on it.
REM  Non-blocking on purpose: a failing test must not strand her with no
REM  way to publish, but it is now IMPOSSIBLE to push without being told.
echo.
echo [3/6] Running the site JS tests ...
echo ---------- 2b. JS TESTS (tests/test_chat.js) ---------- >> %LOG%
where node >NUL 2>&1
if errorlevel 1 (
  echo    node not found - JS tests SKIPPED.
  echo [SKIPPED - node is not on PATH] >> %LOG%
) else (
  node tests/test_chat.js < NUL >> %LOG% 2>&1
  set JSRC=!ERRORLEVEL!
  echo    exit code !JSRC! >> %LOG%
  if not "!JSRC!"=="0" (
    echo.
    echo    [WARNING] The site JS tests FAILED ^(exit !JSRC!^).
    echo    The push will continue, but something on the live site is broken.
    echo    Read section 2b of push_log.txt.
    echo.
  ) else (
    echo    JS tests passed.
  )
)

REM ---------- 3. what git ACTUALLY sees. Logged either way. ----------
echo.
echo [4/6] Reading git status ...
echo ---------- 3. GIT STATUS (before commit) ---------- >> %LOG%
git status --porcelain >> %LOG% 2>&1
git status --porcelain > _gitstat.tmp 2>&1
for %%A in (_gitstat.tmp) do set STATSIZE=%%~zA
if "!STATSIZE!"=="0" (
  echo    Working tree clean - nothing new to commit.
  echo [none - working tree clean] >> %LOG%
  set DIDCOMMIT=0
) else (
  echo    Changes found. Staging and committing...
  echo ---------- 3b. GIT ADD + COMMIT ---------- >> %LOG%
  git add -A >> %LOG% 2>&1
  git commit -m "Update portfolio: %DATE% %TIME%" >> %LOG% 2>&1
  echo    commit exit code: !ERRORLEVEL! >> %LOG%
  set DIDCOMMIT=1
)
del _gitstat.tmp >NUL 2>&1

REM ---------- 4. behind/ahead BEFORE pushing - gotcha 57's first command ----------
echo.
echo [5/6] Comparing with GitHub ...
echo ---------- 4. AHEAD / BEHIND (left=origin only, right=local only) ---------- >> %LOG%
git fetch -c credential.helper= origin >> %LOG% 2>&1
git rev-list --left-right --count origin/main...HEAD >> %LOG% 2>&1

REM ---------- 5. THE PUSH. Output goes to the log AND the screen. ----------
echo.
echo [6/6] Pushing to GitHub (origin main) ...
echo ---------- 5. GIT PUSH ---------- >> %LOG%
git push origin main > _push.tmp 2>&1
set PUSHCODE=%ERRORLEVEL%
type _push.tmp
type _push.tmp >> %LOG%
del _push.tmp >NUL 2>&1
echo git push exit code: %PUSHCODE% >> %LOG%

echo ---------- 6. AFTER THE PUSH ---------- >> %LOG%
git rev-list --left-right --count origin/main...HEAD >> %LOG% 2>&1
git log -1 --oneline >> %LOG% 2>&1

echo.
echo ====================================================
if not "%PUSHCODE%"=="0" (
  echo   PUSH FAILED  ^(exit %PUSHCODE%^)
  echo   Read push_log.txt - section 5 now has the real reason.
) else (
  if "!DIDCOMMIT!"=="0" (
    echo   PUSH OK - but there was NOTHING NEW TO SEND.
    echo   The live site has NOT changed. That is not a failure,
    echo   it means the build produced no new files. If you expected
    echo   a change, your edit did not reach content.py or images\.
  ) else (
    echo   SUCCESS - a new commit was pushed.
    echo   Vercel redeploys by itself. Check in ~1-2 minutes:
    echo   https://jamielyn-ludovice.vercel.app
  )
)
echo ====================================================
echo.
pause
