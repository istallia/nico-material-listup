#!python3
#-*- coding: utf-8 -*-

# 「ニコニコ素材リストアップツール ライブラリ」by @is_ptcm
# メインスクリプトと関数をまとめたスクリプトを分けることにより可読性の向上を目指す
VERSION = 'v0.7.3'


# --- パッケージ読み込み
import os.path
import sys
import time
import json
import re
import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup


# --- ファイルからIDを抽出
def getIdList(file_path, use_path):
	# 下準備
	print('+ '+os.path.basename(file_path), end='')
	content = b''
	# ファイルを読み込み
	with open(file_path, mode='rb') as f:
		content = f.read()
	if len(content) < 1:
		print(' -> 空、または読み込み失敗')
		return []
	content   = content.replace(b'\x00', b'')
	root, ext = os.path.splitext(file_path)
	if ext[1:].lower() == 'aup':
		# AviUtlでは連続する数字の短縮が行われる
		for length in range(3,10):
			for num in range(10):
				content = re.sub(bytes([0x80+length])+bytes([0x30+num])+b'[\x01-\x79]', b'%d'%(num)*length, content)
	content = re.sub(b'[\\x80-\\xff][^\\x2e]', b'_', content)
	# 抽出する (ファイルパス)
	if use_path:
		path_list = re.findall(b'(?:\\w:)?(?:[\\\\/]{1,2}[^\\/\\\\:\\*\\?<>|\\n\\t\\x01-\\x1f]{1,127})+\\.[a-zA-Z0-9][-\\w]{1,10}[a-zA-Z0-9]', content)
		content   = b'\n'.join(path_list)
	# 抽出する (ID直接検索)
	id_list = re.findall(b'(?:[^a-zA-Z0-9]|^)((nc|im|sm|td)\\d{2,12})(?=[^a-zA-Z0-9]|$)', content)
	id_list = list(set(id_list))
	for i in range(len(id_list)):
		id_list[i] = id_list[i][0].decode('utf-8')
	print(' -> '+str(len(id_list))+'件のIDを抽出')
	return id_list


# --- IDリストの配列から10件ごとのテキストを生成
def generateIdListText(id_list):
	id_text = ''
	if len(id_list) < 1:
		return ''
	for i in range(len(id_list)):
		if i % 10 == 9 or i == len(id_list) - 1:
			id_text = id_text + id_list[i] + '\n'
		else:
			id_text = id_text + id_list[i] + ' '
	return id_text[0:-1]


# --- 素材IDからID、タイトル、投稿者、URLの配列を取得
def fetchMaterialInfo(id):
	# 素材種別からURLを作る
	head = id[:2]
	url  = ''
	print('+ '+id, end='')
	if head == 'sm':
		url = 'https://www.nicovideo.jp/watch/' + id
	elif head == 'im':
		url = 'https://seiga.nicovideo.jp/seiga/' + id
	elif head == 'nc':
		url = 'https://commons.nicovideo.jp/material/' + id
	elif head == 'td':
		url = 'https://3d.nicovideo.jp/works/' + id
	# 必要な情報をスクレイピング
	max_retry  = 3
	is_success = False
	title      = ''
	creator    = ''
	for i in range(max_retry):
		try:
			# html取得
			html = urlopen(url).read()
			soup = BeautifulSoup(html, 'html.parser')
			# タイトルと投稿者を取得
			if head == 'sm':
				title   = soup.select_one('meta[name="twitter:title"]')['content']
				creator = json.loads(soup.select_one('script[type="application/ld+json"]').string)
				creator = creator['author']['name']
			elif head == 'im':
				title   = soup.select_one('ul.sg_pankuzu > li.active > span[itemprop="title"]').text
				creator = soup.select_one('div.lg_txt_illust > strong').text
			elif head == 'nc':
				title   = soup.select_one('div.materialHeadTitle').text
				creator = soup.select_one('div.mUserProfile a.materialUsername').text
			elif head == 'td':
				title   = soup.select_one('div.work-author-name').text
				creator = soup.select_one('h1.work-info-title').text
			print(' -> ' + title + ', ' + creator)
			is_success = True
			break
		except urllib.error.HTTPError as e:
			# 取得に失敗: ネットワークエラー
			print(' -> 素材ページにアクセスできませんでした')
			break
		except (IndexError, AttributeError):
			# 取得に失敗: 指定要素がない
			if i == max_retry-1:
				print(' -> タイトルと投稿者の取得に失敗')
		except Exception as e:
			with open(os.path.dirname(os.path.abspath(sys.argv[0]))+'/error.log', mode='w', encoding='utf-8') as f:
				f.write(e)
			sys.exit(1)
	# カンマは後で使うので置換
	title   = title.replace(',', '，')
	creator = creator.replace(',', '，')
	# 取得に成功していればその値を返す
	if is_success:
		return [id, title, creator, url]
	else:
		return [id, '(取得失敗)', '(取得失敗)', url]


# --- バージョン取得
def getVersion():
	return VERSION


# --- 更新を確認(7日ごと)
def checkUpdate():
	# 最終確認日時(unix時間)を取得
	last_time = 0
	file_name = os.path.dirname(os.path.abspath(sys.argv[0])) + '/_version_check'
	if os.path.isfile(file_name):
		last_time_text = '0'
		with open(file_name, mode='r', encoding='ascii') as f:
			last_time_text = f.read()
		last_time = int(last_time_text)
	# 現在時刻と比較する
	current_time = int(time.time())
	if last_time > current_time-604800:
		return
	# オンラインでバージョン確認
	last_version = VERSION
	try:
		# html取得
		html = urlopen('https://textblog.minibird.jp/twitter/').read()
		soup = BeautifulSoup(html, 'html.parser')
		# バージョン文字列取得
		last_version = soup.select_one('#listup-tool-last-version').text
		last_version = last_version[12:].replace('.zip', '').replace('-', '.')
	except:
		pass
	# 更新があれば通知
	if last_version != VERSION:
		print('\n現在の最新版は' + last_version + 'です。\n')
	# 最終確認日時を更新
	with open(file_name, mode='w', encoding='ascii') as f:
		f.write(str(current_time))
	return
