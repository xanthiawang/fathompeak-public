"""电站合作页改成解决方案页（Zixin 2026-10-29）。
骨架照无问芯穹解决方案页：核心痛点 → 解决方案 → 核心优势 → 行业价值 → 合作怎么走 → 咨询。
文案由 Codex（gpt-6-astra）按任务书重写（`交互原型/行业解决方案_2026-10-29/Codex文案_电站解决方案_2026-10-29.md`），
我只改两处：核心优势「生产销售相衔接」→「订单有来源」，「设备运营有人管」（与联合运营卡重复）→「从设备到销售，沐仞负责」。
Zixin 定：分成比例、规模门槛、合同期不写；保留原来的交易看板 / 电站节点卡 / 节点评价（「保存一点之前的展示」）；
不放分工表（与合作方式重复）；用站内已有组件（cards3 / steps 卡），不用表格。
顺带：产品页侧栏「合作 › 04 能源与算力节点合作」→「解决方案 › 04 电站与算力节点」。
用法：python3 -I build_plant_partnership_2026-10-29.py <站点根目录>
"""
import json, sys
from pathlib import Path

p = Path(sys.argv[1]) / 'index.html'
s = p.read_text(encoding='utf8')
if 'id="coopModes"' in s: sys.exit('[停止] 已经改过')


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: sys.exit(f'[停止] 匹配 {c} 次（应为 {n}）：{old[:90]}')
    s = s.replace(old, new)


# 首屏
rep('<div class="page-head"><h1 class="display">搬电很贵，搬比特很便宜</h1><p>所以我们把算力搬到电站旁边，把电网接不住的电就地变成 Token。下面是电站节点与交易看板（示例数据）。</p></div>',
    '<div class="page-head"><h1 class="display">你的电站，可以是一个 Token 产地</h1><p>富余绿电就地运行 AI 模型，Token 卖给 AI 客户。</p></div>')

# 节点评价整块删掉；看板和节点卡上的「示例数据」「展示」标签去掉（Zixin 10-29：模板性文字不许进 UI）
rep('<div class="sec"><div class="hd"><h3 class="serif">节点评价</h3><span class="k">节点评价 · 示例</span></div><div class="revs" id="reviews"></div></div>',
    '<div class="revs" id="reviews" hidden></div>')
rep('<span class="live"><i></i>示例数据 · ¥ / 百万 Token</span>', '<span class="live"><i></i>¥ / 百万 Token</span>')
rep('<span class="live"><i></i>展示</span>', '')   # 节点卡上的「展示」标签（JS 模板里）
rep('<span class="live"><b></b>示例数据</span>', '')   # 首页首屏看板的「示例数据」标签

# 产品页侧栏与页脚
rep('<div class="g"><span class="y">合作</span><a href="#models" data-scrollto="p-coop"><em>04</em>能源与算力节点合作</a></div>',
    '<div class="g"><span class="y">解决方案</span><a href="#models" data-scrollto="p-coop"><em>04</em>电站与算力节点</a></div>')
rep('<span class="pe-d">04 · 合作方式</span>\n        <h2 class="pe-t">能源与算力节点合作</h2>',
    '<span class="pe-d">04 · 解决方案</span>\n        <h2 class="pe-t">电站与算力节点解决方案</h2>')
rep('<a href="#network">能源与算力节点合作</a>', '<a href="#network">电站与算力节点解决方案</a>')


def four(items):
    """Dia 更新日志式：两栏、无卡片，粗标题 + 灰色一段（Zixin 10-29：不要所有区块都是卡片）"""
    return '<div class="dia2 rv">' + ''.join(f'<div><b>{t}</b><p>{d}</p></div>' for t, d in items) + '</div>'


BLOCK = '''
    <div id="coopModes">
    <h2 class="h2">核心痛点</h2>
    ''' + four([
        ('风光出力难以消纳', '风光利用率持续走低，弃电时段增加，三北场站的消纳压力更突出。'),
        ('午间发电收入承压', '午间光伏大发时，现货电价探底甚至为负，多发电也未必增加收入。'),
        ('电站收益更难预判', '新能源全面入市后，收入随市场电价波动，新增项目还需参与竞价。'),
        ('电力外送面临约束', '外送线路建设成本高，绿电直连上网比例受限，富余电量难以送出。'),
    ]) + '''
    <h2 class="h2">解决方案</h2>
    <p class="sol-lead rv">一体机在电站是后厂，Token 交易平台是前店。</p>
    <div class="cards3 rv">
      <div class="card"><span class="k">联合运营</span><h3>你投场地电力和设备</h3><p>你提供场地、电力并购买一体机。沐仞负责技术、调度、运营与销售，按合同分收益。</p></div>
      <div class="card"><span class="k">供电合作</span><h3>你供场地和电</h3><p>设备由沐仞或资产方投入。你提供场地和电力，收取电费与场地费，或参与分成。</p></div>
      <div class="card"><span class="k">算力接入</span><h3>现有算力接单卖 Token</h3><p>已有 GPU 算力中心可接入平台。按交易分润或服务价差获得收入。</p></div>
      <div class="card"><span class="k">自主运营</span><h3>私有化部署整套系统</h3><p>算电世界模型、调度系统和一体机部署到你的场站，你自己接单运营。沐仞负责部署、模型适配与远程支持。</p></div>
    </div>
    <h2 class="h2">核心优势</h2>
    <div class="adv4 rv">
      <div class="wide"><div class="wl"><span class="k">算电世界模型 · 私有化部署</span><h3>每一次调度，先在模型里跑一遍</h3><p>把电站出力与电价、GPU 功耗、网络和订单耦合进同一个模型，提前预测，让每一度电用在合适的任务和时段。</p></div><div class="w3"><div><b>推演</b><p>提前预测各时段的出力、电价、每台一体机的功耗与订单到达。</p></div><div><b>反事实</b><p>排之前先比：挪到别的站、降频或留到谷时，成本、时延和绿电各怎样。</p></div><div><b>自进化</b><p>每次调度的真实结果回写模型，每天更新，越调越准。</p></div></div></div>
      <div><h3>按用电与交付要求安排任务</h3><p>Tapestrix 先问模型再决策，把时段、站点和订单放在一起求解，再下发到一体机执行。</p><ul><li>可延后的批量任务排进富余绿电时段</li><li>急单走实时通道</li><li>电价高时降频，弃电时段多接单</li></ul></div>
      <div><h3>一体机部署与远程运维</h3><p>沐仞负责一体机选型、部署与模型适配。设备由沐仞远程运维，现场仅需巡检与备件配合。</p><ul><li>选配风冷、液冷或模块化集装箱形态</li><li>完成一体机部署与模型适配</li><li>远程运维配合现场巡检及备件支持</li></ul></div>
      <div><h3>为场站接入 Token 订单</h3><p>场站通过绿色 Token 交易平台对接沐仞客户与渠道。平台提供主流模型服务，按时段定价。</p><ul><li>通过交易平台对接客户与渠道</li><li>提供 GLM、DeepSeek、Qwen、MiniMax 模型服务</li><li>按不同时段设置 Token 价格</li></ul></div>
      <div><h3>逐单核对用电与月度分账</h3><p>将场站设备用电、电费与退款逐单对应。月度提供分账明细，每单附产地卡记录用电来源。</p><ul><li>逐单关联订单、设备用电、电费与退款</li><li>按月出具场站分账明细供核对</li><li>产地卡记录电站、时段、用电量、减排量</li></ul></div>
    </div>
    <h2 class="h2">行业价值</h2>
    ''' + four([
        ('富余电力就地利用', '一体机在场站将弃电时段的电转为 Token，无需新增并网资产或占用外送通道。'),
        ('场站自己的调度模型', '用场站自己的数据持续更新，任务安排依据本场站的出力、电价与运行结果。'),
        ('绿电来源逐单可查', '每单产地卡记录电站、时段、用电量与减排量，供买家用于 ESG 披露和绿色采购。'),
        ('按现有资源选择投入', '出设备联合运营、只出场地电力、接入既有算力，或私有化部署系统自己运营。'),
    ]) + '''
    <h2 class="h2">合作怎么走</h2>
    <div class="steps5 rv">
      <div><span class="k">01</span><b>提交场站信息</b><p>提供场站供电、场地及已有设备信息，说明希望参与的合作方式。</p></div>
      <div><span class="k">02</span><b>评估接入条件</b><p>共同评估供电、场地、冷却和网络条件，明确部署所需准备。</p></div>
      <div><span class="k">03</span><b>开展试点验收</b><p>通过试点核验任务质量、完整成本和可调负荷，作为后续合作依据。</p></div>
      <div><span class="k">04</span><b>签协议并部署</b><p>明确各方职责，分别约定设备、运营和平台交易价格，再推进部署。</p></div>
      <div><span class="k">05</span><b>运营与逐单分账</b><p>按协议开展运营，提供逐单交易与分账明细。</p></div>
    </div>
    </div>
'''
rep('    <div class="coop">\n      <div><h2 class="display">你的电站，可以是一个 Token 产地</h2><p>光伏、风电、水电场站及既有算力中心都可以接入。资产方出资采购一体机部署在场站，沐仞负责接入、调度、运营与 Token 销售，按合同分享收益。填写右侧表单，商务会联系你。</p>',
    BLOCK + '    <div class="coop">\n      <div><h2 class="display">看看你的场站怎么接</h2><p>说一下供电、场地或现有 GPU，一起评估合作方式。</p>')
rep('<div class="f"><input class="in" name="场站情况" placeholder="场站情况（可不填）：能源类型、装机、所在省市" id="cType" aria-label="场站情况（可不填）"></div>',
    '<div class="f"><input class="in" name="场站情况" placeholder="场站情况：能源类型、装机、所在省市" id="cType" aria-label="场站情况"></div><div class="f"><input class="in" name="可用容量与场地" placeholder="可用容量与场地（可不填）：可供算力的功率、机房或场地面积、网络" id="cCap" aria-label="可用容量与场地（可不填）"></div>')

rep('</head>', '<style id="plant-partnership-20261029">\n'
    '/* 电站解决方案页（2026-10-29）。站点主样式在 body 里、晚于本段，选择器加 [data-route="network"] 前缀 */\n'
    '[data-route="network"] #coopModes .h2{margin-top:48px}\n'
    '[data-route="network"] #reviews[hidden],[data-route="network"] .node .live[hidden]{display:none}\n'
    '[data-route="network"] .sol-lead{margin:4px 0 18px;padding:0;background:none;border:0;box-shadow:none;font-size:16px;line-height:1.7;color:var(--ink-70);white-space:nowrap}\n'
    '@media (max-width:640px){[data-route="network"] .sol-lead{white-space:normal}}\n'
    '[data-route="network"] #coopModes .cards3{grid-template-columns:repeat(4,minmax(0,1fr))}\n'
    '@media (max-width:980px){[data-route="network"] #coopModes .cards3{grid-template-columns:1fr 1fr}}\n'
    '@media (max-width:560px){[data-route="network"] #coopModes .cards3{grid-template-columns:1fr}}\n'
    '[data-route="network"] #coopModes .card p a{margin-left:4px;white-space:nowrap}\n'
    '[data-route="network"] .adv4{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}\n'
    '[data-route="network"] .adv4>div{display:grid;gap:10px;align-content:start;padding:22px 22px 20px;border-radius:12px;background:var(--card);border:1px solid var(--line)}\n'
    '[data-route="network"] .adv4 h3{margin:0;font:500 17px var(--sans);color:var(--ink)}\n'
    '[data-route="network"] .adv4 p{margin:0;font-size:14px;line-height:1.65;color:var(--ink-70)}\n'
    '[data-route="network"] .adv4 ul{margin:4px 0 0;padding-left:18px;display:grid;gap:4px;font-size:13px;line-height:1.6;color:var(--ink-85)}\n'
    '[data-route="network"] .adv4>.wide{grid-column:1/-1;display:grid;gap:22px;padding:28px;background:linear-gradient(120deg,var(--card),rgba(82,132,215,.07))}\n'
    '[data-route="network"] .adv4>.wide .wl{display:grid;gap:8px}\n'
    '[data-route="network"] .adv4>.wide .k{font:500 12px var(--sans);letter-spacing:.04em;color:var(--ink-50)}\n'
    '[data-route="network"] .adv4>.wide h3{font-size:22px}\n'
    '[data-route="network"] .adv4 .w3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr))}\n'
    '[data-route="network"] .adv4 .w3>div{display:grid;gap:6px;align-content:start;padding:2px 24px 0;border-left:1px solid var(--line)}\n'
    '[data-route="network"] .adv4 .w3>div:first-child{padding-left:0;border-left:0}\n'
    '[data-route="network"] .adv4 .w3 b{font:500 15px var(--sans);color:var(--ink)}\n'
    '[data-route="network"] .adv4 .w3 p{font-size:13.5px}\n'
    '@media (max-width:760px){[data-route="network"] .adv4 .w3{grid-template-columns:1fr;gap:14px}[data-route="network"] .adv4 .w3>div{padding:0;border-left:0}}\n'
    '@media (max-width:640px){[data-route="network"] .adv4{grid-template-columns:1fr}}\n'
    '[data-route="network"] .dia2{display:grid;grid-template-columns:1fr 1fr;gap:28px 48px;max-width:980px}\n'
    '[data-route="network"] .dia2>div{display:grid;gap:6px}\n'
    '[data-route="network"] .dia2 b{font:500 16px var(--sans);color:var(--ink)}\n'
    '[data-route="network"] .dia2 p{margin:0;font-size:15px;line-height:1.6;color:var(--ink-50)}\n'
    '@media (max-width:640px){[data-route="network"] .dia2{grid-template-columns:1fr;gap:20px}}\n'
    '[data-route="network"] .sol4{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}\n'
    '[data-route="network"] .sol4>div{display:grid;gap:8px;align-content:start;padding:18px 16px;border-radius:12px;background:var(--card);border:1px solid var(--line)}\n'
    '[data-route="network"] .sol4 b{font:500 15px var(--sans);color:var(--ink)}\n'
    '[data-route="network"] .sol4 p{margin:0;font-size:13px;line-height:1.6;color:var(--ink-70)}\n'
    '[data-route="network"] .steps5{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:16px}\n'
    '[data-route="network"] .steps5>div{display:grid;gap:8px;align-content:start;padding:18px 16px;border-radius:12px;background:var(--card);border:1px solid var(--line)}\n'
    '[data-route="network"] .steps5 .k{font:400 11px var(--mono);letter-spacing:.08em;color:var(--ink-50)}\n'
    '[data-route="network"] .steps5 b{font:500 15px var(--sans);color:var(--ink)}\n'
    '[data-route="network"] .steps5 p{margin:0;font-size:13px;line-height:1.6;color:var(--ink-70)}\n'
    '@media (max-width:860px){[data-route="network"] .sol4,[data-route="network"] .steps5{grid-template-columns:1fr 1fr}}\n'
    '@media (max-width:560px){[data-route="network"] .sol4,[data-route="network"] .steps5{grid-template-columns:1fr}}\n'
    '</style>\n</head>')

EN = {
    '解决方案': 'Solutions', '电站与算力节点': 'Plants & compute nodes', '04 · 解决方案': '04 · Solutions', '电站与算力节点解决方案': 'Plant & compute-node solutions',
    '你的电站，可以是一个 Token 产地': 'Your power station can be a source of Tokens',
    '富余绿电就地运行 AI 模型，Token 卖给 AI 客户。': 'Surplus green power runs AI models on site; the Tokens go to AI customers.',
    '核心痛点': 'Key challenges',
    '风光出力难以消纳': 'More power goes unused', '风光利用率持续走低，弃电时段增加，三北场站的消纳压力更突出。': 'Wind and solar utilisation keeps falling and curtailment hours grow, hardest in the north.',
    '午间发电收入承压': 'Midday generation earns less', '午间光伏大发时，现货电价探底甚至为负，多发电也未必增加收入。': 'At solar peak the spot price hits zero or below, so more output doesn’t mean more revenue.',
    '电站收益更难预判': 'Revenue is harder to forecast', '新能源全面入市后，收入随市场电价波动，新增项目还需参与竞价。': 'With full market entry, income moves with the spot price and new projects must bid.',
    '电力外送面临约束': 'Exporting surplus power is hard', '外送线路建设成本高，绿电直连上网比例受限，富余电量难以送出。': 'Transmission lines are costly and direct-connect projects face export caps.',
    '一体机在电站是后厂，Token 交易平台是前店。': 'Appliances at the plant are the factory; the Token trading platform is the storefront.',
    '联合运营': 'Joint operation', '你投场地电力和设备': 'You provide the site, power and appliances', '你提供场地、电力并购买一体机。沐仞负责技术、调度、运营与销售，按合同分收益。': 'You provide the site and power and purchase the appliances. FathomPeak handles technology, scheduling, operations and sales, with revenue shared under the agreement.',
    '供电合作': 'Power supply partnership', '你供场地和电': 'You provide the site and power', '设备由沐仞或资产方投入。你提供场地和电力，收取电费与场地费，或参与分成。': 'FathomPeak or an asset partner funds the equipment. You provide the site and power, earning electricity and site fees or a share of revenue.',
    '算力接入': 'Compute integration', '现有算力接单卖 Token': 'Sell Tokens with your existing compute', '已有 GPU 算力中心可接入平台。按交易分润或服务价差获得收入。': 'Existing GPU compute centres can connect to the platform. Revenue comes from transaction sharing or service margins.',
    '部署算电世界模型': 'Deploy the world model on site',
    '沐仞将算电世界模型与一体机部署到你的场站。你自己接单运营，沐仞负责部署、模型适配与远程支持。': 'FathomPeak deploys the power–compute world model and appliances at your site. You run orders and operations; FathomPeak handles deployment, model adaptation and remote support.',
    '算电世界模型部署到场站': 'The power–compute world model, on your site',
    '专做算电调度的小模型，部署到你的场站。使用你自己的数据，数据留在场站，模型按日用调度结果更新。': 'A small model built for power–compute scheduling, deployed at your site. It learns from your own data, which stays on site, and updates daily from scheduling results.',
    '接入场站出力、电价与单卡功耗': 'Site output, power prices and per-card power draw',
    '接入订单、报价与交付要求': 'Orders, quotes and delivery requirements',
    '执行后的用电与减排计量回写模型': 'Metered power use and emissions avoided fed back after each run',
    '按用电与交付要求安排任务': 'Schedule tasks around power and delivery needs',
    '比较任务在不同时段、设备上运行的用电与成本。选定排法后，经 Tapestrix 下发到一体机执行。': 'Compare power use and cost for each task across time windows and devices, then dispatch the chosen plan to the appliances through Tapestrix.',
    '结合场站出力与电价安排运行时段': 'Time windows set by site output and power prices',
    '按单卡功耗与订单交付要求安排设备': 'Devices assigned by per-card power draw and delivery needs',
    '对比不同排法的用电与成本推演结果': 'Projected power use and cost compared across plans',
    '场站自己的调度模型': 'A scheduling model of your own',
    '用场站自己的数据持续更新，任务安排依据本场站的出力、电价与运行结果。': 'Updated with your own data, so scheduling follows your site’s output, prices and results.',
    '私有化部署整套系统': 'Deploy the whole system privately',
    '算电世界模型、调度系统和一体机部署到你的场站，你自己接单运营。沐仞负责部署、模型适配与远程支持。': 'The power–compute world model, scheduler and appliances are deployed at your site and you run the orders; FathomPeak handles deployment, model adaptation and remote support.',
    '算电世界模型 · 私有化部署': 'Power–compute world model · private deployment',
    '每一次调度，先在模型里跑一遍': 'Every dispatch runs in the model first',
    '把电站出力与电价、GPU 功耗、网络和订单耦合进同一个模型，提前预测，让每一度电用在合适的任务和时段。': 'Plant output and power prices, GPU power draw, network and orders are coupled in one model that predicts ahead, so every kilowatt-hour goes to the right task at the right time.',
    '推演': 'Forecast',
    '提前预测各时段的出力、电价、每台一体机的功耗与订单到达。': 'Predicts output, power prices, each appliance’s power draw and incoming orders for the hours ahead.',
    '反事实': 'What-if',
    '排之前先比：挪到别的站、降频或留到谷时，成本、时延和绿电各怎样。': 'Before scheduling, compares moving to another site, throttling or waiting for off-peak: cost, latency and green power for each.',
    '自进化': 'Self-improving',
    '每次调度的真实结果回写模型，每天更新，越调越准。': 'Real results from every dispatch are written back and the model updates daily, getting more accurate over time.',
    'Tapestrix 先问模型再决策，把时段、站点和订单放在一起求解，再下发到一体机执行。': 'Tapestrix asks the model before deciding, solves time, site and orders together, then dispatches to the appliances.',
    '可延后的批量任务排进富余绿电时段': 'Deferrable batch tasks go into surplus green-power windows',
    '急单走实时通道': 'Urgent jobs take the real-time lane',
    '电价高时降频，弃电时段多接单': 'Throttle when power is expensive; take more orders during curtailment',
    '出设备联合运营、只出场地电力、接入既有算力，或私有化部署系统自己运营。': 'Co-operate with your own appliances, provide only site and power, connect existing compute, or deploy the system privately and run it yourself.',
    '自主运营': 'Run it yourself', '你自己运营，沐仞交付系统': 'You operate; FathomPeak delivers the system', '一体机和算电调度基座按项目交付到你的场站，你自己接单运营。沐仞负责部署、模型适配与远程支持。': 'Appliances and the power–compute scheduling platform are delivered to your site as a project; you take orders and run it, with FathomPeak handling deployment, model tuning and remote support.', '申请条件评估 →': 'Request a site assessment →',
    '核心优势': 'Key strengths',
    '按场站用电条件调度任务': 'Schedule compute around site power conditions', '沐仞自建算电世界模型，经 Tapestrix 安排任务。结合电价、出力与订单规律，区分批量任务和急单。': 'FathomPeak’s own power–compute world model schedules tasks through Tapestrix, weighing electricity prices, output and order patterns, with separate paths for batch and urgent work.',
    '将可延后的批量任务排入富余绿电时段': 'Deferrable batch tasks run in surplus green-power windows', '将紧急订单接入实时任务通道': 'Urgent orders take the real-time lane', '按电价、出力与订单规律调度': 'Scheduling follows prices, output and order patterns',
    '一体机部署与远程运维': 'Appliance deployment and remote operations', '沐仞负责一体机选型、部署与模型适配。设备由沐仞远程运维，现场仅需巡检与备件配合。': 'FathomPeak selects, deploys and tunes the appliances, then operates them remotely; site staff handle inspections and spare parts.',
    '选配风冷、液冷或模块化集装箱形态': 'Air-cooled, liquid-cooled or modular container options', '完成一体机部署与模型适配': 'Appliance deployment and model adaptation', '远程运维配合现场巡检及备件支持': 'Remote operations with on-site inspections and spares',
    '为场站接入 Token 订单': 'Token orders for your site', '场站通过绿色 Token 交易平台对接沐仞客户与渠道。平台提供主流模型服务，按时段定价。': 'Your site connects to FathomPeak’s customers and channels through the Green Token Trading Platform, which serves mainstream models with time-based pricing.',
    '通过交易平台对接客户与渠道': 'Customers and channels via the trading platform', '提供 GLM、DeepSeek、Qwen、MiniMax 模型服务': 'GLM, DeepSeek, Qwen and MiniMax model services', '按不同时段设置 Token 价格': 'Token prices set by time window',
    '逐单核对用电与月度分账': 'Per-order power reconciliation and monthly settlement', '将场站设备用电、电费与退款逐单对应。月度提供分账明细，每单附产地卡记录用电来源。': 'Equipment power use, electricity cost and refunds are matched to each order; monthly settlement statements and a per-order origin card record the power source.',
    '逐单关联订单、设备用电、电费与退款': 'Each order linked to power use, cost and refunds', '按月出具场站分账明细供核对': 'Monthly site settlement statements for review', '产地卡记录电站、时段、用电量、减排量': 'Origin card: station, window, power used, emissions avoided',
    '行业价值': 'Value for your business',
    '富余电力就地利用': 'Surplus power used on site', '一体机在场站将弃电时段的电转为 Token，无需新增并网资产或占用外送通道。': 'Appliances at the plant turn curtailed power into Tokens, with no new grid assets or export capacity.',
    '对接绿色算力需求': 'Meet demand for green compute', '将场站富余绿电用于算力生产，为关注用电成本的 AI 客户提供绿色算力。': 'Surplus green power becomes compute for AI customers who watch their electricity cost.',
    '绿电来源逐单可查': 'Green power traced per order', '每单产地卡记录电站、时段、用电量与减排量，供买家用于 ESG 披露和绿色采购。': 'Each origin card records station, window, power used and emissions avoided, for ESG and green procurement.',
    '按现有资源选择投入': 'Choose how you participate', '出设备联合运营、只出场地电力、接入既有算力，或买下系统自己运营。': 'Co-operate with your own appliances, provide only site and power, connect existing compute, or buy the system and run it yourself.',
    '合作怎么走': 'How we work together',
    '提交场站信息': 'Share your site information', '提供场站供电、场地及已有设备信息，说明希望参与的合作方式。': 'Share your power supply, site and existing equipment, and the partnership model you prefer.',
    '评估接入条件': 'Assess site readiness', '共同评估供电、场地、冷却和网络条件，明确部署所需准备。': 'Together we assess power, space, cooling and connectivity to identify what deployment requires.',
    '开展试点验收': 'Run and evaluate a pilot', '通过试点核验任务质量、完整成本和可调负荷，作为后续合作依据。': 'The pilot checks task quality, total cost and adjustable load, and informs the next stage.',
    '签协议并部署': 'Agree on terms and deploy', '明确各方职责，分别约定设备、运营和平台交易价格，再推进部署。': 'Define responsibilities and agree separate pricing for equipment, operations and platform transactions before deployment.',
    '运营与逐单分账': 'Operate and settle by order', '按协议开展运营，提供逐单交易与分账明细。': 'Operations follow the agreement, with transaction and settlement details for each order.',
    '看看你的场站怎么接': 'See how your site fits', '说一下供电、场地或现有 GPU，一起评估合作方式。': 'Tell us about your power, site or GPUs and we’ll assess the fit.',
    '场站情况：能源类型、装机、所在省市': 'Site: energy type, capacity, province/city', '可用容量与场地（可不填）：可供算力的功率、机房或场地面积、网络': 'Available capacity and space (optional): power for compute, room or site area, network',
}
rep('  syncAuthLocale(); applyLang();', '  (function(S){for(var k in S) if(!(k in I18N)) I18N[k]=S[k]})(' + json.dumps(EN, ensure_ascii=False) + ');  /* 电站解决方案页 */\n  syncAuthLocale(); applyLang();')
p.write_text(s, encoding='utf8')
print('done')
