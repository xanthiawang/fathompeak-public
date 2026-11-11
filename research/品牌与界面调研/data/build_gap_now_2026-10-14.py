# 功能差距清单 2026-10-14「现在就能做」五项：法律文件页、费用估算、控制台订单、文档补充、合规与安全页
# 用法：python3 build_gap_now_2026-10-14.py <site/index.html>
# 每处替换都要求锚点在文件里恰好出现一次，找不到或重复就停下，不写文件。
import json, re, sys, os

path = sys.argv[1]
s = open(path, encoding='utf-8').read()
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'legal_source_2026-10-14')

def rep(old, new):
    global s
    n = s.count(old)
    if n != 1:
        sys.exit(f'anchor count {n}: {old[:80]!r}')
    s = s.replace(old, new)

if 'data-route="compliance"' in s:
    sys.exit('already applied')

# ---------- 法律文件：平台公示原文（2026-09-03 版），去掉原样式，h2 保留 ----------
def legal(name):
    d = json.load(open(os.path.join(SRC, name + '.json'), encoding='utf-8'))['data']
    d = re.sub(r'<style>.*?</style>', '', d, flags=re.S).strip()
    d = d.replace('<div class="legal-doc">', '', 1)
    d = d[:d.rindex('</div>')].strip()
    d = d.replace('<div class="notice">', '<div class="box lg-note">')
    d = d.replace('<div class="meta">', '<div class="lg-meta">')
    return re.sub(r'\n\s*', '', d)

def legal_page(route, name, other_route, other_label):
    return (f'<section data-route="{route}"><div class="article legal">'
            f'<div class="lg-top"><span class="k">法律文件</span><a class="ul" href="#{other_route}">{other_label} →</a></div>'
            f'{legal(name)}'
            f'<p class="note">相关页面：<a class="ul" href="#compliance">合规与安全</a></p>'
            f'</div></section>\n')

PRIV = legal_page('privacy', 'privacy-policy', 'terms', '用户服务协议')
TERMS = legal_page('terms', 'user-agreement', 'privacy', '隐私政策')

# ---------- 合规与安全：只用站内已有表述与平台公示的隐私政策原句 ----------
COMP = '''<section data-route="compliance">
  <div class="wrap cp">
    <div class="page-head"><h1 class="display">合规与安全</h1><p>资质与备案、数据处理方式和法律文件。</p></div>
    <div class="cp-sec"><h2>资质与备案</h2>
      <dl class="cp-dl"><dt>ICP 备案</dt><dd><a class="ul" href="https://beian.miit.gov.cn/" target="_blank" rel="noopener">粤ICP备2026126659号</a><span>北京沐仞科技有限公司</span></dd>
      <dt>词元出海</dt><dd>有。出海运营主体在广东汕头，持中央网信办词元出海业务批复，合规文件可在签约前提供。</dd></dl></div>
    <div class="cp-sec"><h2>数据怎么处理</h2>
      <div class="cp-qa"><b>数据会不会出境？</b><p>来数加工在境内合规处理；签约前可做数据与安全评审。</p></div>
      <div class="cp-quote"><span class="k">摘自《隐私政策》</span>
        <dl class="cp-dl"><dt>存储地域</dt><dd>原则上，我们在中华人民共和国境内收集和产生的个人信息存储于境内。</dd>
        <dt>请求中转处理</dt><dd>为完成 API 中转，我们会接收并转发您提交的请求内容。除故障排查、安全审计、您开启的历史保存功能或法律法规要求外，我们不会将您的业务明文内容用于模型二次训练，也不会在服务目的达成后无必要长期留存。</dd>
        <dt>向模型服务商转发</dt><dd>为实现中转功能，您的请求内容可能被转发给您选择或系统调度的第三方模型服务商；其处理规则以其自身隐私政策为准。</dd>
        <dt>安全措施</dt><dd>采取传输加密、访问控制、权限最小化、审计与备份等合理措施。请您妥善保管账号与 API Key。</dd></dl>
        <a class="ul" href="#privacy">阅读完整隐私政策 →</a></div></div>
    <div class="cp-sec"><h2>API Key 安全</h2>
      <dl class="cp-dl"><dt>按项目拆分</dt><dd>建议按项目管理 API Key，用量与成本按项目归集。</dd><dt>泄露处理</dt><dd>发现密钥泄露时，立即撤销并更换，检查相关调用记录。</dd></dl></div>
    <div class="cp-sec"><h2>法律文件</h2>
      <div class="cp-docs"><a href="#privacy"><b>隐私政策</b><span>版本生效日期：2026年9月3日</span><i>阅读 →</i></a><a href="#terms"><b>用户服务协议</b><span>版本生效日期：2026年9月3日</span><i>阅读 →</i></a></div></div>
    <div class="cp-end"><p>签约前需要数据与安全评审？</p><button class="btn black" type="button" data-scrollto="enterprise-sales">联系销售</button></div>
  </div>
</section>
'''

rep('<!-- 更新日志 -->\n<section data-route="changelog">',
    '<!-- 合规与安全、法律文件（2026-10-14） -->\n' + COMP + PRIV + TERMS + '\n<!-- 更新日志 -->\n<section data-route="changelog">')

# 页脚与注册勾选：不再弹「请邮件索取」
rep('<a href="#enterprise">合规与安全</a>', '<a href="#compliance">合规与安全</a>')
rep('<button class="lnk" data-toast="用户协议请邮件 fathompeak@163.com 索取。">用户协议</button><button class="lnk" data-toast="隐私政策请邮件 fathompeak@163.com 索取。">隐私政策</button>',
    '<a href="#terms">用户协议</a><a href="#privacy">隐私政策</a>')
rep('<span>我已阅读并同意用户协议和隐私政策</span>',
    '<span>我已阅读并同意<a class="ul" href="#terms" target="_blank" rel="noopener">用户协议</a>和<a class="ul" href="#privacy" target="_blank" rel="noopener">隐私政策</a></span>')

# ---------- 定价：费用估算（输出单价取本页参考价；输入单价由用户按控制台填写，不预设） ----------
CALC = '''
    <div class="pr-sec" id="prCalc">
      <div class="pr-hd"><h2>估算费用</h2><p>选模型，填入输入和输出用量，按本页输出参考价估算。</p></div>
      <div class="pc">
        <div class="pc-in">
          <label class="ac-f pc-wide"><span>模型</span><select class="in" id="pcModel"></select></label>
          <label class="ac-f"><span>输出 Token（百万）</span><input class="in" type="number" min="0" step="any" inputmode="decimal" id="pcOut" value="1"></label>
          <label class="ac-f"><span>输入 Token（百万）</span><input class="in" type="number" min="0" step="any" inputmode="decimal" id="pcIn" value="1"></label>
          <label class="ac-f pc-wide"><span>输入单价（¥ / 百万词元）</span><input class="in" type="number" min="0" step="any" inputmode="decimal" id="pcInP" placeholder="见控制台模型列表"></label>
        </div>
        <div class="pc-out">
          <div class="pc-row"><span>输出部分</span><b class="mono" id="pcO"></b></div>
          <div class="pc-row"><span>输入部分</span><b class="mono" id="pcI"></b></div>
          <p class="pc-hint" id="pcHint">填写输入单价后计入输入部分。</p>
          <div class="pc-row pc-tot"><span id="pcTotA">合计</span><span id="pcTotB" hidden>合计（不含输入部分）</span><b class="mono" id="pcT"></b></div>
          <p class="pr-note">输出单价 <span class="mono" id="pcP"></span>，取自上方模型价格表。输入单价以控制台模型列表为准。估算不含教育价与合同价。</p>
        </div>
      </div>
    </div>
'''
rep('<p class="pr-ex"><span>例：GLM-5.3-Flash 生成 100 万个输出词元，输出部分约</span> <b class="mono" id="prEx"></b></p></div>\n    </div>\n',
    '<p class="pr-ex"><span>例：GLM-5.3-Flash 生成 100 万个输出词元，输出部分约</span> <b class="mono" id="prEx"></b></p></div>\n    </div>\n' + CALC)

# ---------- 文档：curl / Python / Node 示例 + 接入客户端 ----------
SP = '<span class="s">"请用一句话介绍算电协同。"</span>'
PY = ('<div class="code pre" data-lang="py" hidden><button class="cp" data-copy>复制</button><span class="g"># pip install openai</span><br>import os<br>from openai import OpenAI<br><br>'
      'client = OpenAI(<br>    base_url=<span class="s">"https://YOUR_API_HOST/v1"</span>,<br>    api_key=os.environ[<span class="s">"API_KEY"</span>],<br>)<br>'
      'resp = client.chat.completions.create(<br>    model=<span class="s">"GLM-5.3-Flash"</span>,<br>    messages=[{<span class="s">"role"</span>: <span class="s">"user"</span>, <span class="s">"content"</span>: ' + SP + '}],<br>)<br>'
      'print(resp.choices[0].message.content)</div>')
NODE = ('<div class="code pre" data-lang="node" hidden><button class="cp" data-copy>复制</button><span class="g">// npm install openai</span><br><span class="g">// 保存为 .mjs 文件后用 node 运行</span><br>import OpenAI from <span class="s">"openai"</span>;<br><br>'
        'const client = new OpenAI({<br>  baseURL: <span class="s">"https://YOUR_API_HOST/v1"</span>,<br>  apiKey: process.env.API_KEY,<br>});<br>'
        'const resp = await client.chat.completions.create({<br>  model: <span class="s">"GLM-5.3-Flash"</span>,<br>  messages: [{ role: <span class="s">"user"</span>, content: ' + SP + ' }],<br>});<br>'
        'console.log(resp.choices[0].message.content);</div>')
rep('<h3>3. 发第一条请求</h3><div class="code">',
    '<h3>3. 发第一条请求</h3><p>curl、Python 与 Node.js 任选其一，Python 与 Node.js 使用 OpenAI 官方 SDK。</p><div class="dtabs" role="tablist"><button class="chip on" type="button" data-lang="curl">curl</button><button class="chip" type="button" data-lang="py">Python</button><button class="chip" type="button" data-lang="node">Node.js</button></div><div class="code" data-lang="curl">')
rep('<p>调用成功后核对返回结果、用量与计费明细，以及订单的能源记录。</p></div>',
    PY + NODE + '\n        <p>调用成功后核对返回结果、用量与计费明细，以及订单的能源记录。</p></div>')
rep('<button data-doc="auth">鉴权与 Key</button>', '<button data-doc="clients">接入客户端</button><button data-doc="auth">鉴权与 Key</button>')
CLIENTS = '''      <div class="pane" data-doc="clients"><h1>接入客户端</h1><p>支持自定义 OpenAI 兼容服务商的桌面与网页客户端，填入接入地址、API Key 和模型名称就能使用。</p>
        <div class="code"><button class="cp" data-copy>复制</button><span class="g"># 服务商类型：OpenAI 兼容</span><br>API 地址 = <span class="s">"https://YOUR_API_HOST/v1"</span><br>API Key = <span class="s">"$API_KEY"</span><br>模型 = <span class="s">"GLM-5.3-Flash"</span></div>
        <h3>Cherry Studio</h3><p>设置 → 模型服务 → 添加，提供商类型选 OpenAI。API 地址填 <span class="mono">https://YOUR_API_HOST</span>，Cherry Studio 会自动补全 /v1 路径；填好后核对输入框下方显示的完整请求地址。再填 API 密钥，添加模型名称。</p>
        <h3>Lobe Chat</h3><p>设置 → AI 服务商 → OpenAI，填入 API Key，API 代理地址填 <span class="mono">https://YOUR_API_HOST/v1</span>，然后获取模型列表或手动添加模型名称。</p>
        <h3>CC Switch</h3><p>新增自定义供应商，按要切换的工具选择接口格式（沐仞兼容 OpenAI 与 Gemini 原生格式），填入请求地址和 API Key，保存后切换到这个供应商。</p>
        <h3>DeepChat</h3><p>设置 → 模型服务商 → 添加自定义服务商，类型选 OpenAI，API URL 填 <span class="mono">https://YOUR_API_HOST/v1</span>，填入 API Key 后拉取或添加模型。</p>
        <p class="note">各客户端的菜单名称会随版本变化，以客户端当前版本为准。接入地址见控制台。</p></div>
'''
rep('      <div class="pane" data-doc="auth">', CLIENTS + '      <div class="pane" data-doc="auth">')

# ---------- 控制台：订单（进行中 / 已完成），已完成页签用交易看板示例行生成产地卡 ----------
rep('<button type="button" data-p="usage">用量</button>', '<button type="button" data-p="usage">用量</button><button type="button" data-p="orders">订单</button>')
ORD = '''      <div class="cs-p" data-p="orders">
        <div class="cs-hd"><div><h2>订单</h2><p>每笔订单附一张产地卡：哪座电站、哪个时段、用了多少电、产出多少词元。做绿色采购、ESG 披露或跨境业务时，手里有一份可追溯的数据。</p></div></div>
        <div class="od-tabs" role="tablist"><button class="chip on" type="button" data-os="run">进行中</button><button class="chip" type="button" data-os="done">已完成</button></div>
        <div class="od-p" data-os="run"><div class="cs-empty"><b>没有进行中的订单</b><span>发出请求后，进行中的订单显示在这里。</span></div></div>
        <div class="od-p" data-os="done" hidden>
          <div class="od-hd"><span>你的账户还没有已完成的订单。下面是平台交易看板的订单，点开查看产地卡。</span><span class="k">示例数据</span></div>
          <div class="od-list" id="odList"></div>
          <p class="cs-fine">示例数据取自平台交易看板。发电时段、用电量与产出词元在平台接口接入后按订单显示。</p>
        </div>
      </div>
'''
rep('      <div class="cs-p" data-p="bill">', ORD + '      <div class="cs-p" data-p="bill">')

# ---------- CSS ----------
CSS = '''
/* 2026-10-14 费用估算、控制台订单与产地卡、文档代码页签、合规与安全、法律文件 */
.pc{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);gap:16px}
.pc-in{display:grid;grid-template-columns:1fr 1fr;gap:14px;background:var(--card);border:1px solid var(--line);border-radius:var(--r20);padding:22px 24px;align-content:start}
.pc-in .pc-wide{grid-column:1/-1} .pc-in select.in{appearance:none;background:var(--card) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath d='M3 4.5 6 7.5 9 4.5' fill='none' stroke='%23707070' stroke-width='1.4'/%3E%3C/svg%3E") no-repeat right 14px center;padding-right:36px}
.pc-out{background:var(--accent-tint);border-radius:var(--r20);padding:22px 26px;display:grid;align-content:start;gap:4px}
.pc-row{display:flex;justify-content:space-between;align-items:baseline;gap:16px;padding:10px 0;border-bottom:1px solid var(--line);font-size:15px;color:var(--ink-70)} .pc-row b{font-size:17px;color:var(--ink);font-weight:500}
.pc-tot{border-bottom:0;color:var(--ink)} .pc-tot b{font-size:28px} .pc-hint{margin:6px 0 0;font-size:13px;color:var(--ink-50)} .pc-hint[hidden],.pc-tot [hidden]{display:none}
.pc-out .pr-note{margin-top:10px}
.dtabs,.od-tabs{display:flex;gap:8px;flex-wrap:wrap;margin:10px 0 0}
.code.pre{white-space:pre} .code[hidden]{display:none}
.od-tabs{margin:0 0 16px}
.od-hd{display:flex;justify-content:space-between;align-items:baseline;gap:12px;flex-wrap:wrap;font-size:14px;color:var(--ink-70);margin-bottom:10px}
.od-list{border-top:1px solid var(--line)}
.od{border-bottom:1px solid var(--line)}
.od-h{appearance:none;border:0;background:transparent;width:100%;display:grid;grid-template-columns:minmax(0,1fr) auto auto;gap:16px;align-items:center;padding:14px 4px;font:400 14px var(--sans);color:var(--ink);text-align:left;cursor:pointer}
.od-h .od-p2{font:400 13px var(--mono);color:var(--ink-70)} .od-h .od-go{font-size:13px;color:var(--ink-50);white-space:nowrap} .od-h[aria-expanded="true"] .od-go{color:var(--ink)}
.od-card{margin:0 0 16px;background:var(--card);border:1px solid var(--line);border-radius:var(--r16);padding:6px 18px 4px} .od-card[hidden]{display:none}
.od-card .cs-dl{border-top:0} .od-card .cs-dl dt:last-of-type,.od-card .cs-dl dd:last-of-type{border-bottom:0}
.cp{max-width:880px;padding-bottom:40px}
.cp-sec{margin-top:64px} .cp-sec h2{font:400 30px/1.15 var(--serif);letter-spacing:-.02em;margin-bottom:16px}
.cp-dl{display:grid;grid-template-columns:150px minmax(0,1fr);margin:0;border-top:1px solid var(--line)}
.cp-dl dt,.cp-dl dd{margin:0;padding:14px 0;border-bottom:1px solid var(--line);font-size:15px;line-height:1.6} .cp-dl dt{color:var(--ink-50);padding-right:16px} .cp-dl dd{color:var(--ink-85)} .cp-dl dd span{display:block;font-size:13px;color:var(--ink-50);margin-top:2px}
.cp-qa{margin-bottom:22px} .cp-qa b{display:block;font:500 16px var(--sans);color:var(--ink)} .cp-qa p{margin:6px 0 0;font-size:15px;color:var(--ink-70)}
.cp-quote{background:var(--paper-2);border-radius:var(--r16);padding:18px 20px} .cp-quote .k{display:block;margin-bottom:10px} .cp-quote>.ul{display:inline-block;margin-top:14px;font-size:14px}
.cp-docs{display:grid;grid-template-columns:1fr 1fr;gap:12px} .cp-docs a{display:grid;gap:4px;background:var(--card);border:1px solid var(--line);border-radius:var(--r16);padding:18px 20px;transition:border-color .2s var(--ease)} .cp-docs a:hover{border-color:var(--ink-30)}
.cp-docs b{font:400 22px/1.2 var(--serif);color:var(--ink)} .cp-docs span{font-size:13px;color:var(--ink-50)} .cp-docs i{font-style:normal;font-size:14px;color:var(--ink-70);margin-top:8px}
.cp-end{margin-top:64px;display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap;border-top:1px solid var(--line);padding-top:24px} .cp-end p{margin:0;font-size:17px;color:var(--ink)}
.legal .lg-top{display:flex;justify-content:space-between;align-items:baseline;gap:12px;flex-wrap:wrap;margin-bottom:6px} .legal .lg-top .k{margin:0} .legal .lg-top .ul{font-size:14px}
.legal .lg-meta p{font-size:14px;color:var(--ink-50);margin:0 0 18px} .legal .lg-meta strong{font-weight:500}
.legal .lg-note p{font-size:15px;margin:0 0 8px} .legal .lg-note p:last-child{margin:0}
.legal h2{font:400 24px/1.25 var(--serif);letter-spacing:-.01em;margin:34px 0 10px}
.legal ol,.legal ul{padding-left:22px;color:var(--ink-85);margin:0 0 14px} .legal li{font-size:15px;line-height:1.7;margin-bottom:8px} .legal li strong{font-weight:600;color:var(--ink)}
html[lang="en"] .article.legal:before{content:"English translation of the Chinese original."}
@media (max-width:800px){
  .pc{grid-template-columns:1fr} .pc-in{grid-template-columns:1fr;padding:18px} .pc-out{padding:18px 20px}
  .od-h{grid-template-columns:minmax(0,1fr) auto;gap:4px 12px} .od-h .od-go{grid-column:2;grid-row:1} .od-h .od-p2{grid-column:1}
  .cp-dl{grid-template-columns:1fr} .cp-dl dt{padding:14px 0 0;border-bottom:0} .cp-dl dd{padding-top:4px}
  .cp-docs{grid-template-columns:1fr} .cp-sec{margin-top:48px} .legal h2{font-size:21px}
}
'''
rep('\n}\n</style>\n\n<div hidden aria-hidden="true">', '\n}\n' + CSS + '</style>\n\n<div hidden aria-hidden="true">')

# ---------- JS ----------
JS = r'''
  /* 定价：费用估算。输出按本页输出参考价；输入单价由用户按控制台填写，空着就不计入 */
  (function(){var sel=$('#pcModel'); if(!sel) return;
    sel.innerHTML=M.map(function(m){return '<option value="'+m.id+'"'+(m.id==='glm-5-3-flash'?' selected':'')+'>'+m.name+' · ¥'+m.mkt.toFixed(2)+'</option>'}).join('');
    function num(id){var v=parseFloat($(id).value);return isFinite(v)&&v>0?v:0}
    function money(n){return '¥'+n.toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2})}
    function calc(){var m=byId[sel.value]||M[0], o=num('#pcOut')*m.mkt, hasP=$('#pcInP').value.trim()!=='', i=hasP?num('#pcIn')*num('#pcInP'):0;
      $('#pcO').textContent=money(o); $('#pcI').textContent=hasP?money(i):'—'; $('#pcT').textContent=money(o+i);
      $('#pcHint').hidden=hasP; $('#pcTotA').hidden=!hasP; $('#pcTotB').hidden=hasP; $('#pcP').textContent='¥'+m.mkt.toFixed(2)+' / 百万词元'}
    ['#pcModel','#pcOut','#pcIn','#pcInP'].forEach(function(id){$(id).addEventListener('input',calc);$(id).addEventListener('change',calc)}); calc()})();

  /* 文档：快速开始的 curl / Python / Node 页签 */
  $$('.dtabs [data-lang]').forEach(function(b){b.addEventListener('click',function(){var k=b.getAttribute('data-lang');
    $$('.dtabs [data-lang]').forEach(function(x){x.classList.toggle('on',x===b)}); $$('.docs .code[data-lang]').forEach(function(c){c.hidden=c.getAttribute('data-lang')!==k})})});

  /* 控制台：订单页签；已完成页签列交易看板示例行，点开是产地卡（时段、用电量、产出词元待平台接口） */
  $$('.od-tabs [data-os]').forEach(function(b){b.addEventListener('click',function(){var k=b.getAttribute('data-os');
    $$('.od-tabs [data-os]').forEach(function(x){x.classList.toggle('on',x===b)}); $$('.od-p').forEach(function(p){p.hidden=p.getAttribute('data-os')!==k})})});
  (function(){var el=$('#odList'); if(!el) return; var typ={}; N.forEach(function(x){typ[x.n]=x.t});
    el.innerHTML=T.slice(0,6).map(function(r,i){return '<div class="od"><button class="od-h" type="button" aria-expanded="false" aria-controls="odC'+i+'"><span><span>'+r[0]+'</span> → <span>'+r[1]+'</span></span><span class="od-p2">'+fmt(r[2])+' / M</span><span class="od-go">产地卡</span></button>'+
      '<div class="od-card" id="odC'+i+'" hidden><dl class="cs-dl"><dt>电站</dt><dd>'+r[0]+'</dd><dt>电站类型</dt><dd>'+(typ[r[0]]||'—')+'</dd><dt>模型</dt><dd>'+r[1]+'</dd><dt>成交价</dt><dd class="mono">'+fmt(r[2])+' / 百万词元</dd><dt>减排</dt><dd class="mono">−'+r[3].toFixed(2)+' kg</dd><dt>发电时段</dt><dd>—</dd><dt>用电量</dt><dd>—</dd><dt>产出词元</dt><dd>—</dd></dl></div></div>'}).join('');
    $$('.od-h',el).forEach(function(b){b.addEventListener('click',function(){var c=$('#'+b.getAttribute('aria-controls')),o=c.hidden;c.hidden=!o;b.setAttribute('aria-expanded',String(o))})})})();
'''
rep('\n  /* ---------- 复制与提示 ---------- */', JS + '\n  /* ---------- 复制与提示 ---------- */')

# 路由标题
rep("about:'关于沐仞 · 沐仞'})[name]", "about:'关于沐仞 · 沐仞',compliance:'合规与安全 · 沐仞',privacy:'隐私政策 · 沐仞',terms:'用户服务协议 · 沐仞'})[name]")

# ---------- 英文 ----------
zh = json.load(open(os.path.join(SRC, 'legal_zh_keys.json'), encoding='utf-8'))
en = json.load(open(os.path.join(SRC, 'legal_en.json'), encoding='utf-8'))
assert len(zh) == len(en), (len(zh), len(en))
E = dict(zip(zh, en))
E.update({
  # 页脚与注册
  "用户协议": "Terms of Service", "隐私政策": "Privacy Policy", "我已阅读并同意": "I have read and agree to the ", "和": " and ",
  # 法律文件页
  "法律文件": "Legal", "用户服务协议 →": "Terms of Service →", "隐私政策 →": "Privacy Policy →", "相关页面：": "Related: ",
  # 合规与安全
  "资质与备案、数据处理方式和法律文件。": "Licences and filings, how data is handled, and legal documents.",
  "资质与备案": "Licences & filings", "ICP 备案": "ICP filing", "粤ICP备2026126659号": "Guangdong ICP No. 2026126659",
  "词元出海": "Token export", "数据怎么处理": "How data is handled", "摘自《隐私政策》": "From the Privacy Policy",
  "存储地域": "Storage location", "请求中转处理": "Request relay", "向模型服务商转发": "Forwarding to model providers", "安全措施": "Security measures",
  "阅读完整隐私政策 →": "Read the full Privacy Policy →", "API Key 安全": "API key security", "版本生效日期：2026年9月3日": "Effective 3 September 2026",
  "阅读 →": "Read →", "签约前需要数据与安全评审？": "Need a data and security review before signing?",
  "合规与安全 · 沐仞": "Compliance & security · FathomPeak", "隐私政策 · 沐仞": "Privacy Policy · FathomPeak", "用户服务协议 · 沐仞": "Terms of Service · FathomPeak",
  # 费用估算
  "估算费用": "Estimate your cost", "选模型，填入输入和输出用量，按本页输出参考价估算。": "Pick a model and enter input and output volumes; the estimate uses the reference output prices on this page.",
  "输出 Token（百万）": "Output tokens (millions)", "输入 Token（百万）": "Input tokens (millions)", "输入单价（¥ / 百万词元）": "Input price (¥ / M tokens)",
  "见控制台模型列表": "See the console model list", "输出部分": "Output", "输入部分": "Input", "填写输入单价后计入输入部分。": "Enter an input price to include the input cost.",
  "合计": "Total", "合计（不含输入部分）": "Total (excluding input)", "输出单价": "Output price",
  "，取自上方模型价格表。输入单价以控制台模型列表为准。估算不含教育价与合同价。": ", from the model price table above. Input prices follow the console model list. Education and contract prices are not included.",
  # 文档
  "curl、Python 与 Node.js 任选其一，Python 与 Node.js 使用 OpenAI 官方 SDK。": "Use curl, Python or Node.js. The Python and Node.js examples use the official OpenAI SDK.",
  "// 保存为 .mjs 文件后用 node 运行": "// Save as a .mjs file and run it with node",
  "接入客户端": "Connect a client",
  "支持自定义 OpenAI 兼容服务商的桌面与网页客户端，填入接入地址、API Key 和模型名称就能使用。": "Desktop and web clients that accept a custom OpenAI-compatible provider work once you enter the endpoint, API key and model name.",
  "# 服务商类型：OpenAI 兼容": "# Provider type: OpenAI-compatible", "API 地址 =": "API address =", "模型 =": "Model =",
  "设置 → 模型服务 → 添加，提供商类型选 OpenAI。API 地址填": "Settings → Model Provider → Add, and choose OpenAI as the provider type. Set the API address to",
  "，Cherry Studio 会自动补全 /v1 路径；填好后核对输入框下方显示的完整请求地址。再填 API 密钥，添加模型名称。": "; Cherry Studio appends the /v1 path itself, so check the full request URL shown under the field. Then enter the API key and add the model name.",
  "设置 → AI 服务商 → OpenAI，填入 API Key，API 代理地址填": "Settings → AI Provider → OpenAI. Enter the API key and set the API proxy address to",
  "，然后获取模型列表或手动添加模型名称。": ", then fetch the model list or add the model name by hand.",
  "新增自定义供应商，按要切换的工具选择接口格式（沐仞兼容 OpenAI 与 Gemini 原生格式），填入请求地址和 API Key，保存后切换到这个供应商。": "Add a custom provider and pick the API format for the tool you are switching (FathomPeak supports OpenAI and Gemini native formats). Enter the endpoint and API key, save, then switch to this provider.",
  "设置 → 模型服务商 → 添加自定义服务商，类型选 OpenAI，API URL 填": "Settings → Model Providers → Add custom provider, type OpenAI, and set the API URL to",
  "，填入 API Key 后拉取或添加模型。": ". Enter the API key, then fetch or add models.",
  "各客户端的菜单名称会随版本变化，以客户端当前版本为准。接入地址见控制台。": "Menu names change between client versions; follow the version you have installed. Find the endpoint in the console.",
  # 控制台订单
  "订单": "Orders", "进行中": "Running", "已完成": "Completed", "没有进行中的订单": "No running orders",
  "发出请求后，进行中的订单显示在这里。": "Orders in progress appear here after you send requests.",
  "你的账户还没有已完成的订单。下面是平台交易看板的订单，点开查看产地卡。": "Your account has no completed orders yet. Below are orders from the platform trading board; open one to see its origin card.",
  "示例数据取自平台交易看板。发电时段、用电量与产出词元在平台接口接入后按订单显示。": "Sample data from the platform trading board. Generation window, energy used and tokens produced appear per order once the platform API is connected.",
  "显示密码": "Show password", "充值金额": "Top-up amount",
  "电站类型": "Plant type", "成交价": "Price", "减排": "CO2 avoided", "发电时段": "Generation window", "用电量": "Energy used", "产出词元": "Tokens produced",
})
blob = json.dumps(E, ensure_ascii=False)
rep("  var lang='zh'; try{lang=localStorage.getItem('fp-lang')||'zh'}catch(e){}",
    "  /* 2026-10-14 合规与安全、法律文件、费用估算、文档示例与客户端、控制台订单 */\n  Object.assign(I18N," + blob + ");\n  var lang='zh'; try{lang=localStorage.getItem('fp-lang')||'zh'}catch(e){}")

open(path, 'w', encoding='utf-8').write(s)
print('ok', len(s))
