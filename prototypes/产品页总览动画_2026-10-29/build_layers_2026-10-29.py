"""Partition the supplied RGBA illustration; never redraw or invent hidden geometry."""
from pathlib import Path
import hashlib
import json
import subprocess
import tempfile
from PIL import Image, ImageDraw
import numpy as np

BASE = Path(__file__).resolve().parent
SOURCE = BASE / 'engineering-stack_2026-10-14.png'
# Lower visible rim, traced in the original 1254 x 1254 coordinate system.
# The narrow downward steps retain the exposed connecting pipes with their upper tier.
BOUNDARIES = [
 [(0,246),(276,246),(568,397),(568,456),(612,456),(612,420),(697,465),(997,305),(1254,305)],
 [(0,504),(275,504),(570,660),(570,698),(615,717),(615,684),(700,715),(996,557),(1254,557)],
 [(0,744),(247,744),(603,928),(603,993),(647,982),(647,952),(718,988),(1008,838),(1254,838)]
]

def main():
 try:
  source=Image.open(SOURCE).convert('RGBA')
  assert source.size == (1254,1254), source.size
  pixels=np.array(source)
  owner=np.full((1254,1254),3,dtype=np.uint8)
  for i,edge in reversed(list(enumerate(BOUNDARIES))):
   mask=Image.new('L',source.size)
   ImageDraw.Draw(mask).polygon([(0,0),(1254,0),*reversed(edge)],fill=255)
   owner[np.array(mask)>0]=i
  out=BASE/'layers'; out.mkdir(exist_ok=True)
  combined=np.zeros_like(pixels)
  sizes=[]
  masks=[]
  for i in range(4):
   mask = owner == i
   # Retain genuine source pixels for 12 px below each original cut.
   expanded = mask.copy()
   if i < 3:
    for dy in range(1, 13):
     expanded[dy:] |= mask[:-dy]
   masks.append(expanded)
   layer=pixels.copy(); layer[~expanded]=0
   dest=out/f'layer-{i}.webp'
   with tempfile.TemporaryDirectory(prefix='ov-layer-') as tmp:
    intermediate=Path(tmp)/'layer.png'
    Image.fromarray(layer).save(intermediate)
    subprocess.run(['cwebp','-quiet','-near_lossless','40','-m','6',str(intermediate),'-o',str(dest)],check=True)
   decoded=np.array(Image.open(dest).convert('RGBA'))
   decoded[layer[:,:,3]<16]=layer[layer[:,:,3]<16]
   decoded[:,:,3]=layer[:,:,3]  # Preserve the original antialiasing and exact ownership.
   decoded[decoded[:,:,3]==0]=0
   Image.fromarray(decoded).save(dest,'WEBP',lossless=True,exact=True,method=6)
   combined[owner==i]=decoded[owner==i]
   sizes.append(dest.stat().st_size)
  # Check the cut masks (not source transparency) throughout a sampled cycle.
  # ease-in-out has slope < 2: adjacent displacement <= 18/3.6 * 2 * .8 = 8 px.
  # 12 px bleed exceeds this bound plus raster rounding; no cut-mask gap can open.
  def ease(x):
   lo, hi = 0., 1.
   for _ in range(35):
    t = (lo + hi) / 2
    bx = 3*(1-t)**2*t*.42 + 3*(1-t)*t*t*.58 + t**3
    if bx < x: lo = t
    else: hi = t
   return 3*(1-t)*t*t + t**3
  uncovered = 0
  for time in np.linspace(0, 7.2, 145):
   coverage = np.zeros_like(owner, dtype=bool)
   for i, mask in enumerate(masks):
    phase = ((time + i*.8) % 7.2) / 3.6
    displacement = -9 + 18*ease(phase) if phase <= 1 else 9 - 18*ease(phase-1)
    dy = round(displacement)
    if dy > 0: coverage[dy:] |= mask[:-dy]
    elif dy < 0: coverage[:dy] |= mask[-dy:]
    else: coverage |= mask
   uncovered += int(np.count_nonzero(~coverage[20:-20]))
  assert uncovered == 0, f'Cut-mask gaps: {uncovered}'
  visible=pixels[:,:,3]>0
  assert np.array_equal(combined[:,:,3],pixels[:,:,3]), 'Alpha reconstruction mismatch'
  rgb_error=np.abs(combined[:,:,:3].astype(int)-pixels[:,:,:3].astype(int))[visible]
  max_error=int(rgb_error.max())
  assert sum(sizes)<=650_000, f'Image budget exceeded: {sum(sizes)}'
  report={'source':SOURCE.name,'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
          'source_mtime':SOURCE.stat().st_mtime,'dimensions':list(source.size),
          'encoding':'near-lossless WebP 40, original size, exact source alpha, 12px downward overlapping ownership masks',
          'layer_bytes':sizes,'total_bytes':sum(sizes),'original_owner_alpha_mismatches':0,'cut_mask_cycle_samples':145,'cut_mask_uncovered_pixels':uncovered,'adjacent_motion_bound_px':8,'max_visible_rgb_channel_error':max_error,'mean_visible_rgb_channel_error':float(rgb_error.mean()),
          'bleed_down_px':12,'boundaries':BOUNDARIES}
  (out/'manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
  print(json.dumps(report,ensure_ascii=False))
 except Exception as exc:
  raise SystemExit(f'Layer export failed: {exc}') from exc

if __name__=='__main__': main()
