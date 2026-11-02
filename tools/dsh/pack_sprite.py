#!/usr/bin/env python3
"""DSH demo - pack a full-frame sprite sheet into GBA sprite data.

Input : PNG sheet, N frames stacked vertically (frame = W x H, H multiple of N).
Output: <outdir>/pool.4bpp        deduplicated 8x8 tiles (4bpp)
        <outdir>/bow_sprite.s     graphic header + metasprite + sequence (.romext)

Palette: opaque pixels remapped to the nearest of Zero's 16-colour palette;
index 0 = transparent.  Anchor: bottom-centre (fw8/2, fh-8).
"""
import argparse, pathlib, json
from PIL import Image

ZERO_PAL = [
    (74, 148, 148), (65, 74, 65), (0, 41, 106), (65, 98, 139),
    (148, 180, 213), (255, 255, 255), (222, 131, 16), (255, 189, 0),
    (255, 238, 131), (255, 213, 172), (156, 16, 65), (213, 32, 90),
    (255, 82, 98), (255, 164, 139), (148, 255, 123), (139, 172, 57),
]

def nearest_pal(rgb):
    # User bow energy green; rendered via a pose-scoped palette override.
    if rgb[1] > 100 and rgb[1] > rgb[0] * 1.3 and rgb[1] > rgb[2] * 1.3:
        return 14
    best, bi = 1 << 30, 1
    for i in range(1, 16):
        c = ZERO_PAL[i]
        d = (rgb[0]-c[0])**2 + (rgb[1]-c[1])**2 + (rgb[2]-c[2])**2
        if d < best:
            best, bi = d, i
    return bi

def tile_4bpp(px, x0, y0):
    out = bytearray()
    for y in range(8):
        for x in range(0, 8, 2):
            out.append((px[y0+y][x0+x] & 0xF) | ((px[y0+y][x0+x+1] & 0xF) << 4))
    return bytes(out)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--outdir", default=r"E:\rmz3\rmz3\sprites\dsh_bow")
    ap.add_argument("--frames", type=int, default=3)
    ap.add_argument("--frame-h", type=int, default=56)
    ap.add_argument("--dur", type=int, default=8, help="ticks per frame in the sequence")
    args = ap.parse_args()

    outdir = pathlib.Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    im = Image.open(args.input).convert("RGBA")
    W, H = im.size
    fh, n = args.frame_h, args.frames
    assert H == fh * n, f"height {H} != {fh}*{n}"
    fw8 = W + ((8 - W % 8) % 8)

    frames = []
    src = im.load()
    for f in range(n):
        rows = []
        for y in range(fh):
            row = []
            for x in range(fw8):
                if x >= W:
                    row.append(0)
                    continue
                r, g, b, a = src[x, f*fh + y]
                # Treat the game's transparent teal (74,148,148) as index 0 too:
                # indexed PNGs store transparency as that colour with alpha=255.
                if a == 0 or (abs(r - 74) < 10 and abs(g - 148) < 10 and abs(b - 148) < 10):
                    row.append(0)
                else:
                    row.append(nearest_pal((r, g, b)))
            rows.append(row)
        frames.append(rows)

    pool, pool_index, frame_subs = [], {}, []
    for rows in frames:
        subs = []
        for row in range(fh // 8):
            for col in range(fw8 // 8):
                data = tile_4bpp(rows, col*8, row*8)
                if all(b == 0 for b in data):
                    continue
                if data not in pool_index:
                    pool_index[data] = len(pool)
                    pool.append(data)
                subs.append((pool_index[data], col, row))
        frame_subs.append(subs)

    (outdir / "pool.4bpp").write_bytes(b"".join(pool))

    # Auto anchor: bottom-centre, based on the actual content bottom (not the
    # frame bottom, since the sheet may have empty padding rows).  -4 matches
    # the existing Zero body (whose lowest pixel sits at sprite y=+4).
    ax = fw8 // 2
    content_bottom = 0
    for rows in frames:
        for y in range(fh):
            if any(v != 0 for v in rows[y]):
                content_bottom = y
    ay = content_bottom - 4
    # Optional asset-specific pivot; keep it next to the input PNG so
    # re-importing the same art does not silently reset its alignment.
    anchor_path = pathlib.Path(args.input).with_suffix(".anchor.json")
    if anchor_path.exists():
        anchor = json.loads(anchor_path.read_text(encoding="utf-8"))
        ax, ay = anchor["x"], anchor["y"]
        if type(ax) is not int or type(ay) is not int:
            raise ValueError("Anchor x/y must be integers")

    # metasprite: frame header (offset u16, count u8, sheet u8) + subsprite (u16 tile, x s8, y s8)
    nf = len(frame_subs)
    hdr = bytearray()
    body = bytearray()
    for subs in frame_subs:
        off = nf * 4 + len(body)
        hdr += bytes([off & 0xFF, (off >> 8) & 0xFF, len(subs) & 0xFF, 0])
        for (ti, col, row) in subs:
            x = col*8 - ax
            y = row*8 - ay
            body += bytes([ti & 0xFF, (ti >> 8) & 0xFF, x & 0xFF, y & 0xFF])

    pool_size = len(pool) * 32
    seq_pairs = (nf + 1) * 2  # (frame,dur) for each frame + one hold, per group
    g0 = 12
    g1 = g0 + seq_pairs
    g2 = g1 + seq_pairs

    L = []
    L.append('  .include "asm/macros.inc"')
    L.append('  .balign 4, 0')
    L.append('  .section .romext')
    L.append('')
    L.append('.global gDshBowGraphic')
    L.append('gDshBowGraphic:')
    L.append('  .4byte gDshBowTiles-.')
    L.append(f'  .4byte {pool_size} | (0 << 22)')
    L.append('  .2byte 0, BPP4')
    L.append('gDshBowGraphic_Palettes:')
    L.append('')
    L.append('gDshBowTiles:')
    L.append(f'  .incbin "{(outdir / "pool.4bpp").as_posix()}"')
    L.append('')
    L.append('  .balign 4, 0')
    L.append('.global gDshBowMetaSprite')
    L.append('gDshBowMetaSprite:')
    for f in range(nf):
        off = int.from_bytes(hdr[f*4:f*4+2], "little")
        L.append(f'  .2byte {off}')
        L.append(f'  .byte {hdr[f*4+2]}, 0')
    for i in range(0, len(body), 4):
        u16 = int.from_bytes(body[i:i+2], "little")
        x, y = body[i+2], body[i+3]
        L.append(f'  .2byte 0x{u16:04x}')
        L.append(f'  .byte {x}, {y}')
    L.append('')
    L.append('  .balign 4, 0')
    L.append('.global gDshBowSequence')
    L.append('gDshBowSequence:')
    L.append(f'  .4byte .+12')
    L.append(f'  .4byte .+{g1 - 4}')
    L.append(f'  .4byte .+{g2 - 8}')
    for _ in range(3):
        for f in range(nf):
            L.append(f'  .byte {f}, {args.dur}')
        L.append('  .byte 0, 254')
    L.append('')
    L.append('  .balign 4, 0')

    (outdir / "bow_sprite.s").write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"frames={nf} pool_tiles={len(pool)} bytes={pool_size} anchor=({ax},{ay})")
    print("subs per frame:", [len(s) for s in frame_subs])

if __name__ == "__main__":
    main()
