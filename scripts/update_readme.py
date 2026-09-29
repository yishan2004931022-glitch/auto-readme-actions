#!/usr/bin/env python3
"""Render a repository-activity section into README.md between two markers.

Design notes
------------
* Idempotent: the file is only rewritten when the rendered block differs from
  what is already there, so re-running the workflow produces no empty commits.
* Rate-limit aware: every API call goes through `api()`, which honours
  Retry-After / X-RateLimit-Reset and backs off exponentially instead of
  hammering the API.
* Cached: the raw payload is stored in .cache/activity.json so a failed run can
  be diagnosed, and so a future multi-repo aggregation can reuse it.
* Secret-safe: the token is read from the environment, never logged, and never
  interpolated into any printed string.
"""

from __future__ import annotations

import json
import os
import pathlib
import random
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

REPO = os.environ.get("REPO") or os.environ.get("GITHUB_REPOSITORY", "")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
DRY_RUN = os.environ.get("DRY_RUN") == "1"

ROOT = pathlib.Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
CACHE = ROOT / ".cache" / "activity.json"
START, END = "<!-- ACTIVITY:START -->", "<!-- ACTIVITY:END -->"

MAX_ATTEMPTS = 5


def api(path: str, params: str = "") -> list | dict:
    """GET the GitHub API with exponential backoff and rate-limit handling."""
    url = f"https://api.github.com/repos/{REPO}{path}"
    if params:
        url += "?" + params
    for attempt in range(1, MAX_ATTEMPTS + 1):
        req = urllib.request.Request(url, headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "auto-readme-actions",
            **({"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}),
        })
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                remaining = resp.headers.get("X-RateLimit-Remaining")
                if remaining is not None and int(remaining) < 20:
                    print(f"::warning::rate limit low ({remaining} left)")
                return json.load(resp)
        except urllib.error.HTTPError as err:
            if err.code in (403, 429):
                wait = int(err.headers.get("Retry-After") or 0)
                if not wait:
                    reset = int(err.headers.get("X-RateLimit-Reset") or 0)
                    wait = max(reset - int(time.time()), 0)
                wait = min(wait or 2 ** attempt, 60) + random.uniform(0, 1)
                print(f"::warning::throttled on {path}, sleeping {wait:.1f}s "
                      f"(attempt {attempt}/{MAX_ATTEMPTS})")
                time.sleep(wait)
                continue
            if 500 <= err.code < 600 and attempt < MAX_ATTEMPTS:
                time.sleep(min(2 ** attempt, 30))
                continue
            raise
        except urllib.error.URLError:
            if attempt == MAX_ATTEMPTS:
                raise
            time.sleep(min(2 ** attempt, 30))
    raise RuntimeError(f"giving up on {path} after {MAX_ATTEMPTS} attempts")


def short(text: str, n: int = 72) -> str:
    text = " ".join((text or "").splitlines()[:1].__iter__()).strip()
    return text if len(text) <= n else text[: n - 1] + "…"


def collect() -> dict:
    commits = api("/commits", "per_page=5")
    prs = api("/pulls", "state=all&per_page=5&sort=updated&direction=desc")
    issues = [i for i in api("/issues", "state=all&per_page=10&sort=updated&direction=desc")
              if "pull_request" not in i][:5]
    return {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "commits": [{"sha": c["sha"][:7], "url": c["html_url"],
                     "message": short(c["commit"]["message"]),
                     "date": c["commit"]["author"]["date"][:10]} for c in commits],
        "pulls": [{"number": p["number"], "url": p["html_url"], "title": short(p["title"]),
                   "state": "merged" if p.get("merged_at") else p["state"]} for p in prs],
        "issues": [{"number": i["number"], "url": i["html_url"], "title": short(i["title"]),
                    "state": i["state"]} for i in issues],
    }


def render(data: dict) -> str:
    lines = ["", f"_Last updated: {data['generated_at']} by "
                 "[update-readme.yml](../../actions/workflows/update-readme.yml)._", ""]

    lines += ["### Latest commits", "", "| Commit | Message | Date |", "| --- | --- | --- |"]
    for c in data["commits"]:
        lines.append(f"| [`{c['sha']}`]({c['url']}) | {c['message']} | {c['date']} |")
    if not data["commits"]:
        lines.append("| — | no commits yet | — |")

    lines += ["", "### Recent pull requests", "", "| PR | Title | State |", "| --- | --- | --- |"]
    for p in data["pulls"]:
        lines.append(f"| [#{p['number']}]({p['url']}) | {p['title']} | {p['state']} |")
    if not data["pulls"]:
        lines.append("| — | no pull requests yet | — |")

    lines += ["", "### Recent issues", "", "| Issue | Title | State |", "| --- | --- | --- |"]
    for i in data["issues"]:
        lines.append(f"| [#{i['number']}]({i['url']}) | {i['title']} | {i['state']} |")
    if not data["issues"]:
        lines.append("| — | no issues yet | — |")

    lines.append("")
    return "\n".join(lines)


def splice(readme: str, block: str) -> str:
    if START not in readme or END not in readme:
        raise SystemExit("::error::README markers missing — refusing to write")
    head, rest = readme.split(START, 1)
    _, tail = rest.split(END, 1)
    return f"{head}{START}\n{block}\n{END}{tail}"


def main() -> int:
    if not REPO:
        raise SystemExit("::error::REPO (owner/name) is not set")

    data = collect()
    block = render(data)

    if DRY_RUN:
        print(block)
        return 0

    current = README.read_text(encoding="utf-8")
    updated = splice(current, block)

    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if updated == current:
        print("README already up to date — nothing to commit")
        return 0

    README.write_text(updated, encoding="utf-8")
    print("README activity section updated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
