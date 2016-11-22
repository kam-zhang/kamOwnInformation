#include <stdio.h>
#include <cmath>
#include <cstdlib>
#include "base/BaseTypes.h"
#include "GeneralFunction.h"
using namespace std;

VOID PrintHex(const CHAR* pName, const VOID*p, WORD32 n)
{
    UCHAR * pChar = (UCHAR*)p;
    CHAR Buffer[16];
    UCHAR tab[17] = {'0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f',' '};
    printf("\n%s's Address is 0x%08x, size is %d bytes\n", pName, p, n);
    for(WORD32 i = 0; i < 16; i++)
        printf("%s%c %s%s", (0 == (i%16))?"          |":"", (0 == (i%4))?tab[i]:' ', (3 == (i%4))?" ":"", (15 == (i%16))?"|\n":"");
    for(WORD32 i = 0; i < n; i++)
        printf("%s%02x%s%s", (0 == (i%16))?(sprintf(Buffer,"0x%08x|",(pChar+i)),Buffer):"", *(pChar + i),(3 == (i%4))?" ":"", (15 == (i%16))?"|\n":"");
    printf("\n");
}


