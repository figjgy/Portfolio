@echo off
REM ============================================================
REM  PUSH THE PORTFOLIO TO GITHUB  ->  Vercel redeploys by itself
REM ============================================================
REM  Double-click this file. If GitHub asks you to sign in, a
REM  browser window opens - sign in there, then it continues.
REM ============================================================
cd /d "%~dp0"
echo.
echo ====================================================
echo   Pushing your portfolio to GitHub
echo ====================================================
echo.
echo These commits will be sent:
echo.
git log --oneline origin/main..HEAD
echo.
echo ----------------------------------------------------
git push origin main
echo ----------------------------------------------------
echo.
if errorlevel 1 (
  echo   PUSH FAILED - see the message above.
  echo   Most common cause: you need to sign in to GitHub.
) else (
  echo   DONE. Vercel will redeploy in about a minute.
  echo   Check: https://jamielyn-ludovice.vercel.app
)
echo.
pause
