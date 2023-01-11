import std/xmlparser
import std/xmltree

# join
import std/strutils

# collect
import std/sugar

#[
    参考情報
    [【Nim】XMLをDOMで読み込む - Flat Leon Works](https://flat-leon.hatenablog.com/entry/nim_xml_dom_parser)
    [PythonistaのためのNim入門](https://zenn.dev/dumblepy/articles/3f4f1c288ada66)

]#

let node: XmlNode = xmlparser.parseXml(stdin.readAll)

# csv header
echo [
    "asin",
    "title",
    "title_yomi",
    "authors",
    "authors_yomi",
    "publishers",
    "publication_date",
    "purchase_date",
    "amazon_url",
].join(",")

for m in node.findAll("meta_data"):
    let
        asin = m.child("ASIN").innerText
        title = m.child("title").innerText
        title_yomi = m.child("title").attr("pronunciation")
        authors = collect(newSeq):
            for a in m.findAll("author"): a.innerText
        authors_yomi = collect(newSeq):
            for a in m.findAll("author"): a.attr("pronunciation")
        publishers = collect(newSeq):
            for p in m.findAll("publisher"): p.innerText
        publication_date = m.child("publication_date").innerText
        purchase_date = m.child("purchase_date").innerText

        # csv body
        row = [
            asin,
            title,
            title_yomi,
            authors.join("/"),
            authors_yomi.join("/"),
            publishers.join("/"),
            publication_date,
            purchase_date,
            "https://amazon.jp/dp/" & asin,
        ].join(",")

    echo row
