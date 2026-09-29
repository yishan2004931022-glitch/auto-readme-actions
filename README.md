# auto-readme-actions

[![Update README](https://github.com/yishan2004931022-glitch/auto-readme-actions/actions/workflows/update-readme.yml/badge.svg)](https://github.com/yishan2004931022-glitch/auto-readme-actions/actions/workflows/update-readme.yml)
[![Validate markers](https://github.com/yishan2004931022-glitch/auto-readme-actions/actions/workflows/validate-markers.yml/badge.svg)](https://github.com/yishan2004931022-glitch/auto-readme-actions/actions/workflows/validate-markers.yml)

A small DevOps exercise: a GitHub Actions pipeline keeps the section below in sync with
recent repository activity, so the README never has to be updated by hand.

## How it works

1. `update-readme.yml` runs on a daily schedule, on every push to `main`, and on demand.
2. `scripts/update_readme.py` queries the GitHub REST API (with rate-limit backoff),
   caches the result in `.cache/activity.json`, and rewrites the text between the markers.
3. The workflow commits only when the rendered section actually changed, so repeated runs
   are idempotent and do not create empty commits.

The two HTML comments below are the markers. Everything between them is generated —
do not edit it by hand. `validate-markers.yml` fails CI if either marker goes missing.

## Repository activity

<!-- ACTIVITY:START -->
_This section is generated automatically. The first workflow run will replace it._
<!-- ACTIVITY:END -->

## Local development

```bash
export GITHUB_TOKEN=<a token with read access to this repo>
export REPO=yishan2004931022-glitch/auto-readme-actions
python scripts/update_readme.py          # writes README.md and .cache/activity.json
DRY_RUN=1 python scripts/update_readme.py  # prints the rendered section only
```
