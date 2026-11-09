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

echo [*] Checking cloud sync and launching distribution flow...
.venv\Scripts\python.exe -m engine.run share --catchup %*

echo.
echo ===================================================================
echo [Tip] To re-launch today's tabs at any time, run:
echo       Share-Now.bat --force
echo ===================================================================
echo.
pause
