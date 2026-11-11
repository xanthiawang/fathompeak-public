"""首页结尾文案（Zixin 2026-10-14）：
- 大标题仿 "One idea, every format, all in your brand style." → "一个平台，低至半价，/ 连起所有的 AI 工具。"
  （Zixin 原话"半价"；报价单 2026-10-08 只有 GLM-5.3 是 5 折，其余 6–8.2 折，所以写"低至半价"，与下方折扣区间一致）
- 副句 → 折扣区间"企业报价 5 折 – 8.2 折"（报价单：GLM-5.3 0.5 … kimi-k3 0.82）
- 最下面的说明 → "从一次真实任务测试开始"
用法：python3 -I build_home_end_copy_2026-10-14.py <index.html 或原型.html> [...]（有 I18N 的文件同时补英文）
"""
import json, sys

NB = ' '
H_OLD = '<h2 class="rv">让电站的富余绿电，跑你的 AI。</h2>'
L1, L2 = '一个平台，低至半价，', '连起所有的 AI 工具。'
H_NEW = f'<h2 class="rv">{L1}<br>{L2}</h2>'
S_OLD = '<p class="end-sub rv">从一次真实任务测试开始</p>'
SUB = f'企业报价 5{NB}折{NB}–{NB}8.2{NB}折'
S_NEW = f'<p class="end-sub rv">{SUB}</p>'
N_OLD = '<p class="rv d2">先完成一次小规模调用，再验证质量、时延与费用</p>'
N_NEW = '<p class="rv d2">从一次真实任务测试开始</p>'
EN = {L1: 'One platform, as low as half price,', L2: 'for all your AI tools.', SUB: 'Enterprise quotes: 18%–50% off list price'}

for path in sys.argv[1:]:
    s = open(path, encoding='utf8').read()
    k = s.find('var I18N={')
    pre, post = (s[:k], s[k:]) if k >= 0 else (s, '')
    for old, new in ((H_OLD, H_NEW), (S_OLD, S_NEW), (N_OLD, N_NEW)):
        c = pre.count(old)
        if c != 1: sys.exit(f'[停止] {path}: 匹配 {c} 次（应为 1）：{old[:50]}')
        pre = pre.replace(old, new)
    s = pre + post
    if k >= 0:
        k2 = s.index('var I18N={') + len('var I18N={')
        s = s[:k2] + ''.join(json.dumps(a, ensure_ascii=False) + ':' + json.dumps(b, ensure_ascii=False) + ',' for a, b in EN.items()) + s[k2:]
    open(path, 'w', encoding='utf8').write(s)
    print('done:', path, '(+EN)' if k >= 0 else '')
