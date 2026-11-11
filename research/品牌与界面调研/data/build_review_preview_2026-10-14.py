"""按 impeccable critique（2026-10-14，21/32）改首页，先出预览 HTML，不动线上（Zixin："不要直接修改线上网站 先做修改后的html看一下效果"）。
改动（只用《企业信息表》里已有的事实）：
 P1 首屏：标题保留原句；副文案按 Zixin 给的两行（"……MiniMax，兼容 OpenAI 与 Gemini。/ 一体机部署在电站旁，用富余绿电生产词元，价低至 5 折。"），
    这两行和"Soul"已于 2997925 上线，本脚本遇到已上线的文字就跳过。标题放大成全页最大字（≤56px）、CJK 只在标点/空格处断行、标点压半宽；水印更淡。
 P1 英文版：卡片/步骤标题不再用 Pinyon 花体首字母（"35" 被看成 "55"、"RMB" 花体 R）。
 P1 电站方：统一叫"电站合作"（按钮"申请电站合作 →"），首屏去掉重复的"能源与节点合作"。
    不另起一节（Zixin："是否可以在现有排版上加文字即可或者改变字体？而不是突然又出来一行"）：
    项目案例两组：小号组名在上，下面一句衬线标语（客户"绿色词元，直供全球。"；电站"富余绿电，就地变成词元。"+右侧"申请电站合作 →"），下面仍是原来的案例卡。
 P2 主按钮：箭头统一为 →。
 P2 手机：怎么用"步骤—截图"交错排列；底部常驻按钮在页脚、结尾、电站合作组可见时隐藏；菜单展开时隐藏咨询按钮（全站）；首屏小链接触控高度 44px。
 P2 对比度：首页小号灰字由 50% 提到 62%，未激活步骤由 35% 提到 55%。
 其他：首屏装饰窗口里被弧线盖住的"查看产品与模型 →"移出 Tab 顺序。
用法：python3 -I build_review_preview_2026-10-14.py <源 index.html> <输出 index.html>
"""
import json, sys

SRC, OUT = sys.argv[1], sys.argv[2]
SOFT = '--soft' in sys.argv  # 线上已被别的会话部分采纳时，已做过的改动跳过，只补没做的
s = open(SRC, encoding='utf8').read()
NB = ' '


def home_rep(old, new, n=1):
    global s
    a = s.index('<div id="home2">'); b = s.index('<section data-route=', a)
    c = s[a:b].count(old)
    if c != n:
        if SOFT: print(f'[跳过] 首页内匹配 {c} 次：{old[:50]}'); return
        sys.exit(f'[停止] 首页内匹配 {c} 次（应为 {n}）：{old[:60]}')
    s = s[:a] + s[a:b].replace(old, new) + s[b:]


def home_has(t):
    a = s.index('<div id="home2">'); b = s.index('<section data-route=', a)
    return t in s[a:b]


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        if SOFT: print(f'[跳过] 全文匹配 {c} 次：{old[:50]}'); return
        sys.exit(f'[停止] 全文匹配 {c} 次（应为 {n}）：{old[:60]}')
    s = s.replace(old, new)


# 首屏副文案与 Soul：已上线（2997925）则跳过
SUB1 = 'GLM、DeepSeek、Qwen、MiniMax，兼容 OpenAI 与 Gemini。'
SUB2 = f'一体机部署在电站旁，用富余绿电生产词元，价低至 5{NB}折。'
if not home_has(SUB1):
    home_rep('<p class="sub">GLM、DeepSeek、Qwen、MiniMax 一个端点接入，兼容 OpenAI 与 Gemini 原生格式。一体机部署在电站旁，用富余绿电生产词元，为 AI 企业提供低成本、可追溯的推理服务。</p>',
             f'<p class="sub">{SUB1}<br>{SUB2}</p>')
if not home_has('<b>Soul</b>'):
    home_rep('<b>某头部社交平台</b>', '<b>Soul</b>')
home_rep('>免费试用 API ↓</a>', '>免费试用 API →</a>', 2)
home_rep('>申请成为产地 →</a>', '>申请电站合作 →</a>', 2)
home_rep('<div class="s2"><a href="#enterprise">企业采购与海外服务 →</a><a href="#network">能源与节点合作 →</a></div>',
         '<div class="s2"><a href="#enterprise">企业采购与海外服务 →</a></div>')
home_rep('<a class="ul" href="#models">查看产品与模型 →</a>', '<a class="ul" href="#models" tabindex="-1">查看产品与模型 →</a>')

# 项目案例：两组标题改衬线小标题；电站组标题行加说明与链接，并包一层 #plant（底部浮条据此隐藏）
PITCH = '富余绿电，就地变成词元。'  # Zixin：加的说明太长，"这几个字就够了"
SLOGAN_C = '绿色词元，直供全球。'  # 客户组标语（仿 Gamma；"词元直供"是公司用语，海外订单占比超 83%）
home_rep('  <div class="cgh rv">客户与订单</div>\n', f'  <div class="cgh2 rv"><span class="k">客户与订单</span><b>{SLOGAN_C}</b></div>\n')
a = s.index('<div id="home2">'); b = s.index('<section data-route=', a)
h = s[a:b]
i0 = h.find('  <div class="cgh rv">电站合作</div>\n  <div class="cases">')
if i0 < 0 and SOFT: print('[跳过] 电站案例组已被改过')
elif i0 < 0: sys.exit('[停止] 找不到电站案例组')
if i0 >= 0:
    i1 = h.index('  </div>\n', i0 + 60) + len('  </div>\n')
    grp = h[i0:i1]
    for w in ('100MW 光伏电站', '35 座光伏电站', '海上风电直连海上算力中心', '1GW 光伏项目'):
        if w not in grp: sys.exit(f'[停止] 电站案例块缺少 {w}')
    grp = grp.replace('  <div class="cgh rv">电站合作</div>\n',
                      f'  <div class="cgh2 rv"><span class="k">电站合作</span><b>{PITCH}</b><a class="ul" href="#network">申请电站合作 →</a></div>\n')
    grp = '  <div id="plant">\n' + grp + '  </div>\n'
    h = h[:i0] + grp + h[i1:]
    s = s[:a] + h + s[b:]

# 底部常驻按钮：页脚、结尾、电站合作组可见时都隐藏
rep("var heroIn=true,endIn=false; function upd(){var home=$('section[data-route=\"home\"]').classList.contains('on'); var on=home&&!heroIn&&!endIn;",
    "var heroIn=true,endIn=false,ftIn=false,pcIn=false; function upd(){var home=$('section[data-route=\"home\"]').classList.contains('on'); var on=home&&!heroIn&&!endIn&&!ftIn&&!pcIn;")
rep("if(end) new IntersectionObserver(function(es){endIn=es[0].isIntersecting;upd()},{threshold:0.01}).observe(end);",
    "if(end) new IntersectionObserver(function(es){endIn=es[0].isIntersecting;upd()},{threshold:0.01}).observe(end);\n"
    "    var ft=document.querySelector('footer'); if(ft) new IntersectionObserver(function(es){ftIn=es[0].isIntersecting;upd()},{threshold:0}).observe(ft);\n"
    "    var pc=document.querySelector('#home2 #plant'); if(pc) new IntersectionObserver(function(es){pcIn=es[0].isIntersecting;upd()},{threshold:0}).observe(pc);")

CSS = '''
<style id="home2-review">
/* 首页按 critique 修改（2026-10-14） */
#home2 .hero h1{font-size:clamp(32px,3.9vw,56px);line-height:1.14;letter-spacing:-.03em;word-break:keep-all;font-feature-settings:"halt"}
#home2 .word{color:rgba(255,255,255,.045)}
#home2 .k,#home2 .cgh,#home2 .case .st,#home2 .hero .ctas .s,#home2 .end p{color:rgba(0,0,0,.62)}
#home2 .end p.end-sub{color:rgba(0,0,0,.72)}
#home2 .step{opacity:.55}
#home2 .step.on{opacity:1}
html[lang="en"] #home2 .case b::first-letter,html[lang="en"] #home2 .itile .n::first-letter,html[lang="en"] #home2 .step b::first-letter,
html[lang="en"] #home2 .panel b::first-letter,html[lang="en"] #home2 .rc-src b::first-letter,html[lang="en"] #home2 .cgh2 b::first-letter{font:inherit;font-size:1em;padding:0}
/* 项目案例组标题：衬线小标题；电站组同一行带说明与链接 */
#home2 .cgh2{display:grid;grid-template-columns:minmax(0,1fr) auto;grid-template-areas:"k k" "b a";align-items:baseline;column-gap:22px;margin:0 0 18px}
#home2 .cgh2 .k{grid-area:k;display:block;margin-bottom:8px}
#home2 #plant .cgh2{margin-top:44px}
#home2 .cgh2 b{grid-area:b;font-family:var(--serif);font-weight:400;font-size:28px;line-height:1.25;letter-spacing:-.015em;color:#000;font-variation-settings:"opsz" 144;font-feature-settings:"halt"}
#home2 .cgh2 a.ul{grid-area:a;font-size:14px;white-space:nowrap}
body:has(#pill.open) .fab{opacity:0;pointer-events:none}
@media (max-width:860px){
  #home2 .feat{display:flex;flex-direction:column;gap:16px}
  #home2 .feat .steps,#home2 .feat .media{display:contents}
  #home2 .step[data-i="0"]{order:1}#home2 .pan[data-p="0"]{order:2}
  #home2 .step[data-i="1"]{order:3}#home2 .pan[data-p="1"]{order:4}
  #home2 .step[data-i="2"]{order:5}#home2 .pan[data-p="2"]{order:6}
  #home2 .step{padding:28px 0 4px}
  #home2 .hero .ctas .s,#home2 .hero .ctas .s2 a{display:inline-flex;align-items:center;min-height:44px}
  #home2 .hero .ctas{gap:4px}
  #home2 .cgh2{grid-template-columns:1fr;grid-template-areas:"k" "b" "a";row-gap:4px}
  #home2 .cgh2 b{font-size:24px}
  #home2 .cgh2 a.ul{justify-self:start;min-height:44px;display:inline-flex;align-items:center}
}
</style>
'''
k = s.rindex('</head>'); s = s[:k] + CSS + s[k:]

EN = {
    SUB1: 'GLM, DeepSeek, Qwen and MiniMax, compatible with OpenAI and Gemini.',
    SUB2: 'Appliances beside power plants turn surplus green power into tokens, at up to 50% off.',
    '申请电站合作 →': 'Apply for a plant partnership →', '电站合作': 'Power plant partnerships', '客户与订单': 'Customers and orders',
    PITCH: 'Surplus green power, turned into tokens on site.', SLOGAN_C: 'Green tokens, supplied worldwide.',
}
k2 = s.index('var I18N={') + len('var I18N={')
s = s[:k2] + ''.join(json.dumps(x, ensure_ascii=False) + ':' + json.dumps(y, ensure_ascii=False) + ',' for x, y in EN.items()) + s[k2:]

open(OUT, 'w', encoding='utf8').write(s)
print('done:', OUT)
