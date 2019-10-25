/*
    Part of the Real-Time Embedded Systems course at Halmstad University
    Copyright (c) 2016, Sebastian Kunze <sebastian.kunze@hh.se>
    All rights reserved.
*/

/* Startup code for Raspberry Pi 3 */
#include <stdint.h>
#include <string.h>

__asm__ (
	/* declare function */
	".section .startup\n"
	".global Entry\n"
	".type Entry, %function\n"
	"Entry:\n"

	/* stack pointer values */
	".equ ISTACK, 0x7000\n"		/* interrupt stack */
	".equ STACK,  0x8000\n"		/* application stack */

#if 0
	/* set up stack pointers */
	"    mov r0, #0xD2\n"
	"    msr cpsr_c, r0\n"
	"    mov sp, #ISTACK\n"
	"    mov r0, #0xD3\n"
	"    msr cpsr_c, r0\n"
#endif
	"    mov sp, #STACK\n"

	/* enable L1 cache */
	"    mrc p15, 0, r0, c1, c0, 0\n"
	"    orr r0, #0x1800\n"
	"    orr r0, #0x4\n"
	"    mcr p15, 0, r0, c1, c0, 0\n"

#if 0
	/* enable VFP */
	"    mrc p15, #0, r1, c1, c0, #2\n"
	"    orr r1, r1, #(0xf << 20)\n"
	"    mcr p15, #0, r1, c1, c0, #2\n"
	"    mov r1, #0\n"
	"    mcr p15, #0, r1, c7, c5, #4\n"
	"    mov r0, #0x40000000\n"
	"    fmxr fpexc, r0\n"
#endif

	/* jump to C startup */
	"    bl SystemInit\n"
	"1:\n"
	"    b 1b\n"
);

void SystemInit(void)
{
	extern char _sbss, _ebss;

	typedef void (*func)(void);
	extern func __preinit_array_start[], __preinit_array_end;
	extern func __init_array_start[], __init_array_end;
	extern func __fini_array_start[], __fini_array_end;

	extern int main();

	/* clear .bss */
	memset(&_sbss, 0, &_ebss - &_sbss);

	/* call preinit_array */
	for(int i = 0; i < &__preinit_array_end - __preinit_array_start; i++)
		__preinit_array_start[i]();

	/* call static constructors */
	for(int i = 0; i < &__init_array_end - __init_array_start; i++)
		__init_array_start[i]();

	/* call main */
	main();

	/* call static destructors */
	for(int i = &__fini_array_end - __fini_array_start - 1; i >= 0; i--)
		__fini_array_start[i]();

	/* and never return */
	while(1) {
		__asm__ volatile("CPSID I");
		__asm__ volatile("WFI");
	}
}