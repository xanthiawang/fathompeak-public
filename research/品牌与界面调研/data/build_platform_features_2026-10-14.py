"""2026-10-14 控制台与文档：补齐原平台（new-api）里不需要新数据的功能。
控制台：Key 导入客户端（Cherry Studio / CC Switch / Lobe Chat / DeepChat，逐项复制 base_url、Key、模型名称）；
创建 Key 加分组、无限额度开关、批量创建 1–20；概览开始使用清单（已创建 Key / 已充值 / 已发出首个请求，按账户状态计算）；
余额旁的可用时长（余额 ÷ 近 24 小时消费，没有消费显示 --）；公告、常见问答面板（空状态）；使用日志按模型消费图（近 7 / 30 天，
只读 LOGS，空时空状态）；右上角通知铃（空状态）；安全与访问加第三方账号绑定（微信，未绑定）；子账号改为成员（列表、邀请、角色）。
文档：接入客户端加编程工具 / 聊天机器人框架 / 翻译工具 / AQBot；模型与计费加缓存计费与推理强度后缀（不写价格）。
所有新增中文都在 I18N 末尾一个 Object.assign 里给英文。
usage: python3 build_platform_features_2026-10-14.py <index.html>
每个锚点必须恰好命中一次，命不中就停，不写文件。"""
import sys, pathlib

p = pathlib.Path(sys.argv[1]); s = p.read_text(encoding='utf-8')
EDITS = []
def edit(anchor, new, mode='replace'):
    EDITS.append((anchor, new, mode))

# ───────────────────────── CSS ─────────────────────────
CSS = r'''<style id="bt-platform-css">
/* 2026-10-14 原平台功能补齐（不需要新数据）：通知铃、开始使用清单、可用时长、公告与常见问答、按模型消费图、
   Key 导入客户端与批量创建、成员与角色、第三方账号绑定；文档的客户端分组。数据为空时一律显示空状态 */
.bt{position:relative}
.bt-bellw{position:absolute;top:8px;right:14px;z-index:30}
.bt-bell{appearance:none;width:34px;height:34px;border-radius:999px;border:1px solid var(--glass-line);background:var(--glass);box-shadow:var(--dia-sh);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);display:grid;place-items:center;color:var(--ink-70);cursor:pointer;position:relative;padding:0;transition:box-shadow .3s var(--out),color .2s var(--ease)}
.bt-bell:hover,.bt-bell[aria-expanded="true"]{color:var(--ink);box-shadow:var(--dia-sh2)}
.bt-bell svg{width:17px;height:17px}
.bt-bell i{position:absolute;top:6px;right:7px;width:7px;height:7px;border-radius:50%;background:var(--blue-1);box-shadow:0 0 0 2px #fff}
.bt-ntfpop{right:14px;top:50px;width:340px}
.bt-ntf0{display:grid;gap:4px;justify-items:center;text-align:center;padding:24px 18px 22px}
.bt-ntf0 b{font:400 19px/1.3 var(--serif);letter-spacing:-.01em;font-variation-settings:"opsz" 144}
.bt-ntf0 p{margin:0;font-size:13.5px;color:var(--ink-70)}
.bt-ntfl{list-style:none;margin:0;padding:0;display:grid;max-height:320px;overflow:auto}
.bt-ntfl li,.bt-ann li{display:grid;gap:2px;padding:12px 14px;border-bottom:1px solid var(--line)}
.bt-ntfl b,.bt-ann b{font:500 14.5px var(--sans)} .bt-ntfl p,.bt-ann p{margin:0;font-size:13.5px;color:var(--ink-70)} .bt-ntfl .mono,.bt-ann .mono{font-size:12px;color:var(--ink-50)}
@media (min-width:1201px){.bt:not(.no-rail) .bt-rs:first-child{padding-top:54px}}

/* 概览：开始使用清单（按账户状态打勾） */
.bt-prog{font:400 13px var(--mono);color:var(--ink-50);white-space:nowrap}
.bt-check{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
.bt-check li{display:grid;grid-template-columns:24px minmax(0,1fr);gap:8px 12px;align-content:start;background:rgba(255,255,255,.58);border:1px solid rgba(0,0,0,.06);border-radius:16px;padding:18px 18px 16px;box-shadow:0 1px 2px rgba(0,0,0,.025),0 10px 24px -16px rgba(0,0,0,.10)}
.bt-check li>i{width:22px;height:22px;border-radius:50%;border:1.5px solid var(--ink-30);position:relative;margin-top:1px}
.bt-check li.done>i{background:#000;border-color:#000}
.bt-check li.done>i:after{content:"";position:absolute;left:6px;top:6px;width:8px;height:4px;border-left:1.5px solid #fff;border-bottom:1.5px solid #fff;transform:rotate(-45deg)}
.bt-check li>div{display:grid;gap:4px;min-width:0}
.bt-check b{font:500 15.5px var(--sans)}
.bt-check p{margin:0;font-size:13.5px;line-height:1.55;color:var(--ink-70)}
.bt-check .cs-st{font-size:12.5px;color:var(--ink-50)}
.bt-check li>.bt-btn{grid-column:2;justify-self:start;height:36px;padding:0 16px}
.bt-check li.done>.bt-btn{display:none}

/* 概览：公告、常见问答（平台接口填充前是空状态） */
.bt-two{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}
.bt-box{display:grid;gap:14px;align-content:start;min-width:0}
.bt-mini,.bt-ann,.bt-faq{background:rgba(255,255,255,.58);border:1px solid rgba(0,0,0,.06);border-radius:16px;box-shadow:0 1px 2px rgba(0,0,0,.025),0 10px 24px -16px rgba(0,0,0,.10)}
.bt-mini{display:grid;gap:6px;justify-items:start;padding:22px 22px 24px}
.bt-mini b{font:500 15.5px var(--sans)} .bt-mini p{margin:0;font-size:14px;color:var(--ink-70)}
.bt-ann{list-style:none;margin:0;padding:0;overflow:hidden}
.bt-ann li:last-child{border-bottom:0}
.bt-faq{overflow:hidden}
.bt-faq details{border-bottom:1px solid var(--line)} .bt-faq details:last-child{border-bottom:0}
.bt-faq summary{padding:14px 18px;cursor:pointer;font-weight:500}
.bt-faq details p{margin:0;padding:0 18px 16px;color:var(--ink-70);font-size:14px}

/* 钱包：四格（余额、可用时长、累计消费、请求次数） */
.cs-tiles.n4{grid-template-columns:repeat(4,minmax(0,1fr))}
.cs-tiles .cs-help{font-size:12.5px}

/* 使用日志：按模型的每日消费（堆叠柱，颜色跟随模型在目录中的顺序） */
.cs-trend{margin-bottom:6px}
.cs-trhd{display:flex;align-items:center;justify-content:space-between;gap:10px 16px;flex-wrap:wrap;margin:0 0 12px}
.cs-trhd .cs-h3{margin:0}
.cs-seg{display:flex;gap:6px}
.cs-chart{position:relative;background:var(--card);border:1px solid var(--line);border-radius:16px;padding:22px 22px 14px}
.cs-trplot{position:relative;height:200px;margin-left:64px}
.cs-trgrid span{position:absolute;left:0;right:0;height:0;border-top:1px solid var(--line)}
.cs-trgrid span:last-child{border-top-color:var(--ink-30)}
.cs-trgrid em{position:absolute;right:calc(100% + 10px);top:-8px;font:400 11.5px var(--mono);font-style:normal;color:var(--ink-50);white-space:nowrap}
.cs-trbars{position:absolute;inset:0;display:grid;gap:4px;align-items:end}
.cs-trbars.n30,.cs-trx.n30{gap:2px}
.cs-trc{height:100%;display:flex;flex-direction:column-reverse;gap:2px;outline:none;border-radius:4px 4px 0 0;min-width:0}
.cs-trc:hover,.cs-trc:focus-visible{background:rgba(0,0,0,.035)}
.cs-trc:focus-visible{outline:2px solid var(--blue-1);outline-offset:1px}
.cs-trc i{display:block;flex:none;min-height:1px}
.cs-trc i:last-child{border-radius:3px 3px 0 0}
.cs-trx{display:grid;gap:4px;margin:8px 0 0 64px;font:400 11px var(--mono);color:var(--ink-50)}
.cs-trx span{display:flex;justify-content:center;min-width:0;white-space:nowrap}
.cs-trlg{list-style:none;margin:16px 0 0;padding:0;display:flex;flex-wrap:wrap;gap:6px 18px;font-size:13px;color:var(--ink-70)}
.cs-trlg i,.cs-trtip i{display:inline-block;width:10px;height:10px;border-radius:3px;margin-right:6px;vertical-align:-1px;flex:none}
.cs-trtip{position:absolute;z-index:5;top:12px;pointer-events:none;background:rgba(255,255,255,.97);border:1px solid var(--line);border-radius:12px;box-shadow:0 8px 24px rgba(0,0,0,.10);padding:10px 12px;font-size:13px;min-width:190px;display:grid;gap:5px}
.cs-trtip>.mono{font-size:12px;color:var(--ink-50)}
.cs-trtip div{display:flex;align-items:center;gap:4px}
.cs-trtip div span:last-child{margin-left:auto;padding-left:14px;font-family:var(--mono)}
.cs-trtip .cs-trsum{border-top:1px solid var(--line);padding-top:5px;font-weight:500}

/* 创建 Key：分组、批量创建、无限额度开关 */
.cs-lbrow{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap}
.cs-lbrow>label:first-child{font:500 14px var(--sans);color:var(--ink)}
.cs-sw{display:inline-flex;align-items:center;gap:8px;font-size:13.5px;color:var(--ink-70);cursor:pointer;white-space:nowrap}
.cs-sw input{appearance:none;-webkit-appearance:none;margin:0;width:34px;height:20px;border-radius:999px;background:rgba(0,0,0,.18);position:relative;cursor:pointer;flex:none;transition:background-color .2s var(--ease)}
.cs-sw input:before{content:"";position:absolute;top:2px;left:2px;width:16px;height:16px;border-radius:50%;background:#fff;box-shadow:0 1px 2px rgba(0,0,0,.2);transition:transform .2s var(--ease)}
.cs-sw input:checked{background:#000} .cs-sw input:checked:before{transform:translateX(14px)}
.cs-sw input:focus-visible{outline:2px solid var(--blue-1);outline-offset:2px}
.cs-f>input.in:disabled{background:var(--paper);color:var(--ink-30);cursor:not-allowed}
.cs-f>select.in{height:44px;font-size:15px}
#csKey{white-space:pre-line}
.cs-reveal .cs-keyrow code{flex:1 1 280px} /* 新 Key 旁有「复制」「导入客户端」两个按钮：窄屏时 Key 独占一行，按钮换到下一行 */

/* 导入客户端对话框 */
.cs-imptabs{display:flex;flex-wrap:wrap;gap:6px}
.cs-impk{margin:0;font-size:14px;color:var(--ink-70);overflow-wrap:anywhere} .cs-impk b{color:var(--ink);font-weight:500}
.cs-impstep{margin:0;font-size:14px;line-height:1.6;color:var(--ink-70)}
.cs-imprw{display:grid;gap:6px;min-width:0}
.cs-imprw code{background:var(--paper)!important}
.cs-imprw .btn:disabled{opacity:.4;cursor:not-allowed}

/* 成员与角色 */
.cs-mem .cs-newf .mk-sel{height:38px;font-size:13px}
.cs-mems{list-style:none;margin:0;padding:0;border-top:1px solid var(--line)}
.cs-mems li{display:grid;grid-template-columns:minmax(0,1fr) auto auto auto;gap:8px 18px;align-items:center;padding:12px 0;border-bottom:1px solid var(--line);font-size:14px}
.cs-mm{min-width:0;display:grid;gap:2px} .cs-mm>span:first-child{overflow-wrap:anywhere;color:var(--ink)}
.cs-you{font:400 11px var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--ink-50)}
.cs-mems .cs-st{font-size:13px;color:var(--ink-70);white-space:nowrap}
.cs-mems .mk-sel{height:30px}

/* 手机上宽内容不撑开页面：控制台分页（模型 API 宽表）与文档正文列都按 minmax(0,1fr) 收住，长地址可换行 */
.bt-pg,.bt-sec{grid-template-columns:minmax(0,1fr)}
.bt-tw{position:relative} /* 表头里绝对定位的读屏文字（如「固定」）要被表格滚动容器收住，否则手机上会撑出横向滚动 */
.two.docs>div{min-width:0}
.docs p .mono{overflow-wrap:anywhere}

/* 文档：接入客户端分组 */
.docs h2.dg{font:400 11px var(--mono);letter-spacing:.06em;text-transform:uppercase;color:var(--ink-50);margin:38px 0 0;padding-top:16px;border-top:1px solid var(--line)}
.docs h2.dg+h3,.docs .dn+h3{margin-top:14px}
.docs .dn{background:var(--paper-2);border-radius:var(--r12);padding:12px 16px;font-size:14px;max-width:none;margin:12px 0 0}

@media (min-width:761px) and (max-width:1000px){.bt-check{grid-template-columns:minmax(0,1fr)}}
@media (max-width:800px){.cs-tiles.n4>div:first-child{grid-column:auto} .cs-kt td.cs-ops{white-space:normal;max-width:190px} .cs-kt .cs-ops .ac-link{margin:0 0 4px 12px} .cs-mems li{grid-template-columns:minmax(0,1fr) auto} .cs-mems li>.cs-mm{grid-column:1/-1}}
@media (max-width:760px){
  .bt-org{padding-right:44px}
  .bt-ntfpop{left:12px;right:12px;top:52px;width:auto}
  .bt-check,.bt-two{grid-template-columns:minmax(0,1fr)}
  .cs-chart{padding:16px 12px 12px}
  .cs-trplot{height:170px;margin-left:54px}
  .cs-trx{margin-left:54px}
  .cs-trgrid em{right:calc(100% + 6px);font-size:11px}
}
</style>
'''
edit('  .bt-credpop{left:12px;right:12px;bottom:auto;top:56px;width:auto}\n}\n</style>\n', CSS, 'after')

# ───────────────────────── 控制台 HTML ─────────────────────────
BELL = '''    <div class="bt-bellw"><button class="bt-bell" type="button" id="btBell" aria-label="通知" aria-haspopup="true" aria-expanded="false" aria-controls="btNtfPop"><svg viewBox="0 0 20 20" aria-hidden="true"><path d="M10 3a4.5 4.5 0 0 0-4.5 4.5c0 4-1.5 5.5-1.5 5.5h12s-1.5-1.5-1.5-5.5A4.5 4.5 0 0 0 10 3ZM8.3 16a1.8 1.8 0 0 0 3.4 0" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/></svg><i id="btBellDot" hidden></i></button></div>
    <div class="bt-pop bt-ntfpop" id="btNtfPop" hidden>
      <div class="bt-pophd"><b>通知</b><span>余额预警与公告</span></div>
      <ul class="bt-ntfl" id="btNtfL" hidden></ul>
      <div class="bt-ntf0" id="btNtf0"><b>还没有通知</b><p>余额预警和平台公告会显示在这里。</p></div>
      <button type="button" data-go="acct"><svg viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="10" r="2.6" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M10 2.5v2.2M10 15.3v2.2M2.5 10h2.2M15.3 10h2.2M4.7 4.7l1.6 1.6M13.7 13.7l1.6 1.6M4.7 15.3l1.6-1.6M13.7 6.3l1.6-1.6" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>设置余额预警</button>
    </div>
'''
edit('\n    <div class="bt-main cs-main">\n', BELL, 'before_nl')

edit('<div class="bt-cred"><b>余额</b><p>在线充值后按实际用量扣费。</p><span class="mono" id="btCredBal">¥0.00</span></div>',
     '\n        <div class="bt-cred"><b>可用时长</b><p>按余额和近 24 小时消费估算。</p><span class="mono" id="btCredRun">--</span></div>', 'after')

CHECK = '''        <div class="bt-sec">
          <div class="bt-hd"><h2>开始使用</h2><span class="bt-prog" id="btProg">0 / 3</span></div>
          <ol class="bt-check" id="btCheck">
            <li data-ck="key"><i aria-hidden="true"></i><div><b>已创建 Key</b><p>按项目创建 API Key，完整 Key 只在创建时显示一次。</p><span class="cs-st">未完成</span></div><button class="bt-btn" type="button" data-go="keys">创建 API Key</button></li>
            <li data-ck="topup"><i aria-hidden="true"></i><div><b>已充值</b><p>在线充值后按实际用量扣费。</p><span class="cs-st">未完成</span></div><button class="bt-btn" type="button" data-go="bill">去充值</button></li>
            <li data-ck="req"><i aria-hidden="true"></i><div><b>已发出首个请求</b><p>用 Key 调用任一模型，请求会出现在使用日志里。</p><span class="cs-st">未完成</span></div><a class="bt-btn" href="#docs">查看接入文档</a></li>
          </ol>
        </div>
'''
edit('        <div class="bt-sec">\n          <h2>模型 API</h2>', CHECK, 'before')  # 概览顶部留给 API Key 光场区，清单放在它后面

BOARD = '''        <div class="bt-sec">
          <div class="bt-two">
            <div class="bt-box"><h2>公告</h2><ul class="bt-ann" id="btAnn" hidden></ul><div class="bt-mini" id="btAnn0"><b>还没有公告</b><p>平台发布的维护和服务公告会显示在这里。</p></div></div>
            <div class="bt-box"><h2>常见问答</h2><div class="bt-faq" id="btFaq" hidden></div><div class="bt-mini" id="btFaq0"><b>还没有常见问答</b><p>平台整理的常见问题会显示在这里。</p><a class="bt-a" href="#docs">查看接入文档 →</a></div></div>
          </div>
        </div>
'''
edit('        <div class="bt-sec">\n          <h2>学习</h2>', BOARD, 'before')

edit('<div class="cs-reveal" id="csReveal" hidden><span class="k">新的 API Key</span><p>复制并保存这个 Key，关闭后无法再次查看。</p><div class="cs-keyrow"><code class="mono" id="csKey"></code><button class="btn black sm" type="button" id="csCopy">复制</button></div>',
     '<div class="cs-reveal" id="csReveal" hidden><span class="k">新的 API Key</span><p id="csRevP">复制并保存这个 Key，关闭后无法再次查看。</p><div class="cs-keyrow"><code class="mono" id="csKey"></code><button class="btn black sm" type="button" id="csCopy">复制</button><button class="btn gray sm" type="button" id="csRevImp">导入客户端</button></div>')

edit('''              <div class="cs-f2">
                <div class="cs-f"><label for="csKquota">额度上限（¥）</label><input class="in mono" id="csKquota" name="quota" inputmode="decimal" autocomplete="off"><p class="cs-help">选填。留空表示不限额度。</p></div>
                <div class="cs-f"><label for="csKexp">过期时间</label>''',
     '''              <div class="cs-f2">
                <div class="cs-f"><label for="csKg">分组</label><select class="in" id="csKg" name="group"><option value="default">默认</option></select><p class="cs-help">平台开放其他分组后可在这里选择。</p></div>
                <div class="cs-f"><label for="csKcnt">批量创建</label><input class="in mono" id="csKcnt" name="cnt" type="number" min="1" max="20" step="1" value="1" inputmode="numeric" autocomplete="off"><p class="cs-help">一次创建 1–20 个 Key，名称后自动加序号。</p></div>
              </div>
              <div class="cs-f2">
                <div class="cs-f"><div class="cs-lbrow"><label for="csKquota">额度上限（¥）</label><label class="cs-sw"><input type="checkbox" id="csKinf" name="inf" checked><span>无限额度</span></label></div><input class="in mono" id="csKquota" name="quota" inputmode="decimal" autocomplete="off" disabled><p class="cs-help" id="csKqh">已开启无限额度。关闭后填写额度上限。</p></div>
                <div class="cs-f"><label for="csKexp">过期时间</label>''')

IMP = '''        <dialog class="cs-dlg" id="csImp" aria-labelledby="csImpT">
          <form method="dialog" id="csImpF">
            <div class="cs-dlg-hd"><h3 id="csImpT">导入客户端</h3><button class="cs-x" type="button" id="csImpX" aria-label="关闭">×</button></div>
            <div class="cs-fs">
              <p class="cs-impk"><span>API Key</span> <b id="csImpFor"></b></p>
              <div class="cs-imptabs" id="csImpTabs" role="tablist" aria-label="客户端"><button class="chip on" type="button" role="tab" aria-selected="true" data-cl="cherry">Cherry Studio</button><button class="chip" type="button" role="tab" aria-selected="false" tabindex="-1" data-cl="ccswitch">CC Switch</button><button class="chip" type="button" role="tab" aria-selected="false" tabindex="-1" data-cl="lobe">Lobe Chat</button><button class="chip" type="button" role="tab" aria-selected="false" tabindex="-1" data-cl="deepchat">DeepChat</button></div>
              <p class="cs-impstep" id="csImpStep"></p>
              <div class="cs-imprw"><span class="cs-lb">接口地址</span><div class="cs-keyrow"><code class="mono" id="csImpUrl"></code><button class="btn gray sm" type="button" data-impcp="Url">复制</button></div></div>
              <div class="cs-imprw"><span class="cs-lb">API Key</span><div class="cs-keyrow"><code class="mono" id="csImpKey"></code><button class="btn gray sm" type="button" data-impcp="Key">复制</button></div><p class="cs-help" id="csImpKh">完整 Key 只在创建时显示一次，请粘贴你保存的 Key。</p></div>
              <div class="cs-imprw"><span class="cs-lb">模型名称</span><div class="cs-keyrow"><code class="mono" id="csImpM"></code><button class="btn gray sm" type="button" data-impcp="M">复制</button></div></div>
              <p class="cs-help">将 YOUR_API_HOST 替换为平台提供的 HTTPS 接入域名。各客户端的菜单名称会随版本变化，以客户端当前版本为准。</p>
            </div>
            <div class="cs-dlg-ft"><a class="btn gray sm" href="#docs" id="csImpDoc">查看接入文档</a><button class="btn black sm" type="button" id="csImpOk">完成</button></div>
          </form>
        </dialog>
'''
edit('''            <div class="cs-dlg-ft"><button class="btn gray sm" type="button" id="csCancel">取消</button><button class="btn black sm" type="submit">创建</button></div>
          </form>
        </dialog>
''', IMP, 'after')

TREND = '''        <div class="cs-trend">
          <div class="cs-trhd"><h3 class="cs-h3">消费趋势</h3><div class="cs-seg" id="csTrSeg" role="group" aria-label="消费趋势时间范围"><button class="chip on" type="button" data-td="7" aria-pressed="true">近 7 天</button><button class="chip" type="button" data-td="30" aria-pressed="false">近 30 天</button></div></div>
          <div class="cs-chart" id="csTr" hidden>
            <div class="cs-trplot"><div class="cs-trgrid" id="csTrG"></div><div class="cs-trbars" id="csTrB"></div></div>
            <div class="cs-trx" id="csTrX" aria-hidden="true"></div>
            <ul class="cs-trlg" id="csTrL"></ul>
            <div class="cs-trtip" id="csTrTip" hidden></div>
          </div>
          <div class="cs-empty" id="csTr0"><b>还没有消费记录</b><span>发出请求后，这里按天显示每个模型的消费。</span></div>
        </div>
'''
edit('<div class="cs-hd"><div><h2>使用日志</h2><p>上方按模型汇总，下方逐条列出每次请求。</p></div></div>\n', TREND, 'after')

edit('<div class="cs-tiles"><div><span class="k">余额</span><b class="mono">¥0.00</b></div><div><span class="k">累计消费</span><b class="mono">¥0.00</b></div><div><span class="k">请求次数</span><b class="mono">0</b></div></div>',
     '<div class="cs-tiles n4"><div><span class="k">余额</span><b class="mono" id="csBal">¥0.00</b></div><div><span class="k">可用时长</span><b class="mono" id="csRun">--</b><span class="cs-help">按近 24 小时消费估算</span></div><div><span class="k">累计消费</span><b class="mono" id="csSpent">¥0.00</b></div><div><span class="k">请求次数</span><b class="mono" id="csReqs">0</b></div></div>')

edit('<div class="cs-empty"><b>还没有充值记录</b>', '<div class="cs-empty" id="csTopups0"><b>还没有充值记录</b>')

edit('''        <div class="cs-box" data-for="company" hidden><h3 class="cs-h3">子账号</h3><p>邀请同事加入，额度和账单由主账号统一管理。</p>
          <form class="cs-newf" id="csInv"><input class="in" type="email" name="email" placeholder="同事邮箱"><button class="btn black sm" type="submit">邀请</button></form>
          <ul class="cs-subs" id="csSubs"></ul></div>''',
     '''        <div class="cs-box cs-mem" data-for="company" hidden><h3 class="cs-h3">成员与角色</h3><p>邀请同事加入企业账户，额度和账单由企业账户统一管理。管理员可以管理成员、API Key 和账单；成员可以创建和使用自己的 API Key。</p>
          <form class="cs-newf" id="csInv" novalidate><input class="in" type="email" name="email" placeholder="同事邮箱" aria-label="同事邮箱" autocomplete="off"><select class="mk-sel" name="mrole" aria-label="角色"><option value="member">成员</option><option value="admin">管理员</option></select><button class="btn black sm" type="submit">邀请</button></form>
          <ul class="cs-mems" id="csSubs"></ul></div>''')

edit('''<button class="btn gray sm" type="button" id="csPk">添加通行密钥</button></li>
''', '''          <li><div><b>第三方账号绑定</b><p>绑定后可以用第三方账号登录。</p><span class="cs-st">微信账号：未绑定</span></div><button class="btn gray sm" type="button" id="csWx">绑定微信</button></li>
''', 'after')

# ───────────────────────── 文档 HTML ─────────────────────────
edit('''模型 = <span class="s">"GLM-5.3-Flash"</span></div>
        <h3>Cherry Studio</h3>''', '''模型 = <span class="s">"GLM-5.3-Flash"</span></div>
        <p>在控制台的 API Key 列表里点「导入客户端」，可以逐项复制接入地址、API Key 和模型名称。</p>
        <h2 class="dg">桌面与网页客户端</h2>
        <h3>Cherry Studio</h3>''')

DOCS = '''        <h3>AQBot</h3><p>在服务商设置里添加自定义服务商，类型选 OpenAI 兼容，API 地址填 <span class="mono">https://YOUR_API_HOST/v1</span>，再填 API Key 和模型名称。</p>
        <h2 class="dg">编程工具</h2>
        <p class="dn">编程工具要求平台开启对应接口：Claude Code 使用 Anthropic Messages 格式（<span class="mono">/v1/messages</span>），Codex CLI 使用 OpenAI Responses 格式（<span class="mono">/v1/responses</span>）。使用前请确认平台已为你要用的模型开启这些接口。</p>
        <h3>Claude Code</h3><p>用三个环境变量设置接入地址（不带 /v1）、API Key 和模型名称，然后在同一个终端运行 claude。</p>
        <div class="code pre"><button class="cp" data-copy>复制</button>export ANTHROPIC_BASE_URL=<span class="s">"https://YOUR_API_HOST"</span><br>export ANTHROPIC_AUTH_TOKEN=<span class="s">"$API_KEY"</span><br>export ANTHROPIC_MODEL=<span class="s">"GLM-5.3-Flash"</span><br>claude</div>
        <h3>Codex CLI</h3><p>编辑 <span class="mono">~/.codex/config.toml</span>，新增一个服务商：base_url 填接入地址，env_key 填保存 API Key 的环境变量名，model 填模型名称。设置好环境变量后，在终端运行 codex。</p>
        <div class="code pre"><button class="cp" data-copy>复制</button><span class="g"># ~/.codex/config.toml</span><br>model = <span class="s">"GLM-5.3-Flash"</span><br>model_provider = <span class="s">"fathompeak"</span><br><br>[model_providers.fathompeak]<br>name = <span class="s">"FathomPeak"</span><br>base_url = <span class="s">"https://YOUR_API_HOST/v1"</span><br>env_key = <span class="s">"API_KEY"</span><br>wire_api = <span class="s">"responses"</span></div>
        <h2 class="dg">聊天机器人框架</h2>
        <h3>LangBot</h3><p>在管理面板添加模型，供应商选 OpenAI 兼容，Base URL 填 <span class="mono">https://YOUR_API_HOST/v1</span>，再填 API Key 和模型名称。</p>
        <h3>AstrBot</h3><p>在管理面板的服务提供商里新增一项，类型选 OpenAI，API Base URL 填 <span class="mono">https://YOUR_API_HOST/v1</span>，再填 API Key 和模型名称。</p>
        <h2 class="dg">翻译工具</h2>
        <h3>Fluent Read（流畅阅读）</h3><p>在插件设置里把翻译服务设为自定义 OpenAI 兼容接口，接口地址填完整的 <span class="mono">https://YOUR_API_HOST/v1/chat/completions</span>，再填 API Key 和模型名称。</p>
        <h3>Luna Translator</h3><p>翻译设置里添加大模型通用接口，API 接口地址填 <span class="mono">https://YOUR_API_HOST/v1</span>，再填 API Key 和模型名称。</p>
'''
edit('        <p class="note">各客户端的菜单名称会随版本变化，以客户端当前版本为准。接入地址见控制台。</p></div>', DOCS, 'before')

edit('<h3>绿电记录</h3><p>核对订单的节点', '''<h3>缓存计费</h3><p>部分模型支持输入缓存：请求开头与近期请求相同的输入内容可以命中缓存，命中部分按缓存价计费，其余输入按普通输入价计费。是否支持缓存、缓存价是多少，取决于平台为该模型开启的配置，以模型详情和控制台为准。</p><h3>推理强度后缀</h3><p>支持推理强度的模型，可以在模型名称后加后缀指定推理强度，相当于把请求的推理强度（reasoning_effort）设为对应档位。推理强度越高，模型用于思考的 Token 通常越多，费用和耗时也会增加。哪些模型可以加后缀，取决于平台为该模型开启的配置。</p><div class="tbl"><table><tr><th>后缀</th><th>推理强度</th></tr><tr><td class="mono">-high</td><td>高</td></tr><tr><td class="mono">-medium</td><td>中</td></tr><tr><td class="mono">-low</td><td>低</td></tr></table></div>''', 'before')

# ───────────────────────── 控制台 JS ─────────────────────────
edit('  var LOGS=[];\n', '''  /* 2026-10-14 原平台功能补齐：以下数据同样由平台接口填充，前端不造数据。
     TOPUPS 充值记录 {t, no, via, amount, st}；BALANCE 余额（¥）；NOTICES 公告 {t, title, body}；ALERTS 余额预警等通知 {t, title, body}；FAQS 常见问答 {q, a} */
  var TOPUPS=[], BALANCE=0, NOTICES=[], ALERTS=[], FAQS=[];
''', 'after')

edit("""<td><span class="cs-l">分组</span>默认</td>""", """<td><span class="cs-l">分组</span>'+(k.group&&k.group!=='default'?esc(k.group):'默认')+'</td>""")
edit("""'<td class="cs-ops"><button class="ac-link" type="button" data-tog="'+i+'">'""",
     """'<td class="cs-ops"><button class="ac-link" type="button" data-imp="'+i+'">导入客户端</button><button class="ac-link" type="button" data-tog="'+i+'">'""")
edit("    $$('#csKeys [data-tog]').forEach(", """    $$('#csKeys [data-imp]').forEach(function(b){b.addEventListener('click',function(){var k=me.keys[+b.getAttribute('data-imp')];openImp(k,freshKey(k))})});
""", 'before')
edit("""    ['#csLt','#csLm','#csLk'].forEach(function(id){$(id).classList.toggle('on',id==='#csLt'?$(id).value!=='7':!!$(id).value)});
  }
""", """    ['#csLt','#csLm','#csLk'].forEach(function(id){$(id).classList.toggle('on',id==='#csLt'?$(id).value!=='7':!!$(id).value)});
    renderTrend();
  }
""")
edit("""    $('#csSubs').innerHTML=(me.subs||[]).map(function(s){return '<li><span>'+esc(s.email)+'</span><span>已邀请</span></li>'}).join('');
""", "    renderMembers();\n")
edit("    btRender();\n  }\n", "    btRender(); platRender();\n  }\n")
edit("function openDlg(){nf.reset();clearAccountError(nf);", "function openDlg(){nf.reset();syncInf();clearAccountError(nf);")

edit("""  nf.addEventListener('submit',function(e){e.preventDefault();var q=nf.quota.value.trim(),ex=nf.exp.value,ips=nf.ips.value.split(/[\\s,，]+/).filter(Boolean);
    if(q&&!(/^\\d+(\\.\\d{1,2})?$/.test(q)&&parseFloat(q)>0)) return accountError(nf,nf.quota,'额度上限请填写大于 0 的金额，最多两位小数。');
    if(ex&&ex<today()) return accountError(nf,nf.exp,'过期时间不能早于今天。');
    if(ips.some(function(x){return !IPRX.test(x)})) return accountError(nf,nf.ips,'IP 白名单格式不正确，请每行填写一个 IP 或网段。');
    var k=genKey(),n=nf.kname.value.trim()||('Key '+(me.keys.length+1));
    me.keys.unshift({name:n,tail:k.slice(-4),at:today(),on:true,quota:q?parseFloat(q):null,exp:ex,models:$$('#csKm .chip.on').map(function(c){return c.getAttribute('data-m')}),ips:ips});
    persist();closeDlg();$('#csKq').value='';$('#csKs').value='';$('#csKey').textContent=k;$('#csReveal').hidden=false;renderConsole()});
""", """  /* 无限额度开关：开着时不填额度；批量创建 1–20 个，名称后加序号；新 Key 的完整值只留在本次显示里（fresh），点「我已保存」后清掉 */
  function syncInf(){var on=nf.inf.checked;nf.quota.disabled=on;if(on)nf.quota.value='';$('#csKqh').textContent=on?'已开启无限额度。关闭后填写额度上限。':'这个 Key 的累计消费达到上限后停止调用。'}
  nf.inf.addEventListener('change',function(){syncInf();if(!nf.inf.checked)nf.quota.focus()});
  nf.addEventListener('submit',function(e){e.preventDefault();var inf=nf.inf.checked,q=nf.quota.value.trim(),c=nf.cnt.value.trim(),ex=nf.exp.value,ips=nf.ips.value.split(/[\\s,，]+/).filter(Boolean);
    if(!inf&&!(/^\\d+(\\.\\d{1,2})?$/.test(q)&&parseFloat(q)>0)) return accountError(nf,nf.quota,'额度上限请填写大于 0 的金额，最多两位小数。');
    if(!/^\\d+$/.test(c)||+c<1||+c>20) return accountError(nf,nf.cnt,'批量创建数量请填写 1 到 20 之间的整数。');
    if(ex&&ex<today()) return accountError(nf,nf.exp,'过期时间不能早于今天。');
    if(ips.some(function(x){return !IPRX.test(x)})) return accountError(nf,nf.ips,'IP 白名单格式不正确，请每行填写一个 IP 或网段。');
    var n=nf.kname.value.trim()||('Key '+(me.keys.length+1)),cnt=+c,ms=$$('#csKm .chip.on').map(function(x){return x.getAttribute('data-m')}),made=[];
    for(var i=cnt;i>=1;i--){var k=genKey(),nm=cnt>1?n+'-'+i:n;me.keys.unshift({name:nm,tail:k.slice(-4),at:today(),on:true,quota:inf?null:parseFloat(q),exp:ex,models:ms,ips:ips,group:nf.group.value});made.unshift({name:nm,tail:k.slice(-4),key:k})}
    fresh=made;persist();closeDlg();$('#csKq').value='';$('#csKs').value='';
    $('#csKey').textContent=made.map(function(x){return cnt>1?x.name+'  '+x.key:x.key}).join('\\n');
    $('#csRevP').textContent=cnt>1?'复制并保存这些 Key，关闭后无法再次查看。':'复制并保存这个 Key，关闭后无法再次查看。';
    $('#csReveal').hidden=false;renderConsole()});
""")
edit("  $('#csSaved').addEventListener('click',function(){$('#csReveal').hidden=true;$('#csKey').textContent=''});\n",
     "  $('#csSaved').addEventListener('click',function(){$('#csReveal').hidden=true;$('#csKey').textContent='';fresh=[]});\n  $('#csRevImp').addEventListener('click',function(){if(fresh.length)openImp(fresh[0],fresh[0].key)});\n")

edit("""  $('#csInv').addEventListener('submit',function(e){e.preventDefault();var m=this.email.value.trim().toLowerCase();if(!MAIL.test(m)){toast('请输入有效的邮箱地址。');return}me.subs=me.subs||[];me.subs.push({email:m,at:today()});persist();this.reset();renderConsole()});
""", """  /* 成员与角色：本人为管理员；邀请时选角色（管理员 / 成员），之后可改角色或移除。邀请邮件等平台接口 */
  $('#csInv').addEventListener('submit',function(e){e.preventDefault();var f=this,m=f.email.value.trim().toLowerCase();if(!MAIL.test(m)){toast('请输入有效的邮箱地址。');f.email.focus();return}
    me.subs=me.subs||[];if(m===String(me.email||'').toLowerCase()||me.subs.some(function(s){return s.email===m})){toast('这个邮箱已在成员列表中。');return}
    me.subs.push({email:m,at:today(),role:f.mrole.value==='admin'?'admin':'member'});persist();f.reset();renderConsole();toast('已加入成员列表。邀请邮件接入后即可发送。')});
""")
edit("$('#csOut').addEventListener('click',function(){signOut();ntf._for=null;closeDlg();", "$('#csOut').addEventListener('click',function(){signOut();ntf._for=null;closeDlg();closeImp();fresh=[];")

NEWJS = r"""  /* ---------- 2026-10-14 原平台功能补齐（不需要新数据） ---------- */
  /* 导入客户端：列出客户端需要的接入地址、API Key、模型名称，逐项复制。纯前端流程，不调用客户端的唤起协议。
     完整 Key 只在刚创建、还没点「我已保存」时可复制；其余情况只显示末 4 位 */
  var CLIENTS={cherry:{url:BASE,step:'设置 → 模型服务 → 添加，提供商类型选 OpenAI。API 地址不用带 /v1，Cherry Studio 会自动补全。'},
    ccswitch:{url:BASE+'/v1',step:'新增自定义供应商，按要切换的工具选择接口格式，填入请求地址和 API Key，保存后切换到这个供应商。'},
    lobe:{url:BASE+'/v1',step:'设置 → AI 服务商 → OpenAI，填入 API Key 和 API 代理地址，再获取模型列表或手动添加模型。'},
    deepchat:{url:BASE+'/v1',step:'设置 → 模型服务商 → 添加自定义服务商，类型选 OpenAI，填入 API URL 和 API Key，再拉取或添加模型。'}};
  var imp=$('#csImp'), impK=null, impCl='cherry', fresh=[];
  function freshKey(k){for(var i=0;i<fresh.length;i++){if(fresh[i].tail===k.tail&&fresh[i].name===k.name)return fresh[i].key}return null}
  function impModel(k){var id=((k&&k.models)||[])[0];return byId[id]?byId[id].name:(byId['glm-5-3-flash']||M[0]).name}
  function impSync(){var c=CLIENTS[impCl],full=impK&&impK.full;
    $$('#csImpTabs [data-cl]').forEach(function(b){var on=b.getAttribute('data-cl')===impCl;b.classList.toggle('on',on);b.setAttribute('aria-selected',String(on));b.tabIndex=on?0:-1});
    $('#csImpStep').textContent=c.step; $('#csImpUrl').textContent=c.url; $('#csImpKey').textContent=full||('sk-…'+(impK?impK.tail:''));
    $('[data-impcp="Key"]').disabled=!full; $('#csImpKh').hidden=!!full; $('#csImpM').textContent=impModel(impK)}
  function openImp(k,full){impK={name:k.name,tail:k.tail,models:k.models,full:full||null};impCl='cherry';$('#csImpFor').textContent=k.name;impSync();
    if(imp.showModal){if(!imp.open)imp.showModal()}else{imp.setAttribute('open','')} $('#csImpTabs .on').focus()}
  function closeImp(){if(imp.close){if(imp.open)imp.close()}else{imp.removeAttribute('open')}}
  $$('#csImpTabs [data-cl]').forEach(function(b){b.addEventListener('click',function(){impCl=b.getAttribute('data-cl');impSync()})});
  $('#csImpTabs').addEventListener('keydown',function(e){if(['ArrowLeft','ArrowRight'].indexOf(e.key)<0)return;e.preventDefault();var ks=Object.keys(CLIENTS),i=ks.indexOf(impCl);impCl=ks[(i+(e.key==='ArrowLeft'?-1:1)+ks.length)%ks.length];impSync();$('#csImpTabs .on').focus()});
  $$('[data-impcp]').forEach(function(b){b.addEventListener('click',function(){if(b.disabled)return;copyText($('#csImp'+b.getAttribute('data-impcp')).textContent,function(){toast('已复制')})})});
  $('#csImpX').addEventListener('click',closeImp); $('#csImpOk').addEventListener('click',closeImp);
  imp.addEventListener('click',function(e){if(e.target===imp)closeImp()});
  $('#csImpF').addEventListener('submit',function(e){e.preventDefault();closeImp()});
  $('#csImpDoc').addEventListener('click',function(e){e.preventDefault();closeImp();location.hash='#docs';setTimeout(function(){var b=$('#docIdx [data-doc="clients"]');if(b)b.click()},40)});

  /* 使用日志：按模型的每日消费（近 7 / 30 天）。只读 LOGS，颜色跟随模型在目录 M 中的顺序；没有记录时显示空状态 */
  var TCOL=['#2F63B8','#D9693A','#7A5BC2','#1E9C86','#D9A21B','#C2577E','#6B8E23'], TOTH='#A3A3A3', trN=7;
  function p2(n){return ('0'+n).slice(-2)}
  function dk(d){return d.getFullYear()+'-'+p2(d.getMonth()+1)+'-'+p2(d.getDate())}
  function mIdx(name){for(var i=0;i<M.length;i++){if(M[i].name===name)return i}return -1}
  function niceMax(x){var e=Math.pow(10,Math.floor(Math.log(x)/Math.LN10)),f=x/e,st=[1,1.2,1.5,2,2.5,3,4,5,6,8,10];for(var i=0;i<st.length;i++){if(f<=st[i])return st[i]*e}return 10*e}
  function renderTrend(){var d0=new Date();d0.setHours(0,0,0,0);d0.setDate(d0.getDate()-(trN-1));var days=[],at={},ser={};
    for(var i=0;i<trN;i++){var d=new Date(d0);d.setDate(d0.getDate()+i);at[dk(d)]=days.length;days.push({k:dk(d),v:{},s:0})}
    LOGS.forEach(function(r){var k=dk(new Date(r.t));if(at[k]==null)return;var j=mIdx(r.model),nm=j>=0&&j<TCOL.length?r.model:'其他',c=+r.cost||0,b=days[at[k]];b.v[nm]=(b.v[nm]||0)+c;b.s+=c;if(c>0)ser[nm]=1});
    var names=Object.keys(ser).sort(function(a,b){var x=mIdx(a),y=mIdx(b);return (x<0?99:x)-(y<0?99:y)}),top=Math.max.apply(null,days.map(function(b){return b.s})),has=names.length>0&&top>0;
    $('#csTr').hidden=!has; $('#csTr0').hidden=has; $('#csTrTip').hidden=true;
    $('#csTr0').innerHTML=LOGS.length?'<b>所选时间内没有消费</b><span>换一个时间范围，或发出请求后再来看。</span>':'<b>还没有消费记录</b><span>发出请求后，这里按天显示每个模型的消费。</span>';
    if(!has)return;
    var mx=niceMax(top),col=function(n){return n==='其他'?TOTH:TCOL[mIdx(n)]},cols='repeat('+trN+',minmax(0,1fr))',bars=$('#csTrB'),x=$('#csTrX');
    $('#csTrG').innerHTML=[1,.5,0].map(function(f){return '<span style="bottom:'+(f*100)+'%"><em>'+cny(mx*f)+'</em></span>'}).join('');
    bars.className='cs-trbars'+(trN>7?' n30':''); bars.style.gridTemplateColumns=cols; x.className='cs-trx'+(trN>7?' n30':''); x.style.gridTemplateColumns=cols;
    bars.innerHTML=days.map(function(b,i){return '<div class="cs-trc" tabindex="0" role="img" data-i="'+i+'" aria-label="'+b.k+' · '+cny(b.s)+'">'+names.filter(function(n){return b.v[n]>0}).map(function(n){return '<i style="height:'+(b.v[n]/mx*100).toFixed(2)+'%;background:'+col(n)+'"></i>'}).join('')+'</div>'}).join('');
    x.innerHTML=days.map(function(b,i){return '<span>'+(trN<=7||(trN-1-i)%5===0?b.k.slice(5):'')+'</span>'}).join('');
    $('#csTrL').innerHTML=names.map(function(n){return '<li><i style="background:'+col(n)+'"></i>'+esc(n)+'</li>'}).join('');
    $$('.cs-trc',bars).forEach(function(c){
      function show(){var b=days[+c.getAttribute('data-i')],t=$('#csTrTip'),wr=$('#csTr').getBoundingClientRect(),r=c.getBoundingClientRect();
        t.innerHTML='<span class="mono">'+b.k+'</span>'+names.filter(function(n){return b.v[n]>0}).map(function(n){return '<div><i style="background:'+col(n)+'"></i><span>'+esc(n)+'</span><span>'+cny(b.v[n])+'</span></div>'}).join('')+'<div class="cs-trsum"><span>合计</span><span>'+cny(b.s)+'</span></div>';
        t.hidden=false;var tw=t.offsetWidth,l=r.right-wr.left+10;if(l+tw>wr.width-8)l=r.left-wr.left-tw-10;t.style.left=Math.max(8,l)+'px'}
      function hide(){$('#csTrTip').hidden=true}
      c.addEventListener('mouseenter',show);c.addEventListener('focus',show);c.addEventListener('mouseleave',hide);c.addEventListener('blur',hide)})}
  $$('#csTrSeg [data-td]').forEach(function(b){b.addEventListener('click',function(){trN=+b.getAttribute('data-td');$$('#csTrSeg [data-td]').forEach(function(x){var on=x===b;x.classList.toggle('on',on);x.setAttribute('aria-pressed',String(on))});renderTrend()})});

  /* 成员列表：本人（管理员）在最前，其后是邀请的同事 */
  function renderMembers(){var you='<li><span class="cs-mm"><span>'+esc(me.email||'')+'</span><span class="cs-you">你</span></span><span>管理员</span><span class="cs-st ok">已加入</span><span></span></li>';
    $('#csSubs').innerHTML=you+(me.subs||[]).map(function(s,i){var r=s.role==='admin'?'admin':'member';
      return '<li><span class="cs-mm"><span>'+esc(s.email)+'</span><span class="cs-sub mono">'+esc(s.at||'')+'</span></span><select class="mk-sel" data-role="'+i+'" aria-label="角色"><option value="member"'+(r==='member'?' selected':'')+'>成员</option><option value="admin"'+(r==='admin'?' selected':'')+'>管理员</option></select><span class="cs-st wait">待加入</span><button class="ac-link" type="button" data-rm="'+i+'">移除</button></li>'}).join('');
    $$('#csSubs [data-role]').forEach(function(sel){sel.addEventListener('change',function(){me.subs[+sel.getAttribute('data-role')].role=sel.value;persist();toast('已更新角色。')})});
    $$('#csSubs [data-rm]').forEach(function(b){b.addEventListener('click',function(){if(!b._armed){b._armed=1;b.textContent='确认移除';return}me.subs.splice(+b.getAttribute('data-rm'),1);persist();renderConsole();toast('已移除成员。')})})}

  /* 余额与可用时长：可用时长 = 余额 ÷ 近 24 小时消费；没有消费时显示 -- */
  function runway(){var s=Date.now()-864e5,d=LOGS.reduce(function(a,r){return r.t>=s?a+(+r.cost||0):a},0);if(!(d>0))return '--';var x=BALANCE/d;
    if(x>=1)return (x<10?x.toFixed(1):String(Math.floor(x)))+' <span>天</span>';var h=x*24;return h<1?'<span>不足 1 小时</span>':Math.floor(h)+' <span>小时</span>'}
  function nItem(n){return '<li><span class="mono">'+esc(dk(new Date(n.t)))+'</span><b>'+esc(n.title||'')+'</b>'+(n.body?'<p>'+esc(n.body)+'</p>':'')+'</li>'}
  function byT(a,b){return new Date(b.t)-new Date(a.t)}
  function platRender(){if(!me)return;var spent=LOGS.reduce(function(a,r){return a+(+r.cost||0)},0),rw=runway();
    ['#btBal','#btCredBal','#csBal'].forEach(function(id){$(id).textContent=cny(BALANCE)}); $('#btCredRun').innerHTML=rw; $('#csRun').innerHTML=rw;
    $('#csSpent').textContent=cny(spent); $('#csReqs').textContent=LOGS.length.toLocaleString('en-US');
    $('#csTopups').innerHTML=TOPUPS.map(function(r){return '<tr><td class="mono">'+stamp(r.t)+'</td><td class="mono">'+esc(r.no||'')+'</td><td>'+esc(r.via||'')+'</td><td class="mono r">'+cny(r.amount||0)+'</td><td>'+esc(r.st||'')+'</td></tr>'}).join(''); $('#csTopups0').hidden=TOPUPS.length>0;
    var st={key:me.keys.length>0,topup:TOPUPS.length>0||BALANCE>0,req:LOGS.length>0},done=0;
    $$('#btCheck [data-ck]').forEach(function(li){var on=!!st[li.getAttribute('data-ck')],s=$('.cs-st',li);if(on)done++;li.classList.toggle('done',on);s.className='cs-st'+(on?' ok':'');s.textContent=on?'已完成':'未完成'});
    $('#btProg').textContent=done+' / 3';
    var ann=NOTICES.slice().sort(byT); $('#btAnn').innerHTML=ann.map(nItem).join(''); $('#btAnn').hidden=!ann.length; $('#btAnn0').hidden=!!ann.length;
    $('#btFaq').innerHTML=FAQS.map(function(f){return '<details><summary>'+esc(f.q)+'</summary><p>'+esc(f.a)+'</p></details>'}).join(''); $('#btFaq').hidden=!FAQS.length; $('#btFaq0').hidden=!!FAQS.length;
    var all=ALERTS.concat(NOTICES).sort(byT); $('#btNtfL').innerHTML=all.map(nItem).join(''); $('#btNtfL').hidden=!all.length; $('#btNtf0').hidden=!!all.length; $('#btBellDot').hidden=!all.length}

  /* 安全与访问：第三方账号绑定（微信） */
  $('#csWx').addEventListener('click',function(){toast('微信绑定接入后即可使用。')});

"""
edit('  /* 定价页：模型价格来自同一份模型目录 */\n', NEWJS, 'before')

edit("  function closePops(){['#btOrgPop','#btCredPop'].forEach(function(id){$(id).hidden=true});$('#btOrgB').setAttribute('aria-expanded','false');$('#btCredB').setAttribute('aria-expanded','false')}",
     "  function closePops(){['#btOrgPop','#btCredPop','#btNtfPop'].forEach(function(id){$(id).hidden=true});['#btOrgB','#btCredB','#btBell'].forEach(function(id){$(id).setAttribute('aria-expanded','false')})}")
edit("  document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!(($('#btOrgPop').hidden)&&($('#btCredPop').hidden))){closePops();$('#btOrgB').focus()}});",
     "  $('#btBell').addEventListener('click',function(e){e.stopPropagation();openPop(this,'#btNtfPop')});\n"
     "  document.addEventListener('keydown',function(e){if(e.key!=='Escape')return;var o=[['#btOrgPop','#btOrgB'],['#btCredPop','#btCredB'],['#btNtfPop','#btBell']].filter(function(x){return !$(x[0]).hidden})[0];if(o){closePops();$(o[1]).focus()}});")

# ───────────────────────── 英文 ─────────────────────────
EN = {
  # 通知铃
  "通知": "Notifications", "余额预警与公告": "Balance alerts and announcements", "还没有通知": "No notifications yet",
  "余额预警和平台公告会显示在这里。": "Balance alerts and platform announcements will appear here.", "设置余额预警": "Set a balance alert",
  # 开始使用清单
  "开始使用": "Get started", "已创建 Key": "API key created", "按项目创建 API Key，完整 Key 只在创建时显示一次。": "Create an API key per project. The full key is shown only once, when it's created.",
  "已充值": "Balance topped up", "已发出首个请求": "First request sent", "用 Key 调用任一模型，请求会出现在使用日志里。": "Call any model with your key; the request will show up in your usage logs.",
  "未完成": "Not done yet",
  # 公告与常见问答
  "公告": "Announcements", "还没有公告": "No announcements yet", "平台发布的维护和服务公告会显示在这里。": "Maintenance and service announcements from the platform will appear here.",
  "常见问答": "FAQ", "还没有常见问答": "No FAQ entries yet", "平台整理的常见问题会显示在这里。": "Common questions collected by the platform will appear here.",
  # 可用时长
  "可用时长": "Est. time left", "按余额和近 24 小时消费估算。": "Estimated from your balance and spend over the last 24 hours.", "按近 24 小时消费估算": "Based on the last 24 hours of spend",
  "天": "days", "小时": "hours", "不足 1 小时": "Under 1 hour",
  # 创建 Key
  "导入客户端": "Import to client", "复制并保存这些 Key，关闭后无法再次查看。": "Copy and save these keys. You won't be able to see them again.",
  "平台开放其他分组后可在这里选择。": "Other groups can be selected here once the platform offers them.", "批量创建": "Batch create",
  "一次创建 1–20 个 Key，名称后自动加序号。": "Create 1–20 keys at once; a number is added to each name.", "无限额度": "Unlimited",
  "已开启无限额度。关闭后填写额度上限。": "Unlimited is on. Turn it off to set a spend limit.", "这个 Key 的累计消费达到上限后停止调用。": "Calls stop once this key's total spend reaches the limit.",
  "批量创建数量请填写 1 到 20 之间的整数。": "For batch create, enter a whole number from 1 to 20.",
  # 导入客户端对话框
  "客户端": "Clients", "接口地址": "Base URL", "模型名称": "Model name", "完成": "Done",
  "完整 Key 只在创建时显示一次，请粘贴你保存的 Key。": "The full key is shown only once, when it's created. Paste the key you saved.",
  "将 YOUR_API_HOST 替换为平台提供的 HTTPS 接入域名。各客户端的菜单名称会随版本变化，以客户端当前版本为准。": "Replace YOUR_API_HOST with the HTTPS endpoint provided by the platform. Menu names vary between client versions; follow the version you have.",
  "设置 → 模型服务 → 添加，提供商类型选 OpenAI。API 地址不用带 /v1，Cherry Studio 会自动补全。": "Settings → Model Provider → Add, with provider type OpenAI. Leave /v1 off the API address; Cherry Studio adds it.",
  "新增自定义供应商，按要切换的工具选择接口格式，填入请求地址和 API Key，保存后切换到这个供应商。": "Add a custom provider, choose the API format for the tool you're switching, enter the request URL and API key, save, then switch to this provider.",
  "设置 → AI 服务商 → OpenAI，填入 API Key 和 API 代理地址，再获取模型列表或手动添加模型。": "Settings → AI Providers → OpenAI. Enter the API key and API proxy URL, then fetch the model list or add models by hand.",
  "设置 → 模型服务商 → 添加自定义服务商，类型选 OpenAI，填入 API URL 和 API Key，再拉取或添加模型。": "Settings → Model Providers → Add custom provider, type OpenAI. Enter the API URL and API key, then fetch or add models.",
  # 消费趋势
  "消费趋势": "Spend trend", "消费趋势时间范围": "Spend trend time range", "还没有消费记录": "No spend yet",
  "发出请求后，这里按天显示每个模型的消费。": "After you send requests, daily spend by model appears here.", "所选时间内没有消费": "No spend in this period",
  "换一个时间范围，或发出请求后再来看。": "Try another time range, or check back after sending requests.", "其他": "Other",
  # 成员与角色
  "成员与角色": "Members & roles", "邀请同事加入企业账户，额度和账单由企业账户统一管理。管理员可以管理成员、API Key 和账单；成员可以创建和使用自己的 API Key。": "Invite colleagues to the company account; credit and billing are managed centrally. Admins manage members, API keys and billing; members create and use their own API keys.",
  "角色": "Role", "成员": "Member", "管理员": "Admin", "你": "You", "已加入": "Joined", "待加入": "Pending", "移除": "Remove", "确认移除": "Confirm removal",
  "这个邮箱已在成员列表中。": "This email is already on the member list.", "已加入成员列表。邀请邮件接入后即可发送。": "Added to the member list. Invitation emails will be sent once that's connected.",
  "已更新角色。": "Role updated.", "已移除成员。": "Member removed.",
  # 第三方账号绑定
  "第三方账号绑定": "Linked accounts", "绑定后可以用第三方账号登录。": "Link an account to sign in with it.", "微信账号：未绑定": "WeChat: not linked",
  "绑定微信": "Link WeChat", "微信绑定接入后即可使用。": "WeChat linking will be available once connected.",
  # 文档：接入客户端
  "在控制台的 API Key 列表里点「导入客户端」，可以逐项复制接入地址、API Key 和模型名称。": "In the console's API key list, click “Import to client” to copy the endpoint, API key and model name one at a time.",
  "桌面与网页客户端": "Desktop and web clients",
  "在服务商设置里添加自定义服务商，类型选 OpenAI 兼容，API 地址填": "In provider settings, add a custom provider of type OpenAI-compatible and set the API URL to",
  "，再填 API Key 和模型名称。": ", then enter the API key and model name.",
  "编程工具": "Coding tools",
  "编程工具要求平台开启对应接口：Claude Code 使用 Anthropic Messages 格式（": "Coding tools need the matching interface enabled on the platform: Claude Code uses the Anthropic Messages format (",
  "），Codex CLI 使用 OpenAI Responses 格式（": "), and Codex CLI uses the OpenAI Responses format (",
  "）。使用前请确认平台已为你要用的模型开启这些接口。": "). Before you start, confirm these interfaces are enabled for the models you plan to use.",
  "用三个环境变量设置接入地址（不带 /v1）、API Key 和模型名称，然后在同一个终端运行 claude。": "Set three environment variables for the endpoint (without /v1), API key and model name, then run claude in the same terminal.",
  "编辑": "Edit",
  "，新增一个服务商：base_url 填接入地址，env_key 填保存 API Key 的环境变量名，model 填模型名称。设置好环境变量后，在终端运行 codex。": " and add a provider: set base_url to the endpoint, env_key to the name of the environment variable that holds your API key, and model to the model name. Set that variable, then run codex in your terminal.",
  "聊天机器人框架": "Chatbot frameworks",
  "在管理面板添加模型，供应商选 OpenAI 兼容，Base URL 填": "In the admin panel, add a model with an OpenAI-compatible provider and set the Base URL to",
  "在管理面板的服务提供商里新增一项，类型选 OpenAI，API Base URL 填": "In the admin panel, add a service provider of type OpenAI and set the API Base URL to",
  "翻译工具": "Translation tools", "Fluent Read（流畅阅读）": "Fluent Read",
  "在插件设置里把翻译服务设为自定义 OpenAI 兼容接口，接口地址填完整的": "In the extension settings, set the translation service to a custom OpenAI-compatible API and set the API URL to the full",
  "翻译设置里添加大模型通用接口，API 接口地址填": "In translation settings, add a general LLM API and set the API URL to",
  # 文档：模型与计费
  "缓存计费": "Cache billing",
  "部分模型支持输入缓存：请求开头与近期请求相同的输入内容可以命中缓存，命中部分按缓存价计费，其余输入按普通输入价计费。是否支持缓存、缓存价是多少，取决于平台为该模型开启的配置，以模型详情和控制台为准。": "Some models support input caching: when the start of a request repeats input from recent requests, that part can hit the cache and is billed at the cache rate, while the rest is billed at the normal input rate. Whether a model supports caching, and its cache rate, depend on how the platform has configured that model; see the model details and the console.",
  "推理强度后缀": "Reasoning-effort suffixes",
  "支持推理强度的模型，可以在模型名称后加后缀指定推理强度，相当于把请求的推理强度（reasoning_effort）设为对应档位。推理强度越高，模型用于思考的 Token 通常越多，费用和耗时也会增加。哪些模型可以加后缀，取决于平台为该模型开启的配置。": "For models that support reasoning effort, add a suffix to the model name to set it; this is the same as setting the request's reasoning effort (reasoning_effort) to that level. Higher effort usually means more thinking tokens, so cost and latency go up. Which models accept these suffixes depends on how the platform has configured each model.",
  "后缀": "Suffix", "推理强度": "Reasoning effort", "高": "High", "中": "Medium", "低": "Low",
  # 控制台外框里原本没有英文的读屏标签（EN 审计要求为 0）
  "控制台导航": "Console navigation", "返回沐仞官网": "Back to the FathomPeak website", "收起侧栏": "Collapse sidebar", "展开侧栏": "Expand sidebar",
  "按名称查找 API Key": "Find an API key by name", "按类型和厂商筛选": "Filter by type and vendor", "账户摘要": "Account summary",
  "暂停背景光影": "Pause background light", "播放背景光影": "Play background light",
}
import json
EN_JS = "  /* 2026-10-14 原平台功能补齐：通知铃、开始使用清单、可用时长、公告与常见问答、消费趋势、导入客户端、批量创建、成员与角色、第三方绑定、文档客户端与计费 */\n  Object.assign(I18N," + json.dumps(EN, ensure_ascii=False) + ");\n"
edit("  var lang='zh'; try{lang=localStorage.getItem('fp-lang')||'zh'}catch(e){}\n", EN_JS, 'before')

# 英文切换：按钮在运行中改 aria-label / title（侧栏收起、背景光影暂停）后也要翻译；属性里出现新的中文时以它为准，不用旧缓存
edit("var key='__zh_'+at, src=el[key]!=null?el[key]:el.getAttribute(at); if(!src) return;",
     "var key='__zh_'+at, cur=el.getAttribute(at), src=el[key]!=null&&!CJK.test(cur||'')?el[key]:cur; if(!src) return;")
edit("observe(document.body,{childList:true,subtree:true});\n",
     "  new MutationObserver(function(ms){ if(lang!=='en') return; for(var i=0;i<ms.length;i++){ var v=ms[i].target.getAttribute(ms[i].attributeName); if(v&&CJK.test(v)){ clearTimeout(__lt); __lt=setTimeout(applyLang,16); return } } }).observe(document.body,{subtree:true,attributes:true,attributeFilter:['aria-label','title','placeholder']});\n", 'after')

# ───────────────────────── 应用 ─────────────────────────
for anchor, new, mode in EDITS:
    n = s.count(anchor)
    if n != 1:
        sys.exit(f'anchor hit {n}x (need 1): {anchor[:90]!r}')
    if mode == 'replace': s = s.replace(anchor, new)
    elif mode == 'after': s = s.replace(anchor, anchor + new)
    elif mode == 'before': s = s.replace(anchor, new + anchor)
    elif mode == 'before_nl': s = s.replace(anchor, '\n' + new.rstrip('\n') + anchor)
p.write_text(s, encoding='utf-8')
print(f'ok: {len(EDITS)} edits, {len(EN)} English strings -> {p}')
