#!/usr/bin/env bash

# define the youplay folder
BRAPY_BASE_DIR=$(dirname "$PWD")

STR1=" ist ein auf Qt5 (PyQt5) basierender in Python geschriebender Webbrowser."
STR2=" ist ein auf Qt5 (PyQt5) basierender in Python geschriebender Webbrowser. (AUR-Version)"

TMPDIR=$(mktemp -d -p .)
cp PKGBUILD "$TMPDIR"/

cd "$TMPDIR"

# build AUR zst-file from out PKGBUILD-file
makepkg -si PKGBUILD

mkdir -pv "$BRAPY_BASE_DIR/dist"
mv *.zst "$BRAPY_BASE_DIR"/dist/

# re-modify program string :-)
sudo sed -i -e "s/$STR2/$STR1/g" /usr/bin/brapy
sudo sed -i -e "s/APP_MANUAL_INSTALLED: bool = True/APP_MANUAL_INSTALLED: bool = False/g" /usr/bin/brapy

# cleanup
cd .. && rm -rf "$TMPDIR"

echo "Done."
exit
