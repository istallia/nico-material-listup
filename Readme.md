
# ニコニコ素材リストアップツール v0.7.0
(2021-09-20)

## 概要

動画編集ソフトのプロジェクトファイル等からニコニコの素材のIDを抽出し、コンテンツツリーに登録しやすい10件ごとのリストにまとめるツールです。  
元々はAviUtlとRecotteStudio用でしたが、仕組み的にどのソフトでもいけそうだったので内部でやってた制限を取っ払いました。  
ニコニコのサイトから素材の名前と作者を取得し、CSVファイルにまとめる機能もあります。  
IDをまとめたテキストファイルやCSVファイルはプロジェクトファイルのあるフォルダに出力されるため、右クリックメニューに登録して使うこともできます。

## 導入

zipをダウンロードし解凍したら、中にある`regist.bat`を管理者権限で実行してください。  
右クリックメニューに登録されます。  
(逆に登録解除したい場合は管理者権限で`remove.bat`を実行してください)

## 使い方

素材IDを抽出したいファイルまたはフォルダを右クリックし、メニューから「ニコニコ素材の一覧を生成する」を選択してください。  
ファイル指定時はファイルから、フォルダ指定時はフォルダ下のすべてのファイルからIDを抽出します。  
さらにオンラインでタイトルや投稿者を取得してcsvにまとめるか聞かれるので、必要に応じてyかNを入力してください。  
(この時点でIDをまとめたテキストファイル、IDs.txtは保存されています)

※複数ファイル/フォルダからのID抽出には対応できません。フォルダ指定をご活用ください。

## 対象となるファイル

素材はファイル名に素材IDを含む必要があります。sm、im、nc、tdの後に数字が2桁以上続くものが対象です。  
例えば、素材を以下のような名前で保存していれば使えます。

+ nc12345678.wav
+ nc12345678_いい感じの素材.png
+ 美しい景色(im12345678).gif
+ 【福袋】素材音声詰め合わせ[sm12345678].mp4
+ 【nc12345678】超イカしたサウンド.wav

※ v0.5からのアップデートでいろいろ試みてはいますが、ID周辺のバイナリによっては誤検知したり、検出漏れが発生する可能性があります。  
その場合は不具合のあったファイルor誤検知したIDの周辺のバイナリ情報(バイナリエディタのスクショ)をTwitterのDMなどに送ってくれれば対応します。

## 注意

+ 本ツールはニコニコ各サービスのWebサイトへアクセスします。多重起動するなど、むやみに負荷をかける行為はしないでください。
+ ニコニ・コモンズ、静画、動画、立体に対応しています。それ以外の素材を前項の形式のファイル名で保存していたとしても抽出することはできません。
+ 既に削除されている素材の名前や作者を取得することはできません。
+ 「nc数字」「im数字」「sm数字」「td数字」を検出するため、このような文字列がテキストオブジェクト等に含まれると検出されてしまいます。仕様にしておくので活用したい場合は活用してください。

## クレジット

制作者: イスターリャ(@is_ptcm)  
言語　: Python 3.8.2

※本ツールの二次配布はご遠慮ください。
