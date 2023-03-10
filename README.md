# odin-docset
Odin docset generation for the odin pkgs to be used in Zeal / Dash / Velocity

## Steps to generate the docset

First download the most recent docs for the packages
```sh
bash download_pkgs_docs.sh
```

After the download ends generate the docset database
```sh
python3 generate_odin_docset.py
```

With all that done now you just need to copy the Odin.docset folder to your Zeal / Dash / Velocity docsets folder.
