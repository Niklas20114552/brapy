#!/usr/bin/bash
echo "Du willst brapy deinstallieren?"
echo "Hattest du ein Problem mit brapy?"
echo "Dann erstelle doch bitte ein Issue auf GitHub, damit wird es fixen."
echo
read -p "Drücke eine beliebige Taste zum fortfahren..." -rsn1
echo
if [[ $(pidof brapy | wc -w) != 0 ]]; then
    echo "Brapy läuft noch. Sei doch so lieb und schließe Brapy."
    exit
fi
sudo rm -rfv /usr/local/share/brapy
sudo rm -f /usr/local/bin/brapy
sudo rm -f /usr/local/bin/brapy-uninstaller
sudo rm -f /usr/share/applications/brapy.desktop
echo "Fertig. Aber es ist doch Schade..."