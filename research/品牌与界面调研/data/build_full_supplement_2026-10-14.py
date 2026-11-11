"""全部补充预览（Zixin 2026-10-14："在我们的基础上 修改完成全部补充 做html"；不动线上）。
底稿：线上 index.html（49b44ea）先跑 build_review_preview_2026-10-14.py --soft（首页审查改动），再跑本脚本。
补的是与原平台 / 参考站 / 硅基流动对比后缺的功能，只用有出处的事实；没出处的一律标黄「待公司确认」，不编在线率、限流档位或开票政策：
 1 占位符：YOUR_API_HOST、<沐仞接入地址>、"接入地址见控制台" → 真实地址 api.fathompeak.cn（2026-10-14 实测：不带 Key 返回 new_api_error 401）；复制代码时把 NBSP 换成空格。
 2 定价：模型价格表加 输入 / 缓存命中 / 输出 三列 + 厂商、类型筛选 + 搜索；新增"分时价格"；计算器自动填输入价；FAQ 去掉无出处的"富余绿电时段更便宜"。
    输入与缓存价出自 2026-10-08 报价单刊例价（含税 6%）。报价单写明"商业机密"，所以整块标黄，公开前要公司确认。
    DeepSeek-V4-Flash：报价单是 V4.1-Flash（输出 4 / 8），与平台目录 4.50 对不上 → 标"型号待核对"；Qwen、MiniMax 没有出处 → "待同步"。
 3 模型详情：模型 ID 一键复制、输入 / 缓存 / 输出三格价格、DeepSeek 忙时价、curl / Python / Node.js 三种示例、返回全部模型；假的"试一次调用"框改成"在线试用"入口。
 4 更新日志：L 填入有出处的记录（官网 git 提交、模型收录日期、飞书 9/24、9/28 进度说明），筛选改为 模型 / 平台 / 官网。
 5 服务状态页 #status：浏览器实时检测 api.fathompeak.cn 连通与往返时间；历史可用率、故障公告标"待接入监控"。
 6 文档：新增 账户与实名、充值与发票、限流与配额 三页；错误码补 400 / 403 / 5xx 与真实 401 返回体；每页"复制本页"；llms.txt。
 7 站内搜索：导航放大镜 + ⌘K / Ctrl+K / "/"，搜页面、模型、文档、指南、接口。
 8 控制台：侧栏加"在线试用"（文本对话，预览不发起真实调用，标"需开通 + 备案"）；钱包加"月度预算与提醒"、"代金券"。
 9 页脚：资源栏加 更新日志 / 服务状态 / llms.txt；社群二维码位置标"待公司提供"。
 评审辅助：左下"标出新增"按钮给所有新增块描虚线框；黄色胶囊 = 待公司确认。
登录页按 Zixin 说的"保持"，不改。
用法：python3 -I build_full_supplement_2026-10-14.py <底稿 html> <输出 html> [<llms.txt 输出路径>] [--console-only]
--console-only（2026-10-14 夜，上线用）：只做 1 占位符 + 8 控制台（体验中心入口、预算、代金券）+ 评审按钮（后面的正式版处理会去掉）；
  定价（含报价单机密价）、更新日志、服务状态、文档、站内搜索、页脚都不改，JS 只留预算提示。
"""
import json, sys

CONSOLE_ONLY = '--console-only' in sys.argv
args = [x for x in sys.argv[1:] if not x.startswith('--')]
SRC, OUT = args[0], args[1]
LLMS = args[2] if len(args) > 2 else None
SKIP = False  # 为 True 时 rep / rep_all 不做任何改动（--console-only 跳过官网部分）
s = open(SRC, encoding='utf8').read()
HOST = 'api.fathompeak.cn'
SITE = 'https://xanthiawang.github.io/fathompeak-site/'


def rep(old, new, n=1):
    global s
    if SKIP: return
    c = s.count(old)
    if c != n: sys.exit(f'[停止] 匹配 {c} 次（应为 {n}）：{old[:80]}')
    s = s.replace(old, new)


def rep_all(old, new, at_least=1):
    global s
    if SKIP: return 0
    c = s.count(old)
    if c < at_least: sys.exit(f'[停止] 匹配 {c} 次（至少 {at_least}）：{old[:80]}')
    s = s.replace(old, new)
    return c


def tbc(t='待公司确认'):
    return f'<span class="tbc">{t}</span>'


# ---------- 1 占位符 ----------
rep_all('# 将 YOUR_API_HOST 替换为正式控制台提供的 HTTPS 域名', '# 沐仞 API 接入地址', 3)
rep_all('# 接入地址见控制台', '# 沐仞 API 接入地址', 4)
rep_all('各客户端的菜单名称会随版本变化，以客户端当前版本为准。接入地址见控制台。', f'各客户端的菜单名称会随版本变化，以客户端当前版本为准。接入地址为 https://{HOST}/v1。', 2)
rep_all('将 YOUR_API_HOST 替换为平台提供的 HTTPS 接入域名。各客户端的菜单名称会随版本变化，以客户端当前版本为准。',
        f'接入地址为 https://{HOST}/v1。各客户端的菜单名称会随版本变化，以客户端当前版本为准。', 2)
rep_all('&lt;沐仞接入地址&gt;/v1', f'{HOST}/v1', 1)
rep_all('\\"&lt;沐仞接入地址&gt;\\"', f'\\"https://{HOST}/v1\\"', 1)
rep_all('"&lt;沐仞接入地址&gt;"', f'"https://{HOST}/v1"', 1)
n_host = rep_all('YOUR_API_HOST', HOST, 15)
rep('function copyText(t,done){', 'function copyText(t,done){t=String(t).replace(/\\u00a0/g," ");')

SKIP = CONSOLE_ONLY
# ---------- 2 定价 ----------
rep('<div class="pr-hd"><h2>模型价格</h2><p>目录与输出参考价来自沐仞模型平台。DeepSeek 为空闲时段价格，MiniMax-M3 为 ≤512k 档。</p></div>',
    '<div class="pr-hd"><h2>模型价格</h2><p>单位 ¥ / 百万词元。目录与输出参考价来自沐仞模型平台，输入与缓存命中价来自 2026-10-08 报价单的刊例价。DeepSeek 分闲时、忙时计价，MiniMax-M3 为 ≤512k 档。</p></div>'
    '<div class="sup-bar sup-new" id="supPrBar"><label class="sup-q"><svg viewBox="0 0 16 16" aria-hidden="true"><circle cx="7" cy="7" r="5" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M11 11l3.5 3.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>'
    '<input type="search" id="supPrQ" placeholder="查找模型" aria-label="查找模型" autocomplete="off" spellcheck="false"></label><div class="sup-chips" id="supPrC" role="group" aria-label="按厂商和类型筛选"></div></div>')
rep('<th>模型</th><th>厂商</th><th>类型</th><th>上下文</th><th class="r">输出参考价 ¥ / 百万词元</th><th></th></tr></thead><tbody id="prRows">',
    '<th>模型</th><th>厂商</th><th>类型</th><th>上下文</th><th class="r">输入</th><th class="r">缓存命中</th><th class="r">输出</th><th></th></tr></thead><tbody id="prRows">')
rep('<p class="pr-note">输入、缓存等其余计费项按模型分别计价，以控制台模型列表为准。</p>',
    '<p class="pr-note sup-new">输入与缓存命中价来自 2026-10-08 报价单（刊例价，含税）。' + tbc('报价单注明为商业机密，公开前请公司确认') +
    ' 标"待同步"的价格目前没有出处，需要平台补齐。</p><p class="sup-none" id="supPr0" hidden>没有符合条件的模型</p>')
TOD = ('\n    <div class="pr-sec sup-new" id="prTod">\n'
       '      <div class="pr-hd"><h2>分时价格</h2><p>同一个模型在不同时段价格不同，按请求发出时的北京时间计价。</p></div>\n'
       '      <div class="sup-tod">\n'
       '        <div class="sup-card"><span class="k">DeepSeek-V4-Pro · 闲时</span><b class="mono">22:00–08:00</b><p class="mono">输入 ¥4.50 · 缓存 ¥0.45 · 输出 ¥13.50</p></div>\n'
       '        <div class="sup-card"><span class="k">DeepSeek-V4-Pro · 忙时</span><b class="mono">08:00–22:00</b><p class="mono">输入 ¥9.00 · 缓存 ¥0.90 · 输出 ¥27.00</p></div>\n'
       '        <div class="sup-card dim"><span class="k">绿电时段价</span><b>规划中</b><p>按电站富余绿电的时段定价，时段与价格确定后在这里公布。' + tbc() + '</p></div>\n'
       '      </div>\n'
       '      <p class="sup-now" id="supNow"></p>\n'
       '      <p class="pr-note">时段与价格来自 2026-10-08 报价单。' + tbc() + '</p>\n'
       '    </div>\n')
rep('\n    <div class="pr-sec">\n      <div class="pr-hd"><h2>费用怎么算</h2>', TOD + '\n    <div class="pr-sec">\n      <div class="pr-hd"><h2>费用怎么算</h2>')
rep('placeholder="见控制台模型列表"', 'placeholder="按上方价格表自动填入"')
rep_all('，取自上方模型价格表。输入单价以控制台模型列表为准。估算不含教育价与合同价。', '，取自上方模型价格表。输入单价按价格表自动填入，可以修改。估算不含教育价与合同价。', 1)
FAQ_OLD = '价格由模型、用量、节点资源和交付时限决定。富余绿电时段的词元更便宜。'
FAQ_NEW = '价格由模型、用量和计费时段决定。目前 DeepSeek 分闲时与忙时计价，见定价页的分时价格。'
rep_all(FAQ_OLD, FAQ_NEW, 4)
FAQ2_OLD = '按模型分别计价。本页列出输出参考价，输入、缓存等计费项以控制台模型列表为准。'
FAQ2_NEW = '按模型分别计价，见上方模型价格表。命中缓存的输入按缓存价计费，其余输入按输入价计费。'
rep_all(FAQ2_OLD, FAQ2_NEW, 1)

# ---------- 4 更新日志 ----------
LOG = [
    {'m': '10', 't': '官网', 'd': '2026-10-14', 'h': '接口参考上线', 'p': '接口参考页的内容取自沐仞模型平台的 OpenAPI 文档，按模型、对话、嵌入、重排序等分组列出请求参数与返回。', 'by': '沐仞科技'},
    {'m': '10', 't': '官网', 'd': '2026-10-14', 'h': '首页改版', 'p': '新首页讲清为什么在电站旁生产词元、怎么接入、适合哪些行业，并列出已签约与推进中的项目案例。', 'by': '沐仞科技'},
    {'m': '10', 't': '官网', 'd': '2026-10-14', 'h': '合规与法律页面、费用估算', 'p': '新增合规与安全、用户服务协议、隐私政策三个页面；定价页加入费用估算。', 'by': '沐仞科技'},
    {'m': '10', 't': '模型', 'd': '2026-10-13', 'h': '模型目录收录 7 个模型', 'p': 'DeepSeek-V4-Flash、DeepSeek-V4-Pro、Qwen3.8-Flash、GLM-5.3-Flash、GLM-5.3、MiniMax-M2.7、MiniMax-M3，上下文均为 1M，用同一个 API Key 调用。', 'by': '沐仞科技'},
    {'m': '09', 't': '平台', 'd': '2026-09-28', 'h': '平台英文界面', 'p': '平台英文版基本完成，可以中英切换，并按浏览器语言自动识别。' + tbc('来自内部进度汇报，对外发布前请公司确认'), 'by': '沐仞科技'},
    {'m': '09', 't': '平台', 'd': '2026-09-24', 'h': '企业组织与成员', 'p': '企业客户由管理员为成员派发账号，个人用户自助注册；登录后自己创建 API Key，查看使用日志和钱包。' + tbc('来自内部进度汇报，对外发布前请公司确认'), 'by': '沐仞科技'},
]
rep('  var L=[];', '  /* 更新日志（补充预览）：出处为官网 git 提交、模型收录日期、飞书 9/24 与 9/28 进度说明 */\n  var L=' + json.dumps(LOG, ensure_ascii=False) + ';')
rep('<div class="idx" id="logIdx"><div class="y">2026</div><button class="on" data-m="10">10 月</button><button data-m="09">9 月</button><button data-m="08">8 月</button></div>',
    '<div class="idx" id="logIdx"><div class="y">2026</div><button class="on" data-m="10">10 月</button><button data-m="09">9 月</button></div>')
rep('<button class="chip" data-t="节点">节点</button><button class="chip" data-t="模型">模型</button><button class="chip" data-t="账单">账单</button>',
    '<button class="chip" data-t="模型">模型</button><button class="chip" data-t="平台">平台</button><button class="chip" data-t="官网">官网</button>')

# ---------- 5 服务状态页 ----------
STATUS = '''<!-- 服务状态（全部补充预览 2026-10-14） -->
<section data-route="status">
  <div class="wrap">
    <div class="page-head pr-head"><span class="k">实时检测</span><h1 class="display">服务状态</h1><p>在你的浏览器里实时检测沐仞 API 能否连通。历史可用率接入监控后在这里公布。</p></div>
    <div class="st-now sup-new">
      <div class="st-hd"><span class="st-dot" id="stDot" aria-hidden="true"></span><b id="stSum">正在检测</b><button class="btn gray sm" type="button" id="stRe">重新检测</button></div>
      <div class="tbl"><table class="st-tbl"><thead><tr><th>组件</th><th>地址</th><th>状态</th><th class="r">往返</th></tr></thead><tbody>
        <tr><td>API 网关</td><td class="mono">api.fathompeak.cn</td><td id="stApi">正在检测</td><td class="r mono" id="stMs">—</td></tr>
        <tr><td>控制台与注册</td><td class="mono">account.fathompeak.cn</td><td>待接入监控</td><td class="r mono">—</td></tr>
        <tr><td>各模型可用性</td><td>7 个模型</td><td>待接入监控</td><td class="r mono">—</td></tr>
      </tbody></table></div>
      <p class="note">检测由你的浏览器直接请求 api.fathompeak.cn，只说明网络能连通，不代表每个模型都可用。</p>
    </div>
    <div class="pr-sec sup-new"><div class="pr-hd"><h2>近 90 天可用率</h2><p>每个组件每天一格，接入监控后自动更新。</p></div>
      <div class="st-empty">还没有监控数据。''' + tbc('待公司确认：监控工具与对外公布口径') + '''</div></div>
    <div class="pr-sec sup-new"><div class="pr-hd"><h2>故障与维护公告</h2><p>计划维护会提前在这里和控制台通知里公告。</p></div>
      <div class="st-empty">暂无公告。''' + tbc('待公司确认：公告流程与通知渠道') + '''</div></div>
  </div>
</section>

'''
rep('<!-- 往期周报 -->', STATUS + '<!-- 往期周报 -->')
rep("changelog:'更新日志 - 沐仞科技 FathomPeak',", "changelog:'更新日志 - 沐仞科技 FathomPeak',status:'服务状态 - 沐仞科技 FathomPeak',")

# ---------- 6 文档 ----------
rep('<button data-doc="models">模型与计费</button><div class="y">参考</div>',
    '<button data-doc="models">模型与计费</button><button class="sup-new" data-doc="account">账户与实名</button><button class="sup-new" data-doc="billing">充值与发票</button><div class="y">参考</div>')
rep('<button data-doc="errors">错误码</button>', '<button data-doc="errors">错误码</button><button class="sup-new" data-doc="limits">限流与配额</button>')
rep('<a class="ul" href="#guides" style="display:block;padding:6px 0 0;font-size:14px">指南与检查清单 →</a></div>',
    '<a class="ul" href="#guides" style="display:block;padding:6px 0 0;font-size:14px">指南与检查清单 →</a>'
    '<a class="ul sup-new" href="#status" style="display:block;padding:6px 0 0;font-size:14px">服务状态 →</a>'
    '<a class="ul sup-new" href="llms.txt" target="_blank" rel="noopener" style="display:block;padding:6px 0 0;font-size:14px">llms.txt ↗</a></div>')
ERR_OLD_START = '<div class="pane" data-doc="errors"><h1>错误码</h1>'
if not SKIP: i = s.index(ERR_OLD_START); j = s.index('<div class="pane" data-doc="sla">', i)
ERR = ('<div class="pane" data-doc="errors"><h1>错误码</h1><p>先看状态码和错误信息，再按下表处理。</p>\n'
       '        <div class="tbl"><table><tr><th>码</th><th>原因</th><th>怎么处理</th></tr>'
       '<tr class="sup-new"><td class="mono">400</td><td>请求参数有误，例如模型名称写错、消息格式不对</td><td>对照接口参考检查请求体；模型名称以模型目录为准</td></tr>'
       '<tr><td class="mono">401</td><td>Key 无效或已吊销</td><td>到控制台重新创建 Key</td></tr>'
       '<tr class="sup-new"><td class="mono">403</td><td>余额不足、Key 额度用完，或模型、IP 不在 Key 的允许范围内 ' + tbc('待平台确认返回码') + '</td><td>充值，或在控制台调整 Key 的额度、可用模型与 IP 白名单</td></tr>'
       '<tr><td class="mono">429</td><td>触发限流</td><td>见<a class="ul" href="#docs" data-sup-doc="limits">限流与配额</a>；需要更高并发请联系商务</td></tr>'
       '<tr class="sup-new"><td class="mono">5xx</td><td>平台或上游模型暂时故障</td><td>稍后重试，并查看<a class="ul" href="#status">服务状态</a></td></tr></table></div>\n'
       '        <h3 class="sup-new">错误返回示例</h3><p class="sup-new">不带 Key 或 Key 无效时，返回 401 和下面的 JSON（2026-10-14 实测）：</p>'
       '<div class="code pre sup-new"><button class="cp" data-copy>复制</button>{"error":{"code":"","message":"Invalid token (request id: …)","type":"new_api_error"}}</div>'
       '<p class="note">每个错误都带 request id，联系支持时请一并提供。</p></div>\n      ')
if not SKIP: s = s[:i] + ERR + s[j:]
rep('<h3>可用性</h3><p>可用率与故障补偿写进服务协议。</p></div>',
    '<h3>可用性</h3><p>可用率与故障补偿写进服务协议。</p><p class="sup-new">实时连通情况见<a class="ul" href="#status">服务状态</a>。</p></div>')
DOCS_NEW = ('      <div class="pane sup-new" data-doc="account"><h1>账户与实名</h1><p>沐仞有个人、企业、教育三种账户，注册时选择，用同一个控制台。</p>'
            '<h3>注册</h3><p>注册入口：<a class="ul" href="https://account.fathompeak.cn/sign-up" target="_blank" rel="noopener">account.fathompeak.cn</a>。注册后登录，创建 API Key。</p>'
            '<div class="tbl"><table><tr><th>账户类型</th><th>适合</th><th>说明</th></tr>'
            '<tr><td>个人</td><td>开发者、个人项目</td><td>自助注册，自己创建和管理 API Key。</td></tr>'
            '<tr><td>企业</td><td>团队与公司采购</td><td>管理员邀请同事加入并分配角色，额度和账单由企业账户统一管理；可以签合同、对公转账、按月结算。</td></tr>'
            '<tr><td>教育</td><td>学生、老师与实验室</td><td>edu.cn 邮箱注册后自动认证；没有学校邮箱，可以上传学生证或在读证明。</td></tr></table></div>'
            '<h3>实名认证</h3><p>个人与企业是否需要实名认证、怎么认证 ' + tbc() + '</p></div>\n'
            '      <div class="pane sup-new" data-doc="billing"><h1>充值与发票</h1><p>按 Token 用量计费，充值后从余额扣费，没有月费。</p>'
            '<h3>在线充值</h3><p>在控制台「钱包与账单」里选择金额和支付方式（支付宝或微信），也可以输入兑换码。' + tbc('待公司确认：到账时间与最低金额') + '</p>'
            '<h3>企业付款</h3><p>企业客户可以预付，也可以按月结算，以合同约定为准。对公转账请邮件 <a class="ul" href="mailto:fathompeak@163.com">fathompeak@163.com</a>。' + tbc('待公司提供：对公账户信息') + '</p>'
            '<h3>价格与税</h3><p>价格均为含税价（增值税 6%）。' + tbc('来自 10-08 报价单，待公司确认') + '</p>'
            '<h3>发票</h3><p>支持电子发票与增值税发票。' + tbc('待公司确认：开票入口、所需信息与开票时间') + '</p>'
            '<h3>退款</h3><p>' + tbc('待公司确认：余额能否退、怎么退') + '</p></div>\n'
            '      <div class="pane sup-new" data-doc="limits"><h1>限流与配额</h1><p>每个 API Key 都可以单独设置额度和访问范围，超出范围的请求会被拒绝。</p>'
            '<h3>按 Key 设置</h3><div class="tbl"><table><tr><th>设置</th><th>作用</th></tr>'
            '<tr><td>额度上限（¥）</td><td>这个 Key 累计可以花多少钱，用完后请求被拒绝</td></tr>'
            '<tr><td>过期时间</td><td>到期后 Key 自动失效</td></tr>'
            '<tr><td>可用模型</td><td>只允许调用选中的模型</td></tr>'
            '<tr><td>IP 白名单</td><td>只接受来自这些 IP 的请求</td></tr></table></div>'
            '<p>在控制台「API Key」里创建或编辑 Key 时设置。</p>'
            '<h3>速率限制</h3><p>每分钟请求数（RPM）与每分钟词元数（TPM）有上限，超出时返回 429。' + tbc('待公司确认：默认上限与提额方式') + '</p>'
            '<h3>遇到 429 怎么办</h3><p>响应带 Retry-After 头时，按它等待后重试；没有时按指数退避重试（1 秒、2 秒、4 秒……），并限制最大重试次数。需要更高并发请联系商务。</p></div>\n')
rep('      <div class="pane" data-doc="errors"><h1>错误码</h1>', DOCS_NEW + '      <div class="pane" data-doc="errors"><h1>错误码</h1>')

# ---------- 7 站内搜索：导航入口 ----------
SICON = '<svg viewBox="0 0 16 16" aria-hidden="true"><circle cx="7" cy="7" r="5" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M11 11l3.5 3.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>'
rep('<a href="#console" data-nav="console" class="login">登录</a><a href="#" class="lang" role="button">EN</a></nav>',
    f'<a href="#" class="sup-sbtn sup-new" role="button" aria-label="搜索" title="搜索（⌘K）">{SICON}<kbd>⌘K</kbd></a><a href="#console" data-nav="console" class="login">登录</a><a href="#" class="lang" role="button">EN</a></nav>')
rep('<a href="#guides" data-nav="guides">指南</a><a class="lang" href="#" role="button">EN</a></nav>',
    '<a href="#guides" data-nav="guides">指南</a><a href="#" class="sup-sbtn-m sup-new" role="button">搜索</a><a class="lang" href="#" role="button">EN</a></nav>')

SKIP = False
# ---------- 8 控制台：在线试用、预算、代金券 ----------
CHAT_ICON = '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M4 4h12a2 2 0 0 1 2 2v7a2 2 0 0 1-2 2H9l-4 3v-3H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/></svg>'
rep('<span>模型 API</span></button>', f'<span>模型 API</span></button>\n        <button type="button" data-p="play" class="sup-new">{CHAT_ICON}<span>在线试用</span></button>')
PLAY = ('      <div class="cs-p" data-p="play">\n        <div class="bt-pg">\n'
        '          <div class="bt-hd"><h1>在线试用</h1><button class="bt-btn" type="button" id="supPgCode">查看代码</button></div>\n'
        '          <p class="bt-lede">选一个模型直接对话，先看效果再接入。在线试用按实际用量从余额扣费。</p>\n'
        '          <p class="sup-warn">' + tbc() + ' 需要在平台开启对话功能，并完成生成式人工智能服务备案；计费方式（扣余额或送试用额度）待定。本预览不发起真实调用。</p>\n'
        '          <div class="sup-pg">\n'
        '            <div class="sup-pg-side">\n'
        '              <div class="cs-f"><label for="supPgM">模型</label><select class="in" id="supPgM"></select></div>\n'
        '              <div class="cs-f"><label for="supPgT">温度 <span class="mono" id="supPgTv">0.7</span></label><input type="range" min="0" max="2" step="0.1" value="0.7" id="supPgT"></div>\n'
        '              <div class="cs-f"><label for="supPgN">最大输出词元</label><input class="in mono" id="supPgN" value="1024" inputmode="numeric" autocomplete="off"></div>\n'
        '              <div class="cs-f"><label for="supPgS">系统提示词</label><textarea class="in" id="supPgS" rows="4" placeholder="可选，例如：用中文简洁回答"></textarea></div>\n'
        '            </div>\n'
        '            <div class="sup-pg-main">\n'
        '              <div class="sup-pg-log" id="supPgLog" aria-live="polite"><p class="sup-pg-empty">在下方输入问题，开始对话。</p></div>\n'
        '              <form class="sup-pg-in" id="supPgF" novalidate><textarea class="in" id="supPgQ" rows="2" placeholder="输入问题，Enter 发送，Shift + Enter 换行" aria-label="输入问题"></textarea><button class="bt-btn pri" type="submit">发送</button></form>\n'
        '              <p class="sup-pg-ft">内容由人工智能生成，仅供参考。请遵守<a class="ul" href="#terms">用户服务协议</a>。</p>\n'
        '              <div class="code pre sup-pg-code" id="supPgC" hidden><button class="cp" data-copy>复制</button><span id="supPgCt"></span></div>\n'
        '            </div>\n'
        '          </div>\n'
        '        </div>\n      </div>\n')
rep('      <div class="cs-p" data-p="explore">', PLAY + '      <div class="cs-p" data-p="explore">')
BUD = ('        <h3 class="cs-h3">账单</h3>\n        <div class="cs-empty">还没有账单</div>\n'
       '        <div class="sup-new sup-bud"><h3 class="cs-h3">月度预算与提醒</h3>\n'
       '          <p class="cs-help">设一个每月花费上限，用到设定比例时通知你；也可以选择超出后暂停调用。' + tbc('需平台支持') + '</p>\n'
       '          <form class="sup-bud-f" id="supBud" novalidate>\n'
       '            <div class="cs-f"><label for="supBudA">每月预算（¥）</label><input class="in mono" id="supBudA" inputmode="decimal" autocomplete="off" placeholder="例如 500"></div>\n'
       '            <div class="cs-f"><span class="cs-lb">提醒比例</span><div class="sup-chk"><label><input type="checkbox" checked value="75"> 75%</label><label><input type="checkbox" checked value="90"> 90%</label><label><input type="checkbox" checked value="100"> 100%</label></div></div>\n'
       '            <div class="cs-f"><label class="sup-sw"><input type="checkbox" id="supBudStop"> 超出预算后暂停所有 API Key 的调用</label></div>\n'
       '            <div><button class="btn black sm" type="submit">保存预算</button></div>\n'
       '          </form></div>\n'
       '        <h3 class="cs-h3 sup-new">代金券</h3>\n        <div class="cs-empty sup-new">还没有代金券。活动或商务赠送的代金券会显示在这里，优先于余额扣费。' + tbc() + '</div>\n')
rep('        <h3 class="cs-h3">账单</h3>\n        <div class="cs-empty">还没有账单</div>\n', BUD)

SKIP = CONSOLE_ONLY
# ---------- 9 页脚 ----------
rep('<a href="#network">电站网络</a><a href="#news">新闻动态</a></div>',
    '<a href="#network">电站网络</a><a href="#news">新闻动态</a><a class="sup-new" href="#changelog">更新日志</a><a class="sup-new" href="#status">服务状态</a><a class="sup-new" href="llms.txt" target="_blank" rel="noopener">llms.txt</a></div>')
rep('<div class="social" id="footSocial"></div></div>',
    '<div class="social" id="footSocial"></div><p class="sup-new sup-comm">微信社群与公众号 ' + tbc('待公司提供二维码') + '</p></div>')

SKIP = False
# ---------- 评审按钮与搜索框 ----------
if CONSOLE_ONLY:
    rep('<div class="dock" id="dock" aria-hidden="true">', '<button class="sup-tog" id="supTog" type="button" aria-pressed="false">标出新增</button>\n<div class="dock" id="dock" aria-hidden="true">')
    SKIP = True
rep('<div class="dock" id="dock" aria-hidden="true">',
    '<button class="sup-tog" id="supTog" type="button" aria-pressed="false">标出新增</button>\n'
    '<div class="sup-s" id="supS" hidden><div class="sup-s-bg" data-close></div><div class="sup-s-box" role="dialog" aria-modal="true" aria-label="站内搜索">'
    f'<label class="sup-s-q">{SICON}<input type="search" id="supQ" placeholder="搜索模型、文档、指南、接口" aria-label="搜索" autocomplete="off" spellcheck="false" aria-controls="supR"><kbd>Esc</kbd></label>'
    '<ul class="sup-s-r" id="supR" role="listbox" aria-label="搜索结果"></ul><p class="sup-s-ft">↑ ↓ 选择 · Enter 打开 · Esc 关闭</p></div></div>\n'
    '<div class="dock" id="dock" aria-hidden="true">')

SKIP = False
# ---------- CSS ----------
CSS = r'''
<style id="sup-css">
/* 全部补充预览（2026-10-14） */
.tbc{display:inline-flex;align-items:center;margin:0 2px;padding:1px 9px;border-radius:999px;background:rgba(255,214,10,.42);border:1px solid rgba(212,161,6,.55);color:#5C4500;font:500 12px/1.6 var(--sans);letter-spacing:0;white-space:normal;vertical-align:1px;text-align:left}
html.sup-mark .sup-new{outline:2px dashed #2F63B8;outline-offset:3px;border-radius:6px}
.sup-tog{position:fixed;right:20px;bottom:76px;z-index:60;height:36px;padding:0 14px;border-radius:999px;border:1px solid var(--glass-line,rgba(0,0,0,.1));background:var(--glass,rgba(255,255,255,.8));backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);font:500 13px var(--sans);color:var(--ink);cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,.08)}
.sup-tog[aria-pressed="true"]{background:#2F63B8;border-color:#2F63B8;color:#fff}
/* 搜索 */
.pill nav a.sup-sbtn{display:inline-flex;align-items:center;gap:6px;opacity:.45}
.pill nav a.sup-sbtn:hover{opacity:1}
.sup-sbtn svg{width:15px;height:15px}
.sup-sbtn kbd{font:500 11px var(--mono);padding:1px 5px;border:1px solid var(--line);border-radius:5px}
.sup-s{position:fixed;inset:0;z-index:200;display:flex;justify-content:center;align-items:flex-start;padding:12vh 16px 16px}
.sup-s[hidden]{display:none}
.sup-s-bg{position:absolute;inset:0;background:rgba(0,0,0,.28);backdrop-filter:blur(2px);-webkit-backdrop-filter:blur(2px)}
.sup-s-box{position:relative;width:min(640px,100%);max-height:70vh;display:flex;flex-direction:column;background:var(--card);border:1px solid var(--line);border-radius:var(--r16,16px);box-shadow:0 24px 60px -20px rgba(0,0,0,.35);overflow:hidden}
.sup-s-q{display:flex;align-items:center;gap:10px;padding:14px 16px;border-bottom:1px solid var(--line)}
.sup-s-q svg{width:18px;height:18px;flex:none;color:var(--ink-50)}
.sup-s-q input{flex:1;min-width:0;border:0;outline:0;background:transparent;font:400 17px var(--sans);color:var(--ink)}
.sup-s-q input::-webkit-search-cancel-button{display:none}
.sup-s-q kbd{font:500 11px var(--mono);color:var(--ink-50);padding:2px 6px;border:1px solid var(--line);border-radius:5px}
.sup-s-r{list-style:none;margin:0;padding:6px;overflow:auto}
.sup-s-r li{display:grid;grid-template-columns:56px minmax(0,1fr);gap:2px 12px;padding:10px 12px;border-radius:10px;cursor:pointer}
.sup-s-r li[aria-selected="true"]{background:var(--gray-btn,rgba(0,0,0,.05))}
.sup-s-r .k{grid-row:span 2;align-self:start;margin-top:2px;font:500 11px var(--mono);letter-spacing:.04em;color:var(--ink-50)}
.sup-s-r b{font-weight:500;font-size:15px;color:var(--ink);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.sup-s-r span.s{font-size:13px;color:var(--ink-50);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.sup-s-r .none{display:block;padding:18px 12px;color:var(--ink-50);font-size:14px;cursor:default}
.sup-s-ft{margin:0;padding:10px 16px;border-top:1px solid var(--line);font:400 12px var(--mono);color:var(--ink-50)}
/* 定价 */
.sup-bar{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:0 0 14px}
.sup-q{display:inline-flex;align-items:center;gap:8px;height:38px;padding:0 14px;border:1px solid var(--line);border-radius:999px;background:var(--card)}
.sup-q svg{width:15px;height:15px;color:var(--ink-50)}
.sup-q input{border:0;outline:0;background:transparent;font:400 14px var(--sans);color:var(--ink);width:150px}
.sup-chips{display:flex;flex-wrap:wrap;gap:6px}
.pr-tbl td.r{white-space:nowrap}
.pr-tbl td.r small{display:block;font-size:11px;color:var(--ink-50);font-family:var(--sans)}
.pr-tbl tr.sup-sub td{padding-top:0;border-top:0;color:var(--ink-70)}
.sup-na{font:400 12px var(--sans);color:var(--ink-50)}
.sup-none{color:var(--ink-50);font-size:14px}
.sup-tod{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
.sup-card{padding:18px 20px;border:1px solid var(--line);border-radius:var(--r16,16px);background:var(--card)}
.sup-card .k{display:block;margin-bottom:8px}
.sup-card b{display:block;font-size:22px;font-weight:500;letter-spacing:-.01em}
.sup-card p{margin:8px 0 0;font-size:13px;color:var(--ink-70)}
.sup-card.dim{background:transparent;border-style:dashed}
.sup-now{margin:14px 0 0;font-size:14px;color:var(--ink-70)}
.sup-now b{color:var(--ink);font-weight:500}
/* 状态页 */
.st-now{margin-top:8px;padding:22px 24px;border:1px solid var(--line);border-radius:var(--r20,20px);background:var(--card)}
.st-hd{display:flex;align-items:center;gap:12px;margin-bottom:14px}
.st-hd b{font-size:18px;font-weight:500;flex:1}
.st-dot{width:12px;height:12px;border-radius:50%;background:var(--ink-30);flex:none}
.st-dot.ok{background:#2F9E5B;box-shadow:0 0 0 4px rgba(47,158,91,.16)}
.st-dot.bad{background:#E5484D;box-shadow:0 0 0 4px rgba(229,72,77,.16)}
.st-tbl td,.st-tbl th{white-space:nowrap}
.st-ok{color:#2F7A4A}.st-bad{color:#C2363B}
.st-empty{padding:22px 20px;border:1px dashed var(--line);border-radius:var(--r16,16px);color:var(--ink-70);font-size:14px}
/* 文档 */
.docs .pane{position:relative}
.sup-cpp{position:absolute;top:6px;right:0}
.docs .pane > h1{padding-right:110px}
/* 控制台：在线试用 */
.sup-warn{margin:0 0 18px;font-size:13px;line-height:1.7;color:var(--ink-70)}
.sup-pg{display:grid;grid-template-columns:240px minmax(0,1fr);gap:24px;align-items:start}
.sup-pg-side{display:grid;gap:14px}
.sup-pg-side .cs-f label{display:flex;justify-content:space-between;font-size:13px;color:var(--ink-70);margin-bottom:6px}
.sup-pg-side input[type=range]{width:100%}
.sup-pg-side textarea{resize:vertical;min-height:84px}
.sup-pg-main{display:grid;gap:12px;min-width:0}
.sup-pg-log{min-height:300px;max-height:460px;overflow:auto;padding:18px;border:1px solid var(--line);border-radius:var(--r16,16px);background:var(--card);display:flex;flex-direction:column;gap:12px}
.sup-pg-empty{margin:auto;color:var(--ink-50);font-size:14px}
.sup-msg{max-width:82%;padding:10px 14px;border-radius:14px;font-size:14px;line-height:1.65;white-space:pre-wrap;word-break:break-word}
.sup-msg.u{align-self:flex-end;background:#000;color:#fff;border-bottom-right-radius:4px}
.sup-msg.a{align-self:flex-start;background:var(--gray-btn,rgba(0,0,0,.05));color:var(--ink-70);border-bottom-left-radius:4px}
.sup-msg.a .m{display:block;margin-bottom:4px;font:500 11px var(--mono);color:var(--ink-50)}
.sup-pg-in{display:flex;gap:10px;align-items:flex-end}
.sup-pg-in textarea{flex:1;min-width:0;resize:none}
.sup-pg-ft{margin:0;font-size:12px;color:var(--ink-50)}
.sup-pg-code{margin:0;white-space:pre-wrap;overflow-wrap:anywhere}
/* 控制台：预算 */
.sup-bud{margin-top:18px}
.sup-bud-f{display:grid;gap:12px;max-width:520px}
.sup-chk{display:flex;gap:16px;flex-wrap:wrap;font-size:14px}
.sup-chk label,.sup-sw{display:inline-flex;align-items:center;gap:6px;font-size:14px;color:var(--ink-70)}
/* 页脚 */
.sup-comm{margin:12px 0 0;font-size:13px;color:var(--ink-50)}
/* 模型详情 */
.sup-back{display:block;width:fit-content;margin-bottom:14px;font-size:14px}
#modelPane .detail>*{min-width:0}
.sup-idcp{margin-left:8px;padding:1px 8px;border:1px solid var(--line);border-radius:999px;background:transparent;font:500 11px var(--sans);color:var(--ink-70);cursor:pointer;vertical-align:1px}
.sup-mt{display:flex;gap:6px;margin:8px 0 0}
@media (max-width:860px){
  .sup-tod{grid-template-columns:1fr}
  .sup-pg{grid-template-columns:1fr}
  .sup-pg-main{order:-1}  /* 手机上对话区在前，参数在后 */
  .sup-pg-log{min-height:220px}
  .sup-msg{max-width:92%}
  .sup-q input{width:120px}
  .st-now{padding:18px 16px}
  .st-tbl td:nth-child(2),.st-tbl th:nth-child(2){display:none}
  .sup-tog{right:14px;bottom:68px}
  .docs .pane > h1{padding-right:0}
  .sup-cpp{position:static;margin:0 0 10px}
}
@media (prefers-color-scheme: dark){ :root:not([data-theme="light"]) .tbc{color:#3D2E00} }
</style>
'''
k = s.rindex('</head>'); s = s[:k] + CSS + s[k:]

# ---------- JS（放进主脚本作用域，能用 M、G、L、byId、route、csTab 等） ----------
PX = {
    'glm-5-3': {'i': 8, 'c': 2, 'o': 28},
    'glm-5-3-flash': {'i': 0.8, 'c': 0.23, 'o': 2.8},
    'deepseek-v4-pro': {'i': 4.5, 'c': 0.45, 'o': 13.5, 'idle': True, 'busy': {'i': 9, 'c': 0.9, 'o': 27}},
    'deepseek-v4-flash': {'chk': True},
}
JS = r'''
  /* ======== 全部补充预览（2026-10-14） ======== */
  (function(){
    var PX=__PX__;
    function y(n){return '¥'+(+n).toFixed(2)}
    var TBC=function(t){return '<span class="tbc">'+(t||'待公司确认')+'</span>'};
    /* 评审：标出新增 */
    var tog=$('#supTog'); if(tog) tog.addEventListener('click',function(){var on=document.documentElement.classList.toggle('sup-mark');tog.setAttribute('aria-pressed',on?'true':'false')});

    /* ---- 定价：三列价格 + 筛选 ---- */
    var prV='all',prT='all';
    var vendors=[]; M.forEach(function(m){if(vendors.indexOf(m.vendor)<0)vendors.push(m.vendor)});
    var types=[]; M.forEach(function(m){m.type.forEach(function(t){if(types.indexOf(t)<0)types.push(t)})});
    var pc=$('#supPrC');
    if(pc){ pc.innerHTML='<button class="chip on" type="button" data-f="all">全部</button>'+vendors.map(function(v){return '<button class="chip" type="button" data-v="'+v+'">'+v+'</button>'}).join('')+types.map(function(t){return '<button class="chip" type="button" data-t="'+t+'">'+t+'</button>'}).join('');
      $$('#supPrC .chip').forEach(function(b){b.addEventListener('click',function(){
        if(b.hasAttribute('data-f')){prV='all';prT='all'} else if(b.hasAttribute('data-v')){prV=prV===b.getAttribute('data-v')?'all':b.getAttribute('data-v')} else {prT=prT===b.getAttribute('data-t')?'all':b.getAttribute('data-t')}
        $$('#supPrC .chip').forEach(function(x){var on=x.hasAttribute('data-f')?(prV==='all'&&prT==='all'):x.hasAttribute('data-v')?x.getAttribute('data-v')===prV:x.getAttribute('data-t')===prT;x.classList.toggle('on',on)});
        renderPr()})}); }
    function cell(v,lab){return v==null?'<span class="sup-na">待同步</span>':y(v)+(lab?'<small>'+lab+'</small>':'')}
    function renderPr(){var q=(($('#supPrQ')||{}).value||'').trim().toLowerCase();
      var rows=M.filter(function(m){return (prV==='all'||m.vendor===prV)&&(prT==='all'||m.type.indexOf(prT)>=0)&&(!q||(m.name+' '+m.vendor+' '+m.type.join(' ')).toLowerCase().indexOf(q)>=0)});
      $('#prRows').innerHTML=rows.map(function(m){var p=PX[m.id]||{}, lab=p.idle?'闲时':'';
        var out=p.chk?y(m.mkt)+'<small>'+'型号待核对'+'</small>':cell(p.o!=null?p.o:m.mkt,lab);
        var r='<tr><td>'+m.name+'</td><td>'+m.vendor+'</td><td>'+m.type.join(' · ')+'</td><td class="mono">'+m.ctx+'</td><td class="r mono">'+cell(p.i,lab)+'</td><td class="r mono">'+cell(p.c,lab)+'</td><td class="r mono">'+out+'</td><td><a class="btn gray sm" href="#model-'+m.id+'">查看详情</a></td></tr>';
        if(p.busy) r+='<tr class="sup-sub"><td><span class="k">忙时 08:00–22:00</span></td><td></td><td></td><td></td><td class="r mono">'+y(p.busy.i)+'</td><td class="r mono">'+y(p.busy.c)+'</td><td class="r mono">'+y(p.busy.o)+'</td><td></td></tr>';
        return r}).join('');
      $('#supPr0').hidden=rows.length>0}
    if($('#prRows')){ renderPr(); var pq=$('#supPrQ'); if(pq) pq.addEventListener('input',renderPr) }
    /* 当前时段（北京时间） */
    function bjNow(){return new Date(Date.now()+(new Date().getTimezoneOffset()+480)*6e4)}  /* 用本地时间读出北京时间 */
    function updNow(){var el=$('#supNow'); if(!el) return; var d=bjNow(), h=d.getHours(), mm=('0'+d.getMinutes()).slice(-2), idle=(h>=22||h<8);
      el.innerHTML='现在北京时间 <b class="mono">'+h+':'+mm+'</b>，DeepSeek 按<b>'+(idle?'闲时':'忙时')+'</b>价计费。'}
    updNow(); setInterval(updNow,30000);
    /* 计算器：自动填输入价 */
    var sel=$('#pcModel'), inP=$('#pcInP');
    function fillIn(){var p=PX[sel.value]; inP.value=p&&p.i!=null?p.i:''; inP.dispatchEvent(new Event('input'))}
    if(sel&&inP){ sel.addEventListener('change',fillIn); fillIn() }

    /* ---- 模型详情：补充价格、模型 ID、多语言示例、在线试用入口 ---- */
    function codeFor(m,k){var H='https://__HOST__/v1';
      if(k==='py') return '<span class="g"># pip install openai</span><br>import os<br>from openai import OpenAI<br><br>client = OpenAI(<br>    base_url=<span class="s">"'+H+'"</span>,<br>    api_key=os.environ[<span class="s">"API_KEY"</span>],<br>)<br>resp = client.chat.completions.create(<br>    model=<span class="s">"'+m.name+'"</span>,<br>    messages=[{<span class="s">"role"</span>: <span class="s">"user"</span>, <span class="s">"content"</span>: <span class="s">"你好"</span>}],<br>)<br>print(resp.choices[0].message.content)';
      return '<span class="g">// npm install openai</span><br>import OpenAI from <span class="s">"openai"</span>;<br><br>const client = new OpenAI({<br>  baseURL: <span class="s">"'+H+'"</span>,<br>  apiKey: process.env.API_KEY,<br>});<br>const resp = await client.chat.completions.create({<br>  model: <span class="s">"'+m.name+'"</span>,<br>  messages: [{ role: <span class="s">"user"</span>, content: <span class="s">"你好"</span> }],<br>});<br>console.log(resp.choices[0].message.content);'}
    var _rm=renderModel;
    renderModel=function(id){_rm(id); var m=byId[id]||M[0], p=PX[m.id]||{}, pane=$('#modelPane'); if(!pane) return;
      var head=pane.querySelector('.detail > div'); if(head&&!head.querySelector('.sup-back')) head.insertAdjacentHTML('afterbegin','<a class="ul sup-back sup-new" href="#models">← 全部模型</a>');
      var dl=pane.querySelector('dl.meta');
      if(dl){ dl.insertAdjacentHTML('afterbegin','<dt class="sup-new">模型 ID</dt><dd class="mono sup-new">'+m.name+'<button class="sup-idcp" type="button" data-cpid="'+m.name+'">复制</button></dd>');
        var extra='';  /* 输入 / 缓存价放在下方三格价格里，这里只补忙时与核对说明 */
        if(p.busy) extra+='<dt class="sup-new">忙时 08:00–22:00</dt><dd class="mono sup-new">输入 '+y(p.busy.i)+' · 缓存 '+y(p.busy.c)+' · 输出 '+y(p.busy.o)+'</dd>';
        if(p.chk) extra+='<dt class="sup-new">价格核对</dt><dd class="sup-new">'+TBC('报价单为 DeepSeek-V4.1-Flash，输出 ¥4（闲时）/ ¥8（忙时），型号与价格待平台核对')+'</dd>';
        if(extra){ var dts=dl.querySelectorAll('dt'); for(var i=0;i<dts.length;i++){ if(dts[i].textContent==='输出参考价'||dts[i].__zh==='输出参考价'||/Output reference/.test(dts[i].textContent)){ dts[i].nextElementSibling.insertAdjacentHTML('afterend',extra); break } } } }
      var pr=pane.querySelector('.price');
      if(pr) pr.outerHTML='<div class="price sup-new"><div>输入'+(p.idle?'（闲时）':'')+'<span>'+(p.i!=null?y(p.i):'待同步')+'</span></div><div>缓存命中<span>'+(p.c!=null?y(p.c):'待同步')+'</span></div><div>输出<span>'+y(p.o!=null?p.o:m.mkt)+'</span></div></div>'+(p.i!=null?'<p class="pr-note sup-new" style="margin-top:8px">输入与缓存价来自 2026-10-08 报价单。'+TBC('公开前请公司确认')+' 合同价请联系商务。</p>':'<p class="pr-note sup-new" style="margin-top:8px">输入与缓存价待平台同步。合同价请联系商务。</p>');
      $$('#modelPane a.btn.black').forEach(function(a){ if(/获取 API Key|Get API Key/.test(a.textContent)){ a.textContent='免费试用 API →'; a.classList.add('sup-new') } });
      var code=pane.querySelector('.code');
      if(code&&!pane.querySelector('.sup-mt')){ code.setAttribute('data-ml','curl');
        code.insertAdjacentHTML('beforebegin','<div class="sup-mt sup-new" role="tablist"><button class="chip on" type="button" data-ml="curl">curl</button><button class="chip" type="button" data-ml="py">Python</button><button class="chip" type="button" data-ml="node">Node.js</button></div>');
        code.insertAdjacentHTML('afterend','<div class="code pre sup-new" data-ml="py" hidden style="margin-top:8px"><button class="cp" data-copy>复制</button>'+codeFor(m,'py')+'</div><div class="code pre sup-new" data-ml="node" hidden style="margin-top:8px"><button class="cp" data-copy>复制</button>'+codeFor(m,'node')+'</div>');
        $$('#modelPane .sup-mt .chip').forEach(function(b){b.addEventListener('click',function(){var k=b.getAttribute('data-ml');$$('#modelPane .sup-mt .chip').forEach(function(x){x.classList.toggle('on',x===b)});$$('#modelPane .code[data-ml]').forEach(function(c){c.hidden=c.getAttribute('data-ml')!==k})})}); }
      var play=pane.querySelector('.play');
      if(play) play.outerHTML='<div class="play sup-new"><h3>在线试用</h3><p class="sub">在控制台「在线试用」里直接和 '+m.name+' 对话，先看效果再接入。'+TBC('需平台开启对话功能并完成生成式 AI 服务备案')+'</p><div class="row"><a class="btn black" href="#console-preview" data-sup-play="'+m.id+'">去在线试用 →</a></div></div>';
      var pl=pane.querySelector('[data-sup-play]'); if(pl) pl.addEventListener('click',function(e){e.preventDefault(); goPlay(pl.getAttribute('data-sup-play'))});
      var cp=pane.querySelector('.sup-idcp'); if(cp) cp.addEventListener('click',function(){copyText(cp.getAttribute('data-cpid'),function(){toast('已复制模型 ID')})});
      bindCopy();
    };

    /* ---- 控制台：在线试用 ---- */
    function goPlay(id){location.hash='#console-preview'; setTimeout(function(){csTab('play'); var s2=$('#supPgM'); if(s2&&id){s2.value=id; s2.dispatchEvent(new Event('change'))}},150)}
    var pgM=$('#supPgM');
    if(pgM){ pgM.innerHTML=M.map(function(m){return '<option value="'+m.id+'">'+m.name+'</option>'}).join('');
      var pgT=$('#supPgT'), pgTv=$('#supPgTv'); pgT.addEventListener('input',function(){pgTv.textContent=(+pgT.value).toFixed(1); pgCode()});
      function esc(t){return String(t).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
      var hist=[];
      function pgCode(){var m=byId[pgM.value]||M[0], msgs=[]; var sys=$('#supPgS').value.trim(); if(sys) msgs.push({role:'system',content:sys}); hist.forEach(function(x){msgs.push(x)}); if(!msgs.length||msgs[msgs.length-1].role!=='user') msgs.push({role:'user',content:$('#supPgQ').value.trim()||'你好'});
        var body={model:m.name,messages:msgs,temperature:+pgT.value,max_tokens:parseInt($('#supPgN').value,10)||1024};
        $('#supPgCt').innerHTML='curl <span class="s">https://__HOST__/v1/chat/completions</span> \\<br>  -H <span class="s">"Authorization: Bearer $API_KEY"</span> \\<br>  -H <span class="s">"Content-Type: application/json"</span> \\<br>  -d <span class="s">\''+esc(JSON.stringify(body))+'\'</span>'}
      ['#supPgM','#supPgN','#supPgS','#supPgQ'].forEach(function(k){$(k).addEventListener('input',pgCode)}); pgM.addEventListener('change',pgCode); pgCode();
      $('#supPgCode').addEventListener('click',function(){var c=$('#supPgC'); c.hidden=!c.hidden; pgCode(); bindCopy()});
      $('#supPgF').addEventListener('submit',function(e){e.preventDefault(); var q=$('#supPgQ').value.trim(); if(!q) return; var m=byId[pgM.value]||M[0], log=$('#supPgLog'); var em=log.querySelector('.sup-pg-empty'); if(em) em.remove();
        hist.push({role:'user',content:q});
        log.insertAdjacentHTML('beforeend','<div class="sup-msg u">'+esc(q)+'</div><div class="sup-msg a"><span class="m">'+m.name+'</span>预览不发起真实调用。开通后，这里显示 '+m.name+' 的回答，以及本次用掉的输入、输出词元与费用。</div>');
        log.scrollTop=log.scrollHeight; $('#supPgQ').value=''; pgCode()});
      $('#supPgQ').addEventListener('keydown',function(e){if(e.key==='Enter'&&!e.shiftKey&&!e.isComposing){e.preventDefault(); $('#supPgF').requestSubmit()}});
    }
    /* ---- 控制台：预算 ---- */
    var bud=$('#supBud'); if(bud) bud.addEventListener('submit',function(e){e.preventDefault(); toast('预览：预算设置没有保存到平台，需要平台支持后才能生效。')});

    /* ---- 文档：复制本页、跳转到指定页 ---- */
    $$('.docs .pane').forEach(function(p){ var h=p.querySelector('h1'); if(!h) return; h.insertAdjacentHTML('afterend','<button class="btn gray sm sup-cpp sup-new" type="button">复制本页</button>');
      p.querySelector('.sup-cpp').addEventListener('click',function(){var c=p.cloneNode(true); $$('button',c).forEach(function(b){b.remove()}); $$('.tbc',c).forEach(function(b){b.remove()});
        var t=c.innerText||c.textContent; t='# '+(h.textContent)+'\n\n'+t.replace(/^.*\n/,'').replace(/\n{3,}/g,'\n\n').trim()+'\n\n来源：'+location.href.split('#')[0]+'#docs'; copyText(t,function(){toast('已复制本页内容')})}) });
    function openDoc(k){location.hash='#docs'; setTimeout(function(){var b=$('#docIdx [data-doc="'+k+'"]'); if(b) b.click()},40)}
    document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('[data-sup-doc]'); if(a){e.preventDefault(); openDoc(a.getAttribute('data-sup-doc'))}});

    /* ---- 服务状态 ---- */
    function check(){var dot=$('#stDot'), sum=$('#stSum'), api=$('#stApi'), ms=$('#stMs'); if(!dot) return;
      dot.className='st-dot'; sum.textContent='正在检测'; api.textContent='正在检测'; api.className=''; ms.textContent='—';
      var t0=performance.now(), done=false, to=setTimeout(function(){if(done)return; done=true; fail()},8000);
      function fail(){dot.className='st-dot bad'; sum.textContent='无法连接 API 网关'; api.textContent='无法连接'; api.className='st-bad'}
      fetch('https://__HOST__/v1/models?_='+Date.now(),{mode:'no-cors',cache:'no-store'}).then(function(){if(done)return; done=true; clearTimeout(to); var d=Math.round(performance.now()-t0); dot.className='st-dot ok'; sum.textContent='API 网关可以连通'; api.textContent='可以连通'; api.className='st-ok'; ms.textContent=d+' ms'},function(){if(done)return; done=true; clearTimeout(to); fail()})}
    var stRe=$('#stRe'); if(stRe) stRe.addEventListener('click',check);
    window.addEventListener('hashchange',function(){if(location.hash==='#status') setTimeout(check,30)}); if(location.hash==='#status') setTimeout(check,30);

    /* ---- 站内搜索 ---- */
    var IX=[];
    [['#models','产品与服务'],['#pricing','定价'],['#enterprise','企业合作'],['#network','电站合作'],['#about','关于我们'],['#docs','文档'],['#api','接口参考'],['#guides','接入与采购指南'],['#edu','教育优惠'],['#news','新闻动态'],['#changelog','更新日志'],['#status','服务状态'],['#compliance','合规与安全'],['#privacy','隐私政策'],['#terms','用户服务协议'],['#console','控制台']].forEach(function(r){IX.push({k:'页面',t:r[1],s:location.pathname.split('/').pop()+r[0],go:function(){location.hash=r[0]}})});
    M.forEach(function(m){IX.push({k:'模型',t:m.name,s:m.vendor+' · '+m.type.join(' · ')+' · '+m.ctx+' · 输出 '+y(m.mkt),go:function(){location.hash='#model-'+m.id}})});
    $$('.docs .pane').forEach(function(p){var h=p.querySelector('h1'); if(!h) return; var k=p.getAttribute('data-doc'); IX.push({k:'文档',t:h.textContent,s:(p.textContent||'').replace(h.textContent,'').replace('复制本页','').replace(/\s+/g,' ').trim().slice(0,160),go:function(){openDoc(k)}})});
    (typeof G!=='undefined'?G:[]).forEach(function(g){IX.push({k:'指南',t:g.t,s:g.s||'',go:function(){location.hash='#guide-'+g.id}})});
    try{ JSON.parse($('#apData').textContent).groups.forEach(function(g){g.ops.forEach(function(o){IX.push({k:'接口',t:o.m+' '+o.p,s:g.zh+' · '+o.sum+(o.sub?' · '+o.sub:''),go:function(){location.hash='#api'; setTimeout(function(){var el=document.getElementById(o.id); if(el) window.scrollTo(0,Math.max(0,window.scrollY+el.getBoundingClientRect().top-100))},120)}})})}) }catch(e){}
    var S=$('#supS'), Q=$('#supQ'), R=$('#supR'), hits=[], cur=0, lastFocus=null;
    function en(t){try{if(lang==='en'){var r=trKey(t); return r||''}}catch(e){} return ''}
    function find(q){q=q.trim().toLowerCase(); if(!q) return IX.filter(function(x){return x.k==='页面'}).slice(0,8);
      var out=[]; IX.forEach(function(x){var t=x.t.toLowerCase(), sc=-1; if(t.indexOf(q)===0) sc=0; else if(t.indexOf(q)>=0) sc=1; else if((en(x.t)||'').toLowerCase().indexOf(q)>=0) sc=1; else if(x.s.toLowerCase().indexOf(q)>=0) sc=2; if(sc>=0) out.push([sc,x])}); out.sort(function(a,b){return a[0]-b[0]}); return out.slice(0,20).map(function(a){return a[1]})}
    function draw(){hits=find(Q.value); cur=0; R.innerHTML=hits.length?hits.map(function(x,i){return '<li role="option" id="supO'+i+'" aria-selected="'+(i===0)+'" data-i="'+i+'"><span class="k">'+x.k+'</span><b>'+x.t.replace(/</g,'&lt;')+'</b><span class="s">'+x.s.replace(/</g,'&lt;')+'</span></li>'}).join(''):'<li class="none" role="option" aria-disabled="true">没有找到相关内容</li>'; Q.setAttribute('aria-activedescendant',hits.length?'supO0':'')}
    function mark(i){cur=(i+hits.length)%hits.length; $$('#supR li[data-i]').forEach(function(li){li.setAttribute('aria-selected',+li.getAttribute('data-i')===cur?'true':'false')}); var el=$('#supO'+cur); if(el){el.scrollIntoView({block:'nearest'}); Q.setAttribute('aria-activedescendant','supO'+cur)}}
    function openS(){lastFocus=document.activeElement; S.hidden=false; Q.value=''; draw(); setTimeout(function(){Q.focus()},0); closeMenu()}
    function closeS(){S.hidden=true; if(lastFocus&&lastFocus.focus) lastFocus.focus()}
    function pick(i){var x=hits[i]; if(!x) return; closeS(); x.go()}
    if(S){ Q.addEventListener('input',draw);
      Q.addEventListener('keydown',function(e){if(e.key==='ArrowDown'){e.preventDefault();mark(cur+1)} else if(e.key==='ArrowUp'){e.preventDefault();mark(cur-1)} else if(e.key==='Enter'&&!e.isComposing){e.preventDefault();pick(cur)} else if(e.key==='Escape'){e.preventDefault();closeS()}});
      R.addEventListener('click',function(e){var li=e.target.closest('li[data-i]'); if(li) pick(+li.getAttribute('data-i'))});
      S.querySelector('[data-close]').addEventListener('click',closeS);
      document.addEventListener('keydown',function(e){var tag=(e.target.tagName||'').toLowerCase(), typing=tag==='input'||tag==='textarea'||tag==='select'||e.target.isContentEditable;
        if((e.metaKey||e.ctrlKey)&&(e.key==='k'||e.key==='K')){e.preventDefault(); S.hidden?openS():closeS()} else if(e.key==='/'&&!typing&&S.hidden){e.preventDefault(); openS()} else if(e.key==='Escape'&&!S.hidden){closeS()}});
      $$('.sup-sbtn,.sup-sbtn-m').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault(); openS()})}); }
  })();
'''.replace('__PX__', json.dumps(PX)).replace('__HOST__', HOST)
if CONSOLE_ONLY:
    JS = r'''
  /* ======== 控制台补充（上线版，2026-10-14） ======== */
  (function(){
    var tog=$('#supTog'); if(tog) tog.addEventListener('click',function(){var on=document.documentElement.classList.toggle('sup-mark');tog.setAttribute('aria-pressed',on?'true':'false')});
    var bud=$('#supBud'); if(bud) bud.addEventListener('submit',function(e){e.preventDefault(); toast('预览：预算设置没有保存到平台，需要平台支持后才能生效。')});
  })();
'''
rep("  $$('[data-product-target]').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();jumpTo(a.getAttribute('data-product-target'))})});\n  window.addEventListener('hashchange',route); route();",
    JS + "  $$('[data-product-target]').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();jumpTo(a.getAttribute('data-product-target'))})});\n  window.addEventListener('hashchange',route); route();")

# ---------- 英文 ----------
EN_FORCE = {
    '# 沐仞 API 接入地址': '# FathomPeak API endpoint',
    f'各客户端的菜单名称会随版本变化，以客户端当前版本为准。接入地址为 https://{HOST}/v1。': f'Menu names change between client versions; follow the version you have installed. The endpoint is https://{HOST}/v1.',
    f'接入地址为 https://{HOST}/v1。各客户端的菜单名称会随版本变化，以客户端当前版本为准。': f'The endpoint is https://{HOST}/v1. Menu names change between client versions; follow the version you have installed.',
    FAQ_NEW: 'Price depends on the model, usage and billing hours. DeepSeek currently has off-peak and peak prices; see time-of-day pricing on the pricing page.',
    FAQ2_NEW: 'Each model is priced separately; see the price table above. Cached input is billed at the cache price, the rest at the input price.',
    '，取自上方模型价格表。输入单价按价格表自动填入，可以修改。估算不含教育价与合同价。': ', taken from the price table above. The input price is filled in from the table and can be edited. Estimates exclude education and contract prices.',
}
EN = {
    '单位 ¥ / 百万词元。目录与输出参考价来自沐仞模型平台，输入与缓存命中价来自 2026-10-08 报价单的刊例价。DeepSeek 分闲时、忙时计价，MiniMax-M3 为 ≤512k 档。':
        'Prices in ¥ per million tokens. The catalog and output reference prices come from the FathomPeak model platform; input and cache-hit prices are list prices from the 8 October 2026 quote. DeepSeek has off-peak and peak prices; MiniMax-M3 is the ≤512k tier.',
    '查找模型': 'Find a model', '输入': 'Input', '缓存命中': 'Cache hit', '输出': 'Output', '待同步': 'Not yet synced', '闲时': 'Off-peak', '忙时': 'Peak',
    '型号待核对': 'Model to verify', '忙时 08:00–22:00': 'Peak 08:00–22:00', '没有符合条件的模型': 'No models match',
    '输入与缓存命中价来自 2026-10-08 报价单（刊例价，含税）。': 'Input and cache-hit prices come from the 8 October 2026 quote (list prices, tax included).',
    '报价单注明为商业机密，公开前请公司确认': 'The quote is marked confidential; company approval needed before publishing',
    '标"待同步"的价格目前没有出处，需要平台补齐。': 'Prices marked "Not yet synced" have no source yet; the platform needs to fill them in.',
    '分时价格': 'Time-of-day pricing', '同一个模型在不同时段价格不同，按请求发出时的北京时间计价。': 'The same model can cost different amounts at different times. Billing uses Beijing time when the request is sent.',
    'DeepSeek-V4-Pro · 闲时': 'DeepSeek-V4-Pro · off-peak', 'DeepSeek-V4-Pro · 忙时': 'DeepSeek-V4-Pro · peak',
    '输入 ¥4.50 · 缓存 ¥0.45 · 输出 ¥13.50': 'Input ¥4.50 · cache ¥0.45 · output ¥13.50', '输入 ¥9.00 · 缓存 ¥0.90 · 输出 ¥27.00': 'Input ¥9.00 · cache ¥0.90 · output ¥27.00',
    '绿电时段价': 'Green-power hours', '规划中': 'Planned', '按电站富余绿电的时段定价，时段与价格确定后在这里公布。': 'Pricing by the hours when plants have surplus green power. Hours and prices will be published here once set.',
    '时段与价格来自 2026-10-08 报价单。': 'Hours and prices come from the 8 October 2026 quote.',
    '待公司确认': 'Company to confirm', '现在北京时间': 'Beijing time now', '，DeepSeek 按': '. DeepSeek is billed at ', '价计费。': ' prices.',
    '按上方价格表自动填入': 'Filled in from the price table',
    '官网': 'Website', '平台': 'Platform', '沐仞科技': 'FathomPeak', '发布 ·': 'Published ·',
    '接口参考上线': 'API reference launched', '接口参考页的内容取自沐仞模型平台的 OpenAPI 文档，按模型、对话、嵌入、重排序等分组列出请求参数与返回。': "The API reference comes from the FathomPeak model platform's OpenAPI docs, grouped into models, chat, embeddings, rerank and more, with request parameters and responses.",
    '首页改版': 'Homepage redesign', '新首页讲清为什么在电站旁生产词元、怎么接入、适合哪些行业，并列出已签约与推进中的项目案例。': 'The new homepage explains why tokens are produced beside power plants, how to connect, which industries it suits, and lists signed and in-progress projects.',
    '合规与法律页面、费用估算': 'Compliance and legal pages, cost estimator', '新增合规与安全、用户服务协议、隐私政策三个页面；定价页加入费用估算。': 'Added Compliance & Security, Terms of Service and Privacy Policy pages; the pricing page gained a cost estimator.',
    '模型目录收录 7 个模型': '7 models in the catalog', 'DeepSeek-V4-Flash、DeepSeek-V4-Pro、Qwen3.8-Flash、GLM-5.3-Flash、GLM-5.3、MiniMax-M2.7、MiniMax-M3，上下文均为 1M，用同一个 API Key 调用。': 'DeepSeek-V4-Flash, DeepSeek-V4-Pro, Qwen3.8-Flash, GLM-5.3-Flash, GLM-5.3, MiniMax-M2.7 and MiniMax-M3, all with 1M context, all called with one API key.',
    '平台英文界面': 'Platform English interface', '平台英文版基本完成，可以中英切换，并按浏览器语言自动识别。': "The platform's English version is mostly done: it switches between Chinese and English and follows the browser language.",
    '来自内部进度汇报，对外发布前请公司确认': 'From an internal progress report; company to confirm before publishing',
    '企业组织与成员': 'Organizations and members', '企业客户由管理员为成员派发账号，个人用户自助注册；登录后自己创建 API Key，查看使用日志和钱包。': 'Business admins issue accounts to members; individuals sign up themselves. After signing in, users create their own API keys and see usage logs and their wallet.',
    '服务状态': 'Status', '实时检测': 'Live check', '服务状态 - 沐仞科技 FathomPeak': 'Status - FathomPeak', '在你的浏览器里实时检测沐仞 API 能否连通。历史可用率接入监控后在这里公布。': 'Checks from your browser, in real time, whether the FathomPeak API can be reached. Historical uptime will be published here once monitoring is connected.',
    '正在检测': 'Checking', '重新检测': 'Check again', '组件': 'Component', '地址': 'Address', '状态': 'Status', '往返': 'Round trip', 'API 网关': 'API gateway', '控制台与注册': 'Console and sign-up', '各模型可用性': 'Per-model availability', '7 个模型': '7 models', '待接入监控': 'Monitoring not connected',
    '检测由你的浏览器直接请求 api.fathompeak.cn，只说明网络能连通，不代表每个模型都可用。': 'Your browser requests api.fathompeak.cn directly. A pass only means the network is reachable, not that every model is available.',
    '近 90 天可用率': 'Uptime, last 90 days', '每个组件每天一格，接入监控后自动更新。': 'One cell per component per day, updated automatically once monitoring is connected.', '还没有监控数据。': 'No monitoring data yet.',
    '待公司确认：监控工具与对外公布口径': 'Company to confirm: monitoring tool and what to publish', '故障与维护公告': 'Incidents and maintenance', '计划维护会提前在这里和控制台通知里公告。': 'Planned maintenance will be announced here and in console notifications in advance.',
    '暂无公告。': 'No notices.', '待公司确认：公告流程与通知渠道': 'Company to confirm: notice process and channels',
    'API 网关可以连通': 'API gateway reachable', '可以连通': 'Reachable', '无法连接 API 网关': 'Cannot reach the API gateway', '无法连接': 'Unreachable',
    '账户与实名': 'Accounts & verification', '充值与发票': 'Top-ups & invoices', '限流与配额': 'Rate limits & quotas', '服务状态 →': 'Status →',
    '沐仞有个人、企业、教育三种账户，注册时选择，用同一个控制台。': 'FathomPeak has personal, business and education accounts. You choose at sign-up; all use the same console.',
    '注册': 'Sign up', '注册入口：': 'Sign up at ', '。注册后登录，创建 API Key。': '. Then sign in and create an API key.',
    '账户类型': 'Account type', '适合': 'For', '说明': 'Notes', '个人': 'Personal', '开发者、个人项目': 'Developers and personal projects', '自助注册，自己创建和管理 API Key。': 'Self-serve sign-up; create and manage your own API keys.',
    '企业': 'Business', '团队与公司采购': 'Teams and company purchasing', '管理员邀请同事加入并分配角色，额度和账单由企业账户统一管理；可以签合同、对公转账、按月结算。': 'Admins invite colleagues and assign roles; credit and billing are managed by the business account. Contracts, bank transfers and monthly billing are available.',
    '教育': 'Education', '学生、老师与实验室': 'Students, teachers and labs', 'edu.cn 邮箱注册后自动认证；没有学校邮箱，可以上传学生证或在读证明。': 'Signing up with an edu.cn email verifies automatically; without a school email, upload a student ID or enrollment certificate.',
    '实名认证': 'Identity verification', '个人与企业是否需要实名认证、怎么认证': 'Whether individuals and businesses need identity verification, and how ',
    '按 Token 用量计费，充值后从余额扣费，没有月费。': 'Billed by token usage, deducted from your balance after you top up. No monthly fee.',
    '在线充值': 'Online top-up', '在控制台「钱包与账单」里选择金额和支付方式（支付宝或微信），也可以输入兑换码。': 'In the console, open Wallet & billing, choose an amount and a payment method (Alipay or WeChat), or enter a redemption code.',
    '待公司确认：到账时间与最低金额': 'Company to confirm: crediting time and minimum amount', '企业付款': 'Business payment',
    '企业客户可以预付，也可以按月结算，以合同约定为准。对公转账请邮件': 'Business customers can prepay or settle monthly, as set in the contract. For bank transfers, email ',
    '待公司提供：对公账户信息': 'Company to provide: bank account details', '价格与税': 'Prices and tax', '价格均为含税价（增值税 6%）。': 'All prices include tax (6% VAT).',
    '来自 10-08 报价单，待公司确认': 'From the 8 October quote; company to confirm', '发票': 'Invoices', '支持电子发票与增值税发票。': 'Electronic invoices and VAT invoices are available.',
    '待公司确认：开票入口、所需信息与开票时间': 'Company to confirm: where to request, details needed and turnaround', '退款': 'Refunds', '待公司确认：余额能否退、怎么退': 'Company to confirm: whether and how balances are refunded',
    '每个 API Key 都可以单独设置额度和访问范围，超出范围的请求会被拒绝。': 'Each API key can have its own credit limit and access scope; requests outside it are rejected.',
    '按 Key 设置': 'Per-key settings', '设置': 'Setting', '作用': 'Effect', '额度上限（¥）': 'Credit limit (¥)', '这个 Key 累计可以花多少钱，用完后请求被拒绝': 'How much this key can spend in total; requests are rejected once it is used up',
    '过期时间': 'Expiry', '到期后 Key 自动失效': 'The key stops working when it expires', '可用模型': 'Allowed models', '只允许调用选中的模型': 'Only the selected models can be called',
    'IP 白名单': 'IP allowlist', '只接受来自这些 IP 的请求': 'Only requests from these IPs are accepted', '在控制台「API Key」里创建或编辑 Key 时设置。': 'Set these when you create or edit a key under API keys in the console.',
    '速率限制': 'Rate limits', '每分钟请求数（RPM）与每分钟词元数（TPM）有上限，超出时返回 429。': 'Requests per minute (RPM) and tokens per minute (TPM) are capped; going over returns 429.',
    '待公司确认：默认上限与提额方式': 'Company to confirm: default limits and how to raise them', '遇到 429 怎么办': 'Handling 429',
    '响应带 Retry-After 头时，按它等待后重试；没有时按指数退避重试（1 秒、2 秒、4 秒……），并限制最大重试次数。需要更高并发请联系商务。': 'If the response has a Retry-After header, wait that long and retry; otherwise retry with exponential backoff (1 s, 2 s, 4 s…) and cap the number of retries. Contact sales for higher concurrency.',
    '先看状态码和错误信息，再按下表处理。': 'Check the status code and error message, then follow the table.',
    '请求参数有误，例如模型名称写错、消息格式不对': 'Bad request parameters, such as a misspelled model name or malformed messages', '对照接口参考检查请求体；模型名称以模型目录为准': 'Check the request body against the API reference; use model names from the catalog',
    '余额不足、Key 额度用完，或模型、IP 不在 Key 的允许范围内': "Insufficient balance, the key's credit is used up, or the model or IP is outside the key's allowed scope ",
    '待平台确认返回码': 'Platform to confirm the status code', '充值，或在控制台调整 Key 的额度、可用模型与 IP 白名单': "Top up, or adjust the key's credit limit, allowed models and IP allowlist in the console",
    '见': 'See ', '；需要更高并发请联系商务': '; contact sales for higher concurrency', '平台或上游模型暂时故障': 'Temporary failure on the platform or upstream model', '稍后重试，并查看': 'Retry later and check ',
    '错误返回示例': 'Error response example', '不带 Key 或 Key 无效时，返回 401 和下面的 JSON（2026-10-14 实测）：': 'Without a key, or with an invalid key, the API returns 401 and this JSON (tested 14 October 2026):',
    '每个错误都带 request id，联系支持时请一并提供。': 'Every error includes a request id; include it when you contact support.', '实时连通情况见': 'For live reachability, see ',
    '复制本页': 'Copy page', '已复制本页内容': 'Page copied',
    '搜索': 'Search', '搜索（⌘K）': 'Search (⌘K)', '搜索模型、文档、指南、接口': 'Search models, docs, guides and APIs', '搜索结果': 'Search results', '站内搜索': 'Site search',
    '↑ ↓ 选择 · Enter 打开 · Esc 关闭': '↑ ↓ select · Enter open · Esc close', '没有找到相关内容': 'Nothing found', '页面': 'Page', '文档': 'Docs', '指南': 'Guide', '接口': 'API', '模型': 'Model',
    '在线试用': 'Playground', '查看代码': 'View code', '选一个模型直接对话，先看效果再接入。在线试用按实际用量从余额扣费。': 'Chat with a model directly to see the results before you integrate. Playground usage is deducted from your balance.',
    '需要在平台开启对话功能，并完成生成式人工智能服务备案；计费方式（扣余额或送试用额度）待定。本预览不发起真实调用。': 'Requires the chat feature to be enabled on the platform and generative AI service filing. Billing (balance or trial credit) is undecided. This preview makes no real calls.',
    '温度': 'Temperature', '最大输出词元': 'Max output tokens', '系统提示词': 'System prompt', '可选，例如：用中文简洁回答': 'Optional, e.g. answer briefly in English',
    '在下方输入问题，开始对话。': 'Type a question below to start.', '输入问题，Enter 发送，Shift + Enter 换行': 'Type a question; Enter to send, Shift + Enter for a new line', '输入问题': 'Question', '发送': 'Send',
    '内容由人工智能生成，仅供参考。请遵守': 'Content is AI-generated and for reference only. Please follow the ', '用户服务协议': 'Terms of Service',
    '月度预算与提醒': 'Monthly budget and alerts', '设一个每月花费上限，用到设定比例时通知你；也可以选择超出后暂停调用。': 'Set a monthly spending cap and get notified at the thresholds you choose; optionally pause calls once it is exceeded.',
    '需平台支持': 'Needs platform support', '每月预算（¥）': 'Monthly budget (¥)', '例如 500': 'e.g. 500', '提醒比例': 'Alert at', '超出预算后暂停所有 API Key 的调用': 'Pause all API keys once the budget is exceeded', '保存预算': 'Save budget',
    '预览：预算设置没有保存到平台，需要平台支持后才能生效。': 'Preview: the budget was not saved to the platform; it needs platform support first.',
    '代金券': 'Vouchers', '还没有代金券。活动或商务赠送的代金券会显示在这里，优先于余额扣费。': 'No vouchers yet. Vouchers from promotions or sales appear here and are used before your balance.',
    '更新日志': 'Changelog', '微信社群与公众号': 'WeChat community and official account ', '待公司提供二维码': 'QR codes to be provided by the company',
    '标出新增': 'Mark additions', '← 全部模型': '← All models', '模型 ID': 'Model ID', '复制': 'Copy', '已复制模型 ID': 'Model ID copied',
    '输入（闲时）': 'Input (off-peak)', '缓存命中（闲时）': 'Cache hit (off-peak)', '价格核对': 'Price check',
    '报价单为 DeepSeek-V4.1-Flash，输出 ¥4（闲时）/ ¥8（忙时），型号与价格待平台核对': 'The quote lists DeepSeek-V4.1-Flash at ¥4 (off-peak) / ¥8 (peak) output; model and price to be verified on the platform',
    '输入与缓存价来自 2026-10-08 报价单。': 'Input and cache prices come from the 8 October 2026 quote.', '公开前请公司确认': 'Company to confirm before publishing', '合同价请联系商务。': 'Contact sales for contract prices.',
    '输入与缓存价待平台同步。合同价请联系商务。': 'Input and cache prices are not yet synced from the platform. Contact sales for contract prices.',
    '需平台开启对话功能并完成生成式 AI 服务备案': 'Requires chat to be enabled on the platform and generative AI service filing', '去在线试用 →': 'Open the playground →',
}
RX_ADD = (",\n    [/^在控制台「在线试用」里直接和 (.+) 对话，先看效果再接入。$/, function(m,a){return 'Chat with '+a+' in the console playground to see results before you integrate. '}],\n"
          "    [/^预览不发起真实调用。开通后，这里显示 (.+) 的回答，以及本次用掉的输入、输出词元与费用。$/, function(m,a){return 'This preview makes no real calls. Once enabled, this shows the answer from '+a+', plus the input and output tokens and cost of the call.'}]")
rep('\n  ];\n  function rxTr(k){', RX_ADD + '\n  ];\n  function rxTr(k){')  # 原数组最后一项没有逗号，补规则时前置逗号
if CONSOLE_ONLY:  # 上线版：只留页面里用到的词条，没上线的定价、报价单等文字不进源码
    EN = {k2: v for k2, v in EN.items() if k2 in s}
    EN_FORCE = {k2: v for k2, v in EN_FORCE.items() if k2 in s}
rep('  syncAuthLocale(); applyLang();', '  (function(F,S){Object.assign(I18N,F); for(var k in S) if(!(k in I18N)) I18N[k]=S[k]})(' + json.dumps(EN_FORCE, ensure_ascii=False) + ',' + json.dumps(EN, ensure_ascii=False) + ');  /* 全部补充预览的英文：改写过的键强制覆盖，新键只补缺 */\n  syncAuthLocale(); applyLang();')

open(OUT, 'w', encoding='utf8').write(s)
print('done:', OUT, f'(YOUR_API_HOST 替换 {n_host} 处)')

# ---------- llms.txt ----------
if LLMS:
    a = s.index('  var M=') + len('  var M=')
    depth = 0
    for i2 in range(a, len(s)):
        if s[i2] == '[': depth += 1
        elif s[i2] == ']':
            depth -= 1
            if depth == 0: b = i2 + 1; break
    MODELS = json.loads(s[a:b])
    lines = ['# 沐仞科技 FathomPeak', '',
             '> 北京沐仞科技有限公司，做算电协同与绿色词元。大模型 API：GLM、DeepSeek、Qwen、MiniMax 等模型用同一个 API Key 调用，兼容 OpenAI 与 Gemini 原生格式。', '',
             f'- API 接入地址（OpenAI 兼容）：https://{HOST}/v1',
             '- 注册：https://account.fathompeak.cn/sign-up',
             '- 联系：fathompeak@163.com', '',
             '## 文档',
             f'- [快速开始]({SITE}#docs)：API Key、接入地址与第一条请求',
             f'- [接口参考]({SITE}#api)：取自沐仞模型平台的 OpenAPI 文档',
             f'- [接入与采购指南]({SITE}#guides)',
             f'- [定价]({SITE}#pricing)：按 Token 用量计费，单位 ¥ / 百万词元',
             f'- [服务状态]({SITE}#status)',
             f'- [更新日志]({SITE}#changelog)', '',
             '## 模型（输出参考价，¥ / 百万词元）']
    for m in MODELS:
        lines.append(f"- [{m['name']}]({SITE}#model-{m['id']})：{m['vendor']} · {' · '.join(m['type'])} · 上下文 {m['ctx']} · 输出参考价 ¥{m['mkt']:.2f}")
    lines += ['', '## 公司',
              f'- [关于沐仞]({SITE}#about)',
              f'- [合规与安全]({SITE}#compliance)',
              f'- [用户服务协议]({SITE}#terms)',
              f'- [隐私政策]({SITE}#privacy)', '']
    open(LLMS, 'w', encoding='utf8').write('\n'.join(lines))
    print('done:', LLMS)
