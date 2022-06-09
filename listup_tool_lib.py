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

# 「ニコニコ素材リストアップツール ライブラリ」by @is_ptcm
# メインスクリプトと関数をまとめたスクリプトを分けることにより可読性の向上を目指す
VERSION = 'v0.8.1'


# --- パッケージ読み込み
import os.path
import sys
import time
import json
import re
import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup


# --- エクスポート用HTMLテンプレの定義
html_template = '''\
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<style>
		body {
			margin     : 0.5rem auto;
			max-width  : 1080px;
			overflow-x : hidden;
		}
		.ids-area {
			margin      : 1rem 0.5rem;
			white-space : nowrap;
		}
		.ids-area #id-list {
			max-width     : 1080px;
			text-overflow : ellipsis;
			display       : inline-block;
			overflow-x    : hidden;
		}
		table {
			border-collapse : collapse;
			margin          : 0px auto;
			width           : 100%;
		}
		td, th {
			border : 1px solid #222;
		}
		td:nth-child(1), td > input[type="checkbox"] { cursor : pointer; }
		td:nth-child(-n+2) {
			text-align : center;
		}
		.thumbnail {
			max-height : 6rem;
		}
	</style>
	<script type="text/javascript">
		/* --- IDをリストアップ --- */
		const generateIdList = () => {
			const idSpan     = document.getElementById('id-list');
			const lastHeight = idSpan.offsetHeight;
			const checkboxes = [... document.getElementsByClassName('id-check')];
			let idsText      = '';
			checkboxes.forEach(box => {
				if (box.checked) idsText += box.id + ' ';
			});
			idSpan.textContent = idsText;
			window.scrollBy(0, idSpan.offsetHeight-lastHeight);
		};
		document.addEventListener('DOMContentLoaded', () => {
			generateIdList();
			const checkboxes = [... document.getElementsByClassName('id-check')];
			checkboxes.forEach(box => {
				box.addEventListener('change', generateIdList);
				box.parentNode.addEventListener('click', event => {
					if (event.target.tagName.toLowerCase() !== 'td') return;
					event.currentTarget.children[0].checked = !event.currentTarget.children[0].checked;
					generateIdList();
				});
			});
		});
		/* --- IDをコピーする --- */
		const copyIds = () => {
			const idSpan = document.getElementById('id-list');
			navigator.clipboard.writeText(idSpan.textContent);
		};
		document.addEventListener('DOMContentLoaded', () => {
			document.getElementById('copy-ids').addEventListener('click', copyIds);
		});
	</script>
</head>
<body>
<div class="ids-area">
	<button id="copy-ids">IDリストをコピー</button><br><span id="id-list"></span>
</div>
<table>
	<thead>
		<tr>
			<th>■</th>
			<th>サムネイル</th>
			<th>タイトル</th>
			<th>投稿者</th>
		</tr>
	</thead>
	<tbody>{content}</tbody>
</table>
</body>
</html>\
'''


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
	# すべてのIDを1列にまとめる
	id_text = '[1-line]\n' + ' '.join(id_list) + '\n'
	# 10件ごとにまとめる
	id_text += '\n[each-10-ids]\n'
	if len(id_list) < 1:
		return ''
	for i in range(len(id_list)):
		if i % 10 == 9 or i == len(id_list) - 1:
			id_text = id_text + id_list[i] + '\n'
		else:
			id_text = id_text + id_list[i] + ' '
	return id_text[0:-1]


# --- 取得したタイトルや投稿者などの情報からクレジットテキスト生成
def generateCreditText(list_contents, text_format):
	text_credit = ''
	for content in list_contents:
		text_credit += text_format.replace('%id%', content[0]).replace('%title%', content[1]).replace('%creator%', content[2]).replace('%url%', content[3]) + '\n'
	return text_credit


# --- HTMLを生成
def generateHTML(info_list):
	content = ''
	for info in info_list:
		checked_attr = ' checked="true"'
		if info['title'] == '削除された動画' or info['title'] == '(取得失敗)':
			checked_attr = ''
		content += f'<tr>'
		content += f'<td><input type="checkbox" id="{info["id"]}" class="id-check"{checked_attr}></td>'
		content += f'<td><a href="{info["URL"]}" target="_blank"><img src="{info["thumbnailURL"]}" class="thumbnail"></a></td>'
		if len(info['audioURL']) < 1:
			content += f'<td>{info["id"]}<br>{info["title"]}</td>'
		else:
			content += f'<td>{info["id"]}<br>{info["title"]}<br><audio controls src="{info["audioURL"]}"></td>'
		if len(info['userID']) < 1:
			content += f'<td>{info["username"]}</td>'
		else:
			if info['id'].startswith('nc'):
				content += f'<td><a href="https://commons.nicovideo.jp/users/{info["userID"]}?ref=listup-tool" target="_blank">{info["username"]}</a></td>'
			elif info['id'].startswith('im'):
				content += f'<td><a href="https://seiga.nicovideo.jp/user/illust/{info["userID"]}?ref=listup-tool" target="_blank">{info["username"]}</a></td>'
			elif info['id'].startswith('td'):
				content += f'<td><a href="https://3d.nicovideo.jp/users/{info["userID"]}?ref=listup-tool" target="_blank">{info["username"]}</a></td>'
			else:
				content += f'<td><a href="https://www.nicovideo.jp/user/{info["userID"]}?ref=listup-tool" target="_blank">{info["username"]}</a></td>'
		content += f'</tr>'
	return html_template.replace('{content}', content)


# --- 素材IDからID、タイトル、投稿者、サムネ、URLの配列を取得
def fetchMaterialInfo(id):
	# 返却用オブジェクトを生成
	material_info = {
		'id'           : id,
		'title'        : '(取得失敗)',
		'username'     : '(取得失敗)',
		'userID'       : '',
		'thumbnailURL' : '',
		'URL'          : '',
		'audioURL'     : ''
	}
	# 素材種別からURLを作る
	head = id[:2]
	print('+ '+id, end='')
	if head == 'sm':
		material_info['URL'] = 'https://www.nicovideo.jp/watch/' + id
	elif head == 'im':
		material_info['URL'] = 'https://seiga.nicovideo.jp/seiga/' + id
	elif head == 'nc':
		material_info['URL'] = 'https://commons.nicovideo.jp/material/' + id
	elif head == 'td':
		material_info['URL'] = 'https://3d.nicovideo.jp/works/' + id
	# 作品情報を取得
	work_text = ''
	work_info = []
	try:
		work_text = urlopen(f'https://public-api.commons.nicovideo.jp/v1/tree/node/{id}?with_meta=1').read()
		work_info = json.loads(work_text)
	except (json.decoder.JSONDecodeError, urllib.error.URLError):
		print(' -> 作品情報の取得に失敗')
		return material_info
	work_info                     = work_info['data']['node']
	material_info['title']        = work_info['title']
	material_info['userID']       = str(work_info['userId'])
	material_info['thumbnailURL'] = work_info['thumbnailURL'].replace('size=l', 'size=s')
	if work_info['contentKind'] == 'commons' and work_info['commonsMaterialKind'] == 'audio':
		material_info['audioURL'] = f'https://commons.nicovideo.jp/api/preview/get?cid={id.replace("nc","")}'
	# ユーザー情報を取得
	user_text = ''
	user_info = []
	try:
		user_text = urlopen(f'https://account.nicovideo.jp/api/public/v1/users/{work_info["userId"]}.json').read()
		user_info = json.loads(user_text)
	except (json.decoder.JSONDecodeError, urllib.error.URLError):
		print(' -> ユーザー情報の取得に失敗')
		return material_info
	user_info                 = user_info['data']
	material_info['username'] = user_info['nickname']
	print(f' -> {material_info["title"]} by {material_info["username"]}')
	return material_info


# --- バージョン取得
def getVersion():
	return VERSION


# --- 設定ファイルを読み込み
def readConfig():
	path_config = os.path.dirname(os.path.abspath(sys.argv[0])) + '/config.txt'
	text_config = []
	list_config = {}
	if not os.path.isfile(path_config):
		return list_config
	with open(path_config, mode='r', encoding='utf-8') as f:
		text_config = f.read().replace('\r', '')
		text_config = text_config.split('\n')
	for i in range(len(text_config)):
		if '=' in text_config[i]:
			text_config[i]    = text_config[i].split('=')
			text_config[i][0] = text_config[i][0].strip()
			text_config[i][1] = text_config[i][1].strip()
			list_config[text_config[i][0]] = text_config[i][1]
	return list_config


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


# --- ファイル名重複をチェック
def checkDuplicatedFile(dirname, postfix = ''):
	filenames = [
		os.path.abspath(dirname + f'/Ids{postfix}.txt'),
		os.path.abspath(dirname + f'/IDs{postfix}.csv'),
		os.path.abspath(dirname + f'/credits{postfix}.txt'),
		os.path.abspath(dirname + f'/credits{postfix}.html')
	]
	for name in filenames:
		if os.path.isfile(name):
			return True
	return False
