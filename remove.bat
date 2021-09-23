@echo off
chcp 932
rem ニコニコ素材リストアップツール(v0.7)をレジストリから削除するバッチファイル

setlocal

reg delete "HKEY_CURRENT_USER\Software\Classes\SystemFileAssociations\.aup" /f
reg delete "HKEY_CURRENT_USER\Software\Classes\SystemFileAssociations\.ccproj" /f
reg delete "HKEY_CURRENT_USER\Software\Classes\*\shell\コモンズ素材の一覧を生成する" /f
reg delete "HKEY_CURRENT_USER\Software\Classes\*\shell\ニコニコ素材の一覧を生成する" /f
reg delete "HKEY_CURRENT_USER\Software\Classes\Directory\shell\ニコニコ素材の一覧を生成する" /f
