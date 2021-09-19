#!python3
#-*- coding: utf-8 -*-

# 「ニコニコ素材リストアップツール ライブラリ」by @is_ptcm
# メインスクリプトと関数をまとめたスクリプトを分けることにより可読性の向上を目指す


# --- パッケージ読み込み
import os.path
import sys
import time
import json
import re
import urllib
import glob
from urllib.request import urlopen
from bs4 import BeautifulSoup


# --- ファイルからIDを抽出
def getIdList(file_path):
	# 下準備
	print('[読み込み] '+os.path.basename(file_path), end='')
	content = b''
	# ファイルを読み込み
	with open(file_path, mode='rb') as f:
		content = f.read()
	if len(content) < 1:
		print(' -> 空、または読み込み失敗')
		return []
	# 抽出する
	content = content.replace(b'\x00', b'')
	id_list = re.findall(b'(?:\\b|^)((nc|im|sm|td)\\d{2,12})(?=\\b|$)', content)
	id_list = list(set(id_list))
	for i in range(len(id_list)):
		id_list[i] = id_list[i][0].decode('utf-8')
	print(' -> '+str(len(id_list))+'件のIDを抽出')
	return id_list
