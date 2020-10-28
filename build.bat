@echo off
cd %~dp0
pyinstaller -F --clean --noupx listup_tool.py --icon iconmonstr-file-27-240.ico
move /Y .\dist\listup_tool.exe .\listup_tool.exe
pause
