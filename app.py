import csv
import json
import sys
from dataclasses import dataclass
from datetime import datetime
from typing import TextIO
from xml.etree import ElementTree

import click
import jaconv


@dataclass(frozen=True)
class Book:
    asin: str
    title: str
    title_yomi: str
    authors: list[str]
    publishers: list[str]
    publication_date: str
    purchase_date: str

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
            return {
                "asin": b.asin,
                "title": b.title,
                "authors": b.authors,
                "publishers": b.publishers,
                "publication_date": b.publication_date,
                "purchase_date": b.purchase_date,
            }
        else:
            type_name = b.__class__.__name__
            raise TypeError(f"Unexpected type {type_name}")


def export_csv(books: list[Book], output: TextIO) -> None:
    """CSV出力
    生成ファイルがUTF-8なので、直接Excelで開くと文字化けする
    """

    writer = csv.DictWriter(output, fieldnames=Book.csv_fieldnames(), dialect="excel")

    writer.writeheader()

    for b in books:
        writer.writerow(b.to_dict)


def export_json(books: list[Book], output: TextIO) -> None:
    """JSON出力"""
    json.dump(books, output, ensure_ascii=False, indent=4, default=Book.json_body)


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
    "input_",
    type=click.File("r"),
    help="KindleSyncMetadataCache.xml path",
    required=True,
)
@click.option(
    "-o",
    "--output",
    type=click.File("w"),
    default=sys.stdout,
    help="converted file path [default: STDOUT]",
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
def main(input_: TextIO, output: TextIO, format_: str) -> None:
    tree = ElementTree.parse(input_)
    root = tree.getroot()

    books = []
    for book in root.iter("meta_data"):
        asin = book.find("ASIN").text
        title = book.find("title").text

        # ASINだけのエントリーがいくつかあるので無視する
        if "---" in title:
            continue

        # よみはひらがなの方が分かりやすい
        # よみが空文字の書籍がある
        title_yomi = jaconv.kata2hira(book.find("title").attrib.get("pronunciation", ""))

        # authors,publishersは空だったり複数登録されている場合がある
        authors = [a.text for a in book.find("authors")]
        publishers = [p.text for p in book.find("publishers")]

        # 出版日(出版日が空文字の書籍がある)
        publication_date = datetime_to_date(book.find("publication_date").text)

        # 購入日
        purchase_date = datetime_to_date(book.find("purchase_date").text)

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
            export_csv(books, output)
        case "json":
            export_json(books, output)
        case _:
            export_csv(books, output)

    if input_:
        input_.close()

    if output:
        output.close()


if __name__ == "__main__":
    main()
