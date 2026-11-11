"""首页"行业与场景"示意图 + 功能区面板配色，按 Dia 视觉语言、只用沐仞色卡：
- 行业 / 模型 = Dia 式灰底胶囊：彩色圆点（色卡六色轮换）+ 名称 + 白色内嵌小标签（如 Dia 的 On/Off）。
- 交易平台 / 群智基座 = Dia 窗口式半透明色面板（雾蓝 / 薰衣草），内嵌白色小胶囊。
- 光伏 / 风电 / 水电 = 三张不同色调的卡（霞粉 / 雾蓝 / 薰衣草），图标用色卡深色。
- 连线光点按色卡多色流动（prefers-reduced-motion 时隐藏）。
- 功能区 01/02/03 说明压成一句；右侧三块滑动面板各一种色调（雾蓝 / 霞粉 / 薰衣草）。
- 文档代码块的语法高亮从青 / 橙改为雾蓝 / 霞粉。
色卡：晨蓝 #2F63B8 #5284D7 · 雾蓝 #A9C3E8 #E3ECF8 · 暮紫 #4E3F66 #3D314F · 薰衣草 #D6CBDD · 霞粉 #EBCFC4 #E8D4CC · 炭 #212021。
CSS 插到最后一个 </style> 前。首屏 HTML 与结尾 CTA 不变。
用法：python3 -I build_home_schematic_2026-10-14.py <仓库副本目录>
"""
import json, os, sys

P = os.path.join(sys.argv[1], 'index.html')
s = open(P, encoding='utf8').read()
hero0 = s[s.index('<div class="hero">'):s.index('<div class="partners">')]
end0 = s[s.index('<div class="cta-end rv">'):s.index('</section>', s.index('<div class="cta-end rv">'))]

def rep(old, new, n=1):
    global s
    k = s.index('var I18N={')
    c = s[:k].count(old)
    if c != n: sys.exit(f'[停止] 匹配 {c} 次（应为 {n}）：{old[:80]}')
    s = s[:k].replace(old, new) + s[k:]

# ---------- 功能区三句压短 ----------
rep('配置接入地址、API Key 和模型名称，用一条真实任务检查返回格式与流式输出，通过后切换业务流量。', '改接入地址和 API Key，跑通一条真实任务，再切业务流量。')
rep('价格按模型、调用规模、响应时延、并发需求和绿电来源计算；公开价在模型市场查看，企业用量可以按量报价。', '按模型、用量、时延和绿电来源计价；公开价在模型市场，企业可按量报价。')
rep('每笔订单附一张产地卡：哪座电站、哪个时段、用了多少电、产出多少词元。做绿色采购、ESG 披露或跨境业务时，手里有一份可追溯的数据。', '每笔订单一张产地卡：哪座电站、哪个时段、用了多少电、产出多少词元。')
# 代码块高亮回到色卡
rep('.code .c{color:#7BC9D0} .code .s{color:#F0C27B}', '.code .c{color:#A9C3E8} .code .s{color:#EBCFC4}')

# ---------- 示意图 ----------
DOTS = ['#2F63B8', '#A9C3E8', '#4E3F66', '#EBCFC4', '#5284D7', '#D6CBDD']

def ico(path, w=22):
    return f'<svg viewBox="0 0 24 24" width="{w}" height="{w}" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{path}</g></svg>'

def pill(text, tag, dot):
    return f'<span class="sxp"><b style="background:{dot}"></b><span class="t">{text}</span>' + (f'<span class="v">{tag}</span>' if tag else '') + '</span>'

IND = [('AI 短剧与影视', '批量'), ('AI for Science', '科研'), ('社交与陪伴', '对话'),
       ('内容与图文审核', '审核'), ('AI Agent', '多模型'), ('企业知识库', 'B 端')]
MODELS = ['DeepSeek', 'Qwen', 'GLM', 'MiniMax']
PLANTS = [('sun', '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>', '光伏电站'),
          ('wind', '<path d="M12 12v10M12 12 8 3M12 12l9 3M12 12l-8 6"/><circle cx="12" cy="12" r="1.4"/>', '风电场'),
          ('hydro', '<path d="M12 3s6 7 6 11a6 6 0 0 1-12 0c0-4 6-11 6-11z"/>', '水电站')]

def wire(src, dst, h=64):
    paths = ''.join(f'<path d="M{a:.1f} 0 C{a:.1f} {h * .55:.0f} {b:.1f} {h * .45:.0f} {b:.1f} {h}"/>' for a, b in zip(src, dst))
    return f'<svg class="sx-w" style="height:{h}px" viewBox="0 0 1000 {h}" preserveAspectRatio="none" aria-hidden="true"><g class="base">{paths}</g><g class="flow">{paths}</g></svg>'

c3 = [(i + .5) / 3 * 1000 for i in range(3)]
WIRE_IN = wire(c3, [500] * 3)
WIRE_LINE = wire([500], [500], 36)
WIRE_OUT = wire([500] * 3, c3)

def wrow(svg):
    return f'<div class="sx-r sx-wr"><span></span>{svg}</div>'

SX = ('<div class="sec sx-sec"><div class="hh c rv"><span class="k">一张图看懂</span><h2>行业与场景</h2>'
      '<p class="sx-lead">已有词元采购客户包括某 AI for Science 独角兽、某全球头部社交平台，以及某头部大厂的跨境电商图文审核。</p></div>\n'
      '      <div class="sx rv">'
      '<div class="sx-r"><span class="sx-k">场景</span><div class="sx-g3p">' + ''.join(pill(t, v, DOTS[i]) for i, (t, v) in enumerate(IND)) + '</div></div>'
      + wrow(WIRE_IN)
      + '<a class="sx-r sx-a" href="#models" data-product-target="p-api"><span class="sx-k">接口</span><span class="sxw mist"><b>绿色词元交易平台</b>'
        '<span class="sxw-v"><i>统一 API</i><i>OpenAI / Gemini 格式</i><i>按词元计费</i></span><em aria-hidden="true">→</em></span></a>'
      + wrow(WIRE_LINE)
      + '<a class="sx-r sx-a" href="#models" data-product-target="p-market"><span class="sx-k">模型</span><span class="sx-models">'
        + ''.join(pill(m, '', DOTS[[0, 2, 4, 5][i]]) for i, m in enumerate(MODELS)) + '<em aria-hidden="true">→</em></span></a>'
      + wrow(WIRE_LINE)
      + '<a class="sx-r sx-a" href="#models" data-product-target="p-base"><span class="sx-k">调度</span><span class="sxw lav"><b>算电协同群智基座</b>'
        '<span class="sxw-v"><i>任务时限</i><i>电力预测</i><i>节点状态</i></span><em aria-hidden="true">→</em></span></a>'
      + wrow(WIRE_OUT)
      + '<a class="sx-r sx-a" href="#models" data-product-target="p-box"><span class="sx-k">电站</span><span class="sx-g3">'
        + ''.join(f'<span class="sx-plant {k}">{ico(p)}<b>{t}</b><i>FPTM 一体机</i></span>' for k, p, t in PLANTS) + '</span></a>'
      + '</div></div>\n    ')

pre = s[:s.index('var I18N={')]
a = pre.index('<div class="sec fq-sec">')
b = pre.index('<div class="sec home-sec">', a)
s = s[:a] + SX + s[b:]

flow_css = ''.join(f'.sx-w .flow path:nth-child(6n+{i + 1}){{stroke:{c}}}' for i, c in enumerate(['#2F63B8', '#4E3F66', '#5284D7', '#D6CBDD', '#A9C3E8', '#EBCFC4']))
CSS = '''
/* 首页行业与场景示意图（Dia 视觉语言 + 沐仞色卡） */
.sx-sec{margin-top:140px}
.sx-lead{max-width:40em;margin:14px auto 0;font-size:15px;line-height:1.7;color:var(--ink-50)}
.sx{max-width:1000px;margin:40px auto 0}
.sx-r{display:grid;grid-template-columns:64px minmax(0,1fr);align-items:center;column-gap:16px;color:var(--ink);text-decoration:none}
.sx-k{font:400 11px var(--mono);letter-spacing:.08em;color:var(--ink-30)}
.sx-g3p{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px 12px}
.sxp{display:inline-flex;align-items:center;gap:10px;min-width:0;padding:7px 8px 7px 16px;border-radius:var(--pill);background:#EFEDEA;font:400 13px var(--mono);letter-spacing:.02em;color:var(--ink)}
.sxp b{width:9px;height:9px;border-radius:50%;flex:none}
.sxp .t{flex:1;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.sxp .v{flex:none;padding:3px 9px;border-radius:6px;background:#fff;font-size:12px;color:var(--ink-70)}
.sx-w{display:block;width:100%;overflow:visible}
.sx-w path{fill:none;vector-effect:non-scaling-stroke}
.sx-w .base path{stroke:rgba(33,32,33,.10);stroke-width:1.5}
.sx-w .flow path{stroke-width:3;stroke-linecap:round;stroke-dasharray:1 26;animation:sxflow 2.6s linear infinite}
''' + flow_css + '''
@keyframes sxflow{to{stroke-dashoffset:-54}}
.sxw{position:relative;display:flex;flex-direction:column;align-items:center;gap:10px;max-width:560px;width:100%;margin:0 auto;padding:16px 46px 14px;border-radius:16px;text-align:center;backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);box-shadow:0 10px 30px -18px rgba(33,32,33,.35);transition:transform .3s var(--ease-out)}
.sxw.mist{background:rgba(227,236,248,.85);border:1px solid rgba(169,195,232,.7)}
.sxw.lav{background:rgba(234,228,240,.85);border:1px solid rgba(214,203,221,.9)}
.sxw b{font-family:var(--serif);font-weight:400;font-size:21px;letter-spacing:-.01em;color:var(--ink)}
.sxw-v{display:flex;flex-wrap:wrap;justify-content:center;gap:6px}
.sxw-v i{font-style:normal;padding:3px 10px;border-radius:6px;background:rgba(255,255,255,.85);font:400 12px var(--mono);color:var(--ink-70)}
.sx-r em{position:absolute;right:16px;top:50%;margin-top:-10px;font-style:normal;color:var(--ink-30);transition:transform .3s var(--ease),color .2s}
.sx-models{position:relative;display:flex;justify-content:center;flex-wrap:wrap;gap:10px;max-width:560px;width:100%;margin:0 auto;padding:4px 40px}
.sx-models .sxp{padding:7px 16px}
.sx-g3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}
.sx-plant{display:flex;flex-direction:column;align-items:center;gap:6px;padding:18px 8px 14px;border-radius:16px;transition:transform .3s var(--ease-out)}
.sx-plant.sun{background:rgba(235,207,196,.45);border:1px solid rgba(235,207,196,.9);color:#4E3F66}
.sx-plant.wind{background:rgba(227,236,248,.85);border:1px solid rgba(169,195,232,.7);color:#2F63B8}
.sx-plant.hydro{background:rgba(234,228,240,.85);border:1px solid rgba(214,203,221,.9);color:#3D314F}
.sx-plant b{font-weight:500;font-size:14px;color:var(--ink)}
.sx-plant i{font-style:normal;padding:3px 10px;border-radius:6px;background:rgba(255,255,255,.85);font:400 11px var(--mono);color:var(--ink-70)}
a.sx-a:hover .sxw,a.sx-a:hover .sx-plant{transform:translateY(-2px)}
a.sx-a:hover em{transform:translateX(4px);color:var(--ink)}
/* 功能区右侧滑动面板：每块一种色调（学 Dia） */
.feat .shot[data-s="0"]{background:#E3ECF8;border-color:rgba(169,195,232,.7)}
.feat .shot[data-s="1"]{background:#F6EBE6;border-color:rgba(235,207,196,.9)}
.feat .shot[data-s="2"]{background:#EAE4F0;border-color:rgba(214,203,221,.9)}
@media (prefers-reduced-motion:reduce){.sx-w .flow{display:none}}
@media (max-width:800px){
  .sx-r{grid-template-columns:1fr}
  .sx-k,.sx-r em{display:none}
  .sx-wr span{display:none}
  .sx-g3p{grid-template-columns:1fr 1fr;gap:8px}
  .sxp{font-size:12px;padding:6px 6px 6px 12px;gap:8px}
  .sxp .v{display:none}
  .sxw{padding:14px 16px}
  .sx-models{padding:4px 0}
  .sx-g3{gap:8px}
  .sx-plant b{font-size:13px}
}
'''
k = s.rindex('</style>')
s = s[:k] + CSS + s[k:]

EN = {"改接入地址和 API Key，跑通一条真实任务，再切业务流量。": "Change the endpoint and API key, run one real job, then switch traffic.",
      "按模型、用量、时延和绿电来源计价；公开价在模型市场，企业可按量报价。": "Priced by model, volume, latency and green-power source; public prices are in the model market, and enterprises can get volume quotes.",
      "每笔订单一张产地卡：哪座电站、哪个时段、用了多少电、产出多少词元。": "Every order comes with an origin card: which plant, which hours, how much power, how many tokens.",
      "一张图看懂": "At a glance", "社交与陪伴": "Social & companionship", "AI 短剧与影视": "AI short drama & video",
      "批量": "Batch", "科研": "Research", "对话": "Chat", "审核": "Review", "多模型": "Multi-model", "B 端": "B2B",
      "OpenAI / Gemini 格式": "OpenAI / Gemini formats", "任务时限": "Deadlines", "电力预测": "Power forecasts", "节点状态": "Node status",
      "电站": "Plants", "光伏电站": "Solar plants", "风电场": "Wind farms", "水电站": "Hydro plants", "FPTM 一体机": "FPTM appliance"}
k2 = s.index('var I18N={') + len('var I18N={')
s = s[:k2] + ''.join(json.dumps(x, ensure_ascii=False) + ':' + json.dumps(y, ensure_ascii=False) + ',' for x, y in EN.items()) + s[k2:]

assert s[s.index('<div class="hero">'):s.index('<div class="partners">')] == hero0, '首屏 HTML 被改动'
e = s.index('<div class="cta-end rv">')
assert s[e:s.index('</section>', e)] == end0, '首页结尾 CTA 被改动'
open(P, 'w', encoding='utf8').write(s)
print('done.')
