#!/usr/bin/bash
echo -e "Das ist BETA Software.\nJa.\nMehr kommt jetzt auch nicht...\nIch wollts halt nur mal erwähnt haben.\n\nNun kommt aber das Wichtige:\n- Python muss installiert sein.\n- Pip sollte installiert sein.\n- Nur Linux wird unterstützt.\n- Sudo rechte werden für die Installation benötigt.\n"
if [[ $1 == "--apt" ]]; then
    echo "Es wird APT-GET zum Installieren verwendet."
    read -p "Press any key to continue" -rsn1
    echo "Und los gehts.."
    sudo apt-get install python-pyqt5 python3-pyqt5.qtwebengine python3-requests python3-pyqt5-sip
elif [[ $1 == "--pacman" ]]; then
    echo "Es wird PACMAN zum Installieren verwendet."
    read -p "Press any key to continue" -rsn1
    echo "Und los gehts.."
    sudo pacman -S --needed python-pyqt5 python-pyqt5-sip python-pyqt5-webengine python-requests
elif [[ $1 == "--pip" ]]; then
    echo "Es wird PIP3 zum Installieren verwendet."
    read -p "Press any key to continue" -rsn1
    echo "Und los gehts.."
    sudo pip3 install pyqt5 requests pyqtwebengine pyqt5-sip
else
    echo "Bitte gebe deine Installationsart an:"
    echo " --pip     Verwende Pip zum installieren      [Keine Limitierung]"
    echo " --apt     Verwende Apt-get zum installieren  [Nur für Debian   ]"
    echo " --pacman  Verwende Pacman zum installieren.  [Nur für Archlinux]"
    exit
fi
sudo mkdir -pv /usr/local/share/brapy
sudo cp -v brapy_logo.png /usr/local/share/brapy/
sudo cp -v volume_off.png /usr/local/share/brapy/
sudo cp -v error.html /usr/local/share/brapy/
sudo cp -v errorfile.html /usr/local/share/brapy/
sudo cp -v home.html /usr/local/share/brapy/
sudo cp -v main.py /usr/local/bin/brapy
sudo cp -v brapy.desktop /usr/share/applications/
echo "Das sollte nun funktioniert haben..."
exit
