import csv
import json
import sys
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass, field
from datetime import datetime

import click
import jaconv  # type: ignore


@dataclass(frozen=True)
class Book:
    # https://amazon.jp/dp/<asin> が商品ページ
    # 単行本が文庫本化されたため、単行本ページごと消されて
    # asinやtitle情報があってもページがない商品あり。
    asin: str = ""
    title: str = ""
    title_yomi: str = ""
    authors: list[str] = field(default_factory=list)
    publishers: list[str] = field(default_factory=list)
    publication_date: str = ""
    purchase_date: str = ""

    @property
    def csv_row(self) -> dict:
        return {
            "asin": self.asin,
            "title": self.title,
            "title_yomi": self.title_yomi,
            "authors": ", ".join(self.authors),
            "publishers": ", ".join(self.publishers),
            "publication_date": self.publication_date,
            "purchase_date": self.purchase_date,
        }

    @staticmethod
    def csv_fieldnames() -> list[str]:
        """csvのヘッダ部分"""
        return [
            "asin",
            "title",
            "title_yomi",
            "authors",
            "publishers",
            "publication_date",
            "purchase_date",
        ]

    @staticmethod
    def json_body(b) -> dict:
        """jsonシリアライズ用"""
        if isinstance(b, Book):
            return asdict(b)
        else:
            type_name = b.__class__.__name__
            raise TypeError(f"Unexpected type {type_name}")


def export_csv(books: list[Book], file_path: str | None) -> None:
    """CSV出力
    生成ファイルがUTF-8なので、直接Excelで開くと文字化けする
    """

    match file_path:
        case None:
            # -oオプション指定なしのとき
            writer = csv.DictWriter(sys.stdout, fieldnames=Book.csv_fieldnames(), dialect="excel")
            writer.writeheader()
            for b in books:
                writer.writerow(b.csv_row)
        case _:
            with open(file_path, "w") as fp:
                writer = csv.DictWriter(fp, fieldnames=Book.csv_fieldnames(), dialect="excel")
                writer.writeheader()
                for b in books:
                    writer.writerow(b.csv_row)


def export_json(books: list[Book], file_path: str | None) -> None:
    """JSON出力"""

    match file_path:
        case None:
            # -oオプション指定なしのとき
            json.dump(
                {"count": len(books), "books": books}, sys.stdout, ensure_ascii=False, indent=4, default=Book.json_body
            )
        case _:
            with open(file_path, "w") as fp:
                json.dump(
                    {"count": len(books), "books": books}, fp, ensure_ascii=False, indent=4, default=Book.json_body
                )


def datetime_to_date(dt: str) -> str:
    """datetimeに変換可能な文字から日付だけを返す
    datetime.fromisoformatはtimezoneの表記揺れに対応していないため書き換えて処理する
    https://qiita.com/kg1/items/c455cb643c9a12096ab1#python-37%E3%81%AEfromisoformat%E3%81%AE%E5%88%A9%E7%94%A8%E3%81%AF%E6%B3%A8%E6%84%8F
    """
    if dt is None or len(dt) == 0:
        # 出版日が入っていないものが結講ある
        return ""

    # 末尾 0000 を 00:00 に書き換え
    dt_ = f"{dt[:-2]}:{dt[-2:]}"
    t = datetime.fromisoformat(dt_)
    return t.strftime("%Y-%m-%d")


@click.command()
@click.option(
    "-i",
    "--input",
    "input_path",
    type=click.Path(exists=True, readable=True),
    help="KindleSyncMetadataCache.xml path",
    required=True,
)
@click.option(
    "-o",
    "--output",
    "output_path",
    type=click.Path(),
    default=None,
    help="converted file path",
)
@click.option(
    "-f",
    "--format",
    "format_",
    type=click.Choice(["csv", "json"]),
    default="csv",
    show_default=True,
    help="output format",
)
def main(input_path: str, output_path: str | None, format_: str) -> None:
    tree = ET.parse(input_path)
    root = tree.getroot()

    books = []
    for book in root.iter("meta_data"):
        asin: str = book.find("ASIN").text  # type: ignore
        title: str = book.find("title").text  # type: ignore

        # ASINだけのエントリーがいくつかあるので無視する
        if "---" in title:
            continue

        # よみはひらがなの方が分かりやすい
        # よみが空文字の書籍がある
        title_yomi: str = jaconv.kata2hira(book.find("title").attrib.get("pronunciation", ""))  # type: ignore

        # authors,publishersは空だったり複数登録されている場合がある
        authors: list[str] = [a.text for a in book.find("authors")]  # type: ignore
        publishers: list[str] = [p.text for p in book.find("publishers")]  # type: ignore

        # 出版日(出版日が空文字の書籍がある)
        publication_date = datetime_to_date(book.find("publication_date").text)  # type: ignore

        # 購入日
        purchase_date = datetime_to_date(book.find("purchase_date").text)  # type: ignore

        books.append(
            Book(
                asin=asin,
                title=title,
                title_yomi=title_yomi,
                authors=authors,
                publishers=publishers,
                publication_date=publication_date,
                purchase_date=purchase_date,
            )
        )

    # TODO 別フォーマットを追加する
    match format_:
        case "csv":
            export_csv(books, output_path)
        case "json":
            export_json(books, output_path)
        case _:
            export_csv(books, output_path)


if __name__ == "__main__":
    main()
