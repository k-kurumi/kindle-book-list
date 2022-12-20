from dataclasses import dataclass, field


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
    url: str = ""
