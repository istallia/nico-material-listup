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
