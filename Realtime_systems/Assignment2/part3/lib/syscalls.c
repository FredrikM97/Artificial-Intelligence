/*
    Part of the Real-Time Embedded Systems course at Halmstad University
    Copyright (c) 2017, Sebastian Kunze <sebastian.kunze@hh.se>
    All rights reserved.
*/

/* Newlib Syscalls */
#include <sys/types.h>
#include <sys/times.h>
#include <sys/stat.h>
#include <unistd.h>
#include <stdlib.h>
/* ================================================================== */

/* misc things */
#include <errno.h>
#undef errno
extern int errno;

char *__env[1] = { 0 };
char **environ = __env;

#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wunused-parameter"

/* memory management */
caddr_t _sbrk(int incr)
{
	extern const void _end, _heap_end;
	static caddr_t heap_ptr = NULL;
	       caddr_t base;

	if(heap_ptr == NULL)
		heap_ptr = (caddr_t)&_end;

	if(((caddr_t)&_heap_end - heap_ptr) >= 0) {
		/* allocate heap */
		base = heap_ptr;
		heap_ptr += incr;
		return base;
	} else {
		/* OOM */
		errno = ENOMEM;
		return ((caddr_t)-1);
	}
}

/* ================================================================== */
/* file handling */
int _open(const char *name, int flags, int mode) { return -1; }
int _close(int fd)                     { return -1; }
int _lseek(int fd, int ptr, int dir)   { return 0; }
int _isatty(int fd)                    { return 1; }
int _stat(char *file, struct stat *st) { st->st_mode = S_IFCHR; return 0; }
int _fstat(int fd, struct stat *st)    { st->st_mode = S_IFCHR; return 0; }
int _link(char *old, char *new)        { errno = EMLINK; return -1; }
int _unlink(char *name)                { errno = ENOENT; return -1; }
/* ================================================================== */

/* process management */
int _getpid(void)                                { return 1; }
int _fork(void)                                  { errno = EAGAIN; return -1; }
int _execve(char* name, char** argv, char** env) { errno = ENOMEM; return -1; }
int _kill(int pid, int sig)                      { errno = EINVAL; return -1; }
int _wait(int *status)                           { errno = ECHILD; return -1; }
int _times(struct tms *buf)                      { return -1; }
void _exit(int status)                           { while(1); }
/* ================================================================== */

#pragma GCC diagnostic pop