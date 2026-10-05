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

_Last updated: 2026-10-05 10:21 UTC by [update-readme.yml](../../actions/workflows/update-readme.yml)._

### Latest commits

| Commit | Message | Date |
| --- | --- | --- |
| [`d8e106c`](https://github.com/yishan2004931022-glitch/auto-readme-actions/commit/d8e106ca91e2302f2b2a9649391973d782231013) | chore(readme): refresh activity section [skip ci] | 2026-10-04 |
| [`cc33506`](https://github.com/yishan2004931022-glitch/auto-readme-actions/commit/cc33506ea35852b6cff3c4d508713548b344ea1f) | chore(readme): refresh activity section [skip ci] | 2026-10-03 |
| [`2e54832`](https://github.com/yishan2004931022-glitch/auto-readme-actions/commit/2e54832af4676552d08bf35a748187eeaa355feb) | chore(readme): refresh activity section [skip ci] | 2026-10-02 |
| [`6ee8e8a`](https://github.com/yishan2004931022-glitch/auto-readme-actions/commit/6ee8e8ad439a5ed7a6d04b02c4451913afdbc9f0) | chore(readme): refresh activity section [skip ci] | 2026-10-01 |
| [`be27527`](https://github.com/yishan2004931022-glitch/auto-readme-actions/commit/be275274a4cb00d04728a52e04490472b67f05b2) | chore(readme): refresh activity section [skip ci] | 2026-09-30 |

### Recent pull requests

| PR | Title | State |
| --- | --- | --- |
| [#2](https://github.com/yishan2004931022-glitch/auto-readme-actions/pull/2) | feat: auto-update README activity section | merged |

### Recent issues

| Issue | Title | State |
| --- | --- | --- |
| [#1](https://github.com/yishan2004931022-glitch/auto-readme-actions/issues/1) | Automate the README activity section via GitHub Actions | closed |

<!-- ACTIVITY:END -->

## Local development

```bash
export GITHUB_TOKEN=<a token with read access to this repo>
export REPO=yishan2004931022-glitch/auto-readme-actions
python scripts/update_readme.py          # writes README.md and .cache/activity.json
DRY_RUN=1 python scripts/update_readme.py  # prints the rendered section only
```
