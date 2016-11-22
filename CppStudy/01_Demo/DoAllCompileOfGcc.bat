@set CurrentPath=%cd%
@echo *******************%CurrentPath% Gcc清理过程如下：**************************
@if not exist .\Project (MD .\Project)
@if not exist .\bin (MD .\bin)
@cd .\Project
@del .\*.* /Q /F
@del .\CMakeFiles\*.* /Q /S /F
@del ..\bin\*.* /Q /F
@rd .\CMakeFiles /Q /S


@path %CurrentPath%\..\00_Tools\MinGW\bin;%CurrentPath%\..\00_Tools\CMake 2.8\bin;C:\Windows\system32;C:\Windows;C:\Windows\System32\Wbem;C:\Windows\System32\WindowsPowerShell\v1.0
path
@echo *******************%CurrentPath% Gcc工程建立如下：**************************
@cmake .. -G "MinGW Makefiles"

@rem mingw32-make.exe 
@cmake --build . > ..\CompilerLog.txt
@echo *******************%CurrentPath% Gcc编译结果如下：**************************
@type ..\CompilerLog.txt
@copy .\*.exe ..\bin
@cd ..
@.\bin\UnitRun.exe > .\UnitTestResult.txt
@echo *******************%CurrentPath% Gcc运行结果如下：**************************
@.\bin\UnitRun.exe
@pause