# Brapy

Brapy ist ein auf Qt5 (PyQt5) in Python geschriebener Webbrowser.

Brapy ist noch lange nicht ausgereift. Also bitte ich hier (wie immer), dass Fehler im Issue-Tab von Github gemeldet werden.

## Installation

Klone das Git-Repository mit:

```git clone https://github.com/Niklas20114552/brapy```

Navigiere in das Verzeichnis:

```cd brapy```

Nun musst du das Setup im Terminal ausführen:

Für Arch Linux (und alles was darauf basiert): ```./setup.sh --pacman```

Für Debian (und Ubuntu und alles was darauf basiert): ```./setup.sh --apt```

Für Red Hat (und alles was darauf basiert, wie Fedora): ```./setup.sh --dnf```

Für alles andere: ```./setup.sh --pip```

## Was noch nicht funktioniert

### Rechtsklickmenü

Es wird noch das Standard Rechtsklickmenü von PyQt5.QWebEngineView verwendet.

Daher funktionieren Knöpfe wie "Open link in new tab" oder "Save page" noch nicht, da diese Funktionen noch nicht implementiert sind.

### Vollbild

Man kann schon mit F11 in den Vollbildmodus wechseln, aber auf Webseiten die einen Eigenen Knopf dafür haben (wie z.B. YouTube) funktioniert dies noch nicht.

### Drucken

Einfach noch überhaupt nicht implementiert. Kommt aber noch.

### Webseiten mit Zertifikatsfehler aufrufen

Dies ist ein Bug.

### Berechtigungen

Einfach noch überhaupt nicht implementiert. Kommt aber noch.
