# TODOS

## T1: 添加 README + 一键安装文档
**Why:** 开源项目想让别人 Fork 使用，但无 README 时没人会尝试。
**Pros:** 降低 Fork 门槛，增加开源认可度。
**Cons:** 需要 30 分钟（CC 可以帮忙）。
**Context:** 需要说明：Twitter API 申请步骤、GitHub Secrets 配置（ANTHROPIC_API_KEY）、people.yml 修改方法、如何在 Repo Settings 中开启 GitHub Pages。
**Depends on:** 核心功能完成后再写

## T2: 考虑将每日自动 commit 放到独立 data/gh-pages 分支
**Why:** main 分支每天多一条自动 commit，将来 review PR 时历史很噪。
**Pros:** main 分支只有人工修改，分支历史干净。
**Cons:** Actions 配置更复杂，V1 不必要。
**Context:** 如果未来有贡献者提 PR，混乱的 main 历史会增加 review 难度。参考：很多类似的 GitHub data 项目（如 github-activity-readme）用 gh-pages 分支存放生成内容。
**Depends on:** 等项目有外部贡献者后再评估
