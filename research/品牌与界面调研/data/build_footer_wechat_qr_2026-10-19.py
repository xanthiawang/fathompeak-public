"""官网联系方式加微信公众号二维码（Zixin 2026-10-19：「我想把公众号加入我们的联系方式上，类似图二」——
图二：一行「微信公众号」、白色圆角卡片里的二维码、下方「微信扫一扫」）。
站点原本预留了 SOCIAL 列表（页脚 #footSocial 与右下角咨询浮窗 #fabQr 共用，空时不显示），这里填入公众号并按图二改排版。
公众号名称 Zixin 还没给，只写「微信公众号」，不写名字。
第二版（Zixin：「二维码的线框不好看，按 Dia 风格重新设计」）：去掉描边，白色大圆角卡片 + 极淡的扩散阴影，
二维码原图的白边裁掉，留白交给卡片内边距（仍够扫码静区）。
第三版（Zixin：「这个光晕不好看」）：去掉背后的渐变光晕，只留白色圆角卡片 + Dia 柔和投影（站点 --dia-sh2）。
用法：python3 -I build_footer_wechat_qr_2026-10-19.py <站点仓库根目录> <公众号二维码图片>
"""
import json, shutil, sys
from pathlib import Path

ROOT, QR = Path(sys.argv[1]), Path(sys.argv[2])
if not QR.exists(): sys.exit(f'[停止] 找不到二维码图片 {QR}')
DST = 'art/qr/wechat-mp_2026-10-19.png'
(ROOT / 'art' / 'qr').mkdir(parents=True, exist_ok=True)
from PIL import Image, ImageOps
im = Image.open(QR).convert('L')
bbox = ImageOps.invert(im).point(lambda v: 255 if v > 60 else 0).getbbox()   # 深色模块的外框
pad = 4; im = im.crop((max(0, bbox[0] - pad), max(0, bbox[1] - pad), min(im.width, bbox[2] + pad), min(im.height, bbox[3] + pad)))
im.save(ROOT / DST, optimize=True)   # PNG：边缘比 JPG 干净
p = ROOT / 'index.html'; s = p.read_text(encoding='utf8')


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n: sys.exit(f'[停止] 匹配 {c} 次（应为 {n}）：{old[:90]}')
    s = s.replace(old, new)


rep("  var SOCIAL=[]; /* 有官方二维码后按此格式填入",
    f"  var SOCIAL=[{{k:'微信公众号',img:'{DST}',cap:'微信扫一扫'}}]; /* 2026-10-19 填入公众号。格式");
rep("""  function qrHTML(){return SOCIAL.map(function(x){return '<figure><img src="'+x.img+'" alt="'+x.k+'二维码" width="96" height="96" loading="lazy"><figcaption>'+x.k+'</figcaption></figure>'}).join('')}""",
    """  /* 图二样式：标签「微信公众号」→ 白色圆角卡片里的二维码 → 「微信扫一扫」 */
  function qrHTML(){return SOCIAL.map(function(x){return '<figure class="qr"><figcaption class="qr-k">'+x.k+'</figcaption><span class="qr-card"><img src="'+x.img+'" alt="沐仞科技'+x.k+'二维码" width="128" height="128" loading="lazy"></span>'+(x.cap?'<span class="qr-cap">'+x.cap+'</span>':'')+'</figure>'}).join('')}""")
rep('</head>', '<style id="wechat-qr-20261019">\n'
    '/* 联系方式里的公众号二维码（2026-10-19，参照图二；Dia 风格：无描边、白色大圆角、柔和投影，不加光晕）。\n'
    '   站点主样式在 body 里、晚于本段，选择器加一级前缀 */\n'
    'footer .social,.fab-p .fab-qr{display:block;margin-top:20px}\n'
    'footer .social figure.qr,.fab-p .fab-qr figure.qr{display:grid;justify-items:start;gap:12px;margin:0;text-align:left}\n'
    'footer .social .qr-k{font:400 11px var(--mono);letter-spacing:.06em;text-transform:uppercase;color:var(--ink-50)}\n'
    'footer .social .qr-card,.fab-p .fab-qr .qr-card{display:block;padding:14px;background:#fff;border:0;border-radius:22px;'
    'box-shadow:0 6px 20px rgba(0,0,0,.08),0 0 2px rgba(0,0,0,.05)}\n'
    'footer .social .qr-card img{display:block;width:128px;height:128px;margin:0;border-radius:4px;image-rendering:auto}\n'
    'footer .social .qr-cap,.fab-p .fab-qr .qr-cap{font:400 13px var(--sans);color:var(--ink-50)}\n'
    '.fab-p .fab-qr{padding-top:14px;border-top:1px solid var(--line-2)}\n'
    '.fab-p .fab-qr .qr-k{font:500 13px var(--sans);color:var(--ink)}\n'
    '.fab-p .fab-qr .qr-card{padding:10px;border-radius:18px;box-shadow:0 2px 8px rgba(0,0,0,.06),0 0 2px rgba(0,0,0,.04)}\n'
    '.fab-p .fab-qr .qr-card img{display:block;width:100px;height:100px;margin:0;border-radius:3px}\n'
    '</style>\n</head>')
EN = {'微信扫一扫': 'Scan with WeChat'}
rep('  syncAuthLocale(); applyLang();', '  (function(S){for(var k in S) if(!(k in I18N)) I18N[k]=S[k]})(' + json.dumps(EN, ensure_ascii=False) + ');  /* 公众号二维码 */\n  syncAuthLocale(); applyLang();')
p.write_text(s, encoding='utf8')
print('done:', DST)
