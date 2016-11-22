@set CurrentPath=%cd%
@if not exist .\Project (MD .\Project)
@if not exist .\bin (MD .\bin)
@cd .\Project
@del .\*.exe /Q 
@del ..\bin\*.* /Q 
@del .\Debug\*.* /Q 


@path %CurrentPath%\..\00_Tools\MinGW\bin;%CurrentPath%\..\00_Tools\CMake 2.8\bin;

@echo *******************编译结果如下：**************************
@cmake --build . > ..\CompilerLog.txt
@type ..\CompilerLog.txt

@if exist *.exe ( copy .\*.exe ..\bin ) else ( copy .\Debug\*.exe ..\bin )
@cd ..
@.\bin\UnitRun.exe > .\UnitTestResult.txt
@echo *******************运行结果如下：**************************
@.\bin\UnitRun.exe
@pause
