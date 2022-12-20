import sys
import xml.etree.ElementTree as et
from datetime import datetime
from io import StringIO

import jaconv  # type: ignore
import pandas as pd
from pandas import DataFrame

from .book import Book


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


def file_to_dataframe(file_path: str) -> DataFrame:

    if file_path == "<stdin>":
        file = StringIO(sys.stdin.read())
    else:
        file = file_path

    tree = et.parse(file)
    root = tree.getroot()

    books: list[Book] = []

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

        # 商品ページ
        url = f"https://amazon.jp/dp/{asin}"

        books.append(
            Book(
                asin=asin,
                title=title,
                title_yomi=title_yomi,
                authors=authors,
                publishers=publishers,
                publication_date=publication_date,
                purchase_date=purchase_date,
                url=url,
            )
        )

    return pd.DataFrame(books)
