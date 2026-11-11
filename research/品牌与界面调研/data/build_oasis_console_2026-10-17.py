"""把「绿洲」作为用户后台里的一页接进控制台（Zixin 2026-10-17：「这个是在用户后台界面里的一个环节而已，不是单独的界面」）。
叠在线上 index.html（c5c5450）上，只生成预览，不改线上，也不改 Codex 的原型文件。
 · 侧栏「用量与订单」之后加「绿洲」（个人、企业管理员、企业成员可见；超管不显示）。
 · 概览右栏加一行绿洲入口，显示当前树和阶段。
 · 绿洲页（第二版，Zixin 10-17 指出第一版使用逻辑有问题、地图局促后重写）：
   调用 → 能量球 → 点一下收进当前树，4 份长成 → 送代金券进钱包 + 开种袋，下一颗自动种下；
   营地种满自动开放溪畔、林地，不手动扩建；地图通栏，未开放区域只轻雾化；当前树状态在地图底栏。
   原型里体验中心每发一条消息算一次调用；侧栏「绿洲」有待收能量角标。
 · 钱包「代金券」显示绿洲送的券。
 · 插画用 Codex 10-18 交付的 A 版蚀刻 PNG（转 webp）：荒漠绿洲场景 + 5×2 成长图集；坑位改为前后错开。
   玩法不再沿用 Codex 的 reducer（第一版用过）。
用法：python3 -I build_oasis_console_2026-10-17.py <线上 index.html> <输出 html> <Codex 原型目录> [<预览目录/art/oasis>]
"""
import sys
from pathlib import Path

SRC, OUT, CODEX = sys.argv[1], sys.argv[2], Path(sys.argv[3])
ART_OUT = Path(sys.argv[4]) if len(sys.argv) > 4 else None
HERE = Path(__file__).resolve().parent
s = open(SRC, encoding='utf8').read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: sys.exit(f'[停止] 匹配 {c} 次（应为 {n}）：{old[:90]}')
    s = s.replace(old, new)


SPROUT = '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M10 17V9.5M10 11.5C10 8 7.6 6.3 4 6.3c0 3.5 2.4 5.2 6 5.2ZM10 9.5c0-3 2-4.7 5.6-4.7 0 3-2 4.7-5.6 4.7ZM5.5 17h9" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
CHEV = '<svg class="bt-chev" viewBox="0 0 16 16" aria-hidden="true"><path d="M2.5 8h10M9 4.5l3.5 3.5L9 11.5" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ROLES = 'personal member admin'

# 1 侧栏：绿电批量任务之前（运行时「用量与订单」会被移到 API Key 后，绿洲紧随其后）
rep('<button type="button" data-p="batch" class="sup-new">',
    f'<button type="button" data-p="oasis" data-roles="{ROLES}">{SPROUT}<span>绿洲</span></button>\n        <button type="button" data-p="batch" class="sup-new">')

# 2 页面：放在绿电批量任务页之前
PAGE = ('<div class="cs-p" data-p="oasis">\n'
        '        <div class="cs-hd"><div><h2>绿洲</h2><p>在平台上的每次调用都会变成能量，让绿洲里的树长大。树长成后送代金券，绿洲也会慢慢变大。</p></div>'
        '<div class="oa-acts"><button class="btn gray sm" type="button" data-oa="rules" data-oa-top>怎么玩</button><button class="btn gray sm" type="button" data-oa="reset" data-oa-top>重新开始</button></div></div>\n'
        '        <div class="oa" id="oaRoot"></div>\n      </div>\n      ')
rep('<div class="cs-p" data-p="batch">', PAGE + '<div class="cs-p" data-p="batch">')

# 3 弹层放在 body 层级（页面隐藏时也能正常打开）
rep('<div class="toast" id="toast" role="status" aria-live="polite"></div>',
    '<dialog class="cs-dlg" id="oaDlg" aria-labelledby="oaDlgT"><div class="cs-dlg-hd"><h3 id="oaDlgT"></h3><button class="cs-x" type="button" data-oa="close" aria-label="关闭">×</button></div><div class="oa-dlgb" id="oaDlgB"></div></dialog>\n'
    '<div class="toast" id="toast" role="status" aria-live="polite"></div>')

# 4 概览右栏入口
rep('</svg></button>\n      </div>\n      <div class="bt-rs bt-stats">',
    f'</svg></button>\n        <button class="bt-row oa-rail" type="button" data-go="oasis" data-roles="{ROLES}"><i>{SPROUT}</i><span id="oaRailT">绿洲</span>{CHEV}</button>\n      </div>\n      <div class="bt-rs bt-stats">')

# 5 钱包代金券
rep('<div class="cs-empty sup-new">还没有代金券。活动或商务赠送的代金券会显示在这里，优先于余额扣费。</div>',
    '<div class="cs-empty sup-new" id="oaWalletEmpty">还没有代金券。活动或商务赠送的代金券会显示在这里，优先于余额扣费。</div><div class="oa-wallet" id="oaWallet" hidden></div>')

# 6 样式
css = (HERE / 'oasis_console_2026-10-17.css').read_text(encoding='utf8')
rep('</head>', '<style id="oasis-console">\n' + css + '</style>\n</head>')

# 7 脚本：绿洲界面与逻辑
ui = (HERE / 'oasis_console_2026-10-17.js').read_text(encoding='utf8')
rep("  window.addEventListener('hashchange',route); route();", ui + "\n  window.addEventListener('hashchange',route); route();")

open(OUT, 'w', encoding='utf8').write(s)
print('done:', OUT)

# 8 插画：Codex 10-18 交付的 A 版蚀刻 PNG 转 webp（不改原图；见 art/交付索引_etched_2026-10-18.md）
if ART_OUT:
    from PIL import Image
    ART_OUT.mkdir(parents=True, exist_ok=True)
    for name in ['oasis-world_etched_2026-10-18', 'oasis-growth_etched_2026-10-18']:
        try:
            im = Image.open(CODEX / 'art' / (name + '.png'))
            im.save(ART_OUT / (name + '.webp'), 'WEBP', quality=86, method=6)
            print('art:', name, (ART_OUT / (name + '.webp')).stat().st_size, 'bytes')
        except Exception as exc:
            sys.exit(f'[停止] 插画转换失败 {name}: {exc}')
