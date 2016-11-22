#!/bin/bash
echo $0
test1=$(dirname $0)
echo test1 is $test1
CurrentDir=$(cd $test1;pwd)

echo CurrentDir is $CurrentDir
cd $CurrentDir
pwd
if [ ! -d "$CurrentDir/../project" ];
    then
    mkdir ../project
    cd ../project
    echo 12344
else 
    echo 45678
    cd ../project
    rm ./* -r
fi
echo abc is $(pwd)
cmake $CurrentDir -G "Eclipse CDT4 - Unix Makefiles"

cmake --build .

./UnitRun


