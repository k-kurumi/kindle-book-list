# kindle-book-list

`Kindle for mac` の `KindleSyncMetadataCache.xml` を再利用しやすいフォーマットに変換するツール

## Usage

1. `Kindle for mac` を起動して所有書籍一覧を更新する

2. `KindleSyncMetadataCache.xml` をカレントにコピーする

   > `~/Library/Application Support/Kindle/Cache/KindleSyncMetadataCache.xml`

3. 実行する

   オプション一覧

   | option       | default        | description                                   |
   | ------------ | -------------- | --------------------------------------------- |
   | `--in-file`  | `stdin`        | `Kindle for mac` の xml ファイル              |
   | `--out-file` | `stdout (csv)` | 保存ファイル名を指定する (.csv, .xlsx, .json) |

   標準入力から読み込み、標準出力に csv で出力

   ```shell
   cat ./KindleSyncMetadataCache.xml | docker run --rm -i kurumi/kindle-book-list:latest
   ```

   ファイルを指定して読み込み、カレントに out.xlsx で出力

   ```shell
   docker run --rm -v ${PWD}:/app \
      kurumi/kindle-book-list:latest \
      --in-file KindleSyncMetadataCache.xml \
      --out-file out.xlsx
   ```

## 開発環境のセットアップ

1. [Devbox](https://www.jetpack.io/devbox/docs/installing_devbox/) をインストールする
2. シェル起動とライブラリインストール

   ```shell
   devbox shell
   poetry shell
   poetry install
   ```
