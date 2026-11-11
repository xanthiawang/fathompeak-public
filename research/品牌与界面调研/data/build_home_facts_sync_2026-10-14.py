"""把首页重设计原型里已确认的文案同步到线上站首页，版式沿用线上现有设计（不搬原型的版式）。
1 项目案例：只写《企业信息表》支持的事实，分"客户与订单""电站合作"两组，每卡底部写状态（已签约 / 已签战略协议 / 初步合作意向…）；
  删掉无出处或夸大的"南亚 1GW""广东 8MW""正在推进技术验证"。
2 行业与场景第一行的客户说明：删"AI for Science 独角兽""头部大厂跨境电商图文审核"（前者仅 BP，后者仅在价格谈判），改为已签约客户 + 战略合作。
3 怎么用三步小字：01 列出主流模型与兼容格式（去掉"再切业务流量"）；02 给出折扣（报价单 2026-10-08：GLM-5.3 刊例 28 → 折后 14 元/百万词元）；
  03 标题改为强调绿电。
4 结尾：大标题改为"让电站的富余绿电，跑你的 AI。"，原"从一次真实任务测试开始"降为副句（Zixin 2026-10-14 同意改动此处）。
首屏 HTML 逐字不变。所有新文案补英文。
用法：python3 -I build_home_facts_sync_2026-10-14.py <仓库目录>
"""
import json, os, sys

P = os.path.join(sys.argv[1], 'index.html')
s = open(P, encoding='utf8').read()
hero0 = s[s.index('<div class="hero">'):s.index('<div class="partners">')]
NB = ' '  # 不换行空格：防止"14 元""5 折"被拆到两行


def home_bounds():
    a = s.index('<section data-route="home"')
    return a, s.index('<section data-route=', a + 10)


def rep_home(old, new):
    """只在首页 section 内替换，且必须恰好命中一次。"""
    global s
    a, b = home_bounds()
    c = s[a:b].count(old)
    if c != 1: sys.exit(f'[停止] 首页内匹配 {c} 次（应为 1）：{old[:60]}')
    s = s[:a] + s[a:b].replace(old, new) + s[b:]


# 1 项目案例
a, b = home_bounds()
h = s[a:b]
i0 = h.index('<div class="hh rv"><span class="k">试点与推进中项目</span><h2>项目案例</h2></div>')
tail = '<p>节点运行与订单级能源计量关联记录。</p></div>\n      </div>'
i1 = h.index(tail, i0) + len(tail)
old_cases = h[i0:i1]
for w in ('南亚 1GW', '广东 · 8MW', '正在推进技术验证', '天津 · 分布式光伏'):
    assert w in old_cases, f'项目案例旧内容缺少 {w}'


def card(k, t, p, st):
    return f'        <div class="case"><span class="k">{k}</span><b>{t}</b><p>{p}</p><span class="cst">{st}</span></div>\n'


CASES = [
    ('客户与订单', [
        ('词元出海 · 新加坡', '5,000 万元海外词元采购合同', '与某新加坡客户签署。', '已签约'),
        ('AI 模型推理', '1,000 万元推理服务协议', '与某清华系 AI 企业签署，覆盖 Qwen、GLM、Gemma 等开源模型。', '已签约'),
        ('社交与情感陪伴', '某头部社交平台', '绿色词元供应、大模型推理优化与一体机部署。', '已达成战略合作'),
        ('订单总量', '已签词元订单超 6,000 万元', '截至 2026 年第三季度，其中海外订单占比超 83%。', '已签约'),
    ]),
    ('电站合作', [
        ('集中式光伏 · 河北', '某能源国企 100MW 光伏电站', '拟作为首个集中式光伏算电协同试点。', '已签战略协议 · 技术方案设计中'),
        ('分布式光伏 · 20 个城市', '某新能源企业 35 座光伏电站', '合计约 100MW，拟开放用于部署词元一体机。', '已签战略协议'),
        ('海上风电 · 汕头', '海上风电直连海上算力中心', '拟与某上市公司共同推进。', '已达成战略合作'),
        ('集中式光伏 · 老挝', '1GW 光伏项目算电协同试点', '已与项目方就试点方案深入沟通。', '初步合作意向'),
    ]),
]
new_cases = '<div class="hh rv"><span class="k">合作与订单</span><h2>项目案例</h2></div>\n'
for g, cards in CASES:
    new_cases += f'      <div class="cgh">{g}</div>\n      <div class="cases">\n' + ''.join(card(*c) for c in cards) + '      </div>\n'
new_cases = new_cases.rstrip('\n')
s = s[:a] + h[:i0] + new_cases + h[i1:] + s[b:]

# 2 行业与场景第一行
rep_home('已有词元采购客户包括某 AI for Science 独角兽、某全球头部社交平台，以及某头部大厂的跨境电商图文审核。',
         '已签约客户包括某新加坡客户与某清华系 AI 企业；与某头部社交平台已达成战略合作。')

# 3 怎么用三步
P1 = '一行地址，接入 GLM、DeepSeek、Qwen、MiniMax 等主流模型；OpenAI 与 Gemini 调用格式都兼容。'
P2 = f'词元用电站富余的绿电生产，成本更低。企业报价低至公开价 5{NB}折：GLM-5.3 输出每百万词元 28{NB}元{NB}→{NB}14{NB}元。'
T3 = '绿电从哪来，每一单都查得到'
P3 = '每笔订单一张产地卡：哪座光伏、风电或水电站，哪个时段，用了多少绿电，可用于 ESG 披露与绿色采购。'
rep_home('配置接入地址、API Key 和模型名称，用一条真实任务检查返回格式与流式输出，通过后切换业务流量。', P1)
rep_home('价格按模型、调用规模、响应时延、并发需求和绿电来源计算；公开价在模型市场查看，企业用量可以按量报价。', P2)
rep_home('<b>每一个词元，都查得到产地</b>', f'<b>{T3}</b>')
rep_home('每笔订单附一张产地卡：哪座电站、哪个时段、用了多少电、产出多少词元。做绿色采购、ESG 披露或跨境业务时，手里有一份可追溯的数据。', P3)

# 4 结尾
END = '让电站的富余绿电，跑你的 AI。'
rep_home('<p class="display">从一次真实任务测试开始</p>',
         f'<p class="display end-line">{END}</p><p class="end-sub">从一次真实任务测试开始</p>')

CSS = '''
/* 首页项目案例两组 + 每卡状态；结尾副句（2026-10-14 按企业信息表核实后同步） */
.cgh{margin:34px 0 12px;font-family:var(--mono);font-weight:400;font-size:11px;letter-spacing:.08em;color:var(--ink-50)}
.hh+.cgh{margin-top:0}
.case{display:flex;flex-direction:column}
.case p{margin-bottom:12px}
.case .cst{margin-top:auto;font-family:var(--mono);font-weight:400;font-size:11px;letter-spacing:.08em;color:var(--ink-50)}
.cta-end .end-line{font-feature-settings:"halt";word-break:keep-all}
.cta-end .end-sub{margin:-6px 0 24px;font-size:17px;color:var(--ink-70)}
@media (max-width:800px){.cta-end .end-sub{font-size:15px}}
'''
k = s.rindex('</style>')
s = s[:k] + CSS + s[k:]

EN = {
    "合作与订单": "Partnerships and orders", "客户与订单": "Customers and orders", "电站合作": "Power plant partnerships",
    "词元出海 · 新加坡": "Tokens overseas · Singapore", "5,000 万元海外词元采购合同": "RMB 50 million overseas token purchase contract",
    "与某新加坡客户签署。": "Signed with a customer in Singapore.", "已签约": "Signed",
    "AI 模型推理": "AI model inference", "1,000 万元推理服务协议": "RMB 10 million inference service agreement",
    "与某清华系 AI 企业签署，覆盖 Qwen、GLM、Gemma 等开源模型。": "Signed with a Tsinghua-affiliated AI company; covers open models including Qwen, GLM and Gemma.",
    "某头部社交平台": "A leading social platform",
    "绿色词元供应、大模型推理优化与一体机部署。": "Green token supply, model inference optimization and appliance deployment.",
    "已达成战略合作": "Strategic partnership agreed", "订单总量": "Total orders",
    "已签词元订单超 6,000 万元": "Over RMB 60 million in signed token orders",
    "截至 2026 年第三季度，其中海外订单占比超 83%。": "As of Q3 2026; overseas orders make up over 83%.",
    "集中式光伏 · 河北": "Utility-scale solar · Hebei", "某能源国企 100MW 光伏电站": "A state-owned energy group's 100MW solar plant",
    "拟作为首个集中式光伏算电协同试点。": "Planned as the first utility-scale solar compute–power pilot.",
    "已签战略协议 · 技术方案设计中": "Strategic agreement signed · technical design in progress",
    "分布式光伏 · 20 个城市": "Distributed solar · 20 cities", "某新能源企业 35 座光伏电站": "35 solar plants of a renewable energy company",
    "合计约 100MW，拟开放用于部署词元一体机。": "About 100MW in total, to be opened for token appliance deployment.",
    "已签战略协议": "Strategic agreement signed", "海上风电 · 汕头": "Offshore wind · Shantou",
    "海上风电直连海上算力中心": "Offshore wind powering an offshore compute center directly",
    "拟与某上市公司共同推进。": "To be developed jointly with a listed company.",
    "集中式光伏 · 老挝": "Utility-scale solar · Laos", "1GW 光伏项目算电协同试点": "Compute–power pilot at a 1GW solar project",
    "已与项目方就试点方案深入沟通。": "Pilot plan discussed in depth with the project owner.", "初步合作意向": "Preliminary intent to cooperate",
    "已签约客户包括某新加坡客户与某清华系 AI 企业；与某头部社交平台已达成战略合作。":
        "Signed customers include a customer in Singapore and a Tsinghua-affiliated AI company; a strategic partnership is in place with a leading social platform.",
    P1: "One address connects you to leading models including GLM, DeepSeek, Qwen and MiniMax; OpenAI and Gemini request formats both work.",
    P2: "Tokens are made with surplus green power at the plant, so they cost less. Enterprise quotes go as low as 50% of the public price: GLM-5.3 output drops from ¥28 to ¥14 per million tokens.",
    T3: "Where the green power came from, on every order",
    P3: "Every order comes with an origin card: which solar, wind or hydro plant, which time window and how much green power — ready for ESG reporting and green procurement.",
    END: "Let surplus green power run your AI.",
}
k2 = s.index('var I18N={') + len('var I18N={')
s = s[:k2] + ''.join(json.dumps(x, ensure_ascii=False) + ':' + json.dumps(y, ensure_ascii=False) + ',' for x, y in EN.items()) + s[k2:]

assert s[s.index('<div class="hero">'):s.index('<div class="partners">')] == hero0, '首屏 HTML 被改动'
open(P, 'w', encoding='utf8').write(s)
print('done.')
