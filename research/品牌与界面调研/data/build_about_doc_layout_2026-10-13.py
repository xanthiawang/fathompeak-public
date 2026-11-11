"""关于页改为"文档式"排版（左侧吸顶目录 + 右侧单栏正文 + 细线列表），首页地平线光圈下移避开白色标题。
在 build_about_layout_2026-10-13.py 之后运行，只改本地副本 index.html；首屏 HTML 与首页结尾 CTA 逐字不变（只改光圈 CSS）。
用法：python3 -I build_about_doc_layout_2026-10-13.py <仓库副本目录>
"""
import json, os, re, sys

P = os.path.join(sys.argv[1], 'index.html')
s = open(P, encoding='utf8').read()
hero0 = s[s.index('<div class="hero">'):s.index('<div class="partners">')]
end0 = s[s.index('<div class="cta-end rv">'):s.index('</section>', s.index('<div class="cta-end rv">'))]

def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: sys.exit(f'[停止] 匹配 {c} 次（应为 {n}）：{old[:70]}')
    s = s.replace(old, new)

# ---------- 1. 首页标题与光圈不再重合（第二个参数选方案：down = 文字下移进暗部、光圈略上提；shadow = 位置不动、文字加柔和暗边） ----------
HERO = sys.argv[2] if len(sys.argv) > 2 else 'down'
if HERO == 'down':
    a = s.index(':root[data-scheme="B"] .hero .field{inset:0;')
    b = s.index('}', a)
    rule = s[a:b]
    assert rule.count('calc(235px + 100vw)') == 1
    # 弧顶 235px → 190px；窄屏半径不小于 1200px，弧更平，标题两端不再压到光带
    new_rule = (rule.replace('calc(235px + 100vw)', 'calc(190px + var(--R))')
                    .replace('100vw', 'var(--R)')
                    .replace('{inset:0;', '{--R:max(100vw,1200px);inset:0;', 1))
    s = s[:a] + new_rule + s[b:]
    rep('.hero .h{position:absolute;left:24px;right:24px;top:116px;', '.hero .h{position:absolute;left:24px;right:24px;top:226px;')
    rep('.hero .tag{position:absolute;left:24px;right:24px;top:172px;', '.hero .tag{position:absolute;left:24px;right:24px;top:282px;')
    rep('.hero .h-sub{position:absolute;left:24px;right:24px;top:212px;', '.hero .h-sub{position:absolute;left:24px;right:24px;top:322px;')
    rep('.hero .word{position:absolute;left:50%;top:max(270px,calc(50svh - 50.5vw + 120px));',
        '.hero .word{position:absolute;left:50%;top:268px;')
    rep('.hero .product{position:absolute;left:50%;top:max(300px,46svh);',
        '.hero .product{position:absolute;left:50%;top:max(420px,48svh);')
elif HERO == 'shadow':
    k = s.index('</style>')
    s = s[:k] + '\n/* 首屏白字压在霞光带上：加一圈柔和暗边 */\n:root[data-scheme="B"] .hero .h,:root[data-scheme="B"] .hero .tag,:root[data-scheme="B"] .hero .h-sub{text-shadow:0 0 1px rgba(33,32,33,.55),0 1px 3px rgba(33,32,33,.45),0 2px 18px rgba(33,32,33,.35)}\n' + s[k:]

# ---------- 2. 关于页：文档式 ----------
def rows(items):
    return '<ul class="ab-rows">' + ''.join(
        f'<li><span class="k">{k}</span><div><b>{t}</b>' + (f'<span class="s">{d}</span>' if d else '') + '</div></li>'
        for k, t, d in items) + '</ul>'

TOC = [('ab-news', '新闻动态'), ('ab-story', '我们的故事'), ('ab-roadmap', '路线图'), ('ab-values', '价值观'),
       ('ab-support', '机构支持'), ('ab-investors', '投资方'), ('ab-honors', '奖项与荣誉'), ('ab-company', '公司信息'),
       ('careers', '加入我们'), ('ab-contact', '联系我们')]

ABOUT = '''<section data-route="about">
  <div class="wrap">
  <div class="ab">
    <div class="ab-head"><span class="ab-mk"><svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true"><path d="M3 20 10 6l4 7 3-4 4 11z" fill="currentColor"/></svg>沐仞 FathomPeak</span><h1 class="display">关于沐仞</h1></div>
    <div class="ab-grid">
      <nav class="ab-toc" aria-label="关于沐仞目录">''' + ''.join(f'<a href="#about" data-scrollto="{i}">{t}</a>' for i, t in TOC) + '''</nav>
      <div class="ab-body">

        <div class="ab-sec" id="ab-news"><h2>新闻动态</h2>
          <div class="events" id="aboutNews"></div>
          <a class="ul ab-more" href="#news">查看全部新闻 →</a>
        </div>

        <div class="ab-sec" id="ab-story"><h2>我们的故事</h2>
          <p>创始人路畅为清华大学工学直博生，研究方向为算电协同调度，入选中国 AI U25 创业者榜单。他连续创业六年，曾任某 AI Infra 企业 COO，参与青海省国网算电协同调度项目，并入选清华大学—麻省理工学院 Energy Ventures 交换项目。在人工智能基础设施与能源基础设施长期分立发展的格局下，路畅提出并构建了"算电协同、词元直供"的全新范式：不再把电力输送到算力所在之处，而是把算力任务调度到绿电所在之处。</p>
          <p>基于这一思路，公司自研 TAPESTRIX 异构调度架构，构建与能源系统深度耦合的分布式算网。沐仞词元一体机部署于光伏、风电、水电等新能源电站，将富余绿电就地转化为绿色词元，再经由绿色词元交易平台交付全球 AI 企业。平台、基座、一体机三层产品形成"平台接单、基座调度、一体机生产、平台交付"的完整闭环，每笔订单均可追溯至电站、时段与能源消耗。</p>
          <p>核心团队由清华大学、北京大学、南洋理工大学、武汉大学等高校的博士与研究者，以及来自微软亚洲研究院、字节跳动、英伟达等企业的技术骨干组成，研究成果发表于 ASPLOS、ISCA、OSDI 等体系结构与系统领域顶级会议。</p>
          <h3>使命</h3>
          <p>以绿色能源承载全球计算。</p>
          <h3>愿景</h3>
          <p>扎根中国算电基础，服务全球计算需求。短期以新能源电站与全球 AI 企业为两端，与头部能源国企落成算电协同试点，形成词元直供的商业闭环。中长期建设覆盖中国、东南亚、中东、欧洲与北美的全球分布式算网，通过算力任务的时空迁移消纳多地绿电，形成"算电双轮驱动、时空互补调度"的全球算力潮汐体系。</p>
        </div>

        <div class="ab-sec" id="ab-roadmap"><h2>路线图</h2>
          <p class="q">从一座电站，到一张算网，再到全球算力潮汐</p>
          <p>绿色词元直供是地基。路线图在其上逐层构建：先把电站侧算力变成可交付的服务，再让调度系统统一指挥算力与电力，最终形成跨地区、跨时区的全球分布式算网。</p>
          ''' + rows([
              ('01 · 现阶段', '绿色词元直供', '绿色词元交易平台面向全球 AI 企业提供推理服务；沐仞词元一体机部署于新能源电站，与头部能源国企落成算电协同试点，完成从绿电获取、词元生产到跨境交付与结算的闭环。'),
              ('02 · 开发中', '算电协同群智基座', '由算力集群管理、电力资源管理、算电协同调度三个智能体组成的调度层，统一观测算力、电力、网络与存储资源，完成绿电与电价预测、GPU 能耗预测和跨电站任务迁移；开放第三方电站与算力中心接入，节点越多，调度越优。'),
              ('03 · 愿景', '全球算力潮汐', '覆盖中国、东南亚、中东、欧洲与北美的全球分布式算网。算力任务随各地绿电的时空分布迁移，以"算电双轮驱动、时空互补调度"消纳多地绿电，把中国的能源优势转化为全球的 AI 词元优势。'),
          ]) + '''
        </div>

        <div class="ab-sec" id="ab-values"><h2>价值观</h2>
          <p class="q">栉风沐雨，登高万仞</p>
          <h3>登高万仞</h3><p>以长期主义攻克算力与能源交叉领域的硬核问题，在难而正确的方向上持续投入。</p>
          <h3>实事求是</h3><p>以可计量、可追溯的数据作为决策与对外承诺的依据。</p>
          <h3>扎根现场</h3><p>深入电站与机房一线，在真实场景中验证技术、解决问题。</p>
          <h3>开放协同</h3><p>与能源企业、产业资本、高校与客户共建算电协同生态，共享增长收益。</p>
        </div>

        <div class="ab-sec" id="ab-support"><h2>机构支持</h2>
          ''' + rows([
              ('高校', '清华大学', '创始人与核心团队的科研来源，涵盖能源技术、计算机、交叉信息与工程物理。'),
              ('高校', '北京大学', '计算机与人工智能方向技术骨干来源。'),
              ('联合研发', '深圳清华大学研究院', '共建算电协同联合研发中心。'),
              ('首席顾问', '张文宇教授', '前浙江大学二级教授、麻省理工学院博士后，"群智工业"理论提出者，连续 4 年入选全球前 2% 顶尖科学家。'),
              ('资质', '中央网信办', '词元出海业务资质批复，出海运营主体位于广东汕头。'),
          ]) + '''
        </div>

        <div class="ab-sec" id="ab-investors"><h2>投资方</h2>
          <p>公司两个月内完成天使轮、天使+轮两轮千万级融资，股东包括能源侧与产业侧上市企业、清华系资本及社会资本。</p>
        </div>

        <div class="ab-sec" id="ab-honors"><h2>奖项与荣誉</h2>
          ''' + rows([
              ('第一名', '北京卫视《转在北京》', '智算纵横赛道'),
              ('第一名', '央视《赢在 AI+》', '智效跃迁赛道'),
              ('亚军', '"挑战杯"', '清华大学校赛'),
              ('十佳团队', '国创赛', '清华大学校赛'),
              ('国家金奖', '中国国际"互联网+"大学生创新创业大赛', '第八届 · 创始人作为项目核心成员'),
              ('入选', '中国 AI U25 创业者榜单', '创始人路畅'),
          ]) + '''
          <p>团队累计获得各类荣誉 40 余项。</p>
        </div>

        <div class="ab-sec" id="ab-company"><h2>公司信息</h2>
          ''' + rows([
              ('总部', '北京市海淀区', ''),
              ('研发', '北京海淀、深圳南山', ''),
              ('出海运营', '广东汕头', '持中央网信办词元出海业务批复'),
              ('创始人', '路畅，创始人兼 CEO', '清华大学工学直博生，研究方向为算电协同调度'),
              ('团队', '20 余人', '来自清华大学、北京大学、南洋理工大学、武汉大学等高校，以及微软亚洲研究院、字节跳动、英伟达等企业'),
              ('业务', '2026 年第三季度已签词元订单超 6000 万元', '其中海外订单占比超 83%'),
              ('研究成果', '数十篇论文', '发表于 ASPLOS、ISCA、OSDI 等会议；软件著作权及专利 10 余项'),
          ]) + '''
        </div>

        <div class="ab-sec" id="careers"><h2>加入我们</h2>
          <p class="q">我们正在招人</p>
          <p>异构调度算法、推理系统、分布式系统、能源系统建模、海外市场与产品等方向均有开放职位。年轻团队，硬核问题，快速成长。</p>
          <p class="ab-cta"><a class="btn black" href="mailto:fathompeak@163.com?subject=%E5%BA%94%E8%81%98">加入我们 ↗</a><span>HR 联系：<a class="ul" href="mailto:fathompeak@163.com">fathompeak@163.com</a></span></p>
        </div>

        <div class="ab-sec" id="ab-contact"><h2>联系我们</h2>
          <h3>业务咨询 · 媒体 · 合作</h3>
          <p><a class="ul" href="mailto:fathompeak@163.com">fathompeak@163.com</a>　企业采购、海外服务与电站合作，写信说明应用场景、需求规模和联系方式。</p>
          <p><a class="ul" href="#enterprise">查看企业合作 →</a>　<a class="ul" href="#network">查看电站合作 →</a></p>
          <h3>公司地址</h3>
          <p>北京市海淀区清河中街 66 号院 1 号楼。研发在北京海淀与深圳南山；出海运营主体设在广东省汕头市。</p>
        </div>

      </div>
    </div>
  </div>
  </div>
</section>'''

a = s.index('<section data-route="about">')
b = s.index('</section>', a) + len('</section>')
old_about = s[a:b]
# 旧版里的招聘按钮 mailto 用于核对邮箱一致
assert 'fathompeak@163.com' in old_about and 'id="careers"' in old_about
s = s[:a] + ABOUT + s[b:]

CSS = '''
/* 关于页：文档式排版（左侧吸顶目录 + 右侧单栏正文） */
.ab{max-width:1000px;margin:0 auto;padding:132px 0 24px}
.ab-head{margin-bottom:76px}
.ab-mk{display:flex;align-items:center;gap:10px;font:500 15px var(--sans);color:var(--ink-85);margin-bottom:14px}
.ab-head .display{font-size:72px;line-height:1;letter-spacing:-.04em;margin:0}
.ab-grid{display:grid;grid-template-columns:300px minmax(0,580px);column-gap:120px;align-items:start}
.ab-toc{position:sticky;top:100px;display:grid;gap:4px;justify-items:start;font-size:15px}
.ab-toc a{color:var(--ink-50);padding:2px 0;transition:color .2s var(--ease)}
.ab-toc a:hover{color:var(--ink)}
.ab-toc a.on{color:var(--accent)}
.ab-sec{padding-bottom:84px}
.ab-sec>h2{font-family:var(--serif);font-weight:400;font-size:48px;line-height:1.12;letter-spacing:-.03em;margin:0 0 22px;font-variation-settings:"opsz" 144}
.ab-sec p{font-size:16px;line-height:1.75;color:var(--ink-70);margin:0 0 14px}
.ab-sec h3{font:600 16px/1.5 var(--sans);color:var(--ink);margin:26px 0 4px}
.ab-sec p.q{font-family:var(--serif);font-size:22px;line-height:1.45;color:var(--ink);letter-spacing:-.01em}
.ab-rows{list-style:none;margin:10px 0 16px;padding:0;border-top:1px solid var(--line)}
.ab-rows li{display:grid;grid-template-columns:92px minmax(0,1fr);gap:16px;padding:15px 0;border-bottom:1px solid var(--line)}
.ab-rows .k{font:400 12px/1.9 var(--mono);color:var(--ink-50)}
.ab-rows b{display:block;font-weight:500;font-size:15px;line-height:1.6;color:var(--ink)}
.ab-rows .s{display:block;font-size:14px;line-height:1.7;color:var(--ink-70);margin-top:2px}
.ab-sec .events{border-top:1px solid var(--line)}
.ab-sec .ev{grid-template-columns:1fr;gap:4px;align-items:start}
.ab-sec .ev .k{justify-self:start}
.ab-more{display:inline-block;margin-top:16px;font-size:14px}
.ab-cta{display:flex;align-items:center;gap:18px;flex-wrap:wrap;margin-top:22px!important}
.ab-cta span{font-size:13px;color:var(--ink-50)}
@media (max-width:1100px){.ab-grid{grid-template-columns:220px minmax(0,1fr);column-gap:56px}}
@media (max-width:800px){
  .ab{padding-top:104px}
  .ab-head{margin-bottom:28px}
  .ab-head .display{font-size:48px}
  .ab-grid{grid-template-columns:1fr}
  .ab-toc{position:static;margin-bottom:48px;font-size:15px}
  .ab-sec{padding-bottom:60px}
  .ab-sec>h2{font-size:36px}
  .ab-rows li{grid-template-columns:1fr;gap:2px}
}
'''
k = s.index('</style>')
s = s[:k] + CSS + s[k:]

SPY = '''<script id="ab-spy">
/* 关于页目录：滚动时高亮当前小节 */
(function(){var toc=document.querySelectorAll('.ab-toc a');if(!toc.length)return;
  function spy(){var sec=document.querySelector('section[data-route="about"]');if(!sec||!sec.classList.contains('on'))return;var cur=toc[0];
    Array.prototype.forEach.call(toc,function(a){var t=document.getElementById(a.getAttribute('data-scrollto'));if(t&&t.getBoundingClientRect().top<160)cur=a});
    if(window.innerHeight+window.scrollY>=document.documentElement.scrollHeight-4)cur=toc[toc.length-1];
    Array.prototype.forEach.call(toc,function(a){a.classList.toggle('on',a===cur)})}
  window.addEventListener('scroll',spy,{passive:true});window.addEventListener('hashchange',function(){setTimeout(spy,60)});spy();
})();
</script>
'''
rep('<script id="fp-fresh">', SPY + '<script id="fp-fresh">')

EN = {"关于沐仞目录": "About contents", "价值观": "Values", "公司信息": "Company", "联系我们": "Contact", "使命": "Mission",
      "栉风沐雨，登高万仞": "Through wind and rain, to the summit", "出海运营": "Overseas entity", "数十篇论文": "Dozens of papers",
      "路畅，创始人兼 CEO": "Lu Chang, founder & CEO", "业务咨询 · 媒体 · 合作": "Business · press · partnerships", "公司地址": "Address",
      "查看企业合作 →": "Enterprise →", "查看电站合作 →": "Power-site partnerships →"}
k2 = s.index('var I18N={') + len('var I18N={')
s = s[:k2] + ''.join(json.dumps(x, ensure_ascii=False) + ':' + json.dumps(y, ensure_ascii=False) + ',' for x, y in EN.items()) + s[k2:]

assert s[s.index('<div class="hero">'):s.index('<div class="partners">')] == hero0, '首屏 HTML 被改动'
e = s.index('<div class="cta-end rv">')
assert s[e:s.index('</section>', e)] == end0, '首页结尾 CTA 被改动'
open(P, 'w', encoding='utf8').write(s)
print('done.')
