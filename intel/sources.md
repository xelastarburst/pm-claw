# Intelligence Sources & Search Queries

## X / Twitter

### Queries (rotate daily, pick 3-4)
- `site:x.com "isaac sim" problem OR broken OR crash OR bug OR frustrated`
- `site:x.com "isaac lab" issue OR help OR stuck OR workaround`
- `site:x.com sim2real robotics difficulty OR challenge OR gap`
- `site:x.com synthetic data robotics quality OR limitation OR problem`
- `site:x.com "domain randomization" robotics issue OR fail`
- `site:x.com omniverse robotics pain OR broken OR crash`
- `site:x.com robot simulation gap OR limitation OR missing`
- `site:x.com "physical AI" challenge OR problem OR limitation`

## Reddit

### Subreddits
- r/robotics
- r/reinforcementlearning
- r/nvidia
- r/ROS
- r/computervision
- r/MachineLearning (robotics threads)

### Queries
- `site:reddit.com "isaac sim" problem OR help OR issue OR crash`
- `site:reddit.com "isaac lab" stuck OR bug OR error`
- `site:reddit.com sim2real robotics challenge OR gap OR difficult`
- `site:reddit.com synthetic data robotics limitation OR quality`
- `site:reddit.com robot simulation frustrated OR broken OR alternative`
- `site:reddit.com mujoco vs isaac comparison OR migration`

## NVIDIA Isaac Forum

### Direct URLs to scrape
- https://forums.developer.nvidia.com/c/simulation-and-training/isaac-sim/660
- https://forums.developer.nvidia.com/c/simulation-and-training/isaac-lab/940

### Queries
- `site:forums.developer.nvidia.com "isaac sim" bug OR crash OR help`
- `site:forums.developer.nvidia.com "isaac lab" error OR issue OR question`

## GitHub Issues

### Repos to watch
- `NVIDIA-Omniverse/IsaacSim` (if public)
- `isaac-sim/IsaacLab`
- `NVIDIA-Omniverse/orbit` (legacy)
- `google-deepmind/mujoco`
- `NVIDIA/warp`
- `NVIDIA-Omniverse/newton`

### Queries
- `site:github.com isaac-sim issues bug OR crash OR feature-request`
- `site:github.com IsaacLab issues help OR question OR bug`
- `site:github.com "sim2real" robotics issue OR limitation`
- `site:github.com "synthetic data" robotics issue`

## arXiv

### Queries
- `site:arxiv.org sim2real gap robotics 2025 OR 2026`
- `site:arxiv.org synthetic data robotics limitation 2025 OR 2026`
- `site:arxiv.org robot simulation benchmark challenge 2025 OR 2026`
- `site:arxiv.org domain randomization failure OR limitation`

## Hacker News

### Queries
- `site:news.ycombinator.com robotics simulation problem`
- `site:news.ycombinator.com "isaac sim" OR "isaac lab"`
- `site:news.ycombinator.com sim2real robotics`
- `site:news.ycombinator.com synthetic data robotics`

## Discord

### Queries
- `site:discord.com "isaac sim" help OR issue`
- `site:discord.com robotics simulation problem`

---

## Query Rotation Strategy

Each daily run picks a subset to avoid rate limits and ensure breadth over time:
- **Always run**: NVIDIA Forum (primary signal source), GitHub Issues, Reddit
- **Rotate**: X, arXiv, HN, Discord (2 of 4 each day)
- **Weekly deep dive**: Full sweep of all sources every Monday
