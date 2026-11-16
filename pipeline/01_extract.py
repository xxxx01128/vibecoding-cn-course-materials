#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
01_extract.py —— 信息获取管线的第一步：从离线 HTML / PDF 中抽取干净正文。

设计目标（对应 Rubric: pipelineAutomation）：
  - 换源可复用：所有输入/输出路径来自 config/course.json，不硬编码。
  - 可复跑：幂等操作，重复执行结果一致。
  - 保留结构：标题层级、代码块、链接、列表都转成 Markdown，便于后续翻译保形。

用法：
  python pipeline/01_extract.py
"""
import os, sys, json, re, html, zipfile

try:
    from bs4 import BeautifulSoup, NavigableString, Tag
    from pypdf import PdfReader
except ImportError as e:
    sys.exit("缺少依赖，请先运行: python -m pip install beautifulsoup4 pypdf\n" + str(e))

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CFG = json.load(open(os.path.join(HERE, "..", "config", "course.json"), encoding="utf-8"))


def abspath(p):
    return os.path.normpath(os.path.join(ROOT, p))


def clean_text(t):
    t = t.replace("\u200b", "").replace("\u200c", "").replace("\ufeff", "")
    t = html.unescape(t)
    t = re.sub(r"[ \t\r\f\v]+", " ", t)
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()


NOISE_SELECTORS = [
    "script", "style", "noscript", "svg", "nav", "footer", "header",
    "aside", "form", "button", "iframe", "[aria-hidden='true']",
    ".cookie", ".cookie-banner", ".subscribe", ".newsletter",
    ".related", ".sidebar", ".menu", ".breadcrumb",
]


def score_container(node):
    """正文得分 = 纯文本长度 - 链接文本的惩罚（导航区链接密集，得分低）。"""
    text = node.get_text(" ", strip=True)
    link_text = " ".join(a.get_text(" ", strip=True) for a in node.find_all("a"))
    return len(text) - 2 * len(link_text)


def pick_main(soup):
    """按优先级找正文容器：语义标签 -> 常见 class -> body；同级取得分最高者。"""
    candidate_selectors = [
        "article", "main", "[role='main']",
        ".post-content", ".entry-content", ".article-content",
        ".markdown-body", ".prose", ".content", "#content",
    ]
    for sel in candidate_selectors:
        nodes = soup.select(sel)
        if nodes:
            best = max(nodes, key=score_container)
            if score_container(best) > 400:
                return best
    return soup.body or soup


def inline_text(node):
    """取一个块级节点的纯文本（去掉内部脚本样式）。"""
    for t in node.find_all(["script", "style", "noscript", "svg"]):
        t.decompose()
    return clean_text(node.get_text(" ", strip=True))


def node_to_md(node, base_url=""):
    """递归把 DOM 子树转成 Markdown，保留标题/段落/列表/代码/链接。"""
    out = []

    def walk(n):
        if isinstance(n, NavigableString):
            s = clean_text(str(n))
            if s:
                out.append(s)
            return
        if not isinstance(n, Tag):
            return
        name = n.name.lower()
        if name in ["script", "style", "noscript", "svg", "button", "iframe"]:
            return
        if re.fullmatch(r"h[1-6]", name):
            lvl = int(name[1])
            txt = inline_text(n)
            if txt:
                out.append("\n\n" + "#" * lvl + " " + txt + "\n\n")
            return
        if name == "pre":
            code = n.get_text()
            code = re.sub(r"\n{3,}", "\n\n", code).strip("\n")
            lang = ""
            cn = n.find("code")
            if cn and cn.get("class"):
                for c in cn["class"]:
                    if c.startswith("language-"):
                        lang = c.replace("language-", "")
                        break
            out.append("\n\n```" + lang + "\n" + code + "\n```\n\n")
            return
        if name == "code":
            out.append("`" + clean_text(n.get_text()) + "`")
            return
        if name == "blockquote":
            txt = inline_text(n)
            if txt:
                out.append("\n\n> " + txt + "\n\n")
            return
        if name == "li":
            txt = inline_text(n)
            if txt:
                out.append("- " + txt + "\n")
            return
        if name in ["ul", "ol"]:
            out.append("\n")
            for c in n.find_all("li", recursive=False):
                walk(c)
            out.append("\n")
            return
        if name == "a":
            txt = clean_text(n.get_text(" ", strip=True))
            href = n.get("href", "")
            if txt and href and not href.startswith("#"):
                if href.startswith("/") and base_url:
                    from urllib.parse import urljoin
                    href = urljoin(base_url, href)
                out.append("[" + txt + "](" + href + ")")
            elif txt:
                out.append(txt)
            return
        if name == "br":
            out.append("\n")
            return
        if name in ["p", "div", "section", "span", "strong", "em", "b", "i",
                    "figure", "figcaption", "table", "tr", "td", "th", "dl", "dt", "dd"]:
            for c in n.children:
                walk(c)
            if name in ["p", "div", "section", "tr", "table"]:
                out.append("\n\n")
            return
        for c in n.children:
            walk(c)

    walk(node)
    md = "".join(out)
    md = re.sub(r"[ \t]+\n", "\n", md)
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip()


def extract_html(path, base_url=""):
    raw = open(path, encoding="utf-8", errors="ignore").read()
    soup = BeautifulSoup(raw, "html.parser")
    for sel in NOISE_SELECTORS:
        for n in soup.select(sel):
            n.decompose()
    main = pick_main(soup)
    md = node_to_md(main, base_url)
    title = ""
    if soup.title and soup.title.string:
        title = clean_text(soup.title.string)
    h1 = soup.find("h1")
    if h1 and not title:
        title = clean_text(h1.get_text(" ", strip=True))
    return {"title": title, "markdown": md}


def extract_pdf(path, max_pages=None):
    reader = PdfReader(path)
    pages = reader.pages if max_pages is None else reader.pages[:max_pages]
    chunks = []
    for i, pg in enumerate(pages):
        try:
            t = pg.extract_text() or ""
        except Exception:
            t = ""
        if t.strip():
            chunks.append("<!-- page %d -->\n%s" % (i + 1, clean_text(t)))
    md = "\n\n".join(chunks)
    md = re.sub(r"\n{3,}", "\n\n", md)
    return {"title": os.path.splitext(os.path.basename(path))[0], "markdown": md,
            "pages": len(reader.pages)}


def ensure_source():
    """确保离线源可用：若 offline_dir 不存在则从 zip 解压。"""
    d = abspath(CFG["source"]["offline_dir"])
    if os.path.isdir(d):
        return d
    zpath = abspath(CFG["source"].get("zip", ""))
    if zpath and os.path.exists(zpath):
        with zipfile.ZipFile(zpath) as z:
            z.extractall(os.path.dirname(d))
        print("[extract] 从 zip 解压到", d)
        return d
    sys.exit("找不到离线源：" + d)


def main():
    src_dir = ensure_source()
    raw_dir = abspath(CFG["target"]["raw"])
    os.makedirs(raw_dir, exist_ok=True)
    page_map_path = os.path.join(src_dir, "page_map.json")
    page_map = json.load(open(page_map_path, encoding="utf-8")) if os.path.exists(page_map_path) else {}

    manifest = {
        "course": CFG["course"],
        "source_dir": CFG["source"]["offline_dir"],
        "items": [],
    }

    pages_dir = os.path.join(src_dir, "pages")
    order = 1
    for fn in sorted(os.listdir(pages_dir)) if os.path.isdir(pages_dir) else []:
        if not fn.lower().endswith(".html"):
            continue
        url = next((u for u, v in page_map.items() if v == fn), "")
        try:
            res = extract_html(os.path.join(pages_dir, fn), url)
        except Exception as e:
            res = {"title": fn, "markdown": "", "error": str(e)}
        md = res.get("markdown", "")
        status = "ok" if len(md) >= 400 else ("stub" if len(md) > 0 else "empty")
        out_name = "%02d_%s.md" % (order, os.path.splitext(fn)[0])
        open(os.path.join(raw_dir, out_name), "w", encoding="utf-8").write(
            "# " + res.get("title", fn) + "\n\n> 来源: " + (url or "本地讲义页") + "\n\n" + md
        )
        manifest["items"].append({
            "id": "P%02d" % order, "kind": "html", "origin": fn, "file": out_name,
            "title": res.get("title", fn), "url": url, "chars": len(md), "status": status,
        })
        order += 1

    # 课程自带 PDF
    pdf_dir = os.path.join(src_dir, "pdfs")
    pdf_files = []
    if os.path.isdir(pdf_dir):
        pdf_files += [os.path.join(pdf_dir, f) for f in sorted(os.listdir(pdf_dir)) if f.lower().endswith(".pdf")]
    for extra in CFG["source"].get("extra_pdfs", []):
        p = abspath(extra)
        if os.path.exists(p):
            pdf_files.append(p)

    for pdf in pdf_files:
        try:
            res = extract_pdf(pdf)
        except Exception as e:
            res = {"title": os.path.basename(pdf), "markdown": "", "error": str(e)}
        md = res.get("markdown", "")
        status = "ok" if len(md) >= 400 else ("stub" if len(md) > 0 else "empty")
        out_name = "%02d_%s.md" % (order, os.path.splitext(os.path.basename(pdf))[0])
        open(os.path.join(raw_dir, out_name), "w", encoding="utf-8").write(
            "# " + res["title"] + "\n\n> 来源: PDF " + os.path.basename(pdf) + "\n\n" + md
        )
        manifest["items"].append({
            "id": "P%02d" % order, "kind": "pdf", "origin": os.path.basename(pdf), "file": out_name,
            "title": res["title"], "url": "", "chars": len(md), "status": status,
            "pages": res.get("pages", 0),
        })
        order += 1

    mpath = abspath(CFG["target"]["manifest"])
    json.dump(manifest, open(mpath, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    ok = [i for i in manifest["items"] if i["status"] == "ok"]
    stub = [i for i in manifest["items"] if i["status"] == "stub"]
    empty = [i for i in manifest["items"] if i["status"] == "empty"]
    print("[extract] 共 %d 项 -> %s" % (len(manifest["items"]), raw_dir))
    print("[extract] 有正文=%d  占位=%d  空=%d" % (len(ok), len(stub), len(empty)))
    print("[extract] 正文总字符=%d" % sum(i["chars"] for i in ok))
    print("[extract] manifest ->", mpath)


if __name__ == "__main__":
    main()
