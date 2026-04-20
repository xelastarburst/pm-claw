#!/usr/bin/env python3
"""Render the "🎯 Issue Status Board" section on the Daily Digest tab.

Reads intel/problems.jsonl, computes:
  - Total tracked / open / resolved
  - 4-week weekly-new trend sparkline
  - Resolution velocity
  - Recently resolved list (last 5)

Replaces the region marked by:
  <!-- STATUS_BOARD_START -->
  <!-- STATUS_BOARD_END -->
"""
import json
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JSONL = ROOT / "intel" / "problems.jsonl"
DASHBOARD = ROOT / "dashboard" / "index.html"


def load_problems():
    out = []
    for line in JSONL.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def parse_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except Exception:
        return None


def weekly_sparkline(problems, weeks=8, width=140, height=26):
    today = date.today()
    start = today - timedelta(weeks=weeks)
    buckets_new = [0] * weeks
    buckets_resolved = [0] * weeks
    for p in problems:
        d = parse_date(p.get("date", ""))
        if d and d >= start:
            idx = min(weeks - 1, (d - start).days // 7)
            buckets_new[idx] += 1
        rd = parse_date(p.get("resolved_date", ""))
        if rd and rd >= start:
            idx = min(weeks - 1, (rd - start).days // 7)
            buckets_resolved[idx] += 1
    vmax = max(1, max(buckets_new + buckets_resolved))
    bar_w = (width - 4) / weeks
    bars = []
    for i, (n, r) in enumerate(zip(buckets_new, buckets_resolved)):
        x = 2 + i * bar_w
        # Open-bar (red/orange) from top of zero
        if n > 0:
            h = (n / vmax) * (height - 6)
            bars.append(f'<rect x="{x:.1f}" y="{height-4-h:.1f}" width="{bar_w*0.42:.1f}" height="{h:.1f}" fill="#f97316" opacity="0.85"/>')
        if r > 0:
            h = (r / vmax) * (height - 6)
            bars.append(f'<rect x="{x+bar_w*0.5:.1f}" y="{height-4-h:.1f}" width="{bar_w*0.42:.1f}" height="{h:.1f}" fill="#22c55e" opacity="0.9"/>')
    return (
        f'<svg width="{width}" height="{height}" style="vertical-align:middle">'
        f'<line x1="2" y1="{height-3.5}" x2="{width-2}" y2="{height-3.5}" stroke="#334155" stroke-width="0.5"/>'
        + "".join(bars)
        + f'</svg>'
    )


def sev_color(sev):
    return {
        "blocker": "#ef4444",
        "pain": "#f97316",
        "friction": "#eab308",
        "wishlist": "#a855f7",
    }.get(sev, "#64748b")


def render_section(problems):
    total = len(problems)
    open_n = sum(1 for p in problems if p.get("status", "open") == "open")
    resolved_n = sum(1 for p in problems if p.get("status") == "resolved")
    inprog_n = sum(1 for p in problems if p.get("status") == "in-progress")
    today = date.today()
    cutoff_30 = today - timedelta(days=30)
    new_30 = sum(1 for p in problems if (parse_date(p.get("date", "")) or today) >= cutoff_30)
    res_30 = sum(
        1
        for p in problems
        if p.get("status") == "resolved" and (parse_date(p.get("resolved_date", "")) or date(1970, 1, 1)) >= cutoff_30
    )
    net_30 = new_30 - res_30
    net_color = "#ef4444" if net_30 > 0 else ("#22c55e" if net_30 < 0 else "#94a3b8")
    net_sign = "+" if net_30 > 0 else ""
    # Resolution rate
    rate = (resolved_n / total * 100) if total else 0
    spark = weekly_sparkline(problems)

    # Severity of open issues breakdown
    sev_counts = Counter(p.get("severity", "friction") for p in problems if p.get("status", "open") == "open")

    # Recently resolved (last 5)
    resolved = sorted(
        [p for p in problems if p.get("status") == "resolved" and p.get("resolved_date")],
        key=lambda x: x.get("resolved_date", ""),
        reverse=True,
    )[:5]
    resolved_list = ""
    if resolved:
        items = []
        for p in resolved:
            url = p.get("source_url") or "#"
            target = ' target="_blank"' if url.startswith("http") else ""
            title = (p.get("title") or p.get("id", ""))[:80]
            rd = p.get("resolved_date", "")
            items.append(
                f'<div class="resolved-item"><span class="r-date">{rd}</span>'
                f'<a href="{url}"{target}>{title}</a></div>'
            )
        resolved_list = (
            '<div class="resolved-list"><h4>&#x2705; Recently resolved</h4>'
            + "".join(items)
            + "</div>"
        )
    else:
        resolved_list = '<div class="resolved-list"><h4>&#x2705; Recently resolved</h4><div style="color:#64748b;font-size:.76rem;padding:6px 0">No resolutions in the last period.</div></div>'

    sev_chips = " ".join(
        f'<span class="sev sev-{s}">{s} {n}</span>'
        for s, n in sorted(sev_counts.items(), key=lambda x: -x[1])
    )

    return f"""<!-- STATUS_BOARD_START -->
<section>
<h2>&#x1f3af; Issue Status Board</h2>
<p style="color:#94a3b8;font-size:.85rem;margin-bottom:12px;line-height:1.55">Live health of the dev-issue pipeline. Updated daily from <code>intel/problems.jsonl</code>. Resolutions tracked when upstream issue closes or fix ships.</p>
<div class="status-board">
<div class="sb-card">
<div class="sb-num">{total}</div>
<div class="sb-lbl">Total tracked</div>
</div>
<div class="sb-card sb-open">
<div class="sb-num">{open_n}</div>
<div class="sb-lbl">Open</div>
<div class="sb-sub">{sev_chips}</div>
</div>
<div class="sb-card sb-resolved">
<div class="sb-num">{resolved_n}</div>
<div class="sb-lbl">Resolved · {rate:.0f}%</div>
</div>
<div class="sb-card">
<div class="sb-num" style="color:{net_color}">{net_sign}{net_30}</div>
<div class="sb-lbl">Net last 30d</div>
<div class="sb-sub" style="color:#64748b;font-size:.68rem">{new_30} new &middot; {res_30} resolved</div>
</div>
<div class="sb-card sb-trend">
<div class="sb-spark">{spark}</div>
<div class="sb-lbl">8-week trend</div>
<div class="sb-sub" style="color:#64748b;font-size:.62rem"><span style="color:#f97316">&#9632;</span> new &middot; <span style="color:#22c55e">&#9632;</span> resolved</div>
</div>
</div>
{resolved_list}
<p style="color:#64748b;font-size:.7rem;margin-top:10px;font-style:italic">Auto-generated by <code>scripts/render_status_board.py</code>.</p>
</section>
<!-- STATUS_BOARD_END -->"""


def main():
    problems = load_problems()
    section = render_section(problems)
    html = DASHBOARD.read_text()
    if "<!-- STATUS_BOARD_START -->" in html:
        import re
        html = re.sub(
            r"<!-- STATUS_BOARD_START -->.*?<!-- STATUS_BOARD_END -->",
            section,
            html,
            flags=re.DOTALL,
        )
    else:
        # Insert at the top of the Daily Digest tab, right after <div id="tab-digest" class="tab-content">
        anchor = '<div id="tab-digest" class="tab-content">'
        idx = html.find(anchor)
        if idx == -1:
            raise SystemExit("Could not find Daily Digest tab anchor")
        insert_at = idx + len(anchor)
        html = html[:insert_at] + "\n" + section + "\n" + html[insert_at:]
    DASHBOARD.write_text(html)
    print(f"Status board rendered: {len(problems)} issues")


if __name__ == "__main__":
    main()
