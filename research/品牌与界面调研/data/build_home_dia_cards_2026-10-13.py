"""首页"行业与场景"按 Dia 精选应用卡重做 + 分层图按 Dia 常见问题 / 隐私页样式重做。
- 行业卡：上方油画裁切图（art/backgrounds 两幅，取右半部分）+ 一张白色小卡；下方 应用图标式色块 + 行业名，
  衬线标题写结果，底部分类 + 箭头。行业补全为 BP 9.15 列出的六类：AI 短剧与影视、AI for Science、社交与情感陪伴、
  内容与图文审核、AI Agent、企业知识库。
- 合作方式：细边框卡 + 小胶囊标签 + 大号正文（Dia 功能卡）。
- 分层图：双线上下框、黑底编号方块、衬线标题、等宽胶囊 + 色点（Dia 常见问题 / 隐私页）。
替换 build_home_industry 写入的区块与样式；首屏 HTML 与首页结尾 CTA 逐字不变。
用法：python3 -I build_home_dia_cards_2026-10-13.py <仓库副本目录>
"""
import json, os, re, sys

P = os.path.join(sys.argv[1], 'index.html')
s = open(P, encoding='utf8').read()
hero0 = s[s.index('<div class="hero">'):s.index('<div class="partners">')]
end0 = s[s.index('<div class="cta-end rv">'):s.index('</section>', s.index('<div class="cta-end rv">'))]

# ---------- 1. 换掉旧的行业区块与样式 ----------
a = s.index('<div class="sec"><div class="hd"><h3 class="serif">行业与场景</h3><span class="k">非实时 · 弱实时推理</span></div>')
b = s.index('<div class="sec" style="margin-top:44px"><div class="hd"><h3 class="serif">项目案例</h3>', a)
css_a = s.index('/* 首页行业与场景：行业名做加粗标题')
css_b = s.index('.ind h3{font-size:21px}}', css_a) + len('.ind h3{font-size:21px}}')
assert css_b < s.index('</style>') + 10 ** 6

TF = 'art/backgrounds/products-token-flow_2026-10-13.webp'
EC = 'art/backgrounds/products-energy-compute_2026-10-13.webp'

def glyph(path):
    return f'<svg viewBox="0 0 24 24" width="14" height="14" aria-hidden="true"><g fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{path}</g></svg>'

G = {
    'film': glyph('<rect x="3" y="6" width="18" height="12" rx="2"/><path d="M3 10h18"/>'),
    'flask': glyph('<path d="M10 3v6l-5 9h14l-5-9V3M9 3h6"/>'),
    'chat': glyph('<path d="M4 5h16v10H9l-5 4z"/>'),
    'eye': glyph('<path d="M2 12s4-6 10-6 10 6 10 6-4 6-10 6S2 12 2 12z"/><circle cx="12" cy="12" r="2.5"/>'),
    'nodes': glyph('<circle cx="6" cy="6" r="2"/><circle cx="18" cy="6" r="2"/><circle cx="12" cy="18" r="2"/><path d="M7.5 7.5 11 16M16.5 7.5 13 16"/>'),
    'book': glyph('<path d="M5 4h11a3 3 0 0 1 3 3v13H8a3 3 0 0 1-3-3z"/><path d="M5 17a3 3 0 0 1 3-3h11"/>'),
}

CARDS = [  # 图标, 行业名, 结果标题, 分类, 链接, 背景图, 背景位置, 小卡眉标, 小卡标题
    ('film', 'AI 短剧与影视生成', '批量生成，<br>排进绿电时段', '内容生成', '#guide-dev-peak', TF, '62% 40%', '批量任务', '分镜与文案生成'),
    ('flask', 'AI for Science', '科研推理，<br>按词元采购', '科研机构 · 高校', '#enterprise', EC, '70% 30%', '科研任务', '文献抽取与信息整理'),
    ('chat', '社交与情感陪伴', '海量对话，<br>按用量计费', '社交平台', '#models', TF, '92% 60%', '对话调用', '陪伴类应用'),
    ('eye', '内容与图文审核', '图文审核，<br>批量交付', '跨境电商 · 平台审核', '#enterprise', EC, '96% 70%', '审核任务', '商品图文审核'),
    ('nodes', 'AI Agent 平台', '一个接口，<br>接入多家模型', '智能体', '#models', EC, '58% 55%', '统一接口', 'DeepSeek · Qwen · GLM'),
    ('book', '企业知识库', '先用真实样例测，<br>再按量采购', 'B 端企业', '#enterprise', TF, '78% 25%', '知识库问答', '检索增强与辅助开发'),
]

def card(c):
    ic, name, title, cat, href, img, pos, k, t = c
    return (f'<a class="fa" href="{href}">'
            f'<span class="fa-art" style="background-image:url(\'{img}\');background-position:{pos}" aria-hidden="true">'
            f'<span class="fa-doc"><span class="k">{k}</span><b>{t}</b><i></i><i></i><i class="s"></i></span></span>'
            f'<span class="fa-b"><span class="fa-n"><span class="fa-ic">{G[ic]}</span>{name}</span>'
            f'<span class="fa-t">{title}</span>'
            f'<span class="fa-f"><span>{cat}</span><span aria-hidden="true">→</span></span></span></a>')

INDUSTRY = ('<div class="sec"><div class="hd"><h3 class="serif">行业与场景</h3><span class="k">非实时 · 弱实时推理</span></div>\n'
            '      <p class="fa-lead">主要承接可延后、可批量的推理任务；越能等，越能排进绿电富余的低价时段。已有词元采购客户包括某 AI for Science 独角兽、某全球头部社交平台，以及某头部大厂的跨境电商图文审核。</p>\n'
            '      <div class="fa-grid">' + ''.join(card(c) for c in CARDS) + '</div>\n'
            '      <div class="fx-row">'
            '<div class="fx"><span class="fx-pill">词元出海</span><p>出海运营主体持中央网信办词元出海业务批复，海外团队合规地用上中国模型。</p><a class="ul" href="#enterprise">企业采购与海外服务 →</a></div>'
            '<div class="fx"><span class="fx-pill">渠道与社区</span><p>个人开发者与一人公司按需调用；社区、应用平台和渠道方可以合作分发。</p><a class="ul" href="#enterprise" data-scrollto="enterprise-sales">联系销售 →</a></div>'
            '</div></div>\n    ')

def row(n, layer, title, desc, chips, dot, target=None):
    head = (f'<span class="fq-n">{n}</span><span class="fq-m"><span class="fq-t"><em>{layer}</em>{title}</span>'
            + (f'<span class="fq-d">{desc}</span>' if desc else '') + '</span>'
            '<span class="fq-c">' + ''.join(f'<i><b style="background:{dot}"></b>{c}</i>' for c in chips) + '</span>')
    if target:
        return f'<a class="fq" href="#models" data-product-target="{target}">{head}<span class="fq-go" aria-hidden="true">→</span></a>'
    return f'<div class="fq">{head}<span class="fq-go"></span></div>'

STACK = ('<div class="sec fq-sec"><div class="fq-rule"></div>'
         '<h3 class="fq-h">一张图看懂沐仞</h3>'
         '<p class="fq-lead">上层是你调用的接口，下层是电站旁运行模型的一体机；中间由调度基座把任务排到绿电富余的节点。</p>'
         '<div class="fq-list">'
         + row('01', '场景', '你的业务', '', ['AI 短剧与影视', 'AI for Science', '社交与陪伴', '内容审核', 'AI Agent', '企业知识库'], '#9DBBE4')
         + row('02', '接口', '绿色词元交易平台', '一个端点接入主流模型，兼容 OpenAI 与 Gemini 原生格式，按词元计费。', ['统一 API', '按词元计费', '订单能源记录'], '#5284D7', 'p-api')
         + row('03', '模型', '主流大模型', '', ['DeepSeek', 'Qwen', 'GLM', 'MiniMax'], '#B7A8A3', 'p-market')
         + row('04', '调度', '算电协同群智基座', '结合任务时限、电力预测与节点状态，把任务排到绿电富余的节点运行。', ['Tapestrix', 'NetWeaver'], '#7A6071', 'p-base')
         + row('05', '算力与能源', 'FPTM 词元一体机 · 新能源电站', '一体机部署在光伏、风电、水电场站旁，用富余绿电生产词元。', ['光伏', '风电', '水电', '既有算力中心'], '#212021', 'p-box')
         + '</div><div class="fq-rule b"></div></div>\n    ')

s = s[:a] + INDUSTRY + STACK + s[b:]
css_a = s.index('/* 首页行业与场景：行业名做加粗标题')
css_b = s.index('.ind h3{font-size:21px}}', css_a) + len('.ind h3{font-size:21px}}')
CSS = '''/* 首页行业与场景（Dia 精选应用卡）：油画裁切 + 白色小卡；应用图标式色块 + 行业名；衬线结果标题；分类 + 箭头 */
.fa-lead{max-width:46em;margin:-4px 0 26px;font-size:16px;line-height:1.75;color:var(--ink-70)}
.fa-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}
.fa{display:flex;flex-direction:column;border:1px solid var(--line);border-radius:var(--r16);background:var(--paper);overflow:hidden;color:var(--ink);text-decoration:none;transition:transform .3s var(--ease-out),box-shadow .3s var(--ease)}
.fa:hover{transform:translateY(-3px);box-shadow:0 18px 40px -24px rgba(33,32,33,.35)}
.fa-art{position:relative;display:block;aspect-ratio:16/9;background-color:var(--hz-3);background-size:330% auto;background-repeat:no-repeat}
.fa-doc{position:absolute;left:14%;right:14%;top:22%;bottom:-8px;background:rgba(255,255,255,.94);border-radius:8px 8px 0 0;box-shadow:0 12px 30px rgba(0,0,0,.18);padding:14px 16px;display:flex;flex-direction:column;gap:7px}
.fa-doc .k{font:400 10px var(--mono);letter-spacing:.06em;color:var(--ink-50)}
.fa-doc b{font-family:var(--serif);font-weight:400;font-size:16px;line-height:1.25;color:var(--ink)}
.fa-doc i{display:block;height:5px;border-radius:3px;background:var(--line)}
.fa-doc i.s{width:58%}
.fa-b{display:flex;flex-direction:column;flex:1;padding:18px 20px 16px}
.fa-n{display:flex;align-items:center;gap:9px;font:500 14px var(--sans);color:var(--ink-85)}
.fa-ic{display:grid;place-items:center;width:22px;height:22px;border-radius:6px;background:linear-gradient(160deg,#5284D7 0%,#B7A8A3 60%,#3D314F 100%)}
.fa-t{display:block;margin:12px 0 22px;font-family:var(--serif);font-weight:400;font-size:27px;line-height:1.2;letter-spacing:-.02em;color:var(--ink)}
.fa-f{display:flex;justify-content:space-between;align-items:center;margin-top:auto;font-size:14px;color:var(--ink-50)}
.fx-row{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:20px}
.fx{border:1px solid var(--line);border-radius:var(--r16);background:var(--paper);padding:22px 24px}
.fx-pill{display:inline-block;padding:5px 12px;border-radius:var(--pill);background:var(--card);font:500 12px var(--sans);letter-spacing:.06em;color:var(--ink-70)}
.fx p{margin:14px 0 14px;font-size:18px;line-height:1.6;color:var(--ink-70)}
.fx a{font-size:14px;color:var(--ink-70)}
/* 分层图（Dia 常见问题 / 隐私页）：双线框、黑底编号、衬线标题、等宽胶囊 + 色点 */
.fq-sec{margin-top:72px}
.fq-rule{height:7px;border-top:4px solid var(--ink);border-bottom:1px solid var(--ink)}
.fq-rule.b{border-top-width:1px;border-bottom-width:4px;margin-top:8px}
.fq-h{text-align:center;font-family:var(--serif);font-weight:400;font-size:36px;letter-spacing:-.02em;margin:44px 0 10px}
.fq-lead{max-width:40em;margin:0 auto 26px;text-align:center;font-size:16px;line-height:1.7;color:var(--ink-70)}
.fq-list{display:grid}
.fq{display:grid;grid-template-columns:44px minmax(0,1fr) auto 24px;align-items:center;gap:18px;padding:20px 4px;border-top:1px solid var(--line);color:var(--ink);text-decoration:none}
.fq:first-child{border-top:0}
a.fq:hover .fq-t{text-decoration:underline;text-underline-offset:5px;text-decoration-thickness:1px}
.fq-n{display:inline-grid;place-items:center;width:30px;height:28px;background:var(--ink);color:var(--paper);font-family:var(--serif);font-size:17px}
.fq-t{display:block;font-family:var(--serif);font-weight:400;font-size:24px;line-height:1.3;letter-spacing:-.01em}
.fq-t em{font-style:normal;font:400 12px var(--mono);letter-spacing:.06em;color:var(--ink-50);margin-right:12px;vertical-align:.3em}
.fq-d{display:block;margin-top:4px;font-size:14px;line-height:1.6;color:var(--ink-50)}
.fq-c{display:flex;flex-wrap:wrap;justify-content:flex-end;gap:8px;max-width:520px}
.fq-c i{display:inline-flex;align-items:center;gap:8px;padding:6px 12px;border-radius:var(--pill);background:var(--line-2);font:400 12px var(--mono);font-style:normal;letter-spacing:.02em;color:var(--ink);white-space:nowrap}
.fq-c i b{width:8px;height:8px;border-radius:50%;display:inline-block}
.fq-go{font-size:16px;color:var(--ink-50);text-align:right}
@media (max-width:1100px){.fa-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.fq{grid-template-columns:44px minmax(0,1fr) 20px}.fq-c{grid-column:2/3;justify-content:flex-start;max-width:none}.fq-go{grid-row:1;grid-column:3}}
@media (max-width:800px){.fa-grid,.fx-row{grid-template-columns:1fr}.fa-t{font-size:24px}.fq-h{font-size:28px}.fq{grid-template-columns:38px minmax(0,1fr) 16px;gap:12px}.fq-t{font-size:20px}}'''
s = s[:css_a] + CSS + s[css_b:]

EN = {"主要承接可延后、可批量的推理任务；越能等，越能排进绿电富余的低价时段。已有词元采购客户包括某 AI for Science 独角兽、某全球头部社交平台，以及某头部大厂的跨境电商图文审核。":
          "Built for deferrable, batchable inference: the more a job can wait, the more of it runs in low-price windows of surplus green power. Token buyers already include an AI for Science unicorn, a leading global social platform, and a major company's cross-border e-commerce image-and-text review.",
      "AI 短剧与影视生成": "AI short drama & video", "内容生成": "Content generation", "批量任务": "Batch job", "分镜与文案生成": "Storyboards & scripts",
      "科研任务": "Research job", "文献抽取与信息整理": "Literature extraction", "科研机构 · 高校": "Research institutes · universities",
      "社交与情感陪伴": "Social & companionship", "社交平台": "Social platforms", "对话调用": "Chat calls", "陪伴类应用": "Companion apps",
      "内容与图文审核": "Content & image review", "跨境电商 · 平台审核": "Cross-border e-commerce · moderation", "审核任务": "Review job", "商品图文审核": "Product image & text review",
      "智能体": "Agents", "统一接口": "Unified API", "知识库问答": "Knowledge Q&A", "检索增强与辅助开发": "Retrieval & coding assistance",
      "词元出海": "Token export", "渠道与社区": "Channels & communities",
      "场景": "Use cases", "接口": "API", "模型": "Models", "调度": "Scheduling", "算力与能源": "Compute & energy",
      "AI 短剧与影视": "AI short drama", "社交与陪伴": "Social & companionship", "内容审核": "Content review", "AI Agent": "AI agents"}
# 换行标题：文本节点分开翻译
EN.update({"批量生成，": "Batch generation,", "排进绿电时段": "in green-power windows", "科研推理，": "Research inference,", "按词元采购": "bought per token",
           "海量对话，": "High-volume chat,", "按用量计费": "billed by usage", "图文审核，": "Image & text review,", "批量交付": "delivered in batches",
           "一个接口，": "One API,", "接入多家模型": "many models", "先用真实样例测，": "Test on real samples,", "再按量采购": "then buy by volume"})
k2 = s.index('var I18N={') + len('var I18N={')
s = s[:k2] + ''.join(json.dumps(x, ensure_ascii=False) + ':' + json.dumps(y, ensure_ascii=False) + ',' for x, y in EN.items()) + s[k2:]

assert s[s.index('<div class="hero">'):s.index('<div class="partners">')] == hero0, '首屏 HTML 被改动'
e = s.index('<div class="cta-end rv">')
assert s[e:s.index('</section>', e)] == end0, '首页结尾 CTA 被改动'
open(P, 'w', encoding='utf8').write(s)
print('done.')
