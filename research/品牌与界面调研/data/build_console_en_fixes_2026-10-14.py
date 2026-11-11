"""控制台两处英文问题（Zixin 2026-10-14："把 1 members 和 API Key 花体也修了"）：
1 花体首字母：原逻辑"控制台（.bt）里以拉丁字母开头的衬线标题中英文模式都加手写首字母"（如 h1"API Key"的花体 A）。
  改为控制台里一律不加；其他页面英文模式下的大标题照旧。
2 单复数：右栏"1 位成员 / 1 个 API Key"在英文里译成"1 members / 1 API keys"。
  数量为 1 时用带零宽空格的中文键（中文显示不变），英文表里对应 member / API key；其他数量仍是 members / API keys。
用法：python3 -I build_console_en_fixes_2026-10-14.py <index.html>（原地修改）
"""
import json, sys

P = sys.argv[1]
s = open(P, encoding='utf8').read()


def rep(old, new):
    global s
    c = s.count(old)
    if c != 1: sys.exit(f'[停止] 匹配 {c} 次（应为 1）：{old[:70]}')
    s = s.replace(old, new)


rep("/* 控制台（.bt）里以拉丁字母开头的衬线标题中英文模式都加手写首字母 */",
    "/* 手写首字母只用于控制台以外的页面、英文模式下以拉丁字母开头的衬线大标题；控制台（.bt）里不加（Zixin 2026-10-14：去掉\"API Key\"花体） */")
rep("var inC=!!el.closest('.bt'), on=(lang==='en'||inC)&&/^[A-Za-z]/.test(el.textContent.trim());",
    "var inC=!!el.closest('.bt'), on=!inC&&lang==='en'&&/^[A-Za-z]/.test(el.textContent.trim());")
rep("$('#btKeyN').innerHTML='<b>'+me.keys.length+'</b> <span>个 API Key</span>';",
    "var _kn=me.keys.length; $('#btKeyN').innerHTML='<b>'+_kn+'</b> <span>'+(_kn===1?'个 API Key\\u200b':'个 API Key')+'</span>';  /* \\u200b：数量为 1 时英文用单数 */")
rep("$('#btMem').innerHTML='<b>'+((me.subs||[]).length+1)+'</b> <span>位成员</span>';",
    "var _mn=(me.subs||[]).length+1; $('#btMem').innerHTML='<b>'+_mn+'</b> <span>'+(_mn===1?'位成员\\u200b':'位成员')+'</span>';  /* \\u200b：数量为 1 时英文用单数 */")

EN = {'个 API Key​': 'API key', '位成员​': 'member'}
k = s.index('var I18N={') + len('var I18N={')
s = s[:k] + ''.join(json.dumps(a, ensure_ascii=False) + ':' + json.dumps(b) + ',' for a, b in EN.items()) + s[k:]
open(P, 'w', encoding='utf8').write(s)
print('done.')
