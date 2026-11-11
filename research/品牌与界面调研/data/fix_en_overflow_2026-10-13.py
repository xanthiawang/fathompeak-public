"""英文模式溢出修正：首屏产品窗侧栏的"时段"胶囊英文太长、不换行，压到右侧主栏。
英文改短 + 侧栏里的胶囊允许换行。首屏 HTML 不改（只改 CSS 与词典）。
用法：python3 -I fix_en_overflow_2026-10-13.py <仓库副本目录>
"""
import os, sys

P = os.path.join(sys.argv[1], 'index.html')
s = open(P, encoding='utf8').read()
hero0 = s[s.index('<div class="hero">'):s.index('<div class="partners">')]

def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: sys.exit(f'[停止] 匹配 {c} 次（应为 {n}）：{old[:80]}')
    s = s.replace(old, new)

rep('"时段以订单为准": "Confirm timing in the order"', '"时段以订单为准": "Set per order"')
k = s.index('</style>')
s = s[:k] + '\n/* 首屏产品窗侧栏很窄：胶囊允许换行，不压到主栏 */\n.hero .product .side .pk{white-space:normal;max-width:100%;line-height:1.35}\n/* 英文比中文长：模型卡价格行允许换行；页脚版权行手机端可换行 */\n.hero .product .mc .pr{flex-wrap:wrap;row-gap:4px}\n@media (max-width:800px){footer .bottom span{white-space:normal}}\n/* 英文版首屏：大字标 FathomPeak 比"沐仞"宽得多，缩小；说明文字放宽到三行，不压到产品窗 */\n:root[lang="en"]:not([data-scheme="C"]) .hero .word{font-size:clamp(100px,14vw,210px)}\n@media (min-width:801px){:root[lang="en"]:not([data-scheme="C"]) .hero .h-sub{max-width:min(92ch,100%)} :root[lang="en"]:not([data-scheme="C"]) .hero .h{font-size:clamp(26px,3.4vw,38px);white-space:nowrap}}\n' + s[k:]

assert s[s.index('<div class="hero">'):s.index('<div class="partners">')] == hero0, '首屏 HTML 被改动'
open(P, 'w', encoding='utf8').write(s)
print('done.')
