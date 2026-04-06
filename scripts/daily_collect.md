# PM Claw Daily Intelligence Collection

You are the PM Claw collection agent. Your job: scrape all intelligence sources for the Physical AI / robotics simulation ecosystem, generate a daily brief, update the data files, rebuild the dashboard, and push to GitHub.

## Working Directory

`/Users/lingq/Documents/PM_claw`

## Step 1: Read Current State

1. Read `intel/problems.jsonl` to know what's already tracked (avoid duplicates)
2. Note the highest ID number used (format: `YYYY-MM-DD-NNN`) so you can assign new IDs
3. Get today's date for the brief filename

## Step 2: Scrape All Sources

Search ALL of the following sources. Use WebSearch for each query. Today's date should be used in date-sensitive queries.

### NVIDIA Isaac Forum (ALWAYS RUN)
Search queries (run all):
- `site:forums.developer.nvidia.com "isaac sim" bug OR crash OR help 2026`
- `site:forums.developer.nvidia.com "isaac lab" error OR issue OR question 2026`
- `site:forums.developer.nvidia.com isaac sim 5.1 OR 6.0 problem`

### GitHub Issues (ALWAYS RUN)
Search queries (run all):
- `site:github.com isaac-sim/IsaacLab issues 2026`
- `site:github.com NVIDIA-Omniverse issues bug 2026`
- `site:github.com isaac-sim/IsaacSim issues 2026`
- `site:github.com NVIDIA/warp issues 2026`

### Reddit (ALWAYS RUN)
Search queries (run all):
- `site:reddit.com "isaac sim" OR "isaac lab" problem OR issue OR crash 2026`
- `site:reddit.com sim2real robotics challenge OR gap 2026`
- `site:reddit.com robot simulation frustrated OR broken OR alternative 2026`
- `site:reddit.com mujoco vs isaac OR newton 2026`

### X / Twitter (ROTATE — run on Mon/Wed/Fri)
- `site:x.com "isaac sim" problem OR broken OR crash 2026`
- `site:x.com sim2real robotics difficulty OR challenge 2026`
- `site:x.com "physical AI" challenge OR limitation 2026`

### arXiv (ROTATE — run on Tue/Thu)
- `site:arxiv.org sim2real gap robotics 2026`
- `site:arxiv.org synthetic data robotics limitation 2026`
- `site:arxiv.org robot simulation benchmark 2026`

### Hacker News (ROTATE — run on Mon/Thu)
- `site:news.ycombinator.com robotics simulation 2026`
- `site:news.ycombinator.com "isaac sim" OR "isaac lab" 2026`

### Discord (ROTATE — run on Wed/Sat)
- `site:discord.com "isaac sim" help OR issue 2026`

**IMPORTANT:** For each search result, click through to read the actual content using WebFetch when a result looks relevant. Don't just rely on search snippets.

## Step 3: Classify & Deduplicate

For each new issue found:

1. **Check if it's already in problems.jsonl** — match by source_url or by title similarity. Skip duplicates.
2. **Classify** using the taxonomy:
   - **Category**: `sim2real` | `synthetic-data` | `training-infra` | `environment-design` | `asset-pipeline` | `deployment` | `perception` | `manipulation` | `locomotion` | `multi-agent` | `hardware-integration` | `tooling-dx` | `crashes-stability` | `sensors-perception` | `docs-onboarding` | `env-api` | `integration` | `feature-requests`
   - **Severity**: `blocker` (workflow completely broken) | `pain` (significant friction, workarounds exist) | `friction` (annoying but manageable) | `wishlist` (nice to have)
   - **Signal strength**: `high` (multiple reports, high engagement) | `medium` (few reports, clear pain) | `low` (single mention)
3. **Assign an ID**: `YYYY-MM-DD-NNN` where the date is today and NNN is sequential starting from 001

## Step 4: Write Daily Brief

Create `intel/briefs/daily/YYYY-MM-DD.md` with this format:

```markdown
# PM Claw Daily Developer Issue Digest — YYYY-MM-DD

**Period scanned:** Last 7 days (DATE_START → DATE_END)
**Sources:** [list sources actually searched today]
**Filter:** Isaac Sim >=5.1 prioritized; pre-5.1 flagged

---

## [severity emoji] Category Name

### N. Issue Title (version)
- **URL:** https://...
- **Version:** Isaac Sim X.Y.Z
- **Category:** category-name
- **Severity:** severity
- **Source:** source | date
- **Summary:** 2-3 sentence description of the problem and its impact.
- **Signal:** What pattern or trend does this represent?

---

## Summary Stats

| Metric | Count |
|---|---|
| Total issues tracked | N |
| New issues today | N |
| Blockers | N |
| Pain | N |
| Friction | N |
| Wishlist | N |

## Top Signals This Week

1. **Signal name** — Description
2. ...
```

Use these severity emojis:
- Blocker: `## 🔴`
- Pain: `## 🟠`
- Friction: `## 🟡`
- Wishlist: `## 🟣`

## Step 5: Update problems.jsonl

Append new entries to `intel/problems.jsonl`. Each entry is one JSON object per line:

```json
{"id":"YYYY-MM-DD-001","date":"YYYY-MM-DD","title":"Short title","description":"Detailed description","category":"category","severity":"severity","source":"source-name","source_url":"https://...","signal_strength":"high|medium|low","tags":["tag1","tag2"],"isaac_sim_version":"X.Y.Z"}
```

## Step 6: Rebuild Dashboard

Run:
```bash
python3 scripts/rebuild_dashboard.py
```

This regenerates the digest tabs from the updated problems.jsonl.

## Step 7: Commit and Push

```bash
git add intel/briefs/daily/YYYY-MM-DD.md intel/problems.jsonl dashboard/index.html
git commit -m "Daily intel: YYYY-MM-DD — N new issues tracked

Sources: [list sources searched]
Blockers: N | Pain: N | Friction: N | Wishlist: N

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
git push origin main
```

## Quality Rules

- **Never fabricate issues.** Every entry must have a real source URL that you actually visited.
- **Be specific in descriptions.** Include version numbers, GPU models, OS versions when available.
- **Err on the side of inclusion.** If something might be a duplicate but you're not sure, include it with a note in the description.
- **Signal > noise.** A well-classified issue with 3 sentences is better than a wall of text.
- **If a source is down or returns no results**, note it in the brief's header and move on. Don't block the whole pipeline.
- **If you find 0 new issues**, still generate the brief (noting "no new issues found") and rebuild the dashboard (which updates the date).
