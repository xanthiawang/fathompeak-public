"""Procedural isometric line-art for the FathomPeak demo (device / node cube / layer stack), in the
"dark blueprint + glow" style of the reference board (2026-10-12). Colors are CSS variables so the
illustrations follow scheme A/B. Writes demo/art/*.svg and injects them inline into the demo HTML
between <!--art:NAME--> ... <!--/art:NAME--> markers.
Usage: python3 -I isometric_art_2026-10-12.py <demo_dir> [demo_html]"""
import math, os, random, sys

S3 = math.sqrt(3) / 2


def iso(p, s=1.0):
    x, y, z = p
    return ((x - y) * S3 * s, (x + y) * 0.5 * s - z * s)


def poly(pts, cls, extra=''):
    d = ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts)
    return f'<polygon points="{d}" class="{cls}"{extra}/>'


def path(pts, cls, close=False, extra=''):
    d = 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts) + ('Z' if close else '')
    return f'<path d="{d}" class="{cls}"{extra}/>'


class Scene:
    def __init__(self):
        self.items = []  # (layer, svg)

    def add(self, svg, layer=0):
        self.items.append((layer, svg))

    def box(self, x, y, z, w, d, h, s, cls_top='f-top', cls_l='f-left', cls_r='f-right', layer=0, edge='edge'):
        T = [(x, y, z + h), (x + w, y, z + h), (x + w, y + d, z + h), (x, y + d, z + h)]
        R = [(x + w, y, z), (x + w, y + d, z), (x + w, y + d, z + h), (x + w, y, z + h)]
        L = [(x, y + d, z), (x + w, y + d, z), (x + w, y + d, z + h), (x, y + d, z + h)]
        for face, cls in ((L, cls_l), (R, cls_r), (T, cls_top)):
            self.add(poly([iso(p, s) for p in face], f'{cls} {edge}'), layer)

    def face_rect(self, face, x, y, z, u0, v0, u1, v1, s, cls, layer=1):
        """rectangle on a face plane; face in top|right|left; (x,y,z) = cube origin, dims passed via closure"""
        if face == 'top':
            pts = [(x + u0, y + v0, z), (x + u1, y + v0, z), (x + u1, y + v1, z), (x + u0, y + v1, z)]
        elif face == 'right':
            pts = [(x, y + u0, z + v0), (x, y + u1, z + v0), (x, y + u1, z + v1), (x, y + u0, z + v1)]
        else:
            pts = [(x + u0, y, z + v0), (x + u1, y, z + v0), (x + u1, y, z + v1), (x + u0, y, z + v1)]
        self.add(poly([iso(p, s) for p in pts], cls), layer)

    def face_path(self, face, x, y, z, uv, s, cls, layer=1):
        pts = []
        for u, v in uv:
            if face == 'top': pts.append((x + u, y + v, z))
            elif face == 'right': pts.append((x, y + u, z + v))
            else: pts.append((x + u, y, z + v))
        self.add(path([iso(p, s) for p in pts], cls), layer)

    def face_dot(self, face, x, y, z, u, v, s, r, cls, layer=2):
        p = (x + u, y + v, z) if face == 'top' else (x, y + u, z + v) if face == 'right' else (x + u, y, z + v)
        X, Y = iso(p, s)
        self.add(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="{r}" class="{cls}"/>', layer)

    def render(self, vw, vh, pad=24, extra_defs='', bg='dark', title=''):
        # bbox from numbers in the svg fragments
        import re
        xs, ys = [], []
        for _, frag in self.items:
            for m in re.finditer(r'(-?\d+\.\d)[, ](-?\d+\.\d)', frag):
                xs.append(float(m.group(1))); ys.append(float(m.group(2)))
            for m in re.finditer(r'cx="(-?\d+\.\d)" cy="(-?\d+\.\d)"', frag):
                xs.append(float(m.group(1))); ys.append(float(m.group(2)))
        minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
        cw, ch = maxx - minx, maxy - miny
        sc = min((vw - 2 * pad) / cw, (vh - 2 * pad) / ch)
        tx = (vw - cw * sc) / 2 - minx * sc
        ty = (vh - ch * sc) / 2 - miny * sc
        body = '\n'.join(f for _, f in sorted(self.items, key=lambda t: t[0]))
        return f'''<svg viewBox="0 0 {vw} {vh}" class="art art-{bg}" role="img" aria-label="{title}" xmlns="http://www.w3.org/2000/svg">
<defs>
  <pattern id="{bg}-dots" width="14" height="14" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" class="art-dot"/></pattern>
  <filter id="{bg}-glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <filter id="{bg}-soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="14"/></filter>
  {extra_defs}
</defs>
<rect width="{vw}" height="{vh}" class="art-bg"/>
<rect width="{vw}" height="{vh}" fill="url(#{bg}-dots)"/>
<ellipse cx="{vw*0.82:.0f}" cy="{vh*0.12:.0f}" rx="{vw*0.42:.0f}" ry="{vh*0.34:.0f}" class="art-vignette" filter="url(#{bg}-soft)"/>
<g transform="translate({tx:.1f},{ty:.1f}) scale({sc:.3f})">
{body}
</g>
</svg>'''


def device():
    """FPTM-style 一体机: chassis + heatsink fins + ports + status LED."""
    sc = Scene(); s = 1.0
    w, d, h = 150, 92, 34
    # ground shadow
    sh = [iso(p) for p in [(-14, -14, -2), (w + 14, -14, -2), (w + 14, d + 14, -2), (-14, d + 14, -2)]]
    sc.add(poly(sh, 'art-shadow'), -1)
    sc.box(0, 0, 0, w, d, h, s)
    # fins along y on top of chassis
    fw, gap, fh = 5, 7, 20
    n = 12; x0 = (w - (n * fw + (n - 1) * gap)) / 2
    for i in range(n):
        sc.box(x0 + i * (fw + gap), 10, h, fw, d - 20, fh, s, cls_top='f-fin-top', cls_l='f-fin-l', cls_r='f-fin-r', layer=1, edge='edge-thin')
    # ports on right face (x = w): u along y, v along z
    X = w
    for k, (u, pw) in enumerate([(10, 16), (30, 16), (50, 12)]):
        sc.face_rect('right', X, 0, 0, u, 9, u + pw, 21, s, 'port', 2)
        sc.face_rect('right', X, 0, 0, u + 2, 11, u + pw - 2, 19, s, 'port-in', 2)
    for u in (70, 79):
        sc.face_dot('right', X, 0, 0, u, 15, s, 2.4, 'port-round', 2)
    sc.face_dot('right', X, 0, 0, 86, 27, s, 2.0, 'led', 3)
    sc.face_dot('right', X, 0, 0, 86, 27, s, 5.0, 'led-halo', 2)
    # left face: vent slots + label plate
    for i in range(6):
        sc.face_path('left', 0, d, 0, [(14 + i * 7, 8), (14 + i * 7, 26)], s, 'vent', 2)
    sc.face_rect('left', 0, d, 0, 96, 10, 136, 24, s, 'plate', 2)
    # peak mark on plate (brand logo shape)
    sc.face_path('left', 0, d, 0, [(100, 12), (108, 22), (113, 16), (116, 19), (122, 12)], s, 'mark', 3)
    return sc.render(440, 300, pad=34, bg='dark', title='词元一体机 isometric 线稿')


def cube():
    """Compute node at a power station: cube with glowing grid panels (PV array on top) and circuit traces."""
    rng = random.Random(7)
    sc = Scene(); s = 1.0
    a = 124
    sh = [iso(p) for p in [(-16, -16, -2), (a + 16, -16, -2), (a + 16, a + 16, -2), (-16, a + 16, -2)]]
    sc.add(poly(sh, 'art-shadow'), -1)
    sc.box(0, 0, 0, a, a, a, s)
    cell, gapc = 9, 3
    def panel(face, ox, oy, oz, n, m, u0, v0):
        for i in range(n):
            for j in range(m):
                u, v = u0 + i * (cell + gapc), v0 + j * (cell + gapc)
                sc.face_rect(face, ox, oy, oz, u, v, u + cell, v + cell, s, 'cellk', 2)
        W, H = n * cell + (n - 1) * gapc, m * cell + (m - 1) * gapc
        sc.face_rect(face, ox, oy, oz, u0 - 5, v0 - 5, u0 + W + 5, v0 + H + 5, s, 'panel-frame', 1)
        return (u0 - 5, v0 - 5, u0 + W + 5, v0 + H + 5)
    # top: PV array 7x7 ; right & left: 5x5 panels
    ft = panel('top', 0, 0, a, 7, 7, (a - (7 * cell + 6 * gapc)) / 2, (a - (7 * cell + 6 * gapc)) / 2)
    fr = panel('right', a, 0, 0, 5, 5, (a - (5 * cell + 4 * gapc)) / 2, (a - (5 * cell + 4 * gapc)) / 2)
    fl = panel('left', 0, a, 0, 5, 5, (a - (5 * cell + 4 * gapc)) / 2, (a - (5 * cell + 4 * gapc)) / 2)
    # circuit traces: from panel frame edge outward with one right-angle bend, end in a via
    def traces(face, ox, oy, oz, frame, k):
        u0, v0, u1, v1 = frame
        for _ in range(k):
            side = rng.choice('udlr')
            if side == 'u': su, sv, du, dv = rng.uniform(u0 + 6, u1 - 6), v0, 0, -1
            elif side == 'd': su, sv, du, dv = rng.uniform(u0 + 6, u1 - 6), v1, 0, 1
            elif side == 'l': su, sv, du, dv = u0, rng.uniform(v0 + 6, v1 - 6), -1, 0
            else: su, sv, du, dv = u1, rng.uniform(v0 + 6, v1 - 6), 1, 0
            l1 = rng.uniform(8, 18); l2 = rng.uniform(6, 16)
            p1 = (su + du * l1, sv + dv * l1)
            turn = rng.choice([-1, 1])
            p2 = (p1[0] + (dv * turn) * l2, p1[1] + (du * turn) * l2)
            pts = [(su, sv), p1, p2]
            pts = [(min(max(u, 6), a - 6), min(max(v, 6), a - 6)) for u, v in pts]
            sc.face_path(face, ox, oy, oz, pts, s, 'trace', 1)
            sc.face_dot(face, ox, oy, oz, pts[-1][0], pts[-1][1], s, 1.8, 'via', 2)
    traces('top', 0, 0, a, ft, 9); traces('right', a, 0, 0, fr, 7); traces('left', 0, a, 0, fl, 7)
    # corner brackets on the 7 visible vertices
    for p in [(0, 0, a), (a, 0, a), (a, a, a), (0, a, a), (a, 0, 0), (a, a, 0), (0, a, 0)]:
        X, Y = iso(p, s)
        sc.add(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="2.2" class="vertex"/>', 3)
    return sc.render(440, 300, pad=30, bg='dark', title='电站侧算力节点 isometric 线稿')


def stack():
    """Four-layer architecture (BP p14) as translucent stacked plates on a light card."""
    sc = Scene(); s = 1.0
    w = d = 118; t = 5; gap = 24
    layers = [('物理层', '就地转换', 'PHYSICAL'), ('调度层', '计算跟电走', 'SCHEDULING'), ('商业层', '词元分润', 'COMMERCIAL'), ('计量层', '能碳可追溯', 'METERING')]
    for i, (cn, sub, en) in enumerate(layers):
        z = i * gap
        alpha_cls = f'plate-{i}'
        sc.box(0, 0, z, w, d, t, s, cls_top=f'plate-top {alpha_cls}', cls_l=f'plate-side {alpha_cls}', cls_r=f'plate-side {alpha_cls}', layer=i, edge='edge-plate')
        # leader + label: even layers to the right, odd to the left
        if i % 2 == 0:
            ax, ay = iso((w, d / 2, z + t), s); lx = ax + 26; anchor = 'start'
        else:
            ax, ay = iso((w / 2, d, z + t), s); lx = ax - 26; anchor = 'end'
        sc.add(f'<path d="M{ax:.1f},{ay:.1f} L{lx:.1f},{ay:.1f}" class="leader"/><circle cx="{ax:.1f}" cy="{ay:.1f}" r="1.8" class="leader-dot"/>', 9)
        tx = lx + (6 if anchor == 'start' else -6)
        sc.add(f'<text x="{tx:.1f}" y="{ay - 3:.1f}" text-anchor="{anchor}" class="lbl-cn">{cn} · {sub}</text><text x="{tx:.1f}" y="{ay + 9:.1f}" text-anchor="{anchor}" class="lbl-en">{en}</text>', 9)
    return sc.render(440, 300, pad=30, bg='light', title='四层架构：物理、调度、商业、计量')


def inject(html_path, arts):
    src = open(html_path).read()
    for name, svg in arts.items():
        a, b = f'<!--art:{name}-->', f'<!--/art:{name}-->'
        i, j = src.find(a), src.find(b)
        if i < 0 or j < 0:
            print('marker missing:', name); continue
        src = src[:i + len(a)] + '\n' + svg + '\n' + src[j:]
    open(html_path, 'w').write(src)


if __name__ == '__main__':
    demo_dir = sys.argv[1]
    out = os.path.join(demo_dir, 'art'); os.makedirs(out, exist_ok=True)
    arts = {'device': device(), 'cube': cube(), 'stack': stack()}
    arts['cube-m'] = arts['cube'].replace('viewBox="0 0 440 300"', 'viewBox="0 0 440 300"')
    for k, v in arts.items():
        open(os.path.join(out, f'{k}.svg'), 'w').write(v)
        print(k, len(v), 'bytes')
    if len(sys.argv) > 2:
        inject(sys.argv[2], arts); print('injected into', sys.argv[2])
