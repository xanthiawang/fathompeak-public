"""英文模式溢出扫描：桌面 1440 与手机 390 两个视口，逐路由在中文与英文两种语言下，
找出"带文字的元素超出父元素左右边界"的情况，只报告英文才出现的问题。
用法：python3 -I scan_en_overflow_2026-10-13.py <index.html> <输出目录>
"""
import importlib.util, json, os, subprocess, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('wt', os.path.join(HERE, 'cdp_walkthrough_2026-10-12.py'))
wt = importlib.util.module_from_spec(spec); spec.loader.exec_module(wt)
html_path, out_dir = sys.argv[1], sys.argv[2]
os.makedirs(out_dir, exist_ok=True)
wrapped = os.path.join(out_dir, 'wrapped_ov.html')
open(wrapped, 'w', encoding='utf8').write(wt.SKEL + open(html_path, encoding='utf8').read() + '\n</body></html>')
url0 = 'file://' + wrapped
ROUTES = ['home', 'models', 'enterprise', 'network', 'about', 'news', 'docs', 'guides', 'guide-esg-talk', 'model-glm-5-3']

SCAN = r"""(function(){document.querySelectorAll('.rv').forEach(function(e){e.classList.add('shown')});
var out=[];document.querySelectorAll('section[data-route].on *, .hdr *, footer *, .hero *').forEach(function(el){
 var has=false;for(var i=0;i<el.childNodes.length;i++){var n=el.childNodes[i];if(n.nodeType===3&&n.nodeValue.trim()){has=true;break}} if(!has)return;
 var cs=getComputedStyle(el); if(cs.display==='none'||cs.visibility==='hidden'||cs.position==='fixed')return;
 var r=el.getBoundingClientRect(); if(!r.width||!r.height)return;
 var p=el.parentElement; while(p&&getComputedStyle(p).display==='contents')p=p.parentElement; if(!p||p===document.body)return;
 var q=p.getBoundingClientRect(); var over=Math.round(Math.max(r.right-q.right,q.left-r.left));
 if(over>3||el.scrollWidth>el.clientWidth+3&&cs.overflow==='visible'&&cs.whiteSpace==='nowrap')
   out.push((el.className&&typeof el.className==='string'?'.'+el.className.trim().split(/\s+/).join('.'):el.tagName.toLowerCase())+' | '+el.textContent.trim().slice(0,50)+' | +'+over+'px')});
return JSON.stringify(out)})()"""

prof = os.path.join(out_dir, '.chrome-ov')
proc = subprocess.Popen([wt.CHROME, '--headless=new', f'--remote-debugging-port={wt.PORT}', f'--user-data-dir={prof}', '--allow-file-access-from-files', 'about:blank'],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
report = {}
try:
    for _ in range(50):
        try: urllib.request.urlopen(f'http://127.0.0.1:{wt.PORT}/json/version', timeout=1); break
        except Exception: time.sleep(0.2)
    for vname, W, H, dsf, mob in [('desktop', 1440, 900, 1, False), ('mobile', 390, 844, 2, True)]:
        tab = json.loads(urllib.request.urlopen(urllib.request.Request(f'http://127.0.0.1:{wt.PORT}/json/new?about:blank', method='PUT')).read())
        ws = wt.WS(tab['webSocketDebuggerUrl'])
        ws.send('Emulation.setDeviceMetricsOverride', {'width': W, 'height': H, 'deviceScaleFactor': dsf, 'mobile': mob}); ws.send('Page.enable')
        res = {}
        for lang in ('zh', 'en'):
            ws.send('Page.navigate', {'url': url0 + '#home'}); time.sleep(1.5)
            ws.send('Runtime.evaluate', {'expression': f"try{{localStorage.setItem('fp-lang','{lang}')}}catch(e){{}}"})
            for r in ROUTES:
                ws.send('Page.navigate', {'url': 'about:blank'}); time.sleep(0.2)
                ws.send('Page.navigate', {'url': url0 + '#' + r}); time.sleep(1.6)
                v = ws.send('Runtime.evaluate', {'expression': SCAN, 'returnByValue': True})['result']['result']['value']
                res[(lang, r)] = set(json.loads(v))
        for r in ROUTES:
            zh_keys = {x.split(' | ')[0] for x in res[('zh', r)]}
            only = sorted(x for x in res[('en', r)] if x.split(' | ')[0] not in zh_keys)
            if only: report[f'{vname} #{r}'] = only
finally:
    proc.terminate()
json.dump(report, open(os.path.join(out_dir, 'en_overflow.json'), 'w'), ensure_ascii=False, indent=1)
for k, v in report.items():
    print('##', k)
    for x in v[:12]: print('  ', x)
print('routes with EN-only overflow:', len(report))
