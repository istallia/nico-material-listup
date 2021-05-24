all:
	pyinstaller listup_tool.py -F --clean --noupx --icon iconmonstr-file-27-240.ico
	cp ./dist/listup_tool.exe .

clean:
	rm -rf __pycache__
	rm -rf build
	rm -rf dist
	rm listup_tool.spec
