"""控制台里加回中英文切换（Zixin 2026-10-14："我们的后台好像没有切换中英文的功能了？"）。
原因：50c2da4（10-14 04:15，控制台改 Baseten 式外壳）加了 html.in-console .hdr,footer,.menu,.fab{display:none}，
中英切换只在顶部导航里，进控制台后整条导航被隐藏，控制台外壳自己又没有切换入口。
做法：在控制台右上角通知铃旁加一个 .lang 胶囊（与铃同样的白玻璃样式）。站点现有的 .lang 点击处理与文字更新
（EN ↔ 中文）对所有 .lang 元素生效，所以不用新写切换逻辑；手机端也可见（侧栏底部在手机上被隐藏，不放那里）。
用法：python3 -I build_console_lang_toggle_2026-10-14.py <源 index.html> <输出 html>
"""
import json, sys

SRC, OUT = sys.argv[1], sys.argv[2]
s = open(SRC, encoding='utf8').read()

old = '<div class="bt-bellw"><button class="bt-bell"'
if s.count(old) != 1: sys.exit(f'[停止] 通知铃位置匹配 {s.count(old)} 次（应为 1）')
s = s.replace(old, '<div class="bt-bellw"><a class="lang bt-lang" href="#" role="button" aria-label="切换语言">EN</a><button class="bt-bell"')

CSS = '''
<style id="bt-lang-css">
/* 控制台右上角中英切换（2026-10-14）：与通知铃同款白玻璃胶囊 */
.bt-bellw{display:flex;align-items:center;gap:8px}
.bt-lang{height:34px;min-width:46px;padding:0 12px;border-radius:999px;border:1px solid var(--glass-line);background:var(--glass);box-shadow:var(--dia-sh);
  backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);display:inline-flex;align-items:center;justify-content:center;
  font:500 12px/1 var(--mono);letter-spacing:.06em;color:var(--ink-70);text-decoration:none;cursor:pointer;transition:box-shadow .3s var(--out),color .2s var(--ease)}
.bt-lang:hover{color:var(--ink);box-shadow:var(--dia-sh2)}
.bt-lang:focus-visible{outline:2px solid var(--blue-1);outline-offset:2px}
</style>
'''
k = s.rindex('</head>'); s = s[:k] + CSS + s[k:]
k2 = s.index('var I18N={') + len('var I18N={')
s = s[:k2] + json.dumps('切换语言', ensure_ascii=False) + ':' + json.dumps('Switch language') + ',' + s[k2:]
open(OUT, 'w', encoding='utf8').write(s)
print('done:', OUT)
