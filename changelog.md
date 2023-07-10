# Changelog

## 0.05-beta1 : 10.07.2023 - Added Archlinux PKGBUILD 

By: [@Niklas20114552](https://github.com/Niklas20114552)

Added:

- PKGBUILD for Archlinux
- Confirm Dialog for Updater when manually installed
- Error Dialog for Updater when installed via package manager
- Custom Contextmenu

Fixed:

- Move ```sudo rm -f /usr/local/bin/brapy-uninstaller``` to the end of uninstall.sh. Fixed that the Uninstaller closes mid in uninstallation.

## 0.04.1 : 15.06.2023 - Added uninstaller and bug fixes

By: [@Niklas20114552](https://github.com/Niklas20114552)

Added:

- Uninstaller:
    - Github Repository: /uninstall.sh
    - Installed: /usr/local/bin/brapy-uninstaller

Fixed:

- Browser throws a Security Error when loading URL that contains a ```@``` (like https://youtube.com/@user) 
- Added missing equals-sign in extraerror.html. Fixes bug, that "no internet"-error is being displayed when url contains username.
- Moved Sudo commands behind the confirm-prompt in setup.sh

Changed:

- Desktop Entry Name is now "Brapy Web Browser" instead of "Brapy"

## 0.04 : 06.06.2023 - Added basic configuration files and more security

By: [@Niklas20114552](https://github.com/Niklas20114552)

Added:

- Configuration File: ~/.config/brapy/brapy.ini
- Security features: (For this Error Messages was the file extraerror.html added)
    - Do not allow to navigate to URLs that contains a username (Can be disabled in config)
- Added Error Message for no Internet Connection

Fixed:

- Wrong Errormessage is being displayed, when a website is navigation to a url that does not exists.

## 0.03.2 : 04.06.2023 - Inline Variable and Shortcuts

By: [@Niklas20114552](https://github.com/Niklas20114552)

Changed:

- Variables:
    - Inline every shortcut_ Variable
- Shortcuts:
    - Corrected wrong Action-Labels

Added:

- Shortcuts:
    - Alt + Home (aka. Pos1) : Go to Homepage

## 0.03.1 : 04.06.2023 - Fixed Upgrader

By: [@Niklas20114552](https://github.com/Niklas20114552)

Fixed:

- Upgrader:
    - Upgrader could not copy files.
    - Upgrader failed to start brapy again.
    - Improve syntax.

Changed:

- Setup:
    - Separated Font installation.
    - Added sudo to touch.

- main.py:
    - Copy upgrade.sh first to /tmp befor run it. (Bash does not like it when the running skript is changed.)

Added:

- Upgrade.html:
    - Added button to see changelog.

## 0.03 : 03.06.2023 - Added Upgrader

By: [@Niklas20114552](https://github.com/Niklas20114552)

Added:

- Upgrader
- Unattended Mode for setup.sh
- Missing Semicolons in error.html and errorfile.html

Changed:

- main.py : Every direct link to home.html is replaced by variable self.homeurl

## 0.02 : 03.06.2023 - Improved Shortcuts and Address bar focus

By: [@Niklas20114552](https://github.com/Niklas20114552)

Added: 

- Shortcuts: ([#6](https://github.com/Niklas20114552/brapy/issues/6))
    - Alt + Left Arrow : Go back in navigation history.
    - Alt + Right Arrow : Go forward in navigation history.
    - F5 / CTRL + R : Reload Page
- Address bar is now focused when opening a new tab ([#4](https://github.com/Niklas20114552/brapy/pull/4))

Changed:

- brapy --version now says "brapy 0.02" instead of "0.02"


## 0.01 : 03.06.2023 - Added RedHat/DNF Setup Support

By: [@Niklas20114552](https://github.com/Niklas20114552)

Added:

- Support for DNF in setup.sh : --dnf ([#5](https://github.com/Niklas20114552/brapy/issues/5))

## 0.01 : 31.05.2023 - Introducing versioning

By: [@ProfP30](https://github.com/ProfP30)

Added:

- Versioning
- Command Line Arguments:
    - --version / -v : Get Version of brapy
    - --help / -h : Show Help

## 31.05.2023 - Address bar focus

By: [@ProfP30](https://github.com/ProfP30)

Added:

- Shortcut (Ctrl + L): Focus Address bar


## 29.05.2023 - Initial Release

By: [@Niklas20114552](https://github.com/Niklas20114552)

Added:

- Base Files: main.py brapy_logo.png error.html errorfile.html home.html brapy.desktop
- Installation: setup.sh(Debian, Pip3 and Archlinux support)
