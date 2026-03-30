# Robotics Ecosystem Map
*Data: Oct 2025 – Mar 2026 | Focus: NVIDIA Physical AI stack*

---

## 1. Humanoid Robots

| Company | What They Do | NVIDIA Relationship | Stage | Funding/Valuation | Notable |
|---------|-------------|-------------------|-------|------------------|---------|
| **Figure AI** | General-purpose humanoid (Figure 02). Deployed at BMW manufacturing lines. | **Deep partner** — uses NVIDIA 3-computer architecture, GTC 2026 stage | Growth | $39B val, $1B+ Series C (Sep 2025) | Highest-valued pure-play humanoid startup |
| **Agility Robotics** | Digit humanoid for logistics. Amazon warehouse deployments. | **Deep partner** — GTC 2026, NVIDIA 3-computer arch | Growth | ~$2.1B val, $400M Series C (Mar 2025) | Amazon partnership, production-ready |
| **Apptronik** | Apollo humanoid for manufacturing (Mercedes, GXO). | **Partner** — uses Omniverse digital twins | Growth | $935M+ raised, $520M Series A-X (Feb 2026) | Google DeepMind partnership, Mercedes, John Deere investors |
| **1X Technologies** | NEO humanoid targeting home use. Norway/US. | **Neutral** — OpenAI ecosystem | Growth | Seeking $1B at $10B val (Sep 2025), $130M+ raised | OpenAI-backed, home robot focus unique |
| **Tesla** | Optimus humanoid. Internal production for Tesla factories, external sales planned 2026. | **Complex** — uses Omniverse for training, but competitive tension | Public | Internal (Tesla market cap) | Optimus v3 prototype early 2026, production late 2026 |
| **Boston Dynamics** | Atlas electric humanoid (production version CES 2026). Spot, Stretch deployed. | **Partner** — expanded collaboration Mar 2025 | Owned (Hyundai) | Hyundai subsidiary | Google DeepMind partnership for embodied AI, shipping Atlas 2026 |
| **NEURA Robotics** | 4NE-1 cognitive humanoid. German. 4NE1 Mini (€19,999) for research. | **Neutral** | Growth | $1.5B+ raised, €1B from Tether (Mar 2026) | Europe's leading humanoid, €1B order book |
| **Unitree** | Go2 quadruped, G1/H1 humanoid. Low-cost leader ($16K G1). | **Customer** — uses Isaac Sim | Growth | China-based, private | LeRobot v0.5 added G1 support, massive hobbyist adoption |
| **Agibot (China)** | Humanoid for manufacturing. Backed by ByteDance. | **Neutral** | Growth | China ecosystem | Targeting thousands of units 2025-2026 |
| **Fourier Intelligence** | GR-2 humanoid for rehab and industrial. | **Customer** — GR00T adopter | Growth | China-based | Medical + industrial dual focus |

## 2. Foundation Models for Robotics (Robot Brains)

| Company | What They Do | NVIDIA Relationship | Stage | Funding/Valuation | Notable |
|---------|-------------|-------------------|-------|------------------|---------|
| **Skild AI** | "Universal brain" foundation model spanning legged, wheeled, humanoid. CMU spinout. | **Deep partner** — NVIDIA invested, uses Isaac Lab + Cosmos world models, Foxconn factory deal | Growth | $14B val, $2B+ raised. $1.4B from SoftBank + NVIDIA (Jan 2026) | Highest-valued robot brain startup |
| **Physical Intelligence (π)** | General-purpose robot policy models (π0). | **Neutral** — independent | Growth | $11B val (Mar 2026 talks), $600M Series B (Nov 2025) | Raising $1B more, 2 years old |
| **FieldAI** | Risk-aware foundation models for construction/oil&gas inspection robots. | **Deep partner** — NVIDIA invested, uses Isaac Lab + Cosmos + Isaac Sim for validation | Growth | $400M+ raised, $2B val. Bezos, Khosla, NVIDIA backing | Cross-embodied models, real industrial deployments |
| **Google DeepMind** | Gemini Robotics + Gemini Robotics-ER. On-device model (Jun 2025). MuJoCo maintainer. | **Competitor** — alternative stack (Gemini + MuJoCo vs GR00T + Isaac) | Big Tech | Google internal | Partnered with Boston Dynamics, Apptronik, Agile Robots |
| **NVIDIA (GR00T)** | GR00T N1.7, N2 preview. Humanoid foundation model. | **Self** | Public | — | "2x task generalization vs alternatives" at GTC 2026 |
| **Covariant (now Covariant AI)** | Pick-and-place AI brain, acquired by Amazon. | **Neutral** | Acquired | Amazon acquisition | Now powers Amazon warehouse AI |
| **HuggingFace / LeRobot** | Open-source robot learning framework. LeRobot v0.5 with humanoid support. | **Neutral** — complementary ecosystem | Open source | — | IsaacLab-Arena integration, growing community |

## 3. Industrial Robot Giants (GTC 2026 Partners)

| Company | What They Do | NVIDIA Relationship | Stage | Notable |
|---------|-------------|-------------------|-------|---------|
| **FANUC** | World's largest industrial robot maker. ~1M installed base. | **Deep partner** — integrating Omniverse + Isaac into commissioning | Public | GTC 2026 stage |
| **ABB Robotics** | Industrial robots + cobots. Global #2. | **Deep partner** — Omniverse integration for commissioning | Public | GTC 2026 partner |
| **YASKAWA** | Industrial robots, Motoman series. | **Deep partner** — Omniverse + Isaac frameworks | Public | GTC 2026 stage |
| **KUKA** | Industrial robots, owned by Midea (China). | **Deep partner** — Omniverse libraries integration | Public (Midea) | GTC 2026 stage |
| **Universal Robots** | Cobot market leader (UR series). | **Partner** — GTC 2026 | Public (Teradyne) | GTC 2026 stage |
| **Hexagon Robotics** | Metrology and manufacturing intelligence. | **Partner** — GTC 2026 | Public | GTC 2026 |

*Together these companies operate 2M+ installed robots worldwide (per NVIDIA).*

## 4. Simulation & Synthetic Data

| Company | What They Do | NVIDIA Relationship | Stage | Notable |
|---------|-------------|-------------------|-------|---------|
| **Genesis (AI)** | Generative physics engine. Claim 43M FPS on single GPU. Open-source. | **Competitor** — direct threat to Isaac Sim | Research/startup | Top simulation competitor per our research |
| **Google DeepMind (MuJoCo)** | MuJoCo physics engine (free, open-source). Standard for RL research. | **Competitor** — MuJoCo Warp (475x speedup) now in Newton | Open source | Now integrated into Newton via MuJoCo Warp |
| **NVIDIA (Isaac Sim/Lab)** | Isaac Sim 6.0, Isaac Lab 3.0, Newton 1.0. Full sim stack. | **Self** | Public | Newton = open physics under Linux Foundation |
| **Open Robotics (Gazebo)** | Gazebo simulator. ROS ecosystem standard. | **Neutral** — legacy, declining for RL | Open source | Still used for ROS integration testing |
| **World Labs** | Spatial intelligence / 3D world generation. Fei-Fei Li's startup. | **Partner** — GTC 2026 | Startup | Could disrupt synthetic data generation |
| **Cosmos (NVIDIA)** | World foundation models for synthetic data gen. Cosmos Predict/Transfer 2.5. | **Self** | Public | FieldAI + Skild AI building on Cosmos |

## 5. Mobile Robots / AMRs / Warehouse

| Company | What They Do | NVIDIA Relationship | Stage | Notable |
|---------|-------------|-------------------|-------|---------|
| **Amazon Robotics** | Warehouse AMRs (Sequoia system). 750K+ robots deployed. | **Deep partner** — Omniverse digital twins, Isaac Sim, GTC partner | Big Tech | Largest robot fleet in the world |
| **Locus Robotics** | Warehouse AMRs. 13,000+ bots, 300+ facilities. | **Neutral** | Growth | Pre-IPO, market leader in collaborative AMRs |
| **Symbotic** | AI-powered warehouse automation. Walmart primary customer. | **Neutral** | Public | $31.3B market cap |
| **KION Group** | Forklifts + warehouse logistics. Working with Accenture + Siemens. | **Partner** — Mega Omniverse Blueprint for warehouse digital twins | Public | GXO deployment via NVIDIA Jetson forklifts |
| **GXO Logistics** | World's largest pure-play contract logistics. | **Partner** — Apptronik Apollo deployment, KION digital twins | Public | NVIDIA ecosystem customer through partners |

## 6. Manufacturing Digital Twins (GTC 2026)

| Company | NVIDIA Relationship | Notable |
|---------|-------------------|---------|
| **Foxconn** | Deep partner — Omniverse factory twins, Skild AI deployment | iPhone manufacturer going robotic |
| **Toyota** | Partner — Omniverse manufacturing | Building AI-driven production |
| **Caterpillar** | Partner — Omniverse | Heavy equipment digital twins |
| **TSMC** | Partner — Omniverse | Semiconductor fab optimization |
| **Siemens** | Partner — Xcelerator + Omniverse | Industrial software integration |
| **PTC / Onshape** | Partner — GTC 2026 | Design-to-sim "single source of truth" |

---

## NVIDIA Partnership Tiers

### Tier 1: Deep Partners (NVIDIA invested or co-building)
- **Skild AI** — NVIDIA invested $1.4B round, uses full stack (Isaac Lab + Cosmos + deployment)
- **FieldAI** — NVIDIA Ventures invested, uses Isaac Lab + Cosmos + Isaac Sim
- **Figure AI** — GTC stage, 3-computer architecture
- **Agility Robotics** — GTC stage, 3-computer architecture
- **Amazon Robotics** — Omniverse digital twins at scale
- **FANUC / ABB / YASKAWA / KUKA** — integrating Omniverse into 2M+ robot commissioning

### Tier 2: Active Partners
- **Apptronik** — Omniverse digital twins, GXO deployment
- **Boston Dynamics** — expanded collaboration (Mar 2025)
- **Universal Robots** — GTC 2026
- **Foxconn, Toyota, TSMC** — factory digital twins
- **KION / Siemens / PTC** — industrial workflow integration

### Tier 3: Customers / Users
- **Unitree** — uses Isaac Sim
- **Fourier Intelligence** — GR00T adopter
- **Hundreds of startups** — using Isaac Lab for RL training

### Competitors
- **Google DeepMind** — Gemini Robotics + MuJoCo. Partnered with Boston Dynamics + Apptronik (overlap!)
- **Genesis AI** — direct simulation competitor
- **Tesla** — uses Omniverse but builds own vertical stack
- **Physical Intelligence** — independent robot brain, doesn't need NVIDIA's models

---

## Key Observations

1. **NVIDIA is becoming the Android of robotics** — TechCrunch (Jan 2026) explicitly made this comparison. Full stack: simulation (Isaac) + training (Cosmos) + models (GR00T) + edge (Jetson). No one else offers end-to-end.

2. **The "Big 4" industrial robot makers all signed on** — FANUC, ABB, YASKAWA, KUKA integrating Omniverse. This is 2M+ installed robots potentially feeding the NVIDIA ecosystem. Massive moat.

3. **Google DeepMind is the only credible platform competitor** — Gemini Robotics + MuJoCo + Boston Dynamics partnership. But they don't have the industrial relationships or simulation scale.

4. **Robot brain startups are the hottest category** — Skild ($14B), Physical Intelligence ($11B), FieldAI ($2B). Investors betting the "brain" is the winner-take-most layer.

5. **Humanoid funding is insane** — $3.2B globally in 2025 alone. Figure ($39B), Skild ($14B), NEURA ($1.5B raised). Valuations disconnected from revenue.

6. **China ships, West develops** — Chinese companies (Unitree, Agibot, BYD) targeting thousands of units. Western companies still in pilot/demo stage. Cost advantage: G1 at $16K vs Figure 02 price TBD.

7. **Google and NVIDIA both partnered with Apptronik and Boston Dynamics** — shows these hardware companies are hedging, not picking one platform.

8. **The middleware gap** — No clear winner for robot deployment, monitoring, fleet management. ROS2 is messy. Opportunity space.

---

## China vs West: Humanoid Split

| Metric | West | China |
|--------|------|-------|
| **Funding** | $10B+ (Figure, Skild, Apptronik, 1X, etc.) | Lower VC but massive govt + corp backing |
| **Valuation leaders** | Figure ($39B), Skild ($14B) | Unitree, Agibot, Fourier (private) |
| **Shipping volume** | Mostly pilot/demo | Targeting 1000s of units 2025-2026 |
| **Cost** | Premium ($100K+) | Low-cost ($16K Unitree G1) |
| **Focus** | Manufacturing, logistics | Manufacturing + consumer |
| **AI stack** | NVIDIA + Google ecosystems | Mix of in-house + NVIDIA Isaac |
| **Key players** | Figure, Agility, Apptronik, BD, Tesla | Unitree, Agibot, Fourier, UBTECH, BYD |
| **Advantage** | Better AI/software, more funding | Faster iteration, lower cost, mass production |

*Source: Multiple web searches, GTC 2026 announcements, funding databases, NVIDIA press releases.*
