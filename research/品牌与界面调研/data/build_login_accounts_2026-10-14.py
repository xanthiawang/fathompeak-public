"""登录与账号三处修改（Zixin 2026-10-14 夜："按这三条改，然后做开发交接说明"）。叠在线上 index.html（1652761 起）上。
 1 成员账号就是工作邮箱：企业登录改成「工作邮箱 + 邮箱验证码 / 密码」两种方式（默认验证码；忘记密码直接用验证码登录）；
   成员页「邀请」改「添加成员」（工作邮箱 + 角色），去掉「复制邀请链接」（链接注册的账号不是管理员加的工作邮箱）；
   超管开通企业时，管理员同样用工作邮箱 + 验证码首次登录。
 2 登录页互相提示：个人登录、企业登录各有一条提示条（「这个邮箱有企业账号 / 没有企业账号但有个人账号」+ 一键切换并带上已填的邮箱）。
   提示由平台的账号查询接口决定，前端留 window.acCrossHint('p'|'o') 给开发接；平台没接之前不会出现。
 3 企业自助申请、运营一键开通：官网「企业合作」表单删「预计月用量」，加「同时申请开通企业账户」（勾选后才出现工作邮箱，必填）；
   超管「用户与组织」页加「企业开户申请」列表（数据入口 RT_APPS），点「开通」带入企业名称和管理员邮箱。
线上口径不变：所有登录在平台接通前都只提示「尚未开通」。
用法：python3 -I build_login_accounts_2026-10-14.py <线上 index.html> <输出 html>
"""
import json, re, sys

SRC, OUT = sys.argv[1], sys.argv[2]
s = open(SRC, encoding='utf8').read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: sys.exit(f'[停止] 匹配 {c} 次（应为 {n}）：{old[:80]}')
    s = s.replace(old, new)


AGREE_O = '<label class="ac-ok"><input id="acOrgAgree" type="checkbox"><span>我已阅读并同意<a class="ul" href="#terms" target="_blank" rel="noopener">用户服务协议</a>和<a class="ul" href="#privacy" target="_blank" rel="noopener">隐私政策</a></span></label>'

# ---------- 1 企业登录：工作邮箱 + 验证码 / 密码 ----------
a = s.index('          <form id="acOrgF" class="ac-auth-form" novalidate>'); b = s.index('          </form>', a) + len('          </form>')
s = s[:a] + '''          <div class="ac-methods" role="tablist" aria-label="企业登录方式"><button type="button" role="tab" id="acOmCode" aria-selected="true" data-om="code">邮箱验证码</button><button type="button" role="tab" id="acOmPw" aria-selected="false" tabindex="-1" data-om="pw">密码</button></div>
          <form id="acOrgF" class="ac-auth-form" novalidate>
            <div class="ac-f"><label for="acOrgU">工作邮箱</label><input class="in" id="acOrgU" type="email" autocomplete="username" autocapitalize="none" spellcheck="false" placeholder="管理员为你添加的工作邮箱"></div>
            <div class="ac-f" data-omf="code"><label for="acOrgC">验证码</label><div class="ac-code"><input class="in" id="acOrgC" inputmode="numeric" autocomplete="one-time-code" placeholder="请输入验证码" maxlength="6"><button class="ac-send" id="acOrgSend" type="button">获取验证码</button></div></div>
            <div class="ac-f" data-omf="pw" hidden><label for="acOrgPw">密码</label><input class="in" id="acOrgPw" type="password" autocomplete="current-password" placeholder="请输入密码"><p class="ac-help">忘记密码？<button class="ac-inl" type="button" data-om-go="code">用邮箱验证码登录</button>，登录后可以重设。</p></div>
            <div class="ac-cross" id="acCrossO" role="status" hidden><span>这个邮箱没有企业账号，但有个人账号。</span><button class="ac-inl" type="button" data-cross="p">去个人登录 →</button></div>
            ''' + AGREE_O + '''
            <p class="ac-msg" id="acOrgMsg" role="alert"></p>
            <button class="btn black full" type="submit">登录</button>
          </form>''' + s[b:]
rep('<p class="ac-help ac-orgnote">企业账号由沐仞或企业管理员分配，不能在这里注册。个人用户请用<button class="ac-inl" type="button" data-to-tab="p">个人登录</button>。</p>',
    '<p class="ac-help ac-orgnote">企业账号就是管理员为你添加的工作邮箱，不能在这里注册。个人用户请用<button class="ac-inl" type="button" data-to-tab="p">个人登录</button>。</p>')
# 登录脚本里的企业登录处理：两种方式；线上仍提示尚未开通
rep("""    $('#acOrgF').addEventListener('submit',function(e){e.preventDefault(); var m=$('#acOrgMsg'); m.textContent='';
      if(!$('#acOrgU').value.trim()){m.textContent='请输入企业账号。'; $('#acOrgU').focus(); return}
      if(!$('#acOrgPw').value){m.textContent='请输入密码。'; $('#acOrgPw').focus(); return}
      if(!$('#acOrgAgree').checked){m.textContent='请先阅读并同意用户服务协议和隐私政策。'; return}
      $('#acOrgPw').value=''; if(LIVE){svc('企业登录尚未开通。如需开通企业账户，请联系我们。');return} enter('admin')});""",
    """    var om='code';
    function omSet(v){om=v; $$('#acOrg [data-om]').forEach(function(b){var on=b.getAttribute('data-om')===v; b.setAttribute('aria-selected',String(on)); b.tabIndex=on?0:-1}); $$('#acOrg [data-omf]').forEach(function(f){f.hidden=f.getAttribute('data-omf')!==v}); $('#acOrgMsg').textContent=''}
    $$('#acOrg [data-om]').forEach(function(b){b.addEventListener('click',function(){omSet(b.getAttribute('data-om'))})});
    $$('#acOrg [data-om-go]').forEach(function(b){b.addEventListener('click',function(){omSet(b.getAttribute('data-om-go')); $('#acOrgC').focus()})});
    function orgMail(){var v=$('#acOrgU').value.trim(); if(!MAIL.test(v)){$('#acOrgMsg').textContent='请输入有效的工作邮箱。'; $('#acOrgU').focus(); return ''} return v}
    $('#acOrgSend').addEventListener('click',function(){$('#acOrgMsg').textContent=''; if(!orgMail()) return; if(LIVE){svc('企业登录尚未开通。如需开通企业账户，请联系我们。');return} if(window.supCountdown) window.supCountdown(this)});
    $('#acOrgF').addEventListener('submit',function(e){e.preventDefault(); var m=$('#acOrgMsg'); m.textContent='';
      if(!orgMail()) return;
      if(om==='code'&&!/^\\d{6}$/.test($('#acOrgC').value.trim())){m.textContent='请输入 6 位验证码。'; $('#acOrgC').focus(); return}
      if(om==='pw'&&!$('#acOrgPw').value){m.textContent='请输入密码。'; $('#acOrgPw').focus(); return}
      if(!$('#acOrgAgree').checked){m.textContent='请先阅读并同意用户服务协议和隐私政策。'; return}
      $('#acOrgPw').value=''; if(LIVE){svc('企业登录尚未开通。如需开通企业账户，请联系我们。');return} enter('admin')});""")

# ---------- 2 互相提示 ----------
rep('<label class="ac-ok"><input id="acAgree" type="checkbox" name="agree" required>',
    '<div class="ac-cross" id="acCrossP" role="status" hidden><span>这个手机号 / 邮箱有企业账号。企业成员请用企业登录。</span><button class="ac-inl" type="button" data-cross="o">去企业登录 →</button></div>\n            '
    '<label class="ac-ok"><input id="acAgree" type="checkbox" name="agree" required>')

# ---------- 1 成员页：添加成员（工作邮箱 + 角色） ----------
rep('<div class="cs-hd"><div><h2>成员</h2><p>邀请同事加入企业账户。额度和账单由企业账户统一管理；管理员可以管理成员、API Key 和账单，成员可以创建和使用自己的 API Key。</p></div></div>',
    '<div class="cs-hd"><div><h2>成员</h2><p>添加同事的工作邮箱，他们就能用「企业登录」进入这个企业账户。额度和账单由企业账户统一管理；管理员可以管理成员、API Key 和账单，成员可以创建和使用自己的 API Key。</p></div></div>')
rep('        <h3 class="cs-h3">邀请</h3>\n        <form class="cs-newf" id="csInv" novalidate><input class="in" type="email" name="email" placeholder="同事邮箱" aria-label="同事邮箱" autocomplete="off">',
    '        <h3 class="cs-h3">添加成员</h3>\n        <form class="cs-newf" id="csInv" novalidate><input class="in" type="email" name="email" placeholder="同事的工作邮箱" aria-label="同事的工作邮箱" autocomplete="off">')
rep('<button class="btn black sm" type="submit">发邀请</button><button class="btn gray sm" type="button" id="csInvLink">复制邀请链接</button></form>',
    '<button class="btn black sm" type="submit">添加</button></form>')
rep('<p class="cs-help">邮件邀请适合有邮箱的同事；没有邮箱的同事用邀请链接注册后自动加入。成员被移除后，他创建的 API Key 同时失效。</p>',
    '<p class="cs-help">成员的账号就是这个工作邮箱：第一次用邮箱验证码登录，之后可以设密码，也可以一直用验证码，忘记密码不用找人重置。成员被移除后，他创建的 API Key 同时失效。</p>')
rep("$('#csInvLink').addEventListener('click',", "var _invL=$('#csInvLink'); if(_invL) _invL.addEventListener('click',")
rep("toast('已发出邀请，对方接受后显示为已加入。')", "toast('已添加。对方用这个工作邮箱登录企业账号，第一次用邮箱验证码。')")
rep('<p class="cs-help">开通后给这个邮箱发邀请，对方接受后成为企业管理员。</p>',
    '<p class="cs-help">管理员的账号就是这个工作邮箱，第一次用邮箱验证码登录「企业登录」。</p>')

# ---------- 3 企业开户申请 ----------
rep('<div class="f"><input class="in" name="预计用量" placeholder="预计月用量或任务规模" aria-label="预计月用量或任务规模"></div>', '')  # 门槛越低越好（Zixin：预计月用量删除）
rep('<div class="f"><input class="in" name="需求" placeholder="模型、应用场景或海外服务需求" aria-label="模型、应用场景或海外服务需求"></div><input class="hp" type="text" name="_honey"',
    '<div class="f"><input class="in" name="需求" placeholder="需求（可不填）：模型、应用场景或海外服务" aria-label="需求（可不填）"></div>'
    '<label class="f-chk"><input type="checkbox" name="申请开通企业账户" value="是" id="salesOpen"><span>同时申请开通企业账户</span></label>'
    '<div class="f" id="salesMailW" hidden><input class="in" type="email" name="工作邮箱" id="salesMail" placeholder="工作邮箱：开通后管理员用它登录" aria-label="工作邮箱" autocomplete="email"></div>'
    '<input class="hp" type="text" name="_honey"')
rep('        <form class="cs-ntf" id="rtNewF" hidden novalidate><h3 class="cs-h3">开通企业账户</h3>',
    '        <h3 class="cs-h3">企业开户申请</h3>\n'
    '        <div class="tbl"><table class="cs-tbl cs-wide"><thead><tr><th>提交时间</th><th>企业</th><th>联系方式</th><th>工作邮箱</th><th>需求</th><th><span class="sr">操作</span></th></tr></thead><tbody id="rtApps"></tbody></table></div>\n'
    '        <div class="cs-empty" id="rtApps0"><b>没有待处理的申请</b><span>客户在官网「企业合作」勾选「申请开通企业账户」后显示在这里。点「开通」会带入企业名称和管理员邮箱。</span></div>\n'
    '        <form class="cs-ntf" id="rtNewF" hidden novalidate><h3 class="cs-h3">开通企业账户</h3>')

CSS = '''
<style id="login-accounts-css">
/* 登录与账号三处修改（2026-10-14 夜） */
#acOrg .ac-methods{margin-top:14px}
.ac-cross{display:flex;flex-wrap:wrap;align-items:center;gap:6px 10px;margin:2px 0 4px;padding:11px 14px;border-radius:12px;font-size:13.5px;line-height:1.5;color:var(--ink);
  background:linear-gradient(100deg,#E3ECF8,#EEE7EC 56%,#F3E6E0);border:1px solid rgba(61,49,79,.10)}
.ac-cross .ac-inl{font-weight:500}
.f-chk{display:flex;gap:8px;align-items:flex-start;font-size:13.5px;color:var(--ink-70);line-height:1.5;margin:2px 0 4px}
.f-chk input{margin-top:3px}
</style>
'''
k = s.rindex('</head>'); s = s[:k] + CSS + s[k:]

JS = r'''
  /* ======== 登录与账号三处修改（2026-10-14 夜） ======== */
  (function(){
    /* 2 互相提示：平台查到这个手机号 / 邮箱属于另一类账号时，调用 acCrossHint('p') 或 acCrossHint('o') 显示提示 */
    window.acCrossHint=function(where){var p=$('#acCrossP'), o=$('#acCrossO'); if(p) p.hidden=where!=='p'; if(o) o.hidden=where!=='o'};
    ['#acPhone','#acEmail','#acOrgU'].forEach(function(k){var e=$(k); if(e) e.addEventListener('input',function(){window.acCrossHint('')})});
    $$('[data-cross]').forEach(function(b){b.addEventListener('click',function(){var to=b.getAttribute('data-cross');
      if(to==='o'){var v=($('#acEmail')&&$('#acEmail').value.trim())||''; var t=$('#acTabO'); if(t) t.click(); if(v) $('#acOrgU').value=v; $('#acOrgU').focus()}
      else {var v2=$('#acOrgU').value.trim(); var t2=$('#acTabP'); if(t2) t2.click(); var et=$('#acEmailTab'); if(v2&&et){et.click(); $('#acEmail').value=v2} }
      window.acCrossHint('')})});
    /* 3 企业开户申请：勾选「申请开通企业账户」时工作邮箱必填 */
    var so=$('#salesOpen'); if(so) so.addEventListener('change',function(){var w=$('#salesMailW'); w.hidden=!so.checked; if(so.checked) $('#salesMail').focus()});
    var sf=$('#salesForm'); if(sf) sf.addEventListener('submit',function(e){var c=$('#salesOpen'), m=$('#salesMail'); if(c&&c.checked&&!MAIL.test((m.value||'').trim())){e.preventDefault(); e.stopImmediatePropagation(); var msg=sf.querySelector('.form-msg'); if(msg) msg.textContent='申请开通企业账户需要填写工作邮箱。'; m.focus()}},true);
    /* 超管：企业开户申请列表。RT_APPS 由平台接口填充 {t, org, contact, mail, need}，前端不造数据 */
    var RT_APPS=[];
    function rtApps(){var tb=$('#rtApps'); if(!tb) return; tb.innerHTML=RT_APPS.map(function(a,i){return '<tr><td class="mono">'+esc(a.t||'')+'</td><td>'+esc(a.org||'')+'</td><td>'+esc(a.contact||'')+'</td><td>'+esc(a.mail||'')+'</td><td>'+esc(a.need||'')+'</td><td><button class="btn black sm" type="button" data-app="'+i+'">开通</button> <button class="btn gray sm" type="button" data-rej="'+i+'">拒绝</button></td></tr>'}).join('');
      $('#rtApps0').hidden=RT_APPS.length>0;
      $$('#rtApps [data-app]').forEach(function(b){b.addEventListener('click',function(){var a=RT_APPS[+b.getAttribute('data-app')]; var f=$('#rtNewF'); f.hidden=false; $('#rtOn').value=a.org||''; $('#rtOm').value=a.mail||''; f.scrollIntoView({block:'center'}); $('#rtOn').focus()})});
      $$('#rtApps [data-rej]').forEach(function(b){b.addEventListener('click',function(){toast('拒绝需要平台接入后才能通知申请人。')})})}
    var _rc=renderConsole; renderConsole=function(){_rc(); rtApps()};
  })();
'''
rep("  $$('[data-product-target]').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();jumpTo(a.getAttribute('data-product-target'))})});\n  window.addEventListener('hashchange',route); route();",
    JS + "  $$('[data-product-target]').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();jumpTo(a.getAttribute('data-product-target'))})});\n  window.addEventListener('hashchange',route); route();")

EN = {
    '企业登录方式': 'Business sign-in method', '邮箱验证码': 'Email code', '工作邮箱': 'Work email', '管理员为你添加的工作邮箱': 'The work email your admin added',
    '用邮箱验证码登录': 'sign in with an email code', '，登录后可以重设。': ', then reset it after signing in.', '忘记密码？': 'Forgot your password? ',
    '这个邮箱没有企业账号，但有个人账号。': 'This email has no business account, but it has a personal one.', '去个人登录 →': 'Go to personal sign-in →',
    '这个手机号 / 邮箱有企业账号。企业成员请用企业登录。': 'This phone number / email has a business account. Company members, use business sign-in.', '去企业登录 →': 'Go to business sign-in →',
    '企业账号就是管理员为你添加的工作邮箱，不能在这里注册。个人用户请用': 'A business account is the work email your admin added; it cannot be created here. Individuals, use',
    '请输入有效的工作邮箱。': 'Enter a valid work email.', '请输入 6 位验证码。': 'Enter the 6-digit code.',
    '添加同事的工作邮箱，他们就能用「企业登录」进入这个企业账户。额度和账单由企业账户统一管理；管理员可以管理成员、API Key 和账单，成员可以创建和使用自己的 API Key。': 'Add a colleague’s work email and they can use business sign-in to enter this account. Credit and billing are managed by the business account; admins manage members, API keys and billing, and members create and use their own API keys.',
    '添加成员': 'Add member', '同事的工作邮箱': 'Colleague’s work email', '添加': 'Add',
    '成员的账号就是这个工作邮箱：第一次用邮箱验证码登录，之后可以设密码，也可以一直用验证码，忘记密码不用找人重置。成员被移除后，他创建的 API Key 同时失效。': 'A member’s account is this work email: they sign in with an email code the first time, then can set a password or keep using codes, so nobody needs to reset passwords for them. When a member is removed, their API keys stop working.',
    '已添加。对方用这个工作邮箱登录企业账号，第一次用邮箱验证码。': 'Added. They sign in to the business account with this work email, using an email code the first time.',
    '管理员的账号就是这个工作邮箱，第一次用邮箱验证码登录「企业登录」。': 'The admin’s account is this work email; they sign in through business sign-in with an email code the first time.',
    '工作邮箱：开通后管理员用它登录': 'Work email: the admin signs in with it once the account is open', '同时申请开通企业账户': 'Also apply for a business account', '需求（可不填）：模型、应用场景或海外服务': 'Needs (optional): models, use case or overseas service', '需求（可不填）': 'Needs (optional)',
    '申请开通企业账户需要填写工作邮箱。': 'A work email is needed to apply for a business account.', '企业开户申请': 'Business account applications', '提交时间': 'Submitted', '企业': 'Company', '联系方式': 'Contact', '需求': 'Needs',
    '没有待处理的申请': 'No pending applications', '客户在官网「企业合作」勾选「申请开通企业账户」后显示在这里。点「开通」会带入企业名称和管理员邮箱。': 'Applications from the website’s Enterprise page appear here. Open fills in the company name and admin email.',
    '开通': 'Open', '拒绝': 'Decline', '拒绝需要平台接入后才能通知申请人。': 'Declining can notify the applicant once the platform is connected.',
}
rep('  syncAuthLocale(); applyLang();', '  (function(S){for(var k in S) if(!(k in I18N)) I18N[k]=S[k]})(' + json.dumps(EN, ensure_ascii=False) + ');  /* 登录与账号三处修改英文：只补缺 */\n  syncAuthLocale(); applyLang();')
open(OUT, 'w', encoding='utf8').write(s)
print('done:', OUT)
