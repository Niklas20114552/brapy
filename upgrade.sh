#!/usr/bin/bash
rm -rf /tmp/brapy_upgrade
git clone https://github.com/Niklas20114552/brapy /tmp/brapy_upgrade
cd /tmp/brapy_upgrade
if [[ -f /usr/local/share/brapy/dnf.type ]]; then
    ./setup.sh --dnf --unattended
elif [[ -f /usr/local/share/brapy/apt.type ]]; then
    ./setup.sh --apt --unattended
elif [[ -f /usr/local/share/brapy/pip.type ]]; then
    ./setup.sh --pip --unattended
elif [[ -f /usr/local/share/brapy/pacman.type ]]; then
    ./setup.sh --pacman --unattended
fi
exit