"""关于页"机构支持""奖项与荣誉""公司信息"由一行一条改成横向多栏（Zixin 2026-10-14："考虑做成横版的排版吗 节省位置"）。
正文栏桌面只有约 580px（左侧有目录），所以用 3 栏；文字长的条目（张文宇教授、团队、研究成果）占 2 栏，让每行排满。
手机：奖项 2 栏（条目短）；机构支持、公司信息保持单栏（文字长）。只加类名和样式，文字不动，英文翻译照旧生效。
用法：python3 -I build_about_grid_2026-10-14.py <仓库 index.html>
"""
import sys

P = sys.argv[1]
s = open(P, encoding='utf8').read()
a = s.index('<section data-route="about"'); b = s.index('<section data-route=', a + 10)
ab = s[a:b]


def sub(old, new):
    global ab
    c = ab.count(old)
    if c != 1: sys.exit(f'[停止] 关于页匹配 {c} 次（应为 1）：{old[:60]}')
    ab = ab.replace(old, new)


for sid in ('ab-support', 'ab-honors', 'ab-company'):
    i = ab.index(f'id="{sid}"'); j = ab.index('<ul class="ab-rows">', i)
    if j - i > 200: sys.exit(f'[停止] {sid} 后面没紧跟 ab-rows 列表')
    ab = ab[:j] + f'<ul class="ab-rows ab-grid3 g-{sid[3:]}">' + ab[j + len('<ul class="ab-rows">'):]
sub('<li><span class="k">首席顾问</span>', '<li class="w2"><span class="k">首席顾问</span>')
sub('<li><span class="k">团队</span>', '<li class="w2"><span class="k">团队</span>')
sub('<li><span class="k">研究成果</span>', '<li class="w2"><span class="k">研究成果</span>')
s = s[:a] + ab + s[b:]

CSS = '''
<style id="about-grid">
/* 关于页三块信息改为横向 3 栏（2026-10-14）：每格顶线 + 小号标签 + 标题 + 说明 */
.ab-rows.ab-grid3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));column-gap:22px;border-top:0}
.ab-rows.ab-grid3 li{display:block;padding:14px 0 18px;border-top:1px solid var(--line);border-bottom:0}
.ab-rows.ab-grid3 li.w2{grid-column:span 2}
.ab-rows.ab-grid3 .k{display:block;margin-bottom:6px;line-height:1.5}
.ab-rows.ab-grid3 b{line-height:1.45}
.ab-rows.ab-grid3 .s{margin-top:4px;line-height:1.6}
@media (max-width:640px){
  .ab-rows.ab-grid3{grid-template-columns:1fr}
  .ab-rows.ab-grid3 li.w2{grid-column:auto}
  .ab-rows.ab-grid3.g-honors{grid-template-columns:repeat(2,minmax(0,1fr));column-gap:16px}
}
</style>
'''
k = s.rindex('</head>'); s = s[:k] + CSS + s[k:]
open(P, 'w', encoding='utf8').write(s)
print('done.')
