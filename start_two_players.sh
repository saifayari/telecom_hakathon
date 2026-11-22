#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GODOT_BIN="${GODOT_BIN:-$(command -v godot || command -v godot4 || true)}"

if [ -z "$GODOT_BIN" ]; then
    echo "❌ Error: Godot binary ('godot' or 'godot4') was not found in PATH."
    echo "💡 On Arch Linux: sudo pacman -S godot"
    echo "💡 On Ubuntu/Debian: sudo apt install godot4"
    echo "💡 Or set GODOT_BIN=/path/to/godot"
    exit 1
fi

echo "=========================================================="
echo "🕹️  SCRAPBOUND - 2-Player Local Test Launcher (Linux)"
echo "=========================================================="
echo "Starting Player 1 (Host Window)..."
"$GODOT_BIN" --path "$SCRIPT_DIR" --resolution 960x540 --position 50,100 "$@" &
P1_PID=$!

sleep 1.5

echo "Starting Player 2 (Client Window)..."
"$GODOT_BIN" --path "$SCRIPT_DIR" --resolution 960x540 --position 980,100 "$@" &
P2_PID=$!

echo ""
echo "✅ Both windows launched!"
echo "👉 In Window 1: Click 'HOST GAME (P1)'"
echo "👉 In Window 2: Click 'JOIN GAME (P2)'"
echo "👉 Then click 'START MATCH' on Window 1!"
echo "=========================================================="

wait $P1_PID $P2_PID 2>/dev/null || true
