@REM 完成增量编译并且自动制作出生成V3.2 V3.3的BPL1 TDD bpl1.lws和bpl1.so，放到当前目录的的一个文件夹内

 
@setlocal ENABLEDELAYEDEXPANSION
@set THIS_PATH=%~dp0
@echo on 


set date_time1=%DATE%_%TIME%
set date_time2=%date_time1: =0%
set date_time3=%date_time2::=%
set date_time4=%date_time3:/=-%
@set CMAC_VERSION_PATH=%THIS_PATH%BPL1_TDD_CmacVersion%date_time4%
@if not exist %CMAC_VERSION_PATH% (MD %CMAC_VERSION_PATH%) else (
@REM 删除之前编译文件
@del /Q %CMAC_VERSION_PATH%)

cd %THIS_PATH%code\DailyBuild\BPL1\Script
call Linux_BPL1_CMAC.bat
echo %CMAC_VERSION_PATH%

@dir %THIS_PATH%code\rt_lwos > temp.txt
@findstr /c:"REL_P4080-core" temp.txt > temp2.txt
@set /a count=0
@for /f %%i in (temp2.txt) do (
  @set /a count = !count! + 1 )
@if not 2 equ !count! ( @cls
                    @echo 编译失败
                    @goto End )
                  
@del temp.txt
@del temp2.txt


cd %THIS_PATH%code\rt_lwos
copy /Y P4080-core_CMAC*.* %CMAC_VERSION_PATH%
echo %CMAC_VERSION_PATH%
copy /Y REL_P4080-core_CMAC*.* %THIS_PATH%eNodeB\eBBU\BPL1\RMI_CC16\TDD 
copy /Y REL_P4080-core_CMAC*.* %CMAC_VERSION_PATH%

del /Q %THIS_PATH%eNodeB\Version_SW\LTE_TDD\*.*
cd %THIS_PATH%eNodeB\version_create\script\swbat\lte_tdd
echo %CMAC_VERSION_PATH%
call LTE_TDD_BPL1_LWS.bat
cd %THIS_PATH%eNodeB\version_create\script\swbat\lte_tdd
echo %CMAC_VERSION_PATH%
call LTE_TDD_BPL1_SO.bat
echo %CMAC_VERSION_PATH%
cd %CMAC_VERSION_PATH%
copy /Y %THIS_PATH%eNodeB\Version_SW\LTE_TDD\*.TdlBpl1Rmios .
:End
@pause
