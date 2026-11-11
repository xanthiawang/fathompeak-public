"""体验中心（Zixin 2026-10-14）。第二版："体验中心的 UI 还是不好看。为什么缩到那么小一个角落？直接铺满全屏。参考硅基流动，还有 Runway，
它可以直接选要用的模型和 prompt。" 配色、字体、风格保持我们的（晨蓝树影光、Fraunces / 思源宋标题、白玻璃、黑胶囊按钮、排线插画）。
第一版（圆角卡片里的小首屏）备份在会话草稿目录 build_console_playground_v1_backup.py。
布局（铺满控制台工作区，去掉页面内边距）：
 - 首屏：整片晨蓝树影光，白色衬线大标题「今天想试哪个模型？」，上方一条「模型目录收录 7 个模型」动态胶囊（更新日志里的真实记录）。
 - 宽输入框（Runway 式）：底栏左边是模型按钮（厂商图标 + 名称 ▾，点开是模型列表：类型、上下文、输出价，可搜索）和「+ 对比」（最多 3 个），
   右边是「参数」（弹出面板：温度、Top-P、最大输出、思考预算、系统提示词、算力节点、查看代码）和黑色圆形发送键。
 - 输入框下：7 个模型的快捷胶囊；再下面是按场景分类的 prompt 模板卡（写作 / 编程 / 翻译 / 分析 / 客服），点卡片同时填好 prompt 和模型。
 - 发出后：对比视图铺满全宽，每个模型一列（白玻璃卡，卡底首字时延 / 速度 / 词元 / 费用 / 产地），输入框停在底部。
 - 不发起真实调用：回答区写「体验中心尚未开通」，指标为 --。
名字：在线试用 → 体验中心（只出现在本预览新增内容里）。
叠加顺序：线上 → supplement → console_backend → superadmin → login → 本脚本 → role_versions。
用法：python3 -I build_console_playground_2026-10-14.py <输入 html> <输出 html>
"""
import json, sys

LIVE = '--live' in sys.argv  # 上线版：不写闲时 / 忙时钟点（出自报价单）
args = [x for x in sys.argv[1:] if not x.startswith('--')]
SRC, OUT = args[0], args[1]
s = open(SRC, encoding='utf8').read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: sys.exit(f'[停止] 匹配 {c} 次（应为 {n}）：{old[:80]}')
    s = s.replace(old, new)


def tbc(t='待公司确认'):
    return f'<span class="tbc">{t}</span>'


# prompt 模板：只是示例问题，卡片预选一个模型，用户可以改
TPL = [
    ('写作', '写一篇产品发布稿', '为一款面向开发者的大模型 API 平台写一篇 300 字的产品发布稿，语气专业、简洁。', 'glm-5-3', 'sign'),
    ('写作', '把文案改得更口语', '把下面这段话改得更口语、更短，保留原意：\n', 'glm-5-3-flash', 'tag'),
    ('编程', '解释一段代码', '逐行解释下面这段代码在做什么，并指出可能的 bug：\n', 'deepseek-v4-pro', 'boxes'),
    ('编程', '写单元测试', '为下面这个函数写 pytest 单元测试，覆盖边界情况：\n', 'deepseek-v4-flash', 'key'),
    ('翻译', '中英互译，保留术语', '把下面的中文翻译成英文，专业术语前后一致，最后列出术语表：\n', 'qwen3-8-flash', 'book'),
    ('分析', '总结长文要点', '用 5 条要点总结下面这篇文章，每条不超过 30 字：\n', 'minimax-m3', 'book'),
    ('分析', '从数据里找规律', '下面是一组表格数据，找出 3 个最值得注意的变化，并解释可能的原因：\n', 'glm-5-3', 'solar'),
    ('客服', '写一段客服回复', '客户说充值后余额没到账。写一段礼貌、清楚的回复，说明怎么查和下一步：\n', 'minimax-m2-7', 'tag'),
]
CATS = ['全部', '写作', '编程', '翻译', '分析', '客服']

a = s.index('      <div class="cs-p" data-p="play">'); b = s.index('      <div class="cs-p" data-p="explore">', a)
SEND = '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M10 15.5v-11M5.5 9 10 4.5 14.5 9" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
PANE = '''      <div class="cs-p" data-p="play">
        <div class="xp" id="xp" data-mode="empty">
          <div class="xp-bg" aria-hidden="true"><div class="bt-key-light"></div></div>
          <div class="xp-stage">
            <div class="xp-intro">
              <a class="xp-news" href="#changelog"><span class="xp-newk">新</span><span>模型目录收录 7 个模型</span><span aria-hidden="true">→</span></a>
              <h1 class="xp-h">今天想试哪个模型？</h1>
            </div>
            <div class="xp-top"><h1 class="xp-h2">体验中心</h1><button class="bt-btn" type="button" id="xpNew">新对话</button></div>
            <div class="xp-cols" id="xpCols"></div>
            <form class="xp-box" id="xpBox" novalidate>
              <textarea id="xpQ" rows="3" placeholder="输入问题，或从下面选一个模板" aria-label="输入问题"></textarea>
              <div class="xp-bar">
                <div class="xp-left"><div class="xp-pills" id="xpPills"></div><button class="xp-add" type="button" id="xpAdd">+ 对比</button></div>
                <div class="xp-right"><button class="xp-opt" type="button" id="xpParB" aria-expanded="false" aria-controls="xpPar"><span>参数</span><svg viewBox="0 0 12 12" aria-hidden="true"><path d="M3 4.5 6 7.5 9 4.5" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
                  <button class="xp-send" type="submit" aria-label="发送">''' + SEND + '''</button></div>
              </div>
              <div class="xp-pop xp-mpop" id="xpMPop" hidden>
                <label class="bt-q"><svg viewBox="0 0 16 16" aria-hidden="true"><circle cx="7" cy="7" r="5" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M11 11l3.5 3.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg><input type="search" id="xpMQ" placeholder="查找模型" aria-label="查找模型" autocomplete="off" spellcheck="false"></label>
                <div class="xp-mlist" id="xpML" role="listbox" aria-label="选择模型"></div>
              </div>
              <div class="xp-pop xp-ppop" id="xpPar" hidden>
                <b class="xp-ph">参数</b>
                <label><span>温度 <b class="mono" id="xpTv">0.7</b></span><input type="range" min="0" max="2" step="0.1" value="0.7" id="xpT"></label>
                <label><span>Top-P <b class="mono" id="xpPv">1</b></span><input type="range" min="0" max="1" step="0.05" value="1" id="xpP"></label>
                <div class="xp-p2"><label><span>最大输出词元</span><input class="in mono" id="xpN" value="1024" inputmode="numeric" autocomplete="off"></label>
                  <label id="xpBudW"><span>思考预算</span><input class="in mono" id="xpB" value="4096" inputmode="numeric" autocomplete="off"></label></div>
                <label><span>系统提示词</span><textarea class="in" id="xpS" rows="2" placeholder="可选，例如：用中文简洁回答"></textarea></label>
                <label><span>算力节点</span><select class="in" disabled><option>自动调度（按时段与节点余量）</option></select></label>
                <div class="xp-pf"><button class="bt-a" type="button" id="xpReset">恢复默认</button><button class="bt-btn" type="button" id="xpCodeB" aria-expanded="false" aria-controls="xpCode">查看代码</button></div>
              </div>
            </form>
            <div class="code pre xp-code" id="xpCode" hidden><button class="cp" data-copy>复制</button><span id="xpCodeT"></span></div>
            <div class="xp-chips" id="xpChips" role="group" aria-label="快速选择模型"></div>
            <div class="xp-tpl">
              <div class="xp-tabs" id="xpTabs" role="group" aria-label="模板分类">''' + ''.join(f'<button class="bt-chip{" on" if i == 0 else ""}" type="button" data-c="{c}" aria-pressed="{"true" if i == 0 else "false"}">{c}</button>' for i, c in enumerate(CATS)) + '''</div>
              <div class="xp-cards" id="xpCards"></div>
            </div>
            <p class="xp-note">体验中心按实际用量从余额扣费，价格见<a class="bt-a" href="#pricing">定价</a>。''' + tbc() + '''　内容由人工智能生成，仅供参考，请遵守<a class="bt-a" href="#terms">用户服务协议</a>。生成式人工智能服务备案号：--''' + tbc('待公司提供') + '''</p>
          </div>
        </div>
      </div>
'''
s = s[:a] + PANE + s[b:]

# 模型详情「去体验中心」把模型带过来
if "var s2=$('#supPgM');" in s: rep("var s2=$('#supPgM'); if(s2&&id){s2.value=id; s2.dispatchEvent(new Event('change'))}", "if(window.supPlaySet&&id) window.supPlaySet(id)")  # 只推控制台时没有模型详情入口
n_ren = s.count('在线试用')
s = s.replace('在线试用', '体验中心')

CSS = '''
<style id="sup-xp-css">
/* 体验中心（2026-10-14 第二版）：铺满工作区；晨蓝树影光 + 白玻璃输入框 + 模型快捷胶囊 + 模板卡；配色、字体沿用控制台 */
.cs-p[data-p="play"]{padding:0!important}
.xp{position:relative;isolation:isolate;min-height:100vh}
.xp-bg{position:absolute;left:0;right:0;top:0;height:600px;z-index:-1;overflow:hidden;isolation:isolate;background:#2F63B8;transition:height .35s var(--out,ease)}
.xp-bg::after{content:"";position:absolute;inset:0;pointer-events:none;background:linear-gradient(180deg,rgba(33,32,33,.14) 0%,transparent 28%,rgba(248,248,248,.2) 58%,rgba(248,248,248,.88) 86%,#F8F8F8 100%)}
.xp-stage{max-width:1180px;margin:0 auto;padding:96px 48px 56px;display:grid;gap:22px;min-width:0}
.xp-intro{display:grid;justify-items:center;gap:20px;text-align:center}
.xp-news{display:inline-flex;align-items:center;gap:10px;height:36px;padding:0 14px 0 6px;border-radius:999px;background:rgba(255,255,255,.88);border:1px solid rgba(255,255,255,.7);
  box-shadow:0 2px 8px rgba(0,0,0,.08);font:500 13px var(--sans);color:var(--ink);text-decoration:none}
.xp-newk{display:inline-grid;place-items:center;height:24px;padding:0 9px;border-radius:999px;background:#000;color:#fff;font-size:12px}
.xp-h{margin:0;font:400 60px/1.08 var(--serif);letter-spacing:-.025em;color:#fff;text-shadow:0 1px 18px rgba(33,32,33,.18);font-variation-settings:"opsz" 144}
.xp-top{display:none;justify-content:flex-start;align-items:center;gap:16px}
.xp-h2{margin:0;font:400 32px/1.15 var(--serif);letter-spacing:-.02em;color:#fff;text-shadow:0 1px 14px rgba(33,32,33,.16);font-variation-settings:"opsz" 144}
.xp-box{position:relative;width:min(940px,100%);justify-self:center;display:grid;gap:10px;padding:16px 16px 14px 20px;border-radius:26px;background:rgba(255,255,255,.96);border:1px solid rgba(255,255,255,.75);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.9),0 24px 56px -28px rgba(33,32,33,.5),0 2px 10px rgba(0,0,0,.06)}
.xp-box textarea{border:0;outline:0;resize:none;background:transparent;font:400 17px/1.6 var(--sans);color:var(--ink);min-height:78px}
.xp-bar{display:grid;grid-template-columns:minmax(0,1fr) auto;align-items:end;gap:10px}
.xp-left{display:flex;flex-wrap:wrap;gap:6px;align-items:center;min-width:0}
.xp-right{display:flex;gap:8px;align-items:center}
.xp-pills{display:flex;flex-wrap:wrap;gap:6px}
.xp-pill{display:inline-flex;align-items:center;gap:7px;height:36px;padding:0 6px 0 11px;border-radius:999px;background:var(--gray-btn);font:500 14px var(--sans);color:var(--ink)}
.xp-pill>button:first-child{appearance:none;border:0;background:transparent;display:inline-flex;align-items:center;gap:6px;font:inherit;color:inherit;cursor:pointer;padding:0}
.xp-pill svg.ch{width:10px;height:10px;color:var(--ink-50)}
.xp-x{appearance:none;border:0;background:transparent;width:22px;height:22px;border-radius:50%;color:var(--ink-50);cursor:pointer;font-size:15px;line-height:1}
.xp-x:hover{background:rgba(0,0,0,.07);color:var(--ink)}
.xp-add,.xp-opt{appearance:none;height:36px;padding:0 13px;border-radius:999px;border:1px solid var(--line);background:transparent;font:500 13.5px var(--sans);color:var(--ink-70);cursor:pointer;display:inline-flex;align-items:center;gap:6px}
.xp-opt svg{width:10px;height:10px}
.xp-add:hover,.xp-opt:hover,.xp-opt[aria-expanded="true"]{color:var(--ink);border-color:rgba(0,0,0,.2)}
.xp-send{appearance:none;width:40px;height:40px;border-radius:50%;border:0;background:#000;color:#fff;display:inline-grid;place-items:center;cursor:pointer}
.xp-send svg{width:18px;height:18px}
.xp-pop{position:absolute;top:calc(100% + 10px);z-index:20;background:#fff;border:1px solid var(--line);border-radius:20px;
  box-shadow:0 24px 60px -24px rgba(33,32,33,.45),0 2px 8px rgba(0,0,0,.06);padding:14px}
.xp-mpop{left:12px;width:min(420px,calc(100% - 24px));display:grid;gap:10px}
.xp-mpop .bt-q{height:40px}
.xp-mlist{display:grid;gap:2px;max-height:340px;overflow:auto}
.xp-mi{appearance:none;border:0;background:transparent;display:grid;grid-template-columns:22px minmax(0,1fr) auto;gap:4px 10px;align-items:center;padding:10px;border-radius:12px;text-align:left;cursor:pointer;font:inherit;color:var(--ink)}
.xp-mi:hover,.xp-mi[aria-selected="true"]{background:var(--gray-btn)}
.xp-mi b{font:500 14.5px var(--sans)}
.xp-mi .m2{grid-column:2/4;font-size:12.5px;color:var(--ink-50)}
.xp-mi .bt-tag{justify-self:end}
.xp-ppop{right:12px;width:min(360px,calc(100% - 24px));display:grid;gap:12px;max-height:min(560px,calc(100vh - 150px));overflow:auto;overscroll-behavior:contain}
.xp-ph{font:400 20px/1.2 var(--serif);font-variation-settings:"opsz" 144}
.xp-ppop label{display:grid;gap:6px;font-size:13px;color:var(--ink-70)}
.xp-ppop label>span{display:flex;justify-content:space-between}
/* 输入框、下拉框：去掉上下内边距按行高居中，否则 38px 高里装不下文字（2026-10-14 修：算力节点文字被截断） */
.xp-ppop input.in,.xp-ppop select.in{height:40px;padding-top:0;padding-bottom:0;line-height:38px}
.xp-ppop textarea.in{height:auto;padding:10px 14px;line-height:1.5;resize:vertical}
.xp-ppop input[type=range]{width:100%;accent-color:#000}
.xp-p2{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.xp-pf{display:flex;justify-content:space-between;align-items:center;padding-top:10px;border-top:1px solid var(--line)}
.xp-chips{display:flex;flex-wrap:wrap;justify-content:center;gap:8px;max-width:940px;justify-self:center}
.xp-chip{appearance:none;display:inline-flex;align-items:center;gap:8px;height:40px;padding:0 15px 0 12px;border-radius:999px;border:1px solid var(--glass-line,rgba(255,255,255,.6));
  background:rgba(255,255,255,.82);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);box-shadow:0 1px 2px rgba(0,0,0,.04);font:500 14px var(--sans);color:var(--ink);cursor:pointer}
.xp-chip[aria-pressed="true"]{background:#000;color:#fff;border-color:#000}
.xp-tpl{display:grid;gap:18px;margin-top:30px}
.xp-tabs{display:flex;flex-wrap:wrap;justify-content:center;gap:6px}
.xp-cards{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}
.xp-card{appearance:none;text-align:left;display:grid;grid-template-rows:164px auto;padding:0;border:1px solid rgba(0,0,0,.06);border-radius:22px;overflow:hidden;cursor:pointer;font:inherit;color:var(--ink);
  background:linear-gradient(155deg,rgba(47,99,184,.13),rgba(61,49,79,.10) 62%,rgba(33,32,33,.05));box-shadow:0 1px 2px rgba(0,0,0,.03),0 14px 30px -22px rgba(33,32,33,.3);transition:transform .3s var(--out,ease),box-shadow .3s}
.xp-card:hover{transform:translateY(-2px);box-shadow:0 2px 8px rgba(0,0,0,.06),0 22px 40px -24px rgba(33,32,33,.38)}
.xp-card:focus-visible{outline:2px solid var(--ink);outline-offset:3px}
.xp-art{display:grid;place-items:center}
.xp-art .bt-collage{display:block;width:136px;height:136px}
.xp-ct{display:grid;gap:7px;align-content:start;padding:16px 18px 18px;background:rgba(255,255,255,.78)}
.xp-ct .k{font:400 11px var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--ink-50)}
.xp-ct b{font:400 19px/1.25 var(--serif);letter-spacing:-.01em;font-variation-settings:"opsz" 144}
.xp-ct p{margin:0;font-size:13px;line-height:1.55;color:var(--ink-70);display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.xp-ct .xp-mc{display:inline-flex;align-items:center;gap:6px;font-size:12.5px;color:var(--ink-70);margin-top:2px}
.xp-note{margin:10px 0 0;font-size:12.5px;color:var(--ink-50);text-align:center}
.xp-code{margin:0;width:min(940px,100%);justify-self:center;white-space:pre-wrap;overflow-wrap:anywhere}
/* 对话：铺满全宽的对比列 */
.xp[data-mode="chat"] .xp-bg{height:240px}
.xp[data-mode="chat"] .xp-intro,.xp[data-mode="chat"] .xp-chips,.xp[data-mode="chat"] .xp-tpl{display:none}
.xp[data-mode="chat"] .xp-top{display:flex}
.xp[data-mode="chat"] .xp-stage{max-width:none;padding:34px 40px 28px;gap:16px}
.xp[data-mode="chat"] .xp-pop{top:auto;bottom:calc(100% + 10px)}
.xp-cols{display:none;gap:14px}
.xp[data-mode="chat"] .xp-cols{display:grid}
.xp-cols.n1{grid-template-columns:minmax(0,1fr)}
.xp-cols.n2{grid-template-columns:repeat(2,minmax(0,1fr))}
.xp-cols.n3{grid-template-columns:repeat(3,minmax(0,1fr))}
.xp-col{display:grid;grid-template-rows:auto 1fr auto;height:calc(100vh - 330px);min-height:360px;background:rgba(255,255,255,.72);border:1px solid rgba(0,0,0,.06);border-radius:22px;
  box-shadow:0 1px 2px rgba(0,0,0,.025),0 14px 32px -20px rgba(0,0,0,.18);overflow:hidden;backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px)}
.xp-col header{display:flex;flex-wrap:wrap;align-items:center;gap:6px 9px;padding:15px 18px;border-bottom:1px solid var(--line)}
.xp-col header b{flex:0 1 auto;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font:400 19px/1.2 var(--serif);letter-spacing:-.01em;font-variation-settings:"opsz" 144}
.xp-col header .bt-tag,.xp-col header svg,.xp-col header img{flex:none;white-space:nowrap}
.xp-col header .xp-node{margin-left:auto;white-space:nowrap;font:400 11px var(--mono);letter-spacing:.06em;color:var(--ink-50)}
.xp-msgs{display:flex;flex-direction:column;gap:12px;padding:18px;overflow:auto}
.xp-m{max-width:88%;padding:11px 15px;border-radius:18px;font-size:14.5px;line-height:1.65;white-space:pre-wrap;word-break:break-word}
.xp-m.u{align-self:flex-end;background:#000;color:#fff;border-bottom-right-radius:6px}
.xp-m.a{align-self:flex-start;background:var(--gray-btn);color:var(--ink-70);border-bottom-left-radius:6px}
.xp-met{display:flex;flex-wrap:wrap;gap:4px 16px;padding:13px 18px;border-top:1px solid var(--line);font:400 11px var(--mono);letter-spacing:.04em;color:var(--ink-50)}
.xp-met b{font-weight:400;color:var(--ink)}
@media (max-width:1100px){.xp-cards{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:860px){
  .xp-stage{padding:64px 16px 40px}
  .xp-bg{height:520px}
  .xp-h{font-size:36px}
  .xp-box textarea{min-height:64px;font-size:16px}
  .xp-cards{grid-template-columns:minmax(0,1fr)}
  .xp-card{grid-template-rows:132px auto}
  .xp-art .bt-collage{width:110px;height:110px}
  .xp[data-mode="chat"] .xp-stage{padding:24px 16px}
  .xp-cols.n2,.xp-cols.n3{grid-template-columns:minmax(0,1fr)}
  .xp-col{height:auto;min-height:280px}
  .xp-pop{left:8px!important;right:8px!important;width:auto!important}
  .xp-p2{grid-template-columns:minmax(0,1fr)}
}
</style>
'''
k = s.rindex('</head>'); s = s[:k] + CSS + s[k:]

JS = r'''
  /* ======== 体验中心（2026-10-14 第二版） ======== */
  (function(){
    var xp=$('#xp'); if(!xp) return;
    var TPL=__TPL__;
    var sel=['glm-5-3-flash'], hist=[[]], box=$('#xpBox'), slot=0, cat='全部';
    var CH='<svg class="ch" viewBox="0 0 12 12" aria-hidden="true"><path d="M3 4.5 6 7.5 9 4.5" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg>';
    function mm(id){return byId[id]||M[0]}
    function reasoning(){return sel.some(function(id){return mm(id).type.indexOf('推理')>=0})}
    function closePop(){['#xpMPop','#xpPar'].forEach(function(k){$(k).hidden=true}); $('#xpParB').setAttribute('aria-expanded','false')}
    function pills(){
      $('#xpPills').innerHTML=sel.map(function(id,i){var m=mm(id); return '<span class="xp-pill"><button type="button" data-slot="'+i+'" aria-haspopup="listbox" aria-label="更换模型 '+esc(m.name)+'">'+vlogo(m.vendor,16)+'<span>'+esc(m.name)+'</span>'+CH+'</button>'+(sel.length>1?'<button class="xp-x" type="button" data-rm="'+i+'" aria-label="移除这个模型">×</button>':'')+'</span>'}).join('');
      $('#xpAdd').hidden=sel.length>=3; $('#xpBudW').hidden=!reasoning();
      $$('#xpPills [data-slot]').forEach(function(b){b.addEventListener('click',function(e){e.stopPropagation(); var open=$('#xpMPop').hidden||slot!==+b.getAttribute('data-slot'); closePop(); if(!open) return; slot=+b.getAttribute('data-slot'); $('#xpMQ').value=''; mlist(); $('#xpMPop').hidden=false; $('#xpMQ').focus()})});
      $$('#xpPills [data-rm]').forEach(function(b){b.addEventListener('click',function(e){e.stopPropagation(); var i=+b.getAttribute('data-rm'); sel.splice(i,1); hist.splice(i,1); pills(); cols(); chips(); code()})}) }
    function mlist(){var q=($('#xpMQ').value||'').trim().toLowerCase();
      $('#xpML').innerHTML=M.filter(function(m){return !q||(m.name+' '+m.vendor+' '+m.type.join(' ')).toLowerCase().indexOf(q)>=0}).map(function(m){return '<button class="xp-mi" type="button" role="option" data-id="'+m.id+'" aria-selected="'+(sel[slot]===m.id)+'">'+vlogo(m.vendor,18)+'<b>'+esc(m.name)+'</b><span class="bt-tag g">'+m.type.join(' · ')+'</span><span class="m2">'+esc(m.vendor)+' · 上下文 '+m.ctx+' · 输出 ¥'+m.mkt.toFixed(2)+' / 百万词元</span></button>'}).join('')||'<p class="m2" style="padding:10px;color:var(--ink-50)">没有符合条件的模型</p>';
      $$('#xpML [data-id]').forEach(function(b){b.addEventListener('click',function(){sel[slot]=b.getAttribute('data-id'); closePop(); pills(); cols(); chips(); code(); $('#xpQ').focus()})}) }
    $('#xpMQ').addEventListener('input',mlist);
    function chips(){ $('#xpChips').innerHTML=M.map(function(m){return '<button class="xp-chip" type="button" data-id="'+m.id+'" aria-pressed="'+(sel[0]===m.id)+'">'+vlogo(m.vendor,18)+'<span>'+esc(m.name)+'</span></button>'}).join('');
      $$('#xpChips [data-id]').forEach(function(b){b.addEventListener('click',function(){sel[0]=b.getAttribute('data-id'); pills(); chips(); code(); $('#xpQ').focus()})}) }
    function cards(){ var list=TPL.filter(function(t){return cat==='全部'||t[0]===cat});
      $('#xpCards').innerHTML=list.map(function(t){var m=mm(t[3]); return '<button class="xp-card" type="button" data-t="'+TPL.indexOf(t)+'"><span class="xp-art"><span class="bt-collage" data-art="'+t[4]+'" aria-hidden="true"></span></span><span class="xp-ct"><span class="k">'+t[0]+'</span><b>'+esc(t[1])+'</b><p>'+esc(t[2])+'</p><span class="xp-mc">'+vlogo(m.vendor,14)+esc(m.name)+'</span></span></button>'}).join('');
      $$('#xpCards [data-t]').forEach(function(b){b.addEventListener('click',function(){var t=TPL[+b.getAttribute('data-t')]; sel[0]=t[3]; $('#xpQ').value=t[2]; pills(); chips(); code(); var q=$('#xpQ'); q.focus(); q.setSelectionRange(q.value.length,q.value.length); window.scrollTo({top:0,behavior:'smooth'})})}) }
    $$('#xpTabs .bt-chip').forEach(function(b){b.addEventListener('click',function(){cat=b.getAttribute('data-c'); $$('#xpTabs .bt-chip').forEach(function(x){var on=x===b; x.classList.toggle('on',on); x.setAttribute('aria-pressed',String(on))}); cards()})});
    function bj(){return new Date(Date.now()+(new Date().getTimezoneOffset()+480)*6e4)}
    function msg(r){return '<div class="xp-m '+(r.u?'u':'a')+'">'+esc(r.t)+'</div>'}
    function cols(){var c=$('#xpCols'); if(xp.getAttribute('data-mode')!=='chat'){c.innerHTML=''; return}
      c.className='xp-cols n'+sel.length;
      c.innerHTML=sel.map(function(id,i){var m=mm(id); return '<article class="xp-col"><header>'+vlogo(m.vendor,18)+'<b>'+esc(m.name)+'</b><span class="bt-tag g">'+m.type.join(' · ')+'</span><span class="xp-node">节点 · 自动调度</span></header>'+
        '<div class="xp-msgs">'+(hist[i]||[]).map(msg).join('')+'</div>'+
        '<footer class="xp-met"><span>首字时延 <b>--</b></span><span>速度 <b>--</b></span><span>词元 <b>--</b></span><span>费用 <b>--</b></span><span>产地 <b>--</b></span></footer></article>'}).join('');
      $$('#xpCols .xp-msgs').forEach(function(x){x.scrollTop=x.scrollHeight}) }
    function code(){var m=mm(sel[0]), msgs=[], sys=$('#xpS').value.trim(); if(sys) msgs.push({role:'system',content:sys}); msgs.push({role:'user',content:$('#xpQ').value.trim()||'你好'});
      var body={model:m.name,messages:msgs,temperature:+$('#xpT').value,top_p:+$('#xpP').value,max_tokens:parseInt($('#xpN').value,10)||1024};
      $('#xpCodeT').innerHTML='<span class="g"># 对比时每个模型各发一次请求，只改 model</span>\ncurl <span class="s">https://__HOST__/v1/chat/completions</span> \\\n  -H <span class="s">"Authorization: Bearer $API_KEY"</span> \\\n  -H <span class="s">"Content-Type: application/json"</span> \\\n  -d <span class="s">\''+esc(JSON.stringify(body))+'\'</span>'}
    $('#xpAdd').addEventListener('click',function(){var next=M.filter(function(x){return sel.indexOf(x.id)<0})[0]; if(!next) return; sel.push(next.id); hist.push((hist[0]||[]).filter(function(r){return r.u}).map(function(r){return {u:1,t:r.t}})); pills(); cols(); code()});
    $('#xpParB').addEventListener('click',function(e){e.stopPropagation(); var open=$('#xpPar').hidden; closePop(); $('#xpPar').hidden=!open; this.setAttribute('aria-expanded',String(open))});
    $('#xpT').addEventListener('input',function(){$('#xpTv').textContent=(+this.value).toFixed(1); code()});
    $('#xpP').addEventListener('input',function(){$('#xpPv').textContent=String(+(+this.value).toFixed(2)); code()});
    ['#xpN','#xpB','#xpS','#xpQ'].forEach(function(k2){$(k2).addEventListener('input',code)});
    $('#xpReset').addEventListener('click',function(){$('#xpT').value=0.7; $('#xpTv').textContent='0.7'; $('#xpP').value=1; $('#xpPv').textContent='1'; $('#xpN').value=1024; $('#xpB').value=4096; $('#xpS').value=''; code()});
    $('#xpCodeB').addEventListener('click',function(){var c=$('#xpCode'), open=c.hidden; c.hidden=!open; this.setAttribute('aria-expanded',String(open)); code(); bindCopy()});
    $$('#xpMPop,#xpPar').forEach(function(p){p.addEventListener('click',function(e){e.stopPropagation()})});
    document.addEventListener('click',function(){if(!$('#xpMPop').hidden||!$('#xpPar').hidden) closePop()});
    document.addEventListener('keydown',function(e){if(e.key==='Escape'&&(!$('#xpMPop').hidden||!$('#xpPar').hidden)) closePop()});
    box.addEventListener('submit',function(e){e.preventDefault(); var q=$('#xpQ').value.trim(); if(!q){$('#xpQ').focus(); return}
      closePop(); xp.setAttribute('data-mode','chat');
      sel.forEach(function(id,i){var m=mm(id); hist[i]=hist[i]||[]; hist[i].push({u:1,t:q});
        var t='体验中心尚未开通。开通后这里显示 '+m.name+' 的回答，以及首字时延、速度、词元、费用和电站产地。';
        if(!__LIVE__&&/deepseek/i.test(m.id)){var h=bj().getHours(); t+='\n现在按'+((h>=22||h<8)?'闲时':'忙时')+'价计费。'}
        hist[i].push({u:0,t:t})});
      $('#xpQ').value=''; cols(); code()});
    $('#xpQ').addEventListener('keydown',function(e){if(e.key==='Enter'&&!e.shiftKey&&!e.isComposing){e.preventDefault(); box.requestSubmit()}});
    $('#xpNew').addEventListener('click',function(){hist=sel.map(function(){return []}); xp.setAttribute('data-mode','empty'); cols(); $('#xpQ').focus()});
    window.supPlaySet=function(id){if(!byId[id]) return; sel=[id]; hist=[[]]; xp.setAttribute('data-mode','empty'); pills(); cols(); chips(); code()};
    pills(); chips(); cards(); code();
  })();
'''.replace('__HOST__', 'api.fathompeak.cn').replace('__TPL__', json.dumps(TPL, ensure_ascii=False)).replace('__LIVE__', 'true' if LIVE else 'false')
rep("  $$('[data-product-target]').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();jumpTo(a.getAttribute('data-product-target'))})});\n  window.addEventListener('hashchange',route); route();",
    JS + "  $$('[data-product-target]').forEach(function(a){a.addEventListener('click',function(e){e.preventDefault();jumpTo(a.getAttribute('data-product-target'))})});\n  window.addEventListener('hashchange',route); route();")

RX_ADD = (",\n    [/^体验中心尚未开通。开通后这里显示 (.+) 的回答，以及首字时延、速度、词元、费用和电站产地。$/, function(m,a){return 'The playground is not enabled yet. Once it is, this shows the answer from '+a+', with time to first token, speed, tokens, cost and the plant it ran on.'}],"
          "\n    [/^更换模型 (.+)$/, function(m,a){return 'Change model '+a}]")
rep('\n  ];\n  function rxTr(k){', RX_ADD + '\n  ];\n  function rxTr(k){')
EN = {
    '体验中心': 'Playground', '今天想试哪个模型？': 'Which model will you try today?', '新': 'New', '模型目录收录 7 个模型': '7 models in the catalog', '新对话': 'New chat',
    '输入问题，或从下面选一个模板': 'Ask a question, or pick a template below', '输入问题': 'Question', '+ 对比': '+ Compare', '参数': 'Parameters', '发送': 'Send',
    '查找模型': 'Find a model', '选择模型': 'Choose a model', '没有符合条件的模型': 'No models match', '温度': 'Temperature', '最大输出词元': 'Max output tokens', '思考预算': 'Thinking budget',
    '系统提示词': 'System prompt', '可选，例如：用中文简洁回答': 'Optional, e.g. answer briefly in English', '算力节点': 'Compute node', '自动调度（按时段与节点余量）': 'Auto-scheduled (by time and node capacity)',
    '恢复默认': 'Reset', '查看代码': 'View code', '快速选择模型': 'Quick model pick', '模板分类': 'Template categories', '全部': 'All', '写作': 'Writing', '编程': 'Coding', '翻译': 'Translation', '分析': 'Analysis', '客服': 'Support',
    '写一篇产品发布稿': 'Write a product launch post', '把文案改得更口语': 'Make copy more conversational', '解释一段代码': 'Explain some code', '写单元测试': 'Write unit tests', '中英互译，保留术语': 'Translate, keeping terms consistent',
    '总结长文要点': 'Summarize a long article', '从数据里找规律': 'Find patterns in data', '写一段客服回复': 'Write a support reply',
    '为一款面向开发者的大模型 API 平台写一篇 300 字的产品发布稿，语气专业、简洁。': 'Write a 300-word launch post for an LLM API platform for developers. Keep it professional and concise.',
    '体验中心按实际用量从余额扣费，价格见': 'Playground usage is deducted from your balance; prices are on the', '定价': 'pricing page',
    '内容由人工智能生成，仅供参考，请遵守': 'Content is AI-generated and for reference only. Please follow the', '用户服务协议': 'Terms of Service', '。生成式人工智能服务备案号：--': '. Generative AI service filing number: --',
    '节点 · 自动调度': 'Node · auto-scheduled', '首字时延': 'First token', '速度': 'Speed', '词元': 'Tokens', '费用': 'Cost', '产地': 'Origin', '现在按闲时价计费。': 'Billed at off-peak prices now.', '现在按忙时价计费。': 'Billed at peak prices now.',
    '移除这个模型': 'Remove this model', '去体验中心 →': 'Open the playground →', '待公司提供': 'Company to provide',
}
rep('  syncAuthLocale(); applyLang();', '  (function(S){for(var k in S) if(!(k in I18N)) I18N[k]=S[k]})(' + json.dumps(EN, ensure_ascii=False) + ');  /* 体验中心英文：只补缺 */\n  syncAuthLocale(); applyLang();')
open(OUT, 'w', encoding='utf8').write(s)
print('done:', OUT, f'（在线试用 → 体验中心 {n_ren} 处）')
