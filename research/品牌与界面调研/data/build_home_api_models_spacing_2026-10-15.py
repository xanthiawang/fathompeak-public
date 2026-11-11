"""首页「怎么用」01 改口径 + 产品页分段（Zixin 2026-10-15）。叠在 build_remove_notes 的输出上。
 1 "这个逻辑有点不太对。我们是直接给他们 API，他们拿到 API Key 就可以用"：
   首页 01「改一行地址，就接上了」（把 api.openai.com 划掉换成沐仞地址，像是从 OpenAI 迁移）改成「拿到 API Key，就能调用」；
   右侧示意窗不再划掉 OpenAI 地址，改成两行配置：API Key + 接入地址；去掉底部「示例」标签；链接改为「获取 API Key →」。
   文档里「从 OpenAI 迁移」那篇指南的 base_url 对比不动（那篇本来就是讲迁移的）。
 2 "第二个页面感觉正文几个部分粘连在一起了"：产品与服务页各产品之间只有留白，没有分隔。
   改：相邻两个产品之间加一条细线和上方留白；同一产品下的子栏目（模型市场、节点定价）用更浅的线，留白小一些。
用法：python3 -I build_home_api_models_spacing_2026-10-15.py <输入 html> <输出 html>
"""
import json, sys

SRC, OUT = sys.argv[1], sys.argv[2]
s = open(SRC, encoding='utf8').read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: sys.exit(f'[停止] 匹配 {c} 次（应为 {n}）：{old[:80]}')
    s = s.replace(old, new)


T1 = '拿到 API Key，就能调用'
P1 = '在控制台创建 API Key，填上接入地址，就能调用 GLM、DeepSeek、Qwen、MiniMax 等主流模型；OpenAI 与 Gemini 调用格式都兼容。'
rep('<b>改一行地址，就接上了</b><div class="more"><div><p>一行地址，接入 GLM、DeepSeek、Qwen、MiniMax 等主流模型；OpenAI 与 Gemini 调用格式都兼容。</p><a class="ul" href="#models">浏览模型市场 →</a></div></div>',
    f'<b>{T1}</b><div class="more"><div><p>{P1}</p><a class="ul" href="#login">获取 API Key →</a></div></div>')
rep('<div class="sw-diff"><span class="k">base_url</span><s>api.openai.com/v1</s><span class="ar">→</span><b>api.fathompeak.cn/v1</b></div>',
    '<div class="sw-diff sw-cfg"><span class="k">API Key</span><b>sk-••••••••••••</b><span class="k">base_url</span><b>api.fathompeak.cn/v1</b></div>')
rep('<span>用量计入订单</span><span class="ex">示例</span></div>', '<span>用量计入订单</span></div>')

CSS = '''
<style id="home-api-models-css">
/* 首页 01：两行配置（API Key / 接入地址），2026-10-15 */
#home2 .sw-diff.sw-cfg{display:grid;grid-template-columns:auto minmax(0,1fr);gap:8px 14px;padding:10px 14px}
#home2 .sw-diff.sw-cfg b{justify-self:start;max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
/* 产品与服务页：产品之间细线分隔，子栏目用更浅的线（2026-10-15："正文几个部分粘连在一起了"） */
section[data-route="models"] .pe{padding-bottom:96px}
section[data-route="models"] .pe.sub{padding-bottom:80px}
section[data-route="models"] .pe+.pe{border-top:1px solid rgba(61,49,79,.13);padding-top:80px}
section[data-route="models"] .pe+.pe.sub{border-top-color:rgba(61,49,79,.07);padding-top:64px}
@media (max-width:760px){section[data-route="models"] .pe{padding-bottom:60px}section[data-route="models"] .pe.sub{padding-bottom:52px}
  section[data-route="models"] .pe+.pe{padding-top:52px}section[data-route="models"] .pe+.pe.sub{padding-top:44px}}
</style>
'''
k = s.rindex('</head>'); s = s[:k] + CSS + s[k:]
EN = {T1: 'Get an API key and start calling', P1: 'Create an API key in the console, set the endpoint, and call leading models including GLM, DeepSeek, Qwen and MiniMax; OpenAI and Gemini request formats both work.',
      '获取 API Key →': 'Get an API key →'}
rep('  syncAuthLocale(); applyLang();', '  (function(S){for(var k in S) if(!(k in I18N)) I18N[k]=S[k]})(' + json.dumps(EN, ensure_ascii=False) + ');  /* 首页 01 新口径 */\n  syncAuthLocale(); applyLang();')
open(OUT, 'w', encoding='utf8').write(s)
print('done:', OUT)
