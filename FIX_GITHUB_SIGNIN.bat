@echo off
REM ============================================================
REM  FIX THE GITHUB SIGN-IN, THEN PUSH
REM ------------------------------------------------------------
REM  Use this when the push fails with:
REM     "Permission to figjgy/Portfolio.git denied ... 403"
REM
REM  That means Windows has a SAVED GitHub login that does not
REM  have write access to the repo. This forgets it, so GitHub
REM  asks you to sign in again in the browser.
REM
REM  IMPORTANT: sign in with the SAME GitHub account you use in
REM  the browser when you upload files - that account owns the
REM  repo and can write to it.
REM ============================================================
cd /d "%~dp0"

echo ==================================================== > push_log.txt
echo   SIGN-IN RESET + PUSH  %DATE% %TIME% >> push_log.txt
echo ==================================================== >> push_log.txt

echo.
echo ====================================================
echo   Step 1 of 2 - forgetting the old GitHub sign-in
echo ====================================================
echo.

(echo protocol=https& echo host=github.com) | git credential reject
echo --- git credential reject done >> push_log.txt 2>&1

cmdkey /delete:git:https://github.com >nul 2>&1
cmdkey /delete:LegacyGeneric:target=git:https://github.com >nul 2>&1
git credential-manager github logout >nul 2>&1

echo   Old sign-in cleared.
echo.
echo ====================================================
echo   Step 2 of 2 - pushing (a browser will open)
echo ====================================================
echo.
echo   Sign in with the account that owns figjgy/Portfolio
echo   - the same one you use on github.com in your browser.
echo.

git log --oneline origin/main..HEAD
echo --- commits to send: >> push_log.txt
git log --oneline origin/main..HEAD >> push_log.txt 2>&1

echo.
echo ----------------------------------------------------
git push origin main 2>&1
set PUSHCODE=%errorlevel%
echo --- push exit code: %PUSHCODE% >> push_log.txt
git push origin main >> push_log.txt 2>&1
echo ----------------------------------------------------
echo.

if "%PUSHCODE%"=="0" (
  echo   DONE. Vercel redeploys in about a minute.
  echo   Check: https://jamielyn-ludovice.vercel.app
) else (
  echo   STILL FAILING. Read the message above.
  echo   If it says 403 again, the account you signed in with
  echo   does not have write access to figjgy/Portfolio.
)
echo.
pause
