#!/bin/bash

if [ ! -d "$CurrentDir/../project" ];
    then
	mkdir ./gtest-1.7.0/lib
fi
cd ./gtest-1.7.0/lib
rm * -r
cmake ../
cmake --build .
cp ./libgtest.a ../../Lib/libgtest.a
rm * -r