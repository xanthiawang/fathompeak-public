"""Build the competitor brand board (HTML -> PDF via headless Chrome) from screenshots + extracted_styles.json.
Data captured 2026-10-12 with headless Chrome (1440x900 viewport). Usage: python3 -I build_board_2026-10-12.py <research_dir>"""
import html, json, os, subprocess, sys
from importlib import util

R = sys.argv[1]
D = os.path.join(R, 'data')
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

spec = util.spec_from_file_location('cd', os.path.join(D, 'color_distance_2026-10-12.py'))
cd = util.module_from_spec(spec); spec.loader.exec_module(cd)

SITES = [  # key, name, category, swatches (curated from extracted_styles.json), fonts, visual notes (observed on screenshots)
    ('00b_fathompeak_home_iframe', '沐仞科技（现网 fathompeak.cn）', '自身', ['#2563EB', '#06B6D4', '#10B981', '#3EA4EC', '#0F172A', '#F4F6FB'], 'Inter（首页）/ Public Sans（外壳）', '白底；蓝到绿渐变大标题；右侧实时词元交易看板；四个卖点图标'),
    ('01_siliconflow', '硅基流动 SiliconFlow', 'API 平台（国内）', ['#6C28F6', '#743AED', '#36384A', '#F1F1FF', '#1E293B'], 'Roboto + 系统中文字体', '浅紫底轮播 banner，主推新模型上线；深色产品矩阵卡片'),
    ('02_ppio', 'PPIO 派欧云', '算力聚合 + 模型 API', ['#1161FE', '#0E58EA', '#E9F1FF', '#F7F8FA', '#181818'], '系统字体（PingFang）', '浅蓝白底；3D 玻璃立方体；新模型上线轮播；"Tools for Agents"'),
    ('03_infini', '无问芯穹 Infinigence', '异构算力优化 + MaaS', ['#5D2BFE', '#000000', '#FFFFFF', '#333333'], 'PingFang SC', '黑底紫光等轴测芯片插画；合作伙伴 logo 条'),
    ('09_deepseek_platform', 'DeepSeek 开放平台', '官方 API（参照）', ['#121519', '#3B82F6', '#FFFFFF', '#0F1115'], 'Inter / Montserrat', '左侧蓝灰渐变插画 + 右侧登录表单；极简'),
    ('04_openrouter', 'OpenRouter', 'API 聚合（海外）', ['#7624F4', '#FCFCFE', '#03080A', '#035ADE'], 'Plus Jakarta Sans / Gordita', '极简白底；单一紫色 CTA"Get API Key"；规模数字条；模型卡片'),
    ('05_together', 'Together AI', 'AI 云（海外）', ['#000000', '#010120', '#FC4C02', '#CAAEF5', '#EF2CC1', '#C8F6F9'], 'The Future + PP Neue Montreal Mono', '白底 + 彩色 3D 抽象几何；等宽小标签；研究感'),
    ('06_crusoe', 'Crusoe', '能源资产延伸型 AI 云', ['#000000', '#CEEB13', '#323C2A', '#ECF0E9'], 'Suisse Intl + ABC Diatype Mono', '黑底机房实拍；荧光黄绿 CTA 与色块；等宽大标题'),
    ('07_emerald', 'Emerald AI', '算电协同软件型', ['#253023', '#50594F', '#438C36', '#F6F6F7'], 'DM Sans + Crimson Pro（衬线）', '数据中心航拍实景；衬线斜体大标题；深绿 + 鲜绿'),
    ('08_soluna', 'Soluna', '绿电数据中心', ['#231F20', '#CB5727', '#783518', '#FFFFFF'], 'Nunito Sans', '风机航拍；锈橙 + 炭黑分区；规模数字（MW）'),
]

PALETTE = [
    ('主色 Primary', [('深海蓝', '#102A43', '品牌锚点、标题、深色底'), ('深能源青', '#0B7285', '按钮、链接、白底上的品牌青')]),
    ('辅色 Secondary', [('能源青', '#169FB0', '图形、线条、大字；或放在深海蓝底上'), ('青雾', '#E6F5F7', '卡片与区块底色'), ('雾白', '#F5F8FC', '页面底色')]),
    ('灰阶 Grayscale', [('墨', '#0F172A', '正文'), ('石墨灰', '#475569', '次级文字'), ('银灰', '#CBD5E1', '分隔线、禁用态'), ('白', '#FFFFFF', '')]),
    ('强调色 Accent（可选，见方案 B）', [('峰光琥珀', '#F2A93B', '只放在深海蓝底：峰值、绿电窗口高亮'), ('琥珀深', '#9A5B00', '白底上的强调文字')]),
]


def lum(h):
    h = h.lstrip('#'); c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def contrast(a, b):
    la, lb = sorted([lum(a), lum(b)], reverse=True); return (la + 0.05) / (lb + 0.05)


def grade(r):
    return 'AAA' if r >= 7 else 'AA' if r >= 4.5 else 'AA 大字' if r >= 3 else '不合格'


data = json.load(open(os.path.join(D, 'extracted_styles.json')))
e = html.escape
parts = ["""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>竞品品牌视觉调研板</title><style>
@page { size: 1600px 900px; margin: 0; }
body { margin: 0; font-family: "PingFang SC", "Hiragino Sans GB", -apple-system, sans-serif; color: #102A43; }
.page { width: 1600px; height: 900px; box-sizing: border-box; padding: 48px 56px; page-break-after: always; overflow: hidden; }
h1 { font-size: 34px; margin: 0 0 8px; } h2 { font-size: 24px; margin: 0 0 20px; }
.meta { color: #475569; font-size: 14px; margin-bottom: 28px; }
ol.find { font-size: 18px; line-height: 1.55; padding-left: 26px; margin: 0; } ol.find li { margin-bottom: 12px; }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 26px 40px; }
.card { display: grid; grid-template-columns: 400px 1fr; gap: 18px; }
.card img { width: 400px; height: 250px; object-fit: cover; object-position: top; border: 1px solid #CBD5E1; }
.card h3 { grid-column: 1 / -1; margin: 0; font-size: 20px; }
.cat { color: #475569; font-size: 13px; } .hl { font-size: 14px; margin: 6px 0; } .small { font-size: 12px; color: #475569; }
.sw { display: inline-block; margin: 6px 8px 0 0; font-size: 11px; color: #475569; text-align: center; }
.sw i { display: block; width: 72px; height: 36px; border: 1px solid #CBD5E1; margin-bottom: 3px; }
table { border-collapse: collapse; font-size: 15px; } td, th { padding: 8px 14px; border-bottom: 1px solid #E2E8F0; text-align: left; }
.chip { display: inline-block; width: 46px; height: 28px; border: 1px solid #CBD5E1; vertical-align: middle; }
.bad { color: #B91C1C; font-weight: 600; } .mid { color: #B45309; } .ok { color: #047857; }
.pal { display: grid; grid-template-columns: 240px 1fr; row-gap: 22px; align-items: start; }
.pal .row { display: flex; gap: 28px; } .pc { width: 230px; font-size: 12px; color: #475569; }
.pc i { display: block; width: 230px; height: 56px; border: 1px solid #CBD5E1; margin-bottom: 6px; } .pc b { color: #102A43; font-size: 13px; }
</style></head><body>"""]

parts.append(f"""<section class="page"><h1>沐仞科技｜竞品官网与品牌视觉调研</h1>
<div class="meta">采集时间：2026-10-12。工具：无头 Chrome，1440×900 视口。色值取自页面实际计算样式（computed style）与 CSS 变量；色差算法为 CIEDE2000。截图与原始数据见 data/ 文件夹。</div>
<ol class="find">
<li><b>国内模型 API 平台的颜色高度同质</b>：紫色（硅基流动 #6C28F6、无问芯穹 #5D2BFE、OpenRouter #7624F4）或标准科技蓝（PPIO #1161FE、DeepSeek 平台 #3B82F6），配 3D 玻璃或抽象几何插画，首屏都是"新模型上线"轮播。</li>
<li><b>能源 + AI 公司走"实景 + 大地色"</b>：Crusoe 荧光黄绿 #CEEB13、Emerald 深绿 #253023、Soluna 锈橙 #CB5727，使用真实机房、电站、风机照片，配衬线或等宽字体，语气偏宣言式。</li>
<li><b>沐仞的蓝撞色</b>：现网主蓝 #2563EB 与 PPIO 主色色差 ΔE 2.2；品牌规范 V1 的亮蓝 #176BFA 色差 3.4，接近肉眼难分。</li>
<li><b>能源青 #169FB0 是空白色区</b>：与所有竞品主色色差都大于 25；但白底对比度只有 3.17，需要配一个深色版本用于文字和按钮。</li>
<li><b>"Token 工厂 / 词元"已被占用</b>：PPIO 写"面向 Agent 时代打造 Token 工厂"，无问芯穹导航有"Token工厂"，硅基流动推"TokenPlus 词元优选"。沐仞 BP 里的"词元工厂"不再具有区分度。</li>
<li><b>沐仞的独有元素</b>：现网"实时词元交易看板"（电站 × 模型 × 成交价 × 减排量）在所有竞品中都没有出现，可以作为品牌标志性资产，前提是展示的是真实数据。</li>
<li><b>自身一致性问题</b>：首页 iframe 的页面标题写"拼好算"；外壳与首页用了两套配色（#3EA4EC 与 #2563EB），都不是规范 V1；联系邮箱是 fathompeak@163.com；BP 上印的 www.fathompeak.tech 证书已于 2026-10-02 过期。</li>
</ol></section>""")

for i in range(0, len(SITES), 4):
    parts.append('<section class="page"><div class="grid">')
    for key, name, cat, sw, fonts, vis in SITES[i:i + 4]:
        d = data.get(key, {})
        img = f"data/{key}_long.png"
        sws = ''.join(f'<span class="sw"><i style="background:{c}"></i>{c}</span>' for c in sw)
        parts.append(f"""<div class="card"><h3>{e(name)} <span class="cat">· {e(cat)}</span></h3>
<img src="{img}"><div><div class="hl"><b>主标题：</b>{e((d.get('heroText') or '')[:60])}</div>
<div class="small"><b>页面描述：</b>{e((d.get('description') or '')[:90])}</div>
<div class="small" style="margin-top:6px"><b>字体：</b>{e(fonts)}</div>
<div class="small" style="margin-top:4px"><b>视觉：</b>{e(vis)}</div><div>{sws}</div></div></div>""")
    parts.append('</div></section>')

rows = []
for n, c in cd.ours.items():
    dist, cn, cc = min((cd.de2000(c, v), k, v) for k, v in cd.competitors.items())
    cls = 'bad' if dist < 5 else 'mid' if dist < 15 else 'ok'
    rows.append(f'<tr><td><span class="chip" style="background:{c}"></span> {e(n)} {c}</td><td><span class="chip" style="background:{cc}"></span> {e(cn)} {cc}</td><td class="{cls}">ΔE {dist:.1f}</td></tr>')
parts.append(f"""<section class="page"><h2>色彩重合度：沐仞用色 vs 最近的竞品主色</h2>
<div class="meta">CIEDE2000：ΔE 约 2.3 为恰可察觉差；小于 5 时，并排对比也很难区分；大于 25 可以视为不同色区。</div>
<table><tr><th>沐仞用色</th><th>最接近的竞品色</th><th>色差</th></tr>{''.join(rows)}</table></section>""")

pal = []
for gname, cols in PALETTE:
    cells = []
    for nm, hx, use in cols:
        rw, rn = contrast(hx, '#FFFFFF'), contrast(hx, '#102A43')
        dist, cn, _ = min((cd.de2000(hx, v), k, v) for k, v in cd.competitors.items())
        navy = '' if hx == '#102A43' else f'<br>深海蓝底 {rn:.2f} {grade(rn)}'
        cells.append(f'<div class="pc"><i style="background:{hx}"></i><b>{e(nm)} {hx}</b><br>白底 {rw:.2f} {grade(rw)}{navy}<br>最近竞品 ΔE {dist:.1f}<br>{e(use)}</div>')
    pal.append(f'<div><b>{e(gname)}</b></div><div class="row">{"".join(cells)}</div>')
parts.append(f"""<section class="page"><h2>候选色卡（结构参照 LifeWire 设计交接稿：主色 / 辅色 / 灰阶 / 强调色 + WCAG 等级）· 待确认</h2>
<div class="pal">{''.join(pal)}</div></section>""")
parts.append('</body></html>')

out_html = os.path.join(R, '竞品品牌视觉调研板_2026-10-12.html')
open(out_html, 'w').write('\n'.join(parts))
out_pdf = os.path.join(R, '竞品品牌视觉调研板_2026-10-12.pdf')
subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-pdf-header-footer', f'--print-to-pdf={out_pdf}', 'file://' + out_html],
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
print(out_pdf)
