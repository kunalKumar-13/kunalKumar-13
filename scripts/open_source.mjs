#!/usr/bin/env node
// Rewrites the line between the open-source markers in README.md with live counts:
// merged upstream pull requests by org, and pull requests reviewed on Music Blocks.
//
// Own repos and team/hackathon repos are not upstream open source, so they are left out.
// Reads GITHUB_TOKEN (or GH_TOKEN). Run by .github/workflows/agent-console.yml.
import { readFileSync, writeFileSync } from "node:fs";

const USER = "kunalKumar-13";
const NOT_UPSTREAM = new Set([
    USER, "kartikeyajay2006", "code-gamerr", "PriyaGhosal", "kushaltalati",
    "raghav-shell", "Nency-Ravaliya", "dsc-jiit-128",
]);
const ORG_NAMES = {
    sugarlabs: "Sugar Labs", plone: "Plone", ZeusLN: "Zeus", "fortran-lang": "fortran-lang",
    django: "Django", metabrainz: "MetaBrainz", openstreetmap: "OpenStreetMap",
};
const README = new URL("../README.md", import.meta.url);
const START = "<!-- open-source:start -->";
const END = "<!-- open-source:end -->";

const token = process.env.GITHUB_TOKEN || process.env.GH_TOKEN;
if (!token) throw new Error("GITHUB_TOKEN is not set");

async function search(q) {
    const items = [];
    for (let page = 1; page <= 10; page++) {
        const url = `https://api.github.com/search/issues?q=${encodeURIComponent(q)}&per_page=100&page=${page}`;
        const res = await fetch(url, { headers: { Authorization: `Bearer ${token}`, Accept: "application/vnd.github+json" } });
        if (!res.ok) throw new Error(`${res.status} for ${q}`);
        const body = await res.json();
        items.push(...body.items);
        if (items.length >= body.total_count || body.items.length === 0) break;
    }
    return items;
}

const owner = (item) => item.repository_url.split("/repos/")[1].split("/")[0];

const merged = (await search(`author:${USER} type:pr is:merged`)).filter((i) => !NOT_UPSTREAM.has(owner(i)));
const byOrg = {};
for (const i of merged) byOrg[owner(i)] = (byOrg[owner(i)] || 0) + 1;
const orgs = Object.entries(byOrg).sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));

const reviewed = (await search(`repo:sugarlabs/musicblocks type:pr reviewed-by:${USER} -author:${USER}`)).length;

const line =
    `**${merged.length} merged pull requests** upstream: ` +
    orgs.map(([o, n]) => `${ORG_NAMES[o] || o} ${n}`).join(" · ") +
    `. And **${reviewed} pull requests reviewed** on Music Blocks.`;

const readme = readFileSync(README, "utf8");
const at = readme.indexOf(START);
const end = readme.indexOf(END);
if (at < 0 || end < at) throw new Error("open-source markers not found in README.md");
const next = readme.slice(0, at + START.length) + "\n" + line + "\n" + readme.slice(end);
if (next !== readme) writeFileSync(README, next);
console.log(line);
