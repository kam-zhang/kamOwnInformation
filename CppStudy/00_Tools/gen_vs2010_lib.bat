@set CurrentPath=%~dp0%

path %CurrentPath%\..\00_Tools\MinGW\bin;%CurrentPath%\..\00_Tools\CMake 2.8\bin;C:\Windows\system32;C:\Windows;C:\Windows\System32\Wbem;C:\Windows\System32\WindowsPowerShell\v1.0
path
@if not exist .\gtest-1.7.0\lib (MD .\gtest-1.7.0\lib)
cd .\gtest-1.7.0\lib

cmake .. -G "Visual Studio 10"

cmake --build . 

copy .\Debug\gtest.lib ..\..\Lib\gtest-vc10.lib
del .\*.* /Q /F /S
rd .\CMakeFiles /Q /S
rd .\Debug /Q /S
rd .\gtest.dir /Q /S
rd .\gtest_main.dir /Q /S
rd .\Win32 /Q /S
cd ..
rd .\lib /Q /S
@pause