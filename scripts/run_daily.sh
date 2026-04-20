#!/usr/bin/env bash
# PM Claw — run the daily intelligence pipeline locally.
#
# Usage: bash scripts/run_daily.sh
#
# This invokes Claude Code in print mode with the pipeline spec + today's
# overrides. It scrapes all sources, classifies new issues, rebuilds the
# dashboard, and commits + pushes using your local `gh` auth.
#
# Requirements:
#   - claude CLI installed and authenticated (`claude --version` must work)
#   - gh CLI authed with push to xelastarburst/pm-claw (`gh auth status`)
#   - python3 (for rebuild_dashboard.py and render_indicators.py)

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

TODAY="$(date +%Y-%m-%d)"
echo "▶ PM Claw daily pipeline — $TODAY"
echo "  repo: $REPO_ROOT"
echo

# Sanity checks
command -v claude >/dev/null 2>&1 || { echo "✗ claude CLI not found on PATH. Install it first."; exit 1; }
command -v gh >/dev/null 2>&1 || { echo "✗ gh CLI not found on PATH."; exit 1; }
gh auth status >/dev/null 2>&1 || { echo "✗ gh not authenticated. Run: gh auth login"; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "✗ python3 not found on PATH."; exit 1; }

# Pull latest in case remote has changes (e.g. from other machines)
git fetch origin main --quiet
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse @{u})
if [ "$LOCAL" != "$REMOTE" ]; then
  echo "⚠ local is behind origin/main. Pulling first."
  git pull --ff-only origin main
  echo
fi

# Spec + overrides. The agent reads daily_collect.md from the repo so this
# prompt just frames today's run.
PROMPT="Run the PM Claw daily intelligence pipeline.

Read scripts/daily_collect.md in this repo — it has the full 8-step spec. Execute it end-to-end for today ($TODAY).

Overrides:
- Working directory is $REPO_ROOT.
- Rotation: derive from today's day-of-week. Always run NVIDIA forum + GitHub + Reddit queries.
- After Step 5 (append to problems.jsonl), do Step 5.5 (update intel/indicators.jsonl per the spec) THEN run python3 scripts/render_indicators.py.
- Step 6: python3 scripts/rebuild_dashboard.py.
- Step 7: update Overview / Ecosystem / Tech Radar / footer tabs in dashboard/index.html. DO NOT modify the Strategy tab (it's human-edited).
- Step 8: commit with the standard daily-intel format and push to origin/main. Local gh auth is configured and will work.

Quality rules (non-negotiable):
- Never fabricate. Every problem entry needs a real source_url you visited via WebFetch.
- If 0 new issues, still write today's brief (note 'no new issues') and rebuild the dashboard.
- Include versions, GPU, OS, driver where available.

When done: print the commit SHA and confirm push succeeded."

echo "▶ Invoking Claude Code (this may take 30–60 min for the full pipeline)…"
echo
claude -p "$PROMPT"

echo
echo "▶ Pipeline complete. Verify:"
echo "   - New file: intel/briefs/daily/$TODAY.md"
echo "   - New lines in: intel/indicators.jsonl (dated $TODAY)"
echo "   - New commit on main: $(git log -1 --oneline)"
echo "   - Dashboard: https://xelastarburst.github.io/pm-claw/"
