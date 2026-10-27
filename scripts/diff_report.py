#!/usr/bin/env python3
"""diff_report.py — 生成润色前后的逐句对照表（Markdown）

用法：
  python3 diff_report.py before.txt after.txt [--format md|json]
说明：句子按简单规则切分（会避开 et al.、e.g.、Fig.、p.、小数点）；
词级差异用 ~~删除~~ 与 **新增** 标出。1:1 替换逐句配对，句数不等的替换块合并成一行并标注“合并/拆分”。
仅依赖标准库。
"""
import argparse
import difflib
import json
import re
import sys

ABBR = r"(?:et al|e\.g|i\.e|cf|vs|Fig|Figs|Eq|No|Dr|Prof|pp?|ed|eds|trans|vol|Mr|Ms)"


def split_sentences(text):
    text = re.sub(r"\s+", " ", text.strip())
    protected = re.sub(rf"\b({ABBR})\.", lambda m: m.group(1) + "<DOT>", text)
    protected = re.sub(r"(\d)\.(\d)", r"\1<DOT>\2", protected)
    parts, last = [], 0
    for m in re.finditer(r"[.!?][\"”’)\]]*(?:\[\^?\w+\])*(\s+)(?=[\"“(\[]?[A-Z0-9])", protected):
        parts.append(protected[last:m.start(1)])
        last = m.end(1)
    parts.append(protected[last:])
    return [p.replace("<DOT>", ".").strip() for p in parts if p.strip()]


TOK = re.compile(r"\S+")


def word_diff(a, b):
    ta, tb = TOK.findall(a), TOK.findall(b)
    sm = difflib.SequenceMatcher(None, ta, tb, autojunk=False)
    out = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            out.append(" ".join(ta[i1:i2]))
        else:
            if i2 > i1:
                out.append("~~" + " ".join(ta[i1:i2]) + "~~")
            if j2 > j1:
                out.append("**" + " ".join(tb[j1:j2]) + "**")
    return " ".join(out)


def align(before, after):
    sb, sa = split_sentences(before), split_sentences(after)
    sm = difflib.SequenceMatcher(None, sb, sa, autojunk=False)
    rows = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            for k in range(i2 - i1):
                rows.append((sb[i1 + k], sa[j1 + k], "未改动"))
        elif op == "delete":
            for s in sb[i1:i2]:
                rows.append((s, "", "删除"))
        elif op == "insert":
            for s in sa[j1:j2]:
                rows.append(("", s, "新增"))
        else:
            if i2 - i1 == j2 - j1:
                for k in range(i2 - i1):
                    rows.append((sb[i1 + k], sa[j1 + k], "修改"))
            else:
                tag = "合并" if (i2 - i1) > (j2 - j1) else "拆分"
                rows.append((" ".join(sb[i1:i2]), " ".join(sa[j1:j2]), f"{tag}({i2-i1}→{j2-j1})"))
    return rows


def esc(s):
    return s.replace("|", "\\|")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("before")
    ap.add_argument("after")
    ap.add_argument("--format", choices=["md", "json"], default="md")
    args = ap.parse_args()
    try:
        before = open(args.before, encoding="utf-8").read()
        after = open(args.after, encoding="utf-8").read()
    except OSError as e:
        print(f"读取失败: {e}", file=sys.stderr)
        return 2
    rows = align(before, after)
    if args.format == "json":
        print(json.dumps([{"n": i + 1, "before": b, "after": a, "status": s,
                           "diff": word_diff(b, a) if b and a else ""}
                          for i, (b, a, s) in enumerate(rows)], ensure_ascii=False, indent=2))
        return 0
    changed = sum(1 for r in rows if r[2] != "未改动")
    print(f"共 {len(rows)} 行，其中改动 {changed} 行。\n")
    print("| # | 原句 | 润色后 | 状态 | 词级差异（~~删~~ **增**） |")
    print("|---|------|--------|------|------------------------|")
    for i, (b, a, s) in enumerate(rows, 1):
        d = word_diff(b, a) if (b and a and s != "未改动") else ""
        print(f"| {i} | {esc(b)} | {esc(a)} | {s} | {esc(d)} |")
    return 0


if __name__ == "__main__":
    sys.exit(main())
