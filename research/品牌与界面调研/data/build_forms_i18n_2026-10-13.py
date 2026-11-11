"""表单真提交 + 英文模式补全。
1) 联系销售、电站合作、三处周报订阅：按钮改为"提交 / 订阅"，经 FormSubmit 转发到 fathompeak@163.com；
   失败（含 FormSubmit 首次激活前）时显示"改用邮件发送"，链接里带好已填字段。
2) 英文：合并补译词典（翻译 JSON，键与页面中文逐字一致），并给翻译函数加正则规则，覆盖带数字、时间的动态文本。
在 build_models_release_layout 之后运行，只改本地副本 index.html；首屏 HTML 与首页结尾 CTA 逐字不变。
用法：python3 -I build_forms_i18n_2026-10-13.py <仓库副本目录> <译文1.json> [<译文2.json> ...]
"""
import json, os, sys

P = os.path.join(sys.argv[1], 'index.html')
s = open(P, encoding='utf8').read()
hero0 = s[s.index('<div class="hero">'):s.index('<div class="partners">')]
end0 = s[s.index('<div class="cta-end rv">'):s.index('</section>', s.index('<div class="cta-end rv">'))]

def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: sys.exit(f'[停止] 匹配 {c} 次（应为 {n}）：{old[:80]}')
    s = s.replace(old, new)

HP = '<input class="hp" type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true">'
MSG = '<span class="form-msg" role="status" aria-live="polite"></span>'

# ---------- 1. 表单标记 ----------
rep('<form class="form" id="salesForm"><div class="f"><input class="in" placeholder="公司" aria-label="公司"></div><div class="f"><input class="in" placeholder="联系方式" aria-label="联系方式"></div><div class="f"><input class="in" placeholder="预计月用量或任务规模" aria-label="预计月用量或任务规模"></div><div class="f"><input class="in" placeholder="模型、应用场景或海外服务需求" aria-label="模型、应用场景或海外服务需求"></div><button class="btn black" type="submit">查看提交方式</button><span class="fine">表单仅展示需求字段，不会提交信息。请将需求发送至 fathompeak@163.com。</span></form>',
    '<form class="form" id="salesForm" data-lead="联系销售" data-ok="已收到，商务会通过你留下的联系方式联系你。">'
    '<div class="f"><input class="in" name="公司" required placeholder="公司" aria-label="公司"></div>'
    '<div class="f"><input class="in" name="联系方式" required placeholder="联系方式（手机 / 邮箱 / 微信）" aria-label="联系方式"></div>'
    '<div class="f"><input class="in" name="预计用量" placeholder="预计月用量或任务规模" aria-label="预计月用量或任务规模"></div>'
    '<div class="f"><input class="in" name="需求" placeholder="模型、应用场景或海外服务需求" aria-label="模型、应用场景或海外服务需求"></div>'
    + HP + '<button class="btn black" type="submit">提交</button>' + MSG +
    '<span class="fine">提交后发送至沐仞商务邮箱 fathompeak@163.com，仅用于联系你。</span></form>')

rep('<form class="form" id="coopForm"><div class="f"><input class="in" placeholder="电站名称 / 公司" id="cName" aria-label="电站名称 / 公司"></div><div class="f"><input class="in" placeholder="能源类型、装机容量与场地条件" id="cType" aria-label="能源类型、装机容量与场地条件"></div><div class="f"><input class="in" placeholder="联系方式" id="cContact" aria-label="联系方式"></div><div class="f"><button class="btn black" type="submit">查看提交方式</button></div><div class="done">本页未提交信息。请将场站资料发送至 fathompeak@163.com。</div></form>',
    '<form class="form" id="coopForm" data-lead="电站合作" data-ok="已收到，商务会通过你留下的联系方式联系你。">'
    '<div class="f"><input class="in" name="电站名称或公司" required placeholder="电站名称 / 公司" id="cName" aria-label="电站名称 / 公司"></div>'
    '<div class="f"><input class="in" name="能源类型与装机" placeholder="能源类型、装机容量与场地条件" id="cType" aria-label="能源类型、装机容量与场地条件"></div>'
    '<div class="f"><input class="in" name="所在地" placeholder="所在省市" aria-label="所在省市"></div>'
    '<div class="f"><input class="in" name="联系方式" required placeholder="联系方式（手机 / 邮箱 / 微信）" id="cContact" aria-label="联系方式"></div>'
    + HP + '<div class="f"><button class="btn black" type="submit">提交</button></div>' + MSG +
    '<span class="fine">提交后发送至沐仞商务邮箱 fathompeak@163.com，仅用于联系你。</span></form>')

NLF = ('<form data-lead="周报订阅" data-ok="订阅成功。"><input class="in" type="email" name="邮箱" placeholder="电子邮箱" required aria-label="电子邮箱">'
       + HP + '<button class="btn black" type="submit">订阅</button></form>' + MSG)
rep('<form><input class="in" type="email" placeholder="电子邮箱" required aria-label="电子邮箱"><button class="btn black" type="submit">订阅</button></form><span class="ok">请发邮件至 fathompeak@163.com 订阅周报。</span>', NLF, 3)
rep('<p>发邮件至 fathompeak@163.com 订阅；往期内容见新闻页。</p>', '<p>填写邮箱即可订阅；往期内容见新闻页。</p>')
rep('<form class="newsf" id="newsFoot"><input class="in" type="email" placeholder="邮箱" aria-label="邮箱"><button class="btn black" type="submit">订阅</button></form>',
    '<form class="newsf" id="newsFoot" data-lead="周报订阅" data-ok="订阅成功。"><input class="in" type="email" name="邮箱" required placeholder="邮箱" aria-label="邮箱">'
    + HP + '<button class="btn black" type="submit">订阅</button></form>' + MSG)

# ---------- 2. 表单脚本 ----------
rep("$('#salesForm').addEventListener('submit',function(e){e.preventDefault();toast('请将需求发送至 fathompeak@163.com。')});", '')
rep("$('#coopForm').addEventListener('submit',function(e){e.preventDefault();toast('请将场站信息发送至 fathompeak@163.com。')});", '')
rep("$$('.news form').forEach(function(f){f.addEventListener('submit',function(e){e.preventDefault();toast('请发邮件至 fathompeak@163.com 订阅周报。')})});", '')
rep("$('#newsFoot').addEventListener('submit',function(e){e.preventDefault();toast('请发邮件至 fathompeak@163.com 订阅周报。')});",
    r"""/* ---------- 表单：经 FormSubmit 转发到商务邮箱；没发出去时给出带好字段的邮件链接 ---------- */
  var LEAD_TO='fathompeak@163.com', LEAD_URL='https://formsubmit.co/ajax/'+LEAD_TO;
  function leadMsgEl(f){var m=f.querySelector('.form-msg');if(!m&&f.nextElementSibling&&f.nextElementSibling.classList.contains('form-msg'))m=f.nextElementSibling;return m}
  function sendLead(f){
    if(f.__busy) return; var hp=f.querySelector('[name=_honey]'); if(hp&&hp.value) return;
    var kind=f.getAttribute('data-lead'), data={}, lines=[];
    Array.prototype.forEach.call(f.querySelectorAll('[name]'),function(el){if(el.name==='_honey')return;var v=el.value.trim();data[el.name]=v;if(v)lines.push(el.name+'：'+v)});
    var first=data[Object.keys(data)[0]]||'';
    var payload={_subject:'官网 · '+kind+(first?' · '+first:''),_template:'table',_captcha:'false','表单':kind,'页面':location.href,'语言':lang==='en'?'English':'中文'};
    Object.keys(data).forEach(function(k){payload[k]=data[k]});
    var mail='mailto:'+LEAD_TO+'?subject='+encodeURIComponent('官网 · '+kind)+'&body='+encodeURIComponent(lines.join('\n'));
    var btn=f.querySelector('button[type=submit]'), label=btn.textContent, m=leadMsgEl(f);
    f.__busy=1; btn.disabled=true; if(m){m.className='form-msg';m.textContent='提交中…'}
    function done(ok){ f.__busy=0; btn.disabled=false; btn.textContent=label; if(!m) return;
      if(ok){ f.reset(); m.className='form-msg ok'; m.textContent=f.getAttribute('data-ok') }
      else { m.className='form-msg err'; m.innerHTML='<span>没有发送成功。</span> <a class="ul" href="'+mail+'">改用邮件发送 →</a>' } }
    fetch(LEAD_URL,{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},body:JSON.stringify(payload)})
      .then(function(r){return r.json()}).then(function(j){done(!!j&&String(j.success)==='true')}).catch(function(){done(false)});
  }
  $$('form[data-lead]').forEach(function(f){f.addEventListener('submit',function(e){e.preventDefault();sendLead(f)})});""")

CSS = '''
/* 表单提交反馈 */
.hp{position:absolute!important;left:-9999px!important;width:1px;height:1px;opacity:0}
.form-msg{display:block;min-height:0;font-size:13px;line-height:1.6;color:var(--ink-70);margin-top:8px}
.form-msg:empty{display:none}
.form-msg.ok{color:var(--peak)}
.form-msg.err{color:var(--ink)}
.btn[disabled]{opacity:.55;cursor:default}
'''
k = s.index('</style>')
s = s[:k] + CSS + s[k:]

# ---------- 3. 翻译函数加正则规则（动态文本：电站 → 模型、价格、窗口倒计时、期号） ----------
# 2026-10-13 晚另一会话已把 tx() 改成 tr1/trk（字典 + 按「 · 」「 → 」拆段）；正则规则接在 trk 查不到之后
rep("function trk(k){ var r=tr1(k); if(r!=null) return r;", "function trk(k){ var r=tr1(k); if(r!=null) return r; r=rxTr(k); if(r!=null) return r;")
rep("  function tr1(k){", r"""  function trKey(k){ return trk(k) }
  var RX=[
    [/^(.+?) → (.+)$/, function(m,a,b){var x=trKey(a); return x==null?null:x+' → '+b}],
    [/^(.+?) · 沐仞$/, function(m,a){return a+' · FathomPeak'}],
    [/^(.+?) · 输出参考价$/, function(m,a){return a+' · reference output price'}],
    [/^(.+?) · 对话$/, function(m,a){return a+' · Chat'}],
    [/^(.+?) · 推理$/, function(m,a){return a+' · Reasoning'}],
    [/^¥([\d.]+) \/ 百万词元$/, function(m,a){return '¥'+a+' / M tokens'}],
    [/^上下文 (.+)$/, function(m,a){return 'Context '+a}],
    [/^平价窗口 (.+) · 还有 (\d+)h (\d+)m$/, function(m,a,b,c){return 'Off-peak window '+a+' · '+b+'h '+c+'m left'}],
    [/^下一个窗口 (.+) · (\d+)h (\d+)m 后开始$/, function(m,a,b,c){return 'Next window '+a+' · starts in '+b+'h '+c+'m'}],
    [/^第 (\d+) 期 · (.+)$/, function(m,a,b){return 'Issue '+a+' · '+b}],
    [/^展示估算 ¥([\d.,]+)$/, function(m,a){return 'Estimate ¥'+a}],
    [/^减排展示 (.+)$/, function(m,a){return 'Emissions avoided '+a}]
  ];
  function rxTr(k){ for(var i=0;i<RX.length;i++){ var m=k.match(RX[i][0]); if(m){ var r=RX[i][1].apply(null,m); if(r!=null) return r } } return null }
  function tr1(k){""")

# placeholder / aria-label / title / data-toast 也走词典
rep("$$('[placeholder]').forEach(function(el){ var src=el.__zh!=null?el.__zh:el.getAttribute('placeholder'); if(lang==='zh'){ if(el.__zh!=null){el.setAttribute('placeholder',el.__zh); el.__zh=null} return } var k=src.trim(); if(I18N[k]!=null){ el.__zh=src; el.setAttribute('placeholder',I18N[k]) } });",
    "['placeholder','aria-label','title','data-toast','data-ok'].forEach(function(at){ $$('['+at+']').forEach(function(el){ var key='__zh_'+at, src=el[key]!=null?el[key]:el.getAttribute(at); if(!src) return; if(lang==='zh'){ if(el[key]!=null){el.setAttribute(at,el[key]); el[key]=null} return } if(!CJK.test(src)) return; var k=src.trim(), t=trKey(k); if(t==null) t=rxTr(k); if(t!=null){ el[key]=src; el.setAttribute(at,t) } }) });")

# ---------- 3b. 断链：电站页"了解设备与部署"指向不存在的指南；英文模式下标签页标题也翻译 ----------
rep('href="#guide-plant-video"', 'href="#guide-plant-machine"')
rep("[name]||'沐仞';", "[name]||'沐仞'; document.__zt=null; titleLang();")
rep("function setLang(l){ lang=l; try{localStorage.setItem('fp-lang',l)}catch(e){} applyLang() }",
    "function titleLang(){ var z=document.__zt||document.title; if(lang==='en'){ var t=trKey(z); if(t==null) t=rxTr(z); if(t!=null){ document.__zt=z; document.title=t } } else if(document.__zt){ document.title=document.__zt; document.__zt=null } }\n  function setLang(l){ lang=l; try{localStorage.setItem('fp-lang',l)}catch(e){} applyLang(); titleLang() }")

rep('按合同分享收益。写信给商务，我们会联系你。</p>', '按合同分享收益。填写右侧表单，商务会联系你。</p>')

# ---------- 4. 合并补译词典 ----------
EN = {
    "提交": "Submit", "订阅": "Subscribe", "提交中…": "Sending…", "联系方式（手机 / 邮箱 / 微信）": "Contact (phone / email / WeChat)",
    "所在省市": "Province / city", "电子邮箱": "Email", "邮箱": "Email", "订阅成功。": "You're subscribed.",
    "已收到，商务会通过你留下的联系方式联系你。": "Received. Our team will reach you at the contact you left.",
    "没有发送成功。": "It didn't go through.", "改用邮件发送 →": "Send by email instead →",
    "提交后发送至沐仞商务邮箱 fathompeak@163.com，仅用于联系你。": "Submissions go to fathompeak@163.com and are only used to contact you.",
    "填写邮箱即可订阅；往期内容见新闻页。": "Enter your email to subscribe; past issues are on the news page.",
    "/ 百万词元 · 输出参考价": "/ M tokens · reference output price",
    "光伏、风电、水电场站及既有算力中心都可以接入。资产方出资采购一体机部署在场站，沐仞负责接入、调度、运营与词元销售，按合同分享收益。填写右侧表单，商务会联系你。": "Solar, wind and hydro plant sites, as well as existing computing centers, can all connect. Asset owners fund the appliances deployed at the site; FathomPeak handles onboarding, scheduling, operations and token sales, and revenue is shared per the contract. Fill in the form and our team will get in touch.",
}
for path in sys.argv[2:]:
    for zh, en in json.load(open(path, encoding='utf8')).items():
        if isinstance(en, str) and en.strip():
            EN.setdefault(zh.strip(), en)  # 不去空格：链接前后的片段要保留空格
k2 = s.index('var I18N={') + len('var I18N={')
s = s[:k2] + ''.join(json.dumps(x, ensure_ascii=False) + ':' + json.dumps(y, ensure_ascii=False) + ',' for x, y in EN.items()) + s[k2:]

assert s[s.index('<div class="hero">'):s.index('<div class="partners">')] == hero0, '首屏 HTML 被改动'
e = s.index('<div class="cta-end rv">')
assert s[e:s.index('</section>', e)] == end0, '首页结尾 CTA 被改动'
open(P, 'w', encoding='utf8').write(s)
print('done.', len(EN), 'EN entries')
