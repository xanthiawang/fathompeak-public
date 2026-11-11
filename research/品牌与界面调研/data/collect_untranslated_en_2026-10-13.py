"""英文模式漏翻扫描：无头 Chrome 打开站点，切到 EN，逐个路由（含每个模型、指南详情）渲染后，
收集仍含中文的文本节点、placeholder、aria-label、title、data-toast，以及脚本里 toast('…') 的字面量。
用法：python3 -I collect_untranslated_en_2026-10-13.py <index.html> <输出 json>
"""
import importlib.util, json, os, re, subprocess, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('wt', os.path.join(HERE, 'cdp_walkthrough_2026-10-12.py'))
wt = importlib.util.module_from_spec(spec); spec.loader.exec_module(wt)

html_path, out_json = sys.argv[1], sys.argv[2]
src = open(html_path, encoding='utf8').read()
out_dir = os.path.dirname(os.path.abspath(out_json))
wrapped = os.path.join(out_dir, 'wrapped_en.html')
open(wrapped, 'w', encoding='utf8').write(wt.SKEL + src + '\n</body></html>')
url0 = 'file://' + wrapped

ids = re.findall(r'"id": "([a-z0-9-]+)"', src[src.index('var M='):src.index('var I18N={')])
routes = ['home', 'models', 'pricing', 'enterprise', 'network', 'about', 'news', 'docs', 'guides', 'login', 'console', 'start', 'changelog', 'newsletter']
routes += ['model-' + i for i in ids if not i.startswith(('dev-', 'plant-', 'esg-', 'proc-'))]
gids = re.findall(r'"id": "((?:dev|plant|esg|proc)[a-z0-9-]*)"', src)
routes += ['guide-' + g for g in gids]

COLLECT = r"""(function(){var CJK=/[一-鿿]/,out={text:[],attr:[]};
var w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT,null),n;
while((n=w.nextNode())){var p=n.parentNode;if(!p||p.nodeName==='SCRIPT'||p.nodeName==='STYLE'||(p.closest&&p.closest('.lang')))continue;var t=n.nodeValue.trim();if(t&&CJK.test(t))out.text.push(t)}
document.querySelectorAll('[placeholder],[aria-label],[title],[data-toast]').forEach(function(e){['placeholder','aria-label','title','data-toast'].forEach(function(a){var v=e.getAttribute(a);if(v&&CJK.test(v))out.attr.push(a+'␟'+v.trim())})});
if(CJK.test(document.title))out.attr.push('document.title␟'+document.title);
return JSON.stringify(out)})()"""

prof = os.path.join(out_dir, '.chrome-profile-en')
proc = subprocess.Popen([wt.CHROME, '--headless=new', f'--remote-debugging-port={wt.PORT}', f'--user-data-dir={prof}',
                         '--window-size=1440,900', '--allow-file-access-from-files', 'about:blank'],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
text, attr = {}, {}
try:
    for _ in range(50):
        try: urllib.request.urlopen(f'http://127.0.0.1:{wt.PORT}/json/version', timeout=1); break
        except Exception: time.sleep(0.2)
    req = urllib.request.Request(f'http://127.0.0.1:{wt.PORT}/json/new?about:blank', method='PUT')
    ws = wt.WS(json.loads(urllib.request.urlopen(req).read())['webSocketDebuggerUrl'])
    ws.send('Page.enable'); ws.send('Runtime.enable')
    ws.send('Page.navigate', {'url': url0 + '#home'}); time.sleep(2)
    ws.send('Runtime.evaluate', {'expression': "try{localStorage.setItem('fp-lang','en')}catch(e){}"})
    for r in routes:
        ws.send('Page.navigate', {'url': 'about:blank'}); time.sleep(0.2)
        ws.send('Page.navigate', {'url': url0 + '#' + r}); time.sleep(1.6)
        v = ws.send('Runtime.evaluate', {'expression': COLLECT, 'returnByValue': True})['result']['result']['value']
        d = json.loads(v)
        for t in d['text']: text.setdefault(t, r)
        for a in d['attr']: attr.setdefault(a, r)
        print(f'{r:28s} text={len(d["text"]):4d} attr={len(d["attr"]):3d}')
finally:
    proc.terminate()

pre = src[:src.index('var I18N={')]
toasts = sorted(set(re.findall(r"toast\('([^']*[一-鿿][^']*)'\)", src)))
json.dump({'text': text, 'attr': attr, 'toast_literals': toasts}, open(out_json, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print('unique text', len(text), 'attr', len(attr), 'toasts', len(toasts))
