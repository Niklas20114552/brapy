#!/usr/bin/python3
import sys, requests, os, json, getopt, re, subprocess
from PyQt5.QtCore import Qt, QUrl, QDir, QStandardPaths, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QHBoxLayout, QVBoxLayout, QWidget, QMessageBox, QPushButton, QTabWidget, QTabBar, QMenu, QAction, QDialog, QLabel, QFileDialog, QProgressBar
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt5.QtGui import QKeySequence, QFont, QFocusEvent
from packaging import version
from shutil import copyfile
from urllib.parse import urlparse
from configparser import ConfigParser
config = ConfigParser()

APP_VERSION: str = "0.04.1"
APP_NAME: str = "Brapy"
APP_DESCR: str = APP_NAME + " ist ein auf Qt5 (PyQt5) in Python geschriebender Webbrowser."

class LineEdit(QLineEdit):
    def __init__(self):
        super().__init__()
        self.mousePressEvent = self.on_click

    def focusInEvent(self, event: QFocusEvent) -> None:
        self.selectAll()

        super().focusInEvent(event)

    def on_click(self, event) -> None:
        pass

class DownloadDialog(QDialog):
    def __init__(self, url, file_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Download")

        layout = QVBoxLayout(self)
        self.file_label = QLabel(f"Name: {file_name}")
        self.file_label.setFixedWidth(500)
        self.url_label = QLabel(f"URL: {url}")
        self.url_label.setFixedWidth(500)
        layout.addWidget(self.url_label)
        layout.addWidget(self.file_label)

        pathlayout = QHBoxLayout()
        self.path_lineedit = QLineEdit()
        pathlayout.addWidget(self.path_lineedit)
        self.browse_button = QPushButton("Auswählen...")
        self.browse_button.clicked.connect(self.browse_path)
        pathlayout.addWidget(self.browse_button)
        layout.addLayout(pathlayout)

        buttonlayout = QHBoxLayout()
        self.confirm_button = QPushButton("Downloaden")
        self.confirm_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("Abbrechen")
        self.cancel_button.clicked.connect(self.reject)
        buttonlayout.addWidget(self.cancel_button)
        buttonlayout.addWidget(self.confirm_button)
        layout.addLayout(buttonlayout)

    def browse_path(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Datei Speichern...", self.path_lineedit.text(), "Alle Dateien")
        if not file_path == "":
            self.path_lineedit.setText(file_path)

class WebBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.downloads = []

        config.read(os.path.expanduser('~/.config/brapy/brapy.ini'))
        if not os.path.exists(os.path.expanduser('~/.config/brapy/brapy.ini')):
            config.add_section('Security')
            config.set('Security', 'allow_usernames_in_url', 'False')
            with open(os.path.expanduser('~/.config/brapy/brapy.ini'), 'w') as f:
                config.write(f)
        if config.get('Security', 'allow_usernames_in_url') == "True":
            self.config_allowusernamesinurl = True
        else:
            self.config_allowusernamesinurl = False

        text = requests.get("https://raw.githubusercontent.com/Niklas20114552/brapy/main/main.py").text
        pattern = r'APP_VERSION: str = "(.+?)"'
        match = re.search(pattern, text)
        if match:
            self.lastversion = match.group(1)
        else:
            self.lastversion = APP_VERSION

        if self.is_version_greater(self.lastversion, APP_VERSION):
            self.homeurl = f"file:///usr/local/share/brapy/homeupdate.html?old={APP_VERSION}&new={self.lastversion}"
            self.updateavailable = True
        else:
            self.homeurl = "file:///usr/local/share/brapy/home.html"
            self.updateavailable = False
        
        self.setWindowTitle(APP_NAME)
        layout = QVBoxLayout()

        # Tableiste erstellen
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)

        # Neuer-Tab-Knopf erstellen
        self.new_tab_button = QPushButton("")
        self.new_tab_button.setFont(QFont('Material Icons Outlined', 12))
        self.new_tab_button.setFixedSize(30, 30)  # Größe des Knopfs anpassen
        self.new_tab_button.clicked.connect(lambda: self.add_new_tab(self.homeurl, "Neuer Tab"))

        self.mute_tab_button = QPushButton("")
        self.mute_tab_button.setFont(QFont('Material Icons', 12))
        self.mute_tab_button.setFixedSize(30, 30)  # Größe des Knopfs anpassen
        self.mute_tab_button.clicked.connect(self.toggle_mute_tab)

        self.download_button = QPushButton("")
        self.download_button.setFont(QFont('Material Icons', 12))
        self.download_button.setFixedSize(30, 30)  # Größe des Knopfs anpassen
        self.download_button.clicked.connect(self.show_downloads)

        corner_layout = QHBoxLayout()
        corner_layout.addWidget(self.mute_tab_button)
        corner_layout.addWidget(self.new_tab_button)
        corner_layout.addWidget(self.download_button)
        corner_layout.addStretch()
        corner_widget = QWidget()
        corner_widget.setLayout(corner_layout)
        self.tab_widget.setCornerWidget(corner_widget)
        self.load_tabs()
        # Hauptwidget erstellen und dem Hauptfenster zuweisen
        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        new_tab_action = QAction("New Tab", self)
        new_tab_action.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_T))
        new_tab_action.triggered.connect(lambda: self.add_new_tab(self.homeurl, "Neuer Tab"))
        self.addAction(new_tab_action)

        close_action = QAction("Close " + APP_NAME, self)
        close_action.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_Q))
        close_action.triggered.connect(self.quit)
        self.addAction(close_action)

        fullscreen_action = QAction("Toggle Fullscreen", self)
        fullscreen_action.setShortcut(QKeySequence(Qt.Key_F11))
        fullscreen_action.triggered.connect(self.toggle_fullscreen)
        self.addAction(fullscreen_action)

        location_action = QAction("Location", self)
        location_action.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_L))
        location_action.triggered.connect(lambda: self.new_tab_address_bar.setFocus())
        self.addAction(location_action)

        self.tab_widget.currentChanged.connect(self.upmutebutton)
    def is_version_greater(self, version1, version2):
        parts1 = version1.split(".")
        parts2 = version2.split(".")
        max_parts = max(len(parts1), len(parts2))
        for i in range(max_parts):
            part1 = int(parts1[i]) if i < len(parts1) else 0
            part2 = int(parts2[i]) if i < len(parts2) else 0
            if part1 > part2:
                return True
            elif part1 < part2:
                return False
        return False
    def upgrade(self):
        self.save_tabs()
        print("Save complete!")
        with open(os.path.expanduser('~/.config/brapy/tabs.json'), 'r') as file:
            data = json.load(file)
        data.append({"url": "file:///usr/local/share/brapy/upgrade.html", "title": "Upgrade abgeschlossen"})
        with open(os.path.expanduser('~/.config/brapy/tabs.json'), 'w') as file:
            json.dump(data, file)
        copyfile("/usr/local/share/brapy/upgrade", "/tmp/brapy_upgrade.sh")
        subprocess.run("chmod +x /tmp/brapy_upgrade.sh", shell=True)
        process = subprocess.Popen("pkexec /tmp/brapy_upgrade.sh", shell=True)
        process.wait()
        new_brapy = subprocess.Popen("brapy", shell=True)
        sys.exit()

    def load_tabs(self):
        tabs_file_path = os.path.expanduser("~/.config/brapy/tabs.json")
        if os.path.exists(tabs_file_path):
            print("Save exists! Load Save!")
            with open(tabs_file_path, "r") as tabs_file:
                tabs_data = json.load(tabs_file)
                for tab_data in tabs_data:
                    url = tab_data["url"]
                    if url == "file:///usr/local/share/brapy/home.html" or url.startswith("file:///usr/local/share/brapy/homeupdate.html"):
                        url = self.homeurl
                    elif url == "file:///usr/local/share/brapy/upgrade.html":
                        url = url + "?ver=" + APP_VERSION
                    title = tab_data["title"]
                    self.add_new_tab(url, title)
            os.remove(tabs_file_path)
        else:
             self.add_new_tab(self.homeurl, "Neuer Tab")

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def save_tabs(self):
        tabs_data = []
        for i in range(self.tab_widget.count()):
            tab_widget = self.tab_widget.widget(i)
            web_view = tab_widget.findChild(QWebEngineView)
            url = web_view.url().toString()
            title = self.tab_widget.tabText(i)
            tabs_data.append({"url": url, "title": title})

        tabs_file_dir = os.path.expanduser("~/.config/brapy/")
        os.makedirs(tabs_file_dir, exist_ok=True)
        tabs_file_path = os.path.join(tabs_file_dir, "tabs.json")
        with open(tabs_file_path, "w") as tabs_file:
            json.dump(tabs_data, tabs_file)

    def upmutebutton(self):
        if not self.tab_widget.count() == 0:
            current_tab_index = self.tab_widget.currentIndex()
            if current_tab_index >= 0:
                tab_widget = self.tab_widget.widget(current_tab_index)
                web_view = tab_widget.findChild(QWebEngineView)

            # Überprüfen, ob der Tab bereits stumm geschaltet ist
            is_muted = web_view.page().isAudioMuted()
            title = web_view.page().title()
            self.setWindowTitle(title + " - " + APP_NAME)
            if is_muted:
                self.mute_tab_button.setText("")
                self.tab_widget.setTabText(current_tab_index, f" {title}")
            else:
                self.mute_tab_button.setText("")
                self.tab_widget.setTabText(current_tab_index, title)


    def toggle_mute_tab(self):
        current_tab_index = self.tab_widget.currentIndex()
        if current_tab_index >= 0:
            tab_widget = self.tab_widget.widget(current_tab_index)
            web_view = tab_widget.findChild(QWebEngineView)

        # Überprüfen, ob der Tab bereits stumm geschaltet ist
        is_muted = web_view.page().isAudioMuted()

        # Tab stummschalten oder Stummschaltung aufheben
        web_view.page().setAudioMuted(not is_muted)

    def closeEvent(self, event):
        self.save_tabs()
        print("Save complete!")
        super().closeEvent(event)

    def quit(self):
        self.save_tabs()
        print("Save complete!")
        sys.exit()

    def show_downloads(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Downloads")
        dialog.setFixedSize(400, 300)  # Feste Fenstergröße

        layout = QVBoxLayout(dialog)

        title_label = QLabel("Aktuelle Downloads:")
        layout.addWidget(title_label)

        self.download_layouts = {}  # Dictionary zum Speichern der Download-Layouts

        for download in self.downloads:
            download_layout = QHBoxLayout()

            name_label = QLabel(download.path().split("/")[-1])  # Zugriff auf den Dateinamen des Downloads
            download_layout.addWidget(name_label)

            progress_bar = QProgressBar()
            progress_bar.setFixedHeight(20)  # Feste Höhe für die Fortschrittsleiste
            download_layout.addWidget(progress_bar)

            cancel_button = QPushButton("Abbrechen")
            download_layout.addWidget(cancel_button)

            # Verknüpfung von Download-Objekt, Fortschrittsleiste und Abbrechen-Knopf
            self.download_layouts[download] = {
                'progress_bar': progress_bar,
                'cancel_button': cancel_button
            }

            # Verbindung des Abbrechen-Knopfs mit der entsprechenden Funktion
            cancel_button.clicked.connect(lambda _, item=download: self.cancel_download(item))

            layout.addLayout(download_layout)
        self.download_timer = QTimer()
        self.download_timer.timeout.connect(self.update_download_list)
        self.download_timer.start(500)
        dialog.setLayout(layout)
        dialog.exec_()

    def cancel_download(self, download):
        download.cancel()
        download_path = download.path()
        file_name = download_path.split("/")[-1]
        download_folder = download_path.rsplit('/', 1)[0]
        for filename in os.listdir(download_folder):
            if filename.startswith(file_name) and filename.endswith(".download"):
                os.remove(download_folder + "/" + filename)
        #self.downloads.remove(download)
        self.update_download_list()

    def update_download_list(self):
        for download in self.downloads:
            layout = self.download_layouts[download]
            progress_bar = layout['progress_bar']
            received_bytes = download.receivedBytes()  # Empfangene Bytes
            total_bytes = download.totalBytes()  # Gesamtgröße des Downloads

            if total_bytes > 0:
                progress = int((received_bytes / total_bytes) * 100)  # Fortschritt in Prozent berechnen
            else:
                progress = 0

            progress_bar.setValue(progress)

    def add_new_tab(self, url, title):
        def extract_username(url):
            parsed_url = urlparse(url)
            if parsed_url.username:
                return parsed_url.username
            elif parsed_url.netloc:
                netloc_parts = parsed_url.netloc.split('@')
                if len(netloc_parts) == 2:
                    return netloc_parts[0]
            return None
        def check_url_existence(url_string):
            try:
                requests.head("http://1.1.1.1/", timeout=1)
                hostname = urlparse(url_string).hostname
                username = extract_username(url_string)
                if not username == None and not self.config_allowusernamesinurl:
                    return f"file:///usr/local/share/brapy/extraerror.html?eurl={hostname}&code=b01&name={username}"
                try:
                    response = requests.get(url_string)
                    return url_string
                except requests.exceptions.RequestException as e:
                    if e.response is not None:
                        return f"file:///usr/local/share/brapy/error.html?eurl={url_string}&code={e.response.status_code}"
                    else:
                        return f"file:///usr/local/share/brapy/error.html?eurl={url_string}&code=404"
            except requests.ConnectionError:
                return f"file:///usr/local/share/brapy/extraerror.html?eurl={hostname}&code=b00"

        def check_file_existence(url_string):
            path = url_string.removeprefix("file://")
            if os.path.exists(path):
                return url_string
            else:
                return f"file:///usr/local/share/brapy/errorfile.html?file={path}"

        def load_url():
            url = self.new_tab_address_bar.text()
            if not url.startswith("file://"):
                if url.startswith("www."):
                    url = f"https://{url}"
                elif not (url.startswith("https://") or url.startswith("http://")):
                    url = f"https://{url}"
                qeurl = check_url_existence(url)
                new_tab_webview.load(QUrl(qeurl))
            else:
                if '?' in url:
                    url = url.rsplit('?', 1)
                    qeurl = check_file_existence(url[0])
                    if not qeurl.startswith("file:///usr/local/share/brapy/errorfile.html"):
                        qeurl = qeurl + "?" + url[1]
                else:
                    qeurl = check_file_existence(url)
                new_tab_webview.load(QUrl(qeurl))

        def load_curl(url):
            if not url.startswith("file://"):
                qeurl = check_url_existence(url)
                if url.startswith("www."):
                    url = f"https://{url}"
                elif not (url.startswith("https://") or url.startswith("http://")):
                    url = f"https://{url}"
                new_tab_webview.load(QUrl(qeurl))
            else:
                if '?' in url:
                    url = url.rsplit('?', 1)
                    qeurl = check_file_existence(url[0])
                    if not qeurl.startswith("file:///usr/local/share/brapy/errorfile.html"):
                        qeurl = qeurl + "?" + url[1]
                else:
                    qeurl = check_file_existence(url)
                new_tab_webview.load(QUrl(qeurl))

        def gohome():
            new_tab_webview.load(QUrl(self.homeurl))

        def search():
            search_query = new_tab_search_bar.text()
            url = f"https://duckduckgo.com/?q={search_query}"
            load_curl(url)

        def update_tab_title():
            title = new_tab_webview.page().title()
            index = self.tab_widget.currentIndex()
            if new_tab_webview.page().isAudioMuted():
                self.tab_widget.setTabText(index, " " + title)
            else:
                self.tab_widget.setTabText(index, title)
            self.setWindowTitle(title + " - " + APP_NAME)

        def update_address_bar(url):
            url_text = url.toString()
            if url_text.startswith("file:///usr/local/share/brapy/error.html") or url_text.startswith("file:///usr/local/share/brapy/extraerror.html"):
                url_text = "Fehler beim Laden der Webseite"
            elif url_text.startswith("file:///usr/local/share/brapy/errorfile.html"):
                url_text = "Fehler beim Laden der Datei"
            elif url_text.startswith("file:///usr/local/share/brapy/upgrade.html"):
                url_text = "Upgrade abgeschlossen"
            elif url_text == "file:///usr/local/share/brapy/home.html" or url_text.startswith("file:///usr/local/share/brapy/homeupdate.html"):
                url_text = ""
            elif url_text.startswith("file://"):
                url_text = check_file_existence(url_text)
                if url_text.startswith("file:///usr/local/share/brapy/errorfile.html"):
                    new_tab_webview.load(QUrl(url_text))
                    print(f"Thats odd! {url_text}")
            elif url_text.startswith("https://") or url_text.startswith("http://"):
                url_text = check_url_existence(url_text)
                if url_text.startswith("file:///usr/local/share/brapy/error.html") or url_text.startswith("file:///usr/local/share/brapy/extraerror.html"):
                    new_tab_webview.load(QUrl(url_text))
                    print(f"Thats odd! {url_text}")
            self.new_tab_address_bar.setText(url_text)
            self.new_tab_address_bar.setCursorPosition(0)  # Cursor auf den Anfang des Texts setzen

        def close_tab(index):
            self.tab_widget.removeTab(index)
            tabs_file_path = os.path.expanduser("~/.config/brapy/tabs.json")
            if self.tab_widget.count() == 0:
                if os.path.exists(tabs_file_path):
                    os.remove(tabs_file_path)
                sys.exit()

        def goback():
            new_tab_webview.back()

        def goforward():
            new_tab_webview.forward()

        def reload():
            new_tab_webview.reload()

        def download_requested(download):
            url = download.url().host()
            path = download.path()
            file_name = QUrl(path).fileName()
            default_path = QDir.homePath() + "/Downloads/" + file_name

            dialog = DownloadDialog(url, file_name, self)
            dialog.path_lineedit.setText(default_path)
            if dialog.exec_() == QDialog.Accepted:
                file_path = dialog.path_lineedit.text()
                download.setPath(file_path)
                download.accept()
                self.downloads.append(download)

        # Widget für neue Registerkarte erstellen
        new_tab_widget = QWidget()
        new_tab_layout = QVBoxLayout()
        new_tab_address_layout = QHBoxLayout()
        new_tab_widget.setLayout(new_tab_layout)

        # Neue Registerkarte zum Tab-Widget hinzufügen
        self.tab_widget.addTab(new_tab_widget, title)

        # Adressleiste zur neuen Registerkarte hinzufügen
        self.new_tab_address_bar = LineEdit()
        new_tab_search_bar = QLineEdit()
        new_tab_back_button = QPushButton("")
        new_tab_back_button.setFont(QFont('Material Icons Outlined', 12))
        new_tab_forward_button = QPushButton("")
        new_tab_forward_button.setFont(QFont('Material Icons Outlined', 12))
        new_tab_reload_button = QPushButton("")
        new_tab_reload_button.setFont(QFont('Material Icons Outlined', 12))
        new_tab_home_button = QPushButton("")
        new_tab_home_button.setFont(QFont('Material Icons Outlined', 12))
        new_tab_upgrade_button = QPushButton(" Update auf " + self.lastversion)
        new_tab_upgrade_button.setFixedHeight(26)
        new_tab_forward_button.setFixedSize(30, 26)
        new_tab_reload_button.setFixedSize(30, 26)
        new_tab_back_button.setFixedSize(30, 26)
        new_tab_home_button.setFixedSize(30, 26)
        new_tab_search_bar.setFixedWidth(500)
        new_tab_upgrade_button.clicked.connect(self.upgrade)
        new_tab_home_button.clicked.connect(gohome)
        new_tab_back_button.clicked.connect(goback)
        new_tab_reload_button.clicked.connect(reload)
        new_tab_forward_button.clicked.connect(goforward)
        self.new_tab_address_bar.setPlaceholderText("Hier URL eingeben")
        new_tab_search_bar.setPlaceholderText("Suchen")
        self.new_tab_address_bar.returnPressed.connect(load_url)
        new_tab_search_bar.returnPressed.connect(search)
        new_tab_address_layout.addWidget(new_tab_back_button)
        new_tab_address_layout.addWidget(new_tab_forward_button)
        new_tab_address_layout.addWidget(new_tab_reload_button)
        new_tab_address_layout.addWidget(new_tab_home_button)
        new_tab_address_layout.addWidget(self.new_tab_address_bar)
        new_tab_address_layout.addWidget(new_tab_search_bar)
        if self.updateavailable:
            new_tab_address_layout.addWidget(new_tab_upgrade_button)
        new_tab_layout.addLayout(new_tab_address_layout)

        # Webview zur neuen Registerkarte hinzufügen
        new_tab_webview = QWebEngineView()
        new_tab_layout.addWidget(new_tab_webview)

        # Signal zum Aktualisieren der Adressleiste in der neuen Registerkarte verbinden
        profile = QWebEngineProfile.defaultProfile()
        profile.downloadRequested.connect(download_requested)
        new_tab_webview.urlChanged.connect(update_address_bar)
        new_tab_webview.titleChanged.connect(update_tab_title)
        new_tab_webview.page().audioMutedChanged.connect(self.upmutebutton)
        load_curl(url)
        # Aktuelle Registerkarte auf die neue Registerkarte umschalten
        self.tab_widget.setCurrentWidget(new_tab_widget)

        # Schließen-Knopf zur Registerkarte hinzufügen
        close_button = QPushButton("")
        close_button.setFont(QFont('Material Icons Outlined', 12))
        close_button.setFixedSize(20, 20)  # Größe des Knopfs anpassen
        close_button.clicked.connect(lambda: close_tab(self.tab_widget.indexOf(new_tab_widget)))
        tab_bar = self.tab_widget.tabBar()
        tab_bar.setTabButton(self.tab_widget.indexOf(new_tab_widget), QTabBar.RightSide, close_button)

        # Knopfgröße für alle Registerkarten anpassen
        tab_bar.setStyleSheet("QTabBar::close-button { width: 20px; height: 20px; margin: 0px; padding: 0px; }")

        close_tab_action = QAction("Close Tab", self)
        close_tab_action.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_W))
        close_tab_action.triggered.connect(lambda: close_tab(self.tab_widget.indexOf(new_tab_widget)))
        new_tab_webview.addAction(close_tab_action)

        goback_action = QAction("Go Back", self)
        goback_action.setShortcut(QKeySequence(Qt.ALT + Qt.Key_Left))
        goback_action.triggered.connect(goback)
        new_tab_webview.addAction(goback_action)

        goforward_action = QAction("Go Forward", self)
        goforward_action.setShortcut(QKeySequence(Qt.ALT + Qt.Key_Right))
        goforward_action.triggered.connect(goforward)
        new_tab_webview.addAction(goforward_action)

        reload_action = QAction("Reload", self)
        reload_action.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_R))
        reload_action.triggered.connect(reload)
        new_tab_webview.addAction(reload_action)

        reload2_action = QAction("Reload", self)
        reload2_action.setShortcut(QKeySequence(Qt.Key_F5))
        reload2_action.triggered.connect(reload)
        new_tab_webview.addAction(reload2_action)

        gohome_action = QAction("Go Home", self)
        gohome_action.setShortcut(QKeySequence(Qt.ALT + Qt.Key_Home))
        gohome_action.triggered.connect(gohome)
        new_tab_webview.addAction(gohome_action)
        
        if url == "file:///usr/local/share/brapy/home.html" or url.startswith("file:///usr/local/share/brapy/homeupdate.html"):
            self.new_tab_address_bar.setFocus()

# def trace(message: str):
#     global TRACE
#     if TRACE:
#         print(message)

def show_console_help_option():
    print(APP_NAME + " - " + APP_DESCR)
    print("")
    print("Version: " + APP_NAME + " " + APP_VERSION)
    print("")
    print("Aufruf: " + APP_NAME + " [OPTIONEN]")
    print("")
    print("Optionen:")
    print("  -h, --help                    Hilfeoptionen anzeigen")
    print("  -v, --version                 Version der Anwendung anzeigen")
    # print("  -t, --trace                   Debuginformationen in der Konsole ausgeben")
    print("")

def read_commandline_args(argv):
    try:
        # opts, args = getopt.getopt(argv, "hvt", ["help", "version", "trace"])
        opts, args = getopt.getopt(argv, "hv", ["help", "version"])

    except getopt.GetoptError as err:
        print(f"GetoptError: {err}")
        show_console_help_option()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            show_console_help_option()
            sys.exit()
        else:

            if opt in ("-v", "--version"):
                print("brapy " + APP_VERSION)
                sys.exit()
            # if opt in ("-t", "--trace"):
            #     global TRACE
            #     TRACE = True

def main(argv):
    app = QApplication(sys.argv)

    read_commandline_args(argv)

    browser = WebBrowser()
    browser.show()

    return app.exec_()

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

