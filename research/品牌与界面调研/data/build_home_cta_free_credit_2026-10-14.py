"""首页"获取 API Key"按钮改为免费额度钩子（Zixin 2026-10-14："获取 api key 可以换成表述'先送免费额度拉人'"）。
依据：报价单 2026-10-08"如需试用额度，欢迎申请免费测试包"。第一版写"申请免费测试额度"，Zixin 改为"不要申请，就写免费试用"→"免费试用 API"；不写金额，也不写"注册即送"。
范围：首页首屏、首页结尾两个按钮 + 只在首页出现的底部常驻按钮；其他页面的"获取 API Key"不动。
用法：python3 -I build_home_cta_free_credit_2026-10-14.py <仓库 index.html> [原型.html]
"""
import json, sys

ZH_D, ZH_R = '免费试用 API ↓', '免费试用 API →'
OLD = ('获取 API Key', '申请免费测试额度')  # 依次兼容线上曾用过的按钮文案
EN = {ZH_D: 'Try the API free ↓', ZH_R: 'Try the API free →', '免费试用 API': 'Try the API free'}

for path in sys.argv[1:]:
    s = open(path, encoding='utf8').read()
    k = s.find('var I18N={')
    pre, post = (s[:k], s[k:]) if k >= 0 else (s, '')
    if '<div id="home2">' in pre:  # 线上站：只改 #home2 与底部常驻按钮
        a = pre.index('<div id="home2">'); b = pre.index('<section data-route=', a)
        home = pre[a:b]
        o = next((x for x in OLD if home.count(f'>{x} ↓</a>') == 2), None)
        if o is None: sys.exit('[停止] 首页内找不到 2 处旧按钮文案')
        pre = pre[:a] + home.replace(f'>{o} ↓</a>', f'>{ZH_D}</a>') + pre[b:]
        dk = '<div class="dock" id="dock" aria-hidden="true"><a class="btn black" href="#start" tabindex="-1">'
        old = next((dk + f'{x} →</a></div>' for x in OLD if pre.count(dk + f'{x} →</a></div>') == 1), None)
        if old is None: sys.exit('[停止] 底部常驻按钮未找到')
        pre = pre.replace(old, dk + f'{ZH_R}</a></div>')
    else:  # 原型
        o = next((x for x in OLD if f'>{x} ↓</a>' in pre), None)
        if o is None: sys.exit('[停止] 原型里没有旧按钮文案')
        pre = pre.replace(f'>{o} ↓</a>', f'>{ZH_D}</a>').replace(f'>{o} →</a>', f'>{ZH_R}</a>')
    s = pre + post
    if k >= 0:
        k2 = s.index('var I18N={') + len('var I18N={')
        s = s[:k2] + ''.join(json.dumps(x, ensure_ascii=False) + ':' + json.dumps(y, ensure_ascii=False) + ',' for x, y in EN.items()) + s[k2:]
    open(path, 'w', encoding='utf8').write(s)
    print('done:', path)
