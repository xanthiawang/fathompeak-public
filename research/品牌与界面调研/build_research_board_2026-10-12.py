"""Build the visual competitor research board: every captured screenshot with source URL, date, palette, fonts and observations.
Outputs: 竞品调研图文板_2026-10-12.html (+ board_assets/*.jpg) and the same as PDF via headless Chrome.
Usage: python3 -I build_research_board_2026-10-12.py <research_dir>"""
import html, json, os, subprocess, sys
from importlib import util
import fitz

R = sys.argv[1]
A = os.path.join(R, 'board_assets'); os.makedirs(A, exist_ok=True)
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
DATE = '2026-10-12'
spec = util.spec_from_file_location('cd', os.path.join(R, 'data', 'color_distance_2026-10-12.py'))
cd = util.module_from_spec(spec); spec.loader.exec_module(cd)

def load(*parts):
    f = os.path.join(R, *parts)
    return json.load(open(f)) if os.path.exists(f) else {}
STY = {'data': load('data', 'extracted_styles.json'), 'ux': load('ux', 'extracted_styles.json'), 'ux_home': load('ux_home', 'extracted_styles.json'),
       'mobile': load('mobile', 'extracted_styles.json'), 'mobile2': load('mobile2', 'extracted_styles.json'), 'extra': load('extra', 'extracted_styles.json')}

def jpg(folder, key, scale, suffix='', top_frac=1.0):
    """Downscale (and crop to the top part of) a captured PNG to a JPEG in board_assets; returns relative path or None.
    Desktop captures are 2400px tall and mobile 2200px (CSS px); the board shows the top portion so pages stay compact."""
    src = os.path.join(R, folder, f'{key}_long.png')
    if not os.path.exists(src):
        src = os.path.join(R, folder, f'{key}.png')
        if not os.path.exists(src): return None
    out = f'board_assets/{folder}_{key}{suffix}.jpg'
    dst = os.path.join(R, out)
    if not os.path.exists(dst):
        d = fitz.open(src); p = d[0]; r = p.rect
        clip = fitz.Rect(0, 0, r.width, r.height * top_frac)
        p.get_pixmap(matrix=fitz.Matrix(scale, scale), clip=clip).save(dst, jpg_quality=82)
    return out

def meta(folder, key):
    return STY.get(folder, {}).get(key, {})

# ---- competitor definitions: (id, name, category, url, palette, fonts, shots, observations)
# shots: list of (caption, folder, key, kind)  kind: 'd' desktop, 'm' mobile
SITES = [
    dict(id='fp', name='沐仞科技（现网）', cat='自身 · 词元交易平台', url='fathompeak.cn / admin.fathompeak.cn',
         pal=['#2563EB', '#06B6D4', '#10B981', '#3EA4EC', '#0F172A', '#F4F6FB'], fonts='Inter（首页 iframe）/ Public Sans（外壳）',
         shots=[('首页（iframe 内容）', 'data', '00b_fathompeak_home_iframe', 'd'), ('首页外壳 fathompeak.cn', 'data', '00_fathompeak_cn', 'd'),
                ('模型市场 admin.fathompeak.cn/token-market', 'ux', 'fp_market', 'd'), ('控制台入口 admin.fathompeak.cn', 'ux', 'fp_admin', 'd'),
                ('手机端首页', 'mobile', 'fp_home', 'm'), ('手机端模型市场', 'mobile', 'fp_market', 'm')],
         obs=['首页标题写"没有中间商赚差价的绿色词元交易平台"，与 BP 第 26 页"不拼裸词元价格"的策略相反。',
              '外壳用 #3EA4EC（Public Sans），首页 iframe 用 Tailwind 默认蓝 #2563EB（Inter），两套都不是品牌规范 V1。',
              '导航 8 项，其中"节点定价、节点评价、发起任务、融合智慧算网中枢"是供给侧概念。',
              '模型卡片只有一个"市场价"，价格藏在"选择此模型获取特价"之后；筛选只有 全部 / Chat / Reasoning。',
              '手机端首页只剩导航和页脚，iframe 内容未渲染（390px iPhone 模拟，待真机复核）。',
              '"实时词元交易看板"（电站 × 模型 × 均价 × 减排）是所有竞品都没有的元素。']),
    dict(id='sf', name='硅基流动 SiliconFlow', cat='API 平台（国内）', url='siliconflow.cn',
         pal=['#6C28F6', '#743AED', '#36384A', '#F1F1FF', '#1E293B'], fonts='Roboto + 系统中文字体',
         shots=[('首页', 'data', '01_siliconflow', 'd'), ('模型中心 /models', 'ux', 'sf_models', 'd'), ('价格 /pricing', 'ux', 'sf_pricing', 'd'),
                ('文档 docs.siliconflow.cn', 'ux', 'sf_docs', 'd'), ('登录页 account.siliconflow.cn', 'extra', 'sf_signup', 'd'),
                ('手机端首页', 'mobile', 'sf_home', 'm'), ('手机端模型中心', 'mobile', 'sf_models', 'm')],
         obs=['首屏是轮播 banner，主推"硅基流动上线 ×× 模型"；紫色 #6C28F6 为主色，深色产品卡片带线框几何纹理。',
              '模型中心：卡片网格，含厂商 logo、发布日期、长描述、能力图标、上下文与参数量；筛选有模型类型 + 20 个应用场景标签。',
              '价格页：按厂商分组的表格，输入 / 输出 / 缓存三列，部分模型按"费用发生时段"分价（9–18 点与其他时段）。',
              '文档为 Mintlify 风格：左目录、⌘K 搜索、实名认证等常见问题在"功能特性"下。',
              '"TokenPlus 词元优选"是其 Token 调度产品名，"词元"一词已被使用。']),
    dict(id='ppio', name='PPIO 派欧云', cat='算力聚合 + 模型 API', url='ppio.com',
         pal=['#1161FE', '#0E58EA', '#E9F1FF', '#F7F8FA', '#181818'], fonts='系统字体（PingFang / 微软雅黑）',
         shots=[('首页', 'data', '02_ppio', 'd'), ('LLM Playground /llm', 'ux', 'ppio_models', 'd'), ('价格 /pricing', 'ux', 'ppio_pricing', 'd'),
                ('文档 /docs', 'ux', 'ppio_docs', 'd'), ('手机端首页', 'mobile', 'ppio_home', 'm'), ('手机端价格', 'mobile', 'ppio_pricing', 'm')],
         obs=['首屏轮播"PPIO 上线 Kimi K3 / DeepSeek-V4"，3D 玻璃立方体插画，顶部有"安装 Skills"命令行条。',
              '主色 #1161FE 与沐仞现网主蓝 #2563EB 色差 ΔE 2.2，与规范 V1 亮蓝 #176BFA 色差 3.4。',
              '价格页：14 张表格，按厂商分组，输入 / Cache Read / 输出三列，每行有"在线体验"。',
              '模型页直接是 Playground：左侧参数面板、右侧对话；首页标语"面向 Agent 时代打造 Token 工厂"。',
              '手机端正常，筛选 chip 横向滚动。']),
    dict(id='infini', name='无问芯穹 Infinigence', cat='异构算力优化 + MaaS', url='infini-ai.com',
         pal=['#5D2BFE', '#000000', '#FFFFFF', '#333333'], fonts='PingFang SC',
         shots=[('首页', 'data', '03_infini', 'd'), ('首页（第二次抓取，含 Cookie 弹窗关闭后）', 'ux', 'infini_cloud', 'd'), ('手机端首页', 'mobile2', 'infini_home', 'm')],
         obs=['黑底紫光等轴测芯片城市插画；首页有 11 段视频、203 组 CSS 动画、354 张图片，是本次最重的页面。',
              '定位语"通用人工智能基础设施服务商"，导航里有"Token工厂"。',
              '首页有强制 Cookie 同意弹窗；面向企业，无公开定价页。']),
    dict(id='ds', name='DeepSeek 开放平台', cat='官方 API（参照）', url='platform.deepseek.com',
         pal=['#121519', '#3B82F6', '#FFFFFF', '#0F1115'], fonts='Inter / Montserrat',
         shots=[('开放平台登录页', 'data', '09_deepseek_platform', 'd'), ('模型 & 价格 api-docs.deepseek.com', 'ux', 'ds_pricing', 'd'), ('手机端价格页', 'mobile2', 'ds_pricing', 'm')],
         obs=['平台首页即登录页：左侧蓝灰渐变插画 + 右侧表单，极简。',
              '价格页按"空闲时段 / 高峰时段"分价，高峰为空闲的 2 倍（输入未命中 1 元 vs 2 元，输出 4 元 vs 8 元，deepseek-flash）。',
              '这说明"按时段定价"用户已经能理解，是沐仞"高峰平价"的直接对照基准。']),
    dict(id='zhipu', name='智谱 BigModel', cat='官方 API（参照）', url='open.bigmodel.cn',
         pal=['#131212', '#FFFFFF', '#F5F5F5'], fonts='MiSans',
         shots=[('首页', 'extra', 'zhipu_home', 'd'), ('定价 /pricing', 'ux', 'zhipu_pricing', 'd'), ('手机端定价', 'mobile', 'zhipu_pricing', 'm')],
         obs=['定价页用大卡片展示旗舰模型（上下文、输入 / 输出单价、缓存命中），下方有"有什么不清楚的，随时问我"的问答机器人。',
              '黑白为主，几乎不用彩色；按钮为黑色实心。']),
    dict(id='kimi', name='Kimi 开放平台（Moonshot）', cat='官方 API（参照）', url='platform.moonshot.cn',
         pal=['#000000', '#FFFFFF'], fonts='Inter',
         shots=[('首页', 'extra', 'moonshot_home', 'd'), ('模型推理价格 /docs/pricing/chat', 'ux', 'moonshot_pricing', 'd'), ('手机端价格页', 'mobile2', 'moonshot_pricing', 'm')],
         obs=['价格文档：按 K3 / K2 系列分表，列出缓存写入（5min / 1h）、缓存命中、未命中、输出、上下文。',
              '文档为 Mintlify 风格，带"复制页面"与"提出问题"。']),
    dict(id='or', name='OpenRouter', cat='API 聚合（海外）', url='openrouter.ai',
         pal=['#7624F4', '#FCFCFE', '#03080A', '#035ADE'], fonts='Plus Jakarta Sans / Gordita',
         shots=[('首页', 'data', '04_openrouter', 'd'), ('模型列表 /models', 'ux', 'or_models', 'd'), ('文档 Quickstart', 'ux', 'or_docs', 'd'),
                ('登录页 /sign-in', 'extra', 'or_signin', 'd'), ('手机端首页', 'mobile', 'or_home', 'm'), ('手机端模型列表', 'mobile', 'or_models', 'm')],
         obs=['首屏无插画：一句定位 + 两个按钮（Get API Key / Discover Models）+ 四个规模数字（600T+ tokens、10M+ users、80+ providers、500+ models）。',
              '模型列表可在列表 / 表格之间切换，左侧 12 组筛选（模态、价格、上下文、Zero data retention 等），每行显示 Token 用量和输入 / 输出价。',
              '文档第一屏就是可复制的 curl；手机端把筛选收进 Filter 按钮，列表仍可读。',
              '主色紫 #7624F4，只用于主按钮；页面几乎没有动画。']),
    dict(id='tg', name='Together AI', cat='AI 云（海外）', url='together.ai',
         pal=['#000000', '#010120', '#FC4C02', '#CAAEF5', '#EF2CC1', '#C8F6F9'], fonts='The Future + PP Neue Montreal Mono',
         shots=[('首页', 'data', '05_together', 'd'), ('模型库 /models', 'ux', 'tg_models', 'd'), ('定价 /pricing', 'ux', 'tg_pricing', 'd'), ('手机端首页', 'mobile2', 'tg_home', 'm')],
         obs=['彩色 3D 抽象几何 + 等宽小标签，GSAP 动效，321 张图片。',
              '模型库卡片：名称 + Cached / Input / Output 三个价格 + 部署方式标签（SERVERLESS / DEDICATED）。',
              '定价页是 18 张可筛选的表，按 Chat / Vision / Image / Audio 等切换，单位 per 1M tokens。']),
    dict(id='crusoe', name='Crusoe', cat='能源资产延伸型 AI 云', url='crusoe.ai',
         pal=['#000000', '#CEEB13', '#323C2A', '#ECF0E9'], fonts='Suisse Intl + ABC Diatype Mono',
         shots=[('首页', 'data', '06_crusoe', 'd'), ('定价 /cloud/pricing', 'ux', 'crusoe_pricing', 'd'), ('手机端首页', 'mobile', 'crusoe_home', 'm')],
         obs=['黑底机房实拍 + 荧光黄绿 #CEEB13 色块，等宽大标题"The AI factory company"。',
              '首页有 7 段视频、3 个 canvas、GSAP；图片 alt 显示用了等轴测线稿（微电网、园区、机架）。',
              '定价页把 GPU 实例、托管推理、微调分开列，GPU 按小时计价。']),
    dict(id='emerald', name='Emerald AI', cat='算电协同软件型', url='emeraldai.co',
         pal=['#253023', '#50594F', '#438C36', '#F6F6F7'], fonts='DM Sans + Crimson Pro（衬线）',
         shots=[('首页', 'data', '07_emerald', 'd'), ('手机端首页', 'mobile2', 'emerald_home', 'm')],
         obs=['数据中心航拍实景，衬线斜体大标题"Power for AI. Flexibility for the Grid."',
              '深绿 #253023 + 鲜绿 #438C36；首页以新闻卡片（TechCrunch、WEF）建立可信度；无产品定价页。']),
    dict(id='soluna', name='Soluna', cat='绿电数据中心', url='solunacomputing.com',
         pal=['#231F20', '#CB5727', '#783518', '#FFFFFF'], fonts='Nunito Sans',
         shots=[('首页', 'data', '08_soluna', 'd'), ('手机端首页', 'mobile2', 'soluna_home', 'm')],
         obs=['风机航拍 + 锈橙 #CB5727 / 炭黑分区；标语"Renewable Computing"。',
              '按受众分导航：For Power Producers / For AI / For Bitcoin / For Investors；规模数字以 MW 计。']),
]

e = html.escape
css = """
body{margin:0;font-family:"PingFang SC","Hiragino Sans GB",-apple-system,sans-serif;color:#102A43;background:#fff}
.wrap{max-width:1180px;margin:0 auto;padding:40px 24px 80px}
h1{font-size:30px;margin:0 0 6px} h2{font-size:22px;margin:0;display:flex;gap:12px;align-items:baseline;flex-wrap:wrap}
h2 small{font-size:13px;color:#475569;font-weight:400}
.meta{color:#475569;font-size:13px;margin:4px 0 18px}
section{border-top:1px solid #CBD5E1;padding-top:26px;margin-top:34px;page-break-before:always}
section.first{border-top:0;margin-top:0;page-break-before:auto}
.info{display:flex;gap:26px;flex-wrap:wrap;align-items:flex-start;margin:10px 0 16px}
.sw{display:flex;gap:8px;flex-wrap:wrap} .sw span{font:11px/1.2 ui-monospace,Menlo,monospace;color:#475569;text-align:center}
.sw i{display:block;width:56px;height:30px;border:1px solid #CBD5E1;border-radius:3px;margin-bottom:3px}
.kv{font-size:13px;color:#475569} .kv b{color:#102A43;font-weight:500}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
figure{margin:0;page-break-inside:avoid} figure img{width:100%;height:auto;display:block;border:1px solid #CBD5E1;border-radius:4px}
.grid figure img{max-height:700px;object-fit:cover;object-position:top} .mob figure img{max-height:600px;object-fit:cover;object-position:top}
figcaption{font-size:12px;color:#475569;margin-top:6px} figcaption b{color:#102A43;font-weight:500}
.mob{display:flex;gap:16px;flex-wrap:wrap;margin-top:18px;align-items:flex-start}
.mob figure{width:190px} .mob figure img{border-radius:14px}
@media (max-width:760px){ .grid,.thumbs{grid-template-columns:1fr 1fr} .mob figure{width:46%} }
.obs{margin:16px 0 0;padding-left:20px;font-size:14px;line-height:1.6} .obs li{margin-bottom:4px}
.thumbs{display:grid;grid-template-columns:repeat(4,1fr);gap:12px} .thumbs figure img{aspect-ratio:1440/900;object-fit:cover;object-position:top}
table{border-collapse:collapse;font-size:13px;width:100%} td,th{padding:8px 10px;border-bottom:1px solid #E2E8F0;text-align:left;vertical-align:top}
th{color:#475569;font-weight:500} .chip{display:inline-block;width:40px;height:22px;border:1px solid #CBD5E1;vertical-align:middle;margin-right:6px}
.bad{color:#B91C1C;font-weight:600} .mid{color:#B45309} .ok{color:#047857}
.note{font-size:13px;color:#475569}
@media print{ @page{size:1754px 1240px;margin:36px} .wrap{max-width:1680px;padding:0} section{page-break-before:always} }
"""
out = [f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>沐仞竞品调研图文板</title><style>{css}</style></head><body><div class="wrap">']

# ---- overview
out.append(f'<section class="first"><h1>沐仞科技｜竞品官网、模型市场、定价、文档与手机端图文板</h1>'
           f'<p class="meta">采集：{DATE}，无头 Chrome。桌面 1440×900 视口，截图为首页起 2400px 高；手机端为 390×844 iPhone 模拟，截图为 2200px 高。'
           f'每张图下方标注页面与地址。原始 PNG 与页面样式数据（颜色、字体、导航、CTA、表单、动画数量、脚本库）在 data/、ux/、ux_home/、mobile/、mobile2/、extra/ 文件夹。</p>')
out.append('<h2>首页总览</h2><div class="thumbs">')
for s in SITES:
    cap, folder, key, kind = s['shots'][0]
    p = jpg(folder, key, 0.83)
    if p: out.append(f'<figure><img src="{p}" alt="{e(s["name"])}"><figcaption><b>{e(s["name"])}</b> · {e(s["url"])}</figcaption></figure>')
out.append('</div>')
out.append('<h2 style="margin-top:28px">一页看完的结论</h2><ol class="obs">'
           '<li><b>国内 AI 平台视觉同质</b>：紫或科技蓝 + 3D 玻璃 / 等轴测插画 + "新模型上线"轮播（硅基流动、PPIO、无问芯穹）。</li>'
           '<li><b>海外开发者平台用数据当图形</b>：OpenRouter 的规模数字与模型列表、Together 的价格大表，几乎不用插画和轮播。</li>'
           '<li><b>能源 + AI 公司用实景 + 大地色</b>：Crusoe 荧光黄绿、Emerald 深绿、Soluna 锈橙，机房、电站、风机实拍，衬线或等宽字体。</li>'
           '<li><b>定价全行业公开</b>，单位 ¥ 或 $ / 百万 Token，输入 / 输出 / 缓存三列；DeepSeek 与硅基流动已按时段分价。沐仞现网不公开价格。</li>'
           '<li><b>沐仞的蓝撞色</b>：现网 #2563EB 与 PPIO #1161FE 色差 2.2；规范 V1 亮蓝 #176BFA 色差 3.4。能源青 #169FB0 距所有竞品主色 > 25。</li>'
           '<li><b>沐仞手机端首页空白</b>（iframe 未渲染，待真机复核）；导航 8 项含供给侧概念；"Token 工厂 / 词元"已被 PPIO、无问芯穹、硅基流动使用。</li>'
           '</ol></section>')

# ---- per site
for s in SITES:
    out.append(f'<section><h2>{e(s["name"])} <small>{e(s["cat"])} · {e(s["url"])} · 采集 {DATE}</small></h2>')
    sw = ''.join(f'<span><i style="background:{c}"></i>{c}</span>' for c in s['pal'])
    hero = ''
    for cap, folder, key, kind in s['shots']:
        m = meta(folder, key)
        if m.get('h1') or m.get('heroText'):
            hero = (m.get('h1') or [m.get('heroText')])
            hero = hero[0] if isinstance(hero, list) else hero
            break
    out.append(f'<div class="info"><div class="sw">{sw}</div><div class="kv"><b>字体</b> {e(s["fonts"])}<br><b>首屏文案</b> {e(str(hero)[:80]) if hero else "—"}</div></div>')
    desk = [x for x in s['shots'] if x[3] == 'd']; mob = [x for x in s['shots'] if x[3] == 'm']
    out.append('<div class="grid">')
    for cap, folder, key, kind in desk:
        p = jpg(folder, key, 0.83, suffix='_top', top_frac=0.67)
        m = meta(folder, key); url = m.get('url', '')
        if p: out.append(f'<figure><img src="{p}" alt="{e(cap)}"><figcaption><b>{e(cap)}</b><br>{e(url)}</figcaption></figure>')
        else: out.append(f'<figure><figcaption><b>{e(cap)}</b><br>（本次未抓到）</figcaption></figure>')
    out.append('</div>')
    if mob:
        out.append('<div class="mob">')
        for cap, folder, key, kind in mob:
            p = jpg(folder, key, 0.42, top_frac=0.6)
            m = meta(folder, key); url = m.get('url', '')
            if p: out.append(f'<figure><img src="{p}" alt="{e(cap)}"><figcaption><b>{e(cap)}</b><br>{e(url)}</figcaption></figure>')
            else: out.append(f'<figure><figcaption><b>{e(cap)}</b><br>（本次未抓到）</figcaption></figure>')
        out.append('</div>')
    out.append('<ul class="obs">' + ''.join(f'<li>{e(o)}</li>' for o in s['obs']) + '</ul></section>')

# ---- mobile side by side
out.append('<section><h2>手机端横向对比 <small>390px iPhone 模拟 · 首页或模型 / 定价页</small></h2><div class="mob">')
for folder, key, cap in [('mobile', 'fp_home', '沐仞 首页'), ('mobile', 'fp_market', '沐仞 模型市场'), ('mobile', 'sf_home', '硅基流动 首页'), ('mobile', 'sf_models', '硅基流动 模型中心'),
                         ('mobile', 'ppio_home', 'PPIO 首页'), ('mobile', 'ppio_pricing', 'PPIO 价格'), ('mobile', 'or_home', 'OpenRouter 首页'), ('mobile', 'or_models', 'OpenRouter 模型'),
                         ('mobile', 'zhipu_pricing', '智谱 定价'), ('mobile2', 'ds_pricing', 'DeepSeek 价格'), ('mobile2', 'moonshot_pricing', 'Kimi 价格'), ('mobile2', 'tg_home', 'Together 首页'),
                         ('mobile2', 'infini_home', '无问芯穹 首页'), ('mobile', 'crusoe_home', 'Crusoe 首页'), ('mobile2', 'emerald_home', 'Emerald 首页'), ('mobile2', 'soluna_home', 'Soluna 首页')]:
    p = jpg(folder, key, 0.42, top_frac=0.6)
    if p: out.append(f'<figure><img src="{p}" alt="{e(cap)}"><figcaption><b>{e(cap)}</b></figcaption></figure>')
out.append('</div></section>')

# ---- UX structure table
out.append('<section><h2>UX 结构对比 <small>导航 · 首屏主 CTA · 模型页形态 · 定价页 · 文档</small></h2><table><tr><th>品牌</th><th>一级导航</th><th>首屏主 CTA</th><th>模型页</th><th>定价页</th><th>文档</th></tr>')
rows = [
    ('沐仞现网', '主页 · 控制台 · 文档 · 模型市场 · 节点定价 · 节点评价 · 发起任务 · 融合智慧算网中枢', '立即询价购算 / 浏览模型市场', '卡片网格；单一"市场价"，点击"获取特价"', '无公开定价页', '未抓到有效内容'),
    ('硅基流动', '产品 · 模型 · 价格 · 文档 · 生态合作', '登录 / 立即试用', '卡片网格，20 个场景标签筛选', '按厂商分组表格，部分按时段分价', 'Mintlify 风格，⌘K'),
    ('PPIO', '模型服务 · Agent 云 · GPU 云 · 边缘云 · 新闻 · 关于', '立即注册', 'Playground 优先', '14 张表，输入 / Cache / 输出', 'Mintlify 风格'),
    ('OpenRouter', 'Models · Benchmarks · Chat · Rankings · Apps · Pricing · Docs', 'Get API Key', '列表 / 表格切换，12 组筛选', '模型页即价格', 'Quickstart 首屏为 curl'),
    ('Together', 'Inference · Compute · Model Shaping · Research · Developers · Pricing', 'Start building', '卡片，三个价格 + 部署标签', '18 张可筛选表', '—'),
    ('DeepSeek', '快速开始 · API 指南 · API 文档', '登录', '—', '空闲 / 高峰分价，高峰 2 倍', 'Docusaurus'),
    ('智谱', '研究 · 产品 · 文档 · 体验 · 定价 · 支持', '登录 / 注册', '—', '旗舰模型大卡片 + 问答机器人', '—'),
    ('Crusoe', 'Cloud · Pricing · AI Infrastructure · About · Resources', 'Get started / Contact sales', '—', 'GPU 按小时，推理按 Token', '—'),
]
for r in rows: out.append('<tr>' + ''.join(f'<td>{e(c)}</td>' for c in r) + '</tr>')
out.append('</table></section>')

# ---- color distance
rows = []
for n, c in cd.ours.items():
    dist, cn, cc = min((cd.de2000(c, v), k, v) for k, v in cd.competitors.items())
    cls = 'bad' if dist < 5 else 'mid' if dist < 15 else 'ok'
    rows.append(f'<tr><td><span class="chip" style="background:{c}"></span>{e(n)} {c}</td><td><span class="chip" style="background:{cc}"></span>{e(cn)} {cc}</td><td class="{cls}">ΔE {dist:.1f}</td></tr>')
out.append('<section><h2>色彩重合度 <small>CIEDE2000；ΔE 小于 5 并排也难区分，大于 25 可视为不同色区</small></h2><table><tr><th>沐仞用色</th><th>最接近的竞品色</th><th>色差</th></tr>' + ''.join(rows) + '</table>'
           '<p class="note">竞品色值来自各站 CSS 变量或主按钮的计算样式（data/extracted_styles.json）。</p></section>')

out.append('</div></body></html>')
out_html = os.path.join(R, '竞品调研图文板_2026-10-12.html')
open(out_html, 'w').write('\n'.join(out))
# artifact variant: same page without the document skeleton (the Artifact tool wraps it)
body = '\n'.join(out).split('<body>', 1)[1].replace('</body></html>', '')
open(os.path.join(R, '竞品调研图文板_artifact.html'), 'w').write(f'<title>沐仞竞品调研图文板</title>\n<style>{css}</style>\n{body}')
out_pdf = os.path.join(R, '竞品调研图文板_2026-10-12.pdf')
subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-pdf-header-footer', '--virtual-time-budget=20000', f'--print-to-pdf={out_pdf}', 'file://' + out_html],
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
print(out_html); print(out_pdf); print(len(os.listdir(A)), 'assets')
