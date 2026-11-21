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

echo "🎮 Launching SCRAPBOUND with $GODOT_BIN..."
exec "$GODOT_BIN" --path "$SCRIPT_DIR" "$@"
