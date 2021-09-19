#!python3
#-*- coding: utf-8 -*-

# 「ニコニコ素材リストアップツール」by @is_ptcm
#
# ニコニコの素材を動画編集ソフトのプロジェクトファイルから抽出してリストアップしてくれるツール
# 10件ずつなのでコピペでコンテンツツリーに持って行く


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
import listup_tool_lib as tool


#--- タイトルを描画
print('------ 「ニコニコ素材リストアップツール」v0.7.0 by @is_ptcm ------\n')


#--- 読み出すファイル/フォルダをコマンドライン引数から取得(複数可)
input_list = []
if len(sys.argv) < 2:
	print('ファイル名(or パス)を入力してください: ', end='')
	file_name = input().strip()
	input_list.append(file_name)
else:
	for i in range(1,len(sys.argv)):
		input_list.append(sys.argv[i])
for i in range(len(input_list)):
	input_list[i] = os.path.abspath(input_list[i])
input_list = list(set(input_list))


#--- すべてのファイル名を取得
file_list = []
dir_list  = []
for i in range(len(input_list)):
	if os.path.isdir(input_list[i]):
		dir_list.append(input_list[i])
	elif os.path.isfile(input_list[i]):
		file_list.append(input_list[i])
for i in range(len(dir_list)):
	files = glob.glob(dir_list + '\\**')
	for j in range(len(files)):
		file_list.append(os.path.abspath(files[j]))


#--- デバッグ用
input()
