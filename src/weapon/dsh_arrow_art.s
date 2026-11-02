	.include "asm/macros.inc"

@ DSH demo: hand-built sprite set for the bow arrow, living in the extension
@ area so its size is not constrained by any retail sprite sheet.
@
@ The motion slot it takes over is DM109 (originally sprites/dynamic/weapon/
@ unk_109).  Only the table entries that point at it are rewritten; the retail
@ sheet itself stays in place, so no existing symbol moves.

	.section .romext
	.balign 4, 0

	.global gDshArrowGraphic
gDshArrowGraphic:
	.4byte gDshArrowTiles-. @ src (self relative)
	.4byte 1152 | (48 << 22) @ bytesize | destination VRAM tile
	.2byte 128, BPP4 @ rowsize (unused), props

gDshArrowTiles:
	.incbin "sprites/dynamic/weapon/dsh_arrow/arrow.tiles.bin"

	.include "sprites/dynamic/weapon/dsh_arrow/metasprite.inc"
	.include "sprites/dynamic/weapon/dsh_arrow/sequence.inc"
