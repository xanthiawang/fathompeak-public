"""超管「中转 / 电站」逻辑整理（Zixin 2026-10-16："修复这些问题 修复前再仔细检查一遍"）。叠在线上 12f2ad4 上。
修复前复查结论（和上一轮审查不同的地方）：
 · 「表格视图详情打开旧面板」不成立：旧的「已有渠道」表、旧详情面板 #rtChD 都在整体隐藏的 .rt-legacy 里，用户点不到；可见的表格「编辑」开的就是新编辑框。不改。
 · 「表格里的同步按钮」同上，在隐藏的旧表里。不改。
 · 渠道卡片上直接改优先级 / 权重保留：new-api 的渠道列表本来就能行内改，方便批量调；它和编辑框改的是同一个值。
 · 「最大重试」按钮只是跳到路由页的快捷入口，不是第二个编辑处，保留，只改页名。
 · 「需开发」「new-api 现成」标签在线上已被样式隐藏，不改。
 · 工作台待办里的财务单子：「公司资料学习」会话已在本地分支 fin-desk 做完，这里跳过，避免重复。
 · 审计日志条目（「冻结组织」「改组织定价」「发布基础价…家组织」）是历史记录，英文翻译按原文正则匹配，保持原样；只改界面上的按钮和说明。
本脚本做的：
 1 路由页：删掉和渠道列表重复的「按渠道」表；页名「路由与转换」→「路由与可靠性」（侧栏、页头、所有引用）；「按模型」里的渠道名可点开编辑框；
   「封禁 / 禁用」统一叫「停用」；删掉「智能路由…交接文档」和「只在预览里生效」这两句。
 2 定价：页头下加「怎么计价」规则框（个人、企业各一行）；「继承的组织」→「沿用基础价的企业」；
   分时价加时段来源（手填时段 / 跟随电站绿电时段）和「全部模型」，「折扣 %」改成「按原价 %」说清楚；
   去掉分时价、个人套餐里的「new-api」「需开发」。
 3 渠道编辑框：加「渠道来源：第三方厂商 / 自营节点」，选自营时挑算力节点（节点在「电站与时段」新增后可选）；卡片上标「自营节点」；
   多密钥的「自动禁用 / 禁用原因 / 禁用时间」→「停用」。
 4 电站：说明改成「自营渠道挂节点、节点挂电站，第三方渠道不挂电站」；表格加「所属合作方」；官网展示说明去掉「官网后台那张表停用」；
   绿电时段说明对上新的分时价来源。
 5 企业客户详情和定价里的「组织」→「企业 / 企业客户」（客户自己后台的「组织余额」、OpenAI 的「组织 ID」不动）。
 6 日志说明、模型「同步资料」按钮去掉「new-api」，按钮改名「更新模型资料」。
用法：python3 -I build_relay_logic_fix_2026-10-16.py <线上 index.html（12f2ad4）> <输出 html>
"""
import json, re, sys

SRC, OUT = sys.argv[1], sys.argv[2]
s = open(SRC, encoding='utf8').read()
EN = {}


def _is_dict_line(l):
    t = l.lstrip()
    return t.startswith('Object.assign(I18N') or t.startswith('var I18N') or t.startswith('(function(S){for(var k in S)') or t.startswith('I18N[')


def rep(old, new, n=1):
    """只替换页面和脚本里的文字；英文翻译表那几行（中文原文是词条名）不动，新文字另加英文词条。"""
    global s
    if '\n' in old:
        c = s.count(old)
        if c != n: sys.exit(f'[停止] 匹配 {c} 次（应为 {n}）：{old[:90]}')
        s = s.replace(old, new); return
    lines = s.split('\n'); c = sum(l.count(old) for l in lines if not _is_dict_line(l))
    if c != n: sys.exit(f'[停止] 匹配 {c} 次（应为 {n}）：{old[:90]}')
    s = '\n'.join(l if _is_dict_line(l) else l.replace(old, new) for l in lines)


# ---------- 1 路由页 ----------
rep('<span>路由与转换</span></button>', '<span>路由与可靠性</span></button>')
P1 = '一个对外模型由哪些渠道提供、谁先被选中，以及请求失败后怎么重试。单个渠道的优先级、权重、模型映射和请求转换，在渠道的编辑框里改。'
rep('<h2>路由与转换</h2><p>每个渠道的映射、优先级、权重和请求 / 响应转换一览；点「编辑」在这里直接改，和「渠道接入」用同一个编辑框。</p>', f'<h2>路由与可靠性</h2><p>{P1}</p>')
s, n = re.subn(r'\n        <h3 class="cs-h3">按渠道</h3>\n        <div class="tbl"><table class="cs-tbl cs-wide"><thead><tr><th>渠道</th><th>模型映射</th>.*?<tbody id="rtRoute"></tbody></table></div>\n        <div class="cs-empty" id="rtRoute0">.*?</div>', '', s, flags=re.S)
if n != 1: sys.exit(f'[停止] 按渠道表删除 {n} 处')
rep("$('#rtRoute').innerHTML=CHANNELS.map(", "if($('#rtRoute'))$('#rtRoute').innerHTML=CHANNELS.map(")
rep("$('#rtRoute0').hidden=CHANNELS.length>0;", "if($('#rtRoute0'))$('#rtRoute0').hidden=CHANNELS.length>0;")
P2 = '一个对外模型背后有哪些渠道、谁先被选中。优先级高的先用，同优先级按权重分流。点渠道名可以改它的优先级和权重。'
rep('<p class="cs-help">一个对外模型背后有哪些渠道、谁先被选中。优先级高的先用，同优先级按权重分流。</p>', f'<p class="cs-help">{P2}</p>')
rep("return esc(c.name)+'<span class=\"cs-sub mono\"> 优先级 '", "return '<button class=\"ac-link\" type=\"button\" data-rtroute=\"'+CHANNELS.indexOf(c)+'\">'+esc(c.name)+'</button><span class=\"cs-sub mono\"> 优先级 '")
rep("$('#rtRouteM0').hidden=M.length>0;", "$('#rtRouteM0').hidden=M.length>0;\n    $$('#rtRouteM [data-rtroute]').forEach(function(b){b.addEventListener('click',function(){rtCEopen(+b.getAttribute('data-rtroute'),'route')})});")
L1, L2 = '自动停用与恢复', '定期测试失败的渠道自动停用，恢复后自动启用'
rep('<span class="cs-lb">自动恢复与禁用</span><label class="f-chk"><input type="checkbox" name="auto"><span>测试失败自动禁用，恢复后自动启用</span></label>',
    f'<span class="cs-lb">{L1}</span><label class="f-chk"><input type="checkbox" name="auto"><span>{L2}</span></label>')
P3 = '这些是全局策略；单个渠道的优先级、权重和失败后自动停用，在渠道的编辑框里设。'
rep('<p class="cs-help">这些是全局策略；渠道上的优先级、权重、自动封禁是对单个渠道的设置。接口接入前，这里保存的值只在预览里生效。</p>\n        <p class="cs-help">智能路由（按任务把请求交给更便宜的模型）在规划中，定义见交接文档；现有映射和权重是静态规则。</p>',
    f'<p class="cs-help">{P3}</p>')
rep('title="全局请求重试次数，在「路由与转换」里改"', 'title="全局请求重试次数，在「路由与可靠性」里改"')
P4 = '同一个对外模型可以由多个渠道提供；谁先用、权重多少在「路由与可靠性」里看，在渠道编辑框里改。未设价的模型不能上架。价格在「定价」里改。'
rep('<p class="cs-help">同一个对外模型可以由多个渠道提供；谁先用、权重多少在「路由与转换」里设。未设价的模型不能上架。价格在「定价」里改。</p>', f'<p class="cs-help">{P4}</p>')
P5 = '登录注册、计费充值、安全限制、邮件和日志的全局开关都在这里改。渠道重试与自动停用在「路由与可靠性」，公司信息与 API 地址在官网后台。'
rep('<p>登录注册、计费充值、安全限制、邮件和日志的全局开关，都在这里改，不再跳回原后台。渠道重试与自动禁用在「路由与转换」，公司信息与 API 地址在官网后台。</p>', f'<p>{P5}</p>')
EN.update({'路由与可靠性': 'Routing & reliability', P1: 'Which channels serve each public model, which one is picked first, and how failed requests are retried. Per-channel priority, weight, model mapping and request transforms are edited in the channel editor.',
           P2: 'Which channels sit behind each public model and which is picked first. Higher priority goes first; equal priority is split by weight. Click a channel to change its priority and weight.',
           L1: 'Auto-disable and recover', L2: 'Disable channels that fail periodic tests and re-enable them on recovery', P3: 'These are global. Per-channel priority, weight and auto-disable on failure are set in the channel editor.',
           '全局请求重试次数，在「路由与可靠性」里改': 'Global retry count; change it under Routing & reliability',
           P4: 'One public model can be served by several channels; see order and weight under Routing & reliability and change them in the channel editor. Unpriced models cannot be listed. Prices are edited under Pricing.',
           P5: 'Global switches for sign-in, billing and top-up, security limits, email and logs. Channel retries and auto-disable are under Routing & reliability; company details and the API address are in the website admin.'})

# ---------- 2 定价 ----------
R1 = '个人用户：基础价 × 价格分组倍率，再按分时价打折；订了个人套餐的先扣套餐额度，扣法相同。'
R2 = '企业客户：设了合同价的模型按合同价，没设的按基础价；不乘价格分组倍率；分时价同样打折。'
rep('<div class="rt-tabs" role="tablist" id="rtPrTabs">', f'<div class="rt-rule"><b>怎么计价</b><p>{R1}</p><p>{R2}</p></div>\n        <div class="rt-tabs" role="tablist" id="rtPrTabs">')
rep('<th class="r">继承的组织</th>', '<th class="r">沿用基础价的企业</th>')
rep('个模型待发布，影响 <b id="rtPubO">0</b> 家继承的组织。', '个模型待发布，影响 <b id="rtPubO">0</b> 家沿用基础价的企业客户。')
rep("家继承的组织按新价计费。", "家沿用基础价的企业客户按新价计费。")
rep("'没有组织继承'", "'没有企业沿用基础价'")
T1 = '在绿电富余的时段给模型打折。时段有两种来源：手填的固定时段，对所有电站生效；或者跟随某座电站在「绿电时段」里发布的时段。改价写进审计日志。'
rep('<p class="cs-help rt-sh2">在绿电富余的时段给模型打折。时段来自「绿电时段」，计费写成 new-api 的按时段表达式；改价写进审计日志。</p>', f'<p class="cs-help rt-sh2">{T1}</p>')
rep('<form class="cs-newf" id="rtTodF" novalidate><select class="mk-sel" name="model" id="rtTodM" aria-label="模型"></select><input class="in mono cs-pr" name="from" placeholder="09:00" aria-label="开始时间" autocomplete="off"><input class="in mono cs-pr" name="to" placeholder="16:00" aria-label="结束时间" autocomplete="off"><input class="in mono cs-pr" name="pct" inputmode="decimal" placeholder="折扣 %" aria-label="折扣百分比" autocomplete="off">',
    '<form class="cs-newf" id="rtTodF" novalidate><select class="mk-sel" name="src" id="rtTodS" aria-label="时段来源"><option value="fixed">手填时段（所有电站）</option><option value="plant">跟随电站绿电时段</option></select><select class="mk-sel" name="model" id="rtTodM" aria-label="模型"></select><input class="in mono cs-pr" name="from" placeholder="09:00" aria-label="开始时间" autocomplete="off"><input class="in mono cs-pr" name="to" placeholder="16:00" aria-label="结束时间" autocomplete="off"><select class="mk-sel" name="plant" id="rtTodP" aria-label="电站" hidden><option value="">还没有发布绿电时段的电站</option></select><input class="in mono cs-pr" name="pct" inputmode="decimal" placeholder="按原价 %" aria-label="按原价的百分比" autocomplete="off">')
rep('<th>时段</th><th class="r">折扣</th><th class="r">基础 输出</th>', '<th>时段</th><th class="r">按原价</th><th class="r">基础 输出</th>')
T2 = '选模型（或全部模型）和时段，填按原价收的百分比。例：09:00–16:00 填 50，就是这段时间打 5 折。'
rep('<span>选一个模型和时段，填折扣。例：09:00–16:00 打 5 折。</span>', f'<span>{T2}</span>')
rep("tm.innerHTML=M.filter(function(m){return m.mkt>0}).map(function(m){return '<option value=\"'+m.id+'\">'+esc(m.name)+'</option>'}).join('');",
    "tm.innerHTML='<option value=\"*\">全部模型</option>'+M.filter(function(m){return m.mkt>0}).map(function(m){return '<option value=\"'+m.id+'\">'+esc(m.name)+'</option>'}).join('');")
rep("var m=byId[t.id]||{};return '<tr><td>'+esc(m.name||t.id)+'</td><td class=\"mono\">'+esc(t.from)+'–'+esc(t.to)+'</td>",
    "var m=byId[t.id]||{};return '<tr><td>'+esc(t.id==='*'?'全部模型':(m.name||t.id))+'</td><td class=\"mono\">'+(t.src==='plant'?esc(t.plant||'')+' 绿电时段':esc(t.from)+'–'+esc(t.to))+'</td>")
rep("if(!f.model.value){toast('先给模型设基础价。');return}if(!re.test(f.from.value.trim()))",
    "if(!f.model.value){toast('先给模型设基础价。');return}if(f.src&&f.src.value==='plant'){if(!f.plant.value){toast('还没有发布绿电时段的电站，先在「电站与时段 › 绿电时段」发布。');return}}else if(!re.test(f.from.value.trim()))")
rep("if(!(pc>0&&pc<100)){toast('折扣填 1 到 99 之间的百分比。');f.pct.focus();return}", "if(!(pc>0&&pc<100)){toast('按原价的百分比填 1 到 99，比如 50 就是打 5 折。');f.pct.focus();return}")
rep("RT_TOD.push({id:f.model.value,from:f.from.value.trim(),to:f.to.value.trim(),pct:pc});audit('新增分时价 '+((byId[f.model.value]||{}).name||'')",
    "RT_TOD.push({src:'fixed',id:f.model.value,from:f.from.value.trim(),to:f.to.value.trim(),pct:pc});audit('新增分时价 '+((f.model.value==='*'?'全部模型':(byId[f.model.value]||{}).name)||'')")
rep('<p class="cs-help rt-sh2">个人用户按月付费、每月得到一份额度；用完后按设置停用或转为按量计费。企业不适用，企业用合同价。订阅的扣费与续费用 new-api 的订阅功能承接，需开发。</p>', '<p class="cs-help rt-sh2">个人用户按月付费、每月得到一份额度；用完后按设置停用或转为按量计费。企业不适用，企业用合同价。</p>')
EN.update({'怎么计价': 'How pricing works', R1: 'Personal users: base price × price-group ratio, then the time-of-day discount; subscribers use their plan credit first, charged the same way.',
           R2: 'Business customers: contract price where one is set, base price otherwise; no price-group ratio; the time-of-day discount still applies.',
           '沿用基础价的企业': 'Businesses on base price', ' 家沿用基础价的企业客户。': ' businesses on base price.', '没有企业沿用基础价': 'No business on base price', T1: 'Discount models when green power is plentiful. Times either come from a fixed window you enter, for all plants, or follow the green-power hours a plant publishes. Price changes go to the audit log.',
           '手填时段（所有电站）': 'Fixed window (all plants)', '跟随电站绿电时段': "Follow a plant's green hours", '全部模型': 'All models', '还没有发布绿电时段的电站': 'No plant has published green hours', '按原价 %': '% of base price', '按原价': '% of base',
           T2: 'Pick a model (or all models) and a window, then the % of the base price to charge. Example: 09:00–16:00 at 50 means half price in that window.',
           '还没有发布绿电时段的电站，先在「电站与时段 › 绿电时段」发布。': 'No plant has published green hours yet; publish them under Plants & hours › Green hours first.',
           '按原价的百分比填 1 到 99，比如 50 就是打 5 折。': 'Enter 1–99 as a % of the base price; 50 means half price.',
           '个人用户按月付费、每月得到一份额度；用完后按设置停用或转为按量计费。企业不适用，企业用合同价。': 'Personal users pay monthly for a monthly credit; when it runs out they are paused or moved to pay-as-you-go, as set. Not for businesses, which use contract prices.'})

# ---------- 3 渠道编辑框 ----------
rep('<span class="cs-lb">自动封禁</span>', '<span class="cs-lb">自动停用</span>')
rep("KST={1:'启用',2:'手动停用',3:'自动禁用'}", "KST={1:'启用',2:'手动停用',3:'自动停用'}")
rep('<th>禁用原因</th><th>禁用时间</th>', '<th>停用原因</th><th>停用时间</th>')
rep("?'已保存的密钥在平台里；接口接入后逐把列出状态、禁用原因和时间。", "?'已保存的密钥在平台里；接口接入后逐把列出状态、停用原因和时间。")
S1, S2 = '第三方厂商的渠道不挂电站；自营节点是我们部署在电站侧的一体机，产地卡和绿电统计按它所在的电站算。', '还没有算力节点，先在「电站与时段」新增电站和节点。'
rep('<div class="cs-f"><label for="rtCEn">名称 *</label><input class="in" id="rtCEn" name="name" autocomplete="off"></div>',
    '<div class="cs-f"><label for="rtCEn">名称 *</label><input class="in" id="rtCEn" name="name" autocomplete="off"></div>\n'
    '                <div class="cs-f"><label for="rtCEsrc">渠道来源</label><select class="mk-sel" id="rtCEsrc" name="src"><option value="vendor">第三方厂商（上游 API）</option><option value="self">自营节点（电站侧一体机）</option></select>'
    f'<p class="cs-help">{S1}</p></div>\n'
    f'                <div class="cs-f" id="rtCEnodeF" hidden><label for="rtCEnode">算力节点</label><select class="mk-sel" id="rtCEnode" name="node" disabled><option value="">还没有算力节点</option></select><p class="cs-help">{S2}</p></div>')
EN.update({'自动停用': 'Auto-disable', '停用原因': 'Reason', '停用时间': 'Disabled at', '已保存的密钥在平台里；接口接入后逐把列出状态、停用原因和时间。上面填的新密钥保存后出现在这里。': 'Saved keys live on the platform; once connected each key is listed with status, reason and time. New keys entered above appear here after saving.',
           '渠道来源': 'Channel source', '第三方厂商（上游 API）': 'Third-party vendor (upstream API)', '自营节点（电站侧一体机）': 'Our node (appliance at a plant)', S1: 'Vendor channels are not tied to a plant. Our nodes are appliances we run beside plants; origin cards and green-power totals use their plant.',
           '算力节点': 'Compute node', '还没有算力节点': 'No compute nodes yet', S2: 'No compute nodes yet; add plants and nodes under Plants & hours first.', '自营节点': 'Our node'})

# ---------- 4 电站 ----------
G1 = '接入的电站、算力节点与用电来源，是订单产地卡和分时价「跟随电站」的数据来源。每座电站挂在「企业客户」里对应的电站合作方名下。打开「官网展示」的电站会出现在官网「电站合作」页（与官网后台打通后生效）。'
rep('<p class="bt-lede">接入的电站、算力节点与用电来源，是订单产地卡和「绿电折扣」的数据来源。官网「电站合作」页也读这张表，打开「官网展示」的才显示；官网后台原来那张电站表停用。</p>', f'<p class="bt-lede">{G1}</p>')
rep('<thead><tr><th>电站</th><th>能源类型</th><th>所在地</th><th>装机</th><th>算力节点</th><th>绑定渠道</th><th>状态</th><th>官网展示</th></tr></thead>',
    '<thead><tr><th>电站</th><th>所属合作方</th><th>能源类型</th><th>所在地</th><th>装机</th><th>算力节点</th><th>挂载的自营渠道</th><th>状态</th><th>官网展示</th></tr></thead>')
G2 = '自营渠道挂到算力节点，节点挂到电站；第三方厂商的渠道不挂电站。电站离线时，挂在它下面的自营渠道自动停用并告警。'
rep('<p>每个渠道挂到一个节点，每个节点挂到一个电站。电站离线时，对应渠道自动停用并告警。</p>', f'<p>{G2}</p>')
G3 = '按电站发布计划绿电时段，可以提前公示，变更留痕。分时价选「跟随电站绿电时段」时读这张表，绿电批量任务也按它排期。'
rep('<p class="bt-lede">按电站发布计划绿电时段，可以提前公示，变更留痕。分时价和批量任务都读这张表。</p>', f'<p class="bt-lede">{G3}</p>')
EN.update({G1: "Plants, compute nodes and power sources: the data behind order origin cards and plant-following time-of-day prices. Each plant sits under its plant partner in Business customers. Plants with Show on website switched on appear on the website's Plant partnership page once the website admin is connected.",
           '所属合作方': 'Partner', '挂载的自营渠道': 'Our channels on it', G2: 'Our channels attach to compute nodes, nodes to plants; vendor channels attach to no plant. When a plant goes offline, our channels under it are disabled and an alert is raised.',
           G3: "Publish planned green-power hours per plant, ahead of time, with changes logged. Time-of-day prices set to follow a plant read this table, and green batch jobs are scheduled by it."})

# ---------- 5 组织 → 企业（超管界面，审计日志条目不动） ----------
rep('data-go="rt-orgs">← 组织</button>', 'data-go="rt-orgs">← 企业客户</button>')
O1 = '绑定的渠道决定这家企业能用哪些模型。设专属价不会自动授予访问；沿用基础价也不代表能用全部模型。'
rep('绑定的渠道决定这家组织能用哪些模型。设专属价不会自动授予访问；继承基础价也不代表能用全部模型。', O1)
O2 = '只列这家企业绑定渠道里的模型。留空 = 沿用基础价；填了 = 合同价，只对这家企业生效。「恢复继承」是明确动作，空值不是零价。'
rep('只列这家组织绑定渠道里的模型。留空 = 继承 C 端基础价；填了 = 覆盖，只对这家组织生效。「恢复继承」是明确动作，空值不是零价。', O2)
rep('>保存组织定价</button>', '>保存合同价</button>')
rep('为这家组织新增合约', '为这家企业新增合约')
rep('<b>冻结组织</b><p class="cs-help">冻结后这家组织所有成员的 API Key 立即停用，余额保留。</p>', '<b>冻结企业账户</b><p class="cs-help">冻结后这家企业所有成员的 API Key 立即停用，余额保留。</p>')
rep('id="rtOFreeze">冻结组织</button>', 'id="rtOFreeze">冻结企业账户</button>')
rep("$('#rtOFreeze').textContent=o.frozen?'解冻组织':'冻结组织';", "$('#rtOFreeze').textContent=o.frozen?'解冻企业账户':'冻结企业账户';")
rep("this.textContent=o.frozen?'解冻组织':'冻结组织';", "this.textContent=o.frozen?'解冻企业账户':'冻结企业账户';")
rep('合同价开通后在组织详情里按模型覆盖。', '合同价开通后在企业详情里按模型设置。')
rep('>关联组织账户</label>', '>关联企业账户</label>')
rep('改价、改额度、开通组织、入账、改设置。', '改价、改额度、开通企业账户、入账、改设置。', 2)
EN.update({'← 企业客户': '← Business customers', O1: 'Bound channels decide which models this business can use. A special price does not grant access; staying on the base price does not mean every model is available.',
           O2: "Only models on this business's bound channels are listed. Blank = base price; filled = contract price for this business only. Restore inheritance is an explicit action; blank is not a zero price.",
           '保存合同价': 'Save contract prices', '为这家企业新增合约': 'New contract for this business', '冻结企业账户': 'Freeze business account', '解冻企业账户': 'Unfreeze business account',
           '冻结后这家企业所有成员的 API Key 立即停用，余额保留。': "Freezing disables every member's API keys at once; the balance is kept.",
           '合同价开通后在企业详情里按模型设置。': 'Contract prices are set per model in the business detail after opening.', '关联企业账户': 'Linked business account',
           '员工的每次操作：改价、改额度、开通企业账户、入账、改设置。': 'Every staff action: price and allowance changes, business accounts opened, bank entries, settings.',
           '管理员的每次操作：改价、改额度、开通企业账户、入账、改设置。': 'Every admin action: price and allowance changes, business accounts opened, bank entries, settings.'})

# ---------- 6 日志、模型资料 ----------
rep('<p>接入后读取 new-api 的全站使用日志，可以导出 CSV。</p>', '<p>接入后读取平台的全站使用日志，可以导出 CSV。</p>')
rep('<p>接入后读取 new-api 的任务日志：图片、视频、音频和批量任务，失败的可以看原因。</p>', '<p>接入后读取平台的任务日志：图片、视频、音频和批量任务，失败的可以看原因。</p>')
rep('id="rtMdSync">同步资料</button>', 'id="rtMdSync" title="按上游更新模型的名称、能力和上下文">更新模型资料</button>')
rep("toast('同步资料要接 new-api 的同步接口；接好后按上游更新名称、能力和上下文。')", "toast('接入平台后，按上游更新模型的名称、能力和上下文。')")
EN.update({'接入后读取平台的全站使用日志，可以导出 CSV。': 'Reads the platform usage log once connected, with CSV export.', '接入后读取平台的任务日志：图片、视频、音频和批量任务，失败的可以看原因。': 'Once connected this reads platform task logs: image, video, audio and batch jobs, with failure reasons.',
           '更新模型资料': 'Update model details', '按上游更新模型的名称、能力和上下文': 'Update names, capabilities and context from upstream', '接入平台后，按上游更新模型的名称、能力和上下文。': 'Once connected, model names, capabilities and context are updated from upstream.'})

# ---------- 样式与脚本 ----------
CSS = '''
<style id="relay-logic-fix-css">
/* 超管中转逻辑整理（2026-10-16）：定价页的计价规则框 */
.rt-rule{display:grid;gap:4px;margin:0 0 18px;padding:14px 16px;border:1px solid var(--line);border-radius:14px;background:rgba(255,255,255,.72)}
.rt-rule b{font:500 13px var(--sans);color:var(--ink)}
.rt-rule p{margin:0;font-size:13.5px;line-height:1.6;color:var(--ink-70)}
</style>
'''
k = s.rindex('</head>'); s = s[:k] + CSS + s[k:]
JS = r'''
  /* ======== 超管中转逻辑整理（2026-10-16）：渠道来源（第三方 / 自营节点）、分时价时段来源 ======== */
  (function(){
    var f=$('#rtCEF'); if(!f||!$('#rtCEsrc')) return;
    function srcSync(){var self=f.src.value==='self';$('#rtCEnodeF').hidden=!self}
    $('#rtCEsrc').addEventListener('change',srcSync);
    var _open=rtCEopen; rtCEopen=function(i,tab){_open(i,tab);var c=i>=0?CHANNELS[i]:null;f.src.value=(c&&c.src)||'vendor';f.node.value=(c&&c.node)||'';srcSync()};
    f.addEventListener('submit',function(){var d=rtCEs;if(!d)return;var src=f.src.value,node=f.node.value,i=d.i;
      setTimeout(function(){if(!$('#rtCE').hidden)return;var c=i>=0?CHANNELS[i]:CHANNELS[CHANNELS.length-1];if(!c)return;c.src=src;c.node=src==='self'?node:'';rootRender()},0)},true);
    var _cr=rtChRender; rtChRender=function(){_cr();$$('#rtChList .rt-ccard').forEach(function(card){var b=card.querySelector('[data-cedit]'),ft=card.querySelector('.ft');if(!b||!ft)return;var c=CHANNELS[+b.getAttribute('data-cedit')];if(c&&c.src==='self')ft.insertAdjacentHTML('beforeend','<span class="rt-gtag">自营节点</span>')});rtTx()};
    var ts=$('#rtTodS'); if(ts) ts.addEventListener('change',function(){var p=ts.value==='plant',tf=$('#rtTodF');tf.from.hidden=p;tf.to.hidden=p;$('#rtTodP').hidden=!p});
  })();
'''
rep("  window.addEventListener('hashchange',route); route();", JS + "  window.addEventListener('hashchange',route); route();")
rep('  syncAuthLocale(); applyLang();', '  (function(S){for(var k in S) if(!(k in I18N)) I18N[k]=S[k]})(' + json.dumps(EN, ensure_ascii=False) + ');  /* 超管中转逻辑整理 */\n  I18N["自动停用"]="Auto-disable";I18N["渠道来源"]="Channel source";  /* 旧词条里有不同译法，统一 */\n  syncAuthLocale(); applyLang();')
open(OUT, 'w', encoding='utf8').write(s)
print('done:', OUT, len(EN), 'EN entries')
