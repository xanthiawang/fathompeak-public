"""登录即注册的账户怎么设置密码（Zixin 2026-10-28：「我们现在设置的登录即注册，那么密码怎么设置」→「改进原型，先出预览」）。
问题：验证码登录时自动注册（微信登录同理），账户本来就没有密码；但「安全与访问」只有「修改密码」，第一栏要填当前密码，这些用户设不了。
改法（密码是可选的第二种登录方式，账户分「未设置 / 已设置」两种状态）：
 · 安全与访问：「修改密码」改为「登录密码」一行，显示状态。
   未设置 → 按钮「设置密码」，用已绑定的手机号或邮箱收验证码，再填新密码，不要当前密码；
   已设置 → 按钮「修改」，填当前密码；忘了可点「忘了当前密码？用验证码验证」改用验证码。
   新密码规则：至少 8 位，同时包含字母和数字，不能包含手机号。
 · 登录页：密码登录不能注册，按钮下「未注册的手机号验证后将自动创建个人账户」只在验证码登录时显示；
   密码框下加一句「用验证码注册的账户默认没有密码…」，切换链接改为「忘了或没设置过密码？用验证码登录」。
 · 第二版（Zixin 发来密码态按钮截图：「登录/注册」）：按钮在密码登录时也写「登录 / 注册」，和验证码登录一致；
   注册仍然只能走验证码，所以密码态按钮下改为提示「新用户请用验证码登录，验证后自动创建个人账户。」
 · 原型里：用验证码进入的账户是「未设置」，用密码进入的是「已设置」；状态只存在当前页面。
用法：python3 -I build_password_setup_2026-10-28.py <站点根目录（含 index.html）>
"""
import json, sys
from pathlib import Path

p = Path(sys.argv[1]) / 'index.html'
s = p.read_text(encoding='utf8')
if 'id="csPwSt"' in s: sys.exit('[停止] 已经改过')


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: sys.exit(f'[停止] 匹配 {c} 次（应为 {n}）：{old[:90]}')
    s = s.replace(old, new)


# ---- 登录页 ----
rep('<input class="in" id="acPw" name="password" type="password" autocomplete="current-password" placeholder="请输入密码" disabled></div>',
    '<input class="in" id="acPw" name="password" type="password" autocomplete="current-password" placeholder="请输入密码" disabled><p class="ac-help" id="acPwHint">用验证码注册的账户默认没有密码，登录后可在「安全与访问」设置。</p></div>')
# 密码登录时：按钮仍写「登录 / 注册」；「自动注册」提示换成「新用户请用验证码登录」；切换链接覆盖「没设置过密码」的人
rep('<p class="ac-help ac-first" id="acFirst">未注册的手机号验证后将自动创建个人账户。企业成员请用<button class="ac-inl" type="button" data-to-tab="o">企业登录</button>。</p>',
    '<p class="ac-help ac-first" id="acFirst">未注册的手机号验证后将自动创建个人账户。企业成员请用<button class="ac-inl" type="button" data-to-tab="o">企业登录</button>。</p>\n            <p class="ac-help ac-first" id="acFirstPw" hidden>新用户请用验证码登录，验证后自动创建个人账户。</p>')
rep("$('#acPwSw').textContent=on?'忘记密码？用验证码登录':'用密码登录';$('#acContinue').textContent=(on||(authMethod!=='phone'&&authLocale==='zh'))?'登录':'登录 / 注册';",
    "$('#acPwSw').textContent=on?'忘了或没设置过密码？用验证码登录':'用密码登录';$('#acContinue').textContent=(authMethod!=='phone'&&authLocale==='zh')?'登录':'登录 / 注册';"
    "$('#acFirst').hidden=on||(authMethod!=='phone'&&authLocale==='zh');$('#acFirstPw').hidden=!on||(authMethod!=='phone'&&authLocale==='zh');")
rep("$('#acContinue').textContent=(authPw||(!phone&&authLocale==='zh'))?'登录':'登录 / 注册';$('#acFirst').hidden=!phone&&authLocale==='zh'}",
    "$('#acContinue').textContent=(!phone&&authLocale==='zh')?'登录':'登录 / 注册';$('#acFirst').hidden=authPw||(!phone&&authLocale==='zh');$('#acFirstPw').hidden=!authPw||(!phone&&authLocale==='zh')}")
# 原型：用密码进来的账户算「已设置密码」，用验证码进来的算「未设置」
rep("window.supLogin('personal',$(authMethod==='phone'?'#acPhone':'#acEmail').value.trim());return}",
    "var _wasPw=authPw; window.supLogin('personal',$(authMethod==='phone'?'#acPhone':'#acEmail').value.trim()); if(me) me.pwSet=_wasPw; return}")

# ---- 安全与访问：登录密码 ----
a = s.find('<li><div><b>修改密码</b>')
b = s.find('</form></li>', a)
if a < 0 or b < 0 or s.count('<li><div><b>修改密码</b>') != 1: sys.exit('[停止] 找不到「修改密码」这一行')
s = s[:a] + '''<li><div><b>登录密码</b><p id="csPwD">还没有设置。设置后可以用手机号或邮箱加密码登录，验证码登录照常可用。</p><span class="cs-st" id="csPwSt">未设置</span></div><button class="btn gray sm" type="button" id="csPwB" data-sx aria-controls="csPwF" aria-expanded="false">设置密码</button>
            <form class="cs-sx" id="csPwF" hidden novalidate>
              <div class="cs-f" id="csPwCurF"><label for="csPw0">当前密码</label><input class="in" id="csPw0" name="pw0" type="password" autocomplete="current-password"><p class="cs-help"><button class="ac-inl" type="button" id="csPwFg">忘了当前密码？用验证码验证</button></p></div>
              <div class="cs-f" id="csPwCodeF" hidden><label for="csPwC">验证码</label><div class="ac-code"><input class="in" id="csPwC" name="code" inputmode="numeric" autocomplete="one-time-code" placeholder="请输入验证码" maxlength="6" disabled><button class="ac-send" id="csPwSend" type="button">获取验证码</button></div><p class="cs-help"><span>验证码发送到</span> <span class="mono" id="csPwTo"></span></p></div>
              <div class="cs-f"><label for="csPw1">新密码</label><input class="in" id="csPw1" name="pw1" type="password" autocomplete="new-password"><p class="cs-help">至少 8 位，同时包含字母和数字，不能包含手机号。</p></div>
              <div class="cs-f"><label for="csPw2">确认新密码</label><input class="in" id="csPw2" name="pw2" type="password" autocomplete="new-password"></div>
              <p class="ac-msg" id="csPwMsg" role="alert"></p>
              <div class="cs-acts"><button class="btn black sm" type="submit" id="csPwOk">保存密码</button><button class="btn gray sm" type="button" data-sx-close>取消</button></div>
            </form></li>''' + s[b + len('</form></li>'):]

rep("""  $('#csPwF').addEventListener('submit',function(e){e.preventDefault();var f=this;
    if(!f.pw0.value) return accountError(f,f.pw0,'请输入当前密码。');
    if(f.pw1.value.length<8) return accountError(f,f.pw1,'新密码至少 8 位。');
    if(f.pw1.value!==f.pw2.value) return accountError(f,f.pw2,'两次输入的新密码不一致。');
    sxClose(f);toast('修改密码接入后即可使用。')});""",
    """  /* 登录密码（2026-10-28）：登录即注册的账户默认没有密码。未设置 → 用验证码验证后设置；已设置 → 用当前密码修改，忘了可改用验证码 */
  var pwByCode=false;
  function pwMask(){if(me.phone)return me.phone.replace(/^(\\d{3})\\d{4}(\\d{4})$/,'$1****$2');var m=me.email||'',i=m.indexOf('@');return i>0?m.charAt(0)+'***'+m.slice(i):m}
  function pwMode(code){var f=$('#csPwF');pwByCode=code;$('#csPwCurF').hidden=code;$('#csPwCodeF').hidden=!code;f.pw0.disabled=code;f.code.disabled=!code;$('#csPwTo').textContent=pwMask();clearAccountError(f)}
  function pwRow(){var on=!!me.pwSet,st=$('#csPwSt');$('#csPwD').textContent=on?'已设置。建议定期更换，不要与其他网站共用。':'还没有设置。设置后可以用手机号或邮箱加密码登录，验证码登录照常可用。';st.textContent=on?'已设置':'未设置';st.className='cs-st'+(on?' ok':'');$('#csPwB').textContent=on?'修改':'设置密码';$('#csPwOk').textContent=on?'保存新密码':'保存密码';pwMode(!on)}
  $('#csPwB').addEventListener('click',function(){if($('#csPwF').hidden)return;pwMode(!me.pwSet);(pwByCode?$('#csPwC'):$('#csPw0')).focus()});
  $('#csPwFg').addEventListener('click',function(){pwMode(true);$('#csPwC').focus()});
  $('#csPwSend').addEventListener('click',function(){if(window.supCountdown){window.supCountdown(this);if(window.supProtoTip)window.supProtoTip();return}toast('验证码服务接入后即可使用。')});
  $('#csPwF').addEventListener('submit',function(e){e.preventDefault();var f=this,pw=f.pw1.value,was=!!me.pwSet;
    if(pwByCode){if(!/^\\d{6}$/.test(f.code.value.trim())) return accountError(f,f.code,'请输入 6 位验证码。')}
    else if(!f.pw0.value) return accountError(f,f.pw0,'请输入当前密码。');
    if(pw.length<8||!/[A-Za-z]/.test(pw)||!/\\d/.test(pw)) return accountError(f,f.pw1,'新密码至少 8 位，并同时包含字母和数字。');
    if(me.phone&&pw.indexOf(me.phone)>=0) return accountError(f,f.pw1,'新密码不能包含手机号。');
    if(pw!==f.pw2.value) return accountError(f,f.pw2,'两次输入的新密码不一致。');
    me.pwSet=true;persist();sxClose(f);pwRow();toast(was?'密码已修改。':'密码已设置，下次可以用密码登录。')});""")
rep('function renderConsole(){ if(!me) return;', 'function renderConsole(){ if(!me) return; pwRow();')

# ---- 英文 ----
EN = {
    '用验证码注册的账户默认没有密码，登录后可在「安全与访问」设置。': 'Accounts created with a verification code have no password until you set one in Security & access.',
    '忘了或没设置过密码？用验证码登录': 'Forgot or never set a password? Sign in with a code',
    '新用户请用验证码登录，验证后自动创建个人账户。': 'New here? Sign in with a code. Your personal account is created after verification.',
    '登录密码': 'Password',
    '还没有设置。设置后可以用手机号或邮箱加密码登录，验证码登录照常可用。': 'Not set yet. Once set, you can sign in with your phone or email and password. Code sign-in keeps working.',
    '已设置。建议定期更换，不要与其他网站共用。': 'Set. Change it from time to time and don’t reuse it on other sites.',
    '未设置': 'Not set', '已设置': 'Set', '设置密码': 'Set password', '保存密码': 'Save password', '保存新密码': 'Save new password',
    '忘了当前密码？用验证码验证': 'Forgot your current password? Verify with a code instead',
    '验证码发送到': 'Code goes to',
    '至少 8 位，同时包含字母和数字，不能包含手机号。': 'At least 8 characters, with both letters and numbers. Must not contain your phone number.',
    '新密码至少 8 位，并同时包含字母和数字。': 'Use at least 8 characters, with both letters and numbers.',
    '新密码不能包含手机号。': 'The new password must not contain your phone number.',
    '请输入 6 位验证码。': 'Enter the 6-digit code.',
    '密码已修改。': 'Password changed.',
    '密码已设置，下次可以用密码登录。': 'Password set. You can sign in with it next time.',
    '验证码服务接入后即可使用。': 'Verification codes will work once the service is connected.',
}
rep('  syncAuthLocale(); applyLang();', '  (function(S){for(var k in S) if(!(k in I18N)) I18N[k]=S[k]})(' + json.dumps(EN, ensure_ascii=False) + ');  /* 登录密码设置 */\n  syncAuthLocale(); applyLang();')

p.write_text(s, encoding='utf8')
print('done')
