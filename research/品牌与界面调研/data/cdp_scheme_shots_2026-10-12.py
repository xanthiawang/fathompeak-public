"""色彩 Demo 三套方案的无头走查：沿用 cdp_extract_2026-10-12.py 的 stdlib CDP 客户端。
每套方案（#A / #B / #C）：桌面 1440 视口加载、收集 Runtime.exceptionThrown / console.error / Log error、整页截图；
再按 gradient_study_2026-10-12.py 的方法对首屏横带逐列取均值、算相邻列的 ΔE2000（检查过渡是否有硬边），结果写 scheme_shots.json。
demo 文件按 artifact 约定以 <title> 开头无 doctype，先包一层带 viewport 的骨架写到输出目录再加载。
用法：python3 cdp_scheme_shots_2026-10-12.py <demo.html> <输出目录>"""
import base64, importlib.util, json, os, socket, struct, subprocess, sys, time, urllib.request
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('cd', os.path.join(HERE, 'color_distance_2026-10-12.py'))
cd = importlib.util.module_from_spec(spec); spec.loader.exec_module(cd)

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PORT = 9341
SKEL = '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body>\n'
W, H = 1440, 900
# 首屏取样区：画板 1 的 .herobg（导航 + 首屏），由页面里的 getBoundingClientRect 给出
RECT_JS = "(function(){var e=document.querySelector('.frame.site .herobg');var r=e.getBoundingClientRect();var nv=e.querySelector('.nav').getBoundingClientRect();var hh=e.querySelector('.hero h1').getBoundingClientRect();return JSON.stringify({x:r.left+window.scrollX,y:r.top+window.scrollY,w:r.width,h:r.height,nav_h:nv.height,h1_top:hh.top-r.top,scheme:document.documentElement.getAttribute('data-scheme'),pressed:[].map.call(document.querySelectorAll('.seg button'),function(b){return b.id+'='+b.getAttribute('aria-pressed')}),paint:document.querySelectorAll('[data-paint] svg').length,sh:document.documentElement.scrollHeight,sw:document.documentElement.scrollWidth,iw:window.innerWidth,title:document.title})})()"


class WS:
    def __init__(self, url):
        host, rest = url.split("//", 1)[1].split("/", 1)
        h, p = host.split(":")
        self.s = socket.create_connection((h, int(p)), timeout=60)
        key = base64.b64encode(os.urandom(16)).decode()
        self.s.sendall((f"GET /{rest} HTTP/1.1\r\nHost: {host}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n"
                        f"Sec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n").encode())
        buf = b""
        while b"\r\n\r\n" not in buf:
            buf += self.s.recv(4096)
        self.buf = buf.split(b"\r\n\r\n", 1)[1]
        self.i = 0; self.events = []

    def send(self, method, params=None):
        self.i += 1
        data = json.dumps({"id": self.i, "method": method, "params": params or {}}).encode()
        hdr = bytearray([0x81]); n = len(data)
        if n < 126: hdr.append(0x80 | n)
        elif n < 65536: hdr.append(0x80 | 126); hdr += struct.pack(">H", n)
        else: hdr.append(0x80 | 127); hdr += struct.pack(">Q", n)
        mask = os.urandom(4)
        self.s.sendall(bytes(hdr) + mask + bytes(b ^ mask[k % 4] for k, b in enumerate(data)))
        while True:
            msg = json.loads(self._recv())
            if msg.get("id") == self.i: return msg
            if "method" in msg: self.events.append(msg)

    def _read(self, n):
        while len(self.buf) < n:
            chunk = self.s.recv(1 << 20)
            if not chunk: raise ConnectionError("closed")
            self.buf += chunk
        out, self.buf = self.buf[:n], self.buf[n:]
        return out

    def _recv(self):
        payload = b""
        while True:
            b1, b2 = self._read(2); n = b2 & 0x7F
            if n == 126: n = struct.unpack(">H", self._read(2))[0]
            elif n == 127: n = struct.unpack(">Q", self._read(8))[0]
            payload += self._read(n)
            if b1 & 0x80: return payload.decode("utf-8", "replace")


def classify(events):
    errs, logs = [], []
    for ev in events:
        m, p = ev["method"], ev.get("params", {})
        if m == "Runtime.exceptionThrown":
            d = p.get("exceptionDetails", {}); e = d.get("exception", {})
            errs.append("exception: " + (e.get("description") or d.get("text") or "?")[:300])
        elif m == "Runtime.consoleAPICalled" and p.get("type") in ("error", "warning", "assert"):
            errs.append(p["type"] + ": " + " ".join(str(a.get("value", a.get("description", ""))) for a in p.get("args", []))[:300])
        elif m == "Log.entryAdded" and p.get("entry", {}).get("level") in ("error", "warning"):
            logs.append(p["entry"]["level"] + " " + p["entry"].get("source", "") + ": " + p["entry"].get("text", "")[:200] + " " + p["entry"].get("url", "")[:120])
    return errs, logs


def hexc(c): return '#%02X%02X%02X' % tuple(int(round(float(v))) for v in c)


def strip_stats(arr, axis):
    """只含背景的条带：沿 axis 取均值后算相邻 ΔE2000（硬拼会出现尖峰）。axis=0 → 逐列（左→右），axis=1 → 逐行（上→下）。"""
    m = arr.mean(axis=axis); n = m.shape[0]
    stops = [hexc(m[int(p * (n - 1))]) for p in (0, .25, .5, .75, 1)]
    d = [cd.de2000(hexc(m[i]), hexc(m[i + 1])) for i in range(n - 1)]
    return dict(stops=stops, max_adjacent_dE=round(max(d), 2), mean_adjacent_dE=round(float(np.mean(d)), 3), total_dE=round(float(np.sum(d)), 1))


def sample_background(png, info):
    """首屏里不含文字与图板的区域：底部留白一条（左→右）、左侧留白一条（上→下，导航以下）；C 另加油画横带本体。"""
    arr = np.asarray(Image.open(png).convert('RGB')).astype(np.float32)
    H, W = arr.shape[0], arr.shape[1]; nav = int(info.get('nav_h', 52)); h1 = int(info.get('h1_top', 0))
    out = dict(bottom_strip_L2R=strip_stats(arr[H - 36:H - 4, :, :], 0),
               left_gutter_T2B=strip_stats(arr[nav + 2:H - 2, 4:24, :], 1))
    if h1 > nav + 120:  # 方案 C：横带在导航与标题之间露出，取其本体
        out['paint_band_L2R'] = strip_stats(arr[nav + 6:min(nav + 150, h1 - 8), :, :], 0)
        out['paint_band_fade_T2B'] = strip_stats(arr[nav + 2:h1 - 4, 4:24, :], 1)
    return out


def sample_band(png, rect, scale):
    """gradient_study 的方法：对首屏区域逐列 / 逐行取均值，给 0/25/50/75/100% 的停靠色和相邻列的最大 ΔE2000。"""
    im = Image.open(png).convert('RGB'); arr = np.asarray(im).astype(np.float32)
    x0, y0 = int(rect['x'] * scale), int(rect['y'] * scale); x1, y1 = x0 + int(rect['w'] * scale), y0 + int(rect['h'] * scale)
    hero = arr[y0:y1, x0:x1, :]
    col = hero.mean(axis=0); row = hero.mean(axis=1)
    Wc, Hr = col.shape[0], row.shape[0]
    stops_h = [hexc(col[int(p * (Wc - 1))]) for p in (0, .25, .5, .75, 1)]
    stops_v = [hexc(row[int(p * (Hr - 1))]) for p in (0, .25, .5, .75, 1)]
    # 相邻列 / 行均值的 ΔE2000：硬拼会在某一列跳出一个尖峰
    d_cols = [cd.de2000(hexc(col[i]), hexc(col[i + 1])) for i in range(Wc - 1)]
    d_rows = [cd.de2000(hexc(row[i]), hexc(row[i + 1])) for i in range(Hr - 1)]
    return dict(left_to_right=stops_h, top_to_bottom=stops_v,
                max_adjacent_col_dE=round(max(d_cols), 2), max_adjacent_row_dE=round(max(d_rows), 2),
                p99_col_dE=round(float(np.percentile(d_cols, 99)), 2), p99_row_dE=round(float(np.percentile(d_rows, 99)), 2))


def main(html_path, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    wrapped = os.path.join(out_dir, "wrapped.html")
    with open(wrapped, "w", encoding="utf-8") as f:
        f.write(SKEL + open(html_path, encoding="utf-8").read() + "\n</body></html>")
    url0 = "file://" + os.path.abspath(wrapped)
    prof = os.path.join(out_dir, ".chrome-profile")
    proc = subprocess.Popen([CHROME, "--headless=new", f"--remote-debugging-port={PORT}", f"--user-data-dir={prof}",
                             "--hide-scrollbars", f"--window-size={W},{H}", "--lang=zh-CN", "--allow-file-access-from-files", "about:blank"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    results = {}
    try:
        for _ in range(50):
            try: urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/version", timeout=1); break
            except Exception: time.sleep(0.2)
        req = urllib.request.Request(f"http://127.0.0.1:{PORT}/json/new?about:blank", method="PUT")
        tab = json.loads(urllib.request.urlopen(req).read())
        ws = WS(tab["webSocketDebuggerUrl"])
        try:
            ws.send("Emulation.setDeviceMetricsOverride", {"width": W, "height": H, "deviceScaleFactor": 1, "mobile": False})
            ws.send("Page.enable"); ws.send("Runtime.enable"); ws.send("Log.enable")
            for scheme in ("A", "B", "C"):
                ws.events = []
                for attempt in range(2):  # 偶发 Connection reset（大页 + SVG 滤镜），重开一个 tab 再来一次
                    try:
                        ws.send("Page.navigate", {"url": "about:blank"}); time.sleep(0.3)   # 同一 URL 只换 hash 不会重新加载，先去 about:blank
                        ws.send("Page.navigate", {"url": url0 + "#" + scheme}); time.sleep(3.5)  # 等 Google Fonts 与首屏动画
                        ws.send("Runtime.evaluate", {"expression": "window.scrollTo(0,0)"}); time.sleep(0.3)
                        break
                    except (ConnectionError, OSError) as e:
                        print(f"   retry #{scheme} after {e!r}"); time.sleep(1.5)
                        req = urllib.request.Request(f"http://127.0.0.1:{PORT}/json/new?about:blank", method="PUT")
                        tab = json.loads(urllib.request.urlopen(req).read()); ws = WS(tab["webSocketDebuggerUrl"]); ws.events = []
                        ws.send("Emulation.setDeviceMetricsOverride", {"width": W, "height": H, "deviceScaleFactor": 1, "mobile": False})
                        ws.send("Page.enable"); ws.send("Runtime.enable"); ws.send("Log.enable")
                r = ws.send("Runtime.evaluate", {"expression": RECT_JS, "returnByValue": True})
                val = r.get("result", {}).get("result", {}).get("value")
                info = json.loads(val) if isinstance(val, str) else {"error": str(r)[:300]}
                ws.send("Runtime.evaluate", {"expression": "1"})
                errs, logs = classify(ws.events)
                scale = 0.6; h = min(int(info.get("sh", H)), 9000)
                shot = ws.send("Page.captureScreenshot", {"format": "png", "clip": {"x": 0, "y": 0, "width": W, "height": h, "scale": scale}, "captureBeyondViewport": True})
                png = os.path.join(out_dir, f"scheme_{scheme}_desktop_1440.png")
                if "result" in shot: open(png, "wb").write(base64.b64decode(shot["result"]["data"]))
                # 首屏单独再截一张 1:1，供取样与近看
                hero = ws.send("Page.captureScreenshot", {"format": "png", "clip": {"x": info["x"], "y": info["y"], "width": info["w"], "height": info["h"], "scale": 1}, "captureBeyondViewport": True})
                hpng = os.path.join(out_dir, f"scheme_{scheme}_hero.png")
                if "result" in hero: open(hpng, "wb").write(base64.b64decode(hero["result"]["data"]))
                band = sample_band(hpng, dict(x=0, y=0, w=info["w"], h=info["h"]), 1) if os.path.exists(hpng) else None
                bg = sample_background(hpng, info) if os.path.exists(hpng) else None
                results[scheme] = dict(info=info, js_errors=errs, log=logs, png=os.path.basename(png), hero_png=os.path.basename(hpng), hero_band=band, background=bg,
                                       overflow=bool(info.get("sw", 0) > info.get("iw", 0) + 1))
                flag = "OK " if not errs and not results[scheme]["overflow"] else "!! "
                print(f"{flag}#{scheme} scheme={info.get('scheme')} pressed={info.get('pressed')} paint_svgs={info.get('paint')} sh={info.get('sh')} sw={info.get('sw')}/{info.get('iw')} errs={len(errs)} log={len(logs)}")
                for e in errs: print("    ", e)
                for l in logs: print("    ", l)
                for k, v in (bg or {}).items(): print(f"     {k:22s} stops {v['stops']} max adj ΔE {v['max_adjacent_dE']} mean {v['mean_adjacent_dE']} total {v['total_dE']}")
                if band: print(f"     hero L>R {band['left_to_right']} T>B {band['top_to_bottom']} max adj ΔE col {band['max_adjacent_col_dE']} row {band['max_adjacent_row_dE']} (p99 {band['p99_col_dE']}/{band['p99_row_dE']})")
        finally:
            try: urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json/close/{tab['id']}")
            except Exception: pass
        results["captured_at"] = time.strftime("%Y-%m-%d %H:%M:%S %z")
        json.dump(results, open(os.path.join(out_dir, "scheme_shots.json"), "w"), ensure_ascii=False, indent=1)
    finally:
        proc.terminate()


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
