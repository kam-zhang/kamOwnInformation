@REM 完成增量编译并且自动制作出生成V3.2 V3.3的BPN TDD bpl1.lws和bpl1.so，放到当前目录的的一个文件夹内

 
@setlocal ENABLEDELAYEDEXPANSION
@set THIS_PATH=%~dp0
@echo on 


set date_time1=%DATE%_%TIME%
set date_time2=%date_time1: =0%
set date_time3=%date_time2::=%
set date_time4=%date_time3:/=-%
@set MY_CMAC_VERSION_PATH=%THIS_PATH%BPN_TDD_CmacVersion%date_time4%
@if not exist %MY_CMAC_VERSION_PATH% (MD %MY_CMAC_VERSION_PATH%) else (
@REM 删除之前编译文件
@del /Q %MY_CMAC_VERSION_PATH%)

cd %THIS_PATH%code\DailyBuild\BPN\Script
call Linux_BPN_CMAC.bat

echo %MY_CMAC_VERSION_PATH%
:debug
cd %THIS_PATH%code\rt_lwos
dir %THIS_PATH%code\rt_lwos > temp.txt
findstr /c:"MCS" temp.txt > temp2.txt
set /a count=0
for /f %%i in (temp2.txt) do (
  @set /a count = !count! + 1 )
if not !count! equ 6  ( cls & @echo 编译失败 & @goto End ) 
@del temp.txt
@del temp2.txt

cd %THIS_PATH%code\rt_lwos
copy /Y MCS-core_*.* %MY_CMAC_VERSION_PATH%
copy /Y REL_MCS-core_*.* %MY_CMAC_VERSION_PATH%
echo %MY_CMAC_VERSION_PATH%
copy /Y *MCS-core_*.* %THIS_PATH%eNodeB\eBBU\BPN\RMI_CC16\TDD

cd %THIS_PATH%eNodeB\Version_Create\Script
echo %MY_CMAC_VERSION_PATH%
set PANFU=%~d0
call V3.2_VersionMaker_LTE_TDD.bat

%PANFU%
cd %MY_CMAC_VERSION_PATH%
copy /Y %THIS_PATH%eNodeB\VersionNo_LTE_TDD\*.pkg .
:End
@pause
