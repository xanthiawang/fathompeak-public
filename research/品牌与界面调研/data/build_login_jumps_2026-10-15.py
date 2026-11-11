"""登录页直接跳到对应后台（Zixin 2026-10-15："我只需要现在的跳转能顺利连接就行"）。叠在线上 e458800 上。
不接真实接口，不验证身份；只把「登录」按钮接到对应的后台：
 · 个人登录（手机号 / 邮箱 + 任意 6 位验证码）、微信 / Google / GitHub → 个人后台；
 · 企业登录（工作邮箱 + 任意 6 位验证码或任意密码）→ 企业管理员后台；
   如果这个邮箱在管理员的「成员」页里被加成「成员」，就进企业成员后台（和真实规则一样：角色由账号决定，不让用户选）；
   成员名单记在本机浏览器（localStorage: fp-proto-members），管理员再登录时成员页还在；
 · 员工登录（工作邮箱 + 任意密码 + 任意 6 位两步验证码）→ 超管后台。
「获取验证码」只倒计时、不发短信，点了会提示「原型阶段不发送验证码，输入任意 6 位数字即可」。
后台左上角显示登录时填的手机号或邮箱。退出登录回到登录页。
另：后台和登录页里的「文档 / 查看接入文档」链接改到 #api（AI 模型接口），之前还指向旧的 #docs 快速开始。
用法：python3 -I build_login_jumps_2026-10-15.py <线上 index.html（e458800 或之后，含 5c45ca4 密码登录）> <输出 html>
"""
import json, sys

SRC, OUT = sys.argv[1], sys.argv[2]
s = open(SRC, encoding='utf8').read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: sys.exit(f'[停止] 匹配 {c} 次（应为 {n}）：{old[:80]}')
    s = s.replace(old, new)


# 进入后台：带上登录时填的手机号 / 邮箱；员工登录进超管（root）
rep("""    var T={personal:['personal',''],admin:['company','admin'],member:['company','member'],super:['super','super']};
    function enter(k){var t=T[k]; me={email:'',type:t[0],role:t[1],since:today(),keys:[],subs:[],edu:'none',preview:true}; logged=true; syncLogin(); location.hash='#console'}
    var LIVE=true; if(!LIVE) window.supLogin=enter;""",
    """    var T={personal:['personal','personal',''],admin:['company','admin','企业账户'],member:['company','member','企业账户'],super:['personal','root','沐仞运营']};
    /* 原型：登录不验证身份，直接进对应后台（2026-10-15）。企业成员名单记在本机浏览器，管理员加的「成员」邮箱登录后进成员后台 */
    var PK='fp-proto-members';
    function pget(){try{return JSON.parse(localStorage.getItem(PK)||'{}')||{}}catch(e){return {}}}
    function enter(k,id){var t=T[k], ph=/^1\\d{10}$/.test(id||''), all=pget();
      me={email:ph?'':(id||''),phone:ph?id:'',type:t[0],role:t[1],org:t[2],since:today(),keys:[],subs:[],edu:'none',preview:true,proto:true};
      if(k==='admin') me.subs=Object.keys(all).filter(function(e){return e!==id}).map(function(e){return {email:e,at:all[e].at||today(),role:all[e].r,joined:!!all[e].j}});
      if(k==='member'&&all[id]){all[id].j=1; try{localStorage.setItem(PK,JSON.stringify(all))}catch(e){}}  /* 成员第一次登录：管理员那边显示「已加入」 */
      logged=true; syncLogin(); location.hash='#console'}
    function orgRole(em){var r=pget()[em]; return r&&r.r==='member'?'member':'admin'}
    function psync(){if(me&&me.proto&&me.role==='admin'){var all={}; (me.subs||[]).forEach(function(x){all[x.email]={r:x.role==='admin'?'admin':'member',at:x.at||today(),j:x.joined?1:0}}); try{localStorage.setItem(PK,JSON.stringify(all))}catch(e){}}}
    var _rcp=renderConsole; renderConsole=function(){_rcp(); psync()}; var _psp=persist; persist=function(){_psp(); psync()};  /* 加成员、改角色、移除后都记下来 */
    function protoTip(){toast('原型阶段不发送验证码，输入任意 6 位数字即可。')}
    var LIVE=false; if(!LIVE) window.supLogin=enter;""")
# 成员页：登录过的成员显示「已加入」
rep("""<td><span class="cs-st wait">待加入</span></td>""", """<td>'+(x.joined?'<span class="cs-st ok">已加入</span>':'<span class="cs-st wait">待加入</span>')+'</td>""")
rep("$('#csMemP').textContent=subs.length;", "$('#csMemP').textContent=subs.filter(function(x){return !x.joined}).length;")
# 个人登录：把手机号 / 邮箱带进后台
rep("if(window.supLogin){window.supLogin('personal');return}",
    "if(window.supLogin){var _pw=$('#acPw'); if(_pw) _pw.value=''; window.supLogin('personal',$(authMethod==='phone'?'#acPhone':'#acEmail').value.trim());return}")  # 5c45ca4 起个人登录也可以用密码，进后台前清掉密码框
rep("if(window.supCountdown){window.supCountdown(this);return}authUnavailable(authMethod)});",
    "if(window.supCountdown){window.supCountdown(this);if(window.supProtoTip)window.supProtoTip();return}authUnavailable(authMethod)});")
# 企业登录：按成员名单决定进管理员还是成员后台
rep("$('#acOrgPw').value=''; if(LIVE){svc('企业登录尚未开通。如需开通企业账户，请联系我们。');return} enter('admin')});",
    "$('#acOrgPw').value=''; if(LIVE){svc('企业登录尚未开通。如需开通企业账户，请联系我们。');return} var em=$('#acOrgU').value.trim().toLowerCase(); enter(orgRole(em),em)});")
rep("if(LIVE){svc('企业登录尚未开通。如需开通企业账户，请联系我们。');return} if(window.supCountdown) window.supCountdown(this)});",
    "if(LIVE){svc('企业登录尚未开通。如需开通企业账户，请联系我们。');return} if(window.supCountdown){window.supCountdown(this); protoTip()}});")
rep("$('#adPw').value=''; $('#adOtp').value=''; if(LIVE){m.textContent='运营后台尚未接入。员工账号由开发开通。';return} enter('super')});",
    "var am=$('#adMail').value.trim().toLowerCase(); $('#adPw').value=''; $('#adOtp').value=''; if(LIVE){m.textContent='运营后台尚未接入。员工账号由开发开通。';return} enter('super',am)});\n    window.supProtoTip=protoTip;")
# 第三方登录（原型）：进个人后台前也要先勾选协议（微信）
rep("if(!LIVE) $$('[data-provider]').forEach(function(b){b.addEventListener('click',function(e){e.stopImmediatePropagation(); enter('personal')},true)});",
    "if(!LIVE) $$('[data-provider]').forEach(function(b){b.addEventListener('click',function(e){e.stopImmediatePropagation(); if(b.dataset.provider==='wechat'&&!$('#acAgree').checked){toast('请先阅读并同意用户服务协议和隐私政策。');return} enter('personal')},true)});")
# 后台里的「文档 / 查看接入文档」都打开扒下来的「AI 模型接口」（#api），和顶部导航一致（Zixin 2026-10-15："后台跳转后的文档没有更新？？"）
# 不改：导入客户端对话框（#csImpDoc，专门打开「接入客户端」那一节）和 #api 左栏「开始」组（data-doc-open，打开各指南）
import re
s, n = re.subn(r'href="#docs"(?! id="csImpDoc")(?! data-doc-open)', 'href="#api"', s)
if n != 8: sys.exit(f'[停止] 文档链接改了 {n} 处（应为 8：登录页 1、侧栏底部 1、概览空状态 2、开始使用 1、问答 1、学习卡 1、使用日志空状态 1）')
EN = {'原型阶段不发送验证码，输入任意 6 位数字即可。': 'Prototype: no code is sent. Enter any 6 digits.'}
rep('  syncAuthLocale(); applyLang();', '  (function(S){for(var k in S) if(!(k in I18N)) I18N[k]=S[k]})(' + json.dumps(EN, ensure_ascii=False) + ');  /* 原型登录提示 */\n  syncAuthLocale(); applyLang();')
open(OUT, 'w', encoding='utf8').write(s)
print('done:', OUT)
