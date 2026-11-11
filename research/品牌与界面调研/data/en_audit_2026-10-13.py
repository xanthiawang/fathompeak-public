import json,time,subprocess,urllib.request,importlib.util,sys
spec=importlib.util.spec_from_file_location('cdp','/Users/zixin/programs/ai-skills/reference-site-prototype/scripts/cdp_client.py');cdp=importlib.util.module_from_spec(spec);spec.loader.exec_module(cdp)
port=9543;prof=sys.argv[0]+'.prof';subprocess.run(['rm','-rf',prof])
pr=subprocess.Popen([cdp.CHROME,'--headless=new',f'--remote-debugging-port={port}',f'--user-data-dir={prof}','about:blank'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
routes=sys.argv[2].split(',')
JS=r'''(function(){
 var vis=function(el){var r=el.getBoundingClientRect();var cs=getComputedStyle(el);return r.width>0&&r.height>0&&cs.visibility!=='hidden'&&cs.display!=='none'&&!el.closest('[hidden]')&&el.closest('[data-route]')?el.closest('[data-route]').classList.contains('on'):r.width>0};
 var path=function(el){var p=[];for(var i=0;i<3&&el&&el!==document.body;i++,el=el.parentElement){p.unshift(el.tagName.toLowerCase()+(el.className&&typeof el.className=='string'?'.'+el.className.trim().split(/\s+/).join('.'):''))}return p.join('>')};
 var cjk=[],w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT),n;
 while((n=w.nextNode())){var p=n.parentElement;if(!p||/SCRIPT|STYLE/.test(p.nodeName)||p.closest('.lang'))continue;if(!/[一-鿿]/.test(n.nodeValue))continue;if(!vis(p))continue;
   var sec=p.closest('[data-route]');if(sec&&!sec.classList.contains('on'))continue;cjk.push(path(p)+' :: '+n.nodeValue.trim()+' ⟪'+p.parentElement.textContent.trim().replace(/\s+/g,' ').slice(0,160)+'⟫')}
 var heads=[];document.querySelectorAll('body *').forEach(function(el){if(!el.firstChild||el.closest('#pill,.menu,nav'))return;var sec=el.closest('[data-route]');if(sec&&!sec.classList.contains('on'))return;if(el.closest('footer'))return;
   var cs=getComputedStyle(el);var fs=parseFloat(cs.fontSize);if(fs<19)return;if(!/Fraunces/.test(cs.fontFamily))return;
   var own=Array.prototype.some.call(el.childNodes,function(c){return c.nodeType==3&&c.nodeValue.trim()});if(!own)return;
   var r=el.getBoundingClientRect();if(!(r.width>0&&r.height>0))return;var t=el.textContent.trim();
   var host=el.closest('.hand1');heads.push((host?'HAND ':'---- ')+Math.round(fs)+'px '+path(el)+' :: '+t.slice(0,60))});
 return {cjk:cjk,heads:heads}})()'''
try:
  for _ in range(50):
    try: urllib.request.urlopen(f'http://127.0.0.1:{port}/json/version',timeout=1);break
    except Exception: time.sleep(.2)
  tab=json.loads(urllib.request.urlopen(urllib.request.Request(f'http://127.0.0.1:{port}/json/new?about:blank',method='PUT')).read())
  ws=cdp.WS(tab['webSocketDebuggerUrl']);ws.send('Page.enable');ws.send('Runtime.enable')
  ws.send('Emulation.setDeviceMetricsOverride',{'width':1440,'height':900,'deviceScaleFactor':1,'mobile':False})
  ev=lambda e:ws.send('Runtime.evaluate',{'expression':e,'returnByValue':True,'awaitPromise':True})['result']['result'].get('value')
  ws.send('Page.navigate',{'url':sys.argv[1]+'#home'});time.sleep(4)
  ev("localStorage.setItem('fp-lang','en');sessionStorage.setItem('fp-fresh','1')");ws.send('Page.reload');time.sleep(5)
  for r in routes:
    ev(f"location.hash='#{r}'");time.sleep(1.2)
    ev("document.querySelectorAll('.rv').forEach(function(e){e.classList.add('shown')})");time.sleep(.5)
    o=ev(JS);print(f'\n######## {r}  lang={ev("document.documentElement.lang")}  cjk={len(o["cjk"])}  heads={len(o["heads"])}')
    for h in o['heads']: print('  H',h)
    for c in o['cjk']: print('  Z',c)
finally: pr.terminate()
