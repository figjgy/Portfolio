@echo off
setlocal enabledelayedexpansion
REM ============================================================
REM  PUSH PREVIEW BRANCH TO GITHUB  ->  Creates Vercel Preview
REM ============================================================
cd /d "%~dp0"
set PATH=%LOCALAPPDATA%\Git\cmd;%LOCALAPPDATA%\Git\mingw64\bin;%PATH%

echo.
echo ====================================================
echo   PUSHING fix/improvements-v1 TO GITHUB
echo ====================================================
echo.

echo [1/3] Building and verifying portfolio...
python -u build.py < NUL
if not "%ERRORLEVEL%"=="0" (
  echo [ERROR] Build failed.
  pause & exit /b 1
)

python -u check_portfolio.py < NUL
if not "%ERRORLEVEL%"=="0" (
  echo [ERROR] Check failed.
  pause & exit /b 1
)

echo.
echo [2/3] Checking git changes...
git add -A
git diff --cached --quiet
if not errorlevel 1 (
  echo No new changes to commit.
) else (
  git commit -m "Enhance SEO, OpenGraph preview, mobile navigation, and external link targets"
)

echo.
echo [3/3] Pushing branch fix/improvements-v1 to GitHub...
echo (If a browser window opens, sign in to authorize GitHub)
git push -u origin fix/improvements-v1

if "%ERRORLEVEL%"=="0" (
  echo.
  echo ====================================================
  echo   SUCCESS! Branch fix/improvements-v1 pushed.
  echo   Vercel is now building your preview deployment.
  echo ====================================================
) else (
  echo.
  echo [ERROR] Push failed. Check credentials or connection.
)

echo.
pause
