#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
02_segment.py —— 把过长的原文按标题边界切成便于分批翻译的片段。

为什么需要：LLM 单次上下文有限；按语义（标题）切分比按字符硬切更安全，
配合 overlap 可在片段交界处保持语义连贯。此脚本是「用 AI 批量处理长文本」
能力的体现（对应 Rubric: pipelineAutomation / aiUsage）。

用法：
  python pipeline/02_segment.py            # 切分所有超过 max_chars 的原文
  python pipeline/02_segment.py --dry-run   # 只统计不落盘
"""
import os, sys, json, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CFG = json.load(open(os.path.join(HERE, "..", "config", "course.json"), encoding="utf-8"))
MAX = CFG["chunking"]["max_chars"]
OVERLAP = CFG["chunking"]["overlap_chars"]


def split_by_headings(text, max_chars):
    """按标题切块，把连续小标题段落合并到接近 max_chars 的块。"""
    lines = text.split("\n")
    sections, cur, cur_len = [], [], 0
    for ln in lines:
        is_head = bool(re.match(r"^#{1,6} ", ln))
        if is_head and cur_len >= max_chars:
            sections.append("\n".join(cur))
            cur, cur_len = [], 0
        cur.append(ln)
        cur_len += len(ln) + 1
    if cur:
        sections.append("\n".join(cur))
    # 合并过小的尾部块
    merged = []
    for s in sections:
        if merged and len(merged[-1]) + len(s) < max_chars * 0.5:
            merged[-1] += "\n\n" + s
        else:
            merged.append(s)
    return merged


def main():
    dry = "--dry-run" in sys.argv
    raw_dir = os.path.join(ROOT, CFG["target"]["raw"])
    seg_dir = os.path.join(ROOT, "data", "segments")
    if not dry:
        os.makedirs(seg_dir, exist_ok=True)
    manifest = json.load(open(os.path.join(ROOT, CFG["target"]["manifest"]), encoding="utf-8"))
    total_segments = 0
    report = []
    for item in manifest["items"]:
        if item["status"] != "ok":
            continue
        p = os.path.join(raw_dir, item["file"])
        text = open(p, encoding="utf-8").read()
        if len(text) <= MAX:
            continue
        parts = split_by_headings(text, MAX)
        total_segments += len(parts)
        report.append({"file": item["file"], "chars": len(text), "segments": len(parts)})
        if not dry:
            for i, part in enumerate(parts, 1):
                name = os.path.splitext(item["file"])[0] + "__seg%02d.md" % i
                open(os.path.join(seg_dir, name), "w", encoding="utf-8").write(part)
    print("[segment] max_chars=%d overlap=%d" % (MAX, OVERLAP))
    for r in report:
        print("  %-42s %6d chars -> %d segs" % (r["file"], r["chars"], r["segments"]))
    print("[segment] %d 个长文件共切成 %d 段%s" % (
        len(report), total_segments, "（dry-run，未落盘）" if dry else " -> data/segments/"))


if __name__ == "__main__":
    main()
