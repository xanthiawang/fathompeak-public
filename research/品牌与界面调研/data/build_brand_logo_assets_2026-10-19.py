"""新 logo（层叠峰面 + FATHOMPEAK 科技字标 + 沐仞科技，Codex 分支 codex/logo-svg-monochrome-20261018）派生网站用素材。
Zixin 2026-10-19：「把我们所有官网和所有后台的 logo 和字，关于 logo 的所有字体，都换成这个」；旧 logo 指双峰山形标。
2026-10-19 第二版（Zixin：「我只是想进行图形更换，大小和比例要和之前一样」）：只把旧山形换成新峰面图形，原有文字、版式、背景不动。
  art/brand/fathompeak-mark_2026-10-19.svg        峰面图形（紧贴边界，取自官方主标，不重画、不改渐变）
  art/share/favicon.svg                           方形视框里放图形
  art/share/icon-192.png、icon-512.png、apple-touch-icon.png  原渐变底不变，白色山形换成新图形的白色剪影（宽 64%，居中）
  art/share/og-1200x630_2026-10-19.png            原分享图只把左上角白色山形换成新图形白色剪影（高约 11px，同一位置），文字不动
第三版（Zixin：「你的英文字体没用我们的 logo」）：用作 logo 的英文「FathomPeak」统一换成新标的 FATHOMPEAK 转曲字标，中文与位置不动：
  art/brand/fathompeak-wordmark_2026-10-19.svg   英文字标（紧贴边界，黑色）
  分享图左上角「FathomPeak」→ 白色字标（字高 13px，同一位置）
  登录插画：Zixin 10-19 要求保持原图，不改。
用法：python3 -I build_brand_logo_assets_2026-10-19.py <官方 logo 目录> <站点仓库根目录>
"""
import base64, importlib.util, json, os, re, subprocess, sys, time, urllib.request
from pathlib import Path

LOGO, SITE = Path(sys.argv[1]), Path(sys.argv[2])
spec = importlib.util.spec_from_file_location("w", "/Users/zixin/Desktop/沐仞科技/04_调研与测试/品牌与界面调研/data/cdp_walkthrough_2026-10-12.py")
w = importlib.util.module_from_spec(spec); spec.loader.exec_module(w)
OUT = SITE / 'art' / 'brand'; OUT.mkdir(parents=True, exist_ok=True)
TMP = Path(os.environ.get('TMPDIR', '/tmp')) / 'fp_logo_build'; TMP.mkdir(parents=True, exist_ok=True)


def group_xml(src, gid):
    """取出 <g id="gid"> … 对应的 </g>（按嵌套深度配对）。"""
    a = src.find(f'<g id="{gid}"')
    if a < 0: sys.exit(f'[停止] 主标里找不到分组 {gid}')
    depth, i = 0, a
    for m in re.finditer(r'<g\b|</g>', src[a:]):
        depth += 1 if m.group(0) == '<g' else -1
        if depth == 0: return src[a:a + m.end()]
    sys.exit(f'[停止] 分组 {gid} 没有闭合')


src = (LOGO / 'primary.svg').read_text(encoding='utf8')
defs = re.search(r'<defs>.*?</defs>', src, re.S).group(0)
SYM, EN, CN = group_xml(src, '峰面图形'), group_xml(src, '英文科技字标'), group_xml(src, '中文沐仞')
HEAD = '<svg xmlns="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" viewBox="{vb}" width="{w}" height="{h}">\n<title>{t}</title>\n'

# Chrome：量边界、渲染 PNG
port = 9483
proc = subprocess.Popen([w.CHROME, "--headless=new", f"--remote-debugging-port={port}", f"--user-data-dir={TMP}/prof", "--hide-scrollbars", "--allow-file-access-from-files", "about:blank"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    for _ in range(50):
        try: urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=1); break
        except Exception: time.sleep(0.2)
    tab = json.loads(urllib.request.urlopen(urllib.request.Request(f"http://127.0.0.1:{port}/json/new?about:blank", method="PUT")).read())
    ws = w.WS(tab["webSocketDebuggerUrl"]); ws.send("Page.enable"); ws.send("Runtime.enable")

    def ev(js):
        r = ws.send("Runtime.evaluate", {"expression": js, "returnByValue": True, "awaitPromise": True})
        return r["result"]["result"].get("value")

    def load(url, wait=1.0):
        ws.send("Page.navigate", {"url": url}); time.sleep(wait)

    load('file://' + str(LOGO / 'primary.svg'))
    bb = json.loads(ev("""JSON.stringify(Object.fromEntries(['峰面图形','英文科技字标','中文沐仞'].map(id=>{const r=document.getElementById(id).getBoundingClientRect(),o=document.documentElement.getBoundingClientRect();return [id,[r.left-o.left,r.top-o.top,r.width,r.height]]})))"""))
    sx, sy, sw, sh = bb['峰面图形']; ex, ey, ew, eh = bb['英文科技字标']; cx, cy, cw, ch = bb['中文沐仞']
    print('bbox symbol', [round(v, 1) for v in bb['峰面图形']], 'en', [round(v, 1) for v in bb['英文科技字标']], 'cn', [round(v, 1) for v in bb['中文沐仞']])

    def save(name, body, vb, wpx, hpx, title):
        p = OUT / name
        p.write_text(HEAD.format(vb=vb, w=wpx, h=hpx, t=title) + defs + '\n' + body + '\n</svg>\n', encoding='utf8')
        return p

    # 1 图形
    pad = sh * 0.04
    mark = save('fathompeak-mark_2026-10-19.svg', SYM, f'{sx-pad:.2f} {sy-pad:.2f} {sw+2*pad:.2f} {sh+2*pad:.2f}', round(sw + 2 * pad), round(sh + 2 * pad), 'FathomPeak 沐仞科技 · 峰面图形')
    padw = eh * 0.06
    wordmark = save('fathompeak-wordmark_2026-10-19.svg', EN, f'{ex-padw:.2f} {ey-padw:.2f} {ew+2*padw:.2f} {eh+2*padw:.2f}', round(ew + 2 * padw), round(eh + 2 * padw), 'FathomPeak 沐仞科技 · 英文字标')

    # 4 favicon：方形视框，图形居中
    side = sw * 1.08
    fav = SITE / 'art' / 'share' / 'favicon.svg'
    fav.write_text(HEAD.format(vb=f'{sx-(side-sw)/2:.2f} {sy+sh/2-side/2:.2f} {side:.2f} {side:.2f}', w=64, h=64, t='FathomPeak 沐仞科技') + defs + '\n' + SYM + '\n</svg>\n', encoding='utf8')

    def shot(html, W, H, out, transparent=False):
        hp = TMP / 'shot.html'; hp.write_text(html, encoding='utf8')
        ws.send("Emulation.setDeviceMetricsOverride", {"width": W, "height": H, "deviceScaleFactor": 1, "mobile": False})
        if transparent: ws.send("Emulation.setDefaultBackgroundColorOverride", {"color": {"r": 0, "g": 0, "b": 0, "a": 0}})
        load('file://' + str(hp), 1.2)
        data = ws.send("Page.captureScreenshot", {"format": "png", "clip": {"x": 0, "y": 0, "width": W, "height": H, "scale": 1}})["result"]["data"]
        Path(out).write_bytes(base64.b64decode(data))
        if transparent: ws.send("Emulation.setDefaultBackgroundColorOverride", {})

    # 5 白色剪影（透明底，用于渐变底的图标与分享图）：图形原样渲染后滤成纯白
    shot(f'<html><body style="margin:0;background:transparent"><img src="file://{wordmark}" style="width:1500px;height:auto;display:block;filter:brightness(0) invert(1)"></body></html>', 1500, 110, TMP / 'wordmark_white.png', True)
    shot(f'<html><body style="margin:0;background:transparent"><img src="file://{wordmark}" style="width:1500px;height:auto;display:block"></body></html>', 1500, 110, TMP / 'wordmark_black.png', True)
    shot(f'<html><body style="margin:0;background:transparent"><img src="file://{mark}" style="width:1300px;height:auto;display:block;filter:brightness(0) invert(1)"></body></html>', 1300, 470, TMP / 'mark_white.png', True)
finally:
    proc.terminate()

from PIL import Image, ImageDraw, ImageFilter
import random


def erase(im, box, thresh):
    """box 内凡与背景差异大的像素（字迹）连同外扩一圈，用每行左右边缘颜色线性插值补回，再加一点纸纹噪点。"""
    x0, y0, x1, y1 = box; px = im.load(); rnd = random.Random(7)
    g = im.convert('L'); gp = g.load()
    mask = Image.new('L', im.size, 0); mp = mask.load()
    for y in range(y0, y1):
        ref = (gp[x0, y] + gp[x1 - 1, y]) / 2
        for x in range(x0, x1):
            if abs(gp[x, y] - ref) > thresh: mp[x, y] = 255
    mask = mask.filter(ImageFilter.MaxFilter(9)); mp = mask.load()
    for y in range(y0, y1):
        L, R = px[x0, y], px[x1 - 1, y]
        for x in range(x0, x1):
            if mp[x, y]:
                t = (x - x0) / max(1, x1 - 1 - x0); n = rnd.uniform(-1.6, 1.6)
                px[x, y] = tuple(int(L[c] * (1 - t) + R[c] * t + n) for c in range(3))


def white_mark(width):
    m = Image.open(TMP / 'mark_white.png').convert('RGBA'); m = m.crop(m.getbbox())
    return m.resize((round(width), round(m.height * width / m.width)), Image.LANCZOS)


def erase_mountain(im, bbox, grow=3):
    """旧山形 path「M3 20 10 6l4 7 3-4 4 11z」（24 单位）按它在图里的实测外框 bbox 还原成多边形，
    外扩 grow 像素盖住抗锯齿边；只在这块形状里、每行用左右两侧紧邻的背景色线性补齐，形状外一个像素都不动。"""
    x0, y0, x1, y1 = bbox; sx, sy = (x1 - x0) / 18, (y1 - y0) / 14
    pts = [(x0 + (x - 3) * sx, y0 + (y - 6) * sy) for x, y in [(3, 20), (10, 6), (14, 13), (17, 9), (21, 20)]]
    mask = Image.new('L', im.size, 0); ImageDraw.Draw(mask).polygon(pts, fill=255)
    mask = mask.filter(ImageFilter.MaxFilter(grow * 2 + 1)); mp = mask.load(); px = im.load(); W, H = im.size
    for y in range(H):
        x = 0
        while x < W:
            if not mp[x, y]: x += 1; continue
            a = x
            while x < W and mp[x, y]: x += 1
            L, R = px[max(0, a - 1), y], px[min(W - 1, x), y]; n = x - a + 1
            for i in range(a, x):
                t = (i - a + 1) / n; px[i, y] = tuple(round(L[c] * (1 - t) + R[c] * t) for c in range(3))


# 6 方形图标：只抹旧山形本身（按原形状还原轮廓，行内左右补色），居中放新图形白色剪影，宽 64%
# 旧山形实测外框（白色像素范围）：512 → 144–367 × 182–355；192 → 55–137 × 69–132；180 → 51–128 × 65–124
for name, S, box in [('icon-512.png', 512, (144, 182, 367, 355)), ('icon-192.png', 192, (55, 69, 137, 132)), ('apple-touch-icon.png', 180, (51, 65, 128, 124))]:
    im = Image.open(SITE / 'art' / 'share' / name).convert('RGB')
    erase_mountain(im, box, 3 if S > 200 else 2)
    m = white_mark(S * 0.64); im = im.convert('RGBA')
    cx, cy = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
    im.alpha_composite(m, (round(cx - m.width / 2), round(cy - m.height / 2))); im.convert('RGB').save(SITE / 'art' / 'share' / name, optimize=True)

def wordmark_png(name, width=None, height=None):
    m = Image.open(TMP / name).convert('RGBA'); m = m.crop(m.getbbox())
    if height: width = m.width * height / m.height
    return m.resize((round(width), round(m.height * width / m.width)), Image.LANCZOS)


# 7 分享图：左上角白色山形（原 77–100 × 74–91）换新图形剪影；「沐仞」不动；「FathomPeak」（原 174–312 × 72–89）换白色字标
og = Image.open(SITE / 'art' / 'share' / 'og-1200x630.png').convert('RGB')
erase_mountain(og, (77, 74, 100, 91), 2)
erase(og, (168, 64, 320, 98), 18)
m = white_mark(31); og = og.convert('RGBA'); og.alpha_composite(m, (round(88.5 - m.width / 2), round(82.5 - m.height / 2)))
wm = wordmark_png('wordmark_white.png', height=13); og.alpha_composite(wm, (174, round(80.5 - wm.height / 2)))
og.convert('RGB').save(SITE / 'art' / 'share' / 'og-1200x630_2026-10-19.png', optimize=True)

print('done:', sorted(p.name for p in OUT.iterdir()), '+ favicon / icons / og')
