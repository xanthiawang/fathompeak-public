"""首页"行业与场景"去掉上下双线；补英文模式漏翻（分层列表里的胶囊与标题）。
用法：python3 -I fix_home_rules_en_2026-10-13.py <仓库副本目录>
"""
import json, os, sys

P = os.path.join(sys.argv[1], 'index.html')
s = open(P, encoding='utf8').read()
hero0 = s[s.index('<div class="hero">'):s.index('<div class="partners">')]

k = s.index('var I18N={')
pre, post = s[:k], s[k:]
for old in ('<div class="fq-rule"></div>', '<div class="fq-rule b"></div>'):
    if pre.count(old) != 1: sys.exit(f'[停止] {old} 匹配 {pre.count(old)} 次')
    pre = pre.replace(old, '')
pre = pre.replace('.fq-h{text-align:center;font-family:var(--serif);font-weight:400;font-size:36px;letter-spacing:-.02em;margin:44px 0 10px}',
                  '.fq-h{text-align:center;font-family:var(--serif);font-weight:400;font-size:36px;letter-spacing:-.02em;margin:0 0 10px}')
s = pre + post

EN = {"统一 API": "Unified API", "主流大模型": "Leading models", "FPTM 词元一体机 · 新能源电站": "FPTM token appliances · renewable plants",
      "光伏": "Solar", "风电": "Wind", "水电": "Hydro", "既有算力中心": "Existing compute centers", "按词元计费": "Per-token billing",
      "场景": "Use cases", "接口": "API", "模型": "Models", "调度": "Scheduling", "算力与能源": "Compute & energy"}
k2 = s.index('var I18N={') + len('var I18N={')
s = s[:k2] + ''.join(json.dumps(x, ensure_ascii=False) + ':' + json.dumps(y, ensure_ascii=False) + ',' for x, y in EN.items()) + s[k2:]

assert s[s.index('<div class="hero">'):s.index('<div class="partners">')] == hero0, '首屏 HTML 被改动'
open(P, 'w', encoding='utf8').write(s)
print('done.')
