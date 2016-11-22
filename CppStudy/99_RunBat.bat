@echo on
@setlocal ENABLEDELAYEDEXPANSION
@del /Q RunABatLog.txt
@for /f %%i  in  ('dir /A:D /B .\0*') do ( 
    cd .\%%i
    echo ***************************Deal %%i Gcc Version**************************
    del /Q MyDoAllCompileOfGcc.bat 
    findstr /V  /C:"pause" DoAllCompileOfGcc.bat >> MyDoAllCompileOfGcc.bat 
    call MyDoAllCompileOfGcc.bat >> ..\RunABatLog.txt
    del /Q MyDoAllCompileOfGcc.bat 
    
    echo ***************************Deal %%i VS2010 Version**************************
    del /Q MyDoAllCompileOfVs2010.bat 
    findstr /V  /C:"pause" DoAllCompileOfVs2010.bat >> MyDoAllCompileOfVs2010.bat 
    call MyDoAllCompileOfVs2010.bat >> ..\RunABatLog.txt
    del /Q MyDoAllCompileOfVs2010.bat 
    
    del /Q MyClean.bat 
    findstr /V  /C:"pause" Clean.bat >> MyClean.bat 
    call MyClean.bat >> ..\RunABatLog.txt
    del /Q MyClean.bat 
    
    cd ..
)
@pause