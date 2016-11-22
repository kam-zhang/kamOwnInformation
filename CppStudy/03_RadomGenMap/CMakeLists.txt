CMAKE_MINIMUM_REQUIRED(VERSION 2.8)

PROJECT(UnitTest)


FILE(GLOB_RECURSE all_files 
"${CMAKE_CURRENT_SOURCE_DIR}/Source/*.C"
"${CMAKE_CURRENT_SOURCE_DIR}/Source/*.c"
"${CMAKE_CURRENT_SOURCE_DIR}/Source/*.CPP"
"${CMAKE_CURRENT_SOURCE_DIR}/Source/*.cpp"
"${CMAKE_CURRENT_SOURCE_DIR}/TestSource/*.C"
"${CMAKE_CURRENT_SOURCE_DIR}/TestSource/*.c"
"${CMAKE_CURRENT_SOURCE_DIR}/TestSource/*.CPP"
"${CMAKE_CURRENT_SOURCE_DIR}/TestSource/*.cpp"
)

INCLUDE_DIRECTORIES( 
"${CMAKE_CURRENT_SOURCE_DIR}/Include"
"${CMAKE_CURRENT_SOURCE_DIR}Include/gtest"
"${CMAKE_CURRENT_SOURCE_DIR}Include/gtest/internal"
"${CMAKE_CURRENT_SOURCE_DIR}/TestSource"
)

if(${CMAKE_COMPILER_IS_GNUCC})
    add_definitions(-Wall -g)
endif()

link_directories("${CMAKE_CURRENT_SOURCE_DIR}/../00_Tools/Lib")
#source_group_by_dir(all_files)
add_executable(UnitRun ${all_files})
message (STATUS "CMAKE_C_COMPILER is ${CMAKE_C_COMPILER}, CMAKE_CXX_COMPILER is ${CMAKE_CXX_COMPILER}")
message (STATUS "CMAKE_COMPILER_IS_GNUCC is ${CMAKE_COMPILER_IS_GNUCC}")
if(${CMAKE_COMPILER_IS_GNUCC})
    target_link_libraries(UnitRun libgtest.a)
else()
    target_link_libraries(UnitRun gtest-vc10.lib)
endif()
#target_link_libraries(UnitRun libgtest.a)gtest-vc10.lib

