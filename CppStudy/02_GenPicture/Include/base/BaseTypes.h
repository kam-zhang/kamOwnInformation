#ifndef INCL_BaseTypes_H_
#define INCL_BaseTypes_H_

typedef unsigned char  BYTE;
typedef char CHAR;
typedef char SCHAR;
typedef unsigned char UCHAR;

typedef unsigned short WORD;
typedef unsigned short WORD16;
typedef signed short   SWORD16;

typedef unsigned long  DWORD;
typedef unsigned int   WORD32;
typedef signed long    SWORD32;

#ifndef WIN32
    typedef unsigned long long WORD64;
#else
    typedef unsigned long long WORD64;
#endif
#define SWITCH_ON   1
#define SWITCH_OFF 0

#define SUCCESS 0
#define FAILURE -1

#define PRIVATE static
#define PUBLIC extern

#ifndef VOID
#define VOID void
#endif
#ifndef NULL
#define NULL ((VOID*)0)
#endif

#endif
