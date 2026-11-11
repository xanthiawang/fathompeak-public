"""首页"产品与合作"四卡 + "行业与场景"六卡 → 合成一个紧凑的分层列表（Dia 常见问题样式：双线、黑底编号、衬线标题、等宽胶囊），
标题"行业与场景"。第 01 行（场景）放六个行业，每个一句价值 + 已有采购客户；02–05 行是交易平台、模型、调度基座、一体机与节点合作。
在 build_home_restructure 之后运行；首屏与结尾 CTA 不变。
用法：python3 -I build_home_fq_industry_2026-10-13.py <仓库副本目录>
"""
import json, os, sys

P = os.path.join(sys.argv[1], 'index.html')
s = open(P, encoding='utf8').read()
hero0 = s[s.index('<div class="hero">'):s.index('<div class="partners">')]
end0 = s[s.index('<div class="cta-end rv">'):s.index('</section>', s.index('<div class="cta-end rv">'))]

pre = s[:s.index('var I18N={')]
a = pre.index('<div class="sec" style="margin-top:44px"><div class="hd"><h3 class="serif">产品与合作</h3>')
b = pre.index('<div class="sec" style="margin-top:44px"><div class="hd"><h3 class="serif">项目案例</h3>')

IND = [('AI 短剧与影视', '剧本、分镜批量出稿'), ('AI for Science', '科研推理，不用自建算力'), ('社交与情感陪伴', '大流量对话，按词元承接'),
       ('内容与图文审核', '海量图文，按批审核'), ('AI Agent 平台', '多步调用，按任务挑模型'), ('企业知识库', '知识库问答，按量采购')]

def row(n, layer, title, desc, chips, dot, target=None, href='#models'):
    head = (f'<span class="fq-n">{n}</span><span class="fq-m"><span class="fq-t"><em>{layer}</em>{title}</span>'
            + (f'<span class="fq-d">{desc}</span>' if desc else '') + '</span>'
            '<span class="fq-c">' + ''.join(f'<i><b style="background:{dot}"></b>{c}</i>' for c in chips) + '</span>')
    attr = f' data-product-target="{target}"' if target else ''
    return f'<a class="fq" href="{href}"{attr}>{head}<span class="fq-go" aria-hidden="true">→</span></a>'

ROW1 = ('<div class="fq fq-wide"><span class="fq-n">01</span><span class="fq-m"><span class="fq-t"><em>场景</em>你的业务</span>'
        '<span class="fq-d">已有词元采购客户包括某 AI for Science 独角兽、某全球头部社交平台，以及某头部大厂的跨境电商图文审核。</span>'
        '<span class="fq-ind">' + ''.join(f'<span class="fqi"><b><i></i>{n}</b><span>{v}</span></span>' for n, v in IND) + '</span></span></div>')

SEC = ('<div class="sec fq-sec"><div class="fq-rule"></div>'
       '<h3 class="fq-h">行业与场景</h3>'
       '<p class="fq-lead">从你的业务到电站旁的一体机：上层是你调用的接口，下层是运行模型的算力；中间由调度基座把任务排到绿电富余的节点。</p>'
       '<div class="fq-list">' + ROW1
       + row('02', '接口', '绿色词元交易平台', '一个端点接入主流模型，兼容 OpenAI 与 Gemini 原生格式，按词元计费；出海运营主体持网信办词元出海批复。', ['统一 API', '按词元计费', '产地卡'], '#5284D7', 'p-api')
       + row('03', '模型', '主流大模型', '', ['DeepSeek', 'Qwen', 'GLM', 'MiniMax'], '#B7A8A3', 'p-market')
       + row('04', '调度', '算电协同群智基座', '结合任务时限、电力预测与节点状态，把任务排到绿电富余的节点运行；Tapestrix 调度架构已在工信部备案。', ['Tapestrix', 'NetWeaver'], '#7A6071', 'p-base')
       + row('05', '算力与能源', 'FPTM 词元一体机 · 新能源电站', '一体机部署在光伏、风电、水电场站旁；资产方出设备，沐仞负责接入、调度与运营，按协议分享收益。', ['光伏', '风电', '水电', '既有算力中心'], '#212021', 'p-box')
       + '</div><div class="fq-rule b"></div></div>\n    ')
s = s[:a] + SEC + s[b:]

CSS = '''
/* 首页行业与场景（分层列表）：第 01 行放六个行业，三列小网格 */
.fq.fq-wide{align-items:start}
.fq.fq-wide .fq-m{grid-column:2/5}
.fq.fq-wide .fq-n{margin-top:2px}
.fq-ind{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px 32px;margin-top:18px}
.fqi b{display:flex;align-items:center;gap:8px;font:500 15px var(--sans);color:var(--ink)}
.fqi b i{width:8px;height:8px;border-radius:50%;background:#9DBBE4;flex:none}
.fqi>span{display:block;margin:3px 0 0 16px;font-size:13px;line-height:1.6;color:var(--ink-50)}
@media (max-width:1100px){.fq.fq-wide .fq-m{grid-column:2/4}.fq-ind{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:800px){.fq.fq-wide .fq-m{grid-column:2/4}.fq-ind{grid-template-columns:repeat(2,minmax(0,1fr));gap:12px 16px}}
'''
k = s.index('</style>')
s = s[:k] + CSS + s[k:]

EN = {"从你的业务到电站旁的一体机：上层是你调用的接口，下层是运行模型的算力；中间由调度基座把任务排到绿电富余的节点。":
          "From your business to the appliances beside power plants: on top is the API you call, below is the compute running the models, and in between the scheduling base routes jobs to nodes with surplus green power.",
      "你的业务": "Your business", "剧本、分镜批量出稿": "Scripts and storyboards drafted in batches", "科研推理，不用自建算力": "Research inference, no compute to build",
      "大流量对话，按词元承接": "High-traffic chat, handled per token", "海量图文，按批审核": "Images and text reviewed in batches",
      "多步调用，按任务挑模型": "Multi-step calls, the right model per task", "知识库问答，按量采购": "Knowledge-base Q&A, bought by volume",
      "一个端点接入主流模型，兼容 OpenAI 与 Gemini 原生格式，按词元计费；出海运营主体持网信办词元出海批复。": "One endpoint for leading models, compatible with native OpenAI and Gemini formats, billed per token; our overseas entity holds CAC approval for token export.",
      "产地卡": "Origin card",
      "结合任务时限、电力预测与节点状态，把任务排到绿电富余的节点运行；Tapestrix 调度架构已在工信部备案。": "Uses job deadlines, power forecasts and node status to run jobs on nodes with surplus green power; the Tapestrix scheduling architecture is filed with MIIT.",
      "一体机部署在光伏、风电、水电场站旁；资产方出设备，沐仞负责接入、调度与运营，按协议分享收益。": "Appliances sit beside solar, wind and hydro plants; asset owners fund the hardware, FathomPeak handles onboarding, scheduling and operations, and revenue is shared by agreement.",
      "AI 短剧与影视": "AI short drama & video", "AI Agent 平台": "AI agent platforms"}
k2 = s.index('var I18N={') + len('var I18N={')
s = s[:k2] + ''.join(json.dumps(x, ensure_ascii=False) + ':' + json.dumps(y, ensure_ascii=False) + ',' for x, y in EN.items()) + s[k2:]

assert s[s.index('<div class="hero">'):s.index('<div class="partners">')] == hero0, '首屏 HTML 被改动'
e = s.index('<div class="cta-end rv">')
assert s[e:s.index('</section>', e)] == end0, '首页结尾 CTA 被改动'
open(P, 'w', encoding='utf8').write(s)
print('done.')
