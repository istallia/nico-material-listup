#!python3
#coding:utf-8

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
print('------ 「ニコニコ素材リストアップツール」v0.6.0 by @is_ptcm ------\n')

# --- 読み出すaupファイルをコマンドライン引数より取得
if len(sys.argv) < 2:
	print('ファイル名(or パス)を入力してください: ', end='')
	filename = input().strip()
else:
	filename = sys.argv[1]
filename = os.path.abspath(filename)

# --- 変数の用意
IDs      = []
length   = 0
IDs_list = ''

# --- IDリストをファイルから取得する関数
def getIdsList(filename):
	# ファイル名を表示
	print('ファイルを読み込みます: '+os.path.basename(filename))
	root, ext = os.path.splitext(filename)
	# Recotte Studioのプロジェクトファイルの場合
	if ext == '.ccproj':
		# 読み出し
		ccproj = {}
		with open(filename, mode='r', encoding='utf-8') as f:
			ccproj = json.load(f)
		if len(ccproj) < 1:
			print('ファイルが存在しないか、中身が空っぽです。')
			return
		print('ファイルを読み込めました。')
		# 検索
		for item in ccproj['file-items']:
			search_result = re.search('((nc|im|sm|td)\d{2,12})', item['apath'])
			if not search_result == None:
				IDs.append(search_result.groups()[0])
		IDs    = list(set(IDs))
		length = len(IDs)
		return IDs
	# その他のプロジェクトファイルの場合
	else:
		# 読み出し
		aup = b''
		with open(filename,mode='rb') as f:
			aup = f.read()
		if len(aup) < 1:
			print('ファイルが存在しないか、中身が空っぽです。')
			return
		print('ファイルを読み込めました。')
		# 検索
		IDs    = re.findall(b'[^a-zA-Z0-9]*((nc|im|sm|td)\\d{2,12})[^a-zA-Z0-9]', aup)
		IDs    = list(set(IDs))
		length = len(IDs)
		for i in range(length):
			IDs[i] = IDs[i][0].decode('utf-8')
		return IDs

# --- ディレクトリが指定されたら中身を全部見る
if os.path.isdir(filename):
	name_list = glob.glob(filename+'/**', recursive=True)
	for name in name_list:
		if os.path.isfile(name):
			IDs.extend(getIdsList(name))
elif os.path.isfile(filename):
	IDs = getIdsList(filename)
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
				m_title   = soup.select_one('div.commons_title').text
				m_creator = soup.select_one('div.m_user_profile a.userlink').text
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
	csv_text = csv_text + IDs[i] + ', ' + titles[i].replace(',','，') + ',' + creators[i].replace(',','，') + '\n'
csv_text = csv_text[0:-1]
# csv_text = csv_text.replace(chr(0xff5e), chr(0x301c))
# csv_text = csv_text.replace(chr(0xff0d), chr(0x2212))
# csv_text = csv_text.replace(chr(0xffe0), chr(0x00a2))
# csv_text = csv_text.replace(chr(0xffe1), chr(0x00a3))
# csv_text = csv_text.replace(chr(0xffe2), chr(0x00ac))
# csv_text = csv_text.replace(chr(0x2015), chr(0x2014))
# csv_text = csv_text.replace(chr(0x2225), chr(0x2225))
with open(os.path.dirname(filename)+'\\Ids.csv', mode='w', encoding='cp932') as f:
	f.write(csv_text)

# --- 終了待ち
input('Enterで終了: ')
