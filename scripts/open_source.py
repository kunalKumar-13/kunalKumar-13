#!/usr/bin/env python3
"""Render the open-source section of README.md from the live GitHub API.

Counts only pull requests to repositories owned by a GitHub *Organization*,
so personal and friends' repositories do not pad the numbers. Every row links
to the search that produced it, so any figure here can be checked in one click.

Reads GITHUB_TOKEN from the environment. Run by .github/workflows/agent-console.yml.
"""
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from collections import defaultdict

USER = "kunalKumar-13"
TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
README = os.path.join(os.path.dirname(__file__), "..", "README.md")

START = "<!-- OPEN-SOURCE:START -->"
END = "<!-- OPEN-SOURCE:END -->"

# Display names for organisations whose login is not how the project is known.
PRETTY = {
    "sugarlabs": "Sugar Labs",
    "plone": "Plone",
    "django": "Django",
    "metabrainz": "MetaBrainz",
    "fortran-lang": "fortran-lang",
    "ZeusLN": "ZEUS",
    "openstreetmap": "OpenStreetMap",
    "dipy": "DIPY",
    "pvlib": "pvlib",
    "meshery": "Meshery",
    "urunc-dev": "urunc",
    "OWASP": "OWASP",
    "matplotlib": "Matplotlib",
    "stdlib-js": "stdlib",
}


def api(path, params=None):
    url = f"https://api.github.com/{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github+json")
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            # Search is rate limited separately and more tightly than REST.
            if e.code in (403, 429) and attempt < 2:
                time.sleep(5 * (attempt + 1))
                continue
            raise


def search_prs(qualifier):
    """All PRs by USER matching qualifier, following pagination."""
    items, page = [], 1
    while True:
        d = api("search/issues", {
            "q": f"is:pr author:{USER} {qualifier}",
            "per_page": 100,
            "page": page,
        })
        items += d["items"]
        if len(items) >= d["total_count"] or not d["items"] or page >= 10:
            return items
        page += 1
        time.sleep(2)


def owner_is_org(login, cache={}):
    if login not in cache:
        try:
            cache[login] = api(f"users/{login}")["type"] == "Organization"
        except Exception as e:
            print(f"warn: owner type for {login}: {e}", file=sys.stderr)
            cache[login] = False
    return cache[login]


def repo_of(item):
    # repository_url looks like https://api.github.com/repos/<owner>/<name>
    return item["repository_url"].split("/repos/", 1)[1]


def collect():
    merged = search_prs("is:merged")
    open_ = search_prs("is:open")

    stats = defaultdict(lambda: {"merged": 0, "open": 0, "repos": set()})
    for bucket, items in (("merged", merged), ("open", open_)):
        for it in items:
            owner, name = repo_of(it).split("/", 1)
            if not owner_is_org(owner):
                continue
            stats[owner][bucket] += 1
            stats[owner]["repos"].add(name)

    return stats


def render(stats):
    rows = sorted(stats.items(), key=lambda kv: (-kv[1]["merged"], kv[0].lower()))
    rows = [r for r in rows if r[1]["merged"] or r[1]["open"]]

    total_merged = sum(s["merged"] for _, s in rows)
    total_open = sum(s["open"] for _, s in rows)
    merged_orgs = sum(1 for _, s in rows if s["merged"])

    out = [START, "", "## Open source", ""]
    out.append(
        f"**{total_merged} merged pull requests** across **{merged_orgs} organisations**, "
        f"and {total_open} open across {len(rows)}. Counting only repositories owned by a GitHub "
        f"organisation, so personal projects do not inflate the number. Every row "
        f"links to the search behind it."
    )
    out += ["", "| Organisation | Merged | Open | Repositories |", "|---|---:|---:|---|"]

    for login, s in rows:
        q = urllib.parse.quote(f"is:pr author:{USER} org:{login} is:merged")
        link = f"https://github.com/pulls?q={q}"
        repos = ", ".join(f"`{r}`" for r in sorted(s["repos"])[:4])
        if len(s["repos"]) > 4:
            repos += f" +{len(s['repos']) - 4}"
        name = PRETTY.get(login, login)
        merged = f"**[{s['merged']}]({link})**" if s["merged"] else "0"
        out.append(f"| {name} | {merged} | {s['open'] or 0} | {repos} |")

    out += ["", f"<sub>Regenerated from the GitHub API - see "
                f"[the generator](https://github.com/{USER}/{USER}/blob/main/scripts/open_source.py).</sub>",
            "", END]
    return "\n".join(out)


def main():
    stats = collect()
    block = render(stats)

    with open(README, encoding="utf-8") as f:
        readme = f.read()

    if START in readme and END in readme:
        readme = re.sub(
            re.escape(START) + r".*?" + re.escape(END),
            lambda _: block,
            readme,
            flags=re.S,
        )
    else:
        print("error: markers not found in README.md", file=sys.stderr)
        return 1

    with open(README, "w", encoding="utf-8", newline="\n") as f:
        f.write(readme)

    print(block)
    return 0


if __name__ == "__main__":
    sys.exit(main())
