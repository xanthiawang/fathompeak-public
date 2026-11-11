"""登录页插画被顶部导航条压住（Zixin 2026-10-19：「图片和我们的导航 bar 重叠了」）。
原因：.ac 只留 12px 上边距，插画按整屏高度画，从顶部 12px 开始；导航胶囊固定在顶部 28–80px，正好压在插画上半截。
改法：只在电脑宽度（>800px，插画可见时）给用户登录页的 .ac 加 96px 上边距（导航底 80px + 16px 间距），
插画列宽按剩余高度重算（(100svh − 96 − 12) × 2/3），整张图仍在一屏内、比例不变。运营后台登录（.ad-login）不显示导航，不改。
用法：python3 -I build_login_art_below_nav_2026-10-19.py <站点仓库根目录>
"""
import sys
from pathlib import Path

p = Path(sys.argv[1]) / 'index.html'; s = p.read_text(encoding='utf8')
old = '</head>'
if s.count(old) != 1: sys.exit('[停止] </head> 不唯一')
if 'id="login-below-nav-20261019"' in s: sys.exit('[停止] 已经加过')
css = ('<style id="login-below-nav-20261019">\n'
       '/* 登录页插画让出顶部导航（2026-10-19）：导航胶囊固定在 28–80px，插画从 96px 开始，按剩余高度保持 2:3 */\n'
       '@media (min-width:801px){.ac:not(.ad-login){padding-top:96px;grid-template-columns:minmax(0,min(48%,calc((100svh - 108px)*.666667))) minmax(0,1fr)}}\n'
       '</style>\n</head>')
p.write_text(s.replace(old, css), encoding='utf8')
print('done')
