#!/usr/bin/env python3
"""Generate a monthly retrospective draft that diffs the strategic state against 30 days ago.

Reads:
  - intel/problems.jsonl       — what problems were added/closed
  - intel/indicators.jsonl     — how the 9 leading indicators moved
  - intel/ecosystem.md         — ecosystem notes (optional)
  - git log                    — commit-level activity

Writes:
  - intel/retrospectives/YYYY-MM-DRAFT.md

The draft is a starting point; a human reviews, edits, and saves as YYYY-MM.md
before publishing. The dashboard's "What Changed This Month" card reads from
the latest non-DRAFT file.

Usage:
  python3 scripts/generate_retrospective.py            # current month
  python3 scripts/generate_retrospective.py 2026-05    # specific month
"""

import json
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROBLEMS = ROOT / "intel" / "problems.jsonl"
INDICATORS = ROOT / "intel" / "indicators.jsonl"
RETRO_DIR = ROOT / "intel" / "retrospectives"


def parse_ym(arg):
    if arg:
        y, m = arg.split("-")
        return int(y), int(m)
    now = datetime.now()
    return now.year, now.month


def load_jsonl(path):
    if not path.exists():
        return []
    out = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return out


def parse_date(d):
    try:
        return datetime.strptime(d, "%Y-%m-%d")
    except (ValueError, TypeError):
        return None


def month_window(year, month):
    start = datetime(year, month, 1)
    if month == 12:
        end = datetime(year + 1, 1, 1) - timedelta(seconds=1)
    else:
        end = datetime(year, month + 1, 1) - timedelta(seconds=1)
    return start, end


def problems_added_in_window(problems, start, end):
    out = []
    for p in problems:
        d = parse_date(p.get("date", ""))
        if d and start <= d <= end:
            out.append(p)
    return out


def category_breakdown(entries):
    return Counter(p.get("category", "unknown") for p in entries)


def severity_breakdown(entries):
    return Counter(p.get("severity", "unknown") for p in entries)


def indicator_diff(indicators, start, end):
    """For each indicator: first value in window, last value, delta."""
    by_key = defaultdict(list)
    for row in indicators:
        d = parse_date(row.get("date", ""))
        if not d:
            continue
        by_key[row["indicator"]].append((d, row))
    diffs = {}
    for key, rows in by_key.items():
        in_window = [(d, r) for d, r in rows if start <= d <= end]
        if not in_window:
            continue
        in_window.sort(key=lambda x: x[0])
        first_d, first_r = in_window[0]
        last_d, last_r = in_window[-1]
        diffs[key] = {
            "first_date": first_d.strftime("%Y-%m-%d"),
            "first_value": first_r.get("value"),
            "last_date": last_d.strftime("%Y-%m-%d"),
            "last_value": last_r.get("value"),
            "note": last_r.get("note", ""),
            "points": len(in_window),
        }
    return diffs


def git_commits_in_window(start, end):
    try:
        out = subprocess.check_output(
            [
                "git", "-C", str(ROOT),
                "log",
                f"--since={start.isoformat()}",
                f"--until={end.isoformat()}",
                "--format=%h|%s",
            ],
            text=True,
        )
        return [line for line in out.strip().split("\n") if line]
    except subprocess.CalledProcessError:
        return []


def fmt_pct_change(first, last):
    try:
        f, l = float(first), float(last)
    except (TypeError, ValueError):
        return "—"
    if f == 0:
        return f"↑new ({l})" if l > 0 else "—"
    pct = (l - f) / abs(f) * 100
    arrow = "↑" if pct > 0 else ("↓" if pct < 0 else "→")
    return f"{arrow}{abs(pct):.0f}%"


def render(year, month, problems_added, cat_counts, sev_counts, indicator_diffs, commits):
    start, end = month_window(year, month)
    window_label = f"{start.strftime('%Y-%m-%d')} → {end.strftime('%Y-%m-%d')}"
    total_problems = len(problems_added)

    def cat_line():
        if not cat_counts:
            return "  - (none)"
        return "\n".join(f"  - {c}: {n}" for c, n in cat_counts.most_common())

    def sev_line():
        if not sev_counts:
            return "  - (none)"
        return "\n".join(f"  - {s}: {n}" for s, n in sev_counts.most_common())

    def indicator_rows():
        if not indicator_diffs:
            return "  - (no indicator data yet this month)"
        rows = []
        for key in sorted(indicator_diffs):
            d = indicator_diffs[key]
            delta = fmt_pct_change(d["first_value"], d["last_value"])
            first = d["first_value"] if d["first_value"] is not None else "—"
            last = d["last_value"] if d["last_value"] is not None else "—"
            rows.append(
                f"- **{key}** — {first} → {last} ({delta}) over {d['points']} data points"
            )
        return "\n".join(rows)

    def commits_section():
        if not commits:
            return "  - (no commits this month)"
        return "\n".join(f"- `{c}`" for c in commits[:30])

    def top_problems_section():
        if not problems_added:
            return "  - (no new problems this month)"
        blockers = [p for p in problems_added if p.get("severity") == "blocker"]
        pain = [p for p in problems_added if p.get("severity") == "pain"]
        top = blockers[:5] + pain[:5]
        lines = []
        for p in top:
            lines.append(
                f"- **[{p.get('severity','?').upper()}]** {p.get('title','?')} "
                f"(`{p.get('category','?')}`) — {p.get('source_url','')}"
            )
        return "\n".join(lines) if lines else "  - (no blockers or pain items)"

    return f"""# PM Claw Monthly Retrospective — {year}-{month:02d}

**Window:** {window_label}
**Status:** DRAFT — review and rename to `{year}-{month:02d}.md` to publish.

---

## Executive Summary

*TODO: 2-3 sentence human-written summary pointing to the biggest strategic movement this month. See the data below.*

---

## New Problems Tracked

**Total added this month:** {total_problems}

**By category:**
{cat_line()}

**By severity:**
{sev_line()}

### Notable new entries (top blockers + pain)

{top_problems_section()}

---

## Leading Indicator Movement

{indicator_rows()}

*Indicators with meaningful movement (>25% delta or threshold trigger) warrant portfolio re-scoring. Review the "Leading Indicators" section of the Strategy tab for thresholds.*

---

## Ecosystem / Activity Log

{commits_section()}

---

## Strategic Reassessment

*TODO (human): based on the data above, which bets should move tiers?*

- Bets promoted: _(e.g., B3 Newton parity from Tier B to Tier A if mesh-terrain NaN reports doubled)_
- Bets demoted: _(e.g., B7 benchmark from Tier B to Tier C if RoboCasa365 became the de-facto standard)_
- New bets to consider: _(things that didn't exist at start of month)_

---

*Generated by `scripts/generate_retrospective.py`. Review, edit, rename without DRAFT suffix, and commit to publish.*
"""


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    year, month = parse_ym(arg)
    start, end = month_window(year, month)

    problems = load_jsonl(PROBLEMS)
    indicators = load_jsonl(INDICATORS)

    problems_added = problems_added_in_window(problems, start, end)
    cat_counts = category_breakdown(problems_added)
    sev_counts = severity_breakdown(problems_added)
    indicator_diffs = indicator_diff(indicators, start, end)
    commits = git_commits_in_window(start, end)

    RETRO_DIR.mkdir(parents=True, exist_ok=True)
    out_path = RETRO_DIR / f"{year}-{month:02d}-DRAFT.md"

    body = render(year, month, problems_added, cat_counts, sev_counts, indicator_diffs, commits)
    out_path.write_text(body)

    print(f"Wrote {out_path}")
    print(f"  Problems added in window: {len(problems_added)}")
    print(f"  Indicators with data: {len(indicator_diffs)}")
    print(f"  Commits: {len(commits)}")


if __name__ == "__main__":
    main()
