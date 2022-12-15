# kindle-book-list

`Kindle for mac` の `KindleSyncMetadataCache.xml` を再利用しやすいフォーマットに変換するツール

## Usage

1. `Kindle for mac` を起動して所有書籍一覧を更新する

2. `KindleSyncMetadataCache.xml` をカレントにコピーする

   > `~/Library/Application Support/Kindle/Cache/KindleSyncMetadataCache.xml`

3. 実行する

   ```shell
   ╭─ Options ────────────────────────────────────────────────╮
   │ --in-file         TEXT  [default: <stdin>]               │
   │ --out-file        TEXT  [default: <stdout>]              │
   │ --help                  Show this message and exit.      │
   ╰──────────────────────────────────────────────────────────╯

   cat ./data/KindleSyncMetadataCache.xml | docker run --rm -i kurumi/kindle-book-list:latest
   ```
