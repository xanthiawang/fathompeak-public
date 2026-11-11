"""Verify the 2026-10-14 platform-parity additions (build_platform_features_2026-10-14.py):
notification bell, overview checklist / runway / announcements + FAQ, usage spend chart, API key import-to-client,
group + unlimited + batch create, members & roles, WeChat binding, docs clients + billing.
Every console pane and the two docs panes at 1440 / 390, zh + en: no JS errors, no horizontal overflow, no visible
Chinese in EN (text, placeholder / aria-label / title, <option>, toasts). The site keeps no browser session, so the
console is opened through #console-preview (in-memory account); no password is typed anywhere. Optional 4th arg 'fixture'
expects a local test copy whose LOGS / TOPUPS / BALANCE were filled and whose preview account is a company account; it
then also checks the chart, runway and the company-only members section.
usage: python3 verify_platform_features_2026-10-14.py <base-url> <port> [shots-dir] [fixture]"""
import base64, json, os, time, subprocess, urllib.request, importlib.util, sys, datetime
spec = importlib.util.spec_from_file_location('cdp', '/Users/zixin/programs/ai-skills/reference-site-prototype/scripts/cdp_client.py')
cdp = importlib.util.module_from_spec(spec); spec.loader.exec_module(cdp)
BASE = sys.argv[1]; port = int(sys.argv[2]) if len(sys.argv) > 2 else 9581
SHOTS = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] != '-' else None
FIXTURE = len(sys.argv) > 4 and sys.argv[4] == 'fixture'
if SHOTS: os.makedirs(SHOTS, exist_ok=True)
prof = os.path.join(os.environ.get('TMPDIR', '/tmp'), 'fp-verify-prof-%d' % port)
subprocess.run(['rm', '-rf', prof])
pr = subprocess.Popen([cdp.CHROME, '--headless=new', f'--remote-debugging-port={port}', f'--user-data-dir={prof}', '--hide-scrollbars', 'about:blank'],
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
PANES = ['home', 'models', 'orders', 'explore', 'acct', 'bill', 'keys', 'sec', 'usage']
TODAY = datetime.date.today().isoformat()
ERR_HOOK = "window.__errs=[];addEventListener('error',function(e){__errs.push(String(e.message||e))});addEventListener('unhandledrejection',function(e){__errs.push('rej '+String(e.reason))});"
CJK_JS = r'''(function(){var out=[],w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT),n;
 var live=function(el){var sec=el.closest('[data-route]');if(sec&&!sec.classList.contains('on'))return false;var d=el.closest('dialog');if(d&&!d.open)return false;return true};
 while((n=w.nextNode())){var p=n.parentElement;if(!p||/SCRIPT|STYLE/.test(p.nodeName)||p.closest('.lang'))continue;if(!/[一-鿿。，：；（）]/.test(n.nodeValue))continue;
  if(!live(p))continue;var r=p.getBoundingClientRect(),cs=getComputedStyle(p);
  if(!(r.width>0&&r.height>0)||cs.visibility==='hidden'||p.closest('[hidden]'))continue;out.push(n.nodeValue.trim().slice(0,80))}
 document.querySelectorAll('[placeholder],[aria-label],[title]').forEach(function(el){if(!live(el))return;
  ['placeholder','aria-label','title'].forEach(function(a){var v=el.getAttribute(a);if(v&&/[一-鿿]/.test(v))out.push('@'+a+': '+v)})});
 document.querySelectorAll('option').forEach(function(o){if(live(o)&&/[一-鿿]/.test(o.textContent))out.push('option: '+o.textContent)});
 return out})()'''
OVF_JS = r'''(function(){var W=document.documentElement.clientWidth,sw=document.documentElement.scrollWidth,bad=[];
 if(sw>W+1){document.querySelectorAll('body *').forEach(function(el){var r=el.getBoundingClientRect();if(r.width&&r.right>W+1&&getComputedStyle(el).position!=='fixed'){var sec=el.closest('[data-route]');if(sec&&!sec.classList.contains('on'))return;bad.push((el.id?'#'+el.id:el.tagName.toLowerCase()+'.'+String(el.className).split(' ')[0])+' r='+Math.round(r.right))}})}
 return {W:W,sw:sw,bad:bad.slice(0,6)}})()'''
CJK = lambda t: any('一' <= c <= '鿿' for c in (t or ''))
fails = []
def check(cond, msg):
    print(('  ok   ' if cond else '  FAIL ') + msg)
    if not cond: fails.append(msg)
try:
    for _ in range(50):
        try: urllib.request.urlopen(f'http://127.0.0.1:{port}/json/version', timeout=1); break
        except Exception: time.sleep(.2)
    tab = json.loads(urllib.request.urlopen(urllib.request.Request(f'http://127.0.0.1:{port}/json/new?about:blank', method='PUT')).read())
    ws = cdp.WS(tab['webSocketDebuggerUrl']); ws.send('Page.enable'); ws.send('Runtime.enable')
    ws.send('Page.addScriptToEvaluateOnNewDocument', {'source': ERR_HOOK})
    def ev(e):
        r = ws.send('Runtime.evaluate', {'expression': e, 'returnByValue': True, 'awaitPromise': True})['result']
        if 'exceptionDetails' in r: return {'__exc': r['exceptionDetails'].get('text'), 'desc': r.get('result', {}).get('description')}
        return r['result'].get('value')
    def shot(name, w):
        if not SHOTS: return
        h = ev('Math.min(document.documentElement.scrollHeight,7000)') or 900
        s = ws.send('Page.captureScreenshot', {'format': 'png', 'captureBeyondViewport': True, 'clip': {'x': 0, 'y': 0, 'width': w, 'height': h, 'scale': 1}})
        if 'result' in s: open(os.path.join(SHOTS, name + '.png'), 'wb').write(base64.b64decode(s['result']['data']))
    def pane(p):
        ev(f"document.querySelector('.cs-nav button[data-p=\"{p}\"]').click();window.scrollTo(0,0)"); time.sleep(.35)
    def state(label, lang):
        o = ev(OVF_JS); e = ev('window.__errs'); line = f'{label:30s} sw={o["sw"]}/{o["W"]} errs={len(e)}'
        cj = ev(CJK_JS) if lang == 'en' else []
        if lang == 'en': line += f' cjk={len(cj)}'
        check(o['sw'] <= o['W'] + 1 and not e and not cj, line + ('' if o['sw'] <= o['W'] + 1 else ' OVF ' + str(o['bad'])) + ('' if not e else ' ERR ' + str(e)) + ('' if not cj else ' CJK ' + str(cj[:8])))
    def toast(): time.sleep(.2); return ev("document.getElementById('toast').textContent")
    def tcheck(t, lang, what):
        check(bool(t) and (lang == 'zh' or not CJK(t)), f'{what} toast: {t}')
    def seed(lang, w):
        ws.send('Page.navigate', {'url': BASE + '#home'}); time.sleep(3)
        ev(f"localStorage.clear();localStorage.setItem('fp-lang','{lang}')")
        ws.send('Page.reload'); time.sleep(4)
        ev("location.hash='#console-preview'"); time.sleep(1.2)
        check(ev("document.querySelector('[data-route].on').getAttribute('data-route')") == 'console' and ev('location.hash') == '#console', f'{w}/{lang} #console-preview opens the console')
    for (w, h, mobile) in [(1440, 900, False), (390, 844, True)]:
        ws.send('Emulation.setDeviceMetricsOverride', {'width': w, 'height': h, 'deviceScaleFactor': 1, 'mobile': mobile})
        for lang in ['zh', 'en']:
            print(f'\n===== {w}px  lang={lang}  {"FIXTURE" if FIXTURE else ""}')
            seed(lang, w)
            if FIXTURE:
                pane('usage'); state('usage with fixture', lang); shot(f'{w}_{lang}_fx_usage', w)
                nb = ev("document.querySelectorAll('#csTrB .cs-trc').length"); seg = ev("document.querySelectorAll('#csTrB .cs-trc i').length")
                check(not ev("document.getElementById('csTr').hidden") and nb == 7 and seg > 0, f'chart drawn: 7 days, {seg} segments')
                lg = ev("Array.prototype.map.call(document.querySelectorAll('#csTrL li'),function(l){return l.textContent})"); print('    legend:', lg)
                ev("var c=document.querySelectorAll('#csTrB .cs-trc');c[c.length-1].dispatchEvent(new MouseEvent('mouseenter'))"); time.sleep(.2)
                tip = ev("document.getElementById('csTrTip').hidden?'':document.getElementById('csTrTip').innerText"); print('    tooltip:', tip.replace('\n', ' | '))
                check(bool(tip) and (lang == 'zh' or not CJK(tip)), 'tooltip on last day')
                tr = ev("(function(){var t=document.getElementById('csTrTip').getBoundingClientRect(),c=document.getElementById('csTr').getBoundingClientRect();return [Math.round(t.left-c.left),Math.round(c.right-t.right)]})()")
                check(tr[0] >= 0 and tr[1] >= 0, f'tooltip inside chart card {tr}')
                state('tooltip shown', lang); shot(f'{w}_{lang}_fx_tooltip', w)
                ev("document.querySelector('#csTrSeg [data-td=\"30\"]').click()"); time.sleep(.2)
                check(ev("document.querySelectorAll('#csTrB .cs-trc').length") == 30, '30-day view')
                lbl = ev("Array.prototype.filter.call(document.querySelectorAll('#csTrX span'),function(s){return s.textContent}).length"); check(lbl == 6, f'30-day labels every 5th ({lbl})')
                state('usage 30 days', lang); shot(f'{w}_{lang}_fx_usage30', w)
                pane('bill'); run = ev("document.getElementById('csRun').innerText"); print('    runway:', run, ev("document.getElementById('csBal').textContent"))
                check(run not in ('--', '') and (lang == 'zh' or not CJK(run)), f'runway computed: {run}')
                state('wallet with fixture', lang)
                pane('home'); prog = ev("document.getElementById('btProg').textContent"); check(prog == '2 / 3', f'checklist with topup+request: {prog}')
                ev("document.querySelector('#csTrSeg [data-td=\"7\"]').click()")
            for p in PANES:
                pane(p)
                check(ev(f"document.querySelector('.cs-p[data-p=\"{p}\"]').classList.contains('on')"), f'pane {p} shown')
                state(f'pane {p} (new account)', lang); shot(f'{w}_{lang}_{p}', w)
            # ---- overview: checklist + boards ----
            pane('home')
            if not FIXTURE: check(ev("document.getElementById('btProg').textContent") == '0 / 3' and ev("document.querySelectorAll('#btCheck li.done').length") == 0, 'checklist 0 / 3 for a new account')
            check(ev("!document.getElementById('btAnn0').hidden&&document.getElementById('btAnn').hidden&&!document.getElementById('btFaq0').hidden"), 'announcements + FAQ empty states')
            # ---- bell ----
            ev("document.getElementById('btBell').click()"); time.sleep(.2)
            check(ev("!document.getElementById('btNtfPop').hidden&&!document.getElementById('btNtf0').hidden&&document.getElementById('btBellDot').hidden"), 'bell popover opens with empty state, no dot')
            br = ev("(function(){var b=document.getElementById('btBell').getBoundingClientRect(),p=document.getElementById('btNtfPop').getBoundingClientRect();return [Math.round(b.right),Math.round(b.top),Math.round(p.left),Math.round(p.right)]})()")
            check(br[0] >= w - 60 and br[1] < 40 and br[2] >= 0 and br[3] <= w, f'bell top-right, popover in viewport {br}')
            state('bell popover', lang); shot(f'{w}_{lang}_bell', w)
            ev("document.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape'}))"); time.sleep(.1)
            check(ev("document.getElementById('btNtfPop').hidden&&document.activeElement.id==='btBell'"), 'Escape closes popover, focus back on bell')
            # bell vs. sidebar org button: no overlap
            ov = ev("(function(){var a=document.getElementById('btBell').getBoundingClientRect(),b=document.getElementById('btOrgB').getBoundingClientRect();return a.left<b.right&&b.left<a.right&&a.top<b.bottom&&b.top<a.bottom})()")
            check(not ov, 'bell does not overlap the account button')
            # ---- credit popover runway ----
            ev("document.getElementById('btCredB').click()"); time.sleep(.2)
            if not FIXTURE: check(ev("document.getElementById('btCredRun').textContent") == '--', 'credit popover runway "--" without spend')
            ev("document.body.click()"); time.sleep(.1)
            # ---- wallet tiles ----
            pane('bill')
            tiles = ev("Array.prototype.map.call(document.querySelectorAll('.cs-tiles.n4 b'),function(b){return b.textContent})")
            check(FIXTURE or tiles == ['¥0.00', '--', '¥0.00', '0'], f'wallet tiles {tiles}')
            # ---- usage chart empty ----
            if not FIXTURE:
                pane('usage')
                check(ev("document.getElementById('csTr').hidden&&!document.getElementById('csTr0').hidden&&document.querySelectorAll('#csTrB .cs-trc').length===0"), 'spend chart: empty state, nothing plotted')
                ev("document.querySelector('#csTrSeg [data-td=\"30\"]').click()"); time.sleep(.1)
                check(ev("document.querySelector('#csTrSeg [data-td=\"30\"]').getAttribute('aria-pressed')") == 'true' and ev("document.getElementById('csTr').hidden"), '30-day toggle, still empty')
            # ---- create dialog: group, unlimited, batch ----
            pane('keys'); ev("document.getElementById('csNew').click()"); time.sleep(.3)
            check(ev("var f=document.getElementById('csNewF');f.inf.checked&&f.quota.disabled&&f.cnt.value==='1'&&f.group.value==='default'"), 'dialog defaults: unlimited on, quota disabled, batch 1, group default')
            state('create dialog', lang); shot(f'{w}_{lang}_create', w)
            dr = ev("(function(){var r=document.querySelector('#csDlg').getBoundingClientRect();return [Math.round(r.left),Math.round(r.right),Math.round(r.bottom)]})()")
            check(dr[0] >= 0 and dr[1] <= w and dr[2] <= h, f'dialog inside viewport {dr}')
            ev("var f=document.getElementById('csNewF');f.kname.value='Proj';f.inf.click()"); time.sleep(.1)
            check(ev("!document.getElementById('csNewF').quota.disabled"), 'unlimited off enables quota')
            ev("document.getElementById('csNewF').requestSubmit()"); time.sleep(.1); m1 = ev("document.getElementById('csNewMsg').textContent")
            check(bool(m1) and ev("document.getElementById('csDlg').open"), f'quota required when not unlimited: {m1}')
            ev("var f=document.getElementById('csNewF');f.quota.value='50';f.cnt.value='21';f.dispatchEvent(new Event('input'));f.requestSubmit()"); time.sleep(.1); m2 = ev("document.getElementById('csNewMsg').textContent")
            check(bool(m2) and ev("document.getElementById('csKcnt').getAttribute('aria-invalid')") == 'true', f'batch 21 rejected: {m2}')
            if lang == 'en': check(not CJK(m1) and not CJK(m2), 'EN validation messages')
            ev("var f=document.getElementById('csNewF');f.cnt.value='3';f.requestSubmit()"); time.sleep(.5)
            lines = ev("document.getElementById('csKey').textContent.split('\\n')")
            check(not ev("document.getElementById('csDlg').open") and len(lines) == 3 and ev("document.querySelectorAll('#csKeys tr').length") == 3, f'batch 3 created, 3 keys revealed {[l[:12] for l in lines]}')
            row = ev("Array.prototype.map.call(document.querySelectorAll('#csKeys tr:first-child td'),function(t){return t.innerText.replace(/\\n/g,' | ')})"); print('    row:', row)
            check(row[0].startswith('Proj-1') and '¥50.00' in row[3], 'row: name with number, limit ¥50')
            state('keys after batch', lang); shot(f'{w}_{lang}_keys_batch', w)
            # ---- import dialog ----
            ev("document.querySelector('#csKeys [data-imp=\"1\"]').click()"); time.sleep(.3)
            check(ev("document.getElementById('csImp').open") and ev("document.getElementById('csImpKey').textContent").startswith('sk-') and len(ev("document.getElementById('csImpKey').textContent")) == 51 and not ev("document.querySelector('[data-impcp=\"Key\"]').disabled"), 'import: full key while the new key is still shown')
            check(ev("document.getElementById('csImpUrl').textContent") == 'https://YOUR_API_HOST', 'Cherry Studio base URL without /v1')
            state('import dialog (Cherry Studio)', lang); shot(f'{w}_{lang}_import', w)
            ir = ev("(function(){var r=document.querySelector('#csImp').getBoundingClientRect();return [Math.round(r.left),Math.round(r.right),Math.round(r.top),Math.round(r.bottom)]})()")
            check(ir[0] >= 0 and ir[1] <= w and ir[2] >= 0 and ir[3] <= h, f'import dialog inside viewport {ir}')
            urls = []
            for cl in ['ccswitch', 'lobe', 'deepchat']:
                ev(f"document.querySelector('#csImpTabs [data-cl=\"{cl}\"]').click()"); time.sleep(.1)
                urls.append(ev("document.getElementById('csImpUrl').textContent")); state(f'import tab {cl}', lang)
            check(urls == ['https://YOUR_API_HOST/v1'] * 3, f'other clients use /v1 {urls}')
            ev("document.querySelector('[data-impcp=\"Url\"]').click()"); tcheck(toast(), lang, 'copy URL')
            ev("document.getElementById('csImpOk').click()"); time.sleep(.2)
            check(not ev("document.getElementById('csImp').open"), 'import dialog closes')
            ev("document.getElementById('csSaved').click()"); time.sleep(.1)
            ev("document.querySelector('#csKeys [data-imp=\"0\"]').click()"); time.sleep(.3)
            kt = ev("document.getElementById('csImpKey').textContent")
            check(kt.startswith('sk-…') and len(kt) == 8 and ev("document.querySelector('[data-impcp=\"Key\"]').disabled") and not ev("document.getElementById('csImpKh').hidden"), f'after "saved": key masked {kt}, copy disabled, hint shown')
            state('import dialog masked', lang)
            ev("document.getElementById('csImpX').click()"); time.sleep(.2)
            # ---- checklist after key ----
            pane('home')
            check(ev("document.getElementById('btProg').textContent") == ('3 / 3' if FIXTURE else '1 / 3') and ev("document.querySelector('#btCheck [data-ck=\"key\"]').classList.contains('done')"), 'checklist 1 / 3 after creating keys')
            state('overview with keys', lang); shot(f'{w}_{lang}_home_keys', w)
            # ---- members ----
            pane('acct')
            if not FIXTURE:
                check(ev("document.querySelector('.cs-mem').hidden"), 'members section hidden for the personal preview account (company only)')
            else:
              check(ev("!document.querySelector('.cs-mem').hidden") and ev("document.querySelectorAll('#csSubs li').length") == 1, 'members: owner row only')
              ev("var f=document.getElementById('csInv');f.email.value='admin@example.com';f.mrole.value='admin';f.requestSubmit()"); t1 = toast()
              tcheck(t1, lang, 'invite')
              check(ev("document.querySelectorAll('#csSubs li').length") == 2 and ev("document.querySelector('#csSubs [data-role=\"0\"]').value") == 'admin', 'invited as admin')
              ev("var f=document.getElementById('csInv');f.email.value='admin@example.com';f.requestSubmit()"); t2 = toast()
              check(ev("document.querySelectorAll('#csSubs li').length") == 2, 'duplicate invite refused'); tcheck(t2, lang, 'duplicate')
              ev("var s=document.querySelector('#csSubs [data-role=\"0\"]');s.value='member';s.dispatchEvent(new Event('change'))"); t3 = toast()
              ev("var f=document.getElementById('csInv');f.email.value='dev@example.com';f.requestSubmit()"); time.sleep(.2)
              saved = ev("document.querySelector('#csSubs [data-role=\"0\"]').value"); check(saved == 'member' and ev("document.querySelectorAll('#csSubs li').length") == 3, f'role change kept after re-render ({saved})'); tcheck(t3, lang, 'role')
              state('members', lang); shot(f'{w}_{lang}_members', w)
              ev("document.querySelector('#csSubs [data-rm=\"0\"]').click()"); time.sleep(.1)
              check(ev("document.querySelectorAll('#csSubs li').length") == 3, 'remove needs confirmation')
              ev("document.querySelector('#csSubs [data-rm=\"0\"]').click()"); t4 = toast()
              check(ev("document.querySelectorAll('#csSubs li').length") == 2, 'removed after confirm'); tcheck(t4, lang, 'remove')
            # ---- security: WeChat ----
            pane('sec'); ev("document.getElementById('csWx').click()"); tcheck(toast(), lang, 'WeChat bind')
            check('未绑定' in ev("document.getElementById('csWx').closest('li').innerText") if lang == 'zh' else 'not linked' in ev("document.getElementById('csWx').closest('li').innerText"), 'WeChat shows not linked')
            # ---- docs ----
            for d in ['clients', 'models']:
                ev("location.hash='#docs'"); time.sleep(.8)
                ev(f"document.querySelector('#docIdx [data-doc=\"{d}\"]').click()"); time.sleep(.3)
                state(f'docs {d}', lang); shot(f'{w}_{lang}_docs_{d}', w)
            hs = ev("Array.prototype.map.call(document.querySelectorAll('.pane[data-doc=\"clients\"] h3'),function(h){return h.textContent})"); print('    clients:', hs)
            for name in ['AQBot', 'Claude Code', 'Codex CLI', 'LangBot', 'AstrBot', 'Luna Translator']:
                check(name in hs, f'docs lists {name}')
            check(any(x.startswith('Fluent Read') for x in hs), 'docs lists Fluent Read')
            check(not ev('window.__errs'), f'no JS errors {ev("window.__errs")}')
finally:
    pr.terminate()
print('\nFAILS:', len(fails))
for f in fails: print(' -', f)
