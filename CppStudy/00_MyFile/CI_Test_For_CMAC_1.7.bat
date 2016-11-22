@REM pcLint&����&�Զ������Ե�һվʽ���
@REM V1.0�´����汾
@REM V1.1Log����Ŀ¼��������������������ָ��������޸���ʾ�Ľ������Ϊ����
@REM V1.2 ���ӽű�ִ��ǰ��ɾ��rt_lwosĿ¼���ļ�������MIX�ļ��У��޸�Windows7�����ɽ���ļ�������bug
@REM V1.3 ����ÿ����������Pclint ��ʱ�ű����ܣ�ȷ���������ģ�����ͬ��pclint
@REM V1.4 �޸Ľű��ļ����ƣ�V3.2/V3.3ͨ�ýű����ű������޸���
@REM V1.5 �޸�BPN���õĽű�
@REM V1.6 �޸�FT���У�鷽ʽ
@REM V1.7 ���eFT�Զ�ִ�У���ִ�н���Զ����
 
@setlocal ENABLEDELAYEDEXPANSION
@set Code_PATH=%~dp0
@echo on 

@REM ����Pclint&�Զ�������Ŀ¼
@set Etc_PATH=%Code_PATH%code\Code_LTE\cmac\etc
@set FT_PATH=%Code_PATH%TestCase\FT\MAC\Project
@set Pclint_PATH=%Etc_PATH%\pclint
@set AT_MACRO_PATH=%FT_PATH%\VOS_Macro
@set AT_MICRO_PATH=%FT_PATH%\VOS_Micro
@set AT_BPN_PATH=%FT_PATH%\VOS_BPN

@REM ���ñ���Ŀ¼
@set CompileScript_PATH=%Code_PATH%code\DailyBuild
@set BPL1_Script_PATH=%CompileScript_PATH%\BPL1
@set BPN_Script_PATH=%CompileScript_PATH%\BPN

@REM ����������Ŀ¼
@set BuildResultPath=%Code_PATH%code\rt_lwos
set date_time1=%DATE%_%TIME%
set date_time2=%date_time1: =0%
set date_time3=%date_time2::=%
set date_time4=%date_time3:/=-%
@set CollectAll_PATH=%Code_PATH%CollectAll_%date_time4%
@if not exist %CollectAll_PATH% (MD %CollectAll_PATH%) else (
@REM ɾ��֮ǰ���еı����ļ�
@del /Q %CollectAll_PATH%)

@if exist %BuildResultPath% ( del /Q %BuildResultPath% )


@REM �����в���ѡ���֧
@echo �밴��ʾ�����Ӧ����
@echo ִ������:A 
@echo ��վlint:Malt 
@echo ΢վlint:Milt 
@echo BPL1����:L 
@echo BPN����:N 
@echo ��վAT:MaAt 
@echo ΢վAT:MiAt
@echo BPNAT:NAt

@echo ��ѡ��:
@rem set /P Param1=
@set Param1=a

@if %Param1%==Milt goto Label_LINTMICRO
@if %Param1%==Malt goto Label_LINTMACRO
@if %Param1%==L goto Label_BUILDBPL1
@if %Param1%==N goto Label_BUILDBPN
@if %Param1%==MaAt goto Label_ATMACRO
@if %Param1%==MiAt goto Label_ATMICRO
@if %Param1%==NAt  goto Label_ATBPN

rem @�������н��Ϊundo
@set MacroLintResult=UnDo
@set MicroLintResult=UnDo
@set BPNLintResult=UnDo
@set BPL1BuildResult=UnDo
@set BPNBuildResult=UnDo
@set VosMacro_CompileResult=UnDo
@set VosMacro_TestResult=UnDo
@set VosMicro_CompileResult=UnDo
@set VosMicro_TestResult=UnDo
@set VosBPN_CompileResult=UnDo
@set VosBPN_TestResult=UnDo
@set eFT_TestResult=UnDo
@echo ����·��:%Code_PATH%> %CollectAll_PATH%\TestResultAndTimeStatic.txt



@echo ��ʼPclint--------------------------------------------
:Label_LINTMACRO
@echo ��վLint
@echo ��վ PcLint Start %time%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt
cd %Pclint_PATH%
@call SetEnv_Macro.bat
@del /Q  Tmpautorun_all.bat 
@findstr /V  /C:"call lint_usecase.bat" autorun_all.bat >> Tmpautorun_all.bat
@call Tmpautorun_all.bat
@copy %Pclint_PATH%\pclint_OUT\cmac.lnt.txt %CollectAll_PATH%\Macrocmac.lint.txt

@findstr /I "error" %Pclint_PATH%\pclint_OUT\cmac.lnt.txt >NUL
@if !errorlevel!==0 ( set MacroLintResult=Failed 
                      goto End
                    ) else ( 
                      set MacroLintResult=Successful )
echo ��վ PcLint End   %time%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt
@if %Param1%==Malt (goto End)
rem goto Label_BUILDBPL1
:Label_LINTMICRO
@echo ΢վLint
echo ΢վ PcLint Start %time%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt
cd %Pclint_PATH%
call SetEnv_Micro.bat
@if not exist Tmpautorun_all.bat (
@findstr /V  /C:"call lint_usecase.bat" autorun_all.bat >> Tmpautorun_all.bat )
@call Tmpautorun_all.bat
@copy %Pclint_PATH%\pclint_OUT\cmac.lnt.txt %CollectAll_PATH%\Microcmac.lint.txt

@findstr /I  "error" %Pclint_PATH%\pclint_OUT\cmac.lnt.txt >NUL
@if !errorlevel!==0 ( set MicroLintResult=Failed 
                      goto End
                    ) else ( 
                      set MicroLintResult=Successful )
echo ΢վ PcLint End   %time%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt
@if %Param1%==Milt (goto End)
@echo ����Pclint--------------------------------------------

:Label_LINTMICRO
@echo BPN Lint
echo BPN PcLint Start %time%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt
cd %Pclint_PATH%
call SetEnv_ARMMacro.bat
@if not exist Tmpautorun_all.bat ( @findstr /V  /C:"call lint_usecase.bat" autorun_all.bat >> Tmpautorun_all.bat )
@call Tmpautorun_all.bat
@copy %Pclint_PATH%\pclint_OUT\cmac.lnt.txt %CollectAll_PATH%\BPNcmac.lint.txt

@findstr /I  "error" %Pclint_PATH%\pclint_OUT\cmac.lnt.txt >NUL
@if !errorlevel!==0 ( set BPNLintResult=Failed 
                      goto End
                    ) else ( 
                      set BPNLintResult=Successful )
echo BPN PcLint End   %time%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt
@if %Param1%==Milt (goto End)
@echo ����Pclint--------------------------------------------

:Label_BUILDBPL1
@echo ��ʼ����--------------------------------------------
@echo ����BPL1
echo BPL1 ���� Start %time%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt
@cd %BPL1_Script_PATH%\Script
@call Linux_BPL1_CMAC_Inc.bat
@copy %BPL1_Script_PATH%\CompileInfo\BPLB_COMPILE_CMAC.log %CollectAll_PATH%\BPLB_COMPILE_CMAC.log

@dir %BuildResultPath% > temp.txt
@findstr /c:"REL_P4080-core" temp.txt > temp2.txt
@set /a count=0
@for /f %%i in (temp2.txt) do (
  @set /a count = !count! + 1 )
@if 2 equ !count! ( set BPL1BuildResult=Successful 
                  ) else (  
                    set BPL1BuildResult=Failed
                    goto End)
@del temp.txt
@del temp2.txt
echo BPL1 ���� End   %time%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt
@if %Param1%==L (goto End)


:Label_BUILDBPN
@echo ����BPN
cd %BPN_Script_PATH%\Script
echo BPN ���� Start %time%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt
@call Linux_BPN_CMAC.bat
@copy %BPN_Script_PATH%\CompileInfo\Linux_BPN_CMAC.log %CollectAll_PATH%\Linux_BPN_CMAC.log

@dir %BuildResultPath% > temp.txt
@findstr /c:"MCS" temp.txt > temp2.txt
@set /a count=0
@for /f %%i in (temp2.txt) do (
  @set /a count = !count! + 1 )
@if 6 equ !count! ( set BPNBuildResult=Successful 
                  ) else (  
                    set BPNBuildResult=Failed 
                    goto End)
@del temp.txt
@del temp2.txt
echo BPN ���� End   %time%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt
@if %Param1%==N (goto End)
@echo ��������--------------------------------------------

goto eFT_Run

:Label_ATMACRO
@echo VS�Զ���������Կ�ʼ-------------------------------
@echo BPL1AT
echo ��վFT���� Start %time%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt
cd %AT_MACRO_PATH%
del /Q %AT_MACRO_PATH%\Debug\*.exe  
@call ft_test.bat
@copy %AT_MACRO_PATH%\VosMacro_CompileResult.txt %CollectAll_PATH%\VosMacro_CompileResult.txt
@copy %AT_MACRO_PATH%\VosMacro_TestResult.txt %CollectAll_PATH%\VosMacro_TestResult.txt
set VosMacro_TestResult=Failed
@dir %AT_MACRO_PATH%\Debug >temp.txt
@findstr /I "MT.exe" temp.txt >NUL
@if !errorlevel!==0 ( set VosMacro_CompileResult=Successful ) else ( 
                      set VosMacro_CompileResult=Failed 
                      goto End) 
del temp.txt
@findstr /I  "δ" VosMacro_TestResult.txt >NUL
@if !errorlevel!==0 ( set VosMacro_TestResult=Failed 
                      goto End
                    ) else ( 
                      set VosMacro_TestResult=Successful )
@if %Param1%==MaAt (goto End)
:VosMacroEnd
echo ��վFT���� End   %time%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt

:Label_ATMICRO
@echo ΢վAT
echo ΢վFT���� Start %time%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt
cd %AT_MICRO_PATH%
del /Q %AT_MICRO_PATH%\Debug\*.exe  
@call ft_test.bat
@copy %AT_MICRO_PATH%\VosMicro_CompileResult.txt %CollectAll_PATH%\VosMicro_CompileResult.txt
@copy %AT_MICRO_PATH%\VosMicro_TestResult.txt %CollectAll_PATH%\VosMicro_TestResult.txt
set VosMicro_TestResult=Failed
@dir %AT_MICRO_PATH%\Debug >temp.txt
@findstr /I "ManualTest.exe" temp.txt >NUL
@if !errorlevel!==0 ( set VosMicro_CompileResult=Successful ) else ( 
                         set VosMicro_CompileResult=Failed 
                         goto End  ) 
del temp.txt
@findstr /I  "δ" VosMicro_TestResult.txt >NUL
@if !errorlevel!==0 ( set VosMicro_TestResult=Failed 
                      goto End
                    ) else ( 
                      set VosMicro_TestResult=Successful )
@if %Param1%==MiAt (goto End)
:VosMicroEnd
echo ΢վFT���� End   %time%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt


:Label_ATBPN
@echo BPNAT
echo BPN FT���� Start %time%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt
cd %AT_BPN_PATH%
del /Q %AT_BPN_PATH%\Debug\*.exe  
@call ft_test.bat
@copy %AT_BPN_PATH%\VosMacro_CompileResult.txt %CollectAll_PATH%\VosBPN_CompileResult.txt
@copy %AT_BPN_PATH%\VosMacro_TestResult.txt %CollectAll_PATH%\VosBPN_TestResult.txt
set VosBPN_TestResult=Failed
@dir %AT_BPN_PATH%\Debug >temp.txt
@findstr /I "MT.exe" temp.txt >NUL
@if !errorlevel!==0 ( set VosBPN_CompileResult=Successful ) else ( 
                      set VosBPN_CompileResult=Failed 
                      goto End  ) 
del temp.txt
@findstr /I  "δͨ��" %CollectAll_PATH%\VosBPN_TestResult.txt >NUL

@if !errorlevel!==0 ( set VosBPN_TestResult=Failed 
                      goto End ) else ( set VosBPN_TestResult=Successful )

:VosBPNEnd
@echo BPN FT���� End   %time%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt


:eFT_Run
@echo eFT���� Start %time%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt
@echo eFT���� Start %time%
@cd %Code_PATH%\TestCase\FT\MAC
@del /Q Myrun_eFT.bat 
@findstr /V  /C:"pause" run_eFT.bat >> Myrun_eFT.bat 

@call Myrun_eFT.bat > %CollectAll_PATH%\eFTLog.txt
@del /Q Myrun_eFT.bat
@findstr /I  "FAILED" %CollectAll_PATH%\eFTLog.txt >NUL
@if !errorlevel!==0 ( set eFT_TestResult=Failed 
                      goto End ) else ( set eFT_TestResult=Successful )
:eFT Run End
@echo eFT���� End   %time%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt

:End
@echo �������������ʱ�� %time%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt
cls
@color 0a
@echo ******************Run Result****************************
@echo ******************Run Result****************************>> %CollectAll_PATH%\TestResultAndTimeStatic.txt
@if %MacroLintResult%==Failed ( color 0c )
@echo ��վ_Pclint��� is %MacroLintResult% 
@echo ��վ_Pclint��� is %MacroLintResult%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt

@if %MicroLintResult%==Failed ( color 0c )
@echo ΢վ_Pclint��� is %MicroLintResult%
@echo ΢վ_Pclint��� is %MicroLintResult%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt

@if %BPNLintResult%==Failed ( color 0c )
@echo BPN_Pclint��� is %BPNLintResult%
@echo BPN_Pclint��� is %BPNLintResult%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt
   
@if %BPL1BuildResult%==Failed ( color 0c )
@echo BPL1������ is %BPL1BuildResult%
@echo BPL1������ is %BPL1BuildResult%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt
     
@if %BPNBuildResult%==Failed ( color 0c )
@echo BPN������ is %BPNBuildResult%
@echo BPN������ is %BPNBuildResult%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt
     
@if %VosMacro_CompileResult%==Failed ( color 0c )
@echo ��վ_FT������ is %VosMacro_CompileResult%
@echo ��վ_FT������ is %VosMacro_CompileResult%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt
     
@if %VosMacro_TestResult%==Failed ( color 0c )
@echo ��վ_FT���Խ�� is %VosMacro_TestResult%
@echo ��վ_FT���Խ�� is %VosMacro_TestResult%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt
     
@if %VosMicro_CompileResult%==Failed ( color 0c )
@echo ΢վ_FT������ is %VosMicro_CompileResult%
@echo ΢վ_FT������ is %VosMicro_CompileResult%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt
     
@if %VosMicro_TestResult%==Failed ( color 0c )
@echo ΢վ_FT���Խ�� is %VosMicro_TestResult%
@echo ΢վ_FT���Խ�� is %VosMicro_TestResult%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt
     
@if %VosBPN_CompileResult%==Failed ( color 0c )
@echo BPN_FT������ is %VosBPN_CompileResult%
@echo BPN_FT������ is %VosBPN_CompileResult%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt
     
@if %VosBPN_TestResult%==Failed ( color 0c )
@echo BPN_FT���Խ�� is %VosBPN_TestResult%
@echo BPN_FT���Խ�� is %VosBPN_TestResult%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt

@if %eFT_TestResult%==Failed ( color 0c )
@echo eFT���Խ�� is %eFT_TestResult%
@echo eFT���Խ�� is %eFT_TestResult%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt


@echo ����Log��鿴Ŀ¼:%CollectAll_PATH%
@echo ����Log��鿴Ŀ¼:%CollectAll_PATH%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt

@setlocal DISABLEEXTENSIONS
@cd 
@pause
