#include "gtest/gtest.h"
#include <iostream>
#include <cmath>
#include <cstdlib>
#include "base/BaseTypes.h"
#include "GeneralFunction.h"
using namespace std;
#define GTEST_MODE  SWITCH_OFF
#define LogPrintf(a) cout<<(a)<<'\n'

struct fruit
{
	virtual void eat(){LogPrintf("eat fruit");}
};
struct apple : fruit
{
	void eat(){LogPrintf("eat apple");}
};
struct orange : fruit
{
	
};
int main(int argc, char **argv)
{
#if (SWITCH_ON == GTEST_MODE)
    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();	
#else
    fruit f;
	apple app;
	orange ora;
    MemoryPrint(f);
	MemoryPrint(app);
	MemoryPrint(ora);

	f.eat();
	app.eat();
	ora.eat();
#endif
}



