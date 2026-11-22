@echo off
title SCRAPBOUND - 2-Player Local Test Launcher
cd /d "%~dp0"

echo ========================================================
echo   SCRAPBOUND - Starting 2-Player Local Multiplayer Test
echo ========================================================
echo.
echo Launching Player 1 (HOST) - Left Window...
start "" "..\art (2)\art\agent_new\Godot_v4.7.2-stable_win64.exe\Godot_v4.7.2-stable_win64.exe" --path "%~dp0." --host

timeout /t 2 /nobreak >nul

echo Launching Player 2 (CLIENT) - Right Window...
start "" "..\art (2)\art\agent_new\Godot_v4.7.2-stable_win64.exe\Godot_v4.7.2-stable_win64.exe" --path "%~dp0." --join

echo.
echo --------------------------------------------------------
echo Both windows are launched side-by-side!
echo Host Window (Left) will automatically host on port 7777.
echo Client Window (Right) will connect to 127.0.0.1:7777.
echo.
echo Click [START MATCH] on the Host window (Left) when ready!
echo --------------------------------------------------------
timeout /t 5 >nul
