"""首页行业卡去掉上方大图（油画裁切 + 白色小卡）：面积太大、各卡之间没有区别。
只留 应用图标式色块 + 行业名、衬线结果标题、分类 + 箭头。首屏与结尾 CTA 不变。
用法：python3 -I fix_home_cards_noart_2026-10-13.py <仓库副本目录>
"""
import os, re, sys

P = os.path.join(sys.argv[1], 'index.html')
s = open(P, encoding='utf8').read()
hero0 = s[s.index('<div class="hero">'):s.index('<div class="partners">')]

s, n = re.subn(r'<span class="fa-art"[^>]*>.*?<i class="s"></i></span></span>', '', s, flags=re.S)
if n != 6: sys.exit(f'[停止] 大图匹配 {n} 处（应为 6）')
for rule in [r'\.fa-art\{[^}]*\}\n', r'\.fa-doc[^{]*\{[^}]*\}\n']:
    s = re.sub(rule, '', s)
old = '.fa-b{display:flex;flex-direction:column;flex:1;padding:18px 20px 16px}'
assert s.count(old) == 1
s = s.replace(old, '.fa-b{display:flex;flex-direction:column;flex:1;padding:22px 22px 18px}')

assert s[s.index('<div class="hero">'):s.index('<div class="partners">')] == hero0, '首屏 HTML 被改动'
open(P, 'w', encoding='utf8').write(s)
print('done. removed', n)
