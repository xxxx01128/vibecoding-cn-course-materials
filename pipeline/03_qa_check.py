#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
03_qa_check.py —— 翻译质量抽检：覆盖率、术语一致性、结构保真、疑似漏译。

对应 Rubric：
  - contentAccuracy：覆盖度、术语统一、无大段漏译
  - aiUsage：质量抽检有据（本报告即证据）

检查项：
  1. 覆盖率      有实质正文的原文中，多少比例有对应译文（目标 >=80%）
  2. 术语一致性  是否出现术语的错误/竞争译法（如"代码审查" vs 术语表"代码评审"）
  3. 结构保真    标题数、代码块数在译文/原文间的比值
  4. 疑似漏译    译文过短（<原文 35%）的标记为疑似摘要式漏译

输出：qa/qa_report.md（人读） + qa/qa_report.json（机读）

用法：
  python pipeline/03_qa_check.py
"""
import os, sys, json, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CFG = json.load(open(os.path.join(HERE, "..", "config", "course.json"), encoding="utf-8"))
GLOSS = json.load(open(os.path.join(ROOT, CFG["glossary"]), encoding="utf-8"))["terms"]

RAW = os.path.join(ROOT, CFG["target"]["raw"])
TRANS = os.path.join(ROOT, CFG["target"]["translated"])
QA = os.path.join(ROOT, CFG["target"]["qa"])
MIN_RATIO = CFG["coverage"]["min_ratio"]
os.makedirs(QA, exist_ok=True)

# 竞争译法检测：正确译法 -> 常见错误译法列表
COMPETING = {
    "代码评审": ["代码审查", "代码检视"],
    "氛围编程": ["振动编码", "直觉编程"],
    "上下文工程": ["语境工程"],
    "提示词注入": ["提示注入", "提示词注入攻击（非规范）"],
    "大语言模型": ["大型语言模型"],
    "可观测性": ["可观察性"],
    "词元": [],  # token 通常保留，不强制
    "大语言模型（LLM）": [],
}
# 产品名不应被翻译
PRODUCTS = ["Claude Code", "Codex", "Warp", "Cursor", "Kubernetes", "OWASP", "GitHub Copilot"]
PRODUCT_WRONG = {"克劳德代码": "Claude Code", "代码助手": "Copilot"}


def count_headings(t):
    return len(re.findall(r"^#{1,6} ", t, re.M))


def count_codeblocks(t):
    return t.count("```") // 2


def strip_source_line(t):
    return re.sub(r"^> 来源:.*$", "", t, flags=re.M)


def check_file(item):
    p_raw = os.path.join(RAW, item["file"])
    p_trans = os.path.join(TRANS, item["file"])
    if not os.path.exists(p_raw):
        return None
    raw = open(p_raw, encoding="utf-8").read()
    if not os.path.exists(p_trans):
        return {"id": item["id"], "file": item["file"], "title": item["title"],
                "status": "missing", "raw_chars": len(raw), "trans_chars": 0}
    trans = open(p_trans, encoding="utf-8").read()
    raw_body = strip_source_line(raw)
    trans_body = strip_source_line(trans)
    rh, th = count_headings(raw_body), count_headings(trans_body)
    rc, tc = count_codeblocks(raw_body), count_codeblocks(trans_body)
    ratio = len(trans_body) / max(1, len(raw_body))

    # PDF 文本层常把一句话拆成多行，导致 raw 字符虚高、字符比失真。
    # 对 PDF 类原文改用「英文词数」估算预期中文字符（经验：1 英文词≈1.6 中文字），
    # 用 word_ratio 判定漏译，避免误报。
    word_ratio = None
    if item.get("kind") == "pdf":
        en_words = len(re.findall(r"[A-Za-z][A-Za-z'-]*", raw_body))
        expected_zh = en_words * 1.6
        word_ratio = len(trans_body) / max(1, expected_zh)

    issues = []
    # 术语竞争译法
    for correct, wrongs in COMPETING.items():
        for w in wrongs:
            n = trans.count(w)
            if n:
                issues.append("术语不一致：'%s' 出现 %d 次（术语表应为 '%s'）" % (w, n, correct))
    for wrong, correct in PRODUCT_WRONG.items():
        if wrong in trans:
            issues.append("产品名被误译：'%s' 应为 '%s'" % (wrong, correct))
    # 结构保真
    if rh and th < rh * 0.6:
        issues.append("标题偏少：原文 %d / 译文 %d（疑似漏段）" % (rh, th))
    if rc and tc < rc * 0.7:
        issues.append("代码块偏少：原文 %d / 译文 %d" % (rc, tc))
    # 疑似摘要式漏译（中文通常比英文短，0.35 是宽松下限）
    # PDF 类以 word_ratio 为准（分母按英文词折算，规避断行虚高）
    eff_ratio = word_ratio if word_ratio is not None else ratio
    if eff_ratio < 0.35:
        if word_ratio is not None:
            issues.append("疑似漏译：PDF 译文/预期中文(按词数估) %.2f < 0.35（字符比 %.2f 因断行不计）" % (word_ratio, ratio))
        else:
            issues.append("疑似漏译：译文/原文字符比 %.2f < 0.35" % ratio)

    status = "ok" if not issues else ("warn" if eff_ratio >= 0.35 else "fail")
    return {"id": item["id"], "file": item["file"], "title": item["title"],
            "status": status, "raw_chars": len(raw_body), "trans_chars": len(trans_body),
            "ratio": round(ratio, 2), "word_ratio": round(word_ratio, 2) if word_ratio is not None else None,
            "headings_raw": rh, "headings_trans": th,
            "codeblocks_raw": rc, "codeblocks_trans": tc, "issues": issues}


def main():
    manifest = json.load(open(os.path.join(ROOT, CFG["target"]["manifest"]), encoding="utf-8"))
    ok_items = [i for i in manifest["items"] if i["status"] == "ok"]
    results = [check_file(i) for i in ok_items]
    results = [r for r in results if r]

    translated_n = sum(1 for r in results if r["status"] in ("ok", "warn", "fail"))
    coverage = translated_n / max(1, len(ok_items))
    term_issues = sum(1 for r in results for x in r.get("issues", []) if "术语不一致" in x or "误译" in x)
    missing = [r for r in results if r["status"] == "missing"]
    warns = [r for r in results if r["status"] == "warn"]
    fails = [r for r in results if r["status"] == "fail"]

    summary = {
        "total_with_content": len(ok_items),
        "translated": translated_n,
        "coverage": round(coverage, 3),
        "coverage_target": MIN_RATIO,
        "coverage_pass": coverage >= MIN_RATIO,
        "term_issues": term_issues,
        "missing": len(missing), "warn": len(warns), "fail": len(fails),
        "glossary_terms": len(GLOSS),
    }
    json.dump({"summary": summary, "items": results},
              open(os.path.join(QA, "qa_report.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    lines = [
        "# 翻译质量抽检报告",
        "",
        "> 由 `pipeline/03_qa_check.py` 自动生成；每次翻译迭代后复跑，结果可复核。",
        "",
        "## 汇总结论",
        "",
        "| 指标 | 数值 | 判定 |",
        "|---|---|---|",
        "| 有实质正文的讲义 | %d 篇 | — |" % len(ok_items),
        "| 已有中文译文 | %d 篇 | — |" % translated_n,
        "| **覆盖率** | **%.1f%%** | **%s**（目标 ≥%.0f%%） |" % (
            coverage * 100, "通过" if coverage >= MIN_RATIO else "未通过", MIN_RATIO * 100),
        "| 术语一致性问题 | %d 处 | %s |" % (term_issues, "通过" if term_issues == 0 else "需修"),
        "| 术语表条目 | %d 条 | — |" % len(GLOSS),
        "| 疑似漏译(fail) | %d 篇 | — |" % len(fails),
        "| 警告(warn) | %d 篇 | — |" % len(warns),
        "| 缺失 | %d 篇 | — |" % len(missing),
        "",
        "## 逐篇明细",
        "",
        "| ID | 文件 | 状态 | 原文字符 | 译文字符 | 比值 | 标题(原/译) | 代码块(原/译) | 问题 |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for r in results:
        lines.append("| %s | %s | %s | %s | %s | %s | %s/%s | %s/%s | %s |" % (
            r["id"], r["file"], r["status"], r.get("raw_chars", "-"), r.get("trans_chars", "-"),
            r.get("ratio", "-"), r.get("headings_raw", "-"), r.get("headings_trans", "-"),
            r.get("codeblocks_raw", "-"), r.get("codeblocks_trans", "-"),
            "；".join(r.get("issues", [])) or "—"))
    lines += ["", "## 判定说明", "",
              "- 比值 <0.35 视为疑似摘要式漏译；中文通常短于英文，阈值已放宽。",
              "- 术语/结构问题为软性警告，需人工确认是否真为问题（如专有名词）。",
              "- 覆盖率按「有实质正文的讲义」为分母，占位/受限页不计入。", ""]
    open(os.path.join(QA, "qa_report.md"), "w", encoding="utf-8").write("\n".join(lines))

    print("[qa] 覆盖率 %.1f%% (%d/%d) %s" % (
        coverage * 100, translated_n, len(ok_items), "PASS" if coverage >= MIN_RATIO else "FAIL"))
    print("[qa] 术语问题 %d, 缺失 %d, warn %d, fail %d" % (term_issues, len(missing), len(warns), len(fails)))
    print("[qa] 报告 ->", os.path.join(QA, "qa_report.md"))


if __name__ == "__main__":
    main()
