"""Sample real pixel gradients from competitor hero screenshots (captured 2026-10-12).
For each site: mean colour per column (left→right) and per row (top→bottom) over the hero area, dominant colours,
and a composite PNG: hero crop + two ramp bars + hex stops.
Usage: python3 -I gradient_study_2026-10-12.py <research_dir> [key ...]
With keys given, only those sites are (re)sampled and merged into gradient_stops.json; _all.png is skipped.
2026-10-13: added Dia Early Birds (source of the final 晨昏蓝 horizon) and the final prototype hero (v26)."""
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw

R = sys.argv[1]
OUT = os.path.join(R, 'gradient_study'); os.makedirs(OUT, exist_ok=True)

# key, name, source file, hero rows (y0, y1) in that file's pixel space
SITES = [
    ('fp', '沐仞现网', 'screenshots/00_fathompeak_cn.png', (70, 560)),
    ('sf', '硅基流动', 'screenshots/01_siliconflow.png', (70, 700)),
    ('ppio', 'PPIO', 'screenshots/02_ppio.png', (70, 760)),
    ('infini', '无问芯穹', 'screenshots/03_infini.png', (60, 780)),
    ('or', 'OpenRouter', 'screenshots/04_openrouter.png', (60, 700)),
    ('tg', 'Together', 'screenshots/05_together.png', (60, 760)),
    ('crusoe', 'Crusoe', 'screenshots/06_crusoe.png', (40, 820)),
    ('emerald', 'Emerald', 'screenshots/07_emerald.png', (60, 880)),
    ('soluna', 'Soluna', 'screenshots/08_soluna.png', (60, 760)),
    ('ds', 'DeepSeek 平台', 'data/09_deepseek_platform_long.png', (0, 520)),
    ('zhipu', '智谱', 'extra/zhipu_home_long.png', (40, 480)),
    ('kimi', 'Kimi 平台', 'extra/moonshot_home_long.png', (40, 480)),
    ('lifewire', 'LifeWire 现网', 'lifewire/lw_home_long.png', (60, 560)),
    ('earlybirds', 'Dia Early Birds（晨昏蓝来源）', 'b2b/dia_earlybirds_top.png', (0, 900)),
    ('fp_final', '沐仞定稿首屏 · 晨昏蓝 v26', 'demo/color_scheme_shots/final_B_hero_2026-10-13.png', (0, 900)),
]
ONLY = set(sys.argv[2:])
if ONLY:
    SITES = [s for s in SITES if s[0] in ONLY]

def hexc(c): return '#%02X%02X%02X' % tuple(int(round(v)) for v in c)

def dominant(arr, k=6):
    q = (arr // 24) * 24 + 12
    flat = q.reshape(-1, 3)
    keys, counts = np.unique(flat, axis=0, return_counts=True)
    order = np.argsort(-counts)[:k]
    tot = flat.shape[0]
    return [(hexc(keys[i]), round(float(counts[i]) / tot * 100, 1)) for i in order]

results = {}
rows_img = []
for key, name, rel, (y0, y1) in SITES:
    im = Image.open(os.path.join(R, rel)).convert('RGB')
    arr = np.asarray(im).astype(np.float32)
    hero = arr[y0:y1, :, :]
    col = hero.mean(axis=0)          # W x 3  (left -> right)
    row = hero.mean(axis=1)          # H x 3  (top -> bottom)
    W, H = col.shape[0], row.shape[0]
    stops_h = [hexc(col[int(p * (W - 1))]) for p in (0, .25, .5, .75, 1)]
    stops_v = [hexc(row[int(p * (H - 1))]) for p in (0, .25, .5, .75, 1)]
    dom = dominant(hero.astype(np.int32))
    results[key] = dict(name=name, source=rel, hero_rows=[y0, y1], left_to_right=stops_h, top_to_bottom=stops_v, dominant=dom)

    # composite: hero crop (520 wide) | ramps (520 wide): H-bar, V-bar, labels
    hw = 520; hh = int(hw * (y1 - y0) / W)
    crop = im.crop((0, y0, W, y1)).resize((hw, hh))
    canvas = Image.new('RGB', (hw * 2 + 60, max(hh, 170) + 30), 'white')
    canvas.paste(crop, (10, 20))
    d = ImageDraw.Draw(canvas)
    x0 = hw + 40
    # horizontal ramp bar drawn from per-column means
    for i in range(hw):
        c = col[int(i * (W - 1) / (hw - 1))]
        d.line([(x0 + i, 40), (x0 + i, 80)], fill=tuple(int(v) for v in c))
    for i in range(hw):
        c = row[int(i * (H - 1) / (hw - 1))]
        d.line([(x0 + i, 110), (x0 + i, 150)], fill=tuple(int(v) for v in c))
    d.text((x0, 24), 'left -> right (mean per column)', fill=(60, 60, 60))
    d.text((x0, 94), 'top -> bottom (mean per row)', fill=(60, 60, 60))
    for j, p in enumerate((0, .25, .5, .75, 1)):
        x = x0 + int(p * (hw - 1)); d.text((min(x, x0 + hw - 60), 82), stops_h[j], fill=(40, 40, 40)); d.text((min(x, x0 + hw - 60), 152), stops_v[j], fill=(40, 40, 40))
    d.text((10, 4), f'{key}  {name}  {rel}  rows {y0}-{y1}', fill=(0, 0, 0))
    canvas.save(os.path.join(OUT, f'{key}.png'))
    rows_img.append(canvas)

if not ONLY:
    # stacked sheet
    w = max(i.width for i in rows_img); h = sum(i.height for i in rows_img)
    sheet = Image.new('RGB', (w, h), 'white'); y = 0
    for i in rows_img:
        sheet.paste(i, (0, y)); y += i.height
    sheet.save(os.path.join(OUT, '_all.png'))
else:
    jp = os.path.join(OUT, 'gradient_stops.json')
    if os.path.exists(jp):
        old = json.load(open(jp)); old.update(results); results = old
json.dump(results, open(os.path.join(OUT, 'gradient_stops.json'), 'w'), ensure_ascii=False, indent=1)
for k, v in results.items():
    print(f"{k:8s} L>R {v['left_to_right']}  T>B {v['top_to_bottom']}  dom {v['dominant'][:4]}")
