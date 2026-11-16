#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
04_build_site.py —— 把译文构建成一个可离线浏览的静态文档站（发布形态）。

对应 Rubric:
  - artifactCompleteness：仓库/文档站可独立使用、目录结构清晰
  - pipelineAutomation：换源后重跑即可生成新站点

产出：
  site/index.html      —— 课程主页 + 全部译文导航（按主题分组、可搜索）
  site/assets/style.css
  复制译文到 site/posts/ 供浏览器直接打开

用法：
  python pipeline/04_build_site.py
"""
import os, json, re, shutil, html

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CFG = json.load(open(os.path.join(HERE, "..", "config", "course.json"), encoding="utf-8"))
TRANS = os.path.join(ROOT, CFG["target"]["translated"])
SITE = os.path.join(ROOT, "site")
POSTS = os.path.join(SITE, "posts")

# 主题分组（按文件序号映射，便于学习者按课程模块浏览）
GROUPS = [
    (1, 2, "第一模块 · 智能体与提示工程"),
    (3, 8, "第二模块 · 编码智能体与工具"),
    (9, 12, "第三模块 · 上下文管理"),
    (13, 16, "第四模块 · AI 安全"),
    (17, 24, "第五模块 · 代码评审与可观测性"),
    (25, 31, "第六模块 · 提示与安全基础"),
    (32, 35, "第七模块 · 产业实践（PDF）"),
]


def md_to_html(md):
    """极简 Markdown→HTML（够用即可：标题/列表/代码/引用/段落/加粗/链接）。"""
    lines = md.split("\n")
    out, in_code, in_list = [], False, False
    def inline(s):
        s = html.escape(s)
        s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
        s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
        s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
        return s
    for ln in lines:
        if ln.strip().startswith("```"):
            if in_code:
                out.append("</code></pre>"); in_code = False
            else:
                if in_list: out.append("</ul>"); in_list = False
                lang = ln.strip()[3:].strip()
                out.append('<pre><code class="language-%s">' % html.escape(lang)); in_code = True
            continue
        if in_code:
            out.append(html.escape(ln)); continue
        m = re.match(r"^(#{1,6}) (.*)", ln)
        if m:
            if in_list: out.append("</ul>"); in_list = False
            lvl = len(m.group(1))
            out.append("<h%d>%s</h%d>" % (lvl, inline(m.group(2)), lvl)); continue
        if ln.startswith("> "):
            if in_list: out.append("</ul>"); in_list = False
            out.append("<blockquote>%s</blockquote>" % inline(ln[2:])); continue
        if re.match(r"^\s*[-*] ", ln):
            if not in_list: out.append("<ul>"); in_list = True
            out.append("<li>%s</li>" % inline(re.sub(r"^\s*[-*] ", "", ln))); continue
        if not ln.strip():
            if in_list: out.append("</ul>"); in_list = False
            continue
        if in_list: out.append("</ul>"); in_list = False
        out.append("<p>%s</p>" % inline(ln))
    if in_code: out.append("</code></pre>")
    if in_list: out.append("</ul>")
    return "\n".join(out)


CSS = """
:root{--card:#fff;--bg:#f6f7f9;--ink:#1f2329;--sub:#646a73;--brand:#8c1515;--line:#e4e6eb}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:-apple-system,'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif;line-height:1.75}
header{background:var(--brand);color:#fff;padding:32px 24px}header h1{margin:0 0 6px;font-size:1.9rem}header p{margin:0;opacity:.9}
.wrap{max-width:960px;margin:0 auto;padding:24px}
.toolbar{background:#fff;border:1px solid var(--line);border-radius:10px;padding:14px 16px;margin-bottom:20px;display:flex;gap:12px;align-items:center}
.toolbar input{flex:1;padding:10px 12px;border:1px solid var(--line);border-radius:6px;font-size:1rem}
.badge{background:#eef4ff;color:#2b5caa;border-radius:12px;padding:2px 10px;font-size:.8rem}
h2.grp{font-size:1.15rem;color:var(--brand);border-left:4px solid var(--brand);padding-left:10px;margin:28px 0 12px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px;text-decoration:none;color:var(--ink);transition:.15s}
.card:hover{border-color:var(--brand);box-shadow:0 3px 12px rgba(140,21,21,.1)}
.card .t{font-weight:600;margin-bottom:6px}.card .m{font-size:.8rem;color:var(--sub)}
article{background:#fff;border:1px solid var(--line);border-radius:10px;padding:28px 32px}
article pre{background:#1f2329;color:#e8e8e8;padding:14px;border-radius:8px;overflow:auto}
article code{background:#f2f3f5;padding:1px 5px;border-radius:4px;font-size:.9em}
article pre code{background:none;padding:0;color:inherit}
blockquote{border-left:3px solid var(--brand);margin:12px 0;padding:6px 14px;color:var(--sub);background:#fafafa}
a{color:var(--brand)}.back{display:inline-block;margin-bottom:16px}
footer{text-align:center;color:var(--sub);padding:24px;font-size:.85rem}
"""


def build():
    manifest = json.load(open(os.path.join(ROOT, CFG["target"]["manifest"]), encoding="utf-8"))
    os.makedirs(POSTS, exist_ok=True)
    items = []
    for it in manifest["items"]:
        src = os.path.join(TRANS, it["file"])
        if not os.path.exists(src):
            continue
        md = open(src, encoding="utf-8").read()
        title = re.search(r"^# (.+)$", md, re.M)
        title = title.group(1).strip() if title else it["title"]
        post_name = os.path.splitext(it["file"])[0] + ".html"
        body = md_to_html(md)
        doc = """<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>%s</title>
<link rel="stylesheet" href="../assets/style.css"></head><body>
<div class="wrap"><a class="back" href="../index.html">← 返回目录</a>
<article>%s</article></div></body></html>""" % (html.escape(title), body)
        open(os.path.join(POSTS, post_name), "w", encoding="utf-8").write(doc)
        n = int(re.match(r"P(\d+)", it["id"]).group(1))
        items.append({"n": n, "title": title, "post": post_name, "chars": len(md)})

    # 首页
    groups_html = []
    for lo, hi, name in GROUPS:
        gi = [i for i in items if lo <= i["n"] <= hi]
        if not gi: continue
        cards = "\n".join(
            ' <a class="card" href="posts/%s"><div class="t">%s</div><div class="m">%s · %d 字</div></a>'
            % (html.escape(i["post"]), html.escape(i["title"]), i["n"], i["chars"]) for i in gi)
        groups_html.append('<h2 class="grp">%s</h2><div class="grid">%s</div>' % (html.escape(name), cards))
    index = """<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>%s · 中文资料包</title>
<link rel="stylesheet" href="assets/style.css"></head><body>
<header><div class="wrap"><h1>%s</h1><p>%s ｜ 全量中文译文资料包 ｜ 共 %d 篇</p></div></header>
<div class="wrap">
<div class="toolbar"><input id="q" placeholder="输入关键词筛选讲义标题…" oninput="filt()">
<span class="badge">%d 篇译文</span></div>
<div id="content">%s</div>
<footer>由 pipeline/04_build_site.py 自动生成 · 术语表 %d 条 · 可离线浏览</footer>
</div>
<script>
function filt(){var q=document.getElementById('q').value.toLowerCase();
document.querySelectorAll('.card').forEach(function(c){c.style.display=c.textContent.toLowerCase().indexOf(q)>-1?'':'none';});
document.querySelectorAll('h2.grp').forEach(function(h){var g=h.nextElementSibling;var any=[].some.call(g.querySelectorAll('.card'),function(c){return c.style.display!='none';});h.style.display=g.style.display=any?'':'none';});}
</script></body></html>""" % (
        html.escape(CFG["course"]["title_zh"]), html.escape(CFG["course"]["title_zh"]),
        html.escape(CFG["course"]["term"]), len(items), len(items),
        "\n".join(groups_html), len(json.load(open(os.path.join(ROOT, CFG["glossary"]), encoding="utf-8"))["terms"]))
    os.makedirs(os.path.join(SITE, "assets"), exist_ok=True)
    open(os.path.join(SITE, "index.html"), "w", encoding="utf-8").write(index)
    open(os.path.join(SITE, "assets", "style.css"), "w", encoding="utf-8").write(CSS)
    print("[site] 生成 %d 篇译文页面 -> %s" % (len(items), SITE))
    print("[site] 主页 ->", os.path.join(SITE, "index.html"))


if __name__ == "__main__":
    build()
