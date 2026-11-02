# Neon arrow asset

source.png is the unmodified user-provided 727x2164 RGBA strip, pointing left.
compile_asset.py reads it and produces arrow.tiles.bin (1152 bytes), metasprite.json, and preview.svg.
Run with Python + Pillow only when replacing the source. Normal builds consume the checked-in binary directly.
Three 32x24 frames, 12 tiles/frame, three 32x8 subsprites/frame. All frames use sheetIdx 0 and tile offsets 0/12/24.
Palette indices are restricted to stable colors in the existing weapon palette. No shared palette writes.
DM109 is the shield graphics slot. VRAM usage is 36 of its 48 tiles; ROM data is placed in the extension section.
The old sheet/0.png is a retained legacy asset and is no longer referenced by dsh_arrow_art.s.
