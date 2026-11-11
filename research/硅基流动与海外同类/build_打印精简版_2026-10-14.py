#!/usr/bin/env python3
"""从 Quarto 导出的 HTML 生成打印精简版 PDF：去掉来源标记、来源列、第 7/8 节和前言说明，紧凑排版。
运行：python3 build_打印精简版_2026-10-14.py   （需本机 Google Chrome）"""
import re, os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "硅基流动与海外同类_业务市场营销调研_2026-10-14.html")
OUT_HTML = os.path.join(HERE, "硅基流动与海外同类_打印精简版_2026-10-14.html")
OUT_PDF = os.path.join(HERE, "硅基流动与海外同类_打印精简版_2026-10-14.pdf")
s = open(SRC, encoding="utf-8").read()

def drop_section(s, sid):
    i = s.find(f'<section id="{sid}"')
    if i < 0: return s
    j = s.find("<section id=", i + 10)
    k = s.find("</main>", i)
    end = j if 0 < j < k else k
    return s[:i] + s[end:]

# 1. 删第 7、8 节
for sid in ["证据边界与待核实", "原始材料"]:
    s = drop_section(s, sid)
# 2. 删目录侧栏、标题元信息、前言说明（证据标记、金额口径、选题理由）
s = re.sub(r'<nav id="TOC".*?</nav>', "", s, flags=re.S)
s = re.sub(r'<header id="title-block-header".*?</header>', lambda m: re.sub(r'<div class="quarto-title-meta">.*', "</header>", m.group(0), flags=re.S), s, flags=re.S)
s = re.sub(r'<p>核查日期：.*?</p>', "", s, count=1, flags=re.S)
s = re.sub(r'<p>证据标记：</p>\s*<ul>.*?</ul>', "", s, count=1, flags=re.S)
s = re.sub(r'<p>金额一律照原币种列出.*?</p>', "", s, count=1, flags=re.S)
s = re.sub(r'<p>为什么选这三家：.*?</p>', "", s, count=1, flags=re.S)
s = re.sub(r'<p>来源：.*?</p>', "", s, flags=re.S)   # 段落式来源说明
# 3. 表格：删「来源」「性质」列
def fix_table(m):
    t = m.group(0)
    rows = list(re.finditer(r'<tr[^>]*>.*?</tr>', t, flags=re.S))
    if not rows: return t
    head_cells = re.findall(r'<t[hd][^>]*>.*?</t[hd]>', rows[0].group(0), flags=re.S)
    drop = [i for i, c in enumerate(head_cells) if re.sub("<[^>]+>", "", c).strip() in ("来源", "性质")]
    if not drop: return t
    def fix_row(rm):
        r = rm.group(0)
        cells = list(re.finditer(r'<t[hd][^>]*>.*?</t[hd]>', r, flags=re.S))
        for i in sorted(drop, reverse=True):
            if i < len(cells): r = r[:cells[i].start()] + r[cells[i].end():]
        return r
    t = re.sub(r'<tr[^>]*>.*?</tr>', fix_row, t, flags=re.S)
    t = re.sub(r'<colgroup>.*?</colgroup>', "", t, flags=re.S)
    return t
s = re.sub(r'<table.*?</table>', fix_table, s, flags=re.S)
# 4. 去掉正文里的【来源标记】（不碰 script/style/base64）
def strip_tags_in_text(m):
    seg = m.group(0)
    seg = re.sub(r'【(招股书|官|投|媒|三方|传|算|判断)[^】]{0,12}】', "", seg)
    seg = re.sub(r'(【判断】)', "", seg)
    return seg
parts = re.split(r'(<script.*?</script>|<style.*?</style>|<img[^>]*>)', s, flags=re.S)
s = "".join(p if p.startswith(("<script", "<style", "<img")) else strip_tags_in_text(re.match(r'.*', p, re.S)) for p in parts)
s = s.replace("、、", "、").replace("；；", "；").replace("（）", "").replace("（ ）", "")
s = re.sub(r'\s*、\s*</', "</", s)
# 5. 紧凑打印样式
CSS = """<style id="compact-print">
@page{size:A4;margin:11mm 12mm}
body,.quarto-container,#quarto-content,main{font-size:9pt!important;line-height:1.32!important;color:#000!important;background:#fff!important}
#quarto-margin-sidebar,#quarto-sidebar,.quarto-title-meta,.quarto-title-banner,#quarto-back-to-top,.nav-page,footer,.quarto-title-block .quarto-title-meta{display:none!important}
main.content,#quarto-document-content,.column-page,.column-body{max-width:100%!important;width:100%!important;margin:0!important;padding:0!important}
.quarto-title h1.title{font-size:15pt!important;margin:0 0 2pt!important;line-height:1.2!important} .quarto-title .subtitle{font-size:9.5pt!important;color:#444!important;margin:0 0 6pt!important}
h2{font-size:11.5pt!important;margin:9pt 0 3pt!important;padding:0!important;border:0!important;break-after:avoid} h3{font-size:10pt!important;margin:7pt 0 2pt!important;break-after:avoid} h4{font-size:9.5pt!important;margin:5pt 0 2pt!important}
p{margin:0 0 3pt!important} ul,ol{margin:0 0 3pt 14pt!important;padding:0!important} li{margin:0!important} li>p{margin:0!important}
table{font-size:7.8pt!important;line-height:1.25!important;margin:2pt 0 6pt!important;width:100%!important;border-collapse:collapse!important}
th,td{padding:1.5pt 3.5pt!important;vertical-align:top!important;border-top:0!important;border-bottom:1px solid #bbb!important} thead th{border-bottom:1.2px solid #000!important;font-weight:700!important} tr{break-inside:avoid}
a{color:#000!important;text-decoration:none!important}
figure,.figure,.quarto-figure{margin:2pt 0 4pt!important;break-inside:avoid} figure img,.figure img{max-width:100%!important;max-height:88mm!important;width:auto!important;display:block;margin:0 auto}
figcaption,.figure-caption{font-size:7.5pt!important;color:#444!important;margin:1pt 0 0!important;text-align:left!important}
strong{font-weight:700} code{font-size:7.8pt!important}
</style>"""
s = s.replace("</head>", CSS + "\n</head>", 1)
open(OUT_HTML, "w", encoding="utf-8").write(s)
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={OUT_PDF}", "file://" + OUT_HTML], capture_output=True, timeout=180)
import fitz
d = fitz.open(OUT_PDF); txt = "".join(p.get_text() for p in d)
print("pages", d.page_count, "| 残留来源标记", len(re.findall(r'【[^】]{1,12}】', txt)), "| 来源列", txt.count("来源"), "| 原始材料", txt.count("原始材料"))
