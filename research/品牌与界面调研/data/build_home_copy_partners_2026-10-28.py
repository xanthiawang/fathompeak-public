"""首页首屏文案、「为什么做这个」一节与合作方滚动带（Zixin 2026-10-28）。
第一轮：
 · 隆基删掉；滚动带右下角加一行不显眼的小字「部分合作方及客户」
 · 「免费试用 API」→「免费试用 Token」；「申请成为产地」→「电站申请合作」（首屏、页尾、底部浮条三处一起改）
 · 「低成本、高可用、全兼容。」→「更绿色、更便宜、同优质。」
 · 「GLM、DeepSeek、Qwen、MiniMax，兼容 OpenAI 与 Gemini。」→ 模型名后接「官方质量，低至 5 折。」
 · 「一体机部署在电站旁，用富余绿电生产词元，价低至 5 折。」→「将算力部署至分布式电站，余电变 Token，用中国电算服务全球 AI 用户。」
第二轮（Zixin：「给 5 折加粗。你搜索这些 logo 然后修改进去；…改为绿电冗余，Token 紧缺；所后面修改成…」，图上批注：
「token 高峰价」「不要交叉文字和图形」「删去吧？」）：
 · 首屏「5 折」加粗
 · 加星星充电、天津能源集团 logo（原图在预览目录 logo_sources/，见那里的 来源.md）；星星充电子品牌名单待确认，暂不加
 · 「大模型，缺电。」→「绿电冗余，Token 紧缺。」；段落「所以」后面改为「把部分推理任务调度到分布式的风、光、水电站里完成计算，便可实现分布式算电协同和城市边缘计算。」
 · 图表：「官方 API 高峰价」→「Token 高峰价」，结论胶囊同步；「电价为负」从斜线重叠区里移出，放在蓝条右侧空白处
 · 图下来源一行：收进「数据来源」折叠，默认不显示（两组时段来自不同来源，留着出处以备查）
第三轮（Zixin 截图批注）：
 · 「怎么用」02「价格，从电开始就低」：删掉「GLM-5.3 输出每百万词元 28 元 → 14 元」，「公开价」改「官网价」，前半句改写为
   「Token 用绿色余电生产，分布式节点更贴近 AI 需求发生的地方，在沐仞科技 Tapestrix 架构的加速下，单位 Token 成本大幅下降。」
 · 「行业与场景」：「词元出海」那张卡放到第一个位置
第四轮（Zixin：「写'万帮数字能源'，用百科的」）：
 · 万帮数字能源官网页头用的也是「StarCharge｜星星充电」logo，没有单独标识（百度百科要人机验证，打不开）→ 滚动带在星星充电后面加文字项「万帮数字能源」
 · 天津能源 logo 继续用维基百科那张
英文同步。
用法：python3 -I build_home_copy_partners_2026-10-28.py <站点根目录（含 index.html）> <logo 原图目录>
"""
import json, sys
from pathlib import Path
from PIL import Image

ROOT, SRC = Path(sys.argv[1]), Path(sys.argv[2])
p = ROOT / 'index.html'
s = p.read_text(encoding='utf8')
if 'class="marq-note"' in s: sys.exit('[停止] 已经改过')


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: sys.exit(f'[停止] 匹配 {c} 次（应为 {n}）：{old[:90]}')
    s = s.replace(old, new)


# ---- 合作方 logo：转灰度、保留透明底、裁掉四周空白、高 80px（与现有 art/logos 一致） ----
LOGOS = {'starcharge': '星星充电_官网中文横版_zhongwenLogo.png', 'tianjin-energy': '天津能源集团_维基百科_TJE_logo.png'}
for key, name in LOGOS.items():
    f = SRC / name
    if not f.exists(): sys.exit(f'[停止] 找不到 logo 原图 {f}')
    im = Image.open(f).convert('RGBA')
    im = im.crop(im.getchannel('A').getbbox())
    gray = Image.merge('LA', (im.convert('L'), im.getchannel('A')))
    gray = gray.resize((round(gray.width * 80 / gray.height), 80), Image.LANCZOS)
    gray.save(ROOT / 'art' / 'logos' / f'{key}.png', optimize=True)
    print('logo', key, gray.size)

# ---- 首屏 ----
rep('<p class="tagline">低成本、高可用、全兼容。</p>', '<p class="tagline">更绿色、更便宜、同优质。</p>')
# 「5 折」之间是不换行空格（ ），站点原文和英文字典的键都这样写
rep('<p class="sub">GLM、DeepSeek、Qwen、MiniMax，兼容 OpenAI 与 Gemini。<br>一体机部署在电站旁，用富余绿电生产词元，价低至 5 折。</p>',
    '<p class="sub">GLM、DeepSeek、Qwen、MiniMax，官方质量，低至 <b>5 折</b>。<br>将算力部署至分布式电站，余电变 Token，用中国电算服务全球 AI 用户。</p>')
rep('<a class="btn black" href="#start">免费试用 API ↓</a><a class="btn glass" href="#network">申请成为产地 →</a>',
    '<a class="btn black" href="#start">免费试用 Token ↓</a><a class="btn glass" href="#network">电站申请合作 →</a>', 2)
rep('<a class="btn black" href="#start" tabindex="-1">免费试用 API →</a>', '<a class="btn black" href="#start" tabindex="-1">免费试用 Token →</a>')

# ---- 合作方滚动带：删隆基，加星星充电、天津能源（首页 LOGOS 与旧版 PARTNERS 两份名单） ----
rep("var LOGOS=['longi','stategrid',", "var LOGOS=['stategrid','tianjin-energy','starcharge','t:万帮数字能源',")
rep("{i:'longi',t:'隆基'},", "{i:'tianjin-energy',t:'天津能源'},{i:'starcharge',t:'星星充电'},{t:'万帮数字能源'},")
# 滚动带支持文字项（「t:」开头），字体与灰度和 logo 一致
rep("""var mh=LOGOS.map(function(n){return '<img src="art/logos/'+n+'.png" alt="">'}).join('');""",
    """var mh=LOGOS.map(function(n){return n.indexOf('t:')===0?'<span class="mq-t">'+n.slice(2)+'</span>':'<img src="art/logos/'+n+'.png" alt="">'}).join('');""")
rep('<div class="marq" aria-label="合作伙伴"><div class="tr" id="marq"></div></div>',
    '<div class="marq" aria-label="部分合作方及客户"><div class="tr" id="marq"></div></div>\n<p class="marq-note">部分合作方及客户</p>')

# ---- 为什么做这个 ----
rep('<span class="k">为什么做这个</span><h2>大模型，缺电。</h2>', '<span class="k">为什么做这个</span><h2>绿电冗余，Token 紧缺。</h2>')
rep('<br>我们觉得这不该是常态。所以把算力搬到了电站旁边。</p></div>',
    '<br>我们觉得这不该是常态。所以把部分推理任务调度到分布式的风、光、水电站里完成计算，便可实现分布式算电协同和城市边缘计算。</p></div>')
rep('<div class="nm">官方 API 高峰价<small>', '<div class="nm">Token 高峰价<small>')
rep('<span>官方 API 最贵的时候，电站的电最便宜</span>', '<span>Token 最贵的时候，电站的电最便宜</span>')
# 「电价为负」不再压在斜线重叠区上：蓝条里不放字，标签放在蓝条右侧的空白处
rep('<span class="seg ng" style="left:33.33%;width:33.33%">电价为负</span><span class="ov" style="left:37.5%;width:12.5%"></span><span class="ov" style="left:58.33%;width:8.34%"></span></div>',
    '<span class="seg ng" style="left:33.33%;width:33.33%"></span><span class="ov" style="left:37.5%;width:12.5%"></span><span class="ov" style="left:58.33%;width:8.34%"></span><span class="ng-l" style="left:calc(66.67% + 10px)">电价为负</span></div>')
rep('<div class="cap">高峰价：DeepSeek 官方价格页，2026-08 起。负电价：山东现货市场，2025 年五一假期。两组时段来自不同来源，用于说明重叠。</div>',
    '<details class="cap-src"><summary>数据来源</summary><p class="cap">高峰价：DeepSeek 官方价格页，2026-08 起。负电价：山东现货市场，2025 年五一假期。两组时段来自不同来源，用于说明重叠。</p></details>')

# ---- 怎么用 02：价格（正文与英文字典键同步；「5 折」「28 元」等之间是不换行空格） ----
OLD02 = '词元用电站富余的绿电生产，成本更低。企业报价低至公开价 5 折：GLM-5.3 输出每百万词元 28 元 → 14 元。'
NEW02 = 'Token 用绿色余电生产，分布式节点更贴近 AI 需求发生的地方，在沐仞科技 Tapestrix 架构的加速下，单位 Token 成本大幅下降。企业报价低至官网价 5 折。'
rep(f'<p>{OLD02}</p>', f'<p>{NEW02}</p>')
rep(f'"{OLD02}":"Tokens are made with surplus green power at the plant, so they cost less. Enterprise quotes go as low as 50% of the public price: GLM-5.3 output drops from ¥28 to ¥14 per million tokens."',
    f'"{NEW02}":"Tokens are made with surplus green power, and distributed nodes sit closer to where AI demand arises. Accelerated by FathomPeak’s Tapestrix architecture, the cost per token drops sharply. Enterprise quotes go as low as 50% of the official price."')

# ---- 行业与场景：「词元出海」放第一 ----
EXP = "    ['词元出海','来数加工在境内合规处理，出海运营主体持网信办词元出海批复，海外团队合规调用中国模型。','','#5284D7'],\n"
rep(EXP, '')
rep('var IND=[\n', 'var IND=[\n' + EXP)

rep('</head>', '<style id="home-copy-20261028">\n'
    '/* 首页文案与合作方（2026-10-28）。站点主样式在 body 里、晚于本段，选择器加 #home2 前缀 */\n'
    '#home2 .sub b{font-weight:600;color:inherit}\n'
    '#home2 .marq .mq-t{display:block;height:26px;line-height:26px;font:500 18px/26px var(--serif);letter-spacing:.06em;color:var(--ink);opacity:.62;white-space:nowrap}\n'
    '#home2 .marq-note{margin:-10px 0 0;padding:0 clamp(16px,4vw,48px) 8px;text-align:right;font:400 11px/1.4 var(--sans);letter-spacing:.08em;color:var(--ink);opacity:.32;pointer-events:none}\n'
    '#home2 .lane .ng-l{position:absolute;top:0;bottom:0;display:flex;align-items:center;font-size:12px;font-weight:500;color:var(--blue-2);white-space:nowrap}\n'
    '#home2 .cap-src{margin-top:12px;text-align:right}\n'
    '#home2 .cap-src summary{display:inline-block;list-style:none;cursor:pointer;font-size:12px;color:var(--ink-50);text-decoration:underline;text-decoration-color:var(--line);text-underline-offset:3px}\n'
    '#home2 .cap-src summary::-webkit-details-marker{display:none}\n'
    '#home2 .cap-src .cap{margin:8px 0 0;text-align:left}\n'
    '</style>\n</head>')

EN = {
    '更绿色、更便宜、同优质。': 'Greener. Cheaper. Same quality.',
    'GLM、DeepSeek、Qwen、MiniMax，官方质量，低至': 'GLM, DeepSeek, Qwen and MiniMax at official quality, up to',
    '5 折': '50% off',
    '。': '.',
    '将算力部署至分布式电站，余电变 Token，用中国电算服务全球 AI 用户。': 'We put compute at distributed power plants, turn surplus power into tokens, and serve AI users worldwide with power and compute from China.',
    '免费试用 Token ↓': 'Try tokens free ↓',
    '免费试用 Token →': 'Try tokens free →',
    '电站申请合作 →': 'Power plants: partner with us →',
    '部分合作方及客户': 'Selected partners and customers',
    '万帮数字能源': 'Wanbang Digital Energy',
    '绿电冗余，Token 紧缺。': 'Surplus green power. Scarce tokens.',
    '我们觉得这不该是常态。所以把部分推理任务调度到分布式的风、光、水电站里完成计算，便可实现分布式算电协同和城市边缘计算。': 'We don’t think it should stay this way. So we route part of the inference workload to distributed wind, solar and hydro plants, enabling distributed power–compute coordination and edge computing in cities.',
    'Token 高峰价': 'Token peak price',
    'Token 最贵的时候，电站的电最便宜': 'When tokens cost the most, plant power costs the least',
    '数据来源': 'Sources',
}
rep('  syncAuthLocale(); applyLang();', '  (function(S){for(var k in S) if(!(k in I18N)) I18N[k]=S[k]})(' + json.dumps(EN, ensure_ascii=False) + ');  /* 首页文案与合作方 */\n  syncAuthLocale(); applyLang();')

p.write_text(s, encoding='utf8')
print('done')
