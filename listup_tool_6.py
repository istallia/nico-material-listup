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

# --- 標準パッケージ
import os.path
import sys
import time
import json
import re
import urllib
import glob
from urllib.request import urlopen
from bs4 import BeautifulSoup

# --- タイトルを描画
print('------ 「ニコニコ素材リストアップツール」v0.6.5 by @is_ptcm ------\n')

# --- 読み出すaupファイルをコマンドライン引数より取得
if len(sys.argv) < 2:
	print('ファイル名(or パス)を入力してください: ', end='')
	filename = input().strip()
else:
	filename = sys.argv[1]
filename = os.path.abspath(filename)

# --- 変数の用意
exclude_ext_list = ['lwi', 'avi', 'mp4', 'flv', 'mov', 'asf', 'mkv', 'webm', 'mpg', 'm2ts', 'mpg', 'mpeg', 'wav', 'mp3', 'ogg', 'wma', 'm4a', 'flac', 'aif', 'aiff', 'aac', 'mid', 'midi', 'jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp', 'ico', 'zip', 'lzh', '7z', 'gz', 'tar', 'exe', 'dll']
IDs              = []
length           = 0
IDs_list         = ''

# --- IDリストをファイルから取得する関数
def getIdsList(filename):
	# ファイル名を表示
	print('ファイルを読み込みます: '+os.path.basename(filename), end='')
	root, ext = os.path.splitext(filename)
	# Recotte Studioのプロジェクトファイルの場合
	if ext == '.ccproj':
		# 読み出し
		ccproj = {}
		with open(filename, mode='r', encoding='utf-8') as f:
			ccproj = json.load(f)
		if len(ccproj) < 1:
			print(' -> 空、または読み込み失敗')
			return []
		# 検索
		IDs = []
		for item in ccproj['file-items']:
			search_result = re.search('((nc|im|sm|td)\d{2,12})', item['apath'])
			if not search_result == None:
				IDs.append(search_result.groups()[0])
		IDs    = list(set(IDs))
		length = len(IDs)
		print(' -> '+str(length)+'件のIDを抽出')
		return IDs
	# その他のプロジェクトファイルの場合
	else:
		# 読み出し
		aup = b''
		with open(filename,mode='rb') as f:
			aup = f.read()
		if len(aup) < 1:
			print(' -> 空、または読み込み失敗')
			return []
		# 検索
		aup    = aup.replace(b'\x00', b'')
		IDs    = re.findall(b'(?:[^a-zA-Z0-9]|^)((nc|im|sm|td)\\d{2,12})(?=[^a-zA-Z0-9]|$)', aup)
		IDs    = list(set(IDs))
		length = len(IDs)
		for i in range(length):
			IDs[i] = IDs[i][0].decode('utf-8')
		print(' -> '+str(length)+'件のIDを抽出')
		return IDs

# --- ディレクトリが指定されたら中身を全部見る
if os.path.isdir(filename):
	name_list = glob.glob(filename+'/**', recursive=True)
	for name in name_list:
		file_title, ext = os.path.splitext(name);
		if os.path.isfile(name) and not ext[1:].lower() in exclude_ext_list:
			IDs.extend(getIdsList(name))
elif os.path.isfile(filename):
	IDs = getIdsList(filename)
IDs    = list(set(IDs))
length = len(IDs)

# --- 整列＆出力
print('')
for i in range(length):
	if i % 10 == 9 or i == length - 1:
		print(IDs[i])
		IDs_list = IDs_list + IDs[i] + '\n'
	else:
		print(IDs[i]+' ', end='')
		IDs_list = IDs_list + IDs[i] + ' '
IDs_list = IDs_list[0:-1]

# --- IDが存在しない場合はファイルを出さずに終了する
if len(IDs) < 1:
	input('\nニコニコ素材が見つかりませんでした。Enterで終了します: ')
	sys.exit(0)

# --- IDリストをテキストファイルに出力
with open(os.path.dirname(filename)+'\\Ids.txt', mode='w', encoding='sjis') as f:
	f.write(IDs_list)
print('')

# --- CSVを生成するか確認
confirm = input('オンラインでタイトルと作者を取得しますか？結果はCSV形式で保存されます[y/N(Enter)] ').strip()
if not confirm == 'y' and not confirm == 'Y':
	sys.exit(0)

# --- タイトルと作者を取得
titles   = []
creators = []
for material_id in IDs:
	retry_count = 0
	html        = ''
	if material_id[:2] == 'nc':
		while retry_count >= 0 and retry_count < 4:
			try:
				print('タイトルと作者を取得: '+material_id, end='')
				html      = urlopen('http://commons.nicovideo.jp/material/'+material_id).read()
				soup      = BeautifulSoup(html, 'html.parser')
				m_title   = soup.select_one('div.materialHeadTitle').text
				m_creator = soup.select_one('div.mUserProfile a.materialUsername').text
				print(' -> '+m_title+', '+m_creator)
				titles.append(m_title)
				creators.append(m_creator)
				retry_count = -1
			except urllib.error.HTTPError as e:
				print('\nエラーコード: ', end='')
				print(e.code)
				titles.append('(取得に失敗)')
				creators.append('(取得に失敗)')
				retry_count = -1
			except (IndexError, AttributeError):
				retry_count += 1
				if retry_count >= 4:
					print('\nIDの取得に失敗。ニコニ・コモンズに障害が発生しているか、素材が削除された可能性があります。')
					titles.append('(取得に失敗)')
					creators.append('(取得に失敗)')
				else:
					print('\nIDの取得に失敗。再試行します...')
			time.sleep(0.3)
	elif material_id[:2] == 'im':
		while retry_count >= 0 and retry_count < 4:
			try:
				print('タイトルと作者を取得: '+material_id, end='')
				html      = urlopen('https://seiga.nicovideo.jp/seiga/'+material_id).read()
				soup      = BeautifulSoup(html, 'html.parser')
				m_title   = soup.select_one('ul.sg_pankuzu > li.active > span[itemprop="title"]').text
				m_creator = soup.select_one('div.lg_txt_illust > strong').text
				print(' -> '+m_title+', '+m_creator)
				titles.append(m_title)
				creators.append(m_creator)
				retry_count = -1
			except urllib.error.HTTPError as e:
				print('\nエラーコード: ', end='')
				print(e.code)
				titles.append('(取得に失敗)')
				creators.append('(取得に失敗)')
				retry_count = -1
			except IndexError:
				retry_count += 1
				if retry_count >= 4:
					print('\nIDの取得に失敗。ニコニコ静画に障害が発生しているか、素材が削除された可能性があります。')
					titles.append('(取得に失敗)')
					creators.append('(取得に失敗)')
				else:
					print('\nIDの取得に失敗。再試行します...')
			time.sleep(0.3)
	elif material_id[:2] == 'sm':
		while retry_count >= 0 and retry_count < 4:
			try:
				print('タイトルと作者を取得: '+material_id, end='')
				html      = urlopen('https://www.nicovideo.jp/watch/'+material_id).read()
				soup      = BeautifulSoup(html, 'html.parser')
				m_title   = soup.select_one('meta[name="twitter:title"]')['content']
				m_creator = json.loads(soup.select_one('script[type="application/ld+json"]').string)
				m_creator = m_creator['author']['name']
				print(' -> '+m_title+', '+m_creator)
				titles.append(m_title)
				creators.append(m_creator)
				retry_count = -1
			except urllib.error.HTTPError as e:
				print('\nエラーコード: ', end='')
				print(e.code)
				titles.append('(取得に失敗)')
				creators.append('(取得に失敗)')
				retry_count = -1
			except IndexError:
				retry_count += 1
				if retry_count >= 4:
					print('\nIDの取得に失敗。ニコニコ動画に障害が発生しているか、素材が削除された可能性があります。')
					titles.append('(取得に失敗)')
					creators.append('(取得に失敗)')
				else:
					print('\nIDの取得に失敗。再試行します...')
			time.sleep(0.3)
	elif material_id[:2] == 'td':
		while retry_count >= 0 and retry_count < 4:
			try:
				print('タイトルと作者を取得: '+material_id, end='')
				html      = urlopen('https://3d.nicovideo.jp/works/'+material_id).read()
				soup      = BeautifulSoup(html, 'html.parser')
				m_title   = soup.select_one('div.work-author-name').text
				m_creator = soup.select_one('h1.work-info-title').text
				print(' -> '+m_title+', '+m_creator)
				titles.append(m_title)
				creators.append(m_creator)
				retry_count = -1
			except urllib.error.HTTPError as e:
				print('\nエラーコード: ', end='')
				print(e.code)
				titles.append('(取得に失敗)')
				creators.append('(取得に失敗)')
				retry_count = -1
			except IndexError:
				retry_count += 1
				if retry_count >= 4:
					print('\nIDの取得に失敗。ニコニ立体に障害が発生しているか、素材が削除された可能性があります。')
					titles.append('(取得に失敗)')
					creators.append('(取得に失敗)')
				else:
					print('\nIDの取得に失敗。再試行します...')
			time.sleep(0.3)
print('')

# --- csvファイルに出力
csv_text = ''
for i in range(length):
	csv_text = csv_text + IDs[i] + ', ' + titles[i].replace(',','，') + ',' + creators[i].replace(',','，')+ ','
	prefix   = IDs[i][:2]
	if prefix == 'nc':
		csv_text += 'https://commons.nicovideo.jp/material/' + IDs[i]
	elif prefix == 'sm':
		csv_text += 'https://www.nicovideo.jp/watch/' + IDs[i]
	elif prefix == 'im':
		csv_text += 'https://seiga.nicovideo.jp/seiga/' + IDs[i]
	elif prefix == 'td':
		csv_text += 'https://3d.nicovideo.jp/works/' + IDs[i]
	csv_text += '\n'
csv_text = csv_text[0:-1]
with open(os.path.dirname(filename)+'\\Ids.csv', mode='w', encoding='cp932', errors="ignore") as f:
	f.write(csv_text)

# --- 終了待ち
input('Enterで終了: ')
