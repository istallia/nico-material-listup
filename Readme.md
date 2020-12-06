
# ニコニコ素材リストアップツール v0.6.3
(2020-12-06)

## 概要

動画編集ソフトのプロジェクトファイルからニコニコの素材のIDを抽出し、コンテンツツリーに登録しやすい10件ごとのリストにまとめるツールです。  
元々はAviUtlとRecotteStudio用でしたが、仕組み的にどのソフトでもいけそうだったので内部でやってた制限を取っ払いました。  
ニコニコのサイトから素材の名前と作者を取得し、CSVファイルにまとめる機能もあります。  
IDをまとめたテキストファイルやCSVファイルはプロジェクトファイルのあるフォルダに出力されるため、右クリックメニューに登録して使うこともできます。

## 使い方

プロジェクトファイルを本ツールにドラッグアンドドロップ(D&D)してください。または、ダブルクリックで起動した後にファイルパスを入力してください。  
IDの抽出が成功するとタイトルと作者を取得するか聞かれるので、必要に応じて操作してください。(この時点でテキストファイルは保存されています)

本ツールはレジストリを編集して右クリックメニューに登録すると、より便利に利用できます。  
使い方はプロジェクトファイルを右クリックし「ニコニコ素材の一覧を生成する」をクリックするだけ！  
今バージョンでは自動でレジストリに書き込んでくれるバッチファイルも付けました。「regist.bat」を管理者権限で実行してください。  
なお「remove.bat」は削除用です。いらなくなったときに実行すれば右クリックメニューから消えてくれます。

[2020-10-14]  
動画編集ソフトのプロジェクトファイルを想定していますが、制限撤廃によりどんな種類のファイルにでも使用できるようになりました。  
本ツールで出力されたテキストファイルやCSVファイルを読み込んでも正常に検出できました(何の意味もないけど)

[2020-12-05]  
フォルダ指定抽出機能が追加されました。フォルダの右クリックメニューから「ニコニコ素材の一覧を生成する」ことができます。  
※高速化および誤検知防止のため画像や動画、音声ファイルといった主要なバイナリファイルは読み込まないように拡張子でフィルタしていますが、ひとまずなハードコーディングなので読み込んでしまうかもしれません。  
問題が報告されるようであれば、この読み込み除外拡張子をユーザ側で設定できるようにします。

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
