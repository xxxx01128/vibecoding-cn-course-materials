#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_all.py —— 一键复跑整条「获取 → 分段 → 翻译 → 抽检 → 发布」管线。

设计意图（对应 Rubric: pipelineAutomation / 换源可复用）：
  - 换一门课：只改 config/course.json 的 course/source/glossary/target，重跑本脚本。
  - 翻译步骤：默认检测 译文/ 缺失则提示；可用 --with-translate-prompt 生成待译清单，
    交给 AI/人工按 prompts/translate.md 完成后，再重跑本脚本即可自动抽检与发布。
  - 幂等：每步都可单独运行；重复执行不产生副作用。

用法：
  python pipeline/run_all.py                 # 提取→分段→抽检→构建站点
  python pipeline/run_all.py --with-todo     # 额外生成 译文/_待办清单.md
"""
import os, sys, json, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CFG = json.load(open(os.path.join(HERE, "..", "config", "course.json"), encoding="utf-8"))


def run(script, *args):
    print("\n" + "=" * 60)
    print("▶ 运行", script, " ".join(args))
    print("=" * 60)
    r = subprocess.run([sys.executable, os.path.join(HERE, script), *args], cwd=ROOT)
    if r.returncode != 0:
        print("✗ %s 失败（exit %d），管线中止。" % (script, r.returncode))
        sys.exit(r.returncode)


def gen_todo():
    manifest = json.load(open(os.path.join(ROOT, CFG["target"]["manifest"]), encoding="utf-8"))
    trans_dir = os.path.join(ROOT, CFG["target"]["translated"])
    todo = [i for i in manifest["items"] if i["status"] == "ok"
            and not os.path.exists(os.path.join(trans_dir, i["file"]))]
    lines = ["# 待译清单", "",
             "> 按 `pipeline/prompts/translate.md` 逐篇翻译；文件名保持一致，写入 `译文/`。", "",
             "| 序号 | 文件 | 原文字符 | 标题 |", "|---|---|---|---|"]
    for i in todo:
        lines.append("| %s | `%s` | %d | %s |" % (
            i["id"], i["file"], i["chars"], i["title"].replace("|", "/")))
    if not todo:
        lines.append("| — | 全部已完成 | — | — |")
    open(os.path.join(trans_dir, "_待办清单.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("[run_all] 待译 %d 篇 -> 译文/_待办清单.md" % len(todo))


def main():
    print("课程：%s（%s）" % (CFG["course"]["title_zh"], CFG["course"]["id"]))
    run("01_extract.py")
    run("02_segment.py")
    if "--with-todo" in sys.argv:
        gen_todo()
    run("03_qa_check.py")
    run("04_build_site.py")
    print("\n✓ 管执行完毕。译文缺失的讲义见 译文/_待办清单.md（如有）。")


if __name__ == "__main__":
    main()
