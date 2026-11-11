"""Verify gap items 6–8: every route at 1440 / 390, zh + en, no JS errors, no horizontal overflow,
plus interaction checks for model search / vendor / sort, nav sign-up, enterprise path, console sample.
usage: python3 verify_678.py <base-url> <port>"""
import json, time, subprocess, urllib.request, importlib.util, sys
spec = importlib.util.spec_from_file_location('cdp', '/Users/zixin/programs/ai-skills/reference-site-prototype/scripts/cdp_client.py')
cdp = importlib.util.module_from_spec(spec); spec.loader.exec_module(cdp)
BASE = sys.argv[1]; port = int(sys.argv[2]) if len(sys.argv) > 2 else 9561
prof = '/private/tmp/claude-501/-Users-zixin-Desktop-----/bcfbcc8d-ce9d-43dd-bfb3-9d5e9f552e35/scratchpad/chrome-prof-%d' % port
subprocess.run(['rm', '-rf', prof])
pr = subprocess.Popen([cdp.CHROME, '--headless=new', f'--remote-debugging-port={port}', f'--user-data-dir={prof}', '--hide-scrollbars', 'about:blank'],
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
ROUTES = ['home', 'models', 'model-glm-5-3', 'pricing', 'edu', 'enterprise', 'network', 'about', 'news', 'newsletter', 'changelog',
          'docs', 'guides', 'guide-dev-switch', 'compliance', 'privacy', 'terms', 'start', 'login', 'console']
ERR_HOOK = "window.__errs=[];addEventListener('error',function(e){__errs.push(String(e.message||e))});addEventListener('unhandledrejection',function(e){__errs.push('rej '+String(e.reason))});"
CJK_JS = r'''(function(){var out=[],w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT),n;
 while((n=w.nextNode())){var p=n.parentElement;if(!p||/SCRIPT|STYLE/.test(p.nodeName)||p.closest('.lang'))continue;if(!/[一-鿿]/.test(n.nodeValue))continue;
  var sec=p.closest('[data-route]');if(sec&&!sec.classList.contains('on'))continue;var r=p.getBoundingClientRect(),cs=getComputedStyle(p);
  if(!(r.width>0&&r.height>0)||cs.visibility==='hidden'||p.closest('[hidden]'))continue;out.push(n.nodeValue.trim().slice(0,80))}
 document.querySelectorAll('[placeholder],[aria-label],[title]').forEach(function(el){var sec=el.closest('[data-route]');if(sec&&!sec.classList.contains('on'))return;
  ['placeholder','aria-label','title'].forEach(function(a){var v=el.getAttribute(a);if(v&&/[一-鿿]/.test(v))out.push('@'+a+': '+v)})});
 document.querySelectorAll('option').forEach(function(o){var sec=o.closest('[data-route]');if(sec&&sec.classList.contains('on')&&/[一-鿿]/.test(o.textContent))out.push('option: '+o.textContent)});
 return out})()'''
OVF_JS = r'''(function(){var W=document.documentElement.clientWidth,sw=document.documentElement.scrollWidth,bad=[];
 if(sw>W+1){document.querySelectorAll('body *').forEach(function(el){var r=el.getBoundingClientRect();if(r.width&&r.right>W+1&&getComputedStyle(el).position!=='fixed'){var sec=el.closest('[data-route]');if(sec&&!sec.classList.contains('on'))return;bad.push((el.id?'#'+el.id:el.tagName.toLowerCase()+'.'+String(el.className).split(' ')[0])+' r='+Math.round(r.right))}})}
 return {W:W,sw:sw,bad:bad.slice(0,6)}})()'''
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
        if 'exceptionDetails' in r: return {'__exc': r['exceptionDetails'].get('text')}
        return r['result'].get('value')
    def go(h, wait=1.0):
        ev(f"location.hash='#{h}'"); time.sleep(wait); ev("document.querySelectorAll('.rv').forEach(function(e){e.classList.add('shown')})"); time.sleep(.3)
    for (w, h, mobile) in [(1440, 900, False), (390, 844, True)]:
        ws.send('Emulation.setDeviceMetricsOverride', {'width': w, 'height': h, 'deviceScaleFactor': 1, 'mobile': mobile})
        for lang in ['zh', 'en']:
            print(f'\n===== {w}px  lang={lang}')
            ws.send('Page.navigate', {'url': BASE + '#home'}); time.sleep(3)
            ev(f"localStorage.clear();localStorage.setItem('fp-lang','{lang}');sessionStorage.setItem('fp-fresh','1')"); ws.send('Page.reload'); time.sleep(4)
            for r in ROUTES:
                if r == 'console':  # log in a personal account first
                    go('start'); ev("var f=document.getElementById('acSignup');f.email.value='verify@example.com';f.pw.value='verify-pass-1';f.agree.checked=true;f.requestSubmit()"); time.sleep(1)
                go(r)
                o = ev(OVF_JS); e = ev('window.__errs')
                on = ev("(document.querySelector('[data-route].on')||{}).getAttribute&&document.querySelector('[data-route].on').getAttribute('data-route')")
                line = f'{r:18s} on={on:12s} sw={o["sw"]}/{o["W"]} errs={len(e)}'
                if lang == 'en': cj = ev(CJK_JS); line += f' cjk={len(cj)}'
                check(o['sw'] <= o['W'] + 1 and not e and (lang == 'zh' or not cj), line + ('' if o['sw'] <= o['W'] + 1 else ' OVF ' + str(o['bad'])) + ('' if not e else ' ERR ' + str(e)) + ('' if lang == 'zh' or not cj else ' CJK ' + str(cj[:6])))
            # ---- interactions ----
            ev("localStorage.removeItem('fp-session-v2')"); ws.send('Page.reload'); time.sleep(4)
            go('models')
            rows = lambda: ev("Array.prototype.map.call(document.querySelectorAll('#allModels .row .n'),function(n){return n.firstChild.nodeValue.trim()})")
            cards = lambda: ev("document.querySelectorAll('#featured .mcard').length")
            check(len(rows()) == 7 and cards() == 7, f'models: 7 rows/cards initially ({len(rows())}/{cards()})')
            ev("var q=document.getElementById('mkQ');q.value='glm';q.dispatchEvent(new Event('input'))"); time.sleep(.3)
            check(rows() == ['GLM-5.3-Flash', 'GLM-5.3'], f'search "glm" -> {rows()}')
            ev("var q=document.getElementById('mkQ');q.value='智谱';q.dispatchEvent(new Event('input'))"); time.sleep(.3)
            check(rows() == ['GLM-5.3-Flash', 'GLM-5.3'], f'search "智谱" -> {rows()}')
            ev("var q=document.getElementById('mkQ');q.value='deepseek v4';q.dispatchEvent(new Event('input'))"); time.sleep(.3)
            check(len(rows()) == 2, f'search "deepseek v4" -> {rows()}')
            ev("var q=document.getElementById('mkQ');q.value='';q.dispatchEvent(new Event('input'))"); time.sleep(.3)
            opts = ev("Array.prototype.map.call(document.querySelectorAll('#mkVendor option'),function(o){return o.value})")
            check(opts == ['all', 'DeepSeek', 'Alibaba', 'Zhipu', 'MiniMax'], f'vendor options {opts}')
            ev("var s=document.getElementById('mkVendor');s.value='MiniMax';s.dispatchEvent(new Event('change'))"); time.sleep(.3)
            check(rows() == ['MiniMax-M2.7', 'MiniMax-M3'], f'vendor MiniMax -> {rows()}')
            ev("document.querySelector('#chips [data-f=\"推理\"]').click()"); time.sleep(.3)
            r2 = rows(); print('    MiniMax + 推理 ->', r2)
            ev("document.querySelector('#chips [data-f=\"all\"]').click();var s=document.getElementById('mkVendor');s.value='all';s.dispatchEvent(new Event('change'))"); time.sleep(.3)
            ev("var s=document.getElementById('mkSort');s.value='asc';s.dispatchEvent(new Event('change'))"); time.sleep(.3)
            pr_ = ev("Array.prototype.map.call(document.querySelectorAll('#allModels .row > span:nth-child(4)'),function(n){return parseFloat(n.textContent.replace('¥',''))})")
            check(pr_ == sorted(pr_) and len(pr_) == 7, f'sort asc prices {pr_}')
            fc = ev("Array.prototype.map.call(document.querySelectorAll('#featured .mcard .p'),function(n){return parseFloat(n.textContent.replace('¥',''))})")
            check(fc == sorted(fc), f'cards sorted asc {fc}')
            ev("document.getElementById('mkSortH').click()"); time.sleep(.3)
            pr_ = ev("Array.prototype.map.call(document.querySelectorAll('#allModels .row > span:nth-child(4)'),function(n){return parseFloat(n.textContent.replace('¥',''))})")
            check(pr_ == sorted(pr_, reverse=True) and ev("document.getElementById('mkSort').value") == 'desc', f'header click -> desc {pr_}')
            ev("document.getElementById('mkSortH').click()"); time.sleep(.3)
            check(ev("document.getElementById('mkSort').value") == '' and rows()[0] == 'DeepSeek-V4-Flash', 'header click again -> default order')
            ev("var q=document.getElementById('mkQ');q.value='zzzz';q.dispatchEvent(new Event('input'))"); time.sleep(.4)
            empty = ev("(document.querySelector('#featured .mk-empty')||{}).textContent")
            check(bool(empty) and rows() == [], f'empty state: {empty}')
            if lang == 'en':
                cj = ev(CJK_JS); check(not cj, f'EN models after filtering: cjk={cj[:5]}')
            o = ev(OVF_JS); check(o['sw'] <= o['W'] + 1, f'models no overflow after filtering {o}')
            ev("document.querySelector('[data-mk-reset]').click()"); time.sleep(.3)
            check(len(rows()) == 7 and ev("document.getElementById('mkQ').value") == '', 'reset restores 7 rows')
            # ---- nav sign-up ----
            if not mobile:
                sg = ev("(function(){var a=document.querySelector('.pill .top nav a.signup');var r=a.getBoundingClientRect();return {t:a.textContent,h:a.getAttribute('href'),vis:r.width>0}})()")
                check(sg['vis'] and sg['h'] == '#start', f'pill nav sign-up {sg}')
                ev("document.querySelector('.pill .top nav a.signup').click()"); time.sleep(1)
                check(ev("location.hash") == '#start' and ev("document.querySelector('.pill .top nav a.signup').classList.contains('on')"), 'click sign-up -> #start, link marked on')
            else:
                ev("document.getElementById('plus').click()"); time.sleep(.6)
                sg = ev("(function(){var a=document.querySelector('.menu .btns a.signup');var r=a.getBoundingClientRect();return {t:a.textContent,vis:r.width>0&&r.bottom<=innerHeight}})()")
                check(sg['vis'], f'mobile menu sign-up visible {sg}')
                o = ev(OVF_JS); check(o['sw'] <= o['W'] + 1, f'menu open no overflow {o}')
                ev("document.querySelector('.menu .btns a.signup').click()"); time.sleep(1)
                check(ev("location.hash") == '#start' and not ev("document.getElementById('pill').classList.contains('open')"), 'mobile sign-up -> #start, menu closed')
            # ---- enterprise path on #start ----
            ev("document.querySelector('.ac-types [data-t=\"company\"]').click()"); time.sleep(.3)
            st = ev("""(function(){var f=document.getElementById('acSignup');var vis=function(el){return !!el&&el.getBoundingClientRect().height>0};
              return {co:vis(f.querySelector('.ac-co')),coText:f.querySelector('.ac-co p').textContent,email:vis(f.email),pw:vis(f.pw),agree:vis(f.querySelector('.ac-ok')),submit:vis(f.querySelector('button[type=submit]')),login:vis(f.querySelector('.ac-alt'))}})()""")
            check(st['co'] and not st['email'] and not st['pw'] and not st['agree'] and not st['submit'] and st['login'], f'enterprise: sales panel only {st}')
            if lang == 'en':
                cj = ev(CJK_JS); check(not cj, f'EN start/company: cjk={cj[:5]}')
            o = ev(OVF_JS); check(o['sw'] <= o['W'] + 1, f'start/company no overflow {o}')
            ev("document.querySelector('.ac-co a').click()"); time.sleep(1.4)
            pos = ev("(function(){var r=document.getElementById('enterprise-sales').getBoundingClientRect();return {hash:location.hash,top:Math.round(r.top)}})()")
            check(pos['hash'] == '#enterprise' and 0 <= pos['top'] < 400, f'contact sales -> enterprise sales form {pos}')
            go('start'); ev("document.querySelector('.ac-types [data-t=\"personal\"]').click()"); time.sleep(.3)
            st = ev("(function(){var f=document.getElementById('acSignup');return {co:f.querySelector('.ac-co').getBoundingClientRect().height>0,email:f.email.getBoundingClientRect().height>0}})()")
            check(not st['co'] and st['email'], f'personal: normal form back {st}')
            # ---- console sample + sign-up hidden when logged in ----
            ev("var f=document.getElementById('acSignup');f.email.value='verify2@example.com';f.pw.value='verify-pass-1';f.agree.checked=true;f.requestSubmit()"); time.sleep(1.2)
            code = ev("document.querySelector('.cs-code').innerText")
            check('YOUR_API_HOST' in code and 'api.fathompeak.cn' not in code and '$API_KEY' in code, 'console sample uses YOUR_API_HOST + $API_KEY')
            print('    ', code.replace('\n', ' | ')[:260])
            hid = ev("Array.prototype.every.call(document.querySelectorAll('.signup'),function(a){return a.hidden&&a.getBoundingClientRect().width===0})")
            check(hid, 'sign-up links hidden when logged in')
            if lang == 'en':
                cj = ev(CJK_JS); check(not cj, f'EN console overview: cjk={cj[:5]}')
            check(not ev('window.__errs'), f'no JS errors after interactions {ev("window.__errs")}')
finally:
    pr.terminate()
print('\nFAILS:', len(fails))
for f in fails: print(' -', f)
