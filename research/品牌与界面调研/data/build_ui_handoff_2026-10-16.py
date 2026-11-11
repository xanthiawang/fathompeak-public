"""UI 视觉交付包的说明页与色值文件（Zixin 2026-10-16："整理我们做 ui 上用到的所有视觉设计和材料，我给视觉团队"）。
读交付包里的实际文件生成：00_先看这个.html、01_色彩与字体/tokens.json、tokens.css。素材有更新时重跑即可。
色值、字号取自线上 c5c5450 的计算样式（无头 Chrome 读 getComputedStyle），插画用途按 index.html 里的引用核对。
2026-10-19：Logo 定为层叠峰面（Codex 分支 codex/logo-svg-monochrome-20261018），05_品牌标识 与 07_页面截图 随官网 ae48adf 更新。
用法：python3 -I build_ui_handoff_2026-10-16.py <交付包目录>
"""
import html, json, os, sys

P = sys.argv[1]
WEB = sys.argv[sys.argv.index('--web') + 1] if '--web' in sys.argv else None  # 网页版：放到 GitHub 下载页，加整包下载、文件清单、noindex
E = html.escape


def human(n):
    return f'{n / 1048576:.1f} MB' if n >= 1048576 else f'{max(1, round(n / 1024))} KB'

# ---------- 色值（线上计算样式） ----------
COLORS = [
    ('基底', [('--paper', '#F8F8F8', '页面底色（官网与后台）'), ('--paper-2', '#F3F1EA', '暖纸，少量区块'), ('--card', '#FFFFFF', '卡片'),
              ('--ink', '#000000', '官网标题与正文'), ('后台 --ink', '#212021', '后台正文、首页首屏底（炭黑）')]),
    ('晨蓝 · 强调', [('--accent', '#2F63B8', '链接文字、导航当前态、表头色带起点；不做大面积平涂'), ('--accent-fill', '#5284D7', '小面积填充点缀（圆点、状态）'),
                   ('--accent-soft', '#DCE7F7', '浅底'), ('--accent-tint', '#EEF3FB', '更浅的底')]),
    ('暮紫 · 深色搭配', [('--hz-2b / --hi', '#3D314F', '后台徽标底、深色强调、色带中段'), ('--peak / --icon', '#4E3F66', '图标描边、功能紫'), ('--peak-soft', '#EAE4F0', '紫色浅底')]),
    ('雾色 · 晨昏过渡', [('--field-1', '#A9C3E8', '雾蓝'), ('--field-2', '#E3ECF8', '晨雾'), ('--field-3', '#EBCFC4', '暖粉'), ('--field-4', '#D6CBDD', '淡紫'),
                     ('--hz-haze', '#E8D4CC', '暮霭'), ('--hz-2', '#B7A8A3', '灰褐')]),
]
ALPHA = [('文字 85%', 'rgba(0,0,0,.85)'), ('文字 70%（说明）', 'rgba(0,0,0,.7)'), ('文字 50%（弱）', 'rgba(0,0,0,.5)'), ('文字 30%（占位）', 'rgba(0,0,0,.3)'),
         ('官网分隔线', 'rgba(0,0,0,.08)'), ('官网细线', 'rgba(0,0,0,.05)'), ('后台分隔线', 'rgba(61,49,79,.14)'), ('后台细线', 'rgba(61,49,79,.08)'),
         ('后台卡框', 'rgba(61,49,79,.22)'), ('白玻璃', 'rgba(255,255,255,.86)'), ('灰玻璃按钮', 'rgba(235,235,235,.7)')]
GRADS = [('晨昏渐变（官网浅色强调区）', 'linear-gradient(120deg,#E3ECF8 0%,#ECE6F1 52%,#F6E9E2 100%)', '定价「计算方式」、费用估算结果、产品页强调标签。替代原来的平涂浅蓝。'),
         ('示意窗雾面', 'linear-gradient(135deg,#D3DEEE 0%,#E0D9E8 55%,#EDDFD6 100%)', '首页「怎么用」第二块示意窗；另两块是纯色 #EEDCD3（暖粉）和 #E9E8E4（纸灰）。'),
         ('后台页头 wash', 'linear-gradient(155deg,rgba(47,99,184,.16),rgba(61,49,79,.09) 54%,rgba(33,32,33,.025) 78%,#F8F8F8)', '后台各页顶部的淡色过渡。'),
         ('后台区块 band', 'linear-gradient(135deg,rgba(47,99,184,.10),rgba(61,49,79,.08))', '后台大块区域的浅色底。'),
         ('表头色带 band-x', 'linear-gradient(105deg,#2F63B8 0%,#3D314F 66%,#212021 100%)', '后台所有表格的表头，文字白 94%。'),
         ('空状态白玻璃', 'linear-gradient(165deg,rgba(255,255,255,.83),rgba(255,255,255,.91))', '压在树影背景上的卡片；配白 62% 描边、顶部内高光、暮紫软阴影 0 12px 36px -24px rgba(61,49,79,.42)。')]
TYPE = [('官网正文', 'DM Sans · 中文落到苹方 / 系统黑体', '16px / 24px', '400'),
        ('首页首屏标题', 'Fraunces · 思源宋体（Noto Serif SC）', '40px / 1.5，字距 −1px', '400'),
        ('官网区块标题', 'Fraunces · 思源宋体', '46px / 1.12，字距 −1.15px', '400'),
        ('后台一级标题', 'Fraunces · 思源宋体', '40px / 1.12，字距 −1px（手机 30px）', '400'),
        ('后台区块标题', 'Fraunces · 思源宋体', '28px / 1.2，字距 −0.56px（手机 24px）', '400'),
        ('后台正文', 'DM Sans · 苹方', '15px / 1.55', '400'),
        ('主按钮', 'DM Sans · 苹方', '17px', '500'),
        ('数字、代码、标签', 'DM Mono', '14px / 1.5', '400'),
        ('表头', 'DM Mono', '11px，字距 .08em，白 94%', '400'),
        ('花体首字母', 'Pinyon Script（HandLatin）', '1.3em，只修饰拉丁字母开头的标题首字母', '400')]
RADII = [('10px', '小按钮、导航项'), ('12px', '输入框、账户按钮、案例卡'), ('16px', '普通卡片、统计卡、示意窗'), ('20px', '大卡、空状态卡、首页主按钮'),
         ('24px', '大面板'), ('30px', '大容器'), ('999px', '胶囊：后台主按钮、筛选条、标签')]
SHADOW = [('卡片 / 筛选条', '0 2px 8px rgba(0,0,0,.06), 0 0 2px rgba(0,0,0,.04)'), ('浮层', '0 6px 20px rgba(0,0,0,.08), 0 0 2px rgba(0,0,0,.05)'),
          ('官网大浮层', '0 -1px 2px -1px rgba(45,35,24,.09), 0 24px 60px -20px rgba(60,45,30,.25)'), ('示意窗', '0 1px 2px rgba(0,0,0,.05), 0 22px 44px -26px rgba(0,0,0,.32)')]
EASE = [('标准', 'cubic-bezier(.4,0,.2,1)'), ('出场', 'cubic-bezier(.22,1,.36,1)'), ('入场', 'cubic-bezier(0,0,.2,1)')]

# ---------- 插画（按 index.html 引用核对） ----------
ART_USED = [('engraved-dark-atlas_2026-10-14.webp', '后台排线图集（3 × 2）', '后台空状态与面板插画。上排：太阳能板、书、路牌；下排：箱子、价签、钥匙。黑白排线主体叠不规则深色色片，边缘透明。'),
            ('api-key-dapple-blue_2026-10-14.webp', '蓝色树影', '后台概览、体验中心、超管页头的背景。叠两层慢速动画（树影 10s、光斑 13s），系统开「减少动态效果」时静止。'),
            ('products-token-flow_2026-10-13.webp', '词元流动', '产品与服务页顶部横幅，产品列表小图标的底纹。'),
            ('engineering-stack_2026-10-14.png', '工程分层图', '产品与服务页「任务处理流程」右侧的分层示意（接入、调度、计算、电力）。'),
            ('engraved-ascent_2026-10-14.webp', '登录排线：手与机械手', '客户登录页、员工登录页左侧。鼠标拖动有轻微视差（见登录排线插画说明）。'),
            ('education-editorial-engraving-2026-10-14.png', '教育排线', '教育优惠页。')]
ART_SPARE = [('doodle-atlas_2026-10-14.webp', '手绘涂鸦图集（备选）'), ('editorial-collage-atlas_2026-10-14.webp', '编辑拼贴图集（备选）'), ('engraved-blend-atlas_2026-10-14.webp', '排线混合图集（备选）'),
             ('console-dapple_2026-10-14.webp', '浅色树影（备选）'), ('products-energy-compute_2026-10-13.webp', '能源与算力（备选）')]
PAGES = [('01_首页_首屏', '首页 · 首屏'), ('02_首页_怎么用', '首页 · 怎么用'), ('03_首页_项目案例', '首页 · 项目案例'), ('04_产品与服务', '产品与服务'), ('05_产品与服务_流程', '产品与服务 · 流程'),
         ('06_定价', '定价'), ('07_企业合作', '企业合作'), ('08_电站合作', '电站合作'), ('09_关于我们', '关于我们'), ('10_文档', '文档（AI 模型接口）'),
         ('11_登录_个人', '登录 · 个人'), ('12_登录_企业', '登录 · 企业'), ('13_个人后台_概览', '个人后台 · 概览'), ('14_体验中心', '体验中心'), ('15_企业管理员_成员', '企业管理员 · 成员'),
         ('16_企业管理员_钱包', '企业管理员 · 钱包'), ('17_企业成员_概览', '企业成员 · 概览'), ('18_超管_工作台', '超管 · 工作台'), ('19_超管_渠道接入', '超管 · 渠道接入'),
         ('20_超管_渠道编辑框', '超管 · 渠道编辑框'), ('21_超管_定价', '超管 · 定价'), ('22_财务工作台', '财务 · 工作台')]
COMPS = [('01_按钮组', '主按钮（黑胶囊）与次按钮（灰玻璃胶囊）'), ('02_项目案例卡', '项目案例卡：细线框、衬线标题、底部状态'), ('03_定价公式框', '晨昏渐变说明框'),
         ('04_登录卡', '登录页「个人 / 企业」切换'), ('05_后台页头与筛选', '后台页头：衬线标题 + 黑胶囊 + 白玻璃筛选条'), ('06_空状态插画卡', '空状态：排线插画 + 白玻璃卡'),
         ('07_开始使用步骤卡', '步骤卡：圆形勾选 + 半透明白卡'), ('08_表格与色带表头', '表格：色带表头 + 细线行'), ('09_统计卡', '统计卡：白卡 + 等宽数字'),
         ('10_侧栏', '后台侧栏：账户块、分组标题、图标导航'), ('11_渠道卡片', '超管渠道卡片'), ('12_渠道编辑框', '超管编辑框：标签页 + 分组表单')]

# ---------- tokens.json / tokens.css ----------
tok = {'说明': '沐仞 UI 色值、字体、圆角、阴影、动效。取自线上 c5c5450 的计算样式，2026-10-16。', '色彩': {}, '透明色': dict(ALPHA), '渐变': {g[0]: g[1] for g in GRADS},
       '字体': {'衬线（标题）': '"Fraunces","Noto Serif SC","Songti SC","STSong",Georgia,serif', '无衬线（正文）': '"DM Sans","Noto Sans SC","PingFang SC","Hiragino Sans GB",system-ui,sans-serif',
              '等宽（数字、代码）': '"DM Mono","IBM Plex Mono",Menlo,monospace', '花体首字母': '"HandLatin"（Pinyon Script 子集）'},
       '字号': {t[0]: {'字体': t[1], '字号行高': t[2], '字重': t[3]} for t in TYPE}, '圆角': dict(RADII), '阴影': dict(SHADOW), '缓动': dict(EASE)}
for g, items in COLORS:
    tok['色彩'][g] = {n: {'值': v, '用途': u} for n, v, u in items}
os.makedirs(os.path.join(P, '01_色彩与字体'), exist_ok=True)
json.dump(tok, open(os.path.join(P, '01_色彩与字体', 'tokens.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=2)
css = ['/* 沐仞 UI 色值（线上 c5c5450，2026-10-16）。官网用 :root，后台在 .bt 里覆盖了墨色与线色。 */', ':root{']
for g, items in COLORS:
    css.append(f'  /* {g} */')
    for n, v, u in items:
        if n.startswith('--') and '/' not in n: css.append(f'  {n}:{v};  /* {u} */')
css += ['  --hz-2b:#3D314F; --peak:#4E3F66; --hz-3:#212021;', '  --ink-85:rgba(0,0,0,.85); --ink-70:rgba(0,0,0,.7); --ink-50:rgba(0,0,0,.5); --ink-30:rgba(0,0,0,.3);',
        '  --line:rgba(0,0,0,.08); --line-2:rgba(0,0,0,.05); --gray-btn:rgba(235,235,235,.7);',
        f'  --wash-soft:{GRADS[0][1]};', '  --serif:"Fraunces","Noto Serif SC","Songti SC","STSong",Georgia,serif;',
        '  --sans:"DM Sans","Noto Sans SC","PingFang SC","Hiragino Sans GB",system-ui,sans-serif;', '  --mono:"DM Mono","IBM Plex Mono",Menlo,monospace;',
        '  --r10:10px; --r12:12px; --r16:16px; --r20:20px; --r24:24px; --r30:30px; --pill:999px;',
        '  --shadow:0 2px 8px rgba(0,0,0,.06),0 0 2px rgba(0,0,0,.04);', '  --ease:cubic-bezier(.4,0,.2,1); --ease-out:cubic-bezier(.22,1,.36,1);', '}',
        '.bt{  /* 后台 */', '  --ink:#212021; --line:rgba(61,49,79,.14); --line-2:rgba(61,49,79,.08); --frame:rgba(61,49,79,.22);',
        '  --icon:#4E3F66; --icon-active:#2F63B8; --glass:rgba(255,255,255,.86); --hi:#3D314F; --gray-btn:rgba(61,49,79,.07);',
        f'  --wash:{GRADS[2][1]};', f'  --band:{GRADS[3][1]};', f'  --band-x:{GRADS[4][1]};', '}']
open(os.path.join(P, '01_色彩与字体', 'tokens.css'), 'w', encoding='utf8').write('\n'.join(css) + '\n')

# ---------- 说明页 ----------
icons = sorted(f for f in os.listdir(os.path.join(P, '03_图标')) if f.endswith('.svg'))
explore = sorted(f for f in os.listdir(os.path.join(P, '05_品牌标识', '探索稿_未定稿')) if f.endswith('.png'))


def sw(n, v, u):
    dark = v.upper() in ('#000000', '#212021', '#2F63B8', '#3D314F', '#4E3F66', '#5284D7')
    return f'<div class="sw"><i style="background:{v}"></i><b>{E(v)}</b><span class="mono">{E(n)}</span><p>{E(u)}</p></div>'


def count(rel):
    d = os.path.join(P, rel); return sum(len(fs) for _, _, fs in os.walk(d)) if os.path.isdir(d) else 0


FOLDERS = [('01_色彩与字体', 'tokens.json、tokens.css：本页色值、字号、圆角、阴影的文件版，可导入 Figma 变量或给开发直接用。'),
           ('02_字体文件', '页面实际加载的 Fraunces、DM Sans、DM Mono 和花体 Pinyon Script（woff2），附授权说明。'),
           ('03_图标', f'后台侧栏全部 {len(icons)} 个图标，20 × 20、描边 1.4，SVG。'),
           ('04_插画与背景', '「现用」是页面正在用的；「备选_页面未使用」是做过但没上线的；另附插画方向和登录排线的生成说明。'),
           ('05_品牌标识', '「现用」：层叠峰面 Logo（官方 SVG / PNG，可编辑）、网站用的单独图形和英文字标、网站图标、分享图、公众号二维码。「旧版_2026-10-19前」：被替换掉的双峰山形标。「探索稿_未定稿」：定稿前的方向探索，只作回溯。'),
           ('06_第三方Logo', '合作方与模型厂商的 Logo，保持原色；合作方 Logo 目前页面上没有展示。'),
           ('07_页面截图', '电脑（1440 宽）、手机（390 宽）各 22 页，外加 12 张组件特写。页面截图 10-19 重拍，已是新 Logo。'),
           ('08_参考与历史文档', '10-14 设计交接、10-13 设计幻灯片、色彩过渡研究、竞品视觉调研板。部分内容已过时，以本页为准。')]

parts = []
parts.append(f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">{"<meta name=\"robots\" content=\"noindex,nofollow\">" if WEB else ""}
<title>沐仞 UI 视觉交付包</title>
<link rel="stylesheet" href="02_字体文件/fonts.css">
<style>
@font-face{{font-family:"HandLatin";src:url("02_字体文件/hand-pinyonscript-subset.woff2") format("woff2")}}
:root{{--paper:#F8F8F8;--card:#fff;--ink:#212021;--ink-70:rgba(0,0,0,.7);--ink-50:rgba(0,0,0,.5);--line:rgba(61,49,79,.14);--accent:#2F63B8;--peak:#4E3F66;
--serif:"Fraunces","Noto Serif SC","Songti SC","STSong",Georgia,serif;--sans:"DM Sans","PingFang SC","Hiragino Sans GB",system-ui,sans-serif;--mono:"DM Mono",Menlo,monospace;
--wash:linear-gradient(120deg,#E3ECF8 0%,#ECE6F1 52%,#F6E9E2 100%);color-scheme:light}}
*{{box-sizing:border-box}} html{{scroll-behavior:smooth}}
body{{margin:0;background:var(--paper);color:var(--ink);font:15px/1.65 var(--sans);-webkit-font-smoothing:antialiased}}
a{{color:var(--accent)}}
.wrap{{max-width:1180px;margin:0 auto;padding:0 24px 96px;display:grid;grid-template-columns:200px minmax(0,1fr);gap:56px}}
header.top{{background:var(--wash);border-bottom:1px solid var(--line);padding:56px 24px 44px;margin-bottom:40px}}
header.top .in{{max-width:1180px;margin:0 auto}}
header.top .k{{font:400 12px var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--ink-50)}}
h1{{font:400 46px/1.12 var(--serif);letter-spacing:-.025em;margin:10px 0 14px}}
h1 .h::first-letter{{font-family:"HandLatin",var(--serif);font-size:1.3em}}
header.top p{{max-width:62ch;margin:0;color:var(--ink-70);font-size:16px}}
.dl{{display:flex;flex-wrap:wrap;align-items:center;gap:10px 16px;margin-top:22px}} .dl a.btn{{display:inline-flex;align-items:center;height:44px;padding:0 22px;border-radius:999px;background:#000;color:#fff;text-decoration:none;font-weight:500}} .dl span{{font-size:13.5px;color:var(--ink-70)}}
.files{{columns:2 320px;column-gap:28px;font-size:13.5px}} .files h3{{break-after:avoid;margin:18px 0 6px}} .files ul{{list-style:none;margin:0 0 6px;padding:0}} .files li{{display:flex;gap:10px;justify-content:space-between;border-bottom:1px solid var(--line);padding:5px 0;break-inside:avoid}} .files li a{{word-break:break-all}} .files li span{{color:var(--ink-50);font-family:var(--mono);font-size:12px;white-space:nowrap}}
nav.toc{{position:sticky;top:24px;align-self:start;display:grid;gap:6px;font-size:14px}}
nav.toc b{{font:400 11px var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--ink-50);margin-bottom:4px}}
nav.toc a{{color:var(--ink-70);text-decoration:none}} nav.toc a:hover{{color:var(--ink)}}
main{{min-width:0}}
section{{margin-bottom:72px;scroll-margin-top:24px}}
h2{{font:400 32px/1.2 var(--serif);letter-spacing:-.02em;margin:0 0 8px}}
h3{{font:500 16px var(--sans);margin:28px 0 10px}}
.lede{{color:var(--ink-70);max-width:70ch;margin:0 0 20px}}
.mono{{font-family:var(--mono)}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px 20px}}
table{{width:100%;border-collapse:collapse;font-size:14px}}
th{{text-align:left;font:400 11px var(--mono);letter-spacing:.08em;color:rgba(255,255,255,.94);padding:12px 14px;white-space:nowrap}}
thead{{background:linear-gradient(105deg,#2F63B8 0%,#3D314F 66%,#212021 100%)}}
td{{padding:12px 14px;border-bottom:1px solid var(--line);vertical-align:top}}
.tw{{overflow-x:auto;border-radius:14px;border:1px solid var(--line);background:#fff}}
ul.rules{{margin:0;padding:0;list-style:none;display:grid;gap:10px}}
ul.rules li{{background:#fff;border:1px solid var(--line);border-radius:14px;padding:14px 18px}}
ul.rules b{{font-weight:500}}
.sws{{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:12px;margin-bottom:8px}}
.sw{{background:#fff;border:1px solid var(--line);border-radius:16px;overflow:hidden;display:grid}}
.sw i{{display:block;height:72px;border-bottom:1px solid var(--line)}}
.sw b{{font:500 14px var(--mono);padding:10px 14px 0}} .sw span{{font-size:12px;color:var(--ink-50);padding:0 14px}} .sw p{{margin:4px 14px 14px;font-size:13px;color:var(--ink-70);line-height:1.5}}
.alpha{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:8px}}
.alpha div{{display:flex;align-items:center;gap:10px;background:#fff;border:1px solid var(--line);border-radius:12px;padding:8px 12px;font-size:13px}}
.alpha i{{width:28px;height:28px;border-radius:8px;flex:none;border:1px solid rgba(0,0,0,.06);background-image:linear-gradient(45deg,#ddd 25%,transparent 25%,transparent 75%,#ddd 75%),linear-gradient(45deg,#ddd 25%,#fff 25%,#fff 75%,#ddd 75%);background-size:8px 8px;background-position:0 0,4px 4px;position:relative;overflow:hidden}}
.alpha i em{{position:absolute;inset:0}} .alpha code{{font:12px var(--mono);color:var(--ink-50);margin-left:auto}}
.grad{{display:grid;grid-template-columns:220px minmax(0,1fr);gap:16px;align-items:center;background:#fff;border:1px solid var(--line);border-radius:16px;padding:12px;margin-bottom:10px}}
.grad i{{display:block;height:84px;border-radius:12px;border:1px solid rgba(0,0,0,.05)}}
.glassdemo{{background:url('04_插画与背景/现用/api-key-dapple-blue_2026-10-14.webp') center/cover;padding:14px}} .glassdemo em{{display:block;height:100%;border-radius:10px;border:1px solid rgba(255,255,255,.62);box-shadow:inset 0 1px 0 rgba(255,255,255,.8),0 12px 36px -24px rgba(61,49,79,.42)}}
.grad b{{font-weight:500}} .grad code{{display:block;font:12px/1.5 var(--mono);color:var(--ink-50);word-break:break-all;margin:4px 0}} .grad p{{margin:0;font-size:13.5px;color:var(--ink-70)}}
.spec{{display:grid;gap:10px}}
.spec .card{{display:grid;grid-template-columns:minmax(0,1fr) 260px;gap:16px;align-items:center}}
.spec .smp{{overflow:hidden;white-space:nowrap;text-overflow:ellipsis}}
.spec .meta{{font-size:13px;color:var(--ink-70)}} .spec .meta b{{display:block;color:var(--ink);font-weight:500}}
.kv{{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:10px}}
.kv div{{background:#fff;border:1px solid var(--line);padding:12px 14px;font-size:13.5px}} .kv b{{display:block;font-weight:500}} .kv code{{font:12px/1.5 var(--mono);color:var(--ink-50)}}
.comps{{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:16px}}
figure{{margin:0;background:#fff;border:1px solid var(--line);border-radius:16px;overflow:hidden;display:grid}}
figure a{{display:block;background:#F1F1F3}} figure img{{display:block;width:100%;height:auto;max-height:340px;object-fit:contain}}
figcaption{{padding:10px 14px 12px;font-size:13.5px;color:var(--ink-70)}} figcaption b{{display:block;color:var(--ink);font-weight:500}}
.icons{{display:grid;grid-template-columns:repeat(auto-fill,minmax(112px,1fr));gap:10px}}
.icons div{{background:#fff;border:1px solid var(--line);border-radius:14px;padding:16px 8px 10px;display:grid;justify-items:center;gap:8px;font-size:12.5px;color:var(--ink-70);text-align:center}}
.icons img{{width:28px;height:28px}}
.arts{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px}}
.arts img{{aspect-ratio:4/3;object-fit:cover;max-height:none}}
.pages{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:14px}}
.pages img{{aspect-ratio:16/10;object-fit:cover;object-position:top;max-height:none}}
.pages figcaption a{{display:inline;background:none;margin-right:10px;font-size:13px}}
.note{{background:var(--wash);border:1px solid rgba(61,49,79,.08);border-radius:16px;padding:16px 20px}}
.note p{{margin:0 0 6px}} .note p:last-child{{margin:0}}
.tag{{display:inline-block;font:400 11px var(--mono);letter-spacing:.06em;padding:2px 9px;border-radius:999px;background:rgba(61,49,79,.08);color:var(--peak);vertical-align:middle}}
.tag.warn{{background:#F6E9E2;color:#8A4B32}}
@media (max-width:860px){{.wrap{{grid-template-columns:minmax(0,1fr);gap:24px}} nav.toc{{position:static;grid-template-columns:repeat(2,minmax(0,1fr))}} h1{{font-size:34px}} .grad,.spec .card{{grid-template-columns:minmax(0,1fr)}}}}
</style></head><body>
<header class="top"><div class="in"><span class="k">沐仞 FathomPeak · UI 视觉交付包 · 2026-10-16</span>
<h1><span class="h">UI 视觉设计与素材</span></h1>
<p>官网和后台（个人、企业管理员、企业成员、超管、财务）在线上实际使用的色彩、字体、组件、图标、插画和页面，全部取自线上版本 c5c5450（2026-10-16）。网页在线地址：<a href="https://xanthiawang.github.io/fathompeak-site/">xanthiawang.github.io/fathompeak-site</a>。</p>{{DLBAR}}</div></header>
<div class="wrap">
<nav class="toc" aria-label="目录"><b>目录</b><a href="#pkg">包里有什么</a><a href="#rules">设计原则</a><a href="#color">色彩</a><a href="#type">字体</a><a href="#shape">圆角、阴影、动效</a><a href="#comp">组件</a><a href="#icon">图标</a><a href="#art">插画与背景</a><a href="#brand">品牌标识</a><a href="#logo">第三方 Logo</a><a href="#pages">页面截图</a><a href="#ref">参考与历史</a><a href="#open">还没定的</a>{"<a href=\"#files\">全部文件下载</a>" if WEB else ""}</nav>
<main>''')

parts.append('<section id="pkg"><h2>包里有什么</h2><p class="lede">文件夹按用途分，每个文件夹名前面的编号和本页目录对应。没有 Figma 源文件：现在的设计都直接写在网页代码里，下面的色值、字号是从线上页面读出来的实际值。</p><div class="tw"><table><thead><tr><th>文件夹</th><th>文件数</th><th>内容</th></tr></thead><tbody>'
             + ''.join(f'<tr><td class="mono">{E(f)}</td><td class="mono">{count(f)}</td><td>{E(d)}</td></tr>' for f, d in FOLDERS) + '</tbody></table></div></section>')

parts.append('''<section id="rules"><h2>设计原则</h2><p class="lede">这几条是这几轮改稿里反复确认过的，新做的页面和插画请按它来。</p><ul class="rules">
<li><b>纸白底、墨黑字。</b>页面底 #F8F8F8，卡片纯白；官网正文纯黑，后台正文炭黑 #212021。</li>
<li><b>晨蓝只给链接和当前态。</b>#2F63B8 用在链接、导航当前项、表头色带起点，不做大面积平涂浅蓝块。需要浅色强调时用晨昏渐变（晨蓝 → 淡紫 → 暖米）。</li>
<li><b>颜色之间要过渡，不要硬拼。</b>页头用 wash 渐变，大区块用 band，卡片用白玻璃（半透明白 + 细线 + 软阴影），透明填充和文字分开设色，不给整个组件降透明度。</li>
<li><b>主按钮只有一种：黑色胶囊。</b>次按钮是灰玻璃胶囊；文字链接带下划线。</li>
<li><b>标题用衬线，正文用无衬线，数字用等宽。</b>标题 Fraunces / 思源宋体，正文 DM Sans / 苹方，金额、Key、代码、表头用 DM Mono。拉丁字母开头的标题首字母可以用花体，中文标题不用花体。</li>
<li><b>插画是黑白排线 + 不规则深色色片。</b>参考 Every 的版画拼贴；背景用树影光斑，参考 Dia 浏览器。不用写实照片、3D 图标或高饱和插画；配色始终在沐仞色卡里。</li>
<li><b>线要轻。</b>官网分隔线黑 8%，后台分隔线暮紫 14%、卡框暮紫 22%，统一 1px。</li>
<li><b>不放示意说明文字。</b>正式界面上不写「示意」「演示数据」「需开发」这类话；交易看板、产地卡这类用示例数字的地方保留「示例」标注，避免被当成真实成交。</li></ul></section>''')

c = ['<section id="color"><h2>色彩</h2><p class="lede">主色只有三组：晨蓝、暮紫、炭黑，雾色用来做晨昏过渡。<span class="mono">--</span> 开头的是代码里的变量名，01_色彩与字体 里有同样内容的 tokens.json / tokens.css。</p>']
for g, items in COLORS:
    c.append(f'<h3>{E(g)}</h3><div class="sws">' + ''.join(sw(n, v, u) for n, v, u in items) + '</div>')
c.append('<h3>透明色（文字层级与线）</h3><div class="alpha">' + ''.join(f'<div><i><em style="background:{v}"></em></i>{E(n)}<code>{E(v)}</code></div>' for n, v in ALPHA) + '</div>')
def gprev(n, v):
    # 白玻璃放在白底上看不出来：叠在现用的树影背景上展示
    if '白玻璃' in n: return f'<i class="glassdemo"><em style="background:{v}"></em></i>'
    return f'<i style="background:{v}"></i>'
c.append('<h3>渐变</h3>' + ''.join(f'<div class="grad">{gprev(n, v)}<div><b>{E(n)}</b><code>{E(v)}</code><p>{E(u)}</p></div></div>' for n, v, u in GRADS))
c.append('<p class="lede" style="margin-top:12px">首页首屏是炭黑底上的一道晨昏光弧（晨蓝 → 暖粉 → 暮紫），见 07_页面截图/电脑/01_首页_首屏.png；它由代码绘制，没有单独的图片文件。</p></section>')
parts.append(''.join(c))

t = ['<section id="type"><h2>字体</h2><p class="lede">拉丁字体都打进了 02_字体文件（SIL OFL 开源授权，可商用）。中文标题用思源宋体（Noto Serif SC），网页从 Google Fonts 加载；中文正文落到系统字体（苹方、冬青黑体）。</p><div class="spec">',
     '<div class="card"><div class="smp" style="font:400 40px/1.15 var(--serif);letter-spacing:-.025em">算电协同 · Green tokens</div><div class="meta"><b>Fraunces · 思源宋体</b>标题、区块大字、后台一级标题</div></div>',
     '<div class="card"><div class="smp" style="font:400 18px/1.6 var(--sans)">统一接口接入主流模型，按词元用量计费。Unified API, billed per token.</div><div class="meta"><b>DM Sans · 苹方</b>正文、界面、按钮</div></div>',
     '<div class="card"><div class="smp" style="font:400 18px/1.6 var(--mono)">¥4.50 / M · sk-••••3a9c · 0123456789</div><div class="meta"><b>DM Mono</b>金额、Key、代码、表头、标签</div></div>',
     '<div class="card"><div class="smp" style="font:400 40px/1.15 var(--serif)"><span style="font-family:HandLatin,var(--serif);font-size:1.3em">A</span>PI Key</div><div class="meta"><b>Pinyon Script（花体首字母）</b>只修饰拉丁字母开头标题的第一个字母，1.3 倍大；中文不用</div></div></div>',
     '<h3>字号</h3><div class="tw"><table><thead><tr><th>用途</th><th>字体</th><th>字号 / 行高</th><th>字重</th></tr></thead><tbody>'
     + ''.join(f'<tr><td>{E(a)}</td><td>{E(b)}</td><td class="mono">{E(cc)}</td><td class="mono">{E(d)}</td></tr>' for a, b, cc, d in TYPE) + '</tbody></table></div></section>']
parts.append(''.join(t))

parts.append('<section id="shape"><h2>圆角、阴影、动效</h2><h3>圆角</h3><div class="kv">' + ''.join(f'<div style="border-radius:{r}"><b class="mono">{E(r)}</b>{E(u)}</div>' for r, u in RADII)
             + '</div><h3>阴影</h3><div class="kv">' + ''.join(f'<div style="border-radius:16px;box-shadow:{v}"><b>{E(n)}</b><code>{E(v)}</code></div>' for n, v in SHADOW)
             + '</div><h3>动效</h3><div class="kv">' + ''.join(f'<div style="border-radius:16px"><b>{E(n)}</b><code>{E(v)}</code></div>' for n, v in EASE)
             + '<div style="border-radius:16px"><b>树影背景</b><code>树影 10s、光斑 13s，ease-in-out 往返；只在可见时播放</code></div><div style="border-radius:16px"><b>减少动态效果</b><code>系统开启 prefers-reduced-motion 时，背景与流程动画全部静止</code></div></div></section>')

parts.append('<section id="comp"><h2>组件</h2><p class="lede">从线上页面截下来的实物（电脑宽度）。点图片看原图。</p><div class="comps">'
             + ''.join(f'<figure><a href="07_页面截图/组件特写/{E(f)}.png"><img src="07_页面截图/组件特写/{E(f)}.png" alt="{E(d)}" loading="lazy"></a><figcaption><b>{E(d)}</b></figcaption></figure>' for f, d in COMPS) + '</div></section>')

parts.append(f'<section id="icon"><h2>图标</h2><p class="lede">后台侧栏的 {len(icons)} 个图标。规格：20 × 20 画布、描边 1.4、圆头圆角、不填色；默认暮紫 #4E3F66，当前项晨蓝 #2F63B8。新增图标照这个规格画。</p><div class="icons">'
             + ''.join(f'<div><img src="03_图标/{E(f)}" alt=""><span>{E(f[3:-4])}</span></div>' for f in icons) + '</div></section>')

a = ['<section id="art"><h2>插画与背景</h2><p class="lede">「现用」按页面里的实际引用核对过。PNG 是原图（可编辑，无分层），WebP 是网页用的压缩版。生成提示词和方向说明在 04_插画与背景 里。</p><h3>现用</h3><div class="arts">']
a += [f'<figure><a href="04_插画与背景/现用/{E(f)}"><img src="04_插画与背景/现用/{E(f)}" alt="{E(n)}" loading="lazy"></a><figcaption><b>{E(n)}</b>{E(d)}</figcaption></figure>' for f, n, d in ART_USED]
a.append('</div><h3>备选（做过，页面没用）</h3><div class="arts">')
a += [f'<figure><a href="04_插画与背景/备选_页面未使用/{E(f)}"><img src="04_插画与背景/备选_页面未使用/{E(f)}" alt="{E(n)}" loading="lazy"></a><figcaption><b>{E(n)}</b></figcaption></figure>' for f, n in ART_SPARE]
a.append('</div></section>')
parts.append(''.join(a))

b = ['<section id="brand"><h2>品牌标识</h2><p class="lede">2026-10-18 定稿：层叠峰面图形 + FATHOMPEAK 转曲英文字标 + 沐仞科技。官方 SVG 是独立路径和渐变，可直接编辑节点，不依赖字体。官网与后台 10-19 已全部换上（旧的双峰山形标在「旧版_2026-10-19前」）。</p><div class="arts">',
     '<figure><a href="05_品牌标识/现用/官方logo_2026-10-18/primary.svg"><img src="05_品牌标识/现用/官方logo_2026-10-18/primary.png" alt="主标组合" style="aspect-ratio:4/3;object-fit:contain;padding:20px;background:#fff"></a><figcaption><b>主标组合</b>图形 + FATHOMPEAK + 沐仞科技，竖排。另有圆形、方形版本和单独图形，都在「官方logo_2026-10-18」。</figcaption></figure>',
     '<figure><a href="05_品牌标识/现用/官方logo_2026-10-18/circle.svg"><img src="05_品牌标识/现用/官方logo_2026-10-18/circle.png" alt="圆形版本" style="aspect-ratio:4/3;object-fit:contain;padding:20px;background:#fff"></a><figcaption><b>圆形 / 方形版本</b>头像、应用图标等方形位置用。</figcaption></figure>',
     '<figure><a href="05_品牌标识/现用/网站用_峰面图形.svg"><img src="05_品牌标识/现用/网站用_峰面图形.svg" alt="峰面图形" style="aspect-ratio:4/3;object-fit:contain;padding:44px;background:#fff"></a><figcaption><b>网站用：峰面图形</b>页头、后台侧栏、关于页、首页演示头像。只替换原来山形标的位置，大小与旧标一致（约 12px 高），不另加文字。</figcaption></figure>',
     '<figure><a href="05_品牌标识/现用/网站用_英文字标.svg"><img src="05_品牌标识/现用/网站用_英文字标.svg" alt="英文字标" style="aspect-ratio:4/3;object-fit:contain;padding:44px;background:#fff"></a><figcaption><b>网站用：英文字标</b>Logo 里的英文 FathomPeak 一律用这个转曲字标，字高与旁边文字接近；不要用普通字体打 FathomPeak。英文模式下「沐仞」会被翻成 FathomPeak，要隐藏，避免和字标重复。</figcaption></figure>',
     '<figure><a href="05_品牌标识/现用/og-1200x630.png"><img src="05_品牌标识/现用/og-1200x630.png" alt="分享图"></a><figcaption><b>分享图 1200 × 630</b>微信、社交平台转发时的预览图；左上角是新图形和字标。</figcaption></figure>',
     '<figure><a href="05_品牌标识/现用/icon-512.png"><img src="05_品牌标识/现用/icon-512.png" alt="应用图标" style="aspect-ratio:4/3;object-fit:contain;padding:30px"></a><figcaption><b>网站图标</b>favicon.svg、192 / 512 PNG、apple-touch-icon。渐变底不变，白色新图形。</figcaption></figure>',
     '<figure><a href="05_品牌标识/现用/微信公众号二维码.png"><img src="05_品牌标识/现用/微信公众号二维码.png" alt="微信公众号二维码" style="aspect-ratio:4/3;object-fit:contain;padding:30px;background:#fff"></a><figcaption><b>微信公众号二维码</b>官网页脚「联系我们」和右下角咨询浮窗用：白色圆角卡片 + 柔和投影，不加描边和光晕，下方写「微信扫一扫」。</figcaption></figure></div>',
     '<p class="lede"><b>登录插画</b>（04_插画与背景/现用 里的握手版画）保持原图，里面的「FathomPeak Tech」仍是旧字样，等插画重画时再换。</p>',
     '<h3>Logo 探索稿 <span class="tag warn">定稿前</span></h3><p class="lede">10-14 做的几轮方向探索。2026-10-18 已选定层叠峰面，以下只作回溯，不要当正式标识使用。</p><div class="arts">']
b += [f'<figure><a href="05_品牌标识/探索稿_未定稿/{E(f)}"><img src="05_品牌标识/探索稿_未定稿/{E(f)}" alt="" loading="lazy"></a><figcaption>{E(f[:-4])}</figcaption></figure>' for f in explore]
b.append('</div></section>')
parts.append(''.join(b))

parts.append('''<section id="logo"><h2>第三方 Logo</h2><p class="lede">模型厂商 Logo（DeepSeek、通义千问、智谱、MiniMax）用在模型目录和后台渠道，保持原色。合作方 Logo（国家电网、隆基、中广核、京东方、深圳燃气、昇腾、英伟达初创加速计划、Soul）是之前首页用过的，目前页面上没有展示。</p>
<div class="note"><p>这些是别家的商标。正式对外使用前，需要确认对方同意展示，并按对方的品牌规范使用（不改色、不变形、留足安全距离）。</p></div></section>''')

pg = ['<section id="pages"><h2>页面截图</h2><p class="lede">电脑截图宽 1440，手机截图宽 390（两倍像素）。都是首屏或该区块的一屏，不是整页长图。后台数据都是空状态，没有编造的业务数据。</p><div class="pages">']
pg += [f'<figure><a href="07_页面截图/电脑/{E(f)}.png"><img src="07_页面截图/电脑/{E(f)}.png" alt="{E(n)}" loading="lazy"></a><figcaption><b>{E(n)}</b><a href="07_页面截图/电脑/{E(f)}.png">电脑</a><a href="07_页面截图/手机/{E(f)}.png">手机</a></figcaption></figure>' for f, n in PAGES]
pg.append('</div></section>')
parts.append(''.join(pg))

parts.append('''<section id="ref"><h2>参考与历史</h2><ul class="rules">
<li><b>Dia 浏览器（diabrowser.com）</b>：后台的树影光斑背景、半透明表面、细线的参考。只借鉴质感，配色仍用沐仞色卡。</li>
<li><b>Every（every.to）</b>：排线拼贴插画、英文标题花体首字母的参考。</li>
<li><b>08_参考与历史文档/设计交接_2026-10-14.md</b>：上一版设计交接，色彩和组件参数大部分仍然对；登录页、后台分身份、超管、财务那部分以本页为准。</li>
<li><b>设计交接幻灯片_2026-10-13.pdf</b>：更早的快照，首页布局已改，只作回溯。</li>
<li><b>色彩过渡研究_2026-10-13.pdf</b>：「晨昏蓝」配色和渐变过渡是怎么定下来的。</li>
<li><b>竞品品牌视觉调研板_2026-10-12.pdf</b>：同类平台的视觉调研。</li></ul></section>''')

parts.append('''<section id="open"><h2>还没定的</h2><div class="note">
<p><b>Logo：</b>2026-10-18 已定为层叠峰面，官网与后台已换上。只差登录插画里的「FathomPeak Tech」旧字样，要等插画重画时一起换。</p>
<p><b>中文字体：</b>标题用的思源宋体从 Google Fonts 加载，国内访问可能慢；正式上线前要么自托管思源宋体（开源，可商用），要么换成有商用授权的中文字体。</p>
<p><b>超管和财务后台：</b>还在改，侧栏名称和分组可能再变（比如「路由与转换」会改名「路由与可靠性」）；视觉规范不变。</p>
<p><b>「种树」减碳反馈：</b>按公司要求，用户侧要能直观看到自己用了绿电、减了碳（类似支付宝种树）。这块的插画和交互还没做，需要视觉团队一起设计。</p>
<p><b>没有 Figma 文件：</b>如果要建设计库，可以从 01_色彩与字体/tokens.json 导入变量，组件照 07_页面截图/组件特写 还原。</p></div></section>''')
if WEB:
    fl = ['<section id="files"><h2>全部文件下载</h2><p class="lede">点文件名打开或下载。手机上想存图片，长按图片保存；要一次拿全部，用页面顶部的「下载整包」。</p><div class="files">']
    for top in sorted(d for d in os.listdir(P) if os.path.isdir(os.path.join(P, d)) and d[:2].isdigit()):
        fl.append(f'<h3>{E(top)}</h3><ul>')
        for d, _, fs in sorted(os.walk(os.path.join(P, top))):
            for f in sorted(fs):
                if f.startswith('.'): continue
                fp = os.path.join(d, f); rel = os.path.relpath(fp, P)
                fl.append(f'<li><a href="{E(rel)}" download>{E(os.path.relpath(fp, os.path.join(P, top)))}</a><span>{human(os.path.getsize(fp))}</span></li>')
        fl.append('</ul>')
    fl.append('</div></section>')
    parts.append(''.join(fl))
parts.append('</main></div></body></html>\n')
page = ''.join(parts)
if WEB:
    zsize = human(os.path.getsize(os.path.join(P, WEB))) if os.path.exists(os.path.join(P, WEB)) else ''
    page = page.replace('{DLBAR}', f'<div class="dl"><a class="btn" href="{E(WEB)}" download>下载整包（ZIP，{zsize}）</a><span>微信里点下载没反应：点右上角「…」，选「在浏览器打开」再下载。</span></div>')
    open(os.path.join(P, 'index.html'), 'w', encoding='utf8').write(page)
else:
    open(os.path.join(P, '00_先看这个.html'), 'w', encoding='utf8').write(page.replace('{DLBAR}', ''))
print('done', len(icons), 'icons', len(explore), 'explorations')
