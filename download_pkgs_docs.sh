#!/bin/bash
wget -mpEk "https://pkg.odin-lang.org/"
mkdir -p Odin.docset/Contents/Resources/Documents
cp -R pkg.odin-lang.org/* Odin.docset/Contents/Resources/Documents/
