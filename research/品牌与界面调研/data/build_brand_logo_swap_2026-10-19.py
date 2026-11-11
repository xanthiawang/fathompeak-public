"""把站点里所有旧双峰山形标（path「M3 20 10 6l4 7 3-4 4 11z」）换成新峰面图形（Zixin 2026-10-19）。
第二版：只换图形，版式和占位大小不变；新图形高度与旧图形接近（约 12px）。
第三版：用作 logo 的英文「FathomPeak」换成新标的 FATHOMPEAK 转曲字标（字高与原文字接近），中文不动。
第四版：英文模式（html lang=en）会把「沐仞」翻成「FathomPeak」，与字标重复——「沐仞」包进 .fp-cn，英文模式隐藏；
手机页头英文模式也改显示字标，不再出现普通字体的 FathomPeak。
登录插画（用户登录、运营后台登录）按 Zixin 10-19 要求保持原图，不改。
先跑 build_brand_logo_assets_2026-10-19.py 生成 art/brand/ 与图标、分享图，再跑本脚本。原地修改站点仓库（有 Git 可回退）。
 · 官网页头、关于页标题上方、所有后台侧栏（.bt-logo，个人 / 企业 / 超管 / 财务共用）、首页演示回答头像：山形 → 新图形
 · 网站图标、分享图：换新文件（带版本号防缓存）
 · 小程序预览：只更新图标链接版本号（页面里原本没有山形图形）
 · 设计规范页 design/palette-type.html：未使用的山形遮罩样式 → 新图形
用法：python3 -I build_brand_logo_swap_2026-10-19.py <站点仓库根目录>
"""
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]); V = '20261019'
MARK, WORD = 'art/brand/fathompeak-mark_2026-10-19.svg', 'art/brand/fathompeak-wordmark_2026-10-19.svg'
for f in [MARK, WORD, 'art/share/og-1200x630_2026-10-19.png']:
    if not (ROOT / f).exists(): sys.exit(f'[停止] 缺少素材 {f}，先跑 build_brand_logo_assets_2026-10-19.py')


def edit(rel, pairs):
    p = ROOT / rel; s = p.read_text(encoding='utf8')
    for old, new, n in pairs:
        c = s.count(old)
        if c != n: sys.exit(f'[停止] {rel} 匹配 {c} 次（应为 {n}）：{old[:90]}')
        s = s.replace(old, new)
    p.write_text(s, encoding='utf8'); print('edited', rel)


OLD_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 20 10 6l4 7 3-4 4 11z" fill="currentColor"/></svg>'
edit('index.html', [
    # 页头：只换图形，「沐仞」文字保留
    ('<a class="logo" href="#home" aria-label="沐仞 首页">' + OLD_SVG + '<span class="wm">沐仞</span></a>',
     f'<a class="logo" href="#home" aria-label="沐仞 首页"><img class="logo-mark" src="{MARK}" width="34" height="12" alt=""><span class="wm">沐仞</span><img class="wm-en" src="{WORD}" width="138" height="10" alt="FathomPeak"></a>', 1),
    # 首页演示头像
    ('<span class="av" aria-hidden="true"><svg viewBox="0 0 24 24" width="14" height="14"><path d="M3 20 10 6l4 7 3-4 4 11z" fill="#fff"/></svg></span>',
     f'<span class="av" aria-hidden="true"><img src="{MARK}" width="18" height="6" alt=""></span>', 1),
    # 关于页：只换图形，「沐仞 FathomPeak」文字保留
    ('<span class="ab-mk"><svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true"><path d="M3 20 10 6l4 7 3-4 4 11z" fill="currentColor"/></svg>沐仞 FathomPeak</span>',
     f'<span class="ab-mk"><img class="ab-mark" src="{MARK}" width="37" height="13" alt=""><span class="ab-wmt"><span class="fp-cn">沐仞</span><img class="ab-wm" src="{WORD}" width="138" height="10" alt="FathomPeak"></span></span>', 1),
    # 后台侧栏
    ('<a class="bt-logo" href="#home" aria-label="返回沐仞官网">' + OLD_SVG + '</a>',
     f'<a class="bt-logo" href="#home" aria-label="返回沐仞官网"><img src="{MARK}" width="30" height="11" alt=""></a>', 1),
    # 图标与分享图
    ('<link rel="icon" href="art/share/favicon.svg" type="image/svg+xml">', f'<link rel="icon" href="art/share/favicon.svg?v={V}" type="image/svg+xml">', 1),
    ('<link rel="icon" href="art/share/icon-192.png" sizes="192x192" type="image/png">', f'<link rel="icon" href="art/share/icon-192.png?v={V}" sizes="192x192" type="image/png">', 1),
    ('<link rel="apple-touch-icon" href="art/share/apple-touch-icon.png">', f'<link rel="apple-touch-icon" href="art/share/apple-touch-icon.png?v={V}">', 1),
    ('https://xanthiawang.github.io/fathompeak-site/art/share/og-1200x630.png', 'https://xanthiawang.github.io/fathompeak-site/art/share/og-1200x630_2026-10-19.png', 2),
    ('<img src="art/share/icon-512.png" alt="" width="512" height="512">', f'<img src="art/share/icon-512.png?v={V}" alt="" width="512" height="512">', 1),
    # 样式：占位框大小沿用旧值，只定图形宽度
    ('</head>', '<style id="brand-logo-20261019">\n'
     '/* 新峰面图形（2026-10-19）替换旧双峰山形标：占位框不变，图形高度与旧标接近。站点主样式写在 body 里、晚于本段，选择器加前缀提高优先级 */\n'
     '.hdr .pill .logo .logo-mark{width:34px;height:auto;display:block;flex:none}\n'
     '#home2 .sw-ans .av{background:#fff;box-shadow:inset 0 0 0 1px rgba(0,0,0,.1)}\n'
     '#home2 .sw-ans .av img{width:18px;height:auto;display:block}\n'
     '.ab-head .ab-mk .ab-mark{width:37px;height:auto;display:block;flex:none}\n'
     '.ab-head .ab-mk .ab-wmt{display:inline-flex;align-items:center;gap:6px}\n'
     '.ab-head .ab-mk .ab-wm{height:10px;width:auto;display:block}\n'
     '.bt .bt-logo img{width:30px;height:auto;display:block}\n'
     '/* 英文模式：「沐仞」会被翻成 FathomPeak，与字标重复，隐藏；手机页头改显示字标 */\n'
     'html[lang="en"] .fp-cn{display:none}\n'
     '.hdr .pill .logo .wm-en{display:none;height:10px;width:auto;margin-left:8px}\n'
     '@media (max-width:800px){html[lang="en"] .hdr .pill .logo .wm{display:none}html[lang="en"] .hdr .pill .logo .wm-en{display:block}}\n'
     '</style>\n</head>', 1),
])

edit('mini-preview/index.html', [
    ('<link rel="icon" href="../art/share/favicon.svg">', f'<link rel="icon" href="../art/share/favicon.svg?v={V}">', 1),
    # 英文换字标，中文不动
    ('<button class="mini-brand" data-nav="home" aria-label="返回首页">沐仞<span>FathomPeak</span></button>',
     f'<button class="mini-brand" data-nav="home" aria-label="返回首页">沐仞<span><img src="../{WORD}" width="111" height="8" alt="FathomPeak"></span></button>', 1),
    ('<a class="wordmark" href="../" aria-label="沐仞官网">FathomPeak<span>沐仞科技</span></a>',
     f'<a class="wordmark" href="../" aria-label="沐仞官网"><img src="../{WORD}" width="208" height="15" alt="FathomPeak"><span>沐仞科技</span></a>', 1),
])
s = (ROOT / 'mini-preview/styles.css').read_text(encoding='utf8')
(ROOT / 'mini-preview/styles.css').write_text(s.rstrip('\n') + '\n/* 新 logo（2026-10-19）：英文换成 FATHOMPEAK 转曲字标，字高与原文字接近 */\n.mini-brand span img{height:8px;width:auto;display:block}\n.wordmark img{height:15px;width:auto;display:block}\n', encoding='utf8')
print('edited mini-preview/styles.css')

p = ROOT / 'design/palette-type.html'; s = p.read_text(encoding='utf8')
a = s.find('.pill i{'); b = s.find('}', a)
if a < 0 or 'M3 20 10 6' not in s[a:b]: sys.exit('[停止] 设计规范页的 .pill i 规则变了')
s = s[:a] + f'.pill i{{width:56px;height:40px;border-radius:12px;display:inline-block;background:url("../{MARK}") center/46px auto no-repeat}}' + s[b + 1:]
if 'M3 20 10 6' in s: sys.exit('[停止] 设计规范页里还有旧山形标')
p.write_text(s, encoding='utf8'); print('edited design/palette-type.html')

for rel in ['index.html', 'mini-preview/index.html', 'design/palette-type.html', 'art/share/favicon.svg']:
    if 'M3 20 10 6' in (ROOT / rel).read_text(encoding='utf8'): sys.exit(f'[停止] {rel} 还有旧山形标')
print('done: no old mountain mark left')
