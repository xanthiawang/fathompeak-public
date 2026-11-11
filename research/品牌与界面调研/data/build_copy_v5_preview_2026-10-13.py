"""v5 预览：在 v4 的 23 处文字替换之上，把品牌故事全文、价值观、路线图、几个数、认可与支持、投资方、
"同一个正午"时间轴，用网站现有组件（.sec .hd / .cards3 / .steps4 / .cases / .board / .h2 / .tbl）插进首页和关于页。
原型文件不改；输出新的预览副本与一页放置说明。用法：python3 -I build_copy_v5_preview_2026-10-13.py
"""
import html, json, os, re, sys, importlib.util

D = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('v4', os.path.join(D, 'build_copy_v4_preview_2026-10-13.py'))
v4 = importlib.util.module_from_spec(spec); spec.loader.exec_module(v4)
SRC = v4.SRC
OUT = os.path.join(D, '..', 'demo', '沐仞官网原型_文案v5预览_2026-10-13.html')
PLAN = os.path.join(D, '..', '..', '沐仞官网_新增内容放置说明_2026-10-13.html')

# ---------- 新增区块（全部复用现有类名；只补时间轴色条、大数字、故事段落三处小样式） ----------
CSS = '''
/* v5 预览新增：只用现有 token */
.noon .lead2{font-family:var(--serif);font-size:clamp(26px,3.4vw,40px);letter-spacing:-.02em;line-height:1.2;margin:4px 0 0;color:var(--ink)}
.noon .p2{font-size:16px;color:var(--ink-70);max-width:44em;margin:12px 0 0}
.noon .punch{font-family:var(--serif);font-size:20px;margin:16px 0 0;color:var(--ink)}
.noon .cases b.big,.nums b.big{display:block;font-family:var(--serif);font-weight:400;font-size:44px;line-height:1;letter-spacing:-.03em;font-variation-settings:"opsz" 144;color:var(--ink);margin:6px 0 8px}
.noon .cases p,.nums p{font-size:14px;color:var(--ink-70);margin:0}
.tl{display:grid;gap:12px;margin-top:6px}
.tl .r{display:grid;grid-template-columns:190px 1fr;gap:14px;align-items:center}
.tl .r .nm{font-size:14px;color:var(--ink)} .tl .r .nm small{display:block;font:400 11px var(--mono);color:var(--ink-50);letter-spacing:.04em}
.tl .bar{position:relative;height:30px;background:var(--paper);border-radius:8px}
.tl .bar span{position:absolute;top:0;bottom:0;border-radius:8px;font:400 11px/30px var(--mono);color:#fff;padding-left:8px;white-space:nowrap;overflow:hidden}
.tl .ax{display:grid;grid-template-columns:190px 1fr;gap:14px} .tl .tk{position:relative;height:16px;font:400 11px var(--mono);color:var(--ink-50)} .tl .tk i{position:absolute;font-style:normal;transform:translateX(-50%)}
.tl .cap{font:400 11px var(--mono);color:var(--ink-50);margin-top:6px;letter-spacing:.02em}
.story-txt p{font-size:16px;line-height:1.75;color:var(--ink-70);max-width:44em;margin:0 0 14px}
.story-txt p.q{font-family:var(--serif);font-size:22px;line-height:1.45;color:var(--ink)}
.pv-hold{border:1px dashed var(--ink-30);border-radius:var(--r16);padding:16px 18px;font-size:14px;color:var(--ink-50)}
@media (max-width:800px){.tl .r,.tl .ax{grid-template-columns:1fr}.tl .ax>div:first-child{display:none}}
'''

HOME_NOON = '''  <div class="wrap rv noon" style="padding-top:70px">
    <div class="sec"><div class="hd"><h3 class="serif">为什么做这个</h3><span class="k">同一个正午</span></div>
      <p class="lead2">大模型，缺电。</p>
      <p class="p2">一边，风电和光伏的电越来越多地送不出去；另一边，大模型的调用量两年多涨了一千多倍，官方 API 开始在工作日高峰收两倍的价。电多的地方没有算，算缺的时候正是电多的时候。所以我们把算力搬到了电站旁边。</p>
      <p class="punch">它不等电来，它去电那里。</p>
      <div class="cases" style="margin-top:26px">
        <div class="case"><span class="k">2025 · 全国风电利用率</span><b class="big">94.3%</b><p>"十四五"以来首次与光伏一起跌破 95%。</p></div>
        <div class="case"><span class="k">2026 年初 · 青海弃光率</span><b class="big">21.3%</b><p>每五度光伏电，就有一度多送不出去。</p></div>
        <div class="case"><span class="k">2026-08 起 · 官方 API</span><b class="big">×2</b><p>头部模型厂商工作日高峰价是低谷的两倍。</p></div>
        <div class="case"><span class="k">2025 · 山东现货市场</span><b class="big">1500+ 小时</b><p>全年负电价时长，五一假期每天 8–16 点几乎都为负。</p></div>
      </div>
      <div class="board">
        <div class="tl">
          <div class="r"><div class="nm">官方 API 高峰价<small>头部模型厂商 · 工作日</small></div><div class="bar"><span style="left:37.5%;width:12.5%;background:var(--peak)">高峰 ×2</span><span style="left:58.33%;width:16.67%;background:var(--peak)">高峰 ×2</span></div></div>
          <div class="r"><div class="nm">限流集中时段<small>模型厂商公告 · 工作日</small></div><div class="bar"><span style="left:62.5%;width:12.5%;background:#7A6071">限流</span></div></div>
          <div class="r"><div class="nm">现货市场负电价<small>山东 · 2025 年五一</small></div><div class="bar"><span style="left:33.33%;width:33.33%;background:var(--accent-fill)">电价为负</span></div></div>
          <div class="ax"><div></div><div class="tk"><i style="left:0">0</i><i style="left:25%">6</i><i style="left:33.33%">8</i><i style="left:50%">12</i><i style="left:66.67%">16</i><i style="left:75%">18</i><i style="left:100%">24</i></div></div>
          <div class="cap">三条时段来自不同主体与日期，放在一起说明结构性重叠，不代表同一天的实测。来源：全国新能源消纳监测预警中心、新能源消纳月报、DeepSeek 官方价格页、厂商公告、山东电力现货市场公开报道。</div>
        </div>
      </div>
    </div>
  </div>
'''

HOME_NUMS = '''<div class="sec nums" style="margin-top:44px"><div class="hd"><h3 class="serif">几个数，看进度</h3><span class="k">截至 2026 年 9 月</span></div>
      <div class="steps4"><div><b class="big">83%+</b><p>订单金额来自海外客户</p></div><div><b class="big">20+</b><p>人的团队，来自清华、北大</p></div><div><b class="big">80%+</b><p>研发人员占比</p></div><div><b class="big">50+</b><p>论文、专利与软件著作权</p></div></div></div>
    '''

ABOUT_BLOCKS = '''    <h2 class="h2">我们的故事</h2>
    <div class="story-txt rv">
      <p class="q">栉风沐雨，登高万仞。沐仞的名字，来自去难去的地方，做难做的事。</p>
      <p>英文名 FathomPeak，从谷到峰：在电的低谷生产，在算力的高峰交付。logo 是一座山，也是一枚印章，盖在每一个从电站出发的词元上。</p>
      <p>我们做这件事，是因为看到了一个荒唐的正午：风电和光伏的电越来越多地送不出去，而同一时刻，大模型在排队、在涨价。把西北的电送到东部，要修几千公里的输电线；把一次推理的结果送到世界另一端，只要一根光纤。所以与其让电去找算力，不如让算力去找电。</p>
      <p>创始人路畅在清华大学读工学直博，研究的就是算电协同调度；他做过 AI 基础设施公司的 COO，也投过分布式光伏电站。团队来自清华大学、北京大学，横跨电机、计算机与经济金融。一半的人懂电，一半的人懂算。</p>
      <p>短期，我们把电站直供的大模型 API 交到国内外企业和开发者手里，让每一笔订单都带着产地。中长期，开放词元生产网络，让更多电站成为产地，再把调度跨到不同地区与时区：太阳在哪里，算力就在哪里。</p>
    </div>
    <h2 class="h2">价值观</h2>
    <div class="steps4 rv"><div><span class="k">01</span><b>登高万仞</b><p>难而对的事，先去现场。我们的机器在电站，不在 PPT 里。</p></div><div><span class="k">02</span><b>每个数字都有产地</b><p>说出口的，都查得到。查不到的，不说。</p></div><div><span class="k">03</span><b>双脚沾泥</b><p>电站比会议室重要。问题在现场解决。</p></div><div><span class="k">04</span><b>和客户算同一本账</b><p>价格、用量、电量都摊开。你看到的账，就是我们看到的账。</p></div></div>
    <h2 class="h2">路线图</h2>
    <div class="cards3 rv">
      <div class="card"><span class="k">01 · 现阶段</span><h3>产地</h3><p>电站直供的大模型 API：一体机进入风电与光伏场站，产地卡随订单交付。</p></div>
      <div class="card"><span class="k">02 · 开发中</span><h3>网络</h3><p>更多电站成为产地：开放第三方电站接入，跨站调度，让每一座电站都能把余电变成词元。</p></div>
      <div class="card"><span class="k">03 · 愿景</span><h3>潮汐</h3><p>太阳在哪里，算力就在哪里：跨地区、跨时区调度，让推理始终跑在最富余的绿电上。</p></div>
    </div>
    <h2 class="h2">认可与支持</h2>
    <div class="tbl rv"><table>
      <tr><td>资质</td><td>网信办词元出海批复，出海运营主体在广东汕头</td></tr>
      <tr><td>计划与机构</td><td>NVIDIA Inception 初创加速计划成员</td></tr>
      <tr><td>赛事</td><td>央视《赢在 AI+》智效跃迁赛道第一名；北京卫视《转在北京》智算纵横赛道第一名</td></tr>
      <tr><td>媒体</td><td>中央电视台、北京卫视报道；研究见刊《浦江科技评论》</td></tr>
      <tr><td>团队背景</td><td>清华大学、北京大学</td></tr>
    </table></div>
    <h2 class="h2">投资方</h2>
    <div class="pv-hold rv">【预览占位，合并前填好或删除】累计融资与投资方名单由公司提供。参考写法：累计融资 ××，投资方包括 ××、××。</div>
'''

NEW_EN = {
 "为什么做这个": "Why we do this", "同一个正午": "The same noon", "大模型，缺电。": "AI is short of power.",
 "一边，风电和光伏的电越来越多地送不出去；另一边，大模型的调用量两年多涨了一千多倍，官方 API 开始在工作日高峰收两倍的价。电多的地方没有算，算缺的时候正是电多的时候。所以我们把算力搬到了电站旁边。": "On one side, more and more wind and solar power can't reach the grid. On the other, model usage has grown over a thousandfold in two years and official APIs now charge double at weekday peaks. Where power is plentiful there is no compute, and compute runs short exactly when power is plentiful. So we moved compute to the power plant.",
 "它不等电来，它去电那里。": "It doesn't wait for power. It goes where the power is.",
 "2025 · 全国风电利用率": "2025 · National wind utilization", "\"十四五\"以来首次与光伏一起跌破 95%。": "Below 95% together with solar for the first time in the 14th Five-Year Plan period.",
 "2026 年初 · 青海弃光率": "Early 2026 · Qinghai solar curtailment", "每五度光伏电，就有一度多送不出去。": "More than one in five solar kWh can't be delivered.",
 "2026-08 起 · 官方 API": "Since Aug 2026 · Official API", "头部模型厂商工作日高峰价是低谷的两倍。": "A leading model vendor charges double at weekday peaks.",
 "2025 · 山东现货市场": "2025 · Shandong spot market", "1500+ 小时": "1,500+ hours", "全年负电价时长，五一假期每天 8–16 点几乎都为负。": "Hours of negative prices in a year; nearly every day 8:00–16:00 over the May holiday.",
 "官方 API 高峰价": "Official API peak price", "头部模型厂商 · 工作日": "Leading vendor · weekdays", "高峰 ×2": "Peak ×2", "限流集中时段": "Rate-limit window", "模型厂商公告 · 工作日": "Vendor notice · weekdays", "限流": "Throttled", "现货市场负电价": "Negative spot prices", "山东 · 2025 年五一": "Shandong · May 2025", "电价为负": "Negative price",
 "三条时段来自不同主体与日期，放在一起说明结构性重叠，不代表同一天的实测。来源：全国新能源消纳监测预警中心、新能源消纳月报、DeepSeek 官方价格页、厂商公告、山东电力现货市场公开报道。": "The three windows come from different sources and dates; together they show a structural overlap, not a single day's measurement. Sources: national renewable integration monitoring center, monthly integration reports, DeepSeek pricing page, vendor notices, public reports on Shandong's spot market.",
 "几个数，看进度": "A few numbers", "截至 2026 年 9 月": "As of Sep 2026", "订单金额来自海外客户": "of order value from overseas customers", "人的团队，来自清华、北大": "people, from Tsinghua and Peking University", "研发人员占比": "in R&D", "论文、专利与软件著作权": "papers, patents and software copyrights",
 "我们的故事": "Our story", "价值观": "Values", "路线图": "Roadmap", "认可与支持": "Recognition", "投资方": "Investors",
 "登高万仞": "Climb the high peak", "难而对的事，先去现场。我们的机器在电站，不在 PPT 里。": "For hard, right things, go to the site first. Our machines live at power plants, not in slides.",
 "每个数字都有产地": "Every number has an origin", "说出口的，都查得到。查不到的，不说。": "What we say can be checked. What can't be checked, we don't say.",
 "双脚沾泥": "Boots in the mud", "电站比会议室重要。问题在现场解决。": "The plant matters more than the meeting room. Problems get solved on site.",
 "和客户算同一本账": "One ledger with our customers", "价格、用量、电量都摊开。你看到的账，就是我们看到的账。": "Price, usage and energy are all on the table. The ledger you see is the one we see.",
 "01 · 现阶段": "01 · Now", "02 · 开发中": "02 · Building", "03 · 愿景": "03 · Vision", "产地": "Origin", "网络": "Network", "潮汐": "Tides",
 "电站直供的大模型 API：一体机进入风电与光伏场站，产地卡随订单交付。": "Model APIs direct from the plant: machines at wind and solar sites, an origin card with every order.",
 "更多电站成为产地：开放第三方电站接入，跨站调度，让每一座电站都能把余电变成词元。": "More plants become origins: third-party plants join, scheduling spans sites, and every plant can turn surplus power into tokens.",
 "太阳在哪里，算力就在哪里：跨地区、跨时区调度，让推理始终跑在最富余的绿电上。": "Wherever the sun is, the compute follows: scheduling across regions and time zones keeps inference on the most abundant green power.",
 "资质": "License", "网信办词元出海批复，出海运营主体在广东汕头": "CAC approval for cross-border token services; cross-border entity in Shantou, Guangdong",
 "计划与机构": "Programs", "NVIDIA Inception 初创加速计划成员": "Member of NVIDIA Inception",
 "赛事": "Competitions", "央视《赢在 AI+》智效跃迁赛道第一名；北京卫视《转在北京》智算纵横赛道第一名": "First place, CCTV \"Win in AI+\" efficiency track; first place, BRTV \"Transform in Beijing\" compute track",
 "媒体": "Media", "中央电视台、北京卫视报道；研究见刊《浦江科技评论》": "Featured by CCTV and BRTV; research published in Pujiang Science & Technology Review",
 "团队背景": "Team background", "清华大学、北京大学": "Tsinghua University, Peking University",
 "栉风沐雨，登高万仞。沐仞的名字，来自去难去的地方，做难做的事。": "Through wind and rain, up the high peak. Our name means going where it's hard to go and doing what's hard to do.",
 "英文名 FathomPeak，从谷到峰：在电的低谷生产，在算力的高峰交付。logo 是一座山，也是一枚印章，盖在每一个从电站出发的词元上。": "FathomPeak, from valley to peak: produced in power's valleys, delivered at compute's peaks. Our logo is a mountain and a seal, stamped on every token that leaves a power plant.",
 "我们做这件事，是因为看到了一个荒唐的正午：风电和光伏的电越来越多地送不出去，而同一时刻，大模型在排队、在涨价。把西北的电送到东部，要修几千公里的输电线；把一次推理的结果送到世界另一端，只要一根光纤。所以与其让电去找算力，不如让算力去找电。": "We started because of an absurd noon: more and more wind and solar power can't reach the grid, while at the same moment AI models queue and prices rise. Sending power from the northwest to the east takes thousands of kilometres of lines; sending an inference result across the world takes one fibre. So instead of moving power to compute, we move compute to power.",
 "创始人路畅在清华大学读工学直博，研究的就是算电协同调度；他做过 AI 基础设施公司的 COO，也投过分布式光伏电站。团队来自清华大学、北京大学，横跨电机、计算机与经济金融。一半的人懂电，一半的人懂算。": "Founder Lu Chang is a direct-PhD candidate in engineering at Tsinghua University researching compute-power co-scheduling; he was COO of an AI infrastructure company and has invested in distributed solar. The team comes from Tsinghua and Peking University across electrical engineering, computer science and economics. Half of us know power; half know compute.",
 "短期，我们把电站直供的大模型 API 交到国内外企业和开发者手里，让每一笔订单都带着产地。中长期，开放词元生产网络，让更多电站成为产地，再把调度跨到不同地区与时区：太阳在哪里，算力就在哪里。": "Near term, we put model APIs direct from the plant into the hands of companies and developers at home and abroad, with an origin on every order. Longer term, we open the token production network so more plants become origins, and schedule across regions and time zones: wherever the sun is, the compute follows.",
}

def main():
    out = open(SRC, encoding='utf8').read()
    for page, where, old, new, en, note in v4.R:
        assert out.count(old) == 1, where
        out = out.replace(old, new, 1)
    ins = [
        ('  <div class="feat">', HOME_NOON + '  <div class="feat">'),
        ('<div class="sec" style="margin-top:44px"><div class="hd"><h3 class="serif">为什么是沐仞</h3>', HOME_NUMS + '<div class="sec" style="margin-top:44px"><div class="hd"><h3 class="serif">为什么是沐仞</h3>'),
        ('    <h2 class="h2">公司</h2>', ABOUT_BLOCKS + '    <h2 class="h2">公司</h2>'),
        ('</style>', CSS + '</style>'),
    ]
    for a, b in ins:
        if out.count(a) != 1: sys.exit('[停止] 锚点不唯一：' + a[:40])
        out = out.replace(a, b, 1)
    en = {}
    for page, where, old, new, e, note in v4.R:
        if e: en[v4.text_only(new)] = e
    en.update(v4.EXTRA_EN); en.update(NEW_EN)
    key = 'var I18N={'
    out = out.replace(key, key + ''.join(json.dumps(k, ensure_ascii=False) + ':' + json.dumps(v, ensure_ascii=False) + ',' for k, v in en.items()), 1)
    open(OUT, 'w', encoding='utf8').write(out)
    print('preview ->', OUT, '|', len(v4.R), 'text replacements, 4 insertions,', len(en), 'EN entries')

if __name__ == '__main__':
    main()
