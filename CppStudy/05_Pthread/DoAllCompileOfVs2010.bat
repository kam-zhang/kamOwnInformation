@set CurrentPath=%cd%
@echo *******************%CurrentPath% VS2010����������£�**************************
@if not exist .\Project (MD .\Project)
@if not exist .\bin (MD .\bin)
@cd .\Project
@del .\*.* /Q /F
@del .\CMakeFiles\*.* /Q /S /F
@del ..\bin\*.* /Q /F
@rd .\CMakeFiles /Q /S


@path %CurrentPath%\..\00_Tools\MinGW\bin;%CurrentPath%\..\00_Tools\CMake 2.8\bin;C:\Windows\system32;C:\Windows;C:\Windows\System32\Wbem;C:\Windows\System32\WindowsPowerShell\v1.0

@echo *******************%CurrentPath% VS2010���̽������£�**************************
@cmake .. -G "Visual Studio 10"

@rem mingw32-make.exe 
@cmake --build . > ..\CompilerLog.txt
@echo *******************%CurrentPath% VS2010���������£�**************************
@type ..\CompilerLog.txt
@copy .\Debug\*.exe ..\bin
@cd ..
@.\bin\UnitRun.exe > .\UnitTestResult.txt
@echo *******************%CurrentPath% VS2010���н�����£�**************************
@.\bin\UnitRun.exe
@pause