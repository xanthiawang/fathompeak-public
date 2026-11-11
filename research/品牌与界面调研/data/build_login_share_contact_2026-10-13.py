"""登录直达正式平台 + 分享卡片 + 咨询浮窗。
1) 站内演示的 #start / #login / #console 不再展示：链接与路由直接跳转正式平台
   （注册 account.fathompeak.cn/sign-up，登录 admin.fathompeak.cn/login）。首屏 HTML 不改，只在脚本里改写链接。
2) 分享：meta description、Open Graph / Twitter 卡片、站点图标（art/share/）；正文最前放一张隐藏的 512 图供微信兜底抓图。
3) 右下角"咨询"浮窗：企业采购表单、电站合作表单、商务邮箱；二维码由 SOCIAL 配置驱动，为空时不显示（不放占位）。
在 build_forms_i18n 之后运行，只改本地副本 index.html。
用法：python3 -I build_login_share_contact_2026-10-13.py <仓库副本目录>
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

SITE = 'https://xanthiawang.github.io/fathompeak-site/'
DESC = '主流模型 × 异构算力，一站式大模型 API 平台。一体机部署在电站旁，用富余绿电生产词元，为 AI 企业提供低成本、可追溯的推理服务。'

# ---------- 1. 分享卡片与图标 ----------
rep('<meta name="viewport" content="width=device-width,initial-scale=1">\n<title>沐仞 FathomPeak</title>',
    '<meta name="viewport" content="width=device-width,initial-scale=1">\n<title>沐仞 FathomPeak</title>\n'
    f'<meta name="description" content="{DESC}">\n'
    '<meta property="og:type" content="website">\n<meta property="og:site_name" content="沐仞 FathomPeak">\n'
    '<meta property="og:title" content="沐仞 FathomPeak · 一站式大模型 API 平台">\n'
    f'<meta property="og:description" content="{DESC}">\n'
    f'<meta property="og:url" content="{SITE}">\n<meta property="og:image" content="{SITE}art/share/og-1200x630.png">\n'
    '<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
    '<meta property="og:locale" content="zh_CN">\n<meta name="twitter:card" content="summary_large_image">\n'
    f'<meta name="twitter:image" content="{SITE}art/share/og-1200x630.png">\n'
    '<link rel="icon" href="art/share/favicon.svg" type="image/svg+xml">\n<link rel="icon" href="art/share/icon-192.png" sizes="192x192" type="image/png">\n'
    '<link rel="apple-touch-icon" href="art/share/apple-touch-icon.png">\n<meta name="theme-color" content="#F8F8F8">')
# 微信未接 JS-SDK 时会抓页面里的大图作缩略图，放一张隐藏的品牌图兜底
rep('<div class="hdr">', '<div hidden aria-hidden="true"><img src="art/share/icon-512.png" alt="" width="512" height="512"></div>\n<div class="hdr">')

# ---------- 2. 登录直达正式平台 ----------
rep("function route(){ var h=(location.hash||'#home').slice(1);",
    "var PLATFORM={start:'https://account.fathompeak.cn/sign-up',login:'https://admin.fathompeak.cn/login',console:'https://admin.fathompeak.cn/login'};\n"
    "  $$('a[href=\"#start\"],a[href=\"#login\"],a[href=\"#console\"]').forEach(function(a){a.setAttribute('href',PLATFORM[a.getAttribute('href').slice(1)])});\n"
    "  function route(){ var h=(location.hash||'#home').slice(1); if(PLATFORM[h]){ location.replace(PLATFORM[h]); return }")

# ---------- 3. 咨询浮窗 + 二维码配置 ----------
FAB = '''<div class="fab" id="fab"><button class="fab-b" id="fabBtn" type="button" aria-expanded="false" aria-controls="fabPanel"><svg viewBox="0 0 20 20" width="18" height="18" aria-hidden="true"><path d="M4 4h12a2 2 0 0 1 2 2v7a2 2 0 0 1-2 2H9l-4 3v-3H4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg><span>咨询</span></button>
  <div class="fab-p" id="fabPanel" hidden><b>联系沐仞</b>
    <a href="#enterprise" data-scrollto="enterprise-sales"><span>企业采购与海外服务</span><i>填写需求 →</i></a>
    <a href="#network" data-scrollto="coopForm"><span>电站与节点合作</span><i>提交场站信息 →</i></a>
    <a href="https://account.fathompeak.cn/sign-up"><span>开发者</span><i>注册获取 API Key →</i></a>
    <a href="mailto:fathompeak@163.com"><span>商务邮箱</span><i>fathompeak@163.com</i></a>
    <div class="fab-qr" id="fabQr"></div></div></div>
'''
rep('<div class="toast" id="toast"', FAB + '<div class="toast" id="toast"')
rep('<div><span>公司地址</span>北京市海淀区清河中街 66 号院 1 号楼</div></div></div>',
    '<div><span>公司地址</span>北京市海淀区清河中街 66 号院 1 号楼</div></div><div class="social" id="footSocial"></div></div>')

JS = r"""
  /* ---------- 咨询浮窗与社媒二维码：SOCIAL 为空时只显示链接，不出现二维码位 ---------- */
  var SOCIAL=[]; /* 有官方二维码后按此格式填入，图片放 art/qr/：{k:'公众号',img:'art/qr/wechat-mp.png'}, {k:'企业微信',img:'art/qr/wecom.png'} */
  function qrHTML(){return SOCIAL.map(function(x){return '<figure><img src="'+x.img+'" alt="'+x.k+'二维码" width="96" height="96" loading="lazy"><figcaption>'+x.k+'</figcaption></figure>'}).join('')}
  if(SOCIAL.length){ $('#fabQr').innerHTML=qrHTML(); $('#footSocial').innerHTML=qrHTML() }
  (function(){var b=$('#fabBtn'),p=$('#fabPanel'); function set(o){p.hidden=!o; b.setAttribute('aria-expanded',String(o))}
    b.addEventListener('click',function(e){e.stopPropagation(); set(p.hidden)});
    p.addEventListener('click',function(e){ if(e.target.closest('a')) set(false) });
    document.addEventListener('click',function(e){ if(!p.hidden&&!e.target.closest('#fab')) set(false) });
    document.addEventListener('keydown',function(e){ if(e.key==='Escape') set(false) }) })();
"""
rep("  /* ---------- 功能区：指示条 + 粘性截图 ---------- */", JS + "  /* ---------- 功能区：指示条 + 粘性截图 ---------- */")

CSS = '''
/* 咨询浮窗 */
.fab{position:fixed;right:20px;bottom:20px;z-index:60}
.fab-b{display:inline-flex;align-items:center;gap:8px;height:44px;padding:0 18px;border:0;border-radius:var(--pill);background:var(--ink);color:var(--paper);font:500 14px var(--sans);cursor:pointer;box-shadow:0 10px 30px -10px rgba(0,0,0,.35);transition:background .2s var(--ease)}
.fab-b:hover{background:var(--hover)}
.fab-p{position:absolute;right:0;bottom:56px;width:300px;padding:16px;border-radius:var(--r16);background:var(--card);border:1px solid var(--line);box-shadow:var(--shadow-lg);display:grid;gap:2px}
.fab-p[hidden]{display:none}
.fab-p b{font:500 15px var(--sans);margin:0 0 8px;color:var(--ink)}
.fab-p a{display:flex;justify-content:space-between;gap:10px;padding:10px 0;border-top:1px solid var(--line-2);font-size:13px;color:var(--ink)}
.fab-p a i{font-style:normal;color:var(--ink-50);white-space:nowrap}
.fab-p a:hover i{color:var(--ink)}
.fab-qr:empty,.social:empty{display:none}
.fab-qr,.social{display:flex;gap:12px;flex-wrap:wrap;margin-top:10px}
.fab-qr figure,.social figure{margin:0;text-align:center;font-size:12px;color:var(--ink-50)}
.fab-qr img,.social img{display:block;width:96px;height:96px;border-radius:8px;background:#fff;margin-bottom:4px}
@media (max-width:800px){.fab{right:14px;bottom:14px}.fab-b{height:44px;width:44px;padding:0;justify-content:center}.fab-b span{display:none}.fab-p{width:min(300px,calc(100vw - 28px))}}
'''
k = s.index('</style>')
s = s[:k] + CSS + s[k:]

EN = {"咨询": "Contact", "联系沐仞": "Contact FathomPeak", "企业采购与海外服务": "Enterprise & overseas", "填写需求 →": "Send requirements →",
      "电站与节点合作": "Plant & node partners", "提交场站信息 →": "Submit site details →", "开发者": "Developers",
      "注册获取 API Key →": "Sign up for an API key →", "商务邮箱": "Business email"}
k2 = s.index('var I18N={') + len('var I18N={')
s = s[:k2] + ''.join(json.dumps(x, ensure_ascii=False) + ':' + json.dumps(y, ensure_ascii=False) + ',' for x, y in EN.items()) + s[k2:]

assert s[s.index('<div class="hero">'):s.index('<div class="partners">')] == hero0, '首屏 HTML 被改动'
e = s.index('<div class="cta-end rv">')
assert s[e:s.index('</section>', e)] == end0, '首页结尾 CTA 被改动'
open(P, 'w', encoding='utf8').write(s)
print('done.')
