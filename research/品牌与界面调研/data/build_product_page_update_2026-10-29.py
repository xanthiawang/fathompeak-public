"""产品与服务页（#models）跟上 10-29 的改动：算电世界模型、私有化部署归电站页、电站四种合作方式、去掉「样例」。
总览保留，但把四步各自对应的产品写出来，否则「三款产品如何协同」看不出来。
必须在 build_plant_partnership_2026-10-29.py 之后跑（04 那一栏的标题由它改名）；04 的四种合作方式直接复用电站页的中文句子，英文跟着电站页字典走。
用法：python3 -I build_product_page_update_2026-10-29.py <站点根目录>
"""
import json, sys
from pathlib import Path

p = Path(sys.argv[1]) / 'index.html'
s = p.read_text(encoding='utf8')
if 'product-page-20261029' in s: sys.exit('[停止] 已经改过')
if 'id="coopModes"' not in s: sys.exit('[停止] 先跑电站页脚本')


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: sys.exit(f'[停止] 匹配 {c} 次（应为 {n}）：{old[:90]}')
    s = s.replace(old, new)


# 首屏
rep('<p>模型调用选 Token 交易平台；资源调度选算电基座；本地部署选 FPTM 一体机。能源与算力资产方可以合作运营节点。</p>',
    '<p>模型调用选 Token 交易平台；资源调度选算电基座；本地部署选 FPTM 一体机。电站与能源企业看解决方案。</p>')

# 总览：每一步标出由哪款产品负责
rep('<span class="flow-eyebrow">01 / API REQUEST</span>', '<span class="flow-eyebrow">01 · 绿色 Token 交易平台</span>')
rep('<span class="flow-eyebrow">02 / TASK ROUTING</span>', '<span class="flow-eyebrow">02 · 算电协同群智基座</span>')
rep('<span class="flow-eyebrow">03 / STATION INFERENCE</span>', '<span class="flow-eyebrow">03 · FPTM 一体机</span>')
rep('<span class="flow-eyebrow">04 / RESULT DELIVERY</span>', '<span class="flow-eyebrow">04 · 绿色 Token 交易平台</span>')
rep('<p>结合任务时限、电力预测、节点与网络状态，安排运行位置和时段。</p>',
    '<p>算电世界模型先推演，再结合任务时限与网络状态，安排运行位置和时段。</p>')
rep('<p>推理结果经平台交付客户，并关联本次任务的用量与费用。</p>',
    '<p>推理结果经平台交付客户，附产地卡记录电站、时段与用电量。</p>')
rep('<dt>关联</dt><dd>实际提供的能源信息</dd>', '<dt>产地卡</dt><dd>电站、时段、用电量</dd>')
rep('<p data-flow-caption="1" hidden>结合任务要求、电力预测、节点与网络状态，安排运行节点和时段，将任务送往电站侧一体机。</p>',
    '<p data-flow-caption="1" hidden>算电世界模型先推演，再安排运行节点和时段，将任务送往电站侧一体机。</p>')
rep('<p data-flow-caption="3" hidden>推理结果返回平台并交付客户，同时记录用量、费用与能源信息。</p>',
    '<p data-flow-caption="3" hidden>推理结果返回平台并交付客户，同时记录用量、费用与产地卡。</p>')

# 01：去掉「样例」
rep('<p>说明应用场景、模型需求和预期用量，用样例负载测试后报价采购。<a class="ul" href="#enterprise">联系销售 →</a></p>',
    '<p>说明应用场景、模型需求和预期用量，用你的任务测试后报价采购。<a class="ul" href="#enterprise">联系销售 →</a></p>')

# 02：底座是算电世界模型；私有化部署归电站页
rep('<span class="tg pk"><i aria-hidden="true"></i>项目交付</span><span class="tg ln">Tapestrix</span><span class="tg ln">NetWeaver</span>',
    '<span class="tg pk"><i aria-hidden="true"></i>私有化部署</span><span class="tg ln">算电世界模型</span><span class="tg ln">Tapestrix</span><span class="tg ln">NetWeaver</span>')
rep('<p class="pe-lead">将算力、电力、网络与存储纳入协同管理，支持资源观测、预测和任务安排。</p>',
    '<p class="pe-lead">三个智能体共用一个算电世界模型：把电、算力、网络和订单耦合在一起提前预测，每次调度先在模型里跑一遍。</p>')
rep('<b>按项目交付</b><p>调度基座按项目交付，通过企业订购入口说明需求。<a class="ul" href="#enterprise">项目合作 →</a></p><span class="pe-by"><i aria-hidden="true"></i>项目合作</span>',
    '<b>部署到电站与能源企业</b><p>算电世界模型与调度系统私有化部署到你的场站，按项目交付。<a class="ul" href="#network">电站解决方案 →</a></p><span class="pe-by"><i aria-hidden="true"></i>私有化部署</span>')

# 04：四种合作方式，与电站页一致
a = s.index('<article class="pe" id="p-coop">'); b = s.index('</article>', a)
art = s[a:b]
new_art = '''<article class="pe" id="p-coop">
        <span class="pe-d">04 · 解决方案</span>
        <h2 class="pe-t">电站与算力节点解决方案</h2>
        <div class="pe-tags"><span class="tg pk"><i aria-hidden="true"></i>四种合作方式</span><span class="tg ln">新能源场站</span><span class="tg ln">第三方算力中心</span><span class="tg ln">能源企业</span></div>
        <p class="pe-lead">一体机在电站是后厂，Token 交易平台是前店。按你手里的资源选合作方式。<a class="ul" href="#network">电站解决方案 →</a></p>
        <div class="pe-grid"><div class="pe-it"><b>你投场地电力和设备</b><p>你提供场地、电力并购买一体机。沐仞负责技术、调度、运营与销售，按合同分收益。</p><span class="pe-by"><i aria-hidden="true"></i>联合运营</span></div><div class="pe-it"><b>你供场地和电</b><p>设备由沐仞或资产方投入。你提供场地和电力，收取电费与场地费，或参与分成。</p><span class="pe-by"><i aria-hidden="true"></i>供电合作</span></div><div class="pe-it"><b>现有算力接单卖 Token</b><p>已有 GPU 算力中心可接入平台。按交易分润或服务价差获得收入。</p><span class="pe-by"><i aria-hidden="true"></i>算力接入</span></div><div class="pe-it"><b>私有化部署整套系统</b><p>算电世界模型、调度系统和一体机部署到你的场站，你自己接单运营。沐仞负责部署、模型适配与远程支持。</p><span class="pe-by"><i aria-hidden="true"></i>自主运营</span></div></div>
      '''
s = s[:a] + new_art + s[b:]

EN = {
    '模型调用选 Token 交易平台；资源调度选算电基座；本地部署选 FPTM 一体机。电站与能源企业看解决方案。': 'Model calls: the Token Trading Platform. Scheduling: the power–compute platform. On-premises: FPTM appliances. Power plants and energy companies: see Solutions.',
    '01 · 绿色 Token 交易平台': '01 · Green Token Trading Platform', '02 · 算电协同群智基座': '02 · Power–compute collective platform',
    '03 · FPTM 一体机': '03 · FPTM appliance', '04 · 绿色 Token 交易平台': '04 · Green Token Trading Platform',
    '算电世界模型先推演，再结合任务时限与网络状态，安排运行位置和时段。': 'The power–compute world model runs it first, then picks the site and time window around deadlines and network state.',
    '推理结果经平台交付客户，附产地卡记录电站、时段与用电量。': 'Results go to the customer through the platform, with an origin card for station, window and power used.',
    '产地卡': 'Origin card', '电站、时段、用电量': 'Station, window, power used',
    '算电世界模型先推演，再安排运行节点和时段，将任务送往电站侧一体机。': 'The world model runs the task first, then assigns node and window and sends it to the plant-side appliance.',
    '推理结果返回平台并交付客户，同时记录用量、费用与产地卡。': 'Results return through the platform to the customer, with usage, cost and origin card recorded.',
    '说明应用场景、模型需求和预期用量，用你的任务测试后报价采购。': 'Tell us the use case, models and expected volume; we test with your tasks, then quote.',
    '私有化部署': 'Private deployment', '算电世界模型': 'Power–compute world model',
    '三个智能体共用一个算电世界模型：把电、算力、网络和订单耦合在一起提前预测，每次调度先在模型里跑一遍。': 'Three agents share one power–compute world model that couples power, compute, network and orders to predict ahead; every dispatch runs in the model first.',
    '部署到电站与能源企业': 'Deployed for plants and energy companies', '算电世界模型与调度系统私有化部署到你的场站，按项目交付。': 'The world model and scheduler are deployed privately at your site, delivered as a project.',
    '电站解决方案 →': 'Power plant solutions →', '四种合作方式': 'Four ways to partner', '能源企业': 'Energy companies',
    '一体机在电站是后厂，Token 交易平台是前店。按你手里的资源选合作方式。': 'Appliances at the plant are the factory; the Token trading platform is the storefront. Pick the model that fits your resources.',
    '联合运营': 'Joint operation', '供电合作': 'Power supply', '算力接入': 'Compute access',
}
rep('  syncAuthLocale(); applyLang();', '  (function(S){for(var k in S) I18N[k]=S[k]})(' + json.dumps(EN, ensure_ascii=False) + ');  /* product-page-20261029 */\n  syncAuthLocale(); applyLang();')
p.write_text(s, encoding='utf8')
print('done')
