@echo off
chcp 932
rem コモンズ素材リストアップツール(v0.2)をレジストリに登録するバッチファイル

setlocal
set APP_PATH=%~dp0listup_tool.exe
set COMMAND1=\"%APP_PATH%\"
set COMMAND2=\"%%1\"
set COMMAND3=%COMMAND1% %COMMAND2%
echo %COMMAND1% %COMMAND2%

reg add "HKEY_CURRENT_USER\Software\Classes\*\shell\ニコニコ素材の一覧を生成する" /v "Icon" /t REG_SZ /d "%APP_PATH%" /f
reg add "HKEY_CURRENT_USER\Software\Classes\*\shell\ニコニコ素材の一覧を生成する\command" /ve /t REG_SZ /d "%COMMAND3%" /f
