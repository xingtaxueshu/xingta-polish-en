# 示例：案例 08（OLS 结果段）

> 自编中性样例，非真实论文。展示数字/术语保护与「保留并提问」。

## 原文

Table 3 reports the results of the OLS regressions. In Column (1), the coefficient of family income is 0.083 (SE = 0.021), and it is significant at the 1% level. After adding the controls of parents' education in Column (2), the coefficient decreases to 0.051 and still significant at the 5% level. It can be seen that the family income has a obvious effect on students' reading time. Moreover, the R² of Column (2) is 0.214, much higher than Column (1), which is 0.097.


## 本 skill（v2）润色文本

Table 3 reports the results of the OLS regressions. In Column (1), the coefficient on family income is 0.083 (SE = 0.021), and it is significant at the 1% level. After adding parents' education as controls in Column (2), the coefficient decreases to 0.051 and is still significant at the 5% level. It can be seen that family income has an obvious effect on students' reading time. Moreover, the R² of Column (2) is 0.214, much higher than that of Column (1), which is 0.097.


## 二、修改清单

| # | 类型 | 原文片段 | 修改后片段 | 影响语义？ | 原因 |
|---|---|---|---|---|---|
| 1 | 介词与搭配 | `the coefficient of family income` | `the coefficient on family income` | 否 | 回归系数惯用 coefficient on |
| 2 | 词汇选择 | `After adding the controls of parents' education in Column (2)` | `After adding parents' education as controls in Column (2)` | 否 | 更自然的搭配 |
| 3 | 一致 | `and still significant` | `and is still significant` | 否 | 补谓语 |
| 4 | 冠词 | `the family income has a obvious` | `family income has an obvious` | 否 | 泛指；a/an |
| 5 | 比较结构 | `than Column (1), which is 0.097` | `than that of Column (1), which is 0.097` | 否 | 比较对象应为 R² |

## 三、保留审计

- 脚本 check_invariants.py（术语：OLS, R², Column (1), Column (2), SE = 0.021）输出：
```
RESULT: PASS (0 errors, 0 warnings)
提示：通过只说明数字/引用/引语/术语形式一致，不代表论断强度未变，仍需人工审阅。
```
- 处置：无 ERROR/WARN，无需处置。
- 清单覆盖自查：已用 diff 对照：未发现未记录的改动词。
- 论断强度：已逐句对照 hedge、量词、因果词；原有 hedge 全部保留（见问题清单中标注的保留项）。

## 四、给作者的问题与风险提示

1. “obvious effect”：横截面 OLS 系数能否支持 effect 的措辞取决于研究设计；我保留原词，请自行判断是否改为 association。
2. “significant at the 1% level”等：数字未改动，我不核算。
