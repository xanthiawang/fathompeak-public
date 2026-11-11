"""登录分个人 / 企业两个入口，控制台按身份分开、不切换（Zixin 2026-10-15）。叠在线上 f350805 上。
Zixin："算了还是分开成个人和企业登录吧。然后重新设计后台的 ui 和使用逻辑；然后后台不设置个人和企业的切换。不去掉邀请链接。"
     "你设计的时候要在现在发布的版本的视觉、背景图和设计的基础上修改。"
 1 登录：恢复 d88055b 的「个人登录 / 企业登录」两个标签、企业登录（工作邮箱 + 验证码 / 密码）、互相提示；
   做法：把 `git diff -U0 f350805 d88055b` 里登录相关的段落按行号套回去（成员页两段和英文词条那段不套）。
 2 成员页：保留「复制邀请链接」，文案改成两个入口的说法（按邮箱添加 / 邀请链接，都用「企业登录」进入）。
 3 控制台按身份分开，沿用线上视觉（蓝色光影背景、表头色带、卡片、花体都不动），只改结构和文案：
   · 左上角不再是切换器：显示账户名和身份（个人 / 企业 · 管理员 / 企业 · 成员）；账户菜单里只有自己这一个身份，
     写明「企业成员请退出后用企业登录进入」或反过来。
   · 侧栏分组：API Key 挪到上面和模型、体验中心一组；新增「用量」组（使用日志、用量分析）；
     最后一组个人和成员叫「账户」，企业管理员叫「企业管理」（成员、钱包与账单、企业认证、安全与访问、通用设置）。
   · 概览：标题下加一行身份说明；「开始使用」按身份：个人 = 创建 Key / 充值 / 发请求，管理员 = 创建 Key / 充值 / 添加成员，
     成员 = 创建 Key / 发请求（成员不能充值）。右栏「几位成员」只给管理员看。底部额度：成员叫「我的额度」。
   · 实名认证：个人只看个人认证，企业管理员只看企业认证（菜单名也叫企业认证）；成员没有这一页。
   · 资料页、使用日志、用量分析的说明按身份写（成员只看自己的请求，管理员看全企业）。
用法：python3 -I build_console_identity_split_2026-10-15.py <线上 index.html（f350805）> <输出 html> <login_two_entrances_from_d88055b_2026-10-15.diff>
"""
import json, re, sys

SRC, OUT, DIFF = sys.argv[1], sys.argv[2], sys.argv[3]
s = open(SRC, encoding='utf8').read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: sys.exit(f'[停止] 匹配 {c} 次（应为 {n}）：{old[:80]}')
    s = s.replace(old, new)


# ---------- 1 登录两个入口：按行号套回 d88055b 的登录段落 ----------
SKIP = {3209, 3212, 4511}  # 成员页两段（下面另写）、方案 B 的英文词条（留着无害）
lines = s.split('\n')
hunks = []
for m in re.finditer(r'^@@ -(\d+)(?:,(\d+))? \+\d+(?:,\d+)? @@.*\n((?:[-+].*\n?)*)', open(DIFF, encoding='utf8').read(), re.M):
    a, n = int(m.group(1)), int(m.group(2) if m.group(2) is not None else 1)
    body = m.group(3).split('\n')
    old = [l[1:] for l in body if l.startswith('-')]
    new = [l[1:] for l in body if l.startswith('+')]
    hunks.append((a, n, old, new))
if len(hunks) != 13: sys.exit(f'[停止] diff 段数 {len(hunks)}（应为 13）')
for a, n, old, new in sorted(hunks, key=lambda h: -h[0]):
    if a in SKIP: continue
    if n == 0:  # 纯插入：插在第 a 行之后
        lines[a:a] = new
    else:
        if lines[a - 1:a - 1 + n] != old: sys.exit(f'[停止] 第 {a} 行和 diff 不一致，底稿不是 f350805')
        lines[a - 1:a - 1 + n] = new
s = '\n'.join(lines)
for k in ['id="acTabO"', 'id="acOrgF"', 'acCrossHint', 'data-to-tab="o"']:
    if k not in s: sys.exit('[停止] 登录两个入口没有套上：' + k)

# ---------- 2 成员页：保留邀请链接 ----------
rep('<div class="cs-hd"><div><h2>成员</h2><p>添加同事的邮箱，他们登录后在左上角切换到这个企业。额度和账单由企业账户统一管理；管理员可以管理成员、API Key 和账单，成员可以创建和使用自己的 API Key。</p></div></div>',
    '<div class="cs-hd"><div><h2>成员</h2><p>按工作邮箱添加同事，或把邀请链接发给同事，他们都用「企业登录」进入这个企业账户。额度和账单由企业账户统一管理；管理员可以管理成员、API Key 和账单，成员可以创建和使用自己的 API Key。</p></div></div>')
rep('<p class="cs-help">同事已有账号的，加入后直接可用；没有账号的会收到邮件，用这个邮箱登录即自动加入。没有邮箱的同事可以用邀请链接。成员被移除后，他创建的 API Key 同时失效。</p>',
    '<p class="cs-help">按邮箱添加：同事会收到邮件，用这个邮箱在「企业登录」用验证码登录即可。邀请链接：发到工作群，同事打开后用自己的工作邮箱验证就加入；链接可以随时重置，旧链接立即失效。成员被移除后，他创建的 API Key 同时失效。</p>')

# ---------- 3 控制台按身份：标记位 ----------
rep('<div class="bt-hd"><h1>API Key</h1><button class="bt-btn pri" type="button" data-go="keys" id="btNewKey">创建 API Key</button></div>',
    '<div class="bt-hd"><h1>API Key</h1><button class="bt-btn pri" type="button" data-go="keys" id="btNewKey">创建 API Key</button></div>\n          <p class="bt-who" id="btWho"></p>')
rep('<li data-ck="topup">', '<li data-ck="topup" data-roles="personal admin root">')
rep('<li data-ck="req">', '<li data-ck="req" data-roles="personal member root">')
rep('<button class="bt-btn" type="button" data-go="bill">去充值</button></li>',
    '<button class="bt-btn" type="button" data-go="bill">去充值</button></li>\n            <li data-ck="mem" data-roles="admin"><i aria-hidden="true"></i><div><b>已添加成员</b><p>按工作邮箱添加同事，或把邀请链接发到工作群。</p><span class="cs-st">未完成</span></div><button class="bt-btn" type="button" data-go="members">添加成员</button></li>')
rep('<div class="bt-orgs" id="btOrgs"></div>', '<div class="bt-orgs" id="btOrgs"></div>\n        <p class="bt-orgnote" id="btOrgNote"></p>')
rep('<div class="cs-hd"><div><h2>实名认证</h2><p>核验个人或企业身份。认证结果用于开票主体与合同签署。</p></div></div>',
    '<div class="cs-hd"><div><h2 id="supKycH">实名认证</h2><p id="supKycP">核验个人或企业身份。认证结果用于开票主体与合同签署。</p></div></div>')
rep('<li><div><b>个人认证</b>', '<li data-roles="personal root"><div><b>个人认证</b>')
rep('<li><div><b>企业认证</b>', '<li data-roles="admin root"><div><b>企业认证</b>')
rep('<div class="cs-hd"><div><h2>个人资料</h2><p>账户类型在注册时选择，同一个控制台。</p></div></div>',
    '<div class="cs-hd"><div><h2 id="csAcctH">个人资料</h2><p id="csAcctP">账户类型在注册时选择，同一个控制台。</p></div></div>')
rep('<h2>使用日志</h2><p>上方按模型汇总，下方逐条列出每次请求。</p>', '<h2>使用日志</h2><p id="csLogP">上方按模型汇总，下方逐条列出每次请求。</p>')
rep('<h2>用量分析</h2><p>按时间、API Key 和模型查看请求量、词元、费用与性能。</p>', '<h2>用量分析</h2><p id="supStP">按时间、API Key 和模型查看请求量、词元、费用与性能。</p>')

CSS = '''
<style id="identity-split-css">
/* 控制台按身份分开（2026-10-15）：沿用线上视觉，只加身份标注 */
.bt-orgn{display:grid;line-height:1.2;min-width:0}
.bt-orgn b{font-weight:500;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.bt-orgn small{font:400 11px var(--mono);letter-spacing:.04em;color:var(--ink-50);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.bt-orgs .bt-me{display:flex;align-items:center;gap:10px;padding:8px 10px}
.bt-orgnote{margin:0;padding:2px 14px 10px;font-size:12.5px;line-height:1.55;color:var(--ink-50)}
.bt-orgnote:empty{display:none}
.bt-who{margin:-8px 0 0;font-size:15px;line-height:1.5;color:rgba(255,255,255,.94);text-shadow:0 1px 10px rgba(33,32,33,.2)}
.bt-who:empty{display:none}
/* 账户菜单原来被右侧蓝色背景盖住一半（sticky 侧栏自成层叠上下文，排在主区下面）；把侧栏抬上来 */
.bt-side{z-index:20}
.bt-orgb{border-radius:12px;padding-top:6px;padding-bottom:6px}
@media (min-width:1001px){.bt[data-role="member"] .bt-check{grid-template-columns:repeat(2,minmax(0,1fr))}}
</style>
'''
k = s.rindex('</head>'); s = s[:k] + CSS + s[k:]

JS = r'''
  /* ======== 控制台按身份分开（2026-10-15）：个人登录进个人后台，企业登录进企业后台；后台里不切换身份 ======== */
  (function(){
    var nav=$('.cs-nav'); if(!nav) return;
    function nb(p){return nav.querySelector('[data-p="'+p+'"]')}
    function put(el,t){if(el) el.textContent=t}
    /* 侧栏分组：API Key 和模型、体验中心一组；「用量」一组；最后一组按身份叫「账户」或「企业管理」 */
    var acc=nav.querySelector('.cs-grp'); nb('play').after(nb('keys'));
    var gu=document.createElement('span'); gu.className='cs-grp bt-grp'; gu.textContent='用量';
    var rl=document.createElement('i'); rl.className='bt-rule'; rl.setAttribute('aria-hidden','true');
    acc.before(gu); gu.after(nb('usage')); acc.before(rl); nb('usage').after(nb('stats')); nb('sec').after(nb('acct'));
    var WHO={personal:'个人账户',admin:'企业 · 管理员',member:'企业 · 成员',root:'超级管理员'};
    var HERO={personal:'个人账户 · 在线充值，按实际用量扣费',admin:'企业账户 · 管理员 · 成员的用量从企业余额扣',member:'企业账户 · 成员 · 用量计入企业账单，额度由管理员分配',root:'运营账户 · 平台管理在左侧「管理员」分组'};
    var NOTE={personal:'企业成员请退出后，用「企业登录」进入。',admin:'个人账户请退出后，用「个人登录」进入。',member:'个人账户请退出后，用「个人登录」进入。',root:''};
    var _ra=roleApply; roleApply=function(){_ra(); var role=me.role||'personal', org=role==='admin'||role==='member';
      var name=org?(me.org||'企业账户'):role==='root'?(me.org||'沐仞运营'):(me.email||me.phone||'我的账户');
      $('#btOrgN').innerHTML='<b>'+esc(name)+'</b><small>'+esc(WHO[role]||'')+'</small>';
      $('#btOrgs').innerHTML='<div class="bt-me"><i>'+(lang==='en'?(org?'B':role==='root'?'F':'P'):esc(name.charAt(0)))+'</i><span><b>'+esc(name)+'</b><small>'+esc(roleName(role))+'</small></span></div>';
      put($('#btOrgNote'),NOTE[role]||''); put($('#btWho'),HERO[role]||'');
      put(acc,role==='admin'?'企业管理':'账户');
      var kb=nb('kyc'); if(kb) put($('span',kb),role==='admin'?'企业认证':'实名认证');
      put($('#supKycH'),role==='admin'?'企业认证':'实名认证');
      put($('#supKycP'),role==='admin'?'上传营业执照，核验企业身份。认证后，发票抬头与合同主体为企业。':role==='root'?'核验个人或企业身份。认证结果用于开票主体与合同签署。':'核验个人身份。认证结果用于开票与合同签署。');
      put($('#csAcctH'),org?'账号资料':'个人资料');
      put($('#csAcctP'),org?'你在企业账户里的账号资料与通知设置。个人账户请退出后，用「个人登录」进入。':role==='root'?'运营账号的资料与通知设置。':'个人账户的资料与通知设置。企业成员请用「企业登录」进入。');
      put($('#csLogP'),role==='member'?'只显示你自己的请求。上方按模型汇总，下方逐条列出每次请求。':role==='admin'?'显示企业全部成员的请求。上方按模型汇总，下方逐条列出每次请求。':'上方按模型汇总，下方逐条列出每次请求。');
      put($('#supStP'),role==='member'?'只统计你自己的请求：按时间、API Key 和模型查看请求量、词元、费用与性能。':role==='admin'?'统计企业全部成员的请求：按时间、API Key 和模型查看请求量、词元、费用与性能。':'按时间、API Key 和模型查看请求量、词元、费用与性能。');
      put($('#btCheck [data-ck="topup"] p'),role==='admin'?'在线充值或对公转账，成员的用量从企业余额扣。':'在线充值后按实际用量扣费。');
      if(role==='member') put($('#btCredL'),'我的额度');
      var mr=$('#btMem')&&$('#btMem').closest('.bt-row'); if(mr) mr.hidden=!(role==='admin'||role==='root');
      ckCount()};
    /* 「开始使用」只数当前身份能看到的几项 */
    function ckCount(){if(!me) return; var role=me.role||'personal', st={key:me.keys.length>0,topup:TOPUPS.length>0||BALANCE>0,req:LOGS.length>0,mem:(me.subs||[]).length>0}, n=0, d=0;
      $$('#btCheck [data-ck]').forEach(function(li){var r=li.getAttribute('data-roles'); if(r&&r.split(' ').indexOf(role)<0) return; n++; var on=!!st[li.getAttribute('data-ck')], s2=$('.cs-st',li); if(on) d++; li.classList.toggle('done',on); s2.className='cs-st'+(on?' ok':''); s2.textContent=on?'已完成':'未完成'});
      $('#btProg').textContent=d+' / '+n}
    var _pr=platRender; platRender=function(){_pr(); ckCount()};
  })();
'''
rep("  $$('[data-product-target]').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();jumpTo(a.getAttribute('data-product-target'))})});\n  window.addEventListener('hashchange',route); route();",
    JS + "  $$('[data-product-target]').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();jumpTo(a.getAttribute('data-product-target'))})});\n  window.addEventListener('hashchange',route); route();")

EN = {'我的账户': 'My account', '个人账户': 'Personal account', '用量': 'Usage', '企业管理': 'Organization', '企业认证': 'Company verification', '个人': 'Personal', '企业 · 管理员': 'Admin', '企业 · 成员': 'Member',  # 英文侧栏窄，企业名已在上一行，只写角色
      '沐仞运营': 'FathomPeak operations',
      '个人账户 · 在线充值，按实际用量扣费': 'Personal account · top up online, pay for what you use',
      '企业账户 · 管理员 · 成员的用量从企业余额扣': "Business account · Admin · members' usage is charged to the business balance",
      '企业账户 · 成员 · 用量计入企业账单，额度由管理员分配': 'Business account · Member · usage goes on the business bill; your admin sets your allowance',
      '运营账户 · 平台管理在左侧「管理员」分组': 'Operations account · platform tools are under Admin on the left',
      '企业成员请退出后，用「企业登录」进入。': 'Business members: sign out, then use Business sign-in.',
      '个人账户请退出后，用「个人登录」进入。': 'For your personal account, sign out, then use Personal sign-in.',
      '上传营业执照，核验企业身份。认证后，发票抬头与合同主体为企业。': 'Upload the business licence to verify the company. Invoices and contracts are then issued to the company.',
      '核验个人身份。认证结果用于开票与合同签署。': 'Verify your identity. The result is used for invoices and contracts.',
      '账号资料': 'Account profile',
      '你在企业账户里的账号资料与通知设置。个人账户请退出后，用「个人登录」进入。': 'Your profile and notification settings in the business account. For your personal account, sign out, then use Personal sign-in.',
      '运营账号的资料与通知设置。': 'Profile and notification settings for the operations account.',
      '个人账户的资料与通知设置。企业成员请用「企业登录」进入。': 'Profile and notification settings for your personal account. Business members use Business sign-in.',
      '只显示你自己的请求。上方按模型汇总，下方逐条列出每次请求。': 'Only your own requests. A per-model summary at the top, every request listed below.',
      '显示企业全部成员的请求。上方按模型汇总，下方逐条列出每次请求。': 'Requests from every member of the business. A per-model summary at the top, every request listed below.',
      '只统计你自己的请求：按时间、API Key 和模型查看请求量、词元、费用与性能。': 'Only your own requests: volume, tokens, cost and performance by time, API key and model.',
      '统计企业全部成员的请求：按时间、API Key 和模型查看请求量、词元、费用与性能。': "All members' requests: volume, tokens, cost and performance by time, API key and model.",
      '在线充值或对公转账，成员的用量从企业余额扣。': "Top up online or by bank transfer; members' usage is charged to the business balance.",
      '我的额度': 'My allowance', '已添加成员': 'Members added', '按工作邮箱添加同事，或把邀请链接发到工作群。': 'Add colleagues by work email, or share the invite link in your team chat.', '添加成员': 'Add members',
      '按工作邮箱添加同事，或把邀请链接发给同事，他们都用「企业登录」进入这个企业账户。额度和账单由企业账户统一管理；管理员可以管理成员、API Key 和账单，成员可以创建和使用自己的 API Key。': 'Add colleagues by work email or send them the invite link; either way they use Business sign-in to enter this business account. Allowance and billing are managed centrally; admins manage members, API keys and billing, members create and use their own API keys.',
      '按邮箱添加：同事会收到邮件，用这个邮箱在「企业登录」用验证码登录即可。邀请链接：发到工作群，同事打开后用自己的工作邮箱验证就加入；链接可以随时重置，旧链接立即失效。成员被移除后，他创建的 API Key 同时失效。': "By email: your colleague gets an email and signs in with that address and a code under Business sign-in. Invite link: share it in your team chat; colleagues open it and verify their own work email to join. You can reset the link at any time and the old one stops working. When a member is removed, the API keys they created stop working too."}
FORCE = ['企业认证']  # 旧词条里有一处译成 Company，统一成 Company verification
rep('  syncAuthLocale(); applyLang();', '  (function(S){for(var k in S) if(!(k in I18N)) I18N[k]=S[k]})(' + json.dumps(EN, ensure_ascii=False) + ');  /* 按身份分开的英文：只补缺 */\n  '
    + ''.join('I18N[%s]=%s;' % (json.dumps(k, ensure_ascii=False), json.dumps(EN[k], ensure_ascii=False)) for k in FORCE) + '  /* 这几个键强制用新译法 */\n  syncAuthLocale(); applyLang();')
open(OUT, 'w', encoding='utf8').write(s)
print('done:', OUT)
