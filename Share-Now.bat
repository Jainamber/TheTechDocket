@echo off
setlocal enabledelayedexpansion
title TheTechDocket — Guided Distribution Launchpad

echo.
echo ===================================================================
echo   THE TECH DOCKET — GUIDED BROWSER DISTRIBUTION FLOW
echo   North Star Law: Increasing Weekly Visitors (thetechdocket.com)
echo ===================================================================
echo.

cd /d "C:\NewStartsNov\TheTechDocket"

if "%1"=="--report" (
    echo [*] Opening visual analytics and North Star report...
    .venv\Scripts\python.exe -m engine.run report --open
    goto end
)

echo [*] Checking cloud sync and launching distribution flow...
.venv\Scripts\python.exe -m engine.run share --catchup %*

echo.
echo ===================================================================
echo [Tip] To open your visual analytics dashboard at any time, run:
echo       Share-Now.bat --report
echo [Tip] To re-launch today's distribution tabs, run:
echo       Share-Now.bat --force
echo ===================================================================

:end
echo.
pause
