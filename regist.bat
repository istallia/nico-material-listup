@echo off
chcp 932
rem �R�����Y�f�ރ��X�g�A�b�v�c�[��(v0.2)�����W�X�g���ɓo�^����o�b�`�t�@�C��

setlocal
set APP_PATH=%~dp0listup_tool.exe
set COMMAND1=\"%APP_PATH%\"
set COMMAND2=\"%%1\"
set COMMAND3=%COMMAND1% %COMMAND2%
echo %COMMAND1% %COMMAND2%

reg add "HKEY_CURRENT_USER\Software\Classes\*\shell\�j�R�j�R�f�ނ̈ꗗ�𐶐�����" /v "Icon" /t REG_SZ /d "%APP_PATH%" /f
reg add "HKEY_CURRENT_USER\Software\Classes\*\shell\�j�R�j�R�f�ނ̈ꗗ�𐶐�����\command" /ve /t REG_SZ /d "%COMMAND3%" /f
