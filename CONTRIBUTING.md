# 贡献指南 · Contributing

感谢你愿意改进 xingta-polish-en。这个项目的立场是**保真优先**：只润色语言，不改论点、数据、引文、结论。贡献请围绕这一点。

## 欢迎的贡献

- 使用反馈：哪个学科、哪个 Agent、哪一步出了问题（请用 Issue 里的“使用反馈”模板）。
- 新的中式英语模式（`references/chinglish-patterns.md`）：请给出「原句 → 改句 → 原因」，并保证改句不改变原意。
- 学科或期刊风格的补充、引文格式注意事项的修正。
- 脚本的 bug 修复（`scripts/`，仅用标准库）。

## 请避免

- 加入“规避 AI 检测 / 免查重”之类的承诺。
- 在样例中使用真实、未发表或他人的稿件；样例请自编、中性。
- 夸大效果。评测声明和局限要如实保留。

## 提交流程

1. Fork 后新建分支，改动尽量小而可审。
2. 改了 `scripts/` 的话，请跑一下 `python3 evals/score.py A B2`，并在 PR 中说明结果。
3. 开 Pull Request，说明改了什么、为什么。

Issue 或 PR 里请不要粘贴未发表稿件的全文或可识别个人的信息。

---

*English:* Contributions are welcome, especially usage feedback, new "original → revised → reason" patterns, discipline-specific notes and script fixes. Please keep the fidelity-first principle, do not add claims about evading AI detection, and use self-written neutral examples rather than real unpublished manuscripts. Open a small, reviewable PR and explain what changed and why.
