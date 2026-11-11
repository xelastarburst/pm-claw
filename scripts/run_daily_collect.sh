#!/usr/bin/env bash
# PM Claw Daily Intelligence Collection Runner
# Invoked by launchd at 7 AM PT daily.
# Runs claude CLI in non-interactive mode with the collection prompt.

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CLAUDE="${CLAUDE:-$HOME/.local/bin/claude}"
LOG_DIR="$REPO_DIR/logs"
DATE=$(date +%Y-%m-%d)
LOG_FILE="$LOG_DIR/collect-$DATE.log"

mkdir -p "$LOG_DIR"

echo "=== PM Claw Daily Collection: $DATE ===" >> "$LOG_FILE" 2>&1
echo "Started: $(date)" >> "$LOG_FILE" 2>&1

cd "$REPO_DIR"

# Read the collection prompt and run claude in non-interactive mode
"$CLAUDE" --print \
  --allowedTools "WebSearch,WebFetch,Read,Write,Edit,Bash,Glob,Grep" \
  "$(cat "$REPO_DIR/scripts/daily_collect.md")" \
  >> "$LOG_FILE" 2>&1

EXIT_CODE=$?

echo "" >> "$LOG_FILE"
echo "Finished: $(date)" >> "$LOG_FILE"
echo "Exit code: $EXIT_CODE" >> "$LOG_FILE"

exit $EXIT_CODE
