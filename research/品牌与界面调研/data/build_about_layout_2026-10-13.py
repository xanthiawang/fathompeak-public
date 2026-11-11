"""关于页排版修正（在 33f7344 之上）：新闻动态移到页头下方；机构支持 5 卡一行；联系 2 卡两栏；
招聘块收紧上下留白；页脚删"关注"列后改四栏网格。只改本地副本 index.html，首屏与首页结尾 CTA 逐字不变。
用法：python3 -I build_about_layout_2026-10-13.py <仓库副本目录>
"""
import os, sys

P = os.path.join(sys.argv[1], 'index.html')
s = open(P, encoding='utf8').read()
hero0 = s[s.index('<div class="hero">'):s.index('<div class="partners">')]
end0 = s[s.index('<div class="cta-end rv">'):s.index('</section>', s.index('<div class="cta-end rv">'))]

def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: sys.exit(f'[停止] 匹配 {c} 次（应为 {n}）：{old[:60]}')
    s = s.replace(old, new)

# 1. 新闻动态移到页头正下方
a = s.index('<section data-route="about">'); b = s.index('</section>', a)
i = s.index('    <div class="sec rv" style="margin-top:36px"><div class="hd"><h2 class="h2" style="margin:0">新闻动态</h2>', a)
j = s.index('\n', i) + 1
assert a < i < b
news = s[i:j]
s = s[:i] + s[j:]
head_end = '服务全球计算需求。</p></div>\n'
k = s.index(head_end, a) + len(head_end)
s = s[:k] + '\n' + news.replace('style="margin-top:36px"', 'style="margin-top:8px"') + s[k:]

# 2. 机构支持 5 卡同排；联系 2 卡两栏
rep('<h2 class="h2">机构支持</h2>\n    <div class="cards3 rv">', '<h2 class="h2">机构支持</h2>\n    <div class="cards3 rv c5">')
rep('<div class="cards3 rv contact">', '<div class="cards3 rv contact c2">')

# 3. 招聘块留白；网格样式
rep('.careers{margin-top:56px}',
    '.careers{margin-top:8px;padding-top:56px;padding-bottom:40px}\n'
    '.cards3.c5{grid-template-columns:repeat(5,1fr)}\n'
    '.cards3.c2{grid-template-columns:repeat(2,1fr)}\n'
    '@media (max-width:1100px){.cards3.c5{grid-template-columns:repeat(3,1fr)}}\n'
    '@media (max-width:800px){.cards3.c5,.cards3.c2{grid-template-columns:1fr}}')

# 4. 页脚：删"关注"后剩 联系 + 三列
rep('footer .cols{display:grid;grid-template-columns:minmax(220px,1.5fr) repeat(4,minmax(120px,1fr));',
    'footer .cols{display:grid;grid-template-columns:minmax(220px,1.5fr) repeat(3,minmax(120px,1fr));')

assert s[s.index('<div class="hero">'):s.index('<div class="partners">')] == hero0, '首屏被改动'
e = s.index('<div class="cta-end rv">')
assert s[e:s.index('</section>', e)] == end0, '首页结尾 CTA 被改动'
open(P, 'w', encoding='utf8').write(s)
print('done.')
