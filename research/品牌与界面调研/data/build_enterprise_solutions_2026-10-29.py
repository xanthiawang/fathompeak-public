"""企业订购页按无问芯穹「AI 原生企业解决方案」结构重写（Zixin 2026-10-29：写清楚我们为企业提供什么好处和优势）。
结构：首屏 → 核心痛点 → 解决方案 → 核心优势 → 行业价值 → 个人/企业账号 → 四步 → 咨询。
文案：Codex 第二轮（Codex文案_企业订购页_第二轮_2026-10-29.md），痛点逐条有报道/论文依据，见 企业痛点与价值_调研笔记_2026-10-29.md「第二轮」。
FAQ 删掉：牌照、数据出境、专票、本地部署、SLA 都已写进方案和优势，算电协同项目归电站页。
用法：python3 -I build_enterprise_solutions_2026-10-29.py <站点根目录>
"""
import json, sys
from pathlib import Path

p = Path(sys.argv[1]) / 'index.html'
s = p.read_text(encoding='utf8')
if 'id="entModes"' in s: sys.exit('[停止] 已经改过')


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: sys.exit(f'[停止] 匹配 {c} 次（应为 {n}）：{old[:90]}')
    s = s.replace(old, new)


def dia(items):
    return '<div class="dia2 rv">' + ''.join(f'<div><b>{t}</b><p>{d}</p></div>' for t, d in items) + '</div>'


def rows(items):
    # 痛点单列横排：左标题右说明，细线分隔（Zixin：同一页别全是卡片）
    return '<div class="rows5 rv">' + ''.join(f'<div><b>{t}</b><p>{d}</p></div>' for t, d in items) + '</div>'


def adv(items):
    return '<div class="adv4 rv">' + ''.join(
        f'<div><h3>{t}</h3><p>{d}</p><ul>' + ''.join(f'<li>{b}</li>' for b in bl) + '</ul></div>' for t, d, bl in items) + '</div>'


# 首屏
rep('<h1 class="display">企业采购与海外服务</h1><p>面向企业、高校、科研机构及渠道平台，说清应用场景和用量，先测试，再报价采购。每笔订单附一张产地卡，记录电站、时段与用电量。</p>',
    '<h1 class="display">低价用模型，清楚管账</h1><p>沐仞按量提供模型服务，用量、费用与用电逐单可查。</p>')

# 三张卡 → 痛点 + 解决方案 + 优势 + 价值
a = s.index('    <div class="cards3 rv">\n      <div class="card"><span class="k">企业与机构采购</span>')
b = s.index('    <h2 class="h2">个人账号与企业账号</h2>')
BLOCK = '''    <h2 class="h2">核心痛点</h2>
    ''' + rows([
        ('调用增长，预算难控', '用量随业务扩张，费用难预估，也难对应业务收益。'),
        ('自建算力，闲置也贵', '业务负载有高有低，自建算力仍需承担闲置成本。'),
        ('敏感数据，部署两难', '业务希望尽快用上模型，数据保护与治理要求也需兼顾。'),
        ('AI 排放，核算缺据', '按金额估算难反映实际用电，排放披露缺少可靠依据。'),
        ('跨境调用，链路难查', '跨境调用涉及多重合规要求，模型来源与计费也需核实。'),
    ]) + '''
    <h2 class="h2">解决方案</h2>
    <p class="sol-lead rv">从按量调用到本地部署，按业务需求选择交付方式。</p>
    <div class="cards3 rv" id="entModes">
      <div class="card"><span class="k">按量采购</span><h3>按量采购 Token</h3><p>先用你的任务测试，再按 Token 用量报价。支持 GLM、DeepSeek、Qwen、MiniMax。</p></div>
      <div class="card"><span class="k">私有部署</span><h3>私有化部署与智能体</h3><p>一体机部署在机房或实验室，数据不出域。智能体接入企业工具，沐仞远程运维。</p></div>
      <div class="card"><span class="k">海外调用</span><h3>Token 出海</h3><p>海外团队直接调用中国模型。出海运营主体持中央网信办业务批复，签约前可提供合规文件。</p></div>
      <div class="card"><span class="k">渠道合作</span><h3>渠道与平台分发</h3><p>面向自有应用与渠道分发提供模型服务。价格与结算方式按协议约定。</p></div>
    </div>
    <h2 class="h2">核心优势</h2>
    ''' + adv([
        ('用量账单归集到业务', '按 Token 实际用量计费。通过组织钱包与逐单记录，让费用有归属、用量可核对。',
         ['正式报价前完成业务用量测试', '通过主子账号归集组织用量', '提供逐单用量与计费核对记录']),
        ('算电调度降低调用成本', '批量任务可排入绿电时段，公开价 4 折起。按量购买 Token，无需先投入自建算力。',
         ['将批量任务安排至绿电时段', '按业务实际用量提供模型服务', '急单走实时通道，时延写进协议']),
        ('按业务边界选择部署', '敏感业务可选私有化部署。跨境模型调用提供获批通道，模型与计费逐单可查。',
         ['提供私有化一体机与远程运维', '提供持网信办批复的跨境通道', '逐单记录调用模型与计费明细']),
        ('逐单提供用电减排依据', '产地卡记录每单实测用电量与减排量。企业核算有据可查，减少对金额估算的依赖。',
         ['随订单提供可查验的产地卡', '逐单记录任务的实测用电量', '提供每单对应的减排量记录']),
    ]) + '''
    <h2 class="h2">行业价值</h2>
    <div class="val4 rv">
      <div><b>预算安排更有依据</b><p>看清业务用量与费用，让预算调整有据可循。</p></div>
      <div><b>算力投入更有弹性</b><p>业务起伏时，减少固定算力投入与闲置负担。</p></div>
      <div><b>部署选择贴合业务</b><p>兼顾敏感业务部署与跨境模型使用需求。</p></div>
      <div><b>碳排核算更有依据</b><p>为内部核算与对外披露提供可追溯的用电依据。</p></div>
    </div>
'''
s = s[:a] + BLOCK + s[b:]

# 四步：去掉「样例」
rep('<b>确认需求与样例</b><p>明确任务、模型、用量与响应要求，准备可测试的样例负载。</p>',
    '<b>确认需求与测试任务</b><p>明确任务、模型、用量与响应要求，准备用于测试的真实任务。</p>')

# FAQ 整块删掉（内容已进方案与优势）
a = s.index('    <div class="faq rv"><h2>企业采购常见问题</h2>')
b = s.index('    <div class="coop rv" id="enterprise-sales">')
s = s[:a] + s[b:]

# 咨询区保持线上原文（Zixin 10-29：「带着任务来谈」像在命令人）

R = '[data-route="enterprise"]'
rep('</head>', '<style id="enterprise-solutions-20261029">\n'
    f'{R} .sol-lead{{margin:4px 0 18px;font-size:16px;line-height:1.7;color:var(--ink-70);white-space:nowrap}}\n'
    f'@media (max-width:640px){{{R} .sol-lead{{white-space:normal}}}}\n'
    f'{R} #entModes{{grid-template-columns:repeat(4,minmax(0,1fr))}}\n'
    f'@media (max-width:980px){{{R} #entModes{{grid-template-columns:1fr 1fr}}}}\n'
    f'@media (max-width:560px){{{R} #entModes{{grid-template-columns:1fr}}}}\n'
    f'{R} .dia2{{display:grid;grid-template-columns:1fr 1fr;gap:28px 48px;max-width:980px}}\n'
    f'{R} .dia2>div{{display:grid;gap:6px}}\n'
    f'{R} .dia2 b{{font:500 16px var(--sans);color:var(--ink)}}\n'
    f'{R} .dia2 p{{margin:0;font-size:15px;line-height:1.6;color:var(--ink-50)}}\n'
    f'@media (max-width:640px){{{R} .dia2{{grid-template-columns:1fr;gap:20px}}}}\n'
    f'{R} .adv4{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}}\n'
    f'{R} .adv4>div{{display:grid;gap:10px;align-content:start;padding:22px 22px 20px;border-radius:12px;background:var(--card);border:1px solid var(--line)}}\n'
    f'{R} .adv4 h3{{margin:0;font:500 17px var(--sans);color:var(--ink)}}\n'
    f'{R} .adv4 p{{margin:0;font-size:14px;line-height:1.65;color:var(--ink-70)}}\n'
    f'{R} .adv4 ul{{margin:4px 0 0;padding-left:18px;display:grid;gap:4px;font-size:13px;line-height:1.6;color:var(--ink-85)}}\n'
    f'@media (max-width:640px){{{R} .adv4{{grid-template-columns:1fr}}}}\n'
    f'{R} .rows5{{display:grid;max-width:980px;border-top:1px solid var(--line)}}\n'
    f'{R} .rows5>div{{display:grid;grid-template-columns:220px minmax(0,1fr);gap:24px;align-items:baseline;padding:16px 0;border-bottom:1px solid var(--line)}}\n'
    f'{R} .rows5 b{{font:500 16px var(--sans);color:var(--ink)}}\n'
    f'{R} .rows5 p{{margin:0;font-size:15px;line-height:1.6;color:var(--ink-50)}}\n'
    f'@media (max-width:640px){{{R} .rows5>div{{grid-template-columns:1fr;gap:4px}}}}\n'
    # 行业价值：四列，顶部一条细线，和上面的卡片区分开
    f'{R} .val4{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:28px}}\n'
    f'{R} .val4>div{{display:grid;gap:8px;align-content:start;padding-top:16px;border-top:1px solid var(--ink)}}\n'
    f'{R} .val4 b{{font:500 16px var(--sans);color:var(--ink)}}\n'
    f'{R} .val4 p{{margin:0;font-size:14px;line-height:1.6;color:var(--ink-50)}}\n'
    f'@media (max-width:980px){{{R} .val4{{grid-template-columns:1fr 1fr}}}}\n'
    f'@media (max-width:560px){{{R} .val4{{grid-template-columns:1fr;gap:20px}}}}\n'
    '</style>\n</head>')

EN = {
    '低价用模型，清楚管账': 'Lower model costs. Clearer spending.',
    '沐仞按量提供模型服务，用量、费用与用电逐单可查。': 'Usage-based model services, with usage, cost and electricity traceable for every order.',
    '调用增长，预算难控': 'Growing usage, unpredictable spend', '用量随业务扩张，费用难预估，也难对应业务收益。': 'As usage grows, costs get harder to forecast and to tie to business returns.',
    '自建算力，闲置也贵': 'Idle capacity still costs money', '业务负载有高有低，自建算力仍需承担闲置成本。': 'Demand rises and falls, but owned compute keeps costing money when idle.',
    '敏感数据，部署两难': 'Sensitive data complicates deployment', '业务希望尽快用上模型，数据保护与治理要求也需兼顾。': 'Teams want AI quickly while still meeting data protection and governance rules.',
    'AI 排放，核算缺据': 'AI emissions lack an accounting basis', '按金额估算难反映实际用电，排放披露缺少可靠依据。': 'Spend-based estimates miss actual electricity use, leaving disclosures without solid evidence.',
    '跨境调用，链路难查': 'Cross-border access is hard to verify', '跨境调用涉及多重合规要求，模型来源与计费也需核实。': 'Cross-border use brings overlapping compliance rules, and model source and billing need checking.',
    '从按量调用到本地部署，按业务需求选择交付方式。': 'From usage-based access to on-premises deployment, pick what fits your business.',
    '按量采购': 'Usage-based', '按量采购 Token': 'Buy Tokens by usage', '先用你的任务测试，再按 Token 用量报价。支持 GLM、DeepSeek、Qwen、MiniMax。': 'We test with your tasks, then quote by Token usage. GLM, DeepSeek, Qwen and MiniMax supported.',
    '私有部署': 'Private deployment', '私有化部署与智能体': 'Private deployment and agents', '一体机部署在机房或实验室，数据不出域。智能体接入企业工具，沐仞远程运维。': 'Appliances run in your server room or lab and data stays inside. Agents connect to your tools; FathomPeak operates them remotely.',
    '海外调用': 'Overseas access', '海外团队直接调用中国模型。出海运营主体持中央网信办业务批复，签约前可提供合规文件。': 'Overseas teams call Chinese models directly. Our overseas operator holds CAC approval for Token export, with compliance documents available before signing.',
    '渠道合作': 'Channels', '渠道与平台分发': 'Channel and platform distribution', '面向自有应用与渠道分发提供模型服务。价格与结算方式按协议约定。': 'Model services for your own apps and channel distribution, with pricing and settlement set by agreement.',
    '用量账单归集到业务': 'Usage and billing tied to the business', '按 Token 实际用量计费。通过组织钱包与逐单记录，让费用有归属、用量可核对。': 'Pay for actual Token usage. An organisation wallet and per-order records make spend attributable and usage verifiable.',
    '正式报价前完成业务用量测试': 'Workload tested before a formal quote', '通过主子账号归集组织用量': 'Usage rolled up across main and sub-accounts', '提供逐单用量与计费核对记录': 'Per-order usage and billing records',
    '算电调度降低调用成本': 'Power–compute scheduling lowers cost', '批量任务可排入绿电时段，公开价 4 折起。按量购买 Token，无需先投入自建算力。': 'Batch work runs in green-power windows, from 40% of list price. Buy Tokens as needed, with no upfront compute.',
    '将批量任务安排至绿电时段': 'Batch work scheduled into green-power windows', '按业务实际用量提供模型服务': 'Model services sized to actual usage', '急单走实时通道，时延写进协议': 'Urgent jobs on the real-time lane, latency in the agreement',
    '按业务边界选择部署': 'Deployment that fits your boundaries', '敏感业务可选私有化部署。跨境模型调用提供获批通道，模型与计费逐单可查。': 'Sensitive work can be deployed privately. Cross-border use goes through an approved channel, with model and billing traceable per order.',
    '提供私有化一体机与远程运维': 'Private appliances with remote operations', '提供持网信办批复的跨境通道': 'A CAC-approved cross-border channel', '逐单记录调用模型与计费明细': 'Model and billing recorded per order',
    '逐单提供用电减排依据': 'Power and emissions evidence per order', '产地卡记录每单实测用电量与减排量。企业核算有据可查，减少对金额估算的依赖。': 'Origin cards record measured electricity and emissions avoided for each order, so accounting relies less on spend-based estimates.',
    '随订单提供可查验的产地卡': 'A verifiable origin card with each order', '逐单记录任务的实测用电量': 'Measured electricity per order', '提供每单对应的减排量记录': 'Emissions avoided per order',
    '预算安排更有依据': 'Better-informed budgets', '看清业务用量与费用，让预算调整有据可循。': 'See usage and cost by business activity and adjust budgets on evidence.',
    '算力投入更有弹性': 'More flexible compute spend', '业务起伏时，减少固定算力投入与闲置负担。': 'Less fixed compute and idle cost when demand swings.',
    '部署选择贴合业务': 'Deployment that fits the business', '兼顾敏感业务部署与跨境模型使用需求。': 'Covers both sensitive workloads and cross-border model use.',
    '碳排核算更有依据': 'Better carbon accounting', '为内部核算与对外披露提供可追溯的用电依据。': 'Traceable electricity data for internal accounting and external disclosure.',
    '联系销售': 'Talk to sales',  # 线上被后加的 'Sales lead' 覆盖，标题显示错了
    '确认需求与测试任务': 'Confirm needs and test tasks', '明确任务、模型、用量与响应要求，准备用于测试的真实任务。': 'Define tasks, models, volume and response needs, and prepare real tasks for testing.',
}
rep('  syncAuthLocale(); applyLang();', '  (function(S){for(var k in S) I18N[k]=S[k]})(' + json.dumps(EN, ensure_ascii=False) + ');  /* 企业订购页 */\n  syncAuthLocale(); applyLang();')
p.write_text(s, encoding='utf8')
print('done')
