@REM ����������벢���Զ�����������V3.2 V3.3��BPN FDD bpl1.lws��bpl1.so���ŵ���ǰĿ¼�ĵ�һ���ļ�����

 
@setlocal ENABLEDELAYEDEXPANSION
@set THIS_PATH=%~dp0
@echo on 


set date_time1=%DATE%_%TIME%
set date_time2=%date_time1: =0%
set date_time3=%date_time2::=%
set date_time4=%date_time3:/=-%
@set MY_CMAC_VERSION_PATH=%THIS_PATH%BPN_FDD_CmacVersion%date_time4%
@if not exist %MY_CMAC_VERSION_PATH% (MD %MY_CMAC_VERSION_PATH%) else (
@REM ɾ��֮ǰ�����ļ�
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
if not !count! equ 6  ( cls & @echo ����ʧ�� & @goto End ) 
@del temp.txt
@del temp2.txt

cd %THIS_PATH%code\rt_lwos
copy /Y MCS-core_*.* %MY_CMAC_VERSION_PATH%
echo %MY_CMAC_VERSION_PATH%
copy /Y *MCS-core_*.* %THIS_PATH%eNodeB\eBBU\BPN\RMI_CC16\FDD
set PANFU=%~d0
cd %THIS_PATH%eNodeB\Version_Create\Script
echo %MY_CMAC_VERSION_PATH%
call V3.2_VersionMaker_LTE_FDD.bat

%PANFU%
cd %MY_CMAC_VERSION_PATH%
copy /Y %THIS_PATH%eNodeB\VersionNo_LTE_FDD\*.pkg .
:End
@pause
