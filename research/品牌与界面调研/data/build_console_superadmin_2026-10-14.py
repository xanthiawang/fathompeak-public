"""超级管理员版后台（Zixin 2026-10-14："超管版也做一个"；晚：线框感重 → 改用客户控制台概览同一套 Dia 组件；再按《超管后台对标_2026-10-14.md》补资金流水、退款、对账与报表、绿电时段、告警、公告与内容、管理员与权限，并改正分时价说明）。用客户控制台同一套外壳、字体与组件，不重画 new-api 的密集表格。
叠加顺序：线上 → build_full_supplement → build_console_backend（含 #console-preview-super 入口与花体恢复）→ 本脚本 → build_console_role_versions。
菜单：运营概览 / 平台（渠道、模型与定价、用户、组织、兑换码）/ 沐仞运营（认证审核、对公入账、开票处理、电站与节点、分时价、批量任务）
     / 系统（菜单展示、系统设置、全站日志、审计日志）。每页右上角标「new-api 现成」或「需开发」，与《后台架构》一致。
数据：全部空状态；只有「模型与定价」「分时价」用已有出处的数（平台模型目录输出价、2026-10-08 报价单刊例价，后者标待公司确认）。
用法：python3 -I build_console_superadmin_2026-10-14.py <输入 html> <输出 html>
"""
import json, sys

LIVE = '--live' in sys.argv  # 上线版：不放报价单里的输入 / 缓存价和闲时 / 忙时钟点（报价单注明为机密）
args = [x for x in sys.argv[1:] if not x.startswith('--')]
SRC, OUT = args[0], args[1]
s = open(SRC, encoding='utf8').read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: sys.exit(f'[停止] 匹配 {c} 次（应为 {n}）：{old[:80]}')
    s = s.replace(old, new)


def tbc(t='待公司确认'):
    return f'<span class="tbc">{t}</span>'


def ico(d):
    return f'<svg viewBox="0 0 20 20" aria-hidden="true"><path d="{d}" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'


# Dia 组件（与客户控制台概览同一套）：bt-pg 页框、bt-hd 大标题、bt-lede、bt-flt 白玻璃筛选、bt-tw/bt-tbl 深色渐变表头、
# bt-empty 排线插画空状态、bt-mini 玻璃卡、bt-check 待办、bt-panel 晨昏色卡；标签用 bt-tag（不用蓝，蓝只给链接）
TAG = {'api': '<span class="bt-tag ad-api">new-api 现成</span>', 'dev': '<span class="bt-tag g ad-dev">需开发</span>',
       'mix': '<span class="bt-tag ad-api">new-api 现成</span><span class="bt-tag g ad-dev">需开发</span>'}
QI = '<svg viewBox="0 0 16 16" aria-hidden="true"><circle cx="7" cy="7" r="5" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M11 11l3.5 3.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>'


def q(ph):
    return f'<label class="bt-q">{QI}<input type="search" placeholder="{ph}" aria-label="{ph}" autocomplete="off" spellcheck="false"></label>'


def sel(label, opts):
    return f'<label class="bt-sel"><span>{label}</span><select aria-label="{label}">' + ''.join(f'<option>{o}</option>' for o in opts) + '</select></label>'


def chips(labels):
    return '<div class="bt-chips ad-chips" role="group">' + ''.join(f'<button class="bt-chip{" on" if i == 0 else ""}" type="button" aria-pressed="{"true" if i == 0 else "false"}">{l}</button>' for i, l in enumerate(labels)) + '</div>'


def flt(*items):
    return '<div class="bt-flt">' + ''.join(items) + '</div>'


def tbl(heads, tbody_id=''):
    R = ' class="r"'
    th = ''.join('<th' + (R if h.startswith('>') else '') + '>' + h.lstrip('>') + '</th>' for h in heads)
    tid = (' id=' + json.dumps(tbody_id)) if tbody_id else ''
    return f'<div class="bt-tw"><table class="bt-tbl"><thead><tr>{th}</tr></thead><tbody{tid}></tbody></table></div>'


def empty(art, title, sub, acts=''):
    return (f'<div class="bt-empty"><span class="bt-ill bt-collage" data-art="{art}" aria-hidden="true"></span><b>{title}</b><p>{sub}</p>'
            + (f'<div class="bt-acts">{acts}</div>' if acts else '') + '</div>')


def b(label, pri=False, extra=''):
    return f'<button class="bt-btn{" pri" if pri else ""}" type="button" data-ad-act{extra}>{label}</button>'


def pane(p, title, desc, tag, body, act=''):
    return (f'      <div class="cs-p" data-p="{p}">\n        <div class="bt-pg">\n'
            f'          <div class="bt-hd"><h1>{title}</h1><div class="ad-hr">{TAG[tag]}{act}</div></div>\n'
            f'          <p class="bt-lede">{desc}</p>\n'
            f'          {body}\n        </div>\n      </div>\n')


def form(title, fields, btn):
    return ('<div class="bt-mini ad-form"><b>' + title + '</b><form class="ad-fr" novalidate data-ad-form>' +
            ''.join(f'<input class="in{" mono" if m else ""}" placeholder="{ph}" aria-label="{ph}" autocomplete="off"{" inputmode=" + json.dumps(m) if m else ""}>' for ph, m in fields) +
            f'<button class="bt-btn pri" type="submit">{btn}</button></form></div>')


PANES = ''
PANES += pane('ad-home', '运营概览', '全平台的用户、请求、消耗与待处理事项。', 'mix',
              '<div class="ad-kpi">' + ''.join(f'<div class="bt-mini"><span class="ad-k">{k}</span><b class="ad-n mono">--</b><span class="ad-s">{s2}</span></div>' for k, s2 in
                                             [('用户', '个人 -- · 企业 --'), ('今日请求', '较昨日 --'), ('今日消耗', '¥ · 较昨日 --'), ('可用渠道', '共 -- 个')]) + '</div>\n'
              '          <h2 class="ad-h2">待处理</h2>\n'
              '          <ol class="bt-check ad-todo">'
              '<li><i aria-hidden="true"></i><div><b>认证审核</b><p>教育认证、实名认证、企业认证。</p><span class="cs-st">-- 条</span></div><button class="bt-btn" type="button" data-ad-go="ad-review">去处理</button></li>'
              '<li><i aria-hidden="true"></i><div><b>对公入账</b><p>核对转账凭证，给账户加余额。</p><span class="cs-st">-- 笔</span></div><button class="bt-btn" type="button" data-ad-go="ad-bank">去处理</button></li>'
              '<li><i aria-hidden="true"></i><div><b>开票申请</b><p>处理客户提交的开票申请。</p><span class="cs-st">-- 张</span></div><button class="bt-btn" type="button" data-ad-go="ad-inv">去处理</button></li></ol>\n'
              '          <div class="bt-panel"><div class="bt-panel-tx"><b>电站与节点</b><p>接入的电站、算力节点与用电来源，是订单产地卡、日志里「绿电折扣」和绿电时段价的数据来源。接入电站与节点系统后，这里显示各节点状态。</p></div>'
              '<span class="bt-panel-ill bt-collage" data-art="solar" aria-hidden="true"></span></div>\n'
              '          <p class="ad-fine">数字接入平台数据后显示。用户、请求、消耗与渠道来自 new-api 数据看板；待处理事项来自沐仞新增的运营服务。</p>')
PANES += pane('ad-ch', '渠道', '上游模型供应商与自有节点的接入，按优先级和权重分流。', 'api',
              flt(q('查找渠道'), sel('状态', ['全部', '已启用', '已停用']), sel('类型', ['全部', 'OpenAI 兼容', 'Gemini', '自有节点'])) + '\n          ' +
              tbl(['ID', '名称', '分组', '类型', '状态', '>响应时间', '>已用 / 剩余', '>优先级', '>权重']) + '\n          ' +
              empty('boxes', '还没有接入渠道数据', '接入后直接读取 new-api 的渠道列表：测速、启停、余额与分流权重。', b('新增渠道')), b('新增渠道', True))
PANES += pane('ad-models', '模型与定价', '模型上架、计费方式与价格。客户控制台的模型目录与定价页都读这里。', 'api',
              tbl(['模型', '厂商', '计费方式', '>输入', '>缓存读取', '>输出', '时段', '状态'], 'adModels') + '\n          ' +
              ('<p class="ad-fine">单位 ¥ / 百万词元。输出价来自平台模型目录；输入与缓存价待平台同步。</p>' if LIVE else '<p class="ad-fine">单位 ¥ / 百万词元。输出价来自平台模型目录；输入与缓存价来自 2026-10-08 报价单刊例价。' + tbc('报价单注明为商业机密，公开前请公司确认') + '</p>'), b('新增模型', True))
PANES += pane('ad-users', '用户', '全部个人、教育与企业账户：额度、分组、角色与启停。', 'api',
              flt(q('查找用户'), sel('类型', ['全部', '个人', '教育', '企业']), sel('实名', ['全部', '已认证', '未认证']), sel('状态', ['全部', '已启用', '已冻结', '已停用'])) + '\n          ' +
              tbl(['ID', '用户', '类型', '实名', '状态', '>可用额度', '分组', '邀请人', '注册时间']) + '\n          ' +
              empty('key', '还没有用户数据', '接入后读取 new-api 的用户列表，可以改额度和分组，冻结或停用账户，冻结原因必填。') + '\n          <p class="ad-fine">未实名的账户只能用赠送额度，用完即停。' + tbc() + '</p>')
PANES += pane('ad-orgs', '组织', '开通企业组织并指定管理员；管理员再添加自己的成员。', 'dev',
              form('开通组织', [('组织名称', ''), ('管理员邮箱', '')], '开通') + '\n          ' +
              tbl(['组织', '管理员', '>成员', '价格分组', '合同价有效期', '>钱包余额', '>本月消费', '>预算上限', '企业认证', '状态']) + '\n          ' +
              empty('sign', '还没有组织', '开通后，组织、成员数、余额和本月消费显示在这里。合同价通过「价格分组」绑定并设有效期；超预算可以自动冻结，冻结原因必填。') +
              '\n          <p class="ad-fine">' + tbc('上游 new-api 没有组织，只有分组；开发说的组织管理需确认是否已在 fork 里') + '</p>')
PANES += pane('ad-redeem', '兑换码', '批量生成兑换码，用于活动赠送和代金券。', 'api',
              form('生成兑换码', [('名称', ''), ('面额（¥）', 'decimal'), ('数量', 'numeric')], '生成') + '\n          ' +
              tbl(['名称', '兑换码', '>面额', '状态', '创建时间', '兑换账户']) + '\n          ' +
              empty('tag', '还没有兑换码', '生成后，兑换码与使用情况显示在这里。'))
PANES += pane('ad-review', '认证审核', '教育认证、实名认证与企业认证的人工审核。', 'dev',
              chips(['教育认证', '实名认证', '企业认证']) + '\n          ' +
              tbl(['提交时间', '账户', '类型', '材料', '状态']) + '\n          ' +
              empty('book', '没有待审核的申请', '客户提交学生证、在读证明或企业材料后显示在这里。') +
              '\n          <p class="ad-fine">' + tbc('实名若接第三方认证服务，可以不设人工审核') + '</p>')
PANES += pane('ad-bank', '对公入账', '企业对公转账按「录款 → 复核 → 入账」处理：财务录入银行流水，第二个人复核后才给账户加余额。', 'mix',
              '<ol class="bt-check ad-steps"><li><i aria-hidden="true"></i><div><b>录款</b><p>录入到账日期、付款户名、金额和银行流水号，上传回单。</p></div></li>'
              '<li><i aria-hidden="true"></i><div><b>复核</b><p>另一位财务核对回单与流水，可以退回。</p></div></li>'
              '<li><i aria-hidden="true"></i><div><b>入账</b><p>给对应账户或组织加余额，写进资金流水；可以撤销并留痕。</p></div></li></ol>\n          ' +
              form('录入到账', [('到账日期', ''), ('付款户名', ''), ('金额（¥）', 'decimal'), ('银行流水号', '')], '录入') + '\n          ' +
              chips(['待复核', '已入账', '已退回', '全部']) + '\n          ' +
              tbl(['到账日期', '付款户名', '>金额', '流水号', '对应账户', '录入人', '复核人', '状态']) + '\n          ' +
              empty('tag', '没有待复核的转账', '财务录款后显示在这里，复核通过即入账。付款户名和实名主体不一致时，需要代付协议。'))
PANES += pane('ad-inv', '开票处理', '处理客户的开票申请，上传发票后客户可以下载。', 'dev',
              chips(['待处理', '已开票', '已红冲', '全部']) + '\n          ' +
              tbl(['申请时间', '账户', '抬头', '类型', '>金额', '状态']) + '\n          ' +
              empty('book', '没有开票申请', '客户在控制台「发票」里提交后显示在这里。') +
              '\n          <p class="ad-fine">' + tbc('待公司确认：按消费还是按充值开票、开票时限') + '</p>')
PANES += pane('ad-plants', '电站与节点', '接入的电站、算力节点与用电来源，是订单产地卡和「绿电折扣」的数据来源。', 'dev',
              tbl(['电站', '能源类型', '所在地', '装机', '算力节点', '绑定渠道', '状态', '接入时间']) + '\n          ' +
              empty('solar', '还没有电站与节点数据', '每个渠道挂到一个节点，每个节点挂到一个电站。电站离线时，对应渠道自动停用并告警。', b('新增电站')), b('新增电站', True))
if not LIVE:
    DAY = ''.join(f'<i class="{"idle" if (h >= 22 or h < 8) else "busy"}" title="{h}:00"></i>' for h in range(24))
    PANES += pane('ad-tod', '分时价', '按时段给模型定价：闲时 / 忙时，以及按电站富余绿电的时段价。保存后写成 new-api 的按时段表达式计费。', 'mix',
                  '<div class="bt-mini ad-day"><b>DeepSeek-V4-Pro · 全天</b><div class="ad-bar">' + DAY + '</div><div class="ad-ax"><span>0:00</span><span>6:00</span><span>12:00</span><span>18:00</span><span>24:00</span></div>'
                  '<p><span class="ad-lg idle"></span>闲时 22:00–08:00 · 输出 ¥13.50　<span class="ad-lg busy"></span>忙时 08:00–22:00 · 输出 ¥27.00</p></div>\n          ' +
                  '<div class="bt-tw"><table class="bt-tbl"><thead><tr><th>模型</th><th>时段</th><th class="r">输入</th><th class="r">缓存读取</th><th class="r">输出</th><th>来源</th></tr></thead><tbody>'
                  '<tr><td>DeepSeek-V4-Pro</td><td class="mono">闲时 22:00–08:00</td><td class="mono r">¥4.50</td><td class="mono r">¥0.45</td><td class="mono r">¥13.50</td><td>报价单</td></tr>'
                  '<tr><td>DeepSeek-V4-Pro</td><td class="mono">忙时 08:00–22:00</td><td class="mono r">¥9.00</td><td class="mono r">¥0.90</td><td class="mono r">¥27.00</td><td>报价单</td></tr>'
                  '<tr><td>全部模型</td><td>绿电时段</td><td class="mono r">--</td><td class="mono r">--</td><td class="mono r">--</td><td>规划中</td></tr></tbody></table></div>\n'
                  '          <p class="ad-fine">计费用 new-api 的表达式定价（rc.37 起支持按小时、星期，含跨夜时段），这里做编辑与全天预览；改价写进审计日志。时段与价格来自 2026-10-08 报价单。' + tbc() + '</p>', b('新增时段', True))
else:
    PANES += pane('ad-tod', '分时价', '按时段给模型定价：闲时 / 忙时，以及按电站富余绿电的时段价。保存后写成 new-api 的按时段表达式计费。', 'mix',
                  tbl(['模型', '时段', '>输入', '>缓存读取', '>输出', '状态']) + '\n          ' +
                  empty('solar', '还没有配置分时价', '配置后，每个模型的时段与价格显示在这里，并预览全天价格。') +
                  '\n          <p class="ad-fine">计费用 new-api 的表达式定价（rc.37 起支持按小时、星期，含跨夜时段），这里做编辑与全天预览；改价写进审计日志。</p>', b('新增时段', True))
PANES += pane('ad-batch', '批量任务', '客户提交的绿电批量任务：排队、执行时段与完成情况。', 'dev',
              tbl(['提交时间', '账户', '模型', '>请求数', '计划时段', '状态']) + '\n          ' +
              empty('boxes', '还没有批量任务', '批量接口开发完成后，客户提交的任务显示在这里。'))

# ---------- 2026-10-14 晚：按《超管后台对标》补的页面 ----------
PANES += pane('ad-ledger', '资金流水', '每一笔钱的进出：充值、赠送、消费、退款、人工调整分开记，带单号、操作人和变动后余额。', 'dev',
              flt(q('按账户或单号查找'), sel('类型', ['全部', '充值', '赠送', '消费', '退款', '人工调整']), sel('时间', ['本月', '上月', '近 90 天'])) + '\n          ' +
              tbl(['时间', '账户', '类型', '>金额', '>变动后余额', '单号', '操作人', '备注']) + '\n          ' +
              empty('tag', '还没有资金流水', '对公入账、兑换码、退款和每次调用扣费都会在这里逐笔记账，赠送额度单独标记并可设过期。'), b('导出 CSV', True))
PANES += pane('ad-refund', '退款', '退款时同时作废对应额度；已开发票的先红冲，再退款。', 'dev',
              chips(['待处理', '已退款', '已拒绝', '全部']) + '\n          ' +
              tbl(['申请时间', '账户', '原充值单', '>退款金额', '>作废额度', '关联发票', '状态']) + '\n          ' +
              empty('tag', '没有退款申请', '客户申请或运营发起的退款显示在这里。'), b('发起退款', True))
PANES += pane('ad-report', '对账与报表', '按月生成对账单，看充值、赠送、消耗和余额负债；按渠道核对上游成本与毛利。', 'dev',
              '<div class="ad-kpi">' + ''.join(f'<div class="bt-mini"><span class="ad-k">{k}</span><b class="ad-n mono">--</b><span class="ad-s">{s2}</span></div>' for k, s2 in
                                             [('本月充值', '¥'), ('本月赠送', '¥'), ('本月消耗', '¥'), ('余额负债', '全部账户余额合计')]) + '</div>\n'
              '          <h2 class="ad-h2">月度对账单</h2>\n          ' +
              tbl(['月份', '组织 / 账户', '>充值', '>消耗', '>期末余额', '状态']) + '\n          ' +
              empty('book', '还没有对账单', '每月按组织、成员和 API Key 生成上月对账单，可以导出发给客户。') +
              '\n          <h2 class="ad-h2">上游成本</h2>\n          ' +
              tbl(['渠道', '>我们记的成本', '>上游账单', '>差额', '>毛利率']) + '\n          ' +
              empty('boxes', '还没有上游账单', '导入上游账单后，按渠道核对成本与毛利。'), b('导出', True))
PANES += pane('ad-hours', '绿电时段', '按电站发布计划绿电时段，可以提前公示，变更留痕。分时价和批量任务都读这张表。', 'dev',
              flt(sel('电站', ['全部电站']), sel('时间', ['本周', '下周', '本月'])) + '\n          ' +
              tbl(['电站', '日期', '计划绿电时段', '来源', '发布人', '状态']) + '\n          ' +
              empty('solar', '还没有发布绿电时段', '时段要来自电站的真实计量与预测，不能用估算值。'), b('发布时段', True))
RULES = [('渠道连续失败或被自动停用', '渠道测速失败、余额耗尽时提醒运营'), ('用户余额低于阈值', '按账户设置的预警线'), ('组织预算到达提醒比例', '75% / 90% / 100%，超预算可自动冻结'),
         ('待办超时', '认证审核、对公入账、开票超过 24 小时未处理'), ('电站离线', '自动停用对应渠道，并通知运营')]
PANES += pane('ad-alerts', '告警', '出问题时主动叫人：推送到运营群、邮箱或 Webhook。', 'mix',
              '<div class="ad-mods">' + ''.join(f'<div class="bt-mini ad-mod"><div><b>{a}</b><span>{b2}</span></div><label class="ad-sw"><input type="checkbox" checked data-ad-menu aria-label="{a}"><span></span></label></div>' for a, b2 in RULES) + '</div>\n'
              '          <div class="bt-flt ad-chans"><span class="ad-k">推送到</span>' + ''.join(f'<button class="bt-chip{" on" if i == 0 else ""}" type="button">{c}</button>' for i, c in enumerate(['邮件', 'Webhook', 'Bark', 'Gotify'])) + '</div>\n'
              '          <h2 class="ad-h2">最近告警</h2>\n          ' +
              tbl(['时间', '告警', '对象', '推送到', '状态']) + '\n          ' +
              empty('sign', '最近没有告警', '触发的告警和处理状态显示在这里。'))
PANES += pane('ad-content', '公告与内容', '站内公告、控制台常见问答和首页内容。', 'api',
              '<div class="ad-mods">' + ''.join(f'<div class="bt-mini ad-set"><b>{a}</b><p>{b2}</p><button class="bt-a" type="button" data-ad-act>{c} →</button></div>' for a, b2, c in
                                             [('站内公告', '维护通知、模型上新与调价，显示在客户控制台概览和通知铃里。', '发布公告'), ('常见问答', '客户控制台概览里的常见问题。', '编辑问答'),
                                              ('模型下线通知', '提前通知用到该模型的客户，并给出替代模型。', '新建通知'), ('首页与关于', '控制台首页文案与关于页。', '在 new-api 中编辑')]) + '</div>')
PERMS = [('渠道与模型', 1, 1, 0, 0), ('改价（模型价、分时价）', 1, 1, 0, 0), ('用户与额度', 1, 1, 0, 0), ('开通、冻结组织', 1, 1, 0, 0), ('认证审核', 1, 1, 0, 0),
         ('对公入账（录款 / 复核）', 1, 0, 1, 0), ('开票与退款', 1, 0, 1, 0), ('系统设置与菜单', 1, 0, 0, 0), ('查看日志与报表', 1, 1, 1, 1)]
PANES += pane('ad-admins', '管理员与权限', '按职责分权：运营管渠道、价格和客户，财务管入账、开票和退款，只读账号只能看。', 'mix',
              '<div class="bt-tw"><table class="bt-tbl ad-perm"><thead><tr><th>权限</th><th>超级管理员</th><th>运营</th><th>财务</th><th>只读</th></tr></thead><tbody>' +
              ''.join('<tr><td>' + n + '</td>' + ''.join(f'<td>{"✓" if v else "—"}</td>' for v in vs) + '</tr>' for n, *vs in PERMS) + '</tbody></table></div>\n'
              '          <h2 class="ad-h2">管理员</h2>\n          ' +
              tbl(['管理员', '角色', '两步验证', '最近登录', '状态']) + '\n          ' +
              empty('key', '还没有其他管理员', '添加后，对方用工作邮箱登录运营后台，第一次登录要绑定两步验证。'), b('添加管理员', True))
MENU = [('概览', 'lock', '全部'), ('模型 API', 'on', '全部'), ('在线试用', 'off', '全部'), ('探索', 'on', '全部'), ('API Key', 'lock', '全部'), ('使用日志', 'lock', '全部'),
        ('用量分析', 'on', '全部'), ('订单与产地卡', 'on', '全部'), ('绿电批量任务', 'off', '全部'), ('成员', 'on', '企业管理员'), ('账单分摊', 'on', '企业管理员'),
        ('钱包与账单', 'lock', '全部'), ('发票', 'on', '个人 · 企业管理员'), ('实名认证', 'on', '个人 · 企业管理员'), ('通用设置', 'lock', '全部'), ('安全与访问', 'lock', '全部')]
cards = ''.join(f'<div class="bt-mini ad-mod"><div><b>{n}</b><span>{who}</span></div>' + ('<span class="bt-tag g">必选</span>' if st == 'lock' else f'<label class="ad-sw"><input type="checkbox"{" checked" if st == "on" else ""} data-ad-menu aria-label="{n}"><span></span></label>') + '</div>' for n, st, who in MENU)
PANES += pane('ad-menu', '菜单展示', '决定客户控制台显示哪些页面。关掉的页面所有客户都看不到；角色权限之外再收一层。', 'api',
              f'<div class="ad-mods">{cards}</div>\n'
              '          <p class="ad-fine">对应 new-api 自带的「系统设置 › 站点与品牌 › 侧边栏模块」。在线试用与绿电批量任务默认关闭：前者等备案，后者等批量接口。</p>')
SETS = [('站点与品牌', '系统名称、logo、公告、顶部导航与侧边栏模块'), ('身份验证', '邮箱、手机、微信、通行密钥等登录方式'), ('计费与支付', '充值方式、支付渠道、汇率与充值档位'),
        ('模型', '模型映射、分组与倍率'), ('请求策略', '重试、超时与渠道选择'), ('安全与限制', 'RPM / TPM 限流、IP 限制、敏感词'), ('控制台内容', '概览公告、常见问答、关于页'), ('内容安全', '敏感词过滤与请求审查'), ('运维', '日志保留、数据清理、系统信息')]
PANES += pane('ad-set', '系统设置', '平台级配置。沿用 new-api 的设置页，这里按分组列出用途。', 'api',
              '<div class="ad-mods">' + ''.join(f'<div class="bt-mini ad-set"><b>{x}</b><p>{y}</p><button class="bt-a" type="button" data-ad-act>在 new-api 中配置 →</button></div>' for x, y in SETS) + '</div>')
PANES += pane('ad-logs', '全站日志', '所有账户的调用记录，用于排查与对账。', 'api',
              flt(q('按用户、Key 或模型查找'), sel('时间', ['今天', '近 7 天', '近 30 天']), sel('类型', ['全部', '调用', '充值', '管理'])) + '\n          ' +
              tbl(['时间', '渠道', '用户', 'API Key', '模型', '流式', '>词元', '>费用', '>耗时']) + '\n          ' +
              empty('book', '还没有调用记录', '接入后读取 new-api 的全站使用日志，可以导出 CSV。'), b('导出 CSV', True))
PANES += pane('ad-audit', '审计日志', '管理员的每次操作：改价、改额度、开通组织、入账、改设置。', 'api',
              tbl(['时间', '操作人', '操作', '对象', 'IP']) + '\n          ' +
              empty('key', '还没有审计记录', '管理员操作会自动记录在这里。'))
rep('      <div class="cs-p" data-p="acct">', PANES + '      <div class="cs-p" data-p="acct">')

# ---------- 侧栏：超管菜单 ----------
I = {
    'ad-home': 'M3.5 9 10 3.5 16.5 9v7.5h-4.5v-4.5h-4v4.5H3.5Z',
    'ad-ch': 'M3 6h14M3 10h14M3 14h14 M6 4v4M14 8v4M9 12v4',
    'ad-models': 'M10 2.5 16.5 6v8L10 17.5 3.5 14V6Z M3.5 6 10 9.5 16.5 6 M10 9.5v8',
    'ad-users': 'M7.5 9.6a2.8 2.8 0 1 0 0-5.6 2.8 2.8 0 0 0 0 5.6Z M2.5 16.5c.6-2.9 2.6-4.4 5-4.4s4.4 1.5 5 4.4 M13 4.3a2.7 2.7 0 0 1 0 5.2 M14.6 12.2c1.6.5 2.6 1.9 3 4.3',
    'ad-orgs': 'M3.5 17.5v-11l6.5-3 6.5 3v11 M7 8.5h1.5M11.5 8.5H13M7 12h1.5M11.5 12H13 M8.5 17.5v-2.5h3v2.5',
    'ad-redeem': 'M3 6.5h14v2a1.5 1.5 0 0 0 0 3v2H3v-2a1.5 1.5 0 0 0 0-3Z M8 6.5v7',
    'ad-review': 'M4.5 3.5h11v13h-11Z M7 7.5h6M7 10.5h6 M7.5 13.5l1.5 1.2 2.8-2.8',
    'ad-bank': 'M3 8 10 3.5 17 8 M4.5 8v7M8 8v7M12 8v7M15.5 8v7 M3 16.5h14',
    'ad-inv': 'M5 2.5h10v15l-2.5-1.5L10 17.5 7.5 16 5 17.5Z M7.5 6.5 10 9l2.5-2.5M10 9v5M8 11.2h4',
    'ad-plants': 'M10 2.5v3M4.7 4.7l2.1 2.1M15.3 4.7l-2.1 2.1 M10 13a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7Z M5 17.5h10M7 15.5h6',
    'ad-tod': 'M10 17a7 7 0 1 0 0-14 7 7 0 0 0 0 14Z M10 6v4l2.8 2',
    'ad-batch': 'M10 3 17 6.8 10 10.6 3 6.8Z M3 10.4l7 3.8 7-3.8 M3 13.8l7 3.7 7-3.7',
    'ad-menu': 'M3.5 4.5h13v11h-13Z M7.5 4.5v11 M10 8h4M10 11h4',
    'ad-set': 'M10 12.6a2.6 2.6 0 1 0 0-5.2 2.6 2.6 0 0 0 0 5.2Z M10 2.5v2.2M10 15.3v2.2M2.5 10h2.2M15.3 10h2.2M4.7 4.7l1.6 1.6M13.7 13.7l1.6 1.6M4.7 15.3l1.6-1.6M13.7 6.3l1.6-1.6',
    'ad-logs': 'M2.5 10h3l2.5-6 4 12 2.5-6h3',
    'ad-audit': 'M10 2.5 16 5v4.5c0 4-2.6 6.6-6 8-3.4-1.4-6-4-6-8V5Z M7.5 10l1.8 1.8 3.2-3.3',
    'ad-ledger': 'M4.5 3h11v14h-11Z M7 6.5h6M7 9.5h6M7 12.5h3.5',
    'ad-refund': 'M7 6 3.5 9.5 7 13 M3.5 9.5h9a4 4 0 0 1 0 8H10',
    'ad-report': 'M3 16.5h14 M5 14V9M9 14V5M13 14v-6M17 14V8',
    'ad-hours': 'M10 6.5a3.5 3.5 0 1 0 0 7 3.5 3.5 0 0 0 0-7Z M10 2.5v1.8M10 15.7v1.8M2.5 10h1.8M15.7 10h1.8M4.7 4.7l1.3 1.3M14 14l1.3 1.3M4.7 15.3 6 14M14 6l1.3-1.3',
    'ad-alerts': 'M5.5 13.5V9a4.5 4.5 0 0 1 9 0v4.5l1.5 2h-12Z M8.5 17.5h3',
    'ad-content': 'M3.5 8v4l3 .5 6 3.5V4L6.5 7.5Z M15 8a2.5 2.5 0 0 1 0 4',
    'ad-admins': 'M10 2.5 16 5v4.5c0 4-2.6 6.6-6 8-3.4-1.4-6-4-6-8V5Z M10 8.2a1.6 1.6 0 1 0 0-3.2 1.6 1.6 0 0 0 0 3.2Z M7.3 12c.4-1.4 1.5-2.2 2.7-2.2s2.3.8 2.7 2.2',
}
L = {'ad-home': '运营概览', 'ad-ch': '渠道', 'ad-models': '模型与定价', 'ad-users': '用户', 'ad-orgs': '组织', 'ad-redeem': '兑换码', 'ad-review': '认证审核', 'ad-bank': '对公入账',
     'ad-inv': '开票处理', 'ad-plants': '电站与节点', 'ad-tod': '分时价', 'ad-batch': '批量任务', 'ad-menu': '菜单展示', 'ad-set': '系统设置', 'ad-logs': '全站日志', 'ad-audit': '审计日志', 'ad-ledger': '资金流水', 'ad-refund': '退款', 'ad-report': '对账与报表', 'ad-hours': '绿电时段', 'ad-alerts': '告警', 'ad-content': '公告与内容', 'ad-admins': '管理员与权限'}


def nb(p):
    return f'<button type="button" data-p="{p}" data-sr="super" hidden>{ico(I[p])}<span>{L[p]}</span></button>'


RULE = '<i class="bt-rule" aria-hidden="true" data-sr="super" hidden></i>'
GRP = lambda t: f'<span class="cs-grp bt-grp" data-sr="super" hidden>{t}</span>'
SNAV = '\n        '.join([nb('ad-home'), RULE, GRP('平台'), nb('ad-ch'), nb('ad-models'), nb('ad-tod'), nb('ad-users'), nb('ad-orgs'), nb('ad-redeem'), RULE,
                         GRP('财务'), nb('ad-ledger'), nb('ad-bank'), nb('ad-inv'), nb('ad-refund'), nb('ad-report'), RULE,
                         GRP('绿电'), nb('ad-plants'), nb('ad-hours'), nb('ad-batch'), RULE,
                         GRP('客户运营'), nb('ad-review'), nb('ad-content'), nb('ad-alerts'), RULE,
                         GRP('系统'), nb('ad-admins'), nb('ad-menu'), nb('ad-set'), nb('ad-logs'), nb('ad-audit')])
a = s.index('<nav class="cs-nav bt-nav" aria-label="控制台">'); b = s.index('</nav>', a)
s = s[:b] + '  ' + SNAV + '\n      ' + s[b:]

# ---------- CSS ----------
CSS = '''
<style id="sup-super-css">
/* 超管版（2026-10-14）：沿用客户控制台的 Dia 组件，只补这几处 */
.ad-hr{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.ad-dev{display:inline-flex;align-items:center;gap:6px}
.ad-dev:before{content:"";width:6px;height:6px;border-radius:50%;background:#3D314F}
.ad-kpi{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}
.ad-kpi .bt-mini{gap:4px}
.ad-k{font:400 11px var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--ink-50)}
.bt-mini .ad-n{font:400 34px/1.1 var(--serif);letter-spacing:-.02em;font-variation-settings:"opsz" 144}
.ad-s{font-size:13px;color:var(--ink-50)}
.ad-h2{font:400 28px/1.2 var(--serif);letter-spacing:-.02em;margin:18px 0 0;font-variation-settings:"opsz" 144}
.ad-fine{margin:0;font-size:13px;color:var(--ink-50)}
.ad-chips{margin:0}
.ad-form{gap:12px}
.ad-fr{display:flex;flex-wrap:wrap;gap:10px}
.ad-fr .in{flex:1 1 180px;height:42px;padding-top:0;padding-bottom:0;line-height:40px;border-radius:999px;background:rgba(255,255,255,.75)}
.ad-mods{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.ad-mod{grid-template-columns:minmax(0,1fr) auto;align-items:center;justify-items:stretch}
.ad-mod b{display:block}
.ad-mod span:not(.bt-tag){font-size:13px;color:var(--ink-50)}
.ad-set p{margin:0;font-size:14px;color:var(--ink-70)}
.ad-sw{position:relative;display:inline-block;width:42px;height:24px;flex:none}
.ad-sw input{position:absolute;inset:0;opacity:0;margin:0;cursor:pointer}
.ad-sw span{position:absolute;inset:0;border-radius:999px;background:rgba(0,0,0,.14);box-shadow:inset 0 1px 2px rgba(0,0,0,.08);transition:background .25s}
.ad-sw span:after{content:"";position:absolute;top:3px;left:3px;width:18px;height:18px;border-radius:50%;background:#fff;box-shadow:0 1px 3px rgba(0,0,0,.2);transition:transform .25s}
.ad-sw input:checked+span{background:#000}
.ad-sw input:checked+span:after{transform:translateX(18px)}
.ad-sw input:focus-visible+span{outline:2px solid var(--ink);outline-offset:2px}
.ad-steps li{grid-template-columns:24px minmax(0,1fr)}
.ad-day{gap:10px}
.ad-day .ad-bar,.ad-day .ad-ax,.ad-day p{justify-self:stretch;width:100%}
.ad-bar{display:grid;grid-template-columns:repeat(24,minmax(0,1fr));gap:3px}
.ad-bar i{height:28px;border-radius:6px}
.ad-bar .idle,.ad-lg.idle{background:linear-gradient(180deg,#5B83C9,#2F63B8)}
.ad-bar .busy,.ad-lg.busy{background:linear-gradient(180deg,#5A4E6B,#3D314F)}
.ad-ax{display:flex;justify-content:space-between;font:400 11px var(--mono);color:var(--ink-50)}
.ad-day p{margin:0;font-size:13px;color:var(--ink-70)}
.ad-lg{display:inline-block;width:10px;height:10px;border-radius:3px;margin-right:6px;vertical-align:-1px}
.ad-chans{align-items:center}
.ad-perm td:not(:first-child),.ad-perm th:not(:first-child){text-align:center}
@media (max-width:860px){.ad-kpi,.ad-mods{grid-template-columns:minmax(0,1fr)}.bt-mini .ad-n{font-size:28px}.ad-bar i{height:20px}}
</style>
'''
k = s.rindex('</head>'); s = s[:k] + CSS + s[k:]

# ---------- JS ----------
PX = {} if LIVE else {'glm-5-3': [8, 2, 28], 'glm-5-3-flash': [0.8, 0.23, 2.8], 'deepseek-v4-pro': [4.5, 0.45, 13.5]}
JS = r'''
  /* ======== 超管版（2026-10-14） ======== */
  (function(){
    var PX=__PX__;
    function isSup(){return me&&me.type==='super'}
    function supSuper(){ if(!me) return; var sup=isSup();
      $$('[data-sr="super"]').forEach(function(el){el.hidden=!sup});
      if(sup){ $$('.cs-nav > *').forEach(function(el){if(el.getAttribute('data-sr')!=='super') el.hidden=true});
        ['.bt-pins','#btCredB'].forEach(function(q){var e=$(q); if(e) e.hidden=true});
        var cur=$('.cs-nav button.on'); if(!cur||cur.hidden||!/^ad-/.test(cur.getAttribute('data-p'))) csTab('ad-home'); }
      else { var c2=$('.cs-nav button.on'); if(c2&&/^ad-/.test(c2.getAttribute('data-p'))) csTab('home'); var e2=$('.bt-pins'); if(e2) e2.hidden=false; var e3=$('#btCredB'); if(e3) e3.hidden=false } }
    var _rc2=renderConsole; renderConsole=function(){_rc2(); supSuper()};
    /* 模型与定价：读同一份模型目录 M；输入 / 缓存只填有出处的 */
    var tb=$('#adModels'); if(tb) tb.innerHTML=M.map(function(m){var p=PX[m.id]; return '<tr><td>'+vlogo(m.vendor,18)+' '+esc(m.name)+'</td><td>'+esc(m.vendor)+'</td><td>按量</td><td class="mono r">'+(p?cny(p[0]):'待同步')+'</td><td class="mono r">'+(p?cny(p[1]):'待同步')+'</td><td class="mono r">'+cny(m.mkt)+'</td><td>'+(m.id==='deepseek-v4-pro'&&!__LIVE__?'闲时 / 忙时':'全天')+'</td><td>已上架</td></tr>'}).join('');
    $$('[data-ad-go]').forEach(function(b){b.addEventListener('click',function(){csTab(b.getAttribute('data-ad-go'))})});
    $$('[data-ad-act]').forEach(function(b){b.addEventListener('click',function(){toast('接入平台后即可使用。')})});
    $$('[data-ad-form]').forEach(function(f){f.addEventListener('submit',function(e){e.preventDefault(); toast('接入平台后即可使用。')})});
    $$('[data-ad-menu]').forEach(function(c){c.addEventListener('change',function(){toast('预览：开关不会保存。对应 new-api 系统设置 › 侧边栏模块。')})});
    $$('.ad-chips').forEach(function(g){var bs=$$('.bt-chip',g); bs.forEach(function(b){b.addEventListener('click',function(){bs.forEach(function(x){var on=x===b; x.classList.toggle('on',on); x.setAttribute('aria-pressed',String(on))})})})});
  })();
'''.replace('__PX__', json.dumps(PX)).replace('__LIVE__', 'true' if LIVE else 'false')
rep("  $$('[data-product-target]').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();jumpTo(a.getAttribute('data-product-target'))})});\n  window.addEventListener('hashchange',route); route();",
    JS + "  $$('[data-product-target]').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();jumpTo(a.getAttribute('data-product-target'))})});\n  window.addEventListener('hashchange',route); route();")

EN = {
    '运营概览': 'Operations overview', '平台': 'Platform', '沐仞运营': 'FathomPeak operations', '系统': 'System', '渠道': 'Channels', '模型与定价': 'Models & pricing', '用户': 'Users', '组织': 'Organizations',
    '兑换码': 'Redemption codes', '认证审核': 'Verification review', '对公入账': 'Bank transfers', '开票处理': 'Invoicing', '电站与节点': 'Plants & nodes', '分时价': 'Time-of-day pricing', '批量任务': 'Batch jobs',
    '菜单展示': 'Menu display', '系统设置': 'System settings', '全站日志': 'All usage logs', '审计日志': 'Audit log', 'new-api 现成': 'Built into new-api', '需开发': 'Needs development',
    '全平台的用户、请求、消耗与待处理事项。': 'Users, requests, spend and pending work across the platform.', '今日请求': 'Requests today', '今日消耗': 'Spend today', '可用渠道': 'Channels up', '待处理': 'Pending',
    '教育认证、实名认证、企业认证': 'Education, identity and company verification', '核对转账凭证，给账户加余额': 'Check transfer receipts and credit accounts', '开票申请': 'Invoice requests', '处理客户提交的开票申请': 'Handle customer invoice requests',
    '去处理 · --': 'Open · --', '数字接入平台数据后显示。用户、请求、消耗与渠道来自 new-api 数据看板；待处理事项来自沐仞新增的运营服务。': 'Figures appear once platform data is connected. Users, requests, spend and channels come from the new-api dashboard; pending items come from the new FathomPeak operations service.',
    '上游模型供应商与自有节点的接入，按优先级和权重分流。': 'Upstream model providers and our own nodes, routed by priority and weight.', '查找渠道': 'Find a channel', '全部': 'All', '已启用': 'Active', '已停用': 'Disabled',
    '名称': 'Name', '分组': 'Group', '类型': 'Type', '状态': 'Status', '响应时间': 'Latency', '已用 / 剩余': 'Used / left', '优先级': 'Priority', '权重': 'Weight', '操作': 'Actions',
    '还没有接入渠道数据': 'No channel data yet', '接入后直接读取 new-api 的渠道列表。': 'Reads the new-api channel list once connected.', '新增渠道': 'Add channel',
    '模型上架、计费方式与价格。客户控制台的模型目录与定价页都读这里。': 'Model listings, billing method and prices. The customer model catalog and pricing page read from here.', '计费方式': 'Billing', '缓存读取': 'Cache read', '时段': 'Hours', '按量': 'Per token',
    '全天': 'All day', '闲时 / 忙时': 'Off-peak / peak', '已上架': 'Listed', '待同步': 'Not yet synced', '新增模型': 'Add model',
    '单位 ¥ / 百万词元。输出价来自平台模型目录；输入与缓存价来自 2026-10-08 报价单刊例价。': 'In ¥ per million tokens. Output prices come from the platform catalog; input and cache prices are list prices from the 8 October 2026 quote.',
    '全部个人、教育与企业账户：额度、分组、角色与启停。': 'All personal, education and business accounts: credit, group, role and status.', '查找用户': 'Find a user', '个人': 'Personal', '教育': 'Education', '企业': 'Business',
    '可用额度': 'Available credit', '角色': 'Role', '邀请人': 'Invited by', '注册时间': 'Signed up', '还没有用户数据': 'No user data yet', '接入后读取 new-api 的用户列表，可以改额度、分组与角色，停用账户。': 'Reads the new-api user list once connected; change credit, group and role, or disable accounts.',
    '开通企业组织并指定管理员；管理员再添加自己的成员。': 'Open business organizations and name an admin, who then adds members.', '组织名称': 'Organization name', '管理员邮箱': 'Admin email', '开通组织': 'Open organization',
    '管理员': 'Admin', '成员': 'Members', '钱包余额': 'Wallet balance', '本月消费': 'This month', '企业认证': 'Company verification', '开通时间': 'Opened', '还没有组织': 'No organizations yet',
    '开通后，组织与成员数、余额和本月消费显示在这里。': 'Once opened, organizations, member counts, balance and monthly spend appear here.', '上游 new-api 没有组织，只有分组；开发说的组织管理需确认是否已在 fork 里': 'Upstream new-api has groups, not organizations; confirm whether the fork already has organization management',
    '批量生成兑换码，用于活动赠送和代金券。': 'Generate redemption codes in bulk for promotions and vouchers.', '面额（¥）': 'Value (¥)', '面额': 'Value', '数量': 'Quantity', '生成': 'Generate', '创建时间': 'Created', '兑换账户': 'Redeemed by',
    '还没有兑换码': 'No codes yet', '生成后，兑换码与使用情况显示在这里。': 'Generated codes and their use appear here.',
    '教育认证、实名认证与企业认证的人工审核。': 'Manual review of education, identity and company verification.', '教育认证': 'Education', '实名认证': 'Identity', '提交时间': 'Submitted', '账户': 'Account', '材料': 'Documents',
    '没有待审核的申请': 'Nothing to review', '客户提交学生证、在读证明或企业材料后显示在这里。': 'Student IDs, enrollment certificates or company documents appear here once submitted.', '实名若接第三方认证服务，可以不设人工审核': 'If identity checks use a third-party service, manual review is not needed',
    '核对企业对公转账，确认后给对应账户或组织加余额。': 'Check company bank transfers and credit the account or organization once confirmed.', '到账时间': 'Received', '付款户名': 'Payer', '金额': 'Amount', '凭证': 'Receipt', '对应账户': 'Account',
    '没有待确认的转账': 'No transfers to confirm', '客户上传或邮件发来转账凭证后显示在这里。': 'Receipts uploaded or emailed by customers appear here.',
    '处理客户的开票申请，上传发票后客户可以下载。': 'Handle invoice requests; customers can download the invoice once uploaded.', '已开票': 'Invoiced', '申请时间': 'Requested', '抬头': 'Name', '没有开票申请': 'No invoice requests',
    '客户在控制台「发票」里提交后显示在这里。': 'Requests submitted under Invoices in the console appear here.', '待公司确认：按消费还是按充值开票、开票时限': 'Company to confirm: invoice on spend or on top-up, and turnaround',
    '接入的电站、算力节点与用电来源，是订单产地卡和「绿电折扣」的数据来源。': 'Connected plants, compute nodes and power sources: the data behind origin cards and the green discount.', '能源类型': 'Energy type', '所在地': 'Location', '装机': 'Capacity', '算力节点': 'Compute node', '接入时间': 'Connected',
    '还没有电站与节点数据': 'No plant or node data yet', '接入电站与节点系统后，这里管理节点上下线与产地卡字段。': 'Once the plant and node system is connected, manage nodes and origin-card fields here.', '新增电站': 'Add plant',
    '按时段给模型定价：闲时 / 忙时，以及按电站富余绿电的时段价。': 'Price models by time: off-peak / peak, and green-power hours when plants have surplus.', '闲时 22:00–08:00': 'Off-peak 22:00–08:00', '忙时 08:00–22:00': 'Peak 08:00–22:00',
    '报价单': 'Quote', '全部模型': 'All models', '绿电时段': 'Green-power hours', '规划中': 'Planned', 'new-api 的定价不分时段，需要开发。时段与价格来自 2026-10-08 报价单。': 'new-api pricing has no time periods, so this needs development. Hours and prices come from the 8 October 2026 quote.', '新增时段': 'Add period',
    '客户提交的绿电批量任务：排队、执行时段与完成情况。': 'Green batch jobs from customers: queue, scheduled hours and completion.', '请求数': 'Requests', '计划时段': 'Scheduled', '还没有批量任务': 'No batch jobs yet', '批量接口开发完成后，客户提交的任务显示在这里。': 'Customer jobs appear here once the batch API is built.',
    '决定客户控制台显示哪些页面。关掉的页面所有客户都看不到；角色权限之外再收一层。': 'Choose which pages the customer console shows. A page switched off is hidden from every customer, on top of role permissions.', '必选': 'Required',
    '对应 new-api 自带的「系统设置 › 站点与品牌 › 侧边栏模块」。在线试用与绿电批量任务默认关闭：前者等备案，后者等批量接口。': 'This is new-api’s built-in System settings › Site & brand › Sidebar modules. Playground and green batch jobs are off by default: the first waits for filing, the second for the batch API.',
    '平台级配置。沿用 new-api 的设置页，这里列出分组与用途。': 'Platform-wide configuration, using the new-api settings pages. Listed here by section.', '站点与品牌': 'Site & brand', '系统名称、logo、公告、顶部导航与侧边栏模块': 'System name, logo, notices, top navigation and sidebar modules',
    '身份验证': 'Authentication', '邮箱、手机、微信、通行密钥等登录方式': 'Sign-in methods: email, phone, WeChat, passkeys', '计费与支付': 'Billing & payments', '充值方式、支付渠道、汇率与充值档位': 'Top-up methods, payment channels, exchange rate and amounts',
    '模型映射、分组与倍率': 'Model mapping, groups and multipliers', '请求策略': 'Request policy', '重试、超时与渠道选择': 'Retries, timeouts and channel choice', '安全与限制': 'Security & limits', 'RPM / TPM 限流、IP 限制、敏感词': 'RPM / TPM limits, IP restrictions, blocked words',
    '控制台内容': 'Console content', '概览公告、常见问答、关于页': 'Overview notices, FAQ, about page', '运维': 'Operations', '日志保留、数据清理、系统信息': 'Log retention, data cleanup, system info', '打开': 'Open',
    '所有账户的调用记录，用于排查与对账。': 'Calls from every account, for troubleshooting and reconciliation.', '按用户、Key 或模型查找': 'Find by user, key or model', '流式': 'Stream', '词元': 'Tokens', '费用': 'Cost', '耗时': 'Duration',
    '还没有调用记录': 'No calls yet', '接入后读取 new-api 的全站使用日志。': 'Reads the new-api usage log once connected.', '管理员的每次操作：改价、改额度、开通组织、入账、改设置。': 'Every admin action: price and credit changes, new organizations, credits and settings.',
    '操作人': 'By', '对象': 'Target', '还没有审计记录': 'No audit records yet', '管理员操作会自动记录在这里。': 'Admin actions are recorded here automatically.',
    '接入平台后即可使用。': 'Available once the platform is connected.', '预览：开关不会保存。对应 new-api 系统设置 › 侧边栏模块。': 'Preview: switches are not saved. This maps to new-api System settings › Sidebar modules.',
}
EN.update({"财务": "Finance", "绿电": "Green power", "客户运营": "Customer operations", "资金流水": "Ledger", "退款": "Refunds", "对账与报表": "Statements & reports", "告警": "Alerts", "公告与内容": "Notices & content", "管理员与权限": "Admins & permissions", "每一笔钱的进出：充值、赠送、消费、退款、人工调整分开记，带单号、操作人和变动后余额。": "Every movement of money, recorded separately as top-up, credit, spend, refund or manual adjustment, with reference, operator and resulting balance.", "按账户或单号查找": "Find by account or reference", "赠送": "Credit", "消费": "Spend", "人工调整": "Manual adjustment", "本月": "This month", "上月": "Last month", "近 90 天": "Last 90 days", "变动后余额": "Balance after", "单号": "Reference", "操作人": "Operator", "备注": "Note", "还没有资金流水": "No ledger entries yet", "对公入账、兑换码、退款和每次调用扣费都会在这里逐笔记账，赠送额度单独标记并可设过期。": "Bank transfers, redemption codes, refunds and every usage charge are recorded here; credits are marked separately and can expire.", "导出 CSV": "Export CSV", "退款时同时作废对应额度；已开发票的先红冲，再退款。": "A refund also voids the matching credit; invoiced amounts are reversed first.", "已退款": "Refunded", "已拒绝": "Declined", "原充值单": "Original top-up", "退款金额": "Refund", "作废额度": "Credit voided", "关联发票": "Invoice", "没有退款申请": "No refund requests", "客户申请或运营发起的退款显示在这里。": "Refunds requested by customers or started by operations appear here.", "发起退款": "Start refund", "按月生成对账单，看充值、赠送、消耗和余额负债；按渠道核对上游成本与毛利。": "Monthly statements; top-ups, credits, spend and balance liability; upstream cost and margin by channel.", "本月充值": "Top-ups this month", "本月赠送": "Credits this month", "本月消耗": "Spend this month", "余额负债": "Balance liability", "全部账户余额合计": "Sum of all account balances", "月度对账单": "Monthly statements", "月份": "Month", "组织 / 账户": "Organization / account", "期末余额": "Closing balance", "还没有对账单": "No statements yet", "每月按组织、成员和 API Key 生成上月对账单，可以导出发给客户。": "Each month, last month’s statement is generated by organization, member and API key, ready to export for customers.", "上游成本": "Upstream cost", "我们记的成本": "Our recorded cost", "上游账单": "Upstream bill", "差额": "Difference", "毛利率": "Gross margin", "还没有上游账单": "No upstream bills yet", "导入上游账单后，按渠道核对成本与毛利。": "Import upstream bills to check cost and margin by channel.", "导出": "Export", "按电站发布计划绿电时段，可以提前公示，变更留痕。分时价和批量任务都读这张表。": "Publish planned green-power hours per plant, in advance and with a change history. Time-of-day pricing and batch jobs both read this table.", "电站": "Plant", "全部电站": "All plants", "本周": "This week", "下周": "Next week", "日期": "Date", "计划绿电时段": "Planned green hours", "发布人": "Published by", "还没有发布绿电时段": "No green-power hours published", "时段要来自电站的真实计量与预测，不能用估算值。": "Hours must come from real plant metering and forecasts, not estimates.", "发布时段": "Publish hours", "出问题时主动叫人：推送到运营群、邮箱或 Webhook。": "Notify people when something goes wrong: operations chat, email or webhook.", "渠道连续失败或被自动停用": "Channel keeps failing or was auto-disabled", "渠道测速失败、余额耗尽时提醒运营": "Alert operations when a channel fails speed tests or runs out of balance", "用户余额低于阈值": "User balance below threshold", "按账户设置的预警线": "Using each account’s alert threshold", "组织预算到达提醒比例": "Organization budget reaching an alert level", "75% / 90% / 100%，超预算可自动冻结": "75% / 90% / 100%; can freeze automatically when over budget", "待办超时": "Pending work overdue", "认证审核、对公入账、开票超过 24 小时未处理": "Verification, bank transfers or invoices untouched for 24 hours", "电站离线": "Plant offline", "自动停用对应渠道，并通知运营": "Disable the matching channels and notify operations", "推送到": "Send to", "邮件": "Email", "最近告警": "Recent alerts", "最近没有告警": "No recent alerts", "触发的告警和处理状态显示在这里。": "Triggered alerts and their status appear here.", "站内公告、控制台常见问答和首页内容。": "In-app notices, console FAQ and home content.", "站内公告": "Notices", "维护通知、模型上新与调价，显示在客户控制台概览和通知铃里。": "Maintenance, new models and price changes, shown on the customer overview and in the notification bell.", "发布公告": "Publish notice", "客户控制台概览里的常见问题。": "Questions shown on the customer overview.", "编辑问答": "Edit FAQ", "模型下线通知": "Model retirement notices", "提前通知用到该模型的客户，并给出替代模型。": "Tell customers using a model ahead of time, with a replacement.", "新建通知": "New notice", "首页与关于": "Home & about", "控制台首页文案与关于页。": "Console home copy and about page.", "在 new-api 中编辑": "Edit in new-api", "按职责分权：运营管渠道、价格和客户，财务管入账、开票和退款，只读账号只能看。": "Split duties: operations handles channels, prices and customers; finance handles transfers, invoices and refunds; read-only accounts can only view.", "权限": "Permission", "运营": "Operations", "只读": "Read-only", "渠道与模型": "Channels & models", "改价（模型价、分时价）": "Pricing (model and time-of-day)", "用户与额度": "Users & credit", "开通、冻结组织": "Open or freeze organizations", "对公入账（录款 / 复核）": "Bank transfers (entry / review)", "开票与退款": "Invoices & refunds", "系统设置与菜单": "Settings & menus", "查看日志与报表": "Logs & reports", "两步验证": "Two-step", "最近登录": "Last sign-in", "还没有其他管理员": "No other admins", "添加后，对方用工作邮箱登录运营后台，第一次登录要绑定两步验证。": "Once added, they sign in with a work email and set up two-step verification at first sign-in.", "添加管理员": "Add admin", "企业对公转账按「录款 → 复核 → 入账」处理：财务录入银行流水，第二个人复核后才给账户加余额。": "Bank transfers go through entry → review → credit: finance records the bank statement, and a second person reviews before the balance is credited.", "录款": "Entry", "复核": "Review", "入账": "Credit", "录入到账日期、付款户名、金额和银行流水号，上传回单。": "Record date, payer, amount and bank reference; upload the receipt.", "另一位财务核对回单与流水，可以退回。": "Another finance staff member checks the receipt and statement and can send it back.", "给对应账户或组织加余额，写进资金流水；可以撤销并留痕。": "Credit the account or organization and record it in the ledger; can be reversed with a trail.", "录入到账": "Record transfer", "到账日期": "Received", "银行流水号": "Bank reference", "录入": "Record", "待复核": "To review", "已入账": "Credited", "已退回": "Returned", "流水号": "Reference", "录入人": "Entered by", "复核人": "Reviewed by", "没有待复核的转账": "No transfers to review", "财务录款后显示在这里，复核通过即入账。付款户名和实名主体不一致时，需要代付协议。": "Transfers appear here after entry and are credited once reviewed. If the payer differs from the verified account holder, a third-party payment agreement is needed.", "价格分组": "Price group", "合同价有效期": "Contract valid until", "预算上限": "Budget", "开通后，组织、成员数、余额和本月消费显示在这里。合同价通过「价格分组」绑定并设有效期；超预算可以自动冻结，冻结原因必填。": "Once opened, organizations, members, balance and monthly spend appear here. Contract prices are bound through a price group with an end date; organizations over budget can be frozen automatically, with a required reason.", "实名": "Verified", "已认证": "Verified", "未认证": "Not verified", "已冻结": "Frozen", "接入后读取 new-api 的用户列表，可以改额度和分组，冻结或停用账户，冻结原因必填。": "Reads the new-api user list once connected; change credit and group, or freeze or disable accounts (a reason is required to freeze).", "未实名的账户只能用赠送额度，用完即停。": "Unverified accounts can only use free credit and stop when it runs out.", "已红冲": "Reversed", "绑定渠道": "Channels", "每个渠道挂到一个节点，每个节点挂到一个电站。电站离线时，对应渠道自动停用并告警。": "Each channel maps to a node and each node to a plant. When a plant goes offline, its channels are disabled and an alert is sent.", "按时段给模型定价：闲时 / 忙时，以及按电站富余绿电的时段价。保存后写成 new-api 的按时段表达式计费。": "Price models by time: off-peak / peak and green-power hours. Saved as new-api time-based pricing expressions.", "DeepSeek-V4-Pro · 全天": "DeepSeek-V4-Pro · 24 hours", "计费用 new-api 的表达式定价（rc.37 起支持按小时、星期，含跨夜时段），这里做编辑与全天预览；改价写进审计日志。时段与价格来自 2026-10-08 报价单。": "Billing uses new-api expression pricing (hour and weekday since rc.37, including overnight ranges); this page edits and previews the day, and price changes go to the audit log. Hours and prices come from the 8 October 2026 quote.", "接入后读取 new-api 的全站使用日志，可以导出 CSV。": "Reads the new-api usage log once connected, with CSV export.", "内容安全": "Content safety", "敏感词过滤与请求审查": "Blocked words and request review"})
EN.update({'个人 -- · 企业 --': 'Personal -- · Business --', '较昨日 --': 'vs yesterday --', '¥ · 较昨日 --': '¥ · vs yesterday --', '共 -- 个': '-- total',
    '-- 条': '-- items', '-- 笔': '-- transfers', '-- 张': '-- invoices', '去处理': 'Open', '教育认证、实名认证、企业认证。': 'Education, identity and company verification.',
    '核对转账凭证，给账户加余额。': 'Check transfer receipts and credit accounts.', '处理客户提交的开票申请。': 'Handle customer invoice requests.',
    '接入的电站、算力节点与用电来源，是订单产地卡、日志里「绿电折扣」和绿电时段价的数据来源。接入电站与节点系统后，这里显示各节点状态。': 'Connected plants, compute nodes and power sources feed origin cards, the green discount in logs and green-hour prices. Node status appears here once the plant and node system is connected.',
    '接入后直接读取 new-api 的渠道列表：测速、启停、余额与分流权重。': 'Reads the new-api channel list once connected: speed tests, on/off, balance and routing weight.', 'OpenAI 兼容': 'OpenAI-compatible', '自有节点': 'Own nodes',
    '开通': 'Open', '生成兑换码': 'Generate codes', '在 new-api 中配置 →': 'Configure in new-api →', '平台级配置。沿用 new-api 的设置页，这里按分组列出用途。': 'Platform-wide configuration using the new-api settings pages, listed by section.',
    '时间': 'Time', '调用': 'Calls', '充值': 'Top-ups', '管理': 'Admin', '来源': 'Source', '企业管理员': 'Business admin', '个人 · 企业管理员': 'Personal · Business admin',
    '接入后读取 new-api 的用户列表，可以改额度、分组与角色，或停用账户。': 'Reads the new-api user list once connected; change credit, group and role, or disable accounts.',
    '开通后，组织、成员数、余额和本月消费显示在这里。': 'Once opened, organizations, member counts, balance and monthly spend appear here.'})
rep('  syncAuthLocale(); applyLang();', '  (function(S){for(var k in S) if(!(k in I18N)) I18N[k]=S[k]})(' + json.dumps(EN, ensure_ascii=False) + ');  /* 超管版英文：只补缺 */\n  syncAuthLocale(); applyLang();')

open(OUT, 'w', encoding='utf8').write(s)
print('done:', OUT)
