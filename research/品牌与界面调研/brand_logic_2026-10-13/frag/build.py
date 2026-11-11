import os,re,sys
F=os.path.dirname(os.path.abspath(__file__)); H=os.path.join(F,'..','..','五家竞品品牌逻辑拆解_2026-10-13.html')
s=open(H,encoding='utf8').read()
for k in ['sf','ppio','infini','crusoe','emerald']:
    for kind,tag in [('row','ROW'),('sec','SECTION')]:
        p=os.path.join(F,f'{kind}_{k}.html')
        if os.path.exists(p):
            body=open(p,encoding='utf8').read()
            s=re.sub(rf'<!--{tag}:{k}-->.*?<!--/{tag}:{k}-->|<!--{tag}:{k}-->', f'<!--{tag}:{k}-->'+body+f'<!--/{tag}:{k}-->', s, count=1, flags=re.S)
p=os.path.join(F,'sec_cross.html')
if os.path.exists(p):
    s=re.sub(r'<!--SECTION:cross-->.*?<!--/SECTION:cross-->|<!--SECTION:cross-->','<!--SECTION:cross-->'+open(p,encoding='utf8').read()+'<!--/SECTION:cross-->',s,count=1,flags=re.S)
open(H,'w',encoding='utf8').write(s); print('built', len(s))
