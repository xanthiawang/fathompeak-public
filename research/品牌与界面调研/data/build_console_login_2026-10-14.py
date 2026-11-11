"""登录：个人登录 / 企业登录两个入口（Zixin 2026-10-14 晚："还是要分成个人用户登录和企业用户登录……点错了账号不就废了吗？"
"下面不用加演示、登录什么的，直接给正式的 UI"）。
口径：
 - 两种账号分开：个人账号用手机号 / 邮箱验证码或微信（海外 Google / GitHub）自助注册；企业账号由沐仞开通管理员、管理员再分配成员
   （开发 9/24："B 端成员账号由管理员派发"），用企业账号 + 密码登录，不能在登录页注册。
 - 点错入口不会废掉账号：企业登录不会创建任何账号，登录失败会提示切到个人登录；个人登录只会创建个人账号，以后申请企业账户也不受影响。
 - 页面记住上次用的入口。超级管理员走单独的运营后台登录（#admin-login），官网不放链接。
预览里：个人登录 → 个人控制台；企业登录 → 企业管理员控制台；运营后台登录 → 超管控制台。不发起真实请求。
叠加顺序：线上 → supplement → console_backend → superadmin → 本脚本 → playground → role_versions。
用法：python3 -I build_console_login_2026-10-14.py <输入 html> <输出 html>
"""
import json, sys

LIVE = '--live' in sys.argv  # 上线版：两个入口照样显示，但个人 / 企业 / 运营后台登录都提示尚未开通，不进入预览控制台
args = [x for x in sys.argv[1:] if not x.startswith('--')]
SRC, OUT = args[0], args[1]
s = open(SRC, encoding='utf8').read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: sys.exit(f'[停止] 匹配 {c} 次（应为 {n}）：{old[:80]}')
    s = s.replace(old, new)


# ---------- 1 登录页：个人 / 企业切换 ----------
rep('        <p class="ac-lead">管理 API Key、用量与账单。</p>\n',
    '        <p class="ac-lead">管理 API Key、用量与账单。</p>\n'
    '        <div class="ac-seg" role="tablist" aria-label="登录入口"><button type="button" role="tab" id="acTabP" aria-selected="true" aria-controls="acPersonal" data-tab="p">个人登录</button>'
    '<button type="button" role="tab" id="acTabO" aria-selected="false" aria-controls="acOrg" tabindex="-1" data-tab="o">企业登录</button></div>\n'
    '        <div id="acPersonal" role="tabpanel" aria-labelledby="acTabP">\n')
ORG = '''        </div>
        <div id="acOrg" role="tabpanel" aria-labelledby="acTabO" hidden>
          <form id="acOrgF" class="ac-auth-form" novalidate>
            <div class="ac-f"><label for="acOrgU">企业账号</label><input class="in" id="acOrgU" autocomplete="username" autocapitalize="none" spellcheck="false" placeholder="管理员分配的账号或企业邮箱"></div>
            <div class="ac-f"><label for="acOrgPw">密码</label><input class="in" id="acOrgPw" type="password" autocomplete="current-password" placeholder="请输入密码"><p class="ac-help">忘记密码？请联系企业管理员重置。管理员请联系沐仞。</p></div>
            <label class="ac-ok"><input id="acOrgAgree" type="checkbox"><span>我已阅读并同意<a class="ul" href="#terms" target="_blank" rel="noopener">用户服务协议</a>和<a class="ul" href="#privacy" target="_blank" rel="noopener">隐私政策</a></span></label>
            <p class="ac-msg" id="acOrgMsg" role="alert"></p>
            <button class="btn black full" type="submit">登录</button>
          </form>
          <p class="ac-help ac-orgnote">企业账号由沐仞或企业管理员分配，不能在这里注册。个人用户请用<button class="ac-inl" type="button" data-to-tab="p">个人登录</button>。</p>
          <div class="ac-orgapply"><span>还没有企业账户？</span><a class="ul" href="#enterprise" data-scrollto="enterprise-sales">申请开通 →</a></div>
        </div>
'''
rep('        <div class="ac-service" id="acService" role="status" tabindex="-1" hidden>', ORG + '        <div class="ac-service" id="acService" role="status" tabindex="-1" hidden>')
rep('<p class="ac-help ac-first" id="acFirst">未注册的手机号验证后将自动创建账户。</p>',
    '<p class="ac-help ac-first" id="acFirst">未注册的手机号验证后将自动创建个人账户。企业成员请用<button class="ac-inl" type="button" data-to-tab="o">企业登录</button>。</p>')

# 登录、发码、第三方：预览里接到对应控制台
rep("if(!/^\\d{6}$/.test($('#acCode').value.trim())){authError($('#acCode'),'请输入 6 位验证码。');return}authUnavailable(authMethod)});",
    "if(!/^\\d{6}$/.test($('#acCode').value.trim())){authError($('#acCode'),'请输入 6 位验证码。');return}if(window.supLogin){window.supLogin('personal');return}authUnavailable(authMethod)});")
rep("$('#acSend').addEventListener('click',function(){if(authLocale!=='zh'||!authIdentifier()||!requireAuthConsent())return;authUnavailable(authMethod)});",
    "$('#acSend').addEventListener('click',function(){if(authLocale!=='zh'||!authIdentifier()||!requireAuthConsent())return;if(window.supCountdown){window.supCountdown(this);return}authUnavailable(authMethod)});")

# ---------- 2 运营后台登录 ----------
ADMIN = '''<!-- 运营后台登录（超级管理员单独入口，2026-10-14） -->
<section data-route="admin-login">
  <div class="ac ad-login">
    <div class="ac-art"><img class="ac-engraving" loading="lazy" src="art/account/engraved-ascent_2026-10-14.webp" width="1024" height="1536" decoding="async" alt="" draggable="false"></div>
    <div class="ac-main">
      <div class="ac-form">
        <span class="k">沐仞运营后台</span>
        <h1 class="display">员工登录</h1>
        <p class="ac-lead">仅限沐仞员工使用。每次登录都需要两步验证。</p>
        <form id="adLogin" class="ac-auth-form" novalidate>
          <div class="ac-f"><label for="adMail">工作邮箱</label><input class="in" id="adMail" type="email" autocomplete="username" autocapitalize="none" spellcheck="false"></div>
          <div class="ac-f"><label for="adPw">密码</label><input class="in" id="adPw" type="password" autocomplete="current-password"></div>
          <div class="ac-f"><label for="adOtp">两步验证码</label><input class="in mono" id="adOtp" inputmode="numeric" maxlength="6" autocomplete="one-time-code" placeholder="身份验证器里的 6 位数字"></div>
          <p class="ac-msg" id="adMsg" role="alert"></p>
          <button class="btn black full" type="submit">登录运营后台</button>
        </form>
        <div class="ac-support"><p><span>不是员工？</span> <a class="ul" href="#login">客户登录 →</a></p></div>
      </div>
    </div>
  </div>
</section>

'''
rep('<!-- 往期周报 -->', ADMIN + '<!-- 往期周报 -->')
rep("login:'登录 - 沐仞科技 FathomPeak',", "login:'登录 - 沐仞科技 FathomPeak','admin-login':'运营后台登录 - 沐仞科技 FathomPeak',")

CSS = '''
<style id="sup-login-css">
/* 登录：个人 / 企业两个入口（2026-10-14） */
.ac-seg{display:grid;grid-template-columns:1fr 1fr;gap:4px;padding:4px;margin:22px 0 6px;border-radius:999px;background:var(--gray-btn,rgba(61,49,79,.07))}
.ac-seg button{appearance:none;border:0;height:40px;border-radius:999px;background:transparent;font:500 15px var(--sans);color:var(--ink-70);cursor:pointer;transition:background .25s,color .2s,box-shadow .25s}
.ac-seg button[aria-selected="true"]{background:#fff;color:var(--ink);box-shadow:0 1px 2px rgba(0,0,0,.06),0 6px 16px -10px rgba(0,0,0,.25)}
.ac-seg button:focus-visible{outline:2px solid var(--ink);outline-offset:2px}
.ac-inl{appearance:none;border:0;background:none;padding:0;font:inherit;color:var(--ink);text-decoration:underline;text-underline-offset:3px;cursor:pointer}
.ac-orgnote{margin-top:14px}
.ac-orgapply{display:flex;gap:8px;align-items:baseline;margin-top:22px;padding-top:18px;border-top:1px solid var(--line);font-size:14px;color:var(--ink-70)}
.ad-login .k{display:block;margin-bottom:10px}
/* 运营后台登录是内部入口：不显示官网导航、页脚和咨询浮窗 */
body:has(section[data-route="admin-login"].on) .hdr,body:has(section[data-route="admin-login"].on) footer,body:has(section[data-route="admin-login"].on) .fab,body:has(section[data-route="admin-login"].on) .dock{display:none}
</style>
'''
k = s.rindex('</head>'); s = s[:k] + CSS + s[k:]

JS = r'''
  /* ======== 登录：个人 / 企业两个入口（2026-10-14） ======== */
  (function(){
    var T={personal:['personal',''],admin:['company','admin'],member:['company','member'],super:['super','super']};
    function enter(k){var t=T[k]; me={email:'',type:t[0],role:t[1],since:today(),keys:[],subs:[],edu:'none',preview:true}; logged=true; syncLogin(); location.hash='#console'}
    var LIVE=__LIVE__; if(!LIVE) window.supLogin=enter;
    function svc(t){var b=$('#acService'); if(b){$('#acServiceText').textContent=t; b.hidden=false; b.focus()} else toast(t)}
    /* 个人 / 企业切换，记住上次用的入口 */
    function tab(t,focus){var org=t==='o'; $('#acPersonal').hidden=org; $('#acOrg').hidden=!org;
      [['#acTabP','p'],['#acTabO','o']].forEach(function(x){var b=$(x[0]), on=x[1]===t; b.setAttribute('aria-selected',String(on)); b.tabIndex=on?0:-1});
      try{localStorage.setItem('fp-login-tab',t)}catch(e){} if(focus) (org?$('#acOrgU'):$('#acTabP')).focus()}
    $$('.ac-seg [data-tab]').forEach(function(b){b.addEventListener('click',function(){tab(b.getAttribute('data-tab'),false)});
      b.addEventListener('keydown',function(e){if(e.key==='ArrowRight'||e.key==='ArrowLeft'){e.preventDefault(); var t=b.getAttribute('data-tab')==='p'?'o':'p'; tab(t,false); $(t==='p'?'#acTabP':'#acTabO').focus()}})});
    $$('[data-to-tab]').forEach(function(b){b.addEventListener('click',function(){tab(b.getAttribute('data-to-tab'),true)})});
    var last='p'; try{last=localStorage.getItem('fp-login-tab')||'p'}catch(e){} tab(last==='o'?'o':'p',false);
    /* 企业登录 */
    $('#acOrgF').addEventListener('submit',function(e){e.preventDefault(); var m=$('#acOrgMsg'); m.textContent='';
      if(!$('#acOrgU').value.trim()){m.textContent='请输入企业账号。'; $('#acOrgU').focus(); return}
      if(!$('#acOrgPw').value){m.textContent='请输入密码。'; $('#acOrgPw').focus(); return}
      if(!$('#acOrgAgree').checked){m.textContent='请先阅读并同意用户服务协议和隐私政策。'; return}
      $('#acOrgPw').value=''; if(LIVE){svc('企业登录尚未开通。如需开通企业账户，请联系我们。');return} enter('admin')});
    /* 获取验证码：60 秒倒计时 */
    if(!LIVE) window.supCountdown=function(btn){if(btn._t) return; var n=60, txt=btn.textContent; btn.disabled=true; btn.textContent='重新发送 '+n+'s';
      btn._t=setInterval(function(){n--; if(n<=0){clearInterval(btn._t); btn._t=null; btn.disabled=false; btn.textContent=txt; return} btn.textContent='重新发送 '+n+'s'},1000)};
    /* 第三方登录（微信 / Google / GitHub）都是个人账号 */
    if(!LIVE) $$('[data-provider]').forEach(function(b){b.addEventListener('click',function(e){e.stopImmediatePropagation(); enter('personal')},true)});
    /* 运营后台登录 */
    $('#adLogin').addEventListener('submit',function(e){e.preventDefault(); var m=$('#adMsg'); m.textContent='';
      if(!MAIL.test($('#adMail').value.trim())){m.textContent='请输入工作邮箱。'; $('#adMail').focus(); return}
      if(!$('#adPw').value){m.textContent='请输入密码。'; $('#adPw').focus(); return}
      if(!/^\d{6}$/.test($('#adOtp').value.trim())){m.textContent='请输入 6 位两步验证码。'; $('#adOtp').focus(); return}
      $('#adPw').value=''; $('#adOtp').value=''; if(LIVE){m.textContent='运营后台尚未接入。员工账号由开发开通。';return} enter('super')});
  })();
'''
JS = JS.replace('__LIVE__', 'true' if LIVE else 'false')
rep("  $$('[data-product-target]').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();jumpTo(a.getAttribute('data-product-target'))})});\n  window.addEventListener('hashchange',route); route();",
    JS + "  $$('[data-product-target]').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();jumpTo(a.getAttribute('data-product-target'))})});\n  window.addEventListener('hashchange',route); route();")
RX_ADD = ",\n    [/^重新发送 (\\d+)s$/, function(m,a){return 'Resend in '+a+'s'}]"
rep('\n  ];\n  function rxTr(k){', RX_ADD + '\n  ];\n  function rxTr(k){')
EN = {
    '个人登录': 'Personal', '企业登录': 'Business', '登录入口': 'Sign-in type', '企业账号': 'Business account', '管理员分配的账号或企业邮箱': 'Account from your admin, or company email',
    '请输入密码': 'Enter your password', '忘记密码？请联系企业管理员重置。管理员请联系沐仞。': 'Forgot your password? Ask your company admin to reset it. Admins, contact FathomPeak.',
    '企业账号由沐仞或企业管理员分配，不能在这里注册。个人用户请用': 'Business accounts are issued by FathomPeak or your company admin and cannot be created here. Individuals, use',
    '还没有企业账户？': 'No business account yet?', '申请开通 →': 'Apply →', '未注册的手机号验证后将自动创建个人账户。企业成员请用': 'Unregistered numbers get a personal account after verification. Company members, use',
    '请输入企业账号。': 'Enter your business account.', '请输入密码。': 'Enter your password.', '请先阅读并同意用户服务协议和隐私政策。': 'Please agree to the Terms of Service and Privacy Policy first.',
    '沐仞运营后台': 'FathomPeak operations console', '员工登录': 'Staff sign-in', '仅限沐仞员工使用。每次登录都需要两步验证。': 'For FathomPeak staff only. Two-step verification is required at every sign-in.',
    '工作邮箱': 'Work email', '密码': 'Password', '两步验证码': 'Two-step code', '身份验证器里的 6 位数字': '6 digits from your authenticator app', '登录运营后台': 'Sign in',
    '不是员工？': 'Not staff?', '客户登录 →': 'Customer sign-in →', '运营后台登录 - 沐仞科技 FathomPeak': 'Operations sign-in - FathomPeak',
    '请输入工作邮箱。': 'Enter your work email.', '企业登录尚未开通。如需开通企业账户，请联系我们。': 'Business sign-in is not available yet. Contact us to open a business account.', '运营后台尚未接入。员工账号由开发开通。': 'The operations console is not connected yet. Staff accounts are set up by the developers.', '请输入 6 位两步验证码。': 'Enter the 6-digit two-step code.',
}
rep('  syncAuthLocale(); applyLang();', '  (function(S){for(var k in S) if(!(k in I18N)) I18N[k]=S[k]})(' + json.dumps(EN, ensure_ascii=False) + ');  /* 登录英文：只补缺 */\n  syncAuthLocale(); applyLang();')
open(OUT, 'w', encoding='utf8').write(s)
print('done:', OUT)
