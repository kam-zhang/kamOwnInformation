#include "gtest/gtest.h"
#include "MyFunction.h"
using namespace std;

TEST(MyFunctionTest, 2_Add_4_should_be_6)
{
    ASSERT_TRUE(6 == MyFunction().Add(2,4));
}
TEST(MyFunctionTest, n7_Add_2_should_be_n5)
{
    ASSERT_TRUE(-5 == MyFunction().Add(-7,2));   
}
TEST(MyFunctionTest, n1_Add_n2_should_be_n3)
{
    ASSERT_TRUE(-3 == MyFunction().Add(-1,-2));   
}