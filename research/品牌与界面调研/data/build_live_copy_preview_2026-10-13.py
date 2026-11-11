"""在线上最新版（xanthiawang/fathompeak-site 的 index.html）上套用品牌文案，输出本地预览，不提交、不推送。
保留不改：首页首屏（标题、第二行、说明、产品窗、按钮）与首页结尾 CTA（"从一次真实任务测试开始"）。
其余按 v7 的品牌文案改：首页新增"为什么做这个"+ 高峰价 / 电价对比卡；核心能力 02、03 正文；为什么是沐仞五条；
关于页 页头、两张卡、故事 / 价值观 / 路线图 / 认可与支持 / 投资方占位、公司表格三行；企业页一句与出海卡标题；电站页标题、说明与合作区标题。
用法：python3 -I build_live_copy_preview_2026-10-13.py <线上仓库副本目录>
"""
import json, os, re, sys, html, importlib.util

D = os.path.dirname(os.path.abspath(__file__))
def load(name, fn):
    spec = importlib.util.spec_from_file_location(name, os.path.join(D, fn)); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
v4 = load('v4', 'build_copy_v4_preview_2026-10-13.py')
v5 = load('v5', 'build_copy_v5_preview_2026-10-13.py')
v7 = load('v7', 'build_copy_v7_preview_2026-10-13.py')

REPO = sys.argv[1] if len(sys.argv) > 1 else os.path.join(D, '..', '..', '官网线上版副本_2026-10-13')
SRC = os.path.join(REPO, 'index.html')
OUT = os.path.join(REPO, 'index_品牌文案预览_2026-10-13.html')
CMP = os.path.join(D, '..', '..', '官网线上版_品牌文案改动对照_2026-10-13.html')

# (页面, 位置, 线上原文, 新文, 英文)
R = [
 ('首页', '核心能力 02 正文',
  '<p>将任务时限、并发需求与绿电供给一起纳入调度，优先匹配成本和交付条件合适的节点。平台主要面向非实时或弱实时推理；低延迟需求需先测试并确认服务条件。</p>',
  '<p>算力就在电站旁，用的是电网接不住的电，成本从电开始就低。价格按模型、调用规模、响应时延、并发需求和绿电来源计算；不赶时间的任务，调度会排到电最多的时段和电站。</p>', None),
 ('首页', '核心能力 03 正文',
  '<p>按订单关联计算节点、运行时段与能源信息，便于追溯和对账。绿电及减排数据应有来源和核算口径；是否可用于披露或采购证明，需按具体要求核验。</p>',
  '<p>每笔订单附一张产地卡：哪座电站、哪个时段、用了多少电、产出多少词元。做绿色采购、ESG 披露或跨境业务时，手里有一份可追溯的数据。</p>', None),
 ('首页', '为什么是沐仞 副标', '<span class="k">模型服务与算电协同产品</span>', '<span class="k">换一家，就没有的东西。</span>', None),
 ('首页', '为什么 01', '<b>成本优化</b><p>结合绿电供给、设备配置与任务需求优化推理成本。实际节省需在相同任务和服务条件下比较。</p>',
  '<b>产地价</b><p>别人的成本里是数据中心的工业电价，我们的成本里是电站侧最便宜的那一段电；单机异构 GPU 混插，再压一层硬件成本。</p>', None),
 ('首页', '为什么 02', '<b>协同调度</b><p>将网络时延、算力状态与任务时限纳入调度；服务可用率与响应要求按具体测试和协议确认。</p>',
  '<b>产地证</b><p>不是一句"绿色"，而是一张写着电站、时段和电量的卡。只有自己连着电站的人做得出来。</p>', None),
 ('首页', '为什么 03', '<b>统一接入</b><p>提供统一模型接入，减少接口配置与管理工作；各模型的请求格式、工具调用和流式能力需按文档验证。</p>',
  '<b>高峰时段，电正多</b><p>工作日白天是官方 API 的高峰，也是光伏出力最大的时候。别人缺的时候，正是我们电最多的时候。</p>', None),
 ('首页', '为什么 04', '<b>异构算力</b><p>通过 Tapestrix 管理异构计算资源，结合设备适配与推理测试选择配置；具体支持的芯片和模型以方案为准。</p>',
  '<b>持牌出海</b><p>出海运营主体持网信办词元出海批复，来数加工在境内合规处理，海外团队不必走中转。</p>', None),
 ('首页', '为什么 05', '<b>追溯与服务核验</b><p>关联订单与能源记录，便于业务追溯；跨境服务的资质、数据流向与适用范围在签约前逐项确认。</p>',
  '<b>一个端点，全兼容</b><p>主流模型一个端点，OpenAI 与 Gemini 原生格式原样兼容；Tapestrix 统一调度不同型号的 GPU，调度架构已在工信部备案。</p>', None),
 ('关于', '页头说明', '<p>沐仞科技连接 AI 计算需求与能源侧算力，提供模型服务、算电协同调度及推理设备，探索以富余绿电支撑计算的新路径。</p>',
  '<p>让每一度绿电，都算数。我们把大模型推理搬到风电和光伏电站旁边，用电网接不住的电生产词元，再通过一个平台交给需要它的人。太阳在哪里，算力就在哪里。</p>',
  'Make every green kilowatt-hour count. We run model inference next to wind and solar plants on power the grid can\'t take, and deliver the tokens through one platform. Wherever the sun is, the compute follows.'),
 ('关于', '卡片 1', '<span class="k">模型服务</span><h3>绿色词元交易平台</h3>', '<span class="k">平台</span><h3>电站直供的大模型 API</h3>', None),
 ('关于', '卡片 2', '<span class="k">场站算力</span><h3>场站侧推理节点</h3><p>在场站或机房部署推理设备，结合电力与资源状态安排任务，并建立运行与能源记录。</p>',
  '<span class="k">电站侧</span><h3>在电站旁生产词元</h3><p>一体机部署在风电与光伏场站，异构 GPU 混插；按刻钟预测电量与电价，把任务排到电最多的时段；每笔订单附产地卡。</p>', None),
 ('关于', '创始人', '<td>路畅，创始人兼 CEO，清华大学工学直博生，研究方向为算电协同调度</td></tr>',
  '<td>路畅，创始人兼 CEO，清华大学工学直博生，研究方向为算电协同调度；曾任 AI 基础设施公司 COO，有分布式光伏电站投资经历</td></tr>\n      <tr><td>团队</td><td>20 余人，研发人员占 80% 以上，来自清华大学、北京大学</td></tr>\n      <tr><td>海外业务</td><td>订单金额 83% 以上来自海外客户</td></tr>\n      <tr><td>研究成果</td><td>论文、专利与软件著作权 50 余项</td></tr>', None),
 ('企业', '页头说明', '再安排测试、报价与采购。海外服务另行确认适用范围。</p>',
  '再安排测试、报价与采购。每笔订单附一张产地卡，记录电站、时段与用电量。海外服务另行确认适用范围。</p>', None),
 ('企业', '出海卡片标题', '<span class="k">词元出海</span><h3>海外客户</h3>', '<span class="k">词元出海</span><h3>合规地用上中国模型</h3>', 'Compliant access to Chinese models'),
 ('电站', '页头标题', '<h1 class="display">让能源与算力协同运行</h1>', '<h1 class="display">搬电很贵，搬比特很便宜</h1>', 'Moving power is costly. Moving bits is cheap.'),
 ('电站', '页头说明', '<p>在适合的场站部署推理设备，结合电力供给安排计算任务。下方展示节点与交易界面，实际接入状态及业务记录需按平台数据核对。</p>',
  '<p>所以我们把算力搬到电站旁边，把电网接不住的电就地变成词元。下方展示节点与交易界面，实际接入状态及业务记录需按平台数据核对。</p>',
  'So we move compute to the plant and turn power the grid can\'t take into tokens on site. Below are nodes and a trading view; actual connection status and records should be checked against platform data.'),
 ('电站', '合作区标题', '<h2 class="display">评估场站条件，洽谈节点合作</h2>', '<h2 class="display">你的电站，可以是一个词元产地</h2>', 'Your plant can be a token origin'),
]

EXTRA_EN = {
 "算力就在电站旁，用的是电网接不住的电，成本从电开始就低。价格按模型、调用规模、响应时延、并发需求和绿电来源计算；不赶时间的任务，调度会排到电最多的时段和电站。": "Our compute sits next to the plant and runs on power the grid can't take, so cost is low from the start. Price depends on model, volume, latency, concurrency and power source; batch work is scheduled to the hours and plants with the most power.",
 "每笔订单附一张产地卡：哪座电站、哪个时段、用了多少电、产出多少词元。做绿色采购、ESG 披露或跨境业务时，手里有一份可追溯的数据。": "Every order carries an origin card: the plant, the hour, the energy used and the tokens produced. Traceable data for green procurement, ESG disclosure and cross-border business.",
 "换一家，就没有的东西。": "What you won't get anywhere else.",
 "路畅，创始人兼 CEO，清华大学工学直博生，研究方向为算电协同调度；曾任 AI 基础设施公司 COO，有分布式光伏电站投资经历": "Lu Chang, founder & CEO; direct-PhD candidate in engineering at Tsinghua University researching compute-power co-scheduling; former COO of an AI infrastructure company with experience investing in distributed solar.",
}

def text_only(s):
    return html.unescape(re.sub(r'<[^>]+>', '', s)).strip()

def main():
    src = open(SRC, encoding='utf8').read()
    hero_before = src[src.index('<div class="hero">'):src.index('<div class="partners">')]
    end_before = src[src.index('<div class="cta-end rv">'):src.index('</section>', src.index('<div class="cta-end rv">'))]
    out = src
    for page, where, old, new, en in R:
        n = out.count(old)
        if n != 1: sys.exit(f'[停止] {page}·{where}：线上原文出现 {n} 次')
        out = out.replace(old, new, 1)
    for a, b in [('  <div class="feat">', v7.HOME_WHY + '  <div class="feat">'),
                 ('    <h2 class="h2">公司</h2>', v7.ABOUT_BLOCKS + '    <h2 class="h2">公司</h2>'),
                 ('</style>', v7.CSS + '</style>')]:
        if out.count(a) != 1: sys.exit('[停止] 锚点不唯一：' + a[:40])
        out = out.replace(a, b, 1)
    # 保护：首屏与结尾 CTA 必须逐字不变
    assert out[out.index('<div class="hero">'):out.index('<div class="partners">')] == hero_before, '首屏被改动'
    assert out[out.index('<div class="cta-end rv">'):out.index('</section>', out.index('<div class="cta-end rv">'))] == end_before, '结尾 CTA 被改动'
    en = {}
    for page, where, old, new, e in R:
        if e: en[text_only(new)] = e
    for d in (v4.EXTRA_EN, v5.NEW_EN, v7.NEW_EN, EXTRA_EN):
        en.update(d)
    key = 'var I18N={'
    out = out.replace(key, key + ''.join(json.dumps(k, ensure_ascii=False) + ':' + json.dumps(v, ensure_ascii=False) + ',' for k, v in en.items()), 1)
    open(OUT, 'w', encoding='utf8').write(out)

    rows = ''.join(f'<tr><td>{p}</td><td>{w}</td><td class="o">{html.escape(text_only(o))}</td><td class="n">{html.escape(text_only(n))}</td></tr>' for p, w, o, n, e in R)
    adds = ('<tr><td>首页</td><td>新增 · 为什么做这个</td><td class="o">（无）</td><td class="n">大模型，缺电。风电和光伏的电，越来越多地送不出去；同一时刻，大模型在排队、在涨价。电多的地方没有算，算缺的时候正是电多的时候。我们觉得这不该是常态。所以把算力搬到了电站旁边。＋ 高峰价 / 电价对比卡</td></tr>'
            '<tr><td>关于</td><td>新增 · 我们的故事 / 价值观 / 路线图 / 认可与支持 / 投资方</td><td class="o">（无）</td><td class="n">见预览；投资方为虚线占位，上线前填好或删除</td></tr>')
    cmp = f'''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>线上版品牌文案改动</title>
<style>:root{{color-scheme:light}} body{{margin:0;background:#F8F8F8;font-family:"PingFang SC",-apple-system,sans-serif;color:#111;line-height:1.6}} .w{{max-width:1180px;margin:0 auto;padding:32px 16px 60px}}
h1{{font-size:24px;margin:0}} p{{color:#555;max-width:86ch}} table{{border-collapse:collapse;width:100%;background:#fff;font-size:13.5px;margin-top:14px}} th,td{{text-align:left;padding:9px 10px;border-bottom:1px solid #e6e6e6;vertical-align:top}}
th{{background:#F3F1EA;color:#666;font-weight:500;font-size:12px}} td.o{{color:#888;width:36%}} td.n{{color:#000;width:40%}} .warn{{background:#FBEFEA;border-left:3px solid #9A3B1E;padding:10px 14px;margin-top:14px;color:#333}}</style>
<div class="w"><h1>线上版（2026-10-13 19:28）套用品牌文案：改动对照</h1>
<p>基于仓库 main 最新提交生成本地预览，未提交、未推送。首页首屏与结尾"从一次真实任务测试开始"逐字保留（脚本已断言未变）。</p>
<div class="warn"><b>请特别看这几处：</b>线上版的核心能力 02、03 正文和"为什么是沐仞"五条，是另一会话刻意改成的谨慎写法（带"以确认为准""需核验"等限定）。这次按你的要求换成了品牌文案，限定语随之去掉。其中"每笔订单附一张产地卡""高峰时段，电正多""调度架构已在工信部备案"属于对外承诺，产地卡上线、定价政策与备案材料确认前，建议保留线上的谨慎版。</div>
<table><tr><th>页面</th><th>位置</th><th>线上原文</th><th>改为</th></tr>{rows}{adds}</table></div>'''
    open(CMP, 'w', encoding='utf8').write(cmp)
    print('preview ->', OUT); print('compare ->', CMP); print(len(R), 'replacements')

if __name__ == '__main__':
    main()
