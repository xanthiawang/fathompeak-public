"""首页去重：删掉"一张图看懂沐仞"分层图（第 01 层与行业卡重复，02–05 层与功能区 01/02/03、"为什么是沐仞"重复）；
按硅基流动首页顺序（产品 → 为什么选择 → 行业 → 客户）把"为什么是沐仞"移到"行业与场景"前面。
首屏与结尾 CTA 不变。
用法：python3 -I fix_home_dedupe_2026-10-13.py <仓库副本目录>
"""
import os, sys

P = os.path.join(sys.argv[1], 'index.html')
s = open(P, encoding='utf8').read()
hero0 = s[s.index('<div class="hero">'):s.index('<div class="partners">')]
end0 = s[s.index('<div class="cta-end rv">'):s.index('</section>', s.index('<div class="cta-end rv">'))]

# 1. 删分层图
a = s.index('<div class="sec fq-sec">')
b = s.index('<div class="fq-rule b"></div></div>', a) + len('<div class="fq-rule b"></div></div>')
while s[b] in ' \n': b += 1
s = s[:a] + s[b:]

# 2. "为什么是沐仞"移到"行业与场景"之前
WHY0 = '<div class="sec" style="margin-top:44px"><div class="hd"><h3 class="serif">为什么是沐仞</h3>'
w = s.index(WHY0)
w_end = s.index('\n  </div>\n  <div class="wrap rv"><div class="sec"><div class="hd"><h3 class="serif">新闻', w)
why = s[w:w_end]
s = s[:w] + s[w_end:]
IND0 = '<div class="sec"><div class="hd"><h3 class="serif">行业与场景</h3>'
i = s.index(IND0)
s = s[:i] + why + '\n    <div class="sec" style="margin-top:44px"><div class="hd"><h3 class="serif">行业与场景</h3>' + s[i + len(IND0):]
assert s.count('为什么是沐仞</h3>') == 1 and s.count('行业与场景</h3>') == 1 and 'fq-sec' not in s.split('<style')[0] + s[s.index('<body'):]

assert s[s.index('<div class="hero">'):s.index('<div class="partners">')] == hero0, '首屏 HTML 被改动'
e = s.index('<div class="cta-end rv">')
assert s[e:s.index('</section>', e)] == end0, '首页结尾 CTA 被改动'
open(P, 'w', encoding='utf8').write(s)
print('done.')
