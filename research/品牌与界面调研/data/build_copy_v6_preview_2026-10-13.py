"""v6 预览：按 Zixin 10-13 反馈收紧 v5。
- 首页"为什么做这个"：只学 Valhalla 的文字写法（大标题 + 两句 + 一句收束），视觉用本站组件；
  图表只留一张卡，对比"官方 API 高峰价"与"现货电价"两个维度。
- "几个数"不单独成块，并进关于页"公司"表格。
- 关于页故事压到三段，去掉与首页重复的"正午"段。
原型不改。用法：python3 -I build_copy_v6_preview_2026-10-13.py
"""
import json, os, sys, importlib.util

D = os.path.dirname(os.path.abspath(__file__))
def load(name, fn):
    spec = importlib.util.spec_from_file_location(name, os.path.join(D, fn)); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
v4 = load('v4', 'build_copy_v4_preview_2026-10-13.py')
v5 = load('v5', 'build_copy_v5_preview_2026-10-13.py')
OUT = os.path.join(D, '..', 'demo', '沐仞官网原型_文案v6预览_2026-10-13.html')

CSS = '''
/* v6 预览新增：只用本站 token */
.why2{max-width:760px;margin:0 auto;padding:80px 20px 10px;text-align:center}
.why2 .lead2{font-family:var(--serif);font-weight:400;font-size:clamp(30px,4vw,44px);letter-spacing:-.025em;line-height:1.15;margin:8px 0 0;color:var(--ink);font-variation-settings:"opsz" 144}
.why2 .p2{font-size:16px;line-height:1.75;color:var(--ink-70);margin:14px auto 0;max-width:36em}
.why2 .punch{font-family:var(--serif);font-size:19px;color:var(--ink);margin:14px 0 0}
.why2 .board{text-align:left;margin-top:26px;padding:16px 18px 12px}
.tl{display:grid;gap:10px}
.tl .r{display:grid;grid-template-columns:150px 1fr;gap:12px;align-items:center}
.tl .r .nm{font-size:13px;color:var(--ink)} .tl .r .nm small{display:block;font:400 10.5px var(--mono);color:var(--ink-50);letter-spacing:.04em}
.tl .bar{position:relative;height:24px;background:var(--paper);border-radius:6px}
.tl .bar span{position:absolute;top:0;bottom:0;border-radius:6px;font:400 10.5px/24px var(--mono);color:#fff;padding-left:7px;white-space:nowrap;overflow:hidden}
.tl .ax{display:grid;grid-template-columns:150px 1fr;gap:12px} .tl .tk{position:relative;height:14px;font:400 10.5px var(--mono);color:var(--ink-50)} .tl .tk i{position:absolute;font-style:normal;transform:translateX(-50%)}
.tl .cap{font:400 10.5px var(--mono);color:var(--ink-50);margin-top:4px}
.story-txt p{font-size:16px;line-height:1.75;color:var(--ink-70);max-width:44em;margin:0 0 12px}
.story-txt p.q{font-family:var(--serif);font-size:22px;line-height:1.45;color:var(--ink)}
.pv-hold{border:1px dashed var(--ink-30);border-radius:var(--r16);padding:14px 18px;font-size:14px;color:var(--ink-50)}
@media (max-width:800px){.tl .r,.tl .ax{grid-template-columns:1fr}.tl .ax>div:first-child{display:none}}
'''

HOME_WHY = '''  <div class="why2 rv">
    <span class="k">为什么做这个</span>
    <p class="lead2">大模型，缺电。</p>
    <p class="p2">风电和光伏的电，越来越多地送不出去；同一时刻，大模型在排队、在涨价。电和算，在同一个正午错开了。</p>
    <p class="p2" style="margin-top:6px">我们觉得这不该是常态。所以把算力搬到了电站旁边。</p>
    <p class="punch">它不等电来，它去电那里。</p>
    <div class="board"><div class="tl">
      <div class="r"><div class="nm">官方 API 高峰价<small>工作日 · 低谷价的 2 倍</small></div><div class="bar"><span style="left:37.5%;width:12.5%;background:var(--peak)">高峰</span><span style="left:58.33%;width:16.67%;background:var(--peak)">高峰</span></div></div>
      <div class="r"><div class="nm">现货电价<small>白天出现负电价</small></div><div class="bar"><span style="left:33.33%;width:33.33%;background:var(--accent-fill)">电价为负</span></div></div>
      <div class="ax"><div></div><div class="tk"><i style="left:0">0</i><i style="left:33.33%">8</i><i style="left:50%">12</i><i style="left:66.67%">16</i><i style="left:75%">18</i><i style="left:100%">24</i></div></div>
      <div class="cap">高峰价：DeepSeek 官方价格页，2026-08 起。负电价：山东现货市场，2025 年五一假期。两组时段来自不同来源，用于说明重叠。</div>
    </div></div>
  </div>
'''

ABOUT_BLOCKS = '''    <h2 class="h2">我们的故事</h2>
    <div class="story-txt rv">
      <p class="q">栉风沐雨，登高万仞。去难去的地方，做难做的事。</p>
      <p>英文名 FathomPeak，从谷到峰：在电的低谷生产，在算力的高峰交付。logo 是一座山，也是一枚印章，盖在每一个从电站出发的词元上。</p>
      <p>创始人路畅在清华大学读工学直博，研究的就是算电协同调度；他做过 AI 基础设施公司的 COO，也投过分布式光伏电站。团队一半的人懂电，一半的人懂算。</p>
      <p>短期，我们把电站直供的大模型 API 交到国内外企业和开发者手里；长期，让更多电站成为产地，太阳在哪里，算力就在哪里。</p>
    </div>
''' + v5.ABOUT_BLOCKS.split('    </div>\n    <h2 class="h2">价值观</h2>', 1)[1].join(['    <h2 class="h2">价值观</h2>', ''])

ABOUT_BLOCKS = ABOUT_BLOCKS.replace('      <tr><td>团队背景</td><td>清华大学、北京大学</td></tr>\n', '')
assert '团队背景' not in ABOUT_BLOCKS

COMPANY_ROWS = '投资经历</td></tr>\n      <tr><td>团队</td><td>20 余人，研发人员占 80% 以上，来自清华大学、北京大学</td></tr>\n      <tr><td>海外业务</td><td>订单金额 83% 以上来自海外客户</td></tr>\n      <tr><td>研究成果</td><td>论文、专利与软件著作权 50 余项</td></tr>'

NEW_EN = {
 "为什么做这个": "Why we do this", "大模型，缺电。": "AI is short of power.",
 "风电和光伏的电，越来越多地送不出去；同一时刻，大模型在排队、在涨价。电和算，在同一个正午错开了。": "More and more wind and solar power can't reach the grid; at the same moment, AI models queue and prices rise. Power and compute miss each other at the same noon.",
 "我们觉得这不该是常态。所以把算力搬到了电站旁边。": "We don't think it should be this way. So we moved compute to the power plant.",
 "它不等电来，它去电那里。": "It doesn't wait for power. It goes where the power is.",
 "官方 API 高峰价": "Official API peak price", "工作日 · 低谷价的 2 倍": "Weekdays · 2× off-peak", "高峰": "Peak",
 "现货电价": "Spot power price", "白天出现负电价": "Negative in daytime", "电价为负": "Negative price",
 "高峰价：DeepSeek 官方价格页，2026-08 起。负电价：山东现货市场，2025 年五一假期。两组时段来自不同来源，用于说明重叠。": "Peak price: DeepSeek pricing page, since Aug 2026. Negative price: Shandong spot market, May 2025 holiday. Different sources, shown together to illustrate the overlap.",
 "栉风沐雨，登高万仞。去难去的地方，做难做的事。": "Through wind and rain, up the high peak. Go where it's hard to go; do what's hard to do.",
 "创始人路畅在清华大学读工学直博，研究的就是算电协同调度；他做过 AI 基础设施公司的 COO，也投过分布式光伏电站。团队一半的人懂电，一半的人懂算。": "Founder Lu Chang is a direct-PhD candidate in engineering at Tsinghua University researching compute-power co-scheduling; he was COO of an AI infrastructure company and has invested in distributed solar. Half of our team knows power; half knows compute.",
 "短期，我们把电站直供的大模型 API 交到国内外企业和开发者手里；长期，让更多电站成为产地，太阳在哪里，算力就在哪里。": "Near term, we put model APIs direct from the plant into the hands of companies and developers at home and abroad. Long term, more plants become origins: wherever the sun is, the compute follows.",
 "团队": "Team", "20 余人，研发人员占 80% 以上，来自清华大学、北京大学": "20+ people, over 80% in R&D, from Tsinghua and Peking University",
 "海外业务": "Overseas business", "订单金额 83% 以上来自海外客户": "Over 83% of order value from overseas customers",
 "研究成果": "Research", "论文、专利与软件著作权 50 余项": "50+ papers, patents and software copyrights",
}

def main():
    out = open(v4.SRC, encoding='utf8').read()
    for page, where, old, new, en, note in v4.R:
        assert out.count(old) == 1, where
        out = out.replace(old, new, 1)
    for a, b in [('  <div class="feat">', HOME_WHY + '  <div class="feat">'),
                 ('    <h2 class="h2">公司</h2>', ABOUT_BLOCKS + '    <h2 class="h2">公司</h2>'),
                 ('投资经历</td></tr>', COMPANY_ROWS),
                 ('</style>', CSS + '</style>')]:
        if out.count(a) != 1: sys.exit('[停止] 锚点不唯一：' + a[:40])
        out = out.replace(a, b, 1)
    en = {}
    for page, where, old, new, e, note in v4.R:
        if e: en[v4.text_only(new)] = e
    en.update(v4.EXTRA_EN); en.update(v5.NEW_EN); en.update(NEW_EN)
    key = 'var I18N={'
    out = out.replace(key, key + ''.join(json.dumps(k, ensure_ascii=False) + ':' + json.dumps(v, ensure_ascii=False) + ',' for k, v in en.items()), 1)
    open(OUT, 'w', encoding='utf8').write(out)
    print('preview ->', OUT)

if __name__ == '__main__':
    main()
