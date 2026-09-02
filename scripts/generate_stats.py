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


user = request("https://api.github.com/users/" + LOGIN)

query = """
query($login: String!) {
  user(login: $login) {
    followers { totalCount }
    contributionsCollection {
      contributionCalendar { totalContributions }
      totalCommitContributions
      totalIssueContributions
      totalPullRequestContributions
      totalPullRequestReviewContributions
    }
    repositories(first: 100, privacy: PUBLIC, ownerAffiliations: OWNER,
      orderBy: {field: PUSHED_AT, direction: DESC}) {
      totalCount
      nodes { name stargazerCount forkCount pushedAt isFork primaryLanguage { name } }
    }
  }
}
"""
graph = request(
    "https://api.github.com/graphql",
    {"query": query, "variables": {"login": LOGIN}},
)
if graph.get("errors"):
    raise RuntimeError(json.dumps(graph["errors"], ensure_ascii=False))
profile = graph["data"]["user"]
contrib = profile["contributionsCollection"]
repos = profile["repositories"]["nodes"]

public_repos = profile["repositories"]["totalCount"]
followers = profile["followers"]["totalCount"]
contributions = contrib["contributionCalendar"]["totalContributions"]
commits = contrib["totalCommitContributions"]
total_stars = sum(repo["stargazerCount"] for repo in repos)
latest = repos[0] if repos else None
latest_name = latest["name"] if latest else "—"
latest_lang = (latest.get("primaryLanguage") or {}).get("name", "mixed") if latest else "—"
updated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

values = {
    "__CONTRIBUTIONS__": str(contributions),
    "__COMMITS__": str(commits),
    "__REPOS__": str(public_repos),
    "__FOLLOWERS__": str(followers),
    "__STARS__": str(total_stars),
    "__LATEST__": html.escape(latest_name),
    "__LANG__": html.escape(latest_lang),
    "__UPDATED__": updated,
    "__LOGIN__": html.escape(user["login"]),
}

template = """<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="300" viewBox="0 0 1000 300" role="img" aria-labelledby="title desc">
<title id="title">Live GitHub statistics for __LOGIN__</title>
<desc id="desc">Automatically generated from the GitHub API</desc>
<defs>
  <linearGradient id="accent" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#2783DE"/><stop offset="1" stop-color="#5E9FE8"/></linearGradient>
  <style>.text{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}.surface{fill:#F9F8F7;stroke:#E6E5E3}.label{fill:#7D7A75}.value{fill:#2C2C2B}.accent{fill:url(#accent)}@media(prefers-color-scheme:dark){.surface{fill:#202020;stroke:rgba(255,255,255,.2)}.label{fill:rgba(255,255,255,.65)}.value{fill:#fff}}</style>
</defs>
<rect class="surface" x="1" y="1" width="998" height="298" rx="16"/>
<g class="text"><text class="value" x="32" y="42" font-size="20" font-weight="700">GitHub activity</text><circle cx="950" cy="35" r="6" fill="#46A171"/><text class="label" x="934" y="40" text-anchor="end" font-size="13">AUTO-SYNCED</text>
<g transform="translate(32 68)">
  <rect class="surface" width="220" height="116" rx="12"/><rect class="accent" width="5" height="116" rx="2.5"/><text class="label" x="24" y="34" font-size="13">ВКЛАД ЗА 365 ДНЕЙ</text><text class="value" x="24" y="84" font-size="42" font-weight="750">__CONTRIBUTIONS__</text>
  <rect class="surface" x="238" width="220" height="116" rx="12"/><text class="label" x="262" y="34" font-size="13">КОММИТЫ ЗА 365 ДНЕЙ</text><text class="value" x="262" y="84" font-size="42" font-weight="750">__COMMITS__</text>
  <rect class="surface" x="476" width="220" height="116" rx="12"/><text class="label" x="500" y="34" font-size="13">ПУБЛИЧНЫЕ РЕПОЗИТОРИИ</text><text class="value" x="500" y="84" font-size="42" font-weight="750">__REPOS__</text>
  <rect class="surface" x="714" width="220" height="116" rx="12"/><text class="label" x="738" y="34" font-size="13">ПОДПИСЧИКИ</text><text class="value" x="738" y="84" font-size="42" font-weight="750">__FOLLOWERS__</text>
</g>
<line x1="32" y1="212" x2="968" y2="212" stroke="#2783DE" stroke-opacity=".14"/>
<text class="label" x="32" y="246" font-size="13">ПОСЛЕДНИЙ АКТИВНЫЙ РЕПОЗИТОРИЙ</text><text class="value" x="32" y="272" font-size="18" font-weight="650">__LATEST__ · __LANG__</text>
<text class="label" x="968" y="246" text-anchor="end" font-size="13">ЗВЁЗДЫ: __STARS__</text><text class="label" x="968" y="272" text-anchor="end" font-size="13">Обновлено __UPDATED__</text></g>
</svg>"""
for marker, value in values.items():
    template = template.replace(marker, value)

output = Path(__file__).resolve().parents[1] / "assets" / "live-stats.svg"
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(template, encoding="utf-8")
print("Generated", output)
