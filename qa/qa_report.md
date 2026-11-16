# 翻译质量抽检报告

> 由 `pipeline/03_qa_check.py` 自动生成；每次翻译迭代后复跑，结果可复核。

## 汇总结论

| 指标 | 数值 | 判定 |
|---|---|---|
| 有实质正文的讲义 | 30 篇 | — |
| 已有中文译文 | 30 篇 | — |
| **覆盖率** | **100.0%** | **通过**（目标 ≥80%） |
| 术语一致性问题 | 0 处 | 通过 |
| 术语表条目 | 68 条 | — |
| 疑似漏译(fail) | 0 篇 | — |
| 警告(warn) | 0 篇 | — |
| 缺失 | 0 篇 | — |

## 逐篇明细

| ID | 文件 | 状态 | 原文字符 | 译文字符 | 比值 | 标题(原/译) | 代码块(原/译) | 问题 |
|---|---|---|---|---|---|---|---|---|
| P01 | 01_agentic-ai-threats.md | ok | 55006 | 29736 | 0.54 | 56/56 | 0/0 | — |
| P02 | 02_ai-code-review-best-practices.md | ok | 13167 | 4896 | 0.37 | 32/32 | 0/0 | — |
| P03 | 03_benefits-agentic-ai-oncall.md | ok | 7499 | 3042 | 0.41 | 7/7 | 0/0 | — |
| P04 | 04_claude-code-best-practices.md | ok | 11197 | 7174 | 0.64 | 8/8 | 9/9 | — |
| P05 | 05_code-review-essentials.md | ok | 12093 | 4491 | 0.37 | 9/9 | 2/2 | — |
| P06 | 06_code-reviews-just-do-it.md | ok | 4026 | 1725 | 0.43 | 1/1 | 0/0 | — |
| P07 | 07_context-rot.md | ok | 50976 | 21581 | 0.42 | 43/43 | 1/1 | — |
| P08 | 08_copilot-prompt-injection-rce.md | ok | 7815 | 3467 | 0.44 | 14/14 | 0/0 | — |
| P09 | 09_devin-coding-agents-101.md | ok | 22062 | 8105 | 0.37 | 61/61 | 0/0 | — |
| P10 | 10_finding-vulnerabilities-claude-codex.md | ok | 23766 | 10811 | 0.45 | 15/15 | 3/3 | — |
| P12 | 12_how-long-contexts-fail.md | ok | 11152 | 4526 | 0.41 | 8/8 | 0/0 | — |
| P13 | 13_how-to-review-code-effectively.md | ok | 22743 | 10165 | 0.45 | 24/24 | 0/0 | — |
| P15 | 15_kubernetes-troubleshooting-ai.md | ok | 10926 | 5449 | 0.5 | 12/12 | 0/0 | — |
| P17 | 17_mcp-food-for-thought.md | ok | 5317 | 2962 | 0.56 | 6/6 | 3/3 | — |
| P18 | 18_mcp-introduction.md | ok | 33872 | 15273 | 0.45 | 36/36 | 5/5 | — |
| P19 | 19_mcp-registry-preview.md | ok | 6670 | 3523 | 0.53 | 6/6 | 0/0 | — |
| P20 | 20_mcp-server-authentication.md | ok | 14268 | 10257 | 0.72 | 15/15 | 8/23 | — |
| P21 | 21_multi-agent-systems-ai-native.md | ok | 10693 | 4177 | 0.39 | 5/5 | 0/0 | — |
| P22 | 22_observability-basics.md | ok | 12227 | 6010 | 0.49 | 27/27 | 2/2 | — |
| P23 | 23_owasp-top-ten.md | ok | 16563 | 11880 | 0.72 | 27/27 | 0/0 | — |
| P25 | 25_prompt-engineering-guide.md | ok | 723 | 390 | 0.54 | 2/2 | 0/0 | — |
| P26 | 26_prompt-engineering-overview.md | ok | 24184 | 8829 | 0.37 | 35/35 | 0/0 | — |
| P27 | 27_sast-vs-dast.md | ok | 23418 | 9912 | 0.42 | 30/30 | 0/0 | — |
| P28 | 28_specs-are-the-new-source-code.md | ok | 12589 | 5284 | 0.42 | 8/8 | 0/0 | — |
| P29 | 29_sre-introduction.md | ok | 27053 | 9661 | 0.36 | 15/15 | 0/0 | — |
| P30 | 30_warp-vs-claude-code.md | ok | 4144 | 1927 | 0.47 | 9/9 | 0/0 | — |
| P31 | 31_writing-effective-tools-for-agents.md | ok | 22770 | 9232 | 0.41 | 14/14 | 1/1 | — |
| P32 | 32_ai-assisted-code-review-assessment.md | ok | 53368 | 21682 | 0.41 | 1/1 | 0/0 | — |
| P33 | 33_how-anthropic-uses-claude-code.md | ok | 75227 | 14167 | 0.19 | 1/54 | 0/0 | — |
| P34 | 34_how-openai-uses-codex.md | ok | 13058 | 5190 | 0.4 | 1/1 | 0/0 | — |

## 判定说明

- 比值 <0.35 视为疑似摘要式漏译；中文通常短于英文，阈值已放宽。
- 术语/结构问题为软性警告，需人工确认是否真为问题（如专有名词）。
- 覆盖率按「有实质正文的讲义」为分母，占位/受限页不计入。
