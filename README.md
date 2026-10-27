# xingta-polish-en · 星塔学术英文润色 Skill

> 面向中文人文社科作者的**保真优先**英文学术润色 Agent Skill。
> 核心立场：**只润色语言，不改论点、数据、引文、结论**；看不准的地方标出来问作者，不替作者拍板。

> ⚠️ **评测声明**：本仓库附带的实验（`evals/results.md`）是**同一模型的自我评测**，**不是真实作者盲评**；12 个样例是**自编中性段落，不是真实论文**。结论只代表“这套工作流在自编样例上的行为差异”，不代表真实投稿效果。

## 它是什么

一个遵循 SKILL.md 约定的 Agent Skill（可用于 Claude Code、Codex、Cursor 等支持 Skill 的环境，也可把 SKILL.md 当作系统提示使用）。它让助手在润色英文论文段落时遵守一套固定流程：

1. 开始前确认：学科、章节、目标期刊、润色强度（轻 / 标准 / 大改）、文本载体。
2. 先建“保留台账”（数字、引文、引语、术语、专名、hedge、脚注），再分三遍润色：语法正确 → 中式英语与衔接 → 学科/期刊风格。
3. 用 `scripts/check_invariants.py` 机器核对数字、引用、引语、术语是否被改动。
4. 固定输出四部分：润色文本；逐条编号的修改清单（类型 + 是否影响语义）；保留审计；给作者的问题与风险提示。

### 铁律（摘要，完整见 SKILL.md）

- 只改语言，不改论证、数据、引文、结论。
- 不编造：不加事实、文献、数字、因果。
- 怀疑事实有问题，只标记，不改。
- **不承诺规避 AI 检测，也不提供“降重/免查重”**；并提醒：检测工具对非母语写作者存在误判风险。
- 未发表稿件的保密提示：处理前请确认所用工具与平台的数据政策。
- AI 使用披露以**目标期刊的要求为准**（`references/disclosure-templates.md` 只是起点）。

## 目录

```
SKILL.md                    # 入口：铁律 + 工作流（≤200 行）
references/
  invariants.md             # 保留台账 + 论断强度审计
  chinglish-patterns.md     # 45 条「原句→改句→原因」中式英语模式库
  humanities-argument.md    # 人文社科论证写法（综述、框架、界定、对话式引用…）
  citation-styles.md        # 引文格式注意事项（只统一格式，不补文献）
  disclosure-templates.md   # AI 使用披露模板（以期刊要求为准）
  output-contract.md        # 四部分输出规范
scripts/
  check_invariants.py       # 数字/引用/引语/术语保留检查（仅标准库）
  diff_report.py            # 逐句对照 Markdown 表（词级删改标记）
evals/                      # 实验：cases / runs / score.py / rubric.md / results.md
examples/                   # 完整示例
LICENSE                     # MIT
```

## 安装

**Skill 目录方式（示例，路径按你的环境调整）**

```bash
git clone <本仓库地址> ~/.claude/skills/xingta-polish-en     # Claude Code
# 或复制到你所用工具的 skills 目录
```

**仅用脚本**：只需 Python 3.9+，无第三方依赖。

## 使用示例

对助手说：

> 用 xingta-polish-en 润色下面这段，学科：教育学，章节：文献综述，目标期刊：SSCI 教育类，强度：标准。

助手会先确认缺失的信息，再输出四部分。你也可以单独用脚本核对：

```bash
python3 scripts/check_invariants.py 原文.txt 润色后.txt --terms-file terms.txt
python3 scripts/diff_report.py 原文.txt 润色后.txt            # 逐句对照
python3 evals/score.py A B2                                    # 复现实验计分
```

完整示例见 `examples/`（含与“通用提示”的对比）。

## 实验结果速览（请连同上面的声明一起读）

12 个自编样例、85 个预埋语言问题（详见 `evals/results.md`）：

| | 通用提示（A） | 本 skill v2（B2） |
|---|---|---|
| 预埋问题修复 | 85/85 | 79/85 |
| 保留项丢失 | 2 | 0 |
| 论断/指称实质改变（人工复核） | 8 处（6 例涉及） | 0 |
| 平均编辑比例 | 0.256 | 0.118 |

要点：通用提示修语法很彻底，但会悄悄把“很多”写成“大量”、把“有助于”写成“促进”、替作者补一个新的强论断；本 skill 更保守，代价是修复率略低、输出更长、需要作者看清单。计分有事后修正与自评偏差，v2 的部分修改由 v1 实验触发，详见 results.md。

## 局限

- 自评 + 自编样例：没有真实作者盲评，没有母语审稿人评分。
- 评分用正则代理指标，对时态、连字符等有争议项不严谨。
- `check_invariants.py` 只检查字符串层面的保留，**不能判断论断强度是否改变**；强度审计依赖人工。
- 不核实事实与文献真伪；不保证目标期刊的格式与政策合规。
- 不做翻译质量担保；对严重病句、逻辑断裂的段落，只能标出并提问，不能替作者补论证。
- **不提供也不承诺任何“通过 AI 检测”“规避查重”的效果。**

## 致谢与参考

本项目的结构思路参考了以下开源项目；**只借鉴思路，所有文字均为重写，没有复制其正文**。请到原仓库查看其完整内容与许可证：

- [Yila-AI/awesome-research-skills](https://github.com/Yila-AI/awesome-research-skills) 中的 `sci-ssci-polishing`（保留台账、论断强度保守处理的思路）
- [Yuan1z0825/nature-skills](https://github.com/Yuan1z0825/nature-skills) 中的 `nature-polishing`（分章节润色、术语/数值一致性扫描的思路）
- [Haojae/scipilot-writing-skill](https://github.com/Haojae/scipilot-writing-skill)（开始前逐项询问、脚本自检、修改日志的思路）

本项目聚焦人文社科、保真优先与可核对的输出契约，与上述项目定位不同，不是它们的替代品或衍生版本。

## 许可

MIT，© 2026 星塔学术。见 [LICENSE](LICENSE)。
