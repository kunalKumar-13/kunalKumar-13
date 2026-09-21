#!/usr/bin/env python3
"""Render assets/stats.svg from the live GitHub API.

The card under "The receipts" was a hand-made snapshot that could only go
stale, and had: 636 contributions / 579 commits / 24 pull requests / 30
repositories, against a real 928 / 710 / 123 / 41. Sitting under a page that
promises "every number in it was true when you loaded this page" -- and
directly above a live table reporting 37 merged pull requests -- the stale
"24 pull requests" read as a contradiction.

Keeps the original design exactly: 880x222 card, 53 weekly bars, the same
five-step blue-to-mauve ramp. Only the numbers move.

Also rewrites the alt text of the <img> in README.md, so the figures a screen
reader is given match the ones in the picture.

Reads GITHUB_TOKEN from the environment. Run by .github/workflows/agent-console.yml.
"""
import json
import os
import re
import sys
import urllib.request

USER = "kunalKumar-13"
TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
HERE = os.path.dirname(__file__)
SVG = os.path.join(HERE, "..", "assets", "stats.svg")
README = os.path.join(HERE, "..", "README.md")

QUERY = """
{
  user(login: "%s") {
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      totalRepositoriesWithContributedCommits
      contributionCalendar {
        totalContributions
        weeks { contributionDays { contributionCount date } }
      }
    }
  }
}
""" % USER

# Card geometry, taken from the asset this replaces.
WIDTH, HEIGHT = 880, 222
BAR_X0, BAR_W = 40.0, 12.9
AXIS_W = 800.0
# Spaced so the last bar's right edge lands exactly on the end of the axis
# rule at x=840, which is how the asset this replaces was laid out.
BAR_STEP = (AXIS_W - BAR_W) / 52
BASELINE, MAX_H = 188.0, 84.0
RAMP = ["#21384f", "#1f6feb", "#388bfd", "#7aa2f7", "#bb9af7"]

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def fetch():
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY}).encode(),
        headers={"Content-Type": "application/json"},
    )
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req, timeout=30) as r:
        payload = json.load(r)
    if "errors" in payload:
        raise RuntimeError(payload["errors"])
    return payload["data"]["user"]["contributionsCollection"]


def month_label(iso):
    """2026-09-22 -> 'Sep 2026'."""
    year, month, _ = iso.split("-")
    return f"{MONTHS[int(month) - 1]} {year}"


def bar_colour(count, peak):
    if count == 0:
        return RAMP[0]
    # Four live steps above zero, so a quiet week still reads as present.
    step = min(4, 1 + int((count / peak) * 4.0)) if peak else 1
    return RAMP[step]


def render(data):
    cal = data["contributionCalendar"]
    weeks = cal["weeks"]
    totals = [sum(d["contributionCount"] for d in w["contributionDays"]) for w in weeks]
    peak = max(totals) if totals else 0

    first_day = weeks[0]["contributionDays"][0]["date"]
    last_day = weeks[-1]["contributionDays"][-1]["date"]

    figures = [
        (cal["totalContributions"], "contributions"),
        (data["totalCommitContributions"], "commits"),
        (data["totalPullRequestContributions"], "pull requests"),
        (data["totalRepositoriesWithContributedCommits"], "repositories"),
    ]

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}" fill="none" '
        f"font-family=\"'JetBrains Mono','SFMono-Regular',ui-monospace,Menlo,Consolas,monospace\">",
        f'  <rect x="1" y="1" width="{WIDTH - 2}" height="{HEIGHT - 2}" rx="16" '
        f'fill="#0d1117" stroke="#30363d" stroke-width="1.5"/>',
        '  <text x="40" y="28" font-size="13" font-weight="700" fill="#7aa2f7">Last 12 months</text>',
        '  <text x="167" y="28" font-size="11.5" fill="#7d8590">· weekly contributions</text>',
        f'  <text x="840" y="28" font-size="11" fill="#565f89" text-anchor="end">'
        f'live · {month_label(last_day)}</text>',
    ]

    for (value, label), x in zip(figures, (40, 250, 460, 670)):
        out.append(
            f'  <text x="{x}" y="56" font-size="30" font-weight="700" fill="#e6edf3">{value}</text>'
            f'<text x="{x}" y="76" font-size="12" fill="#7d8590">{label}</text>'
        )

    bars = []
    for i, count in enumerate(totals):
        x = round(BAR_X0 + i * BAR_STEP, 1)
        h = round((count / peak) * MAX_H, 1) if peak else 0.0
        y = round(BASELINE - h, 1)
        delay = round(i * 0.02, 2)
        bars.append(
            f'<rect x="{x}" y="{BASELINE}" width="{BAR_W}" height="0" rx="1.5" '
            f'fill="{bar_colour(count, peak)}">'
            f'<animate attributeName="height" values="0;{h}" dur="0.55s" '
            f'begin="{delay:.2f}s" fill="freeze"/>'
            f'<animate attributeName="y" values="{BASELINE};{y}" dur="0.55s" '
            f'begin="{delay:.2f}s" fill="freeze"/></rect>'
        )
    out.append("  " + "".join(bars))

    out += [
        f'  <rect x="40" y="193" width="{AXIS_W:.0f}" height="1" fill="#21262d"/>',
        f'  <text x="40" y="209" font-size="10.5" fill="#565f89">{month_label(first_day)}</text>',
        f'  <text x="440.0" y="209" font-size="10.5" fill="#565f89" text-anchor="middle">'
        f'peak week · {peak}</text>',
        f'  <text x="840" y="209" font-size="10.5" fill="#565f89" text-anchor="end">'
        f'{month_label(last_day)}</text>',
        "</svg>",
    ]
    return "\n".join(out) + "\n", figures


def update_readme_alt(figures):
    """Keep the img alt text honest -- it hardcodes the same four numbers."""
    alt = ", ".join(f"{value} {label}" for value, label in figures) + " in the last 12 months"
    with open(README, encoding="utf-8") as f:
        readme = f.read()

    pattern = re.compile(r'(<img src="[^"]*assets/stats\.svg[^"]*"[^>]*?alt=")[^"]*(")')
    new, n = pattern.subn(lambda m: m.group(1) + alt + m.group(2), readme)
    if n != 1:
        print(f"warn: stats.svg alt text matched {n} times, not rewriting", file=sys.stderr)
        return
    if new != readme:
        with open(README, "w", encoding="utf-8", newline="\n") as f:
            f.write(new)
        print(f"README alt -> {alt}")


def main():
    data = fetch()
    svg, figures = render(data)

    # The page's whole claim is that its numbers are live, so a mangled byte
    # here is worth failing over rather than shipping.
    if "\ufffd" in svg:
        print("error: replacement character in generated SVG", file=sys.stderr)
        return 1

    with open(SVG, "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)

    update_readme_alt(figures)
    print(" / ".join(f"{v} {l}" for v, l in figures))
    return 0


if __name__ == "__main__":
    sys.exit(main())
