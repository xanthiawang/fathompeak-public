"""首页节奏按 Dia 首页整理：
1 统一标题：每节 = 小号灰色眉标 + 大号衬线标题（与"大模型，缺电。"同级，32–46px）；功能区补标题，项目案例、常见问题、行业与场景放大到同级。
2 统一间距：大节之间约 140px（手机 88px）。
3 首页去掉"新闻动态"（关于页顶部已有），脚本加判空。
4 动效：滚过首屏后底部出现固定的"获取 API Key"黑胶囊（结尾 CTA 出现时隐藏）；箭头悬停右移；新标题淡入。
首屏 HTML 与首页结尾 CTA 逐字不变。
用法：python3 -I build_home_rhythm_2026-10-13.py <仓库副本目录>
"""
import json, os, sys

P = os.path.join(sys.argv[1], 'index.html')
s = open(P, encoding='utf8').read()
hero0 = s[s.index('<div class="hero">'):s.index('<div class="partners">')]
end0 = s[s.index('<div class="cta-end rv">'):s.index('</section>', s.index('<div class="cta-end rv">'))]

def rep(old, new, n=1):
    global s
    k = s.index('var I18N={')
    c = s[:k].count(old)
    if c != n: sys.exit(f'[停止] 匹配 {c} 次（应为 {n}）：{old[:80]}')
    s = s[:k].replace(old, new) + s[k:]

# 1. 功能区补标题
rep('\n  <div class="feat">\n', '\n  <div class="hh c rv"><span class="k">怎么用</span><h2>接入、计价与产地</h2></div>\n  <div class="feat">\n')
# 项目案例：统一标题
rep('<div class="sec" style="margin-top:44px"><div class="hd"><h3 class="serif">项目案例</h3><span class="k">试点与推进中项目</span></div>',
    '<div class="sec home-sec"><div class="hh rv"><span class="k">试点与推进中项目</span><h2>项目案例</h2></div>')
# 3. 去掉首页新闻
rep('<div class="wrap rv"><div class="sec"><div class="hd"><h3 class="serif">新闻动态</h3><a class="ul" href="#news">查看全部新闻 →</a></div><div class="events" id="homeNews"></div></div></div>\n', '')
rep("$('#homeNews').innerHTML=NEWS.slice(0,3).map(newsRow).join('');", "var _hn=$('#homeNews'); if(_hn){_hn.innerHTML=NEWS.slice(0,3).map(newsRow).join('')}")
# 4. 底部固定 CTA
rep('<div class="fab" id="fab">', '<div class="dock" id="dock" aria-hidden="true"><a class="btn black" href="#start" tabindex="-1">获取 API Key →</a></div>\n<div class="fab" id="fab">')
JS = r"""
  /* ---------- 首页底部固定 CTA（学 Dia）：滚过首屏出现，结尾 CTA 进入视口时隐藏 ---------- */
  (function(){var d=$('#dock'),hero=$('.hero'),end=$('section[data-route="home"] .cta-end'); if(!d||!hero||!window.IntersectionObserver) return;
    var heroIn=true,endIn=false; function upd(){var home=$('section[data-route="home"]').classList.contains('on'); var on=home&&!heroIn&&!endIn; d.classList.toggle('on',on); d.setAttribute('aria-hidden',String(!on)); d.querySelector('a').tabIndex=on?0:-1}
    new IntersectionObserver(function(es){heroIn=es[0].isIntersecting;upd()},{threshold:0.05}).observe(hero);
    if(end) new IntersectionObserver(function(es){endIn=es[0].isIntersecting;upd()},{threshold:0.01}).observe(end);
    window.addEventListener('hashchange',function(){setTimeout(upd,60)}); upd() })();
"""
rep("  /* ---------- 功能区：指示条 + 粘性截图 ---------- */", JS + "  /* ---------- 功能区：指示条 + 粘性截图 ---------- */")

CSS = '''
/* 首页节奏（学 Dia）：统一标题 + 统一间距 + 底部固定 CTA + 箭头悬停 */
.hh{max-width:1120px;margin:0 auto 26px;padding:0 20px}
.home-sec .hh,.fq-sec .hh{padding:0}
.hh.c{text-align:center}
.hh .k{display:block;margin-bottom:10px}
.hh h2,.fq-h,.faq h2{font-family:var(--serif);font-weight:400;font-size:clamp(30px,4vw,44px);line-height:1.15;letter-spacing:-.025em;color:var(--ink);font-variation-settings:"opsz" 144}
.hh h2{margin:0}
.why2{padding-top:140px}
.hh.c{margin-top:140px}
.feat{padding-top:24px}
.fq-sec{margin-top:140px}
.home-sec{margin-top:140px}
.faq{margin-top:140px}
.faq h2{margin-bottom:40px}
section[data-route="home"] .cta-end{padding-top:140px}
.dock{position:fixed;left:50%;bottom:22px;z-index:55;transform:translate(-50%,24px);opacity:0;pointer-events:none;transition:opacity .35s var(--ease),transform .45s var(--ease-out)}
.dock.on{opacity:1;transform:translate(-50%,0);pointer-events:auto}
.dock .btn{height:48px;padding:0 26px;font-size:15px;box-shadow:0 14px 34px -14px rgba(0,0,0,.45)}
.fq-go,.fa-f span:last-child{transition:transform .3s var(--ease)}
a.fq:hover .fq-go,a.fa:hover .fa-f span:last-child{transform:translateX(5px)}
section[data-route="home"] .fq-sec .fq-h,section[data-route="home"] .faq h2{font-size:clamp(30px,4vw,44px);line-height:1.15;letter-spacing:-.025em}
section[data-route="home"] .home-sec .hh{text-align:center}
@media (max-width:800px){.why2{padding-top:88px}.hh.c,.fq-sec,.home-sec,.faq{margin-top:88px}section[data-route="home"] .cta-end{padding-top:88px}.dock{bottom:14px}.dock .btn{height:44px;padding:0 20px;font-size:14px}}
'''
k = s.index('</style>')
s = s[:k] + CSS + s[k:]

EN = {"怎么用": "How it works", "接入、计价与产地": "Integration, pricing & origin", "试点与推进中项目": "Pilots and projects in progress",
      "获取 API Key →": "Get API Key →"}
k2 = s.index('var I18N={') + len('var I18N={')
s = s[:k2] + ''.join(json.dumps(x, ensure_ascii=False) + ':' + json.dumps(y, ensure_ascii=False) + ',' for x, y in EN.items()) + s[k2:]

assert s[s.index('<div class="hero">'):s.index('<div class="partners">')] == hero0, '首屏 HTML 被改动'
e = s.index('<div class="cta-end rv">')
assert s[e:s.index('</section>', e)] == end0, '首页结尾 CTA 被改动'
open(P, 'w', encoding='utf8').write(s)
print('done.')
