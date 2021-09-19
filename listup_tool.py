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


# --- タイトルを描画
print('------ 「ニコニコ素材リストアップツール」v0.7.0 by @is_ptcm ------\n')


# --- 除外リストを作成
exclude_csv_path = os.path.dirname(os.path.abspath(__file__)) + 'exclude_ext_list.txt'
exclude_ext_list = ['lwi', 'avi', 'mp4', 'flv', 'mov', 'asf', 'mkv', 'webm', 'mpg', 'm2ts', 'mpg', 'mpeg', 'wav', 'mp3', 'ogg', 'wma', 'm4a', 'flac', 'aif', 'aiff', 'aac', 'mid', 'midi', 'jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp', 'ico', 'zip', 'lzh', '7z', 'gz', 'tar', 'exe', 'dll']
if os.path.isfile(exclude_csv_path):
	# 追加除外リストが存在すれば読み込む
	content = ''
	with open(exclude_csv_path, mode='r', encoding='utf-8') as f:
		content = f.read()
	exclude_ext_list.extend(re.findall(r'[-\w]+', content))


# --- 読み出すファイル/フォルダをコマンドライン引数から取得(複数可)
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


# --- すべてのファイル名を取得
base_path = ''
file_list = []
dir_list  = []
for i in range(len(input_list)):
	root, ext = os.path.splitext(input_list[i])
	if os.path.isdir(input_list[i]):
		dir_list.append(input_list[i])
	elif os.path.isfile(input_list[i]) and not ext[1:] in exclude_ext_list:
		file_list.append(input_list[i])
for i in range(len(dir_list)):
	files = [p for p in glob.glob(dir_list[i]+'\\**', recursive=True) if os.path.isfile(p)]
	for j in range(len(files)):
		root, ext = os.path.splitext(input_list[i])
		if not ext[1:] in exclude_ext_list:
			file_list.append(os.path.abspath(files[j]))
base_path = os.path.dirname(file_list[0])


# --- すべてのIDを取得
print('')
id_list = []
for i in range(len(file_list)):
	id_list.extend(tool.getIdList(file_list[i]))
if len(id_list) < 1:
	input('ニコニコ素材が見つかりませんでした。Enterで終了します:')
	sys.exit(0)
print('+ 合計' + str(len(id_list)) + '件のIDを抽出\n')



# --- IDリストを保存し、さらにタイトルや投稿者も取得するか確認する
id_text = tool.generateIdListText(id_list)
with open(base_path+'/IDs.txt', mode='w', encoding='cp932') as f:
	f.write(id_text)
confirm = input('オンラインでタイトルと投稿者を取得しますか？結果はCSV形式で保存されます[y/N(Enter)] ').strip()
if not confirm == 'y' and not confirm == 'Y':
	sys.exit(0)


# --- IDリストからタイトルと投稿者を取得
csv_list = []
csv_text = ''
print('')
for i in range(len(id_list)):
	csv_list.append(tool.fetchMaterialInfo(id_list[i]))
print('')


# --- 取得したデータをcsvに保存
for i in range(len(csv_list)):
	csv_list[i] = ','.join(csv_list[i])
csv_text = '\n'.join(csv_list)
with open(base_path+'/IDs.csv', mode='w', encoding='cp932') as f:
	f.write(csv_text)
input('Enterで終了:')
