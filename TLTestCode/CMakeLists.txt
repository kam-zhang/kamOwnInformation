CMAKE_MINIMUM_REQUIRED(VERSION 2.8)

PROJECT(tngppTestProj)
#FILE(GLOB_RECURSE testFiles ${CMAKE_SOURCE_DIR}/test/*.hpp)

SET(testcase ${CMAKE_SOURCE_DIR}/test/testcase.cpp)

FIND_LIBRARY(testngpp_so NAMES testngpp PATHS ${CMAKE_SOURCE_DIR}/testngppTool/lib)

IF(testngpp_so)
LINK_DIRECTORIES(${CMAKE_SOURCE_DIR}/testngppTool/lib/)
ELSE()
MESSAGE(FATAL_ERROR "Can not find libtestngpp.so!")
ENDIF()

INCLUDE_DIRECTORIES(${CMAKE_SOURCE_DIR}/testngppTool/include)
INCLUDE_DIRECTORIES(${CMAKE_SOURCE_DIR}/src/include)

FILE(GLOB_RECURSE src "*.cpp")

ADD_DEFINITIONS(-g -ggdb -fPIC)

ADD_LIBRARY(test SHARED ${testcase} ${src})

TARGET_LINK_LIBRARIES(test testngpp)



