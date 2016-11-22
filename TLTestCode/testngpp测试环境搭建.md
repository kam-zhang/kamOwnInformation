搭建testngpp测试环境
============================
测试驱动开发方法正在如火如荼的进行着，如何搭建一套即方便又好用的测试环境极为重要。测试环境的易用性包括编译单元的自动添加和删除能力，编译器的自动识别能力以及XUnit测试框架的自身优越性。基于以上各个方面，对比业界流行的构建管理工具和测试框架，此处选择，cmake+testngpp组合，为了满足testngpp的annotation特性，在linux环境下使用shell脚本实现，在windows环境下使用bat脚本实现。
实现过程
-----------------------------
####测试环境目录结构
~~~
├── build.sh
├── CMakeLists.txt
├── README
├── src
│   ├── include
│   └── source
├── test
│   ├── ddd
│   └── ssss.xpp
└── testngppTool
    ├── 3rdparty
    ├── bin
    ├── include
    ├── lib
    └── testngpp
~~~


####CMakeLists.txt实现
~~~cmake
CMAKE_MINIMUM_REQUIRED(VERSION 2.8)

PROJECT(tngppTestProj)

SET(testcase ${CMAKE_SOURCE_DIR}/test/testcase.cpp)

INCLUDE_DIRECTORIES(${CMAKE_SOURCE_DIR}/testngppTool/include)
INCLUDE_DIRECTORIES(${CMAKE_SOURCE_DIR}/src/include)

LINK_DIRECTORIES("${CMAKE_SOURCE_DIR}/testngppTool/lib")

FILE(GLOB_RECURSE src "*.cpp")

ADD_DEFINITIONS(-g -ggdb -fPIC)

ADD_LIBRARY(test SHARED ${testcase} ${src})

TARGET_LINK_LIBRARIES(test testngpp)
~~~

####shell脚本实现
~~~bash
#!/bin/bash

function generateTestCase()
{
	testngppgenPath=$1
	testcasePath=$2

    xppFiles=($(find . -type f -iwholename "*/test/*" -iname "*.xpp"))

	for file in ${xppFiles[@]}
	do
		m="$m ${file/$PWD/.}"
	done

	python ${testngppgenPath}/testngppgen.pyc -e gb2312 -o ${testcasePath}/testcase.cpp $m
}

function createBuildPath()
{
    if [ ! -d "./build" ]
    then
        mkdir ./build

    else
        rm -rf ./build/*
    fi

    cd ./build
}

function compile()
{
	cmake ..
	cmake --build .
}

function loadTestCase()
{
	testngppToolPath=$1
	testcase=$2
	if [ -f $testcase ]
	then
		${testngppToolPath}/bin/testngpp-runner ./libtest -s -c -L "${testngppToolPath}/testngpp/listener" -l "testngppstdoutlistener -c -v" -l "testngppxmllistener testresult_demo.xml"
	fi
}

generateTestCase /home/andy/testngpp-testproject/testngppTool/testngpp/generator ./test

createBuildPath

compile

loadTestCase /home/andy/testngpp-testproject/testngppTool libtest.so
~~~
####使用约束
在test目录中定义测试用例时，测试用例文件后缀必须为xpp

使用效果
----------------------------------
~~~bash
andy@andy-HP-EliteBook-820-G2:~/testngpp-testproject$ ./build.sh
-- The C compiler identification is GNU 4.8.4
-- The CXX compiler identification is GNU 4.8.4
-- Check for working C compiler: /usr/bin/cc
-- Check for working C compiler: /usr/bin/cc -- works
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Check for working CXX compiler: /usr/bin/c++
-- Check for working CXX compiler: /usr/bin/c++ -- works
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Configuring done
-- Generating done
-- Build files have been written to: /home/andy/testngpp-testproject/build
Scanning dependencies of target test
[ 33%] Building CXX object CMakeFiles/test.dir/test/testcase.cpp.o
[ 66%] Building CXX object CMakeFiles/test.dir/src/source/show.cpp.o
[100%] Building CXX object CMakeFiles/test.dir/CMakeFiles/2.8.12.2/CompilerIdCXX/CMakeCXXCompilerId.cpp.o
Linking CXX shared library libtest.so
[100%] Built target test
maximum # of sandboxes = 1
loading testngppstdoutlistener ... OK
loading testngppxmllistener ... OK

[   RUN    ] testcase::show_out::show you value out
[    OK    ] (87 us)
[   RUN    ] testcase::show_in::show you value in
[    OK    ] (79 us)


===========================RESULT===========================
[    OK    ] 2 cases from 1 suites ran successfully.

(0s 1285us)

~~~
至此，linux环境的testngpp测试环境完整搭建完毕，可以愉快的使用了。


