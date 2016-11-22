@REM pcLint&编译&自动化测试的一站式入口
@REM V1.0新创建版本
@REM V1.1Log保存目录按照日期命名，避免出现覆盖现象；修改显示的结果名称为汉字
@REM V1.2 增加脚本执行前，删除rt_lwos目录下文件，保留MIX文件夹；修复Windows7下生成结果文件夹名称bug
@REM V1.3 增加每次重新生成Pclint 临时脚本功能，确保在添加新模块后，能同步pclint
@REM V1.4 修改脚本文件名称，V3.2/V3.3通用脚本；脚本内容无更改
@REM V1.5 修改BPN调用的脚本
@REM V1.6 修改FT结果校验方式
@REM V1.7 添加eFT自动执行，和执行结果自动检查
 
@setlocal ENABLEDELAYEDEXPANSION
@set Code_PATH=%~dp0
@echo on 

@REM 设置Pclint&自动化编译目录
@set Etc_PATH=%Code_PATH%code\Code_LTE\cmac\etc
@set FT_PATH=%Code_PATH%TestCase\FT\MAC\Project
@set Pclint_PATH=%Etc_PATH%\pclint
@set AT_MACRO_PATH=%FT_PATH%\VOS_Macro
@set AT_MICRO_PATH=%FT_PATH%\VOS_Micro
@set AT_BPN_PATH=%FT_PATH%\VOS_BPN

@REM 设置编译目录
@set CompileScript_PATH=%Code_PATH%code\DailyBuild
@set BPL1_Script_PATH=%CompileScript_PATH%\BPL1
@set BPN_Script_PATH=%CompileScript_PATH%\BPN

@REM 创建输出结果目录
@set BuildResultPath=%Code_PATH%code\rt_lwos
set date_time1=%DATE%_%TIME%
set date_time2=%date_time1: =0%
set date_time3=%date_time2::=%
set date_time4=%date_time3:/=-%
@set CollectAll_PATH=%Code_PATH%CollectAll_%date_time4%
@if not exist %CollectAll_PATH% (MD %CollectAll_PATH%) else (
@REM 删除之前所有的编译文件
@del /Q %CollectAll_PATH%)

@if exist %BuildResultPath% ( del /Q %BuildResultPath% )


@REM 命令行参数选择分支
@echo 请按提示输入对应代号
@echo 执行所有:A 
@echo 宏站lint:Malt 
@echo 微站lint:Milt 
@echo BPL1编译:L 
@echo BPN编译:N 
@echo 宏站AT:MaAt 
@echo 微站AT:MiAt
@echo BPNAT:NAt

@echo 请选择:
@rem set /P Param1=
@set Param1=a

@if %Param1%==Milt goto Label_LINTMICRO
@if %Param1%==Malt goto Label_LINTMACRO
@if %Param1%==L goto Label_BUILDBPL1
@if %Param1%==N goto Label_BUILDBPN
@if %Param1%==MaAt goto Label_ATMACRO
@if %Param1%==MiAt goto Label_ATMICRO
@if %Param1%==NAt  goto Label_ATBPN

rem @设置所有结果为undo
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
@echo 代码路径:%Code_PATH%> %CollectAll_PATH%\TestResultAndTimeStatic.txt



@echo 开始Pclint--------------------------------------------
:Label_LINTMACRO
@echo 宏站Lint
@echo 宏站 PcLint Start %time%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt
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
echo 宏站 PcLint End   %time%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt
@if %Param1%==Malt (goto End)
rem goto Label_BUILDBPL1
:Label_LINTMICRO
@echo 微站Lint
echo 微站 PcLint Start %time%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt
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
echo 微站 PcLint End   %time%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt
@if %Param1%==Milt (goto End)
@echo 结束Pclint--------------------------------------------

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
@echo 结束Pclint--------------------------------------------

:Label_BUILDBPL1
@echo 开始编译--------------------------------------------
@echo 编译BPL1
echo BPL1 编译 Start %time%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt
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
echo BPL1 编译 End   %time%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt
@if %Param1%==L (goto End)


:Label_BUILDBPN
@echo 编译BPN
cd %BPN_Script_PATH%\Script
echo BPN 编译 Start %time%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt
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
echo BPN 编译 End   %time%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt
@if %Param1%==N (goto End)
@echo 结束编译--------------------------------------------

goto eFT_Run

:Label_ATMACRO
@echo VS自动化编译测试开始-------------------------------
@echo BPL1AT
echo 宏站FT测试 Start %time%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt
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
@findstr /I  "未" VosMacro_TestResult.txt >NUL
@if !errorlevel!==0 ( set VosMacro_TestResult=Failed 
                      goto End
                    ) else ( 
                      set VosMacro_TestResult=Successful )
@if %Param1%==MaAt (goto End)
:VosMacroEnd
echo 宏站FT测试 End   %time%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt

:Label_ATMICRO
@echo 微站AT
echo 微站FT测试 Start %time%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt
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
@findstr /I  "未" VosMicro_TestResult.txt >NUL
@if !errorlevel!==0 ( set VosMicro_TestResult=Failed 
                      goto End
                    ) else ( 
                      set VosMicro_TestResult=Successful )
@if %Param1%==MiAt (goto End)
:VosMicroEnd
echo 微站FT测试 End   %time%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt


:Label_ATBPN
@echo BPNAT
echo BPN FT测试 Start %time%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt
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
@findstr /I  "未通过" %CollectAll_PATH%\VosBPN_TestResult.txt >NUL

@if !errorlevel!==0 ( set VosBPN_TestResult=Failed 
                      goto End ) else ( set VosBPN_TestResult=Successful )

:VosBPNEnd
@echo BPN FT测试 End   %time%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt


:eFT_Run
@echo eFT测试 Start %time%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt
@echo eFT测试 Start %time%
@cd %Code_PATH%\TestCase\FT\MAC
@del /Q Myrun_eFT.bat 
@findstr /V  /C:"pause" run_eFT.bat >> Myrun_eFT.bat 

@call Myrun_eFT.bat > %CollectAll_PATH%\eFTLog.txt
@del /Q Myrun_eFT.bat
@findstr /I  "FAILED" %CollectAll_PATH%\eFTLog.txt >NUL
@if !errorlevel!==0 ( set eFT_TestResult=Failed 
                      goto End ) else ( set eFT_TestResult=Successful )
:eFT Run End
@echo eFT测试 End   %time%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt

:End
@echo 所有任务结束，时间 %time%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt
cls
@color 0a
@echo ******************Run Result****************************
@echo ******************Run Result****************************>> %CollectAll_PATH%\TestResultAndTimeStatic.txt
@if %MacroLintResult%==Failed ( color 0c )
@echo 宏站_Pclint结果 is %MacroLintResult% 
@echo 宏站_Pclint结果 is %MacroLintResult%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt

@if %MicroLintResult%==Failed ( color 0c )
@echo 微站_Pclint结果 is %MicroLintResult%
@echo 微站_Pclint结果 is %MicroLintResult%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt

@if %BPNLintResult%==Failed ( color 0c )
@echo BPN_Pclint结果 is %BPNLintResult%
@echo BPN_Pclint结果 is %BPNLintResult%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt
   
@if %BPL1BuildResult%==Failed ( color 0c )
@echo BPL1编译结果 is %BPL1BuildResult%
@echo BPL1编译结果 is %BPL1BuildResult%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt
     
@if %BPNBuildResult%==Failed ( color 0c )
@echo BPN编译结果 is %BPNBuildResult%
@echo BPN编译结果 is %BPNBuildResult%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt
     
@if %VosMacro_CompileResult%==Failed ( color 0c )
@echo 宏站_FT编译结果 is %VosMacro_CompileResult%
@echo 宏站_FT编译结果 is %VosMacro_CompileResult%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt
     
@if %VosMacro_TestResult%==Failed ( color 0c )
@echo 宏站_FT测试结果 is %VosMacro_TestResult%
@echo 宏站_FT测试结果 is %VosMacro_TestResult%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt
     
@if %VosMicro_CompileResult%==Failed ( color 0c )
@echo 微站_FT编译结果 is %VosMicro_CompileResult%
@echo 微站_FT编译结果 is %VosMicro_CompileResult%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt
     
@if %VosMicro_TestResult%==Failed ( color 0c )
@echo 微站_FT测试结果 is %VosMicro_TestResult%
@echo 微站_FT测试结果 is %VosMicro_TestResult%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt
     
@if %VosBPN_CompileResult%==Failed ( color 0c )
@echo BPN_FT编译结果 is %VosBPN_CompileResult%
@echo BPN_FT编译结果 is %VosBPN_CompileResult%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt
     
@if %VosBPN_TestResult%==Failed ( color 0c )
@echo BPN_FT测试结果 is %VosBPN_TestResult%
@echo BPN_FT测试结果 is %VosBPN_TestResult%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt

@if %eFT_TestResult%==Failed ( color 0c )
@echo eFT测试结果 is %eFT_TestResult%
@echo eFT测试结果 is %eFT_TestResult%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt


@echo 具体Log请查看目录:%CollectAll_PATH%
@echo 具体Log请查看目录:%CollectAll_PATH%>> %CollectAll_PATH%\TestResultAndTimeStatic.txt

@setlocal DISABLEEXTENSIONS
@cd 
@pause
