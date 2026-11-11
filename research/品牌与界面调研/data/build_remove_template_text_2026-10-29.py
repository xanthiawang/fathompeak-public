"""删掉官网 UI 里的模板性文字（Zixin 2026-10-29：「模版文字全部删了」；规则见 memory feedback-no-template-labels-in-ui）。
只改用户看得到的文字；英文字典里残留的旧键不碰（不显示）。每条替换同时给新中文配英文，并强制覆盖字典。
用法：python3 -I build_remove_template_text_2026-10-29.py <站点根目录>
"""
import json, sys
from pathlib import Path

p = Path(sys.argv[1]) / 'index.html'
s = p.read_text(encoding='utf8')
if 'template-text-removed-20261029' in s: sys.exit('[停止] 已经改过')

# (旧, 新, 预期次数)
R = [
    ('<span>产地卡 · 示例</span>', '<span>产地卡</span>', 1),
    ('<span>产地卡可以用在</span><span>示例</span>', '<span>产地卡可以用在</span>', 1),
    ('<i class="rt-soon">待接入</i>', '', 6),
    ('<p>本页数值为示例。</p>', '', 1),
    ("'<div class=\"msg\">演示环境不发起真实调用；获取 FathomPeak Key 后，用 curl 跑第一条请求。</div>", "'<div class=\"msg\">获取 FathomPeak Key 后，用 curl 跑第一条请求。</div>", 1),
    ('<span class="tag">示例样刊</span>', '', 1),
    ('<p class="note">¥ / 百万 Token。沐仞价为示例。</p>', '<p class="note">¥ / 百万 Token</p>', 1),
    ("<p class=\"note\">示例样刊。窗口是什么？读 <a", "<p class=\"note\">窗口是什么？读 <a", 1),
    ("toast('原型阶段不发送验证码，输入任意 6 位数字即可。')", "toast('输入任意 6 位数字即可。')", 1),
    ('<div class="on">交易展示</div>', '<div class="on">Token 交易</div>', 1),
    ('<span>Token 交易展示</span>', '<span>Token 交易</span>', 1),
    ('<span class="t">交易展示</span>', '<span class="t">产地与价格</span>', 1),
]
for old, new, n in R:
    c = s.count(old)
    if c != n: sys.exit(f'[停止] 匹配 {c} 次（应为 {n}）：{old[:80]}')
    s = s.replace(old, new)

EN = {
    '获取 FathomPeak Key 后，用 curl 跑第一条请求。': 'Get a FathomPeak Key, then run your first request with curl.',
    '窗口是什么？读': 'What is a window? Read',
    '输入任意 6 位数字即可。': 'Enter any 6 digits.',
    'Token 交易': 'Token trading',
    '产地与价格': 'Origins and prices',
}
s = s.replace('  syncAuthLocale(); applyLang();', '  (function(S){for(var k in S) I18N[k]=S[k]})(' + json.dumps(EN, ensure_ascii=False) + ');  /* template-text-removed-20261029 */\n  syncAuthLocale(); applyLang();', 1)
p.write_text(s, encoding='utf8')
print('done')
