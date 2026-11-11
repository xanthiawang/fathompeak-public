"""Verify the console modules added 2026-10-14 (side-nav groups, API Key filters + create dialog, usage log,
wallet, profile notifications, security & access).
Every pane at 1440 / 390, zh + en: no JS errors, no horizontal overflow, no visible Chinese in EN
(text, placeholder / aria-label / title, <option>), plus interaction checks. The account session is seeded
through localStorage; no password is typed anywhere.
usage: python3 verify_console_modules_2026-10-14.py <base-url> <port> [shots-dir]"""
import base64, json, os, time, subprocess, urllib.request, importlib.util, sys, datetime
spec = importlib.util.spec_from_file_location('cdp', '/Users/zixin/programs/ai-skills/reference-site-prototype/scripts/cdp_client.py')
cdp = importlib.util.module_from_spec(spec); spec.loader.exec_module(cdp)
BASE = sys.argv[1]; port = int(sys.argv[2]) if len(sys.argv) > 2 else 9571
SHOTS = sys.argv[3] if len(sys.argv) > 3 else None
if SHOTS: os.makedirs(SHOTS, exist_ok=True)
prof = '/private/tmp/claude-501/-Users-zixin-Desktop-----/98f34898-246f-42df-9da9-7854d7cc4368/scratchpad/chrome-prof-%d' % port
subprocess.run(['rm', '-rf', prof])
pr = subprocess.Popen([cdp.CHROME, '--headless=new', f'--remote-debugging-port={port}', f'--user-data-dir={prof}', '--hide-scrollbars', 'about:blank'],
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
PANES = ['home', 'keys', 'usage', 'orders', 'bill', 'acct', 'sec']
TODAY = datetime.date.today().isoformat()
IN30 = (datetime.date.today() + datetime.timedelta(days=30)).isoformat()
ERR_HOOK = "window.__errs=[];addEventListener('error',function(e){__errs.push(String(e.message||e))});addEventListener('unhandledrejection',function(e){__errs.push('rej '+String(e.reason))});"
CJK_JS = r'''(function(){var out=[],w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT),n;
 var live=function(el){var sec=el.closest('[data-route]');if(sec&&!sec.classList.contains('on'))return false;var d=el.closest('dialog');if(d&&!d.open)return false;return true};
 while((n=w.nextNode())){var p=n.parentElement;if(!p||/SCRIPT|STYLE/.test(p.nodeName)||p.closest('.lang'))continue;if(!/[一-鿿]/.test(n.nodeValue))continue;
  if(!live(p))continue;var r=p.getBoundingClientRect(),cs=getComputedStyle(p);
  if(!(r.width>0&&r.height>0)||cs.visibility==='hidden'||p.closest('[hidden]'))continue;out.push(n.nodeValue.trim().slice(0,80))}
 document.querySelectorAll('[placeholder],[aria-label],[title]').forEach(function(el){if(!live(el))return;
  ['placeholder','aria-label','title'].forEach(function(a){var v=el.getAttribute(a);if(v&&/[一-鿿]/.test(v))out.push('@'+a+': '+v)})});
 document.querySelectorAll('option').forEach(function(o){if(live(o)&&/[一-鿿]/.test(o.textContent))out.push('option: '+o.textContent)});
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
        if 'exceptionDetails' in r: return {'__exc': r['exceptionDetails'].get('text'), 'desc': r.get('result', {}).get('description')}
        return r['result'].get('value')
    def shot(name, w):
        if not SHOTS: return
        h = ev('Math.min(document.documentElement.scrollHeight,6000)') or 900
        s = ws.send('Page.captureScreenshot', {'format': 'png', 'captureBeyondViewport': True, 'clip': {'x': 0, 'y': 0, 'width': w, 'height': h, 'scale': 1}})
        if 'result' in s: open(os.path.join(SHOTS, name + '.png'), 'wb').write(base64.b64decode(s['result']['data']))
    def pane(p):
        ev(f"document.querySelector('.cs-nav button[data-p=\"{p}\"]').click();window.scrollTo(0,0)"); time.sleep(.35)
    def state(label, lang):
        o = ev(OVF_JS); e = ev('window.__errs'); line = f'{label:28s} sw={o["sw"]}/{o["W"]} errs={len(e)}'
        cj = ev(CJK_JS) if lang == 'en' else []
        if lang == 'en': line += f' cjk={len(cj)}'
        check(o['sw'] <= o['W'] + 1 and not e and not cj, line + ('' if o['sw'] <= o['W'] + 1 else ' OVF ' + str(o['bad'])) + ('' if not e else ' ERR ' + str(e)) + ('' if not cj else ' CJK ' + str(cj[:8])))
    def toast(): time.sleep(.15); return ev("document.getElementById('toast').textContent")
    for (w, h, mobile) in [(1440, 900, False), (390, 844, True)]:
        ws.send('Emulation.setDeviceMetricsOverride', {'width': w, 'height': h, 'deviceScaleFactor': 1, 'mobile': mobile})
        for lang in ['zh', 'en']:
            print(f'\n===== {w}px  lang={lang}')
            acct = {'verify@example.com': {'email': 'verify@example.com', 'type': 'company', 'since': TODAY, 'org': '', 'school': '', 'edu': '', 'keys': [], 'subs': []}}
            ws.send('Page.navigate', {'url': BASE + '#home'}); time.sleep(3)
            ev(f"localStorage.clear();localStorage.setItem('fp-lang','{lang}');sessionStorage.setItem('fp-fresh','1');"
               f"localStorage.setItem('fp-acct-v2',{json.dumps(json.dumps(acct))});localStorage.setItem('fp-session-v2',JSON.stringify('verify@example.com'))")
            ws.send('Page.reload'); time.sleep(4)
            ev("location.hash='#console'"); time.sleep(1.2)
            check(ev("document.querySelector('[data-route].on').getAttribute('data-route')") == 'console', 'seeded session opens #console')
            grp = ev("Array.prototype.map.call(document.querySelectorAll('.cs-nav > *'),function(e){return (e.tagName==='SPAN'?'|':'')+e.textContent.trim()})")
            print('    nav:', grp)
            want = ['|使用', '概览', 'API Key', '使用日志', '订单', '|账户', '钱包', '个人资料', '安全与访问'] if lang == 'zh' else ['|Usage', 'Overview', 'API Key', 'Usage logs', 'Orders', '|Account', 'Wallet', 'Profile', 'Security & access']
            check(grp == want, f'nav groups {grp}')
            for p in PANES:
                pane(p)
                check(ev(f"document.querySelector('.cs-p[data-p=\"{p}\"]').classList.contains('on')") and ev(f"document.querySelector('.cs-nav button[data-p=\"{p}\"]').getAttribute('aria-current')") == 'page', f'pane {p} shown + nav current')
                state(f'pane {p} (new account)', lang)
                shot(f'{w}_{lang}_{p}_empty', w)
            # empty states for a new account
            pane('keys')
            check(ev("!document.getElementById('csKeysEmpty').hidden&&document.querySelectorAll('#csKeys tr').length===0"), 'keys: empty state, no rows')
            heads = ev("Array.prototype.map.call(document.querySelectorAll('.cs-kt th'),function(t){return t.textContent})")
            print('    key columns:', heads); check(len(heads) == 8, 'keys: 8 columns')
            pane('usage')
            heads = ev("Array.prototype.map.call(document.querySelectorAll('.cs-wide th'),function(t){return t.textContent})")
            print('    log columns:', heads); check(len(heads) == 8 and ev("!document.getElementById('csLogsEmpty').hidden&&!document.getElementById('csSumE').hidden"), 'usage: 8 log columns, summary + log empty states')
            # ---- API Key: dialog, create with options, validation ----
            pane('keys'); ev("document.getElementById('csNew').click()"); time.sleep(.4)
            check(ev("document.getElementById('csDlg').open") and ev("document.querySelectorAll('#csKm .chip').length") == 7, 'dialog opens with 7 model chips')
            state('dialog open', lang); shot(f'{w}_{lang}_keys_dialog', w)
            dr = ev("(function(){var r=document.querySelector('#csDlg').getBoundingClientRect();return [Math.round(r.left),Math.round(r.right),Math.round(r.bottom)]})()")
            check(dr[0] >= 0 and dr[1] <= w and dr[2] <= h, f'dialog inside viewport {dr}')
            ev("var f=document.getElementById('csNewF');f.kname.value='Thesis';f.quota.value='-5';f.requestSubmit()"); time.sleep(.2)
            m1 = ev("document.getElementById('csNewMsg').textContent")
            check(bool(m1) and ev("document.getElementById('csDlg').open"), f'invalid quota rejected: {m1}')
            ev("var f=document.getElementById('csNewF');f.quota.value='100';f.ips.value='not-an-ip';f.dispatchEvent(new Event('input'));f.requestSubmit()"); time.sleep(.2)
            m2 = ev("document.getElementById('csNewMsg').textContent"); check(bool(m2), f'invalid IP rejected: {m2}')
            if lang == 'en': check(not any('一' <= c <= '鿿' for c in (m1 or '') + (m2 or '')), 'EN validation messages translated')
            ev(f"var f=document.getElementById('csNewF');f.ips.value='203.0.113.8\\n10.0.0.0/24';f.exp.value='{IN30}';"
               "document.querySelectorAll('#csKm .chip')[0].click();document.querySelectorAll('#csKm .chip')[2].click();document.querySelectorAll('#csKm .chip')[4].click();f.requestSubmit()"); time.sleep(.5)
            check(not ev("document.getElementById('csDlg').open") and not ev("document.getElementById('csReveal').hidden") and len(ev("document.getElementById('csKey').textContent")) == 51, 'create: dialog closed, full key revealed once')
            row = ev("Array.prototype.map.call(document.querySelectorAll('#csKeys tr:first-child td'),function(t){return t.innerText.replace(/\\n/g,' | ')})")
            print('    row:', row)
            check(row[0].startswith('Thesis') and IN30 in row[0] and '¥100.00' in row[3] and '+1' in row[5] and row[6].endswith(TODAY), 'row shows name, expiry, quota, models, date')
            state('keys with one key', lang); shot(f'{w}_{lang}_keys_row', w)
            ev("document.getElementById('csSaved').click();document.getElementById('csNew').click()"); time.sleep(.3)
            check(ev("document.getElementById('csNewF').kname.value") == '' and ev("document.querySelectorAll('#csKm .chip.on').length") == 0, 'dialog resets on reopen')
            ev("var f=document.getElementById('csNewF');f.kname.value='Batch jobs';f.requestSubmit()"); time.sleep(.4); ev("document.getElementById('csSaved').click()")
            n = lambda: ev("document.querySelectorAll('#csKeys tr').length")
            check(n() == 2, 'two keys listed')
            ev("var q=document.getElementById('csKq');q.value='bat';q.dispatchEvent(new Event('input'))"); time.sleep(.2)
            check(n() == 1 and 'Batch' in ev("document.querySelector('#csKeys tr td').textContent"), 'search by name')
            ev("var q=document.getElementById('csKq');q.value='';q.dispatchEvent(new Event('input'));var s=document.getElementById('csKs');s.value='off';s.dispatchEvent(new Event('change'))"); time.sleep(.2)
            check(n() == 0 and not ev("document.getElementById('csKeysNone').hidden"), 'filter disabled -> none + clear-filters state')
            ev("document.getElementById('csKclr').click()"); time.sleep(.2); check(n() == 2, 'clear filters')
            ev("document.querySelector('#csKeys [data-tog=\"1\"]').click()"); time.sleep(.2)
            t1 = toast(); check(bool(t1) and (lang == 'zh' or not any('一' <= c <= '鿿' for c in t1)), f'toggle toast: {t1}')
            ev("var s=document.getElementById('csKs');s.value='off';s.dispatchEvent(new Event('change'))"); time.sleep(.2)
            st = ev("document.querySelector('#csKeys tr td:nth-child(2)').textContent")
            check(n() == 1 and 'Thesis' in ev("document.querySelector('#csKeys tr td').textContent"), f'disabled key filtered ({st})')
            ev("var s=document.getElementById('csKs');s.value='on';s.dispatchEvent(new Event('change'))"); time.sleep(.2); check(n() == 1, 'enabled filter')
            ev("var s=document.getElementById('csKs');s.value='';s.dispatchEvent(new Event('change'))"); time.sleep(.2)
            ev("document.querySelector('#csKeys [data-del=\"0\"]').click()"); time.sleep(.1)
            check(n() == 2, 'delete needs confirmation'); ev("document.querySelector('#csKeys [data-del=\"0\"]').click()"); time.sleep(.2)
            check(n() == 1, 'delete after confirm')
            state('keys after actions', lang)
            ev("document.getElementById('csNew').click()"); time.sleep(.2); ev("document.getElementById('csCancelX').click()"); time.sleep(.2)
            check(not ev("document.getElementById('csDlg').open"), 'dialog close button')
            # ---- usage filters ----
            pane('usage')
            check(ev("document.querySelectorAll('#csLm option').length") == 8 and ev("document.querySelectorAll('#csLk option').length") == 2, 'usage: model (7) + key (1) filter options')
            ev("['csLt','csLm','csLk'].forEach(function(id,i){var s=document.getElementById(id);s.selectedIndex=i===0?0:1;s.dispatchEvent(new Event('change'))})"); time.sleep(.2)
            check(not ev("document.getElementById('csLogsEmpty').hidden") and ev("document.querySelectorAll('#csLogs tr').length") == 0, 'usage: filters applied, still empty, no fabricated rows')
            state('usage filtered', lang); shot(f'{w}_{lang}_usage_filtered', w)
            # ---- wallet ----
            pane('bill')
            ev("document.querySelector('.cs-pay [data-v=\"wechat\"]').click()"); time.sleep(.1)
            check(ev("document.querySelector('.cs-pay [data-v=\"wechat\"]').getAttribute('aria-checked')") == 'true' and ev("document.querySelector('.cs-pay [data-v=\"alipay\"]').getAttribute('aria-checked')") == 'false', 'payment method switch')
            ev("document.getElementById('csRedeem').requestSubmit()"); t2 = toast()
            ev("var f=document.getElementById('csRedeem');f.code.value='ABCD-1234';f.requestSubmit()"); t3 = toast()
            check(t2 and t3 and t2 != t3, f'redeem: empty -> "{t2}", code -> "{t3}"')
            aff = ev("document.getElementById('csAff').textContent"); check('?aff=' in aff and aff.endswith('#start'), f'invite link {aff}')
            ref = ev("Array.prototype.map.call(document.querySelectorAll('.cs-ref-n b'),function(b){return b.textContent})")
            check(ref == ['¥0.00', '¥0.00', '0'], f'referral counters at zero {ref}')
            state('wallet after actions', lang)
            # ---- profile / notifications ----
            pane('acct')
            uid = ev("document.getElementById('csUid').textContent"); check(uid.isdigit() and len(uid) == 6, f'user id {uid}')
            check(ev("!document.querySelector('#csOrg').hidden") and ev("!document.querySelector('#csSubs').closest('.cs-box').hidden"), 'company fields + sub-accounts kept')
            ev("document.querySelector('#csNtf [data-v=\"webhook\"]').click()"); time.sleep(.1)
            check(ev("document.querySelector('#csNtf [data-nm=\"webhook\"]').hidden") is False and ev("document.querySelector('#csNtf [data-nm=\"email\"]').hidden") is True, 'webhook shows URL field, hides email')
            ev("var f=document.getElementById('csNtf');f.th.value='50';f.hook.value='ftp://x';f.requestSubmit()"); time.sleep(.1)
            check(bool(ev("document.getElementById('csNtfMsg').textContent")), 'bad webhook URL rejected')
            ev("var f=document.getElementById('csNtf');f.hook.value='https://example.com/hook';f.requestSubmit()"); t4 = toast()
            saved = ev("JSON.parse(localStorage.getItem('fp-acct-v2'))['verify@example.com'].notify")
            check(saved == {'via': 'webhook', 'th': '50', 'mail': '', 'hook': 'https://example.com/hook'}, f'notify saved {saved} / {t4}')
            state('profile webhook', lang); shot(f'{w}_{lang}_acct_webhook', w)
            # ---- security ----
            pane('sec')
            ev("document.querySelector('[aria-controls=\"csPwF\"]').click()"); time.sleep(.2)
            check(not ev("document.getElementById('csPwF').hidden"), 'change-password form opens')
            ev("document.getElementById('csPwF').requestSubmit()"); time.sleep(.1)
            check(bool(ev("document.getElementById('csPwMsg').textContent")), 'empty password form rejected (no password typed)')
            ev("document.querySelector('[aria-controls=\"csTotpF\"]').click()"); time.sleep(.1)
            ev("var f=document.getElementById('csTotpF');f.code.value='12';f.requestSubmit()"); time.sleep(.1)
            check(bool(ev("document.getElementById('csTotpMsg').textContent")), '2FA: short code rejected')
            state('security forms open', lang); shot(f'{w}_{lang}_sec_forms', w)
            ev("document.getElementById('csPwF').querySelector('[data-sx-close]').click();document.getElementById('csTotpF').querySelector('[data-sx-close]').click()"); time.sleep(.1)
            check(ev("document.getElementById('csPwF').hidden&&document.getElementById('csTotpF').hidden"), 'forms close')
            ev("document.getElementById('csPk').click()"); t5 = toast(); check(bool(t5), f'passkey: {t5}')
            ev("document.getElementById('csTok').click()"); time.sleep(.2)
            tok1 = ev("document.getElementById('csTokV').textContent")
            check(len(tok1) == 32 and not ev("document.getElementById('csTokR').hidden"), 'access token generated + revealed once')
            ev("document.getElementById('csTok').click()"); time.sleep(.1)
            check(ev("document.getElementById('csTokV').textContent") == tok1, 'regenerate needs confirmation')
            ev("document.getElementById('csTok').click()"); time.sleep(.2)
            check(ev("document.getElementById('csTokV').textContent") != tok1, 'regenerate after confirm')
            state('security token', lang)
            if lang == 'en':
                for t in (t2, t3, t4, t5):
                    check(not any('一' <= c <= '鿿' for c in (t or '')), f'EN toast translated: {t}')
            # ---- persisted after reload, old-format key still renders ----
            ev("var a=JSON.parse(localStorage.getItem('fp-acct-v2'));a['verify@example.com'].keys.push({name:'Old key',tail:'abcd',at:'2026-10-01'});localStorage.setItem('fp-acct-v2',JSON.stringify(a))")
            ws.send('Page.reload'); time.sleep(3.5); ev("location.hash='#console'"); time.sleep(.8); pane('keys')
            check(n() == 2 and 'Old key' in ev("document.getElementById('csKeys').textContent"), 'keys persist; pre-existing key format renders')
            state('after reload', lang)
            ev("document.getElementById('csOut').click()"); time.sleep(1)
            check(ev("location.hash") == '#login', 'sign out -> #login')
            check(not ev('window.__errs'), f'no JS errors {ev("window.__errs")}')
finally:
    pr.terminate()
print('\nFAILS:', len(fails))
for f in fails: print(' -', f)
