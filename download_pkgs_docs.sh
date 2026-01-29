#!/bin/bash

mkdir -p Odin.docset/Contents/Resources/Documents
wget                                                          \
  --mirror                                                    \
  --page-requisites                                           \
  --adjust-extension                                          \
  --convert-links                                             \
  --no-host-directories                                       \
  --directory-prefix=Odin.docset/Contents/Resources/Documents \
  "https://pkg.odin-lang.org"                                 \
  "https://odin-lang.org/scss/custom.min.css"                 \
  "https://odin-lang.org/css/style.css"                       \
  "https://odin-lang.org/logo.svg"
