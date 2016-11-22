#!/bin/bash
set +x
##############################################
function generateTestCase()
{
	testngppgenPath=$1
	testcasePath=$2

    xppFiles=($(find ${testcasePath} -type f -iwholename "*/test/*" -iname "*.xpp"))

    echo $xppFiles
	for file in ${xppFiles[@]}
	do
		m="$m ${file/$PWD/.}"
	done
    echo "filelist is" $m
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

function setDynamicLibLoadPath()
{
    dynamicLoadPath=$1
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$dynamicLoadPath
}

function loadTestCase()
{
	testngppToolPath=$1
	testcase=$2
	if [ -f $testcase ]
	then
		${testngppToolPath}/bin/testngpp-runner ./libtest -s "" -c "3" -L "${testngppToolPath}/testngpp/listener" -l "testngppstdoutlistener -c -v" -l "testngppxmllistener testresult_demo.xml"
	fi
}

##############################################
curentpath=`pwd`
dynamicLibPath=`pwd`/testngppTool/lib

echo -e "\033[31m 设置动态加载库路径... \033[0m"
setDynamicLibLoadPath $dynamicLibPath

echo -e "\033[31m 生成测试用例文件... \033[0m"
generateTestCase `pwd`/testngppTool/testngpp/generator `pwd`/test

echo -e "\033[31m 创建编译路径... \033[0m"
createBuildPath

echo -e "\033[31m 开始编译... \033[0m"
compile

echo -e "\033[31m 开始运行用例... \033[0m"
loadTestCase `pwd`/../testngppTool libtest.so


