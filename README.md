# kindle-book-list

`Kindle for mac` の `KindleSyncMetadataCache.xml` を再利用しやすいフォーマットに変換するツール

## Usage

1. `Kindle for mac` を起動して所有書籍一覧を更新する

   > mac 版の書籍情報 `~/Library/Application Support/Kindle/Cache/KindleSyncMetadataCache.xml`

2. 実行する

   標準入力から読み込み、標準出力に csv で出力

   ```shell
   cat ~/Library/Application\ Support/Kindle/Cache/KindleSyncMetadataCache.xml \
      | docker run --rm -i kurumi/kindle-book-list:latest
   ```

   ファイルを指定して読み込み、カレントに out.xlsx で出力

   ```shell
   cp ~/Library/Application\ Support/Kindle/Cache/KindleSyncMetadataCache.xml .

   docker run --rm -v ${PWD}:/work \
      kurumi/kindle-book-list:latest \
      --in-file /work/KindleSyncMetadataCache.xml \
      --out-file /work/out.xlsx
   ```

   オプション一覧

   | option       | default        | description                                   |
   | ------------ | -------------- | --------------------------------------------- |
   | `--in-file`  | `stdin`        | `Kindle for mac` の xml ファイル              |
   | `--out-file` | `stdout (csv)` | 保存ファイル名を指定する (.csv, .xlsx, .json) |
