@set CurrentPath=%cd%
@echo *******************%CurrentPath% Gcc����������£�**************************
@if not exist .\Project (MD .\Project)
@if not exist .\bin (MD .\bin)
@cd .\Project
@del .\*.* /Q /F
@del .\CMakeFiles\*.* /Q /S /F
@del ..\bin\*.* /Q /F
@rd .\CMakeFiles /Q /S


@path %CurrentPath%\..\00_Tools\MinGW\bin;%CurrentPath%\..\00_Tools\CMake 2.8\bin;C:\Windows\system32;C:\Windows;C:\Windows\System32\Wbem;C:\Windows\System32\WindowsPowerShell\v1.0
path
@echo *******************%CurrentPath% Gcc���̽������£�**************************
@cmake .. -G "MinGW Makefiles"

@rem mingw32-make.exe 
@cmake --build . > ..\CompilerLog.txt
@echo *******************%CurrentPath% Gcc���������£�**************************
@type ..\CompilerLog.txt
@copy .\*.exe ..\bin
@cd ..
@.\bin\UnitRun.exe > .\UnitTestResult.txt
@echo *******************%CurrentPath% Gcc���н�����£�**************************
@.\bin\UnitRun.exe
@pause