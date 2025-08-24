#!/bin/bash
wget -mpEk "https://pkg.odin-lang.org/"
mkdir -p Odin.docset/Contents/Resources/Documents
cp -R pkg.odin-lang.org/* Odin.docset/Contents/Resources/Documents/

wget https://odin-lang.org/scss/custom.min.css
wget https://odin-lang.org/css/style.css
wget https://odin-lang.org/lib/highlight/styles/github-dark.min.css

cat custom.min.css style.css github-dark.min.css >> Odin.docset/Contents/Resources/Documents/style.css

wget https://odin-lang.org/logo.svg
mv logo.svg Odin.docset/Contents/Resources/Documents/logo.svg
sed 's;https://odin-lang.org/logo.svg;/odin/logo.svg;g' -i $(find Odin.docset/Contents/Resources/Documents -name "*.html")
