#include "gtest/gtest.h"
#include <iostream>
#include <cmath>
#include <cstdlib>
#include "base/BaseTypes.h"
#include "GeneralFunction.h"
using namespace std;
#define GTEST_MODE  SWITCH_ON
UCHAR b[256] = {0x01,0x23,0x45,0x56};
int main(int argc, char **argv)
{
#if (SWITCH_ON == GTEST_MODE)
    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();	
#else
    WORD32 x = 0xabcd1234;
    WORD32 a[6] = {0x00112233,0x44556677,0x8899aabb,0xccddeeff,0x01234567,0x89abcdef};
    
    MemoryPrint(x);
    MemoryPrint(a);
    MemoryPrint(a[6]);
    MemoryPrint(b);
#endif
}



