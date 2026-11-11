"""首页「行业与场景」改成「行业解决方案」（Zixin 2026-10-29）。
 · 标题定为「方案按场景定，成本由世界模型算。」（Zixin 选 1），副标题点出自建算电世界模型；小标签「行业解决方案」
 · 「开发者与社区」不是行业，移出卡片，改成卡片下方一行小字（注册即用 → 免费试用 Token）
 · 新卡「企业私有化与智能体部署」补上，仍是 6 张 3×2
 · 每张卡底部三个场景标签：写这个场景的客户在做什么、我们接什么（参考无问芯穹解决方案页的写法：每个方案三个各不相同的能力标签），
   不写计费方式之类通用词（Zixin：「你这标签没有什么实际意义」）
注意：私有化一体机的交付口径上线前要和开发确认。
用法：python3 -I build_industry_solutions_2026-10-29.py <站点根目录>
"""
import json, sys
from pathlib import Path

p = Path(sys.argv[1]) / 'index.html'
s = p.read_text(encoding='utf8')
if '各行各业的低价 Token' in s: sys.exit('[停止] 已经改过')


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: sys.exit(f'[停止] 匹配 {c} 次（应为 {n}）：{old[:90]}')
    s = s.replace(old, new)


rep('<div class="hh rv"><span class="k">一张图看懂</span><h2>行业与场景</h2><p>主要承接可延后、可批量的推理任务。</p></div>',
    '<div class="hh rv"><span class="k">行业解决方案</span><h2>让 AI 用上绿电<br>各行各业的低价 Token</h2><p>按行业给出 AI 方案；算电世界模型替你选时段、选节点，Token 公开价 4 折起。</p></div>')
# 「开发者与社区」直接去掉（Zixin 10-29：删除那行小字）
TILES = [
    # 第三次纠正（Zixin 10-29）：文字太多，只留核心信息；不要标签
    # 第四次（10-29 晚）：短剧、Science、社交、审核四张恢复线上原文（Zixin：线上写得更好）
    ['Token 出海', '持网信办出海批复，海外团队直接调用中国模型。', '', '#5284D7'],
    ['AI 短剧与影视', '剧本、分镜与配音文案批量生成；可延后的任务排进绿电富余时段，成本更低。', '', '#2F63B8'],
    ['AI for Science', '文献抽取、数据整理与科研推理，按 Token 用量采购，不用自建算力。', '', '#A9C3E8'],
    ['社交与情感陪伴', '大流量对话按 Token 计费；官方 API 的高峰时段，这里照样有供给。', '', '#4E3F66'],
    ['内容与图文审核', '海量图文批量审核，可以按审核结果打包交付。', '', '#EBCFC4'],
    ['企业私有化与智能体部署', '一体机部署在你的机房，数据不出域，智能体接入企业工具。', '', '#D6CBDD'],
]
a = s.find('var IND=['); b = s.find('];', a) + 2
if a < 0 or s.count('var IND=[') != 1: sys.exit('[停止] 找不到 IND')
s = s[:a] + 'var IND=' + json.dumps(TILES, ensure_ascii=False) + ';' + s[b:]

rep('</head>', '<style id="industry-solutions-20261029">\n'
    '/* 行业解决方案（2026-10-29）。站点主样式在 body 里、晚于本段，选择器加 #home2 前缀 */\n'
    '#home2 .inds-note{max-width:900px;margin:14px auto 0;font-size:13px;line-height:1.6;color:var(--ink-50);text-align:center}\n'
    '#home2 .inds-note a{color:var(--ink-70);margin-left:6px}\n'
    '#home2 .itile .pf{font:400 12px/1.7 var(--sans);letter-spacing:0;color:var(--ink-70)}\n'
    '</style>\n</head>')

EN = {
    '让 AI 用上绿电': 'Run AI on green power', '各行各业的低价 Token': 'Low-cost Tokens for every industry',
    '按行业给出 AI 方案；算电世界模型替你选时段、选节点，Token 公开价 4\u00a0折起。': 'An AI solution for each industry; our power–compute world model picks the window and the node, with Tokens from 60% off the list price.',
    '沐仞自建的算电世界模型持续学习电价、出力与任务规律，替你选时段、选节点、控成本。': 'FathomPeak’s own power–compute world model keeps learning prices, plant output and workload patterns, and picks the window, the node and the cost for you.',
    '持网信办出海批复，海外团队直接调用中国模型。': 'CAC-approved for token export; overseas teams call Chinese models directly.',
    '一体机部署在你的机房，数据不出域，智能体接入企业工具。': 'Appliances in your own server room, data stays on site, agents wired to your tools.',
    '行业解决方案': 'Industry solutions',
    '方案按场景定，成本由世界模型算。': 'Solutions set by scenario. Costs worked out by our world model.',
    '从短剧生成到企业私有化，按场景给出模型、算力与成本方案。沐仞自建的算电世界模型持续学习电价、出力与任务规律，替你选时段、选节点、控成本。': 'From short-drama generation to on-premise deployment, each scenario gets a model, compute and cost plan. FathomPeak’s own power–compute world model keeps learning prices, plant output and workload patterns, and picks the window, the node and the cost for you.',
    '个人开发者与一人公司不用走方案：注册即用，一个端点接入主流模型。': 'Individual developers and one-person companies don’t need a plan: sign up and go, one endpoint for the leading models.',
    '企业私有化与智能体部署': 'On-premise & agent deployment',
    '由持网信办批复的出海运营主体对外服务，海外团队用同一端点调用中国模型；来数在境内加工，合规链路由沐仞搭好。': 'Our CAC-approved cross-border entity serves overseas teams, who call Chinese models through the same endpoint; inbound data is processed in China, with the compliance chain set up by FathomPeak.',
    '把剧本、分镜、图生视频拆成可延后的批量任务，世界模型排进绿电富余时段生产，急单走实时通道；每批附产地卡结算。': 'Scripts, storyboards and image-to-video are split into deferrable batch jobs that the world model schedules into surplus green-power windows; urgent jobs take the real-time lane, and every batch settles with an origin card.',
    '按课题开通额度，文献抽取与长文本推理走批量通道，不用自建算力；用量与绿电数据出具产地卡，可用于报销与 ESG 报告。': 'Quotas are opened per project; literature extraction and long-context reasoning run on the batch lane with no compute to build; usage and green-power data come as origin cards for reimbursement and ESG reports.',
    '实时对话优先调度到低延迟节点并保证高峰供给，世界模型按负载在多个模型间分流，成本随电价浮动。': 'Live chat is routed to low-latency nodes with supply guaranteed through peak hours; the world model splits traffic across models by load, and cost follows the power price.',
    '多模态模型批量审核图文，任务放在绿电时段降成本；结果按批打包交付并留痕，可追溯到节点与时段。': 'Multimodal models review images and text in bulk, scheduled into green-power windows to cut cost; results are delivered in packaged batches with an audit trail back to node and time window.',
    'FPTM 一体机部署在企业或园区内，模型与数据不出域；智能体运行底座接入企业系统与工具，由世界模型统一调度与运维。': 'FPTM appliances run inside your company or campus, so models and data stay on site; an agent runtime connects your systems and tools, scheduled and maintained by the world model.',
    '持牌出海通道': 'Licensed cross-border channel', '境内合规数据处理': 'Compliant data processing in China', '统一端点海外调用': 'One endpoint for overseas calls',
    '批量任务绿电排产': 'Batch jobs on green-power windows', '图生视频队列': 'Image-to-video queue', '急单实时通道': 'Real-time lane for urgent jobs',
    '课题额度与对账': 'Per-project quotas & statements', '长文本批量推理': 'Long-context batch reasoning', '产地卡用于报告': 'Origin cards for reports',
    '高峰保供通道': 'Guaranteed supply at peak', '多模型分流': 'Multi-model routing', '低延迟节点优先': 'Low-latency nodes first',
    '多模态批量审核': 'Multimodal bulk review', '按批交付留痕': 'Batch delivery with audit trail', '绿电时段降本': 'Lower cost on green-power windows',
    'FPTM 一体机': 'FPTM appliance', '智能体运行底座': 'Agent runtime', '世界模型调度运维': 'World-model scheduling & ops',
}
rep('  syncAuthLocale(); applyLang();', '  (function(S){for(var k in S) if(!(k in I18N)) I18N[k]=S[k]})(' + json.dumps(EN, ensure_ascii=False) + ');  /* 行业解决方案 */\n  syncAuthLocale(); applyLang();')
p.write_text(s, encoding='utf8')
print('done')
