# odin-docset
Odin docset generation for the odin pkgs to be used in Zeal / Dash / Velocity

## Setup

1. Download last version from [releases](https://github.com/drmargarido/odin-docset/releases) and
2. Copy the Odin.docset folder to your Zeal / Dash / Velocity docsets folder.
3. All done, it's ready to use!

## Steps to generate the manually

First download the most recent docs for the packages
```sh
bash download_pkgs_docs.sh
```

After the download ends generate the docset database
```sh
python3 generate_odin_docset.py
```

With all that done now you just need to copy the Odin.docset folder to your Zeal / Dash / Velocity docsets folder.
