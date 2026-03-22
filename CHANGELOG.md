# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0.0] - 2026-03-22

### Added
- Initial pipeline: daily fetch of tweets from Sam Altman, Dario Amodei, and Andrej Karpathy via Twitter API Free Tier (tweepy)
- Claude Haiku translation with TITLE: / SUMMARY: format and robust fallback parsing for malformed LLM output
- Jinja2 HTML rendering to `docs/index.html` and `docs/archive/YYYY-MM-DD.html` (GitHub Pages compatible)
- Tweet deduplication via `processed_ids.json` committed to repo
- GitHub Actions daily cron at 01:00 UTC (09:00 BJT) with `workflow_dispatch` for manual testing
- Configurable people list via `people.yml` with per-person source enable/disable
- 21 pytest tests covering all core functions including fetch_tweets, translate, and main env-check paths
