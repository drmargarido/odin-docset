#!/usr/local/bin/python

import os, re, sqlite3
from bs4 import BeautifulSoup, NavigableString, Tag

entity_to_type = {
    "pkg-Types": "Type",
    "pkg-Constants": "Constant",
    "pkg-Variables": "Variable",
    "pkg-Procedures": "Procedure",
    "pkg-Procedure Groups": "Procedure",
}

conn = sqlite3.connect("Odin.docset/Contents/Resources/docSet.dsidx")
cur = conn.cursor()

try:
    cur.execute("DROP TABLE searchIndex;")
except:
    pass

cur.execute("CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);")
cur.execute("CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);")

docpath = "Odin.docset/Contents/Resources/Documents"

def parse_packages(top_level_soup):
    for pkg in top_level_soup.find_all("td", {"class": "pkg-name"}):
        name = pkg.text.strip()
        if not pkg.a:
            continue

        pkg_href = pkg.a.attrs["href"]
        if len(name) > 1:
            cur.execute("INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)", (name, "Package", pkg_href))
            print("package: %s, path: %s" % (name, pkg_href))

            pkg_page = open(os.path.join(docpath, pkg_href)).read()
            pkg_soup = BeautifulSoup(pkg_page, features="lxml")

            current_type = ""
            for node in pkg_soup.find("article", {"class": "documentation"}):
                if node.name == "h2":
                    entity_type = node.attrs.get("id", "")
                    current_type = entity_to_type.get(entity_type, "")

                if node.name == "section":
                    if current_type == "":
                        continue

                    for entity in node.find_all("h3"):
                        entity_name = entity.attrs["id"]
                        entity_href = "{0}#{1}".format(pkg_href, entity_name)
                        prefixed_entity_name = "{0}.{1}".format(name, entity_name)
                        cur.execute("INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)", (prefixed_entity_name, current_type, entity_href))

page = open(os.path.join(docpath,"core.html")).read()
soup = BeautifulSoup(page, features="lxml")
parse_packages(soup)

page = open(os.path.join(docpath,"vendor.html")).read()
soup = BeautifulSoup(page, features="lxml")
parse_packages(soup)

conn.commit()
conn.close()
