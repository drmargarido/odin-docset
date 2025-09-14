#!/bin/bash
if [ ! -d ./Odin.docset/Contents/Resources/Documents ]; then
    mkdir -p Odin.docset/Contents/Resources/Documents
    httrack -w https://pkg.odin-lang.org/ -q -n -%P -p7 -N0 -s2 -D -a -K0 -c7 -%k -r3 -A100000 -F "Mozilla/4.5 (compatible; HTTrack 3.0x; Windows 98)" -%F "\<\!\-\- Mirrored from %s%s by HTTrack Website Copier/3.x [XR&CO'2014], %s -->" +\*.png +\*.gif +\*.jpg +\*.jpeg +\*.css +\*.js -ad.doubleclick.net/\* -twitch.tv/\* -github.com/\* -discord.com/\* -%s -%u -i -C2 -O "./Odin.docset/Contents/Resources/Documents"
    python -m venv .venv;
    if [ "$SHELL" == "/usr/bin/bash" ] || [ "$SHELL" == "/usr/bin/zsh" ] || [ "$SHELL" == "/bin/bash" ] || [ "$SHELL" == "/bin/zsh" ]; then
        source .venv/bin/activate
    elif [ "$SHELL" == "/usr/bin/fish" ] || [ "$SHELL" == "/bin/fish" ]; then
        source .venv/bin/activate.fish
    fi
    python ./generate_odin_docset.py
else
    httrack --update
    python ./generate_odin_docset.py
fi
# cp -R pkg.odin-lang.org/* Odin.docset/Contents/Resources/Documents/
