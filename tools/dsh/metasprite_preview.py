#!/usr/bin/env python3
"""DSH demo - assemble Zero's shield-guard metasprites into per-frame previews.

Reads metasprite.json + sheet/*.png, assembles each of the 7 frames (GBA OBJ 1D
tile mapping: a [w,h] subsprite at tileNum T uses T..T+(w/8)(h/8)-1, laid out
row-major) and writes frame_N.png into tools/dsh/preview/.

Purpose: give the artist an exact reference of body/arm/shield tile positions
before redrawing the shield as a bow.
"""
import json, pathlib, sys
from PIL import Image

# Usage: metasprite_preview.py [sprite_dir_rel_to_zero]  (default shield/shield)
motion = sys.argv[1] if len(sys.argv) > 1 else "shield/shield"
ROOT = pathlib.Path(r"E:\rmz3\rmz3\sprites\dynamic\zero") / motion
OUT = pathlib.Path(r"E:\rmz3\rmz3\tools\dsh\preview") / motion.replace("/", "_")
OUT.mkdir(parents=True, exist_ok=True)

ms = json.loads((ROOT / "metasprite.json").read_text(encoding="utf-8"))
# collect sheet count from the highest sheetIdx
nsheet = 1 + max(f["sheetIdx"] for f in ms["data"])
sheets = [Image.open(ROOT / f"sheet/{i}.png").convert("RGBA") for i in range(nsheet)]

TILE = 8

def tile_pixels(sheet, tile_num):
    per_row = sheet.width // TILE
    x = (tile_num % per_row) * TILE
    y = (tile_num // per_row) * TILE
    return sheet.crop((x, y, x + TILE, y + TILE))

composites = []
for fi, frame in enumerate(ms["data"]):
    sheet = sheets[frame["sheetIdx"]]
    subs = frame["subsprites"]
    # bounding box (in the anchor coordinate space)
    minx = min(s["x"] for s in subs)
    miny = min(s["y"] for s in subs)
    maxx = max(s["x"] + s["size"][0] for s in subs)
    maxy = max(s["y"] + s["size"][1] for s in subs)
    pad = 8
    w, h = maxx - minx + 2 * pad, maxy - miny + 2 * pad
    canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for s in subs:
        tw, th = s["size"][0] // TILE, s["size"][1] // TILE
        for r in range(th):
            for c in range(tw):
                t = s["tileNum"] + r * tw + c
                px = pad - minx + s["x"] + c * TILE
                py = pad - miny + s["y"] + r * TILE
                canvas.paste(tile_pixels(sheet, t), (px, py))
    canvas.save(OUT / f"frame_{fi}.png")
    composites.append(canvas)
    print(f"frame {fi}: {len(subs)} subsprites, canvas {w}x{h}")

# composite sheet (all 7 side by side)
cw = sum(c.width for c in composites)
ch = max(c.height for c in composites)
comp = Image.new("RGBA", (cw, ch), (255, 255, 255, 255))
x = 0
for c in composites:
    comp.paste(c, (x, 0))
    x += c.width
comp.save(OUT / "all_frames.png")
print(f"wrote {OUT} (frame_0..6.png + all_frames.png)")
