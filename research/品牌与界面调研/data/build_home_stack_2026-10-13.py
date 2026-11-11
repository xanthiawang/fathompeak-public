"""首页分层图"一张图看懂沐仞"：放在行业与场景之后、项目案例之前。
自上而下 场景 → 接口（交易平台）→ 模型 → 调度（群智基座）→ 一体机与电站，颜色从天空蓝渐到炭黑（同首屏地平线色卡）。
文字都来自站上已有说法。第 2–5 层可点，跳到产品页对应条目。
用法：python3 -I build_home_stack_2026-10-13.py <仓库副本目录>
"""
import json, os, sys

P = os.path.join(sys.argv[1], 'index.html')
s = open(P, encoding='utf8').read()
hero0 = s[s.index('<div class="hero">'):s.index('<div class="partners">')]
end0 = s[s.index('<div class="cta-end rv">'):s.index('</section>', s.index('<div class="cta-end rv">'))]

def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: sys.exit(f'[停止] 匹配 {c} 次（应为 {n}）：{old[:80]}')
    s = s.replace(old, new)

def layer(cls, k, title, desc, chips, target=None):
    inner = (f'<span class="ly-k">{k}</span><div class="ly-m"><b>{title}</b>' + (f'<span>{desc}</span>' if desc else '') + '</div>'
             '<span class="ly-c">' + ''.join(f'<i>{c}</i>' for c in chips) + '</span>')
    if target:
        return f'<a class="ly {cls}" href="#models" data-product-target="{target}">{inner}<span class="ly-go" aria-hidden="true">→</span></a>'
    return f'<div class="ly {cls}">{inner}<span class="ly-go"></span></div>'

STACK = ('<div class="sec stack-sec"><div class="hd"><h3 class="serif">一张图看懂沐仞</h3><span class="k">上层调用 · 下层发电</span></div>\n'
         '      <p class="ind-lead">上层是你调用的接口，下层是电站旁运行模型的一体机；中间由调度基座把任务排到绿电富余的节点。</p>\n'
         '      <div class="lstack">'
         + layer('l1', '01 · 场景', '你的业务', '', ['AI 短剧与内容生成', 'AI for Science', 'AI Agent 平台', '企业知识库', '词元出海'])
         + layer('l2', '02 · 接口', '绿色词元交易平台', '一个端点接入主流模型，兼容 OpenAI 与 Gemini 原生格式，按词元计费。', ['统一 API', '按词元计费', '订单能源记录'], 'p-api')
         + layer('l3', '03 · 模型', '主流大模型', '', ['DeepSeek', 'Qwen', 'GLM', 'MiniMax'], 'p-market')
         + layer('l4', '04 · 调度', '算电协同群智基座', '结合任务时限、电力预测与节点状态，把任务排到绿电富余的节点运行。', ['Tapestrix', 'NetWeaver'], 'p-base')
         + layer('l5', '05 · 算力与能源', 'FPTM 词元一体机 · 新能源电站', '一体机部署在光伏、风电、水电场站旁，用富余绿电生产词元。', ['光伏', '风电', '水电', '既有算力中心'], 'p-box')
         + '</div></div>\n    ')

anchor = '<div class="sec" style="margin-top:44px"><div class="hd"><h3 class="serif">项目案例</h3>'
rep(anchor, STACK + anchor)

CSS = '''
/* 首页分层图：自上而下 场景 → 接口 → 模型 → 调度 → 一体机与电站，颜色从天空蓝渐到炭黑 */
.stack-sec{margin-top:56px}
.lstack{display:grid;gap:6px}
.ly{display:grid;grid-template-columns:150px minmax(0,1fr) auto 24px;align-items:center;gap:20px;padding:20px 24px;border-radius:var(--r12);color:var(--ink);text-decoration:none;transition:transform .25s var(--ease-out),box-shadow .25s var(--ease)}
a.ly:hover{transform:translateY(-2px);box-shadow:0 14px 30px -18px rgba(33,32,33,.45)}
.ly-k{font:400 12px var(--mono);letter-spacing:.04em;opacity:.7}
.ly-m b{display:block;font-family:var(--serif);font-weight:600;font-size:21px;line-height:1.25;letter-spacing:-.01em}
.ly-m span{display:block;margin-top:4px;font-size:14px;line-height:1.6;opacity:.8}
.ly-c{display:flex;flex-wrap:wrap;justify-content:flex-end;gap:6px;max-width:440px}
.ly-c i{font-style:normal;font:400 12px var(--sans);padding:4px 10px;border-radius:var(--pill);border:1px solid currentColor;opacity:.85;white-space:nowrap}
.ly-go{font-size:16px;opacity:.6;text-align:right}
.ly.l1{background:var(--card);border:1px solid var(--line)}
.ly.l1 .ly-c{max-width:680px}
.ly.l2{background:#DCE7F7;color:#1F3F78}
.ly.l3{background:#E9DCD8;color:#4E3F66}
.ly.l4{background:#7A6071;color:#fff}
.ly.l5{background:radial-gradient(70% 140% at 85% 0%,rgba(122,96,113,.55),transparent 70%),#212021;color:#fff}
.ly.l4 .ly-c i,.ly.l5 .ly-c i{border-color:rgba(255,255,255,.45)}
@media (max-width:1000px){.ly{grid-template-columns:110px minmax(0,1fr) 20px}.ly-c{grid-column:2/3;justify-content:flex-start;max-width:none}.ly-go{grid-row:1;grid-column:3}}
@media (max-width:800px){.ly{grid-template-columns:minmax(0,1fr) 20px;gap:10px;padding:18px}.ly-k{grid-column:1}.ly-m,.ly-c{grid-column:1}.ly-go{grid-row:1;grid-column:2}.ly-m b{font-size:19px}}
'''
k = s.index('</style>')
s = s[:k] + CSS + s[k:]

EN = {"一张图看懂沐仞": "FathomPeak at a glance", "上层调用 · 下层发电": "Calls on top · power below",
      "上层是你调用的接口，下层是电站旁运行模型的一体机；中间由调度基座把任务排到绿电富余的节点。": "On top is the API you call; at the bottom are the appliances running models beside power plants. In between, the scheduling base routes each job to nodes with surplus green power.",
      "01 · 场景": "01 · Use cases", "你的业务": "Your business", "02 · 接口": "02 · API",
      "一个端点接入主流模型，兼容 OpenAI 与 Gemini 原生格式，按词元计费。": "One endpoint for leading models, compatible with native OpenAI and Gemini formats, billed per token.",
      "统一 API": "Unified API", "按词元计费": "Per-token billing", "订单能源记录": "Order energy records",
      "03 · 模型": "03 · Models", "主流大模型": "Leading models", "04 · 调度": "04 · Scheduling",
      "结合任务时限、电力预测与节点状态，把任务排到绿电富余的节点运行。": "Uses job deadlines, power forecasts and node status to run jobs on nodes with surplus green power.",
      "05 · 算力与能源": "05 · Compute & energy", "FPTM 词元一体机 · 新能源电站": "FPTM token appliances · renewable plants",
      "一体机部署在光伏、风电、水电场站旁，用富余绿电生产词元。": "Appliances sit beside solar, wind and hydro plants and turn surplus green power into tokens.",
      "光伏": "Solar", "风电": "Wind", "既有算力中心": "Existing compute centers"}
k2 = s.index('var I18N={') + len('var I18N={')
s = s[:k2] + ''.join(json.dumps(x, ensure_ascii=False) + ':' + json.dumps(y, ensure_ascii=False) + ',' for x, y in EN.items()) + s[k2:]

assert s[s.index('<div class="hero">'):s.index('<div class="partners">')] == hero0, '首屏 HTML 被改动'
e = s.index('<div class="cta-end rv">')
assert s[e:s.index('</section>', e)] == end0, '首页结尾 CTA 被改动'
open(P, 'w', encoding='utf8').write(s)
print('done.')
