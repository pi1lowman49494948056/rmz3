#!/usr/bin/env python3
"""DSH demo - bow placeholder (CORRECTED).

Draws a vertical bow into Zero's standing shield-guard frames (0/1/2) in the
*assembled* metasprite coordinate space, then inverse-maps each pixel back to
the sheet using the GBA 1D tile layout.  This avoids the scramble caused by
drawing directly in the linear sheet space.

Colors (Zero's palette): 1 = dark outline, 2 = dark blue, 5 = white.
"""
import math, pathlib, shutil
from PIL import Image

ROOT = pathlib.Path(r"E:\rmz3\rmz3\sprites\dynamic\zero\shield\shield")
SHEET = ROOT / "sheet" / "0.png"
shutil.copyfile(SHEET.with_suffix(".png.bak"), SHEET)  # restore original

import json
ms = json.loads((ROOT / "metasprite.json").read_text(encoding="utf-8"))

img = Image.open(SHEET).convert("P")
PER_ROW = img.width // 8  # tiles per row (4)

# Clear shield tiles: 20..33 (sheet rows 5..8, y=40..72).
for y in range(40, 72):
    for x in range(0, 32):
        img.putpixel((x, y), 0)

def set_px(mx, my, color):
    """Set a pixel at metasprite anchor coords (mx,my), routing through the
    frame's subsprites into the sheet."""
    for s in subs:
        w, h = s["size"]
        if s["x"] <= mx < s["x"] + w and s["y"] <= my < s["y"] + h:
            rx, ry = mx - s["x"], my - s["y"]
            c, r = rx // 8, ry // 8
            tile = s["tileNum"] + r * (w // 8) + c
            sx = (tile % PER_ROW) * 8 + (rx % 8)
            sy = (tile // PER_ROW) * 8 + (ry % 8)
            img.putpixel((sx, sy), color)
            return

# Vertical bow in metasprite space: shield occupies x=0..16, y=-26..-10.
# String on the right, arc bulging left, arrow across the middle.
STRING_X = 13
CY = -18.0
R = 10
def bow_pixels():
    for my in range(-25, -11):        # string (vertical, 2px thick)
        set_px(STRING_X, my, 1)
        set_px(STRING_X + 1, my, 5)
    for my in range(-26, -10):        # arc (left limb)
        dy = my - CY
        if abs(dy) <= R:
            dx = int(round(math.sqrt(R * R - dy * dy)))
            x = STRING_X - dx
            set_px(x, my, 2)
            set_px(x + 1, my, 1)
    for mx in range(3, STRING_X + 1):  # arrow
        set_px(mx, int(CY), 5)

# Frame 0/2: 16x16 shield.  Frame 1: two 8x16 pieces; draw the same bow across them.
for fi in (0, 1, 2):
    subs = ms["data"][fi]["subsprites"]
    bow_pixels()

img.save(SHEET)
print(f"corrected bow drawn into {SHEET}")
