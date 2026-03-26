# Changelog

All notable changes to this project will be documented in this file.

## [0.2.1.0] - 2026-03-26

### Changed
- 设计系统全面更新（v2）：强调色从琥珀金 `#B8730A` 改为森林绿 `#15803D`，深色模式背景改为微绿近黑 `#0A0F0D`
- 刊头字体从 Fraunces 衬线体改为 Clash Grotesk 几何粗体；正文字体从 Plus Jakarta Sans 改为 Source Sans 3
- 美学方向从"精致编辑风"调整为"专业编辑 / 财经媒体感（Financial Times 风格）"
- 配色方案从暖色中性调改为冷色中性调
- 更新 CLAUDE.md 设计系统核心原则以匹配新设计规范

## [0.2.0.0] - 2026-03-22

### Added
- README with GitHub Pages link, Fork setup guide, and local run instructions
- `gh-pages` branch deployment: static site now lives on a dedicated orphan branch, keeping `main` clean
- `.nojekyll` in `gh-pages` to prevent Jekyll processing

### Changed
- GitHub Actions workflow split into two steps: commit `processed_ids.json` to `main`, deploy HTML to `gh-pages`
- Redesigned page template: modern card layout with subtle shadows, hover effects, clean typography, and CSS custom properties
- Footer simplified to a single "历史存档" archive link
- `docs/` added to `.gitignore` — generated files are build artifacts, not source

### Removed
- `docs/.gitkeep`, `docs/index.html`, `docs/archive/` from `main` branch tracking

## [0.1.0.0] - 2026-03-22

### Added
- Initial pipeline: daily fetch of tweets from Sam Altman, Dario Amodei, and Andrej Karpathy via Twitter API Free Tier (tweepy)
- Claude Haiku translation with TITLE: / SUMMARY: format and robust fallback parsing for malformed LLM output
- Jinja2 HTML rendering to `docs/index.html` and `docs/archive/YYYY-MM-DD.html` (GitHub Pages compatible)
- Tweet deduplication via `processed_ids.json` committed to repo
- GitHub Actions daily cron at 01:00 UTC (09:00 BJT) with `workflow_dispatch` for manual testing
- Configurable people list via `people.yml` with per-person source enable/disable
- 21 pytest tests covering all core functions including fetch_tweets, translate, and main env-check paths
