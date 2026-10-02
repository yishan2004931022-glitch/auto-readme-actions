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

_Last updated: 2026-10-02 09:42 UTC by [update-readme.yml](../../actions/workflows/update-readme.yml)._

### Latest commits

| Commit | Message | Date |
| --- | --- | --- |
| [`6ee8e8a`](https://github.com/yishan2004931022-glitch/auto-readme-actions/commit/6ee8e8ad439a5ed7a6d04b02c4451913afdbc9f0) | chore(readme): refresh activity section [skip ci] | 2026-10-01 |
| [`be27527`](https://github.com/yishan2004931022-glitch/auto-readme-actions/commit/be275274a4cb00d04728a52e04490472b67f05b2) | chore(readme): refresh activity section [skip ci] | 2026-09-30 |
| [`b255bfd`](https://github.com/yishan2004931022-glitch/auto-readme-actions/commit/b255bfdaff4b363df620c0ae66322ce623b50fa3) | chore(readme): refresh activity section [skip ci] | 2026-09-30 |
| [`81e4f4c`](https://github.com/yishan2004931022-glitch/auto-readme-actions/commit/81e4f4cabd4f725f09d0b473ec99b05862cd69a9) | chore(readme): refresh activity section [skip ci] | 2026-09-29 |
| [`21f3047`](https://github.com/yishan2004931022-glitch/auto-readme-actions/commit/21f3047dbc7e3b87a99baa79d13bddf762ef8155) | feat: auto-update README activity section (#2) | 2026-09-29 |

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
