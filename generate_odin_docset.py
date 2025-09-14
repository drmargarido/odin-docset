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

main_path = "Odin.docset/Contents/Resources/Documents/pkg.odin-lang.org"

def parse_packages(top_level_soup):
    current_directory = None
    for parent_pkg in top_level_soup.find_all("tr", {"class": "directory-pkg"}):
        pkg = parent_pkg.find("td", {"class": "pkg-name"})
        name = pkg.text.strip()
        if "directory-child" in parent_pkg["class"]:
            name = "{0}/{1}".format(current_directory, name)
        else:
            current_directory = name

        if not pkg.a:
            continue

        path_arr = docpath.split('/')
        search_path = path_arr[len(path_arr) - 1]
        pkg_href = pkg.a.attrs["href"]
        # pkg_href =
        print("[+] PKG Href: ", pkg_href)
        if len(name) >= 1:
            cur.execute("INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)", (name, "Package", "pkg.odin-lang.org/{0}/{1}".format(search_path, pkg_href)))
            print("package: %s, path: %s" % (name, os.path.join(docpath, pkg_href)))
            # print("docpath: ", search_path)
            # exit(1)
            pkg_page = open(os.path.join(docpath, pkg_href)).read()
            pkg_soup = BeautifulSoup(pkg_page, features="lxml")

            current_type = ""
            for node in pkg_soup.find("section", {"class": "documentation"}):
                if node.name == "h2":
                    entity_type = node.attrs.get("id", "")
                    current_type = entity_to_type.get(entity_type, "")

                if node.name == "div":
                    if current_type == "":
                        continue

                    for entity in node.find_all("h3"):
                        entity_name = entity.attrs["id"]
                        entity_href = "pkg.odin-lang.org/{0}/{1}#{2}".format(search_path,pkg_href, entity_name)
                        # pkg.odin-lang.org/core/{pkg_href}
                        print("[+] Entity Href: ", entity_href)
                        prefixed_entity_name = "{0}.{1}".format(name, entity_name)
                        print(f"[+] Entity href: {entity_href}")
                        # exit(1)
                        cur.execute("INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)", (prefixed_entity_name, current_type, entity_href))

docpath = main_path + "/core"
page = open(os.path.join(docpath,"index.html")).read()
soup = BeautifulSoup(page, features="lxml")
parse_packages(soup)

docpath = main_path + "/vendor"
page = open(os.path.join(docpath,"index.html")).read()
soup = BeautifulSoup(page, features="lxml")
parse_packages(soup)

docpath = main_path + "/base"
page = open(os.path.join(docpath,"index.html")).read()
soup = BeautifulSoup(page, features="lxml")
parse_packages(soup)


conn.commit()
conn.close()
