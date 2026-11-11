"""上线合并（Zixin 2026-10-14 夜："修复问题 然后推上线"；选「保留线上那版，补上我这边独有的」）。
线上 b360fd4 / 3ddb3aa 已有另一个会话做的四种身份（me.role = personal / member / admin / root，data-roles 显隐，
#console-preview(-member|-admin|-root)）、成员页、钱包里的对公 / 发票 / 分摊、超管的用户与组织 / 模型与价格 / 内容。这些一律不动。
本脚本在线上那版上补我这边独有的（侧栏不重排，只插按钮）：
 0 花体恢复：控制台里以拉丁字母开头的衬线标题，中英文模式都加 HandLatin 首字母（设计交接口径）。
 1 客户侧新页：用量分析（使用日志后）、绿电批量任务（订单与产地卡后）、实名认证（钱包与账单后，成员不显示）。
 2 通用设置：通知方式加 Bark、Gotify，新增「通知哪些事」；安全与访问：登录设备；使用日志：导出 CSV。
 3 超管（root）「管理员」组里加：财务（资金流水、开票处理、退款、对账与报表）、绿电（电站与节点、分时价、绿电时段、批量任务）、
   运营（告警、管理员与权限、全站日志、审计日志）。页面取自 build_console_superadmin --live 的输出（不含报价单机密价与钟点）。
 4 正式版处理：去掉「标出新增」按钮；控制台与登录页里的黄色「待公司确认」、超管页「new-api 现成 / 需开发」标签不显示；
   预算提示用「…接入后即可…」口径。
前置（同一条链）：线上 → build_full_supplement --console-only → build_console_playground --live → build_console_login --live → 本脚本。
用法：python3 -I build_console_merge_live_2026-10-14.py <输入 html> <console_backend 输出 html> <superadmin --live 输出 html> <输出 html>
"""
import re, sys

SRC, CON, SAL, OUT = sys.argv[1:5]
s = open(SRC, encoding='utf8').read()
con = open(CON, encoding='utf8').read()
sal = open(SAL, encoding='utf8').read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: sys.exit(f'[停止] 匹配 {c} 次（应为 {n}）：{old[:80]}')
    s = s.replace(old, new)


def pane_of(doc, p):
    a = doc.index(f'      <div class="cs-p" data-p="{p}">')
    b = doc.index('      <div class="cs-p" data-p="', a + 20)
    return doc[a:b]


def btn_of(doc, p):
    m = re.search(r'<button type="button" data-p="' + re.escape(p) + r'"[^>]*>.*?</button>', doc, re.S)
    if not m: sys.exit(f'[停止] 找不到按钮 {p}')
    return m.group(0)


def style_of(doc, sid):
    a = doc.index(f'<style id="{sid}">'); b = doc.index('</style>', a) + len('</style>')
    return doc[a:b]


def i18n_line(doc, mark):
    m = re.search(r'  \(function\(S\)\{for\(var k in S\) if\(!\(k in I18N\)\) I18N\[k\]=S\[k\]\}\)\(.*?\);  /\* ' + re.escape(mark) + r' \*/\n', doc)
    if not m: sys.exit(f'[停止] 找不到英文词条行 {mark}')
    return m.group(0)


# ---------- 0 花体恢复 ----------
rep("/* 手写首字母只用于控制台以外的页面、英文模式下以拉丁字母开头的衬线大标题；控制台（.bt）里不加（Zixin 2026-10-14：去掉\"API Key\"花体） */",
    "/* 手写首字母：控制台以外的页面只在英文模式加；控制台（.bt）里中英文模式都加，只修饰以拉丁字母开头的衬线标题（设计交接；2026-10-14 晚恢复） */")
rep("var inC=!!el.closest('.bt'), on=!inC&&lang==='en'&&/^[A-Za-z]/.test(el.textContent.trim());",
    "var inC=!!el.closest('.bt'), on=(lang==='en'||inC)&&/^[A-Za-z]/.test(el.textContent.trim());")

# ---------- 1 客户侧：侧栏按钮 + 新页 ----------
b_stats = btn_of(con, 'stats'); b_batch = btn_of(con, 'batch')
b_kyc = btn_of(con, 'kyc').replace(' data-sr="pay"', ' data-roles="personal admin root"')
U = re.search(r'<button type="button" data-p="usage">.*?</button>', s, re.S).group(0)
O = re.search(r'<button type="button" data-p="orders">.*?</button>', s, re.S).group(0)
B = re.search(r'<button type="button" data-p="bill" data-roles="personal admin root">.*?</button>', s, re.S).group(0)
rep(U, U + '\n        ' + b_stats)
rep(O, O + '\n        ' + b_batch)
rep(B, B + '\n        ' + b_kyc)
NEWP = pane_of(con, 'stats') + pane_of(con, 'batch') + pane_of(con, 'kyc')

# ---------- 3 超管：管理员组里补三组页面 ----------
GROUPS = [('财务', ['ad-ledger', 'ad-inv', 'ad-refund', 'ad-report']), ('绿电', ['ad-plants', 'ad-tod', 'ad-hours', 'ad-batch']), ('运营', ['ad-alerts', 'ad-admins', 'ad-logs', 'ad-audit'])]
nav_add = ''
for g, ps in GROUPS:
    nav_add += f'\n        <span class="cs-grp bt-grp bt-sub" data-roles="root">{g}</span>'
    for p in ps:
        nav_add += '\n        ' + btn_of(sal, p).replace(' data-sr="super" hidden', ' data-roles="root"')
        NEWP += pane_of(sal, p)
C = re.search(r'<button type="button" data-p="root-content" data-roles="root">.*?</button>', s, re.S).group(0)
rep(C, C + nav_add)
rep('      <div class="cs-p" data-p="acct">', NEWP + '      <div class="cs-p" data-p="acct">')

# ---------- 2 通知、登录设备、日志导出 ----------
rep('<button type="button" role="radio" aria-checked="false" tabindex="-1" data-v="webhook">Webhook</button></div>',
    '<button type="button" role="radio" aria-checked="false" tabindex="-1" data-v="webhook">Webhook</button><button type="button" role="radio" aria-checked="false" tabindex="-1" data-v="bark">Bark</button><button type="button" role="radio" aria-checked="false" tabindex="-1" data-v="gotify">Gotify</button></div>')
rep('<p class="cs-help">余额预警会发送到这个地址。</p></div>',
    '<p class="cs-help">余额预警会发送到这个地址。</p></div>\n'
    '          <div class="cs-f" data-nm="bark" hidden><label for="supBark">Bark 推送地址</label><input class="in mono" id="supBark" type="url" placeholder="https://" autocomplete="off" spellcheck="false"><p class="cs-help">在 Bark 应用里复制推送地址。</p></div>\n'
    '          <div class="cs-f" data-nm="gotify" hidden><label for="supGot">Gotify 服务器地址</label><input class="in mono" id="supGot" type="url" placeholder="https://" autocomplete="off" spellcheck="false"></div>\n'
    '          <div class="cs-f" data-nm="gotify" hidden><label for="supGotT">Gotify 应用令牌</label><input class="in mono" id="supGotT" autocomplete="off" spellcheck="false"></div>\n'
    '          <div class="cs-f"><span class="cs-lb">通知哪些事</span><div class="sup-chk sup-col"><label><input type="checkbox" checked> 余额低于预警阈值</label><label><input type="checkbox" checked> 月度预算达到提醒比例</label><label><input type="checkbox" checked> 模型下线与调价</label><label><input type="checkbox" checked> 平台维护公告</label><label><input type="checkbox" checked> 新设备登录</label></div></div>')
rep('        <h3 class="cs-h3">登录记录</h3>\n',
    '        <h3 class="cs-h3">登录设备</h3>\n'
    '        <div class="tbl"><table class="cs-tbl"><thead><tr><th>设备</th><th>IP</th><th>最近活动</th><th><span class="sr">操作</span></th></tr></thead><tbody id="supSess"></tbody></table></div>\n'
    '        <p class="cs-fine">退出其他设备后，那些设备需要重新登录。<button class="ac-link" type="button" id="supSessOut">退出其他设备</button></p>\n'
    '        <h3 class="cs-h3">登录记录</h3>\n')
rep('<div class="cs-hd"><div><h2>使用日志</h2><p>上方按模型汇总，下方逐条列出每次请求。</p></div></div>',
    '<div class="cs-hd"><div><h2>使用日志</h2><p>上方按模型汇总，下方逐条列出每次请求。</p></div><button class="btn gray sm" type="button" id="supLogCsv">导出 CSV</button></div>')

# ---------- 4 正式版处理 ----------
rep('<button class="sup-tog" id="supTog" type="button" aria-pressed="false">标出新增</button>\n', '')
rep("toast('预览：预算设置没有保存到平台，需要平台支持后才能生效。')", "toast('预算提醒接入后即可生效。')")

# ---------- CSS ----------
CSS = (style_of(con, 'sup-console-css') + '\n' + style_of(sal, 'sup-super-css') + '\n'
       '<style id="merge-live-css">\n/* 上线合并（2026-10-14 夜） */\n.bt .tbc,.ac .tbc,.ad-hr .bt-tag{display:none!important}\n'
       '.bt-nav .bt-sub{margin-top:8px;padding-left:22px;opacity:.8}\n.cs-p .tbl{position:relative}\n</style>\n')
k = s.rindex('</head>'); s = s[:k] + CSS + s[k:]

# ---------- JS ----------
JS = r'''
  /* ======== 上线合并（2026-10-14 夜）：用量分析、导出、批量任务、实名、登录设备、超管补充页 ======== */
  (function(){
    function dl(name,head,rows){if(!rows.length){toast('没有可导出的记录。');return} var q=function(v){v=String(v==null?'':v);return /[",\n]/.test(v)?'"'+v.replace(/"/g,'""')+'"':v};
      var t='﻿'+[head].concat(rows).map(function(r){return r.map(q).join(',')}).join('\n'), a=document.createElement('a'); a.href=URL.createObjectURL(new Blob([t],{type:'text/csv;charset=utf-8'})); a.download=name; document.body.appendChild(a); a.click(); setTimeout(function(){URL.revokeObjectURL(a.href); a.remove()},0)}
    function since(d){return d===1?new Date(new Date().toDateString()).getTime():Date.now()-d*864e5}
    var sd=7, LH=['时间','API Key','模型','输入词元','输出词元','费用（¥）','算力节点','绿电折扣'];
    function lrow(r){return [stamp(r.t),r.key,r.model,r.input,r.output,(+r.cost||0).toFixed(4),r.node||'',r.green||'']}
    function statRows(){var k=$('#supStK').value, m=$('#supStM').value, from=since(sd); return LOGS.filter(function(r){return r.t>=from&&(!k||r.key===k)&&(!m||r.model===m)})}
    function supStats(){if(!$('#supS1')||!me) return; var k=$('#supStK'), m=$('#supStM'), kv=k.value, mv=m.value;
      opts(k,'全部 Key',me.keys.map(function(x){return x.name}).filter(function(n,i,a){return a.indexOf(n)===i})); opts(m,'全部模型',M.map(function(x){return x.name})); k.value=kv; m.value=mv;
      var rows=statRows(), n=rows.length, i=0, o=0, c=0, tt=[], tp=[], lim=0, err=0;
      rows.forEach(function(r){i+=+r.input||0; o+=+r.output||0; c+=+r.cost||0; if(r.ttft!=null) tt.push(+r.ttft); if(r.tps!=null) tp.push(+r.tps); if(r.status===429) lim++; if(r.status>=400) err++});
      var avg=function(a){return a.reduce(function(x,v){return x+v},0)/a.length};
      $('#supS1').textContent=n.toLocaleString('en-US'); $('#supS2').textContent=i.toLocaleString('en-US'); $('#supS3').textContent=o.toLocaleString('en-US'); $('#supS4').textContent=cny(c);
      $('#supS5').textContent=tt.length?Math.round(avg(tt))+' ms':'--'; $('#supS6').textContent=tp.length?avg(tp).toFixed(1):'--'; $('#supS7').textContent=lim; $('#supS8').textContent=n&&rows.some(function(r){return r.status!=null})?(err/n*100).toFixed(1)+'%':'--'}
    $$('#supStSeg .chip').forEach(function(b){b.addEventListener('click',function(){sd=+b.getAttribute('data-sd'); $$('#supStSeg .chip').forEach(function(x){var on=x===b; x.classList.toggle('on',on); x.setAttribute('aria-pressed',String(on))}); supStats()})});
    ['#supStK','#supStM'].forEach(function(id){var e=$(id); if(e) e.addEventListener('change',supStats)});
    $('#supStCsv').addEventListener('click',function(){dl('沐仞_用量_'+today()+'.csv',LH,statRows().map(lrow))});
    $('#supLogCsv').addEventListener('click',function(){var days=+$('#csLt').value,m=$('#csLm').value,k=$('#csLk').value,from=since(days); dl('沐仞_使用日志_'+today()+'.csv',LH,LOGS.filter(function(r){return r.t>=from&&(!m||r.model===m)&&(!k||r.key===k)}).map(lrow))});
    $('#supBatchGo').addEventListener('click',function(){toast('批量任务接口开发完成后即可申请。')});
    $$('[data-kyc]').forEach(function(b){b.addEventListener('click',function(){toast('实名认证服务接入后即可使用。')})});
    function supSess(){var tb=$('#supSess'); if(!tb) return; var u=navigator.userAgent, br=/Edg\//.test(u)?'Edge':/Chrome\//.test(u)?'Chrome':/Firefox\//.test(u)?'Firefox':/Safari\//.test(u)?'Safari':'浏览器', os=/Mac OS X/.test(u)?'macOS':/Windows/.test(u)?'Windows':/Android/.test(u)?'Android':/iPhone|iPad/.test(u)?'iOS':/Linux/.test(u)?'Linux':'';
      tb.innerHTML='<tr><td>'+br+(os?' · '+os:'')+'</td><td class="mono">--</td><td>当前</td><td>本机</td></tr>'}
    $('#supSessOut').addEventListener('click',function(){toast('会话管理接口接入后即可使用。')});
    /* 超管补充页：动作在平台接入后才可用；筛选胶囊只切换选中态 */
    $$('[data-ad-act]').forEach(function(b){b.addEventListener('click',function(){toast('接入平台后即可使用。')})});
    $$('[data-ad-form]').forEach(function(f){f.addEventListener('submit',function(e){e.preventDefault(); toast('接入平台后即可使用。')})});
    $$('[data-ad-menu]').forEach(function(c){c.addEventListener('change',function(){toast('接入平台后即可使用。')})});
    $$('[data-ad-go]').forEach(function(b){b.addEventListener('click',function(){csTab(b.getAttribute('data-ad-go'))})});
    $$('.ad-chips').forEach(function(g){var bs=$$('.bt-chip',g); bs.forEach(function(b){b.addEventListener('click',function(){bs.forEach(function(x){var on=x===b; x.classList.toggle('on',on); x.setAttribute('aria-pressed',String(on))})})})});
    /* 切换身份后，当前页对新身份不可见（如成员没有钱包）就回到概览 */
    var _rc=renderConsole; renderConsole=function(){_rc(); supStats(); supSess(); var cur=$('.cs-nav button.on'); if(cur&&cur.hidden) csTab('home')};
  })();
'''
rep("  $$('[data-product-target]').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();jumpTo(a.getAttribute('data-product-target'))})});\n  window.addEventListener('hashchange',route); route();",
    JS + "  $$('[data-product-target]').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();jumpTo(a.getAttribute('data-product-target'))})});\n  window.addEventListener('hashchange',route); route();")

# ---------- 英文：沿用两份脚本的词条（只补缺） ----------
import json


def only_used(line):
    """词条行只留本页用到的键（超管版词条里有分时价钟点、报价单等文字，上线版页面不用，也不进源码）"""
    m = re.match(r'(  \(function\(S\)\{for\(var k in S\) if\(!\(k in I18N\)\) I18N\[k\]=S\[k\]\}\))\((.*)\);(  /\* .*? \*/\n)$', line, re.S)
    d = json.loads(m.group(2))
    return m.group(1) + '(' + json.dumps({k2: v for k2, v in d.items() if k2 in s}, ensure_ascii=False) + ');' + m.group(3)


EN_LINES = only_used(i18n_line(con, '控制台架构补齐的英文：只补缺')) + only_used(i18n_line(sal, '超管版英文：只补缺')) + \
    "  (function(S){for(var k in S) if(!(k in I18N)) I18N[k]=S[k]})({'预算提醒接入后即可生效。':'Budget alerts take effect once connected.','运营':'Operations'});\n"
rep('  syncAuthLocale(); applyLang();', EN_LINES + '  syncAuthLocale(); applyLang();')
open(OUT, 'w', encoding='utf8').write(s)
print('done:', OUT)
