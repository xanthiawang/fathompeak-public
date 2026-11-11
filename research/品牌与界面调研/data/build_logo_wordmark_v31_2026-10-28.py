"""logo 字标按官方 v31 统一（Zixin 2026-10-28：「logo 不对，不是我们标准的字体」）。
依据：品牌素材 05_品牌标识/现用/官方logo_2026-10-18/字体规范_2026-10-20.md ——
  字标是定制轮廓，没有可安装字体，「不要用 Noto Serif、Songti SC、普通无衬线字……重新输入替代」，
  「正式排版直接放置 wordmark-en.svg / wordmark-zh.svg」；「中文全称保留『沐仞科技』，本次不将公司全称缩写为『沐仞』」。
网站原来的问题：
 · 中文：官网手机页头、关于页、小程序页头用字体打的「沐仞」，小程序入口页用字体打的「沐仞科技」→ 换成官方中文字标「沐仞科技」
 · 英文：10-19 从旧版主标拆出的 FATHOMPEAK（v30 之前），和 v31 的 wordmark-en.svg 路径不同 → 换成 v31
 · 图形（峰面）与官方一致，不动
英文模式仍只显示英文字标（中文字标带 fp-cn / wm 类，英文模式隐藏）。
第二轮（Zixin：「导航 bar 的 logo 要改成带文字的；最后页面底部加上我们完整的带文字和符号的 logo」，参考无问芯穹页脚）：
 · 导航胶囊：电脑端原来只有图形 → 图形 + 中文字标「沐仞科技」（英文版图形 + FATHOMPEAK）。官方没有横排组合，用的是官方独立字标
 · 页脚第一栏「联系我们」上方放官方主标 primary.svg（图形 + FATHOMPEAK + 沐仞科技，规范里的完整组合）
用法：python3 -I build_logo_wordmark_v31_2026-10-28.py <站点根目录> <官方 logo 目录（含 wordmark-en.svg、wordmark-zh.svg）>
"""
import shutil, sys
from pathlib import Path

ROOT, SRC = Path(sys.argv[1]), Path(sys.argv[2])
EN, ZH = 'art/brand/fathompeak-wordmark-en_v31.svg', 'art/brand/fathompeak-wordmark-zh_v31.svg'
PRIMARY = 'art/brand/fathompeak-primary_v31.svg'
OLD = 'art/brand/fathompeak-wordmark_2026-10-19.svg'
shutil.copyfile(SRC / 'wordmark-en.svg', ROOT / EN)
shutil.copyfile(SRC / 'wordmark-zh.svg', ROOT / ZH)
shutil.copyfile(SRC / 'primary.svg', ROOT / PRIMARY)


def edit(rel, pairs):
    p = ROOT / rel; s = p.read_text(encoding='utf8')
    for old, new, n in pairs:
        c = s.count(old)
        if c != n: sys.exit(f'[停止] {rel} 匹配 {c} 次（应为 {n}）：{old[:90]}')
        s = s.replace(old, new)
    if OLD in s: sys.exit(f'[停止] {rel} 还有旧英文字标')
    p.write_text(s, encoding='utf8'); print('edited', rel)


edit('index.html', [
    # 页头：电脑端只显示图形（原样）；手机端中文显示中文字标、英文显示英文字标
    # 第三轮（Zixin 参考硅基流动页头：图形 + 中文大字 + 英文小字上下叠放，中英文版都显示）
    (f'<span class="wm">沐仞</span><img class="wm-en" src="{OLD}" width="138" height="10" alt="FathomPeak">',
     f'<span class="wm-stack"><img class="wm wm-zh" src="{ZH}" width="70" height="16" alt="沐仞科技"><img class="wm-en" src="{EN}" width="70" height="5" alt="FathomPeak"></span>', 1),
    # 关于页标题上方：图形 + 中文字标 + 英文字标
    (f'<span class="fp-cn">沐仞</span><img class="ab-wm" src="{OLD}" width="138" height="10" alt="FathomPeak">',
     f'<img class="fp-cn ab-wmzh" src="{ZH}" width="57" height="13" alt="沐仞科技"><img class="ab-wm" src="{EN}" width="140" height="10" alt="FathomPeak">', 1),
    # 页脚第一栏上方：官方主标
    ('<footer>\n  <div class="cols">\n    <div class="co"><span class="k">联系我们</span>',
     f'<footer>\n  <div class="cols">\n    <div class="co"><a class="f-logo" href="#home" aria-label="沐仞科技 FathomPeak 首页"><img src="{PRIMARY}" width="180" height="97" alt="沐仞科技 FATHOMPEAK"></a><span class="k">联系我们</span>', 1),
    ('</head>', '<style id="logo-wordmark-v31-20261028">\n'
     '/* logo 字标按官方 v31（2026-10-28）：中英文都放字标图，不用字体打字。站点主样式在 body 里、晚于本段，选择器加前缀 */\n'
     '/* 导航胶囊：图形 + 中文大字 + 英文小字上下叠放（参考硅基流动页头），中英文版都显示 */\n'
     '.hdr .pill .logo{width:auto;padding:0 10px 0 8px;gap:8px}\n'
     '.hdr .pill .logo .wm-stack{display:flex;flex-direction:column;align-items:flex-start;gap:3px;margin-left:2px}\n'
     '.hdr .pill .logo img.wm-zh{display:block;height:15px;width:auto;margin:0}\n'
     '.hdr .pill .logo .wm-en{display:block;height:5px;width:auto;margin:0}\n'
     'html[lang="en"] .hdr .pill .logo .wm{display:block}\n'
     'html[lang="en"] .ab-head .ab-mk .ab-wmzh{display:none}\n'
     '/* 窄电脑屏放不下叠放字标时只留图形（实测：中文 860px、英文 950px 起导航才不换行） */\n'
     '@media (min-width:801px) and (max-width:859px){.hdr .pill .logo .wm-stack{display:none}.hdr .pill .logo{width:40px;padding:0}}\n'
     '@media (min-width:801px) and (max-width:949px){html[lang="en"] .hdr .pill .logo .wm-stack{display:none}html[lang="en"] .hdr .pill .logo{width:40px;padding:0}}\n'
     '/* 页脚主标 */\n'
     'footer .co .f-logo{display:block;width:max-content;margin:0 0 28px}\n'
     'footer .co .f-logo img{width:180px;height:auto;display:block}\n'
     '.ab-head .ab-mk .ab-wmzh{height:13px;width:auto;display:block}\n'
     '.ab-head .ab-mk .ab-wmt{gap:10px}\n'
     '</style>\n</head>', 1),
])

edit('mini-preview/index.html', [
    (f'<button class="mini-brand" data-nav="home" aria-label="返回首页">沐仞<span><img src="../{OLD}" width="111" height="8" alt="FathomPeak"></span></button>',
     f'<button class="mini-brand" data-nav="home" aria-label="返回首页"><img class="mb-zh" src="../{ZH}" width="70" height="16" alt="沐仞科技"><span><img src="../{EN}" width="111" height="8" alt="FathomPeak"></span></button>', 1),
    (f'<img src="../{OLD}" width="208" height="15" alt="FathomPeak"><span>沐仞科技</span>',
     f'<img src="../{EN}" width="208" height="15" alt="FathomPeak"><span><img class="wm-zh" src="../{ZH}" width="65" height="15" alt="沐仞科技"></span>', 1),
])
css = ROOT / 'mini-preview/styles.css'
c = css.read_text(encoding='utf8')
if 'mb-zh' not in c:
    css.write_text(c.rstrip('\n') + '\n/* logo 字标按官方 v31（2026-10-28）：中文用「沐仞科技」字标图，不用字体打字 */\n'
                   '.mini-brand{align-items:center}\n.mini-brand .mb-zh{height:16px;width:auto;display:block}\n'
                   '.wordmark span img.wm-zh{height:15px;width:auto;display:block}\n', encoding='utf8')
    print('edited mini-preview/styles.css')
print('done')
