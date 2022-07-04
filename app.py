import csv
import os
import sys
from dataclasses import dataclass
from typing import Dict, List, TextIO
from xml.etree import ElementTree

import click
import jaconv


@dataclass(frozen=True)
class Book:
    asin: str
    title: str
    title_yomi: str
    authors: List[str]
    publishers: List[str]

    @property
    def row_dict(self) -> Dict:
        return {
            "asin": self.asin,
            "title": self.title,
            "title_yomi": self.title_yomi,
            "authors": ", ".join(self.authors),
            "publishers": ", ".join(self.publishers),
        }

    @staticmethod
    def csv_fieldnames() -> List[str]:
        """csvのヘッダ部分"""
        return ["asin", "title", "title_yomi", "authors", "publishers"]


def export_csv(books: List[Book], output: TextIO) -> None:
    """CSV出力
    生成ファイルがUTF-8なので、直接Excelで開くと文字化けする
    """

    writer = csv.DictWriter(output, fieldnames=Book.csv_fieldnames(), dialect="excel")

    writer.writeheader()

    for b in books:
        writer.writerow(b.row_dict)


@click.command()
@click.option(
    "-i", type=click.File("r"), help="KindleSyncMetadataCache.xml path", required=True
)
@click.option(
    "-o",
    type=click.File("w"),
    default=sys.stdout,
    help="converted file path [default:STDOUT]",
)
def main(i: TextIO, o: TextIO) -> None:
    xml_file = i
    output = o

    tree = ElementTree.parse(xml_file)
    root = tree.getroot()

    books = []
    for book in root.iter("meta_data"):
        asin = book.find("ASIN").text
        title = book.find("title").text

        # ASINだけのエントリーがいくつかあるので無視する
        if "---" in title:
            continue

        # よみはひらがなの方が分かりやすい
        title_yomi = jaconv.kata2hira(
            book.find("title").attrib.get("pronunciation", "")
        )

        # authors,publishersは空だったり複数登録されている場合がある
        authors = [a.text for a in book.find("authors")]
        publishers = [p.text for p in book.find("publishers")]

        books.append(
            Book(
                asin=asin,
                title=title,
                title_yomi=title_yomi,
                authors=authors,
                publishers=publishers,
            )
        )

    # TODO 別フォーマットを追加する
    match os.path.splitext(output.name):
        case [_, ".csv"]:
            export_csv(books, output)
        case ["<stdout>", ""]:
            # オプション指定なしのとき
            export_csv(books, output)
        case _:
            raise ValueError(f"Invalid output format: {output.name}")


if __name__ == "__main__":
    main()
