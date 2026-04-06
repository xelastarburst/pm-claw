#!/usr/bin/env python3
"""Rebuild the PM Claw dashboard digest sections from problems.jsonl.

Reads intel/problems.jsonl and regenerates:
  - Header stats (total entries, date)
  - Digest tab content (1d, 7d, 2w, 1m windows)

Leaves Overview, Ecosystem, and Tech Radar tabs untouched.
"""

import json
import re
import html
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JSONL = ROOT / "intel" / "problems.jsonl"
DASHBOARD = ROOT / "dashboard" / "index.html"

SEVERITY_ORDER = {"blocker": 0, "pain": 1, "friction": 2, "wishlist": 3}


def load_problems():
    problems = []
    with open(JSONL) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            p = json.loads(line)
            problems.append(p)
    return problems


def parse_date(d):
    try:
        return datetime.strptime(d, "%Y-%m-%d")
    except (ValueError, TypeError):
        return None


def filter_by_window(problems, today, days):
    cutoff = today - timedelta(days=days)
    return [p for p in problems if parse_date(p.get("date")) and parse_date(p["date"]) >= cutoff]


def severity_sort_key(p):
    return SEVERITY_ORDER.get(p.get("severity", "wishlist"), 3)


def escape(text):
    return html.escape(str(text)) if text else ""


def render_issue_item(p):
    sev = p.get("severity", "friction")
    title = escape(p.get("title", "Untitled"))
    desc = escape(p.get("description", ""))
    url = p.get("source_url", "")
    source = escape(p.get("source", "unknown"))
    date_str = p.get("date", "")
    tags = p.get("tags", [])

    # Format date for display
    dt = parse_date(date_str)
    display_date = dt.strftime("%b %d") if dt else date_str

    title_html = f'<a href="{escape(url)}" target="_blank">{title}</a>' if url else title
    tags_html = "".join(f'<span class="issue-tag">{escape(t)}</span>' for t in tags[:4])

    return f'''<div class="issue-item sev-{sev}">
<div class="issue-title">{title_html}</div>
<div class="issue-desc">{desc}</div>
<div class="issue-meta"><span class="issue-sev issue-sev-{sev}">{sev}</span><span class="issue-src">{source}</span><span class="issue-date">{display_date}</span>{tags_html}</div>
</div>'''


def render_window(problems, window_label, today, days, is_active=False):
    filtered = filter_by_window(problems, today, days)
    filtered.sort(key=severity_sort_key)

    total = len(filtered)
    blockers = sum(1 for p in filtered if p.get("severity") == "blocker")
    pain = sum(1 for p in filtered if p.get("severity") == "pain")
    friction = sum(1 for p in filtered if p.get("severity") == "friction")
    wishlist = sum(1 for p in filtered if p.get("severity") == "wishlist")

    active_cls = " active" if is_active else ""

    # Stats bar
    stats_items = [f'<div class="ws-item"><div class="ws-num">{total}</div><div class="ws-lbl">Issues</div></div>']
    if blockers:
        stats_items.append(f'<div class="ws-item"><div class="ws-num">{blockers}</div><div class="ws-lbl">Blockers</div></div>')
    if pain:
        stats_items.append(f'<div class="ws-item"><div class="ws-num">{pain}</div><div class="ws-lbl">Pain</div></div>')
    if friction:
        stats_items.append(f'<div class="ws-item"><div class="ws-num">{friction}</div><div class="ws-lbl">Friction</div></div>')
    if wishlist:
        stats_items.append(f'<div class="ws-item"><div class="ws-num">{wishlist}</div><div class="ws-lbl">Wishlist</div></div>')

    # Summary
    date_range = f"{(today - timedelta(days=days)).strftime('%b %d')} &#8211; {today.strftime('%b %d, %Y')}"
    summary = f"<strong>{total} issues tracked ({date_range}).</strong>"

    # Top severities for summary
    top_blockers = [p for p in filtered if p.get("severity") == "blocker"]
    if top_blockers:
        titles = ", ".join(p.get("title", "")[:50] for p in top_blockers[:3])
        summary += f" Blockers: {escape(titles)}."

    # Issue cards (limit to 20 per window to keep HTML manageable)
    cards = "\n".join(render_issue_item(p) for p in filtered[:20])
    overflow = ""
    if len(filtered) > 20:
        overflow = f'\n<p style="text-align:center;padding:12px;color:#475569;font-size:.75rem;font-style:italic">+ {len(filtered) - 20} more issues not shown</p>'

    return f'''<!-- {window_label} -->
<div id="digest-{window_label}" class="digest-window{active_cls}">
<div class="window-stats">
{"".join(stats_items)}
</div>
<div class="digest-summary"><p>{summary}</p></div>

{cards}{overflow}
</div>'''


def rebuild():
    problems = load_problems()
    today = datetime.now()

    total_entries = len(problems)
    date_str = today.strftime("%Y-%m-%d")
    display_date = today.strftime("%b %d, %Y")

    # Build digest windows
    windows = [
        render_window(problems, "1d", today, 1),
        render_window(problems, "7d", today, 7, is_active=True),
        render_window(problems, "2w", today, 14),
        render_window(problems, "1m", today, 30),
    ]

    digest_html = "\n\n".join(windows)

    # Read current dashboard
    content = DASHBOARD.read_text()

    # Update header date
    content = re.sub(
        r'<span>&#x1f4c5; [^<]+</span>',
        f'<span>&#x1f4c5; {date_str}</span>',
        content
    )

    # Update JSONL entry count in stats bar
    content = re.sub(
        r'(<div class="stat"><div class="num">)\d+(</div><div class="lbl">JSONL Entries</div></div>)',
        rf'\g<1>{total_entries}\g<2>',
        content
    )

    # Replace digest section content (between the digest-tabs div and the closing </section>)
    digest_pattern = re.compile(
        r'(<!-- 1 DAY -->|<!-- 1d -->).*?(</section>\s*</div>\s*\n\s*\n\s*<div id="tab-ecosystem")',
        re.DOTALL
    )
    replacement = f'{digest_html}\n\n</section>\n</div>\n\n\n<div id="tab-ecosystem"'
    content = digest_pattern.sub(replacement, content)

    DASHBOARD.write_text(content)
    print(f"Dashboard rebuilt: {total_entries} entries, date={date_str}")
    print(f"  1d: {len(filter_by_window(problems, today, 1))} issues")
    print(f"  7d: {len(filter_by_window(problems, today, 7))} issues")
    print(f"  2w: {len(filter_by_window(problems, today, 14))} issues")
    print(f"  1m: {len(filter_by_window(problems, today, 30))} issues")


if __name__ == "__main__":
    rebuild()
