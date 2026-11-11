"""产品与服务页改为"更新日志式"版式：顶部油画横幅（晨昏蓝色卡）+ 左侧吸顶圆点目录 + 每个产品一条"发布条目"
（编号标签、大标题、色卡标签、衬线导语、两列要点网格）。文字沿用现有页面，模型市场 / 节点定价的 JS 容器与 id 原样保留。
在 build_about_doc_layout_2026-10-13.py 之后运行，只改本地副本 index.html；首屏 HTML 与首页结尾 CTA 逐字不变。
用法：python3 -I build_models_release_layout_2026-10-13.py <仓库副本目录>
"""
import json, os, sys

P = os.path.join(sys.argv[1], 'index.html')
s = open(P, encoding='utf8').read()
hero0 = s[s.index('<div class="hero">'):s.index('<div class="partners">')]
end0 = s[s.index('<div class="cta-end rv">'):s.index('</section>', s.index('<div class="cta-end rv">'))]

def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: sys.exit(f'[停止] 匹配 {c} 次（应为 {n}）：{old[:70]}')
    s = s.replace(old, new)

# ---------- 2. 页面结构 ----------
def item(label, title, desc):
    return (f'<div class="pe-it"><b>{title}</b><p>{desc}</p>'
            f'<span class="pe-by"><i aria-hidden="true"></i>{label}</span></div>')

def grid(items):
    return '<div class="pe-grid">' + ''.join(item(*x) for x in items) + '</div>'

def tags(*ts):
    out = []
    for t in ts:
        kind, txt = t
        out.append(f'<span class="tg {kind}">' + ('<i aria-hidden="true"></i>' if kind != 'ln' else '') + f'{txt}</span>')
    return '<div class="pe-tags">' + ''.join(out) + '</div>'

NAV = [('总览', [('p-flow', '', '从任务接入到交付结算', False)]),
       ('产品', [('p-api', '01', '绿色词元交易平台', False), ('p-market', '', '模型市场', True), ('pricingSec', '', '节点定价', True),
                ('p-base', '02', '算电协同群智基座', False), ('p-box', '03', 'FPTM 系列词元一体机', False)]),
       ('合作', [('p-coop', '04', '能源与算力节点合作', False)])]
NAVHTML = '<nav class="pidx" aria-label="产品目录">' + ''.join(
    f'<div class="g"><span class="y">{g}</span>' + ''.join(
        f'<a href="#models" data-scrollto="{i}"' + (' class="s"' if sub else '') + '>' + (f'<em>{n}</em>' if n else '') + f'{t}</a>'
        for i, n, t, sub in items) + '</div>' for g, items in NAV) + '</nav>'

MODELS = '''<section data-route="models">
  <div class="pbanner"><div class="pb-art" aria-hidden="true"></div>
    <div class="pb-in"><span class="pb-meta">产品与服务 · 模型目录更新于 2026-10-13</span><h1 class="display">模型服务与<br>算电协同产品</h1><p>模型调用选词元交易平台；资源调度选算电基座；本地部署选 FPTM 一体机。能源与算力资产方可以合作运营节点。</p></div></div>
  <div class="wrap">
  <div class="pl">
    ''' + NAVHTML + '''
    <div class="pmain">

      <article class="pe" id="p-flow">
        <span class="pe-d">总览 · 三款产品如何协同</span>
        <h2 class="pe-t">从任务接入到交付结算</h2>
        ''' + grid([
            ('绿色词元交易平台', '接入需求', '客户确认模型、用量与交付时限，平台提供接入、报价和订单管理。'),
            ('Tapestrix · NetWeaver', '调度资源', '结合任务要求、电力预测与节点状态，安排计算资源和运行时段。'),
            ('FPTM 系列', '执行推理', '部署在场站或机房的 FPTM 一体机运行模型，提供推理算力。'),
            ('可追溯', '交付结算', '交付模型调用结果，记录用量、费用与能源信息。'),
        ]) + '''
      </article>

      <article class="pe" id="p-api">
        <span class="pe-d">01 · 模型调用与词元采购</span>
        <h2 class="pe-t">绿色词元交易平台</h2>
        ''' + tags(('acc', 'API'), ('ln', '按词元计费'), ('ln', 'OpenAI · Gemini 格式')) + '''
        <p class="pe-lead">统一接口接入主流模型，按词元用量计费。面向开发者和机构，主要承接非实时或弱实时推理。</p>
        ''' + grid([
            ('个人与开发者', '账户开通与 API 接入', '在本站获取 API Key，按接入文档配置地址、模型名称与调用参数。<a class="ul" href="#start">查看开通流程 →</a>'),
            ('企业与机构', '面向企业、科研机构与高校', '说明应用场景、模型需求和预期用量，用样例负载测试后报价采购。<a class="ul" href="#enterprise">联系销售 →</a>'),
            ('渠道商与平台方', '应用分发与渠道合作', '将模型服务用于自有应用或授权渠道分发，价格与结算按协议执行。<a class="ul" href="#enterprise">联系销售 →</a>'),
            ('海外客户', '词元出海', '出海运营主体持中央网信办词元出海业务批复，海外团队合规地用上中国模型。'),
        ]) + '''
        <div class="pe-sub"><h3>主要承接的任务</h3><span class="caps"><i>AI Agent 调用</i><i>科研模型推理</i><i>AI 内容处理</i><i>企业知识库推理</i><i>文本生成</i><i>图像生成</i><i>代码生成</i><i>开发者与 OPC 应用</i><i>园区与机构集中采购</i></span></div>
      </article>

      <article class="pe sub" id="p-market">
        <span class="pe-d">01 · 绿色词元交易平台 · 模型目录 2026-10-13</span>
        <h2 class="pe-t" id="secTitle">模型市场</h2>
        <p class="pe-lead">目录与输出参考价来自沐仞模型平台。DeepSeek 为空闲时段价格，MiniMax-M3 为 ≤512k 档。</p>
        <div class="chips" id="chips"><button class="chip on" data-f="all">全部</button><button class="chip" data-f="对话">对话</button><button class="chip" data-f="推理">推理</button></div>
        <div class="cards" id="featured"></div>
        <div class="mlist"><h3>全部模型</h3>
          <div class="row hd"><span>模型</span><span>类型</span><span>上下文</span><span>输出参考 / M</span><span class="hide-m">收录日期</span><span></span></div>
          <div id="allModels"></div></div>
      </article>

      <article class="pe sub" id="pricingSec">
        <span class="pe-d">01 · 绿色词元交易平台 · 电站节点</span>
        <h2 class="pe-t">节点定价</h2>
        <p class="pe-lead">结合节点资源、电力供给与任务要求评估成本。</p>
        <div class="two pe-price"><div class="idx" id="priceIdx"></div><div id="priceBody"></div></div>
      </article>

      <article class="pe" id="p-base">
        <span class="pe-d">02 · 算力与电力协同调度</span>
        <h2 class="pe-t">算电协同群智基座</h2>
        ''' + tags(('pk', '项目交付'), ('ln', 'Tapestrix'), ('ln', 'NetWeaver')) + '''
        <p class="pe-lead">将算力、电力、网络与存储纳入协同管理，支持资源观测、预测和任务安排。</p>
        ''' + grid([
            ('智能体一', '算力集群管理', '观测 GPU 与进程状态，管理异构资源，并结合任务负载评估能耗。'),
            ('智能体二', '电力资源管理', '结合场站数据预测发电与用电条件，为成本评估和任务安排提供依据。'),
            ('智能体三', '算电协同调度', '根据任务时限、网络状态与资源供给，选择合适节点并协调任务运行。'),
            ('项目合作', '按项目交付', '调度基座按项目交付，通过企业合作入口说明需求。<a class="ul" href="#enterprise">项目合作 →</a>'),
        ]) + '''
        <div class="pe-sub"><h3>应用场景</h3><span class="caps"><i>算力中心任务调度</i><i>GPU 集群能耗预测</i><i>AI 任务跨空间调度</i><i>光伏电站发电量预测</i><i>电价变化预测</i><i>光伏电站群智观测</i><i>算力任务跨电站调度</i><i>网络时延协同管理</i></span></div>
      </article>

      <article class="pe" id="p-box">
        <span class="pe-d">03 · 推理设备与部署</span>
        <h2 class="pe-t">FPTM 系列词元一体机</h2>
        ''' + tags(('acc', '风冷'), ('acc', '液冷'), ('ln', '可移动集装箱')) + '''
        <p class="pe-lead">面向场站、机房与既有节点的推理设备，支持异构 GPU 配置及风冷、液冷方案。</p>
        ''' + grid([
            ('风冷', '8 卡 / 16 卡风冷一体机', '5090 / RTX Pro 6000，8 卡或 16 卡，可上架标准机房。'),
            ('液冷', 'CDU 塔式液冷一体机', '无需机房恒温恒湿，适配电站环境，部署即用。'),
            ('集装箱', '可移动集装箱方案', '无需机房建设，单箱可达 300P 算力，无氟液冷。'),
            ('部署场景', '新能源场站与闲置算力', '分布式与集中式光伏电站、风电场、水电站、既有闲置算力中心和边缘算力节点。'),
            ('核心用途', '以算代储', '利用适用的富余电力运行 AI 推理任务，拓展电力消纳与价值实现方式。'),
            ('核心能力', '单机异构 GPU 混插', '同一台设备混插不同型号 GPU，统一调度、协同计算。'),
            ('采购与部署', '设备采购与本地部署', '资产方可采购设备并合作运营；企业、科研机构与高校可在机房或实验室部署。<a class="ul" href="#enterprise">联系销售 →</a>'),
        ]) + '''
      </article>

      <article class="pe" id="p-coop">
        <span class="pe-d">04 · 合作方式</span>
        <h2 class="pe-t">能源与算力节点合作</h2>
        ''' + tags(('pk', '分润'), ('ln', '新能源场站'), ('ln', '第三方算力中心')) + '''
        <p class="pe-lead">资产方投入场地、电力或设备；沐仞提供接入、调度、运营与词元销售，双方按协议分享收益。</p>
        ''' + grid([
            ('新能源场站', '资产方或投资机构出资采购一体机', '一体机部署在光伏、风电、水电等新能源场站。'),
            ('沐仞负责', '算法、接入、调度、运营、销售', '提供技术方案、节点接入、任务调度、设备运营与词元销售服务。'),
            ('收益', '词元销售分润', '按协议约定的比例和周期分配词元销售收益。'),
            ('第三方算力中心', '接入绿色词元交易平台', '既有算力中心也可以接入交易平台。<a class="ul" href="#network">电站合作页 →</a>'),
        ]) + '''
      </article>


    </div>
  </div>
  </div>
</section>'''

a = s.index('<section data-route="models">')
b = s.index('</section>', a) + len('</section>')
old = s[a:b]
for must in ('id="chips"', 'id="featured"', 'id="allModels"', 'id="priceIdx"', 'id="priceBody"', 'id="secTitle"', 'id="p-api"', 'id="pricingSec"'):
    assert must in old and must in MODELS, must
s = s[:a] + MODELS + s[b:]

CSS = '''
/* 产品与服务：更新日志式版式（油画横幅 + 左侧圆点目录 + 发布条目），配色只用本站色卡 */
.pbanner{position:relative;height:500px;overflow:hidden;background:var(--hz-3);color:#fff}
.pb-art{position:absolute;inset:0;background:
  radial-gradient(34% 52% at 80% 16%, rgba(207,217,228,.85), transparent 70%),
  radial-gradient(48% 42% at 64% 72%, rgba(233,220,216,.9), transparent 72%),
  radial-gradient(36% 40% at 92% 82%, rgba(217,192,185,.75), transparent 70%),
  radial-gradient(44% 46% at 36% 74%, rgba(122,96,113,.7), transparent 72%),
  radial-gradient(58% 78% at 6% 92%, rgba(33,32,33,.9), transparent 74%),
  linear-gradient(180deg,#5284D7 0%,#6F9CE0 24%,#9DBBE4 42%,#D9C0B9 58%,#7A6071 76%,#3D314F 90%,#212021 100%)}
.pb-art:after{content:"";position:absolute;inset:0;background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/></filter><rect width='200' height='200' filter='url(%23n)' opacity='.08'/></svg>");mix-blend-mode:overlay;opacity:.9}
.pbanner:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(33,32,33,0) 40%,rgba(33,32,33,.45) 100%);pointer-events:none}
.pb-in{position:absolute;z-index:1;left:max(20px,calc(50% - 540px));right:20px;bottom:56px}
.pb-meta{display:block;font:400 13px var(--mono);letter-spacing:.02em;color:rgba(255,255,255,.85);margin-bottom:18px}
.pb-in .display{font-size:72px;line-height:1.05;letter-spacing:-.035em;color:#fff;margin:0}
.pb-in p{max-width:36em;margin:18px 0 0;font-size:16px;line-height:1.65;color:rgba(255,255,255,.82)}
.pl{display:grid;grid-template-columns:200px minmax(0,1fr);column-gap:72px;max-width:1180px;margin:0 auto;padding:64px 0 24px;align-items:start}
.pidx{position:sticky;top:100px;display:grid;gap:2px}
.pidx .g+.g{margin-top:22px}
.pidx .y{display:block;font:500 15px var(--sans);color:var(--ink);margin-bottom:6px}
.pidx a em{font:400 11px var(--mono);font-style:normal;color:var(--ink-30);margin-right:7px}
.pidx a.s{padding-left:44px;font-size:13px}
.pidx a.s:before{left:25px;width:4px;height:4px;margin-top:-2px}
.pidx a.s.on:before{width:4px;height:12px;margin-top:-6px}
.pidx a{position:relative;display:block;padding:5px 0 5px 22px;font-size:14px;color:var(--ink-50);transition:color .2s var(--ease)}
.pidx a:before{content:"";position:absolute;left:3px;top:50%;width:6px;height:6px;margin-top:-3px;border-radius:3px;background:var(--line);transition:all .25s var(--ease)}
.pidx a:hover{color:var(--ink)}
.pidx a.on{color:var(--ink)}
.pidx a.on:before{height:16px;margin-top:-8px;background:var(--ink)}
.pe{padding:0 0 88px;scroll-margin-top:100px}
.pe.sub .pe-t{font-size:34px}
.pe.sub{padding-bottom:72px}
.pe-d{display:block;font:400 13px var(--mono);color:var(--ink-50);margin-bottom:12px}
.pe-t{font-family:var(--serif);font-weight:400;font-size:48px;line-height:1.1;letter-spacing:-.03em;margin:0;color:var(--ink);font-variation-settings:"opsz" 144}
.pe-tags{display:flex;flex-wrap:wrap;gap:8px;margin:16px 0 0}
.tg{display:inline-flex;align-items:center;gap:6px;height:26px;padding:0 11px;border-radius:var(--pill);font:500 12px var(--sans);border:1px solid var(--line);color:var(--ink)}
.tg i{width:7px;height:7px;border-radius:50%;background:currentColor}
.tg.acc{background:var(--accent-soft);border-color:transparent;color:var(--accent)}
.tg.pk{background:var(--peak-soft);border-color:transparent;color:var(--peak)}
.tg.ln{font-family:var(--mono);font-weight:400;border-color:var(--ink-30)}
.pe-lead{max-width:36em;margin:22px 0 0;font-family:var(--serif);font-size:18px;line-height:1.6;color:var(--ink)}
.pe-grid{display:grid;grid-template-columns:1fr 1fr;gap:44px 56px;margin-top:40px}
.pe-it b{display:block;font-weight:500;font-size:15px;line-height:1.5;color:var(--ink)}
.pe-it p{margin:6px 0 0;font-size:14px;line-height:1.7;color:var(--ink-50)}
.pe-it p a{margin-left:4px;color:var(--ink-70)}
.pe-by{display:flex;align-items:center;gap:8px;margin-top:14px;font-size:13px;color:var(--ink-70)}
.pe-by i{width:18px;height:18px;border-radius:50%;flex:none;background:linear-gradient(160deg,var(--hz-1) 0%,#B7A8A3 55%,var(--hz-2b) 100%)}
.pe-sub{margin-top:44px}
.pe-sub h3{font:500 15px var(--sans);margin:0 0 12px;color:var(--ink)}
.pe .chips{display:flex;gap:8px;justify-content:flex-start;margin:26px 0 22px}
.pe .chips .chip{height:28px;padding:0 13px;border-radius:var(--pill);font-size:12px;background:transparent;border:1px solid var(--ink-30);color:var(--ink-50)}
.pe .chips .chip.on{border-color:var(--ink);color:var(--ink);background:transparent}
.pe .mlist{margin-top:40px}
.pe .mlist h3{font:500 15px var(--sans);margin:0 0 10px}
.pe .two.pe-price{padding:30px 0 0;grid-template-columns:170px minmax(0,1fr)}
@media (max-width:1100px){.pl{grid-template-columns:170px minmax(0,1fr);column-gap:40px}.pe-grid{gap:36px 36px}}
@media (max-width:800px){
  .pbanner{height:420px}
  .pb-in{left:20px;right:20px;bottom:36px}
  .pb-in .display{font-size:42px}
  .pl{grid-template-columns:1fr;padding-top:40px}
  .pidx{display:none}
  .pe{padding-bottom:64px}
  .pe-t{font-size:34px}
  .pe-grid{grid-template-columns:1fr;gap:28px}
  .pe .two.pe-price{grid-template-columns:1fr}
}
'''
k = s.index('</style>')
s = s[:k] + CSS + s[k:]

SPY = '''<script id="pidx-spy">
/* 产品页左侧目录：滚动时高亮当前条目 */
(function(){var toc=document.querySelectorAll('.pidx a');if(!toc.length)return;
  function spy(){var sec=document.querySelector('section[data-route="models"]');if(!sec||!sec.classList.contains('on'))return;var cur=toc[0];
    Array.prototype.forEach.call(toc,function(a){var t=document.getElementById(a.getAttribute('data-scrollto'));if(t&&t.getBoundingClientRect().top<160)cur=a});
    if(window.innerHeight+window.scrollY>=document.documentElement.scrollHeight-4)cur=toc[toc.length-1];
    Array.prototype.forEach.call(toc,function(a){a.classList.toggle('on',a===cur)})}
  window.addEventListener('scroll',spy,{passive:true});window.addEventListener('hashchange',function(){setTimeout(spy,60)});spy();
})();
</script>
'''
rep('<script id="fp-fresh">', SPY + '<script id="fp-fresh">')

EN = {"产品目录": "Products", "产品与服务 · 模型目录更新于 2026-10-13": "Products · model catalog updated 2026-10-13",
      "模型服务与": "Model services &", "算电协同产品": "compute-power products", "总览": "Overview", "产品": "Products", "合作": "Partnership", "总览 · 三款产品如何协同": "Overview · how the three products work together", "01 · 绿色词元交易平台 · 模型目录 2026-10-13": "01 · Green token platform · catalog 2026-10-13", "01 · 绿色词元交易平台 · 电站节点": "01 · Green token platform · site nodes",
      "01 · 模型调用与词元采购": "01 · Model calls & token purchasing", "02 · 算力与电力协同调度": "02 · Compute-power scheduling",
      "03 · 推理设备与部署": "03 · Inference hardware", "04 · 合作方式": "04 · Partnership", "模型目录 · 2026-10-13": "Model catalog · 2026-10-13",
      "电站节点 · 价格": "Site nodes · pricing", "按词元计费": "Per-token billing", "OpenAI · Gemini 格式": "OpenAI · Gemini format",
      "项目交付": "Project delivery", "分润": "Revenue share", "可移动集装箱": "Mobile container", "按项目交付": "Delivered per project",
      "项目合作": "Projects", "第三方算力中心": "Third-party compute centers", "工作方式 · 接入需求 · 调度资源 · 执行推理 · 交付结算": "How it works · intake · scheduling · inference · settlement",
      "目录与输出参考价来自沐仞模型平台。DeepSeek 为空闲时段价格，MiniMax-M3 为 ≤512k 档。": "Catalog and output reference prices come from the FathomPeak model platform. DeepSeek prices are off-peak; MiniMax-M3 is the ≤512k tier.",
      "结合节点资源、电力供给与任务要求评估成本。": "Costs are assessed from node resources, power supply and job requirements."}
k2 = s.index('var I18N={') + len('var I18N={')
s = s[:k2] + ''.join(json.dumps(x, ensure_ascii=False) + ':' + json.dumps(y, ensure_ascii=False) + ',' for x, y in EN.items()) + s[k2:]

assert s[s.index('<div class="hero">'):s.index('<div class="partners">')] == hero0, '首屏 HTML 被改动'
e = s.index('<div class="cta-end rv">')
assert s[e:s.index('</section>', e)] == end0, '首页结尾 CTA 被改动'
open(P, 'w', encoding='utf8').write(s)
print('done.')
