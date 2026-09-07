@echo off
REM ============================================================
REM  PUSH THE PORTFOLIO TO GITHUB  ->  Vercel redeploys by itself
REM ============================================================
REM  Double-click this file. If GitHub asks you to sign in, a
REM  browser window opens - sign in there, then it continues.
REM
REM  Everything printed here is also saved to push_log.txt so it
REM  can be read afterwards if something goes wrong.
REM ============================================================
cd /d "%~dp0"

echo ==================================================== > push_log.txt
echo   PUSH RUN %DATE% %TIME% >> push_log.txt
echo ==================================================== >> push_log.txt

echo.
echo ====================================================
echo   Pushing your portfolio to GitHub
echo ====================================================
echo.
echo Sign-in helper in use:
git config --get credential.helper
git config --get credential.helper >> push_log.txt 2>&1

echo.
echo These commits will be sent:
echo.
git log --oneline origin/main..HEAD
echo --- commits to send: >> push_log.txt
git log --oneline origin/main..HEAD >> push_log.txt 2>&1

echo.
echo ----------------------------------------------------
echo --- push output: >> push_log.txt
git push origin main 2>&1
git push origin main >> push_log.txt 2>&1
set PUSHCODE=%errorlevel%
echo ----------------------------------------------------
echo.

echo --- exit code: %PUSHCODE% >> push_log.txt
if "%PUSHCODE%"=="0" (
  echo   DONE. Vercel will redeploy in about a minute.
  echo   Check: https://jamielyn-ludovice.vercel.app
) else (
  echo   PUSH FAILED - the full message is saved in push_log.txt
  echo   Tell Claude to read Portfolio\push_log.txt
)
echo.
pause
