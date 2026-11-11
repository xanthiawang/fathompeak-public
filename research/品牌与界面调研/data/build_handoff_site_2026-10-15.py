"""把开发交接说明做成能在微信里打开的独立网页（Zixin 2026-10-15："开发交接说明也要微信能发给别人能打开的"、"推到 github 新的域名"）。
claude.ai 在国内微信里打不开，所以另建 GitHub Pages 站点 xanthiawang/fathompeak-handoff，和官网仓库分开。
和 claude.ai 上那份的区别：
 · 去掉 Google Fonts（国内会卡住页面加载），用系统字体；
 · mermaid 流程图预先渲染成静态 SVG（浅色、深色各一张，按系统配色切换），页面不再依赖任何外部脚本；
 · 补全 doctype / charset / viewport，加 noindex，不让搜索引擎收录。
用法：python3 -I build_handoff_site_2026-10-15.py <交接说明.html> <light.svg> <dark.svg> <输出 index.html>
（SVG 由 mermaid 11.4.1 在无头 Chrome 里渲染：flowchart htmlLabels=false，配色同 claude.ai 页面上的 mermaid 运行时。）
"""
import re, sys

SRC, LIGHT, DARK, OUT = sys.argv[1:5]
s = open(SRC, encoding='utf8').read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: sys.exit(f'[停止] 匹配 {c} 次（应为 {n}）：{old[:80]}')
    s = s.replace(old, new)


rep('<link rel="preconnect" href="https://fonts.googleapis.com">\n', '')
s, n = re.subn(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com/[^"]*">\n', '', s)
if n != 1: sys.exit('[停止] 没找到 Google Fonts')
CSS = '''
/* 微信版：流程图是静态 SVG，按系统配色显示浅色或深色那张 */
.flow{overflow-x:auto;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px;margin:10px 0}
.flow svg{display:block;margin:0 auto;max-width:100%;height:auto}
.fl-d{display:none}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]) .fl-l{display:none}:root:not([data-theme="light"]) .fl-d{display:block}}
:root[data-theme="dark"] .fl-l{display:none} :root[data-theme="dark"] .fl-d{display:block}
@media (max-width:820px){.flow svg{max-width:none;width:860px}}
</style>'''
rep('</style>', CSS)
# 样式先加（SVG 里也有 </style>），再放流程图
m = re.search(r'<pre class="mermaid">\n.*?</pre>', s, re.S)
if not m: sys.exit('[停止] 没找到流程图')
light, dark = open(LIGHT, encoding='utf8').read(), open(DARK, encoding='utf8').read()
s = s[:m.start()] + '<figure class="flow" aria-label="登录派发流程图"><div class="fl-l">' + light + '</div><div class="fl-d">' + dark + '</div></figure>' + s[m.end():]
title = re.search(r'<title>(.*?)</title>\n', s)
s = s.replace(title.group(0), '')
s = ('<!doctype html>\n<html lang="zh-CN">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
     '<meta name="robots" content="noindex,nofollow">\n<title>' + title.group(1) + '</title>\n'
     + s.replace('<div class="wrap">', '</head>\n<body>\n<div class="wrap">', 1).rstrip() + '\n</body>\n</html>\n')
if 'fonts.googleapis' in s or '<script' in s: sys.exit('[停止] 还有外部字体或脚本')
open(OUT, 'w', encoding='utf8').write(s)
print('done:', OUT, len(s))
