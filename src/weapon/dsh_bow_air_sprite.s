  .include "asm/macros.inc"
  .balign 4, 0
  .section .romext

.global gDshBowAirGraphic
gDshBowAirGraphic:
  .4byte gDshBowAirTiles-.
  .4byte 2592 | (0 << 22)
  .2byte 0, BPP4
gDshBowAirGraphic_Palettes:

gDshBowAirTiles:
  .incbin "sprites/dsh_bow_air/pool.4bpp"

  .balign 4, 0
.global gDshBowAirMetaSprite
gDshBowAirMetaSprite:
  .2byte 20
  .byte 34, 0
  .2byte 156
  .byte 34, 0
  .2byte 292
  .byte 34, 0
  .2byte 428
  .byte 33, 0
  .2byte 560
  .byte 27, 0
  .2byte 0x0000
  .byte 234, 196
  .2byte 0x0001
  .byte 242, 196
  .2byte 0x0002
  .byte 226, 204
  .2byte 0x0003
  .byte 234, 204
  .2byte 0x0004
  .byte 242, 204
  .2byte 0x0005
  .byte 250, 204
  .2byte 0x0006
  .byte 2, 204
  .2byte 0x0007
  .byte 226, 212
  .2byte 0x0008
  .byte 234, 212
  .2byte 0x0009
  .byte 242, 212
  .2byte 0x000a
  .byte 250, 212
  .2byte 0x000b
  .byte 2, 212
  .2byte 0x000c
  .byte 10, 212
  .2byte 0x000d
  .byte 226, 220
  .2byte 0x000e
  .byte 234, 220
  .2byte 0x000f
  .byte 242, 220
  .2byte 0x0010
  .byte 250, 220
  .2byte 0x0011
  .byte 2, 220
  .2byte 0x0012
  .byte 10, 220
  .2byte 0x0013
  .byte 226, 228
  .2byte 0x0014
  .byte 234, 228
  .2byte 0x0015
  .byte 242, 228
  .2byte 0x0016
  .byte 250, 228
  .2byte 0x0017
  .byte 2, 228
  .2byte 0x0018
  .byte 10, 228
  .2byte 0x0019
  .byte 234, 236
  .2byte 0x001a
  .byte 242, 236
  .2byte 0x001b
  .byte 250, 236
  .2byte 0x001c
  .byte 2, 236
  .2byte 0x001d
  .byte 10, 236
  .2byte 0x001e
  .byte 242, 244
  .2byte 0x001f
  .byte 250, 244
  .2byte 0x0020
  .byte 2, 244
  .2byte 0x0021
  .byte 10, 244
  .2byte 0x0000
  .byte 234, 196
  .2byte 0x0001
  .byte 242, 196
  .2byte 0x0002
  .byte 226, 204
  .2byte 0x0003
  .byte 234, 204
  .2byte 0x0004
  .byte 242, 204
  .2byte 0x0005
  .byte 250, 204
  .2byte 0x0006
  .byte 2, 204
  .2byte 0x0007
  .byte 226, 212
  .2byte 0x0008
  .byte 234, 212
  .2byte 0x0009
  .byte 242, 212
  .2byte 0x000a
  .byte 250, 212
  .2byte 0x0022
  .byte 2, 212
  .2byte 0x000c
  .byte 10, 212
  .2byte 0x000d
  .byte 226, 220
  .2byte 0x000e
  .byte 234, 220
  .2byte 0x000f
  .byte 242, 220
  .2byte 0x0010
  .byte 250, 220
  .2byte 0x0023
  .byte 2, 220
  .2byte 0x0024
  .byte 10, 220
  .2byte 0x0013
  .byte 226, 228
  .2byte 0x0014
  .byte 234, 228
  .2byte 0x0015
  .byte 242, 228
  .2byte 0x0016
  .byte 250, 228
  .2byte 0x0025
  .byte 2, 228
  .2byte 0x0026
  .byte 10, 228
  .2byte 0x0019
  .byte 234, 236
  .2byte 0x001a
  .byte 242, 236
  .2byte 0x001b
  .byte 250, 236
  .2byte 0x0027
  .byte 2, 236
  .2byte 0x0028
  .byte 10, 236
  .2byte 0x001e
  .byte 242, 244
  .2byte 0x001f
  .byte 250, 244
  .2byte 0x0020
  .byte 2, 244
  .2byte 0x0021
  .byte 10, 244
  .2byte 0x0000
  .byte 234, 196
  .2byte 0x0001
  .byte 242, 196
  .2byte 0x0002
  .byte 226, 204
  .2byte 0x0003
  .byte 234, 204
  .2byte 0x0004
  .byte 242, 204
  .2byte 0x0005
  .byte 250, 204
  .2byte 0x0006
  .byte 2, 204
  .2byte 0x0007
  .byte 226, 212
  .2byte 0x0008
  .byte 234, 212
  .2byte 0x0009
  .byte 242, 212
  .2byte 0x000a
  .byte 250, 212
  .2byte 0x0022
  .byte 2, 212
  .2byte 0x000c
  .byte 10, 212
  .2byte 0x000d
  .byte 226, 220
  .2byte 0x000e
  .byte 234, 220
  .2byte 0x000f
  .byte 242, 220
  .2byte 0x0010
  .byte 250, 220
  .2byte 0x0029
  .byte 2, 220
  .2byte 0x002a
  .byte 10, 220
  .2byte 0x0013
  .byte 226, 228
  .2byte 0x0014
  .byte 234, 228
  .2byte 0x0015
  .byte 242, 228
  .2byte 0x0016
  .byte 250, 228
  .2byte 0x002b
  .byte 2, 228
  .2byte 0x002c
  .byte 10, 228
  .2byte 0x0019
  .byte 234, 236
  .2byte 0x001a
  .byte 242, 236
  .2byte 0x001b
  .byte 250, 236
  .2byte 0x0027
  .byte 2, 236
  .2byte 0x002d
  .byte 10, 236
  .2byte 0x001e
  .byte 242, 244
  .2byte 0x001f
  .byte 250, 244
  .2byte 0x0020
  .byte 2, 244
  .2byte 0x002e
  .byte 10, 244
  .2byte 0x0000
  .byte 234, 196
  .2byte 0x0001
  .byte 242, 196
  .2byte 0x0002
  .byte 226, 204
  .2byte 0x0003
  .byte 234, 204
  .2byte 0x0004
  .byte 242, 204
  .2byte 0x0005
  .byte 250, 204
  .2byte 0x0006
  .byte 2, 204
  .2byte 0x0007
  .byte 226, 212
  .2byte 0x0008
  .byte 234, 212
  .2byte 0x0009
  .byte 242, 212
  .2byte 0x000a
  .byte 250, 212
  .2byte 0x0022
  .byte 2, 212
  .2byte 0x000c
  .byte 10, 212
  .2byte 0x000d
  .byte 226, 220
  .2byte 0x000e
  .byte 234, 220
  .2byte 0x000f
  .byte 242, 220
  .2byte 0x0010
  .byte 250, 220
  .2byte 0x002f
  .byte 2, 220
  .2byte 0x0030
  .byte 10, 220
  .2byte 0x0013
  .byte 226, 228
  .2byte 0x0014
  .byte 234, 228
  .2byte 0x0015
  .byte 242, 228
  .2byte 0x0016
  .byte 250, 228
  .2byte 0x0031
  .byte 2, 228
  .2byte 0x0032
  .byte 10, 228
  .2byte 0x0019
  .byte 234, 236
  .2byte 0x001a
  .byte 242, 236
  .2byte 0x001b
  .byte 250, 236
  .2byte 0x0033
  .byte 2, 236
  .2byte 0x0034
  .byte 10, 236
  .2byte 0x001e
  .byte 242, 244
  .2byte 0x001f
  .byte 250, 244
  .2byte 0x0035
  .byte 2, 244
  .2byte 0x0036
  .byte 226, 204
  .2byte 0x0037
  .byte 234, 204
  .2byte 0x0038
  .byte 242, 204
  .2byte 0x0039
  .byte 250, 204
  .2byte 0x003a
  .byte 2, 204
  .2byte 0x003b
  .byte 226, 212
  .2byte 0x003c
  .byte 234, 212
  .2byte 0x003d
  .byte 242, 212
  .2byte 0x003e
  .byte 250, 212
  .2byte 0x003f
  .byte 2, 212
  .2byte 0x0040
  .byte 10, 212
  .2byte 0x0041
  .byte 18, 212
  .2byte 0x0042
  .byte 234, 220
  .2byte 0x0043
  .byte 242, 220
  .2byte 0x0044
  .byte 250, 220
  .2byte 0x0045
  .byte 2, 220
  .2byte 0x0046
  .byte 10, 220
  .2byte 0x0047
  .byte 18, 220
  .2byte 0x0048
  .byte 234, 228
  .2byte 0x0049
  .byte 242, 228
  .2byte 0x004a
  .byte 250, 228
  .2byte 0x004b
  .byte 2, 228
  .2byte 0x004c
  .byte 10, 228
  .2byte 0x004d
  .byte 242, 236
  .2byte 0x004e
  .byte 250, 236
  .2byte 0x004f
  .byte 2, 236
  .2byte 0x0050
  .byte 2, 244

  .balign 4, 0
.global gDshBowAirSequence
gDshBowAirSequence:
 .4byte .Lair_hold
 .4byte .Lair_exit
 .4byte .Lair_exit
.Lair_hold:
 .byte 0,4,1,4,2,4,3,4,0,254
.Lair_exit:
 .byte 4,2,4,2,0,255
 .balign 4,0
