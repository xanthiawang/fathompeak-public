"""文档入口、渐变配色、表单门槛（Zixin 2026-10-14 夜）。叠在 build_login_accounts 的输出上。
 1 文档："文档这一页我不是让你去扒我们原始网站的文档信息了吗，为啥没更新？" ——内容 10-14 已从 admin.fathompeak.cn 的文档
   （AI模型接口，10 组 32 个接口）扒下来（253127e），但放在单独的「接口参考」页 #api，导航「文档」仍打开旧的手写「快速开始」。
   改：导航、手机菜单、页脚的「文档」都打开这份文档；页面标题沿用原网站的「AI 模型接口」；左栏顶部加「开始」组
   （快速开始 / 接入客户端 / 鉴权与 Key / 模型与计费 / 错误码 / 延迟与服务等级），点了打开原来的指南页。
 2 配色："这个蓝色不好看，用渐变，参考 Dia" ——全站扫出的平涂浅蓝（定价页「计算方式」、费用估算结果、首页怎么用的两块示意窗、
   产品页的强调标签）改成晨昏渐变（晨蓝 → 淡紫 → 暖米）。登录页插画底色被插画盖住，不改。
 3 表单门槛："不要给人注册设置这么多门槛，检查其他部分一样" ——电站合作表单把「能源类型与装机」「所在地」并成一栏选填。
   （联系销售表单在 build_login_accounts 里已删「预计月用量」、工作邮箱改为勾选申请开户后才出现。）
用法：python3 -I build_docs_gradient_forms_2026-10-14.py <输入 html> <输出 html>
"""
import json, sys

SRC, OUT = sys.argv[1], sys.argv[2]
s = open(SRC, encoding='utf8').read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: sys.exit(f'[停止] 匹配 {c} 次（应为 {n}）：{old[:80]}')
    s = s.replace(old, new)


# ---------- 1 文档 ----------
rep('<a href="#docs" data-nav="docs">文档</a>', '<a href="#api" data-nav="docs">文档</a>', 2)
rep('<a href="#docs">文档</a>', '<a href="#api">文档</a>')
rep("api:'接口参考 - 沐仞科技 FathomPeak',", "api:'文档 - 沐仞科技 FathomPeak',")
GUIDES = [('quick', '快速开始'), ('clients', '接入客户端'), ('auth', '鉴权与 Key'), ('models', '模型与计费'), ('errors', '错误码'), ('sla', '延迟与服务等级')]
rep("""    var nav='<a class="ap-back" href="#docs">← '+apL('文档')+'</a><button class="ap-nb on" type="button" data-ap="ap-top">'+apL('接入地址与鉴权')+'</button>'+""",
    """    var nav='<div class="y">'+apL('开始')+'</div>'+""" + json.dumps(GUIDES, ensure_ascii=False) + """.map(function(g){return '<a class="ap-nb ap-guide" href="#docs" data-doc-open="'+g[0]+'"><span>'+apL(g[1])+'</span></a>'}).join('')+
      '<div class="y">'+apL('接口')+'</div><button class="ap-nb on" type="button" data-ap="ap-top">'+apL('接入地址与鉴权')+'</button>'+""")
rep("""'<header class="ap-top" id="ap-top"><span class="k">'+apL('接口参考')+' · '+(lang==='en'?AP.groups.length+' groups · '+n+' endpoints':AP.groups.length+' 组 · '+n+' 个接口')+'</span><h1>'+apL('接口参考')+'</h1>'+""",
    """'<header class="ap-top" id="ap-top"><span class="k">'+apL('文档')+' · '+(lang==='en'?AP.groups.length+' groups · '+n+' endpoints':AP.groups.length+' 组 · '+n+' 个接口')+'</span><h1>'+apL('AI 模型接口')+'</h1>'+""")
# 手机上左栏隐藏、用下拉框跳转：下拉框里也加「开始」组
rep("""    var jump='<select class="in ap-jump" aria-label="'+apL('跳到接口')+'"><option value="ap-top">'+apL('接入地址与鉴权')+'</option>'+""",
    """    var jump='<select class="in ap-jump" aria-label="'+apL('跳到接口')+'"><optgroup label="'+apL('开始')+'">'+""" + json.dumps(GUIDES, ensure_ascii=False) + """.map(function(g){return '<option value="doc:'+g[0]+'">'+apL(g[1])+'</option>'}).join('')+'</optgroup><option value="ap-top" selected>'+apL('接入地址与鉴权')+'</option>'+""")
# 左栏目录和手机下拉不显示请求方式（GET / POST）：几乎全是 POST，在目录里只是噪音；接口详情里路径前照常显示（Zixin：「post？？这个存在的意义？」）
rep("""<button class="ap-nb" type="button" data-ap="'+o.id+'"><span class="ap-nm '+o.m.toLowerCase()+'">'+o.m+'</span><span>""", """<button class="ap-nb" type="button" data-ap="'+o.id+'"><span>""")
rep("""'<option value="'+o.id+'">'+o.m+' · '+""", """'<option value="'+o.id+'">'+""")
# 文档页左栏的「接口参考 →」改名，和导航一致
rep('<a class="ap-idx" href="#api">接口参考 →</a>', '<a class="ap-idx" href="#api">AI 模型接口 →</a>')

# ---------- 3 电站合作表单：两栏并一栏选填 ----------
rep('<div class="f"><input class="in" name="能源类型与装机" placeholder="能源类型、装机容量与场地条件" id="cType" aria-label="能源类型、装机容量与场地条件"></div><div class="f"><input class="in" name="所在地" placeholder="所在省市" aria-label="所在省市"></div>',
    '<div class="f"><input class="in" name="场站情况" placeholder="场站情况（可不填）：能源类型、装机、所在省市" id="cType" aria-label="场站情况（可不填）"></div>')

# 联系销售的说明不再提「预期用量」（那一栏已删）
rep('说明业务场景、模型与预期用量，便于安排需求评估。', '留下公司和联系方式，商务会联系你。要开通企业账户，可以一起申请。', 3)  # 页面 1 处 + 英文词条 2 处（英文在下面强制覆盖）

# ---------- 2 渐变 ----------
CSS = '''
<style id="gradient-fix-css">
/* 平涂浅蓝改晨昏渐变（2026-10-14 夜；Zixin："这个蓝色不好看，用渐变，参考 Dia"） */
:root{--wash-soft:linear-gradient(120deg,#E3ECF8 0%,#ECE6F1 52%,#F6E9E2 100%)}
body .pr-eq,body .pc-out{background:var(--wash-soft);border:1px solid rgba(61,49,79,.08)}
#home2 .sw.mist{background:linear-gradient(135deg,#D3DEEE 0%,#E0D9E8 55%,#EDDFD6 100%)}
#home2 .sw.mist .sw-in{background:linear-gradient(160deg,#EAF0F9 0%,#F0EBF3 60%,#F7EEE8 100%)}
body .tg.acc{background:var(--wash-soft);color:var(--ink)}
/* 文档左栏「开始」组：指南链接与接口按钮同一种样式 */
.ap-nav a.ap-guide{text-decoration:none}
</style>
'''
k = s.rindex('</head>'); s = s[:k] + CSS + s[k:]

JS = r'''
  /* ======== 文档左栏「开始」：打开原来的指南页并切到对应一节（2026-10-14 夜） ======== */
  document.addEventListener('change',function(e){var t=e.target; if(!t.classList||!t.classList.contains('ap-jump')||t.value.indexOf('doc:')!==0) return; var k=t.value.slice(4); t.value='ap-top'; location.hash='#docs'; setTimeout(function(){var b=$('#docIdx [data-doc="'+k+'"]'); if(b) b.click(); window.scrollTo(0,0)},40)});
  document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('[data-doc-open]'); if(!a) return; e.preventDefault();
    var k=a.getAttribute('data-doc-open'); location.hash='#docs'; setTimeout(function(){var b=$('#docIdx [data-doc="'+k+'"]'); if(b) b.click(); window.scrollTo(0,0)},40)});
'''
rep("  $$('[data-product-target]').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();jumpTo(a.getAttribute('data-product-target'))})});\n  window.addEventListener('hashchange',route); route();",
    JS + "  $$('[data-product-target]').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();jumpTo(a.getAttribute('data-product-target'))})});\n  window.addEventListener('hashchange',route); route();")
EN = {'留下公司和联系方式，商务会联系你。要开通企业账户，可以一起申请。': 'Leave your company and contact details and our sales team will reach out. You can apply for a business account at the same time.', '开始': 'Start', '接口': 'Endpoints', 'AI 模型接口': 'AI model API', 'AI 模型接口 →': 'AI model API →', '快速开始': 'Quick start', '接入客户端': 'Connect a client',
      '鉴权与 Key': 'Auth & keys', '模型与计费': 'Models & billing', '错误码': 'Error codes', '延迟与服务等级': 'Latency & service levels', '文档 - 沐仞科技 FathomPeak': 'Docs - FathomPeak',
      '场站情况（可不填）：能源类型、装机、所在省市': 'Site details (optional): energy type, capacity, province', '场站情况（可不填）': 'Site details (optional)'}
rep('  syncAuthLocale(); applyLang();', '  (function(S){for(var k in S) if(!(k in I18N)) I18N[k]=S[k]})(' + json.dumps(EN, ensure_ascii=False) + ');  /* 文档入口与表单英文：只补缺 */\n  I18N["留下公司和联系方式，商务会联系你。要开通企业账户，可以一起申请。"]="Leave your company and contact details and our sales team will reach out. You can apply for a business account at the same time.";  /* 改写过的键强制覆盖 */\n  syncAuthLocale(); applyLang();')
open(OUT, 'w', encoding='utf8').write(s)
print('done:', OUT)
