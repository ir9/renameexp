# renameexp / CG集を買ったらファイル名の連番の桁数が可変長でビュアーが順番に開いてくれない問題を解決するヤツ

1. エロCG集を買い、Downloadし解凍します
2. ワクワクしながら1枚目のjpegを開きます
3. ビュアーで次の画像を開きます（大体"→"キー）
4. **いきなりクライマックスじゃねーーーーか** [**クソァァァァァァァァァァｌ！！！！！！！！！！！！！！！！！！！！！**](https://www.youtube.com/results?search_query=%E3%82%AD%E3%83%BC%E3%83%9C%E3%83%BC%E3%83%89%E3%82%AF%E3%83%A9%E3%83%83%E3%82%B7%E3%83%A3%E3%83%BC)

という悲しい悲しい事故が発生するのは、大体以下のようなファイル名付けになっています：

```
ero-cg-1.jpg
ero-cg-2.jpg
ero-cg-3.jpg
 :
ero-cg-9.jpg
ero-cg-10.jpg
```

`ero-cg-1.jpg` 開いた次に `ero-cg-10.jpg` 開いちゃうって話ですね。 最後ですね。 クライマックスですねぴえん

そんな問題を解決するべく、良い感じにファイル名をリネームしてくれるのが、このスクリプト **「CG集を買ったらファイル名の連番の桁数が可変長でビュアーが順番に開いてくれない問題を解決するヤツ」** です。

わい「過去・現在・未来、すべての宇宙から、2枚目でクライマックスをおっぱじめて、いっぱいいっぱい悲しい思いをする人を無くしたい！！

『キミは少女じゃないからダメ

「えー。 魔法少女えぇやん。 なりたいやん。

『ダメ

「えー

## usage / 使い方

前提：Python3 を使えるようにしてください

```bash
python renameexp.py [-mpb] path_or_filelist
```

```
// example
python renameexp.py /path/to/your/feti-images/dir/
```

基本的にはディレクトリを食わせるだけです。 ディレクトリの代わりに、画像ファイルの一覧が記載されたテキストファイルを食わせることが出来ます。

### `-m`, `--move`

ファイルをリネームします。 `path_or_filelist` にパスを指定した場合、デフォルトで有効になります

### `-p`, `--print`

 (オリジナルファイル名, 修正後のファイル名) のペアを出力します。 ファイルに移動は行いません。 `path_or_filelist` に、ファイル名の一覧のファイルを指定した場合、デフォルトで有効になります。

### `-b`, `--backup`

`_backup` ディレクトリを作成しバックアップを取ります


## Author / つくったひと

* いろきゅう
* http://ir9.jp
* twitter:@ir9

なんだかんだ自分で使ってます :-)
