"""线上首页只上两处（Zixin 2026-10-14："把修改好的这两个问题上线"）：
1 首屏副文案改为 Zixin 给的两行：
  "GLM、DeepSeek、Qwen、MiniMax，兼容 OpenAI 与 Gemini。" / "一体机部署在电站旁，用富余绿电生产词元，价低至 5 折。"
  （她原文把 OpenAI、Gemini 和模型并列；我们卖的是这四家模型，OpenAI/Gemini 是兼容的接口格式，所以写"兼容"。标题与"低成本、高可用、全兼容。"不变。）
2 项目案例"某头部社交平台"→"Soul"（与首页滚动 logo 一致；信息表：已与 Soul 达成战略合作、WAIC2026 战略合作伙伴）。
其余审查修改（电站合作一节、按钮、对比度、手机排版等）仍只在预览里。
用法：python3 -I build_home_hero_sub_soul_2026-10-14.py <仓库 index.html>
"""
import json, sys

P = sys.argv[1]
s = open(P, encoding='utf8').read()
NB = ' '
SUB1 = 'GLM、DeepSeek、Qwen、MiniMax，兼容 OpenAI 与 Gemini。'
SUB2 = f'一体机部署在电站旁，用富余绿电生产词元，价低至 5{NB}折。'


def home_rep(old, new):
    global s
    a = s.index('<div id="home2">'); b = s.index('<section data-route=', a)
    c = s[a:b].count(old)
    if c != 1: sys.exit(f'[停止] 首页内匹配 {c} 次（应为 1）：{old[:60]}')
    s = s[:a] + s[a:b].replace(old, new) + s[b:]


home_rep('<p class="sub">GLM、DeepSeek、Qwen、MiniMax 一个端点接入，兼容 OpenAI 与 Gemini 原生格式。一体机部署在电站旁，用富余绿电生产词元，为 AI 企业提供低成本、可追溯的推理服务。</p>',
         f'<p class="sub">{SUB1}<br>{SUB2}</p>')
home_rep('<b>某头部社交平台</b>', '<b>Soul</b>')

EN = {SUB1: 'GLM, DeepSeek, Qwen and MiniMax, compatible with OpenAI and Gemini.',
      SUB2: 'Appliances beside power plants turn surplus green power into tokens, at up to 50% off.'}
k = s.index('var I18N={') + len('var I18N={')
s = s[:k] + ''.join(json.dumps(a, ensure_ascii=False) + ':' + json.dumps(b, ensure_ascii=False) + ',' for a, b in EN.items()) + s[k:]
open(P, 'w', encoding='utf8').write(s)
print('done.')
