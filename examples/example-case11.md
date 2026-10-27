# 示例：案例 11（博物馆线上展览，引言段）

> 自编中性样例，非真实论文。展示同一段落在「通用提示」与「本 skill」下的差别。

## 原文

With the rapid development of digital technology, the museum is playing a more and more important role in the cultural life of people. Recently, many museums have launched the online exhibition, and the number of the visitors of online exhibition has grown rapidly. But there is few research discuss the experience of the visitors in the online exhibition. Therefore, it is of great significance to study the visitors' experience of online exhibition from the perspective of narrative. This paper takes the online exhibitions of three provincial museums for example, and analyze the narrative strategies.


## A：通用提示 "Polish this academic paragraph."

Digital technology has transformed the role of museums in contemporary cultural life. In recent years, many museums have launched online exhibitions, and the number of online visitors has grown rapidly. However, little research has examined visitors' experience of online exhibitions. It is therefore important to study this experience from a narrative perspective. This paper takes the online exhibitions of three provincial museums as examples and analyzes their narrative strategies.


注意：A 把 "playing more and more important role" 改成了 "Digital technology has transformed the role of museums"——这是**新增的因果/强论断**，原文并未这样说。

## B：本 skill（v2）

### 一、润色文本

Museums are playing an increasingly important role in cultural life as digital technology develops rapidly. Recently, many museums have launched online exhibitions, and the number of visitors to online exhibitions has grown rapidly. However, there is little research on visitors' experience of online exhibitions. Therefore, it is important to study visitors' experience of online exhibitions from the perspective of narrative. This paper takes the online exhibitions of three provincial museums as examples and analyzes the narrative strategies.


## 二、修改清单

| # | 类型 | 原文片段 | 修改后片段 | 影响语义？ | 原因 |
|---|---|---|---|---|---|
| 1 | 套话/语序 | `With the rapid development of digital technology, the museum is playing a more and more important role in the cultural life of people` | `Museums are playing an increasingly important role in cultural life as digital technology develops rapidly` | 轻微 | 保留“技术发展”与“作用增强”两层；people 删去，请确认“cultural life”不需限定 |
| 2 | 冠词/名词堆叠 | `launched the online exhibition, and the number of the visitors of online exhibition` | `launched online exhibitions, and the number of visitors to online exhibitions` | 否 | 复数泛指；of 结构改为 visitors to |
| 3 | 语法 | `But there is few research discuss the experience of the visitors in the online exhibition` | `However, there is little research on visitors' experience of online exhibitions` | 否 | few research 不成立；动词缺失；little research 保留“很少”的强度 |
| 4 | 套话 | `it is of great significance to study` | `it is important to study` | 轻微 | 空泛套话改为朴素表达，强度降一档，请确认 |
| 5 | 词汇选择 | `takes the online exhibitions of three provincial museums for example` | `takes the online exhibitions of three provincial museums as examples` | 否 | 固定搭配 |
| 6 | 一致 | `and analyze the narrative strategies` | `and analyzes the narrative strategies` | 否 | 单数主语 |

## 三、保留审计

- 脚本 check_invariants.py（术语：narrative strategies, three provincial museums）输出：
```
RESULT: PASS (0 errors, 0 warnings)
提示：通过只说明数字/引用/引语/术语形式一致，不代表论断强度未变，仍需人工审阅。
```
- 处置：无 ERROR/WARN，无需处置。
- 清单覆盖自查：已用 diff 对照：下列词的改动未在清单中出现，需补记或确认是否为对齐假象：['therefore']。
- 论断强度：已逐句对照 hedge、量词、因果词；原有 hedge 全部保留（见问题清单中标注的保留项）。

## 四、给作者的问题与风险提示

1. 开头句把“随着数字技术发展，博物馆作用越来越重要”改成 as 从句：因果关联无出处，请考虑补充文献。
2. “there is little research ...”是存在性断言，建议补充综述依据。
