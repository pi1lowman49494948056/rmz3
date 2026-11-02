  .include "asm/macros.inc"
  .balign 4, 0
  .section .romext

.global gDshBowGraphic
gDshBowGraphic:
  .4byte gDshBowTiles-.
  .4byte 2368 | (0 << 22)
  .2byte 0, BPP4
gDshBowGraphic_Palettes:

gDshBowTiles:
  .incbin "sprites/dsh_bow/pool.4bpp"

  .balign 4, 0
.global gDshBowMetaSprite
gDshBowMetaSprite:
  .2byte 24
  .byte 28, 0
  .2byte 136
  .byte 27, 0
  .2byte 244
  .byte 27, 0
  .2byte 352
  .byte 27, 0
  .2byte 460
  .byte 27, 0
  .2byte 568
  .byte 28, 0
  .2byte 0x0000
  .byte 237, 207
  .2byte 0x0001
  .byte 229, 215
  .2byte 0x0002
  .byte 237, 215
  .2byte 0x0003
  .byte 245, 215
  .2byte 0x0004
  .byte 253, 215
  .2byte 0x0005
  .byte 229, 223
  .2byte 0x0006
  .byte 237, 223
  .2byte 0x0007
  .byte 245, 223
  .2byte 0x0008
  .byte 253, 223
  .2byte 0x0009
  .byte 5, 223
  .2byte 0x000a
  .byte 229, 231
  .2byte 0x000b
  .byte 237, 231
  .2byte 0x000c
  .byte 245, 231
  .2byte 0x000d
  .byte 253, 231
  .2byte 0x000e
  .byte 5, 231
  .2byte 0x000f
  .byte 229, 239
  .2byte 0x0010
  .byte 237, 239
  .2byte 0x0011
  .byte 245, 239
  .2byte 0x0012
  .byte 253, 239
  .2byte 0x0013
  .byte 5, 239
  .2byte 0x0014
  .byte 229, 247
  .2byte 0x0015
  .byte 237, 247
  .2byte 0x0016
  .byte 245, 247
  .2byte 0x0017
  .byte 253, 247
  .2byte 0x0018
  .byte 5, 247
  .2byte 0x0019
  .byte 245, 255
  .2byte 0x001a
  .byte 253, 255
  .2byte 0x001b
  .byte 5, 255
  .2byte 0x001c
  .byte 237, 207
  .2byte 0x001d
  .byte 229, 215
  .2byte 0x001e
  .byte 237, 215
  .2byte 0x001f
  .byte 245, 215
  .2byte 0x0020
  .byte 253, 215
  .2byte 0x0021
  .byte 229, 223
  .2byte 0x0022
  .byte 237, 223
  .2byte 0x0023
  .byte 245, 223
  .2byte 0x0024
  .byte 253, 223
  .2byte 0x0025
  .byte 5, 223
  .2byte 0x0026
  .byte 229, 231
  .2byte 0x0027
  .byte 237, 231
  .2byte 0x0028
  .byte 245, 231
  .2byte 0x0029
  .byte 253, 231
  .2byte 0x002a
  .byte 5, 231
  .2byte 0x002b
  .byte 229, 239
  .2byte 0x002c
  .byte 237, 239
  .2byte 0x002d
  .byte 245, 239
  .2byte 0x002e
  .byte 253, 239
  .2byte 0x002f
  .byte 5, 239
  .2byte 0x0030
  .byte 237, 247
  .2byte 0x0031
  .byte 245, 247
  .2byte 0x0032
  .byte 253, 247
  .2byte 0x0033
  .byte 5, 247
  .2byte 0x0019
  .byte 245, 255
  .2byte 0x001a
  .byte 253, 255
  .2byte 0x001b
  .byte 5, 255
  .2byte 0x0034
  .byte 237, 207
  .2byte 0x0035
  .byte 229, 215
  .2byte 0x0036
  .byte 237, 215
  .2byte 0x0037
  .byte 245, 215
  .2byte 0x0038
  .byte 253, 215
  .2byte 0x0039
  .byte 229, 223
  .2byte 0x003a
  .byte 237, 223
  .2byte 0x003b
  .byte 245, 223
  .2byte 0x003c
  .byte 253, 223
  .2byte 0x003d
  .byte 5, 223
  .2byte 0x003e
  .byte 229, 231
  .2byte 0x003f
  .byte 237, 231
  .2byte 0x0040
  .byte 245, 231
  .2byte 0x0041
  .byte 253, 231
  .2byte 0x0042
  .byte 5, 231
  .2byte 0x0043
  .byte 229, 239
  .2byte 0x0044
  .byte 237, 239
  .2byte 0x0045
  .byte 245, 239
  .2byte 0x0046
  .byte 253, 239
  .2byte 0x0047
  .byte 5, 239
  .2byte 0x0048
  .byte 237, 247
  .2byte 0x0031
  .byte 245, 247
  .2byte 0x0032
  .byte 253, 247
  .2byte 0x0033
  .byte 5, 247
  .2byte 0x0019
  .byte 245, 255
  .2byte 0x001a
  .byte 253, 255
  .2byte 0x001b
  .byte 5, 255
  .2byte 0x0034
  .byte 237, 207
  .2byte 0x0035
  .byte 229, 215
  .2byte 0x0036
  .byte 237, 215
  .2byte 0x0037
  .byte 245, 215
  .2byte 0x0038
  .byte 253, 215
  .2byte 0x0039
  .byte 229, 223
  .2byte 0x003a
  .byte 237, 223
  .2byte 0x003b
  .byte 245, 223
  .2byte 0x003c
  .byte 253, 223
  .2byte 0x003d
  .byte 5, 223
  .2byte 0x003e
  .byte 229, 231
  .2byte 0x003f
  .byte 237, 231
  .2byte 0x0040
  .byte 245, 231
  .2byte 0x0041
  .byte 253, 231
  .2byte 0x0042
  .byte 5, 231
  .2byte 0x0043
  .byte 229, 239
  .2byte 0x0044
  .byte 237, 239
  .2byte 0x0045
  .byte 245, 239
  .2byte 0x0046
  .byte 253, 239
  .2byte 0x0047
  .byte 5, 239
  .2byte 0x0048
  .byte 237, 247
  .2byte 0x0031
  .byte 245, 247
  .2byte 0x0032
  .byte 253, 247
  .2byte 0x0033
  .byte 5, 247
  .2byte 0x0019
  .byte 245, 255
  .2byte 0x001a
  .byte 253, 255
  .2byte 0x001b
  .byte 5, 255
  .2byte 0x001c
  .byte 237, 207
  .2byte 0x001d
  .byte 229, 215
  .2byte 0x001e
  .byte 237, 215
  .2byte 0x001f
  .byte 245, 215
  .2byte 0x0020
  .byte 253, 215
  .2byte 0x0021
  .byte 229, 223
  .2byte 0x0022
  .byte 237, 223
  .2byte 0x0023
  .byte 245, 223
  .2byte 0x0024
  .byte 253, 223
  .2byte 0x0025
  .byte 5, 223
  .2byte 0x0026
  .byte 229, 231
  .2byte 0x0027
  .byte 237, 231
  .2byte 0x0028
  .byte 245, 231
  .2byte 0x0029
  .byte 253, 231
  .2byte 0x002a
  .byte 5, 231
  .2byte 0x002b
  .byte 229, 239
  .2byte 0x002c
  .byte 237, 239
  .2byte 0x002d
  .byte 245, 239
  .2byte 0x002e
  .byte 253, 239
  .2byte 0x0049
  .byte 5, 239
  .2byte 0x0030
  .byte 237, 247
  .2byte 0x0031
  .byte 245, 247
  .2byte 0x0032
  .byte 253, 247
  .2byte 0x0033
  .byte 5, 247
  .2byte 0x0019
  .byte 245, 255
  .2byte 0x001a
  .byte 253, 255
  .2byte 0x001b
  .byte 5, 255
  .2byte 0x0000
  .byte 237, 207
  .2byte 0x0001
  .byte 229, 215
  .2byte 0x0002
  .byte 237, 215
  .2byte 0x0003
  .byte 245, 215
  .2byte 0x0004
  .byte 253, 215
  .2byte 0x0005
  .byte 229, 223
  .2byte 0x0006
  .byte 237, 223
  .2byte 0x0007
  .byte 245, 223
  .2byte 0x0008
  .byte 253, 223
  .2byte 0x0009
  .byte 5, 223
  .2byte 0x000a
  .byte 229, 231
  .2byte 0x000b
  .byte 237, 231
  .2byte 0x000c
  .byte 245, 231
  .2byte 0x000d
  .byte 253, 231
  .2byte 0x000e
  .byte 5, 231
  .2byte 0x000f
  .byte 229, 239
  .2byte 0x0010
  .byte 237, 239
  .2byte 0x0011
  .byte 245, 239
  .2byte 0x0012
  .byte 253, 239
  .2byte 0x0013
  .byte 5, 239
  .2byte 0x0014
  .byte 229, 247
  .2byte 0x0015
  .byte 237, 247
  .2byte 0x0016
  .byte 245, 247
  .2byte 0x0017
  .byte 253, 247
  .2byte 0x0018
  .byte 5, 247
  .2byte 0x0019
  .byte 245, 255
  .2byte 0x001a
  .byte 253, 255
  .2byte 0x001b
  .byte 5, 255

  .balign 4, 0
.global gDshBowSequence
gDshBowSequence:
  .4byte .+12
  .4byte .+22
  .4byte .+32
  .byte 0, 16
  .byte 1, 16
  .byte 2, 16
  .byte 3, 16
  .byte 4, 16
  .byte 5, 16
  .byte 0, 254
  .byte 0, 16
  .byte 1, 16
  .byte 2, 16
  .byte 3, 16
  .byte 4, 16
  .byte 5, 16
  .byte 0, 254
  .byte 0, 16
  .byte 1, 16
  .byte 2, 16
  .byte 3, 16
  .byte 4, 16
  .byte 5, 16
  .byte 0, 254

  .balign 4, 0
