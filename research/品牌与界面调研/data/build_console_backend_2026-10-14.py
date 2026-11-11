"""控制台（后台）架构补齐预览（Zixin 2026-10-14："你在最新版上面修改；然后后台架构呢 我更关心后台"）。不动线上。
叠加顺序：线上 index.html（origin/main）→ build_full_supplement_2026-10-14.py → 本脚本。
依据：对比结论（原平台 new-api / Dia·Baseten·OpenRouter / 硅基流动）、角色口径（超管 / B 端管理员建成员共用组织钱包 / C 端个人）、
控制台角色与钱包思考_2026-10-14.md。只做前端流程，数据一律空状态；平台还没有的能力标黄「待公司确认 / 需平台支持」。
改动：
 1 三种预览身份：#console-preview（个人）、#console-preview-admin（企业管理员）、#console-preview-member（企业成员）；左上角显示账户类型 · 角色。
 2 侧栏按目标架构重排：顶部（概览 / 模型 API / 在线试用 / 探索）→ 开发（API Key / 使用日志 / 用量分析 / 订单与产地卡 / 绿电批量任务）
   → 组织（成员 / 账单分摊，仅管理员）→ 账户设置（钱包与账单 / 发票 / 实名认证 / 通用设置 / 安全与访问）。
 3 新页：用量分析（请求、词元、费用、首字时延、输出速度、429、错误率、限流，导出 CSV）、绿电批量任务（介绍 + 申请）、
   成员（管理员添加普通成员、额度上限，替代原「成员与角色」邀请选角色）、账单分摊（按成员 / 按 Key，导出）、发票（抬头、申请、记录）、实名认证（个人 / 企业）。
 4 钱包：归属行（个人钱包 / 组织钱包）；成员看不到充值、兑换、预算，改看可用额度；对公转账收款信息位置。
 5 通用设置：通知方式加 Bark、Gotify（原平台有）；新增「通知哪些事」。安全与访问：新增登录设备。使用日志：导出 CSV。
用法：python3 -I build_console_backend_2026-10-14.py <输入 html> <输出 html>
"""
import json, re, sys

SRC, OUT = sys.argv[1], sys.argv[2]
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


# ---------- 0 恢复控制台花体首字母（Zixin 2026-10-14 晚："没有我们的花体和字体设计"）----------
# 49b44ea 把控制台的 HandLatin 首字母整个关掉了（误读了"API Key 花体也修了"）。按设计交接：控制台中英文模式下，以拉丁字母开头的衬线标题都加花体首字母；中文标题不用花体。
rep("/* 手写首字母只用于控制台以外的页面、英文模式下以拉丁字母开头的衬线大标题；控制台（.bt）里不加（Zixin 2026-10-14：去掉\"API Key\"花体） */",
    "/* 手写首字母：控制台以外的页面只在英文模式加；控制台（.bt）里中英文模式都加，只修饰以拉丁字母开头的衬线标题（设计交接；2026-10-14 晚恢复） */")
rep("var inC=!!el.closest('.bt'), on=!inC&&lang==='en'&&/^[A-Za-z]/.test(el.textContent.trim());",
    "var inC=!!el.closest('.bt'), on=(lang==='en'||inC)&&/^[A-Za-z]/.test(el.textContent.trim());")

# ---------- 1 侧栏重排 ----------
a = s.index('<nav class="cs-nav bt-nav" aria-label="控制台">'); b = s.index('</nav>', a)
nav = s[a:b]
btn = {}
for m in re.finditer(r'<button[^>]*data-p="([a-z]+)"[^>]*>.*?</button>', nav, re.S):
    btn[m.group(1)] = m.group(0)
need = ['home', 'models', 'play', 'explore', 'keys', 'usage', 'orders', 'bill', 'acct', 'sec']
miss = [k for k in need if k not in btn]
if miss: sys.exit(f'[停止] 侧栏缺少按钮 {miss}（先跑 build_full_supplement）')
grp_old = re.search(r'<span class="cs-grp bt-grp">([^<]+)</span>', nav).group(1)  # 原"账户设置"组名


def nb(p, label, d, sr=None):
    return f'<button type="button" data-p="{p}" class="sup-new"' + (f' data-sr="{sr}"' if sr else '') + f'>{ico(d)}<span>{label}</span></button>'


RULE = '<i class="bt-rule" aria-hidden="true"></i>'
NEW_NAV = ('<nav class="cs-nav bt-nav" aria-label="控制台">\n        '
           + '\n        '.join([btn['home'], btn['models'], btn['play'], btn['explore'], RULE,
                                '<span class="cs-grp bt-grp sup-new">开发</span>', btn['keys'], btn['usage'],
                                nb('stats', '用量分析', 'M4 16.5V10M8.7 16.5V4.5M13.3 16.5v-8M18 16.5H2'), btn['orders'],
                                nb('batch', '绿电批量任务', 'M10 3 17 6.8 10 10.6 3 6.8Z M3 10.4l7 3.8 7-3.8 M3 13.8l7 3.7 7-3.7'), RULE,
                                '<span class="cs-grp bt-grp sup-new" data-sr="admin">组织</span>',
                                nb('members', '成员', 'M7.5 9.6a2.8 2.8 0 1 0 0-5.6 2.8 2.8 0 0 0 0 5.6Z M2.5 16.5c.6-2.9 2.6-4.4 5-4.4s4.4 1.5 5 4.4 M13 4.3a2.7 2.7 0 0 1 0 5.2 M14.6 12.2c1.6.5 2.6 1.9 3 4.3', 'admin'),
                                nb('split', '账单分摊', 'M10 3a7 7 0 1 0 7 7h-7Z M12.5 2.6A7 7 0 0 1 17.4 7.5H12.5Z', 'admin'),
                                RULE.replace('<i ', '<i data-sr="admin" '),
                                f'<span class="cs-grp bt-grp">{grp_old}</span>', btn['bill'],
                                nb('invoice', '发票', 'M5 2.5h10v15l-2.5-1.5L10 17.5 7.5 16 5 17.5Z M7.5 6.5 10 9l2.5-2.5M10 9v5M8 11.2h4', 'pay'),
                                nb('kyc', '实名认证', 'M4.5 4.5h11a2 2 0 0 1 2 2v7a2 2 0 0 1-2 2h-11a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2Z M7 11.3a1.8 1.8 0 1 0 0-3.6 1.8 1.8 0 0 0 0 3.6Z M11.5 8.5H15M11.5 11.5H15', 'pay'),
                                btn['acct'], btn['sec']]) + '\n      ')
s = s[:a] + NEW_NAV + s[b:]

# ---------- 2 新页面 ----------
PANES = f'''      <div class="cs-p" data-p="stats">
        <div class="cs-hd"><div><h2>用量分析</h2><p>按时间、API Key 和模型查看请求量、词元、费用与性能。</p></div><button class="btn gray sm" type="button" id="supStCsv">导出 CSV</button></div>
        <div class="sup-flt"><div class="cs-seg" id="supStSeg" role="group" aria-label="时间范围"><button class="chip" type="button" data-sd="1" aria-pressed="false">今天</button><button class="chip on" type="button" data-sd="7" aria-pressed="true">近 7 天</button><button class="chip" type="button" data-sd="30" aria-pressed="false">近 30 天</button></div><select class="mk-sel" id="supStK" aria-label="API Key"></select><select class="mk-sel" id="supStM" aria-label="模型"></select></div>
        <div class="cs-tiles n4"><div><span class="k">请求次数</span><b class="mono" id="supS1">0</b></div><div><span class="k">输入词元</span><b class="mono" id="supS2">0</b></div><div><span class="k">输出词元</span><b class="mono" id="supS3">0</b></div><div><span class="k">费用</span><b class="mono" id="supS4">¥0.00</b></div></div>
        <h3 class="cs-h3">性能</h3>
        <div class="cs-tiles n4"><div><span class="k">平均首字时延</span><b class="mono" id="supS5">--</b></div><div><span class="k">平均输出速度</span><b class="mono" id="supS6">--</b><span class="cs-help">词元 / 秒</span></div><div><span class="k">被限流（429）</span><b class="mono" id="supS7">0</b></div><div><span class="k">错误率</span><b class="mono" id="supS8">--</b></div></div>
        <p class="cs-fine">{tbc('需平台在每条记录里写入首字时延、输出速度与状态码')}</p>
        <h3 class="cs-h3">限流</h3>
        <div class="cs-box"><p>账户的每分钟请求数（RPM）与每分钟词元数（TPM）上限显示在这里，超出时返回 429。当前上限：RPM -- · TPM --</p><p class="cs-fine">{tbc('待公司确认：默认上限、是否按消费分级、怎么提额')}</p></div>
      </div>
      <div class="cs-p" data-p="batch">
        <div class="cs-hd"><div><h2>绿电批量任务</h2><p>不急着要结果的请求，打包成一批交给调度，排到电站富余绿电的时段执行。</p></div><button class="btn black sm" type="button" id="supBatchGo">申请开通</button></div>
        <ol class="sup-steps"><li><b>上传</b><span>把请求写成 JSONL 文件，每行一个请求。</span></li><li><b>排队</b><span>调度把任务排到电站富余绿电的时段执行。</span></li><li><b>下载</b><span>完成后下载结果文件，用量与费用计入账单和订单产地卡。</span></li></ol>
        <div class="cs-empty"><b>还没有批量任务</b><span>开通后，任务进度与结果文件显示在这里。</span></div>
        <p class="cs-fine">{tbc('需平台开发批量接口；完成时限与价格待公司确认')}</p>
      </div>
      <div class="cs-p" data-p="members">
        <div class="cs-hd"><div><h2>成员</h2><p>管理员添加的成员共用组织钱包，各自创建和使用自己的 API Key。</p></div></div>
        <form class="cs-newf sup-memf" id="supMemF" novalidate><input class="in" type="email" name="email" placeholder="成员邮箱" aria-label="成员邮箱" autocomplete="off"><input class="in mono" name="cap" inputmode="decimal" placeholder="每月额度上限（¥，可不填）" aria-label="每月额度上限" autocomplete="off"><button class="btn black sm" type="submit">添加成员</button></form>
        <p class="cs-help">添加后，平台把登录方式发到成员邮箱。{tbc('待公司确认：能否有多个管理员、成员额度上限是否支持')}</p>
        <div class="tbl"><table class="cs-tbl"><thead><tr><th>成员</th><th>角色</th><th>状态</th><th class="r">本月消费</th><th class="r">每月额度上限</th><th>加入时间</th><th><span class="sr">操作</span></th></tr></thead><tbody id="supMem"></tbody></table></div>
      </div>
      <div class="cs-p" data-p="split">
        <div class="cs-hd"><div><h2>账单分摊</h2><p>组织钱包的消费按成员和 API Key 拆开，方便内部结算。</p></div><button class="btn gray sm" type="button" id="supSpCsv">导出 CSV</button></div>
        <div class="cs-seg sup-seg" id="supSpSeg" role="group" aria-label="分摊方式"><button class="chip on" type="button" data-sp="m" aria-pressed="true">按成员</button><button class="chip" type="button" data-sp="k" aria-pressed="false">按 API Key</button></div>
        <div class="tbl"><table class="cs-tbl"><thead id="supSpH"></thead><tbody id="supSpB"></tbody></table></div>
        <div class="cs-empty" id="supSp0"><b>本月还没有消费</b><span>成员发出请求后，这里按成员或 API Key 汇总费用。</span></div>
        <p class="cs-fine">{tbc('按成员分摊需要平台在使用记录里写入成员')}</p>
      </div>
      <div class="cs-p" data-p="invoice">
        <div class="cs-hd"><div><h2>发票</h2><p>维护发票抬头，按可开票金额申请电子发票。</p></div></div>
        <div class="cs-tiles"><div><span class="k">可开票金额</span><b class="mono" id="supInvA">¥0.00</b><span class="cs-help">按已消费金额计算</span></div><div><span class="k">开票中</span><b class="mono">¥0.00</b></div><div><span class="k">已开票</span><b class="mono">¥0.00</b></div></div>
        <p class="cs-fine">{tbc('待公司确认：按消费还是按充值开票、开票时限、海外客户的 Invoice')}</p>
        <h3 class="cs-h3">发票抬头</h3>
        <form class="sup-invf" id="supInvF" novalidate>
          <div class="cs-f"><span class="cs-lb" id="supInvTL">发票类型</span><div class="cs-pm" role="radiogroup" aria-labelledby="supInvTL"><button type="button" role="radio" aria-checked="true" data-v="normal">数电普票</button><button type="button" role="radio" aria-checked="false" tabindex="-1" data-v="special">数电专票</button></div></div>
          <div class="cs-f"><label for="supInvN">抬头名称</label><input class="in" id="supInvN" name="title" autocomplete="off" placeholder="公司全称或个人姓名"></div>
          <div class="cs-f"><label for="supInvTax">纳税人识别号</label><input class="in mono" id="supInvTax" name="tax" autocomplete="off" placeholder="企业抬头必填"></div>
          <div class="cs-f" data-inv="special" hidden><label for="supInvAddr">注册地址与电话</label><input class="in" id="supInvAddr" name="addr" autocomplete="off"></div>
          <div class="cs-f" data-inv="special" hidden><label for="supInvBank">开户行与账号</label><input class="in" id="supInvBank" name="bank" autocomplete="off"></div>
          <div class="cs-f"><label for="supInvMail">接收邮箱</label><input class="in" id="supInvMail" name="mail" type="email" autocomplete="off"></div>
          <p class="ac-msg" id="supInvMsg" role="alert"></p>
          <div><button class="btn black sm" type="submit">保存抬头</button></div>
        </form>
        <h3 class="cs-h3">申请开票</h3>
        <div class="cs-newf"><input class="in mono" id="supInvAmt" inputmode="decimal" placeholder="开票金额（¥）" aria-label="开票金额" autocomplete="off"><button class="btn black sm" type="button" id="supInvGo">申请开票</button></div>
        <h3 class="cs-h3">开票记录</h3>
        <div class="tbl"><table class="cs-tbl"><thead><tr><th>申请时间</th><th>类型</th><th>抬头</th><th class="r">金额</th><th>状态</th><th><span class="sr">下载</span></th></tr></thead><tbody></tbody></table></div>
        <div class="cs-empty"><b>还没有开票记录</b><span>申请后，开票进度和发票下载显示在这里。</span></div>
      </div>
      <div class="cs-p" data-p="kyc">
        <div class="cs-hd"><div><h2>实名认证</h2><p>核验个人或企业身份。认证结果用于开票主体与合同签署。</p></div></div>
        <p class="cs-st" id="supKycSt">未认证</p>
        <ul class="cs-sl">
          <li><div><b>个人认证</b><p>姓名、身份证号与人脸核验，适合个人开发者。</p></div><button class="btn gray sm" type="button" data-kyc>开始认证</button></li>
          <li><div><b>企业认证</b><p>上传营业执照，再由法定代表人人脸核验，或用对公账户小额打款验证。认证后，发票抬头与合同主体为企业。</p></div><button class="btn gray sm" type="button" data-kyc>开始认证</button></li>
          <li><div><b>海外用户</b><p>海外个人与企业的身份核验方式另行提供。</p></div></li>
        </ul>
        <p class="cs-fine">{tbc('待公司确认：是否必须实名、未实名能用哪些功能、认证服务商')}</p>
      </div>
'''
rep('      <div class="cs-p" data-p="acct">', PANES + '      <div class="cs-p" data-p="acct">')

# ---------- 3 钱包：归属、按角色显示 ----------
rep('<div class="cs-p" data-p="bill">\n        <div class="cs-hd"><div><h2>钱包</h2><p>余额以人民币显示，按实际用量扣费。</p></div></div>\n',
    '<div class="cs-p" data-p="bill">\n        <div class="cs-hd"><div><h2>钱包</h2><p>余额以人民币显示，按实际用量扣费。</p></div></div>\n'
    '        <p class="sup-own sup-new" id="supOwn"></p>\n'
    '        <div class="cs-box sup-new" data-sr="member"><b>你的可用额度：不限</b><p>管理员没有给你设额度上限，用量从组织钱包扣除。需要充值或提额，请联系组织管理员。</p></div>\n')
rep('        <h3 class="cs-h3">充值</h3>\n        <div class="cs-pay">', '        <h3 class="cs-h3" data-sr="pay">充值</h3>\n        <div class="cs-pay" data-sr="pay">')
rep('        <h3 class="cs-h3">兑换码</h3>\n        <form class="cs-newf" id="csRedeem"', '        <h3 class="cs-h3" data-sr="pay">兑换码</h3>\n        <form class="cs-newf" id="csRedeem" data-sr="pay"')
rep('<div class="sup-new sup-bud">', '<div class="sup-new sup-bud" data-sr="pay">')
rep('<h3 class="cs-h3 sup-new">代金券</h3>\n        <div class="cs-empty sup-new">', '<h3 class="cs-h3 sup-new" data-sr="pay">代金券</h3>\n        <div class="cs-empty sup-new" data-sr="pay">')  # 代金券跟钱包主人走，成员看不到
rep('        <p class="cs-fine">企业客户可以对公转账或按月结算，邮件 <a class="ul" href="mailto:fathompeak@163.com">fathompeak@163.com</a>。</p>',
    '        <p class="cs-fine" data-sr="pay">企业客户可以对公转账或按月结算，邮件 <a class="ul" href="mailto:fathompeak@163.com">fathompeak@163.com</a>。</p>\n'
    '        <div class="cs-box sup-new" data-sr="pay"><h3 class="cs-h3">对公转账</h3><p>收款户名：北京沐仞科技有限公司。开户行与账号' + tbc('待公司提供') + '。转账后把凭证发到 fathompeak@163.com，财务确认后入账。</p></div>')

# ---------- 4 成员：原「成员与角色」移到组织 › 成员 ----------
rep('<div class="cs-box cs-mem" data-for="company" hidden>', '<div class="cs-box cs-mem" data-for="moved" hidden>')
rep('<form class="cs-ntf" id="csNtf" novalidate>', '<p class="cs-fine sup-new" data-for="company" data-sr="admin" hidden>成员管理已移到侧栏「组织 › 成员」。</p>\n        <form class="cs-ntf" id="csNtf" novalidate>')

# ---------- 5 通知：Bark、Gotify、通知哪些事 ----------
rep('<button type="button" role="radio" aria-checked="false" tabindex="-1" data-v="webhook">Webhook</button></div>',
    '<button type="button" role="radio" aria-checked="false" tabindex="-1" data-v="webhook">Webhook</button><button type="button" role="radio" aria-checked="false" tabindex="-1" data-v="bark" class="sup-new">Bark</button><button type="button" role="radio" aria-checked="false" tabindex="-1" data-v="gotify" class="sup-new">Gotify</button></div>')
rep('<p class="cs-help">余额预警会发送到这个地址。</p></div>',
    '<p class="cs-help">余额预警会发送到这个地址。</p></div>\n'
    '          <div class="cs-f" data-nm="bark" hidden><label for="supBark">Bark 推送地址</label><input class="in mono" id="supBark" type="url" placeholder="https://" autocomplete="off" spellcheck="false"><p class="cs-help">在 Bark 应用里复制推送地址。</p></div>\n'
    '          <div class="cs-f" data-nm="gotify" hidden><label for="supGot">Gotify 服务器地址</label><input class="in mono" id="supGot" type="url" placeholder="https://" autocomplete="off" spellcheck="false"></div>\n'
    '          <div class="cs-f" data-nm="gotify" hidden><label for="supGotT">Gotify 应用令牌</label><input class="in mono" id="supGotT" autocomplete="off" spellcheck="false"></div>\n'
    '          <div class="cs-f sup-new"><span class="cs-lb">通知哪些事</span><div class="sup-chk sup-col"><label><input type="checkbox" checked> 余额低于预警阈值</label><label><input type="checkbox" checked> 月度预算达到提醒比例</label><label><input type="checkbox" checked> 模型下线与调价</label><label><input type="checkbox" checked> 平台维护公告</label><label><input type="checkbox" checked> 新设备登录</label></div><p class="cs-help">' + tbc('需平台支持按事项推送') + '</p></div>')

# ---------- 6 安全：登录设备；日志：导出 CSV ----------
rep('        <h3 class="cs-h3">登录记录</h3>\n',
    '        <h3 class="cs-h3 sup-new">登录设备</h3>\n'
    '        <div class="tbl sup-new"><table class="cs-tbl"><thead><tr><th>设备</th><th>IP</th><th>最近活动</th><th><span class="sr">操作</span></th></tr></thead><tbody id="supSess"></tbody></table></div>\n'
    '        <p class="cs-fine sup-new">退出其他设备后，那些设备需要重新登录。<button class="ac-link" type="button" id="supSessOut">退出其他设备</button></p>\n'
    '        <h3 class="cs-h3">登录记录</h3>\n')
rep('<div class="cs-hd"><div><h2>使用日志</h2><p>上方按模型汇总，下方逐条列出每次请求。</p></div></div>',
    '<div class="cs-hd"><div><h2>使用日志</h2><p>上方按模型汇总，下方逐条列出每次请求。</p></div><button class="btn gray sm sup-new" type="button" id="supLogCsv">导出 CSV</button></div>')

# ---------- 7 预览身份 ----------
rep("function btPreview(){if(location.hash!=='#console-preview')return;if(!me){me={email:'',type:'personal',since:today(),keys:[],subs:[],edu:'none',preview:true};logged=true;syncLogin()}history.replaceState(null,'',location.pathname+location.search+'#console')}",
    "function btPreview(){var R={'#console-preview':['personal',''],'#console-preview-admin':['company','admin'],'#console-preview-member':['company','member'],'#console-preview-super':['super','super']}[location.hash];if(!R)return;"
    "if(!me||me.preview){me={email:'',type:R[0],role:R[1],since:today(),keys:[],subs:[],edu:'none',preview:true};logged=true;syncLogin()}history.replaceState(null,'',location.pathname+location.search+'#console')}  /* 三种预览身份：个人 / 企业管理员 / 企业成员 */")
rep("$('#btOrgSub').textContent=TYPE[me.type]||'';",
    "$('#btOrgSub').textContent=(me.type==='super'?'超级管理员':(TYPE[me.type]||''))+(me.type==='company'?(me.role==='member'?' · 成员':' · 管理员'):'');")
rep('<button class="sup-tog" id="supTog" type="button" aria-pressed="false">标出新增</button>',
    '<div class="sup-roles" id="supRoles" role="group" aria-label="预览身份"><span>预览身份</span><a href="#console-preview" data-r="personal">个人</a><a href="#console-preview-admin" data-r="admin">企业管理员</a><a href="#console-preview-member" data-r="member">企业成员</a><a href="#console-preview-super" data-r="super">超级管理员</a></div>\n'
    '<button class="sup-tog" id="supTog" type="button" aria-pressed="false">标出新增</button>')

# ---------- CSS ----------
CSS = '''
<style id="sup-console-css">
/* 控制台架构补齐预览（2026-10-14） */
.sup-roles{display:none;position:fixed;right:20px;bottom:122px;z-index:60;align-items:center;gap:4px;padding:4px;border-radius:999px;border:1px solid var(--glass-line,rgba(0,0,0,.1));background:var(--glass,rgba(255,255,255,.85));backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);box-shadow:0 2px 8px rgba(0,0,0,.08);font:500 12px var(--sans)}
html.in-console .sup-roles{display:flex}
.sup-roles span{padding:0 8px;color:var(--ink-50)}
.sup-roles a{padding:6px 10px;border-radius:999px;color:var(--ink-70);text-decoration:none}
.sup-roles a[aria-current="true"]{background:#000;color:#fff}
.sup-flt{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:0 0 16px}
.sup-seg{margin:0 0 14px}
.sup-own{margin:-8px 0 16px;font-size:13px;color:var(--ink-70)}
.sup-own b{font-weight:500;color:var(--ink)}
.sup-memf{flex-wrap:wrap}
.sup-memf .in{flex:1 1 200px}
.sup-steps{list-style:none;margin:0 0 18px;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;counter-reset:s}
.sup-steps li{padding:16px 18px;border:1px solid var(--line);border-radius:var(--r16,16px);background:var(--card);counter-increment:s}
.sup-steps li:before{content:"0" counter(s);display:block;font:500 11px var(--mono);color:var(--ink-50);margin-bottom:6px}
.sup-steps b{display:block;font-weight:500;margin-bottom:4px}
.sup-steps span{font-size:13px;color:var(--ink-70);line-height:1.6}
.sup-invf{display:grid;gap:12px;max-width:560px}
.sup-col{flex-direction:column;gap:8px}
.cs-p .tbl{position:relative}  /* 表头里的 .sr（绝对定位）留在可横滑的表格框里，不撑宽整页 */
.cs-tbl .sup-rm{appearance:none;border:0;background:none;padding:0;font:inherit;font-size:13px;color:var(--ink-70);text-decoration:underline;cursor:pointer}
@media (max-width:860px){
  .sup-steps{grid-template-columns:1fr}
  .sup-roles{right:14px;bottom:112px}
  .sup-roles span{display:none}
}
</style>
'''
k = s.rindex('</head>'); s = s[:k] + CSS + s[k:]

# ---------- JS ----------
JS = r'''
  /* ======== 控制台架构补齐预览（2026-10-14） ======== */
  (function(){
    function isAdm(){return me&&me.type==='company'&&me.role!=='member'}
    function isMem(){return me&&me.type==='company'&&me.role==='member'}
    function srOk(r){return r==='admin'?isAdm():r==='member'?isMem():r==='pay'?!isMem():true}
    function dl(name,head,rows){if(!rows.length){toast('没有可导出的记录。');return} var q=function(v){v=String(v==null?'':v);return /[",\n]/.test(v)?'"'+v.replace(/"/g,'""')+'"':v};
      var t='﻿'+[head].concat(rows).map(function(r){return r.map(q).join(',')}).join('\n'), a=document.createElement('a'); a.href=URL.createObjectURL(new Blob([t],{type:'text/csv;charset=utf-8'})); a.download=name; document.body.appendChild(a); a.click(); setTimeout(function(){URL.revokeObjectURL(a.href); a.remove()},0)}
    function y(n){return cny(+n||0)}
    function since(d){return d===1?new Date(new Date().toDateString()).getTime():Date.now()-d*864e5}
    /* 角色：按身份显示 / 隐藏；带 data-for 的元素在原有判断之上再收紧 */
    function supRoles(){ if(!me) return;
      $$('[data-sr]').forEach(function(el){var ok=srOk(el.getAttribute('data-sr')); el.hidden=el.hasAttribute('data-for')?(el.hidden||!ok):!ok});
      var cur=$('.cs-nav button.on'); if(cur&&cur.hidden) csTab('home');
      var r=me.type==='super'?'super':isAdm()?'admin':isMem()?'member':'personal'; $$('#supRoles a').forEach(function(a){a.setAttribute('aria-current',a.getAttribute('data-r')===r&&me.preview?'true':'false')});
      var own=$('#supOwn'); if(own) own.innerHTML=isAdm()?'<b>组织钱包</b> · 成员共用，由管理员充值':isMem()?'<b>组织钱包</b> · 由管理员充值，你按额度使用':'<b>个人钱包</b> · 自己充值、自己使用';
      supStatsOpts(); supStats(); supMembers(); supSplit(); supInv(); supSess() }
    var _rc=renderConsole; renderConsole=function(){_rc(); supRoles()};

    /* 用量分析 */
    var sd=7;
    function supStatsOpts(){var k=$('#supStK'), m=$('#supStM'); if(!k) return; var kv=k.value, mv=m.value;
      opts(k,'全部 Key',me.keys.map(function(x){return x.name}).filter(function(n,i,a){return a.indexOf(n)===i})); opts(m,'全部模型',M.map(function(x){return x.name})); k.value=kv; m.value=mv}
    function statRows(){var k=$('#supStK').value, m=$('#supStM').value, from=since(sd); return LOGS.filter(function(r){return r.t>=from&&(!k||r.key===k)&&(!m||r.model===m)})}
    function supStats(){if(!$('#supS1')) return; var rows=statRows(), n=rows.length, i=0, o=0, c=0, tt=[], tp=[], lim=0, err=0;
      rows.forEach(function(r){i+=+r.input||0; o+=+r.output||0; c+=+r.cost||0; if(r.ttft!=null) tt.push(+r.ttft); if(r.tps!=null) tp.push(+r.tps); if(r.status===429) lim++; if(r.status>=400) err++});
      var avg=function(a){return a.reduce(function(x,v){return x+v},0)/a.length};
      $('#supS1').textContent=n.toLocaleString('en-US'); $('#supS2').textContent=i.toLocaleString('en-US'); $('#supS3').textContent=o.toLocaleString('en-US'); $('#supS4').textContent=y(c);
      $('#supS5').textContent=tt.length?Math.round(avg(tt))+' ms':'--'; $('#supS6').textContent=tp.length?avg(tp).toFixed(1):'--'; $('#supS7').textContent=lim; $('#supS8').textContent=n&&rows.some(function(r){return r.status!=null})?(err/n*100).toFixed(1)+'%':'--'}
    $$('#supStSeg .chip').forEach(function(b){b.addEventListener('click',function(){sd=+b.getAttribute('data-sd'); $$('#supStSeg .chip').forEach(function(x){var on=x===b; x.classList.toggle('on',on); x.setAttribute('aria-pressed',String(on))}); supStats()})});
    ['#supStK','#supStM'].forEach(function(id){var e=$(id); if(e) e.addEventListener('change',supStats)});
    var LH=['时间','API Key','模型','输入词元','输出词元','费用（¥）','算力节点','绿电折扣'];
    function lrow(r){return [stamp(r.t),r.key,r.model,r.input,r.output,(+r.cost||0).toFixed(4),r.node||'',r.green||'']}
    $('#supStCsv').addEventListener('click',function(){dl('沐仞_用量_'+today()+'.csv',LH,statRows().map(lrow))});
    $('#supLogCsv').addEventListener('click',function(){var days=+$('#csLt').value,m=$('#csLm').value,k=$('#csLk').value,from=since(days); dl('沐仞_使用日志_'+today()+'.csv',LH,LOGS.filter(function(r){return r.t>=from&&(!m||r.model===m)&&(!k||r.key===k)}).map(lrow))});

    /* 绿电批量任务、实名认证 */
    $('#supBatchGo').addEventListener('click',function(){toast('批量任务接口开发完成后即可申请。')});
    $$('[data-kyc]').forEach(function(b){b.addEventListener('click',function(){toast('实名认证服务接入后即可使用。')})});

    /* 成员：管理员添加普通成员，可设每月额度上限 */
    function supMembers(){var tb=$('#supMem'); if(!tb||!me) return; var rows='<tr><td>'+(me.email?esc(me.email):'你')+'</td><td>管理员</td><td>已启用</td><td class="mono r">¥0.00</td><td class="mono r">不限</td><td class="mono">'+esc(me.since||'')+'</td><td></td></tr>';
      (me.subs||[]).forEach(function(m,ix){rows+='<tr><td>'+esc(m.email)+'</td><td>'+(m.role==='admin'?'管理员':'成员')+'</td><td>已添加</td><td class="mono r">¥0.00</td><td class="mono r">'+(m.cap?y(m.cap):'不限')+'</td><td class="mono">'+esc(m.at||'')+'</td><td><button class="sup-rm" type="button" data-rm="'+ix+'">移除</button></td></tr>'});
      tb.innerHTML=rows; $$('#supMem [data-rm]').forEach(function(b){b.addEventListener('click',function(){me.subs.splice(+b.getAttribute('data-rm'),1); persist(); renderConsole(); if(typeof btRender==='function') btRender(); toast('已移除。')})})}
    $('#supMemF').addEventListener('submit',function(e){e.preventDefault(); var f=this, m=f.email.value.trim().toLowerCase(), cap=f.cap.value.trim();
      if(!MAIL.test(m)){toast('请输入有效的邮箱地址。'); f.email.focus(); return}
      if(cap&&!/^\d+(\.\d{1,2})?$/.test(cap)){toast('额度上限请填写金额，最多两位小数。'); f.cap.focus(); return}
      me.subs=me.subs||[]; if(m===String(me.email||'').toLowerCase()||me.subs.some(function(s){return s.email===m})){toast('这个邮箱已在成员列表中。'); return}
      me.subs.push({email:m,at:today(),role:'member',cap:cap?+cap:0}); persist(); f.reset(); renderConsole(); if(typeof btRender==='function') btRender(); toast('已添加。登录方式邮件接入后即可发送。')});

    /* 账单分摊 */
    var sp='m';
    function supSplit(){var h=$('#supSpH'); if(!h) return; var from=new Date(new Date().getFullYear(),new Date().getMonth(),1).getTime(), g={};
      LOGS.filter(function(r){return r.t>=from}).forEach(function(r){var key=sp==='m'?(r.user||'未记录成员'):r.key; var x=g[key]||(g[key]={n:0,c:0}); x.n++; x.c+=+r.cost||0});
      h.innerHTML='<tr><th>'+(sp==='m'?'成员':'API Key')+'</th><th class="r">请求次数</th><th class="r">本月消费</th></tr>';
      var ks=Object.keys(g); $('#supSpB').innerHTML=ks.map(function(k2){return '<tr><td>'+esc(k2)+'</td><td class="mono r">'+g[k2].n.toLocaleString('en-US')+'</td><td class="mono r">'+y(g[k2].c)+'</td></tr>'}).join(''); $('#supSp0').hidden=ks.length>0; supSplit.rows=ks.map(function(k2){return [k2,g[k2].n,g[k2].c.toFixed(4)]})}
    $$('#supSpSeg .chip').forEach(function(b){b.addEventListener('click',function(){sp=b.getAttribute('data-sp'); $$('#supSpSeg .chip').forEach(function(x){var on=x===b; x.classList.toggle('on',on); x.setAttribute('aria-pressed',String(on))}); supSplit()})});
    $('#supSpCsv').addEventListener('click',function(){dl('沐仞_账单分摊_'+today()+'.csv',[sp==='m'?'成员':'API Key','请求次数','本月消费（¥）'],supSplit.rows||[])});

    /* 发票：可开票金额 = 已消费金额（LOGS 合计）；抬头只存在当前页面 */
    var invT='normal';
    function supInv(){var a=$('#supInvA'); if(!a) return; a.textContent=y(LOGS.reduce(function(x,r){return x+(+r.cost||0)},0)); var f=$('#supInvF'), v=me.inv||{}; if(f._for!==me){f._for=me; f.title.value=v.title||''; f.tax.value=v.tax||''; f.addr.value=v.addr||''; f.bank.value=v.bank||''; f.mail.value=v.mail||''; setInvT(v.type||'normal')}}
    function setInvT(t){invT=t; $$('#supInvF .cs-pm button').forEach(function(b){var on=b.getAttribute('data-v')===t; b.setAttribute('aria-checked',String(on)); b.tabIndex=on?0:-1}); $$('#supInvF [data-inv]').forEach(function(el){el.hidden=el.getAttribute('data-inv')!==t})}
    $$('#supInvF .cs-pm button').forEach(function(b){b.addEventListener('click',function(){setInvT(b.getAttribute('data-v'))})});
    $('#supInvF').addEventListener('submit',function(e){e.preventDefault(); var f=this, msg=$('#supInvMsg'); msg.textContent='';
      if(!f.title.value.trim()){msg.textContent='请填写抬头名称。'; f.title.focus(); return}
      if(invT==='special'&&!f.tax.value.trim()){msg.textContent='数电专票需要纳税人识别号。'; f.tax.focus(); return}
      if(f.mail.value.trim()&&!MAIL.test(f.mail.value.trim())){msg.textContent='请输入有效的邮箱地址。'; f.mail.focus(); return}
      me.inv={type:invT,title:f.title.value.trim(),tax:f.tax.value.trim(),addr:f.addr.value.trim(),bank:f.bank.value.trim(),mail:f.mail.value.trim()}; persist(); toast('抬头已保存。开票接口接入后即可提交。')});
    $('#supInvGo').addEventListener('click',function(){var can=LOGS.reduce(function(x,r){return x+(+r.cost||0)},0), v=parseFloat($('#supInvAmt').value);
      if(!(can>0)){toast('可开票金额为 ¥0.00，暂时不能申请。'); return} if(!(v>0)||v>can){toast('开票金额不能超过可开票金额。'); return} toast('开票接口接入后即可提交。')});

    /* 登录设备：只列当前这台（浏览器 · 系统）；其他设备由平台会话接口返回 */
    function supSess(){var tb=$('#supSess'); if(!tb) return; var u=navigator.userAgent, br=/Edg\//.test(u)?'Edge':/Chrome\//.test(u)?'Chrome':/Firefox\//.test(u)?'Firefox':/Safari\//.test(u)?'Safari':'浏览器', os=/Mac OS X/.test(u)?'macOS':/Windows/.test(u)?'Windows':/Android/.test(u)?'Android':/iPhone|iPad/.test(u)?'iOS':/Linux/.test(u)?'Linux':'';
      tb.innerHTML='<tr><td>'+br+(os?' · '+os:'')+'</td><td class="mono">--</td><td>当前</td><td>本机</td></tr>'}
    $('#supSessOut').addEventListener('click',function(){toast('会话管理接口接入后即可使用。')});
  })();
'''
rep("  $$('[data-product-target]').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();jumpTo(a.getAttribute('data-product-target'))})});\n  window.addEventListener('hashchange',route); route();",
    JS + "  $$('[data-product-target]').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();jumpTo(a.getAttribute('data-product-target'))})});\n  window.addEventListener('hashchange',route); route();")

# ---------- 英文（只补缺，不覆盖站上已有译文） ----------
EN = {
    '开发': 'Build', '组织': 'Organization', '用量分析': 'Analytics', '绿电批量任务': 'Green batch jobs', '成员': 'Members', '账单分摊': 'Cost allocation', '实名认证': 'Identity verification', '发票': 'Invoices',
    '预览身份': 'Preview as', '个人': 'Personal', '企业管理员': 'Business admin', '企业成员': 'Business member', '超级管理员': 'Super admin', '管理员': 'Admin',
    '按时间、API Key 和模型查看请求量、词元、费用与性能。': 'Requests, tokens, cost and performance by time, API key and model.', '导出 CSV': 'Export CSV', '今天': 'Today', '近 7 天': 'Last 7 days', '近 30 天': 'Last 30 days',
    '全部 Key': 'All keys', '全部模型': 'All models', '请求次数': 'Requests', '输入词元': 'Input tokens', '输出词元': 'Output tokens', '费用': 'Cost', '性能': 'Performance',
    '平均首字时延': 'Avg. time to first token', '平均输出速度': 'Avg. output speed', '词元 / 秒': 'tokens / s', '被限流（429）': 'Rate limited (429)', '错误率': 'Error rate',
    '需平台在每条记录里写入首字时延、输出速度与状态码': 'Needs the platform to record time to first token, output speed and status code per request', '限流': 'Rate limits',
    '账户的每分钟请求数（RPM）与每分钟词元数（TPM）上限显示在这里，超出时返回 429。当前上限：RPM -- · TPM --': 'Your account’s requests-per-minute (RPM) and tokens-per-minute (TPM) limits appear here; going over returns 429. Current limits: RPM -- · TPM --',
    '待公司确认：默认上限、是否按消费分级、怎么提额': 'Company to confirm: default limits, spend-based tiers, how to raise them',
    '不急着要结果的请求，打包成一批交给调度，排到电站富余绿电的时段执行。': 'Requests that are not urgent go in a batch; the scheduler runs them in hours when plants have surplus green power.', '申请开通': 'Request access',
    '上传': 'Upload', '把请求写成 JSONL 文件，每行一个请求。': 'Write requests to a JSONL file, one request per line.', '排队': 'Queue', '调度把任务排到电站富余绿电的时段执行。': 'The scheduler runs the job in hours with surplus green power.',
    '下载': 'Download', '完成后下载结果文件，用量与费用计入账单和订单产地卡。': 'Download the results when done; usage and cost go to your bill and order origin cards.', '还没有批量任务': 'No batch jobs yet', '开通后，任务进度与结果文件显示在这里。': 'Once enabled, job progress and result files appear here.',
    '需平台开发批量接口；完成时限与价格待公司确认': 'Needs a platform batch API; turnaround and price for the company to confirm',
    '管理员添加的成员共用组织钱包，各自创建和使用自己的 API Key。': 'Members added by an admin share the organization wallet and create and use their own API keys.', '成员邮箱': 'Member email', '每月额度上限（¥，可不填）': 'Monthly limit (¥, optional)', '每月额度上限': 'Monthly limit', '添加成员': 'Add member',
    '添加后，平台把登录方式发到成员邮箱。': 'Once added, the platform emails the member how to sign in.', '待公司确认：能否有多个管理员、成员额度上限是否支持': 'Company to confirm: multiple admins, per-member limits',
    '角色': 'Role', '本月消费': 'This month', '加入时间': 'Joined', '操作': 'Actions', '已启用': 'Active', '已添加': 'Added', '不限': 'No limit', '移除': 'Remove', '你': 'You',
    '组织钱包的消费按成员和 API Key 拆开，方便内部结算。': 'Organization wallet spend split by member and API key for internal accounting.', '按成员': 'By member', '按 API Key': 'By API key',
    '本月还没有消费': 'No spend this month', '成员发出请求后，这里按成员或 API Key 汇总费用。': 'Once members send requests, costs are summed here by member or API key.', '按成员分摊需要平台在使用记录里写入成员': 'Splitting by member needs the platform to record the member on each request', '未记录成员': 'Member not recorded',
    '维护发票抬头，按可开票金额申请电子发票。': 'Keep your invoice details and request e-invoices up to the invoiceable amount.', '可开票金额': 'Invoiceable', '按已消费金额计算': 'Based on amount spent', '开票中': 'In progress', '已开票': 'Invoiced',
    '待公司确认：按消费还是按充值开票、开票时限、海外客户的 Invoice': 'Company to confirm: invoice on spend or on top-up, turnaround, invoices for overseas customers', '发票抬头': 'Invoice details', '发票类型': 'Invoice type', '数电普票': 'Standard e-invoice', '数电专票': 'Special VAT e-invoice',
    '抬头名称': 'Name on invoice', '公司全称或个人姓名': 'Full company name or personal name', '纳税人识别号': 'Taxpayer ID', '企业抬头必填': 'Required for companies', '注册地址与电话': 'Registered address and phone', '开户行与账号': 'Bank and account number', '接收邮箱': 'Delivery email', '保存抬头': 'Save details',
    '申请开票': 'Request invoice', '开票金额（¥）': 'Amount (¥)', '开票金额': 'Amount', '开票记录': 'Invoice history', '申请时间': 'Requested', '类型': 'Type', '抬头': 'Name', '金额': 'Amount', '还没有开票记录': 'No invoices yet', '申请后，开票进度和发票下载显示在这里。': 'After you request one, progress and downloads appear here.',
    '核验个人或企业身份。认证结果用于开票主体与合同签署。': 'Verify an individual or company. The result sets the invoicing entity and who signs contracts.', '未认证': 'Not verified', '个人认证': 'Individual', '姓名、身份证号与人脸核验，适合个人开发者。': 'Name, ID number and face check, for individual developers.', '开始认证': 'Start',
    '企业认证': 'Company', '上传营业执照，再由法定代表人人脸核验，或用对公账户小额打款验证。认证后，发票抬头与合同主体为企业。': 'Upload the business licence, then verify with the legal representative’s face check or a small transfer from the company account. After that, invoices and contracts are in the company’s name.',
    '海外用户': 'Overseas users', '海外个人与企业的身份核验方式另行提供。': 'Verification for overseas individuals and companies will be provided separately.', '待公司确认：是否必须实名、未实名能用哪些功能、认证服务商': 'Company to confirm: whether verification is required, what works without it, and the verification provider',
    '你的可用额度：不限': 'Your available credit: no limit', '管理员没有给你设额度上限，用量从组织钱包扣除。需要充值或提额，请联系组织管理员。': 'Your admin has not set a limit; usage is deducted from the organization wallet. Contact your admin to top up or raise it.',
    '组织钱包': 'Organization wallet', '个人钱包': 'Personal wallet', '· 成员共用，由管理员充值': '· shared by members, topped up by the admin', '· 由管理员充值，你按额度使用': '· topped up by the admin; you use it within your limit', '· 自己充值、自己使用': '· you top up and use it',
    '对公转账': 'Bank transfer', '收款户名：北京沐仞科技有限公司。开户行与账号': 'Payee: 北京沐仞科技有限公司 (Beijing FathomPeak Technology). Bank and account number', '待公司提供': 'Company to provide', '。转账后把凭证发到 fathompeak@163.com，财务确认后入账。': '. After transferring, email the receipt to fathompeak@163.com; finance credits it after checking.',
    '成员管理已移到侧栏「组织 › 成员」。': 'Member management has moved to Organization › Members in the sidebar.',
    'Bark 推送地址': 'Bark push URL', '在 Bark 应用里复制推送地址。': 'Copy the push URL from the Bark app.', 'Gotify 服务器地址': 'Gotify server URL', 'Gotify 应用令牌': 'Gotify app token', '通知哪些事': 'Notify me about',
    '余额低于预警阈值': 'Balance below the alert threshold', '月度预算达到提醒比例': 'Monthly budget reaching an alert level', '模型下线与调价': 'Model retirements and price changes', '平台维护公告': 'Platform maintenance', '新设备登录': 'Sign-in from a new device', '需平台支持按事项推送': 'Needs platform support for per-event notifications',
    '登录设备': 'Signed-in devices', '设备': 'Device', '最近活动': 'Last active', '当前': 'Now', '本机': 'This device', '退出其他设备后，那些设备需要重新登录。': 'Devices you sign out must sign in again.', '退出其他设备': 'Sign out other devices',
    '没有可导出的记录。': 'Nothing to export.', '已移除。': 'Removed.', '已添加。登录方式邮件接入后即可发送。': 'Added. The sign-in email will be sent once email is connected.', '额度上限请填写金额，最多两位小数。': 'Enter the limit as an amount with up to two decimals.',
    '批量任务接口开发完成后即可申请。': 'You can request access once the batch API is built.', '实名认证服务接入后即可使用。': 'Available once the verification service is connected.', '请填写抬头名称。': 'Enter the name for the invoice.', '数电专票需要纳税人识别号。': 'A special VAT invoice needs a taxpayer ID.',
    '抬头已保存。开票接口接入后即可提交。': 'Details saved. Requests can be submitted once invoicing is connected.', '可开票金额为 ¥0.00，暂时不能申请。': 'The invoiceable amount is ¥0.00, so you cannot request one yet.', '开票金额不能超过可开票金额。': 'The amount cannot exceed the invoiceable amount.', '开票接口接入后即可提交。': 'Requests can be submitted once invoicing is connected.',
    '会话管理接口接入后即可使用。': 'Available once session management is connected.',
}
rep('  syncAuthLocale(); applyLang();', '  (function(S){for(var k in S) if(!(k in I18N)) I18N[k]=S[k]})(' + json.dumps(EN, ensure_ascii=False) + ');  /* 控制台架构补齐的英文：只补缺 */\n  syncAuthLocale(); applyLang();')

open(OUT, 'w', encoding='utf8').write(s)
print('done:', OUT)
