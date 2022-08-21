
# ニコニコ素材リストアップツール v0.8.3rc2
(2022-08-22)

## 概要

動画編集ソフトのプロジェクトファイル等からニコニコの素材のIDを抽出し、コンテンツツリーに登録しやすい10件ごとのリストにまとめるツールです。  
元々はAviUtlとRecotteStudio用でしたが、仕組み的にどのソフトでもいけそうだったので内部でやってた制限を取っ払いました。  
ニコニコのサイトから素材の名前と作者を取得し、CSVファイルにまとめる機能もあります。  
各種生成ファイルはプロジェクトファイルのあるフォルダに出力されるため、右クリックメニューに登録して使うこともできます。

## 導入

zipをダウンロードし解凍したら、中にある`regist.bat`を管理者権限で実行してください。  
右クリックメニューに登録されます。  
(逆に登録解除したい場合は管理者権限で`remove.bat`を実行してください)

※ Tablacus Explorer への導入方法は配布ページをご覧ください。(セルフ丸投げですみません)

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
+ nc0000_im0000_合成素材.jpg

※ v0.5からのアップデートでいろいろ試みてはいますが、ID周辺のバイナリによっては誤検知したり、検出漏れが発生する可能性があります。  
その場合は不具合のあったファイルor誤検知したIDの周辺のバイナリ情報(バイナリエディタのスクショ)をTwitterのDMなどに送ってくれれば対応します。

## クレジットテキスト生成

クレジットテキストを生成できます。クレジットテキストにはID、作品名、投稿者名、URLを含めることができます。  
この機能を利用するには設定ファイル`config.txt`に`credit-format`という項目を設定してください。設定例は以下のとおりです。

	credit-format = 【%id%】 %title% (%creator%)

`%id%`、`%title%`、`%creator%`、`%url%`のところがそれぞれID、作品名、投稿者名、URLに置き換わります。  
書かれていない/設定ファイルがない場合は生成されません。

※ 設定ファイルの文字エンコーディングは「cp932」または「sjis」でお願いします。
※ 1作品のクレジットが2行以上となるクレジットテキストは生成できません。
※ 作品種別ごとにまとめる機能はありません。

# HTML生成

使用作品を表にまとめたHTMLを生成できます。HTMLではサムネイル、作品ID、タイトル、投稿者名を確認できます。  
サムネイルをクリックすると作品ページに飛ぶことができます。投稿者名をクリックすると投稿者のマイページに飛ぶことができます。  
また、上部のボタンとチェックボックスを活用することで、選択した作品のみのIDリストをコピーすることができます。

この機能を利用するには、設定ファイル`config.txt`に`export-html`という項目を追加してください。設定例は以下のとおりです。

	export-html = True

Trueで有効、Falseで無効です。書かれていない/設定ファイルがない場合は無効扱いになります。

## 誤検知対策: 除外拡張子リスト

一部の拡張子は中身を読み込まないように設定されています。  
ツールと同じフォルダに`exclude_ext_list.txt`を作成し、その中に除外したい拡張子を書き込んでおくと、追加でその拡張子も除外します。

	lwi,  avi,  mp4,  flv,  mov, asf,  mkv,  webm, mpg,   m2ts,
	mpg,  mpeg, wav,  mp3,  ogg, wma,  m4a,  flac, aif,   aiff,
	aac,  mid,  midi, jpg,  jpe, jpeg, png,  gif,  bmp,   webp,
	psd,  apd,  ai,   mdp,  ico, zip,  lzh,  7z,   gz,    tar,
	rar,  exe,  dll,  msi,  sys, iso,  docx, dotx, xlsx,  xlsm,
	pptx, pptm, potx, potm, db,  pdf,  lnk,  url,  cache, user,
	auf,  auo,  aui,  bak,  pdb, sln

## 誤検知対策: 2段階抽出を利用する拡張子リスト

一部の拡張子ではファイルパスを抽出し、その中からIDを抽出する2段階抽出を利用します。  
ツールと同じフォルダに`2step_ext_list.txt`を作成し、その中に2段階抽出を利用したい拡張子を書き込んでおくと、追加でその拡張子も2段階抽出を利用します。

	aup, pmm, emm

## 更新確認

最短で1週間ごとにGitHubのAPIと通信し、新しいバージョンがないか確認します。最新バージョンが見つかればコンソールでお知らせします。  
この機能はconfig.txtで無効化できます。

	check-update = False

Trueで有効、Falseで無効です。書かれていない/設定ファイルがない場合は有効扱いになります。

## 注意

+ 本ツールはニコニコ各サービスのWebサイトへアクセスします。多重起動するなど、むやみに負荷をかける行為はしないでください。
+ ニコニ・コモンズ、静画、動画、立体に対応しています。それ以外の素材を前項の形式のファイル名で保存していたとしても抽出することはできません。
+ 既に削除されている素材の名前や作者を取得することはできません。
+ 「nc数字」「im数字」「sm数字」「td数字」を検出するため、このような文字列がテキストオブジェクト等に含まれると検出されてしまいます。仕様にしておくので活用したい場合は活用してください。

## ファイルの上書きについて

デフォルト設定では、ファイル名は固定で、同じフォルダで抽出を行うと確認なしに上書きされます。  
config.txtで既にファイルがあった場合の挙動を変更することができます。

	overwrite-mode = confirm

| 値        | 説明                                   |
| ---       | ---                                    |
| overwrite | デフォルト設定。確認なしで上書きする。 |
| confirm   | 同名のファイルがあれば確認する。       |
| datetime  | 常にファイル名に日時を付与する。       |
| number    | 同名のファイルがあれば連番を付与する。 |

## ビルド方法

pyinstallerで固めるだけです。アイコンは[iconmonstr](https://iconmonstr.com/file-27-svg/)さんのものを使用しています。  
リポジトリのルートディレクトリに移動して以下を実行してください。

	pyinstaller -F --clean --noupx listup_tool.py --icon iconmonstr-file-27-240.ico

## クレジット

制作者: イスターリャ(@is_ptcm)  
言語　: Python 3.8.2
