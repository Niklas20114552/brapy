#!/usr/bin/bash
echo -e "Das ist BETA Software.\nJa.\nMehr kommt jetzt auch nicht...\nIch wollts halt nur mal erwähnt haben.\n\nNun kommt aber das Wichtige:\n- Python muss installiert sein.\n- Pip sollte installiert sein.\n- WGET muss installiert sein.\n- Nur Linux wird unterstützt.\n- Sudo rechte werden für die Installation benötigt.\n"
if [[ $1 == "--apt" ]]; then
    touch /usr/local/share/brapy/apt.type
    echo "Es wird APT-GET zum Installieren verwendet."
    if [[ $2 != "--unattended" ]]; then
        read -p "Drücke eine beliebige Taste zum fortfahren..." -rsn1
    fi
    echo "Und los gehts.."
    sudo apt-get install python3-pyqt5 python3-pyqt5.qtwebengine python3-requests python3-pyqt5.sip -y
elif [[ $1 == "--pacman" ]]; then
    touch /usr/local/share/brapy/pacman.type
    echo "Es wird PACMAN zum Installieren verwendet."
    if [[ $2 != "--unattended" ]]; then
        read -p "Drücke eine beliebige Taste zum fortfahren..." -rsn1
    fi
    echo "Und los gehts.."
    sudo pacman -S --needed --noconfirm python-pyqt5 python-pyqt5-sip python-pyqt5-webengine python-requests
elif [[ $1 == "--pip" ]]; then
    touch /usr/local/share/brapy/pip.type
    echo "Es wird PIP3 zum Installieren verwendet."
    if [[ $2 != "--unattended" ]]; then
        read -p "Drücke eine beliebige Taste zum fortfahren..." -rsn1
    fi
    echo "Und los gehts.."
    sudo pip3 install pyqt5 requests pyqtwebengine pyqt5-sip
elif [[ $1 == "--dnf" ]]; then
    touch /usr/local/share/brapy/dnf.type
    echo "Es wird DNF zum Installieren verwendet."
    if [[ $2 != "--unattended" ]]; then
        read -p "Drücke eine beliebige Taste zum fortfahren..." -rsn1
    fi
    echo "Und los gehts.."
    sudo dnf install PyQt5 python3-pyqt5-sip python3-requests python3-qt5-webengine -y
else
    echo "Bitte gebe deine Installationsart an:"
    echo " --pip     Verwende Pip zum installieren      [Keine Limitierung]"
    echo " --apt     Verwende Apt-get zum installieren  [Nur für Debian   ]"
    echo " --pacman  Verwende Pacman zum installieren   [Nur für Archlinux]"
    echo " --dnf     Verwende Dnf zum installieren      [Nur für Red Hat  ]"
    exit
fi
sudo mkdir -pv /usr/local/share/brapy
sudo cp -v brapy_logo.png /usr/local/share/brapy/
sudo cp -v error.html /usr/local/share/brapy/
sudo cp -v errorfile.html /usr/local/share/brapy/
sudo cp -v home.html /usr/local/share/brapy/
sudo cp -v homeupdate.html /usr/local/share/brapy/
sudo cp -v upgrade.html /usr/local/share/brapy/
sudo cp -v upgrade.sh /usr/local/share/brapy/upgrade
sudo cp -v main.py /usr/local/bin/brapy
sudo cp -v brapy.desktop /usr/share/applications/
if ! fc-list | grep -i "Material Icons Outlined">/dev/null; then
    if which wget >/dev/null; then
        sudo wget --output-document=/usr/share/fonts/MaterialIconsOutlined-Regular.otf https://github.com/google/material-design-icons/raw/master/font/MaterialIconsOutlined-Regular.otf
    else
        echo "Bitte installiere WGET und führe das Setup dann erneut aus"
        exit
    fi
fi
if ! fc-list | grep -i "Material Icons">/dev/null; then
    if which wget >/dev/null; then
        sudo wget --output-document=/usr/share/fonts/MaterialIcons-Regular.ttf https://github.com/google/material-design-icons/raw/master/font/MaterialIcons-Regular.ttf
    else
        echo "Bitte installiere WGET und führe das Setup dann erneut aus"
        exit
    fi
fi
echo "Das sollte nun funktioniert haben..."
exit
