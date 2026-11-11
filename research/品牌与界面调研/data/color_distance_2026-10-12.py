"""CIEDE2000 distance between FathomPeak colors and competitor primary colors.
Competitor colors are taken from extracted_styles.json (headless Chrome, 2026-10-12)."""
import math, json

def srgb_to_lab(h):
    h = h.lstrip('#'); rgb = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    rgb = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    x = (0.4124 * rgb[0] + 0.3576 * rgb[1] + 0.1805 * rgb[2]) / 0.95047
    y = (0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2])
    z = (0.0193 * rgb[0] + 0.1192 * rgb[1] + 0.9505 * rgb[2]) / 1.08883
    f = lambda t: t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116
    return 116 * f(y) - 16, 500 * (f(x) - f(y)), 200 * (f(y) - f(z))

def de2000(c1, c2):
    L1, a1, b1 = srgb_to_lab(c1); L2, a2, b2 = srgb_to_lab(c2)
    C1, C2 = math.hypot(a1, b1), math.hypot(a2, b2); Cb = (C1 + C2) / 2
    G = 0.5 * (1 - math.sqrt(Cb ** 7 / (Cb ** 7 + 25 ** 7)))
    a1p, a2p = (1 + G) * a1, (1 + G) * a2
    C1p, C2p = math.hypot(a1p, b1), math.hypot(a2p, b2)
    h1p = math.degrees(math.atan2(b1, a1p)) % 360; h2p = math.degrees(math.atan2(b2, a2p)) % 360
    dLp, dCp = L2 - L1, C2p - C1p
    dh = h2p - h1p
    if C1p * C2p == 0: dh = 0
    elif dh > 180: dh -= 360
    elif dh < -180: dh += 360
    dHp = 2 * math.sqrt(C1p * C2p) * math.sin(math.radians(dh / 2))
    Lbp, Cbp = (L1 + L2) / 2, (C1p + C2p) / 2
    if C1p * C2p == 0: hbp = h1p + h2p
    elif abs(h1p - h2p) <= 180: hbp = (h1p + h2p) / 2
    else: hbp = (h1p + h2p + 360) / 2 if h1p + h2p < 360 else (h1p + h2p - 360) / 2
    T = 1 - 0.17 * math.cos(math.radians(hbp - 30)) + 0.24 * math.cos(math.radians(2 * hbp)) + 0.32 * math.cos(math.radians(3 * hbp + 6)) - 0.20 * math.cos(math.radians(4 * hbp - 63))
    dth = 30 * math.exp(-((hbp - 275) / 25) ** 2)
    Rc = 2 * math.sqrt(Cbp ** 7 / (Cbp ** 7 + 25 ** 7))
    Sl = 1 + 0.015 * (Lbp - 50) ** 2 / math.sqrt(20 + (Lbp - 50) ** 2); Sc = 1 + 0.045 * Cbp; Sh = 1 + 0.015 * Cbp * T
    Rt = -math.sin(math.radians(2 * dth)) * Rc
    return math.sqrt((dLp / Sl) ** 2 + (dCp / Sc) ** 2 + (dHp / Sh) ** 2 + Rt * (dCp / Sc) * (dHp / Sh))

competitors = {  # primary / signature colors observed on live sites
    '硅基流动 primary': '#6C28F6', 'PPIO primary': '#1161FE', '无问芯穹 primary': '#5D2BFE',
    'OpenRouter primary': '#7624F4', 'Together orange': '#FC4C02', 'Together dark blue': '#010120',
    'Crusoe hi-vis': '#CEEB13', 'Crusoe dark green': '#323C2A', 'Emerald vivid green': '#438C36',
    'Emerald dark green': '#253023', 'Soluna rust': '#CB5727', 'DeepSeek平台 blue': '#3B82F6',
}
ours = {
    'V1 深海蓝': '#102A43', 'V1 亮蓝': '#176BFA', 'V1 能源青': '#169FB0',
    '官网壳 primary': '#3EA4EC', '官网首页 brand-blue': '#2563EB', '官网首页 cyan': '#06B6D4', '官网首页 green': '#10B981',
}
if __name__ == '__main__':
    out = {}
    for n, c in ours.items():
        ds = sorted(((de2000(c, cc), cn, cc) for cn, cc in competitors.items()))
        out[n] = [(round(d, 1), cn, cc) for d, cn, cc in ds[:3]]
        print(f'{n} {c}: ' + '; '.join(f'{cn} {cc} ΔE={d:.1f}' for d, cn, cc in ds[:3]))
    json.dump(out, open(__file__.replace('.py', '.json'), 'w'), ensure_ascii=False, indent=1)
