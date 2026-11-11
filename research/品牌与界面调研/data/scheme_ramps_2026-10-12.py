"""方案 B（晨昏蓝）与方案 C（松绿油画）的 OKLab 过渡带 + WCAG 对比度表 + 与同行主色的 ΔE2000。
token 逐字取自 demo/沐仞官网原型_2026-10-12.html 的 :root[data-scheme="B"] / :root[data-scheme="C"]；
ΔE2000 直接复用 color_distance_2026-10-12.py 的 de2000()（同行主色表也来自那里）。
输出：scheme_ramps_2026-10-12.json（所有数字）+ 终端打印可粘贴的 HTML 片段。
用法：python3 scheme_ramps_2026-10-12.py"""
import importlib.util, json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('cd', os.path.join(HERE, 'color_distance_2026-10-12.py'))
cd = importlib.util.module_from_spec(spec); spec.loader.exec_module(cd)
de2000, COMPETITORS = cd.de2000, cd.competitors

# ---------- sRGB <-> OKLab（Björn Ottosson 2020 系数） ----------
def hex2rgb(h): h = h.lstrip('#'); return [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
def rgb2hex(rgb): return '#%02X%02X%02X' % tuple(max(0, min(255, round(c * 255))) for c in rgb)
def lin(c): return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
def unlin(c): c = max(0.0, min(1.0, c)); return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055
def cbrt(x): return math.copysign(abs(x) ** (1 / 3), x)

def hex2oklab(h):
    r, g, b = (lin(c) for c in hex2rgb(h))
    l = cbrt(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b)
    m = cbrt(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b)
    s = cbrt(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b)
    return (0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
            1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
            0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s)

def oklab2hex(L, a, b):
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    r = 4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    bb = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s
    return rgb2hex([unlin(r), unlin(g), unlin(bb)])

def mix(h1, h2, t):
    A, B = hex2oklab(h1), hex2oklab(h2)
    return oklab2hex(*[A[i] + (B[i] - A[i]) * t for i in range(3)])

def ramp(anchors, n):
    """n 个等距停靠点，逐段 OKLab 线性插值穿过所有锚点（锚点在 0 … 1 等分位置）。"""
    out = []
    for k in range(n):
        t = k / (n - 1) * (len(anchors) - 1)
        i = min(int(t), len(anchors) - 2)
        out.append(mix(anchors[i], anchors[i + 1], t - i))
    return out

def lighten(h, dL, chroma=1.0):
    L, a, b = hex2oklab(h); return oklab2hex(L + dL, a * chroma, b * chroma)

# ---------- WCAG 2.x 对比度 ----------
def lum(h): r, g, b = (lin(c) for c in hex2rgb(h)); return 0.2126 * r + 0.7152 * g + 0.0722 * b
def contrast(fg, bg): x, y = lum(fg) + .05, lum(bg) + .05; return round(max(x, y) / min(x, y), 2)
def grade(r): return 'AAA' if r >= 7 else 'AA' if r >= 4.5 else 'AA 大字' if r >= 3 else '不合格'

# ---------- 原型 token（逐字） ----------
PROTO = {
    'B': dict(accent='#2F63B8', accent_fill='#5284D7', accent_soft='#DCE7F7', accent_tint='#EEF3FB',
              field_1='#A9C3E8', field_2='#E3ECF8', field_3='#EBCFC4', field_4='#D6CBDD',
              peak='#4E3F66', peak_soft='#EAE4F0', hz_1='#5284D7', hz_2='#B7A8A3', hz_2b='#3D314F', hz_3='#212021', hz_haze='#E8D4CC'),
    'C': dict(accent='#2F6B4A', accent_fill='#4F7A5C', accent_soft='#DCE8DC', accent_tint='#EEF4EE',
              field_1='#C9D9BE', field_2='#EEF4EE', field_3='#E8E0C6', field_4='#DCE8DC',
              peak='#2E4A38', peak_soft='#DCE6DA', hz_1='#8FB08E', hz_2='#4F7A5C', hz_2b='#2E4A38', hz_3='#0F1F18', hz_haze='#C9D9BE'),
}
NAMES = {
    'B': dict(accent='文字蓝', accent_fill='填充蓝', accent_soft='蓝 soft', accent_tint='蓝 tint', field_1='色场 1 · 浅蓝', field_2='色场 2 · 蓝雾',
              field_3='色场 3 · 霞粉', field_4='色场 4 · 淡紫', peak='峰时 · 暮紫浅', peak_soft='峰时底', hz_1='地平线 1 · 填充蓝', hz_2='地平线 2 · 霞',
              hz_2b='地平线 2b · 暮紫', hz_3='地平线 3 · 炭', hz_haze='霞光'),
    'C': dict(accent='文字绿', accent_fill='填充绿', accent_soft='绿 soft', accent_tint='绿 tint', field_1='色场 1 · 苔', field_2='色场 2 · 绿雾',
              field_3='色场 3 · 亚麻', field_4='色场 4 · 绿 soft', peak='峰时 · 松绿', peak_soft='峰时底', hz_1='地平线 1 · 鼠尾草', hz_2='地平线 2 · 填充绿',
              hz_2b='地平线 2b · 松绿', hz_3='地平线 3 · 炭绿', hz_haze='雾 · 苔'),
}
# 油画横带调色板（paint() 的 day），逐字取自原型
PAINT_DAY = dict(sky=['#2E4A38', '#4F7A5C', '#8FB08E', '#D9E3CF'], strokes=['#27402F', '#3F6A4B', '#6E9470', '#A9C3A3', '#C9D9BE', '#E8E0C6'], mist='#F2EFE4')

# ---------- 过渡带定义：名称、锚点、步数 ----------
RAMPS = {
    'B': [
        ('dark', '炭 → 暮紫 → 文字蓝（标题渐变、页脚、深色图板）', ['#212021', '#3D314F', '#2F63B8'], 7),
        ('light', '填充蓝 → 白（光斑、区块底、卡片、chip）', ['#5284D7', '#FFFFFF'], 7),
        ('horizon', '地平线：填充蓝 → 霞 → 暮紫 → 炭（原型首屏的晨昏带）', ['#5284D7', '#B7A8A3', '#3D314F', '#212021'], 13),
    ],
    'C': [
        ('dark', '炭绿 → 松绿 → 文字绿（标题渐变、页脚、深色图板）', ['#0F1F18', '#2E4A38', '#2F6B4A'], 7),
        ('light', '填充绿 → 白（区块底、卡片、chip）', ['#4F7A5C', '#FFFFFF'], 7),
        ('horizon', '油画天空：松绿 → 填充绿 → 鼠尾草 → 浅苔（paint() day 的 sky 四停）', PAINT_DAY['sky'], 13),
    ],
}

def nearest_on_ramp(h, stops):
    d = [(de2000(h, s), s) for s in stops]; return min(d)

def analyse(key):
    P = PROTO[key]; out = dict(tokens=P, ramps={}, derived={}, contrast_white=[], contrast_dark=[], competitors={})
    for rid, label, anchors, n in RAMPS[key]:
        stops = ramp(anchors, n)
        adj = [round(de2000(stops[i], stops[i + 1]), 1) for i in range(n - 1)]
        out['ramps'][rid] = dict(label=label, anchors=anchors, stops=stops, adjacent_dE=adj, max_adjacent_dE=max(adj))
    # 原型的浅色 token 落在「填充 → 白」带的哪里
    light = out['ramps']['light']['stops']
    for name in ('field_1', 'accent_soft', 'field_2', 'accent_tint', 'hz_1', 'peak_soft', 'field_4'):
        d, s = nearest_on_ramp(P[name], light)
        out['ramps']['light'].setdefault('proto_on_ramp', {})[name] = dict(hex=P[name], nearest=s, dE=round(d, 1))
    # 派生 token（demo 自己的变量名需要的中间值）
    D = out['derived']
    D['brand_600'] = mix(P['accent_fill'], P['accent'], .5)
    D['brand_800'] = lighten(P['accent'], -.07)
    D['t400'] = mix(P['field_1'], P['accent_fill'], .5) if key == 'B' else P['hz_1']
    D['peak_soft_2'] = mix(P['peak_soft'], '#FFFFFF', .5)
    D['art_bg1'], D['art_bg2'] = (P['hz_3'], P['hz_2b'])
    D['art_dot'] = mix(D['art_bg1'], D['art_bg2'], .5)
    D['art_bright'] = lighten(P['accent_fill'], .22, .85) if key == 'B' else lighten(P['hz_1'], .14, .9)
    D['n_ramp'] = out['ramps']['dark']['stops']
    D['t300'] = P['field_1'] if key == 'B' else out['ramps']['light']['stops'][3]
    D['fbtn'] = (P['field_1'], D['t400'], P['hz_3']) if key == 'B' else (D['art_bright'], P['hz_1'], P['hz_3'])
    # 成对对比度：主按钮白字、页脚按钮深字、chip 文字对底
    pairs = [('主按钮上半 白字', '#FFFFFF', D['brand_600']), ('主按钮下半 白字', '#FFFFFF', P['accent']), ('填充色上白字', '#FFFFFF', P['accent_fill']),
             ('页脚按钮上半 深字', D['fbtn'][2], D['fbtn'][0]), ('页脚按钮下半 深字', D['fbtn'][2], D['fbtn'][1]),
             ('峰时文字 on 峰时底', P['hz_2b'], P['peak_soft']), ('文字色 on tint', P['accent'], P['accent_tint'])]
    out['contrast_pairs'] = [dict(name=n, fg=f, bg=b, ratio=contrast(f, b), grade=grade(contrast(f, b))) for n, f, b in pairs]
    # 对比度：全部 token 对白，深色图板文字对炭
    for name, h in P.items():
        r = contrast(h, '#FFFFFF'); out['contrast_white'].append(dict(token=name, name=NAMES[key][name], hex=h, ratio=r, grade=grade(r)))
    dark = P['hz_3']
    for name, h in [('白', '#FFFFFF'), ('霞 hz-2' if key == 'B' else '鼠尾草 hz-1', P['hz_2'] if key == 'B' else P['hz_1']),
                    ('色场 1', P['field_1']), ('填充', P['accent_fill']), ('高光（派生）', D['art_bright'])]:
        r = contrast(h, dark); out['contrast_dark'].append(dict(name=name, hex=h, bg=dark, ratio=r, grade=grade(r)))
    # 与同行主色的 ΔE2000（color_distance 的方法与色表）
    for name in ('accent', 'accent_fill', 'peak', 'hz_2b'):
        ds = sorted((round(de2000(P[name], c), 1), cn, c) for cn, c in COMPETITORS.items())
        out['competitors'][name] = dict(hex=P[name], nearest=ds[:3])
    return out

def ramp_html(stops, lt_from=None):
    """.ramp 的 span 片段；浅色停靠点加 class=lt 让标签用深字。"""
    parts = []
    for s in stops:
        lt = ' class="lt"' if contrast(s, '#FFFFFF') < 4.5 else ''
        parts.append(f'<span style="background:{s}"{lt}><i>{s}</i></span>')
    return '<div class="ramp">' + ''.join(parts) + '</div>'

def table_html(R):
    rows = ''.join(f'<tr><td class="mono">{c["hex"]}</td><td>{c["name"]}<span class="tk2">--{c["token"].replace("_","-")}</span></td><td class="num">{c["ratio"]:.2f}</td><td>{c["grade"]}</td></tr>' for c in R['contrast_white'])
    rows2 = ''.join(f'<tr><td class="mono">{c["hex"]} / {c["bg"]}</td><td>{c["name"]} on 炭</td><td class="num">{c["ratio"]:.2f}</td><td>{c["grade"]}</td></tr>' for c in R['contrast_dark'])
    rows3 = ''.join(f'<tr><td class="mono">{c["fg"]} / {c["bg"]}</td><td>{c["name"]}</td><td class="num">{c["ratio"]:.2f}</td><td>{c["grade"]}</td></tr>' for c in R['contrast_pairs'])
    return ('<table class="ctab"><thead><tr><th>色值</th><th>token</th><th>对白</th><th>WCAG</th></tr></thead><tbody>' + rows +
            '</tbody><thead><tr><th>前景 / 背景</th><th>深色图板上</th><th>比值</th><th>WCAG</th></tr></thead><tbody>' + rows2 +
            '</tbody><thead><tr><th>前景 / 背景</th><th>成对</th><th>比值</th><th>WCAG</th></tr></thead><tbody>' + rows3 + '</tbody></table>')

if __name__ == '__main__':
    res = {k: analyse(k) for k in ('B', 'C')}
    res['paint_day'] = PAINT_DAY
    json.dump(res, open(os.path.join(HERE, 'scheme_ramps_2026-10-12.json'), 'w'), ensure_ascii=False, indent=1)
    for k in ('B', 'C'):
        R = res[k]
        print(f'\n===== 方案 {k} =====')
        for rid, r in R['ramps'].items():
            print(f'[{rid}] {r["label"]}\n   stops: {r["stops"]}\n   adjacent ΔE2000: {r["adjacent_dE"]} max={r["max_adjacent_dE"]}')
            if 'proto_on_ramp' in r:
                for n, v in r['proto_on_ramp'].items(): print(f'   原型 {n} {v["hex"]} ≈ 带上 {v["nearest"]} ΔE={v["dE"]}')
            print('   html:', ramp_html(r['stops']))
        print('derived:', json.dumps(R['derived'], ensure_ascii=False))
        print('contrast vs white:')
        for c in R['contrast_white']: print(f'   {c["token"]:12s} {c["hex"]} {c["name"]:14s} {c["ratio"]:5.2f} {c["grade"]}')
        print(f'contrast on dark {R["contrast_dark"][0]["bg"]}:')
        for c in R['contrast_dark']: print(f'   {c["name"]:12s} {c["hex"]} {c["ratio"]:5.2f} {c["grade"]}')
        print('pairs:')
        for c in R['contrast_pairs']: print(f'   {c["name"]:16s} {c["fg"]} on {c["bg"]} {c["ratio"]:5.2f} {c["grade"]}')
        print('table html:', table_html(R))
        print('nearest competitor ΔE2000:')
        for n, v in R['competitors'].items(): print(f'   {n} {v["hex"]}: ' + '; '.join(f'{cn} {c} ΔE={d}' for d, cn, c in v['nearest']))
