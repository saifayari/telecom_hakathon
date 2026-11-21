@echo off
title SCRAPBOUND - 2-Player Local Test Launcher
cd /d "%~dp0"

echo Starting Player 1 (Host Window)...
start "" "..\art (2)\art\agent_new\Godot_v4.7.2-stable_win64.exe\Godot_v4.7.2-stable_win64.exe" --path "%~dp0."

timeout /t 2 /nobreak >nul

echo Starting Player 2 (Client Window)...
start "" "..\art (2)\art\agent_new\Godot_v4.7.2-stable_win64.exe\Godot_v4.7.2-stable_win64.exe" --path "%~dp0."

echo Both windows launched!
echo In Window 1: Click "HOST GAME (P1)"
echo In Window 2: Click "JOIN GAME (P2)"
echo Then click "START MATCH" on Window 1!
exit
