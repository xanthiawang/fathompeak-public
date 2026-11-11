"""Build the deployable site/ folder from the single-file prototype.

- wraps the artifact fragment (starts with <title>) in a full HTML skeleton
- self-hosts the Latin fonts (Fraunces, DM Sans, DM Mono) in site/fonts/ so the page
  renders with the right type even where Google Fonts is unreachable
- loads the CJK Google fonts (Noto Serif SC / Noto Sans SC) non-blocking, so a hanging
  request to fonts.googleapis.com never delays the first paint

Usage: python3 build_site_2026-10-13.py [--refetch-fonts]
"""
import sys as _sys
_sys.exit("已停用：2026-10-13 起 GitHub 仓库 site/（xanthiawang/fathompeak-site）是唯一源文件，其他会话已在仓库内直接改文案。"
          "重新生成会覆盖这些修改。要改网站，请在 site/ 里 git pull 后直接编辑 index.html。")
import os, re, sys, urllib.request

ROOT = '/Users/zixin/Desktop/沐仞科技'
SRC = ROOT + '/品牌竞品调研_2026-10-12/demo/沐仞官网原型_2026-10-12.html'
SITE = ROOT + '/site'
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'

frag = open(SRC, encoding='utf-8').read()
head, body = frag.split('</title>', 1)
m = re.search(r'<link rel="stylesheet" href="(https://fonts\.googleapis\.com/css2\?[^"]+)">', body)
assert m, 'font link not found'
families = re.findall(r'family=([^&]+)', m.group(1))
latin = [f for f in families if not f.startswith('Noto')]
cjk = [f for f in families if f.startswith('Noto')]
assert latin and cjk, families

os.makedirs(SITE + '/fonts', exist_ok=True)
fonts_css = SITE + '/fonts/fonts.css'
if not os.path.exists(fonts_css) or '--refetch-fonts' in sys.argv:
    url = 'https://fonts.googleapis.com/css2?' + '&'.join('family=' + f for f in latin) + '&display=swap'
    css = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=60).read().decode()
    out, n = [], 0
    for subset, blk in re.findall(r'/\* ([\w-]+) \*/\s*@font-face \{(.*?)\}', css, re.S):
        if subset not in ('latin', 'latin-ext'):
            continue
        src = re.search(r'url\((https://fonts\.gstatic\.com/[^)]+)\)', blk).group(1)
        fam = re.search(r"font-family: '([^']+)'", blk).group(1)
        style = re.search(r'font-style: (\w+)', blk).group(1)
        fn = re.sub(r'[^a-z0-9]+', '-', f'{fam}-{style}-{subset}'.lower()).strip('-') + '.woff2'
        data = urllib.request.urlopen(urllib.request.Request(src, headers={'User-Agent': UA}), timeout=60).read()
        open(SITE + '/fonts/' + fn, 'wb').write(data); n += 1
        out.append('@font-face {' + blk.replace(src, fn) + '}')
    open(fonts_css, 'w', encoding='utf-8').write('\n'.join(out) + '\n')
    print('fonts fetched', n)

cjk_url = 'https://fonts.googleapis.com/css2?' + '&'.join('family=' + f for f in cjk) + '&display=swap'
link = ('<link rel="stylesheet" href="fonts/fonts.css">'
        '<link rel="preload" as="style" href="' + cjk_url + '" onload="this.onload=null;this.rel=\'stylesheet\'">'
        '<noscript><link rel="stylesheet" href="' + cjk_url + '"></noscript>')
body = body.replace(m.group(0), link, 1)
html = ('<!doctype html>\n<html lang="zh-CN">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        + head + '</title>\n</head>\n<body>\n' + body + '\n</body>\n</html>\n')
open(SITE + '/index.html', 'w', encoding='utf-8').write(html)
print('index.html', len(html), 'latin', latin, 'cjk', cjk)
