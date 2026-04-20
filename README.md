# 🦀 PM Claw — Physical AI Intelligence Dashboard

A live intelligence dashboard tracking the NVIDIA Physical AI ecosystem: developer issues, research papers, industry moves, and competitive landscape.

**[→ View the Dashboard](https://xelastarburst.github.io/pm-claw/)**

![Dashboard Preview](https://img.shields.io/badge/status-active-22c55e) ![Issues Tracked](https://img.shields.io/badge/issues_tracked-22-f97316) ![Companies](https://img.shields.io/badge/companies-50%2B-3b82f6) ![Papers](https://img.shields.io/badge/arxiv_papers-8-8b5cf6)

---

## What is this?

PM Claw is an opinionated intelligence tool for anyone building in the Physical AI / robotics simulation space. It aggregates signals from:

- **NVIDIA Developer Forums** — Isaac Sim & Isaac Lab issues
- **GitHub Issues** — IsaacLab, IsaacSim repos
- **Reddit** — r/reinforcementlearning, r/robotics, r/MachineLearning
- **ArXiv** — cs.RO, cs.AI papers
- **X / Twitter** — Key researchers and companies
- **Industry news** — TechCrunch, CNBC, The Neuron, a16z, Bessemer

## Dashboard Tabs

### 📊 Overview
Executive summary of 38 problems across 6 categories (Oct 2025–Mar 2026). Heatmap, trending topics, and weak signals.

### 📥 Daily Digest
Developer issue tracker with **4 lookback windows**:
| Window | Issues | Key Theme |
|--------|--------|-----------|
| 1 Day | 2 | Edge deployment (Jetson Thor WebRTC) |
| 7 Days | 12 | Physics explosion bugs from USD imports |
| 2 Weeks | 16 | Blackwell GPU compatibility cluster |
| 1 Month | 22 | DX crisis (85+ Reddit upvotes), driver breakage |

### 🌍 Ecosystem
50+ companies mapped across the NVIDIA Physical AI ecosystem:
- Humanoid robots (Figure, Agility, Unitree, Tesla...)
- Robot brains / foundation models (Skild AI, Physical Intelligence, GR00T...)
- Industrial giants (FANUC, ABB, YASKAWA, KUKA)
- Simulation competitors (Genesis AI, MuJoCo, Gazebo)
- Synthetic data & 3D assets (Lightwheel, Cosmos, Palatial...)
- NVIDIA partnership tiers (Deep → Active → Users → Competitors)

### 🔬 Tech Radar
Weekly accumulated technology updates (Mar 22–29, 2026):
- **8 key ArXiv papers** — UniDex, GR00T N1, LeRobot v0.5, ROS-LLM...
- **13 industry moves** — Google+Agile Robots, Amazon humanoid acquisition, Arm AGI CPU, Figure at White House...
- **X / social signals** — ARC-AGI-3 benchmark, sim wars debate, VC landscape maps

## Data

```
PM-claw/
├── dashboard/
│   └── index.html          # Single-file dashboard (no dependencies)
├── intel/
│   ├── problems.jsonl       # Structured issue data
│   ├── ecosystem.md         # Ecosystem research notes
│   ├── sources.md           # Source URLs and methodology
│   └── briefs/
│       ├── 2026-03-28.md    # Daily brief
│       └── daily/
│           └── 2026-03-29.md
├── PROJECT.md               # Project spec
└── README.md
```

## Running Locally

It's a single HTML file. No build step, no dependencies.

```bash
cd dashboard
python3 -m http.server 8888
# Open http://localhost:8888
```

Or just open `dashboard/index.html` directly in your browser.

## Focus

- **Isaac Sim 5.1+** prioritized (pre-5.1 issues flagged)
- **NVIDIA ecosystem** as the primary lens
- **Developer pain** over marketing — what's actually broken, not what's announced

## License

MIT
