# kindle-book-list

`Kindle for mac` の `KindleSyncMetadataCache.xml` を再利用しやすいフォーマットに変換するツール

## Usage

1. `Kindle for mac` を起動して所有書籍一覧を更新する

2. `KindleSyncMetadataCache.xml` をカレントにコピーする

   > `~/Library/Application Support/Kindle/Cache/KindleSyncMetadataCache.xml` (Kindle for mac の場合)

3. 実行する

   ```shell
   docker run --rm -v $PWD:/app kurumi/kindle-book-list:latest -i <カレントのKindleSyncMetadataCache.xmlへのパス> -o <出力ファイルパス>

   ## ex:
   ## docker run --rm -v $PWD:/app kurumi/kindle-book-list:latest -i data/KindleSyncMetadataCache.xml -o data/output.csv
   ```
