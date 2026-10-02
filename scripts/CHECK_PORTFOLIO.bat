@echo off
REM ============================================================
REM  CHECK THE PORTFOLIO BEFORE PUSHING
REM ------------------------------------------------------------
REM  Finds the mistakes that do not look like mistakes:
REM   - a caption attached to the wrong picture
REM   - an image named in content.py that is not in images\
REM   - a page asking for a file that is not in site\assets\
REM   - a link pointing at a page that does not exist
REM   - placeholders still waiting for real artwork
REM  Safe: it only reads. It changes nothing.
REM ============================================================
cd /d "%~dp0"
python check_portfolio.py
echo.
pause
