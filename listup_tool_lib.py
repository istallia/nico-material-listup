#!python3
#-*- coding: utf-8 -*-

# 「ニコニコ素材リストアップツール ライブラリ」by @is_ptcm
# メインスクリプトと関数をまとめたスクリプトを分けることにより可読性の向上を目指す


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
