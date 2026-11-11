"""把首页重设计原型（demo/沐仞首页_重设计_视觉动效交互_2026-10-14.html）换进线上站首页。
Zixin 2026-10-14："首页的设计换成这个，但导航 bar、非首页的不换"——所以只替换 <section data-route="home"> 的内容；
导航、页脚、其他路由、咨询浮窗、底部常驻按钮沿用线上。

做法：
1 原型正文（首屏 → 结尾，不含原型自带的导航/页脚/底部按钮）包进 <div id="home2">。
2 原型 CSS 每条选择器加 #home2 前缀（:root/html/body 映射成 #home2，overflow-x 用 clip 以免打断 sticky）；
  前面先放一条 #home2 内的 all:revert，挡住线上同名类（.hero/.case/.k/.feat…）的样式（svg/img 不重置，保留其尺寸与描边属性）。
3 原型 JS 改成只在 #home2 内查元素；模型目录 M 与看板 T 直接取线上数据（线上脚本暴露 window.__FP），不另存一份；
  动态生成/滚动插入的内容调用线上翻译（__FP.txEl），英文模式也不留中文。
4 线上脚本里写旧首页元素的几行加空值保护；底部常驻按钮改为在新结尾出现时隐藏。
5 英文：EN 字典补齐 #home2 内全部新文案。
用法：python3 -I build_home_redesign_port_2026-10-14.py <仓库目录> <原型.html>
"""
import json, os, re, shutil, sys

REPO, PROTO = sys.argv[1], sys.argv[2]
P = os.path.join(REPO, 'index.html')
s = open(P, encoding='utf8').read()
p = open(PROTO, encoding='utf8').read()
LIVE = 'https://xanthiawang.github.io/fathompeak-site/'


def must(cond, msg):
    if not cond: sys.exit('[停止] ' + msg)


# ---------- 1 原型正文 ----------
body = p[p.index('<header class="hero" id="top">'):p.index('<footer class="ft">')].rstrip() + '\n'
body = body.replace(LIVE + '#', '#').replace('src="model-logos/', 'src="art/model-logos/')
ANS_ZH = '把算力任务调度到绿电所在之处：一体机部署在电站旁，用富余绿电生产词元。'
ANS_EN = 'Compute tasks are routed to where the green power is: appliances sit beside the plants and turn surplus green power into tokens.'
must(body.count(f'data-t="{ANS_ZH}"') == 1, '示例回答 data-t 未找到')
body = body.replace(f'data-t="{ANS_ZH}"', f'data-t="{ANS_ZH}" data-en="{ANS_EN}"')
must(LIVE not in body, '正文里还有绝对链接')
HOME2 = '\n<div id="home2">\n' + body + '</div>\n'


# ---------- 2 原型 CSS 加 #home2 前缀 ----------
css = p[p.index('<style>') + len('<style>'):p.index('</style>')]


def blocks(t):
    out, i, n = [], 0, len(t)
    while i < n:
        if t.startswith('/*', i): i = t.index('*/', i) + 2; continue
        if t[i].isspace(): i += 1; continue
        j = t.index('{', i); pre = t[i:j].strip(); d, k = 1, j + 1
        while d:
            d += {'{': 1, '}': -1}.get(t[k], 0); k += 1
        out.append((pre, t[j + 1:k - 1])); i = k
    return out


def split_sel(sel):
    parts, d, cur = [], 0, ''
    for ch in sel:
        if ch in '([': d += 1
        elif ch in ')]': d -= 1
        if ch == ',' and d == 0: parts.append(cur); cur = ''
        else: cur += ch
    return parts + [cur]


def pref(sel):
    sel = ' '.join(sel.split())
    for r in (':root', 'html', 'body'):
        if sel == r or sel.startswith((r + ' ', r + ':', r + '[', r + '.')):
            return '#home2' + sel[len(r):]
    return '#home2 ' + sel


def scope(t):
    out = []
    for pre, bd in blocks(t):
        if pre.startswith('@media') or pre.startswith('@supports'):
            out.append(pre + '{' + scope(bd) + '}')
        elif pre.startswith('@'):
            out.append(pre + '{' + bd + '}')
        else:
            sels = [pref(x) for x in split_sel(pre)]
            if any(x == '#home2' for x in sels):
                bd = bd.replace('overflow-x:hidden', 'overflow-x:clip')
            out.append(','.join(sels) + '{' + bd + '}')
    return '\n'.join(out)


RESET = ('#home2 :where(*:not(svg,svg *,img)),#home2 :where(*:not(svg,svg *,img))::before,'
         '#home2 :where(*:not(svg,svg *,img))::after{all:revert}')
CSS = ('\n<style id="home2-css">\n/* 首页（2026-10-14 重设计）：先挡住线上同名类，再放原型样式；全部限定在 #home2 内 */\n'
       + RESET + '\n' + scope(css) +
       '\nhtml:has(section[data-route="home"].on) body{background:#FBFAF6;margin:0}'
       '\nsection[data-route="home"]{padding:0;margin:0;max-width:none}\n</style>\n')
must(css.count('{') == css.count('}'), '原型 CSS 括号不配对')


# ---------- 3 原型 JS ----------
js = p[p.index('<script>') + len('<script>'):p.index('</script>', p.index('<script>'))]


def jrep(old, new, cnt=1):
    global js
    c = js.count(old)
    must(c == cnt, f'原型 JS 匹配 {c} 次（应为 {cnt}）：{old[:70]}')
    js = js.replace(old, new)


jrep("var $=function(s){return document.querySelector(s)}, $$=function(s){return [].slice.call(document.querySelectorAll(s))};",
     "var root=document.getElementById('home2'); if(!root) return;\n"
     "  var $=function(s){return root.querySelector(s)}, $$=function(s){return [].slice.call(root.querySelectorAll(s))};\n"
     "  var FP=window.__FP||{}, tx=function(el){if(FP.txEl&&el)FP.txEl(el)};")
mi = js.index('  var M=['); mj = js.index('\n', mi)
js = js[:mi] + "  var M=(FP.M||[]).map(function(m){return [m.name,m.vendor||'',(m.type||[''])[0],m.mkt]});" + js[mj:]
ti = js.index('  var T=['); tj = js.index('\n', ti)
js = js[:ti] + "  var T=FP.T||[];" + js[tj:]
jrep("../../官网线上版副本_2026-10-13/art/logos/", "art/logos/")
jrep("tk.insertAdjacentHTML('afterbegin',row(T[ti]))", "tk.insertAdjacentHTML('afterbegin',row(T[ti])); tx(tk.firstElementChild)")
jrep("function fill(){var h='';for(var i=0;i<5;i++)h+=row(T[(ti+i)%T.length]);tk.innerHTML=h.replace(/ new/g,'')} fill();",
     "function fill(){if(!T.length)return; var h='';for(var i=0;i<5;i++)h+=row(T[(ti+i)%T.length]);tk.innerHTML=h.replace(/ new/g,'')} fill();")
jrep("if(!reduce) setInterval(", "if(!reduce&&T.length) setInterval(")
jrep("}).join('')}\n  renderM('all');", "}).join(''); tx(mlist)}\n  renderM('all');")
jrep("$('#flip').textContent=card.classList.contains('flip')?'看产地卡':'用在哪里'}",
     "$('#flip').textContent=card.classList.contains('flip')?'看产地卡':'用在哪里'; tx($('#flip'))}")
jrep("var t=ans.dataset.t;", "var t=(document.documentElement.lang==='en'&&ans.dataset.en)||ans.dataset.t;")
di = js.index('  /* 底部常驻 CTA'); dj = js.rindex('})();')
FIT = r"""  tx(root);
  /* 首屏：文案换成英文等变长时，把产品窗口推到文案下方，避免压字 */
  var hHero=$('.hero'), hCopy=$('.hero .copy'), hWin=$('.win');
  function fitHero(){ if(!hHero||!hCopy||!hWin) return; var hb=hHero.getBoundingClientRect(); if(!hb.height) return; hWin.style.top=''; var need=hCopy.getBoundingClientRect().bottom-hb.top+14; if(hWin.getBoundingClientRect().top-hb.top<need) hWin.style.top=need+'px' }
  fitHero(); addEventListener('resize',fitHero); addEventListener('hashchange',function(){setTimeout(fitHero,60)});
  if(window.MutationObserver) new MutationObserver(fitHero).observe(document.documentElement,{attributes:true,attributeFilter:['lang']});
  if(document.fonts&&document.fonts.ready) document.fonts.ready.then(fitHero);
"""
js = js[:di] + FIT + js[dj:]
js = js.replace(LIVE + '#', '#')
must(LIVE not in js, 'JS 里还有绝对链接')
JS = '\n<script id="home2-js">\n/* 首页（2026-10-14 重设计）交互：只作用于 #home2；数据取线上 window.__FP */\n' + js.strip() + '\n</script>\n'


# ---------- 4 换进线上站 ----------
a = s.index('<section data-route="home">') + len('<section data-route="home">')
b = s.index('\n</section>\n\n<!-- 模型市场 -->', a)
old_home = s[a:b]
must('<div class="hero">' in old_home and 'cta-end' in old_home, '旧首页边界不对')
s = s[:a] + HOME2 + s[b:]


def rep(old, new, cnt=1):
    global s
    c = s.count(old)
    must(c == cnt, f'线上匹配 {c} 次（应为 {cnt}）：{old[:70]}')
    s = s.replace(old, new)


ti = s.index('  var T=['); tj = s.index('\n', ti)
s = s[:tj] + '\n  window.__FP={M:M,T:T};' + s[tj:]
rep("\n    node.__zh=src; node.nodeValue=out }\n",
    "\n    node.__zh=src; node.nodeValue=out }\n"
    "  window.__FP=window.__FP||{}; window.__FP.txEl=function(el){var w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT),n,l=[]; while((n=w.nextNode()))l.push(n); l.forEach(tx)};\n")
rep("tickerRows(hero,5);", "if(hero)tickerRows(hero,5);")
rep("[hero,net].forEach(function(el,k){ var row=", "[hero,net].forEach(function(el,k){ if(!el) return; var row=")
rep("$('#heroCards').innerHTML=", "($('#heroCards')||{}).innerHTML=")
rep("$('#mq1').innerHTML=mqHTML; $('#mq2').innerHTML=mqHTML;", "($('#mq1')||{}).innerHTML=mqHTML; ($('#mq2')||{}).innerHTML=mqHTML;")
rep("$('#homeModels').innerHTML=", "($('#homeModels')||{}).innerHTML=")
rep("end=$('section[data-route=\"home\"] .cta-end');", "end=$('section[data-route=\"home\"] .cta-end')||$('#home2 .end');")
k = s.rindex('</head>'); s = s[:k] + CSS + s[k:]
k = s.index('\n\n<script type="module" id="account-art-motion"'); s = s[:k] + '\n' + JS + s[k:]

# 模型图标
dst = os.path.join(REPO, 'art', 'model-logos'); os.makedirs(dst, exist_ok=True)
for f in sorted(os.listdir(os.path.join(os.path.dirname(PROTO), 'model-logos'))):
    if f.endswith('.svg'): shutil.copyfile(os.path.join(os.path.dirname(PROTO), 'model-logos', f), os.path.join(dst, f))

# ---------- 5 英文 ----------
EN = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'home2_en_2026-10-14.json'), encoding='utf8')) \
    if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'home2_en_2026-10-14.json')) else {}
EN[ANS_ZH] = ANS_EN
k2 = s.index('var I18N={') + len('var I18N={')
s = s[:k2] + ''.join(json.dumps(x, ensure_ascii=False) + ':' + json.dumps(y, ensure_ascii=False) + ',' for x, y in EN.items()) + s[k2:]

open(P, 'w', encoding='utf8').write(s)
print('done. EN entries:', len(EN))
