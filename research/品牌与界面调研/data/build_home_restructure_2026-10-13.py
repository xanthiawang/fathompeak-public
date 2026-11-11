"""首页按"一节只答一个问题"重排（参照硅基流动首页：产品矩阵 → 为什么 → 行业 → 客户）。
1 首屏：不动。2 为什么做这个：不动（唯一讲"高峰撞上富余绿电"的地方）。
3 功能区 02：只讲价格怎么算，删掉重复的故事句。
4 "为什么是沐仞"五条 → "产品与合作"四张卡（交易平台 / 群智基座 / 一体机 / 节点合作），持牌出海与工信部备案并入卡片；
  删掉与前文重复的三条。
5 行业与场景：导语只留"谁已经在买"；六张卡标题改成行业专属的价值；删掉合作方式一行（出海已并入平台卡，渠道合作在企业页）。
6 常见问题：删"订单的绿电记录能用来做什么"（功能区 03 已讲）。
7 用词：营销页统一"产地卡"（随上面删除，首页不再出现"产地证 / 绿电记录"）。
只用站上已有的说法，不加新数字或承诺。首屏 HTML 与首页结尾 CTA 逐字不变。
用法：python3 -I build_home_restructure_2026-10-13.py <仓库副本目录>
"""
import json, os, re, sys

P = os.path.join(sys.argv[1], 'index.html')
s = open(P, encoding='utf8').read()
hero0 = s[s.index('<div class="hero">'):s.index('<div class="partners">')]
end0 = s[s.index('<div class="cta-end rv">'):s.index('</section>', s.index('<div class="cta-end rv">'))]

def rep(old, new, n=1):
    global s
    c = s[:s.index('var I18N={')].count(old)
    if c != n: sys.exit(f'[停止] 匹配 {c} 次（应为 {n}）：{old[:80]}')
    k = s.index('var I18N={')
    s = s[:k].replace(old, new) + s[k:]

# ---------- 3. 功能区 02 只讲计价 ----------
rep('<p>算力就在电站旁，用的是电网接不住的电，成本从电开始就低。价格按模型、调用规模、响应时延、并发需求和绿电来源计算；不赶时间的任务，调度会排到电最多的时段和电站。</p>',
    '<p>价格按模型、调用规模、响应时延、并发需求和绿电来源计算；公开价在模型市场查看，企业用量可以按量报价。</p>')

# ---------- 4. 为什么是沐仞 → 产品与合作 ----------
def glyph(path):
    return f'<svg viewBox="0 0 24 24" width="14" height="14" aria-hidden="true"><g fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{path}</g></svg>'

PRODUCTS = [
    (glyph('<path d="M4 7h16M4 12h16M4 17h10"/>'), '绿色词元交易平台', '一个端点，<br>接入主流模型',
     '兼容 OpenAI 与 Gemini 原生格式，按词元计费；出海运营主体持网信办词元出海批复，海外团队合规调用。', '模型调用与词元采购', 'data-product-target="p-api" href="#models"'),
    (glyph('<circle cx="6" cy="6" r="2"/><circle cx="18" cy="6" r="2"/><circle cx="12" cy="18" r="2"/><path d="M7.5 7.5 11 16M16.5 7.5 13 16M8 6h8"/>'), '算电协同群智基座', '把任务排到<br>绿电富余的节点',
     '算力、电力与协同调度三类智能体统一观测资源；Tapestrix 调度架构已在工信部备案。', '算力与电力协同调度', 'data-product-target="p-base" href="#models"'),
    (glyph('<rect x="5" y="4" width="14" height="16" rx="2"/><path d="M9 8h6M9 12h6M9 16h3"/>'), 'FPTM 系列词元一体机', '部署在电站旁的<br>推理设备',
     '单机异构 GPU 混插；风冷、液冷与可移动集装箱三种形态。', '推理设备与部署', 'data-product-target="p-box" href="#models"'),
    (glyph('<path d="M4 20 10 8l4 7 3-4 3 9z"/>'), '能源与节点合作', '资产方出设备，<br>沐仞来运营',
     '光伏、风电、水电场站与既有算力中心都可以接入，按协议分享词元销售收益。', '合作方式', 'href="#network"'),
]
def pcard(p):
    ic, name, title, line, cat, attrs = p
    return (f'<a class="fa" {attrs}><span class="fa-b"><span class="fa-n"><span class="fa-ic">{ic}</span>{name}</span>'
            f'<span class="fa-t">{title}</span><span class="fa-p">{line}</span>'
            f'<span class="fa-f"><span>{cat}</span><span aria-hidden="true">→</span></span></span></a>')

w0 = '<div class="sec" style="margin-top:44px"><div class="hd"><h3 class="serif">为什么是沐仞</h3>'
pre = s[:s.index('var I18N={')]
w = pre.index(w0)
w_end = pre.index('\n    <div class="sec" style="margin-top:44px"><div class="hd"><h3 class="serif">行业与场景</h3>', w)
PROD = ('<div class="sec" style="margin-top:44px"><div class="hd"><h3 class="serif">产品与合作</h3><span class="k">三类产品 · 一种合作方式</span></div>\n'
        '      <div class="fa-grid c4">' + ''.join(pcard(p) for p in PRODUCTS) + '</div></div>')
s = s[:w] + PROD + s[w_end:]

# ---------- 5. 行业与场景 ----------
rep('<p class="fa-lead">主要承接可延后、可批量的推理任务；越能等，越能排进绿电富余的低价时段。已有词元采购客户包括某 AI for Science 独角兽、某全球头部社交平台，以及某头部大厂的跨境电商图文审核。</p>',
    '<p class="fa-lead">已有词元采购客户包括某 AI for Science 独角兽、某全球头部社交平台，以及某头部大厂的跨境电商图文审核。</p>')
for old, new in [('批量生成，<br>排进绿电时段', '剧本、分镜，<br>批量出稿'),
                 ('科研推理，<br>按词元采购', '科研推理，<br>不用自建算力'),
                 ('海量对话，<br>按用量计费', '大流量对话，<br>按词元承接'),
                 ('图文审核，<br>批量交付', '海量图文，<br>按批审核'),
                 ('一个接口，<br>接入多家模型', '多步调用，<br>按任务挑模型'),
                 ('先用真实样例测，<br>再按量采购', '知识库问答，<br>按量采购')]:
    rep(f'<span class="fa-t">{old}</span>', f'<span class="fa-t">{new}</span>')
pre = s[:s.index('var I18N={')]
fx = pre.index('\n      <div class="fx-row">')
fx_end = pre.index('联系销售 →</a></div></div>', fx) + len('联系销售 →</a></div></div>')
s = s[:fx] + s[fx_end:]

# ---------- 6. 常见问题删重复项 ----------
pre = s[:s.index('var I18N={')]
q = pre.index('订单的绿电记录能用来做什么？')
qa = pre.rfind('<div class="q">', 0, q)
qb = pre.index('<div class="q">', q)
s = s[:qa] + s[qb:]

# ---------- 样式：四列网格 + 卡片说明行 ----------
CSS = '''
/* 首页产品与合作：沿用行业卡样式，四列，多一行说明 */
.fa-grid.c4{grid-template-columns:repeat(4,minmax(0,1fr))}
.fa-p{display:block;margin:-8px 0 20px;font-size:14px;line-height:1.7;color:var(--ink-70)}
@media (max-width:1100px){.fa-grid.c4{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:800px){.fa-grid.c4{grid-template-columns:1fr}}
'''
k = s.index('</style>')
s = s[:k] + CSS + s[k:]

pre = s[:s.index('var I18N={')]
for gone in ('为什么是沐仞', '产地证', '订单的绿电记录', '越能等，越能排进绿电富余的低价时段'):
    assert gone not in pre[pre.index('<section data-route="home">'):pre.index('</section>', pre.index('<section data-route="home">'))], gone

EN = {"价格按模型、调用规模、响应时延、并发需求和绿电来源计算；公开价在模型市场查看，企业用量可以按量报价。":
          "Pricing depends on the model, call volume, latency, concurrency and green-power source; public prices are in the model market, and enterprise volume can be quoted separately.",
      "产品与合作": "Products & partnerships", "三类产品 · 一种合作方式": "Three products · one partnership model",
      "一个端点，": "One endpoint,", "接入主流模型": "leading models",
      "兼容 OpenAI 与 Gemini 原生格式，按词元计费；出海运营主体持网信办词元出海批复，海外团队合规调用。": "Compatible with native OpenAI and Gemini formats, billed per token; our overseas entity holds CAC approval for token export, so overseas teams call compliantly.",
      "模型调用与词元采购": "Model calls & token purchasing", "把任务排到": "Routes jobs to", "绿电富余的节点": "nodes with surplus green power",
      "算力、电力与协同调度三类智能体统一观测资源；Tapestrix 调度架构已在工信部备案。": "Three agents for compute, power and coordination observe resources together; the Tapestrix scheduling architecture is filed with MIIT.",
      "算力与电力协同调度": "Compute–power scheduling", "部署在电站旁的": "Inference hardware", "推理设备": "beside power plants",
      "单机异构 GPU 混插；风冷、液冷与可移动集装箱三种形态。": "Mixed heterogeneous GPUs in one machine; air-cooled, liquid-cooled and mobile-container forms.",
      "推理设备与部署": "Inference hardware & deployment", "能源与节点合作": "Energy & node partnerships", "资产方出设备，": "Asset owners fund the hardware,",
      "沐仞来运营": "FathomPeak operates it", "光伏、风电、水电场站与既有算力中心都可以接入，按协议分享词元销售收益。": "Solar, wind and hydro sites and existing compute centers can connect and share token-sales revenue by agreement.",
      "合作方式": "Partnership",
      "已有词元采购客户包括某 AI for Science 独角兽、某全球头部社交平台，以及某头部大厂的跨境电商图文审核。": "Token buyers already include an AI for Science unicorn, a leading global social platform, and a major company's cross-border e-commerce image-and-text review.",
      "剧本、分镜，": "Scripts and storyboards,", "批量出稿": "drafted in batches", "不用自建算力": "no compute to build",
      "大流量对话，": "High-traffic chat,", "按词元承接": "handled per token", "海量图文，": "Images and text at scale,", "按批审核": "reviewed in batches",
      "多步调用，": "Multi-step calls,", "按任务挑模型": "the right model per task", "知识库问答，": "Knowledge-base Q&A,", "按量采购": "bought by volume"}
k2 = s.index('var I18N={') + len('var I18N={')
s = s[:k2] + ''.join(json.dumps(x, ensure_ascii=False) + ':' + json.dumps(y, ensure_ascii=False) + ',' for x, y in EN.items()) + s[k2:]

assert s[s.index('<div class="hero">'):s.index('<div class="partners">')] == hero0, '首屏 HTML 被改动'
e = s.index('<div class="cta-end rv">')
assert s[e:s.index('</section>', e)] == end0, '首页结尾 CTA 被改动'
open(P, 'w', encoding='utf8').write(s)
print('done.')
