"""首页"行业与场景"重写：只按行业分类，行业名做加粗标题 + 图标，正文一句沐仞带来的好处，底部小标签；
出海与渠道属于合作方式，拆到下面单独一行。文字都来自站上已有说法，不加新数字。
只改本地副本 index.html；首屏 HTML 与首页结尾 CTA 逐字不变。
用法：python3 -I build_home_industry_2026-10-13.py <仓库副本目录>
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

a = s.index('<div class="sec"><div class="hd"><h3 class="serif">行业与场景</h3></div>')
b = s.index('</div></div>', s.index('<div class="card"><span class="k">出海业务 · 海外客户</span>', a)) + len('</div></div>')

def ico(path):
    return f'<svg class="ind-i" viewBox="0 0 24 24" width="26" height="26" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">{path}</g></svg>'

FILM = ico('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 9h18M7 5l2 4M12 5l2 4M17 5l2 4"/>')
FLASK = ico('<path d="M9 3h6M10 3v6l-5 9a2 2 0 0 0 1.8 3h10.4a2 2 0 0 0 1.8-3l-5-9V3"/><path d="M7.5 15h9"/>')
AGENT = ico('<circle cx="12" cy="5" r="2"/><circle cx="5" cy="18" r="2"/><circle cx="19" cy="18" r="2"/><circle cx="12" cy="12" r="2.5"/><path d="M12 7v2.5M10 13.5l-3.5 3M14 13.5l3.5 3"/>')
BOOK = ico('<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z"/><path d="M4 19V5M8 7h7M8 11h5"/>')

def card(icon, title, body, tags):
    return (f'<div class="ind">{icon}<h3>{title}</h3><p>{body}</p>'
            '<span class="ind-t">' + ''.join(f'<i>{t}</i>' for t in tags) + '</span></div>')

NEW = ('<div class="sec"><div class="hd"><h3 class="serif">行业与场景</h3><span class="k">非实时 · 弱实时推理</span></div>\n'
       '      <p class="ind-lead">主要承接可延后、可批量的推理任务；越能等，越能排进绿电富余的低价时段。</p>\n'
       '      <div class="ind4">'
       + card(FILM, 'AI 短剧与内容生成', '文案、分镜批量生成，排进绿电富余的时段运行，成本更低。', ['批量', '可延后'])
       + card(FLASK, 'AI for Science', '文献抽取与科研推理按词元用量采购，不用自建算力。', ['科研机构', '高校'])
       + card(AGENT, 'AI Agent 平台', '一个接口接入多家模型，按任务挑选模型，管住推理成本。', ['多模型', '统一接口'])
       + card(BOOK, '企业知识库', '问答、检索增强与辅助开发，用真实样例测完再按量采购。', ['B 端企业'])
       + '</div>\n'
       '      <div class="ind-alt">'
       '<div><span class="k">合作方式</span><b>词元出海</b><p>出海运营主体持中央网信办词元出海业务批复，海外团队合规地用上中国模型。</p><a class="ul" href="#enterprise">企业采购与海外服务 →</a></div>'
       '<div><span class="k">合作方式</span><b>渠道与社区</b><p>个人开发者与一人公司按需调用；社区、应用平台和渠道方可以合作分发。</p><a class="ul" href="#enterprise" data-scrollto="enterprise-sales">联系销售 →</a></div>'
       '</div></div>')
s = s[:a] + NEW + s[b:]

CSS = '''
/* 首页行业与场景：行业名做加粗标题，一句好处，小标签；合作方式另起一行 */
.ind-lead{max-width:40em;margin:-4px 0 22px;font-size:16px;line-height:1.7;color:var(--ink-70)}
.ind4{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}
.ind{display:flex;flex-direction:column;background:var(--card);border:1px solid var(--line);border-radius:var(--r16);padding:22px 22px 18px;box-shadow:var(--shadow)}
.ind .ind-i{color:var(--accent);margin-bottom:18px}
.ind h3{font-family:var(--serif);font-weight:600;font-size:23px;line-height:1.25;letter-spacing:-.015em;margin:0 0 10px;color:var(--ink)}
.ind p{margin:0;font-size:14px;line-height:1.7;color:var(--ink-70)}
.ind-t{display:flex;flex-wrap:wrap;gap:6px;margin-top:auto;padding-top:16px}
.ind-t i{font-style:normal;font:400 11px var(--mono);letter-spacing:.03em;color:var(--ink-50);border:1px solid var(--line);border-radius:var(--pill);padding:3px 9px}
.ind-alt{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:14px}
.ind-alt>div{display:grid;grid-template-columns:auto 1fr;grid-template-areas:"k k" "b b" "p p" "a a";align-content:start;background:var(--paper-2);border-radius:var(--r16);padding:18px 22px}
.ind-alt .k{grid-area:k;margin-bottom:6px}
.ind-alt b{grid-area:b;font:600 17px var(--sans);color:var(--ink)}
.ind-alt p{grid-area:p;margin:4px 0 10px;font-size:14px;line-height:1.7;color:var(--ink-70)}
.ind-alt a{grid-area:a;justify-self:start;font-size:13px;color:var(--ink-70)}
@media (max-width:1100px){.ind4{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:800px){.ind4,.ind-alt{grid-template-columns:1fr}.ind h3{font-size:21px}}
'''
k = s.index('</style>')
s = s[:k] + CSS + s[k:]

EN = {"非实时 · 弱实时推理": "Non-real-time · near-real-time inference",
      "主要承接可延后、可批量的推理任务；越能等，越能排进绿电富余的低价时段。": "Built for deferrable, batchable inference: the more a job can wait, the more of it runs in low-price windows of surplus green power.",
      "AI 短剧与内容生成": "AI short drama & content",
      "文案、分镜批量生成，排进绿电富余的时段运行，成本更低。": "Scripts and storyboards generated in batches, run in surplus green-power windows at lower cost.",
      "文献抽取与科研推理按词元用量采购，不用自建算力。": "Literature extraction and research inference, bought per token, with no compute to build yourself.",
      "AI Agent 平台": "AI agent platforms",
      "一个接口接入多家模型，按任务挑选模型，管住推理成本。": "One API for many models: pick the model per task and keep inference costs in check.",
      "企业知识库": "Enterprise knowledge bases",
      "问答、检索增强与辅助开发，用真实样例测完再按量采购。": "Q&A, retrieval augmentation and coding assistance, tested on real samples before you buy by volume.",
      "批量": "Batch", "可延后": "Deferrable", "科研机构": "Research institutes", "高校": "Universities",
      "多模型": "Multi-model", "统一接口": "Unified API", "B 端企业": "Enterprises", "合作方式": "Partnership",
      "渠道与社区": "Channels & communities", "联系销售 →": "Contact sales →",
      "出海运营主体持中央网信办词元出海业务批复，海外团队合规地用上中国模型。": "Our overseas entity holds CAC approval for token export, so overseas teams can use Chinese models compliantly.",
      "个人开发者与一人公司按需调用；社区、应用平台和渠道方可以合作分发。": "Individual developers and one-person companies call on demand; communities, app platforms and channel partners can distribute with us."}
k2 = s.index('var I18N={') + len('var I18N={')
s = s[:k2] + ''.join(json.dumps(x, ensure_ascii=False) + ':' + json.dumps(y, ensure_ascii=False) + ',' for x, y in EN.items()) + s[k2:]

assert s[s.index('<div class="hero">'):s.index('<div class="partners">')] == hero0, '首屏 HTML 被改动'
e = s.index('<div class="cta-end rv">')
assert s[e:s.index('</section>', e)] == end0, '首页结尾 CTA 被改动'
open(P, 'w', encoding='utf8').write(s)
print('done.')
