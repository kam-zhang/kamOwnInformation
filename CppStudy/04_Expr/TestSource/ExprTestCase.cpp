#include <iostream>
#include "gtest/gtest.h"
#include "Expr.h"
#include <time.h>
using namespace std;

TEST(Expr_TestSuit1, 2_Add_4_should_be_6)
{
    ASSERT_TRUE(6 == Expr("2+4"));
}
TEST(Expr_TestSuit1, 5_sub_6_should_be_negative_1)
{
    ASSERT_TRUE(-1 == Expr("5-6"));
}

TEST(Expr_TestSuit1, 2_Add_4_Sub_3_should_be_3)
{
    ASSERT_TRUE(3 == Expr("2+4-3"));
}

TEST(Expr_TestSuit1, 2_Add_4_mul_3_should_be_14)
{
    ASSERT_TRUE(14 == Expr("2+4*3"));
}
TEST(Expr_TestSuit1, 2_Add_9_div_3_should_be_5)
{
    ASSERT_TRUE(5 == Expr("2+9/3"));
}
TEST(Expr_TestSuit1, 2_Add_9_mod_5_should_be_6)
{
    ASSERT_TRUE(6 == Expr("2+9%5"));
}
TEST(Expr_TestSuit1, 2_mul_3_add_3_should_be_9)
{
    ASSERT_TRUE(2*3+3 == Expr("2*3+3"));
}
TEST(Expr_TestSuit1, 2_add_2_mul_3_add_3_should_be_11)
{
    ASSERT_TRUE(2+2*3+3 == Expr("2+2*3+3"));
}

TEST(Expr_TestSuit1, 2_add_2_mul_3_div_3_mul_8_mod_3_add_3_should_be_6)
{
    ASSERT_TRUE(2+2*3/3*8%3+3 == Expr("2+2*3/3*8%3+3"));
}
TEST(Expr_TestSuit1, 2_add_2_mul_3_div_3_add_8_mod_3_add_3_should_be_9)
{
    ASSERT_TRUE(2+2*3/3+8%3+3 == Expr("2+2*3/3+8%3+3"));
}
TEST(Expr_TestSuit1, 2_should_be_2)
{
    ASSERT_TRUE(2 == Expr("2"));
}
TEST(Expr_TestSuit1, 2_sub_9_add_2_mul_3_div_3_add_8_mod_3_add_3_sub_9_should_be_negative_9)
{
    ASSERT_TRUE(2-9+2*3/3+8%3+3-9 == Expr("2-9+2*3/3+8%3+3-9"));
}
TEST(Expr_TestSuit1, 3_Power_4_should_be_81)
{
    ASSERT_TRUE(81 == Expr("3@4"));
}
TEST(Expr_TestSuit1, 2_mul_9_mod_5_should_be_3)
{
    ASSERT_TRUE(2*9%5 == Expr("2*9%5"));
}

TEST(Expr_TestSuit1, 2_add_3_sub_9_mod_5_should_be_1)
{
    ASSERT_TRUE(2+3-9%5 == Expr("2+3-9%5"));
}

TEST(Expr_TestSuit1, 2_add_3_power_2_sub_5_should_be_6)
{
    ASSERT_TRUE(6 == Expr("2+3@2-5"));
}
TEST(Expr_TestSuit1, 2_add_3_mul_5_power_3_div_6_sub_5_should_be_59)
{
    ASSERT_TRUE(59 == Expr("2+3*5@3/6-5"));
}
TEST(Expr_TestSuit1, 2_add_3_mul_5_power_3_add_6_sub_5_should_be_378)
{
    ASSERT_TRUE(378 == Expr("2+3*5@3+6-5"));
}
TEST(Expr_TestSuit1, 2_sub_2_add_3_mul_4_div_2_mul_5_power_3_mod_2_add_6_sub_5_should_be_1)
{
    ASSERT_TRUE(1 == Expr("2-2+3*4/2*5@3%2+6-5"));
}
TEST(Expr_TestSuit1, 2_sub_2_add_3_mul_4_div_2_add_5_power_3_mod_2_add_6_sub_5_should_be_8)
{
    ASSERT_TRUE(8 == Expr("2-2+3*4/2+5@3%2+6-5"));
}
TEST(Expr_TestSuit1, TestRunTime)
{
    long RunTime;
    long StartTime = clock();

    for(int i=0; i < 100000;i++)
        Expr("2+9%5");
    RunTime = clock() - StartTime;
    cout<<"RunTime is "<<((double)RunTime/(CLOCKS_PER_SEC/10))<<"us/Time"<<endl;
}



