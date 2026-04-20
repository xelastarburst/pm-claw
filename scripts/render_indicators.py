#!/usr/bin/env python3
"""Render the "📡 Indicator Tracker" section on the Strategy tab from intel/indicators.jsonl.

Reads all historical indicator values, computes:
  - Current value + 30-day delta
  - Inline SVG sparkline of last 30 days
  - Threshold alert status (green / yellow / red)

Replaces the region in dashboard/index.html marked by the sentinel comments:
  <!-- INDICATOR_TRACKER_START -->
  <!-- INDICATOR_TRACKER_END -->

Safe to run repeatedly; idempotent.
"""

import json
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JSONL = ROOT / "intel" / "indicators.jsonl"
DASHBOARD = ROOT / "dashboard" / "index.html"

# Indicator metadata: display name + threshold logic
# threshold returns ("green"/"yellow"/"red", "reason") given current + history
INDICATORS = [
    {
        "key": "blackwell-bug-count",
        "label": "Blackwell Bug Count",
        "direction": "lower-is-better",
        "green_max": 3, "yellow_max": 7,
        "note": "Should trend to zero within 90 days of B1/B4 shipping.",
        "source_url": "https://github.com/isaac-sim/IsaacLab/issues?q=is%3Aissue+blackwell",
        "source_label": "GitHub search",
    },
    {
        "key": "pi-07-replication-papers",
        "label": "π0.7 Replication / Refutation Papers",
        "direction": "signal",
        "green_max": 0, "yellow_max": 0,  # any value ≥1 triggers B6 decision
        "trigger": "first paper → trigger B6 decision point immediately",
        "note": "First independent replication triggers B6 decision point.",
        "source_url": "https://arxiv.org/search/?query=compositional+generalization+robot&start=0",
        "source_label": "arXiv search",
    },
    {
        "key": "ai-native-sim-tools",
        "label": "3rd-Party AI-Native Sim Tools",
        "direction": "higher-warns",
        "green_max": 4, "yellow_max": 7,
        "note": "Crossing 5+ combined user-base signals B8 urgency → Tier S.",
        "source_url": "https://github.com/isaac-sim/IsaacLab/issues/5278",
        "source_label": "IsaacLab #5278",
    },
    {
        "key": "cosmos-downloads",
        "label": "Cosmos Download Count",
        "direction": "higher-is-better",
        "note": "Flat for 2 months → double B5 investment.",
        "source_url": "https://nvidianews.nvidia.com/news/nvidia-announces-major-release-of-cosmos-world-foundation-models-and-physical-ai-data-tools",
        "source_label": "NVIDIA press",
    },
    {
        "key": "unitree-2026-target",
        "label": "Unitree 2026 Shipment Target",
        "direction": "higher-triggers-acquisition",
        "note": "50K+ combined units → accelerate B9 / B11 / B12.",
        "source_url": "https://www.bloomberg.com/news/articles/2026-04-15/tesla-s-chinese-robot-rival-ramps-up-global-push-ahead-of-ipo",
        "source_label": "Bloomberg",
    },
    {
        "key": "isaac-vs-mujoco-arxiv",
        "label": "Isaac vs MuJoCo arXiv Share",
        "direction": "lower-warns",
        "note": "MuJoCo crossing 40% of new robotics papers → Scenario 2 materializing.",
        "source_url": "https://arxiv.org/list/cs.RO/recent",
        "source_label": "arXiv cs.RO",
    },
    {
        "key": "lerobot-checkpoints",
        "label": "LeRobot HuggingFace Checkpoints",
        "direction": "higher-triggers-acquisition",
        "note": "Doubling quarterly → deepen B11 sooner.",
        "source_url": "https://huggingface.co/lerobot",
        "source_label": "HuggingFace",
    },
    {
        "key": "groot-adopter-count",
        "label": "GR00T Adopter Count (Internal)",
        "direction": "internal-only",
        "note": ">50% of new robotics startups → moat holding. <30% → reframe as platform.",
        "source_url": None,
        "source_label": None,
    },
    {
        "key": "newton-vs-physx-usage",
        "label": "Newton vs PhysX Usage (Internal)",
        "direction": "internal-only",
        "note": "Plateau → feature parity gap is the issue; ship B3 faster.",
        "source_url": None,
        "source_label": None,
    },
]


def load_history():
    """Return dict: indicator_key → list of (date, value) sorted ascending."""
    history = defaultdict(list)
    if not JSONL.exists():
        return history
    with open(JSONL) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            key = obj.get("indicator")
            value = obj.get("value")
            date = obj.get("date")
            if key and date:
                history[key].append((date, value, obj.get("note", "")))
    for k in history:
        history[k].sort(key=lambda r: r[0])
    return history


def fmt_value(v):
    if v is None:
        return "—"
    if isinstance(v, (int, float)):
        if v >= 1_000_000:
            return f"{v/1_000_000:.1f}M"
        if v >= 1_000:
            return f"{v/1_000:.1f}K"
        return str(int(v)) if v == int(v) else f"{v:.2f}"
    return str(v)


def delta_30d(history_entries):
    """Given [(date, value, note), ...] sorted ascending, return (first_value, last_value, delta_str)."""
    vals = [(d, v) for d, v, _ in history_entries if v is not None]
    if len(vals) < 2:
        return None, vals[-1][1] if vals else None, "—"
    first_d, first_v = vals[0]
    last_d, last_v = vals[-1]
    try:
        first_v = float(first_v)
        last_v = float(last_v)
    except (TypeError, ValueError):
        return first_v, last_v, "—"
    if first_v == 0:
        return first_v, last_v, "↑new" if last_v > 0 else "—"
    pct = (last_v - first_v) / abs(first_v) * 100
    arrow = "↑" if pct > 0 else ("↓" if pct < 0 else "→")
    return first_v, last_v, f"{arrow}{abs(pct):.0f}%"


def status_color(meta, value, delta_str):
    """Return (hex_color, label) for the indicator chip."""
    if meta["direction"] == "internal-only" or value is None:
        return "#64748b", "manual"
    try:
        v = float(value)
    except (TypeError, ValueError):
        return "#64748b", "—"
    if meta["direction"] == "lower-is-better":
        if v <= meta.get("green_max", 0):
            return "#22c55e", "on-track"
        if v <= meta.get("yellow_max", 999):
            return "#eab308", "watch"
        return "#ef4444", "alert"
    if meta["direction"] == "higher-warns":
        if v <= meta.get("green_max", 0):
            return "#22c55e", "quiet"
        if v <= meta.get("yellow_max", 999):
            return "#eab308", "building"
        return "#ef4444", "trigger"
    if meta["direction"] == "signal":
        if v == 0:
            return "#22c55e", "quiet"
        return "#ef4444", "TRIGGERED"
    # higher-is-better / higher-triggers-acquisition / lower-warns: neutral unless trend
    return "#3b82f6", "tracking"


def render_sparkline(history_entries, width=80, height=20):
    """Tiny inline SVG sparkline. Takes last 30 data points."""
    vals = [v for _, v, _ in history_entries if v is not None]
    try:
        vals = [float(v) for v in vals]
    except (TypeError, ValueError):
        return ""
    if len(vals) < 2:
        return f'<svg width="{width}" height="{height}" style="vertical-align:middle"><circle cx="{width//2}" cy="{height//2}" r="2" fill="#64748b"/></svg>'
    vals = vals[-30:]
    vmin, vmax = min(vals), max(vals)
    rng = vmax - vmin if vmax != vmin else 1
    points = []
    for i, v in enumerate(vals):
        x = i * (width - 2) / (len(vals) - 1) + 1
        y = height - 2 - (v - vmin) / rng * (height - 4)
        points.append(f"{x:.1f},{y:.1f}")
    color = "#3b82f6"
    return (
        f'<svg width="{width}" height="{height}" style="vertical-align:middle">'
        f'<polyline points="{" ".join(points)}" fill="none" stroke="{color}" stroke-width="1.5"/>'
        f"</svg>"
    )


def render_section(history):
    today_str = datetime.now().strftime("%Y-%m-%d")

    rows = []
    triggered_alerts = []
    for meta in INDICATORS:
        entries = history.get(meta["key"], [])
        first, last, delta = delta_30d(entries)
        color, label = status_color(meta, last, delta)
        spark = render_sparkline(entries)
        val_display = fmt_value(last)
        note = meta.get("note", "")
        src_url = meta.get("source_url")
        src_label = meta.get("source_label")
        source_html = (
            f' <a href="{src_url}" target="_blank" style="color:#00aeef;font-size:.62rem;text-decoration:none;font-family:ui-monospace,Menlo,Consolas,monospace">↗ {src_label}</a>'
            if src_url else ""
        )
        rows.append(
            f'<tr>'
            f'<td class="c"><strong>{meta["label"]}</strong>{source_html}<div style="font-size:.7rem;color:#64748b;margin-top:2px">{note}</div></td>'
            f'<td style="font-weight:700;color:#f7fafc">{val_display}</td>'
            f'<td>{spark}</td>'
            f'<td style="color:{color};font-size:.7rem">{delta}</td>'
            f'<td><span class="sev" style="background:{color}33;color:{color}">{label}</span></td>'
            f"</tr>"
        )
        if label in ("alert", "trigger", "TRIGGERED"):
            triggered_alerts.append((meta["label"], label, val_display, note))

    table = (
        '<div class="hm"><table>'
        '<tr><th style="text-align:left">Indicator</th><th>Current</th><th>30d Trend</th><th>Δ</th><th>Status</th></tr>'
        + "".join(rows)
        + "</table></div>"
    )

    # Alert cards
    alert_html = ""
    if triggered_alerts:
        alert_items = "".join(
            f'<div class="card blocker"><h3>⚠ {label.upper()}: {name} = {val}</h3><p>{note}</p></div>'
            for name, label, val, note in triggered_alerts
        )
        alert_html = f'<div class="card-grid" style="grid-template-columns:1fr;margin-bottom:14px">{alert_items}</div>'

    data_point_count = sum(len(h) for h in history.values())

    return f"""<!-- INDICATOR_TRACKER_START -->
<section>
<h2>&#x1f4e1; Indicator Tracker &mdash; Live Strategic Signals</h2>
<p style="color:#94a3b8;font-size:.85rem;margin-bottom:14px;line-height:1.55">Live tracking of the 9 leading indicators from Section 9. Updated daily by the PM Claw collection agent; internal-only metrics require manual input. <strong style="color:#f7fafc">{data_point_count}</strong> data points logged as of {today_str}.</p>
{alert_html}
{table}
<p style="color:#64748b;font-size:.7rem;margin-top:10px;font-style:italic">Auto-generated by <code>scripts/render_indicators.py</code> from <code>intel/indicators.jsonl</code>. Re-run after each daily update.</p>
</section>
<!-- INDICATOR_TRACKER_END -->"""


def main():
    history = load_history()
    new_section = render_section(history)
    content = DASHBOARD.read_text()

    if "<!-- INDICATOR_TRACKER_START -->" in content:
        import re
        content = re.sub(
            r"<!-- INDICATOR_TRACKER_START -->.*?<!-- INDICATOR_TRACKER_END -->",
            new_section,
            content,
            flags=re.DOTALL,
        )
    else:
        # Insert after the "In Progress" section — or before the final </div> of tab-strategy
        # We'll insert right before the footer so it lands at the bottom of the Strategy tab.
        insert_before = '<footer><p>Ziggy'
        idx = content.find(insert_before)
        if idx == -1:
            raise SystemExit("Could not find insertion anchor in dashboard/index.html")
        # Back up to the last </section> before the footer (which closes the final strategy section)
        # Insert our new section right after that closing </section> but before </div> that closes tab-strategy
        # Simpler: insert right before the </div> that closes tab-strategy, which is right before the footer.
        closing_div = content.rfind("</div>", 0, idx)
        content = content[:closing_div] + new_section + "\n\n" + content[closing_div:]

    DASHBOARD.write_text(content)
    pts = sum(len(h) for h in history.values())
    print(f"Indicator tracker rendered: {pts} data points across {len(history)} indicators")


if __name__ == "__main__":
    main()
