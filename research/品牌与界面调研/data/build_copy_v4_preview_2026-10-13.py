"""把品牌叙事页 v4 的文字嵌进现有官网原型：只换文字，不动结构、排版和内容结构。
原型文件不改；输出一份预览副本 + 一张新旧文案对照表。
用法：python3 -I build_copy_v4_preview_2026-10-13.py
"""
import html, json, os, sys

D = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(D, '..', 'demo', '沐仞官网原型_2026-10-12.html')
OUT = os.path.join(D, '..', 'demo', '沐仞官网原型_文案v4预览_2026-10-13.html')
CMP = os.path.join(D, '..', '..', '沐仞官网文案v4_新旧对照_2026-10-13.html')

# (页面, 位置, 旧, 新, 英文, 备注)
R = [
 # ---------- 首页 · 首屏 ----------
 ('首页', '首屏标题', '<p class="h">主流模型 <span class="x">×</span> 异构算力，一站式大模型 API 平台。</p>',
  '<p class="h">给大模型，一座电站。</p>', 'Give AI models a power plant.', ''),
 ('首页', '首屏第二行', '<p class="tag">低成本、高可用、全兼容。</p>',
  '<p class="tag">每一个词元，都有产地。</p>', 'Every token has an origin.', '商标需检索'),
 ('首页', '首屏说明', '<p class="h-sub">GLM、DeepSeek、Qwen、MiniMax 一个端点接入，兼容 OpenAI 与 Gemini 原生格式。一体机部署在电站旁，用富余绿电生产词元，为 AI 企业提供低成本、可追溯的推理服务。</p>',
  '<p class="h-sub">沐仞把大模型推理搬到风电和光伏电站旁边，用电网接不住的电生产词元。GLM、DeepSeek、Qwen、MiniMax 一个端点接入，兼容 OpenAI 与 Gemini 原生格式。</p>',
  'FathomPeak runs model inference right next to wind and solar plants, on power the grid can\'t take. GLM, DeepSeek, Qwen and MiniMax behind one endpoint, compatible with OpenAI and Gemini native formats.', ''),
 # ---------- 首页 · 三个核心能力 ----------
 ('首页', '核心能力 02 标题', '<b>不急的任务，跑在绿电便宜的地方</b>', '<b>价格，从电开始就低</b>', 'Priced from the power up', ''),
 ('首页', '核心能力 02 正文', '<p>价格按模型、调用规模、响应时延、并发需求和绿电来源计算。不赶时间的任务交给调度，迁到绿电更便宜、算力更空闲的节点去跑；要实时的，优先调到离你近的低延迟节点。</p>',
  '<p>算力就在电站旁，用的是电网接不住的电，成本从电开始就低。价格按模型、调用规模、响应时延、并发需求和绿电来源计算；不赶时间的任务，调度会排到电最多的时段和电站。</p>',
  'Our compute sits next to the plant and runs on power the grid can\'t take, so cost is low from the start. Price depends on model, volume, latency, concurrency and power source; batch work is scheduled to the hours and plants with the most power.', ''),
 ('首页', '核心能力 03 标题', '<b>每一笔订单，都查得到用的是哪座电站的电</b>', '<b>每一个词元，都查得到产地</b>', 'Every token, traceable to its plant', ''),
 ('首页', '核心能力 03 正文', '<p>订单和计算节点、运行时段、电力来源、能源消耗、词元产出关联在一起。做绿色采购、ESG 披露或跨境业务时，手里有一份可追溯的数据。</p>',
  '<p>每笔订单附一张产地卡：哪座电站、哪个时段、用了多少电、产出多少词元。做绿色采购、ESG 披露或跨境业务时，手里有一份可追溯的数据。</p>',
  'Every order carries an origin card: the plant, the hour, the energy used and the tokens produced. Traceable data for green procurement, ESG disclosure and cross-border business.', '产地卡上线时间待确认'),
 # ---------- 首页 · 为什么是沐仞 ----------
 ('首页', '为什么是沐仞 副标', '<span class="k">平台接单，基座调度，一体机生产。</span>', '<span class="k">换一家，就没有的东西。</span>', 'What you won\'t get anywhere else.', ''),
 ('首页', '为什么 01', '<b>高性价比</b><p>一体机部署在发电侧，用富余绿电生产词元；单机异构 GPU 混插，降低硬件投入和单位词元成本。</p>',
  '<b>产地价</b><p>别人的成本里是数据中心的工业电价，我们的成本里是电站侧最便宜的那一段电；单机异构 GPU 混插，再压一层硬件成本。</p>',
  None, ''),
 ('首页', '为什么 02', '<b>高可用</b><p>NetWeaver 把网络延迟变成可观测、可约束的调度变量；实时任务调到低延迟节点，非实时任务跟着绿电走。</p>',
  '<b>产地证</b><p>不是一句"绿色"，而是一张写着电站、时段和电量的卡。只有自己连着电站的人做得出来。</p>',
  None, ''),
 ('首页', '为什么 03', '<b>全兼容</b><p>主流模型一个端点，OpenAI 与 Gemini 原生请求格式原样兼容，改一行 base_url 即可接入。</p>',
  '<b>高峰时段，电正多</b><p>工作日白天是官方 API 的高峰，也是光伏出力最大的时候。别人缺的时候，正是我们电最多的时候。</p>',
  None, '不承诺"不分峰谷"，定价政策定了再改'),
 ('首页', '为什么 04', '<b>异构算力</b><p>不同品牌、型号的 GPU 由 Tapestrix 统一调度；调度架构已在工信部备案。</p>',
  '<b>持牌出海</b><p>出海运营主体持网信办词元出海批复，来数加工在境内合规处理，海外团队不必走中转。</p>',
  None, ''),
 ('首页', '为什么 05', '<b>可追溯与合规</b><p>每笔订单关联电站、时段与电力来源；出海运营主体持网信办词元出海批复。</p>',
  '<b>一个端点，全兼容</b><p>主流模型一个端点，OpenAI 与 Gemini 原生格式原样兼容；Tapestrix 统一调度不同型号的 GPU，调度架构已在工信部备案。</p>',
  None, ''),
 # ---------- 首页 · 收尾 ----------
 ('首页', '收尾大字', '<p class="display">准备好了吗？</p>', '<p class="display">这一代的智能，从电开始算。</p>', 'This generation of intelligence starts with power.', ''),
 # ---------- 关于沐仞 ----------
 ('关于', '页头说明', '<p>算电协同，词元出海。我们在发电侧把富余绿电就地变成词元，再通过一个平台卖给需要它的人。</p>',
  '<p>让每一度绿电，都算数。我们把大模型推理搬到风电和光伏电站旁边，用电网接不住的电生产词元，再通过一个平台交给需要它的人。太阳在哪里，算力就在哪里。</p>',
  'Make every green kilowatt-hour count. We run model inference next to wind and solar plants on power the grid can\'t take, and deliver the tokens through one platform. Wherever the sun is, the compute follows.', '使命与愿景放进现有页头'),
 ('关于', '卡片 1', '<span class="k">前店</span><h3>绿色词元交易平台</h3>', '<span class="k">平台</span><h3>电站直供的大模型 API</h3>', None, '对外不用"前店后厂"'),
 ('关于', '卡片 2', '<span class="k">后厂</span><h3>电站侧词元工厂</h3><p>一体机部署在电站旁，异构 GPU 混插；调度让计算跟着绿电走；每笔订单做能碳计量。</p>',
  '<span class="k">电站侧</span><h3>在电站旁生产词元</h3><p>一体机部署在风电与光伏场站，异构 GPU 混插；按刻钟预测电量与电价，把任务排到电最多的时段；每笔订单附产地卡。</p>',
  None, '对外不用"词元工厂"'),
 ('关于', '创始人', '<td>路畅，创始人兼 CEO，清华大学工学博士，研究方向为算电协同调度</td>',
  '<td>路畅，创始人兼 CEO，清华大学工学直博，研究方向为算电协同调度；曾任 AI 基础设施公司 COO，有分布式光伏电站投资经历</td>',
  None, '更正：BP 为直博在读，不写"博士"'),
 # ---------- 企业与出海 ----------
 ('企业与出海', '页头说明', '多出来的是发票、合同、子账号、专属报价，和一条合规的出海通道。</p>',
  '多出来的是发票、合同、子账号、专属报价，一条合规的出海通道，和每笔订单附带的产地卡。</p>', None, ''),
 ('企业与出海', '出海卡片标题', '<span class="k">词元出海</span><h3>海外客户</h3>', '<span class="k">词元出海</span><h3>合规地用上中国模型</h3>', 'Compliant access to Chinese models', ''),
 # ---------- 电站合作 ----------
 ('电站合作', '页头标题', '<h1 class="display">计算跟着绿电走</h1>', '<h1 class="display">搬电很贵，搬比特很便宜</h1>', 'Moving power is costly. Moving bits is cheap.', '避开媒体常用的"算力追着绿电跑"'),
 ('电站合作', '页头说明', '<p>一体机部署在电站旁，把富余绿电就地变成词元。下面是接入网络的电站和实时成交。</p>',
  '<p>所以我们把算力搬到电站旁边，把电网接不住的电就地变成词元。下面是已经成为词元产地的电站和实时成交。</p>',
  'So we move compute to the plant and turn power the grid can\'t take into tokens on site. Below are the plants already producing tokens, and live trades.', ''),
 ('电站合作', '合作区标题', '<h2 class="display">有富余绿电的电站，可以接入</h2>', '<h2 class="display">你的电站，可以是一个词元产地</h2>', 'Your plant can be a token origin', ''),
]


# 按单个元素补的英文（标题与正文分开的条目）
EXTRA_EN = {
 "产地价": "Origin price",
 "别人的成本里是数据中心的工业电价，我们的成本里是电站侧最便宜的那一段电；单机异构 GPU 混插，再压一层硬件成本。": "Others pay data-center industrial rates; we use the cheapest power at the plant itself, and mixed-GPU machines cut hardware cost further.",
 "产地证": "Origin proof",
 "不是一句\"绿色\"，而是一张写着电站、时段和电量的卡。只有自己连着电站的人做得出来。": "Not a claim of \"green\", but a card with the plant, the hour and the energy used. Only a company wired to the plant can issue it.",
 "高峰时段，电正多": "At peak hours, power is plentiful",
 "工作日白天是官方 API 的高峰，也是光伏出力最大的时候。别人缺的时候，正是我们电最多的时候。": "Weekday daytime is peak time for official APIs, and also when solar output is highest. When others run short, we have the most power.",
 "持牌出海": "Licensed for cross-border",
 "出海运营主体持网信办词元出海批复，来数加工在境内合规处理，海外团队不必走中转。": "Our cross-border entity holds a CAC token-export approval; data is processed compliantly in China, with no grey resellers in between.",
 "一个端点，全兼容": "One endpoint, fully compatible",
 "主流模型一个端点，OpenAI 与 Gemini 原生格式原样兼容；Tapestrix 统一调度不同型号的 GPU，调度架构已在工信部备案。": "Leading models behind one endpoint, compatible with OpenAI and Gemini native formats; Tapestrix schedules mixed GPUs, and the scheduler is filed with MIIT.",
 "平台": "Platform",
 "电站直供的大模型 API": "Model API, direct from the power plant",
 "电站侧": "At the plant",
 "在电站旁生产词元": "Tokens made at the plant",
 "一体机部署在风电与光伏场站，异构 GPU 混插；按刻钟预测电量与电价，把任务排到电最多的时段；每笔订单附产地卡。": "Integrated machines sit at wind and solar sites with mixed GPUs; power and price are forecast every 15 minutes and work is scheduled to the hours with the most power; every order carries an origin card.",
 "路畅，创始人兼 CEO，清华大学工学直博，研究方向为算电协同调度；曾任 AI 基础设施公司 COO，有分布式光伏电站投资经历": "Lu Chang, founder & CEO; direct-PhD candidate in engineering at Tsinghua University researching compute-power co-scheduling; former COO of an AI infrastructure company with experience investing in distributed solar.",
}

def text_only(s):
    import re
    return html.unescape(re.sub(r'<[^>]+>', '', s)).strip()

def main():
    src = open(SRC, encoding='utf8').read()
    out = src
    for page, where, old, new, en, note in R:
        n = out.count(old)
        if n != 1:
            sys.exit(f'[停止] {page}·{where}：原文出现 {n} 次，需要唯一匹配')
        out = out.replace(old, new, 1)
    # EN 字典：只追加新句，不改原有条目
    add = {}
    for page, where, old, new, en, note in R:
        if en:
            add[text_only(new)] = en
    add.update(EXTRA_EN)
    key = 'var I18N={'
    assert out.count(key) == 1, 'I18N 字典位置不唯一'
    pairs = ''.join(json.dumps(k, ensure_ascii=False) + ':' + json.dumps(v, ensure_ascii=False) + ',' for k, v in add.items())
    out = out.replace(key, key + pairs, 1)
    open(OUT, 'w', encoding='utf8').write(out)

    # 对照表
    rows = ''.join(
        f'<tr><td>{page}</td><td>{where}</td><td class="o">{html.escape(text_only(old))}</td><td class="n">{html.escape(text_only(new))}</td><td>{html.escape(note)}</td></tr>'
        for page, where, old, new, en, note in R)
    cmp = f'''<title>官网文案新旧对照</title>
<style>:root{{color-scheme:light}} body{{margin:0;background:#F8F8F8;font-family:"PingFang SC",-apple-system,sans-serif;color:#111;line-height:1.6}}
.w{{max-width:1180px;margin:0 auto;padding:32px 16px 60px}} h1{{font-size:26px;margin:0}} p{{color:#555;max-width:80ch}}
table{{border-collapse:collapse;width:100%;background:#fff;font-size:13.5px;margin-top:16px}} th,td{{text-align:left;padding:9px 10px;border-bottom:1px solid #e6e6e6;vertical-align:top}}
th{{background:#F3F1EA;color:#666;font-weight:500;font-size:12px}} td.o{{color:#888;text-decoration:line-through;text-decoration-color:#ccc;width:30%}} td.n{{color:#000;width:32%}}
ul{{color:#444}}</style>
<div class="w"><h1>官网文案 v4：新旧对照</h1>
<p>只换文字，结构、排版和内容区块都没动。预览文件：<code>品牌竞品调研_2026-10-12/demo/沐仞官网原型_文案v4预览_2026-10-13.html</code>；原型文件未修改。新句子已补进 EN 字典。共 {len(R)} 处。</p>
<table><tr><th>页面</th><th>位置</th><th>原文</th><th>新文</th><th>备注</th></tr>{rows}</table>
<h2 style="font-size:18px;margin-top:28px">现有结构里没有位置、这次没放进去的</h2>
<ul><li>品牌故事全文（"大模型，缺电"、名字由来、"一半的人懂电，一半的人懂算"）</li>
<li>四条价值观与路线图（产地 → 网络 → 潮汐）</li>
<li>"几个数，看进度"、认可与支持、投资方、创始人原话</li>
<li>"同一个正午"时间轴与三张事实卡</li></ul>
<p>这些需要新增区块才能放；要不要加、加在哪一页，等你看完这一版再定。</p></div>'''
    open(CMP, 'w', encoding='utf8').write(cmp)
    print('preview ->', OUT); print('compare ->', CMP); print(len(R), 'replacements,', len(add), 'EN entries')

if __name__ == '__main__':
    main()
