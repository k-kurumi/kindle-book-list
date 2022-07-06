# kindle-book-list

`Kindle for mac` の `KindleSyncMetadataCache.xml` を再利用しやすいフォーマットに変換するツール

## Usage

1. `Kindle for mac` を起動して所有書籍一覧を更新する

2. `KindleSyncMetadataCache.xml` をカレントにコピーする

   > `~/Library/Application Support/Kindle/Cache/KindleSyncMetadataCache.xml` (Kindle for mac の場合)

3. 実行する

   ```shell
   ##
   ## Options:
   ##   -i, --input FILENAME     KindleSyncMetadataCache.xml path  [required]
   ##   -o, --output FILENAME    converted file path [default: STDOUT]
   ##   -f, --format [csv|json]  output format  [default: csv]
   ##   --help                   Show this message and exit.
   ##

   docker run --rm -v $PWD:/app kurumi/kindle-book-list:latest -i <カレントのKindleSyncMetadataCache.xmlへのパス> -f json

   ##
   ## ex: csv を data/output.csv に出力
   ## docker run --rm -v $PWD:/app kurumi/kindle-book-list:latest -i data/KindleSyncMetadataCache.xml -o data/output.csv
   ##
   ```
