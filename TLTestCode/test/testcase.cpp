#include <testngpp/internal/TestCase.h>
#include <testngpp/internal/TestFixtureDesc.h>
#include <testngpp/internal/TestSuiteDesc.h>
#include <testngpp/internal/DataDriven.h>
#include "salaryTestCase.xpp"

static struct TESTCASE_TestsalaryTest_test_7
   : public TESTNGPP_NS::TestCase
{
   TESTCASE_TestsalaryTest_test_7()
      : TESTNGPP_NS::TestCase
        ( "when QingWen work for JiaZheng in october salary should be 4200"
        , "salaryTest"
        , "testcase"
        , 0
        , "salaryTestCase.xpp"
        , 7)
   {}

   void setFixture(TESTNGPP_NS::TestFixture* fixture)
   {
      if(fixture == 0)
      {
         belongedFixture = new TestsalaryTest();
      }
      else
      {
         belongedFixture = dynamic_cast<TestsalaryTest*>(fixture);
      }
   }

   void runTest()
   {
      
belongedFixture->test_7()
;
   }

   TESTNGPP_NS::TestFixture* getFixture() const
   {
      return belongedFixture;
   }

   unsigned int numberOfTags() const
   {
      return 0;
   }

   const char** getTags() const
   {
      static const char* tags[] = {0};
      return tags;
   }

   const char* getMemCheckSwitch() const
   {
      static const char* memCheckSwitch = "none";
      return memCheckSwitch;
   }

private:
   TestsalaryTest* belongedFixture;
} testcase_instance_TestsalaryTest_test_7 ;



static struct TESTCASE_TestsalaryTest_test_12
   : public TESTNGPP_NS::TestCase
{
   TESTCASE_TestsalaryTest_test_12()
      : TESTNGPP_NS::TestCase
        ( "when QingWen work for JiaBaoyu in March salary should be 11200"
        , "salaryTest"
        , "testcase"
        , 0
        , "salaryTestCase.xpp"
        , 12)
   {}

   void setFixture(TESTNGPP_NS::TestFixture* fixture)
   {
      if(fixture == 0)
      {
         belongedFixture = new TestsalaryTest();
      }
      else
      {
         belongedFixture = dynamic_cast<TestsalaryTest*>(fixture);
      }
   }

   void runTest()
   {
      
belongedFixture->test_12()
;
   }

   TESTNGPP_NS::TestFixture* getFixture() const
   {
      return belongedFixture;
   }

   unsigned int numberOfTags() const
   {
      return 0;
   }

   const char** getTags() const
   {
      static const char* tags[] = {0};
      return tags;
   }

   const char* getMemCheckSwitch() const
   {
      static const char* memCheckSwitch = "none";
      return memCheckSwitch;
   }

private:
   TestsalaryTest* belongedFixture;
} testcase_instance_TestsalaryTest_test_12 ;



static struct TESTCASE_TestsalaryTest_test_16
   : public TESTNGPP_NS::TestCase
{
   TESTCASE_TestsalaryTest_test_16()
      : TESTNGPP_NS::TestCase
        ( "when SheYue work for JiaMu in june salary should be 6000"
        , "salaryTest"
        , "testcase"
        , 0
        , "salaryTestCase.xpp"
        , 16)
   {}

   void setFixture(TESTNGPP_NS::TestFixture* fixture)
   {
      if(fixture == 0)
      {
         belongedFixture = new TestsalaryTest();
      }
      else
      {
         belongedFixture = dynamic_cast<TestsalaryTest*>(fixture);
      }
   }

   void runTest()
   {
      
belongedFixture->test_16()
;
   }

   TESTNGPP_NS::TestFixture* getFixture() const
   {
      return belongedFixture;
   }

   unsigned int numberOfTags() const
   {
      return 0;
   }

   const char** getTags() const
   {
      static const char* tags[] = {0};
      return tags;
   }

   const char* getMemCheckSwitch() const
   {
      static const char* memCheckSwitch = "none";
      return memCheckSwitch;
   }

private:
   TestsalaryTest* belongedFixture;
} testcase_instance_TestsalaryTest_test_16 ;



static struct TESTCASE_TestsalaryTest_test_20
   : public TESTNGPP_NS::TestCase
{
   TESTCASE_TestsalaryTest_test_20()
      : TESTNGPP_NS::TestCase
        ( "when SheYue work for WangFuren in october salary should be 3000"
        , "salaryTest"
        , "testcase"
        , 0
        , "salaryTestCase.xpp"
        , 20)
   {}

   void setFixture(TESTNGPP_NS::TestFixture* fixture)
   {
      if(fixture == 0)
      {
         belongedFixture = new TestsalaryTest();
      }
      else
      {
         belongedFixture = dynamic_cast<TestsalaryTest*>(fixture);
      }
   }

   void runTest()
   {
      
belongedFixture->test_20()
;
   }

   TESTNGPP_NS::TestFixture* getFixture() const
   {
      return belongedFixture;
   }

   unsigned int numberOfTags() const
   {
      return 0;
   }

   const char** getTags() const
   {
      static const char* tags[] = {0};
      return tags;
   }

   const char* getMemCheckSwitch() const
   {
      static const char* memCheckSwitch = "none";
      return memCheckSwitch;
   }

private:
   TestsalaryTest* belongedFixture;
} testcase_instance_TestsalaryTest_test_20 ;



static struct TESTCASE_TestsalaryTest_test_24
   : public TESTNGPP_NS::TestCase
{
   TESTCASE_TestsalaryTest_test_24()
      : TESTNGPP_NS::TestCase
        ( "when XiRen work for JiaZheng in Sep salary should be 8000"
        , "salaryTest"
        , "testcase"
        , 0
        , "salaryTestCase.xpp"
        , 24)
   {}

   void setFixture(TESTNGPP_NS::TestFixture* fixture)
   {
      if(fixture == 0)
      {
         belongedFixture = new TestsalaryTest();
      }
      else
      {
         belongedFixture = dynamic_cast<TestsalaryTest*>(fixture);
      }
   }

   void runTest()
   {
      
belongedFixture->test_24()
;
   }

   TESTNGPP_NS::TestFixture* getFixture() const
   {
      return belongedFixture;
   }

   unsigned int numberOfTags() const
   {
      return 0;
   }

   const char** getTags() const
   {
      static const char* tags[] = {0};
      return tags;
   }

   const char* getMemCheckSwitch() const
   {
      static const char* memCheckSwitch = "none";
      return memCheckSwitch;
   }

private:
   TestsalaryTest* belongedFixture;
} testcase_instance_TestsalaryTest_test_24 ;



static struct TESTCASE_TestsalaryTest_test_28
   : public TESTNGPP_NS::TestCase
{
   TESTCASE_TestsalaryTest_test_28()
      : TESTNGPP_NS::TestCase
        ( "when XiRen work for JiaBaoyu in october salary should be 28000"
        , "salaryTest"
        , "testcase"
        , 0
        , "salaryTestCase.xpp"
        , 28)
   {}

   void setFixture(TESTNGPP_NS::TestFixture* fixture)
   {
      if(fixture == 0)
      {
         belongedFixture = new TestsalaryTest();
      }
      else
      {
         belongedFixture = dynamic_cast<TestsalaryTest*>(fixture);
      }
   }

   void runTest()
   {
      
belongedFixture->test_28()
;
   }

   TESTNGPP_NS::TestFixture* getFixture() const
   {
      return belongedFixture;
   }

   unsigned int numberOfTags() const
   {
      return 0;
   }

   const char** getTags() const
   {
      static const char* tags[] = {0};
      return tags;
   }

   const char* getMemCheckSwitch() const
   {
      static const char* memCheckSwitch = "none";
      return memCheckSwitch;
   }

private:
   TestsalaryTest* belongedFixture;
} testcase_instance_TestsalaryTest_test_28 ;



static struct TESTCASE_TestsalaryTest_test_32
   : public TESTNGPP_NS::TestCase
{
   TESTCASE_TestsalaryTest_test_32()
      : TESTNGPP_NS::TestCase
        ( "when input error salary should be INVALID_SALARY"
        , "salaryTest"
        , "testcase"
        , 0
        , "salaryTestCase.xpp"
        , 32)
   {}

   void setFixture(TESTNGPP_NS::TestFixture* fixture)
   {
      if(fixture == 0)
      {
         belongedFixture = new TestsalaryTest();
      }
      else
      {
         belongedFixture = dynamic_cast<TestsalaryTest*>(fixture);
      }
   }

   void runTest()
   {
      
belongedFixture->test_32()
;
   }

   TESTNGPP_NS::TestFixture* getFixture() const
   {
      return belongedFixture;
   }

   unsigned int numberOfTags() const
   {
      return 0;
   }

   const char** getTags() const
   {
      static const char* tags[] = {0};
      return tags;
   }

   const char* getMemCheckSwitch() const
   {
      static const char* memCheckSwitch = "none";
      return memCheckSwitch;
   }

private:
   TestsalaryTest* belongedFixture;
} testcase_instance_TestsalaryTest_test_32 ;



static TESTNGPP_NS::TestCase* g_TESTCASEARRAY_TestsalaryTest[] = {
&testcase_instance_TestsalaryTest_test_7,
&testcase_instance_TestsalaryTest_test_12,
&testcase_instance_TestsalaryTest_test_16,
&testcase_instance_TestsalaryTest_test_20,
&testcase_instance_TestsalaryTest_test_24,
&testcase_instance_TestsalaryTest_test_28,
&testcase_instance_TestsalaryTest_test_32,
0
};




/*static*/ TESTNGPP_NS::TestFixtureDesc test_fixture_desc_instance_TestsalaryTest
   ( "salaryTest"
   , "salaryTestCase.xpp"
   , g_TESTCASEARRAY_TestsalaryTest
   , (sizeof(g_TESTCASEARRAY_TestsalaryTest)/sizeof(g_TESTCASEARRAY_TestsalaryTest[0])) - 1
   );



static TESTNGPP_NS::TestFixtureDesc* array_of_fixture_desc_testcase[] = {
&test_fixture_desc_instance_TestsalaryTest,
0
};




static TESTNGPP_NS::TestSuiteDesc test_suite_desc_instance_testcase
   ( "testcase"
   , array_of_fixture_desc_testcase
   , (sizeof(array_of_fixture_desc_testcase)/sizeof(array_of_fixture_desc_testcase[0])) - 1
   );



extern "C" DLL_EXPORT TESTNGPP_NS::TestSuiteDesc* ___testngpp_test_suite_desc_getter() {
   return &test_suite_desc_instance_testcase;
}


