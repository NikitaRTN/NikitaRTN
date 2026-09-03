from __future__ import annotations

import html
import json
import os
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

LOGIN = "NikitaRTN"
TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
if not TOKEN:
    raise SystemExit("GH_TOKEN or GITHUB_TOKEN is required")


def request(url: str, payload: dict | None = None) -> dict:
    data = json.dumps(payload).encode() if payload else None
    req = urllib.request.Request(url, data=data)
    req.add_header("Authorization", "Bearer " + TOKEN)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "NikitaRTN-live-profile")
    if payload:
        req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)


query = """
query($login: String!) {
  user(login: $login) {
    followers { totalCount }
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { contributionCount date } }
      }
      totalCommitContributions
    }
    repositories(first: 100, privacy: PUBLIC, ownerAffiliations: OWNER,
      orderBy: {field: PUSHED_AT, direction: DESC}) {
      totalCount
      nodes { name stargazerCount pushedAt primaryLanguage { name } }
    }
  }
}
"""
graph = request("https://api.github.com/graphql", {"query": query, "variables": {"login": LOGIN}})
if graph.get("errors"):
    raise RuntimeError(json.dumps(graph["errors"], ensure_ascii=False))

profile = graph["data"]["user"]
collection = profile["contributionsCollection"]
calendar = collection["contributionCalendar"]
repos = profile["repositories"]["nodes"]
projects = [repo for repo in repos if repo["name"].lower() != LOGIN.lower()]
latest = projects[0] if projects else (repos[0] if repos else None)
updated = datetime.now(timezone.utc).strftime("%d %b %Y · %H:%M UTC")
latest_name = html.escape(latest["name"]) if latest else "No public project"
latest_lang = html.escape((latest.get("primaryLanguage") or {}).get("name", "Mixed")) if latest else "—"
latest_date = latest["pushedAt"][:10] if latest else "—"
total_stars = sum(repo["stargazerCount"] for repo in repos)
metrics = {
    "__CONTRIBUTIONS__": calendar["totalContributions"],
    "__COMMITS__": collection["totalCommitContributions"],
    "__REPOS__": profile["repositories"]["totalCount"],
    "__STARS__": total_stars,
    "__FOLLOWERS__": profile["followers"]["totalCount"],
}


def heat_color(count: int) -> str:
    if count == 0:
        return "#151D31"
    if count == 1:
        return "#173D48"
    if count <= 3:
        return "#20636C"
    if count <= 6:
        return "#2EA4AA"
    return "#4FE1E8"


heatmap: list[str] = []
active_days = 0
for column, week in enumerate(calendar["weeks"][-5:]):
    for row, day in enumerate(week["contributionDays"]):
        count = day["contributionCount"]
        active_days += int(count > 0)
        x, y = 827 + column * 45, 276 + row * 15
        title = f"{day['date']}: {count} contributions"
        heatmap.append(f'<rect x="{x}" y="{y}" width="34" height="11" rx="3" fill="{heat_color(count)}"><title>{title}</title></rect>')
template = """<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="420" viewBox="0 0 1200 420" role="img" aria-labelledby="title desc">
<title id="title">Live GitHub signal for NikitaRTN</title>
<desc id="desc">Verified GitHub API metrics and a five-week contribution heatmap</desc>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#070B14"/><stop offset="1" stop-color="#10152A"/></linearGradient>
  <linearGradient id="accent"><stop stop-color="#4FE1E8"/><stop offset="1" stop-color="#806CFF"/></linearGradient>
  <pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M30 0H0V30" fill="none" stroke="#AFC4FF" stroke-opacity=".045"/></pattern>
  <style>.sans{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif}.mono{font-family:"SFMono-Regular",Consolas,"Liberation Mono",monospace}.white{fill:#F7FAFF}.muted{fill:#8C9AB9}.cyan{fill:#4FE1E8}.violet{fill:#9A8CFF}.card{fill:#0E1628;stroke:#263453}.rule{stroke:#2A395A}</style>
</defs>
<rect width="1200" height="420" rx="24" fill="url(#bg)"/><rect x="1" y="1" width="1198" height="418" rx="23" fill="none" stroke="#26314D"/><rect width="1200" height="420" rx="24" fill="url(#grid)"/>
<g class="mono"><text class="cyan" x="42" y="48" font-size="12" font-weight="700" letter-spacing="2">LIVE / GITHUB SIGNAL</text><text class="muted" x="42" y="72" font-size="11">SOURCE: REST + GRAPHQL API</text><circle cx="963" cy="45" r="4" fill="#4ADE80"/><text class="muted" x="977" y="49" font-size="11">AUTO-SYNCED</text><text class="muted" x="1158" y="49" text-anchor="end" font-size="11">__UPDATED__</text></g>
<g transform="translate(42 96)">
  <g><rect class="card" width="207" height="116" rx="14"/><rect width="207" height="3" rx="1.5" fill="#4FE1E8"/><text class="mono muted" x="20" y="34" font-size="10" letter-spacing="1">CONTRIBUTIONS / 365D</text><text class="sans white" x="20" y="88" font-size="44" font-weight="750">__CONTRIBUTIONS__</text></g>
  <g transform="translate(225)"><rect class="card" width="207" height="116" rx="14"/><rect width="207" height="3" rx="1.5" fill="#62C7ED"/><text class="mono muted" x="20" y="34" font-size="10" letter-spacing="1">COMMITS / 365D</text><text class="sans white" x="20" y="88" font-size="44" font-weight="750">__COMMITS__</text></g>
  <g transform="translate(450)"><rect class="card" width="207" height="116" rx="14"/><rect width="207" height="3" rx="1.5" fill="#806CFF"/><text class="mono muted" x="20" y="34" font-size="10" letter-spacing="1">PUBLIC REPOSITORIES</text><text class="sans white" x="20" y="88" font-size="44" font-weight="750">__REPOS__</text></g>
  <g transform="translate(675)"><rect class="card" width="207" height="116" rx="14"/><rect width="207" height="3" rx="1.5" fill="#9A8CFF"/><text class="mono muted" x="20" y="34" font-size="10" letter-spacing="1">STARS RECEIVED</text><text class="sans white" x="20" y="88" font-size="44" font-weight="750">__STARS__</text></g>
  <g transform="translate(900)"><rect class="card" width="216" height="116" rx="14"/><rect width="216" height="3" rx="1.5" fill="#C0B7FF"/><text class="mono muted" x="20" y="34" font-size="10" letter-spacing="1">FOLLOWERS</text><text class="sans white" x="20" y="88" font-size="44" font-weight="750">__FOLLOWERS__</text></g>
</g>
"""
template += """
<g><rect class="card" x="42" y="238" width="710" height="144" rx="16"/><text class="mono violet" x="66" y="270" font-size="10" font-weight="700" letter-spacing="1.4">LATEST ACTIVE PROJECT</text><text class="sans white" x="66" y="317" font-size="30" font-weight="750">__LATEST__</text><text class="mono muted" x="66" y="350" font-size="11">PRIMARY LANGUAGE</text><text class="mono cyan" x="196" y="350" font-size="11">__LANG__</text><line class="rule" x1="292" y1="340" x2="292" y2="356"/><text class="mono muted" x="314" y="350" font-size="11">LAST PUSH __PUSHED__</text><text class="mono muted" x="728" y="350" text-anchor="end" font-size="10">PROFILE REPOSITORY EXCLUDED</text></g>
<g><rect class="card" x="774" y="238" width="384" height="144" rx="16"/><text class="mono cyan" x="798" y="270" font-size="10" font-weight="700" letter-spacing="1.4">CONTRIBUTION HEATMAP / 5W</text><text class="mono muted" x="1134" y="270" text-anchor="end" font-size="10">__ACTIVE_DAYS__ ACTIVE DAYS</text>__HEATMAP__</g>
<g class="mono"><text class="muted" x="42" y="405" font-size="10">VERIFIED PUBLIC DATA · GENERATED BY GITHUB ACTIONS</text><text class="muted" x="1158" y="405" text-anchor="end" font-size="10">github.com/NikitaRTN</text></g>
</svg>"""

values = {
    **{marker: str(value) for marker, value in metrics.items()},
    "__UPDATED__": updated,
    "__LATEST__": latest_name,
    "__LANG__": latest_lang,
    "__PUSHED__": latest_date,
    "__ACTIVE_DAYS__": str(active_days),
    "__HEATMAP__": "".join(heatmap),
}
for marker, value in values.items():
    template = template.replace(marker, value)

output = Path(__file__).resolve().parents[1] / "assets" / "live-stats.svg"
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(template, encoding="utf-8")
print("Generated", output)
