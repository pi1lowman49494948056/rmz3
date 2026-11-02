#!/usr/bin/env python3
"""Compile the bounded spacecraft demo room. No third-party dependencies."""
import argparse
import json
from pathlib import Path
import re
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]
LC = 'src/stage/spacecraft/landscape.c'
BIN = 'data/stage/spacecraft/screen.bin'
SCRIPT = 'src/data/scripts/spacecraft.inc'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def array(source, name):
    match = re.search(r'(' + name + r'\[[^\]]*\]\s*=\s*\{)(.*?)(\};)', source, re.S)
    require(match is not None, 'Missing array: ' + name)
    body = re.sub(r'//[^\n]*', '', match[2])
    # Split expressions first: the header contains (1 << 5) - 1.
    cells = [x.strip() for x in body.split(',') if x.strip()]
    require(len(cells) == 420, name + ': expected header + 416 cells')
    return match, cells[:4], [int(x, 0) for x in cells[4:]]


def replace_array(source, name, header, values):
    match, _, _ = array(source, name)
    body = '\n  ' + ', '.join(header) + ',\n'
    body += ''.join('  ' + ', '.join(hex(v) for v in values[r*32:(r+1)*32]) + ',\n' for r in range(13))
    return source[:match.start(2)] + body + source[match.end(2):]


def generate(root=ROOT):
    config = json.loads((root/'tools/dsh/room.json').read_text(encoding='utf-8-sig'))
    require(config['schema_version'] == 1, 'Unsupported schema_version')
    lines = (root/'tools/dsh/map.txt').read_text(encoding='utf-8-sig').splitlines()
    require(bool(lines), 'Empty map')
    w, h = len(lines[0]), len(lines)
    require(w > 0 and all(len(x) == w for x in lines), 'Uneven map rows')
    require(w % 15 == 0 and h % 10 == 0, 'Dimensions must be multiples of 15 x 10')
    require(all(set(x) <= {'.', '#'} for x in lines), 'Only . and # are supported')
    ox, oy = config['origin_chunk']; walls = config['wall_columns']
    require(all(type(v) is int for v in [ox, oy, walls]), 'Origin/wall values must be integers')
    cols, rows = w//15, h//10
    require(0 <= ox and 0 <= oy and ox+cols <= 32 and oy+rows <= 13, 'Room exceeds 32 x 13 chunk grid')
    require(1 <= walls < w//2, 'Invalid wall thickness')
    require(all(row[:walls] == '#'*walls and row[-walls:] == '#'*walls for row in lines), 'Left/right walls must be closed')
    require(lines[-1] == '#'*w, 'Bottom must be closed for this demo')
    left, top = ox*240, oy*160
    right, bottom = left+w*16-walls*16, top+h*16
    left += walls*16
    require(right-left >= 240, 'Playable width must fit one screen')

    def landing(point, label):
        x, y = point
        require(type(x) is int and type(y) is int, label + ': integer pixels required')
        require(walls*16+8 <= x < (w-walls)*16-8 and 32 <= y < h*16, label + ': outside safe room bounds')
        # Feet on a 16px boundary; conservative standing clearance, 16px wide/32px high.
        require(y % 16 == 0, label + ': feet Y must align to a metatile top')
        for cx in range((x-8)//16, (x+7)//16+1):
            require(lines[y//16][cx] == '#', label + ': no solid floor')
            require(all(lines[cy][cx] == '.' for cy in range((y-32)//16, y//16)), label + ': body intersects terrain')
        return ox*240+x, top+y

    spawn = landing(config['spawn_px'], 'spawn')
    target = landing(config['teleport']['target_px'], 'teleport target')
    trigger = config['teleport']['trigger_left_px']
    require(type(trigger) is int, 'Trigger must be integer pixels')
    trigger += ox*240
    require(left <= trigger < right, 'Trigger outside room')
    require(spawn[0] < trigger and target[0] < trigger, 'Spawn/target must be outside trigger region')
    require(any(row[(trigger-ox*240)//16:(right-ox*240)//16].count('.') for row in lines), 'Trigger has no empty cells')

    baseline = (root/'tools/dsh/baseline/landscape.c.txt').read_text(encoding='utf8')
    screen = bytearray((root/'tools/dsh/baseline/screen.bin').read_bytes())
    require(len(screen) % 300 == 0 and len(screen)//300 <= 256, 'Invalid chunk pool')
    _, header, cmap = array(baseline, 'sChunkMap1')
    null = int(header[1], 0)
    # Outside the demo is inaccessible; do not retain obsolete room geometry on resize.
    result_map = [null]*416
    # Preserve every chunk used by decorative layers, plus sentinel chunks.
    protected = {0, null}
    for name in ['sChunkMap2', 'sChunkMap3']:
        protected.update(array(baseline, name)[2])
    n = len(screen)//300
    free = [i for i in range(n) if i not in protected]
    existing = {bytes(screen[i*300:(i+1)*300]): i for i in range(n) if i != null}
    allocated = {}
    unique = {}
    # Reserve exact matches before assigning any new data.
    screens = []
    for r in range(rows):
        for c in range(cols):
            data = struct.pack('<150H', *[int(lines[r*10+y][c*15+x] == '#') for y in range(10) for x in range(15)])
            screens.append(data)
    reserved = {existing[d] for d in screens if d in existing}
    free = [i for i in free if i not in reserved]
    for index, data in enumerate(screens):
        if data not in unique:
            if data in existing:
                cid = existing[data]
            else:
                require(bool(free), 'Insufficient unshared chunk IDs; simplify layout (no files written)')
                cid = free.pop(0)
            unique[data] = cid
            allocated[cid] = data
            screen[cid*300:(cid+1)*300] = data
        r, c = divmod(index, cols)
        result_map[(oy+r)*32+ox+c] = unique[data]
    source = (root/LC).read_text(encoding='utf8')
    source = replace_array(source, 'sChunkMap1', header, result_map)
    for name, val in [('sScreenBehavior', 0x0102), ('sTilesetOffset', 0x01)]:
        _, hdr, grid = array(baseline, name)
        if name == 'sScreenBehavior':
            grid = [(v & 0x0fff) | 0xf000 for v in grid]
        for r in range(oy, oy+rows):
            for c in range(ox, ox+cols): grid[r*32+c] = val
        source = replace_array(source, name, hdr, grid)
    scripts = (root/SCRIPT).read_text(encoding='utf8')
    pattern = r'(Camera_0834d268:.*?\.2byte[^\n]*\n)\s*\.4byte[^\n]*'
    scripts, count = re.subn(pattern, lambda m:m[1]+'  .4byte '+', '.join(str(x)+'*PX' for x in [left,right,top,bottom]), scripts, count=1, flags=re.S)
    require(count == 1, 'Camera template not found')
    scripts, count = re.subn(r'(Entity_ZeroSpaceCraftStartPoint:[^\n]*\n\s*\.byte[^\n]*\n)\s*\.4byte[^\n]*', lambda m:m[1]+f'  .4byte {spawn[0]}*PX, {spawn[1]}*PX', scripts, count=1)
    require(count == 1, 'Spawn template not found')
    values = dict(DSH_ROOM_RIGHT=right, DSH_ROOM_TOP=top, DSH_ROOM_BOTTOM=bottom,
                  DSH_TRIGGER_X=trigger, DSH_TARGET_X=target[0], DSH_TARGET_Y=target[1],
                  DSH_TARGET_CAMERA_Y=max(top+80,min(bottom-80,target[1])))
    hdr = '/* Generated by tools/dsh/map_editor.py; edit room.json instead. */\n#ifndef DSH_ROOM_CONFIG_H\n#define DSH_ROOM_CONFIG_H\n'
    hdr += ''.join(f'#define {k} {v}\n' for k,v in values.items())+'#endif\n'
    outputs = {root/LC:source.encode(), root/BIN:bytes(screen), root/SCRIPT:scripts.encode(), root/'include/dsh_room_config.h':hdr.encode()}
    summary = f'{w}x{h} metatiles; {cols}x{rows} screens; {len(unique)} unique chunks; bounds {left},{top}..{right},{bottom}; spawn {spawn}; target {target}'
    return outputs, summary


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Validate and check generated files without writing')
    args=parser.parse_args()
    try:
        outputs, summary=generate()
        changed=[p for p,b in outputs.items() if not p.exists() or p.read_bytes()!=b]
        print(summary)
        if args.check:
            require(not changed, 'Generated files are stale: '+', '.join(str(p.relative_to(ROOT)) for p in changed))
            print('PASS: configuration and generated files agree');return
        # All parsing, collision, bounds and capacity checks finish before the first write.
        for p in changed:
            tmp=p.with_name(p.name+'.dsh-tmp');tmp.write_bytes(outputs[p]);tmp.replace(p)
        print(f'Synchronized {len(changed)} files. Now build rmz3.gba.')
    except (ValueError, KeyError, TypeError, OSError) as e:
        print('ERROR:', e, file=sys.stderr);sys.exit(1)


if __name__ == '__main__': main()
