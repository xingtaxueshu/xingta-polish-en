#!/usr/bin/env python3
"""evals/score.py — 对 evals/runs/<组名>/ 下的润色结果打分（可复现部分）

用法：python3 evals/score.py A B [--json out.json]
目录约定：
  evals/cases/NN.txt|NN.json       原文与元数据（必须保留项/植入问题/语气强度检查）
  evals/runs/<组>/NN.txt           该组的润色后文本
  evals/runs/<组>/NN.report.md     （仅 B 组）含“修改清单”表格，用于一致性检查
自动指标：
  preserve_lost    必须保留项（逐字串）丢失数
  checker_errors   check_invariants.py（无术语）报出的错误数
  fixed / total    植入问题修复数（正则判定“错误写法已不存在”，是粗略代理，需配合人工）
  strength_flags   语气强度正则违规数（hedge 被删 / 被禁止的强化词出现）
  edit_ratio       词级改动比例（越高改得越多）
  log_cov          （B）修改清单覆盖的改动词比例；log_bad = 清单中与原文/译文对不上的条目数
人工指标（新论断/论证强度变化）不在此脚本内，见 results.md。
"""
import glob, json, os, re, sys, difflib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
import check_invariants as ci
import diff_report as dr


def norm(s):
    s = s.replace("“", '"').replace("”", '"').replace("’", "'").replace("‘", "'")
    return re.sub(r"\s+", " ", s)


def parse_log(path):
    rows = []
    if not os.path.exists(path):
        return rows
    for line in open(path, encoding="utf-8"):
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 4 and cells[0].isdigit():
            clean = lambda x: x.strip().strip("`").strip("“”\"'").strip()
            rows.append((cells[0], clean(cells[2]), clean(cells[3])))
    return rows


def toks(s):
    return [re.sub(r"^\W+|\W+$", "", t).lower() for t in s.split() if re.sub(r"^\W+|\W+$", "", t)]


def changed_tokens(before, after):
    tb, ta = toks(before), toks(after)
    sm = difflib.SequenceMatcher(None, tb, ta, autojunk=False)
    dele, ins = [], []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op != "equal":
            dele += tb[i1:i2]; ins += ta[j1:j2]
    return dele, ins, 1 - sm.ratio()


def score(group):
    res = []
    for jf in sorted(glob.glob(os.path.join(HERE, "cases", "*.json"))):
        cid = os.path.basename(jf)[:-5]
        meta = json.load(open(jf, encoding="utf-8"))
        before = open(os.path.join(HERE, "cases", cid + ".txt"), encoding="utf-8").read()
        p = os.path.join(HERE, "runs", group, cid + ".txt")
        if not os.path.exists(p):
            continue
        after = open(p, encoding="utf-8").read()
        nb, na = norm(before), norm(after)
        lost = [x for x in meta["must_preserve"] if norm(x) not in na]
        _, errs, _, _ = ci.run(before, after, [])
        fixed = [i["id"] for i in meta["issues"] if not re.search(i["absent_regex"], after, re.M)]
        unfixed = [i["id"] for i in meta["issues"] if i["id"] not in fixed]
        flags = []
        for h in meta["hedges"]:
            if "keep_regex" in h and not re.search(h["keep_regex"], after, re.I):
                flags.append(h["id"] + ":hedge-lost")
            if "forbid_regex" in h and re.search(h["forbid_regex"], after, re.I):
                flags.append(h["id"] + ":forbidden-strengthener")
        dele, ins, er = changed_tokens(before, after)
        log = parse_log(os.path.join(HERE, "runs", group, cid + ".report.md"))
        logbad, cov = None, None
        if log:
            logbad = [n for n, o, r in log
                      if (o and norm(o).lower() not in nb.lower()) or (r and norm(r).lower() not in na.lower())]
            lo = set(t for _, o, _ in log for t in toks(o)); lr = set(t for _, _, r in log for t in toks(r))
            tot = len(dele) + len(ins)
            ok = sum(1 for t in dele if t in lo) + sum(1 for t in ins if t in lr)
            cov = ok / tot if tot else 1.0
        res.append(dict(case=cid, preserve_lost=lost, checker_errors=errs, fixed=fixed,
                        unfixed=unfixed, n_issues=len(meta["issues"]), strength_flags=flags,
                        edit_ratio=round(er, 3), log_entries=len(log), log_bad=logbad,
                        log_cov=None if cov is None else round(cov, 3)))
    return res


def main():
    groups = [a for a in sys.argv[1:] if not a.startswith("--")]
    out = None
    if "--json" in sys.argv:
        out = sys.argv[sys.argv.index("--json") + 1]
        groups = [g for g in groups if g != out]
    allres = {g: score(g) for g in groups}
    for g, rs in allres.items():
        print(f"\n## 组 {g}\n")
        print("| case | preserve_lost | checker_errors | fixed/total | strength_flags | edit_ratio | log_entries | log_bad | log_cov |")
        print("|---|---|---|---|---|---|---|---|---|")
        for r in rs:
            print(f"| {r['case']} | {len(r['preserve_lost'])} | {len(r['checker_errors'])} | {len(r['fixed'])}/{r['n_issues']} | "
                  f"{len(r['strength_flags'])} | {r['edit_ratio']} | {r['log_entries'] or '-'} | "
                  f"{'-' if r['log_bad'] is None else len(r['log_bad'])} | {'-' if r['log_cov'] is None else r['log_cov']} |")
        T = lambda k: sum(len(r[k]) for r in rs)
        fx, tot = sum(len(r['fixed']) for r in rs), sum(r['n_issues'] for r in rs)
        print(f"| **合计** | **{T('preserve_lost')}** | **{T('checker_errors')}** | **{fx}/{tot} ({fx/tot:.1%})** | **{T('strength_flags')}** | "
              f"{sum(r['edit_ratio'] for r in rs)/len(rs):.3f} (avg) | | | |")
    if out:
        json.dump(allres, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
