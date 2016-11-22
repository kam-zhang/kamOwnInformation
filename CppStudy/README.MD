有问题请邮件、IM反馈 张凯敏10117906
    此工程可用于开发、C/C++学习、练习、单元测试等方面，采用cmake作为make工具，GNU4.8.1（gcc、g++）作为编译器，内嵌了gTest单元测试工具，也可修改main()函数作为工具开发；目录结构如下：
E:\CppStudyPath>
│  00_ReadMe.txt
├─00_Tools
│  ├─CMake 2.8
│  │  ├─省略，内部都是CMake文件
│  └─MinGW
│      ├─省略，内部都是MinGW文件
└─01_Demo
    │  Clean.bat
    │  CMakeLists.txt
    │  DoAllCompile.bat
    │  DoIncCompile.bat
    │
    ├─Include
    │  │  MyFunction.h
    │  │  PublicDef.h
    │  │
    │  ├─base
    │  │      BaseTypes.h
    │  │      stdc.h
    │  │
    │  └─gtest
    │          gtest Include文件
    │
    ├─Lib
    │      libgtest.a
    │
    ├─Source
    │      MyFunction.cpp
    │
    └─TestSource
            main.cpp
            MyFunctionTestCase.cpp

00_ReadMe.txt  是本文件
00_Tools 目录下放的是CMake和MinGW编译器；
01_Demo放的是代码示例；

其中Include、Source、TestSource这三个文件中放的是代码；
main.cpp默认是gtest调用函数，如果用gtest单元测试框架的话，不必修改；
MyFunction*.*文件都是自己开发的文件，可以增加
Clean.bat    清除所有自动生成文件的脚本，不要修改
CMakeLists.txt  CMake使用的文件，不要修改
DoAllCompile.bat   重新生成Project下文件，重新全编译，重新生成可执行文件，并执行可执行文件
DoIncCompile.bat   重新增量编译，重新生成可执行文件，并执行可执行文件


使用方法：
1、从svn上把00_Tools、01_Demo下载到本地；
2、新建自己的目录，姓名+工号
3、把00_Demo中内容，删除.svn信息后，复制到新建目录下
3、执行新建目录下 DoAllCompile.bat  会出现，如下执行界面，为通过，即建立成功，可以开始自己代码的开发

*******************运行结果如下：**************************
[==========] Running 1 test from 1 test case.
[----------] Global test environment set-up.
[----------] 1 test from MyFunctionTest
[ RUN      ] MyFunctionTest.should_sucess
[       OK ] MyFunctionTest.should_sucess (0 ms)
[----------] 1 test from MyFunctionTest (16 ms total)

[----------] Global test environment tear-down
[==========] 1 test from 1 test case ran. (16 ms total)
[  PASSED  ] 1 test.
请按任意键继续. . .

dasdadadadad


