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


#--- 読み出すファイルをコマンドライン引数から取得(複数可)
file_list = []
if len(sys.argv) < 2:
	print('ファイル名(or パス)を入力してください: ', end='')
	file_list.append(input().strip())
else:
	for i in range(1,len(sys.argv)):
		file_list.append(sys.argv[i])
for i in range(len(file_list)):
	file_list[i] = os.path.abspath(file_list[i])
file_list = list(set(file_list))


#--- デバッグ用
input()
