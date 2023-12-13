#!python3
#-*- coding: utf-8 -*-

# Copyright (C) 2020-2023 istallia
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

# 「ニコニコ素材リストアップツール 情報取得テスト」by @is_ptcm
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import listup_tool_lib as tool


# --- 動画情報の取得テスト
def test_fetch_video():
    info = tool.fetchMaterialInfo('sm37664648') # 【動画投稿支援】IDリストをコンテンツツリーに一括で流し込める拡張機能作った【VOICEROID】
    assert info['id'] == 'sm37664648'
    assert info['title'] != '(取得失敗)'
    assert info['username'] != '(取得失敗)'
    assert len(info['userID']) > 0
    assert len(info['thumbnailURL']) > 0
    assert len(info['URL']) > 0
    assert len(info['audioURL']) < 1


# --- コモンズ素材の情報取得テスト (音声)
def test_fetch_sound():
    info = tool.fetchMaterialInfo('nc148600') # プロフェッショナル 仕事の流儀　ポーン音
    assert info['id'] == 'nc148600'
    assert info['title'] != '(取得失敗)'
    assert info['username'] != '(取得失敗)'
    assert len(info['userID']) > 0
    assert len(info['thumbnailURL']) > 0
    assert len(info['URL']) > 0
    assert len(info['audioURL']) > 0


# --- コモンズ素材の情報取得テスト (ライセンス)
def test_fetch_license():
    info = tool.fetchMaterialInfo('nc235556') # コモンズ20プレイヤー
    assert info['id'] == 'nc235556'
    assert info['title'] != '(取得失敗)'
    assert info['username'] != '(取得失敗)'
    assert len(info['userID']) > 0
    assert len(info['thumbnailURL']) > 0
    assert len(info['URL']) > 0
    assert len(info['audioURL']) < 1


# --- 静画の情報取得テスト
def test_fetch_image():
    info = tool.fetchMaterialInfo('im6111040') # デフォルメさとうささら立ち絵 表情差分
    assert info['id'] == 'im6111040'
    assert info['title'] != '(取得失敗)'
    assert info['username'] != '(取得失敗)'
    assert len(info['userID']) > 0
    assert len(info['thumbnailURL']) > 0
    assert len(info['URL']) > 0
    assert len(info['audioURL']) < 1


# --- ニコニ立体の情報取得テスト
def test_fetch_model():
    info = tool.fetchMaterialInfo('td14712') # ニコニ立体ちゃん
    assert info['id'] == 'td14712'
    assert info['title'] != '(取得失敗)'
    assert info['username'] != '(取得失敗)'
    assert len(info['userID']) > 0
    assert len(info['thumbnailURL']) > 0
    assert len(info['URL']) > 0
    assert len(info['audioURL']) < 1
