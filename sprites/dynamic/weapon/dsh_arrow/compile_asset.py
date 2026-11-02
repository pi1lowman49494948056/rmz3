"""Compile the supplied RGBA sprite strip to GBA 4bpp tile data.
No generative redraw: source.png is preserved verbatim. Pillow only decodes it.
Run with Python + Pillow; normal make uses the checked-in arrow.tiles.bin.
"""
from pathlib import Path
from PIL import Image
import json, math
ROOT = Path(__file__).resolve().parent
im = Image.open(ROOT / 'source.png').convert('RGBA')
pix = im.load()
# Fixed source bands include the detached sparks around each projectile.
bands = [(0,850),(850,1450),(1450,im.height)]
bounds=[]
for ya,yb in bands:
    points=[(x,y) for y in range(ya,yb) for x in range(im.width)
            if pix[x,y][3]>32 and max(pix[x,y][:3])>48]
    bounds.append((min(x for x,y in points),min(y for x,y in points),
                   max(x for x,y in points)+1,max(y for x,y in points)+1))
# Stable indices shared by all normal/elemental weapon palettes. No writes to
# the shared palette bank, so the Buster's elemental colors remain untouched.
palette={0:(0,0,0),4:(247,247,247),8:(66,230,0),9:(148,255,123),
         10:(173,255,247),14:(255,239,255),15:(255,255,255)}
scale=min(30/max(b[2]-b[0] for b in bounds),22/max(b[3]-b[1] for b in bounds))
frames=[]
for x0,y0,x1,y1 in bounds:
    cx,cy=(x0+x1)/2,(y0+y1)/2
    frame=[]
    for y in range(24):
        for x in range(32):
            xa,xb=cx+(x-16)/scale,cx+(x+1-16)/scale
            ya,yb=cy+(y-12)/scale,cy+(y+1-12)/scale
            total=alpha=0.0; rgb=[0.,0.,0.]
            for sy in range(max(0,math.floor(ya)),min(im.height,math.ceil(yb))):
                for sx in range(max(0,math.floor(xa)),min(im.width,math.ceil(xb))):
                    weight=max(0,min(xb,sx+1)-max(xa,sx))*max(0,min(yb,sy+1)-max(ya,sy))
                    r,g,b,a=pix[sx,sy]
                    opacity=a/255 if max(r,g,b)>32 else 0
                    total+=weight; alpha+=weight*opacity
                    for k,v in enumerate((r,g,b)): rgb[k]+=weight*opacity*v
            if not total or alpha/total<0.20:
                frame.append(0)
            else:
                color=[v/alpha for v in rgb]
                frame.append(min((k for k in palette if k),key=lambda k:sum((color[j]-palette[k][j])**2 for j in range(3))))
    frames.append(frame)
encoded=bytearray()
for frame in frames:
    for ty in range(3):
        for tx in range(4):
            for y in range(8):
                for x in range(0,8,2):
                    off=(ty*8+y)*32+tx*8+x
                    encoded.append(frame[off] | (frame[off+1]<<4))
assert len(encoded)==1152
(ROOT/'arrow.tiles.bin').write_bytes(encoded)
meta={'label':'gDshArrowMetaSprite','data':[]}
for f in range(3):
    meta['data'].append({'sheetIdx':0,'subsprites':[
        {'tileNum':f*12+r*4,'xflip':False,'yflip':False,'size':[32,8],'x':-16,'y':-12+8*r}
        for r in range(3)]})
(ROOT/'metasprite.json').write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8')
# SVG diagnostic preview comes from the compiled palette indices, not a second
# painted asset. 8x nearest pixel enlargement, three frames side by side.
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="816" height="224" viewBox="0 0 102 28">', '<rect width="102" height="28" fill="#15202b"/>']
for f,frame in enumerate(frames):
    for y in range(24):
        for x in range(32):
            k=frame[y*32+x]
            if k:
                c='#%02x%02x%02x'%palette[k]
                svg.append(f'<rect x="{1+f*34+x}" y="{2+y}" width="1" height="1" fill="{c}"/>')
svg.append('</svg>')
(ROOT/'preview.svg').write_text('\n'.join(svg),encoding='utf-8')
print('Source bounds:', bounds)
print('Compiled: 3 x 32x24, 36 tiles, 1152 bytes; indices:', sorted(set(sum(frames,[]))))
