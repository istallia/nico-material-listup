@echo off
chcp 932
rem �R�����Y�f�ރ��X�g�A�b�v�c�[��(v0.2)�����W�X�g������폜����o�b�`�t�@�C��

setlocal

reg delete "HKEY_CURRENT_USER\Software\Classes\SystemFileAssociations\.aup" /f
reg delete "HKEY_CURRENT_USER\Software\Classes\SystemFileAssociations\.ccproj" /f
reg delete "HKEY_CURRENT_USER\Software\Classes\*\shell\�R�����Y�f�ނ̈ꗗ�𐶐�����" /f
reg delete "HKEY_CURRENT_USER\Software\Classes\*\shell\�j�R�j�R�f�ނ̈ꗗ�𐶐�����" /f
reg delete "HKEY_CURRENT_USER\Software\Classes\Directory\shell\�j�R�j�R�f�ނ̈ꗗ�𐶐�����" /f
