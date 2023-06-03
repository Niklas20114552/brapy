#!/usr/bin/bash
git clone https://github.com/Niklas20114552/brapy /tmp/brapy_upgrade
if [[ -f /usr/local/share/brapy/dnf.type ]]; then
    /tmp/brapy_upgrade/setup.sh --dnf --unattended
    brapy & disown
elif [[ -f /usr/local/share/brapy/apt.type ]]; then
    /tmp/brapy_upgrade/setup.sh --apt --unattended
    brapy & disown
elif [[ -f /usr/local/share/brapy/pip.type ]]; then
    /tmp/brapy_upgrade/setup.sh --pip --unattended
    brapy & disown
elif [[ -f /usr/local/share/brapy/pacman.type ]]; then
    /tmp/brapy_upgrade/setup.sh --pacman --unattended
    brapy & disown
fi