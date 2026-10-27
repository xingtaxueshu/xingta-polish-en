#!/usr/bin/env python3
"""check_invariants.py — 润色前后「必须保留项」一致性检查（星塔学术 xingta-polish-en）

对比润色前后两份文本，检查：
  1. 数字（含小数、百分比、千分位、年代如 1850s；英文数词 two–twelve/twenty 归一化为数字）
  2. 括号/叙述式引用，如 (Author, 2020)、Krashen (2004)、[1]、[^2]、p. 5
  3. 直接引语（双引号内文字）
  4. 专有名词（句中大写词，启发式；只给警告）
  5. 指定术语（--term / --terms-file，大小写敏感，缺失即报错）

用法：
  python3 check_invariants.py before.txt after.txt [--term "difference-in-differences"] \
      [--terms-file terms.txt] [--json]
退出码：0 无错误；1 有错误（保留项丢失/被改/新增）；2 用法错误。
仅依赖 Python 3 标准库。它只做形式检查，不能判断语义是否变化。
"""
import argparse
import difflib
import json
import re
import sys
from collections import Counter

NUM_WORDS = {
    "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7",
    "eight": "8", "nine": "9", "ten": "10", "eleven": "11", "twelve": "12", "twenty": "20",
}
# 注意：不归一化 "one"（常作代词）；"first/second" 等序数词不检查。

FOOTNOTE_RE = re.compile(r"\[\^?[\w-]+\]")
NUM_RE = re.compile(r"(?<![\w.])\d+(?:,\d{3})*(?:\.\d+)?(?:%|s\b)?")
WORD_NUM_RE = re.compile(r"\b(" + "|".join(NUM_WORDS) + r")\b", re.I)
PAREN_CITE_RE = re.compile(r"\((?:see |cf\. |e\.g\., )?[A-Z][^()]*?\d{4}[a-z]?[^()]*\)")
NARR_CITE_RE = re.compile(
    r"[A-Z][\w'’\-]+(?:,? (?:et al\.|and|&) ?[A-Z]?[\w'’\-]*)* \(\d{4}[a-z]?(?:, [^()]*)?\)")
NUMERIC_CITE_RE = re.compile(r"\[\d+(?:\s*[,–-]\s*\d+)*\]")
PAGE_RE = re.compile(r"\bpp?\.\s*\d+(?:\s*[–-]\s*\d+)?")
QUOTE_RE = re.compile(r"[“\"]([^”\"\n]{3,}?)[”\"]")
CAP_RE = re.compile(r"\b[A-Z][A-Za-z'’\-]*[A-Za-z]\b|\b[A-Z]{2,}\b")


def norm_ws(s):
    return re.sub(r"\s+", " ", s.replace("’", "'")).strip()


def extract_numbers(text):
    t = FOOTNOTE_RE.sub(" ", text)
    out = [m.group(0).replace(",", "") for m in NUM_RE.finditer(t)]
    out += [NUM_WORDS[m.group(1).lower()] for m in WORD_NUM_RE.finditer(t)]
    return Counter(out)


def extract_citations(text):
    found = []
    for rx in (PAREN_CITE_RE, NARR_CITE_RE, NUMERIC_CITE_RE, PAGE_RE, FOOTNOTE_RE):
        found += [norm_ws(m.group(0)) for m in rx.finditer(text)]
    return Counter(found)


def extract_quotes(text):
    return Counter(norm_ws(m.group(1)).rstrip(".,;:") for m in QUOTE_RE.finditer(text))


def extract_proper(text):
    """句中（非句首）大写词。启发式，仅用于警告。"""
    out = set()
    for m in CAP_RE.finditer(FOOTNOTE_RE.sub(" ", text)):
        start = m.start()
        prev = text[:start].rstrip()
        if not prev or prev[-1] in ".!?:\n" or prev.endswith(("“", "\"")) and len(prev) < 2:
            continue
        out.add(m.group(0))
    return out


def diff_counter(b, a):
    lost = b - a
    new = a - b
    return dict(lost), dict(new)


def closest(term, after):
    words = re.findall(r"[\w'’\-]+", after)
    n = max(1, len(term.split()))
    cands = [" ".join(words[i:i + n]) for i in range(len(words) - n + 1)]
    m = difflib.get_close_matches(term, cands, n=1, cutoff=0.6)
    return m[0] if m else None


def run(before, after, terms):
    errors, warns, info = [], [], []
    res = {}
    for name, fn in (("numbers", extract_numbers), ("citations", extract_citations),
                     ("quotes", extract_quotes)):
        lost, new = diff_counter(fn(before), fn(after))
        res[name] = {"lost_or_reduced": lost, "new_or_increased": new}
        for k, v in lost.items():
            errors.append(f"[{name}] 丢失/减少 ×{v}: {k}")
        for k, v in new.items():
            errors.append(f"[{name}] 新增/增加 ×{v}: {k}")
    pb, pa = extract_proper(before), extract_proper(after)
    missing_p = sorted(w for w in pb if w not in after)
    new_p = sorted(w for w in pa if w not in before)
    res["proper_nouns"] = {"missing": missing_p, "new_capitalized": new_p}
    for w in missing_p:
        warns.append(f"[proper_nouns] 句中大写词在润色后消失: {w}")
    for w in new_p:
        info.append(f"[proper_nouns] 润色后新出现的大写词: {w}")
    term_res = {}
    for t in terms:
        cb, ca = before.count(t), after.count(t)
        term_res[t] = {"before": cb, "after": ca}
        if cb == 0:
            warns.append(f"[terms] 指定术语在润色前文本中不存在: {t}")
        elif ca == 0:
            hint = closest(t, after)
            errors.append(f"[terms] 术语丢失: {t}" + (f"（最接近: {hint}）" if hint else ""))
        elif ca < cb:
            errors.append(f"[terms] 术语出现次数减少 {cb}→{ca}: {t}")
    res["terms"] = term_res
    return res, errors, warns, info


def main():
    ap = argparse.ArgumentParser(description="润色前后保留项一致性检查")
    ap.add_argument("before")
    ap.add_argument("after")
    ap.add_argument("--term", action="append", default=[], help="必须保留的术语，可重复")
    ap.add_argument("--terms-file", help="每行一个术语，# 开头为注释")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    try:
        rd = lambda p: sys.stdin.read() if p == "-" else open(p, encoding="utf-8").read()
        before, after = rd(args.before), rd(args.after)
        terms = list(args.term)
        if args.terms_file:
            terms += [l.strip() for l in open(args.terms_file, encoding="utf-8")
                      if l.strip() and not l.lstrip().startswith("#")]
    except OSError as e:
        print(f"读取失败: {e}", file=sys.stderr)
        return 2
    res, errors, warns, info = run(before, after, terms)
    status = "FAIL" if errors else "PASS"
    if args.json:
        print(json.dumps({"status": status, "errors": errors, "warnings": warns, "info": info,
                          "detail": res}, ensure_ascii=False, indent=2))
    else:
        for e in errors:
            print("ERROR", e)
        for w in warns:
            print("WARN ", w)
        for i in info:
            print("INFO ", i)
        print(f"RESULT: {status} ({len(errors)} errors, {len(warns)} warnings)")
        if not errors:
            print("提示：通过只说明数字/引用/引语/术语形式一致，不代表论断强度未变，仍需人工审阅。")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
