OUTPUT_FORMAT("elf32-littlearm", "elf32-bigarm", "elf32-littlearm")
OUTPUT_ARCH(arm)
MEMORY {
    ewram   : ORIGIN = 0x02000000, LENGTH = 4M - 4k
    iwram   : ORIGIN = 0x03000000, LENGTH = 32k
		rom     : ORIGIN = (0x08000000), LENGTH = 32M
}

gMaxLines = 0;
gNumMusicPlayers = 15;

SECTIONS {
	. = 0x2000000;
	ewram (NOLOAD) :
	ALIGN(4)
    {
      INCLUDE "linker/ewram.txt"
      /* DSH demo scratch state lives at the end of ewram. */
      src/weapon/dsh_bow.o (.bss);
    } >ewram = 0x00

	. = 0x3000000;
    iwram (NOLOAD) :
    ALIGN(4)
    {
        src/libs/m4a.o(.bss.code);
        INCLUDE "linker/iwram.txt"
    } >iwram = 0x00

    . = 0x8000000;
    .text :
    ALIGN(4)
    {
      src/rom_header.o (.text);
			src/crt0.o (.text);
			src/sprite2.o (.text);
			src/sprite2.o (.rodata);
			src/sprite2.o (.data);
			src/mmbn4.o (.rodata);
			src/mmbn4.o (.text);
			src/main.o (.text);
			INCLUDE "linker/text.txt"
    } >rom = 0x00

	lib_text :
	ALIGN(4)
	{
		src/libs/m4a_1.o (.text);
		src/libs/m4a.o (.text);
		src/libs/libagbsyscall.o (.text);
		src/libs/agb_sram.o (.text);
		*libgcc.a:*_call_via_rX*.o(.text);
		*libgcc.a:*_divsi3*.o(.text);
		*libgcc.a:*_dvmd_tls*.o(.text);
		*libgcc.a:*_modsi3*.o(.text);
		*libgcc.a:*_udivsi3*.o(.text);
		*libgcc.a:*_umodsi3*.o(.text);
		*libc.a:*memcpy*.o(.text);
		*libc.a:*memset*.o(.text);
	} >rom = 0x00

	.rodata :
	ALIGN(4)
	{
			INCLUDE "linker/rodata.txt"
	} >rom = 0x00

	/*
	  DSH demo extension area.

	  The original image fills the cartridge exactly up to 0x08800000, so any
	  new code or art has to live past that point.  Appending here leaves every
	  existing symbol address unchanged, which is what keeps the still
	  hard-coded absolute addresses in the decompilation valid.
	*/
	.romext :
	ALIGN(4)
	{
			src/weapon/dsh_bow.o (.text);
			src/weapon/dsh_bow.o (.rodata);
			src/weapon/dsh_bow.o (.data);
			src/weapon/dsh_bow_sprite.o (.romext);
            src/weapon/dsh_bow_air_sprite.o (.romext);
			src/weapon/dsh_arrow_art.o (.romext);
            src/weapon/dsh_arrow_art.o (.rodata);
	} >rom = 0x00

    /* Discard everything not specifically mentioned above. */
	/DISCARD/ :
    {
        *(*);
    }
}