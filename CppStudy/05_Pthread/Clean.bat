@echo *******************清理过程如下：**************************
@if not exist .\Project (goto DeleteBin)
@cd .\Project
@del .\*.* /Q /F /S
@del .\*.* /Q /F /S /A:H
@rd .\CMakeFiles /Q /S
@rd .\Debug /Q /S
@rd .\UnitRun.dir /Q /S
@rd .\Win32 /Q /S
@rd .\ipch /Q /S
@cd ..
@rd .\Project
:DeleteBin
@del .\bin\*.* /Q /F
@rd .\bin
@del *Log.txt /Q
@del *Result.txt /Q
@pause