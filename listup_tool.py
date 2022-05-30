#!python3
#-*- coding: utf-8 -*-

# Copyright (C) 2020-2022 istallia
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# 「ニコニコ素材リストアップツール」by @is_ptcm
#
# ニコニコの素材を動画編集ソフトのプロジェクトファイルから抽出してリストアップしてくれるツール
# 10件ずつなのでコピペでコンテンツツリーに持って行く


# --- パッケージ読み込み
import os.path
import datetime
import sys
import re
import glob
import copy
import listup_tool_lib as tool


# --- タイトルを描画
print('------ 「ニコニコ素材リストアップツール」'+tool.getVersion()+' by @is_ptcm ------\n')
config = tool.readConfig()
if 'check-update' in config and config['check-update'].lower() != 'true':
	print('\nアップデートチェッカは無効化されています。\n')
else:
	tool.checkUpdate()


# --- 除外リストを作成
exclude_csv_path = os.path.dirname(os.path.abspath(sys.argv[0])) + '/exclude_ext_list.txt'
exclude_ext_list = [
	'lwi'  ,'avi'  ,'mp4'  ,'flv'  ,'mov' ,'asf'  ,'mkv'  ,'webm' ,'mpg'   ,'m2ts' ,
	'mpg'  ,'mpeg' ,'wav'  ,'mp3'  ,'ogg' ,'wma'  ,'m4a'  ,'flac' ,'aif'   ,'aiff' ,
	'aac'  ,'mid'  ,'midi' ,'jpg'  ,'jpe' ,'jpeg' ,'png'  ,'gif'  ,'bmp'   ,'webp' ,
	'psd'  ,'apd'  ,'ai'   ,'mdp'  ,'ico' ,'zip'  ,'lzh'  ,'7z'   ,'gz'    ,'tar'  ,
	'rar'  ,'exe'  ,'dll'  ,'msi'  ,'sys' ,'iso'  ,'docx' ,'dotx' ,'xlsx'  ,'xlsm' ,
	'pptx' ,'pptm' ,'potx' ,'potm' ,'db'  ,'pdf'  ,'lnk'  ,'url'  ,'cache' ,'user' ,
	'auf'  ,'auo'  ,'aui'  ,'bak'  ,'pdb' ,'sln'
]
if os.path.isfile(exclude_csv_path):
	# 追加除外リストが存在すれば読み込む
	content = ''
	with open(exclude_csv_path, mode='r', encoding='utf-8') as f:
		content = f.read()
	exclude_ext_list.extend(re.findall(r'[-\w]+', content))


# --- 2段階抽出を利用するリストを作成
step2_csv_path = os.path.dirname(os.path.abspath(sys.argv[0])) + '/2step_ext_list.txt'
step2_ext_list = ['aup', 'pmm', 'emm']
if os.path.isfile(step2_csv_path):
	# 2段階抽出を利用する拡張子リストが存在すれば読み込む
	content = ''
	with open(step2_csv_path, mode='r', encoding='utf-8') as f:
		content = f.read()
	step2_ext_list.extend(re.findall(r'[-\w]+', content))


# --- 読み出すファイル/フォルダをコマンドライン引数から取得(複数可)
base_path  = ''
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
base_path  = os.path.dirname(input_list[0])


# --- すべてのファイル名を取得
file_list = []
dir_list  = []
for i in range(len(input_list)):
	root, ext = os.path.splitext(input_list[i])
	if os.path.isdir(input_list[i]):
		dir_list.append(input_list[i])
	elif os.path.isfile(input_list[i]) and not (ext[1:].lower() in exclude_ext_list):
		file_list.append(input_list[i])
for i in range(len(dir_list)):
	files = [p for p in glob.glob(dir_list[i]+'\\**', recursive=True) if os.path.isfile(p)]
	for j in range(len(files)):
		root, ext = os.path.splitext(files[j])
		if not (ext[1:].lower() in exclude_ext_list):
			file_list.append(os.path.abspath(files[j]))
if len(file_list) < 1:
	input('\n抽出可能なファイルが存在しません。Enterで終了します:')
	sys.exit(0)


# --- すべてのIDを取得
print('')
id_list = []
for i in range(len(file_list)):
	root, ext = os.path.splitext(file_list[i])
	id_list.extend(tool.getIdList(file_list[i], ext[1:].lower() in step2_ext_list))
if len(id_list) < 1:
	input('ニコニコ素材が見つかりませんでした。Enterで終了します:')
	sys.exit(0)
id_list = list(set(id_list))
print('+ 合計' + str(len(id_list)) + '件のIDを抽出\n')


# --- 同名ファイルがあるか確認
postfix = ''
if 'overwrite-mode' in config and config['overwrite-mode'] == 'datetime':
	now     = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
	postfix = '-' + now.strftime('%Y%m%d-%H%M%S')
if 'overwrite-mode' in config and tool.checkDuplicatedFile(base_path):
	if config['overwrite-mode'] == 'number':
		postfix_candidate = ''
		for i in range(1000):
			postfix_candidate = f' ({i+1})'
			if not tool.checkDuplicatedFile(base_path, postfix_candidate):
				break
		if len(postfix_candidate) > 0:
			postfix = postfix_candidate
		else:
			config['overwrite-mode'] = 'confirm'
	if config['overwrite-mode'] == 'confirm':
		confirm_overwrite = input('同名のファイルがあります。上書きしますか？ [y/N(Enter)] ').strip()
		if confirm_overwrite.lower() != 'y':
			sys.exit(0)


# --- IDリストを保存し、さらにタイトルや投稿者も取得するか確認する
id_text = tool.generateIdListText(id_list)
with open(base_path+f'/IDs{postfix}.txt', mode='w', encoding='cp932') as f:
	f.write(id_text)
confirm = input('オンラインでタイトルと投稿者を取得しますか？結果はCSV形式で保存されます[y/N(Enter)] ').strip()
if not confirm.lower() == 'y':
	sys.exit(0)


# --- IDリストからタイトルと投稿者を取得
info_list = []
csv_list  = []
csv_text  = ''
print('')
for i in range(len(id_list)):
	material_info = tool.fetchMaterialInfo(id_list[i])
	info_list.append(material_info)
	csv_list.append([
		material_info['id'],
		material_info['title'],
		material_info['username'],
		material_info['URL']
	])
print('')


# --- 取得したデータをクレジットテキストとして保存
if 'credit-format' in config:
	text = tool.generateCreditText(csv_list, config['credit-format'])
	with open(base_path+f'/credits{postfix}.txt', mode='w', encoding='cp932', errors="ignore") as f:
		f.write(text)


# 取得したデータをHTMLとして保存
if 'export-html' in config and config['export-html'].lower() == 'true':
	html = tool.generateHTML(info_list)
	with open(base_path+f'/credits{postfix}.html', mode='w', encoding='utf-8', errors="ignore") as f:
		f.write(html)


# --- 取得したデータをcsvに保存
for i in range(len(csv_list)):
	csv_list[i] = ','.join(csv_list[i])
csv_text = '\n'.join(csv_list)
with open(base_path+f'/IDs{postfix}.csv', mode='w', encoding='cp932', errors="ignore") as f:
	f.write(csv_text)
input('Enterで終了:')
