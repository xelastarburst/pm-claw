# PM Claw — Physical AI Intelligence Pipeline

## Mission

Build and maintain a daily intelligence briefing on user problems and solution space in physical AI / robotics, with focus on simulation (Isaac Sim/Lab, synthetic data, sim2real) and adjacent domains. Accumulate over time for historical pattern recognition.

---

## Architecture

### Data Layer (files)

```
PM-claw/
├── PROJECT.md              ← This file
├── intel/
│   ├── briefs/
│   │   └── YYYY-MM-DD.md   ← Daily briefing (structured intelligence)
│   ├── problems.jsonl       ← Structured problem entries (append-only, searchable)
│   ├── sources.md           ← Source registry + search queries
│   └── SUMMARY.md           ← Rolling executive summary (updated weekly)
└── dashboard/
    └── index.html           ← Canvas dashboard (Phase 3)
```

### Collection (daily cron job)

- Isolated agent session runs every morning at **7:00 AM PT**
- Searches each source with targeted queries
- Writes the daily brief to `intel/briefs/YYYY-MM-DD.md`
- Appends structured entries to `intel/problems.jsonl`
- Delivers summary to Xela via announce

### Dashboard (Canvas HTML)

- Single-page HTML served via OpenClaw Canvas
- Sections: Today's Brief, Problem Heatmap, Trending Topics, Historical View
- Filterable by source, category, date range
- No external infra — reads from accumulated files

---

## Source Coverage

| Source | Method | Target |
|--------|--------|--------|
| **X/Twitter** | `web_search site:x.com` | Complaints, workarounds, wishlists about Isaac Sim/Lab, sim2real, synthetic data |
| **Reddit** | `web_search site:reddit.com` | r/robotics, r/reinforcementlearning, r/nvidia, r/ROS pain points |
| **NVIDIA Isaac Forum** | `web_fetch` on forums.developer.nvidia.com | Bug reports, feature requests, "how do I..." posts |
| **Discord** | `web_search site:discord.com` | Isaac, robotics simulation servers |
| **GitHub Issues** | `web_search site:github.com` | isaac-sim, IsaacLab, Isaac-ROS, Newton, Warp issues |
| **arXiv** | `web_search site:arxiv.org` | Papers citing simulation gaps, sim2real failures, synthetic data limits |
| **Hacker News** | `web_search site:news.ycombinator.com` | Robotics/simulation discussions, startup pain points |

---

## Problem Taxonomy

Each problem entry gets tagged with:

- **Category**: `sim2real` · `synthetic-data` · `training-infra` · `environment-design` · `asset-pipeline` · `deployment` · `perception` · `manipulation` · `locomotion` · `multi-agent` · `hardware-integration` · `tooling-dx`
- **Severity**: `blocker` · `pain` · `friction` · `wishlist`
- **Source**: `x` · `reddit` · `forum` · `github` · `arxiv` · `discord` · `hn`
- **Signal strength**: `strong` (multiple people, high frustration) · `moderate` (few people, clear pain) · `weak` (single mention, mild)

### problems.jsonl schema

```json
{
  "id": "2026-03-28-001",
  "date": "2026-03-28",
  "title": "Short problem description",
  "description": "Detailed context",
  "category": "sim2real",
  "severity": "pain",
  "source": "reddit",
  "source_url": "https://...",
  "signal_strength": "moderate",
  "tags": ["isaac-sim", "domain-randomization"],
  "related_ids": []
}
```

---

## Phases

### Phase 1 — First Manual Brief ✅ (today)
- [x] Set up folder structure
- [x] Write PROJECT.md
- [ ] Create sources.md with search queries
- [ ] Run first intelligence sweep across all sources
- [ ] Produce `intel/briefs/2026-03-28.md`
- [ ] Seed `intel/problems.jsonl` with structured entries
- [ ] Review with Xela, iterate on format

### Phase 2 — Automate Collection (next)
- [ ] Create daily cron job (7 AM PT, isolated agent session)
- [ ] Write collection prompt with source list + taxonomy
- [ ] Set up announce delivery to Xela
- [ ] Test run, validate output quality
- [ ] Add error handling (source down, rate limits)

### Phase 3 — Dashboard
- [ ] Build Canvas HTML dashboard
- [ ] Today's Brief section (current day highlights)
- [ ] Problem Heatmap (category × severity matrix)
- [ ] Trending Topics (what's getting hotter)
- [ ] Historical View (timeline, accumulation charts)
- [ ] Search/filter by category, source, date range

### Phase 4 — Solution Space (future)
- [ ] Add solution tracking (what exists, what's being built)
- [ ] Map problems → existing solutions → gaps
- [ ] Competitive landscape updates
- [ ] Opportunity scoring

---

## Notes

- Started: 2026-03-28
- Owner: Ziggy (collection + synthesis) + Xela (review + strategy)
- Model: NVIDIA Claude Opus 4.6
- Host: DGX Spark (GB10), spark-0a40
