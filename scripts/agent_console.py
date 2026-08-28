#!/usr/bin/env python3
"""Render assets/agent-console.svg: an agent trace over this account's live GitHub activity.

Reads GITHUB_TOKEN from the environment. Run by .github/workflows/agent-console.yml.
"""
import json, os, re, subprocess, sys, urllib.request
from datetime import datetime, timezone, timedelta

USER = "kunalKumar-13"
TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "agent-console.svg")


def api(path):
    req = urllib.request.Request(f"https://api.github.com/{path}")
    req.add_header("Accept", "application/vnd.github+json")
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def graphql(query):
    body = json.dumps({"query": query}).encode()
    req = urllib.request.Request("https://api.github.com/graphql", data=body)
    req.add_header("Authorization", f"Bearer {TOKEN}")
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)["data"]


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def collect():
    since = (datetime.now(timezone.utc) - timedelta(days=7)).strftime("%Y-%m-%d")

    # commits in the last 7 days
    commits = repos_touched = 0
    try:
        d = graphql('{ user(login:"%s"){ contributionsCollection(from:"%sT00:00:00Z"){ '
                    'totalCommitContributions totalRepositoriesWithContributedCommits } } }' % (USER, since))
        cc = d["user"]["contributionsCollection"]
        commits = cc["totalCommitContributions"]
        repos_touched = cc["totalRepositoriesWithContributedCommits"]
    except Exception as e:
        print("warn: commit stats:", e, file=sys.stderr)

    # open pull requests that are NOT in this user's own repos
    upstream = []
    try:
        q = f"search/issues?q=type:pr+author:{USER}+state:open&sort=created&order=desc&per_page=30"
        for it in api(q).get("items", []):
            repo = it["repository_url"].replace("https://api.github.com/repos/", "")
            if repo.lower().startswith(USER.lower() + "/"):
                continue
            upstream.append((repo, it["title"]))
    except Exception as e:
        print("warn: pulls:", e, file=sys.stderr)

    # where the actual commit volume went over the last 30 days — push
    # timestamps are too easy to skew with a one-line docs commit
    focus = ("", "")
    try:
        d30 = (datetime.now(timezone.utc) - timedelta(days=30)).strftime("%Y-%m-%d")
        d = graphql('{ user(login:"%s"){ contributionsCollection(from:"%sT00:00:00Z"){ '
                    'commitContributionsByRepository(maxRepositories:20){ contributions{ totalCount } '
                    'repository{ name description isFork owner{ login } } } } } }' % (USER, d30))
        best = None
        for c in d["user"]["contributionsCollection"]["commitContributionsByRepository"]:
            r = c["repository"]
            if r["isFork"] or r["owner"]["login"].lower() != USER.lower() or r["name"] == USER:
                continue
            n = c["contributions"]["totalCount"]
            if best is None or n > best[0]:
                best = (n, r["name"], (r["description"] or "").strip())
        if best:
            focus = (best[1], best[2])
    except Exception as e:
        print("warn: focus:", e, file=sys.stderr)

    return commits, repos_touched, upstream[:3], focus


def build_lines(commits, repos_touched, upstream, focus):
    """Return [(kind, text)] making up the trace."""
    L = [("cmd", f"agent --observe {USER} --window 7d"), ("gap", "")]

    L += [("think", "what has this human shipped lately?"),
          ("tool", "github.commits(since=7d)"),
          ("obs", f"{commits} commits across {repos_touched} repositories"),
          ("gap", "")]

    L += [("think", "is any of it upstream, or all his own sandbox?"),
          ("tool", "github.pulls(state=open, upstream=true)")]
    if upstream:
        for repo, title in upstream:
            t = title if len(title) <= 46 else title[:45].rstrip() + "…"
            L.append(("obs2", f"{repo:<26}{t}"))
    else:
        L.append(("obs", "no upstream pull requests open right now"))
    L.append(("gap", ""))

    name, desc = focus
    if name:
        L += [("think", "what is he actually building right now?"),
              ("tool", "github.commits(group_by=repo, since=30d)")]
        d = desc.split(".")[0] if desc else ""
        d = d if len(d) <= 52 else d[:51].rstrip() + "…"
        L.append(("obs", f"{name}" + (f" — {d}" if d else "")))
        L.append(("gap", ""))

    L += [("ans", "Builds AI agents, RAG systems and developer tooling."),
          ("ans2", "Ships upstream. Answers only what the data supports.")]
    return L


PALETTE = {  # label, label colour, body colour
    "think": ("THINK ", "#bb9af7", "#a9b1d6"),
    "tool":  ("TOOL  ", "#7dcfff", "#e6edf3"),
    "obs":   ("OBS   ", "#9ece6a", "#e6edf3"),
    "obs2":  ("      ", "#9ece6a", "#8b949e"),
    "ans":   ("ANSWER", "#e0af68", "#e6edf3"),
    "ans2":  ("      ", "#e0af68", "#e6edf3"),
}


def render(lines, stamp):
    """Reveal the whole trace in under two seconds, then hold it.

    The first cut staggered lines over a 20s loop, so a visitor met a mostly
    empty terminal and had to wait 14s for a full trace that then wiped. The
    trace now types in fast and freezes: whenever you arrive, you read it.
    """
    LH = 20
    top = 80
    STAGGER = 0.13          # whole trace lands in ~1.9s
    REVEAL = 0.30
    W = 880

    y = top
    body = []
    step = 0.0
    for kind, text in lines:
        if kind == "gap":
            y += 11         # tighter than a full line
            continue
        body.append((kind, text, y, step))
        step += STAGGER
        y += LH

    prompt_y = y + 26
    height = prompt_y + 24

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{height}" '
           f'viewBox="0 0 {W} {height}" fill="none" '
           f'font-family="\'JetBrains Mono\',\'SFMono-Regular\',ui-monospace,Menlo,Consolas,monospace">',
           f'<rect x="1" y="1" width="{W-2}" height="{height-2}" rx="14" fill="#0d1117" stroke="#30363d" stroke-width="1.5"/>',
           f'<path d="M1 42 h{W-2}" stroke="#30363d" stroke-width="1.5"/>']
    for i, c in enumerate(("#ff5f56", "#febc2e", "#28c840")):
        out.append(f'<circle cx="{24+i*20}" cy="21.5" r="6" fill="{c}"/>')
    out.append(f'<text x="{W/2}" y="26" text-anchor="middle" fill="#7d8590" font-size="12.5">'
               f'agent-console — observing @{USER}</text>')

    for kind, text, ly, begin in body:
        anim = (f'<animate attributeName="opacity" from="0" to="1" begin="{begin:.2f}s" '
                f'dur="{REVEAL}s" fill="freeze"/>')
        if kind == "cmd":
            out.append(f'<text x="28" y="{ly}" font-size="13.5" opacity="0">'
                       f'<tspan fill="#7aa2f7" font-weight="700">❯</tspan>'
                       f'<tspan fill="#e6edf3"> {esc(text)}</tspan>{anim}</text>')
        else:
            label, lc, bc = PALETTE[kind]
            out.append(f'<text x="28" y="{ly}" font-size="13.5" xml:space="preserve" opacity="0">'
                       f'<tspan fill="{lc}" font-weight="700">{label}</tspan>'
                       f'<tspan fill="{bc}">  {esc(text)}</tspan>{anim}</text>')

    out.append(f'<path d="M28 {prompt_y-20} h{W-56}" stroke="#21262d" stroke-width="1"/>')
    out.append(f'<text x="28" y="{prompt_y}" font-size="13.5" opacity="0">'
               f'<tspan fill="#7aa2f7" font-weight="700">❯</tspan>'
               f'<animate attributeName="opacity" from="0" to="1" begin="{step:.2f}s" dur="0.3s" fill="freeze"/></text>')
    out.append(f'<rect x="46" y="{prompt_y-11}" width="9" height="15" fill="#7aa2f7" opacity="0">'
               f'<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;0.01;0.5;0.51;1" '
               f'dur="1.06s" begin="{step:.2f}s" repeatCount="indefinite"/></rect>')
    out.append(f'<text x="{W-28}" y="{prompt_y}" text-anchor="end" font-size="11" fill="#565f89" opacity="0">'
               f'regenerated {stamp} · every 6h'
               f'<animate attributeName="opacity" from="0" to="1" begin="{step:.2f}s" dur="0.4s" fill="freeze"/></text>')
    out.append('</svg>')
    return "\n".join(out)


def main():
    commits, repos_touched, upstream, focus = collect()
    lines = build_lines(commits, repos_touched, upstream, focus)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    svg = render(lines, stamp)
    path = os.path.abspath(OUT)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(svg)
    print(f"wrote {path}  ({len(svg)} bytes)")
    print(f"  commits={commits} repos={repos_touched} upstream={len(upstream)} focus={focus[0]}")


if __name__ == "__main__":
    main()
