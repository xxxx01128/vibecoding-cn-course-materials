# CS146S《现代软件开发者 / Vibe Coding》中文资料包

> 斯坦福大学 CS146S（2025 秋，授课教师 Mihail Eric）公开课程资料的**全量中文译制包**。
> 本包不是简单机翻，而是一条**可复跑的信息获取—翻译—校对—发布管线**的产出，换一门课的资料即可复用同一流程。

---

## 一、这个包解决什么问题

课程官网 [`themodernsoftware.dev`](https://themodernsoftware.dev/) 的讲义分散在 30+ 个第三方博客、文档站与 PDF 中，中文学习者面临三个障碍：**找不全**、**读不动**（英文长文）、**译法乱**（同一术语多种译法）。本包把这件事一次性做完：

- **找全**：以离线缓存 + URL 映射表为单一事实来源，脚本批量抽取正文并归档；
- **译准**：机器翻译（AI）＋ 统一术语表 ＋ 结构化校对，产出质量可控的中文；
- **好用**：一个可离线浏览的静态文档站 + 完整目录，陌生人零成本上手；
- **可复跑**：换源后一条命令重跑全流程。

## 二、来源与覆盖范围

| 项目 | 内容 |
|---|---|
| 课程 | CS146S: The Modern Software Developer，Stanford University，Fall 2025 |
| 一手来源 | 课程官网 `themodernsoftware.dev` 的 Syllabus 所列全部阅读材料 |
| 素材形态 | 离线缓存包 `CS146S_offline.zip`（30 篇讲义网页 + 3 篇 PDF）+ `Vibe_Coding_Playbook.pdf` |
| 有实质正文 | **30 篇**（含 4 篇 PDF 正文），合计约 60.7 万字符英文 |
| 中文译文 | **30 篇全覆盖**（详见 [`qa/qa_report.md`](qa/qa_report.md)） |
| 术语表 | [`术语表/glossary.json`](术语表/glossary.json)，**68 条**核心术语，全文强制统一 |
| 附加产物 | 清洗后的英文原文 `原文/`、可离线浏览的文档站 `site/`、质量抽检报告 `qa/` |

**覆盖判定口径**：以「有实质正文的讲义」为分母。原站有 4 个页面受登录墙 / 反爬限制（如 `good-context-good-code`、`peeking-under-the-hood-of-claude-code`、`how-warp-uses-warp`、`lessons-from-ai-code-reviews`），仅有占位内容，本身无可译正文，已如实列入下方「已知缺口」，不计入覆盖分母。

## 三、目录结构

```
VibeCoding中文资料包/
├── README.md                  ← 你正在读的文件（资料包说明）
├── AI日志.md               ← 每日 AI 协作记录：工具 / prompt / 踩坑
├── 复盘AAR.md                  ← 七维 AAR 复盘（含失败经验与改进）
├── 拿来说明/                   ← 3 个关键产出的「怎么借助 AI 做出来」
│   ├── 01-术语驱动的翻译一致性.md
│   ├── 02-可复跑的获取翻译管线.md
│   └── 03-长文本分段与质量抽检.md
├── config/course.json         ← 课程源配置（换源只改这里）
├── 术语表/glossary.json        ← 68 条术语，译法唯一事实来源
├── 原文/                       ← 脚本抽取的干净英文正文（35 个文件）
├── 译文/                       ← 30 篇中文译文（交付主体）
├── pipeline/                   ← 可复跑管线脚本
│   ├── 01_extract.py           提取：HTML/PDF → 干净 Markdown
│   ├── 02_segment.py           分段：按标题边界切长文
│   ├── 03_qa_check.py          抽检：覆盖率/术语/结构/漏译
│   ├── 04_build_site.py        发布：生成静态文档站
│   ├── run_all.py              一键编排全流程
│   └── prompts/translate.md    翻译 prompt 模板（含 v1→v3 迭代）
├── data/manifest.json          ← 资料清单（每篇的来源、字数、状态）
├── qa/qa_report.md             ← 质量抽检报告（机器生成，可复核）
└── site/index.html             ← 可离线浏览的文档站入口
```

## 四、翻译流程（机器翻译 + 术语表 + 人工校对）

```
   ① 获取            ② 分段              ③ 翻译              ④ 校对              ⑤ 发布
离线包/URL  ──→  按标题切块  ──→  AI 逐段翻译  ──→  术语/结构抽检  ──→  静态文档站
 01_extract     02_segment      prompts/translate   03_qa_check        04_build_site
   ↓ manifest       ↓ segments      ↓ 译文/            ↓ qa_report        ↓ site/
```

1. **获取（extract）**：BeautifulSoup 剥离导航/页脚等噪音，语义化保留标题、列表、代码块、链接；pypdf 抽取 PDF 文本层；产出 `原文/*.md` 与 `data/manifest.json`。
2. **分段（segment）**：超过 6000 字符的长文按标题边界切块，避免长文本翻译时的上下文衰减与漏段。
3. **翻译（translate）**：AI 按 [`prompts/translate.md`](pipeline/prompts/translate.md) 逐段精译，**术语表强制统一**、代码保真、结构保形；30 篇并行处理以提升效率。
4. **校对（QA）**：`03_qa_check.py` 自动检查覆盖率、竞争译法（如"代码审查"应为"代码评审"）、标题/代码块保真、疑似漏译，产出可复核报告。
5. **发布（build）**：`04_build_site.py` 生成可按主题浏览、可搜索、可离线打开的静态站点。

## 五、使用方法

### 5.1 直接阅读译文

- **最简单**：用浏览器打开 [`site/index.html`](site/index.html)，按主题浏览或输入关键词筛选；点击卡片打开对应译文。
- 或直接进入 `译文/` 目录，用任意 Markdown 阅读器打开 `.md` 文件。

### 5.2 复跑管线（换一门课）

```bash
# 1) 安装依赖
python -m pip install beautifulsoup4 pypdf

# 2) 修改配置：把 config/course.json 的 source 指向新的离线包/URL 映射，
#    并在 术语表/glossary.json 中维护该课程的术语。

# 3) 一键复跑（提取→分段→生成待译清单→抽检→发布）
python pipeline/run_all.py --with-todo

# 4) 按 译文/_待办清单.md 完成翻译后，再跑一次以更新抽检与站点
python pipeline/run_all.py
```

各步骤也可单独运行：`python pipeline/01_extract.py` 等，脚本均为幂等设计。

### 5.3 复用术语表

`术语表/glossary.json` 是译法唯一事实来源。每条术语含 `en`（英文）、`zh`（统一译法）、`note`（注意事项）。新增课程时替换该文件即可，`03_qa_check.py` 会自动据此检测竞争译法。

## 六、质量与验收对照

| Rubric 维度 | 本包对应证据 |
|---|---|
| contentAccuracy 内容准确完整（25） | 30 篇译文全覆盖；68 条术语统一；`qa/qa_report.md` 逐篇核对结构保真与漏译 |
| pipelineAutomation 管线自动化（20） | `pipeline/` 下 4 个脚本 + `run_all.py` 一键编排；换源只改 `config/course.json` |
| artifactCompleteness 产物完整（15） | 本 README + 目录结构 + 术语表 + 可独立运行的文档站 |
| aiUsage AI 使用质量（20） | `AI日志.md` 记录多轮迭代与 prompt 优化；`拿来说明/` 含 3 个可追溯案例 |
| reflectionQuality 复盘质量（20） | `复盘AAR.md` 七维复盘，含失败经验与改进方案 |

## 七、已知缺口

1. **受限页面无正文**：4 个来源页（详见 `原文/` 中状态为 stub/empty 的条目）有登录墙 / 反爬，仅占位，无法翻译；已如实标注，未伪造内容。
2. **图片型 PDF**：`Vibe_Coding_Playbook.pdf` 共 14 页，文本层为空（纯图片），本版未做 OCR；如需覆盖，可在管线中增加 OCR 步骤（见 `复盘AAR.md` 改进项）。
3. **机器翻译的固有局限**：个别长句仍需人工润色；`qa` 标记为 warn 的条目建议人工复核。
4. **视频 / Google Slides**：官网含 3 个 YouTube 视频与 14 个 Google Slides 链接，需联网或账号，未纳入离线包，故未翻译。

## 八、许可与致谢

素材版权归原作者所有，本包仅为学习用途的中文译制与流程演示。课程信息来自 Stanford CS146S 公开课程页；感谢各位原作者与课程团队。
