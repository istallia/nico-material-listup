#!python3
#-*- coding: utf-8 -*-

# 「ニコニコ素材リストアップツール ライブラリ」by @is_ptcm
# メインスクリプトと関数をまとめたスクリプトを分けることにより可読性の向上を目指す


# --- パッケージ読み込み
import os.path
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
	content = content.replace(b'\x00', b'')
	# 抽出する (ファイルパス)
	if use_path:
		path_list = re.findall(b'(?:\\w:)?(?:[\\\\/][^\\/\\\\:\\*\\?<>|\\n\\t\\x01-\\x1f]{1,127})+\\.[-\\w]{1,12}', content)
		content   = b'\n'.join(path_list)
	# 抽出する (ID直接検索)
	id_list = re.findall(b'(?:\\b|^)((nc|im|sm|td)\\d{2,12})(?=\\b|$)', content)
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
		except IndexError:
			# 取得に失敗: 指定要素がない
			if i == max_retry-1:
				print(' -> タイトルと投稿者の取得に失敗')
	# カンマは後で使うので置換
	title   = title.replace(',', '，')
	creator = creator.replace(',', '，')
	# 取得に成功していればその値を返す
	if is_success:
		return [id, title, creator, url]
	else:
		return [id, '(取得失敗)', '(取得失敗)', url]
