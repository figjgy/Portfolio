@echo off
setlocal enabledelayedexpansion
REM ============================================================
REM  PUSH THE PORTFOLIO TO GITHUB  ->  Vercel redeploys by itself
REM ============================================================
REM  Double-click this file.
REM  It will:
REM    1. Rebuild site\ from content.py (build.py)
REM    2. Verify captions, links & images (check_portfolio.py)
REM    3. Stage and commit all new/modified files
REM    4. Push to GitHub (origin main) -> triggers Vercel deploy
REM ============================================================
cd /d "%~dp0"

echo ==================================================== > push_log.txt
echo   PORTFOLIO BUILD, CHECK, COMMIT ^& PUSH >> push_log.txt
echo   %DATE% %TIME% >> push_log.txt
echo ==================================================== >> push_log.txt

echo.
echo ====================================================
echo   PORTFOLIO DEPLOYMENT TO GITHUB ^& VERCEL
echo ====================================================
echo.

echo [1/4] Rebuilding site from content.py ...
echo ---------- 1. BUILD ---------- >> push_log.txt
python -u build.py < NUL >> push_log.txt 2>&1
set BUILDRC=%ERRORLEVEL%
echo    exit code %BUILDRC% >> push_log.txt
if not "%BUILDRC%"=="0" (
  echo.
  echo  [ERROR] Build failed! Check push_log.txt for details.
  echo  Nothing was pushed.
  echo.
  pause
  exit /b 1
)
echo    Build successful.

echo.
echo [2/4] Verifying consistency ...
echo ---------- 2. CHECK ---------- >> push_log.txt
python -u check_portfolio.py < NUL >> push_log.txt 2>&1
set CHECKRC=%ERRORLEVEL%
echo    exit code %CHECKRC% >> push_log.txt
if not "%CHECKRC%"=="0" (
  echo.
  echo  [ERROR] Consistency check failed! Check push_log.txt for details.
  echo  Nothing was pushed.
  echo.
  pause
  exit /b 1
)
echo    Consistency check passed.

echo.
echo [3/4] Staging and committing changes ...
echo ---------- 3. GIT COMMIT ---------- >> push_log.txt
set HAS_CHANGES=0
for /f "tokens=*" %%i in ('git status --porcelain') do (
  set HAS_CHANGES=1
)

if "%HAS_CHANGES%"=="1" (
  echo    Changes detected. Staging and committing...
  git add -A >> push_log.txt 2>&1
  git commit -m "Update portfolio: %DATE% %TIME%" >> push_log.txt 2>&1
  echo    Committed latest updates.
) else (
  echo    No new uncommitted changes.
)

echo.
echo [4/4] Pushing to GitHub (origin main) ...
echo ---------- 4. GIT PUSH ---------- >> push_log.txt
echo.
git push origin main
set PUSHCODE=%ERRORLEVEL%
echo git push exit code: %PUSHCODE% >> push_log.txt

echo.
echo ====================================================
if "%PUSHCODE%"=="0" (
  echo   SUCCESS! Everything pushed to GitHub.
  echo   Vercel is now automatically rebuilding and deploying!
  echo.
  echo   Check your live website in ~1-2 minutes:
  echo   https://jamielyn-ludovice.vercel.app
) else (
  echo   PUSH FAILED (Exit Code: %PUSHCODE%)
  echo   Details saved in push_log.txt.
  echo   If prompted to sign in to GitHub, please authorize in your browser.
)
echo ====================================================
echo.
pause
